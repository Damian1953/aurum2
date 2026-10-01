# DELAYED-TREND — Outcome-blinder Vorbericht und Economic Geometry Gate, Version 1

**Project Aurum II, `01_forschung/11_delayed_trend/delayed_trend_vorbericht_geometry_gate_v1.md`. 19.09.2026. Messung nach `delayed_trend_measurement_spec_v1.0.md` (fixiert vor der Messung), Library `dtlib.py` v1.0 (5 von 5 Tests: DT1/DT2/DT3 von Hand, Invalidierung und Geometrie, Look-ahead), Skript `measure_dt.py`. Eingaben: eingefrorene Kandidatentabellen (BTC Stufe B 173db748…/e6c2726a…, XRP v1.0 0373bba0…/15d506a8…, DOT v1.0 4ec162e5…/20cd5f48…, Prüfsummen im Lauf geprüft), 4h-Discovery-Dateien. Es wurde nichts nach der Einstiegskerze berechnet: keine Exits, kein r_net, keine MFE/MAE, keine Stop- oder Zieltreffer, keine Trefferquoten, keine Kursentwicklung nach dem Einstieg. Development auf BTC/XRP/DOT, keine ETH/SOL-Daten. Kein P&L-Lauf.**

## 1. Kontext-Events

| | BTC S1 | BTC S2 | XRP S1 | XRP S2 | DOT S1 | DOT S2 |
|---|---|---|---|---|---|---|
| Kontexte | 14 | 96 | 17 | 92 | 15 | 75 |
| davon innerhalb 180 Kerzen invalidiert (Schluss unter L_ref) | 9 | 76 | 8 | 77 | 11 | 66 |
| Median Kerzen bis Invalidierung (nur Kontextstatistik) | 50 | 8 | 34.5 | 10 | 33 | 9 |
| ohne Trendziel (Vorlauf) | 0 | 0 | 0 | 0 | 0 | 0 |
| Blöcke | P1 8, P2 6 | P1 53, P2 43 | P1 6, P2 11 | P1 53, P2 39 | P2a 9, P2b 4, P1 2 | P2a 26, P2b 43, P1 6 |

Die Failed-Breakdown-Kontexte (S2) werden in 79 bis 88 Prozent der Fälle innerhalb des Fensters invalidiert, im Median nach 8 bis 10 Kerzen, weil L_ref das Sweep-Tief der Kandidatenkerze selbst ist. Die Double-Bottom-Kontexte (S1) halten länger (Median 33 bis 50 Kerzen bis zur Invalidierung, 53 bis 73 Prozent invalidiert). Diese Zahlen sind Kontextstatistik zur Zählung der Einstiegsmöglichkeiten, keine Outcome-Aussage über Einstiege.

## 2. Gültige Einstiege je Zelle (Punkte 2 bis 4)

| Coin | Zelle | Kontexte | Einstiege | Anteil | Status ohne Einstieg | Zeit Kontext → Einstieg, Kerzen P25 / Median / P75 (Tage) |
|---|---|---|---|---|---|---|
| BTC | S1×DT1 | 14 | 14 | 100 % | — | 8 / 10 / 11 (1.7) |
| BTC | S1×DT2 | 14 | 6 | 43 % | retest_failed 8 | 5 / 6 / 6 (0.9) |
| BTC | S1×DT3 | 14 | 4 | 29 % | no_consolidation 8, no_breakout 2 | 42 / 50 / 59 (8.3) |
| BTC | S2×DT1 | 96 | 35 | 36 % | invalidiert vor Bestätigung 32, kein Higher Low 29 | 13 / 16 / 20 (2.7) |
| BTC | S2×DT2 | 96 | 49 | 51 % | no_retest_hold 43, retest_failed 4 | 5 / 6 / 9 (1.0) |
| BTC | S2×DT3 | 96 | 5 | 5 % | no_consolidation 86, no_breakout 5 | 21 / 23 / 36 (3.8) |
| XRP | S1×DT1 | 17 | 15 | 88 % | no_higher_low 1, invalidiert 1 | 8 / 11 / 14 (1.8) |
| XRP | S1×DT2 | 17 | 8 | 47 % | retest_failed 7, no_retest_hold 2 | 5 / 5 / 5 (0.8) |
| XRP | S1×DT3 | 17 | 3 | 18 % | no_consolidation 13, no_breakout 1 | 48 / 55 / 62 (9.2) |
| XRP | S2×DT1 | 92 | 43 | 47 % | no_higher_low 28, invalidiert 21 | 12 / 15 / 21 (2.5) |
| XRP | S2×DT2 | 92 | 46 | 50 % | no_retest_hold 39, retest_failed 7 | 5 / 5 / 8 (0.8) |
| XRP | S2×DT3 | 92 | 11 | 12 % | no_consolidation 77, no_breakout 4 | 22 / 25 / 38 (4.2) |
| DOT | S1×DT1 | 15 | 10 | 67 % | invalidiert 3, no_higher_low 2 | 11 / 14.5 / 16 (2.4) |
| DOT | S1×DT2 | 15 | 8 | 53 % | retest_failed 5, no_retest_hold 2 | 5 / 5.5 / 8 (0.9) |
| DOT | S1×DT3 | 15 | 2 | 13 % | no_consolidation 13 | 26 / 29.5 / 33 (4.9) |
| DOT | S2×DT1 | 75 | 31 | 41 % | invalidiert 27, no_higher_low 17 | 14 / 17 / 21 (2.8) |
| DOT | S2×DT2 | 75 | 40 | 53 % | no_retest_hold 32, retest_failed 3 | 5 / 6 / 10 (1.0) |
| DOT | S2×DT3 | 75 | 4 | 5 % | no_consolidation 65, no_breakout 6 | 24 / 29 / 35 (4.8) |

