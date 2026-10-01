# MTP Reverse Engineering — Bericht Stufe 1

**Project Aurum II, 03_woo_mtp_reverse_engineering. Rechenlauf vom 16.09.2026 auf Plan Version 1.1. Datenbasis: CoinMarketCap BTC/USD Tageskerzen 2013-04-28 bis 2026-09-15 (4889 Tage), dazu Bitstamp (ab 2011), Coinbase (ab 2015), Binance (ab 2017) als Gegenproben. Sechzehn beobachtete BTC-Trades aus dem öffentlichen Backtester (Ebene A).**

Erfolgsmass ist Reproduktionsgenauigkeit. Keine Performancekennzahl wurde berechnet. Kürzel: [A] beobachtet, [B] rekonstruiert, [C] spekulativ. Stufe 2 ist unberührt.

## 1. Ergebnis in einem Satz

Die Exit-Mechanik von Market Trend Pro ist rekonstruiert: Der Backtester rechnet auf CoinMarketCap-Tageskursen, steigt zum Schlusskurs des Signaltages ein, setzt den Stop auf «Schluss des letzten Legs minus 6.5 mal Wilder-ATR(180) am Leg-Tag» und das Ziel auf «Schluss des ersten Legs plus 37.5 mal Wilder-ATR(180) am Einstiegstag», beide intraday am Niveau ausgeführt. Damit sind 10 von 16 Exit-Preisen auf 0.05 Prozent genau reproduziert, alle sechs übrigen auf 0.6 bis 5 Prozent, und für 13 von 16 Trades fallen Entry-Tag und Exit-Tag mit der Vollsimulation exakt zusammen. Die Entry-Definition (Pivot-Hoch mit Alter 20 bis 365 Tage) ist stark vereinbar, aber in zwei Fällen noch nicht eindeutig. Die Stufe-2-Matrix hat dieses System in vier Punkten nicht abgebildet.

## 2. Datenquelle und Ausführung (Stufe A)

| Trade | Entry | Ø Entry [A] | Bitstamp Close | Coinbase Close | Binance Close | CMC Close | Treffer |
|---|---|---|---|---|---|---|---|
| 4 | 2017-02-24 | 1173.68 | 1180.14 (-0.55 %) | 1186.91 (-1.11 %) | – | **1173.68** | exakt |
| 5 | 2017-04-26 | 1281.08 | 1287.99 (-0.54 %) | 1298.44 (-1.34 %) | – | **1281.08** | exakt |
| 11 | 2021-04-13 | 63503.46 | 63564.48 (-0.10 %) | 63588.22 (-0.13 %) | 63575.00 (-0.11 %) | **63503.46** | exakt |
| 15 | 2025-01-20 | 102016.66 | 102141.00 (-0.12 %) | 102145.43 (-0.13 %) | 102260.01 (-0.24 %) | **102016.66** | exakt |

Die drei Ein-Leg-Einstiege sind auf den Rappen die CoinMarketCap-Tagesschlusskurse (UTC-Tag). Open, High, Low und Folge-Open jeder Börse scheiden aus (Abweichungen 0.7 bis 7 Prozent). Trade 11 (13.04.2021, 63503.46) ist zusätzlich unabhängig über eine zweite Quelle bestätigt.

**H-D1 Preisquelle CoinMarketCap: bestätigt [B].** **H-D2 Einstieg zum Schluss des Signaltages: bestätigt [B].** Zeitzone UTC, keine Verschiebung nötig (H-Z nicht eröffnet).

Datenvorbehalt: Die heutige CMC-Historie 2015 und 2016 weicht offenbar von der Fassung ab, die der Backtester verwendet hat (Abschnitt 4, Trades 1 bis 3). Ab 2017 gibt es keine Abweichung.

## 3. Exit-Ausführung (Stufe B)

Alle 16 Exit-Preise liegen innerhalb der Tagesspanne des Exit-Tages auf CMC-Daten, kein einziger entspricht Open, Close oder Folge-Open (Abweichung zum Close 0.2 bis 7 Prozent). Alle acht Verlierer enden an Abwärtstagen, sieben der acht Gewinner an Aufwärtstagen. **H-X4 Exit intraday am berechneten Niveau: bestätigt [B].** Alternativen Close-Exit und Folge-Open: widerlegt.

## 4. Stop und Take Profit (Stufen C bis E)

