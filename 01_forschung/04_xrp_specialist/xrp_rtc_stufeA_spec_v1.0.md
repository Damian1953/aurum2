# XRP-RTC Stufe A — Spezifikation Version 1.0 (Freeze)

**Project Aurum II, `01_forschung/04_xrp_specialist/xrp_rtc_stufeA_spec_v1.0.md`. 17.09.2026. Status: eingefroren vor jeder Outcome-Berechnung. Ersetzt den Plan v0.4 (SHA b8497a56…) für den RTC-Teil. Erster unabhängiger Generalisierungstest der auf BTC entwickelten Reversal-Mechanik (Governance v1, Evidenzklasse «Independent discovery»). Grundlage: BTC-Parameterpaket v1.1 (Freeze 7c4be2f8…), Umsetzungsentscheide U1 bis U21 (257a7f06…), Parameterprüfung (720e16e6…), Entscheide vom 17.09.2026 (ENTSCHEIDE cac0cb16…), Governance v1 (d995baf0…), Auswertungsregeln v1 (aa453a1b…) mit Regel v2 für «mechanistically promising». Library: rlib v1.0 (f1ffdbb8…) auf ylib (7f0230c9…), Regressionstest gegen Stufe A bestanden (Bericht `regressionstest_rlib_v1.0_gegen_stufeA.md`). Bis zum Freeze dieser Datei wurden keine XRP-Outcomes, Post-Entry-Renditen, MFE/MAE, Stop- oder Zieltreffer berechnet oder angesehen.**

## 1. Datenquelle und Zeitraum

Signalquelle: Binance Spot XRPUSDT 4h, alle zwölf Spalten, UTC-Raster 00/04/08/12/16/20. Discovery-Datei `02_daten/holdout/discovery/XRPUSDT_spot4h_discovery.csv`, SHA-256 6fda0931ded268ac… (Manifest v1.1 e2e764b4…), 12397 Kerzen von 2018-05-04 08:00 bis 2023-12-31 20:00 UTC, keine NaN, kein Nullvolumen. Flow-Datei `XRPUSDT_flow4h_discovery.csv` (dlib v0.2, 4e042804…) auf demselben Raster, 18 Spalten, Funding-z ab 2020-04-05, `delta_oi_zscore` ab 2022-02-04. Validation-Dateien (ab 2024-01-01) werden nicht geladen, die Ladesperre in `ylib.load` und `dlib._load` ist aktiv (`AURUM_VALIDATION` nicht gesetzt). Kraken XRPUSD 240 wird in Stufe A nicht verwendet, es ist die Ausführungsreihe der späteren Validation.

Datenlücken: 7 Lücken im Raster mit 9 fehlenden Kerzen (2018-06-26 12h, 2018-07-04 8h, 2018-11-14 8h, 2019-03-12 8h, 2019-05-15 12h, 2019-08-15 8h, 2020-02-19 8h). Regel wie BTC (U2): alle Fenster sind Kerzenindex-Fenster über die vorhandenen Kerzen, ATR und True Range verwenden den vorigen vorhandenen Schluss, Kandidaten mit einer Lücke im 120-Kerzen-Fenster werden mit Flag `gap_in_window` berichtet, nicht ausgeschlossen.

Vorlauf: 134 Kerzen (ATR14 plus 120-Kerzen-Hoch), erste auswertbare Kerze Index 134 (2018-05-26 16:00 UTC). Blöcke: P1 bis 2020-12-31 (2018-05 bis 2020-12), P2 2021-01-01 bis 2023-12-31. Vermerk aus v0.4: Die XRP-Expansion ab November 2024 liegt im Holdout und ist für Stufe A ohne Bedeutung.

## 2. Timeframe und Normierung

4h-Kerzen. Wilder-ATR über 14 Kerzen (Initialisierung als Mittel der ersten 14 True Ranges, danach rekursiv). Für Grössenvergleiche der Kerze t (Docht, Körper, `ext`, `dd120_atr`, Penetration, `at_low_structure`) gilt ATR14_{t−1}. Für Stop und Chandelier gilt ATR14_t. EMA50 der Schlusskurse (Initialisierung als Mittel der ersten 50 Schlusskurse). `volume_zscore_t` = (V_t − Mittel(V, t−60..t−1)) / SD(V, t−60..t−1, Populations-SD), NaN bei SD 0. `close_location_t` = (C − L) / (H − L), NaN bei H = L. Tages-ATR14 (für E-D): Wilder-ATR über Tageskerzen, die aus den 4h-Kerzen des UTC-Tages aggregiert werden (Open erste, High max, Low min, Close letzte Kerze), Wert des Vortages gilt für alle Kerzen des laufenden Tages.

