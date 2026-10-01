# Ideen-Scan v1: Neue Ansätze für ein profitorientiertes Krypto-Werkzeug

Stand 01.10.2026, 16:30 Zürich. Desk Research (Web, Literatur, eigene Daten).

**Status: Diskussionsgrundlage, keine Evidenz.**
- Alle eigenen Zahlen in diesem Dokument sind **EXPLORATIV und nicht vorregistriert**.
- Sie stammen aus `tools/ideen/explorativ_scan_v1.py`, Ergebnis `explorativ_scan_v1.json`.
- Verwendet wurden nur öffentliche Rohdaten (`data/raw`), schon beim Einlesen auf **t < 2024-01-01** geschnitten.
- Nicht geöffnet: Holdout, holdout_manifest, Kraken-Futures-Funding (liegt erst ab 2025-09 vor). Dadurch bleiben 2024–2026 für einen vorregistrierten Test frei.
- Keine Keys, kein Börsenkontakt, kein Trading.

Rahmen:
- Privatkonto Schweiz, Kraken, Kosten K1. Spot gemäss C1/C2: 0.40 % Maker (Tier 1) + 0.05 % Slippage je Seite, Roundtrip rund 0.90 %. Perps 0.02 % Maker bzw. 0.05 % Taker.
- D3: Damian höchstens 1 Std./Woche, Review höchstens 4 Monate nach Paper-Start.
- Ziel: Ansätze, die der Agent weitgehend selbständig erforschen und betreiben kann.

## Kurzfazit

| # | Ansatz | Go/No-Go | Ein Satz |
|---|---|---|---|
| 1 | Delta-neutraler Funding-/Basis-Carry (Spot long + Perp short, Kraken) | **GO für Vorregistrierung** | Einziger Ansatz mit strukturellem, gut belegtem Ertragsmechanismus und ohne Richtungswette. Die Rendite ist seit 2024 aber deutlich geschrumpft, und Kraken-Funding hat keinen Zinssockel. |
| 2 | Volatilitäts-Targeting mit Trendfilter (BTC/ETH, Spot) als Überlagerung | **GO für Vorregistrierung (als Overlay, nicht als neue Alpha)** | Senkt Volatilität und Drawdown recht verlässlich. Ein Mehrertrag ist nicht belegt und überschneidet sich mit Turtle 55/20. |
| 3 | Staking bzw. Geldmarkt als Basisrendite und Hürde | **GO als Benchmark** | Kein Edge, aber die ehrliche Messlatte, die jede Strategie schlagen muss. |
| 4 | Rebalancing-Prämie im diversifizierten Korb | No-Go als eigene Strategie | Kleiner Effekt, von Survivorship und Korbwahl dominiert. Nützlich höchstens als Konstruktionsregel. |
| 5 | Optionen bzw. Vol-Verkauf (Covered Calls, Deribit) | Später, nicht jetzt | Varianzprämie belegt, aber Tail-Risiko, Steuerrisiko (Derivate) und Daten-/Venue-Aufwand. |
| 6 | Saisonalität / Tageszeit / Wochentag | No-Go | Effekte im Bereich weniger Basispunkte, statistisch nicht stabil, weit unter den Kosten. |
| 7 | Cross-Exchange- / Dreiecks-Arbitrage | No-Go | Spreads zwischen US-/EU-Börsen liegen um eine Grössenordnung unter den Retail-Kosten. |
| 8 | Market Making | No-Go | Retail-Gebühren und adverse Selektion schliessen es aus. |

---

## 1. Delta-neutraler Funding-/Basis-Carry

**Mechanismus**
- Spot long (BTC oder ETH) und gleich grosser Perp short. Die Preisbewegung hebt sich auf.
- Ertrag: Funding, das die Longs den Shorts zahlen, bzw. die Basis bei Terminkontrakten.
- Ursache laut Literatur: Nachfrage von Kleinanlegern nach gehebelter Long-Exposure, dazu knappes Arbitrage-Kapital wegen Margin-Friktionen.

