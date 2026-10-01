# XRP v0.4 und DOT v0.4 — Parameterprüfung vor dem Freeze, Version 1

**Project Aurum II, `01_forschung/00_gemeinsam/xrp_dot_parameter_audit_v1.md`. 17.09.2026. Frage: Welche Zahlen in XRP v0.4 und DOT v0.4 sind echte coinübergreifende Definitionen, welche wurden aus dem BTC-Parameterpaket v1.1 übernommen, und bei welchen ist die ökonomische Bedeutung nicht coinunabhängig, sodass ein coin-spezifischer Wert ex ante und regelbasiert abzuleiten ist. Grundlage sind ausschliesslich Preis- und Volatilitätsstatistiken der Discovery-Dateien, keine Signale, keine Outcomes. Die BTC-Zahlen werden nicht verändert.**

## 1. Ergebnis in einem Satz

Von den rund 40 Zahlen des Parameterpakets sind 31 in ATR-Einheiten, als z-Score oder als Zeitkonvention formuliert und damit coinunabhängig übertragbar. Vier Zahlen sind absolute Prozentwerte, deren Bedeutung mit der Volatilität des Coins wandert, und genau diese vier prägen Kontext und Matching: K1 (12 Prozent Rückgang), die Niveau-Penetration (0.1 Prozent), `at_low_structure` (2 Prozent) und die Matching-Toleranz `dd120` (±3 Punkte). Sie müssen für XRP und DOT vor dem Freeze regelbasiert neu gesetzt werden. Zwei weitere Zahlen (ΔOI 10 Prozent, Slippage) sind Konventionen mit Vorbehalt.

## 2. Volatilitätsstatistik der Discovery-Dateien (Preisdaten, keine Outcomes)

| Coin | Kerzen | ATR14 4h in Prozent des Schlusses, Median (P25 bis P75) | ATR14 Tag in Prozent, Median | Anteil Kerzen mit `dd120` ≤ −12 Prozent | 12 Prozent in ATR-Vielfachen | 0.1 Prozent in ATR | 2 Prozent in ATR |
|---|---|---|---|---|---|---|---|
| BTC | 13950 | 1.87 (1.34 bis 2.55) | 4.95 | 34.9 | 6.4 | 0.054 | 1.07 |
| ETH | 13950 | 2.41 (1.77 bis 3.28) | 6.48 | 42.1 | 5.0 | 0.042 | 0.83 |
| XRP | 12397 | 2.42 (1.81 bis 3.36) | 6.62 | 55.6 | 5.0 | 0.041 | 0.83 |
| DOT | 7381 | 3.05 (2.12 bis 4.05) | 7.78 | 53.0 | 3.9 | 0.033 | 0.65 |
| SOL | 7427 | 3.77 (2.73 bis 4.84) | 9.25 | 63.8 | 3.2 | 0.027 | 0.53 |

Lesart: Auf BTC bedeutet «12 Prozent unter dem 120-Kerzen-Hoch» einen Rückgang von 6.4 typischen ATR, auf DOT nur 3.9, auf SOL 3.2. Der BTC-Kontext K1 trifft auf 35 Prozent der BTC-Kerzen zu, auf XRP und DOT auf über die Hälfte, auf SOL auf fast zwei Drittel. Derselbe Zahlenwert beschreibt auf den Alts also keinen Selloff mehr, sondern den Normalzustand. Das ist der Fall, den der Nutzer meint: plausibel auf BTC, stillschweigend übernommen, ökonomisch nicht gleichbedeutend.

## 3. Einordnung jedes Parameters

**Gruppe A, in ATR-Einheiten definiert, coinunabhängig, unverändert übernehmen.** K2 `ext` ≤ −2.0 ATR innerhalb sechs Kerzen. K3 innerhalb 1.0 ATR eines Niveaus. Zonenbreite 0.5 ATR. Y1 beziehungsweise X1/D1: `lower_wick_atr` ≥ 0.5, Docht ≥ 1.5 Körper. Y2 beziehungsweise X2/D2: Toleranz zweites Tief −0.5 bis +1.0 ATR, Nackenlinie ≥ 2.0 ATR über den Tiefs, Verfall 0.5 ATR unter dem zweiten Tief. Y3 beziehungsweise X3/D3: `lower_wick_atr` ≥ 1.0, Docht ≥ 2.0 Körper, `close_location` ≥ 0.60 (Anteil, dimensionslos). Stop 0.5 ATR14 unter dem Strukturtief. Cap 3 ATR14 (X1, X3, D1, D3, Kontrollen, nicht X2/D2). Chandelier 3 ATR14 (E-U) und 3 Tages-ATR14 (E-D). Matching-Toleranz `ext` ±0.5 ATR. Alle diese Grössen skalieren mit ATR14 des jeweiligen Coins und behalten ihre Bedeutung.

