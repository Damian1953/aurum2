# XS21 Cross-Sectional Momentum: Point-in-Time-Vorregistrierung, Version 0.2 (ENTWURF)

**Project Aurum II, `01_forschung/09_lane_c/xs21_point_in_time_prereg_v0.2.md`, 01.10.2026.**

**Status: ENTWURF zur Prüfung durch Claude und Damian. NICHT eingefroren, es gibt keinen Lauf und es wurden keine Outcomes berechnet.** Ein Freeze entsteht erst als v1.0 mit SHA-Eintrag in ENTSCHEIDE.

Grundlage:
- v0.1 (`xs21_point_in_time_prereg_v0.1.md`, SHA 00a98886c8414f00…), bleibt unverändert.
- ENTSCHEIDE vom 01.10.2026, Punkte B1 bis B8, C1, C3 und F1 (Entwurf Schritt 0 v0.2, von Damian übernommen).

Die XS21-Regeln aus der Stufe-2-Vorregistrierung v1 werden wörtlich übernommen. Geändert haben sich nur Universum, Zeitraum und Evidenzklasse, die Mehrfachtest-Korrektur und die Ausführbarkeit.

## 0. Änderungen gegenüber v0.1

| Punkt | v0.1 | v0.2 |
|---|---|---|
| B1 | Schwelle 50 Mio. USD, begründet mit Ausführbarkeit auf Kraken | Schwelle definiert das Forschungsuniversum U1. Begründung neu: «Mindestliquidität auf der Signalbörse». Die Ausführbarkeit regelt U2 (B8) |
| B2 | Dezil-Variante offen | vorregistrierter Vergleich, keine Auswahl. Top-3 bleibt primär |
| B3 | Delisting-Glattstellung offen | bestätigt: letzte Tageskerze, K2-Slippage |
| B4 | Short-Bein offen | Long+Short primär, Long-only als vorregistrierter Vergleich |
| B5 | «Discovery bis 2023, Holdout ab 2024», «Holdout validation möglich» | ein Lauf von 2020-02 bis 2026-09-14 mit der Etikette «Discovery/Robustheit mit Vorbelastung». Der Teil ab 2024 wird separat ausgewiesen. Das Etikett «Holdout validation» ist ausgeschlossen |
| B6 | – | Ausführbarkeits-Gate auf der gewählten Börse vor jedem Paper-Betrieb |
| B7 | nur Nicht-ASCII-Symbole ausgeschlossen | eingefrorene Ausschlussliste: nur Basiswert Krypto, Stablecoin-Paare ausgeschlossen |
| B8 | – | zweites Universum U2 (Top 20 nach Binance-Quote-Volumen des Vormonats), Holm über U1 und U2, nur U2 ist Sleeve-Kandidat |

## 1. Hypothese

H-C2 (Stufe 2) gilt auf einem Point-in-Time-Universum, wenn der Cross-Sectional-Momentum-Effekt nicht von der Auswahl der Überlebenden getragen wurde. Zwei Fragen werden getrennt beantwortet:
- **Forschungsfrage (U1):** Existiert der Effekt ohne Survivorship?
- **Handelbarkeitsfrage (U2):** Existiert er auch in einem liquiden, ausführbaren Universum?

Falsifikation: Auf U1 verschwindet das Alpha oder wird von den delisteten Symbolen dominiert.

## 2. Universen, point-in-time

### 2.1 Basismenge

- **Quelle:** Binance USDT-M Perpetuals aus dem Monatsarchiv `data/futures/um/monthly/klines/`.
- **Liste:** aus dem Lane-C-Loader v1.1 (`binance_um_universe.csv`, SHA f5563c09…), ergänzt um den Collector-Snapshot vom 01.10.2026.
- **Mitgliedschaft am Stichtag T** (jeder siebte Handelstag, 00:00 UTC, wie Stufe 2). Ein Symbol gehört zur Basismenge, wenn alle diese Bedingungen erfüllt sind:
  - `first_month` ≤ Monat(T) ≤ `last_month`.
  - Der Vormonat hat vollständige Tages-Klines.
  - Quote ist USDT, es ist ein Perpetual (keine Terminkontrakte `_YYMMDD`, keine `SETTLED`-Artefakte).
  - Der Name besteht nur aus ASCII-Zeichen.
  - Das Symbol steht nicht auf der B7-Ausschlussliste (§2.4).

