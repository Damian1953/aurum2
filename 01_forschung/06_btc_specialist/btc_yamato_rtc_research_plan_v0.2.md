# BTC YAMATO RTC — Forschungsplan, Version 0.2

**Project Aurum II, Strang 06_btc_specialist. 17.09.2026. Status: Plan zur Prüfung vor dem Freeze. Kein Rechenlauf. Ersetzt Version 0.1 in der Teststruktur, übernimmt deren Spezifikationen (`btc_japanese_price_action_features_v0.1.md`, `btc_previous_open_levels_spec_v0.1.md`, `btc_sakata_bottom_peak_spec_v0.1.md`, `btc_ichimoku_increment_plan_v0.1.md`) unverändert. Quellenregel: `.jp`-Quellen. Alle Freeze-Urteile bleiben unangetastet. Änderung gegenüber v0.1: zweistufige Discovery mit drei primären Bottom-Hypothesen, einheitlicher Exit-Baseline, gematchter Kontrollgruppe und getrennter Inkrement-Stufe, damit bei rund 60 bis 120 Kandidaten nicht sieben gleichrangige Tests laufen.**

## 0. Hypothese (unverändert)

Japanese Bottom Confirmation, Trend Capture, Peak Confirmation: Nach starken BTC-Rückgängen wird ein Boden erst nach Price-Action-Bestätigung gehandelt, der entstehende Trend gehalten, ohne festes Ziel, bis eine bestätigte Struktur- oder Peak-Evidenz vorliegt. Abschnitte 0, 1, 2, 3, 11, 13 und 14 der Version 0.1 (Hypothese, Verhältnis zu BTC-RTC und Vorbelastung, Multi-Timeframe-Kontext, Niveaus, Quellenzuordnung, Daten, Look-ahead) gelten unverändert.

## 1. Stufe A, Primary Bottom Discovery

Drei primäre Bottom-Hypothesen, alle mit demselben Kontext (K1 Selloff mindestens 12 Prozent unter dem 120-Kerzen-Hoch, K2 Extension mindestens 2 ATR unter EMA50 innerhalb der letzten sechs Kerzen, K3 innerhalb 1 ATR eines Niveaus der Bibliothek oder an der lokalen Low-Struktur), demselben Trigger, demselben Stop, demselben Sizing und demselben Exit. Sie unterscheiden sich ausschliesslich in der Kandidatendefinition.

**Y1, Failed Breakdown / Swing-Low-Reclaim.** Bestätigtes relevantes Swing Low (3/3-Bestätigung, nicht älter als 240 Kerzen) oder 120-Kerzen-Tief oder mehrfach getestete Zone, Kerze t handelt mindestens 0.1 Prozent darunter, schliesst wieder darüber, Lower-Wick-Rejection (`lower_wick_atr` ≥ 0.5 und LW ≥ 1.5 · B). Library `failed_breakdown`. Dann TA.

**Y2, Double Bottom / Sakata-Bestätigung.** Die algorithmische Double-Bottom-Struktur der Sakata-Spezifikation Abschnitt 2 (zwei bestätigte Swing Lows in 240 Kerzen, mindestens 12 Kerzen auseinander, zweites Tief im Band minus 0.5 bis plus 1.0 ATR, Zwischenhoch mindestens 2 ATR über den Tiefs als Nackenlinie). Bestätigung ohne Doppelung, vorab festgelegt: Die Nackenlinien-Bruchkerze (erste Kerze mit Schluss über der Nackenlinie) ist die Bestätigungskerze selbst, sie ersetzt TA, weil der Nackenlinienbruch die Sakata-Bestätigung des Bodens ist und ein zusätzliches «Schluss über dem Hoch der Bruchkerze» eine zweite Bestätigung derselben Aussage wäre. Einstieg zur Eröffnung der Kerze nach der Bruchkerze. Triple Bottom und 逆三尊 sind in Y2 enthalten (erster Nackenlinienbruch zählt), als Flag berichtet.

**Y3, Lower-Wick plus Volume Climax.** Kerze t mit `lower_wick_atr` ≥ 1.0, LW ≥ 2.0 · B, `close_location` ≥ 0.60 und `volume_zscore` ≥ 1.5 (ungewöhnliches Volumen, vorab gesetzt, angelehnt an die kabutech-Beschreibung des Selling Climax mit dreifachem Volumen). Dann TA.

**Trigger TA (Y1, Y3):** Die folgende abgeschlossene 4h-Kerze schliesst über dem Hoch der Kandidatenkerze, Einstieg zur Eröffnung der übernächsten Kerze, sonst verfällt der Kandidat. Keine Intrabar-Annahme.

