"""
Project Aurum II — DELAYED-TREND P&L, Library v1.0. Spezifikation: ../dt_pnl_spec_v1.0.md (eingefroren).
Neu gegenueber den eingefrorenen Libraries: nur der DT-Exit (Spec §6) und die Kontrollen mit Ersatzniveaus (Spec §8).
Einstiege, Fill-, Kosten-, Matching-, Diagnose- und Statusregeln stammen unveraendert aus rlib v1.0, dtlib v1.0 und eval_cross.py.
"""
import numpy as np, pandas as pd

CHAND_K = 3.0; TIME_STOP = 360; WINDOW = 180; ERS_L = 120; ERS_P = 18


def costs(Y, venue):
    """Kostenszenarien: K0/K1/K2 aus spot_r (ylib.COST); Kraken-Venue maker_plan (=K1), taker_K2 (=K2), maker_entry_taker_stop (Entwurf)."""
    import aurum_costs as _ac
    v = _ac.load("venue_kraken")["spot_long_scenarios"]
    out = {k: dict(fee_in=Y.COST[k]["fee"], fee_out=Y.COST[k]["fee"], fee_out_cut=Y.COST[k]["fee"], fric=Y.COST[k]["fric"], slip_in=Y.COST[k]["slip_in"], slip_sl=Y.COST[k]["slip_sl"]) for k in ("K0", "K1", "K2")}
    m = v["maker_plan"]; t = v["taker_K2"]; d = v["maker_entry_taker_stop"]
    out["kraken_maker_plan"] = dict(fee_in=m["fee"], fee_out=m["fee"], fee_out_cut=m["fee"], fric=m["fric"], slip_in=m["slip_in"], slip_sl=m["slip_sl"])
    out["kraken_taker_K2"] = dict(fee_in=t["fee"], fee_out=t["fee"], fee_out_cut=t["fee"], fric=t["fric"], slip_in=t["slip_in"], slip_sl=t["slip_sl"])
    out["kraken_maker_entry_taker_stop"] = dict(fee_in=d["fee_entry"], fee_out=d["fee_exit_stop"], fee_out_cut=d["fee_exit_target"], fric=d["fric"], slip_in=d["slip_in"], slip_sl=d["slip_sl"])
    return out


def simulate_dt(e, stop0, t_ctx, df, atr_d, K):
    """DT-Exit (Spec §6). atr_d: Tages-ATR14 des Vortages je 4h-Kerze (rlib.features 'atr_d'). Liest fuer die Entscheidung an Kerze b nur Kerzen <= b."""
    o, h, l, c = (df[k].to_numpy() for k in ("open", "high", "low", "close")); n = len(df)
    entry = o[e] * (1 + K["slip_in"]); R = entry - stop0
    mfe = h[e] - entry; mae = entry - l[e]; exit_px = None; exit_b = None; reason = None
    if l[e] <= stop0:
        exit_px = (o[e] if o[e] <= stop0 else stop0) * (1 - K["slip_sl"]); exit_b = e; reason = "stop_init"
    hc = c[e]; floor = hc - CHAND_K * atr_d[e] if np.isfinite(atr_d[e]) else -np.inf
    if exit_px is None and e >= t_ctx + TIME_STOP:   # nicht erreichbar (e <= t+180), der Vollstaendigkeit halber
        exit_px, exit_b, reason = (o[e + 1] * (1 - K["slip_in"]), e + 1, "time360") if e + 1 < n else (c[e] * (1 - K["slip_in"]), e, "cut")
    b = e
    while exit_px is None:
        b += 1
        if b >= n:
            exit_px = c[n - 1] * (1 - K["slip_in"]); exit_b = n - 1; reason = "cut"; break
        S = max(stop0, floor)
        if o[b] <= S:
            exit_px = o[b] * (1 - K["slip_sl"]); exit_b = b; reason = "stop_gap"; break
        if l[b] <= S:
            exit_px = S * (1 - K["slip_sl"]); exit_b = b; reason = "stop" if S == stop0 else "chandelier_d"; break
        mfe = max(mfe, h[b] - entry); mae = max(mae, entry - l[b])
        hc = max(hc, c[b])
        if np.isfinite(atr_d[b]):
            floor = max(floor, hc - CHAND_K * atr_d[b])
        if b >= t_ctx + TIME_STOP:
            if b + 1 < n:
                exit_px = o[b + 1] * (1 - K["slip_in"]); exit_b = b + 1; reason = "time360"
            else:
                exit_px = c[b] * (1 - K["slip_in"]); exit_b = b; reason = "cut"
            break
    fee_out = K["fee_out_cut"] if reason == "cut" else K["fee_out"]
    fees = entry * (K["fee_in"] + K["fric"]) + exit_px * (fee_out + K["fric"]); pnl = exit_px - entry - fees
    return dict(e=int(e), x=int(exit_b), entry=float(entry), stop0=float(stop0), R=float(R), exit=float(exit_px), reason=reason,
                r_net=float(pnl / R), r_gross=float((exit_px - entry) / R), mfe_r=float(mfe / R), mae_r=float(mae / R), bars=int(exit_b - e))


