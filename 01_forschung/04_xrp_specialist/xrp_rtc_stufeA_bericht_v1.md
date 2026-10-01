# XRP-RTC Stufe A — Bericht des einmaligen Outcome-Laufs, Version 1

**Project Aurum II, `01_forschung/04_xrp_specialist/xrp_rtc_stufeA_bericht_v1.md`. 18.09.2026, 00:40 UTC. Lauf nach Spezifikation v1.0 (SHA 27fa0bd1…, eingefroren vor Outcomes), Library rlib v1.0 (f1ffdbb8…), Auswertungsskript `eval_cross.py`, Seed 20260918, Bootstrap 2000. Kandidaten aus der outcome-blinden Zählung (Prüfsummen im Skript verifiziert). Kostenmodell K1 massgebend. Evidenzklasse: Independent discovery. Ergebnisdatei `eval/eval_XRP.json`.**

## 1. Ergebnis in einem Satz

Keine der drei primären Familien liefert auf XRP ein Signal gegen die gematchten Kontrollen: X1 Failed Breakdown (68 Trades, 57 Paare) und X3 Wick plus Volumen (22 Trades, 14 Paare) sind netto negativ und von ihren Kontrollen nicht unterscheidbar, X2 Double Bottom (17 Trades, 17 Paare) erreicht zwar deutlich häufiger einen neuen Trend als seine Kontrollen, wird aber vom Exit vor dem Trend beendet und bleibt netto negativ. Status aller drei nach Regel v2: no evidence, inconclusive. Kein Fast Fail, kein Fast Promote, keine Validation. Die auf BTC entwickelte Mechanik generalisiert damit auf XRP nicht.

## 2. Primäre Familie (T0 beziehungsweise Nackenlinie, Exit E-U, Kosten K1)

