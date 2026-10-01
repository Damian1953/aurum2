# Validierungsstufe MTP — Vorregistrierung, Entwurf Version 0.1

**Project Aurum II, Forschungsstrang 03_mtp_validation (neu, nach 03_woo_mtp_reverse_engineering). 16.09.2026, Version 0.1 mit erweiterten Robustheitsmetriken und strikter Trennung von Signal und Sizing. Status: Entwurf zur Prüfung. Nichts wird gerechnet, bevor die Entscheidungen in Abschnitt 11 getroffen sind und das Dokument mit Prüfsumme eingefroren ist.**

Grundhaltung: MTP wird als ernsthafter Kandidat für einen starken Trend-Following-Edge behandelt. Die Validierung soll zeigen, ob die asymmetrische Payoff-Struktur der rekonstruierten Mechanik (wenige grosse Gewinner, begrenzte Verluste, sehr weiter Stop, sehr weites Ziel, Pyramiding) über unabhängige Coins und auf handelbaren Daten wiederkehrt. Keine pessimistische Vorannahme, keine nachträgliche Optimierung. Kein Parameter wird aufgrund der Ergebnisse von A oder B verändert.

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

## 6. Sizing, strikt getrennt vom Signal

Die Signalmechanik wird zuerst geprüft, das Sizing danach. Deshalb gilt für die Kriterien eine einfache, vorregistrierte und für alle Coins identische Risikoregel ohne Kapitalpfad-Abhängigkeit:

**Sicht 1 (massgebend).** Je Coin ein Sleeve mit festem Startkapital. Jeder Leg (Einstieg und jedes Add-on) riskiert r = 2 Prozent des Startkapitals des Sleeves bis zum eigenen Stop: Einheiten = 0.02 mal Startkapital geteilt durch (6.5 mal ATR am Leg-Tag). Kein Compounding, damit jeder Trade unabhängig vom Pfad in R messbar ist. Obergrenze Notional je Coin 100 Prozent des Startkapitals, ein Add-on, das sie überschreiten würde, wird verkleinert, nie der Einstieg.

**Sicht 1b (berichtet).** Wie Sicht 1 mit Compounding (r auf die laufende Sleeve-Equity).

**Sicht 2 (berichtet).** Gemeinsames Portfolio mit geteiltem Kapital, r = 2 Prozent der Portfolio-Equity je Leg, Portfolio-Exposure höchstens 100 Prozent, bei Kapitalknappheit Add-ons verkleinert. Sicht 2 misst Kapitalbindungseffekte, nicht den Signal-Edge, und ist kein Kriterium.

Portfolio-Sizing, Risikostaffelung oder jede Sizing-Optimierung werden erst untersucht, wenn die Signalmechanik nach Abschnitt 8 bestanden hat, und dann in einer eigenen Vorregistrierung.

**Definition von R.** R eines Trades ist das geplante Risiko des ersten Legs in Kapitaleinheiten: Einheiten des ersten Legs mal 6.5 mal ATR am Einstiegstag. Der Netto-P&L des ganzen Trades (alle Legs, nach Kosten) geteilt durch R ist das R-Multiple des Trades. Zusätzlich berichtet: R_gesamt als Summe der geplanten Risiken aller Legs und das entsprechende Multiple, damit der Beitrag des Pyramidings sichtbar wird.

## 7. Kennzahlen

Alle Kennzahlen je Coin, je Ebene (A, B, B2), je Kostenszenario, je Zeitblock, dazu gepoolt über die Coins. Kein CAGR als Kriterium, CAGR wird berichtet.

**Trade-Ebene.** Erwartung in R je Trade (Mittel), Median R, Verteilung der R-Multiples (P5, P25, P75, P90, P95, Anteil R kleiner als -1, Anteil R grösser als 3), Profit-Faktor, Trefferquote, durchschnittlicher Gewinner und durchschnittlicher Verlierer (in R und in Prozent), Gain-Loss-Verhältnis, Anzahl Trades, Legs je Trade (Mittel, Maximum), Exposure (Anteil investierter Tage, mittlere Notional-Exposure), durchschnittliche Haltedauer gesamt, der Gewinner und der Verlierer.

**Exit-Struktur.** Verteilung der Exits nach Stop und Ziel, je Coin und gepoolt. Anteil der Stop-Exits, die über dem Durchschnittseinstieg liegen (Stop im Gewinn nach Add-ons). Realisiertes Verhältnis Ziel-Distanz zu Stop-Distanz.

**Pfad-Ebene, Berichtswerte.** Max Drawdown, längste und mittlere Recovery Time (Tage vom Drawdown-Tief bis zum alten Hoch), schlechtestes Jahr, schlechtestes rollendes Jahr, Ulcer-Index, Exposure-gleiche Passivposition als Vergleich.

**Konzentration und Wiederholbarkeit.** Anteil jedes Coins am Gesamt-P&L. Anteil der grössten Gewinner am Gesamt-P&L (Top 1, Top 3, Top 5, Top 10 Prozent). Ergebnis je Coin ohne den grössten Gewinner dieses Coins. Portfolioergebnis ohne Top 1, Top 3 und Top 5 Trades. Anzahl Coins mit positiver Erwartung ohne ihren grössten Gewinner. Anzahl Zeitblöcke mit positiver Erwartung je Coin.

Das Entfernen der grössten Gewinner ist kein Pass-Fail-Test gegen Trendfolge. Ein Trend-Following-System darf von wenigen grossen Trends leben. Gemessen wird, ob diese Eigenschaft über Coins und Zeitblöcke wiederholt auftritt (mehrere Coins, mehrere Blöcke mit je eigenen grossen Gewinnern) oder ob das Gesamtergebnis von einem einzelnen historischen BTC-Trade dominiert wird. Die Wiederholbarkeit wird berichtet und in Kriterium 2 und 3 über Coin-Mehrheit und Zeitblöcke geprüft, nicht über das Entfernen von Trades.

