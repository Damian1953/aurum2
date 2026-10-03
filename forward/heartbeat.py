#!/usr/bin/env python3
"""Gemeinsamer Heartbeat aller Forward-Linien (Collector, PAPER v1.0, Sleeves A/B, VOLTARGET).

Eine Statuszeile je Runner und ALARM, wenn ein erwarteter Lauf fehlt (kein Lauf seit dem letzten faelligen Termin laut
SCHEDULE, ohne Fahrplan: letzter Lauf aelter als MAX_AGE_H Stunden, oder gar keiner) oder der letzte Lauf fehlgeschlagen ist. Erwartet wird ein Lauf nur, wenn der Runner freigegeben ist
(Collector und PAPER immer; Sleeves und VOLTARGET nur mit enabled=true in ihrer Konfiguration).
Liest nur Dateien (run_history.jsonl), schreibt nichts, startet nichts, kein cron-Eintrag.
Aufruf: python forward/heartbeat.py   (Exit 1 bei Alarm, sonst 0)
Schnittstelle zu den Runnern: jede Zeile in run_history.jsonl hat einen UTC-Zeitstempel (started_utc oder run_utc)
und ein Ergebnis (ok: bool oder rc: int, 0 = ok).
"""
import datetime as dt, json, os, sys
from zoneinfo import ZoneInfo

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_AGE_H = 26          # Rueckfallgrenze fuer Runner ohne Fahrplan (taeglicher Lauf plus 2 Stunden Toleranz)
# Fahrplan (cron, Zuerich): ein Lauf gilt erst als vorhanden, wenn er NACH dem letzten faelligen Termin gestartet ist.
# Faellig ist ein Termin GRACE_MIN Minuten nach der geplanten Zeit (Collector braucht ~2 min, Runner warten auf ihn).
# Grund (2026-10-03): Box-Pause 02.10. ~23:30 bis 03.10. 07:04, cron hat 06:15-07:00 uebersprungen; die 26-h-Regel
# meldete um 07:30 faelschlich OK, weil die Vortagslaeufe erst ~25 h alt waren.
SCHEDULE = {"Collector": "06:15", "PAPER v1.0": "06:50", "Sleeves A/B": "06:55", "VOLTARGET": "07:00"}
GRACE_MIN = 20
UTC = dt.timezone.utc
ZH = ZoneInfo("Europe/Zurich")


def _env(k, d):
    return os.environ.get(k, d)


def runners():
    """(name, run_history-Pfad, Konfigurationsdatei oder None = immer erwartet)."""
    return [
        ("Collector", os.path.join(_env("AURUM_DATA_LIVE", "/workspace/aurum2/data_live"), "run_history.jsonl"), None),
        ("PAPER v1.0", os.path.join(_env("AURUM_PAPER_OUT", "/workspace/aurum2/paper"), "logs", "run_history.jsonl"), None),
        ("Sleeves A/B", os.path.join(_env("AURUM_SLEEVES_OUT", "/workspace/aurum2/paper_sleeves"), "logs", "run_history.jsonl"),
         os.path.join(REPO, "sleeves", "sleeves_config.json")),
        ("VOLTARGET", os.path.join(_env("AURUM_VOLTARGET_OUT", "/workspace/aurum2/paper_voltarget"), "logs", "run_history.jsonl"),
         os.path.join(REPO, "voltarget", "voltarget_config.json")),
    ]


def _ts(x):
    s = x.get("started_utc") or x.get("run_utc")
    if not s:
        return None
    t = dt.datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    return t if t.tzinfo else t.replace(tzinfo=UTC)


def _ok(x):
    if "ok" in x:
        return bool(x["ok"])
    return x.get("rc") == 0


def _last(path):
    if not os.path.exists(path):
        return None
    last = None
    for line in open(path):
        line = line.strip()
        if line:
            try:
                last = json.loads(line)
            except ValueError:
                continue
    return last


def last_due(now, hhmm, grace_min=GRACE_MIN):
    """Letzter faelliger Termin (UTC): heute hhmm Zuerich, falls schon grace_min Minuten vorbei, sonst gestern."""
    loc = now.astimezone(ZH); h, m = map(int, hhmm.split(":"))
    for back in (0, 1, 2):
        d = (loc - dt.timedelta(days=back)).date()
        slot = dt.datetime(d.year, d.month, d.day, h, m, tzinfo=ZH)
        if slot + dt.timedelta(minutes=grace_min) <= loc:
            return slot.astimezone(UTC)
    return None


