#!/usr/bin/env python3
"""Aurum II – taeglicher Datensammler, NUR oeffentliche Daten, keine Keys, kein Trading.

Quellen
  kraken_futures_funding  futures.kraken.com v4 historicalfundingrates (rollendes ~1 Jahr), 15 Symbole wie 02_daten/raw
  kraken_ohlc             api.kraken.com /0/public/OHLC 1h/4h/1d (je 720 Bars), 10 Projekt-Coins, nur abgeschlossene Bars
  binance_funding         data.binance.vision Monats-ZIPs fundingRate (mit CHECKSUM); fapi.binance.com ist von hier geoblockt (451)
  binance_universe        data.binance.vision S3-Listing futures/um/daily/klines + HEAD auf die 1d-Kline von gestern/vorgestern
  kraken_futures_tickers  futures.kraken.com v3 instruments + tickers (ab 1.1): Tages-Snapshot je Perpetual (tradeable, 24h-Volumen USD,
                          Open Interest, Last, Zeitstempel) fuer das XS21-Ausfuehrbarkeits-Gate (M3); Instrumentenliste als Snapshot
  kraken_spot_tickers     api.kraken.com /0/public/Ticker (ab 1.1): 24h-Volumen und Last der 10 Projekt-Coins

Schreibpfad (02_daten/README.md): Validierung je Batch (kritisch -> ganzer Batch in _quarantine, nichts geschrieben),
append-only mit Dedup ueber den Zeitstempel, Konflikte (gleicher Schluessel, andere Werte) werden protokolliert und NICHT
ueberschrieben, Lockfile, temporaere Datei + fsync + os.replace. Provenance je Batch in provenance.jsonl.
Status in last_run_status.json, Exit-Code 1 bei jedem Quellenfehler, 2 bei Lock-Konflikt.
"""
import argparse, concurrent.futures as cf, csv, datetime as dt, fcntl, hashlib, io, json, logging, math, os, re, socket, ssl, sys, time, traceback, urllib.error, urllib.parse, urllib.request, uuid, zipfile

VERSION = "1.1"
OUT = os.path.abspath(os.environ.get("AURUM_DATA_LIVE", "/workspace/aurum2/data_live"))
UA = "aurum2-collector/1.1 (public market data, research)"
TIMEOUT = 30

KRAKEN_FUT = ["PF_ADAUSD", "PF_AVAXUSD", "PF_BNBUSD", "PF_DOTUSD", "PF_ETHUSD", "PF_LINKUSD", "PF_LTCUSD", "PF_SOLUSD",
              "PF_XBTUSD", "PF_XRPUSD", "PI_BCHUSD", "PI_ETHUSD", "PI_LTCUSD", "PI_XBTUSD", "PI_XRPUSD"]
KRAKEN_DEAD_OK = {"PI_BCHUSD"}  # seit 2025-04 ohne neue Raten, leer = Warnung, kein Fehler
# Dateiname wie 02_daten/raw/kraken_api (BTCUSD), API-Paar XBTUSD
KRAKEN_PAIRS = {"BTCUSD": "XBTUSD", "ETHUSD": "ETHUSD", "SOLUSD": "SOLUSD", "XRPUSD": "XRPUSD", "ADAUSD": "ADAUSD",
                "AVAXUSD": "AVAXUSD", "BNBUSD": "BNBUSD", "DOTUSD": "DOTUSD", "LINKUSD": "LINKUSD", "LTCUSD": "LTCUSD"}
KRAKEN_TF = {"1h": 60, "4h": 240, "1d": 1440}
BINANCE_SYMS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "AVAXUSDT", "BNBUSDT", "DOTUSDT", "LINKUSDT", "LTCUSDT"]
BV = "https://data.binance.vision"
BV_S3 = "https://s3-ap-northeast-1.amazonaws.com/data.binance.vision"

log = logging.getLogger("collector")


# ------------------------------------------------------------------ Hilfen
def utcnow():
    return dt.datetime.now(dt.timezone.utc)


def iso(ts):
    return ts.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(s):
    s = s.strip().replace("Z", "+00:00")
    t = dt.datetime.fromisoformat(s)
    if t.tzinfo is None:
        raise ValueError(f"Zeitstempel ohne Zone: {s}")
    return t.astimezone(dt.timezone.utc)


class HttpError(Exception):
    def __init__(self, code, url, msg=""):
        super().__init__(f"HTTP {code} {url} {msg}".strip()); self.code = code


