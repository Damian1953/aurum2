# Stufe 1 — Robustheitsbericht

**Project Aurum II. Rechenlauf vom 2026-09-15. Vorregistrierung Version 1.0, SHA-256 `e7b28d3396ad1257…`, eingefroren am 15.09.2026.**

Alle Schwellen stammen aus der eingefrorenen Vorregistrierung. Kein Wert wurde nach dem Lauf verändert. Jede gerechnete Konfiguration inklusive Jitter steht in `stage1_config_log.csv`.

## 1. Urteil je Kandidat

| Kandidat | Urteil | Dimensionen bestanden | Bemerkung |
|---|---|---|---|
| R1 | **VERWORFEN** | 0 von 2 | D1: verworfen, D2: verworfen |
| R2 | **VERWORFEN** | 0 von 3 | D1: verworfen, D2: verworfen, D3: verworfen |
| R3 | **VERWORFEN** | 0 von 4 | D1: verworfen, D2: verworfen, D3: verworfen, D4: verworfen |
| R4 | **VERWORFEN** | 0 von 3 | D1: verworfen, D2: verworfen, D3: verworfen |
| R5 | **VERWORFEN** | 0 von 3 | D1: verworfen, D2: verworfen, D3: verworfen |
| F1 | **VERWORFEN (vorläufig)** | – | Funding, nur BTC, ETH, SOL ab 10.09.2025 |

**Kein Kandidat besteht.** Die Nullhypothese aus Abschnitt 1 der Vorregistrierung ist nicht widerlegt. Siehe `stage1_summary.md` für die Einordnung.

## 2. Gesamtmetriken je Kandidat, Coin und Dimension

Volle Historie je Coin nach Warmup. Dwell ist der Median der Verweildauer in Bars. Schwellen: Dwell ≥ 10 (häufige Zustände) beziehungsweise ≥ 5 (seltene), Ein-Bar ≤ 25 %, Wechsel D1/D2 ≤ 30, D3 ≤ 12, D4 ≤ 30 je 252 Bars, Jitter Mittel ≥ 85 % und Minimum ≥ 75 %, Kalenderjahr-Blöcke ≥ 70 % bestanden ohne Faktor-2-Ausreisser.

### R1

| Coin | Dim | Dwell je Zustand | Anteil je Zustand | Ein-Bar | Wechsel/Jahr | Jitter Mittel / Min | Blöcke bestanden | Urteil | Grund |
|---|---|---|---|---|---|---|---|---|---|
| BTC | D1 | UP 9.0, DOWN 3.0, RANGE 14.0 | UP 41 %, DOWN 36 %, RANGE 23 % | 17 % | 13.5 | 95 % / 91 % | 0 % | verworfen | Dwell UP 9.0 < 10, Dwell DOWN 3.0 < 10 | Blöcke 0 % |
| BTC | D2 | SQUEEZE 10.0, NORMAL 12.0, EXPANSION 13.0 | SQUEEZE 25 %, NORMAL 57 %, EXPANSION 18 % | 5 % | 17.4 | 92 % / 91 % | 56 % | verworfen | Blöcke 56 % |
| ETH | D1 | UP 7.5, RANGE 10.0, DOWN 4.0 | UP 40 %, RANGE 19 %, DOWN 41 % | 20 % | 13.5 | 95 % / 92 % | 22 % | verworfen | Dwell UP 7.5 < 10, Dwell DOWN 4.0 < 10 | Blöcke 22 %, Faktor 2 |
| ETH | D2 | NORMAL 13.0, SQUEEZE 8.0, EXPANSION 13.0 | NORMAL 56 %, SQUEEZE 24 %, EXPANSION 20 % | 7 % | 18.3 | 92 % / 90 % | 67 % | verworfen | Blöcke 67 % |
| SOL | D1 | DOWN 4.0, RANGE 13.0, UP 5.0 | DOWN 33 %, RANGE 29 %, UP 38 % | 17 % | 15.8 | 95 % / 92 % | 0 % | verworfen | Dwell DOWN 4.0 < 10, Dwell UP 5.0 < 10 | Blöcke 0 % |
| SOL | D2 | NORMAL 12.0, SQUEEZE 7.0, EXPANSION 10.0 | NORMAL 56 %, SQUEEZE 27 %, EXPANSION 17 % | 5 % | 21.3 | 92 % / 90 % | 50 % | verworfen | Blöcke 50 % |
| XRP | D1 | DOWN 6.0, RANGE 14.0, UP 6.0 | DOWN 38 %, RANGE 33 %, UP 28 % | 13 % | 13.8 | 95 % / 92 % | 0 % | verworfen | Dwell DOWN 6.0 < 10, Dwell UP 6.0 < 10 | Blöcke 0 % |
| XRP | D2 | SQUEEZE 8.0, NORMAL 10.0, EXPANSION 13.5 | SQUEEZE 25 %, NORMAL 55 %, EXPANSION 19 % | 4 % | 18.0 | 90 % / 89 % | 62 % | verworfen | Blöcke 62 % |
| ADA | D1 | DOWN 16.0, RANGE 9.5, UP 8.0 | DOWN 42 %, RANGE 28 %, UP 31 % | 15 % | 12.7 | 95 % / 90 % | 12 % | verworfen | Dwell RANGE 9.5 < 10, Dwell UP 8.0 < 10 | Blöcke 12 % |
| ADA | D2 | NORMAL 11.0, SQUEEZE 8.0, EXPANSION 11.0 | NORMAL 57 %, SQUEEZE 24 %, EXPANSION 19 % | 8 % | 21.2 | 90 % / 89 % | 75 % | ok |  |
| AVAX | D1 | RANGE 12.0, DOWN 7.0, UP 8.0 | RANGE 28 %, DOWN 44 %, UP 28 % | 16 % | 13.2 | 95 % / 91 % | 20 % | verworfen | Dwell DOWN 7.0 < 10, Dwell UP 8.0 < 10 | Blöcke 20 %, Faktor 2 |
| AVAX | D2 | NORMAL 10.0, SQUEEZE 6.5, EXPANSION 12.0 | NORMAL 57 %, SQUEEZE 27 %, EXPANSION 17 % | 8 % | 20.3 | 91 % / 89 % | 40 % | verworfen | Blöcke 40 % |
| LINK | D1 | RANGE 10.0, UP 4.5, DOWN 6.5 | RANGE 29 %, UP 35 %, DOWN 36 % | 15 % | 13.3 | 96 % / 92 % | 29 % | verworfen | Dwell UP 4.5 < 10, Dwell DOWN 6.5 < 10 | Blöcke 29 %, Faktor 2 |
| LINK | D2 | EXPANSION 12.0, NORMAL 9.5, SQUEEZE 6.0 | EXPANSION 18 %, NORMAL 57 %, SQUEEZE 25 % | 9 % | 20.6 | 92 % / 90 % | 29 % | verworfen | Dwell NORMAL 9.5 < 10 | Blöcke 29 % |
| DOT | D1 | UP 6.5, RANGE 12.0, DOWN 15.5 | UP 24 %, RANGE 27 %, DOWN 49 % | 14 % | 12.7 | 95 % / 90 % | 50 % | verworfen | Dwell UP 6.5 < 10 | Blöcke 50 % |
| DOT | D2 | NORMAL 9.0, EXPANSION 8.0, SQUEEZE 6.0 | NORMAL 58 %, EXPANSION 16 %, SQUEEZE 25 % | 11 % | 21.9 | 91 % / 90 % | 33 % | verworfen | Dwell NORMAL 9.0 < 10 | Blöcke 33 % |
| BNB | D1 | UP 4.0, RANGE 13.0, DOWN 5.0 | UP 35 %, RANGE 36 %, DOWN 29 % | 18 % | 15.5 | 95 % / 91 % | 12 % | verworfen | Dwell UP 4.0 < 10, Dwell DOWN 5.0 < 10 | Blöcke 12 % |
| BNB | D2 | SQUEEZE 7.0, NORMAL 9.0, EXPANSION 12.0 | SQUEEZE 26 %, NORMAL 54 %, EXPANSION 19 % | 9 % | 18.8 | 90 % / 89 % | 38 % | verworfen | Dwell NORMAL 9.0 < 10 | Blöcke 38 % |
| LTC | D1 | DOWN 8.0, UP 5.5, RANGE 12.0 | DOWN 40 %, UP 26 %, RANGE 34 % | 14 % | 14.8 | 95 % / 90 % | 12 % | verworfen | Dwell DOWN 8.0 < 10, Dwell UP 5.5 < 10 | Blöcke 12 % |
| LTC | D2 | NORMAL 11.0, SQUEEZE 8.0, EXPANSION 11.0 | NORMAL 54 %, SQUEEZE 26 %, EXPANSION 20 % | 4 % | 19.1 | 91 % / 89 % | 75 % | ok |  |

### R2

