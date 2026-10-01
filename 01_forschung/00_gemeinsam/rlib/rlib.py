"""
Project Aurum II — RTC Cross-Coin Library, Version 1.0 (XRP v1.0, DOT v1.0, spaeter ETH/SOL; BTC Stufe B).
Baut auf ylib.py (BTC YAMATO Stufe A v1.1) auf und aendert dort nichts. Unterschiede sind ausschliesslich Konfiguration:
  k1_mode     "pct": dd120 = C_t/max(H,t-120..t-1) - 1 <= k1_dd            (BTC Stufe A, eingefroren)
              "atr": dd120_atr = (C_t - max(H,t-120..t-1)) / ATR14_{t-1} <= k1_dd_atr   (Entscheid 17.09.2026, Konstante -6.0)
  pen_mode    "pct": L_t <= Niveau*(1-fb_pen)      "atr": L_t <= Niveau - fb_pen_atr*ATR14_{t-1}   (0.05)
  als_mode    "pct": min(L,t-2..t) <= als_tol*min(L,t-120..t-3)   "atr": <= min(L,t-120..t-3) + als_atr*ATR14_{t-1}   (1.0)
  ctrl_mode   "pct": |dd120 - dd120_sig| <= ctrl_dd (0.03)     "atr": |dd120_atr - dd120_atr_sig| <= ctrl_dd_atr (1.5)
Trigger: TA (Stufe A), T0 (Eroeffnung t+1), TB (Reclaim: erster Schluss > Niveau in t+1..t+6, Einstieg Eroeffnung danach).
Exits:   EU (Chandelier 3 ATR14 4h + 4h-Strukturbruch), ED (Chandelier 3 Tages-ATR14 + Tages-Strukturbruch), E0 (EMA20 oder 30 Kerzen).
Alle Merkmale der Kerze t verwenden ausschliesslich Kerzen <= t. Keine Optimierung, keine Parameter ausserhalb CFG.
"""
import sys, copy
import numpy as np, pandas as pd
sys.path.insert(0, "/home/claude/yamato")
import ylib as Y

BASE = dict(Y.FROZEN)
BASE.update(k1_mode="atr", k1_dd_atr=-6.0, pen_mode="atr", fb_pen_atr=0.05, als_mode="atr", als_atr=1.0,
            ctrl_mode="atr", ctrl_dd_atr=1.5, tb_look=6, e0_ema=20, e0_bars=30, atr_d_n=14, swing_d_k=3)

def cfg_btc_stufeA():
    c = dict(BASE); c.update(k1_mode="pct", pen_mode="pct", als_mode="pct", ctrl_mode="pct"); return c

def cfg_alt():
    return dict(BASE)

BLOCKS = {
    "BTC": [("P1", "2017-08-17", "2020-12-31"), ("P2", "2021-01-01", "2023-12-31")],
    "XRP": [("P1", "2018-05-04", "2020-12-31"), ("P2", "2021-01-01", "2023-12-31")],
    "DOT": [("P2a", "2021-01-01", "2022-06-30"), ("P2b", "2022-07-01", "2023-12-31")],   # P1 (2020-08..2020-12) nicht gewertet
    "ETH": [("P1", "2017-08-17", "2020-12-31"), ("P2", "2021-01-01", "2023-12-31")],
    "SOL": [("P2a", "2021-01-01", "2022-06-30"), ("P2b", "2022-07-01", "2023-12-31")],
}

def block_of(ts, coin):
    for name, a, b in BLOCKS[coin]:
        if pd.Timestamp(a, tz="UTC") <= ts <= pd.Timestamp(b, tz="UTC") + pd.Timedelta(hours=23, minutes=59):
            return name
    return "none"


# ----------------------------------------------------------------------------
# Merkmale mit Modus
# ----------------------------------------------------------------------------

