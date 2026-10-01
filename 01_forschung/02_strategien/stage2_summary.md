# Stufe 2 — Fazit

**Project Aurum II. Rechenlauf vom 16.09.2026 auf der eingefrorenen Vorregistrierung Version 1.0 (SHA-256 8f576b7a…). Zehn Coins, vier Familien, 37 primäre Tests, 985 gerechnete Konfigurationen, 19 207 Trades. Szenario K1 (Taker plus Reibung, tatsächliches Funding) ist massgebend.**

## Ergebnis in einem Satz

Von 37 vorregistrierten Tests bestehen zwei alle acht Kriterien (D-CC Cash-and-Carry und XS21 Long+Short), einer besteht teilweise (XS21 Long-only), 34 werden verworfen. Beide bestandenen Konstruktionen tragen einen Vorbehalt, der in der Vorregistrierung schon angelegt war und der ihre Reichweite begrenzt: XS21 ist survivorship-behaftet, D-CC gilt für Binance-Funding und hat die Kraken-Gegenprobe nicht bestanden. Die Woo-Matrix zeigt auf der Long-Seite einen messbaren Alpha-Effekt, verfehlt aber die Kriterien Drawdown, Coin-Mehrheit und Holm-Korrektur. Sämtliche Short-Konstruktionen sind ohne Edge.

## Was die Daten zeigen

### Familie A, Woo-Matrix W0 bis W8

Alle acht Ausbruchs-Varianten Long-only (W1 bis W8) haben gegen die exposure-gleiche Passivposition ein positives Alpha von 10 bis 21 Prozent pro Jahr mit t-Werten zwischen 1.7 und 2.4, Sharpe 0.83 bis 1.04, Exposure nur 8 bis 26 Prozent. Der Alpha-Teiltest 13.3a ist bei allen bestanden. Das ist ein echter Befund: Die Ausbruchslogik mit nachgezogenem ATR-Stopp verdient je Einheit Marktrisiko mehr als das Halten des Marktes.

Trotzdem wird jede Variante verworfen, aus drei Gründen, die unabhängig voneinander greifen.

Erstens Kriterium c6: Der maximale Drawdown ist bei jeder Variante tiefer als bei der Passivposition mit gleicher durchschnittlicher Exposure (W2: -41 gegen -29 Prozent, W6: -31 gegen -24 Prozent). Trendfolge konzentriert die Exposure auf wenige Phasen und ist dann voll investiert, die Passivposition verteilt sie. Das Kriterium war so gesetzt und gilt.

Zweitens Kriterium c8: Die unkorrigierten Bootstrap-p-Werte liegen bei 0.004 bis 0.009, die Holm-korrigierten bei 0.052 bis 0.072. Bei fünfzehn Tests in der Familie reicht das nicht für die Fünf-Prozent-Grenze. Der Abstand ist klein, aber die Vorregistrierung kennt kein «knapp». Die Deflated Sharpe Ratio als Sensitivität liegt bei 0.52 bis 0.75, also ebenfalls unter der üblichen 0.95-Grenze.

Drittens Kriterium c1: Bei W2, W3, W5 und W8 ist die Mehrheit der geeigneten Coins nicht positiv. LTC, DOT und LINK sind bei fast allen Varianten negativ, ADA, SOL und BNB stark positiv. Der Edge ist coinabhängig. W1, W4, W6 und W7 bestehen c1, scheitern aber an c6 und c8.

Drei Paarvergleiche, die die Vorregistrierung vorsah: Der SMA200-Filter (W2 gegen W8) ändert am Ergebnis fast nichts, CAGR 32.4 gegen 33.3 Prozent, Sharpe 1.04 gegen 1.01, er senkt nur das schlechteste Jahr von -18 auf -12 Prozent. Pyramiding (W6 gegen W2) senkt den CAGR von 32.4 auf 29.2 Prozent bei gleichem Sharpe, verbessert aber MaxDD (-31 gegen -41 Prozent), Calmar (0.94 gegen 0.78) und Return je Exposure (180 gegen 162 Prozent). Pyramiding ist Risikoformung, kein zusätzlicher Ertrag. W0, die reine SMA-Kreuzung ohne Stopp, hat kein Alpha (t 0.76) und einen Drawdown von -62 Prozent: Der Stopp macht den Unterschied, nicht der Filter.

