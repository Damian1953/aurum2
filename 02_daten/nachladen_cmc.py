#!/usr/bin/env python3
"""
Project Aurum II — CoinMarketCap BTC/USD Tageshistorie (fuer 03_woo_mtp_reverse_engineering).
Befund Stufe A: Die Ein-Leg-Einstiege des MTP-Backtesters sind exakt die CoinMarketCap-Tagesschlusskurse (UTC).
Quelle: CMC data-api v3 historical (oeffentlich, ohne Schluessel). Stdlib only, TLS via nachladen_historie.ssl_context().
Ausgabe: raw/coinmarketcap/BTCUSD_1d.csv  (t,open,high,low,close,volume,marketcap, UTC-Tag)
"""
import os, sys, json, csv, time, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nachladen_historie as NH

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "raw", "coinmarketcap")
START = dt.datetime(2013, 4, 28, tzinfo=dt.timezone.utc)   # CMC-Historie beginnt 2013-04-28
STEP = dt.timedelta(days=365)
# CMC-IDs der zehn Coins (Validierungs-Vorregistrierung v0.2, Abschnitt 3). Name und Symbol werden aus der Antwort geprueft.
COINS = {"BTC": 1, "ETH": 1027, "SOL": 5426, "XRP": 52, "ADA": 2010, "AVAX": 5805, "LINK": 1975, "DOT": 6636, "BNB": 1839, "LTC": 2}


def main(sym="BTC", cid=1):
    OUT = os.path.join(OUTDIR, f"{sym}USD_1d.csv")
    rows = {}; seen_name = None
    t0 = START; now = dt.datetime.now(dt.timezone.utc)
    while t0 < now:
        t1 = min(t0 + STEP, now)
        url = (f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id={cid}&convertId=2781"
               f"&timeStart={int(t0.timestamp())}&timeEnd={int(t1.timestamp())}")
        raw = NH.fetch(url)
        if raw is None:
            print(f"  404 fuer {t0.date()}..{t1.date()}"); t0 = t1; continue
        js = json.loads(raw)
        d = js.get("data", {})
        if d.get("symbol") and d.get("symbol") != sym:
            raise RuntimeError(f"CMC-ID {cid} liefert Symbol {d.get('symbol')}, erwartet {sym}. Abbruch.")
        seen_name = d.get("name", seen_name)
        quotes = d.get("quotes", [])
        for q in quotes:
            day = q["timeOpen"][:10]; v = q["quote"]
            rows[day] = (day, v["open"], v["high"], v["low"], v["close"], v.get("volume", ""), v.get("marketCap", ""))
        if quotes: print(f"  {sym} {t0.date()}..{t1.date()}: {len(quotes)} Tage (gesamt {len(rows)})")
        t0 = t1
        time.sleep(0.7)
    out = [rows[k] for k in sorted(rows)]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = OUT + ".tmp"
    with open(tmp, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["t", "open", "high", "low", "close", "volume", "marketcap"])
        for r in out: w.writerow(r)
    os.replace(tmp, OUT)
    # Luecken melden
    days = [dt.date.fromisoformat(r[0]) for r in out]
    gaps = [(days[i-1], days[i]) for i in range(1, len(days)) if (days[i] - days[i-1]).days > 1]
    print(f"  OK {sym} ({seen_name}): {len(out)} Zeilen, {out[0][0] if out else '-'} bis {out[-1][0] if out else '-'}, Luecken: {gaps[:10] if gaps else 'keine'}")
    if sym == "BTC":
        chk = {"2017-02-24": 1173.68, "2021-04-13": 63503.46, "2025-01-20": 102016.66}
        for d, want in chk.items():
            got = rows.get(d)
            print(f"  Kontrolle {d}: close {round(float(got[4]),2) if got else None} erwartet {want}")
    return len(out)


if __name__ == "__main__":
    only = sys.argv[1:] or list(COINS)
    print(f"CoinMarketCap USD-Tageskerzen ab 2013-04-28 fuer {', '.join(only)} ...")
    ok = 0
    for sym in only:
        try:
            main(sym, COINS[sym]); ok += 1
        except Exception as e:
            print(f"  FEHLER {sym}: {e}")
    print(f"Fertig. OK: {ok} von {len(only)}.")
