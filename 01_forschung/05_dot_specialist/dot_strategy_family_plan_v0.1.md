# DOT Specialist — Strategiefamilien-Plan, Version 0.1

**Project Aurum II, Forschungsstrang 05_dot_specialist. 17.09.2026. Status: Plan zur Prüfung. Kein Rechenlauf, keine Optimierung. Freeze-Urteile der Stufen 1, 2 und der MTP-Validierung bleiben unberührt.**

## 0. Zweck und Abgrenzung

Primäre Frage: Welche Strategiefamilie besitzt auf DOT überhaupt stabile Evidenz? Nicht: welche Parameter sind optimal. Drei Familien werden mit je einem vorab gesetzten Parametersatz unter identischen Daten, Kosten, Slippage, Zeitblöcken und Sizing-Regeln gegeneinander gestellt (Head-to-Head). Erst wenn eine Familie robust besteht, darf eine getrennte Version 2 Parameter und Ausführung verfeinern.

Vorbelastung, offen ausgewiesen: DOT war in Stufe 2 bei fast allen Woo-Varianten negativ (W2 Long minus 10 Prozent CAGR, W6 minus 6, Mean Reversion Long minus 10 Prozent), in der MTP-Validierung mit sechs Trades, null Gewinnern und minus 0.75 R der schwächste Coin. Tägliche Trendfolge auf DOT ist damit dreimal geprüft und dreimal gescheitert. Ein breiter externer Strategietest zeigt, dass viele scheinbar gute historische DOT-Setups nach Auswahlkorrektur nicht standhalten. Die Konsequenz ist ein besonders enger Freiheitsgrad: drei Familien, drei Parametersätze, sechs primäre Tests, keine Gitter, und die Deflated Sharpe Ratio wird mit einer Trial-Zahl geführt, die die externen Vorversuche einrechnet (Abschnitt 9).

DOT hat zudem die kürzeste Historie im Universum (Binance ab 2020-08-18, Kraken ab 2020-08-18, Perp und Funding ab 2020-08-20, OI ab 2021-12-01). Block P1 ist für DOT nur das letzte Drittel von 2020. Die Trade-Mindestzahlen werden dadurch schwerer erreichbar, das ist so hinzunehmen, nicht durch Lockerung zu umgehen.

## 1. Marktstruktur-Hypothese

Ausgangsvermutung: DOT produziert viele Fehlausbrüche. Preisausbrüche über Mehrwochen-Hochs kehren häufig innerhalb weniger Tage um, während echte Expansionsphasen (Ende 2020, 2021, kurz Ende 2024) von steigendem Open Interest und Volumen begleitet sind. Funding läuft in Ausbrüchen schnell ins Extrem, was Ausbrüche schwächt, die von Perp-Longs getrieben sind. Wenn das stimmt, unterscheiden OI, Volumen und Funding echte Expansion von crowd-getriebenen Fehlsignalen, und die Familie C (perp-bestätigter Ausbruch) sollte gegenüber A (reiner Ausbruch) eine höhere Trefferquote bei ähnlicher Erwartung je Gewinner zeigen.

Deskriptive Vorprüfung ohne Auswahlwirkung, nach dem Freeze, vor dem Strategielauf: Anteil der 20-Tage-Ausbrüche, die innerhalb von fünf Tagen unter das Ausbruchsniveau zurückfallen (DOT gegen BTC, ETH, SOL auf derselben Definition), Verteilung von ΔOI_5d und Volumenverhältnis an Ausbruchstagen, Funding-z an Ausbruchstagen, Autokorrelation der Tagesrenditen. Ergebnis ist Bericht, ändert keine Parameter.

## 2. Strategiefamilien

**DOT-A, Volatility Breakout, Tagesbasis primär, 4h Robustheit.** Kompression: Keltner-Kanal-Breite (EMA20 ± 2 ATR20) relativ zum Mittelband liegt unter dem 20-Prozent-Perzentil ihrer letzten 180 Tage. Expansion: Schluss über dem Donchian-Hoch der letzten 20 Tage (ohne aktuellen Tag), Kompression an mindestens einem der letzten fünf Tage. Kein gleitender Durchschnitt als Filter, kein Crossover. Einstieg zur Eröffnung des Folgetages, Stop Chandelier 3 mal ATR20 vom höchsten Schluss, nachgezogen, kein Ziel. Short spiegelbildlich unter dem Donchian-Tief.

