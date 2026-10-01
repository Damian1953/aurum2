# DOT Specialist — Strategiefamilien-Plan, Version 0.3

**Project Aurum II, Forschungsstrang 05_dot_specialist. 17.09.2026. Status: Plan zur Prüfung. Kein Rechenlauf, kein Freeze. Ersetzt Version 0.1 (Version 0.2 nicht vergeben). Alle Freeze-Urteile der Stufen 1, 2 und der MTP-Validierung bleiben unangetastet. Setzt `rtc_reversal_to_trend_framework_v0.1.md` und `candlestick_flow_feature_library_spec_v0.1.md` voraus und hält nur DOT-spezifische Festlegungen fest.**

## 0. Zweck und Abgrenzung

Primäre Frage: Welche der drei ökonomisch getrennten Hypothesen besitzt auf DOT überhaupt Evidenz? Nicht: welche Parameter sind optimal. Drei Hypothesen mit je einem vorab gesetzten Parametersatz unter identischen Daten, Kosten, Slippage, Blöcken und Sizing (Head-to-Head): DOT-A (4h Volatility Compression, dann Preisausbruch), DOT-C (exakt derselbe Ausbruch, verschachtelt, plus Derivate-Bestätigung) und DOT-RTC (Selloff und Überdehnung, Candle- oder Failed-Breakdown-Reversal, Trend Hold, Peak Exit).

Was sich gegenüber v0.1 ändert: DOT-A wechselt auf 4h primär mit der coin-übergreifend identischen Engine (BTC-B, XRP-B), Tagesbasis wird Robustheit. DOT-C ist jetzt bewusst in DOT-A verschachtelt (in v0.1 ohne Kompressionsbedingung), damit der inkrementelle Informationswert der Derivatedaten isoliert gemessen wird: Der Vergleich A gegen C ist ein gepaarter Teilmengentest auf denselben Ausbrüchen, keine zweite Familie. DOT-B (tägliche Mean- und Order-Flow-Reversion) entfällt und wird durch DOT-RTC ersetzt. DOT-RTC ist ausdrücklich keine tägliche Mean Reversion und kein weiterer täglicher Woo-Test: 4h, Kontext plus Niveau plus Rejection statt z-Score, Chandelier statt Mittelwert. Der Order-Flow-Filter aus v0.1 (Taker-Kaufanteil) geht in RTC-1 auf.

Vorbelastung, offen ausgewiesen: DOT war in Stufe 2 bei fast allen Woo-Varianten negativ (W2 Long minus 10 Prozent CAGR, W6 minus 6, MR Long minus 10), in der MTP-Validierung mit sechs Trades, null Gewinnern und minus 0.75 R der schwächste Coin. Tägliche Trendfolge auf DOT ist dreimal geprüft und dreimal gescheitert. Nach der methodischen Regel des Frameworks (Abschnitt 1) ist das Vorbelastung, kein Veto gegen 4h-Kompression, 4h-Flow oder 4h-Reversal, weil Zeitebene, Signal und Exit andere Kombinationen sind. Die Trial-Zahl der DSR führt die Vorversuche (Abschnitt 8). Die frühere Formulierung «keine Version 2 mit gelockerten Kriterien» bleibt in der Sache und wird präzisiert: keine Parametervariante einer gescheiterten Hypothese, neue Mechaniken zulässig.

DOT hat die kürzeste Historie im Universum (Binance ab 2020-08-18, Kraken ab 2020-08-18, Perp und Funding ab 2020-08-20, OI ab 2021-12-01). Discovery-Fenster 2020-08 bis 2023-12 (rund 3.4 Jahre, rund 7400 Kerzen), Block P1 ist nur das letzte Drittel von 2020. Die Trade-Mindestzahl von 30 in der Discovery wird für DOT-RTC voraussichtlich knapp, das ist hinzunehmen und wird als «geringe Basis» ausgewiesen, nicht durch Lockerung umgangen.

## 1. Marktstruktur-Hypothese

Unverändert aus v0.1: DOT produziert viele Fehlausbrüche, echte Expansionsphasen sind von steigendem OI und Volumen begleitet, Funding läuft in Ausbrüchen schnell ins Extrem. Ergänzt um die RTC-Vermutung: DOT-Selloffs enden häufig mit einem Durchstich unter ein sichtbares Tief (Stops abgeholt) und Rückkehr in die Range, und nur ein Teil davon wird ein Trend. Deskriptive Vorprüfung nach dem Freeze, vor dem Lauf, ohne Auswahlwirkung: Anteil der 120-Kerzen-Ausbrüche, die innerhalb von 30 Kerzen unter das Ausbruchsniveau zurückfallen (DOT gegen BTC, ETH, SOL), Verteilung von ΔOI und Volumen-z an Ausbruchskerzen, Anzahl RTC-Kontextereignisse und Failed Breakdowns je Jahr, Anteil mit Reversal-Evidenz, 20-Tage-Vorwärtsrendite nach Kontextereignissen gegen unbedingt.