| Coin | Dim | Dwell je Zustand | Anteil je Zustand | Ein-Bar | Wechsel/Jahr | Jitter Mittel / Min | Blöcke bestanden | Urteil | Grund |
|---|---|---|---|---|---|---|---|---|---|
| BTC | D1 | UP 9.5, RANGE 7.5, DOWN 17.0 | UP 34 %, RANGE 35 %, DOWN 31 % | 16 % | 14.1 | 93 % / 93 % | 33 % | verworfen | Dwell UP 9.5 < 10, Dwell RANGE 7.5 < 10 | Blöcke 33 % |
| BTC | D2 | SQUEEZE 10.0, NORMAL 12.0, EXPANSION 13.0 | SQUEEZE 25 %, NORMAL 57 %, EXPANSION 18 % | 5 % | 17.4 | 92 % / 91 % | 56 % | verworfen | Blöcke 56 % |
| BTC | D3 | CALM 4.5, STRESS_DOWN 3.0, STRESS_UP 4.5 | CALM 80 %, STRESS_DOWN 8 %, STRESS_UP 12 % | 31 % | 10.4 | 96 % / 96 % | 11 % | verworfen | Dwell CALM 4.5 < 10, Dwell STRESS_DOWN 3.0 < 5, Dwell STRESS_UP 4.5 < 5, Ein-Bar 31% > 25% | Blöcke 11 %, Faktor 2 |
| ETH | D1 | UP 8.5, RANGE 8.0, DOWN 12.0 | UP 32 %, RANGE 36 %, DOWN 32 % | 19 % | 13.8 | 93 % / 91 % | 22 % | verworfen | Dwell UP 8.5 < 10, Dwell RANGE 8.0 < 10 | Blöcke 22 %, Faktor 2 |
| ETH | D2 | NORMAL 13.0, SQUEEZE 8.0, EXPANSION 13.0 | NORMAL 56 %, SQUEEZE 24 %, EXPANSION 20 % | 7 % | 18.3 | 92 % / 90 % | 67 % | verworfen | Blöcke 67 % |
| ETH | D3 | CALM 4.0, STRESS_DOWN 3.5, STRESS_UP 2.0 | CALM 77 %, STRESS_DOWN 12 %, STRESS_UP 11 % | 31 % | 14.4 | 96 % / 95 % | 11 % | verworfen | Dwell CALM 4.0 < 10, Dwell STRESS_DOWN 3.5 < 5, Dwell STRESS_UP 2.0 < 5, Ein-Bar 31% > 25%, Wechsel 14.4 > 12 | Blöcke 11 %, Faktor 2 |
| SOL | D1 | DOWN 7.5, RANGE 8.5, UP 6.0 | DOWN 26 %, RANGE 42 %, UP 32 % | 16 % | 15.2 | 94 % / 93 % | 33 % | verworfen | Dwell DOWN 7.5 < 10, Dwell RANGE 8.5 < 10, Dwell UP 6.0 < 10 | Blöcke 33 %, Faktor 2 |
| SOL | D2 | NORMAL 12.0, SQUEEZE 7.0, EXPANSION 10.0 | NORMAL 56 %, SQUEEZE 27 %, EXPANSION 17 % | 5 % | 21.3 | 92 % / 90 % | 50 % | verworfen | Blöcke 50 % |
| SOL | D3 | CALM 12.0, STRESS_UP 3.0, STRESS_DOWN 5.0 | CALM 78 %, STRESS_UP 10 %, STRESS_DOWN 12 % | 25 % | 8.7 | 98 % / 96 % | 33 % | verworfen | Dwell STRESS_UP 3.0 < 5 | Blöcke 33 %, Faktor 2 |
| XRP | D1 | DOWN 9.0, RANGE 11.0, UP 7.5 | DOWN 28 %, RANGE 51 %, UP 20 % | 14 % | 14.4 | 93 % / 91 % | 12 % | verworfen | Dwell DOWN 9.0 < 10, Dwell UP 7.5 < 10 | Blöcke 12 % |
| XRP | D2 | SQUEEZE 8.0, NORMAL 10.0, EXPANSION 13.5 | SQUEEZE 25 %, NORMAL 55 %, EXPANSION 19 % | 4 % | 18.0 | 90 % / 89 % | 62 % | verworfen | Blöcke 62 % |
| XRP | D3 | CALM 6.0, STRESS_UP 2.5, STRESS_DOWN 2.0 | CALM 80 %, STRESS_UP 12 %, STRESS_DOWN 8 % | 26 % | 12.5 | 96 % / 95 % | 0 % | verworfen | Dwell CALM 6.0 < 10, Dwell STRESS_UP 2.5 < 5, Dwell STRESS_DOWN 2.0 < 5, Ein-Bar 26% > 25%, Wechsel 12.5 > 12 | Blöcke 0 %, Faktor 2 |
| ADA | D1 | DOWN 18.5, RANGE 10.0, UP 12.5 | DOWN 36 %, RANGE 38 %, UP 26 % | 15 % | 12.8 | 94 % / 92 % | 38 % | verworfen | Blöcke 38 %, Faktor 2 |
| ADA | D2 | NORMAL 11.0, SQUEEZE 8.0, EXPANSION 11.0 | NORMAL 57 %, SQUEEZE 24 %, EXPANSION 19 % | 8 % | 21.2 | 90 % / 89 % | 75 % | ok |  |
| ADA | D3 | CALM 4.0, STRESS_UP 3.0, STRESS_DOWN 2.5 | CALM 75 %, STRESS_UP 15 %, STRESS_DOWN 11 % | 33 % | 15.2 | 97 % / 95 % | 12 % | verworfen | Dwell CALM 4.0 < 10, Dwell STRESS_UP 3.0 < 5, Dwell STRESS_DOWN 2.5 < 5, Ein-Bar 33% > 25%, Wechsel 15.2 > 12 | Blöcke 12 %, Faktor 2 |
| AVAX | D1 | RANGE 12.0, UP 10.5, DOWN 11.0 | RANGE 39 %, UP 23 %, DOWN 38 % | 13 % | 12.9 | 94 % / 92 % | 20 % | verworfen | Blöcke 20 %, Faktor 2 |
| AVAX | D2 | NORMAL 10.0, SQUEEZE 6.5, EXPANSION 12.0 | NORMAL 57 %, SQUEEZE 27 %, EXPANSION 17 % | 8 % | 20.3 | 91 % / 89 % | 40 % | verworfen | Blöcke 40 % |
| AVAX | D3 | STRESS_DOWN 2.0, CALM 6.0, STRESS_UP 4.0 | STRESS_DOWN 11 %, CALM 79 %, STRESS_UP 9 % | 33 % | 10.1 | 98 % / 94 % | 20 % | verworfen | Dwell STRESS_DOWN 2.0 < 5, Dwell CALM 6.0 < 10, Dwell STRESS_UP 4.0 < 5, Ein-Bar 33% > 25% | Blöcke 20 % |
| LINK | D1 | RANGE 8.0, UP 8.0, DOWN 7.0 | RANGE 43 %, UP 28 %, DOWN 29 % | 14 % | 14.4 | 93 % / 92 % | 14 % | verworfen | Dwell RANGE 8.0 < 10, Dwell UP 8.0 < 10, Dwell DOWN 7.0 < 10 | Blöcke 14 %, Faktor 2 |
| LINK | D2 | EXPANSION 12.0, NORMAL 9.5, SQUEEZE 6.0 | EXPANSION 18 %, NORMAL 57 %, SQUEEZE 25 % | 9 % | 20.6 | 92 % / 90 % | 29 % | verworfen | Dwell NORMAL 9.5 < 10 | Blöcke 29 % |
| LINK | D3 | CALM 4.0, STRESS_UP 5.0, STRESS_DOWN 3.0 | CALM 75 %, STRESS_UP 14 %, STRESS_DOWN 10 % | 24 % | 12.1 | 97 % / 96 % | 29 % | verworfen | Dwell CALM 4.0 < 10, Dwell STRESS_DOWN 3.0 < 5, Wechsel 12.1 > 12 | Blöcke 29 %, Faktor 2 |
| DOT | D1 | UP 7.0, RANGE 12.0, DOWN 19.0 | UP 19 %, RANGE 37 %, DOWN 45 % | 12 % | 13.5 | 93 % / 91 % | 67 % | verworfen | Dwell UP 7.0 < 10 | Blöcke 67 % |
| DOT | D2 | NORMAL 9.0, EXPANSION 8.0, SQUEEZE 6.0 | NORMAL 58 %, EXPANSION 16 %, SQUEEZE 25 % | 11 % | 21.9 | 91 % / 90 % | 33 % | verworfen | Dwell NORMAL 9.0 < 10 | Blöcke 33 % |
| DOT | D3 | CALM 2.0, STRESS_UP 3.0, STRESS_DOWN 3.0 | CALM 77 %, STRESS_UP 10 %, STRESS_DOWN 13 % | 33 % | 13.2 | 97 % / 96 % | 0 % | verworfen | Dwell CALM 2.0 < 10, Dwell STRESS_UP 3.0 < 5, Dwell STRESS_DOWN 3.0 < 5, Ein-Bar 33% > 25%, Wechsel 13.2 > 12 | Blöcke 0 %, Faktor 2 |
| BNB | D1 | UP 7.0, RANGE 12.0, DOWN 7.0 | UP 28 %, RANGE 50 %, DOWN 21 % | 15 % | 14.8 | 93 % / 93 % | 12 % | verworfen | Dwell UP 7.0 < 10, Dwell DOWN 7.0 < 10 | Blöcke 12 % |
| BNB | D2 | SQUEEZE 7.0, NORMAL 9.0, EXPANSION 12.0 | SQUEEZE 26 %, NORMAL 54 %, EXPANSION 19 % | 9 % | 18.8 | 90 % / 89 % | 38 % | verworfen | Dwell NORMAL 9.0 < 10 | Blöcke 38 % |
| BNB | D3 | CALM 3.0, STRESS_DOWN 3.0, STRESS_UP 5.0 | CALM 80 %, STRESS_DOWN 7 %, STRESS_UP 13 % | 30 % | 10.8 | 97 % / 96 % | 12 % | verworfen | Dwell CALM 3.0 < 10, Dwell STRESS_DOWN 3.0 < 5, Ein-Bar 30% > 25% | Blöcke 12 %, Faktor 2 |
| LTC | D1 | DOWN 11.0, RANGE 12.0, UP 8.0 | DOWN 34 %, RANGE 45 %, UP 21 % | 13 % | 13.5 | 94 % / 92 % | 12 % | verworfen | Dwell UP 8.0 < 10 | Blöcke 12 % |
| LTC | D2 | NORMAL 11.0, SQUEEZE 8.0, EXPANSION 11.0 | NORMAL 54 %, SQUEEZE 26 %, EXPANSION 20 % | 4 % | 19.1 | 91 % / 89 % | 75 % | ok |  |
| LTC | D3 | CALM 10.0, STRESS_DOWN 2.0, STRESS_UP 4.0 | CALM 81 %, STRESS_DOWN 9 %, STRESS_UP 10 % | 27 % | 10.9 | 97 % / 97 % | 12 % | verworfen | Dwell STRESS_DOWN 2.0 < 5, Dwell STRESS_UP 4.0 < 5, Ein-Bar 27% > 25% | Blöcke 12 %, Faktor 2 |

