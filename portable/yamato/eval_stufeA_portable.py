# PORTABLE VERSION, generiert von tools/make_portable.py. NICHT VON HAND AENDERN.
# Quelle (eingefroren): 01_forschung/06_btc_specialist/stufeA/eval_stufeA.py  sha256 60efb294fe3340c8304077d30b16da16c7214affb00dec36da69c8a3c63ad100
# Regeln: paths. Arbeitsbereich: AURUM_ROOT (Default: Ordner '..' relativ zu dieser Datei).
import os as _aos; _AR = _aos.environ.get("AURUM_ROOT") or _aos.path.abspath(_aos.path.join(_aos.path.dirname(_aos.path.abspath(__file__)), ".."))
"""BTC YAMATO RTC Stufe A — einmaliger Outcome-Lauf (Plan v1.1, Auswertungsregeln v1). Seed 20260917."""
import numpy as np, pandas as pd, sys, json, hashlib
sys.path.insert(0, _AR + "/yamato"); import ylib as Y
SEED = 20260917; NB = 2000
df = Y.load("data/BTCUSDT_4h_discovery.csv"); f = Y.features(df); lo, hi = Y.swings(df)
o, h, l, c, v = (df[k].to_numpy() for k in ("open", "high", "low", "close", "volume"))
atr = f.atr.to_numpy(); n = len(df)
tb = df["taker_buy_quote"].to_numpy(); qv = df["quote_volume"].to_numpy()
ti = np.where(qv > 0, (2 * tb - qv) / qv, np.nan); volz = f.volz.to_numpy()
cy = pd.read_csv("data/candidates_y1_y3.csv"); y2 = pd.read_csv("data/candidates_y2.csv"); y2c = y2[y2.y2]
P2 = pd.Timestamp("2021-01-01", tz="UTC"); block = np.where(df.t < P2, "P1", "P2")
year = df.t.dt.year.to_numpy()

def diag(tr):
    """Diagnosemetriken je Trade (U17), Follow-through, Klassifikation (Plan Abschnitt 4)."""
    out = []
    for _, r in tr.iterrows():
        e, x, entry, exitp, R = int(r.e), int(r.x), r.entry, r.exit, r.R
        lo_ref = l[max(0, e - 120): min(n, e + 13)].min()
        hi_ref = h[e: min(n, x + 61)].max(); span = hi_ref - lo_ref
        pre_hi = h[max(0, e - 120): e].max()
        ok60 = (x + 60) < n
        d = dict(entry_eff=(1 - (entry - lo_ref) / span) if span > 0 else np.nan,
                 exit_eff=(1 - (hi_ref - exitp) / span) if (span > 0 and ok60) else np.nan,
                 capture=(exitp - entry) / span if (span > 0 and ok60) else np.nan,
                 dist_low_atr=(entry - lo_ref) / atr[e], giveback_r=r.mfe_r - r.r_gross)
        # neuer Trend: Schluss ueber pre_hi innerhalb 42/84/180/360 Kerzen
        for hz, lab in ((42, "7d"), (84, "14d"), (180, "30d"), (360, "60d")):
            seg = c[e + 1: min(n, e + 1 + hz)]
            d[f"trend_{lab}"] = bool((seg > pre_hi).any()) if (e + hz) < n else np.nan
        # Persistenz: nach erstem neuen Hoch 30 Kerzen ueber pre_hi
        seg = c[e + 1: min(n, e + 361)]; idx = np.where(seg > pre_hi)[0]
        if len(idx) and (e + 1 + idx[0] + 30) < n:
            d["persist30"] = bool((c[e + 1 + idx[0]: e + 1 + idx[0] + 30] > pre_hi).all())
        else:
            d["persist30"] = np.nan
        t30, t60 = d["trend_30d"], d["trend_60d"]
        if t30 is True: cls = "trend"
        elif (t60 is True) and r.mfe_r >= 1: cls = "delayed_trend"
        elif r.mfe_r >= 1 and (t60 is False): cls = "rebound"
        elif r.mfe_r < 1: cls = "fail"
        else: cls = "na"
        d["cls"] = cls
        # Follow-through 1/3/6 Kerzen nach Einstieg
        for k in (1, 3, 6):
            if e + k < n:
                d[f"ft{k}_px_atr"] = (c[e + k] - entry) / atr[e]
                d[f"ft{k}_volz"] = np.nanmean(volz[e: e + k + 1]); d[f"ft{k}_ti"] = np.nanmean(ti[e: e + k + 1])
        d["ft_absorb"] = bool(d.get("ft3_ti", 0) > 0.2 and d.get("ft3_px_atr", 1) < 0.5) if e + 3 < n else np.nan
        d["block"] = block[int(r.t)]; d["year"] = int(year[int(r.t)])
        out.append(d)
    return pd.concat([tr.reset_index(drop=True), pd.DataFrame(out)], axis=1)

