# BTC YAMATO RTC — Stufe B, Bericht des einmaligen Development-Laufs, Version 1

**Project Aurum II, `01_forschung/06_btc_specialist/btc_yamato_stufeB_bericht_v1.md`. 19.09.2026. Eingefrorene Spezifikation `btc_yamato_stufeB_spec_v1.0.md` (SHA 0aed8e18…), rlib v1.0 (f1ffdbb8…) Modus `cfg_btc_stufeA`, Skripte `count_btc_b.py` (c5d5b818…) und `eval_btc_b.py` (2335b4f2…), Eingabe `BTCUSDT_spot4h_discovery.csv` (2d394fd1…), Kandidaten der outcome-blinden Zählung (173db748…, e6c2726a…), Seed 20260918, Bootstrap 2000, Kosten primär K1. Ein Lauf, keine Wiederholung, keine Parameteränderung. Ergebnisse versiegelt (`stufeB/eval/eval_BTC_B.json` 5d70030f…). BTC ist Development-Markt, Ebene C. Stufe A bleibt unverändert.**

## 1. Ergebnis in einem Absatz

Die beiden Stufe-B-Hypothesen bestätigen sich nicht. Erstens: Der Verzicht auf die Bestätigung (T0 statt TA) bringt je Kandidat keinen Gewinn, sondern kostet. Auf Y1 liegt die Erwartung je Kandidat bei T0 −0.23 R gegen −0.04 R bei TA und −0.12 R bei TB, auf Y3 −0.33 gegen −0.06 und −0.25 R. T0 handelt fast alle Kandidaten (78 von 96 Y1, 24 von 29 Y3) und verliert bei 26 beziehungsweise 25 Prozent Trefferquote im Mittel 0.29 und 0.40 R je Trade. Die Bestätigung filtert Verlierer, sie kostet keinen Trend: Der Einstieg liegt bei TA 2.9 ATR über dem ex-post Tief, bei T0 2.7 ATR. Zweitens: Der Exit-Horizont ist nicht das Problem. E-D (Tages-ATR) hebt das Mittel auf Y1 von −0.29 auf +0.11 R und auf Y2 von −0.30 auf +0.36 R, aber ausschliesslich durch wenige lange Trend-Trades (95. Perzentil 7.5 R), der Median bleibt bei −1.2 R, die Capture sinkt, der Giveback steigt, und keiner der drei gepaarten Vergleiche ist nach Holm signifikant. E0 (EMA20) ist auf Y1 und Y3 schlechter als E-U. Gegen die gematchten Kontrollen ist Y1 mit T0/E-U inconclusive (70 Paare, Median −0.03 R, 49 Prozent positiv), Y2 relativ besser als seine T0-Kontrollen (13 Paare, Median +0.73 R, 77 Prozent positiv, Holm p 0.042), aber absolut negativ und mit 14 Signalen deskriptiv, Y3 mit 18 Paaren nach Regel v2 mechanistisch vielversprechend in der Low-Frequency-Stufe, absolut −0.40 R netto und in Block P2 negativ. Der Kontext bleibt, was er in Stufe A war: eine Basisrate, die Geld verliert (Kontrollen −0.32 bis −0.98 R), und Muster, die den Verlust relativ verringern, ohne ihn aufzuheben.

## 2. Reproduktion der Referenzzeilen (Stufe A)

Y1 TA/E-U 16 Signale, Mittel −0.229 R, Y2 Nackenlinie/E-U 14 Signale, Mittel −0.297 R, Y3 TA/E-U 6 Signale, Mittel −0.291 R: identisch mit dem Stufe-A-Bericht (−0.23, −0.30, Y3 sechs Signale). Kandidaten, Kontrollpool und Einstiege wie in der Zählung. Die Stufe-A-Status (Y1 Fast Fail, Y2 und Y3 inconclusive) bleiben unverändert und werden hier nicht neu bewertet. Unterschied zu Stufe A in der Kontrollgruppe: Stufe B matcht Kontrollen mit demselben Trigger wie das verglichene Sleeve (T0 für Y1 und Y3, T0 für Y2-Kontrollen an der Bodenkerze s2), Stufe A verwendete TA auf den Kontrollen. Deshalb hat Y2 hier 13 statt 6 Paare.