### R3

| Coin | Dim | Dwell je Zustand | Anteil je Zustand | Ein-Bar | Wechsel/Jahr | Jitter Mittel / Min | Blöcke bestanden | Urteil | Grund |
|---|---|---|---|---|---|---|---|---|---|
| BTC | D1 | UP 9.5, RANGE 7.5, DOWN 17.0 | UP 34 %, RANGE 35 %, DOWN 31 % | 16 % | 14.1 | 93 % / 93 % | 33 % | verworfen | Dwell UP 9.5 < 10, Dwell RANGE 7.5 < 10 | Blöcke 33 % |
| BTC | D2 | SQUEEZE 10.0, NORMAL 12.0, EXPANSION 13.0 | SQUEEZE 25 %, NORMAL 57 %, EXPANSION 18 % | 5 % | 17.4 | 92 % / 91 % | 56 % | verworfen | Blöcke 56 % |
| BTC | D3 | CALM 4.5, STRESS_DOWN 3.0, STRESS_UP 4.5 | CALM 80 %, STRESS_DOWN 8 %, STRESS_UP 12 % | 31 % | 10.4 | 96 % / 96 % | 11 % | verworfen | Dwell CALM 4.5 < 10, Dwell STRESS_DOWN 3.0 < 5, Dwell STRESS_UP 4.5 < 5, Ein-Bar 31% > 25% | Blöcke 11 %, Faktor 2 |
| BTC | D4 | CONFIRMED 2.0, UNCONFIRMED 2.0 | CONFIRMED 50 %, UNCONFIRMED 50 % | 35 % | 61.4 | 95 % / 94 % | 0 % | verworfen | Dwell CONFIRMED 2.0 < 10, Dwell UNCONFIRMED 2.0 < 10, Ein-Bar 35% > 25%, Wechsel 61.4 > 30 | Blöcke 0 % |
| ETH | D1 | UP 8.5, RANGE 8.0, DOWN 12.0 | UP 32 %, RANGE 36 %, DOWN 32 % | 19 % | 13.8 | 93 % / 91 % | 22 % | verworfen | Dwell UP 8.5 < 10, Dwell RANGE 8.0 < 10 | Blöcke 22 %, Faktor 2 |
| ETH | D2 | NORMAL 13.0, SQUEEZE 8.0, EXPANSION 13.0 | NORMAL 56 %, SQUEEZE 24 %, EXPANSION 20 % | 7 % | 18.3 | 92 % / 90 % | 67 % | verworfen | Blöcke 67 % |
| ETH | D3 | CALM 4.0, STRESS_DOWN 3.5, STRESS_UP 2.0 | CALM 77 %, STRESS_DOWN 12 %, STRESS_UP 11 % | 31 % | 14.4 | 96 % / 95 % | 11 % | verworfen | Dwell CALM 4.0 < 10, Dwell STRESS_DOWN 3.5 < 5, Dwell STRESS_UP 2.0 < 5, Ein-Bar 31% > 25%, Wechsel 14.4 > 12 | Blöcke 11 %, Faktor 2 |
| ETH | D4 | CONFIRMED 2.0, UNCONFIRMED 2.0 | CONFIRMED 52 %, UNCONFIRMED 48 % | 36 % | 56.6 | 94 % / 93 % | 0 % | verworfen | Dwell CONFIRMED 2.0 < 10, Dwell UNCONFIRMED 2.0 < 10, Ein-Bar 36% > 25%, Wechsel 56.6 > 30 | Blöcke 0 % |
| SOL | D1 | DOWN 7.5, RANGE 8.5, UP 6.0 | DOWN 26 %, RANGE 42 %, UP 32 % | 16 % | 15.2 | 94 % / 93 % | 33 % | verworfen | Dwell DOWN 7.5 < 10, Dwell RANGE 8.5 < 10, Dwell UP 6.0 < 10 | Blöcke 33 %, Faktor 2 |
| SOL | D2 | NORMAL 12.0, SQUEEZE 7.0, EXPANSION 10.0 | NORMAL 56 %, SQUEEZE 27 %, EXPANSION 17 % | 5 % | 21.3 | 92 % / 90 % | 50 % | verworfen | Blöcke 50 % |
| SOL | D3 | CALM 12.0, STRESS_UP 3.0, STRESS_DOWN 5.0 | CALM 78 %, STRESS_UP 10 %, STRESS_DOWN 12 % | 25 % | 8.7 | 98 % / 96 % | 33 % | verworfen | Dwell STRESS_UP 3.0 < 5 | Blöcke 33 %, Faktor 2 |
| SOL | D4 | CONFIRMED 2.0, UNCONFIRMED 2.0 | CONFIRMED 47 %, UNCONFIRMED 53 % | 40 % | 63.2 | 95 % / 95 % | 0 % | verworfen | Dwell CONFIRMED 2.0 < 10, Dwell UNCONFIRMED 2.0 < 10, Ein-Bar 40% > 25%, Wechsel 63.2 > 30 | Blöcke 0 % |
| XRP | D1 | DOWN 9.0, RANGE 11.0, UP 7.5 | DOWN 28 %, RANGE 51 %, UP 20 % | 14 % | 14.4 | 93 % / 91 % | 12 % | verworfen | Dwell DOWN 9.0 < 10, Dwell UP 7.5 < 10 | Blöcke 12 % |
| XRP | D2 | SQUEEZE 8.0, NORMAL 10.0, EXPANSION 13.5 | SQUEEZE 25 %, NORMAL 55 %, EXPANSION 19 % | 4 % | 18.0 | 90 % / 89 % | 62 % | verworfen | Blöcke 62 % |
| XRP | D3 | CALM 6.0, STRESS_UP 2.5, STRESS_DOWN 2.0 | CALM 80 %, STRESS_UP 12 %, STRESS_DOWN 8 % | 26 % | 12.5 | 96 % / 95 % | 0 % | verworfen | Dwell CALM 6.0 < 10, Dwell STRESS_UP 2.5 < 5, Dwell STRESS_DOWN 2.0 < 5, Ein-Bar 26% > 25%, Wechsel 12.5 > 12 | Blöcke 0 %, Faktor 2 |
| XRP | D4 | CONFIRMED 2.0, UNCONFIRMED 2.0 | CONFIRMED 48 %, UNCONFIRMED 52 % | 34 % | 58.0 | 95 % / 95 % | 0 % | verworfen | Dwell CONFIRMED 2.0 < 10, Dwell UNCONFIRMED 2.0 < 10, Ein-Bar 34% > 25%, Wechsel 58.0 > 30 | Blöcke 0 % |
| ADA | D1 | DOWN 18.5, RANGE 10.0, UP 12.5 | DOWN 36 %, RANGE 38 %, UP 26 % | 15 % | 12.8 | 94 % / 92 % | 38 % | verworfen | Blöcke 38 %, Faktor 2 |
| ADA | D2 | NORMAL 11.0, SQUEEZE 8.0, EXPANSION 11.0 | NORMAL 57 %, SQUEEZE 24 %, EXPANSION 19 % | 8 % | 21.2 | 90 % / 89 % | 75 % | ok |  |
| ADA | D3 | CALM 4.0, STRESS_UP 3.0, STRESS_DOWN 2.5 | CALM 75 %, STRESS_UP 15 %, STRESS_DOWN 11 % | 33 % | 15.2 | 97 % / 95 % | 12 % | verworfen | Dwell CALM 4.0 < 10, Dwell STRESS_UP 3.0 < 5, Dwell STRESS_DOWN 2.5 < 5, Ein-Bar 33% > 25%, Wechsel 15.2 > 12 | Blöcke 12 %, Faktor 2 |
| ADA | D4 | CONFIRMED 2.0, UNCONFIRMED 2.0 | CONFIRMED 49 %, UNCONFIRMED 51 % | 37 % | 58.4 | 95 % / 94 % | 0 % | verworfen | Dwell CONFIRMED 2.0 < 10, Dwell UNCONFIRMED 2.0 < 10, Ein-Bar 37% > 25%, Wechsel 58.4 > 30 | Blöcke 0 % |
| AVAX | D1 | RANGE 12.0, UP 10.5, DOWN 11.0 | RANGE 39 %, UP 23 %, DOWN 38 % | 13 % | 12.9 | 94 % / 92 % | 20 % | verworfen | Blöcke 20 %, Faktor 2 |
| AVAX | D2 | NORMAL 10.0, SQUEEZE 6.5, EXPANSION 12.0 | NORMAL 57 %, SQUEEZE 27 %, EXPANSION 17 % | 8 % | 20.3 | 91 % / 89 % | 40 % | verworfen | Blöcke 40 % |
| AVAX | D3 | STRESS_DOWN 2.0, CALM 6.0, STRESS_UP 4.0 | STRESS_DOWN 11 %, CALM 79 %, STRESS_UP 9 % | 33 % | 10.1 | 98 % / 94 % | 20 % | verworfen | Dwell STRESS_DOWN 2.0 < 5, Dwell CALM 6.0 < 10, Dwell STRESS_UP 4.0 < 5, Ein-Bar 33% > 25% | Blöcke 20 % |
| AVAX | D4 | UNCONFIRMED 2.0, CONFIRMED 2.0 | UNCONFIRMED 51 %, CONFIRMED 49 % | 40 % | 61.7 | 95 % / 93 % | 0 % | verworfen | Dwell UNCONFIRMED 2.0 < 10, Dwell CONFIRMED 2.0 < 10, Ein-Bar 40% > 25%, Wechsel 61.7 > 30 | Blöcke 0 % |
| LINK | D1 | RANGE 8.0, UP 8.0, DOWN 7.0 | RANGE 43 %, UP 28 %, DOWN 29 % | 14 % | 14.4 | 93 % / 92 % | 14 % | verworfen | Dwell RANGE 8.0 < 10, Dwell UP 8.0 < 10, Dwell DOWN 7.0 < 10 | Blöcke 14 %, Faktor 2 |
| LINK | D2 | EXPANSION 12.0, NORMAL 9.5, SQUEEZE 6.0 | EXPANSION 18 %, NORMAL 57 %, SQUEEZE 25 % | 9 % | 20.6 | 92 % / 90 % | 29 % | verworfen | Dwell NORMAL 9.5 < 10 | Blöcke 29 % |
| LINK | D3 | CALM 4.0, STRESS_UP 5.0, STRESS_DOWN 3.0 | CALM 75 %, STRESS_UP 14 %, STRESS_DOWN 10 % | 24 % | 12.1 | 97 % / 96 % | 29 % | verworfen | Dwell CALM 4.0 < 10, Dwell STRESS_DOWN 3.0 < 5, Wechsel 12.1 > 12 | Blöcke 29 %, Faktor 2 |
| LINK | D4 | CONFIRMED 2.0, UNCONFIRMED 3.0 | CONFIRMED 46 %, UNCONFIRMED 54 % | 38 % | 59.0 | 94 % / 94 % | 0 % | verworfen | Dwell CONFIRMED 2.0 < 10, Dwell UNCONFIRMED 3.0 < 10, Ein-Bar 38% > 25%, Wechsel 59.0 > 30 | Blöcke 0 % |
| DOT | D1 | UP 7.0, RANGE 12.0, DOWN 19.0 | UP 19 %, RANGE 37 %, DOWN 45 % | 12 % | 13.5 | 93 % / 91 % | 67 % | verworfen | Dwell UP 7.0 < 10 | Blöcke 67 % |
| DOT | D2 | NORMAL 9.0, EXPANSION 8.0, SQUEEZE 6.0 | NORMAL 58 %, EXPANSION 16 %, SQUEEZE 25 % | 11 % | 21.9 | 91 % / 90 % | 33 % | verworfen | Dwell NORMAL 9.0 < 10 | Blöcke 33 % |
| DOT | D3 | CALM 2.0, STRESS_UP 3.0, STRESS_DOWN 3.0 | CALM 77 %, STRESS_UP 10 %, STRESS_DOWN 13 % | 33 % | 13.2 | 97 % / 96 % | 0 % | verworfen | Dwell CALM 2.0 < 10, Dwell STRESS_UP 3.0 < 5, Dwell STRESS_DOWN 3.0 < 5, Ein-Bar 33% > 25%, Wechsel 13.2 > 12 | Blöcke 0 %, Faktor 2 |
| DOT | D4 | CONFIRMED 2.0, UNCONFIRMED 2.0 | CONFIRMED 45 %, UNCONFIRMED 55 % | 40 % | 61.2 | 94 % / 94 % | 0 % | verworfen | Dwell CONFIRMED 2.0 < 10, Dwell UNCONFIRMED 2.0 < 10, Ein-Bar 40% > 25%, Wechsel 61.2 > 30 | Blöcke 0 % |
| BNB | D1 | UP 7.0, RANGE 12.0, DOWN 7.0 | UP 28 %, RANGE 50 %, DOWN 21 % | 15 % | 14.8 | 93 % / 93 % | 12 % | verworfen | Dwell UP 7.0 < 10, Dwell DOWN 7.0 < 10 | Blöcke 12 % |
| BNB | D2 | SQUEEZE 7.0, NORMAL 9.0, EXPANSION 12.0 | SQUEEZE 26 %, NORMAL 54 %, EXPANSION 19 % | 9 % | 18.8 | 90 % / 89 % | 38 % | verworfen | Dwell NORMAL 9.0 < 10 | Blöcke 38 % |
| BNB | D3 | CALM 3.0, STRESS_DOWN 3.0, STRESS_UP 5.0 | CALM 80 %, STRESS_DOWN 7 %, STRESS_UP 13 % | 30 % | 10.8 | 97 % / 96 % | 12 % | verworfen | Dwell CALM 3.0 < 10, Dwell STRESS_DOWN 3.0 < 5, Ein-Bar 30% > 25% | Blöcke 12 %, Faktor 2 |
| BNB | D4 | UNCONFIRMED 3.0, CONFIRMED 2.0 | UNCONFIRMED 58 %, CONFIRMED 42 % | 40 % | 45.0 | 94 % / 93 % | 0 % | verworfen | Dwell UNCONFIRMED 3.0 < 10, Dwell CONFIRMED 2.0 < 10, Ein-Bar 40% > 25%, Wechsel 45.0 > 30 | Blöcke 0 %, Faktor 2 |
| LTC | D1 | DOWN 11.0, RANGE 12.0, UP 8.0 | DOWN 34 %, RANGE 45 %, UP 21 % | 13 % | 13.5 | 94 % / 92 % | 12 % | verworfen | Dwell UP 8.0 < 10 | Blöcke 12 % |
| LTC | D2 | NORMAL 11.0, SQUEEZE 8.0, EXPANSION 11.0 | NORMAL 54 %, SQUEEZE 26 %, EXPANSION 20 % | 4 % | 19.1 | 91 % / 89 % | 75 % | ok |  |
| LTC | D3 | CALM 10.0, STRESS_DOWN 2.0, STRESS_UP 4.0 | CALM 81 %, STRESS_DOWN 9 %, STRESS_UP 10 % | 27 % | 10.9 | 97 % / 97 % | 12 % | verworfen | Dwell STRESS_DOWN 2.0 < 5, Dwell STRESS_UP 4.0 < 5, Ein-Bar 27% > 25% | Blöcke 12 %, Faktor 2 |
| LTC | D4 | CONFIRMED 2.0, UNCONFIRMED 3.0 | CONFIRMED 50 %, UNCONFIRMED 50 % | 39 % | 53.6 | 95 % / 94 % | 0 % | verworfen | Dwell CONFIRMED 2.0 < 10, Dwell UNCONFIRMED 3.0 < 10, Ein-Bar 39% > 25%, Wechsel 53.6 > 30 | Blöcke 0 % |

