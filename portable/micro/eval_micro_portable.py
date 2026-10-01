# PORTABLE VERSION, generiert von tools/make_portable.py. NICHT VON HAND AENDERN.
# Quelle (eingefroren): 01_forschung/10_rebound_micro/mlib/eval_micro.py  sha256 91f6455ecb2bd74d629a0fc61fe17487bfa17b1ff624f10c1af7e90206306eb4
# Regeln: paths, sha_self. Arbeitsbereich: AURUM_ROOT (Default: Ordner '..' relativ zu dieser Datei).
import os as _aos; _AR = _aos.environ.get("AURUM_ROOT") or _aos.path.abspath(_aos.path.join(_aos.path.dirname(_aos.path.abspath(__file__)), ".."))
_FROZEN_SELF = _aos.path.join(_aos.path.dirname(_aos.path.abspath(__file__)), "eval_micro.py")  # eingefrorenes Original im Arbeitsbereich
"""
Project Aurum II — REBOUND-MICRO Auswertung je Coin, Version 1.0 (rebound_micro_spec_v1.0.md Abschnitte 7 bis 10).
Aufruf: python3 eval_micro.py COIN -> run/{COIN}_eval.json. Kein Pooling ueber Coins. Seed 20260918, Bootstrap 2000.
"""
import sys, json, hashlib, numpy as np, pandas as pd
from scipy import stats
sys.path.insert(0, _AR + "/micro"); sys.path.insert(0, _AR + "/rtc"); import rlib as R

SEED, NBOOT = 20260918, 2000
PRIMARY = ["M1xQ0", "M1xQ1"]
BLOCKS = {"BTC": ["P1", "P2"], "XRP": ["P1", "P2"], "DOT": ["P2a", "P2b"]}
ETH_SOL_1H = {"ETH": 13950 * 4, "SOL": 7427 * 4}       # aus Holdout-Manifest v1.1 (4h-Zeilen x 4), keine ETH/SOL-Daten geladen


def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()


def boot_mean(x, seed=SEED, n=NBOOT):
    x = np.asarray(x, float); rng = np.random.default_rng(seed)
    if len(x) == 0: return dict(mean=np.nan, p_pos=np.nan, ci_lo=np.nan, ci_hi=np.nan)
    m = np.array([rng.choice(x, len(x), replace=True).mean() for _ in range(n)])
    return dict(mean=float(x.mean()), p_pos=float((m > 0).mean()), p_le0=float((m <= 0).mean()), ci_lo=float(np.quantile(m, .025)), ci_hi=float(np.quantile(m, .975)))


def cell_stats(t, k="K1", coin="BTC", n_bars_1h=None):
    r = t[f"r_net_{k}"].to_numpy(float); n = len(r)
    if n == 0: return dict(n=0)
    win = r[r > 0]; loss = r[r < 0]; reasons = t[f"reason_{k}"].value_counts().to_dict()
    aw = float(win.mean()) if len(win) else np.nan; al = float(loss.mean()) if len(loss) else np.nan
    bm = boot_mean(r)
    d = dict(n=int(n), hit_rate=float((r > 0).mean()), target_rate=float(t[f"reason_{k}"].isin(["target", "target_gap"]).mean()),
             stop_rate=float(t[f"reason_{k}"].isin(["stop", "stop_gap", "stop_ambiguous"]).mean()), time_rate=float(t[f"reason_{k}"].isin(["time24", "cut"]).mean()), reasons=reasons,
             avg_win_R=aw, avg_loss_R=al, win_loss_ratio=float(aw / abs(al)) if len(win) and len(loss) else np.nan,
             p_be_emp=float(abs(al) / (aw + abs(al))) if len(win) and len(loss) else np.nan,
             mean_r=float(r.mean()), median_r=float(np.median(r)), sum_r=float(r.sum()), p_pos=bm["p_pos"], ci=[bm["ci_lo"], bm["ci_hi"]],
             profit_factor=float(win.sum() / abs(loss.sum())) if len(loss) and loss.sum() != 0 else np.nan,
             cost_R_median=float(t[f"cost_R_{k}"].median()), stop_atr4_median=float(t.entry_to_stop_atr4.median()),
             top1_share=float(win.max() / win.sum()) if len(win) else np.nan, mean_without_best=float(np.delete(r, r.argmax()).mean()) if n > 1 else np.nan,
             bars_held_median=float(t.bars_held.median()))
    d["blocks"] = {b: dict(n=int((t.block == b).sum()), mean_r=float(r[(t.block == b).to_numpy()].mean()) if (t.block == b).any() else np.nan) for b in BLOCKS[coin]}
    if k == "K1":
        st = t[t.reason.isin(["stop", "stop_gap", "stop_ambiguous"])]; tg = t[t.reason.isin(["target", "target_gap"])]
        d["stop_then_target_share"] = float(st.stop_then_target.astype(float).mean()) if len(st) else np.nan
        d["mfe_after_target_R_median"] = float(tg.mfe_after_target_R.median()) if len(tg) else np.nan
        d["new20d_high_share"] = float(tg.new20d_high.astype(float).mean()) if len(tg) else np.nan; d["new30d_high_share"] = float(tg.new30d_high.astype(float).mean()) if len(tg) else np.nan
        if n_bars_1h: d["rate_per_1000_bars"] = float(n / n_bars_1h * 1000); d["expected_eth_sol"] = {c: float(n / n_bars_1h * ETH_SOL_1H[c]) for c in ETH_SOL_1H}
    return d


