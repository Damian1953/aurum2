# BTC YAMATO RTC — Forschungsplan, Version 0.1

**Project Aurum II, Strang 06_btc_specialist (`01_forschung/06_btc_specialist/`). 17.09.2026. Status: Plan zur Prüfung. Kein Rechenlauf, kein Freeze. Quellenregel dieses Strangs: Externe Inspiration ausschliesslich aus japanischen `.jp`-Quellen (Monex, Nomura, Okasan, Hoxsin, Matsui, Rakuten, OANDA Japan, CoinPost, SBI VC Trade, kabutech, GogoJungle). Alle Freeze-Urteile bleiben unangetastet. Ergänzt `btc_specialist_research_plan_v0.2.md` um eine vierte, eigenständige BTC-Hypothese und stützt sich auf vier Spezifikationen: `btc_japanese_price_action_features_v0.1.md`, `btc_previous_open_levels_spec_v0.1.md`, `btc_sakata_bottom_peak_spec_v0.1.md`, `btc_ichimoku_increment_plan_v0.1.md`, sowie auf das RTC-Framework v0.1 und die Feature Library v0.1.**

## 0. Hypothese

Japanese Bottom Confirmation, Trend Capture, Peak Confirmation. Nach starken BTC-Rückgängen wird eine Bodenbildung möglichst früh, aber erst nach Price-Action-Bestätigung gehandelt, der entstehende Aufwärtstrend wird gehalten, solange die Struktur intakt ist, und erst bei japanisch definierter, bestätigter Peak- oder Trendbruch-Evidenz verkauft. Kein festes Gewinnziel, kein Exit am Mittelwert.

Die `.jp`-Quellen ergeben eine konsistente Logik: Kerzenform mit Betonung von Docht, Schlusslage und Volumen, 酒田五法 als Mehrkerzenlehre mit der Regel «erst Boden bestätigen, dann kaufen» und «erst Deckenbruch, dann verkaufen», Multi-Timeframe von Monat und Tag zum 4h-Chart, 一目均衡表 mit klassischen Parametern als Trendbestätigung, MACD-Divergenz als Bestätigung, Eröffnungen früherer Perioden als Referenzniveaus, Halving als Hintergrund. YAMATO übersetzt diese Logik in deterministische Regeln und prüft sie inkrementell, das ist unsere Synthese, nicht die der Quellen (Abschnitt 11).

## 1. Verhältnis zu BTC-RTC und Vorbelastung

YAMATO ist ein Geschwister von BTC-RTC (Framework v0.1) auf demselben Coin und derselben Zeitebene. Gemeinsam sind Kontext (K1 bis K3), Failed Breakdown, Lower-Wick-Rejection, Bestätigungs-Trigger TA und TB, Chandelier als harter Boden, Diagnosen. Eigen sind die Sakata-Mehrkerzenmuster (Double- und Triple-Bottom mit Nackenlinie, 三山), die Previous-Open-Niveaus mit Trigger TC, der strukturelle Hold ohne Peak-Score (E-Y: Peak Candidate, dann Bruch des letzten Higher Low), MACD-Divergenz und Ichimoku als Inkremente, und der Multi-Timeframe-Kontext von Woche und Tag. Beide werden vorregistriert und in derselben Discovery gerechnet. Regel gegen Auswahl: Die Überlappung der Kandidaten wird berichtet, kein Strang wird nach Ergebnis dem anderen vorgezogen, beide gehen bei «Signal vorhanden» in die Validation, und beide zählen in der Trial-Zahl des jeweils anderen. Der Portfolio-Layer entscheidet später über Gewichte.

Vorbelastung BTC (Abschnitt 0 des BTC-Plans v0.2): MTP ist auf BTC identifiziert, Stufe 1 und 2 haben auf BTC Tagesregeln geprüft. Nach der methodischen Regel des Frameworks ist das Dokumentation, kein Veto. Ein negativer YAMATO-Test beendet ausschliesslich die eingefrorene YAMATO-Spezifikation, keine Parameteroptimierung danach, eine sachlich neue japanische Price-Action-Hypothese darf später separat vorregistriert werden.

## 2. Multi-Timeframe-Hierarchie (A)

