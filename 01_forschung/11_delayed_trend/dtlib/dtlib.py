"""
Project Aurum II — DELAYED-TREND Library, Version 1.0 (outcome-blind).
Spezifikation: delayed_trend_measurement_spec_v1.0.md. Berechnet Kontexte, Einstiege (DT1/DT2/DT3), Stops und Geometrie.
Enthaelt KEINE Trade-Simulation: nichts nach der Einstiegskerze e wird gelesen (ausser O_e).
"""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/home/claude/rtc"); sys.path.insert(0, "/home/claude/yamato")
import rlib as R; Y = R.Y

P = dict(window=180, hl_min_above_ref_atr=0.5, hl_min_rise_atr=1.0, rt_tol_atr=0.25, rt_fail_atr=0.5, box_bars=18, box_max_atr=3.0,
         stop_pad_atr=0.5, target_lookback=120, k1_roundtrip_stop_bp=99.0, k1_roundtrip_target_bp=89.0)


def contexts(cy, y2, df, feat):
    """Kontexte S1 (Double Bottom, y2=True) und S2 (Failed Breakdown, y1=True). Rueckgabe DataFrame: src, t, l_ref, level, ref (Zielreferenz), atr_t, h_pre."""
    h = df["high"].to_numpy(); l = df["low"].to_numpy(); atr = feat["atr"].to_numpy(); hh120 = feat["hh120"].to_numpy(); n = len(df)
    rows = []
    for _, r in y2[y2.y2].iterrows():
        t, s2 = int(r.t), int(r.s2)
        rows.append(dict(src="S1", t=t, l_ref=float(l[s2]), level=float(r.neck), ref=s2, atr_t=float(atr[t]), h_pre=float(hh120[s2]) if np.isfinite(hh120[s2]) else np.nan))
    for _, r in cy[cy.y1].iterrows():
        t = int(r.t)
        rows.append(dict(src="S2", t=t, l_ref=float(l[t]), level=float(r.tb_lvl_y1), ref=t, atr_t=float(atr[t]), h_pre=float(hh120[t]) if np.isfinite(hh120[t]) else np.nan))
    ctx = pd.DataFrame(rows).sort_values(["src", "t"]).reset_index(drop=True)
    # Invalidierung: erste Kerze k > t mit C_k < l_ref; Kontextende = min(k, t+window)
    c = df["close"].to_numpy(); inv = []; end = []
    for _, r in ctx.iterrows():
        t = int(r.t); k = -1
        for j in range(t + 1, min(n, t + P["window"] + 1)):
            if c[j] < r.l_ref: k = j; break
        inv.append(k); end.append(min(k if k >= 0 else n, t + P["window"], n - 1))
    ctx["inv_bar"] = inv; ctx["end_bar"] = end   # Einstieg e muss e <= end_bar erfuellen (inv_bar-Eroeffnung noch handelbar)
    return ctx


def dt1(t, l_ref, atr_t, end_bar, df, atr, swing_lows):
    """Higher Low: erstes bestaetigtes Swing Low s (t < s, s+3 <= t+window), L_s >= l_ref + 0.5 ATR_t, max(H,t..s) >= L_s + 1.0 ATR_t, e = s+4 <= end_bar."""
    h = df["high"].to_numpy(); l = df["low"].to_numpy(); n = len(df)
    for s in swing_lows[(swing_lows > t) & (swing_lows + 3 <= t + P["window"])]:
        s = int(s)
        if l[s] < l_ref + P["hl_min_above_ref_atr"] * atr_t: continue
        if h[t: s + 1].max() < l[s] + P["hl_min_rise_atr"] * atr_t: continue
        e = s + 4
        if e > end_bar or e >= n: return dict(status="window_or_invalidated", detail=int(s))
        stop = l[s] - P["stop_pad_atr"] * atr[s + 3]
        return dict(status="entry", e=e, stop=float(stop), struct_bar=s)
    return dict(status="no_higher_low")


def dt2(t, level, atr_t, end_bar, df, atr):
    """Retest and Hold: b >= t+3 mit L_b <= P+0.25ATR_t, C_b >= P-0.5ATR_t; Hold C_{b+1} > P; e = b+2. Gescheiterter Retest beendet die Familie."""
    h = df["high"].to_numpy(); l = df["low"].to_numpy(); c = df["close"].to_numpy(); n = len(df); failed_holds = 0
    b = t + 3
    while b + 2 <= min(end_bar, t + P["window"], n - 1):
        if l[b] <= level + P["rt_tol_atr"] * atr_t:
            if c[b] < level - P["rt_fail_atr"] * atr_t: return dict(status="retest_failed", detail=int(b), failed_holds=failed_holds)
            if c[b + 1] > level:
                e = b + 2
                if e > end_bar: return dict(status="window_or_invalidated", detail=int(b), failed_holds=failed_holds)
                stop = min(l[b], l[b + 1]) - P["stop_pad_atr"] * atr[b + 1]
                return dict(status="entry", e=e, stop=float(stop), struct_bar=int(b), failed_holds=failed_holds)
            failed_holds += 1
            # Hold-Kerze selbst kann ein gescheiterter Retest sein: naechste Iteration prueft b+1 regulaer
        b += 1
    return dict(status="no_retest_hold", failed_holds=failed_holds)


