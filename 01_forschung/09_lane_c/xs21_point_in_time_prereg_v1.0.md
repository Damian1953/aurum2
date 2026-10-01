# XS21 Cross-Sectional Momentum: Point-in-Time-Vorregistrierung, Version 1.0

**Project Aurum II, `01_forschung/09_lane_c/xs21_point_in_time_prereg_v1.0.md`, 01.10.2026.**

**Status: FREEZE-KANDIDAT, nicht eingefroren – wartet auf Freigabe Damian.** Es gibt keinen Lauf, es wurden keine Outcomes berechnet, und es sind noch keine Kurs-, Volumen- oder Funding-Daten für XS21 beschafft. Eingefroren ist dieses Dokument erst, wenn Damian es freigibt und seine SHA-256 in ENTSCHEIDE eingetragen ist. Bis dahin gilt es als Entwurf.

Grundlage:
- v0.2 (`xs21_point_in_time_prereg_v0.2.md`, SHA 9907c0e198fa29ec…) und v0.1 (SHA 00a98886c8414f00…). Beide bleiben unverändert.
- Review Claude zu v0.2 (`xs21_point_in_time_v0.2_review_claude_v1.md`, SHA 3919ac12f49a5be6…) mit den Pflichtänderungen M1 bis M7 und den Zusatzpunkten der Checkliste §5 des Reviews.
- Vorgaben Damian vom 01.10.2026: PAXG und XAUT ausschliessen. BTCDOM, DEFI, FOOTBALL und BLUEBIRD ausschliessen. USTC, FRAX, STABLE und STBL zulassen, wenn das Binance-Listing nach der Entkopplung bzw. Umbenennung liegt. Die Regel so fassen, dass diese Fälle aus ihr folgen.
- ENTSCHEIDE vom 01.10.2026, Punkte B1 bis B8, C1, C3 und F1.

Übernommen aus der Stufe-2-Vorregistrierung v1 sind die XS21-Regeln (Signal, Ranking, Haltedauer, Gewichtung, Kosten, Kriterien). Abweichungen sind in §0 vollständig aufgeführt. Wichtigste methodische Abweichung ist die Signalquelle (M7).

## 0. Änderungen

### 0.1 Gegenüber v0.1 (aus v0.2, unverändert)

| Punkt | v0.1 | v0.2 und v1.0 |
|---|---|---|
| B1 | Schwelle 50 Mio. USD, begründet mit Ausführbarkeit auf Kraken | Die Schwelle definiert das Forschungsuniversum U1, Begründung «Mindestliquidität auf der Signalbörse». Die Ausführbarkeit regelt U2 (B8) |
| B2 | Dezil-Variante offen | vorregistrierter Vergleich, keine Auswahl. Top-3 bleibt primär |
| B3 | Delisting-Glattstellung offen | letzte Tageskerze, K2-Slippage |
| B4 | Short-Bein offen | Long+Short primär, Long-only als vorregistrierter Vergleich |
| B5 | «Discovery bis 2023, Holdout ab 2024» | ein Lauf 2020-02 bis 2026-09-14, Etikette «Discovery/Robustheit mit Vorbelastung», kein «Holdout validation» |
| B6 | – | Ausführbarkeits-Gate vor jedem Paper-Betrieb |
| B7 | nur Nicht-ASCII-Symbole ausgeschlossen | eingefrorene Ausschlussliste nach Regel |
| B8 | – | zweites Universum U2 (Top 20 nach Quote-Volumen des Vormonats), Holm über U1 und U2, nur U2 ist Sleeve-Kandidat |

### 0.2 Gegenüber v0.2 (Review Claude v1 und Vorgaben Damian)

