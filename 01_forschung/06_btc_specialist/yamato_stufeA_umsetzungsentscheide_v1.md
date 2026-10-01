# BTC YAMATO RTC, Stufe A — Umsetzungsentscheide vor jeder Ergebnisberechnung, Version 1

**Project Aurum II, `01_forschung/06_btc_specialist/`. 17.09.2026, nach dem Freeze von Plan v1.0 und Parameterpaket (SHA 56069bc0…, 98376c2d…). Diese Entscheide präzisieren technisch mehrdeutige Stellen der eingefrorenen Spezifikation. Sie wurden vor der Umsetzung der Kandidatenlogik und vor jeder Zählung oder Auswertung getroffen und ändern keine eingefrorene Zahl. Jede Präzisierung nennt die Mehrdeutigkeit, die Entscheidung und den Grund. Nach Sicht auf Zählungen oder Ergebnisse werden sie nicht geändert.**

## U1 Fensterlogik über Datenlücken

Mehrdeutigkeit: Die Binance-4h-Reihe hat im Discovery-Fenster 9 Lücken mit insgesamt 17 fehlenden Kerzen (2017 bis 2020, längste 7 Kerzen am 08./09.02.2018). «120 Kerzen» kann Kerzenindex oder Kalenderzeit heissen. Entscheid: Alle Fenster sind Kerzenindex-Fenster über die vorhandenen Kerzen. Eine Lücke verkürzt das Kalenderfenster geringfügig, ATR und True Range verwenden den vorigen vorhandenen Schluss. Kandidaten, deren 120-Kerzen-Fenster eine Lücke enthält, werden mit Flag `gap_in_window` berichtet, nicht ausgeschlossen. Grund: 17 Kerzen auf 13950 sind vernachlässigbar, Kalenderlogik würde Sonderfälle ohne Nutzen erzeugen.

## U2 ATR-Normierung, welche Kerze

Mehrdeutigkeit: Library sagt ATR_{t−1} für Grössenvergleiche der Kerze t, Framework sagt ATR14_t für Stop und Chandelier. Entscheid: Geometrie (`lower_wick_atr`, `ext`, K2, K3-Distanz, Zonen-Toleranz, Double-Bottom-Toleranzen und Nackenlinienhöhe) mit ATR_{t−1} beziehungsweise ATR der Kerze vor der jeweils bewerteten Struktur-Kerze, Stop und Chandelier mit ATR14 der Kerze, an deren Schluss sie berechnet werden. Wilder-ATR mit Startwert Mittel der ersten 14 True Ranges, die ersten 130 Kerzen (14 ATR plus 120 Fenster) sind Warmup ohne Kandidaten.

## U3 Swing-Bestätigung, Gleichstand

Mehrdeutigkeit: «kleiner als die Tiefs der drei Kerzen davor und danach» bei gleichen Tiefs. Entscheid: strikt kleiner in beiden Richtungen, Gleichstand ist kein Swing. Bestätigung auf Kerze s+3, verwendbar ab der Bewertung der Kerze s+3 (also für Niveaus «Stand t−1» ab t = s+4). Grund: strikte Regel ohne Nebenfälle, gleiche Tiefs sind auf 4h-BTC selten.

## U4 Niveau «Stand t−1» und Alter

Entscheid: `swing_low_level_t` ist das jüngste Swing Low s mit s+3 ≤ t−1 und t − s ≤ 240. `nbar_low_level_t` = min(L, t−120..t−3). Zone: Menge der bestätigten Swing Lows (s+3 ≤ t−1, t − s ≤ 240), Cluster um jedes Swing Low mit Band ±0.5 · ATR_{t−1}, gültig bei mindestens drei Swing Lows im Band, Zonenniveau = Median der Tiefs im Band, bei mehreren gültigen Zonen die dem Schluss nächste unterhalb oder, falls keine unterhalb, die nächste überhaupt. Grund: die Spezifikation nennt Toleranz und Berührungen, nicht das Niveau selbst, der Median ist die robuste Mitte.

## U5 K3, Vorzeichen der Distanz

Mehrdeutigkeit: «innerhalb 1 ATR eines Niveaus» sagt nicht, ob der Schluss über oder unter dem Niveau liegen darf. Entscheid: abs(C_t − L) / ATR_{t−1} ≤ 1.0 für mindestens eines der drei Niveaus, oder `at_low_structure_t` = 1. Grund: Ein Failed Breakdown schliesst per Definition knapp über dem Niveau, ein Kandidat mit Schluss knapp darunter (zweiter Test des Niveaus) ist ebenso «am Niveau».

