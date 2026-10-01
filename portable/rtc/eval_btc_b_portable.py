# PORTABLE VERSION, generiert von tools/make_portable.py. NICHT VON HAND AENDERN.
# Quelle (eingefroren): 01_forschung/00_gemeinsam/rlib/eval_btc_b.py  sha256 2335b4f27f0b81023937bf4bdc3ac37a20ddb6dd10d303995d08bc3c303796a1
# Regeln: paths. Arbeitsbereich: AURUM_ROOT (Default: Ordner '..' relativ zu dieser Datei).
import os as _aos; _AR = _aos.environ.get("AURUM_ROOT") or _aos.path.abspath(_aos.path.join(_aos.path.dirname(_aos.path.abspath(__file__)), ".."))
"""
Einmaliger Outcome-Lauf BTC YAMATO Stufe B v1.0 (rlib cfg_btc_stufeA, Stufe-A-Parameter). Abgeleitet von eval_cross.py, Aenderungen: Modus, Praefix Y, Pfade, keine Inkremente (RTC-1/RTC-2 abgeschlossen). Seed 20260918. Auswertungsregeln v1 mit Regel v2 (Governance v1 Abschnitt 3).
Kandidaten aus der eingefrorenen outcome-blinden Zaehlung (count_<COIN>/), Prueffsummen werden geprueft.
"""
import sys, os, json, hashlib, numpy as np, pandas as pd
sys.path.insert(0, _AR + "/rtc"); import rlib as R; Y = R.Y
COIN = sys.argv[1]; assert COIN == "BTC"; SYM = f"{COIN}USDT"; P = "Y"
SEED = 20260918; NB = 2000; rng = np.random.default_rng(SEED)
D = _AR + "/holdout/discovery"; CNT = _AR + f"/rtc/count_{COIN}_B"; OUT = _AR + f"/rtc/eval_{COIN}_B"; os.makedirs(OUT, exist_ok=True)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
cnt = json.load(open(f"{CNT}/count_{COIN}_B.json"))
spot = f"{D}/{SYM}_spot4h_discovery.csv"; flowp = f"{D}/{SYM}_flow4h_discovery.csv"
assert sha(spot) == cnt["sha"]["spot"] and sha(flowp) == cnt["sha"]["flow"] and sha(_AR + "/rtc/rlib.py") == cnt["sha"]["rlib"]
assert sha(f"{CNT}/candidates_y1_y3.csv") == cnt["sha"]["candidates_y1_y3"] and sha(f"{CNT}/candidates_y2.csv") == cnt["sha"]["candidates_y2"]
assert os.environ.get("AURUM_VALIDATION") is None
df = Y.load(spot); C = R.cfg_btc_stufeA(); f = R.features(df, C); lo, hi = Y.swings(df); flow = pd.read_csv(flowp)
cy = pd.read_csv(f"{CNT}/candidates_y1_y3.csv"); y2 = pd.read_csv(f"{CNT}/candidates_y2.csv")
o, h, l, c, v = (df[k].to_numpy() for k in ("open", "high", "low", "close", "volume")); atr = f.atr.to_numpy(); n = len(df)
tb = df["taker_buy_quote"].to_numpy(); qv = df["quote_volume"].to_numpy(); ti = np.where(qv > 0, (2 * tb - qv) / qv, np.nan); volz = f.volz.to_numpy()
blk = np.array([R.block_of(x, COIN) for x in df["t"]]); year = df.t.dt.year.to_numpy()
BLOCKS = [b for b in dict.fromkeys(blk) if b != "none"]
c1 = cy[cy.y1]; c3 = cy[cy.y3]; c2 = y2[y2.y2]
FAM = {f"{P}1": c1, f"{P}2": c2, f"{P}3": c3}

