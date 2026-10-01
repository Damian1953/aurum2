#!/usr/bin/env python3
"""
Project Aurum II — DELAYED-TREND P&L, einziger Lauf v1.0. Spezifikation ../dt_pnl_spec_v1.0.md (SHA in SPEC_SHA, Pruefung im Lauf).
Aufruf: AURUM_ROOT=<repo>/build/root python dt_pnl_run.py --lauf   (Arbeitsbereich vorher mit `make stage` aufbauen).
Status-, Diagnose- und Statistikfunktionen wortgleich aus rtc/eval_cross.py (ohne Follow-through- und Flow-Felder).
"""
import sys, os, json, hashlib, datetime, argparse, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
AR = os.environ.get("AURUM_ROOT") or os.path.join(REPO, "build", "root")
SPEC = os.path.join(HERE, "..", "dt_pnl_spec_v1.0.md")
SPEC_SHA = "56a13bf7d434356539e956457e3616ea93a7ded4ea25f4247fd31380bf41d47a"
RLIB_SHA = "f1ffdbb81cad3115b7a975a435185b463c9d752bd86ee9f7b47ece3c4819b13c"; DTLIB_SHA = "f2d6c3906aff57d37b85d8dc7226e1188cd38bf50679412c5ade80f3ae8a9dc2"
SEED = 20260918; NB = 2000
PRIMARY = [("BTC", "S2", "DT1"), ("XRP", "S2", "DT1"), ("XRP", "S2", "DT2")]
SECONDARY = [("BTC", "S2", "DT2"), ("DOT", "S2", "DT1"), ("DOT", "S2", "DT2")]
DESCRIPTIVE = [(c, "S1", f) for c in ("BTC", "XRP", "DOT") for f in ("DT1", "DT2")]
LAST_BAR = pd.Timestamp("2023-12-31 20:00", tz="UTC")


def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()


# ---------------- eval_cross.py (wortgleich, ohne ft/Flow); rng ist der Lauf-Generator ----------------
RNG = [None]
def diag(tr, d):
    o, h, l, c = (d["df"][k_].to_numpy() for k_ in ("open", "high", "low", "close")); atr = d["atr4"]; n = len(o); blk = d["blk"]; year = d["year"]; out = []
    for _, r in tr.iterrows():
        e, x, entry, exitp = int(r.e), int(r.x), r.entry, r.exit
        lo_ref = l[max(0, e - 120): min(n, e + 13)].min(); hi_ref = h[e: min(n, x + 61)].max(); span = hi_ref - lo_ref
        pre_hi = h[max(0, e - 120): e].max(); ok60 = (x + 60) < n
        dd_ = dict(entry_eff=(1 - (entry - lo_ref) / span) if span > 0 else np.nan, exit_eff=(1 - (hi_ref - exitp) / span) if (span > 0 and ok60) else np.nan,
                   capture=(exitp - entry) / span if (span > 0 and ok60) else np.nan, dist_low_atr=(entry - lo_ref) / atr[e], giveback_r=r.mfe_r - r.r_gross)
        for hz, lab in ((42, "7d"), (84, "14d"), (180, "30d"), (360, "60d")):
            seg = c[e + 1: min(n, e + 1 + hz)]; dd_[f"trend_{lab}"] = bool((seg > pre_hi).any()) if (e + hz) < n else np.nan
        seg = c[e + 1: min(n, e + 361)]; idx = np.where(seg > pre_hi)[0]
        dd_["persist30"] = bool((c[e + 1 + idx[0]: e + 1 + idx[0] + 30] > pre_hi).all()) if (len(idx) and (e + 1 + idx[0] + 30) < n) else np.nan
        t30, t60 = dd_["trend_30d"], dd_["trend_60d"]
        dd_["cls"] = "trend" if t30 is True else ("delayed_trend" if (t60 is True and r.mfe_r >= 1) else ("rebound" if (r.mfe_r >= 1 and t60 is False) else ("fail" if r.mfe_r < 1 else "na")))
        dd_["block"] = blk[int(r.t)]; dd_["year"] = int(year[int(r.t)]); dd_["cut_trend"] = bool(dd_["trend_60d"] is True and (x < e + 360) and (c[x + 1: min(n, e + 361)] > pre_hi).any()) if x + 1 < n else np.nan
        out.append(dd_)
    return pd.concat([tr.reset_index(drop=True), pd.DataFrame(out)], axis=1)

