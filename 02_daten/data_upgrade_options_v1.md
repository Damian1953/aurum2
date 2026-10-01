# Datenquellen-Optionen für RTC und Flow-Forschung, Version 1

**Project Aurum II, `02_daten/data_upgrade_options_v1.md`. 17.09.2026. Status: Bewertung, keine Beschaffung. Keine kostenpflichtige Quelle wird gekauft, bevor der Informationsgewinn der kostenlosen oder bereits vorhandenen Ebenen (RTC-0 bis RTC-2) gemessen ist. Angaben zu Abdeckung und Preisen sind Stand der öffentlichen Seiten am 17.09.2026 und vor einer Entscheidung zu verifizieren.**

## 0. Bewertungsraster

Jede Quelle wird nach ihrem Informationsgewinn für fünf Zwecke bewertet: Bottom-Erkennung (Kontext und Bestätigung eines Bodens), Peak-Erkennung (Evidenz eines Endes), Flow-Erschöpfung (aggressiver Fluss kippt), Liquidations-Kapitulation (erzwungene Verkäufer oder Käufer als Marker), realistische Slippage (Ausführung auf Kraken). Dazu Historientiefe, zeitpunktgenaue Verfügbarkeit (point-in-time), Reproduzierbarkeit (Prüfsummen, feste Dateien) und Kosten. Skala: hoch, mittel, gering, keiner.

## 1. Vorhandene und gerade geladene Ebenen (kostenlos)

| Quelle | Inhalt, Historie | Bottom | Peak | Flow | Liquidation | Slippage | Status |
|---|---|---|---|---|---|---|---|
| Binance Vision Spot Klines, alle Spalten, 1d und 4h | OHLCV, Quote-Volumen, Trades, Taker-Buy Base und Quote, ab 2017-08 (BTC), je Listing | hoch (Form, Volumen, Taker-Imbalance) | hoch | hoch | keiner | gering (Binance, nicht Kraken) | wird geladen, `nachladen_4h.py` |
| Binance Vision Perp Klines, alle Spalten | dasselbe auf USDT-M Perpetuals, ab 2019-09 (BTC) | mittel (Perp-Flow) | mittel | hoch (Perp-Taker-Imbalance) | keiner | keiner | wird geladen |
| Binance Funding 8h | ab 2019-09 (BTC), 2020 (übrige) | mittel (Kapitulation) | mittel (Crowding) | mittel | keiner | keiner | vorhanden |
| Binance OI täglich | ab 2021-01 (BTC), 2021-12 (übrige), nur Tagesschnappschuss | gering (Tagesauflösung) | mittel (OI-Expansion ohne Preis) | mittel | keiner | keiner | vorhanden |
| Binance Spot-Perp-Basis | abgeleitet aus Spot- und Perp-Klines, 4h und 1d | gering | mittel (Premium-Extreme) | mittel | keiner | keiner | abgeleitet nach dem Laden |
| Kraken OHLCVT Archiv 2026Q2 plus API | 1 bis 1440 Minuten, alle Paare, ab erstem Handel, Trades-Spalte, kein Taker-Split | mittel (Form, Gegenprobe) | mittel | keiner | keiner | mittel (Kerzen, nicht Ticks) | 1d vorhanden, 240 wird extrahiert |
| Kraken Time-and-Sales (Tick-Trades) | jeder öffentliche Trade je Paar seit erstem Handel bis 30.06.2026, Spalten timestamp, price, volume, type (buy/sell), order_type (limit/market), trade_id, rund 13 Teile zu 2 GB plus Quartals-Updates, kostenlos | hoch (aggressive Marktorders je Seite auf der Ausführungsbörse, ein Taker-Split auf Kraken) | hoch | hoch (Kraken-Flow als zweite Venue) | keiner | hoch (erster handelbarer Preis nach Kerzengrenze exakt, Tiefe des Preissprungs) | nicht geladen, empfohlen als nächste kostenlose Ebene |
| OKX Historical Data | Tick-Trades ab 2021-09, Funding ab 2022-03, L2-Orderbuch ab 2023-03, Kerzen ab 2023-07, Borrowing Rates ab 2021-12, Download über die OKX-Seite, nach deren Angaben ohne Gebühr | mittel (Cross-Venue-Gegenprobe) | mittel | mittel (zweite Perp-Venue für Funding und Flow-Richtung) | keiner (nicht angeboten) | gering | nicht geladen, für Cross-Venue-Bericht ab 2023 |

