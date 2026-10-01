# Hypothesen nach Stufe 2, Version 2

**Project Aurum II, 16.09.2026. Dieses Dokument hält fest, was aus dem Stufe-2-Lauf als Hypothese folgt. Es ist keine Vorregistrierung, es eröffnet keine Variantenmatrix und es ändert nichts an den 37 finalen Urteilen. Es dient als Grundlage für die Planung der nächsten Stufe.**

## Grundsatz

Jede Hypothese unten ist aus den Stufe-2-Daten abgeleitet und deshalb auf denselben Daten nicht mehr prüfbar. Prüfbar ist sie nur auf Daten, die im Lauf nicht enthalten waren: ein anderes Universum (Point-in-Time), eine andere Börse (Kraken) oder eine Zeit, die noch nicht vergangen ist (Forward-Test). Das gilt auch für Hypothesen, die sich aus knappen Ergebnissen ergeben. Ein zweiter Lauf mit engerer Familie, anderem Drawdown-Mass oder gelockerter Coin-Mehrheit ist keine Prüfung, sondern Anpassung.

## Familie A, Woo-Matrix

**H-A1, Alpha der Ausbruchslogik Long.** Ausbruch über HH(N) mit nachgezogenem ATR-Stopp erzeugt gegen die exposure-gleiche Passivposition ein positives Alpha (Stufe 2: 10 bis 21 Prozent pro Jahr, t 1.7 bis 2.4, alle acht Ausbruchsvarianten). Status: Befund, kein Edge nach Kriterien. Prüfung: Forward-Test mit den eingefrorenen Regeln von W2 oder W6 auf Spot. Verwerfungsregel vorab festlegen, zum Beispiel Alpha-t unter 1.0 nach 24 Monaten oder MaxDD tiefer als der Stufe-2-Wert.

**H-A2, Drawdown-Profil.** Ausbruchs-Trendfolge hat auf Tagesdaten in Kryptowährungen systematisch tiefere Drawdowns als eine gleich-exponierte Passivposition (Stufe 2: c6 bei 15 von 15 Varianten verfehlt). Das ist eine Eigenschaft der Konstruktion, nicht des Zeitraums. Folgerung für die spätere Stufe mit kontinuierlicher Exposure-Steuerung: Dort ist der Drawdown das Ziel, nicht der Ertrag.

**H-A3, Stopp gegen Filter.** Der ATR-Stopp, nicht der SMA200-Filter, trägt den Effekt (W0 ohne Stopp kein Alpha, W2 gegen W8 praktisch gleich). Der Filter senkt nur das schlechteste Jahr. Status: Befund aus Paarvergleich, keine Prüfung nötig, Konsequenz für die Architektur: Der Filter ist eine Risikoschicht, keine Signalschicht.

**H-A4, Pyramiding als Risikoformung.** Gestaffelter Einstieg 0.50 plus 0.25 plus 0.25 senkt CAGR um rund drei Prozentpunkte, verbessert MaxDD, Calmar und Return je Exposure (W6 gegen W2, W7 gegen W4). Status: Befund, konsistent auf beiden Paaren. Konsequenz: Pyramiding gehört in die Risikoschicht, sein Nutzen wird an Drawdown gemessen, nicht an CAGR.

**H-A5, Coinabhängigkeit.** Der Alpha-Effekt ist auf LTC, DOT und LINK abwesend oder negativ, auf ADA, SOL, BNB, ETH stark. Status: Beobachtung ohne Erklärung. Keine Coin-Auswahl nach Ergebnis. Prüfbar nur im Point-in-Time-Universum oder Forward-Test mit vorher fixiertem Universum.

**H-A6, Short-Spiegelung.** Die auf die Short-Seite gespiegelte Ausbruchslogik hat keinen Edge (W2, W4, W8 Short alle negativ, kein Coin über Cash, keine Jitter-Region). Status: verworfen. Eine Short-Konstruktion in Aurum II, falls überhaupt, muss auf einer anderen Logik beruhen als der Spiegelung eines Long-Ausbruchs. Das ist keine Aufforderung, eine zu suchen.

**H-A7, Instrument.** Long-only-Trendfolge auf Perps zahlt 3 bis 6 Prozentpunkte CAGR pro Jahr Funding. Spot ist für die Long-Seite das bessere Instrument. Status: Befund aus der Spot-Referenz, Konsequenz für die Architektur: Long-Seite auf Spot, Perps nur dort, wo eine Short-Seite oder ein Carry-Bein sie verlangt.

## Familie B, Mean Reversion

**H-B1.** Mean Reversion auf Tagesdaten (z-Score 20, alle Jitter) hat in Kryptowährungen 2017 bis 2026 keinen Ertrag, Short-Seite zerstörerisch. Status: verworfen, keine weitere Prüfung vorgesehen.

## Familie C, Momentum

**H-C1, Time-Series-Momentum ist Beta.** TS21, TS63, TS126 Long-only sind Marktbeta mit halber Exposure, kein Alpha gegen EP. Status: verworfen als Edge. Konsequenz: Ein Momentum-Gate wäre in einer späteren Stufe eine Exposure-Steuerung, keine Signalquelle.

