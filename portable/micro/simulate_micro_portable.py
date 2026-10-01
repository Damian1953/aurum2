# PORTABLE VERSION, generiert von tools/make_portable.py. NICHT VON HAND AENDERN.
# Quelle (eingefroren): 01_forschung/10_rebound_micro/mlib/simulate_micro.py  sha256 fef60859063dd8bc77505346bdc8c5b373e7e635e978feb4994f13160887ab8e
# Regeln: paths, sha_self. Arbeitsbereich: AURUM_ROOT (Default: Ordner '..' relativ zu dieser Datei).
import os as _aos; _AR = _aos.environ.get("AURUM_ROOT") or _aos.path.abspath(_aos.path.join(_aos.path.dirname(_aos.path.abspath(__file__)), ".."))
_FROZEN_SELF = _aos.path.join(_aos.path.dirname(_aos.path.abspath(__file__)), "simulate_micro.py")  # eingefrorenes Original im Arbeitsbereich
"""
Project Aurum II — REBOUND-MICRO Trade-Simulation und Lauf je Coin, Version 1.0.
Spezifikation: rebound_micro_spec_v1.0.md Abschnitte 3 bis 6. Long only, 1h-Kerzen, festes Limit-Ziel, Stop-Market, Zeitstopp 24 Kerzen.
Aufruf: python3 simulate_micro.py COIN  -> run/{COIN}_trades.csv, run/{COIN}_baseline.csv, run/{COIN}_controls.csv, run/{COIN}_run.log
"""
import os, sys, json, hashlib, time, numpy as np, pandas as pd
sys.path.insert(0, _AR + "/micro"); sys.path.insert(0, _AR + "/rtc")
import mlib as M; import rlib as R; Y = R.Y

HOLD = 24                      # abgeschlossene 1h-Kerzen nach Einstieg
DIAG_BARS_20D, DIAG_BARS_30D = 480, 720


def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()


def simulate(o, h, l, c, e, stop, target, K, hold=HOLD):
    """Ein Trade. Gibt dict mit exit_b, exit_px, reason, r_net, cost_R, R, entry_fill zurueck. Reihenfolge je Kerze nach Spec 4."""
    n = len(o); entry_raw = o[e]; entry = entry_raw * (1 + K["slip_in"]); R_ = entry - stop
    fee = K["fee"] + K["fric"]
    def close_out(px, b, reason, slip_ref):
        fees = (entry + px) * fee; pnl = px - entry - fees
        cost = fees + (entry - entry_raw) + (slip_ref - px)
        return dict(exit_b=int(b), exit_px=float(px), reason=reason, r_net=float(pnl / R_), cost_R=float(cost / R_), R=float(R_), entry_fill=float(entry), entry_raw=float(entry_raw))
    if R_ <= 0: return dict(exit_b=int(e), exit_px=np.nan, reason="invalid_stop", r_net=np.nan, cost_R=np.nan, R=float(R_), entry_fill=float(entry), entry_raw=float(entry_raw))
    if entry_raw <= stop:
        px = entry_raw * (1 - K["slip_sl"]); return close_out(px, e, "stop_init", entry_raw)
    if entry_raw >= target:  # Ziel unter/gleich Einstieg: nicht anwendbar (wird vorher ausgeschlossen)
        return dict(exit_b=int(e), exit_px=np.nan, reason="target_below_entry", r_net=np.nan, cost_R=np.nan, R=float(R_), entry_fill=float(entry), entry_raw=float(entry_raw))
    last = min(e + hold - 1, n - 1)
    for b in range(e, last + 1):
        if b > e and o[b] <= stop: return close_out(o[b] * (1 - K["slip_sl"]), b, "stop_gap", o[b])
        hit_stop = l[b] <= stop; hit_tgt = h[b] >= target
        if hit_stop and hit_tgt: return close_out(stop * (1 - K["slip_sl"]), b, "stop_ambiguous", stop)
        if hit_stop: return close_out(stop * (1 - K["slip_sl"]), b, "stop", stop)
        if b > e and o[b] >= target: return close_out(o[b], b, "target_gap", o[b])
        if hit_tgt: return close_out(target, b, "target", target)
    if e + hold < n: return close_out(o[e + hold] * (1 - K["slip_in"]), e + hold, "time24", o[e + hold])
    return close_out(c[n - 1] * (1 - K["slip_in"]), n - 1, "cut", c[n - 1])


