# BTC YAMATO RTC — Stufe A, eingefrorenes Parameterpaket, Version 1.1

**Project Aurum II, `01_forschung/06_btc_specialist/`. Freeze bestätigt am 17.09.2026. Dieses Blatt fasst jede Zahl zusammen, die Stufe A verwendet, mit Quelle. Es ist zusammen mit `btc_yamato_rtc_research_plan_v1.1.md` eingefroren. Gegenüber Version 1.0 (SHA 98376c2d…) ändert sich ausschliesslich der Wegfall der 3-ATR-Abbruchgrenze für Y2 (Abschnitt Trigger, Einstieg, Stop, Sizing). Keine der Zahlen wird vor oder nach Sicht auf Ergebnisse geändert. Stufe B, Peak Engine, XRP, DOT und Visual AI bleiben offen.**

## Quellen (SHA-256 zum Zeitpunkt des Freeze)

| Dokument | SHA-256 | Eingefrorene Teile |
|---|---|---|
| `btc_yamato_rtc_research_plan_v1.1.md` | siehe ENTSCHEIDE (v1.0 war 56069bc009f697bbed985a1f80540f203268db2ba88964bcca9b558d3ba79003) | vollständig |
| `btc_sakata_bottom_peak_spec_v0.1.md` | 2e052ab076b5ce23ae9acfb071f904facafad46c33dc682304e1820964fa745e | Abschnitte 1 bis 3 (Bottom Candidates, Double Bottom, Bestätigung) |
| `candlestick_flow_feature_library_spec_v0.1.md` | d5c4cfbd2f2e82ec186da9354997c9ccff6508adcd7a17893b4bf0cfa45cacec | Abschnitt 1 (Normierung), Abschnitt 2 (Kontextflags), Abschnitt 5 (Swing-Struktur, Niveaus, Failed Breakdown, `volume_zscore`) |
| `rtc_reversal_to_trend_framework_v0.1.md` | 269667b3df168ec628a53f03bc5a63c737cfd123dedd74fd5e2456fa555216ba | Abschnitt 2 (Discovery-Schnitt), Abschnitt 3 (Kontext K1 bis K3, Stop), Abschnitt 4 (Trigger TA), Abschnitt 5 (Chandelier), Abschnitt 14 (Capture-Metriken) |

## Zeitraum und Daten

Signalquelle Binance Spot BTCUSDT 4h, alle Spalten, UTC-Raster 00/04/08/12/16/20. Discovery-Fenster: Datenbeginn 2017-08-17 bis 2023-12-31 23:59:59 UTC (letzte Kerze 2023-12-31 20:00), physisch abgeschnittene Kopie mit Prüfsumme. Holdout ab 2024-01-01, in Stufe A nicht berührt. Blöcke: P1 bis 2020-12-31, P2 2021-01-01 bis 2023-12-31.

## Normierung

Wilder-ATR über 14 Kerzen. Für Grössenvergleiche der Kerze t gilt ATR_{t−1}. Für Stop und Chandelier gilt ATR14_t. EMA50 der Schlusskurse. `volume_zscore` = (V_t − Mittel(V, t−60..t−1)) / SD(V, t−60..t−1).

## Kontext (alle drei, für Y1 und Y3 auf der Kandidatenkerze t, für Y2 nach Umsetzungsentscheid)

K1: `dd120_t` = C_t / max(H, t−120..t−1) − 1 ≤ −0.12.
K2: `ext` = (C − EMA50) / ATR_{t−1} ≤ −2.0 auf mindestens einer der Kerzen t−5 bis t.
K3: innerhalb 1.0 ATR eines Niveaus (Swing Low, 120-Kerzen-Tief, Zone) oder `at_low_structure_t` = 1 (min(L, t−2..t) ≤ 1.02 · min(L, t−120..t−3)).

Vormerkung (kein Bestandteil der Baseline): Eine volatilitätsnormierte Kontextdefinition (Rückgang in ATR statt 12 Prozent) kann später als vorregistrierte Robustheitsdiagnose geführt werden. Sie ersetzt die eingefrorene Baseline nicht.

## Struktur und Niveaus

Swing Low bestätigt, wenn L_s kleiner ist als die Tiefs der drei Kerzen davor und der drei Kerzen danach, bekannt ab s+3. Swing High spiegelbildlich. Niveaus, Stand t−1: `swing_low_level` = letztes bestätigtes Swing Low, nicht älter als 240 Kerzen. `nbar_low_level` = min(L, t−120..t−3). `zone_low_level` = Band der Breite 0.5 · ATR_{t−1} um ein bestätigtes Swing Low mit mindestens zwei weiteren bestätigten Swing Lows innerhalb dieser Toleranz in den letzten 240 Kerzen (mindestens drei Berührungen).

## Kandidaten

