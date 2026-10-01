# CoinGlass — Abdeckungsprüfung vor dem Kauf, Version 1

**Project Aurum II, `02_daten/coinglass_abdeckungspruefung_v1.md`. 18.09.2026. Prüfung aus der öffentlichen Dokumentation, ohne Kauf, ohne API-Schlüssel. Ergebnis: Der 79-USD-Plan ist für den D-CC-Zweck nicht ausreichend belegt, Kauf zurückgestellt.**

## 1. Was D-CC braucht

Kraken-Futures-Funding je Symbol (mindestens PF_XBTUSD, PF_ETHUSD, PF_XRPUSD, PF_DOTUSD, PF_SOLUSD und die übrigen fünf D-CC-Coins) als Settlement-Reihe oder mindestens 8h-Aggregat, von Kontraktbeginn (PF-Kontrakte 2021 bis 2022, PI-Kontrakte 2018 bis 2019) bis 2025-09, damit die Kraken-Vorzeichen- und Höhenübereinstimmung mit Binance über mehr als ein Jahr geprüft werden kann. Der kostenlose Kraken-Endpunkt liefert nur das rollende Jahr ab 2025-09-17.

## 2. Was die CoinGlass-Dokumentation belegt

Endpunkt `/api/futures/funding-rate/history` mit Parametern exchange, symbol, interval (1h, 4h, 8h, 1d), limit bis 1000, start_time, end_time. Kraken ist auf der Preisseite als unterstützte Futures-Börse gelistet, die Dokumentation des Endpunkts nennt als Beispiele nur Binance und OKX, die Liste der Börsen je Endpunkt ist erst mit Schlüssel abrufbar (`/api/futures/supported-exchange-pairs`, `/api/futures/funding-rate/exchange-list`). Ob Kraken-Futures-Symbole im Funding-History-Endpunkt verfügbar sind, ist damit nicht belegt.

Historische Tiefe nach Plan und Intervall (Preisseite): Hobbyist 29 USD: 4h 180 Tage, 6h und 12h 360 Tage, 1d unbegrenzt, kein 1h. Startup 79 USD: 1h 180 Tage, 4h 180 Tage, 6h und 12h 360 Tage, 1d unbegrenzt. Standard 299 USD: 1h und 4h 360 Tage, 1d unbegrenzt. Professional 699 USD: 1h und 4h 720 Tage. Nur das Tagesintervall reicht in allen Plänen «all-time» zurück.

## 3. Bewertung

Der Startup-Plan liefert für 8h-nahe Intervalle höchstens 360 Tage, also nicht mehr als der kostenlose Kraken-Endpunkt bereits liefert. Die einzige Verlängerung über 2025-09 hinaus ist das Tagesintervall (Funding als Tages-OHLC oder Tagesaggregat). Für D-CC ist ein Tagesaggregat brauchbar, weil die Einschaltschwelle auf einem 7-Tage-Fenster (`f_7d`) definiert ist und das Vorzeichen des Funding auf Tagesbasis erhalten bleibt, aber die Settlement-genaue Buchung (Stufe 2 buchte je Settlement) ist damit nicht reproduzierbar, und die Tiefe des Kraken-Tagesintervalls ist nicht dokumentiert («all-time» bezieht sich auf die Datenbank, nicht auf jede Börse).

Zwei Bedingungen sind vor einem Kauf offen: Erstens, ob Kraken im Funding-History-Endpunkt überhaupt als exchange akzeptiert wird. Zweitens, wie weit das Kraken-Tagesintervall tatsächlich zurückreicht. Beides ist nur mit einem Schlüssel prüfbar.

## 4. Empfehlung

Kein Kauf jetzt. Zwei kostenlose Schritte davor: Anfrage an den CoinGlass-Support mit der konkreten Frage (Kraken PF_XBTUSD im Funding-History-Endpunkt, Tiefe des 1d-Intervalls), und Prüfung, ob der Hobbyist-Plan (29 USD) für einen Testmonat genügt, weil er dasselbe Tagesintervall «all-time» enthält wie Startup, der Unterschied betrifft nur Intervalle unter 4h, die D-CC nicht braucht. Falls die Antwort Kraken und Tiefe ab 2021 bestätigt, ist der Hobbyist-Plan für einen Monat die günstigere Wahl (29 statt 79 USD). Falls Kraken nicht enthalten ist, entfällt CoinGlass, und die D-CC-Kraken-Validation bleibt auf den rollenden Endpunkt angewiesen, mit dem ersten verwertbaren Zweijahresfenster im September 2027. Die monatliche Sicherung des kostenlosen Endpunkts läuft unabhängig davon weiter.
