# Paper-Runner (PAPER_PREREG_v1.0)

Täglicher Paper-Betrieb W2, W6, Turtle 55/20 auf öffentlichen Kraken-Tageskerzen (Collector). Keine Keys, keine Orders.

- `paper_engine.py` Regeln und Buchhaltung (eingefroren), `run_paper.py` Tageslauf (eingefroren), `run_paper.sh` cron-Wrapper.
- `wochenbericht.py` / `run_wochenbericht.sh` Wochenbericht (montags 07:10) nach `/workspace/aurum2/paper/berichte/`.
- Ausgaben unter `/workspace/aurum2/paper/` (`state/`, `ledger/`, `logs/`).
- Planung: `collector/ensure_scheduler.sh` setzt die cron-Einträge `aurum2-paper` (06:50) und `aurum2-paper-bericht` und holt verpasste Läufe nach.
- Freeze: `00_doku/paper_freeze_2026-10-01_expected_shas.txt`. Der Runner läuft nicht, wenn eine eingefrorene Datei abweicht.
- Manuell: `paper/run_paper.sh` (Lauf), `AURUM_PAPER_OUT=... .venv/bin/python paper/wochenbericht.py --datum JJJJ-MM-TT`.