Befund, mechanisch: DT2 (Retest and Hold) tritt fast immer unmittelbar auf (Median 5 bis 6 Kerzen, das ist der früheste zulässige Fall t+3 Retest, t+4 Hold, t+5 Einstieg; gescheiterte Holds vor dem Einstieg Median 0). Der Hold nach Retest ist damit auf 4h fast so häufig wie der Retest selbst, in 43 bis 53 Prozent der Kontexte, und er ist im Wesentlichen ein Einstieg zwei bis drei Kerzen nach dem Kontext auf einem etwas höheren Preis. DT1 (Higher Low) tritt nach im Median 10 bis 17 Kerzen (2 bis 3 Tage) auf, nicht nach 2 bis 4 Wochen wie der Higher Low über der Nackenlinie in DB-CONTEXT, weil die Bedingung hier L_s ≥ L_ref + 0.5 ATR und ein Anstieg von 1 ATR ist. Auf S2 wird DT1 in 21 bis 32 Fällen je Coin durch die schnelle Invalidierung vor der Bestätigung verhindert. DT3 (Konsolidierung 18 Kerzen mit Breite ≤ 3 ATR) entsteht nach einem Selloff-Kontext selten (5 bis 29 Prozent), Einstiege 2 bis 11 je Zelle.

## 3. Geometrie je Zelle (Punkte 5 bis 10)

