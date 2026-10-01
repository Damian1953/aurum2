# Candlestick and Flow Feature Library — Spezifikation, Version 0.1

**Project Aurum II, gemeinsame Komponente für alle coin-spezifischen Stränge (`01_forschung/00_gemeinsam/`). 17.09.2026. Status: Spezifikation zur Prüfung. Kein Rechenlauf. Die Definitionen sind für alle Coins identisch, der Informationswert wird je Coin und Zeitebene getrennt geprüft.**

## 0. Zweck

Eine deterministische Bibliothek, die aus OHLCV-Kerzen (plus, wo vorhanden, Quote-Volumen, Anzahl Trades, Taker-Buy-Volumen, Funding, Open Interest, Basis, Liquidationen) je Kerze binäre Pattern-Flags, stetige Formmerkmale und Flow-Merkmale berechnet. Sie ist die einzige Quelle für Candle- und Flow-Merkmale in RTC (Bottom Entry Engine, Hold Engine, Peak Evidence Engine), in den Breakout-Familien, in den Vorprüfungen und in der Informationswert-Analyse. Kein Strang definiert eigene Candle-Regeln. Jede Änderung an dieser Bibliothek ist eine neue Version mit Prüfsumme und macht laufende Freezes ungültig.

Grundhaltung: Ein Candle-Pattern ist ein Merkmal, kein Signal, und sein Name ist nicht die primäre Information. Jede Kerze wird zuerst in ihre deterministische Geometrie zerlegt (Range, Body, Dochte, Close-Lage, Richtung, alles relativ zu Range, Body und ATR), die diskreten Muster (Hammer, Harami, Engulfing, Hikkake und so weiter) sind Kombinationen dieser Geometrie mit Kontext und bleiben als Flags erhalten, aber die stetigen Geometriemerkmale sind gleichrangig oder wichtiger. Hinter der Kerzenform stehen nach den ausgewerteten japanischen und chinesischen Quellen vor allem Dochtlänge, Schlusslage, Volumen und die Position im Chart, und genau diese Grössen werden hier als Zahlen geführt. Die einzige grossangelegte Untersuchung an Kryptomärkten, die uns bekannt ist (Moser und Brauneis, International Review of Economics and Finance, Band 108, 2026: rund 400 Coins, 1935 Paare, 36 Börsen, Stundenkerzen Juli 2018 bis Januar 2022, 55 TA-Lib-Muster, Superior-Predictive-Ability-Test), findet für einige Muster statistisch robuste, aber ökonomisch kleine Folgeerträge: bullish Hikkake rund 8 bis 10 Basispunkte über 1 bis 6 Stunden, bullish Harami 4 bis 9 Basispunkte, Inverted Hammer und Doji Star deutlich mehr, auf der Gegenseite Hanging Man, Bearish Harami und Bearish Hikkake als signifikant negative Prädiktoren. Die Autoren halten selbst fest, dass Nettoerträge nach Gebühren negativ werden können. Für Aurum II folgt daraus: Candle-Muster liefern Information über die nächsten Stunden bis Tage, aber keinen für sich handelbaren Edge. Sie werden deshalb ausschliesslich als Bestätigungs- und Evidenzmerkmale in Konstruktionen verwendet, die ihre Erwartung aus dem Halten eines Trends beziehen, nie als isolierter Ein- oder Ausstieg.

## 1. Eingaben und Normalisierung

Je Kerze t: Open O, High H, Low L, Close C, Volumen V (Basiswährung), Quote-Volumen Q, Taker-Buy-Quote-Volumen TBQ (Binance-Klines, Spalten 8 und 11), Anzahl Trades N. Auf Kraken-Kerzen fehlen Q, TBQ, dort sind Flow-Merkmale «nicht auswertbar».

Abgeleitete Grössen, alle nur aus Kerzen bis einschliesslich t:

