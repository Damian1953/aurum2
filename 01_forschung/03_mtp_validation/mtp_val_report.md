# Validierungsstufe MTP — Bericht

**Project Aurum II, 03_mtp_validation. Lauf «out_full» vom 2026-09-17. Vorregistrierung v0.2 (SHA-256 `733bf2f5ccd709e8…`), Spezifikation v1 (`ed85be81521284bd…`), beide eingefroren am 17.09.2026. Zehn Coins, Ebenen A (Replikation CMC), B (Real Kraken), B2 (Signale auf Kraken), Sichten 1, 1b, 2, Kostenszenarien K0 bis K2, Bootstrap 2000 Wiederholungen. Alle Definitionen aus der Vorregistrierung, keine Änderung nach Kenntnis der Ergebnisse.**

**Urteil nach Vorregistrierung Abschnitt 8 (Ebene B, K1, handelbare Konvention, Sicht 1, Pool ohne BTC): VERWORFEN.**

Kontrollen vor dem Lauf: Look-ahead-Test bestanden (BTC und ETH, Niveau, Pivot, ATR und SMA auf abgeschnittener Historie identisch). BTC-Replikation der sechzehn Backtester-Trades in Ebene A: Entry-Tag 13 von 16, Exit-Tag 14 von 16, Exit-Preis unter 0.1 Prozent 10 von 16 (Erwartung 13, 13, 10).

## 1. Kriterien

| Kriterium | Ebene B, K1, Pool ohne BTC | Ebene A, ohne Kosten, Pool ohne BTC |
|---|---|---|
| 1 Erwartung R_gesamt > 0 und Profit-Faktor ≥ 1.5 | ja | ja |
| 2 ETH positiv und Mehrheit der übrigen Coins (≥ 10 Trades) | nein | ja |
| 3 mindestens zwei von drei Zeitblöcken positiv | nein | ja |
| 4 Bootstrap-5 %-Perzentil > 0 und Holm-p < 0.05 | nein | ja |
| 5 Beta-Trennung: Alpha oder Risikotransformation | nein | nein |
| 6 Edge-Retention ≥ 60 % und abweichender Exit-Grund ≤ 15 % | nein | – |
| 7 Trade-Mindestzahl (Pool ≥ 60, ETH ≥ 10) | ja | – |

Zu 2: ETH 10 Trades, Erwartung R_gesamt 0.48. Geeignete übrige Coins XRP, LINK, LTC, davon positiv XRP. Zu 6: Retention 0.37, abweichender Exit-Grund 1.19 %. Zu 7: geringe Trade-Basis. Holm-korrigierte p-Werte: A|none|1 0.000, B|K1|1 0.105, B2|K1|1 0.119.

## 2. Übersicht je Ebene, Sicht 1, Pool ohne BTC (mit BTC in Klammern)

