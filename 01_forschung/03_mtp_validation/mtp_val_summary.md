# Validierungsstufe MTP — Fazit

**Project Aurum II. Einmaliger Volllauf vom 17.09.2026 auf der eingefrorenen Vorregistrierung v0.2 (SHA-256 733bf2f5…) und der Spezifikation v1 (ed85be81…). Zehn Coins, Ebene A (Replikation auf CoinMarketCap), Ebene B (Kraken-Spot, handelbare Konvention, Kosten K0 bis K2), B2 (Signale auf Kraken), drei Sizing-Sichten, Bootstrap 2000. Kontrollen vor dem Lauf bestanden: Look-ahead-Test ohne Abweichung, BTC-Replikation 13 von 16 Entries, 14 von 16 Exits, 10 von 16 Exit-Preise unter 0.1 Prozent.**

## Ergebnis in einem Satz

Die rekonstruierte MTP-Mechanik wird nach den vorregistrierten Kriterien **verworfen**: Auf handelbaren Kraken-Daten (Ebene B, K1, ohne BTC) besteht sie nur die Kriterien 1 und 7, verfehlt Coin-Mehrheit, Zeitblöcke, Bootstrap mit Holm, Beta-Trennung und Retention. Auf Indexdaten ohne Kosten (Ebene A) besteht sie die Kriterien 1 bis 4, aber nicht die Beta-Trennung, weil sie je Einheit Risiko nicht mehr verdient als eine konstante Position mit gleicher Exposure. Der Befund ist kein Ausführungsproblem: Die Ausführung auf Kraken kostet wenig, die Zeit kostet viel. Was in A stark aussieht, stammt überwiegend aus 2017 bis 2021 und ist ab 2022 weg.

## Was die Daten zeigen

### Ebene A: die Mechanik auf ihren eigenen Daten

Über neun Validierungscoins und 102 Trades liefert die Mechanik ohne Kosten eine Erwartung von 0.70 R_gesamt je Trade (2.63 R_first), Profit-Faktor 4.5, Trefferquote 31 Prozent, Median minus 0.52 R. Die Verteilung ist die erwartete: 76 Prozent der Trades enden am Stop, 24 Prozent laufen über 3 R, die besten zehn Prozent der Trades tragen 56 Prozent des Bruttogewinns. Ohne die fünf besten Trades bleiben 351 von 537 Prozentpunkten Sleeve-Ertrag übrig, sieben von neun Coins sind positiv, sechs auch ohne ihren grössten Gewinner. Der Bootstrap ist deutlich (5-Prozent-Perzentil plus 3.4 Prozent pro Jahr, Holm-p unter 0.001). Bis hierhin sieht die Konstruktion aus, wie Woo sie beschreibt.

Zwei Dinge relativieren das. Erstens die Zeit: In Block P1 bis 2020 liegt die Erwartung bei 1.37 R (37 Trades), in P2 bei 0.66 R, in P3 ab 2024 bei 0.08 R (39 Trades). Die Jahre 2022, 2023, 2025 und 2026 sind negativ. Zweitens die Beta-Trennung: Alpha ist positiv und signifikant (3.6 Prozent pro Jahr, t 2.56), aber die Sharpe Ratio des Systems (1.31) liegt unter der einer konstanten Position mit derselben mittleren Exposure von 2.9 Prozent (1.34), und der Drawdown ist grösser als der dieser Passivposition (minus 9.5 gegen minus 3.6 Prozent). Nach der eingefrorenen Definition ist das weder ein Alpha-Effekt noch eine Risikotransformation. Das System nimmt in wenigen Phasen konzentriert Long-Exposure in einem Markt, der in diesen Jahren stark gestiegen ist, und verdient damit ungefähr das, was diese Exposure verdient hätte.

BTC, als Identifikationsmarkt nicht gewertet, liegt mit 1.04 R und Profit-Faktor 6.8 über allen anderen Coins. Das ist mit der Vermutung vereinbar, dass Woos Defaults auf BTC gewachsen sind.

### Ebene B: dieselben Signale auf Kraken

Im handelbaren Fenster (ab 2018 für die grossen Coins, später für die jüngeren) bleiben 73 Trades. Erwartung 0.10 R_gesamt, Profit-Faktor 2.6, Trefferquote 21 Prozent, Median minus 0.67 R. Nur ETH, XRP, SOL und ADA sind positiv, LINK, LTC, AVAX, DOT und BNB negativ, davon LINK, LTC und AVAX klar. Nur Block P1 ist positiv (15 Trades), P2 und P3 sind bei null. Der Bootstrap reicht nicht (5-Prozent-Perzentil minus 0.0 Prozent, Holm-p 0.105). Die Top-5-Trades tragen 51 Prozent des Bruttogewinns, ohne sie bleiben 38 von 215 Prozentpunkten.

Die Ausführung selbst ist nicht das Problem. 68 der 73 B-Trades haben ein exaktes Gegenstück in A. Der Exit-Grund stimmt in 98.8 Prozent überein, der Exit-Tag in 82 Prozent exakt und in 90 Prozent auf einen Tag genau. Der Übergang von Tagesschluss auf den ersten handelbaren Kraken-Preis nach Mitternacht kostet 0.1 Prozent je Fill, K1-Kosten und Slippage zusammen etwa 0.05 R je Trade. Es gab in acht Jahren und neun Coins genau einen Phantom-Stop, bei dem ein Kraken-Tief den CMC-Stop berührte und das CMC-Tief nicht, aber dieser eine (LINK, November 2020) verwandelte einen Ziel-Exit mit plus 4 R in einen Stop mit minus 1 R und erklärt allein den grössten Teil der Retention-Differenz auf den Paaren (0.61, ohne dieses Paar 0.86). Fünf weitere B-Trades ohne Gegenstück in A sind Randeffekte des Vergleichsfensters, alle Verlierer. Die vorregistrierte Retention von 0.37 verfehlt die Schwelle, aber der eigentliche Grund, warum B schwach ist, ist derselbe wie in A: Das B-Fenster liegt in der Zeit, in der die Mechanik nicht mehr trägt (A im selben Fenster: 0.26 R).

