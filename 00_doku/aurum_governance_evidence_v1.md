# AURUM II — Governance und Evidenzklassen, Version 1

**Project Aurum II, `00_doku/aurum_governance_evidence_v1.md`. 17.09.2026, vor den nächsten Outcome-Läufen. Gilt für alle künftigen Läufe in allen Lanes. Ändert kein eingefrorenes Ergebnis: Stufe 1, Stufe 2, MTP-Validierung (VERWORFEN) und BTC YAMATO Stufe A v1.1 (Y1 not supported und Fast Fail, Y2 und Y3 inconclusive) bleiben mit ihrem Status nach Auswertungsregeln v1 bestehen und werden nicht rückwirkend umetikettiert.**

## 1. BTC ist Development-Markt

BTC ist der Markt, auf dem das RTC-Framework, die Feature Library, die Kontrollgruppenmethode, die Auswertungsregeln und die Stufe-A-Spezifikation entwickelt und zum ersten Mal durchgerechnet wurden. Alle Lehren aus dem Stufe-A-Lauf (T0 statt TA, längerer Exit-Horizont, negative Basisrate der Kontrollen) sind auf BTC-Discovery-Daten nach Sicht auf BTC-Outcomes entstanden. Deshalb gilt: Kein weiterer BTC-Lauf auf Discovery-Daten bis 2023 kann die Trigger-Familie T0/TA/TB oder die Exit-Familie E-U/E-D/E-W unabhängig bestätigen. BTC Stufe B liefert Development-Evidenz, mehr nicht. Ein positives Stufe-B-Ergebnis ist eine Begründung für einen Validation-Lauf auf dem BTC-Holdout ab 2024, nicht für einen Sleeve.

Die ersten unabhängigen Generalisierungstests der aus BTC abgeleiteten Regeln sind XRP-RTC Stufe A und DOT-RTC Stufe A, unter zwei Bedingungen: Ihre Spezifikation (v1.0) wird eingefroren, bevor XRP- oder DOT-Outcomes berechnet werden, und die Zahlen des BTC-Parameterpakets v1.1 werden nicht coin-spezifisch angepasst. Beides ist in XRP v0.4 und DOT v0.4 bereits so vorgesehen. Ein Ergebnis auf XRP oder DOT zählt als «Independent discovery», weil die Regeln nicht auf XRP- oder DOT-Daten entwickelt wurden. Es zählt trotzdem nicht als Validation, weil auch XRP und DOT Discovery-Daten bis 2023 verwenden.

ETH und SOL folgen derselben Logik, sobald ihre Vorregistrierung eingefroren ist. Sollte eine Regel nach den XRP- und DOT-Läufen verändert werden, wären XRP und DOT damit ebenfalls Development-Märkte für diese veränderte Regel, und der nächste unberührte Coin (ETH oder SOL) würde zum unabhängigen Test.

## 2. Outcome-informed Varianten

Folgende Konfigurationen sind aus dem Stufe-A-Lauf abgeleitet und tragen dauerhaft den Vermerk «outcome-informed, Ebene C» in jedem Bericht und in jeder Roadmap-Zeile: Y2 mit neuem Exit (E-D oder E-W auf denselben Nackenlinien-Einstiegen), Y3 mit T0 (Einstieg ohne Bestätigungskerze), Y1 mit T0 oder TB, und allgemein die Trigger-Familie T0/TA/TB sowie die Exit-Familie E-D/E-W, soweit sie auf BTC laufen. Sie sind neue Discovery-Hypothesen, keine Reparaturen und keine Fortsetzungen von Stufe A.