def http(url, method="GET", retries=4, backoff=2.0):
    """GET/HEAD mit Retries (Netzfehler, 429, 5xx). 4xx ausser 429 sofort als HttpError (404 = nicht vorhanden)."""
    last = None
    for a in range(retries + 1):
        try:
            req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return r.status, r.read() if method == "GET" else b""
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                last = HttpError(e.code, url)
                ra = e.headers.get("Retry-After") if e.headers else None
                wait = float(ra) if ra and ra.isdigit() else backoff * 2 ** a
            else:
                raise HttpError(e.code, url)
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, ssl.SSLError) as e:
            last = e; wait = backoff * 2 ** a
        if a < retries:
            log.debug("Retry %d fuer %s in %.1fs (%s)", a + 1, url, wait, last)
            time.sleep(min(wait, 60))
    raise last


def sha256b(b):
    return hashlib.sha256(b).hexdigest()


# ------------------------------------------------------------------ Speicher (append-only)
class Store:
    def __init__(self, run_id, prov):
        self.run_id = run_id; self.prov = prov

    @staticmethod
    def read(path):
        if not os.path.exists(path):
            return None, {}
        with open(path, newline="") as fh:
            rd = csv.reader(fh); hdr = next(rd)
            return hdr, {r[0]: r for r in rd if r}

    def quarantine(self, name, header, rows, reasons):
        q = os.path.join(OUT, "_quarantine"); os.makedirs(q, exist_ok=True)
        base = os.path.join(q, f"{name.replace('/', '__')}_{self.run_id}")
        with open(base + ".csv", "w", newline="") as fh:
            w = csv.writer(fh); w.writerow(header); w.writerows(rows)
        with open(base + ".reason.txt", "w") as fh:
            fh.write("\n".join(reasons) + "\n")
        log.error("QUARANTAENE %s: %d Zeilen, %d kritische Defekte, z.B. %s", name, len(rows), len(reasons), reasons[:3])

    def append(self, rel, header, rows, validate, source, meta):
        """rows: Liste von Listen (Strings), Spalte 0 = Schluessel (ISO-Zeit). Rueckgabe dict mit Zaehlern."""
        path = os.path.join(OUT, rel); os.makedirs(os.path.dirname(path), exist_ok=True)
        crit = validate(rows)
        if crit:
            self.quarantine(rel, header, rows, crit)
            self.prov.write(dict(event="quarantine", file=rel, source=source, rows=len(rows), reasons=crit[:20], **meta))
            raise ValueError(f"{rel}: Batch mit {len(crit)} kritischen Defekten quarantaenisiert")
        os.makedirs(os.path.join(OUT, ".locks"), exist_ok=True)
        with open(os.path.join(OUT, ".locks", rel.replace("/", "__") + ".lock"), "w") as lk:
            fcntl.flock(lk, fcntl.LOCK_EX)
            hdr, have = self.read(path)
            if hdr is not None and hdr != header:
                raise ValueError(f"{rel}: Header {hdr} != {header}")
            new, conflicts, same = [], [], 0
            seen = set()
            for r in rows:
                k = r[0]
                if k in seen:
                    continue
                seen.add(k)
                if k in have:
                    if have[k] == r:
                        same += 1
                    elif _numeq(have[k], r):
                        same += 1
                    else:
                        conflicts.append(dict(key=k, stored=have[k], incoming=r))
                else:
                    new.append(r)
            if new:
                last = max(have) if have else None
                late = [r for r in new if last is not None and r[0] < last]
                allrows = list(have.values()) + new
                allrows.sort(key=lambda r: r[0])
                if late:
                    log.warning("%s: %d neue Zeilen liegen vor dem bisherigen Ende (Luecke gefuellt)", rel, len(late))
                buf = io.StringIO(); w = csv.writer(buf, lineterminator="\n"); w.writerow(header); w.writerows(allrows)
                data = buf.getvalue().encode()
                if os.path.exists(path):  # append-only: bestehende Bytes muessen Praefix bleiben, sofern nichts eingefuegt wurde
                    old = open(path, "rb").read()
                    if not late and not data.startswith(old):
                        raise ValueError(f"{rel}: append-only verletzt (bestehende Bytes wuerden veraendert)")
                tmp = f"{path}.tmp.{os.getpid()}"
                with open(tmp, "wb") as fh:
                    fh.write(data); fh.flush(); os.fsync(fh.fileno())
                os.replace(tmp, path)
                dfd = os.open(os.path.dirname(path), os.O_RDONLY); os.fsync(dfd); os.close(dfd)
            if conflicts:
                known = self.known_conflicts()
                fresh = [c for c in conflicts if (rel, c["key"], json.dumps(c["incoming"])) not in known]
                with open(os.path.join(OUT, "conflicts.jsonl"), "a") as fh:
                    for c in fresh:
                        known.add((rel, c["key"], json.dumps(c["incoming"])))
                        fh.write(json.dumps(dict(run_id=self.run_id, file=rel, **c)) + "\n")
                log.warning("%s: %d Konflikte, davon %d neu protokolliert (nicht ueberschrieben, siehe conflicts.jsonl)", rel, len(conflicts), len(fresh))
            total = len(have) + len(new)
            keys = sorted(list(have) + [r[0] for r in new])
        res = dict(file=rel, fetched=len(rows), new=len(new), unchanged=same, conflicts=len(conflicts), total=total,
                   first=keys[0] if keys else None, last=keys[-1] if keys else None,
                   new_first=min((r[0] for r in new), default=None), new_last=max((r[0] for r in new), default=None))
        self.prov.write(dict(event="append", source=source, **res, **meta))
        log.info("%s [%s]: geholt %d, neu %d, unveraendert %d, Konflikte %d, total %d (%s .. %s)", rel, source, res["fetched"], res["new"],
                 res["unchanged"], res["conflicts"], res["total"], res["first"], res["last"])
        return res

    def known_conflicts(self):
        if not hasattr(self, "_kc"):
            self._kc = set(); p = os.path.join(OUT, "conflicts.jsonl")
            if os.path.exists(p):
                for line in open(p):
                    d = json.loads(line); self._kc.add((d["file"], d["key"], json.dumps(d["incoming"])))
        return self._kc


