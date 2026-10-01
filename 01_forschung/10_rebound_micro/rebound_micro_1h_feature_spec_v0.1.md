# REBOUND-MICRO — 1h-Feature-Spezifikation, Version 0.1

**Project Aurum II, `01_forschung/10_rebound_micro/rebound_micro_1h_feature_spec_v0.1.md`. 18.09.2026. Gilt für die 1h-Library `mlib.py` (getrennt von rlib/ylib 4h und dlib 4h). Quelle: Binance Spot 1h, zwölf Spalten (t, open, high, low, close, volume, close_time, quote_volume, trades, taker_buy_base, taker_buy_quote). Perp 1h nur als Diagnosequelle derselben Merkmale. Alle Merkmale der Kerze b verwenden ausschliesslich Kerzen ≤ b. Keine dieser Festlegungen wird nach Kenntnis von M3-Outcomes geändert.**

## 1. Raster, Lücken, Join

1h-Raster UTC, Kerze b beginnt bei t_b und endet bei t_b plus 59:59. Rasterlücken (Audit) werden nicht gefüllt. Rolling-Fenster sind Kerzenindex-Fenster über vorhandene Kerzen; enthält das Fenster eine Lücke, wird das Merkmal NaN (fail-closed, Flag `gap_in_window`). Off-Grid-Kerzen (BTC Spot, 43 Kerzen 09. bis 11.02.2018) sind quarantäniert und nicht in der Datei. Join 4h → 1h: eine 4h-Kerze t (Beginn T) enthält die 1h-Kerzen mit T ≤ t_b < T + 4h; der 4h-Kontext am Schluss von t ist ab der ersten 1h-Kerze mit t_b ≥ T + 4h verwendbar. Prüfung: Aggregation der vier 1h-Kerzen muss Open, High, Low, Close der 4h-Kerze reproduzieren (Provenance-Crosscheck, bekannte Abweichungen ausgewiesen).

## 2. Kerzengeometrie (kontinuierlich, ATR-normiert)

ATR14(1h): Wilder über 14 1h-Kerzen, Initialisierung als Mittel der ersten 14 True Ranges. Für Vergleiche der Kerze b gilt ATR14(1h)_{b−1}. `range_b` = H − L, `body_b` = |C − O|, `lower_wick_b` = min(O, C) − L, `upper_wick_b` = H − max(O, C). Merkmale: `lower_wick_atr` = lower_wick / ATR14_{b−1}, `lower_wick_range` = lower_wick / range (NaN bei range 0), `body_range` = body / range, `close_location` = (C − L) / range, `range_atr` = range / ATR14_{b−1}. Diagnoseflags, keine Trigger: `bullish_harami_b` = C_{b−1} < O_{b−1} und O_b > C_{b−1} und C_b < O_{b−1} und C_b > O_b und body_b < body_{b−1}; `hikkake_b` = Inside Bar bei b−2 (H_{b−2} ≤ H_{b−3}, L_{b−2} ≥ L_{b−3}), Ausbruch nach unten bei b−1 (L_{b−1} < L_{b−2}, C_{b−1} ≤ H_{b−2}), Rückkehr bei b (C_b > H_{b−2}).

## 3. Flow-Merkmale (Spot 1h)

Aggressives Verkaufsvolumen `sell_quote_b` = quote_volume − taker_buy_quote (Quote-Währung, Taker-Verkäufe). Aggressives Kaufvolumen `buy_quote_b` = taker_buy_quote.

`taker_imbalance_b` = (2 · taker_buy_quote − quote_volume) / quote_volume, Bereich −1 bis +1, NaN bei quote_volume 0. Kein Fenster, kein Lag.

`delta_taker_imbalance_b` = taker_imbalance_b − Mittel(taker_imbalance, b−6..b−1). Fenster 6 Kerzen, Mindesthistorie 6, NaN wenn eines der sechs NaN.

`volume_zscore_b` = (volume_b − Mittel(volume, b−168..b−1)) / SD(volume, b−168..b−1, Populations-SD). Fenster 168 Kerzen (sieben Tage), Mindesthistorie 168, NaN bei SD 0. Kein Clipping in der Berechnung, Bericht mit Winsorization bei ±5 nur für Verteilungsgrafiken.

`trade_count_zscore_b` = analog auf `trades`, Fenster 168.

`sell_volume_zscore_b` = analog auf `sell_quote`, Fenster 168.

`downside_price_progress_b` = max(0, O_b − C_b) / ATR14(1h)_{b−1}, dimensionslos, null bei steigender Kerze. Einheit ATR.

`sell_efficiency_b` = downside_price_progress_b / max(sell_volume_zscore_b, 0.5). Einheit ATR je Einheit z. Denominator-Regel: Der Nenner ist nach unten auf 0.5 begrenzt, damit kleine oder negative z-Werte keine Explosion erzeugen. Für die M3-Absorptionsbedingung wird `sell_efficiency` nur ausgewertet, wenn `sell_volume_zscore` ≥ 1.0, also ausschliesslich bei überdurchschnittlichem aggressivem Verkaufen. Lesart: kleiner Wert = viel aggressives Verkaufen, wenig Preisfortschritt nach unten = mögliche Absorption. NaN, wenn ATR14 oder z NaN.

Diagnose (kein Trigger): dieselben fünf Merkmale aus Perp 1h, gejoint über den Zeitstempel, ausgewiesen als `*_perp`, mit Abdeckungstabelle.

## 4. Lags und Mindesthistorie

Alle Fenster enden bei b−1 (exklusive der aktuellen Kerze) für Mittel und SD, die aktuelle Kerze liefert nur den Zähler. Erste auswertbare Kerze: Index 168 (Volumen-z) beziehungsweise 14 (ATR), Warmup 168 Kerzen (sieben Tage) für die gesamte Library. Rolling-Fenster über eine Lücke → NaN.

## 5. Fehlende Werte

Fail-closed: Jede NaN-Eingabe in einer Trigger-Bedingung macht die Bedingung falsch, der Kandidat entsteht nicht, das Fehlen wird gezählt (`nan_feature`). Kein Vorwärtsfüllen.

## 6. Look-ahead-Tests (Pflicht vor Kandidatenzählung)

Test 1: Störung aller 1h-Kerzen ab Index T verändert kein Merkmal mit Index < T. Test 2: Verschiebung einer einzelnen Kerze b um +1 verändert Merkmale mit Index < b nicht. Test 3: Der 4h-Kontext einer 1h-Kerze b ist identisch, wenn alle 1h-Kerzen ≥ b gestört werden (Join-Test). Test 4: AVWAP an Kerze b verändert sich nicht durch Störung von Kerzen > b, und der Anker verändert sich nicht durch Störung von Kerzen nach dem Anker. Test 5: Kandidaten M1, M2, M3 mit Einstiegskerze e < T sind identisch nach Störung ab T.

## 7. Unit-Tests (Pflicht)

Synthetische Kerzen mit bekannten Werten für jedes Merkmal (mindestens ein Fall je Merkmal, ein Grenzfall je Denominator-Regel, ein NaN-Fall je Fenster), 4h→1h-Join auf konstruierten Daten, AVWAP von Hand nachgerechnet auf fünf Kerzen, Episode-Reset auf konstruierter K1-Sequenz.
