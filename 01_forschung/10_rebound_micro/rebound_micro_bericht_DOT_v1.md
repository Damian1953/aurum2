# REBOUND-MICRO v1.0 — Development-Bericht DOT

**Project Aurum II, `01_forschung/10_rebound_micro/rebound_micro_bericht_DOT_v1.md`. 18.09.2026. Einmaliger Lauf nach `rebound_micro_spec_v1.0.md` (SHA 001a3853…). Eingaben: Spot 1h 3ff35b27d3f0a18c…, Spot 4h 426b5ae7e4d4e57b…, mlib 6b7e7ba888e17cac…, simulate fef60859063dd8bc…. Regression der Kandidatentabelle gegen die outcome-blinde Zählung v0.1: IDENTICAL. Ergebnisdateien versiegelt in ENTSCHEIDE.md. Development Evidence, Ebene C, kein Sleeve-Status. Primärer Kostenmassstab K1, K0 und K2 Sensitivität.**

## 1. Fallzahlen und Zulassung

Kontext-Events mit vollständigem 1h-Fenster 89, Kandidaten 100. Zulassung je Zelle (gehandelt / kein enger Stop / Ziel unter Einstieg / Lücke / Overlap): M1xQ0 37 / 17 / 9 / 4 / 0, M1xQ1 42 / 17 / 4 / 4 / 0, M2xQ0 3 / 6 / 1 / 1 / 0, M2xQ1 2 / 6 / 2 / 1 / 0, M3xQ0 4 / 17 / 1 / 0 / 0, M3xQ1 3 / 17 / 2 / 0 / 0. Baseline: Q0 68 gehandelt (21 Ziel unter Einstieg), Q1 80 (9). Kontrollpool 395 4h-Kerzen (K1 und K2 ohne K3), Kontroll-M1-Kandidaten 66, Kontroll-Trade-Zeilen 22.

## 2. Primary-Zellen M1×Q0 und M1×Q1 (alle Kostenstufen)

| Zelle | Kosten | n | Mittel r_net | Median | Trefferquote | Zielrate | Stoprate | Zeitstopp | avg_win | avg_loss | win/loss | p_BE_emp | PF | p_pos | cost_R Med. | Stop ATR4h Med. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M1xQ0 | K0 | 37 | -0.161 | -0.034 | 46 % | 38 % | 49 % | 14 % | 1.08 | -1.21 | 0.89 | 0.53 | 0.76 | 0.23 | 0.21 | 0.54 |
| M1xQ0 | K1 | 37 | -0.632 | -0.699 | 38 % | 38 % | 49 % | 14 % | 1.00 | -1.63 | 0.62 | 0.62 | 0.37 | 0.01 | 0.57 | 0.54 |
| M1xQ0 | K2 | 37 | -1.316 | -1.497 | 22 % | 38 % | 49 % | 14 % | 1.13 | -1.99 | 0.57 | 0.64 | 0.16 | 0.00 | 1.14 | 0.54 |
| M1xQ1 | K0 | 42 | -0.390 | -1.138 | 29 % | 26 % | 64 % | 10 % | 1.68 | -1.22 | 1.38 | 0.42 | 0.55 | 0.08 | 0.25 | 0.50 |
| M1xQ1 | K1 | 42 | -0.925 | -1.396 | 24 % | 26 % | 64 % | 10 % | 1.58 | -1.71 | 0.93 | 0.52 | 0.29 | 0.00 | 0.71 | 0.50 |
| M1xQ1 | K2 | 42 | -1.685 | -1.852 | 21 % | 26 % | 64 % | 10 % | 1.14 | -2.46 | 0.47 | 0.68 | 0.13 | 0.00 | 1.40 | 0.50 |

Ausstiegsgründe K1: M1xQ0: stop 18, target 14, time24 5; M1xQ1: stop 27, target 11, time24 4.

Blöcke K1 (n, Mittel): M1xQ0: P2a 17 / -0.25, P2b 18 / -1.02; M1xQ1: P2a 18 / -0.83, P2b 22 / -1.33. Konzentration: grösster Gewinn als Anteil der Gewinnsumme M1xQ0 24 %, M1xQ1 46 %.

## 3. Baseline T0 (gleiche Events, 4h-struktureller Stop)