**DOT-B, Mean- und Order-Flow-Reversion, Tagesbasis.** Gleichgewicht: EMA20 der Tagesschlüsse (VWAP20 als Robustheitsvariante, sofern Volumen sauber). Überdehnung: z = (Close − EMA20) / ATR20 ≤ −2.5 (Long) oder ≥ +2.5 (Short). Exit bei z-Vorzeichenwechsel oder nach 10 Tagen, Stop 2 mal ATR20 vom Einstieg, fix. Order-Flow-Proxy als vorregistrierter Filter, nicht als Bedingung: Taker-Kaufanteil (Taker-Buy-Volumen geteilt durch Volumen, Binance-Kline-Spalte) am Signaltag unter 0.40 für Long-Einstiege (Verkaufsdruck erschöpft) gegen darüber. Der Proxy ist nur verfügbar, wenn die Klines mit allen Spalten nachgeladen sind, sonst entfällt der Filter fail-closed.

**DOT-C, Perp-bestätigter Breakout, Tagesbasis.** Preisausbruch wie DOT-A (Donchian 20, ohne Kompressionsbedingung, damit C nicht A plus Filter ist, sondern die Bestätigung an die Stelle der Kompression tritt) PLUS drei Bedingungen am Signaltag, alle vorab gesetzt und ökonomisch begründet:

- ΔOI_5d ≥ +10 Prozent (neues Kapital kommt in die Bewegung, nicht Umschichtung),
- Volumen des Signaltages ≥ 1.5 mal Mittel der letzten 20 Tage (Expansion wird gehandelt, nicht nur notiert),
- Funding-z (90 Tage) ≤ +1.5 für Long (die Bewegung ist noch nicht von Perp-Longs überfüllt), ≥ −1.5 für Short.

Alle drei müssen erfüllt sein. Kein Gitter über die Schwellen. Jitter-Nachbarn: ΔOI 5 und 15 Prozent, Volumen 1.25 und 2.0, Funding-z 1.0 und 2.0, je einzeln variiert. Stop und Exit wie DOT-A. Weil OI erst ab 2021-12-01 vorliegt, beginnt DOT-C an diesem Datum, und der Head-to-Head-Vergleich A gegen B gegen C wird auf zwei Fenstern geführt: dem gemeinsamen Fenster ab 2021-12-01 (massgebend für den Vergleich) und je Familie auf ihrer vollen Historie (Bericht).

## 3. Exakte minimale Inputs

| Grösse | Definition | Bekannt am |
|---|---|---|
| EMA20, ATR20 (Wilder) | Tagesschlüsse, True Range | Tagesschluss |
| Keltner-Breite, Perzentil 180 Tage | (4 ATR20) / EMA20, rollendes Perzentil nur Vergangenheit | Tagesschluss |
| Donchian 20 | höchstes Hoch, tiefstes Tief der letzten 20 Tage ohne aktuellen Tag | Vortag |
| z (B) | (Close − EMA20) / ATR20 | Tagesschluss |
| VWAP20 (B-Robustheit) | Summe Close mal Volumen / Summe Volumen, 20 Tage | Tagesschluss |
| Taker-Kaufanteil (B-Filter) | Taker-Buy-Volumen / Volumen, Binance-Kline | Tagesschluss |
| ΔOI_5d (C) | OI_t / OI_{t−5} − 1, Tageswerte 00:00 UTC | Schnappschuss 00:00 des Folgetages zählt für den Folgetag |
| Volumenverhältnis (C) | Volumen_t / Mittel(Volumen_{t−20..t−1}) | Tagesschluss |
| Funding-z (C, Filter) | z der 8h-Rate über 90 Tage, zuletzt abgerechnete Rate | Settlement |
| Basis | (Perp − Spot) / Spot, Tagesschluss | Tagesschluss, Bericht |

## 4. Datenbedarf und Datenstand

**Vorhanden:** Binance Spot DOTUSDT Tageskerzen ab 2020-08-18 (OHLCV), Binance Perp ab 2020-08-22, Funding 8h ab 2020-08-20 bis 2026-08-31, OI täglich ab 2021-12-01, Kraken Spot ab 2020-08-18 (Archiv plus API), CMC ab 2020-08-20. Alle mit Prüfsummen.

**Nachzuladen vor dem Freeze:** Binance Spot und Perp Tageskerzen mit allen zwölf Spalten (Taker-Buy-Volumen, Trades), Binance 4h-Kerzen für die DOT-A-Robustheitsvariante, Kraken 240-Minuten aus dem Archiv, Funding September 2026 sobald publiziert. Volumen für DOT-C aus Binance Spot (Signalquelle), Kraken-Volumen als Gegenprobe.

