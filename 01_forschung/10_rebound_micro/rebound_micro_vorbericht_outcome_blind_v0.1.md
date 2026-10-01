# REBOUND-MICRO — Outcome-blinder Vorbericht vor Freeze, Version 0.1

**Project Aurum II, `01_forschung/10_rebound_micro/rebound_micro_vorbericht_outcome_blind_v0.1.md`. 18.09.2026. Berechnet wurden ausschliesslich Kandidatenkerzen, Einstiegskerzen, Einstiegspreise, strukturelle Stops, Zielpreise (Q0, Q1) zum Einstiegszeitpunkt und die daraus folgende Geometrie. Keine Exits, kein P&L, keine r_net, keine realisierte Trefferquote, keine MFE/MAE, keine Stop- oder Zielergebnisse, keine Post-Entry-Renditen. Keine ETH- oder SOL-Daten. Library `mlib.py` v0.1, Zählskript `count_micro.py`, Ergebnisse `count_<COIN>.json` und `count_<COIN>.csv`. Tests 5 von 5 (Unit, Denominator, Join, AVWAP von Hand und Reset, Kandidaten-Look-ahead).**

## 1. 1h-Datenabdeckung BTC/XRP/DOT

Spot 1h Discovery: BTC 55698 Kerzen ab 2017-08-17, XRP 49537 ab 2018-05-04, DOT 29502 ab 2020-08-18. Perp 1h ab 2020-01 (BTC, XRP) und 2020-08 (DOT), nur Diagnose. Details im Datenaudit.

## 2. Lücken und Off-Grid

Spot: BTC 28 Lücken (170 Kerzen), XRP 25 (87), DOT 10 (19), alle bekannt und in der Library fail-closed. Off-Grid: BTC 43 Kerzen vom Februar 2018 quarantäniert, nicht in der Datei. Perp: XRP zwei mehrtägige Lücken 2022, BTC und DOT lückenlos. Kraken-1h-Naht nicht betroffen.

## 3. 4h-Kontext-Events mit vollständigem 1h-Fenster

Kontextkerzen (K1 ATR-Form, K2, K3) auf 4h: BTC 2240, XRP 2206, DOT 1374. Zusammenhängende Kontext-Events (Suchfenster sechs 4h-Kerzen): BTC 171, davon 158 mit lückenfreiem 1h-Fenster und Warmup (P1 68, P2 90); XRP 165, 148 vollständig (P1 65, P2 83); DOT 94, 89 vollständig (P2a 39, P2b 41, P1 nicht gewertet 9). K1-Episoden für den AVWAP-Anker: BTC 117, XRP 104, DOT 62, Median-Länge 24 bis 32 4h-Kerzen.

## 4. Kandidaten M1/M2/M3 (erster Kandidat je Event und Mechanismus, in vollständigen Fenstern)

BTC: M1 130 Kandidaten, davon 98 mit engem Invalidationspunkt (Einstieg minus Stop ≤ 1.0 ATR14(4h)) und 32 ausgeschlossen (`no_tight_invalidation`). M2 15, davon 3 eng, 12 ausgeschlossen. M3 12, davon 1 eng, 11 ausgeschlossen. XRP: M1 107, 79 eng, 28 ausgeschlossen. M2 13, 5 eng. M3 23, 6 eng. DOT: M1 63, 46 eng, 17 ausgeschlossen. M2 10, 4 eng. M3 22, 5 eng.

Befund, mechanisch: Nur M1 (1h-Reclaim eines 4h-Niveaus) liefert eine engere Invalidation in der Mehrzahl der Fälle (75 Prozent). M2 (1h-Rejection mit Docht ≥ 1 ATR14(1h) und Stop unter dem Docht) und M3 (Absorption plus Flow-Wende, Stop unter der Absorptionsspanne) erzeugen in 70 bis 92 Prozent der Fälle einen Stop, der nicht enger ist als die 4h-Struktur, weil die Rejection- oder Absorptionskerzen selbst 1.5 bis 2 ATR14(1h) hoch sind. M2 und M3 sind damit auf allen drei Coins Zellen unter 10 Fällen und werden rein deskriptiv bleiben. Absorptionskerzen (Sell-z ≥ 1, Effizienz ≤ 0.25) gibt es reichlich (BTC 3760, XRP 3195, DOT 2033 über die Discovery), die Sequenz bis zum Reclaim innerhalb des Kontextfensters ist selten.

## 5. Überschneidung M1/M2/M3 (Events, eng)

