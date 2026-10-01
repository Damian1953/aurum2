#!/usr/bin/env python3
"""Nachtrag nach dem Lauf (01.10.2026, deskriptiv, kein zweiter Lauf): Survivorship-Zerlegung je Block (Spec §5.3 verlangt
Stand 2026-09-14 auch je Block; der Lauf-Code gibt nur den Gesamtzeitraum aus). Liest nur Lauf-Ausgaben und Roh-Kerzen.
Status: ueberlebend = Kerze mit count > 0 (U5a) am Datenende 2026-09-15. Trade-Summen (pnl_net K1) nach Einstiegsblock.
Zusatz: deskriptive Kennzahlen ohne 2026 und Jahres-Summen Tagesbeitraege vs. Trades (Konvention U9)."""
import csv, glob, io, json, os, zipfile
import numpy as np, pandas as pd
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUN = os.path.join(REPO, "01_forschung/09_lane_c/xs21_pit_v1.0/run")
END = pd.Timestamp("2026-09-15", tz="UTC")
BL = [("B1", "2020-01-01", "2021-12-31"), ("B2", "2022-01-01", "2023-12-31"), ("B3", "2024-01-01", "2026-09-14")]


def alive(sym):
    for p in glob.glob(os.path.join(REPO, f"data/xs21/zips/daily/klines/{sym}/1d/*2026-09-15.zip")):
        z = zipfile.ZipFile(p)
        for r in csv.reader(io.StringIO(z.read(z.namelist()[0]).decode())):
            if r and r[0][:1].isdigit() and int(r[8]) > 0:
                return True
    return False


def main():
    out = {}
    cache = {}
    for nm in ("U1_LS", "U2_LS"):
        t = pd.read_csv(os.path.join(RUN, f"xs21_trades_{nm}.csv"), parse_dates=["entry_date"])
        t["alive"] = [cache.setdefault(s, alive(s)) for s in t.sym]
        res = {"gesamt": {}}
        for k, g in t.groupby("alive"):
            res["gesamt"]["survivors" if k else "delisted"] = {"n_trades": int(len(g)), "sum_trades": float(g.pnl_net.sum()), "expectancy": float(g.pnl_net.mean())}
        for b, a, e in BL:
            m = (t.entry_date >= pd.Timestamp(a, tz="UTC")) & (t.entry_date <= pd.Timestamp(e, tz="UTC"))
            res[b] = {}
            for k, g in t[m].groupby("alive"):
                res[b]["survivors" if k else "delisted"] = {"n_trades": int(len(g)), "sum_trades": float(g.pnl_net.sum()), "expectancy": float(g.pnl_net.mean())}
        c = pd.read_csv(os.path.join(RUN, f"xs21_daily_components_{nm}_K1.csv"), index_col=0, parse_dates=True)
        x = c.net[c.index < pd.Timestamp("2026-01-01", tz="UTC")]
        eq = (1 + x).cumprod(); yrs = len(x) / 365
        res["ohne_2026"] = {"cagr": float(eq.iloc[-1] ** (1 / yrs) - 1), "sharpe": float(x.mean() / x.std() * np.sqrt(365)),
                            "maxdd": float((eq / eq.cummax() - 1).min()), "bis": str(x.index[-1].date())}
        tt = pd.read_csv(os.path.join(RUN, f"xs21_trades_{nm}.csv"), parse_dates=["exit_date"])
        res["jahr_tagesbeitraege_vs_trades"] = {str(y): [float(c.net[c.index.year == y].sum()), float(tt.pnl_net[tt.exit_date.dt.year == y].sum())] for y in sorted(set(c.index.year))}
        out[nm] = res
    json.dump(out, open(os.path.join(RUN, "xs21_nachtrag_survivorship_bloecke.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