| Nr. | Abschnitt | v0.2 | v1.0 |
|---|---|---|---|
| M1 | §2.4 | «Basiswert ist ein Krypto-Asset, Stablecoin-Paare ausgeschlossen» | Regelwortlaut: einzelnes Krypto-Asset ohne Bindung an Fiat, Rohstoff, Wertpapier oder Index. Daraus folgen die Ausschlüsse von PAXG, XAUT, BTCDOM, DEFI, FOOTBALL und BLUEBIRD |
| M2 | §2.4 | 59 Symbole «unklar», nicht ausgeschlossen | Prüfung jedes Eintrags gegen die Binance-Ankündigung, Auffangregel (Spot-Paar oder On-Chain-Token führt zur Zulassung, sonst Ausschluss), Quelle und Prüfdatum je Eintrag, Sensitivitätslauf deskriptiv. Keine Symbole bleiben unklar |
| M3 | §5.4 | Gate-Schwellen offen | Schwellen eingefroren: Kraken-Futures-Listing, Median 24h-Volumen über 30 Tage ≥ 2 Mio. USD, ≥ 90 Prozent der Positionen in den ersten 8 Rebalancings, Cash statt Ausweichen, Position ≤ 0.1 Prozent des 24h-Volumens |
| M4 | §7 | fehlendes Funding wird nicht gefüllt (Regel offen) | adverses Median-Funding (Median des absoluten Fundings, immer zulasten der Position), Bericht je Bein, Vorbehalt über 5 Prozent |
| M5 | §5.2 | Blöcke offen | B1 2020-02-01 bis 2021-12-31, B2 2022-01-01 bis 2023-12-31, B3 2024-01-01 bis 2026-09-14. Bestehen verlangt B1 **und** B2 positiv. **Abweichung von Stufe 2:** dort genügen 2 von 3 Blöcken, hier zählt B3 nicht als Stimme. Strenger als Stufe 2 |
| M6 | §2.2, §3 | keine Mindestgrösse | Stichtag zählt nur mit U1 ≥ 20 Symbolen. Laufbeginn ist der erste solche Stichtag, vorab nur aus Listing und Volumen bestimmt, gemeinsam für U1 und U2 |
| M7 | §0, §4 | «Regeln wörtlich aus Stufe 2» bei Perp-Tageskerzen | **Abweichung von Stufe 2:** Stufe 2 berechnete ret(21) auf Binance-**Spot**-Tageskerzen. XS21 PiT verwendet Binance-USDT-M-**Perp**-Tageskerzen, weil viele Symbole des PiT-Universums kein Spot-Paar haben (Begründung §4). «Wörtlich» gilt nur noch für die Regellogik |
| – | §4 | Dezil auch in U2 | Dezil in U2 gestrichen, «identisch mit Jitter Top-2». In U1 bleibt das Dezil |
| – | §2.3 | Tie-Break alphabetisch (Entwurf) | bestätigt |
| – | §6 | – | Vermerk «Netto-Ergebnisse von U1 sind nicht als handelbare Renditen zu lesen» |
| – | §7 | – | Prüfbedingung U2 ⊆ U1 im Code. DTB3 bis 2026-09-14 mit SHA abgelegt |
| – | §5.3 | Survivorship-Zerlegung per 2026-09-14 | zusätzlich per 2023-12-31 |
| – | §2.4 | «Vor 2026 betrifft die Liste nur PAXGUSDT, USDCUSDT und XAUUSDT (first_month 2025-12)» | **Korrektur einer Tatsachenangabe** (auch im Review §0 übernommen): USDC ab 2023-03, PAXG ab 2025-03, XAU ab 2025-12, XAUT ab 2026-03. Mit M1 kommen DEFI (ab 2020-08), BTCDOM (2021-06), FOOTBALL (2022-09) und BLUEBIRD (2022-11) hinzu. Der Teil 2020-02 bis 2023-12 ist damit von fünf Ausschlüssen berührt (§2.4) |

Die Kosten-Lesart zu REBOUND-MICRO und das JSON-Kostenmodell (`config/cost_model_v1.json`) sind im Review akzeptiert (§6).

## 1. Hypothese

