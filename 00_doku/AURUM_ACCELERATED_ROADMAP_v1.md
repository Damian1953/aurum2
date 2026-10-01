# AURUM II — Accelerated Research Roadmap, Version 1

**Project Aurum II, `00_doku/AURUM_ACCELERATED_ROADMAP_v1.md`. Stand 17.09.2026 nach dem BTC-YAMATO-Stufe-A-Lauf. Grundprinzip: Discovery schnell und breit genug, Validation streng und eng, Produktion erst nach Validation. Drei parallele Lanes, jede Hypothese vor ihrem eigenen Outcome-Lauf separat eingefroren. Statusebenen: formal supported, mechanistically promising, no evidence (inconclusive oder Fast Fail). Bestehende Freeze-Urteile bleiben unangetastet. Alle Zahlen zu erwarteten Trades sind Schätzungen aus Zählungen, keine Outcomes.**

## 1. Stand der Sleeves

| Lane | Sleeve, Hypothese | Coin | Status | Nächster Lauf | Datenbedarf | Erwartete Trades (Discovery) | Validation | Production Readiness |
|---|---|---|---|---|---|---|---|---|
| A | YAMATO Stufe A, Y1 Failed Breakdown | BTC | not supported, Fast Fail (v1.1, 16 Signale, gepaart −0.34 R gegen Kontrollen) | keiner für v1.1 | vollständig | 16 | nein | nein |
| A | YAMATO Stufe A, Y2 Double Bottom | BTC | inconclusive, insufficient sample (14 Signale, gepaart +0.75 R, netto negativ, 85 Prozent Konzentration, 50 Prozent neue 20-Tage-Hochs) | Stufe B Exit-Vergleich auf denselben Einstiegen | vollständig | 14 | nein | nein |
| A | YAMATO Stufe A, Y3 Wick plus Volumen | BTC | inconclusive (6 Signale, 1 Kontrollpaar) | Stufe B Trigger-Vergleich (T0 liefert bis 29) | vollständig | 6, mit T0 bis 29 | nein | nein |
| A | YAMATO Stufe B, Trigger-Familie T0/TA/TB und Exit-Familie E-U/E-D/E-W | BTC | Entwurf v0.1, vor Freeze | Freeze, Zählung, ein Lauf | vollständig | T0 auf Y1 70 bis 85 | nein | nein |
| A | XRP-RTC Stufe A (X1, X2, X3, T0 primär, E-U und E-D) | XRP | Plan v0.4, vor Freeze | Freeze, Zählung, Matching, ein Lauf | vollständig (4h, 1h, Flow) | X1 mit T0 70 bis 110, X2 15 bis 25, X3 20 bis 40 | nein | nein |
| A | DOT-RTC Stufe A (D1, D2, D3) | DOT | Plan v0.4, vor Freeze | wie XRP | vollständig | D1 mit T0 45 bis 75 | nein | nein |
| A | ETH-RTC, SOL-RTC | ETH, SOL | Skizzen v0.1 | Vorregistrierung nach XRP und DOT | vollständig | ETH 90 bis 130 Kandidaten, SOL 70 bis 110 | nein | nein |
| B | BTC-MTP täglich (Spezifikation v1) | BTC | Referenz, kein unberührtes Fenster, kein Test | Forward-Fenster ab Freeze als einzige saubere Prüfung | vollständig | 1 bis 2 je Jahr | nur Forward | nein |
| B | BTC-B 4h Volatility Expansion | BTC | Plan v0.2, vor Freeze | Freeze mit gemeinsamer Breakout-Engine, ein Lauf | vollständig | 20 bis 40 je Seite | nein | nein |
| B | DOT-A 4h Compression Breakout, DOT-C verschachtelt | DOT | Plan v0.4, vor Freeze | mit DOT-RTC | vollständig, OI ab 2021-12 | A 25 bis 45 je Seite, C 10 bis 20 | nein | nein |
| B | XRP-B, XRP-B+ | XRP | Plan v0.4 | mit XRP-RTC | vollständig | 20 bis 40 je Seite | nein | nein |
| C | D-CC Funding-Carry (Stufe 2 bestanden mit Datenvorbehalt) | 10 Coins | Vorregistrierung Kraken-Validation offen | Kraken-Funding-Historie über ein Jahr abwarten oder Tardis Kraken Futures | Kraken-Funding fehlt vor 2025-09 | Stufe 2: CC N Sharpe positiv, Kraken-Vorzeichen 79 bis 88 Prozent | offen | nein |
| C | XS21 Cross-sectional (Stufe 2 bestanden mit Survivorship-Vorbehalt) | Universum | Point-in-Time-Vorregistrierung offen | Delisting-Universum beschaffen | delistete Coins fehlen | Stufe 2 bestanden | offen | nein |
| C | Derivatives-Confirmation (Inkremente RTC-1, RTC-2, DOT-C, XRP-B+) | 5 Coins | Library v0.1 umgesetzt, Look-ahead bestanden | in den Lane-A- und Lane-B-Läufen | Flow-Ausgaben vorhanden | als Teilmengen | mit dem jeweiligen Sleeve | nein |
| D | BTC Options Gamma Reversal | BTC | Notiz v0.1, vorgemerkt | nach den drei Lanes | Deribit-Ketten fehlen | offen | nein | nein |
| Quer | Visual AI Second Opinion | BTC zuerst | Rendering und Prompt v0.1 technisch vorbereitet, synthetisch geprüft | nach dem ersten Discovery-Lauf mit Signalliste | Modellwahl offen | 3 Aufrufe je Signal | nur als Inkrement | nein |
| Quer | Halving-Kontext | BTC, Alts als exogen | Plan v0.1 | Kontextaufteilung nach den Discovery-Läufen | vollständig | explorativ | nein | nein |