def diagnostics(o, h, l, c, e, stop, target, tr, R_):
    """Nach dem Trade: Ziel nach Stop innerhalb des Haltefensters, MFE nach Ziel, neues 20/30-Tage-Hoch innerhalb 30 Tagen nach Ziel."""
    n = len(o); d = dict(stop_then_target=np.nan, mfe_after_target_R=np.nan, new20d_high=np.nan, new30d_high=np.nan)
    last = min(e + HOLD - 1, n - 1)
    if tr["reason"] in ("stop", "stop_gap", "stop_init", "stop_ambiguous"):
        d["stop_then_target"] = bool((h[tr["exit_b"] + 1: last + 1] >= target).any()) if tr["exit_b"] + 1 <= last else False
    if tr["reason"] in ("target", "target_gap"):
        xb = tr["exit_b"]
        if xb + 1 <= last: d["mfe_after_target_R"] = float((h[xb + 1: last + 1].max() - target) / R_)
        else: d["mfe_after_target_R"] = 0.0
        prior20 = h[max(0, xb - DIAG_BARS_20D): xb + 1].max(); prior30 = h[max(0, xb - DIAG_BARS_30D): xb + 1].max()
        fut = h[xb + 1: min(n, xb + 1 + DIAG_BARS_30D)]
        d["new20d_high"] = bool((fut > prior20).any()) if len(fut) else False; d["new30d_high"] = bool((fut > prior30).any()) if len(fut) else False
    return d


def run_cells(df1, cands, blk1, coin, kind="cell"):
    """Simuliert je Zelle (mech x q) alle zugelassenen Kandidaten mit Overlap-Regel. cands: Kandidatentabelle mit Spalten e, stop, q0, q1, event, t4, mech."""
    o, h, l, c = (df1[k].to_numpy() for k in ("open", "high", "low", "close")); rows = []
    for mech in sorted(cands.mech.unique()):
        for q in ("q0", "q1"):
            sub = cands[(cands.mech == mech)].sort_values("e")
            open_until = -1
            for _, r in sub.iterrows():
                e = int(r.e); status = "traded"
                if not bool(r.get("full", True)) or bool(r.get("gap_in_window", False)): status = "gap_in_window"
                elif not bool(r.valid_stop): status = "invalid_stop"
                elif not bool(r.tight): status = "no_tight_invalidation"
                elif not (np.isfinite(r[q]) and r[q] > r.entry): status = "target_below_entry" if np.isfinite(r[q]) else "no_episode"
                elif e <= open_until: status = "overlap_skip"
                base = dict(coin=coin, kind=kind, cell=f"{mech}x{q.upper()}", mech=mech, q=q.upper(), event=int(r.event), t4=int(r.t4), e=e, t_entry=str(df1["t"].iat[e]),
                            entry_raw=float(r.entry), stop=float(r.stop), target=float(r[q]) if np.isfinite(r[q]) else np.nan, block=blk1[e], status=status,
                            entry_to_stop_atr4=float(r.entry_to_stop_atr4), flow_flag=bool(r.get("flow_flag", False)), harami=bool(r.get("bullish_harami", False)), hikkake=bool(r.get("hikkake", False)))
                if status != "traded": rows.append(base); continue
                out = dict(base)
                for k in ("K0", "K1", "K2"):
                    tr = simulate(o, h, l, c, e, float(r.stop), float(r[q]), M.COST[k])
                    if k == "K1":
                        out.update(exit_b=tr["exit_b"], t_exit=str(df1["t"].iat[tr["exit_b"]]), exit_px=tr["exit_px"], reason=tr["reason"], R=tr["R"], entry_fill=tr["entry_fill"], bars_held=tr["exit_b"] - e + 1)
                        out.update(diagnostics(o, h, l, c, e, float(r.stop), float(r[q]), tr, tr["R"]))
                    out[f"r_net_{k}"] = tr["r_net"]; out[f"cost_R_{k}"] = tr["cost_R"]; out[f"reason_{k}"] = tr["reason"]
                open_until = out["exit_b"]
                rows.append(out)
    return pd.DataFrame(rows)


