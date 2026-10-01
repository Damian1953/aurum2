# CARRY_PREREG v0.9: Delta-neutraler Funding-Carry auf Kraken (BTC, ETH)

**Project Aurum II, `01_forschung/13_carry/carry_prereg_v0.9.md`, Stand 01.10.2026, 22:00 Zürich.**

**Status: VERWORFEN (Entscheid Damian 2026-10-01 22:16), nicht eingefroren, nicht gelaufen.** Der Entwurf wird nur zur Dokumentation abgelegt. Es gibt keinen Freeze, keinen Lauf, kein Review und keinen Paper-Betrieb. Die Deklaration der Vorbelastung (§0.1, §0.3, §8) bleibt für jede spätere Wiederaufnahme verbindlich.

Ursprünglicher Status bis 22:16: Entwurf zur Review durch Claude, danach Freigabe Damian.

Grundlage:
- Entwurf v0.1 `01_forschung/12_ideen_scan/carry_prereg_entwurf_v0.1.md` (SHA caebba226564477b…), bleibt unverändert.
- Ideen-Scan v1 `01_forschung/12_ideen_scan/ideen_scan_v1.md` (SHA 90804578a6d3d292…), §1.
- ENTSCHEIDE: 2026-09-15 «Funding ist Kostenposition», Stufe-2-Lauf 2026-09-16 (D-CC), Lane-C-Befund 2026-09-17, B5, C1, C2, C3, D1, D3, D4, F1, A7 (als Vorbild der Abbruchregel).
- Governance v1.1 `00_doku/aurum_governance_evidence_v1.1.md` (SHA 03f40ee6…), insbesondere Evidenzklassen und §7 Economic Validation Gate.
- Kostenmodell `config/cost_model_v1.json` v1.1 (SHA c652caa5bb237914…), Abschnitt `venue_kraken`.

---

## 0. Wichtigste Änderungen gegenüber v0.1 und eine Korrektur der Ausgangslage

### 0.1 Korrektur: Der Zeitraum ab 2024 ist für Carry NICHT unberührt

Der Auftrag und der Ideen-Scan (§1, «Als Carry-Outcome wurde sie nie ausgewertet») gehen davon aus, dass 2024+ für einen sauberen vorregistrierten Test frei ist. Das trifft nicht zu. Belegt im Repo:

| Vorbelastung | Quelle | Was bereits bekannt ist |
|---|---|---|
| **Stufe 2, D-CC Cash-and-Carry** (formaler, vorregistrierter Test, Lauf 16.09.2026) | `01_forschung/02_strategien/stage2_summary.md`, ENTSCHEIDE 2026-09-16 | Spot long + Perp short, Einschalten bei f_7d ≥ 10 % p. a., Ausstieg bei f_7d ≤ 0, Binance-Funding **2020-01 bis 2026-09-14**, zehn Coins inkl. BTC/ETH. Jahresrenditen (Notional 1.0) 2024 +12 %, 2025 +3 %, 2026 bisher +2 %. Jitter 5/15 %, 3/14 Tage. Urteil bestanden, mit Datenvorbehalt Kraken |
| **Kraken-Gegenprobe Stufe 2 §9** | `01_forschung/02_strategien/kraken_funding_crosscheck.json` | 349 Tage Kraken-Funding (Überlappungsjahr): Mittel f_7d BTC 3.1 %, ETH 2.8 % p. a.; Vorzeichenübereinstimmung mit Binance 84.5 / 88.3 % |
| **Strategiebewertung 15.09.2026** | `01_forschung/00_datenbasis/AURUM_II_STRATEGIEBEWERTUNG_2026-09-15.md`, ENTSCHEIDE 2026-09-15 | Kraken PF_XBTUSD 10.09.2025 bis 30.06.2026: +2.69 % p. a., ETH +3.05 % p. a. |
| **ENTSCHEIDE B5** | ENTSCHEIDE 2026-10-01 | «Für die XS21-Regel und für **D-CC** gilt der Zeitraum ab 2024 als verbraucht.» Einzige saubere Out-of-Sample-Evidenz ist ein Forward-Fenster |
| XS21 PiT v1.0 | ENTSCHEIDE 2026-10-01 13:55 | Binance-Funding 2024+ als Kostenposition der Short-Beine (indirekt) |

**Folge für das Design (verbindlich):** Ein retrospektiver Lauf auf 2024–2026 kann nur die Etikette **«Discovery/Robustheit mit Vorbelastung»** tragen (wie XS21 PiT nach B5). Er ist ein *Ausschlusstest* (scheitert die Konstruktion schon hier, wird die Linie geschlossen), aber kein Wirksamkeitsnachweis. Konfirmatorische Evidenz kann nur das Forward-Fenster auf Kraken-Daten nach dem Freeze liefern (§10). Das Etikett «Holdout validation» ist ausgeschlossen.

### 0.3 Nachtrag 22:15: Echte Kraken-Funding-Historie ab 2022 und deren Kenntnis (Vorbelastung)

- Eingang 01.10.2026, 22:15: Machbarkeitsstudie `fuer_aurum/andreas_carry_machbarkeit_v1.md` mit echten Kraken-Reihen PF_XBTUSD und PF_ETHUSD **2022-03-22 bis 2026-10-01** (`fuer_aurum/daten/`, SHA a4faf822… bzw. 0779644d…). Quelle: öffentliche Kraken-Support-ZIP «Export historical funding rates» (2022-03-22 16:00 bis 2026-02-01 00:00 UTC, ZIP-SHA 65ba6712a6ab6573…, am 01.10.2026 22:15 von der Box neu geladen) plus API v4.
- Provenienzprüfung (Box, 01.10.2026): ZIP gegen die gelieferten CSV 30'431 von 30'431 Stunden identisch (max. Abweichung 0), Collector gegen CSV 9'091 Stunden identisch. Bis 2022-09-29 Intervall 4 h, Normierung auf 1 h nicht verifiziert.
- **Gesehen und damit verbraucht:** Die Studie enthält Jahresmittel des Fundings (BTC 2022 +2.2 %, 2023 +8.9 %, 2024 +16.5 %, 2025 +7.6 %, 2026 +2.3 %; ETH −17.0 %, +9.4 %, +15.3 %, +3.9 %, +3.4 %), Gesamtmittel (BTC +8.1 %, ETH +4.0 % p. a.), schlechteste 30/365 Tage und negative Monate. Damit sind die Funding-Niveaus 2024+ auf Kraken vollständig bekannt. Ein retrospektiver Test 2024+ wäre keine unabhängige Evidenz mehr.
- Weitere Befunde der Studie, die in v1.0 eingeflossen wären: Zins von 0.0025 %/h (≈ 22 % p. a.) auf nicht durch USD gedeckte unrealisierte Verluste, getrennte Wallets als Standard (Unified Wallet: BTC/ETH 99 % Sicherheitswert), 0.20 % Umwandlungsgebühr, Gegenpartei Payward Digital Solutions Ltd (Bermuda, nicht FINMA-beaufsichtigt), Spot bei Payward Trading Ltd (BVI), steuerliche Behandlung des Fundings ungeklärt (KS 36).