## 2. Hypothesen

**DOT-A, 4h Volatility Compression, Preisausbruch.** Identisch mit BTC-B und XRP-B: `kelt_pct` unter 0.20 auf mindestens einer der letzten 30 Kerzen, Schluss über dem höchsten Hoch der letzten 120 Kerzen ohne die aktuelle (Long) beziehungsweise unter dem tiefsten Tief (Short), Einstieg zur Eröffnung der Folgekerze, Chandelier 3 · ATR20 vom höchsten Schluss, nachgezogen, kein Ziel, kein gleitender Durchschnitt als Filter. Tagesbasis (Fenster 20 und 180 Tage) als Robustheit.

**DOT-C, exakt DOT-A plus Bestätigung, verschachtelt.** Dieselbe Ausbruchskerze mit drei Zusatzbedingungen, alle vorab gesetzt: OI-Bestätigung `delta_open_interest` ≥ +0.10 (neues Kapital kommt in die Bewegung), Taker-Flow-Bestätigung `taker_imbalance` ≥ +0.10 auf der Ausbruchskerze (Expansion wird aggressiv gekauft, ersetzt das Volumenverhältnis aus v0.1, das in `volume_zscore` als Berichtswert bleibt), Funding-Crowding-Filter `funding_zscore` ≤ +1.5 (die Bewegung ist nicht von Perp-Longs überfüllt). Short spiegelbildlich (ΔOI ≥ +0.10, `taker_imbalance` ≤ −0.10, `funding_zscore` ≥ −1.5). Alle drei müssen erfüllt sein. Jitter je einzeln: ΔOI 0.05 und 0.15, Taker 0.05 und 0.20, Funding-z 1.0 und 2.0. Weil OI erst ab 2021-12 vorliegt, wird der Vergleich A gegen C auf dem gemeinsamen Fenster ab 2021-12 geführt, als gepaarter Teilmengentest (bestätigte gegen unbestätigte Ausbrüche), und zusätzlich je Bedingung einzeln (nur OI, nur Taker, nur Funding) als Bericht, damit sichtbar wird, welche Datenklasse den Gewinn trägt.

**DOT-RTC, 4h, 8h Robustheit.** Nach Framework, ohne DOT-spezifische Abweichung: Kontext K1 bis K3, Familien RTC-CR und RTC-FB (priorisiert), Trigger T0, TA, TB, später T1h, Ebenen RTC-0 bis RTC-3, Hold E1, Exits E1 und E2 (mit P12, P13), Kontrolle E0, Diagnosen Kerzengrenzen, Cross-Venue, Capture Efficiency, Tageskontext.

**Referenzlinien, keine Tests:** MTP v1 und W2 auf DOT (aus Stufe 2 und MTP-Validierung bekannt).

**Short-Spiegel von DOT-RTC:** tertiär, auf Perp-Daten, mit Vermerk.

## 3. Inputs

Feature Library vollständig, Signalquelle Binance Spot 4h und Perp 4h, Funding 8h, OI täglich ab 2021-12 (4h-OI nach Metrics-Aggregation, sobald geladen), Liquidationen keine Quelle (RTC-3 entfällt fail-closed). Ausführung Ebene B auf Kraken DOTUSD 240.

## 4. Datenbedarf und Datenstand

Vorhanden: Binance Spot 1d ab 2020-08-18, Perp 1d ab 2020-08-22, Funding ab 2020-08-20, OI ab 2021-12-01, Kraken 1d ab 2020-08-18, CMC ab 2020-08-20. Wird geladen (17.09.2026): Binance Spot und Perp 4h und 1d mit allen Spalten, Kraken 240 aus dem Archiv plus API. Danach: Binance Spot und Perp 1h, Kraken 60, Metrics-Aggregation, OKX-Kerzen ab 2023-07. Nach dem Laden Lückenprüfung, Raster, Gegenproben, Prüfsummen, Abdeckungstabelle je Merkmal.

Discovery 2020-08 bis 2023-12, Holdout 2024-01 bis Datenende (rund 2.7 Jahre, länger als das Discovery-Fenster ein Drittel der Historie, das ist für DOT ungewöhnlich und wird ausgewiesen). DOT-C und I2 nur ab 2021-12. Fail-closed wie Framework.

## 5. Look-ahead-Risiken

Framework Abschnitt 16 und Feature Library Abschnitt 8. DOT-spezifisch: Die Kraken-Frühphase 2020 ist dünn (B-Start-Regel), ΔOI auf 4h-Kerzen verwendet den Tagesschnappschuss von 00:00 (bekannt ab Kerze 00:00) bis die Metrics-Aggregation vorliegt. Look-ahead-Test mit Schnitt 30.06.2022 für alle drei Hypothesen und beide Zeitebenen.

## 6. Kostenmodell