| Grösse | Definition |
|---|---|
| Body | B = abs(C − O) |
| Range | R = H − L, bei R = 0 ist die Kerze «nicht auswertbar» |
| Oberer Docht | UW = H − max(O, C) |
| Unterer Docht | LW = min(O, C) − L |
| Richtung | bullish wenn C > O, bearish wenn C < O, sonst neutral |
| Close-Lage | CL = (C − L) / R, Wert 0 bis 1 |
| ATR | Wilder-ATR über 14 Kerzen, ATR_{t−1} (bis einschliesslich Vorkerze) für alle Grössenvergleiche der Kerze t, damit die Normierung die aktuelle Kerze nicht enthält |
| Body-Grösse | b = B / ATR_{t−1} |
| Mittelwert Body | Bm = Mittel von B über die Kerzen t−20 bis t−1 |
| Taker-Imbalance | TI = (2 · TBQ − Q) / Q, Wert −1 bis +1, positiv heisst Überhang aggressiver Käufer |
| Volumenverhältnis | VR = V / Mittel(V über t−20 bis t−1) |
| Geometrie-Quoten | `body_range` = B / R, `uw_range` = UW / R, `lw_range` = LW / R, `uw_body` = UW / max(B, 0.05 · R), `lw_body` = LW / max(B, 0.05 · R), `range_atr` = R / ATR_{t−1}, `direction` = +1, 0, −1 |

Schwellen, alle vorab gesetzt, nicht optimiert, für alle Coins und Zeitebenen gleich: «kleiner Body» ist B ≤ 0.30 · R, «Doji» ist B ≤ 0.10 · R, «langer Body» ist B ≥ 1.0 · Bm und b ≥ 0.5, «kurzer Docht» ist Docht ≤ 0.15 · R, «langer Docht» ist Docht ≥ 2.0 · B und Docht ≥ 0.5 · R.

Kryptomärkte handeln durchgehend, Eröffnungslücken existieren nicht (O_t ist praktisch C_{t−1}). Alle klassischen Muster, die eine Lücke verlangen (Morning Star, Evening Star, Dark Cloud Cover, Piercing), werden deshalb in der lückenlosen Fassung definiert. Das ist eine Abweichung von Nison und Bulkowski und wird so ausgewiesen.

## 2. Kontextflags

Muster tragen ihre Bedeutung nur im Kontext. Der Kontext wird getrennt vom Formflag berechnet, damit die Engines ihn je nach Zweck verlangen oder nicht:

| Flag | Definition (auf Kerze t, nur Vergangenheit) |
|---|---|
| decline | (C_{t−1} − EMA50_{t−1}) / ATR_{t−1} ≤ −1.5 oder Low-Minimum der Kerzen t−5 bis t liegt unter dem tiefsten Tief der Kerzen t−120 bis t−6 |
| advance | spiegelbildlich: (C_{t−1} − EMA50_{t−1}) / ATR_{t−1} ≥ +1.5 oder High-Maximum der Kerzen t−5 bis t über dem höchsten Hoch der Kerzen t−120 bis t−6 |
| at_low_structure | min(L über t−2 bis t) ≤ 1.02 · tiefstes Tief der Kerzen t−120 bis t−3 |
| at_high_structure | max(H über t−2 bis t) ≥ 0.98 · höchstes Hoch der Kerzen t−120 bis t−3 |

Die Konstanten 1.5 (Extension in ATR), 120 Kerzen (20 Tage auf 4h) und 2 Prozent sind vorab gesetzt. Auf Tageskerzen gelten dieselben Zahlen mit 120 Tagen.

## 3. Bullish Reversal-Muster

Alle Flags werden auf der Kerze gesetzt, mit deren Schluss das Muster vollständig ist. Nur diese Kerze darf einen Einstieg auslösen (frühestens Eröffnung der Folgekerze).

**Hammer.** Kerze t: LW lang (LW ≥ 2.0 · B und LW ≥ 0.5 · R), UW kurz (UW ≤ 0.15 · R), CL ≥ 0.60. Richtung beliebig. Kontext decline verlangt (ohne decline ist dieselbe Form kein Hammer, sondern «Hanging-Man-Form», siehe Abschnitt 4).

