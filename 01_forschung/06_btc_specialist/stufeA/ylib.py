"""
Project Aurum II — BTC YAMATO RTC, Stufe A. Deterministische Library.
Eingefroren: btc_yamato_rtc_research_plan_v1.0.md, yamato_stufeA_freeze_v1.0.md,
Umsetzungsentscheide yamato_stufeA_umsetzungsentscheide_v1.md (U1 bis U20).
Version 1.1 (17.09.2026): Y2 ohne 3-ATR-Abbruchgrenze (Plan v1.1 Abschnitt 13a), sonst unveraendert.
Alle Merkmale der Kerze t verwenden ausschliesslich Kerzen <= t. Keine Optimierung, keine Parameter ausserhalb FROZEN.
"""
import numpy as np
import pandas as pd

FROZEN = dict(
    atr_n=14, ema_n=50, vol_n=60,
    k1_dd=-0.12, k1_win=120, k2_ext=-2.0, k2_look=6, k3_atr=1.0, als_tol=1.02,
    swing_k=3, level_age=240, nbar_win=120, zone_tol=0.5, zone_touch=3,
    fb_pen=0.001, fb_wick_atr=0.5, fb_wick_body=1.5,
    y3_wick_atr=1.0, y3_wick_body=2.0, y3_cl=0.60, y3_volz=1.5,
    db_max_age=240, db_min_sep=12, db_tol_lo=0.5, db_tol_hi=1.0, db_neck=2.0, db_dup=12,
    stop_pad=0.5, stop_max=3.0, chand_k=3.0,
    ctrl_win=540, ctrl_min_gap=12, ctrl_dd=0.03, ctrl_ext=0.5, ctrl_n=3,
    cut="2023-12-31T20:00:00Z", block_p2="2021-01-01T00:00:00Z",
)
COST = {
    "K0": dict(fee=0.0016, fric=0.0, slip_in=0.0, slip_sl=0.0),
    "K1": dict(fee=0.0040, fric=0.0002, slip_in=0.0005, slip_sl=0.0010),
    "K2": dict(fee=0.0080, fric=0.0006, slip_in=0.0015, slip_sl=0.0030),
}
WARMUP = FROZEN["atr_n"] + FROZEN["k1_win"]   # 134 Kerzen ohne Kandidaten


# ----------------------------------------------------------------------------
# Daten und Basismerkmale
# ----------------------------------------------------------------------------

def load(path):
    """Discovery-Code darf keine Validation-Datei laden (Governance v1, Punkt 4). Freigabe nur mit AURUM_VALIDATION=1."""
    import os
    if "validation" in os.path.basename(path).lower() and os.environ.get("AURUM_VALIDATION") != "1":
        raise PermissionError(f"Validation-Datei im Discovery-Kontext gesperrt: {path}")
    df = pd.read_csv(path)
    df["t"] = pd.to_datetime(df["t"], utc=True)
    for c in ("open", "high", "low", "close", "volume"):
        df[c] = df[c].astype(float)
    return df.reset_index(drop=True)


def wilder_atr(h, l, c, n):
    tr = np.empty(len(h)); tr[0] = h[0] - l[0]
    tr[1:] = np.maximum.reduce([h[1:] - l[1:], np.abs(h[1:] - c[:-1]), np.abs(l[1:] - c[:-1])])
    atr = np.full(len(h), np.nan)
    if len(h) >= n:
        atr[n - 1] = tr[:n].mean()
        for i in range(n, len(h)):
            atr[i] = (atr[i - 1] * (n - 1) + tr[i]) / n
    return atr


def ema(x, n):
    out = np.full(len(x), np.nan); a = 2.0 / (n + 1)
    if len(x) >= n:
        out[n - 1] = x[:n].mean()
        for i in range(n, len(x)):
            out[i] = a * x[i] + (1 - a) * out[i - 1]
    return out


def rolling_max_prev(x, win, end_off=1):
    """max(x[t-win .. t-end_off]) je t, NaN wenn Fenster nicht voll."""
    out = np.full(len(x), np.nan)
    for t in range(win + end_off - 1, len(x)):
        out[t] = x[t - win - end_off + 1: t - end_off + 1].max()
    return out


