#!/usr/bin/env python3
"""Unabhaengige Nachpruefung des XS21-PiT-v1.0-Laufs aus den Lauf-Ausgaben und den Roh-ZIPs (eigene, einfache Implementierung,
importiert xs21_pit nicht). Prueft: Spec-SHA im Log, U2 Teilmenge U1, Auswahl = Top/Bottom-3 nach ret(21) am Schluss T unter den
Mitgliedern (nur Daten bis T), Brutto-Rendite und Kosten K1 aus unabhaengig rekonstruierten Gewichten, Bilanzidentitaet,
Anteil gefuelltes Funding."""
import csv, glob, io, json, os, sys, zipfile
import numpy as np, pandas as pd
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUN = os.path.join(REPO, "01_forschung/09_lane_c/xs21_pit_v1.0/run")
SPEC_SHA = "edb24cde8c391c60cd90fdad753f403a8835de7e4da275af0d5d3eed01e998af"
FEE, FRIC, FRIC_K2 = 0.0005, 0.0002, 0.0006


def zrows(p):
    t = zipfile.ZipFile(p).read(zipfile.ZipFile(p).namelist()[0]).decode()
    return [r for r in csv.reader(io.StringIO(t)) if r and r[0][:1].isdigit()]


def main():
    out = {}; ok = True
    meta = json.load(open(os.path.join(RUN, "xs21_run.log")))
    out["spec_sha_im_log"] = meta["spec_sha256"] == SPEC_SHA; ok &= out["spec_sha_im_log"]
    uni = pd.read_csv(os.path.join(RUN, "xs21_universen.csv")).fillna("")
    sub = all(set(r.U2.split()) <= set(r.U1.split()) for r in uni.itertuples() if r.n_U1 >= 20)
    out["U2_teilmenge_U1"] = sub; ok &= sub
    # Rohkurse
    O, C = {}, {}
    for p in glob.glob(os.path.join(REPO, "data/xs21/zips/*/klines/*/1d/*.zip")):
        s = p.split("/klines/")[1].split("/")[0]
        for r in zrows(p):
            d = pd.Timestamp(int(r[0]), unit="ms", tz="UTC").floor("D")
            O.setdefault(s, {})[d] = float(r[1]); C.setdefault(s, {})[d] = float(r[4])
    for nm, uk in (("U1_LS", "U1"), ("U2_LS", "U2")):
        sel = pd.read_csv(os.path.join(RUN, f"xs21_auswahl_{nm}.csv")).fillna("")
        members = {r.T: r._asdict()[uk].split() for r in uni.itertuples()}
        bad = 0
        for r in sel.itertuples():
            T = pd.Timestamp(r.T, tz="UTC"); T0 = T - pd.Timedelta(days=21)
            rets = {s: C[s][T] / C[s][T0] - 1 for s in members[r.T] if T in C.get(s, {}) and T0 in C.get(s, {})}
            lo = sorted([(-v, s) for s, v in rets.items() if v > 0])[:3]; sh = sorted([(v, s) for s, v in rets.items() if v < 0])[:3]
            exp_l = [s for _, s in lo]; exp_s = [s for _, s in sh]
            got_l = r.long.strip("[]").replace("'", "").replace(",", " ").split(); got_s = r.short.strip("[]").replace("'", "").replace(",", " ").split()
            if exp_l != got_l or exp_s != got_s: bad += 1
        out[f"{nm}_auswahl_abweichungen"] = bad; ok &= bad == 0 or bad <= 0
        comp = pd.read_csv(os.path.join(RUN, f"xs21_daily_components_{nm}_K1.csv"), index_col=0, parse_dates=True)
        recon = comp["gross"] + comp["funding"] + comp["cash"] - comp["cost"]
        out[f"{nm}_bilanz_maxabw"] = float((recon - comp["net"]).abs().max()); ok &= out[f"{nm}_bilanz_maxabw"] < 1e-12
        # Gewichte unabhaengig: je Stichtag 1/6 je Position ab T+1 fuer 7 Tage; Brutto aus Eroeffnungskursen
        days = comp.index
        Wd = {}
        for r in sel.itertuples():
            T = pd.Timestamp(r.T, tz="UTC")
            ls = r.long.strip("[]").replace("'", "").replace(",", " ").split(); ss = r.short.strip("[]").replace("'", "").replace(",", " ").split()
            for k in range(1, 8):
                d = T + pd.Timedelta(days=k)
                Wd[d] = {**{s: 0.5 / 3 for s in ls}, **{s: -0.5 / 3 for s in ss}}
        g = []; c = []; prev = {}
        for d in days:
            w = Wd.get(d, {}); gr = 0.0
            # Positionen nur solange Kerzen vorhanden (Delisting): Gewicht 0 nach letzter Kerze
            w = {s: v for s, v in w.items() if d in O[s]}
            for s, v in w.items():
                nx = [x for x in (d + pd.Timedelta(days=i) for i in range(1, 5)) if x in O[s]]
                gr += v * ((O[s][nx[0]] / O[s][d] - 1) if nx else (C[s][d] / O[s][d] - 1))
            tv = sum(abs(w.get(s, 0) - prev.get(s, 0)) for s in set(w) | set(prev))
            g.append(gr); c.append(tv * (FEE + FRIC)); prev = w
        g = pd.Series(g, index=days); c = pd.Series(c, index=days)
        out[f"{nm}_brutto_maxabw"] = float((g - comp["gross"]).abs().max())
        out[f"{nm}_brutto_summe"] = [float(g.sum()), float(comp["gross"].sum())]
        out[f"{nm}_kosten_summe_unabh_vs_lauf"] = [float(c.sum()), float(comp["cost"].sum())]
    ev = json.load(open(os.path.join(RUN, "xs21_eval.json")))
    for nm in ("U1_LS", "U2_LS"):
        out[f"{nm}_funding_gefuellt"] = ev["results"][nm]["scen"]["K1"]["fill"]
    out["gesamt_ok"] = bool(ok)
    json.dump(out, open(os.path.join(RUN, "xs21_check.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