### 0.2 Änderungen gegenüber v0.1

| Nr. | v0.1 | v0.9 | Grund |
|---|---|---|---|
| Ä1 | Testperiode A: Binance 2024-01 bis 2026-08, massgeblich | Binance nur noch **deskriptive Referenz** (§3.4) | Binance 2024+ in Stufe 2 D-CC verbraucht (B5); Binance hat einen Zinssockel, Kraken nicht; Venue ist Kraken |
| Ä2 | Periode B: Kraken nur ab 2025-09-17 | **Kraken-Reihe K\***: ab 2025-09-17 echtes Kraken-Funding, davor (2023-12-01 bis 2025-09-17) aus öffentlichen Kraken-Mark- und Indexkursen **rekonstruiertes** Funding, nur mit bestandenem Treue-Gate (§3.2) | einzige Kraken-nahe Quelle für 2024–2025; Kraken liefert Funding nur rollend für 1 Jahr |
| Ä3 | R1 dauerhaft primär, R2 Filter 7d > 0 sekundär | **Primär: Schwellenregel S** (Einstieg nur, wenn das 30-Tage-Funding die Kapitalhürde plus Kostenaufschlag übersteigt, §4.2). R1 dauerhaft nur noch Vergleich | Auftrag; der Filter 7d > 0 lohnte sich explorativ wegen der Spot-Kosten nicht; ein ökonomisch hergeleiteter Schwellenwert ist kein Tuning |
| Ä4 | Hürde DTB3 auf das Kapital, implizit | Explizite Überschussdefinition: Kapital ausserhalb des Markts verzinst zu DTB3, im Markt unverzinst (§5.1) | saubere Antwort auf «schlägt Carry den risikolosen Satz?» |
| Ä5 | Margin 50 %, Stressregel «+30 % seit Rebalancing» | Margin-Modell mit Bändern (½·m, 2·m), stündliche Liquidationsprüfung auf dem Mark-Hoch, Wartungsmarge 1 %, Liquidationskosten (§4.4, §4.5) | F1 verlangt ein Kapital- und Margin-Modell |
| Ä6 | Bootstrap-p < 0.05, Periode B nicht negativ, schlechteste 30 Tage > −3 % | Kriterien P1–P8 (§6), u. a. Mindestgrösse +1.0 Pp. p. a., Blockregel, Taker-K2-Pflicht, Mindestexposition | ein statistisch signifikanter, aber winziger Überschuss rechtfertigt Gegenpartei- und Steuerrisiko nicht |
| Ä7 | – | Deklaration aller Vortests (§8), Abbruchregel A-CARRY (§9), Forward- und Paper-Plan (§10) | Auftrag, Governance |

---

## 1. Hypothese

- **H-CARRY:** Eine delta-neutrale Position aus BTC- bzw. ETH-Spot long (Kraken Spot) und gleich grosser Short-Position im linearen Perpetual PF_XBTUSD bzw. PF_ETHUSD (Kraken Futures), eröffnet nur, wenn das nachlaufende Funding die Kapitalhürde deutlich übersteigt (Regel S, §4), erzielt nach allen Kosten eine Rendite auf das gebundene Kapital, die **über dem risikolosen USD-Satz** (FRED DTB3) liegt.
- **H0 (je Coin):** Der mittlere tägliche Überschuss über DTB3 ist ≤ 0.
- Getestet wird **je Coin** (BTC, ETH), zwei primäre Zellen, Holm über beide.
- Mechanismus: Long-Nachfrage nach Hebel erzeugt positive Prämien des Perps über dem Index; Shorts erhalten Funding (Schmeling/Schrimpf/Todorov 2023; He/Manela/Ross/von Wachter 2022). Gegenhypothese aus dem Repo (ENTSCHEIDE 2026-09-15): Auf Kraken ist Funding zu klein für einen eigenen Ertragsbaustein. Dieser Test entscheidet zwischen beiden Lesarten für BTC/ETH.

## 2. Instrumente, Venue, Konventionen

