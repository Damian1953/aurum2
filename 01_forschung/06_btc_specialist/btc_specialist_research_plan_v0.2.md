# BTC Specialist — Forschungsplan, Version 0.2

**Project Aurum II, Forschungsstrang 06_btc_specialist. 17.09.2026. Status: Plan zur Prüfung. Kein Rechenlauf, kein Freeze. Version 0.1 war der Abschnitt «BTC Trend» im Architektur-Update v1, dieser Plan ersetzt ihn. Alle Freeze-Urteile bleiben unangetastet, insbesondere das Urteil «verworfen» der MTP-Validierung auf neun Coins.**

## 0. Zweck und Vorbelastung

BTC erhält drei getrennte Forschungsfragen mit drei getrennten Engines, die nicht gegeneinander ausgewählt werden: BTC-MTP (tägliche Trendfolge nach der rekonstruierten Woo-Spezifikation v1), BTC-B (4h Volatility Expansion) und BTC-RTC (Reversal-to-Trend Capture nach dem Framework v0.1). Die Frage ist nicht, welche die beste ist, sondern ob die drei unterschiedliche Trade-Ereignisse und Zeithorizonte erfassen und später komplementär sein könnten.

Vorbelastung, offen ausgewiesen. BTC ist der Identifikationsmarkt der MTP-Rekonstruktion: Die Spezifikation v1 wurde aus 16 öffentlichen BTC-Trades rekonstruiert, ihre Replikationskontrolle lief auf BTC, und der Validierungslauf hat BTC auf der A-Ebene bis 2026 mitgerechnet (als Bericht, nicht als Kriterium: 1.04 R je Trade, Profit-Faktor 6.8, über allen anderen Coins). Das negative Cross-Coin-Ergebnis beendet BTC-Trendfolge nicht, weil die Kombination «MTP auf BTC allein» nie ein Test war. Aber: Es gibt für BTC-MTP kein unberührtes Datenfenster, weder vor noch nach 2024. Deshalb kann BTC-MTP in diesem Plan keinen Sleeve-Status erreichen. Es bleibt Referenz, Ereignisquelle für die Komplementaritäts- und Halving-Analyse, und Kandidat für ein Forward-Fenster ab dem Freeze-Datum, das die einzige saubere Prüfung wäre. Die Hypothese aus der MTP-Validierung (Exposure-Steuerung statt Alpha je Trade) bleibt ein eigener, hier nicht bearbeiteter Strang.

Weitere Vorbelastung: Stufe 2 hat auf BTC die Woo-Varianten W0 bis W8, MR, TS und XS21-Anteile gerechnet (Tagesbasis), Stufe 1 Regime-Labels. Keine dieser Konstruktionen ist eine 4h-Kompression oder ein 4h-Reversal. Sie zählen in der DSR-Trial-Zahl als Vorbelastung des Coins (Abschnitt 8), nicht als Veto.

## 1. Drei Engines

**BTC-MTP, täglich.** Spezifikation v1, unverändert (Wilder-ATR 180, SMA200-Filter, Pivot 5/1 mit Alter 20 bis 365, Stop 6.5 ATR, Ziel 37.5 ATR, Add-on 1.5 ATR, Ausführung Ebene B). Kein neuer Test, keine Kriterien. Berichtet werden die Trades auf BTC (A und B) als Referenzlinie und als Ereignisliste. Horizont: Wochen bis Monate.

**BTC-B, 4h Volatility Expansion.** Identische Definition wie DOT-A und XRP-B (eine Engine, drei Coins): Kompression, wenn `kelt_pct` unter 0.20 liegt (Keltner-Breite 4 · ATR20 / EMA20 unter ihrem 20-Prozent-Perzentil der letzten 1080 Kerzen, 180 Tage) auf mindestens einer der letzten 30 Kerzen (fünf Tage). Expansion: Schluss über dem höchsten Hoch der letzten 120 Kerzen ohne die aktuelle (20 Tage) für Long, unter dem tiefsten Tief für Short. Einstieg zur Eröffnung der Folgekerze, Stop Chandelier 3 · ATR20 vom höchsten Schluss seit Einstieg, nachgezogen, nie gesenkt, kein Ziel. Kein gleitender Durchschnitt als Filter. Horizont: Tage bis Wochen. Tagesbasis als Robustheitsvariante (Fenster 20 Tage, 180 Tage, wie in den v0.1-Plänen).

**BTC-RTC, 4h.** Bottom Entry Engine mit den Familien RTC-CR (Candle Reversal) und RTC-FB (Failed Breakdown, priorisiert), Trigger T0, TA, TB (später T1h), Hold Engine, Peak Evidence Engine mit P12 (Kaufklimax) und P13 (Failed Breakout) nach Framework v0.1, Ebenen RTC-0 bis RTC-2 (RTC-3 nur mit Liquidationsquelle), Exits E0, E1, E2, 8h als Robustheit, Kerzengrenzen-, Cross-Venue- und Capture-Efficiency-Diagnosen. Keine BTC-spezifische Abweichung von den Framework-Zahlen. Horizont: Tage (E0) bis Wochen (E1, E2).

## 2. Komplementaritätsanalyse (Bericht, kein Test)

