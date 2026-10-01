# DB-CONTEXT — Bestätigter Double Bottom als temporärer bullischer Kontext, Vorregistrierung Version 0.1 für ETH und SOL

**Project Aurum II, `01_forschung/07_eth_sol_specialist/eth_sol_double_bottom_context_prereg_v0.1.md`. 18.09.2026. Status: Entwurf zur Prüfung vor dem Freeze, freeze-fähig nach Klärung von Abschnitt 8. Low-frequency mechanism nach Governance v1.1 Abschnitt 8. Hypothese outcome-informed, Ebene C, abgeleitet aus Y2 (BTC, Development), X2 und D2 (XRP, DOT, Independent discovery), die für diese Hypothese alle drei Development Evidence sind. ETH und SOL sind die einzigen unabhängigen Tests. Keine ETH- oder SOL-Daten wurden geladen, keine ETH- oder SOL-Outcomes berechnet. Alle Konstanten stammen aus den drei Development-Coins und werden vor dem Freeze festgeschrieben.**

## 0. Kernsatz

`confirmed double bottom ≠ immediate trade`, sondern `confirmed double bottom = temporary bullish context`. Der Nackenlinienbruch erzeugt keinen Einstieg mehr, sondern öffnet ein Kontextfenster, in dem drei getrennte, vorab definierte Einstiegsmechanismen zulässig sind. Kein Trade muss mehr gleichzeitig tief kaufen, die Reversion ernten und den Trend halten.

## 1. Development-Befund, der die Hypothese trägt (Zahlen aus den drei eingefrorenen Läufen)

Nach dem Nackenlinienbruch (Kandidatenkerze t) erreichen die Double Bottoms innerhalb 60 Tagen ein neues 20-Tage-Hoch in 50 Prozent (BTC, 14 Fälle), 71 Prozent (XRP, 17) und 47 Prozent (DOT, 15) der Fälle, gegen 34 bis 35 Prozent bei gematchten Kontrollen auf XRP und DOT. Der Median bis zum neuen Hoch liegt bei 75 Kerzen (XRP, DOT), auf BTC bei 206 Kerzen, also 12 bis 34 Tage. Der sofortige Trade am Nackenlinienbruch endete nach 11 bis 15 Kerzen, in 47 bis 71 Prozent der Fälle vor dem Trend, und war auf allen drei Coins netto negativ. Die Struktur ist also informativ über einen Zeitraum von Wochen, und die 4h-Umsetzung hat diesen Zeitraum nie gehalten. Gegenbefund, ebenfalls ausgewiesen: In 36 Prozent (BTC), 35 Prozent (XRP) und 53 Prozent (DOT) der Fälle schliesst der Kurs innerhalb 60 Kerzen unter dem zweiten Boden, der Kontext wird also in einem Drittel bis der Hälfte der Fälle schnell invalidiert.

## 2. Development-Prüfung der drei Einstiegsmechanismen (Häufigkeit und Timing, keine Trade-Outcomes)

Gemessen wurde auf den 14, 17 und 15 bestätigten Double Bottoms der Development-Coins ausschliesslich, ob und wann die drei Einstiegsbedingungen innerhalb 60 Kerzen nach t eintreten, ob sie vor einer Invalidierung eintreten, und ob danach ein neues 20-Tage-Hoch folgt. Es wurden keine Trades simuliert. Datei `dev_dbctx_refined.json`.

| | BTC (14) | XRP (17) | DOT (15) |
|---|---|---|---|
| Neues Hoch innerhalb 60 Tagen | 50 Prozent | 71 Prozent | 47 Prozent |
| Invalidierung (Schluss unter L2 in 60 Kerzen) | 36 Prozent | 35 Prozent | 53 Prozent |
| DB-C1 Retest (ab t+3, Tief ≤ N + 0.25 ATR, Schluss ≥ N − 0.5 ATR), Rate, Median Kerzen | 93 Prozent, 3 | 94 Prozent, 3.5 | 87 Prozent, 3 |
| Neues Hoch nach C1-Einstieg | 54 Prozent | 69 Prozent | 46 Prozent |
| Retest scheitert zuerst (Schluss unter N − 0.5 ATR) | 14 Prozent | 18 Prozent | 20 Prozent |
| DB-C2 Higher Low über Nackenlinie (bestätigtes Swing Low ≥ N − 0.5 ATR), Rate, Median Kerzen bis Bestätigung | 71 Prozent, 21.5 | 59 Prozent, 26.5 | 47 Prozent, 13 |
| Neues Hoch nach C2-Einstieg | 50 Prozent | 50 Prozent | 71 Prozent |
| DB-C3 Konsolidierungsbreakout (Schluss über dem Hoch der 18 Kerzen nach t, ab t+19), Rate, Median Kerzen | 50 Prozent, 35 | 29 Prozent, 39 | 47 Prozent, 26 |
| Neues Hoch nach C3-Einstieg | 29 Prozent | 60 Prozent | 71 Prozent |