## 3. Primäre Familie: T0 (Y2 Nackenlinie) mit E-U gegen Kontrollen (K1)

| | Y1 | Y2 | Y3 |
|---|---|---|---|
| Signale (P1 / P2) | 78 (41 / 37) | 14 (8 / 6) | 24 (12 / 12) |
| Verfall in_position / Stop zu weit | 17 / 1 | 0 / 0 | 3 / 2 |
| R netto K1 Mittel / Median / Trefferquote | −0.29 / −1.10 / 26 % | −0.30 / −0.35 / 7 % | −0.40 / −0.75 / 25 % |
| K0 / K2 Mittel | −0.09 / −0.61 | −0.22 / −0.43 | −0.30 / −0.58 |
| Profit Factor, grösster Gewinn (Anteil Bruttogewinn) | 0.65, 19 % | 0.09, 100 % | 0.41, 58 % |
| MFE Median, Capture Median | 0.74 R, −0.19 | 0.29 R, −0.16 | 0.55 R, −0.27 |
| Exit-Gründe | stop 32, chandelier 31, structure 8, stop_init 7 | chandelier 10, structure 4 | chandelier 9, stop 9, structure 5, stop_init 1 |
| Haltedauer Median | 10 Kerzen | 15.5 | 12 |
| Klassen fail / rebound / trend / delayed | 39 / 20 / 14 / 5 | 10 / 0 / 3 / 1 | 16 / 4 / 2 / 2 |
| Neues 20-Tage-Hoch in 30 / 60 Tagen | 18 % / 28 % | 21 % / 50 % | 8 % / 21 % |
| Kontrollen gehandelt, R netto Mittel / Median | 180, −0.49 / −1.28 | 32, −0.98 / −1.30 | 40, −0.32 / −1.16 |
| Kontrollen MFE Median, Capture Median | 0.97 R, −0.10 | 0.98 R, −0.12 | 0.98 R, −0.13 |
| Paare | 70 | 13 | 18 |
| ΔR Mittel (Bootstrap 5–95 %), Median, Anteil positiv | +0.16 (−0.26 bis +0.59), −0.03, 49 % | +0.67 (+0.17 bis +1.11), +0.73, 77 % | +0.05 (−0.82 bis +0.87), +0.29, 61 % |
| ΔMFE / ΔCapture / ΔTrend Mittel | −0.52 / −0.06 / −0.02 | −1.03 / 0.00 / +0.10 | −1.09 / −0.13 / −0.07 |
| ΔR nach Block Mittel (Median) | P1 +0.37 (−0.03), P2 −0.03 (0.00) | P1 +0.84 (+0.65), P2 +0.40 (+0.89) | P1 +1.05 (+0.51), P2 −0.96 (+0.07) |
| Bootstrap-p (ΔR ≤ 0), Holm | 0.27, 0.54 | 0.014, 0.042 | 0.45, 0.54 |
| Regel v2 (a Kontrolle, b Shift, c Konzentration, d Blöcke) | nein, nein, ja, ja | ja, nein, ja, ja | ja, nein, ja, ja |
| Fast Fail | nein | nein | nein |

«Signal vorhanden» (Holm < 0.05 und ΔR-Mittel > 0 und Netto K1 > 0): keine Hypothese, Y2 verfehlt es allein an der Bedingung Netto K1 > 0. Die Kontrollen haben in allen drei Familien höhere MFE als die Signale (ΔMFE −0.5 bis −1.1 R), das heisst die Muster identifizieren keine Kerzen mit grösserem Aufwärtspotenzial als der Kontext allein, sie verlieren nur weniger, weil sie öfter früh gestoppt werden oder weniger weit laufen.