def diag(tr):
    out = []
    for _, r in tr.iterrows():
        e, x, entry, exitp = int(r.e), int(r.x), r.entry, r.exit
        lo_ref = l[max(0, e - 120): min(n, e + 13)].min(); hi_ref = h[e: min(n, x + 61)].max(); span = hi_ref - lo_ref
        pre_hi = h[max(0, e - 120): e].max(); ok60 = (x + 60) < n
        d = dict(entry_eff=(1 - (entry - lo_ref) / span) if span > 0 else np.nan, exit_eff=(1 - (hi_ref - exitp) / span) if (span > 0 and ok60) else np.nan,
                 capture=(exitp - entry) / span if (span > 0 and ok60) else np.nan, dist_low_atr=(entry - lo_ref) / atr[e], giveback_r=r.mfe_r - r.r_gross)
        for hz, lab in ((42, "7d"), (84, "14d"), (180, "30d"), (360, "60d")):
            seg = c[e + 1: min(n, e + 1 + hz)]; d[f"trend_{lab}"] = bool((seg > pre_hi).any()) if (e + hz) < n else np.nan
        seg = c[e + 1: min(n, e + 361)]; idx = np.where(seg > pre_hi)[0]
        d["persist30"] = bool((c[e + 1 + idx[0]: e + 1 + idx[0] + 30] > pre_hi).all()) if (len(idx) and (e + 1 + idx[0] + 30) < n) else np.nan
        t30, t60 = d["trend_30d"], d["trend_60d"]
        d["cls"] = "trend" if t30 is True else ("delayed_trend" if (t60 is True and r.mfe_r >= 1) else ("rebound" if (r.mfe_r >= 1 and t60 is False) else ("fail" if r.mfe_r < 1 else "na")))
        for k in (1, 3, 6):
            if e + k < n:
                d[f"ft{k}_px_atr"] = (c[e + k] - entry) / atr[e]; d[f"ft{k}_volz"] = np.nanmean(volz[e: e + k + 1]); d[f"ft{k}_ti"] = np.nanmean(ti[e: e + k + 1])
        d["block"] = blk[int(r.t)]; d["year"] = int(year[int(r.t)]); d["cut_trend"] = bool(d["trend_60d"] is True and (x < e + 360) and (c[x + 1: min(n, e + 361)] > pre_hi).any()) if x + 1 < n else np.nan
        out.append(d)
    return pd.concat([tr.reset_index(drop=True), pd.DataFrame(out)], axis=1)

def stats(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) == 0: return dict(n=0)
    return dict(n=int(len(x)), mean=round(float(x.mean()), 3), median=round(float(np.median(x)), 3), p5=round(float(np.percentile(x, 5)), 3), p95=round(float(np.percentile(x, 95)), 3), win=round(float((x > 0).mean()), 3))
def boot(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) < 2: return dict(n=int(len(x)))
    m = np.array([rng.choice(x, len(x)).mean() for _ in range(NB)]); md = np.array([np.median(rng.choice(x, len(x))) for _ in range(NB)])
    return dict(n=int(len(x)), mean=round(float(x.mean()), 3), median=round(float(np.median(x)), 3), b_p5=round(float(np.percentile(m, 5)), 3), b_p95=round(float(np.percentile(m, 95)), 3),
                b_med_p5=round(float(np.percentile(md, 5)), 3), b_med_p95=round(float(np.percentile(md, 95)), 3), p_pos=round(float((m > 0).mean()), 3), p_boot_le0=round(float((m <= 0).mean()), 4), share_pos=round(float((x > 0).mean()), 3))
def pf(r): g = r[r > 0].sum(); b = -r[r < 0].sum(); return round(float(g / b), 3) if b > 0 else None
def conc(r):
    g = np.sort(np.asarray(r[r > 0], float))[::-1]; s = g.sum()
    return dict(top1=round(float(g[0] / s), 3) if s > 0 else None, top3=round(float(g[:3].sum() / s), 3) if s > 0 else None)