**Belege**
- Schmeling, Schrimpf, Todorov, «Crypto Carry», BIS Working Paper 1087 (2023), Management Science (2026): https://www.bis.org/publ/work1087.pdf, https://doi.org/10.1287/mnsc.2024.05069. Carry im Mittel über 10 % p. a., zeitweise über 40–60 % p. a., stark schwankend und mit Crashs verknüpft.
- He, Manela, Ross, von Wachter, «Fundamentals of Perpetual Futures» (arXiv 2212.06888): https://arxiv.org/abs/2212.06888. Abweichungen von No-Arbitrage-Preisen sind gross, bewegen sich über Coins gemeinsam und **nehmen über die Zeit ab**. Eine einfache Strategie erzielt hohe Sharpe-Ratios, auch bei Binance-Höchstgebühren.
- Ethena, Dokumentation «Funding Risk» (Stand 31.12.2024): https://docs.ethena.fi/protocol-overview/risks/funding-risk. BTC/ETH-Funding im Mittel 7.8–9 % p. a. über 3 Jahre. 15.9 % (BTC) bzw. 17.5 % (ETH) der Tage negativ. Längste Negativserie 13 Tage. Achtung: Quelle eines Marktteilnehmers mit Eigeninteresse.
- Galaxy Research zur Basis-Kompression (Februar 2025): https://www.galaxy.com/insights/perspectives/bitcoin-sell-off-drives-basis-compression-etf-outflows-and-risk-off. CME-Basis grösstenteils unter 10 % p. a., zeitweise rund 4 %.
- Kraken-Funding-Methode (Kraken MTF, Contract Specifications): https://support.mtf.kraken.com/hc/en-us/articles/25499987607837-Linear-Contract-Specifications. Funding = zeitgewichtete Prämie Perp gegen Index, **ohne fixen Zinsanteil**. Binance hat dagegen einen Sockel von 0.01 %/8 h, rund 10.95 % p. a.

**Exploratorischer Check (Binance-Funding 2020–2023, nicht vorregistriert)**

| Coin | Funding Ø p. a. | 2020 | 2021 | 2022 | 2023 | Tage negativ |
|---|---|---|---|---|---|---|
| BTC | 15.0 % | 17.2 % | 30.6 % | 4.2 % | 7.9 % | 12 % |
| ETH | 18.5 % | 27.4 % | 37.5 % | 0.8 % | 8.3 % | 11 % |
| SOL | −3.6 % | – | 28.6 % | −38.0 % | 1.3 % | 27 % |

- Der Tagesmedian liegt bei fast allen Coins exakt bei 10.95 % p. a. Das ist der Binance-Zinssockel und kein Marktsignal.
- Auffälligkeit BNB: Ø 0.8 % bei nur 26 % positiven Perioden. Vermutlich eine Daten- oder Regelbesonderheit, nicht geprüft.
- **Dauerhaft investiert, netto auf das eingesetzte Kapital** (Annahme: 1.5 × Kapital für Spot und Margin, ein Roundtrip zu 1.0 % pro Jahr):
  - BTC: 2020 10.8 %, 2021 19.7 %, 2022 2.1 %, 2023 4.6 %;
  - ETH: 2020 17.7 %, 2021 24.4 %, 2022 −0.1 %, 2023 4.8 %.
- **Mit Filter** (im Markt, wenn das 7-Tage-Mittel des Funding > 0): netto 6.7 % p. a. (BTC) bzw. 9.9 % p. a. (ETH) auf das Kapital, bei 41 bzw. 33 Schaltvorgängen. Die Kosten fressen rund 4–5 Prozentpunkte p. a. Der Filter lohnt sich mit Spot-Kosten K1 also kaum.

**Realistische Nettorendite nach Kosten:** grob **2–6 % p. a. auf das Kapital (in USD)**, in Boomphasen deutlich mehr, in Bärenmärkten um 0.
- Begründung: Kompression seit 2024 (Ethena, Galaxy, He et al.), kein Zinssockel bei Kraken, Kapitalbedarf über 1×.
- Wichtig: Diese Spanne ist eine **Einschätzung** und kein gemessener Wert für Kraken. Massgebliche Vergleichsgrösse ist der risikolose USD-Satz (2026 rund 4 %, vgl. FRED DTB3). Der Überschuss ist also möglicherweise klein oder null.

**Hauptrisiken**
- Negatives Funding über Wochen (SOL 2022: schlechteste 30-Tage-Summe −36 %).
- Liquidation des Short-Beins bei starken Anstiegen, wenn die Margin nicht rechtzeitig nachgeschossen wird.
- Gegenparteirisiko: Spot und Derivate laufen bei Kraken über verschiedene Gesellschaften (u. a. Bermuda, MiFID/Zypern), FTX-Erfahrung.
- Basisrisiko zwischen Perp-Index und Spot-Fill.
- USD/CHF-Währungsrisiko.
- **Steuer (D4):** Funding-Zahlungen sind vermutlich steuerbares Einkommen und kein steuerfreier Kapitalgewinn. Der Perp-Short dient zwar der Absicherung eigener Bestände (KS 36, Kriterium 5), Volumen und Haltedauer können aber zur Prüfung auf gewerbsmässigen Handel führen. ESTV, Kreisschreiben Nr. 36: https://www.estv2.admin.ch/dvs/kreisschreiben/dbst-ks-2012-1-036-d-de.pdf; ESTV-Arbeitspapier Kryptowährungen: https://www.estv.admin.ch/dam/de/sd-web/HgzNhzz7q7YD/dbst-arbeitspapier-kryptowaehrungen-de.pdf. Vor Live mit Steuerberatung klären.

