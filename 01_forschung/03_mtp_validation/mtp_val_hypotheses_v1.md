# Hypothesen nach der MTP-Validierung, Version 1

**Project Aurum II, 17.09.2026. Abgeleitet aus dem Volllauf der Validierungsstufe. Keine dieser Hypothesen ist auf denselben Daten prüfbar. Keine eröffnet eine Variantenmatrix. Das Urteil «verworfen» bleibt bestehen.**

## Grundsatz

Alles Folgende ist aus den Ergebnissen abgeleitet und deshalb Ebene C. Prüfbar sind die Hypothesen nur auf Daten, die im Lauf nicht enthalten waren (andere Assets mit Point-in-Time-Universum, andere Zeiträume, andere Börsen), oder durch Beobachtungen, die den Zusammenhang erklären, ohne Parameter zu verändern.

## Aus Ebene A

**H-V1, Zeitabhängigkeit.** Die Mechanik trägt auf Indexdaten bis 2021 (1.37 R je Trade bis 2020, 0.66 R 2021 bis 2023) und danach nicht mehr (0.08 R ab 2024, negative Jahre 2022, 2023, 2025, 2026). Zwei Erklärungen sind offen: ein Marktregime (Krypto-Bullenphasen 2017 und 2020/2021 mit anhaltenden Ausbrüchen über 365-Tage-Hochs) oder eine strukturelle Reifung (mehr Teilnehmer, engere Spreads, mehr Fehlausbrüche über alte Hochs). Beides ist nur durch Zeit prüfbar, nicht durch Rechnen. Konsequenz: Ein Forward-Test müsste eine Verwerfungsregel haben, die schon jetzt fast erfüllt wäre.

**H-V2, Beta statt Alpha.** Der Ertrag in A ist bei 2.9 Prozent mittlerer Exposure von dem einer konstanten Position gleicher Exposure nicht zu unterscheiden (Sharpe 1.31 gegen 1.34, Drawdown grösser). Das Alpha der Regression ist positiv und signifikant, entsteht aber aus dem Timing der Exposure in einem steigenden Markt, nicht aus einer Rendite je Risikoeinheit über dem Markt. Prüfbar durch einen Zeitraum, in dem der Markt insgesamt nicht steigt. Der ist mit 2022 bis 2026 zum Teil vorhanden, und dort ist die Mechanik bei null.

**H-V3, Konzentration mit Wiederholung.** Die Form der Verteilung (24 Prozent der Trades über 3 R, 76 Prozent am Stop, Top-10-Prozent tragen 56 Prozent) tritt auf sieben von neun Coins auf, sechs sind auch ohne ihren grössten Gewinner positiv. Die Eigenschaft «wenige grosse Gewinner» ist also nicht ein einzelner BTC-Trade, sondern wiederkehrend über Coins, aber nicht über Zeitblöcke. Das ist die präziseste Beschreibung dessen, was die Mechanik ist: ein Instrument, das in Bullenphasen auf vielen Coins gleichzeitig grosse Trends fängt und ausserhalb davon Stops sammelt.

## Aus Ebene B und B2

**H-V4, Ausführung ist zweitrangig.** Kosten, Slippage, Next-Bar-Open und Kraken-Fills kosten zusammen rund 0.05 R je Trade, der Übergang A nach B auf gepaarten Trades ist 0.86 ohne den einen Phantom-Stop. Das Ergebnis in B ist schwach, weil das B-Fenster in der Zeit liegt, in der A schwach ist, nicht weil Kraken schlechter füllt als der Index. Konsequenz: Für künftige Stränge ist die Ausführungsebene B ein solider, wenig verlustreicher Übergang, die Zeitachse ist die kritische Dimension.

**H-V5, Phantom-Stops sind selten, aber gross.** Ein einziger Phantom-Stop in acht Jahren, aber er kostete 5 R. Ein weiter Stop von 6.5 ATR wird auf Börsendaten fast nie von einem Wick erreicht, wenn der Index es nicht auch tut. Wenn doch, trifft es einen Trade, der sonst am Ziel geendet hätte, weil nur laufende Gewinner so lange offen sind. Die Asymmetrie ist strukturell: Phantom-Stops treffen bevorzugt die besten Trades.

**H-V6, Signale auf Börsendaten sind ein anderes System.** Mit Kraken-Kerzen als Signalquelle ist das Wilder-ATR 20 Prozent höher, Stops und Ziele liegen weiter, nur 34 Prozent der Trades sind identisch. Ein Betrieb ohne Index-Feed hätte ein System, das in dieser Stufe nicht getestet wurde und das in B2 bei 0.00 R liegt. Konsequenz: Jede spätere Umsetzung braucht entweder den Index-Feed (mit dem Risiko seiner Verfügbarkeit und Verzögerung) oder eine eigene Validierung auf Börsensignalen.

## Aus Sizing und Pyramiding

**H-V7, Pyramiding erhöht Notional vor Absicherung.** Der gemeinsame Stop liegt im Mittel erst nach dem vierten Add-on über dem Durchschnittseinstieg. Die meisten Trades enden vorher. Das Pyramiding erhöht deshalb bei der Mehrheit der Trades das Notional, ohne die älteren Legs abzusichern. Es ist im Ergebnis Positionsvergrösserung in laufende Trends, keine Risikoformung. Die Stufe-2-Beobachtung (Pyramiding senkt Drawdown bei Ratchet-Stop) gilt für die dortige Konstruktion, nicht für diese.

**H-V8, Portfolio-Sizing schlägt die Passivposition nicht.** Sicht 2 mit 29 Prozent Exposure erreicht 20 Prozent CAGR bei minus 44 Prozent Drawdown, die exposure-gleiche Passivposition 38 Prozent. Skalierung des Sizings verbessert das Verhältnis nicht, weil das Signal es nicht hergibt.

## Was daraus folgt

Kein Strang aus dieser Stufe. Der Forward-Test (Priorität 4) wird nicht gestartet. Die Prioritäten 2 (XS21 Point-in-Time) und 3 (D-CC Kraken) bleiben, ihre Vorbehalte sind andere. Die Arbeitshypothese «MTP enthält einen wirtschaftlich relevanten Trend-Following-Edge» ist nach dieser Stufe nicht haltbar für den Zeitraum ab 2022 und nicht vom Marktbeta trennbar davor. Sollte die Frage nach Trendfolge in Aurum II erneut gestellt werden, dann als Frage nach einer Exposure-Steuerung, die den in Stufe 2 und hier gleichermassen sichtbaren Effekt nutzt (Trendfolge fängt Bullenphasen), ohne auf Alpha je Trade zu setzen. Das wäre eine neue Vorregistrierung mit eigener Fragestellung, keine Variante dieser.

Nicht begründet: Parameteränderungen an Stop, Ziel, Pivot oder Abstand. Coin-Auswahl nach Ergebnis. Fensterwahl nach Ergebnis. Kombination mit Regimefiltern aus Stufe 1.
