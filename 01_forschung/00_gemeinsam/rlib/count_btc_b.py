"""
Outcome-blinde Zaehlung und strukturelles Matching fuer BTC YAMATO Stufe B v1.0 (rlib cfg_btc_stufeA, Stufe-A-Parameter). Abgeleitet von count_cross.py, Aenderungen: Modus, Familienpraefix Y, Coverage-Diagnose, keine Inkrement-Teilmengen (RTC-1/RTC-2 abgeschlossen).
Berechnet KEINE Trades, keine Exits, keine Post-Entry-Renditen, keine MFE/MAE, keine Stop-/Zieltreffer.
Verwendet nur Kandidatenkerze t, Einstiegskerze e (Trigger), Eroeffnung von e (Einstiegspreis) und initialen Stop (Zulaessigkeit).
Positionsausschluss beim Matching (braucht Exits) wird nicht angewendet: Matchzahlen sind Obergrenzen.
"""
import sys, json, hashlib, os, numpy as np, pandas as pd
sys.path.insert(0, "/home/claude/rtc"); import rlib as R; Y = R.Y
COIN = sys.argv[1]; SYM = f"{COIN}USDT"
D = "/home/claude/holdout/discovery"; OUT = f"/home/claude/rtc/count_{COIN}_B"; os.makedirs(OUT, exist_ok=True)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
spot = f"{D}/{SYM}_spot4h_discovery.csv"; flowp = f"{D}/{SYM}_flow4h_discovery.csv"
assert "validation" not in spot and os.environ.get("AURUM_VALIDATION") is None
df = Y.load(spot); C = R.cfg_btc_stufeA(); f = R.features(df, C); lo, hi = Y.swings(df)
flow = pd.read_csv(flowp); assert len(flow) == len(df)
n = len(df); W = Y.WARMUP
tt = df["t"]; blk = np.array([R.block_of(x, COIN) for x in tt])
rep = dict(coin=COIN, cfg={k: v for k, v in C.items()}, sha=dict(spot=sha(spot), flow=sha(flowp), rlib=sha("/home/claude/rtc/rlib.py"), ylib=sha("/home/claude/yamato/ylib.py")))
gapsec = tt.diff().dt.total_seconds().to_numpy(); gap_idx = np.where(gapsec[1:] != 4 * 3600)[0] + 1
rep["bars"] = dict(total=int(n), first=str(tt.iloc[0]), last=str(tt.iloc[-1]), warmup=int(W), evaluable=int(n - W), first_evaluable=str(tt.iloc[W]),
                   grid_gaps=int(len(gap_idx)), missing_bars=int(sum(int(gapsec[i] / 14400) - 1 for i in gap_idx)), blocks={b: int((blk == b).sum()) for b in np.unique(blk)})
gap_in_window = np.zeros(n, bool)
for i in gap_idx: gap_in_window[i: i + 121] = True
# Kontext-Coverage (Diagnose, nicht zur Anpassung)
k1a = f.k1.to_numpy()[W:]; k1atr = (f.dd120_atr.to_numpy()[W:] <= -6.0)
rep["context_coverage"] = dict(k1_pct12_share=round(float(k1a.mean()), 3), k1_atr6_share_diag=round(float(np.nanmean(k1atr)), 3), k1_and_k2=int((f.k1 & f.k2).to_numpy()[W:].sum()),
                               k1_episodes=int(((f.k1.to_numpy()[1:]) & (~f.k1.to_numpy()[:-1])).sum()))
cy = R.candidates_y1_y3(df, f, lo, C); y2 = R.candidates_y2(df, f, lo, hi, C)
cy["block"] = blk[cy.t]; cy["gap_in_window"] = gap_in_window[cy.t]
ctx = cy[cy.ctx]; rep["context_bars"] = dict(total=int(len(ctx)), by_block=ctx.block.value_counts().to_dict())
rep["swings"] = dict(lows=int(len(lo)), highs=int(len(hi)))
assert COIN == "BTC"; P = "Y"
c1 = cy[cy.y1]; c3 = cy[cy.y3]; c2 = y2[y2.y2] if len(y2) else y2
def blkc(ts): return {b: int((blk[np.asarray(ts, int)] == b).sum()) for b in np.unique(blk)}
rep["candidates"] = {f"{P}1": dict(total=int(len(c1)), by_block=blkc(c1.t), levels=c1.y1_levels.value_counts().to_dict(), gap_in_window=int(c1.gap_in_window.sum()), fb_without_ctx=int((cy.fb_any & ~cy.ctx).sum())),
                     f"{P}2": dict(total=int(len(c2)), by_block=blkc(c2.t) if len(c2) else {}, pairs_all=int(len(y2)), ctx_false=int((~y2.ctx).sum()) if len(y2) else 0, dup=int(y2.dup.sum()) if len(y2) else 0, triple=int(c2.triple.sum()) if len(c2) else 0),
                     f"{P}3": dict(total=int(len(c3)), by_block=blkc(c3.t), gap_in_window=int(c3.gap_in_window.sum()), y3_without_ctx=int((cy.y3_any & ~cy.ctx).sum()))}