def baseline_table(df1, J, A, ev_full, coin):
    """Baseline je vollstaendigem Kontext-Event: Einstieg erste 1h-Kerze nach Kontextkerze t4, Stop low4 - 0.5 ATR4, Q0 EMA20 am Schluss t4, Q1 AVWAP am Schluss der Kerze davor."""
    t1 = M._ts(df1["t"]); rows = []
    tp = ((df1["high"] + df1["low"] + df1["close"]) / 3).to_numpy(); vol = df1["volume"].to_numpy()
    for _, ev in ev_full.iterrows():
        t4 = int(ev.t4); t_start = J["t4_ts"][t4] + 4 * 3600
        eb = int(np.searchsorted(t1, t_start))
        if eb >= len(t1) or t1[eb] != t_start: continue     # Luecke an der Einstiegskerze
        atr4 = J["atr4"][t4]; stop = J["low4"][t4] - 0.5 * atr4; entry = float(df1["open"].iat[eb])
        q0 = float(J["ema20_4h"][eb]); q1 = np.nan; ep = int(A["ep4"][t4])
        if ep >= 0:   # AVWAP der Episode vom Anker bis zur letzten 1h-Kerze der Kontextkerze (Anker am Schluss von t4 bekannt)
            idx = np.where((t1 >= A["anchors"][ep]) & (t1 < t_start))[0]
            if len(idx) and vol[idx].sum() > 0:
                q1 = float((tp[idx] * vol[idx]).sum() / vol[idx].sum())
                if np.isfinite(A["avwap"][eb - 1]): assert np.isclose(q1, A["avwap"][eb - 1]), (t4, q1, A["avwap"][eb - 1])
        rows.append(dict(event=int(ev.event), t4=t4, mech="BASE", b=eb - 1, e=eb, entry=entry, stop=float(stop), R=entry - stop, entry_to_stop_atr4=(entry - stop) / atr4,
                         tight=True, valid_stop=bool(entry - stop > 0), q0=q0, q1=q1, gap_in_window=False, full=True))
    return pd.DataFrame(rows)