ATR(180) wurde in drei Varianten geprüft: einfacher Durchschnitt der True Range, Wilder-Glättung (RMA, alpha 1/180), exponentiell (span 180). Nur Wilder passt.

**Ein-Leg-Trades, initialer Stop = Einstieg minus 6.5 mal Wilder-ATR(180) am Einstiegstag:**

| Trade | Entry | ATRw | ATR/Kurs | Stop-Niveau | Exit [A] | Abweichung | Exit-Tag |
|---|---|---|---|---|---|---|---|
| 4 | 1173.68 | 21.62 | 1.84 % | 1033.17 | 1033.60 | -0.04 % | Treffer |
| 11 | 63503.46 | 1710.71 | 2.69 % | 52383.8 | 52383.82 | 0.00 % | Treffer |
| 15 | 102016.66 | 2792.02 | 2.74 % | 83868.5 | 83891.32 | -0.03 % | Treffer |

Das Cluster der Verluste bei -16 bis -19 Prozent ist damit erklärt: 6.5 mal ein Wilder-ATR von 2.5 bis 2.9 Prozent des Kurses. Der Stop wird nicht nachgezogen (Trade 15: höchster Schluss nach Einstieg 106146, ein nachgezogener Stop hätte bei 87 000 oder höher gelegen). **H-SL1 bestätigt [B]. H-SL2 Trailing auf Kurs: widerlegt. H-SL3 ATR fixiert am Leg-Tag: bestätigt [B].**

**Mehr-Leg-Trades, Stop = Schluss des letzten Legs minus 6.5 mal Wilder-ATR(180) am Leg-Tag.** Für jeden Verlierer wurde der Tag gesucht, an dem Close minus 6.5 ATRw dem Exit entspricht:

| Trade | Legs | letzter Leg (rekonstruiert) | Close Leg | Stop-Niveau | Exit [A] | Abweichung |
|---|---|---|---|---|---|---|
| 8 | 2 | 2020-02-09 | 10116.67 | 7954.19 | 7953.95 | +0.003 % |
| 10 | 2 | 2021-03-13 | 61243.08 | 51361.75 | 51361.73 | 0.000 % |
| 12 | 3 | 2021-10-20 | 65992.84 | 50806.03 | 50806.03 | 0.000 % |
| 13 | 8 | 2024-01-02 | 44957.97 | 38569.81 | 38570.93 | -0.003 % |
| 16 | 7 | 2025-10-05 | 123513.47 | 104765.02 | 104770.44 | -0.005 % |
| 1 | 2 | 2015-07-12 (?) | 310.87 | 220.94 | 232.77 | -5.1 % |
| 2 | 6 | 2015-11-04 (?) | 411.56 | 334.01 | 340.24 | -1.8 % |

Trade 13 ist ein Stop-Exit, obwohl er mit plus 29 Prozent endet, weil der letzte Leg weit über dem Durchschnittseinstieg lag. **H-SL4 Stop wird bei jedem Add-on auf den neuen Leg gesetzt: bestätigt [B]** (fünf von fünf Trades ab 2017 auf 0.005 Prozent). Der Schalter «Only Pyramid When SL > New Avg Entry» ist damit verständlich: Nach einem Add-on liegt der Stop bei «letzter Leg minus 6.5 ATR» und kann über oder unter dem neuen Durchschnittseinstieg liegen.

**Take Profit = Schluss des ersten Legs plus 37.5 mal Wilder-ATR(180) am Einstiegstag, fix für den ganzen Trade:**

| Trade | Legs | Entry-Close | ATRw Entry | TP-Niveau | Exit [A] | Abweichung |
|---|---|---|---|---|---|---|
| 5 | 1 | 1281.08 | 28.22 | 2339.41 | 2337.63 | +0.08 % |
| 6 | 3 | 2718.26 | 86.99 | 5980.54 | 5979.50 | +0.02 % |
| 7 | 5 | 4879.88 | 236.06 | 13732.06 | 13739.84 | -0.06 % |
| 9 | 4 | 8658.55 | 360.79 | 22188.06 | 22188.92 | 0.00 % |
| 14 | 5 | 49958.22 | 1117.02 | 91846.36 | 91841.20 | +0.01 % |
| 3 | 9 | 441.39 | 11.54 | 873.99 | 859.89 | +1.6 % |

