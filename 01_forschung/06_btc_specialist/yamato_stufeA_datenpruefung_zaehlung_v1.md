# BTC YAMATO RTC, Stufe A — Datenprüfung, Library, Tests, Kandidatenzählung, Matching, Version 1.1

**Project Aurum II, `01_forschung/06_btc_specialist/stufeA/`. 17.09.2026. Stand nach dem Freeze (Plan v1.0 SHA 56069bc0…, Parameterpaket 98376c2d…). Dieses Dokument enthält keine Performance-Auswertung: keine R-Werte, keine Erwartungen, keine MFE, keine Kontrollgruppen-Differenzen. Die Simulation wurde ausgeführt, damit Positionsfenster für das Matching vorliegen, ihre Ergebnisspalten wurden nicht gelesen und liegen nur in `stufeA/_private/`. Am Ende steht ein Halt mit zwei strukturellen Befunden, die vor jeder Ergebnisberechnung entschieden werden müssen.**

## 1. Datenvalidierung

Eingabe: `02_daten/raw/binance_full/BTCUSDT_4h.csv` (SHA-256 f8d0e58dd88c583138e079772f78bb7401f3b33f3e18d1870ec7476617d715b3, 19890 Kerzen, 2017-08-17 04:00 bis 2026-09-16 20:00 UTC). Prüfungen: 4h-Raster vollständig eingehalten, OHLC-Konsistenz ohne Befund, keine Kerze mit Volumen null oder Range null, Taker-Buy nie über Volumen, Vollspalten-Tageskerzen gegen OHLCV 0 Abweichungen, 4h auf Tag aggregiert 0 Abweichungen (Loader-Gegenproben). Lücken: 9, zusammen 17 fehlende Kerzen, alle 2017-09 bis 2020-02, längste 7 Kerzen (2018-02-08 00:00 bis 2018-02-09 08:00, Binance-Wartung), keine Lücke nach Februar 2020.

Discovery-Kopie: `BTCUSDT_4h_discovery.csv`, physisch abgeschnitten nach der Kerze 2023-12-31 20:00 UTC, 13950 Kerzen (P1 7380, P2 6570), SHA-256 2d394fd1cbc344d5e012e12b40bc5835fef0fbe72f0678c2abf417babd96a7e6. Alle Läufe dieser Stufe lesen ausschliesslich diese Datei. Kraken XBTUSD 240 im selben Fenster: 13958 Kerzen, 3 Lücken (10 Kerzen) bis Januar 2018, ab 2018 vollständig, in Stufe A nicht verwendet (Ebene B ist Validation).

Nebenbefund 1h: Der 1h-Lauf ist für sechs Coins vollständig, für BTC, ETH, BNB, LTC Spot hat Binance am 09.02.2018 Stundenkerzen ausserhalb des Rasters publiziert (Beginn hh:28:14), der Loader hat diese Reihen abgelehnt. `nachladen_1h.py` (SHA ab119e8d…) quarantäniert solche Kerzen jetzt mit Protokoll, `Daten-nachladen-1h-Nachtrag.command` lädt die vier Reihen nach. Für Stufe A ohne Bedeutung.

## 2. Library und Umsetzungsentscheide

`ylib.py` (SHA 3610b303…) setzt Parameterpaket und Umsetzungsentscheide U1 bis U20 um: Wilder-ATR14, EMA50, Geometrie, `volume_zscore` 60, K1 bis K3, Swing-Bestätigung 3/3 strikt, drei Niveaus Stand t−1, Failed Breakdown, Y3, Double Bottom mit Nackenlinie und Zeitordnung, Trigger TA, Stop mit 3-ATR-Grenze, Exit E-U (Chandelier plus Strukturbruch), Kosten K0 bis K2, Kontrollpool und Matching. Alle Zahlen stehen in einem Block `FROZEN` und werden nirgends überschrieben. Die Umsetzungsentscheide stehen in `yamato_stufeA_umsetzungsentscheide_v1.md` und wurden vor der ersten Zählung geschrieben. Eine Ergänzung zu U8 wurde bei der Umsetzung nötig und ist hier festgehalten: s1 ist das jüngste qualifizierende Swing Low vor s2, und die Eindeutigkeit (ein Kandidat je Kerze, keine zweite Kandidatenkerze innerhalb 12 Kerzen) wird in Zeitordnung der Kandidatenkerzen geprüft, nicht in Iterationsreihenfolge der Paare. Die erste Fassung hatte das in Iterationsreihenfolge geprüft, der Permutationstest hat den Fehler aufgedeckt (Abschnitt 3), die Korrektur erfolgte vor jeder Zählung.

