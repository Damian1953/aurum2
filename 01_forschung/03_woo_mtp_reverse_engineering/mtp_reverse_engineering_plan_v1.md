# Woo / Market Trend Pro — Reverse-Engineering-Plan, Version 1

**Project Aurum II, Forschungsstrang 03_woo_mtp_reverse_engineering. Stand 16.09.2026. Status: Plan zur Prüfung, kein Rechenlauf gestartet.**

## 0. Zweck und Abgrenzung

Ziel ist ausschliesslich, die öffentlich sichtbare Mechanik von Travis Woos Market Trend Pro (MTP) aus Primärdaten so exakt wie möglich zu rekonstruieren und zu prüfen, ob die Woo-Matrix W0 bis W8 aus Stufe 2 dasselbe System abgebildet hat. Erfolgsmass ist die Reproduktionsgenauigkeit der beobachteten BTC-Signale (Termine, Legs, Preise), nicht eine Performancekennzahl. CAGR, Sharpe, Calmar, Drawdown, Profit und Alpha sind in diesem Strang keine Auswahlkriterien und werden nicht berechnet.

Stufe 2 bleibt unangetastet. Kein Ergebnis dieses Strangs wird benutzt, um ein Stufe-2-Urteil umzudeuten. Was hier entsteht, ist eine neue Hypothese für einen neuen Strang (03_woo_forward_spot), nicht eine Korrektur der alten.

Drei Ebenen werden im ganzen Dokument getrennt und mit Kürzeln markiert: **[A] beobachtet** (direkt aus dem öffentlichen Backtester), **[B] rekonstruiert** (eine mathematische Regel erklärt die beobachteten Trades), **[C] spekulativ** (plausibel, ohne ausreichende Evidenz). Zum Zeitpunkt dieses Plans gibt es noch keine Ebene-B-Aussage. Alles unter «Hypothesen» ist Ebene C, bis der Test es hebt oder verwirft.

## 1. Bekannte Fakten [A]

### 1.1 Defaults des öffentlichen Backtesters

| Modul | Parameter | Default |
|---|---|---|
| Entry Filter | SMA | 200, aktiviert |
| Breakout Entry | Must Close Above | ON |
| Breakout Entry | Close Above Within | 30 Tage |
| Breakout Entry | Min Age | 20 |
| Breakout Entry | Max Age | 365 |
| Stop Loss | ATR Period, Multiplier | 180, 6.5 |
| Take Profit | ATR Period, Multiplier | 180, 37.5 |
| Pyramid | Min Pyramid, Max Pyramid | 0, 100 |
| Pyramid | Only Pyramid When SL > New Avg Entry | OFF |
| Failed Breakout Exit | Close-Below-Within-Komponente | OFF |
| Failed Breakout Exit | FBO SMA Filter, FBO SMA | ON, 200 |
| Failed Breakout Exit | FBO Min Age, FBO Max Age | 20, 200 |

Weitere im Optimizer sichtbare Schalter: SL ATR PERIOD, TP ATR PERIOD, FILTER MA PERIOD, FBO FILTER MA PERIOD, Filter enable, FBO filter enable, SL ATR MULT, TP ATR MULT, MIN PYRAMID, MAX PYRAMID, REQUIRE SL ABOVE AVG ENTRY, MIN AGE, MAX AGE, EXIT ON FAILED BREAKOUT, MUST CLOSE ABOVE, CLOSE BELOW WITHIN DAYS, CLOSE ABOVE WITHIN DAYS.

### 1.2 Beobachtete Struktur

Long/Cash-Kern. SMA200 als Default-Filter. Breakout-Entry. Mehrstufiges Pyramiding mit deutlich mehr als zwei Add-ons (BTC maximal 9 Legs). Sehr lange Gewinner, starke positive Schiefe, viele Verlierer, wenige grosse Gewinner. Portfolio über mehrere Assets. Position Sizing teilweise durch den Nutzer konfigurierbar.

### 1.3 BTC-Trades aus der Trade-Data-Tabelle

Sechzehn Trades, abgelegt in `mtp_btc_trades_observed_v1.csv`. Spalten `entry`, `exit`, `legs`, `avg_entry`, `exit_px` sind Ebene A. Die Spalten `hold_d` und `ret` sind Arithmetik auf diesen Zahlen, keine Interpretation.

