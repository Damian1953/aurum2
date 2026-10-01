# AURUM II — Accelerated Research Roadmap, Version 1.1

**Project Aurum II, `00_doku/AURUM_ACCELERATED_ROADMAP_v1.1.md`. Stand 17.09.2026, ersetzt Version 1. Änderungen gegenüber v1: Feld «Evidence class» je Zeile, BTC als Development-Markt, outcome-informed Varianten markiert, Regel v2 für «mechanistically promising», physisch getrennte Holdouts, Lane C parallel zu XRP und DOT, Visual AI ohne eigene Woche. Grundlage: `aurum_governance_evidence_v1.md`. Bestehende Freeze-Urteile unverändert. Erwartete Trades sind Schätzungen aus Zählungen, keine Outcomes.**

## 1. Sleeve-Tabelle

Evidence class: Development (Dev), Independent discovery (IndD), Holdout validation (HoldV), Forward validation (FwdV), Production eligible (Prod). Der Wert in der Spalte ist die Klasse, die der nächste Lauf höchstens erreichen kann, in Klammern die heute erreichte.

| Lane | Sleeve, Hypothese | Coin | Status | Evidence class | Nächster Lauf | Datenbedarf | Erwartete Trades | Validation | Production |
|---|---|---|---|---|---|---|---|---|---|
| A | YAMATO Stufe A, Y1 Failed Breakdown mit TA | BTC | not supported, Fast Fail (v1.1, 16 Signale) | Dev (Dev), abgeschlossen | keiner | vollständig | 16 | nein | nein |
| A | YAMATO Stufe A, Y2 Double Bottom | BTC | inconclusive (14 Signale) | Dev (Dev) | Stufe B Exit-Vergleich, outcome-informed | vollständig | 14 | nein | nein |
| A | YAMATO Stufe A, Y3 Wick plus Volumen mit TA | BTC | inconclusive (6 Signale, 1 Paar) | Dev (Dev) | Stufe B Trigger-Vergleich, outcome-informed | vollständig | 6, mit T0 bis 29 | nein | nein |
| A | YAMATO Stufe B, Trigger T0/TA/TB und Exit E-U/E-D/E-W, outcome-informed, Ebene C | BTC | Entwurf v0.1, vor Freeze | Dev, Deckel: höchstens Validation-Lauf auf BTC-Holdout | Freeze, Zählung, ein Lauf, Regel v2 | vollständig, Discovery-Datei | T0 auf Y1 70 bis 85 | nur nach positivem Lauf | nein |
| A | XRP-RTC Stufe A (X1, X2, X3, T0 primär, E-U und E-D) | XRP | Plan v0.4, vor Freeze | IndD, erster unabhängiger Generalisierungstest | Freeze vor Outcomes, Zählung, Matching, ein Lauf, Regel v2 | vollständig, Discovery-Datei | X1 mit T0 70 bis 110, X2 15 bis 25, X3 20 bis 40 | bei MP v2 mit ≥20 Trades oder formal supported | nein |
| A | DOT-RTC Stufe A (D1, D2, D3) | DOT | Plan v0.4, vor Freeze | IndD, zweiter unabhängiger Generalisierungstest | wie XRP | vollständig, Discovery-Datei | D1 mit T0 45 bis 75 | wie XRP | nein |
| A | ETH-RTC, SOL-RTC | ETH, SOL | Skizzen v0.1 | IndD, sofern Regeln nach XRP und DOT unverändert bleiben | Vorregistrierung nach XRP und DOT | vollständig, Discovery-Dateien vorhanden | ETH 90 bis 130 Kandidaten, SOL 70 bis 110 | nein | nein |
| B | BTC-MTP täglich (v1) | BTC | Referenz, kein unberührtes Fenster | FwdV als einzige mögliche Klasse | Forward-Fenster ab Freeze | vollständig | 1 bis 2 je Jahr | nur Forward | nein |
| B | BTC-B 4h Volatility Expansion | BTC | Plan v0.2, vor Freeze | Dev (Breakout-Engine wird auf BTC entwickelt) | Freeze mit gemeinsamer Engine, ein Lauf | vollständig | 20 bis 40 je Seite | nein | nein |
| B | DOT-A Compression Breakout, DOT-C verschachtelt | DOT | Plan v0.4 | IndD, wenn Engine vor DOT-Outcomes eingefroren | mit DOT-RTC | vollständig, OI ab 2021-12 | A 25 bis 45 je Seite, C 10 bis 20 | nein | nein |
| B | XRP-B, XRP-B+ | XRP | Plan v0.4 | IndD, wie DOT-A | mit XRP-RTC | vollständig | 20 bis 40 je Seite | nein | nein |
| C | D-CC Funding-Carry | 10 Coins | Stufe 2 bestanden, Datenvorbehalt | HoldV möglich (Regeln vor Kraken-Daten eingefroren) | Kraken-Funding-Tiefe prüfen (Loader), Vorregistrierung Kraken-Validation, Lauf | Kraken-Funding vor 2025-09 fehlt, Weg K1 dann K2 | Stufe 2: CC N Sharpe positiv | offen | nein |
| C | XS21 Cross-sectional | Universum | Stufe 2 bestanden, Survivorship-Vorbehalt | HoldV möglich | Universum aus S3-Listing (Loader), Point-in-Time-Vorregistrierung, Lauf | delistete Symbole, Weg U1 | Stufe 2 bestanden | offen | nein |
| C | Derivatives-Confirmation (RTC-1, RTC-2, DOT-C, XRP-B+) | 5 Coins | Library v0.1, Look-ahead bestanden | Klasse des jeweiligen Sleeves | in den Lane-A- und Lane-B-Läufen | Flow-Discovery-Dateien vorhanden | Teilmengen | mit dem Sleeve | nein |
| D | BTC Options Gamma Reversal | BTC | Notiz v0.1, vorgemerkt | Dev | nach den drei Lanes | Deribit-Ketten fehlen | offen | nein | nein |
| Quer | Visual AI Second Opinion | BTC zuerst | Rendering und Prompt v0.1 eingefroren, geringere Priorität | Inkrement, Klasse des Basis-Sleeves | nach den drei Discovery-Läufen und dem Lane-C-Befund | Modellwahl offen | 3 Aufrufe je Signal | nur als Inkrement | nein |
| Quer | Halving-Kontext | BTC, Alts exogen | Plan v0.1 | Bericht, keine Klasse | nach den Discovery-Läufen | vollständig | explorativ | nein | nein |

