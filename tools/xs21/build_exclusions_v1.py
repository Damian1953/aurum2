#!/usr/bin/env python3
"""Baut die B7-Listen v1.0 (FREEZE-KANDIDAT) nach Regel M1/M2 aus Symbollisten. Keine Kurse/Renditen/Volumen."""
import csv, hashlib, importlib.util, io, json, os, sys
from collections import Counter
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IN = os.path.join(REPO, "01_forschung/09_lane_c/xs21_pit_v0.2")
OUT = os.path.join(REPO, "01_forschung/09_lane_c/xs21_pit_v1.0"); os.makedirs(OUT, exist_ok=True)
spec = importlib.util.spec_from_file_location("m", os.path.join(REPO, "tools/xs21/exclusion_map_v1.0.py")); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
src = {"uni": os.path.join(REPO, "data/raw/binance_um_universe.csv"), "snap": os.path.join(IN, "binance_um_snapshot_2026-10-01.csv"),
       "spot": os.path.join(IN, "binance_spot_symbols_2026-10-01.json")}
uni = {r["symbol"]: r for r in csv.DictReader(open(src["uni"]))}
snap = {r["symbol"]: r for r in csv.DictReader(open(src["snap"]))}
spot = set(json.load(open(src["spot"])))
usdt = sorted(s for s in set(uni) | set(snap) if s.endswith("USDT") and "_" not in s and "SETTLED" not in s and s.isascii())
fails = [f"{b}USDT nicht im Universum" for b in M.M if b + "USDT" not in usdt]
def fm(s): return uni.get(s, {}).get("first_month", "nach 2026-08 (nur Snapshot)")
rows = []
for b, d in sorted(M.M.items()):
    s = b + "USDT"; ok = d["typ"] in M.ZULASSEN_TYP
    if d["sicherheit"] == "auffang" and s not in spot:
        fails.append(f"{s}: Auffang ohne Spot-Paar")
    rows.append(dict(symbol=s, entscheid="zugelassen" if ok else "ausgeschlossen", typ=d["typ"], sicherheit=d["sicherheit"], grund=d["grund"],
                     quelle=d["quelle"], pruefdatum="2026-10-01", first_month=fm(s), binance_spot_usdt="ja" if s in spot else "nein",
                     sensitivitaet_ohne=("ja" if ok and d["sicherheit"] in ("wahrscheinlich", "auffang") else "nein")))
# USTC-Pruefung: Listing nach Entkopplung Mai 2022
assert fm("USTCUSDT") > "2022-05", fm("USTCUSDT")
def write(name, rs):
    p = os.path.join(OUT, name); buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=list(rs[0]), lineterminator="\n"); w.writeheader(); w.writerows(rs)
    open(p, "w").write(buf.getvalue()); return p
p1 = write("xs21_b7_klassifikation_v1.0.csv", rows)
p2 = write("xs21_exclusions_v1.0.csv", [r for r in rows if r["entscheid"] == "ausgeschlossen"])
p3 = write("xs21_sensitivitaet_ohne_v1.0.csv", [r for r in rows if r["sensitivitaet_ohne"] == "ja"])
offen = [r for r in rows if r["entscheid"] == "ausgeschlossen" and r["sicherheit"] == "wahrscheinlich"]
with open(os.path.join(OUT, "xs21_b7_v1.0.sha256"), "w") as fh:
    for p in (p1, p2, p3, os.path.join(REPO, "tools/xs21/exclusion_map_v1.0.py"), os.path.join(REPO, "tools/xs21/build_exclusions_v1.py"), src["snap"], src["spot"]):
        fh.write(f"{sha(p)}  {os.path.relpath(p, REPO)}\n")
    fh.write(f"{sha(src['uni'])}  02_daten/raw/binance_um_universe.csv\n")
ex = [r for r in rows if r["entscheid"] == "ausgeschlossen"]; zu = [r for r in rows if r["entscheid"] == "zugelassen"]
print("USDT-Perps (ASCII, ohne Termin/SETTLED):", len(usdt), "| klassifizierte Sonderfaelle:", len(rows))
print("ausgeschlossen:", len(ex), dict(Counter(r["typ"] for r in ex)), dict(Counter(r["sicherheit"] for r in ex)))
print("zugelassen (geprueft):", len(zu), dict(Counter(r["sicherheit"] for r in zu)))
print("Sensitivitaet ohne:", [r["symbol"] for r in rows if r["sensitivitaet_ohne"] == "ja"])
print("Ausschluesse mit first_month <= 2023-12:", [(r["symbol"], r["first_month"]) for r in ex if r["first_month"] <= "2023-12"])
print("Ausschluesse first_month 2024-01..2025-12:", [(r["symbol"], r["first_month"]) for r in ex if "2024-01" <= r["first_month"] <= "2025-12"])
print("Ausschluss 'wahrscheinlich' (Ankuendigung nicht einzeln abgerufen):", len(offen))
print("FEHLER:", fails); sys.exit(1 if fails else 0)
