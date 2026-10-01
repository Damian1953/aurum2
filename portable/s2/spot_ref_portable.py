# PORTABLE VERSION, generiert von tools/make_portable.py. NICHT VON HAND AENDERN.
# Quelle (eingefroren): 01_forschung/02_strategien/spot_ref.py  sha256 9231d0805268edadf9b6905ca4c7b85e26a796427c6f05413ef4c52cff3541c2
# Regeln: cost:SPOT=stage2_spot_ref. Arbeitsbereich: AURUM_ROOT (Default: Ordner '..' relativ zu dieser Datei).
import os as _aos; _AR = _aos.environ.get("AURUM_ROOT") or _aos.path.abspath(_aos.path.join(_aos.path.dirname(_aos.path.abspath(__file__)), ".."))
try:
    import aurum_costs as _ac
except ImportError:
    import sys as _asys; _asys.path.append(_aos.path.join(_AR, "pylib")); import aurum_costs as _ac
#!/usr/bin/env python3
"""
Spot-Referenz fuer die Long-only-Varianten der Familie A (Vorregistrierung Abschnitt 12, «Bericht, kein Kriterium»):
gleiche Gewichte wie im Perp-Lauf, Kostenmodell Kraken Spot Tier 1 Maker 0.40 je Seite plus 0.02 Reibung, kein Funding.
Aufruf: python3 spot_ref.py out_full  -> haengt Abschnitt 10 an stage2_report.md an und schreibt spot_reference.json
"""
import sys, os, json, math
import numpy as np, pandas as pd
import s2lib as L
from stage2 import VARIANTS, sim_all, pooled

out_dir = sys.argv[1]
coins = L.COINS
tb = L.load_tbill()
data = {c: L.CoinData(c, tb) for c in coins}
inds = {c: L.indicators(data[c].spot) for c in coins}
SPOT = _ac.load("stage2_spot_ref")  # zentral: config/cost_model_v1.json [stage2_spot_ref]
rows = []; store = {}
for V in [v for v in VARIANTS if v["family"] == "A"]:
    p = V["params"]; sims = {}
    for c in coins:
        cd = data[c]; ind = inds[c]
        if p["mode"] == "cross":
            w, tr = L.run_trend(cd, ind, side=+1, mode="cross", sma_n=p["sma_n"]); need = [f"sma{p['sma_n']}", "atr"]
        else:
            w, tr = L.run_trend(cd, ind, side=+1, mode="breakout", N=p["N"], k=p["k"], gate=p["gate"], sma_n=p["sma_n"], pyramid=p["pyramid"]); need = [f"sma{p['sma_n']}", "atr", f"hh{p['N']}"]
        m = ind[need].notna().all(axis=1); active = m.idxmax() if m.any() else None
        # Spot: kein Funding -> fund_day auf null setzen
        cd_spot = cd
        fd_backup = cd_spot.fund_day
        cd_spot.fund_day = pd.Series(0.0, index=cd.idx)
        s = L.simulate(cd_spot, w, SPOT)
        cd_spot.fund_day = fd_backup
        if active is not None:
            s.loc[s.index < active, ["gross", "net", "cost", "funding", "cash"]] = np.nan
        sims[c] = s
    pool = pooled(sims)
    eq = L.equity_stats(pool["net"], data["BTC"].cash_daily)
    store[V["id"]] = eq
    rows.append((V["id"], eq))

res = json.load(open(os.path.join(out_dir, "stage2_results.json")))
lines = ["", "## 10. Spot-Referenz Familie A Long-only (Bericht, kein Kriterium)", "",
         "Gleiche Gewichte wie im Perp-Lauf, Kostenmodell Kraken Spot Tier 1 Maker 0.40 je Seite plus 0.02 Reibung, kein Funding, Cash zum T-Bill-Satz. Gegenueberstellung mit K1 Perp (0.05 plus 0.02 je Seite, tatsaechliches Funding). Die Differenz ist im Wesentlichen das auf Long-Perps gezahlte Funding abzueglich der hoeheren Spot-Gebuehr.", "",
         "| Variante | Spot CAGR | Spot Sharpe | Spot MaxDD | Spot Calmar | K1 Perp CAGR | K1 Perp Sharpe | K1 Perp MaxDD | Differenz CAGR |", "|---|---|---|---|---|---|---|---|---|"]
for vid, eq in rows:
    k1 = res["results"][f"{vid}|L"]["scenarios"]["K1"]["pooled"]["equity"]
    lines.append(f"| {vid} | {eq['cagr']*100:.1f} % | {eq['sharpe']:.2f} | {eq['maxdd']*100:.1f} % | {eq['calmar']:.2f} | {k1['cagr']*100:.1f} % | {k1['sharpe']:.2f} | {k1['maxdd']*100:.1f} % | {(eq['cagr']-k1['cagr'])*100:+.1f} Pp |")
lines.append("")
with open(os.path.join(out_dir, "stage2_report.md"), "a") as fh:
    fh.write("\n".join(lines))
json.dump(store, open(os.path.join(out_dir, "spot_reference.json"), "w"), indent=1, default=float)
print("\n".join(lines))
