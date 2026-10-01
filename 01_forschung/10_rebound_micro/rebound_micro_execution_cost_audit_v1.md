# REBOUND-MICRO — Execution-Cost-Audit K1, Version 1

**Project Aurum II, `01_forschung/10_rebound_micro/rebound_micro_execution_cost_audit_v1.md`. 18.09.2026. Rein arithmetischer, outcome-blinder Audit des K1-Kostenmodells vor dem Freeze von REBOUND-MICRO v1.0. Keine Parameteränderung, keine Outcomes. Skript `audit/cost_audit.py`, Ergebnisse `audit/cost_audit_v1.json` und `audit/cost_audit_m1_only.json`. Grundlage: Kandidatentabellen der outcome-blinden Zählung (`count/count_{BTC,XRP,DOT}.csv`), Auswahl M1, enger Invalidationspunkt, vollständiges 1h-Fenster (BTC 98, XRP 79, DOT 46).**

## 1. Ergebnis

**PASS.** Kein Implementierungs- oder Einheitenfehler. Die ausgewiesenen K1-Kosten je Trade in R sind die arithmetische Folge des bereits eingefrorenen konservativen K1-Modells (identisch mit `ylib.COST` aus BTC Stufe A und `rlib`, seit Stufe A unverändert) in Verbindung mit einer Stopdistanz von rund 1.1 bis 1.3 Prozent des Kurses. Die in der Zählung gespeicherte Spalte `cost_R` wurde unabhängig vom Bibliothekscode nachgerechnet (Formel unten): maximale Abweichung 2.6e-14, also identisch. Zusätzlich geprüft: Einstieg über Stop in allen Fällen, R = Einstieg − Stop exakt, `entry_to_stop_atr4` = R / ATR14(4h) exakt.

Ein Punkt wird als Erratum zum Vorbericht festgehalten (Abschnitt 5): Die Kostenzahlen in Abschnitt 8 des Vorberichts waren über M1, M2 und M3 zusammen berechnet, obwohl sie als «M1 eng» beschriftet waren. Für M1 allein lautet der DOT-Median 0.78 R statt 0.68 R. BTC und XRP ändern sich in der zweiten Nachkommastelle nicht. Die Schlussfolgerung des Vorberichts bleibt unverändert, der Befund wird für DOT eher stärker.

## 2. Das K1-Modell (eingefroren seit BTC Stufe A)

K1: Gebühr 0.40 Prozent je Seite (Kraken Spot Tier 1 Taker), Reibung 0.02 Prozent je Seite, Slippage 0.05 Prozent am Einstieg, 0.10 Prozent am Stop, Ziel als Limit ohne Slippage. Kein separater Spread-Term: Spread und Queue-Effekte sind in Reibung und Slippage zusammengefasst. K0: Gebühr 0.16 Prozent je Seite, sonst null. K2: Gebühr 0.80, Reibung 0.06, Slippage 0.15 Einstieg, 0.30 Stop.

## 3. Komponenten in Basispunkten und in R (K1)

Stopdistanz M1 eng, in Prozent des Einstiegspreises, P25 / Median / P75: BTC 0.67 / 1.10 / 1.49, XRP 0.80 / 1.13 / 1.67, DOT 0.89 / 1.27 / 2.79. Zum Vergleich die 4h-Baseline desselben Events (T0 an der ersten 1h-Eröffnung nach der Kontextkerze, Stop Kontexttief minus 0.5 ATR14(4h)): BTC 1.15 / 1.70 / 2.80, XRP 1.56 / 2.42 / 3.67, DOT 1.61 / 2.46 / 4.00.

| Komponente | bp | R bei BTC (P25 / Med / P75) | R bei XRP | R bei DOT |
|---|---|---|---|---|
| 1. Stopdistanz in Prozent | | 0.67 / 1.10 / 1.49 | 0.80 / 1.13 / 1.67 | 0.89 / 1.27 / 2.79 |
| 2. Entry Fee | 40 | 0.60 / 0.36 / 0.27 | 0.50 / 0.35 / 0.24 | 0.45 / 0.32 / 0.14 |
| 3. Exit Fee am Ziel | 40 | 0.60 / 0.36 / 0.27 | 0.50 / 0.35 / 0.24 | 0.45 / 0.32 / 0.14 |
| 4. Exit Fee am Stop | 40 | 0.60 / 0.36 / 0.27 | 0.50 / 0.35 / 0.24 | 0.45 / 0.32 / 0.14 |
| 5. Entry-Slippage | 5 | 0.07 / 0.05 / 0.03 | 0.06 / 0.04 / 0.03 | 0.06 / 0.04 / 0.02 |
| 6. Ziel-Slippage (Limit) | 0 | 0 | 0 | 0 |
| 7. Stop-Slippage | 10 | 0.15 / 0.09 / 0.07 | 0.12 / 0.09 / 0.06 | 0.11 / 0.08 / 0.04 |
| 8. Reibung (Spread-Komponente), je Seite | 2 | 0.03 / 0.02 / 0.01 | 0.03 / 0.02 / 0.01 | 0.02 / 0.02 / 0.01 |
| 9a. Rundlauf K1, Zielpfad (40+2+5 + 40+2) | 89 | 1.34 / 0.81 / 0.60 | 1.11 / 0.79 / 0.53 | 1.00 / 0.70 / 0.32 |
| 9b. Rundlauf K1, Stoppfad (40+2+5 + 40+2+10) | 99 | 1.49 / 0.90 / 0.67 | 1.23 / 0.88 / 0.60 | 1.12 / 0.78 / 0.36 |

