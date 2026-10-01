# PORTABLE VERSION, generiert von tools/make_portable.py. NICHT VON HAND AENDERN.
# Quelle (eingefroren): 01_forschung/10_rebound_micro/mlib/mlib.py  sha256 6b7e7ba888e17cac80705097dd36be93a3ee6204b6ea00bd6be6f0b042bfe938
# Regeln: paths, cost:COST=spot_r. Arbeitsbereich: AURUM_ROOT (Default: Ordner '..' relativ zu dieser Datei).
import os as _aos; _AR = _aos.environ.get("AURUM_ROOT") or _aos.path.abspath(_aos.path.join(_aos.path.dirname(_aos.path.abspath(__file__)), ".."))
try:
    import aurum_costs as _ac
except ImportError:
    import sys as _asys; _asys.path.append(_aos.path.join(_AR, "pylib")); import aurum_costs as _ac
"""
Project Aurum II — REBOUND-MICRO 1h-Library, Version 1.0 (v0.1 plus ctx_override in join_4h fuer die Kontrollgruppe, sonst identisch; getrennt von rlib/ylib 4h und dlib 4h).
Spezifikation: rebound_micro_1h_feature_spec_v0.1.md, rebound_micro_research_plan_v0.1.md, equilibrium_target_research_v0.1.md.
Alle Merkmale der 1h-Kerze b verwenden ausschliesslich Kerzen <= b. Der 4h-Kontext einer 1h-Kerze stammt aus 4h-Kerzen, die vor
Beginn der 1h-Kerze abgeschlossen sind. Diese Datei enthaelt KEINE Trade-Simulation (kein Exit, kein P&L): Kandidaten, Stops,
Ziele und Geometrie sind outcome-blind.
"""
import os, numpy as np, pandas as pd

P = dict(atr_n=14, vol_n=168, ti_delta_n=6, warmup=168, search_bars_4h=6, episode_gap_4h=6,
         m1_pen_atr4h=0.05, m_stop_pad_atr1h=0.25, m2_wick_atr=1.0, m2_wick_body=2.0, m2_cl=0.60,
         m3_sellz=1.0, m3_eff=0.25, m3_turn=0.15, m3_look=6, tight_cap_atr4h=1.0, time_stop_bars=24, baseline_time_stop_4h=30,
         cut="2023-12-31T23:00:00Z")
COST = _ac.load("spot_r")  # zentral: config/cost_model_v1.json [spot_r]


def load_1h(path, cut=P["cut"]):
    if "validation" in os.path.basename(path).lower() and os.environ.get("AURUM_VALIDATION") != "1":
        raise PermissionError(path)
    df = pd.read_csv(path); df["t"] = pd.to_datetime(df["t"], utc=True)
    df = df[df["t"] <= pd.Timestamp(cut)].reset_index(drop=True)
    for c in ("open", "high", "low", "close", "volume", "quote_volume", "trades", "taker_buy_base", "taker_buy_quote"):
        df[c] = df[c].astype(float)
    return df


def wilder_atr(h, l, c, n):
    tr = np.empty(len(h)); tr[0] = h[0] - l[0]
    tr[1:] = np.maximum.reduce([h[1:] - l[1:], np.abs(h[1:] - c[:-1]), np.abs(l[1:] - c[:-1])])
    atr = np.full(len(h), np.nan)
    if len(h) >= n:
        atr[n - 1] = tr[:n].mean()
        for i in range(n, len(h)):
            atr[i] = (atr[i - 1] * (n - 1) + tr[i]) / n
    return atr


def _ts(t):
    """tz-aware Zeitstempel -> Sekunden seit Epoche (int64)."""
    idx = pd.DatetimeIndex(t).tz_convert("UTC").tz_localize(None)
    return (idx - pd.Timestamp("1970-01-01")) // pd.Timedelta(seconds=1)   # Sekunden, unabhaengig von der internen Aufloesung


def _gap_flags(t, step_s):
    """gap_before[b] = Kerze b folgt nicht unmittelbar auf b-1."""
    d = np.diff(_ts(t)); return np.concatenate([[False], d != step_s])


def _zscore_past(x, n, gapb):
    """z_b = (x_b - mean(x_{b-n..b-1})) / sd(...). NaN, wenn im Bereich b-n..b eine Luecke liegt (gap_before an b-n+1..b) oder Historie fehlt."""
    s = pd.Series(x); m = s.shift(1).rolling(n).mean(); sd = s.shift(1).rolling(n).std(ddof=0)
    g = pd.Series(gapb.astype(int)).rolling(n).sum()      # Summe gap_before ueber b-n+1..b
    return ((s - m) / sd).where((sd > 0) & (g.fillna(1) == 0)).to_numpy()


