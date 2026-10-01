# REBOUND-MICRO — Spezifikation Version 1.0 (Freeze vor Outcome)

**Project Aurum II, `01_forschung/10_rebound_micro/rebound_micro_spec_v1.0.md`. 18.09.2026. Diese Spezifikation friert den einmaligen Development-Lauf auf BTC, XRP und DOT ein. Sie fasst Forschungsplan v0.1, 1h-Feature-Spec v0.1, Equilibrium-Target v0.1, Promotion-Regeln v0.1, Trial-Accounting v0.1, den outcome-blinden Vorbericht v0.1 (mit Erratum aus dem Execution-Cost-Audit v1) und die fünf Entscheidungen des STOP-GATE vom 18.09.2026 zusammen. Nach dem SHA-256-Eintrag in `00_doku/ENTSCHEIDE.md` wird nichts mehr geändert. Development Evidence, Ebene C (outcome-informed Hypothese nach REBOUND-20). ETH und SOL bleiben unberührt. Bisher eingefrorene Ergebnisse (Stufe 1, Stufe 2, MTP, YAMATO Stufe A, XRP v1.0, DOT v1.0, REBOUND-20-Closure) bleiben unverändert.**

## 1. Fünf Entscheidungen des STOP-GATE (bindend)

1. **Primary-Matrix auf M1 beschränkt.** Formale Primary-Hypothesen je Coin sind ausschliesslich M1×Q0 und M1×Q1. Holm-Korrektur über diese zwei Tests je Coin. Begründung outcome-blind: M2 und M3 haben unter 10 enge Fälle je Coin (Vorbericht Abschnitte 4 und 13). M2 und M3 werden vollständig simuliert und berichtet, aber ausschliesslich mit Status `descriptive / insufficient sample`. Sie werden nicht gelöscht, nicht als negative Ergebnisse umetikettiert, und es gibt keine weitere Schwellen- oder Feature-Suche für M2 und M3.
2. **Flow-Inkrement.** Der nested Flow-Vergleich auf M1 wird vor Freeze als `insufficient coverage — not formally testable in v1.0` festgehalten (Flow-Transition vor M1 bei 2 von 98, 2 von 79, 2 von 46). Flow-Flags und M3 werden deskriptiv berichtet. Keine Änderung der Flow-Definition, keine Suche nach lockereren Schwellen.
3. **Kosten.** K1 ist alleiniger Primary-Kostenmassstab. K0 und K2 sind ausschliesslich Sensitivität. Ein Maker- oder Limit-Execution-Test wäre eine separate outcome-informed Execution-Hypothese mit eigener Vorregistrierung und wird in v1.0 nicht eingeführt. Für Q0 und Q1 wird keine Maker-Gutschrift unterstellt. Die Promotion-Regel bleibt unverändert. Der Execution-Cost-Audit v1 hat PASS ergeben.
4. **Baseline exakt gepaart.** Baseline T0 auf denselben qualifizierten 4h-Kontext-Events wie der M1-Fall: Einstieg an der ersten handelbaren 1h-Eröffnung nach Abschluss der Kontextkerze, ursprünglicher 4h-struktureller Stop (Kontexttief minus 0.5 ATR14(4h) der Kontextkerze), dieselben Q0/Q1-Zieldefinitionen, derselbe Zeitstopp (24 1h-Kerzen), dasselbe Kostenmodell. Der Vergleich isoliert «unmittelbare Context-Execution» gegen «Abwarten des 1h Failed-Breakdown/Reclaim mit strukturell näherem Stop». Wo M1 nicht auftritt, wird kein künstliches M1-Paar erzeugt. Gepaarte Vergleiche nur auf Kontext-Events, auf denen beide Trades existieren.
5. **Exit.** Zeitstopp nach 24 vollständig abgeschlossenen 1h-Kerzen. Q0 = der zum Einstieg bereits bekannte EMA20(4h)-Wert als fester Preislevel, die EMA20 wird während des Trades nicht nachgeführt. Q1 = eingefrorener Anchored-VWAP-Level gemäss `equilibrium_target_research_v0.1.md`. Keine Zieländerung nach Einstieg.

## 2. Bibliotheken und Daten

