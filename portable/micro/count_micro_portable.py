# PORTABLE VERSION, generiert von tools/make_portable.py. NICHT VON HAND AENDERN.
# Quelle (eingefroren): 01_forschung/10_rebound_micro/mlib/count_micro.py  sha256 9860249f11c42cf20037ef40c27c06fabd987297d308a41dc8b04f9afdb32f8a
# Regeln: paths. Arbeitsbereich: AURUM_ROOT (Default: Ordner '..' relativ zu dieser Datei).
import os as _aos; _AR = _aos.environ.get("AURUM_ROOT") or _aos.path.abspath(_aos.path.join(_aos.path.dirname(_aos.path.abspath(__file__)), ".."))
"""Outcome-blinde Zaehlung REBOUND-MICRO v0.1 auf BTC/XRP/DOT. Keine Exits, kein P&L, keine MFE/MAE."""
import sys, json, hashlib, numpy as np, pandas as pd, time
sys.path.insert(0, _AR + "/micro"); sys.path.insert(0, _AR + "/rtc"); import mlib as M; import rlib as R; Y = R.Y
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
coin = sys.argv[1]; t0 = time.time()
p1 = _AR + f"/micro/raw/{coin}USDT_spot_1h.csv"; p4 = _AR + f"/holdout/discovery/{coin}USDT_spot4h_discovery.csv"
df1 = M.load_1h(p1); df4 = Y.load(p4); C = R.cfg_alt(); f4 = R.features(df4, C)
f1 = M.features_1h(df1); J = M.join_4h(df1, df4, f4, C); A = M.avwap_episodes(df1, df4, f4, J)
res = M.candidates(df1, f1, J, A, coin); res = M.geometry(res, "K1")
res.to_csv(_AR + f"/micro/count_{coin}.csv", index=False)
# Perp-Flow-Diagnose: Abdeckung der Perp-1h-Merkmale an den Kandidatenkerzen (Join ueber Zeitstempel)
dfp = M.load_1h(_AR + f"/micro/raw/{coin}USDT_perp_1h.csv"); fp = M.features_1h(dfp); fp["t"] = dfp["t"]
pj = pd.DataFrame({"t": df1["t"].iloc[res.b.astype(int)].to_numpy()}).merge(fp[["t", "taker_imbalance", "sell_volume_zscore"]], on="t", how="left")
n1 = len(df1); ctx = J["ctx4"]; ev4 = J["ev4"]
events = sorted(set(ev4[ev4 >= 0])); ev_rows = []
gapb = f1["gap_before"].to_numpy()
for e in events:
    idx = np.where((J["event_id"] == e) & J["ctx_active"])[0]
    if len(idx) == 0: ev_rows.append(dict(event=e, bars_1h=0, full=False)); continue
    full = not gapb[max(0, idx[0] - M.P["warmup"]): idx[-1] + 1].any()
    ev_rows.append(dict(event=e, bars_1h=int(len(idx)), full=bool(full), t4=int(J["ctx_src"][idx[0]])))
ev = pd.DataFrame(ev_rows)
blk = np.array([R.block_of(x, coin) for x in df4["t"]])
rep = dict(coin=coin, sha=dict(spot1h=sha(p1), spot4h=sha(p4), mlib=sha(_AR + "/micro/mlib.py"), rlib=sha(_AR + "/rtc/rlib.py")),
           bars_1h=int(n1), first_1h=str(df1.t.iat[0]), last_1h=str(df1.t.iat[-1]), warmup_1h=M.P["warmup"],
           context_bars_4h=int(ctx.sum()), context_events=int(len(events)), events_with_full_1h=int(ev.full.sum()) if len(ev) else 0, events_incomplete=int((~ev.full).sum()) if len(ev) else 0,
           events_by_block={b: int(sum(1 for _, r in ev.iterrows() if r.get("full", False) and blk[int(r.t4)] == b)) for b in sorted(set(blk))},
           episodes_k1=int(len(A["anchors"])), episode_len_4h_median=float(pd.Series(A["ep4"][A["ep4"] >= 0]).value_counts().median()) if (A["ep4"] >= 0).any() else None)