### 2.2 U1: breites Forschungsuniversum (B1)

U1 umfasst alle Symbole der Basismenge mit einem Dollar-Umsatz (`quote_volume`, Summe der Tages-Klines) im Vormonat von mindestens 50 Millionen USD.

Begründung: Mindestliquidität auf der Signalbörse. Die Schwelle ist vor dem Lauf festgelegt und wird nicht variiert. Sie ist ausdrücklich **kein** Kriterium für Ausführbarkeit.

### 2.3 U2: ausführbares Liquiditätsuniversum (B8)

U2 umfasst die 20 Symbole der Basismenge (also nach B7 gefiltert) mit dem höchsten Binance-`quote_volume` des Vormonats am Stichtag T.
- Die Rangbildung ist point-in-time und daher frei von Survivorship.
- Bei Gleichstand entscheidet die alphabetische Reihenfolge des Symbols (ENTWURF, siehe §8).
- Hat die Basismenge weniger als 20 Symbole, besteht U2 aus allen.

### 2.4 Ausschlussliste B7 (ENTWURF v0.1)

**Regel:** Zugelassen sind nur Symbole, deren Basiswert ein Krypto-Asset ist. Stablecoin-Paare werden ausgeschlossen.

**Umsetzung:** eine eingefrorene Liste, erstellt nach Basiswert und nicht nach Ergebnis. Für die Liste wurden keine Kurse, Renditen oder Volumen betrachtet, nur Symbolnamen, Listing-Monate und als Gegenprobe das Binance-Spot-Listing.

| Datei | Inhalt |
|---|---|
| `xs21_pit_v0.2/xs21_exclusions_v0.1.csv` | 198 Ausschlüsse mit Kategorie, Grund und Sicherheit |
| `xs21_pit_v0.2/xs21_unklar_v0.1.csv` | 59 Symbole mit unklarem Basiswert, vorläufig **nicht** ausgeschlossen |
| `xs21_pit_v0.2/xs21_exclusions_v0.1.sha256` | Prüfsummen von Listen, Klassifikation (`tools/xs21/exclusion_map_v0.1.py`) und Eingaben |
| `tools/xs21/build_exclusions.py` | Erzeugung der Listen |

Kategorien der 198 Ausschlüsse:
- 143 Aktien
- 35 ETFs
- 8 Rohstoffe
- 8 nicht kotierte Unternehmen (Pre-IPO)
- 2 tokenisiertes Gold (PAXG, XAUT, zur Entscheidung)
- 1 Devisenkurs (USDBRL)
- 1 Stablecoin (USDC)

Davon sind 141 sicher, 55 wahrscheinlich und 2 zur Entscheidung. Fast alle Ausschlüsse sind ab 2026 gelistet (TradFi-Perps ab 05.01.2026). Vor 2026 betrifft die Liste nur PAXGUSDT, USDCUSDT und XAUUSDT (`first_month` 2025-12).

Bewusst **nicht** ausgeschlossen, weil der Basiswert Krypto ist, jeweils mit Vermerk in `tools/xs21/exclusion_map_v0.1.py`:
- die Krypto-Indizes BTCDOM, DEFI, FOOTBALL und BLUEBIRD,
- USTC (entkoppelter ehemaliger Stablecoin),
- FRAX, STABLE und STBL (Governance-/Chain-Token).

Vor dem Freeze muss jeder Eintrag mit «wahrscheinlich», «zur_entscheidung» oder «unklar» gegen die Binance-Listing-Ankündigung (Feld «Underlying») geprüft werden.

### 2.5 Delisting (B3)