**Stop und Sizing:** initialer Stop unter der Kandidatenstruktur minus 0.5 ATR14 (Y1 unter dem Sweep-Tief, Y2 unter dem zweiten Tief, Y3 unter dem Kerzentief), kein Trade bei Stop über 3 ATR, Sicht 1 (2 Prozent des Sleeve-Startkapitals je R), eine Position, keine Add-ons.

**Überlappung:** Ein Kandidat kann mehrere Definitionen erfüllen. Jede Hypothese wird auf allen Kandidaten ihrer Definition getestet, die Schnittmengen (Y1 und Y3, Y1 und Y2, alle drei) werden berichtet. Keine Prioritätsregel, keine Kombination vor der Validation.

**Sekundär, deskriptiv, nicht in der Holm-Familie:** Bullish Harami in der Tiefzone, Morning Star, Bullish Engulfing, Bullish Hikkake, jeweils mit Kontext und TA, mit denselben Metriken berichtet. Sie dienen keiner Systemauswahl in dieser Stufe. Sollen sie später eine Rolle spielen, brauchen sie eine eigene Vorregistrierung.

## 2. Einheitliche Exit-Baseline E-U (für Y1 bis Y3 identisch)

Gewinner laufen lassen, kein Ziel, kein Exit am Mittelwert. Zwei Regeln, beide immer aktiv, die frühere gilt:

Harter Boden: Chandelier `floor_t` = max(`floor_{t−1}`, HH_seit_Einstieg − 3.0 · ATR14_t), nur steigend, wirksamer Stop max(initialer Stop, Floor), Ausführung intraday als Stop-Market mit Slippage.

Struktureller Exit: Schluss unter dem zuletzt bestätigten Higher Low seit Einstieg (Library `structure_break` auf das letzte 3/3-bestätigte Swing Low nach dem Einstieg), Exit zur Eröffnung der Folgekerze. Solange seit dem Einstieg kein Swing Low bestätigt ist, gilt nur der harte Boden.

Keine Peak-Logik in Stufe A, keine individuelle Exit-Regel je Muster. Damit misst Stufe A Entry-Qualität bei konstantem Exit.

## 3. Kontrollgruppe (zentral für die Discovery)

Frage der Kontrollgruppe: War der bestätigte japanische Boden besser als ein vergleichbar stark gefallener BTC-Zeitpunkt ohne dieses Muster?

Für jedes Signal (Kandidat mit erfolgter Bestätigung) werden bis zu drei Kontrollzeitpunkte gezogen, deterministisch, vorab festgelegt: Kerzen mit erfülltem Kontext K1 bis K3, ohne das Muster der geprüften Hypothese (bei Y1 kein `failed_breakdown`, bei Y2 kein Double-Bottom-Kandidat, bei Y3 keine Wick-Volumen-Kerze) und ohne eines der beiden anderen primären Muster, innerhalb von ±90 Tagen um das Signal, mit `dd120` innerhalb ±3 Prozentpunkten und `ext` innerhalb ±0.5 ATR des Signals (zeit- und selloff-gematcht), die nächsten drei nach Abstand in `dd120`, nicht innerhalb von 12 Kerzen des Signals selbst und nicht innerhalb einer offenen Signalposition. Auf jeden Kontrollzeitpunkt wird derselbe Trigger TA (Schluss der Folgekerze über dem Hoch der Kontrollkerze), derselbe Stop (Tief der Kontrollkerze minus 0.5 ATR) und dieselbe Exit-Baseline angewandt, damit die Differenz allein dem Muster zuzurechnen ist und nicht dem Trigger. Kontrollzeitpunkte, bei denen TA nicht eintritt, verfallen wie Signale, die Verfallsquote wird für beide Gruppen berichtet.

Test je Hypothese: gepaarte Differenz (Signal gegen Mittel seiner Kontrollen) in Erwartung je Trade (R), MFE, Capture Ratio, Trade-Bootstrap 2000, Holm über Y1 bis Y3. Zusätzlich die unbedingte Referenz (Signal gegen exposure-gleiche Passivposition) als Bericht, nicht als Kriterium der Stufe A, weil sie die Frage der Kontrollgruppe nicht beantwortet.

Discovery-Kriterium «Signal vorhanden» je Hypothese: gepaarte Differenz der Erwartung gegen die Kontrollgruppe grösser null mit Bootstrap-5-Prozent-Perzentil über null nach Holm, Erwartung netto K1 über null, mindestens 30 bestätigte Signale (unter 30 «geringe Basis», unter 20 nur deskriptiv, vorab so festgelegt), beide Discovery-Blöcke (bis 2020, 2021 bis 2023) nicht negativ bei mindestens 10 Signalen je Block, Vorzeichen auf mindestens einer verschobenen Kerzenaggregation erhalten, sobald 1h-Daten vorliegen.

