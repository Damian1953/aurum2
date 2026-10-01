# DOT-RTC Stufe A — Spezifikation Version 1.0 (Freeze)

**Project Aurum II, `01_forschung/05_dot_specialist/dot_rtc_stufeA_spec_v1.0.md`. 17.09.2026. Status: eingefroren vor jeder Outcome-Berechnung. Ersetzt den Plan v0.4 (SHA 46efcc97…) für den RTC-Teil. Zweiter unabhängiger Generalisierungstest der auf BTC entwickelten Reversal-Mechanik (Governance v1, Evidenzklasse «Independent discovery»). Grundlage: BTC-Parameterpaket v1.1 (Freeze 7c4be2f8…), Umsetzungsentscheide U1 bis U21 (257a7f06…), Parameterprüfung (720e16e6…), Entscheide vom 17.09.2026 (ENTSCHEIDE cac0cb16…), Governance v1 (d995baf0…), Auswertungsregeln v1 (aa453a1b…) mit Regel v2 für «mechanistically promising». Library: rlib v1.0 (f1ffdbb8…) auf ylib (7f0230c9…), Regressionstest gegen Stufe A bestanden (Bericht `regressionstest_rlib_v1.0_gegen_stufeA.md`). Bis zum Freeze dieser Datei wurden keine DOT-Outcomes, Post-Entry-Renditen, MFE/MAE, Stop- oder Zieltreffer berechnet oder angesehen.**

## 1. Datenquelle und Zeitraum

Signalquelle: Binance Spot DOTUSDT 4h, alle zwölf Spalten, UTC-Raster 00/04/08/12/16/20. Discovery-Datei `02_daten/holdout/discovery/DOTUSDT_spot4h_discovery.csv`, SHA-256 426b5ae7e4d4e57b… (Manifest v1.1 e2e764b4…), 7381 Kerzen von 2020-08-18 20:00 bis 2023-12-31 20:00 UTC, keine NaN, kein Nullvolumen. Flow-Datei `DOTUSDT_flow4h_discovery.csv` (dlib v0.2, 4e042804…) auf demselben Raster, 18 Spalten, Funding-z ab 2020-11-18, `delta_oi_zscore` ab 2022-02-04. Validation-Dateien (ab 2024-01-01) werden nicht geladen, die Ladesperre in `ylib.load` und `dlib._load` ist aktiv (`AURUM_VALIDATION` nicht gesetzt). Kraken DOTUSD 240 wird in Stufe A nicht verwendet, es ist die Ausführungsreihe der späteren Validation.

Datenlücken: keine, das 4h-Raster ist von der ersten bis zur letzten Kerze lückenlos (7381 Kerzen). Die BTC-Regel U2 (Kerzenindex-Fenster, Flag `gap_in_window`) gilt formal weiter und bleibt ohne Anwendungsfall.

Vorlauf: 134 Kerzen (ATR14 plus 120-Kerzen-Hoch), erste auswertbare Kerze Index 134 (2020-09-10 04:00 UTC). Blöcke nach v0.4: P1 (2020-09 bis 2020-12, 677 auswertbare Kerzen) wird für die Blockregel nicht gewertet, seine Signale zählen im Sleeve und im primären Test. Blockregel auf P2 in zwei Hälften: P2a 2021-01-01 bis 2022-06-30, P2b 2022-07-01 bis 2023-12-31, je nicht negativ bei mindestens 10 Signalen. Vermerk aus v0.4: Das Holdout ab 2024 (rund 5900 Kerzen) ist für DOT länger als ein Drittel der Historie, ausgewiesen. Vorbelastung: Tägliche Trendfolge auf DOT dreimal gescheitert (Stufe 2, MTP-Validierung), kein Veto gegen 4h-Mechanismen.

## 2. Timeframe und Normierung