Wird ein Symbol während eines Haltezeitraums delistet, wird es zur letzten verfügbaren Tageskerze zum Schluss glattgestellt, mit K2-Slippage.

## 3. Zeitraum und Evidenzklasse (B5)

**Ein einziger Lauf von 2020-02-01 bis 2026-09-14.** Der erste Stichtag ist 2020-02-01, der erste mit vollständigem Vormonat im Archiv, das 2020-01 beginnt.

- **Etikette:** «Discovery/Robustheit mit Vorbelastung».
- **Grund:** Stufe 2 hat 2024-01-01 bis 2026-09-14 als In-Sample-Block P3 verwendet (Kriterium c3). XS21 LS hat 276 Trades mit Einstieg ab 2024, und die zehn Stufe-2-Coins sind Teil des PiT-Universums. Für die XS21-Regel und für D-CC gilt der Zeitraum ab 2024 als verbraucht.
- **Ausweis:** Berichtet werden der Gesamtzeitraum und getrennt die Teile 2020-02 bis 2023-12 und 2024-01 bis 2026-09-14. Der Teil ab 2024 ist **keine** Validation.
- **Ausgeschlossen:** das Etikett «Holdout validation», ebenso jede Holdout-Logik nach Manifest für XS21 und D-CC.
- **Einzige saubere Out-of-Sample-Evidenz:** ein Forward-Fenster ab 15.09.2026, beginnend mit dem Collector (E2).
- Die Stufe-2-Urteile bleiben unverändert.

## 4. Regeln, wörtlich aus Stufe 2, getrennt auf U1 und U2

**Primär (B4):** Long+Short. Alle sieben Handelstage gilt:
- **Long-Bein:** Unter allen Symbolen des Universums mit `ret(21) > 0` werden die drei mit dem höchsten `ret(21)` gleichgewichtet long gehalten.
- **Short-Bein:** Unter denen mit `ret(21) < 0` werden die drei niedrigsten short gehalten.
- Beide Beine erhalten je halbes Kapital. Gibt es weniger als drei geeignete Symbole, bleibt der Rest in Cash.
- Kein Gate, kein Stopp, kein Filter.
- Signale auf Binance-Perp-Tageskerzen (Schluss), Ausführung zur Eröffnung des Folgetages.
- Kosten K0, K1, K2 wie Stufe 2 (`stage2_perp`, Perp-Modell mit Funding auf beiden Beinen), Cash zum T-Bill-Satz.

**Vorregistrierte Vergleiche, keine Auswahl:**
- Long-only (B4).
- Top-N als Anteil des Universums: oberstes und unterstes Dezil, je gleichgewichtet (B2). In U2 sind das je zwei Symbole.
- Jitter wie Stufe 2: L ∈ {42, 63}, Top-N ∈ {2, 4}.

## 5. Kriterien und Mehrfachtest

- Es gelten die acht Stufe-2-Kriterien für Familie C, je Universum unverändert. Das Alpha wird gegen das gleichgewichtete Universum gemessen, also U1 gegen EW-U1 und U2 gegen EW-U2.
- **Holm (B8):** Primärtests sind U1 Top-3 L+S und U2 Top-3 L+S. Holm-Korrektur der einseitigen Block-Bootstrap-p-Werte für Sharpe > 0 über diese zwei Tests, Niveau 5 Prozent (Verfahren wie Stufe 2 §19). Vergleiche und Jitter sind keine Primärtests.
- **Survivorship-Zerlegung** (die eigentliche Frage): Der Ertrag wird zerlegt in die Beiträge der Symbole, die am 2026-09-14 noch TRADING waren, und der bis dahin delisteten. Das geschieht für den Gesamtzeitraum und für beide Teilzeiträume. Besteht XS21 nur mit den Überlebenden, ist H-C2 falsifiziert.
- **Interpretation:**

