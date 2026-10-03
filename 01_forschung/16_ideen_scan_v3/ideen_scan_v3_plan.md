# Ideen-Scan v3: Plan (Schritt 1)

**Status:** Plan, reine Offline-Forschung. Keine neue Forward- oder Paper-Linie bis zum Betriebs-Review 2027-02-02 (Moratorium, ENTSCHEIDE 2026-10-02). Kein Holdout, keine Keys, kein Trading.
**Stand:** 2026-10-03 08:35 (Zürich, UTC+2). Auftrag: Damian (über Haupt-Agenten).
**Regeln:** Spot long, Kraken-ausführbares Universum U2 (B8), keine Nicht-Krypto-Instrumente (B7; Nicht-Krypto-**Daten** als Signal sind zulässig), Kosten K1 (`venue_kraken` `maker_plan`, 0.47 % je Seite, Roundtrip 0.94 %). Geschlossen und ausgeschlossen: Lane A (Bottom/Reversal/Rebound/DT), XS21, Funding-Carry. Discovery nur Daten bis 2023-12-31; Holdout-Ordner sind bei jeder Suche ausgeschlossen.
**Trial-Zähler vor Scan v3:** rund 270 (ENTSCHEIDE 2026-10-01 22:35).

## 0. Abgrenzung: Beispiele aus dem Auftrag, die NICHT neu sind
- **Kalender/Wochenende:** in Scan v1 §6 geprüft (No-Go, Effekte im Basispunktbereich, Kosten rund 25-mal grösser) und Saisonalität ist ausgeschlossen. Nicht erneut.
- **Stablecoin-Angebotswachstum, Exchange-Netflows:** in Scan v2 t3/t4 geprüft (No-Go; Netflows zusätzlich Look-ahead durch revidierte Adress-Labels). Nach der Methodenregel (ENTSCHEIDE, «neuer Mechanismus, neue Vorregistrierung») nur mit klar anderem Mechanismus zulässig; siehe F8, niedrigste Priorität.
- **Regime-Filter aus bestehenden Signalen:** teilweise in v2 (t2 SMA200 + MVRV-Bremse, No-Go). Als F7 nur mit Vorbelastungsvermerk.

## 1. Hypothesen-Familien

| # | Familie | Ökonomische Begründung | Daten (frei, öffentlich) | auf der Box? | Budget (Trials) |
|---|---|---|---|---|---|
| F1 | **Halving-Zyklus** (BTC) | Angebotsschock: Halbierung der Neuemission senkt den Verkaufsdruck der Miner; mögliche verzögerte Preisreaktion | Halving-Daten (öffentlich, Blockhöhe), CoinMetrics Community PriceUSD ab 2014 | ja (< 2024) | 1 (nur deskriptiv) |
| F2 | **BTC → Altcoin Lead-Lag** (täglich) | Informationsdiffusion: Kapital und Aufmerksamkeit fliessen zuerst in BTC, illiquidere Coins reagieren verzögert (begrenzte Aufmerksamkeit, Arbitragekosten) | Binance Spot 1d (Proxy), Kraken OHLC für U2 | ja (< 2024, 10 Coins) | 2 |
| F3 | **Volatilitätsrisikoprämie als Timing-Signal** (BTC Spot) | Hohe implizite gegenüber realisierter Vola = Angst/Absicherungsnachfrage; Prämienentschädigung führt zu höheren Folgerenditen des Basiswerts | Deribit DVOL (öffentliche API, ab 2021-03), realisierte Vola aus Spot | nein | 2 |
| F4 | **Abnormales Volumen / Aufmerksamkeit** (Zeitreihe je Coin, kein Querschnitts-Ranking) | High-Volume-Return-Premium (Gervais/Kaniel/Mingelgrin 2001): Sichtbarkeitsschock erhöht die Investorenbasis | Binance/Kraken Volumen 1d | ja (< 2024) | 2 |
| F5 | **On-Chain-Aktivität** (aktive Adressen, Gebühren, NVT) | Netzwerknutzung als Fundamentalwert (Metcalfe); Bewertung relativ zur Nutzung statt zum Einstand (anders als MVRV) | CoinMetrics Community (AdrActCnt, FeeTotUSD, TxTfrValAdjUSD) | nein | 2 |
| F6 | **Aktien-Risikoappetit-Regime** (VIX, S&P-500-Trend) | Gemeinsamer Risikofaktor: in Stressphasen werden Krypto-Positionen mit Aktien abgebaut | FRED VIXCLS, SP500 (nur 10 Jahre frei) | nein | 2 |
| F7 | **Regime-Ensemble** (W2-Trend + MAKRO_LIQ + MVRV, Mehrheitsregel) | Diversifikation über schwach korrelierte Regime-Signale | vorhanden | ja | 2 (Vorbelastung hoch) |
| F8 | **Stablecoin Supply Ratio** (BTC-Marktwert / Stablecoin-Marktwert) | «Trockenes Pulver» relativ zur Bewertung statt Wachstum (anders als v2 t4) | DefiLlama, CoinMetrics | ja | 1 (Vorbelastung v2) |

