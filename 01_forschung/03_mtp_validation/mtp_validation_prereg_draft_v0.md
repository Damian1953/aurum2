# Validierungsstufe MTP — Vorregistrierung, Entwurf Version 0

**Project Aurum II, Forschungsstrang 03_mtp_validation (neu, nach 03_woo_mtp_reverse_engineering). 16.09.2026. Status: Entwurf zur Prüfung. Nichts wird gerechnet, bevor die Entscheidungen in Abschnitt 11 getroffen sind und das Dokument mit Prüfsumme eingefroren ist.**

## 1. Fragestellung und Arbeitshypothese

Arbeitshypothese: Die rekonstruierte MTP-Mechanik (Spezifikation v1) enthält einen echten und wirtschaftlich relevanten Trend-Following-Edge. Diese Hypothese wird weder durch Skepsis noch durch Euphorie vorweggenommen. Getestet wird sie in zwei Ebenen mit identischen Signalen: **A, Replikation** auf der Datenquelle des Backtesters (CoinMarketCap), und **B, Real** auf handelbaren Kraken-Daten mit Gebühren, Slippage und Fill-Annahmen. Die dritte Frage ist, wie viel des in A gemessenen Ergebnisses in B erhalten bleibt.

Formal H0: Die eingefrorene Mechanik erzeugt nach Kosten (Ebene B, Szenario K1) keine positive Erwartung je Trade, die sich von einer passiven Position mit gleicher Exposure unterscheidet. H1: Sie tut es, und der Effekt ist über Coins und Zeitblöcke stabil.

Stufe 2 von Aurum II ist kein Test dieser Mechanik. Sie hat bei Stop, Trailing, Ziel, Exit, Add-ons und Fill-Logik eine andere Strategie geprüft. Ihre Urteile werden weder herangezogen noch umgedeutet.

## 2. Eingefrorene Mechanik

Spezifikation v1, Abschnitt 9, ohne Änderung: Wilder-ATR(180), SMA200-Filter nur beim Einstieg, Pivot-Niveau (Breite 5, Alter 20 bis 365, verbraucht durch Tageshoch), Einstieg per Tageshoch zum Schluss, Add-on per Pivot-Ausbruch mit Schluss über Niveau und Abstand 1.5 ATR, Stop «letzter Leg minus 6.5 ATR» ohne Trailing, Ziel «erster Leg plus 37.5 ATR» fix, Exits intraday am Niveau. Klasse-3-Bestandteile (Verbrauch, Pivot-Breite, Abstand) gehen in der Basis-Form ein und werden als Annahme ausgewiesen. Sollten die Leg-Termine aus dem Backtester vor dem Freeze eintreffen und eine Klasse-3-Annahme ändern, wird die Spezifikation auf v1.1 gehoben und dieser Entwurf angepasst, danach eingefroren. Nach dem Freeze keine Änderung, auch nicht bei neuen Backtester-Daten.

Keine Parameteränderung während oder nach dem Lauf. Kein Ergebnis wird durch eine Anpassung gerettet. Jitter-Nachbarn werden berichtet, nicht ausgewählt: 6.5 ATR gegen 5.5 und 7.5, 37.5 ATR gegen 30 und 45, Pivot-Breite 5 gegen 3 und 10. Sie dienen der Frage «ist das Ergebnis eine Spitze oder ein Plateau», nicht der Wahl.

## 3. Universum und Zeitraum

Die zehn Coins aus Stufe 2 (BTC, ETH, SOL, XRP, ADA, AVAX, LINK, DOT, BNB, LTC), Survivorship-Vermerk wie dort. Zeitraum je Coin ab dem ersten Tag mit vollem Warmup (365 Tage für das Niveau, 200 für SMA, 180 für ATR) bis 2026-09-15. Zeitblöcke wie Stufe 2: P1 bis 2020, P2 2021 bis 2023, P3 ab 2024. BTC zusätzlich ab 2015 (CMC ab 2013).

## 4. Ebene A, Replikation

Daten: CMC-Tageskerzen je Coin. Ausführung wie Spezifikation: Einstieg zum CMC-Schluss, Exits am Niveau, keine Kosten (wie im Backtester, der keine Gebühren ausweist, zu prüfen in Abschnitt 11). Zwei Sichten: je Coin als eigenständiges System mit vollem Kapital, und Portfolio mit dem Sizing aus Abschnitt 6. BTC-Trades werden gegen die 16 beobachteten geprüft (Kontrollzeile, Erwartung 13 von 16 exakt).

