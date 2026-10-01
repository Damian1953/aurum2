# BTC YAMATO RTC — Forschungsplan, Version 1.1 (eingefroren)

**Project Aurum II, Strang 06_btc_specialist. 17.09.2026. Status: eingefroren als Version 1.1. Version 1.0 (SHA 56069bc0…) wurde am 17.09.2026 eingefroren, vor jeder Outcome-Auswertung. Version 1.1 ändert ausschliesslich einen formalen Spezifikationsdefekt in Y2 (Abschnitt 13a), alles andere ist wörtlich Version 1.0. Ersetzt Version 0.2 und Version 0.1 in der Teststruktur, übernimmt deren Spezifikationen (`btc_japanese_price_action_features_v0.1.md`, `btc_previous_open_levels_spec_v0.1.md`, `btc_sakata_bottom_peak_spec_v0.1.md`, `btc_ichimoku_increment_plan_v0.1.md`) unverändert. Quellenregel: `.jp`-Quellen. Alle Freeze-Urteile bleiben unangetastet. Struktur: zweistufige Discovery mit drei primären Bottom-Hypothesen, einheitlicher Exit-Baseline, gematchter Kontrollgruppe und getrennter Inkrement-Stufe, damit bei rund 60 bis 120 Kandidaten nicht sieben gleichrangige Tests laufen.**

## 0. Hypothese (unverändert)

Japanese Bottom Confirmation, Trend Capture, Peak Confirmation: Nach starken BTC-Rückgängen wird ein Boden erst nach Price-Action-Bestätigung gehandelt, der entstehende Trend gehalten, ohne festes Ziel, bis eine bestätigte Struktur- oder Peak-Evidenz vorliegt. Abschnitte 0, 1, 2, 3, 11, 13 und 14 der Version 0.1 (Hypothese, Verhältnis zu BTC-RTC und Vorbelastung, Multi-Timeframe-Kontext, Niveaus, Quellenzuordnung, Daten, Look-ahead) gelten unverändert.

## 1. Stufe A, Primary Bottom Discovery

Drei primäre Bottom-Hypothesen, alle mit demselben Kontext (K1 Selloff mindestens 12 Prozent unter dem 120-Kerzen-Hoch, K2 Extension mindestens 2 ATR unter EMA50 innerhalb der letzten sechs Kerzen, K3 innerhalb 1 ATR eines Niveaus der Bibliothek oder an der lokalen Low-Struktur), demselben Trigger, demselben Stop, demselben Sizing und demselben Exit. Sie unterscheiden sich ausschliesslich in der Kandidatendefinition.

**Y1, Failed Breakdown / Swing-Low-Reclaim.** Bestätigtes relevantes Swing Low (3/3-Bestätigung, nicht älter als 240 Kerzen) oder 120-Kerzen-Tief oder mehrfach getestete Zone, Kerze t handelt mindestens 0.1 Prozent darunter, schliesst wieder darüber, Lower-Wick-Rejection (`lower_wick_atr` ≥ 0.5 und LW ≥ 1.5 · B). Library `failed_breakdown`. Dann TA.

**Y2, Double Bottom / Sakata-Bestätigung.** Die algorithmische Double-Bottom-Struktur der Sakata-Spezifikation Abschnitt 2 (zwei bestätigte Swing Lows in 240 Kerzen, mindestens 12 Kerzen auseinander, zweites Tief im Band minus 0.5 bis plus 1.0 ATR, Zwischenhoch mindestens 2 ATR über den Tiefs als Nackenlinie). Bestätigung ohne Doppelung, vorab festgelegt: Die Nackenlinien-Bruchkerze (erste Kerze mit Schluss über der Nackenlinie) ist die Bestätigungskerze selbst, sie ersetzt TA, weil der Nackenlinienbruch die Sakata-Bestätigung des Bodens ist und ein zusätzliches «Schluss über dem Hoch der Bruchkerze» eine zweite Bestätigung derselben Aussage wäre. Einstieg zur Eröffnung der Kerze nach der Bruchkerze. Triple Bottom und 逆三尊 sind in Y2 enthalten (erster Nackenlinienbruch zählt), als Flag berichtet.

