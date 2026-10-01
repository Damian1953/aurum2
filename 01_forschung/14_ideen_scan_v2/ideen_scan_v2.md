# Ideen-Scan v2: Krypto-Strategien für ein Schweizer Privatkonto (zweite Runde)

**Status:** Recherche + explorative Vorprüfung. Keine Vorregistrierung eingefroren, kein Test gelaufen, kein Holdout geöffnet, keine Keys, kein Trading.
**Stand:** 2026-10-01 22:25 (Zürich, UTC+2). Auftrag: Steering-Nachricht nach Verwerfung des Funding-Carry (Entscheid Damian 2026-10-01 22:16).
**Mandat:** Spot-long bevorzugt, ≤ 1 h/Woche Aufwand für Damian, idealerweise keine Derivate. Kosten K1 (Kraken Spot, 0.47 % je Seite inkl. Slippage), Cash verzinst mit DTB3.
**Ausgeschlossen (bereits geschlossen oder getestet):** Lane A (Bottom/Reversal/Rebound/DT), XS21, Carry, Saisonalität, Cross-Exchange-Arb, Market Making. W2/W6/Turtle 55/20 laufen bereits im Paper (PAPER v1.0).

## 0. Daten- und Schnittdeklaration (bitte zuerst lesen)

- Alle explorativen Rechnungen nur auf Daten **vor 2024-01-01**. Kein Zugriff auf `02_daten/holdout/` oder `holdout_manifest*`.
- Preise: Binance Spot 1d BTCUSDT/ETHUSDT aus `data/raw/binance_full` (geschnitten < 2024), ergänzend CoinMetrics PriceUSD ab 2014.
- Freie, öffentliche Zusatzdaten (ohne Key), abgelegt in `/workspace/aurum2/work/scan_v2/raw/`, SHA256 in `rohdaten_SHA256SUMS.txt`:
  - CoinMetrics Community API: BTC `CapMVRVCur`, `FlowInExNtv`, `FlowOutExNtv`, `SplyExNtv`, `CapMrktCurUSD`, `PriceUSD`; ETH `CapMVRVCur`, `PriceUSD`.
  - alternative.me Fear & Greed (ab 2018-02).
  - DefiLlama Stablecoin-Gesamtangebot (ab 2017-11).
  - FRED: `DTWEXBGS` (Dollar-Index breit), `DFII10` (Realzins 10J), `WALCL`, `RRPONTSYD`, `WTREGEN` (für Fed-Netto-Liquidität).
- Skript: `tools/ideen/explorativ_scan_v2.py` (SHA256 ea6783b0…), Resultat `explorativ_scan_v2.json` (SHA256 53dd15d0…).
- **Informelle Trials:** 10 neue (t1–t10) + Referenzen (Buy&Hold, SMA200). Globaler Zähler damit ca. **270** (vorher ca. 260 nach Carry-Deklaration). Alle Zahlen unten sind **In-Sample-Explorationen** und kein Beleg.
- **Vorbelastung:** ETH-Daten < 2024 wurden hier (t8–t10) und bereits in Scan v1 verwendet. Wenn ETH gemäss F1 als «unberührter» Markt gelten soll, ist das nur noch für ETH ≥ 2024 wahr. BTC-Preise ≥ 2024 sind dem Team in groben Zügen bekannt (Stage 2, Paper, allgemeine Marktkenntnis). Für die hier neuen Signale (MVRV, Makro) wurden **keine** Resultate ≥ 2024 berechnet.

## 1. Kurzfazit