### R4

| Coin | Dim | Dwell je Zustand | Anteil je Zustand | Ein-Bar | Wechsel/Jahr | Jitter Mittel / Min | Blöcke bestanden | Urteil | Grund |
|---|---|---|---|---|---|---|---|---|---|
| BTC | D1 | UP 6.0, RANGE 13.0, DOWN 16.0 | UP 25 %, RANGE 52 %, DOWN 22 % | 15 % | 12.4 | 94 % / 93 % | 33 % | verworfen | Dwell UP 6.0 < 10 | Blöcke 33 % |
| BTC | D2 | SQUEEZE 10.0, NORMAL 12.0, EXPANSION 13.0 | SQUEEZE 25 %, NORMAL 57 %, EXPANSION 18 % | 5 % | 17.4 | 92 % / 91 % | 56 % | verworfen | Blöcke 56 % |
| BTC | D3 | CALM 4.5, STRESS_DOWN 3.0, STRESS_UP 4.5 | CALM 80 %, STRESS_DOWN 8 %, STRESS_UP 12 % | 31 % | 10.4 | 96 % / 96 % | 11 % | verworfen | Dwell CALM 4.5 < 10, Dwell STRESS_DOWN 3.0 < 5, Dwell STRESS_UP 4.5 < 5, Ein-Bar 31% > 25% | Blöcke 11 %, Faktor 2 |
| ETH | D1 | UP 13.0, RANGE 17.0, DOWN 28.0 | UP 23 %, RANGE 52 %, DOWN 25 % | 13 % | 10.4 | 95 % / 94 % | 56 % | verworfen | Blöcke 56 %, Faktor 2 |
| ETH | D2 | NORMAL 13.0, SQUEEZE 8.0, EXPANSION 13.0 | NORMAL 56 %, SQUEEZE 24 %, EXPANSION 20 % | 7 % | 18.3 | 92 % / 90 % | 67 % | verworfen | Blöcke 67 % |
| ETH | D3 | CALM 4.0, STRESS_DOWN 3.5, STRESS_UP 2.0 | CALM 77 %, STRESS_DOWN 12 %, STRESS_UP 11 % | 31 % | 14.4 | 96 % / 95 % | 11 % | verworfen | Dwell CALM 4.0 < 10, Dwell STRESS_DOWN 3.5 < 5, Dwell STRESS_UP 2.0 < 5, Ein-Bar 31% > 25%, Wechsel 14.4 > 12 | Blöcke 11 %, Faktor 2 |
| SOL | D1 | DOWN 25.0, RANGE 12.0, UP 6.0 | DOWN 18 %, RANGE 59 %, UP 23 % | 19 % | 11.4 | 95 % / 93 % | 33 % | verworfen | Dwell UP 6.0 < 10 | Blöcke 33 %, Faktor 2 |
| SOL | D2 | NORMAL 12.0, SQUEEZE 7.0, EXPANSION 10.0 | NORMAL 56 %, SQUEEZE 27 %, EXPANSION 17 % | 5 % | 21.3 | 92 % / 90 % | 50 % | verworfen | Blöcke 50 % |
| SOL | D3 | CALM 12.0, STRESS_UP 3.0, STRESS_DOWN 5.0 | CALM 78 %, STRESS_UP 10 %, STRESS_DOWN 12 % | 25 % | 8.7 | 98 % / 96 % | 33 % | verworfen | Dwell STRESS_UP 3.0 < 5 | Blöcke 33 %, Faktor 2 |
| XRP | D1 | DOWN 9.0, RANGE 21.0, UP 10.5 | DOWN 20 %, RANGE 64 %, UP 16 % | 12 % | 11.1 | 95 % / 93 % | 25 % | verworfen | Dwell DOWN 9.0 < 10 | Blöcke 25 % |
| XRP | D2 | SQUEEZE 8.0, NORMAL 10.0, EXPANSION 13.5 | SQUEEZE 25 %, NORMAL 55 %, EXPANSION 19 % | 4 % | 18.0 | 90 % / 89 % | 62 % | verworfen | Blöcke 62 % |
| XRP | D3 | CALM 6.0, STRESS_UP 2.5, STRESS_DOWN 2.0 | CALM 80 %, STRESS_UP 12 %, STRESS_DOWN 8 % | 26 % | 12.5 | 96 % / 95 % | 0 % | verworfen | Dwell CALM 6.0 < 10, Dwell STRESS_UP 2.5 < 5, Dwell STRESS_DOWN 2.0 < 5, Ein-Bar 26% > 25%, Wechsel 12.5 > 12 | Blöcke 0 %, Faktor 2 |
| ADA | D1 | RANGE 16.5, DOWN 14.0, UP 13.0 | RANGE 56 %, DOWN 25 %, UP 19 % | 13 % | 10.8 | 95 % / 93 % | 50 % | verworfen | Blöcke 50 % |
| ADA | D2 | NORMAL 11.0, SQUEEZE 8.0, EXPANSION 11.0 | NORMAL 57 %, SQUEEZE 24 %, EXPANSION 19 % | 8 % | 21.2 | 90 % / 89 % | 75 % | ok |  |
| ADA | D3 | CALM 4.0, STRESS_UP 3.0, STRESS_DOWN 2.5 | CALM 75 %, STRESS_UP 15 %, STRESS_DOWN 11 % | 33 % | 15.2 | 97 % / 95 % | 12 % | verworfen | Dwell CALM 4.0 < 10, Dwell STRESS_UP 3.0 < 5, Dwell STRESS_DOWN 2.5 < 5, Ein-Bar 33% > 25%, Wechsel 15.2 > 12 | Blöcke 12 %, Faktor 2 |
| AVAX | D1 | RANGE 23.0, UP 13.0, DOWN 15.5 | RANGE 58 %, UP 16 %, DOWN 27 % | 5 % | 9.0 | 95 % / 93 % | 60 % | verworfen | Blöcke 60 % |
| AVAX | D2 | NORMAL 10.0, SQUEEZE 6.5, EXPANSION 12.0 | NORMAL 57 %, SQUEEZE 27 %, EXPANSION 17 % | 8 % | 20.3 | 91 % / 89 % | 40 % | verworfen | Blöcke 40 % |
| AVAX | D3 | STRESS_DOWN 2.0, CALM 6.0, STRESS_UP 4.0 | STRESS_DOWN 11 %, CALM 79 %, STRESS_UP 9 % | 33 % | 10.1 | 98 % / 94 % | 20 % | verworfen | Dwell STRESS_DOWN 2.0 < 5, Dwell CALM 6.0 < 10, Dwell STRESS_UP 4.0 < 5, Ein-Bar 33% > 25% | Blöcke 20 % |
| LINK | D1 | RANGE 13.0, UP 7.5, DOWN 5.0 | RANGE 59 %, UP 21 %, DOWN 19 % | 13 % | 13.4 | 94 % / 93 % | 14 % | verworfen | Dwell UP 7.5 < 10, Dwell DOWN 5.0 < 10 | Blöcke 14 % |
| LINK | D2 | EXPANSION 12.0, NORMAL 9.5, SQUEEZE 6.0 | EXPANSION 18 %, NORMAL 57 %, SQUEEZE 25 % | 9 % | 20.6 | 92 % / 90 % | 29 % | verworfen | Dwell NORMAL 9.5 < 10 | Blöcke 29 % |
| LINK | D3 | CALM 4.0, STRESS_UP 5.0, STRESS_DOWN 3.0 | CALM 75 %, STRESS_UP 14 %, STRESS_DOWN 10 % | 24 % | 12.1 | 97 % / 96 % | 29 % | verworfen | Dwell CALM 4.0 < 10, Dwell STRESS_DOWN 3.0 < 5, Wechsel 12.1 > 12 | Blöcke 29 %, Faktor 2 |
| DOT | D1 | RANGE 21.0, UP 10.0, DOWN 19.0 | RANGE 57 %, UP 13 %, DOWN 30 % | 5 % | 10.0 | 95 % / 92 % | 50 % | verworfen | Blöcke 50 % |
| DOT | D2 | NORMAL 9.0, EXPANSION 8.0, SQUEEZE 6.0 | NORMAL 58 %, EXPANSION 16 %, SQUEEZE 25 % | 11 % | 21.9 | 91 % / 90 % | 33 % | verworfen | Dwell NORMAL 9.0 < 10 | Blöcke 33 % |
| DOT | D3 | CALM 2.0, STRESS_UP 3.0, STRESS_DOWN 3.0 | CALM 77 %, STRESS_UP 10 %, STRESS_DOWN 13 % | 33 % | 13.2 | 97 % / 96 % | 0 % | verworfen | Dwell CALM 2.0 < 10, Dwell STRESS_UP 3.0 < 5, Dwell STRESS_DOWN 3.0 < 5, Ein-Bar 33% > 25%, Wechsel 13.2 > 12 | Blöcke 0 %, Faktor 2 |
| BNB | D1 | RANGE 25.5, UP 7.0, DOWN 13.0 | RANGE 64 %, UP 22 %, DOWN 14 % | 10 % | 9.3 | 96 % / 96 % | 25 % | verworfen | Dwell UP 7.0 < 10 | Blöcke 25 % |
| BNB | D2 | SQUEEZE 7.0, NORMAL 9.0, EXPANSION 12.0 | SQUEEZE 26 %, NORMAL 54 %, EXPANSION 19 % | 9 % | 18.8 | 90 % / 89 % | 38 % | verworfen | Dwell NORMAL 9.0 < 10 | Blöcke 38 % |
| BNB | D3 | CALM 3.0, STRESS_DOWN 3.0, STRESS_UP 5.0 | CALM 80 %, STRESS_DOWN 7 %, STRESS_UP 13 % | 30 % | 10.8 | 97 % / 96 % | 12 % | verworfen | Dwell CALM 3.0 < 10, Dwell STRESS_DOWN 3.0 < 5, Ein-Bar 30% > 25% | Blöcke 12 %, Faktor 2 |
| LTC | D1 | DOWN 13.0, RANGE 21.5, UP 9.0 | DOWN 24 %, RANGE 60 %, UP 15 % | 12 % | 10.9 | 96 % / 94 % | 25 % | verworfen | Dwell UP 9.0 < 10 | Blöcke 25 %, Faktor 2 |
| LTC | D2 | NORMAL 11.0, SQUEEZE 8.0, EXPANSION 11.0 | NORMAL 54 %, SQUEEZE 26 %, EXPANSION 20 % | 4 % | 19.1 | 91 % / 89 % | 75 % | ok |  |
| LTC | D3 | CALM 10.0, STRESS_DOWN 2.0, STRESS_UP 4.0 | CALM 81 %, STRESS_DOWN 9 %, STRESS_UP 10 % | 27 % | 10.9 | 97 % / 97 % | 12 % | verworfen | Dwell STRESS_DOWN 2.0 < 5, Dwell STRESS_UP 4.0 < 5, Ein-Bar 27% > 25% | Blöcke 12 %, Faktor 2 |