def features(df, C):
    Y.FROZEN.update({k: v for k, v in C.items() if k in Y.FROZEN})
    f = Y.features(df)
    c = df["close"].to_numpy(); l = df["low"].to_numpy(); n = len(df)
    with np.errstate(invalid="ignore", divide="ignore"):
        f["dd120_atr"] = (c - f["hh120"].to_numpy()) / f["atr_prev"].to_numpy()
    if C["k1_mode"] == "atr":
        f["k1"] = f["dd120_atr"] <= C["k1_dd_atr"]
    if C["als_mode"] == "atr":
        lmin3 = np.full(n, np.nan)
        for t in range(2, n):
            lmin3[t] = l[t - 2:t + 1].min()
        f["at_low"] = lmin3 <= f["ll_struct"].to_numpy() + C["als_atr"] * f["atr_prev"].to_numpy()
    # Tages-ATR und Tages-Swing-Lows fuer E-D (nur abgeschlossene Tage; gueltig ab der ersten Kerze des Folgetages)
    day = df["t"].dt.floor("D")
    dd = df.groupby(day).agg(o=("open", "first"), h=("high", "max"), l=("low", "min"), c=("close", "last"))
    dd["atr_d"] = Y.wilder_atr(dd["h"].to_numpy(), dd["l"].to_numpy(), dd["c"].to_numpy(), C["atr_d_n"])
    atr_d_prev_day = dd["atr_d"].shift(1)          # Wert des Vortages
    f["atr_d"] = atr_d_prev_day.reindex(day).to_numpy()
    # Tages-Swing-Lows: bestaetigt am Schluss von Tag s+k, bekannt ab Kerzen des Tages s+k+1
    dl = dd["l"].to_numpy(); k = C["swing_d_k"]; days = dd.index.to_numpy()
    dsl = [(days[s], dl[s], days[s + k]) for s in range(k, len(dl) - k) if dl[s] < dl[s - k:s].min() and dl[s] < dl[s + 1:s + k + 1].min()]
    f.attrs["daily_swing_lows"] = dsl   # (Tag s, Tief, Bestaetigungstag)
    f.attrs["cfg"] = copy.deepcopy(C)
    return f


def failed_breakdown(t, df, feat, lv, C):
    l = df["low"].iat[t]; c = df["close"].iat[t]; ap = feat["atr_prev"].iat[t]
    lw = feat["lw"].iat[t]; b = feat["body"].iat[t]; lwa = feat["lw_atr"].iat[t]
    if not (np.isfinite(lwa) and lwa >= C["fb_wick_atr"] and lw >= C["fb_wick_body"] * b):
        return []
    hit = []
    for name, L in zip(("swing", "nbar", "zone"), lv):
        if L is None:
            continue
        pen = (l <= L * (1 - C["fb_pen"])) if C["pen_mode"] == "pct" else (np.isfinite(ap) and l <= L - C["fb_pen_atr"] * ap)
        if pen and c > L:
            hit.append((name, float(L)))
    return hit


def candidates_y1_y3(df, feat, swing_lows, C, start=None):
    n = len(df); rows = []; start = Y.WARMUP if start is None else start
    for t in range(start, n):
        ctx, lv = Y.context_at(t, df, feat, swing_lows)
        fb = failed_breakdown(t, df, feat, lv, C)
        y3 = Y.y3_flag(t, feat)
        # TB-Referenzniveau: Y1 hoechstes getroffenes Niveau; Y3 ll_struct bei at_low, sonst naechstes Niveau innerhalb k3_atr
        tb_lvl_y1 = max(L for _, L in fb) if fb else np.nan
        tb_lvl_y3 = np.nan
        if y3:
            if bool(feat["at_low"].iat[t]):
                tb_lvl_y3 = float(feat["ll_struct"].iat[t])
            else:
                c = df["close"].iat[t]; ap = feat["atr_prev"].iat[t]
                near = [L for L in lv if L is not None and np.isfinite(ap) and abs(c - L) / ap <= C["k3_atr"]]
                tb_lvl_y3 = min(near, key=lambda L: abs(c - L)) if near else np.nan
        rows.append(dict(t=t, ctx=ctx, y1=bool(ctx and fb), y1_levels="|".join(nm for nm, _ in fb), y3=bool(ctx and y3),
                         fb_any=bool(fb), y3_any=y3, lv_swing=lv[0], lv_nbar=lv[1], lv_zone=lv[2], tb_lvl_y1=tb_lvl_y1, tb_lvl_y3=tb_lvl_y3))
    return pd.DataFrame(rows)


def candidates_y2(df, feat, swing_lows, swing_highs, C, start=None):
    Y.FROZEN.update({k: v for k, v in C.items() if k in Y.FROZEN})
    return Y.candidates_y2(df, feat, swing_lows, swing_highs, start)


# ----------------------------------------------------------------------------
# Trigger
# ----------------------------------------------------------------------------