| # | Kandidat | Evidenz | Daten frei? | Explorativ 2017-08 bis 2023 (CAGR / Sharpe ex / MaxDD) | ab 2021 (Sharpe) | Urteil |
|---|---|---|---|---|---|---|
| Ref | BTC Buy&Hold | – | ja | 43.1 % / 0.84 / −83 % | 0.48 | Benchmark |
| Ref | BTC SMA200 (≈ W2-Familie) | – | ja | 24.2 % / 0.67 / −66 % | 0.45 | Benchmark |
| t1 | **MVRV-Bewertungsband** (rein < 1.0, raus > 3.5) | 1 Peer-Review (2026), In-Sample | ja | 51.6 % / 1.06 / −63 % (3 Wechsel) | 0.91 | **GO als Prereg-Entwurf B** (Testbarkeit gering) |
| t7 | **Fed-Netto-Liquidität** 13 W > 0 | gemischt (FRL 2023, SSRN 2024; Gegenbeleg RFS 2021) | ja | 48.6 % / 0.98 / −63 % (32 Wechsel) | 0.63 | **GO als Prereg-Entwurf A** |
| t6 | Dollar schwach (DXY < SMA100) | schwach/praktikerlastig | ja | 41.9 % / 0.92 / −61 % (52 Wechsel) | 0.71 | Beobachten (nur als Sensitivität in A) |
| t2 | SMA200 + MVRV-Bremse | – | ja | 13.6 % / 0.47 / −64 % | 0.03 | NO-GO |
| t3 | Exchange-Bestand sinkt 30 T | Praktiker | ja, aber revidiert | 3.3 % / 0.25 / −61 % | −0.25 | NO-GO (Look-ahead, schwach) |
| t4 | Stablecoin-Wachstum 30 T | schwach, Lead-Lag umgekehrt | ja | 25.6 % / 0.66 / −66 % | 0.45 | NO-GO |
| t5 | Fear & Greed konträr | gemischt, OOS negativ | ja | −4.4 % / 0.19 / −78 % | 0.19 | NO-GO |
| t8 | ETH/BTC-Rotation (SMA50) | Kointegration scheitert | ja | 39.2 % / 0.80 / −82 % | 0.38 | NO-GO |
| t9 | Dual Momentum BTC/ETH/Cash 90 T | Antonacci (Aktien) | ja | 24.3 % / 0.65 / −80 % | 0.40 | NO-GO (redundant zu W2) |
| t10 | Inverse-Vol BTC/ETH (Risk Parity light) | Low-Vol-Effekt schwach | ja | 43.4 % / 0.84 / −87 % | ≈ 50/50 | NO-GO (kein Mehrwert) |
| – | BTC-Dominanz / Altseason | nur Praktiker | teils (kostenpflichtig) | nicht gerechnet | – | NO-GO |
| – | Post-Listing / Token-Unlocks | ja (Reversal/Abverkauf) | Unlocks nur kostenpflichtig | nicht gerechnet | – | NO-GO (braucht Short) |
| – | Kurzfrist-Mean-Reversion Majors Kraken | Reversal v. a. illiquide Coins | ja | nicht gerechnet | – | NO-GO (Kosten; Entscheid 2026-09-15) |
| – | Vol-Target-Overlay (aus Scan v1) | Moreira/Muir 2017 | ja | siehe Scan v1 | – | bleibt GO-Kandidat aus v1 |

**Ehrliche Kernaussage:** Kein Kandidat zeigt eine robuste, statistisch belastbare Rendite-Edge. Die zwei besten Kandidaten sind **Risiko-Transformationen** (weniger Drawdown, ähnliche oder leicht bessere Rendite als Buy&Hold) mit sehr wenigen unabhängigen Ereignissen. Realistisch ist «Buy&Hold mit weniger Schmerz», nicht «Alpha».

## 2. Kandidaten im Einzelnen

### 2.1 MVRV-Bewertungsband (t1) — GO als Entwurf B

- **Mechanismus:** MVRV = Marktkapitalisierung / Realized Cap (Durchschnitts-Einstandswert aller Coins on-chain). Hohe Werte = Halter mit grossem unrealisiertem Gewinn, Verkaufsdruck und Euphorie; < 1 = Markt unter dem durchschnittlichen Einstand, Kapitulation. Zyklische Bewertungsregel, kein Kurzfristsignal.
- **Evidenz:**
  - Grobys, Näsman, Sandretto (2026), «Using on-chain data to predict Bitcoin cycles», *Research in International Business and Finance* 89: https://ideas.repec.org/a/eee/riibaf/v89y2026ics0275531926002138.html — MVRV-Z-Regel mit Sharpe 1.28 vs. 0.45 Buy&Hold, aber nur ca. 3 Trades und In-Sample.
  - Informeller Walk-Forward (GitHub, nicht begutachtet): https://github.com/lonelyobserver0/mvrv-regime-monitor — OOS 2022–2026 nur 1 Trade; weist selbst auf mögliches Abschwächen der Zyklen (ETF-Ära) hin.
