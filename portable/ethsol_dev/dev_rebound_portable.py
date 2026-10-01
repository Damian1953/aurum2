# PORTABLE VERSION, generiert von tools/make_portable.py. NICHT VON HAND AENDERN.
# Quelle (eingefroren): 01_forschung/07_eth_sol_specialist/dev/dev_rebound.py  sha256 9ddf6c3c7088203c21596174b9d862b166840ba7d0b2feabd6b79a2830c8907f
# Regeln: paths. Arbeitsbereich: AURUM_ROOT (Default: Ordner '..' relativ zu dieser Datei).
import os as _aos; _AR = _aos.environ.get("AURUM_ROOT") or _aos.path.abspath(_aos.path.join(_aos.path.dirname(_aos.path.abspath(__file__)), ".."))
"""Development-Analyse REBOUND-20 (nur BTC, XRP, DOT; keine ETH/SOL-Daten). Grössen am Einstieg: potential_atr = (EMA20_t - open_e)/ATR14_t, potential_R = (EMA20_t - open_e)/R.
EMA20_t = EMA20 am Schluss der Kandidatenkerze t (vor Einstieg bekannt). Outcome: r_net der E0-Simulation (Schluss >= EMA20 -> naechste Eroeffnung, sonst 30 Kerzen, initialer Stop), K1."""
import sys, json, numpy as np, pandas as pd
sys.path.insert(0, _AR + "/rtc"); import rlib as R; Y = R.Y
out = {}
def analyse(coin, df, f, trades_by_fam):
    ema20 = Y.ema(df.close.to_numpy(), 20); o = df.open.to_numpy(); atr = f.atr.to_numpy()
    res = {}
    for fam, tr in trades_by_fam.items():
        t = tr.t.astype(int).to_numpy(); e = tr.e.astype(int).to_numpy()
        pot_atr = (ema20[t] - o[e]) / atr[t]; pot_R = (ema20[t] - o[e]) / tr.R.to_numpy()
        d = dict(n=int(len(tr)), pot_atr=dict(median=round(float(np.nanmedian(pot_atr)), 2), p25=round(float(np.nanpercentile(pot_atr, 25)), 2), p75=round(float(np.nanpercentile(pot_atr, 75)), 2)),
                 pot_R=dict(median=round(float(np.nanmedian(pot_R)), 2), p25=round(float(np.nanpercentile(pot_R, 25)), 2), p75=round(float(np.nanpercentile(pot_R, 75)), 2)),
                 r_net_all=round(float(tr.r_net.mean()), 3), win_all=round(float((tr.r_net > 0).mean()), 3))
        for name, x, grid in (("atr", pot_atr, (1.0, 1.5)), ("R", pot_R, (1.0, 1.5))):
            for q in grid:
                m = x >= q; sub = tr.r_net[m]
                d[f"{name}>={q}"] = dict(n=int(m.sum()), share=round(float(m.mean()), 3), r_net=round(float(sub.mean()), 3) if m.sum() else None, median=round(float(sub.median()), 3) if m.sum() else None, win=round(float((sub > 0).mean()), 3) if m.sum() else None,
                                          r_net_rest=round(float(tr.r_net[~m].mean()), 3) if (~m).sum() else None)
        # Kosten in R: K1 Rundlauf ~0.99 Prozent des Notionals
        cost_R = 0.0099 * tr.entry.to_numpy() / tr.R.to_numpy(); d["cost_R_median"] = round(float(np.median(cost_R)), 3)
        res[fam] = d
    return res
for coin in ("XRP", "DOT"):
    df = Y.load(_AR + f"/holdout/discovery/{coin}USDT_spot4h_discovery.csv"); C = R.cfg_alt(); f = R.features(df, C); P = "X" if coin == "XRP" else "D"
    fams = {f"{P}1": pd.read_csv(f"eval_{coin}/trades_{P}1_T0_E0_K1.csv"), f"{P}3": pd.read_csv(f"eval_{coin}/trades_{P}3_T0_E0_K1.csv")}
    out[coin] = analyse(coin, df, f, fams)
# BTC: Stufe-A-Kandidaten (Regressionsdatei), TA-Trigger wie Stufe A, Exit E0 neu simuliert (Development)
df = Y.load(_AR + "/yamato/data/BTCUSDT_4h_discovery.csv"); C = R.cfg_btc_stufeA(); f = R.features(df, C); lo, hi = Y.swings(df)
cy = pd.read_csv("regress/candidates_y1_y3_rlib.csv")
fams = {}
for kind, cand in (("Y1", cy[cy.y1]), ("Y3", cy[cy.y3])):
    for trig in ("TA", "T0"):
        tr, _ = R.run_sleeve(cand.sort_values("t"), df, f, lo, kind, trig, "E0", "K1", C); fams[f"{kind}_{trig}"] = tr
out["BTC"] = analyse("BTC", df, f, fams)
json.dump(out, open("dev_rebound/dev_rebound20.json", "w"), indent=1)
for coin, r in out.items():
    for fam, d in r.items():
        print(coin, fam, "n", d["n"], "pot_atr med", d["pot_atr"]["median"], "pot_R med", d["pot_R"]["median"], "cost_R", d["cost_R_median"], "E0 all", d["r_net_all"], d["win_all"])
        for k in ("atr>=1.0", "atr>=1.5", "R>=1.0", "R>=1.5"): print("    ", k, d[k])