`mlib.py` v1.0 (Erweiterung von v0.1 um den optionalen Parameter `ctx_override` in `join_4h` für die Kontrollgruppe, Standardverhalten unverändert, Regression: Kandidatentabellen aller drei Coins byteidentisch mit der Zählung v0.1), `rlib.py` v1.0 (unverändert, `cfg_alt`), `ylib.py` (unverändert). Neu: `simulate_micro.py` v1.0 (Trade-Simulation, Baseline, Kontrollen, Lauf je Coin) und `eval_micro.py` v1.0 (Auswertung, Bootstrap, Holm, Promotion-Prüfung). Tests `tests/test_mlib.py` (5, unverändert) und `tests/test_simulate.py` (synthetische Pfade: Ziel, Stop, Gap-Stop, gleichzeitige Berührung, Zeitstopp, Datenende, Gebühren von Hand). Daten: Binance Spot 1h Discovery (SHA im Datenaudit v0.1), 4h-Discovery-Dateien aus dem Holdout-Manifest v1.1. Discovery-Guard: keine Datei mit `validation` im Namen wird geladen.

## 3. Kandidaten (unverändert aus v0.1)

Kontext, Suchfenster, Mechanismen M1, M2, M3, Stop-Definitionen, enger Invalidationspunkt (Einstieg minus Stop ≤ 1.0 ATR14(4h)), erster Kandidat je Event und Mechanismus, Lückenregel, Flow-Flag, Q0 und Q1 exakt wie `rebound_micro_research_plan_v0.1.md` Abschnitte 3 bis 5 und `mlib.candidates`. Die Kandidatentabelle des Laufs muss mit `count/count_{COIN}.csv` der outcome-blinden Zählung identisch sein (Prüfung im Lauf, Abbruch bei Abweichung).

Zulassung zum Trade je Zelle: Kandidat in vollständigem Fenster, `valid_stop`, `tight`, Ziel der Zelle über dem Einstiegspreis (`q_above`), und keine offene Position derselben Zelle zum Einstiegszeitpunkt (`overlap_skip`, gezählt). Kandidaten mit Ziel unter oder gleich dem Einstieg sind `target_below_entry` (gezählt, nicht gehandelt).

## 4. Trade-Simulation (1h, Long, identisch für Zellen, Baseline und Kontrollen)

Einstieg: Eröffnung der Einstiegskerze e, Fill = open[e] × (1 + slip_in). R = Fill − Stop. Zulassung verlangt open[e] > Stop (`valid_stop`), eine Eröffnung auf oder unter dem Stop ist nicht handelbar (`invalid_stop`, gezählt).

Haltefenster: Kerzen e bis e+23 (24 abgeschlossene Kerzen). Je Kerze b in dieser Reihenfolge geprüft:

1. open[b] ≤ Stop (b > e): Ausstieg open[b] × (1 − slip_sl), `stop_gap`.
2. low[b] ≤ Stop und high[b] ≥ Ziel in derselben Kerze: konservativ Stop, Ausstieg Stop × (1 − slip_sl), `stop_ambiguous` (gezählt und separat berichtet).
3. low[b] ≤ Stop: Ausstieg Stop × (1 − slip_sl), `stop`.
4. open[b] ≥ Ziel (b > e): Ausstieg open[b], `target_gap` (Limit wird an der Eröffnung besser gefüllt, keine Slippage).
5. high[b] ≥ Ziel: Ausstieg exakt Ziel, `target`, keine Slippage.

Kein Ausstieg bis e+23: Ausstieg open[e+24] × (1 − slip_in), `time24`. Endet die Discovery-Datei vorher: Ausstieg close der letzten Kerze × (1 − slip_in), `cut`. Gebühren: (Fill Einstieg + Fill Ausstieg) × (fee + fric). r_net = (Ausstieg − Einstieg − Gebühren) / R. Kosten je Trade in R = (Gebühren + Einstiegs-Slippage (Fill − open[e]) + Ausstiegs-Slippage (Referenzpreis − Fill, Referenz = Stop beziehungsweise Eröffnung bei Stop- und Zeitausstieg, 0 am Ziel)) / R, berichtet als `cost_R`. Kein Chandelier, kein Strukturbruch, kein Scale-out, kein Nachführen des Ziels. K0, K1, K2 nach `mlib.COST` (K1 Gebühr 0.40 Prozent je Seite, Reibung 0.02, Slippage 0.05 Einstieg und 0.10 Stop, Ziel ohne Slippage).

## 5. Baseline (gepaart)

