#!/bin/bash
# Project Aurum II — 03_mtp_validation: Kraken-OHLCVT-Archiv (offiziell, 2026Q2) laden, pruefen, zehn Tagesdateien extrahieren
cd "$(dirname "$0")" || exit 1
echo "Project Aurum II — Kraken-Archiv 2026Q2 (ca. 10 GB Download, danach nur zehn kleine Dateien)"
echo "Freier Speicher wird gebraucht: rund 22 GB (Teile plus zusammengesetztes Archiv), danach loeschbar."
python3 kraken_archiv.py
echo
echo "Fertig. Fenster kann geschlossen werden."
read -r -p "Enter zum Schliessen..." _
