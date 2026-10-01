# DELAYED-TREND — Forschungsplan, Version 0.1 (nur Spezifikation, kein Backtest)

**Project Aurum II, `01_forschung/11_delayed_trend/delayed_trend_research_plan_v0.1.md`. 19.09.2026. Status: Entwurf zur Prüfung, kein Freeze, keine Zählung, kein Outcome. Neue Architektur, keine Rebound-Version und keine Reparatur: REBOUND (REBOUND-20, REBOUND-MICRO) bleibt geschlossen, kein EMA20-Ziel, kein Versuch, den ersten Bounce zu monetarisieren. Hypothese outcome-informed, Ebene C, aus den eingefrorenen Läufen auf BTC, XRP und DOT (YAMATO Stufe A und B, XRP v1.0, DOT v1.0, REBOUND-MICRO v1.0). Deshalb: BTC, XRP, DOT = Development Evidence. ETH und SOL bleiben unabhängige Generalisierungsmärkte, keine ETH- oder SOL-Daten werden geladen. Bis zur Freigabe dieses Plans wird nichts gerechnet, auch keine outcome-blinde Zählung.**

## 1. Ausgangshypothese

Bottom- und Double-Bottom-Strukturen nach einem Selloff liefern möglicherweise Information über einen späteren Trend, aber nicht über einen unmittelbaren Rebound. Belege aus den eingefrorenen Development-Läufen: Nach bestätigten Double Bottoms entsteht innerhalb 60 Tagen in 47 bis 71 Prozent der Fälle ein neues 20-Tage-Hoch (Kontrollen 34 bis 35 Prozent), im Median nach 12 bis 34 Tagen; nach Failed-Breakdown-Kandidaten mit T0 in 21 bis 28 Prozent (BTC Stufe B), nach REBOUND-MICRO-Zieltreffern in 35 bis 55 Prozent. Jeder bisher getestete Trade ab dem ersten Reversal (Chandelier 3 ATR14 auf 4h, festes Ziel auf 4h oder 1h) endete vor diesem Trend, in 16 bis 50 Prozent der Fälle nachweislich abgeschnitten, und war netto negativ. Der Bottom erzeugt deshalb in dieser Architektur keinen Trade, sondern ausschliesslich einen Zustand: `bullish_trend_context_active = true`. Ein Trade entsteht erst, wenn innerhalb dieses Kontexts eine neue Trendstruktur algorithmisch sichtbar ist.

Primäre Forschungsfrage, ausdrücklich nicht «steigt der Markt irgendwann später», sondern: Kann ein verzögerter Einstieg die spätere Trendinformation in einen Trade mit wirtschaftlich brauchbarer Einstiegs-, Stop- und Kostengeometrie übersetzen? Die Frage wird zuerst outcome-blind beantwortet (Abschnitt 6), und eine Entry-Familie geht nur dann in einen P&L-Lauf, wenn ihre Geometrie das Economic Gate (Abschnitt 7) besteht.

## 2. Verhältnis zu bestehenden Spezifikationen

DB-CONTEXT v0.1 für ETH und SOL (`07_eth_sol_specialist/eth_sol_double_bottom_context_prereg_v0.1.md`, nicht eingefroren) enthält bereits drei Einstiegsmechanismen auf dem Double Bottom (Retest, Higher Low, Konsolidierungsbreakout) und die Development-Häufigkeiten ohne Trades. DELAYED-TREND verallgemeinert diesen Ansatz (Kontextquelle nicht nur Double Bottom, Geometrie vor Outcome, Economic Gate vor P&L) und kehrt die Reihenfolge um: erst Development auf BTC/XRP/DOT, dann eine ETH/SOL-Vorregistrierung mit der überlebenden Familie. Das widerspricht der Klausel in DB-CONTEXT Abschnitt 5 («kein Rückgriff auf BTC-, XRP-, DOT-Outcomes der drei Mechanismen»). Vorschlag: DB-CONTEXT v0.1 wird durch DELAYED-TREND ersetzt und nicht eingefroren, die ETH/SOL-Vorregistrierung wird nach dem Development neu geschrieben (Entscheidung 2 in Abschnitt 10). YAMATO, XRP v1.0, DOT v1.0 und REBOUND bleiben unverändert, ihre Kandidatendefinitionen werden hier nur als Kontextquellen wiederverwendet, nicht verändert.