def features_1h(df):
    """Kerzengeometrie und Flow-Merkmale nach Feature-Spezifikation v0.1."""
    o, h, l, c, v = (df[k].to_numpy() for k in ("open", "high", "low", "close", "volume"))
    qv, tbq, tr_n = df["quote_volume"].to_numpy(), df["taker_buy_quote"].to_numpy(), df["trades"].to_numpy()
    n = len(df); gapb = _gap_flags(df["t"].to_numpy(), 3600)
    atr = wilder_atr(h, l, c, P["atr_n"]); atr_prev = np.concatenate([[np.nan], atr[:-1]])
    rng = h - l; body = np.abs(c - o); lw = np.minimum(o, c) - l; uw = h - np.maximum(o, c)
    with np.errstate(invalid="ignore", divide="ignore"):
        f = dict(atr=atr, atr_prev=atr_prev, range=rng, body=body, lower_wick=lw, upper_wick=uw,
                 lower_wick_atr=lw / atr_prev, lower_wick_range=np.where(rng > 0, lw / rng, np.nan), body_range=np.where(rng > 0, body / rng, np.nan),
                 close_location=np.where(rng > 0, (c - l) / rng, np.nan), range_atr=rng / atr_prev,
                 taker_imbalance=np.where(qv > 0, (2 * tbq - qv) / qv, np.nan), sell_quote=qv - tbq, buy_quote=tbq)
    ti = pd.Series(f["taker_imbalance"])
    f["delta_taker_imbalance"] = (ti - ti.shift(1).rolling(P["ti_delta_n"]).mean()).where(pd.Series(gapb.astype(int)).rolling(P["ti_delta_n"]).sum().fillna(1) == 0).to_numpy()
    f["volume_zscore"] = _zscore_past(v, P["vol_n"], gapb)
    f["trade_count_zscore"] = _zscore_past(tr_n, P["vol_n"], gapb)
    f["sell_volume_zscore"] = _zscore_past(f["sell_quote"], P["vol_n"], gapb)
    with np.errstate(invalid="ignore", divide="ignore"):
        f["downside_price_progress"] = np.maximum(0.0, o - c) / atr_prev
        f["sell_efficiency"] = f["downside_price_progress"] / np.maximum(f["sell_volume_zscore"], 0.5)
    # Diagnoseflags
    bh = np.zeros(n, bool); hk = np.zeros(n, bool)
    for b in range(3, n):
        bh[b] = (c[b - 1] < o[b - 1]) and (o[b] > c[b - 1]) and (c[b] < o[b - 1]) and (c[b] > o[b]) and (body[b] < body[b - 1])
        hk[b] = (h[b - 2] <= h[b - 3]) and (l[b - 2] >= l[b - 3]) and (l[b - 1] < l[b - 2]) and (c[b - 1] <= h[b - 2]) and (c[b] > h[b - 2])
    f["bullish_harami"] = bh; f["hikkake"] = hk; f["gap_before"] = gapb
    return pd.DataFrame(f)


# ----------------------------------------------------------------------------
# 4h -> 1h Join und Kontext
# ----------------------------------------------------------------------------