| Zelle | Kosten | n | Mittel r_net | Trefferquote | Zielrate | Stoprate | avg_win | avg_loss | win/loss | p_BE_emp | cost_R Med. | Stop ATR4h Med. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BASExQ0 | K0 | 68 | 0.002 | 54 % | 41 % | 38 % | 0.86 | -1.02 | 0.84 | 0.54 | 0.12 | 0.88 |
| BASExQ0 | K1 | 68 | -0.261 | 40 % | 41 % | 38 % | 0.88 | -1.01 | 0.87 | 0.54 | 0.34 | 0.88 |
| BASExQ1 | K0 | 80 | -0.105 | 52 % | 41 % | 41 % | 0.74 | -1.04 | 0.71 | 0.58 | 0.12 | 0.88 |
| BASExQ1 | K1 | 80 | -0.375 | 36 % | 41 % | 41 % | 0.77 | -1.03 | 0.75 | 0.57 | 0.37 | 0.88 |

## 4. Gepaarter Primary-Vergleich Zelle minus Baseline (gleiches Event, gleiches Ziel)

| Zelle | Kosten | Paare | Mittel Diff. | Median Diff. | Anteil positiv | Bootstrap-p (einseitig) | Vorzeichentest p | Wilcoxon p | Mittel Zelle | Mittel Baseline (gepaart) |
|---|---|---|---|---|---|---|---|---|---|---|
| M1xQ0 | K0 | 35 | -0.096 | -0.054 | 37 % | 0.672 | 0.955 | 0.789 | -0.169 | -0.073 |
| M1xQ0 | K1 | 35 | -0.297 | -0.221 | 31 % | 0.897 | 0.992 | 0.962 | -0.636 | -0.339 |
| M1xQ0 | K2 | 35 | -0.552 | -0.239 | 26 % | 0.985 | 0.999 | 0.995 | -1.312 | -0.760 |
| M1xQ1 | K0 | 42 | -0.177 | -0.133 | 26 % | 0.777 | 1.000 | 0.987 | -0.390 | -0.213 |
| M1xQ1 | K1 | 42 | -0.427 | -0.366 | 24 % | 0.966 | 1.000 | 0.996 | -0.925 | -0.498 |
| M1xQ1 | K2 | 42 | -0.737 | -0.685 | 19 % | 0.998 | 1.000 | 1.000 | -1.685 | -0.947 |

Holm über die zwei Primary-Tests (K1): p roh M1xQ0 0.897, M1xQ1 0.966, Holm-adjustiert M1xQ0 1.000, M1xQ1 1.000. Signifikant bei α 0.05: keine.

Kreuztabelle der Ausstiegsart je Paar (K1, Zeile M1, Spalte Baseline, T Ziel, S Stop, Z Zeitstopp):

M1×Q0: M1 T und Baseline T: 8; M1 T und Baseline S: 3; M1 T und Baseline Z: 1; M1 S und Baseline T: 5; M1 S und Baseline S: 10; M1 S und Baseline Z: 3; M1 Z und Baseline S: 1; M1 Z und Baseline Z: 4. Einstiegsverzögerung M1 gegenüber Baseline Median 3 Stunden. Baseline bereits vor dem M1-Einstieg ausgestoppt: 4 von 35.

M1×Q1: M1 T und Baseline T: 9; M1 T und Baseline S: 1; M1 T und Baseline Z: 1; M1 S und Baseline T: 6; M1 S und Baseline S: 17; M1 S und Baseline Z: 4; M1 Z und Baseline S: 2; M1 Z und Baseline Z: 2. Einstiegsverzögerung M1 gegenüber Baseline Median 3 Stunden. Baseline bereits vor dem M1-Einstieg ausgestoppt: 4 von 42.

## 5. Frage C: Q1 gegen Q0 auf denselben M1-Trades (K1)

35 Events mit beiden Zellen gehandelt. Mittel r_net Q0 -0.708, Q1 -0.939, Differenz Q1 minus Q0 Mittel -0.231, Median 0.000, Anteil Q1 besser 20 %, Bootstrap p_pos 0.066. Zielrate Q0 37 %, Q1 29 %.

## 6. Diagnosen (vorregistriert, keine Statuswirkung)