H-C2 (Stufe 2) gilt auf einem Point-in-Time-Universum, wenn der Cross-Sectional-Momentum-Effekt nicht von der Auswahl der Überlebenden getragen wurde. Zwei Fragen werden getrennt beantwortet:
- **Forschungsfrage (U1):** Existiert der Effekt ohne Survivorship?
- **Handelbarkeitsfrage (U2):** Existiert er auch in einem liquiden, ausführbaren Universum?

Falsifikation: Auf U1 verschwindet das Alpha oder wird von den delisteten Symbolen dominiert.

## 2. Universen, point-in-time

### 2.1 Basismenge

- **Quelle:** Binance USDT-M Perpetuals aus dem Monatsarchiv `data/futures/um/monthly/klines/` von `data.binance.vision`.
- **Liste:** aus dem Lane-C-Loader v1.1 (`binance_um_universe.csv`, SHA f5563c09…), ergänzt um den Collector-Snapshot vom 01.10.2026 (`xs21_pit_v0.2/binance_um_snapshot_2026-10-01.csv`, SHA bff906a0…).
- **Stichtage T:** jeder siebte Tag ab 2020-02-01, 00:00 UTC, wie Stufe 2. Das Raster ist fest, der Laufbeginn folgt aus M6 (§3).
- **Mitgliedschaft am Stichtag T.** Ein Symbol gehört zur Basismenge, wenn alle diese Bedingungen erfüllt sind:
  - `first_month` ≤ Monat(T) ≤ `last_month`.
  - Der Vormonat hat vollständige Tages-Klines.
  - Quote ist USDT, es ist ein Perpetual (keine Terminkontrakte `_YYMMDD`, keine `SETTLED`-Artefakte).
  - Der Name besteht nur aus ASCII-Zeichen.
  - Das Symbol steht nicht auf der B7-Ausschlussliste v1.0 (§2.4).

### 2.2 U1: breites Forschungsuniversum (B1, M6)

U1 umfasst alle Symbole der Basismenge mit einem Dollar-Umsatz (`quote_volume`, Summe der Tages-Klines) im Vormonat von mindestens 50 Millionen USD.

Begründung: Mindestliquidität auf der Signalbörse. Die Schwelle ist vor dem Lauf festgelegt und wird nicht variiert. Sie ist ausdrücklich **kein** Kriterium für Ausführbarkeit.

**Mindestgrösse (M6):** Ein Stichtag zählt nur, wenn U1 mindestens 20 Symbole hat, also mindestens so viele wie U2. Fällt U1 nach dem Laufbeginn an einem Stichtag unter 20, halten U1 und U2 an diesem Stichtag Cash (T-Bill). Die Anzahl solcher Stichtage wird berichtet.

### 2.3 U2: ausführbares Liquiditätsuniversum (B8)

U2 umfasst die 20 Symbole der Basismenge (also nach B7 gefiltert) mit dem höchsten Binance-`quote_volume` des Vormonats am Stichtag T.
- Die Rangbildung ist point-in-time und daher frei von Survivorship.
- Bei Gleichstand entscheidet die alphabetische Reihenfolge des Symbols (bestätigt).
- Hat die Basismenge weniger als 20 Symbole, besteht U2 aus allen.
- Prüfbedingung U2 ⊆ U1 siehe §7.

### 2.4 Ausschlussliste B7 v1.0 (M1, M2)

**Regel (M1):** «Zugelassen sind nur Perpetuals auf ein einzelnes Krypto-Asset, dessen ökonomisches Exposure nicht an einen Fiat-Wert, einen Rohstoff, ein Wertpapier oder einen Index gebunden ist. Ausgeschlossen sind Stablecoins, tokenisierte Rohstoffe und Wertpapiere sowie Index- und Korb-Perps.»