### R5

| Coin | Dim | Dwell je Zustand | Anteil je Zustand | Ein-Bar | Wechsel/Jahr | Jitter Mittel / Min | Blöcke bestanden | Urteil | Grund |
|---|---|---|---|---|---|---|---|---|---|
| BTC | D1 | UP 8.0, RANGE 5.0, DOWN 15.5 | UP 42 %, RANGE 20 %, DOWN 38 % | 21 % | 13.4 | 94 % / 92 % | 0 % | verworfen | Dwell UP 8.0 < 10, Dwell RANGE 5.0 < 10 | Blöcke 0 % |
| BTC | D2 | SQUEEZE 4.0, NORMAL 5.0, EXPANSION 4.0 | SQUEEZE 30 %, NORMAL 52 %, EXPANSION 18 % | 24 % | 20.9 | 90 % / 88 % | 0 % | verworfen | Dwell SQUEEZE 4.0 < 5, Dwell NORMAL 5.0 < 10, Dwell EXPANSION 4.0 < 5 | Blöcke 0 % |
| BTC | D3 | CALM 9.0, STRESS_DOWN 4.0, STRESS_UP 4.5 | CALM 76 %, STRESS_DOWN 12 %, STRESS_UP 12 % | 26 % | 10.1 | 97 % / 94 % | 33 % | verworfen | Dwell CALM 9.0 < 10, Dwell STRESS_DOWN 4.0 < 5, Dwell STRESS_UP 4.5 < 5, Ein-Bar 26% > 25% | Blöcke 33 %, Faktor 2 |
| ETH | D1 | UP 8.5, RANGE 3.0, DOWN 6.5 | UP 40 %, RANGE 24 %, DOWN 36 % | 23 % | 14.0 | 94 % / 90 % | 11 % | verworfen | Dwell UP 8.5 < 10, Dwell RANGE 3.0 < 10, Dwell DOWN 6.5 < 10 | Blöcke 11 % |
| ETH | D2 | NORMAL 4.0, SQUEEZE 5.0, EXPANSION 2.0 | NORMAL 53 %, SQUEEZE 27 %, EXPANSION 19 % | 29 % | 23.0 | 90 % / 88 % | 0 % | verworfen | Dwell NORMAL 4.0 < 10, Dwell EXPANSION 2.0 < 5, Ein-Bar 29% > 25% | Blöcke 0 % |
| ETH | D3 | CALM 5.0, STRESS_DOWN 2.0, STRESS_UP 3.5 | CALM 73 %, STRESS_DOWN 13 %, STRESS_UP 14 % | 27 % | 13.5 | 97 % / 94 % | 11 % | verworfen | Dwell CALM 5.0 < 10, Dwell STRESS_DOWN 2.0 < 5, Dwell STRESS_UP 3.5 < 5, Ein-Bar 27% > 25%, Wechsel 13.5 > 12 | Blöcke 11 %, Faktor 2 |
| SOL | D1 | DOWN 11.0, RANGE 5.0, UP 6.5 | DOWN 35 %, RANGE 28 %, UP 37 % | 18 % | 17.6 | 92 % / 90 % | 0 % | verworfen | Dwell RANGE 5.0 < 10, Dwell UP 6.5 < 10 | Blöcke 0 % |
| SOL | D2 | NORMAL 5.0, SQUEEZE 4.5, EXPANSION 5.0 | NORMAL 53 %, SQUEEZE 30 %, EXPANSION 18 % | 23 % | 23.4 | 91 % / 89 % | 0 % | verworfen | Dwell NORMAL 5.0 < 10, Dwell SQUEEZE 4.5 < 5 | Blöcke 0 % |
| SOL | D3 | CALM 6.5, STRESS_UP 3.0, STRESS_DOWN 4.0 | CALM 76 %, STRESS_UP 11 %, STRESS_DOWN 12 % | 24 % | 10.7 | 98 % / 96 % | 33 % | verworfen | Dwell CALM 6.5 < 10, Dwell STRESS_UP 3.0 < 5, Dwell STRESS_DOWN 4.0 < 5 | Blöcke 33 %, Faktor 2 |
| XRP | D1 | DOWN 5.0, RANGE 6.0, UP 6.5 | DOWN 36 %, RANGE 37 %, UP 27 % | 23 % | 19.7 | 91 % / 88 % | 12 % | verworfen | Dwell DOWN 5.0 < 10, Dwell RANGE 6.0 < 10, Dwell UP 6.5 < 10 | Blöcke 12 % |
| XRP | D2 | SQUEEZE 6.0, NORMAL 5.0, EXPANSION 5.0 | SQUEEZE 31 %, NORMAL 52 %, EXPANSION 18 % | 24 % | 22.5 | 90 % / 88 % | 12 % | verworfen | Dwell NORMAL 5.0 < 10 | Blöcke 12 % |
| XRP | D3 | CALM 4.0, STRESS_UP 3.0, STRESS_DOWN 2.0 | CALM 75 %, STRESS_UP 15 %, STRESS_DOWN 10 % | 32 % | 14.7 | 96 % / 93 % | 0 % | verworfen | Dwell CALM 4.0 < 10, Dwell STRESS_UP 3.0 < 5, Dwell STRESS_DOWN 2.0 < 5, Ein-Bar 32% > 25%, Wechsel 14.7 > 12 | Blöcke 0 %, Faktor 2 |
| ADA | D1 | DOWN 16.0, RANGE 6.0, UP 14.0 | DOWN 46 %, RANGE 22 %, UP 32 % | 15 % | 12.1 | 94 % / 92 % | 0 % | verworfen | Dwell RANGE 6.0 < 10 | Blöcke 0 % |
| ADA | D2 | SQUEEZE 3.0, NORMAL 4.0, EXPANSION 6.5 | SQUEEZE 27 %, NORMAL 53 %, EXPANSION 20 % | 23 % | 25.1 | 89 % / 86 % | 12 % | verworfen | Dwell SQUEEZE 3.0 < 5, Dwell NORMAL 4.0 < 10 | Blöcke 12 % |
| ADA | D3 | CALM 4.0, STRESS_UP 3.0, STRESS_DOWN 2.0 | CALM 73 %, STRESS_UP 16 %, STRESS_DOWN 11 % | 34 % | 15.6 | 97 % / 94 % | 12 % | verworfen | Dwell CALM 4.0 < 10, Dwell STRESS_UP 3.0 < 5, Dwell STRESS_DOWN 2.0 < 5, Ein-Bar 34% > 25%, Wechsel 15.6 > 12 | Blöcke 12 %, Faktor 2 |
| AVAX | D1 | RANGE 4.0, UP 7.0, DOWN 8.0 | RANGE 23 %, UP 29 %, DOWN 48 % | 21 % | 14.2 | 93 % / 91 % | 17 % | verworfen | Dwell RANGE 4.0 < 10, Dwell UP 7.0 < 10, Dwell DOWN 8.0 < 10 | Blöcke 17 %, Faktor 2 |
| AVAX | D2 | EXPANSION 6.0, NORMAL 4.0, SQUEEZE 4.0 | EXPANSION 16 %, NORMAL 53 %, SQUEEZE 30 % | 24 % | 23.0 | 90 % / 87 % | 17 % | verworfen | Dwell NORMAL 4.0 < 10, Dwell SQUEEZE 4.0 < 5 | Blöcke 17 % |
| AVAX | D3 | STRESS_DOWN 2.0, CALM 5.0, STRESS_UP 4.0 | STRESS_DOWN 11 %, CALM 79 %, STRESS_UP 10 % | 34 % | 10.8 | 97 % / 94 % | 0 % | verworfen | Dwell STRESS_DOWN 2.0 < 5, Dwell CALM 5.0 < 10, Dwell STRESS_UP 4.0 < 5, Ein-Bar 34% > 25% | Blöcke 0 % |
| LINK | D1 | RANGE 5.5, UP 6.5, DOWN 7.0 | RANGE 29 %, UP 37 %, DOWN 34 % | 17 % | 16.2 | 92 % / 89 % | 14 % | verworfen | Dwell RANGE 5.5 < 10, Dwell UP 6.5 < 10, Dwell DOWN 7.0 < 10 | Blöcke 14 %, Faktor 2 |
| LINK | D2 | SQUEEZE 4.0, NORMAL 4.0, EXPANSION 4.0 | SQUEEZE 29 %, NORMAL 52 %, EXPANSION 20 % | 20 % | 24.4 | 90 % / 89 % | 0 % | verworfen | Dwell SQUEEZE 4.0 < 5, Dwell NORMAL 4.0 < 10, Dwell EXPANSION 4.0 < 5 | Blöcke 0 % |
| LINK | D3 | CALM 5.0, STRESS_UP 5.0, STRESS_DOWN 3.0 | CALM 74 %, STRESS_UP 16 %, STRESS_DOWN 11 % | 27 % | 11.5 | 98 % / 95 % | 0 % | verworfen | Dwell CALM 5.0 < 10, Dwell STRESS_DOWN 3.0 < 5, Ein-Bar 27% > 25% | Blöcke 0 %, Faktor 2 |
| DOT | D1 | UP 9.0, RANGE 4.5, DOWN 13.5 | UP 24 %, RANGE 20 %, DOWN 57 % | 21 % | 13.7 | 94 % / 93 % | 0 % | verworfen | Dwell UP 9.0 < 10, Dwell RANGE 4.5 < 10 | Blöcke 0 % |
| DOT | D2 | NORMAL 4.0, EXPANSION 3.5, SQUEEZE 4.0 | NORMAL 52 %, EXPANSION 19 %, SQUEEZE 29 % | 30 % | 23.0 | 90 % / 88 % | 17 % | verworfen | Dwell NORMAL 4.0 < 10, Dwell EXPANSION 3.5 < 5, Dwell SQUEEZE 4.0 < 5, Ein-Bar 30% > 25% | Blöcke 17 %, Faktor 2 |
| DOT | D3 | CALM 4.0, STRESS_UP 1.5, STRESS_DOWN 2.0 | CALM 75 %, STRESS_UP 11 %, STRESS_DOWN 14 % | 35 % | 12.0 | 97 % / 95 % | 0 % | verworfen | Dwell CALM 4.0 < 10, Dwell STRESS_UP 1.5 < 5, Dwell STRESS_DOWN 2.0 < 5, Ein-Bar 35% > 25% | Blöcke 0 %, Faktor 2 |
| BNB | D1 | UP 11.0, RANGE 5.0, DOWN 5.0 | UP 38 %, RANGE 32 %, DOWN 30 % | 20 % | 17.7 | 92 % / 90 % | 0 % | verworfen | Dwell RANGE 5.0 < 10, Dwell DOWN 5.0 < 10 | Blöcke 0 % |
| BNB | D2 | SQUEEZE 3.0, NORMAL 5.0, EXPANSION 6.0 | SQUEEZE 29 %, NORMAL 51 %, EXPANSION 19 % | 24 % | 21.1 | 90 % / 89 % | 0 % | verworfen | Dwell SQUEEZE 3.0 < 5, Dwell NORMAL 5.0 < 10 | Blöcke 0 % |
| BNB | D3 | CALM 7.0, STRESS_DOWN 3.5, STRESS_UP 5.0 | CALM 76 %, STRESS_DOWN 9 %, STRESS_UP 15 % | 28 % | 10.7 | 97 % / 96 % | 50 % | verworfen | Dwell CALM 7.0 < 10, Dwell STRESS_DOWN 3.5 < 5, Ein-Bar 28% > 25% | Blöcke 50 %, Faktor 2 |
| LTC | D1 | DOWN 7.0, RANGE 5.0, UP 6.5 | DOWN 44 %, RANGE 26 %, UP 30 % | 22 % | 14.6 | 93 % / 92 % | 12 % | verworfen | Dwell DOWN 7.0 < 10, Dwell RANGE 5.0 < 10, Dwell UP 6.5 < 10 | Blöcke 12 %, Faktor 2 |
| LTC | D2 | SQUEEZE 5.0, NORMAL 6.0, EXPANSION 7.0 | SQUEEZE 28 %, NORMAL 53 %, EXPANSION 19 % | 24 % | 20.4 | 90 % / 89 % | 12 % | verworfen | Dwell NORMAL 6.0 < 10 | Blöcke 12 % |
| LTC | D3 | CALM 6.0, STRESS_DOWN 2.0, STRESS_UP 4.0 | CALM 76 %, STRESS_DOWN 11 %, STRESS_UP 13 % | 33 % | 13.3 | 97 % / 96 % | 25 % | verworfen | Dwell CALM 6.0 < 10, Dwell STRESS_DOWN 2.0 < 5, Dwell STRESS_UP 4.0 < 5, Ein-Bar 33% > 25%, Wechsel 13.3 > 12 | Blöcke 25 %, Faktor 2 |