**Inverted Hammer** (nur Informationswert-Test, nicht in RTC): UW lang, LW kurz, CL ≤ 0.40, Kontext decline. Aufgenommen, weil er in der zitierten Untersuchung der stärkste bullish Prädiktor war, aber nicht in die Bottom Entry Engine, weil seine Form (Kauf wurde abgewiesen) ökonomisch keine Erschöpfung der Verkäufer belegt. Der Informationswert-Test kann das widerlegen, dann wäre er ein Kandidat für eine spätere Version.

**Bullish Engulfing.** Kerze t−1 bearish, Kerze t bullish, O_t ≤ C_{t−1} und C_t ≥ O_{t−1} (Body t umschliesst Body t−1), B_t ≥ 1.0 · Bm (kein Mikro-Engulfing). Kontext decline.

**Bullish Harami.** Kerze t−1 bearish mit langem Body, Body der Kerze t vollständig innerhalb des Body von t−1 (max(O_t, C_t) ≤ O_{t−1} und min(O_t, C_t) ≥ C_{t−1}), Richtung von t beliebig, B_t ≤ 0.5 · B_{t−1}. Kontext decline. Harami-Cross (Doji in t) ist eingeschlossen.

**Morning Star, lückenlos.** Kerze t−2 bearish mit langem Body, Kerze t−1 kleiner Body (B ≤ 0.30 · R_{t−1}) mit min(O, C)_{t−1} ≤ C_{t−2} + 0.25 · B_{t−2}, Kerze t bullish mit C_t ≥ O_{t−2} − 0.5 · B_{t−2} (Schluss mindestens in der oberen Hälfte des Body von t−2). Kontext decline auf t−2.

**Bullish Hikkake, nach Chesler.** Kerze t−k−1 (Mutterkerze), Kerze t−k ist Inside Bar (H ≤ H_{t−k−1} und L ≥ L_{t−k−1}), Kerze t−k+1 hat tieferes Hoch und tieferes Tief als der Inside Bar (falscher Ausbruch nach unten), und innerhalb der folgenden drei Kerzen (t−k+2 bis t−k+4) schliesst eine Kerze über dem Hoch des Inside Bar. Das Flag wird auf dieser Bestätigungskerze t gesetzt, k ergibt sich aus der Lage, 1 ≤ k ≤ 3 Kerzen zwischen Inside Bar und Bestätigung. Kontext: keiner verlangt (das Muster trägt seinen Kontext in sich), für RTC wird decline zusätzlich über die Engine verlangt.

Sammelflag `bull_any` = Bullish Harami oder Bullish Hikkake oder Hammer oder Bullish Engulfing oder Morning Star. Priorität nach Evidenz und Handelbarkeit: die ersten vier primär, Morning Star sekundär (im Sammelflag enthalten, im Informationswert-Test getrennt ausgewiesen). Anzahl gleichzeitig erfüllter Muster `bull_count` als Bericht.

## 4. Bearish Reversal- und Peak-Muster

**Shooting Star.** UW lang, LW kurz, CL ≤ 0.40, Kontext advance.

**Hanging Man.** Form des Hammers (LW lang, UW kurz, CL ≥ 0.60), Kontext advance. In der zitierten Untersuchung signifikant negativ, deshalb ausdrücklich enthalten, obwohl die Form intuitiv bullish wirkt.

**Bearish Engulfing.** Kerze t−1 bullish, Kerze t bearish, O_t ≥ C_{t−1} und C_t ≤ O_{t−1}, B_t ≥ 1.0 · Bm. Kontext advance.

**Bearish Harami.** Kerze t−1 bullish mit langem Body, Body t innerhalb des Body t−1, B_t ≤ 0.5 · B_{t−1}. Kontext advance.

**Evening Star, lückenlos.** Spiegelbild des Morning Star: t−2 bullish langer Body, t−1 kleiner Body mit max(O, C)_{t−1} ≥ C_{t−2} − 0.25 · B_{t−2}, t bearish mit C_t ≤ O_{t−2} + 0.5 · B_{t−2}. Kontext advance auf t−2.

**Dark Cloud Cover, lückenlos.** Kerze t−1 bullish mit langem Body, Kerze t bearish, O_t ≥ C_{t−1} − 0.1 · B_{t−1} (eröffnet nahe oder über dem Vorschluss), C_t < C_{t−1} − 0.5 · B_{t−1} und C_t > O_{t−1} (schliesst unter der Mitte, aber nicht unter der Eröffnung von t−1, sonst ist es ein Engulfing). Kontext advance.

