# REBOUND-MICRO v1.0 — Cross-Coin-Bericht (BTC, XRP, DOT), Version 1

**Project Aurum II, `01_forschung/10_rebound_micro/rebound_micro_cross_coin_bericht_v1.md`. 18.09.2026. Zusammenführung der drei versiegelten Development-Läufe nach `rebound_micro_spec_v1.0.md` (SHA 001a3853…). Keine Pooling-Statistik: jede Zahl gilt je Coin, die Zusammenschau ist eine Zählung übereinstimmender Vorzeichen. Einzelberichte `rebound_micro_bericht_{BTC,XRP,DOT}_v1.md`. Alle drei Läufe: Kandidatentabelle identisch mit der outcome-blinden Zählung v0.1, keine Regeländerung zwischen Coins, Holm über zwei Primary-Tests je Coin.**

## 1. Ergebnis in einem Satz

Der 1h-Reclaim (M1) liefert auf allen drei Development-Coins den vorab gemessenen engeren Stop (Median 0.42 bis 0.55 ATR14(4h) gegenüber 0.84 bis 0.89 bei T0), aber weder vor noch nach Kosten ein besseres Ergebnis als die unmittelbare Context-Execution T0 auf demselben Event, und nach K1 ist er auf allen drei Coins in beiden Primary-Zellen Fast Fail.

## 2. Primary-Zellen je Coin (K1, primär, und K0 als Sensitivität)

| Coin | Zelle | n | Mittel K1 | Zielrate | Stoprate | win/loss K1 | p_BE_emp K1 | Trefferquote K1 | Paare | Median Diff. K1 | Anteil positiv | Mittel K0 | Median Diff. K0 | Anteil positiv K0 | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTC | M1×Q0 | 84 | −0.95 | 49 % | 46 % | 0.66 | 0.60 | 23 % | 81 | −0.375 | 26 % | −0.27 | −0.14 | 31 % | Fast Fail |
| BTC | M1×Q1 | 80 | −0.98 | 34 % | 50 % | 0.84 | 0.54 | 22 % | 75 | −0.272 | 28 % | −0.23 | −0.13 | 32 % | Fast Fail |
| XRP | M1×Q0 | 64 | −0.82 | 41 % | 50 % | 0.65 | 0.61 | 30 % | 59 | −0.291 | 25 % | −0.20 | −0.12 | 34 % | Fast Fail |
| XRP | M1×Q1 | 69 | −0.89 | 36 % | 52 % | 0.72 | 0.58 | 25 % | 62 | −0.269 | 31 % | −0.26 | −0.13 | 34 % | Fast Fail |
| DOT | M1×Q0 | 37 | −0.63 | 38 % | 49 % | 0.62 | 0.62 | 38 % | 35 | −0.221 | 31 % | −0.16 | −0.05 | 37 % | Fast Fail |
| DOT | M1×Q1 | 42 | −0.93 | 26 % | 64 % | 0.93 | 0.52 | 24 % | 42 | −0.366 | 24 % | −0.39 | −0.13 | 26 % | Fast Fail |

Holm-adjustierte p-Werte der Primary-Tests: alle 1.000 (roh 0.85 bis 1.00). Bootstrap-Anteil positiver Mittelwerte p_pos nach K1: 0.00 bis 0.01 in allen sechs Zellen. Blöcke: in allen sechs Zellen beide Blöcke negativ (BTC P1/P2 −0.92/−0.99 und −0.97/−0.99, XRP −0.82/−0.81 und −1.02/−0.76, DOT P2a/P2b −0.25/−1.02 und −0.83/−1.33). Konzentration: grösster Gewinn 12 bis 46 Prozent der Gewinnsumme, Vorzeichen ohne besten Trade überall negativ. Promotion-Bedingung 3 (nicht negativ) und 7 (Baseline) in allen sechs Zellen verfehlt. Keine Zelle promoviert.

Baseline T0 auf denselben Events (K1): Q0 −0.59 / −0.39 / −0.26 R, Q1 −0.62 / −0.30 / −0.38 R (BTC / XRP / DOT). Vor Kosten (K0): Q0 −0.20 / −0.11 / 0.00, Q1 −0.20 / −0.01 / −0.10.

## 3. Frage A: Verbessert M1 die tatsächliche Reward/Loss-Geometrie gegenüber T0?