| Ebene | Kosten | Trades | E[R_gesamt] | Median R_ges | E[R_first] | Profit-Faktor | Trefferquote | Ø Gewinner | Ø Verlierer | Ø Legs | Ø Halten | CAGR | MaxDD | Exposure |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A Sicht 1 | none | 102 (118) | 0.70 (0.74) | -0.52 | 2.63 | 4.51 (4.80) | 31.4 % | 21.6 % | -2.2 % | 2.2 | 110 d | 9.2 % | -9.5 % | 2.9 % |
| A Sicht 1 | K0 | 102 (118) | 0.69 (0.73) | -0.53 | 2.61 | 4.41 (4.69) | 31.4 % | 21.5 % | -2.2 % | 2.2 | 110 d | 9.1 % | -9.7 % | 2.9 % |
| A_window Sicht 1 | none | 68 (84) | 0.26 (0.41) | -0.61 | 1.94 | 3.32 (3.89) | 23.5 % | 23.7 % | -2.2 % | 2.2 | 121 d | 6.1 % | -5.1 % | 2.8 % |
| B Sicht 1 | K0 | 73 (89) | 0.12 (0.28) | -0.66 | 1.52 | 2.71 (3.30) | 20.5 % | 23.5 % | -2.2 % | 2.1 | 118 d | 6.5 % | -7.3 % | 3.4 % |
| B Sicht 1 | K1 | 73 (89) | 0.10 (0.26) | -0.67 | 1.47 | 2.61 (3.16) | 20.5 % | 23.3 % | -2.3 % | 2.1 | 118 d | 6.4 % | -7.4 % | 3.4 % |
| B Sicht 1 | K2 | 73 (89) | 0.06 (0.21) | -0.70 | 1.39 | 2.44 (2.92) | 20.5 % | 22.9 % | -2.4 % | 2.1 | 118 d | 6.2 % | -7.6 % | 3.4 % |
| B_sameday Sicht 1 | K1 | 73 (89) | 0.10 (0.25) | -0.68 | 1.47 | 2.61 (3.15) | 20.5 % | 23.3 % | -2.3 % | 2.1 | 118 d | 6.4 % | -7.4 % | 3.4 % |
| B_full Sicht 1 | K1 | 86 (102) | 0.28 (0.39) | -0.63 | 1.74 | 3.04 (3.49) | 25.6 % | 20.3 % | -2.3 % | 2.1 | 109 d | 7.1 % | -13.7 % | 3.2 % |
| B2 Sicht 1 | K0 | 51 (63) | 0.02 (0.35) | -0.65 | 1.63 | 2.79 (4.44) | 17.6 % | 28.8 % | -2.2 % | 2.3 | 158 d | 5.4 % | -6.6 % | 3.3 % |
| B2 Sicht 1 | K1 | 51 (63) | 0.00 (0.33) | -0.67 | 1.59 | 2.69 (4.25) | 17.6 % | 28.6 % | -2.3 % | 2.3 | 158 d | 5.4 % | -6.7 % | 3.3 % |
| B2 Sicht 1 | K2 | 51 (63) | -0.03 (0.29) | -0.71 | 1.50 | 2.51 (3.96) | 15.7 % | 31.8 % | -2.4 % | 2.3 | 158 d | 5.2 % | -6.9 % | 3.4 % |
| B Sicht 1b | K1 | 73 (89) | 0.08 (0.24) | -0.68 | 1.51 | 2.40 (2.93) | 20.5 % | 28.0 % | -3.0 % | 2.1 | 118 d | 6.6 % | -7.6 % | 4.0 % |
| A Sicht 1b | none | 102 (118) | 0.68 (0.72) | -0.53 | 2.69 | 3.87 (4.06) | 31.4 % | 33.4 % | -3.9 % | 2.2 | 110 d | 10.8 % | -10.8 % | 4.0 % |
| B Sicht 2 | K1 | 64 (79) | 0.26 (0.42) | -0.65 | 22.91 | 1.59 (1.89) | 18.8 % | 925.6 % | -134.3 % | 2.1 | 131 d | 20.3 % | -44.4 % | 29.0 % |

A_window ist Ebene A eingeschränkt auf das B-Fenster je Coin (Basis der Retention). CAGR und MaxDD sind Berichtswerte auf dem Sleeve-Mittel (Sicht 1, 2 Prozent Nominal Initial Risk je Leg ohne Compounding), keine Kriterien. Sicht 2 zeigt das gemeinsame Portfolio.

## 3a. Ergebnis je Coin, Ebene B, K1, Sicht 1