| U1 | U2 | Lesart |
|---|---|---|
| besteht | besteht | Effekt real und liquide. U2 ist Sleeve-Kandidat |
| besteht | besteht nicht | Effekt real, aber für ein Privatkonto nicht handelbar. Kein Sleeve |
| besteht nicht | besteht | kein Survivorship-freier Effekt. Kein Sleeve, Bericht |
| besteht nicht | besteht nicht | H-C2 auf PiT falsifiziert |

- **Status:** nach Regel v2 (Governance v1.1). Die Evidenzklasse ist höchstens «Discovery/Robustheit mit Vorbelastung» (§3). Eine Promotion zu Validation ist nur über das Forward-Fenster möglich, nicht über diesen Lauf.
- **Ausführbarkeits-Gate (B6):** Vor jedem Paper-Betrieb eines U2-Sleeves wird auf der gewählten Börse geprüft, dass die tatsächlich gewählten Symbole handelbar und ausreichend liquide sind. Nach C3 ist die Arbeitsannahme Kraken Futures, vorbehaltlich D4. Die Schwellen des Gates sind noch **nicht** festgelegt (§8). Eine zweite Börse kommt nur in Frage, falls U2 auf Kraken das Gate nicht besteht.

## 6. Kosten

Primär `stage2_perp` K0/K1/K2 aus `config/cost_model_v1.json`, unverändert. Der K1-Perp-Satz von 0.05 Prozent entspricht dem Kraken-Futures-Taker (`venue_kraken`). Nach C1 ist XS21 ein Perp-Sleeve, weil es ein Short-Bein braucht.

## 7. Datenbeschaffung vor dem Lauf (noch nicht ausgeführt)

- **Daten:** Tages-Klines aller Symbole der Basismenge ab 2020-01, einschliesslich der delisteten, aus `data.binance.vision`. Dazu Funding-Historie je Symbol aus den Monats-ZIPs `fundingRate`, Provenienz mit Prüfsummen.
- **Machbarkeit:** `data.binance.vision` ist von der Agent-Box erreichbar. `fapi.binance.com` ist von dort geoblockt, wird aber nicht benötigt.
- **Abdeckung:** Für U2 und B7 sind die `quote_volume`-Spalten der Tages-Klines nötig. Für Kosten auf dem Short-Bein braucht es Funding für jedes gehaltene Symbol. Fehlendes Funding wird berichtet und nicht gefüllt (Regel offen, §8).
- Moratorium F1: kein anderer neuer Strang. Dieser Entwurf setzt nur bestehende Entscheide um.

## 8. Offen vor dem Freeze (zur Prüfung durch Claude/Damian)

1. **B7-Liste:** Die Einträge «wahrscheinlich» (55) und «unklar» (59) gegen die Binance-Ankündigungen prüfen. Bei den unklaren Symbolen gibt es für CHIP, GENIUS, GRAM, KAT, MARSCOIN, OPG, OPN, RE und ROBO ein Binance-Spot-Paar, das spricht für Krypto. Ausserdem entscheiden: PAXG, XAUT (tokenisiertes Gold), USTC und die Krypto-Indizes.
2. **Gleichstand in U2:** Tie-Break alphabetisch, bestätigen.
3. **Schwellen des Ausführbarkeits-Gates (B6):** z.B. Mindest-Tagesvolumen je Symbol auf Kraken Futures, Anteil handelbarer Symbole je Stichtag, Verhalten bei nicht handelbarem Symbol. Noch nicht festgelegt.
4. **Fehlendes Funding** einzelner Symbole: als null behandeln oder Symbol ausschliessen. Zu bestimmen ohne Blick auf Ergebnisse.
5. **Zeitblöcke für Kriterium 4** im verlängerten Zeitraum: die Stufe-2-Blöcke übernehmen oder 2026 als eigenen Block führen.
6. **Dezil-Vergleich in U2** mit zwei Symbolen: so lassen oder streichen.
7. **Mindestgrösse von U1 je Stichtag:** Muss U1 eine Mindestzahl von Symbolen haben, damit der Stichtag zählt? In v0.1 nicht geregelt.
