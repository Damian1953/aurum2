#!/bin/bash
# Project Aurum II — 03_woo_mtp_reverse_engineering: BTC/USD-Tageshistorie von Bitstamp und Coinbase
cd "$(dirname "$0")" || exit 1
echo "Project Aurum II — BTC/USD-Historie (Bitstamp ab 2011, Coinbase ab 2015)"
python3 nachladen_btc_historie.py
echo
echo "Fertig. Fenster kann geschlossen werden."
read -r -p "Enter zum Schliessen..." _