**Fail-closed:** DOT-C nur ab 2021-12-01. Order-Flow-Filter nur, wenn Taker-Volumen vollständig vorliegt. Keine Rekonstruktion von OI vor 2021-12 aus anderen Quellen. Fehlende Tageswerte machen den betreffenden Tag für den jeweiligen Filter «nicht auswertbar».

**Abdeckung:** rund sechs Jahre, Blöcke P1 (2020-08 bis 2020-12, nur Bericht, zu kurz für Kriterien), P2 2021 bis 2023, P3 ab 2024. Kriterium 2 (Zeitblöcke) wird für DOT als «beide vollen Blöcke P2 und P3 positiv» formuliert.

## 5. Look-ahead-Risiken

Wie XRP-Plan Abschnitt 5, dazu spezifisch: Das Volumenverhältnis in DOT-C verwendet das Volumen des Signaltages, das erst am Tagesschluss vollständig ist, deshalb Einstieg zur Eröffnung des Folgetages, nie intraday. ΔOI_5d verwendet den OI-Schnappschuss um 00:00 UTC, der dem Vortag zugeordnet wird, also ist ΔOI am Signaltag t die Veränderung bis 00:00 des Tages t, nicht t+1. Perzentile der Keltner-Breite nur aus der Vergangenheit. Keine Verwendung der Kraken-Frühphase 2020 als Ausführungsbasis (B-Start-Regel). Look-ahead-Test mit abgeschnittener Historie (30.06.2023) für alle drei Familien.

## 6. Kostenmodell

Identisch für alle drei Familien, das ist die Voraussetzung des Head-to-Head: Perpetual-Modell K0 bis K2 wie Stufe 2 mit tatsächlichem Funding, Spot-Modell für Long-Seiten als Zusatzzeile, Ebene B mit Kraken-Spot-Ausführung für Long-Seiten (Einstieg erster handelbarer Preis der Folgekerze, Stop-Market mit Slippage). Short-Seiten auf Binance-Perp-Daten mit Kraken-Perp-Sätzen und Vermerk. Cash zum T-Bill-Satz. Kostenquote und Turnover je Familie ausgewiesen.

## 7. Long- und Short-Logik

Jede Familie Long-only, Short-only, Long+Short (0.5 und 0.5). Keine Symmetrieannahme. DOT-C Short verlangt ΔOI_5d ≥ +10 Prozent (steigendes OI in einen Abwärtsausbruch heisst: Shorts kommen hinzu), Volumen ≥ 1.5 und Funding-z ≥ −1.5. Funding-Belastung nach tatsächlicher Rate je Seite.

Der Vergleich A gegen C ist der Kern: gleicher Ausbruch, einmal mit Kompression, einmal mit Perp-Bestätigung. Berichtet wird zusätzlich die Schnittmenge (Ausbrüche, die beide Bedingungen erfüllen) und die Differenz (nur A, nur C), damit sichtbar wird, ob die Bestätigung Fehlausbrüche entfernt oder nur Trades reduziert.

## 8. Robustheitskriterien

Bestanden gilt je Familie und Seite unter K1, Tagesbasis, Sicht 1 (initialer Stop riskiert 2 Prozent des Sleeve-Startkapitals, kein Compounding), auf der vollen Historie der Familie:

1. Erwartung je Trade netto grösser null, CAGR über Cash, Profit-Faktor mindestens 1.3.
2. Beide vollen Zeitblöcke P2 und P3 mit positiver Erwartung.
3. Jitter-Region: mindestens zwei Drittel der Nachbarn positiv, Sharpe der Basis höchstens 1.5 mal Nachbar-Median. Nachbarn: A Perzentil 10/30, Donchian 15/30, Stop 2.5/3.5. B z 2.0/3.0, EMA 15/30, Halten 7/14. C wie Abschnitt 2.
4. Trade-Mindestzahl: A Klasse M (mindestens 30 Trades je Seite auf sechs Jahren, Vermerk «geringe Basis» unter 60), B Klasse S (mindestens 60), C Klasse M (mindestens 20 ab 2021-12, Vermerk «geringe Basis»).
5. MaxDD nicht schlechter als exposure-gleiche Passivposition.
6. Beta-Trennung: Alpha- oder Risikotransformations-Teiltest.
7. Bootstrap-5-Prozent-Perzentil grösser null und Holm-p unter 0.05 in der Familie von sechs Tests.
8. Kostenstress: Vorzeichen unter K2 erhalten.
9. Edge-Retention Kraken (Long): mindestens 60 Prozent, abweichender Exit-Grund höchstens 15 Prozent.