Daraus folgen:
- PAXG und XAUT: ausgeschlossen (tokenisierter Rohstoff, Exposure Gold).
- BTCDOM, DEFI, FOOTBALL, BLUEBIRD: ausgeschlossen (Index- bzw. Korb-Perps).
- USTC: zugelassen. Binance-UM-Listing 2023-11 (`first_month`), also nach der Entkopplung im Mai 2022. Während der gesamten Handelszeit kein gebundener Stablecoin. Die Prüfung ist im Builder als Bedingung kodiert.
- FRAX: zugelassen. Der Perp startet am 15.01.2026, am Tag des Tauschs FXS→FRAX. Underlying laut Ankündigung ist der Frax-Token (ehemals FXS), nicht der Stablecoin. Es gibt keine frühere FRAXUSDT-Notierung im Archiv.
- STBL: zugelassen. Perp ab 17.09.2025, Underlying ist der STBL-Plattform-Token, nicht ein Stablecoin.
- STABLE: zugelassen. Pre-Market-Perp ab 06.11.2025, Underlying ist der Layer-1-Token der Stable-Chain.
- USDC: ausgeschlossen (Stablecoin).

**Vorgehen (M2):**
1. Jedes Symbol, dessen Basiswert aus dem Namen nicht eindeutig ist, wird gegen die Binance-Listing-Ankündigung geprüft (Underlying bzw. Einordnung als TradFi-, Equity-, Pre-IPO- oder Standard-Krypto-Perpetual).
2. **Auffangregel:** Bleibt ein Symbol danach unklar, entscheidet eine feste Rangfolge. Ein Binance-Spot-Paar oder ein identifizierbarer On-Chain-Token führt zur Zulassung (Sicherheit «auffang»), fehlt beides, wird es ausgeschlossen.
3. Jeder Eintrag trägt Quelle und Prüfdatum (01.10.2026).
4. **Sensitivität:** Zusätzlich wird ein Lauf ohne alle *zugelassenen* Symbole mit Sicherheit «wahrscheinlich» oder «auffang» berichtet (11 Symbole, `xs21_sensitivitaet_ohne_v1.0.csv`). Er ist deskriptiv und kein Primärtest.
5. Grundlage sind nur Symbolnamen, Listing-Monate, Binance-Ankündigungen und das Binance-Spot-Listing. Kurse, Renditen und Volumen wurden nicht betrachtet.

**Dateien:**

| Datei | Inhalt |
|---|---|
| `xs21_pit_v1.0/xs21_b7_klassifikation_v1.0.csv` | alle 265 geprüften Sonderfälle mit Entscheid, Typ, Sicherheit, Grund, Quelle, Prüfdatum, `first_month`, Spot-Paar, Sensitivitätskennzeichen |
| `xs21_pit_v1.0/xs21_exclusions_v1.0.csv` | die 220 Ausschlüsse (massgeblich für §2.1) |
| `xs21_pit_v1.0/xs21_sensitivitaet_ohne_v1.0.csv` | die 11 Symbole für den Sensitivitätslauf |
| `xs21_pit_v1.0/xs21_b7_v1.0.sha256` | Prüfsummen der Listen, der Klassifikation (`tools/xs21/exclusion_map_v1.0.py`), des Builders (`tools/xs21/build_exclusions_v1.py`) und der Eingaben |

Alle übrigen der 895 USDT-Perpetuals (ASCII, ohne Termin- und SETTLED-Artefakte) sind nach Namen und Listing-Kontext Einzel-Krypto-Assets und bleiben nach der Regel zugelassen.