def summarize(sig, ctr_tr, pairs, kind, cost_res):
    r = dict(signals=int(len(sig)), blocks=sig.block.value_counts().to_dict(), costs=cost_res, r_net=stats(sig.r_net), r_gross=stats(sig.r_gross), mfe_r=stats(sig.mfe_r), mae_r=stats(sig.mae_r), bars=stats(sig.bars),
             stop_dist_atr=stats(sig.stop_dist_atr), entry_eff=stats(sig.entry_eff), exit_eff=stats(sig.exit_eff), capture=stats(sig.capture), giveback_r=stats(sig.giveback_r), dist_low_atr=stats(sig.dist_low_atr),
             exit_reason=sig.reason.value_counts().to_dict(), cls=sig.cls.value_counts().to_dict(), profit_factor=pf(sig.r_net), concentration=conc(sig.r_net),
             trend_rate={k: round(float(sig[k].dropna().astype(float).mean()), 3) for k in ("trend_7d", "trend_14d", "trend_30d", "trend_60d") if sig[k].notna().any()},
             persist30=round(float(sig.persist30.dropna().astype(float).mean()), 3) if sig.persist30.notna().any() else None, cut_trend_rate=round(float(sig.cut_trend.dropna().astype(float).mean()), 3) if sig.cut_trend.notna().any() else None,
             ft={k: round(float(sig[k].mean()), 3) for k in sig.columns if k.startswith("ft")}, years={int(k): round(float(v), 2) for k, v in sig.groupby("year").r_net.sum().items()},
             by_block={b: stats(sig[sig.block == b].r_net) for b in BLOCKS},
             controls=dict(traded=int(len(ctr_tr)), r_net=stats(ctr_tr.r_net) if len(ctr_tr) else {}, mfe_r=stats(ctr_tr.mfe_r) if len(ctr_tr) else {}, capture=stats(ctr_tr.capture) if len(ctr_tr) else {},
                           cls=ctr_tr.cls.value_counts().to_dict() if len(ctr_tr) else {}, profit_factor=pf(ctr_tr.r_net) if len(ctr_tr) else None),
             paired=dict(n_pairs=int(len(pairs)), d_r=boot(pairs.d_r) if len(pairs) else {}, d_mfe=boot(pairs.d_mfe) if len(pairs) else {}, d_capture=boot(pairs.d_capture) if len(pairs) else {}, d_trend=boot(pairs.d_trend) if len(pairs) else {},
                         by_block={b: stats(pairs[pairs.block == b].d_r) for b in BLOCKS} if len(pairs) else {}))
    return r
