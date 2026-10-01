# DELAYED-TREND — Messregeln für die outcome-blinde Geometrie, Version 1.0 (fixiert vor der Messung)

**Project Aurum II, `01_forschung/11_delayed_trend/delayed_trend_measurement_spec_v1.0.md`. 19.09.2026. Setzt Forschungsplan v0.1 (SHA 0241c247…) und die Nutzerentscheidungen vom 19.09.2026 um. Fixiert vor der ersten Berechnung. Development auf BTC, XRP, DOT, ETH/SOL unberührt. Es wird nichts berechnet, was nach der Einstiegskerze liegt: keine Exits, keine Post-Entry-Renditen, kein r_net, keine MFE/MAE, keine Stop- oder Zieltreffer, keine Trefferquoten, keine Kursentwicklung nach Einstieg. Library `dtlib.py` v1.0 auf rlib v1.0 (f1ffdbb8…) und ylib (7f0230c9…).**

## 1. Daten und Modus

4h-Discovery-Dateien aus dem Manifest v1.1 (BTC 2d394fd1…, XRP 6fda0931…, DOT 426b5ae7…), Validation-Guard aktiv. Kontextquellen aus den eingefrorenen Kandidatentabellen: BTC `06_btc_specialist/stufeB/count/` (Modus `cfg_btc_stufeA`, identisch mit Stufe A), XRP `04_xrp_specialist/count/`, DOT `05_dot_specialist/count/` (Modus `cfg_alt`). Prüfsummen werden im Lauf gegen die jeweiligen count-JSON geprüft. ATR14 = Wilder-ATR der Library, ATR14_t bezeichnet den Wert an der Kontextkerze, ATR14_e den an der Kerze vor der Einstiegskerze (e−1, vollständig bekannt). Blöcke wie rlib.BLOCKS.

## 2. Kontextquellen (getrennte Familien)

S1 Double Bottom: jedes Y2/X2/D2-Paar mit `y2 = True` (gültig nach Zeitordnung, Kontext auf s2). Kontextkerze t = Bruchkerze (erster Schluss über der Nackenlinie N). L_ref = L_{s2}. Level P = N. Referenzkerze für das Trendziel: s2.
S2 Failed Breakdown: jede Y1/X1/D1-Kandidatenkerze (`y1 = True`, Kontext erfüllt). Kontextkerze t = Kandidatenkerze. L_ref = L_t (das Sweep-Tief der Kandidatenkerze, identisch mit der Stop-Referenz der eingefrorenen Specs). Level P = `tb_lvl_y1` (höchstes getroffenes Niveau). Referenzkerze für das Trendziel: t.

Kontextzustand `bullish_trend_context_active` von t+1 bis einschliesslich t+180 (30 Tage). Vorzeitiges Ende: erste Kerze k > t mit C_k < L_ref (Invalidierung), danach kein Einstieg aus diesem Kontext, eine Einstiegskerze e muss e ≤ k erfüllen (Eröffnung der Invalidierungskerze ist noch handelbar, weil die Invalidierung erst an ihrem Schluss bekannt ist). Nach t+180 verfällt der Kontext. Jeder Kontext wird unabhängig geführt, auch bei Überlappung mit anderen Kontexten derselben Quelle; die Überlappung von Einstiegen (Einstieg innerhalb von 180 Kerzen nach dem vorigen Einstieg derselben Zelle) wird gezählt und berichtet, nicht ausgeschlossen (Positionsausschluss braucht Exits, deshalb Obergrenze).

## 3. Trendziel für die geometrische Prüfung (pre-selloff high)

H_pre = max(H, r−120 .. r−1) mit r = Referenzkerze (s2 bei S1, t bei S2). Das ist exakt das `hh120` der Library, das in K1 (`dd120`) verwendet wird, also das Hoch, gegen das der Selloff gemessen wurde. Es ist am Schluss der Kerze r vollständig bekannt und wird nicht verändert. Lookback 120 Kerzen (20 Tage), keine Alternative. Existiert es nicht (r < 121, Vorlauf), ist der Kontext für die Geometrie `no_target` und wird gezählt, nicht gemessen. Liegt H_pre ≤ Einstiegspreis, ist RR_geo ≤ 0, der Fall wird als `target_below_entry` gezählt und geht mit RR_geo = 0 in die Verteilung ein (konservativ, weil ein Trade über dem Vor-Selloff-Hoch den laufenden Trend handelt, das Ziel dieser Prüfung aber die Rückkehr zum Hoch ist).