- **Daten:** CoinMetrics Community `CapMVRVCur`, täglich, frei, ohne Key. Realized Cap ist aus der Blockchain deterministisch, kaum revisionsanfällig (anders als Exchange-Labels).
- **Explorativ:** 2017-08 bis 2023: 51.6 % / 1.06 / −63 % bei 3 Wechseln; bis 2020 Sharpe 1.19 (B&H 1.09), ab 2021 Sharpe 0.91 bei MaxDD −35 % (B&H Sharpe 0.48). CoinMetrics 2014–2023: 62.2 % / 1.18 / −61 % vs. B&H 49.5 % / 0.91 / −84 % (5 Wechsel). Korrelation mit SMA200-Exposition 0.55.
- **Realistisch netto nach K1:** Kosten vernachlässigbar (≈ 1 Wechsel pro 1–2 Jahre, < 0.5 %/J). Erwartung: ungefähr Buy&Hold-Rendite ±10 Pp/J, mit deutlich tieferem Drawdown **falls** die Zyklen bestehen bleiben.
- **Überanpassungsrisiko: hoch.** Die Schwellen 1.0/3.5 sind Praktiker-Folklore, die in Kenntnis der Spitzen 2013/2017 entstanden ist. N ≈ 3–5 Zyklen. Die Zyklusspitzen fielen bereits (2021 erreichte MVRV die 3.5 nur im Frühjahr, nicht beim Novemberhoch). Wenn künftige Spitzen unter 3.5 bleiben, wird die Regel zu Buy&Hold mit Verzögerung (und verpasst das Aussteigen).
- **Praxis Schweiz:** ideal: Spot, sehr wenige Trades (spricht steuerlich gegen gewerbsmässigen Handel nach KS 36), ≈ 5 Min./Woche (eine Zahl ablesen).
- **Urteil:** GO als Vorregistrierungs-**Entwurf**, aber mit ehrlicher Feststellung, dass ein Test 2024+ kaum Aussagekraft haben kann (0–2 Ereignisse). Eher als Kernbestand-Regel für langfristige Bestände denken als als eigener «Sleeve».

### 2.2 Makro-/Liquiditäts-Regime (t7, t6) — GO als Entwurf A (t7)

- **Mechanismus:** BTC als Liquiditäts-/Risikoanlage: wächst die Fed-Netto-Liquidität (Bilanz WALCL minus Treasury-Konto TGA minus Reverse Repo), steigt die Risikobereitschaft; ein schwacher Dollar wirkt ähnlich.
- **Evidenz (gemischt):**
  - Finance Research Letters 57 (2023), «The effects of quantitative easing on Bitcoin prices»: https://ideas.repec.org/a/eee/finlet/v57y2023ics1544612323006049.html — zeitvariable, temporäre Effekte; langfristig positiver Liquiditätskanal.
  - SSRN 4904716 (2024), «Does Monetary Liquidity Affect Bitcoin Price?»: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4904716 — hoher Erklärungsanteil nach COVID (Working Paper).
  - Masterarbeiten Tilburg: http://arno.uvt.nl/show.cgi?fid=187959 und http://arno.uvt.nl/show.cgi?fid=191939 — Effekte klein/temporär bzw. instabil.
  - **Gegenbeleg:** Liu & Tsyvinski (2021), *RFS* 34(6), «Risks and Returns of Cryptocurrency»: https://ideas.repec.org/a/oup/rfinst/v34y2021i6p2689-2727..html — BTC ohne signifikante Exposition gegenüber klassischen Makrofaktoren (Stichprobe bis 2018).
- **Daten:** FRED, frei. H.4.1 erscheint donnerstags (Stand Mittwoch). Revisionen gering; für PiT sollte ALFRED (Vintages) verwendet werden.
- **Explorativ (t7):** 48.6 % / 0.98 / −63 %, 32 Wechsel (≈ 5/J); bis 2020 Sharpe 1.25, ab 2021 Sharpe 0.63 (B&H 0.48, SMA200 0.45), MaxDD ab 2021 −53 %. t6 (DXY < SMA100): 41.9 % / 0.92 / −61 %, ab 2021 Sharpe 0.71, 52 Wechsel.
- **Realistisch netto nach K1:** ≈ 5 Wechsel/J × 2 × 0.47 % ≈ 2–3 %/J Kosten (in den Zahlen enthalten). Erwartung: grob B&H-ähnliche Rendite mit −20 bis −30 % geringerem Drawdown; Edge gegenüber SMA200 unsicher.
- **Überanpassungsrisiko: mittel bis hoch.** Im Wesentlichen ein Zyklus (QE 2020 / QT 2022). Fenster (13 W, SMA100) ungetunt gewählt, aber der Kandidat selbst stammt aus öffentlicher Praktiker-Narrativ, die mit Blick auf 2020–2022 entstand. Überlappung mit Trend (Korrelation 0.53).
- **Praxis:** Spot, wöchentlich ein Blick (≈ 10 Min.), ≈ 5 Trades/J. Steuerlich vertretbar, aber mehr Handelsaktivität als MVRV.
- **Urteil:** GO als Vorregistrierungs-Entwurf A (nur t7; t6 als vorab fixierte Sensitivität, nicht als zweite Hypothese). Testperiode 2024+ liefert ≈ 10–15 Wechsel, also wenigstens etwas Aussagekraft.