def blockof(t4s): return {b: int(sum(1 for t in t4s if blk[int(t)] == b)) for b in sorted(set(blk))}
cand = {}
for m in ("M1", "M2", "M3"):
    r = res[res.mech == m]; rf = r[r.gap_in_window == False]
    d = dict(candidates=int(len(r)), in_full_windows=int(len(rf)), valid_stop=int(rf.valid_stop.sum()), tight=int((rf.tight & rf.valid_stop).sum()), no_tight_invalidation=int((~rf.tight & rf.valid_stop).sum()),
             q0_above=int((rf.tight & rf.valid_stop & rf.q0_above).sum()), q1_above=int((rf.tight & rf.valid_stop & rf.q1_above).sum()), q1_no_episode=int((rf.tight & rf.valid_stop & rf.q1.isna()).sum()),
             flow_flag=int((rf.tight & rf.valid_stop & rf.flow_flag).sum()) if m != "M3" else None, by_block=blockof(rf[rf.tight & rf.valid_stop].t4.to_numpy()),
             harami=int(rf.bullish_harami.sum()), hikkake=int(rf.hikkake.sum()))
    g = rf[rf.tight & rf.valid_stop]
    def q(x): x = x.dropna(); return dict(n=int(len(x)), median=round(float(x.median()), 3), p25=round(float(x.quantile(.25)), 3), p75=round(float(x.quantile(.75)), 3)) if len(x) else dict(n=0)
    d["entry_to_stop_atr4"] = q(g.entry_to_stop_atr4); d["entry_to_stop_atr1"] = q(g.entry_to_stop_atr1); d["baseline_entry_to_stop_atr4"] = q(g.baseline_entry_to_stop_atr4)
    d["stop_ratio_1h_vs_4h"] = q(g.entry_to_stop_atr4 / g.baseline_entry_to_stop_atr4)
    d["entry_to_q0_atr4"] = q(g[g.q0_above].entry_to_q0_atr4); d["entry_to_q1_atr4"] = q(g[g.q1_above].entry_to_q1_atr4)
    d["rr_geo_q0"] = q(g.rr_geo_q0); d["rr_geo_q1"] = q(g.rr_geo_q1); d["pbe_geo_q0"] = q(g.pbe_geo_q0); d["pbe_geo_q1"] = q(g.pbe_geo_q1); d["cost_R"] = q(g.cost_R)
    d["entry_delay_1h_from_context_close_median"] = float((g.e - 0).sub(0).median()) if len(g) else None
    cand[m] = d
rep["candidates"] = cand
g = res[(res.gap_in_window == False) & res.tight & res.valid_stop]
s = {m: set(g[g.mech == m].event) for m in ("M1", "M2", "M3")}
rep["overlap_events"] = dict(M1_M2=len(s["M1"] & s["M2"]), M1_M3=len(s["M1"] & s["M3"]), M2_M3=len(s["M2"] & s["M3"]), all3=len(s["M1"] & s["M2"] & s["M3"]), M3_only=len(s["M3"] - s["M1"] - s["M2"]), union=len(s["M1"] | s["M2"] | s["M3"]))
rep["flow_fields"] = {k: dict(valid=int(f1[k].notna().sum()), share=round(float(f1[k].notna().mean()), 3)) for k in ("taker_imbalance", "delta_taker_imbalance", "volume_zscore", "trade_count_zscore", "sell_volume_zscore", "sell_efficiency")}
rep["perp_flow_at_candidates"] = dict(joined=int(pj.taker_imbalance.notna().sum()), of=int(len(pj)))
rep["m3_absorption_bars_total"] = int(((f1.sell_volume_zscore >= 1.0) & (f1.sell_efficiency <= 0.25)).sum())
rep["seconds"] = round(time.time() - t0)
json.dump(rep, open(_AR + f"/micro/count_{coin}.json", "w"), indent=1, default=str)
print(json.dumps(rep, indent=1, default=str))
