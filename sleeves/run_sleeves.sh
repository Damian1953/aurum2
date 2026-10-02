#!/usr/bin/env bash
# Cron-Wrapper Sleeves A/B (eingefroren 2026-10-02, Tag sleeves-ab-v1.0-freeze). cron 06:55 Zuerich (aurum2-sleeves, collector/ensure_scheduler.sh). Keine Keys, keine Orders.
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
export AURUM_DATA_LIVE="${AURUM_DATA_LIVE:-/workspace/aurum2/data_live}"
export AURUM_SLEEVES_OUT="${AURUM_SLEEVES_OUT:-/workspace/aurum2/paper_sleeves}"
export TZ=Europe/Zurich PYTHONDONTWRITEBYTECODE=1
mkdir -p "$AURUM_SLEEVES_OUT/logs"
LOG="$AURUM_SLEEVES_OUT/logs/cron.log"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3
exec 9>"$AURUM_SLEEVES_OUT/.runner.lock"
flock -n 9 || { echo "$(date -Iseconds) Lock belegt, Abbruch" >> "$LOG"; exit 2; }
flock -w 2400 "$AURUM_DATA_LIVE/.collector.lock" true 2>/dev/null
echo "$(date -Iseconds) START sleeves ($*)" >> "$LOG"
"$PY" "$REPO/sleeves/run_sleeves.py" "$@" >> "$LOG" 2>&1; rc=$?
echo "$(date -Iseconds) ENDE sleeves rc=$rc" >> "$LOG"
exit "$rc"
