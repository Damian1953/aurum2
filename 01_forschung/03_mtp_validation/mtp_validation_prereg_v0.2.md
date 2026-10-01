# Validierungsstufe MTP — Vorregistrierung, Version 0.2 (Freeze-Fassung zur Bestätigung)

**Project Aurum II, Forschungsstrang 03_mtp_validation (nach 03_woo_mtp_reverse_engineering). 17.09.2026, Version 0.2. Gegenüber 0.1: handelbare Ausführungskonvention in Ebene B (erster handelbarer Kraken-Preis nach 00:00 UTC), BTC als Identifikationsmarkt ohne Validierungsgewicht, präzisierte Risikodefinition mit Open-Risk-Messung je Add-on und R_gesamt gleichrangig zu R, Mechanik-Reproduzierbarkeit CMC gegen Kraken als eigener Diagnoseblock, Entscheidungen aus Abschnitt 11 getroffen. Status: Freeze-Fassung. Nach Bestätigung wird die Prüfsumme in `00_doku/ENTSCHEIDE.md` protokolliert, danach keine Änderung mehr.**

Grundhaltung: MTP wird als ernsthafter Kandidat für einen starken Trend-Following-Edge behandelt. Die Validierung soll zeigen, ob die asymmetrische Payoff-Struktur der rekonstruierten Mechanik (wenige grosse Gewinner, begrenzte Verluste, sehr weiter Stop, sehr weites Ziel, Pyramiding) über unabhängige Coins und auf handelbaren Daten wiederkehrt. Keine pessimistische Vorannahme, keine nachträgliche Optimierung. Kein Parameter wird aufgrund der Ergebnisse von A oder B verändert.

## 1. Fragestellung und Arbeitshypothese

Arbeitshypothese: Die rekonstruierte MTP-Mechanik (Spezifikation v1) enthält einen echten und wirtschaftlich relevanten Trend-Following-Edge. Diese Hypothese wird weder durch Skepsis noch durch Euphorie vorweggenommen. Getestet wird sie in zwei Ebenen mit identischen Signalen: **A, Replikation** auf der Datenquelle des Backtesters (CoinMarketCap), und **B, Real** auf handelbaren Kraken-Daten mit Gebühren, Slippage und Fill-Annahmen. Die dritte Frage ist, wie viel des in A gemessenen Ergebnisses in B erhalten bleibt.

Formal H0: Die eingefrorene Mechanik erzeugt nach Kosten (Ebene B, Szenario K1) keine positive Erwartung je Trade, die sich von einer passiven Position mit gleicher Exposure unterscheidet. H1: Sie tut es, und der Effekt ist über Coins und Zeitblöcke stabil.

Stufe 2 von Aurum II ist kein Test dieser Mechanik. Sie hat bei Stop, Trailing, Ziel, Exit, Add-ons und Fill-Logik eine andere Strategie geprüft. Ihre Urteile werden weder herangezogen noch umgedeutet.

## 2. Eingefrorene Mechanik

Spezifikation v1, Abschnitt 9, ohne Änderung: Wilder-ATR(180), SMA200-Filter nur beim Einstieg, Pivot-Niveau (Breite 5, Alter 20 bis 365, verbraucht durch Tageshoch), Einstieg per Tageshoch zum Schluss, Add-on per Pivot-Ausbruch mit Schluss über Niveau und Abstand 1.5 ATR, Stop «letzter Leg minus 6.5 ATR» ohne Trailing, Ziel «erster Leg plus 37.5 ATR» fix, Exits intraday am Niveau. Klasse-3-Bestandteile (Verbrauch per Tageshoch, Pivot-Breite 5, Abstand 1.5 ATR) gehen in der Basis-Form ein und sind als Annahmen ausgewiesen. Der Freeze wartet nicht auf Leg-Termine aus dem Backtester. Treffen Leg-Termine (Trade 13, 16, 7) vor dem Freeze ein, werden sie ausgewertet und können eine Klasse-3-Annahme bestätigen oder verwerfen, dann Spezifikation v1.1 und Freeze. Treffen sie nach dem Freeze ein, dienen sie als Out-of-Sample-Replikationskontrolle der eingefrorenen Basisregel: Die Basis sagt für Trade 13 die Leg-Tage 18.01., 20.01., 21.06., 23.10.2023 und 02.01.2024 voraus, die Alternative acht andere. Das Ergebnis dieser Kontrolle wird berichtet und ändert die eingefrorene Mechanik nicht. Nach dem Freeze keine Änderung, auch nicht bei neuen Backtester-Daten.