def paired(cell, base, k):
    m = cell.merge(base[["event", f"r_net_{k}"]].rename(columns={f"r_net_{k}": "r_base"}), on="event", how="inner")
    d = (m[f"r_net_{k}"] - m.r_base).to_numpy(float)
    if len(d) == 0: return dict(n_pairs=0)
    bm = boot_mean(d); pos = int((d > 0).sum()); neg = int((d < 0).sum())
    out = dict(n_pairs=int(len(d)), mean_diff=bm["mean"], median_diff=float(np.median(d)), share_pos=float((d > 0).mean()), p_boot_one_sided=bm["p_le0"], ci=[bm["ci_lo"], bm["ci_hi"]],
               sign_test_p=float(stats.binomtest(pos, pos + neg, 0.5, alternative="greater").pvalue) if pos + neg else np.nan,
               mean_cell=float(m[f"r_net_{k}"].mean()), mean_base_paired=float(m.r_base.mean()))
    if len(d) >= 10 and (d != 0).any():
        try: out["wilcoxon_p"] = float(stats.wilcoxon(d, alternative="greater").pvalue)
        except Exception: out["wilcoxon_p"] = np.nan
    return out


def holm(pvals):
    names = list(pvals); p = np.array([pvals[n] for n in names], float); order = np.argsort(p); m = len(p); adj = np.empty(m)
    run = 0.0
    for rank, i in enumerate(order):
        run = max(run, (m - rank) * p[i]); adj[i] = min(1.0, run)
    return {n: float(a) for n, a in zip(names, adj)}


def promotion_check(cs, pr, k="K1"):
    """Sechs Bedingungen plus Baseline-Bedingung (Promotion-Regeln v0.1 Abschnitt 2), je Zelle und Coin."""
    if cs.get("n", 0) == 0: return dict(eligible=False, reason="no trades")
    c = dict(
        c1_geometry=bool(cs["win_loss_ratio"] >= 0.80 and cs["stop_atr4_median"] <= 0.60) if np.isfinite(cs.get("win_loss_ratio", np.nan)) else False,
        c2_pbe=bool(cs["p_be_emp"] <= 0.60) if np.isfinite(cs.get("p_be_emp", np.nan)) else False,
        c3_not_negative=bool(cs["mean_r"] >= -0.05 and cs["p_pos"] >= 0.40 and (np.isfinite(cs["profit_factor"]) and cs["profit_factor"] >= 0.90)),
        c4_sample=bool(cs["n"] >= 30 and all(v >= 30 for v in cs.get("expected_eth_sol", {}).values())),
        c5_concentration=bool(np.isfinite(cs["top1_share"]) and cs["top1_share"] <= 0.40 and np.sign(cs["mean_without_best"]) == np.sign(cs["mean_r"])),
        c6_blocks=bool(sum(1 for b in cs["blocks"].values() if b["n"] >= 10 and b["mean_r"] >= -0.05) >= 2),
        c7_baseline=bool(pr.get("n_pairs", 0) > 0 and pr["median_diff"] > 0 and pr["share_pos"] >= 0.55))
    c["all"] = all(c.values()); return c


