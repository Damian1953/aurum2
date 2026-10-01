# XRP Specialist — Vorregistrierungsplan, Version 0.3

**Project Aurum II, Forschungsstrang 04_xrp_specialist. 17.09.2026. Status: Plan zur Prüfung. Kein Rechenlauf, kein Freeze. Ersetzt Version 0.1 (Version 0.2 nicht vergeben, die Vorgabe vom 17.09.2026 ist die Revision). Alle Freeze-Urteile der Stufen 1, 2 und der MTP-Validierung bleiben unangetastet. Dieser Plan setzt `rtc_reversal_to_trend_framework_v0.1.md` und `candlestick_flow_feature_library_spec_v0.1.md` voraus und hält nur XRP-spezifische Festlegungen fest.**

## 0. Zweck und Abgrenzung

Forschungsfrage: Liegt der XRP-spezifische Edge nicht in der kurzfristigen Rückkehr zum Mittelwert, sondern im frühen Einfangen eines bestätigten Bodens, aus dem gelegentlich ein grosser Trend entsteht? Und daneben: Erzeugt ein 4h-Kompressionsausbruch auf XRP eine Erwartung, die die Kriterien erreicht?

Was sich gegenüber v0.1 ändert: XRP-A (reine 4h Mean Reversion mit Exit am Vorzeichenwechsel) ist keine Endstrategie mehr. Ihr Exit-Prinzip lebt als Kontrollarchitektur E0 weiter (identischer Einstieg, Exit am kurzfristigen Gleichgewicht), damit die Frage «Reversion oder Trend Capture» direkt und gepaart beantwortet wird. XRP-C (Hybrid nach Efficiency Ratio) entfällt, weil die Hold Engine des RTC die kontinuierliche Anpassung an die Marktphase bereits leistet (in einer Range endet der Trade am Chandelier oder an Peak-Evidenz, in einem Trend läuft er) und ein zusätzlicher Gewichtungsmotor Freiheitsgrade ohne neue Hypothese wäre. XRP-B (Volatility Breakout) wechselt auf 4h primär mit der coin-übergreifend identischen Engine (BTC-B, DOT-A), Tagesbasis wird Robustheitsvariante. Die Derivate-Filter F1 bis F3 werden durch die inkrementellen Ebenen RTC-1 bis RTC-3 und die verschachtelte Bestätigung des Breakouts ersetzt, die dieselben Fragen präziser stellen.

Vorbelastung, offen ausgewiesen: Stufe 2 hat eine tägliche Mean Reversion (z20 ±2, Exit SMA20, Stop 3 ATR, 10 Bars) auf XRP Long mit 5 Prozent CAGR bei Sharpe 0.3 gerechnet, Short negativ, und verworfen. In der MTP-Validierung war XRP der einzige geeignete Coin mit positiver Erwartung in Ebene B (0.91 R_gesamt, 10 Trades). Nach der methodischen Regel des Frameworks (Abschnitt 1) gilt: Die schwache tägliche MR widerlegt keine 4h-Reversal-Hypothese mit Trend-Hold, weil Zeitebene, Signal (Kontext plus Umkehrmuster plus Flow statt z-Score) und Exit (Chandelier statt Mittelwert) andere sind. Sie ist Vorbelastung in der Trial-Zahl. Die frühere Formulierung «keine XRP-A-Variante 2» wird ersetzt durch: Scheitert XRP-RTC in der eingefrorenen Form, gibt es keine Parametervariante von XRP-RTC. Eine neue Mechanik auf XRP bleibt zulässig.

## 1. Marktstruktur-Hypothese