## U6 Failed Breakdown, mehrere Niveaus

Entscheid: Das Flag ist gesetzt, wenn die Bedingung auf mindestens einem der drei Niveaus erfüllt ist. Alle erfüllten Niveaus werden im Kandidaten gespeichert (Bericht), der Stop bezieht sich auf das Kerzentief, nicht auf das Niveau. Bedingung «Kerze handelt unter dem Niveau»: L_t ≤ L · (1 − 0.001). Bedingung «schliesst darüber»: C_t > L strikt.

## U7 Y2, Kontextbewertung

Mehrdeutigkeit: Der Kontext K1 bis K3 ist für Y1 und Y3 auf der Kandidatenkerze definiert. Bei Y2 liegt die Kandidatenkerze (Nackenlinienbruch) mindestens 2 ATR über den Tiefs, dort sind K2 (Extension unter minus 2 ATR innerhalb sechs Kerzen) und K3 (am Niveau) strukturell meist nicht erfüllt, obwohl der Boden selbst im Kontext liegt. Entscheid: Für Y2 wird der Kontext auf der Kerze s2 (zweites Tief) bewertet, K2 mit dem Fenster s2−5..s2, K1 und K3 auf s2. Grund: Der Kontext soll den Selloff und die Lage des Bodens beschreiben, nicht die Bestätigungskerze. Für Y1 und Y3 bleibt es bei der Kandidatenkerze t, weil dort Kerze und Boden zusammenfallen.

## U8 Y2, Zeitpunkt und Eindeutigkeit

Entscheid: Ein Paar (s1, s2) ist ab der Kerze s2+3 (Bestätigung von s2) prüfbar. Kandidat ist die erste Kerze t ≥ s2+3 mit C_t > N und t − s1 ≤ 240, sofern zwischen s2 und t kein Schluss unter L_{s2} − 0.5 · ATR_{s2−1} lag (Verfall). Das Zwischenhoch h1 muss ein bestätigtes Swing High mit s1 < h1 < s2 sein, bei mehreren das höchste. Jede Kerze t kann höchstens einen Y2-Kandidaten auslösen, bei mehreren gültigen Paaren das mit dem jüngsten s2. Ein Paar, dessen Nackenlinie schon vor s2+3 gebrochen wurde (Schluss über N zwischen s2 und s2+2), wird beim ersten Schluss über N ab s2+3 Kandidat, wenn der Schluss dann noch über N liegt. Triple Bottom: Paare (s1, s2) und (s2, s3) erzeugen nach dem ersten Nackenlinienbruch keinen zweiten Kandidaten innerhalb von 12 Kerzen; ein Flag `triple` wird gesetzt, wenn ein drittes Tief im Band innerhalb 360 Kerzen vor s2 liegt.

## U9 Y3, Body null

Entscheid: LW ≥ 2.0 · B wird wörtlich geprüft, bei B = 0 ist die Bedingung erfüllt. Die übrigen Bedingungen (Docht ≥ 1 ATR, Close-Lage ≥ 0.60, Volumen-z ≥ 1.5) bleiben. `volume_zscore` mit Fenster t−60..t−1, SD null macht die Kerze nicht auswertbar.

## U10 Trigger TA und Einstiegszeitpunkt

Entscheid: TA ist erfüllt, wenn C_{t+1} > H_t strikt. Einstieg zur Eröffnung von t+2 (O_{t+2}), plus Slippage. Fällt die Kerze t+1 auf eine Lücke (t+1 ist die erste Kerze nach einer Lücke), gilt sie trotzdem als Folgekerze (U1). Für Y2 Einstieg zur Eröffnung der Kerze nach der Bruchkerze. Der initiale Stop wird bei der Kandidatenkerze fixiert (ATR14 der Kandidatenkerze) und durch den Trigger nicht neu berechnet. Prüfung «Einstieg − Stop > 3 ATR14» mit dem tatsächlichen Einstiegspreis und ATR14 der Kandidatenkerze.

## U11 Eine Position, Kandidaten während offener Position