| Nr | Entry | Exit | Legs | Ø Entry | Exit | Tage | Exit gegen Ø Entry |
|---|---|---|---|---|---|---|---|
| 1 | 2015-06-30 | 2015-08-18 | 2 | 284.94 | 232.77 | 49 | -18.3 % |
| 2 | 2015-10-16 | 2015-11-10 | 6 | 330.22 | 340.24 | 25 | +3.0 % |
| 3 | 2016-04-20 | 2016-12-22 | 9 | 570.46 | 859.89 | 246 | +50.7 % |
| 4 | 2017-02-24 | 2017-03-18 | 1 | 1173.68 | 1033.60 | 22 | -11.9 % |
| 5 | 2017-04-26 | 2017-05-24 | 1 | 1281.08 | 2337.63 | 28 | +82.5 % |
| 6 | 2017-08-01 | 2017-10-20 | 3 | 3648.77 | 5979.50 | 80 | +63.9 % |
| 7 | 2019-04-02 | 2019-06-26 | 5 | 6920.69 | 13739.84 | 85 | +98.5 % |
| 8 | 2020-01-30 | 2020-03-09 | 2 | 9814.26 | 7953.95 | 39 | -19.0 % |
| 9 | 2020-04-30 | 2020-12-17 | 4 | 10669.76 | 22188.92 | 231 | +108.0 % |
| 10 | 2021-02-08 | 2021-03-25 | 2 | 52761.62 | 51361.73 | 45 | -2.7 % |
| 11 | 2021-04-13 | 2021-04-22 | 1 | 63503.46 | 52383.82 | 9 | -17.5 % |
| 12 | 2021-10-06 | 2021-12-04 | 3 | 60800.22 | 50806.03 | 59 | -16.4 % |
| 13 | 2023-01-18 | 2024-01-23 | 8 | 29887.23 | 38570.93 | 370 | +29.1 % |
| 14 | 2024-02-12 | 2024-11-13 | 5 | 67668.60 | 91841.20 | 275 | +35.7 % |
| 15 | 2025-01-20 | 2025-02-26 | 1 | 102016.66 | 83891.32 | 37 | -17.8 % |
| 16 | 2025-04-25 | 2025-10-10 | 7 | 112170.79 | 104770.44 | 168 | -6.6 % |

Mittlere Haltedauer 110.5 Tage, Median 54, längster Trade 370 Tage, 3.75 Legs im Mittel, Trefferquote 8 von 16.

### 1.4 Zwei Beobachtungen, die direkt aus den Zahlen folgen, ohne Marktdaten

Erstens: Die drei Einzel-Leg-Einstiege (Nr. 4, 5, 15) sind exakt als float32 darstellbar (1173.6800537109375 ist float32 von 1173.68, 1281.0799560546875 von 1281.08, 102016.6640625 von 102016.66). Einstiegspreise sind also Kursnotierungen mit zwei Dezimalen, die im Backtester in einfacher Genauigkeit gespeichert wurden. Mehr-Leg-Einstiege verlieren das Muster durch die Durchschnittsbildung. Kein einziger Exit-Preis ist float32. Exits sind demnach berechnete Werte (ein Stop- oder TP-Niveau, oder eine Rechnung auf einem Quote), keine gespeicherten Notierungen. Ebene A ist die Zahlenstruktur, die Deutung «Exit am berechneten Niveau statt am Bar-Preis» ist Ebene C und wird in H-X4 geprüft.

Zweitens: Fünf der acht Verlierer liegen zwischen -16.4 und -19.0 Prozent gegenüber dem Durchschnittseinstieg (Nr. 1, 8, 11, 12, 15), die übrigen drei bei -11.9, -6.6 und -2.7 Prozent. Ein Cluster dieser Enge deutet auf einen Ausstiegsmechanismus mit fester relativer Distanz. Das ist mit 6.5 mal ATR(180) vereinbar, wenn ATR(180) zwischen 2.5 und 3 Prozent des Kurses liegt, und mit einem Stop, der vom Einstieg und nicht von einem späteren Hoch gemessen wird. Deutung Ebene C, Prüfung in H-SL1 bis H-SL3.

## 2. Unbekannte Variablen