**Ergebnis:**
- 220 Ausschlüsse: 156 Aktien, 40 ETFs, 8 Rohstoffe, 8 Pre-IPO, 4 Index/Korb, 2 tokenisierte Rohstoffe, 1 Devisenkurs, 1 Stablecoin. Davon 180 «sicher» (Ankündigung geprüft oder eindeutiger Ticker) und 40 «wahrscheinlich» (Aktien- oder ETF-Ticker, Ankündigung nicht einzeln abgerufen. Diese Symbole sind ausgeschlossen, die Regel liefert für sie denselben Entscheid wie die Kategorie).
- 45 geprüfte Zulassungen: 34 «sicher», 2 «wahrscheinlich» (O, PONS), 9 «auffang» (CHIP, GENIUS, GRAM, KAT, MARSCOIN, OPG, OPN, RE, ROBO).
- Keine Symbole bleiben unklar. Alle 59 der v0.1-Liste «unklar» sind entschieden: 41 zugelassen, 18 ausgeschlossen (TradFi-, Equity-, ETF- oder Pre-IPO-Perps laut Ankündigung).
- **Zeitliche Wirkung (Korrektur gegenüber v0.2 und Review):** Mit `first_month` bis 2023-12 sind fünf Symbole ausgeschlossen, DEFI (2020-08), BTCDOM (2021-06), FOOTBALL (2022-09), BLUEBIRD (2022-11) und USDC (2023-03). 2024 bis 2025 kommen PAXG (2025-03) und XAU (2025-12) dazu, alle übrigen ab 2026. Der Kernzeitraum ist damit nicht unberührt, aber nur durch strukturell begründete Ausschlüsse, nicht durch Ergebnisse.

### 2.5 Delisting (B3)

Wird ein Symbol während eines Haltezeitraums delistet, wird es zur letzten verfügbaren Tageskerze zum Schluss glattgestellt, mit K2-Slippage.

## 3. Zeitraum und Evidenzklasse (B5, M6)

**Ein einziger Lauf bis 2026-09-14.** Das Stichtag-Raster beginnt 2020-02-01, dem ersten Stichtag mit vollständigem Vormonat im Archiv, das 2020-01 beginnt.

**Laufbeginn (M6):** Der erste Stichtag des Rasters, an dem U1 mindestens 20 Symbole hat. Er wird nach der Datenbeschaffung und vor dem Lauf nur aus Listing und `quote_volume` bestimmt, ohne Renditen und ohne Funding, und gilt gemeinsam für U1 und U2. Ergebnis und SHA des Bestimmungsskripts werden vor dem Lauf in ENTSCHEIDE eingetragen. Liegt der Laufbeginn nach 2020-02-01, beginnt Block B1 am Laufbeginn.

- **Etikette:** «Discovery/Robustheit mit Vorbelastung».
- **Grund:** Stufe 2 hat 2024-01-01 bis 2026-09-14 als In-Sample-Block P3 verwendet. XS21 LS hat 276 Trades mit Einstieg ab 2024, und die zehn Stufe-2-Coins sind Teil des PiT-Universums. Für die XS21-Regel und für D-CC gilt der Zeitraum ab 2024 als verbraucht.
- **Ausweis:** Gesamtzeitraum und die drei Blöcke B1, B2, B3 (§5.2). Der Teil ab 2024 ist **keine** Validation.
- **Ausgeschlossen:** das Etikett «Holdout validation», ebenso jede Holdout-Logik nach Manifest für XS21 und D-CC.
- **Einzige saubere Out-of-Sample-Evidenz:** ein Forward-Fenster ab 15.09.2026 (E2).
- Die Stufe-2-Urteile bleiben unverändert.

## 4. Regeln, getrennt auf U1 und U2

Die Regellogik ist aus Stufe 2 übernommen. Abweichend ist die Signalquelle (M7, unten).

**Primär (B4):** Long+Short. An jedem Stichtag (alle sieben Tage) gilt:
- **Long-Bein:** Unter allen Symbolen des Universums mit `ret(21) > 0` werden die drei mit dem höchsten `ret(21)` gleichgewichtet long gehalten.
- **Short-Bein:** Unter denen mit `ret(21) < 0` werden die drei niedrigsten short gehalten.
- Beide Beine erhalten je halbes Kapital. Gibt es weniger als drei geeignete Symbole, bleibt der Rest in Cash.
- Kein Gate, kein Stopp, kein Filter.
- Ausführung zur Eröffnung des Folgetages.
- Kosten K0, K1, K2 wie Stufe 2 (`stage2_perp`, Perp-Modell mit Funding auf beiden Beinen), Cash zum T-Bill-Satz.