**H-TP1 bestätigt [B]** (fünf Trades ab 2017 auf 0.08 Prozent, Trade 3 mit Datenvorbehalt 2016). Das Ziel wird nicht mit Add-ons angehoben (Trade 7 und 9 hätten sonst weit höhere Ziele gehabt). **H-TP2 «TP praktisch irrelevant»: widerlegt.** Sechs der acht Gewinner enden am Ziel, keiner der Gewinner am Stop ausser Trade 13 (Stop über Durchschnittseinstieg).

**Exit-Klassifikation aller 16 Trades:** 10 Stop-Exits (1, 2, 4, 8, 10, 11, 12, 13, 15, 16), 6 Take-Profit-Exits (3, 5, 6, 7, 9, 14). Kein Exit braucht den Failed-Breakout-Mechanismus zur Erklärung. **H-FBO1 bis H-FBO3: unklar, keine Evidenz nötig.** Der SMA200-Filter löst keinen Exit aus: Trade 13 blieb im Oktober 2023 offen, obwohl der Schluss unter dem SMA200 lag. **H-E2 bestätigt [B].**

## 5. Entry-Definition und Legs (Stufen G und H, vorgezogen)

Weil Stop und Ziel exakt bekannt sind, konnte die Vollsimulation (Stufe 9 des Plans) vorgezogen werden: Sie erzeugt Trades aus einer Entry-Regel, führt Stop und Ziel wie oben und wird an den 16 beobachteten Trades gemessen. Die Age-Deutungen aus dem Plan wurden nacheinander geprüft.

**H-AGE1 (Fenster [d-365, d-20] als Maximum): widerlegt.** Trade 7 (April 2019) bricht über 4300, das 365-Tage-Hoch lag bei 9964. Trade 13 (Januar 2023) bricht über 21 450, das 365-Tage-Hoch bei 48 000.

**H-AGE3 (Age als Positionsalter): widerlegt.** Trade 13 lief 370 Tage.

**Regel (b), «jüngstes ungebrochenes Hoch, älter als 20 Tage»:** Niveau = Hoch des jüngsten Tages, der mindestens 20 und höchstens 365 Tage zurückliegt und dessen Hoch seither nicht überschritten wurde. Signal, wenn das Tageshoch dieses Niveau überschreitet und der Schluss über dem SMA200 liegt. Ergebnis: alle 16 Entry-Tage sind Signaltage, aber die Regel erzeugt 15 zusätzliche Trades, die MTP nicht zeigt, und zu viele Legs. **Vereinbar, aber unvollständig.**