def _numeq(a, b):
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if x == y:
            continue
        try:
            fx, fy = float(x), float(y)
        except ValueError:
            return False
        if not (fx == fy or (math.isfinite(fx) and abs(fx - fy) <= 1e-12 * max(1.0, abs(fx)))):
            return False
    return True


class Prov:
    def __init__(self, run_id):
        self.path = os.path.join(OUT, "provenance.jsonl"); self.run_id = run_id

    def write(self, d):
        with open(self.path, "a") as fh:
            fh.write(json.dumps(dict(ts=iso(utcnow()), run_id=self.run_id, collector=VERSION, **d), default=str) + "\n")


# ------------------------------------------------------------------ Validierung
def _time_checks(rows, crit):
    prev = None
    for i, r in enumerate(rows):
        try:
            t = parse_iso(r[0])
            if iso(t) != r[0]:
                crit.append(f"Zeile {i}: Zeitformat {r[0]}")
        except Exception:
            crit.append(f"Zeile {i}: ungueltiges Datum {r[0]!r}"); continue
        if prev is not None and r[0] <= prev:
            crit.append(f"Zeile {i}: Zeitachse nicht monoton/Duplikat {r[0]} nach {prev}")
        prev = r[0]
        if t > utcnow() + dt.timedelta(minutes=5):
            crit.append(f"Zeile {i}: Zeit in der Zukunft {r[0]}")


def validate_ohlc(rows):
    crit = []; _time_checks(rows, crit)
    for i, r in enumerate(rows):
        try:
            o, h, l, c, v = map(float, r[1:6]); n = int(r[6])
        except Exception:
            crit.append(f"Zeile {i}: fehlender/ungueltiger Wert {r}"); continue
        if min(o, h, l, c) <= 0 or not all(map(math.isfinite, (o, h, l, c, v))):
            crit.append(f"Zeile {i}: nicht positive Kurse {r}")
        if not (l <= min(o, c) and max(o, c) <= h):
            crit.append(f"Zeile {i}: Open/Close ausserhalb Hoch-Tief {r}")
        if v < 0 or n < 0:
            crit.append(f"Zeile {i}: negatives Volumen/Trades {r}")
    return crit


def validate_funding(cols_float):
    def v(rows):
        crit = []; _time_checks(rows, crit)
        for i, r in enumerate(rows):
            try:
                xs = [float(r[j]) for j in cols_float]
            except Exception:
                crit.append(f"Zeile {i}: fehlender/ungueltiger Wert {r}"); continue
            if not all(map(math.isfinite, xs)):
                crit.append(f"Zeile {i}: nicht endlich {r}")
        return crit
    return v


def validate_rel_funding(rows):
    crit = validate_funding([1, 2])(rows)
    for i, r in enumerate(rows):
        try:
            if abs(float(r[2])) > 0.05:  # 5 % je Stunde waere absurd
                crit.append(f"Zeile {i}: relativeFundingRate unplausibel {r[2]}")
        except Exception:
            pass
    return crit


def validate_binance_funding(rows):
    crit = validate_funding([1])(rows)
    for i, r in enumerate(rows):
        try:
            if abs(float(r[1])) > 0.05 or int(r[2]) not in (1, 2, 4, 8):
                crit.append(f"Zeile {i}: unplausibel {r}")
        except Exception:
            crit.append(f"Zeile {i}: ungueltig {r}")
    return crit