## 4. Frage A: Trigger-Familie, Erwartung je Kandidat (96 Y1-Kandidaten, 29 Y3-Kandidaten, verfallene zählen null)

| | Y1 T0 | Y1 TA | Y1 TB | Y3 T0 | Y3 TA | Y3 TB |
|---|---|---|---|---|---|---|
| gehandelt / kein Trigger / in_position / Stop zu weit | 78 / 0 / 17 / 1 | 16 / 69 / 6 / 5 | 58 / 14 / 17 / 7 | 24 / 0 / 3 / 2 | 6 / 19 / 0 / 4 | 16 / 5 / 3 / 5 |
| R netto Mittel je Trade, Trefferquote | −0.29, 26 % | −0.23, 19 % | −0.20, 29 % | −0.40, 25 % | −0.29, 17 % | −0.46, 25 % |
| Erwartung je Kandidat | −0.233 | −0.038 | −0.121 | −0.334 | −0.060 | −0.255 |
| Einstieg über ex-post Tief, Median ATR | 2.71 | 2.89 | 2.86 | 2.16 | 2.55 | 2.46 |
| MFE Median, Capture Median | 0.74, −0.19 | 0.46, −0.16 | 0.90, −0.14 | 0.55, −0.27 | 0.08, −0.72 | 0.21, −0.39 |
| Profit Factor | 0.65 | 0.66 | 0.74 | 0.41 | 0.64 | 0.33 |

Gepaart je Kandidat (Trigger minus T0): Y1 TA +0.195 R (Bootstrap 5–95 % −0.06 bis +0.42, p ≤ 0 0.096), Y1 TB +0.112 (−0.00 bis +0.23, p 0.056), Y3 TA +0.274 (+0.06 bis +0.48, p 0.019), Y3 TB +0.080 (−0.10 bis +0.26, p 0.22). Holm über vier: 0.076, 0.167, 0.19, 0.22, keiner unter 0.05. Richtung in allen vier Vergleichen: die Bestätigung ist je Kandidat besser als T0, nicht schlechter. Die Stufe-B-Hypothese «die Bestätigung kostet Trend Capture» ist damit auf BTC nicht gestützt: Die Bestätigung kostet 0.2 bis 0.4 ATR Einstiegshöhe und filtert dafür mehr Verlierer als Gewinner heraus. TB (Reclaim des Niveaus innerhalb sechs Kerzen) liegt zwischen T0 und TA.

## 5. Frage B: Exit-Familie auf denselben T0-Einstiegen (Y2 Nackenlinie)

| | Y1 E-U | Y1 E-D | Y1 E0 | Y2 E-U | Y2 E-D | Y2 E0 | Y3 E-U | Y3 E-D | Y3 E0 |
|---|---|---|---|---|---|---|---|---|---|
| Trades | 78 | 69 | 77 | 14 | 13 | 14 | 24 | 25 | 24 |
| R netto Mittel / Median | −0.29 / −1.10 | +0.11 / −1.20 | −0.49 / −1.12 | −0.30 / −0.35 | +0.36 / −0.87 | −0.10 / −0.07 | −0.40 / −0.75 | −0.28 / −1.11 | −0.58 / −1.10 |
| Trefferquote, PF | 26 %, 0.65 | 19 %, 1.11 | 39 %, 0.34 | 7 %, 0.09 | 23 %, 1.54 | 14 %, 0.02 | 25 %, 0.41 | 20 %, 0.68 | 33 %, 0.21 |
| 95. Perzentil R | 3.2 | 7.5 | 1.1 | 0.1 | 5.4 | 0.0 | 1.6 | 3.3 | 0.7 |
| Capture Median, Giveback Median | −0.19, 1.39 | −0.22, 1.81 | −0.13, 1.06 | −0.16, 0.54 | −0.33, 1.31 | +0.01, 0.14 | −0.27, 1.19 | −0.34, 1.50 | −0.27, 1.12 |
| Haltedauer Median | 10 | 13 | 4 | 15.5 | 49 | 2 | 12 | 21 | 7 |
| abgeschnittene Trends | 28 % | 25 % | 29 % | 50 % | 38 % | 50 % | 21 % | 16 % | 21 % |