| Coin | Start | Trades | E[R_ges] | Med R_ges | E[R_first] | PF | Treffer | Ø Legs | Ø Halten | SL / TP | SL im Gewinn | Blöcke positiv | Anteil P&L | ohne grössten Gewinner E[R_ges] | grösster Anteil | CAGR | MaxDD | Recovery max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTC | 2014-12-26 | 16 | 0.98 | -0.27 | 3.91 | 6.24 | 44 % | 2.8 | 116 d | 69 % / 31 % | 18 % | 1 | 36.8 % | 0.78 | 31 % | 9.1 % | -15.5 % | 492 d |
| ETH | 2018-01-13 | 10 | 0.48 | -0.49 | 1.95 | 2.86 | 20 % | 2.6 | 113 d | 80 % / 20 % | 0 % | 0 | 11.5 % | -0.08 | 56 % | 6.3 % | -11.5 % | 767 d |
| SOL | 2021-06-17 | 6 | 1.07 | -0.51 | 4.76 | 7.24 | 33 % | 2.5 | 128 d | 67 % / 33 % | 0 % | 0 | 16.8 % | 0.38 | 55 % | 12.6 % | -5.6 % | 570 d |
| XRP | 2018-01-13 | 10 | 0.91 | -0.42 | 3.69 | 7.08 | 40 % | 2.2 | 142 d | 70 % / 30 % | 14 % | 0 | 21.7 % | 0.53 | 41 % | 8.8 % | -4.6 % | 422 d |
| ADA | 2018-10-01 | 8 | 0.33 | -1.02 | 3.46 | 5.08 | 25 % | 2.1 | 160 d | 75 % / 25 % | 0 % | 0 | 16.3 % | -0.07 | 55 % | 8.1 % | -14.1 % | 620 d |
| AVAX | 2021-12-21 | 6 | -0.67 | -0.92 | -0.88 | 0.05 | 17 % | 1.7 | 118 d | 100 % / 0 % | 17 % | 0 | -3.1 % | -0.83 | 100 % | 1.6 % | -6.4 % | 530 d |
| LINK | 2019-09-25 | 14 | -0.31 | -0.95 | 0.25 | 1.26 | 21 % | 1.7 | 85 d | 93 % / 7 % | 15 % | 0 | 2.0 % | -0.74 | 94 % | 3.8 % | -19.7 % | 24 d |
| DOT | 2021-08-20 | 6 | -0.75 | -0.71 | -1.23 | 0.00 | 0 % | 1.8 | 102 d | 100 % / 0 % | 0 % | 0 | -4.3 % | -0.70 | – | 0.7 % | -7.6 % | 757 d |
| BNB | 2025-04-22 | 1 | -0.36 | -0.36 | -0.73 | 0.00 | 0 % | 2.0 | 271 d | 100 % / 0 % | 0 % | 0 | -0.4 % | – | – | 3.0 % | -7.8 % | 16 d |
| LTC | 2018-01-13 | 12 | -0.22 | -0.57 | 0.41 | 1.40 | 8 % | 2.3 | 103 d | 92 % / 8 % | 0 % | 0 | 2.9 % | -0.63 | 100 % | 3.7 % | -16.2 % | 276 d |

## 3b. Ergebnis je Coin, Ebene A, ohne Kosten, Sicht 1

