# REBOUND-MICRO v1.0 — Development-Bericht XRP

**Project Aurum II, `01_forschung/10_rebound_micro/rebound_micro_bericht_XRP_v1.md`. 18.09.2026. Einmaliger Lauf nach `rebound_micro_spec_v1.0.md` (SHA 001a3853…). Eingaben: Spot 1h 2e169dbdf38fa797…, Spot 4h 6fda0931ded268ac…, mlib 6b7e7ba888e17cac…, simulate fef60859063dd8bc…. Regression der Kandidatentabelle gegen die outcome-blinde Zählung v0.1: IDENTICAL. Ergebnisdateien versiegelt in ENTSCHEIDE.md. Development Evidence, Ebene C, kein Sleeve-Status. Primärer Kostenmassstab K1, K0 und K2 Sensitivität.**

## 1. Fallzahlen und Zulassung

Kontext-Events mit vollständigem 1h-Fenster 148, Kandidaten 156. Zulassung je Zelle (gehandelt / kein enger Stop / Ziel unter Einstieg / Lücke / Overlap): M1xQ0 64 / 28 / 15 / 12 / 0, M1xQ1 69 / 28 / 10 / 12 / 0, M2xQ0 4 / 8 / 1 / 1 / 0, M2xQ1 4 / 8 / 1 / 1 / 0, M3xQ0 2 / 17 / 4 / 0 / 0, M3xQ1 6 / 17 / 0 / 0 / 0. Baseline: Q0 126 gehandelt (22 Ziel unter Einstieg), Q1 131 (17). Kontrollpool 700 4h-Kerzen (K1 und K2 ohne K3), Kontroll-M1-Kandidaten 118, Kontroll-Trade-Zeilen 44.

## 2. Primary-Zellen M1×Q0 und M1×Q1 (alle Kostenstufen)

| Zelle | Kosten | n | Mittel r_net | Median | Trefferquote | Zielrate | Stoprate | Zeitstopp | avg_win | avg_loss | win/loss | p_BE_emp | PF | p_pos | cost_R Med. | Stop ATR4h Med. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M1xQ0 | K0 | 64 | -0.197 | -0.787 | 36 % | 41 % | 50 % | 9 % | 1.42 | -1.10 | 1.29 | 0.44 | 0.72 | 0.14 | 0.28 | 0.41 |
| M1xQ0 | K1 | 64 | -0.817 | -1.309 | 30 % | 41 % | 50 % | 9 % | 1.04 | -1.60 | 0.65 | 0.61 | 0.27 | 0.00 | 0.83 | 0.41 |
| M1xQ0 | K2 | 64 | -1.693 | -1.776 | 14 % | 41 % | 50 % | 9 % | 0.91 | -2.12 | 0.43 | 0.70 | 0.07 | 0.00 | 1.65 | 0.41 |
| M1xQ1 | K0 | 69 | -0.263 | -1.103 | 39 % | 36 % | 52 % | 12 % | 1.19 | -1.20 | 0.99 | 0.50 | 0.64 | 0.06 | 0.30 | 0.41 |
| M1xQ1 | K1 | 69 | -0.885 | -1.379 | 25 % | 36 % | 52 % | 12 % | 1.10 | -1.53 | 0.72 | 0.58 | 0.23 | 0.00 | 0.84 | 0.41 |
| M1xQ1 | K2 | 69 | -1.764 | -2.013 | 13 % | 36 % | 52 % | 12 % | 0.81 | -2.15 | 0.37 | 0.73 | 0.06 | 0.00 | 1.69 | 0.41 |

Ausstiegsgründe K1: M1xQ0: stop 32, target 26, time24 6; M1xQ1: stop 36, target 25, time24 8.

Blöcke K1 (n, Mittel): M1xQ0: P1 31 / -0.82, P2 33 / -0.81; M1xQ1: P1 33 / -1.02, P2 36 / -0.76. Konzentration: grösster Gewinn als Anteil der Gewinnsumme M1xQ0 12 %, M1xQ1 19 %.

## 3. Baseline T0 (gleiche Events, 4h-struktureller Stop)

