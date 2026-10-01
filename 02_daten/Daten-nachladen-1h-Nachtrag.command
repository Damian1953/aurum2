#!/bin/bash
# Project Aurum II — Nachtrag 1h: Binance Spot 1h fuer BTC, ETH, BNB, LTC (Kerzen ausserhalb Raster vom 2018-02-09 werden quarantaeniert)
cd "$(dirname "$0")" || exit 1
echo "Project Aurum II — 1h-Nachtrag Binance Spot BTC, ETH, BNB, LTC (rund 8 Minuten)"
python3 nachladen_1h.py --coins BTC,ETH,BNB,LTC --nur-binance
echo
echo "Fertig. Protokoll: raw/nachladen_1h.log"
read -r -p "Enter zum Schliessen..." _
