# DOT-RTC Stufe A — Bericht des einmaligen Outcome-Laufs, Version 1

**Project Aurum II, `01_forschung/05_dot_specialist/dot_rtc_stufeA_bericht_v1.md`. 18.09.2026, 01:05 UTC. Lauf nach Spezifikation v1.0 (SHA 172229d3…, eingefroren vor Outcomes), Library rlib v1.0 (f1ffdbb8…), Auswertungsskript `eval_cross.py` (SHA 3975f2b2…, identisch mit dem XRP-Lauf), Seed 20260918, Bootstrap 2000. Kandidaten aus der outcome-blinden Zählung (Prüfsummen im Skript verifiziert). Kostenmodell K1 massgebend. Evidenzklasse: Independent discovery. Ergebnisdatei `eval/eval_DOT.json`. Keine Änderung zwischen XRP- und DOT-Lauf.**

## 1. Ergebnis in einem Satz

Auf DOT schlagen zwei der drei Familien ihre gematchten Kontrollen: D1 Failed Breakdown (54 Trades, 52 Paare, ΔR Median +0.21 R, 67 Prozent positive Paare, beide Blöcke positiv) und D3 Wick plus Volumen (16 Trades, 16 Paare, ΔR Median +0.50 R, 81 Prozent positiv, beide Blöcke positiv) erhalten nach Regel v2 den Status «mechanistically promising» mit je 3 von 4 Kriterien, D2 Double Bottom (15 Trades, 13 Paare) bleibt inconclusive. Der Vorbehalt ist gewichtig und gehört in denselben Satz: Keine der drei Familien ist netto positiv (D1 −0.17 R, D3 −0.33 R bei K1), der Vorsprung entsteht, weil die Kontrollen auf DOT noch deutlich schlechter sind (D1-Kontrollen −0.65 R Mittel, −1.29 R Median, Trefferquote 16.5 Prozent). Nach der eingefrorenen Regel ist D1 (54 Trades, über 20) validation-eligible, D3 (16 Trades, unter 20) nicht. «Formal supported» erreicht keine Familie, das Holm-korrigierte Kriterium «Signal vorhanden» ist nicht erfüllt (netto K1 unter null, Holm-p 0.056 und 0.048).

## 2. Primäre Familie (T0 beziehungsweise Nackenlinie, Exit E-U, Kosten K1)