Head-to-Head-Regel: Eine Familie hat «stabile Evidenz», wenn sie alle neun Kriterien auf mindestens einer Seite besteht. Bestehen mehrere, wird keine ausgewählt, alle gehen in Version 2. Besteht keine, ist die Antwort auf die primäre Frage «keine», und es gibt keine Version 2 mit gelockerten Kriterien. Der Vergleich der Kennzahlen zwischen Familien (Erwartung, Profit-Faktor, R-Verteilung, Trefferquote, Konzentration) wird berichtet, entscheidet aber nicht, weil DOT-C ein kürzeres Fenster hat.

Berichtet: R-Multiples, Sortino, Recovery, Exposure, Haltedauer, Konzentration, Ergebnis ohne grössten Gewinner, Kostenquote, 4h-Robustheit (A), VWAP-Robustheit (B), Order-Flow-Filter (B), Schnittmengen A/C, Referenzlinien MTP v1 und W2 auf DOT (aus Stufe 2 und MTP-Validierung bekannt, ohne neue Tests).

## 9. Nullhypothesen und Multiple Testing

H0-A: Ausbruch nach Kompression erzeugt auf DOT nach K1 keine Erwartung über der exposure-gleichen Passivposition, weder Long noch Short.
H0-B: Rückkehr zum Gleichgewicht nach Überdehnung erzeugt keine solche Erwartung.
H0-C: Perp-bestätigte Ausbrüche erzeugen keine solche Erwartung, und ihre Trefferquote ist nicht höher als die unbestätigter Ausbrüche (zweiter Teil als Bericht mit Trade-Bootstrap der Differenz).
H0-Filter (B, Order-Flow): Taker-Kaufanteil unter 0.40 verändert die Erwartung der Long-Einstiege nicht.

Primäre Familie für Holm: sechs Tests (A-L, A-S, B-L, B-S, C-L, C-S). Long+Short-Kombinationen sind abgeleitet und keine eigenen Tests. Deflated Sharpe Ratio mit zwei Trial-Zahlen: 6 (diese Stufe) und 6 plus Jitter plus die 15 DOT-Tests der Woo-Matrix aus Stufe 2 plus 3 aus Familie B Stufe 2 plus 1 MTP-Validierung, also 25 plus Jitter, als konservative Sensitivität, die einrechnet, dass DOT bereits mehrfach getestet wurde. Externe Vorversuche Dritter sind nicht zählbar, aber der Grund, warum die Trade-Mindestzahlen und die Blockregel hier nicht gelockert werden.

## 10. Offene Entscheidungen vor dem Freeze

1. Datennachladen: Binance Tages- und 4h-Kerzen mit allen Spalten, Kraken 240-Minuten aus dem Archiv. Empfehlung: ja, vor dem Freeze.
2. DOT-C ohne Kompressionsbedingung (Empfehlung, damit A und C zwei Familien sind) oder mit (dann ist C ein Filter auf A und gehört in die Filter-Familie).
3. Die drei Schwellen von DOT-C (ΔOI 10 Prozent, Volumen 1.5, Funding-z 1.5) bestätigen. Änderungen nur vor dem Freeze.
4. Primäre Zeitebene Tag für alle drei Familien (Empfehlung) oder 4h für A.
5. Trade-Mindestzahlen (30 / 60 / 20) und Blockregel «P2 und P3 positiv» bestätigen.
6. Profit-Faktor-Schwelle 1.3 bestätigen.
7. Ob VWAP20 als Robustheitsvariante von B mitläuft (braucht Volumen, Empfehlung: ja, Bericht).
8. Ob der Head-to-Head auf dem gemeinsamen Fenster ab 2021-12 oder auf der vollen Historie je Familie geführt wird. Empfehlung: Kriterien auf voller Historie je Familie, Vergleichstabelle auf dem gemeinsamen Fenster.
9. Trial-Zahl der DSR-Sensitivität (25 plus Jitter) bestätigen.

Nach Klärung: Version 1.0, Prüfsumme in ENTSCHEIDE, Datenbeschaffung, Look-ahead-Test, deskriptive Vorprüfung, ein Volllauf. Version 2 nur für eine Familie, die alle Kriterien besteht, mit eigener Vorregistrierung.