Preisreihe des Backtesters (Börse, Index, Tageszeit des Bar-Schlusses, UTC oder lokal). Definition von «Age» (Alter des Hochs, Alter des Ausbruchs, Alter der Position). Definition des Ausbruchsniveaus (höchster Close, höchstes High, mit welchem Fenster). Bedeutung von «Close Above Within 30». Ausführungszeitpunkt von Entries (Schluss des Signaltages, Eröffnung des Folgetages, Intraday am Niveau). Ausführungszeitpunkt von Exits (Intraday am Stop-Niveau, Schluss, Folge-Eröffnung). Trigger der Add-ons. Grösse der Legs (konstant, degressiv, kapitalabhängig) und ob Max Pyramid 100 eine Anzahl oder ein Prozentsatz ist. Ob der Stop nachgezogen wird und wovon (höchstes High, höchster Close, letzter Leg-Einstieg). Ob ATR(180) zum Einstieg fixiert oder täglich neu berechnet wird. Ob der TP je Leg oder auf den Durchschnitt gilt. Was der FBO-Exit genau prüft. Ob Legs einzeln oder alle zusammen geschlossen werden (die Tabelle zeigt einen Exit je Trade, was auf Gesamtschliessung deutet, Ebene C). Ob Portfoliobeschränkungen (Kapital, Anzahl Positionen) BTC-Signale unterdrückt haben.

## 3. Hypothesen je MTP-Modul (alle Ebene C bis zur Prüfung)

### 3.1 Datenquelle und Konvention

**H-D1.** Die Preisreihe ist eine USD-Reihe einer westlichen Spot-Börse mit zwei Dezimalen (Coinbase, Bitstamp oder ein Index), nicht Binance USDT. Prüfung: Die drei float32-Einstiege 1173.68 (2017-02-24), 1281.08 (2017-04-26) und 102016.66 (2025-01-20) werden gegen Open und Close mehrerer Quellen verglichen. Ein exakter Treffer identifiziert Quelle und Ausführungszeitpunkt zugleich. Höchster Informationsgewinn je Aufwand im ganzen Plan.

**H-D2.** Entries werden zum Schluss des Signaltages ausgeführt, nicht zur Eröffnung des Folgetages. Alternative H-D2b: Folge-Open. Prüfung über H-D1.

### 3.2 Age und Ausbruchsniveau

**H-AGE1 (Alter des Hochs).** Das Ausbruchsniveau ist das höchste High (oder der höchste Close) aller Tage, die zwischen Max Age und Min Age zurückliegen, also im Fenster [t-365, t-20]. Der Ausschluss der letzten 20 Tage verhindert, dass ein frisches Hoch sofort «ausgebrochen» wird. Alternative H-AGE1b: Das Niveau ist das höchste High der letzten 365 Tage, und Min Age verlangt, dass dieses Hoch mindestens 20 Tage alt ist (sonst kein Signal). Die beiden Varianten unterscheiden sich, wenn in den letzten 20 Tagen ein neues Hoch gesetzt wurde.

**H-AGE2 (Alter des Ausbruchs).** «Close Above Within 30» bedeutet: Der Einstieg erfolgt, wenn innerhalb der letzten 30 Tage ein Close über dem Niveau lag und die Filterbedingung erfüllt ist. Alternative H-AGE2b: Der erste Close über dem Niveau muss innerhalb von 30 Tagen nach einem Ereignis erfolgen (etwa nach dem Erreichen von Min Age). Alternative H-AGE2c: Das Signal verfällt, wenn der Close-Above länger als 30 Tage zurückliegt und noch kein Einstieg erfolgt ist (etwa weil der SMA200-Filter blockierte).

**H-AGE3.** Min Age und Max Age beziehen sich auf das Alter der Position (Trade wird nach 365 Tagen geschlossen). Trade 13 mit 370 Tagen widerspricht der harten Form, nicht aber einer Form mit Ausführung am Folgetag oder mit Kalender- gegen Handelstagen. Wird als Alternative mitgeführt, weil Trade 13 exakt an der 365-Grenze endet und kein anderer Trade länger lief.

**H-LVL1.** Das Niveau ist das höchste High im Fenster. Alternative H-LVL1b: höchster Close. «Must Close Above ON» spricht dafür, dass der Vergleich Close gegen Niveau geführt wird, sagt aber nichts über die Definition des Niveaus.

### 3.3 Entry-Bedingung

**H-E1.** Entry am Tag t, wenn Close(t) über dem Niveau nach H-AGE1/H-LVL1 liegt, Close(t) über SMA200(t) liegt, keine Position offen ist, und die Within-Bedingung nach H-AGE2 erfüllt ist. Einstieg zum Close(t) oder Open(t+1) nach H-D2.

**H-E2.** Der SMA200-Filter ist eine reine Einstiegsbedingung, kein Ausstiegsgrund. Das unterscheidet MTP von der Stufe-2-Matrix, wo das Gate auch den Exit auslöste. Prüfung: Gibt es Tage innerhalb offener MTP-Trades, an denen Close unter SMA200 lag, ohne dass der Trade endete? Trade 3 (2016), 9 (2020) und 13 (2023) sind lang genug, um das zu zeigen.