## 3. Tests

Unit-Tests (`tests/test_ylib.py`, 8 Tests, alle bestanden): Wilder-ATR auf konstanter Range, Swing-Bestätigung strikt mit Gleichstand, Niveaus und Zone mit drei Berührungen, Verfall alter Swings, Failed Breakdown auf Swing- und 120-Kerzen-Niveau, Y3 mit Body und Volumen-z, Kontext und Kandidat nach synthetischem Selloff, Double Bottom mit Nackenlinienbruch (s1, h1, s2, t exakt), Trigger TA, Chandelier-Exit, Strukturbruch-Exit zur Folgeeröffnung, Kontrollmatching mit Abstands- und Positionsausschluss.

Look-ahead-Tests (`lookahead_test.py`, `lookahead_test.json`): Abschneidetest bei 2022-06-30 20:00 (Kerze 10655): alle Merkmale, Swings, Y1- und Y3-Kandidaten und 302 Y2-Paare bis Kerze 10651 bitgleich mit dem Volllauf. Permutationstest an 25 zufälligen Kerzen (Seed 20260917): Merkmale, Niveaus, Kontext, Failed Breakdown, Y3 und Y2-Kandidaten bis t−3 unverändert bei permutierten Folgekerzen, 25 von 25 bestanden. Der erste Durchlauf hatte 6 von 25 Y2-Abweichungen, Ursache war die Iterationsreihenfolge (Abschnitt 2), nach Korrektur 25 von 25.

## 4. Kandidatenzählung (Discovery-Fenster, 13816 bewertete Kerzen nach Warmup)

Swings: 1422 bestätigte Swing Lows, 1413 Swing Highs. K1 (mindestens 12 Prozent unter dem 20-Tage-Hoch) auf 4869 Kerzen in 169 Episoden, K1 und K2 auf 2539 Kerzen, voller Kontext K1 bis K3 auf 1842 Kerzen (P1 948, P2 894).

| Hypothese | Kandidaten | P1 | P2 | Bemerkung |
|---|---|---|---|---|
| Y1 Failed Breakdown | 96 | 53 | 43 | Niveaus: 120-Kerzen-Tief 28, Zone 27, Swing 14, Kombinationen 27. Ohne Kontext gäbe es 306 Failed Breakdowns |
| Y2 Double Bottom | 14 | 8 | 6 | 425 gültige Paare vor Zeitordnung, 249 Duplikate (mehrere s1 je Bruchkerze), 377 ohne Kontext auf s2, 9 der 14 mit drittem Tief (Triple) |
| Y3 Wick plus Volumen | 29 | 15 | 14 | ohne Kontext 61 |

Überlappung: Y1 und Y3 teilen 23 Kerzen, Y2 überlappt mit keiner, Vereinigung 116 Kandidatenkerzen. Y1 nach Jahr: 2017 2, 2018 34, 2019 13, 2020 4, 2021 23, 2022 15, 2023 5.

## 5. Bestätigung und Signale (Zählung, keine Outcomes)

