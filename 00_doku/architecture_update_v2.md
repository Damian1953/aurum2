# Aurum II — Zielarchitektur, Update Version 2

**Project Aurum II, 17.09.2026. Ersetzt `architecture_update_v1.md` vom selben Tag in den Abschnitten 1, 2, 4 und 7 und ergänzt Abschnitt 8. Datenschicht, Betrieb und Protokoll in `AURUM_II_ARCHITEKTUR_UND_UMSETZUNG_2026-09-15.md` bleiben unverändert. Crypto-only. Keine Multi-Asset-Plattform. Alle Freeze-Urteile bleiben unangetastet.**

## 1. Grundsätze

Aurum II ist ein Portfolio aus unabhängigen Sleeves, von denen jeder seine eigenen Setups erzeugt. Kein Sleeve kennt einen diskreten Regime-Schalter (Stufe 1, verworfen, final). Kontinuierliche Gewichtungen und hierarchischer Zeitebenen-Kontext (Tag als langsamer Kontext ohne Schalter, 4h als Setup, 1h als Bestätigung) sind zulässig, sofern vorregistriert. Ein späterer Portfolio-Layer verteilt Kapital graduell nach nachgewiesenem Edge, Risiko und Korrelation und wird erst gebaut, wenn mindestens zwei Sleeves die Validation bestanden haben.

Jede Hypothese durchläuft zwei Stufen. Die Discovery Stage prüft auf dem Fenster bis 31.12.2023 mit wenigen, vorab fixierten Varianten, ob ein Signal existiert, und erlaubt keine Produktionsfreigabe. Die Validation Stage prüft die aus der Discovery eingefrorene Mechanik einmalig auf dem Holdout ab 01.01.2024, mit Venue-Wechsel, Kostenstress und Multiplizitätskontrolle, und entscheidet allein über einen Sleeve. Ein Forward-Fenster ab dem Freeze ist die dritte Stufe für bestandene Sleeves. Beide Stufen folgen derselben Kette: Vorregistrierung mit Prüfsumme, Datenprüfung mit Prüfsummen und Abdeckung, Look-ahead-Test, ein Lauf, Urteil nach eingefrorenen Kriterien, Hypothesen für den nächsten Schritt. Kein Urteil wird nachträglich umgedeutet, kein Parameter nach Kenntnis eines Ergebnisses geändert.

Methodische Regel (ersetzt die Formulierung «keine Version 2» aus v1): Frühere negative Ergebnisse gelten ausschliesslich für die getestete Kombination aus Marktmechanik, Zeitebene, Signal, Exit und Instrument. Ein negativer Test beendet die eingefrorene Hypothese, nicht den Coin. Verboten ist «negativer Test, Parameter ändern, erneut testen, bis positiv». Zulässig ist «neuer ökonomischer Mechanismus, neue Vorregistrierung, neuer Test», mit offen ausgewiesener Vorbelastung und deren Zählung in der Trial-Zahl. Eine Version 2 derselben Hypothese (Parameter, Ausführung) ist nur nach bestandener Version 1 zulässig.

## 2. Sleeves und Stand

| Sleeve | Instrument | Hypothesen | Stand 17.09.2026 | Nächster Schritt |
|---|---|---|---|---|
| BTC Specialist | Kraken Spot (Long), Perp (Short), Index- und Binance-Signale | BTC-MTP (Referenz, kein Test, kein unberührtes Fenster), BTC-B 4h Volatility Expansion, BTC-RTC | Plan v0.2 | Freeze mit Framework, Discovery |
| XRP Specialist | Binance Perp (Short, Signale), Kraken Spot (Long) | XRP-RTC (primär, Familien CR und FB, Kontrolle E0), XRP-B 4h Breakout mit verschachtelter Bestätigung | Plan v0.3 | 4h-Daten validieren, 1h laden, Freeze, Discovery |
| DOT Specialist | wie XRP | DOT-A 4h Compression Breakout, DOT-C verschachtelt plus Derivate, DOT-RTC | Plan v0.3, Head-to-Head | wie XRP, geringe Basis ausgewiesen |
| Altcoin-Universum | Binance Perp Long+Short | XS21 (Stufe 2 bestanden mit Survivorship-Vorbehalt) | Priorität nach den Spezialisten, nicht gestartet | Point-in-Time-Universum, eigene Vorregistrierung |
| Portfolio-Carry | Kraken Spot long plus Perp short | D-CC (Stufe 2 bestanden mit Datenvorbehalt) | nicht gestartet | Kraken-Funding-Historie, eigene Vorregistrierung |
| BTC Exposure-Steuerung | Kraken Spot | Hypothese aus der MTP-Validierung | nicht definiert | eigene Vorregistrierung |
| Spätere CEP-Sleeves | offen | weitere Familien | nicht definiert | je eigene Vorregistrierung |

Gemeinsame Komponenten aller Spezialisten-Sleeves: Candlestick and Flow Feature Library v0.1, RTC-Framework v0.1, eine Breakout-Engine (Keltner-Kompression, 120-Kerzen-Ausbruch, Chandelier), Halving-Kontextplan v0.1, Visual-AI-Plan v0.1, Datenquellen-Bewertung v1. Definitionen sind coin-übergreifend identisch, die Aussagekraft wird coin-spezifisch validiert.

