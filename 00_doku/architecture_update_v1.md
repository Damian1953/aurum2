# Aurum II — Zielarchitektur, Update Version 1

**Project Aurum II, 17.09.2026. Ersetzt den Abschnitt Strategiearchitektur in `AURUM_II_ARCHITEKTUR_UND_UMSETZUNG_2026-09-15.md`, lässt Datenschicht, Betrieb und Protokoll dort unverändert. Crypto-only. Keine Multi-Asset-Plattform.**

## 1. Grundsätze

Aurum II ist ein Portfolio aus unabhängigen Sleeves, von denen jeder seine eigenen Setups erzeugt. Kein Sleeve kennt einen diskreten Regime-Schalter (Stufe 1, verworfen, final). Kontinuierliche Gewichtungen innerhalb eines Sleeves (etwa der ER-basierte Hybrid bei XRP) sind zulässig, sofern sie vorregistriert sind. Ein späterer Portfolio-Layer verteilt Kapital graduell nach nachgewiesenem Edge, Risiko und Korrelation. Er wird erst gebaut, wenn mindestens zwei Sleeves die eingefrorenen Kriterien bestanden haben.

Jeder Sleeve durchläuft dieselbe Kette: Vorregistrierung mit Prüfsumme, Datenprüfung mit Prüfsummen und Abdeckung, Look-ahead-Test, ein Volllauf, Urteil nach eingefrorenen Kriterien, Hypothesen für den nächsten Schritt. Kein Urteil wird nachträglich umgedeutet. Kein Parameter wird nach Kenntnis eines Ergebnisses geändert. Eine Version 2 eines Sleeves ist nur zulässig, wenn Version 1 bestanden hat, und dann für Parameter und Ausführung, nicht für die Rettung eines verworfenen Signals.

## 2. Sleeves und Stand

| Sleeve | Instrument | Kandidat | Stand 17.09.2026 | Nächster Schritt |
|---|---|---|---|---|
| BTC Trend | Kraken Spot (Long), Index-Signale | MTP-Spezifikation v1 (rekonstruiert, eingefroren) | Validierung verworfen: auf Kraken ab 2018 keine Kriterien erfüllt, auf Index nur 1 bis 4, kein Alpha gegenüber exposure-gleicher Passivposition, Ertrag konzentriert bis 2021 | «Weiter untersuchen» heisst: neue Hypothese, keine Variante. Kandidat ist eine Exposure-Steuerung, die Bullenphasen fängt, statt Alpha je Trade zu suchen. Braucht eigene Vorregistrierung. Kein Forward-Test der Spezifikation v1. |
| XRP Specialist | Binance Perp (Short, Signale), Kraken Spot (Long) | XRP-A Mean Reversion 4h, XRP-B Volatility Breakout, XRP-C kontinuierlicher Hybrid | Plan v0.1, neun offene Entscheidungen | 4h-Daten laden, Freeze, deskriptive Vorprüfung, ein Volllauf |
| DOT Specialist | wie XRP | DOT-A Volatility Breakout, DOT-B Reversion, DOT-C perp-bestätigter Breakout | Plan v0.1, Head-to-Head-Design, neun offene Entscheidungen | Daten mit allen Spalten laden, Freeze, ein Volllauf. Tägliche Trendfolge auf DOT dreimal gescheitert, Freiheitsgrade eng |
| Altcoin-Universum | Binance Perp Long+Short | XS21 Cross-Sectional Momentum (Stufe 2 bestanden mit Survivorship-Vorbehalt) | Priorität 2 in der Reihenfolge, nicht gestartet | Point-in-Time-Universum mit delisteten Coins, eigene Vorregistrierung |
| Portfolio-Carry | Kraken Spot long plus Perp short | D-CC Cash-and-Carry (Stufe 2 bestanden mit Datenvorbehalt Kraken-Funding) | Priorität 3, nicht gestartet | Kraken-Funding-Historie über mehr als ein Jahr, Kapital- und Margin-Modell, eigene Vorregistrierung |
| Spätere CEP-Sleeves | offen | weitere Crypto-Edge-Pro-Familien | nicht definiert | erst nach Abschluss der obigen, je mit eigener Vorregistrierung |

Reihenfolge der aktiven Arbeit: XRP und DOT (neu eröffnet, parallel in der Planphase), danach XS21 Point-in-Time, danach D-CC Kraken, danach BTC-Exposure-Hypothese. Die Reihenfolge ändert sich nicht nach Ergebnissen, sondern nur durch Entscheid im Protokoll.

