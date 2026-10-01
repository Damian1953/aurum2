#!/usr/bin/env python3
"""Baut die B7-Ausschlussliste (ENTWURF v0.1) fuer XS21 PiT v0.2 aus den Universumsdaten.
Eingaben (nur Symbollisten, keine Kurse/Renditen/Volumen):
  data/raw/binance_um_universe.csv (Lane-C-Loader v1, 1014 Symbole)
  01_forschung/09_lane_c/xs21_pit_v0.2/binance_um_snapshot_2026-10-01.csv (Collector, 1056 Symbole)
  01_forschung/09_lane_c/xs21_pit_v0.2/binance_spot_symbols_2026-10-01.json (data.binance.vision Spot-Listing, Gegenprobe)
Ausgabe: xs21_exclusions_v0.1.csv, xs21_unklar_v0.1.csv, *.sha256, Bericht auf stdout."""
import csv, hashlib, importlib.util, io, json, os, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(REPO, "01_forschung/09_lane_c/xs21_pit_v0.2")
spec = importlib.util.spec_from_file_location("m", os.path.join(REPO, "tools/xs21/exclusion_map_v0.1.py")); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)

def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

src = {"lane_c_universe": os.path.join(REPO, "data/raw/binance_um_universe.csv"), "snapshot": os.path.join(D, "binance_um_snapshot_2026-10-01.csv"),
       "spot": os.path.join(D, "binance_spot_symbols_2026-10-01.json")}
uni = {r["symbol"]: r for r in csv.DictReader(open(src["lane_c_universe"]))}
snap = {r["symbol"]: r for r in csv.DictReader(open(src["snapshot"]))}
spot = set(json.load(open(src["spot"])))
usdt = sorted(s for s in set(uni) | set(snap) if s.endswith("USDT") and "_" not in s and "SETTLED" not in s and s.isascii())
base = {s[:-4]: s for s in usdt}
fails = []
for b in list(M.EXCL) + M.UNKLAR + list(M.KEEP_NOTE):
    if b not in base:
        fails.append(f"{b}USDT nicht im USDT-Perp-Universum")
dups = set(M.EXCL) & set(M.UNKLAR)
if dups: fails.append(f"doppelt: {dups}")
rows = []
for b, (cat, conf, why) in sorted(M.EXCL.items()):
    s = b + "USDT"
    rows.append(dict(symbol=s, base=b, kategorie=cat, sicherheit=conf, grund=why,
                     first_month=uni.get(s, {}).get("first_month", "nach 2026-08 (nur Snapshot)"),
                     binance_spot_usdt=("ja" if s in spot else "nein")))
warn = [r["symbol"] for r in rows if r["binance_spot_usdt"] == "ja"]
out = os.path.join(D, "xs21_exclusions_v0.1.csv")
buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=list(rows[0]), lineterminator="\n"); w.writeheader(); w.writerows(rows)
open(out, "w").write(buf.getvalue())
un = [dict(symbol=b + "USDT", first_month=uni.get(b + "USDT", {}).get("first_month", "nach 2026-08 (nur Snapshot)"),
           binance_spot_usdt=("ja" if b + "USDT" in spot else "nein"), status="vorlaeufig NICHT ausgeschlossen, vor Freeze klaeren") for b in sorted(M.UNKLAR)]
out2 = os.path.join(D, "xs21_unklar_v0.1.csv")
buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=list(un[0]), lineterminator="\n"); w.writeheader(); w.writerows(un)
open(out2, "w").write(buf.getvalue())
with open(os.path.join(D, "xs21_exclusions_v0.1.sha256"), "w") as fh:
    for p in (out, out2, os.path.join(REPO, "tools/xs21/exclusion_map_v0.1.py"), src["snapshot"], src["spot"]):
        fh.write(f"{sha(p)}  {os.path.relpath(p, REPO)}\n")
    fh.write(f"{sha(src['lane_c_universe'])}  02_daten/raw/binance_um_universe.csv\n")
from collections import Counter
print("USDT-Perps (ASCII, ohne Termin/SETTLED):", len(usdt))
print("Ausschluesse:", len(rows), dict(Counter(r["kategorie"] for r in rows)), dict(Counter(r["sicherheit"] for r in rows)))
print("davon first_month <= 2025-12:", [r["symbol"] for r in rows if r["first_month"] <= "2025-12"])
print("Unklar:", len(un), "davon mit Binance-Spot-USDT-Paar (Hinweis Krypto):", [u["symbol"] for u in un if u["binance_spot_usdt"] == "ja"])
print("WARNUNG Ausschluss mit Spot-Paar:", warn)
print("FEHLER:", fails)
sys.exit(1 if fails else 0)