def run_cell(ent, df, atr_d, K, atr4):
    """Eine Position je Zelle (Spec §5): Einstiege nach e geordnet, Einstieg nur wenn e > x des letzten Trades."""
    ent = ent.sort_values(["e", "t"]).reset_index(drop=True); trades = []; log = []; open_until = -1
    for _, r in ent.iterrows():
        e = int(r.e); t = int(r.t)
        if e <= open_until:
            log.append(dict(t=t, e=e, status="in_position")); continue
        tr = simulate_dt(e, float(r.stop), t, df, atr_d, K)
        tr.update(t=t, stop_dist_atr=float((df["open"].iat[e] - r.stop) / atr4[t]), struct_bar=int(r.struct_bar) if np.isfinite(r.struct_bar) else -1)
        trades.append(tr); open_until = tr["x"]; log.append(dict(t=t, e=e, status="traded"))
    return pd.DataFrame(trades), pd.DataFrame(log)


def substitute_levels(cb, df):
    """Spec §8: Ersatz-L_ref = min(L, c-120..c), Ersatz-P = max(H, c-18..c)."""
    h = df["high"].to_numpy(); l = df["low"].to_numpy()
    return float(l[max(0, cb - ERS_L): cb + 1].min()), float(h[max(0, cb - ERS_P): cb + 1].max())


def ctx_end(cb, l_ref, df):
    """Invalidierung und Kontextende wie dtlib.contexts."""
    c = df["close"].to_numpy(); n = len(df); k = -1
    for j in range(cb + 1, min(n, cb + WINDOW + 1)):
        if c[j] < l_ref: k = j; break
    return min(k if k >= 0 else n, cb + WINDOW, n - 1), k


def control_entry(cb, fam, df, atr4, swing_lows, D):
    l_ref, P = substitute_levels(cb, df); end, inv = ctx_end(cb, l_ref, df); a = float(atr4[cb])
    d = D.dt1(cb, l_ref, a, end, df, atr4, swing_lows) if fam == "DT1" else D.dt2(cb, P, a, end, df, atr4)
    d.update(l_ref=l_ref, P=P, end_bar=int(end), inv_bar=int(inv))
    if d["status"] == "entry" and df["open"].iat[int(d["e"])] <= d["stop"]:
        d["status"] = "entry_below_stop"
    return d


def run_controls(match, fam, df, atr_d, atr4, swing_lows, D, K):
    rows = []
    for _, mr in match.iterrows():
        for cb in mr.ctrls:
            d = control_entry(int(cb), fam, df, atr4, swing_lows, D)
            base = dict(sig_t=int(mr.t), ctrl_t=int(cb), l_ref=d["l_ref"], P=d["P"], end_bar=d["end_bar"], inv_bar=d["inv_bar"])
            if d["status"] != "entry":
                base["status"] = d["status"]; rows.append(base); continue
            tr = simulate_dt(int(d["e"]), float(d["stop"]), int(cb), df, atr_d, K); tr.update(base); tr.update(status="traded", t=int(cb), struct_bar=int(d["struct_bar"]))
            rows.append(tr)
    return pd.DataFrame(rows)
