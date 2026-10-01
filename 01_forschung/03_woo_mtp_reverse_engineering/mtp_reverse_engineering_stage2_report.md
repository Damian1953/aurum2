# MTP Reverse Engineering — Bericht Stufe 2: isolierte Varianten und Abschluss

**Project Aurum II, 03_woo_mtp_reverse_engineering. 16.09.2026. Eingefroren und nicht mehr variiert: CMC-Datenquelle, Same-Day-Close-Entry, Wilder-ATR(180), Stop «letzter Leg minus 6.5 ATR» ohne Trailing, Ziel «erster Leg plus 37.5 ATR», Exits intraday am Niveau. Variiert wurde ausschliesslich je ein Bestandteil der Entry- und Leg-Logik gegenüber der Basis aus Stufe 1. Keine neuen Parameter, keine Optimierung auf 16 von 16.**

## 1. Basis und Messgrössen

Basis (Stufe 1): Pivot-Breite 5, Entry per Tageshoch, Add-on per Schluss über Niveau, Abstand 1.5 ATR, Niveau verbraucht durch ein Tageshoch darüber, Min Age 20, Max Age 365. Messgrössen je Variante: Entry-Tag exakt, Exit-Tag exakt, Exit-Preis unter 0.1 Prozent, Leg-Zahl exakt, zusätzliche Trades ohne Gegenstück (FP, ohne den offenen Trade ab August 2026).

| Variante | Entry | Exit-Tag | Exit-Preis | Legs | FP | Trades |
|---|---|---|---|---|---|---|
| **Basis** | **13** | **13** | **10** | **9** | 1 | 17 |
| V-C1 Niveau verbraucht nur durch Einstieg, Leg oder Schluss darüber | 12 | 11 | 8 | 8 | 2 | 16 |
| V-C2 Niveau verbraucht nur durch Schluss darüber | 12 | 10 | 7 | 6 | 2 | 16 |
| Min Age 60 | 3 | 2 | 1 | 2 | 5 | 11 |
| Must Close Above OFF (Legs per Tageshoch) | 12 | 11 | 8 | 8 | 2 | 17 |
| Must Close Above ON auch für Entries | 7 | 7 | 5 | 5 | 2 | 15 |
| V-C2 mit Pivot-Breite 8 | 12 | 9 | 8 | 8 | 1 | 16 |
| V-C2 mit Pivot-Breite 10 | 12 | 10 | 9 | 9 | 2 | 17 |

Keine Variante schlägt die Basis in der Summe. Die Basis bleibt die Referenz-Regelmenge (Spezifikation Abschnitt 9).

## 2. Was die Varianten im Einzelnen zeigen

**Verbrauch eines Niveaus (V-C1, V-C2).** Beide Varianten lösen die zwei offenen Konflikte aus Stufe 1: Trade 7 wird am 02.04.2019 exakt eröffnet und am 26.06.2019 exakt am Ziel geschlossen, und Trade 13 erhält exakt acht Legs mit dem korrekten letzten Leg 02.01.2024 (Basis: fünf Legs). Beide Varianten erzeugen aber neue Fehler an anderer Stelle: einen Trade ab 20.07.2017, den MTP nicht zeigt (dadurch entfällt Trade 6), und ein Add-on am 20.05.2024 in Trade 14, das die Position am 05.07.2024 am Stop beendet statt am 13.11.2024 am Ziel (dadurch verschieben sich Trade 15 und 16). Die Fehlermengen sind disjunkt: Basis erklärt Trade 6 und 14, V-C2 erklärt Trade 7 und 13. Das ist kein Feinjustierungsproblem, sondern ein Hinweis darauf, dass die Verbrauchsregel eine dritte Form hat, die keine der beiden dokumentierten Alternativen trifft, oder dass die Pivot-Definition an diesen Stellen anders ist. Klassifikation: **noch nicht identifiziert.** Die entscheidende Beobachtung ist die Leg-Folge von Trade 13. Basis sagt 18.01., 20.01., 21.06., 23.10.2023 und 02.01.2024 voraus, V-C2 sagt 18.01., 20.01., 17.03., 10.04., 03.07., 23.10., 01.12.2023 und 02.01.2024 voraus. MTP zeigt acht Legs. Die Trade-Data-Tabelle des Backtesters entscheidet das ohne weitere Rechnung.

**Min Age 60.** Reduziert die Treffer auf 3 von 16, weil fast alle beobachteten Niveaus zwischen 20 und 60 Tage alt waren (Trade 10 und 11: 29 und 31 Tage, Trade 13: 74, Trade 14: 32, Trade 15: 34). Min Age 20 als Mindestalter des Niveaus ist damit **gesichert** im Sinn von «60 ist ausgeschlossen». Vorhersage für einen Backtester-Lauf mit Min Age 60: Trade 4, 5, 7, 9, 10, 11, 12, 14, 15, 16 verschwinden oder verschieben sich, es bleiben etwa elf Trades mit anderen Terminen. Diese Vorhersage ist falsifizierbar und kostet nur einen Lauf.

