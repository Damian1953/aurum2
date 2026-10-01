# Daten

## Datenvertrag

Jede Zeitreihe traegt Quelle, Zeitzone, Bar-Intervall, Regel zur Bar-Vollstaendigkeit, Erstabruf, letzte Aenderung und Version.

**Ein laufender Bar wird von der Zugriffsschicht nicht herausgegeben.** Damit ist Look-ahead im Live-Pfad baulich ausgeschlossen. Signal auf Bar t, Ausfuehrung fruehestens zur Eroeffnung von t plus eins. Bei Stop-Fills gilt der unguenstigere Wert aus Stop und Eroeffnung.

## Schreibpfad

1. Klassifikation jeder Zeile in kritisch und Warnung.
2. Ein Batch mit einem kritischen Defekt wird vollstaendig abgelehnt und quarantaenisiert.
3. Datei-Lock, temporaere Datei im selben Verzeichnis, flush und fsync, Validierung, atomares Ersetzen.
4. Jede verworfene Zeile wird mit Grund protokolliert.

Kritisch sind: fehlendes oder ungueltiges Datum, fehlende Werte in Kursspalten, Schluss ausserhalb der Hoch-Tief-Spanne, nicht positive Werte, nicht monotone Zeitachse, Duplikate.

Hintergrund: Im Altprojekt erzeugte eine einzige Zeile ohne Datum in DOT_1d.csv einen dauerhaften Preisfehler von plus 140 Prozent. Ein Scan aller 137 Dateien fand elf betroffene Dateien in elf Defektklassen.

## Universum

Point-in-Time. Coin ab tatsaechlichem Listing waehlbar. Delistete Coins bleiben in der Historie. Quartalsweise mechanische Neuauswahl ohne Ermessen.

Start: BTC, ETH, SOL. Erweiterung nur bei nachgewiesenem Eigenbeitrag. Die Korrelation zwischen den Majors liegt belegt bei 0.85 bis 0.93.

## Perp-Serien

Funding-Rate je Zahlungsperiode mit echtem Zeitstempel, Open Interest, Mark- und Index-Preis getrennt, Basis Spot gegen Perp, Liquidationsschwelle je Position.

## Nachladen der Historie

Die Boersen-Hosts sind aus der Claude-Umgebung heraus gesperrt. Das Nachladen laeuft deshalb
direkt auf dem Mac:

1. Im Finder `02_daten/Daten-nachladen.command` doppelklicken (oder im Terminal
   `python3 nachladen_historie.py`).
2. Beim ersten Mal fragt macOS allenfalls nach Zugriff auf den Ordner Dokumente. Bestaetigen.
3. Der Lauf holt Binance Vision ab 2017 fuer zehn Symbole und Kraken fuer die letzten 720 Tage.
   Dauer beim ersten Mal einige Minuten. Spaetere Laeufe sind inkrementell.
4. Am Ende erscheint eine Pruef-Tabelle. Alles muss auf OK stehen.

Nur Standardbibliothek, kein pandas noetig. Ergebnis unter `raw/`, siehe `raw/README.md`.

`python3 nachladen_historie.py --check` prueft nur, ohne zu laden.

## Stufe 2: Perpetual-Daten

`Daten-nachladen-Futures.command` doppelklicken. Laedt in zwei Schritten:

1. `--futures`: Binance-USDT-M-Funding je Zahlungszeitpunkt (ab 2019-09) und Perp-Tageskerzen, fuer alle zehn Symbole. Einige Minuten.
2. `--oi`: Open Interest aus Tagesdateien (ab dem ersten verfuegbaren Tag, vermutlich Ende 2021). Ein Abruf je Tag und Symbol, deshalb langsam, ungefaehr eine bis zwei Stunden fuer zehn Symbole. Der Lauf sichert alle 200 Tage einen Zwischenstand und kann jederzeit abgebrochen und mit demselben Befehl fortgesetzt werden.

Beide Schritte sind inkrementell. Am Ende `python3 nachladen_historie.py --check`, alles muss OK sein. Coins, die bei Open Interest eine Luecke ueber drei Tage zeigen, werden fuer D-OI ausgeschlossen (fail-closed, siehe Vorregistrierung Abschnitt 9).
