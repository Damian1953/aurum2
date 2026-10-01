# BTC Ichimoku-Inkrement-Plan, Version 0.1

**Project Aurum II, Strang 06_btc_specialist, Teil von BTC YAMATO RTC. 17.09.2026. Status: Plan zur Prüfung. Kein Rechenlauf. Quellenregel: `.jp`-Quellen. Ichimoku erzeugt keinen eigenständigen Einstieg und keinen eigenständigen Exit, es wird ausschliesslich als Inkrement zu einem bereits bestätigten YAMATO-Signal geprüft.**

## 0. Definition, klassisch, ohne Optimierung

Nach den japanischen Standardbeschreibungen (Matsui, Rakuten, Dukascopy Japan): Tenkan-sen = (höchstes Hoch + tiefstes Tief) / 2 über 9 Kerzen, Kijun-sen dasselbe über 26 Kerzen, Senkou Span A = (Tenkan + Kijun) / 2 um 26 Kerzen nach vorn versetzt, Senkou Span B = (höchstes Hoch + tiefstes Tief) / 2 über 52 Kerzen um 26 nach vorn versetzt, Chikou Span = Schluss um 26 Kerzen zurückversetzt. Parameter 9, 26, 52, Versatz 26, auf 4h-Kerzen unverändert übernommen (die Zahlen stammen aus dem japanischen Tageskalender, ihre Übertragung auf 4h ist eine Konvention, keine Kalibrierung, und wird nicht angepasst). Die Kijun ist die Mitte der 26-Kerzen-Spanne, ihre Steigung und die Lage des Preises zu ihr gelten in den Quellen als mittelfristige Trendaussage, 三役好転 (Tenkan über Kijun, Chikou über dem Preis, Preis über der Wolke) als starkes Kaufsignal, das selten ist.

Point-in-time: Senkou A und B für Kerze t sind die vor 26 Kerzen berechneten Werte (die «Wolke unter dem aktuellen Preis» ist bekannt). Die Chikou-Bedingung «Chikou über dem Preis» vergleicht C_t mit C_{t−26}, ist also bekannt. Der nach vorn gezeichnete Wolkenteil (Senkou für t+1 bis t+26) ist ebenfalls aus Daten bis t berechnet und darf verwendet werden, wird in dieser Version aber nicht verwendet.

## 1. Warum Ichimoku ein verzögerter Preisfilter sein könnte, und wie das geprüft wird

Die Kijun ist ein 26-Kerzen-Mittelpunkt, ein Schluss darüber ist mechanisch nahe an «der Preis liegt über dem Median der letzten 4.3 Tage». Die japanischen Quellen selbst nennen die Schwächen: Whipsaws in Ranges, Widersprüche zwischen Zeitebenen, Seltenheit der starken Signale. Ein Inkrement ist deshalb nur dann ein Zusatzwert, wenn die Kijun-Regel etwas anderes tut als eine gleich verzögerte Preisregel. Vorregistrierte Redundanzkontrolle: Jeder Kijun-Test wird parallel mit zwei Ersatzregeln gleicher Verzögerung gerechnet, erstens «Schluss über dem 26-Kerzen-Median der Schlusskurse», zweitens «Schluss über dem Einstieg plus 1 ATR» (reine Preisfortschrittsregel). Zeigt die Kijun-Regel keinen Unterschied zu diesen Ersatzregeln (gepaarte Differenz der Erwartung innerhalb des Bootstrap-Intervalls), ist Ichimoku als verzögerter Preisfilter ohne Zusatzinformation zu vermerken, und die einfachere Regel bleibt. Das ist vorab so festgelegt.

## 2. Inkrement-Tests

**Y6, Kijun-Reclaim als Trendbestätigung nach bestätigtem Boden.** Baseline: YAMATO-Einstieg mit Trigger TA. Inkrement: Einstieg erst, wenn nach der TA-Bestätigung zusätzlich eine Kerze über der Kijun schliesst (innerhalb von 12 Kerzen, sonst verfällt der Kandidat). Gepaarter Vergleich auf denselben Kandidaten: Erwartung je Trade, Einstiegspreis relativ zum Kandidatenschluss, verfallene Kandidaten, Capture Ratio. Frage: Bestätigt die Kijun, dass aus der Umkehr ein Trend wurde, oder verspätet sie nur den Einstieg? Ersatzregeln nach Abschnitt 1 laufen mit.

**Y7, Kijun-Verlust als Exit-Bestätigung nach Peak Candidate.** Baseline: E-Y (Bruch des letzten Higher Low nach Peak Candidate). Inkrement: Exit, sobald nach einem Peak Candidate eine Kerze unter der Kijun schliesst, was in der Regel vor dem Bruch des Higher Low eintritt. Gepaart: Giveback, Erwartung, Anteil abgeschnittener Gewinner (Trades, die nach dem Kijun-Exit noch mehr als 2 ATR stiegen). Ersatzregeln laufen mit.

**Bericht, kein Test:** Anteil der YAMATO-Einstiege mit 三役好転 innerhalb von 30 Kerzen nach Einstieg und deren Erwartung gegen die übrigen, Lage des Kandidaten zur Wolke (unter, in, über) als Kontextaufteilung, Tages-Ichimoku (Preis zur Tageswolke) als Multi-Timeframe-Kontext des Kandidaten.

## 3. Was Ichimoku nicht darf

Kein Einstieg ohne YAMATO-Kandidaten und Bestätigung. Kein Exit ohne Peak Candidate. Keine Parameteränderung, auch keine «4h-angepasste» Fassung. Keine Verwendung des nach vorn gezeichneten Wolkenteils als Ziel.

## 4. Offene Entscheidungen

1. Fenster 12 Kerzen für den Kijun-Reclaim nach TA bestätigen.
2. Ersatzregeln (26-Kerzen-Median, Einstieg plus 1 ATR) bestätigen.
3. Ob Y7 gleichrangig mit Y6 in der Holm-Familie läuft (Empfehlung: ja, beide in der YAMATO-Familie).