### 3.4 Pyramiding

**H-P1.** Jedes Add-on verwendet dieselbe Ausbruchsdefinition wie der Entry: neuer Close über dem aktuellen Niveau nach H-AGE1, wobei das Niveau mit jedem neuen Hoch wandert. Bei 9 Legs in Trade 3 über 246 Tage und 8 Legs in Trade 13 über 370 Tage müssten 8 beziehungsweise 7 solche Ereignisse rekonstruierbar sein.

**H-P2.** Add-ons werden durch ATR-Abstände ausgelöst (neues Leg, wenn der Kurs um k mal ATR über dem letzten Leg liegt). Prüfung: Für jeden Mehr-Leg-Trade wird der Kursverlauf nach ATR(180)-Vielfachen über dem letzten Leg abgetastet und gezählt, ob die Anzahl Legs mit einem festen k erklärbar ist.

**H-P3.** Add-ons an neuen Allzeithochs oder N-Tage-Hochs mit festem N. Prüfung analog H-P1 mit N aus {20, 30, 55, 100}. Kein Feinjustieren von N, nur diese Gitterpunkte.

**H-P4 (Grösse).** Legs sind gleich gross (Einheiten). Prüfung: Mit hypothetischen Leg-Terminen aus H-P1 bis H-P3 und den zugehörigen Kursen wird der Durchschnittseinstieg mit gleichen Gewichten berechnet und gegen den beobachteten Ø Entry gehalten. Alternative H-P4b: degressive Grössen (halbierend). Alternative H-P4c: Grösse aus Risiko-Sizing (Kapital mal Risikoanteil geteilt durch Stop-Distanz), dann ist die Grösse kursabhängig und nicht identifizierbar ohne Kapitalpfad.

**H-P5.** Max Pyramid 100 ist eine Prozentangabe des Ausgangskapitals oder der Ausgangsposition, nicht eine Anzahl. Min Pyramid 0 und Max Pyramid 100 als Prozent würde bedeuten: Add-ons dürfen die Position bis auf das Doppelte der Erstposition erhöhen. Bei 9 Legs wäre jedes Add-on dann rund 12.5 Prozent der Erstposition. Alternative H-P5b: Anzahl, praktisch unbegrenzt. Prüfung über H-P4.

**H-P6.** «Only Pyramid When SL > New Avg Entry OFF» bedeutet, dass Add-ons auch dann erfolgen, wenn der nachgezogene Stop unter dem neuen Durchschnittseinstieg liegt, die Position also nach dem Add-on wieder ins Risiko kommt. Der Schalter existiert nur, wenn der Stop nachgezogen wird und wenn er auf die Gesamtposition wirkt. Das stützt H-SL2 und H-X1 indirekt.

### 3.5 Stop Loss

**H-SL1 (initial).** Initialer Stop = Einstieg minus 6.5 mal ATR(180) zum Einstiegstag. Bei den fünf Verlierern mit -16 bis -19 Prozent müsste ATR(180)/Kurs am jeweiligen Einstiegstag zwischen 2.5 und 3.0 Prozent liegen. Das ist mit einer Rechnung je Trade direkt prüfbar und die schärfste Einzelprüfung des Plans.

**H-SL2 (nachziehen).** Der Stop wird auf höchstes High seit Einstieg minus 6.5 mal ATR(180) nachgezogen. Alternative H-SL2b: auf höchsten Close. Alternative H-SL2c: kein Nachziehen, Stop bleibt am Durchschnittseinstieg orientiert und wird nur bei Add-ons neu gesetzt. Die Verlierer Nr. 10 (-2.7 Prozent nach 45 Tagen) und 16 (-6.6 Prozent nach 168 Tagen, 7 Legs) sind die Testfälle: Ohne Nachziehen wären solche Exits nur durch FBO oder TP erklärbar.

**H-SL3 (ATR fixiert oder laufend).** ATR(180) wird täglich neu berechnet und der Stop entsprechend angepasst. Alternative: ATR zum Einstieg eingefroren. Bei 180 Tagen Periode ist der Unterschied klein, aber in Trade 13 (370 Tage) und 9 (231 Tage) messbar.

**H-SL4 (Bezug bei Add-ons).** Nach einem Add-on wird der Stop vom neuen Durchschnittseinstieg oder vom letzten Leg neu berechnet. Alternative: Der Stop bleibt am höchsten High orientiert und Add-ons ändern ihn nicht.

### 3.6 Take Profit