**Kapital und Infrastruktur**
- Ab rund 2'000–5'000 CHF sinnvoll, damit Mindestgrössen und Rundung nicht dominieren.
- Kraken-Spot- und Kraken-Derivatives-Konto. Zugang für Schweizer Kunden laut Kraken möglich, mit Eignungsprüfung: https://www.kraken.com/ch/pro/perps/crypto-perpetuals, https://support.kraken.com/ch/articles/360023786632-kraken-derivatives-eligibility.
- Täglicher Job für Margin-Überwachung und Rebalancing, im Paper-Betrieb ohne Keys.

**Testbar mit öffentlichen Daten ohne Keys:** ja.
- Binance-Funding 2020–2026 liegt vor; 2024+ bleibt für den vorregistrierten Test reserviert.
- Kraken-Funding ab 2025-09 sammelt der Collector bereits. Die öffentliche Kraken-API liefert historische Funding-Raten.
- Vorbehalt: Die Binance-Funding-Historie 2024+ ging in Stufe 2 bzw. XS21 schon als Kostenkomponente der Short-Beine ein. Als Carry-Outcome wurde sie nie ausgewertet.

**Zeitbedarf Damian:** einmalig rund 1 h (Eignung Kraken Derivatives, Entscheid D4/Steuer), danach nahezu 0. Passt zu D3.

**Go/No-Go:** **GO für Vorregistrierung.** Entwurf: `carry_prereg_entwurf_v0.1.md` (nicht eingefroren).

---

## 2. Volatilitäts-Targeting mit Trendfilter (Overlay)

**Mechanismus**
- Positionsgrösse = Zielvolatilität / realisierte 30-Tage-Volatilität, höchstens 1, kein Hebel.
- Optional nur investiert, wenn der Kurs über dem 200-Tage-Schnitt liegt.
- Volatilität ist gut prognostizierbar, Renditen kaum. Deshalb verbessert sich vor allem das Risikoprofil.

**Belege**
- Harvey, Hoyle, Korgaonkar, Rattray, Sargaison, Van Hemert, «The Impact of Volatility Targeting», Journal of Portfolio Management 45(1), 2018: https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf. Höhere Sharpe-Ratio bei risikoreichen Anlagen wie Aktien, durchgehend kleinere Extremverluste.
- Liu, Tsyvinski, «Risks and Returns of Cryptocurrency», Review of Financial Studies 34(6), 2021: https://academic.oup.com/rfs/article/34/6/2689/5912024. Starkes Time-Series-Momentum in Krypto.

**Exploratorischer Check (Binance 1d 2018–2023, K1, Umschichtung nur bei Abweichung > 0.1, nicht vorregistriert)**

| Variante | BTC CAGR / MaxDD / Sharpe | ETH CAGR / MaxDD / Sharpe |
|---|---|---|
| Buy and Hold | 21.1 % / −81 % / 0.63 | 20.2 % / −94 % / 0.67 |
| Vol-Target 40 % | 20.7 % / −65 % / 0.65 | 21.8 % / −69 % / 0.67 |
| Vol-Target 40 % + Trend 200 | 25.4 % / −47 % / 0.92 | 35.2 % / −42 % / 1.12 |
| Vol-Target 60 % + Trend 200 | 30.7 % / −61 % / 0.90 | 49.3 % / −54 % / 1.13 |

- Vol-Targeting allein: gleiche Rendite, deutlich kleinerer Drawdown, Sharpe kaum besser. Das stimmt mit Harvey et al. überein.
- Der Mehrertrag stammt vom Trendfilter. Er ist durch Parameterwahl (200 Tage, 40/60 %) und die gleiche Datenperiode wie Stufe 2 belastet. Der Grad an Outcome-Information ist hoch, die Evidenzklasse höchstens Development.

**Realistische Nettorendite:** kein belastbarer Mehrertrag gegenüber Buy and Hold. Realistisch ist eine **Halbierung von Volatilität und Drawdown bei ähnlicher bis etwas tieferer Rendite**.

**Hauptrisiken**
- Whipsaw in Seitwärtsphasen.
- Starke Korrelation mit Turtle 55/20 und W2/W6 (gleiche Quelle: Trend).
- Overfitting der Parameter.

