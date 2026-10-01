# XRP Specialist — Vorregistrierungsplan, Version 0.4

**Project Aurum II, Forschungsstrang 04_xrp_specialist. 17.09.2026. Status: Plan zur Prüfung vor dem Freeze, kein Lauf. Ersetzt Version 0.3. Übernimmt die Stufe-A-Struktur aus BTC YAMATO (drei primäre Bottom-Hypothesen, gematchte Kontrollgruppe, einheitliche Exit-Baseline, drei Discovery-Ebenen, Fast Fail und Fast Promote) und die Lehren aus dem BTC-Lauf, ohne dessen Zahlen zu ändern. Setzt RTC-Framework v0.1, Feature Library v0.1, Derivatives-Library v0.1 und Auswertungsregeln v1 voraus.**

## 0. Was sich gegenüber v0.3 ändert und warum

Der BTC-Stufe-A-Lauf hat gezeigt: Die TA-Bestätigung kostet drei Viertel der Kandidaten und verbessert die Signale nicht gegenüber Kontext-Kontrollen, der Chandelier 3 ATR14 auf 4h beendet Positionen im Median nach 12 bis 15 Kerzen, und die Basisrate von Bounces nach Selloffs ist negativ. XRP v0.4 zieht daraus keine Parameteränderung an den eingefrorenen BTC-Regeln, sondern drei Konsequenzen für die eigene Vorregistrierung, die vor dem XRP-Lauf und ohne XRP-Outcomes gesetzt werden: Erstens läuft die Trigger-Frage (T0, TA, TB) von Anfang an als Familie mit, statt TA allein als Baseline zu setzen, weil die Kandidatenzahl sonst wieder unter die Mindestzahl fällt. Zweitens laufen zwei Exit-Baselines gleichrangig (E-U 4h und E-D auf Tages-ATR), damit die Frage des Exit-Horizonts nicht erst in einer Stufe B gestellt wird. Drittens ist die Kontrollgruppe von Anfang an Teil des primären Tests.

Das erhöht die Zahl der Konfigurationen. Die Multiplizität wird deshalb strikt hierarchisch geführt (Abschnitt 6): Der primäre Test je Hypothese ist eine vorab benannte Konfiguration (T0, E-U), alles andere sind vorregistrierte Vergleiche innerhalb der Hypothese. XRP-B (Breakout) und die Derivatives-Bestätigung bleiben wie v0.3.

## 1. Primäre Hypothese XRP-RTC, drei Bottom-Familien (Stufe A, wie BTC)

Kontext K1 bis K3 unverändert (12 Prozent unter 20-Tage-Hoch, 2 ATR unter EMA50 in sechs Kerzen, innerhalb 1 ATR eines Niveaus oder an der Low-Struktur). X1 Failed Breakdown (Y1-Definition), X2 Double Bottom mit Nackenlinienbruch (Y2-Definition, ohne 3-ATR-Grenze wie v1.1), X3 Lower-Wick plus Volume Climax (Y3-Definition, Volumen-z 1.5). Alle Zahlen identisch mit dem BTC-Parameterpaket v1.1, keine XRP-Anpassung. Trigger: T0 als primär (Einstieg Eröffnung t+1), TA und TB als vorregistrierte Vergleiche (X2: Nackenlinienbruch ist der Trigger). Stop wie BTC. Exit: E-U primär, E-D (Chandelier 3 auf Tages-ATR14 mit Tages-Swing-Strukturbruch) als vorregistrierter Vergleich. Kontrollgruppe wie BTC (drei gematchte Kontrollen, ±90 Tage, dd120 ±3 Punkte, ext ±0.5 ATR, gleicher Trigger und Exit, Referenz s2 für X2).

Flow-Inkremente aus der Derivatives-Library, inkrementell und verschachtelt: RTC-1 (Volumen-z ≥ 1, Taker-Imbalance ≥ 0, Flow-Wechsel ≥ 0.10), RTC-2 (Funding-z ≤ −1 oder ΔOI ≤ −10 Prozent), als Teilmengentests. Follow-through-Diagnose (Preis, Taker, Volumen über 1, 3, 6 Kerzen) für alle Signale und Kontrollen.

Kontrollarchitektur E0 (Exit am EMA20 oder nach 30 Kerzen) bleibt als gepaarter Vergleich, weil XRP die Frage «Reversion oder Trend Capture» stellt.

## 2. XRP-B, 4h Volatility Breakout, und XRP-B+ (unverändert aus v0.3)