**Signalquelle (M7), Abweichung von Stufe 2:** `ret(21)` wird auf Binance-USDT-M-**Perpetual**-Tageskerzen (Schluss) berechnet. Stufe 2 verwendete Binance-**Spot**-Tageskerzen (Holdout- und Börsen-Prüfung v1, 2.1). Begründung: Viele Symbole des PiT-Universums haben kein Binance-Spot-Paar, insbesondere viele delistete. Spot-Kerzen würden das Universum auf Symbole mit Spot-Paar einschränken und damit eine neue Auswahlverzerrung einführen. Perp-Kerzen gelten für Signal, Ausführung, Delisting, die EW-Benchmark und die Volumenschwellen. Die Abweichung wird im Bericht aufgeführt.

**Vorregistrierte Vergleiche, keine Auswahl:**
- Long-only (B4).
- Nur in U1: oberstes und unterstes Dezil, je gleichgewichtet (B2). In U2 gestrichen, «identisch mit Jitter Top-2» (ein Dezil von 20 sind 2 Symbole).
- Jitter wie Stufe 2: L ∈ {42, 63}, Top-N ∈ {2, 4}.
- Sensitivität B7 ohne die 11 Symbole «wahrscheinlich»/«auffang» (§2.4), deskriptiv.

## 5. Kriterien und Mehrfachtest

### 5.1 Kriterien

Es gelten die acht Stufe-2-Kriterien für Familie C, je Universum unverändert, ausser Kriterium 3 (Zeitblöcke, §5.2). Das Alpha wird gegen das gleichgewichtete Universum gemessen, also U1 gegen EW-U1 und U2 gegen EW-U2.

**Holm (B8):** Primärtests sind U1 Top-3 L+S und U2 Top-3 L+S. Holm-Korrektur der einseitigen Block-Bootstrap-p-Werte für Sharpe > 0 über diese zwei Tests, Niveau 5 Prozent (Verfahren wie Stufe 2 §19). Vergleiche, Jitter und Sensitivität sind keine Primärtests. U1 und U2 sind stark korreliert, Holm ist damit konservativ. Das bleibt so.

### 5.2 Zeitblöcke (M5)

- B1: 2020-02-01 (bzw. Laufbeginn nach M6) bis 2021-12-31
- B2: 2022-01-01 bis 2023-12-31
- B3: 2024-01-01 bis 2026-09-14

Massgeblich ist die Zuordnung nach Einstiegsdatum des Trades. Das Kriterium (in der Stufe-2-Tabelle Nr. 3, in v0.2 und im Review als «Kriterium 4» bezeichnet) lautet in v1.0: **Erwartung je Trade nach Kosten (K1) > 0 in B1 und in B2.** B3 wird berichtet, darf aber nicht die fehlende Stimme liefern. 2026 ist kein eigener Block. **Abweichung:** Stufe 2 verlangt ≥ 2 von 3 Blöcken. Die v1.0-Regel ist strenger, damit der vorbelastete Zeitraum ab 2024 (§3) nicht über das Urteil mitentscheidet.

### 5.3 Survivorship-Zerlegung

Der Ertrag wird zerlegt in die Beiträge der Symbole, die am Stichtag der Zerlegung noch TRADING waren, und der bis dahin delisteten.
- Stand 2026-09-14: für den Gesamtzeitraum und für jeden Block.
- Zusätzlich Stand 2023-12-31: für den Teil bis 2023-12-31, damit der Vergleich mit dem Lane-C-Befund (81 Symbole bis Ende 2023 delistet) möglich ist.

Besteht XS21 nur mit den Überlebenden, ist H-C2 falsifiziert.

**Interpretation:**