def stats(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) == 0: return dict(n=0)
    return dict(n=int(len(x)), mean=round(float(x.mean()), 3), median=round(float(np.median(x)), 3),
                p5=round(float(np.percentile(x, 5)), 3), p95=round(float(np.percentile(x, 95)), 3),
                win=round(float((x > 0).mean()), 3))

def boot(x, rng):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) < 2: return dict(n=int(len(x)))
    m = np.array([rng.choice(x, len(x)).mean() for _ in range(NB)])
    return dict(n=int(len(x)), mean=round(float(x.mean()), 3), b_p5=round(float(np.percentile(m, 5)), 3),
                b_p95=round(float(np.percentile(m, 95)), 3), p_pos=round(float((m > 0).mean()), 3))

rep = {"seed": SEED, "cost_primary": "K1"}; rng = np.random.default_rng(SEED)
all_sig = {}; all_ctrl = {}
for kind, cand in (("Y1", cy[cy.y1]), ("Y2", y2c), ("Y3", cy[cy.y3])):
    res = {}
    for cost in ("K0", "K1", "K2"):
        tr, lg = Y.run_sleeve(cand.sort_values("t"), df, f, lo, kind, cost)
        if cost == "K1": tr_main = tr
        res[f"r_net_{cost}"] = stats(tr.r_net) if len(tr) else dict(n=0)
    if not len(tr_main):
        rep[kind] = dict(signals=0); continue
    sig = diag(tr_main); sig["kind"] = kind; all_sig[kind] = sig
    # Kontrollen (U15, U21)
    pool = Y.control_pool(cy, y2c, df, f); pos = list(zip(tr_main.e.astype(int), tr_main.x.astype(int)))
    if kind == "Y2":
        ref = y2c.set_index("t").loc[tr_main.t, "s2"].astype(int).to_numpy(); m = Y.match_controls(pd.DataFrame(dict(t=ref)), pool, f, pos)
    else:
        m = Y.match_controls(tr_main[["t"]], pool, f, pos)
    ctr_rows = []
    for (_, mr), st in zip(m.iterrows(), tr_main.t):
        for cb in mr.ctrls:
            e = Y.trigger_ta(cb, df)
            if e is None: ctr_rows.append(dict(sig_t=st, ctrl_t=cb, status="no_trigger")); continue
            stop0 = l[cb] - Y.FROZEN["stop_pad"] * atr[cb]
            if o[e] - stop0 > Y.FROZEN["stop_max"] * atr[cb] or o[e] <= stop0:
                ctr_rows.append(dict(sig_t=st, ctrl_t=cb, status="stop_too_wide")); continue
            t = Y.simulate_trade(e, stop0, df, f, lo, "K1"); t.update(sig_t=st, ctrl_t=cb, t=cb, status="traded"); ctr_rows.append(t)
    ctr = pd.DataFrame(ctr_rows); ctr_tr = ctr[ctr.status == "traded"].copy()
    if len(ctr_tr): ctr_tr = diag(ctr_tr); ctr_tr["kind"] = kind + "_ctrl"; all_ctrl[kind] = ctr_tr
    # gepaarte Differenzen
    pairs = []
    for st in tr_main.t:
        s = sig[sig.t == st].iloc[0]; cc = ctr_tr[ctr_tr.sig_t == st] if len(ctr_tr) else ctr_tr
        if len(cc) == 0: continue
        pairs.append(dict(t=st, d_r=s.r_net - cc.r_net.mean(), d_mfe=s.mfe_r - cc.mfe_r.mean(),
                          d_capture=s.capture - cc.capture.mean() if np.isfinite(s.capture) and np.isfinite(cc.capture.mean()) else np.nan,
                          d_trend=float(s.cls in ("trend", "delayed_trend")) - float(cc.cls.isin(["trend", "delayed_trend"]).mean()), block=s.block, n_ctrl=len(cc)))
    pairs = pd.DataFrame(pairs)
    gross_pos = sig.r_gross[sig.r_gross > 0]; conc = float(gross_pos.max() / gross_pos.sum()) if len(gross_pos) else np.nan
    yrs = sig.groupby("year").r_net.sum(); years_pos = int((yrs > 0).sum())
    r = dict(signals=int(len(sig)), blocks=sig.block.value_counts().to_dict(), costs=res,
             r_gross=stats(sig.r_gross), mfe_r=stats(sig.mfe_r), mae_r=stats(sig.mae_r), bars=stats(sig.bars),
             stop_dist_atr=stats(sig.stop_dist_atr), entry_eff=stats(sig.entry_eff), exit_eff=stats(sig.exit_eff),
             capture=stats(sig.capture), giveback_r=stats(sig.giveback_r), dist_low_atr=stats(sig.dist_low_atr),
             exit_reason=sig.reason.value_counts().to_dict(), cls=sig.cls.value_counts().to_dict(),
             trend_rate={k: round(float(sig[k].dropna().astype(float).mean()), 3) for k in ("trend_7d", "trend_14d", "trend_30d", "trend_60d")},
             persist30=round(float(sig.persist30.dropna().astype(float).mean()), 3) if sig.persist30.notna().any() else None,
             ft={k: round(float(sig[k].mean()), 3) for k in sig.columns if k.startswith("ft") and k != "ft_absorb"},
             ft_absorb_rate=round(float(sig.ft_absorb.dropna().astype(float).mean()), 3),
             concentration_top1=round(conc, 3) if np.isfinite(conc) else None, years_positive=years_pos, years_total=int(len(yrs)),
             by_block={b: stats(sig[sig.block == b].r_net) for b in ("P1", "P2")},
             controls=dict(matched=int(len(m)), traded=int(len(ctr_tr)), status=ctr.status.value_counts().to_dict() if len(ctr) else {},
                           r_net=stats(ctr_tr.r_net) if len(ctr_tr) else {}, mfe_r=stats(ctr_tr.mfe_r) if len(ctr_tr) else {},
                           capture=stats(ctr_tr.capture) if len(ctr_tr) else {}, cls=ctr_tr.cls.value_counts().to_dict() if len(ctr_tr) else {},
                           entry_eff=stats(ctr_tr.entry_eff) if len(ctr_tr) else {}),
             paired=dict(n_pairs=int(len(pairs)), d_r=boot(pairs.d_r, rng) if len(pairs) else {}, d_mfe=boot(pairs.d_mfe, rng) if len(pairs) else {},
                         d_capture=boot(pairs.d_capture, rng) if len(pairs) else {}, d_trend=boot(pairs.d_trend, rng) if len(pairs) else {},
                         by_block={b: stats(pairs[pairs.block == b].d_r) for b in ("P1", "P2")} if len(pairs) else {}))
    # Status nach Auswertungsregeln v1 Abschnitt 2
    pr = r["paired"]; dr = pr.get("d_r", {}); dm = pr.get("d_mfe", {}); dc = pr.get("d_capture", {})
    a = dr.get("mean", -1) > 0 and dr.get("p_pos", 0) >= 0.80
    b = (r["mfe_r"].get("median", 0) > r["controls"]["mfe_r"].get("median", 0)) and dc.get("mean", -1) > 0
    bb = pr.get("by_block", {}); bl = [bb[k]["mean"] for k in bb if bb[k].get("n", 0) >= 5]
    cnd = (all(x > 0 for x in bl) if len(bl) == 2 else dr.get("mean", -1) > 0)
    d = (conc if np.isfinite(conc) else 0) <= 0.40; e_ = r["costs"]["r_net_K1"].get("mean", -1) > 0
    mp = bool(a and b and cnd and d and e_)
    ff = bool((dr.get("mean", 0) <= 0 and dm.get("mean", 0) <= 0) or (r["r_gross"]["mean"] > 0 and r["costs"]["r_net_K1"]["mean"] <= 0 and r["costs"]["r_net_K2"]["mean"] < 0) or (len(bl) == 2 and all(x < 0 for x in bl)))
    # Statuszuweisung nur mit mindestens 5 gepaarten Beobachtungen (Auswertungsregeln v1, Praezisierung nach dem Lauf, siehe Bericht)
    enough = int(pr.get("n_pairs", 0)) >= 5
    if not enough: mp = False; ff = False
    status = "mechanistically_promising" if mp else ("not_supported_fast_fail" if ff else "inconclusive_insufficient_sample")
    fast_promote = bool(mp and years_pos >= 2)
    r["status"] = dict(status=status, conditions=dict(a=bool(a), b=bool(b), c=bool(cnd), d=bool(d), e=bool(e_)), fast_fail=ff, fast_promote=fast_promote, enough_pairs=enough)
    # P&L in ATR (R mal Stopdistanz), weil R-Definitionen zwischen Y2 und Kontrollen verschieden sind
    r["pnl_atr"] = stats(sig.r_net * sig.stop_dist_atr)
    if len(ctr_tr): r["controls"]["pnl_atr"] = stats(ctr_tr.r_net * (ctr_tr.entry - ctr_tr.stop0) / atr[ctr_tr.t.astype(int).to_numpy()])
    rep[kind] = r
    sig.to_csv(f"data/trades_{kind}_K1.csv", index=False); ctr.to_csv(f"data/controls_{kind}_K1.csv", index=False); pairs.to_csv(f"data/pairs_{kind}.csv", index=False)
# Ueberlappung Y1/Y3 auf Signalebene
s1 = set(all_sig["Y1"].t) if "Y1" in all_sig else set(); s3 = set(all_sig["Y3"].t) if "Y3" in all_sig else set()
rep["overlap_signals"] = dict(Y1_and_Y3=len(s1 & s3))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
rep["sha256"] = dict(input=sha("data/BTCUSDT_4h_discovery.csv"), ylib=sha("ylib.py"), eval=sha("eval_stufeA.py"))
json.dump(rep, open("data/eval_stufeA.json", "w"), indent=1, default=lambda x: None if isinstance(x, float) and np.isnan(x) else (bool(x) if isinstance(x, np.bool_) else x))
print("done")