**Three Black Crows.** Kerzen t−2, t−1, t alle bearish mit B ≥ 0.7 · Bm, jede schliesst tiefer als die vorige, jede eröffnet innerhalb des Body der vorigen, jede mit LW ≤ 0.25 · R. Kontext advance auf t−2. Vermerk: Das Muster ist per Definition erst nach drei Abwärtskerzen vollständig, ein Teil der Bewegung ist dann vorbei. Es wird geführt, aber in der Peak Evidence Engine mit demselben Gewicht wie alle anderen, nicht höher.

**Bearish Hikkake.** Spiegelbild von Abschnitt 3: Inside Bar, falscher Ausbruch nach oben (höheres Hoch und höheres Tief als der Inside Bar), Bestätigung durch einen Schluss unter dem Tief des Inside Bar innerhalb von drei Kerzen. In der zitierten Untersuchung als negativer Prädiktor gefunden, deshalb in der Peak Evidence Engine enthalten.

Sammelflag `bear_any` über die acht Peak-Muster, `bear_count` als Bericht. Priorität für die Engines nach Evidenz und Handelbarkeit: Bearish Harami, Hanging Man, Bearish Hikkake, Shooting Star, Bearish Engulfing (primäre fünf), Evening Star, Dark Cloud Cover, Three Black Crows (sekundär, im Sammelflag enthalten, im Informationswert-Test getrennt ausgewiesen).

## 5. Stetige Form- und Flow-Merkmale

Alle Merkmale sind je Kerze t deterministisch aus Daten bis einschliesslich t berechnet. Normierungsfenster enden mit t−1, damit die Kerze t nicht ihre eigene Normierung beeinflusst. Rollende Mittel und Standardabweichungen sind einfache (nicht exponentielle) Fenster, die Fensterlängen sind in Kerzen der jeweiligen Zeitebene angegeben.

**Formmerkmale (Preis)**

| Merkmal | Definition |
|---|---|
| `body_atr` | B / ATR_{t−1} |
| `lower_wick_atr` | LW / ATR_{t−1} |
| `upper_wick_atr` | UW / ATR_{t−1} |
| `close_location` | (C − L) / (H − L) |
| `ext` | (C_t − EMA50_t) / ATR_{t−1}, normalisierte Extension |
| `dd120` | C_t / max(H über t−120 bis t−1) − 1, Rückgang vom 20-Tage-Hoch (auf 4h) |
| `ru120` | C_t / min(L über t−120 bis t−1) − 1, Anstieg vom 20-Tage-Tief |
| `mom10` | (C_t − C_{t−10}) / ATR_{t−1}, normalisiertes Momentum |
| `hh20`, `ll20` | 1 wenn H_t über dem höchsten Hoch der Kerzen t−20 bis t−1, spiegelbildlich für Tiefs |
| `hh120`, `ll120` | dasselbe über 120 Kerzen |
| `kelt_w` | 4 · ATR20_t / EMA20_t, Keltner-Kanal-Breite relativ |
| `kelt_pct` | Perzentil von `kelt_w` innerhalb der Kerzen t−1080 bis t−1 (nur Vergangenheit) |
| `er20` | Kaufman Efficiency Ratio über 20 Kerzen |

**Flow-Merkmale (Binance-Klines, Perp-Daten)**