## 3. Zeitblöcke, Kalenderjahre, Kernassets

Je Block das Urteil je Dimension. Ein Block gilt als bestanden, wenn Dwell, Ein-Bar und Wechselrate innerhalb der Schwellen liegen.

**R1 BTC**

| Block | D1 | D2 |
|---|---|---|
| 2018 | verworfen | verworfen |
| 2019 | verworfen | ok |
| 2020 | verworfen | ok |
| 2021 | verworfen | ok |
| 2022 | verworfen | verworfen |
| 2023 | verworfen | verworfen |
| 2024 | verworfen | ok |
| 2025 | verworfen | ok |
| 2026 | verworfen | verworfen |

**R1 ETH**

| Block | D1 | D2 |
|---|---|---|
| 2018 | ok | ok |
| 2019 | ok | ok |
| 2020 | verworfen | ok |
| 2021 | verworfen | ok |
| 2022 | verworfen | ok |
| 2023 | verworfen | ok |
| 2024 | verworfen | verworfen |
| 2025 | verworfen | verworfen |
| 2026 | verworfen | verworfen |

**R2 BTC**

| Block | D1 | D2 | D3 |
|---|---|---|---|
| 2018 | verworfen | verworfen | ok |
| 2019 | ok | ok | verworfen |
| 2020 | verworfen | ok | verworfen |
| 2021 | verworfen | ok | verworfen |
| 2022 | ok | verworfen | verworfen |
| 2023 | ok | verworfen | verworfen |
| 2024 | verworfen | ok | verworfen |
| 2025 | verworfen | ok | verworfen |
| 2026 | verworfen | verworfen | verworfen |