**Y3, Lower-Wick plus Volume Climax.** Kerze t mit `lower_wick_atr` ≥ 1.0, LW ≥ 2.0 · B, `close_location` ≥ 0.60 und `volume_zscore` ≥ 1.5 (ungewöhnliches Volumen, vorab gesetzt, angelehnt an die kabutech-Beschreibung des Selling Climax mit dreifachem Volumen). Dann TA. Die Werte 1.0 und 2.0 für `volume_zscore` sind ausschliesslich vorregistrierte Jitter- und Robustheitswerte. Sie ersetzen die Basisspezifikation unabhängig vom Ergebnis nicht. Zeigt Y3 nur bei 2.0 Informationswert, ist das ein Sensitivitätsbefund und keine bestandene Basisstrategie.

**Trigger TA (Y1, Y3):** Die folgende abgeschlossene 4h-Kerze schliesst über dem Hoch der Kandidatenkerze, Einstieg zur Eröffnung der übernächsten Kerze, sonst verfällt der Kandidat. Keine Intrabar-Annahme.

**Stop und Sizing:** initialer Stop unter der Kandidatenstruktur minus 0.5 ATR14 (Y1 unter dem Sweep-Tief, Y2 unter dem zweiten Tief, Y3 unter dem Kerzentief). Kein Trade bei Stop über 3 ATR für Y1 und Y3. Für Y2 entfällt diese Abbruchgrenze (Version 1.1, Abschnitt 13a), die reale Stopdistanz in ATR wird je Trade berichtet. Sicht 1 (2 Prozent des Sleeve-Startkapitals je R, ein weiter Stop führt zu entsprechend kleinerer Position, keine Mindestpositionsgrösse), eine Position, keine Add-ons.

**Überlappung:** Ein Kandidat kann mehrere Definitionen erfüllen. Jede Hypothese wird auf allen Kandidaten ihrer Definition getestet, die Schnittmengen (Y1 und Y3, Y1 und Y2, alle drei) werden berichtet. Keine Prioritätsregel, keine Kombination vor der Validation.

**Sekundär, deskriptiv, nicht in der Holm-Familie:** Bullish Harami in der Tiefzone, Morning Star, Bullish Engulfing, Bullish Hikkake, jeweils mit Kontext und TA, mit denselben Metriken berichtet. Sie dienen keiner Systemauswahl in dieser Stufe. Sollen sie später eine Rolle spielen, brauchen sie eine eigene Vorregistrierung.

## 2. Einheitliche Exit-Baseline E-U (für Y1 bis Y3 identisch)

Gewinner laufen lassen, kein Ziel, kein Exit am Mittelwert. Zwei Regeln, beide immer aktiv, die frühere gilt:

Harter Boden: Chandelier `floor_t` = max(`floor_{t−1}`, HH_seit_Einstieg − 3.0 · ATR14_t), nur steigend, wirksamer Stop max(initialer Stop, Floor), Ausführung intraday als Stop-Market mit Slippage.

Struktureller Exit: Schluss unter dem zuletzt bestätigten Higher Low seit Einstieg (Library `structure_break` auf das letzte 3/3-bestätigte Swing Low nach dem Einstieg), Exit zur Eröffnung der Folgekerze. Solange seit dem Einstieg kein Swing Low bestätigt ist, gilt nur der harte Boden.

Keine Peak-Logik in Stufe A, keine individuelle Exit-Regel je Muster. Damit misst Stufe A Entry-Qualität bei konstantem Exit.

## 3. Kontrollgruppe (zentral für die Discovery)

Frage der Kontrollgruppe: War der bestätigte japanische Boden besser als ein vergleichbar stark gefallener BTC-Zeitpunkt ohne dieses Muster?

