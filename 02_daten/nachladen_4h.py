#!/usr/bin/env python3
"""
Project Aurum II — 04_xrp_specialist / 05_dot_specialist: Datennachladen 4h und Vollspalten.

Laedt fuer alle zehn Coins des Universums:
  1. Binance Vision Spot   Klines 4h und 1d mit allen Spalten (Quote-Volumen, Anzahl Trades, Taker-Buy-Volumen)
  2. Binance Vision Perp   Klines 4h und 1d mit allen Spalten (USDT-M Perpetual)
  3. Kraken 240-Minuten-Kerzen aus dem bereits geladenen Archiv Kraken_OHLCVT_Full_2026Q2.zip
     (liegt in raw/kraken_archiv/_download/, wird bei Bedarf aus den fuenf Teilen zusammengesetzt)
  4. Kraken REST OHLC interval=240 (letzte 720 Kerzen = 120 Tage) als Ergaenzung nach dem Archivende
     und Zusammenfuehrung Archiv + API mit dokumentierter Naht

Prueft jede Reihe: Zeitraster (4h-Kerzen beginnen 00/04/08/12/16/20 UTC), Monotonie, Luecken,
OHLC-Konsistenz, Taker-Buy <= Volumen. Gegenproben: Vollspalten-Tageskerzen gegen die vorhandenen
OHLCV-Tageskerzen (raw/binance, raw/binance_perp), 4h auf Tag aggregiert gegen Tageskerzen.
Schreibt raw/provenance_4h.json mit SHA-256 je Datei. Nichts wird geloescht oder ueberschrieben,
ausser die eigenen Ausgabedateien (atomar).

Ausgaben:
  raw/binance_full/<SYM>USDT_4h.csv, _1d.csv        raw/binance_perp_full/<SYM>USDT_4h.csv, _1d.csv
  raw/kraken_archiv/<PAIR>_240.csv (roh)             raw/kraken_4h/<COIN>USD_4h.csv (konvertiert)
  raw/kraken_api/<COIN>USD_4h.csv                    raw/kraken_merged/<COIN>USD_4h.csv
  raw/provenance_4h.json                             raw/nachladen_4h.log

Aufruf: python3 nachladen_4h.py [--coins XRP,DOT] [--nur-binance | --nur-kraken]
Wiederaufnahme: vorhandene Ausgabedateien werden ab dem letzten Monat ergaenzt.
"""
import csv
import datetime as dt
import io
import json
import os
import re
import sys
import time
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nachladen_historie as NH  # ssl_context, fetch, sha256_of, month_iter, USER_AGENT

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
DIR_SPOT_FULL = os.path.join(RAW, "binance_full")
DIR_PERP_FULL = os.path.join(RAW, "binance_perp_full")
DIR_SPOT_OLD = os.path.join(RAW, "binance")
DIR_PERP_OLD = os.path.join(RAW, "binance_perp")
DIR_KA = os.path.join(RAW, "kraken_archiv")
DIR_KA_DL = os.path.join(DIR_KA, "_download")
DIR_K4 = os.path.join(RAW, "kraken_4h")
DIR_KAPI = os.path.join(RAW, "kraken_api")
DIR_KMERGED = os.path.join(RAW, "kraken_merged")
PROVENANCE = os.path.join(RAW, "provenance_4h.json")
LOGFILE = os.path.join(RAW, "nachladen_4h.log")

COINS = ["BTC", "ETH", "SOL", "XRP", "ADA", "AVAX", "LINK", "DOT", "BNB", "LTC"]
KRAKEN_PAIRS = {"BTC": "XBTUSD", "ETH": "ETHUSD", "SOL": "SOLUSD", "XRP": "XRPUSD", "ADA": "ADAUSD",
                "AVAX": "AVAXUSD", "LINK": "LINKUSD", "DOT": "DOTUSD", "BNB": "BNBUSD", "LTC": "LTCUSD"}
SPOT_START = (2017, 8)
PERP_START = (2019, 9)
PAUSE = 0.10
ZIPNAME = "Kraken_OHLCVT_Full_2026Q2.zip"

FULL_COLUMNS = ["t", "open", "high", "low", "close", "volume", "close_time",
                "quote_volume", "trades", "taker_buy_base", "taker_buy_quote"]