def stats(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) == 0: return dict(n=0)
    return dict(n=int(len(x)), mean=round(float(x.mean()), 3), median=round(float(np.median(x)), 3), p5=round(float(np.percentile(x, 5)), 3), p95=round(float(np.percentile(x, 95)), 3), win=round(float((x > 0).mean()), 3))
def boot(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) < 2: return dict(n=int(len(x)))
    m = np.array([RNG[0].choice(x, len(x)).mean() for _ in range(NB)]); md = np.array([np.median(RNG[0].choice(x, len(x))) for _ in range(NB)])
    return dict(n=int(len(x)), mean=round(float(x.mean()), 3), median=round(float(np.median(x)), 3), b_p5=round(float(np.percentile(m, 5)), 3), b_p95=round(float(np.percentile(m, 95)), 3),
                b_med_p5=round(float(np.percentile(md, 5)), 3), b_med_p95=round(float(np.percentile(md, 95)), 3), p_pos=round(float((m > 0).mean()), 3), p_boot_le0=round(float((m <= 0).mean()), 4), share_pos=round(float((x > 0).mean()), 3))
def pf(r): g = r[r > 0].sum(); b = -r[r < 0].sum(); return round(float(g / b), 3) if b > 0 else None
def conc(r):
    g = np.sort(np.asarray(r[r > 0], float))[::-1]; s = g.sum()
    return dict(top1=round(float(g[0] / s), 3) if s > 0 else None, top3=round(float(g[:3].sum() / s), 3) if s > 0 else None)
def summarize(sig, ctr_tr, pairs, cost_res, BLOCKS):
    r = dict(signals=int(len(sig)), blocks=sig.block.value_counts().to_dict(), costs=cost_res, r_net=stats(sig.r_net), r_gross=stats(sig.r_gross), mfe_r=stats(sig.mfe_r), mae_r=stats(sig.mae_r), bars=stats(sig.bars),
             stop_dist_atr=stats(sig.stop_dist_atr), entry_eff=stats(sig.entry_eff), exit_eff=stats(sig.exit_eff), capture=stats(sig.capture), giveback_r=stats(sig.giveback_r), dist_low_atr=stats(sig.dist_low_atr),
             exit_reason=sig.reason.value_counts().to_dict(), cls=sig.cls.value_counts().to_dict(), profit_factor=pf(sig.r_net), concentration=conc(sig.r_net),
             trend_rate={k_: round(float(sig[k_].dropna().astype(float).mean()), 3) for k_ in ("trend_7d", "trend_14d", "trend_30d", "trend_60d") if sig[k_].notna().any()},
             persist30=round(float(sig.persist30.dropna().astype(float).mean()), 3) if sig.persist30.notna().any() else None, cut_trend_rate=round(float(sig.cut_trend.dropna().astype(float).mean()), 3) if sig.cut_trend.notna().any() else None,
             years={int(k_): round(float(v), 2) for k_, v in sig.groupby("year").r_net.sum().items()},
             by_block={b: stats(sig[sig.block == b].r_net) for b in BLOCKS},
             controls=dict(traded=int(len(ctr_tr)), r_net=stats(ctr_tr.r_net) if len(ctr_tr) else {}, mfe_r=stats(ctr_tr.mfe_r) if len(ctr_tr) else {}, capture=stats(ctr_tr.capture) if len(ctr_tr) else {},
                           cls=ctr_tr.cls.value_counts().to_dict() if len(ctr_tr) else {}, profit_factor=pf(ctr_tr.r_net) if len(ctr_tr) else None),
             paired=dict(n_pairs=int(len(pairs)), d_r=boot(pairs.d_r) if len(pairs) else {}, d_mfe=boot(pairs.d_mfe) if len(pairs) else {}, d_capture=boot(pairs.d_capture) if len(pairs) else {}, d_trend=boot(pairs.d_trend) if len(pairs) else {},
                         by_block={b: stats(pairs[pairs.block == b].d_r) for b in BLOCKS} if len(pairs) else {}))
    return r
