#!/bin/bash
# Project Aurum II — 04_xrp_specialist / 05_dot_specialist: 4h-Kerzen und Vollspalten nachladen
cd "$(dirname "$0")" || exit 1
echo "Project Aurum II — Datennachladen fuer XRP- und DOT-Specialist"
echo "Schritt 1 und 2: Binance Vision Spot und Perp, Tages- und 4h-Kerzen mit allen Spalten, zehn Coins (20 bis 40 Minuten)"
echo "Schritt 3: Kraken 240-Minuten-Kerzen aus dem vorhandenen Archiv 2026Q2 (kein neuer Download)"
echo "Schritt 4: Kraken API 240 Minuten als Ergaenzung, Zusammenfuehrung mit Naht"
echo "Kann unterbrochen und spaeter fortgesetzt werden, vorhandene Dateien werden ergaenzt."
echo
python3 nachladen_4h.py
echo
echo "Fertig. Protokoll: raw/nachladen_4h.log, Herkunft und Pruefsummen: raw/provenance_4h.json"
read -r -p "Enter zum Schliessen..." _