def trigger(t, df, mode, level=np.nan, C=BASE):
    n = len(df)
    if mode == "T0":
        return t + 1 if t + 1 < n else None
    if mode == "TA":
        return Y.trigger_ta(t, df)
    if mode == "TB":
        if not np.isfinite(level):
            return None
        c = df["close"].to_numpy()
        for j in range(1, C["tb_look"] + 1):
            if t + j + 1 >= n:
                return None
            if c[t + j] > level:
                return t + j + 1
        return None
    raise ValueError(mode)


# ----------------------------------------------------------------------------
# Simulation mit Exit-Modus
# ----------------------------------------------------------------------------

def simulate_trade(e, stop0, df, feat, swing_lows, exit_mode="EU", cost="K1", C=BASE):
    if exit_mode == "EU":
        Y.FROZEN.update({k: v for k, v in C.items() if k in Y.FROZEN})
        return Y.simulate_trade(e, stop0, df, feat, swing_lows, cost)
    K = Y.COST[cost]
    o, h, l, c = (df[k].to_numpy() for k in ("open", "high", "low", "close")); n = len(df)
    t_idx = df["t"]
    entry_raw = o[e]; entry = entry_raw * (1 + K["slip_in"]); R = entry - stop0
    mfe = h[e] - entry; mae = entry - l[e]
    exit_px = None; exit_b = None; reason = None
    if l[e] <= stop0:
        exit_px = (o[e] if o[e] <= stop0 else stop0) * (1 - K["slip_sl"]); exit_b = e; reason = "stop_init"
    if exit_mode == "ED":
        atr_d = feat["atr_d"].to_numpy(); dsl = feat.attrs["daily_swing_lows"]
        day = df["t"].dt.floor("D").to_numpy()
        hh = h[e]; floor = hh - C["chand_k"] * atr_d[e] if np.isfinite(atr_d[e]) else -np.inf
    if exit_mode == "E0":
        ema20 = Y.ema(c, C["e0_ema"])
    b = e
    while exit_px is None:
        b += 1
        if b >= n:
            exit_px = c[n - 1] * (1 - K["slip_in"]); exit_b = n - 1; reason = "cut"; break
        S = max(stop0, floor) if exit_mode == "ED" else stop0
        if o[b] <= S:
            exit_px = o[b] * (1 - K["slip_sl"]); exit_b = b; reason = "stop_gap"; break
        if l[b] <= S:
            exit_px = S * (1 - K["slip_sl"]); exit_b = b; reason = "stop" if S == stop0 else "chandelier_d"; break
        mfe = max(mfe, h[b] - entry); mae = max(mae, entry - l[b])
        if exit_mode == "ED":
            hh = max(hh, h[b])
            if np.isfinite(atr_d[b]):
                floor = max(floor, hh - C["chand_k"] * atr_d[b])
            # Tages-Strukturbruch: juengstes Tages-Swing-Low mit Tag s >= Einstiegstag, bestaetigt vor dem Tag von b
            de = day[e]; db = day[b]
            known = [(s, lv) for s, lv, conf in dsl if s >= de and conf < db]
            if known and c[b] < known[-1][1]:
                if b + 1 < n:
                    exit_px = o[b + 1] * (1 - K["slip_in"]); exit_b = b + 1; reason = "structure_d"
                else:
                    exit_px = c[b] * (1 - K["slip_in"]); exit_b = b; reason = "cut"
                break
        if exit_mode == "E0":
            if (np.isfinite(ema20[b]) and c[b] >= ema20[b]) or (b - e) >= C["e0_bars"]:
                if b + 1 < n:
                    exit_px = o[b + 1] * (1 - K["slip_in"]); exit_b = b + 1; reason = "ema20" if c[b] >= ema20[b] else "time30"
                else:
                    exit_px = c[b] * (1 - K["slip_in"]); exit_b = b; reason = "cut"
                break
    fees = (entry + exit_px) * (K["fee"] + K["fric"]); pnl = exit_px - entry - fees
    return dict(e=e, x=exit_b, entry=entry, stop0=stop0, R=R, exit=exit_px, reason=reason,
                r_net=pnl / R, r_gross=(exit_px - entry) / R, mfe_r=mfe / R, mae_r=mae / R, bars=exit_b - e)


