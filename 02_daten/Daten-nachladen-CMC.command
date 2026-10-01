#!/bin/bash
# Project Aurum II — 03_mtp_validation: CoinMarketCap USD-Tageshistorie fuer zehn Coins (Preisquelle des MTP-Backtesters)
cd "$(dirname "$0")" || exit 1
echo "Project Aurum II — CoinMarketCap-Historie, zehn Coins, ab 2013"
python3 nachladen_cmc.py
echo
echo "Fertig. Fenster kann geschlossen werden."
read -r -p "Enter zum Schliessen..." _