**Gesamtbudget Scan v3:** höchstens 14 Trials, globaler Zähler damit höchstens rund 284. Ein Trial = eine vorab fixierte Regel auf einem Datensatz. Varianten nach Sicht der Ergebnisse sind verboten.

## 2. Kill-Kriterien je Familie (Screening, vor jeder Vorregistrierung)
Allgemein (alle Familien): Kill, wenn **eines** zutrifft:
- K-a: Brutto-Effekt je Trade kleiner als 2 × K1-Roundtrip (< 1.88 %) bei Handelsregeln, bzw. kein Mehrwert gegenüber BTC Buy&Hold und SMA200 bei Regimeregeln (Sharpe-Differenz ≤ 0).
- K-b: Vorzeichen in den Hälften 2018–2020 und 2021–2023 nicht gleich.
- K-c: |t| < 2 (Datums-Cluster, d. h. ein Mittelwert je Datum).
Zusätzlich je Familie:
- F1: N < 5 Zyklen → grundsätzlich «nicht prüfbar»; nur Bericht, ob Halving-Fenster über MVRV-Zustand (Linie B) hinaus etwas erklärt. Kein Sleeve-Kandidat.
- F2: Kill, wenn der Effekt nur in den 3 illiquidesten Coins auftritt (U2-Ausführbarkeit) oder nach K1 negativ ist.
- F3: Kill, wenn < 30 unabhängige Signal-Episoden 2021–2023 (DVOL-Historie zu kurz).
- F4: Kill, wenn Korrelation mit Lane-A-Rebound-Signalen > 0.5 (Überlappung mit geschlossener Lane).
- F5: Kill, wenn Korrelation mit MVRV-Zustand > 0.7 (redundant zu Linie B).
- F6: Kill, wenn Korrelation mit W2-Exposition > 0.7 (redundant zu Trend).
- F7: Kill, wenn Ensemble nicht beide Einzelsignale **und** SMA200 in beiden Hälften schlägt.
- F8: Kill, wenn Korrelation mit t4 (v2) > 0.5.

## 3. Reihenfolge (billigste zuerst)
1. **F2** Lead-Lag: Daten auf der Box, eine Tabelle. → Screening jetzt (S1, S2).
2. **F1** Halving: Daten auf der Box, deskriptiv. → Screening jetzt (S3).
3. F4 Volumen: Daten auf der Box, aber Abgrenzung zu Lane A muss vorher schriftlich fixiert werden.
4. F8 SSR: Daten auf der Box, niedrige Priorität.
5. F7 Ensemble: Daten/Signale vorhanden, aber hohe Vorbelastung.
6. F6 VIX/S&P: FRED-Abruf nötig (einfach).
7. F5 On-Chain-Aktivität: CoinMetrics-Abruf nötig.
8. F3 DVOL: Deribit-Abruf, kurze Historie.

## 4. Screening-Spezifikation S1–S3 (vor dem Rechnen fixiert)
Gemeinsam: Binance Spot 1d bis 2023-12-31, Coins ADA, AVAX, BNB, DOT, LINK, LTC, XRP (ETH und SOL bewusst ausgeschlossen, um sie nicht weiter zu belasten; die 7 Coins sind ein Survivorship-behafteter Proxy für U2). Rendite r_t = close_t / close_(t−1) − 1.
- **S1 (F2, Trial 1):** Signaltag t: BTC-Rendite r_btc,t > 2 × Standardabweichung der BTC-Renditen der 60 Vortage. Messung: mittlere Altcoin-Rendite am Tag t+1 (gleichgewichtet über verfügbare Coins, ein Wert je Datum), minus K1-Roundtrip 0.94 %. Bericht: Mittel, t-Wert, Hälften, je Coin.
- **S2 (F2, Trial 2):** Regression über alle Tage, gepoolt mit Datums-Mittelwerten: r_alt,t+1 = a + b·r_btc,t + c·r_alt,t. Prüft, ob ein systematischer Lead-Lag besteht (b > 0, |t| ≥ 2).
- **S3 (F1, Trial 3):** CoinMetrics PriceUSD 2014-01-01 bis 2023-12-31, Halvings 2016-07-09 und 2020-05-11. Mittlere Tages-Log-Rendite in den 540 Tagen nach einem Halving gegen alle übrigen Tage; zusätzlich Anteil der Tage im Fenster mit MVRV-Zustand INVESTIERT (Regel Linie B). Rein deskriptiv.