## 5. Ebene B, Real

Daten: Kraken-Spot-Tageskerzen je Coin in USD (Beschaffung Abschnitt 10). Signale werden **auf CMC-Daten erzeugt** wie in A (die Mechanik ist auf CMC definiert) und **auf Kraken-Daten ausgeführt**. Alternative B2, berichtet: Signale und Ausführung beide auf Kraken-Daten. Fills:

- Einstieg und Add-on: Kraken-Schluss des Signaltages (00:00 UTC, gleiche Kerze) plus Slippage.
- Stop: Stop-Market am Niveau. Fill am Niveau minus Slippage, wenn das Kraken-Tief das Niveau erreicht. Liegt das Kraken-Open unter dem Niveau, Fill am Open minus Slippage.
- Ziel: Limit am Niveau. Fill am Niveau, wenn das Kraken-Hoch es erreicht, ohne Slippage. Liegt das Open darüber, Fill am Open.
- Kosten wie Stufe-2-Spot-Modell: K1 0.40 Prozent Gebühr plus 0.02 Reibung je Seite, K2 0.80 plus 0.06, K0 0.16 ohne Reibung, Bericht aller drei, K1 massgebend. Slippage am Stop zusätzlich 0.10 Prozent (K1) und 0.30 Prozent (K2), begründet durch Stop-Market-Ausführung an Abwärtstagen.
- Cash zum T-Bill-Satz wie Stufe 2.

Kein Perp, kein Funding, kein Short. Long-only Spot.

## 6. Sizing und Portfolio

Die Erstposition und jede Add-on-Grösse folgen einem eigenen, hier festgelegten Risiko-Sizing (Klasse-3-Annahme, ausgewiesen): Einheiten = r mal Equity geteilt durch (6.5 mal ATR), mit r = 2 Prozent je Leg (Entscheidung 11.3). Maximale Exposure je Coin 100 Prozent des Sleeve-Kapitals, Portfolio-Exposure höchstens 100 Prozent, bei Kapitalknappheit wird das Add-on verkleinert, nie der Einstieg. Je Coin ein Sleeve mit gleichem Startkapital (Sicht 1), dazu ein gemeinsames Portfolio mit geteiltem Kapital (Sicht 2). Beide Sichten werden berichtet, Sicht 1 ist für die Kriterien massgebend, weil sie ohne Kapitalbindungseffekte auskommt.

## 7. Kennzahlen

Je Coin, je Ebene, je Kostenszenario, je Zeitblock, dazu gepoolt: Erwartung je Trade (brutto und netto), Profit-Faktor, Trefferquote, Ø Gewinn und Ø Verlust, Gain-Loss-Verhältnis, Anzahl Trades und Legs je Trade, Haltedauer Gewinner und Verlierer, CAGR (berichtet, nicht Kriterium), MaxDD, Recovery Time (Tage vom Drawdown-Tief bis zum alten Hoch, längste und mittlere), Exposure (Anteil investierter Tage und mittlere Notional-Exposure), Tail-Risiko (schlechtester Trade, schlechtestes Jahr, schlechtestes rollendes Jahr, 5-Prozent-Quantil der Trade-Verteilung), Beitrag der grössten Gewinner (Anteil der Top-3 und Top-10-Prozent am Bruttogewinn, Ergebnis ohne den besten Trade und ohne die besten drei), Exit-Verteilung (Anteil Stop, Ziel), Verhältnis Stop-Distanz zu Ziel-Distanz realisiert.

Edge-Retention A nach B: Verhältnis der Erwartung je Trade B/A, Verhältnis Profit-Faktor B/A, Differenz der Trefferquote, Anzahl Trades mit abweichendem Exit-Grund zwischen A und B (Stop in B, Ziel in A oder umgekehrt), Anteil der Trades, in denen der Kraken-Fill den CMC-Fill um mehr als 1 Prozent verfehlt.

Statistik wie Stufe 2: stationärer Block-Bootstrap auf Tagesrenditen, 5-Prozent-Perzentil der Überrendite gegen Cash, p-Wert für Sharpe grösser null, Holm über die Anzahl der Tests dieser Stufe (drei: A, B, B2, je gepoolt), Trade-Bootstrap der Erwartung berichtet. Beta-Trennung gegen exposure-gleiche Passivposition wie Stufe 2 Abschnitt 13.3.