def rolling_min_prev(x, win, end_off=1):
    out = np.full(len(x), np.nan)
    for t in range(win + end_off - 1, len(x)):
        out[t] = x[t - win - end_off + 1: t - end_off + 1].min()
    return out


def features(df):
    F = FROZEN
    o, h, l, c, v = (df[k].to_numpy() for k in ("open", "high", "low", "close", "volume"))
    n = len(df)
    atr = wilder_atr(h, l, c, F["atr_n"])
    atr_prev = np.concatenate([[np.nan], atr[:-1]])
    e50 = ema(c, F["ema_n"])
    body = np.abs(c - o); rng = h - l
    uw = h - np.maximum(o, c); lw = np.minimum(o, c) - l
    with np.errstate(invalid="ignore", divide="ignore"):
        cl = np.where(rng > 0, (c - l) / rng, np.nan)
        lw_atr = lw / atr_prev; uw_atr = uw / atr_prev
        ext = (c - e50) / atr_prev
    hh120 = rolling_max_prev(h, F["k1_win"], 1)
    dd120 = c / hh120 - 1.0
    ll_struct = rolling_min_prev(l, F["nbar_win"], 3)          # min(L, t-120..t-3)
    lmin3 = np.full(n, np.nan)
    for t in range(2, n):
        lmin3[t] = l[t - 2:t + 1].min()
    at_low = (lmin3 <= F["als_tol"] * ll_struct)
    # volume z 60
    volz = np.full(n, np.nan)
    for t in range(F["vol_n"], n):
        w = v[t - F["vol_n"]:t]; sd = w.std(ddof=0)
        volz[t] = (v[t] - w.mean()) / sd if sd > 0 else np.nan
    # K2: ext <= -2 on any of t-5..t
    k2 = np.zeros(n, bool)
    for t in range(n):
        lo = max(0, t - F["k2_look"] + 1); w = ext[lo:t + 1]
        k2[t] = np.nanmin(w) <= F["k2_ext"] if np.isfinite(w).any() else False
    k1 = dd120 <= F["k1_dd"]
    out = pd.DataFrame(dict(atr=atr, atr_prev=atr_prev, ema50=e50, body=body, rng=rng, uw=uw, lw=lw, cl=cl,
                            lw_atr=lw_atr, uw_atr=uw_atr, ext=ext, hh120=hh120, dd120=dd120, ll_struct=ll_struct,
                            at_low=at_low, volz=volz, k1=k1, k2=k2))
    return out


# ----------------------------------------------------------------------------
# Swings und Niveaus
# ----------------------------------------------------------------------------

def swings(df):
    """Bestaetigte Swing Lows/Highs (strikt, U3). Liefert Arrays der Indizes s; bekannt ab s+3."""
    l = df["low"].to_numpy(); h = df["high"].to_numpy(); k = FROZEN["swing_k"]; n = len(df)
    lows, highs = [], []
    for s in range(k, n - k):
        if l[s] < l[s - k:s].min() and l[s] < l[s + 1:s + k + 1].min():
            lows.append(s)
        if h[s] > h[s - k:s].max() and h[s] > h[s + 1:s + k + 1].max():
            highs.append(s)
    return np.array(lows, int), np.array(highs, int)


def levels_at(t, df, feat, swing_lows):
    """Niveaus Stand t-1 (U4): swing_low_level, nbar_low_level, zone_low_level (oder None)."""
    F = FROZEN; l = df["low"].to_numpy(); c = df["close"].to_numpy(); k = F["swing_k"]
    atr_prev = feat["atr_prev"].iat[t]
    known = swing_lows[(swing_lows + k <= t - 1) & (t - swing_lows <= F["level_age"])]
    swing_level = float(l[known[-1]]) if len(known) else None
    nbar_level = float(feat["ll_struct"].iat[t]) if np.isfinite(feat["ll_struct"].iat[t]) else None
    zone_level = None
    if len(known) >= F["zone_touch"] and np.isfinite(atr_prev):
        lv = l[known]; zones = []
        for s in known:
            band = np.abs(lv - l[s]) <= F["zone_tol"] * atr_prev
            if band.sum() >= F["zone_touch"]:
                zones.append(float(np.median(lv[band])))
        if zones:
            zones = sorted(set(zones)); below = [z for z in zones if z <= c[t]]
            zone_level = max(below) if below else min(zones)
    return swing_level, nbar_level, zone_level


