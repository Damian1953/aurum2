# DELAYED-TREND — P&L-Spezifikation, Version 1.0

**Project Aurum II, `01_forschung/11_delayed_trend/dt_pnl_spec_v1.0.md`. 01.10.2026. Status: EINGEFROREN am 01.10.2026, Freigabe Damian 14:20 Zürich, vor jedem Outcome. Setzt die Entscheide A1 bis A8 vom 01.10.2026 (`00_doku/ENTSCHEIDE.md`) um, auf Grundlage von Forschungsplan v0.1 (0241c247…), Messregeln v1.0 (ec7ed621…) und Vorbericht mit Geometry Gate v1 (0e3085a4…). Bis zum Freeze wurde kein DT-Exit, kein r_net, keine MFE/MAE und keine Kursentwicklung nach einem DT-Einstieg berechnet oder angesehen. Development-Daten BTC, XRP, DOT bis 2023-12-31, nur die Discovery-Dateien. Keine ETH/SOL-Daten, kein Holdout, kein Lesen des Holdout-Manifests.**

## 1. Evidenzvermerk (A8, wörtlich)

«DT ist outcome-informed (Ebene C), laeuft auf denselben Discovery-Daten wie alle gescheiterten Vorgaenger, und die globale Trial-Zahl liegt bei rund 240. Ein positives Ergebnis gilt deshalb hoechstens als «mechanistically promising» in der Klasse Development. Ein Holdout-Lauf ist nur nach dem Economic Validation Gate zulaessig (Governance v1.1 §7), und dieser Vermerk wird im DT-Freeze woertlich uebernommen.»

Evidenzklasse: Development (alle drei Coins, weil die DT-Hypothese aus den eingefrorenen Läufen auf BTC, XRP und DOT abgeleitet ist). Trial-Accounting: dieser Lauf zählt 6 getestete Zellen (A1), dazu 6 deskriptive S1-Zellen ohne Test.

## 2. Abbruchregel für Lane A (A7, wörtlich)

«Vor dem DT-P&L-Lauf festgeschrieben: Ist Netto-K1 in den drei Primaerzellen zusammen kleiner als null, wird Lane A (Bottom, Reversal, Rebound, DT) vollstaendig geschlossen. Es folgt keine weitere Variante, keine Umformulierung und kein neuer Timeframe auf BTC, XRP oder DOT. Eine Wiederaufnahme waere nur mit neuen Daten (Forward-Fenster) und einer neuen Vorregistrierung zulaessig, die diesen Entscheid ausdruecklich zitiert.»

Operationalisierung (vor dem Lauf festgelegt, bindend): «Netto-K1 der drei Primärzellen zusammen» ist die **Summe von r_net unter K1 (in R) über alle Trades der drei Primärzellen** BTC S2×DT1, XRP S2×DT1 und XRP S2×DT2. Das Vorzeichen ist identisch mit dem der gepoolten Erwartung je Trade. Ist die Summe kleiner als null, wird mechanisch ein Eintrag in ENTSCHEIDE angehängt, der Lane A schliesst. Zusätzlich berichtet, nicht bindend: das ungewichtete Mittel der drei Zellenerwartungen.

## 3. Zellen (A1, A2, A3)

| Rolle | Zellen | Test |
|---|---|---|
| primär | BTC S2×DT1, XRP S2×DT1, XRP S2×DT2 | Holm über alle 6 |
| sekundär | BTC S2×DT2, DOT S2×DT1, DOT S2×DT2 | Holm über alle 6, keine nachträgliche Aufwertung |
| deskriptiv (A2) | S1×DT1 und S1×DT2 auf BTC, XRP, DOT | kein Test, kein Status |
| abgeschlossen (A3) | DT3 auf allen Zellen | «Spezifikation abgeschlossen, keine Fortführung», wird nicht gerechnet |

Kein Pooling über Coins für Status oder Holm (A7 ist eine eigene Regel über die drei Primärzellen).

## 4. Daten und Eingaben