| Merkmal | Definition | Quelle, Verfügbarkeit |
|---|---|---|
| `volume_zscore` | (V_t − Mittel(V, t−60..t−1)) / SD(V, t−60..t−1) | Spot-Kline, ab Datenbeginn |
| `trade_count_zscore` | (N_t − Mittel(N, t−60..t−1)) / SD(N, t−60..t−1) | Spot-Kline, ab Datenbeginn |
| `taker_imbalance` | (2 · TBQ_t − Q_t) / Q_t | Spot-Kline, ab Datenbeginn |
| `taker_imbalance_perp` | dasselbe auf der Perp-Kline | Perp-Kline, ab 2019-09 (BTC) bzw. Listing |
| `ti_delta6` | `taker_imbalance_t` − Mittel(`taker_imbalance`, t−6..t−1), Flow-Wechsel über einen Tag | abgeleitet |
| `delta_open_interest` | OI_d / OI_{d−5} − 1 aus Tagesschnappschüssen 00:00 UTC, für eine 4h-Kerze gilt der Wert des letzten bekannten Schnappschusses (00:00 des laufenden Tages, bekannt ab Kerze 00:00) | Binance OI, ab 2021-12-01 (BTC ab 2021-01) |
| `funding_zscore` | (f_letzte − Mittel(f, 270 Perioden)) / SD(f, 270 Perioden), 270 Perioden zu 8h sind 90 Tage, f_letzte ist die zuletzt abgerechnete Rate | Binance Funding, ab 2020 (BTC ab 2019-09) |
| `funding_7d` | Summe der letzten 21 Raten, annualisiert mal 365/7 | abgeleitet |
| `spot_perp_basis` | (C_perp − C_spot) / C_spot auf derselben Kerze | Binance Spot und Perp, ab Perp-Listing |
| `basis_zscore` | z von `spot_perp_basis` über 180 Kerzen | abgeleitet |
| `taker_buy_zscore` | (TBQ_t − Mittel(TBQ, t−60..t−1)) / SD(TBQ, t−60..t−1) | Spot-Kline |
| `price_progress_per_taker_volume` | (C_t − O_t) / ATR_{t−1} geteilt durch max(`taker_buy_zscore_t`, 0.5), Preisfortschritt je Einheit aggressiven Kaufens, klein bei Absorption | abgeleitet |
| `lw_x_vol` | `lower_wick_atr_t` · max(`volume_zscore_t`, 0), Interaktion Docht mal Volumen (Hypothese H1) | abgeleitet |
| `uw_x_vol` | `upper_wick_atr_t` · max(`volume_zscore_t`, 0) | abgeleitet |
| `lw_x_ti` | `lower_wick_atr_t` · max(`ti_delta6_t`, 0), Docht mal Flow-Wechsel zur Käuferseite (optional) | abgeleitet |
| `uw_x_tb` | `upper_wick_atr_t` · max(`taker_buy_zscore_t`, 0), Docht mal Kaufklimax (optional) | abgeleitet |

**Liquidationsmerkmale (nur wenn eine Quelle mit 4h-Auflösung und dokumentierter Historie vorliegt, sonst leer, siehe `data_upgrade_options_v1.md`)**

| Merkmal | Definition |
|---|---|
| `long_liq_usd`, `short_liq_usd` | aggregierte Long- bzw. Short-Liquidationen in USD in der Kerze t |
| `long_liq_ratio` | `long_liq_usd_t` / Median(`long_liq_usd`, t−180..t−1), 180 Kerzen sind 30 Tage auf 4h |
| `short_liq_ratio` | spiegelbildlich |
| `liq_spike_long` | 1 wenn `long_liq_ratio` ≥ 3.0 in t oder t−1 |
| `liq_spike_short` | 1 wenn `short_liq_ratio` ≥ 3.0 in t oder t−1 |

Kein Schwellenwert dieser Tabelle wird anhand von Renditen gesetzt oder verändert. Die Zahlen (60 Kerzen für z-Scores, 270 Funding-Perioden, 180 Kerzen für Liquidationsmedian, Faktor 3.0) sind vorab gesetzt. Fehlt eine Eingabe, ist das Merkmal leer und jede Regel, die es verlangt, «nicht auswertbar» (fail-closed), nie null.

**Swing-Struktur**

Ein Swing Low ist bestätigt, wenn L_s kleiner ist als die Tiefs der drei Kerzen davor und der drei Kerzen danach, das Flag wird auf Kerze s+3 gesetzt (erst dann bekannt). Swing High spiegelbildlich. `last_swing_low`, `last_swing_high`, `prev_swing_low`, `prev_swing_high` sind die jeweils letzten zwei bestätigten Niveaus, Stand Kerze t. Abgeleitet: `hh_hl_intact` = 1 wenn `last_swing_high` > `prev_swing_high` und `last_swing_low` > `prev_swing_low`, `lower_high` = 1 wenn ein neu bestätigtes Swing High unter dem vorigen liegt, `structure_break` = 1 wenn C_t < `last_swing_low`. Die Bestätigungsverzögerung von drei Kerzen ist die wichtigste Look-ahead-Falle dieser Bibliothek und wird im Look-ahead-Test explizit geprüft (Abschnitt 8).

