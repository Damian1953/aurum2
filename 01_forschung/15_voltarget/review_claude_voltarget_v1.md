# Review Claude zu VOLTARGET_PREREG v0.2, Zusammenfassung v1

**Stand:** 2026-10-02 (Zürich, UTC+2). Zusammenfassung durch Aurum II Bot im Auftrag der Projektleitung, Grundlage: Review Claude zu `VOLTARGET_PREREG_v0.2.md`.
**Status:** Umsetzung als `VOLTARGET_PREREG_v1.0.md` (**Kandidat, nicht eingefroren**). Kein Freeze, kein Start, kein cron. v0.2 bleibt unverändert liegen. `00_doku/ENTSCHEIDE.md` wird hier nicht verändert.

## 1. Pflichtänderungen

| Nr. | Stelle | Punkt | Umsetzung |
|---|---|---|---|
| M1 | §1 | Erwartung offen aussprechen: Das Overlay wird selten aktiv sein, «nicht prüfbar» ist wahrscheinlich, und es überschneidet sich mit dem ATR-Stopp bzw. dem 20-Tage-Ausstieg der Basis. | v1.0 §1 «Erwartung» |
| M2 | §7.1 | Zusammenspiel G1 und G3 erklären: Ist c < 0.90, ist G3 die strengere Schranke; G1 greift, wenn c nahe bei 1 liegt. | v1.0 §7.1 «Zusammenspiel G1 und G3» |
| M3 | §8.2 | Am ersten Review greift KR3 nur, wenn zusätzlich die nicht annualisierten Kosten der Vol-Anpassungen über 0.33 % liegen. In `gates.py` umsetzen, mit Tests. | `gates.KR3_FIRST_REVIEW_MIN = 0.0033`, `kr3_cost_kill(..., first_review=True)`; Konfiguration `gates.kr3_first_review_min`; Test `test_m3_kr3_first_review_needs_non_annualised_above_033pct` |
| M4 | §3.7, §6 | Symmetrische Sync-Buchung am Startbar für B (mit E) und C (mit E·c), mit denselben Kosten. Sync-Kosten von VT getrennt ausweisen. Synthetischer Test: Mit s ≡ 1 sind VT, B und C identisch, inklusive Sync. | `voltarget_engine.run_compare`, `sync_costs`, `costs_by_reason`; Runner-Spalte `eq_base_sync`, Sync-Kosten im Zustand; Tests `test_m4_symmetric_sync_for_b_and_c`, `test_m4_identity_vt_b_c_with_s_equal_one_including_sync` |

## 2. Bestätigt (bleibt)
- G2-Toleranz 0.05 (Sharpe_VT ≥ Sharpe_Basis − 0.05).
- Cash-Konvention VOLTARGET 0 % und Sharpe ohne Zinsabzug (wie PAPER F3).

## 3. Bericht
- Verteilung von s je Coin ausweisen (Coin-Tage mit s < 1). Umsetzung: `voltarget_engine.scale_distribution`, Zustand `s_verteilung` und `summary`.

## 4. Gemeinsamer Wochenbericht und Heartbeat (Startvoraussetzung)
- Der gemeinsame einseitige Wochenbericht aus dem Sleeves-Auftrag (M3) muss auch VOLTARGET abdecken.
- Gemeinsamer Heartbeat über alle Forward-Linien: eine Statuszeile je Runner und Alarm, wenn ein Lauf fehlt.
- Beides ist Voraussetzung für den Start. Umsetzung auf Branch `sleeves-v1` (`forward/heartbeat.py`, `forward/voltarget_bericht.py`, `paper/wochenbericht.py`), ohne cron. VOLTARGET liefert nur seine Zustandsdatei nach der dort dokumentierten Schnittstelle; die beiden Branches berühren keine gemeinsame Datei.

## 5. Präzisierung vor dem Freeze (Entscheid Projektleitung 2026-10-02)
- Kursdrift löst keine Vol-Anpassung aus: Ziel ohne Basis-Ereignis = w_B(t) · s (driftendes Gewicht der Basis B mal s), Band vergleicht mit w_B(t) · s; mit s ≡ 1 ist VT exakt B (Tests W2, W6 mit E = 0.5/0.75, T55_20). Keine inhaltliche Änderung gegenüber dem Review (VT als skalierte Version von B auf denselben Positionen). C bleibt «E · c bei Basis-Ereignissen, danach Drift ohne Umschichtung»; mit c = 1 exakt B.
- M4 von der Projektleitung bestätigt.