Die Short-Spiegelungen W2, W4 und W8 sind alle negativ (CAGR -5 bis -9 Prozent, MaxDD -63 bis -80 Prozent, kein Coin über Cash). Die Aurum-Hypothese «Ausbruchslogik gespiegelt auf die Short-Seite» ist damit verworfen. Long+Short verwässert die Long-Seite entsprechend.

Das auf Long-Perps gezahlte Funding kostet 3 bis 6 Prozentpunkte CAGR pro Jahr. Die Spot-Referenz (Bericht, kein Kriterium) liegt bei jeder Variante höher, W2 auf Spot 37.0 gegen 32.4 Prozent auf Perps, bei gleichem Drawdown. Für eine Long-only-Trendfolge ist Spot das bessere Instrument.

### Familie B, Mean Reversion

Verworfen ohne Nähe zu einem Kriterium. Long 5.7 Prozent CAGR bei Sharpe 0.25, Short -36 Prozent CAGR mit MaxDD -99 Prozent, alle Jitter-Nachbarn im selben Bild. Gegen den Trend in Kryptowährungen zu handeln hat in neun Jahren auf Tagesdaten keinen Ertrag geliefert.

### Familie C, Time-Series- und Cross-Sectional-Momentum

TS21, TS63 und TS126 Long-only zeigen hohe CAGR (35 bis 47 Prozent) bei 49 Prozent Exposure, aber kein Alpha gegen die Passivposition (t 1.1 bis 1.4), Drawdowns von -55 bis -65 Prozent und Holm-p 0.085. Das ist Marktbeta mit halber Exposure, kein Edge. Alle Short-Seiten sind mit MaxDD über -90 Prozent zerstörerisch. Die Kennzeichnung «BEIDES» bei TS-Short ist ein Artefakt: Die Short-Passivposition ist noch schlechter als die Strategie, das Urteil bleibt verworfen.

XS21 ist die Ausnahme. Long+Short besteht alle acht Kriterien: CAGR 49 Prozent, Sharpe 1.15, MaxDD -37.5 Prozent gegen -42 Prozent der Passivposition, Alpha 46 Prozent pro Jahr mit t 3.6, Beta -0.01, Holm-p unter 0.001, alle drei Zeitblöcke positiv, alle vier Jitter-Nachbarn positiv, K2 robust (CAGR 41 Prozent). Long-only besteht sieben von acht Kriterien und scheitert an c6 (MaxDD -72 gegen -70 Prozent), Short-only ist verworfen. Die Jahresrenditen von XS21 Long+Short sind 2020 und 2021 mit 164 und 168 Prozent aussergewöhnlich, sonst 14 bis 40 Prozent, 2026 bisher -7 Prozent.

Der Survivorship-Vermerk der Vorregistrierung gilt hier mit voller Kraft. XS21 wählt alle sieben Tage die drei stärksten unter zehn Coins, die 2026 nach heutiger Liquidität ausgesucht wurden und alle überlebt haben. Genau diese Konstruktion, Auswahl der Gewinner unter Überlebenden, ist die, bei der ein Rückblick am meisten schmeichelt. Der Test ist bestanden, aber er misst ein Universum, das es 2018 so nicht gab. Ohne Point-in-Time-Universum mit delisteten Coins ist die Zahl nicht belastbar.

### Familie D, Carry, Funding, Open Interest

D-CC Cash-and-Carry besteht alle acht Kriterien: CAGR 12.0 Prozent, Sharpe 4.95, MaxDD -1.7 Prozent, Erwartung je Trade 4.9 Prozent, Trefferquote 60 Prozent, alle drei Zeitblöcke positiv, alle Jitter-Nachbarn positiv, K2 robust (CAGR 9.1 Prozent, Sharpe 3.1). Der Ertrag ist erhaltenes Funding auf dem Short-Bein, 11.5 Prozent pro Jahr, abzüglich 2.1 Prozent Kosten. Das Basis-Ergebnis zwischen Spot und Perp ist vernachlässigbar, bei BTC 0.7 Prozentpunkte über alle elf Trades.

