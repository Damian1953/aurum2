#!/usr/bin/env python3
"""
Project Aurum II — Nachladen der Kurshistorie (Stufe 0, Datenbasis)

Laeuft direkt auf dem Mac im Terminal (nicht in einer Sandbox), weil die
Boersen-Hosts aus der Claude-Umgebung heraus gesperrt sind.

Was das Skript tut
  1. Binance Vision, Spot, Tageskerzen (USDT-Paare), ab 2017-08 bis gestern UTC.
     Lange Historie fuer die Regime-Forschung. Nur abgeschlossene Tage.
  2. Kraken, Spot, Tageskerzen (USD-Paare), die letzten 720 Tage.
     Fuellt die leere Bitcoin-Datei und dient als Gegenprobe zu Binance.
  3. Validiert jeden Datensatz fail-closed, schreibt atomar, protokolliert
     Herkunft mit Pruefsumme. Ein Datensatz mit kritischem Defekt wird
     komplett verworfen und in _quarantine/ abgelegt. Bestehende Dateien
     bleiben dann unveraendert.

Nur Standardbibliothek. Kein pandas noetig.

Aufruf
  python3 nachladen_historie.py            Spot und Kraken nachladen (inkrementell)
  python3 nachladen_historie.py --core     nur BTC, ETH, SOL
  python3 nachladen_historie.py --futures  Binance Perpetuals: Funding-Historie und Perp-Tageskerzen (Stufe 2)
  python3 nachladen_historie.py --oi       Binance Open Interest, Tagesdateien, langsam, unterbrechbar (Stufe 2, D-OI)
  python3 nachladen_historie.py --check    nichts laden, nur vorhandene Dateien pruefen
  python3 nachladen_historie.py --symbols BTCUSDT ETHUSDT   eigene Auswahl (Binance)

Ausgabe
  02_daten/raw/binance/{SYMBOL}_1d.csv           Spot
  02_daten/raw/binance_perp/{SYMBOL}_1d.csv      Perpetual-Tageskerzen
  02_daten/raw/binance_funding/{SYMBOL}_funding.csv   Funding je Zahlungszeitpunkt, relative Rate
  02_daten/raw/binance_oi/{SYMBOL}_oi_1d.csv     Open Interest, letzter Wert je UTC-Tag
  02_daten/raw/kraken/{PAIR}_1d.csv
  02_daten/raw/provenance.json          Herkunft, Zeitraum, Pruefsumme je Datei
  02_daten/raw/nachladen.log            Laufprotokoll
  02_daten/raw/_quarantine/             verworfene Datensaetze mit Grund
"""

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import os
import ssl
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import zipfile

# ----------------------------------------------------------------------------
# Konfiguration
# ----------------------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
DIR_BINANCE = os.path.join(RAW, "binance")
DIR_KRAKEN = os.path.join(RAW, "kraken")
DIR_PERP = os.path.join(RAW, "binance_perp")
DIR_FUNDING = os.path.join(RAW, "binance_funding")
DIR_OI = os.path.join(RAW, "binance_oi")
DIR_QUARANTINE = os.path.join(RAW, "_quarantine")
PROVENANCE = os.path.join(RAW, "provenance.json")
LOGFILE = os.path.join(RAW, "nachladen.log")

BINANCE_BASE = "https://data.binance.vision/data/spot"
BINANCE_FUT = "https://data.binance.vision/data/futures/um"
BINANCE_START = (2017, 8)
FUT_START = (2019, 9)                 # erste Binance-USDT-M-Perpetuals
OI_START = dt.date(2021, 1, 1)        # Metrics-Archiv, tatsaechlicher Beginn wird per 404 erkannt
FUNDING_COLUMNS = ["t", "rate", "interval_hours"]
OI_COLUMNS = ["t", "oi", "oi_value"]
BINANCE_SYMBOLS_ALL = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT",
    "AVAXUSDT", "LINKUSDT", "DOTUSDT", "BNBUSDT", "LTCUSDT",
]
BINANCE_SYMBOLS_CORE = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]

KRAKEN_PAIRS = {  # Dateiname : Kraken-Paarbezeichnung fuer die Abfrage
    "XBT_USD": "XBTUSD",
    "ETH_USD": "ETHUSD",
    "SOL_USD": "SOLUSD",
}

PAUSE_SECONDS = 0.20        # Hoeflichkeitspause zwischen Abrufen
RETRIES = 4
TIMEOUT = 30
USER_AGENT = "AurumII-Datenbasis/0.1 (research, low volume)"