M1xQ0: Anteil der Stop-outs, nach denen das Ziel innerhalb der 24 Kerzen dennoch erreicht wurde 33 %. MFE nach erreichtem Ziel bis Kerze 24 Median 1.02 R, neues 20-Tage-Hoch innerhalb 30 Tagen nach Ziel 50 %, 30-Tage-Hoch 29 %. Haltedauer Median 4 Kerzen. Teilmengen deskriptiv (n, Mittel K1): Flow-Flag 2 / -0.47, Harami 0 / n/a, Hikkake 0 / n/a. Kontrollgruppe (K1 und K2 ohne K3): 4 Kontroll-Trades, Mittel -1.453, Median -1.403, Events mit Kontrolle 3, Differenz Zelle minus Kontrollmittel Median 0.015, Anteil positiv 67 %. Kandidatenrate 0.69 je 1000 1h-Kerzen, erwartete Trades ETH 39, SOL 21 (nur Hochrechnung, keine ETH/SOL-Daten).

M1xQ1: Anteil der Stop-outs, nach denen das Ziel innerhalb der 24 Kerzen dennoch erreicht wurde 11 %. MFE nach erreichtem Ziel bis Kerze 24 Median 1.89 R, neues 20-Tage-Hoch innerhalb 30 Tagen nach Ziel 55 %, 30-Tage-Hoch 36 %. Haltedauer Median 4 Kerzen. Teilmengen deskriptiv (n, Mittel K1): Flow-Flag 2 / -0.42, Harami 1 / -1.75, Hikkake 0 / n/a. Kontrollgruppe (K1 und K2 ohne K3): 4 Kontroll-Trades, Mittel -1.453, Median -1.403, Events mit Kontrolle 3, Differenz Zelle minus Kontrollmittel Median 0.015, Anteil positiv 67 %. Kandidatenrate 0.79 je 1000 1h-Kerzen, erwartete Trades ETH 44, SOL 23 (nur Hochrechnung, keine ETH/SOL-Daten).

## 7. M2 und M3 (descriptive / insufficient sample, Entscheidung 1)

M2xQ0: n 3, Mittel r_net K1 0.024, Gründe {'time24': 1, 'stop': 1, 'target': 1}, gepaart 3 Paare, Median Diff. -0.373, Anteil positiv 33 %. Status: descriptive / insufficient sample.

M2xQ1: n 2, Mittel r_net K1 -0.529, Gründe {'stop': 1, 'time24': 1}, gepaart 2 Paare, Median Diff. -0.454, Anteil positiv 50 %. Status: descriptive / insufficient sample.

M3xQ0: n 4, Mittel r_net K1 -0.987, Gründe {'stop': 2, 'time24': 1, 'target': 1}, gepaart 4 Paare, Median Diff. -0.355, Anteil positiv 25 %. Status: descriptive / insufficient sample.

M3xQ1: n 3, Mittel r_net K1 -0.395, Gründe {'stop': 1, 'target': 1, 'time24': 1}, gepaart 3 Paare, Median Diff. -0.374, Anteil positiv 33 %. Status: descriptive / insufficient sample.

## 8. Promotion-Prüfung und Status (Governance v1.1, Regeln v0.1)

M1xQ0: Bedingungen 1 Geometrie False, 2 p_BE False, 3 nicht negativ False, 4 Fallzahl False, 5 Konzentration True, 6 Blöcke False, 7 Baseline False. Promotion: False. Regel v2: a Baseline-Paare False, b Geometrie False, c Konzentration True, d Blöcke True (Zählung 2), Fast Fail True. Status: **normal (>=30): fast fail**.

M1xQ1: Bedingungen 1 Geometrie True, 2 p_BE True, 3 nicht negativ False, 4 Fallzahl False, 5 Konzentration False, 6 Blöcke False, 7 Baseline False. Promotion: False. Regel v2: a Baseline-Paare False, b Geometrie True, c Konzentration False, d Blöcke True (Zählung 2), Fast Fail True. Status: **normal (>=30): fast fail**.

Hinweis zur Regel v2: Die Kriterien c und d prüfen nur Stabilität von Konzentration und Blöcken und sind auch bei negativem Gesamtmittel erfüllbar. Ein Status «mechanistisch vielversprechend» setzt nach Governance v1.1 einen positiven relativen Effekt voraus (Kriterium a). Fast Fail hat in der eingefrorenen Auswertung Vorrang und ist hier für beide Primary-Zellen erfüllt.