| | D1 Failed Breakdown | D2 Double Bottom | D3 Wick plus Volumen |
|---|---|---|---|
| Kandidaten, Trades | 75, 54 (21 in Position) | 15, 15 | 17, 16 (1 in Position) |
| Gepaarte Kontrollen, Kontrolltrades | 52 Paare, 133 | 13 Paare, 34 | 16 Paare, 36 |
| Erwartung netto K1 (Mittel, Median) | −0.168 R, −0.894 R | −0.335 R, −0.379 R | −0.328 R, −0.918 R |
| Erwartung K0, K2 | +0.028, −0.494 | −0.269, −0.450 | −0.184, −0.570 |
| Trefferquote, Profit Factor | 33 Prozent, 0.76 | 13 Prozent, 0.20 | 25 Prozent, 0.50 |
| Kontrollen: Erwartung, Median, Trefferquote, PF | −0.650 R, −1.289 R, 16.5 Prozent, 0.39 | −0.585 R, −1.183 R, 21 Prozent, 0.41 | −1.052 R, −1.378 R, 8 Prozent, 0.19 |
| Paarige Differenz ΔR: Mittel, Median | +0.524, +0.214 | +0.092, +0.335 | +0.801, +0.503 |
| Bootstrap-Intervall ΔR Mittel (5 bis 95 Prozent) | +0.078 bis +0.988 | −0.431 bis +0.565 | +0.168 bis +1.502 |
| Bootstrap-Intervall ΔR Median | +0.080 bis +0.505 | −0.368 bis +1.020 | +0.334 bis +1.322 |
| Anteil positiver Paare, p_pos (Bootstrap) | 67 Prozent, 0.97 | 62 Prozent, 0.64 | 81 Prozent, 0.98 |
| MFE Median (Signal, Kontrolle), ΔMFE gepaart | 0.80 R, 0.89 R, −0.09 R | 0.39 R, 0.58 R, −1.33 R | 0.39 R, 0.85 R, −0.31 R |
| MAE Median | 0.52 R | 0.19 R | 0.65 R |
| Capture Ratio Median (Signal, Kontrolle), ΔCapture | −0.115, −0.122, +0.02 | −0.208, −0.127, −0.13 | −0.169, −0.158, 0.00 |
| Klassen trend, delayed, rebound, fail | 15, 2, 15, 22 | 7, 0, 0, 8 | 5, 0, 3, 8 |
| Trend plus delayed: Signal gegen Kontrolle | 31 gegen 39 Prozent | 47 gegen 35 Prozent | 31 gegen 36 Prozent |
| Konzentration Top-1, Top-3 der Gewinne | 23.8, 46.3 Prozent | 76.4, 100 Prozent | 83.6, 98.7 Prozent |
| Top-Paar-Anteil an Σ positiver ΔR, Median ohne bestes Paar | 16 Prozent, +0.20 | 22 Prozent, +0.33 | 31 Prozent, +0.44 |
| Block P2a, P2b Erwartung (Signale) | −0.252 (n 21), −0.233 (n 29) | −0.345 (n 9), −0.709 (n 4) | +0.053 (n 5), −0.364 (n 9) |
| Block P2a, P2b ΔR Median (Paare) | +0.165 (n 20), +0.248 (n 28) | +0.808 (n 8), −0.280 (n 3) | +0.324 (n 5), +0.890 (n 9) |
| P1 (2020-09 bis 12, nicht als Block gewertet) | 4 Trades, Jahr 2020 +2.95 R | 2 Trades, +0.91 R | 2 Trades, −2.24 R |
| Jahre positiv | 2 von 4 (2020, 2022) | 1 von 4 | 1 von 4 |
| Haltedauer Median, Exitgründe | 12; Chandelier 21, Stop 19, Struktur 10, Stop Einstieg 4 | 11; Chandelier 14, Struktur 1 | 6; Chandelier 9, Stop 6, Struktur 1 |
| Einstieg über ex-post Tief, Median | 2.2 ATR | 5.1 ATR | 2.9 ATR |
| Neuer Trend nach Exit abgeschnitten | 39 Prozent | 47 Prozent | 38 Prozent |
| Holm-p (Bootstrap, gepaart) | 0.056 | 0.36 | 0.048 |
| v1-Bedingungen a bis e | ja, nein, ja, ja, nein | nein, nein, ja, nein, nein | ja, nein, ja, nein, nein |
| v2-Kriterien Kontrolle, Verschiebung, keine Dominanz, Zeitkonsistenz | ja, nein, ja, ja (3 von 4) | ja, nein, ja, nein (2 von 4) | ja, nein, ja, ja (3 von 4) |
| Status nach v2 | mechanistically promising | no evidence, inconclusive | mechanistically promising |
| Fast Fail, Fast Promote | nein, nein | nein, nein | nein, nein |
| Validation-eligible (MP und mindestens 20 Trades) | ja (54 Trades) | nein | nein (16 Trades) |
| Evidenzklasse | Independent discovery | Independent discovery | Independent discovery |

Lesart D1: Der Vorsprung gegen die Kontrollen ist auf DOT konsistent, in beiden P2-Hälften positiv (Median +0.17 und +0.25 R), ohne Einzeltrade-Dominanz (Top-Paar 16 Prozent, Median ohne bestes Paar +0.20), mit Bootstrap-Intervall des Medians +0.08 bis +0.51 R. Es ist aber ein Vorsprung innerhalb einer verlierenden Klasse: D1 verliert bei K1 im Mittel 0.17 R je Trade (Median −0.89), gewinnt 33 Prozent der Trades, hat einen Profit Factor von 0.76 und wäre nur ohne Kosten (K0 +0.03 R) knapp positiv. Die Kontrollen verlieren 0.65 R. MFE, Capture und Trendquote unterscheiden sich nicht von den Kontrollen (Kriterium 2 nicht erfüllt), das heisst, der Failed Breakdown verbessert nicht das Aufwärtspotenzial, sondern vermeidet einen Teil der Fehlsignale des Kontexts (Trefferquote 33 gegen 16.5 Prozent, Stop-Exits 23 von 54 gegen die Kontrollen). Nach der eingefrorenen Regel v2 ist das «mechanistically promising» und mit 54 Trades validation-eligible. Ob ein Validation-Lauf sinnvoll ist, obwohl die Erwartung netto negativ ist, ist eine Entscheidung des Nutzers, nicht dieses Berichts.

