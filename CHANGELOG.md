# Changelog (Repo-Struktur, nicht Forschung)

Forschungsentscheide stehen weiterhin ausschliesslich in `00_doku/ENTSCHEIDE.md`.

## 2026-10-01

- CARRY_PREREG v0.9 `01_forschung/13_carry/carry_prereg_v0.9.md`: VERWORFEN (Damian 22:16), nicht eingefroren, nicht gelaufen; ENTSCHEIDE 22:16 mit Deklaration der Vorbelastung; OP-11.
- Paper-Runner v1.0 (`paper/`), PAPER_PREREG_v1.0 eingefroren (Tag `paper-v1.0-freeze`), cron via `collector/ensure_scheduler.sh`, Wochenbericht; D1 entschieden.
- Ideen-Scan v1 (`01_forschung/12_ideen_scan/`, explorativ, nicht vorregistriert) und Carry-Vorregistrierungs-Entwurf v0.1; D3 entschieden; XS21-Vermerke zur Nachpruefung (ENTSCHEIDE 15:45).
- DT P&L v1.0: einziger Lauf, Pruefung, Bericht, A7-Eintrag (Lane A geschlossen); `00_doku/dt_pnl_run_2026-10-01_expected_shas.txt`, Tag `dt-pnl-v1.0-run`.
- DT P&L v1.0: Spezifikation, Lauf-Code, Pruefskript, Tests eingefroren (`00_doku/dt_pnl_freeze_2026-10-01_expected_shas.txt`, Tag `dt-pnl-v1.0-freeze`).
- `original-2026-10-01` (Tag): verbatim Kopie von `/workspace/aurum2/projekt`, 455 Dateien, ohne `02_daten/raw` (412 MB) und `__pycache__`.
- Daten-Layout: `data/` gitignored, `02_daten/raw` als Symlink, `make data`, siehe `DATA.md`. DTB3 als Ersatz neu von FRED geladen.
- Gepinnte Umgebung: `requirements.txt`, `requirements.lock`, `.python-version` (3.13.5).
- Zentrales Kostenmodell `config/cost_model_v1.json` + `pylib/aurum_costs.py`. Werte 1:1 aus den eingefrorenen Dateien, per Test gebunden.
- Konfigurierbarer Root `AURUM_ROOT`: portable Versionen in `portable/` (mechanisch, `make portable-check`), Arbeitsbereich `build/root`. Siehe `REPRODUCIBILITY.md`.
- Lokale CI: `make test` (34 + Repo-Tests), `make repro` (4 Reproduktionen), `make verify-frozen`, `make ci`, `make ci-fast`, pre-commit-Hook (`make hooks`).
- `OFFENE_PUNKTE.md`: Gebührenwiderspruch und weitere Befunde, bewusst nicht aufgelöst.
- Schritt 2: Datensammler `collector/` (öffentliche Daten, täglich 06:15 Zürich via cron), siehe `collector/README.md`.

## 2026-10-01 (Nachmittag): Schritt 0 umgesetzt

- ENTSCHEIDE.md: je ein datierter Eintrag zu A1–A8, B1–B8, C1–C3, D1, D4, D5, E1–E4 und F1 (Empfehlung übernommen). D2 und D3 als offen vermerkt, dazu der E3-Korrekturvermerk. Es wird nur angehängt, `make verify-frozen` prüft, dass der Stand im Tag ein Byte-Präfix bleibt. Die neue SHA steht in `00_doku/schritt0_2026-10-01_expected_shas.txt`.
- Entwürfe `00_doku/entwuerfe/ENTSCHEIDE_Entwurf_Schritt0_v0.{1,2}.docx` plus Textauszug.
- E3: `00_doku/rm_2026-09-18_expected_shas.addendum_2026-10-01.txt`. verify-frozen wendet `*.addendum_*.txt` an.
- C2: `config/cost_model_v1.json` v1.1 mit `venue_kraken`. Die eingefrorenen Abschnitte sind unverändert, dazu ein Test. `05_evidenz/README_v1.1_gebuehren.md` korrigiert die Gebührensätze.
- B1–B8: `01_forschung/09_lane_c/xs21_point_in_time_prereg_v0.2.md` (ENTWURF) und B7-Ausschlussliste `xs21_pit_v0.2/` (ENTWURF v0.1, Prüfsummen, `tools/xs21/`). Kein Lauf.