Die Kraken-Tick-Daten sind die einzige kostenlose Quelle, die zwei Lücken zugleich schliesst: Taker-Richtung auf der Ausführungsbörse (Binance-Taker-Imbalance ist Binance-Flow, nicht Kraken-Flow) und exakte Fills für die Ebene B (erster Trade nach 00:00, 04:00 UTC, statt der Kerzeneröffnung). Kosten: rund 26 GB Download, Verarbeitung auf dem Mac zu 4h-Aggregaten je Paar (Volumen buy und sell, Anzahl Marktorders, erster Trade je Kerze), danach löschbar.

## 2. Kostenpflichtige oder eingeschränkte Quellen

| Quelle | Inhalt, Historie | Bottom | Peak | Flow | Liquidation | Slippage | Kosten, Einschränkung |
|---|---|---|---|---|---|---|---|
| CoinGlass API | aggregierte Long- und Short-Liquidationen je Coin über Börsen, Intervalle 1m bis 1w, Felder time, aggregated_long_liquidation_usd, aggregated_short_liquidation_usd, 1000 Punkte je Anfrage mit Paginierung. Dazu OI- und Funding-Historie über Börsen, Long/Short-Ratios | mittel (Long-Liquidations-Spike als Kapitulationsmarker) | mittel (Short-Squeeze, Buy Climax) | gering | hoch, die einzige bezahlbare Liquidationshistorie mit 4h | keiner | Hobbyist 29 USD je Monat (Intervalle ab 4h, 30 Anfragen je Minute), Startup 79 USD, Standard 299 USD (auch 1h und kürzer). Historientiefe der Liquidationsreihe ist auf der Seite nicht angegeben und muss mit einem Monatsabonnement geprüft werden. Aggregation über Börsen ist point-in-time nur, wenn CoinGlass die Börsenliste nicht rückwirkend geändert hat, das ist nicht dokumentiert |
| Tardis.dev | Rohaufzeichnungen der Websocket-Feeds: Trades, L2-Orderbuch, Liquidationen, Derivative Ticker (OI, Funding, Mark, Index), Book Ticker, Optionen. Binance USDT-M ab 2019-11-17, OKX ab 2019-03-30, Kraken Futures ab 2019-03-30, über 40 Börsen. Tägliche CSV-Dateien je Börse und Symbol, Replay-API in Pro- und Business-Abonnements | hoch (Liquidationen je Trade, Orderbuch-Tiefe am Tief) | hoch | hoch (Trades mit Seite, OI in Sekunden) | hoch, Börsen-eigene Liquidationsfeeds seit 2019 | hoch (L2 auf Kraken Futures und OKX, nicht Kraken Spot) | kostenpflichtig, Preis nach Umfang, nicht pauschal öffentlich. Datenvolumen im Terabyte-Bereich für volle Bücher, Liquidationen und Ticker allein sind klein. Die Websocket-Aufzeichnung enthält Verbindungsabbrüche, deshalb Lückenprüfung nötig |
| Amberdata | Trades, OHLCV, Funding, OI, Liquidationen, volle Orderbuch-Events und Snapshots, Liquiditäts- und Pressure-Metriken, REST und Websocket, für Binance, OKX, Kraken und weitere | hoch | hoch | hoch | hoch | hoch | Enterprise-Preisgestaltung auf Anfrage, keine öffentlichen Tarife. Für ein Einzelprojekt vermutlich die teuerste Option. Vorteil wären abgeleitete Metriken, die Aurum II aber selbst aus Rohdaten rechnen kann und aus Gründen der Reproduzierbarkeit auch soll |
| Binance Vision Metrics, 5 Minuten | OI, OI-Wert, Top-Trader- und Konto-Long/Short-Ratios, Taker-Long/Short-Volumenverhältnis der Perps in 5-Minuten-Auflösung, ab 2021-12 (BTC ab 2021-01), eine Tagesdatei je Symbol und Tag | mittel | mittel | hoch (4h-OI statt Tagesschnappschuss, Taker-Verhältnis der Perps) | keiner | keiner | kostenlos. Der bisherige Loader hat aus diesen Dateien nur die letzte Beobachtung je Tag behalten, die 5-Minuten-Zeilen sind nicht gespeichert. Ein erneuter Lauf mit Aggregation auf 4h ist eine Loader-Erweiterung (rund 1700 Tagesdateien je Coin, langsam, aber ohne Kosten) |