**R2 ETH**

| Block | D1 | D2 | D3 |
|---|---|---|---|
| 2018 | ok | ok | verworfen |
| 2019 | ok | ok | verworfen |
| 2020 | verworfen | ok | verworfen |
| 2021 | verworfen | ok | verworfen |
| 2022 | verworfen | ok | verworfen |
| 2023 | verworfen | ok | verworfen |
| 2024 | verworfen | verworfen | verworfen |
| 2025 | verworfen | verworfen | verworfen |
| 2026 | verworfen | verworfen | ok |

**R3 BTC**

| Block | D1 | D2 | D3 | D4 |
|---|---|---|---|---|
| 2018 | verworfen | verworfen | ok | verworfen |
| 2019 | ok | ok | verworfen | verworfen |
| 2020 | verworfen | ok | verworfen | verworfen |
| 2021 | verworfen | ok | verworfen | verworfen |
| 2022 | ok | verworfen | verworfen | verworfen |
| 2023 | ok | verworfen | verworfen | verworfen |
| 2024 | verworfen | ok | verworfen | verworfen |
| 2025 | verworfen | ok | verworfen | verworfen |
| 2026 | verworfen | verworfen | verworfen | verworfen |

**R3 ETH**

| Block | D1 | D2 | D3 | D4 |
|---|---|---|---|---|
| 2018 | ok | ok | verworfen | verworfen |
| 2019 | ok | ok | verworfen | verworfen |
| 2020 | verworfen | ok | verworfen | verworfen |
| 2021 | verworfen | ok | verworfen | verworfen |
| 2022 | verworfen | ok | verworfen | verworfen |
| 2023 | verworfen | ok | verworfen | verworfen |
| 2024 | verworfen | verworfen | verworfen | verworfen |
| 2025 | verworfen | verworfen | verworfen | verworfen |
| 2026 | verworfen | verworfen | ok | verworfen |