| Coin | Start | Trades | E[R_ges] | Med R_ges | E[R_first] | PF | Treffer | Ø Legs | Ø Halten | SL / TP | SL im Gewinn | Blöcke positiv | Anteil P&L | ohne grössten Gewinner E[R_ges] | grösster Anteil | CAGR | MaxDD | Recovery max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTC | 2014-04-28 | 16 | 1.04 | -0.20 | 4.05 | 6.85 | 38 % | 2.8 | 118 d | 69 % / 31 % | 9 % | 1 | 19.4 % | 0.83 | 31 % | 8.7 % | -15.1 % | 492 d |
| ETH | 2016-08-06 | 14 | 1.50 | -0.35 | 3.78 | 5.89 | 36 % | 2.4 | 99 d | 64 % / 36 % | 0 % | 1 | 15.9 % | 1.18 | 27 % | 9.7 % | -7.1 % | 698 d |
| SOL | 2021-04-10 | 6 | 1.11 | -0.48 | 4.85 | 7.74 | 33 % | 2.5 | 128 d | 67 % / 33 % | 0 % | 0 | 8.7 % | 0.42 | 55 % | 12.3 % | -5.7 % | 567 d |
| XRP | 2014-08-04 | 20 | 1.24 | -0.47 | 3.77 | 7.32 | 40 % | 2.0 | 87 d | 65 % / 35 % | 8 % | 1 | 22.6 % | 1.11 | 21 % | 9.7 % | -8.3 % | 304 d |
| ADA | 2018-10-01 | 8 | 0.31 | -1.00 | 3.56 | 5.36 | 25 % | 2.2 | 161 d | 75 % / 25 % | 0 % | 0 | 8.5 % | -0.04 | 55 % | 8.3 % | -14.0 % | 619 d |
| AVAX | 2021-09-22 | 5 | -0.58 | -0.81 | -0.80 | 0.07 | 20 % | 1.8 | 157 d | 100 % / 0 % | 20 % | 0 | -1.2 % | -0.76 | 100 % | 2.1 % | -6.1 % | 555 d |
| LINK | 2018-09-20 | 14 | 0.45 | -0.68 | 2.64 | 4.89 | 36 % | 1.9 | 104 d | 79 % / 21 % | 18 % | 0 | 11.1 % | 0.15 | 38 % | 9.9 % | -8.5 % | 481 d |
| DOT | 2021-08-20 | 6 | -0.72 | -0.67 | -1.18 | 0.00 | 0 % | 1.8 | 102 d | 100 % / 0 % | 0 % | 0 | -2.1 % | -0.67 | – | 0.8 % | -7.5 % | 757 d |
| BNB | 2018-07-25 | 10 | 1.53 | -0.33 | 4.55 | 7.11 | 40 % | 2.6 | 148 d | 60 % / 40 % | 0 % | 0 | 13.7 % | 1.17 | 36 % | 10.8 % | -7.5 % | 703 d |
| LTC | 2014-04-28 | 19 | 0.10 | -0.44 | 0.59 | 1.77 | 26 % | 2.3 | 91 d | 89 % / 11 % | 18 % | 1 | 3.4 % | -0.13 | 67 % | 3.6 % | -14.6 % | 505 d |

BTC ist Identifikationsmarkt und zählt nicht für die Kriterien. «SL im Gewinn» ist der Anteil der Stop-Exits, bei denen der Stop nach Add-ons über dem Durchschnittseinstieg lag. «Blöcke positiv» zählt Zeitblöcke mit mindestens fünf Trades und positiver Erwartung.

## 4. Zeitblöcke, Pool ohne BTC

| Ebene | P1 bis 2020 n / E[R_ges] / PF | P2 2021 bis 2023 | P3 ab 2024 |
|---|---|---|---|
| A|none|1 | 37 / 1.37 / 7.58 | 26 / 0.66 / 4.48 | 39 / 0.08 / 2.49 |
| B|K1|1 | 15 / 0.62 / 5.36 | 22 / -0.02 / 1.98 | 36 / -0.05 / 1.93 |
| B2|K1|1 | 5 / -0.75 / – | 17 / 0.53 / 6.46 | 29 / -0.17 / 1.39 |

## 5. Verteilung der R-Multiples und Konzentration, Pool ohne BTC

| Ebene | P5 | P25 | Median | P75 | P90 | P95 | Anteil R < −1 | Anteil R > 3 | Top-1-Anteil | Top-3 | Top-5 | Top-10 % | Summe ohne Top 1 | ohne Top 3 | ohne Top 5 | Summe gesamt | Trade-Bootstrap 5 % E[R_ges] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A|none|1 | -1.00 | -1.00 | -0.52 | 0.58 | 5.22 | 5.66 | 12 % | 24 % | 6 % | 16 % | 27 % | 56 % | 498.73 % | 423.54 % | 351.44 % | 537.36 % | 0.30 |
| B|K1|1 | -1.04 | -1.02 | -0.67 | -0.29 | 4.34 | 5.07 | 37 % | 15 % | 11 % | 31 % | 51 % | 77 % | 177.20 % | 106.10 % | 38.49 % | 215.01 % | -0.27 |
| B|K2|1 | -1.08 | -1.05 | -0.70 | -0.32 | 4.29 | 5.02 | 38 % | 15 % | 11 % | 31 % | 51 % | 78 % | 165.38 % | 95.16 % | 28.36 % | 202.65 % | -0.31 |
| B2|K1|1 | -1.04 | -1.01 | -0.67 | -0.27 | 0.67 | 5.51 | 35 % | 10 % | 41 % | 69 % | 95 % | 98 % | 55.11 % | -16.73 % | -82.83 % | 161.67 % | -0.45 |