### 2.3 Exchange-Netflows / Exchange-Bestand (t3) — NO-GO
- **Mechanismus:** Abflüsse von Börsen = Akkumulation, weniger Verkaufsangebot.
- **Evidenz:** v. a. Praktiker (Glassnode/CryptoQuant-Blogs), keine robuste Peer-Review-Evidenz für eine handelbare Regel gefunden.
- **Daten:** CoinMetrics frei, aber **Adress-Labels werden rückwirkend revidiert** → historische Serien enthalten Look-ahead.
- **Explorativ:** 3.3 % / 0.25, 145 Wechsel, ab 2021 negativ. **NO-GO.**

### 2.4 Stablecoin-Angebotswachstum (t4) — NO-GO
- **Evidenz:** Ante et al. (2021), *Technological Forecasting & Social Change* 170: https://ideas.repec.org/a/eee/tefoso/v170y2021ics0040162521002833.html — nur kurzfristige (stündliche) Effekte von Tether-Emissionen. Lead-Lag-Analyse (Praktiker) findet eher BTC → Stablecoin-Angebot: https://coincise.co/stablecoin
- **Explorativ:** 25.6 % / 0.66, ab 2021 Sharpe 0.45 (< B&H). **NO-GO.**

### 2.5 Fear & Greed (t5) — NO-GO
- **Evidenz:** Positiv: Finance Research Letters 58 (2023): https://ideas.repec.org/a/eee/finlet/v58y2023ipas154461232300778x.html. Kritisch: *Digital Finance* (2026): https://link.springer.com/article/10.1007/s42521-026-00218-y — kein Out-of-Sample-Mehrwert.
- **Explorativ:** konträre Regel −4.4 %/J; Forward-30-T-Median je Zustand zeigt eher Momentum (extreme Gier +17 %, extreme Angst +1.7 %), also keinen konträren Effekt. **NO-GO.**

### 2.6 BTC-Dominanz / Altseason-Rotation — NO-GO
- Nur Praktiker-Quellen, keine akademische Evidenz gefunden. Dominanz-Historien frei nur lückenhaft (CoinGecko-Historie limitiert, TradingView nicht frei exportierbar). Altcoin-Exposition widerspricht dem Mandat (Survivorship, Delistings, Liquidität). Die nächstverwandte, prüfbare Form (ETH/BTC-Rotation t8) scheitert ab 2021. **NO-GO.**

### 2.7 ETH/BTC-Paar-/Ratio-Trading spot-only (t8) — NO-GO
- **Evidenz:** Kointegration ETH/BTC instabil, publizierte Pair-Strategie scheitert: https://validatedstrategies.com/strategy/PAR. Spot-only heisst ausserdem: nur Rotation, kein echter Spread.
- **Explorativ:** 136 Wechsel, ab 2021 1.8 %/J, MaxDD −82 %. **NO-GO.**

### 2.8 Dual Momentum BTC vs. Cash (t9) — NO-GO
- **Evidenz:** Antonacci, SSRN 2042750: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2042750 (Aktien/Anleihen). Für Krypto: Han, Kang, Ryu, SSRN 4675565: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4675565 — Time-Series-Momentum stark, Querschnitt nach Kosten schwach.
- **Beurteilung:** Der absolute-Momentum-Teil ist exakt das, was W2/W6/Turtle schon abdecken. Explorativ schlechter (ab 2021 Sharpe 0.40, MaxDD −80 %). **NO-GO (redundant).**

