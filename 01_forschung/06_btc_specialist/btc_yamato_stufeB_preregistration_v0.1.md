# BTC YAMATO RTC — Stufe B, Vorregistrierung, Version 0.1 (Entwurf)

**Project Aurum II, `01_forschung/06_btc_specialist/`. 17.09.2026, nach dem Stufe-A-Bericht (Y1 Fast Fail, Y2 und Y3 inconclusive). Status: Entwurf zur Prüfung, kein Freeze, kein Lauf. Stufe B ist eine neue Vorregistrierung mit neuen Hypothesen, keine Reparatur von Stufe A. Alle Zahlen von Stufe A bleiben eingefroren und werden hier nicht verändert, Stufe B verwendet dieselben Kandidatendefinitionen (Y1, Y2, Y3 als Kandidatenquellen, nicht als Strategien) und stellt zwei Fragen, die Stufe A aufgeworfen hat.**

## 0. Kernfrage

Wie viel Qualität bringt die Bestätigung, und wie viel Trend Capture kostet sie? Und, aus Stufe A hinzugekommen: Ist der Exit-Horizont das Problem? Stufe A hat gezeigt, dass Y2-Böden in 50 Prozent der Fälle innerhalb 60 Tagen ein neues 20-Tage-Hoch erreichen, die Positionen aber nach im Median 15 Kerzen am Chandelier 3 ATR14 enden, und dass der Einstieg nach TA bei Y1 im Median 2.9 ATR, bei Y2 5 ATR über dem ex-post Tief liegt.

Vorbelastung, offen: Diese Hypothesen sind aus dem Stufe-A-Lauf abgeleitet (Ebene C). Sie sind auf denselben Kandidaten prüfbar, weil sie andere Regeln (Trigger, Exit) auf dieselben Ereignisse anwenden, aber jedes Ergebnis von Stufe B trägt den Vermerk «auf Discovery-Daten nach Kenntnis von Stufe A entwickelt» und muss die Validation auf dem Holdout ab 2024 bestehen, bevor es zählt. Trial-Zahl: Stufe A 3 plus Stufe B nach Abschnitt 3.

## 1. Trigger-Familie (H3), drei Trigger, keine weitere Suche

Auf allen Y1- und Y3-Kandidaten (Y2 hat die Bestätigung im Muster, dort nur E-Vergleich): T0 ohne zusätzliche Bestätigung (Einstieg Eröffnung t+1), TA (Schluss der Folgekerze über dem Kandidatenhoch, Einstieg t+2, Stufe-A-Regel), TB (Reclaim des strukturellen Niveaus, Schluss über dem Niveau des Failed Breakdown innerhalb der nächsten sechs Kerzen, Einstieg zur Eröffnung danach). Stop und Sizing wie Stufe A. Gepaart auf denselben Kandidaten: Anzahl gehandelt, Einstiegspreis relativ zum Kandidatenschluss und zum ex-post Tief in ATR, R netto, MFE, Capture Ratio, Fehlsignalquote, verfallene Kandidaten als Kosten. Hauptmetrik: Erwartung je Kandidat (nicht je Trade), damit verfallene Kandidaten den Trigger belasten.

## 2. Exit-Familie, zwei Alternativen zur Baseline E-U

E-U (Stufe A, Chandelier 3 ATR14 plus Strukturbruch) gegen E-D (Chandelier 3 ATR auf Tageskerzen-ATR14, Strukturbruch auf bestätigten Tages-Swing-Lows, alles sonst gleich) gegen E-W (Chandelier 3 ATR14 auf 4h, aber Referenz ist das 20-Tage-Hoch: Floor wird erst aktiv, nachdem der Schluss das Vor-Einstiegs-Hoch überschritten hat, davor gilt nur der initiale Stop). Gepaart auf denselben Einstiegen (Trigger nach Stufe A, also TA beziehungsweise Nackenlinienbruch): Erwartung, Capture Ratio, Giveback, Haltedauer, Anteil abgeschnittener Trends (Trade endet, danach neues 20-Tage-Hoch innerhalb 60 Tagen). Keine k-Suche: k bleibt 3 in allen drei.

## 3. Tests und Multiplizität

Familie Trigger (Holm über vier): T0 gegen TA und TB gegen TA je auf Y1 und Y3, gepaart, Erwartung je Kandidat. Familie Exit (Holm über sechs): E-D gegen E-U und E-W gegen E-U je auf Y1, Y2, Y3, gepaart, Erwartung je Trade und Capture. Interaktion Trigger mal Exit wird nicht getestet (Bericht der 3 mal 3 Matrix ohne Test, keine Auswahl daraus). Kontrollgruppe wie Stufe A für jede Konfiguration, damit die Basisrate sichtbar bleibt. Kriterium «Signal vorhanden» und die drei Discovery-Ebenen wie Auswertungsregeln v1. Mindestzahl 30, Stufung 20, bekannt ist, dass T0 mehr Trades liefert (96 Y1-Kandidaten) und damit als einzige Konfiguration die Mindestzahl erreichen kann.

## 4. Was Stufe B nicht darf

Keine Änderung der Kandidatendefinitionen, des Kontexts, der Stops, der Toleranzen. Keine weiteren Trigger oder Exits nach Sicht auf Ergebnisse. Keine Kombination «bester Trigger mal bester Exit» ohne eigene Validation. Kein Stufe-A-Parameter wird durch Stufe B ersetzt, Stufe A bleibt als Referenzzeile.

## 5. Erwartete Zahlen (aus Stufe-A-Zählungen, ohne Outcomes)

T0 auf Y1: bis 96 Kandidaten, abzüglich Positionsüberlappung rund 70 bis 85 Trades. T0 auf Y3: bis 29. TB: Reclaim innerhalb sechs Kerzen bei Failed Breakdowns ist häufig bereits in der Kandidatenkerze erfüllt (Schluss über dem Niveau ist Teil der Definition), TB unterscheidet sich von T0 deshalb nur um die Bedingung «Folgekerze schliesst nicht wieder darunter», erwartet 60 bis 80 Trades. Exit-Vergleiche auf den Stufe-A-Einstiegen: 16, 14, 6.

## 6. Offene Entscheidungen vor dem Freeze

1. TB-Definition (Reclaim innerhalb sechs Kerzen, Folgekerze nicht darunter) bestätigen.
2. E-D (Tages-ATR) und E-W (Floor erst nach neuem 20-Tage-Hoch) als die zwei Exit-Alternativen bestätigen, keine dritte.
3. Erwartung je Kandidat als Hauptmetrik der Trigger-Familie bestätigen.
4. Ob Stufe B auf BTC allein läuft oder gleichzeitig mit XRP und DOT (Empfehlung: gleichzeitig, mit coin-spezifischer Auswertung und ohne Pooling).