Identisch für alle drei Hypothesen, das ist die Voraussetzung des Head-to-Head: K0 bis K2 mit tatsächlichem Funding, Spot-Modell für Long-Seiten, Ebene B auf Kraken-240 mit erstem handelbaren Preis nach der Kerzengrenze, Stop-Market mit Slippage, Short-Seiten auf Perp-Daten mit Kraken-Perp-Sätzen und Vermerk, Cash zum T-Bill-Satz, Sicht 1. Kostenquote und Turnover je Hypothese.

## 7. Tests und Nullhypothesen (Discovery)

Familie A/C (Holm über drei): A-L, A-S (H0: keine Erwartung über exposure-gleicher Passivposition), C-Inc (H0: bestätigte Ausbrüche haben dieselbe Erwartung je Trade und dieselbe Trefferquote wie unbestätigte, gepaarter Teilmengentest ab 2021-12).

Familie RTC primär (Holm über vier): T1-CR, T1-FB, T2, T3. Hypothesen-Familie (Holm über vier, mit 1h fünf): H1, H2, H3a, H3b, H3c. Inkrement-Familie: I1, I2, P-Inc. Tertiär: Short-Spiegel.

Head-to-Head-Regel: Eine Hypothese hat «Signal vorhanden», wenn ihr primärer Test das Discovery-Kriterium erfüllt. Haben mehrere, wird keine ausgewählt, alle gehen in die Validation. Hat keine, ist die Antwort auf die primäre Frage «keine», und es gibt keine Parametervariante. Der Vergleich der Kennzahlen zwischen Hypothesen wird berichtet, entscheidet aber nicht, weil die Fenster verschieden sind.

Jitter und Robustheit: Tagesbasis für A, 8h für RTC, A Perzentil 0.10 und 0.30, Donchian 90 und 180 Kerzen, Stop 2.5 und 3.5, RTC nach Framework.

## 8. Multiplizität

DSR mit zwei Trial-Zahlen: die Tests dieses Plans (3 plus 12 bis 14, plus Jitter) und konservativ dazu die Vorbelastung DOT (15 Woo-Tests der Stufe-2-Matrix, 3 Familie B, 1 MTP-Validierung, 7 Stufe 1, also 26). Externe Vorversuche Dritter auf DOT sind nicht zählbar, aber der Grund, warum die Blockregel und die Mindestzahlen nicht gelockert werden.

## 9. Kriterien

Discovery «Signal vorhanden» nach Framework Abschnitt 13, mit der DOT-Anpassung, dass Block P1 (nur 2020-08 bis 2020-12) nicht gewertet wird und die Blockbedingung für DOT lautet: Erwartung in P2 nicht negativ und in beiden Hälften von P2 (2021 bis Mitte 2022, Mitte 2022 bis 2023) nicht negativ bei mindestens 10 Trades je Hälfte. Validation auf dem Holdout mit den neun Kriterien, Trade-Mindestzahl 20, Kalenderjahre 2024, 2025, 2026 mit mindestens zwei nicht negativen.

Berichtet: R-Verteilung, MFE und Giveback je Exit, Anteil Floor über Einstieg, Konzentration, Ergebnis ohne grössten Gewinner, Kostenquote, Schnittmengen A/C, Bedingungen einzeln, Referenzlinien, Cross-Venue je Signal, Capture Efficiency, Kerzengrenzen.

## 10. Offene Entscheidungen vor dem Freeze

1. DOT-A auf 4h primär mit der gemeinsamen Engine (Empfehlung) oder Tagesbasis wie v0.1.
2. DOT-C verschachtelt in DOT-A (Vorgabe, bestätigt) mit Taker-Imbalance statt Volumenverhältnis (Empfehlung, weil Taker-Richtung die Absorptionsfrage stellt, Volumen bleibt Bericht).
3. Schwellen von DOT-C (ΔOI 0.10, Taker 0.10, Funding-z 1.5) bestätigen.
4. DOT-B streichen und durch DOT-RTC ersetzen (Vorgabe, bestätigt), VWAP-Robustheit entfällt damit.
5. Trade-Mindestzahl 30 Discovery, 20 Validation, Blockregel mit P2-Hälften bestätigen.
6. Profit-Faktor 1.3 bestätigen.
7. Head-to-Head auf voller Historie je Hypothese mit Vergleichstabelle auf dem gemeinsamen Fenster ab 2021-12 (Empfehlung) bestätigen.
8. Trial-Zahl der DSR-Sensitivität bestätigen.
9. Framework- und Feature-Library-Entscheidungen gelten auch hier.

Nach Klärung: Version 1.0, Prüfsumme in ENTSCHEIDE, gemeinsam mit Framework, Feature Library, XRP- und BTC-Plan eingefroren. Danach Datenvalidierung, Look-ahead-Test, Informationswert-Test, deskriptive Vorprüfung, ein Discovery-Lauf.