# ----------------------------------------------------------------------------
# Kandidaten
# ----------------------------------------------------------------------------

def k3_ok(t, df, feat, lv):
    c = df["close"].iat[t]; atr_prev = feat["atr_prev"].iat[t]
    if bool(feat["at_low"].iat[t]):
        return True
    if not np.isfinite(atr_prev):
        return False
    return any(L is not None and abs(c - L) / atr_prev <= FROZEN["k3_atr"] for L in lv)


def context_at(t, df, feat, swing_lows):
    lv = levels_at(t, df, feat, swing_lows)
    return bool(feat["k1"].iat[t]) and bool(feat["k2"].iat[t]) and k3_ok(t, df, feat, lv), lv


def failed_breakdown(t, df, feat, lv):
    F = FROZEN; l = df["low"].iat[t]; c = df["close"].iat[t]
    lw = feat["lw"].iat[t]; b = feat["body"].iat[t]; lwa = feat["lw_atr"].iat[t]
    if not (np.isfinite(lwa) and lwa >= F["fb_wick_atr"] and lw >= F["fb_wick_body"] * b):
        return []
    hit = []
    for name, L in zip(("swing", "nbar", "zone"), lv):
        if L is not None and l <= L * (1 - F["fb_pen"]) and c > L:
            hit.append(name)
    return hit


def y3_flag(t, feat):
    F = FROZEN
    lwa = feat["lw_atr"].iat[t]; lw = feat["lw"].iat[t]; b = feat["body"].iat[t]
    cl = feat["cl"].iat[t]; vz = feat["volz"].iat[t]
    return bool(np.isfinite(lwa) and lwa >= F["y3_wick_atr"] and lw >= F["y3_wick_body"] * b
                and np.isfinite(cl) and cl >= F["y3_cl"] and np.isfinite(vz) and vz >= F["y3_volz"])


def candidates_y1_y3(df, feat, swing_lows, start=None):
    """Kandidaten Y1 (Failed Breakdown) und Y3 (Wick+Volumen) sowie Kontext-Kerzen (fuer Kontrollen)."""
    n = len(df); rows = []
    start = WARMUP if start is None else start
    for t in range(start, n):
        ctx, lv = context_at(t, df, feat, swing_lows)
        fb = failed_breakdown(t, df, feat, lv)
        y3 = y3_flag(t, feat)
        rows.append(dict(t=t, ctx=ctx, y1=bool(ctx and fb), y1_levels="|".join(fb), y3=bool(ctx and y3),
                         fb_any=bool(fb), y3_any=y3, lv_swing=lv[0], lv_nbar=lv[1], lv_zone=lv[2]))
    return pd.DataFrame(rows)