| U1 | U2 | Lesart |
|---|---|---|
| besteht | besteht | Effekt real und liquide. U2 ist Sleeve-Kandidat |
| besteht | besteht nicht | Effekt real, aber für ein Privatkonto nicht handelbar. Kein Sleeve |
| besteht nicht | besteht | kein Survivorship-freier Effekt. Kein Sleeve, Bericht |
| besteht nicht | besteht nicht | H-C2 auf PiT falsifiziert |

**Status:** nach Regel v2 (Governance v1.1). Die Evidenzklasse ist höchstens «Discovery/Robustheit mit Vorbelastung» (§3). Eine Promotion zu Validation ist nur über das Forward-Fenster möglich, nicht über diesen Lauf.

### 5.4 Ausführbarkeits-Gate (B6, M3), eingefroren

Gilt vor jedem Paper-Betrieb eines U2-Sleeves. Börse nach C3: Kraken Futures, vorbehaltlich D4.
- **Messgrundlage:** Forward-Daten des Collectors ab 15.09.2026, Kraken Futures. Keine Rückrechnung, weil die meisten PF-Perps erst seit 22.03.2022 existieren und keine historischen Volumen vorliegen.
- **Je gewählte Position** gilt sie als handelbar, wenn beide Bedingungen erfüllt sind: Das Symbol ist auf Kraken Futures als Perpetual handelbar, und der Median des 24h-Volumens (USD) der letzten 30 Tage beträgt mindestens 2 Mio. USD.
- **Gate bestanden:** In den ersten 8 Rebalancings des Forward-Fensters sind mindestens 90 Prozent der von U2 gewählten Positionen handelbar.
- **Nicht handelbares Symbol im Betrieb:** Die Position bleibt in Cash. Es wird nicht auf den nächsten Rang ausgewichen.
- **Positionsgrösse:** höchstens 0.1 Prozent des 24h-Volumens je Symbol.
- Eine zweite Börse kommt nur in Frage, falls U2 auf Kraken das Gate nicht besteht.
- **Datengrundlage:** Collector ab v1.1 (seit 01.10.2026): täglicher Snapshot der Kraken-Futures-Instrumente und -Ticker je Perpetual (`tradeable`, 24h-Volumen USD = `volumeQuote`, Open Interest, Last, Zeitstempel) in `data_live/kraken_futures_tickers/`. Für den 30-Tage-Median zählt je UTC-Tag der erste Snapshot. Zeitliche Grenze siehe §8.2.

## 6. Kosten

Primär `stage2_perp` K0/K1/K2 aus `config/cost_model_v1.json`, unverändert. Der K1-Perp-Satz von 0.05 Prozent entspricht dem Kraken-Futures-Taker (`venue_kraken`). Nach C1 ist XS21 ein Perp-Sleeve, weil es ein Short-Bein braucht.

**Netto-Ergebnisse von U1 sind nicht als handelbare Renditen zu lesen. Über die Handelbarkeit entscheidet nur U2.** Das einheitliche Perp-Kostenmodell unterschätzt die Kosten der dünnen Extremwert-Symbole, die U1 typischerweise wählt.

Lesart (Review §4.1, ohne Umetikettierung): K1 Spot 0.40 Prozent entspricht dem Kraken-Spot-Maker-Satz (Tier 1). Der REBOUND-MICRO-Entscheid «keine Maker-Gutschrift» bleibt gültig. Stops sind Market-Orders und damit Taker. Das Szenario `maker_entry_taker_stop` ist ein Entwurf und wird auf keinen eingefrorenen Lauf angewendet. JSON statt `costs.yaml` ist akzeptiert.

## 7. Datenbeschaffung und Prüfungen vor dem Lauf (noch nicht ausgeführt)

Reihenfolge: Freigabe und Freeze v1.0 einschliesslich B7-Liste v1.0, danach Datenbeschaffung, danach Laufbeginn nach M6, danach ein einziger Lauf.