## 4. Discovery-Metriken je Signal (Diagnose, nie Signalinformation)

Für jedes Y1- bis Y3-Signal und jeden Kontrollzeitpunkt, berechnet in einem getrennten Modul ohne Zugriff auf die Signalbildung:

1. Abstand des Einstiegs zum ex-post lokalen Tief in ATR14 (Tief der 120 Kerzen vor bis 12 Kerzen nach dem Einstieg).
2. Maximum Favorable Excursion nach Einstieg in R und ATR, bis zum Exit und über 60 Kerzen.
3. Maximum Adverse Excursion in R und ATR.
4. Ob innerhalb von 7, 14, 30 und 60 Tagen ein neuer signifikanter Aufwärtstrend entsteht, vorab definiert als: Schluss über dem höchsten Hoch der 120 Kerzen vor dem Einstieg (neues 20-Tage-Hoch) innerhalb des Horizonts.
5. Trend Capture Ratio der Baseline E-U (realisierte Bewegung geteilt durch die Spanne vom relevanten Tief bis zum relevanten Hoch, Framework Abschnitt 14).
6. Klassifikation jedes Signals: «kurzfristiger Rebound» (MFE mindestens 1 R, aber kein neues 120-Kerzen-Hoch innerhalb von 30 Tagen), «mehrwöchiger Trend» (neues 120-Kerzen-Hoch innerhalb von 60 Tagen und Haltedauer unter E-U mindestens 30 Kerzen), «Fehlsignal» (Stop ohne MFE über 1 R). Anteile je Hypothese und je Kontrollgruppe.

Dazu je Signal: Einstiegspreis relativ zum Kandidatenschluss (Kosten der Bestätigung), Verfallsquote, Kerzengrenzen-Stabilität, Cross-Venue-Attribut, Tages- und Wochenkontext, Halving-Phase (nur Bericht in Stufe A).

## 5. Stufe B, Incremental Information

Erst nach Stufe A, auf denselben Signalen, ohne dass eine dieser Ebenen in Stufe A einen Einstieg erzeugt oder verhindert hat. Jede Ebene wird gegen die vorgesehene einfache Ersatzregel oder Kontrolle geprüft, gepaart, mit eigener Holm-Familie über die Stufe-B-Tests:

B1, Previous Open: Aufteilung der Signale nach `reclaim` von `open_d_prev` oder `open_w_prev` innerhalb der Bestätigung (Signale mit Reclaim gegen ohne), plus Trigger TC gegen TA als gepaarter Trigger-Vergleich, plus Informationswert der Niveaus mit Zufallskontrolle (Previous-Open-Spezifikation Abschnitt 4).
B2, Ichimoku Kijun: Y6 (Kijun-Reclaim als zusätzliche Bedingung nach TA) und Y7 (Kijun-Verlust als Exit nach Peak Candidate) je gegen die Ersatzregeln 26-Kerzen-Median und Einstieg plus 1 ATR (Ichimoku-Plan Abschnitt 1).
B3, MACD-Divergenz: Signale mit `bull_divergence` gegen ohne, gegen die Ersatzregel `mom10` an denselben Swing Lows.
B4, Halving-Kontext: bedingte Erwartung der Signale nach `cycle_phase`, explorativ, Permutation über Zyklen, nach dem Halving-Plan.

Keine Ebene wird aufgrund von Stufe B in die Validation aufgenommen, wenn sie die Ersatzregel nicht schlägt.

## 6. Japanische Peak Engine als Inkrement-Test (nach Stufe A)

Baseline E-U gegen E-U plus Peak-Evidenz: Exit zur Eröffnung der Folgekerze, wenn nach einem Peak Candidate (Failed Breakout über bestätigtes Swing High, Upper-Wick-Rejection in der Hochzone, Lower High nach neuem Hoch, Sakata-Spezifikation P1, P4, P5) gilt: `floor` ≥ Einstiegspreis (Position risikofrei, wie im Framework, damit Peak-Evidenz auf einem noch nicht etablierten Boden nicht die Umkehr abschneidet). Evening Star und 三山 laufen als Bericht mit. Gepaart auf denselben Signalen: Giveback (MFE minus realisiertes R), Erwartung je Trade, Summe der Top-10-Prozent-Trades, Anteil der Trades, die nach dem Peak-Exit noch mehr als 2 ATR stiegen. Frage: Schützt die Peak Engine Gewinne, oder beendet sie grosse Trends zu früh? Ein Test, eigene Familie.

## 7. YAMATO gegen BTC-RTC