s1, s2, s3 = set(c1.t), set(c2.t.astype(int)) if len(c2) else set(), set(c3.t)
rep["overlap"] = dict(f1_and_f3=len(s1 & s3), f1_and_f2=len(s1 & s2), f2_and_f3=len(s2 & s3), union=len(s1 | s2 | s3))
# Einstiege je Trigger (ohne Ueberlappungsausschluss, ohne Simulation): Trigger-Kerze, Stop-Zulaessigkeit
o = df.open.to_numpy(); l = df.low.to_numpy(); atr = f.atr.to_numpy()
entries = {}
for kind, cand in ((f"{P}1", c1), (f"{P}2", c2), (f"{P}3", c3)):
    for trig in (("T0", "TA", "TB") if kind != f"{P}2" else ("NECK",)):
        st = {"traded": 0, "no_trigger": 0, "stop_too_wide": 0, "entry_below_stop": 0, "cut": 0}; sd = []; ok_t = []
        for _, r in cand.iterrows():
            t = int(r.t)
            if kind == f"{P}2":
                e = t + 1 if t + 1 < n else None; low_ref = l[int(r.s2)]
            else:
                lvl = r["tb_lvl_y1" if kind == f"{P}1" else "tb_lvl_y3"] if trig == "TB" else np.nan
                e = R.trigger(t, df, trig, lvl, C); low_ref = l[t]
            if e is None: st["no_trigger" if t + 7 < n else "cut"] += 1; continue
            stop0 = low_ref - C["stop_pad"] * atr[t]
            if kind != f"{P}2" and o[e] - stop0 > C["stop_max"] * atr[t]: st["stop_too_wide"] += 1; continue
            if o[e] <= stop0: st["entry_below_stop"] += 1; continue
            st["traded"] += 1; sd.append((o[e] - stop0) / atr[t]); ok_t.append(t)
        entries[f"{kind}_{trig}"] = dict(status=st, entries_by_block=blkc(ok_t) if ok_t else {}, stop_dist_atr=dict(median=round(float(np.median(sd)), 2), min=round(float(min(sd)), 2), max=round(float(max(sd)), 2)) if sd else {},
                                          trigger_rate=round(st["traded"] / max(1, len(cand)), 3))
rep["entries"] = entries
rep["increment_subsets"] = "nicht berechnet: RTC-1 und RTC-2 sind abgeschlossen (ENTSCHEIDE 18.09.2026)"
# Kontrollpool und strukturelles Matching OHNE Positionsausschluss (Obergrenze)
pool = Y.control_pool(cy, c2, df, f); rep["control_pool"] = dict(size=int(len(pool)), by_block=blkc(pool))
match = {}
for kind, cand in ((f"{P}1", c1), (f"{P}2", c2), (f"{P}3", c3)):
    if not len(cand): match[kind] = dict(signals=0); continue
    ref = cand.s2.astype(int).to_numpy() if kind == f"{P}2" else cand.t.astype(int).to_numpy()
    m = R.match_controls(pd.DataFrame(dict(t=ref)), pool, f, [], C); m["cand_t"] = cand.t.to_numpy()
    cov = m.n_ctrl.value_counts().sort_index().to_dict(); used = pd.Series([c for cs in m.ctrls for c in cs])
    matched = m[m.n_ctrl > 0]
    match[kind] = dict(candidates=int(len(m)), with_ge1_control=int(len(matched)), with_3_controls=int((m.n_ctrl == 3).sum()), coverage={int(k): int(v) for k, v in cov.items()},
                       mean_ctrl=round(float(m.n_ctrl.mean()), 2), unique_controls=int(used.nunique()) if len(used) else 0, controls_reused=int((used.value_counts() > 1).sum()) if len(used) else 0,
                       matched_by_block=blkc(matched.cand_t) if len(matched) else {}, median_pool_in_window=float(m.n_pool_window.median()),
                       matched_by_year=matched.cand_t.map(lambda i: int(tt.iloc[int(i)].year)).value_counts().sort_index().to_dict() if len(matched) else {})
    m.to_csv(f"{OUT}/match_{kind}.csv", index=False)
rep["matching_upper_bound_no_position_exclusion"] = match
cy.to_csv(f"{OUT}/candidates_y1_y3.csv", index=False); y2.to_csv(f"{OUT}/candidates_y2.csv", index=False)
rep["sha"]["candidates_y1_y3"] = sha(f"{OUT}/candidates_y1_y3.csv"); rep["sha"]["candidates_y2"] = sha(f"{OUT}/candidates_y2.csv")
json.dump(rep, open(f"{OUT}/count_{COIN}_B.json", "w"), indent=1, default=lambda x: int(x) if isinstance(x, (np.integer,)) else str(x))
print(json.dumps({k: rep[k] for k in ("bars", "context_coverage", "context_bars", "candidates", "overlap", "entries", "increment_subsets", "control_pool", "matching_upper_bound_no_position_exclusion")}, indent=1, default=str))