4h-Kerzen. Wilder-ATR über 14 Kerzen (Initialisierung als Mittel der ersten 14 True Ranges, danach rekursiv). Für Grössenvergleiche der Kerze t (Docht, Körper, `ext`, `dd120_atr`, Penetration, `at_low_structure`) gilt ATR14_{t−1}. Für Stop und Chandelier gilt ATR14_t. EMA50 der Schlusskurse (Initialisierung als Mittel der ersten 50 Schlusskurse). `volume_zscore_t` = (V_t − Mittel(V, t−60..t−1)) / SD(V, t−60..t−1, Populations-SD), NaN bei SD 0. `close_location_t` = (C − L) / (H − L), NaN bei H = L. Tages-ATR14 (für E-D): Wilder-ATR über Tageskerzen, die aus den 4h-Kerzen des UTC-Tages aggregiert werden (Open erste, High max, Low min, Close letzte Kerze), Wert des Vortages gilt für alle Kerzen des laufenden Tages.

## 3. Kontext (alle drei Bedingungen auf der Kandidatenkerze t, bei D2 auf s2)

K1, ATR-Form (Entscheid 17.09.2026, Konstante eingefroren): `dd120_atr_t` = (C_t − max(H, t−120..t−1)) / ATR14_{t−1} ≤ −6.0. Die BTC-Form (C_t / max(H) − 1 ≤ −0.12) wird nur als Coverage-Diagnose berichtet, nicht als Baseline und nicht als Variante.
K2: `ext` = (C − EMA50) / ATR14_{t−1} ≤ −2.0 auf mindestens einer der Kerzen t−5 bis t.
K3: innerhalb 1.0 ATR14_{t−1} eines Niveaus (Swing Low, 120-Kerzen-Tief, Zone) oder `at_low_structure_t` = 1 mit ATR-Form: min(L, t−2..t) ≤ min(L, t−120..t−3) + 1.0 · ATR14_{t−1}.

## 4. Struktur und Niveaus (identisch mit BTC, U3 bis U5)

Swing Low bestätigt, wenn L_s strikt kleiner ist als die Tiefs der drei Kerzen davor und der drei Kerzen danach, bekannt ab s+3. Swing High spiegelbildlich. Niveaus, Stand t−1: `swing_low_level` = jüngstes bestätigtes Swing Low, nicht älter als 240 Kerzen. `nbar_low_level` = min(L, t−120..t−3). `zone_low_level` = Median der Tiefs eines Bandes der Breite 0.5 · ATR14_{t−1} um ein bestätigtes Swing Low mit mindestens drei Berührungen in 240 Kerzen, bei mehreren Zonen die höchste unter dem Schluss, sonst die tiefste.

## 5. Kandidaten (Familien D1, D2, D3; Definitionen identisch mit Y1, Y2, Y3 v1.1 bis auf die ATR-Form der Penetration)

D1 Failed Breakdown: L_t ≤ Niveau − 0.05 · ATR14_{t−1} und C_t > Niveau auf mindestens einem der drei Niveaus, `lower_wick_atr_t` ≥ 0.5, LW ≥ 1.5 · Körper. Kontext erfüllt.
D2 Double Bottom mit Nackenlinienbruch: zwei bestätigte Swing Lows s1 < s2 mit 12 ≤ s2 − s1 ≤ 240, L_{s2} ∈ [L_{s1} − 0.5 · ATR14_{s2−1}, L_{s1} + 1.0 · ATR14_{s2−1}], bestätigtes Swing High h1 zwischen s1 und s2 mit H_{h1} − max(L_{s1}, L_{s2}) ≥ 2.0 · ATR14_{s2−1}, Nackenlinie N = H_{h1}, jüngstes qualifizierendes s1 je s2 (U8). Kontext auf s2 (U7). Kandidat = erste Kerze t ≥ s2+3 mit C_t > N, Verfall bei C < L_{s2} − 0.5 · ATR oder t − s1 > 240. Zeitordnung nach Kandidatenkerze, je Kerze das Paar mit jüngstem s2, keine zweite Kandidatenkerze innerhalb 12 Kerzen (U8). Triple Bottom und 逆三尊 enthalten. Keine 3-ATR-Abbruchgrenze (v1.1).
D3 Wick plus Volumen: `lower_wick_atr_t` ≥ 1.0, LW ≥ 2.0 · Körper, `close_location_t` ≥ 0.60, `volume_zscore_t` ≥ 1.5. Kontext erfüllt. Jitter 1.0 und 2.0 nur als Robustheitsbericht.

## 6. Trigger und Einstieg

