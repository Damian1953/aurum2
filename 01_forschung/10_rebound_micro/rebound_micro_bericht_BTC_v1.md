# REBOUND-MICRO v1.0 — Development-Bericht BTC

**Project Aurum II, `01_forschung/10_rebound_micro/rebound_micro_bericht_BTC_v1.md`. 18.09.2026. Einmaliger Lauf nach `rebound_micro_spec_v1.0.md` (SHA 001a3853…). Eingaben: Spot 1h 269b5fe188df0c5d…, Spot 4h 2d394fd1cbc344d5…, mlib 6b7e7ba888e17cac…, simulate fef60859063dd8bc…. Regression der Kandidatentabelle gegen die outcome-blinde Zählung v0.1: IDENTICAL. Ergebnisdateien versiegelt in ENTSCHEIDE.md. Development Evidence, Ebene C, kein Sleeve-Status. Primärer Kostenmassstab K1, K0 und K2 Sensitivität.**

## 1. Fallzahlen und Zulassung

Kontext-Events mit vollständigem 1h-Fenster 158, Kandidaten 169. Zulassung je Zelle (gehandelt / kein enger Stop / Ziel unter Einstieg / Lücke / Overlap): M1xQ0 84 / 32 / 14 / 10 / 0, M1xQ1 80 / 32 / 18 / 10 / 0, M2xQ0 3 / 12 / 0 / 1 / 0, M2xQ1 3 / 12 / 0 / 1 / 0, M3xQ0 0 / 11 / 1 / 1 / 0, M3xQ1 1 / 11 / 0 / 1 / 0. Baseline: Q0 134 gehandelt (24 Ziel unter Einstieg), Q1 132 (26). Kontrollpool 702 4h-Kerzen (K1 und K2 ohne K3), Kontroll-M1-Kandidaten 128, Kontroll-Trade-Zeilen 64.

## 2. Primary-Zellen M1×Q0 und M1×Q1 (alle Kostenstufen)

| Zelle | Kosten | n | Mittel r_net | Median | Trefferquote | Zielrate | Stoprate | Zeitstopp | avg_win | avg_loss | win/loss | p_BE_emp | PF | p_pos | cost_R Med. | Stop ATR4h Med. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M1xQ0 | K0 | 84 | -0.269 | -0.276 | 42 % | 49 % | 46 % | 5 % | 1.01 | -1.18 | 0.86 | 0.54 | 0.61 | 0.03 | 0.28 | 0.55 |
| M1xQ0 | K1 | 84 | -0.954 | -1.056 | 23 % | 49 % | 46 % | 5 % | 1.01 | -1.53 | 0.66 | 0.60 | 0.19 | 0.00 | 0.82 | 0.55 |
| M1xQ0 | K2 | 84 | -1.885 | -1.835 | 13 % | 49 % | 46 % | 5 % | 0.67 | -2.27 | 0.30 | 0.77 | 0.04 | 0.00 | 1.61 | 0.55 |
| M1xQ1 | K0 | 80 | -0.228 | -0.743 | 35 % | 34 % | 50 % | 16 % | 1.53 | -1.18 | 1.30 | 0.43 | 0.70 | 0.12 | 0.32 | 0.50 |
| M1xQ1 | K1 | 80 | -0.982 | -1.295 | 22 % | 34 % | 50 % | 16 % | 1.42 | -1.68 | 0.84 | 0.54 | 0.25 | 0.00 | 0.88 | 0.50 |
| M1xQ1 | K2 | 80 | -1.993 | -1.943 | 12 % | 34 % | 50 % | 16 % | 1.29 | -2.46 | 0.52 | 0.66 | 0.07 | 0.00 | 1.72 | 0.50 |

Ausstiegsgründe K1: M1xQ0: target 41, stop 38, time24 4, stop_ambiguous 1; M1xQ1: stop 40, target 27, time24 13.

Blöcke K1 (n, Mittel): M1xQ0: P1 37 / -0.92, P2 47 / -0.99; M1xQ1: P1 34 / -0.97, P2 46 / -0.99. Konzentration: grösster Gewinn als Anteil der Gewinnsumme M1xQ0 14 %, M1xQ1 29 %.

## 3. Baseline T0 (gleiche Events, 4h-struktureller Stop)