def candidates_y2(df, feat, swing_lows, swing_highs, start=None):
    """Double/Triple Bottom nach Sakata-Spez. Abschnitt 2 und U7/U8. Kandidat = Nackenlinien-Bruchkerze."""
    F = FROZEN; l = df["low"].to_numpy(); h = df["high"].to_numpy(); c = df["close"].to_numpy(); n = len(df)
    k = F["swing_k"]; start = WARMUP if start is None else start
    out = []; last_cand_t = -10 ** 9
    sl = list(swing_lows); sh = swing_highs
    for j, s2 in enumerate(sl):
        if s2 + k >= n or s2 < start:
            continue
        atr_s = feat["atr_prev"].iat[s2]
        if not np.isfinite(atr_s):
            continue
        # juengstes qualifizierendes s1 (U8)
        pair = None
        for s1 in reversed(sl[:j]):
            if s2 - s1 < F["db_min_sep"]:
                continue
            if s2 - s1 > F["db_max_age"]:
                break
            if not (l[s2] >= l[s1] - F["db_tol_lo"] * atr_s and l[s2] <= l[s1] + F["db_tol_hi"] * atr_s):
                continue
            mid = sh[(sh > s1) & (sh < s2)]
            if len(mid) == 0:
                continue
            h1 = int(mid[np.argmax(h[mid])])
            if h[h1] - max(l[s1], l[s2]) < F["db_neck"] * atr_s:
                continue
            pair = (s1, h1); break
        if pair is None:
            continue
        s1, h1 = pair; N = h[h1]
        # Kontext auf s2 (U7)
        ctx, lv = context_at(s2, df, feat, swing_lows)
        # Verfall/Bruch scannen ab s2+3
        expired = False; cand_t = None
        for t in range(s2 + k, n):
            if c[t] < l[s2] - F["db_tol_lo"] * atr_s or t - s1 > F["db_max_age"]:
                expired = True; break
            if c[t] > N:
                cand_t = t; break
        if cand_t is None:
            continue
        thirds = [s3 for s3 in sl[:j] if s3 < s1 and (s2 - s3 <= 360) and abs(l[s3] - l[s2]) <= F["db_tol_hi"] * atr_s]
        triple = len(thirds) > 0
        gyaku = bool(triple and l[s1] < l[s2] and l[s1] < l[thirds[-1]])
        out.append(dict(t=cand_t, s1=s1, s2=s2, h1=h1, neck=N, ctx=ctx, triple=triple, gyaku=gyaku))
    if not out:
        return pd.DataFrame(columns=["t", "s1", "s2", "h1", "neck", "ctx", "triple", "gyaku", "dup", "y2"])
    # Zeitordnung (U8): je Kerze t nur das Paar mit juengstem s2, danach keine zweite Kandidatenkerze innerhalb 12 Kerzen
    res = pd.DataFrame(out).sort_values(["t", "s2"], ascending=[True, False]).reset_index(drop=True)
    dup = []; last_t = -10 ** 9; seen_t = set()
    for _, r in res.iterrows():
        if r["t"] in seen_t or (r["t"] - last_t) < F["db_dup"]:
            dup.append(True)
        else:
            dup.append(False); last_t = r["t"]; seen_t.add(r["t"])
    res["dup"] = dup
    res["y2"] = res["ctx"] & ~res["dup"]
    return res


# ----------------------------------------------------------------------------
# Trigger, Stop, Simulation E-U
# ----------------------------------------------------------------------------

def trigger_ta(t, df):
    """C_{t+1} > H_t -> Einstiegskerze t+2, sonst None."""
    if t + 2 >= len(df):
        return None
    return t + 2 if df["close"].iat[t + 1] > df["high"].iat[t] else None


def simulate_trade(e, stop0, df, feat, swing_lows, cost="K1"):
    """Position ab Eroeffnung von Kerze e, Exit nach E-U (U12, U13). Liefert dict."""
    F = FROZEN; C = COST[cost]
    o, h, l, c = (df[k].to_numpy() for k in ("open", "high", "low", "close"))
    atr = feat["atr"].to_numpy(); n = len(df); k = F["swing_k"]
    entry_raw = o[e]; entry = entry_raw * (1 + C["slip_in"])
    R = entry - stop0
    hh = h[e]; floor = hh - F["chand_k"] * atr[e]; stop = stop0
    mfe = h[e] - entry; mae = entry - l[e]
    # Einstiegskerze: nur initialer Stop
    exit_px = None; exit_b = None; reason = None
    if l[e] <= stop0:
        exit_px = (o[e] if o[e] <= stop0 else stop0) * (1 - C["slip_sl"]); exit_b = e; reason = "stop_init"
    b = e
    while exit_px is None:
        b += 1
        if b >= n:
            exit_px = c[n - 1] * (1 - C["slip_in"]); exit_b = n - 1; reason = "cut"; break
        S = max(stop0, floor)
        if o[b] <= S:
            exit_px = o[b] * (1 - C["slip_sl"]); exit_b = b; reason = "stop_gap"; break
        if l[b] <= S:
            exit_px = S * (1 - C["slip_sl"]); exit_b = b; reason = "stop" if S == stop0 else "chandelier"; break
        mfe = max(mfe, h[b] - entry); mae = max(mae, entry - l[b])
        hh = max(hh, h[b]); floor = max(floor, hh - F["chand_k"] * atr[b])
        # Strukturbruch: juengstes Swing Low s >= e mit s+3 <= b
        sw = swing_lows[(swing_lows >= e) & (swing_lows + k <= b)]
        if len(sw) and c[b] < l[sw[-1]]:
            if b + 1 < n:
                exit_px = o[b + 1] * (1 - C["slip_in"]); exit_b = b + 1; reason = "structure"
            else:
                exit_px = c[b] * (1 - C["slip_in"]); exit_b = b; reason = "cut"
            break
    fees = (entry + exit_px) * (C["fee"] + C["fric"])
    pnl = exit_px - entry - fees
    return dict(e=e, x=exit_b, entry=entry, stop0=stop0, R=R, exit=exit_px, reason=reason,
                r_net=pnl / R, r_gross=(exit_px - entry) / R, mfe_r=mfe / R, mae_r=mae / R, bars=exit_b - e)


