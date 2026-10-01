"""Aurum II Collector 1.2: Makro- und On-Chain-Quellen fuer die Sleeves A (MAKRO_LIQ) und B (MVRV).

Nur oeffentliche Daten ohne Key. Massgebend ist je Beobachtung der Wert beim ERSTEN Abruf (First-Release):
  - neue Beobachtung -> Zeile [obs_date, value, first_fetch_utc, run_id, initial_load] wird angehaengt
  - bekannte Beobachtung mit anderem Wert -> Revision in macro/revisions.jsonl protokolliert, Datei NICHT geaendert
  - jede Rohantwort wird mit SHA256 unter macro/_raw/<quelle>/ abgelegt (nie ueberschrieben)
Quellen
  coinmetrics_mvrv  community-api.coinmetrics.io v4 asset-metrics btc CapMVRVCur 1d, letzte 30 Tage
  fred_macro        fred.stlouisfed.org/graph/fredgraph.csv (ohne Key) WALCL, WTREGEN, RRPONTSYD, DTB3, letzte 200 Tage
Hinweis: FRED beantwortet Anfragen mit eigenem User-Agent nicht (Timeout, getestet 01.10.2026); fuer FRED wird der
Standard-User-Agent von Python-urllib verwendet.
"""
import csv, datetime as dt, fcntl, io, json, math, os, urllib.request

MACRO = "macro"
HDR = ["obs_date", "value", "first_fetch_utc", "run_id", "initial_load"]
CM_URL = ("https://community-api.coinmetrics.io/v4/timeseries/asset-metrics?assets=btc&metrics=CapMVRVCur"
          "&frequency=1d&page_size=1000&start_time={start}")
FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&cosd={start}"
CM_DAYS, FRED_DAYS = 30, 200
# Plausibilitaet (Einheiten wie FRED: WALCL/WTREGEN Mio. USD, RRPONTSYD Mrd. USD, DTB3 % p. a.)
BOUNDS = {"CapMVRVCur": (0.1, 20.0), "WALCL": (1e6, 2e7), "WTREGEN": (0.0, 3e6), "RRPONTSYD": (0.0, 5000.0), "DTB3": (-1.0, 25.0)}
FRED_SERIES = ["WALCL", "WTREGEN", "RRPONTSYD", "DTB3"]


def _C():
    import collect as C  # zur Laufzeit, damit Tests C.OUT umbiegen koennen
    return C


def _raw_store(source, run_id, ext, body):
    C = _C(); d = os.path.join(C.OUT, MACRO, "_raw", source); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, f"{run_id}.{ext}")
    with open(p + ".tmp", "wb") as fh:
        fh.write(body); fh.flush(); os.fsync(fh.fileno())
    os.replace(p + ".tmp", p)
    return os.path.relpath(p, C.OUT), C.sha256b(body)


def validate_obs(series, obs, today):
    """obs: Liste (obs_date 'YYYY-MM-DD', value-String). Rueckgabe Liste kritischer Defekte."""
    lo, hi = BOUNDS[series]; crit = []; prev = None
    for i, (d, v) in enumerate(obs):
        try:
            day = dt.date.fromisoformat(d)
        except ValueError:
            crit.append(f"Zeile {i}: Datum {d!r}"); continue
        if len(d) != 10 or day > today:
            crit.append(f"Zeile {i}: Datum unplausibel {d}")
        if prev is not None and d <= prev:
            crit.append(f"Zeile {i}: nicht streng monoton {prev} -> {d}")
        prev = d
        try:
            x = float(v)
        except ValueError:
            crit.append(f"Zeile {i}: Wert {v!r}"); continue
        if not math.isfinite(x) or not (lo <= x <= hi):
            crit.append(f"Zeile {i}: Wert ausserhalb [{lo}, {hi}]: {v}")
    return crit