## 3. Kontextquellen (Bottom Engine, Erkennungsschicht)

Alle Definitionen wörtlich aus den eingefrorenen Spezifikationen (rlib v1.0, Modus `cfg_btc_stufeA` für BTC, `cfg_alt` für XRP und DOT, keine neue Konstante). Kontextkerze t und Referenztief L_ref:

S1 Double Bottom bestätigt: Y2/X2/D2-Kandidat, t = erste Kerze mit Schluss über der Nackenlinie N, L_ref = L_{s2}, Referenzniveau = N. Bekannte Fallzahlen Development: BTC 14, XRP 17, DOT 15.
S2 Failed Breakdown bestätigt (optional, Entscheidung 1): Y1/X1/D1-Kandidat mit Kontext, t = Kandidatenkerze, L_ref = Sweep-Tief (min L über die Kerzen mit L unter dem Niveau bis t), Referenzniveau = höchstes getroffenes Niveau. Bekannte Fallzahlen: BTC 96, XRP 92, DOT nach Zählung v1.0.

Kontextzustand: `bullish_trend_context_active` ab t+1. Kontextfenster für Einstiegsbedingungen t+1 bis t+60 (10 Tage). Invalidierung: erster Schluss unter L_ref, danach kein Einstieg mehr aus diesem Kontext. Kontextende spätestens t+360. Je Kontext höchstens ein Einstieg je Familie. Überlappende Kontexte derselben Quelle: der jüngere ersetzt den älteren nicht, beide laufen, aber eine Position je Familie und Coin (Überlappung wird gezählt).

## 4. Genau drei Entry-Familien, keine weiteren

Alle Grössen in ATR14(4h), ATR14_t der Kontextkerze für Toleranzen, ATR14 der Einstiegskerze für Stops. Swing Low bestätigt wie XRP v1.0 Abschnitt 4 (k = 3, bekannt ab s+3).

DT1 Higher Low: erstes bestätigtes Swing Low s mit t < s ≤ t+60 und L_s ≥ L_ref + 0.5 · ATR14_t, das nach einem Hoch H_mid = max(H, t..s) liegt mit H_mid − L_s ≥ 1.0 · ATR14_t (das Swing Low ist ein Rücksetzer, kein Seitwärtsrauschen). Einstieg zur Eröffnung s+4 (erste Kerze nach Bestätigung). Stop L_s − 0.5 · ATR14_s. Verfall ohne solches Swing Low bis t+60 oder bei Invalidierung.
DT2 Retest and Hold: Referenzniveau P (Nackenlinie bei S1, Niveau bei S2). Retest: erste Kerze b ≥ t+3 mit L_b ≤ P + 0.25 · ATR14_t und C_b ≥ P − 0.5 · ATR14_t. Hold: C_{b+1} > P (Entscheidung 4: eine oder zwei Kerzen). Einstieg zur Eröffnung b+2. Stop P − 1.0 · ATR14_t. Verfall bei gescheitertem Retest (C_b < P − 0.5 · ATR14_t), fehlendem Hold, oder keinem Retest bis t+60.
DT3 Consolidation Breakout: Konsolidierungshoch CH = max(H, t+1..t+18). Erster Schluss über CH ab t+19 bis t+60. Einstieg zur Eröffnung der Folgekerze. Stop min(L, t+1..b) − 0.5 · ATR14_b. Verfall ohne Breakout bis t+60.

Bewusst nicht enthalten: Sofortiger Einstieg am Bottom oder am Nackenlinienbruch (das war Stufe A/B), Einstieg am ersten 1h-Reclaim (das war REBOUND-MICRO), Pullback zur EMA, Volumen- oder Flow-Filter, Stop-Varianten. Die Familien sind getrennte Sleeves, keine Kombination, keine Auswahl «beste Familie».

## 5. Exit (nur für den späteren P&L-Lauf vorgemerkt, nicht Teil der outcome-blinden Phase)

