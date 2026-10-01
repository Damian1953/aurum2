# Review Claude zu XS21 PiT v1.0, übermittelt von Damian 2026-10-01

(Von Damian am 01.10.2026 um 15:35 Zürich in den Chat kopiert, hier wörtlich abgelegt.)

---

Ich habe den XS21-Bericht gelesen. Das Urteil steht: Es gibt keinen Sleeve. Methodisch ist der Lauf sauber: ein Lauf, eingefroren, ohne Codeänderung nach dem Freeze, und die Abweichungen sind offen ausgewiesen. In drei Punkten ist das Ergebnis aber schwächer, als die Kennzahlen auf den ersten Blick zeigen.

1. Die Signifikanz hängt an einer Rechenkonvention, die man so nicht handeln kann (A9).
CAGR, Sharpe, MaxDD, Alpha und Holm-p beruhen auf der Tageskonvention. Dabei wird jede Position täglich kostenlos auf 1/6 zurückgeführt. Bei extremen Coins weicht das stark vom tatsächlich handelbaren Buy-and-Hold über die Haltedauer ab:

- U1 2026: +2.27 nach Tageskonvention, aber −0.14 aus den Trades
- U2 2025: +0.50 nach Tageskonvention, aber −0.67 aus den Trades

Auf Trade-Ebene ist der Bootstrap-p5 der Erwartung in beiden Universen negativ (−0.11 % und −0.15 %). Das handelbare Ergebnis ist also statistisch nicht von null unterscheidbar. Die Holm-p von 0.042 gilt nur für die idealisierte Rechnung. Das wiegt für mich schwerer als das c6-Scheitern.

2. Der Ertrag stammt vor allem aus dem verbrauchten Jahr 2026.
Rechnet man nur bis Ende 2025, bleiben 10.5 % bzw. 13.2 % CAGR bei Sharpe 0.56 und 0.52, mit Drawdowns von −80 % und −76 %. Den Rest tragen einzelne Squeeze- und Delisting-Ereignisse (ALPACA +520 %) und das Funding auf Gewinner-Coins. Auf einem Privatkonto ist genau das am schlechtesten ausführbar.

3. Die Survivorship ist entlastet, die Strategie nicht.
Der Bericht hält das korrekt fest: Die Strategie scheitert am Risiko, nicht an Survivorship. «H-C2 falsifiziert» ist die formal richtige Lesart nach der eingefrorenen Tabelle. Inhaltlich heisst das Ergebnis aber: Es gibt einen Effekt, er ist nicht handelbar, und der handelbare Teil ist nicht signifikant.

Zwei Punkte solltest du ausdrücklich zur Kenntnis nehmen, damit sie nicht später als Lücke auftauchen. Erstens: gesamt_ok: false im eingefrorenen Prüfskript. Das ist erklärt, weil U5a im Prüfskript fehlt und die K2-Reibung bei Delistings mitgerechnet wird. Zweitens: Die Survivorship-Zerlegung je Block (A6) wurde erst nach dem Lauf nachgetragen. Beides ändert am Urteil nichts. Und die Variante L42 mit 141 % CAGR und Sharpe 1.36 ist ein Vergleich, keine Auswahl. Sie darf nicht der Ausgangspunkt einer neuen Idee werden.

Was das für den Forward-Test heisst

Beide Berichte zusammen bestätigen die Bilanz: kein handelbarer Edge, Lane A geschlossen, XS21 kein Sleeve. Ich würde XS21 nicht in den Papierhandel aufnehmen. Dagegen sprechen drei Gründe: Die Strategie braucht Perps mit Short-Bein, D4 ist offen und das Gate B6 hat noch keine Schwellen. Bei einem Drawdown von −76 % würden einige Monate Forward-Daten am Urteil auch nichts ändern. Höchstens würde ich U2 als reine Schattenrechnung aus öffentlichen Binance-Daten mitführen, ohne Orders, auf Trade-Basis gerechnet und ohne Entscheidgewicht vor 12 Monaten.

Der Papierhandel besteht damit aus W2, W6 und Turtle 55/20, Spot-Long auf Kraken, mit Kosten K1 und einer Vorregistrierung vor dem Start. Für den Entwurf fehlen mir weiterhin D3 (Stunden pro Woche und Datum des Reviews) und D1 (wo der Runner läuft). Soll ich diese Einschätzung als Review-Dokument zu den bestehenden Berichten ins Projekt legen?
