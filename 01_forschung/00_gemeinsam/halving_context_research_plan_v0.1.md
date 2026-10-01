# Halving als Kontextvariable — Forschungsplan, Version 0.1

**Project Aurum II, `01_forschung/00_gemeinsam/`. 17.09.2026. Status: Plan zur Prüfung, explorativ. Kein Rechenlauf. Das Halving ist nie ein Signal, nur eine Kontextvariable für bereits vorhandene Signale.**

## 0. Frage

Ändert sich die bedingte Erfolgswahrscheinlichkeit eines bereits vorhandenen BTC-Signals in unterschiedlichen Phasen des Halving-Zyklus? Und, getrennt: Verhält sich ein XRP-, DOT-, ETH- oder SOL-Signal in den Phasen des BTC-Zyklus unterschiedlich, als exogene Crypto-Cycle-Variable? Nie: Ist das Halving ein Long-Signal.

## 1. Faktenbasis

Halvings: 28.11.2012 (Block 210000), 09.07.2016 (Block 420000), 11.05.2020 (Block 630000), 20.04.2024 (Block 840000). Nächstes Halving bei Block 1050000, nach der Protokollregel von zehn Minuten je Block rund 1458 Tage nach dem letzten, tatsächliche Abstände waren 1319, 1402 und 1441 Tage, weil Blöcke im Mittel schneller kommen. Für die Datenhistorie von Aurum II (CMC ab 2013, Kraken ab 2013 dünn, Binance ab 2017) liegen drei Halvings im Fenster, das vierte ist in der Zukunft. Das sind drei vollständige Zyklen und ein angebrochener. Jede Statistik darüber ist explorativ und mechanistisch, keine Stichprobe im Sinn der bisherigen Stufen.

## 2. Vorregistrierte Kontextmerkmale, alle point-in-time

| Merkmal | Definition | Look-ahead |
|---|---|---|
| `days_since_halving` | Tage seit dem letzten Halving, am Tag t | keiner |
| `days_to_next_expected_halving` | Datum des letzten Halvings plus 1458.3 Tage minus t (Protokollregel, deterministisch, ohne Kenntnis des tatsächlichen nächsten Datums) | keiner, die Regel ist vorab bekannt, ihre Ungenauigkeit (30 bis 140 Tage zu spät) wird ausgewiesen |
| `cycle_position` | `days_since_halving` / 1458.3, Wert 0 bis rund 1 | keiner |
| `cycle_phase` | Quartal des Zyklus nach `cycle_position`: Q1 unter 0.25, Q2 bis 0.50, Q3 bis 0.75, Q4 darüber, Grenzen vorab nach Kalender, nicht nach Ergebnis | keiner |
| `blocks_since_halving` | nur wenn eine tägliche Blockhöhen-Reihe mit dokumentierter Quelle und Prüfsumme geladen werden kann (Kandidaten: öffentliche Block-Explorer-APIs), sonst entfällt das Merkmal fail-closed. Blockhöhe am Tag t ist die letzte Blockhöhe vor 00:00 UTC des Tages t+1, dem Tag t zugeordnet | keiner bei korrekter Zuordnung |

Keine Halving-Schwelle wird nach Performance gesetzt. Die vier Phasen sind das einzige Raster.

## 3. Signale, die konditioniert werden

Nur bereits definierte, unabhängig von diesem Plan vorregistrierte Signale: die 16 beobachteten MTP-BTC-Trades (Rekonstruktion) und die A-Ebene-Trades der MTP-Spezifikation v1 auf BTC ab 2014 (aus der Validierung vorhanden, als Berichtsdaten), die BTC-B-Ausbrüche (4h) und BTC-RTC-Signale aus der Discovery, sobald sie vorliegen. Für XRP, DOT, ETH, SOL die RTC- und Breakout-Signale ihrer Pläne, konditioniert auf die BTC-`cycle_phase`, ausdrücklich als externe Variable bezeichnet, nie als coin-eigenes Halving.

## 4. Auswertung

Je Signalquelle: Erwartung je Trade, Trefferquote und Anteil der Trades über 3 R nach `cycle_phase`, Tabelle mit vier Zeilen und Trade-Zahlen. Statistik: Permutationstest, bei dem die Phasenzuordnung blockweise über ganze Zyklen permutiert wird (nicht über Trades), damit die Abhängigkeit innerhalb eines Zyklus erhalten bleibt. Mit drei Zyklen gibt es nur sechs Permutationen, der kleinste erreichbare p-Wert ist 0.17. Das ist der formale Ausdruck dafür, dass diese Analyse keine Signifikanz liefern kann. Berichtet wird deshalb die Effektgrösse mit Vertrauensintervall aus dem Trade-Bootstrap innerhalb der Phase, mit dem Vermerk, dass Zyklen nicht unabhängig sind.

Zusätzlich eine mechanistische Prüfung, die keine Zyklen zählt: Korrelation der 90-Tage-Vorwärtsrendite von BTC mit `cycle_position` als stetige Variable, mit Block-Bootstrap über 180-Tage-Blöcke, als Bericht.

## 5. Was daraus folgen darf

Nichts, was ein Signal ändert. Zulässig ist eine Hypothese der Form «BTC-RTC-Signale in Phase Q1 und Q2 haben eine höhere Erwartung als in Q4», festgehalten für eine spätere Stufe, prüfbar erst mit dem fünften Halving 2028 oder mit Daten anderer Art. Unzulässig ist ein Filter «nur in Phase Qx handeln» in irgendeiner Vorregistrierung, bevor eine unabhängige Stichprobe existiert. Unzulässig ist auch die Verwendung als Exposure-Steuerung.

## 6. Offene Entscheidungen

1. Ob `blocks_since_halving` geladen wird (Empfehlung: nein, `days_since_halving` reicht für vier Phasen, die Blockhöhe fügt nur Genauigkeit im Tagesbereich hinzu).
2. Phasenraster in Quartalen bestätigen (Alternative: Drittel).
3. Ob die Analyse nach der Discovery (Empfehlung, weil dann alle Signale vorliegen) oder schon mit den MTP-Trades allein läuft.