def join_4h(df1, df4, f4, cfg4, ctx_override=None):
    """v1.0: ctx_override (bool-Array je 4h-Kerze) ersetzt K1&K2&K3 als Kontextmenge (Kontrollgruppe); None = Standard, identisch mit v0.1.
    Fuer jede 1h-Kerze: Index der letzten 4h-Kerze, die VOR Beginn der 1h-Kerze abgeschlossen ist (t4_end <= t1_start).
    Liefert Arrays: idx4_last_closed, ctx_active (Suchfenster), event_id, ema20_4h (Wert am letzten abgeschlossenen 4h-Schluss),
    atr4h (der Kontextkerze des Events), levels (4 Niveaus der Kontextkerze), k1_4h (K1 der letzten abgeschlossenen 4h-Kerze)."""
    import sys; sys.path.insert(0, _AR + "/rtc"); import rlib as R; Y = R.Y
    t1 = _ts(df1["t"]); t4 = _ts(df4["t"])
    t4_end = t4 + 4 * 3600
    idx4 = np.searchsorted(t4_end, t1, side="right") - 1     # letzte 4h-Kerze mit Ende <= Beginn der 1h-Kerze
    ctx4 = (f4["k1"] & f4["k2"]).to_numpy()
    # K3 je 4h-Kerze (Niveaus Stand t-1), wie rlib.context_at; Warmup wie ylib
    lo, hi = Y.swings(df4)
    n4 = len(df4); k3 = np.zeros(n4, bool); lv_all = [None] * n4
    W = Y.WARMUP
    for t in range(W, n4):
        lv = R.Y.levels_at(t, df4, f4, lo); lv_all[t] = lv
        k3[t] = R.Y.k3_ok(t, df4, f4, lv)
    ctx4 = ctx4 & k3; ctx4[:W] = False
    k3_all = k3.copy()
    if ctx_override is not None:
        ctx4 = np.asarray(ctx_override, bool).copy(); ctx4[:W] = False
    # Suchfenster: 4h-Kerzen t+1..t+6 nach jeder Kontextkerze t (aktiv), Events = zusammenhaengende aktive Abschnitte mit Kontextkerze als Beginn
    active4 = np.zeros(n4, bool); ev4 = np.full(n4, -1); ctx_src = np.full(n4, -1); eid = -1; last_ctx = -10**9
    for t in range(n4):
        if ctx4[t]:
            if t - last_ctx > P["search_bars_4h"]: eid += 1
            last_ctx = t
        if last_ctx >= 0 and 0 < t - last_ctx <= P["search_bars_4h"]:
            active4[t] = True; ev4[t] = eid; ctx_src[t] = last_ctx
    ema20_4h = Y.ema(df4["close"].to_numpy(), 20)
    ok = idx4 >= 0
    out = dict(idx4=idx4, ctx_active=np.where(ok, active4[np.clip(idx4 + 1, 0, n4 - 1)], False), event_id=np.where(ok, ev4[np.clip(idx4 + 1, 0, n4 - 1)], -1),
               ctx_src=np.where(ok, ctx_src[np.clip(idx4 + 1, 0, n4 - 1)], -1), ema20_4h=np.where(ok, ema20_4h[np.clip(idx4, 0, n4 - 1)], np.nan),
               k1_4h=np.where(ok, f4["k1"].to_numpy()[np.clip(idx4, 0, n4 - 1)], False))
    # Hinweis: ctx_active fuer 1h-Kerze b gilt, wenn die 4h-Kerze, in die b faellt (idx4+1), im Suchfenster liegt; die Kontextkerze idx4 ist abgeschlossen.
    out["levels4"] = lv_all; out["ctx4"] = ctx4; out["k3_4"] = k3_all; out["atr4"] = f4["atr"].to_numpy(); out["low4"] = df4["low"].to_numpy(); out["open4"] = df4["open"].to_numpy(); out["ev4"] = ev4; out["ctx_src4"] = ctx_src
    return out


def avwap_episodes(df1, df4, f4, J):
    """Anchored VWAP je K1-Episode (Anker = erste 1h-Kerze der 4h-Kerze, an deren Schluss K1 false->true; Ende nach 6 4h-Kerzen K1 false).
    avwap[b] verwendet nur Kerzen anker..b. episode_id[b] = -1 ausserhalb einer Episode."""
    k1 = f4["k1"].to_numpy(); n4 = len(df4); t4 = _ts(df4["t"])
    ep4 = np.full(n4, -1); eid = -1; false_run = 10**9; in_ep = False
    for t in range(n4):
        if k1[t]:
            if not in_ep: eid += 1; in_ep = True
            false_run = 0
        else:
            false_run += 1
            if in_ep and false_run >= P["episode_gap_4h"]:
                ep4[t] = eid; in_ep = False; continue      # sechste falsche Kerze gehoert noch zur Episode, Ende an ihrem Schluss
        if in_ep: ep4[t] = eid
    # Anker-Zeit je Episode = Beginn der ersten 4h-Kerze der Episode
    anchors = {}
    for t in range(n4):
        if ep4[t] >= 0 and ep4[t] not in anchors: anchors[ep4[t]] = t4[t]
    t1 = _ts(df1["t"])
    # Episode je 1h-Kerze: Episode der 4h-Kerze, in die b faellt, aber nur, wenn die Episode am Schluss der VORHERIGEN 4h-Kerze bereits bekannt ist
    # (Anker bekannt am Schluss der Anker-4h-Kerze). Fuer 1h-Kerzen innerhalb der Anker-4h-Kerze selbst ist der Anker noch nicht bekannt -> -1.
    idx4_cur = np.searchsorted(t4, t1, side="right") - 1
    ep1 = np.full(len(df1), -1)
    for b in range(len(df1)):
        i = idx4_cur[b]
        if i < 0: continue
        e = ep4[i]
        if e < 0: continue
        if i > 0 and ep4[i - 1] == e: ep1[b] = e        # Episode war am Schluss der vorherigen 4h-Kerze bekannt
    tp = ((df1["high"] + df1["low"] + df1["close"]) / 3).to_numpy(); v = df1["volume"].to_numpy()
    av = np.full(len(df1), np.nan); cum_pv = 0.0; cum_v = 0.0; cur = -1
    # AVWAP ab Anker (einschliesslich Anker-4h-Kerze, deren 1h-Kerzen zwar keinen Q1 haben, aber in die Summe eingehen)
    ep1_sum = np.full(len(df1), -1)
    for b in range(len(df1)):
        i = idx4_cur[b]; e = ep4[i] if i >= 0 else -1
        if e != cur: cur = e; cum_pv = 0.0; cum_v = 0.0
        if e >= 0 and t1[b] >= anchors[e]:
            cum_pv += tp[b] * v[b]; cum_v += v[b]; ep1_sum[b] = e
            if cum_v > 0: av[b] = cum_pv / cum_v
    av = np.where(ep1 >= 0, av, np.nan)
    return dict(avwap=av, episode_id=ep1, ep4=ep4, anchors=anchors)