**H-C2, Cross-Sectional-Momentum, survivorship-konfundiert.** XS21 Long+Short besteht alle acht Kriterien (Sharpe 1.15, Alpha 46 Prozent, Beta null, alle Blöcke und Nachbarn positiv, K2 robust). Der Effekt ist nicht von der Survivorship des Zehn-Coin-Universums trennbar. Status: bestanden mit Vorbehalt, nicht handelbar. Prüfung: Point-in-Time-Universum mit allen Coins, die zum jeweiligen Stichtag auf Binance USDT-M oder Kraken handelbar waren, inklusive später delisteter. Universum und Regeln vor dem Lauf einfrieren. XS21 ist die einzige Konstruktion, bei der dieser Aufwand durch ein bestandenes Ergebnis begründet ist.

**H-C3, Short-Bein von XS21.** Short-only ist verworfen, aber im Long+Short-Portfolio senkt das Short-Bein MaxDD von -72 auf -37.5 Prozent und Beta von 0.64 auf null bei Sharpe 1.19 gegen 1.15. Das Short-Bein ist Absicherung, kein Ertrag. Status: Befund, relevant für die Konstruktion einer marktneutralen Variante, falls H-C2 im Point-in-Time-Universum besteht.

## Familie D, Carry, Funding, Open Interest

**H-D1, Cash-and-Carry ist eine Regime-Ernte.** D-CC besteht alle Kriterien auf Binance-Funding (Sharpe 4.95, MaxDD -1.7 Prozent), der Ertrag konzentriert sich auf 2020, 2021 und 2024. In Jahren mit Funding nahe null verdient die Konstruktion ungefähr Cash. Status: bestanden mit Datenvorbehalt. Prüfung: Kraken-Funding-Historie über mehrere Jahre beschaffen oder eine Entscheidung protokollieren, dass Binance-Funding als Näherung gilt. Zusätzlich vor jedem Paper-Betrieb: explizites Kapital- und Margin-Modell (Spot 1.0 plus Perp-Margin), Ausführung beider Beine, Basis-Risiko bei Liquidation, Kosten auf Kraken statt Binance-Sätzen.

**H-D2, Schalter-Empfindlichkeit.** Der CC-Schalter (ein bei f_7d ≥ 0.10, aus bei ≤ 0) reagiert auf kleine Unterschiede zwischen Börsen (BTC: 41 Prozent der Tage mit anderem Zustand auf Kraken). Die Jitter-Nachbarn (Schwellen 0.05 und 0.15, Fenster 3 und 14 Tage) sind alle positiv, was gegen eine Schwellenfragilität auf derselben Börse spricht. Status: offen. Prüfbar nur mit Kraken-Funding-Historie.

**H-D3, Funding-Contrarian.** FC Long-only ist nach Holm signifikant (p 0.006, Sharpe 0.99, MaxDD -11 Prozent) bei sieben Prozent Exposure, scheitert an Coin-Mehrheit (ETH negativ), c6 und c7. Status: verworfen. Das Signal «negatives Funding, long» trägt in der Summe, nicht je Coin. Keine Weiterverfolgung ohne neue Daten.

**H-D4, Open Interest.** Veränderung des Open Interest über sieben Tage in Kombination mit der Kursrichtung hat keinen Informationsgehalt auf Tagesdaten (Sharpe 0.03 bis 0.32, Holm-p 1.0, alle Seiten, beide Jitter). Status: verworfen. OI-Daten bleiben geladen, weitere OI-Hypothesen sind nicht vorgesehen.

## Fingerprint

**H-F1.** Die neun Fingerprint-Merkmale trennen die Varianten der Woo-Matrix nicht (fast alle «ähnlich»). Status: Instrument ungeeignet für die Frage «welche Variante ist Market Trend Pro». Die Frage wird nicht weiterverfolgt, weil ihre Beantwortung für den Edge ohne Bedeutung ist.

## Was daraus für die nächste Stufe folgt

Drei Arbeiten sind durch Ergebnisse begründet und in der Vorregistrierung angelegt: das Point-in-Time-Universum (für H-C2), die Kraken-Funding-Historie mit Kapitalmodell (für H-D1) und ein Forward-Test-Protokoll mit vorab festgelegter Verwerfungsregel (für H-A1). Jede dieser Arbeiten braucht ihre eigene kurze Vorregistrierung mit Prüfsumme vor dem Rechnen.

Nicht begründet sind: neue Varianten der Woo-Matrix, andere Stopp- oder Filterformen, Wochen- oder Stundendaten, andere Coins ohne Point-in-Time-Regel, jede Form von Kriterienanpassung.

Offen bleibt die kontinuierliche Exposure-Steuerung. Sie war für eine spätere Stufe vorgesehen. H-A2 und H-C1 geben ihr eine Richtung: Drawdown-Formung einer Long-Seite, die selbst schon Alpha zeigt, nicht Signalsuche.