| Hypothese | Kandidaten | TA erfüllt | in Position | Stop über 3 ATR | gehandelte Signale | P1 | P2 |
|---|---|---|---|---|---|---|---|
| Y1 | 96 | 23 (24 Prozent) | 6 | 5 | 16 | 9 | 7 |
| Y2 | 14 | Bruchkerze ist Bestätigung | 0 | 14 | 0 | 0 | 0 |
| Y3 | 29 | 10 (34 Prozent) | 0 | 4 | 6 | 3 | 3 |

Keine Position war am Schnitt offen. Median von (C_{t+1} − H_t) / ATR über die Y1-Kandidaten liegt bei −0.34, die Kandidatenkerze hat im Median eine Range von 1.31 ATR. Bei den bestätigten Y1-Kandidaten liegt der Abstand Einstieg zu Stop zwischen 1.3 und 4.3 ATR, fünf davon über 3 ATR.

## 6. Kontrollgruppe

Kontrollpool: 1666 Kontextkerzen ohne eines der drei Muster und ausserhalb der Böden gültiger Y2-Paare (P1 851, P2 815). Matching Y1: 16 Signale, 11 mit drei Kontrollen, 4 mit einer, 1 ohne, im Mittel 2.31, 37 verschiedene Kontrollkerzen, keine mehrfach verwendet, median 11 Poolkerzen im Fenster vor Auswahl, TA-Bestätigungsquote der Kontrollen 24 Prozent (Signale 24 Prozent). Matching Y3: 6 Signale, 1 mit drei, 3 mit einer, 2 ohne, im Mittel 1.0, TA-Quote der Kontrollen 17 Prozent. Die Toleranzen wurden nicht erweitert. Die Abdeckung ist für Y1 brauchbar, für Y3 schwach, für Y2 gegenstandslos.

## 7. Halt: zwei strukturelle Befunde vor jeder Ergebnisberechnung

**Befund 1, Y2 ist unter den eingefrorenen Regeln nicht handelbar.** Der Y2-Stop liegt unter dem zweiten Tief (L_{s2} − 0.5 ATR), der Einstieg an der Nackenlinie, die per Definition mindestens 2 ATR über den Tiefs liegt. Der Abstand Einstieg zu Stop beträgt bei allen 14 Kandidaten 3.1 bis 7.3 ATR (Median 4.75), die Abbruchgrenze liegt bei 3 ATR. Y2 erzeugt deshalb null Trades, unabhängig vom Marktverlauf. Das ist kein Marktbefund, sondern ein innerer Widerspruch der eingefrorenen Spezifikation: Nackenlinienhöhe (mindestens 2 ATR), Stop-Puffer (0.5 ATR) und Abbruchgrenze (3 ATR) lassen nur Paare mit Nackenlinie zwischen 2.0 und 2.5 ATR über dem Tief zu, und auch diese nur ohne Eröffnungslücke.

**Befund 2, alle drei Hypothesen liegen unter der Mindestzahl.** Y1 16 Signale, Y3 6, Y2 0. Nach der eingefrorenen Stufung (30 vollwertig, 20 bis 29 geringe Basis, unter 20 deskriptiv) wäre Stufe A auf BTC in dieser Form vollständig deskriptiv, kein Test könnte «Signal vorhanden» erreichen. Ursache ist nicht die Kandidatenzahl (96 Y1-Kandidaten liegen im geschätzten Bereich), sondern die Bestätigungsquote von TA: Die Folgekerze schliesst nur in 24 Prozent der Fälle über dem Hoch einer Sweep-Kerze, die selbst 1.3 ATR Range hat. Meine Schätzung von 50 bis 60 Prozent im Plan v0.2 war falsch. Dazu die Abbruchgrenze von 3 ATR, die bei 5 der 23 bestätigten Y1-Kandidaten greift.

Beide Befunde stammen aus Zählungen, nicht aus Ergebnissen. Kein Outcome wurde berechnet, gelesen oder berichtet. Nach dem Freeze-Protokoll darf keine Zahl geändert werden. Die Entscheidung, wie mit Stufe A weiter verfahren wird, liegt beim Auftraggeber und wird in ENTSCHEIDE protokolliert, bevor irgendeine Ergebnisberechnung startet.