| Zelle | Kosten | n | Mittel r_net | Trefferquote | Zielrate | Stoprate | avg_win | avg_loss | win/loss | p_BE_emp | cost_R Med. | Stop ATR4h Med. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BASExQ0 | K0 | 126 | -0.111 | 48 % | 42 % | 37 % | 0.72 | -0.89 | 0.81 | 0.55 | 0.13 | 0.86 |
| BASExQ0 | K1 | 126 | -0.392 | 40 % | 42 % | 37 % | 0.58 | -1.03 | 0.56 | 0.64 | 0.38 | 0.86 |
| BASExQ1 | K0 | 131 | -0.008 | 40 % | 31 % | 37 % | 1.24 | -0.83 | 1.50 | 0.40 | 0.13 | 0.88 |
| BASExQ1 | K1 | 131 | -0.301 | 32 % | 31 % | 37 % | 1.20 | -1.01 | 1.19 | 0.46 | 0.39 | 0.88 |

## 4. Gepaarter Primary-Vergleich Zelle minus Baseline (gleiches Event, gleiches Ziel)

| Zelle | Kosten | Paare | Mittel Diff. | Median Diff. | Anteil positiv | Bootstrap-p (einseitig) | Vorzeichentest p | Wilcoxon p | Mittel Zelle | Mittel Baseline (gepaart) |
|---|---|---|---|---|---|---|---|---|---|---|
| M1xQ0 | K0 | 59 | 0.022 | -0.120 | 34 % | 0.465 | 0.996 | 0.866 | -0.212 | -0.234 |
| M1xQ0 | K1 | 59 | -0.298 | -0.291 | 25 % | 0.978 | 1.000 | 0.997 | -0.821 | -0.524 |
| M1xQ0 | K2 | 59 | -0.703 | -0.621 | 20 % | 1.000 | 1.000 | 1.000 | -1.685 | -0.982 |
| M1xQ1 | K0 | 62 | 0.181 | -0.128 | 34 % | 0.088 | 0.996 | 0.633 | -0.246 | -0.427 |
| M1xQ1 | K1 | 62 | -0.138 | -0.269 | 31 % | 0.854 | 0.999 | 0.966 | -0.862 | -0.724 |
| M1xQ1 | K2 | 62 | -0.543 | -0.471 | 26 % | 1.000 | 1.000 | 1.000 | -1.735 | -1.192 |

Holm über die zwei Primary-Tests (K1): p roh M1xQ0 0.978, M1xQ1 0.854, Holm-adjustiert M1xQ0 1.000, M1xQ1 1.000. Signifikant bei α 0.05: keine.

Kreuztabelle der Ausstiegsart je Paar (K1, Zeile M1, Spalte Baseline, T Ziel, S Stop, Z Zeitstopp):

M1×Q0: M1 T und Baseline T: 16; M1 T und Baseline S: 2; M1 T und Baseline Z: 3; M1 S und Baseline T: 4; M1 S und Baseline S: 22; M1 S und Baseline Z: 6; M1 Z und Baseline S: 1; M1 Z und Baseline Z: 5. Einstiegsverzögerung M1 gegenüber Baseline Median 4 Stunden. Baseline bereits vor dem M1-Einstieg ausgestoppt: 5 von 59.

M1×Q1: M1 T und Baseline T: 15; M1 T und Baseline S: 3; M1 T und Baseline Z: 2; M1 S und Baseline S: 23; M1 S und Baseline Z: 11; M1 Z und Baseline S: 1; M1 Z und Baseline Z: 7. Einstiegsverzögerung M1 gegenüber Baseline Median 5 Stunden. Baseline bereits vor dem M1-Einstieg ausgestoppt: 7 von 62.

## 5. Frage C: Q1 gegen Q0 auf denselben M1-Trades (K1)

58 Events mit beiden Zellen gehandelt. Mittel r_net Q0 -0.870, Q1 -0.881, Differenz Q1 minus Q0 Mittel -0.011, Median 0.000, Anteil Q1 besser 26 %, Bootstrap p_pos 0.446. Zielrate Q0 40 %, Q1 38 %.

## 6. Diagnosen (vorregistriert, keine Statuswirkung)