Unverändert aus v0.1: lange Range- und Konsolidierungsphasen mit scharfen kurzfristigen Umkehrungen, seltene sehr starke Expansionsphasen (2017, Ende 2020, 2021, Ende 2024), tiefer Perp-Markt mit zeitweise stark divergierendem Funding. Neu ist die Präzisierung, die RTC prüft: Die scharfen Umkehrungen sind auf 4h als Selloff mit Überdehnung und Umkehrmuster erkennbar, und eine Minderheit davon ist der Beginn einer Expansionsphase. Die deskriptive Vorprüfung (Abschnitt 4.1 in v0.1) bleibt und wird ergänzt um: Anzahl RTC-Kontextereignisse (K1 bis K3) je Jahr, Anteil davon mit Reversal-Evidenz, Verteilung der 20-Tage-Vorwärtsrendite nach Kontextereignissen gegen unbedingt, jeweils XRP gegen BTC und ETH auf denselben Definitionen. Nach dem Freeze, vor dem Strategielauf, ohne Auswahlwirkung.

## 2. Kandidaten

**XRP-RTC, primär, 4h, 8h Robustheit.** Bottom Entry Engine nach Framework: Kontext K1 (Rückgang vom 20-Tage-Hoch mindestens 12 Prozent), K2 (Extension mindestens 2 ATR unter EMA50 innerhalb der letzten sechs Kerzen), K3 (innerhalb einer ATR eines deterministischen Support-Niveaus oder an der lokalen Low-Struktur). Zwei Familien: RTC-CR (Candle Reversal, `bull_any`: Bullish Harami, Bullish Hikkake, Hammer, Bullish Engulfing, Morning Star) und RTC-FB (Failed Breakdown / Liquidity Sweep Bottom, priorisiert). Trigger T0 (Eröffnung t+1), TA (Schluss über dem Hoch der Signalkerze), TB (Rückeroberung des Niveaus), später T1h. Ebenen RTC-0 bis RTC-3. Hold E1 (Chandelier 3 ATR14, nur steigend), Exits E1 und E2 (PES ≥ 3 nach Risikofrei-Bedingung, mit P12 Kaufklimax und P13 Failed Breakout), Kontrollarchitektur E0 (Exit am EMA20 oder nach 30 Kerzen). Alle Zahlen aus dem Framework, keine XRP-spezifische Abweichung. Diagnosen: Kerzengrenzen (+1h, +2h), Cross-Venue (Kraken, ab 2023 OKX), Capture Efficiency, Tageskontext.

**XRP-B, Volatility Breakout, 4h primär, Tagesbasis Robustheit.** Identisch mit BTC-B und DOT-A: Keltner-Kompression (`kelt_pct` unter 0.20 auf einer der letzten 30 Kerzen), Ausbruch über das 120-Kerzen-Hoch ohne aktuelle Kerze, Einstieg t+1, Chandelier 3 ATR20, kein Ziel, Short spiegelbildlich. Verschachtelte Bestätigung XRP-B+ (wie DOT-C): derselbe Ausbruch mit `delta_open_interest` ≥ +0.10, `taker_imbalance` ≥ +0.10 auf der Ausbruchskerze und `funding_zscore` ≤ +1.5 (Long), als inkrementeller Test, nicht als eigene Familie.

**Referenzlinien, keine Tests:** MTP-Spezifikation v1 auf XRP (aus der Validierung bekannt) und W2 aus Stufe 2 auf XRP, auf denselben Daten, Kosten und Blöcken.

**Short-Spiegel (Top Entry) von XRP-RTC:** tertiäre Familie nach Framework, auf Perp-Daten, mit Vermerk.

## 3. Inputs

Alle Merkmale aus der Feature Library (Form, Flow, Struktur), Signalquelle Binance Spot 4h (Form, Volumen, Taker), Binance Perp 4h (Perp-Taker, Basis), Funding 8h, OI täglich (ab 2021-12), Liquidationen (keine Quelle, RTC-3 entfällt fail-closed, bis eine Quelle nach `data_upgrade_options_v1.md` vorliegt). Ausführung Ebene B auf Kraken XRPUSD 240 Minuten.

## 4. Datenbedarf und Datenstand

