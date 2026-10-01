# REBOUND-20 — Selloff Rebound zur EMA20-Recovery, Vorregistrierung Version 0.1 für ETH und SOL

**Project Aurum II, `01_forschung/07_eth_sol_specialist/eth_sol_rebound20_prereg_v0.1.md`. 18.09.2026. Status: Entwurf, nicht freeze-fähig in dieser Form (Abschnitt 6). Eigenständiger Sleeve, keine Variante von RTC. Hypothese outcome-informed, Ebene C: abgeleitet aus den Läufen BTC Stufe A (Development), XRP v1.0 und DOT v1.0 (Independent discovery), die für diese Hypothese alle drei Development Evidence sind. ETH und SOL sind die einzigen unabhängigen Tests. Es wurden keine ETH- oder SOL-Daten geladen, keine ETH- oder SOL-Outcomes berechnet. Governance v1.1 gilt (Economic Validation Gate, Abschluss ohne Umetikettierung).**

## 1. Ausgangslage, ausdrücklich dokumentiert

Auf allen sechs untersuchten Familien von XRP und DOT (und auf den BTC-Stufe-A-Einstiegen, hier nachgerechnet) hatte der Exit E0 (Schluss über EMA20 oder 30 Kerzen, initialer Stop) die beste Capture Ratio und den geringsten Giveback gegenüber E-U und E-D (ΔCapture +0.03 bis +0.16, p_pos 0.84 bis 0.995). Das ist der relative Befund. Der absolute Befund ist ebenso klar: E0 blieb auf den Development-Coins netto negativ, XRP X1 −0.34 R, X3 −0.44 R, DOT D1 −0.34 R, D3 −0.37 R, BTC Y1 mit TA −0.35 R, mit T0 −0.49 R, jeweils K1. «E0 war relativ besser» ist deshalb keine Strategie, sondern eine Beobachtung über Exits. Ein Rebound-Sleeve braucht eine eigene Entry-Ökonomie, die vor jedem ETH- oder SOL-Outcome festgelegt wird.

Die Mechanik des Verlusts ist auf allen Development-Coins dieselbe: Wird die EMA20 erreicht, bringt der Trade im Mittel +0.33 bis +0.60 R (XRP X1 +0.52, DOT D1 +0.60), wird der Stop getroffen, kostet er −1.2 bis −1.4 R. Die EMA20 wird in rund der Hälfte der Fälle erreicht (XRP X1 36 von 69, DOT D1 29 von 58, DOT D3 8 von 16). Bei einer Trefferquote um 50 Prozent und einem Auszahlungsverhältnis von rund 0.5 zu 1.3 ist der Erwartungswert strukturell negativ. Ein Rebound-Sleeve muss also entweder das Auszahlungsverhältnis oder die Trefferquote verändern, und beides ist zum Einstiegszeitpunkt nur über den Abstand zur EMA20 und die Stopdistanz steuerbar.

## 2. Development-Prüfung der Mindestbedingung (nur BTC, XRP, DOT)

Zwei vorab benannte Formen mit je zwei vorab benannten Kandidatenwerten, mehr nicht. Form A: `distance_to_EMA20 = (EMA20_t − Open_e) / ATR14_t ≥ k` mit k ∈ {1.0, 1.5}. Form B, ökonomisch direkter: `distance_to_EMA20 / initial_risk = (EMA20_t − Open_e) / (Open_e − Stop) ≥ q` mit q ∈ {1.0, 1.5}. EMA20_t ist der Wert am Schluss der Kandidatenkerze, vor der Einstiegseröffnung bekannt. Auswahlregel, vor der Prüfung festgelegt: Gewählt wird der kleinste Wert, bei dem die E0-Erwartung netto K1 auf mindestens zwei der drei Development-Coins nicht negativ ist. Datei `dev_rebound20.json`.

| Coin, Familie, Trigger | n | Potenzial Median (ATR, R) | Kosten K1 in R | E0 alle | ATR ≥ 1.0: n, E0 | ATR ≥ 1.5: n, E0 | R ≥ 1.0: n, E0 | R ≥ 1.5: n, E0 |
|---|---|---|---|---|---|---|---|---|
| XRP X1 T0 | 69 | 1.46, 0.99 | 0.30 | −0.34 | 49, −0.30 | 33, −0.18 | 34, −0.33 | 10, −0.50 |
| XRP X3 T0 | 22 | 2.16, 1.10 | 0.15 | −0.44 | 18, −0.43 | 17, −0.47 | 14, −0.59 | 3, −0.68 |
| DOT D1 T0 | 58 | 1.45, 1.03 | 0.26 | −0.34 | 42, −0.35 | 24, −0.15 | 29, −0.30 | 9, +0.02 |
| DOT D3 T0 | 16 | 2.16, 1.05 | 0.22 | −0.37 | 13, −0.36 | 12, −0.30 | 9, −0.16 | 2, +0.60 |
| BTC Y1 TA (Stufe A) | 16 | 0.51, 0.27 | 0.18 | −0.35 | 3, −0.42 | 2, −0.46 | 0 | 0 |
| BTC Y1 T0 | 77 | 1.45, 0.96 | 0.28 | −0.49 | 61, −0.55 | 34, −0.82 | 33, −0.92 | 13, −1.20 |
| BTC Y3 T0 | 24 | 1.98, 0.97 | 0.16 | −0.58 | 22, −0.58 | 16, −0.75 | 11, −0.84 | 5, −1.17 |

