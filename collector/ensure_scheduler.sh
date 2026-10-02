#!/usr/bin/env bash
# Stellt sicher, dass der taegliche Collector geplant ist (Box ohne systemd: PID 1 ist tini).
#  1. cron-Daemon starten, falls er nicht laeuft (nach Box-Neustart noetig)
#  2. crontab-Eintrag setzen, falls er fehlt
#  3. Nachholen: wenn heute nach 06:15 (Zuerich) noch kein erfolgreicher Lauf war, sofort im Hintergrund starten
#  4. Paper-Runner (PAPER_PREREG_v1.0, D1): cron 06:50 taeglich und Wochenbericht montags 07:10 sicherstellen;
#     nach 06:50 nachholen, wenn der gestern abgeschlossene Tagesbar noch nicht verarbeitet ist (--if-needed)
#  5. Forward-Linien (eingefroren 2026-10-02): Sleeves A/B 06:55 (aurum2-sleeves), VOLTARGET 07:00 (aurum2-voltarget),
#     gemeinsamer Heartbeat 07:30 (aurum2-heartbeat, nur lesen, Log); nachholen, wenn heute noch kein Lauf protokolliert ist
# Idempotent und still. Aufruf aus ~/.bashrc (jede neue Shell auf der Box) und manuell.
REPO="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${AURUM_DATA_LIVE:-/workspace/aurum2/data_live}"
LINE="15 6 * * * $REPO/collector/run_collector.sh  # aurum2-collector"
if ! pgrep -x cron >/dev/null 2>&1; then
  sudo -n /usr/sbin/cron 2>/dev/null || /usr/sbin/cron 2>/dev/null || echo "aurum2: cron konnte nicht gestartet werden" >&2
fi
if ! crontab -l 2>/dev/null | grep -q "aurum2-collector"; then
  { crontab -l 2>/dev/null; echo "CRON_TZ=Europe/Zurich"; echo "$LINE"; } | crontab -
fi
PLINE="50 6 * * * $REPO/paper/run_paper.sh --if-needed  # aurum2-paper"
BLINE="10 7 * * 1 $REPO/paper/run_wochenbericht.sh  # aurum2-paper-bericht"
SLINE="55 6 * * * $REPO/sleeves/run_sleeves.sh  # aurum2-sleeves"
VLINE="0 7 * * * $REPO/voltarget/run_voltarget.sh  # aurum2-voltarget"
HB_LOG="/workspace/aurum2/forward_heartbeat.log"
HLINE="30 7 * * * cd $REPO && ($REPO/.venv/bin/python forward/heartbeat.py; echo \"rc=\$?\") >> $HB_LOG 2>&1  # aurum2-heartbeat"
for L in "$PLINE" "$BLINE" "$SLINE" "$VLINE" "$HLINE"; do
  tag="${L##*# }"
  if ! crontab -l 2>/dev/null | grep -q "# $tag\$"; then
    { crontab -l 2>/dev/null | grep -q "^CRON_TZ=" || echo "CRON_TZ=Europe/Zurich"; crontab -l 2>/dev/null; echo "$L"; } | crontab -
  fi
done
now_hm=$(TZ=Europe/Zurich date +%H%M); today=$(TZ=Europe/Zurich date +%F)
mkdir -p "$OUT/logs"
if [ "$now_hm" -ge 0615 ] && flock -n "$OUT/.collector.lock" true 2>/dev/null; then
  last_ok=$(python3 - "$OUT/run_history.jsonl" <<'PY' 2>/dev/null
import json, sys, datetime as dt, zoneinfo
z = zoneinfo.ZoneInfo("Europe/Zurich"); best = ""
for l in open(sys.argv[1]):
    d = json.loads(l)
    if d.get("ok"):
        t = dt.datetime.fromisoformat(d["started_utc"].replace("Z", "+00:00")).astimezone(z)
        best = max(best, t.strftime("%F %H%M"))
print(best)
PY
)
  # erfolgreicher Lauf heute ab 06:15? sonst nachholen
  if [[ "$last_ok" < "$today 0615" ]]; then
    echo "$(date -Iseconds) NACHHOLEN (letzter erfolgreicher Lauf: ${last_ok:-nie})" >> "$OUT/logs/cron.log"
    nohup "$REPO/collector/run_collector.sh" >/dev/null 2>&1 &
  fi
fi
# Forward-Linien nachholen: Sleeves A/B ab 06:55, VOLTARGET ab 07:00, wenn heute (Zuerich) noch kein Lauf protokolliert ist.
# Beide Runner rechnen idempotent ab ihrem Startbar und warten selbst auf einen laufenden Collector.
ran_today() {
  python3 - "$1" "$today" <<'PY' 2>/dev/null
import json, sys, datetime as dt, zoneinfo
z = zoneinfo.ZoneInfo("Europe/Zurich"); hit = False
try:
    for l in open(sys.argv[1]):
        t = json.loads(l).get("run_utc")
        if t and dt.datetime.fromisoformat(t.replace("Z", "+00:00")).astimezone(z).strftime("%F") == sys.argv[2]:
            hit = True
except OSError:
    pass
print("1" if hit else "0")
PY
}
if [ "$now_hm" -ge 0655 ] && [ -x "$REPO/sleeves/run_sleeves.sh" ] && [ "$(ran_today /workspace/aurum2/paper_sleeves/logs/run_history.jsonl)" != "1" ]; then
  nohup "$REPO/sleeves/run_sleeves.sh" >/dev/null 2>&1 &
fi
if [ "$now_hm" -ge 0700 ] && [ -x "$REPO/voltarget/run_voltarget.sh" ] && [ "$(ran_today /workspace/aurum2/paper_voltarget/logs/run_history.jsonl)" != "1" ]; then
  nohup "$REPO/voltarget/run_voltarget.sh" >/dev/null 2>&1 &
fi
# Paper-Runner nachholen (wartet selbst auf einen laufenden Collector; prueft selbst, ob noetig)
if [ "$now_hm" -ge 0650 ] && [ -x "$REPO/paper/run_paper.sh" ]; then
  nohup "$REPO/paper/run_paper.sh" --if-needed >/dev/null 2>&1 &
fi
exit 0