Reihenfolge der aktiven Arbeit: XRP, DOT und BTC parallel in der Planphase, gemeinsamer Freeze von Framework, Library und den drei Plänen, dann Discovery je Coin, danach XS21 Point-in-Time, D-CC Kraken, BTC-Exposure-Hypothese. Die Reihenfolge ändert sich nur durch Entscheid im Protokoll.

## 3. Was gesichert ist

Unverändert aus v1: Diskrete Regime-Labels sind keine Zustände. Die gespiegelte Long-Ausbruchslogik hat auf der Short-Seite keinen Edge, tägliche Mean Reversion mit festem z-Fenster keinen auf zehn Coins, Time-Series-Momentum ist Marktbeta. Trendfolge mit weitem Stop und Ziel fängt Bullenphasen und sammelt ausserhalb Stops, ab 2022 null. Ausführung auf Kraken kostet wenig, Phantom-Stops treffen die besten Trades, Signale aus Börsenkerzen sind ein anderes System als aus Indexkerzen. Funding-Carry ist auf Kraken-Funding nicht geprüft. Cross-Sectional-Momentum ist die einzige Konstruktion, die alle Kriterien bestanden hat. Für die neuen Sleeves folgt: Long-Seiten auf Spot, Short-Seiten auf Perps, Ausführung Ebene B mit erstem handelbaren Preis der Folgekerze, Kosten K0 bis K2 mit tatsächlichem Funding, Retention als Kriterium, BTC nie als Validierungsmarkt für etwas, das auf BTC entwickelt wurde.

## 4. Datenschicht (Stand)

Vorhanden mit Prüfsummen: Binance Spot und Perp Tageskerzen (OHLCV), Funding 8h, OI täglich, Kraken Spot Tageskerzen (Archiv plus API), Kraken Funding stündlich ab 2025-09 (drei Coins), CMC, T-Bill. Wird geladen (17.09.2026): Binance Spot und Perp 4h und 1d mit allen Spalten, Kraken 240 aus dem Archiv. Danach zu laden: Binance Spot und Perp 1h, Kraken 60, Binance-Metrics-Aggregation zu 4h-OI, OKX-Kerzen ab 2023-07, Kraken Time-and-Sales (kostenlos, für Kraken-Taker-Seite und exakte Fills). Nicht verfügbar ohne Kauf: Liquidationen (CoinGlass, Tardis), bewertet in `data_upgrade_options_v1.md`, keine Beschaffung vor dem Nachweis des Informationsgewinns der kostenlosen Ebenen. Binance ist der primäre Flow- und Derivate-Feed, Kraken die Ausführungs- und Realitätsprüfung, OKX die Cross-Venue-Gegenprobe. Jede neue Reihe wird vor Verwendung mit Lückenprüfung, Raster, Überlappungsvergleich und Prüfsumme dokumentiert. DOGE ist als elfter Coin der Feature Library vorgesehen, aber nicht geladen, Entscheid offen.

## 5. Ausführungsschicht (unverändert)

Kraken Spot für Long-Seiten, Kraken Perpetuals für Short-Seiten und Carry, Signale je Sleeve auf der vorregistrierten Quelle. Signal am Kerzenschluss, Fill zum ersten handelbaren Preis nach der Kerzengrenze, Stops als ruhende Stop-Market-Orders, Ziele als Limit, Slippage nach Kostenszenario. Kein Same-Day-Close-Fill, keine Intrabar-Annahme mit OHLC-Daten.

## 6. Portfolio-Layer (später, unverändert)

Wie v1: erst nach zwei bestandenen Sleeves, jeder Sleeve liefert täglich Zielexposure, R-Verteilung und Exposure-Pfad, Gewichtung nach Edge, Risiko und Korrelation, kontinuierlich, selbst vorregistriert.

## 7. Zwei unabhängige Analysepfade

Regelbasiert ist die Primary Engine: deterministische Candle-, Geometrie-, Niveau- und Flow-Merkmale, deterministische Entry-, Hold- und Exit-Regeln, identisches Signal bei identischen Daten, vollständig backtestbar und auditierbar. Sie ist für Forschung, Validierung und spätere Ausführung allein massgebend.

Visual AI ist ein späterer, getrennter Pfad, der standardisierte Chart-Ausschnitte mit einem eingefrorenen multimodalen Modell bewertet und Wahrscheinlichkeiten liefert (Bottom, Fortsetzung, Peak, Failed Breakdown oder Breakout, Muster-Konfidenz). Er erhält keine regelbasierten Merkmale, erzeugt kein Signal, überschreibt keines und beeinflusst keine Order, bevor sein inkrementeller Informationswert unabhängig validiert ist (Plan v0.1: drei Arme, Redundanzprüfung, Forward-Pflicht). Prompt, Chartformat, Lookback und Modellversion werden vor jedem Test eingefroren, keine Modellwahl nach P&L.

## 8. Was nicht gebaut wird

Keine Multi-Asset-Erweiterung. Keine diskreten Regime-Filter. Keine Variantenmatrizen über verworfene Konstruktionen. Keine Parametervariante einer gescheiterten Hypothese. Kein Sleeve, der seine Parameter aus dem Ergebnis eines anderen Sleeves bezieht. Kein Live- oder Paper-Betrieb eines Sleeves, der die Validation nicht bestanden hat. Kein 15-Minuten-Primary-Trading. Keine Halving-Schwelle als Signal. Keine Visual-AI-Orderentscheidung.
