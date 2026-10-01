# BTC YAMATO RTC, Stufe A — Bericht des einmaligen Outcome-Laufs, Version 1

**Project Aurum II, `01_forschung/06_btc_specialist/`. 17.09.2026. Eingefrorene Spezifikation Plan v1.1 (SHA aa8195ce…), Parameterpaket v1.1 (7c4be2f8…), Library `ylib.py` (81a74f2a…), Auswertungsregeln v1 (vor dem Lauf geschrieben), Eingabe `BTCUSDT_4h_discovery.csv` (2d394fd1…), Seed 20260917, Bootstrap 2000. Ein Lauf, keine Wiederholung, keine Parameteränderung. Kosten primär K1 (Kraken Spot Tier 1), K0 und K2 als Bericht. Status nach den vorab operationalisierten drei Discovery-Ebenen.**

## 1. Ergebnis in einem Absatz

Keine der drei Bottom-Hypothesen zeigt in der Discovery auf BTC 2017 bis 2023 Evidenz für einen Edge. Y1 (Failed Breakdown, 16 Signale) verliert netto K1 im Mittel 0.23 R je Trade und liegt gepaart unter seinen gematchten Kontrollen (Differenz −0.34 R, Bootstrap-Anteil positiv 2 Prozent), Status «not supported, Fast Fail». Y2 (Double Bottom, 14 Signale) verliert netto 0.30 R je Trade bei nur einem Gewinner, liegt aber gepaart über seinen Kontrollen (+0.75 R, alle sechs Paare positiv), weil die Kontrollen noch stärker verlieren, und erreicht die Hälfte der «mechanistically promising»-Bedingungen, Status «inconclusive, insufficient sample». Y3 (Wick plus Volumen, 6 Signale, 1 gepaarte Kontrolle) ist nicht auswertbar, Status «inconclusive». Der gemeinsame Befund, der schwerer wiegt als jede Einzelhypothese: Kontextkerzen nach einem Selloff mit TA-Bestätigung und E-U-Exit verlieren als Basisrate Geld (Kontrollen −0.30 bis −1.05 R), und die Sakata-Bestätigung reduziert den Verlust, hebt ihn aber nicht auf. Die eingefrorene Kombination aus 4h-Kandidat, Ein-Kerzen-Bestätigung, Stop unter der Struktur und Chandelier 3 ATR14 ist auf BTC nicht tragfähig. Das ist die Aussage über die Spezifikation, nicht über die Mechanik.

## 2. Zahlen je Hypothese

| | Y1 Failed Breakdown | Y2 Double Bottom | Y3 Wick plus Volumen |
|---|---|---|---|
| Signale (P1, P2) | 16 (9, 7) | 14 (8, 6) | 6 (3, 3) |
| R netto K1, Mittel / Median | −0.23 / −0.80 | −0.30 / −0.35 | −0.29 / −0.91 |
| R netto K0 / K2 | −0.09 / −0.46 | −0.22 / −0.43 | −0.21 / −0.43 |
| Trefferquote netto K1 | 19 Prozent | 7 Prozent | 17 Prozent |
| P&L in ATR, Mittel / Median | −0.47 / −1.58 | −1.41 / −1.61 | −0.67 / −2.40 |
| Stopdistanz ATR, Median (Bereich) | 1.89 (1.44 bis 2.90) | 4.75 (3.34 bis 7.29) | 2.66 (2.32 bis 2.91) |
| MFE in R, Mittel / Median | 1.19 / 0.46 | 0.34 / 0.29 | 0.84 / 0.08 |
| MAE in R, Median | 0.70 | 0.27 | 0.77 |
| Haltedauer Kerzen, Median | 12.5 | 15.5 | 9 |
| Exit-Gründe | Chandelier 8, Struktur 4, Stop 4 | Chandelier 10, Struktur 4 | Chandelier 3, Stop 2, Struktur 1 |
| Klassifikation | Fehlsignal 10, Trend 4, Rebound 2 | Fehlsignal 10, Trend 3, verzögert 1 | Fehlsignal 5, Rebound 1 |
| Neues 20-Tage-Hoch innerhalb 30 / 60 Tagen | 25 / 31 Prozent | 21 / 50 Prozent | 0 / 17 Prozent |
| Persistenz 30 Kerzen nach neuem Hoch | 20 Prozent | 71 Prozent | (1 Fall) |
| Bottom Entry Efficiency, Median | 0.43 | 0.41 | 0.12 |
| Abstand Einstieg zum ex-post Tief, Median ATR | 2.9 | 5.0 | 2.6 |
| Capture Ratio, Median | −0.16 | −0.16 | −0.72 |
| Giveback (MFE minus realisiert), Median R | 1.15 | 0.54 | 1.00 |
| Konzentration Top-1-Trade am Bruttogewinn | 52 Prozent | 85 Prozent | 100 Prozent |
| Jahre mit positivem Netto | 1 von 5 | 0 von 6 | 1 von 4 |
| Block P1 / P2 R netto Mittel | +0.14 / −0.70 | −0.29 / −0.30 | +0.31 / −0.89 |
| Follow-through Preis nach 1 / 3 / 6 Kerzen, ATR | −0.33 / −0.60 / −0.91 | −0.01 / −0.41 / −0.42 | −0.93 / −2.24 / −3.21 |