BTC: M1∩M2 3, M1∩M3 1, M2∩M3 0, M3 allein 0, Vereinigung 98. XRP: 3, 3, 1, alle drei 1, M3 allein 3, Vereinigung 84. DOT: 2, 3, 0, M3 allein 2, Vereinigung 50. Der nested Flow-Vergleich auf M1 ist praktisch leer: Flow-Transition vor der M1-Kandidatenkerze bei 2 von 98, 2 von 79, 2 von 46. M3 als Inkrement auf M1 ist damit nicht testbar (`insufficient coverage`, vor Outcome erkennbar).

## 6. Strukturelle 1h-Stopdistanz gegenüber 4h-T0

M1, eng: Einstieg minus Stop im Median 0.53 (BTC), 0.42 (XRP), 0.50 (DOT) ATR14(4h), entspricht 1.0 bis 1.1 ATR14(1h). Baseline (T0 an der Eröffnung nach der Kontextkerze, Stop Kontexttief minus 0.5 ATR14(4h)) im Median 0.86, 0.86, 0.76 ATR14(4h). Verhältnis 1h zu 4h im Median 0.56, 0.50, 0.52, Interquartil 0.39 bis 0.79. Die 1h-Struktur halbiert die Stopdistanz. Vermerk: Die REBOUND-20-Musterkerzen (Failed Breakdown mit langem Docht) hatten Stopdistanzen von 1.3 bis 2.0 ATR, die Baseline hier ist die Kontextkerze ohne Muster, deshalb 0.8.

## 7. Geometrisches Reward/Risk zu Q0 und Q1 (K1, nach Kosten)

M1 eng, Q0 (EMA20 4h) über dem Einstieg bei 84, 64, 37 Kandidaten; Abstand Einstieg bis Q0 im Median 0.78, 0.74, 0.86 ATR14(4h). RR_geo zu Q0 nach K1-Kosten im Median 0.29 (BTC), 0.34 (XRP), 0.49 (DOT), Anteil positiver RR 64, 74, 86 Prozent. Q1 (AVWAP der Episode) über dem Einstieg bei 80, 69, 42; Abstand im Median 1.7, 1.6, 1.8 ATR14(4h), Interquartil 0.5 bis 5.3, also weit und breit gestreut, weil der AVWAP am Beginn der Selloff-Episode ankert und damit oft hoch über dem aktuellen Kurs liegt. RR_geo zu Q1 im Median 1.07, 1.09, 1.54.

## 8. Geometrische Break-even-Trefferquote

p_BE_geo = 1 / (1 + RR_geo), Median M1 eng bei K1: zu Q0 0.64 (BTC), 0.58 (XRP), 0.59 (DOT); zu Q1 0.35, 0.31, 0.36. Bei K0: zu Q0 0.48, 0.46, 0.45. Bei K2: 0.72, 0.74, 0.56. Der entscheidende Befund dieses Vorberichts: Die Kosten je Trade in R liegen bei K1 im Median bei 0.90 (BTC), 0.87 (XRP), 0.68 (DOT) R, bei K0 0.22 bis 0.29 R, bei K2 1.5 bis 2.0 R. Ein enger Stop (R rund 1.1 bis 1.5 Prozent des Kurses) macht die Kraken-Tier-1-Kosten (rund 1 Prozent Rundlauf mit Slippage) zur dominanten Grösse. Die 1h-Struktur löst das Geometrieproblem gegenüber dem Ziel Q0 (RR steigt von rund 0.4 auf 0.3 bis 0.5 nach Kosten, vor Kosten auf 0.9 bis 1.2), aber die Kosten fressen den Gewinn wieder auf. Zu Q1 ist die Geometrie günstig (p_BE 0.31 bis 0.36), Q1 liegt aber im Median 1.6 bis 1.8 ATR entfernt, was eine deutlich niedrigere Trefferquote erwarten lässt. Ob die empirische Trefferquote über oder unter diesen Schwellen liegt, ist die offene Frage des Laufs und wird hier nicht berechnet.

## 9. Flow-Felder und Datenqualität

Spot-Flow vollständig, Rolling-z gültig auf 92 bis 94 Prozent der Kerzen (Lücken fail-closed). Perp-Join an Kandidaten 62 Prozent (BTC), 59 Prozent (XRP), 100 Prozent (DOT), nur Diagnose. `sell_efficiency` mit Denominator-Regel 0.5 und Absorptionsbedingung nur bei Sell-z ≥ 1.

## 10. Look-ahead-Tests

Fünf Tests bestanden (`tests/test_mlib.py`): Merkmale von Hand (Volumen-z, Sell-z, Δ-Taker, Downside-Progress, Effizienz), Denominator- und Lückenregel, Join verwendet nur abgeschlossene 4h-Kerzen und ist invariant gegen Störung späterer 1h-Kerzen, AVWAP von Hand nachgerechnet und invariant gegen Störung späterer Kerzen, Anker innerhalb der Anker-4h-Kerze noch unbekannt, Episode-Reset nach sechs K1-falschen 4h-Kerzen, Kandidaten mit Einstieg vor T invariant gegen Störung ab T.

