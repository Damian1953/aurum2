#!/usr/bin/env bash
# Stellt sicher, dass der taegliche Collector geplant ist (Box ohne systemd: PID 1 ist tini).
#  1. cron-Daemon starten, falls er nicht laeuft (nach Box-Neustart noetig)
#  2. crontab-Eintrag setzen, falls er fehlt
#  3. Nachholen: wenn heute nach 06:15 (Zuerich) noch kein erfolgreicher Lauf war, sofort im Hintergrund starten
#  4. Paper-Runner (PAPER_PREREG_v1.0, D1): cron 06:50 taeglich und Wochenbericht montags 07:10 sicherstellen;
#     nach 06:50 nachholen, wenn der gestern abgeschlossene Tagesbar noch nicht verarbeitet ist (--if-needed)
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
for L in "$PLINE" "$BLINE"; do
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
# Sleeves A/B (MAKRO_LIQ/MVRV v0.2): Runner sleeves/run_sleeves.sh ist BEWUSST NICHT in cron (vor Freeze).
# Die Daten dafuer (coinmetrics_mvrv, fred_macro) sammelt der Collector ab 1.2 im 06:15-Lauf mit.
# Nach dem Freeze hier einen Eintrag "55 6 * * * $REPO/sleeves/run_sleeves.sh  # aurum2-sleeves" ergaenzen.
# Paper-Runner nachholen (wartet selbst auf einen laufenden Collector; prueft selbst, ob noetig)
if [ "$now_hm" -ge 0650 ] && [ -x "$REPO/paper/run_paper.sh" ]; then
  nohup "$REPO/paper/run_paper.sh" --if-needed >/dev/null 2>&1 &
fi
exit 0
