# Regressionstest: Cross-Coin-Library rlib v1.0 gegen BTC YAMATO Stufe A (eingefroren)

**Project Aurum II, `01_forschung/00_gemeinsam/rlib/`. 17.09.2026, 22:05 bis 22:19 UTC. Ergebnis: REGRESSION PASS. Zweck: Nachweis, dass die neue Cross-Coin-Library im Modus «BTC Stufe A» die eingefrorenen Referenzergebnisse auf Ereignisebene exakt reproduziert, bevor sie auf XRP und DOT angewendet wird. Keine Referenzdatei wurde verändert.**

## 1. Prüfgegenstand

`rlib.py` (SHA f1ffdbb8…) setzt auf `ylib.py` (SHA 7f0230c9…, identisch mit dem Stufe-A-Stand 81a74f2a… bis auf die Ladesperre für Validation-Dateien aus Governance v1, keine Regeländerung) auf und fügt Konfigurationsmodi hinzu: K1 in ATR- oder Prozentform, Niveau-Penetration und `at_low_structure` in ATR- oder Prozentform, Matching-Toleranz in ATR- oder Prozentform, Trigger T0/TA/TB, Exits E-U/E-D/E0. Im Modus `cfg_btc_stufeA()` sind alle Modi auf «pct», Trigger TA, Exit E-U, also die eingefrorene Stufe-A-Spezifikation v1.1.

Referenz (eingefroren, Stufe A): `BTCUSDT_4h_discovery.csv` 2d394fd1…, `candidates_y1_y3.csv` c3bce1b9…, `candidates_y2.csv` e6c2726a…, `trades_Y1/Y2/Y3_K1.csv` b75ac230… / 322260ae… / 159e8b2a…, `controls_Y1/Y2/Y3_K1.csv` f395d485… / ab8db079… / ad56597…, `pairs_Y1/Y2/Y3.csv` 7db18f40… / e6ca4368… / cfcc412e…, `eval_stufeA.json` cd0135fe….

## 2. Vergleichsebenen und Regeln

Verglichen wurde auf der kleinsten Ebene, die die Referenz enthält. Ganzzahlen (Kerzenindizes t, s1, s2, h1, e, x, bars, sig_t, ctrl_t, n_ctrl) und Wahrheitswerte (ctx, y1, y3, fb_any, y3_any, triple, gyaku, dup, y2) exakt gleich. Textspalten (y1_levels, reason, status) exakt gleich nach Normalisierung von NaN und leerem Feld auf «» (Begründung Abschnitt 4). Gleitkommazahlen (Niveaus, Nackenlinie, Einstiegspreis, Stop, R, Exitpreis, r_net, r_gross, mfe_r, mae_r, stop_dist_atr, d_r) mit Toleranz 1e-9, die einzige verwendete Toleranz. Sie ist technisch zwingend, weil die Referenz als CSV vorliegt und der Weg float64 → Text → float64 die letzten Stellen rundet. Beobachtete maximale Abweichung über alle Gleitkommaspalten: 7.276e-12 (Preise um 60000 USD, also die 16. signifikante Stelle). Zusätzlich die aggregierten Kennzahlen aus `eval_stufeA.json`: n und mittleres r_net je Kostenmodell K0, K1, K2 auf drei Dezimalen, matched und traded der Kontrollen.

Ausdrücklich nicht verglichen, weil nicht Bestandteil der eingefrorenen Referenz: Bootstrap-Intervalle (seedabhängig, in der Referenz nur als Aggregat) und die Diagnosemetriken aus `eval_stufeA.py` (entry_eff, capture, Klassifikation), die nicht in rlib reimplementiert sind, sondern im Auswertungsskript bleiben.

## 3. Ergebnis (Lauf 2, 387 Sekunden, `regress_btc.log` SHA cf5fc1e8…, `regress_btc_result.json` SHA cbff3fcb…)

205 Prüfungen, 205 bestanden, 0 Abweichungen.

Kandidaten Y1/Y3: 13816 ausgewertete Kerzen, Kontext, Y1 (96), Y3 (29), Failed-Breakdown- und Y3-Flags ohne Kontext, drei Niveaus je Kerze und getroffene Niveaus je Y1-Kandidat identisch. Kandidaten Y2: 425 Paare mit t, s1, s2, h1, Nackenlinie, Kontext, Triple, 逆三尊, Duplikat und Y2-Flag identisch, 14 gültige. Trades K1: Y1 16, Y2 14, Y3 6, je Einstiegskerze, Exitkerze, Haltedauer, Exitgrund, Einstiegspreis, Stop, R, Exitpreis, r_net, r_gross, MFE, MAE, Stopdistanz identisch. K0 und K2: n und Mittelwert identisch. Kontrollen: alle Zeilen (Y1 37, Y2 32, Y3 6) mit Signalkerze, Kontrollkerze und Status identisch, gehandelte (9, 7, 1) auf allen Preis- und R-Spalten identisch. Gepaarte Differenzen d_r (8, 6, 1) identisch.

## 4. Technische Provenance: Lauf 1 und Vergleichsartefakt

Lauf 1 (`regress_btc_run1_FAIL_vergleichsartefakt.log`, SHA 16550cef…) meldete 204 von 205 Prüfungen bestanden und einen FAIL auf der Textspalte `y1_levels`. Ursache, lokalisiert vor jeder Änderung: Die Referenz-CSV liest leere Felder als NaN, die Neuberechnung hält leere Strings, und der Vergleich per `astype(str)` stellte «nan» gegen «». Nach Normalisierung beider Seiten auf «» sind 0 von 13816 Zeilen verschieden, beide Seiten haben exakt 13414 leere Felder. Es handelte sich um ein Artefakt der Vergleichsmethode, nicht um eine Abweichung der Library. Korrigiert wurde ausschliesslich die Vergleichsfunktion im Testskript (`regress_btc.py` SHA ccd98bed…), keine Referenzdatei, keine Library. Lauf 2 wurde vollständig neu ausgeführt, damit die Evidenz ein einziges, reproduzierbares Ergebnis ist. Ein noch früherer Startversuch am Abend wurde durch einen Neustart der Rechenumgebung ohne Ausgabe abgebrochen (leere Protokolldatei), er hat keine Datei erzeugt.

## 5. Unit- und Look-ahead-Tests der neuen Modi (`tests/test_rlib.py`, SHA 09161614…)

Sieben Tests bestanden auf synthetischen Daten ohne Marktbezug: ATR-Form von K1 gegen die Formel und Prozentform gegen die alte Definition, `at_low_structure` in ATR-Form, Penetration 0.05 ATR (0.06 ATR trifft, 0.04 ATR nicht), Trigger T0 (t+1), TB (Reclaim innerhalb sechs Kerzen, Einstieg danach, kein Reclaim → kein Einstieg, kein Niveau → kein Einstieg), E-D verwendet nur abgeschlossene Tage (Störung des laufenden Tages ändert Tages-ATR nicht), E0 endet an EMA20 oder nach 30 Kerzen, und ein Permutations-Look-ahead-Test: Störung aller Kerzen nach T ändert keine Kandidaten und keine Trades, die vor T abgeschlossen sind, für die Kombinationen T0/E-U, TB/E-U, T0/E-D, T0/E0.

## 6. Reproduktion

`python3 regress_btc.py` im Verzeichnis der Library mit den Referenzpfaden aus Abschnitt 1. Laufzeit rund 6.5 Minuten. Ausgabe `regress/regress_btc_result.json` mit Urteil, allen 205 Prüfungen, Prüfsummen der Eingaben und der erzeugten Vergleichsdateien.
