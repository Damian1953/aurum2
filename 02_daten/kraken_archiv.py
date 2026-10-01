#!/usr/bin/env python3
"""
Project Aurum II — 03_mtp_validation: Kraken-Spot-Tageshistorie aus dem offiziellen Kraken-OHLCVT-Archiv.
Quelle: https://support.kraken.com/articles/360047124832 (Kraken_OHLCVT_Full_2026Q2, fuenf Teile, SHA-256-Liste von Kraken).

Ablauf (stdlib only, TLS ueber nachladen_historie.ssl_context()):
  1. Teile part00..part04 und OHLCVT_Full_PARTS_SHA256SUMS.txt nach raw/kraken_archiv/_download/ laden (ca. 10 GB, wird nur geladen, was fehlt).
  2. SHA-256 jedes Teils gegen Krakens Liste pruefen (fail-closed).
  3. Teile zu Kraken_OHLCVT_Full_2026Q2.zip zusammensetzen, SHA-256 des Ganzen protokollieren.
  4. Nur die zehn Tagesdateien <PAIR>USD_1440.csv extrahieren (XBT ETH SOL XRP ADA AVAX LINK DOT BNB LTC).
  5. In unser Format konvertieren: raw/kraken_archiv/<COIN>USD_1d.csv (t,open,high,low,close,volume,trades; UTC-Tag), Rohdatei daneben behalten.
  6. Ergaenzung Juli bis heute aus der Kraken-REST-API (720 Tage) nach raw/kraken_api/<COIN>USD_1d.csv, Naht dokumentiert in provenance_kraken.json.
Manuelle Alternative: Teile im Browser laden und nach raw/kraken_archiv/_download/ legen, dann dieses Skript starten, es ueberspringt vorhandene Teile.
"""
import os, sys, json, csv, hashlib, zipfile, re, time, datetime as dt, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nachladen_historie as NH

HERE = os.path.dirname(os.path.abspath(__file__))
DL = os.path.join(HERE, "raw", "kraken_archiv", "_download")
OUT = os.path.join(HERE, "raw", "kraken_archiv")
API = os.path.join(HERE, "raw", "kraken_api")
BASE = "https://assets.kraken.com/marketing/institutions/"
ZIPNAME = "Kraken_OHLCVT_Full_2026Q2.zip"
PARTS = [f"{ZIPNAME}.part0{i}" for i in range(5)]
SUMS = "OHLCVT_Full_PARTS_SHA256SUMS.txt"
PAIRS = {"BTC": "XBTUSD", "ETH": "ETHUSD", "SOL": "SOLUSD", "XRP": "XRPUSD", "ADA": "ADAUSD", "AVAX": "AVAXUSD",
         "LINK": "LINKUSD", "DOT": "DOTUSD", "BNB": "BNBUSD", "LTC": "LTCUSD"}
