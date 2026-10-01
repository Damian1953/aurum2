# BTC YAMATO RTC, Stufe A — Auswertungsregeln und Statusdefinitionen, Version 1

**Project Aurum II, `01_forschung/06_btc_specialist/`. 17.09.2026, geschrieben vor dem Outcome-Lauf und vor jeder Sicht auf Outcome-Werte. Präzisiert die Auswertung des eingefrorenen Laufs (Plan v1.1, Parameterpaket v1.1) und übersetzt die Vorgabe «Accelerated Research Mode» (drei Discovery-Ebenen, Fast Fail, Fast Promote) in operative Regeln. Keine Kriterienänderung, keine Schwelle wird nach Sicht auf Ergebnisse gesetzt.**

## 1. Was der Lauf berechnet

Je Hypothese (Y1, Y2, Y3) und je gematchter Kontrolle: R netto K1 (dazu K0 und K2 als Bericht), R brutto, MFE und MAE in R und ATR, Haltedauer, Exit-Grund, Stopdistanz in ATR, Einstiegsdifferenz zum Kandidatenschluss, Bottom Entry Efficiency, Capture Ratio, Exit Efficiency, Giveback (MFE minus realisiertes R), Klassifikation (Trend innerhalb 30 Tagen, verzögerter Trend Tag 31 bis 60, Rebound, Fehlsignal) nach Plan Abschnitt 4 und Umsetzungsentscheid U17, Follow-through nach 1, 3 und 6 Kerzen (Preisfortschritt in ATR, Volumen-z, Taker-Imbalance-Mittel) als Diagnose der Nachfrage nach dem Einstieg, Block P1 und P2, Sicht-1-Equity als Bericht.

Gepaarte Vergleiche je Hypothese: Signal gegen Mittel seiner Kontrollen in R netto, MFE (R), Capture Ratio, Anteil Trend. Signale ohne Kontrolle werden in der Signalstatistik geführt, fallen aber aus dem gepaarten Test. Trade-Bootstrap 2000 mit Seed 20260917 über die Paare, berichtet werden Mittelwert, Median, 5- und 95-Prozent-Perzentil und der Anteil der Bootstrap-Ziehungen mit positiver Differenz. Holm über die drei gepaarten R-Differenzen (Y1, Y2, Y3) für den formalen Test. Effektgrössen und Intervallbreiten sind in der Discovery gleichrangig mit p-Werten.

## 2. Drei Discovery-Ebenen, vorab operationalisiert

**Formal supported.** Kriterium «Signal vorhanden» nach Plan Abschnitt 3 und Mindestzahl 30. Bei den vorliegenden Signalzahlen (16, 14, 6) ist dieser Status für keine Hypothese erreichbar, das steht vor dem Lauf fest.

**Mechanistically promising.** Alle fünf Bedingungen, vorab gesetzt: (a) gepaarte Differenz R netto K1 gegen Kontrollen im Mittel grösser null und Anteil positiver Bootstrap-Ziehungen mindestens 0.80, (b) Median der MFE in R bei Signalen grösser als bei Kontrollen und gepaarte Capture-Ratio-Differenz grösser null, (c) Vorzeichen der gepaarten R-Differenz in beiden Blöcken gleich, sofern jeder Block mindestens 5 Paare hat, sonst nur Gesamtvorzeichen, (d) kein einzelner Trade trägt mehr als 40 Prozent des Bruttogewinns der Hypothese, (e) Erwartung je Trade netto K1 grösser null. Dieser Status ist keine Produktionsfreigabe. Er bedeutet: Die Hypothese verdient eine streng vorregistrierte Validation.

**No evidence.** Weder formal supported noch mechanistically promising. Unterteilt in «inconclusive, insufficient sample» (Bedingungen teilweise erfüllt, kleines n, keine Gegenrichtung) und «not supported in Discovery» (Fast-Fail-Bedingungen erfüllt).

**Fast Fail**, vorab: Eine Hypothese wird in dieser Discovery beendet, wenn die gepaarte R-Differenz gegen Kontrollen im Mittel kleiner oder gleich null ist und die MFE-Differenz nicht positiv ist, oder wenn die Kosten K1 den Bruttoeffekt vollständig aufzehren (Erwartung brutto grösser null, netto K1 kleiner oder gleich null, und K2 negativ), oder wenn das Vorzeichen der gepaarten Differenz in beiden Blöcken gegen die Hypothese steht. Fast Fail beendet die eingefrorene Spezifikation, nicht die Mechanik, eine neue Hypothese bleibt zulässig.

**Fast Promote**, vorab: «Mechanistically promising» plus keine Abhängigkeit von einer einzigen Periode (Effekt nicht nur in einem Kalenderjahr) erlaubt den Übergang in die Validation auf dem Holdout ab 2024 mit Venue-Wechsel Kraken und Kostenstress. Fast Promote bedeutet nur: Validation erlaubt, nicht Produktion.

## 3. Was nicht passiert

Keine Änderung von Trigger, Stop, Exit, Kontext, Toleranzen oder Mindestzahlen nach Sicht auf Ergebnisse. Keine Auswahl von Y1, Y2 oder Y3 nach Ergebnis, alle drei werden berichtet, jede erhält ihren Status nach diesen Regeln. Keine Kombination der Hypothesen. Der Overlap mit BTC-RTC (Framework-Familien CR und FB mit Trigger T0) wird berichtet, sobald die RTC-Library umgesetzt ist, in diesem Lauf noch nicht.

## 4. Produktionsvermerk je Hypothese (Bericht)

Trades je Jahr, Turnover, Anteil Maker- und Taker-Ausführung (Einstieg zur Eröffnung ist Taker, Stops sind Taker, Strukturbruch-Exit zur Eröffnung ist Taker, eine Maker-Variante wäre eine Limit-Order an der Eröffnung und ist eine spätere Execution-Hypothese), nötige Datenlatenz (4h-Kerzenschluss plus Sekunden), Instrument (Kraken Spot Long), Funding (keines auf Spot), Slippage nach K1, maximale Positionsdauer, benötigte API-Daten (OHLCV 4h), Ausführungskomplexität (niedrig: Kandidat am Schluss, Bestätigung am nächsten Schluss, Market-Order zur Eröffnung, ruhende Stop-Order).