## 8. Dateien

`stufeA/ylib.py`, `stufeA/tests/test_ylib.py`, `stufeA/lookahead_test.py`, `stufeA/count_stufeA.py`, `stufeA/data/BTCUSDT_4h_discovery.csv`, `stufeA/data/datenpruefung_stufeA.json`, `stufeA/data/lookahead_test.json`, `stufeA/data/count_stufeA.json`, `stufeA/data/candidates_y1_y3.csv` (SHA c3bce1b9…), `stufeA/data/candidates_y2.csv` (SHA e6c2726a…), `yamato_stufeA_umsetzungsentscheide_v1.md`. Nicht Teil des Berichts: `stufeA/_private/` (Trade- und Kontrolltabellen mit ungelesenen Outcome-Spalten).

## 9. Nachtrag Version 1.1 (17.09.2026, vor jeder Ergebnisberechnung)

Entscheid des Auftraggebers: Weg 2, eng begrenzt auf den strukturellen Y2-Spezifikationsdefekt. Plan v1.1 und Parameterpaket v1.1 ändern ausschliesslich den Wegfall der 3-ATR-Abbruchgrenze für Y2 (Plan Abschnitt 13a), Y1 und Y3 bleiben unverändert und werden mit 16 beziehungsweise 6 Signalen nach den eingefrorenen Regeln nur deskriptiv ausgewertet, Status «inconclusive, insufficient sample» (Plan Abschnitt 11a). TA wird nicht gelockert, die Bestätigungsquote ist selbst ein Befund für Stufe B (H3).

Umsetzung: `ylib.py` (SHA 81a74f2a…), eine Zeile in `run_sleeve` (Y2 ohne `stop_too_wide`), dazu `stop_dist_atr` je Trade. Neuer Unit-Test `test_y2_no_cap_v11` (Y2 mit 5.5 ATR wird gehandelt, Y1 mit gleicher Distanz nicht), alle 9 Tests bestanden. Look-ahead-Tests unverändert bestanden (Abschneidetest bitgleich, Permutation 25 von 25). Kandidatenlisten unverändert (SHA c3bce1b9…, e6c2726a…).

Y2 nach v1.1: alle 14 Kandidaten werden gehandelt (P1 8, P2 6), keine andere Regel schliesst einen aus (keine Position-Überlappung, kein Einstieg unter dem Stop, keine Kerze am Schnitt). Entry-Stop-Distanz in ATR: Median 4.75, Bereich 3.11 bis 7.31, alle 14 über 3 ATR, das nominelle Risiko bleibt 2 Prozent je Trade mit entsprechend kleinerer Position. Zum Vergleich Y1 Median 1.89 (1.31 bis 2.91), Y3 Median 2.66 (2.31 bis 2.91).

Kontrollgruppe Y2: Mit der Bruchkerze als Referenz fanden 10 von 14 Signalen keine Kontrolle, weil die Bruchkerze 3 bis 36 Kerzen nach dem Boden liegt und dort keine Selloff-Merkmale mehr trägt. Umsetzungsentscheid U21 (analog U7): Referenzkerze für das Y2-Matching ist das zweite Tief s2, Toleranzen unverändert. Damit 8 von 14 Signalen mit drei Kontrollen, 3 mit zwei, 2 mit einer, 1 ohne, im Mittel 2.29, 30 verschiedene Kontrollkerzen, 2 mehrfach verwendet, TA-Quote der Kontrollen 23 Prozent. Abdeckung für Y2 ausreichend, für Y1 ausreichend (11 von 16 mit drei), für Y3 schwach (1 von 6 mit drei), keine Toleranz erweitert.

Weiterhin kein Outcome berechnet, gelesen oder berichtet. Der einmalige Stufe-A-Outcome-Lauf wartet auf die Freigabe.