**H-TP1.** TP = Durchschnittseinstieg plus 37.5 mal ATR(180). Bei ATR/Kurs von 3 Prozent entspricht das plus 112 Prozent. Trades 7 (+98.5 Prozent, Exit 2019-06-26, nach Erinnerung nahe dem Hoch der damaligen Rally, zu prüfen) und 9 (+108 Prozent, Exit 2020-12-17 im laufenden Aufwärtstrend) sind die Kandidaten für einen TP-Exit. Ein Exit nahe einem Hoch ist mit einem Stop kaum vereinbar, mit einem Intraday-TP gut. Alternative H-TP1b: TP je Leg vom Leg-Einstieg. Alternative H-TP1c: TP vom ersten Leg.

**H-TP2.** Der TP ist in der Praxis fast nie relevant. Prüfung: Zählung, wie viele der acht Gewinner-Exits durch H-TP1 erklärt werden und wie viele durch Stop oder FBO. Ergebnis wird berichtet, nicht bewertet.

### 3.7 Failed Breakout Exit

**H-FBO1.** FBO prüft nach dem Einstieg, ob der Kurs unter das Ausbruchsniveau zurückfällt, wobei das Niveau mit eigenem Age-Fenster [t-200, t-20] und eigenem SMA200-Filter neu bestimmt wird. Exit, wenn Close unter dieses Niveau fällt und (FBO SMA Filter ON) der Close zugleich unter SMA200 liegt. Die Verlierer Nr. 4 (-11.9 Prozent nach 22 Tagen) und 10 (-2.7 Prozent) sind Kandidaten.

**H-FBO2.** «Close Below Within» OFF bedeutet, dass die zeitliche Begrenzung des FBO (nur innerhalb von X Tagen nach dem Ausbruch) abgeschaltet ist, der FBO also während der gesamten Haltedauer aktiv bleibt. Alternative: FBO wirkt nur solange die Position jung ist (Age-Fenster als Positionsalter).

**H-FBO3.** Der FBO SMA200 Filter bedeutet, dass ein Rückfall unter das Niveau nur dann als gescheiterter Ausbruch gilt, wenn der Kurs auch unter dem SMA200 liegt. Über dem SMA200 wird der Rückfall toleriert. Das würde erklären, warum lange Trades (3, 9, 13, 14) Rücksetzer überstehen.

### 3.8 Exit-Ausführung

**H-X1.** Alle Legs werden gemeinsam geschlossen, ein Exit-Preis je Trade. Ebene A zeigt einen Exit je Trade, die Deutung ist naheliegend, aber die Tabelle könnte aggregieren.

**H-X4.** Stop- und TP-Exits werden intraday am berechneten Niveau ausgeführt, wenn das Tageshoch beziehungsweise Tagestief das Niveau berührt. Das erklärt die Nicht-float32-Exitpreise (1.4). Alternative H-X4b: Exit zum Close des Tages, an dem das Niveau unterschritten wurde. Alternative H-X4c: Folge-Open. Prüfung: Für jeden Exit wird geprüft, ob der Exit-Preis innerhalb der Spanne Low bis High des Exit-Tages liegt (spricht für Intraday am Niveau) oder mit Close oder Folge-Open übereinstimmt.

### 3.9 Abgleich mit der Stufe-2-Matrix

**H-M1.** Die Stufe-2-Matrix hat MTP in vier Punkten nicht abgebildet: Ausbruchsniveau (HH(N) ohne Age-Fenster gegen [t-365, t-20]), Stop-Weite (ATR(20) mal 3 oder 4 gegen ATR(180) mal 6.5, also grob Faktor drei bis vier weiter), Gate als Exit (Stufe 2) gegen Filter nur am Einstieg (MTP), und Pyramiding (zwei Add-ons zu 0.25 gegen bis zu acht Add-ons). Die Prüfung ist eine Gegenüberstellung je Modul nach Abschluss der Rekonstruktion, ohne Performancezahlen. Das Ergebnis der Stufe-2-Fingerprint-Analyse («fast alle Varianten ähnlich») wird dadurch nicht verändert, sondern eingeordnet.

## 4. Testreihenfolge

Die Reihenfolge ist so gewählt, dass jede Stufe die Freiheitsgrade der nächsten einschränkt. Eine Stufe wird abgeschlossen und dokumentiert, bevor die nächste beginnt.