def mp_rule_v2(cs, pr):
    """Governance v1.1 Regel v2: >= 3 von 4 -> mechanistisch vielversprechend (auf Baseline-Paare bezogen)."""
    a = bool(pr.get("n_pairs", 0) >= 1 and pr["median_diff"] > 0 and pr["share_pos"] >= 0.60)
    b = bool(cs.get("n", 0) and (cs["win_loss_ratio"] >= 0.80 if np.isfinite(cs.get("win_loss_ratio", np.nan)) else False))   # Ersatz fuer MFE/Capture: Geometrie-Verbesserung
    c = bool(np.isfinite(cs.get("top1_share", np.nan)) and cs["top1_share"] <= 0.40 and np.sign(cs["mean_without_best"]) == np.sign(cs["mean_r"]))
    d = bool(sum(1 for x in cs["blocks"].values() if x["n"] >= 5 and np.sign(x["mean_r"]) == np.sign(cs["mean_r"])) >= 2) if cs.get("n", 0) else False
    ff = bool(pr.get("n_pairs", 0) >= 10 and pr["median_diff"] < 0 and pr["share_pos"] < 0.40)
    return dict(a_control=a, b_geometry=b, c_concentration=c, d_blocks=d, count=int(a + b + c + d), mechanistically_promising=bool((a + b + c + d) >= 3), fast_fail=ff)


def status(cs, pr, mp):
    n = cs.get("n", 0)
    if n < 20: return "descriptive (<20)"
    tier = "low-frequency (20-29)" if n < 30 else "normal (>=30)"
    if mp["fast_fail"]: return f"{tier}: fast fail"
    if mp["mechanistically_promising"]: return f"{tier}: mechanistically promising (MP)"
    return f"{tier}: no evidence / inconclusive"