| | X1 Failed Breakdown | X2 Double Bottom | X3 Wick plus Volumen |
|---|---|---|---|
| Kandidaten, Trades | 92, 68 (22 in Position, 2 Stop über 3 ATR) | 17, 17 | 29, 22 (4 Stop über 3 ATR, 3 in Position) |
| Gepaarte Kontrollen, Kontrolltrades | 57 Paare, 145 | 17 Paare, 44 | 14 Paare, 28 |
| Erwartung netto K1 (Mittel, Median) | −0.293 R, −0.962 R | −0.091 R, −0.339 R | −0.552 R, −0.611 R |
| Erwartung K0, K2 | −0.089, −0.630 | −0.012, −0.225 | −0.428, −0.761 |
| Trefferquote, Profit Factor | 29 Prozent, 0.61 | 18 Prozent, 0.68 | 27 Prozent, 0.16 |
| Kontrollen: Erwartung, Median, PF | −0.300 R, −1.215 R, 0.69 | −0.357 R, −0.799 R, 0.55 | +0.223 R (ein Trade +10 R), −1.216 R, 1.23 |
| Paarige Differenz ΔR: Mittel, Median | +0.030, −0.033 | +0.160, +0.205 | −0.981, +0.081 |
| Bootstrap-Intervall ΔR (Mittel, 5 bis 95 Prozent) | −0.476 bis +0.516 | −0.199 bis +0.531 | −2.232 bis +0.118 |
| Anteil positiver Paare, p_pos (Bootstrap) | 47 Prozent, 0.52 | 53 Prozent, 0.77 | 57 Prozent, 0.07 |
| MFE Median (Signal, Kontrolle), ΔMFE gepaart | 0.83 R, 0.78 R, −0.52 R | 0.46 R, 1.19 R, −1.44 R | 0.67 R, 0.68 R, −2.30 R |
| MAE Median | 0.62 R | 0.29 R | 0.59 R |
| Capture Ratio Median (Signal, Kontrolle) | −0.115, −0.100 | −0.070, −0.043 | −0.156, −0.140 |
| Klassen trend, delayed, rebound, fail | 15, 5, 15, 32 (+1 na) | 12, 0, 0, 5 | 6, 1, 6, 9 |
| Kontrollen trend plus delayed | 56 von 145 (39 Prozent) gegen 29 Prozent | 15 von 44 (34 Prozent) gegen 71 Prozent | 6 von 28 (21 Prozent) gegen 32 Prozent |
| Konzentration Top-1, Top-3 der Gewinne | 22.5, 51.9 Prozent | 75.1, 100 Prozent | 44.9, 72.4 Prozent |
| Block P1, P2 Erwartung (Signale) | −0.075 (n 38), −0.568 (n 30) | −0.287 (n 6), +0.016 (n 11) | −0.386 (n 9), −0.668 (n 13) |
| Block P1, P2 ΔR Median (Paare) | +0.179 (n 32), −0.351 (n 25) | +0.261 (n 6), −0.382 (n 11) | −0.704 (n 6), +0.120 (n 8) |
| Jahre positiv | 2 von 6 (2018, 2020) | 2 von 6 | 0 von 6 |
| Haltedauer Median, Exitgründe | 11 Kerzen; Chandelier 30, Stop 25, Struktur 7, Stop Einstiegskerze 6 | 12; Chandelier 14, Struktur 2, Gap 1 | 14.5; Chandelier 12, Stop 5, Struktur 4, Stop Einstieg 1 |
| Einstieg über ex-post Tief, Median | 2.9 ATR | 4.8 ATR | 2.3 ATR |
| Neuer Trend nach Exit abgeschnitten | 35 Prozent | 71 Prozent | 32 Prozent |
| Holm-p (Bootstrap, gepaart) | 0.97 | 0.69 | 0.97 |
| v1-Bedingungen a bis e | nein, nein, nein, ja, nein | nein, nein, ja, nein, nein | nein ×5 |
| v2-Kriterien Kontrolle, Verschiebung, keine Dominanz, Zeitkonsistenz | nein, nein, ja, nein (1 von 4) | nein, ja, nein, nein (1 von 4) | nein, nein, ja, nein (1 von 4) |
| Status nach v2 | no evidence, inconclusive | no evidence, inconclusive | no evidence, inconclusive |
| Fast Fail, Fast Promote, Validation | nein, nein, nein | nein, nein, nein | nein, nein, nein |
| Evidenzklasse | Independent discovery | Independent discovery | Independent discovery |

Lesart X1: Signal und Kontrolle sind praktisch dieselbe Verteilung (Mittel −0.29 gegen −0.30, Median −0.96 gegen −1.22, PF 0.61 gegen 0.69). Der Failed Breakdown fügt dem Kontext K1 bis K3 auf XRP keine Information hinzu. Kein Fast Fail, weil der Median der Paare bei −0.03 und der Anteil positiver Paare bei 47 Prozent liegt, also über der Fast-Fail-Schwelle 40 Prozent.

Lesart X2: Die Nackenlinienbrüche erreichen in 71 Prozent der Fälle innerhalb 30 Tagen ein neues 20-Tage-Hoch (Kontrollen 34 Prozent, Δtrend +0.41 mit Bootstrap-Intervall +0.20 bis +0.59), aber der Einstieg liegt im Median 4.8 ATR über dem Tief, das MFE erreicht nur 0.46 R gegen 1.19 R bei den Kontrollen, und der Chandelier 3 ATR14 beendet die Position nach im Median 12 Kerzen, in 71 Prozent der Fälle vor dem späteren Trend. Das ist derselbe Befund wie Y2 auf BTC (50 Prozent neue Hochs, Exit nach 15 Kerzen). Netto −0.09 R, 75 Prozent der Gewinne aus einem Trade, Median der Paare kippt ohne das beste Paar ins Negative. Kein Status über inconclusive.

