#!/usr/bin/env python3
"""
Project Aurum II — 1h-Kerzen fuer Entry-Bestaetigung (Trigger T1h) und Kerzengrenzen-Diagnose (+1h, +2h).

Baut auf nachladen_4h.py auf (gleiche Pruefungen, gleiche Gegenproben) und laedt fuer alle zehn Coins:
  1. Binance Vision Spot 1h, alle Spalten           -> raw/binance_full/<SYM>USDT_1h.csv
  2. Binance Vision Perp 1h, alle Spalten           -> raw/binance_perp_full/<SYM>USDT_1h.csv
  3. Kraken 60-Minuten-Kerzen aus dem Archiv 2026Q2 -> raw/kraken_archiv/<PAIR>_60.csv (roh), raw/kraken_1h/<COIN>USD_1h.csv
  4. Kraken REST OHLC interval=60 (letzte 720 Kerzen = 30 Tage) -> raw/kraken_api/<COIN>USD_1h.csv, Zusammenfuehrung
     raw/kraken_merged/<COIN>USD_1h.csv. Hinweis: Zwischen Archivende (30.06.2026) und API-Beginn bleibt bei 1h eine
     bekannte Luecke, die erst das Kraken-Archiv 2026Q3 schliesst. Sie wird in provenance_1h.json ausgewiesen.

Gegenprobe: 1h auf 4h aggregiert (nur vollstaendige Vierergruppen) gegen die vorhandenen 4h-Vollspalten-Kerzen.
Schreibt raw/provenance_1h.json und raw/nachladen_1h.log. Nichts Vorhandenes wird ueberschrieben.

Aufruf: python3 nachladen_1h.py [--coins XRP,DOT] [--nur-binance | --nur-kraken]
"""
import datetime as dt
import json
import os
import re
import sys
import time
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nachladen_historie as NH
import nachladen_4h as M

HERE = M.HERE
M.PROVENANCE = os.path.join(M.RAW, "provenance_1h.json")
M.LOGFILE = os.path.join(M.RAW, "nachladen_1h.log")
DIR_K1 = os.path.join(M.RAW, "kraken_1h")
log = M.log

# 1h-Raster: jede volle Stunde
_bar_seconds_orig = M.bar_seconds
M.bar_seconds = lambda interval: 3600 if interval == "1h" else _bar_seconds_orig(interval)
_validate_orig = M.validate_bars


def validate_bars(rows, interval, label, has_taker=True):
    ok, crit, warn, gaps = _validate_orig(rows, interval, label, has_taker)
    if interval == "1h":
        for i, r in enumerate(rows):
            t = M.parse_iso(r["t"])
            if t.minute or t.second:
                crit.append(f"Zeile {i}: 1h-Kerze ausserhalb Raster {r['t']}")
        ok = len(crit) == 0
    return ok, crit, warn, gaps


M.validate_bars = validate_bars

# Binance hat nach Wartungen einzelne 1h-Kerzen ausserhalb des Stundenrasters publiziert (z. B. 2018-02-09, Beginn hh:28:14).
# Solche Kerzen werden nicht geschrieben, sondern als Quarantaene protokolliert; die fehlenden Stunden erscheinen als Luecke.
OFF_GRID = []
_parse_orig = M.parse_binance_full


def parse_binance_full_1h(blob):
    rows = _parse_orig(blob)
    keep = []
    for r in rows:
        t = M.parse_iso(r["t"])
        if t.minute or t.second:
            OFF_GRID.append(r["t"])
        else:
            keep.append(r)
    return keep


M.parse_binance_full = parse_binance_full_1h