def status_v2(r, sig, pairs):
    pr = r["paired"]; dr = pr.get("d_r", {}); npairs = int(pr.get("n_pairs", 0)); S = {}
    if npairs < 5:
        return dict(status="inconclusive_insufficient_sample", n_pairs=npairs, note="unter 5 Paaren keine Statuszuweisung")
    # v1 Bedingungen (formal supported)
    a = dr.get("mean", -1) > 0 and dr.get("p_pos", 0) >= 0.80
    b = (r["mfe_r"].get("median", 0) > r["controls"]["mfe_r"].get("median", 0)) and pr.get("d_capture", {}).get("mean", -1) > 0
    bl = {k: v["mean"] for k, v in pr["by_block"].items() if v.get("n", 0) >= 5}
    cnd = all(x > 0 for x in bl.values()) if len(bl) >= 2 else dr.get("mean", -1) > 0
    d = (r["concentration"]["top1"] or 0) <= 0.40; e_ = r["costs"]["r_net_K1"].get("mean", -1) > 0
    formal = bool(a and b and cnd and d and e_)
    # v2 Kriterien
    k1 = dr.get("median", -1) > 0 and dr.get("share_pos", 0) >= 0.60
    cls_share = lambda s: (s.cls.isin(["trend", "delayed_trend"]).mean() if len(s) else 0)
    k2 = (r["mfe_r"].get("median", 0) - r["controls"]["mfe_r"].get("median", 0) >= 0.5) or (r["capture"].get("median", 0) - r["controls"]["capture"].get("median", 0) >= 0.10) or (pr.get("d_trend", {}).get("mean", 0) >= 0.15)
    dpos = pairs.d_r[pairs.d_r > 0]; top_share = float(dpos.max() / dpos.sum()) if len(dpos) and dpos.sum() > 0 else 0.0
    med_wo_best = float(np.median(pairs.d_r.drop(pairs.d_r.idxmax()))) if len(pairs) > 1 else 0.0
    k3 = top_share <= 0.40 and np.sign(med_wo_best) == np.sign(dr.get("median", 0)) and dr.get("median", 0) != 0
    blm = {k: v["median"] for k, v in pr["by_block"].items() if v.get("n", 0) >= 5}
    k4 = len(blm) >= 2 and len(set(np.sign(list(blm.values())))) == 1 and dr.get("median", 0) != 0 and np.sign(list(blm.values())[0]) == np.sign(dr.get("median", 0))
    crit = dict(k1_control=bool(k1), k2_shift=bool(k2), k3_no_dominance=bool(k3), k4_time_consistency=bool(k4)); nmet = sum(crit.values())
    ff = bool(npairs >= 10 and dr.get("median", 0) < 0 and dr.get("share_pos", 1) < 0.40)
    if formal: st = "formal_supported"
    elif nmet >= 3 and dr.get("median", 0) > 0: st = "mechanistically_promising"
    elif ff: st = "no_evidence_fast_fail"
    else: st = "no_evidence_inconclusive"
    return dict(status=st, n_pairs=npairs, v1=dict(a=bool(a), b=bool(b), c=bool(cnd), d=bool(d), e=bool(e_)), v2=crit, v2_met=int(nmet), fast_fail=ff, fast_promote=formal,
                validation_eligible=bool(formal or (st == "mechanistically_promising" and len(sig) >= 20)), top_pair_share=round(top_share, 3), median_without_best=round(med_wo_best, 3), blocks_median=blm)

rep = dict(coin=COIN, seed=SEED, cost_primary="K1", cfg=C, sha_inputs=dict(cnt["sha"]), blocks=BLOCKS)
pool = Y.control_pool(cy, c2, df, f)
def run_cfg(kind, cand, trig, ex, cost="K1"):
    tr, lg = R.run_sleeve(cand.sort_values("t"), df, f, lo, kind, trig, ex, cost, C); return tr, lg
def controls_for(kind, tr, trig, ex):
    pos = list(zip(tr.e.astype(int), tr.x.astype(int)))
    sigs = pd.DataFrame(dict(t=c2.set_index("t").loc[tr.t, "s2"].astype(int).to_numpy())) if kind == f"{P}2" else tr[["t"]]
    m = R.match_controls(sigs, pool, f, pos, C); ctr = R.run_controls(m, tr.t, df, f, lo, trig, ex, C)
    ct = ctr[ctr.status == "traded"].copy()
    if len(ct): ct = diag(ct)
    return m, ctr, ct
def make_pairs(sig, ct):
    rows = []
    for st in sig.t:
        s = sig[sig.t == st].iloc[0]; cc = ct[ct.sig_t == st] if len(ct) else ct
        if len(cc) == 0: continue
        rows.append(dict(t=st, d_r=s.r_net - cc.r_net.mean(), d_mfe=s.mfe_r - cc.mfe_r.mean(), d_capture=(s.capture - cc.capture.mean()) if np.isfinite(s.capture) and np.isfinite(cc.capture.mean()) else np.nan,
                         d_trend=float(s.cls in ("trend", "delayed_trend")) - float(cc.cls.isin(["trend", "delayed_trend"]).mean()), block=s.block, n_ctrl=len(cc)))
    return pd.DataFrame(rows)