# ------------------------------------------------------------------ Quellen
def src_kraken_funding(store, args):
    res, errs = {}, []
    for sym in KRAKEN_FUT:
        url = f"https://futures.kraken.com/derivatives/api/v4/historicalfundingrates?symbol={sym}"
        try:
            st, body = http(url); d = json.loads(body)
            if d.get("result") != "success":
                raise ValueError(f"result={d.get('result')} {str(d)[:200]}")
            rows = [[iso(parse_iso(x["timestamp"])), repr(float(x["fundingRate"])), repr(float(x["relativeFundingRate"]))] for x in d.get("rates", [])]
            rows.sort(key=lambda r: r[0])
            if not rows:
                if sym in KRAKEN_DEAD_OK:
                    log.warning("%s: keine Raten (bekannt inaktiv)", sym); res[sym] = dict(new=0, note="inaktiv, leer"); continue
                raise ValueError("leere Antwort")
            res[sym] = store.append(f"kraken_futures_funding/{sym}.csv", ["t", "fundingRate", "relativeFundingRate"], rows,
                                    validate_rel_funding, "kraken_futures_funding",
                                    dict(url=url, http=st, sha256=sha256b(body), server_time=d.get("serverTime")))
        except Exception as e:
            errs.append(f"{sym}: {e}"); log.error("kraken_futures_funding %s: %s", sym, e)
    return res, errs


def src_kraken_ohlc(store, args):
    res, errs = {}, []
    for name, pair in KRAKEN_PAIRS.items():
        for tf, minutes in KRAKEN_TF.items():
            url = f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval={minutes}"
            key = f"{name}_{tf}"
            try:
                st, body = http(url); d = json.loads(body)
                if d.get("error"):
                    raise ValueError(f"API-Fehler {d['error']}")
                series = [v for k, v in d["result"].items() if k != "last"]
                if len(series) != 1:
                    raise ValueError(f"unerwartete Antwort {list(d['result'])}")
                now = time.time(); rows = []; dropped = 0
                for b in series[0]:
                    t0 = int(b[0])
                    if t0 + minutes * 60 > now:  # laufender Bar wird nie herausgegeben
                        dropped += 1; continue
                    rows.append([iso(dt.datetime.fromtimestamp(t0, dt.timezone.utc)), b[1], b[2], b[3], b[4], b[6], str(int(b[7]))])
                res[key] = store.append(f"kraken_ohlc/{key}.csv", ["t", "open", "high", "low", "close", "volume", "trades"], rows,
                                        validate_ohlc, "kraken_ohlc",
                                        dict(url=url, http=st, sha256=sha256b(body), dropped_open_bars=dropped, kraken_last=d["result"].get("last")))
            except Exception as e:
                errs.append(f"{key}: {e}"); log.error("kraken_ohlc %s: %s", key, e)
            time.sleep(1.1)  # Kraken public rate limit
    return res, errs


