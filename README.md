# Project Aurum II

Eigenstaendige Handelsplattform ausschliesslich fuer Kryptowaehrungen. Spot und Perpetual Futures, long und short.

Angelegt am 15.09.2026. Nachfolger von Project Aurum, aber ohne Code-Uebernahme im Bestand.

## Grundhaltung

Forschung zuerst, danach Paper, danach allenfalls Live mit kleinem Kapital. Ein negatives Ergebnis ist ein gueltiges Ergebnis. Es wird nichts gebaut, bevor es nachgewiesen ist.

## Ordner

- `00_doku/` Findings-Digest, Architektur- und Umsetzungsspec, Entscheidprotokoll
- `01_forschung/` Stufenplan 0 bis 5, je Stufe Vorregistrierung und Ergebnisbericht
- `02_daten/` Datenvertrag, Universum, Integritaetsregeln, Marktdaten
- `03_engine/` Code der Handelsplattform
- `04_betrieb/` Betriebskonzept, Runbook, Ueberwachung, Alarmierung
- `05_evidenz/` Kostenmodell, Evidenz-Gates, Lauf-Registratur, Testberichte

## Einstieg

Zuerst `00_doku/AURUM_II_FINDINGS_DIGEST_2026-09-15.md` lesen, danach `00_doku/AURUM_II_ARCHITEKTUR_UND_UMSETZUNG_2026-09-15.md`.

## Harte Regeln

1. Signale nur auf abgeschlossenen Bars. Erzwungen im Datenmodell, nicht durch Disziplin.
2. Ein Kostenmodell fuer das ganze System. Kein Modul haelt eigene Gebuehrenwerte.
3. Backtest, Paper und Live rechnen mit demselben Code.
4. Datenschreiben ist validierend, fail-closed und atomar.
5. Ein Motor, ein Lock, Eigentumsmarke je Position.
6. Kill-Switch gilt fuer jeden Order-Pfad ohne Ausnahme.
7. Forschung und Handel sind physisch getrennt.
8. Kapital folgt der Evidenz.