# ---------------- primaere Familie: T0 (Neck), E-U, gegen Kontrollen ----------------
prim = {}; sigs_prim = {}
for kind, cand in FAM.items():
    trig = "NECK" if kind == f"{P}2" else "T0"
    cost_res = {}
    for cost in ("K0", "K1", "K2"):
        tr, lg = run_cfg(kind, cand, trig, "EU", cost); cost_res[f"r_net_{cost}"] = stats(tr.r_net) if len(tr) else dict(n=0)
        if cost == "K1": tr_main, lg_main = tr, lg
    if not len(tr_main): prim[kind] = dict(signals=0); continue
    sig = diag(tr_main); sig["kind"] = kind; sigs_prim[kind] = sig
    m, ctr, ct = controls_for(kind, tr_main, "T0" if kind != f"{P}2" else "T0", "EU")
    pairs = make_pairs(sig, ct)
    r = summarize(sig, ct, pairs, kind, cost_res); r["log_status"] = lg_main.status.value_counts().to_dict(); r["controls"]["matched"] = int((m.n_ctrl > 0).sum()); r["controls"]["status"] = ctr.status.value_counts().to_dict() if len(ctr) else {}
    r["status_v2"] = status_v2(r, sig, pairs) if len(pairs) else dict(status="inconclusive_insufficient_sample", n_pairs=0)
    r["pnl_atr"] = stats(sig.r_net * sig.stop_dist_atr)
    prim[kind] = r
    sig.to_csv(f"{OUT}/trades_{kind}_T0_EU_K1.csv", index=False); ctr.to_csv(f"{OUT}/controls_{kind}_T0_EU_K1.csv", index=False); pairs.to_csv(f"{OUT}/pairs_{kind}_T0_EU.csv", index=False)
# Holm ueber die drei primaeren (Bootstrap-p der gepaarten Differenz)
pv = {k: prim[k]["paired"]["d_r"].get("p_boot_le0") for k in prim if prim[k].get("signals", 0) and prim[k]["paired"].get("d_r", {}).get("n", 0) >= 2}
order = sorted(pv, key=lambda k: pv[k]); mtot = len(order); holm = {}; prev = 0
for i, k in enumerate(order):
    adj = min(1.0, max(prev, pv[k] * (mtot - i))); holm[k] = dict(p=pv[k], p_holm=round(adj, 4), signal_present=bool(adj < 0.05 and prim[k]["paired"]["d_r"]["mean"] > 0 and prim[k]["costs"]["r_net_K1"]["mean"] > 0)); prev = adj
rep["primary"] = prim; rep["holm_primary"] = holm

# ---------------- Trigger-Familie: TA, TB gegen T0 auf 1 und 3 (Erwartung je Kandidat) ----------------
trigfam = {}
for kind in (f"{P}1", f"{P}3"):
    cand = FAM[kind]; res = {}
    for trig in ("T0", "TA", "TB"):
        tr, lg = run_cfg(kind, cand, trig, "EU"); sig = diag(tr) if len(tr) else tr
        per_cand = float(tr.r_net.sum() / max(1, len(cand)))   # verfallene Kandidaten zaehlen als 0
        res[trig] = dict(candidates=int(len(cand)), traded=int(len(tr)), log_status=lg.status.value_counts().to_dict(), r_net=stats(tr.r_net) if len(tr) else {}, expectancy_per_candidate=round(per_cand, 4),
                         mfe_r=stats(sig.mfe_r) if len(tr) else {}, capture=stats(sig.capture) if len(tr) else {}, cls=sig.cls.value_counts().to_dict() if len(tr) else {}, bars=stats(tr.bars) if len(tr) else {},
                         entry_vs_low_atr=stats(sig.dist_low_atr) if len(tr) else {}, profit_factor=pf(tr.r_net) if len(tr) else None)
        if len(tr): sig.to_csv(f"{OUT}/trades_{kind}_{trig}_EU_K1.csv", index=False)
        res[trig]["_pc"] = np.array([tr[tr.t == t].r_net.iloc[0] if (tr.t == t).any() else 0.0 for t in cand.t])
    for trig in ("TA", "TB"):
        d = res[trig]["_pc"] - res["T0"]["_pc"]; res[f"{trig}_vs_T0_per_candidate"] = boot(d)
    for k in ("T0", "TA", "TB"): res[k].pop("_pc")
    trigfam[kind] = res