def _months(start, end):
    y, m = start
    while (y, m) <= end:
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def src_binance_funding(store, args):
    res, errs = {}, []
    today = utcnow().date(); cur = (today.year, today.month)
    for sym in BINANCE_SYMS:
        rel = f"binance_funding/{sym}_funding.csv"
        hdr, have = Store.read(os.path.join(OUT, rel))
        if have:
            last = parse_iso(max(have)); start = (last.year, last.month)
        else:
            start = (2020, 1)
        per = dict(months=[], missing=[])
        try:
            for y, m in _months(start, cur):
                base = f"{BV}/data/futures/um/monthly/fundingRate/{sym}/{sym}-fundingRate-{y:04d}-{m:02d}.zip"
                try:
                    st, z = http(base)
                except HttpError as e:
                    if e.code == 404:
                        per["missing"].append(f"{y:04d}-{m:02d}"); continue
                    raise
                _, ck = http(base + ".CHECKSUM")
                exp = ck.decode().split()[0]
                if sha256b(z) != exp:
                    raise ValueError(f"CHECKSUM falsch fuer {base}")
                zf = zipfile.ZipFile(io.BytesIO(z)); txt = zf.read(zf.namelist()[0]).decode()
                rows = []
                for r in csv.DictReader(io.StringIO(txt)):
                    ms = int(r["calc_time"])
                    rows.append([iso(dt.datetime.fromtimestamp(ms // 1000, dt.timezone.utc)), r["last_funding_rate"], str(int(r["funding_interval_hours"])), str(ms)])
                rows.sort(key=lambda r: r[0])
                rr = store.append(rel, ["t", "rate", "interval_hours", "calc_time_ms"], rows, validate_binance_funding, "binance_funding",
                                  dict(url=base, http=st, sha256=exp, checksum_ok=True, month=f"{y:04d}-{m:02d}"))
                per["months"].append(dict(month=f"{y:04d}-{m:02d}", new=rr["new"], conflicts=rr["conflicts"]))
                per.update(total=rr["total"], first=rr["first"], last=rr["last"])
            res[sym] = per
            # Verzug: Monat vor dem aktuellen muss spaetestens ab dem 5. vorhanden sein
            prev = (cur[0] - 1, 12) if cur[1] == 1 else (cur[0], cur[1] - 1)
            if today.day >= 5 and f"{prev[0]:04d}-{prev[1]:02d}" in per["missing"]:
                raise ValueError(f"Vormonat {prev} noch nicht publiziert")
        except Exception as e:
            errs.append(f"{sym}: {e}"); log.error("binance_funding %s: %s", sym, e)
    return res, errs


def _s3_list(prefix):
    out, marker = [], ""
    while True:
        url = f"{BV_S3}?delimiter=/&prefix={urllib.parse.quote(prefix)}" + (f"&marker={urllib.parse.quote(marker)}" if marker else "")
        _, body = http(url); txt = body.decode()
        ps = re.findall(r"<Prefix>([^<]+)</Prefix>", txt)
        out += [p for p in ps if p != prefix]
        if "<IsTruncated>true</IsTruncated>" not in txt:
            return out
        nm = re.search(r"<NextMarker>([^<]+)</NextMarker>", txt)
        marker = nm.group(1) if nm else ps[-1]


def src_binance_universe(store, args):
    errs = []
    prefix = "data/futures/um/daily/klines/"
    syms = sorted(p[len(prefix):].strip("/") for p in _s3_list(prefix))
    if len(syms) < 300:
        raise ValueError(f"Universum unplausibel klein: {len(syms)}")
    today = utcnow().date(); d1, d2 = today - dt.timedelta(days=1), today - dt.timedelta(days=2)

    def probe(s):
        for d in (d1, d2):
            q = urllib.parse.quote(s)  # es gibt Symbole mit Nicht-ASCII-Zeichen
            u = f"{BV}/data/futures/um/daily/klines/{q}/1d/{q}-1d-{d.isoformat()}.zip"
            try:
                http(u, method="HEAD", retries=2); return s, d.isoformat()
            except HttpError as e:
                if e.code != 404:
                    raise
        return s, ""

    with cf.ThreadPoolExecutor(24) as ex:
        probes = dict(ex.map(probe, syms))
    snap_date = today.isoformat()
    d = os.path.join(OUT, "binance_universe"); os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f"snapshot_{snap_date}.csv")
    rows = [[s, "1" if probes[s] else "0", probes[s]] for s in syms]
    buf = io.StringIO(); w = csv.writer(buf, lineterminator="\n"); w.writerow(["symbol", "active_proxy", "last_daily_kline"]); w.writerows(rows)
    data = buf.getvalue().encode()
    if os.path.exists(path) and open(path, "rb").read() != data:
        path = path.replace(".csv", f"_{store.run_id}.csv")  # nie ueberschreiben
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data); fh.flush(); os.fsync(fh.fileno())
    os.replace(tmp, path)
    # first_seen-Register (append-only): neue Symbole im Listing
    reg_rel = "binance_universe/first_seen.csv"
    _, have = Store.read(os.path.join(OUT, reg_rel))
    newsyms = [s for s in syms if s not in have]
    if newsyms:
        hdr = ["symbol", "first_seen_snapshot", "active_proxy_then"]
        allr = list(have.values()) + [[s, snap_date, rows[syms.index(s)][1]] for s in newsyms]
        allr.sort(key=lambda r: r[0])
        p = os.path.join(OUT, reg_rel); buf = io.StringIO(); w = csv.writer(buf, lineterminator="\n"); w.writerow(hdr); w.writerows(allr)
        with open(p + ".tmp", "wb") as fh:
            fh.write(buf.getvalue().encode()); fh.flush(); os.fsync(fh.fileno())
        os.replace(p + ".tmp", p)
    gone = [s for s in have if s not in syms]
    n_act = sum(1 for r in rows if r[1] == "1")
    res = dict(file=os.path.relpath(path, OUT), symbols=len(syms), active_proxy=n_act, inactive_proxy=len(syms) - n_act,
               new_in_listing=len(newsyms) if have else 0, first_snapshot=not have, vanished_from_listing=gone, probe_dates=[d1.isoformat(), d2.isoformat()])
    store.prov.write(dict(event="snapshot", source="binance_universe", url=f"{BV_S3}?prefix={prefix}", sha256=sha256b(data), **res))
    return res, errs


# ------------------------------------------------------------------ Kraken Futures Instrumente + Ticker (ab 1.1, XS21-Gate M3)
KFT_HDR = ["t", "tradeable", "suspended", "vol24h_usd", "vol24h_base", "open_interest", "last", "last_time", "mark_price", "opening_date"]
KST_HDR = ["t", "last", "vol24h_base", "vwap24h", "vol24h_usd", "trades24h"]
_EXPIRY = re.compile(r"_\d{6}$")


def _num(x):
    return "" if x is None else repr(float(x))


def _flag(x):
    return "" if x is None else ("1" if x else "0")


def validate_ticker(nonneg, pos, opt_pos=(), flags=()):
    def v(rows):
        crit = []; _time_checks(rows, crit)
        for i, r in enumerate(rows):
            try:
                for j in nonneg:
                    x = float(r[j])
                    if not math.isfinite(x) or x < 0:
                        crit.append(f"Zeile {i}: Spalte {j} negativ/nicht endlich {r}")
                for j in pos:
                    x = float(r[j])
                    if not math.isfinite(x) or x <= 0:
                        crit.append(f"Zeile {i}: Spalte {j} nicht positiv {r}")
                for j in opt_pos:  # leer erlaubt (z.B. nie gehandelt)
                    if r[j] != "" and not (math.isfinite(float(r[j])) and float(r[j]) > 0):
                        crit.append(f"Zeile {i}: Spalte {j} nicht positiv {r}")
                for j in flags:
                    if r[j] not in ("0", "1", ""):
                        crit.append(f"Zeile {i}: Flag {r[j]!r}")
            except (ValueError, IndexError):
                crit.append(f"Zeile {i}: fehlender/ungueltiger Wert {r}")
        return crit
    return v


validate_kft = validate_ticker(nonneg=[3, 4, 5], pos=[], opt_pos=[6, 8], flags=[1, 2])
validate_kst = validate_ticker(nonneg=[2, 4, 5], pos=[1, 3])


def _write_snapshot(store, sub, snap_date, header, rows):
    """Tages-Snapshot nie ueberschreiben (abweichender Inhalt -> Datei mit run_id). Rueckgabe relativer Pfad, sha256."""
    d = os.path.join(OUT, sub); os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f"snapshot_{snap_date}.csv")
    buf = io.StringIO(); w = csv.writer(buf, lineterminator="\n"); w.writerow(header); w.writerows(rows)
    data = buf.getvalue().encode()
    if os.path.exists(path):
        if open(path, "rb").read() == data:
            return os.path.relpath(path, OUT), sha256b(data)
        path = path.replace(".csv", f"_{store.run_id}.csv")
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data); fh.flush(); os.fsync(fh.fileno())
    os.replace(tmp, path)
    return os.path.relpath(path, OUT), sha256b(data)