## 4. Entry-Familien (ATR-Toleranzen mit ATR14_t, Stops mit ATR14_e)

Gemeinsam: Suchbereich t+1 bis t+180, Einstieg nur, wenn e ≤ Invalidierungskerze und e ≤ t+180 und e < n. Einstiegspreis = O_e (Roh, Slippage im Kostenmodell). Je Kontext und Familie nur der erste gültige Einstieg. Kein Einstieg, wenn O_e ≤ Stop (`entry_below_stop`, gezählt).

DT1 Higher Low: Bestätigtes Swing Low s (L_s strikt unter den drei Tiefs davor und den drei danach, bekannt am Schluss von s+3, `ylib.swings`) mit t < s, s+3 ≤ t+180, L_s ≥ L_ref + 0.5 · ATR14_t, und H_mid = max(H, t .. s) ≥ L_s + 1.0 · ATR14_t (das Swing Low ist ein Rücksetzer nach einem Anstieg, kein Rauschen). Zusätzlich darf zwischen t+1 und s+3 keine Invalidierung liegen. Einstieg e = s+4. Stop = L_s − 0.5 · ATR14_{s+3}. Erstes s, das alle Bedingungen erfüllt. Keine rückwirkende Erkennung: die drei rechten Kerzen sind vor e vollständig abgeschlossen.

DT2 Retest and Hold: Retest-Kerze b ≥ t+3 mit L_b ≤ P + 0.25 · ATR14_t und C_b ≥ P − 0.5 · ATR14_t. Hold-Kerze b+1 mit C_{b+1} > P (genau eine vollständig abgeschlossene Kerze, keine zweite). Einstieg e = b+2. Stop = min(L_b, L_{b+1}) − 0.5 · ATR14_{b+1}. Gescheiterter Retest (erste Kerze b ≥ t+3 mit L_b ≤ P + 0.25 · ATR14_t und C_b < P − 0.5 · ATR14_t, bevor ein Hold zustande kam) beendet die Familie für diesen Kontext (`retest_failed`). Scheitert nur der Hold (C_{b+1} ≤ P, ohne dass b+1 selbst ein gescheiterter Retest ist), wird die nächste Retest-Kerze gesucht; die Anzahl gescheiterter Holds vor dem Einstieg wird berichtet. Dokumentiert: Der reine Retest trat in DB-CONTEXT in 87 bis 94 Prozent der Fälle nach im Median 3 Kerzen auf und ist kein Filter; der Mechanismus ist der Hold nach dem Retest.

DT3 Consolidation Breakout: Konsolidierungsbox = Kerzen t+1 .. t+18 (drei Tage, Mindestdauer). Bedingungen: box_high = max(H, t+1..t+18), box_low = min(L, t+1..t+18), box_high − box_low ≤ 3.0 · ATR14_t, box_low > L_ref (keine Invalidierung innerhalb der Box), und alle 18 Kerzen vor t+180 (immer erfüllt). Ist die Box breiter als 3.0 ATR, ist DT3 für diesen Kontext `no_consolidation`. Breakout-Kerze b ≥ t+19 mit C_b > box_high (Schluss, nicht Hoch). Einstieg e = b+1. Stop = box_low − 0.5 · ATR14_b. Genau eine Definition (18 Kerzen, 3.0 ATR, Schluss über Boxhoch), keine Suche.

## 5. Messgrössen je Einstieg (nur aus Kerzen ≤ e−1 und O_e)