Primär T0: Einstieg zur Eröffnung der Kerze t+1. Vorregistrierte Vergleiche auf denselben Kandidaten: TA (C_{t+1} > H_t, Einstieg Eröffnung t+2, sonst Verfall, Ein-Kerzen-Regel) und TB (erster Schluss über dem Referenzniveau in t+1..t+6, Einstieg zur Eröffnung der Folgekerze, sonst Verfall; Referenzniveau D1: höchstes getroffenes Niveau, D3: `nbar_low_level` bei `at_low_structure`, sonst das nächstgelegene Niveau innerhalb 1 ATR). D2: Trigger ist der Nackenlinienbruch, Einstieg zur Eröffnung der Kerze nach der Bruchkerze, TA und TB entfallen. Einstiegspreis: Eröffnung der Einstiegskerze plus Slippage des Kostenmodells. Eine Position je Sleeve, Kandidaten während einer offenen Position verfallen (`in_position`), nach Exit neuer Einstieg ab der nächsten Kandidatenkerze.

## 7. Stop, Ziel, Exits

Initialer Stop: D1 L_t − 0.5 · ATR14_t, D2 L_{s2} − 0.5 · ATR14_{s2}, D3 L_t − 0.5 · ATR14_t. Kein Trade, wenn Eröffnung der Einstiegskerze − Stop > 3 · ATR14_t (D1, D3, Kontrollen), keine Grenze für D2 (v1.1). Kein Trade, wenn die Eröffnung unter dem Stop liegt. R = Einstieg − Stop. Kein Kursziel.

Exit E-U (primär): Chandelier `floor_t` = max(`floor_{t−1}`, HH_seit_Einstieg_t − 3.0 · ATR14_t), nur steigend, wirksamer Stop max(initialer Stop, floor), gilt ab t+1 intraday als Stop-Market. Strukturbruch: Schluss unter dem jüngsten seit Einstieg bestätigten Swing Low → Exit zur Eröffnung der Folgekerze. Die zuerst ausgelöste Regel beendet den Trade.
Exit E-D (vorregistrierter Vergleich): wie E-U mit Tages-ATR14 (Abschnitt 2) im Chandelier und Strukturbruch auf bestätigten Tages-Swing-Lows (k = 3 Tage, Tag s ≥ Einstiegstag, Bestätigungstag vor dem Tag der Prüfkerze).
Exit E0 (Kontrollarchitektur, ein Test auf der Vereinigung): Schluss ≥ EMA20 oder 30 Kerzen nach Einstieg → Exit zur Eröffnung der Folgekerze, initialer Stop bleibt.

## 8. Fill- und Intrabar-Regeln (U12, U13)

Einstiegskerze: nur der initiale Stop ist aktiv, Eröffnung ≤ Stop → Fill an der Eröffnung. Folgekerzen: Eröffnung ≤ wirksamer Stop → Fill an der Eröffnung (`stop_gap`), sonst Tief ≤ wirksamer Stop → Fill am Stop. Stop-Fills mit Slippage `slip_sl`. Struktur- und E0-Exits zur Eröffnung der Folgekerze mit `slip_in`. Position am Datenende offen → Schluss der letzten Kerze (`cut`), berichtet. MFE und MAE ab Einstiegskerze auf Hoch und Tief. Sizing Sicht 1: Notional so, dass R 2 Prozent des Sleeve-Startkapitals riskiert, kein Compounding, Notional höchstens 100 Prozent.

## 9. Kostenmodell

K1 massgebend: Gebühr 0.40 Prozent je Seite, Reibung 0.02 Prozent je Seite, Slippage 0.05 Prozent Einstieg, 0.10 Prozent Stop. K0 (0.16 Prozent, sonst null) und K2 (0.80, 0.06, 0.15, 0.30) als Bericht. Cash zum T-Bill-Satz. Coin-spezifische Kraken-Slippage ist Sache der Validation.

## 10. Ausschlussregeln und fehlende Daten

Kerzen vor Index 134 werden nicht ausgewertet. Kandidatenstatus: `traded`, `in_position`, `no_trigger` (TA, TB), `stop_too_wide`, `entry_below_stop`. Kandidaten am Datenende ohne vollständige Folgekerze verfallen. Flow-Merkmale fehlen fail-closed (NaN): Ein Kandidat ohne gültiges Flow-Merkmal gehört nicht zur Teilmenge des betreffenden Inkrements und wird dort weder als erfüllt noch als nicht erfüllt gezählt. OI-Inkremente sind erst ab 2022-02-04 möglich, Funding ab 2020-04-05.

