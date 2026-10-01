# Datenabdeckung und Datenprüfung, Validierungsstufe MTP, Version 1

**Project Aurum II, 03_mtp_validation. 17.09.2026. Prüfung vor dem Rechenlauf gemäss Vorregistrierung v0.2, Abschnitt 10 und 12. Kein Validierungslauf wurde gestartet.**

## 1. Quellen und Prüfsummen

CoinMarketCap: zehn USD-Tagesreihen über `nachladen_cmc.py`, jede CMC-ID gegen Symbol und Namen aus der API-Antwort geprüft, BTC-Kontrolle der drei Backtester-Schlusskurse bestanden. Kraken: offizielles Archiv `Kraken_OHLCVT_Full_2026Q2.zip` in fünf Teilen, jeder Teil gegen Krakens eigene SHA-256-Liste geprüft, zusammengesetztes Archiv SHA-256 `fc81b54cba6e12af3e9422dde9416179e6ef76af4831d48d839fbdb43018eaa4`, zehn Tagesdateien `<PAIR>USD_1440.csv` extrahiert, alle Kerzen beginnen 00:00 UTC. Kraken-REST-API: 720 Tage je Paar zur Ergänzung ab 01.07.2026. Alle Prüfsummen der Arbeitsdateien in `pruefsummen_daten_v1.txt`.

## 2. Integrität

Alle 30 Dateien: keine Duplikate, keine Kerze mit Hoch unter Tief, Open oder Close ausserhalb der Spanne, keine Nullkurse, keine degenerierten Kraken-Kerzen (Hoch gleich Tief bei Volumen null). CMC: eine Lücke (LINK, 31.07.2022 fehlt), sonst lückenlos. Kraken-Archiv gegen Kraken-API auf der Überlappung (642 Tage je Coin, BNB 435): Open, Hoch, Tief und Schluss identisch auf allen Tagen, Abweichung 0.000 Prozent. Die Naht am 30.06.2026 zwischen Archiv und API ist damit ohne Bruch, die zusammengeführte Reihe liegt in `raw/kraken_merged/`.

## 3. Abdeckung je Coin

| Coin | CMC ab | Kraken ab | Kraken-Lücken (letzte) | Warmup-Ende A | B-Start (Vorschlag) | B-Tage | Tief-Abweichung Kraken zu CMC ab B-Start |
|---|---|---|---|---|---|---|---|
| BTC | 2013-04-28 | 2013-10-06 | 11 (2014-12-26) | 2014-04-28 | 2014-12-26 | 4283 | -0.54 % |
| ETH | 2015-08-07 | 2015-08-07 | 5 (2018-01-13) | 2016-08-06 | 2018-01-13 | 3169 | -0.62 % |
| SOL | 2020-04-10 | 2021-06-17 | 0 | 2021-04-10 | 2021-06-17 | 1918 | -0.38 % |
| XRP | 2013-08-04 | 2017-05-18 | 1 (2018-01-13) | 2014-08-04 | 2018-01-13 | 3169 | -0.76 % |
| ADA | 2017-10-01 | 2018-09-28 | 0 | 2018-10-01 | 2018-10-01 | 2908 | -0.56 % |
| AVAX | 2020-09-22 | 2021-12-21 | 0 | 2021-09-22 | 2021-12-21 | 1731 | -0.38 % |
| LINK | 2017-09-20 | 2019-09-25 | 0 | 2018-09-20 | 2019-09-25 | 2549 | -0.50 % |
| DOT | 2020-08-20 | 2020-08-18 | 0 | 2021-08-20 | 2021-08-20 | 1854 | -0.27 % |
| BNB | 2017-07-25 | 2025-04-22 | 0 | 2018-07-25 | 2025-04-22 | 513 | -0.16 % |
| LTC | 2013-04-28 | 2013-10-24 | 88 (2018-01-13) | 2014-04-28 | 2018-01-13 | 3169 | -0.67 % |

Alle Reihen enden am 16.09.2026 (CMC und Kraken-API). Ebene A läuft je Coin ab Warmup-Ende (365 Tage nach CMC-Beginn, deckt SMA200 und ATR180 ab). Warmup-Ende A ist die Untergrenze für B.

## 4. Befunde, die vor dem Lauf entschieden werden müssen

**Kraken-Frühphase.** BTC 2013 bis 2014 und LTC 2013 bis 2015 haben auf Kraken Lücken bis 16 Tage und Schlusskurse, die im Jahresmittel 2 bis 7 Prozent von CMC abweichen, ETH 2015 über 3 Prozent. Das ist die Illiquidität der frühen Kraken-Märkte, keine Datenfehler. Auf solchen Kerzen würden Stop-Berührungen und Fills nicht die Ausführung messen, sondern das Rauschen einer Börse ohne Tiefe. Zusätzlich hat Kraken am 12. und 13.01.2018 eine 48-Stunden-Wartung, die bei ETH, XRP und LTC als Zwei-Tages-Lücke erscheint (BTC-Archiv führt den Tag).

**Vorschlag B-Start je Coin, rein mechanisch:** der spätere Wert aus Warmup-Ende A und dem ersten Kraken-Tag nach der letzten Lücke. Ergebnis in der Tabelle. Wirkung: BTC ab 2014-12-26, ETH, XRP und LTC ab 2018-01-13, alle übrigen ab Kraken-Beginn. Die Regel ist vor Kenntnis irgendeines Ergebnisses formuliert, braucht keinen Schwellenwert und schneidet genau die Phase ab, in der die Börse nachweislich keine durchgehende Reihe liefert. Als Berichtswert läuft B zusätzlich auf der vollen Überlappung ohne diese Regel, damit sichtbar ist, was die Frühphase geändert hätte.

**Fehlende Tage innerhalb von B.** Nach dem B-Start gibt es keine Kraken-Lücken mehr. Für die eine CMC-Lücke (LINK, 31.07.2022) gilt: Kein CMC-Balken, kein Signal an diesem Tag, ATR und SMA laufen über den vorhandenen Balken weiter, Stop und Ziel werden am nächsten Kraken-Tag geprüft. Dokumentiert, betrifft einen Tag.

**Tief-Abweichung.** Kraken-Tiefs liegen ab B-Start im Mittel 0.16 bis 0.76 Prozent unter den CMC-Tiefs, die Schlusskurse weichen ab 2020 unter 0.3 Prozent ab. Das ist die erwartete Index-Glättung und genau der Effekt, den die Phantom-Stop-Diagnostik (Vorregistrierung Abschnitt 7) misst. Kein Datenproblem, aber der Grund, warum Ebene B nötig ist.

**BNB.** Kraken-Historie 513 Tage ab 22.04.2025. BNB liefert in B höchstens ein bis zwei Trades und wird in Kriterium 2 die Mindestzahl von zehn Trades nicht erreichen. BNB bleibt im Universum (eingefroren), zählt in B faktisch nur als Berichtswert. In A läuft BNB voll ab 2018-07-25.

**BTC als Identifikationsmarkt** ist davon unberührt: A ab 2014-04-28 reproduziert die sechzehn Backtester-Trades, B ab 2014-12-26.

## 5. Was noch fehlt

Nichts auf der Datenseite. Vor dem Lauf braucht es die Bestätigung der B-Start-Regel aus Abschnitt 4 und ihre Protokollierung in ENTSCHEIDE. Danach: Umsetzung `mtp_val.py`, Look-ahead-Test, BTC-Replikationskontrolle (13 von 16), dann ein Volllauf.
