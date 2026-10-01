# BTC Japanese Price-Action Features, Version 0.1

**Project Aurum II, Strang 06_btc_specialist, Teil von BTC YAMATO RTC. 17.09.2026. Status: Feature-Katalog zur Prüfung. Kein Rechenlauf. Quellenregel: `.jp`-Quellen. Der Katalog ergänzt die Candlestick and Flow Feature Library v0.1 um die Merkmale, die YAMATO zusätzlich braucht, und verweist für alles andere auf die Library. Alle Merkmale sind deterministisch, ATR-normalisiert, point-in-time.**

## 1. Multi-Timeframe-Kontext (Weekly, Daily vor 4h)

Grosse Zeitebenen werden vor kleinen gelesen (マルチタイムフレーム in den japanischen Quellen, die Monex- und SBI-Berichte gehen von Monat und Tag zum 4h-Chart). In YAMATO ist das Kontext, kein Schalter:

| Merkmal | Definition, Stand Kerze t (4h) | Verwendung |
|---|---|---|
| `d_ext` | (Tagesschluss_{d−1} − EMA50_d) / ATR14_d auf Tageskerzen, letzter abgeschlossener Tag | Bericht, Kontextaufteilung |
| `d_sma200_rel` | Tagesschluss_{d−1} / SMA200_d − 1 (die 200-Tage-Linie ist in den `.jp`-BTC-Berichten die meistgenannte Referenz) | Bericht |
| `d_ichimoku_pos` | Lage des Tagesschlusses zur Tageswolke: −1 unter, 0 in, +1 über | Bericht |
| `w_ext` | Wochenschluss der Vorwoche relativ zu EMA20_w in ATR14_w | Bericht |
| `w_swing_low_dist` | Abstand des 4h-Schlusses zum letzten bestätigten Wochen-Swing-Low in ATR14_w | Kontext K3 auf Wochenebene, Bericht |

Kein Merkmal dieser Tabelle ist Bedingung eines Einstiegs oder Exits in Version 0.1. Die Kontextaufteilung (Kandidaten mit `d_ext` unter minus 2 gegen übrige, unter der Tageswolke gegen darüber) ist Bericht.

## 2. Kerzengeometrie (aus der Library, hier die Auswahl für YAMATO)

`lw_range`, `lower_wick_atr`, `uw_range`, `upper_wick_atr`, `body_range`, `body_atr`, `close_location`, `range_atr`, `direction`, `volume_zscore`, `lw_x_vol`, `uw_x_vol`, `taker_imbalance`. Die japanischen Quellen betonen Dochtlänge und Schlusslage vor dem Musternamen (kabutech.jp: langer unterer Docht mit hohem Volumen als Kapitulation, langer oberer Docht als Verkaufsdruck), deshalb werden diese Grössen je Kandidat berichtet und in H1 getestet.

## 3. Struktur

Aus der Library: bestätigte Swing Highs und Lows (3/3), `hh_hl_intact`, `lower_high`, `structure_break`, `failed_breakdown`, `failed_breakout`, Support- und Resistance-Niveaus (Swing, 120-Kerzen-Extrem, Zone mit drei Berührungen). Aus `btc_previous_open_levels_spec_v0.1.md`: die Previous-Open-Niveaus und `reclaim`, `reclaim_strong`, `loss`. Aus `btc_sakata_bottom_peak_spec_v0.1.md`: `double_bottom`, `triple_bottom`, `gyaku_sanzon` (逆三尊), `triple_top`, `sanzon` (三尊), je mit Nackenlinie.

## 4. MACD-Divergenz (4h, nur Inkrement)

MACD-Linie = EMA12 − EMA26 der Schlusskurse, Signal = EMA9 der MACD-Linie, Histogramm = MACD − Signal, Standardparameter nach den `.jp`-Beschreibungen (Rakuten, OANDA Japan, CoinPost), nicht angepasst.

`bull_divergence_t` = 1, wenn die zwei letzten bestätigten Swing Lows s1 < s2 innerhalb von 120 Kerzen ein tieferes Preistief (L_{s2} < L_{s1}) und ein höheres MACD-Tief (min MACD-Linie in s2 ± 3 Kerzen > min MACD-Linie in s1 ± 3 Kerzen) zeigen, und s2 auf t oder früher bestätigt ist. Das ist die in den `.jp`-BTC-Analysen (Monex: «MACDは日足レベルですでにダイバージェンスが発生») verwendete Form «Preis tieferes Tief, MACD höheres Tief». Spiegelbildlich `bear_divergence_t` an Swing Highs. Die Divergenz wird je Kandidat als Flag geführt und im Inkrement-Test Y5 (Kandidaten mit Divergenz gegen ohne) geprüft. MACD erzeugt nie einen Einstieg.

Redundanzkontrolle wie bei Ichimoku: Y5 läuft parallel mit der Ersatzregel «`mom10` bei s2 höher als bei s1» (normalisiertes Momentum ohne Glättung), damit sichtbar wird, ob die MACD-Glättung Information trägt.

## 5. Trend-Hold-Merkmale

Je Kerze während einer offenen Position: `hh_hl_intact`, `above_open_w_prev` (Schluss über der Wocheneröffnung der Vorwoche), `above_kijun` (Schluss über der 4h-Kijun), `peak_candidate_recent` (Peak Candidate innerhalb der letzten 30 Kerzen), `last_hl` (letztes bestätigtes Higher Low seit Einstieg). Die Hold-Regel E-Y des Forschungsplans verwendet `peak_candidate_recent` und den Bruch von `last_hl`, die übrigen sind Bericht und Robustheitsvarianten.

## 6. Zielmetriken (Diagnose, nie Signal)

Aus dem Framework Abschnitt 14: `entry_efficiency` (Bottom Entry Efficiency), `capture_ratio` (Trend Capture Ratio), `exit_efficiency` (Peak Exit Efficiency), dazu `realized_share` = realisierte Bewegung geteilt durch die gesamte Post-Bottom-Aufwärtsbewegung bis zum ex-post-Hoch innerhalb von 60 Kerzen nach Exit, und `giveback` = (MFE − realisiertes R) je Trade in R. Berechnung in einem getrennten Modul ohne Zugriff auf die Signalbildung.

## 7. Halving-Kontext

`days_since_halving`, `days_to_next_expected_halving`, `cycle_phase` nach `halving_context_research_plan_v0.1.md`, je Kandidat als Kontext, explorativ. Die `.jp`-Quellen (Monex-Ausblick zum Vierjahreszyklus) behandeln den Zyklus ausdrücklich als Hintergrund, nicht als Signal, mit dem Hinweis, dass der Markt regelmässig von der Erwartung abweicht.

## 8. Ausgabe

`features/binance_BTC_4h_yamato_v0.1.csv` mit allen Merkmalen dieses Katalogs neben den Library-Merkmalen, Prüfsummen in `provenance_features.json`. Look-ahead-Test wie Library Abschnitt 8, zusätzlich für Wochen- und Monatsniveaus die Zuordnungsprüfung (Abschnitt 5 der Previous-Open-Spezifikation).