- Spot: Kraken Spot XBT/USD, ETH/USD (C1: Spot für die Long-Seite).
- Perp: Kraken Futures PF_XBTUSD, PF_ETHUSD (linear, USD-margined, Multi-Collateral), Funding stündlich (C3).
- F1 erfüllt: Spot und Perp auf derselben Börse (Kraken), Kapital- und Margin-Modell in §4.4–4.5. Die Bedingung von F1 («bis XS21 PiT und DT entschieden sind») ist seit 01.10.2026 erfüllt (XS21 falsifiziert, Lane A geschlossen).
- **Funding-Vorzeichen (Kraken):** `relativeFundingRate` > 0 heisst, Longs zahlen Shorts. Unser Short-Bein **erhält** bei positiver Rate und **zahlt** bei negativer Rate. Zahlung je Stunde an das Short-Bein: `+ q · fundingRate_abs(h)` in USD (absolute Rate = USD je Kontrakt bzw. Basiseinheit und Stunde) bzw. gleichwertig `+ q · relativeFundingRate(h) · Index(h)`. Eine Position, die während der ganzen Stunde [h, h+1) offen ist, erhält die Rate der Stunde h. Ein- und Ausstiege liegen immer auf vollen Stunden, Teilstunden gibt es nicht.
- **Zeitstempel-Semantik:** zu prüfen in Datenprüfung D2 (§7): ob der Zeitstempel des Kraken-Endpunkts den Beginn oder das Ende der Abrechnungsstunde bezeichnet. Die Regel ist so formuliert, dass eine Rate nie vor ihrer Veröffentlichung in ein Signal eingeht (§4.2).
- **Funding-Vorzeichen (Binance, nur Referenz):** gleich (positiv: Longs zahlen Shorts), Abrechnung alle 8 h um 00/08/16 UTC an Positionen, die zu diesem Zeitpunkt offen sind.
- **Annualisierung:** Kraken stündlich ×8760, Binance je 8 h ×1095. Raten werden als Bruchteile geführt.
- Zeitzone aller Regeln: UTC. Tagesentscheid um 00:00 UTC (02:00 Zürich im Sommer).

## 3. Daten und Zeitraum

### 3.1 Befund Datenverfügbarkeit (geprüft 01.10.2026, nur Abdeckung, keine Werte ausgewertet)

| Quelle | Abdeckung PF_XBTUSD / PF_ETHUSD | Bemerkung |
|---|---|---|
| Kraken Futures `GET /derivatives/api/v4/historicalfundingrates` | rollendes Fenster: heute ab **2025-10-01 08:00 UTC** (8765 Stunden) | keine Historie davor, auch nicht über CCXT (Lane-C-Befund 2026-09-17). Das Fenster wandert täglich |
| Collector `/workspace/aurum2/data_live/kraken_futures_funding/` | **2025-09-17 08:00 UTC bis 2026-10-01 10:00 UTC**, 9091 Zeilen je Symbol, append-only | die ersten zwei Wochen (17.–30.09.2025) existieren nur noch hier; Kopie `data/raw/kraken_futures_funding/` bis 2026-09-17 |
| Original-Dateien Stufe 2 `kraken_funding/PF_{XBT,ETH,SOL}USD_funding.csv` (ab 10.09.2025) | **fehlen** (OP-4) | nicht wiederherstellbar |
| Kraken Futures Charts `GET /api/charts/v1/{mark,spot,trade}/PF_XBTUSD/{1m,1h,1d}` | **ab 2022-03-22** (1d), 1m und 1h für 2024 geprüft, 2000 Kerzen je Abfrage mit Paging | Grundlage für die Rekonstruktion (§3.2) und für Kurse beider Beine. Der Tick-Typ `spot` wird als CF-Real-Time-Index angenommen (Prüfung D3) |
| Binance USDT-M Funding (`data/raw/binance_funding/`, Collector) | 2020-01-01 bis 2026-08-31 (raw) bzw. 2026-09-30 (Collector), 8 h | fapi geoblockt, nur data.binance.vision; Zinssockel 0.01 %/8 h |
| Kraken Spot OHLC 1h (`data/raw/kraken_1h`, Archiv) | bis 2026-06-30; Collector 1h erst ab 2026-08-18; 1d bis 2026-09-30 | Lücke Juli/August 2026 in 1h; deshalb nur Gegenprobe, nicht Kursquelle |
| DTB3 (`data/supplement/DTB3_3m_tbill_to_2026-09-14.csv`) | bis 2026-09-14 | wird bei der Datenbeschaffung von FRED nachgeführt (Provenienz), sonst vorwärts gefüllt |

### 3.2 Primäre Reihe K\* und Treue-Gate G-R

- **K-ist:** echtes Kraken-Funding aus dem Collector, ab 2025-09-17 08:00 UTC.
- **K-rek:** rekonstruiertes Kraken-Funding 2023-12-01 00:00 UTC bis 2025-09-17 07:00 UTC, nach der veröffentlichten Kraken-Methode (Kraken MTF, Linear Contract Specifications, abgerufen 01.10.2026):
  - je Minute m: Prämie p_m = (Mark_close_m − Index_close_m) / Index_close_m aus den 1m-Kerzen `mark` und `spot`;
  - je Stunde h: Durchschnittsprämie = Mittel der mittleren 30 der 60 Minutenwerte (getrimmt), geteilt durch den Multiplikator n = 8, begrenzt auf [−0.5 %, +0.5 %] je Stunde;
  - diese Rate gilt für die **folgende** Stunde h+1 (Kraken: Rate für 12–13 UTC wird im Fenster 11–12 UTC berechnet);
  - fehlen in einer Stunde mehr als 10 von 60 Minuten, ist die Stunde K-rek-fehlend (Behandlung D5).
  - Bekannte Abweichung: Kraken rechnet mit dem Impact-Mid aus dem Orderbuch, der Mark-Preis enthält einen 30-s-EMA dieses Impact-Mid. Die Rekonstruktion ist deshalb eine Näherung.
- **Treue-Gate G-R** (im Lauf, vor jeder Strategierechnung, auf dem Überlappungsfenster 2025-09-17 08:00 bis 2026-09-30 23:00 UTC, K-rek dort ebenfalls berechnet):
  - (i) Korrelation der Tagessummen K-rek gegen K-ist ≥ 0.80;
  - (ii) |annualisiertes Mittel K-rek − K-ist| ≤ 1.5 Prozentpunkte;
  - (iii) Übereinstimmung des Einstiegszustands von Regel S (§4.2, Bedingung E1 ohne Positionszustand) an ≥ 90 % der Tage.
  - **G-R bestanden (je Coin):** Primärreihe K\* = K-rek bis 2025-09-17 07:00 UTC, danach K-ist. Keine Kalibrierung, keine Skalierung, keine Anpassung von K-rek an K-ist.
  - **G-R nicht bestanden:** Primärperiode schrumpft auf K-ist allein (Signal ab 2025-10-17, Test bis 2026-09-30). K-rek wird nur deskriptiv berichtet. Wegen der kurzen Periode gilt dann zusätzlich die Mindestexposition P8 unverändert; wird sie verfehlt, lautet das Urteil «NICHT TESTBAR» (§6.3).
