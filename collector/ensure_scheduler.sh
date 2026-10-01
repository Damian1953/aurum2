#!/usr/bin/env bash
# Stellt sicher, dass der taegliche Collector geplant ist (Box ohne systemd: PID 1 ist tini).
#  1. cron-Daemon starten, falls er nicht laeuft (nach Box-Neustart noetig)
#  2. crontab-Eintrag setzen, falls er fehlt
#  3. Nachholen: wenn heute nach 06:15 (Zuerich) noch kein erfolgreicher Lauf war, sofort im Hintergrund starten
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
exit 0
