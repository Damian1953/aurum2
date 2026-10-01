# REBOUND-MICRO — 1h-Datenaudit, Version 0.1

**Project Aurum II, `01_forschung/10_rebound_micro/rebound_micro_1h_data_audit_v0.1.md`. 18.09.2026. Binance Spot und Perp 1h für BTC, XRP, DOT, Discovery-Schnitt 2023-12-31 23:00 UTC. Quelle: Loader `nachladen_1h.py` v2 (Provenance `provenance_1h.json`), Dateien byteidentisch mit dem Mac (SHA-Prüfung). Keine ETH- oder SOL-Dateien geladen.**

## 1. Abdeckung (Discovery)

| | BTC Spot | BTC Perp | XRP Spot | XRP Perp | DOT Spot | DOT Perp |
|---|---|---|---|---|---|---|
| Erste Kerze | 2017-08-17 04:00 | 2020-01-01 00:00 | 2018-05-04 08:00 | 2020-01-06 08:00 | 2020-08-18 23:00 | 2020-08-22 07:00 |
| Kerzen bis 2023-12-31 | 55698 | 35064 | 49537 | 34816 | 29502 | 29441 |
| Rasterlücken, fehlende Kerzen | 28, 170 | 0, 0 | 25, 87 | 2, 120 | 10, 19 | 0, 0 |
| Off-Grid-Kerzen in der Datei | 0 (43 quarantäniert, 09. bis 11.02.2018) | 0 | 0 | 0 | 0 | 0 |
| NaN, Nullvolumen | 0, 4 | 0, 1 | 0, 4 | 0, 1 | 0, 3 | 0, 1 |
| Zeitstempel monoton, Duplikate | ja, 0 | ja, 0 | ja, 0 | ja, 0 | ja, 0 | ja, 0 |
| SHA-256 (16) | 269b5fe188df0c5d | 1a8afb20a637dfc8 | 2e169dbdf38fa797 | 6b0273c7a4e1d528 | 3ff35b27d3f0a18c | b251bde45fe561a8 |

Lückenliste Spot (alle drei Coins teilen die Binance-Wartungsfenster): BTC zusätzlich 2017-09-06 (7 Kerzen), 2018-01-04 (1), 2018-02-08 bis 11 (75, das Off-Grid-Ereignis); gemeinsam 2018-06-26 (10), 2018-06-27 (1), 2018-07-04 (7), 2018-10-19 (3), 2018-11-14 (7), 2019-03-12 (6), 2019-05-15 (10), 2019-08-15 (8), 2019-11-13 (2), 2019-11-25 (2), 2020-02-09 (1), 2020-02-19 (5), 2020-03-04 (1), 2020-04-25 (2), 2020-06-28 (3), 2020-11-30 (1), 2020-12-21 (3), 2020-12-25 (1), 2021-02-11 (1), 2021-03-06 (1), 2021-04-20 (2), 2021-04-25 (3), 2021-08-13 (4), 2021-09-29 (2), 2023-03-24 (1). XRP Perp: 2022-02-25 bis 03-01 (72) und 2022-03-31 bis 04-03 (48), zwei mehrtägige Lücken, nur Diagnose betroffen. Kraken-1h-Nahtlücke (Archiv-Ende 2026-06-30 bis API-Start): betrifft nur Kraken-Reihen, die in diesem Zyklus nicht verwendet werden, dokumentiert im 1h-Provenance.

## 2. Join 4h → 1h

Je 4h-Discovery-Kerze wurden die enthaltenen 1h-Kerzen aggregiert und mit der 4h-Datei verglichen. BTC: 13950 4h-Kerzen, 13939 mit 1h-Kerzen, 13903 vollständig (vier 1h-Kerzen), 36 unvollständig (Lücken), 0 OHLC-Abweichungen bei vollständigen Kerzen, 5 Volumenabweichungen (Provenance-Crosscheck bekannt). XRP: 12397, 12397, 12364, 33 unvollständig, 0 OHLC-Abweichungen, 3 Volumen. DOT: 7381, 7381, 7367, 14 unvollständig, 0, 2. Der deterministische Join (4h-Kerze abgeschlossen vor Beginn der 1h-Kerze) ist in `mlib.join_4h` umgesetzt und getestet (Test 3).

## 3. Regel für Signale über Lücken

Ein Kontext-Event wird nur gezählt, wenn im Suchfenster und in den 168 1h-Kerzen davor (Feature-Warmup) keine Rasterlücke liegt. Ausgeschlossen: BTC 13 von 171 Events, XRP 17 von 165, DOT 5 von 94. Kandidaten in ausgeschlossenen Fenstern werden geführt, aber nicht gezählt (`gap_in_window`).

## 4. Flow-Felder

Spot: `quote_volume`, `trades`, `taker_buy_base`, `taker_buy_quote` in allen Zeilen vorhanden, keine NaN. Nullvolumen 3 bis 4 Kerzen je Coin (Wartungsränder), `taker_imbalance` dort NaN. Gültigkeitsanteil der Rolling-z-Merkmale (168-Kerzen-Fenster, lückenfrei): BTC 91.8, XRP 91.8, DOT 94.2 Prozent der Discovery-Kerzen. Perp-Diagnosejoin an den Kandidatenkerzen: BTC 105 von 169 (Perp erst ab 2020), XRP 92 von 156, DOT 100 von 100.

## 5. Bewertung

Die Datenbasis ist für den Development-Lauf ausreichend: Off-Grid-Ereignis quarantäniert, Lücken bekannt und in der Library fail-closed behandelt, Join deterministisch und ohne OHLC-Abweichung. Zwei Einschränkungen: BTC-Spot 2017 bis Anfang 2018 hat die dichteste Lückenfolge, dort fallen mehr Events aus; die XRP-Perp-Lücken 2022 schwächen nur die Diagnose.