| Coin | Zelle | n | Stop ATR P25 / Med / P75 | Stop % Med | Kosten K1 in R P25 / Med / P75 | Distanz Ziel ATR Med (%) | RR_geo gross P25 / Med / P75 | RR_geo net K1 Med | p_BE_geo Med | Ziel unter Einstieg |
|---|---|---|---|---|---|---|---|---|---|---|
| BTC | S1×DT1 | 14 | 1.17 / 1.52 / 1.71 | 2.70 | 0.21 / 0.37 / 0.46 | 10.2 (16.7) | 4.07 / 6.83 / 8.59 | 4.29 | 0.19 | 0 |
| BTC | S1×DT2 | 6 | 1.42 / 1.77 / 1.91 | 2.89 | 0.31 / 0.34 / 0.36 | 10.0 (19.2) | 5.03 / 6.18 / 7.51 | 4.96 | 0.17 | 0 |
| BTC | S1×DT3 | 4 | 3.74 / 3.94 / 4.53 | 5.83 | 0.14 / 0.17 / 0.20 | 10.3 (16.0) | 2.11 / 2.81 / 3.49 | 2.27 | 0.31 | 0 |
| BTC | S2×DT1 | 35 | 1.44 / 1.64 / 2.19 | 3.88 | 0.20 / 0.26 / 0.37 | 9.3 (19.1) | 3.75 / 5.32 / 7.10 | 4.03 | 0.20 | 0 |
| BTC | S2×DT2 | 49 | 1.01 / 1.26 / 1.51 | 2.84 | 0.21 / 0.35 / 0.50 | 9.7 (20.8) | 5.01 / 7.54 / 13.15 | 5.32 | 0.16 | 0 |
| BTC | S2×DT3 | 5 | 3.95 / 3.96 / 4.49 | 12.67 | 0.07 / 0.08 / 0.12 | 5.6 (16.2) | 1.28 / 1.43 / 2.00 | 1.17 | 0.46 | 0 |
| XRP | S1×DT1 | 15 | 1.36 / 1.62 / 2.13 | 3.26 | 0.20 / 0.30 / 0.39 | 7.4 (12.3) | 2.11 / 5.58 / 7.44 | 3.55 | 0.20 | 1 |
| XRP | S1×DT2 | 8 | 1.02 / 1.45 / 1.62 | 3.91 | 0.23 / 0.25 / 0.48 | 7.0 (23.8) | 4.67 / 6.03 / 6.84 | 4.02 | 0.20 | 0 |
| XRP | S1×DT3 | 3 | 4.33 / 4.35 / 4.51 | 9.00 | 0.11 / 0.11 / 0.12 | 10.4 (21.9) | 1.77 / 2.24 / 2.90 | 1.95 | 0.34 | 0 |
| XRP | S2×DT1 | 43 | 1.14 / 1.60 / 1.99 | 3.40 | 0.18 / 0.29 / 0.46 | 9.0 (18.4) | 4.10 / 6.33 / 8.56 | 4.67 | 0.18 | 0 |
| XRP | S2×DT2 | 46 | 0.93 / 1.23 / 1.61 | 3.48 | 0.20 / 0.29 / 0.47 | 9.2 (20.5) | 4.62 / 7.77 / 11.29 | 5.34 | 0.16 | 0 |
| XRP | S2×DT3 | 11 | 3.76 / 3.99 / 5.11 | 7.03 | 0.11 / 0.14 / 0.16 | 8.1 (14.3) | 1.58 / 1.82 / 2.65 | 1.46 | 0.41 | 0 |
| DOT | S1×DT1 | 10 | 1.36 / 1.60 / 1.82 | 5.23 | 0.13 / 0.19 / 0.27 | 6.5 (20.5) | 1.91 / 4.48 / 6.63 | 3.45 | 0.19 | 1 |
| DOT | S1×DT2 | 8 | 1.09 / 1.31 / 1.41 | 3.74 | 0.22 / 0.27 / 0.39 | 8.3 (26.1) | 3.50 / 5.83 / 10.87 | 4.81 | 0.17 | 0 |
| DOT | S1×DT3 | 2 | 3.61 / 3.80 / 4.00 | 13.58 | 0.07 / 0.07 / 0.07 | 6.3 (23.3) | 1.30 / 1.73 / 2.16 | 1.55 | 0.43 | 0 |
| DOT | S2×DT1 | 31 | 1.71 / 1.92 / 2.27 | 4.51 | 0.14 / 0.22 / 0.36 | 10.3 (17.3) | 3.40 / 5.61 / 7.85 | 3.91 | 0.20 | 0 |
| DOT | S2×DT2 | 40 | 1.02 / 1.30 / 1.50 | 2.75 | 0.24 / 0.36 / 0.49 | 10.4 (24.8) | 6.84 / 9.02 / 10.79 | 5.83 | 0.15 | 0 |
| DOT | S2×DT3 | 4 | 3.55 / 3.81 / 4.14 | 7.91 | 0.09 / 0.14 / 0.19 | 7.3 (14.0) | 1.21 / 2.09 / 3.21 | 1.67 | 0.39 | 0 |

Lesart, ausschliesslich geometrisch: Das Trendziel (120-Kerzen-Hoch vor dem Selloff, `hh120` an der Referenzkerze) liegt im Median 6 bis 10 ATR beziehungsweise 12 bis 26 Prozent über dem Einstieg, weil der Kontext einen Drawdown von mindestens 12 Prozent (BTC) beziehungsweise 6 ATR (XRP, DOT) voraussetzt. Bei Stops von 1.2 bis 1.9 ATR (DT1, DT2) ergibt das RR_geo gross von 4.5 bis 9 im Median und Kosten von 0.19 bis 0.37 R. Das ist die geometrische Voraussetzung, nicht eine Erwartung: Ob das Vor-Selloff-Hoch je erreicht wird, ist die unbeantwortete Outcome-Frage (die eingefrorenen Läufe zeigen 21 bis 50 Prozent neue 20-Tage-Hochs innerhalb 60 Tagen, das 120-Kerzen-Hoch liegt höher). DT3 ist die Ausnahme: Der Stop unter dem Boxtief bei Einstieg über dem Boxhoch beträgt strukturell Boxbreite plus 0.5 ATR, im Median 3.8 bis 4.4 ATR, und RR_geo fällt auf 1.4 bis 2.8. Das ist eine Eigenschaft der eingefrorenen DT3-Definition, sie wird nicht verändert.

## 4. Economic Geometry Gate je Zelle (Punkt 11) und Fallzahlen (Punkt 14)