Vorhanden: Binance Spot 1d ab 2018-05-04, Perp 1d ab 2020-01-06, Funding ab 2020-01-06, OI ab 2021-12-01, Kraken 1d ab 2017-05-18, CMC ab 2013-08-04. Wird geladen (17.09.2026): Binance Spot und Perp 4h und 1d mit allen Spalten, Kraken 240 aus dem Archiv plus API. Danach nachzuladen: Binance Spot und Perp 1h (Trigger T1h, Kerzengrenzen-Diagnose), Kraken 60 aus dem Archiv, Binance-Metrics-Aggregation für 4h-OI, OKX-Kerzen ab 2023-07 für den Cross-Venue-Bericht. Nach dem Laden: Lückenprüfung, 4h-Raster, Gegenproben (Vollspalten gegen OHLCV, 4h aggregiert gegen 1d), Prüfsummen, Abdeckungstabelle je Merkmal.

Discovery-Fenster: 2018-05 bis 2023-12 (rund 5.6 Jahre, rund 12300 Kerzen, Blöcke P1 bis 2020, P2 2021 bis 2023). Holdout: 2024-01 bis Datenende (rund 2.7 Jahre). Vermerk: Das Holdout enthält die XRP-Expansion ab November 2024, die dem Verfasser bekannt ist (Framework Abschnitt 2). RTC-2 nur ab 2020-01 (Funding) beziehungsweise 2021-12 (OI), Inkrement I2 auf dem gemeinsamen Fenster.

Fail-closed: fehlende Merkmale machen die Kerze für die betreffende Ebene nicht auswertbar, keine Rückrechnung, keine Ersatzwerte.

## 5. Look-ahead-Risiken

Framework Abschnitt 16 und Feature Library Abschnitt 8. XRP-spezifisch: Kraken XRPUSD 240 hat vor 2018 eine dünne Phase (B-Start-Regel), und die Binance-Spot-Listung 2018-05 liegt vor der Perp-Listung 2020-01, deshalb sind Perp-Merkmale in P1 weitgehend leer. Look-ahead-Test mit Schnitt 30.06.2022 für alle Kandidaten und Zeitebenen.

## 6. Kostenmodell

Unverändert aus v0.1: Perp-Modell K0 bis K2 mit tatsächlichem Funding je 8h-Periode, Spot-Modell für Long-Seiten (Kraken Tier 1), Ebene B auf Kraken-240 mit erstem handelbaren Preis nach der Kerzengrenze, Stop-Market mit 0.10 Prozent Slippage unter K1, 0.30 unter K2. Short-Seiten auf Binance-Perp-Daten mit Kraken-Perp-Sätzen und Vermerk. Cash zum T-Bill-Satz. Kostenquote je Kandidat als Berichtswert, für E0 (kurze Haltedauer) als entscheidender Berichtswert.

## 7. Tests und Nullhypothesen (Discovery)

Primäre Familie XRP-RTC (Holm über vier): T1-CR und T1-FB (RTC-0, E1, Long gegen Passivposition), T2 E2 gegen E1 gepaart, T3 E0 gegen E1 gepaart. Hypothesen-Familie (Holm über vier, mit 1h-Daten fünf): H1 Wick mal Volumen, H2 FB gegen CR, H3a TA gegen T0, H3b TB gegen T0, H3c RTC-MTF gegen TA. Die zentrale Frage dieses Strangs ist T3: H0-T3 lautet, dass der Exit am Gleichgewicht dieselbe Erwartung je Trade liefert wie der Trend-Capture-Exit. Unter der Hypothese des Strangs wird H0-T3 verworfen, mit E1 über E0 in der Erwartung und E0 über E1 in der Trefferquote.

Inkrement-Familie (Holm über drei oder vier): I1 RTC-1 gegen RTC-0, I2 RTC-2 gegen RTC-1, I3 nur mit Liquidationsquelle, P-Inc (E2 mit P12 und P13 gegen ohne).

