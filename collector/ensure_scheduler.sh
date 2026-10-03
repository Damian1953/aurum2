#!/usr/bin/env bash
# Stellt sicher, dass der taegliche Collector geplant ist (Box ohne systemd: PID 1 ist tini).
#  1. cron-Daemon starten, falls er nicht laeuft (nach Box-Neustart noetig)
#  2. crontab-Eintrag setzen, falls er fehlt
#  3. Nachholen: wenn heute nach 06:15 (Zuerich) noch kein erfolgreicher Lauf war, sofort im Hintergrund starten
#  4. Paper-Runner (PAPER_PREREG_v1.0, D1): cron 06:50 taeglich und Wochenbericht montags 07:10 sicherstellen;
#     nach 06:50 nachholen, wenn der gestern abgeschlossene Tagesbar noch nicht verarbeitet ist (--if-needed)
#  5. Forward-Linien (eingefroren 2026-10-02): Sleeves A/B 06:55 (aurum2-sleeves), VOLTARGET 07:00 (aurum2-voltarget),
#     gemeinsamer Heartbeat 07:30 (aurum2-heartbeat, nur lesen, Log); nachholen, wenn heute noch kein Lauf protokolliert ist
#  6. Selbstaufruf: cron alle 10 Minuten (aurum2-ensure), stuendlich 07:05-12:05 (aurum2-catchup-hourly) und @reboot
#     (aurum2-ensure-reboot). Fehlgeschlagenes Nachholen, Heartbeat-Fehler oder ein nicht startbarer cron-Daemon
#     schreiben eine Zeile in die Flag-Datei /workspace/aurum2/ALARM (nur manuell quittieren/loeschen). Grund: Box-Pause
#     02.10. ~23:30 bis 03.10. 07:04 (VM angehalten und fortgesetzt); cron ueberspringt nach einem Uhrsprung > 3 h alle
#     verpassten Termine. Der 10-Minuten-Aufruf holt spaetestens 10 Minuten nach der Fortsetzung nach.
#  7. Nachholen als EINE Kette in fester Reihenfolge (Collector -> PAPER -> Sleeves A/B -> VOLTARGET), mit eigenem Lock.
#     Ein Runner ist faellig, wenn sein Termin heute vorbei ist und er seit max(Termin heute, letzter erfolgreicher
#     Collector-Lauf) nicht gelaufen ist. Sleeves/VOLTARGET nur mit enabled=true. Protokoll: $OUT/logs/catchup.log
# Idempotent und still. Aufruf aus ~/.bashrc (jede neue Shell auf der Box), aus cron (alle 10 min) und manuell.
REPO="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${AURUM_DATA_LIVE:-/workspace/aurum2/data_live}"
ALARM_FILE="${AURUM_ALARM_FILE:-/workspace/aurum2/ALARM}"   # Flag-Datei: wird nur angelegt/ergaenzt, nie automatisch geloescht
alarm() { echo "$(date -Iseconds) $*" >> "$ALARM_FILE"; }
LINE="15 6 * * * $REPO/collector/run_collector.sh  # aurum2-collector"
if ! pgrep -x cron >/dev/null 2>&1; then
  mkdir -p "$OUT/logs"; echo "$(date -Iseconds) cron-Daemon lief nicht, Neustart" >> "$OUT/logs/catchup.log"
  sudo -n /usr/sbin/cron 2>/dev/null || /usr/sbin/cron 2>/dev/null || true
  sleep 1
  if ! pgrep -x cron >/dev/null 2>&1; then
    echo "aurum2: cron konnte nicht gestartet werden" >&2; alarm "FEHLER cron-Daemon laeuft nicht und konnte nicht gestartet werden"
  fi
fi
if ! crontab -l 2>/dev/null | grep -q "aurum2-collector"; then
  { crontab -l 2>/dev/null; echo "CRON_TZ=Europe/Zurich"; echo "$LINE"; } | crontab -
fi
PLINE="50 6 * * * $REPO/paper/run_paper.sh --if-needed  # aurum2-paper"
BLINE="10 7 * * 1 $REPO/paper/run_wochenbericht.sh  # aurum2-paper-bericht"
SLINE="55 6 * * * $REPO/sleeves/run_sleeves.sh  # aurum2-sleeves"
VLINE="0 7 * * * $REPO/voltarget/run_voltarget.sh  # aurum2-voltarget"
HB_LOG="/workspace/aurum2/forward_heartbeat.log"
HLINE="30 7 * * * cd $REPO && { date -Iseconds; $REPO/.venv/bin/python forward/heartbeat.py; rc=\$?; echo \"rc=\$rc\"; [ \$rc -eq 0 ] || echo \"\$(date -Iseconds) FEHLER Heartbeat rc=\$rc (siehe $HB_LOG)\" >> $ALARM_FILE; } >> $HB_LOG 2>&1  # aurum2-heartbeat-v2"
ELINE="*/10 * * * * $REPO/collector/ensure_scheduler.sh >/dev/null 2>&1  # aurum2-ensure"
RLINE="@reboot $REPO/collector/ensure_scheduler.sh >/dev/null 2>&1  # aurum2-ensure-reboot"
KLINE="5 7-12 * * * $REPO/collector/ensure_scheduler.sh >/dev/null 2>&1  # aurum2-catchup-hourly"
# alte Heartbeat-Zeile (ohne ALARM-Datei) ersetzen
if crontab -l 2>/dev/null | grep -q "# aurum2-heartbeat\$"; then
  crontab -l 2>/dev/null | grep -v "# aurum2-heartbeat\$" | crontab -
