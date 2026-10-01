# Daten-Layout

Rohdaten sind **nicht** im Git (412 MB). Versioniert sind alle eingefrorenen Forschungsartefakte inkl. `02_daten/holdout/` (43 MB, Discovery und Validation mit Manifest-Prüfsummen).

| Pfad | Inhalt | versioniert |
|---|---|---|
| `data/raw/` | Kopie von `02_daten/raw` des Originalprojekts (ohne `kraken_archiv/_download`, 17 GB) | nein (`.gitignore`) |
| `02_daten/raw` | Symlink auf `../data/raw`, damit die eingefrorenen Loader- und Forschungsskripte ihre relativen Pfade finden | nein (Symlink, gitignored) |
| `data/supplement/DTB3_3m_tbill.csv` | FRED DTB3 3M T-Bill, neu geladen am 01.10.2026 und bei 2026-07-15 abgeschnitten. **Fehlte in der Kopie**, wird von `s2lib.load_tbill()` gebraucht. SHA-256 `085e8e3853e995329ef194787c038f2e778ca887e17678ea26b81eb7b2c4dffd` (weicht vom Original `26129de6…` ab, vermutlich Formatierung). Die Stufe-2-Ergebnisse sind damit trotzdem bitgleich. | nein |
| `data/supplement/DTB3_3m_tbill_to_2026-09-14.csv` | FRED DTB3, geladen am 01.10.2026, ohne Leerwerte, bei 2026-09-14 abgeschnitten, fuer XS21 PiT v1.0 (Cash-Ertrag). SHA-256 `8b287e3cc711b4c7d5629caed6f531c7564d4d7e8dbcf8f6bc49b069b7ca9d59`. Bis 2026-07-15 bytegleich mit `DTB3_3m_tbill.csv`. FRED revidiert gelegentlich, massgeblich ist die SHA | nein |
| `build/root/` | generierter Arbeitsbereich im Layout der Claude-Sandbox (`rtc/`, `yamato/`, `holdout/`, `dt/`, `micro/`, `s2/`, …), siehe `REPRODUCIBILITY.md` | nein |
| `/workspace/aurum2/data_live/` | laufende Datensammlung (Collector), ausserhalb des Repos | nein |

Einrichten: `make data` (= `tools/link_data.sh`). Die Quelle lässt sich mit `AURUM_DATA_SRC=/pfad/zu/02_daten/raw` überschreiben. Die Daten werden **kopiert**, nicht verlinkt, damit kein Skript in die Originale schreiben kann.

Weitere fehlende Eingaben aus `stage2_results.json`: `kraken_funding/PF_{XBT,ETH,SOL}USD_funding.csv` (für `spot_ref.py` / Kraken-Gegenprobe). Sie werden von `stage2.py` nicht gelesen und sind in `OFFENE_PUNKTE.md` vermerkt.