## 11. Kontrollgruppe und Matching (Definition eines gültigen Matches)

Kontrollpool: Kerzen ab Index 134 mit Kontext K1 bis K3, auf denen keine der drei Muster vorliegt (weder Failed Breakdown noch D3-Flag, auch ohne Kontext), und die nicht Kandidatenkerze oder Bodenkerze s2 ± 3 eines gültigen D2-Paares sind. Je Signal bis zu drei Kontrollen: innerhalb ±540 Kerzen, Abstand > 12 Kerzen zum Signal, |`dd120_atr`| − Differenz ≤ 1.5, |`ext`|-Differenz ≤ 0.5, nicht innerhalb eines offenen Positionsfensters derselben Hypothese, paarweise Abstand > 12 Kerzen, Auswahl nach kleinster `dd120_atr`-Differenz, dann Zeitabstand. Referenzkerze: D1 und D3 die Kandidatenkerze, D2 die Bodenkerze s2 (U21). Auf Kontrollen derselbe Trigger und Exit wie im verglichenen Sleeve, Stop L − 0.5 · ATR14 mit 3-ATR-Grenze, TB-Referenz auf Kontrollen `nbar_low_level`. Keine Erweiterung der Toleranzen, Abdeckung wird berichtet. Ein Signal ohne Kontrolle bildet kein Paar. Statuszuweisung ausser inconclusive nur mit mindestens fünf Paaren.

Die Bedingung «nicht innerhalb eines offenen Positionsfensters» setzt Exit-Zeitpunkte voraus und wird deshalb erst im Outcome-Lauf angewendet. Die outcome-blinde Zählung berichtet Matches ohne diese Bedingung als Obergrenze.

## 12. Zählweise

Kandidaten je Familie = Kerzen mit erfülltem Muster und Kontext (D2: gültige Paare nach Zeitordnung). Einstiege je Trigger = Kandidaten mit Trigger und zulässigem Stop, ohne Überlappungsausschluss in der Zählung. Matches = Signale mit mindestens einer Kontrolle nach Abschnitt 11 ohne Positionsausschluss. Alles je Block P1, P2a und P2b.

## 13. Abgleich mit der BTC-Mechanik

Identischer Codepfad (rlib, Modus `cfg_alt`). Gegenüber BTC Stufe A v1.1 sind genau vier Zahlen in ihrer Form geändert, alle vor Outcomes und mechanistisch aus der ATR-Normierung abgeleitet (Parameterprüfung Gruppe D): K1 als ATR-Vielfaches (6.0 statt 12 Prozent), Penetration 0.05 ATR (statt 0.1 Prozent), `at_low_structure` Tief + 1.0 ATR (statt 2 Prozent), Matching-Toleranz 1.5 ATR-Einheiten (statt 3 Punkte). Alle übrigen 31 Zahlen unverändert. Zusätzlich gegenüber Stufe A, aus dem BTC-Lauf gelernt und in v0.4 vor DOT-Outcomes gesetzt: T0 primär statt TA, E-D als zweite Exit-Baseline, Kontrollgruppe im primären Test.

## 14. Inkremente, Tests, Multiplizität, Kriterien (aus v0.4 übernommen, bestätigt)

Primäre Familie (Holm über drei): D1, D2, D3 je mit T0 (D2 Nackenlinie) und E-U gegen Kontrollen, gepaarte ΔR. Trigger-Familie (Holm über vier): TA und TB gegen T0 auf D1 und D3, Erwartung je Kandidat. Exit-Familie (Holm über drei): E-D gegen E-U auf D1, D2, D3. Kontrollarchitektur (ein Test): E0 gegen E-U auf der Vereinigung. Inkremente (Holm über zwei) als Teilmengentests: RTC-1 (`volume_zscore` ≥ 1, `taker_imbalance` ≥ 0, `ti_delta6` ≥ 0.10), RTC-2 (`funding_zscore` ≤ −1 oder `delta_oi_zscore` ≤ −1.0). Follow-through-Diagnose 1, 3, 6 Kerzen für Signale und Kontrollen. Trial-Zahl 15 plus Jitter plus Vorbelastung DOT (26). Kriterium «Signal vorhanden», Statusebenen formal supported, mechanistically promising (Regel v2), no evidence (inconclusive, Fast Fail), Fast Promote nach Auswertungsregeln v1 und Governance v1 Abschnitt 3. Mindestzahl 30, Stufung 20, Bootstrap-Intervalle. Blockregel: P2a und P2b nicht negativ bei mindestens 10 Signalen je Block, P1 nicht gewertet. Konfigurationsregel für die Validation vorab: primäre Konfiguration, es sei denn, ein Vergleich ist innerhalb seiner Familie nach Holm positiv und die Basiskonfiguration nicht. Keine Auswahl nach Ergebnis, keine Kombination.