Gate A Median Stop ≤ 3.0 ATR, B Median Kosten K1 ≤ 0.40 R, C Median RR_geo gross ≥ 1.50, D P25 RR_geo gross ≥ 1.00, E erwartete Einstiege ≥ 20 (Untergrenze nach Messregeln Abschnitt 6 Punkt 14: Einstiege ohne Folgeeinstieg derselben Zelle innerhalb 180 Kerzen; Obergrenze: alle Einstiege).

| Coin | Zelle | A | B | C | D | Einstiege Unter- / Obergrenze | E (Untergrenze) | Gate | Anteil Einzelfälle mit A, B, C erfüllt |
|---|---|---|---|---|---|---|---|---|---|
| BTC | S1×DT1 | ja | ja | ja | ja | 13 / 14 | nein | **nein (E)** | 57 % |
| BTC | S1×DT2 | ja | ja | ja | ja | 6 / 6 | nein | nein (E) | 83 % |
| BTC | S1×DT3 | nein | ja | ja | ja | 4 / 4 | nein | nein (A, E) | 0 % |
| BTC | S2×DT1 | ja | ja | ja | ja | 21 / 35 | ja | **PASS** | 69 % |
| BTC | S2×DT2 | ja | ja | ja | ja | 19 / 49 | nein | **nein (E, Untergrenze 19)** | 63 % |
| BTC | S2×DT3 | nein | ja | nein | ja | 5 / 5 | nein | nein (A, C, E) | 0 % |
| XRP | S1×DT1 | ja | ja | ja | ja | 13 / 15 | nein | nein (E) | 53 % |
| XRP | S1×DT2 | ja | ja | ja | ja | 8 / 8 | nein | nein (E) | 50 % |
| XRP | S1×DT3 | nein | ja | ja | ja | 3 / 3 | nein | nein (A, E) | 0 % |
| XRP | S2×DT1 | ja | ja | ja | ja | 22 / 43 | ja | **PASS** | 65 % |
| XRP | S2×DT2 | ja | ja | ja | ja | 21 / 46 | ja | **PASS** | 67 % |
| XRP | S2×DT3 | nein | ja | ja | ja | 7 / 11 | nein | nein (A, E) | 0 % |
| DOT | S1×DT1 | ja | ja | ja | ja | 9 / 10 | nein | nein (E) | 80 % |
| DOT | S1×DT2 | ja | ja | ja | ja | 7 / 8 | nein | nein (E) | 50 % |
| DOT | S1×DT3 | nein | ja | ja | ja | 2 / 2 | nein | nein (A, E) | 0 % |
| DOT | S2×DT1 | ja | ja | ja | ja | 12 / 31 | nein | **nein (E, Untergrenze 12)** | 65 % |
| DOT | S2×DT2 | ja | ja | ja | ja | 12 / 40 | nein | **nein (E, Untergrenze 12)** | 55 % |
| DOT | S2×DT3 | nein | ja | ja | ja | 4 / 4 | nein | nein (A, E) | 0 % |

Einzelfallebene: Die 31 bis 50 Prozent der DT1/DT2-Einstiege, die A, B, C nicht alle erfüllen, scheitern fast ausschliesslich an B (Kosten über 0.40 R bei Stops um 1 ATR, Anteil 19 bis 45 Prozent), selten an A (Stop über 3 ATR, 0 bis 16 Prozent) oder C.

Blöcke der Einstiege (Obergrenze): BTC S2×DT1 P1 22, P2 13; S2×DT2 P1 30, P2 19. XRP S2×DT1 P1 25, P2 18; S2×DT2 P1 26, P2 20. DOT S2×DT1 P2a 10, P2b 17, ungewertet 4; S2×DT2 P2a 13, P2b 24, ungewertet 3. Hochrechnung ETH / SOL (Kerzenzahl aus dem Manifest, ohne Daten): S2×DT1 Untergrenze 21 bis 25 / 11 bis 13, Obergrenze 35 bis 59 / 19 bis 31; S2×DT2 Untergrenze 19 bis 24 / 10 bis 13, Obergrenze 49 bis 76 / 26 bis 40; alle S1-Zellen unter 20 auf beiden Coins.

## 5. Überschneidung der Familien (Punkt 12)

Kontexte mit Einstieg in mehreren Familien: BTC S1 DT1∩DT2 6, DT1∩DT3 4, alle drei 2 (von 14); S2 DT1∩DT2 24, DT1∩DT3 5, alle drei 3 (von 60 Kontexten mit Einstieg). XRP S1 8, 3, 1 (von 15); S2 34, 11, 11 (von 55), eine gleiche Einstiegskerze. DOT S1 7, 2, 2 (von 11); S2 26, 4, 4 (von 45). Rund die Hälfte der DT1-Einstiege auf S2 hat im selben Kontext einen früheren DT2-Einstieg. Die Familien sind getrennte Sleeves, es wird keine gewählt.