Coins mit positiver Erwartung ohne ihren grössten Gewinner (B, K1): BTC, SOL, XRP. Zeitblöcke positiv je Coin: BTC 1, ETH 0, SOL 0, XRP 0, ADA 0, AVAX 0, LINK 0, DOT 0, BNB 0, LTC 0. Summen in Prozent des Sleeve-Startkapitals, gepoolt über die Coins. Das Entfernen der grössten Gewinner ist Bericht, kein Kriterium.

## 6. Pfad, Beta-Trennung und Statistik, Pool ohne BTC

| Ebene | CAGR | Sharpe | MaxDD | Recovery max / Mittel | Worst Year | Worst 12M | Ulcer | Exposure | EP CAGR / Sharpe / MaxDD | Alpha p.a. | t | Beta | Up / Down Capture | Kennzeichnung | Bootstrap 5 % p.a. | p Sharpe | Holm p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A|none|1 | 9.2 % | 1.31 | -9.5 % | 341 / 16 d | -2.6 % | -6.7 % | 0.029 | 2.9 % | 5.5 % / 1.34 / -3.6 % | 3.6 % | 2.56 | 0.03 | 0.04 / 0.01 | KEINE | 3.4 % | 0.000 | 0.000 |
| A_window|none|1 | 6.1 % | 0.76 | -5.1 % | 417 / 17 d | 0.6 % | -4.6 % | 0.022 | 2.8 % | 4.1 % / 0.65 / -3.4 % | 1.9 % | 1.45 | 0.03 | 0.04 / 0.01 | KEINE | 0.4 % | 0.035 | – |
| B|K1|1 | 6.4 % | 0.66 | -7.4 % | 430 / 19 d | -0.3 % | -7.0 % | 0.029 | 3.4 % | 4.0 % / 0.46 / -4.7 % | 2.4 % | 1.39 | 0.03 | 0.05 / 0.02 | KEINE | -0.0 % | 0.052 | 0.105 |
| B|K2|1 | 6.2 % | 0.63 | -7.6 % | 430 / 20 d | -0.4 % | -7.2 % | 0.030 | 3.4 % | 4.0 % / 0.46 / -4.7 % | 2.2 % | 1.29 | 0.03 | 0.05 / 0.02 | KEINE | -0.2 % | 0.061 | – |
| B_full|K1|1 | 7.1 % | 0.68 | -13.7 % | 417 / 19 d | -0.6 % | -11.7 % | 0.050 | 3.2 % | 5.8 % / 0.89 / -4.9 % | 2.9 % | 1.42 | 0.02 | 0.04 / 0.01 | KEINE | 1.3 % | 0.012 | – |
| B2|K1|1 | 5.4 % | 0.51 | -6.7 % | 543 / 19 d | 0.0 % | -6.6 % | 0.037 | 3.3 % | 4.0 % / 0.46 / -4.6 % | 1.4 % | 0.81 | 0.04 | 0.05 / 0.02 | KEINE | -0.8 % | 0.119 | 0.119 |
| B|K1|1b | 6.6 % | 0.63 | -7.6 % | 430 / 16 d | -0.4 % | -7.2 % | 0.035 | 4.0 % | 4.2 % / 0.46 / -5.6 % | 2.4 % | 1.27 | 0.04 | 0.06 / 0.02 | KEINE | -0.2 % | 0.058 | – |
| B|K1|2 | 20.3 % | 0.71 | -44.4 % | 192 / 14 d | -14.6 % | -42.6 % | 0.232 | 29.0 % | 38.3 % / 0.98 / -43.6 % | 10.6 % | 1.22 | 0.08 | 0.19 / 0.17 | KEINE | 4.0 % | 0.020 | – |

