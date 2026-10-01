# XS21 Cross-Sectional Momentum — Point-in-Time-Vorregistrierung, Version 0.1

**Project Aurum II, `01_forschung/09_lane_c/xs21_point_in_time_prereg_v0.1.md`. 18.09.2026. Status: Entwurf zur Prüfung vor dem Freeze, kein Lauf. Zweck: Prüfung der Stufe-2-Hypothese H-C2 (XS21 Long+Short bestanden mit Survivorship-Vorbehalt, Sharpe 1.15, Alpha 46 Prozent, Beta null auf dem Zehn-Coin-Universum) auf einem Universum, das zu jedem Stichtag nur enthält, was damals handelbar war, einschliesslich später delisteter Symbole. Datenbasis: Lane-C-Befund v1 (`binance_um_universe.csv`, SHA f5563c09…, 1014 Symbole, 266 heute nicht mehr TRADING, 81 bis Ende 2023 delistet). Die XS21-Regeln aus der Stufe-2-Vorregistrierung v1 werden wörtlich übernommen, nur das Universum ändert sich. Keine Outcomes berechnet.**

## 1. Hypothese

H-C2 besteht auf dem Point-in-Time-Universum, wenn der Cross-Sectional-Momentum-Effekt nicht von der Auswahl der Überlebenden getragen wurde. Falsifikation: Auf dem vollständigen Universum verschwindet das Alpha oder wird von den delisteten Symbolen (die typischerweise zuerst stark steigen und dann abstürzen) dominiert. Beide Ausgänge sind für Aurum II wertvoll, weil XS21 die einzige Konstruktion ist, die alle Stufe-2-Kriterien bestanden hat.

## 2. Universum, point-in-time

Quelle: Binance USDT-M Perpetuals, Monatsarchiv `data/futures/um/monthly/klines/`, Liste aus dem Lane-C-Loader v1.1. Ein Symbol gehört am Stichtag T (jeder siebte Handelstag, 00:00 UTC, wie Stufe 2) zum Universum, wenn `first_month` ≤ Monat(T), `last_month` ≥ Monat(T), der Vormonat vollständige Tages-Klines hat und der Dollar-Umsatz (`quote_volume`) des Vormonats mindestens 50 Millionen USD beträgt. Die Umsatzschwelle ist die einzige neue Zahl gegenüber Stufe 2, sie ist vor dem Lauf festgelegt und wird nicht variiert. Begründung: Die Stufe-2-Coins hatten 2020 bis 2023 Monatsumsätze über einer Milliarde, die Schwelle 50 Millionen schliesst nur Symbole aus, deren Ausführung auf Kraken unrealistisch wäre. Symbole mit Nicht-ASCII-Namen (4) sind ausgeschlossen. Symbole, die im Laufe eines Haltezeitraums delistet werden, werden zur letzten verfügbaren Tageskerze zum Schluss glattgestellt, mit K2-Slippage, das ist die konservative Annahme.

Startdatum 2020-02-01 (erster Stichtag mit vollständigem Vormonat aus dem Archiv, das 2020-01 beginnt), Discovery bis 2023-12-31, Holdout ab 2024-01-01 nach Manifest-Logik. Erwartete Universumsgrösse je Stichtag: 2020 rund 40 bis 80, 2021 100 bis 150, 2022 150 bis 200, 2023 200 bis 300 Symbole.

## 3. Regeln, wörtlich aus Stufe 2

Alle sieben Handelstage: Unter allen am Stichtag im Universum befindlichen Symbolen mit `ret(21) > 0` werden die drei mit dem höchsten `ret(21)` gleichgewichtet long gehalten; unter denen mit `ret(21) < 0` die drei niedrigsten short, beide Beine mit je halbem Kapital. Weniger als drei geeignete Symbole: Rest in Cash. Kein Gate, kein Stopp, kein Filter. Signale auf Binance-Perp-Tageskerzen (Schluss), Ausführung zur Eröffnung des Folgetages, Kosten K0, K1, K2 wie Stufe 2 (Perp-Modell mit Funding auf beiden Beinen), Cash zum T-Bill-Satz.

Neu und vor dem Lauf festgelegt, weil das Universum jetzt grösser ist: Top-3 bleibt die primäre Konfiguration (Vergleichbarkeit mit Stufe 2). Als vorregistrierte Vergleiche, keine Auswahl: Top-N als Anteil des Universums (oberstes und unterstes Dezil, je gleichgewichtet), weil drei von 250 Symbolen ökonomisch etwas anderes sind als drei von zehn. Jitter wie Stufe 2: L ∈ {42, 63}, Top-N ∈ {2, 4}.

## 4. Kriterien

Die acht Stufe-2-Kriterien für Familie C unverändert (Sharpe, Alpha gegen Equal-Weight-Universum, Beta, Blöcke, Jitter-Nachbarn, K2-Robustheit, Retention, Drawdown). Zusätzlich, weil dies die eigentliche Frage ist: Zerlegung des Ertrags in Beiträge von Symbolen, die am Ende des Discovery-Fensters noch TRADING waren, und Beiträgen der bis dahin delisteten (81 Symbole). Besteht XS21 nur mit den Überlebenden, ist H-C2 falsifiziert. Statuszuweisung nach Regel v2 (Governance v1.1), Evidenzklasse: Holdout validation möglich, weil die Regeln vor Sicht auf das Point-in-Time-Universum eingefroren wurden (Stufe 2 v1) und das Universum nach Handelbarkeit, nicht nach Ergebnis gebildet wird. Economic Validation Gate vor der Validation.

## 5. Datenbeschaffung vor dem Lauf

Tages-Klines aller Universumssymbole ab 2020-01 einschliesslich der delisteten, aus demselben Archiv, mit dem bestehenden Loader (Erweiterung um eine Symbolliste aus `binance_um_universe.csv`, geschätzt 1000 Symbole mal 48 Monate, rund 2 GB), Funding-Historie je Symbol (8h, für die Perp-Kosten), Provenienz mit Prüfsummen. Keine Kraken-Daten nötig, weil XS21 ein Perp-Sleeve ist. Der Loader-Lauf ist ein Mac-Lauf von voraussichtlich ein bis zwei Stunden.

## 6. Offene Entscheidungen vor dem Freeze

1. Umsatzschwelle 50 Millionen USD Vormonat bestätigen.
2. Dezil-Variante als vorregistrierten Vergleich bestätigen oder streichen.
3. Delisting-Glattstellung zur letzten Tageskerze mit K2-Slippage bestätigen.
4. Ob das Short-Bein wie in Stufe 2 mitläuft (H-C3: Absicherung, kein Ertrag) oder Long-only zusätzlich als Vergleich geführt wird.