Deckel: Ein positives Ergebnis einer outcome-informed Variante auf denselben BTC-Discovery-Daten rechtfertigt höchstens einen Validation-Lauf auf dem BTC-Holdout. Es begründet keinen Sleeve, keine Produktion und keinen Cross-Coin-Test. Ein negatives Ergebnis schliesst die Variante auf BTC ab. Die Statusebenen aus Abschnitt 3 gelten, die Evidenzklasse bleibt «Development» (Abschnitt 5). Läuft dieselbe Variante auf XRP oder DOT mit eingefrorener Spezifikation vor deren Outcomes, gilt sie dort als «Independent discovery».

## 3. «Mechanistically promising», Regel v2, ex ante

Für alle Läufe ab dem Datum dieses Dokuments (BTC Stufe B, XRP-RTC, DOT-RTC, BTC-B, XRP-B, DOT-A, DOT-C, ETH, SOL, Lane C und Lane D) gilt statt der Fünf-Bedingungen-Regel aus Auswertungsregeln v1 folgende operationale Definition. Sie wird hier festgelegt, bevor Outcomes dieser Läufe existieren, und wird nachträglich nicht geändert. Ein Sleeve erhält den Status «mechanistically promising», wenn mindestens drei der vier folgenden Kriterien erfüllt sind und der Status «formal supported» nicht erreicht ist.

Kriterium 1, Kontrolle: Der Median der gepaarten Differenz ΔR (Signal minus gematchte Kontrolle, Kosten K1) liegt in der erwarteten Richtung, und der Anteil positiver Paare beträgt mindestens 0.60. Für Exit- und Trigger-Vergleiche innerhalb einer Familie tritt an die Stelle der Kontrolle die vorregistrierte Baseline (E-U beziehungsweise TA), die Erwartung je Kandidat ersetzt ΔR bei Trigger-Vergleichen.

Kriterium 2, Verschiebung: Mindestens eine der drei vorregistrierten Verlaufsmetriken zeigt eine relevante Verschiebung gegenüber den Kontrollen oder der Baseline: MFE-Median um mindestens 0.5 R höher, Capture-Ratio-Median um mindestens 0.10 höher, oder die Verteilung der Outcome-Klassen (trend, delayed_trend, rebound, fail) hat einen um mindestens 15 Prozentpunkte höheren Anteil trend plus delayed_trend. Die Schwellen sind absichtlich grob, sie trennen «etwas ist da» von Rauschen, mehr nicht.

Kriterium 3, keine Einzeltrade-Dominanz: Der grösste Einzelbeitrag zur Summe der gepaarten ΔR beträgt höchstens 40 Prozent, und das Vorzeichen des Medians bleibt nach Entfernen des besten Paars erhalten.

Kriterium 4, zeitliche Konsistenz: Die Richtung des Medians ΔR ist in mindestens zwei vorregistrierten Zeitblöcken mit je mindestens fünf Paaren gleich. Hat ein Coin nur zwei gewertete Blöcke, müssen beide dieselbe Richtung zeigen.

Zusätzliche Bedingungen, unverändert aus v1: Mindestens fünf Paare für jede Statuszuweisung ausser inconclusive. Fast Fail bleibt: Median ΔR negativ mit Anteil positiver Paare unter 0.40 bei mindestens 10 Paaren beendet die Spezifikation. Fast Promote bleibt: «formal supported» (alle fünf Bedingungen v1 erfüllt) erlaubt Validation, nicht Produktion. «Mechanistically promising» nach v2 erlaubt Validation nur, wenn das Sleeve mindestens 20 Trades hat, sonst bleibt es als Befund stehen und wird auf dem nächsten Coin oder im Forward-Fenster erneut geprüft. Netto K1 muss für Validation nicht positiv sein, wohl aber für «formal supported».

Status von Stufe A bleibt v1: Y1 wurde nach v1 als not supported und Fast Fail geführt, Y2 und Y3 als inconclusive. Eine Neubewertung nach v2 findet nicht statt, auch nicht als Bericht, damit keine zweite Statustabelle mit anderer Regel neben der eingefrorenen entsteht.

## 4. Physische Trennung der Validation-Holdouts