## 7. Edge-Retention und Mechanik-Reproduzierbarkeit CMC gegen Kraken

**A gegen B (gleiche Signale, Kraken-Ausführung, K1).** A-Trades im B-Fenster 84, B-Trades 89, davon gepaart 84, B-Trades ohne Gegenstück in A 5. Gleicher Exit-Grund 98.8 %. Phantom-Stops (Kraken-Tief unter Stop, CMC-Tief nicht) 1, umgekehrt 0, Ziel nur auf einer Seite 1. Exit-Tag exakt 82.1 %, ±1 Tag 90.5 %, mittlere Abweichung 1.5 Tage. Fill-Abweichung Einstieg Mittel 0.100 % (P95 1.01 %, Anteil über 1 Prozent 5.2 %), Stop -0.100 % (n 67), Ziel 0.000 % (n 16).

**A gegen B (K0).** A-Trades im B-Fenster 84, B-Trades 89, davon gepaart 84, B-Trades ohne Gegenstück in A 5. Gleicher Exit-Grund 98.8 %. Phantom-Stops (Kraken-Tief unter Stop, CMC-Tief nicht) 1, umgekehrt 0, Ziel nur auf einer Seite 1. Exit-Tag exakt 82.1 %, ±1 Tag 90.5 %, mittlere Abweichung 1.5 Tage. Fill-Abweichung Einstieg Mittel 0.050 % (P95 1.01 %, Anteil über 1 Prozent 5.2 %), Stop 0.000 % (n 67), Ziel 0.000 % (n 16).

**A gegen B Same-Day-Close (K1, Berichtswert).** A-Trades im B-Fenster 84, B-Trades 89, davon gepaart 84, B-Trades ohne Gegenstück in A 5. Gleicher Exit-Grund 98.8 %. Phantom-Stops (Kraken-Tief unter Stop, CMC-Tief nicht) 1, umgekehrt 0, Ziel nur auf einer Seite 1. Exit-Tag exakt 82.1 %, ±1 Tag 90.5 %, mittlere Abweichung 1.5 Tage. Fill-Abweichung Einstieg Mittel 0.101 % (P95 0.99 %, Anteil über 1 Prozent 4.7 %), Stop -0.100 % (n 67), Ziel 0.000 % (n 16).

**A gegen B2 (Signale auf Kraken erzeugt).** A-Trades im B2-Fenster 79, B2-Trades 63. Entry-Tag exakt 55.7 %, ±1 Tag 60.8 %. Exit-Tag exakt 30.4 %, ±1 39.2 %. Leg-Zahl gleich 46.8 %, Exit-Grund gleich 57.0 %, vollständig identisch 34.2 %. Stop-Niveau-Abweichung Mittel -10.483 %, P95 33.47 %. SMA200-Filter je Tag gleich 99.9 %. Wilder-ATR Kraken zu CMC Mittel 1.198 (Spanne 1.00 bis 4.99). Pivot-Niveau je Tag gleich (unter 0.5 Prozent) 72.6 %.

Retention K1: E[R_gesamt] B / A_window = 0.10 / 0.26 = 0.37, E[R_first] 1.47 / 1.94, Profit-Faktor 2.61 / 3.32, Trefferquote 20.5 % / 23.5 %, Trades 73 / 68.

## 8. Jitter-Nachbarn (Plateau-Prüfung, ohne Auswahlwirkung), Pool ohne BTC