## 3. Kontext (alle drei Bedingungen auf der Kandidatenkerze t, bei X2 auf s2)

K1, ATR-Form (Entscheid 17.09.2026, Konstante eingefroren): `dd120_atr_t` = (C_t − max(H, t−120..t−1)) / ATR14_{t−1} ≤ −6.0. Die BTC-Form (C_t / max(H) − 1 ≤ −0.12) wird nur als Coverage-Diagnose berichtet, nicht als Baseline und nicht als Variante.
K2: `ext` = (C − EMA50) / ATR14_{t−1} ≤ −2.0 auf mindestens einer der Kerzen t−5 bis t.
K3: innerhalb 1.0 ATR14_{t−1} eines Niveaus (Swing Low, 120-Kerzen-Tief, Zone) oder `at_low_structure_t` = 1 mit ATR-Form: min(L, t−2..t) ≤ min(L, t−120..t−3) + 1.0 · ATR14_{t−1}.

## 4. Struktur und Niveaus (identisch mit BTC, U3 bis U5)

Swing Low bestätigt, wenn L_s strikt kleiner ist als die Tiefs der drei Kerzen davor und der drei Kerzen danach, bekannt ab s+3. Swing High spiegelbildlich. Niveaus, Stand t−1: `swing_low_level` = jüngstes bestätigtes Swing Low, nicht älter als 240 Kerzen. `nbar_low_level` = min(L, t−120..t−3). `zone_low_level` = Median der Tiefs eines Bandes der Breite 0.5 · ATR14_{t−1} um ein bestätigtes Swing Low mit mindestens drei Berührungen in 240 Kerzen, bei mehreren Zonen die höchste unter dem Schluss, sonst die tiefste.

## 5. Kandidaten (Familien X1, X2, X3; Definitionen identisch mit Y1, Y2, Y3 v1.1 bis auf die ATR-Form der Penetration)

X1 Failed Breakdown: L_t ≤ Niveau − 0.05 · ATR14_{t−1} und C_t > Niveau auf mindestens einem der drei Niveaus, `lower_wick_atr_t` ≥ 0.5, LW ≥ 1.5 · Körper. Kontext erfüllt.
X2 Double Bottom mit Nackenlinienbruch: zwei bestätigte Swing Lows s1 < s2 mit 12 ≤ s2 − s1 ≤ 240, L_{s2} ∈ [L_{s1} − 0.5 · ATR14_{s2−1}, L_{s1} + 1.0 · ATR14_{s2−1}], bestätigtes Swing High h1 zwischen s1 und s2 mit H_{h1} − max(L_{s1}, L_{s2}) ≥ 2.0 · ATR14_{s2−1}, Nackenlinie N = H_{h1}, jüngstes qualifizierendes s1 je s2 (U8). Kontext auf s2 (U7). Kandidat = erste Kerze t ≥ s2+3 mit C_t > N, Verfall bei C < L_{s2} − 0.5 · ATR oder t − s1 > 240. Zeitordnung nach Kandidatenkerze, je Kerze das Paar mit jüngstem s2, keine zweite Kandidatenkerze innerhalb 12 Kerzen (U8). Triple Bottom und 逆三尊 enthalten. Keine 3-ATR-Abbruchgrenze (v1.1).
X3 Wick plus Volumen: `lower_wick_atr_t` ≥ 1.0, LW ≥ 2.0 · Körper, `close_location_t` ≥ 0.60, `volume_zscore_t` ≥ 1.5. Kontext erfüllt. Jitter 1.0 und 2.0 nur als Robustheitsbericht.

## 6. Trigger und Einstieg

Primär T0: Einstieg zur Eröffnung der Kerze t+1. Vorregistrierte Vergleiche auf denselben Kandidaten: TA (C_{t+1} > H_t, Einstieg Eröffnung t+2, sonst Verfall, Ein-Kerzen-Regel) und TB (erster Schluss über dem Referenzniveau in t+1..t+6, Einstieg zur Eröffnung der Folgekerze, sonst Verfall; Referenzniveau X1: höchstes getroffenes Niveau, X3: `nbar_low_level` bei `at_low_structure`, sonst das nächstgelegene Niveau innerhalb 1 ATR). X2: Trigger ist der Nackenlinienbruch, Einstieg zur Eröffnung der Kerze nach der Bruchkerze, TA und TB entfallen. Einstiegspreis: Eröffnung der Einstiegskerze plus Slippage des Kostenmodells. Eine Position je Sleeve, Kandidaten während einer offenen Position verfallen (`in_position`), nach Exit neuer Einstieg ab der nächsten Kandidatenkerze.