Woche und Tag: struktureller Kontext, berichtet je Kandidat (`d_ext`, `d_sma200_rel`, `d_ichimoku_pos`, `w_ext`, `w_swing_low_dist`), keine Bedingung, kein Schalter. 4h: primärer Setup- und Signal-Timeframe. 1h: nicht Bestandteil der Basisspezifikation, später optionaler Bestätigungstest (T1h nach Framework), sobald die 1h-Daten validiert sind. Grosse Zeitebenen werden vor kleinen berechnet und im Bericht vor ihnen gelesen.

## 3. Niveaus (B)

Japanische Support- und Resistance-Bibliothek, deterministisch, alle ATR-normalisiert: Previous-Open-Niveaus (4h, Tag, Woche, Monat, laufend und vorig, `btc_previous_open_levels_spec_v0.1.md`), bestätigte Swing Highs und Lows, doppelt und dreifach getestete Zonen (Library Abschnitt 5). Keine gezeichneten Linien. Die Previous-Open-Hypothese (frühere Eröffnungen sind relevante Niveaus, überzeugender Reclaim signalisiert Stärke) wird im Informationswert-Test mit Zufallskontrolle geprüft, bevor sie in der Validation eine Rolle spielen darf.

## 4. Bottom Candidate (C)

Kontext: definierter Selloff (K1, 12 Prozent unter dem 120-Kerzen-Hoch), Überdehnung (K2, 2 ATR unter EMA50 innerhalb der letzten sechs Kerzen), Nähe zu einer relevanten Struktur (K3, innerhalb 1 ATR eines Niveaus der Bibliothek einschliesslich Previous-Open-Niveaus, oder an der lokalen Low-Struktur). Dann eines der fünf Sakata-Muster: 下ヒゲ反転 (B1), はらみ線 in der Tiefzone (B2), 明けの明星 (B3), 三川 / 二番底 mit Nackenlinienbruch (B4), Failed Breakdown (B5), algorithmisch in `btc_sakata_bottom_peak_spec_v0.1.md`. Jeder Kandidat wird in Geometrie zerlegt (`lw_range`, `lower_wick_atr`, `body_range`, `close_location`, `range_atr`) und mit `volume_zscore`, `lw_x_vol`, `taker_imbalance` beschrieben.

## 5. Bestätigung (D): 底を確認してから買う

Kandidat ist nicht Einstieg. Baseline TA: Die folgende abgeschlossene 4h-Kerze schliesst über dem Hoch der Kandidatenkerze. Separat vorregistriert: TB (Rückeroberung des gebrochenen Swing Low oder Supports), TC (Rückeroberung eines Previous-Open-Niveaus, Tag oder Woche, innerhalb von sechs Kerzen). Einstieg frühestens zur Eröffnung der Kerze nach der vollständigen Bestätigungskerze. Initialer Stop unter der Kandidatenstruktur minus 0.5 ATR, Abbruch über 3 ATR, Sizing Sicht 1, eine Position, keine Add-ons.

## 6. MACD-Divergenz (E) und Ichimoku (F) als Inkremente

Y5: Kandidaten mit `bull_divergence` (Preis tieferes Tief, MACD-Linie höheres Tief an den letzten zwei bestätigten Swing Lows) gegen Kandidaten ohne, gepaart auf dem Fenster, mit Ersatzregel `mom10`. Y6: Einstieg erst nach Kijun-Reclaim zusätzlich zu TA, gegen TA allein. Y7: Exit bei Schluss unter Kijun nach Peak Candidate, gegen E-Y. Ersatzregeln gleicher Verzögerung laufen mit (Ichimoku-Plan Abschnitt 1), damit ein Inkrement nur zählt, wenn es mehr ist als ein verzögerter Preisfilter. Weder MACD noch Ichimoku erzeugen allein einen Einstieg oder Exit.

## 7. Trend Hold (G)

Nach bestätigtem Einstieg wird gehalten, solange erstens Higher Highs und Higher Lows bestehen (`hh_hl_intact` oder noch kein neues Swing-Paar), zweitens die Wocheneröffnung der Vorwoche als Support hält (`above_open_w_prev`), drittens keine bestätigte Peak-Struktur besteht. Bricht eine der drei Bedingungen, ist das Evidenz, kein Exit: Der Exit folgt der Regel E-Y (Abschnitt 8). Als mechanische Hard-Floor-Baseline läuft E1 (Chandelier 3 ATR14, nur steigend) parallel, der wirksame Stop ist immer max(initialer Stop, Floor), und der gepaarte Vergleich E-Y gegen E1 ist Test Y2. Kein Exit am Mittelwert, kein Prozentziel.

