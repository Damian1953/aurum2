# BTC YAMATO RTC — Stufe B, Spezifikation Version 1.0 (Freeze)

**Project Aurum II, `01_forschung/06_btc_specialist/btc_yamato_stufeB_spec_v1.0.md`. 19.09.2026. Status: eingefroren vor jeder Outcome-Berechnung von Stufe B. Ersetzt die Vorregistrierung v0.1 (Entwurf vom 17.09.2026). BTC ist Development-Markt (Governance v1.1 Abschnitt 1), Stufe B ist eine outcome-informed Hypothesenfamilie der Ebene C, abgeleitet aus dem eingefrorenen Stufe-A-Bericht (Y1 Fast Fail, Y2 und Y3 inconclusive). Kein Stufe-A-Ergebnis wird verändert, Stufe A bleibt als Referenzzeile im Bericht. Keine Regel aus REBOUND-MICRO wird übernommen (Stufe B verwendet keine 1h-Daten, keine festen Ziele, keine Kandidatenänderung). Library: rlib v1.0 (f1ffdbb8…) im Modus `cfg_btc_stufeA` auf ylib (7f0230c9…), Regressionstest gegen Stufe A bestanden (205 von 205 Trades, `regressionstest_rlib_v1.0_gegen_stufeA.md`). Bis zum Freeze dieser Datei wurden keine Stufe-B-Outcomes (T0-, TB-, E-D-, E0-Trades) berechnet oder angesehen. Die Stufe-A-Outcomes (TA/E-U) sind bekannt und eingefroren.**

## 1. Entscheidungen zu den offenen Punkten der Vorregistrierung v0.1

1. TB-Definition bestätigt: erster Schluss über dem Referenzniveau in t+1 bis t+6, Einstieg zur Eröffnung der Folgekerze, sonst Verfall (identisch mit XRP v1.0 und DOT v1.0 Abschnitt 6).
2. Exit-Alternativen: E-D (Tages-ATR14-Chandelier und Tages-Strukturbruch) bestätigt. An Stelle von E-W (Floor erst nach neuem 20-Tage-Hoch) wird E0 (Schluss ≥ EMA20 oder 30 Kerzen, initialer Stop bleibt) geführt, wie in XRP v1.0 und DOT v1.0 als Kontrollarchitektur eingefroren. Grund, vor Outcome: Vergleichbarkeit über die drei Development-Coins, E-W wäre eine dritte, nur auf BTC getestete Exit-Variante und ist damit nicht cross-coin-fähig. E-W wird nicht getestet.
3. Erwartung je Kandidat als Hauptmetrik der Trigger-Familie bestätigt (verfallene Kandidaten zählen mit null).
4. Stufe B läuft auf BTC allein (Nutzerentscheid 19.09.2026), XRP v1.0 und DOT v1.0 sind bereits gelaufen und versiegelt. Vergleich der drei Coins im Bericht nur als Vorzeichenzählung, kein Pooling.

## 2. Daten, Parameter, Kandidaten (unverändert aus Stufe A)

Signalquelle `02_daten/holdout/discovery/BTCUSDT_spot4h_discovery.csv` (SHA 2d394fd1cbc344d5…, Manifest v1.1 e2e764b4…), 13950 Kerzen 2017-08-17 04:00 bis 2023-12-31 20:00 UTC, 9 Rasterlücken mit 17 fehlenden Kerzen, Vorlauf 134, auswertbar 13816. Flow-Datei `BTCUSDT_flow4h_discovery.csv` wird geladen, aber nicht ausgewertet (RTC-1 und RTC-2 abgeschlossen, ENTSCHEIDE 18.09.2026). Validation-Dateien werden nicht geladen (Guard aktiv). Blöcke P1 2017-08-17 bis 2020-12-31, P2 2021-01-01 bis 2023-12-31.

Parameter: Modus `cfg_btc_stufeA` = Parameterpaket v1.1 (7c4be2f8…) wortgleich: K1 `dd120` = C_t / max(H, t−120..t−1) − 1 ≤ −0.12, K2 `ext` ≤ −2.0 ATR in t−5..t, K3 Niveau innerhalb 1 ATR oder `at_low_structure` (Tief innerhalb 2 Prozent des 120-Kerzen-Tiefs), Penetration 0.1 Prozent, Stop L − 0.5 ATR14_t, Abbruch bei Stopdistanz > 3 ATR (Y1, Y3, Kontrollen, keine Grenze für Y2), Matching ±540 Kerzen, |Δdd120| ≤ 0.03, |Δext| ≤ 0.5, bis zu drei Kontrollen, Abstand > 12 Kerzen. Die ATR-Form (dd120_atr ≤ −6.0) wird nur als Coverage-Diagnose berichtet. Kandidaten Y1 (Failed Breakdown), Y2 (Double Bottom mit Nackenlinienbruch, ohne 3-ATR-Grenze wie v1.1), Y3 (Wick plus Volumen) exakt wie Stufe A v1.1, Y2 und Y3 Definitionen wie XRP v1.0 Abschnitt 5 in Prozentform. Kandidatentabellen der Zählung (Abschnitt 8) sind Eingabe des Laufs, Prüfsummen werden im Lauf geprüft.

