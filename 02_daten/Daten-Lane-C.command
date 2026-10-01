#!/bin/bash
# Project Aurum II — Lane C: Kraken Futures Funding-Historie (offizieller Endpunkt) und Binance-UM-Universum inkl. delisteter Symbole
cd "$(dirname "$0")" || exit 1
echo "Project Aurum II — Lane C Daten (rund 5 bis 10 Minuten, alles kostenlos und offiziell)"
python3 nachladen_lane_c.py
echo
echo "Fertig. Protokoll: raw/nachladen_lane_c.log, Herkunft: raw/provenance_lane_c.json"
read -r -p "Enter zum Schliessen..." _
