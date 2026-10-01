# ETH und SOL — Hypothesen-Skizzen, Version 0.1 (keine Tests)

**Project Aurum II, `01_forschung/07_eth_sol_specialist/`. 17.09.2026. Status: Skizzen zur Vorbereitung, keine Vorregistrierung, kein Lauf. Priorität nach BTC, XRP, DOT. Beide Coins verwenden ausschliesslich die gemeinsamen Engines (RTC-Stufe-A-Struktur, Breakout-Engine, Derivatives-Library), keine coin-eigenen Regeln. Die Skizzen halten fest, was an ETH und SOL anders ist und welche Hypothese das begründet.**

## ETH

Datenlage: Binance Spot ab 2017-08, Perp ab 2019-11 (Datei ab 2020-01), Funding ab 2019-11, OI ab 2021-12, Kraken ETHUSD 240 ab 2015-08 (209 Lücken in der Frühphase), 1h vollständig. Discovery 2017-08 bis 2023-12 wie BTC, rund 14000 Kerzen. Flow-Library-Ausgabe vorhanden.

Vorbelastung: Stufe 2 hat ETH in allen Familien mitgerechnet (Tagesbasis), MTP-Validierung: ETH in Ebene B positiv (einer von vier Coins). Keine 4h-Tests bisher.

Hypothesen-Skizze: ETH läuft strukturell nahe an BTC (Korrelation der Tagesrenditen über 0.8), deshalb ist die erste Frage nicht «hat ETH einen eigenen Boden», sondern «sind ETH-Böden dieselben Ereignisse wie BTC-Böden». Skizze E-1: identische Stufe-A-Struktur (drei Familien, T0, E-U und E-D, Kontrollen) auf ETH, mit einem zusätzlichen Bericht: Anteil der ETH-Kandidaten, die innerhalb ±6 Kerzen einen BTC-Kandidaten haben, und Erwartung der ETH-Signale mit und ohne gleichzeitigen BTC-Kandidaten (Aufteilung, kein Filter). Skizze E-2: Breakout-Engine auf ETH mit Derivatives-Bestätigung wie DOT-C, weil ETH den tiefsten Perp-Markt nach BTC hat und die Bestätigung dort am besten messbar ist. Skizze E-3 (Lane C): ETH-BTC-Relative-Value als Cross-sectional-Baustein, nicht als Einzelstrategie.

Erwartete Zahl: wie BTC, 90 bis 130 Failed-Breakdown-Kandidaten, 15 bis 25 Double Bottoms.

## SOL

Datenlage: Binance Spot ab 2020-08-11, Perp ab 2020-09-14, Funding ab 2020-09, OI ab 2021-12, Kraken SOLUSD 240 erst ab 2021-06-17, 1h vollständig. Discovery 2020-08 bis 2023-12, rund 7400 Kerzen, Block P1 nur 2020-08 bis 2020-12, Blockregel wie DOT. Kraken-Ausführung erst ab 2021-06 (B-Start-Regel), also Validation-Fenster auf Kraken ab 2024 vollständig, Discovery-Retention nur ab 2021-06.

Vorbelastung: Stufe 2 und MTP-Validierung (SOL in Ebene B positiv, mit 0.91 R XRP vergleichbar). Keine 4h-Tests.

Hypothesen-Skizze: SOL hat die höchste Volatilität und die tiefsten Drawdowns des Universums (2022 minus 95 Prozent) und danach die stärkste Erholung. Skizze S-1: identische Stufe-A-Struktur, mit dem Vermerk, dass der 12-Prozent-Kontext bei SOL-Volatilität sehr häufig erfüllt ist (die volatilitätsnormierte Kontextdefinition ist hier die vorgemerkte Robustheitsdiagnose, nie Baseline). Skizze S-2: Breakout-Engine, weil SOL-Trends 2021 und 2023 bis 2024 lang und sauber waren. Skizze S-3 (Lane C): SOL-Funding war 2021 und 2024 extrem, Funding-Carry-Kandidat für D-CC auf Kraken, sobald Kraken-Funding-Historie reicht.

Erwartete Zahl: 70 bis 110 Failed-Breakdown-Kandidaten auf 3.4 Jahren, Double Bottoms 10 bis 18.

## Reihenfolge

ETH und SOL werden nach dem Freeze und den Discovery-Läufen von XRP und DOT vorregistriert (Version 0.1 der Pläne), mit der dann geltenden Fassung der gemeinsamen Engines. Kein Pooling über Coins vor einem vorregistrierten Cross-Coin-Test.