def status_v2(r, sig, pairs):
    pr = r["paired"]; dr = pr.get("d_r", {}); npairs = int(pr.get("n_pairs", 0))
    if npairs < 5:
        return dict(status="inconclusive_insufficient_sample", n_pairs=npairs, note="unter 5 Paaren keine Statuszuweisung")
    a1 = dr.get("mean", -1) > 0 and dr.get("p_pos", 0) >= 0.80
    b1 = (r["mfe_r"].get("median", 0) > r["controls"]["mfe_r"].get("median", 0)) and pr.get("d_capture", {}).get("mean", -1) > 0
    bl = {k_: v["mean"] for k_, v in pr["by_block"].items() if v.get("n", 0) >= 5}
    cnd = all(x > 0 for x in bl.values()) if len(bl) >= 2 else dr.get("mean", -1) > 0
    d1 = (r["concentration"]["top1"] or 0) <= 0.40; e1 = r["costs"]["r_net_K1"].get("mean", -1) > 0
    formal = bool(a1 and b1 and cnd and d1 and e1)
    k1 = dr.get("median", -1) > 0 and dr.get("share_pos", 0) >= 0.60
    k2 = (r["mfe_r"].get("median", 0) - r["controls"]["mfe_r"].get("median", 0) >= 0.5) or (r["capture"].get("median", 0) - r["controls"]["capture"].get("median", 0) >= 0.10) or (pr.get("d_trend", {}).get("mean", 0) >= 0.15)
    dpos = pairs.d_r[pairs.d_r > 0]; top_share = float(dpos.max() / dpos.sum()) if len(dpos) and dpos.sum() > 0 else 0.0
    med_wo_best = float(np.median(pairs.d_r.drop(pairs.d_r.idxmax()))) if len(pairs) > 1 else 0.0
    k3 = top_share <= 0.40 and np.sign(med_wo_best) == np.sign(dr.get("median", 0)) and dr.get("median", 0) != 0
    blm = {k_: v["median"] for k_, v in pr["by_block"].items() if v.get("n", 0) >= 5}
    k4 = len(blm) >= 2 and len(set(np.sign(list(blm.values())))) == 1 and dr.get("median", 0) != 0 and np.sign(list(blm.values())[0]) == np.sign(dr.get("median", 0))
    crit = dict(k1_control=bool(k1), k2_shift=bool(k2), k3_no_dominance=bool(k3), k4_time_consistency=bool(k4)); nmet = sum(crit.values())
    ff = bool(npairs >= 10 and dr.get("median", 0) < 0 and dr.get("share_pos", 1) < 0.40)
    if formal: st = "formal_supported"
    elif nmet >= 3 and dr.get("median", 0) > 0: st = "mechanistically_promising"
    elif ff: st = "no_evidence_fast_fail"
    else: st = "no_evidence_inconclusive"
    return dict(status=st, n_pairs=npairs, v1=dict(a=bool(a1), b=bool(b1), c=bool(cnd), d=bool(d1), e=bool(e1)), v2=crit, v2_met=int(nmet), fast_fail=ff, fast_promote=formal,
                validation_eligible=bool(formal or (st == "mechanistically_promising" and len(sig) >= 20)), top_pair_share=round(top_share, 3), median_without_best=round(med_wo_best, 3), blocks_median=blm)