Ein einziger Trend-Exit für alle drei Familien: Chandelier 3 · Tages-ATR14 vom höchsten Schluss seit Einstieg, nur steigend, plus initialer Stop, plus Zeitstopp t+360. Kein 4h-Chandelier, kein EMA20-Ziel, kein Strukturbruch, kein Scale-out. Begründung outcome-informed und als solche ausgewiesen: E-D hielt auf allen drei Coins länger und liess die wenigen Trend-Trades laufen (Cross-Coin-Zusammenfassung, Stufe B Abschnitt 5). Wird erst mit dem P&L-Freeze fixiert.

## 6. Outcome-blinde Messung je Familie und Coin (vor jedem P&L, Vorbericht)

Je Kontext und Familie ausschliesslich aus Kerzen bis zur Einstiegskerze e berechnet: (1) Zeit Bottom → Einstieg: e − t in Kerzen und Tagen, Median und Interquartil, Anteil Kontexte mit Einstieg, Anteil vor Einstieg invalidiert, Anteil verfallen. (2) Einstieg zu Stop in ATR14(4h) und in Prozent des Einstiegspreises, Median, P25, P75. (3) Einstieg zu Vor-Selloff-Hoch: (max(H, t−120..t−1) − Einstieg) / ATR14 und in Prozent, dazu Anteil Einstiege bereits über diesem Hoch. (4) Einstieg zu «neues 20-Tage-Hoch»: (max(H, e−120..e−1) − Einstieg) / ATR14, das ist die Distanz bis zum Niveau, das in den bisherigen Läufen als Trendbeginn zählte, Anteil Einstiege, die dieses Niveau bereits überschritten haben (dann ist das Ziel 0 und die Familie handelt den laufenden Trend). (5) Geometrisches Reward/Risk RR_geo = (Zielniveau − Einstieg − Kosten) / (Einstieg − Stop + Kosten) mit Zielniveau = Vor-Selloff-Hoch, nach K1 (Rundlauf 89 bp Zielpfad, 99 bp Stoppfad, Audit v1), p_BE_geo = 1 / (1 + RR_geo). (6) Kosten in R unter K1 = 99 bp / Stopdistanz in bp, Median, P25, P75. (7) Erwartete Kandidatenzahl je Coin nach Verfall und Invalidierung, je Block, und Hochrechnung auf ETH und SOL aus den Manifest-Zeilen (ohne ETH/SOL-Daten). Keine Exits, keine Post-Entry-Renditen, keine MFE/MAE, keine Trefferquoten.

Keine dieser Grössen wird nach Sicht auf Werte verändert, kein zweiter Lauf mit anderen Konstanten. Der Vorbericht hat dieselben 16 Punkte wie der REBOUND-MICRO-Vorbericht, angepasst auf 4h.

## 7. Economic Gate vor dem Backtest (numerisch, vorab)

Eine Familie geht auf einem Coin nicht in den P&L-Lauf, wenn im outcome-blinden Vorbericht eine der folgenden Bedingungen erfüllt ist: (a) Median Einstieg zu Stop > 3.0 ATR14(4h) (Referenz: Y2-Nackenlinien-Einstieg 4.75 ATR war unhandelbar, Y1/X1 T0 1.4 bis 2.0 ATR); (b) Median Kosten in R unter K1 > 0.40 R (Referenz: REBOUND-MICRO 0.78 bis 0.90 R hat den Vorteil aufgezehrt, Stufe-A-Trades 0.25 bis 0.40 R); (c) Median RR_geo zum Vor-Selloff-Hoch nach K1 < 1.0 (p_BE_geo > 0.50) oder Anteil Einstiege mit Ziel unter Einstieg > 50 Prozent; (d) weniger als 20 erwartete Einstiege auf dem Coin. Eine Familie, die auf allen drei Development-Coins am Gate scheitert, wird als «Spezifikation abgeschlossen, keine Fortführung» geführt, ohne Outcome. Eine Familie, die auf mindestens zwei Coins besteht, geht auf genau diesen Coins in den P&L-Lauf. Die Schwellen sind Entscheidung 3 in Abschnitt 10 und werden vor der Messung fixiert.