| Variante | B K1 Trades | E[R_ges] | PF | Trefferquote | A Trades | E[R_ges] | PF |
|---|---|---|---|---|---|---|---|
| Basis (6.5 / 37.5 / Pivot 5) | 73 | 0.10 | 2.61 | 20.5 % | 102 | 0.70 | 4.51 |
| sl5.5 {'sl_mult': 5.5} | 77 | 0.16 | 3.08 | 22.1 % | 108 | 0.71 | 5.00 |
| sl7.5 {'sl_mult': 7.5} | 65 | 0.20 | 3.07 | 23.1 % | 91 | 0.72 | 4.57 |
| tp30 {'tp_mult': 30.0} | 74 | 0.13 | 2.32 | 24.3 % | 103 | 0.58 | 3.79 |
| tp45 {'tp_mult': 45.0} | 71 | 0.11 | 2.78 | 19.7 % | 99 | 0.78 | 4.96 |
| piv3 {'piv_left': 3} | 77 | 0.06 | 2.60 | 19.5 % | 107 | 0.64 | 4.53 |
| piv10 {'piv_left': 10} | 63 | 0.18 | 2.72 | 23.8 % | 91 | 0.77 | 4.62 |

## 9. Pyramiding und Open Risk je Add-on, Ebene B K1 Sicht 1, alle Coins

Anzahl Add-ons 114. Open Risk (Mark-to-Market bis Stop, in Prozent des Sleeve-Startkapitals) vor Add-on Mittel 6.42 %, nach Add-on 5.85 %. Ergebnis bei sofortigem Stop vor Add-on -2.03 %, nach Add-on -1.43 % (positiv heisst: Stop schliesst im Gewinn). Notional vor 16.6 %, nach 24.9 %. Anteil Add-ons, nach denen der gemeinsame Stop über dem Durchschnittseinstieg liegt 16 %, erstmals im Mittel beim 3.8. Add-on.

| Add-on Nr. | Anzahl | Open Risk vor | nach | Ergebnis bei Stop vor | nach | Notional nach | Stop über Ø Entry |
|---|---|---|---|---|---|---|---|
| 2 | 60 | 3.50 % | 3.94 % | -2.01 % | -2.50 % | 15.3 % | 5 % |
| 3 | 34 | 7.88 % | 6.78 % | -2.70 % | -1.44 % | 27.3 % | 12 % |
| 4 | 14 | 11.26 % | 9.05 % | -1.48 % | 0.79 % | 41.0 % | 43 % |
| 5 | 4 | 14.88 % | 10.35 % | -0.71 % | 3.65 % | 64.2 % | 75 % |
| 6 | 2 | 18.59 % | 15.66 % | 2.34 % | 5.52 % | 80.2 % | 100 % |

## 10. Umfang und Verifikation

- Eingabedateien mit SHA-256 in `mtp_val_results.json`, Feld `inputs` (20 Dateien), Kraken-Archiv fc81b54c… gegen Krakens Hash-Liste geprüft
- Starts je Coin (A / B / B_full / B2): BTC 2014-04-28 / 2014-12-26 / 2014-04-28 / 2014-12-26; ETH 2016-08-06 / 2018-01-13 / 2016-08-06 / 2018-01-13; SOL 2021-04-10 / 2021-06-17 / 2021-06-17 / 2022-06-17; XRP 2014-08-04 / 2018-01-13 / 2017-05-18 / 2018-05-19; ADA 2018-10-01 / 2018-10-01 / 2018-10-01 / 2019-09-28; AVAX 2021-09-22 / 2021-12-21 / 2021-12-21 / 2022-12-21; LINK 2018-09-20 / 2019-09-25 / 2019-09-25 / 2020-09-24; DOT 2021-08-20 / 2021-08-20 / 2021-08-20 / 2021-08-18; BNB 2018-07-25 / 2025-04-22 / 2025-04-22 / 2026-04-22; LTC 2014-04-28 / 2018-01-13 / 2014-04-28 / 2018-01-13
- Look-ahead-Test und BTC-Replikationskontrolle in `controls.json`, alle Trades je Ebene in `trades/`
- Kostenmodell: K0 Gebühr 0.16 % plus Reibung 0.00 % je Seite, Slippage Einstieg 0.00 %, Stop 0.00 %; K1 Gebühr 0.40 % plus Reibung 0.02 % je Seite, Slippage Einstieg 0.05 %, Stop 0.10 %; K2 Gebühr 0.80 % plus Reibung 0.06 % je Seite, Slippage Einstieg 0.15 %, Stop 0.30 %
## 11. Zerlegung der Edge-Retention (Ergänzung nach dem Lauf, keine Änderung des Kriteriums)