Kosten und Konvention ändern das Bild nicht: K0 bis K2 liegen bei 0.12, 0.10, 0.06 R, Same-Day-Close und Next-Bar-Open sind auf zwei Dezimalen gleich. Die Frühphase, die die B-Start-Regel abschneidet (B_full), hätte 0.28 R gebracht, also mehr, was denselben Zeiteffekt zeigt.

### B2: Signale auf Kraken-Daten erzeugt

Wer das System auf Kraken handelt, hat keinen CMC-Feed. Mit Signalen aus Kraken-Kerzen ist die Mechanik eine andere: Das Wilder-ATR liegt im Mittel 20 Prozent höher (Kraken-Kerzen enthalten Flash-Crash-Extreme, die der Index glättet), Stop und Ziel liegen weiter, Pivot-Niveaus stimmen nur zu 73 Prozent überein, nur 34 Prozent der Trades sind identisch. Erwartung 0.00 R, Profit-Faktor 2.7, ein einzelner Trade trägt 41 Prozent des Bruttogewinns. Das ist die Antwort auf die Frage, ob die Mechanik an der Index-Glättung hängt: teilweise ja.

### Sizing, Pyramiding, Jitter

Die drei Sichten ändern nichts am Urteil. Sicht 1b (Compounding) und Sicht 1 sind fast gleich, Sicht 2 (gemeinsames Portfolio, 29 Prozent Exposure) erreicht 20 Prozent CAGR bei minus 44 Prozent MaxDD und liegt damit unter der exposure-gleichen Passivposition (38 Prozent CAGR). Pyramiding wirkt wie in der Spezifikation beschrieben: Der gemeinsame Stop liegt im Mittel erst beim vierten Add-on über dem Durchschnittseinstieg, davor erhöht jedes Add-on das Notional (von 17 auf 25 Prozent des Sleeve-Kapitals) bei sinkendem Open Risk, weil der Stop mitwandert. Nur 16 Prozent der Add-ons bringen den Stop in den Gewinn, weil die meisten Trades vor dem vierten Add-on enden. Die Jitter-Nachbarn (Stop 5.5 und 7.5, Ziel 30 und 45, Pivot 3 und 10) liegen in B zwischen 0.06 und 0.20 R, in A zwischen 0.58 und 0.78 R. Die Basis liegt in B am unteren Rand, nirgends gibt es eine Spitze, die eine Optimierung verraten würde, aber auch kein Nachbar erreicht die Kriterien.

## Was das Ergebnis bedeutet und was nicht

Es bedeutet: Die rekonstruierte Mechanik hat auf neun Coins über 2018 bis 2026 auf handelbaren Daten keinen Edge, der die vorregistrierten Kriterien erfüllt, und auf Indexdaten ohne Kosten einen Ertrag, der sich nicht von konzentrierter Long-Exposure in einem steigenden Markt trennen lässt und der in den letzten fünf Jahren verschwunden ist. Der öffentliche BTC-Backtest zeigt das Beste, was die Mechanik je geleistet hat, auf dem Markt, auf dem sie entwickelt wurde, in den Jahren, in denen sie funktionierte.

Es bedeutet nicht, dass Trendfolge in Krypto tot ist oder dass die Konstruktion «weiter Stop, weites Ziel, Pyramiding» wertlos ist. Die R-Verteilung hat die Form, die man von Trendfolge erwartet, und sie tritt auf mehreren Coins auf (in A sind sieben von neun positiv). Was fehlt, ist die Wiederholbarkeit über die Zeit. Ob das ein Regimewechsel ab 2022 ist oder eine Eigenschaft des Marktes, der reifer und effizienter geworden ist, kann diese Stufe nicht sagen.

Es bedeutet auch nicht, dass die Rekonstruktion falsch war. Die Replikationskontrolle auf BTC ist bestanden, die Mechanik ist die, die der Backtester zeigt. Getestet wurde das richtige System.

## Konsequenzen nach Freeze-Protokoll

Das Urteil ist final. Es gibt keinen zweiten Lauf mit angepassten Parametern, Fenstern, Kriterien oder Coins. Die Jitter-Nachbarn werden nicht als Kandidaten weiterverfolgt, obwohl zwei von ihnen in B leicht höher liegen, weil das genau die Auswahl nach Ergebnis wäre, die die Vorregistrierung ausschliesst.

Der Strang 03_woo_forward_spot (Priorität 4) verliert damit seine Grundlage in der bisherigen Form: Ein Forward-Test einer Mechanik, die in den letzten fünf Jahren auf keinem der neun Coins die Kriterien erreicht, hätte keine Verwerfungsregel, die er in absehbarer Zeit erreichen könnte. Er wird nicht gestartet, bis eine neue Hypothese vorliegt.

Was aus dem Lauf als Hypothese bleibt, steht in `mtp_val_hypotheses_v1.md`. Die beiden Stränge Priorität 2 (XS21 Point-in-Time) und 3 (D-CC Kraken) sind davon unberührt.

## Dateien

`mtp_val_report.md` (zwölf Abschnitte), `mtp_val_results.json` (alle Kennzahlen, 20 Eingabeprüfsummen, Kontrollen), `controls.json`, `trades/` (17 Dateien, alle Ebenen, Kosten und Sichten), `mtp_val.py`, `report_val.py`, `mtp_val_hypotheses_v1.md`.