Keine Parameteränderung während oder nach dem Lauf. Kein Ergebnis wird durch eine Anpassung gerettet. Jitter-Nachbarn werden berichtet, nicht ausgewählt: 6.5 ATR gegen 5.5 und 7.5, 37.5 ATR gegen 30 und 45, Pivot-Breite 5 gegen 3 und 10. Sie dienen der Frage «ist das Ergebnis eine Spitze oder ein Plateau», nicht der Wahl.

## 3. Universum und Zeitraum

Die zehn Coins aus Stufe 2 (BTC, ETH, SOL, XRP, ADA, AVAX, LINK, DOT, BNB, LTC), Survivorship-Vermerk wie dort.

**BTC ist Identifikationsmarkt.** Die Spezifikation wurde an sechzehn BTC-Trades rekonstruiert, die Klasse-3-Wahlen wurden nach Reproduktionsgüte auf BTC getroffen, und ob Woos Defaults selbst auf BTC optimiert wurden, ist unbekannt. Deshalb gilt BTC in dieser Stufe als Replikationskontrolle (Ebene A muss 13 von 16 beobachteten Trades exakt reproduzieren) und wird vollständig berichtet, zählt aber nicht als Evidenz für die Generalisierbarkeit. Die neun Validierungscoins sind gegenüber BTC nicht unabhängig im statistischen Sinn, sie teilen Marktbeta, Bull-Phasen und Survivorship. «Unabhängig» heisst hier: nicht zur Identifikation benutzt. Eine Generalisierung auf weitere Assets bleibt einer späteren Stufe mit Point-in-Time-Universum vorbehalten. Zeitraum je Coin ab dem ersten Tag mit vollem Warmup (365 Tage für das Niveau, 200 für SMA, 180 für ATR) bis 2026-09-15. Zeitblöcke wie Stufe 2: P1 bis 2020, P2 2021 bis 2023, P3 ab 2024. BTC zusätzlich ab 2015 (CMC ab 2013).

## 4. Ebene A, Replikation

Daten: CMC-Tageskerzen je Coin. Ausführung wie Spezifikation: Einstieg zum CMC-Schluss, Exits am Niveau, keine Kosten (wie im Backtester, der keine Gebühren ausweist), K0 als Zusatzzeile berichtet. Zwei Sichten: je Coin als eigenständiges System mit vollem Kapital, und Portfolio mit dem Sizing aus Abschnitt 6. BTC-Trades werden gegen die 16 beobachteten geprüft (Kontrollzeile, Erwartung 13 von 16 exakt).

## 5. Ebene B, Real

Daten: Kraken-Spot-Tageskerzen je Coin in USD (Beschaffung Abschnitt 10). Signale werden **auf CMC-Daten erzeugt** wie in A (die Mechanik ist auf CMC definiert) und **auf Kraken-Daten ausgeführt**. Alternative B2, berichtet: Signale und Ausführung beide auf Kraken-Daten. Fills:

- Einstieg und Add-on: erster handelbarer Kraken-Preis nach 00:00 UTC des Folgetages (Eröffnung der Kerze t+1 auf Kraken, weil Krypto keine Session-Eröffnung kennt), zuzüglich Slippage 0.05 Prozent (K1) und 0.15 Prozent (K2). Begründung: Der SMA200-Filter und der ATR-Abstand des Add-ons setzen den Schlusskurs t voraus und sind erst nach Kerzenschluss bekannt, eine Ausführung zum Schluss derselben Kerze wäre ein Look-ahead. Stop- und Zielniveau werden wie in A aus dem CMC-Schluss t und dem Wilder-ATR t berechnet und sind ab Kerze t+1 als ruhende Orders wirksam. Als Berichtswert wird B zusätzlich mit Ausführung zum Kraken-Schluss t ausgewiesen, um die Kosten der handelbaren Konvention zu beziffern. Kriterien gelten für die handelbare Konvention.
- Stop: Stop-Market am Niveau. Fill am Niveau minus Slippage, wenn das Kraken-Tief das Niveau erreicht. Liegt das Kraken-Open unter dem Niveau, Fill am Open minus Slippage.
- Ziel: Limit am Niveau. Fill am Niveau, wenn das Kraken-Hoch es erreicht, ohne Slippage. Liegt das Open darüber, Fill am Open.
- Kosten wie Stufe-2-Spot-Modell: K1 0.40 Prozent Gebühr plus 0.02 Reibung je Seite, K2 0.80 plus 0.06, K0 0.16 ohne Reibung, Bericht aller drei, K1 massgebend. Slippage am Stop zusätzlich 0.10 Prozent (K1) und 0.30 Prozent (K2), begründet durch Stop-Market-Ausführung an Abwärtstagen.
- Cash zum T-Bill-Satz wie Stufe 2.

Kein Perp, kein Funding, kein Short. Long-only Spot.

## 6. Sizing, strikt getrennt vom Signal

Die Signalmechanik wird zuerst geprüft, das Sizing danach. Deshalb gilt für die Kriterien eine einfache, vorregistrierte und für alle Coins identische Risikoregel ohne Kapitalpfad-Abhängigkeit:

**Sicht 1 (massgebend).** Je Coin ein Sleeve mit festem Startkapital. **Nominal Initial Risk per Leg = 2 Prozent des Sleeve-Startkapitals**, gemessen vom Leg-Einstieg (Schluss t in A, Fill t+1 in B) bis zum Stop, der bei diesem Leg gesetzt wird (Schluss t minus 6.5 ATR t). Einheiten des Legs = 0.02 mal Startkapital geteilt durch (6.5 mal ATR t). Diese Grösse ist eine Sizing-Vorschrift, kein Mass des offenen Risikos, weil der Stop gemeinsam ist und bei jedem Add-on auf den neuen Leg springt. Kein Compounding, damit jeder Trade unabhängig vom Pfad in R messbar ist. Obergrenze Notional je Coin 100 Prozent des Startkapitals, ein Add-on, das sie überschreiten würde, wird verkleinert, nie der Einstieg.

**Sicht 1b (berichtet).** Wie Sicht 1 mit Compounding (r auf die laufende Sleeve-Equity).

**Sicht 2 (berichtet).** Gemeinsames Portfolio mit geteiltem Kapital, r = 2 Prozent der Portfolio-Equity je Leg, Portfolio-Exposure höchstens 100 Prozent, bei Kapitalknappheit Add-ons verkleinert. Sicht 2 misst Kapitalbindungseffekte, nicht den Signal-Edge, und ist kein Kriterium.

Portfolio-Sizing, Risikostaffelung oder jede Sizing-Optimierung werden erst untersucht, wenn die Signalmechanik nach Abschnitt 8 bestanden hat, und dann in einer eigenen Vorregistrierung.

**Definition von R, zwei gleichrangige Sichten.** R_first eines Trades ist das Nominal Initial Risk des ersten Legs: Einheiten des ersten Legs mal 6.5 mal ATR am Einstiegstag. R_gesamt ist die Summe der Nominal Initial Risks aller Legs des Trades. Der Netto-P&L des ganzen Trades (alle Legs, nach Kosten) geteilt durch R_first ist das First-Leg-Multiple, geteilt durch R_gesamt das Gesamt-Multiple. Beide werden überall gleichrangig berichtet, wo R vorkommt (Erwartung, Median, Verteilung, Bootstrap). Bei starkem Pyramiding kann ein Trade auf First-Leg-R spektakulär aussehen, obwohl viel zusätzliches nominales Risiko aufgebaut wurde, das Gesamt-Multiple zeigt den Ertrag je eingesetzter Risikoeinheit. Kriterium 1 wird auf R_gesamt geprüft, weil es die konservativere Sicht ist, R_first wird daneben ausgewiesen.