def crosscheck_1h_vs_4h(sym, market, rows_1h, entry):
    """1h auf 4h aggregiert (vollstaendige Vierergruppen ab 00/04/08...) gegen die 4h-Vollspalten-Datei."""
    d4 = os.path.join(M.DIR_SPOT_FULL if market == "spot" else M.DIR_PERP_FULL, f"{sym}_4h.csv")
    ref = {r["t"]: r for r in M.read_csv(d4)}
    if not ref:
        entry["crosscheck_1h_aggregated_vs_4h"] = "keine 4h-Datei"; return
    groups = {}
    for r in rows_1h:
        t = M.parse_iso(r["t"])
        key = t.replace(hour=(t.hour // 4) * 4).strftime("%Y-%m-%dT%H:%M:%SZ")
        groups.setdefault(key, []).append(r)
    n, bad = 0, []
    tol = lambda a, b: abs(a - b) > 1e-6 * max(1.0, abs(b))
    for key, bars in groups.items():
        if len(bars) != 4 or key not in ref:
            continue
        n += 1
        o = float(bars[0]["open"]); c = float(bars[-1]["close"])
        h = max(float(b["high"]) for b in bars); l = min(float(b["low"]) for b in bars)
        v = sum(float(b["volume"]) for b in bars)
        x = ref[key]
        if tol(o, float(x["open"])) or tol(c, float(x["close"])) or tol(h, float(x["high"])) or tol(l, float(x["low"])) or tol(v, float(x["volume"])):
            bad.append(key)
    entry["crosscheck_1h_aggregated_vs_4h"] = {"complete_4h_bars": n, "mismatch": len(bad), "examples": bad[:10]}
    log(f"  Gegenprobe {market} {sym} 1h->4h: {n} vollstaendige 4h-Kerzen, {len(bad)} Abweichungen")


def run_binance(coins):
    for coin in coins:
        sym = f"{coin}USDT"
        for market in ("spot", "perp"):
            OFF_GRID.clear()
            r = M.binance_full(sym, market, "1h")
            if r:
                path, rows, entry = r
                if OFF_GRID:
                    entry["off_grid_dropped"] = {"count": len(OFF_GRID), "first": OFF_GRID[0], "last": OFF_GRID[-1]}
                    log(f"  Quarantaene {market} {sym} 1h: {len(OFF_GRID)} Kerzen ausserhalb Raster verworfen ({OFF_GRID[0]} bis {OFF_GRID[-1]})")
                crosscheck_1h_vs_4h(sym, market, rows, entry)
                M.prov_update(f"binance_{market}_{sym}_1h", entry)


def run_kraken_archive(coins):
    z = M.kraken_zip_path()
    if z is None:
        log(f"Kraken-Archiv nicht gefunden in {M.DIR_KA_DL}. Schritt uebersprungen."); return {}
    log(f"Kraken-Archiv: {z} ({os.path.getsize(z) / 1e9:.2f} GB)")
    zf = zipfile.ZipFile(z); names = zf.namelist(); out = {}
    for coin in coins:
        pair = M.KRAKEN_PAIRS[coin]
        m = [n for n in names if re.search(rf"(^|/){pair}_60\.csv$", n)]
        if not m:
            log(f"  FEHLT im Archiv: {pair}_60.csv"); continue
        raw_dst = os.path.join(M.DIR_KA, f"{pair}_60.csv")
        os.makedirs(M.DIR_KA, exist_ok=True)
        with zf.open(m[0]) as src, open(raw_dst + ".tmp", "wb") as dst:
            dst.write(src.read())
        os.replace(raw_dst + ".tmp", raw_dst)
        rows = M.kraken_convert(raw_dst, coin)
        ok, crit, warn, gaps = validate_bars(rows, "1h", f"kraken {pair} 60", has_taker=False)
        for c in crit[:10]:
            log(f"  KRITISCH kraken {pair}: {c}")
        if not ok:
            log(f"  kraken {pair}: nicht geschrieben ({len(crit)} kritische Befunde)"); continue
        path = os.path.join(DIR_K1, f"{coin}USD_1h.csv")
        M.write_csv(path, rows, M.KRAKEN_COLUMNS)
        M.prov_update(f"kraken_archiv_{coin}_1h", {
            "file": os.path.relpath(path, HERE), "raw_file": os.path.relpath(raw_dst, HERE), "archive": M.ZIPNAME,
            "archive_member": m[0], "pair": pair, "interval": "60min", "rows": len(rows), "first": rows[0]["t"],
            "last": rows[-1]["t"], "gaps": len(gaps), "gap_list": gaps[:30],
            "largest_gap_bars": max([g[2] for g in gaps], default=0),
            "sha256_raw": NH.sha256_of(raw_dst), "sha256": NH.sha256_of(path)})
        log(f"  OK kraken {pair} 60: {len(rows)} Kerzen {rows[0]['t']} bis {rows[-1]['t']}, Luecken {len(gaps)}")
        out[coin] = rows
    return out


def run_kraken_api(coins, archive_rows):
    os.makedirs(M.DIR_KAPI, exist_ok=True); os.makedirs(M.DIR_KMERGED, exist_ok=True)
    for coin in coins:
        pair = M.KRAKEN_PAIRS[coin]
        raw = NH.fetch(f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval=60")
        time.sleep(1.1)
        if raw is None:
            log(f"  API {pair}: nicht gefunden"); continue
        js = json.loads(raw)
        if js.get("error"):
            log(f"  API-Fehler {pair}: {js['error']}"); continue
        key = [k for k in js["result"] if k != "last"][0]
        rows = [{"t": M.iso(int(r[0]) * 1000), "open": r[1], "high": r[2], "low": r[3], "close": r[4],
                 "volume": r[6], "trades": r[7]} for r in js["result"][key]][:-1]
        api_path = os.path.join(M.DIR_KAPI, f"{coin}USD_1h.csv")
        by_t = {r["t"]: r for r in M.read_csv(api_path)}
        for r in rows:
            by_t[r["t"]] = r
        api_rows = [by_t[k] for k in sorted(by_t)]
        M.write_csv(api_path, api_rows, M.KRAKEN_COLUMNS)
        M.prov_update(f"kraken_api_{coin}_1h", {"file": os.path.relpath(api_path, HERE), "source": "kraken REST OHLC interval=60",
                                                "pair_key": key, "rows": len(api_rows), "first": api_rows[0]["t"],
                                                "last": api_rows[-1]["t"], "sha256": NH.sha256_of(api_path)})
        log(f"  API {pair} 60: {len(api_rows)} Kerzen {api_rows[0]['t']} bis {api_rows[-1]['t']}")
        arch = archive_rows.get(coin) or M.read_csv(os.path.join(DIR_K1, f"{coin}USD_1h.csv"))
        if not arch:
            continue
        arch_last = arch[-1]["t"]
        merged = list(arch) + [r for r in api_rows if r["t"] > arch_last]
        ok, crit, warn, gaps = validate_bars(merged, "1h", f"kraken merged {pair}", has_taker=False)
        if not ok:
            for c in crit[:10]:
                log(f"  KRITISCH merged {pair}: {c}")
            continue
        mpath = os.path.join(M.DIR_KMERGED, f"{coin}USD_1h.csv")
        M.write_csv(mpath, merged, M.KRAKEN_COLUMNS)
        seam = [g for g in gaps if g[0] == arch_last]
        seam_bars = seam[0][2] if seam else 0
        M.prov_update(f"kraken_merged_{coin}_1h", {
            "file": os.path.relpath(mpath, HERE), "seam_archive_last": arch_last, "api_first": api_rows[0]["t"],
            "seam_gap_bars": seam_bars, "seam_gap_note": "Luecke zwischen Archiv 2026Q2 und API (720 Kerzen), schliesst das Archiv 2026Q3" if seam_bars else "",
            "rows": len(merged), "first": merged[0]["t"], "last": merged[-1]["t"], "gaps": len(gaps), "sha256": NH.sha256_of(mpath)})
        log(f"  merged {pair}: {len(merged)} Kerzen bis {merged[-1]['t']}, Naht nach {arch_last}, Nahtluecke {seam_bars} Kerzen")


def main(argv):
    coins = M.COINS
    if "--coins" in argv:
        coins = [c.strip().upper() for c in argv[argv.index("--coins") + 1].split(",")]
        bad = [c for c in coins if c not in M.COINS]
        if bad:
            print(f"Unbekannte Coins: {bad}"); return 2
    log(f"Start nachladen_1h, Coins {coins}, Python {sys.version.split()[0]}")
    if "--nur-kraken" not in argv:
        log("Schritt 1 und 2: Binance Vision Spot und Perp 1h, alle Spalten")
        run_binance(coins)
    if "--nur-binance" not in argv:
        log("Schritt 3: Kraken 60 Minuten aus dem Archiv")
        arch = run_kraken_archive(coins)
        log("Schritt 4: Kraken API 60 Minuten und Zusammenfuehrung")
        run_kraken_api(coins, arch)
    log(f"Fertig. Herkunft in {os.path.relpath(M.PROVENANCE, HERE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