## 7. Stop, Ziel, Exits

Initialer Stop: X1 L_t − 0.5 · ATR14_t, X2 L_{s2} − 0.5 · ATR14_{s2}, X3 L_t − 0.5 · ATR14_t. Kein Trade, wenn Eröffnung der Einstiegskerze − Stop > 3 · ATR14_t (X1, X3, Kontrollen), keine Grenze für X2 (v1.1). Kein Trade, wenn die Eröffnung unter dem Stop liegt. R = Einstieg − Stop. Kein Kursziel.

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

Kontrollpool: Kerzen ab Index 134 mit Kontext K1 bis K3, auf denen keine der drei Muster vorliegt (weder Failed Breakdown noch X3-Flag, auch ohne Kontext), und die nicht Kandidatenkerze oder Bodenkerze s2 ± 3 eines gültigen X2-Paares sind. Je Signal bis zu drei Kontrollen: innerhalb ±540 Kerzen, Abstand > 12 Kerzen zum Signal, |`dd120_atr`| − Differenz ≤ 1.5, |`ext`|-Differenz ≤ 0.5, nicht innerhalb eines offenen Positionsfensters derselben Hypothese, paarweise Abstand > 12 Kerzen, Auswahl nach kleinster `dd120_atr`-Differenz, dann Zeitabstand. Referenzkerze: X1 und X3 die Kandidatenkerze, X2 die Bodenkerze s2 (U21). Auf Kontrollen derselbe Trigger und Exit wie im verglichenen Sleeve, Stop L − 0.5 · ATR14 mit 3-ATR-Grenze, TB-Referenz auf Kontrollen `nbar_low_level`. Keine Erweiterung der Toleranzen, Abdeckung wird berichtet. Ein Signal ohne Kontrolle bildet kein Paar. Statuszuweisung ausser inconclusive nur mit mindestens fünf Paaren.

Die Bedingung «nicht innerhalb eines offenen Positionsfensters» setzt Exit-Zeitpunkte voraus und wird deshalb erst im Outcome-Lauf angewendet. Die outcome-blinde Zählung berichtet Matches ohne diese Bedingung als Obergrenze.

## 12. Zählweise

Kandidaten je Familie = Kerzen mit erfülltem Muster und Kontext (X2: gültige Paare nach Zeitordnung). Einstiege je Trigger = Kandidaten mit Trigger und zulässigem Stop, ohne Überlappungsausschluss in der Zählung. Matches = Signale mit mindestens einer Kontrolle nach Abschnitt 11 ohne Positionsausschluss. Alles je Block P1 und P2.

## 13. Abgleich mit der BTC-Mechanik

Identischer Codepfad (rlib, Modus `cfg_alt`). Gegenüber BTC Stufe A v1.1 sind genau vier Zahlen in ihrer Form geändert, alle vor Outcomes und mechanistisch aus der ATR-Normierung abgeleitet (Parameterprüfung Gruppe D): K1 als ATR-Vielfaches (6.0 statt 12 Prozent), Penetration 0.05 ATR (statt 0.1 Prozent), `at_low_structure` Tief + 1.0 ATR (statt 2 Prozent), Matching-Toleranz 1.5 ATR-Einheiten (statt 3 Punkte). Alle übrigen 31 Zahlen unverändert. Zusätzlich gegenüber Stufe A, aus dem BTC-Lauf gelernt und in v0.4 vor XRP-Outcomes gesetzt: T0 primär statt TA, E-D als zweite Exit-Baseline, Kontrollgruppe im primären Test.

## 14. Inkremente, Tests, Multiplizität, Kriterien (aus v0.4 übernommen, bestätigt)