- **Daten:** Tages-Klines aller Symbole der Basismenge ab 2020-01, einschliesslich der delisteten, aus `data.binance.vision`. Dazu Funding-Historie je Symbol aus den Monats-ZIPs `fundingRate`, Provenienz mit Prüfsummen. `fapi.binance.com` ist von der Agent-Box geoblockt und wird nicht benötigt.
- **T-Bill:** `data/supplement/DTB3_3m_tbill_to_2026-09-14.csv`, FRED DTB3, geladen am 01.10.2026, ohne Leerwerte, bis 2026-09-14 abgeschnitten, SHA-256 `8b287e3cc711b4c7d5629caed6f531c7564d4d7e8dbcf8f6bc49b069b7ca9d59`. Bis 2026-07-15 ist sie bytegleich mit der Stufe-2-Ersatzdatei `DTB3_3m_tbill.csv` (085e8e38…). Diese endet 2026-07-15 und deckt den Lauf nicht ab.
- **Fehlendes Funding (M4):** Fehlt für eine gehaltene Position das Funding zu einem Settlement, wird es mit dem Median des **absoluten** Fundings aller Symbole des jeweiligen Universums (U1 bzw. U2) zum selben Settlement gefüllt, immer zulasten der Position, das heisst Long und Short zahlen. Weder null noch Ausschluss. Anzahl und Anteil der gefüllten Settlements werden je Bein und Universum berichtet. Liegt der Anteil über 5 Prozent der Positions-Settlements eines Beins, steht das als Vorbehalt im Bericht.
- **Prüfbedingungen im Code (Abbruch bei Verletzung):** U2 ⊆ U1 an jedem Stichtag (ein U2-Symbol unter 50 Mio. USD wäre ein Datenfehler). Kein Symbol der B7-Liste v1.0 in der Basismenge. SHA der eingefrorenen Spezifikation v1.0 und der B7-Liste im Lauf-Log (E3).
- Moratorium F1: kein neuer Strang.

## 8. Offen vor Freeze bzw. vor Lauf

1. **Freigabe Damian** dieses Dokuments und der B7-Liste v1.0. Danach SHA-Eintrag in ENTSCHEIDE.
2. **Datengrundlage Gate (M3):** Die Erfassung der Kraken-Futures-Instrumente und -Ticker (Collector v1.1) hat am **01.10.2026** begonnen (erster Snapshot 10:58 UTC, 284 Perpetuals, alle `tradeable`). Der erste 30-Tage-Median ist mit dem 30. Tages-Snapshot am **30.10.2026** verfügbar. Zwischen 15.09. und 30.09.2026 gibt es keine Volumendaten, und sie lassen sich nicht nachholen. Die Raster-Stichtage 19.09. bis 24.10.2026 sind deshalb nicht nach M3 messbar. Zu entscheiden (Vorschlag): Als «erste 8 Rebalancings» gelten die ersten 8 Raster-Stichtage mit vollständigem 30-Tage-Median, also 31.10. bis 19.12.2026. Das Gate wäre dann frühestens am **19.12.2026** entscheidbar.
3. **Regelergänzungen in v1.0, die über den Wortlaut des Review hinausgehen** (zu bestätigen):
   - M4: Fehlt zu einem Settlement für alle Universumssymbole das Funding, gilt der Median des absoluten Fundings des Universums über die vorangehenden 30 Tage.
   - M5: Zuordnung der Trades zu Blöcken nach Einstiegsdatum; Block B1 beginnt am Laufbeginn nach M6.
   - M6: Unter 20 Symbolen in U1 halten U1 und U2 gemeinsam Cash.
4. **B7 «wahrscheinlich» unter den Ausschlüssen (40):** nicht einzeln gegen die Ankündigung geprüft. Alle sind Aktien-, ETF-, Rohstoff- oder Pre-IPO-Ticker, ab 2026 gelistet. Eine Fehlklassifikation würde nur Krypto-Symbole ab 2026 fälschlich entfernen.