Auf dem Discovery-Fenster: Überlappung der Haltezeiten je Engine-Paar (Anteil der Kerzen, an denen beide long sind), Korrelation der täglichen Sleeve-Renditen, zeitliche Lage der RTC-Einstiege relativ zu MTP- und B-Einstiegen (wie viele Tage vor oder nach einem Trend-Einstieg liegt der Reversal-Einstieg desselben Trends), Verteilung der Haltedauern, Anteil der Marktbewegungen über 20 Prozent, die jede Engine erfasst hat, und die keine erfasst hat. Ergebnis ist eine Tabelle, die zeigt, ob die drei Engines dieselben oder verschiedene Ereignisse handeln. Keine Auswahl, keine Gewichtung. Die Gewichtung ist Sache des Portfolio-Layers, der erst nach zwei bestandenen Sleeves entworfen wird.

## 3. Halving

Nach `halving_context_research_plan_v0.1.md`: `days_since_halving`, `days_to_next_expected_halving`, `cycle_phase` als Kontext für die Trades aller drei Engines, explorativ, ohne Filterwirkung. BTC ist der einzige Coin, bei dem das Halving coin-eigen ist.

## 4. Daten

Vorhanden: CMC täglich ab 2013, Kraken 1d Archiv plus API ab 2013 (dünn bis 2015), Binance Spot 1d ab 2017-08, Perp ab 2019-09, Funding ab 2019-09, OI täglich ab 2021-01, Bitstamp und Coinbase täglich (nur für MTP). Wird geladen: Binance Spot und Perp 4h mit allen Spalten ab 2017-08 beziehungsweise 2019-09, Kraken 240 aus dem Archiv. Danach nachzuladen: Binance Spot und Perp 1h, Kraken 60 aus dem Archiv, Binance-Metrics-Aggregation für 4h-OI, OKX-Kerzen ab 2023-07. Discovery-Fenster für 4h-Engines: 2017-08 bis 2023-12 (rund 6.4 Jahre, rund 14000 Kerzen), Holdout 2024-01 bis Datenende. Für BTC-MTP kein Holdout (Abschnitt 0). BTC-Kraken-240 hat in der Frühphase Lücken, B-Start-Regel.

## 5. Kosten und Ausführung

Wie Framework Abschnitt 15 und die v0.1-Pläne: K0 bis K2, tatsächliches Funding für Perp-Seiten, Long-Seiten auf Kraken Spot (Ebene B mit erstem handelbaren Preis nach der Kerzengrenze), Short-Seiten auf Perp-Daten mit Kraken-Perp-Sätzen und Vermerk, Cash zum T-Bill-Satz. Sicht 1.

## 6. Tests (Discovery)

Primäre Familie je Engine, Holm innerhalb der Engine:

BTC-B: B-L, B-S (H0: keine Erwartung über exposure-gleicher Passivposition).
BTC-RTC: T1-CR, T1-FB (RTC-0, E1, Long), T2 (E2 gegen E1, gepaart), T3 (E0 gegen E1, gepaart). Hypothesen-Familie H1 (Wick mal Volumen), H2 (FB gegen CR), H3a, H3b (Trigger), H3c (1h-Bestätigung, sobald 1h-Daten vorliegen). Inkrement-Familie I1, I2, P-Inc. Tertiär Short-Spiegel.

BTC-MTP: keine Tests.

Discovery-Kriterium «Signal vorhanden» nach Framework Abschnitt 13. Engines, die es erreichen, gehen in die Validation auf dem Holdout mit den neun Kriterien. Die Komplementaritätsanalyse läuft unabhängig davon auf allen drei.

## 7. Look-ahead

Framework Abschnitt 16, dazu: BTC-MTP-Trades stammen aus dem Validierungslauf und sind bis 2026 bekannt, sie werden in der Komplementaritätsanalyse nur auf dem Discovery-Fenster verwendet, damit die Analyse keine Holdout-Information für die anderen Engines trägt.

## 8. Multiplizität

DSR-Trial-Zahl für BTC: 2 Tests BTC-B plus 12 bis 14 Tests BTC-RTC plus Jitter plus Vorbelastung (Stufe 2: 9 Woo-Varianten, 3 MR, 3 TS, 4 D-Familien auf BTC, Stufe 1: 7 Regime-Tests, MTP: 1), also 14 bis 16 plus Jitter plus 27, als konservative Sensitivität. Keine Auswahl nach CAGR.

## 9. Offene Entscheidungen vor dem Freeze

1. BTC-MTP als reine Referenz ohne Kriterien (Empfehlung, aus den Gründen in Abschnitt 0) oder mit Forward-Fenster ab Freeze als eigene Stufe.
2. Discovery-Beginn für BTC-B und BTC-RTC 2017-08 (Binance-Beginn) bestätigen, obwohl Kraken-240 früher reicht (Kraken ist Ausführungs-, nicht Signalquelle).
3. Ob BTC-B auf 4h (Empfehlung, gleiche Engine wie DOT-A) oder auf Tagesbasis primär läuft.
4. Halving-Analyse nach der Discovery (Empfehlung) oder vorher mit MTP-Trades allein.
5. Framework-Entscheidungen 1 bis 14 gelten auch hier.

Nach Klärung: Version 1.0, Prüfsumme in ENTSCHEIDE, gemeinsam mit Framework, Feature Library und den XRP- und DOT-Plänen eingefroren.