# ----------------------------------------------------------------------------
# Kandidaten M1, M2, M3 (outcome-blind: Kandidatenkerze, Einstiegskerze, Stop, Ziele, Geometrie)
# ----------------------------------------------------------------------------

def candidates(df1, f1, J, A, coin):
    o, h, l, c = (df1[k].to_numpy() for k in ("open", "high", "low", "close")); n = len(df1)
    atr1 = f1["atr"].to_numpy(); atr1p = f1["atr_prev"].to_numpy()
    lwa, lw, body, cl = f1["lower_wick_atr"].to_numpy(), f1["lower_wick"].to_numpy(), f1["body"].to_numpy(), f1["close_location"].to_numpy()
    sz, eff, dti, ti = f1["sell_volume_zscore"].to_numpy(), f1["sell_efficiency"].to_numpy(), f1["delta_taker_imbalance"].to_numpy(), f1["taker_imbalance"].to_numpy()
    gapb = f1["gap_before"].to_numpy()
    act, ev, src, ema20 = J["ctx_active"], J["event_id"], J["ctx_src"], J["ema20_4h"]
    rows = []
    # je Event: Fenster der 1h-Kerzen mit act & ev==e
    events = sorted(set(ev[act]) - {-1})
    for e in events:
        idx = np.where((ev == e) & act)[0]
        if len(idx) == 0: continue
        w0, w1 = idx[0], idx[-1]
        # Lueckenpruefung: keine Luecke innerhalb des Fensters oder in den 168 Kerzen davor (Feature-Warmup)
        gap_win = bool(gapb[max(0, w0 - P["warmup"]): w1 + 1].any())
        t4 = int(src[w0]); atr4 = J["atr4"][t4]; lv4 = J["levels4"][t4]; ctx_low = J["low4"][t4]
        levels = [x for x in (list(lv4) if lv4 is not None else []) if x is not None] + [float(ctx_low)]
        found = {}
        # M1
        for b in idx:
            if b + 1 >= n: break
            for L in levels:
                if l[b] <= L - P["m1_pen_atr4h"] * atr4 and c[b] > L:
                    below = [j for j in idx if j <= b and l[j] < L]
                    sweep_low = l[below].min() if below else l[b]
                    found["M1"] = dict(b=int(b), e=int(b + 1), stop=sweep_low - P["m_stop_pad_atr1h"] * atr1[b], level=L, sweep_low=float(sweep_low)); break
            if "M1" in found: break
        # M2
        for b in idx:
            if b + 2 >= n: break
            if np.isfinite(lwa[b]) and lwa[b] >= P["m2_wick_atr"] and lw[b] >= P["m2_wick_body"] * body[b] and np.isfinite(cl[b]) and cl[b] >= P["m2_cl"]:
                if c[b + 1] > c[b] and l[b + 1] > l[b] and (b + 1) in set(idx.tolist()):
                    found["M2"] = dict(b=int(b), e=int(b + 2), stop=l[b] - P["m_stop_pad_atr1h"] * atr1[b], rejection_low=float(l[b])); break
        # M3: Absorption a, Wende b in a+1..a+6, Reclaim c_b > h_a
        idxset = set(idx.tolist())
        for a in idx:
            if not (np.isfinite(sz[a]) and sz[a] >= P["m3_sellz"] and np.isfinite(eff[a]) and eff[a] <= P["m3_eff"]): continue
            for b in range(a + 1, min(n - 1, a + P["m3_look"] + 1)):
                if b not in idxset: break
                if np.isfinite(dti[b]) and dti[b] >= P["m3_turn"] and ti[b] >= 0 and c[b] > h[a]:
                    found["M3"] = dict(b=int(b), e=int(b + 1), stop=l[a:b + 1].min() - P["m_stop_pad_atr1h"] * atr1[b], absorb=int(a)); break
            if "M3" in found: break
        # Flow-Flag fuer M1/M2: Absorption+Wende innerhalb des Fensters bis zur Kandidatenkerze
        def flow_flag(bcand):
            for a in idx:
                if a > bcand: break
                if np.isfinite(sz[a]) and sz[a] >= P["m3_sellz"] and np.isfinite(eff[a]) and eff[a] <= P["m3_eff"]:
                    for b in range(a + 1, min(bcand, a + P["m3_look"]) + 1):
                        if np.isfinite(dti[b]) and dti[b] >= P["m3_turn"] and ti[b] >= 0: return True
            return False
        for m, d in found.items():
            e_ = d["e"]; entry = o[e_]; stop = d["stop"]; R_ = entry - stop
            q0 = ema20[e_]; q1 = A["avwap"][e_ - 1] if e_ - 1 >= 0 else np.nan
            # Baseline 4h (REBOUND-20-Umsetzung) fuer dasselbe Event: Kontextkerze t4, T0-Einstieg Eroeffnung der 4h-Kerze t4+1, Stop L_t4 - 0.5 ATR4
            rows.append(dict(coin=coin, event=int(e), mech=m, t4=t4, b=d["b"], e=e_, t_entry=str(df1["t"].iat[e_]), entry=float(entry), stop=float(stop), R=float(R_),
                             entry_to_stop_atr4=float(R_ / atr4), entry_to_stop_atr1=float(R_ / atr1[e_ - 1]) if np.isfinite(atr1[e_ - 1]) else np.nan,
                             tight=bool(R_ <= P["tight_cap_atr4h"] * atr4), valid_stop=bool(R_ > 0),
                             q0=float(q0) if np.isfinite(q0) else np.nan, q1=float(q1) if np.isfinite(q1) else np.nan,
                             entry_to_q0_atr4=float((q0 - entry) / atr4) if np.isfinite(q0) else np.nan, entry_to_q1_atr4=float((q1 - entry) / atr4) if np.isfinite(q1) else np.nan,
                             q0_above=bool(np.isfinite(q0) and q0 > entry), q1_above=bool(np.isfinite(q1) and q1 > entry), episode=int(A["episode_id"][e_]),
                             flow_flag=bool(flow_flag(d["b"])) if m != "M3" else True, gap_in_window=gap_win, ctx_low=float(ctx_low), atr4=float(atr4),
                             bullish_harami=bool(f1["bullish_harami"].iat[d["b"]]), hikkake=bool(f1["hikkake"].iat[d["b"]]),
                             baseline_entry=float(J["open4"][t4 + 1]) if t4 + 1 < len(J["open4"]) else np.nan,
                             baseline_entry_to_stop_atr4=float((J["open4"][t4 + 1] - (J["low4"][t4] - 0.5 * atr4)) / atr4) if t4 + 1 < len(J["open4"]) else np.nan))
    res = pd.DataFrame(rows)
    return res


def geometry(res, cost="K1"):
    """Geometrisches Reward/Risk und Break-even nach Kosten. Kosten in R: Rundlauf (fee+fric)*2 auf Notional + Slippage Einstieg; Stop-Slippage auf Verlustseite."""
    K = COST[cost]; out = res.copy()
    cost_in = out.entry * (K["fee"] + K["fric"] + K["slip_in"]); cost_out_target = out.entry * (K["fee"] + K["fric"]); cost_out_stop = out.entry * (K["fee"] + K["fric"] + K["slip_sl"])
    for q in ("q0", "q1"):
        reward = (out[q] - out.entry) - cost_in - cost_out_target
        risk = (out.entry - out.stop) + cost_in + cost_out_stop
        rr = reward / risk
        out[f"rr_geo_{q}"] = np.where(out[f"{q}_above"], rr, np.nan)
        out[f"pbe_geo_{q}"] = np.where(out[f"{q}_above"] & (rr > 0), 1 / (1 + rr), np.nan)
    out["cost_R"] = (cost_in + cost_out_stop) / out.R
    return out