**Kapital und Infrastruktur:** gering. Spot, tägliche Entscheidung, rund 10–20 Umschichtungen pro Jahr und Coin. Das passt zu KS 36: Volumen deutlich unter 5× des Bestands.

**Testbar:** ja, vollständig mit öffentlichen Kursen. 2024+ ist für den Test reserviert; die Holdout-Regeln der Governance gelten.

**Zeitbedarf Damian:** nahezu 0.

**Go/No-Go:** **GO für Vorregistrierung, aber nur als Risiko-Overlay auf den bestehenden Paper-Kandidaten.** Gemessen werden soll die Risikotransformation, nicht neue Alpha. So bleibt das Trial-Budget klein.

---

## 3. Staking bzw. Geldmarkt als Basisrendite

**Mechanismus:** Proof-of-Stake-Belohnungen (Inflation und Gebühren des Netzwerks) bzw. Zins auf USD- oder CHF-Geldmarkt.

**Belege**
- Kraken Schweiz, Stand 01.10.2026: ETH bis 2.58 % APY, SOL bis 5.69 % APY: https://www.kraken.com/ch/features/staking/ethereum, https://www.kraken.com/ch/features/staking/solana.
- Ethena nennt rund 3 % für stETH (Quelle oben).

**Realistische Nettorendite:** 2.5–6 % p. a. in Coin-Einheiten, real weitgehend durch Token-Inflation verwässert. Das volle Kursrisiko bleibt.

**Risiken**
- Kursrisiko, Lock-up bei «bonded» ETH, Slashing, Gegenpartei Kraken.
- Steuer: Staking-Erträge gelten als Einkommen (ESTV-Arbeitspapier).

**Kapital, Infrastruktur, Zeit:** minimal; einmal 15 Minuten von Damian, falls gewünscht.

**Testbar:** nicht nötig.

**Go/No-Go:** **GO als Benchmark.** Jede Strategie sollte gegen «Buy and Hold + Staking» und gegen den risikolosen Satz berichtet werden.

---

## 4. Rebalancing-Prämie im diversifizierten Korb

**Mechanismus:** Regelmässiges Zurücksetzen auf Gleichgewichtung erntet Volatilität bei Korrelationen unter 1.

**Beleg:** Bouchey, Nemtchinov, Paulsen, Stein, «Volatility Harvesting: Why Does Diversifying and Rebalancing Create Portfolio Growth?», Journal of Wealth Management 15(2), 2012: http://www.snifferquant.com/gyantal/Incode/papers/Volatility%20Harvesting_JWM_Fall_2012.pdf.

**Exploratorischer Check** (BTC, ETH, XRP, LTC, ADA, BNB, Juni 2018 bis 2023, K1):
- Buy and Hold gleichgewichtet: CAGR 37.6 %, MaxDD −74 %.
- Monatliches Rebalancing: 41.5 %, −76 %.
- Quartalsweises Rebalancing: 39.7 %, −76 %.
- BTC allein: 36.2 %, −77 %.
- Mehrertrag von rund 2–4 Prozentpunkten p. a., aber kein Risikovorteil.
- Der Korb besteht aus Überlebenden (Survivorship). Mit Ausfällen wie LUNA oder FTT wäre das Bild schlechter.

**Realistische Nettorendite:** 0–3 Prozentpunkte p. a. über Buy and Hold, unsicher.

**Risiken:** Korbwahl, Delistings, Rebalancing in fallende Coins hinein.

**Testbar:** ja.

**Zeitbedarf Damian:** 0.

**Go/No-Go:** No-Go als eigene Strategie. Als Konstruktionsregel denkbar, falls ein Korb ohnehin gehalten wird.

---

## 5. Optionen bzw. Vol-Verkauf

**Mechanismus:** Implizite Volatilität liegt im Mittel über der realisierten (Varianzprämie). Covered Calls auf gehaltene BTC/ETH oder Cash-Secured Puts verkaufen diese Prämie.

**Beleg:** Alexander, Imeraj, «The Bitcoin VIX and Its Variance Risk Premium», Journal of Alternative Investments 23(4), 2021: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3383734. Untersucht nur 2019–2020, also kurz.