COLUMNS = ["t", "open", "high", "low", "close", "volume"]


# ----------------------------------------------------------------------------
# Hilfsfunktionen
# ----------------------------------------------------------------------------

def log(msg):
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"{stamp}  {msg}"
    print(line)
    os.makedirs(RAW, exist_ok=True)
    with open(LOGFILE, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


_SSL_CTX = None


def ssl_context():
    """
    Das Python von python.org auf macOS kennt die System-Zertifikate nicht und
    scheitert mit CERTIFICATE_VERIFY_FAILED. Reihenfolge der Aufloesung:
      1. certifi, falls installiert
      2. macOS: Root-Zertifikate aus dem System-Schluesselbund exportieren
      3. Standardkontext (Linux, Homebrew-Python)
    Die Pruefung wird nie abgeschaltet.
    """
    global _SSL_CTX
    if _SSL_CTX is not None:
        return _SSL_CTX
    try:
        import certifi  # type: ignore
        _SSL_CTX = ssl.create_default_context(cafile=certifi.where())
        log("TLS: verwende certifi")
        return _SSL_CTX
    except Exception:
        pass
    if sys.platform == "darwin":
        try:
            pem = b""
            for kc in ("/System/Library/Keychains/SystemRootCertificates.keychain",
                       "/Library/Keychains/System.keychain"):
                out = subprocess.run(["security", "find-certificate", "-a", "-p", kc],
                                     capture_output=True, timeout=30)
                if out.returncode == 0:
                    pem += out.stdout
            if b"BEGIN CERTIFICATE" in pem:
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")
                tmp.write(pem)
                tmp.close()
                _SSL_CTX = ssl.create_default_context(cafile=tmp.name)
                log("TLS: verwende macOS-System-Zertifikate")
                return _SSL_CTX
        except Exception as e:
            log(f"TLS: Export der System-Zertifikate fehlgeschlagen ({e})")
    _SSL_CTX = ssl.create_default_context()
    log("TLS: Standardkontext")
    return _SSL_CTX


def fetch(url):
    """Liefert Bytes oder None bei 404. Wirft bei anderen dauerhaften Fehlern."""
    last_err = None
    for attempt in range(RETRIES):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=TIMEOUT, context=ssl_context()) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            last_err = e
        except urllib.error.URLError as e:
            if isinstance(getattr(e, "reason", None), ssl.SSLCertVerificationError):
                raise RuntimeError(
                    "TLS-Zertifikat nicht pruefbar. Abhilfe: im Ordner /Applications/Python 3.x/ "
                    "die Datei 'Install Certificates.command' doppelklicken, oder "
                    "'python3 -m pip install certifi' ausfuehren, danach erneut starten."
                ) from e
            last_err = e
        except (TimeoutError, ConnectionError) as e:
            last_err = e
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Abruf gescheitert nach {RETRIES} Versuchen: {url} ({last_err})")


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def month_iter(start, end):
    y, m = start
    while (y, m) <= end:
        yield y, m
        m += 1
        if m == 13:
            y, m = y + 1, 1


def yesterday_utc():
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=1)).date()


# ----------------------------------------------------------------------------
# Datenvertrag: Validierung, fail-closed
# ----------------------------------------------------------------------------

def validate(rows, label):
    """
    rows: Liste von dicts mit COLUMNS, t als ISO-Datum (YYYY-MM-DD).
    Rueckgabe: (ok, kritische_defekte, warnungen)
    Kritisch bedeutet: der gesamte Datensatz wird verworfen.
    """
    critical, warnings = [], []
    if not rows:
        return False, ["leerer Datensatz"], []

    seen = set()
    prev = None
    for i, r in enumerate(rows):
        t = r["t"]
        try:
            d = dt.date.fromisoformat(t)
        except Exception:
            critical.append(f"Zeile {i}: ungueltiges Datum '{t}'")
            continue
        if t in seen:
            critical.append(f"Zeile {i}: Duplikat {t}")
        seen.add(t)
        if prev is not None:
            if d <= prev:
                critical.append(f"Zeile {i}: Zeitachse nicht monoton bei {t}")
            elif (d - prev).days > 1:
                warnings.append(f"Luecke von {(d - prev).days} Tagen vor {t}")
        prev = d
        try:
            o, h, l, c = (float(r["open"]), float(r["high"]), float(r["low"]), float(r["close"]))
            v = float(r["volume"])
        except Exception:
            critical.append(f"Zeile {i} ({t}): nicht numerisch")
            continue
        if any(x != x for x in (o, h, l, c, v)):
            critical.append(f"Zeile {i} ({t}): NaN")
            continue
        if min(o, h, l, c) <= 0:
            critical.append(f"Zeile {i} ({t}): Kurs nicht positiv")
        if l > min(o, c) + 1e-12 or h < max(o, c) - 1e-12:
            critical.append(f"Zeile {i} ({t}): Schluss oder Eroeffnung ausserhalb Hoch-Tief")
        if v < 0:
            critical.append(f"Zeile {i} ({t}): negatives Volumen")
        if i > 0:
            pc = float(rows[i - 1]["close"])
            if pc > 0 and abs(c / pc - 1) > 4.0:
                warnings.append(f"Extremsprung {c / pc - 1:+.0%} bei {t} (markiert, nicht geloescht)")
    return (len(critical) == 0), critical, warnings