## 2. Was seit v1 dazugekommen ist

Governance v1 (`00_doku/aurum_governance_evidence_v1.md`): BTC ist Development-Markt, BTC Stufe B kann T0 und die neuen Exits nicht unabhängig bestätigen, XRP und DOT sind die ersten unabhängigen Tests, wenn ihre v1.0 vor Outcomes eingefroren wird. Outcome-informed Varianten (Y2 mit neuem Exit, Y3 mit T0, Trigger- und Exit-Familie auf BTC) tragen den Vermerk Ebene C, ein positives Ergebnis auf BTC-Discovery-Daten rechtfertigt höchstens einen Validation-Lauf. «Mechanistically promising» ist ab jetzt Regel v2 (mindestens drei von vier: Kontrolle in erwarteter Richtung mit Anteil positiver Paare ≥ 0.60, relevante MFE- oder Capture- oder Klassenverschiebung, keine Einzeltrade-Dominanz über 40 Prozent, gleiche Richtung in mindestens zwei Blöcken mit je fünf Paaren), Stufe A behält Status nach v1. Holdouts sind physisch getrennt (`02_daten/holdout/`, Manifest mit Prüfsummen, Loader-Sperre für Validation-Dateien ohne `AURUM_VALIDATION=1`). Lane C hat einen Loader und einen Beschaffungsvergleich (`02_daten/lane_c_data_procurement_v1.md`), Empfehlung: kostenloser Endpunkt zuerst, dann höchstens ein Monat CoinGlass, kein Tardis vor einer bestandenen Validation.

## 3. Reihenfolge der nächsten vier Wochen

Woche 1: Lane-C-Loader auf dem Mac ausführen (Minuten), Befund zu Funding-Tiefe und Universum. Entscheidungen zu XRP v0.4, DOT v0.4 und Stufe B v0.1, dann Freeze XRP v1.0, DOT v1.0, Stufe B v1.0 mit Prüfsummen in ENTSCHEIDE, Zählungen und Matching-Abdeckung auf den Discovery-Dateien, Umsetzungsentscheide, drei Discovery-Läufe mit Regel v2. Woche 2: Berichte und Statuszuweisung (BTC Stufe B als Dev mit Vermerk Ebene C, XRP und DOT als IndD), Cross-Coin-Bild als Bericht ohne Pooling, Validation-Kandidaten benennen. Parallel: D-CC-Kraken-Vorregistrierung und XS21-Point-in-Time-Vorregistrierung schreiben, bei Bedarf CoinGlass-Monat. Woche 3: BTC-B und Breakout-Engine Freeze und Lauf (Dev), ETH- und SOL-Vorregistrierung, Lane-C-Läufe (D-CC Kraken, XS21 Point-in-Time). Woche 4: erste Holdout-Validation eines Kandidaten mit Kraken-Ausführung und Kostenstress, eigenes Skript mit `AURUM_VALIDATION=1` und vorher eingefrorener Validation-Vorregistrierung. Visual AI erst danach, als Inkrement auf einer vorhandenen Signalliste.

## 4. Produktions-Anforderungen je Sleeve-Typ (unverändert aus v1)

Reversal-to-Trend (Lane A): 2 bis 12 Trades je Jahr je Coin, Turnover niedrig, Taker-Ausführung, Latenz Kerzenschluss plus Sekunden, Kraken Spot Long, Perp nur für Short-Spiegel, Slippage K1, Haltedauer Stunden bis Wochen, API OHLCV 4h plus Binance-Flow, Komplexität niedrig. Breakout (Lane B): 20 bis 40 je Seite je Jahr, Long Spot, Short Perp mit Funding, Komplexität mittel. Carry und Cross-sectional (Lane C): täglicher Turnover, Perp beidseitig, Funding zentral, Komplexität hoch. Maker-Ausführung ist eine eigene Execution-Hypothese in der Validation.

## 5. Regeln für alle Lanes

Jede Hypothese vor ihrem Outcome-Lauf eingefroren, Mehrdeutigkeiten vorher entschieden, Kandidatenzahlen dürfen bekannt sein, Outcomes nicht. Statusebenen nach Auswertungsregeln v1 mit Regel v2 für «mechanistically promising» ab diesem Datum. Fast Fail beendet die Spezifikation, Fast Promote erlaubt Validation, nicht Produktion. Coin-spezifische Auswertung, kein Pooling, Cross-Coin-Test erst nach gleichgerichteter Wirkung auf zwei Coins. Keine Parameteränderung nach Sicht auf Outcomes, neue Mechanik heisst neue Vorregistrierung mit Vermerk der Evidenzklasse. Discovery-Code lädt keine Validation-Datei. Produktion erst nach Holdout-Validation, Forward-Fenster und vollständigem Produktionsvermerk.
