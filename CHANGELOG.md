# Changelog (Repo-Struktur, nicht Forschung)

Forschungsentscheide stehen weiterhin ausschliesslich in `00_doku/ENTSCHEIDE.md`.

## 2026-10-01

- `original-2026-10-01` (Tag): verbatim Kopie von `/workspace/aurum2/projekt`, 455 Dateien, ohne `02_daten/raw` (412 MB) und `__pycache__`.
- Daten-Layout: `data/` gitignored, `02_daten/raw` als Symlink, `make data`, siehe `DATA.md`. DTB3 als Ersatz neu von FRED geladen.
- Gepinnte Umgebung: `requirements.txt`, `requirements.lock`, `.python-version` (3.13.5).
- Zentrales Kostenmodell `config/cost_model_v1.json` + `pylib/aurum_costs.py`. Werte 1:1 aus den eingefrorenen Dateien, per Test gebunden.
- Konfigurierbarer Root `AURUM_ROOT`: portable Versionen in `portable/` (mechanisch, `make portable-check`), Arbeitsbereich `build/root`. Siehe `REPRODUCIBILITY.md`.
- Lokale CI: `make test` (34 + Repo-Tests), `make repro` (4 Reproduktionen), `make verify-frozen`, `make ci`, `make ci-fast`, pre-commit-Hook (`make hooks`).
- `OFFENE_PUNKTE.md`: Gebührenwiderspruch und weitere Befunde, bewusst nicht aufgelöst.
- Schritt 2: Datensammler `collector/` (öffentliche Daten, täglich 06:15 Zürich via cron), siehe `collector/README.md`.