1. **Datenquelle und Ausführung (H-D1, H-D2).** Die drei float32-Einstiege gegen Open und Close verfügbarer Quellen. Ergebnis fixiert Preisreihe und Entry-Zeitpunkt für alles Weitere. Ohne Treffer wird mit der besten verfügbaren Reihe gearbeitet und jede spätere Aussage trägt den Vorbehalt «Preisreihe unbekannt».
2. **Exit-Ausführung (H-X4).** Jeder Exit-Preis gegen Low, High, Close des Exit-Tages und Open des Folgetages. Klassifikation je Trade: innerhalb der Spanne, gleich Close, gleich Folge-Open, ausserhalb.
3. **Initialer Stop (H-SL1).** ATR(180) je Einstiegstag, Stop-Niveau, Vergleich mit den fünf Verlierern bei -16 bis -19 Prozent. Bei Einzel-Leg-Trades 11 und 15 ist der Test exakt, weil der Durchschnittseinstieg der Einstieg ist.
4. **Nachziehen des Stops (H-SL2, H-SL3, H-SL4).** Für jeden Trade wird der Pfad des hypothetischen Stops unter jeder Variante berechnet und der erste Tag bestimmt, an dem Low unter Stop fällt. Vergleich mit dem beobachteten Exit-Tag und Exit-Preis. Trades ohne Add-ons zuerst (4, 5, 11, 15), dann Zwei-Leg-Trades (1, 8, 10), dann die übrigen.
5. **Take Profit (H-TP1, H-TP2).** Nur für Gewinner-Exits, die Stufe 4 nicht erklärt.
6. **FBO (H-FBO1 bis H-FBO3).** Nur für Exits, die Stufen 4 und 5 nicht erklären.
7. **Ausbruchsniveau und Entry (H-AGE1, H-AGE2, H-LVL1, H-E1, H-E2).** Für jeden Entry-Tag wird geprüft, welche Kombination aus Fenster, Niveau-Definition und Within-Regel an genau diesem Tag ein Signal erzeugt und an den Tagen davor keines. Zusätzlich werden alle Tage bestimmt, an denen die Regel ein Signal erzeugt hätte, ohne dass MTP einen Trade zeigt (falsche Positive). Für 2015 bis 2017 hängt das von der Datenbeschaffung in Abschnitt 5 ab.
8. **Add-ons (H-P1 bis H-P6).** Für jeden Mehr-Leg-Trade Rekonstruktion der Leg-Termine unter jeder Trigger-Hypothese, Vergleich der Anzahl mit der beobachteten Leg-Zahl, dann Prüfung der Grössenhypothesen über den Durchschnittseinstieg.
9. **Gesamtsimulation ohne Performance.** Die beste vereinbare Regelmenge wird als Signalgenerator über die BTC-Historie laufen gelassen. Output ist ausschliesslich die Liste der erzeugten Trades (Termine, Legs, Preise) gegen die sechzehn beobachteten. Keine Equity, keine Kennzahl.
10. **Gegenüberstellung mit der Stufe-2-Matrix (H-M1).** Tabelle je Modul.

## 5. Benötigte Daten

**Vorhanden.** Binance BTCUSDT Tageskerzen ab 2017-08-17 (decken Trades 6 bis 16, also elf von sechzehn). Kraken XBT/USD 720 Tage (Gegenprobe für Trades 14 bis 16 und für H-D1).

**Fehlend und nötig.** BTC-USD Tageskerzen (Open, High, Low, Close) von spätestens 2014-07-01 bis 2017-08-16, damit SMA200 und ATR(180) für Trade 1 (Einstieg 2015-06-30) mit vollem Fenster berechnet werden können. Quelle nach H-D1: bevorzugt dieselbe Börse, die der Backtester verwendet. Kandidaten Coinbase (ab 2015), Bitstamp (ab 2011), Bitfinex (ab 2013), Kraken (ab 2013, aber über die öffentliche API nur 720 Tage). Das Altprojekt Aurum ist auf längere BTC-Historie zu prüfen, bevor etwas geladen wird.

**Ohne diese Daten** bleiben Trades 1 bis 5 unprüfbar. Der Plan kann mit Trades 6 bis 16 beginnen (Stufen 1 bis 8), die Gesamtsimulation (Stufe 9) ist ohne 2014 bis 2017 unvollständig.

**Zusatzdaten aus dem Backtester** siehe Abschnitt 10.

## 6. Reproduktionsmetriken

Je Hypothese und je Trade wird festgehalten:

- Entry-Tag: Abweichung in Handelstagen zwischen rekonstruiertem und beobachtetem Einstieg (0 ist Treffer, ±1 ist «vereinbar mit Ausführungskonvention», mehr ist Fehltreffer).
- Exit-Tag: gleich.
- Exit-Preis: relative Abweichung zum beobachteten Exit. Unter 0.1 Prozent ist Treffer (Niveau-Rechnung), unter 2 Prozent ist vereinbar (Konvention Close gegen Intraday), darüber Fehltreffer.
- Legs: Anzahl rekonstruiert gegen beobachtet, exakt oder ±1.
- Durchschnittseinstieg: relative Abweichung unter 0.5 Prozent ist Treffer.
- Falsche Positive: Anzahl Tage, an denen die Regel einen Entry erzeugt, den MTP nicht zeigt, je Regelmenge über die ganze Historie.
- Falsche Negative: beobachtete Trades ohne rekonstruierten Entry.

Aggregiert je Regelmenge: Anteil Trades mit Entry-Treffer, Anteil mit Exit-Treffer, Anteil mit Leg-Treffer, Anzahl falsche Positive. Kein Score wird über diese Anteile hinaus gebildet, weil Gewichtungen die Auswahl steuern würden.

Klassifikation je Hypothese nach den Vorgaben: **bestätigt** (alle prüfbaren Trades Treffer, keine falschen Positiven, die nicht durch eine andere bestätigte Regel erklärt sind), **stark vereinbar** (mindestens 80 Prozent Treffer, Rest ±1 Tag oder unter 2 Prozent), **vereinbar** (Mehrheit Treffer, keine Widersprüche, die nicht durch Datenunsicherheit erklärbar sind), **widerlegt** (mindestens ein Trade, der unter keiner Datenkonvention passt, oder systematische falsche Positive), **unklar** (zu wenige prüfbare Trades oder Alternativen nicht unterscheidbar).

## 7. Mögliche Identifikationsprobleme

**Unterbestimmtheit der Legs.** Ein Durchschnittseinstieg mit n Legs ist eine Gleichung für 2n-1 Unbekannte (Termine und relative Grössen). Ohne Leg-Termine aus dem Backtester ist die Grössenhypothese nur unter einer angenommenen Trigger-Regel prüfbar. Konsequenz: H-P4 wird nur dann klassifiziert, wenn H-P1 bis H-P3 zuvor eine eindeutige Termine-Menge liefern. Sonst «unklar».

**Preisreihe.** Unterschiede zwischen Börsen von 0.5 bis 2 Prozent (2015 bis 2017 auch mehr) reichen, um Stop-Berührungen um Tage zu verschieben. Alle Exit-Tests werden deshalb mit einer Toleranz von ±1 Tag geführt und die Preisquelle wird als Vorbehalt geführt, solange H-D1 nicht bestätigt ist.

**Äquivalente Regeln.** Ein Trailing Stop auf höchstem High und ein Trailing Stop auf höchstem Close unterscheiden sich in BTC-Tagesdaten oft nur um Tage. Wo zwei Regeln dieselben sechzehn Trades erklären, werden beide als «vereinbar» geführt. Die Entscheidung fällt nicht hier, sondern gegebenenfalls durch Zusatzdaten nach Abschnitt 10.

**Portfolio-Effekte.** Wenn der Backtester mit Kapitalgrenze über mehrere Assets lief, können BTC-Signale unterdrückt worden sein, weil das Kapital gebunden war. Dann gibt es Regelmengen, die zusätzliche Entries erzeugen, die MTP nicht zeigt, ohne dass die Regel falsch ist. Falsche Positive werden deshalb berichtet und interpretiert, aber nur dann als Widerlegung gewertet, wenn sie auch in Phasen ohne offene Position auftreten.

**Überanpassung durch Stufenwahl.** Die Testreihenfolge selbst ist eine Wahl. Sie wird vor dem ersten Lauf festgehalten und nicht nach Ergebnissen umgestellt. Alternativen werden mitgeführt, nicht nachgeschoben.

**Kalender gegen Handelstage.** Krypto handelt täglich, aber der Backtester könnte Bars nach UTC oder nach einer anderen Zeitzone schneiden. Eine Verschiebung des Tagesrasters um einige Stunden ändert Open, High, Low, Close. Wird in Stufe 1 mitgeprüft (Tagesraster mit Versatz 0, plus 4, plus 8 Stunden ist mit Stundendaten prüfbar, die wir für BTC nicht haben, also zunächst nur Tagesraster UTC, Vorbehalt).

## 8. Fail-Kriterien

Der Strang wird als **nicht rekonstruierbar** abgeschlossen und dokumentiert, wenn nach Stufe 8 keine Regelmenge existiert, die mindestens zwölf der sechzehn Entry-Tage (±1 Tag) und mindestens zehn der sechzehn Exit-Tage (±1 Tag) zugleich erklärt, oder wenn jede Regelmenge, die das schafft, mehr als fünf falsche Positive in positionsfreien Phasen ab 2017-08 erzeugt.