def dt3(t, l_ref, atr_t, end_bar, df, atr):
    """Consolidation Breakout: Box t+1..t+18, Breite <= 3.0 ATR_t, box_low > l_ref; Breakout erster Schluss > box_high ab t+19; e = b+1; Stop box_low - 0.5 ATR_b."""
    h = df["high"].to_numpy(); l = df["low"].to_numpy(); c = df["close"].to_numpy(); n = len(df); B = P["box_bars"]
    if t + B >= n: return dict(status="cut")
    bh = h[t + 1: t + B + 1].max(); bl = l[t + 1: t + B + 1].min()
    if bh - bl > P["box_max_atr"] * atr_t or bl <= l_ref: return dict(status="no_consolidation", box_width_atr=float((bh - bl) / atr_t))
    for b in range(t + B + 1, min(end_bar, t + P["window"], n - 2) + 1):
        if c[b] > bh:
            e = b + 1
            if e > end_bar: return dict(status="window_or_invalidated", detail=int(b))
            return dict(status="entry", e=e, stop=float(bl - P["stop_pad_atr"] * atr[b]), struct_bar=int(b), box_high=float(bh), box_low=float(bl), box_width_atr=float((bh - bl) / atr_t))
    return dict(status="no_breakout", box_width_atr=float((bh - bl) / atr_t))


def geometry(o_e, stop, h_pre, atr_prev):
    R_ = o_e - stop
    if R_ <= 0: return dict(valid=False)
    stop_pct = R_ / o_e * 100.0; cost_R = P["k1_roundtrip_stop_bp"] / (stop_pct * 100.0)
    dist = h_pre - o_e if np.isfinite(h_pre) else np.nan
    rr_gross = max(0.0, dist / R_) if np.isfinite(dist) else np.nan
    rr_net = (dist - P["k1_roundtrip_target_bp"] / 1e4 * o_e) / (R_ + P["k1_roundtrip_stop_bp"] / 1e4 * o_e) if np.isfinite(dist) else np.nan
    return dict(valid=True, R=float(R_), stop_atr=float(R_ / atr_prev), stop_pct=float(stop_pct), cost_R_K1=float(cost_R), dist_target_atr=float(dist / atr_prev) if np.isfinite(dist) else np.nan,
                dist_target_pct=float(dist / o_e * 100) if np.isfinite(dist) else np.nan, rr_geo_gross=float(rr_gross) if np.isfinite(rr_gross) else np.nan,
                rr_geo_net_K1=float(rr_net) if np.isfinite(rr_net) else np.nan, p_be_geo=float(1 / (1 + rr_net)) if (np.isfinite(rr_net) and rr_net > 0) else np.nan,
                target_below_entry=bool(np.isfinite(dist) and dist <= 0))


def entries(ctx, df, feat, swing_lows, coin):
    """Alle Einstiege je Kontext und Familie (erster gueltiger). Liest keine Kerze > e ausser O_e."""
    o = df["open"].to_numpy(); atr = feat["atr"].to_numpy(); atrp = feat["atr_prev"].to_numpy(); rows = []
    for _, r in ctx.iterrows():
        t = int(r.t); base = dict(coin=coin, src=r.src, t=t, l_ref=r.l_ref, level=r.level, atr_t=r.atr_t, h_pre=r.h_pre, inv_bar=int(r.inv_bar), end_bar=int(r.end_bar))
        for fam, fn in (("DT1", lambda: dt1(t, r.l_ref, r.atr_t, int(r.end_bar), df, atr, swing_lows)), ("DT2", lambda: dt2(t, r.level, r.atr_t, int(r.end_bar), df, atr)), ("DT3", lambda: dt3(t, r.l_ref, r.atr_t, int(r.end_bar), df, atr))):
            d = fn(); row = dict(base); row["fam"] = fam; row["status"] = d["status"]
            for k in ("detail", "failed_holds", "box_width_atr", "struct_bar"):
                if k in d: row[k] = d[k]
            if d["status"] == "entry":
                e = int(d["e"]); row.update(e=e, t_entry=str(df["t"].iat[e]), entry=float(o[e]), stop=float(d["stop"]), delay=e - t)
                if not np.isfinite(r.h_pre): row["status"] = "no_target"
                g = geometry(o[e], d["stop"], r.h_pre, atrp[e])
                if not g["valid"]: row["status"] = "entry_below_stop"
                else: row.update({k: v for k, v in g.items() if k != "valid"})
            rows.append(row)
    return pd.DataFrame(rows)