Je Kontext-Event mit Kontextkerze t4 (4h): Einstiegskerze eb = erste 1h-Kerze mit Beginn = Ende der Kontextkerze (Eröffnung der 4h-Kerze t4+1). Stop = low4[t4] − 0.5 × ATR14(4h)[t4]. Q0 = EMA20(4h) am Schluss von t4. Q1 = AVWAP der laufenden K1-Episode vom Anker bis zur letzten 1h-Kerze der Kontextkerze (Schluss vor eb). Ist die Kontextkerze selbst die Anker-4h-Kerze, ist der Anker an ihrem Schluss bekannt und der AVWAP über ihre vier 1h-Kerzen definiert (identisch mit der Library-Regel «Anker bekannt am Schluss der Anker-4h-Kerze»). Zeitstopp 24 1h-Kerzen, Kosten identisch, Overlap-Regel identisch (eine offene Baseline-Position je Ziel). Die Baseline wird auf allen vollständigen Kontext-Events simuliert und standalone berichtet. Der Primary-Vergleich ist die gepaarte Differenz r_net(Zelle) − r_net(Baseline, gleiches Ziel) je Kontext-Event, ausschliesslich auf Events, auf denen beide Trades existieren (M1 eng und Ziel über beiden Einstiegen, beide nicht `overlap_skip`). Anzahl der ungepaarten Events wird berichtet.

## 6. Kontrollgruppe (Diagnose)

Wie Forschungsplan Abschnitt 8: dieselben 1h-Mechanismen in Suchfenstern von 4h-Kerzen mit K1 und K2, aber ohne K3, gematcht mit `rlib.match_controls` (cfg_alt: Fenster ±540 4h-Kerzen, `dd120_atr` ±1.5, `ext`-Toleranz wie cfg_alt, bis zu drei je Event, ausserhalb aller echten Event-Fenster). Kontroll-Trades mit identischer Simulation. Berichtet: Mittel und Median r_net der Kontrollen je Zelle, Differenz Zelle minus Kontrollmittel je Event. Kein Promotion-Kriterium, keine Statuswirkung.

## 7. Primary-Tests und Multiplizität

Je Coin zwei Primary-Tests, je einer für M1×Q0 und M1×Q1: H1 «gepaarte Differenz gegen Baseline hat positiven Mittelwert». Teststatistik: Bootstrap-Verteilung des Mittels der gepaarten Differenzen (2000 Resamples, Seed 20260918), p = Anteil der Resample-Mittel ≤ 0 (einseitig). Holm über die zwei Tests je Coin bei α = 0.05. Zusätzlich berichtet: Median der Differenz, Anteil positiver Paare, Vorzeichentest, Wilcoxon-Vorzeichenrangtest. Kein Pooling über Coins.

## 8. Berichtsgrössen je Zelle und Coin (nach K1, mit K0 und K2 als Sensitivität)

n, Zielrate, Stoprate (getrennt `stop`, `stop_gap`, `stop_ambiguous`), Zeitstopp-Anteil, avg_win_R, avg_loss_R, Verhältnis avg_win/|avg_loss|, p_BE_emp = |avg_loss| / (avg_win + |avg_loss|), Trefferquote (r_net > 0), Mittel und Median r_net, Bootstrap p_pos (Anteil positiver Resample-Mittel), Profit Factor, cost_R Median, Median entry_to_stop_ATR(4h), grösster Einzelgewinn als Anteil der Gewinnsumme, Vorzeichen des Mittels ohne den besten Trade, Blöcke (P1/P2 für BTC und XRP, P2a/P2b für DOT) mit n und Mittel, Anteil Stop-outs, nach denen das Ziel innerhalb von 24 Kerzen dennoch erreicht wird (Diagnose), MFE nach erreichtem Ziel bis 24 Kerzen und neues 20- und 30-Tage-Hoch innerhalb 30 Tagen nach Ziel (Diagnose Rebound gegen Trend). Für M1 zusätzlich: Flow-Flag-Teilmenge deskriptiv, Harami- und Hikkake-Teilmengen deskriptiv.

## 9. Promotion-Regel (unverändert, `rebound_micro_promotion_rules_v0.1.md`)