**R4 BTC**

| Block | D1 | D2 | D3 |
|---|---|---|---|
| 2018 | verworfen | verworfen | ok |
| 2019 | ok | ok | verworfen |
| 2020 | verworfen | ok | verworfen |
| 2021 | verworfen | ok | verworfen |
| 2022 | ok | verworfen | verworfen |
| 2023 | ok | verworfen | verworfen |
| 2024 | verworfen | ok | verworfen |
| 2025 | verworfen | ok | verworfen |
| 2026 | verworfen | verworfen | verworfen |

**R4 ETH**

| Block | D1 | D2 | D3 |
|---|---|---|---|
| 2018 | ok | ok | verworfen |
| 2019 | ok | ok | verworfen |
| 2020 | ok | ok | verworfen |
| 2021 | verworfen | ok | verworfen |
| 2022 | verworfen | ok | verworfen |
| 2023 | verworfen | ok | verworfen |
| 2024 | verworfen | verworfen | verworfen |
| 2025 | ok | verworfen | verworfen |
| 2026 | ok | verworfen | ok |

**R5 BTC**

| Block | D1 | D2 | D3 |
|---|---|---|---|
| 2018 | verworfen | verworfen | ok |
| 2019 | verworfen | verworfen | verworfen |
| 2020 | verworfen | verworfen | ok |
| 2021 | verworfen | verworfen | verworfen |
| 2022 | verworfen | verworfen | verworfen |
| 2023 | verworfen | verworfen | verworfen |
| 2024 | verworfen | verworfen | verworfen |
| 2025 | verworfen | verworfen | verworfen |
| 2026 | verworfen | verworfen | ok |

**R5 ETH**

| Block | D1 | D2 | D3 |
|---|---|---|---|
| 2018 | ok | verworfen | verworfen |
| 2019 | verworfen | verworfen | verworfen |
| 2020 | verworfen | verworfen | verworfen |
| 2021 | verworfen | verworfen | verworfen |
| 2022 | verworfen | verworfen | verworfen |
| 2023 | verworfen | verworfen | verworfen |
| 2024 | verworfen | verworfen | verworfen |
| 2025 | verworfen | verworfen | verworfen |
| 2026 | verworfen | verworfen | ok |

## 4. Halving-Zyklen, Gegenprobe (nur Bericht, kein Hard-Fail)

- **R1 BTC** — H1: D1 verworfen, D2 ok · H2: D1 verworfen, D2 ok · H3: D1 verworfen, D2 ok
- **R1 ETH** — H1: D1 verworfen, D2 ok · H2: D1 verworfen, D2 ok · H3: D1 verworfen, D2 verworfen
- **R2 BTC** — H1: D1 verworfen, D2 ok, D3 verworfen · H2: D1 ok, D2 ok, D3 verworfen · H3: D1 verworfen, D2 ok, D3 verworfen
- **R2 ETH** — H1: D1 ok, D2 ok, D3 verworfen · H2: D1 verworfen, D2 ok, D3 verworfen · H3: D1 verworfen, D2 verworfen, D3 verworfen
- **R3 BTC** — H1: D1 verworfen, D2 ok, D3 verworfen, D4 verworfen · H2: D1 ok, D2 ok, D3 verworfen, D4 verworfen · H3: D1 verworfen, D2 ok, D3 verworfen, D4 verworfen
- **R3 ETH** — H1: D1 ok, D2 ok, D3 verworfen, D4 verworfen · H2: D1 verworfen, D2 ok, D3 verworfen, D4 verworfen · H3: D1 verworfen, D2 verworfen, D3 verworfen, D4 verworfen
- **R4 BTC** — H1: D1 verworfen, D2 ok, D3 verworfen · H2: D1 verworfen, D2 ok, D3 verworfen · H3: D1 verworfen, D2 ok, D3 verworfen
- **R4 ETH** — H1: D1 ok, D2 ok, D3 verworfen · H2: D1 verworfen, D2 ok, D3 verworfen · H3: D1 ok, D2 verworfen, D3 verworfen
- **R5 BTC** — H1: D1 verworfen, D2 verworfen, D3 verworfen · H2: D1 verworfen, D2 verworfen, D3 verworfen · H3: D1 verworfen, D2 verworfen, D3 verworfen
- **R5 ETH** — H1: D1 ok, D2 verworfen, D3 verworfen · H2: D1 verworfen, D2 verworfen, D3 verworfen · H3: D1 verworfen, D2 verworfen, D3 verworfen

## 5. Kraken-Gegenprobe (Datenkonsistenz, Schwelle 90 %)

| Kandidat | Coin | D1 | D2 | D3 | D4 | Label |
|---|---|---|---|---|---|---|
| R1 | BTC | 96 % | 99 % | – | – | 95 % |
| R1 | ETH | 99 % | 100 % | – | – | 99 % |
| R1 | SOL | 98 % | 100 % | – | – | 98 % |
| R2 | BTC | 96 % | 99 % | 99 % | – | 94 % |
| R2 | ETH | 99 % | 100 % | 100 % | – | 98 % |
| R2 | SOL | 100 % | 100 % | 100 % | – | 100 % |
| R3 | BTC | 96 % | 99 % | 99 % | 83 % | 94 % |
| R3 | ETH | 99 % | 100 % | 100 % | 79 % | 98 % |
| R3 | SOL | 100 % | 100 % | 100 % | 78 % | 100 % |
| R4 | BTC | 99 % | 99 % | 99 % | – | 98 % |
| R4 | ETH | 99 % | 100 % | 100 % | – | 99 % |
| R4 | SOL | 99 % | 100 % | 100 % | – | 98 % |
| R5 | BTC | 97 % | 99 % | 99 % | – | 95 % |
| R5 | ETH | 100 % | 96 % | 100 % | – | 98 % |
| R5 | SOL | 100 % | 98 % | 100 % | – | 99 % |

Preisbasierte Dimensionen stimmen zwischen Binance-USDT und Kraken-USD zu 94 bis 100 Prozent überein. D4 (Volumen) liegt bei 79 bis 83 Prozent und verfehlt die Konsistenzschwelle, weil Volumen börsenspezifisch ist. Die Datengrundlage ist für D1 bis D3 belastbar.

## 6. Kandidat F1, Funding

| Coin | Zeitraum | Dwell je Zustand | Anteil je Zustand | Ein-Bar | Wechsel/Jahr | Jitter Mittel / Min | Urteil | Grund |
|---|---|---|---|---|---|---|---|---|
| BTC | 2025-09-10 bis 2026-09-13 | NEUTRAL 29.0, POS 4.0 | NEUTRAL 95 %, POS 5 % | 9 % | 7.0 | 92 % / 89 % | verworfen | Dwell POS 4.0 < 5 |
| ETH | 2025-09-10 bis 2026-09-13 | NEUTRAL 179.0, POS 4.0 | NEUTRAL 99 %, POS 1 % | 0 % | 1.4 | 95 % / 91 % | verworfen | Dwell POS 4.0 < 5 |
| SOL | 2025-09-10 bis 2026-09-13 | NEUTRAL 32.0, POS 7.0, NEG 8.0 | NEUTRAL 88 %, POS 5 %, NEG 7 % | 8 % | 8.4 | 96 % / 95 % | ok |  |

## 7. Umfang des Laufs

- Gerechnete Konfigurationen inklusive Jitter: 539 (siehe `stage1_config_log.csv`)
- Coins: BTC, ETH, SOL, XRP, ADA, AVAX, LINK, DOT, BNB, LTC. Alle mit mindestens 750 definierten Bars.
- Eingabedaten mit SHA-256 in `stage1_results.json`, Feld `inputs`.
- Verifikation: Look-ahead-Test bestanden (Labels bei am 30.06.2023 abgeschnittener Historie identisch mit dem Volllauf, 0 abweichende definierte Zellen). ATR und ADX gegen unabhängige Referenz auf 1e-11 identisch. Perzentilränge im Mittel 0.45 bis 0.50.