Primäre Familie (Holm über drei): X1, X2, X3 je mit T0 (X2 Nackenlinie) und E-U gegen Kontrollen, gepaarte ΔR. Trigger-Familie (Holm über vier): TA und TB gegen T0 auf X1 und X3, Erwartung je Kandidat. Exit-Familie (Holm über drei): E-D gegen E-U auf X1, X2, X3. Kontrollarchitektur (ein Test): E0 gegen E-U auf der Vereinigung. Inkremente (Holm über zwei) als Teilmengentests: RTC-1 (`volume_zscore` ≥ 1, `taker_imbalance` ≥ 0, `ti_delta6` ≥ 0.10), RTC-2 (`funding_zscore` ≤ −1 oder `delta_oi_zscore` ≤ −1.0). Follow-through-Diagnose 1, 3, 6 Kerzen für Signale und Kontrollen. Trial-Zahl 16 plus Jitter plus Vorbelastung XRP. Kriterium «Signal vorhanden», Statusebenen formal supported, mechanistically promising (Regel v2), no evidence (inconclusive, Fast Fail), Fast Promote nach Auswertungsregeln v1 und Governance v1 Abschnitt 3. Mindestzahl 30, Stufung 20, Bootstrap-Intervalle. Blockregel: beide Blöcke nicht negativ bei mindestens 10 Signalen je Block. Konfigurationsregel für die Validation vorab: primäre Konfiguration, es sei denn, ein Vergleich ist innerhalb seiner Familie nach Holm positiv und die Basiskonfiguration nicht. Keine Auswahl nach Ergebnis, keine Kombination.

Nicht Bestandteil dieses Freeze: XRP-B und XRP-B+ (Breakout-Engine, Lane B) werden mit BTC-B und DOT-A gemeinsam in einem eigenen Freeze eingefroren (Roadmap v1.1 Woche 3). Halving-Kontext und Visual AI: keine.

## 15. Evidenzklasse und Deckel

Independent discovery. Höchste Folge eines positiven Ergebnisses: Validation-Lauf auf dem XRP-Holdout mit Kraken-Ausführung. Kein Sleeve, keine Produktion. Ein Cross-Coin-Test wird erst vorregistriert, wenn dieselbe Mechanik auf mindestens zwei Coins in dieselbe Richtung wirkt. Keine Regeländerung nach Sicht auf Outcomes, eine neue Mechanik heisst neue Vorregistrierung.

## 16. Outcome-blinde Zählung und Matching (Befund vor dem Freeze, `count_XRP.json`)

Berechnet wurden ausschliesslich Kandidatenkerzen, Trigger-Kerzen, Eröffnungspreis der Einstiegskerze, initialer Stop (Zulässigkeit) und strukturelle Kontrollen. Keine Exits, keine Post-Entry-Renditen, keine MFE/MAE, keine Stop- oder Zieltreffer. Positionsausschluss und Überlappungsausschluss (beide brauchen Exits) sind nicht angewendet, alle Zahlen sind Obergrenzen für den Outcome-Lauf.

Kerzen: 12397 vorhanden, 134 Vorlauf, 12263 auswertbar ab 2018-05-26 16:00 UTC, 7 Rasterlücken mit 9 fehlenden Kerzen, Kerzen je Block {'P1': 5827, 'P2': 6570}. Swing Lows 1293, Swing Highs 1252.

Kontext-Coverage (Diagnose, keine Anpassungsgrundlage): K1 in ATR-Form trifft 56.4 Prozent der auswertbaren Kerzen, die feste 12-Prozent-Form zum Vergleich 56.1 Prozent, K1 und K2 zugleich 2892 Kerzen, 218 zusammenhängende K1-Episoden, Kontextkerzen (K1 bis K3) 2206 nach Block {'P1': 1171, 'P2': 1035}. Vermerk: Die Coverage-Werte in der Parameterprüfung (Tabelle 2, Spalte ddATR) wurden mit der Näherung (C/H − 1)/(ATR/C) berechnet, die eingefrorene Formel (C − H)/ATR ist um den Faktor C/H strenger in der Skala und liefert die hier berichteten, höheren Anteile. Die Konstante 6.0 bleibt unverändert.

Kandidaten: X1 92 (Block {'P1': 53, 'P2': 39}, Niveaus {'zone': 34, 'nbar': 18, 'swing|zone': 13, 'swing': 13, 'swing|nbar': 9, 'swing|nbar|zone': 3, 'nbar|zone': 2}, 7 mit Lücke im Fenster, 311 Failed Breakdowns ohne Kontext), X2 17 gültige aus 332 Paaren (272 ohne Kontext, 191 Duplikate, 10 Triple, Block {'P1': 6, 'P2': 11}), X3 29 (Block {'P1': 12, 'P2': 17}, 45 ohne Kontext). Überlappung X1 und X3 13, X1 und X2 0, Vereinigung 125.