Getrennt zu beantworten. Das Verhältnis avg_win/|avg_loss| vor Kosten (K0) steigt in fünf von sechs Zellen gegenüber der Baseline (BTC 0.86 gegen 0.73 und 1.30 gegen 0.85, XRP 1.29 gegen 0.81, DOT 0.89 gegen 0.84 und 1.38 gegen 0.71), Ausnahme XRP Q1 (0.99 gegen 1.50). Die geometrische Break-even-Quote sinkt entsprechend auf 0.42 bis 0.54. Die realisierte Trefferquote vor Kosten liegt aber in allen sechs Zellen unter der eigenen Break-even-Quote (42 gegen 54, 35 gegen 43, 36 gegen 44, 39 gegen 50, 46 gegen 53, 29 gegen 42 Prozent) und unter der Trefferquote der Baseline (46, 42, 48, 40, 54, 52 Prozent). Ursache in den Kreuztabellen: Die Stoprate steigt von 37 bis 41 Prozent (T0) auf 46 bis 64 Prozent (M1), die Zielrate bleibt gleich oder sinkt (BTC Q0 49 gegen 45, sonst 26 bis 41 gegen 31 bis 45 Prozent). Der engere Stop wird häufiger getroffen, und ein erheblicher Teil der Baseline-Zeitstopps (kleine Verluste) wird bei M1 zu vollen Stops (BTC Q1 11 von 75 Paaren, XRP Q1 11 von 62, DOT Q1 4 von 42). Die gepaarte Differenz vor Kosten ist in allen sechs Zellen im Median negativ (−0.05 bis −0.14 R) mit 26 bis 37 Prozent positiven Paaren. M1 tritt im Median 3 bis 5 Stunden nach dem T0-Einstieg auf und teilt in 63 bis 78 Prozent der Paare die Ausstiegsart mit der Baseline.

Antwort A: Nein im Ergebnis. Die Geometrie je Trade verbessert sich, die Trefferquote verschlechtert sich stärker. Auf allen drei Coins, in beiden Zellen, vor Kosten.

## 4. Frage B: Überlebt die Verbesserung reale K1-Kosten?

Nein, und die Frage stellt sich nach A nicht mehr als Kostenfrage allein. Nach K1 beträgt das Mittel −0.63 bis −0.98 R je Trade, cost_R Median 0.57 bis 0.88 R (wie im Cost-Audit vorhergesagt), Profit Factor 0.19 bis 0.37. Der Kostenanteil macht aus einem vor Kosten leicht negativen Ergebnis (−0.16 bis −0.39 R) ein stark negatives. Die Baseline verliert nach K1 weniger (−0.26 bis −0.62 R), weil ihr Stop rund doppelt so weit ist und derselbe Rundlauf nur 0.34 bis 0.58 R kostet. Eine Maker-/Limit-Execution-Hypothese würde den Kostenanteil senken, aber nicht das Vorzeichen vor Kosten ändern. Sie ist deshalb für REBOUND-MICRO nicht vorzumerken.

## 5. Frage C: Liefert Q1/AVWAP einen wirtschaftlich besseren Rebound als Q0/EMA20?

Nein. Auf denselben M1-Trades (70, 58, 35 Events mit beiden Zellen) ist das Mittel Q1 minus Q0 −0.12 / −0.01 / −0.23 R, Median 0.00 (41 bis 49 Prozent der Paare enden identisch, meist am gemeinsamen Stop), Q1 in 21 / 26 / 20 Prozent der Fälle besser, Zielrate Q1 33 / 38 / 29 Prozent gegen Q0 49 / 40 / 37 Prozent. Der AVWAP liegt im Median 1.6 bis 1.8 ATR14(4h) entfernt und wird innerhalb von 24 Stunden zu selten erreicht, obwohl die Gewinne bei Erreichen grösser sind (avg_win 1.10 bis 1.58 R gegen 1.00 bis 1.04 R). Der Zeitstopp-Anteil liegt bei Q1 bei 10 bis 16 Prozent, bei Q0 bei 5 bis 14 Prozent.

## 6. Deskriptive Zellen und Flow

M2 (1h-Rejection): 3 / 4 / 2 bis 3 Trades je Coin, Mittel −0.09 bis +0.80 R (BTC Q1 +0.80 aus drei Trades, XRP Q1 +0.70 aus vier). M3 (Absorption): 0 bis 6 Trades, Mittel −0.03 bis −1.15 R. Status aller acht Zellen unverändert «descriptive / insufficient sample». Flow-Flag auf M1: 1 bis 2 Trades je Zelle, wie vorab festgehalten «insufficient coverage — not formally testable in v1.0». Harami-Teilmenge auf BTC 11 Trades, Mittel −1.6 bis −1.7 R, keine Statuswirkung. Kontrollgruppe (K1 und K2 ohne K3): 4 bis 17 Kontroll-Trades je Zelle, Mittel −0.59 bis −1.45 R, Differenz Zelle minus Kontrolle uneinheitlich (Median −0.59 bis +0.68, Anteil positiv 35 bis 67 Prozent bei 3 bis 17 Events). Die Location (K3) unterscheidet die Kontrollen nicht erkennbar von den Signalen. Diagnose ohne Statuswirkung.

