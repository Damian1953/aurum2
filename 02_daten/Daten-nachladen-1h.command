#!/bin/bash
# Project Aurum II — 1h-Kerzen fuer Entry-Bestaetigung und Kerzengrenzen-Diagnose nachladen
cd "$(dirname "$0")" || exit 1
echo "Project Aurum II — 1h-Daten (Binance Spot und Perp 1h alle Spalten, Kraken 60 Minuten aus dem Archiv, Kraken API 60)"
echo "Zehn Coins, rund 15 bis 30 Minuten. Kann unterbrochen und spaeter fortgesetzt werden."
echo
python3 nachladen_1h.py
echo
echo "Fertig. Protokoll: raw/nachladen_1h.log, Herkunft und Pruefsummen: raw/provenance_1h.json"
read -r -p "Enter zum Schliessen..." _