## 6. Look-ahead-Prüfung (Punkt 13)

`tests/test_dtlib.py`, 5 von 5: DT1 Bestätigung erst am Schluss von s+3 und Einstieg s+4, Rise- und Abstandsbedingung, Fensterregel; DT2 Hold-Kerze, gescheiterter Retest beendet die Familie, gescheiterter Hold lässt weitersuchen, kein Retest vor t+3; DT3 Boxbreite, Schluss-Bedingung, Breakout innerhalb der Box zählt nicht; Invalidierung an der ersten Schlusskerze unter L_ref, Zielreferenz `hh120`, Kostenformel von Hand; Look-ahead auf synthetischer Serie mit 12 Einstiegen vor T: alle Einstiege, Stops und Geometrien invariant gegen Störung aller Kerzen ab T.

## 7. Gate-Ergebnis und offene Punkte (STOP)

Nach den fixierten Regeln bestehen drei Zellen das Gate: **BTC S2×DT1, XRP S2×DT1, XRP S2×DT2.** Alle S1-Zellen scheitern an der Fallzahl (14 bis 17 Kontexte, das war vor der Messung erwartet). Alle DT3-Zellen scheitern an A (strukturell weite Stops) und an der Fallzahl. Drei S2-Zellen scheitern nur an E mit der Untergrenze (BTC S2×DT2 19, DOT S2×DT1 12, DOT S2×DT2 12), bei Obergrenzen von 49, 31 und 40.

Was die Untergrenze misst: «kein Folgeeinstieg derselben Zelle innerhalb 180 Kerzen» unterstellt, dass jede Position das volle Kontextfenster offen bleibt. Die tatsächliche Fallzahl eines P&L-Laufs liegt zwischen Unter- und Obergrenze und hängt von den Exits ab (die E-D-Haltedauern der eingefrorenen Läufe lagen im Median bei 13 bis 49 Kerzen). Die Regel wurde vor der Messung so fixiert und wird hier nicht geändert.

Offene Entscheidungen vor einem P&L-Freeze (keine davon wird von mir vorweggenommen):

1. Gate-E-Lesart: nur die drei Zellen mit Untergrenze ≥ 20 (BTC S2×DT1, XRP S2×DT1, XRP S2×DT2) in den P&L-Lauf, oder zusätzlich die drei Zellen mit Obergrenze ≥ 20 (BTC S2×DT2, DOT S2×DT1, DOT S2×DT2) mit dem Vermerk, dass die realisierte Zahl erst nach Exits feststeht und die Low-Frequency-Regel dann greift. Empfehlung: die drei sicheren Zellen primär, die drei Grenzfälle als vorregistrierte Sekundärzellen mit Holm über alle sechs, keine nachträgliche Aufwertung.
2. S1 (Double Bottom) gesamt: alle sechs S1-Zellen unter 20 Einstiegen, damit deskriptiv. Mitführen als deskriptive Zellen (wie M2/M3 in REBOUND-MICRO) oder aus dem P&L-Lauf ausschliessen. Empfehlung: deskriptiv mitführen, ohne Test.
3. DT3: Spezifikation abgeschlossen ohne P&L (Gate A auf allen sechs Zellen verfehlt, 2 bis 11 Einstiege), oder deskriptiv mitführen. Empfehlung: abschliessen, keine Stop-Variante.
4. Exit für den P&L-Lauf bestätigen: Tages-ATR14-Chandelier 3×, nur steigend, initialer Stop, Zeitstopp t+360, keine Alternative (Forschungsplan Abschnitt 5, outcome-informed aus E-D, als solches ausgewiesen).
5. Kontrollgruppe: dieselben drei Einstiegsbedingungen auf gematchten Kontextkerzen ohne Bottom-Struktur mit Ersatzniveaus (Ersatz-P = max(H, t−18..t), Ersatz-L_ref = min(L, t−120..t)), wie Forschungsplan Abschnitt 8, bestätigen.
6. Primary-Metrik des P&L-Laufs: gepaarte ΔR gegen Kontrollen (wie XRP/DOT v1.0) oder Netto-Erwartung K1 absolut mit Economic Validation Gate. Empfehlung: beides berichten, Status nach Regel v2 auf der gepaarten Differenz, Fortführung nur bei Netto K1 ≥ 0.

STOP. Kein DT-P&L-Lauf ohne neue Freigabe. Keine ETH/SOL-Daten.
