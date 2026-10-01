# Delayed Trend (DT) – P&L-Lauf v1.0: Bericht

Stand 01.10.2026, 14:45 Zürich. Freigabe Damian 01.10.2026, 14:20. Einziger Lauf 14:35:14–14:35:17 Zürich.

- Spezifikation `01_forschung/11_delayed_trend/dt_pnl_spec_v1.0.md`, SHA 56a13bf7d434356539e956457e3616ea93a7ded4ea25f4247fd31380bf41d47a (steht im Log).
- Freeze-Commit 2a94bf9, Tag `dt-pnl-v1.0-freeze`; SHAs in `00_doku/dt_pnl_freeze_2026-10-01_expected_shas.txt`.
- Ausgaben in `run/`; SHAs in `00_doku/dt_pnl_run_2026-10-01_expected_shas.txt` (Eval e1216bb8…, Log 3c09fa7e…, Prüfung 27ef4e56…).
- Daten: nur Discovery-Spot 4h bis 2023-12-31 20:00 UTC. Kein Holdout geöffnet, auch das holdout_manifest nicht.

## Kurzfassung (4 Sätze)

Delayed Trend verliert in den drei vorab festgelegten Hauptzellen nach realistischen Kosten insgesamt 8.5 R über 102 Trades, das sind rund −0.08 R je Trade. Damit greift die vorab beschlossene Abbruchregel A7: Lane A (Bottom, Reversal, Rebound, DT) ist vollständig geschlossen, ohne weitere Varianten auf BTC, XRP oder DOT. Keine der sechs getesteten Zellen zeigt ein statistisch belastbares Signal gegenüber der Kontrollgruppe (bester Holm-p-Wert 0.345). Die wenigen positiven Zellen hängen an ein bis drei Ausreissertrades, und bei DT2 liess sich der Kontrollvergleich praktisch nicht durchführen.

## Ergebnisse je Zelle (Kosten K1 Spot, Holm über 6 Zellen)

| Zelle | Rolle | Trades (in Position übersprungen) | Paare | ΔR Mittel / Median / Anteil > 0 | Netto-K1 R je Trade | p | Holm-p | Status |
|---|---|---|---|---|---|---|---|---|
| BTC S2×DT1 | primär | 30 (5) | 26 | +0.663 / +0.014 / 65 % | +0.148 | 0.115 | 0.345 | kein Signal; status_v2 roh «formal_supported», nach §9/A8 nicht wertbar |
| XRP S2×DT1 | primär | 35 (8) | 26 | −0.501 / −0.002 / 46 % | −1.023 | 0.835 | 0.835 | no evidence / inconclusive |
| XRP S2×DT2 | primär | 37 (9) | 1 | – | +0.619 | – | – | inconclusive (insufficient sample, < 2 Paare) |
| BTC S2×DT2 | sekundär | 40 (9) | 0 | – | +0.409 | – | – | inconclusive (insufficient sample) |
| DOT S2×DT1 | sekundär | 23 (8) | 17 | +0.265 / −0.002 / 47 % | −0.147 | 0.199 | 0.398 | no evidence / inconclusive (low-frequency 20–29) |
| DOT S2×DT2 | sekundär | 33 (7) | 1 | – | −0.173 | – | – | inconclusive (insufficient sample) |

A6 (Fortführung nur bei Netto-K1 ≥ 0) wäre für BTC S2×DT1, XRP S2×DT2 und BTC S2×DT2 erfüllt. Wegen A7 ist das gegenstandslos.

Bootstrap-Intervall des ΔR-Mittels (5–95 %):
- BTC S2×DT1: −0.21 bis +1.80;
- XRP S2×DT1: −1.41 bis +0.23;
- DOT S2×DT1: −0.23 bis +0.80.

### Kostenszenarien (R je Trade)

| Zelle | K0 | K1 | K2 | Kraken maker_plan | Kraken taker_K2 | Kraken maker_entry_taker_stop (Entwurf) |
|---|---|---|---|---|---|---|
| BTC S2×DT1 | +0.330 | +0.148 | −0.156 | +0.148 | −0.156 | +0.038 |
| XRP S2×DT1 | −0.811 | −1.023 | −1.368 | −1.023 | −1.368 | −1.154 |
| XRP S2×DT2 | +0.938 | +0.619 | +0.099 | +0.619 | +0.099 | +0.463 |
| BTC S2×DT2 | +0.655 | +0.409 | +0.005 | +0.409 | +0.005 | +0.261 |
| DOT S2×DT1 | +0.028 | −0.147 | −0.438 | −0.147 | −0.438 | −0.248 |
| DOT S2×DT2 | +0.073 | −0.173 | −0.578 | −0.173 | −0.578 | −0.318 |

Die Kraken-Szenarien werden nur berichtet und entscheiden nichts.

### Konzentration und Exits

- BTC S2×DT1: Gewinnquote 20 %, Profit-Faktor 1.15. Die Top-3-Trades liefern 73 % des Bruttogewinns. Ohne den besten Trade (+12.2 R) wäre die Summe −7.8 R.
- XRP S2×DT2: die Top-3 liefern 97 %. Ohne den besten Trade (+37.4 R) wäre die Summe −14.5 R.
- XRP S2×DT1: Profit-Faktor 0.14.
- Exits überwiegend durch den Stop: BTC DT1 23 von 30, XRP DT1 30 von 35, XRP DT2 26 von 37. Der Chandelier greift 3- bis 8-mal je Zelle, der Zeitstopp t+360 nur zweimal insgesamt.