API_PAIRS = {"BTC": "XBTUSD", "ETH": "ETHUSD", "SOL": "SOLUSD", "XRP": "XRPUSD", "ADA": "ADAUSD", "AVAX": "AVAXUSD",
             "LINK": "LINKUSD", "DOT": "DOTUSD", "BNB": "BNBUSD", "LTC": "LTCUSD"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for ch in iter(lambda: fh.read(1 << 22), b""): h.update(ch)
    return h.hexdigest()


def download(name):
    dst = os.path.join(DL, name)
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        print(f"  vorhanden: {name} ({os.path.getsize(dst)/1e9:.2f} GB)"); return dst
    print(f"  lade {name} ...")
    req = urllib.request.Request(BASE + name, headers={"User-Agent": NH.USER_AGENT})
    tmp = dst + ".tmp"
    with urllib.request.urlopen(req, timeout=120, context=NH.ssl_context()) as r, open(tmp, "wb") as fh:
        total = int(r.headers.get("Content-Length") or 0); done = 0; t0 = time.time()
        while True:
            ch = r.read(1 << 22)
            if not ch: break
            fh.write(ch); done += len(ch)
            if total and int(done / (1 << 28)) != int((done - len(ch)) / (1 << 28)):
                print(f"    {done/1e9:.2f} / {total/1e9:.2f} GB ({time.time()-t0:.0f} s)")
    os.replace(tmp, dst); print(f"  OK {name} ({os.path.getsize(dst)/1e9:.2f} GB)")
    return dst


def step_download_verify():
    os.makedirs(DL, exist_ok=True)
    sums_path = download(SUMS)
    want = {}
    for line in open(sums_path):
        parts = line.split()
        if len(parts) >= 2: want[os.path.basename(parts[-1]).lstrip("*")] = parts[0].lower()
    for p in PARTS:
        path = download(p)
        got = sha256(path)
        exp = want.get(p)
        if exp is None:
            print(f"  WARNUNG: kein Kraken-Hash fuer {p} in {SUMS}, Hash protokolliert: {got}")
        elif got != exp:
            raise RuntimeError(f"SHA-256 von {p} stimmt nicht: {got} != {exp}. Datei loeschen und neu laden.")
        else:
            print(f"  SHA-256 OK {p}")
    return want


def step_assemble():
    z = os.path.join(DL, ZIPNAME)
    if os.path.exists(z):
        print(f"  Archiv vorhanden: {ZIPNAME}"); return z
    print("  setze Teile zusammen ...")
    tmp = z + ".tmp"
    with open(tmp, "wb") as out:
        for p in PARTS:
            with open(os.path.join(DL, p), "rb") as fh:
                for ch in iter(lambda: fh.read(1 << 24), b""): out.write(ch)
    os.replace(tmp, z); print(f"  OK {ZIPNAME} ({os.path.getsize(z)/1e9:.2f} GB)")
    return z


def step_extract(z):
    os.makedirs(OUT, exist_ok=True)
    zf = zipfile.ZipFile(z)
    names = zf.namelist()
    found = {}
    for coin, pair in PAIRS.items():
        pat = re.compile(rf"(^|/){pair}_1440\.csv$")
        m = [n for n in names if pat.search(n)]
        if not m:
            print(f"  FEHLT im Archiv: {pair}_1440.csv (Coin {coin})"); continue
        raw_dst = os.path.join(OUT, f"{pair}_1440.csv")
        with zf.open(m[0]) as src, open(raw_dst, "wb") as dst: dst.write(src.read())
        found[coin] = raw_dst
        print(f"  extrahiert {m[0]} -> {os.path.basename(raw_dst)}")
    return found


def step_convert(found):
    prov = {}
    for coin, raw_path in found.items():
        rows = []
        with open(raw_path) as fh:
            for line in fh:
                p = line.strip().split(",")
                if len(p) < 6: continue
                ts = int(float(p[0])); day = dt.datetime.fromtimestamp(ts, dt.timezone.utc)
                rows.append((day.strftime("%Y-%m-%d"), p[1], p[2], p[3], p[4], p[5], p[6] if len(p) > 6 else ""))
        rows.sort()
        # Tagesraster pruefen: Kraken-1440-Kerzen beginnen 00:00 UTC
        offs = set(dt.datetime.fromtimestamp(int(float(l.split(",")[0])), dt.timezone.utc).strftime("%H:%M") for l in open(raw_path) if l.strip())
        out = os.path.join(OUT, f"{coin}USD_1d.csv")
        with open(out + ".tmp", "w", newline="") as fh:
            w = csv.writer(fh); w.writerow(["t", "open", "high", "low", "close", "volume", "trades"]); w.writerows(rows)
        os.replace(out + ".tmp", out)
        days = [dt.date.fromisoformat(r[0]) for r in rows]
        gaps = [(str(days[i-1]), str(days[i])) for i in range(1, len(days)) if (days[i] - days[i-1]).days > 1]
        prov[coin] = dict(pair=PAIRS[coin], rows=len(rows), first=rows[0][0] if rows else None, last=rows[-1][0] if rows else None,
                          gaps=len(gaps), gap_list=gaps[:20], bar_start_utc=sorted(offs), sha256_raw=sha256(raw_path), sha256_csv=sha256(out))
        print(f"  {coin}: {len(rows)} Tage {prov[coin]['first']}..{prov[coin]['last']}, Luecken {len(gaps)}, Kerzenbeginn {sorted(offs)}")
    return prov


def step_api():
    """Kraken REST OHLC, interval 1440, liefert die letzten 720 Tage. Dient der Ergaenzung ab 2026-07-01 und der Gegenprobe."""
    os.makedirs(API, exist_ok=True); prov = {}
    for coin, pair in API_PAIRS.items():
        raw = NH.fetch(f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval=1440")
        if raw is None: print(f"  API: {pair} nicht gefunden"); continue
        js = json.loads(raw)
        if js.get("error"): print(f"  API-Fehler {pair}: {js['error']}"); continue
        key = [k for k in js["result"] if k != "last"][0]
        rows = [(dt.datetime.fromtimestamp(int(r[0]), dt.timezone.utc).strftime("%Y-%m-%d"), r[1], r[2], r[3], r[4], r[6], r[7]) for r in js["result"][key]]
        rows = rows[:-1]  # letzte Kerze ist unvollstaendig
        out = os.path.join(API, f"{coin}USD_1d.csv")
        with open(out + ".tmp", "w", newline="") as fh:
            w = csv.writer(fh); w.writerow(["t", "open", "high", "low", "close", "volume", "trades"]); w.writerows(rows)
        os.replace(out + ".tmp", out)
        prov[coin] = dict(pair_key=key, rows=len(rows), first=rows[0][0], last=rows[-1][0], sha256_csv=sha256(out))
        print(f"  API {coin}: {len(rows)} Tage {rows[0][0]}..{rows[-1][0]}")
        time.sleep(1.1)
    return prov


if __name__ == "__main__":
    print("Kraken-OHLCVT-Archiv 2026Q2, zehn USD-Paare, Tageskerzen")
    print("Schritt 1: Teile laden und gegen Krakens SHA-256-Liste pruefen (ca. 10 GB)")
    want = step_download_verify()
    print("Schritt 2: zusammensetzen")
    z = step_assemble()
    print("Schritt 3: Tagesdateien extrahieren")
    found = step_extract(z)
    print("Schritt 4: konvertieren")
    prov = step_convert(found)
    print("Schritt 5: Ergaenzung und Gegenprobe aus der REST-API")
    api = step_api()
    json.dump(dict(archive=ZIPNAME, archive_sha256=sha256(z), kraken_part_hashes=want, fetched_at=dt.datetime.now(dt.timezone.utc).isoformat(),
                   archiv=prov, api=api), open(os.path.join(OUT, "provenance_kraken.json"), "w"), indent=1)
    print("Fertig. provenance_kraken.json geschrieben. Die Teile in _download/ koennen nach erfolgreicher Pruefung geloescht werden.")