Für jedes Signal (Kandidat mit erfolgter Bestätigung) werden bis zu drei Kontrollzeitpunkte gezogen, deterministisch, vorab festgelegt: Kerzen mit erfülltem Kontext K1 bis K3, ohne das Muster der geprüften Hypothese (bei Y1 kein `failed_breakdown`, bei Y2 kein Double-Bottom-Kandidat, bei Y3 keine Wick-Volumen-Kerze) und ohne eines der beiden anderen primären Muster, innerhalb von ±90 Tagen um das Signal, mit `dd120` innerhalb ±3 Prozentpunkten und `ext` innerhalb ±0.5 ATR des Signals (zeit- und selloff-gematcht), die nächsten drei nach Abstand in `dd120`, nicht innerhalb von 12 Kerzen des Signals selbst und nicht innerhalb einer offenen Signalposition. Auf jeden Kontrollzeitpunkt wird derselbe Trigger TA (Schluss der Folgekerze über dem Hoch der Kontrollkerze), derselbe Stop (Tief der Kontrollkerze minus 0.5 ATR) und dieselbe Exit-Baseline angewandt, damit die Differenz allein dem Muster zuzurechnen ist und nicht dem Trigger. Kontrollzeitpunkte, bei denen TA nicht eintritt, verfallen wie Signale, die Verfallsquote wird für beide Gruppen berichtet. Werden für ein Signal weniger als drei gültige Kontrollen gefunden, wird das Matching nicht erweitert (kein automatisches ±180 Tage), sondern die Abdeckung berichtet: Anteil der Signale mit drei, zwei, einer und keiner Kontrolle. Signale ohne Kontrolle fallen aus dem gepaarten Test und werden getrennt ausgewiesen. Eine breitere Matching-Sensitivität (±180 Tage, ±5 Prozentpunkte) ist als eigener, separat vorregistrierter Zusatz möglich, nicht Teil dieser Stufe. Ziel der Kontrollgruppe ist, den zusätzlichen Informationswert des Musters zu isolieren, nicht Muster und Bestätigung gemeinsam gegen einen unbestätigten Zufallseinstieg zu testen.

Test je Hypothese: gepaarte Differenz (Signal gegen Mittel seiner Kontrollen) in Erwartung je Trade (R), MFE, Capture Ratio, Trade-Bootstrap 2000, Holm über Y1 bis Y3. Zusätzlich die unbedingte Referenz (Signal gegen exposure-gleiche Passivposition) als Bericht, nicht als Kriterium der Stufe A, weil sie die Frage der Kontrollgruppe nicht beantwortet.

Discovery-Kriterium «Signal vorhanden» je Hypothese: gepaarte Differenz der Erwartung gegen die Kontrollgruppe grösser null mit Bootstrap-5-Prozent-Perzentil über null nach Holm, Erwartung netto K1 über null, beide Discovery-Blöcke (bis 2020, 2021 bis 2023) nicht negativ bei mindestens 10 Signalen je Block, Vorzeichen auf mindestens einer verschobenen Kerzenaggregation erhalten, sobald 1h-Daten vorliegen. Trade-Mindestzahl, vorab und nicht je Muster anpassbar: ab 30 bestätigten Signalen vollwertige Auswertung, 20 bis 29 «geringe Basis» mit ausdrücklichem Unsicherheitsvermerk und ohne dieselbe Evidenzstärke wie ein Setup mit mindestens 30, unter 20 nur deskriptiv. Für jede Kennzahl werden Bootstrap-Intervalle (5 und 95 Prozent) und deren Breite berichtet, nie die Trade-Zahl allein. Y2 wird bei 20 bis 29 Signalen vollständig berichtet, aber mit der zweiten Evidenzstufe geführt.

## 4. Discovery-Metriken je Signal (Diagnose, nie Signalinformation)

Für jedes Y1- bis Y3-Signal und jeden Kontrollzeitpunkt, berechnet in einem getrennten Modul ohne Zugriff auf die Signalbildung:

1. Abstand des Einstiegs zum ex-post lokalen Tief in ATR14 (Tief der 120 Kerzen vor bis 12 Kerzen nach dem Einstieg).
2. Maximum Favorable Excursion nach Einstieg in R und ATR, bis zum Exit und über 60 Kerzen.
3. Maximum Adverse Excursion in R und ATR.
4. Ob innerhalb von 7, 14, 30 und 60 Tagen ein neuer signifikanter Aufwärtstrend entsteht, strukturbezogen definiert: mindestens ein 4h-Schluss über dem höchsten Hoch der 120 vollständig vor dem Einstieg liegenden 4h-Kerzen (neues 20-Tage-Hoch) innerhalb des Horizonts. Prozent- (15 Prozent über Einstieg) und ATR-Definitionen (MFE 6 ATR14) nur als diagnostische Sensitivität, nie zur Baseline-Auswahl.
5. Trend Capture Ratio der Baseline E-U (realisierte Bewegung geteilt durch die Spanne vom relevanten Tief bis zum relevanten Hoch, Framework Abschnitt 14).
6. Klassifikation jedes Signals, vorab und ausschliesslich: «Trend» (neues 120-Kerzen-Hoch nach Punkt 4 innerhalb von 30 Tagen), «verzögerter Trend» (MFE mindestens 1 R und neues 120-Kerzen-Hoch erst zwischen Tag 31 und Tag 60, getrennt gekennzeichnet, nicht als Rebound gezählt), «kurzfristiger Rebound» (MFE mindestens 1 R, aber kein neues 120-Kerzen-Hoch innerhalb von 60 Tagen), «Fehlsignal» (Stop oder Exit ohne zuvor MFE mindestens 1 R). Dazu als Persistenzdiagnose, keine zweite Hürde: Anteil der Trends, bei denen der Schluss nach dem ersten neuen 120-Kerzen-Hoch mindestens 30 Kerzen über dem 120-Kerzen-Hoch vor dem Einstieg bleibt (die Bewegung war kein Ein-Kerzen-Spike), berichtet je Klasse. Anteile je Hypothese und je Kontrollgruppe, mit Bootstrap-Intervallen.

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

## 11. Entscheidungen vom 17.09.2026 (v0.2 Abschnitt 11, alle geschlossen)

1. Y3: `volume_zscore` ≥ 1.5 als Basisschwelle, 1.0 und 2.0 nur als vorregistrierte Jitter-Werte, ohne Ersatzwirkung.
2. Y2: Bestätigung allein durch den Nackenlinienbruch, kein zusätzliches TA.
3. Kontrollgruppe: drei gematchte Kontrollen je Signal, ±90 Tage, `dd120` ±3 Prozentpunkte, `ext` ±0.5 ATR, TA-Trigger und identische Stop-, Hold- und Exit-Logik auch auf den Kontrollen, keine automatische Erweiterung, Abdeckung berichten, breiteres Matching nur als separat vorregistrierter Zusatz.
4. Exit-Baseline E-U: Chandelier 3 ATR14 als harter Trailing Floor plus Schluss unter dem letzten bestätigten Higher Low, die zuerst ausgelöste Regel beendet den Trade, identisch für Y1, Y2, Y3 und deren Kontrollen. Kein Exit-Vergleich in Stufe A. «Chandelier allein gegen Chandelier plus Strukturbruch» ist ein späterer, eigener vorregistrierter Inkrement-Test, nur wenn mindestens eine Bottom-Hypothese Informationswert zeigt.
5. Klassifikation strukturbezogen (neues 120-Kerzen-Hoch), mit «verzögerter Trend» als eigener Klasse, 30-Kerzen-Komponente als Persistenzdiagnose, Prozent- und ATR-Definitionen nur als Sensitivität.
6. Mindestzahl 30, Stufung 20, nicht je Muster anpassbar, immer mit Bootstrap-Intervallen.

## 11a. Ergebnisstatus (Präzisierung ohne Kriterienänderung)

Jede Hypothese erhält nach dem Lauf einen von drei Status nach den eingefrorenen Kriterien: «supported» (Kriterium «Signal vorhanden» erfüllt, mindestens 30 Signale), «not supported» (mindestens 30 Signale, Kriterium nicht erfüllt), «inconclusive, insufficient sample» (unter 30 Signale: 20 bis 29 mit geringer Basis, unter 20 deskriptiv, mit Bootstrap-Intervallen berichtet). Negative Evidenz und unzureichende Testkraft werden strikt unterschieden. Ein «inconclusive» widerlegt die Marktmechanik nicht und eröffnet keine Parameteränderung. Die beobachtete TA-Bestätigungsquote ist selbst ein Forschungsbefund und begründet die Stufe-B-Frage H3 (Qualitätsgewinn der Bestätigung gegen den Preis weniger und späterer Einstiege), sie rechtfertigt keine Lockerung von TA in Stufe A.