## 3. Trigger, Exits, Fills, Kosten (wie XRP v1.0 Abschnitte 6 bis 9)

T0 Eröffnung t+1. TA Schluss t+1 über H_t, Einstieg Eröffnung t+2 (Stufe-A-Regel). TB wie Abschnitt 1. Y2 nur Nackenlinienbruch. Eine Position je Sleeve, `in_position`-Verfall. E-U Chandelier 3 ATR14(4h) plus 4h-Strukturbruch (Stufe A). E-D Chandelier 3 Tages-ATR14 plus Tages-Strukturbruch (k = 3 Tage). E0 Schluss ≥ EMA20 oder 30 Kerzen, initialer Stop bleibt. Fill- und Intrabar-Regeln U12/U13, MFE/MAE ab Einstiegskerze, Sizing Sicht 1 (2 Prozent). K1 massgebend (0.40 Prozent je Seite, Reibung 0.02, Slippage 0.05 Einstieg, 0.10 Stop), K0 und K2 Bericht.

## 4. Tests und Multiplizität (vor Outcome fixiert)

Primäre Familie (Holm über drei): Y1 T0/E-U, Y2 Nackenlinie/E-U, Y3 T0/E-U je gegen gematchte Kontrollen mit demselben Trigger und Exit, gepaarte ΔR netto K1, Bootstrap 2000, Seed 20260918. Trigger-Familie (Holm über vier): TA und TB gegen T0 auf Y1 und Y3, Erwartung je Kandidat, Bootstrap der Differenz je Kandidat. Exit-Familie (Holm über drei): E-D gegen E-U auf Y1, Y2, Y3, gepaart auf gemeinsamen Einstiegskerzen. Kontrollarchitektur (ein Test): E0 gegen E-U, gepaart. 3 mal 3 Matrix Trigger mal Exit wird berichtet, nicht getestet, keine Auswahl. Inkremente: keine (RTC-1 und RTC-2 abgeschlossen). Statuszuweisung nach Auswertungsregeln v1 mit Regel v2 (≥ 3 von 4) und Governance v1.1 Abschnitt 8 (unter 20 deskriptiv, 20 bis 29 höchstens MP, ab 30 normal, Statuszuweisung ausser inconclusive nur mit mindestens fünf Paaren). Fast Fail: Median ΔR < 0 und < 40 Prozent positive Paare bei ≥ 10 Paaren. Blockregel: beide Blöcke gleiche Richtung bei mindestens 5 Paaren je Block. Konfigurationsregel für eine spätere Validation: primäre Konfiguration, es sei denn, ein Vergleich ist innerhalb seiner Familie nach Holm positiv und die Basiskonfiguration nicht. Economic Validation Gate (Governance v1.1 Abschnitt 7) für jede Folge.

Referenzzeilen: Y1 TA/E-U (16 Signale, Stufe A −0.23 R, Fast Fail), Y2 Nackenlinie/E-U (14 Signale, −0.30 R, inconclusive), Y3 TA/E-U (6 Signale, inconclusive) müssen im Lauf exakt reproduziert werden (Regression), sie werden nicht neu bewertet.

Trial-Accounting: Stufe B 3 primär, 4 Trigger, 3 Exit, 1 Kontrollarchitektur = 11. Vorbelastung BTC nach `rebound_micro_trial_accounting_v0.1.md` rund 30 plus REBOUND-MICRO 6 = rund 36. Global rund 250 als Sensitivität.

## 5. Evidenzklasse und Deckel

Development Evidence, Ebene C (outcome-informed aus Stufe A). Höchste Folge eines positiven Ergebnisses: eine Vorregistrierung derselben Konfiguration als Cross-Coin-Test, sofern XRP v1.0 oder DOT v1.0 in derselben Konfiguration in dieselbe Richtung zeigen (Cross-Coin-Zusammenfassung v1: E-D nur längere Haltedauer, E0 beste Capture, DOT D1 T0/E-U MP). Keine Validation aus Stufe B allein, kein Sleeve. Keine Regeländerung nach Sicht auf Outcomes.

## 6. Die drei Fragen des Laufs

