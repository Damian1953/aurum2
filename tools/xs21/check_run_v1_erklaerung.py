#!/usr/bin/env python3
"""Nachtrag 01.10.2026 nach dem Lauf: erklaert die von tools/xs21/check_run_v1.py (eingefroren, unveraendert) gemeldeten
Abweichungen. (1) Auswahl: das Pruefskript wendet U5a (Kerzen mit count=0 gelten als nicht vorhanden) nicht an; mit U5a
muessen alle Auswahlen uebereinstimmen. (2) Kosten: Differenz = Anzahl Delisting-Ausstiege x 1/6 x (0.0006 - 0.0002)."""
import csv, glob, io, json, os, zipfile
import pandas as pd
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUN = os.path.join(REPO, "01_forschung/09_lane_c/xs21_pit_v1.0/run")


def zrows(p):
    z = zipfile.ZipFile(p); t = z.read(z.namelist()[0]).decode()
    return [r for r in csv.reader(io.StringIO(t)) if r and r[0][:1].isdigit()]


def pick(x):
    return ([s for _, s in sorted((-v, s) for s, v in x.items() if v > 0)[:3]], [s for _, s in sorted((v, s) for s, v in x.items() if v < 0)[:3]])


def main():
    C, N = {}, {}
    for p in glob.glob(os.path.join(REPO, "data/xs21/zips/*/klines/*/1d/*.zip")):
        s = p.split("/klines/")[1].split("/")[0]
        for r in zrows(p):
            d = pd.Timestamp(int(r[0]), unit="ms", tz="UTC").floor("D"); C.setdefault(s, {})[d] = float(r[4]); N.setdefault(s, {})[d] = int(r[8])
    uni = pd.read_csv(os.path.join(RUN, "xs21_universen.csv")).fillna("")
    chk = json.load(open(os.path.join(RUN, "xs21_check.json")))
    out = {}
    for nm, uk in (("U1_LS", "U1"), ("U2_LS", "U2")):
        sel = pd.read_csv(os.path.join(RUN, f"xs21_auswahl_{nm}.csv")).fillna("")
        mem = {r.T: r._asdict()[uk].split() for r in uni.itertuples()}
        ohne = mit = 0
        for r in sel.itertuples():
            T = pd.Timestamp(r.T, tz="UTC"); T0 = T - pd.Timedelta(days=21)
            got = (r.long.strip("[]").replace("'", "").replace(",", " ").split(), r.short.strip("[]").replace("'", "").replace(",", " ").split())
            a = {s: C[s][T] / C[s][T0] - 1 for s in mem[r.T] if T in C.get(s, {}) and T0 in C.get(s, {})}
            b = {s: v for s, v in a.items() if N[s][T] > 0 and N[s][T0] > 0}
            ohne += pick(a) != tuple(got); mit += pick(b) != tuple(got)
        t = pd.read_csv(os.path.join(RUN, f"xs21_trades_{nm}.csv"))
        nd = int(t.delist_exit.sum()); ku, kl = chk[f"{nm}_kosten_summe_unabh_vs_lauf"]
        out[nm] = {"auswahl_abw_ohne_U5a": ohne, "auswahl_abw_mit_U5a": mit, "n_delisting_ausstiege": nd,
                   "kostendiff_lauf_minus_unabh": kl - ku, "erwartet_delisting": nd * (0.5 / 3) * (0.0006 - 0.0002),
                   "kosten_erklaert": abs((kl - ku) - nd * (0.5 / 3) * 0.0004) < 1e-9}
    out["alles_erklaert"] = all(out[n]["auswahl_abw_mit_U5a"] == 0 and out[n]["kosten_erklaert"] for n in ("U1_LS", "U2_LS"))
    json.dump(out, open(os.path.join(RUN, "xs21_check_erklaerung.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