Lesart, Development: Der Retest kommt fast immer und fast sofort (Median 3 Kerzen), er ist also kein Filter, sondern ein anderer Einstiegspreis, rund 0.5 bis 1 ATR tiefer als der Nackenlinienbruch, und wählt die Fälle nicht aus. Der Higher Low über der Nackenlinie kommt in der Hälfte bis zwei Dritteln der Fälle, im Median nach zwei bis vier Wochen, und die Trendquote danach ist auf XRP und DOT höher als ohne Auswahl (50 bis 71 Prozent). Der Konsolidierungsbreakout ist am seltensten (29 bis 50 Prozent), am spätesten (Median 26 bis 39 Kerzen) und auf XRP und DOT mit 60 bis 71 Prozent Trendquote am selektivsten, auf BTC nicht (29 Prozent, 7 Fälle). Eine erste Aussage über ein Auszahlungsverhältnis ist damit nicht möglich und wird bewusst nicht versucht. Ein zweiter Lauf mit anderen Konstanten findet nicht statt.

## 3. Spezifikation (Regeln ausschliesslich aus BTC/XRP/DOT abgeleitet)

Daten: Binance Spot ETHUSDT und SOLUSDT 4h Discovery-Dateien aus dem Manifest v1.1 (ETH 2017-08 bis 2023-12, SOL 2020-08 bis 2023-12), Flow-Dateien nur für Diagnosen. Normierung, Kontext, Struktur und Double-Bottom-Definition wörtlich wie XRP v1.0 (K1 in ATR-Form −6.0 auf s2, K2, K3 ATR-Form, ATR14, Swing k = 3, Toleranzen −0.5/+1.0 ATR, Nackenlinie ≥ 2 ATR, 12 ≤ s2 − s1 ≤ 240, jüngstes s1, Zeitordnung U8). Kontextöffnung: erster Schluss über der Nackenlinie N (Kerze t). Kontextfenster: t+1 bis t+60 (10 Tage) für die Einstiegsbedingungen, Kontext gilt bis 360 Kerzen nach t oder bis zur Invalidierung. Invalidierung: Schluss unter L_{s2}, danach keine Einstiege mehr aus diesem Double Bottom. Je Double Bottom höchstens ein Einstieg je Mechanismus, die drei Mechanismen sind getrennte Sleeves, keine Kombination, keine Auswahl.

DB-C1 Retest: erste Kerze b ≥ t+3 mit L_b ≤ N + 0.25 · ATR14_{t} und C_b ≥ N − 0.5 · ATR14_t. Einstieg zur Eröffnung b+1. Stop: N − 1.0 · ATR14_t (unter dem Retest-Toleranzband). Verfall, wenn zuerst eine Kerze mit L ≤ N + 0.25 ATR und C < N − 0.5 ATR auftritt (gescheiterter Retest) oder keine Retest-Kerze bis t+60.
DB-C2 Higher Low: erstes bestätigtes Swing Low s > t (bekannt ab s+3, s ≤ t+60) mit L_s ≥ N − 0.5 · ATR14_t. Einstieg zur Eröffnung s+4 (erste Kerze nach Bestätigung). Stop: L_s − 0.5 · ATR14_s. Verfall, wenn kein solches Swing Low bis t+60.
DB-C3 Delayed Continuation: Konsolidierungshoch CH = max(H, t+1..t+18). Erster Schluss über CH ab t+19 bis t+60. Einstieg zur Eröffnung der Folgekerze. Stop: min(L, t+1..b) − 0.5 · ATR14_b, begrenzt auf höchstens 3 ATR14_b unter dem Einstieg (sonst Verfall). Verfall ohne Breakout bis t+60.

Exit für alle drei Sleeves, ein einziger, vorab festgelegter Trend-Exit, weil der Kontext den Trend erfassen soll: Chandelier 3 · Tages-ATR14 vom höchsten Schluss seit Einstieg, nur steigend, plus Zeitstopp 360 Kerzen nach t (Ende des Kontexts), plus initialer Stop. Kein 4h-Chandelier, kein EMA20-Ziel, kein Strukturbruch. Begründung aus den Development-Coins: Der 4h-Chandelier hat den Trend dreimal abgeschnitten, das Tages-ATR-Chandelier als Vergleich (E-D) hielt die Positionen 40 bis 58 Kerzen und erreichte auf den Nackenlinien-Einstiegen die einzige positive Mittelwertdifferenz (XRP X2 +0.21 R Mittel). Das ist ein outcome-informed Grund, er wird als solcher ausgewiesen.

