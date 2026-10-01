#!/bin/bash
# Project Aurum II — Stufe 2: Binance Perpetuals nachladen (Funding, Perp-Kerzen, Open Interest)
cd "$(dirname "$0")" || exit 1
echo "Project Aurum II — Perpetual-Daten fuer Stufe 2"
echo "Schritt 1: Funding-Historie und Perp-Tageskerzen (einige Minuten)"
python3 nachladen_historie.py --futures
echo
echo "Schritt 2: Open Interest, Tagesdateien seit 2021 (langsam, kann unterbrochen und spaeter fortgesetzt werden)"
python3 nachladen_historie.py --oi
echo
echo "Fertig. Fenster kann geschlossen werden."
read -r -p "Enter zum Schliessen..." _