- Vermerk zur Vorbelastung des Gates: Das Niveau von K-ist im Überlappungsfenster ist teilweise bekannt (§0.1). Das Gate prüft nur die Treue der Rekonstruktion, nicht das Ergebnis.

### 3.3 Zeitraum

- **Primärperiode (Lauf R):** 2024-01-01 00:00 UTC bis 2026-09-30 23:00 UTC (rund 33 Monate). Signal-Vorlauf ab 2023-12-01 (Discovery-Zeitraum, nur für den Signalaufbau).
- **Kalenderblöcke:** B2024 (2024-01-01 bis 2024-12-31), B2025 (2025-01-01 bis 2025-12-31), B2026 (2026-01-01 bis 2026-09-30).
- **Teilperiode K-ist:** 2025-09-17 08:00 UTC bis 2026-09-30, separat ausgewiesen (Kriterium P7).
- **Datenstand:** Alle Lauf-Eingaben werden bei der Datenbeschaffung nach dem Freeze mit Prüfsumme eingefroren, Stichtag 2026-09-30 23:00 UTC. Später gesammelte Daten gehören zum Forward-Fenster (§10), nicht zum Lauf R.
- **Evidenzklasse Lauf R:** «Discovery/Robustheit mit Vorbelastung» (B5). Kein «Holdout validation».

### 3.4 Binance-Referenz (deskriptiv, ohne Gewicht)

Dieselben Regeln mit Binance-Funding BTCUSDT/ETHUSDT 2024-01-01 bis 2026-08-31, Kurse wie K\* (Kraken Mark/Index). Zweck: Grösse des Unterschieds «mit Zinssockel gegen ohne». Kein Kriterium, kein Urteil, Vermerk «in Stufe 2 D-CC verbraucht».

### 3.5 Holdout-Sperre

- Der Lauf liest **keine** Datei unter `02_daten/holdout/` und öffnet `holdout_manifest_v1*.json` nicht. Die Loader-Sperre (`AURUM_VALIDATION`) wird nicht gesetzt.
- Alle Kraken-Kurse und K-rek kommen neu aus der öffentlichen Charts-API, K-ist aus dem Collector, Binance-Funding aus `data/raw/binance_funding/` (Stufe-2-Quelle, nicht Holdout).
- `make ci` prüft das Manifest nur per Prüfsumme (bestehende CI, unverändert).

## 4. Regeln

### 4.1 Parameter (alle jetzt fixiert)

| Symbol | Wert | Herleitung |
|---|---|---|
| m (Margin-Ziel, Anteil am Perp-Notional) | 0.50 | v0.1; Kapitalfaktor 1 + m = 1.5 |
| Hürde H_t | (1 + m) · DTB3_t | Break-even: im Markt sind Spot und Margin unverzinst, Funding fliesst nur auf das Notional N = C/(1+m) |
| Kostenaufschlag Δ | 5.0 Prozentpunkte p. a. | ein Roundtrip beider Beine kostet 1.02 % des Notionals (§5.2); über eine Episode von 75 Tagen amortisiert ≈ 5.0 % p. a. |
| Signalfenster lang L | 30 Tage (720 Stunden) | neu, nicht in Stufe 2 oder im Scan getestet |
| Signalfenster kurz | 7 Tage (168 Stunden) | aus Stufe 2 D-CC übernommen (Ausstiegslogik f_7d ≤ 0), keine Neuwahl |
| Margin-Bänder | unten ½·m = 0.25, oben 2·m = 1.00 | symmetrisch in log, kein Tuning |
| Wartungsmarge im Modell MM | 1.0 % des Notionals | Kraken BTC/ETH-Perp Level I verlangt 0.5 %, Level II 1.0 %; konservativ |
| Liquidationskosten | 1.0 % des Notionals plus Taker-Futures und Spot-Notverkauf zu taker_K2 mit slip_sl | konservative Annahme, Kraken-Liquidationsgebühr nicht öffentlich beziffert (Frage Q9) |
| Prüftakt Margin | täglich 00:00 UTC (Rebalancing), stündlich (Liquidationsprüfung) | Paper-Job läuft täglich; Liquidation wird stündlich auf dem Mark-Hoch geprüft |

### 4.2 Signal, Einstieg, Ausstieg (Regel S, primär)

- F30_t = Mittel der stündlichen Kraken-Raten (K\*) der letzten 720 Stunden vor t, ×8760. F7_t analog über 168 Stunden.
- Verwendet werden nur Raten, deren Abrechnungsstunde **vor** t abgeschlossen ist. DTB3_t ist der letzte FRED-Wert mit Datum ≤ Vortag von t.
- Entscheid täglich um t = 00:00 UTC, Ausführung beider Beine zum Schluss der Stunde 00:00–01:00 UTC (Kurs = 1h-Schluss, plus Slippage). Funding läuft ab 01:00 UTC.
- **Einstieg (E1 ∧ E2), wenn flach:** E1: F30_t ≥ H_t + Δ; E2: F7_t > 0.
- **Ausstieg (X1 ∨ X2), wenn investiert:** X1: F30_t < H_t; X2: F7_t < 0.
- Zahlenbeispiel zur Orientierung (DTB3 2024 im Mittel 4.97 %, 2026 bisher 3.65 %): Einstieg ab F30 ≈ 12.5 % (2024) bzw. ≈ 10.5 % (2026), Ausstieg unter ≈ 7.5 % bzw. ≈ 5.5 %.
- Keine Mindesthaltedauer, keine Abkühlphase, kein Gewinnziel (ENTSCHEIDE 2026-09-15 «Kein Profit-Guard»).

### 4.3 Hedge-Verhältnis