Kontrollen (Kontext ohne Muster, gleicher Trigger, Stop, Exit): Y1 37 Kontrollkerzen, 9 mit TA gehandelt (24 Prozent), R netto Mittel −0.30, Median −0.72, MFE Median 0.77, Klassifikation Trend 4, Fehlsignal 3, Rebound 2. Y2 (Referenz zweites Tief, U21) 30 Kontrollkerzen, 7 gehandelt (23 Prozent), R netto Mittel −1.05, Median −1.14, alle sieben Verlierer, P&L in ATR Mittel −1.69. Y3 6 Kontrollkerzen, 1 gehandelt.

Gepaarte Differenzen Signal minus Mittel der Kontrollen (Bootstrap 2000, 5- und 95-Prozent-Perzentil, Anteil positiv):

| | Paare | ΔR netto | ΔMFE | ΔCapture | ΔTrend-Anteil |
|---|---|---|---|---|---|
| Y1 | 8 | −0.34 (−0.67 bis −0.06), 2 Prozent | −0.20 (−0.54 bis 0.16), 18 Prozent | −0.16 (−0.29 bis −0.04), 1 Prozent | −0.06, 29 Prozent |
| Y2 | 6 | +0.75 (+0.51 bis +1.00), 100 Prozent, P1 +0.70, P2 +0.80 | −0.25 (−0.65 bis 0.14), 15 Prozent | +0.08 (−0.01 bis +0.18), 92 Prozent | +0.17, 66 Prozent |
| Y3 | 1 | nicht auswertbar | | | |

Holm über die drei ΔR-Tests: keine Hypothese erreicht «Signal vorhanden» in positiver Richtung (Y1 ist signifikant negativ, Y2 positiv mit sechs Paaren, Y3 leer). Formal supported: keine, das stand vor dem Lauf fest (Mindestzahl 30).

## 3. Status nach den vorab definierten Regeln

**Y1: not supported, Fast Fail.** Alle fünf MP-Bedingungen verfehlt: gepaarte R-Differenz negativ mit 2 Prozent positiven Ziehungen, MFE-Median unter den Kontrollen (0.46 gegen 0.77), Capture-Differenz negativ, beide Blöcke negativ in der gepaarten Differenz, ein Trade trägt 52 Prozent des Bruttogewinns, Netto K1 negativ. Fast-Fail-Bedingung erfüllt (ΔR und ΔMFE nicht positiv). Die eingefrorene Y1-Spezifikation ist beendet. Die Mechanik «Failed Breakdown» ist damit nicht widerlegt, aber diese Umsetzung (Kontext, TA, Stop unter dem Sweep-Tief, Chandelier 3 ATR14) hat auf BTC keine Evidenz und ist schlechter als der Kontext allein.

**Y2: inconclusive, insufficient sample.** Erfüllt (a) ΔR positiv, 100 Prozent positive Ziehungen, (b) MFE-Median über den Kontrollen und Capture-Differenz positiv, (c) gleiche Richtung in beiden Blöcken. Verfehlt (d) Konzentration 85 Prozent auf einen Trade und (e) Netto K1 negativ. Nicht Fast Fail, nicht Fast Promote. Der Effekt ist ein Verlust-Reduktions-Effekt, kein Gewinn-Effekt, und er ist teilweise ein Artefakt der R-Definition: Y2-Stops sind 4.75 ATR weit, Kontroll-Stops rund 2 ATR, in ATR gemessen verliert Y2 1.41 je Trade gegen 1.69 der Kontrollen. Der stärkste Einzelbefund bei Y2 ist struktureller Art: 50 Prozent der Y2-Signale erreichen innerhalb 60 Tagen ein neues 20-Tage-Hoch mit 71 Prozent Persistenz, gegen 1 von 7 Kontrollen. Der Doppelboden mit Nackenlinienbruch identifiziert also überdurchschnittlich oft einen echten Boden, aber der Einstieg liegt 5 ATR über dem Tief, und der Chandelier-Exit mit 3 ATR14 (Median-Haltedauer 15 Kerzen, also 2.5 Tage) beendet die Position, bevor der Trend läuft. Das ist keine Aussage, die eine Parameteränderung rechtfertigt, sondern eine Hypothese für Stufe B und für die Exit-Frage.

**Y3: inconclusive, insufficient sample.** Sechs Signale, ein Kontrollpaar. Fünf Fehlsignale und ein grosser Gewinner, der zugleich Y1-Signal ist. Nicht auswertbar.

Präzisierung der Auswertungsregeln nach dem Lauf, transparent: Die Fast-Fail- und MP-Regeln setzen gepaarte Bootstrap-Werte voraus. Bei Y3 gab es ein einziges Paar, der Bootstrap lieferte keinen Mittelwert, und die Fast-Fail-Bedingung «ΔR nicht positiv» wäre durch den fehlenden Wert erfüllt worden. Deshalb wurde nach dem ersten Auswertungsdurchlauf die Vorbedingung «mindestens 5 Paare für jede Statuszuweisung ausser inconclusive» eingefügt. Das ändert kein Ergebnis von Y1 (8 Paare) oder Y2 (6 Paare), nur die Zuordnung von Y3 von einem technisch bedingten Fast Fail zu inconclusive. Diese Korrektur ist im Code kommentiert und hier ausgewiesen.

