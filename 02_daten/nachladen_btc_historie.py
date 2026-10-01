#!/usr/bin/env python3
"""
Project Aurum II — BTC/USD-Tageshistorie von Bitstamp und Coinbase (fuer 03_woo_mtp_reverse_engineering).
Zweck: Preisquelle des MTP-Backtesters identifizieren und Warmup fuer SMA200/ATR180 ab 2014 bereitstellen.
Stdlib only. Nutzt ssl_context() und fetch() aus nachladen_historie.py (gleicher Ordner).
Ausgabe: raw/bitstamp/BTCUSD_1d.csv, raw/coinbase/BTCUSD_1d.csv  (t,open,high,low,close,volume, UTC-Tag)
"""
import os, sys, json, csv, time, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nachladen_historie as NH

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
START = dt.datetime(2011, 8, 18, tzinfo=dt.timezone.utc)


def write_csv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["t", "open", "high", "low", "close", "volume"])
        for r in rows: w.writerow(r)
    os.replace(tmp, path)


def bitstamp():
    rows = {}
    start = int(START.timestamp()); now = int(time.time())
    while start < now:
        url = f"https://www.bitstamp.net/api/v2/ohlc/btcusd/?step=86400&limit=1000&start={start}"
        raw = NH.fetch(url)
        if raw is None: break
        d = json.loads(raw)["data"]["ohlc"]
        if not d: break
        for c in d:
            ts = int(c["timestamp"]); day = dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%Y-%m-%d")
            rows[day] = (day, c["open"], c["high"], c["low"], c["close"], c["volume"])
        last = int(d[-1]["timestamp"])
        if last <= start: break
        start = last + 86400
        print(f"  bitstamp bis {dt.datetime.fromtimestamp(last, dt.timezone.utc).date()} ({len(rows)} Tage)")
        time.sleep(0.5)
    out = [rows[k] for k in sorted(rows)]
    write_csv(os.path.join(RAW, "bitstamp", "BTCUSD_1d.csv"), out)
    return out


def coinbase():
    rows = {}
    t0 = dt.datetime(2015, 1, 1, tzinfo=dt.timezone.utc); now = dt.datetime.now(dt.timezone.utc)
    while t0 < now:
        t1 = min(t0 + dt.timedelta(days=290), now)
        url = (f"https://api.exchange.coinbase.com/products/BTC-USD/candles?granularity=86400"
               f"&start={t0.strftime('%Y-%m-%dT%H:%M:%SZ')}&end={t1.strftime('%Y-%m-%dT%H:%M:%SZ')}")
        raw = NH.fetch(url)
        if raw is not None:
            for c in json.loads(raw):   # [time, low, high, open, close, volume]
                day = dt.datetime.fromtimestamp(int(c[0]), dt.timezone.utc).strftime("%Y-%m-%d")
                rows[day] = (day, c[3], c[2], c[1], c[4], c[5])
        print(f"  coinbase bis {t1.date()} ({len(rows)} Tage)")
        t0 = t1
        time.sleep(0.4)
    out = [rows[k] for k in sorted(rows)]
    write_csv(os.path.join(RAW, "coinbase", "BTCUSD_1d.csv"), out)
    return out


if __name__ == "__main__":
    print("Bitstamp BTC/USD Tageskerzen ab 2011-08-18 ...")
    b = bitstamp(); print(f"  OK {len(b)} Zeilen, {b[0][0] if b else '-'} bis {b[-1][0] if b else '-'}")
    print("Coinbase BTC-USD Tageskerzen ab 2015-01-01 ...")
    c = coinbase(); print(f"  OK {len(c)} Zeilen, {c[0][0] if c else '-'} bis {c[-1][0] if c else '-'}")
    for src, rows in (("bitstamp", b), ("coinbase", c)):
        NH.log(f"btc_historie {src}: {len(rows)} Zeilen") if hasattr(NH, "log") else None
    print("Fertig.")