fi
for L in "$PLINE" "$BLINE" "$SLINE" "$VLINE" "$HLINE" "$ELINE" "$RLINE" "$KLINE"; do
  tag="${L##*# }"
  if ! crontab -l 2>/dev/null | grep -q "# $tag\$"; then
    { crontab -l 2>/dev/null | grep -q "^CRON_TZ=" || echo "CRON_TZ=Europe/Zurich"; crontab -l 2>/dev/null; echo "$L"; } | crontab -
  fi
done
mkdir -p "$OUT/logs"
CLOG="$OUT/logs/catchup.log"
# faellige Schritte bestimmen (nur lesen); Ausgabe z. B. "collector paper sleeves voltarget"
DUE=$(python3 - "$REPO" "$OUT" <<'PY' 2>>"$CLOG"
import json, os, sys, datetime as dt, zoneinfo
repo, out = sys.argv[1], sys.argv[2]
z = zoneinfo.ZoneInfo("Europe/Zurich")
now = dt.datetime.fromisoformat(os.environ["AURUM_CATCHUP_NOW"]).astimezone(z) if os.environ.get("AURUM_CATCHUP_NOW") else dt.datetime.now(z)
today = now.date()
def slot(hm):
    h, m = map(int, hm.split(":")); return dt.datetime(today.year, today.month, today.day, h, m, tzinfo=z)
def last(path, ok_only=False):
    best = None
    try:
        for l in open(path):
            try:
                d = json.loads(l)
            except ValueError:
                continue
            if ok_only and not (d.get("ok") is True or d.get("rc") == 0):
                continue
            s = d.get("started_utc") or d.get("run_utc")
            if s:
                t = dt.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(z)
                best = t if best is None or t > best else best
    except OSError:
        pass
    return best
def enabled(cfg):
    try:
        return json.load(open(os.path.join(repo, cfg))).get("enabled") is True
    except Exception:
        return False
due = []
c_ok = last(os.path.join(out, "run_history.jsonl"), ok_only=True)
c_any = last(os.path.join(out, "run_history.jsonl"))
if now >= slot("06:15") and (c_ok is None or c_ok < slot("06:15")) \
        and (c_any is None or c_any < now - dt.timedelta(minutes=60)):     # nach Fehlversuch hoechstens stuendlich
    due.append("collector")
runners = [("paper", "06:50", os.path.join(os.environ.get("AURUM_PAPER_OUT", "/workspace/aurum2/paper"), "logs/run_history.jsonl"), None),
           ("sleeves", "06:55", os.path.join(os.environ.get("AURUM_SLEEVES_OUT", "/workspace/aurum2/paper_sleeves"), "logs/run_history.jsonl"), "sleeves/sleeves_config.json"),
           ("voltarget", "07:00", os.path.join(os.environ.get("AURUM_VOLTARGET_OUT", "/workspace/aurum2/paper_voltarget"), "logs/run_history.jsonl"), "voltarget/voltarget_config.json")]
for name, hm, hist, cfg in runners:
    if now < slot(hm) or (cfg and not enabled(cfg)):
        continue
    ref = slot(hm) if c_ok is None or c_ok < slot(hm) else c_ok
    t = last(hist)
    if "collector" in due or t is None or t < ref:
        due.append(name)
print(" ".join(due))
PY
)
if [ -n "$DUE" ]; then
  # eine Kette, feste Reihenfolge; ein zweiter Aufruf waehrend einer laufenden Kette tut nichts
  nohup bash -c '
    exec 8>"$1/.catchup.lock"; flock -n 8 || exit 0
    REPO="$2"; LOG="$3"; AF="$4"; shift 4; fail=""
    for step in "$@"; do
      case "$step" in
        collector) cmd=("$REPO/collector/run_collector.sh") ;;
        paper)     cmd=("$REPO/paper/run_paper.sh" --if-needed) ;;
        sleeves)   cmd=("$REPO/sleeves/run_sleeves.sh") ;;
        voltarget) cmd=("$REPO/voltarget/run_voltarget.sh") ;;
        *) continue ;;
      esac
      echo "$(date -Iseconds) NACHHOLEN $step" >> "$LOG"
      "${cmd[@]}" >/dev/null 2>&1; rc=$?
      echo "$(date -Iseconds) ENDE $step rc=$rc" >> "$LOG"
      # rc 2 = Lock belegt (anderer Lauf aktiv), der naechste Aufruf prueft erneut; alles andere ausser 0 ist ein Fehler
      [ "$rc" -eq 0 ] || [ "$rc" -eq 2 ] || fail="$fail $step(rc=$rc)"
    done
    [ -z "$fail" ] || echo "$(date -Iseconds) FEHLER Nachholen:$fail (siehe $LOG)" >> "$AF"' _ "$OUT" "$REPO" "$CLOG" "$ALARM_FILE" $DUE >/dev/null 2>&1 &
fi
exit 0