Ab sofort existieren je Coin und Datenreihe zwei getrennte Dateien in `02_daten/holdout/`: `discovery/<SYM>_<reihe>_discovery.csv` mit letzter Kerze 2023-12-31 20:00 UTC und `validation/<SYM>_<reihe>_validation.csv` mit erster Kerze 2024-01-01 00:00 UTC, für BTC, XRP, DOT, ETH und SOL, je für Binance Spot 4h, Binance Perp 4h und die Flow-Library-Ausgabe 4h. Beide Prüfsummen und die Prüfsumme der Quelldatei stehen in `holdout_manifest_v1.json`. Die BTC-Spot-Discovery-Datei ist byteidentisch mit der bereits eingefrorenen Stufe-A-Datei (SHA 2d394fd1…), damit bleibt der Stufe-A-Lauf reproduzierbar.

Codeschutz: `ylib.load` und `dlib._load` verweigern jede Datei, deren Name «validation» enthält, mit einem Fehler, solange die Umgebungsvariable `AURUM_VALIDATION` nicht auf 1 steht. Discovery-Skripte setzen diese Variable nie. Ein Validation-Lauf ist ein eigenes Skript mit eigener Vorregistrierung, das die Variable ausdrücklich setzt und dies im Protokoll ausweist. Die Regel «Discovery-Code lädt keine Validation-Datei» ist damit technisch erzwungen, nicht nur vereinbart. Die 1h-Reihen und Kraken-Reihen werden bei ihrer ersten Verwendung in einem Lauf nach demselben Muster getrennt, die Grenze bleibt 2023-12-31.

Bekannte Schwäche, ausgewiesen: Die Validation-Dateien werden aus denselben Rohdaten erzeugt wie die Discovery-Dateien, und die Rohdaten liegen weiter in `raw/`. Die Trennung schützt vor versehentlicher Nutzung, nicht vor absichtlicher. Ein zweiter Schutz ist der Freeze der Validation-Vorregistrierung mit Prüfsumme vor dem ersten Lesen der Validation-Datei.

## 5. Evidenzklassen

Jede Roadmap-Zeile führt ab Version 1.1 das Feld «Evidence class» mit genau einem der folgenden Werte. Der Wert steigt nur durch einen eigenen, vorher eingefrorenen Lauf.

Development: Regel wurde auf diesem Markt entwickelt oder nach Sicht auf Outcomes dieses Marktes verändert. Alle BTC-Ergebnisse aus Stufe A und Stufe B. Höchste Folge: Validation-Lauf auf dem eigenen Holdout.

Independent discovery: Regel wurde vor dem Lauf eingefroren und nicht auf diesem Markt entwickelt, Daten bis 2023. XRP-RTC und DOT-RTC bei Freeze vor Outcomes. Höchste Folge: Validation-Lauf.

Holdout validation: Regel hat auf den Daten ab 2024 mit Kraken-Ausführung und Kostenstress die neun vorregistrierten Validation-Kriterien bestanden. Höchste Folge: Forward-Fenster.

Forward validation: Regel wurde vor einem Zeitfenster eingefroren und hat in diesem Fenster ohne jede Änderung bestanden. Für MTP v1 die einzige mögliche Klasse, weil kein unberührtes Fenster mehr existiert.

Production eligible: Holdout validation bestanden, Forward-Fenster von mindestens sechs Monaten bestanden, Produktionsvermerk vollständig, Kapitalrahmen und Betriebsort entschieden. Heute erfüllt das kein Sleeve.

## 6. Priorität Visual AI

Rendering, Prompt v0.1 und Manifest bleiben vorbereitet und eingefroren. Visual AI wird erst nach den drei Discovery-Läufen (BTC Stufe B, XRP, DOT) und nach dem Lane-C-Datenbefund angegangen, und nur als Inkrement auf einer Signalliste, deren Basisergebnis bereits vorliegt. Sie erhält keine eigene Roadmap-Woche mehr.