Eine Zelle (M1×Q0 oder M1×Q1) auf mindestens zwei der drei Coins gleichzeitig: avg_win/|avg_loss| ≥ 0.80 und Median entry_to_stop_ATR(4h) ≤ 0.60, p_BE_emp ≤ 0.60, Mittel r_net K1 ≥ −0.05 R mit p_pos ≥ 0.40 und PF ≥ 0.90, mindestens 30 Trades und mindestens 30 erwartete Trades auf ETH und SOL (Kandidatenrate je 1000 auswertbare 1h-Kerzen mal ETH- beziehungsweise SOL-Discovery-Länge), grösster Gewinn ≤ 40 Prozent der Gewinnsumme mit stabilem Vorzeichen, zwei Blöcke mit je ≥ 10 Trades und Mittel ≥ −0.05 R, gepaarte Differenz gegen Baseline mit Median > 0 und Anteil positiver Paare ≥ 0.55. M2- und M3-Zellen können nicht promoviert werden (Entscheidung 1). Promotion erlaubt nur eine ETH/SOL-Vorregistrierung, keine Validation, keinen Sleeve.

## 10. Statuszuweisung und die drei Fragen des Laufs

Governance v1.1: Zellen mit ≥ 30 Trades normal, 20 bis 29 Low-Frequency-Evidenz höchstens MP, unter 20 deskriptiv. Regel v2 (≥ 3 von 4) für «mechanistisch vielversprechend», hier vorab so abgebildet: (a) gepaarte Differenz gegen die 4h-Baseline (der vorregistrierte Vergleich dieses Designs) Median > 0 mit ≥ 60 Prozent positiven Paaren, (b) Geometrie-Verbesserung avg_win/|avg_loss| ≥ 0.80 (an Stelle von MFE/Capture, weil hier ein festes Ziel gilt), (c) grösster Gewinn ≤ 40 Prozent der Gewinnsumme mit stabilem Vorzeichen, (d) mindestens zwei Blöcke mit je ≥ 5 Trades und gleichem Vorzeichen wie das Gesamtmittel. Fast Fail: Median der gepaarten Differenz < 0 und < 40 Prozent positive Paare bei ≥ 10 Paaren. Die gematchte Kontrollgruppe (Abschnitt 6) wird zusätzlich berichtet, entscheidet aber nicht. Economic Validation Gate §7 gilt für jede spätere Validation.

Der Lauf beantwortet je Coin: A. Verbessert M1 die tatsächliche Reward/Loss-Geometrie gegenüber T0 (avg_win/|avg_loss|, p_BE_emp, gepaarte Differenz vor Kosten K0)? B. Überlebt diese Verbesserung reale K1-Kosten (Mittel r_net K1, gepaarte Differenz K1)? C. Liefert Q1/AVWAP einen wirtschaftlich besseren Rebound als Q0/EMA20 (Mittel r_net und Zielrate beider Zellen, gleiche Trades)? Falls A ja und B nein: Signalmechanik und Execution Economics werden ausdrücklich getrennt beurteilt, eine spätere Maker-/Execution-Hypothese ist zulässig, aber nur als neue Vorregistrierung. Falls A und B nein: REBOUND-MICRO wird nicht auf ETH/SOL verfolgt («Spezifikation abgeschlossen, keine Fortführung»).

## 11. Ablauf

Freeze (SHA-256 dieser Spezifikation, `mlib.py` v1.0, `simulate_micro.py`, `eval_micro.py`, Tests, Cost-Audit) in ENTSCHEIDE.md, Prüfsummenvergleich Mac↔Projekt. Dann einmaliger Lauf BTC, Versiegelung der Ergebnisdateien (SHA in ENTSCHEIDE.md), dann XRP, Versiegelung, dann DOT, Versiegelung. Keine Regeländerung zwischen Coins. Abschliessend Cross-Coin-Bericht ohne Pooling-Statistik. Jeder Lauf schreibt `run/{COIN}_trades.csv`, `run/{COIN}_baseline.csv`, `run/{COIN}_controls.csv`, `run/{COIN}_eval.json`, `run/{COIN}_run.log` mit SHA aller Eingaben.

## 12. Erratum-Referenz

Die Kostenvergleichswerte in Abschnitt 8 des Vorberichts v0.1 waren über M1, M2 und M3 zusammen gerechnet, siehe `rebound_micro_execution_cost_audit_v1.md` Abschnitt 6. Für die Primary-Zellen (M1) gelten: cost_R K1 Median 0.90 / 0.88 / 0.78 (BTC / XRP / DOT), p_BE_geo Q0 K1 0.64 / 0.58 / 0.59, p_BE_geo Q1 K1 0.35 / 0.28 / 0.32.