| Zelle | Kosten | n | Mittel r_net | Trefferquote | Zielrate | Stoprate | avg_win | avg_loss | win/loss | p_BE_emp | cost_R Med. | Stop ATR4h Med. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BASExQ0 | K0 | 134 | -0.197 | 46 % | 45 % | 39 % | 0.68 | -0.93 | 0.73 | 0.58 | 0.19 | 0.89 |
| BASExQ0 | K1 | 134 | -0.591 | 33 % | 45 % | 39 % | 0.50 | -1.12 | 0.45 | 0.69 | 0.56 | 0.89 |
| BASExQ1 | K0 | 132 | -0.202 | 42 % | 36 % | 40 % | 0.79 | -0.93 | 0.85 | 0.54 | 0.20 | 0.84 |
| BASExQ1 | K1 | 132 | -0.619 | 27 % | 36 % | 40 % | 0.75 | -1.11 | 0.67 | 0.60 | 0.58 | 0.84 |

## 4. Gepaarter Primary-Vergleich Zelle minus Baseline (gleiches Event, gleiches Ziel)

| Zelle | Kosten | Paare | Mittel Diff. | Median Diff. | Anteil positiv | Bootstrap-p (einseitig) | Vorzeichentest p | Wilcoxon p | Mittel Zelle | Mittel Baseline (gepaart) |
|---|---|---|---|---|---|---|---|---|---|---|
| M1xQ0 | K0 | 81 | -0.103 | -0.141 | 31 % | 0.816 | 1.000 | 0.981 | -0.263 | -0.159 |
| M1xQ0 | K1 | 81 | -0.398 | -0.375 | 26 % | 1.000 | 1.000 | 1.000 | -0.955 | -0.557 |
| M1xQ0 | K2 | 81 | -0.734 | -0.609 | 21 % | 1.000 | 1.000 | 1.000 | -1.892 | -1.158 |
| M1xQ1 | K0 | 75 | 0.079 | -0.126 | 32 % | 0.292 | 0.999 | 0.842 | -0.223 | -0.302 |
| M1xQ1 | K1 | 75 | -0.241 | -0.272 | 28 % | 0.948 | 1.000 | 0.992 | -0.987 | -0.746 |
| M1xQ1 | K2 | 75 | -0.599 | -0.426 | 27 % | 1.000 | 1.000 | 1.000 | -2.007 | -1.408 |

Holm über die zwei Primary-Tests (K1): p roh M1xQ0 1.000, M1xQ1 0.948, Holm-adjustiert M1xQ0 1.000, M1xQ1 1.000. Signifikant bei α 0.05: keine.

Kreuztabelle der Ausstiegsart je Paar (K1, Zeile M1, Spalte Baseline, T Ziel, S Stop, Z Zeitstopp):

M1×Q0: M1 T und Baseline T: 32; M1 T und Baseline S: 4; M1 T und Baseline Z: 3; M1 S und Baseline T: 6; M1 S und Baseline S: 27; M1 S und Baseline Z: 5; M1 Z und Baseline Z: 4. Einstiegsverzögerung M1 gegenüber Baseline Median 3 Stunden. Baseline bereits vor dem M1-Einstieg ausgestoppt: 7 von 81.

M1×Q1: M1 T und Baseline T: 19; M1 T und Baseline S: 3; M1 T und Baseline Z: 1; M1 S und Baseline T: 1; M1 S und Baseline S: 27; M1 S und Baseline Z: 11; M1 Z und Baseline S: 4; M1 Z und Baseline Z: 9. Einstiegsverzögerung M1 gegenüber Baseline Median 3 Stunden. Baseline bereits vor dem M1-Einstieg ausgestoppt: 13 von 75.

## 5. Frage C: Q1 gegen Q0 auf denselben M1-Trades (K1)

70 Events mit beiden Zellen gehandelt. Mittel r_net Q0 -0.975, Q1 -1.093, Differenz Q1 minus Q0 Mittel -0.118, Median 0.000, Anteil Q1 besser 21 %, Bootstrap p_pos 0.196. Zielrate Q0 49 %, Q1 33 %.

## 6. Diagnosen (vorregistriert, keine Statuswirkung)