Entscheid: Während einer offenen Position werden Kandidaten aller drei Hypothesen erfasst und als «während Position, nicht gehandelt» berichtet, aber nicht gehandelt. Nach einem Exit auf Kerze x ist der nächste handelbare Kandidat eine Kerze t > x (Exit-Kerze selbst nicht). Die drei Hypothesen teilen sich in der Zählung nicht eine Position: Jede Hypothese wird als eigener Sleeve simuliert (eine Position je Hypothese), damit die Tests Y1 bis Y3 unabhängig voneinander sind. Die Schnittmengen werden berichtet.

## U12 Chandelier, Startpunkt und Ausführung

Entscheid: HH seit Einstieg ist das höchste Hoch ab der Einstiegskerze e (einschliesslich) bis t. `floor_t` gilt für die Kerze t+1, ab der ersten Kerze nach dem Einstieg (`floor_e` aus HH_e und ATR14_e). Wirksamer Stop S_{t+1} = max(initialer Stop, floor_t). Ausführung in Kerze t+1: Wenn O_{t+1} ≤ S, Exit zu O_{t+1} minus Slippage (Gap durch den Stop); sonst wenn L_{t+1} ≤ S, Exit zu S minus Slippage. Einstiegskerze selbst: Stop gilt bereits ab dem Einstieg mit dem initialen Stop.

## U13 Strukturbruch-Exit

Entscheid: «letztes seit Einstieg bestätigtes Swing Low» ist das jüngste Swing Low s mit s ≥ e (Einstiegskerze) und s+3 ≤ t. Exit-Bedingung C_t < L_s strikt, Exit zur Eröffnung von t+1 minus Slippage. Ein Swing Low unterhalb des wirksamen Stops ist praktisch irrelevant, wird aber gleich behandelt. Konfliktregel innerhalb einer Kerze: Der Strukturbruch wird am Schluss von t festgestellt und zu O_{t+1} ausgeführt, ein Stop, der in t+1 ausgelöst würde, kommt nicht mehr zur Anwendung, weil die Position zur Eröffnung geschlossen ist. Wird in Kerze t selbst der Stop ausgelöst, ist der Stop der Exit, der Strukturbruch entfällt.

## U14 Kosten K1

Entscheid: wie in der MTP-Validierung, Spot-Modell Kraken Tier 1: Gebühr 0.40 Prozent je Seite, Reibung 0.02 Prozent je Seite, Slippage 0.05 Prozent beim Einstieg (Einstiegspreis mal 1.0005), 0.10 Prozent am Stop (Stop-Preis mal 0.999), Strukturbruch-Exit zur Eröffnung mit 0.05 Prozent Slippage. R netto = (Exit − Einstieg) / R_brutto minus Kosten in R. K0 (nur Gebühr 0.16 Prozent) und K2 (0.80 Prozent, Reibung 0.06, Slippage 0.15 und 0.30) als Bericht.

## U15 Kontrollgruppe, Reihenfolge und Ausschlüsse

Entscheid: Kontrollkandidaten sind alle Kerzen c mit K1 bis K3 auf c (Kontext wie Y1 und Y3, auf der Kerze selbst), ohne `failed_breakdown_c`, ohne Y3-Bedingung, ohne Y2-Kandidat auf c und ohne dass c innerhalb s2−3..s2+3 eines gültigen Y2-Paares liegt (damit der Boden eines Double Bottom nicht als Kontrolle dient). Für jedes Signal (Kandidat mit Bestätigung, gehandelt) werden Kontrollen gewählt mit abs(c − t) ≤ 540 Kerzen, abs(c − t) > 12, `dd120` innerhalb ±0.03, `ext` innerhalb ±0.5, c nicht innerhalb einer offenen Signalposition derselben Hypothese, Kontrollen desselben Signals mindestens 12 Kerzen auseinander. Auswahl: die drei mit kleinstem abs(`dd120_c` − `dd120_t`), bei Gleichstand die zeitlich näheren. Kontrollen dürfen für mehrere Signale verwendet werden (das wird berichtet). Auf jede Kontrolle: TA (C_{c+1} > H_c), Einstieg O_{c+2}, Stop L_c − 0.5 · ATR14_c, Abbruch über 3 ATR, Exit E-U, Kosten K1, Simulation als Einzeltrade ohne Positionskonflikt (jede Kontrolle wird einzeln simuliert, weil sie kein Sleeve ist).

## U16 Discovery-Schnitt und offene Positionen