**Deterministische Support- und Resistance-Niveaus (Location)**

Keine gezeichneten Linien. Drei Niveaudefinitionen, alle nur aus Kerzen bis t und alle mit denselben Zahlen für alle Coins:

| Niveau | Definition |
|---|---|
| `swing_low_level`, `swing_high_level` | letztes bestätigtes Swing Low beziehungsweise Swing High (3/3-Bestätigung, siehe Swing-Struktur), das nicht älter als 240 Kerzen ist (40 Tage auf 4h) |
| `nbar_low_level`, `nbar_high_level` | tiefstes Tief beziehungsweise höchstes Hoch der Kerzen t−120 bis t−3 |
| `zone_low_level`, `zone_high_level` | mehrfach getestete Zone: Preisband der Breite 0.5 · ATR_{t−1} um ein bestätigtes Swing Low, das in den letzten 240 Kerzen von mindestens zwei weiteren bestätigten Swing Lows innerhalb dieser Toleranz berührt wurde (`zone_touches` ≥ 3). Spiegelbildlich für Hochs |

`support_level` = das höchste der drei Low-Niveaus, das unter dem aktuellen Schluss liegt (das nächste Niveau darunter), `resistance_level` spiegelbildlich. `dist_support_atr` = (C_t − `support_level`) / ATR_{t−1}. Die Fenster 120 und 240 Kerzen und die Toleranz 0.5 ATR sind vorab gesetzt, keine Lookback-Länge wird aus dem Ergebnis gewählt. Die Jitter-Nachbarn 90/180 und 180/360 Kerzen laufen ausschliesslich als Robustheit.

**Liquidity Sweep, Failed Breakdown und Failed Breakout (Kerze t, ein Niveau L aus der Tabelle oben, Stand t−1)**

| Flag | Definition |
|---|---|
| `failed_breakdown` | L_t < L · (1 − 0.001) (die Kerze handelte unter dem Niveau, mindestens 0.1 Prozent, damit Rundung nicht zählt) und C_t > L (schliesst wieder darüber) und `lower_wick_atr_t` ≥ 0.5 und LW ≥ 1.5 · B (relevante Rejection). Wird für jedes der drei Low-Niveaus getrennt gesetzt und als Sammelflag geführt, das Niveau wird im Feature gespeichert |
| `failed_breakout` | spiegelbildlich: H_t > L_high · 1.001 und C_t < L_high und `upper_wick_atr_t` ≥ 0.5 und UW ≥ 1.5 · B |
| `sweep_depth_atr` | (L − L_t) / ATR_{t−1} beim Failed Breakdown, Tiefe des Durchstichs |
| `reclaim_confirmed` | 1 auf Kerze t+1, wenn C_{t+1} > L (Rückeroberung bestätigt), das ist Trigger B des RTC-Frameworks |

Ein Failed Breakdown ist keine Kerzenform, sondern eine Preis-Niveau-Interaktion: Der Markt hat die Stops unter einem Niveau abgeholt und die Verkäufer haben den Preis nicht dort halten können. Er wird deshalb als eigene Bottom-Familie geführt (Framework Abschnitt 3), nicht als weiteres Muster.

## 6. Ausgabeformat

Je Coin, Quelle und Zeitebene eine CSV `features/<QUELLE>_<COIN>_<TF>_features_v0.1.csv` mit Zeitstempel (Kerzenbeginn UTC), allen Flags (0/1, leer bei «nicht auswertbar»), Form-, Flow- und Liquidationsmerkmalen, plus Prüfsumme in `features/provenance_features.json` mit Version der Bibliothek, Prüfsumme des Codes und der Eingabedateien. Fehlende Eingaben (kein Taker-Volumen auf Kraken, keine 21 Kerzen Vorlauf) ergeben leere Felder, nie Nullen.

