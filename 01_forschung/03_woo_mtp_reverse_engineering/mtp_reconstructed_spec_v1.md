# MTP Reconstructed Specification v1

**Project Aurum II, 03_woo_mtp_reverse_engineering. Stand 16.09.2026. Grundlage: Stufe-1-Bericht und Stufe-2-Bericht (isolierte Varianten), sechzehn beobachtete BTC-Trades des öffentlichen Market-Trend-Pro-Backtesters, CoinMarketCap-Tagesdaten.**

Klassifikation je Bestandteil: **1 gesichert** (exakt reproduziert, keine Gegenbeobachtung), **2 stark indiziert** (Mehrheit der Fälle reproduziert, Rest durch bekannte Datenvorbehalte oder eine offene Nachbarfrage erklärbar), **3 noch nicht identifiziert** (Alternativen mit gleicher Trefferzahl, Entscheidung braucht Zusatzdaten). Die Spezifikation beschreibt die Mechanik, nicht den Edge. Nichts darin ist ein Urteil über Ertrag.

## 1. Daten und Zeitraster

| Nr | Bestandteil | Spezifikation | Klasse | Evidenz |
|---|---|---|---|---|
| 1.1 | Preisreihe | CoinMarketCap BTC/USD, Tageskerzen, UTC-Tag | 1 | Drei Ein-Leg-Einstiege exakt CMC-Close, alle Börsen 0.1 bis 7 Prozent daneben |
| 1.2 | Zeitraster | UTC-Tag, keine Verschiebung | 1 | Kein ±1-Tag-Muster in 13 exakt reproduzierten Trades |
| 1.3 | Historie vor 2017 | CMC-Fassung des Backtesters weicht von der heutigen ab | 2 | Trades 1 bis 3 mit 1.6 bis 5 Prozent Abweichung bei identischer Regel, alle späteren unter 0.1 Prozent |

## 2. Volatilitätsmass

| Nr | Bestandteil | Spezifikation | Klasse | Evidenz |
|---|---|---|---|---|
| 2.1 | ATR | True Range mit Wilder-Glättung, Periode 180 (RMA, alpha 1/180) auf CMC-OHLC | 1 | Acht Stop-Exits und fünf TP-Exits ab 2017 auf 0.08 Prozent, SMA- und EMA-Variante um 10 bis 60 Prozent daneben |
| 2.2 | Zeitpunkt | ATR wird am Tag des jeweiligen Legs eingefroren, nicht täglich neu | 1 | Trade 15: ATR am Exit-Tag hätte 1.5 Prozent Abweichung erzeugt |

## 3. Einstieg

| Nr | Bestandteil | Spezifikation | Klasse | Evidenz |
|---|---|---|---|---|
| 3.1 | Fill | Schlusskurs des Signaltages, kein Folge-Open | 1 | Drei Ein-Leg-Einstiege exakt |
| 3.2 | Filter | Schluss über SMA200 (einfach, 200 Tage, CMC-Close) am Signaltag, nur als Einstiegsbedingung | 1 für «nur Einstieg» (Trade 13 blieb unter SMA200 offen), 2 für die exakte Form (Signaltage mit Filter falsch: 2019-03-30, 2023-10-01, korrekt ausgeschlossen) |
| 3.3 | Niveau | Hoch eines Pivot-Tages (lokales Hoch, höher als die fünf Tage davor und der Tag danach), mindestens 20 und höchstens 365 Tage alt, seither nicht überschritten | 2 | 13 von 16 Entry-Tage exakt, Max Age 365 durch fehlende Legs Okt bis Dez 2020 belegt, Fenster-Maximum widerlegt |
| 3.4 | Auslöser | Tageshoch über dem Niveau, Schluss darf unter dem Niveau liegen | 2 | Trade 13 (Schluss unter Niveau) und Trade 16; «Schluss über Niveau» als Entry-Bedingung reduziert Treffer auf 7 von 16 |
| 3.5 | Verbrauch eines Niveaus | Offen: durch ein Tageshoch darüber (Basis, erklärt Trade 6, 14) oder erst durch einen Schluss darüber (Variante C2, erklärt Trade 7, 13) | 3 | Beide Varianten 12 bis 13 Entry-Treffer, disjunkte Fehler, Entscheidung über Leg-Termine Trade 13 |
| 3.6 | Pivot-Breite | Linkes Fenster 5 Tage passt am besten, 8 bis 10 fast gleich, 3 und 15 schlechter | 3 | Trade 8 verlangt schmal, Trade 14 verlangt breit, Konflikt unauflösbar ohne Leg-Termine |
| 3.7 | «Close Above Within 30» | Keine Funktion identifiziert, keine Beobachtung braucht sie | 3 | Frist-Deutungen verschlechtern die Treffer |