Einzelne Module werden als **unklar** abgeschlossen, wenn nach ihrer Stufe zwei oder mehr Alternativen dieselbe Trefferzahl haben und keine Zusatzdaten verfügbar sind.

Der Strang wird **abgebrochen**, wenn H-D1 zeigt, dass die Preisreihe von allen verfügbaren Quellen um mehr als zwei Prozent abweicht und nicht beschafft werden kann, weil dann jede Exit-Rekonstruktion unter der Toleranz bleibt.

Nicht zulässig sind: Feinjustieren von Parametern (etwa 6.3 statt 6.5), um einzelne Trades passend zu machen. Einführen zusätzlicher Regeln, die nur einen Trade erklären. Wechsel der Testreihenfolge nach Ergebnissen. Jede Auswertung, die eine Performancekennzahl liefert.

## 9. Trennung Beobachtung / Rekonstruktion / Spekulation

Jede Aussage im Abschlussbericht dieses Strangs trägt eines der Kürzel [A], [B], [C]. Ebene A ist genau der Inhalt von Abschnitt 1.1 bis 1.3 sowie die Zahlenstruktur in 1.4. Ebene B entsteht erst durch die Klassifikation «bestätigt» oder «stark vereinbar» in Abschnitt 6, mit Angabe, welche Trades die Regel erklärt und welche nicht. Ebene C ist alles andere, einschliesslich jeder Deutung eines Parameternamens. «Vereinbar» bleibt Ebene C mit Vermerk. Keine Ebene-C-Aussage wird ohne Kürzel als MTP-Fakt formuliert, auch nicht in Zusammenfassungen. Eine Regelmenge, die in die Forward-Test-Planung (03_woo_forward_spot) übernommen wird, muss vollständig aus Ebene B bestehen oder jede Ebene-C-Komponente als eigene Annahme ausweisen.

## 10. Zusätzliche Primärdaten mit dem grössten Informationsgewinn

In absteigender Reihenfolge des Nutzens je Aufwand:

1. **Leg-Termine und Leg-Preise je Trade** (falls die Trade-Data-Tabelle aufklappbar ist oder ein Export existiert). Löst die Unterbestimmtheit aus Abschnitt 7 vollständig und macht H-P1 bis H-P5 direkt prüfbar. Wichtigster Einzelgewinn.
2. **Exit-Grund je Trade** (Stop, TP, FBO, Ende), falls der Backtester ihn anzeigt. Ersetzt die Stufen 4 bis 6 durch eine Bestätigung.
3. **Ein zweites Asset mit gleichen Defaults** (ETH oder ein Coin mit anderer Volatilität). Trennt Regeln, die auf BTC äquivalent sind, und prüft, ob die Stop-Distanz wirklich mit ATR skaliert.
4. **Derselbe BTC-Lauf mit einem geänderten Parameter**, je einer der folgenden: Min Age 20 gegen 60, Close Above Within 30 gegen 5, SL Mult 6.5 gegen 3.0, Max Pyramid 100 gegen 0, FBO Filter OFF. Jede Änderung, die Trade-Termine verschiebt, identifiziert die Bedeutung des Parameters fast direkt. Fünf Läufe, fünf Module.
5. **Angabe der Preisquelle** im Backtester (Fusszeile, Einstellung, Dokumentation). Ersetzt H-D1.
6. **Equity- oder Positionsgrössen-Verlauf**, falls sichtbar. Erlaubt Rückschluss auf Leg-Grössen und Risiko-Sizing.
7. **Screenshots der Trade-Marker im Chart** für Trade 3 und 13. Zeigen Leg-Termine grob, auch ohne Tabelle.

Punkte 1, 2 und 4 sind, falls der Backtester sie hergibt, wertvoller als jede Rechnung in diesem Plan.

## 11. Ablage und Freeze

Ordner `01_forschung/03_woo_mtp_reverse_engineering/`. Dieser Plan wird nach Prüfung mit Prüfsumme in `00_doku/ENTSCHEIDE.md` festgehalten, danach beginnt Stufe 1 der Testreihenfolge. Jede Stufe erhält eine eigene Ergebnisdatei `re_stufe<N>_<modul>.md` mit Klassifikation je Hypothese. Der Abschlussbericht `mtp_reconstruction_v1.md` enthält die Regelmenge mit Ebenen-Kürzeln und die Gegenüberstellung zur Stufe-2-Matrix. Kein Performance-Output in diesem Ordner.