Nicht Bestandteil dieses Freeze: DOT-A und DOT-C (Breakout-Engine, Lane B, DOT-C-Schwellen Taker 0.10, Funding-z 1.5, `delta_oi_zscore` ≥ +1.0 bestätigt) werden mit BTC-B und XRP-B gemeinsam in einem eigenen Freeze eingefroren (Roadmap v1.1 Woche 3). Halving-Kontext und Visual AI: keine.

## 15. Evidenzklasse und Deckel

Independent discovery. Höchste Folge eines positiven Ergebnisses: Validation-Lauf auf dem DOT-Holdout mit Kraken-Ausführung. Kein Sleeve, keine Produktion. Ein Cross-Coin-Test wird erst vorregistriert, wenn dieselbe Mechanik auf mindestens zwei Coins in dieselbe Richtung wirkt. Keine Regeländerung nach Sicht auf Outcomes, eine neue Mechanik heisst neue Vorregistrierung.

## 16. Outcome-blinde Zählung und Matching (Befund vor dem Freeze, `count_DOT.json`)

Berechnet wurden ausschliesslich Kandidatenkerzen, Trigger-Kerzen, Eröffnungspreis der Einstiegskerze, initialer Stop (Zulässigkeit) und strukturelle Kontrollen. Keine Exits, keine Post-Entry-Renditen, keine MFE/MAE, keine Stop- oder Zieltreffer. Positionsausschluss und Überlappungsausschluss (beide brauchen Exits) sind nicht angewendet, alle Zahlen sind Obergrenzen für den Outcome-Lauf.

Kerzen: 7381 vorhanden, 134 Vorlauf, 7247 auswertbar ab 2020-09-10 04:00 UTC, 0 Rasterlücken mit 0 fehlenden Kerzen, Kerzen je Block {'P2a': 3276, 'P2b': 3294, 'none': 811}. Swing Lows 721, Swing Highs 686.

Kontext-Coverage (Diagnose, keine Anpassungsgrundlage): K1 in ATR-Form trifft 48.0 Prozent der auswertbaren Kerzen, die feste 12-Prozent-Form zum Vergleich 53.8 Prozent, K1 und K2 zugleich 1769 Kerzen, 124 zusammenhängende K1-Episoden, Kontextkerzen (K1 bis K3) 1374 nach Block {'P2b': 686, 'P2a': 608, 'none': 80}. Vermerk: Die Coverage-Werte in der Parameterprüfung (Tabelle 2, Spalte ddATR) wurden mit der Näherung (C/H − 1)/(ATR/C) berechnet, die eingefrorene Formel (C − H)/ATR ist um den Faktor C/H strenger in der Skala und liefert die hier berichteten, höheren Anteile. Die Konstante 6.0 bleibt unverändert.

Kandidaten: D1 75 (Block {'P2a': 26, 'P2b': 43, 'none': 6}, Niveaus {'zone': 21, 'swing': 16, 'swing|nbar': 10, 'swing|zone': 8, 'nbar|zone': 7, 'nbar': 7, 'swing|nbar|zone': 6}, 0 mit Lücke im Fenster, 129 Failed Breakdowns ohne Kontext), D2 15 gültige aus 209 Paaren (173 ohne Kontext, 113 Duplikate, 12 Triple, Block {'P2a': 9, 'P2b': 4, 'none': 2}), D3 17 (Block {'P2a': 5, 'P2b': 10, 'none': 2}, 18 ohne Kontext). Überlappung D1 und D3 6, D1 und D2 1, Vereinigung 100.