Lesart D3: Stärkster paariger Effekt des Laufs (Median +0.50 R, 81 Prozent positive Paare, beide Blöcke positiv, Holm-p 0.048), aber 16 Trades, davon 84 Prozent der Gewinne aus einem Trade, Median der Haltedauer 6 Kerzen, Persistenz 0, und die Kontrollen sind mit −1.05 R Mittel und 8 Prozent Trefferquote die schlechteste Gruppe des Laufs. Der Status «mechanistically promising» ist nach Regel v2 korrekt, die Validation-Schwelle von 20 Trades ist nicht erreicht, der Befund bleibt stehen und wird nach Governance v1 auf dem nächsten Coin (ETH, SOL) oder im Forward-Fenster erneut geprüft.

Lesart D2: Wie X2 und Y2: 47 Prozent Trendquote gegen 35 Prozent der Kontrollen, MFE 0.39 R gegen 0.58 R, Einstieg 5.1 ATR über dem Tief, Trefferquote 13 Prozent, 76 Prozent der Gewinne aus einem Trade, Blöcke gegenläufig (P2b nur 3 Paare). Inconclusive.

Basisrate: Die Kontrollgruppen sind auf DOT die schlechtesten der drei Coins (Median −1.2 bis −1.4 R, Trefferquoten 8 bis 21 Prozent). Der DOT-Selloff im Kontext K1 bis K3 setzt sich auf 4h im Regelfall fort.

## 3. Trigger-Familie (TA, TB gegen T0, Erwartung je Kandidat, Exit E-U)

D1, 75 Kandidaten: T0 54 Trades, je Kandidat −0.121 R, je Trade −0.168 R, PF 0.76. TA 23 Trades (44 ohne Bestätigung, 31 Prozent Bestätigungsquote), je Kandidat +0.013 R, je Trade +0.041 R (Median −0.25), PF 1.10, MFE 0.93 R, Capture −0.05. TB 46 Trades, je Kandidat −0.137 R, je Trade −0.223 R, PF 0.66. TA minus T0 je Kandidat +0.134 R (Bootstrap −0.105 bis +0.354, p_pos 0.83, 43 Prozent positiv), TB minus T0 −0.015 R (p_pos 0.41). D3, 17 Kandidaten: T0 16 Trades, −0.309 R je Kandidat; TA 1 Trade; TB 6 Trades, −0.238 R je Kandidat.

Lesart: Auf D1 ist TA die einzige Konfiguration des gesamten Laufs mit positiver Erwartung je Trade (+0.04 R, PF 1.10), und anders als auf XRP ist der Unterschied nicht nur Mengeneffekt: MFE 0.93 gegen 0.80 R, Capture −0.05 gegen −0.12, Trefferquote 39 gegen 33 Prozent. Die Basis ist mit 23 Trades klein, das Bootstrap-Intervall je Kandidat schliesst null ein (p_pos 0.83 unter der 0.80-Schwelle für formal, über Zufall), nach Holm innerhalb der Trigger-Familie nicht positiv. Auf DOT zeigt TA also einen Hauch von Qualitätsfilter, auf XRP keinen, auf BTC keinen. TB ist auf allen drei Coins wirkungslos gegen T0.

## 4. Exit-Familie (E-D und E0 gegen E-U auf denselben T0-Einstiegen)