## 11. 4h→1h-Join-Tests

0 OHLC-Abweichungen bei 13903, 12364, 7367 vollständigen 4h-Kerzen, 36, 33, 14 unvollständige (Lücken) je Coin, deterministische Zuordnung «4h abgeschlossen vor 1h-Beginn».

## 12. Finale AVWAP-Anker- und Resetregel

Anker = erste 1h-Kerze der 4h-Kerze, an deren Schluss K1 (ATR-Form) von falsch auf wahr wechselt, bekannt am Schluss dieser 4h-Kerze, nie rückwirkend. Episode endet am Schluss der sechsten aufeinanderfolgenden 4h-Kerze mit K1 falsch. Nächster Wechsel falsch → wahr erzeugt neuen Anker. Typical Price, Spot-Basisvolumen, Lücken übersprungen, kein Tagesreset. Q1 am letzten abgeschlossenen 1h-Schluss vor dem Einstieg, fester Limit-Zielpreis. Alle Kandidaten lagen in einer laufenden Episode (`no_episode` 0).

## 13. Erwartete Fallzahl je Zelle (Development, eng, Ziel über Einstieg)

BTC: M1×Q0 84, M1×Q1 80, M2×Q0 3, M2×Q1 3, M3×Q0 0, M3×Q1 1. XRP: 64, 69, 4, 4, 2, 6. DOT: 37, 42, 3, 2, 4, 3. Nach Überlappungsausschluss (eine Position je Zelle) etwas weniger. Nur M1×Q0 und M1×Q1 erreichen die normale Auswertung (≥ 30) auf allen drei Coins, alle M2- und M3-Zellen bleiben deskriptiv (unter 20). Hochrechnung für ETH (rund 55700 1h-Kerzen) und SOL (rund 29700): M1-Zellen 60 bis 90 beziehungsweise 35 bis 45, M2 und M3 unter 10.

## 14. Trial-Accounting

Primär 6 je Coin (Holm), faktisch auswertbar 2 je Coin (M1×Q0, M1×Q1), die übrigen vier deskriptiv. Vorbelastung BTC rund 30, XRP rund 37, DOT rund 37, global rund 240 (Sensitivität). Festgelegt in `rebound_micro_trial_accounting_v0.1.md`.

## 15. Vorgeschlagene exakte Promotion-Regel

Wie `rebound_micro_promotion_rules_v0.1.md`: eine Zelle auf zwei von drei Coins mit avg_win/|avg_loss| ≥ 0.80, Median Stop ≤ 0.60 ATR14(4h), p_BE_emp ≤ 0.60, Mittel r_net K1 ≥ −0.05 R mit p_pos ≥ 0.40 und PF ≥ 0.90, mindestens 30 Trades und ≥ 30 erwartete auf ETH/SOL, Top-1 ≤ 40 Prozent, zwei Blöcke ≥ −0.05 R, gepaarte Differenz gegen 4h-Baseline Median > 0 mit ≥ 55 Prozent positiv. Angesichts der Kostenlage (Abschnitt 8) wird zusätzlich vorgeschlagen, K0 als Sensitivität zu berichten, ohne die K1-Regel zu ändern.

## 16. Offene Entscheidungen vor Freeze

1. Zellen M2 und M3 wie geplant mitführen (deskriptiv, unter 10 Fälle) oder auf M1×Q0 und M1×Q1 beschränken und Holm über zwei statt sechs. Beides ist vor Outcome zulässig, die Zahlen stehen oben.
2. Der nested Flow-Vergleich auf M1 ist mit 2 von 98 Fällen nicht testbar. Vorschlag: als `insufficient coverage` vorab festhalten und den Flow-Flag nur berichten.
3. Kostenlage: Die K1-Kosten von rund 0.9 R je Trade sind eine Eigenschaft der engen Stops, keine Eigenschaft des Signals. Vorschlag: Lauf wie geplant mit K1 als Massstab, K0 und K2 als Bericht, und die Frage «Maker-Ausführung als Execution-Hypothese» als spätere, getrennte Vorregistrierung vormerken. Keine Änderung der Promotion-Regel.
4. Baseline-Definition bestätigen: T0 auf der Kontextkerze (nicht auf der REBOUND-20-Musterkerze), damit Zelle und Baseline dasselbe Event teilen.
5. Zeitstopp 24 1h-Kerzen und Q0 als fixer Limit-Preis (statt dynamisch «Schluss über EMA20») bestätigen.

STOP. Kein P&L-Lauf. Warten auf Freigabe.