Keltner-Kompression, 120-Kerzen-Ausbruch, Chandelier 3 ATR20, Long und Short. XRP-B+ verschachtelt: ΔOI ≥ +10 Prozent, Taker-Imbalance ≥ +0.10, Funding-z ≤ +1.5. Gepaarter Teilmengentest ab 2021-12.

## 3. Daten und Fenster

Vorhanden und validiert: Binance Spot und Perp 4h und 1h mit allen Spalten (Spot ab 2018-05-04, Perp ab 2020-01-06), Funding ab 2020-01, OI ab 2021-12, Kraken 240 ab 2017-05, Flow-Library-Ausgabe `XRPUSDT_flow_4h.csv` mit Abdeckungstabelle. Discovery 2018-05 bis 2023-12 (rund 12300 Kerzen), Holdout ab 2024 (mit dem bekannten Vermerk zur Expansion ab November 2024). Vorlauf 134 Kerzen.

## 4. Erwartete Zahlen (Schätzung aus BTC-Zählung, skaliert auf XRP-Volatilität, ohne XRP-Daten gesehen zu haben)

XRP hat häufigere 12-Prozent-Rückgänge als BTC. Erwartet: X1 100 bis 160 Kandidaten, mit T0 rund 70 bis 110 Trades, mit TA 25 bis 40. X2 15 bis 25. X3 30 bis 50 Kandidaten, T0 20 bis 40 Trades. Damit ist T0 auf X1 die einzige Konfiguration, die die Mindestzahl 30 sicher erreicht. Die Zählung nach dem Freeze wird das prüfen.

## 5. Kriterien und Status

Discovery-Kriterium «Signal vorhanden», die drei Ebenen (formal supported, mechanistically promising, no evidence mit inconclusive und Fast Fail) und Fast Promote wörtlich nach Auswertungsregeln v1, Mindestzahl 30, Stufung 20, gepaarte Differenzen gegen Kontrollen mit Bootstrap-Intervallen. Validation auf dem Holdout ab 2024 mit Kraken-Ausführung (XRPUSD 240) und Kostenstress, die neun Kriterien aus v0.1.

## 6. Tests und Multiplizität

Primäre Familie (Holm über drei): X1, X2, X3 je mit T0 (X2 Nackenlinie) und E-U gegen gematchte Kontrollen. Trigger-Familie (Holm über vier): TA gegen T0 und TB gegen T0 auf X1 und X3, Erwartung je Kandidat. Exit-Familie (Holm über drei): E-D gegen E-U auf X1, X2, X3. Kontrollarchitektur (ein Test): E0 gegen E-U auf der Vereinigung. Inkremente (Holm über zwei): RTC-1, RTC-2. Breakout-Familie (Holm über drei): B-L, B-S, B+ gegen B. Trial-Zahl: 16 plus Jitter plus Vorbelastung XRP (27). Keine Auswahl einer Konfiguration nach Ergebnis, die Konfigurationsregel für die Validation ist vorab: primäre Konfiguration, es sei denn, ein vorregistrierter Vergleich ist innerhalb seiner Familie nach Holm positiv und die Basiskonfiguration nicht.

## 7. Produktionsvermerk (Bericht je Konfiguration)

Trades je Jahr, Turnover, Maker- und Taker-Anteil (Eröffnungs-Market-Orders sind Taker, eine Maker-Variante mit Limit an der Eröffnung ist eine spätere Execution-Hypothese), Datenlatenz 4h-Schluss, Instrument Kraken Spot (Long) und Perp (Short), Funding auf Perp-Seiten, Slippage K1, maximale Positionsdauer, API-Daten OHLCV 4h plus Binance-Flow, Komplexität niedrig für Spot-Long, mittel für Perp-Short.

## 8. Offene Entscheidungen vor dem Freeze

1. T0 als primärer Trigger für XRP (Empfehlung, wegen Mindestzahl und BTC-Befund) oder TA wie BTC-Stufe A (dann Vergleichbarkeit, aber deskriptive Auswertung wahrscheinlich).
2. E-D als zweite Exit-Baseline mitführen (Empfehlung) bestätigen.
3. Kontrollgruppen-Toleranzen wie BTC bestätigen.
4. Trial-Zahl 16 bestätigen.
5. Framework- und Library-Entscheidungen gelten weiter.

Nach Klärung: Version 1.0, Prüfsumme in ENTSCHEIDE, Umsetzung auf der BTC-Library (identischer Code, Coin-Parameter nur Dateipfad), Look-ahead-Test, Zählung, Matching-Abdeckung, ein Discovery-Lauf.