## 7. Informationswert-Test je Coin und Zeitebene (Discovery Stage, kein Strategietest)

Frage: Trägt ein Muster auf diesem Coin und dieser Zeitebene Information über die Folgerendite, unabhängig von jeder Strategie?

Design, vorab festgelegt: Für jedes Muster mit Kontext, für die stetigen Geometrie- und Interaktionsmerkmale (in Quintilen: `lower_wick_atr`, `upper_wick_atr`, `close_location`, `lw_x_vol`, `uw_x_vol`, je oberstes gegen übrige Quintile, mit Kontext decline beziehungsweise advance) und für `failed_breakdown` und `failed_breakout`, und jede Zeitebene (4h, 1d) je Coin: mittlere Überrendite (Close-to-Close, log) über die Horizonte 1, 6, 18 und 42 Kerzen (auf 4h: 4 Stunden, ein Tag, drei Tage, sieben Tage, auf 1d: 1, 6, 18, 42 Tage) gegenüber der unbedingten mittleren Rendite derselben Horizonte im selben Fenster, plus MFE/MAE-Kennzahl: Anteil der Ereignisse, bei denen der Preis 2 ATR in Musterrichtung erreicht, bevor er 1 ATR gegen die Richtung läuft, gegenüber demselben Anteil an zufälligen Kerzen. Statistik: Block-Bootstrap 2000 (Blocklänge 42 Kerzen) über die Ereignisse, skew-adjustierter t-Test wie in der zitierten Untersuchung, Holm-Korrektur innerhalb eines Coins und einer Zeitebene über alle Muster mal Horizonte (14 Muster plus 5 Geometriemerkmale plus 2 Sweep-Flags, mal 4 Horizonte, 84 Tests). Ein Muster gilt als «informativ» auf diesem Coin, wenn mindestens zwei benachbarte Horizonte nach Holm signifikant sind mit gleichem Vorzeichen in Musterrichtung, und die MFE/MAE-Kennzahl in dieselbe Richtung zeigt. Ergebnis ist eine Tabelle je Coin, die für alle Coins gleich gebaut ist, und ein Vergleich der Tabellen (welche Muster sind auf allen, welche nur auf einzelnen Coins informativ).

Verwendung des Ergebnisses: Es ändert keine Definition und keinen Parameter der Discovery-Läufe. Es dient (a) der Interpretation, (b) der Vorregistrierung coin-spezifischer Musterteilmengen für die Validation Stage, die vor jedem Blick auf die Holdout-Daten festgelegt werden. Ein Muster, das auf einem Coin nicht informativ ist, wird in der Discovery trotzdem im Sammelflag geführt, weil `bull_any` vorab so definiert ist.

Fenster: Der Informationswert-Test läuft nur auf dem Discovery-Fenster (bis 31.12.2023), nie auf dem Holdout (Abschnitt 4 des RTC-Frameworks).

## 8. Look-ahead-Test der Bibliothek

Vor jeder Verwendung: Die Bibliothek wird auf der vollen Historie und auf der bei einem festen Datum abgeschnittenen Historie gerechnet. Alle Flags und Merkmale bis zum Abschneidedatum minus 4 Kerzen müssen bitgleich sein (Flow-Merkmale mit Tagesquellen: minus eine Tageskerze) (die vier Kerzen decken die Swing-Bestätigung und den Hikkake-Vorlauf ab, für die Kerzen unmittelbar vor dem Schnitt sind Abweichungen erwartet und werden protokolliert). Zusätzlich ein Konstruktionstest: Für jedes Muster wird geprüft, dass keine Definition eine Kerze nach t verwendet, indem die Kerzen nach t zufällig permutiert werden und die Flags bis t unverändert bleiben müssen.

## 8a. Kerzengrenzen-Robustheit (Diagnose, nie Basis)