**Gruppe B, standardisiert (z-Score), coinunabhängig, übernehmen.** `volume_zscore` ≥ 1.5 über 60 Kerzen (Jitter 1.0 und 2.0). `funding_zscore` ≤ −1 (RTC-2) und ≤ +1.5 (DOT-C, XRP-B+) über 270 Settlements. `basis_zscore` über 180. Ein z-Score ist per Konstruktion coinbezogen.

**Gruppe C, Zeit- und Strukturkonventionen, übernehmen, als Konvention ausweisen.** ATR14, EMA50, 120-Kerzen-Hoch und -Tief, 240 Kerzen für Swing-Niveaus und Double Bottom, Swing-Bestätigung 3 Kerzen, s2 − s1 ≥ 12, K2-Fenster 6 Kerzen, TB-Reclaim 6 Kerzen, Ein-Kerzen-Regel TA, Matching-Fenster ±540 Kerzen, Ausschluss 12 Kerzen, Follow-through 1, 3, 6 Kerzen, Klassifikation 30 und 60 Tage, Persistenz 30 Kerzen, Keltner-Kompression über 30 Kerzen, Ausbruch über 120 Kerzen, ΔOI über 5 Tage. Diese Zahlen definieren die Zeitskala des Mechanismus (Wochen bis Monate auf 4h). Sie sind nicht aus BTC-Outcomes abgeleitet, sondern aus dem Framework v0.1 vor jedem Lauf gesetzt, und ihre Bedeutung (Anzahl Kerzen) ist coinunabhängig. Eine coin-spezifische Zeitskala wäre eine andere Hypothese.

**Gruppe D, absolute Prozentwerte, coinabhängig, für XRP und DOT regelbasiert neu setzen.**

K1, `dd120` ≤ −0.12. BTC-Bedeutung: 6.4 typische ATR unter dem 120-Kerzen-Hoch. Zwei regelbasierte Wege, beide ohne Outcome: Weg 1, volatilitätsnormierte Form für alle Alt-Coins mit derselben Formel: `dd120_t` ≤ −6.0 · ATR14_{t−1} / C_{t−1}, Konstante 6 als gerundetes BTC-Äquivalent, festgelegt aus Tabelle 2. Ergebnis: Anteil Kontextkerzen BTC 36, XRP 45, DOT 37, ETH 36, SOL 33 Prozent, also erstmals über alle Coins vergleichbare Selektivität. Weg 2, fester Prozentwert, skaliert mit dem Median-ATR-Verhältnis zu BTC und auf ganze Prozent gerundet: XRP 16 Prozent (40 Prozent der Kerzen), DOT 20 Prozent (29 Prozent), ETH 16, SOL 25. Empfehlung: Weg 1, weil er eine Formel für alle Coins ist, sich innerhalb eines Coins an Regimewechsel anpasst (BTC 2018 mit 62 Prozent Kontextkerzen gegen 2023 mit 6 Prozent zeigt, wie stark der feste Prozentwert regimeabhängig ist) und keinen coin-spezifischen Zahlenwert mehr enthält, den man später anfassen könnte. Die höhere XRP-Selektivität von 45 Prozent bleibt auch in ATR-Form, sie spiegelt die langen XRP-Baissen 2018 bis 2020, nicht die Skalierung.

Niveau-Penetration bei Failed Breakdown, 0.001 (0.1 Prozent). BTC-Bedeutung: 0.054 ATR, also ein Bruchteil des Rauschens. Regel: 0.05 · ATR14_{t−1} für alle Coins, gerundetes BTC-Äquivalent. Damit misst die Penetration auf jedem Coin denselben Anteil der typischen Kerzenspanne.

`at_low_structure`, min(L, t−2..t) ≤ 1.02 · min(L, t−120..t−3). BTC-Bedeutung: 2 Prozent entsprechen 1.07 ATR. Regel: min(L, t−2..t) ≤ min(L, t−120..t−3) + 1.0 · ATR14_{t−1}, für alle Coins. Das ist zugleich konsistent mit K3 (1 ATR um ein Niveau).