Der Ertrag ist aber kein Marktedge, sondern eine Regime-Ernte. Jahresrenditen: 2020 19 Prozent, 2021 41 Prozent, 2022 2 Prozent, 2023 5 Prozent, 2024 12 Prozent, 2025 3 Prozent, 2026 bisher 2 Prozent. Ohne die Funding-Spitzen 2020, 2021 und 2024 verdient die Konstruktion ungefähr den Cash-Satz. Sie ist Klasse L mit 133 Trades gepoolt und 9 bis 17 je Coin und trägt nach Vorregistrierung den Vermerk «bestanden mit geringer Trade-Basis».

Die Kraken-Gegenprobe ist nicht bestanden. Die Vorzeichen-Übereinstimmung von f_7d zwischen Binance und Kraken liegt im Überlappungsjahr bei 84.5 Prozent (BTC), 88.3 Prozent (ETH) und 78.8 Prozent (SOL), verlangt waren 90. Die Niveaus stimmen (Korrelation 0.79 bis 0.83), aber der CC-Schalter hätte auf Kraken-Funding bei BTC an 41 Prozent der Tage einen anderen Zustand gehabt. Die Vorregistrierung schreibt dafür den Datenvorbehalt vor: Das Urteil gilt für Binance-Funding, nicht für Kraken.

D-FC Funding-Contrarian Long-only ist statistisch signifikant (Holm-p 0.006, Sharpe 0.99, MaxDD -11 Prozent), scheitert aber an c1 (ETH negativ), c6 und c7. D-OI, erstmals gerechnet, zeigt nichts (Sharpe 0.03 bis 0.32, Holm-p 1.0). Die Open-Interest-Hypothese ist verworfen.

## MTP-Fingerprint, getrennt vom Edge-Urteil

Auf BTC sind W1, W2, W3, W5, W6, W7 und W8 «strukturell ähnlich» (sieben oder acht von neun Merkmalen im Band), W4 teilweise, auf ETH sind es W1, W5 und W7. W0 ist mit vier von sechs Merkmalen ebenfalls im Band. Der Fingerprint unterscheidet die Varianten nicht. Das sagt etwas über den Fingerprint: Die neun Merkmale (wenige Signale, lange Halten, niedrige Trefferquote, konzentrierte Gewinne, kleine Bear-Exposure, schiefe R-Verteilung) sind die allgemeinen Merkmale jeder Ausbruchs-Trendfolge mit nachgezogenem Stopp, nicht die Signatur einer bestimmten Regelmenge. Welche Variante Market Trend Pro am ehesten entspricht, lässt sich mit diesem Instrument nicht sagen.

## Was die Gegenproben zeigen

Der Look-ahead-Test auf einer am 30.06.2023 abgeschnittenen Historie ergab null abweichende Gewichtstage (W2, W6, MR-Short, TS21 auf BTC). Die Signal- und Gewichtslogik ist seit diesem Test unverändert. Die Stopp-, Gate- und Einstiegslogik von W2 wurde gegen eine unabhängige Nachrechnung geprüft (null Verstösse). D-CC wurde auf BTC je Trade unabhängig nachgerechnet (Basis und Funding identisch), das XS21-Portfolio unabhängig aus den Rohdaten (CAGR 86.8 gegen 86.5 Prozent, MaxDD identisch).

Vier Umsetzungsfehler, die der BTC-Testlauf nicht zeigen konnte, wurden vor der Interpretation behoben und sind in Abschnitt 12 des Berichts protokolliert. Keiner davon berührt eine Regel der Vorregistrierung. Der schwerwiegendste war die Poolung von XS21 als Coin-Mittel statt als Portfolio, was CAGR und MaxDD um den Faktor zehn verkleinerte, Sharpe und Vorzeichen aber unberührt liess.

## Datenvorbehalte