## 12. Voraussetzungen aus Framework und Library für den Freeze der Stufe A

Stufe A verwendet aus dem Framework die Kontextschwellen K1 (12 Prozent), K2 (2 ATR innerhalb sechs Kerzen), K3 (1 ATR zum Niveau), den Stop-Puffer 0.5 ATR mit Abbruch über 3 ATR, k = 3.0, den Discovery-Schnitt 31.12.2023 und die Ein-Kerzen-Regel für TA. Aus der Library die Swing-Bestätigung 3/3, die Niveaudefinitionen (120 und 240 Kerzen, Zonen-Toleranz 0.5 ATR, drei Berührungen) und die Failed-Breakdown-Schwellen (Durchstich 0.1 Prozent, Docht 0.5 ATR und das Anderthalbfache des Body). Aus der Sakata-Spezifikation die Double-Bottom-Zahlen (240 Kerzen, Toleranz minus 0.5 bis plus 1.0 ATR, 12 Kerzen Abstand, Nackenlinie 2 ATR). Diese Zahlen werden mit dem Freeze dieses Plans zugleich eingefroren, die übrigen offenen Entscheidungen von Framework, Library und den YAMATO-Spezifikationen betreffen Stufe B, die Peak Engine und die anderen Coins und bleiben offen, ohne Stufe A zu berühren.

## 13a. Version 1.1: Behebung des Y2-Spezifikationsdefekts

Befund nach dem Freeze von Version 1.0, aus der Kandidatenzählung und ohne Outcome-Auswertung: Die eingefrorene Y2-Definition enthält einen inneren Widerspruch. Die Nackenlinie liegt definitionsgemäss mindestens 2 ATR über den Tiefs, der Einstieg erfolgt erst nach dem Nackenlinienbruch, der Stop liegt 0.5 ATR unter dem zweiten Tief, und zugleich schliesst die Regel «kein Trade bei Einstieg minus Stop über 3 ATR» solche Trades aus. Die Risikogrenze macht die Sakata-Bestätigung strukturell weitgehend unhandelbar (14 Kandidaten, 0 Trades, Abstände 3.1 bis 7.3 ATR). Das ist kein Marktergebnis, sondern ein Spezifikationsdefekt.

Änderung in Version 1.1, ausschliesslich: Für Y2 entfällt die 3-ATR-Abbruchgrenze. Unverändert bleiben Double-Bottom-Definition, zweites Tief, Nackenlinie, Nackenlinien-Schluss als Bestätigung und Einstiegssignal, Einstieg zur nächsten handelbaren Eröffnung, Stop «zweites Tief minus 0.5 ATR», Sizing (risikobasiert, konstantes nominelles Kapitalrisiko, kein Mindestnotional) und sämtliche übrigen Regeln, für Y1, Y3 und die Kontrollen gilt die 3-ATR-Grenze weiter. Die reale Stopdistanz in ATR wird je Y2-Trade berichtet. Ein Stop unter der Bruchkerze ist keine Reparatur, sondern eine neue Risikohypothese, und darf später nur als separat vorregistrierte Y2-Execution-Sensitivity untersucht werden, falls Y2 Informationswert zeigt.

Audit: Version 1.0 wurde vor jeder Outcome-Auswertung eingefroren. Bekannt waren zum Zeitpunkt der Änderung ausschliesslich Kandidatenzahlen, Bestätigungs- und Statusquoten und die Entry-Stop-Distanzen. Keine P&L-, MFE-, R-, Gewinn-, Verlust-, Capture- oder sonstigen Outcome-Werte wurden gelesen. Der Defekt wurde allein aus der logischen Beziehung der eingefrorenen Regeln und den Distanzen erkannt.

Freeze-Paket Stufe A: dieser Plan, `btc_sakata_bottom_peak_spec_v0.1.md` (Abschnitte 1 bis 3), die genannten Abschnitte der Library und des Frameworks, je mit Prüfsumme in ENTSCHEIDE. Danach: Datenvalidierung mit Abdeckungstabelle, Umsetzung der Library, Look-ahead-Test, deskriptive Vorprüfung (Kandidatenzählung, ohne Auswahlwirkung), ein Discovery-Lauf Stufe A auf der abgeschnittenen Datenkopie.