def append_first_release(store, rel, series, obs, fetched_utc, source, meta, today):
    """Haengt nur neue Beobachtungen an (First-Release). Revisionen werden protokolliert, nie ueberschrieben."""
    C = _C()
    crit = validate_obs(series, obs, today)
    if crit:
        store.quarantine(rel, ["obs_date", "value"], [list(o) for o in obs], crit)
        store.prov.write(dict(event="quarantine", file=rel, source=source, rows=len(obs), reasons=crit[:20], **meta))
        raise ValueError(f"{rel}: Batch mit {len(crit)} kritischen Defekten quarantaenisiert")
    path = os.path.join(C.OUT, rel); os.makedirs(os.path.dirname(path), exist_ok=True)
    os.makedirs(os.path.join(C.OUT, ".locks"), exist_ok=True)
    with open(os.path.join(C.OUT, ".locks", rel.replace("/", "__") + ".lock"), "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        hdr, have = C.Store.read(path)
        if hdr is not None and hdr != HDR:
            raise ValueError(f"{rel}: Header {hdr} != {HDR}")
        initial = "1" if hdr is None else "0"
        new, revs, same = [], [], 0
        for d, v in obs:
            if d in have:
                if C._numeq([have[d][1]], [v]):
                    same += 1
                else:
                    revs.append(dict(obs_date=d, first_release=have[d][1], incoming=v))
            else:
                new.append([d, v, fetched_utc, store.run_id, initial])
        late = [r for r in new if have and r[0] < max(have)]
        if late:  # Luecke vor dem bisherigen Ende: als Warnung, Zeilen werden trotzdem angehaengt (Zeitpunkt = jetzt)
            C.log.warning("%s: %d neue Beobachtungen vor dem bisherigen Ende (spaet erschienen)", rel, len(late))
        if new:
            rows = list(have.values()) + new; rows.sort(key=lambda r: r[0])
            buf = io.StringIO(); w = csv.writer(buf, lineterminator="\n"); w.writerow(HDR); w.writerows(rows)
            data = buf.getvalue().encode()
            if os.path.exists(path) and not late and not data.startswith(open(path, "rb").read()):
                raise ValueError(f"{rel}: append-only verletzt")
            tmp = f"{path}.tmp.{os.getpid()}"
            with open(tmp, "wb") as fh:
                fh.write(data); fh.flush(); os.fsync(fh.fileno())
            os.replace(tmp, path)
        if revs:
            seen = set(); rp = os.path.join(C.OUT, MACRO, "revisions.jsonl")
            if os.path.exists(rp):
                for line in open(rp):
                    x = json.loads(line); seen.add((x["file"], x["obs_date"], x["incoming"]))
            with open(rp, "a") as fh:
                for r in revs:
                    if (rel, r["obs_date"], r["incoming"]) not in seen:
                        fh.write(json.dumps(dict(ts=fetched_utc, run_id=store.run_id, file=rel, **r)) + "\n")
            C.log.warning("%s: %d Revisionen (protokolliert, First-Release bleibt)", rel, len(revs))
    res = dict(file=rel, fetched=len(obs), new=len(new), unchanged=same, revisions=len(revs), total=len(have) + len(new),
               last_obs=max([d for d, _ in obs], default=None), initial_load=initial == "1")
    store.prov.write(dict(event="append_first_release", source=source, **res, **meta))
    C.log.info("%s [%s]: geholt %d, neu %d, unveraendert %d, Revisionen %d, letzte Beobachtung %s", rel, source,
               res["fetched"], res["new"], res["unchanged"], res["revisions"], res["last_obs"])
    return res


def parse_coinmetrics(body):
    d = json.loads(body)
    if "data" not in d:
        raise ValueError(f"CoinMetrics: unerwartete Antwort {str(d)[:200]}")
    out = []
    for x in d["data"]:
        if x.get("asset") != "btc" or "CapMVRVCur" not in x:
            raise ValueError(f"CoinMetrics: unerwarteter Datensatz {x}")
        t = x["time"]
        if not t.endswith("Z") or "T00:00:00" not in t:
            raise ValueError(f"CoinMetrics: Zeitstempel {t}")
        out.append((t[:10], x["CapMVRVCur"]))
    if d.get("next_page_token"):
        raise ValueError("CoinMetrics: Antwort paginiert (unerwartet bei 30 Tagen)")
    return out


def parse_fredgraph(series, body):
    rd = csv.reader(io.StringIO(body.decode("utf-8-sig")))
    hdr = next(rd)
    if len(hdr) != 2 or hdr[1] != series:
        raise ValueError(f"FRED {series}: Header {hdr}")
    out, missing = [], 0
    for r in rd:
        if not r:
            continue
        if r[1] in (".", ""):
            missing += 1; continue
        out.append((r[0], r[1]))
    return out, missing


def src_coinmetrics_mvrv(store, args):
    C = _C(); now = C.utcnow().replace(microsecond=0); today = now.date()
    start = (today - dt.timedelta(days=CM_DAYS)).isoformat()
    url = CM_URL.format(start=start)
    st, body = C.http(url)
    raw, sha = _raw_store("coinmetrics_mvrv", store.run_id, "json", body)
    obs = parse_coinmetrics(body)
    if not obs:
        raise ValueError("CoinMetrics: keine Beobachtungen")
    r = append_first_release(store, f"{MACRO}/coinmetrics/btc_CapMVRVCur.csv", "CapMVRVCur", obs, C.iso(now),
                             "coinmetrics_mvrv", dict(url=url, http=st, sha256=sha, raw_file=raw), today)
    return {"btc_CapMVRVCur": r}, []


def _fred_get(url, timeout=60):
    req = urllib.request.Request(url)  # Standard-User-Agent (siehe Modul-Doku)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read()


def src_fred_macro(store, args, getter=None):
    C = _C(); get = getter or _fred_get
    res, errs = {}, []
    for sid in FRED_SERIES:
        try:
            now = C.utcnow().replace(microsecond=0); today = now.date()
            url = FRED_URL.format(sid=sid, start=(today - dt.timedelta(days=FRED_DAYS)).isoformat())
            last = None
            for a in range(3):
                try:
                    st, body = get(url); break
                except Exception as e:  # Netz/Timeout: zwei Wiederholungen
                    last = e
            else:
                raise last
            raw, sha = _raw_store(f"fred_{sid}", store.run_id, "csv", body)
            obs, missing = parse_fredgraph(sid, body)
            if not obs:
                raise ValueError("keine Beobachtungen")
            r = append_first_release(store, f"{MACRO}/fred/{sid}.csv", sid, obs, C.iso(now), "fred_macro",
                                     dict(url=url, http=st, sha256=sha, raw_file=raw, missing_dot=missing), today)
            res[sid] = r
        except Exception as e:
            errs.append(f"{sid}: {e}"); C.log.error("fred_macro %s: %s", sid, e)
    return res, errs
