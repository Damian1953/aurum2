# Ideen-Scan v3: Screening S1–S3 (Ergebnis)

**Stand:** 2026-10-03 08:45 (Zürich, UTC+2). Spezifikation vor dem Rechnen committet (`ideen_scan_v3_plan.md` §4, Commit b1ac555). Skript `tools/ideen/screening_scan_v3.py`, Resultat `screening_v3.json`. Daten nur < 2024 (Binance Spot 1d, 7 Altcoins ohne ETH/SOL; CoinMetrics Community aus Scan v2). Kein Holdout. **3 informelle Trials, globaler Zähler rund 273**, Restbudget Scan v3: 11.

| Test | Ergebnis | Kill-Kriterium | Urteil |
|---|---|---|---|
| S1 BTC-Schock (> 2σ) → Altcoins Folgetag | 79 Signale, brutto +0.35 %/Tag (unbedingt +0.27 %), t 0.68; netto nach K1 −0.60 %; Hälften +0.48 % / +0.23 % | K-a (< 1.88 %), K-c (|t| < 2) | **Kill** |
| S2 Lead-Lag-Regression r_alt,t+1 auf r_btc,t | b = −0.07 (t −1.21); bis 2020 −0.13, ab 2021 +0.03 | K-b (Vorzeichenwechsel), K-c | **Kill** → F2 geschlossen |
| S3 Halving-Fenster (540 Tage nach 2016-07 und 2020-05) | Log-Rendite je Tag +0.47 % im Fenster gegen −0.04 % ausserhalb (Welch-t 3.6); Summe je Zyklus 3.06 und 1.99 | F1: N = 2 → nicht prüfbar | **Nicht prüfbar, kein Kandidat** |

## Lesart
- **F2 (Lead-Lag) gibt es auf Tagesbasis nicht.** Altcoins reagieren am Folgetag nicht systematisch auf BTC-Schocks; was existiert, liegt laut Literatur im Minuten- bis Stundenbereich und ist bei K1 nicht handelbar.
- **F1 (Halving) sieht stark aus, ist aber kein Beleg.** Zwei Zyklen, das Fenster von 540 Tagen ist Praktiker-Folklore und enthält genau die bekannten Bullenmärkte 2017 und 2020–21; die Tagesrenditen sind autokorreliert, der t-Wert ist deshalb nicht interpretierbar. Der Zyklus 2024 liegt im Holdout bzw. ist als Marktverlauf bekannt.
- **Nebenbefund für Linie B (nur Bericht, keine Änderung):** Die MVRV-Regel war im Halving-Fenster nur zu 53 % investiert (sonst 79 %), weil sie in der späten Phase der Halving-Bullenmärkte (MVRV > 3.5) aussteigt. Das ist die gewollte Mechanik von B, zeigt aber, dass B die stärkste Zyklusphase teilweise verpasst. Kein Anlass, B anzupassen (eingefroren, Moratorium).
