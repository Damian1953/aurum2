#!/usr/bin/env python3
"""XS21 PiT v1.0 §7: Datenbeschaffung, NUR data.binance.vision (oeffentlich). Keine fapi-Aufrufe (geoblockt, nicht noetig).

Symbole: binance_um_universe.csv (Lane-C-Loader v1.1, eingefroren f5563c09…), USDT-Perpetuals, ASCII, ohne Termin/SETTLED,
ohne B7-Ausschluesse v1.0. Je Symbol:
  - 1d-Klines monatlich first_month..last_month (<= 2026-08), dazu taeglich 2026-09-01..2026-09-15 (Monatsdatei 2026-09 noch nicht publiziert)
  - fundingRate monatlich first_month..min(last_month+1, 2026-09)
Jede ZIP mit .CHECKSUM geprueft, ZIP abgelegt, Provenienz in data/xs21/provenance.jsonl. Wiederaufnahmefaehig. 404 = nicht vorhanden (protokolliert).
"""
import concurrent.futures as cf, csv, hashlib, io, json, os, sys, time, urllib.error, urllib.request, zipfile, datetime as dt
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "data", "xs21"); ZIPS = os.path.join(OUT, "zips")
BV = "https://data.binance.vision/data/futures/um"
UA = "aurum2-xs21/1.0 (public market data, research)"

def http(url, tries=5):
    for a in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404: return 404, None
            if e.code == 451: raise SystemExit(f"HTTP 451 {url} (Geoblock) - Abbruch, kein Umgehen")
            err = e
        except Exception as e:
            err = e
        time.sleep(2 * 2 ** a)
    raise RuntimeError(f"{url}: {err}")

def months(a, b):
    y, m = map(int, a.split("-")); Y, M = map(int, b.split("-"))
    while (y, m) <= (Y, M):
        yield f"{y:04d}-{m:02d}"; y, m = (y + 1, 1) if m == 12 else (y, m + 1)

def job(kind, sym, period):
    if kind == "kl_m": rel = f"monthly/klines/{sym}/1d/{sym}-1d-{period}.zip"
    elif kind == "kl_d": rel = f"daily/klines/{sym}/1d/{sym}-1d-{period}.zip"
    else: rel = f"monthly/fundingRate/{sym}/{sym}-fundingRate-{period}.zip"
    local = os.path.join(ZIPS, rel)
    if os.path.exists(local) and os.path.exists(local + ".ok"):
        return dict(kind=kind, symbol=sym, period=period, url=f"{BV}/{rel}", status="cached", sha256=open(local + ".ok").read().strip())
    st, z = http(f"{BV}/{rel}")
    if st == 404:
        return dict(kind=kind, symbol=sym, period=period, url=f"{BV}/{rel}", status="404")
    st2, ck = http(f"{BV}/{rel}.CHECKSUM")
    h = hashlib.sha256(z).hexdigest()
    if st2 == 404 or ck.decode().split()[0] != h:
        raise RuntimeError(f"CHECKSUM fehlt/falsch: {rel}")
    os.makedirs(os.path.dirname(local), exist_ok=True)
    open(local, "wb").write(z); open(local + ".ok", "w").write(h)
    return dict(kind=kind, symbol=sym, period=period, url=f"{BV}/{rel}", status="ok", sha256=h, checksum_ok=True)

def main():
    excl = {r["symbol"] for r in csv.DictReader(open(os.path.join(REPO, "01_forschung/09_lane_c/xs21_pit_v1.0/xs21_exclusions_v1.0.csv")))}
    uni = list(csv.DictReader(open(os.path.join(REPO, "data/raw/binance_um_universe.csv"))))
    syms = [r for r in uni if r["symbol"].endswith("USDT") and "_" not in r["symbol"] and "SETTLED" not in r["symbol"]
            and r["symbol"].isascii() and r["symbol"] not in excl]
    jobs = []
    for r in syms:
        s, a, b = r["symbol"], r["first_month"], min(r["last_month"], "2026-08")
        if a > "2026-08": continue
        jobs += [("kl_m", s, p) for p in months(a, b)]
        fb = "2026-09" if r["last_month"] >= "2026-08" else next(iter(list(months(r["last_month"], "2026-09"))[1:2]), r["last_month"])
        jobs += [("fu", s, p) for p in months(a, fb)]
        if r["last_month"] >= "2026-08":
            jobs += [("kl_d", s, f"2026-09-{d:02d}") for d in range(1, 16)]
    print(f"Symbole {len(syms)}, Jobs {len(jobs)}", flush=True)
    os.makedirs(OUT, exist_ok=True)
    res = []; t0 = time.time()
    with cf.ThreadPoolExecutor(32) as ex:
        for i, r in enumerate(ex.map(lambda j: job(*j), jobs)):
            res.append(r)
            if i % 2000 == 0: print(i, round(time.time() - t0), flush=True)
    with open(os.path.join(OUT, "provenance.jsonl"), "w") as fh:
        for r in sorted(res, key=lambda r: (r["kind"], r["symbol"], r["period"])):
            fh.write(json.dumps(r) + "\n")
    from collections import Counter
    print(Counter((r["kind"], r["status"] if r["status"] != "cached" else "ok") for r in res))
    json.dump(dict(fetched_at=dt.datetime.now(dt.timezone.utc).isoformat(), symbols=len(syms), jobs=len(jobs)), open(os.path.join(OUT, "fetch_meta.json"), "w"))

if __name__ == "__main__":
    main()