Die Spalte «R» gibt die Kosten der jeweiligen Komponente in Einheiten des initialen Risikos R an, berechnet mit der Stopdistanz des jeweiligen Quantils. Die Kostenzahl `cost_R` der Zählung ist der Stoppfad (9b), berechnet je Kandidat und dann als Median über die Kandidaten genommen. Median der Verhältnisse und Verhältnis der Mediane stimmen bis auf 0.003 überein (DOT 0.784 gegen 0.781).

## 4. Exakte Formel

Kosten in R = Kosten in Basispunkten / Stopdistanz in Basispunkten, mit Stopdistanz in Basispunkten = (Einstieg − Stop) / Einstieg × 10000.

Für den Stoppfad je Kandidat: cost_R = Einstieg × (fee + fric + slip_in + fee + fric + slip_sl) / (Einstieg − Stop) = 0.0099 × Einstieg / R. Für den Zielpfad: 0.0089 × Einstieg / R. Rechenbeispiel BTC mit der Median-Stopdistanz 1.10 Prozent: 99 bp / 110 bp = 0.90 R. Mit der P25-Stopdistanz 0.67 Prozent: 99 / 67 = 1.48 R. Über alle 98 Kandidaten einzeln gerechnet Median 0.90 R (Median des Einstiegspreises 18470, Median von R 173.9, beide Mediane getrennt).

Im Bibliothekscode `mlib.geometry` sind die Kosten am Ausstieg auf den Einstiegspreis bezogen (Notional am Einstieg), nicht auf den Ausstiegspreis. Die Abweichung beträgt bei einem Ziel 0.8 Prozent über dem Einstieg 42 bp × 0.008 = 0.3 bp, bei einem Stop 1.1 Prozent darunter −0.5 bp, also vernachlässigbar. Der Outcome-Simulator (`simulate_micro.py`, v1.0) rechnet wie `rlib.simulate_trade` die Gebühren auf Einstiegs- und Ausstiegspreis exakt.

## 5. Warum 1.1 bis 1.3 Prozent Risiko zu 0.78 bis 0.90 R Kosten führt

Der Rundlauf K1 kostet 99 bp auf das Notional. Das initiale Risiko R beträgt beim engen 1h-Stop im Median 110 bis 127 bp des Notionals. 99 / 110 = 0.90, 99 / 113 = 0.88, 99 / 127 = 0.78. Es handelt sich um dieselben Basispunkte, nur der Nenner ist klein. Bei der 4h-Baseline mit Stopdistanz 170 bis 246 bp ergibt dasselbe Modell 0.58 (BTC), 0.41 (XRP), 0.40 (DOT) R. Bei BTC Stufe A mit Stopdistanzen um 2.5 bis 4 Prozent lag derselbe Rundlauf bei 0.25 bis 0.40 R, weshalb die Kosten dort nie dominant waren. Die Halbierung der Stopdistanz durch die 1h-Struktur verdoppelt die Kosten in R. Das ist genau der Effekt, den der Forschungsplan als Risiko benannt hat («Nicht: Wie machen wir den Stop enger»), und er ist Eigenschaft der Ausführung, nicht des Signals.

Es folgt nichts zu ändern. K1 bleibt alleiniger Primary-Kostenmassstab, K0 und K2 Sensitivität, keine Maker-Gutschrift in v1.0.

## 6. Erratum zum Vorbericht v0.1, Abschnitt 8

Die dort genannten Werte «K1 Median 0.90 / 0.87 / 0.68 R, K0 0.22 bis 0.29, K2 1.5 bis 2.0» und «p_BE_geo Q1 0.35 / 0.31 / 0.36, K0 Q0 0.48 / 0.46 / 0.45, K2 Q0 0.72 / 0.74 / 0.56» stammen aus `count/count_extra.json`, das über alle engen Kandidaten aller drei Mechanismen gerechnet war (BTC 102, XRP 90, DOT 55), nicht nur M1. Für M1 allein (98 / 79 / 46), das ist die Auswahl der Primary-Zellen, gilt:

| | BTC | XRP | DOT |
|---|---|---|---|
| cost_R K1 Median (P25, P75) | 0.90 (0.67, 1.49) | 0.88 (0.60, 1.23) | 0.78 (0.36, 1.12) |
| cost_R K0 Median | 0.29 | 0.28 | 0.25 |
| cost_R K2 Median | 1.97 | 1.93 | 1.71 |
| RR_geo Q0 K0 / K1 / K2 | 0.91 / 0.29 / −0.16 | 1.09 / 0.35 / −0.01 | 1.24 / 0.49 / 0.14 |
| p_BE_geo Q0 K0 / K1 / K2 | 0.48 / 0.64 / 0.71 | 0.44 / 0.58 / 0.72 | 0.44 / 0.59 / 0.58 |
| RR_geo Q1 K0 / K1 / K2 | 2.17 / 1.07 / 0.40 | 1.87 / 1.09 / 0.53 | 2.37 / 1.54 / 0.76 |
| p_BE_geo Q1 K0 / K1 / K2 | 0.30 / 0.35 / 0.48 | 0.30 / 0.28 / 0.34 | 0.27 / 0.32 / 0.39 |
| Anteil RR_geo Q0 K1 > 0 | 54 von 84 | 49 von 64 | 32 von 37 |

Die Abschnitte 7 und 13 des Vorberichts (RR_geo K1 0.29 / 0.34 / 0.49 und 1.07 / 1.09 / 1.54, p_BE_geo Q0 K1 0.64 / 0.58 / 0.59, Zellgrössen) waren bereits M1-only und bleiben gültig. Der Vorbericht v0.1 wird nicht verändert (SHA in ENTSCHEIDE.md), dieses Erratum wird in der Spezifikation v1.0 referenziert. Die Korrektur enthält keine Outcomes und keine Parameteränderung.