Gepaart auf gemeinsamen Einstiegskerzen: E-D minus E-U auf Y1 (66 gemeinsam) ΔR Mittel +0.33 (−0.22 bis +0.93, p ≤ 0 0.18), Median 0.00, nur 14 Prozent der Paare positiv, ΔCapture −0.08 (p 0.99 negativ), ΔGiveback +0.80 (100 Prozent positiv); Y2 (13) ΔR +0.66 (−0.40 bis +2.00, p 0.21), Median −0.56, 31 Prozent positiv; Y3 (23) ΔR +0.14 (p 0.43), Median 0.00, 13 Prozent positiv. Holm über drei: 0.55, 0.55, 0.55. E0 minus E-U: Y1 −0.22 (p 0.92), Y3 −0.17 (p 0.81), Y2 +0.19 (p 0.0015, 86 Prozent positiv, reine Verlustreduktion, Median +0.29 bei Trades von −0.07 R).

Befund: E-D verlängert die Haltedauer (Y1 im Mittel +34 Kerzen, Y2 +87) und lässt in wenigen Fällen einen grossen Trend laufen (Y1 ein Trade über 7 R, Y2 einer über 5 R), verliert aber in der Mehrzahl der Fälle dieselben Stops und gibt bei den übrigen mehr zurück. Das ist derselbe Befund wie in der Cross-Coin-Zusammenfassung («E-D nur längere Haltedauer»), jetzt auf dem dritten Coin. E0 schneidet auf Y1 und Y3 ab, bevor die Chandelier-Trades ihre wenigen Gewinne machen, und ist nur auf Y2 (das mit weitem Stop ohnehin kaum gestoppt wird) eine Verlustbremse.

## 6. Frage C: Statuszuweisung und Cross-Coin-Richtung

Nach Spezifikation Abschnitt 4 (Auswertungsregeln v1, Regel v2, Governance v1.1 Abschnitt 8):

Y1 T0/E-U: 78 Signale, normale Stufe. Regel v2 zwei von vier, kein Fast Fail. **Status: no evidence, inconclusive.** Gegenüber Stufe A (TA, Fast Fail) ist die T0-Variante gegen ihre Kontrollen nicht mehr signifikant negativ, aber absolut schlechter (−0.29 gegen −0.23 R je Trade, −0.23 gegen −0.04 R je Kandidat).

Y2 Nackenlinie/E-U: 14 Signale, unter 20. Regel v2 drei von vier, Holm p 0.042 in der relativen Richtung. Nach Governance v1.1 Abschnitt 8 bleibt eine Familie unter 20 Trades deskriptiv, unabhängig von der Regel v2. **Status: deskriptiv, relativer Effekt gegenüber T0-Kontrollen (Verlustreduktion +0.67 R je Paar), absolut −0.30 R netto, ein Gewinner in 14.** Kein Validation-Anspruch. Derselbe Befund wie in Stufe A mit mehr Paaren.

Y3 T0/E-U: 24 Signale, Low-Frequency-Stufe (20 bis 29, höchstens MP). Regel v2 drei von vier (Median ΔR +0.29 mit 61 Prozent positiven Paaren, kein dominantes Paar, beide Blockmediane positiv). **Status: low-frequency evidence, mechanistically promising, validation deferred (Economic Gate).** Einschränkungen, ausdrücklich: 18 Paare, Bootstrap-Intervall des Mittels −0.82 bis +0.87, Blockmittel P2 −0.96 R, ein Trade trägt 58 Prozent des Bruttogewinns (v1-Bedingung d verfehlt), Netto K1 −0.40 R, MFE der Kontrollen um 1.1 R höher. Nach Governance v1.1 Abschnitt 7 ist eine Holdout-Validation nur bei Netto-Erwartung K1 über null oder vorab eingefrorener Portfolio-/Hedge-Funktion zulässig, beides liegt nicht vor. Status entspricht formal DOT D1 (MP, validation deferred), ist aber in jeder Kennzahl schwächer (DOT D1: 54 Trades, 52 Paare, 67 Prozent positiv, Netto −0.17 R).