KRAKEN_COLUMNS = ["t", "open", "high", "low", "close", "volume", "trades"]
GRID_4H = {0, 4, 8, 12, 16, 20}


# ----------------------------------------------------------------------------
# Hilfsfunktionen
# ----------------------------------------------------------------------------

def log(msg):
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"{stamp}  {msg}"
    print(line, flush=True)
    os.makedirs(RAW, exist_ok=True)
    with open(LOGFILE, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def iso(ts_ms):
    d = dt.datetime.fromtimestamp(ts_ms / 1000, tz=dt.timezone.utc)
    return d.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return [dict(r) for r in csv.DictReader(fh)]


def write_csv(path, rows, columns):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=columns)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in columns})
        fh.flush()
        os.fsync(fh.fileno())
    with open(tmp, newline="", encoding="utf-8") as fh:
        n = sum(1 for _ in csv.DictReader(fh))
    if n != len(rows):
        os.remove(tmp)
        raise RuntimeError(f"Schreibkontrolle fehlgeschlagen fuer {path}: {n} statt {len(rows)} Zeilen")
    os.replace(tmp, path)


_PROV = None


def prov_update(key, entry):
    global _PROV
    if _PROV is None:
        _PROV = {}
        if os.path.exists(PROVENANCE):
            try:
                with open(PROVENANCE, encoding="utf-8") as fh:
                    _PROV = json.load(fh)
            except Exception:
                _PROV = {}
    entry["written_utc"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    _PROV[key] = entry
    tmp = PROVENANCE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(_PROV, fh, indent=1, ensure_ascii=False, sort_keys=True)
    os.replace(tmp, PROVENANCE)


def bar_seconds(interval):
    return {"4h": 4 * 3600, "1d": 24 * 3600}[interval]


def validate_bars(rows, interval, label, has_taker=True):
    """Liefert (ok, kritisch, warnungen, luecken). Kritisch: Raster, Monotonie, OHLC, Taker > Volumen."""
    critical, warnings, gaps = [], [], []
    step = bar_seconds(interval)
    prev = None
    for i, r in enumerate(rows):
        try:
            t = parse_iso(r["t"])
        except Exception:
            critical.append(f"Zeile {i}: Zeitstempel unlesbar {r.get('t')}"); continue
        if interval == "4h" and (t.hour not in GRID_4H or t.minute or t.second):
            critical.append(f"Zeile {i}: 4h-Kerze ausserhalb Raster {r['t']}")
        if interval == "1d" and (t.hour or t.minute or t.second):
            critical.append(f"Zeile {i}: Tageskerze nicht um 00:00 UTC {r['t']}")
        if prev is not None:
            d = (t - prev).total_seconds()
            if d <= 0:
                critical.append(f"Zeile {i}: Zeitachse nicht monoton bei {r['t']}")
            elif d > step:
                gaps.append((prev.strftime("%Y-%m-%dT%H:%M:%SZ"), r["t"], int(d // step) - 1))
        prev = t
        try:
            o, h, l, c, v = (float(r[k]) for k in ("open", "high", "low", "close", "volume"))
        except Exception:
            critical.append(f"Zeile {i} ({r['t']}): OHLCV nicht numerisch"); continue
        if not (l <= min(o, c) and max(o, c) <= h):
            critical.append(f"Zeile {i} ({r['t']}): OHLC inkonsistent")
        if v < 0:
            critical.append(f"Zeile {i} ({r['t']}): Volumen negativ")
        if v == 0:
            warnings.append(f"{r['t']}: Volumen null")
        if has_taker:
            try:
                tb = float(r["taker_buy_base"])
            except Exception:
                critical.append(f"Zeile {i} ({r['t']}): Taker-Buy nicht numerisch"); continue
            if tb < 0 or tb > v * 1.000001:
                critical.append(f"Zeile {i} ({r['t']}): Taker-Buy {tb} > Volumen {v}")
    if gaps:
        warnings.append(f"{len(gaps)} Luecken, groesste {max(g[2] for g in gaps)} Kerzen")
    return len(critical) == 0, critical, warnings, gaps


# ----------------------------------------------------------------------------
# Binance Vision, alle Spalten
# ----------------------------------------------------------------------------

def parse_binance_full(blob):
    rows = []
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        text = z.read(z.namelist()[0]).decode("utf-8")
    for line in csv.reader(io.StringIO(text)):
        if len(line) < 11 or not line[0].strip().lstrip("-").isdigit():
            continue
        ts = int(line[0]); ct = int(line[6])
        if ts > 10**14:          # Mikrosekunden (Binance seit 2025)
            ts //= 1000
        if ct > 10**14:
            ct //= 1000
        rows.append({"t": iso(ts), "open": line[1], "high": line[2], "low": line[3], "close": line[4],
                     "volume": line[5], "close_time": iso(ct), "quote_volume": line[7], "trades": line[8],
                     "taker_buy_base": line[9], "taker_buy_quote": line[10]})
    return rows


def first_month_hint(sym, market):
    """Erster Monat aus den vorhandenen OHLCV-Tagesdateien, sonst Universalstart (404 wird uebersprungen)."""
    old = os.path.join(DIR_SPOT_OLD if market == "spot" else DIR_PERP_OLD, f"{sym}_1d.csv")
    rows = read_csv(old)
    if rows:
        d = dt.date.fromisoformat(rows[0]["t"][:10])
        return (d.year, d.month)
    return SPOT_START if market == "spot" else PERP_START


def binance_full(sym, market, interval):
    base = NH.BINANCE_BASE if market == "spot" else NH.BINANCE_FUT
    outdir = DIR_SPOT_FULL if market == "spot" else DIR_PERP_FULL
    path = os.path.join(outdir, f"{sym}_{interval}.csv")
    label = f"{market} {sym} {interval}"
    existing = read_csv(path)
    by_t = {r["t"]: r for r in existing}
    today = dt.datetime.now(dt.timezone.utc).date()
    end_full_month = today.replace(day=1) - dt.timedelta(days=1)
    end_m = (end_full_month.year, end_full_month.month)
    if existing:
        last = parse_iso(existing[-1]["t"]).date()
        start_m = (last.year, last.month)
        log(f"{label}: vorhanden bis {last}, ergaenze ab {start_m[0]}-{start_m[1]:02d}")
    else:
        start_m = first_month_hint(sym, market)
        log(f"{label}: neu, lade ab {start_m[0]}-{start_m[1]:02d}")
    first_available, missing = None, []
    for y, m in NH.month_iter(start_m, end_m):
        blob = NH.fetch(f"{base}/monthly/klines/{sym}/{interval}/{sym}-{interval}-{y}-{m:02d}.zip")
        time.sleep(PAUSE)
        if blob is None:
            if first_available is None and not existing:
                continue
            missing.append(f"{y}-{m:02d}")
            continue
        if first_available is None:
            first_available = f"{y}-{m:02d}"
        for r in parse_binance_full(blob):
            by_t[r["t"]] = r
    # laufender Monat: Tagesdateien bis gestern
    d = today.replace(day=1)
    stop = today - dt.timedelta(days=1)
    while d <= stop:
        blob = NH.fetch(f"{base}/daily/klines/{sym}/{interval}/{sym}-{interval}-{d.isoformat()}.zip")
        time.sleep(PAUSE)
        if blob is not None:
            for r in parse_binance_full(blob):
                if parse_iso(r["t"]).date() <= stop:
                    by_t[r["t"]] = r
        d += dt.timedelta(days=1)
    rows = [by_t[k] for k in sorted(by_t)]
    if not rows:
        log(f"  {label}: nichts erhalten"); return None
    ok, crit, warn, gaps = validate_bars(rows, interval, label)
    for w in warn[:5]:
        log(f"  Hinweis {label}: {w}")
    if not ok:
        for c in crit[:10]:
            log(f"  KRITISCH {label}: {c}")
        log(f"  {label}: nicht geschrieben ({len(crit)} kritische Befunde)")
        return None
    write_csv(path, rows, FULL_COLUMNS)
    entry = {"file": os.path.relpath(path, HERE), "source": f"binance_vision {market} klines {interval}, alle Spalten",
             "symbol": sym, "market": "spot" if market == "spot" else "usdt_m_perpetual", "interval": interval,
             "rows": len(rows), "first": rows[0]["t"], "last": rows[-1]["t"], "gaps": len(gaps),
             "gap_list": gaps[:30], "missing_months": missing, "sha256": NH.sha256_of(path)}
    if first_available:
        entry["first_available_month_binance"] = first_available
    log(f"  OK {label}: {len(rows)} Kerzen {rows[0]['t']} bis {rows[-1]['t']}, Luecken {len(gaps)}")
    return path, rows, entry


def crosscheck_daily(sym, market, rows_1d, entry):
    """Vollspalten-Tageskerzen gegen die vorhandenen OHLCV-Tageskerzen: Schlusskurse muessen exakt uebereinstimmen."""
    old = read_csv(os.path.join(DIR_SPOT_OLD if market == "spot" else DIR_PERP_OLD, f"{sym}_1d.csv"))
    if not old:
        entry["crosscheck_vs_ohlcv"] = "keine Vergleichsdatei"; return
    new = {r["t"][:10]: r for r in rows_1d}
    common = [r for r in old if r["t"] in new]
    diff = [r["t"] for r in common if abs(float(r["close"]) - float(new[r["t"]]["close"])) > 1e-9 * max(1.0, float(r["close"]))]
    entry["crosscheck_vs_ohlcv"] = {"common_days": len(common), "close_mismatch": len(diff), "examples": diff[:10]}
    log(f"  Gegenprobe {market} {sym} 1d gegen OHLCV: {len(common)} gemeinsame Tage, {len(diff)} abweichende Schlusskurse")


def crosscheck_4h_vs_1d(sym, market, rows_4h, rows_1d, entry):
    """4h auf Tag aggregiert (nur vollstaendige Tage mit sechs Kerzen) gegen Tageskerzen."""
    days = {}
    for r in rows_4h:
        days.setdefault(r["t"][:10], []).append(r)
    d1 = {r["t"][:10]: r for r in rows_1d}
    n, bad = 0, []
    for day, bars in days.items():
        if len(bars) != 6 or day not in d1:
            continue
        n += 1
        o = float(bars[0]["open"]); c = float(bars[-1]["close"])
        h = max(float(b["high"]) for b in bars); l = min(float(b["low"]) for b in bars)
        v = sum(float(b["volume"]) for b in bars)
        ref = d1[day]
        tol = lambda a, b: abs(a - b) > 1e-6 * max(1.0, abs(b))
        if tol(o, float(ref["open"])) or tol(c, float(ref["close"])) or tol(h, float(ref["high"])) or tol(l, float(ref["low"])) or tol(v, float(ref["volume"])):
            bad.append(day)
    entry["crosscheck_4h_aggregated_vs_1d"] = {"complete_days": n, "mismatch": len(bad), "examples": bad[:10]}
    log(f"  Gegenprobe {market} {sym} 4h->1d: {n} vollstaendige Tage, {len(bad)} Abweichungen")


def run_binance(coins):
    for coin in coins:
        sym = f"{coin}USDT"
        for market in ("spot", "perp"):
            res = {}
            for interval in ("1d", "4h"):
                r = binance_full(sym, market, interval)
                if r:
                    res[interval] = r
            if "1d" in res:
                crosscheck_daily(sym, market, res["1d"][1], res["1d"][2])
            if "1d" in res and "4h" in res:
                crosscheck_4h_vs_1d(sym, market, res["4h"][1], res["1d"][1], res["4h"][2])
            for interval, (path, rows, entry) in res.items():
                prov_update(f"binance_{market}_{sym}_{interval}", entry)


# ----------------------------------------------------------------------------
# Kraken 240 Minuten aus dem Archiv
# ----------------------------------------------------------------------------

def kraken_zip_path():
    z = os.path.join(DIR_KA_DL, ZIPNAME)
    if os.path.exists(z) and os.path.getsize(z) > 1 << 30:
        return z
    parts = [os.path.join(DIR_KA_DL, f"{ZIPNAME}.part0{i}") for i in range(5)]
    if all(os.path.exists(p) for p in parts):
        log("Archiv-Zip fehlt, setze aus fuenf Teilen zusammen (einige Minuten)")
        tmp = z + ".tmp"
        with open(tmp, "wb") as out:
            for p in parts:
                with open(p, "rb") as fh:
                    for ch in iter(lambda: fh.read(1 << 24), b""):
                        out.write(ch)
        os.replace(tmp, z)
        log(f"  zusammengesetzt, SHA-256 {NH.sha256_of(z)}")
        return z
    return None


def kraken_convert(raw_path, coin):
    rows = []
    with open(raw_path, encoding="utf-8") as fh:
        for line in fh:
            p = line.strip().split(",")
            if len(p) < 6 or not p[0].strip().lstrip("-").isdigit():
                continue
            ts = int(float(p[0]))
            rows.append({"t": iso(ts * 1000), "open": p[1], "high": p[2], "low": p[3], "close": p[4],
                         "volume": p[5], "trades": p[6] if len(p) > 6 else ""})
    rows.sort(key=lambda r: r["t"])
    return rows


def run_kraken_archive(coins):
    z = kraken_zip_path()
    if z is None:
        log(f"Kraken-Archiv nicht gefunden in {DIR_KA_DL} (weder {ZIPNAME} noch die fuenf Teile). "
            f"Bitte zuerst Daten-Kraken-Archiv.command ausfuehren. Schritt uebersprungen.")
        return {}
    log(f"Kraken-Archiv: {z} ({os.path.getsize(z) / 1e9:.2f} GB)")
    zf = zipfile.ZipFile(z)
    names = zf.namelist()
    out = {}
    for coin in coins:
        pair = KRAKEN_PAIRS[coin]
        pat = re.compile(rf"(^|/){pair}_240\.csv$")
        m = [n for n in names if pat.search(n)]
        if not m:
            log(f"  FEHLT im Archiv: {pair}_240.csv"); continue
        raw_dst = os.path.join(DIR_KA, f"{pair}_240.csv")
        os.makedirs(DIR_KA, exist_ok=True)
        with zf.open(m[0]) as src, open(raw_dst + ".tmp", "wb") as dst:
            dst.write(src.read())
        os.replace(raw_dst + ".tmp", raw_dst)
        rows = kraken_convert(raw_dst, coin)
        ok, crit, warn, gaps = validate_bars(rows, "4h", f"kraken {pair} 240", has_taker=False)
        for c in crit[:10]:
            log(f"  KRITISCH kraken {pair}: {c}")
        if not ok:
            log(f"  kraken {pair}: nicht geschrieben ({len(crit)} kritische Befunde)"); continue
        path = os.path.join(DIR_K4, f"{coin}USD_4h.csv")
        write_csv(path, rows, KRAKEN_COLUMNS)
        entry = {"file": os.path.relpath(path, HERE), "raw_file": os.path.relpath(raw_dst, HERE), "archive": ZIPNAME,
                 "archive_member": m[0], "pair": pair, "interval": "240min", "rows": len(rows),
                 "first": rows[0]["t"], "last": rows[-1]["t"], "gaps": len(gaps), "gap_list": gaps[:30],
                 "largest_gap_bars": max([g[2] for g in gaps], default=0),
                 "sha256_raw": NH.sha256_of(raw_dst), "sha256": NH.sha256_of(path)}
        prov_update(f"kraken_archiv_{coin}_4h", entry)
        log(f"  OK kraken {pair} 240: {len(rows)} Kerzen {rows[0]['t']} bis {rows[-1]['t']}, Luecken {len(gaps)}")
        out[coin] = rows
    return out


def run_kraken_api(coins, archive_rows):
    os.makedirs(DIR_KAPI, exist_ok=True); os.makedirs(DIR_KMERGED, exist_ok=True)
    for coin in coins:
        pair = KRAKEN_PAIRS[coin]
        raw = NH.fetch(f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval=240")
        time.sleep(1.1)
        if raw is None:
            log(f"  API {pair}: nicht gefunden"); continue
        js = json.loads(raw)
        if js.get("error"):
            log(f"  API-Fehler {pair}: {js['error']}"); continue
        key = [k for k in js["result"] if k != "last"][0]
        rows = [{"t": iso(int(r[0]) * 1000), "open": r[1], "high": r[2], "low": r[3], "close": r[4],
                 "volume": r[6], "trades": r[7]} for r in js["result"][key]]
        rows = rows[:-1]  # letzte Kerze unvollstaendig
        api_path = os.path.join(DIR_KAPI, f"{coin}USD_4h.csv")
        # vorhandene API-Datei ergaenzen, damit ueber mehrere Laeufe mehr als 120 Tage entstehen
        by_t = {r["t"]: r for r in read_csv(api_path)}
        for r in rows:
            by_t[r["t"]] = r
        api_rows = [by_t[k] for k in sorted(by_t)]
        write_csv(api_path, api_rows, KRAKEN_COLUMNS)
        entry = {"file": os.path.relpath(api_path, HERE), "source": "kraken REST OHLC interval=240", "pair_key": key,
                 "rows": len(api_rows), "first": api_rows[0]["t"], "last": api_rows[-1]["t"], "sha256": NH.sha256_of(api_path)}
        prov_update(f"kraken_api_{coin}_4h", entry)
        log(f"  API {pair} 240: {len(api_rows)} Kerzen {api_rows[0]['t']} bis {api_rows[-1]['t']}")
        # Zusammenfuehrung: Archiv bis Archivende, danach API. Ueberlappung als Gegenprobe.
        arch = archive_rows.get(coin) or read_csv(os.path.join(DIR_K4, f"{coin}USD_4h.csv"))
        if not arch:
            continue
        arch_last = arch[-1]["t"]
        a_by = {r["t"]: r for r in arch}
        overlap = [r for r in api_rows if r["t"] in a_by]
        diff = [r["t"] for r in overlap if abs(float(r["close"]) - float(a_by[r["t"]]["close"])) > 1e-9 * max(1.0, float(r["close"]))]
        merged = list(arch) + [r for r in api_rows if r["t"] > arch_last]
        ok, crit, warn, gaps = validate_bars(merged, "4h", f"kraken merged {pair}", has_taker=False)
        mpath = os.path.join(DIR_KMERGED, f"{coin}USD_4h.csv")
        if not ok:
            for c in crit[:10]:
                log(f"  KRITISCH merged {pair}: {c}")
            continue
        write_csv(mpath, merged, KRAKEN_COLUMNS)
        seam_gap = [g for g in gaps if g[0] == arch_last]
        prov_update(f"kraken_merged_{coin}_4h", {
            "file": os.path.relpath(mpath, HERE), "seam_archive_last": arch_last,
            "api_first": api_rows[0]["t"], "seam_gap_bars": seam_gap[0][2] if seam_gap else 0,
            "overlap_bars": len(overlap), "overlap_close_mismatch": len(diff), "overlap_examples": diff[:10],
            "rows": len(merged), "first": merged[0]["t"], "last": merged[-1]["t"], "gaps": len(gaps),
            "sha256": NH.sha256_of(mpath)})
        log(f"  merged {pair}: {len(merged)} Kerzen bis {merged[-1]['t']}, Naht nach {arch_last}, "
            f"Nahtluecke {seam_gap[0][2] if seam_gap else 0} Kerzen, Ueberlappung {len(overlap)} Kerzen, {len(diff)} Abweichungen")


# ----------------------------------------------------------------------------

def main(argv):
    coins = COINS
    if "--coins" in argv:
        coins = [c.strip().upper() for c in argv[argv.index("--coins") + 1].split(",")]
        bad = [c for c in coins if c not in COINS]
        if bad:
            print(f"Unbekannte Coins: {bad}"); return 2
    log(f"Start nachladen_4h, Coins {coins}, Python {sys.version.split()[0]}")
    if "--nur-kraken" not in argv:
        log("Schritt 1 und 2: Binance Vision Spot und Perp, 1d und 4h, alle Spalten")
        run_binance(coins)
    if "--nur-binance" not in argv:
        log("Schritt 3: Kraken 240 Minuten aus dem Archiv")
        arch = run_kraken_archive(coins)
        log("Schritt 4: Kraken API 240 Minuten und Zusammenfuehrung")
        run_kraken_api(coins, arch)
    log(f"Fertig. Herkunft in {os.path.relpath(PROVENANCE, HERE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