## 7. Diagnosen ohne Hypothesenbildung

Anteil der Stop-outs, nach denen das Ziel innerhalb des Fensters dennoch erreicht wurde: Q0 26 / 19 / 33 Prozent, Q1 10 / 3 / 11 Prozent. Diese Zahl wird festgehalten, ohne daraus eine Stop-Variante abzuleiten (Forschungsplan: «Nicht: Wie machen wir den Stop enger» gilt auch umgekehrt). Nach erreichtem Ziel: MFE bis Kerze 24 Median 0.9 bis 1.9 R, neues 20-Tage-Hoch innerhalb 30 Tagen in 35 bis 55 Prozent, 30-Tage-Hoch 29 bis 44 Prozent. Das bestätigt die Trennung aus der Bottom-Engine-Notiz: Ein Teil der Ziel-Trades geht in einen Trend über, der Rebound-Sleeve selbst kann ihn mit festem Ziel nicht ernten. Erwartete Fallzahl ETH/SOL (nur Hochrechnung): M1-Zellen 39 bis 59 (ETH), 21 bis 31 (SOL). Sie bleibt ohne Bedeutung, weil keine Zelle promoviert wird.

## 8. Trial-Accounting und Multiplizität

Primär 2 je Coin (Holm), alle Tests p = 1.000. Vorbelastung BTC rund 30, XRP und DOT rund 37, global rund 240: Bei durchgängig negativen Rohwerten hat die Multiplizität keinen Einfluss auf die Statuszuweisung. Die sechs Primary-Zellen und die acht deskriptiven Zellen werden in jeder späteren Vorregistrierung derselben Coins als Vorbelastung geführt.

## 9. Statuszuweisung (Governance v1.1, keine Umetikettierung)

M1×Q0 und M1×Q1: auf BTC, XRP und DOT je «normal (≥ 30): Fast Fail» (Median der gepaarten Differenz < 0 und < 40 Prozent positive Paare bei ≥ 10 Paaren). M2 und M3: «descriptive / insufficient sample». Flow: «insufficient coverage». Promotion: keine. Nach Spec v1.0 Abschnitt 10 (A nein und B nein): REBOUND-MICRO wird nicht auf ETH und SOL verfolgt. Vorgeschlagener Eintrag: **REBOUND-MICRO v1.0 — Spezifikation abgeschlossen, keine Fortführung.** ETH und SOL bleiben unberührt (keine Daten geladen, keine Kandidaten, keine Outcomes). Bisher eingefrorene Ergebnisse unverändert. Der Vorbericht v0.1 bleibt mit seinem Erratum stehen.

## 10. Einordnung für die Roadmap (Vorschlag, keine Entscheidung)

Mit REBOUND-20 (abgeschlossen) und REBOUND-MICRO (abgeschlossen) sind zwei Formen des Rebound-Sleeves auf dem 4h-Kontext K1/K2/K3 geprüft: fester EMA20-/AVWAP-Zielpreis auf 4h und auf 1h. Beide scheitern vor Kosten an der Trefferquote, nicht erst an den Kosten. Die Baseline T0 selbst liegt vor Kosten bei 0.00 bis −0.20 R, das heisst der Kontext allein hat auf Rebound-Horizonten von 24 Stunden keinen erkennbaren Vorteil. Die einzige bisher mechanistisch vielversprechende Verwendung dieses Kontexts bleibt DOT D1 mit E-U (längere Haltedauer, Trend-Kontext, Validation zurückgestellt am Economic Gate). Das spricht dafür, im Bottom-Engine-Bild den Zweig «Trend Context → Delayed Trend Entry» zu priorisieren und den Zweig «Rebound Sleeve» ruhen zu lassen, bis ein grundsätzlich anderer Mechanismus (nicht Stop-, nicht Zielvariante) vorregistriert wird. Offen nach Roadmap v1.1 bleiben: BTC YAMATO Stufe B (Development, separat freizugeben), DB-CONTEXT (vier Entscheidungen), XS21 (vier Entscheidungen, Daten), Lane C und CoinGlass-Support.