### 2.9 Risk-Parity-Korb (t10) — NO-GO
- **Evidenz:** Low-Vol in Krypto schwach (Finance Research Letters 2022): https://www.sciencedirect.com/science/article/pii/S1544612321004116
- **Explorativ:** inverse Vol BTC/ETH ≈ 50/50-Korb (43.4 % / 0.84 / −87 % vs. 41.7 % / 0.82 / −88 %). Zwei hoch korrelierte Anlagen geben keine Diversifikation. **NO-GO.** (Risiko-Reduktion besser über Vol-Target-Overlay aus Scan v1.)

### 2.10 Post-Listing- und Token-Unlock-Effekte — NO-GO
- **Evidenz:** Post-Listing-Reversal: Blockchain Research Lab WP 5: https://www.blockchainresearchlab.org/wp-content/uploads/2020/02/BRL-Working-Paper-5.pdf; SSRN 4715718: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4715718. Unlocks: Keyrock-Studie (16 000 Unlocks): https://keyrock.com/from-locked-to-liquidity-what-16000-token-unlocks-teach-us/
- **Beurteilung:** Effekte sind überwiegend negativ (Abverkauf nach Listing/Unlock) → Ausbeutung braucht Short/Perps; Unlock-Kalender historisch nur kostenpflichtig (Token Unlocks/Tokenomist); Small-Caps mit hohen Kosten. Spot-long-Variante («Unlock meiden») hat für Majors kaum Relevanz. **NO-GO.**

### 2.11 Kurzfrist-Mean-Reversion Majors auf Kraken Spot — NO-GO
- **Evidenz:** Reversal v. a. in illiquiden Coins, Majors zeigen eher Momentum: https://www.sciencedirect.com/science/article/pii/S1057521921002349
- **Beurteilung:** Bei K1 0.47 %/Seite und täglicher Frequenz sind Kosten prohibitiv; zudem bereits durch ENTSCHEID 2026-09-15 (Kurzfrist-MR) geschlossen und mit Lane A verwandt. Nicht gerechnet. **NO-GO.**

### 2.12 Weitere Literatur 2023–2026 (geprüft, nichts Neues für das Mandat)
- Zeitreihen-Momentum/Trend ist die am besten belegte Krypto-Anomalie (Han/Kang/Ryu; Liu/Tsyvinski) — durch W2/W6/Turtle abgedeckt.
- Volatilitäts-Management (Moreira & Muir, *JF* 2017: https://onlinelibrary.wiley.com/doi/10.1111/jofi.12513) — durch Vol-Target-Kandidat aus Scan v1 abgedeckt.

## 3. Empfehlung

1. **Entwurf A — Fed-Netto-Liquiditäts-Regime BTC Spot** (`makro_liq_prereg_entwurf_v0.1.md`): am ehesten testbar (≈ 10–15 Wechsel in 2024–2026), Spot, ≤ 10 Min./Woche. Erwartung ehrlich: Drawdown-Reduktion, keine sichere Mehrrendite.
2. **Entwurf B — MVRV-Bewertungsband BTC Spot** (`mvrv_prereg_entwurf_v0.1.md`): praktisch ideal für Damian (fast kein Aufwand, steuerfreundlich), aber statistisch kaum je bestätigbar; Test 2024+ hat wahrscheinlich 0–2 Ereignisse. Eher als dokumentierte Kernbestand-Regel mit Paper-Beobachtung über Jahre.
3. Beide nur **nach** Review durch Claude und Entscheid Damian einfrieren. Nicht beide gleichzeitig als «Gewinner» werten: ein gemeinsamer Trial-Rahmen mit Holm-Korrektur über A und B (siehe Entwürfe).
4. Grundsätzlich: Die realistischste Verbesserung für ein Privatkonto bleibt ein **einfacher BTC-Kernbestand** plus die bereits laufenden Trend-Sleeves (Paper) plus allenfalls Vol-Target. Neue Signale sind Feinschliff, keine neue Ertragsquelle.

## 4. Trial-Buchhaltung

| Quelle | Trials |
|---|---|
| bis Carry-Verwerfung (ENTSCHEIDE 2026-10-01 22:16) | ca. 260 |
| Scan v2 t1–t10 (informell, < 2024) | 10 |
| Referenzen B&H/SMA200, Halbierungen, CM-2014-Variante | nicht als Trials gezählt (Benchmarks/Robustheit derselben Regel) |
| **Global** | **ca. 270** |