Y1 Failed Breakdown: L_t < Niveau · (1 − 0.001), C_t > Niveau, `lower_wick_atr_t` ≥ 0.5, LW ≥ 1.5 · B, auf mindestens einem der drei Niveaus. Trigger TA.
Y2 Double Bottom: zwei bestätigte Swing Lows s1 < s2 innerhalb 240 Kerzen, s2 − s1 ≥ 12, L_{s2} ≥ L_{s1} − 0.5 · ATR14 und L_{s2} ≤ L_{s1} + 1.0 · ATR14, bestätigtes Swing High h1 zwischen s1 und s2 mit H_{h1} − max(L_{s1}, L_{s2}) ≥ 2.0 · ATR14, Nackenlinie N = H_{h1}. Kandidat und Bestätigung zugleich: erste Kerze t mit C_t > N. Verfall bei Schluss unter L_{s2} − 0.5 · ATR nach s2. Triple Bottom und 逆三尊 enthalten, erster Nackenlinienbruch zählt. Kein TA.
Y3 Wick plus Volumen: `lower_wick_atr_t` ≥ 1.0, LW ≥ 2.0 · B, `close_location_t` ≥ 0.60, `volume_zscore_t` ≥ 1.5. Trigger TA. Jitter 1.0 und 2.0 nur als Robustheit, ohne Ersatzwirkung.

## Trigger, Einstieg, Stop, Sizing

TA: C_{t+1} > H_t, Einstieg zur Eröffnung der Kerze t+2, sonst Verfall (Ein-Kerzen-Regel). Y2: Einstieg zur Eröffnung der Kerze nach der Nackenlinien-Bruchkerze. Initialer Stop: Y1 Sweep-Tief (L_t) − 0.5 · ATR14_t, Y2 L_{s2} − 0.5 · ATR14_t, Y3 L_t − 0.5 · ATR14_t. Kein Trade, wenn Einstieg − Stop > 3 · ATR14, für Y1 und Y3 und die Kontrollen. Für Y2 entfällt diese Grenze (Version 1.1), die Stopdistanz in ATR wird je Trade berichtet, das nominelle Risiko bleibt 2 Prozent, ein weiter Stop ergibt eine kleinere Position, keine Mindestpositionsgrösse. R = Einstieg − Stop. Sicht 1: Notional so, dass R 2 Prozent des Sleeve-Startkapitals riskiert, kein Compounding, Notional höchstens 100 Prozent. Eine Position, keine Add-ons, nach Exit neuer Einstieg ab der nächsten Kandidatenkerze.

## Exit-Baseline E-U (identisch für Y1, Y2, Y3 und Kontrollen)

Chandelier: `floor_t` = max(`floor_{t−1}`, HH_seit_Einstieg_t − 3.0 · ATR14_t), nur steigend, wirksamer Stop max(initialer Stop, `floor`), gilt für t+1, Ausführung intraday als Stop-Market. Strukturbruch: Schluss unter dem letzten seit Einstieg bestätigten Swing Low, Exit zur Eröffnung der Folgekerze. Die zuerst ausgelöste Regel beendet den Trade. Keine Peak-Logik in Stufe A.

## Kosten

Kostenmodell K1 (Spot, Kraken Tier 1): Gebühr 0.40 Prozent je Seite, Reibung 0.02 Prozent, Slippage 0.05 Prozent beim Einstieg, 0.10 Prozent am Stop. K0 und K2 als Bericht. Cash zum T-Bill-Satz.

## Kontrollgruppe

Je Signal bis zu drei Kontrollkerzen: Kontext K1 bis K3 erfüllt, keines der drei Muster, innerhalb ±90 Tagen (540 Kerzen), `dd120` innerhalb ±0.03, `ext` innerhalb ±0.5 ATR, nicht innerhalb von 12 Kerzen des Signals, nicht innerhalb einer offenen Signalposition, die nächsten drei nach Abstand in `dd120`. Auf Kontrollen: Trigger TA, Stop L − 0.5 · ATR14, Exit E-U. Keine Erweiterung der Toleranzen, Abdeckung wird berichtet.

## Kriterium und Mindestzahl

«Signal vorhanden»: gepaarte Differenz der Erwartung je Trade gegen die Kontrollen grösser null mit Bootstrap-5-Prozent-Perzentil über null nach Holm über Y1 bis Y3, Erwartung netto K1 über null, beide Blöcke nicht negativ bei mindestens 10 Signalen je Block, Vorzeichen auf mindestens einer verschobenen Kerzenaggregation erhalten (sobald 1h-Daten vorliegen). Mindestzahl 30, 20 bis 29 «geringe Basis», unter 20 deskriptiv, nicht je Muster anpassbar, immer mit Bootstrap-Intervallen.

## Diagnosemetriken (nie Signal)

Abstand Einstieg zum ex-post Tief (120 Kerzen vor bis 12 nach Einstieg) in ATR, MFE und MAE in R und ATR, neuer Trend als Schluss über dem höchsten Hoch der 120 vollständig vor dem Einstieg liegenden Kerzen innerhalb 7, 14, 30, 60 Tagen, Capture Ratio (Tief bis Hoch, Hoch bis 60 Kerzen nach Exit), Klassifikation Trend (30 Tage), verzögerter Trend (Tag 31 bis 60), Rebound (MFE ≥ 1 R ohne neues Hoch in 60 Tagen), Fehlsignal, Persistenzdiagnose 30 Kerzen über dem Vor-Einstiegs-Hoch.

## Reihenfolge nach dem Freeze

Datenvalidierung, Umsetzung der deterministischen Library, Unit- und Look-ahead-Tests, Kandidatenzählung und Abdeckung, Validierung des Kontrollgruppen-Matchings. Keine Performance-Auswertung, bis alle fünf Schritte bestanden und dokumentiert sind. Technisch mehrdeutige Regeln werden vor jeder Ergebnisberechnung dokumentiert und entschieden, keine Spezifikationsänderung nach Sicht auf Ergebnisse.
