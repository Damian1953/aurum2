# Reproduzierbarkeit

## Grundsatz

Alle Dateien aus dem Tag `original-2026-10-01` sind eingefroren und werden nie geändert (`make verify-frozen` prüft das per `git diff`). Neue Funktion entsteht nur in **neuen** Dateien:

| Ort | Inhalt |
|---|---|
| `portable/<modul>/*` | mechanisch erzeugte Kopien der Originalskripte, erzeugt von `tools/make_portable.py` |
| `config/cost_model_v1.json` + `pylib/aurum_costs.py` | zentrales Kostenmodell K0/K1/K2 |
| `tools/` | Arbeitsbereich, CI, Prüfungen |
| `build/root/` | generierter Arbeitsbereich (gitignored) |

## Projekt-Root `AURUM_ROOT`

Die Originalskripte stammen aus einer Sandbox mit festen Pfaden `/home/claude/{rtc,yamato,micro,dt,s2,holdout,…}`. Die portablen Versionen setzen im Kopf

```python
_AR = os.environ.get("AURUM_ROOT") or <Arbeitsbereich relativ zur Datei>
```

und ersetzen jedes `"/home/claude` durch `_AR + "`. Das Layout ist in `tools/aurum_layout.py` beschrieben, `tools/stage_root.py` baut es in `build/root` auf. Eingefrorene Dateien werden dabei **kopiert**, damit kein Lauf in das Repo schreiben kann. Read-only-Daten werden verlinkt (`holdout`, `data/raw`).

Achtung: Die eingefrorenen Libraries `rlib.py` und `dtlib.py` setzen `/home/claude/...` an den Anfang von `sys.path`. Existiert `/home/claude`, würde das den Arbeitsbereich überschatten. `tools/ci.py` bricht deshalb ab, wenn der Pfad existiert. Die Libraries selbst bleiben unverändert, ihre SHA-256 sind Teil aller Läufe.

## Transformationsregeln (`tools/make_portable.py`)

| Regel | Wirkung |
|---|---|
| `paths` | `"/home/claude` → `_AR + "` |
| `sha_self` | `sha(__file__)` → `sha(_FROZEN_SELF)`; `_FROZEN_SELF` zeigt auf die eingefrorene Originaldatei mit gleichem Namen im Arbeitsbereich |
| `cost:NAME=section` | die Zuweisung `NAME = {...}` wird per AST durch `NAME = _ac.load("section")` ersetzt |

`make portable-check` erzeugt alles neu im Speicher und vergleicht mit `portable/` (0 Abweichungen, keine verwaisten Dateien). Jede portable Datei ist damit nachweislich **Original modulo Pfad und Kostenquelle**.

## Wie die `*_expected_shas.txt` zu den neuen Dateien stehen

1. **Originale** (Skripte, Libraries, Vorregistrierungen, Ergebnisse): Die Listen gelten unverändert und werden von `make verify-frozen` vollständig geprüft. Bekannte Abweichungen stehen mit Begründung in `tools/frozen_allowlist.txt`:
   - `ENTSCHEIDE.md` wird fortgeschrieben.
   - `rm_2026-09-18_expected_shas.txt` nennt noch mlib v0.1.
2. **Skript-SHAs in den Ausgaben** (z.B. `script_sha256` in `*_measure.json` oder `eval_*.json`): Die portablen Skripte schreiben über `sha_self` die SHA der **Originaldatei**, nicht ihre eigene. Das bleibt aussagekräftig, weil
   - `make portable-check` belegt, dass sich die laufende Datei vom Original nur durch die dokumentierten Regeln unterscheidet,
   - die Laufzeit-Asserts auf Eingabe-SHAs (rlib, ylib, dtlib, Kandidatendateien, Holdout-Discovery, Daten) unverändert greifen und
   - die Ausgaben bitgleich zu den eingefrorenen Expected-SHAs sind (siehe unten). Eine verfälschte Logik würde sich in den Ausgaben zeigen.
3. **Libraries mit Kosten** (`ylib.py`, `mlib.py`, `s2lib.py`): Im Arbeitsbereich ersetzt die portable Version die Kopie. `rlib` prüft `ylib` nicht per SHA, deshalb ist das unkritisch. `tests/test_cost_model.py` prüft per AST, dass `config/cost_model_v1.json` wertgleich mit jeder eingefrorenen Kopie ist (inkl. der abgeleiteten Basispunkte in `dtlib`: 99 bp und 89 bp).
4. **Neue Ergebnisse** aus portablen Läufen brauchen eigene, neue Expected-SHA-Listen. Bestehende Listen werden nie überschrieben.

## Prüfungen

| Befehl | Inhalt | Dauer |
|---|---|---|
| `make test` | 34 eingefrorene Tests (rlib 7, ylib 9, mlib 5, simulate 8, dtlib 5) als portable Kopien im Arbeitsbereich, dazu Repo-Tests `tests/` | ca. 25 s |
| `make repro-fast` | DT-Messung BTC/XRP/DOT (9 Dateien gegen `dt_expected_shas.txt`), XRP v1.0 Outcome-Lauf (21 Dateien), BTC YAMATO Stufe B (21 Dateien + stdout-Log) | ca. 1 min |
| `make repro` | zusätzlich Stufe 2 Volllauf mit eingefrorenem `stage2.py` und portabler `s2lib`: alle Felder in `results`, 37 Trade-Dateien, `stage2_config_log.csv`, Prereg-SHA | ca. 5 min |
| `make verify-frozen` | Git-Tag-Vergleich, alle Expected-SHA-Listen, Holdout-Manifest v1.1 (nur Prüfsumme, die Validation-Dateien werden nicht geladen) | Sekunden |
| `make ci` / `make ci-fast` | alles / alles ohne Stufe 2 | |

`stage2_results.json` selbst ist nicht bytegleich, weil darin Laufzeitpfade und Zeitstempel stehen. Verglichen werden deshalb alle Felder unter `results`.