**Open-Risk-Messung je Add-on.** Je Add-on werden berichtet: Open Risk vor dem Add-on (Summe über alle Legs von Einheiten mal Differenz aktueller Schluss zu altem Stop), Open Risk nach dem Add-on (gleich, mit neuem Stop und neuem Leg), Ergebnis des Gesamttrades bei sofortigem gemeinsamen Stop vor und nach dem Add-on (Summe über Legs von Einheiten mal Differenz Stop zu Leg-Einstieg, nach Kosten), Veränderung der Notional-Exposure durch das Add-on, Veränderung des Portfolio-at-Risk (Summe der Open Risks aller Sleeves geteilt durch Gesamtkapital, Sicht 2), und die Ordnungszahl des Add-ons, ab dem der gemeinsame Stop über dem Durchschnittseinstieg liegt. Damit wird sichtbar, ob Pyramiding Exposure erhöht, während das Restrisiko älterer Legs bereits sinkt oder abgesichert ist.

## 7. Kennzahlen

Alle Kennzahlen je Coin, je Ebene (A, B, B2), je Kostenszenario, je Zeitblock, dazu gepoolt über die Coins. Kein CAGR als Kriterium, CAGR wird berichtet.

**Trade-Ebene.** Erwartung in R je Trade (Mittel), Median R, Verteilung der R-Multiples (P5, P25, P75, P90, P95, Anteil R kleiner als -1, Anteil R grösser als 3), Profit-Faktor, Trefferquote, durchschnittlicher Gewinner und durchschnittlicher Verlierer (in R und in Prozent), Gain-Loss-Verhältnis, Anzahl Trades, Legs je Trade (Mittel, Maximum), Exposure (Anteil investierter Tage, mittlere Notional-Exposure), durchschnittliche Haltedauer gesamt, der Gewinner und der Verlierer.

**Exit-Struktur.** Verteilung der Exits nach Stop und Ziel, je Coin und gepoolt. Anteil der Stop-Exits, die über dem Durchschnittseinstieg liegen (Stop im Gewinn nach Add-ons). Realisiertes Verhältnis Ziel-Distanz zu Stop-Distanz.

**Pfad-Ebene, Berichtswerte.** Max Drawdown, längste und mittlere Recovery Time (Tage vom Drawdown-Tief bis zum alten Hoch), schlechtestes Jahr, schlechtestes rollendes Jahr, Ulcer-Index, Exposure-gleiche Passivposition als Vergleich.

**Konzentration und Wiederholbarkeit.** Anteil jedes Coins am Gesamt-P&L. Anteil der grössten Gewinner am Gesamt-P&L (Top 1, Top 3, Top 5, Top 10 Prozent). Ergebnis je Coin ohne den grössten Gewinner dieses Coins. Portfolioergebnis ohne Top 1, Top 3 und Top 5 Trades. Anzahl Coins mit positiver Erwartung ohne ihren grössten Gewinner. Anzahl Zeitblöcke mit positiver Erwartung je Coin.

Das Entfernen der grössten Gewinner ist kein Pass-Fail-Test gegen Trendfolge. Ein Trend-Following-System darf von wenigen grossen Trends leben. Gemessen wird, ob diese Eigenschaft über Coins und Zeitblöcke wiederholt auftritt (mehrere Coins, mehrere Blöcke mit je eigenen grossen Gewinnern) oder ob das Gesamtergebnis von einem einzelnen historischen BTC-Trade dominiert wird. Die Wiederholbarkeit wird berichtet und in Kriterium 2 und 3 über Coin-Mehrheit und Zeitblöcke geprüft, nicht über das Entfernen von Trades.