**Venue:** Deribit schliesst die Schweiz nicht aus (Liste vom 19.03.2026: https://support.deribit.com/hc/en-us/articles/25944487427741-Restricted-Jurisdictions). Kraken bietet für Schweizer Kunden keine Krypto-Optionen an; nicht abschliessend geprüft.

**Realistische Nettorendite:** nicht seriös bezifferbar ohne Test. In Aufwärtstrends deckelt ein Covered Call die Rendite.

**Risiken**
- Tail-Risiko (Crash bei Short-Puts, verpasste Rallyes bei Calls).
- Neue Börse als Gegenpartei.
- Steuer: KS 36, Kriterium 5. Derivate, die nicht nur der Absicherung dienen, sind ein Indiz für gewerbsmässigen Handel.

**Testbar:** teilweise. Die öffentliche Deribit-API liefert DVOL-Index und Trade-Historie; vollständige historische Optionsketten sind kostenpflichtig.

**Zeitbedarf Damian:** zusätzliches Konto, KYC, Steuerklärung, also mehr als D3 erlaubt.

**Go/No-Go:** Später. Frühestens, wenn Carry und Paper laufen.

---

## 6. Saisonalität / Tageszeit / Wochentag

**Beleg:** Baur, Cahill, Godfrey, Liu, Finance Research Letters 31 (2019): https://ideas.repec.org/a/eee/finlet/v31y2019icp78-92.html. Keine dauerhaften Effekte bei Tageszeit, Wochentag oder Monat.

**Exploratorischer Check** (BTC 1h, Binance, 2018–2023):
- Stundenmittel zwischen −3.7 und +3.6 Basispunkte.
- Grösstes |t| 2.5 über 24 Stunden, was bei 24 Tests nach Zufall aussieht.
- Korrelation des Stundenprofils 2018–2020 gegen 2021–2023: 0.46.
- Wochentage: |t| unter 1.6.
- Ein K1-Roundtrip kostet 90 Basispunkte.

**Go/No-Go:** No-Go. Kosten rund 25-mal grösser als der Effekt.

---

## 7. Cross-Exchange- / Dreiecks-Arbitrage

**Beleg:** Makarov, Schoar, «Trading and Arbitrage in Cryptocurrency Markets», Journal of Financial Economics 135(2), 2020: https://doi.org/10.1016/j.jfineco.2019.07.001. Grosse Spreads vor allem **zwischen Ländern** mit Kapitalverkehrskontrollen (z. B. Korea), innerhalb von Ländern klein.

**Exploratorischer Check** (Tagesschluss BTC/USD, 2019–2023, Zeitstempel nicht exakt synchron):
- |Kraken − Coinbase|: Median 2.6 Basispunkte, 95 %-Quantil 9.8 Basispunkte.
- |Kraken − Bitstamp|: Median 3.1, 95 %-Quantil 11.0 Basispunkte.
- An 0 % der Tage über den 90 Basispunkten Roundtrip.
- Dreiecks-Arbitrage braucht Latenz im Millisekundenbereich und Taker-Gebühren auf drei Beinen, für Retail aussichtslos.

**Go/No-Go:** No-Go.

---

## 8. Market Making

**Mechanismus:** Spread verdienen, Inventar steuern.

**Hürde**
- Der Kraken-Spot-Maker kostet in Tier 1 0.40 % je Seite (`config/cost_model_v1.json`, venue_kraken), während der BTC-Spread nahe 1 Basispunkt liegt.
- Profis haben Rebates, Kolokation und Inventarmodelle; Retail trägt die adverse Selektion.
- Das Altprojekt zeigte schon für Intraday eine Fee-to-Gross-Quote von 220 % (`AURUM_II_FINDINGS_DIGEST_2026-09-15.md`).

**Go/No-Go:** No-Go.

---

## Empfohlene Reihenfolge (passt zu D3)

1. **Carry:** Vorregistrierungs-Entwurf v0.1 liegt bei. Damian prüft und gibt frei; mit Claude-Review rund 30–45 Minuten. Danach Freeze und ein Lauf auf 2024-01-01 bis 2026-08 (Binance) plus Kraken ab 2025-09, ausschliesslich mit öffentlichen Daten. Bei Bestehen Paper-Betrieb parallel zu W2/W6/Turtle.
2. **Vol-Target-Overlay** als kleine Vorregistrierung auf die bestehenden Paper-Kandidaten, mit Ziel Risikotransformation.
3. **Benchmark** «Buy and Hold + Staking» und risikoloser Satz in alle künftigen Berichte.

Trial-Accounting: Die explorativen Checks dieses Dokuments zählen als **rund 20 zusätzliche informelle Trials**, und künftige Vorregistrierungen müssen das deklarieren. Grund: Varianten bei Carry, Vol-Target, Rebalancing und Saisonalität.

## Quellenhinweis

- Alle Links wurden am 01.10.2026 abgerufen bzw. per Suche bestätigt.
- Zahlen aus Sekundärquellen, die sich nicht direkt verifizieren liessen (etwa BitMEX-Quartalsberichte 2025), sind bewusst nicht übernommen.