## 4. Stop

| Nr | Bestandteil | Spezifikation | Klasse | Evidenz |
|---|---|---|---|---|
| 4.1 | Initialer Stop | Schluss des Einstiegs minus 6.5 mal ATR(2.1) am Einstiegstag | 1 | Trades 4, 11, 15 auf 0.04 Prozent |
| 4.2 | Nach Add-on | Stop wird auf Schluss des neuen Legs minus 6.5 mal ATR am Leg-Tag gesetzt, gilt für die ganze Position | 1 | Trades 8, 10, 12, 13, 16 auf 0.005 Prozent |
| 4.3 | Trailing | Keines. Der Stop bewegt sich nur bei Add-ons | 1 | Trade 15 und alle Ein-Leg-Trades, jede Trailing-Variante um 2 bis 9 Prozent daneben |
| 4.4 | Ausführung | Intraday am Niveau, sobald das Tagestief das Niveau erreicht, bei Gap unter dem Niveau am Open | 1 für Niveau-Fill, 3 für Gap-Regel (kein Gap-Fall unter den 16 Trades) |
| 4.5 | Gesamtschliessung | Alle Legs werden zusammen geschlossen | 2 | Ein Exit je Trade in der Tabelle, Stop-Niveau des letzten Legs erklärt den Exit der Gesamtposition |

## 5. Ziel

| Nr | Bestandteil | Spezifikation | Klasse | Evidenz |
|---|---|---|---|---|
| 5.1 | Niveau | Schluss des ersten Legs plus 37.5 mal ATR am Einstiegstag, fix für den ganzen Trade, unabhängig von Add-ons | 1 | Trades 5, 6, 7, 9, 14 auf 0.08 Prozent, Trade 3 mit Datenvorbehalt |
| 5.2 | Ausführung | Intraday am Niveau, sobald das Tageshoch es erreicht | 1 | Sechs TP-Exits an Aufwärtstagen innerhalb der Spanne |
| 5.3 | Relevanz | Sechs von acht Gewinnern enden am Ziel, das Ziel ist der Hauptausstieg für Gewinner | 1 | Exit-Klassifikation aller 16 Trades |

## 6. Failed Breakout Exit

| Nr | Bestandteil | Spezifikation | Klasse | Evidenz |
|---|---|---|---|---|
| 6.1 | Funktion | Kein einziger der 16 Exits braucht den Mechanismus. Alle Exits sind Stop (10) oder Ziel (6) | 3 (Existenz unbelegt) | Mit den Defaults «Close Below Within OFF» ist der Mechanismus möglicherweise wirkungslos |

## 7. Pyramiding

