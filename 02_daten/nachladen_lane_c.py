#!/usr/bin/env python3
"""
Project Aurum II — Lane C Datenbeschaffung (kostenlos, offiziell).
  1. Kraken Futures: historische Funding-Raten je Perpetual (oeffentlicher Endpunkt, keine Authentifizierung)
     GET https://futures.kraken.com/derivatives/api/v3/historical-funding-rates?symbol=PF_XBTUSD
     -> raw/kraken_futures_funding/<SYMBOL>.csv, Tiefe wird protokolliert (Beginn, Ende, Anzahl, Intervall)
  2. Binance USDT-M Futures Universum, point-in-time aus Datenexistenz: S3-Listing aller Symbole unter
     data/futures/um/monthly/klines/ (auch delistete), je Symbol erster und letzter Monat aus dem Listing,
     Abgleich mit exchangeInfo (aktuell handelbar) -> raw/binance_um_universe.csv
Nur Beschaffung und Dokumentation, keine Auswertung.
"""
import csv, datetime as dt, json, os, re, sys, time, xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nachladen_historie as NH

HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, "raw")
DIR_KF = os.path.join(RAW, "kraken_futures_funding"); os.makedirs(DIR_KF, exist_ok=True)
LOG = os.path.join(RAW, "nachladen_lane_c.log")
KF_SYMBOLS = ["PF_XBTUSD", "PF_ETHUSD", "PF_SOLUSD", "PF_XRPUSD", "PF_ADAUSD", "PF_AVAXUSD", "PF_LINKUSD", "PF_DOTUSD", "PF_BNBUSD", "PF_LTCUSD",
              "PI_XBTUSD", "PI_ETHUSD", "PI_XRPUSD", "PI_LTCUSD", "PI_BCHUSD"]   # PI_ = inverse Perpetuals (aelter)
S3 = "https://s3-ap-northeast-1.amazonaws.com/data.binance.vision"


def log(m):
    line = f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}  {m}"; print(line, flush=True)
    open(LOG, "a", encoding="utf-8").write(line + "\n")