Overlap Report wie v0.1, dazu getrennte Auswertung dreier Gruppen: nur YAMATO (Y1 bis Y3 ohne BTC-RTC-Kandidat innerhalb ±6 Kerzen), nur BTC-RTC, beide gleichzeitig. Je Gruppe Erwartung, MFE, Capture Ratio, Klassifikation nach Abschnitt 4. Frage: Haben gemeinsame Signale höhere MFE oder bessere Capture Ratio als Signale nur eines Systems? Bericht mit Bootstrap-Intervallen, kein Test, keine Kombination vor einer eigenen Vorregistrierung.

## 8. Erwartete Kandidatenzahl (Schätzung aus Überlegung, nicht aus Daten)

Discovery-Fenster BTC 2017-08 bis 2023-12, rund 14000 4h-Kerzen. Die Zahlen sind Erwartungen aus der Kenntnis des BTC-Verlaufs, nicht aus einer Zählung, weil die deskriptive Vorprüfung nach dem Freeze läuft, damit sie keine Auswahlwirkung haben kann. Selloff-Episoden mit K1 (mindestens 12 Prozent unter dem 20-Tage-Hoch): rund 40 bis 60 in 6.4 Jahren. Y1-Kandidaten: ein bis zwei Failed Breakdowns je Episode, rund 50 bis 90, davon nach TA bestätigt rund 30 bis 55. Y2-Kandidaten: Double Bottoms mit gültiger Nackenlinie rund 15 bis 30, alle per Definition bestätigt, also 15 bis 30 Signale, voraussichtlich unter der Schwelle von 30 und damit «geringe Basis» oder deskriptiv. Y3-Kandidaten: Wick-Volumen-Klimax rund 40 bis 70, bestätigt rund 25 bis 40. Vereinigt rund 60 bis 120 Kandidaten und 45 bis 85 Signale, mit Überlappung vor allem zwischen Y1 und Y3. Kontrollgruppe: bis zu drei je Signal, real wohl zwei im Mittel, also 100 bis 200 Kontrollzeitpunkte. Trifft die Vorprüfung nach dem Freeze deutlich andere Zahlen, wird das protokolliert, die Definitionen ändern sich nicht.

## 9. Multiplizität

Stufe A: Holm über drei (Y1, Y2, Y3). Stufe B: Holm über die vier Ebenen (B1 bis B4, mit Untertests innerhalb je Ebene als Bericht). Peak-Inkrement: ein Test. DSR-Trial-Zahl: 3 plus 4 plus 1 plus Jitter (Kontexte 0.10 und 0.15, 1.5 und 2.5 ATR, Toleranzen und Fenster der Sakata-Spezifikation, k 2.5 und 3.5, Volumen-z 1.0 und 2.0 für Y3) plus BTC-Vorbelastung 27 plus die Tests von BTC-RTC und BTC-B. Keine Auswahl nach CAGR, keine Auswahl einer Hypothese nach Ergebnis, alle mit «Signal vorhanden» gehen in die Validation.

## 10. Konfigurationsregel für die Validation (vorab)

Je Hypothese mit «Signal vorhanden»: Trigger TA (Y1, Y3) beziehungsweise Nackenlinienbruch (Y2), Exit E-U. Peak-Inkrement nur, wenn sein Test Giveback senkt, ohne Erwartung und Top-10-Prozent-Summe zu verschlechtern. Stufe-B-Ebenen nur, wenn sie ihre Ersatzregel schlagen, und dann als bedingte Aufteilung, nicht als Filter, bis die Validation sie bestätigt.

## 11. Offene Entscheidungen vor dem Freeze

1. Y3-Schwelle `volume_zscore` 1.5 bestätigen (Alternative 2.0, näher am kabutech-Beispiel, mit weniger Kandidaten).
2. Y2 ohne zusätzliche TA-Bestätigung (Empfehlung, Begründung Abschnitt 1) bestätigen.
3. Kontrollgruppe: drei Kontrollen je Signal, ±90 Tage, ±3 Prozentpunkte `dd120`, ±0.5 ATR `ext`, mit TA auf den Kontrollen (Empfehlung) bestätigen.
4. Exit-Baseline E-U mit Chandelier und Strukturbruch gleichzeitig (Empfehlung) oder Chandelier allein als Baseline und Strukturbruch als erstes Inkrement.
5. Schwellen der Klassifikation (neues 120-Kerzen-Hoch, 30 Kerzen Haltedauer) bestätigen.
6. Trade-Mindestzahl 30 mit Stufung 20 bestätigen.

Nach Klärung: Version 1.0, Prüfsumme in ENTSCHEIDE, gemeinsamer Freeze mit Framework, Library, BTC-Plan v0.2 und den vier YAMATO-Spezifikationen, deskriptive Vorprüfung (Kandidatenzählung), Look-ahead-Test, ein Discovery-Lauf Stufe A, danach Stufe B und Peak-Inkrement auf denselben Signalen.