Entscheid: Der Datensatz endet mit der Kerze 2023-12-31 20:00 UTC. Eine an dieser Kerze offene Position wird zum Schluss dieser Kerze mit Kosten geschlossen und als «offen am Schnitt» markiert (Bericht, nicht aus der Statistik entfernt). Kandidaten in den letzten zwei Kerzen können keinen Trigger mehr erhalten und gelten als verfallen mit Vermerk. Diagnosemetriken, deren Fenster über den Schnitt hinausreichen (60 Kerzen nach Exit), sind für die betroffenen Trades «nicht berechenbar» und werden als fehlend geführt, nicht abgeschnitten. Grund: Das Holdout bleibt unberührt.

## U17 Diagnose «relevantes Tief» und «relevantes Hoch»

Entscheid: relevantes Tief = min(L) über die Kerzen e−120..e+12 (e Einstiegskerze), relevantes Hoch = max(H) über e..x+60 (x Exit-Kerze), Spanne = Hoch − Tief. `entry_efficiency` = 1 − (Einstieg − Tief) / Spanne, `exit_efficiency` = 1 − (Hoch − Exit) / Spanne, `capture_ratio` = (Exit − Einstieg) / Spanne. Bei Spanne ≤ 0 nicht berechenbar. Vor-Einstiegs-Hoch für die Klassifikation = max(H) über e−120..e−1. Horizonte 7, 14, 30, 60 Tage = 42, 84, 180, 360 Kerzen ab e.

## U18 Blöcke und Zuordnung

Entscheid: Ein Trade gehört zum Block seiner Kandidatenkerze. P1 bis einschliesslich 2020-12-31 20:00, P2 ab 2021-01-01 00:00.

## U19 Sizing Sicht 1

Entscheid: Sleeve-Startkapital 100 (Einheiten), Risiko je Trade 2 Einheiten, Notional = 2 / (R_brutto / Einstieg), höchstens 100. Equity-Pfad nur für Berichte, alle Tests auf R je Trade.

## U20 Reproduzierbarkeit

Entscheid: Der Code liest ausschliesslich `BTCUSDT_4h_discovery.csv` (SHA 2d394fd1…), erzeugt Kandidaten-, Signal-, Kontroll- und Trade-Tabellen als CSV mit Prüfsummen, alle Zufallszahlen (Bootstrap) mit festem Seed 20260917, Look-ahead-Test mit Schnitt 30.06.2022 und Permutationstest wie Library Abschnitt 8.

## U21 (Nachtrag 17.09.2026, vor jeder Ergebnisberechnung) Referenzkerze des Kontrollgruppen-Matchings für Y2

Mehrdeutigkeit: U15 matcht Kontrollen auf `dd120` und `ext` «des Signals» innerhalb ±540 Kerzen. Für Y1 und Y3 ist die Signalkerze die Kandidatenkerze (Boden und Kerze fallen zusammen). Für Y2 ist die Kandidatenkerze die Nackenlinien-Bruchkerze, die 3 bis 36 Kerzen nach dem zweiten Tief liegt und dort keine Selloff-Merkmale mehr trägt (`dd120` −0.01 bis −0.35, im Median deutlich über der Kontextschwelle). Mit der Bruchkerze als Referenz finden 10 von 14 Y2-Signalen keine Kontrolle (Pool im Fenster median 0), weil der Kontrollpool per Definition aus Kontextkerzen besteht. Entscheid: Für Y2 ist die Referenzkerze des Matchings das zweite Tief s2 (Zeitfenster ±540 Kerzen um s2, `dd120` und `ext` an s2, Mindestabstand 12 Kerzen zu s2 und zur Bruchkerze, nicht innerhalb der offenen Y2-Position). Das ist dieselbe Logik wie U7 (Kontext für Y2 auf s2): Die Kontrollfrage lautet «war der bestätigte Doppelboden besser als ein vergleichbar stark gefallener Zeitpunkt ohne dieses Muster», und der vergleichbar gefallene Zeitpunkt ist der Boden, nicht die Bruchkerze. Die Kontrolle steigt nach ihrer eigenen TA-Bestätigung ein, das Y2-Signal erst nach dem Nackenlinienbruch, der spätere und höhere Einstieg ist Teil der Sakata-Bestätigung und wird als Differenz der Einstiegszeitpunkte berichtet. Mit s2 als Referenz: 8 von 14 Signalen mit drei Kontrollen, 3 mit zwei, 2 mit einer, 1 ohne (Mittel 2.29), Toleranzen unverändert. Entschieden aus Zählungen und Abdeckung, ohne Kenntnis von Outcomes.