Einstiege je Trigger (ohne Überlappungsausschluss): D1 T0 75 Einstiege (0 ohne Trigger, 0 Stop über 3 ATR, 0 Eröffnung unter Stop), Stopdistanz Median 1.27 ATR, TA 26 Einstiege (48 ohne Trigger, 1 Stop über 3 ATR, 0 Eröffnung unter Stop), Stopdistanz Median 2.09 ATR, TB 63 Einstiege (10 ohne Trigger, 2 Stop über 3 ATR, 0 Eröffnung unter Stop), Stopdistanz Median 1.58 ATR. D2 Nackenlinie 15 Einstiege (0 ohne Trigger, 0 Stop über 3 ATR, 0 Eröffnung unter Stop), Stopdistanz Median 3.9 ATR. D3 T0 17 Einstiege (0 ohne Trigger, 0 Stop über 3 ATR, 0 Eröffnung unter Stop), Stopdistanz Median 2.01 ATR, TA 1 Einstiege (13 ohne Trigger, 3 Stop über 3 ATR, 0 Eröffnung unter Stop), Stopdistanz Median 2.82 ATR, TB 6 Einstiege (7 ohne Trigger, 4 Stop über 3 ATR, 0 Eröffnung unter Stop), Stopdistanz Median 2.76 ATR.

Kontrollpool 1219 Kerzen {'P2a': 539, 'P2b': 612, 'none': 68}. Matching (Obergrenze): D1 73 von 75 Kandidaten mit mindestens einer Kontrolle, 59 mit drei, Abdeckung {'0': 2, '1': 6, '2': 8, '3': 59}, Kontrollen im Mittel 2.65, 175 verschiedene Kontrollkerzen, 22 mehrfach verwendet, Median Poolgrösse im Fenster 13, nach Block {'P2a': 26, 'P2b': 41, 'none': 6}, nach Jahr {'2020': 6, '2021': 15, '2022': 23, '2023': 29}. D2 13 von 15 Kandidaten mit mindestens einer Kontrolle, 10 mit drei, Abdeckung {'0': 2, '1': 2, '2': 1, '3': 10}, Kontrollen im Mittel 2.27, 34 verschiedene Kontrollkerzen, 0 mehrfach verwendet, Median Poolgrösse im Fenster 10, nach Block {'P2a': 8, 'P2b': 3, 'none': 2}, nach Jahr {'2020': 2, '2021': 4, '2022': 5, '2023': 2}. D3 17 von 17 Kandidaten mit mindestens einer Kontrolle, 10 mit drei, Abdeckung {'1': 3, '2': 4, '3': 10}, Kontrollen im Mittel 2.41, 39 verschiedene Kontrollkerzen, 2 mehrfach verwendet, Median Poolgrösse im Fenster 7, nach Block {'P2a': 5, 'P2b': 10, 'none': 2}, nach Jahr {'2020': 2, '2021': 2, '2022': 4, '2023': 9}.

Inkrement-Teilmengen an der Kandidatenkerze (Flow-Merkmale vor Einstieg): RTC-1 D1 0 von 75, D2 1 von 15, D3 2 von 17. RTC-2 D1 27 von 69 gültigen, D2 3 von 14, D3 8 von 15.

Mechanische Auffälligkeiten, ohne Handlung: Die RTC-1-Teilmenge ist auf D1 leer (0 von 75) und auf D2, D3 fast leer (1, 2), wie bei XRP. D3 TA trifft nur 1 von 17. D2-Stopdistanzen Median 3.9 ATR, Maximum 8.5 ATR (v1.1, keine Grenze). Sechs D1-, zwei D2- und zwei D3-Kandidaten liegen im nicht als Block gewerteten P1 (2020-09 bis 2020-12) und zählen im Sleeve. Zwei D1- und zwei D2-Kandidaten haben keine Kontrolle.

Prüfsummen der Zählung: Spot 426b5ae7e4d4e57b…, Flow c20fdabfee16c5fc…, rlib f1ffdbb81cad3115…, ylib 7f0230c938bc31ba…, Kandidatendateien 4ec162e5a1c24151… und 20cd5f48a796f738….