## 8. Japanese Peak Engine (H)

Peak Candidates: grosse Upper-Wick-Rejection in der Hochzone (P1), 宵の明星 (P2), 三山 / 三尊 mit Nackenlinienbruch (P3), Failed Breakout über bestätigtes Swing High (P4), Lower High nach neuem Hoch (P5). Kandidat ist kein automatischer Exit. Primäre Exit-Bestätigung E-Y: Schluss unter dem zuletzt bestätigten Higher Low innerhalb von 30 Kerzen nach einem Peak Candidate, Exit zur Eröffnung der Folgekerze. Sekundärer Inkrement-Test Y7: Schluss unter der Kijun nach Peak Candidate.

## 9. Zielmetriken (I)

Wirtschaftlich (Kriterien): Erwartung je Trade netto, Profit-Faktor, MaxDD gegen Passivposition, Bootstrap mit Holm, Kostenstress, Retention. Diagnostisch (nie Signal): Bottom Entry Efficiency, Trend Capture Ratio, Peak Exit Efficiency, realisierter Anteil der Post-Bottom-Aufwärtsbewegung, mittleres Giveback vom höchsten unrealisierten Gewinn bis Exit, alle nach Framework Abschnitt 14 in einem getrennten Modul.

## 10. Halving (J), Visual AI (K), Discovery-Regel (L)

Halving nur als Kontext (`days_since_halving`, `days_to_next_expected_halving`, `cycle_phase`), bedingte Erwartung bestehender YAMATO-Signale je Phase, explorativ, drei Zyklen, nach `halving_context_research_plan_v0.1.md`. Visual AI nach `visual_ai_second_opinion_plan_v0.1.md`, BTC-Charts, vier getrennte Konfidenzen (Bottom, Fortsetzung, Peak, Failed Breakdown oder Breakout), Inkrement-Test «YAMATO rules only» gegen «YAMATO rules plus Visual-AI-Zustimmung», kein Erzeugen, kein Überschreiben. Discovery-Regel nach Framework Abschnitt 2: Discovery bis 31.12.2023 (Binance-4h ab 2017-08, rund 6.4 Jahre), Holdout ab 2024, ein negativer Test beendet nur die eingefrorene YAMATO-Spezifikation.

## 11. Was `.jp`-gestützt ist und was Synthese

Direkt gestützt durch `.jp`-Quellen: die Sakata-Definitionen von 三山, 三川, 三尊, 逆三尊, 明けの明星, 宵の明星 und die Regel «Boden bestätigen, dann kaufen, Deckenbruch bestätigen, dann verkaufen» (Monex, Nomura, Okasan, Hoxsin), die Bedeutung von langem Docht mit hohem Volumen als Klimax (kabutech), die Multi-Timeframe-Lesart von Monat und Tag zum 4h-Chart und die 200-Tage-Linie als Referenz in BTC-Berichten (Monex, SBI VC Trade), MACD-Divergenz als Bestätigung in BTC-Analysen (Monex, CoinPost), die klassischen Ichimoku-Parameter, die Kijun-Lesart und 三役好転 samt der Kritik an Whipsaws und Zeitebenen-Widersprüchen (Matsui, Rakuten, Dukascopy Japan), Previous-Open-Niveaus als verbreitete Praxis (GogoJungle-Indikator), Halving als Hintergrund, nicht als Signal (Monex-Ausblick).

Unsere Synthese, nicht in den Quellen: die algorithmischen Definitionen (Toleranzen in ATR, Fenster in Kerzen, Nackenlinienbruch als Kandidatenkerze, Reclaim-Puffer), die Kontextbedingungen K1 bis K3, die Trigger TA, TB, TC als getrennte Tests, der Hold mit drei Bedingungen und E-Y als Peak-dann-Strukturbruch, die Ersatzregeln zur Redundanzkontrolle von MACD und Ichimoku, die inkrementelle Testarchitektur, Discovery und Validation, Capture Efficiency, die Verbindung zu Taker-Flow und Failed Breakdown. Für die Previous-Open-Hypothese gibt es in den `.jp`-Quellen Praxis, aber keine Prüfung, sie ist deshalb die am wenigsten gestützte Komponente und wird mit Zufallskontrolle geprüft.