Primäre Familie XRP-B (Holm über zwei): B-L, B-S gegen Passivposition. Inkrement I-B: XRP-B+ gegen XRP-B (bestätigte gegen unbestätigte Ausbrüche, gepaart auf demselben Fenster ab 2021-12).

Tertiär: Short-Spiegel T1S, I1S, I2S.

Jitter und Robustheit (keine Tests): 8h für RTC, Tagesbasis für B, k 2.5 und 3.5, PES 2 und 4, K1 0.10 und 0.15, K2 1.5 und 2.5, für B Perzentil 0.10 und 0.30, Donchian 90 und 180 Kerzen, Stop 2.5 und 3.5.

DSR-Trial-Zahl: 14 bis 16 Tests dieses Plans plus Jitter plus Vorbelastung XRP (Stufe 2: 9 Woo, 3 MR, 3 TS, 4 D, Stufe 1: 7, MTP: 1, also 27).

## 8. Kriterien

Discovery: «Signal vorhanden» nach Framework Abschnitt 13 (Erwartung netto K1 über null, Bootstrap-5-Prozent-Perzentil über null nach Holm, mindestens 30 Trades, beide Discovery-Blöcke nicht negativ bei mindestens 10 Trades je Block, kein Trade über 40 Prozent des Bruttogewinns). Konfigurationsregel für die Validation nach Framework Abschnitt 13: Familie nur bei bestandenem T1, E2 nur bei bestandenem T2, Trigger nur bei bestandenem H3, höhere Ebene nur bei bestandenem Inkrement, sonst E1, T0 und RTC-0. Kandidatentypen, deren Erwartung nur auf der UTC-Aggregation positiv ist, gehen nicht in die Validation.

Validation auf dem Holdout, einmalig, Mechanik eingefroren, die neun Kriterien aus v0.1 Abschnitt 8, angepasst: Profit-Faktor mindestens 1.3, Trade-Mindestzahl 20 im Holdout (Vermerk «geringe Basis» unter 40), Zeitblöcke innerhalb des Holdouts als Kalenderjahre 2024, 2025, 2026 mit mindestens zwei nicht negativen, Jitter, MaxDD gegen Passivposition, Beta-Trennung, Bootstrap mit Holm, Kostenstress K2, Edge-Retention Kraken mindestens 60 Prozent mit abweichendem Exit-Grund höchstens 15 Prozent. Berichtet, nicht Kriterium: R-Verteilung, MFE und Giveback je Exit, Anteil Trades mit Floor über Einstieg, Konzentration, Ergebnis ohne grössten Gewinner, Kostenquote, Referenzlinien, Cross-Venue-Übereinstimmung je Signal (Kraken, ab 2023 OKX).

## 9. Offene Entscheidungen vor dem Freeze

1. XRP-C streichen (Empfehlung, Begründung Abschnitt 0) oder als Bericht ohne Test mitführen.
2. XRP-B auf 4h primär mit der gemeinsamen Engine (Empfehlung) oder Tagesbasis wie v0.1.
3. Die Filter F1 bis F3 aus v0.1 durch die inkrementellen Ebenen ersetzen (Empfehlung) oder zusätzlich führen.
4. Trade-Mindestzahlen Discovery 30, Validation 20 bestätigen.
5. Profit-Faktor 1.3 bestätigen.
6. Deskriptive Vorprüfung nach dem Freeze, vor dem Lauf (Empfehlung) bestätigen.
7. Referenzlinien MTP v1 und W2 beide (Empfehlung) bestätigen.
8. Short-Spiegel tertiär (Empfehlung) bestätigen.
9. Framework- und Feature-Library-Entscheidungen gelten auch hier.

Nach Klärung: Version 1.0, Prüfsumme in ENTSCHEIDE, gemeinsam mit Framework, Feature Library, BTC- und DOT-Plan eingefroren. Danach: Datenvalidierung, Look-ahead-Test, Informationswert-Test der Muster auf dem Discovery-Fenster, deskriptive Vorprüfung, ein Discovery-Lauf.