delay = e − t (Kerzen, Tage = delay/6). stop_atr = (O_e − Stop) / ATR14_{e−1}. stop_pct = (O_e − Stop) / O_e · 100. cost_R_K1 = 99 bp / (stop_pct · 100 bp) (Stoppfad, Cost-Audit v1). dist_target_atr = (H_pre − O_e) / ATR14_{e−1}, dist_target_pct. RR_geo_gross = (H_pre − O_e) / (O_e − Stop), auf 0 begrenzt bei H_pre ≤ O_e. RR_geo_net_K1 = (H_pre − O_e − 0.0089 · O_e) / (O_e − Stop + 0.0099 · O_e). p_BE_geo = 1 / (1 + RR_geo_net_K1) bei RR > 0. Zusätzlich Anteil Einstiege bereits über dem Vor-Selloff-Hoch, Anteil Einstiege über dem Level P, Block, Jahr.

## 6. Berichtspunkte je Coin und Zelle S×DT (14)

1. Anzahl Kontext-Events (S1, S2), davon vor jedem Einstieg invalidiert, verfallen nach 180, `no_target`. 2. Anzahl gültiger Einstiege je Zelle. 3. Anteil Kontexte mit gültigem Einstieg. 4. Median, P25, P75 der Zeit Kontext → Einstieg. 5. stop_atr P25/Median/P75. 6. stop_pct P25/Median/P75. 7. cost_R_K1 P25/Median/P75. 8. dist_target_atr und dist_target_pct P25/Median/P75, Anteil `target_below_entry`. 9. RR_geo_gross und RR_geo_net_K1. 10. P25/Median/P75 RR_geo_gross. 11. Anteil Einstiege, die alle fünf Gate-Kriterien auf Einzelfallebene erfüllen (stop_atr ≤ 3.0, cost_R ≤ 0.40, RR_gross ≥ 1.5, sowie Zellenebene P25 und n). 12. Überschneidung DT1/DT2/DT3 je Kontext (gleicher Kontext mit Einstieg in mehreren Familien, gleiche Einstiegskerze). 13. Look-ahead-Prüfung (Abschnitt 8). 14. Erwartete Fallzahl eines späteren P&L-Laufs: Einstiege minus Überlappungen (Einstieg innerhalb 180 Kerzen nach dem vorigen der Zelle) als Untergrenze, Einstiege als Obergrenze, je Block, Hochrechnung ETH/SOL nach Kerzenzahl aus dem Manifest.

## 7. Economic Geometry Gate (Zellenebene, vorab, keine Änderung nach Sicht)

Zelle S×DT auf einem Coin darf in den Development-P&L-Lauf nur, wenn alle fünf gelten: A Median stop_atr ≤ 3.0; B Median cost_R_K1 ≤ 0.40; C Median RR_geo_gross ≥ 1.50; D P25 RR_geo_gross ≥ 1.00; E erwartete Einstiege (Untergrenze nach Abschnitt 6 Punkt 14) ≥ 20, sofern die Low-Frequency-Regel nichts Strengeres verlangt. Ökonomische Vorprüfung, kein erwartetes Ergebnis: bei gross RR 1.5 und 0.4 R Kosten Gewinner rund +1.1 R, Verlierer rund −1.4 R, Break-even-Trefferquote rund 56 Prozent. Multiplizität für einen späteren P&L-Lauf: Holm über die zulässigen Zellen je Coin, höchstens sechs, festgelegt vor Outcome.

## 8. Look-ahead-Prüfung

Synthetische Serie: Alle Einstiege mit e < T bleiben identisch (Kontext, Familie, e, Stop, Ziel), wenn alle Kerzen ≥ T gestört werden. Zusätzlich Handrechnung je Familie auf konstruierten Pfaden (DT1 Bestätigung erst an s+3, DT2 Hold-Kerze, DT3 Boxbreite und Schluss-Bedingung) und Regel «Invalidierung beendet den Kontext». Ergebnis im Bericht.

## 9. Was nicht berechnet wird

Kein Exit, kein r_net, keine MFE/MAE, kein Stop-Outcome, kein Zieltreffer, keine Trefferquote, kein Profit Factor, keine empirischen Gewinner oder Verlierer, keine Kursentwicklung nach e. Die Kandidatendateien enthalten keine dieser Spalten.
