"""Unit- und Look-ahead-Tests mlib v0.1 (synthetische Daten, keine Marktdaten)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/home/claude/micro"); sys.path.insert(0, "/home/claude/rtc")
import mlib as M; import rlib as R; Y = R.Y


def synth_1h(n=4000, seed=1, start="2021-01-01"):
    rng = np.random.default_rng(seed); r = rng.normal(0, 0.004, n); c = 100 * np.exp(np.cumsum(r)); o = np.concatenate([[100], c[:-1]])
    h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.002, n))); l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.002, n)))
    v = rng.lognormal(0, 0.5, n); qv = v * c; tbq = qv * rng.uniform(0.3, 0.7, n); tr = rng.integers(50, 500, n)
    t = pd.date_range(start, periods=n, freq="1h", tz="UTC")
    return pd.DataFrame(dict(t=t, open=o, high=h, low=l, close=c, volume=v, quote_volume=qv, trades=tr, taker_buy_base=v * 0.5, taker_buy_quote=tbq))


def agg_4h(df1):
    g = df1.assign(t4=df1.t.dt.floor("4h")).groupby("t4")
    d = g.agg(open=("open", "first"), high=("high", "max"), low=("low", "min"), close=("close", "last"), volume=("volume", "sum")).reset_index().rename(columns={"t4": "t"})
    return d


def test_features_hand():
    df = synth_1h(300); f = M.features_1h(df); b = 250
    o, h, l, c = df.open.iat[b], df.high.iat[b], df.low.iat[b], df.close.iat[b]
    assert np.isclose(f.lower_wick.iat[b], min(o, c) - l) and np.isclose(f.close_location.iat[b], (c - l) / (h - l))
    qv, tbq = df.quote_volume.iat[b], df.taker_buy_quote.iat[b]; assert np.isclose(f.taker_imbalance.iat[b], (2 * tbq - qv) / qv)
    v = df.volume.to_numpy(); w = v[b - 168:b]; assert np.isclose(f.volume_zscore.iat[b], (v[b] - w.mean()) / w.std())
    sq = (df.quote_volume - df.taker_buy_quote).to_numpy(); w = sq[b - 168:b]; assert np.isclose(f.sell_volume_zscore.iat[b], (sq[b] - w.mean()) / w.std())
    ti = f.taker_imbalance.to_numpy(); assert np.isclose(f.delta_taker_imbalance.iat[b], ti[b] - ti[b - 6:b].mean())
    dpp = max(0, o - c) / f.atr_prev.iat[b]; assert np.isclose(f.downside_price_progress.iat[b], dpp)
    assert np.isclose(f.sell_efficiency.iat[b], dpp / max(f.sell_volume_zscore.iat[b], 0.5))
    assert np.isnan(f.volume_zscore.iat[100]) and np.isnan(f.atr.iat[5])   # Mindesthistorie


def test_denominator_and_gap():
    df = synth_1h(400); df.loc[300, "quote_volume"] = 0.0; f = M.features_1h(df); assert np.isnan(f.taker_imbalance.iat[300])
    # Nenner-Regel: sell_volume_zscore stark negativ -> Nenner 0.5
    df2 = synth_1h(400); f2 = M.features_1h(df2); b = 350
    z = f2.sell_volume_zscore.iat[b]
    if z < 0.5: assert np.isclose(f2.sell_efficiency.iat[b], f2.downside_price_progress.iat[b] / 0.5)
    # Luecke: Kerze 250 entfernen -> Merkmale mit Fenster ueber die Luecke NaN
    df3 = synth_1h(600).drop(index=250).reset_index(drop=True); f3 = M.features_1h(df3)
    assert bool(f3.gap_before.iat[250]) and np.isnan(f3.volume_zscore.iat[260]) and np.isnan(f3.delta_taker_imbalance.iat[252]) and np.isfinite(f3.volume_zscore.iat[250 + 168])


def test_join_4h_uses_only_closed_bars():
    df1 = synth_1h(2400); df4 = agg_4h(df1); C = R.cfg_alt(); f4 = R.features(df4, C)
    J = M.join_4h(df1, df4, f4, C)
    t1 = df1.t.to_numpy(); t4 = df4.t.to_numpy()
    for b in (700, 1301, 2003):
        i = J["idx4"][b]; assert t4[i] + np.timedelta64(4, "h") <= t1[b] and t4[i + 1] + np.timedelta64(4, "h") > t1[b]
    # Stoerung der 1h-Kerzen >= b aendert Join-Ausgaben < b nicht (4h aus 1h neu aggregiert)
    b = 1600; df1b = df1.copy(); df1b.loc[b:, ["open", "high", "low", "close"]] *= 1.2; df4b = agg_4h(df1b); f4b = R.features(df4b, C); Jb = M.join_4h(df1b, df4b, f4b, C)
    # 4h-Kerze, die b enthaelt, ist bei idx4[b]+1; alle Ausgaben fuer 1h-Kerzen in frueheren 4h-Kerzen identisch
    cut = np.where(J["idx4"] + 1 < J["idx4"][b] + 1)[0]
    for k in ("ctx_active", "event_id", "ema20_4h", "k1_4h"):
        a, bb = np.asarray(J[k])[cut], np.asarray(Jb[k])[cut]; assert np.array_equal(np.nan_to_num(a.astype(float), nan=-9), np.nan_to_num(bb.astype(float), nan=-9)), k


def test_avwap_hand_and_reset():
    df1 = synth_1h(2400, seed=5); df4 = agg_4h(df1); C = R.cfg_alt(); f4 = R.features(df4, C)
    # K1 kuenstlich setzen: wahr fuer 4h-Kerzen 200..205, falsch 206..212 (7 Kerzen -> Ende), wahr 213..215
    k1 = np.zeros(len(df4), bool); k1[200:206] = True; k1[213:216] = True; f4 = f4.copy(); f4["k1"] = k1
    J = M.join_4h(df1, df4, f4, C); A = M.avwap_episodes(df1, df4, f4, J)
    ep4 = A["ep4"]; assert ep4[200] == 0 and ep4[211] == 0 and ep4[212] == -1 and ep4[213] == 1   # 6 falsche Kerzen 206..211 -> Ende am Schluss von 211
    # AVWAP von Hand: 1h-Kerzen der 4h-Kerzen 200 und 201 (8 Kerzen), Wert an letzter 1h-Kerze von 201
    t_anchor = df4.t.iat[200]; idx = np.where((df1.t >= t_anchor) & (df1.t < df4.t.iat[202]))[0]
    tp = ((df1.high + df1.low + df1.close) / 3).to_numpy(); v = df1.volume.to_numpy()
    hand = (tp[idx] * v[idx]).sum() / v[idx].sum(); assert np.isclose(A["avwap"][idx[-1]], hand)
    # Innerhalb der Anker-4h-Kerze kein Q1 (Anker noch nicht bekannt)
    idx0 = np.where((df1.t >= t_anchor) & (df1.t < df4.t.iat[201]))[0]; assert np.all(A["episode_id"][idx0] == -1) and np.all(np.isnan(A["avwap"][idx0]))
    # Look-ahead: Stoerung nach Kerze b aendert avwap[b] nicht
    b = idx[-1]; df1b = df1.copy(); df1b.loc[b + 1:, "volume"] *= 5; df1b.loc[b + 1:, "close"] *= 1.1; Ab = M.avwap_episodes(df1b, df4, f4, J)
    assert np.isclose(A["avwap"][b], Ab["avwap"][b])


def test_candidates_lookahead():
    df1 = synth_1h(6000, seed=11); df4 = agg_4h(df1); C = R.cfg_alt(); f4 = R.features(df4, C)
    f1 = M.features_1h(df1); J = M.join_4h(df1, df4, f4, C); A = M.avwap_episodes(df1, df4, f4, J)
    res = M.candidates(df1, f1, J, A, "SYN")
    T = 4000; df1b = df1.copy(); rng = np.random.default_rng(3)
    for col in ("open", "high", "low", "close"): df1b.loc[T:, col] = df1b.loc[T:, col].to_numpy() * rng.uniform(0.9, 1.1, len(df1b) - T)
    df1b.loc[T:, "volume"] *= 3; df1b.loc[T:, "quote_volume"] *= 3; df1b.loc[T:, "taker_buy_quote"] *= 2
    df4b = agg_4h(df1b); f4b = R.features(df4b, C); f1b = M.features_1h(df1b); Jb = M.join_4h(df1b, df4b, f4b, C); Ab = M.avwap_episodes(df1b, df4b, f4b, Jb)
    resb = M.candidates(df1b, f1b, Jb, Ab, "SYN")
    # Kandidaten mit Einstieg e < T - 4 (und Fenster vor T) identisch
    a = res[res.e < T - 4].reset_index(drop=True); b = resb[resb.e < T - 4].reset_index(drop=True)
    assert len(a) == len(b), (len(a), len(b))
    for col in ("mech", "t4", "b", "e", "entry", "stop", "q0", "q1"):
        x, y = a[col].to_numpy(), b[col].to_numpy()
        if col == "mech": assert (x == y).all(), col; continue
        else: assert np.allclose(np.nan_to_num(x.astype(float), nan=-9), np.nan_to_num(y.astype(float), nan=-9)), col


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