Kryptomärkte handeln durchgehend, eine 4h-Kerze hängt von der Aggregationsgrenze ab. Primäre Konvention ist und bleibt UTC mit Grenzen 00/04/08/12/16/20, identisch zu den Rohdaten der Börsen. Sie wird nicht nach Ergebnis verändert. Ausschliesslich als Robustheitsdiagnose werden aus 1h-Kerzen zwei verschobene 4h-Aggregationen gebildet (Grenzen +1h: 01/05/09 und so weiter, und +2h: 02/06/10 und so weiter), die Bibliothek wird auf allen drei Aggregationen gerechnet, und berichtet werden je Muster und Coin: Anteil der Signalkerzen, die auf einer verschobenen Aggregation innerhalb von ±1 Kerze ebenfalls ein Signal derselben Klasse tragen (Pattern Overlap), Trade Overlap der RTC-Läufe, Vorzeichen der Erwartung je Aggregation und eine qualitative Stabilitätsaussage. Keine der verschobenen Aggregationen darf zur neuen Basis werden, keine wird ausgewählt, und ein Muster, dessen Erwartung nur auf der UTC-Aggregation positiv ist, wird als «grenzabhängig» vermerkt. Das ist für reine Candle-Muster die wichtigste Robustheitsprüfung, weil ein Hammer, der nur entsteht, wenn vier Stunden zufällig an der richtigen Stelle abgeschnitten werden, kein Marktphänomen ist. Voraussetzung sind 1h-Kerzen (Binance Spot und Perp, Kraken 60 Minuten aus dem Archiv), die noch nicht geladen sind.

## 9. Universum

Vorgesehen: BTC, ETH, SOL, XRP, DOT, LINK, AVAX, ADA, DOGE, LTC (Vorgabe vom 17.09.2026). Zeitebenen: 1d (struktureller Kontext), 4h (primär), 1h (Entry-Bestätigung und Grenzendiagnose), keine 15-Minuten-Ebene. Flow-Merkmale werden auf Binance (primärer Flow- und Derivate-Feed) berechnet, Formmerkmale zusätzlich auf Kraken (Ausführungs- und Realitätsprüfung) und, soweit Daten reichen, OKX (Cross-Venue-Gegenprobe, Kerzen ab Juli 2023). Datenstand: Für neun davon werden 4h- und Vollspalten-Daten gerade geladen, DOGE ist nicht im bisherigen Zehner-Universum (dort BNB) und hat keine Daten (Binance DOGEUSDT Spot ab 2019-07, Perp ab 2020-07, Kraken-Archiv XDGUSD). Offene Entscheidung: Universum auf elf Coins erweitern (DOGE nachladen, BNB bleibt als Datenbestand) oder DOGE weglassen. Die Bibliothek ist coin-agnostisch, die Entscheidung betrifft nur den Datenbestand.

## 10. Offene Entscheidungen vor dem Freeze der Bibliothek

1. Schwellen aus Abschnitt 1 (kleiner Body 0.30, Doji 0.10, langer Docht 2.0 mal Body und 0.5 mal Range, kurzer Docht 0.15) bestätigen. Referenz: TA-Lib-Standardwerte liegen in derselben Grössenordnung, sind aber teilweise über gleitende Mittel definiert.
2. Kontextfenster (EMA50, 1.5 ATR, 120 Kerzen) bestätigen.
3. Swing-Bestätigung 3/3 Kerzen bestätigen.
4. Inverted Hammer nur im Informationswert-Test (Empfehlung) oder auch in der Bottom Entry Engine.
5. DOGE (Abschnitt 9).
6. Horizonte und Blocklänge des Informationswert-Tests bestätigen.
7. Niveau-Fenster 120 und 240 Kerzen, Zonen-Toleranz 0.5 ATR, Mindestberührungen 3 bestätigen.
8. Failed-Breakdown-Schwellen (Durchstich 0.1 Prozent, Docht 0.5 ATR und 1.5 mal Body) bestätigen.
9. 1h-Kerzen laden (Binance Spot und Perp 1h, Kraken 60 aus dem Archiv) für Grenzendiagnose und Entry-Bestätigung: Empfehlung ja, als Loader-Erweiterung nach dem laufenden 4h-Lauf.

Nach Klärung: Version 1.0, Prüfsumme in ENTSCHEIDE, Umsetzung, Look-ahead-Test, dann Informationswert-Test auf dem Discovery-Fenster.