**Must Close Above OFF.** Als Bedingung nur für Add-ons wirkt der Schalter: Ohne ihn erhält Trade 14 am 17.05.2024 ein Add-on (Schluss 67 052 unter dem Niveau 67 234) und endet am 05.07.2024 am Stop mit rund minus 40 Prozent gegenüber dem beobachteten Exit. Vorhersage für einen Backtester-Lauf mit Must Close Above OFF: Trade 14 endet am 05.07.2024 statt am 13.11.2024, Trade 13 hat sechs statt acht Legs, Trade 15 beginnt nicht am 20.01.2025. Als Bedingung für Entries verschlechtert der Schalter die Treffer auf 7 von 16, weil Trade 13 (Schluss unter Niveau am Einstiegstag) und Trade 4 nicht mehr entstehen. **Stark indiziert:** «Must Close Above» wirkt auf Add-ons, nicht auf den ersten Einstieg. Das ist eine ungewöhnliche Asymmetrie und gehört zu den Punkten, die ein Backtester-Lauf bestätigen sollte.

**Pivot-Breite.** 5 und 8 bis 10 liegen nahe beieinander, 3 und 15 sind schlechter. Trade 8 (Einstieg über ein Hoch, das sechs Tage nach einem höheren Hoch lag) verlangt eine Breite von höchstens 5, Trade 14 (kein Add-on über ein Hoch, das neun Tage nach einem höheren lag) verlangt mindestens 9. **Noch nicht identifiziert.** Möglich ist, dass die Pivot-Definition nicht symmetrisch über Tage, sondern über eine andere Grösse läuft (etwa Schlusskurse links, Hochs rechts). Das wurde nicht getestet, weil es nicht vorab dokumentiert war, und wird als Vorschlag für Planversion 2 notiert.

## 3. Stand der Rekonstruktion

Gesichert (Klasse 1): Datenquelle, Zeitraster, Wilder-ATR(180), Fill am Schluss, Stop-Formel, Stop-Neusetzung bei Add-on, kein Trailing, Ziel-Formel, Ziel bleibt bei Add-ons fix, Exits intraday am Niveau, SMA200 nur beim Einstieg, kein FBO nötig. Diese elf Bestandteile reproduzieren jeden Exit ab 2017 auf unter 0.1 Prozent, sobald Entry und Legs stimmen.

Stark indiziert (Klasse 2): Niveau als Pivot-Hoch mit Alter 20 bis 365, Auslöser per Tageshoch, Add-on als weiterer Pivot-Ausbruch mit Schluss über Niveau, keine Leg-Obergrenze, Gesamtschliessung.

Noch nicht identifiziert (Klasse 3): Verbrauch eines Niveaus, exakte Pivot-Breite, Leg-Abstand, Leg-Grössen, Sizing der Erstposition, Funktion von «Close Above Within 30», Gap-Fill-Regel, Failed-Breakout-Mechanismus.

Die Regelmenge in Spezifikation Abschnitt 9 ist die einfachste, die 13 von 16 Trades vollständig erklärt. Sie wird als Basis für die Validierungsstufe verwendet. Jeder Klasse-3-Bestandteil geht dort als ausgewiesene Annahme ein.

## 4. Welche Informationen jetzt tatsächlich noch fehlen

In dieser Reihenfolge, jede mit dem, was sie entscheidet:

1. **Leg-Termine von Trade 13** (acht Legs, 18.01.2023 bis 02.01.2024). Entscheidet Verbrauchsregel und Leg-Abstand in einem Schritt, weil Basis und V-C2 disjunkte Terminfolgen vorhersagen. Wertvollste Einzelinformation.
2. **Leg-Termine von Trade 16** (sieben Legs, 25.04. bis 05.10.2025) und **Trade 7** (fünf Legs, 02.04. bis 26.06.2019). Entscheiden Pivot-Breite (Trade 16: ob 22.04. oder 25.04.2025 der erste Leg war) und die Verbrauchsregel ein zweites Mal.
3. **Leg-Termine von Trade 3** (neun Legs 2016) nur, falls die CMC-Historie 2016 geklärt ist, sonst geringer Wert.
4. **Backtester-Lauf mit Min Age 60** und **Backtester-Lauf mit Must Close Above OFF** auf BTC. Beide Vorhersagen in Abschnitt 2 sind konkret genug, dass ein Blick auf die Trade-Tabelle reicht. Sie prüfen die Spezifikation von aussen, nicht nur an den 16 Trades, an die sie angepasst wurde.
5. **Ein zweites Asset mit denselben Defaults** (ETH), mindestens Entry-Datum, Exit-Datum, Legs, Ø Entry und Exit-Preis. Prüft, ob die Spezifikation asset-unabhängig ist, was die Validierungsstufe voraussetzt.
6. **Position-Sizing-Einstellung des Backtesters** (Risiko je Trade, maximale Exposure, Anzahl Assets im Lauf). Ohne sie bleiben Leg-Grössen und damit die Ø-Entry-Werte unprüfbar. Für die Validierungsstufe wird ein eigenes Sizing festgelegt, deshalb blockiert diese Information nichts, sie würde nur die Replikation exakter machen.
7. **Bestätigung der CMC-Datenfassung** vor 2017 (etwa durch ein Backtester-Chart mit Kurswerten 2015). Gering, betrifft nur Trades 1 bis 3.

Nicht mehr nötig: weitere BTC-Kursquellen, Stundendaten, andere ATR-Varianten, weitere Multiplikatoren.

## 5. Dateien

`mtp_reconstructed_spec_v1.md`, `sim_mtp5.py` (Vollsimulation mit allen Varianten als Schalter), `stage2_variants.txt` (vollständige Ausgabe je Variante mit Leg-Terminen).