Einstiege je Trigger (ohne Überlappungsausschluss): X1 T0 90 Einstiege (0 ohne Trigger, 2 Stop über 3 ATR, 0 Eröffnung unter Stop), Stopdistanz Median 1.39 ATR, TA 23 Einstiege (67 ohne Trigger, 2 Stop über 3 ATR, 0 Eröffnung unter Stop), Stopdistanz Median 1.82 ATR, TB 79 Einstiege (11 ohne Trigger, 2 Stop über 3 ATR, 0 Eröffnung unter Stop), Stopdistanz Median 1.53 ATR. X2 Nackenlinie 17 Einstiege (0 ohne Trigger, 0 Stop über 3 ATR, 0 Eröffnung unter Stop), Stopdistanz Median 4.11 ATR. X3 T0 24 Einstiege (0 ohne Trigger, 5 Stop über 3 ATR, 0 Eröffnung unter Stop), Stopdistanz Median 1.99 ATR, TA 2 Einstiege (25 ohne Trigger, 2 Stop über 3 ATR, 0 Eröffnung unter Stop), Stopdistanz Median 2.43 ATR, TB 16 Einstiege (7 ohne Trigger, 6 Stop über 3 ATR, 0 Eröffnung unter Stop), Stopdistanz Median 2.25 ATR.

Kontrollpool 2006 Kerzen {'P1': 1079, 'P2': 927}. Matching (Obergrenze): X1 79 von 92 Kandidaten mit mindestens einer Kontrolle, 49 mit drei, Abdeckung {'0': 13, '1': 12, '2': 18, '3': 49}, Kontrollen im Mittel 2.12, 172 verschiedene Kontrollkerzen, 20 mehrfach verwendet, Median Poolgrösse im Fenster 6, nach Block {'P1': 46, 'P2': 33}, nach Jahr {'2018': 7, '2019': 20, '2020': 19, '2021': 10, '2022': 9, '2023': 14}. X2 17 von 17 Kandidaten mit mindestens einer Kontrolle, 13 mit drei, Abdeckung {'1': 3, '2': 1, '3': 13}, Kontrollen im Mittel 2.59, 44 verschiedene Kontrollkerzen, 0 mehrfach verwendet, Median Poolgrösse im Fenster 15, nach Block {'P1': 6, 'P2': 11}, nach Jahr {'2018': 1, '2019': 4, '2020': 1, '2021': 1, '2022': 7, '2023': 3}. X3 21 von 29 Kandidaten mit mindestens einer Kontrolle, 7 mit drei, Abdeckung {'0': 8, '1': 6, '2': 8, '3': 7}, Kontrollen im Mittel 1.48, 40 verschiedene Kontrollkerzen, 3 mehrfach verwendet, Median Poolgrösse im Fenster 2, nach Block {'P1': 10, 'P2': 11}, nach Jahr {'2018': 3, '2019': 4, '2020': 3, '2021': 2, '2022': 6, '2023': 3}.

Inkrement-Teilmengen an der Kandidatenkerze (Flow-Merkmale vor Einstieg): RTC-1 X1 2 von 92, X2 0 von 17, X3 1 von 29. RTC-2 X1 19 von 56 gültigen, X2 0 von 12, X3 5 von 18.

Mechanische Auffälligkeiten, ohne Handlung: Die RTC-1-Teilmenge ist auf allen drei Familien nahezu leer (2, 0 und 1 Kandidaten), die drei Flow-Bedingungen treten an Bodenkerzen fast nie gleichzeitig auf. Der RTC-1-Inkrementtest wird damit voraussichtlich als «keine Teilmenge» enden, die Spezifikation bleibt unverändert, eine Neudefinition wäre eine neue Vorregistrierung. X3 hat eine schwache Kontrollabdeckung (8 von 29 ohne Kontrolle, Median Poolgrösse 2), TA trifft auf X3 nur 2 von 29. X2-Stopdistanzen sind wie in v1.1 erwartet gross (Median 4.1 ATR, Maximum 9.0 ATR).

Prüfsummen der Zählung: Spot 6fda0931ded268ac…, Flow 425b430b506c23d7…, rlib f1ffdbb81cad3115…, ylib 7f0230c938bc31ba…, Kandidatendateien 0373bba001c231b4… und 15d506a8bd3741da….