M1xQ0: Anteil der Stop-outs, nach denen das Ziel innerhalb der 24 Kerzen dennoch erreicht wurde 19 %. MFE nach erreichtem Ziel bis Kerze 24 Median 1.14 R, neues 20-Tage-Hoch innerhalb 30 Tagen nach Ziel 35 %, 30-Tage-Hoch 35 %. Haltedauer Median 4 Kerzen. Teilmengen deskriptiv (n, Mittel K1): Flow-Flag 2 / -1.40, Harami 4 / -1.48, Hikkake 1 / -1.73. Kontrollgruppe (K1 und K2 ohne K3): 13 Kontroll-Trades, Mittel -0.699, Median 0.113, Events mit Kontrolle 8, Differenz Zelle minus Kontrollmittel Median -0.041, Anteil positiv 50 %. Kandidatenrate 0.87 je 1000 1h-Kerzen, erwartete Trades ETH 49, SOL 26 (nur Hochrechnung, keine ETH/SOL-Daten).

M1xQ1: Anteil der Stop-outs, nach denen das Ziel innerhalb der 24 Kerzen dennoch erreicht wurde 3 %. MFE nach erreichtem Ziel bis Kerze 24 Median 1.25 R, neues 20-Tage-Hoch innerhalb 30 Tagen nach Ziel 44 %, 30-Tage-Hoch 44 %. Haltedauer Median 5 Kerzen. Teilmengen deskriptiv (n, Mittel K1): Flow-Flag 2 / -1.82, Harami 3 / -1.95, Hikkake 1 / -1.73. Kontrollgruppe (K1 und K2 ohne K3): 11 Kontroll-Trades, Mittel -0.593, Median 0.113, Events mit Kontrolle 8, Differenz Zelle minus Kontrollmittel Median -0.585, Anteil positiv 50 %. Kandidatenrate 0.94 je 1000 1h-Kerzen, erwartete Trades ETH 53, SOL 28 (nur Hochrechnung, keine ETH/SOL-Daten).

## 7. M2 und M3 (descriptive / insufficient sample, Entscheidung 1)

M2xQ0: n 4, Mittel r_net K1 -0.591, Gründe {'stop': 2, 'target': 2}, gepaart 4 Paare, Median Diff. -0.213, Anteil positiv 50 %. Status: descriptive / insufficient sample.

M2xQ1: n 4, Mittel r_net K1 0.700, Gründe {'stop': 2, 'time24': 2}, gepaart 4 Paare, Median Diff. 0.028, Anteil positiv 50 %. Status: descriptive / insufficient sample.

M3xQ0: n 2, Mittel r_net K1 -0.028, Gründe {'target': 2}, gepaart 2 Paare, Median Diff. 0.669, Anteil positiv 100 %. Status: descriptive / insufficient sample.

M3xQ1: n 6, Mittel r_net K1 -0.610, Gründe {'target': 3, 'stop': 2, 'time24': 1}, gepaart 6 Paare, Median Diff. -0.014, Anteil positiv 50 %. Status: descriptive / insufficient sample.

## 8. Promotion-Prüfung und Status (Governance v1.1, Regeln v0.1)

M1xQ0: Bedingungen 1 Geometrie False, 2 p_BE False, 3 nicht negativ False, 4 Fallzahl False, 5 Konzentration True, 6 Blöcke False, 7 Baseline False. Promotion: False. Regel v2: a Baseline-Paare False, b Geometrie False, c Konzentration True, d Blöcke True (Zählung 2), Fast Fail True. Status: **normal (>=30): fast fail**.

M1xQ1: Bedingungen 1 Geometrie False, 2 p_BE True, 3 nicht negativ False, 4 Fallzahl False, 5 Konzentration True, 6 Blöcke False, 7 Baseline False. Promotion: False. Regel v2: a Baseline-Paare False, b Geometrie False, c Konzentration True, d Blöcke True (Zählung 2), Fast Fail True. Status: **normal (>=30): fast fail**.

Hinweis zur Regel v2: Die Kriterien c und d prüfen nur Stabilität von Konzentration und Blöcken und sind auch bei negativem Gesamtmittel erfüllbar. Ein Status «mechanistisch vielversprechend» setzt nach Governance v1.1 einen positiven relativen Effekt voraus (Kriterium a). Fast Fail hat in der eingefrorenen Auswertung Vorrang und ist hier für beide Primary-Zellen erfüllt.