**Edge-Retention A nach B.** Verhältnis der Erwartung in R (R_first und R_gesamt) B/A, Verhältnis Profit-Faktor B/A, Differenz Trefferquote, Anteil der Trades, deren Kraken-Fill den CMC-Fill um mehr als 1 Prozent verfehlt, Kostenanteil am Brutto-P&L.

**Mechanik-Reproduzierbarkeit CMC gegen Kraken.** Ziel ist nicht nur, ob die Performance ähnlich bleibt, sondern ob die Mechanik auf Börsendaten dieselben Entscheidungen trifft. Vergleich A gegen B (gleiche Signale, Kraken-Ausführung): Anteil Trades mit identischem Exit-Grund, Anzahl Phantom-Stops (Kraken-Tief unter Stop bei CMC-Tief über Stop) und umgekehrt, Anzahl Ziel-Treffer nur auf einer Seite, Exit-Tag-Differenz, Fill-Abweichung an Einstieg, Stop und Ziel getrennt. Vergleich A gegen B2 (Signale auf Kraken erzeugt): Entry-Tag-Match exakt und ±1 Tag, Exit-Tag-Match exakt und ±1, Leg-Zahl je Trade, identischer Exit-Grund, relative Abweichung des Stop-Niveaus je Leg, Anteil vollständig identischer Trades (Entry, Legs, Exit-Grund, Exit-Tag ±1), Übereinstimmung des SMA200-Filters je Tag, Verhältnis Wilder-ATR Kraken zu CMC (Mittel und Spanne), Übereinstimmung des Pivot-Niveaus je Tag. Diese Werte sind Bericht und Diagnose, keine Kriterien.

**Statistik.** Wie Stufe 2: stationärer Block-Bootstrap auf Tagesrenditen, 5-Prozent-Perzentil der Überrendite gegen Cash, p-Wert für Sharpe grösser null, Holm über die Tests dieser Stufe (A, B, B2 gepoolt), Trade-Bootstrap der Erwartung in R berichtet. Beta-Trennung gegen exposure-gleiche Passivposition wie Stufe 2 Abschnitt 13.3. Jitter-Nachbarn aus Abschnitt 2 als Plateau-Prüfung berichtet.

## 8. Kriterien (Vorschlag, Entscheidung 11.4)

Bestanden gilt für Ebene B, Szenario K1, handelbare Konvention, Sicht 1 (feste Risikoregel ohne Compounding), gepoolt über die neun Validierungscoins ohne BTC. Der Pool mit BTC wird daneben berichtet.

1. Erwartung in R_gesamt je Trade netto grösser null, Profit-Faktor mindestens 1.5.
2. Positiv (Erwartung in R_gesamt netto grösser null) auf ETH und auf der Mehrheit der übrigen acht Coins mit mindestens zehn Trades. BTC zählt nicht.
3. Mindestens zwei der drei Zeitblöcke mit positiver Erwartung.
4. Bootstrap-5-Prozent-Perzentil der Überrendite grösser null und Holm-korrigierter p-Wert unter 0.05.
5. Beta-Trennung: Alpha-Teiltest oder Risikotransformations-Teiltest bestanden.
6. Edge-Retention: Erwartung in R_gesamt in B mindestens 60 Prozent von A, und der Anteil der Trades mit abweichendem Exit-Grund zwischen A und B höchstens 15 Prozent.
7. Trade-Mindestzahl: gepoolt ohne BTC mindestens 60 Trades, ETH mindestens 10 (Klasse L nach Stufe 2, Vermerk «geringe Trade-Basis» bei weniger als 100).
8. Konzentration wird berichtet, ist kein Kriterium: Ergebnis ohne Top 1, Top 3, Top 5 und je Coin ohne den grössten Gewinner muss ausgewiesen werden, mit der Anzahl der Coins und Zeitblöcke, die auch dann positiv bleiben.