- 4h-Spot-Discovery-Dateien `holdout/discovery/{BTC,XRP,DOT}USDT_spot4h_discovery.csv`, letzte Kerze 2023-12-31 20:00 UTC. SHA-Prüfung gegen die eingefrorenen count-JSON (wie Messung). `AURUM_VALIDATION` darf nicht gesetzt sein, `ylib.load` sperrt Validation-Dateien.
- Kandidatentabellen der eingefrorenen Zählungen (BTC `count_BTC_B`, XRP `count_XRP`, DOT `count_DOT`), SHA gegen die count-JSON.
- Einstiege: die eingefrorenen Messausgaben `out/{COIN}_entries.csv` (SHAs aus `dt_expected_shas.txt`). Der Lauf berechnet sie mit `dtlib` v1.0 (f2d6c390…) neu und bricht ab, wenn Einstiegskerze, Stop oder Status abweichen.
- Libraries unverändert: `rlib` v1.0 (f1ffdbb8…), `dtlib` v1.0, `ylib` portabel (Kosten aus `config/cost_model_v1.json`, Abschnitt `spot_r`).
- Modus: BTC `cfg_btc_stufeA`, XRP und DOT `cfg_alt`. Blöcke `rlib.BLOCKS` (BTC/XRP P1, P2; DOT P2a, P2b, P1 2020 nicht gewertet).

## 5. Einstiege und Positionen

Einstiegskerze e, Einstiegspreis O_e und Initialstop exakt nach Messregeln v1.0 §4: DT1 Stop = L_s − 0.5·ATR14_{s+3}, Einstieg s+4; DT2 Stop = min(L_b, L_{b+1}) − 0.5·ATR14_{b+1}, Einstieg b+2. Nur Einstiege mit Status `entry`.

**Eine Position je Zelle** (Forschungsplan §3, «eine Position je Familie und Coin»): Die Einstiege einer Zelle werden nach e geordnet. Ein Einstieg wird übersprungen (`in_position`), wenn e ≤ x des zuletzt eröffneten Trades derselben Zelle (x = Ausstiegskerze). Die Zellen sind getrennte Sleeves, DT1 und DT2 desselben Coins schliessen sich nicht aus.

## 6. Exit (A4)

Ein einziger Exit für alle Zellen, keine Alternative: Chandelier 3 × Tages-ATR14 vom **höchsten Schluss seit Einstieg** (Forschungsplan §5, wörtlich), nur steigend, plus initialer Stop, plus Zeitstopp t+360 (t = Kontextkerze). Kein Strukturbruch, kein Ziel, kein Scale-out.

- Tages-ATR14 wie `rlib.features`: Wilder-ATR(14) über UTC-Tageskerzen aus den 4h-Kerzen, für alle 4h-Kerzen eines Tages gilt der Wert des Vortages (nur abgeschlossene Tage).
- Floor: an der Einstiegskerze HC = C_e, Floor = HC − 3·ATRd_e. Nach jeder nicht ausgestoppten Kerze b: HC = max(HC, C_b), Floor = max(Floor, HC − 3·ATRd_b). Wirksamer Stop für Kerze b = max(Initialstop, Floor aus Kerzen ≤ b−1). Nur abgeschlossene Kerzen gehen in den Floor ein.
- Fill- und Intrabar-Regeln wie `rlib.simulate_trade` (E-D-Pfad): Einstieg O_e·(1+slip_in). Stop an der Einstiegskerze, wenn L_e ≤ Initialstop (Fill zum Stop, bei Eröffnung darunter zur Eröffnung). Danach: O_b ≤ Stop → Ausstieg O_b·(1−slip_sl) (`stop_gap`); L_b ≤ Stop → Ausstieg Stop·(1−slip_sl) (`stop` bzw. `chandelier_d`).
- Zeitstopp: Ist die Position nach dem Schluss der Kerze b ≥ t+360 noch offen, Ausstieg zur Eröffnung b+1 mit O·(1−slip_in) (`time360`). Datenende: Ausstieg zum letzten Schluss C_{n−1}·(1−slip_in) (`cut`), der Trade zählt.
- r_net = (Exit − Entry − (Entry + Exit)·(fee + fric)) / R mit R = Entry − Initialstop (Entry inklusive Slippage), wie `rlib`.

## 7. Kosten (C1, C2)

Spot-Long (C1). Primär K1 aus `spot_r` (eingefroren: fee 0.40 %, fric 0.02 % je Seite, slip_in 0.05 %, slip_sl 0.10 %), K0 und K2 als Bericht. Kraken-Venue-Modell (`venue_kraken`, Bericht): `maker_plan` (= spot_r K1), Pflicht-Sensitivität `taker_K2` (= spot_r K2) und der Entwurf `maker_entry_taker_stop` (Einstieg Maker 0.40 %, jeder Ausstieg ausser `cut` als Market-Order Taker 0.80 %, Reibung und Slippage wie K1). Das Venue-Modell entscheidet nichts.

## 8. Kontrollgruppe (A5)