def make_pairs(sig, ct):
    rows = []
    for st in sig.t:
        s = sig[sig.t == st].iloc[0]; cc = ct[ct.sig_t == st] if len(ct) else ct
        if len(cc) == 0: continue
        rows.append(dict(t=st, d_r=s.r_net - cc.r_net.mean(), d_mfe=s.mfe_r - cc.mfe_r.mean(), d_capture=(s.capture - cc.capture.mean()) if np.isfinite(s.capture) and np.isfinite(cc.capture.mean()) else np.nan,
                         d_trend=float(s.cls in ("trend", "delayed_trend")) - float(cc.cls.isin(["trend", "delayed_trend"]).mean()), block=s.block, n_ctrl=len(cc)))
    return pd.DataFrame(rows)


def load_coin(COIN, AR, REPO, expected, R, D, Y):
    """Eingaben eines Coins laden und pruefen (SHAs, Datenende, Neuberechnung der Einstiege)."""
    CNT = os.path.join(AR, "rtc", {"BTC": "count_BTC_B", "XRP": "count_XRP", "DOT": "count_DOT"}[COIN]); JS = {"BTC": "count_BTC_B.json", "XRP": "count_XRP.json", "DOT": "count_DOT.json"}[COIN]
    cnt = json.load(open(os.path.join(CNT, JS)))
    spot = os.path.join(AR, "holdout", "discovery", f"{COIN}USDT_spot4h_discovery.csv"); assert "validation" not in os.path.basename(spot)
    assert sha(spot) == cnt["sha"]["spot"] and sha(os.path.join(CNT, "candidates_y1_y3.csv")) == cnt["sha"]["candidates_y1_y3"] and sha(os.path.join(CNT, "candidates_y2.csv")) == cnt["sha"]["candidates_y2"]
    entp = os.path.join(REPO, "01_forschung/11_delayed_trend/out", f"{COIN}_entries.csv"); assert sha(entp) == expected[f"01_forschung/11_delayed_trend/out/{COIN}_entries.csv"]
    C = R.cfg_btc_stufeA() if COIN == "BTC" else R.cfg_alt()
    df = Y.load(spot); f = R.features(df, C); lo, hi = Y.swings(df); n = len(df)
    assert df["t"].iat[-1] <= LAST_BAR, "Datei reicht ueber 2023-12-31 hinaus"
    cy = pd.read_csv(os.path.join(CNT, "candidates_y1_y3.csv")); y2 = pd.read_csv(os.path.join(CNT, "candidates_y2.csv")); c2 = y2[y2.y2]
    ctx = D.contexts(cy, y2, df, f); E = D.entries(ctx, df, f, lo, COIN)
    FZ = pd.read_csv(entp)
    k = ["src", "t", "fam", "status"]; a_ = E[k + ["e", "stop"]].reset_index(drop=True); b_ = FZ[k + ["e", "stop"]].reset_index(drop=True)
    same = len(a_) == len(b_) and (a_[k].astype(str).values == b_[k].astype(str).values).all() and np.allclose(a_.e.fillna(-1), b_.e.fillna(-1)) and np.allclose(a_.stop.fillna(-1), b_.stop.fillna(-1))
    assert same, f"{COIN}: Neuberechnung der Einstiege weicht von der eingefrorenen Messung ab"
    pool = Y.control_pool(cy, c2, df, f)
    blk = np.array([R.block_of(x, COIN) for x in df["t"]]); year = df.t.dt.year.to_numpy()
    d = dict(df=df, f=f, lo=lo, C=C, FZ=FZ, pool=pool, blk=blk, year=year, BLOCKS=[b for b in dict.fromkeys(blk) if b != "none"], atr_d=f["atr_d"].to_numpy(), atr4=f["atr"].to_numpy())
    info = dict(spot=sha(spot), entries_frozen=sha(entp), bars=int(n), last_bar=str(df["t"].iat[-1]), pool=int(len(pool)), mode="cfg_btc_stufeA" if COIN == "BTC" else "cfg_alt")
    return d, info