Ergebnis der Auswahlregel: Kein Kandidat erfüllt sie. Kein Wert von k oder q macht die E0-Erwartung auf zwei von drei Development-Coins nicht negativ. Auf BTC verschlechtert ein grösserer Abstand zur EMA20 das Ergebnis monoton (Y1 T0 von −0.49 auf −1.20 R bei R ≥ 1.5), auf XRP und DOT verbessert ATR ≥ 1.5 das Ergebnis, ohne es positiv zu machen (−0.18, −0.15 R), und R ≥ 1.5 ist auf DOT D1 mit 9 Trades knapp positiv, auf XRP X1 mit 10 Trades klar negativ. Der Abstand zur EMA20 erhöht das Potenzial, aber nicht die Trefferquote, und ein grosser Abstand bedeutet auf BTC einen Markt, der weiter fällt. Das Median-Potenzial in R liegt auf allen Familien bei rund 1.0, das heisst, der typische Weg bis zur EMA20 ist genau eine Risikoeinheit, und davon werden im Mittel 0.5 R realisiert, bei 1.3 R Verlust im Gegenfall.

## 3. Sleeve-Definition (so, wie er bei Freeze-Fähigkeit eingefroren würde)

Datenquelle ETH und SOL: Binance Spot 4h Discovery-Dateien aus dem Manifest v1.1, Kontext und Normierung wie XRP v1.0 (K1 in ATR-Form −6.0, K2, K3 mit ATR-Form, ATR14, EMA50, EMA20 der Schlusskurse). Signal: qualifiziertes Bottom- oder Rejection-Signal, definiert als Failed Breakdown (X1-Definition) oder Wick plus Volumen (X3-Definition) auf der Kandidatenkerze t im Kontext. Trigger T0 (Eröffnung t+1). Stop: Strukturtief minus 0.5 ATR14, Abbruch über 3 ATR. Ziel: Schluss über EMA20 → Exit zur Eröffnung der Folgekerze, sonst Zeitstopp 30 Kerzen, initialer Stop, kein Chandelier. Mindestbedingung: eine der beiden Formen aus Abschnitt 2 mit einem festen Wert, der vor dem ETH/SOL-Freeze eingetragen wird. Kosten K1. Kontrollgruppe: Kontextkerzen ohne Muster mit derselben Mindestbedingung, gleicher Trigger, Stop, Exit. Kriterien nach Auswertungsregeln v1 mit Regel v2, Mindestzahl 30, Economic Validation Gate vor jeder Validation. Evidenzklasse auf ETH und SOL: Independent discovery. Keine Anpassung von K1, Stop, Ziel oder Mindestbedingung nach Sicht auf ETH- oder SOL-Outcomes.

## 4. Was diese Vorregistrierung nicht darf

Keine weiteren Kandidatenwerte, keine dritte Form der Mindestbedingung, keine Suche nach der besten Development-Teilmenge. Die Tabelle in Abschnitt 2 ist vollständig und wird nicht erweitert. Ein Wert, der auf einer Development-Teilmenge mit unter 20 Trades positiv ist (DOT D1 R ≥ 1.5, 9 Trades, DOT D3 R ≥ 1.5, 2 Trades), gilt nicht als Begründung.

## 5. Erwartete Zahlen auf ETH und SOL (Schätzung aus den Development-Coins, ohne ETH/SOL-Daten)

X1-artige Kandidaten mit T0: ETH rund 70 bis 110, SOL 50 bis 90 (aus der Kontextquote und den XRP/DOT-Zahlen). Mit ATR ≥ 1.5 bleiben rund 45 Prozent, mit R ≥ 1.5 rund 15 Prozent. Nur die ATR-Form erreicht voraussichtlich die Mindestzahl 30 je Coin.

## 6. Status und offene Entscheidung

Diese Vorregistrierung ist nicht freeze-fähig, weil die vorab festgelegte Auswahlregel keinen Wert liefert und die Development-Evidenz für einen positiven Erwartungswert des Sleeves in dieser Form fehlt. Sie wird nicht eingefroren, um ETH und SOL nicht mit einer Hypothese zu verbrauchen, die auf allen drei Development-Coins negativ ist. Drei neutrale Alternativen, keine davon ist eine Empfehlung:

Alternative 1, Falsifikationslauf: Freeze mit ATR ≥ 1.5 (dem Wert, der auf zwei von drei Development-Coins am wenigsten negativ war, mit ausgewiesenem Auswahlcharakter) und Lauf auf ETH und SOL als reiner Falsifikationstest der Aussage «Rebound zur EMA20 ist auf 4h nach Selloff nicht monetarisierbar». Kosten: ETH- und SOL-Outcomes für Bottom-Signale werden sichtbar, spätere Bottom-Hypothesen auf ETH und SOL sind dann nicht mehr unabhängig.

Alternative 2, Abschluss: REBOUND-20 als «Spezifikation abgeschlossen, keine Fortführung» führen, weil das Auszahlungsverhältnis 0.5 zu 1.3 bei 50 Prozent Trefferquote auf drei Coins strukturell negativ ist. ETH und SOL bleiben für DB-CONTEXT und spätere Hypothesen unberührt.

Alternative 3, neue Entry-Ökonomie als eigene Development-Arbeit auf BTC, XRP, DOT: Der Verlust entsteht am Stop (−1.3 R), nicht am Ziel. Eine andere Stoplogik (zum Beispiel Stop am Tief der Kandidatenkerze ohne 0.5-ATR-Puffer, oder Einstieg als Limit am Tief statt Market an der Eröffnung) veränderte das Auszahlungsverhältnis. Das wäre eine neue, outcome-informed Mechanik auf den Development-Coins, mit eigener Vorregistrierung, und erst danach ein ETH/SOL-Test. Kosten: Zeit, und ein weiterer Development-Zyklus auf denselben drei Coins.