## 2. Was der erste Lauf gelehrt hat und was daraus in die Pläne einfliesst

Der BTC-Stufe-A-Lauf liefert drei Einsichten, die in XRP v0.4, DOT v0.4 und YAMATO Stufe B eingeflossen sind, ohne die eingefrorenen BTC-Regeln zu ändern: Die Bestätigungskerze (TA) kostet drei Viertel der Kandidaten und verbessert die Signale gegenüber Kontext-Kontrollen nicht, deshalb läuft T0 künftig als primärer Trigger mit TA und TB als Vergleiche. Der Chandelier 3 ATR14 auf 4h beendet Positionen nach im Median 12 bis 15 Kerzen, während die Böden (vor allem Double Bottoms) in der Hälfte der Fälle Wochen später neue Hochs erreichen, deshalb läuft ein Exit auf Tages-ATR als zweite Baseline. Die Basisrate von 4h-Bounces nach Selloffs ist negativ, deshalb ist die gematchte Kontrollgruppe Teil jedes primären Tests.

## 3. Reihenfolge der nächsten vier Wochen

Woche 1: Freeze XRP v1.0 und DOT v1.0 (nach Bestätigung der je fünf offenen Entscheidungen), Freeze YAMATO Stufe B v1.0, Zählungen und Matching-Abdeckung auf allen drei, Umsetzungsentscheide dokumentieren, dann die drei Discovery-Läufe. Woche 2: Berichte, Statuszuweisung, Cross-Coin-Bild (nur Bericht, kein Pooling), Entscheid über Validation-Kandidaten (Fast Promote) und Fast Fails. Woche 3: BTC-B und Breakout-Engine Freeze und Lauf, Visual-AI-Modellwahl und Zeitpunktliste aus den Discovery-Signalen, ETH- und SOL-Vorregistrierung. Woche 4: erste Validation eines Fast-Promote-Kandidaten auf dem Holdout mit Kraken-Ausführung, Lane C: Kraken-Funding-Stand und Delisting-Universum prüfen.

## 4. Produktions-Anforderungen je Sleeve-Typ (Bericht, wird je Strategie gefüllt)

Reversal-to-Trend (Lane A): 2 bis 12 Trades je Jahr je Coin, Turnover niedrig, alle Ausführungen Taker (Eröffnung, Stop), Latenz Kerzenschluss plus Sekunden, Kraken Spot Long, Perp nur für Short-Spiegel, kein Funding auf Spot, Slippage K1, Positionsdauer Stunden bis Wochen, API OHLCV 4h plus Binance-Flow-Feed, Komplexität niedrig. Breakout (Lane B): 20 bis 40 je Seite je Jahr, Long Spot, Short Perp mit Funding, Komplexität mittel. Carry und Cross-sectional (Lane C): täglicher Turnover, Perp beidseitig, Funding zentral, Komplexität hoch. Maker-Ausführung: Limit-Orders an der Eröffnung statt Market-Orders sind eine eigene Execution-Hypothese mit Fill-Risiko, sie wird in der Validation als Variante geführt, nicht in der Discovery.

## 5. Regeln, die für alle Lanes gelten

Jede Hypothese vor ihrem Outcome-Lauf eingefroren, technische Mehrdeutigkeiten vorher dokumentiert und entschieden, Kandidatenzahlen dürfen vor dem Lauf bekannt sein, Outcomes nicht. Drei Statusebenen nach Auswertungsregeln v1, Fast Fail beendet die Spezifikation, nicht die Mechanik, Fast Promote erlaubt Validation, nicht Produktion. Coin-spezifische Auswertung, kein Pooling zur Signifikanzerzeugung, Cross-Coin-Test erst nach gleichgerichteter Wirkung auf zwei Coins. Keine Parameteränderung nach Sicht auf Outcomes, neue Mechanik heisst neue Vorregistrierung. Produktion erst nach bestandener Validation auf dem Holdout mit Kraken-Ausführung und Kostenstress.
