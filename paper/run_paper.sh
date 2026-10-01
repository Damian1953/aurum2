#!/usr/bin/env bash
# Cron-Wrapper Paper-Runner (PAPER_PREREG_v1.0). Keine Keys, keine Orders. Exit = Exit-Code des Laufs.
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
export AURUM_DATA_LIVE="${AURUM_DATA_LIVE:-/workspace/aurum2/data_live}"
export AURUM_PAPER_OUT="${AURUM_PAPER_OUT:-/workspace/aurum2/paper}"
export TZ=Europe/Zurich PYTHONDONTWRITEBYTECODE=1
mkdir -p "$AURUM_PAPER_OUT/logs"
LOG="$AURUM_PAPER_OUT/logs/cron.log"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3
# warten, bis ein laufender Collector fertig ist (max. 40 min)
exec 9>"$AURUM_PAPER_OUT/.runner.lock"
flock -n 9 || { echo "$(date -Iseconds) Lock belegt, Abbruch" >> "$LOG"; exit 2; }
flock -w 2400 "$AURUM_DATA_LIVE/.collector.lock" true 2>/dev/null
echo "$(date -Iseconds) START runner ($*)" >> "$LOG"
"$PY" "$REPO/paper/run_paper.py" "$@" >> "$LOG" 2>&1; rc=$?
echo "$(date -Iseconds) ENDE runner rc=$rc" >> "$LOG"
exit "$rc"