Die vorregistrierte Retention (E[R_gesamt] B geteilt durch A im B-Fenster) beträgt 0.37 und verfehlt die Schwelle von 60 Prozent. Die Zerlegung zeigt, woraus die Differenz besteht. 68 A-Trades im B-Fenster haben ein exaktes Gegenstück in B (gleicher Entry-Tag): E[R_gesamt] 0.262 in A gegen 0.160 in B, Retention auf den Paaren 0.61. Davon entfällt fast alles auf einen einzigen Phantom-Stop (LINK, Einstieg 07.11.2020, in A ein Ziel-Exit mit plus 4.0 R, in B ein Stop-Exit am 23.12.2020 mit minus 1.0 R, weil das Kraken-Tief den CMC-definierten Stop berührte, das CMC-Tief nicht). Ohne dieses Paar liegt die Retention der übrigen 67 Paare bei 0.86, die Differenz sind Kosten und Slippage. Die restlichen fünf B-Trades haben kein Gegenstück in A, weil A am B-Start je Coin bereits in einer Position war oder nach dem Phantom-Stop anders positioniert blieb (AVAX zweimal, LINK zweimal, BNB einmal). Alle fünf sind Verlierer, im Mittel minus 0.75 R, und senken den B-Durchschnitt von 0.160 auf 0.097. Sie sind Randeffekte des Vergleichsfensters und der Zustandsdivergenz, keine Ausführungseffekte. Das Kriterium 6 bleibt wie vorregistriert verfehlt, es ist aber nicht das bindende Kriterium: 2, 3, 4 und 5 sind in B unabhängig davon verfehlt.

## 12. Anmerkungen zur Lesart einzelner Tabellen

Sicht 2 (gemeinsames Portfolio): Die Trade-Prozentwerte (Ø Gewinner, Ø Verlierer, Summen) sind auf das Startkapital eines Sleeves bezogen und deshalb um den Faktor der Coinzahl überhöht, das First-Leg-Multiple ist durch die Exposure-Obergrenze verzerrt (ein durch die Kappung winziger erster Leg erzeugt riesige Multiples). Für Sicht 2 sind nur R_gesamt, die Pfadkennzahlen auf der Portfolio-Equity und die Exposure aussagekräftig. Sicht 1 Exposure von rund 3 Prozent ergibt sich aus 2 Prozent Nominal Initial Risk je Leg bei einem Stop von 6.5 ATR (rund 10 bis 15 Prozent Notional je Leg) und 33 bis 58 Prozent investierter Tage je Coin. Die Pfadkennzahlen (CAGR, MaxDD) sind entsprechend klein und nur relativ zueinander und zur exposure-gleichen Passivposition zu lesen.

B2 gegen A: Das Wilder-ATR auf Kraken-Daten ist im Mittel 20 Prozent höher als auf CMC (Spanne bis Faktor 5 an einzelnen Tagen), weil Kraken-Kerzen die Extreme einzelner Flash-Crashes enthalten, die der Index glättet. Stop und Ziel liegen auf Kraken-Signalen deshalb weiter, Pivot-Niveaus stimmen nur zu 73 Prozent überein, und nur 34 Prozent der Trades sind vollständig identisch. Die Mechanik ist auf Börsendaten nicht dieselbe wie auf Indexdaten.