## 2026-10-01 (spaeter Nachmittag): Review XS21 v0.2 eingearbeitet

- Review Claude: `01_forschung/09_lane_c/xs21_point_in_time_v0.2_review_claude_v1.md` (verbatim).
- `xs21_point_in_time_prereg_v1.0.md` (FREEZE-KANDIDAT, nicht eingefroren) mit M1–M7. B7 v1.0: `tools/xs21/exclusion_map_v1.0.py`, `tools/xs21/build_exclusions_v1.py`, Ausgabe `xs21_pit_v1.0/` mit Pruefsummen. v0.1/v0.2 unveraendert.
- ENTSCHEIDE: E3-Korrekturvermerk (SHA-Uebereinstimmung statt Zeitstempel-Reihenfolge) und Eintrag Freeze-Kandidat angehaengt, SHA in `00_doku/xs21v1_2026-10-01_expected_shas.txt`.
- DTB3 bis 2026-09-14 (`data/supplement/DTB3_3m_tbill_to_2026-09-14.csv`, `make data`).

## 2026-10-01 (Abend): Collector v1.1

- Neue Quellen `kraken_futures_tickers` (Instrumente + Ticker je Perpetual, fuer XS21-Gate M3) und `kraken_spot_tickers` (24h-Volumen der 10 Projekt-Coins). Gleicher Schreibpfad (Validierung, Quarantaene, append-only, Dedup, Provenance, Status). 4 neue Offline-Tests. Erste Erfassung 01.10.2026.

## 2026-10-01 (Abend): XS21 PiT v1.0 Freeze, Daten, Lauf

- Freeze v1.0 (Tag `xs21-pit-v1.0-freeze`), Datenbeschaffung `tools/xs21/fetch_data_v1.py` (data.binance.vision, Provenienz und Prüfsummen in `xs21_pit_v1.0/daten/`), Lauf-Code `xs21_pit_v1.0/xs21_pit.py`, `xs21_pit_run.py`, Tests `tests/test_xs21_pit.py` (Tag `xs21-pit-v1.0-runcode`).
- Einziger Lauf: Ausgaben in `xs21_pit_v1.0/run/`, SHAs in `00_doku/xs21_run_2026-10-01_expected_shas.txt`. Nachprüfung und Nachträge: `tools/xs21/check_run_v1.py`, `check_run_v1_erklaerung.py`, `nachtrag_survivorship_bloecke_v1.py`. Bericht `xs21_pit_v1.0/xs21_pit_v1.0_bericht.md`.

## 2026-10-01 (Nacht): Carry verworfen, Ideen-Scan v2

- Carry: `01_forschung/13_carry/carry_prereg_v0.9.md` VERWORFEN (Damian 22:16), nicht eingefroren, nicht gelaufen; ENTSCHEIDE 22:16.
- Ideen-Scan v2: `01_forschung/14_ideen_scan_v2/` (Bericht, explorative Resultate < 2024, Rohdaten-Pruefsummen, Entwuerfe MAKRO_LIQ v0.1 und MVRV v0.1, nicht eingefroren); Skript `tools/ideen/explorativ_scan_v2.py`; ENTSCHEIDE 22:35 (10 informelle Trials, global ca. 270).
- Entscheid 22:40: MAKRO_LIQ und MVRV nur Forward-Paper; Entwuerfe v0.2 (nicht eingefroren), Review-Auftrag `fuer_claude/an_claude_scan_v2.md`; OP-12 entschieden.
