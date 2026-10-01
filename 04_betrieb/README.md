# Betrieb

## Betriebsort

Aurum II laeuft **nicht** als Fenster-App auf dem Mac. Genau diese Bauweise hat das Altprojekt vom 31.07.2026 bis mindestens 15.09.2026 still stehen lassen, ohne Alarm. Die Systemberechtigungen von macOS blockierten die Hintergrunddienste mit Status 126.

Optionen: dauerhaft laufender kleiner Rechner (Raspberry Pi) oder kleiner Cloud-Server. Entscheid offen, siehe `00_doku/ENTSCHEIDE.md`.

## Ueberwachung

- Heartbeat jede Minute in die Datenbank. Ausbleiben loest Alarm aus.
- Datenfrische in **Kalendertagen**, nicht in Datensatz-Zeilen.
- Eine Warnung, die zweimal wiederkehrt, wird zum Alarm.
- Ein Alarm geht als Nachricht auf das Telefon, nicht in eine Protokolldatei.
- Taeglicher Bericht mit Datenfrische, Heartbeat, Positionen, Funding-Saldo, Soll-Ist-Abgleich, Kill-Switch-Zustand.

Hintergrund: Die Ueberwachungsgroesse `stale_days` meldete im Altprojekt null, weil sie die letzten 21 Pruefzeilen auswertete statt Kalendertage. Ein Vorwarnhinweis vom 25.07.2026 blieb ungelesen und kostete sechs Wochen.

## Oberflaeche

Lesend. Schreibende Endpunkte nur mit Token, Freigabe fuer fremde Ursprunge geschlossen. Im Altprojekt konnte jede Webseite im Browser den Autopiloten starten und den Not-Aus zuruecksetzen.

## Freigabedisziplin

Neue Regel zuerst im Schatten. Getrennte Freigabe je Aenderung. Ein Parameter je Variante. Definierter Rueckweg. Kuenstlicher Ende-zu-Ende-Test im Trockenlauf statt Warten auf ein Marktsignal. Git von Tag eins.