def evaluate(data, OUT, COSTS, R, D, L, rng):
    """Zellen rechnen, Kontrollen, Bootstrap in fester Reihenfolge, Holm ueber 6, Low-Frequency, A7. Schreibt CSV nach OUT."""
    RNG[0] = rng
    # ---------------- Zellen: Trades und Kontrollen (ohne Zufall) ----------------
    prep = {}
    for COIN, src, fam in PRIMARY + SECONDARY + DESCRIPTIVE:
        d = data[COIN]; key = f"{COIN}_{src}x{fam}"
        ent = d["FZ"][(d["FZ"].src == src) & (d["FZ"].fam == fam) & (d["FZ"].status == "entry")].copy()
        cost_res = {}; tr_by = {}
        for cn, K in COSTS.items():
            tr, lg = L.run_cell(ent, d["df"], d["atr_d"], K, d["atr4"]); tr_by[cn] = tr; cost_res[f"r_net_{cn}"] = stats(tr.r_net) if len(tr) else dict(n=0)
            if cn == "K1": log_k1 = lg
        tr = tr_by["K1"]
        for cn, t2 in tr_by.items():   # gleiche Ein- und Ausstiegskerzen in allen Kostenszenarien
            assert list(t2.e) == list(tr.e) and list(t2.x) == list(tr.x), f"{key}: Kostenszenario {cn} veraendert Positionen"
        sig = diag(tr, d) if len(tr) else tr
        pos = list(zip(tr.e.astype(int), tr.x.astype(int))) if len(tr) else []
        m = R.match_controls(tr[["t"]], d["pool"], d["f"], pos, d["C"]) if len(tr) else pd.DataFrame(columns=["t", "n_ctrl", "ctrls", "n_pool_window"])
        ctr = L.run_controls(m, fam, d["df"], d["atr_d"], d["atr4"], d["lo"], D, COSTS["K1"]) if len(m) else pd.DataFrame()
        ct = ctr[ctr.status == "traded"].copy() if len(ctr) else pd.DataFrame()
        if len(ct): ct = diag(ct, d)
        pairs = make_pairs(sig, ct) if len(sig) and len(ct) else pd.DataFrame(columns=["t", "d_r", "d_mfe", "d_capture", "d_trend", "block", "n_ctrl"])
        prep[key] = dict(sig=sig, ctr=ctr, ct=ct, pairs=pairs, m=m, cost_res=cost_res, log=log_k1, d=d, ent=ent)
        if len(sig): sig.to_csv(os.path.join(OUT, f"trades_{key}_K1.csv"), index=False)
        for cn in COSTS:
            if cn != "K1" and len(tr_by[cn]): tr_by[cn].to_csv(os.path.join(OUT, f"trades_{key}_{cn}.csv"), index=False)
        if len(ctr): ctr.to_csv(os.path.join(OUT, f"controls_{key}_K1.csv"), index=False)
        if len(pairs): pairs.to_csv(os.path.join(OUT, f"pairs_{key}.csv"), index=False)
        if len(m): m.assign(ctrls=m.ctrls.apply(lambda v: " ".join(map(str, v)))).to_csv(os.path.join(OUT, f"match_{key}.csv"), index=False)

    # ---------------- Auswertung in fester Reihenfolge (Bootstrap-Generator) ----------------
    res = {}
    for COIN, src, fam in PRIMARY + SECONDARY + DESCRIPTIVE:
        key = f"{COIN}_{src}x{fam}"; P_ = prep[key]; sig, ct, pairs = P_["sig"], P_["ct"], P_["pairs"]
        role = "primary" if (COIN, src, fam) in PRIMARY else ("secondary" if (COIN, src, fam) in SECONDARY else "descriptive")
        if not len(sig): res[key] = dict(role=role, signals=0); continue
        r = summarize(sig, ct, pairs, P_["cost_res"], P_["d"]["BLOCKS"])
        r.update(role=role, entries_available=int(len(P_["ent"])), log_status=P_["log"].status.value_counts().to_dict(),
                 r_net_sum_K1=round(float(sig.r_net.sum()), 4), r_net_mean_K1_exact=float(sig.r_net.mean()))
        r["controls"].update(matched_signals=int((P_["m"].n_ctrl > 0).sum()) if len(P_["m"]) else 0, n_matched_ctrls=int(P_["m"].n_ctrl.sum()) if len(P_["m"]) else 0,
                             status=P_["ctr"].status.value_counts().to_dict() if len(P_["ctr"]) else {})
        if role == "descriptive":
            r["status_v2"] = dict(status="descriptive_no_test (A2)")
        else:
            st = status_v2(r, sig, pairs) if len(pairs) else dict(status="inconclusive_insufficient_sample", n_pairs=0)
            nT = len(sig); raw = st["status"]
            if nT < 20: st["status"] = "inconclusive" if raw.startswith(("no_evidence", "inconclusive")) else "inconclusive (low-frequency, <20 Trades, deskriptiv)"; st["low_frequency"] = "<20 deskriptiv"
            elif nT < 30:
                st["low_frequency"] = "20-29 low-frequency evidence"
                if raw in ("formal_supported", "mechanistically_promising"): st["status"] = "mechanistically_promising (low-frequency)"
            else: st["low_frequency"] = "normal (>=30)"
            st["status_raw"] = raw; r["status_v2"] = st
        r["a6_net_K1_ge_0"] = bool(sig.r_net.mean() >= 0)
        res[key] = r
    tested = [f"{c}_{s}x{f}" for c, s, f in PRIMARY + SECONDARY]
    pv = {k_: res[k_]["paired"]["d_r"].get("p_boot_le0") for k_ in tested if res[k_].get("signals", 0) and res[k_]["paired"].get("d_r", {}).get("n", 0) >= 2}
    order = sorted(pv, key=lambda k_: pv[k_]); mtot = len(order); holm = {}; prev = 0
    for i, k_ in enumerate(order):
        adj = min(1.0, max(prev, pv[k_] * (mtot - i))); holm[k_] = dict(p=pv[k_], p_holm=round(adj, 4), signal_present=bool(adj < 0.05 and res[k_]["paired"]["d_r"]["mean"] > 0 and res[k_]["costs"]["r_net_K1"]["mean"] > 0)); prev = adj
    for k_ in tested:
        if k_ not in holm: holm[k_] = dict(p=None, p_holm=None, signal_present=False, note="weniger als 2 Paare")
    prim_keys = [f"{c}_{s}x{f}" for c, s, f in PRIMARY]
    tot = float(sum(prep[k_]["sig"].r_net.sum() for k_ in prim_keys if len(prep[k_]["sig"]))); ntot = int(sum(len(prep[k_]["sig"]) for k_ in prim_keys))
    a7 = dict(rule="Summe r_net K1 ueber alle Trades der drei Primaerzellen < 0 -> Lane A geschlossen", sum_r_net_K1=round(tot, 4), n_trades=ntot, pooled_mean_K1=round(tot / ntot, 4) if ntot else None,
              unweighted_mean_of_cells=round(float(np.mean([res[k_]["r_net_mean_K1_exact"] for k_ in prim_keys if res[k_].get("signals", 0)])), 4), lane_a_closed=bool(tot < 0))
    return res, holm, a7


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--lauf", action="store_true"); ap.add_argument("--out", default=os.path.join(HERE, "run"))
    a = ap.parse_args()
    if not a.lauf: sys.exit("Nur mit --lauf (einziger Lauf).")
    OUT = a.out; os.makedirs(OUT, exist_ok=True)
    if os.path.exists(os.path.join(OUT, "dt_pnl_eval.json")): sys.exit("ABBRUCH: dt_pnl_eval.json existiert, kein zweiter Lauf.")
    if os.path.exists("/home/claude"): sys.exit("ABBRUCH: /home/claude existiert (ueberschattet rlib/dtlib).")
    assert os.environ.get("AURUM_VALIDATION") is None, "AURUM_VALIDATION gesetzt"
    spec_sha = sha(SPEC); assert spec_sha == SPEC_SHA, f"Spec-SHA {spec_sha} != eingefroren {SPEC_SHA}"
    for d in ("pylib", "yamato", "rtc", "dt"): sys.path.insert(0, os.path.join(AR, d))
    sys.path.insert(0, HERE)
    import rlib as R; import dtlib as D; import dt_pnl as L; Y = R.Y
    assert sha(os.path.join(AR, "rtc", "rlib.py")) == RLIB_SHA and sha(os.path.join(AR, "dt", "dtlib.py")) == DTLIB_SHA
    assert os.path.realpath(R.__file__) == os.path.realpath(os.path.join(AR, "rtc", "rlib.py")) and os.path.realpath(D.__file__) == os.path.realpath(os.path.join(AR, "dt", "dtlib.py"))
    expected = {}
    for line in open(os.path.join(REPO, "01_forschung/11_delayed_trend/dt_expected_shas.txt")):
        s, p = line.split(); expected[p] = s
    COSTS = L.costs(Y, None)
    meta = dict(spec="dt_pnl_spec_v1.0.md", spec_sha256=spec_sha, started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), seed=SEED, nb=NB,
                inputs=dict(rlib=sha(os.path.join(AR, "rtc", "rlib.py")), dtlib=sha(os.path.join(AR, "dt", "dtlib.py")), ylib_portable=sha(Y.__file__), lib=sha(os.path.join(HERE, "dt_pnl.py")), run=sha(__file__),
                            cost_model=sha(os.path.join(REPO, "config", "cost_model_v1.json"))), costs=COSTS, checks={}, coins={})
    conv = lambda x: None if isinstance(x, float) and np.isnan(x) else (bool(x) if isinstance(x, np.bool_) else (int(x) if isinstance(x, np.integer) else (float(x) if isinstance(x, np.floating) else str(x))))
    json.dump(dict(meta, status="gestartet"), open(os.path.join(OUT, "dt_pnl_run.log"), "w"), indent=1, default=conv)
    rng = np.random.default_rng(SEED)
    data = {}
    for COIN in ("BTC", "XRP", "DOT"):
        data[COIN], meta["coins"][COIN] = load_coin(COIN, AR, REPO, expected, R, D, Y)
    meta["checks"]["entries_recomputed_equal_frozen"] = True
    meta["checks"]["last_bar_le_2023_12_31_20UTC"] = True

    res, holm, a7 = evaluate(data, OUT, COSTS, R, D, L, rng)
    tested = [f"{c}_{s}x{f}" for c, s, f in PRIMARY + SECONDARY]
    meta["finished_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    meta["checks"]["cost_scenarios_same_positions"] = True
    meta["status"] = "fertig"
    rep = dict(meta=meta, cells=res, holm=holm, a7=a7)
    json.dump(meta, open(os.path.join(OUT, "dt_pnl_run.log"), "w"), indent=1, default=conv)
    json.dump(rep, open(os.path.join(OUT, "dt_pnl_eval.json"), "w"), indent=1, default=conv)
    for k_ in tested + [f"{c}_{s}x{f}" for c, s, f in DESCRIPTIVE]:
        r = res[k_]
        if not r.get("signals"): print(k_, "keine Trades"); continue
        print(f"{k_:14s} {r['role']:11s} n={r['signals']:3d} K1 mean={r['costs']['r_net_K1'].get('mean')} pairs={r['paired']['n_pairs']} dR={r['paired'].get('d_r', {}).get('mean')} holm={holm.get(k_, {}).get('p_holm')} status={r['status_v2']['status']}")
    print("A7", a7)


if __name__ == "__main__":
    main()