def _first_seen(sub, syms, snap_date):
    """append-only Register: Symbol, erster Snapshot. Rueckgabe (neu, verschwunden)."""
    rel = f"{sub}/first_seen.csv"; p = os.path.join(OUT, rel)
    _, have = Store.read(p)
    new = [s for s in syms if s not in have]
    if new:
        allr = list(have.values()) + [[s, snap_date] for s in new]; allr.sort(key=lambda r: r[0])
        buf = io.StringIO(); w = csv.writer(buf, lineterminator="\n"); w.writerow(["symbol", "first_seen_snapshot"]); w.writerows(allr)
        with open(p + ".tmp", "wb") as fh:
            fh.write(buf.getvalue().encode()); fh.flush(); os.fsync(fh.fileno())
        os.replace(p + ".tmp", p)
    return (new if have else []), [s for s in have if s not in set(syms)]


def src_kraken_futures_tickers(store, args):
    res, errs = {}, []
    ui = "https://futures.kraken.com/derivatives/api/v3/instruments"
    ut = "https://futures.kraken.com/derivatives/api/v3/tickers"
    sti, bi = http(ui); di = json.loads(bi)
    stt, bt = http(ut); dt_ = json.loads(bt)
    for name, d in (("instruments", di), ("tickers", dt_)):
        if d.get("result") != "success":
            raise ValueError(f"{name}: result={d.get('result')} {str(d)[:200]}")
    inst = {x["symbol"]: x for x in di.get("instruments", [])
            if x.get("symbol", "")[:3] in ("PF_", "PI_") and not _EXPIRY.search(x["symbol"])}
    tick = {x["symbol"]: x for x in dt_.get("tickers", []) if x.get("tag") == "perpetual"}
    if len(inst) < 50 or len(tick) < 50:
        raise ValueError(f"unplausibel wenige Perpetuals: instruments {len(inst)}, tickers {len(tick)}")
    t_snap = iso(parse_iso(dt_["serverTime"]).replace(microsecond=0))
    snap_date = t_snap[:10]
    irows = [[s, x.get("type", ""), _flag(x.get("tradeable")), x.get("base", ""), x.get("quote", ""), x.get("openingDate", "")]
             for s, x in sorted(inst.items())]
    ifile, isha = _write_snapshot(store, "kraken_futures_instruments", f"{snap_date}", ["symbol", "type", "tradeable", "base", "quote", "opening_date"], irows)
    new, gone = _first_seen("kraken_futures_instruments", sorted(inst), snap_date)
    store.prov.write(dict(event="snapshot", source="kraken_futures_instruments", url=ui, http=sti, sha256=sha256b(bi), file=ifile,
                          file_sha256=isha, instruments=len(inst), server_time=di.get("serverTime"), new_in_listing=new, vanished_from_listing=gone))
    res["_instruments"] = dict(file=ifile, perpetuals=len(inst), tradeable=sum(1 for r in irows if r[2] == "1"), new_in_listing=new, vanished=gone)
    meta = dict(url=ut, http=stt, sha256=sha256b(bt), server_time=dt_.get("serverTime"), instruments_sha256=sha256b(bi))
    n_ok = 0
    for s in sorted(set(inst) | set(tick)):
        x, i = tick.get(s), inst.get(s, {})
        try:
            if x is None:  # Instrument ohne Ticker: nur Flag, keine Werte -> kein Zeileneintrag, Warnung
                log.warning("kraken_futures_tickers %s: Instrument ohne Ticker", s); res[s] = dict(note="ohne Ticker"); continue
            row = [t_snap, _flag(i.get("tradeable")), _flag(x.get("suspended")), _num(x.get("volumeQuote")), _num(x.get("vol24h")),
                   _num(x.get("openInterest")), _num(x.get("last")), x.get("lastTime") or "", _num(x.get("markPrice")), i.get("openingDate", "")]
            r = store.append(f"kraken_futures_tickers/{s}.csv", KFT_HDR, [row], validate_kft, "kraken_futures_tickers", meta)
            res[s] = dict(new=r["new"], total=r["total"]); n_ok += 1
        except Exception as e:
            errs.append(f"{s}: {e}"); log.error("kraken_futures_tickers %s: %s", s, e)
    res["_summary"] = dict(t=t_snap, symbols_written=n_ok, ge_2m_usd=sum(1 for x in tick.values() if (x.get("volumeQuote") or 0) >= 2e6))
    return res, errs


