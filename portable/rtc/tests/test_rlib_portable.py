# PORTABLE VERSION, generiert von tools/make_portable.py. NICHT VON HAND AENDERN.
# Quelle (eingefroren): 01_forschung/00_gemeinsam/rlib/tests/test_rlib.py  sha256 09161614ebb7d53eb7ce4a80ecdc51d1deab9fabd6b4b2e1950f3750b114af2f
# Regeln: paths. Arbeitsbereich: AURUM_ROOT (Default: Ordner '../..' relativ zu dieser Datei).
import os as _aos; _AR = _aos.environ.get("AURUM_ROOT") or _aos.path.abspath(_aos.path.join(_aos.path.dirname(_aos.path.abspath(__file__)), "../.."))
"""Unit- und Look-ahead-Tests fuer rlib v1.0 (Cross-Coin). Synthetische Daten, keine Marktdaten."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, _AR + "/rtc"); import rlib as R; Y = R.Y


def synth(n=900, seed=3):
    rng = np.random.default_rng(seed); r = rng.normal(0, 0.01, n); c = 100 * np.exp(np.cumsum(r))
    o = np.concatenate([[100], c[:-1]]); h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.004, n))); l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.004, n)))
    v = rng.lognormal(0, 0.5, n); t = pd.date_range("2021-01-01", periods=n, freq="4h", tz="UTC")
    return pd.DataFrame(dict(t=t, open=o, high=h, low=l, close=c, volume=v))


def test_k1_atr_definition():
    df = synth(); C = R.cfg_alt(); f = R.features(df, C)
    t = 500; hh = df.high.to_numpy()[t - 120:t].max(); atrp = f.atr_prev.iat[t]
    exp = (df.close.iat[t] - hh) / atrp
    assert abs(f.dd120_atr.iat[t] - exp) < 1e-12
    assert bool(f.k1.iat[t]) == (exp <= -6.0)
    # BTC-Modus reproduziert die alte Definition
    Cb = R.cfg_btc_stufeA(); fb = R.features(df, Cb)
    assert bool(fb.k1.iat[t]) == (df.close.iat[t] / hh - 1 <= -0.12)


def test_at_low_atr():
    df = synth(); C = R.cfg_alt(); f = R.features(df, C); t = 600
    l = df.low.to_numpy(); ll = l[t - 120:t - 2].min(); lmin3 = l[t - 2:t + 1].min()
    assert bool(f.at_low.iat[t]) == (lmin3 <= ll + 1.0 * f.atr_prev.iat[t])


def test_penetration_atr():
    df = synth(); C = R.cfg_alt(); f = R.features(df, C)
    # Kerze konstruieren: Niveau L, Tief knapp unter L - 0.05 ATR, Schluss ueber L, langer unterer Docht
    t = 400; ap = f.atr_prev.iat[t]; L = 100.0
    df.loc[t, ["open", "close", "high", "low"]] = [L + 0.5 * ap, L + 0.6 * ap, L + 0.7 * ap, L - 0.06 * ap]
    f = R.features(df, C)
    hit = R.failed_breakdown(t, df, f, (L, None, None), C)
    assert hit and hit[0][0] == "swing"
    df.loc[t, "low"] = L - 0.04 * ap; f = R.features(df, C)
    assert R.failed_breakdown(t, df, f, (L, None, None), C) == []


def test_triggers():
    df = synth(); C = R.cfg_alt(); t = 300
    assert R.trigger(t, df, "T0") == t + 1
    c = df.close.to_numpy()
    lvl = c[t + 1] - 1e-9   # t+1 schliesst ueber dem Niveau -> Einstieg t+2
    assert R.trigger(t, df, "TB", lvl, C) == t + 2
    lvl = max(c[t + 1:t + 7]) + 1   # kein Reclaim in 6 Kerzen -> None
    assert R.trigger(t, df, "TB", lvl, C) is None
    assert R.trigger(t, df, "TB", np.nan, C) is None


def test_exit_ed_uses_only_completed_days():
    df = synth(1200, 5); C = R.cfg_alt(); f = R.features(df, C); lo, hi = Y.swings(df)
    # atr_d der Kerze b haengt nur von Tagen vor dem Tag von b ab: Stoerung des laufenden Tages darf atr_d nicht aendern
    b = 700; day = df.t.dt.floor("D"); same = (day == day.iat[b]).to_numpy()
    df2 = df.copy(); df2.loc[same, "high"] *= 1.5; f2 = R.features(df2, C)
    assert np.isclose(f.atr_d.iat[b], f2.atr_d.iat[b])
    # Simulation mit ED laeuft und endet, MFE/MAE konsistent
    e = 650; stop0 = df.low.iat[e] * 0.97
    tr = R.simulate_trade(e, stop0, df, f, lo, "ED", "K1", C)
    assert tr["x"] >= e and tr["reason"] in ("stop_init", "stop", "stop_gap", "chandelier_d", "structure_d", "cut")


def test_exit_e0():
    df = synth(1200, 7); C = R.cfg_alt(); f = R.features(df, C); lo, hi = Y.swings(df)
    e = 500; stop0 = df.low.iat[e] * 0.5   # Stop fern, damit E0 greift
    tr = R.simulate_trade(e, stop0, df, f, lo, "E0", "K1", C)
    assert tr["reason"] in ("ema20", "time30") and tr["bars"] <= 31


def test_lookahead_candidates_and_trades():
    """Stoerung aller Kerzen nach T aendert keine Kandidaten und Trades, die vor T abgeschlossen sind."""
    df = synth(1500, 11); C = R.cfg_alt(); T = 1100
    f = R.features(df, C); lo, hi = Y.swings(df); cy = R.candidates_y1_y3(df, f, lo, C, start=140)
    df2 = df.copy(); rng = np.random.default_rng(1); m = rng.uniform(0.9, 1.1, len(df) - T)
    for col in ("open", "high", "low", "close"): df2.loc[T:, col] = df2.loc[T:, col].to_numpy() * m
    df2.loc[T:, "volume"] *= 3
    f2 = R.features(df2, C); lo2, hi2 = Y.swings(df2); cy2 = R.candidates_y1_y3(df2, f2, lo2, C, start=140)
    k = C["swing_k"]
    pre = cy.t < T - k   # Kandidaten, deren Swing-Bestaetigung vor T liegt
    for col in ("ctx", "y1", "y3", "fb_any", "y3_any"):
        assert (cy.loc[pre, col].to_numpy() == cy2.loc[pre, col].to_numpy()).all(), col
    for trig, ex in (("T0", "EU"), ("TB", "EU"), ("T0", "ED"), ("T0", "E0")):
        tr, _ = R.run_sleeve(cy[cy.y1 | cy.y3].assign(kind="Y1"), df, f, lo, "Y1", trig, ex, "K1", C)
        tr2, _ = R.run_sleeve(cy2[cy2.y1 | cy2.y3].assign(kind="Y1"), df2, f2, lo2, "Y1", trig, ex, "K1", C)
        a = tr[tr.x < T - k - 1]; b = tr2[tr2.x < T - k - 1]
        assert len(a) == len(b) and np.allclose(a.r_net.to_numpy(), b.r_net.to_numpy()), (trig, ex)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