Lesart X3: Netto klar negativ (−0.55 R, PF 0.16), der Kontrollmittelwert ist durch einen einzelnen Kontrolltrade mit +10 R verzerrt (Median −1.22). Auf Paarebene Median +0.08, Mittel −0.98, Blöcke gegenläufig. Inconclusive mit 14 Paaren.

Basisrate: Alle drei Kontrollgruppen sind netto negativ im Median (−1.2, −0.8, −1.2 R). Wie auf BTC ist der 4h-Bounce nach einem Selloff im Kontext K1 bis K3 auf XRP im Mittel ein Verlustgeschäft, mit oder ohne Muster.

## 3. Trigger-Familie (TA, TB gegen T0, Erwartung je Kandidat, Exit E-U)

X1, 92 Kandidaten: T0 68 Trades, Erwartung je Kandidat −0.216 R, je Trade −0.293 R. TA 21 Trades (62 ohne Bestätigung, 23 Prozent Bestätigungsquote), je Kandidat −0.069 R, je Trade −0.303 R, PF 0.49. TB 58 Trades (9 ohne Reclaim), je Kandidat −0.140 R, je Trade −0.221 R, PF 0.66. Gepaarte Differenz je Kandidat TA minus T0 +0.147 R (Bootstrap −0.092 bis +0.361, p_pos 0.86), TB minus T0 +0.077 R (−0.032 bis +0.177, p_pos 0.88). X3, 29 Kandidaten: T0 22 Trades, −0.419 R je Kandidat. TA 2 Trades, −0.016 je Kandidat. TB 16 Trades, −0.216 je Kandidat. TA minus T0 +0.403 R (p_pos 1.0), TB minus T0 +0.203 R (p_pos 0.99).

Lesart: TA und TB schneiden je Kandidat besser ab, weil sie weniger handeln, nicht weil sie besser handeln. Je Trade sind T0 und TA auf X1 gleich schlecht (−0.29 gegen −0.30 R), MFE und Capture identisch (0.83 gegen 0.80 R, −0.115 gegen −0.118). Der Trade-off «Signalzahl gegen Qualität» existiert auf XRP nicht, weil es keine Qualität zu verdünnen gibt. Innerhalb der Familie ist nach Holm nichts positiv, die Konfigurationsregel für die Validation greift nicht.

## 4. Exit-Familie (E-D und E0 gegen E-U auf denselben T0-Einstiegen)

X1: E-D 63 Trades, −0.651 R (Median −1.25), Haltedauer Median 14, Stop-Exits 42 von 63, Capture −0.20, Giveback Median 1.84 R. Gepaart gegen E-U auf 63 gemeinsamen Einstiegen: ΔR −0.379 R (p_pos 0.005, 9.5 Prozent der Paare positiv), ΔCapture −0.119 (p_pos 0.0), ΔGiveback +0.90 R. E0 69 Trades, −0.341 R, Haltedauer Median 4, ΔR gegen E-U −0.056 (p_pos 0.37), ΔCapture +0.042 (p_pos 0.96), ΔGiveback −0.75 R.
X2: E-D 16 Trades, +0.134 R Mittel bei Median −0.645, PF 1.23, Haltedauer Median 57.5 Kerzen (gegen 12), Capture −0.20, Giveback 1.61 R. Gepaart: ΔR +0.209 Mittel bei Median −0.417, 37.5 Prozent positiv, ΔCapture −0.058, ΔHaltedauer +43 Kerzen. E0 17 Trades, −0.150 R, ΔCapture +0.046.
X3: E-D 22 Trades, −0.203 R (Median −1.12), Haltedauer 37, ΔR +0.349 Mittel bei Median 0, 27 Prozent positiv, ΔCapture −0.015. E0 −0.436 R, ΔCapture +0.044.