Trigger-Familie: keine Konfiguration nach Holm positiv, Richtung TA > TB > T0 je Kandidat auf beiden Familien. Exit-Familie: keine nach Holm positiv, E-D Mittel höher, Median und Capture nicht, E0 schlechter (Y1, Y3). Konfigurationsregel für eine spätere Validation: primäre Konfiguration bleibt, keine Auswahl.

Cross-Coin-Richtung (Vorzeichenzählung, kein Pooling): T0/E-U gegen Kontrollen, Failed-Breakdown-Familie: BTC Y1 inconclusive (Median −0.03), XRP X1 inconclusive, DOT D1 MP (Median +0.21). Double Bottom: BTC Y2 relativ positiv, XRP X2 und DOT D2 inconclusive. Wick plus Volumen: BTC Y3 MP low-frequency, XRP X3 inconclusive, DOT D3 MP unter 20. E-D gegen E-U: auf allen drei Coins längere Haltedauer, Mittel teils höher, Median nie, nirgends signifikant. E0: auf keinem Coin besser als E-U ausser als Verlustbremse auf weit gestoppten Double-Bottom-Trades. Kein Muster wirkt auf zwei Coins in derselben Konfiguration mit derselben Stärke, die Voraussetzung für einen Cross-Coin-Test (Spezifikation Abschnitt 5) ist nicht erfüllt.

## 7. Was der Lauf über den Kontext sagt (Diagnose, keine Hypothese)

Über alle drei Familien und alle Trigger liegt die Basisrate der Kontextkerzen (Kontrollen, T0/E-U) bei −0.32 bis −0.98 R netto, die MFE-Mediane der Kontrollen bei 0.97 bis 0.98 R, ihre Trefferquote bei 12 bis 23 Prozent. Der Anteil der Signale, nach denen innerhalb 60 Tagen ein neues 20-Tage-Hoch entsteht, liegt bei 21 bis 50 Prozent, und 16 bis 50 Prozent der Trades werden beendet, bevor dieser Trend läuft. Das ist auf dem dritten Coin dieselbe Struktur wie in der Cross-Coin-Zusammenfassung und im REBOUND-MICRO-Lauf: Der Kontext markiert Böden, aus denen später ein Trend entstehen kann, aber weder ein Rebound-Ziel noch ein Chandelier ab dem ersten Reversal ernten ihn. Das ist der Grund für die getrennte Spezifikation DELAYED-TREND, sie wird hier nicht vorweggenommen.

## 8. Trial-Accounting und Vorbelastung

Stufe B 11 Tests, alle nach Holm nicht signifikant in positiver Richtung. Vorbelastung BTC rund 36 vor diesem Lauf, danach rund 47. Global rund 250. Für jede spätere BTC-Vorregistrierung als Vorbelastung zu führen.

## 9. Status-Eintrag (Vorschlag)

BTC YAMATO Stufe B v1.0 — abgeschlossen. Y1 T0/E-U no evidence inconclusive, Y2 deskriptiv (relativer Effekt, absolut negativ), Y3 low-frequency MP mit validation deferred (Economic Gate), Trigger- und Exit-Familie ohne positives Ergebnis, T0 je Kandidat schlechter als TA und TB. Keine Validation, kein Cross-Coin-Test, keine Regeländerung. Stufe A unverändert. Keine weitere Stufe C der YAMATO-Reihe: Eine neue Mechanik wäre eine neue Vorregistrierung.