def run_sleeve(cands, df, feat, swing_lows, kind, trig="T0", exit_mode="EU", cost="K1", C=BASE):
    """Ein Sleeve je Hypothese und Konfiguration. Y2/X2/D2: Trigger ist der Nackenlinienbruch (Einstieg t+1), trig wird ignoriert."""
    atr = feat["atr"].to_numpy(); l = df["low"].to_numpy(); o = df["open"].to_numpy(); n = len(df)
    trades = []; log = []; open_until = -1
    for _, r in cands.iterrows():
        t = int(r["t"]); rec = dict(t=t, kind=kind, trig=trig, exit=exit_mode)
        if t <= open_until:
            rec["status"] = "in_position"; log.append(rec); continue
        if kind in ("Y2", "X2", "D2"):
            e = t + 1 if t + 1 < n else None; low_ref = l[int(r["s2"])]
        else:
            lvl = r.get("tb_lvl_y1" if kind in ("Y1", "X1", "D1") else "tb_lvl_y3", np.nan) if trig == "TB" else np.nan
            e = trigger(t, df, trig, lvl, C); low_ref = l[t]
        if e is None:
            rec["status"] = "no_trigger"; log.append(rec); continue
        stop0 = low_ref - C["stop_pad"] * atr[t]; entry_raw = o[e]
        if kind not in ("Y2", "X2", "D2") and entry_raw - stop0 > C["stop_max"] * atr[t]:
            rec["status"] = "stop_too_wide"; log.append(rec); continue
        if entry_raw <= stop0:
            rec["status"] = "entry_below_stop"; log.append(rec); continue
        tr = simulate_trade(e, stop0, df, feat, swing_lows, exit_mode, cost, C)
        tr.update(t=t, kind=kind, trig=trig, exit_mode=exit_mode, stop_dist_atr=(entry_raw - stop0) / atr[t]); trades.append(tr)
        open_until = tr["x"]; rec["status"] = "traded"; rec["e"] = e; log.append(rec)
    return pd.DataFrame(trades), pd.DataFrame(log)


# ----------------------------------------------------------------------------
# Kontrollen
# ----------------------------------------------------------------------------

def match_controls(signals, pool, feat, positions, C):
    key = "dd120" if C["ctrl_mode"] == "pct" else "dd120_atr"; tol = C["ctrl_dd"] if C["ctrl_mode"] == "pct" else C["ctrl_dd_atr"]
    dd = feat[key].to_numpy(); ex = feat["ext"].to_numpy(); rows = []
    for _, s in signals.iterrows():
        t = int(s["t"])
        ok = pool[(np.abs(pool - t) <= C["ctrl_win"]) & (np.abs(pool - t) > C["ctrl_min_gap"])]
        ok = ok[(np.abs(dd[ok] - dd[t]) <= tol) & (np.abs(ex[ok] - ex[t]) <= C["ctrl_ext"])]
        ok = np.array([c for c in ok if not any(e <= c <= x for e, x in positions)], int)
        order = sorted(ok, key=lambda c: (abs(dd[c] - dd[t]), abs(c - t)))
        chosen = []
        for c in order:
            if all(abs(c - d) > C["ctrl_min_gap"] for d in chosen):
                chosen.append(int(c))
            if len(chosen) == C["ctrl_n"]:
                break
        rows.append(dict(t=t, n_ctrl=len(chosen), ctrls=chosen, n_pool_window=len(ok)))
    return pd.DataFrame(rows)


def run_controls(match, sig_t, df, feat, swing_lows, trig, exit_mode, C, cost="K1"):
    """Kontrollen mit demselben Trigger und Exit. TB auf Kontrollen: Referenz ll_struct (kein Muster-Niveau vorhanden)."""
    l = df["low"].to_numpy(); o = df["open"].to_numpy(); atr = feat["atr"].to_numpy(); rows = []
    for (_, mr), st in zip(match.iterrows(), sig_t):
        for cb in mr.ctrls:
            lvl = float(feat["ll_struct"].iat[cb]) if trig == "TB" else np.nan
            e = trigger(cb, df, trig, lvl, C)
            if e is None:
                rows.append(dict(sig_t=st, ctrl_t=cb, status="no_trigger")); continue
            stop0 = l[cb] - C["stop_pad"] * atr[cb]
            if o[e] - stop0 > C["stop_max"] * atr[cb] or o[e] <= stop0:
                rows.append(dict(sig_t=st, ctrl_t=cb, status="stop_too_wide")); continue
            tr = simulate_trade(e, stop0, df, feat, swing_lows, exit_mode, cost, C); tr.update(sig_t=st, ctrl_t=cb, t=cb, status="traded"); rows.append(tr)
    return pd.DataFrame(rows)