## 8. Kriterien (Vorschlag, Entscheidung 11.4)

Bestanden gilt für Ebene B, Szenario K1, gepoolt über die zehn Coins, Sicht 1:

1. Erwartung je Trade netto grösser null, Profit-Faktor mindestens 1.5.
2. Positiv (Erwartung netto grösser null) auf BTC und ETH und auf der Mehrheit der übrigen Coins mit mindestens zehn Trades.
3. Mindestens zwei der drei Zeitblöcke mit positiver Erwartung.
4. Bootstrap-5-Prozent-Perzentil der Überrendite grösser null und Holm-korrigierter p-Wert unter 0.05.
5. Beta-Trennung: Alpha-Teiltest oder Risikotransformations-Teiltest bestanden.
6. Edge-Retention: Erwartung je Trade in B mindestens 60 Prozent von A, und der Anteil der Trades mit abweichendem Exit-Grund höchstens 15 Prozent.
7. Trade-Mindestzahl: gepoolt mindestens 60 Trades, BTC und ETH je mindestens 10 (Klasse L nach Stufe 2, Vermerk «geringe Trade-Basis» bei weniger als 100).
8. Konzentration wird berichtet, ist kein Kriterium: Ergebnis ohne die besten drei Trades muss ausgewiesen werden.

Kein Kriterium auf CAGR, Sharpe oder MaxDD absolut. MaxDD wird gegen die exposure-gleiche Passivposition berichtet, nicht als Kriterium, weil ein 6.5-ATR-Stop Drawdowns von 17 bis 19 Prozent je Trade konstruktionsbedingt zulässt und die Frage dieser Stufe der Ertrag je Risiko ist, nicht die Drawdown-Form.

Teilweise bestanden: Kriterien 1 bis 5 in A, aber 6 verfehlt. Das wäre der Befund «Edge existiert im Index, überlebt die Ausführung nicht». Verworfen: 1 oder 4 verfehlt in A.

## 9. Was nicht gemacht wird

Keine Parametersuche. Keine Auswahl von Coins nach Ergebnis. Keine Kombination mit Stufe-2-Varianten. Keine Short-Seite. Kein Regimefilter. Keine Anpassung von Sizing oder Kosten nach Kenntnis der Resultate. Kein zweiter Lauf auf denselben Daten.

## 10. Datenbedarf

CMC-Tageskerzen für die neun weiteren Coins (Loader `nachladen_cmc.py` mit CMC-IDs erweitern, Mac-Launcher). Kraken-Spot-Tageshistorie in USD für alle zehn Coins über die volle Zeit: Die REST-API liefert nur 720 Tage, die vollständige Historie gibt es als Kraken-Download-Archiv (OHLCVT-Zip) oder durch Aggregation der Trade-Historie über die API. Zu klären, welche Quelle benutzt wird (Entscheidung 11.5). Für Coins ohne Kraken-Historie im frühen Zeitraum beginnt B später als A, der Vergleich A gegen B wird nur auf der Überlappung geführt.

## 11. Offene Entscheidungen vor dem Freeze

1. Klasse-3-Annahmen: Basis-Form übernehmen oder auf Leg-Termine aus dem Backtester warten (Empfehlung: warten, wenn die Termine innerhalb einer Woche verfügbar sind, sonst Basis).
2. Ebene A ohne Kosten (wie Backtester) oder mit K0 (Empfehlung: ohne, damit A die Replikation bleibt, K0 als Zusatzzeile).
3. Risiko je Leg r = 2 Prozent (Alternativen 1 oder 3, Empfehlung 2, keine Optimierung, wird eingefroren).
4. Kriterienschwellen in Abschnitt 8, insbesondere Profit-Faktor 1.5 und Retention 60 Prozent.
5. Kraken-Historie: Download-Archiv oder API-Aggregation (Empfehlung: Archiv, weil vollständig und reproduzierbar).
6. Ob B2 (Signale auf Kraken) als dritte Testzeile mitläuft (Empfehlung: ja, berichtet, aber A und B massgebend).
7. Ob die Jitter-Nachbarn aus Abschnitt 2 gerechnet werden (Empfehlung: ja, als Plateau-Prüfung, ohne Auswahlwirkung).
