# Derivatives- und Flow-Feature-Library, Version 0.1 (umgesetzt)

**Project Aurum II, `01_forschung/00_gemeinsam/dlib/`. 17.09.2026. Umsetzung der Flow-Merkmale aus `candlestick_flow_feature_library_spec_v0.1.md` Abschnitt 5 als coin-übergreifend identischer Code (`dlib.py`). Erste Ausgabe für BTC, XRP, DOT, ETH, SOL auf dem Binance-Spot-4h-Raster. Kein Strategietest, keine Schwellen. Verwendung zunächst ausschliesslich inkrementell: «price-action only» gegen «price-action plus derivatives confirmation» innerhalb einer vorregistrierten Hypothese.**

## 1. Merkmale (alle Kerze t, nur Daten bis Kerzenschluss t)

`taker_imbalance` = (2 · Taker-Buy-Quote − Quote-Volumen) / Quote-Volumen, Spot. `taker_imbalance_perp` dasselbe auf der Perp-Kline. `volume_zscore`, `trade_count_zscore`, `taker_buy_zscore` je mit Fenster t−60..t−1. `ti_delta6` = Taker-Imbalance minus ihr Mittel über t−6..t−1. `price_progress_per_taker_volume` = (C − O) / ATR14_{t−1} geteilt durch max(`taker_buy_zscore`, 0.5), `price_progress_per_volume` analog mit `volume_zscore`. `spot_perp_basis` = (Perp-Schluss − Spot-Schluss) / Spot-Schluss auf derselben Kerze, `basis_zscore` über 180 Kerzen. `funding_last` = zuletzt abgerechnete 8h-Rate, deren Settlement-Zeit strikt vor dem Kerzenschluss liegt (eine Rate mit Settlement 08:00 gilt ab der Kerze 08:00, nicht für die Kerze, die um 08:00 schliesst, konservativ), `funding_zscore` über 270 Perioden (90 Tage), `funding_7d_ann` = Summe der letzten 21 Raten mal 365/7. `open_interest` und `delta_open_interest` (OI_d / OI_{d−5} − 1) aus dem Tagesschnappschuss 00:00 UTC, gültig ab der Kerze 00:00 desselben Tages, fail-closed leer, wenn der letzte Schnappschuss älter als ein Tag ist.

Fenster 60, 270, 180 Kerzen beziehungsweise Perioden, OI-Lag 5 Tage, Untergrenze 0.5 im Nenner der Fortschrittsmasse: aus der Spezifikation, nicht optimiert, für alle Coins gleich.

## 2. Abdeckung (erste Ausgabe)

| Coin | 4h-Kerzen | Taker ab | Basis ab | Funding-z ab | ΔOI ab | SHA-256 Ausgabe |
|---|---|---|---|---|---|---|
| BTC | 19890 | 2017-08-17 | 2020-01-01 | 2020-03-31 | 2021-01-06 | c3b6f39d59aeacea… |
| XRP | 18337 | 2018-05-04 | 2020-01-06 | 2020-04-05 | 2021-12-06 | da470538aba9acb3… |
| DOT | 13321 | 2020-08-18 | 2020-08-22 | 2020-11-18 | 2021-12-06 | 9c3bc4373433a265… |
| ETH | 19890 | 2017-08-17 | 2020-01-01 | 2020-03-31 | 2021-12-06 | 935022c152a78022… |
| SOL | 13367 | 2020-08-11 | 2020-09-14 | 2020-12-12 | 2021-12-06 | b18c99359c1e6a86… |

Taker-Merkmale sind ab Datenbeginn vollständig (Binance-Klines tragen die Spalten seit 2017), Funding-z braucht 90 Tage Vorlauf, OI ist für alle fünf Coins erst ab 2021-12-01 verfügbar (BTC-OI-Datei beginnt ebenfalls 2021-12, obwohl Binance Metrics für BTC ab 2021-01 publiziert, das ist ein Loader-Startwert und wird beim nächsten OI-Lauf erweitert). Plausibilität: Taker-Imbalance im Bereich −0.85 bis +0.87, Basis-Median −3.7 bis −4.6 Basispunkte (Perp leicht unter Spot, konsistent mit Binance-Marktstruktur), Funding-z mit Ausreissern bis −70 (DOT, SOL, extreme Negativ-Raten in Crash-Phasen), ΔOI-Median leicht positiv. Funding-Wechsel treten ausschliesslich auf Kerzen mit Beginn 00, 08, 16 UTC auf (1741, 1729, 1652 Fälle bei XRP), das bestätigt die Settlement-Zuordnung.

## 3. Look-ahead-Test

Abschneidetest mit Eingaben bis 30.06.2022 (Spot, Perp, Funding, OI je getrennt abgeschnitten) gegen den Volllauf: alle 16 Merkmale auf 9103 Kerzen identisch bis auf Gleitkomma-Rauschen (maximale Abweichung 5e-13, gleiche Fehlwerte-Maske). Bestanden.

## 4. Vorgesehene Verwendung

RTC-Ebenen (RTC-1 Taker-Flow, RTC-2 Funding und OI) nach Framework Abschnitt 3, Peak-Komponenten P6 bis P9 und P12, DOT-C-Bestätigung, XRP-B-Bestätigung, Follow-through-Diagnose nach Einstieg (Preis, OI, Taker, Volumen über 1, 3, 6 Kerzen, «viel aggressives Kaufen ohne Fortschritt» als Absorptionsmarker). Nächste Ausbaustufe: 4h-OI aus Binance-Metrics-Tagesdateien (Loader-Erweiterung), Kraken-Taker-Seite aus Time-and-Sales, OKX-Funding als Cross-Venue.

## 5. Dateien

`dlib/dlib.py`, `dlib/out/<SYM>_flow_4h.csv` (fünf Coins), `dlib/out/coverage.json`.