Lesart: E-D verlängert die Haltedauer (X2 um 43 Kerzen im Median) und erhöht den Giveback (+0.75 bis +0.90 R), verbessert die Capture Ratio auf keiner Familie und verschlechtert sie auf X1 deutlich. Der Mittelwertgewinn auf X2 und X3 stammt aus wenigen langen Trades, der Median ist auf allen drei Familien schlechter oder gleich. E-D liefert längere Haltedauer, nicht mehr Trend Capture. Der Anteil abgeschnittener Trends sinkt mit E-D nicht (X1 35 gegen 35 Prozent, X2 71 gegen 63, X3 32 gegen 27): Die Trends beginnen später als jede der drei Exit-Logiken die Position hält. E0 (EMA20 oder 30 Kerzen) hat auf allen drei Familien die beste Capture Ratio und den geringsten Giveback, bei gleicher oder schlechterer Erwartung, also bestätigt sich die Kontrollarchitektur-Frage in Richtung Reversion, nicht Trend Capture.

## 5. Inkremente

RTC-1 (Volumen-z ≥ 1, Taker-Imbalance ≥ 0, Flow-Wechsel ≥ 0.10): X1 2 von 68, X2 0, X3 1 von 22. Status insufficient coverage, wie in der Zählung angekündigt, keine Regeländerung. RTC-2 (Funding-z ≤ −1 oder OI-z ≤ −1): X1 14 erfüllt gegen 28 nicht erfüllt (42 mit gültigen Merkmalen), Mittelwertdifferenz −0.166 R (Bootstrap −0.881 bis +0.606, p_pos 0.35): kein Inkrement. X2 0 von 12, X3 4 von 14: insufficient coverage.

## 6. Follow-through und Diagnosen

X1: Preisfortschritt nach 1, 3, 6 Kerzen im Mittel −0.13, −0.19, −0.31 ATR (der Markt fällt nach dem Einstieg im Mittel weiter), Taker-Imbalance nach Einstieg um null (0.01), Volumen-z leicht positiv (0.09 bis 0.27). X2: −0.24, −0.16, +0.28 ATR bei erhöhtem Volumen-z (0.6 bis 0.8). X3: −0.46, −0.15, −0.61 ATR. Einstiegseffizienz Median 0.54, 0.53, 0.56, Exit-Effizienz Median 0.48, 0.48, 0.21, Persistenz über dem Vor-Einstiegs-Hoch 12.5, 33 und 43 Prozent (letztere auf kleiner Basis). Signalüberlappung X1 und X3: 7 Kerzen.

## 7. Technische Provenance

Der erste Auswertungslauf enthielt in der Inkrement-Auswertung einen Berichtsfehler (Bootstrap über die Verkettung der Teilmengen statt über die Mittelwertdifferenz). Er wurde vor der Berichtserstellung korrigiert, das Skript neu ausgeführt, und die Abschnitte primäre Familie, Trigger-Familie und Exit-Familie des ersten und zweiten Laufs sind byteidentisch (gleicher Seed, gleiche Reihenfolge der Zufallsziehungen bis zum Inkrementabschnitt). Der erste Lauf ist unter `eval_XRP_run1_incbug/` aufbewahrt. Keine Regel, keine Schwelle, keine Definition wurde geändert.

## 8. Antworten, soweit XRP sie allein erlaubt

A. Die aus BTC entwickelte RTC-Mechanik generalisiert auf XRP nicht: Keine Familie schlägt ihre Kontrollen, alle drei sind netto negativ, die Statuszuweisung ist dreimal no evidence. B. T0 ist gegenüber TA kein besserer Trade-off, sondern derselbe Trade in dreifacher Menge. C. E-D liefert längere Haltedauer und mehr Giveback, keine höhere Capture Ratio. D. Konsistent mit BTC sind drei Dinge: die negative Basisrate der Kontrollen, die hohe Trendquote der Double Bottoms bei gleichzeitig zu frühem Exit (BTC 50 Prozent, XRP 71 Prozent abgeschnittene Trends), und die Wirkungslosigkeit der Bestätigungskerze. Die Cross-Coin-Zusammenfassung folgt nach dem DOT-Lauf.