## 8. P&L-Phase (erst nach Gate und separatem Freeze, hier nur Rahmen)

Je Coin und Familie: Trades mit Exit nach Abschnitt 5, K1 primär, K0/K2 Bericht, gematchte Kontrollgruppe (Kontextkerzen K1 bis K3 ohne Bottom-Struktur, dieselben drei Einstiegsbedingungen relativ zu Ersatzniveaus wie DB-CONTEXT Abschnitt 3, Ersatz-P = max(H, t−18..t), Ersatz-L_ref = min(L, t−120..t)), gepaarte ΔR, Holm über die zulässigen Familien je Coin, Regel v2, Low-Frequency-Stufung, Blöcke, Konzentration, Anteil abgeschnittener Trends, Zeit bis neues 20-Tage-Hoch. Kein Pooling über Coins. Trial-Accounting: bis 3 je Coin, Vorbelastung BTC rund 47, XRP und DOT rund 43, global rund 260. Promotion zu einer ETH/SOL-Vorregistrierung nur für eine Familie, die auf zwei von drei Coins Regel v2 erfüllt, Netto K1 ≥ 0 hat (Economic Validation Gate) und mindestens 20 erwartete Einstiege je ETH und SOL liefert.

## 9. Was dieser Plan nicht darf

Keine Änderung der Kontextquellen-Definitionen (Y/X/D-Kandidaten bleiben, wie eingefroren), keine vierte Entry-Familie, keine Zielvariante, keine Stop-Variante, keine Flow-Bedingung, kein 1h-Einstieg, kein Visual AI. Keine Messung vor Freigabe, keine ETH/SOL-Daten. REBOUND wird nicht wieder geöffnet, auch nicht als «DT0 Einstieg am Bottom».

## 10. Offene Entscheidungen vor der outcome-blinden Messung

1. Kontextquelle: nur S1 (bestätigter Double Bottom, 14 bis 17 Kontexte je Coin, dann werden alle Familien voraussichtlich Low-Frequency oder deskriptiv) oder S1 und S2 (Failed Breakdown, 92 bis 96 Kontexte, getrennt ausgewertet, sechs Zellen je Coin, Holm über sechs). Empfehlung: S1 und S2 getrennt, weil S1 allein die Mindestzahl 20 fast sicher verfehlt.
2. DB-CONTEXT v0.1 (ETH/SOL) durch DELAYED-TREND ersetzen und die ETH/SOL-Vorregistrierung erst nach dem Development neu schreiben, oder DB-CONTEXT unverändert als unabhängigen ETH/SOL-Test behalten und DELAYED-TREND auf S2 beschränken. Empfehlung: ersetzen, ETH/SOL bleiben so ohnehin unberührt.
3. Economic-Gate-Schwellen bestätigen: Stop Median ≤ 3.0 ATR, Kosten K1 Median ≤ 0.40 R, RR_geo Median ≥ 1.0 zum Vor-Selloff-Hoch, mindestens 20 erwartete Einstiege je Coin.
4. DT2 Hold-Bestätigung: eine Kerze (C_{b+1} > P) oder zwei Kerzen (C_{b+1}, C_{b+2} > P). Und ob DT2 überhaupt geführt wird, nachdem der reine Retest in DB-CONTEXT kein Filter war (87 bis 94 Prozent Rate nach 3 Kerzen). Empfehlung: führen mit einer Kerze Hold, das Gate entscheidet.
5. Kontextfenster 60 Kerzen für die Einstiegsbedingungen und Invalidierung bei Schluss unter L_ref bestätigen (Development: Higher Low nach 13 bis 27 Kerzen, Breakout nach 26 bis 39 Kerzen, Invalidierung in 35 bis 53 Prozent).
6. Reihenfolge: outcome-blinde Messung auf BTC, XRP, DOT unmittelbar nach Freigabe, oder erst nach den XS21- und Lane-C-Schritten. Empfehlung: unmittelbar, die Messung braucht keine neuen Daten und keinen Freeze der P&L-Regeln.