### Deskriptiv (S1, A2, kein Test)

| Zelle | Trades | Netto-K1 R/Trade |
|---|---|---|
| BTC S1×DT1 | 13 | −0.737 |
| BTC S1×DT2 | 6 | −1.293 |
| XRP S1×DT1 | 15 | +0.351 |
| XRP S1×DT2 | 8 | +0.742 |
| DOT S1×DT1 | 10 | −0.750 |
| DOT S1×DT2 | 8 | −1.112 |

## A7 – kombiniertes primäres Netto-K1

- Summe r_net K1 über alle 102 Trades der drei Primärzellen: **−8.47 R**. Je Trade −0.083 R; das ungewichtete Mittel der drei Zellenmittel beträgt −0.085.
- Anteile: BTC S2×DT1 +4.45, XRP S2×DT1 −35.81, XRP S2×DT2 +22.89.
- **Die Summe ist < 0. A7 greift mechanisch: Lane A vollständig geschlossen** (Eintrag in ENTSCHEIDE vom 01.10.2026, 14:40).
- Nur berichtet, ändert nichts am Ausgang: Die Summe hängt an den Kosten. K0 ergäbe +16.2 R, K2 −48.9 R, Kraken maker_entry_taker_stop −22.1 R. Bindend ist nach C1/C2 und Spezifikation allein K1.

## Kontrollabdeckung (Befund)

- DT1-Zellen: 50 bis 52 gehandelte Kontrollen bei BTC und XRP, 32 bei DOT. Paare: 26 / 26 / 17.
- DT2-Zellen: Von 81 bis 93 gematchten Kontrollen je Zelle kamen höchstens eine zum Einstieg. Grund fast immer `retest_failed` (BTC 82, XRP 72, DOT 66), Rest `no_retest_hold`.
- Das Ersatzniveau P = max(H, c−18..c) wird in Kontrollkontexten fast nie im Retest gehalten. Deshalb ist ΔR für DT2 nicht messbar, und XRP S2×DT2 erhält keinen Test.
- Die Ursache ist eine Eigenschaft des eingefrorenen Kontrolldesigns (Vorbericht §7.5) und kein Fehler des Laufs. Für A7 spielt es keine Rolle, weil A7 nur Netto-K1 verwendet.

## Prüfungen

Im Lauf (bestanden):
- SHAs aller Eingaben und der Spezifikation im Log.
- Neuberechnung der Einstiege gleich der eingefrorenen Messung.
- Letzte Kerze ≤ 2023-12-31 20:00 UTC; keine Validation-Datei.

Unabhängig mit `tools/dt/check_dt_pnl_v1.py` (eigene Implementierung), Ergebnis `gesamt_ok = true`:
- Spec-SHA im Log.
- Einstiege gleich der Messung; alle Entscheidungskerzen vor dem Einstieg (kein Look-ahead, nur abgeschlossene Kerzen); Eine-Position-Regel eingehalten.
- Exit-Kerze und Exit-Grund identisch. r_net in allen 6 Kostenszenarien neu gerechnet, maximale Abweichung ≤ 4e-15.
- Kontrollen: 0 Verletzungen beim Matching und bei den Ersatzniveaus; Kontroll-r_net und Paar-ΔR identisch.
- Holm und A7-Summe neu berechnet und gleich.
- Störungstest ab 2022-07-01: 0 von 190 Trades verändert.

## Abweichungen und Festlegungen

- **Abweichungen von der Spezifikation:** keine. Ein Lauf, kein Neustart, kein Bug.
- **Festlegungen vor dem Freeze** (in ENTSCHEIDE, 14:35):
  - (1) A4-Chandelier vom höchsten **Schluss** seit Einstieg (Forschungsplan §5), ohne Strukturbruch-Regel aus rlib E-D.
  - (2) A7 ist operationalisiert als Summe r_net K1 über alle Trades der drei Primärzellen.
- **Statusbezeichnung:** Für BTC S2×DT1 meldet die wörtlich übernommene Funktion `status_v2` «formal_supported» (v1-Kriterien a–e erfüllt). Nach Spezifikation §9 gilt aber nur Holm-p < 0.05 als «Signal vorhanden»; A8 begrenzt zudem auf höchstens «mechanistically promising» (Development). Holm-p beträgt 0.345, also kein Signal.

## Evidenzvermerk (A8, wörtlich)

«DT ist outcome-informed (Ebene C), laeuft auf denselben Discovery-Daten wie alle gescheiterten Vorgaenger, und die globale Trial-Zahl liegt bei rund 240. Ein positives Ergebnis gilt deshalb hoechstens als «mechanistically promising» in der Klasse Development. Ein Holdout-Lauf ist nur nach dem Economic Validation Gate zulaessig (Governance v1.1 §7), und dieser Vermerk wird im DT-Freeze woertlich uebernommen.»

Trial-Accounting: +6 getestete Zellen, dazu 6 deskriptive.