def check(now=None, entries=None, max_age_h=MAX_AGE_H):
    """Rueckgabe Liste dict(name, erwartet, status, alarm, letzter_lauf (Zuerich), alter_h, faellig, text).
    entries: (name, run_history, config|None[, fahrplan 'HH:MM'|None]); ohne vierten Wert gilt SCHEDULE[name]."""
    now = now or dt.datetime.now(UTC)
    out = []
    for e in (entries or runners()):
        name, hist, cfgp = e[:3]
        sched = e[3] if len(e) > 3 else SCHEDULE.get(name)
        due = last_due(now, sched) if sched else None
        erwartet, hinweis = True, ""
        if cfgp is not None:
            if not os.path.exists(cfgp):
                erwartet, hinweis = False, "auf diesem Stand nicht vorhanden"
            else:
                try:
                    erwartet = json.load(open(cfgp)).get("enabled") is True
                except Exception as e:
                    erwartet, hinweis = True, f"Konfiguration nicht lesbar ({e})"
                if not erwartet and not hinweis:
                    hinweis = "nicht freigegeben, kein Lauf erwartet"
        try:
            x = _last(hist); t = _ts(x) if x else None
        except Exception as e:
            x, t, hinweis = None, None, f"run_history nicht lesbar ({e})"
        age = None if t is None else (now - t).total_seconds() / 3600.0
        if not erwartet:
            status, alarm = "INAKTIV", False
        elif t is None:
            status, alarm = "FEHLER", True; hinweis = "kein Lauf protokolliert"
        elif due is not None and t < due:
            status, alarm = "FEHLER", True
            hinweis = f"Lauf fehlt (faellig {due.astimezone(ZH).strftime('%Y-%m-%d %H:%M')} Zürich, Fahrplan {sched})"
        elif age > max_age_h:
            status, alarm = "FEHLER", True; hinweis = f"Lauf fehlt (letzter vor {age:.0f} h, Grenze {max_age_h} h)"
        elif not _ok(x):
            status, alarm = "FEHLER", True; hinweis = "letzter Lauf fehlgeschlagen"
        else:
            status, alarm = "OK", False
        last = t.astimezone(ZH).strftime("%Y-%m-%d %H:%M Zürich") if t else "–"
        out.append(dict(name=name, erwartet=erwartet, status=status, alarm=alarm, letzter_lauf=last,
                        alter_h=None if age is None else round(age, 1),
                        faellig=None if due is None else due.astimezone(ZH).strftime("%Y-%m-%d %H:%M Zürich"),
                        text=f"- {'**ALARM**' if alarm else status} {name}: "
                             + ("FEHLER, " if alarm else "") + f"letzter Lauf {last}"
                             + (f", {hinweis}" if hinweis else "") + "."))
    return out


def cron_status(pgrep=None):
    """cron-Daemon pruefen (die Box hat kein systemd, PID 1 ist tini: ein gestorbener cron startet nicht von selbst).
    Rueckgabe dict(alarm, text). Hinweis: Ist cron tot, laeuft auch dieser Heartbeat aus cron nicht; die Pruefung greift
    beim Aufruf aus einer Shell, aus collector/ensure_scheduler.sh (startet cron neu) und im Wochenbericht."""
    import subprocess
    try:
        ok = (pgrep or (lambda: subprocess.run(["pgrep", "-x", "cron"], capture_output=True).returncode == 0))()
    except Exception:
        ok = False
    return dict(alarm=not ok, text="- OK cron-Daemon: läuft." if ok else
                "- **ALARM** cron-Daemon: FEHLER, läuft nicht (collector/ensure_scheduler.sh startet ihn neu).")


def lines(now=None, entries=None):
    return [r["text"] for r in check(now, entries)]


def main():
    res = check()
    for r in res:
        print(r["text"])
    cr = cron_status()
    print(cr["text"])
    return 1 if any(r["alarm"] for r in res) or cr["alarm"] else 0


if __name__ == "__main__":
    sys.exit(main())
