# Visual AI als unabhängige Second Opinion — Plan, Version 0.1

**Project Aurum II, `01_forschung/00_gemeinsam/`. 17.09.2026. Status: Plan für eine spätere Stufe. Kein Modellaufruf, kein Rechenlauf. Das regelbasierte System bleibt für Forschung, Validierung und Ausführung massgebend.**

## 0. Architekturentscheidung

Aurum II führt zwei unabhängige Analysepfade. Der regelbasierte Pfad (Feature Library, RTC-Engines, Breakout-Familien) ist die Primary Engine: deterministisch, bei identischen Daten identisches Signal, vollständig backtestbar und auditierbar. Der Visual-AI-Pfad bewertet gerenderte Candlestick-Charts direkt mit einem multimodalen Modell und liefert Wahrscheinlichkeiten. Er erzeugt kein Signal und überschreibt keines. Er ist eine vollständig unabhängige Second Opinion, deren einziger Zweck in dieser Stufe die Messung eines inkrementellen Informationswerts ist.

Die Forschungsfrage lautet: Hat ein regelbasiertes Signal mit unabhängiger Visual-AI-Zustimmung eine andere bedingte Erwartung als dasselbe Signal mit Visual-AI-Ablehnung? Und getrennt: Enthält die Visual-AI-Bewertung Information, die nicht bereits in den deterministischen Merkmalen steckt?

## 1. Stand der Evidenz, ehrlich

Die Vorgabe nennt eine 2026 veröffentlichte Studie, nach der multimodale Modelle aus Krypto-Candlestick-Charts prädiktive Signale extrahieren und in einem Top-100-Test bessere risikoadjustierte Resultate als technische Benchmarks erzielen. Diese Studie konnte am 17.09.2026 nicht eindeutig identifiziert werden. Gefunden wurden: Haggett (Stevens Institute, arXiv 2605.00875, November 2025), ein CNN-Vergleich auf BTC, ETH und SPY 2018 bis 2024, bei dem einfache CNNs auf rohen Candlestick-Bildern eine AUC von bis zu 0.89 erreichen, Charts ohne Indikatoren besser abschneiden als mit, BTC vorhersagbarer ist als ETH, und der ausdrücklich keine Kosten, keine Slippage und keine risikoadjustierten Erträge prüft, mit 500 Stichproben je Asset. Dazu ein Benchmark (arXiv 2604.12659, «Do VLMs Truly Read Candlesticks?»), nach dem Vision-Language-Modelle Candlesticks nur in anhaltenden Trends brauchbar bewerten und in den häufigeren Marktlagen schwach sind, mit ausgeprägten Vorhersage-Biases und schwacher Reaktion auf den im Prompt genannten Horizont. Und eine Evaluation von fünf LLMs auf technischer Analyse (arXiv 2607.15414) mit dokumentierten Fehlermodi (numerische Halluzination, Inkonsistenz in Seitwärtsphasen).

Konsequenz: Die Evidenz ist Hypothesengenerator, nicht Beleg. Die plausibelste Erwartung ist, dass ein VLM überwiegend das erkennt, was die Feature Library bereits misst (Trendrichtung, Extension, Wick-Grösse), und dass ein Zusatzwert, falls vorhanden, in der Gestalt-Wahrnehmung mehrerer Kerzen liegt, die eine Regelbibliothek nur mit vielen Einzeldefinitionen abdeckt. Genau das wird getestet, mit einer Redundanzprüfung (Abschnitt 5).

## 2. Was Visual AI liefern darf

Je Bewertungszeitpunkt fünf Zahlen zwischen 0 und 1, getrennt klassifiziert: Bottom/Reversal Confidence, Trend Continuation Confidence, Distribution/Peak Confidence, Failed-Breakdown/Breakout Confidence, Pattern Confidence, plus eine kurze Begründung als Text, die nur protokolliert und nicht ausgewertet wird. Keine Handelsempfehlung, kein Preisziel, keine Positionsgrösse.

## 3. Eingefrorene Bewertungsumgebung

Visual AI erhält ausdrücklich nicht die regelbasierten Merkmale als Text (keine Wick-Werte, keine z-Scores, keine Niveaus, keine Flags). Es erhält ausschliesslich einen vorab standardisierten Chart-Ausschnitt mit dem, was zum Entscheidungszeitpunkt sichtbar war. Nur so kann der Test unterscheiden, ob das Modell dieselben Merkmale visuell reproduziert (kein Zusatzwert) oder etwas anderes sieht.