## 12. Tests und Multiplizität (Discovery)

YAMATO-Familie (Holm über sieben): Y1 Baseline (`yamato_bottom_any`, TA, Hold mit E-Y, Long gegen exposure-gleiche Passivposition), Y2 E-Y gegen E1 gepaart, Y3 TB gegen TA, Y4 TC gegen TA, Y5 MACD-Divergenz-Inkrement, Y6 Kijun-Reclaim-Inkrement, Y7 Kijun-Exit-Inkrement. Berichte: Erwartung je Bottom- und Peak-Muster, Überlappung mit BTC-RTC, Kerzengrenzen (+1h, +2h), Cross-Venue (Kraken, ab 2023 OKX), Capture-Metriken, Tages- und Wochenkontext, Halving-Phasen, Informationswert der Previous-Open-Niveaus.

DSR-Trial-Zahl: 7 plus Jitter (Toleranzen, Fenster, Reclaim-Puffer, k, je einzeln) plus BTC-Vorbelastung 27 plus die 14 bis 16 Tests von BTC-RTC und 2 von BTC-B. Keine Auswahl nach CAGR.

Discovery-Kriterium «Signal vorhanden» und Konfigurationsregel für die Validation nach Framework Abschnitt 13, mit der vorab fixierten Regel: TB oder TC nur bei bestandenem Y3 beziehungsweise Y4 (bei beiden TB), Kijun-Inkremente nur bei bestandenem Y6 beziehungsweise Y7 und nur, wenn sie die Ersatzregeln schlagen, MACD-Aufteilung nur als Hypothese für die Validation, nie als Filter in der Discovery.

## 13. Daten

Vorhanden nach dem 4h-Lauf vom 17.09.2026: Binance Spot und Perp 4h und 1d mit allen Spalten (BTC ab 2017-08 beziehungsweise 2020-01), Kraken XBTUSD 240 (Archiv ab 2013 mit 579 Lücken in der Frühphase, API-Ergänzung bis 17.09.2026, Naht ohne Lücke), Funding, OI täglich, CMC, T-Bill. Wochen- und Monatseröffnungen werden aus den 4h-Kerzen gebildet, keine neue Quelle. Zusätzlich nötig: nichts für die Basisspezifikation. Für die spätere 1h-Bestätigung und die Kerzengrenzen-Diagnose die 1h-Kerzen (`nachladen_1h.py`, Launcher bereitgestellt). Für die Cross-Venue-Gegenprobe OKX-Kerzen ab 2023-07. Liquidations-Heatmaps, die die `.jp`-Berichte verwenden, sind nicht verfügbar und nicht Teil der Spezifikation.

## 14. Look-ahead

Framework Abschnitt 16, Library Abschnitt 8, Previous-Open Abschnitt 5, dazu: Nackenlinien nur aus bestätigten Swing Highs (Bestätigung drei Kerzen nach dem Hoch), Double-Bottom-Kandidat erst auf der Bruchkerze, Ichimoku-Senkou nur die vor 26 Kerzen berechneten Werte, MACD-Divergenz nur an bestätigten Swing Lows. Look-ahead-Test mit Schnitt 30.06.2022.

## 15. Offene Entscheidungen vor dem Freeze

1. YAMATO als eigener Strang neben BTC-RTC (Vorgabe, bestätigt) mit gegenseitiger Zählung in der Trial-Zahl.
2. Trigger TA als Baseline, TB und TC als Tests bestätigen.
3. Hold mit drei Bedingungen und E-Y mit 30-Kerzen-Fenster bestätigen.
4. Ersatzregeln für MACD und Ichimoku bestätigen.
5. Entscheidungen der vier Spezifikationen (Previous-Open 4, Sakata 4, Ichimoku 3) und des Frameworks gelten auch hier.

Nach Klärung: Version 1.0, Prüfsumme in ENTSCHEIDE, gemeinsamer Freeze mit Framework, Library und BTC-Plan v0.2, Datenvalidierung, Look-ahead-Test, Informationswert-Tests (Muster, Niveaus), ein Discovery-Lauf.
