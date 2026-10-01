# REBOUND-MICRO — Promotion-Regeln, Version 0.1 (vor Outcome festgelegt)

**Project Aurum II, `01_forschung/10_rebound_micro/rebound_micro_promotion_rules_v0.1.md`. 18.09.2026. Diese Regeln werden vor dem ersten P&L-Lauf eingefroren und nachträglich nicht geändert. Sie entscheiden ausschliesslich, ob eine Vorregistrierung für ETH und SOL geschrieben werden darf. Sie sind keine Validation und kein Sleeve-Status. Governance v1.1 (Regel v2, Low-Frequency-Stufung, Economic Validation Gate) gilt zusätzlich.**

## 1. Geometrische und empirische Grössen, strikt getrennt

Geometrisch (outcome-blind, im Vorbericht): je Kandidat `entry_to_stop_ATR` (in ATR14(4h) der Kontextkerze und in ATR14(1h)), `entry_to_Q0_ATR`, `entry_to_Q1_ATR`, RR_geo = (Ziel − Einstieg − Kosten) / (Einstieg − Stop + Kosten), p_BE_geo = 1 / (1 + RR_geo). Diese Werte sagen, welche Trefferquote die Geometrie verlangt, nicht, welche erreicht wird.

Empirisch (erst nach dem Lauf): avg_win_R, avg_loss_R (netto K1), hit_rate, stop_rate, p_BE_emp = |avg_loss_R| / (avg_win_R + |avg_loss_R|). Referenz REBOUND-20: avg_win rund +0.5 R, avg_loss rund −1.3 R, p_BE 72 Prozent, Trefferquote rund 50 Prozent.

## 2. Promotion-Bedingung (alle sechs, numerisch)

Mindestens eine Architektur (eine Zelle Mx × Qy, dieselbe Zelle) erfüllt auf mindestens zwei der drei Development-Coins gleichzeitig:

1. Geometrie gegenüber REBOUND-20 verbessert: empirisches avg_win_R / |avg_loss_R| ≥ 0.80 (Referenz rund 0.40) und Median `entry_to_stop_ATR(4h)` ≤ 0.60 (Referenz 1.3 bis 2.0).
2. Keine extreme Break-even-Trefferquote mehr nötig: p_BE_emp ≤ 0.60.
3. Nach K1 nicht offensichtlich strukturell negativ: Mittel r_net (K1) ≥ −0.05 R und Bootstrap-Anteil positiver Mittelwerte p_pos ≥ 0.40 und Profit Factor ≥ 0.90.
4. Ausreichend Fälle: mindestens 30 Trades in der Zelle auf dem Coin, und die Kandidatenrate je 1000 auswertbare 1h-Kerzen, angewendet auf die ETH- und SOL-Discovery-Länge (aus den 4h-Manifest-Zeilen bekannt, ohne ETH/SOL-Daten zu laden), ergibt mindestens 30 erwartete Trades je Coin.
5. Keine Einzeltrade-Dominanz: grösster Einzelgewinn ≤ 40 Prozent der Summe der Gewinne, Vorzeichen des Mittels ohne den besten Trade erhalten.
6. Zeitliche Konsistenz: in mindestens zwei vorregistrierten Blöcken (P1/P2 für BTC und XRP, P2a/P2b für DOT) mit je mindestens 10 Trades ist das Mittel r_net (K1) ≥ −0.05 R.

Zusätzlich, weil der Vergleich mit der strukturellen Baseline der Kern der Hypothese ist: gepaarte Differenz je Kontext-Event zwischen der Zelle und dem 4h-Baseline-Trade mit Median > 0 und Anteil positiver Paare ≥ 0.55 auf denselben zwei Coins.

## 3. Was Promotion nicht bedeutet

Promotion erlaubt ausschliesslich das Schreiben und Einfrieren einer ETH/SOL-Vorregistrierung mit genau der promovierten Zelle (und ihrem nested Flow-Vergleich, falls M1 oder M2). Sie erlaubt keine Validation, keinen Sleeve, keine Produktion, keine Kombination mehrerer Zellen, keine Parameteranpassung. Positive Zellen unter 30 Trades (Low-Frequency-Stufe) lösen keine Promotion aus, auch nicht zu zweit. Wird keine Zelle promoviert, wird REBOUND-MICRO v0.1 als «Spezifikation abgeschlossen, keine Fortführung» geführt, ohne Umetikettierung.

## 4. Multiplizität

Je Coin Holm über die sechs Zellen für den gepaarten Baseline-Vergleich (Bootstrap-p der gepaarten Differenz). Die Promotion-Bedingung 3 verwendet Rohwerte, die Holm-Korrektur wird berichtet und in der ETH/SOL-Vorregistrierung als Vorbelastung geführt. Trial-Accounting in `rebound_micro_trial_accounting_v0.1.md`.