Vor dem Test werden eingefroren und mit Prüfsumme protokolliert: Modell und exakte Versionskennung, Prompt (Wortlaut), Chartdarstellung (Rendering-Code), Lookback-Fenster, Bewertungszeitpunkte, Sampling-Parameter (Temperatur 0 oder feste Seeds, soweit die API es erlaubt), Anzahl Aufrufe je Zeitpunkt (ein Aufruf, keine Mehrheitsentscheidung, sofern nicht vorab anders festgelegt).

Chartdarstellung, standardisiert vor dem Freeze: identische Bildgrösse, identische Kerzenanzahl (120 Kerzen 4h, 20 Tage, bis einschliesslich der Bewertungskerze), identische Skalierungsregel (Preise auf den Schluss der Bewertungskerze normiert, Achse in Prozent, Achsenbereich ausschliesslich aus dem sichtbaren Fenster, nie aus späteren Hochs oder Tiefs), identische Farben, identische Zeitebene, OHLC-Kerzen und Volumenbalken, keine Indikatoren (Haggett: Indikatoren verschlechtern), keine Datumsachse, kein Coin-Name, kein Börsenname, kein zukünftiger Chartbereich, kein späterer Trade-Outcome, keine P&L-Markierungen, identischer Prompt, Modellversion festgehalten. Die Normalisierung des Preisbereichs ist Pflicht, damit das Modell Coins nicht an absoluten Preisen erkennt (ein Chart bei 0.5 ist XRP, einer bei 60000 ist BTC), und wird vor dem Freeze auf synthetischen Charts geprüft. Der Chart enthält damit nichts, was nicht am Schluss der Bewertungskerze bekannt war, und nichts, was dem Modell erlaubt, Coin oder Zeitpunkt aus seinem Trainingswissen zu erkennen.

Prompt: neutral, ohne Nennung eines Setups, das der Chart enthalten könnte, ohne Erwartungshinweis, mit fester Ausgabestruktur (JSON mit den fünf Zahlen). Der Prompt wird einmal formuliert und nicht nach Ergebnissen verändert. Ein Prompt-Test vor dem Freeze ist nur auf synthetischen Charts (zufällige Kerzen ohne Marktbezug) erlaubt, um die Ausgabestruktur zu prüfen, nie auf realen Charts.

## 4. Bewertungszeitpunkte und Kontrollgruppe

Bewertet werden alle RTC-Signalkerzen (Bottom-Engine, alle Ebenen), alle E2-Exit-Kerzen und alle Chandelier-Exit-Kerzen des Discovery-Laufs, und für jede Signalkerze zwei gematchte Kontrollkerzen: eine zufällige Kerze desselben Coins aus demselben Kalenderquartal, die keinen RTC-Kontext hat, und eine Kerze mit RTC-Kontext (K1 bis K3), aber ohne Reversal-Evidenz. Die Kontrollgruppe ist notwendig, weil ein Modell, das auf jedem Chart nach einem Selloff «Bottom» sagt, mit der Regel-Engine übereinstimmt, ohne Information zu liefern. Die Zeitpunkte werden vor dem ersten Modellaufruf als Liste mit Prüfsumme festgehalten. Es gibt keine nachträglichen Zeitpunkte.

## 5. Auswertung

**Drei Arme, zentraler Test.** Erstens «Regel ja, Visual AI ja»: RTC-Trades mit Zustimmung (Bottom Confidence ≥ 0.6, Schwelle vorab). Zweitens «Regel ja, Visual AI nein»: RTC-Trades mit Ablehnung (≤ 0.4), dazwischen «unentschieden». Test: gepaarte Differenz der Erwartung je Trade zwischen den ersten beiden Armen, Trade-Bootstrap, ein Test je Coin, Holm über Coins. Drittens «Visual AI ja ohne Regelsignal»: Kontrollkerzen mit RTC-Kontext, aber ohne Reversal-Evidenz, bei denen das Modell Bottom Confidence ≥ 0.6 ausgibt, ausgewertet mit derselben Hold-Engine als hypothetische Trades (nur Bericht, kein Handel), um zu sehen, ob das Modell Böden findet, die die Regeln nicht finden. Dasselbe Schema für Peak Confidence an E2-Kerzen (Giveback mit und ohne Zustimmung) und für Failed-Breakdown Confidence an FB-Kandidaten.

**Diskriminierung.** AUC der Bottom Probability für «Trade erreicht 2 R vor Stop» über Signal- und Kontrollkerzen, mit Bootstrap-Intervall. Kalibrierung (Reliability-Diagramm) als Bericht.