Kein Kriterium auf CAGR, Sharpe oder MaxDD absolut. MaxDD wird gegen die exposure-gleiche Passivposition berichtet, nicht als Kriterium, weil ein 6.5-ATR-Stop Drawdowns von 17 bis 19 Prozent je Trade konstruktionsbedingt zulässt und die Frage dieser Stufe der Ertrag je Risiko ist, nicht die Drawdown-Form.

Teilweise bestanden: Kriterien 1 bis 5 in A (ohne BTC), aber 6 verfehlt. Das wäre der Befund «Edge existiert im Index, überlebt die Ausführung nicht». Verworfen: 1 oder 4 verfehlt in A.

## 9. Was nicht gemacht wird

Keine Parametersuche. Keine Auswahl von Coins nach Ergebnis. Keine Kombination mit Stufe-2-Varianten. Keine Short-Seite. Kein Regimefilter. Keine Anpassung von Sizing oder Kosten nach Kenntnis der Resultate. Kein zweiter Lauf auf denselben Daten.

## 10. Datenbedarf

CMC-Tageskerzen für die neun weiteren Coins (Loader `nachladen_cmc.py` mit CMC-IDs erweitern, Mac-Launcher). Kraken-Spot-Tageshistorie in USD für alle zehn Coins über die volle Zeit: Die REST-API liefert nur 720 Tage, die vollständige Historie gibt es als Kraken-Download-Archiv (OHLCVT-Zip) oder durch Aggregation der Trade-Historie über die API. Quelle: Kraken-Download-Archiv (Entscheidung 11.5), Prüfsummen der Archivdateien werden in den Ergebnissen festgehalten. Für Coins ohne Kraken-Historie im frühen Zeitraum beginnt B später als A, der Vergleich A gegen B wird nur auf der Überlappung geführt.

## 11. Entscheidungen (getroffen am 17.09.2026)

1. Klasse-3-Annahmen: Basis-Form wird eingefroren, der Freeze wartet nicht auf Backtester-Daten. Leg-Termine, die vor dem Freeze eintreffen, werden ausgewertet, spätere dienen als Out-of-Sample-Replikationskontrolle (Abschnitt 2).
2. Ebene A ohne Kosten, K0 als Zusatzzeile.
3. Nominal Initial Risk per Leg 2 Prozent des Sleeve-Startkapitals ohne Compounding für die Kriterien. Eingefroren, keine Variation.
4. Kriterienschwellen wie Abschnitt 8: Profit-Faktor 1.5, Retention 60 Prozent, abweichender Exit-Grund höchstens 15 Prozent, Kriterium 1 auf R_gesamt.
5. Kraken-Historie aus dem Download-Archiv, mit Prüfsummen.
6. B2 läuft als dritte Zeile, berichtet, nicht massgebend, in der Holm-Korrektur mitgezählt.
7. Jitter-Nachbarn werden gerechnet und berichtet, ohne Auswahlwirkung.

Zusätzlich: Ebene B mit handelbarer Konvention (erster handelbarer Kraken-Preis nach 00:00 UTC) für Kriterien, Same-Day-Close als Berichtswert. BTC Identifikationsmarkt ohne Validierungsgewicht. R_first und R_gesamt gleichrangig, Kriterien auf R_gesamt.

## 12. Ablauf nach Freeze

Prüfsumme dieses Dokuments und der Spezifikation v1 in `00_doku/ENTSCHEIDE.md`. Datenbeschaffung: CMC-Reihen der neun weiteren Coins, Kraken-Archiv für zehn Coins, je mit Prüfsummen. Umsetzung `mtp_val.py` mit Look-ahead-Test (Signale auf abgeschnittener Historie identisch) und Replikationskontrolle BTC (13 von 16) vor dem Volllauf. Ein Volllauf. Bericht in Markdown wie Stufe 2, dazu Fazit und Hypothesen. Kein zweiter Lauf auf denselben Daten.
