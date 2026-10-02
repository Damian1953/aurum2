# forward/ – gemeinsame Betriebsteile aller Forward-Linien

| Datei | Inhalt |
|---|---|
| `heartbeat.py` | Eine Statuszeile je Runner (Collector, PAPER v1.0, Sleeves A/B, VOLTARGET), **ALARM**, wenn ein erwarteter Lauf fehlt (> 26 h) oder fehlgeschlagen ist. Nur Lesen, Exit 1 bei Alarm. Kein cron-Eintrag. |
| `voltarget_bericht.py` | Abschnitt VOLTARGET im gemeinsamen einseitigen Wochenbericht; liest nur `paper_voltarget/state/state_latest.json` und `voltarget/voltarget_config.json`, importiert keinen VOLTARGET-Code. |

Der Wochenbericht selbst ist `paper/wochenbericht.py` (feste Gestaltung `LAYOUT`, höchstens 72 Zeilen). Heartbeat und
gemeinsamer Bericht sind Voraussetzung für den Start von Sleeve A/B und VOLTARGET.

Ablage auf Branch `sleeves-v1`: Der Bericht (`paper/wochenbericht.py`) wurde dort bereits umgebaut; VOLTARGET (Branch
`voltarget-v0`) liefert nur seine Zustandsdatei nach der Schnittstelle in `voltarget_bericht.py`. So berühren die beiden
Branches keine gemeinsame Datei.