Kosten K1. Sizing Sicht 1. Fill-Regeln wie XRP v1.0 Abschnitt 8.

Kontrollgruppe, zwingend: Je Double Bottom drei gematchte Kontrollkontexte: Kerzen mit K1 bis K3 ohne Double-Bottom-Paar, innerhalb ±540 Kerzen, `dd120_atr` ±1.5, `ext` ±0.5 ATR, auf denen dieselben drei Einstiegsbedingungen relativ zu einem Ersatzniveau geprüft werden (Ersatz-Nackenlinie: max(H, t−18..t), Ersatz-L2: min(L, t−120..t)). Gleicher Exit, gleicher Stop. Die Frage lautet: Erzeugt der bestätigte Double Bottom bessere Retest-, Higher-Low- und Breakout-Einstiege als ein beliebiger Selloff-Kontext ohne Doppelboden.

Auswertung: Low-frequency-Regel (unter 20 Trades deskriptiv, 20 bis 29 low-frequency evidence, höchstens mechanistically promising, ab 30 normal), je Coin und je Mechanismus getrennt, Holm über drei Mechanismen je Coin, Regel v2 für den Status, Economic Validation Gate vor jeder Validation. Metriken wie XRP v1.0 plus: Anteil Einstiege je Double Bottom, Zeit von t bis Einstieg, Anteil invalidierter Kontexte vor Einstieg, Anteil abgeschnittener Trends.

## 4. Erwartete Zahlen auf ETH und SOL (Schätzung aus den Development-Coins, ohne ETH/SOL-Daten)

Bestätigte Double Bottoms: ETH 14 bis 20 (6.4 Jahre, BTC-ähnlich), SOL 12 bis 18 (3.4 Jahre, DOT-ähnlich, höhere Volatilität). DB-C1 Einstiege rund 90 Prozent davon, DB-C2 50 bis 70 Prozent, DB-C3 30 bis 50 Prozent. Erwartung: C1 erreicht auf ETH knapp die Stufe 20 bis 29, C2 und C3 bleiben auf beiden Coins deskriptiv unter 20. Das ist vor dem Lauf bekannt und wird so hingenommen, ein Lauf mit Pooling der Coins findet nicht statt.

## 5. Was diese Vorregistrierung nicht darf

Keine weiteren Einstiegsmechanismen, keine zweite Exit-Variante, keine Änderung der Toleranzen 0.25, 0.5, 1.0 ATR, 18 Kerzen, 60 Kerzen, 360 Kerzen nach Sicht auf ETH- oder SOL-Outcomes. Kein Rückgriff auf BTC-, XRP- oder DOT-Outcomes der drei Mechanismen (sie wurden nicht simuliert und bleiben unsimuliert, bis ETH und SOL eingefroren sind).

## 6. Trial-Zahl und Vorbelastung

Sechs Tests je Coin (drei Mechanismen, je gegen Kontrollen, Holm über drei) plus Vorbelastung ETH und SOL aus Stufe 2 und MTP-Validierung. Die drei Development-Coins zählen nicht als Trials für ETH und SOL, weil dort keine Outcomes dieser Mechanismen berechnet wurden.

## 7. Evidenzklasse und Deckel

Independent discovery auf ETH und SOL. Positive Ergebnisse rechtfertigen höchstens einen Validation-Lauf auf dem jeweiligen Holdout nach Economic Validation Gate. Ein späterer Test derselben Mechanismen auf BTC, XRP oder DOT wäre Development (outcome-informed durch die Struktur) und würde als solcher geführt.

## 8. Offene Entscheidungen vor dem Freeze

1. Exit: Tages-ATR-Chandelier mit 360-Kerzen-Zeitstopp als einziger Exit bestätigen, oder zusätzlich E-U als Vergleich (dann Holm über sechs statt drei je Coin).
2. Kontextfenster 60 Kerzen für die Einstiegsbedingungen bestätigen (Development: C2 und C3 im Median nach 13 bis 39 Kerzen).
3. Ersatzniveaus der Kontrollgruppe (max(H, t−18..t), min(L, t−120..t)) bestätigen.
4. Ob DB-C1 überhaupt geführt wird, da der Retest nach Development-Befund kein Filter ist (93 Prozent Rate, Median 3 Kerzen) und der Sleeve damit fast identisch mit dem Nackenlinien-Trade zu einem tieferen Preis wäre. Alternativen: führen wie spezifiziert, oder streichen und Holm über zwei.