**Edge-Retention A nach B.** Verhältnis der Erwartung in R B/A, Verhältnis Profit-Faktor B/A, Differenz Trefferquote, Anzahl Trades mit abweichendem Exit-Grund zwischen A und B, Anteil der Trades, deren Kraken-Fill den CMC-Fill um mehr als 1 Prozent verfehlt, mittlere Fill-Abweichung an Einstieg, Stop und Ziel getrennt, Kostenanteil am Brutto-P&L.

**Statistik.** Wie Stufe 2: stationärer Block-Bootstrap auf Tagesrenditen, 5-Prozent-Perzentil der Überrendite gegen Cash, p-Wert für Sharpe grösser null, Holm über die Tests dieser Stufe (A, B, B2 gepoolt), Trade-Bootstrap der Erwartung in R berichtet. Beta-Trennung gegen exposure-gleiche Passivposition wie Stufe 2 Abschnitt 13.3. Jitter-Nachbarn aus Abschnitt 2 als Plateau-Prüfung berichtet.

## 8. Kriterien (Vorschlag, Entscheidung 11.4)

Bestanden gilt für Ebene B, Szenario K1, gepoolt über die zehn Coins, Sicht 1 (feste Risikoregel ohne Compounding):

1. Erwartung in R je Trade netto grösser null, Profit-Faktor mindestens 1.5.
2. Positiv (Erwartung netto grösser null) auf BTC und ETH und auf der Mehrheit der übrigen Coins mit mindestens zehn Trades.
3. Mindestens zwei der drei Zeitblöcke mit positiver Erwartung.
4. Bootstrap-5-Prozent-Perzentil der Überrendite grösser null und Holm-korrigierter p-Wert unter 0.05.
5. Beta-Trennung: Alpha-Teiltest oder Risikotransformations-Teiltest bestanden.
6. Edge-Retention: Erwartung in R in B mindestens 60 Prozent von A, und der Anteil der Trades mit abweichendem Exit-Grund höchstens 15 Prozent.
7. Trade-Mindestzahl: gepoolt mindestens 60 Trades, BTC und ETH je mindestens 10 (Klasse L nach Stufe 2, Vermerk «geringe Trade-Basis» bei weniger als 100).
8. Konzentration wird berichtet, ist kein Kriterium: Ergebnis ohne Top 1, Top 3, Top 5 und je Coin ohne den grössten Gewinner muss ausgewiesen werden, mit der Anzahl der Coins und Zeitblöcke, die auch dann positiv bleiben.

Kein Kriterium auf CAGR, Sharpe oder MaxDD absolut. MaxDD wird gegen die exposure-gleiche Passivposition berichtet, nicht als Kriterium, weil ein 6.5-ATR-Stop Drawdowns von 17 bis 19 Prozent je Trade konstruktionsbedingt zulässt und die Frage dieser Stufe der Ertrag je Risiko ist, nicht die Drawdown-Form.

Teilweise bestanden: Kriterien 1 bis 5 in A, aber 6 verfehlt. Das wäre der Befund «Edge existiert im Index, überlebt die Ausführung nicht». Verworfen: 1 oder 4 verfehlt in A.

## 9. Was nicht gemacht wird

Keine Parametersuche. Keine Auswahl von Coins nach Ergebnis. Keine Kombination mit Stufe-2-Varianten. Keine Short-Seite. Kein Regimefilter. Keine Anpassung von Sizing oder Kosten nach Kenntnis der Resultate. Kein zweiter Lauf auf denselben Daten.

## 10. Datenbedarf

CMC-Tageskerzen für die neun weiteren Coins (Loader `nachladen_cmc.py` mit CMC-IDs erweitern, Mac-Launcher). Kraken-Spot-Tageshistorie in USD für alle zehn Coins über die volle Zeit: Die REST-API liefert nur 720 Tage, die vollständige Historie gibt es als Kraken-Download-Archiv (OHLCVT-Zip) oder durch Aggregation der Trade-Historie über die API. Zu klären, welche Quelle benutzt wird (Entscheidung 11.5). Für Coins ohne Kraken-Historie im frühen Zeitraum beginnt B später als A, der Vergleich A gegen B wird nur auf der Überlappung geführt.

## 11. Offene Entscheidungen vor dem Freeze

1. Klasse-3-Annahmen: Basis-Form übernehmen oder auf Leg-Termine aus dem Backtester warten (Empfehlung: warten, wenn die Termine innerhalb einer Woche verfügbar sind, sonst Basis).
2. Ebene A ohne Kosten (wie Backtester) oder mit K0 (Empfehlung: ohne, damit A die Replikation bleibt, K0 als Zusatzzeile).
3. Risiko je Leg r = 2 Prozent des Sleeve-Startkapitals ohne Compounding für die Kriterien (Alternativen 1 oder 3, Empfehlung 2, keine Optimierung, wird eingefroren).
4. Kriterienschwellen in Abschnitt 8, insbesondere Profit-Faktor 1.5 und Retention 60 Prozent.
5. Kraken-Historie: Download-Archiv oder API-Aggregation (Empfehlung: Archiv, weil vollständig und reproduzierbar).
6. Ob B2 (Signale auf Kraken) als dritte Testzeile mitläuft (Empfehlung: ja, berichtet, aber A und B massgebend).
7. Ob die Jitter-Nachbarn aus Abschnitt 2 gerechnet werden (Empfehlung: ja, als Plateau-Prüfung, ohne Auswahlwirkung).