Matching-Toleranz `dd120` ±0.03. Auf BTC ein Viertel der K1-Schwelle. Regel bei Weg 1: Toleranz ±1.5 ATR-Einheiten des normierten `dd120` (ein Viertel von 6). Regel bei Weg 2: ein Viertel des skalierten Prozentwerts, XRP ±4, DOT ±5 Punkte.

**Gruppe E, Konventionen mit Vorbehalt.**

ΔOI ≥ +10 Prozent über 5 Tage (DOT-C, XRP-B+, RTC-2 mit −10 Prozent). Eine relative Veränderung des Open Interest ist dimensionslos, ihre Verteilung ist aber coinabhängig (OI kleiner Coins schwankt stärker). Empfehlung: 10 Prozent beibehalten und als Konvention ausweisen, weil DOT-C und XRP-B+ verschachtelte Inkremente auf einer Teilmenge ab 2021-12 sind, deren Trades ohnehin unter der Mindestzahl bleiben, und weil eine z-Score-Form (`delta_oi_zscore`) eine neue Bibliotheksfunktion wäre. Alternative, wenn gewünscht: ΔOI als z-Score über 60 Tage mit Schwelle 1.0, vor dem Freeze zu entscheiden.

Taker-Imbalance ≥ +0.10 (DOT-C, XRP-B+) und ≥ 0 (RTC-1). Verhältnis von Taker-Buy zu Gesamtvolumen minus 0.5, dimensionslos, Streuung coinabhängig, aber die Schwelle 0 (RTC-1) ist eine reine Vorzeichenbedingung und coinunabhängig. 0.10 beibehalten, Konvention.

Kostenmodell K1 (Gebühr 0.40, Reibung 0.02, Slippage 0.05 Einstieg, 0.10 Stop). Die Gebühr ist börsenspezifisch und für alle Coins gleich. Die Slippage ist liquiditätsabhängig, XRP und DOT sind auf Kraken dünner als BTC. Für die Discovery bleibt K1 unverändert, weil das Kriterium «Signal vorhanden» gepaart gegen Kontrollen mit denselben Kosten misst und die Kosten dort weitgehend herausfallen. K2 (Stress) deckt die dünneren Bücher ab und wird berichtet. Coin-spezifische Slippage aus Kraken-Tiefe ist Sache der Validation, nicht der Discovery.

Keltner-Kompression `kelt_pct` < 0.20 (Lane B). Ist ein Perzentilrang der Kanalbreite innerhalb des Coins und damit coinunabhängig, Gruppe B.

Mindestzahl 30 und Stufung 20, Anteil positiver Paare 0.60, Konzentration 40 Prozent, Blockregel: Statistische Konventionen, coinunabhängig. Blockregeln sind bereits coin-spezifisch gesetzt (XRP mit Expansionsvermerk, DOT P2-Hälften).

## 4. Was das für den Freeze bedeutet

XRP v1.0 und DOT v1.0 übernehmen die Gruppen A bis C und E wörtlich. Für Gruppe D wird vor dem Freeze zwischen Weg 1 (ATR-Form) und Weg 2 (skalierter Prozentwert) entschieden, die gewählte Regel gilt für beide Coins identisch und später für ETH und SOL, ohne neue Entscheidung. Die Konstanten (6.0, 0.05, 1.0, 1.5) stehen in diesem Dokument und werden mit dem Freeze eingefroren. Die Kandidatenzählung nach dem Freeze darf die Wirkung zeigen, Outcomes nicht.

Ausdrücklich: Die BTC-Stufe-A-Regeln bleiben, wie sie sind. Sollte BTC später (Stufe B oder ein weiterer Lauf) in der ATR-Form von K1 gerechnet werden, wäre das eine outcome-informed Variante nach Governance v1 Abschnitt 2, kein Ersatz.

Zwei Nebenbefunde ohne Handlungsbedarf: Die Look-ahead-Sicherheit der ATR-Form ist gegeben, weil ATR14_{t−1} und C_{t−1} zum Zeitpunkt t bekannt sind. Und die Umsetzung in `ylib.py` ist eine Konfiguration im `FROZEN`-Dict je Coin (Feld `k1_mode` mit Werten `pct` oder `atr` und Konstante), kein neuer Codepfad für die Mustererkennung.
