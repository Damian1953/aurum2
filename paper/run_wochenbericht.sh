#!/usr/bin/env bash
# Cron-Wrapper Wochenbericht Paper (montags). Schreibt nach $AURUM_PAPER_OUT/berichte/.
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
export AURUM_PAPER_OUT="${AURUM_PAPER_OUT:-/workspace/aurum2/paper}"
export TZ=Europe/Zurich PYTHONDONTWRITEBYTECODE=1
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3
"$REPO/paper/run_paper.sh" --if-needed >/dev/null 2>&1
"$PY" "$REPO/paper/wochenbericht.py" "$@" >> "$AURUM_PAPER_OUT/logs/cron.log" 2>&1