**Regel (b'), Pivot-Hoch:** Wie (b), aber das Niveau muss ein lokales Hoch sein (höher als die n Tage davor). Grund: Trade 14 hätte am 17.05.2024 ein Add-on über dem Hoch vom 22.04.2024 gemacht, das keine Spitze war (13.04. lag höher). MTP hat es nicht gemacht. Mit n = 5 und Add-on nur bei Schluss über dem Niveau («Must Close Above» für Legs) sowie Abstand 1.5 ATR zum letzten Leg:

| Kennzahl | Ergebnis |
|---|---|
| Entry-Tag exakt | 13 von 16 (Trade 5 und 16 einen bzw. drei Tage früher, Trade 7 fehlt) |
| Exit-Tag exakt | 13 von 16 |
| Exit-Preis unter 0.1 Prozent | 10 von 16 (alle ab 2017 ausser Trade 5 mit -0.6 Prozent und Trade 16 mit -0.7 Prozent, Folge des Entry-Versatzes) |
| Legs exakt | 9 von 16 (Simulation unterzählt bei langen Trades: 2, 3, 13, 14, 16) |
| Simulierte Trades ohne Gegenstück | 1 (11.05.2019, Folge des fehlenden Trade 7) plus ein offener Trade ab 19.08.2026 |

Max Age 365 ist bestätigt durch das Fehlen von Legs: Im Oktober bis Dezember 2020 brach BTC über die Hochs von 2019 und 2017, beide älter als 365 Tage, und MTP hat keinen Leg mehr hinzugefügt (Trade 9 endete mit dem Ziel vom Einstiegstag). **H-LVL1 Niveau ist ein Hoch, nicht ein Schluss: bestätigt** (Trade 16, letzter Leg 05.10.2025: Schluss 123 513 unter dem Fenster-Hoch 124 457, Tageshoch darüber). **H-E1 in der Form (b'): stark vereinbar [B mit Rest].**

Zwei Konflikte bleiben und werden nicht durch Feinjustieren gelöst. Trade 7 (02.04.2019): Das Pivot-Niveau 4210 war am 30.03. intraday überschritten worden, ohne dass MTP einstieg (SMA200-Filter falsch), und am 02.04. gilt in der Simulation bereits das nächste Niveau (6552). MTP ist am 02.04. eingestiegen, hat das Niveau 4210 also als noch gültig behandelt. Trade 13 (18.01.2023): Entry am Tag des Hoch-Ausbruchs, obwohl der Schluss unter dem Niveau lag, was der Deutung «Must Close Above» für Entries widerspricht. Beide Fälle betreffen die Frage, wann ein Niveau «verbraucht» ist und ob der Ausbruch per Hoch oder per Schluss zählt. Vorab dokumentierte Alternativen, die als nächstes geprüft werden: Niveau wird nur durch einen tatsächlichen Einstieg oder Leg verbraucht (nicht durch einen gefilterten Ausbruch), und «Close Above Within 30» als Frist zwischen Hoch-Ausbruch und Schluss-Bestätigung.

**Legs.** Rekonstruierte Leg-Tage: Trade 8: 30.01. und 09.02.2020. Trade 10: 08.02. und 13.03.2021. Trade 12: 06.10., 15.10., 20.10.2021. Trade 13: letzter Leg 02.01.2024. Trade 16: letzter Leg 05.10.2025. **H-P1 (jeder Signaltag ist ein Leg): widerlegt** (Trade 8 hatte Signaltage am 06.02., 11.02., 12.02., 13.02.2020 ohne Leg). **H-P2 (Abstand k mal ATR): vereinbar** mit k um 1.5, erklärt Trade 8, 10, 12 exakt, unterzählt aber lange Trades. **H-P3 (N-Tage-Hoch): nicht separat prüfbar, in (b') enthalten.**

**Leg-Grössen.** Mit den rekonstruierten Leg-Tagen: Trade 8 Verhältnis zweiter zu erstem Leg 1.01, Trade 10 0.77 (in Einheiten). Gleich grosse Legs: **widerlegt** (Trade 10 weicht 1.8 Prozent im Durchschnittseinstieg ab). Gleiche Dollarbeträge: widerlegt (Trade 8). Vereinbar ist risikobasiertes Sizing (Einheiten proportional zu Portfolio-Equity geteilt durch ATR), das für Trade 8 eine Equity-Änderung von -0.3 Prozent und für Trade 10 von +7.3 Prozent zwischen den Legs verlangt, beides plausibel für ein Mehr-Asset-Portfolio. **H-P4c vereinbar, ohne Portfolio-Equity nicht identifizierbar.** Konsequenz: Leg-Grössen sind aus BTC allein nicht rekonstruierbar, die Signalstruktur schon.

## 6. Reproduktionsquote, Plan Abschnitt 6

Auf Basis der besten vorab dokumentierten Regelmenge (b' mit n = 5, Legs bei Schluss über Niveau, k = 1.5): Entry-Treffer 13 von 16, Exit-Treffer 13 von 16, Exit-Preis unter 0.1 Prozent bei 10 von 16 und unter 2 Prozent bei 13 von 16, Leg-Treffer 9 von 16, ein falscher Positiver. Die im Plan gesetzte Grenze für die Hypothesenfamilie (12 Entries, 10 Exits) ist überschritten, die Familie gilt als **stark vereinbar**. Per-Trade-Tabelle in `stage1_per_trade.csv`, Simulationsliste in `sim_best_v1.csv`.

## 7. Was stärker und was schwächer geworden ist

Stärker, jetzt Ebene B: Preisquelle CMC. Einstieg zum Tagesschluss. Exit intraday am Niveau. Wilder-ATR(180). Stop fix am Leg, neu gesetzt bei jedem Add-on, kein Trailing. Ziel fix vom ersten Leg. Kein Filter-Exit. Max Age 365 als Grenze für gültige Niveaus. Niveau ist ein Hoch.

Schwächer oder widerlegt: Trailing-Stop. TP irrelevant. Fenster-Maximum als Niveau. Age als Positionsalter. Jeder Signaltag ein Leg. Gleiche Leg-Grössen. Failed-Breakout-Exit als erklärender Mechanismus (in 16 Trades nie nötig).

Offen: exakte Pivot-Definition (n zwischen 5 und 10), Verbrauch eines Niveaus bei gefiltertem Ausbruch, Hoch- gegen Schluss-Bestätigung beim Entry, Leg-Abstand, Leg-Grössen.

## 8. Abgleich mit der Stufe-2-Woo-Matrix (H-M1)

| Modul | Stufe 2 (W1 bis W8) | MTP rekonstruiert |
|---|---|---|
| Niveau | HH(N) über festes Fenster 20, 55, 100, 252 Tage | jüngstes Pivot-Hoch, 20 bis 365 Tage alt, kein festes Fenster |
| Ausbruch | Schluss über HH(N) | Tageshoch über Niveau, Einstieg zum Schluss |
| Stop | ATR(20) mal 3 oder 4, nachgezogen (Ratchet) | Wilder-ATR(180) mal 6.5, fix, nur bei Add-on neu gesetzt |
| Ziel | keines | Einstieg plus 37.5 ATR, fix, sechs von acht Gewinnern enden dort |
| SMA200 | Gate für Einstieg und Ausstieg | nur Einstiegsfilter |
| Pyramiding | zwei Add-ons zu 0.25 bei neuem N-Tage-Hoch plus 1 ATR | bis zu acht Add-ons, jeder ein eigener Pivot-Ausbruch, risikobasiert, Stop springt zum neuen Leg |
| Ausführung | Signal Schluss t, Fill Open t+1 | Fill Schluss t, Exits intraday am Niveau |
| Daten | Binance USDT | CoinMarketCap USD |

**H-M1 bestätigt:** Die Stufe-2-Matrix hat MTP in allen Modulen anders gebaut. Der Stop war drei- bis viermal enger und wurde nachgezogen, ein Ziel fehlte, der Filter schloss Positionen. Die Stufe-2-Urteile bleiben gültig für das, was sie gemessen haben, sie sagen nichts über MTP. Der Fingerprint-Befund «alle Varianten ähnlich» ist damit eingeordnet: Er misst allgemeine Trendfolge-Merkmale, nicht diese Mechanik.

## 9. Datenvorbehalt 2015 und 2016

Trades 1 bis 3 weichen 1.6 bis 5 Prozent ab, alle späteren unter 0.1 Prozent. Die Rechenregel ist dieselbe. Wahrscheinlichste Ursache: CoinMarketCap hat seine Historie vor 2017 nachträglich revidiert (andere Börsenauswahl im Index), der Backtester nutzt eine ältere Fassung oder lädt live. Prüfbar über einen Backtester-Lauf, der die BTC-Kurse jener Tage zeigt. Bis dahin gelten die Rekonstruktionen für 2015 und 2016 als «vereinbar», nicht als «bestätigt».

## 10. Nächste zwei bis drei Tests mit dem grössten Erkenntnisgewinn

1. **Leg-Termine je Trade aus dem Backtester** (Trade-Data-Tabelle aufklappen oder Chart-Marker ablesen), vorrangig Trade 13, 16, 3 und 7. Damit werden Pivot-Definition, Leg-Abstand und die Frage «Hoch oder Schluss» direkt entschieden, und die Leg-Grössen werden mit dem Durchschnittseinstieg prüfbar. Höchster Gewinn je Aufwand.
2. **Zwei Backtester-Läufe mit je einem geänderten Parameter:** Min Age 20 gegen 60 und Must Close Above ON gegen OFF. Beide Läufe verschieben, wenn die Rekonstruktion stimmt, genau die Entries von Trade 7 und 13 und lösen die zwei offenen Konflikte ohne weitere Rechnung.
3. **Vollsimulation mit den zwei vorab dokumentierten Alternativen zum Niveau-Verbrauch** (Verbrauch nur durch Einstieg oder Leg, Frist 30 Tage zwischen Hoch-Ausbruch und Schluss-Bestätigung), gemessen an denselben Kennzahlen. Läuft ohne neue Daten.

Nicht vorgesehen: weitere ATR-Varianten, andere Multiplikatoren, Feinjustierung von n, jede Performancezahl.

## 11. Dateien

`mtp_btc_trades_observed_v1.csv` (Ebene A), `stage1_per_trade.csv`, `sim_best_v1.csv`, `re_lib.py`, `stage_bcd.py`, `sim_mtp4.py` (beste Regelmenge, mit `sim_mtp3.py`), `kraken_funding_crosscheck.json` gehört zu Stufe 2. Datenreihen in `02_daten/raw/coinmarketcap/`, `raw/bitstamp/`, `raw/coinbase/`, Loader `nachladen_cmc.py`, `nachladen_btc_historie.py`.
