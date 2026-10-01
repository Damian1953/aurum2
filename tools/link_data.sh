#!/usr/bin/env bash
# Richtet die nicht versionierten Rohdaten ein (siehe DATA.md).
# Quelle: AURUM_DATA_SRC (Default: /workspace/aurum2/projekt/02_daten/raw), wird KOPIERT (nie verlinkt),
# damit Loader-Skripte nie in die Originale schreiben koennen.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${AURUM_DATA_SRC:-/workspace/aurum2/projekt/02_daten/raw}"
DST="$REPO/data/raw"
if [ ! -d "$DST" ]; then
  [ -d "$SRC" ] || { echo "FEHLER: Quelle $SRC fehlt" >&2; exit 1; }
  mkdir -p "$REPO/data"
  echo "Kopiere $SRC -> $DST (ohne kraken_archiv/_download)"
  (cd "$SRC" && tar --exclude='./kraken_archiv/_download' -cf - .) | (mkdir -p "$DST" && cd "$DST" && tar -xf -)
fi
# 02_daten/raw -> ../data/raw (gitignored Symlink), damit die eingefrorenen Skripte ihre relativen Pfade finden
if [ ! -e "$REPO/02_daten/raw" ]; then ln -s ../data/raw "$REPO/02_daten/raw"; fi
# Ergaenzung: DTB3 T-Bill (fehlte in der Kopie, fuer Stufe-2-Reproduktion noetig)
SUP="$REPO/data/supplement/DTB3_3m_tbill.csv"
if [ ! -f "$SUP" ]; then
  mkdir -p "$REPO/data/supplement"
  echo "Lade DTB3 von FRED (oeffentlich) und schneide bei 2026-07-15 ab"
  curl -fsS -m 60 "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DTB3" \
    | awk -F, 'NR==1 || ($1<="2026-07-15" && $2!="" && $2!=".")' > "$SUP.tmp" && mv "$SUP.tmp" "$SUP"
fi
echo "OK: data/raw ($(du -sh "$DST" | cut -f1)), 02_daten/raw -> ../data/raw, $(basename "$SUP")"