def src_kraken_spot_tickers(store, args):
    res, errs = {}, []
    for name, pair in KRAKEN_PAIRS.items():
        url = f"https://api.kraken.com/0/public/Ticker?pair={pair}"
        try:
            t = iso(utcnow().replace(microsecond=0))
            st, body = http(url); d = json.loads(body)
            if d.get("error"):
                raise ValueError(f"API-Fehler {d['error']}")
            vals = list(d["result"].values())
            if len(vals) != 1:
                raise ValueError(f"unerwartete Antwort {list(d['result'])}")
            v = vals[0]; vol, vwap = float(v["v"][1]), float(v["p"][1])
            row = [t, _num(v["c"][0]), _num(vol), _num(vwap), _num(vol * vwap), str(int(v["t"][1]))]
            r = store.append(f"kraken_spot_tickers/{name}.csv", KST_HDR, [row], validate_kst, "kraken_spot_tickers",
                             dict(url=url, http=st, sha256=sha256b(body), kraken_key=list(d["result"])[0]))
            res[name] = dict(new=r["new"], total=r["total"], vol24h_usd=round(vol * vwap))
        except Exception as e:
            errs.append(f"{name}: {e}"); log.error("kraken_spot_tickers %s: %s", name, e)
        time.sleep(1.1)
    return res, errs


SOURCES = {"kraken_futures_funding": src_kraken_funding, "kraken_ohlc": src_kraken_ohlc,
           "binance_funding": src_binance_funding, "binance_universe": src_binance_universe,
           "kraken_futures_tickers": src_kraken_futures_tickers, "kraken_spot_tickers": src_kraken_spot_tickers}


