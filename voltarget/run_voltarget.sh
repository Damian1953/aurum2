#!/usr/bin/env bash
# Cron-Wrapper VOLTARGET v1.0 (eingefroren 2026-10-02, Tag voltarget-v1.0-freeze). cron 07:00 Zuerich (aurum2-voltarget,
# collector/ensure_scheduler.sh). Keine Keys, keine Orders, keine Boersenverbindung. Exit = Exit-Code des Laufs.
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
export AURUM_DATA_LIVE="${AURUM_DATA_LIVE:-/workspace/aurum2/data_live}"
export AURUM_VOLTARGET_OUT="${AURUM_VOLTARGET_OUT:-/workspace/aurum2/paper_voltarget}"
export TZ=Europe/Zurich PYTHONDONTWRITEBYTECODE=1
mkdir -p "$AURUM_VOLTARGET_OUT/logs"
LOG="$AURUM_VOLTARGET_OUT/logs/cron.log"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3
exec 9>"$AURUM_VOLTARGET_OUT/.runner.lock"
flock -n 9 || { echo "$(date -Iseconds) Lock belegt, Abbruch" >> "$LOG"; exit 2; }
flock -w 2400 "$AURUM_DATA_LIVE/.collector.lock" true 2>/dev/null
echo "$(date -Iseconds) START voltarget ($*)" >> "$LOG"
"$PY" "$REPO/voltarget/run_voltarget.py" "$@" >> "$LOG" 2>&1; rc=$?
echo "$(date -Iseconds) ENDE voltarget rc=$rc" >> "$LOG"
exit "$rc"