D1: E-D 48 Trades, −0.228 R (Median −1.19), Stop-Exits 33 von 48, Haltedauer Mittel +23 Kerzen gegen E-U, Capture −0.22, Giveback 1.79 R. Gepaart: ΔR −0.023 (10 Prozent positiv), ΔCapture −0.115 (p_pos 0.0), ΔGiveback +1.02 R. E0 58 Trades, −0.337 R, ΔR −0.155, ΔCapture +0.034 (p_pos 0.91), ΔGiveback −0.74 R. D2: E-D −0.448 R, Haltedauer Median 40 (gegen 11), ΔR −0.112 (Median −0.37), ΔCapture −0.15 (p_pos 0.01). E0 −0.133 R, ΔR +0.202 (Median +0.32, 80 Prozent positiv, p_pos 0.95), ΔCapture +0.158 (p_pos 0.995). D3: E-D −0.682 R, ΔR −0.354 (6 Prozent positiv), ΔCapture −0.151 (p_pos 0.001). E0 −0.367 R, ΔR −0.039, ΔCapture +0.11 (p_pos 0.92).

Lesart: E-D ist auf DOT auf allen drei Familien schlechter als E-U in Erwartung und Capture Ratio und erhöht den Giveback um 0.7 bis 1.0 R. Der Tages-ATR-Chandelier hält den initialen Stop länger als einzigen Schutz (D1 33 von 48 Exits am initialen Stop), sodass die Verluste voll realisiert werden, ohne dass die Gewinne länger laufen. Der Anteil abgeschnittener Trends sinkt mit E-D nur marginal (39 auf 31 Prozent bei D1). E0 verbessert die Capture Ratio auf allen drei Familien (p_pos 0.91 bis 0.995) und ist auf D2 die einzige Konfiguration mit positiver paariger Differenz gegen E-U (+0.32 R Median, 80 Prozent positiv). Das ist derselbe Befund wie auf XRP: Die frühe Reversion (EMA20) ist auf 4h besser erfasst als der Trend.

## 5. Inkremente

RTC-1: D1 0 von 54, D2 1 von 15, D3 2 von 16, insufficient coverage. RTC-2 (Funding-z ≤ −1 oder OI-z ≤ −1): D1 19 erfüllt gegen 31 nicht (50 gültig), Mittelwertdifferenz −0.203 R (Bootstrap −0.864 bis +0.448, p_pos 0.33): kein Inkrement. D3 7 gegen 7, Differenz −1.027 R (Bootstrap −2.194 bis −0.007, p_pos 0.05): negative Funding- oder OI-Signale verschlechtern D3, auf 14 Trades, ohne Status. D2 insufficient coverage. Auf beiden Coins wirkt RTC-2 eher gegen als für die Hypothese.

## 6. Follow-through und Diagnosen

D1: Preisfortschritt nach 1, 3, 6 Kerzen im Mittel +0.10, −0.02, −0.01 ATR (flach, anders als XRP mit −0.13 bis −0.31), Taker-Imbalance um null, Volumen-z 0.07 bis 0.13. D2: −0.06, −0.19, −0.68 ATR. D3: −0.30, −0.74, −0.79 ATR bei hohem Volumen-z (0.74 bis 0.85), der Markt fällt nach der Klimax-Kerze weiter. Einstiegseffizienz Median 0.62, 0.40, 0.50, Exit-Effizienz 0.37, 0.46, 0.33, Persistenz 24, 43, 0 Prozent. Überlappung D1 und D3: 4 Kerzen.

## 7. Antworten, soweit DOT sie allein erlaubt

A. Die Mechanik generalisiert auf DOT teilweise und nur im relativen Sinn: D1 und D3 schlagen ihre Kontrollen konsistent, aber keine Familie ist netto positiv, und der Vorsprung ist vor allem eine Vermeidung der besonders schlechten DOT-Basisrate. B. Auf D1 ist TA je Trade besser als T0 (einziger positiver Sleeve des Laufs, +0.04 R, 23 Trades), je Kandidat nicht signifikant. C. E-D liefert längere Haltedauer, mehr Giveback und weniger Capture, auf allen drei Familien. D. Konsistent über BTC, XRP und DOT: negative Basisrate der Kontrollen, Double Bottoms mit hoher Trendquote und zu frühem Exit, TB wirkungslos, E0 mit bester Capture Ratio. Die Cross-Coin-Zusammenfassung folgt als eigenes Dokument.