## 3. Was gesichert ist (aus den bisherigen Stufen)

Diskrete Regime-Labels auf Tagesdaten sind keine Zustände (Stufe 1). Die gespiegelte Long-Ausbruchslogik hat auf der Short-Seite keinen Edge, tägliche Mean Reversion mit festem z-Fenster keinen auf zehn Coins, Time-Series-Momentum ist Marktbeta (Stufe 2). Trendfolge mit weitem Stop und Ziel fängt Bullenphasen über viele Coins gleichzeitig und sammelt ausserhalb davon Stops, der Ertrag ist ab 2022 auf allen Coins null und davor nicht vom Marktbeta zu trennen (MTP-Validierung). Die Ausführung auf Kraken kostet gegenüber Index-Signalen wenig (rund 0.05 R je Trade), Phantom-Stops sind selten, treffen aber die besten Trades, und Signale aus Börsenkerzen sind ein anderes System als Signale aus Indexkerzen (Wilder-ATR 20 Prozent höher). Funding-Carry ist eine Regime-Ernte, die auf Kraken-Funding nicht geprüft ist. Cross-Sectional-Momentum ist die einzige Konstruktion, die alle Kriterien bestanden hat, und die einzige, bei der Survivorship das Ergebnis dominieren kann.

Für die neuen Sleeves folgt daraus: Long-Seiten auf Spot, Short-Seiten auf Perps, Ausführung immer als Ebene B mit erstem handelbaren Preis der Folgekerze, Kosten K0 bis K2 mit tatsächlichem Funding, Retention als Kriterium, BTC nie als Validierungsmarkt für etwas, das auf BTC entwickelt wurde.

## 4. Datenschicht (Stand)

Vorhanden mit Prüfsummen: Binance Spot und Perp Tageskerzen (OHLCV, zehn Coins), Binance Funding 8h ab 2020, Binance OI täglich ab 2021 (BTC) und 2021-12 (übrige), Kraken Spot Tageskerzen aus dem Archiv 2026Q2 mit API-Ergänzung (zehn Coins), Kraken Funding stündlich ab 2025-09 (drei Coins), CoinMarketCap Tageskerzen (zehn Coins), T-Bill. Fehlend für die neuen Sleeves: 4h-Kerzen (Binance Spot und Perp, Kraken 240 Minuten aus dem vorhandenen Archiv), Binance-Klines mit allen Spalten (Taker-Volumen, Anzahl Trades), Basis als abgeleitete Reihe. Nicht verfügbar und deshalb ausgeschlossen: Liquidationshistorie, Orderbuch-Imbalance. Jede neue Reihe wird vor Verwendung mit Lückenprüfung, Tagesraster, Überlappungsvergleich und Prüfsumme dokumentiert.

## 5. Ausführungsschicht (unverändert, präzisiert)

Kraken Spot für Long-Seiten, Kraken Perpetuals für Short-Seiten und Carry, Signale je Sleeve auf der in der Vorregistrierung festgelegten Quelle. Fill-Konvention: Signal am Kerzenschluss, Fill zum ersten handelbaren Preis nach der Kerzengrenze, Stops als ruhende Stop-Market-Orders am Niveau, Ziele als Limit. Slippage nach Kostenszenario. Kein Same-Day-Close-Fill in irgendeinem Sleeve.

## 6. Portfolio-Layer (später)

Wird erst entworfen, wenn zwei Sleeves bestanden haben. Grundzüge, die jetzt festgehalten werden, damit die Sleeves kompatibel bleiben: Jeder Sleeve liefert täglich eine Zielexposure je Instrument zwischen minus 1 und plus 1 des Sleeve-Kapitals, seine realisierte R-Verteilung und seinen Exposure-Pfad. Der Layer gewichtet Sleeves nach Edge (Erwartung je Risiko aus der Validierung, nicht aus dem laufenden Betrieb), Risiko (Volatilität und Drawdown des Sleeves) und Korrelation der Sleeve-Renditen, kontinuierlich, ohne Schalter. Die Gewichtung wird selbst vorregistriert und auf den Validierungsergebnissen der Sleeves geprüft, nicht auf neuen Daten der Sleeves.

## 7. Was nicht gebaut wird

Keine Multi-Asset-Erweiterung. Keine diskreten Regime-Filter. Keine Variantenmatrizen über verworfene Konstruktionen. Kein Sleeve, der seine Parameter aus dem Ergebnis eines anderen Sleeves bezieht. Kein Live- oder Paper-Betrieb eines Sleeves, der die Validierung nicht bestanden hat.