**Redundanzprüfung, entscheidend.** Regression der Visual-AI-Wahrscheinlichkeiten auf die deterministischen Merkmale derselben Kerze (`ext`, `dd120`, `lower_wick_atr`, `close_location`, `bull_count`, `volume_zscore`, `taker_imbalance`, `mom10`, `dist_support_atr`, `failed_breakdown`, `lw_x_vol`). Ist der Anteil erklärter Varianz hoch (vorab: R² ≥ 0.7) und verschwindet die bedingte Erwartungsdifferenz, wenn die Merkmale kontrolliert werden, ist Visual AI redundant. Nur ein Residual mit eigener Erwartungsdifferenz ist ein Zusatzwert.

**Konsistenz.** Wiederholte Bewertung derselben Charts (fünf Prozent Stichprobe, zweiter Aufruf) zur Messung der Stabilität. Instabile Ausgaben (Abweichung über 0.2) entwerten die Bewertung dieses Zeitpunkts.

## 6. Vorkehrungen gegen Look-ahead, Prompt-Overfitting und Selection Bias

Look-ahead: kein Chart enthält Kerzen nach dem Bewertungszeitpunkt, keine Achsenbereiche aus der Zukunft, kein Datum, kein absoluter Preis, keine Trade-Ergebnisse im Prompt oder im Bild. Das Modell selbst hat Trainingswissen über die Marktgeschichte. Die Normierung und die Anonymisierung machen die Wiedererkennung eines konkreten Zeitpunkts unwahrscheinlich, aber nicht unmöglich (ein Modell könnte den März 2020 an der Form erkennen). Deshalb gilt jedes historische Ergebnis als obere Schranke, und die belastbare Prüfung ist das Forward-Fenster ab dem Freeze, in dem das Modell die Zukunft nicht kennen kann. Ein Teil des Tests wird deshalb auf dem Forward-Fenster wiederholt, bevor Visual AI in irgendeiner Form Vertrauen erhält.

Prompt-Overfitting: ein Prompt, vor dem Test eingefroren, nur auf synthetischen Charts erprobt, keine Iteration nach Ergebnissen, keine Prompt-Varianten im selben Lauf. Sollte eine zweite Prompt-Fassung je nötig sein, ist das ein neuer Test mit eigener Vorregistrierung und beide Fassungen zählen in der Trial-Zahl.

Selection Bias: ein Modell, eine Version, vorab gewählt nach Verfügbarkeit, Kosten und Reproduzierbarkeit, nie nach Trading-P&L. Alle Bewertungszeitpunkte vorab als Liste, Kontrollgruppen gematcht, keine nachträgliche Auswahl «interessanter» Charts, Holm über Coins, die Redundanzprüfung als Pflichtteil.

## 7. Was Visual AI nicht darf

Kein Signal erzeugen. Kein Signal überschreiben. Keine Orderentscheidung autonom überschreiben, bevor der Zusatzwert unabhängig validiert ist. Keine Positionsgrösse beeinflussen. Nicht in die Validation Stage eines Sleeves eingehen, solange der Forward-Test nicht bestanden ist. Nicht als Filter in einer Vorregistrierung erscheinen, bevor die bedingte Erwartungsdifferenz und die Redundanzprüfung auf Discovery und Forward positiv sind.

## 8. Voraussetzungen und Reihenfolge

Voraussetzung ist ein abgeschlossener Discovery-Lauf mindestens eines RTC-Strangs mit protokollierten Signalzeitpunkten. Vorher gibt es nichts zu bewerten. Reihenfolge: Feature Library und RTC einfrieren, Discovery rechnen, Zeitpunktliste mit Prüfsumme, Rendering-Code und Prompt einfrieren, Modellversion protokollieren, Aufrufe, Auswertung, Bericht. Kosten: rund 3 Aufrufe je Signal (Signal plus zwei Kontrollen) plus Exits, bei geschätzt 100 bis 300 Signalen je Coin und drei Coins eine niedrige vierstellige Zahl an Bildaufrufen, im Budget einer API ohne weiteres.

## 9. Offene Entscheidungen

1. Modellwahl nach Verfügbarkeit und Reproduzierbarkeit (Kandidaten: ein multimodales Modell mit fester Versionskennung und Temperatur 0), vorab.
2. Zustimmungs- und Ablehnungsschwellen 0.6 und 0.4 bestätigen.
3. Lookback 120 Kerzen bestätigen.
4. Ob das Forward-Fenster Pflicht vor jeder Verwendung ist (Empfehlung: ja).
5. Ob ein lokal betriebenes Modell (reproduzierbar, aber schwächer) dem API-Modell (stärker, aber versionsabhängig) vorgezogen wird.