| Nr | Bestandteil | Spezifikation | Klasse | Evidenz |
|---|---|---|---|---|
| 7.1 | Auslöser | Ein Add-on ist ein weiterer Pivot-Ausbruch nach 3.3 innerhalb des offenen Trades, mit Filter 3.2 | 2 | Alle sieben rekonstruierten Leg-Tage sind Pivot-Ausbrüche |
| 7.2 | Bestätigung | Schluss über dem Niveau am Leg-Tag («Must Close Above» für Legs) | 2 | Verbessert Legs von 8 auf 9 und Entries auf 13 von 16, entscheidet Trade 14 |
| 7.3 | Abstand | Schluss mindestens 1.5 ATR über dem Schluss des letzten Legs | 3 | Erklärt Trade 8, 10, 12 exakt, unterzählt lange Trades (2, 3, 13, 14, 16); ohne Abstand Überzählung |
| 7.4 | Anzahl | Keine Obergrenze beobachtet (bis 9 Legs) | 2 | «Max Pyramid 100» als Anzahl oder Prozent, beides verträglich |
| 7.5 | Grösse | Nicht gleich gross, nicht gleiche Dollarbeträge. Verträglich mit Einheiten proportional zu Portfolio-Equity geteilt durch ATR (Risiko-Sizing) | 3 | Trade 8 Verhältnis 1.01, Trade 10 Verhältnis 0.77, verlangt Equity-Änderung -0.3 und +7.3 Prozent, nur mit Mehr-Asset-Equity prüfbar |
| 7.6 | Legs nach TP-Niveau | Add-ons ändern das Ziel nicht (5.1) | 1 | Trade 7 und 9 |

## 8. Portfolio-Ebene

| Nr | Bestandteil | Spezifikation | Klasse | Evidenz |
|---|---|---|---|---|
| 8.1 | Sizing der Erstposition | Unbekannt. Vom Nutzer konfigurierbar [A] | 3 | Keine Beobachtung |
| 8.2 | Kapitalbindung, mehrere Assets | Unbekannt, beeinflusst 7.5 | 3 | Keine Beobachtung |

## 9. Kompakte Regelmenge (Basis-Variante der Vollsimulation)

Täglich, nach Schluss t auf CMC-Daten:

1. ATR_t = Wilder-RMA(180) der True Range. SMA_t = SMA(200) der Schlusskurse.
2. Niveau L_t = Hoch des jüngsten Pivot-Tages p mit t-365 ≤ p ≤ t-20, wobei Hoch(p) grösser ist als die Hochs der fünf Tage vor p und des Tages nach p und kein Tageshoch zwischen p+1 und t-1 über Hoch(p) lag. Kein solcher Tag: kein Niveau.
3. Ohne Position: Einstieg zum Schluss t, wenn Hoch_t > L_t und Schluss_t > SMA_t. Stop = Schluss_t − 6.5 ATR_t. Ziel = Schluss_t + 37.5 ATR_t (bleibt fix).
4. Mit Position: Add-on zum Schluss t, wenn Hoch_t > L_t, Schluss_t > L_t, Schluss_t > SMA_t und Schluss_t ≥ Schluss des letzten Legs + 1.5 ATR_t. Danach Stop = Schluss_t − 6.5 ATR_t für die ganze Position.
5. An jedem Tag t+1 mit Position: Tief ≤ Stop → Exit aller Legs am Stop (bei Open unter Stop am Open). Sonst Hoch ≥ Ziel → Exit aller Legs am Ziel.
6. Kein weiterer Ausstiegsgrund. SMA200 wirkt nur in 3 und 4.

Reproduktion dieser Regelmenge an den 16 Trades: Entry-Tag 13 von 16, Exit-Tag 13 von 16, Exit-Preis unter 0.1 Prozent 10 von 16 (unter 2 Prozent 13 von 16), Legs 9 von 16, ein zusätzlicher Trade (11.05.2019, Folge des fehlenden Trade 7).

## 10. Was diese Spezifikation nicht ist

Sie ist keine Aussage über den Ertrag. Sie ist auf BTC und auf den Zeitraum 2015 bis 2025 rekonstruiert. Die Bestandteile der Klasse 3 sind für die Validierungsstufe als eigene Annahmen auszuweisen, jede Wahl dort ist eine Entscheidung, keine Rekonstruktion. Stufe 2 von Aurum II hat eine andere Strategie getestet und ist kein Test dieser Spezifikation.