Binance-Funding endet am 31.08.2026, die Monatsdatei September ist noch nicht publiziert, die ersten vierzehn Septembertage laufen ohne Funding. Funding beginnt am 01.01.2020, Familie D läuft erst ab dann, Block P1 ist für Familie D nur das Jahr 2020. Perp-Kerzen haben Lücken von drei bis vier Tagen im März und April 2022 bei SOL, XRP und LTC. Der T-Bill-Satz ist ab dem 16.07.2026 fortgeschrieben. Open Interest beginnt für BTC am 01.01.2021, für die übrigen Coins am 01.12.2021, Nullzeilen im Binance-Archiv wurden nach der vorher festgelegten Regel «letzte positive Beobachtung je Tag» behandelt. Kraken-Funding liegt nur für ein Jahr und drei Coins vor.

## Zwei Lesarten, eine Entscheidung

Erste Lesart: Zwei Konstruktionen haben den vollen Test bestanden, dazu ein deutlicher Alpha-Befund in der Woo-Matrix, und die Vorbehalte sind Datenprobleme, die man lösen kann. Zweite Lesart: Was besteht, ist einerseits eine Auswahl unter Überlebenden und andererseits eine Regime-Ernte auf einer Börse, auf der nicht gehandelt wird, und was Alpha zeigt, verfehlt die Kriterien, die vorher gesetzt wurden.

Die Vorregistrierung entscheidet nicht zwischen den Lesarten, sie legt fest, was als bestanden gilt und welche Vorbehalte mitzuführen sind. Beides ist geschehen. Die Kriterien für die Woo-Matrix jetzt zu lockern, die Familiengrösse zu verkleinern oder c6 durch ein anderes Drawdown-Mass zu ersetzen, wäre die nachträgliche Anpassung, die Abschnitt 10 verbietet. Das wird nicht gemacht. Ebenso wenig wird XS21 ohne Point-in-Time-Universum oder D-CC ohne Kraken-Funding-Historie als handelbar bezeichnet.

## Konsequenzen nach Freeze-Protokoll

Die 37 Urteile sind final. Es gibt keinen zweiten Lauf mit angepassten Parametern, Bändern oder Kriterien auf denselben Daten.

Für die weitere Arbeit ergeben sich drei Linien, die alle in der Vorregistrierung angelegt sind und keine neue Variantenmatrix eröffnen. Erstens XS21: Ein Point-in-Time-Universum mit delisteten und damals gehandelten Coins ist die einzige Möglichkeit, das Survivorship-Problem zu lösen. Ohne dieses Universum bleibt XS21 eine Hypothese. Zweitens D-CC: Die Konstruktion braucht eine Kraken-Funding-Historie über mehr als ein Jahr oder eine bewusste Entscheidung, das Binance-Funding als Näherung zu akzeptieren, dazu ein explizites Kapital- und Margin-Modell, weil Spot long und Perp short zusammen mehr Kapital binden als das Notional von 1.0. Drittens Woo-Matrix: Der Alpha-Befund auf der Long-Seite ist als Hypothese festgehalten, nicht als Edge. Die sauberste Bestätigung ist keine Neuberechnung, sondern der Forward-Test auf Daten, die heute noch nicht existieren, mit den eingefrorenen Regeln von W2 oder W6 auf Spot.

Was Stufe 2 nicht beantwortet hat, ist die Frage nach einer kontinuierlichen Exposure-Steuerung. Die war für eine spätere Stufe vorgesehen und ist durch dieses Ergebnis weder nötiger noch weniger nötig geworden.

## Dateien

`stage2_report.md` (Bericht, zwölf Abschnitte), `stage2_mtp_fingerprint.md`, `stage2_results.json` (alle Kennzahlen, Prüfsummen der 48 Eingabedateien, Vorregistrierungs-Prüfsumme), `stage2_config_log.csv` (985 Konfigurationen), `stage2_trades/` (37 Dateien, 19 207 Trades), `spot_reference.json`, `kraken_funding_crosscheck.json`, `stage2_hypotheses_v2.md`.