def main(coin):
    t0 = time.time(); os.makedirs(_AR + "/micro/run", exist_ok=True)
    p1 = _AR + f"/micro/raw/{coin}USDT_spot_1h.csv"; p4 = _AR + f"/holdout/discovery/{coin}USDT_spot4h_discovery.csv"
    assert "validation" not in p1 and "validation" not in p4
    log = dict(coin=coin, spec="rebound_micro_spec_v1.0.md", inputs=dict(spot1h=sha(p1), spot4h=sha(p4), mlib=sha(_AR + "/micro/mlib.py"), rlib=sha(_AR + "/rtc/rlib.py"), simulate=sha(_FROZEN_SELF)))
    df1 = M.load_1h(p1); df4 = Y.load(p4); C = R.cfg_alt(); f4 = R.features(df4, C)
    f1 = M.features_1h(df1); J = M.join_4h(df1, df4, f4, C); A = M.avwap_episodes(df1, df4, f4, J)
    J["t4_ts"] = M._ts(df4["t"])
    cands = M.candidates(df1, f1, J, A, coin); cands = M.geometry(cands, "K1")
    # Regression gegen die outcome-blinde Zaehlung v0.1
    ref = pd.read_csv(_AR + f"/micro/count_{coin}.csv")
    assert len(ref) == len(cands), ("Kandidatenzahl weicht von der Zaehlung ab", len(ref), len(cands))
    for col in ("mech", "event", "t4", "b", "e", "entry", "stop", "q0", "q1", "tight", "gap_in_window", "flow_flag"):
        a, b = ref[col].to_numpy(), cands[col].to_numpy()
        if a.dtype.kind in "fc": assert np.allclose(np.nan_to_num(a.astype(float), nan=-9), np.nan_to_num(b.astype(float), nan=-9)), col
        else: assert (a == b).all(), col
    log["regression_vs_count_v0_1"] = "IDENTICAL"
    blk1 = np.array([R.block_of(x, coin) for x in df1["t"]])
    # Zellen
    trades = run_cells(df1, cands, blk1, coin, "cell")
    # Baseline auf vollstaendigen Events
    gapb = f1["gap_before"].to_numpy(); ev_rows = []
    for e_ in sorted(set(J["ev4"][J["ev4"] >= 0])):
        idx = np.where((J["event_id"] == e_) & J["ctx_active"])[0]
        if len(idx) == 0: continue
        full = not gapb[max(0, idx[0] - M.P["warmup"]): idx[-1] + 1].any()
        if full: ev_rows.append(dict(event=int(e_), t4=int(J["ctx_src"][idx[0]])))
    ev_full = pd.DataFrame(ev_rows)
    base_c = baseline_table(df1, J, A, ev_full, coin)
    base = run_cells(df1, base_c, blk1, coin, "baseline")
    # Kontrollgruppe: K1 & K2 & nicht K3, gematcht auf Events mit gehandeltem M1 (je Ziel)
    ctrl_ctx = (f4["k1"] & f4["k2"]).to_numpy() & ~J["k3_4"]
    Jc = M.join_4h(df1, df4, f4, C, ctx_override=ctrl_ctx); Jc["t4_ts"] = J["t4_ts"]
    cc = M.candidates(df1, f1, Jc, A, coin); cc = M.geometry(cc, "K1") if len(cc) else cc
    ctx_real = np.where(J["ctx4"])[0]; positions = [(int(t), int(t) + M.P["search_bars_4h"]) for t in ctx_real]
    pool = np.where(ctrl_ctx)[0]
    sig = pd.DataFrame(dict(t=sorted(set(trades[(trades.mech == "M1") & (trades.status == "traded")].t4))))
    match = R.match_controls(sig, pool, f4, positions, C) if len(sig) else pd.DataFrame()
    ev4c = Jc["ev4"]; n4 = len(df4); crow = []
    for _, mr in match.iterrows():
        for cb in mr.ctrls:
            evc = ev4c[cb + 1] if cb + 1 < n4 else -1
            if evc < 0: continue
            sub = cc[(cc.event == evc) & (cc.mech == "M1")]
            if len(sub) == 0: continue
            r = sub.iloc[0].to_dict(); r["sig_t4"] = int(mr.t); r["ctrl_t4"] = int(cb); crow.append(r)
    ctrl_c = pd.DataFrame(crow)
    if len(ctrl_c):
        ctrl_unique = ctrl_c.drop_duplicates(subset=["event"])          # jedes Kontroll-Event einmal simuliert
        ctrls = run_cells(df1, ctrl_unique, blk1, coin, "control")
        key = ctrl_c[["event", "sig_t4"]].drop_duplicates()                 # Zuordnung Signal-Event -> Kontroll-Event (mehrfach erlaubt)
        ctrls = ctrls.merge(key, on="event", how="left")
    else: ctrls = pd.DataFrame()
    trades.to_csv(_AR + f"/micro/run/{coin}_trades.csv", index=False); base.to_csv(_AR + f"/micro/run/{coin}_baseline.csv", index=False); ctrls.to_csv(_AR + f"/micro/run/{coin}_controls.csv", index=False)
    log.update(n_candidates=int(len(cands)), n_events_full=int(len(ev_full)), n_baseline_rows=int(len(base)), n_controls_rows=int(len(ctrls)), n_ctrl_pool=int(len(pool)),
               n_ctrl_candidates_M1=int((cc.mech == "M1").sum()) if len(cc) else 0, seconds=round(time.time() - t0),
               outputs={k: sha(_AR + f"/micro/run/{coin}_{k}.csv") for k in ("trades", "baseline", "controls")})
    json.dump(log, open(_AR + f"/micro/run/{coin}_run.log", "w"), indent=1)
    print(json.dumps(log, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