def run_sleeve(cands, df, feat, swing_lows, kind, cost="K1"):
    """Ein Sleeve je Hypothese (U11): Kandidaten in Zeitfolge, eine Position, Trigger TA (Y1, Y3) oder Bruchkerze (Y2)."""
    F = FROZEN; atr = feat["atr"].to_numpy(); l = df["low"].to_numpy(); o = df["open"].to_numpy(); n = len(df)
    trades = []; log = []; open_until = -1
    for _, r in cands.iterrows():
        t = int(r["t"])
        rec = dict(t=t, kind=kind)
        if t <= open_until:
            rec["status"] = "in_position"; log.append(rec); continue
        if kind == "Y2":
            e = t + 1 if t + 1 < n else None; low_ref = l[int(r["s2"])]
        else:
            e = trigger_ta(t, df); low_ref = l[t]
        if e is None:
            rec["status"] = "no_trigger" if t + 2 < n or kind == "Y2" else "cut"; log.append(rec); continue
        stop0 = low_ref - F["stop_pad"] * atr[t]
        entry_raw = o[e]
        if kind != "Y2" and entry_raw - stop0 > F["stop_max"] * atr[t]:   # v1.1: Y2 ohne Abbruchgrenze
            rec["status"] = "stop_too_wide"; log.append(rec); continue
        if entry_raw <= stop0:
            rec["status"] = "entry_below_stop"; log.append(rec); continue
        tr = simulate_trade(e, stop0, df, feat, swing_lows, cost)
        tr.update(t=t, kind=kind, stop_dist_atr=(entry_raw - stop0) / atr[t]); trades.append(tr)
        open_until = tr["x"]; rec["status"] = "traded"; rec["e"] = e; log.append(rec)
    return pd.DataFrame(trades), pd.DataFrame(log)


# ----------------------------------------------------------------------------
# Kontrollgruppe (U15)
# ----------------------------------------------------------------------------

def control_pool(cy13, y2df, df, feat):
    """Kontext-Kerzen ohne eines der drei Muster und nicht im Boden eines gueltigen Y2-Paares."""
    F = FROZEN; k = F["swing_k"]
    pool = cy13[cy13["ctx"] & ~cy13["fb_any"] & ~cy13["y3_any"]]["t"].to_numpy()
    excl = set()
    if len(y2df):
        for _, r in y2df.iterrows():
            excl.add(int(r["t"]))
            for s in range(int(r["s2"]) - k, int(r["s2"]) + k + 1):
                excl.add(s)
    pool = np.array([t for t in pool if t not in excl], int)
    return pool


def match_controls(signals, pool, feat, positions):
    """signals: DataFrame mit t (Kandidatenkerze) je gehandeltem Signal. positions: Liste (e, x) offener Fenster derselben Hypothese."""
    F = FROZEN; dd = feat["dd120"].to_numpy(); ex = feat["ext"].to_numpy()
    rows = []
    for _, s in signals.iterrows():
        t = int(s["t"])
        ok = pool[(np.abs(pool - t) <= F["ctrl_win"]) & (np.abs(pool - t) > F["ctrl_min_gap"])]
        ok = ok[(np.abs(dd[ok] - dd[t]) <= F["ctrl_dd"]) & (np.abs(ex[ok] - ex[t]) <= F["ctrl_ext"])]
        ok = np.array([c for c in ok if not any(e <= c <= x for e, x in positions)], int)
        order = sorted(ok, key=lambda c: (abs(dd[c] - dd[t]), abs(c - t)))
        chosen = []
        for c in order:
            if all(abs(c - d) > F["ctrl_min_gap"] for d in chosen):
                chosen.append(int(c))
            if len(chosen) == F["ctrl_n"]:
                break
        rows.append(dict(t=t, n_ctrl=len(chosen), ctrls=chosen, n_pool_window=len(ok)))
    return pd.DataFrame(rows)