- Gleiche Menge in Coin-Einheiten: q_spot = q_perp = q. Das lineare PF-Kontrakt-P&L ist −q·ΔP, das Spot-P&L +q·ΔS. Das Delta ist damit bis auf die Basis (Perp gegen Index) null, ein Delta-Rebalancing entfällt.
- Beim Einstieg: q = C / ((1 + m) · S), wobei C das gesamte Kapital der Zelle ist. Spotwert N = q·S, Margin M = m·N im Futures-Konto (USD).
- Im Backtest ohne Rundung auf Mindestlose (PF_XBTUSD 0.0001 BTC, PF_ETHUSD 0.001 ETH); im Paper mit Rundung, Referenzkapital 10'000 USD je Coin.

### 4.4 Margin-Modell und Rebalancing

- Futures-Equity E = M + unrealisiertes Perp-P&L + erhaltenes/gezahltes Funding. Margin-Quote r = E / (q · Mark).
- **Tägliche Prüfung 00:00 UTC:** liegt r < 0.25 oder r > 1.00, wird auf r = m = 0.50 zurückgeführt:
  - Gesamtwert V = q·S + E; Zielmenge q' = V / ((1 + m) · S);
  - beide Beine werden um |q − q'| angepasst, der USD-Überschuss bzw. -Bedarf zwischen Spot- und Futures-Konto übertragen (intern, kostenlos, Annahme);
  - Kosten: maker_plan Spot und Futures-Maker (planbare Order).
- Kein Ein- oder Ausstieg wird durch ein Rebalancing ausgelöst. Rebalancing ist auch bei R1 aktiv.

### 4.5 Liquidationsmodell

- **Stündlich:** E_h,worst = E zum letzten Stundenschluss − q · (Mark_high_h − Mark_close_{h−1}). Gilt E_h,worst ≤ MM · q · Mark_high_h, ist die Position **liquidiert**:
  - Perp geschlossen zu Mark_high_h, Kosten: 1.0 % Liquidationszuschlag plus Futures-Taker (0.05 % + 0.02 % Reibung);
  - Spot-Bein zum Schluss der Folgestunde verkauft, taker_K2 mit slip_sl (0.80 % + 0.06 % + 0.30 %);
  - danach flach bis zum nächsten Einstiegssignal.
- Jede Liquidation wird gemeldet. Eine Liquidation im Primärmodell verletzt P5.
- Grobe Einordnung (keine Datenrechnung): Mit m = 0.50 und täglichem Prüftakt braucht eine Liquidation einen Anstieg innerhalb eines Tages von rund +23 % (Margin-Quote knapp über dem unteren Band 0.25) bis +48 % (Quote 0.50). Mit m = 0.33 sind es rund +15 % bis +32 %.

### 4.6 Vergleichsregeln (vorregistriert, ohne Kriterium)

- **R1 dauerhaft:** Einstieg 2024-01-01 01:00 UTC, kein Ausstieg bis Periodenende, Rebalancing und Liquidation wie oben.
- **S-Margin:** Regel S mit m = 0.33 und m = 1.00 (Bänder ½·m, 2·m, Hürde (1 + m)·DTB3).
- **S-Cash0:** Regel S, Kapital ausserhalb des Markts unverzinst (realistischer für USD auf dem Kraken-Konto).
- **S-4h:** Regel S mit Entscheid alle 4 Stunden (nur Bericht).
- **S-Binance:** §3.4.

## 5. Erträge, Kosten, Überschuss

### 5.1 Überschussdefinition

- Kapital C je Coin (Start 1.0). Tageswert V_d um 00:00 UTC.
- **Im Markt:** V = q·S + E. Spot-Bestand und Margin sind unverzinst (kein Staking, kein Zins auf USD-Collateral).
- **Ausserhalb des Markts (primär):** V wächst mit rf_d = (1 + DTB3_d)^(1/365) − 1 (Konvention Stufe 2, s2lib). Der Überschuss ist dann exakt null.
- **Täglicher Überschuss:** e_d = V_d / V_{d−1} − 1 − rf_d.
- **Annualisierter Überschuss:** ē · 365 (arithmetisch), dazu geometrisch berichtet.
- Alle Zahlen in USD. CHF-Sicht nur als Frage (Q12), kein Kriterium.

### 5.2 Kosten (aus `config/cost_model_v1.json`, Abschnitt `venue_kraken`, Bruchteile je Seite)

| Vorgang | Spot | Futures | Summe je Seite |
|---|---|---|---|
| Planbar (Einstieg, Ausstieg, Rebalancing), primär `maker_plan` + Futures `maker` | 0.40 % + 0.02 % Reibung + 0.05 % Slippage = 0.47 % | 0.02 % + 0.02 % = 0.04 % | 0.51 %; Roundtrip beider Beine 1.02 % des Notionals |
| Pflicht-Sensitivität `taker_K2` + Futures `taker` (C2) | 0.80 % + 0.06 % + 0.15 % = 1.01 % | 0.05 % + 0.02 % = 0.07 % | 1.08 %; Roundtrip 2.16 % |
| Zwangsvorgang (Liquidation) | 0.80 % + 0.06 % + 0.30 % (slip_sl) = 1.16 % | 0.05 % + 0.02 % + 1.00 % Liquidationszuschlag | |

- Funding mit Vorzeichen je Abrechnungsstunde (§2), keine Gebühr auf Funding (Kraken MTF).
- Interne Übertragungen Spot ↔ Futures: kostenlos, ohne Verzögerung (Annahme, Frage Q8).
- Basis: Ein- und Ausstieg des Perps zum Mark-1h-Schluss, des Spots zum Index-1h-Schluss, die Basisänderung geht ins Ergebnis ein.
- Das Kostenmodell wird nicht geändert. Eine neue Kraken-Gebührenstufe gilt erst mit neuer Version des Kostenmodells.

## 6. Statistik, Kriterien, Urteil

### 6.1 Signifikanz