## 4. Was der Lauf über die Konstruktion sagt

Die Basisrate ist negativ. Kontextkerzen nach 12 Prozent Rückgang mit TA-Bestätigung und E-U-Exit verlieren, in allen drei Kontrollgruppen. Das deckt sich mit Stufe 2 (tägliche Mean Reversion auf BTC schwach) und ist der Referenzpunkt für jede Bottom-Hypothese: Sie muss nicht nur profitabel sein, sondern eine negative Basisrate überwinden.

Der Chandelier 3 ATR14 auf 4h ist ein kurzer Exit. Median-Haltedauer 12 bis 15 Kerzen, Giveback 0.5 bis 1.2 R, Exit Efficiency 0.3 bis 0.5, und bei Y2 erreichen die Hälfte der Signale nach dem Exit ein neues 20-Tage-Hoch. Die Hold Engine hält nicht lange genug, um die Trends zu fangen, die die Bottom Engine erkennt. Das ist eine Beobachtung, keine Optimierung: Der Exit wurde als einheitliche Baseline gesetzt, und er ist für 4h-Reversal mit mehrwöchigem Trendziel offenbar zu eng. Die Frage «Chandelier allein gegen Chandelier plus Strukturbruch» ist damit die weniger wichtige, die Frage nach der Zeitebene des Exits (ATR-Länge, Referenz auf Tageskerzen) die wichtigere. Beides ist Stufe-B-Material mit eigener Vorregistrierung.

Die TA-Bestätigung filtert nicht zugunsten der Signale. Y1 mit TA ist schlechter als Kontext mit TA. Bei Y1 liegt der Einstieg zur Eröffnung nach der Bestätigung im Median 2.9 ATR über dem ex-post Tief, bei Y2 5.0 ATR. Die Kosten der Bestätigung sind im Preis sichtbar, der Nutzen nicht. Das ist die Kernfrage von Stufe B (H3).

Follow-through: Nach dem Einstieg fällt der Preis in allen drei Gruppen im Mittel (Y1 minus 0.9 ATR nach 6 Kerzen, Y3 minus 3.2 ATR), Taker-Imbalance nach Einstieg um null, Volumen-z leicht positiv. Absorption (aggressives Kaufen ohne Fortschritt) trat in keinem Signal auf. Die Nachfrage nach dem bestätigten Boden ist im Mittel nicht vorhanden.

Konzentration: In allen drei Hypothesen trägt ein Trade den Bruttogewinn (Y1 2019, Y2 2020, Y3 2019, derselbe Trade wie Y1). Ohne diese Trades sind alle Reihen klar negativ. Das ist die Signatur einer Konstruktion, die gelegentlich einen Trend fängt und sonst Stops sammelt, wie MTP, mit schlechterer Bilanz.

## 5. Konsequenzen nach Protokoll

Y1 v1.1 ist beendet (Fast Fail). Y2 und Y3 sind inconclusive, keine Parametervariante, keine Validation. Keine Hypothese geht in die Validation. Der Overlap-Bericht mit BTC-RTC folgt, sobald die RTC-Library steht, er ändert nichts an diesem Urteil.

Hypothesen für Stufe B (eigene Vorregistrierung, aus diesem Lauf abgeleitet, deshalb Ebene C, nur auf anderen Daten oder mit neuen Mechanismen prüfbar): Erstens die Trigger-Frage H3 (T0 ohne Bestätigung, TA, TB Reclaim) mit Einstiegskosten in ATR als Hauptmetrik. Zweitens die Exit-Zeitebene: Chandelier auf Tages-ATR oder ATR mit längerem Fenster als Hold für 4h-Einstiege, gegen E-U. Drittens Y2 als Boden-Identifikator (50 Prozent neue Hochs) getrennt von Y2 als Trade. Viertens: Die identische Spezifikation läuft auf XRP und DOT, dort mit eigener Basisrate, und erst ein Coin-übergreifend gleiches Bild trägt.

Produktionsvermerk (Bericht): Y1 2 bis 3 Trades je Jahr, Y2 2, Y3 1, Turnover minimal, alle Ausführungen Taker (Eröffnung, Stop), Haltedauer Median unter drei Tagen, maximal 52 Kerzen, Daten OHLCV 4h, Latenz Kerzenschluss, Kraken Spot, kein Funding, Komplexität niedrig. Operativ wäre jede der drei handelbar, keine ist es wert.

## 6. Dateien

`stufeA/eval_stufeA.py` (SHA 60efb294…), `stufeA/data/eval_stufeA.json`, `stufeA/data/trades_Y1_K1.csv`, `trades_Y2_K1.csv`, `trades_Y3_K1.csv`, `controls_Y*_K1.csv`, `pairs_Y*.csv`, `yamato_stufeA_auswertungsregeln_v1.md`.