def validate_funding(rows, label):
    critical, warnings = [], []
    if not rows:
        return False, ["leerer Datensatz"], []
    seen, prev = set(), None
    for i, r in enumerate(rows):
        t = r["t"]
        try:
            d = dt.datetime.fromisoformat(t.replace("Z", "+00:00"))
        except Exception:
            critical.append(f"Zeile {i}: ungueltiger Zeitstempel '{t}'"); continue
        if t in seen:
            critical.append(f"Zeile {i}: Duplikat {t}")
        seen.add(t)
        if prev is not None and d <= prev:
            critical.append(f"Zeile {i}: Zeitachse nicht monoton bei {t}")
        if prev is not None and (d - prev).total_seconds() > 3 * 86400:
            warnings.append(f"Luecke von {(d - prev).days} Tagen vor {t}")
        prev = d
        try:
            rate = float(r["rate"])
        except Exception:
            critical.append(f"Zeile {i} ({t}): Rate nicht numerisch"); continue
        if rate != rate:
            critical.append(f"Zeile {i} ({t}): NaN")
        elif abs(rate) > 0.05:
            critical.append(f"Zeile {i} ({t}): Rate {rate} ausserhalb plausibel (+-5% je Periode)")
    return (len(critical) == 0), critical, warnings


def validate_oi(rows, label):
    critical, warnings = [], []
    if not rows:
        return False, ["leerer Datensatz"], []
    seen, prev = set(), None
    for i, r in enumerate(rows):
        t = r["t"]
        try:
            d = dt.date.fromisoformat(t)
        except Exception:
            critical.append(f"Zeile {i}: ungueltiges Datum '{t}'"); continue
        if t in seen:
            critical.append(f"Zeile {i}: Duplikat {t}")
        seen.add(t)
        if prev is not None:
            if d <= prev:
                critical.append(f"Zeile {i}: Zeitachse nicht monoton bei {t}")
            elif (d - prev).days > 3:
                warnings.append(f"Luecke von {(d - prev).days} Tagen vor {t} (D-OI: Coin wird ausgeschlossen)")
        prev = d
        try:
            oi = float(r["oi"])
        except Exception:
            critical.append(f"Zeile {i} ({t}): OI nicht numerisch"); continue
        if oi != oi or oi <= 0:
            critical.append(f"Zeile {i} ({t}): OI nicht positiv")
    return (len(critical) == 0), critical, warnings


def atomic_write_csv(path, rows, columns=None):
    columns = columns or COLUMNS
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=columns)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in columns})
        fh.flush()
        os.fsync(fh.fileno())
    # Kontrolle der temporaeren Datei vor dem Ersetzen
    with open(tmp, newline="", encoding="utf-8") as fh:
        n = sum(1 for _ in csv.DictReader(fh))
    if n != len(rows):
        os.remove(tmp)
        raise RuntimeError(f"Schreibkontrolle fehlgeschlagen fuer {path}: {n} statt {len(rows)} Zeilen")
    os.replace(tmp, path)


