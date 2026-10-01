#!/usr/bin/env bash
# Wrapper fuer den taeglichen Lauf (cron). Ein zweiter Versuch nach 15 min, wenn der erste fehlschlaegt.
# Exit-Code = Exit-Code des letzten Versuchs (0 ok, 1 Quellenfehler, 2 Lock belegt).
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
export AURUM_DATA_LIVE="${AURUM_DATA_LIVE:-/workspace/aurum2/data_live}"
export TZ=Europe/Zurich PYTHONDONTWRITEBYTECODE=1
mkdir -p "$AURUM_DATA_LIVE/logs"
LOG="$AURUM_DATA_LIVE/logs/cron.log"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3
rc=1
for attempt in 1 2; do
  echo "$(date -Iseconds) START Versuch $attempt ($*)" >> "$LOG"
  "$PY" "$REPO/collector/collect.py" "$@" >> "$LOG" 2>&1; rc=$?
  echo "$(date -Iseconds) ENDE Versuch $attempt rc=$rc" >> "$LOG"
  [ "$rc" -eq 0 ] && break
  [ "$rc" -eq 2 ] && break
  [ "$attempt" -eq 1 ] && sleep "${AURUM_RETRY_WAIT:-900}"
done
exit "$rc"