- Pool: Kontextkerzen ohne Bottom-Struktur, `ylib.control_pool` wie XRP/DOT v1.0 und BTC Stufe B (K1 bis K3 erfüllt, kein Failed Breakdown, kein Y3, nicht im Boden eines gültigen Double Bottoms).
- Matching je gehandeltem Signal auf seiner Kontextkerze t mit `rlib.match_controls` (±540 Kerzen, Abstand > 12, |Δdd120| ≤ 0.03 bzw. |Δdd120_atr| ≤ 1.5, |Δext| ≤ 0.5, bis zu 3 Kontrollen, nicht innerhalb einer offenen Signalposition derselben Zelle).
- Ersatzniveaus je Kontrollkerze c (Forschungsplan §8, Vorbericht §7.5): Ersatz-L_ref = min(L, c−120..c), Ersatz-P = max(H, c−18..c), ATR14_t = ATR14_c. Invalidierung, Fenster (c+1 bis c+180) und Einstiegsregel derselben Familie (DT1 bzw. DT2) exakt mit den `dtlib`-Funktionen. Exit wie §6 mit Zeitstopp c+360, Kosten wie das Signal. Kontrollen ohne Einstieg zählen als «kein Einstieg» und gehen nicht in Paare ein.
- Paar: ΔR = r_net(Signal) − Mittel r_net(gehandelte Kontrollen des Signals), K1. Signale ohne gehandelte Kontrolle bilden kein Paar.

## 9. Metriken, Test und Status (A6)

- Primärmetrik: gepaartes ΔR (Status nach Regel v2) und Netto-K1 (Erwartung r_net je Trade). **Fortführung einer Zelle nur bei Netto-K1 ≥ 0** (A6), zusätzlich gilt §2.
- p-Wert je Zelle: Bootstrap des Mittels ΔR (2000 Wiederholungen, Seed 20260918, ein Generator in fester Reihenfolge: primäre Zellen, sekundäre Zellen, deskriptive Zellen), p = Anteil Bootstrap-Mittel ≤ 0. Holm über die 6 Zellen aus §3. «Signal vorhanden» = Holm-p < 0.05, Mittel ΔR > 0 und Netto-K1 > 0 (wie XRP/DOT v1.0).
- Status: Funktion `status_v2` aus `eval_cross.py` wörtlich (formal supported nach v1, sonst mechanistically promising bei ≥ 3 von 4 Kriterien v2 und Median ΔR > 0, Fast Fail, sonst inconclusive; mindestens 5 Paare). Diagnosen (Capture, Outcome-Klassen trend/delayed_trend/rebound/fail, Konzentration) wie `diag` in `eval_cross.py`, ohne Follow-through-Felder. Block eines Trades = Block der Kontextkerze t.
- Low-Frequency-Stufung (Governance v1.1 §8) nach Anzahl Trades der Zelle: unter 20 nur deskriptiv (Status höchstens inconclusive), 20 bis 29 höchstens «mechanistically promising (low-frequency)», nie formal supported, ab 30 normal.
- Bericht je Zelle: Trades, Einträge `in_position`, Exit-Gründe, r_net K0/K1/K2 und Venue-Szenarien, ΔR (Mittel, Median, Anteil positiv, Bootstrap-Intervall), p, Holm-p, Status, Blöcke, Jahre, Haltedauer, MFE, Capture, Kontrollen (gematcht, mit Einstieg, r_net).

## 10. Prüfungen

Im Lauf (Abbruch bei Verletzung): SHAs aller Eingaben und der Spezifikation im Log; Neuberechnung der Einstiege gleich der eingefrorenen Messung; letzte Kerze jeder Datei ≤ 2023-12-31 20:00 UTC; keine Datei mit «validation» im Namen.
Nach dem Lauf, unabhängig (`tools/dt/check_dt_pnl_v1.py`, eigene Implementierung ohne `rlib`/`dtlib`-Simulation): Tages-ATR und Exits aus den Rohkerzen neu simuliert, Kosten neu berechnet, Einstieg nach allen Entscheidungskerzen (kein Look-ahead, nur abgeschlossene Kerzen), Eine-Position-Regel, Kontrollen im Pool und innerhalb der Matching-Toleranzen, Ersatzniveaus neu berechnet; Störungstest: Trades mit Ausstieg vor T bleiben gleich, wenn alle Kerzen ab T gestört werden.

## 11. Was nicht erlaubt ist

Kein zweiter Lauf, keine Exit-, Stop- oder Zielvariante, keine Änderung der Zellen nach Sicht, keine Aufwertung sekundärer Zellen, kein Pooling über Coins für Status, keine ETH/SOL-Daten, kein Holdout. Ein Bug nach dem Freeze wird als datierte Abweichung in ENTSCHEIDE dokumentiert.