def quarantine(label, rows, reasons, columns=None):
    columns = columns or COLUMNS
    os.makedirs(DIR_QUARANTINE, exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base = os.path.join(DIR_QUARANTINE, f"{label}_{stamp}")
    with open(base + ".csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=columns)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in columns})
    with open(base + ".reason.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(reasons))
    log(f"QUARANTAENE {label}: {len(reasons)} kritische Defekte, abgelegt unter {base}.csv")


def read_existing(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return [dict(r) for r in csv.DictReader(fh)]


def update_provenance(entry):
    data = []
    if os.path.exists(PROVENANCE):
        with open(PROVENANCE, encoding="utf-8") as fh:
            try:
                data = json.load(fh)
            except Exception:
                data = []
    data = [d for d in data if not (d.get("file") == entry["file"])]
    data.append(entry)
    data.sort(key=lambda d: d["file"])
    tmp = PROVENANCE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, ensure_ascii=False)
    os.replace(tmp, PROVENANCE)


def commit_dataset(path, label, rows, source, extra=None, kind="ohlc"):
    """Validieren, bei Erfolg atomar schreiben und Herkunft eintragen."""
    rows.sort(key=lambda r: r["t"])
    validator = {"ohlc": validate, "funding": validate_funding, "oi": validate_oi}[kind]
    columns = {"ohlc": COLUMNS, "funding": FUNDING_COLUMNS, "oi": OI_COLUMNS}[kind]
    ok, critical, warnings = validator(rows, label)
    for w in warnings[:10]:
        log(f"  Hinweis {label}: {w}")
    if len(warnings) > 10:
        log(f"  Hinweis {label}: ... und {len(warnings) - 10} weitere Hinweise")
    if not ok:
        quarantine(label, rows, critical, columns)
        log(f"  {label}: bestehende Datei bleibt unveraendert")
        return False
    atomic_write_csv(path, rows, columns)
    entry = {
        "file": os.path.relpath(path, RAW),
        "source": source,
        "rows": len(rows),
        "start": rows[0]["t"],
        "end": rows[-1]["t"],
        "sha256": sha256_of(path),
        "captured_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "bar_rule": {"ohlc": "nur abgeschlossene Tageskerzen, UTC", "funding": "tatsaechliche Zahlungszeitpunkte, UTC",
                     "oi": "letzte Beobachtung je UTC-Tag"}[kind],
        "kind": kind,
        "warnings": len(warnings),
    }
    if extra:
        entry.update(extra)
    update_provenance(entry)
    log(f"  OK {label}: {len(rows)} Zeilen, {rows[0]['t']} bis {rows[-1]['t']}")
    return True


# ----------------------------------------------------------------------------
# Binance Vision
# ----------------------------------------------------------------------------

def parse_binance_zip(blob):
    rows = []
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        name = z.namelist()[0]
        text = z.read(name).decode("utf-8")
    for line in csv.reader(io.StringIO(text)):
        if not line or not line[0].strip().lstrip("-").isdigit():
            continue  # Kopfzeile oder Leerzeile
        ts = int(line[0])
        if ts > 10**14:      # Mikrosekunden (Binance seit 2025)
            ts //= 1000
        d = dt.datetime.fromtimestamp(ts / 1000, tz=dt.timezone.utc).date()
        rows.append({
            "t": d.isoformat(),
            "open": line[1], "high": line[2], "low": line[3], "close": line[4],
            "volume": line[5],
        })
    return rows


def binance_symbol(sym):
    path = os.path.join(DIR_BINANCE, f"{sym}_1d.csv")
    existing = read_existing(path)
    by_date = {r["t"]: r for r in existing}

    today = dt.datetime.now(dt.timezone.utc).date()
    end_full_month = (today.replace(day=1) - dt.timedelta(days=1))  # letzter Tag des Vormonats
    end_m = (end_full_month.year, end_full_month.month)

    if existing:
        last = dt.date.fromisoformat(existing[-1]["t"])
        start_m = (last.year, last.month)      # letzten Monat neu holen
        log(f"{sym}: vorhanden bis {last}, lade ab {start_m[0]}-{start_m[1]:02d}")
    else:
        start_m = BINANCE_START
        log(f"{sym}: keine Datei, lade ab {start_m[0]}-{start_m[1]:02d}")

    first_available = None
    missing_after_start = []
    for y, m in month_iter(start_m, end_m):
        url = f"{BINANCE_BASE}/monthly/klines/{sym}/1d/{sym}-1d-{y}-{m:02d}.zip"
        blob = fetch(url)
        time.sleep(PAUSE_SECONDS)
        if blob is None:
            if first_available is None and not existing:
                continue                      # vor dem Listing
            missing_after_start.append(f"{y}-{m:02d}")
            continue
        if first_available is None:
            first_available = f"{y}-{m:02d}"
        for r in parse_binance_zip(blob):
            by_date[r["t"]] = r

    # Aktueller Monat: Tagesdateien bis gestern
    d = today.replace(day=1)
    stop = yesterday_utc()
    while d <= stop:
        url = f"{BINANCE_BASE}/daily/klines/{sym}/1d/{sym}-1d-{d.isoformat()}.zip"
        blob = fetch(url)
        time.sleep(PAUSE_SECONDS)
        if blob is not None:
            for r in parse_binance_zip(blob):
                if r["t"] <= stop.isoformat():
                    by_date[r["t"]] = r
        d += dt.timedelta(days=1)

    # Falls der Vormonat als Monatsdatei noch fehlt (Binance stellt sie mit Verzoegerung
    # bereit), ebenfalls aus Tagesdateien ergaenzen
    if f"{end_m[0]}-{end_m[1]:02d}" in missing_after_start:
        d = dt.date(end_m[0], end_m[1], 1)
        while d <= end_full_month:
            url = f"{BINANCE_BASE}/daily/klines/{sym}/1d/{sym}-1d-{d.isoformat()}.zip"
            blob = fetch(url)
            time.sleep(PAUSE_SECONDS)
            if blob is not None:
                for r in parse_binance_zip(blob):
                    by_date[r["t"]] = r
            d += dt.timedelta(days=1)
        missing_after_start.remove(f"{end_m[0]}-{end_m[1]:02d}")

    rows = [by_date[k] for k in sorted(by_date)]
    if not rows:
        log(f"{sym}: nichts erhalten, Datei nicht angelegt")
        return False
    extra = {"quote": "USDT", "interval": "1d"}
    if first_available:
        extra["first_available_month_binance"] = first_available
    if missing_after_start:
        extra["missing_months"] = missing_after_start
        log(f"  Hinweis {sym}: fehlende Monatsdateien {missing_after_start}")
    return commit_dataset(path, sym, rows, "binance_vision spot klines 1d", extra)



# ----------------------------------------------------------------------------
# Binance Perpetuals (USDT-M): Funding, Tageskerzen, Open Interest
# ----------------------------------------------------------------------------

def _zip_csv_rows(blob):
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        text = z.read(z.namelist()[0]).decode("utf-8")
    return list(csv.reader(io.StringIO(text)))


def _ts_to_dt(v):
    v = v.strip()
    if v.lstrip("-").isdigit():
        ts = int(v)
        if ts > 10**14:
            ts //= 1000
        return dt.datetime.fromtimestamp(ts / 1000, tz=dt.timezone.utc)
    return dt.datetime.fromisoformat(v.replace("Z", "+00:00")).astimezone(dt.timezone.utc) \
        if "+" in v or "Z" in v else dt.datetime.fromisoformat(v).replace(tzinfo=dt.timezone.utc)


def parse_funding_zip(blob):
    """Binance fundingRate: Spalten calc_time, funding_interval_hours, last_funding_rate (Kopfzeile vorhanden)."""
    rows = _zip_csv_rows(blob)
    if not rows:
        return []
    header = [h.strip().lower() for h in rows[0]]
    has_header = not rows[0][0].strip().lstrip("-").isdigit()
    if has_header:
        i_t = next(i for i, h in enumerate(header) if "time" in h)
        i_r = next(i for i, h in enumerate(header) if "rate" in h)
        i_h = next((i for i, h in enumerate(header) if "interval" in h), None)
        body = rows[1:]
    else:
        i_t, i_r, i_h, body = 0, 2, 1, rows
    out = []
    for line in body:
        if not line or not line[0].strip():
            continue
        t = _ts_to_dt(line[i_t])
        out.append({"t": t.isoformat(), "rate": line[i_r].strip(),
                    "interval_hours": (line[i_h].strip() if i_h is not None and i_h < len(line) else "")})
    return out


def parse_metrics_zip(blob):
    """Binance metrics (5-Minuten-Raster): create_time, symbol, sum_open_interest, sum_open_interest_value, ..."""
    rows = _zip_csv_rows(blob)
    if not rows:
        return []
    header = [h.strip().lower() for h in rows[0]]
    i_t = next(i for i, h in enumerate(header) if "time" in h)
    i_oi = next(i for i, h in enumerate(header) if h == "sum_open_interest")
    i_ov = next((i for i, h in enumerate(header) if h == "sum_open_interest_value"), None)
    out = []
    for line in rows[1:]:
        if not line or not line[0].strip():
            continue
        t = _ts_to_dt(line[i_t])
        out.append((t, line[i_oi].strip(), line[i_ov].strip() if i_ov is not None else ""))
    return out


def perp_symbol(sym):
    """Perp-Tageskerzen, gleiche Logik wie Spot, anderer Archivpfad."""
    path = os.path.join(DIR_PERP, f"{sym}_1d.csv")
    existing = read_existing(path)
    by_date = {r["t"]: r for r in existing}
    today = dt.datetime.now(dt.timezone.utc).date()
    end_full_month = today.replace(day=1) - dt.timedelta(days=1)
    end_m = (end_full_month.year, end_full_month.month)
    if existing:
        last = dt.date.fromisoformat(existing[-1]["t"])
        start_m = (last.year, last.month)
        log(f"Perp {sym}: vorhanden bis {last}, lade ab {start_m[0]}-{start_m[1]:02d}")
    else:
        start_m = FUT_START
        log(f"Perp {sym}: keine Datei, lade ab {start_m[0]}-{start_m[1]:02d}")
    first_available = None
    for y, m in month_iter(start_m, end_m):
        blob = fetch(f"{BINANCE_FUT}/monthly/klines/{sym}/1d/{sym}-1d-{y}-{m:02d}.zip")
        time.sleep(PAUSE_SECONDS)
        if blob is None:
            continue
        if first_available is None:
            first_available = f"{y}-{m:02d}"
        for r in parse_binance_zip(blob):
            by_date[r["t"]] = r
    d = today.replace(day=1)
    stop = yesterday_utc()
    while d <= stop:
        blob = fetch(f"{BINANCE_FUT}/daily/klines/{sym}/1d/{sym}-1d-{d.isoformat()}.zip")
        time.sleep(PAUSE_SECONDS)
        if blob is not None:
            for r in parse_binance_zip(blob):
                if r["t"] <= stop.isoformat():
                    by_date[r["t"]] = r
        d += dt.timedelta(days=1)
    rows = [by_date[k] for k in sorted(by_date)]
    if not rows:
        log(f"Perp {sym}: nichts erhalten"); return False
    extra = {"quote": "USDT", "interval": "1d", "market": "usdt_m_perpetual"}
    if first_available:
        extra["first_available_month_binance"] = first_available
    return commit_dataset(path, f"perp_{sym}", rows, "binance_vision futures/um klines 1d", extra)


def funding_symbol(sym):
    path = os.path.join(DIR_FUNDING, f"{sym}_funding.csv")
    existing = read_existing(path)
    by_t = {r["t"]: r for r in existing}
    today = dt.datetime.now(dt.timezone.utc).date()
    end_full_month = today.replace(day=1) - dt.timedelta(days=1)
    end_m = (end_full_month.year, end_full_month.month)
    if existing:
        last = dt.datetime.fromisoformat(existing[-1]["t"]).date()
        start_m = (last.year, last.month)
        log(f"Funding {sym}: vorhanden bis {last}, lade ab {start_m[0]}-{start_m[1]:02d}")
    else:
        start_m = FUT_START
        log(f"Funding {sym}: keine Datei, lade ab {start_m[0]}-{start_m[1]:02d}")
    first_available = None
    # Monatsdateien bis einschliesslich laufender Monat (Funding-Monatsdatei erscheint mit Verzoegerung)
    for y, m in month_iter(start_m, (today.year, today.month)):
        blob = fetch(f"{BINANCE_FUT}/monthly/fundingRate/{sym}/{sym}-fundingRate-{y}-{m:02d}.zip")
        time.sleep(PAUSE_SECONDS)
        if blob is None:
            continue
        if first_available is None:
            first_available = f"{y}-{m:02d}"
        for r in parse_funding_zip(blob):
            by_t[r["t"]] = r
    rows = [by_t[k] for k in sorted(by_t)]
    if not rows:
        log(f"Funding {sym}: nichts erhalten"); return False
    extra = {"market": "usdt_m_perpetual", "rate_unit": "relativ je Zahlungsperiode (Bruchteil)"}
    if first_available:
        extra["first_available_month_binance"] = first_available
    return commit_dataset(path, f"funding_{sym}", rows, "binance_vision futures/um fundingRate", extra, kind="funding")


def oi_symbol(sym, max_days=None):
    """Open Interest aus Tagesdateien, letzter 5-Minuten-Wert je UTC-Tag. Langsam, inkrementell, unterbrechbar."""
    path = os.path.join(DIR_OI, f"{sym}_oi_1d.csv")
    existing = read_existing(path)
    by_date = {r["t"]: r for r in existing}
    stop = yesterday_utc()
    if existing:
        d = dt.date.fromisoformat(existing[-1]["t"])
        log(f"OI {sym}: vorhanden bis {d}, lade ab {d}")
    else:
        d = OI_START
        log(f"OI {sym}: keine Datei, suche Beginn ab {d}")
    found_any = bool(existing)
    misses_after_found = 0
    zero_rows_days = 0
    n = 0
    while d <= stop:
        blob = fetch(f"{BINANCE_FUT}/daily/metrics/{sym}/{sym}-metrics-{d.isoformat()}.zip")
        time.sleep(0.05)
        n += 1
        if blob is None:
            if found_any:
                misses_after_found += 1
        else:
            found_any = True
            obs = parse_metrics_zip(blob)
            # Binance-Archivartefakt: einzelne 5-Minuten-Zeilen mit Open Interest 0 (z. B. 0E-8) am Tagesende.
            # Ein Open Interest von null ist bei BTC-Perpetuals physisch unmoeglich. Es gilt die letzte
            # positive Beobachtung des Tages. Tage ohne positive Beobachtung bleiben leer (Lueckenregel).
            valid = []
            for t_, oi_, ov_ in obs:
                try:
                    if float(oi_) > 0:
                        valid.append((t_, oi_, ov_))
                except ValueError:
                    pass
            if len(valid) < len(obs):
                zero_rows_days += 1
            if valid:
                t, oi, ov = max(valid, key=lambda x: x[0])
                by_date[d.isoformat()] = {"t": d.isoformat(), "oi": oi, "oi_value": ov}
        if n % 200 == 0:
            log(f"  OI {sym}: {d} ... ({len(by_date)} Tage gesammelt)")
            # Zwischenstand sichern, damit ein Abbruch nichts verliert
            rows = [by_date[k] for k in sorted(by_date)]
            if rows:
                commit_dataset(path, f"oi_{sym}", rows, "binance_vision futures/um metrics (sum_open_interest)",
                               {"market": "usdt_m_perpetual", "partial": True}, kind="oi")
        if max_days and n >= max_days:
            log(f"  OI {sym}: Tageslimit {max_days} erreicht, naechster Lauf setzt fort")
            break
        d += dt.timedelta(days=1)
    rows = [by_date[k] for k in sorted(by_date)]
    if not rows:
        log(f"OI {sym}: nichts erhalten"); return False
    log(f"  OI {sym}: Tage mit Null-Zeilen im Archiv (letzte positive Beobachtung verwendet): {zero_rows_days}")
    return commit_dataset(path, f"oi_{sym}", rows, "binance_vision futures/um metrics (sum_open_interest)",
                          {"market": "usdt_m_perpetual", "missing_days_after_start": misses_after_found,
                           "days_with_zero_rows": zero_rows_days, "daily_rule": "letzte positive Beobachtung vor 00:00 UTC"}, kind="oi")

# ----------------------------------------------------------------------------
# Kraken
# ----------------------------------------------------------------------------

def kraken_pair(file_key, pair):
    path = os.path.join(DIR_KRAKEN, f"{file_key}_1d.csv")
    existing = read_existing(path)
    by_date = {r["t"]: r for r in existing}
    url = f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval=1440"
    log(f"Kraken {file_key}: Abruf der letzten 720 Tage")
    blob = fetch(url)
    time.sleep(1.0)
    if blob is None:
        log(f"Kraken {file_key}: 404, Paar unbekannt")
        return False
    data = json.loads(blob.decode("utf-8"))
    if data.get("error"):
        log(f"Kraken {file_key}: Fehler {data['error']}")
        return False
    result = data["result"]
    key = [k for k in result if k != "last"][0]
    now = dt.datetime.now(dt.timezone.utc).timestamp()
    n_new = 0
    for c in result[key]:
        ts = int(c[0])
        if ts + 86400 > now:
            continue                          # laufende Kerze verwerfen
        d = dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc).date().isoformat()
        by_date[d] = {"t": d, "open": c[1], "high": c[2], "low": c[3], "close": c[4], "volume": c[6]}
        n_new += 1
    rows = [by_date[k] for k in sorted(by_date)]
    return commit_dataset(path, f"kraken_{file_key}", rows, f"kraken public OHLC {key} 1440",
                          {"quote": "USD", "interval": "1d", "api_limit": "720 Kerzen je Abruf"})


# ----------------------------------------------------------------------------
# Pruefmodus
# ----------------------------------------------------------------------------

def check_all():
    files = []
    for d in (DIR_BINANCE, DIR_KRAKEN, DIR_PERP, DIR_FUNDING, DIR_OI):
        if os.path.isdir(d):
            files += [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith(".csv")]
    if not files:
        print("Keine Dateien unter", RAW)
        return
    print(f"{'Datei':<34}{'Zeilen':>8}  {'von':<12}{'bis':<12}{'Status':<10}Hinweise")
    for p in files:
        rows = read_existing(p)
        kind = "funding" if "_funding" in p else ("oi" if "_oi_" in p else "ohlc")
        validator = {"ohlc": validate, "funding": validate_funding, "oi": validate_oi}[kind]
        ok, crit, warn = validator(rows, os.path.basename(p)) if rows else (False, ["leer"], [])
        status = "OK" if ok else "DEFEKT"
        start = rows[0]["t"][:10] if rows else "-"
        end = rows[-1]["t"][:10] if rows else "-"
        note = (crit[0] if crit else (f"{len(warn)} Hinweise" if warn else ""))
        print(f"{os.path.relpath(p, RAW):<34}{len(rows):>8}  {start:<12}{end:<12}{status:<10}{note}")


# ----------------------------------------------------------------------------
# Hauptprogramm
# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Aurum II — Kurshistorie nachladen")
    ap.add_argument("--core", action="store_true", help="nur BTC, ETH, SOL")
    ap.add_argument("--check", action="store_true", help="nur vorhandene Dateien pruefen")
    ap.add_argument("--symbols", nargs="*", help="Binance-Symbole, z. B. BTCUSDT ETHUSDT")
    ap.add_argument("--no-kraken", action="store_true", help="Kraken-Abruf ueberspringen")
    ap.add_argument("--no-binance", action="store_true", help="Binance-Abruf ueberspringen")
    ap.add_argument("--futures", action="store_true", help="Binance Perpetuals: Funding und Perp-Tageskerzen laden")
    ap.add_argument("--oi", action="store_true", help="Binance Open Interest laden (langsam, inkrementell)")
    ap.add_argument("--oi-max-days", type=int, default=None, help="OI: hoechstens so viele Tage je Symbol in diesem Lauf")
    args = ap.parse_args()

    if args.check:
        check_all()
        return

    os.makedirs(RAW, exist_ok=True)
    log("=== Start Nachladen ===")
    symbols = args.symbols or (BINANCE_SYMBOLS_CORE if args.core else BINANCE_SYMBOLS_ALL)

    results = {}
    if args.futures or args.oi:
        for sym in symbols:
            if args.futures:
                for fn, name in ((funding_symbol, "funding"), (perp_symbol, "perp")):
                    try:
                        results[f"{name}_{sym}"] = fn(sym)
                    except Exception as e:
                        log(f"FEHLER {name} {sym}: {e}"); results[f"{name}_{sym}"] = False
            if args.oi:
                try:
                    results[f"oi_{sym}"] = oi_symbol(sym, args.oi_max_days)
                except Exception as e:
                    log(f"FEHLER oi {sym}: {e}"); results[f"oi_{sym}"] = False
        ok = [k for k, v in results.items() if v]; bad = [k for k, v in results.items() if not v]
        log(f"=== Ende Futures. OK: {len(ok)}  Verworfen oder Fehler: {len(bad)} {bad if bad else ''} ===")
        print(); check_all(); return
    if not args.no_binance:
        for sym in symbols:
            try:
                results[sym] = binance_symbol(sym)
            except Exception as e:
                log(f"FEHLER {sym}: {e}")
                results[sym] = False
    if not args.no_kraken:
        for file_key, pair in KRAKEN_PAIRS.items():
            try:
                results[f"kraken_{file_key}"] = kraken_pair(file_key, pair)
            except Exception as e:
                log(f"FEHLER kraken {file_key}: {e}")
                results[f"kraken_{file_key}"] = False

    ok = [k for k, v in results.items() if v]
    bad = [k for k, v in results.items() if not v]
    log(f"=== Ende. OK: {len(ok)}  Verworfen oder Fehler: {len(bad)} {bad if bad else ''} ===")
    print()
    check_all()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAbgebrochen.")
        sys.exit(130)