- Teststatistik je Coin: mittlerer täglicher Überschuss ē über die Primärperiode.
- Stationärer Block-Bootstrap (Politis-Romano, wie `s2lib.block_bootstrap`), mittlere Blocklänge 30 Tage, B = 10'000, Seed 20261001.
- Einseitiger p-Wert auf der zentrierten Reihe: p = (1 + #{ē*_b − ē ≥ ē}) / (B + 1).
- **Holm über die zwei primären Zellen** (BTC, ETH), α = 0.05.
- Gegenprobe, nur berichtet: Newey-West-t (Lag 30), Deflated Sharpe Ratio mit N = 262 Trials (§8). PBO entfällt, weil keine Parameterfamilie zur Auswahl steht.

### 6.2 Kriterien je Coin (alle müssen erfüllt sein)

| Nr. | Kriterium |
|---|---|
| P1 | Holm-adjustiertes einseitiges p < 0.05 (Regel S, Primärmodell) |
| P2 | Annualisierter Netto-Überschuss ≥ +1.0 Prozentpunkte p. a. auf das Kapital (Mindestgrösse für nicht modellierte Gegenpartei-, Betriebs- und Steuerrisiken) |
| P3 | Überschuss > 0 in mindestens zwei der drei Kalenderblöcke (ein Block ohne jede Marktzeit zählt mit 0, also nicht als positiv) |
| P4 | Schlechteste rollende 30-Tage-Summe des Überschusses ≥ −3.0 % des Kapitals |
| P5 | Keine Liquidation im Primärmodell |
| P6 | Pflicht-Sensitivität taker_K2: annualisierter Überschuss > 0 (Punktschätzer) |
| P7 | Teilperiode K-ist: annualisierter Überschuss ≥ −1.0 Prozentpunkte p. a. |
| P8 | Mindestexposition: mindestens 60 Tage im Markt in der Primärperiode |

### 6.3 Urteil

- **BESTANDEN:** mindestens ein Coin erfüllt P1–P8. Nur bestandene Coins sind Paper-Kandidaten. Bedeutung nach §0.1: «Konstruktion nicht ausgeschlossen, Forward-Test zulässig», ausdrücklich **kein** Wirksamkeitsnachweis.
- **NICHT BESTANDEN:** kein Coin erfüllt P1–P8. Teilerfolge (z. B. nur P1 verfehlt) zählen nicht. Es folgt die Abbruchregel §9.
- **NICHT TESTBAR:** G-R verfehlt **und** P8 verfehlt, oder eine Datenprüfung (§7) scheitert unbehebbar. Behandlung wie NICHT BESTANDEN, mit Vermerk; eine Wiederaufnahme nur über das Forward-Fenster (§9).
- Vergleichsregeln (§4.6) und Binance-Referenz ändern kein Urteil.

### 6.4 Pflichtbericht

Je Coin und Regel: Überschuss gesamt und je Block, Funding brutto, Kosten nach Art, Basis-P&L, Anzahl Einstiege, Marktzeit, Haltedauern, Rebalancings, minimale Margin-Quote, Liquidationen, schlechteste 30 Tage, Anteil negativer Funding-Stunden während der Marktzeit, G-R-Werte, K-rek gegen K-ist, Binance-Referenz.

## 7. Ablauf nach dem Freeze und Prüfungen vor dem Lauf (noch nicht ausgeführt)

Reihenfolge wie XS21 PiT (§7 dort):
1. Freeze dieser Spezifikation (v1.0) nach Review und Freigabe: Tag `carry-v1.0-freeze`, SHA in ENTSCHEIDE.
2. Datenbeschaffung, nur öffentliche Endpunkte, ohne Keys: Kraken-Charts 1m/1h `mark` und `spot` für PF_XBTUSD/PF_ETHUSD 2023-12-01 bis 2026-09-30; Kopie K-ist aus dem Collector; DTB3 von FRED nachgeführt. Provenienz und Prüfsummen.
3. Datenprüfungen (outcome-blind, ohne Strategierechnung, Ergebnis ins Log):
   - D1 Vollständigkeit: Anteil fehlender Stunden je Reihe ≤ 1 %, fehlender Minuten in K-rek ≤ 2 %.
   - D2 Einheit und Zeitstempel K-ist: fundingRate_abs ≈ relativeFundingRate × Index (Median der relativen Abweichung ≤ 2 %); Zeitstempel-Semantik aus der Kraken-Dokumentation und dem Abgleich mit K-rek-Verschiebung um ±1 h (nur Korrelation, keine Mittelwerte).
   - D3 Index-Annahme: Charts-`spot` gegen Kraken-Spot-1h-Schluss, Median |Abweichung| ≤ 0.10 % (Fenster mit Kraken-Spot-1h).
   - D4 Mark-Plausibilität: |Mark/Index − 1| ≤ 1 % in ≥ 99.9 % der Stunden (Kraken deckelt die Prämie bei 1 %).
   - D5 Lücken: fehlende Stunden in K-rek oder K-ist werden mit Rate 0 gefüllt **und** gezählt; liegt der Anteil gefüllter Stunden in der Marktzeit über 2 %, Vorbehalt im Bericht.
4. Lauf-Code und Tests freezen (Tag `carry-v1.0-runcode`), mit synthetischen Tests: Vorzeichen, Look-ahead (Störung nach t ändert keinen Entscheid vor t), Liquidation, Rebalancing, Kosten.
5. **Genau ein Lauf.** Das Lauf-Log enthält die SHA der eingefrorenen Spezifikation und die SHAs aller Eingaben (E3).
6. Unabhängige Nachrechnung (Prüfskript), Bericht, ENTSCHEIDE-Eintrag.

Scheitert eine Datenprüfung, wird **vor** dem Lauf ein datierter Eintrag in ENTSCHEIDE geschrieben (Abweichung oder Abbruch), ohne Blick auf Ergebnisse.

## 8. Deklaration der Vortests und Trial-Zählung

| Vortest | Art | Daten | Zählung |
|---|---|---|---|
| Stufe 2 D-CC (Primär + 4 Jitter) | formal, vorregistriert | Binance 2020-01 bis 2026-09-14, zehn Coins | 5 formale Trials (in der globalen Zahl enthalten) |
| Kraken-Gegenprobe Stufe 2 §9 | formal, Datenprüfung | Kraken 349 Tage | 1 |
| Strategiebewertung 15.09.2026, Kraken-Funding-Niveaus | deskriptiv | Kraken 10.09.2025–30.06.2026 | 1 |
| Ideen-Scan v1, Carry-Teil (dauerhaft 1.5× je Jahr, Filter 7d > 0, BTC/ETH/SOL) und übrige Scan-Checks | explorativ, nicht vorregistriert | Binance bis 2023-12-31 | rund 20 informelle Trials für den ganzen Scan |
| XS21 PiT v1.0 | formal | Binance-Funding 2024+ als Kostenposition | indirekt, nicht als Carry-Trial gezählt |
| Globale Trial-Zahl Aurum II vor dem Scan | | | rund 240 (A8) |

- Für DSR (§6.1) gilt N = 240 + 20 + 2 = **262**.
- Ausdrückliche Erklärung (zu wiederholen beim Freeze): Bis zur Erstellung dieses Entwurfs wurde **keine** Strategie-Rendite mit Regel S, mit der Rekonstruktion K-rek oder auf Kraken-Daten 2024–2025 berechnet. Die Kraken-Rohreihen wurden für diesen Entwurf nur auf Abdeckung (erste/letzte Zeitstempel, Zeilenzahl) geprüft.
- Nicht mehr unabhängig: Die Wahl der Konstruktion (Spot long + Perp short, BTC/ETH) und das Wissen um die Funding-Spitzen 2024 sind outcome-informiert. Deshalb der Evidenzdeckel in §3.3.

## 9. Abbruchregel A-CARRY

Vor dem Lauf festgeschrieben (Wortlaut zur Übernahme in ENTSCHEIDE beim Freeze):

«Lautet das Urteil von CARRY v1.0 NICHT BESTANDEN oder NICHT TESTBAR, wird die Linie ‹delta-neutraler Funding-Carry Spot/Perp auf BTC und ETH› geschlossen. Es folgt keine weitere Variante auf Daten bis 2026-09-30: keine anderen Schwellen, Fenster, Margin-Faktoren, Coins, Börsen, Hebel oder Terminkontrakte (Basis-Carry). Eine Wiederaufnahme ist nur mit Forward-Daten ab dem Freeze-Datum über mindestens 12 Monate und einer neuen Vorregistrierung zulässig, die diesen Entscheid ausdrücklich zitiert. Der Collector sammelt weiter (E2).»

Lauf-Abbruch (technisch): bricht der Lauf mit einem Fehler ab, wird nicht neu gestartet, bevor ein ENTSCHEIDE-Eintrag die Ursache benennt und bestätigt, dass keine Outcome-Zahl gesehen wurde. Sind Outcome-Zahlen sichtbar geworden, gilt der Lauf als durchgeführt.

## 10. Bei BESTANDEN: Forward, Paper, Micro-Live

1. **Ausführbarkeits-Gate (wie B6), vor Paper:** Damian prüft manuell die Eignung für Kraken Derivatives bzw. Kraken MTF (Vertragspartnerin, Hebel- und Margin-Regeln je Entity) und D4 Grundsatz; Mindestlose und Rundung bei 10'000 USD je Coin; Datenpfad des Paper-Jobs (Collector v1.2 muss Mark und Index stündlich für PF_XBTUSD/PF_ETHUSD speichern, offen).
2. **Paper-Betrieb (Forward-Fenster):** Start an dem ersten 00:00 UTC nach Damians Paper-Freigabe, nur bestandene Coins, Regeln und Kosten unverändert eingefroren, ohne Keys, ohne Orders, auf der Agent-Box (D1-Vorschlag, Bestätigung ausstehend). Echtes Kraken-Funding aus dem Collector, keine Rekonstruktion.
3. **Paper-Abbruch (sofort, mit Meldung an Damian):** simulierte Liquidation oder r < 2·MM; kumulierter Überschuss < −2.0 % des Kapitals; Datenausfall > 72 h; Änderung der Kraken-Funding-Methode (z. B. Einführung eines Zinssockels) oder der Margin-Regeln. Danach Review, kein stilles Weiterlaufen.
4. **Review nach höchstens 4 Monaten (D3):** deskriptiv, keine Signifikanz verlangt. Ergebnis ist eine Entscheidvorlage für Damian (≤ 15 Minuten): weiterführen, abbrechen oder Micro-Live beantragen.
5. **Micro-Live nur mit ausdrücklicher Freigabe durch Damian** und frühestens nach dem 4-Monats-Review, wenn zusätzlich gilt: Forward-Überschuss (Punktschätzer) > 0, kein Paper-Abbruch, **D2** entschieden (Micro-Live-Betrag, Totalverlust-Obergrenze in CHF), **D4** geklärt (Steuer: Funding vermutlich Einkommen; KS 36; Vertragspartnerin), Keys nie auf der Agent-Box (D1). Kein automatischer Übergang.
6. **Forward validation (Evidenzklasse):** frühestens nach 12 Monaten Forward-Daten, mit denselben Kriterien P1, P2, P4–P8 und der Blockregel P3 auf Quartalen (≥ 3 von 4 positiv). Der Wortlaut dieses Forward-Tests wird mit diesem Dokument eingefroren.

Bei NICHT BESTANDEN gibt es keinen Paper-Betrieb. Die Forward-Datensammlung (Collector) läuft weiter.

## 11. Erwartung vor dem Lauf (ohne Outcome-Rechnung, nur aus bereits Bekanntem)

- Die bekannten Kraken-Niveaus 2025-09 bis 2026-06 (BTC ≈ 2.7–3.1 %, ETH ≈ 2.8–3.1 % p. a.) liegen deutlich unter der Hürde (1.5 × DTB3 ≈ 6 %) und weit unter der Einstiegsschwelle (≈ 11 %). Regel S wird in diesem Zeitraum vermutlich selten investiert sein.
- Das Urteil hängt damit fast ganz an 2024 und Anfang 2025 (K-rek). In Stufe 2 war 2024 auf Binance ein starkes Carry-Jahr (+12 % auf das Notional, mit Zinssockel).
- Ein NICHT BESTANDEN ist wahrscheinlich und wäre ein nützliches, sauberes Ergebnis: Es schliesst die Linie, bevor Konto, Steuerklärung und Betreuung Damians Zeit kosten.

## 12. Verbote

Kein Lauf vor dem Freeze. Keine Coins ausser BTC und ETH. Keine Parameteränderung nach Sicht. Keine Keys, kein Börsenkontakt ausser öffentlichen Marktdaten, kein Trading. Kein Zugriff auf `02_daten/holdout/` und das Manifest. Kein zweiter Lauf.

## 13. Fragen für das Methodik-Review (Claude)

1. **Evidenzklasse und Sinn des Laufs R.** Ist ein retrospektiver Lauf, der wegen B5 nur «Discovery/Robustheit mit Vorbelastung» sein kann, als reiner Ausschlusstest vor dem Forward-Fenster gerechtfertigt? Oder sollte direkt nur forward getestet werden (Kosten: 12+ Monate)?
2. **Rekonstruktion K-rek.** Ist die Rekonstruktion aus 1m-Mark minus Index (getrimmtes Stundenmittel / 8, Wirkung in h+1) methodisch vertretbar, obwohl Kraken das Impact-Mid und nicht den Mark-Preis verwendet? Sind die Gate-Schwellen G-R (Korrelation ≥ 0.80, Niveaudifferenz ≤ 1.5 Pp., Zustandsübereinstimmung ≥ 90 %) streng genug, und ist es richtig, bei Nichtbestehen auf K-ist allein zu schrumpfen statt zu kalibrieren?
3. **Primärreihe.** Ist es richtig, Binance trotz längerer echter Historie nur deskriptiv zu führen (Zinssockel, Venue, Verbrauch in Stufe 2)?
4. **Überschussdefinition.** Ist «Kapital ausserhalb des Markts verzinst zu DTB3» als Primärannahme zulässig, oder muss S-Cash0 (unverzinst, realistischer auf Kraken) primär sein? Beide führen zu anderen Fragen (Strategie gegen T-Bill-Halter bzw. gegen Kraken-Konto).
5. **Schwelle.** Ist die Herleitung H = (1 + m)·DTB3 plus Δ = 5 Pp. (Amortisation über 75 Tage) sauber, oder steckt mit der Wahl von 75 Tagen und 30-Tage-Fenster doch ein Freiheitsgrad, der deklariert werden muss? Soll X2 (F7 < 0) als Stufe-2-Erbe bleiben?
6. **Signifikanz.** Stationärer Block-Bootstrap mit 30 Tagen Blocklänge auf einer Reihe, die über lange Strecken exakt 0 ist (ausserhalb des Markts): Ist das gültig, oder sollte die Statistik nur auf Markttagen bzw. je Episode rechnen? Ist Holm über zwei Coins die richtige Familie, angesichts der hohen Korrelation von BTC- und ETH-Funding?
7. **Mindestgrösse P2 (+1.0 Pp.).** Zu hoch, zu tief, oder sollte sie Teil der Nullhypothese sein (H0: Überschuss ≤ 1 Pp.)?
8. **Kostenmodell.** Ist maker_plan für Spot und Futures bei einem täglichen Ein-/Ausstieg zum 1h-Schluss realistisch (Füllwahrscheinlichkeit, adverse Selektion)? Sind kostenlose, sofortige Übertragungen Spot ↔ Futures zulässig, obwohl verschiedene Gesellschaften beteiligt sein können?
9. **Margin und Liquidation.** Sind m = 0.5, Bänder 0.25/1.0, MM = 1 % und 1 % Liquidationszuschlag angemessen? Reicht die stündliche Prüfung auf dem Mark-Hoch, oder braucht es eine Minutenprüfung? Fehlt ein Modell für Auto-Deleveraging?
10. **Collateral-Variante.** Kraken Futures ist Multi-Collateral: BTC/ETH selbst als Margin im Futures-Konto wäre nahezu liquidationsfrei und bräuchte weniger Kapital, konzentriert aber alles bei einer Gegenpartei. Soll das als vorregistrierte Vergleichsregel aufgenommen werden (Haircuts nötig), oder bewusst nicht?
11. **Kriterium P7.** Ist «K-ist ≥ −1 Pp.» sinnvoll, obwohl bei Regel S in diesem Fenster vermutlich kaum Marktzeit liegt (P7 wäre dann trivial erfüllt)? Alternative: K-ist als eigene Zelle mit Exposition-Untergrenze.
12. **Währung.** Damian denkt in CHF. Soll zusätzlich ein Überschuss gegen den CHF-Geldmarkt (mit USD/CHF-Absicherungskosten) berichtet werden, und welcher Satz?
13. **Vorbelastung und DSR.** Ist N = 262 für die DSR richtig gezählt, und muss die Kenntnis der Kraken-Niveaus 2025/26 (§0.1) als Trial zählen?
14. **Forward-Test.** Reichen 12 Monate mit Quartalsblöcken, und soll α für den Forward-Test gleich bleiben? Wie wird das Forward-Urteil bewertet, wenn Regel S forward fast nie investiert ist?
15. **ENTSCHEIDE-Konflikt.** Der Eintrag 2026-09-15 «Funding ist Kostenposition, nicht Ertragsbaustein» und F1 («D-CC nur Forward-Datensammlung, kein Sleeve») stehen gegen diese Vorregistrierung. Reicht die Freigabe Damians beim Freeze, oder braucht es vorher einen eigenen ENTSCHEIDE-Eintrag, der D-CC formell wieder aufnimmt?
16. **Holdout-Nähe.** Die Flow-Validation-Dateien im Holdout enthalten vermutlich Binance-Funding ab 2024 für BTC/ETH. Ist die Binance-Referenz aus `data/raw/binance_funding/` damit governance-konform, oder sollte sie entfallen?

## 14. Offene Punkte für Damian (Entscheidvorlage, ca. 15 Minuten, nach dem Review)

1. Freigabe des Designs mit der Korrektur §0.1 (Lauf R nur Ausschlusstest, konfirmatorisch nur forward).
2. Formelle Wiederaufnahme von D-CC als Kraken-Carry (Frage 15).
3. Bestätigung: Paper und Micro-Live nur nach §10, D2 und D4 vor jedem Live-Franken.