# ------------------------------------------------------------------ Seed aus 02_daten/raw (einmalig)
def seed(store, raw):
    """Uebernimmt die vorhandene Projekt-Historie einmalig (Provenance 'seed'). Normalisiert Zeitformat auf ...Z."""
    out = {}
    def norm(rows):  # kraken_api/*_1d.csv traegt nur das Datum (= Bar-Beginn 00:00 UTC)
        return [[iso(parse_iso(r[0] + "T00:00:00Z" if len(r[0]) == 10 else r[0]))] + r[1:] for r in rows]
    for sym in KRAKEN_FUT:
        p = os.path.join(raw, "kraken_futures_funding", f"{sym}.csv")
        if os.path.exists(p):
            _, d = Store.read(p); rows = sorted(norm(list(d.values())))
            out[sym] = store.append(f"kraken_futures_funding/{sym}.csv", ["t", "fundingRate", "relativeFundingRate"], rows,
                                    validate_rel_funding, "seed", dict(seed_file=p, sha256=_fsha(p)))
    for name in KRAKEN_PAIRS:
        for tf in KRAKEN_TF:
            p = os.path.join(raw, "kraken_api", f"{name}_{tf}.csv")
            if os.path.exists(p):
                _, d = Store.read(p); rows = sorted(norm(list(d.values())))
                out[f"{name}_{tf}"] = store.append(f"kraken_ohlc/{name}_{tf}.csv", ["t", "open", "high", "low", "close", "volume", "trades"],
                                                   rows, validate_ohlc, "seed", dict(seed_file=p, sha256=_fsha(p)))
    for sym in BINANCE_SYMS:
        p = os.path.join(raw, "binance_funding", f"{sym}_funding.csv")
        if os.path.exists(p):
            _, d = Store.read(p); rows = []
            for r in d.values():
                t = parse_iso(r[0]); ms = int(round(t.timestamp() * 1000))
                rows.append([iso(t.replace(microsecond=0)), r[1], str(int(r[2])), str(ms)])
            rows.sort()
            out[sym] = store.append(f"binance_funding/{sym}_funding.csv", ["t", "rate", "interval_hours", "calc_time_ms"], rows,
                                    validate_binance_funding, "seed", dict(seed_file=p, sha256=_fsha(p)))
    return out


def _fsha(p):
    return sha256b(open(p, "rb").read())


# ------------------------------------------------------------------ Hauptlauf
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", choices=list(SOURCES))
    ap.add_argument("--seed-from", help="einmalig Historie aus 02_daten/raw uebernehmen")
    args = ap.parse_args()
    os.makedirs(os.path.join(OUT, "logs"), exist_ok=True)
    started = utcnow(); run_id = started.strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:6]
    logfile = os.path.join(OUT, "logs", f"collect_{started.astimezone().strftime('%Y-%m-%d')}.log")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[logging.FileHandler(logfile), logging.StreamHandler(sys.stdout)])
    lk = open(os.path.join(OUT, ".collector.lock"), "w")
    try:
        fcntl.flock(lk, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        log.error("Ein anderer Collector-Lauf ist aktiv (Lock). Abbruch."); return 2
    prov = Prov(run_id); store = Store(run_id, prov)
    log.info("Start run_id=%s OUT=%s", run_id, OUT)
    status = dict(run_id=run_id, collector_version=VERSION, host=socket.gethostname(), started_utc=iso(started),
                  started_local=started.astimezone().isoformat(timespec="seconds"), sources={}, errors=[])
    if args.seed_from:
        try:
            status["seed"] = {k: dict(new=v["new"], total=v["total"], conflicts=v["conflicts"]) for k, v in seed(store, args.seed_from).items()}
        except Exception as e:
            status["errors"].append(f"seed: {e}"); log.error("seed: %s", traceback.format_exc())
    for name in (args.only or SOURCES):
        t0 = time.time()
        try:
            res, errs = SOURCES[name](store, args)
            ok = not errs
            status["sources"][name] = dict(ok=ok, seconds=round(time.time() - t0, 1), errors=errs, result=res)
            status["errors"] += [f"{name}: {e}" for e in errs]
        except Exception as e:
            log.error("%s: %s", name, traceback.format_exc())
            status["sources"][name] = dict(ok=False, seconds=round(time.time() - t0, 1), errors=[str(e)])
            status["errors"].append(f"{name}: {e}")
    fin = utcnow()
    status.update(finished_utc=iso(fin), finished_local=fin.astimezone().isoformat(timespec="seconds"),
                  seconds=round((fin - started).total_seconds(), 1), ok=not status["errors"], logfile=logfile)
    tmp = os.path.join(OUT, "last_run_status.json.tmp")
    with open(tmp, "w") as fh:
        json.dump(status, fh, indent=1, default=str); fh.flush(); os.fsync(fh.fileno())
    os.replace(tmp, os.path.join(OUT, "last_run_status.json"))
    with open(os.path.join(OUT, "run_history.jsonl"), "a") as fh:
        fh.write(json.dumps(dict(run_id=run_id, started_utc=status["started_utc"], seconds=status["seconds"], ok=status["ok"],
                                 errors=status["errors"][:20])) + "\n")
    prov.write(dict(event="run_end", ok=status["ok"], errors=len(status["errors"])))
    log.info("Ende run_id=%s ok=%s Fehler=%d Dauer=%ss", run_id, status["ok"], len(status["errors"]), status["seconds"])
    return 0 if status["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