def kraken_futures_funding():
    prov = {}
    for sym in KF_SYMBOLS:
        raw = NH.fetch(f"https://futures.kraken.com/derivatives/api/v3/historical-funding-rates?symbol={sym}")
        time.sleep(1.0)
        if raw is None:
            log(f"  {sym}: nicht gefunden (404)"); continue
        js = json.loads(raw)
        rates = js.get("rates") or []
        if js.get("result") != "success" or not rates:
            log(f"  {sym}: keine Daten ({js.get('error') or js.get('result')})"); continue
        rates.sort(key=lambda r: r["timestamp"])
        path = os.path.join(DIR_KF, f"{sym}.csv")
        with open(path + ".tmp", "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh); w.writerow(["t", "fundingRate", "relativeFundingRate"])
            for r in rates: w.writerow([r["timestamp"], r.get("fundingRate"), r.get("relativeFundingRate")])
        os.replace(path + ".tmp", path)
        ts = [dt.datetime.fromisoformat(r["timestamp"].replace("Z", "+00:00")) for r in rates]
        gaps = sorted(set(round((b - a).total_seconds() / 3600, 1) for a, b in zip(ts[:-1], ts[1:])))
        prov[sym] = dict(rows=len(rates), first=rates[0]["timestamp"], last=rates[-1]["timestamp"], intervals_h=gaps[:6], sha256=NH.sha256_of(path))
        log(f"  OK {sym}: {len(rates)} Raten {rates[0]['timestamp']} bis {rates[-1]['timestamp']}, Intervalle (h) {gaps[:4]}")
    return prov


def binance_um_universe():
    symbols = {}; token = None
    while True:
        url = f"{S3}?delimiter=/&prefix=data/futures/um/monthly/klines/" + (f"&marker={token}" if token else "")
        raw = NH.fetch(url); time.sleep(0.3)
        root = ET.fromstring(raw); ns = {"s": root.tag.split("}")[0].strip("{")}
        prefixes = [p.find("s:Prefix", ns).text for p in root.findall("s:CommonPrefixes", ns)]
        for p in prefixes:
            symbols[p.rstrip("/").split("/")[-1]] = None
        trunc = root.find("s:IsTruncated", ns); nxt = root.find("s:NextMarker", ns)
        if trunc is not None and trunc.text == "true":
            token = nxt.text if nxt is not None else prefixes[-1]
        else:
            break
    log(f"  Binance UM Symbole im Archiv: {len(symbols)}")
    # erster/letzter Monat je Symbol aus dem 1d-Listing
    # v1.1: Wiederaufnahme aus Teilstand, URL-Kodierung, nicht-ASCII-Schluessel werden protokolliert und uebersprungen
    from urllib.parse import quote
    part_path = os.path.join(RAW, "binance_um_universe.partial.json")
    done = json.load(open(part_path)) if os.path.exists(part_path) else {}
    rows = []; skipped = []
    for i, sym in enumerate(sorted(symbols)):
        if sym in done:
            rows.append(done[sym]); continue
        if not sym.isascii():
            skipped.append(sym); log(f"  uebersprungen (nicht ASCII): {sym!r}"); continue
        try:
            raw = NH.fetch(f"{S3}?delimiter=/&prefix=" + quote(f"data/futures/um/monthly/klines/{sym}/1d/", safe="/")); time.sleep(0.15)
            root = ET.fromstring(raw); ns = {"s": root.tag.split("}")[0].strip("{")}
            keys = [k.find("s:Key", ns).text for k in root.findall("s:Contents", ns)]
            months = sorted(set(m.group(1) for k in keys for m in [re.search(r"-1d-(\d{4}-\d{2})\.zip$", k)] if m))
            rec = dict(symbol=sym, first_month=months[0] if months else "", last_month=months[-1] if months else "", n_months=len(months))
        except Exception as ex:
            skipped.append(sym); log(f"  FEHLER {sym}: {ex!r}"); continue
        rows.append(rec); done[sym] = rec
        if (i + 1) % 50 == 0:
            log(f"  ... {i + 1} Symbole"); json.dump(done, open(part_path, "w"))
    json.dump(done, open(part_path, "w"))
    if skipped: log(f"  {len(skipped)} Symbole uebersprungen: {skipped}")
    info = json.loads(NH.fetch("https://fapi.binance.com/fapi/v1/exchangeInfo") or b"{}")
    live = {s["symbol"]: s["status"] for s in info.get("symbols", [])}
    for r in rows:
        r["status_now"] = live.get(r["symbol"], "NOT_LISTED"); r["delisted_or_absent"] = r["status_now"] != "TRADING"
    path = os.path.join(RAW, "binance_um_universe.csv")
    with open(path + ".tmp", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    os.replace(path + ".tmp", path)
    n_del = sum(1 for r in rows if r["delisted_or_absent"])
    log(f"  OK Universum: {len(rows)} Symbole, davon {n_del} nicht mehr TRADING, Datei {os.path.relpath(path, HERE)} SHA {NH.sha256_of(path)[:16]}")
    return dict(symbols=len(rows), not_trading=n_del, skipped=skipped, sha256=NH.sha256_of(path))


if __name__ == "__main__":
    log("Start Lane C: Kraken Futures Funding")
    p1 = kraken_futures_funding()
    log("Binance UM Universum (S3-Listing)")
    p2 = binance_um_universe()
    json.dump(dict(kraken_futures_funding=p1, binance_um_universe=p2, run=dt.datetime.now(dt.timezone.utc).isoformat()),
              open(os.path.join(RAW, "provenance_lane_c.json"), "w"), indent=1)
    log("Fertig. Herkunft in raw/provenance_lane_c.json")