M1xQ0: Anteil der Stop-outs, nach denen das Ziel innerhalb der 24 Kerzen dennoch erreicht wurde 26 %. MFE nach erreichtem Ziel bis Kerze 24 Median 0.94 R, neues 20-Tage-Hoch innerhalb 30 Tagen nach Ziel 39 %, 30-Tage-Hoch 32 %. Haltedauer Median 4 Kerzen. Teilmengen deskriptiv (n, Mittel K1): Flow-Flag 2 / -0.52, Harami 11 / -1.68, Hikkake 2 / -1.06. Kontrollgruppe (K1 und K2 ohne K3): 17 Kontroll-Trades, Mittel -0.822, Median -1.521, Events mit Kontrolle 17, Differenz Zelle minus Kontrollmittel Median -0.457, Anteil positiv 35 %. Kandidatenrate 1.06 je 1000 1h-Kerzen, erwartete Trades ETH 59, SOL 31 (nur Hochrechnung, keine ETH/SOL-Daten).

M1xQ1: Anteil der Stop-outs, nach denen das Ziel innerhalb der 24 Kerzen dennoch erreicht wurde 10 %. MFE nach erreichtem Ziel bis Kerze 24 Median 1.15 R, neues 20-Tage-Hoch innerhalb 30 Tagen nach Ziel 44 %, 30-Tage-Hoch 37 %. Haltedauer Median 6 Kerzen. Teilmengen deskriptiv (n, Mittel K1): Flow-Flag 1 / -1.05, Harami 11 / -1.61, Hikkake 2 / -1.85. Kontrollgruppe (K1 und K2 ohne K3): 17 Kontroll-Trades, Mittel -0.938, Median -1.219, Events mit Kontrolle 13, Differenz Zelle minus Kontrollmittel Median 0.682, Anteil positiv 54 %. Kandidatenrate 1.01 je 1000 1h-Kerzen, erwartete Trades ETH 56, SOL 30 (nur Hochrechnung, keine ETH/SOL-Daten).

## 7. M2 und M3 (descriptive / insufficient sample, Entscheidung 1)

M2xQ0: n 3, Mittel r_net K1 -0.089, Gründe {'target': 2, 'stop': 1}, gepaart 3 Paare, Median Diff. 1.143, Anteil positiv 67 %. Status: descriptive / insufficient sample.

M2xQ1: n 3, Mittel r_net K1 0.799, Gründe {'time24': 1, 'stop': 1, 'target': 1}, gepaart 3 Paare, Median Diff. 1.193, Anteil positiv 67 %. Status: descriptive / insufficient sample.

M3xQ0: keine Trades. Status: descriptive / insufficient sample.

M3xQ1: n 1, Mittel r_net K1 -1.148, Gründe {'stop': 1}, gepaart 1 Paare, Median Diff. 0.030, Anteil positiv 100 %. Status: descriptive / insufficient sample.

## 8. Promotion-Prüfung und Status (Governance v1.1, Regeln v0.1)

M1xQ0: Bedingungen 1 Geometrie False, 2 p_BE False, 3 nicht negativ False, 4 Fallzahl True, 5 Konzentration True, 6 Blöcke False, 7 Baseline False. Promotion: False. Regel v2: a Baseline-Paare False, b Geometrie False, c Konzentration True, d Blöcke True (Zählung 2), Fast Fail True. Status: **normal (>=30): fast fail**.

M1xQ1: Bedingungen 1 Geometrie True, 2 p_BE True, 3 nicht negativ False, 4 Fallzahl False, 5 Konzentration True, 6 Blöcke False, 7 Baseline False. Promotion: False. Regel v2: a Baseline-Paare False, b Geometrie True, c Konzentration True, d Blöcke True (Zählung 3), Fast Fail True. Status: **normal (>=30): fast fail**.

Hinweis zur Regel v2: Die Kriterien c und d prüfen nur Stabilität von Konzentration und Blöcken und sind auch bei negativem Gesamtmittel erfüllbar. Ein Status «mechanistisch vielversprechend» setzt nach Governance v1.1 einen positiven relativen Effekt voraus (Kriterium a). Fast Fail hat in der eingefrorenen Auswertung Vorrang und ist hier für beide Primary-Zellen erfüllt.