def main(coin):
    T = pd.read_csv(_AR + f"/micro/run/{coin}_trades.csv"); B = pd.read_csv(_AR + f"/micro/run/{coin}_baseline.csv")
    try: Cn = pd.read_csv(_AR + f"/micro/run/{coin}_controls.csv")
    except Exception: Cn = pd.DataFrame()
    log = json.load(open(_AR + f"/micro/run/{coin}_run.log"))
    n_bars = int(pd.read_csv(_AR + f"/micro/raw/{coin}USDT_spot_1h.csv", usecols=[0]).shape[0])
    ev = dict(coin=coin, spec="rebound_micro_spec_v1.0.md", inputs=dict(trades=sha(_AR + f"/micro/run/{coin}_trades.csv"), baseline=sha(_AR + f"/micro/run/{coin}_baseline.csv"),
              controls=sha(_AR + f"/micro/run/{coin}_controls.csv"), run_log=log["inputs"], eval_script=sha(_FROZEN_SELF)), seed=SEED, nboot=NBOOT, n_bars_1h_total=n_bars)
    ev["status_counts"] = {cell: T[T.cell == cell].status.value_counts().to_dict() for cell in sorted(T.cell.unique())}
    ev["baseline_status_counts"] = {cell: B[B.cell == cell].status.value_counts().to_dict() for cell in sorted(B.cell.unique())}
    cells = {}
    for cell in sorted(T.cell.unique()):
        t = T[(T.cell == cell) & (T.status == "traded")]; q = cell.split("x")[1]
        base = B[(B.cell == f"BASEx{q}") & (B.status == "traded")]
        d = {k: cell_stats(t, k, coin, n_bars) for k in ("K0", "K1", "K2")}
        d["paired_vs_baseline"] = {k: paired(t, base, k) for k in ("K0", "K1", "K2")}
        d["n_unpaired_cell"] = int((~t.event.isin(base.event)).sum())
        if cell.startswith("M1"):
            for name, mask in (("flow_flag", t.flow_flag), ("harami", t.harami), ("hikkake", t.hikkake)):
                sub = t[mask.astype(bool)]; d[f"subset_{name}"] = dict(n=int(len(sub)), mean_r_K1=float(sub.r_net_K1.mean()) if len(sub) else np.nan)
        if len(Cn) and "cell" in Cn:
            cn = Cn[(Cn.cell == cell) & (Cn.status == "traded")]
            if len(cn):
                per_sig = cn.groupby("sig_t4").r_net_K1.mean().rename("ctrl_mean"); m = t.merge(per_sig, left_on="t4", right_index=True, how="inner")
                dd = (m.r_net_K1 - m.ctrl_mean).to_numpy(float)
                d["controls"] = dict(n_ctrl_trades=int(len(cn)), ctrl_mean_r_K1=float(cn.r_net_K1.mean()), ctrl_median_r_K1=float(cn.r_net_K1.median()), n_events_with_ctrl=int(len(m)),
                                     diff_mean=float(dd.mean()) if len(dd) else np.nan, diff_median=float(np.median(dd)) if len(dd) else np.nan, diff_share_pos=float((dd > 0).mean()) if len(dd) else np.nan)
            else: d["controls"] = dict(n_ctrl_trades=0)
        d["promotion"] = promotion_check(d["K1"], d["paired_vs_baseline"]["K1"])
        d["mp_rule_v2"] = mp_rule_v2(d["K1"], d["paired_vs_baseline"]["K1"]) if d["K1"].get("n", 0) else dict(fast_fail=False, mechanistically_promising=False)
        d["status"] = status(d["K1"], d["paired_vs_baseline"]["K1"], d["mp_rule_v2"]) if cell.startswith("M1") else "descriptive / insufficient sample (Entscheidung 1)"
        cells[cell] = d
    ev["cells"] = cells
    ev["baseline"] = {cell: {k: cell_stats(B[(B.cell == cell) & (B.status == "traded")], k, coin, n_bars) for k in ("K0", "K1", "K2")} for cell in sorted(B.cell.unique())}
    pv = {c: cells[c]["paired_vs_baseline"]["K1"].get("p_boot_one_sided", np.nan) for c in PRIMARY if c in cells}
    ev["primary_tests"] = dict(cells=PRIMARY, p_raw=pv, p_holm=holm({c: (p if np.isfinite(p) else 1.0) for c, p in pv.items()}), alpha=0.05)
    ev["primary_tests"]["significant_holm"] = [c for c, p in ev["primary_tests"]["p_holm"].items() if p < 0.05]
    # Frage C: Q1 gegen Q0 auf denselben M1-Trades (gleiche Events, beide gehandelt)
    a = T[(T.cell == "M1xQ0") & (T.status == "traded")]; b = T[(T.cell == "M1xQ1") & (T.status == "traded")]
    m = a.merge(b[["event", "r_net_K1", "reason"]].rename(columns={"r_net_K1": "r_q1", "reason": "reason_q1"}), on="event", how="inner")
    if len(m):
        dd = (m.r_q1 - m.r_net_K1).to_numpy(float); bm = boot_mean(dd)
        ev["q1_vs_q0_same_trades"] = dict(n=int(len(m)), mean_q0=float(m.r_net_K1.mean()), mean_q1=float(m.r_q1.mean()), mean_diff=bm["mean"], median_diff=float(np.median(dd)), share_q1_better=float((dd > 0).mean()), p_pos=bm["p_pos"],
                                          target_rate_q0=float(m.reason.isin(["target", "target_gap"]).mean()), target_rate_q1=float(m.reason_q1.isin(["target", "target_gap"]).mean()))
    json.dump(ev, open(_AR + f"/micro/run/{coin}_eval.json", "w"), indent=1, default=str)
    return ev


if __name__ == "__main__":
    ev = main(sys.argv[1])
    for c, d in ev["cells"].items():
        k = d["K1"]; p = d["paired_vs_baseline"]["K1"]
        print(c, "n", k.get("n"), "mean", round(k.get("mean_r", np.nan), 3), "hit", round(k.get("hit_rate", np.nan), 2), "w/l", round(k.get("win_loss_ratio", np.nan), 2), "pbe", round(k.get("p_be_emp", np.nan), 2),
              "| pairs", p.get("n_pairs"), "meddiff", round(p.get("median_diff", np.nan), 3), "pos", round(p.get("share_pos", np.nan), 2), "|", d["status"])
    print("primary", ev["primary_tests"])