## 3. Einordnung nach Informationsgewinn je Zweck

Bottom-Erkennung: Die grösste Lücke ist nicht die Datenklasse, sondern die Auflösung des OI (Tagesschnappschuss). Die Binance-Metrics-Tagesdateien (5 Minuten) schliessen sie ab 2021-12 ohne Kosten, nach einem erneuten Loader-Lauf mit 4h-Aggregation, `delta_open_interest` kann dann auf 4h berechnet werden. Liquidationen (CoinGlass, Tardis) sind die einzige neue Datenklasse mit plausibel hohem Gewinn, weil sie erzwungene Verkäufer direkt messen, statt sie aus Volumen und Wicks zu erschliessen.

Peak-Erkennung: Funding und OI sind vorhanden. Short-Liquidationen (Buy Climax) sind derselbe Gewinn wie oben. Orderbuch-Daten (Tardis, Amberdata) wären ein weiterer Marker (Ask-Tiefe bricht weg am Hoch), aber erst ab 2019 auf Perps und ohne Kraken Spot, und mit hohem Volumen.

Flow-Erschöpfung: Binance-Taker-Imbalance ist vorhanden. Kraken-Ticks liefern dieselbe Grösse auf der Ausführungsbörse und damit die Frage, ob Flow-Signale marktweit oder venue-spezifisch sind. OKX-Trades ab 2021-09 als dritte Venue.

Liquidations-Kapitulation: nur CoinGlass oder Tardis. CoinGlass ist billig, aggregiert und in der Tiefe unbekannt, Tardis ist teuer, roh und seit 2019.

Realistische Slippage: Kraken-Ticks (kostenlos) sind hier klar die beste Quelle, weil Aurum II auf Kraken Spot ausführt. Tardis und Amberdata haben Kraken Futures, nicht Kraken Spot, im Tick-Format mit Buch.

## 4. Empfohlene Reihenfolge

Erstens: die laufende Ebene (Binance 4h und Vollspalten, Kraken 240) abschliessen und validieren. Zweitens: Binance-Metrics-Tagesdateien erneut laden und zu 4h-OI und 4h-Perp-Taker-Verhältnis aggregieren (Loader-Erweiterung, kostenlos, langsam). Drittens: Kraken Time-and-Sales laden und zu 4h-Aggregaten mit Taker-Seite und erstem Trade je Kerze verarbeiten, kostenlos, rund 26 GB. Viertens: Discovery RTC-0 bis RTC-2 rechnen und den Informationsgewinn je Ebene messen. Fünftens, nur wenn RTC-2 einen Gewinn gegenüber RTC-1 zeigt oder die Bottom-Engine an der Unterscheidung echter und falscher Böden scheitert: ein Monat CoinGlass Hobbyist zur Prüfung der Liquidationstiefe, dann Entscheid über RTC-3. Tardis nur, wenn CoinGlass die Historie nicht bis mindestens 2021 liefert und RTC-3 als Hypothese trägt. Amberdata nicht, solange Rohdaten selbst verarbeitet werden können.

## 5. Anforderungen an jede neue Quelle vor Verwendung

Feste Dateien mit Prüfsumme (keine Live-Abfragen als einzige Quelle), dokumentierter Beginn je Coin, Lückenprüfung, Zeitraster, Überlappungsvergleich mit einer vorhandenen Reihe (Liquidationen gegen Volumen-Spikes, Kraken-Ticks gegen Kraken-Kerzen), point-in-time-Nachweis (keine rückwirkenden Revisionen oder deren Dokumentation), Eintrag in `provenance_*.json`. Eine Quelle, die diese Anforderungen nicht erfüllt, wird nicht verwendet, auch wenn sie bezahlt ist.