A. Liefert T0 ohne Bestätigung auf Y1 und Y3 je Kandidat mehr als TA (Stufe A) und als TB, und wie viel Trend Capture kostet die Bestätigung (Einstieg relativ zum ex-post Tief in ATR)? B. Ist der Exit-Horizont das Problem: erreicht E-D oder E0 auf denselben Einstiegen eine höhere Capture und weniger abgeschnittene Trends als E-U? C. Ist eine der drei Familien mit T0/E-U gegen Kontrollen mechanistisch vielversprechend, und stimmt die Richtung mit XRP v1.0 und DOT v1.0 überein?

## 7. Scripts

`00_gemeinsam/rlib/count_btc_b.py` (aus `count_cross.py`, Änderungen: Modus `cfg_btc_stufeA`, Präfix Y, Coverage-Diagnose ATR-Form, keine Inkrement-Teilmengen), `00_gemeinsam/rlib/eval_btc_b.py` (aus `eval_cross.py`, Änderungen: Modus, Präfix, Pfade, keine Inkremente). Alle übrigen Zeilen identisch mit den für XRP und DOT gelaufenen Skripten (17d7cb93…, 3975f2b2…), Diff im Freeze-Eintrag dokumentiert.

## 8. Outcome-blinde Zählung (Befund vor dem Freeze, `count_BTC_B/count_BTC_B.json`)

Berechnet ausschliesslich Kandidatenkerzen, Trigger-Kerzen, Eröffnung der Einstiegskerze, initialer Stop (Zulässigkeit) und strukturelle Kontrollen ohne Positionsausschluss (Obergrenzen). Keine Exits, keine Post-Entry-Renditen, keine MFE/MAE.

Kerzen 13950, auswertbar 13816 ab 2017-09-08 16:00 UTC, Blöcke P1 7380, P2 6570. Coverage: K1 (12 Prozent) 35.2 Prozent der auswertbaren Kerzen, ATR-Form zur Diagnose 43.4 Prozent, K1 und K2 2539 Kerzen, 169 K1-Episoden, Kontextkerzen 1842 (P1 948, P2 894). Kandidaten identisch mit Stufe A: Y1 96 (P1 53, P2 43, Niveaus nbar 28, zone 27, swing 14, swing|nbar 11, swing|zone 9, nbar|zone 5, alle drei 2, 8 mit Lücke im Fenster, 306 Failed Breakdowns ohne Kontext), Y2 14 (P1 8, P2 6, aus 425 Paaren, 377 ohne Kontext, 249 Duplikate, 9 Triple), Y3 29 (P1 15, P2 14, 61 ohne Kontext). Überlappung Y1 und Y3 23, Vereinigung 116.

Einstiege je Trigger (Obergrenze ohne Positionsausschluss): Y1 T0 95 (1 Stop über 3 ATR), Stopdistanz Median 1.38 ATR; Y1 TA 18 (73 ohne Trigger, 5 Stop über 3 ATR), Median 1.89 ATR; Y1 TB 72 (16 ohne Trigger, 8 Stop über 3 ATR), Median 1.55 ATR. Y2 Nackenlinie 14, Median 4.75 ATR (3.11 bis 7.31). Y3 T0 27 (2 Stop über 3 ATR), Median 1.99 ATR; Y3 TA 6 (19 ohne Trigger, 4 Stop über 3 ATR), Median 2.66; Y3 TB 17 (6 ohne Trigger, 6 Stop über 3 ATR), Median 2.31.

Kontrollpool 1666 (P1 851, P2 815), identisch mit Stufe A. Matching Obergrenze: Y1 89 von 96 mit mindestens einer Kontrolle, 69 mit drei, im Mittel 2.43, 197 verschiedene Kontrollkerzen, 28 mehrfach verwendet, Median Poolgrösse 12, nach Jahr 2017 2, 2018 30, 2019 13, 2020 2, 2021 23, 2022 15, 2023 4. Y2 13 von 14, 8 mit drei. Y3 22 von 29, 14 mit drei, Median Poolgrösse 5.

Was vor dem Lauf feststeht: Nur Y1 T0 (bis 95 Einstiege, nach Positionsausschluss voraussichtlich 70 bis 85) und Y1 TB (bis 72) erreichen die Mindestzahl 30. Y3 T0 (27) liegt in der Low-Frequency-Stufe, Y2 (14) und alle TA-Zellen bleiben deskriptiv. Die Erwartung je Kandidat auf Y1 hat 96 Kandidaten als Nenner in allen drei Triggern.

Prüfsummen der Zählung: Spot 2d394fd1cbc344d5…, Flow (geladen, nicht ausgewertet) siehe JSON, rlib f1ffdbb81cad3115…, ylib 7f0230c938bc31ba…, Kandidatendateien siehe JSON.
