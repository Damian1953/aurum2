# DOT Specialist — Strategiefamilien-Plan, Version 0.4

**Project Aurum II, Forschungsstrang 05_dot_specialist. 17.09.2026. Status: Plan zur Prüfung vor dem Freeze, kein Lauf. Ersetzt Version 0.3. Übernimmt die Stufe-A-Struktur und die Lehren aus BTC YAMATO Stufe A wie XRP v0.4, ohne Zahlen der eingefrorenen BTC-Spezifikation zu ändern. Drei ökonomisch getrennte Mechanismen, coin-spezifisch ausgewertet, kein Pooling.**

## 0. Drei Mechanismen

**DOT-A, 4h Volatility Compression, Preisausbruch.** Identische Breakout-Engine wie BTC-B und XRP-B: Keltner-Kompression (`kelt_pct` unter 0.20 auf einer der letzten 30 Kerzen), Schluss über dem 120-Kerzen-Hoch ohne aktuelle Kerze (Long) beziehungsweise unter dem Tief (Short), Einstieg zur Eröffnung der Folgekerze, Chandelier 3 ATR20, kein Ziel. Tagesbasis als Robustheit.

**DOT-C, exakt DOT-A plus Bestätigung, verschachtelt.** Dieselbe Ausbruchskerze mit ΔOI ≥ +10 Prozent (Derivatives-Library `delta_open_interest`), Taker-Imbalance ≥ +0.10, Funding-z ≤ +1.5 (Long, Short spiegelbildlich). Gepaarter Teilmengentest ab 2021-12, je Bedingung einzeln als Bericht. DOT-C ist die Messung des inkrementellen Informationswerts der Derivatedaten, keine eigene Familie.

**DOT-RTC, Stufe-A-Struktur.** Kontext K1 bis K3, Familien D1 Failed Breakdown, D2 Double Bottom mit Nackenlinienbruch (ohne 3-ATR-Grenze), D3 Wick plus Volumen, Zahlen identisch mit dem BTC-Parameterpaket v1.1. Trigger T0 primär, TA und TB als Vergleiche. Exit E-U primär, E-D als Vergleich. Kontrollgruppe wie BTC. RTC-1 und RTC-2 als Inkremente. Follow-through-Diagnose.

Referenzlinien MTP v1 und W2 auf DOT aus früheren Stufen, keine Tests.

## 1. Vorbelastung und Fenster

Tägliche Trendfolge auf DOT dreimal gescheitert (Stufe 2, MTP-Validierung), Dokumentation, kein Veto gegen 4h-Mechanismen. Discovery 2020-08 bis 2023-12 (rund 7400 Kerzen), Holdout ab 2024 (rund 5900 Kerzen, für DOT länger als ein Drittel der Historie, ausgewiesen). Block P1 (2020-08 bis 2020-12) nicht gewertet, Blockregel: P2 in zwei Hälften (2021 bis Mitte 2022, Mitte 2022 bis 2023) je nicht negativ bei mindestens 10 Signalen. Daten validiert: Binance Spot und Perp 4h und 1h mit allen Spalten ab 2020-08, Funding ab 2020-08-20, OI ab 2021-12-01, Kraken DOTUSD 240 ab 2020-08-18, Flow-Library-Ausgabe `DOTUSDT_flow_4h.csv`.

## 2. Erwartete Zahlen (Schätzung, ohne DOT-Outcomes)

DOT hat auf 3.4 Jahren Discovery viele 12-Prozent-Rückgänge. Erwartet: D1 60 bis 100 Kandidaten, T0 rund 45 bis 75 Trades, TA 15 bis 25. D2 10 bis 18. D3 20 bis 35 Kandidaten. DOT-A Long 25 bis 45 Ausbrüche, Short ähnlich, DOT-C-Teilmenge ab 2021-12 rund 10 bis 20. Nur D1 mit T0 und DOT-A erreichen voraussichtlich 30. D2 und DOT-C bleiben «geringe Basis» oder deskriptiv, das ist so hinzunehmen.

## 3. Tests und Multiplizität

Familie A/C (Holm über drei): A-L, A-S, C-Inc. RTC primär (Holm über drei): D1, D2, D3 je mit T0 (D2 Nackenlinie) und E-U gegen Kontrollen. Trigger-Familie (Holm über vier): TA und TB gegen T0 auf D1, D3. Exit-Familie (Holm über drei): E-D gegen E-U. Inkremente (Holm über zwei): RTC-1, RTC-2. Trial-Zahl: 15 plus Jitter plus Vorbelastung DOT (26). Kriterien, Statusebenen, Fast Fail und Fast Promote nach Auswertungsregeln v1. Head-to-Head-Regel: Mechanismen mit «mechanistically promising» oder besser gehen in die Validation, keine Auswahl, keine Kombination.

## 4. Produktionsvermerk

DOT-A und DOT-C: Long auf Kraken Spot, Short auf Kraken Perp mit Funding, Ausführung zur Eröffnung (Taker), Stops Taker, Trades je Jahr voraussichtlich 10 bis 20 je Seite, Haltedauer Tage bis Wochen, API OHLCV 4h plus Binance-Flow (OI täglich, Funding 8h), Komplexität mittel wegen Perp-Seite. DOT-RTC wie XRP-RTC.

## 5. Offene Entscheidungen vor dem Freeze

1. T0 als primärer RTC-Trigger (Empfehlung) bestätigen.
2. E-D als zweite Exit-Baseline bestätigen.
3. DOT-C-Schwellen (ΔOI 0.10, Taker 0.10, Funding-z 1.5) bestätigen.
4. Blockregel mit P2-Hälften bestätigen.
5. Trial-Zahl 15 bestätigen.

Nach Klärung: Version 1.0, Prüfsumme in ENTSCHEIDE, Umsetzung auf der BTC-Library, Look-ahead-Test, Zählung, Matching-Abdeckung, ein Discovery-Lauf, coin-spezifisch, ohne Pooling mit BTC oder XRP. Ein Cross-Coin-Generalisierungstest wird erst vorregistriert, wenn dieselbe Mechanik auf mindestens zwei Coins in dieselbe Richtung wirkt.
