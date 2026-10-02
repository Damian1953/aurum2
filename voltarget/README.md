# voltarget/ – Vol-Target-Overlay (ENTWURF v0.1, gesperrt)

Risiko-Overlay auf die unveränderten Paper-Sleeves W2, W6 und T55_20 (PAPER v1.0). Skaliert nur die Positionsgrösse,
erzeugt nie ein Signal. Vorregistrierung: `01_forschung/15_voltarget/VOLTARGET_PREREG_v0.1.md` (nicht eingefroren).

| Datei | Inhalt |
|---|---|
| `voltarget_engine.py` | Kern ohne Datenzugriff: σ_kurz (EWMA, Halbwertszeit 20), σ_lang (365 Tage), s = min(1, σ_lang/σ_kurz), Band 0.10, Simulation, Invarianten, Loader-Sperre Holdout/Validation |
| `base_adapter.py` | Basis-Exposure und Fill-Ereignisse aus `paper/paper_engine.py` (nur Import) |
| `run_voltarget.py` | Tageslauf; **verweigert ohne Freigabe (Exit 3)**, kein Dry-Run-Bypass; Parameter- und Freeze-Prüfung (Exit 4) |
| `voltarget_config.json` | `enabled: false`, `start_bar: null`, `freeze_list: null` |

Status: nicht eingefroren, nicht gestartet, **kein cron-/Scheduler-Eintrag**, kein Shell-Wrapper. Keine Keys, keine Orders,
keine Börsenverbindung. Tests: `tests/test_voltarget.py` (laufen in `make ci-fast`).