rep["trigger_family"] = trigfam

# ---------------- Exit-Familie: E-D und E0 gegen E-U auf denselben T0-Einstiegen ----------------
exitfam = {}
for kind, cand in FAM.items():
    trig = "NECK" if kind == f"{P}2" else "T0"; res = {}
    base, _ = run_cfg(kind, cand, trig, "EU"); base_d = diag(base) if len(base) else base
    for ex in ("EU", "ED", "E0"):
        tr, lg = run_cfg(kind, cand, trig, ex); sig = diag(tr) if len(tr) else tr
        res[ex] = dict(traded=int(len(tr)), r_net=stats(tr.r_net) if len(tr) else {}, mfe_r=stats(sig.mfe_r) if len(tr) else {}, capture=stats(sig.capture) if len(tr) else {}, giveback_r=stats(sig.giveback_r) if len(tr) else {},
                       bars=stats(tr.bars) if len(tr) else {}, exit_reason=tr.reason.value_counts().to_dict() if len(tr) else {}, cls=sig.cls.value_counts().to_dict() if len(tr) else {},
                       cut_trend_rate=round(float(sig.cut_trend.dropna().astype(float).mean()), 3) if len(tr) and sig.cut_trend.notna().any() else None, profit_factor=pf(tr.r_net) if len(tr) else None)
        if len(tr): sig.to_csv(f"{OUT}/trades_{kind}_{trig}_{ex}_K1.csv", index=False)
        # gepaart auf gemeinsamen Einstiegskerzen (Ueberlappung kann Einstiege verschieben)
        if ex != "EU" and len(tr) and len(base):
            j = base.merge(tr, on="e", suffixes=("_u", "_x")); bd = base_d.set_index("e"); xd = sig.set_index("e")
            if len(j):
                res[f"{ex}_vs_EU_paired"] = dict(n_common_entries=int(len(j)), d_r=boot(j.r_net_x - j.r_net_u), d_capture=boot(xd.loc[j.e, "capture"].to_numpy() - bd.loc[j.e, "capture"].to_numpy()),
                                                 d_bars=stats(j.bars_x - j.bars_u), d_giveback=boot(xd.loc[j.e, "giveback_r"].to_numpy() - bd.loc[j.e, "giveback_r"].to_numpy()))
    exitfam[kind] = res
rep["exit_family"] = exitfam

rep["increments"] = "nicht berechnet: RTC-1 und RTC-2 sind abgeschlossen (ENTSCHEIDE 18.09.2026)"
rep["overlap_signals"] = {f"{P}1_and_{P}3": len(set(sigs_prim.get(f"{P}1", pd.DataFrame(columns=["t"])).t) & set(sigs_prim.get(f"{P}3", pd.DataFrame(columns=["t"])).t))}
rep["sha_outputs"] = {fn: sha(f"{OUT}/{fn}") for fn in sorted(os.listdir(OUT)) if fn.endswith(".csv")}
rep["sha_eval_script"] = sha(_AR + "/rtc/eval_btc_b.py")
json.dump(rep, open(f"{OUT}/eval_{COIN}_B.json", "w"), indent=1, default=lambda x: None if isinstance(x, float) and np.isnan(x) else (bool(x) if isinstance(x, np.bool_) else (int(x) if isinstance(x, np.integer) else (float(x) if isinstance(x, np.floating) else str(x)))))
print("done", COIN)
