# Entscheidprotokoll Aurum II

Jeder Entscheid wird hier mit Datum, Begruendung und Quelle festgehalten. Wer einen Entscheid aendert, ergaenzt einen neuen Eintrag und loescht den alten nicht.

## 2026-09-15 — Aurum II wird als eigenstaendiges Projekt gefuehrt

Kein Fork des alten aurum-trader. Uebernommen werden Erkenntnisse und Bausteine, nicht der Bestand. Begruendung im Findings-Digest, Abschnitt 6.

## 2026-09-15 — Reihenfolge Forschung, Paper, Live

Die Stufenlogik wird zu Ende gefuehrt, bevor ein handelndes System gebaut wird. Zwischen Stufe 2 und Stufe 3 steht ein echter Abbruchpunkt.

## 2026-09-15 — Spot und Perpetual Futures, long und short

Erweiterung gegenueber dem Long-Flat-Guardrail der Regime-Research V1. Folge: Regime-Definitionen werden symmetrisch, Funding und Basis werden eigene Forschungsstufe, Margin- und Liquidationsmodell werden Pflicht.

Vorbehalt: Fuer Short, Hebel und Funding existiert im Altbestand kein einziger validierter Wert.

## 2026-09-15 — Kein Profit-Guard, keine fixe Gewinnmitnahme

Belegt: minus vier CAGR-Punkte ohne Drawdown-Nutzen, 62 Prozent der Ausloesungen schnitten Gewinner ab. Quelle MOMENTUM_REPLAY_VALIDIERUNG_2026-07-14.md.

## 2026-09-15 — Kein Intraday, kein Scalping

Doppelt widerlegt, formal im Backtest mit Score 30 von 100 und null Trades, oekonomisch live mit einer Fee-to-Gross-Quote von 220 Prozent. Quelle INTRADAY_NEUKONZEPT_KESTREL_2026-07-02.md.

## 2026-09-15 — Altsystem Aurum wird eingefroren

Der Bot wird nicht wieder gestartet. Kill-Switch bleibt aktiv, die Datensammlung bleibt aus. Offene Positionen und der Fremdbestand SOL bleiben vorerst unberuehrt und werden spaeter bewusst abgewickelt. Aurum II startet nicht neben einem halb laufenden Vorgaenger.

## 2026-09-15 — Kostenstufe bestimmt die Strategieauswahl

Kraken Spot kostet auf der untersten Stufe 0.40 Prozent Maker und 0.80 Prozent Taker je Seite, Kraken Derivate 0.02 Prozent Maker und 0.05 Prozent Taker. Faktor 16 bis 20. Jede Strategie mit nennenswertem Umschlag gehoert damit auf die Perpetual-Seite, nicht auf Spot. Quelle Kraken Fee Schedule, abgerufen am 15.09.2026.

## 2026-09-15 — Strategieklassen, die nicht weiterverfolgt werden

Market Making nach Avellaneda-Stoikov, Orderflow- und Microstructure-Signale, Grid-Trading, Kurzfrist-Mean-Reversion sowie Elliott Wave und Fibonacci als Signalquelle. Begruendung siehe Strategiebewertung vom 15.09.2026. Kurzfassung: gemessener Brutto-Edge kleiner als die Handelskosten, beziehungsweise keine statistisch belastbare Evidenz.

## 2026-09-15 — Aurum II handelt auf Perpetuals, nicht auf Spot

Begruendung ist der Kostenfaktor, nicht der Hebel. Dieselbe Strategie mit fuenf Tagen Haltedauer liefert auf Spot zum Taker-Tarif minus 27 Prozent und auf Perpetuals zum Maker-Tarif plus 27 Prozent pro Jahr. Rechnung in 01_forschung/00_datenbasis/AURUM_II_STRATEGIEBEWERTUNG_2026-09-15.md, Abschnitt 2.5, reproduzierbar ueber 05_evidenz/kostenhuerde_teil1.py und _teil2.py.

## 2026-09-15 — Mittlere Haltedauer mindestens drei Tage

Angestrebt fuenf bis zwanzig Tage. Alles Schnellere ist auf jeder erreichbaren Gebuehrenstufe ein Verlustgeschaeft.

## 2026-09-15 — Funding ist Kostenposition, nicht Ertragsbaustein

Eigene Messung auf den Kraken-Funding-Reihen: BTC plus 2.69 Prozent, ETH plus 3.05 Prozent, SOL minus 0.31 Prozent annualisiert ueber ein Jahr. Funding gehoert in den Kostenfilter vor dem Einstieg, nicht in einen eigenen Sleeve.

## 2026-09-15 — Stufe 0 ist nicht abgeschlossen

Die Strategiebewertung steht, die Datenbasis nicht. Offene Punkte: leere Kraken-Datei fuer Bitcoin seit 17.07.2026, Kraken-Historie nur zwei Jahre, Universum-Archiv ohne Listing-Daten, Funding nur ein Jahr und nur drei Kontrakte.

## 2026-09-15 — Stufe 1 eingefroren

Vorregistrierung Version 1.0, SHA-256 e7b28d3396ad125781f26ee56a1b59111b77ef9cb7a80ddec2fc56a1ac9c2dbb. Alle vier Punkte aus Abschnitt 12 bestaetigt: Schwellen unveraendert, Kalenderjahre primaer und Halving-Zyklen als Gegenprobe, zehn Coins, Funding als F1 mitgerechnet. Pruefsummen der 16 Eingabedateien in 01_forschung/01_regime/stage1_input_checksums.txt.

## 2026-09-15 — Stufe 1 Ergebnis: kein Kandidat tauglich

R1 bis R5 verworfen, F1 vorlaeufig verworfen. Scheitern fast ausschliesslich am Median der Verweildauer (36 von 140 Coin-Dimension-Paaren innerhalb), waehrend Jitter (140 von 140) und Wechselrate (121 von 140) bestehen. Kriterium wird nicht nachtraeglich geaendert. Stufe 3 entfaellt, Stufe 2 laeuft ohne Regimefilter. Eine Regime-Version 2 mit Hysterese ist als Hypothese festgehalten, optional. Bericht in 01_forschung/01_regime/stage1_summary.md.

## 2026-09-15 — Stufe 2 Vorregistrierung eingefroren

`01_forschung/02_strategien/stage2_preregistration_v1.md`, Version 1.0, SHA-256 8f576b7a0b1c5a1adf4b6f0c342398bc8500b287a081923f82f95acc58e1b96e.

Entscheidungen vor dem Freeze: Pyramiding Einstieg 0.50, Add-ons 0.25 und 0.25, Maximum 1.00, kein Hebel. Trade-Mindestzahl gestuft nach Konstruktion (Klassen S, M, L) als eigenstaendiges Kriterium, Bootstrap ersetzt sie nicht. Beta-Trennung in zwei Teiltests Alpha und Risikotransformation. Holm auf Block-Bootstrap-p-Werten als Primaerverfahren, Deflated Sharpe Ratio als Sensitivitaet. W0 ohne R-Multiples (n/a). Risikobasiertes Sizing als Zweitlauf: nein. Short-Spiegelungen nur W2, W4, W8. XS21 mitgerechnet, gekennzeichnet. D-OI bedingt mit exakten Datenanforderungen und fail-closed. Binance-Funding-Historie und Perp-Tageskerzen werden vor dem Lauf geladen.

Woo-Kontext (Turtle- und Minervini-Herkunft, Legacy gegen MTP 2.4, Signal-Engine getrennt von Risikoschicht, unsichere Signalhaeufigkeit, unklares Gewinnziel bei 2.4, Shorts als Aurum-Erweiterung) ist als Interpretation in Abschnitt 6 und 21 sowie in `woo_kontext_v1.md` festgehalten, ohne Aenderung an Regeln oder Baendern. Die Eingabe traf vor Protokollierung der Pruefsumme ein und ist in der eingefrorenen Fassung enthalten.

Eingabedaten Spot und Kraken: Pruefsummen wie Stufe 1. Funding, Perp-Kerzen und Open Interest: Pruefsummen werden nach dem Nachladen in `stage2_results.json` festgehalten, bevor eine Strategie gerechnet wird.

Reihenfolge ab jetzt: Nachladen (Datenbeschaffung), Umsetzung von `stage2.py`, Look-ahead-Test, Rechenlauf, Bericht.

## 2026-09-16 — Open Interest: Auswertungsregel und Datenfreigabe D-OI

Die Binance-Metrics-Archive enthalten je Coin an 17 bis 22 Tagen am Tagesende Nullzeilen (0E-8), die keine Marktbeobachtung, sondern ein Artefakt des Archivs sind. Der Loader (`nachladen_historie.py`, Version 4) uebernimmt je Tag die letzte positive Beobachtung (Option A) und zaehlt die betroffenen Tage in `provenance.json` als `zero_rows_days`. Ein Tag ohne positive Beobachtung wuerde als Luecke gelten. Die Regel wurde vor dem Rechenlauf festgelegt und aendert keine Strategie- oder Kriterienregel der eingefrorenen Vorregistrierung.

Datenstand OI (Tageswerte, Binance USDT-M): BTC 2083 Zeilen 2021-01-01 bis 2026-09-14, alle uebrigen neun Coins 1749 Zeilen 2021-12-01 bis 2026-09-14. Keine Luecke groesser als ein Tag, alle Werte positiv. Die Datenanforderungen der Vorregistrierung fuer D-OI (mindestens 1095 Tage, positiv, Luecke hoechstens drei Tage, BTC und ETH) sind erfuellt. D-OI wird gerechnet, Familie D umfasst damit sieben Tests fuer die Holm-Korrektur.

## 2026-09-16 — Stufe 2 Rechenlauf abgeschlossen

Volllauf `stage2.py --tag full` ueber zehn Coins, Vorregistrierung Version 1.0 (SHA-256 8f576b7a…), 985 Konfigurationen, 19 207 Trades, 48 Eingabedateien mit Pruefsummen in `stage2_results.json`. D-OI gerechnet (BTC und ETH erfuellen die Datenanforderungen), Familie D mit sieben Tests fuer Holm.

Ergebnis: 37 primaere Tests. Bestanden: D-CC (marktneutral) und XS21 Long+Short. Teilweise: XS21 Long-only (c6 verfehlt). Verworfen: 34, darunter die gesamte Woo-Matrix Long (Alpha-Teiltest bestanden, c6, c8 und teils c1 verfehlt), alle Short-Spiegelungen, Mean Reversion, Time-Series-Momentum, Funding-Contrarian, Open Interest. Die Urteile sind final.

Vorbehalte, die mit den Urteilen mitgefuehrt werden: XS21 survivorship-behaftet (Abschnitt 15 der Vorregistrierung), D-CC mit Datenvorbehalt, weil die Kraken-Gegenprobe (Vorzeichen f_7d, Abschnitt 9) mit 78.8 bis 88.3 Prozent unter 90 Prozent liegt. Beide bestandenen Konstruktionen sind damit nicht handelbar, sondern Hypothesen mit definierter Pruefung (Point-in-Time-Universum, Kraken-Funding-Historie mit Kapitalmodell). Keine Kriterienanpassung, kein zweiter Lauf auf denselben Daten.

Umsetzungskorrekturen waehrend des Volllaufs, vor der Interpretation behoben, Volllauf danach neu gerechnet, keine Regelaenderung (Bericht Abschnitt 12): c1 Cash-Referenz je Coin ueber die Tage des Coins. D-CC Trade-Kosten der Spot-Beine mit Spot-Satz. Trade-Funding Familien C und D an den Haltetagen. XS21 als Portfolio auf vollem Kapital gepoolt statt als Coin-Mittel. Alle vier unabhaengig nachgerechnet.

Zusaetze zum Bericht ausserhalb von `report2.py`: Spot-Referenz Familie A (Abschnitt 10, Vorregistrierung Abschnitt 12, Bericht kein Kriterium), Kraken-Gegenprobe (Abschnitt 11), Korrekturprotokoll (Abschnitt 12).

Dateien in `01_forschung/02_strategien/`: `stage2_report.md`, `stage2_summary.md`, `stage2_hypotheses_v2.md`, `stage2_mtp_fingerprint.md`, `stage2_results.json`, `stage2_config_log.csv`, `stage2_trades/`, `spot_reference.json`, `kraken_funding_crosscheck.json`, `spot_ref.py`, aktualisierte `stage2.py` und `s2lib.py`.

Naechster Schritt: Planung der naechsten Stufe auf Basis von `stage2_hypotheses_v2.md`. Drei begruendete Arbeiten: Point-in-Time-Universum, Kraken-Funding-Historie mit Kapitalmodell, Forward-Test-Protokoll fuer die Woo-Long-Seite auf Spot. Jede mit eigener kurzer Vorregistrierung und Pruefsumme vor dem Rechnen.

## 2026-09-16 — Naechste Forschungsstraenge festgelegt, Prioritaet 1 gestartet (Planphase)

Stufe 2 und ihr Freeze bleiben vollstaendig unangetastet. Reihenfolge der naechsten Straenge: 1. `03_woo_mtp_reverse_engineering`, 2. `03_xs21_point_in_time`, 3. `03_dcc_kraken_validation`, 4. `03_woo_forward_spot`. Nur Prioritaet 1 ist in Arbeit, die uebrigen sind in `01_forschung/geplante_straenge_v1.md` dokumentiert und nicht gestartet.

Prioritaet 1: Ziel ist die Rekonstruktion der oeffentlich sichtbaren Mechanik von Market Trend Pro aus Primaerdaten (Defaults des Backtesters, sechzehn BTC-Trades aus der Trade-Data-Tabelle, abgelegt in `mtp_btc_trades_observed_v1.csv`). Erfolgsmass ist Reproduktionsgenauigkeit der Signale, keine Performancekennzahl. Drei Ebenen [A] beobachtet, [B] rekonstruiert, [C] spekulativ werden durchgehend getrennt. Plan `mtp_reverse_engineering_plan_v1.md` liegt zur Pruefung vor, Pruefsumme wird nach Freigabe protokolliert, danach beginnt Stufe 1 der Testreihenfolge (Datenquelle und Ausfuehrungskonvention). Kein Rechenlauf vor Freigabe.

Grundregel: Kein Ergebnis aus dem Reverse Engineering wird benutzt, um einen Stufe-2-Test umzudeuten. Neue Woo-Erkenntnisse werden Hypothesen fuer `03_woo_forward_spot`.

## 2026-09-16 — MTP Reverse Engineering: Plan 1.1 freigegeben, Stufe 1 gerechnet

Plan `01_forschung/03_woo_mtp_reverse_engineering/mtp_reverse_engineering_plan_v1.1.md`, SHA-256 eacc391b43c666437189564dfa56c69ccb561cd5d5b563c7a04abf6bfd19ef62. Praezisierungen gegenueber 1.0: Erfolgsdefinition (parsimonische Regelarchitektur, nicht Code-Beweis), Fail-Kriterien je Hypothesenfamilie statt je Strang, Reihenfolge A bis H bestaetigt, UTC ohne Zusatzfreiheitsgrade, Zusatzdaten aus dem Backtester blockieren den Lauf nicht.

Daten: Altprojekt hatte keine BTC-Reihe vor 2017. Nachgeladen ueber Mac-Launcher: Bitstamp ab 2011, Coinbase ab 2015, CoinMarketCap ab 2013 (`02_daten/raw/bitstamp`, `raw/coinbase`, `raw/coinmarketcap`, Loader `nachladen_btc_historie.py`, `nachladen_cmc.py`).

Ergebnis Stufe 1 (`mtp_reverse_engineering_stage1_report.md`): Preisquelle des Backtesters ist CoinMarketCap (drei Ein-Leg-Einstiege exakt), Einstieg zum Tagesschluss, Exits intraday am Niveau. Stop = Schluss des letzten Legs minus 6.5 mal Wilder-ATR(180) am Leg-Tag, kein Trailing, bei jedem Add-on neu gesetzt (acht Stop-Exits ab 2017 auf 0.05 Prozent). Ziel = Schluss des ersten Legs plus 37.5 mal Wilder-ATR(180), fix (fuenf TP-Exits auf 0.08 Prozent). SMA200 nur Einstiegsfilter. Entry-Niveau = juengstes Pivot-Hoch mit Alter 20 bis 365 Tage, Ausbruch per Tageshoch: stark vereinbar (13 von 16 Entries und Exits exakt in der Vollsimulation), zwei Konflikte (Trade 7, 13) offen. Leg-Regel vereinbar (Abstand 1.5 ATR), Leg-Groessen risikobasiert und aus BTC allein nicht identifizierbar. Datenvorbehalt CMC-Historie 2015 bis 2016.

Abgleich: Die Stufe-2-Woo-Matrix hat MTP in allen Modulen anders gebaut (Niveau, Stop-Weite und Trailing, fehlendes Ziel, Filter-Exit, Pyramiding, Ausfuehrung, Daten). Stufe-2-Urteile bleiben unveraendert gueltig fuer das, was sie gemessen haben.

Naechste Tests (maximal drei, im Bericht Abschnitt 10): Leg-Termine aus dem Backtester, zwei Backtester-Laeufe mit geaendertem Min Age und Must Close Above, Vollsimulation der zwei dokumentierten Alternativen zum Niveau-Verbrauch.

## 2026-09-16 — MTP Reverse Engineering abgeschlossen (Stufe 2, Spezifikation v1), Validierungsstufe entworfen

Isolierte Varianten gerechnet (`mtp_reverse_engineering_stage2_report.md`): Verbrauch eines Niveaus (zwei dokumentierte Alternativen), Min Age 60, Must Close Above OFF und ON fuer Entries, Pivot-Breite. Keine Variante schlaegt die Basis aus Stufe 1 (13 von 16 Entry- und Exit-Tage, 10 von 16 Exit-Preise unter 0.1 Prozent). Die Verbrauchsregel bleibt offen (Basis erklaert Trade 6 und 14, Schluss-Verbrauch erklaert Trade 7 und 13, disjunkt). Min Age 60 und Must Close Above OFF liefern konkrete, falsifizierbare Vorhersagen fuer Backtester-Laeufe.

Eingefroren als gesichert: CMC-Datenquelle, Same-Day-Close-Entry, Wilder-ATR(180), Stop letzter Leg minus 6.5 ATR ohne Trailing, Ziel erster Leg plus 37.5 ATR fix, Exits intraday am Niveau, SMA200 nur Einstieg. Spezifikation `mtp_reconstructed_spec_v1.md` mit Klassifikation 1 gesichert, 2 stark indiziert, 3 noch nicht identifiziert.

Fehlende Informationen in Prioritaet: Leg-Termine Trade 13 (entscheidet Verbrauch und Abstand), Trade 16 und 7, Backtester-Laeufe Min Age 60 und Must Close Above OFF, ein zweites Asset, Sizing-Einstellung des Backtesters.

Stufe 2 von Aurum II ist kein Test dieser Mechanik und wird nicht so interpretiert.

Naechster Strang: `03_mtp_validation`, Vorregistrierung Entwurf v0 (`mtp_validation_prereg_draft_v0.md`) mit Ebene A Replikation (CMC, zehn Coins) und Ebene B Real (Kraken-Spot, Kosten K0 bis K2, Slippage, Fill-Regeln), Edge-Retention A nach B, Kennzahlen je Trade und Tail, sieben Entscheidungen offen (Abschnitt 11). Kein Rechenlauf vor Freeze.

## 2026-09-17 — FREEZE: MTP Reconstructed Specification v1 und Validierungs-Vorregistrierung v0.2

`01_forschung/03_woo_mtp_reverse_engineering/mtp_reconstructed_spec_v1.md`, SHA-256 ed85be81521284bdd8627156a29b863f216d3c4acd2341ea2d75f641d416b4a8.
`01_forschung/03_mtp_validation/mtp_validation_prereg_v0.2.md`, SHA-256 733bf2f5ccd709e81f6ced77485d3f3de5c395cd22e99409662150aa49a62bf9.

Entscheidungen (Vorregistrierung Abschnitt 11): Klasse-3-Annahmen in Basis-Form eingefroren (Verbrauch per Tageshoch, Pivot-Breite 5, Abstand 1.5 ATR), Freeze wartet nicht auf Leg-Termine aus dem Backtester, spaetere Leg-Daten sind Out-of-Sample-Replikationskontrolle (Vorhersage Trade 13 im Dokument). Ebene A ohne Kosten, K0 Zusatzzeile. Nominal Initial Risk per Leg 2 Prozent des Sleeve-Startkapitals ohne Compounding. Kriterien: Profit-Faktor 1.5, Retention 60 Prozent, abweichender Exit-Grund hoechstens 15 Prozent, Kriterium 1 auf R_gesamt. Kraken-Historie aus dem Download-Archiv mit Pruefsummen. B2 als dritte Zeile berichtet. Jitter-Nachbarn berichtet ohne Auswahlwirkung. Ebene B mit handelbarer Konvention (erster handelbarer Kraken-Preis nach 00:00 UTC), Same-Day-Close nur Berichtswert. BTC Identifikationsmarkt ohne Validierungsgewicht, Kriterien auf dem Pool der neun uebrigen Coins mit ETH als Pflichtmarkt. R_first und R_gesamt gleichrangig, Open-Risk-Messung je Add-on. Mechanik-Reproduzierbarkeit CMC gegen Kraken als Diagnoseblock.

Ab jetzt keine Aenderung an Spezifikation oder Vorregistrierung. Reihenfolge: Datenbeschaffung und Datenvalidierung (CMC neun weitere Coins, Kraken-Archiv zehn Coins, Pruefsummen, Abdeckung je Coin dokumentiert), dann Umsetzung mit Look-ahead-Test und BTC-Replikationskontrolle, dann ein Volllauf. Kein Validierungslauf vor abgeschlossener Datenpruefung.

## 2026-09-17 — Datenpruefung abgeschlossen, B-Start-Regel festgelegt

Datenpruefung (`01_forschung/03_mtp_validation/datenabdeckung_v1.md`, Pruefsummen in `pruefsummen_daten_v1.txt`): CMC zehn Coins, Kraken-Archiv 2026Q2 (Teile gegen Krakens SHA-256 geprueft, Archiv fc81b54c…), Kraken-API-Ergaenzung ab 01.07.2026, Archiv und API auf 642 Ueberlappungstagen identisch. Alle 30 Dateien ohne Duplikate oder unmoegliche Kerzen. Zusammengefuehrte Kraken-Reihen in `02_daten/raw/kraken_merged/`.

B-Start-Regel (mechanisch, vor jedem Ergebnis): Ebene B beginnt je Coin am spaeteren Datum aus Warmup-Ende A (365 Tage nach CMC-Beginn) und dem ersten Kraken-Tag nach der letzten fehlenden Daily-Bar. Ergibt BTC 2014-12-26, ETH/XRP/LTC 2018-01-13, ADA 2018-10-01, LINK 2019-09-25, SOL 2021-06-17, DOT 2021-08-20, AVAX 2021-12-21, BNB 2025-04-22. Die volle Ueberlappung ohne diese Regel wird nur als Berichtswert gefuehrt. BNB bleibt im Universum, in Ebene B Berichtswert, falls die vorregistrierte Mindesttradezahl nicht erreicht wird. CMC-Luecke LINK 2022-07-31: kein Signal an diesem Tag, Exits am naechsten Kraken-Tag geprueft.

Reihenfolge: `mtp_val.py`, Look-ahead-Test, BTC-Replikationskontrolle, erst bei bestandenen Kontrollen der einmalige Volllauf.

## 2026-09-17 — Validierungsstufe MTP: Volllauf abgeschlossen, Urteil VERWORFEN

Kontrollen bestanden (Look-ahead 0 Abweichungen BTC und ETH, BTC-Replikation 13/16 Entries, 14/16 Exits, 10/16 Preise). Einmaliger Volllauf `mtp_val.py --tag full`, Bootstrap 2000, 20 Eingabepruefsummen in `mtp_val_results.json`.

Urteil nach Vorregistrierung v0.2 Abschnitt 8 (Ebene B, K1, handelbare Konvention, Sicht 1, Pool ohne BTC): VERWORFEN. B besteht Kriterium 1 (E[R_gesamt] 0.10, PF 2.6) und 7 (73 Trades, geringe Trade-Basis), verfehlt 2 (nur XRP von drei geeigneten Coins positiv), 3 (nur P1 positiv), 4 (Holm-p 0.105), 5 (KEINE), 6 (Retention 0.37). Ebene A (ohne Kosten) besteht 1 bis 4 (E[R_gesamt] 0.70, PF 4.5, Holm-p unter 0.001), verfehlt 5: Sharpe 1.31 gegen exposure-gleiche Passivposition 1.34, Drawdown groesser. Damit auch kein «teilweise».

Kernbefund: Der Ertrag der Mechanik liegt in 2017 bis 2021 (A Block P1 1.37 R, P3 0.08 R) und ist ab 2022 auf allen Coins bei null. Die Ausfuehrung auf Kraken kostet wenig (gepaarte Trades Retention 0.86 ohne einen einzelnen Phantom-Stop von minus 5 R), das B-Fenster liegt in der schwachen Zeit. B2 (Signale auf Kraken) ist ein anderes System (ATR 20 Prozent hoeher, 34 Prozent identische Trades, 0.00 R). Jitter-Nachbarn 0.06 bis 0.20 R in B, keine Spitze, kein Nachbar erreicht die Kriterien, keiner wird weiterverfolgt.

Ergaenzungen im Bericht nach dem Lauf, ohne Aenderung von Kriterien: Abschnitt 11 Zerlegung der Retention, Abschnitt 12 Lesart von Sicht 2 und B2. Eine Umsetzungskorrektur waehrend des Laufs (Sicht 2 Portfolio-Equity statt Sleeve-Mittel, vor der Auswertung behoben, Lauf komplett neu gestartet).

Konsequenzen: Urteil final, kein zweiter Lauf. Strang `03_woo_forward_spot` (Prioritaet 4) wird nicht gestartet. Prioritaeten 2 und 3 unveraendert. Hypothesen in `mtp_val_hypotheses_v1.md`. Dateien in `01_forschung/03_mtp_validation/`.

## 2026-09-17 — Neue Straenge 04_xrp_specialist und 05_dot_specialist eroeffnet, Architektur-Update v1

Zwei coin-spezifische Straenge in der Planphase, kein Rechenlauf, keine Optimierung. Ziel ist die Pruefung, ob XRP und DOT aufgrund ihrer Marktstruktur eine eigene Strategie brauchen, nicht die nachtraegliche Anpassung bestehender Strategien. XRP: drei Kandidaten (A Mean Reversion 4h, B Volatility Breakout, C kontinuierlicher Hybrid nach Efficiency Ratio), drei vorregistrierte Derivate-Filter (Funding-z, Delta-OI), sieben primaere Tests fuer Holm. DOT: Head-to-Head dreier Familien (A Volatility Breakout, B Reversion, C perp-bestaetigter Breakout mit drei vorab gesetzten Schwellen) unter identischen Daten, Kosten, Bloecken und Sizing, sechs primaere Tests, DSR-Sensitivitaet mit 25 plus Jitter Trials wegen der Vorversuche auf DOT. Long und Short getrennt, keine Symmetrieannahme. Plaene `04_xrp_specialist/xrp_strategy_preregistration_plan_v0.1.md` und `05_dot_specialist/dot_strategy_family_plan_v0.1.md`, je neun offene Entscheidungen vor dem Freeze.

Datenstand geprueft: fuer XRP und DOT nur Tagesdaten vorhanden, keine 4h-Kerzen, keine Taker-Volumen, keine Liquidationen. Nachzuladen vor dem Freeze: Binance Spot und Perp 4h und Tageskerzen mit allen Spalten, Kraken 240-Minuten aus dem vorhandenen Archiv. Liquidationen und Orderbuch fail-closed ausgeschlossen. OI-Filter nur ab 2021-12-01, Funding-Filter nur ab 2020.

Vorbelastung offen ausgewiesen: Stufe-2-MR auf XRP schwach, taegliche Trendfolge auf DOT dreimal gescheitert. Konsequenz: keine Variante 2 eines gescheiterten Kandidaten, enge Freiheitsgrade.

Architektur-Update v1 (`00_doku/architecture_update_v1.md`): Crypto-only, Sleeves BTC Trend (nach Validierung: neue Hypothese Exposure-Steuerung noetig, kein Forward-Test der Spezifikation v1), XRP Specialist, DOT Specialist, XS21 Point-in-Time, D-CC Kraken, spaetere CEP-Sleeves. Keine diskreten Regime-Schalter. Portfolio-Layer erst nach zwei bestandenen Sleeves. Reihenfolge: XRP und DOT parallel in der Planphase, dann XS21, D-CC, BTC-Exposure-Hypothese.

## 2026-09-17 — RTC-Framework, Feature Library, Plaene XRP v0.3, DOT v0.3, BTC v0.2, Architektur-Update v2 (Planphase, kein Freeze, kein Lauf)

Vorgaben vom 17.09.2026 (Final Addendum und Asian Price-Action Addendum v2) in die noch nicht eingefrorenen Plaene integriert. Alle Freeze-Urteile der Stufen 1, 2 und der MTP-Validierung bleiben unangetastet.

Methodische Regel (ersetzt «keine Version 2»): Fruehere negative Ergebnisse gelten nur fuer die getestete Kombination aus Marktmechanik, Zeitebene, Signal, Exit und Instrument. Ein negativer Test beendet die Hypothese, nicht den Coin. Verboten bleibt «negativer Test, Parameter aendern, erneut testen». Zulaessig ist «neuer Mechanismus, neue Vorregistrierung, neuer Test» mit ausgewiesener Vorbelastung in der Trial-Zahl. Zwei Stufen fuer alle neuen Familien: Discovery (Daten bis 31.12.2023, wenige feste Varianten, keine Produktionsfreigabe) und Validation (Holdout ab 01.01.2024, Venue-Wechsel Kraken, Kostenstress, Multiplizitaet, allein entscheidend fuer einen Sleeve), Forward-Fenster als dritte Stufe. Vermerk: Das Holdout ist fuer die neuen Mechaniken unberuehrt, aber als Marktverlauf bekannt, Vorkehrung prozedural (abgeschnittene Datenkopie mit Pruefsumme, Freeze vor Holdout-Zugriff).

Neue gemeinsame Komponenten in `01_forschung/00_gemeinsam/`: RTC-Framework v0.1 (Bottom Entry Engine mit Familien CR Candle Reversal und FB Failed Breakdown, Kontext K1 bis K3 zwingend, Trigger T0/TA/TB und spaeter T1h, Ebenen RTC-0 bis RTC-3 inkrementell, Hold Engine Chandelier k 3 nur steigend, Peak Evidence Score mit 13 Komponenten inkl. Kaufklimax und Failed Breakout, Exits E1 und E2, Kontrolle E0 Mean-Reversion-Exit, Multi-Timeframe Tag/4h/1h ohne Schalter, Kerzengrenzen-Diagnose +1h/+2h nie Basis, Cross-Venue-Bericht, Trend Capture Efficiency nur Diagnose, priorisierte Hypothesen H1 Wick mal Volumen, H2 Failed Breakdown, H3 Bestaetigung), Candlestick and Flow Feature Library v0.1 (Geometrie vor Namen, 14 Muster lueckenlos definiert, Flow-Merkmale inkl. taker_imbalance, deterministische Support/Resistance, Sweep-Flags, Informationswert-Test je Coin nur auf Discovery-Fenster), Visual-AI-Plan v0.1 (unabhaengige Second Opinion, drei Arme, Redundanzpruefung, Forward-Pflicht, keine Orderwirkung), Halving-Kontextplan v0.1 (nur Kontextvariable, explorativ, drei Zyklen). Dazu `02_daten/data_upgrade_options_v1.md` (Kraken Time-and-Sales kostenlos als naechste Ebene, CoinGlass fuer Liquidationen erst nach Nachweis des Gewinns der freien Ebenen, Tardis und Amberdata nicht vor Bedarf) und `00_doku/architecture_update_v2.md` (zwei Analysepfade: regelbasiert massgebend, Visual AI getrennt).

Plaene: XRP v0.3 (XRP-RTC primaer, XRP-A wird Kontrolle E0, XRP-C entfaellt, XRP-B auf 4h mit gemeinsamer Breakout-Engine und verschachtelter Bestaetigung), DOT v0.3 (DOT-A 4h Compression Breakout, DOT-C exakt DOT-A plus OI/Taker/Funding verschachtelt, DOT-RTC ersetzt DOT-B), BTC v0.2 (BTC-MTP nur Referenz ohne unberuehrtes Fenster, BTC-B 4h Volatility Expansion, BTC-RTC, Komplementaritaetsanalyse, Halving als Kontext). Trigger-, Exit- und Ebenenwahl fuer die Validation nach vorab fixierten Regeln, keine Auswahl nach CAGR.

Pruefsummen (SHA-256, Planstand, nicht Freeze): rtc_reversal_to_trend_framework_v0.1.md 269667b3df168ec628a53f03bc5a63c737cfd123dedd74fd5e2456fa555216ba, candlestick_flow_feature_library_spec_v0.1.md d5c4cfbd2f2e82ec186da9354997c9ccff6508adcd7a17893b4bf0cfa45cacec, visual_ai_second_opinion_plan_v0.1.md 43ed1d3e9402d7479c2da50e512f733aa223d1a75fa73221975e049ae1d27499, halving_context_research_plan_v0.1.md 828923eda821ce2ad65bc29fe551bd89857feaff909c86eb062c5741efb7ed23, data_upgrade_options_v1.md a712d0d52173578a4165417fdece6f9233bbf3f855bbebad1c5fdf8f48a93018, xrp_strategy_preregistration_plan_v0.3.md 6b0709885928ce4c854b947fb670a727e9da54f1a79fe53d3a44281d8a530a15, dot_strategy_family_plan_v0.3.md 3a4918040cdef74b824633d827bc70ecc356317889f80f12d01ad6acfa5831ac, btc_specialist_research_plan_v0.2.md e0690222738d5905b0c4f3564fb798eaf17b9e6a9a4aa7a484f3fe58afff37ac, architecture_update_v2.md c81f6d1bda015078892baac1bf8d7666f0b8ad78c1166a4e94df6f22c4d6e944.

Daten: Loader `02_daten/nachladen_4h.py` und `Daten-nachladen-4h.command` (SHA 58f17e7b…) laden Binance Spot und Perp 4h und 1d mit allen Spalten, Kraken 240 aus dem Archiv, Kraken API 240 (Lauf am 17.09.2026 durch den Auftraggeber gestartet). Danach nachzuladen: Binance 1h Spot und Perp, Kraken 60, Binance-Metrics-Aggregation zu 4h-OI, OKX-Kerzen, Kraken Time-and-Sales. DOGE als elfter Coin vorgesehen, nicht geladen, Entscheid offen.

Offen vor dem Freeze: Entscheidungen in Framework (14), Feature Library (9), XRP (9), DOT (9), BTC (5), Visual AI (5), Halving (3). Kein Rechenlauf, kein Freeze.

## 2026-09-17 — 4h-Daten geladen, 1h-Loader bereitgestellt, BTC YAMATO RTC (Japan-only) als vierte BTC-Hypothese (Planphase)

Datenlauf `Daten-nachladen-4h.command` abgeschlossen (14:30 bis 15:06 UTC): Binance Spot und Perp 1d und 4h mit allen Spalten fuer zehn Coins, Kraken 240 aus dem Archiv 2026Q2 plus API bis 17.09.2026 mit Naht ohne Luecke. Gegenproben: Vollspalten-Tageskerzen gegen OHLCV 0 Abweichungen auf allen Reihen. 4h auf Tag aggregiert: Spot 0 Abweichungen, Perp je Coin 1 bis 3 Abweichungen, alle am 2023-08-16 (Binance-seitige Inkonsistenz der Perp-Tagesdatei, auf allen zehn Coins gleich) plus BTC 2023-11-10 und XRP 2020-01-16/17. Bekannte Luecken: Spot 4h bis 7 Kerzen (Binance-Wartungen 2018 bis 2019), Perp 4h 18 Kerzen 2022-02-25 bis 03-01 und 12 Kerzen 2022-03-31 bis 04-03 bei SOL, XRP, LTC (Binance-Vision-Luecken), Kraken 240 Fruehphase BTC 579, LTC 1028, ETH 209 Luecken (B-Start-Regel), BNB Kraken erst ab 2025-04. Herkunft und Pruefsummen in `02_daten/raw/provenance_4h.json`. Abdeckungstabelle je Merkmal folgt vor dem Freeze.

1h-Loader `nachladen_1h.py` (SHA 39411c0e…) und `Daten-nachladen-1h.command` (ad627e83…) bereitgestellt: Binance Spot und Perp 1h alle Spalten, Kraken 60 aus dem Archiv, Kraken API 60 (720 Kerzen), Gegenprobe 1h auf 4h. Bekannte Luecke bei Kraken 1h zwischen Archivende 30.06.2026 und API-Beginn, schliesst das Archiv 2026Q3.

BTC YAMATO RTC: neue, eigenstaendige BTC-Hypothese (Japanese Bottom Confirmation, Trend Capture, Peak Confirmation) mit der Quellenregel, dass Hypothesenbildung ausschliesslich aus `.jp`-Quellen stammt. Fuenf Dokumente in `01_forschung/06_btc_specialist/`: Forschungsplan v0.1 (f935334acc7f0d333138c91c2059c55e02cfe9c6b8347be8dfa7fbefea0a3f3e), Japanese Price-Action Features v0.1 (0ea41d0a13cb71cb13c64ee39d0f68f50683f402a4620dfbd18ab6ae7f0616f5), Previous-Open-Levels-Spezifikation v0.1 (6f91db6099afc76b4bdd3020f04b6e538e30df2401c36e5efdf56623bc515544), Sakata-Bottom-Peak-Spezifikation v0.1 (2e052ab076b5ce23ae9acfb071f904facafad46c33dc682304e1820964fa745e), Ichimoku-Inkrement-Plan v0.1 (4a6a7da0cf8512306efa98e6018f800d9e5ef6170e2e7ec292608f94241a5fec). Kern: Kandidat ist nicht Einstieg (Sakata: Boden bestaetigen, dann kaufen), fuenf algorithmische Bottom-Muster inkl. Double/Triple-Bottom mit Nackenlinie und Failed Breakdown, Trigger TA Baseline mit TB und TC (Previous-Open-Reclaim) als Tests, struktureller Hold mit Peak-dann-Higher-Low-Bruch als Exit (E-Y) gegen Chandelier (E1), MACD-Divergenz und Ichimoku (9/26/52, klassisch) nur als Inkremente mit Ersatzregeln gleicher Verzoegerung zur Redundanzkontrolle, sieben Tests in einer Holm-Familie, Discovery bis 2023-12, Holdout ab 2024. YAMATO ist Geschwister von BTC-RTC, beide vorregistriert, keine Auswahl nach Ergebnis, gegenseitige Zaehlung in der Trial-Zahl. Planstand, kein Freeze, kein Lauf.

## 2026-09-17 — YAMATO Forschungsplan v0.2: zweistufige Discovery (Planstand, kein Freeze)

Nach Pruefung des Plans v0.1 fokussiert: Stufe A mit drei primaeren Bottom-Hypothesen (Y1 Failed Breakdown / Swing-Low-Reclaim mit TA, Y2 Double Bottom mit Nackenlinienbruch als einziger Bestaetigung, Y3 Lower-Wick plus Volume Climax mit TA), identischer Kontext, Stop, Sizing und einheitlicher Exit-Baseline E-U (Chandelier 3 ATR14 als harter Boden plus Schluss unter dem letzten bestaetigten Higher Low), keine Peak-Logik in Stufe A. Harami, Morning Star, Engulfing, Hikkake nur deskriptiv. Zeit- und selloff-gematchte Kontrollgruppe (bis drei Kontrollen je Signal, ±90 Tage, dd120 ±3 Punkte, ext ±0.5 ATR, gleicher Trigger, Stop und Exit), Test als gepaarte Differenz Signal gegen Kontrolle, Holm ueber drei. Stufe B getrennt: Previous Open, Kijun, MACD-Divergenz, Halving je gegen Ersatzregel oder Kontrolle, ohne Wirkung auf Einstiege in Stufe A. Peak Engine als eigener Inkrement-Test gegen E-U. Diskriminierende Metriken je Signal (Abstand zum ex-post Tief, MFE, MAE, neuer Trend in 7/14/30/60 Tagen, Capture Ratio, Klassifikation Rebound/Trend/Fehlsignal), nur Diagnose. YAMATO gegen BTC-RTC dreigeteilt (nur YAMATO, nur RTC, beide). Erwartete Kandidatenzahl aus Ueberlegung, nicht aus Daten: 60 bis 120 Kandidaten, 45 bis 85 Signale, Y2 voraussichtlich unter 30. Datei `01_forschung/06_btc_specialist/btc_yamato_rtc_research_plan_v0.2.md`, SHA-256 ea6b4221c70ab56a000d25e82b2c278b482e1a95a9073e94b4799b73c09276fc. Freeze-Entscheid steht aus.

## 2026-09-17 — FREEZE BTC YAMATO RTC Stufe A, Umsetzung, Tests, Zaehlung, HALT vor Ergebnisberechnung

Freeze bestaetigt durch den Auftraggeber. Eingefroren: `btc_yamato_rtc_research_plan_v1.0.md` SHA-256 56069bc009f697bbed985a1f80540f203268db2ba88964bcca9b558d3ba79003 und das Stufe-A-Parameterpaket `yamato_stufeA_freeze_v1.0.md` SHA-256 98376c2d79f94dae26798778cc9d29d0f185f691618bc32fff24e60ef7fb5f4c (Kontext 12 Prozent, 2 ATR in 6 Kerzen, 1 ATR zum Niveau, Swing 3/3, Fenster 120 und 240, Zonen-Toleranz 0.5 ATR mit drei Beruehrungen, Failed-Breakdown-Schwellen, Double-Bottom-Zahlen, Y3 Volumen-z 1.5 mit Jitter 1.0/2.0 ohne Ersatzwirkung, TA Ein-Kerzen-Regel, Stop-Puffer 0.5 ATR mit Abbruch 3 ATR, k 3, E-U Chandelier plus Strukturbruch, Kontrollgruppe 3/±90 Tage/±3 Punkte/±0.5 ATR mit TA, Mindestzahl 30/20, Klassifikation strukturbezogen, Discovery-Schnitt 2023-12-31). Quellen mit SHA: Sakata-Spez. 2e052ab0…, Library d5c4cfbd…, Framework 269667b3…. Keine Aenderung dieser Werte vor oder nach Sicht auf Ergebnisse. Vorgemerkt: volatilitaetsnormierte Kontextdefinition spaeter nur als vorregistrierte Robustheitsdiagnose, nie als Ersatz der Baseline.

Danach ausgefuehrt, ohne Performance-Auswertung: (1) Datenvalidierung Binance BTCUSDT 4h (SHA f8d0e58d…, 9 Luecken mit 17 Kerzen bis 2020-02, sonst ohne Befund), Discovery-Kopie bis 2023-12-31 20:00 UTC mit 13950 Kerzen, SHA 2d394fd1cbc344d5e012e12b40bc5835fef0fbe72f0678c2abf417babd96a7e6. (2) Umsetzungsentscheide U1 bis U20 vor der ersten Zaehlung (`yamato_stufeA_umsetzungsentscheide_v1.md`, SHA 72a041b0…), darunter U7 Kontext fuer Y2 auf s2, U8 Zeitordnung der Double-Bottom-Kandidaten, U13 Strukturbruch-Exit, U15 Kontrollgruppe. (3) Library `stufeA/ylib.py` (SHA 3610b303…), 8 Unit-Tests bestanden, Look-ahead-Test bestanden (Abschneidetest 2022-06-30 bitgleich bis Schnitt minus 4, Permutationstest 25/25; ein Reihenfolgefehler in der Y2-Eindeutigkeit wurde durch den Permutationstest gefunden und vor jeder Zaehlung behoben). (4) Zaehlung: Kontext auf 1842 Kerzen, Y1 96 Kandidaten (23 mit TA, 16 gehandelte Signale), Y2 14 Kandidaten (0 Signale), Y3 29 Kandidaten (10 mit TA, 6 Signale). (5) Kontrollpool 1666 Kerzen, Matching Y1 11/4/1 Signale mit 3/1/0 Kontrollen, Y3 1/3/2. Bericht `yamato_stufeA_datenpruefung_zaehlung_v1.md` (SHA 5222369b…), Kandidatenlisten mit SHA c3bce1b9… und e6c2726a….

HALT vor jeder Ergebnisberechnung, zwei strukturelle Befunde aus Zaehlungen, kein Outcome berechnet oder gelesen: Befund 1: Y2 ist unter den eingefrorenen Regeln nicht handelbar, weil Nackenlinie (mindestens 2 ATR ueber dem Tief) plus Stop-Puffer (0.5 ATR) die Abbruchgrenze (3 ATR) bei allen 14 Kandidaten ueberschreiten (3.1 bis 7.3 ATR). Innerer Widerspruch der Spezifikation. Befund 2: Alle drei Hypothesen liegen unter der Mindestzahl (Y1 16, Y3 6, Y2 0 Signale), Ursache ist die TA-Bestaetigungsquote von 24 Prozent (Schaetzung im Plan v0.2 war 50 bis 60 Prozent, falsch) und die 3-ATR-Grenze. Stufe A waere in dieser Form vollstaendig deskriptiv. Entscheidung des Auftraggebers ausstehend, bis dahin keine Ergebnisberechnung.

## 2026-09-17 — YAMATO Stufe A Version 1.1: Behebung des Y2-Spezifikationsdefekts, Audit-Trail, erneute Kontrollen

Entscheid des Auftraggebers: Weg 2, ausschliesslich eng begrenzt auf den strukturellen Y2-Spezifikationsfehler. Audit-Trail: Version 1.0 (SHA 56069bc0…, Parameterpaket 98376c2d…) wurde vor jeder Outcome-Auswertung eingefroren. Zum Zeitpunkt der Aenderung bekannt waren ausschliesslich Kandidatenzahlen, Bestaetigungs- und Statusquoten und Entry-Stop-Distanzen. Keine P&L-, MFE-, R-, Gewinn-/Verlust-, Capture- oder sonstigen Outcome-Werte wurden gelesen (Simulationsausgaben liegen ungelesen in `stufeA/_private/`). Der Defekt wurde allein aus der logischen Beziehung der eingefrorenen Regeln (Nackenlinie mindestens 2 ATR ueber den Tiefs, Stop 0.5 ATR unter dem zweiten Tief, Abbruch ueber 3 ATR) und den Entry-Stop-Distanzen (3.1 bis 7.3 ATR bei allen 14 Kandidaten) erkannt. Version 1.1 veraendert ausschliesslich die fuer Y2 logisch inkompatible 3-ATR-Eligibility-Grenze: Fuer Y2 entfaellt sie, Stop bleibt zweites Tief minus 0.5 ATR, Einstieg nach Nackenlinien-Schluss zur naechsten Eroeffnung, Sizing risikobasiert mit konstantem nominellem Risiko und ohne Mindestposition, reale Stopdistanz je Trade berichtet. Ein Stop unter der Bruchkerze ist keine Reparatur, sondern eine neue Risikohypothese, nur spaeter als separat vorregistrierte Y2-Execution-Sensitivity. Y1 und Y3 unveraendert (16 und 6 Signale, TA nicht gelockert, kein laengeres Bestaetigungsfenster, keine Filter- oder Mindestzahlaenderung), Auswertung nach eingefrorenen Regeln nur deskriptiv. Ergebnisstatus je Hypothese: supported, not supported, inconclusive (insufficient sample), ohne Kriterienaenderung (Plan Abschnitt 11a). Die TA-Quote von 24 Prozent ist Forschungsbefund und begruendet die Stufe-B-Frage H3, keine Reparatur von Stufe A.

Neue Pruefsummen: `btc_yamato_rtc_research_plan_v1.1.md` aa8195cee9f0e60b53fa22db86dc8621d52f0c1b232d36fec7ba62395f8f9a2d, `yamato_stufeA_freeze_v1.1.md` 7c4be2f80a7af092260de3bf123954a1625935c33cb4a1341576a08e2039c431, `stufeA/ylib.py` 81a74f2a38733f707dcde5ff054b7edf1d450b68e956096c029bb04bf8646f55 (eine Zeile: Y2 ohne stop_too_wide, dazu stop_dist_atr je Trade), `stufeA/tests/test_ylib.py` abdd60c7… (neuer Test test_y2_no_cap_v11), `stufeA/count_stufeA.py` 0f01337b…, Umsetzungsentscheide mit Nachtrag U21 257a7f06…, Bericht f4ee14d3….

Erneute Kontrollen bestanden: 9 Unit-Tests, Look-ahead (Abschneidetest bitgleich, Permutation 25/25), Kandidatenlisten unveraendert. Y2: 14 von 14 Kandidaten handelbar, Entry-Stop-Distanz Median 4.75 ATR (3.11 bis 7.31), keine andere Regel schliesst aus. U21 (vor Outcomes): Referenzkerze des Y2-Matchings ist das zweite Tief s2 (analog U7), weil die Bruchkerze keine Selloff-Merkmale traegt und 10 von 14 Signalen sonst ohne Kontrolle blieben, Toleranzen unveraendert. Abdeckung: Y1 11/4/1 Signale mit 3/1/0 Kontrollen, Y2 8/3/2/1 mit 3/2/1/0, Y3 1/3/2 mit 3/1/0. Der einmalige Stufe-A-Outcome-Lauf wartet auf Freigabe, keine Outcomes berechnet oder gelesen.

## 2026-09-17 — Accelerated Research Mode: YAMATO Stufe A Outcome-Lauf, Ergebnis, Lanes, Roadmap

Vorgabe des Auftraggebers: drei parallele Lanes (A Reversal-to-Trend, B Trend/Breakout, C Derivatives/Relative Value), drei Discovery-Ebenen (formal supported, mechanistically promising, no evidence), Fast Fail und Fast Promote, coin-spezifische Auswertung ohne Pooling, Produktion frueh mitdenken. Auswertungsregeln v1 (`yamato_stufeA_auswertungsregeln_v1.md`, SHA aa453a1b…) vor dem Lauf geschrieben: MP-Bedingungen (a) gepaarte R-Differenz > 0 mit Bootstrap-Anteil >= 0.80, (b) MFE-Median ueber Kontrollen und Capture-Differenz > 0, (c) gleiche Richtung in beiden Bloecken, (d) Konzentration <= 40 Prozent, (e) netto K1 > 0; Fast Fail und Fast Promote operationalisiert.

YAMATO Stufe A, einmaliger Outcome-Lauf (Plan v1.1, Library 81a74f2a…, `eval_stufeA.py` 60efb294…, Ergebnis `eval_stufeA.json` cd0135fe…, Seed 20260917): Y1 Failed Breakdown 16 Signale, netto K1 −0.23 R, Trefferquote 19 Prozent, gepaart gegen gematchte Kontrollen −0.34 R (2 Prozent positive Ziehungen), Status NOT SUPPORTED (Fast Fail). Y2 Double Bottom 14 Signale, netto −0.30 R, ein Gewinner, gepaart +0.75 R (100 Prozent positiv, beide Bloecke), MP-Bedingungen a, b, c erfuellt, d (85 Prozent Konzentration) und e (netto negativ) verfehlt, Status INCONCLUSIVE; 50 Prozent der Y2-Signale erreichen innerhalb 60 Tagen ein neues 20-Tage-Hoch (Kontrollen 1 von 7), Einstieg im Median 5 ATR ueber dem Tief, Chandelier-Exit nach 15 Kerzen. Y3 6 Signale, 1 Kontrollpaar, INCONCLUSIVE. Praezisierung nach dem Lauf, ausgewiesen: Statuszuweisung ausser inconclusive nur mit mindestens 5 Paaren (Y3 waere sonst technisch Fast Fail gewesen), aendert Y1 und Y2 nicht. Basisrate aller Kontrollgruppen negativ (−0.30 bis −1.05 R). Kein Sleeve, keine Validation. Bericht `yamato_stufeA_bericht_v1.md` (SHA 5b2b3684…).

Lehren, in neue Vorregistrierungen uebernommen, ohne Aenderung der eingefrorenen BTC-Regeln: TA kostet drei Viertel der Kandidaten ohne Qualitaetsgewinn gegenueber Kontext-Kontrollen (Stufe B Trigger-Familie T0/TA/TB, `btc_yamato_stufeB_preregistration_v0.1.md` 8b069764…), Chandelier 3 ATR14 auf 4h beendet Positionen nach 12 bis 15 Kerzen (Stufe B Exit-Familie E-U/E-D/E-W), Kontrollgruppe als Teil jedes primaeren Tests. XRP v0.4 (b8497a56…) und DOT v0.4 (46efcc97…): Stufe-A-Struktur mit T0 primaer, E-U und E-D, gematchte Kontrollen, Statusebenen, Produktionsvermerk, je fuenf offene Entscheidungen vor dem Freeze.

Gemeinsame Derivatives- und Flow-Library v0.1 umgesetzt (`00_gemeinsam/dlib/dlib.py` 2eb071b9…, Bericht f4b9c9ce…): 16 Merkmale coin-uebergreifend identisch fuer BTC, XRP, DOT, ETH, SOL auf 4h, Abdeckungstabelle, Funding-Settlement-Zuordnung konservativ (Rate gilt ab der Kerze nach dem Settlement), OI ab 2021-12 fail-closed, Look-ahead-Test bestanden (Abweichung 5e-13). Visual AI technisch vorbereitet (`00_gemeinsam/vaprep/va_render.py` 83e53f74…, Manifest mit eingefrorenem Prompt v0.1, synthetischer Chart geprueft: keine Datumsachse, Prozentskala, kein Name). ETH- und SOL-Skizzen v0.1 (f825daea…), Lane-D-Notiz Options Gamma v0.1 (af588803…, vorgemerkt). 1h-Nachtrag abgeschlossen, alle zehn Spot-1h-Reihen vorhanden, 43 Kerzen je Coin quarantaeniert (09. bis 11.02.2018).

Roadmap `00_doku/AURUM_ACCELERATED_ROADMAP_v1.md` (SHA a9805d15…): Sleeve-Tabelle mit Status, naechstem Lauf, Datenbedarf, erwarteten Trades, Validation- und Production-Status, Vierwochenplan. Naechster Schritt: Entscheidungen zu XRP v0.4, DOT v0.4 und Stufe B v0.1, dann Freeze und drei Discovery-Laeufe.

## 2026-09-17 (Abend) — Governance v1, Evidenzklassen, Holdout-Trennung, Lane C, Roadmap v1.1

Entscheid (Nutzer): Vor den naechsten Outcome-Laeufen fuenf Governance-Punkte, keine Aenderung eingefrorener Ergebnisse. Umgesetzt in `00_doku/aurum_governance_evidence_v1.md` (SHA d995baf0…):

1. BTC ist Development-Markt. BTC Stufe B kann Trigger- und Exit-Familie nicht unabhaengig bestaetigen, hoechste Folge ist ein Validation-Lauf auf dem BTC-Holdout. XRP-RTC und DOT-RTC sind die ersten unabhaengigen Generalisierungstests, Bedingung: Freeze v1.0 vor ihren Outcomes, keine coin-spezifische Anpassung des Parameterpakets v1.1.
2. Outcome-informed Varianten (Y2 mit E-D/E-W, Y3 mit T0, Y1 mit T0/TB, Trigger- und Exit-Familie auf BTC) tragen dauerhaft den Vermerk Ebene C. Positives Ergebnis auf denselben BTC-Discovery-Daten rechtfertigt hoechstens einen Validation-Lauf, keinen Sleeve, keine Produktion, keinen Cross-Coin-Test.
3. «Mechanistically promising» Regel v2, ex ante fuer alle Laeufe ab heute: mindestens drei von vier Kriterien (Median gepaartes ΔR in erwarteter Richtung mit Anteil positiver Paare ≥ 0.60, relevante Verschiebung MFE ≥ 0.5 R oder Capture ≥ 0.10 oder Klassenanteil trend plus delayed_trend ≥ 15 Punkte, groesster Einzelbeitrag ≤ 40 Prozent und Vorzeichen ohne bestes Paar erhalten, gleiche Richtung in mindestens zwei Bloecken mit je ≥ 5 Paaren). Mindestens 5 Paare, Fast Fail und Fast Promote unveraendert, Validation bei MP v2 nur mit ≥ 20 Trades. Keine rueckwirkende Aenderung dieser Regel. Stufe A behaelt Status nach v1, keine Neubewertung, auch nicht als Bericht.
4. Holdouts physisch getrennt: `02_daten/holdout/discovery/<SYM>_<reihe>_discovery.csv` (letzte Kerze 2023-12-31 20:00 UTC) und `validation/<SYM>_<reihe>_validation.csv` (ab 2024-01-01 00:00 UTC) fuer BTC, XRP, DOT, ETH, SOL, je Spot 4h, Perp 4h, Flow 4h (15 Paare, 30 Dateien). Manifest `holdout_manifest_v1.json` (SHA b54dfb0f…) mit Prueffsummen von Quelle, Discovery und Validation. BTC-Spot-Discovery byteidentisch mit der eingefrorenen Stufe-A-Datei (2d394fd1…). Loader-Sperre: `ylib.load` (ylib.py neu SHA 7f0230c9…) und `dlib._load` (dlib.py neu SHA 5e1fd5c2…) verweigern Dateinamen mit «validation» ohne `AURUM_VALIDATION=1`, geprueft (PermissionError ohne, 5940 Zeilen mit Freigabe), Tests 9 von 9 unveraendert bestanden. Aenderung an ylib.py betrifft nur das Laden, keine Regel, kein Stufe-A-Ergebnis.
5. Lane C beschleunigt: Loader `02_daten/nachladen_lane_c.py` (SHA a400d974…) mit Launcher `Daten-Lane-C.command` (SHA 3031f0bc…), Kraken-Futures-Endpunkt historical-funding-rates fuer PF- und PI-Symbole, Binance-Vision-S3-Listing fuer das UM-Universum einschliesslich delisteter Symbole. Beschaffungsvergleich `02_daten/lane_c_data_procurement_v1.md` (SHA 1f553380…): Empfehlung kostenloser Endpunkt zuerst, bei zu geringer Tiefe ein Monat CoinGlass Startup (79 USD) mit Pflichtabgleich, Tardis (8400 bis 36000 USD je Jahr) nicht vor einer bestandenen Validation, XS21-Universum aus S3-Listing mit Vormonats-Dollar-Volumen, keine Marktkapitalisierungsdaten. Lane C parallel zu XRP und DOT.

Evidenzklassen (Development, Independent discovery, Holdout validation, Forward validation, Production eligible) definiert, Feld in jeder Roadmap-Zeile. Visual AI bleibt eingefroren vorbereitet, ohne eigene Woche. Roadmap `00_doku/AURUM_ACCELERATED_ROADMAP_v1.1.md` (SHA 86a392de…) ersetzt v1, v1 bleibt als Datei erhalten.

Naechster Schritt: Lane-C-Loader auf dem Mac, dann Entscheidungen zu XRP v0.4, DOT v0.4, Stufe B v0.1, Freeze, Zaehlung, drei Discovery-Laeufe mit Regel v2.

## 2026-09-17 (spaet) — Entscheide zur XRP/DOT-Parameterpruefung, dlib v0.2, Lane-C-Befund, Konnektoren

Parameterpruefung `01_forschung/00_gemeinsam/xrp_dot_parameter_audit_v1.md` (SHA 720e16e6…): 31 von rund 40 Zahlen des BTC-Pakets v1.1 sind ATR-normiert, z-standardisiert oder Zeitkonvention und damit coinunabhaengig. Vier absolute Prozentwerte sind es nicht: K1 (12 Prozent entspricht 6.4 ATR auf BTC, 3.9 auf DOT, trifft 35 Prozent der BTC-Kerzen, aber 56 Prozent XRP und 53 Prozent DOT), Niveau-Penetration 0.1 Prozent, at_low_structure 2 Prozent, Matching-Toleranz dd120 3 Punkte.

Entscheide (Nutzer, vor jedem XRP- oder DOT-Outcome):
1. K1 fuer XRP, DOT, spaeter ETH und SOL in ATR-Form: dd120_atr = (C_t − max(H, t−120..t−1)) / ATR14_{t−1}, K1 bei dd120_atr ≤ −6.0. Konstante 6 eingefroren, nicht coin-spezifisch optimierbar. BTC Stufe A behaelt 12 Prozent. Matching-Toleranz ±1.5 ATR-Einheiten. Kontextquote je Coin nur als Coverage-Diagnose, nicht zur Anpassung der 6.0. Feste 12-Prozent-Regel nur als diagnostische Vergleichsvariante, keine alternative Baseline.
2. Penetration 0.05 ATR14_{t−1}, at_low_structure = Tief + 1.0 ATR14_{t−1}, Toleranz ein Viertel der K1-Schwelle, alle in ATR-Form.
3. Open-Interest-Inkrement als z-Score: dOI_5d = OI_t / OI_{t−5 Kalendertage} − 1 auf der Tagesreihe, z-Score ueber festes 60-Tage-Rollingfenster nur aus Vergangenheit, Schwelle +1.0 (Expansion) und −1.0 (Kontraktion), identisch fuer alle Coins, fail-closed vor 2021-12 und bei Luecken, keine Rueckrechnung. Bisherige ±10-Prozent-Regel nur als diagnostische Vergleichskonvention. Umgesetzt in dlib v0.2 (`dlib.py` SHA 4e042804…, Feature `delta_oi_zscore`), Look-ahead-Test bestanden (Stoerung nach Cut: 0.0 Abweichung davor, 100 Prozent Aenderung danach), Anteil |z| ≥ 1 auf 28 bis 31 Prozent je Coin. Flow-Discovery- und Validation-Dateien neu erzeugt, Manifest `holdout_manifest_v1.1.json` (SHA e2e764b4…), Spot- und Perp-Dateien unveraendert.
4. Alle Empfehlungen aus XRP v0.4 Abschnitt 8 und DOT v0.4 Abschnitt 5 bestaetigt: T0 primaer, E-D zweite Exit-Baseline, Kontrolltoleranzen wie BTC in ATR-Form, DOT-C-Schwellen Taker 0.10 und Funding-z 1.5 (OI neu als z-Score 1.0), Blockregel DOT P2-Haelften, Trial-Zahl 16 (XRP) und 15 (DOT).

Reihenfolge (Nutzer): XRP v1.0 und DOT v1.0 Freeze vor Stufe B. Discovery-Laeufe XRP → DOT → BTC Stufe B. Nach jedem Lauf sofort Bericht, Status nach Governance v2, Prueffsummen, ENTSCHEIDE, bevor der naechste startet. Keine Regelaenderung zwischen den Laeufen. BTC Stufe B bleibt Development, Deckel Validation. Nach den drei Laeufen eine Vergleichstabelle (Mechanik, Coin, Evidence class, Status, Trades, Effekt gegen Kontrolle, MFE/Capture, Konzentration, Zeitstabilitaet, Execution-Komplexitaet, Empfehlung Fast Fail / Validation Candidate / Further Discovery).

Lane C, Befund `02_daten/lane_c_datenbefund_v1.md`: Kraken-Futures-Endpunkt ist ein rollendes Ein-Jahres-Fenster (2025-09-17 bis heute, Stundenraster, 14 aktive Symbole, PI_BCHUSD tot), keine Historie davor, auch nicht ueber CCXT. Weg K2 (CoinGlass, ein Monat) bleibt fuer D-CC noetig, Loader monatlich laufen lassen. Binance-UM-Universum: 1014 Symbole ab 2020-01, 266 heute nicht TRADING, am Stichtag Ende 2023 waren 298 handelbar, davon 120 heute nicht mehr (40 Prozent), 81 bis Ende 2023 delistet und in Stufe 2 nicht enthalten. XS21-Point-in-Time-Universum kostenlos vollstaendig. Loader v1.1 (SHA 17c8f2fc…): URL-Kodierung, Nicht-ASCII-Symbole uebersprungen (4), Teilstand alle 50 Symbole. Erster Lauf war nach 1000 Symbolen an einem Nicht-ASCII-Namen abgebrochen.

Konnektoren geprueft (nur lesend): CCXT-MCP liefert Kraken Spot und Kraken Futures (Ticker, OHLCV mit Paging ueber since), Kraken-MCP liefert Market-Daten und einen Paper-Workspace `aurum-ii` (10000 USD, Gebuehr 0.26 Prozent, Slippage 0, unberuehrt) sowie einen Lab-Layer mit versiegelter Vorregistrierung. Vermerk: Paper-Gebuehr und Slippage liegen unter K1, vor einer Nutzung als Forward-Fenster auf K1-Annahmen zu setzen (Reset nur mit Freigabe). CCXT-Paging ist ein Ersatz fuer den Kraken-Archiv-plus-REST-Weg mit der 1h-Nahtluecke.

## 2026-09-18 00:05 UTC — CROSS-COIN FREEZE: XRP v1.0 und DOT v1.0 (Regression PASS, outcome-blinde Zaehlung, Freeze vor Outcomes)

Schritt 1, Regressionstest rlib v1.0 (SHA f1ffdbb81cad3115…) gegen BTC Stufe A: REGRESSION PASS, 205 von 205 Pruefungen auf Ereignisebene (Kandidaten, Zeitstempel, Strukturen, Niveaus, Einstiegskerze und -preis, Stop, Exitkerze und -preis, Exitgrund, r_net, r_gross, MFE, MAE, Kontrollen, Paare, K0/K1/K2-Aggregate), einzige Toleranz 1e-9 fuer Gleitkomma (CSV-Roundtrip), beobachtet maximal 7.3e-12. Bericht `01_forschung/00_gemeinsam/rlib/regressionstest_rlib_v1.0_gegen_stufeA.md` (SHA 938bb24f92794352…), Ergebnisdatei `regress/regress_btc_result.json` (SHA cbff3fcb4c55238e…). Technische Provenance: Lauf 1 meldete einen FAIL auf `y1_levels`, Ursache war der Vergleich (NaN gegen leeren Text), nicht die Library, 0 von 13816 Zeilen verschieden nach Normalisierung, Vergleichsfunktion korrigiert, vollstaendiger Lauf 2 als Evidenz, Lauf-1-Protokoll aufbewahrt. Ein noch frueherer Startversuch und die erste XRP-Zaehlung wurden durch Neustarts der Rechenumgebung ohne Ausgabe abgebrochen und wiederholt. Unit- und Look-ahead-Tests der neuen Modi 7 von 7 bestanden. Keine Referenzdatei veraendert.

Schritt 2, Spezifikationen: `01_forschung/04_xrp_specialist/xrp_rtc_stufeA_spec_v1.0.md` (SHA 27fa0bd174b86a1f…) und `01_forschung/05_dot_specialist/dot_rtc_stufeA_spec_v1.0.md` (SHA 172229d3f40e2cb4…), je 16 Abschnitte: Daten und Zeitraum, Normierung, Kontext (K1 ATR-Form −6.0), Struktur, Kandidaten, Trigger (T0 primaer, TA, TB), Stop und Exits (E-U, E-D, E0), Fill-Regeln, Kosten, Ausschluesse, Matching-Definition, Zaehlweise, Abgleich mit BTC (vier Zahlen in ATR-Form, sonst identisch), Tests und Multiplizitaet, Evidenzklasse, Zaehlbefund. Breakout-Familien (XRP-B, DOT-A, DOT-C) sind nicht Teil dieses Freeze, sie folgen mit BTC-B in einem eigenen Freeze (Roadmap v1.1 Woche 3).

Schritt 3, outcome-blinde Zaehlung (`count_cross.py` SHA 17d7cb93e080e19c…, Ergebnisse `count/count_XRP.json` 2735c13014011b43…, `count/count_DOT.json` 2147bfb4630b434b…): keine Exits, keine Post-Entry-Renditen, keine MFE/MAE, keine Stop- oder Zieltreffer berechnet. Positionsausschluss nicht anwendbar ohne Exits, Matchzahlen sind Obergrenzen.
XRP: 12397 Kerzen, 12263 auswertbar, 7 Luecken (9 Kerzen). Kandidaten X1 92, X2 17, X3 29. Einstiege T0: X1 90, X3 24, X2 Nackenlinie 17. Matches (mindestens eine Kontrolle): X1 79 von 92, X2 17 von 17, X3 21 von 29. Ausschluesse: X1 2 Stop ueber 3 ATR, X3 5, X1 13 ohne Kontrolle, X3 8 ohne Kontrolle. K1-Coverage 56.4 Prozent (12-Prozent-Form 56.1).
DOT: 7381 Kerzen, 7247 auswertbar, keine Luecken. Kandidaten D1 75, D2 15, D3 17. Einstiege T0: D1 75, D3 17, D2 15. Matches: D1 73 von 75, D2 13 von 15, D3 17 von 17. Ausschluesse: keine Stop-Grenze bei T0, D1 2 und D2 2 ohne Kontrolle. K1-Coverage 48.0 Prozent (12-Prozent-Form 53.8).
Mechanische Auffaelligkeiten: RTC-1-Teilmenge nahezu leer auf beiden Coins (XRP 2/0/1, DOT 0/1/2), TA trifft auf X3 und D3 fast nie (2 von 29, 1 von 17), X2/D2-Stopdistanzen Median rund 4 ATR (v1.1 ohne Grenze). Coverage-Werte der Parameterpruefung waren eine Naeherung ((C/H−1)/(ATR/C)), die eingefrorene Formel (C−H)/ATR liefert hoehere Anteile, Konstante 6.0 unveraendert.

Schritt 4, Freeze: Beide Spezifikationen mit obigen Prueffsummen eingefroren. Datenstaende: Manifest v1.1 (e2e764b4…), Spot-Discovery XRP 6fda0931…, DOT 426b5ae7…, Flow XRP 425b430b…, DOT c20fdabf…, dlib v0.2 4e042804…, ylib 7f0230c9…, rlib f1ffdbb81cad3115…. Ausdrueckliche Erklaerung: Bis zu diesem Freeze wurden keine XRP- oder DOT-Outcomes, Post-Entry-Renditen, MFE/MAE, Stop- oder Zieltreffer oder sonstige Performanceinformationen berechnet oder angesehen. Keine bereits eingefrorene Zahl, Regel oder Datei wurde veraendert.

STOP-GATE: Keine Outcome-Laeufe gestartet, keine Varianten, keine Lane-C-Features, kein XS21, kein CoinGlass, kein Kraken-Paper- oder Lab-Test. Naechster Schritt nur auf Freigabe: Discovery-Lauf XRP, dann DOT, dann BTC Stufe B, je mit Bericht, Status nach Regel v2, Prueffsummen und ENTSCHEIDE vor dem naechsten.

## 2026-09-18 00:45 UTC — XRP v1.0 Outcome-Lauf abgeschlossen (Independent discovery)

Freigabe (Nutzer): Freeze bestaetigt, einmaliger Outcome-Lauf XRP dann DOT, keine Aenderung an K1, T0, TA, Stoplogik, Matching, Mindestzahlen, Inkrementen. Outcome-blinde Befunde (RTC-1 nahezu leer, TA auf X3 wirkungslos, K1-Coverage 56.4 Prozent) nur als Hinweise, keine Regelaenderung.

Lauf: `eval_cross.py` (SHA 3975f2b2872c8d0a…), Seed 20260918, Bootstrap 2000, Kandidaten aus der eingefrorenen Zaehlung (Prueffsummen im Skript verifiziert), Ergebnis `04_xrp_specialist/eval/eval_XRP.json` (SHA fdaa2ad4f99297f2…), Bericht `xrp_rtc_stufeA_bericht_v1.md` (SHA 9f37b7806ff60c67…).

Ergebnis, Kosten K1, gegen gematchte Kontrollen: X1 Failed Breakdown 68 Trades, 57 Paare, netto −0.293 R (Median −0.962), Kontrollen −0.300 R, ΔR Mittel +0.03, Median −0.03, 47 Prozent positive Paare, Bootstrap −0.48 bis +0.52, PF 0.61, Top-1 22.5 Prozent, Bloecke P1 +0.18 / P2 −0.35 (Median ΔR). X2 Double Bottom 17 Trades, 17 Paare, netto −0.091 R, ΔR +0.16 / +0.21, 53 Prozent positiv, Trendquote 71 Prozent gegen 34 Prozent der Kontrollen (Δtrend +0.41, Bootstrap +0.20 bis +0.59), aber MFE 0.46 R gegen 1.19 R, 71 Prozent der Trends nach dem Exit, Top-1 75 Prozent, Median ohne bestes Paar negativ. X3 Wick plus Volumen 22 Trades, 14 Paare, netto −0.552 R, PF 0.16, ΔR Mittel −0.98 / Median +0.08, Bloecke gegenlaeufig. Holm-p 0.97, 0.69, 0.97. Status nach Regel v2: alle drei NO EVIDENCE, INCONCLUSIVE (je 1 von 4 Kriterien), kein Fast Fail (Median ΔR nicht unter 0 mit Anteil unter 0.40), kein Fast Promote, keine Validation. Evidenzklasse Independent discovery. Basisrate aller Kontrollgruppen negativ (Median −0.8 bis −1.2 R).

Trigger-Familie: TA und TB je Kandidat besser als T0 (X1 +0.15, +0.08 R je Kandidat) ausschliesslich durch weniger Trades, je Trade gleich (X1 T0 −0.29, TA −0.30 R, MFE und Capture identisch). Exit-Familie: E-D verlaengert Haltedauer (X2 +43 Kerzen) und Giveback (+0.75 bis +0.90 R), Capture Ratio nirgends besser, auf X1 schlechter (ΔCapture −0.12, ΔR −0.38, p_pos 0.005). E0 beste Capture Ratio auf allen drei Familien bei gleicher oder schlechterer Erwartung. Inkremente: RTC-1 insufficient coverage (2, 0, 1), RTC-2 auf X1 kein Inkrement (Mittelwertdifferenz −0.17 R, p_pos 0.35), sonst insufficient coverage.

Technische Provenance: Erster Auswertungslauf mit Berichtsfehler in der Inkrement-Bootstrap (Verkettung statt Differenz), korrigiert, neu gelaufen, primaere, Trigger- und Exit-Abschnitte byteidentisch, erster Lauf unter `eval_run1_incbug/` aufbewahrt. Keine Regel oder Definition geaendert.

Naechster Schritt: DOT v1.0 Outcome-Lauf mit demselben Skript, ohne Aenderung.

## 2026-09-18 01:10 UTC — DOT v1.0 Outcome-Lauf abgeschlossen (Independent discovery), Cross-Coin-Zusammenfassung v1

Lauf: `eval_cross.py` (SHA 3975f2b2…, byteidentisch mit dem XRP-Lauf, keine Aenderung zwischen den Coins), Seed 20260918, Ergebnis `05_dot_specialist/eval/eval_DOT.json` (SHA 987864f001624866…), Bericht `dot_rtc_stufeA_bericht_v1.md` (SHA fb1f6b0a66fefb13…).

Ergebnis, Kosten K1, gegen gematchte Kontrollen: D1 Failed Breakdown 54 Trades, 52 Paare, netto −0.168 R (Median −0.894, K0 +0.028), Kontrollen −0.650 R (Median −1.289, Trefferquote 16.5 Prozent), ΔR Mittel +0.52, Median +0.21, 67 Prozent positive Paare, Bootstrap Median +0.08 bis +0.51, Top-Paar 16 Prozent, Bloecke P2a +0.17 / P2b +0.25, Holm-p 0.056. Regel v2: Kriterien 1, 3, 4 erfuellt, 2 nicht (MFE, Capture, Trendquote wie Kontrollen). STATUS MECHANISTICALLY PROMISING, validation-eligible (54 Trades ueber 20), formal supported nein (netto K1 unter null, Holm-p ueber 0.05). D2 Double Bottom 15 Trades, 13 Paare, netto −0.335 R, ΔR +0.09 / +0.34, 62 Prozent positiv, Top-1 76 Prozent, Bloecke gegenlaeufig: NO EVIDENCE, INCONCLUSIVE (2 von 4). D3 Wick plus Volumen 16 Trades, 16 Paare, netto −0.328 R, Kontrollen −1.052 R (Trefferquote 8 Prozent), ΔR +0.80 / +0.50, 81 Prozent positiv, beide Bloecke positiv, Holm-p 0.048, aber Top-1 84 Prozent der Gewinne und 16 Trades: STATUS MECHANISTICALLY PROMISING, nicht validation-eligible (unter 20 Trades), Befund bleibt stehen. Evidenzklasse Independent discovery. Kein Fast Fail, kein Fast Promote.

Trigger-Familie: D1 TA je Trade +0.041 R (PF 1.10, 23 Trades, MFE 0.93 R) gegen T0 −0.168 R, je Kandidat +0.13 R (p_pos 0.83), einzige Konfiguration des Laufs mit positiver Erwartung, nach Holm nicht positiv. TB wirkungslos. Exit-Familie: E-D auf allen drei Familien schlechter als E-U (ΔCapture −0.12 bis −0.15, Giveback +0.7 bis +1.0 R), E0 mit bester Capture Ratio, auf D2 einzige positive paarige Differenz (+0.32 R Median, 80 Prozent). Inkremente: RTC-1 insufficient coverage, RTC-2 gegen die Hypothese (D1 −0.20 R, D3 −1.03 R Mittelwertdifferenz).

Vorbehalt, im Bericht ausgewiesen: Der Vorsprung von D1 und D3 besteht gegenueber der schlechtesten Kontrollgruppe der drei Coins, keine Familie ist netto positiv. Ob ein Validation-Lauf fuer D1 gestartet wird, ist Entscheidung des Nutzers, keine Empfehlung dieses Eintrags.

Cross-Coin-Zusammenfassung `00_gemeinsam/rtc_cross_coin_zusammenfassung_v1.md` (SHA 22720dfd8aff1de4…), Bericht ohne Pooling: A generalisiert auf XRP nicht, auf DOT nur relativ (1 von 3 relativ, 0 von 3 absolut). B T0 ist kein besserer Trade-off, auf DOT ist TA je Trade besser. C E-D liefert nur laengere Haltedauer, E0 die beste Capture Ratio auf allen sechs Familien. D konsistent ueber drei Coins: negative Basisrate der Kontrollen, Double Bottoms mit hoher Trendquote und zu fruehem Exit (Einstieg 4.8 bis 5.1 ATR ueber dem Tief, 47 bis 71 Prozent abgeschnittene Trends), TA filtert kaum, RTC-1 leer, RTC-2 gegen die Hypothese. Keine Konfiguration wirkt auf zwei Coins gleichgerichtet mit Status ueber inconclusive, Cross-Coin-Test nach Governance v1 nicht ausgeloest.

STOP: Keine Varianten, keine Parameteraenderung, kein Validation-Lauf, kein BTC-Stufe-B-Lauf ohne Freigabe. Endgueltige Vergleichstabelle mit Empfehlung je Mechanik nach dem BTC-Stufe-B-Lauf.

## 2026-09-18 02:30 UTC — Governance v1.1, D1-Zurueckstellung, RTC-1/RTC-2 abgeschlossen, neue Vorregistrierungen ETH/SOL, Bottom-Engine-Architektur, XS21, CoinGlass

Entscheide (Nutzer, nach Cross-Coin-Zusammenfassung v1, bestaetigt): keine bestehenden Urteile geaendert.

1. Governance v1.1 `00_doku/aurum_governance_evidence_v1.1.md` (SHA 03f40ee6a76c9211…), Abschnitte 1 bis 6 wortgleich mit v1 (d995baf0…), neu: Abschnitt 7 Economic Validation Gate (Holdout-Validation nur bei Netto-Erwartung K1 ueber null oder vorab eingefrorener Portfolio-/Hedge-Funktion, aendert keinen Discovery-Status), Abschnitt 8 Low-Frequency-Mechanismen (unter 20 deskriptiv, 20 bis 29 low-frequency evidence hoechstens mechanistically promising, ab 30 normal, Kontrollgruppe zwingend, Mindestzahl nirgends gesenkt), Abschnitt 9 Abschluss von Spezifikationen ohne Umetikettierung.
2. DOT D1 (T0, E-U): Status mechanistically promising und validation-eligible unveraendert. Validation zurueckgestellt, «validation deferred, economic gate»: Netto K1 −0.17 R, relativer Vorteil ueberwiegend gegenueber Kontrollgruppe mit −0.65 R.
3. RTC-1: insufficient coverage — Spezifikation abgeschlossen, keine Fortfuehrung. RTC-2: kein Inkrement — Spezifikation abgeschlossen, keine Fortfuehrung. Berichtsbefunde wortgleich bestehen, kein Fast Fail, OI und Funding als Datenklasse nicht verworfen.
4. REBOUND-20 `07_eth_sol_specialist/eth_sol_rebound20_prereg_v0.1.md` (SHA 7514d63f803e99f7…), eigenstaendiger Sleeve, outcome-informed Ebene C, BTC/XRP/DOT Development Evidence. Ausgangslage dokumentiert: E0 relativ besser, absolut auf allen Development-Coins negativ (−0.34 bis −0.58 R). Development-Pruefung (`dev/dev_rebound20.json` 286cffc63752de0e…) mit zwei Formen und je zwei Werten (ATR ≥ 1.0/1.5, Potenzial/R ≥ 1.0/1.5) und vorab benannter Auswahlregel (kleinster Wert mit nicht negativer E0-Erwartung auf zwei von drei Coins): KEIN Kandidat erfuellt die Regel. Mechanik des Verlusts: EMA20 in rund 50 Prozent erreicht (+0.3 bis +0.6 R), sonst Stop (−1.2 bis −1.4 R). Vorregistrierung NICHT freeze-faehig, drei neutrale Alternativen vorgelegt (Falsifikationslauf mit ATR ≥ 1.5, Abschluss, neue Stop-/Entry-Oekonomie als Development). Keine ETH/SOL-Daten geladen.
5. DB-CONTEXT `07_eth_sol_specialist/eth_sol_double_bottom_context_prereg_v0.1.md` (SHA 4834bc5507b54566…), low-frequency mechanism, drei getrennte Einstiege DB-C1 Retest (ab t+3, N+0.25/−0.5 ATR), DB-C2 Higher Low ueber Nackenlinie (Swing Low ≥ N−0.5 ATR), DB-C3 Konsolidierungsbreakout (Hoch der 18 Kerzen, ab t+19), Kontextfenster 60 Kerzen, Kontext bis 360 Kerzen oder Invalidierung (Schluss unter L2), Exit Tages-ATR-Chandelier plus Zeitstopp, Kontrollgruppe mit Ersatzniveaus. Development-Haeufigkeiten ohne Trade-Simulation (`dev/dev_dbctx_refined.json` c0591576abb04c36…): Retest 87 bis 94 Prozent nach Median 3 Kerzen (kein Filter), Higher Low 47 bis 71 Prozent nach 13 bis 27 Kerzen, Breakout 29 bis 50 Prozent nach 26 bis 39 Kerzen, Invalidierung in 60 Kerzen 35 bis 53 Prozent. Vier offene Entscheidungen vor dem Freeze (Exit, Fenster, Ersatzniveaus, ob C1 gefuehrt wird). Keine ETH/SOL-Daten geladen.
6. Architekturnotiz `00_doku/bottom_engine_architecture_v1.md` (SHA 3c17de7d3674dd56…): Bottom Engine als Erkennungsschicht mit zwei getrennten Ausgaben (Bottom Signal → Rebound Sleeve, Trend Context → Delayed Trend Entry), kein Trade muss beides leisten. Zentrale neue Architekturhypothese.
7. XS21 Point-in-Time `01_forschung/09_lane_c/xs21_point_in_time_prereg_v0.1.md` (SHA 00a98886c8414f00…): Universum aus `binance_um_universe.csv`, Stufe-2-Regeln woertlich, neu nur Umsatzschwelle 50 Mio USD Vormonat, Delisting-Glattstellung K2, Zerlegung Ueberlebende gegen delistete als Kernfrage, Start 2020-02, vier offene Entscheidungen.
8. CoinGlass `02_daten/coinglass_abdeckungspruefung_v1.md` (SHA 0b261cef350252ce…): Startup-Plan liefert 4h/8h-nahe Intervalle nur 180 bis 360 Tage (nicht mehr als der kostenlose Kraken-Endpunkt), nur 1d «all-time»; Kraken im Funding-History-Endpunkt nicht belegt. KEIN Kauf. Vorher Support-Anfrage, gegebenenfalls Hobbyist 29 USD statt Startup.
9. BTC Stufe B bleibt Development, separat freizugeben. Keine ETH/SOL-Outcomes, keine Backtests.

## 2026-09-18 08:30 UTC — REBOUND-20 v0.1 abgeschlossen, REBOUND-MICRO v0.1 vorbereitet (outcome-blind, kein P&L)

REBOUND-20 v0.1 — Spezifikation abgeschlossen, keine Fortfuehrung. Keine Umetikettierung. Begruendung (`10_rebound_micro/rebound20_closure_v1.md`, SHA 9a24c4296f444a5f…): Payoff-Geometrie auf BTC/XRP/DOT strukturell unguenstig, EMA20-Rebounds +0.33 bis +0.60 R, Verluste −1.2 bis −1.4 R, Trefferquote rund 50 Prozent, Break-even 72 Prozent bei +0.5/−1.3, keine Mindestbedingung erfuellte die vorab benannte Auswahlregel. ETH/SOL nicht verbraucht.

REBOUND-MICRO v0.1 (neue outcome-informed Hypothese Ebene C, BTC/XRP/DOT Development only, ETH/SOL unberuehrt): Forschungsplan (SHA 282157276409c1b9…), 1h-Feature-Spezifikation (56ea28fb4aa78dc7…), Equilibrium-Ziel (ce625b976be93916…, Q0 EMA20 fix als Limit, Q1 Anchored VWAP mit genau einer Anker-/Resetregel: Anker erste 1h-Kerze der 4h-Kerze mit K1 falsch→wahr, Episode endet nach sechs K1-falschen 4h-Kerzen, kein Volume Profile), Promotion-Regeln numerisch vor Outcome (66fc38b09c0a3258…), Trial-Accounting (ac47db7764f57789…, primaer 6 je Coin, Vorbelastung 30 bis 37, global rund 240), 1h-Datenaudit (7235751ac60897d6…), 1h-Library `mlib.py` (cfe1f7aa375d4a05…) mit 5 von 5 Unit- und Look-ahead-Tests, outcome-blinder Vorbericht (d776c4e11586d7d5…).

Outcome-blinde Zaehlung (keine Exits, kein P&L, keine MFE/MAE): Kontext-Events mit vollstaendigem 1h-Fenster BTC 158, XRP 148, DOT 89. M1 (1h-Reclaim) mit engem Invalidationspunkt (≤ 1 ATR14(4h)): 98, 79, 46; M2 3, 5, 4; M3 1, 6, 5 (M2 und M3 in 70 bis 92 Prozent ohne engeren Stop als die 4h-Struktur). Stopdistanz M1 Median 0.42 bis 0.53 ATR14(4h), Baseline 0.76 bis 0.86, Verhaeltnis rund 0.5. Geometrisches RR zu Q0 nach K1 Median 0.29 bis 0.49 (p_BE_geo 0.58 bis 0.64), zu Q1 1.07 bis 1.54 (p_BE_geo 0.31 bis 0.36) bei Q1-Abstand Median 1.6 bis 1.8 ATR. KOSTENBEFUND: K1-Kosten je Trade im Median 0.68 bis 0.90 R (K0 0.22 bis 0.29, K2 1.5 bis 2.0), weil R bei engen Stops nur 1.1 bis 1.5 Prozent des Kurses betraegt. Nested Flow-Vergleich auf M1 nicht testbar (2 von 98 Faellen). Erwartete Zellen ≥ 30 nur M1×Q0 und M1×Q1 auf allen drei Coins.

Offen vor Freeze (Vorbericht Abschnitt 16): M2/M3 mitfuehren oder auf M1 beschraenken; Flow-Vergleich als insufficient coverage; Kostenlage K1 als Massstab mit K0/K2 als Bericht und Maker-Ausfuehrung als spaetere getrennte Hypothese; Baseline auf Kontextkerze; Zeitstopp 24 und Q0 als Limit bestaetigen. STOP, kein P&L-Lauf, keine ETH/SOL-Daten.

## 2026-09-18 14:40 UTC — REBOUND-MICRO v1.0 FREEZE (Entscheide des STOP-GATE, Cost-Audit PASS, kein Outcome)

Entscheide (Nutzer, 18.09.2026, nach Vorbericht v0.1, alle outcome-blind): (1) Primary-Matrix auf M1×Q0 und M1×Q1 beschraenkt, Holm ueber 2 je Coin; M2 und M3 vollstaendig simuliert und berichtet, Status ausschliesslich «descriptive / insufficient sample», keine Umetikettierung, keine weitere Schwellen- oder Feature-Suche. (2) Nested Flow-Vergleich «insufficient coverage — not formally testable in v1.0» (2 von 98, 2 von 79, 2 von 46); Flow-Flags und M3 deskriptiv, Flow-Definition unveraendert. (3) K1 alleiniger Primary-Kostenmassstab, K0/K2 nur Sensitivitaet, keine Maker-Gutschrift, Maker-/Limit-Execution nur als spaetere separate Vorregistrierung, Promotion-Regel unveraendert. (4) Baseline T0 exakt gepaart auf denselben 4h-Kontext-Events: Einstieg erste 1h-Eroeffnung nach der Kontextkerze, Stop Kontexttief minus 0.5 ATR14(4h), gleiche Q0/Q1, gleicher Zeitstopp 24 1h-Kerzen, gleiche Kosten; kein kuenstliches Paar wo M1 fehlt. (5) Zeitstopp 24 abgeschlossene 1h-Kerzen, Q0 = zum Einstieg bekannter EMA20-Wert als fester Level (kein Nachfuehren), Q1 = eingefrorener AVWAP-Level, keine Zielaenderung nach Einstieg.

Execution-Cost-Audit K1 (`10_rebound_micro/rebound_micro_execution_cost_audit_v1.md`, SHA cfa566bf1e03bb59…, Skript `audit/cost_audit.py` 6dd4209b334761ee…, Ergebnisse `audit/cost_audit_v1.json` ae38beada797ff6f…, `audit/cost_audit_m1_only.json` 8913f926ec650852…): PASS. Rundlauf K1 99 bp Stoppfad (40+2+5 / 40+2+10), 89 bp Zielpfad; Stopdistanz M1 Median 1.10 / 1.13 / 1.27 Prozent (BTC/XRP/DOT), Kosten in R = bp / Stopdistanz in bp = 0.90 / 0.88 / 0.78 R; `cost_R` der Zaehlung unabhaengig nachgerechnet, Abweichung ≤ 2.6e-14; Modell identisch mit `ylib.COST` seit Stufe A. Nichts geaendert. ERRATUM Vorbericht v0.1 Abschnitt 8: Kostenvergleichswerte waren ueber M1+M2+M3 gerechnet (DOT K1 0.68 statt M1-only 0.78 R, p_BE_geo Q1 K1 XRP 0.28 statt 0.31, DOT 0.32 statt 0.36); Abschnitte 7 und 13 waren M1-only und bleiben gueltig; Vorbericht v0.1 unveraendert, Erratum in Audit Abschnitt 6 und Spec v1.0 Abschnitt 12.

Freeze-Dateien: Spezifikation `10_rebound_micro/rebound_micro_spec_v1.0.md` (SHA 001a38534d87b2f8…), `mlib/mlib.py` v1.0 (6b7e7ba888e17cac…, v0.1 plus optionaler `ctx_override` in `join_4h` fuer die Kontrollgruppe, Standardverhalten unveraendert, Regression gegen Zaehlung v0.1 im Lauf erzwungen), `mlib/simulate_micro.py` v1.0 (fef60859063dd8bc…, Simulation nach Spec 4: Stop-Market mit Slippage, festes Limit-Ziel ohne Slippage, Stop-vor-Ziel bei Beruehrung in derselben Kerze, Zeitstopp Eroeffnung Kerze e+24, Gebuehren auf Ein- und Ausstiegspreis; Baseline; Kontrollen K1&K2&¬K3 via `rlib.match_controls`), `mlib/eval_micro.py` v1.0 (91f6455ecb2bd74d…, Bootstrap 2000 Seed 20260918, Holm ueber 2, Promotion-Pruefung, Regel v2 wie Spec 10 abgebildet, Q1-gegen-Q0 auf denselben Trades), Tests `mlib/tests/test_simulate.py` (b8616ef111a3b223…, 8 von 8 bestanden: Zielfill und Gebuehren von Hand, Stop mit Slippage, Gap-Stop und Gap-Ziel, gleichzeitige Beruehrung, Pruefreihenfolge, Zeitstopp exakt 24 Kerzen, Datenende, ungueltiger Stop, Diagnosen, synthetische Gesamtkette) und `mlib/tests/test_mlib.py` (bdd006b1c1bd8d64…, 5 von 5).

Ablauf: einmaliger Development-Lauf BTC → XRP → DOT, Ergebnisse je Coin versiegelt (SHA hier) bevor der naechste Coin laeuft, keine Regelaenderung zwischen Coins, Cross-Coin-Bericht ohne Pooling. Fragen A (Geometrie gegen T0), B (ueberlebt K1), C (Q1 gegen Q0). Falls A ja und B nein: Signalmechanik und Execution Economics getrennt beurteilen. Falls A und B nein: keine Fortfuehrung auf ETH/SOL. Keine ETH/SOL-Daten geladen.

## 2026-09-18 14:35 UTC — REBOUND-MICRO v1.0 Lauf BTC VERSIEGELT (vor XRP)

Einmaliger Development-Lauf BTC nach Spec v1.0, Regression der Kandidatentabelle gegen Zaehlung v0.1: IDENTICAL. Eingaben: spot1h 269b5fe188df0c5d…, spot4h 2d394fd1cbc344d5…, mlib 6b7e7ba8…, rlib f1ffdbb8…, simulate fef60859…. Ausgaben (SHA-256): `10_rebound_micro/run/BTC_trades.csv` 21ed24ccfca56bf4…, `BTC_baseline.csv` 9f68c91119a918ef…, `BTC_controls.csv` e955f10a9c8658af…, `BTC_eval.json` 4424ec355596237c…, `BTC_run.log` 8deda60bad688fd4….

Ergebnis BTC (K1, primaer): M1×Q0 n 84, Mittel r_net −0.95 R, Zielrate 49 Prozent, Stoprate 46 Prozent, avg_win +1.01 R, avg_loss −1.53 R, p_BE_emp 0.60, gepaart gegen Baseline (81 Paare) Median −0.375 R, 26 Prozent positiv → FAST FAIL. M1×Q1 n 80, Mittel −0.98 R, Zielrate 34 Prozent, avg_win +1.42 R, avg_loss −1.68 R, p_BE_emp 0.54, gepaart (75 Paare) Median −0.272 R, 28 Prozent positiv → FAST FAIL. Holm: keine Signifikanz. Vor Kosten (K0): M1×Q0 Mittel −0.27 R, gepaart Median −0.14 R (31 Prozent positiv); M1×Q1 Mittel −0.23 R, gepaart Mittel +0.08 aber Median −0.13 R (32 Prozent positiv). Baseline K1: −0.59 R (Q0), −0.62 R (Q1). M2/M3: 3, 3, 0, 1 Trades, deskriptiv. Keine Regelaenderung. Naechster Coin XRP.

## 2026-09-18 14:50 UTC — REBOUND-MICRO v1.0 Lauf XRP VERSIEGELT (vor DOT)

Einmaliger Development-Lauf XRP nach Spec v1.0, Regression der Kandidatentabelle gegen Zaehlung v0.1: IDENTICAL. Ausgaben (SHA-256): `run/XRP_trades.csv` b36d1c8be483d370…, `XRP_baseline.csv` 4957af3213cea596…, `XRP_controls.csv` 856a9be9b5c0dcc4…, `XRP_eval.json` 531f7a494614da5c…, `XRP_run.log` e86f75d4a93d8df1….

Ergebnis XRP (K1, primaer): M1×Q0 n 64, Mittel −0.82 R, Zielrate 41 Prozent, Stoprate 50 Prozent, avg_win +1.04 R, avg_loss −1.60 R, p_BE_emp 0.61, gepaart (59 Paare) Median −0.291 R, 25 Prozent positiv → FAST FAIL. M1×Q1 n 69, Mittel −0.89 R, Zielrate 36 Prozent, avg_win +1.10 R, avg_loss −1.53 R, p_BE_emp 0.58, gepaart (62 Paare) Median −0.269 R, 31 Prozent positiv → FAST FAIL. Holm: keine Signifikanz. Vor Kosten (K0): M1×Q0 Mittel −0.20 R, w/l 1.29, p_BE 0.44, gepaart Mittel +0.02, Median −0.12 (34 Prozent positiv); M1×Q1 Mittel −0.26 R, gepaart Mittel +0.18, Median −0.13 (34 Prozent positiv). Baseline K1 −0.39 R (Q0), −0.30 R (Q1). M2/M3: 4, 4, 2, 6 Trades, deskriptiv. Keine Regelaenderung. Naechster Coin DOT.

## 2026-09-18 15:00 UTC — REBOUND-MICRO v1.0 Lauf DOT VERSIEGELT (alle drei Coins abgeschlossen)

Einmaliger Development-Lauf DOT nach Spec v1.0, Regression der Kandidatentabelle gegen Zaehlung v0.1: IDENTICAL. Ausgaben (SHA-256): `run/DOT_trades.csv` 0919036fc822ea26…, `DOT_baseline.csv` 98f9ab184446f7a6…, `DOT_controls.csv` 9ec6659c52a75c2c…, `DOT_eval.json` 9716002c506038a7…, `DOT_run.log` 61a8a26d3e1dd564….

Ergebnis DOT (K1, primaer): M1×Q0 n 37, Mittel −0.63 R, Zielrate 38 Prozent, Stoprate 49 Prozent, avg_win +1.00 R, avg_loss −1.63 R, p_BE_emp 0.62, gepaart (35 Paare) Median −0.221 R, 31 Prozent positiv → FAST FAIL. M1×Q1 n 42, Mittel −0.93 R, Zielrate 26 Prozent, Stoprate 64 Prozent, avg_win +1.58 R, avg_loss −1.71 R, p_BE_emp 0.52, gepaart (42 Paare) Median −0.366 R, 24 Prozent positiv → FAST FAIL. Holm: keine Signifikanz. Vor Kosten (K0): M1×Q0 Mittel −0.16 R, gepaart Median −0.05 (37 Prozent positiv); M1×Q1 Mittel −0.39 R, gepaart Median −0.13 (26 Prozent positiv). Baseline K1 −0.26 R (Q0), −0.38 R (Q1). M2/M3: 3, 2, 4, 3 Trades, deskriptiv. Keine Regelaenderung. Cross-Coin-Bericht folgt ohne Pooling.

## 2026-09-18 15:20 UTC — REBOUND-MICRO v1.0 Cross-Coin-Bericht, Statusvorschlag

Berichte: `10_rebound_micro/rebound_micro_bericht_BTC_v1.md`, `_XRP_v1.md`, `_DOT_v1.md` (aus den versiegelten eval.json erzeugt, `mlib/report_coin.py`), `rebound_micro_cross_coin_bericht_v1.md` (keine Pooling-Statistik). SHA-256 der Berichte in `rm12_expected_shas.txt` und im Projekt.

Befund ueber drei Coins (je Coin, Vorzeichen uebereinstimmend): M1×Q0 und M1×Q1 nach K1 Mittel −0.63 bis −0.98 R, gepaart gegen T0 auf demselben Event Median −0.22 bis −0.38 R mit 24 bis 31 Prozent positiven Paaren → FAST FAIL in allen sechs Primary-Zellen, Holm p 1.000. Vor Kosten (K0): Verhaeltnis avg_win/|avg_loss| in fuenf von sechs Zellen besser als die Baseline (0.86 bis 1.38), realisierte Trefferquote (29 bis 46 Prozent) aber in allen sechs Zellen unter der eigenen Break-even-Quote (0.42 bis 0.54) und unter der Baseline (40 bis 54 Prozent), weil die Stoprate von 37 bis 41 auf 46 bis 64 Prozent steigt; gepaarte Differenz K0 Median −0.05 bis −0.14 R, 26 bis 37 Prozent positiv. Frage A: nein im Ergebnis. Frage B: nein (Kostenanteil 0.57 bis 0.88 R wie im Audit). Frage C: nein (Q1 minus Q0 auf denselben Trades −0.01 bis −0.23 R, Zielrate Q1 tiefer). M2/M3 deskriptiv (2 bis 6 Trades), Flow insufficient coverage, Kontrollgruppe ohne erkennbaren Location-Effekt. Keine Promotion.

Statusvorschlag (Spec v1.0 Abschnitt 10, A nein und B nein): REBOUND-MICRO v1.0 — Spezifikation abgeschlossen, keine Fortfuehrung, keine ETH/SOL-Vorregistrierung, keine Maker-/Execution-Hypothese (Vorzeichen bereits vor Kosten negativ). Keine Umetikettierung: Fast-Fail-Status der sechs Zellen bleibt, Vorbericht v0.1 mit Erratum bleibt. ETH/SOL unberuehrt. Roadmap-Einordnung im Cross-Coin-Bericht Abschnitt 10 (Rebound-Sleeve ruhen lassen, Trend-Context-Zweig priorisieren). Bestaetigung durch den Nutzer ausstehend.

## 2026-09-19 — REBOUND-MICRO v1.0 ABGESCHLOSSEN, REBOUND als Strategie-Familie geschlossen (Nutzerentscheid)

Status bestaetigt: **REBOUND-MICRO v1.0 — Spezifikation abgeschlossen, keine Fortfuehrung.** Keine anderen eingefrorenen Urteile veraendert (Stufe 1, Stufe 2, MTP VERWORFEN, YAMATO Stufe A, XRP v1.0, DOT v1.0, RTC-1/RTC-2 abgeschlossen, REBOUND-20 abgeschlossen, DOT D1 MP validation deferred). Fast-Fail-Status der sechs Primary-Zellen, deskriptiver Status von M2/M3, «insufficient coverage» fuer Flow und der Vorbericht v0.1 mit Erratum bleiben wortgleich bestehen.

Begruendung (ausdruecklich): (1) REBOUND-20 war absolut negativ (E0 −0.34 bis −0.58 R, keine Mindestbedingung erfuellt, Closure 9a24c429…). (2) REBOUND-MICRO verbessert zwar die geometrische Reward/Loss-Struktur (avg_win/|avg_loss| vor Kosten in fuenf von sechs Zellen besser als T0), erhoeht aber die Stoprate so stark (37 bis 41 auf 46 bis 64 Prozent), dass die reale Erwartung auf BTC, XRP und DOT verschlechtert wird (gepaart gegen T0 Median −0.22 bis −0.38 R nach K1, 24 bis 31 Prozent positive Paare). (3) Der Befund gilt bereits vor Kosten gegenueber der gepaarten T0-Baseline (K0 Median −0.05 bis −0.14 R, 26 bis 37 Prozent positiv, in allen sechs Zellen). (4) Deshalb keine Maker-/Execution-Hypothese, keine dritte Rebound-Variante und keine ETH/SOL-Vorregistrierung.

REBOUND als Strategie-Familie (REBOUND-20, REBOUND-MICRO) wird vorerst geschlossen. Der Bottom-/Selloff-Kontext (K1/K2/K3, Double-Bottom-Strukturen) wird ausdruecklich NICHT verworfen; offen bleibt ausschliesslich seine Verwendung als Delayed-Trend-Context (neue Architektur, nur Spezifikation, kein Backtest, `11_delayed_trend/delayed_trend_research_plan_v0.1.md`). Naechste Schritte: A. BTC YAMATO Stufe B separat durchfuehren (BTC Development-Markt, keine Regeln aus REBOUND-MICRO uebernommen). B. DELAYED-TREND Forschungsplan v0.1, danach STOP mit offenen Entscheidungen. Parallel XS21 und Lane C. ETH/SOL weiterhin unberuehrt.

Cross-Coin-Bericht `10_rebound_micro/rebound_micro_cross_coin_bericht_v1.md` (SHA c239031dc21f355a…), Coin-Berichte BTC b68b269bb8868e29…, XRP bc410015ceab2a12…, DOT 10d67096fe5bf143….

## 2026-09-19 — BTC YAMATO Stufe B v1.0 FREEZE (vor Outcome)

Spezifikation `06_btc_specialist/btc_yamato_stufeB_spec_v1.0.md` (SHA 0aed8e18aa7edf89…), ersetzt Vorregistrierung v0.1. Entscheide zu den vier offenen Punkten: TB bestaetigt (Reclaim in t+1..t+6), Exits E-D und E0 (statt E-W, Cross-Coin-Vergleichbarkeit, E-W nicht getestet), Erwartung je Kandidat als Hauptmetrik, BTC allein. BTC Development-Markt, Ebene C (outcome-informed aus Stufe A). Parameter `cfg_btc_stufeA` = Parameterpaket v1.1 wortgleich, Kandidaten identisch mit Stufe A (Y1 96, Y2 14, Y3 29, Kontrollpool 1666). Keine Regel aus REBOUND-MICRO. Keine Inkremente (RTC-1/RTC-2 abgeschlossen). Referenzzeilen Stufe A (Y1 TA/E-U 16 Signale −0.23 R Fast Fail, Y2 14 Signale −0.30 R inconclusive, Y3 6 inconclusive) werden reproduziert, nicht neu bewertet.

Skripte: `00_gemeinsam/rlib/count_btc_b.py` (c5d5b81889dec637…) und `eval_btc_b.py` (2335b4f27f0b8102…), abgeleitet aus count_cross.py (17d7cb93…) und eval_cross.py (3975f2b2…), Aenderungen ausschliesslich Modus, Praefix Y, Pfade, Coverage-Diagnose, Entfernung der Inkrement-Bloecke. Zaehlung outcome-blind `06_btc_specialist/stufeB/count/` (count_BTC_B.json 7528d6b72bdc2560…, Kandidaten 173db748014a5a3c… und e6c2726a866d7b08…, Matches d441dd3d…, e83845a9…, b03889ff…): Y1 T0 bis 95 Einstiege, TA 18, TB 72; Y3 T0 27, TA 6, TB 17; Y2 14; Matching Y1 89 von 96 mit Kontrolle. Tests: primaer Holm ueber 3, Trigger Holm ueber 4, Exit Holm ueber 3, E0 ein Test, Seed 20260918, Bootstrap 2000. Trial-Accounting 11, Vorbelastung BTC rund 36. Naechster Schritt: einmaliger Lauf, Bericht, Status.

## 2026-09-19 — BTC YAMATO Stufe B v1.0 LAUF VERSIEGELT, Bericht, Statusvorschlag

Einmaliger Lauf nach Spec v1.0, Referenzzeilen Stufe A exakt reproduziert (Y1 TA/E-U 16 Signale −0.229 R, Y2 14 −0.297 R, Y3 TA 6 −0.291 R). Ausgaben `06_btc_specialist/stufeB/eval/` (eval_BTC_B.json 5d70030f29443f2a…, Log 84dc0c1b03965…, 20 Trade-/Kontroll-/Paardateien mit SHA im JSON). Bericht `btc_yamato_stufeB_bericht_v1.md`.

Befund: Primaer T0/E-U gegen Kontrollen: Y1 78 Signale, −0.29 R, 70 Paare, ΔR Median −0.03, 49 Prozent positiv → no evidence inconclusive. Y2 14 Signale, −0.30 R, 13 Paare, ΔR +0.67 (Median +0.73, 77 Prozent, Holm 0.042), absolut negativ, unter 20 → deskriptiv. Y3 24 Signale, −0.40 R, 18 Paare, ΔR Median +0.29, 61 Prozent, Regel v2 drei von vier → low-frequency MP, validation deferred (Economic Gate, Netto −0.40 R, P2 −0.96 R, Top-Trade 58 Prozent). Trigger je Kandidat (Holm ueber vier, keiner signifikant): TA besser als T0 auf Y1 (+0.20 R) und Y3 (+0.27 R), TB dazwischen; Hypothese «Bestaetigung kostet Trend Capture» nicht gestuetzt. Exit (Holm ueber drei, keiner signifikant): E-D hebt Mittel ueber wenige lange Trend-Trades (Y1 +0.11 R Mittel bei Median −1.20, 14 Prozent positive Paare), Capture tiefer, Giveback hoeher; E0 auf Y1/Y3 schlechter. Kein Muster auf zwei Coins in derselben Konfiguration gleich stark, kein Cross-Coin-Test.

Statusvorschlag: BTC YAMATO Stufe B v1.0 — abgeschlossen, keine Validation, keine Stufe C. Stufe A unveraendert. Bestaetigung durch den Nutzer ausstehend.

## 2026-09-19 — DELAYED-TREND Forschungsplan v0.1 erstellt (nur Spezifikation, kein Backtest, keine Zaehlung)

`11_delayed_trend/delayed_trend_research_plan_v0.1.md` (SHA 0241c24798b3970c…). Neue Architektur: Bottom erzeugt keinen Trade, nur `bullish_trend_context_active`; drei Entry-Familien DT1 Higher Low, DT2 Retest and Hold, DT3 Consolidation Breakout; Kontextquellen S1 Double Bottom (Y2/X2/D2) und optional S2 Failed Breakdown (Y1/X1/D1), Definitionen unveraendert aus den eingefrorenen Specs; outcome-blinde Geometrie (Zeit bis Einstieg, Stop in ATR und Prozent, Distanz zu Vor-Selloff-Hoch und 20-Tage-Hoch, RR_geo, Kosten K1 in R, erwartete Kandidaten) VOR jedem P&L; Economic Gate numerisch vorab (Stop ≤ 3.0 ATR, Kosten ≤ 0.40 R, RR_geo ≥ 1.0, ≥ 20 Einstiege); Exit fuer spaeteren P&L nur vorgemerkt (Tages-ATR-Chandelier 3x, Zeitstopp 360). BTC/XRP/DOT Development, ETH/SOL unberuehrt. REBOUND bleibt geschlossen, kein EMA20-Ziel. Sechs offene Entscheidungen (Abschnitt 10), darunter Ersatz von DB-CONTEXT v0.1. STOP bis zur Freigabe, keine Messung.

## 2026-09-19 — YAMATO Stufe B bestaetigt, DB-CONTEXT superseded, DELAYED-TREND Entscheidungen (Nutzer)

Status bestaetigt: **BTC YAMATO Stufe B v1.0 — abgeschlossen, keine Stufe C.** Einzelurteile unveraendert: Y1 inconclusive, Y2 deskriptiv, Y3 low-frequency mechanistically promising / validation deferred am Economic Gate. Keine weitere YAMATO-Variante, keine Umetikettierung.

DB-CONTEXT v0.1 (`07_eth_sol_specialist/eth_sol_double_bottom_context_prereg_v0.1.md`, Datei unveraendert): `superseded before independent test by DELAYED-TREND development architecture`, Vermerkdatei `…_v0.1_SUPERSEDED.md`. Klausel «kein Rueckgriff auf BTC/XRP/DOT-Outcomes» mit der outcome-informed DT-Hypothese nicht vereinbar. ETH/SOL unangetastet, neue ETH/SOL-Prereg erst nach abgeschlossenem Development.

DELAYED-TREND Entscheidungen vor der Messung: (2) Kontextquellen S1 Double Bottom und S2 Failed Breakdown, vollstaendig getrennt, kein Pooling, maximal sechs Primary-Familien S×DT je Coin, Multiplizitaet vorab (Holm ueber sechs). (4) Economic Geometry Gate: A Median Stop ≤ 3.0 ATR, B Median K1-Kosten ≤ 0.40 R, C Median gross RR_geo zum Trendziel ≥ 1.50, D P25 RR_geo ≥ 1.00, E ≥ 20 erwartete Entries je Coin; keine Schwelle nach Outcome. (5) Trendziel = pre-selloff high nach exakter Library-Regel, vorab definiert. (6) DT1 Higher Low ohne rueckwirkende Swing-Erkennung, Entry erst nach vollstaendiger Bestaetigung. (7) DT2 Retest and Hold: eine abgeschlossene 4h-Kerze bestaetigt Hold ueber dem Level, Entry naechste Eroeffnung, Stop unter Retest-/Hold-Tief; Befund «Retest allein kein Filter» dokumentiert. (8) DT3 eine Konsolidierungsdefinition, keine Grid-Suche. (9) Kontextfenster 180 abgeschlossene 4h-Kerzen, Ende bei Schluss unter L_ref. (10) Je Kontext und Familie nur der erste gueltige Entry, Ueberschneidungen dokumentiert. (11) Outcome-blinde Messung sofort, 14 Berichtspunkte, kein P&L, keine Post-Entry-Groessen. XS21 und Lane C parallel.

## 2026-09-19 — DELAYED-TREND Messregeln v1.0 fixiert, outcome-blinde Messung, Economic Geometry Gate (STOP)

Messregeln `11_delayed_trend/delayed_trend_measurement_spec_v1.0.md` (SHA ec7ed6213ef52a8d…), vor der Messung fixiert: S1 (Y2/X2/D2, t Bruchkerze, L_ref = L_s2, P = N, Zielreferenz s2), S2 (Y1/X1/D1, t Kandidatenkerze, L_ref = L_t, P = tb_lvl_y1, Zielreferenz t); Fenster 180, Invalidierung Schluss < L_ref; Trendziel H_pre = hh120 an der Referenzkerze (Library-Regel, Lookback 120); DT1 Swing Low s (k=3, bekannt s+3), L_s ≥ L_ref + 0.5 ATR_t, Anstieg ≥ 1 ATR_t, Einstieg s+4, Stop L_s − 0.5 ATR; DT2 Retest b ≥ t+3 (L ≤ P+0.25, C ≥ P−0.5), Hold C_{b+1} > P, Einstieg b+2, Stop min(L_b, L_{b+1}) − 0.5 ATR, gescheiterter Retest beendet; DT3 Box t+1..t+18 Breite ≤ 3 ATR_t, Schluss > Boxhoch ab t+19, Stop Boxtief − 0.5 ATR; Gate A ≤ 3.0 ATR, B ≤ 0.40 R, C RR gross ≥ 1.5, D P25 ≥ 1.0, E ≥ 20 (Untergrenze ohne Folgeeinstieg in 180 Kerzen); Holm ueber bis zu sechs Zellen je Coin. Library `dtlib/dtlib.py` (f2d6c3906aff57d3…), `measure_dt.py` (05014537d686877b…), Tests 5 von 5 (105fdb3578a1ffff…, Handrechnung DT1/DT2/DT3, Invalidierung, Geometrie, Look-ahead).

Messung (keine Outcomes, keine Post-Entry-Groessen), `out/{BTC,XRP,DOT}_measure.json` (f61ea0e93f8e03a5…, c9e667140139d2cd…, 1a7b645cf46e305d…), Bericht `delayed_trend_vorbericht_geometry_gate_v1.md` (0e3085a484371cd0…): Kontexte S1 14/17/15, S2 96/92/75 (S2 in 79 bis 88 Prozent innerhalb 180 Kerzen invalidiert, Median 8 bis 10 Kerzen). Einstiege S2×DT1 35/43/31, S2×DT2 49/46/40, S1-Zellen 2 bis 15, DT3 2 bis 11. Geometrie DT1/DT2: Stop Median 1.2 bis 1.9 ATR (2.7 bis 5.2 Prozent), Kosten K1 0.19 bis 0.37 R, Ziel 6 bis 10 ATR (12 bis 26 Prozent) ueber Einstieg, RR gross Median 4.5 bis 9.0, P25 1.9 bis 6.8. DT3 Stop 3.8 bis 4.4 ATR (strukturell), RR 1.4 bis 2.8. DT2 tritt in 42 bis 65 Prozent am fruehesten Zeitpunkt (t+5) auf, DT1 nach Median 10 bis 17 Kerzen. GATE PASS: BTC S2×DT1 (21/35), XRP S2×DT1 (22/43), XRP S2×DT2 (21/46). Nur an E (Untergrenze) gescheitert: BTC S2×DT2 (19/49), DOT S2×DT1 (12/31), DOT S2×DT2 (12/40). Alle S1 an E, alle DT3 an A und E. Sechs offene Entscheidungen (Bericht Abschnitt 7). STOP, kein P&L, keine ETH/SOL-Daten.

## Offen

- Betriebsort: Raspberry Pi, Cloud-Server oder Mac
- Kapitalrahmen und akzeptabler Totalverlust
- Boerse fuer Perpetuals
- Steuerliche und rechtliche Einordnung in der Schweiz
- Zeitbudget
- Abwicklung des Altsystems Aurum


# Schritt 0 — Entscheide vom 01.10.2026 (Entwurf v0.2 uebernommen)

## 2026-10-01 — Schritt 0: Entwurf v0.2 formell uebernommen (Nutzerentscheid)

Damian uebernimmt alle Empfehlungen aus «ENTSCHEIDE – Entwurf Schritt 0, Version 0.2» (Claude, 01.10.2026) inklusive der neuen Punkte B7 und B8. Quelle: `00_doku/entwuerfe/ENTSCHEIDE_Entwurf_Schritt0_v0.2.docx` (SHA 02fbeafbd23f7b10…), Vorversion v0.1 (c841cbc589ed832d…) liegt daneben. Jeder Punkt folgt als eigener Eintrag mit dem Wortlaut der Empfehlung (Umlaute nach Konvention dieser Datei umschrieben, Befunde siehe Entwurf). Offen bleiben D2 und D3 (Zahlen von Damian ausstehend). Reihenfolge nach Entscheid laut Entwurf: E2 Collector, E1 Hygiene, B1 bis B8 einfrieren und XS21 PiT v1.0 ein Lauf, A1 bis A8 einfrieren und DT-P&L ein Lauf mit anschliessender Anwendung von A7, Engine-MVP mit Abnahme gegen die eingefrorenen Stufe-2-Trades, Paper nur fuer Kandidaten mit bestandenem Gate.

## 2026-10-01 — A1 Lesart von Gate E

Empfehlung: 3 primaere Zellen (BTC S2×DT1, XRP S2×DT1, XRP S2×DT2) plus 3 sekundaere Grenzfaelle (BTC S2×DT2, DOT S2×DT1, DOT S2×DT2), Holm ueber alle 6.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

## 2026-10-01 — A2 S1 (Double Bottom), alle 6 Zellen unter 20 Einstiegen

Empfehlung: deskriptiv mitfuehren, ohne Test und ohne Status.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

## 2026-10-01 — A3 DT3 (Gate A ueberall verfehlt)

Empfehlung: abschliessen mit Vermerk «Spezifikation abgeschlossen, keine Fortfuehrung» (Governance v1.1 §9).

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

## 2026-10-01 — A4 Exit

Empfehlung: Tages-ATR14-Chandelier 3×, nur steigend, Zeitstopp t+360, wie im Vorbericht.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

## 2026-10-01 — A5 Kontrollgruppe

Empfehlung: gematchte Kontexte ohne Struktur mit Ersatzniveaus, wie im Vorbericht.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

## 2026-10-01 — A6 Primaermetrik

Empfehlung: gepaartes ΔR (Status nach Regel v2) und Netto-K1. Fortfuehrung nur bei Netto-K1 ≥ 0.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

## 2026-10-01 — A7 Harte Abbruchregel fuer Lane A (neu)

Regel: Vor dem DT-P&L-Lauf festgeschrieben: Ist Netto-K1 in den drei Primaerzellen zusammen kleiner als null, wird Lane A (Bottom, Reversal, Rebound, DT) vollstaendig geschlossen. Es folgt keine weitere Variante, keine Umformulierung und kein neuer Timeframe auf BTC, XRP oder DOT. Eine Wiederaufnahme waere nur mit neuen Daten (Forward-Fenster) und einer neuen Vorregistrierung zulaessig, die diesen Entscheid ausdruecklich zitiert.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

## 2026-10-01 — A8 Evidenzwert eines positiven DT-Ergebnisses (neu)

Regel: DT ist outcome-informed (Ebene C), laeuft auf denselben Discovery-Daten wie alle gescheiterten Vorgaenger, und die globale Trial-Zahl liegt bei rund 240. Ein positives Ergebnis gilt deshalb hoechstens als «mechanistically promising» in der Klasse Development. Ein Holdout-Lauf ist nur nach dem Economic Validation Gate zulaessig (Governance v1.1 §7), und dieser Vermerk wird im DT-Freeze woertlich uebernommen.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

## 2026-10-01 — B1 Umsatzschwelle 50 Mio. USD Vormonat

Empfehlung: Schwelle als Definition des breiten Forschungsuniversums (U1) bestaetigen, die Begruendung aber streichen und durch «Mindestliquiditaet auf der Signalboerse» ersetzen. Die Ausfuehrbarkeit regelt B8.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

Umsetzung: XS21 PiT Vorregistrierung v0.2 (ENTWURF, nicht eingefroren) `01_forschung/09_lane_c/xs21_point_in_time_prereg_v0.2.md`, gilt fuer B1 bis B8.

## 2026-10-01 — B2 Dezil-Variante (oberstes und unterstes Dezil)

Empfehlung: als vorregistrierten Vergleich behalten, nicht als Auswahl. Top-3 bleibt primaer.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

## 2026-10-01 — B3 Delisting-Glattstellung

Empfehlung: zur letzten Tageskerze mit K2-Slippage bestaetigen.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

## 2026-10-01 — B4 Short-Bein

Empfehlung: Long+Short primaer wie Stufe 2 (H-C3: Absicherung, kein Ertrag), Long-only als vorregistrierter Vergleich.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

## 2026-10-01 — B5 Holdout-Status von XS21 (neu, Klaerung)

Empfehlung: Fuer die XS21-Regel und fuer D-CC gilt der Zeitraum ab 2024 als verbraucht. Der PiT-Lauf rechnet 2020-02 bis 2026-09-14 in einem einzigen Lauf mit der Etikette «Discovery/Robustheit mit Vorbelastung», der Teil ab 2024 wird separat ausgewiesen. §2 und §4 der PiT-Vorregistrierung werden entsprechend korrigiert. Die einzige saubere Out-of-Sample-Evidenz fuer XS21 und D-CC ist ein Forward-Fenster ab 15.09.2026, beginnend mit dem Collector (E2). Das Etikett Holdout validation ist fuer beide ausgeschlossen. Die Stufe-2-Urteile bleiben unveraendert.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

## 2026-10-01 — B6 Ausfuehrbarkeit (neu)

Empfehlung: Die Forschungsfrage (existiert der Effekt ohne Survivorship?) wird auf U1 beantwortet. Ueber einen Sleeve entscheidet nur das ausfuehrbare Universum U2 (B8). Vor jedem Paper-Betrieb gilt zusaetzlich ein Ausfuehrbarkeits-Gate auf der gewaehlten Boerse.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

## 2026-10-01 — B7 Nicht-Krypto-Perps ausschliessen (neu)

Empfehlung: Vor dem Freeze eine Ausschlussregel festschreiben: Nur Symbole, deren Basiswert ein Krypto-Asset ist. Umsetzung ueber eine eingefrorene Ausschlussliste mit Pruefsumme, erstellt nach Basiswert und nicht nach Ergebnis, jeder Ausschluss mit Grund. Stablecoin-Paare werden ebenfalls ausgeschlossen.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

Umsetzung: Ausschlussliste ENTWURF v0.1 `01_forschung/09_lane_c/xs21_pit_v0.2/xs21_exclusions_v0.1.csv` mit Pruefsummen, vor dem Freeze durch Claude/Damian zu pruefen (unklare Symbole separat gelistet).

## 2026-10-01 — B8 Zweites, ausfuehrbares Universum U2 (neu)

Empfehlung: Zusaetzlich zu U1 wird vor dem Freeze ein point-in-time Liquiditaetsuniversum U2 vorregistriert: am Stichtag die 20 Krypto-Symbole mit dem hoechsten Binance-Quote-Volumen des Vormonats, nach B7 gefiltert. Die Rangbildung ist point-in-time und daher frei von Survivorship. Gleiche Regeln wie Stufe 2, Holm ueber U1 und U2. Als Sleeve-Kandidat zaehlt nur U2. Besteht U1, aber nicht U2, ist der Effekt real, aber fuer ein Privatkonto nicht handelbar.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

## 2026-10-01 — C1 Spot oder Perps

Empfehlung: Spot fuer die Long-Seite. Perps nur dort, wo ein Short-Bein (XS21) oder ein Carry-Bein (D-CC) es verlangt. Der bisherige Eintrag «Perps statt Spot» wird damit praezisiert, nicht gestrichen.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

## 2026-10-01 — C2 Ein Kostenmodell

Empfehlung: ein zentrales costs.yaml mit Spot- und Perp-Modell (K0/K1/K2) als einzige Quelle. Die abweichenden Saetze in 05_evidenz/README.md werden mit Vermerk korrigiert. Zusaetzlich ein venue-spezifisches Kraken-Modell: Kraken-Spot-Taker 0.80 % je Seite (ENTSCHEIDE Tier 1) liegt doppelt so hoch wie K1-Spot mit 0.40 %. Spot-Long auf Kraken wird deshalb mit Maker-Ausfuehrung geplant, Taker-Ausfuehrung wird mindestens unter K2 gerechnet. Eingefrorene Laeufe bleiben unveraendert und referenzieren ihre damaligen Werte.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

Umsetzung (01.10.2026): `config/cost_model_v1.json` Version 1.1 mit neuem Abschnitt `venue_kraken` (Spot Maker 0.40 / Taker 0.80, Futures Maker 0.02 / Taker 0.05 Prozent je Seite, Tier 1). Die Abschnitte `spot_r`, `stage2_perp` und `stage2_spot_ref` (K0/K1/K2 der eingefrorenen Laeufe) bleiben wertgleich und sind per Test an die eingefrorenen Dateien gebunden. JSON statt YAML, weil die Datei bereits die einzige Quelle ist. Korrektur der Saetze in `05_evidenz/README.md` als neue Datei `05_evidenz/README_v1.1_gebuehren.md`, das Original bleibt unveraendert.

## 2026-10-01 — C3 Boerse

Empfehlung: Kraken fuer Spot-Long bestaetigen. Kraken Futures als Arbeitsannahme fuer das Short-Bein und D-CC auf den zehn Stufe-2-Coins beziehungsweise U2, vorbehaltlich D4. Eine zweite Boerse nur, falls U2 auf Kraken das Ausfuehrbarkeits-Gate nicht besteht. Keine Boerse wird gewaehlt, deren Zulaessigkeit fuer dich nicht manuell geprueft ist.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

## 2026-10-01 — D1 Betriebsort

Empfehlung: kleiner, selbst kontrollierter Cloud-Server oder eigener Rechner im Dauerbetrieb fuer Collector und Paper. Nicht der Mac und keine fremde Agent-Umgebung. Keys liegen nie in einer Agent- oder Chat-Sandbox.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

Vermerk (Damian, 01.10.2026): Uebergangsausnahme. Der Collector fuer oeffentliche Daten darf auf der Agent-Box laufen, bis Damian einen eigenen Server hat. Auf der Box liegen nie Keys.

## 2026-10-01 — D2 Kapitalrahmen und akzeptabler Totalverlust — OFFEN

Empfehlung: vor jeder Live-Phase als feste Zahl festlegen (Micro-Live-Betrag und Obergrenze Gesamtverlust, nach der das Projekt ohne Diskussion stoppt).

Entscheid: offen. Zahlen von Damian ausstehend, nicht entschieden.

## 2026-10-01 — D3 Zeitbudget — OFFEN

Empfehlung: Stunden pro Woche festlegen und eine Zeitbox fuer Schritt 3 von rund 2 Wochen. Ohne bestandenes Ergebnis nach der Zeitbox folgt ein Review-Termin statt neuer Hypothesen.

Entscheid: offen. Zahlen von Damian ausstehend, nicht entschieden.

## 2026-10-01 — D4 Steuern und Recht Schweiz

Empfehlung: vor Live klaeren (Qualifikation als private Vermoegensverwaltung oder gewerbsmaessiger Handel, Zulaessigkeit von Perps fuer Schweizer Privatkunden bei der gewaehlten Boerse, Vertragspartnerin und Aufsicht bei Kraken Futures (vermutlich Bermuda-Gesellschaft), allfaellige FIDLEG-Fragen bei grenzueberschreitender Erbringung, Hebel und Margin je Entity). Fuer Forschung und Paper nicht blockierend.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

## 2026-10-01 — D5 Abwicklung Altsystem

Empfehlung: Altsystem stilllegen, Keys widerrufen, Restbestaende dokumentieren. Turtle 55/20 nur als Referenz behalten, die Zahlen sind in Aurum II nicht nachgerechnet.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

Vermerk: Als Empfehlung uebernommen. Der Status von Altsystem und Keys (stillgelegt, widerrufen, Restbestaende) ist noch nicht bestaetigt, Bestaetigung durch Damian ausstehend.

## 2026-10-01 — E1 Git und Reproduzierbarkeit

Empfehlung: privates Git-Repo, Originale als eingefrorener Tag v0, gepinntes requirements.txt, Pfade ueber AURUM_ROOT in neuen Dateiversionen mit SHA-Vermerk. CI mit den 34 Tests und den vier Repro-Checks aus Review v1. Fehlende Stufe-2-Eingaben (DTB3_3m_tbill.csv, kraken_funding/PF_{XBT,ETH,SOL}USD_funding.csv) ablegen.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

Stand 01.10.2026: Repo mit Tag `original-2026-10-01`, gepinnte Abhaengigkeiten, AURUM_ROOT, `make ci` (34 Tests, vier Reproduktionen bitgleich) umgesetzt. DTB3 als FRED-Neuabruf abgelegt (SHA weicht vom Original ab, Stufe 2 trotzdem bitgleich). `kraken_funding/PF_{XBT,ETH,SOL}USD_funding.csv` fehlen weiterhin (Original noetig).

## 2026-10-01 — E2 Collector sofort

Empfehlung: taeglicher Collector auf oeffentlichen Endpunkten ohne Keys (Kraken-Futures-Funding aller PF-Symbole, Kraken OHLC 4h/1d, Binance-UM-Listing), validierend und atomar nach 02_daten/README.md, mit Heartbeat.

Begruendung: Kraken liefert Funding nur fuer ein rollendes Jahr, jeder Tag ohne Collector ist verloren.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

Stand 01.10.2026: Collector laeuft taeglich 06:15 Europe/Zurich auf der Agent-Box (Ausnahme D1), Status in `last_run_status.json` als Heartbeat. Binance nur ueber data.binance.vision (fapi geoblockt).

## 2026-10-01 — E3 Korrektur im Log

Empfehlung: Korrekturvermerk als neuer Eintrag, der alte bleibt stehen. Die veraltete mlib.py-SHA in rm_2026-09-18_expected_shas.txt wird mit Verweis auf v1.0 ergaenzt.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

Umsetzung: Korrekturvermerk als eigener Eintrag weiter unten, Ergaenzung zu `rm_2026-09-18_expected_shas.txt` als neue Datei `00_doku/rm_2026-09-18_expected_shas.addendum_2026-10-01.txt`.

## 2026-10-01 — E4 Arbeitsteilung

Empfehlung: Claude (Project) fuer Methodik, Vorregistrierungen, ENTSCHEIDE-Texte, Berichte und Review gegen die Governance. Coding-Agents fuer Repo, CI, Collector, Engine, Paper-Runner und unabhaengige Nachrechnung jedes Laufs. Kein Produktionscode in der Chat-Sandbox. Uebergabe ueber Git, ENTSCHEIDE bleibt die einzige Quelle.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

## 2026-10-01 — F1 Keine neuen Hypothesen bis XS21 PiT und DT entschieden sind

Regel: Keine neuen Lane-A-, Rebound-, Visual-AI-, Options- oder Halving-Straenge. D-CC wird nur als Forward-Datensammlung ab 15.09.2026 beobachtet, kein Sleeve. Falls D-CC spaeter wieder aufgenommen wird, gelten Spot und Perp auf derselben Boerse sowie ein Kapital- und Margin-Modell als Pflicht in der Vorregistrierung. ETH/SOL bleiben unberuehrt und damit als unabhaengige Maerkte erhalten.

Entscheid: Empfehlung uebernommen (Damian, 01.10.2026).

## 2026-10-01 — KORREKTURVERMERK zu «2026-09-18 14:35 UTC — REBOUND-MICRO v1.0 Lauf BTC VERSIEGELT» (E3)

Der Eintrag «REBOUND-MICRO v1.0 Lauf BTC VERSIEGELT» traegt 14:35 UTC und liegt damit zeitlich vor dem Eintrag «REBOUND-MICRO v1.0 FREEZE» mit 14:40 UTC. In der Datei steht der FREEZE-Eintrag vor dem Lauf-Eintrag, der Lauf-Eintrag nennt als Eingaben mlib 6b7e7ba8… und simulate fef60859…, also die eingefrorenen v1.0-Dateien. Mindestens einer der beiden Zeitstempel ist falsch. Welcher, laesst sich aus den vorliegenden Dateien nicht mehr belegen (die Lauf-Logs tragen keine Uhrzeit, die Dateizeiten stammen aus der Kopie). Massgeblich ist die Reihenfolge FREEZE vor Lauf. Beide alten Eintraege bleiben unveraendert stehen.

Ergaenzend: `00_doku/rm_2026-09-18_expected_shas.txt` nennt fuer `01_forschung/10_rebound_micro/mlib/mlib.py` noch die SHA von v0.1 (cfe1f7aa…). Gueltig ist v1.0 mit SHA 6b7e7ba888e17cac80705097dd36be93a3ee6204b6ea00bd6be6f0b042bfe938 (FREEZE 18.09.2026). Die Liste bleibt unveraendert, die Ergaenzung steht in `00_doku/rm_2026-09-18_expected_shas.addendum_2026-10-01.txt`.

## 2026-10-01 — Offen (Stand nach Schritt 0, ersetzt die Liste «Offen» oben nicht, sondern schreibt sie fort)

- D2 Kapitalrahmen: Micro-Live-Betrag und Totalverlust-Obergrenze in CHF (Damian)
- D3 Zeitbudget: Stunden pro Woche und Review-Termin (Damian)
- D5 Bestaetigung Status Altsystem und Keys (Damian)
- D4 Steuern und Recht Schweiz vor Live (nicht blockierend fuer Forschung und Paper)
- D1 eigener Server (bis dahin Collector auf der Agent-Box)
- XS21 PiT v0.2: Pruefung des Entwurfs und der B7-Ausschlussliste vor dem Freeze (Claude/Damian), danach v1.0 und ein Lauf
- A1 bis A8: DT-Freeze vor dem P&L-Lauf
- Fehlende Original-Eingaben `kraken_funding/PF_{XBT,ETH,SOL}USD_funding.csv` und Original-DTB3

## 2026-10-01 — KORREKTURVERMERK zum E3-Korrekturvermerk «REBOUND-MICRO v1.0 Lauf BTC VERSIEGELT» (Review Claude zu XS21 v0.2, §4.3)

Der Satz «Massgeblich ist die Reihenfolge FREEZE vor Lauf.» im Korrekturvermerk vom 01.10.2026 wird durch folgenden Wortlaut ersetzt (der fruehere Vermerk bleibt unveraendert stehen):

Die Reihenfolge der Zeitstempel ist nicht belegbar. Massgeblich ist die SHA-Uebereinstimmung der Spezifikation im Lauf-Log mit dem Freeze (SHA 001a38534d87b2f8b37fc658df3a8268438c864368e191bc514d261f67bae328, `10_rebound_micro/rebound_micro_spec_v1.0.md`).

Befund dazu, offen vermerkt: Die Lauf-Logs `10_rebound_micro/run/BTC_run.log`, `XRP_run.log` und `DOT_run.log` sowie `BTC_eval.json` nennen die Spezifikation nur mit Dateinamen (`"spec": "rebound_micro_spec_v1.0.md"`), nicht mit SHA. Die SHA-Uebereinstimmung der Spezifikation ist damit **nicht belegt**. Belegt ist nur, dass die im Log genannten Code-SHAs mlib 6b7e7ba8… und simulate fef60859… mit den im FREEZE-Eintrag genannten v1.0-Dateien uebereinstimmen. Die aktuelle Datei `rebound_micro_spec_v1.0.md` hat die SHA aus dem FREEZE-Eintrag (001a3853…, geprueft 01.10.2026). Ab XS21 PiT v1.0 schreibt jeder Lauf die SHA der eingefrorenen Spezifikation ins Lauf-Log (Vorregistrierung XS21 v1.0 §7).

Umsetzung: Agent (Grok, 01.10.2026) nach Auftrag Damian. Neue ENTSCHEIDE-SHA in `00_doku/xs21v1_2026-10-01_expected_shas.txt`.

## 2026-10-01 — XS21 PiT v1.0 FREEZE-KANDIDAT (nicht eingefroren)

`01_forschung/09_lane_c/xs21_point_in_time_prereg_v1.0.md` setzt M1 bis M7 und die Zusatzpunkte aus dem Review Claude zu v0.2 (`xs21_point_in_time_v0.2_review_claude_v1.md`) sowie die Vorgaben Damian vom 01.10.2026 um (PAXG, XAUT, BTCDOM, DEFI, FOOTBALL, BLUEBIRD ausgeschlossen; USTC, FRAX, STABLE, STBL nach Pruefung zugelassen). B7-Liste v1.0 in `01_forschung/09_lane_c/xs21_pit_v1.0/` (220 Ausschluesse, 0 unklar). v0.1 und v0.2 bleiben unveraendert.

Status: wartet auf Freigabe Damian. Kein Freeze, kein Lauf, keine Datenbeschaffung.

## 2026-10-01 13:07 Europe/Zurich (11:07 UTC) — XS21 PiT v1.0 FREEZE

Freigabe: Damian, 01.10.2026, 13:07 Zuerich. Freigegeben sind `01_forschung/09_lane_c/xs21_point_in_time_prereg_v1.0.md` einschliesslich der drei Regelergaenzungen in §8.3 (M4 30-Tage-Ersatzmedian, M5 Blockzuordnung nach Einstiegsdatum und B1 ab Laufbeginn, M6 gemeinsames Cash von U1 und U2) und des Gate-Fensters M3 nach §8.2 (die ersten 8 Raster-Stichtage mit vollstaendigem 30-Tage-Median, 31.10. bis 19.12.2026).

Freeze-Dateien (SHA-256): Spezifikation v1.0 edb24cde8c391c60cd90fdad753f403a8835de7e4da275af0d5d3eed01e998af. B7-Liste v1.0: `xs21_pit_v1.0/xs21_exclusions_v1.0.csv` 7f68fe168c2de5a4…, Klassifikation 32e1a19da53270af…, Sensitivitaetsliste c0a8f32dfca2f47a…, Klassifikationscode `tools/xs21/exclusion_map_v1.0.py` 8a7f58cea160fcb8…, Builder `tools/xs21/build_exclusions_v1.py` eed6630a2b24e5d4…, Eingaben Snapshot bff906a0…, Spot-Liste 8dfa4293…, `binance_um_universe.csv` f5563c09…. Kostenmodell `config/cost_model_v1.json` c652caa5bb237914… (`stage2_perp` unveraendert). T-Bill `data/supplement/DTB3_3m_tbill_to_2026-09-14.csv` 8b287e3cc711b4c7…. Vollstaendige Liste: `00_doku/xs21_freeze_2026-10-01_expected_shas.txt`.

Zum Zeitpunkt des Freeze: kein Lauf, keine Outcomes, keine XS21-Kurs-, Volumen- oder Funding-Daten beschafft. Reihenfolge nach §7: Datenbeschaffung, Laufbeginn nach M6 (Eintrag hier vor dem Lauf), Freeze des Lauf-Codes (Eintrag hier vor dem Lauf), ein einziger Lauf. Das Lauf-Log muss die SHA der Spezifikation enthalten (E3).

Entscheid: eingefroren (Damian, 01.10.2026). Tag `xs21-pit-v1.0-freeze`.

## 2026-10-01 13:37 Europe/Zurich — XS21 PiT v1.0 Datenbeschaffung, Laufbeginn (M6) und Lauf-Code FREEZE (vor dem Lauf)

Datenbeschaffung nach §7, nur data.binance.vision (fapi geoblockt, nicht verwendet): 673 Symbole (USDT-Perps nach B7 v1.0), 20'547 Monats- und 9'660 Tages-Klines 1d, 19'956 Funding-Monatsdateien, alle mit CHECKSUM geprueft. Fehlend im Archiv: 1'264 Funding-Monate, davon 1'226 nach dem Handelsende (SETTLING) und 38 Symbol-Monate mit Handel (BNX 2022-04 bis 2023-01, ICP 2021-05 bis 2022-06, TLM 2021-07 bis 2022-06, JUP 2024-01, QTUM 2020-02); diese werden nach M4 gefuellt, falls gehalten. Provenienz  (0614ef23…), ZIP-Pruefsummen  (0dc79a6e…).

Befund vor dem Lauf: Das Archiv fuehrt delistete Symbole mit flachen Kerzen ohne Trades weiter (54'122 Kerzen). Umsetzungsfestlegung U5a: Kerzen mit count = 0 gelten als nicht vorhanden. Alle Umsetzungsfestlegungen in . Keine Regel der Spezifikation wird geaendert.

Laufbeginn nach M6, nur aus Listing und quote_volume bestimmt: **2020-04-04** (erster Stichtag mit |U1| >= 20, U1 = 21; vorher 3 bzw. 11 Symbole). Block B1 beginnt damit am 2020-04-04.

Lauf-Code FREEZE:  deca0c29…,  48370287…, Umsetzungsfestlegungen e81504aa…, Pruefskript  c1f16e6d…, Tests  3a521de7… (8 synthetische Tests, u.a. Lookahead, Delisting, M4, M6, ganzer Lauf-Pfad),  54590393… (Stufe 2, unveraendert). Vollstaendige Liste . Danach genau ein Lauf; das Lauf-Log enthaelt die SHA der Spezifikation (E3).

Umsetzung: Agent (Grok), Auftrag Damian vom 01.10.2026. Tag `xs21-pit-v1.0-runcode`.

## 2026-10-01 13:39 Europe/Zurich — KORREKTURVERMERK zu «XS21 PiT v1.0 Datenbeschaffung, Laufbeginn (M6) und Lauf-Code FREEZE»

Im Eintrag 13:37 fehlen durch einen Fehler beim Schreiben (Shell-Ersetzung von Backticks) die Dateinamen. Inhalt und SHAs sind unveraendert gueltig, der Eintrag bleibt stehen. Die fehlenden Namen, in Reihenfolge: Provenienz `01_forschung/09_lane_c/xs21_pit_v1.0/daten/xs21_provenance_v1.0.jsonl.gz` (0614ef23…), ZIP-Pruefsummen `01_forschung/09_lane_c/xs21_pit_v1.0/daten/xs21_zips_v1.0.sha256` (0dc79a6e…); Umsetzungsfestlegungen `01_forschung/09_lane_c/xs21_pit_v1.0/xs21_pit_umsetzung_v1.0.md`; Lauf-Code `01_forschung/09_lane_c/xs21_pit_v1.0/xs21_pit.py` (deca0c29…), `01_forschung/09_lane_c/xs21_pit_v1.0/xs21_pit_run.py` (48370287…), Pruefskript `tools/xs21/check_run_v1.py` (c1f16e6d…), Tests `tests/test_xs21_pit.py` (3a521de7…), `01_forschung/02_strategien/s2lib.py` (54590393…); vollstaendige Liste `00_doku/xs21_runcode_2026-10-01_expected_shas.txt`. Der Tag `xs21-pit-v1.0-runcode` zeigt auf den Commit mit dem eingefrorenen Code; dieser Vermerk folgt vor dem Lauf.

## 2026-10-01 13:55 Europe/Zurich — XS21 PiT v1.0 Lauf (einziger Lauf) und Urteil

Ein einziger Lauf von `01_forschung/09_lane_c/xs21_pit_v1.0/xs21_pit_run.py --lauf` mit dem eingefrorenen Code (Tag `xs21-pit-v1.0-runcode`), 01.10.2026 13:39:37 bis 13:43:45 Zuerich. Spec-SHA edb24cde8c391c60cd90fdad753f403a8835de7e4da275af0d5d3eed01e998af im Lauf-Log (E3). Kein Abbruch, keine Codeaenderung nach dem Freeze, keine Wiederholung. Evidenzklasse «Discovery/Robustheit mit Vorbelastung».

Urteile (Stufe-2-Regel, K1): U1 Top-3 L+S TEILWEISE (c3 verfehlt: B2 -0.085 % je Trade; c6 verfehlt: MaxDD -87.3 % gegen EP -53.5 %); CAGR 31.7 %, Sharpe 0.75, Holm-p 0.042. U2 Top-3 L+S TEILWEISE (c6 verfehlt: MaxDD -75.9 % gegen EP -52.0 %); CAGR 41.3 %, Sharpe 0.81, Holm-p 0.042. Lesart nach §5.3 (beide nicht bestanden): H-C2 auf PiT falsifiziert, kein Sleeve. Survivorship ist nicht der Grund (Fall «besteht nur mit Ueberlebenden» tritt nicht ein). Gefuelltes Funding unter 1 % je Bein, kein Vorbehalt.

Nachpruefung `tools/xs21/check_run_v1.py` (unveraendert): Bilanz und Brutto bitnah gleich; gemeldete Auswahl-Abweichungen (30/8) und Kostendifferenz vollstaendig erklaert durch U5a bzw. K2-Reibung bei 17/2 Delisting-Ausstiegen (`tools/xs21/check_run_v1_erklaerung.py`). Nachtrag: Survivorship-Zerlegung je Block (§5.3), deskriptiv aus den Trades (`tools/xs21/nachtrag_survivorship_bloecke_v1.py`), weil der Lauf-Code sie nur gesamt ausgab. Bericht `01_forschung/09_lane_c/xs21_pit_v1.0/xs21_pit_v1.0_bericht.md`. SHAs der Ausgaben: `00_doku/xs21_run_2026-10-01_expected_shas.txt` (u.a. Log f3fbd6bf…, Eval 66f3e97c…).

Offen fuer Damian: Umgang mit dem Gate M3 und dem Forward-Fenster nach diesem Urteil (die Spezifikation sieht ohne Sleeve-Kandidat keinen Paper-Betrieb vor).

## 2026-10-01 14:35 — DT P&L v1.0 FREEZE (vor jedem Outcome)

Freigabe Damian 01.10.2026, 14:20 Zuerich: Delayed Trend nach A1–A8 freezen und genau einen P&L-Lauf ausfuehren, Governance wie XS21. Spezifikation `01_forschung/11_delayed_trend/dt_pnl_spec_v1.0.md` (SHA 56a13bf7d434356539e956457e3616ea93a7ded4ea25f4247fd31380bf41d47a), Lauf-Code `01_forschung/11_delayed_trend/dt_pnl_v1.0/` (dt_pnl.py, dt_pnl_run.py), unabhaengige Pruefung `tools/dt/check_dt_pnl_v1.py`, Tests `tests/test_dt_pnl.py` (8 synthetische Tests, gruen). Alle SHAs: `00_doku/dt_pnl_freeze_2026-10-01_expected_shas.txt` (Libraries rlib f1ffdbb8…, dtlib f2d6c390…, ylib portabel 45261575…, Kostenmodell c652caa5…, 3 Discovery-Spot-Dateien, Kandidaten, count-JSON, eingefrorene DT-Einstiege).

Umsetzung: Primaer BTC S2xDT1, XRP S2xDT1, XRP S2xDT2; sekundaer BTC S2xDT2, DOT S2xDT1, DOT S2xDT2; Holm ueber 6. S1 nur deskriptiv, DT3 geschlossen. Exit Tages-ATR14-Chandelier 3x nur steigend, Zeitstopp t+360. Kontrollen: gematchte Kontexte (rlib.match_controls, Pool ylib.control_pool) mit Ersatzniveaus. Primaermetrik gepaartes Delta-R und Netto-K1 (Spot, C1/C2); Kraken-Venue-Modell nur berichtet, nicht entscheidend.

Festlegungen vor dem Lauf: (1) A4-Chandelier vom hoechsten Schluss seit Einstieg (Forschungsplan §5), ohne Strukturbruch-Regel. (2) A7 operationalisiert als Summe r_net K1 (R) ueber alle Trades der drei Primaerzellen; ungewichtetes Mittel der Zellenmittel nur berichtet.

A8 Evidenzvermerk (woertlich): «DT ist outcome-informed (Ebene C), laeuft auf denselben Discovery-Daten wie alle gescheiterten Vorgaenger, und die globale Trial-Zahl liegt bei rund 240. Ein positives Ergebnis gilt deshalb hoechstens als «mechanistically promising» in der Klasse Development. Ein Holdout-Lauf ist nur nach dem Economic Validation Gate zulaessig (Governance v1.1 §7), und dieser Vermerk wird im DT-Freeze woertlich uebernommen.»

A7 Abbruchregel (woertlich): «Vor dem DT-P&L-Lauf festgeschrieben: Ist Netto-K1 in den drei Primaerzellen zusammen kleiner als null, wird Lane A (Bottom, Reversal, Rebound, DT) vollstaendig geschlossen. Es folgt keine weitere Variante, keine Umformulierung und kein neuer Timeframe auf BTC, XRP oder DOT. Eine Wiederaufnahme waere nur mit neuen Daten (Forward-Fenster) und einer neuen Vorregistrierung zulaessig, die diesen Entscheid ausdruecklich zitiert.»

Nur Discovery-Daten (bis 2023-12-31); kein Holdout geoeffnet, auch nicht holdout_manifest. Kein DT-P&L-Ergebnis vor diesem Freeze gesehen.

## 2026-10-01 14:40 — DT P&L v1.0 Lauf (einziger Lauf) und Urteile

Einziger Lauf 01.10.2026 14:35:14–14:35:17 Zuerich, Freeze-Commit 2a94bf9 (Tag `dt-pnl-v1.0-freeze`), Spec-SHA 56a13bf7... im Log. Keine Abweichung von der Spezifikation, kein Neustart. Unabhaengige Pruefung `tools/dt/check_dt_pnl_v1.py`: gesamt_ok (Einstiege gleich Messung, Entscheidungskerzen vor Einstieg, Eine-Position-Regel, Exits und Kosten aller 6 Szenarien neu gerechnet bis 1e-14, 0 Matching- und 0 Ersatzniveau-Verletzungen, Holm und A7-Summe neu, Stoerungstest ab 2022-07-01: 0 von 190 Trades veraendert).

Urteile (K1 Spot, Holm ueber 6): BTC S2xDT1 n=30, dR 0.663 (26 Paare), K1 +0.148 R, Holm-p 0.345, kein Signal (status_v2 roh formal_supported, nach §9 und A8 nicht als Signal gewertet). XRP S2xDT1 n=35, dR -0.501 (26 Paare), K1 -1.023 R, Holm-p 0.835, no_evidence. XRP S2xDT2 n=37, K1 +0.619 R, 1 Paar, kein Test (insufficient sample). Sekundaer: BTC S2xDT2 n=40, K1 +0.409, 0 Paare; DOT S2xDT1 n=23, dR 0.265, K1 -0.147, Holm-p 0.398; DOT S2xDT2 n=33, K1 -0.173, 1 Paar. Keine Zelle mit Signal.

A7: Summe r_net K1 der drei Primaerzellen = -8.47 R ueber 102 Trades (-0.083 R je Trade; ungewichtetes Zellenmittel -0.085) < 0. Die Abbruchregel greift. Ausgaben-SHAs: `00_doku/dt_pnl_run_2026-10-01_expected_shas.txt` (Eval e1216bb8..., Log 3c09fa7e..., Pruefung 27ef4e56...). Bericht `01_forschung/11_delayed_trend/dt_pnl_v1.0/dt_pnl_v1.0_bericht.md`.

## 2026-10-01 14:40 — Lane A vollstaendig geschlossen (A7, mechanisch)

Ausloeser: DT P&L v1.0, Netto-K1 der drei Primaerzellen zusammen -8.47 R < 0 (Eintrag oben). Gemaess A7 (woertlich): «Vor dem DT-P&L-Lauf festgeschrieben: Ist Netto-K1 in den drei Primaerzellen zusammen kleiner als null, wird Lane A (Bottom, Reversal, Rebound, DT) vollstaendig geschlossen. Es folgt keine weitere Variante, keine Umformulierung und kein neuer Timeframe auf BTC, XRP oder DOT. Eine Wiederaufnahme waere nur mit neuen Daten (Forward-Fenster) und einer neuen Vorregistrierung zulaessig, die diesen Entscheid ausdruecklich zitiert.»

Lane A (Bottom, Reversal, Rebound, DT) ist damit vollstaendig geschlossen. Positive Einzelzellen (BTC S2xDT1, XRP S2xDT2, BTC S2xDT2) begruenden nach A7 keine Fortfuehrung. Kein Holdout-Lauf.

## 2026-10-01 15:45 — D3 Zeitbudget — ENTSCHIEDEN

Ersetzt den Eintrag «D3 Zeitbudget — OFFEN» (append-only, dieser Eintrag ist massgeblich). Entscheid Damian (uebermittelt 01.10.2026, 15:39 Zuerich, Korrektur 15:40): Damian setzt hoechstens 1 Stunde pro Woche ein. Der Review-Termin liegt hoechstens 4 Monate nach dem Start des Paper-Tradings (bei Start im Oktober 2026 also etwa Anfang Februar 2027). Kontext: Lane A geschlossen (A7), XS21 auf PiT falsifiziert, kein Sleeve; Paper-Plan W2, W6 und Turtle 55/20, Spot long, Kraken, Kosten K1. Folge fuer die Arbeitsweise: Vorschlaege an Damian muessen in dieses Budget passen (Entscheidvorlagen statt offener Fragen, keine laufende Betreuung).

## 2026-10-01 15:45 — XS21 PiT v1.0: Vermerke zur Nachpruefung

(1) Die eingefrorene Nachpruefung `tools/xs21/check_run_v1.py` endet mit `gesamt_ok: false` (`01_forschung/09_lane_c/xs21_pit_v1.0/run/xs21_check.json`). Ursachen, beide erklaert und kein Fehler im Lauf: (a) das Pruefskript wendet die Umsetzungsfestlegung U5a (Kerzen mit count = 0 gelten als nicht vorhanden) nicht an, daher 30 (U1) bzw. 8 (U2) gemeldete Auswahl-Abweichungen; mit U5a 0 Abweichungen; (b) die Kostendifferenz stammt aus der K2-Reibung bei 17 (U1) bzw. 2 (U2) Delisting-Ausstiegen. Erklaerung: `tools/xs21/check_run_v1_erklaerung.py`, `run/xs21_check_erklaerung.json`. Das Pruefskript bleibt unveraendert.
(2) Abweichung A6 des Berichts: Die Survivorship-Zerlegung je Block (§5.3) fehlte im Lauf-Code und wurde nach dem Lauf deskriptiv aus den Trades nachgetragen (`tools/xs21/nachtrag_survivorship_bloecke_v1.py`, `run/xs21_nachtrag_survivorship_bloecke.json`). Gesamtsummen gleich wie im Lauf, kein Einfluss auf das Urteil.

## 2026-10-01 15:55 — Paper-Trading-Umfang, XS21-Schattenrechnung, D1 (Vorschlag)

Grundlage: Review Claude zu XS21 PiT v1.0 (`01_forschung/09_lane_c/xs21_pit_v1.0/xs21_pit_v1.0_review_claude_v1.md`, von Damian am 01.10.2026 15:35 uebermittelt) und Auftrag Damian ueber den Haupt-Agenten.
(1) Paper-Trading = W2, W6 und Turtle 55/20, Spot long auf Kraken, Kosten K1. Vor dem Start ist eine Vorregistrierung (Freeze) Pflicht.
(2) XS21 wird nicht in den Papierhandel aufgenommen (Perps mit Short-Bein noetig, D4 offen, Gate B6 ohne Schwellen).
(3) U2 darf hoechstens als reine Schattenrechnung mitlaufen: oeffentliche Binance-Daten, keine Orders, auf Trade-Basis gerechnet, ohne Entscheidgewicht vor 12 Monaten.
(4) D1 (Ort des Runners): Vorschlag, der Paper-Runner laeuft auf der Agent-Box, ohne Keys und ohne Orders. NOCH NICHT von Damian bestaetigt; Bestaetigung ausstehend.

## 2026-10-01 22:15 — D1 Ort des Paper-Runners — ENTSCHIEDEN

Bestaetigung Damian 01.10.2026, 22:03 Zuerich (ueber den Haupt-Agenten): Der Paper-Runner laeuft auf der Agent-Box, ohne Keys und ohne Orders. Ersetzt den Vorschlag im Eintrag 15:55, Punkt (4). Damian hat den Agenten zudem als Chief Strategist eingesetzt (selbstaendige Fuehrung im Rahmen von Governance, D3 und den Entscheiden).

## 2026-10-01 22:15 — Vorfall: Holdout-Zeilen in Suchausgabe

Beim Suchen nach dem Begriff «07:35» im Repo (rg ohne Ausschluss von 02_daten/holdout) wurden 10 Zeilen aus `02_daten/holdout/validation/BTCUSDT_spot4h_validation.csv` (zufaellige 4h-Kerzen 2024-04 bis 2025-08, Treffer nur wegen der Ziffernfolge) in der Ausgabe angezeigt. Keine Auswertung, keine Kennzahl, keine Verwendung. Kein Einfluss auf PAPER_PREREG v1.0 (Paper nutzt Kraken-Live-Daten ab Startbar, Regeln aus Stufe 2 unveraendert). Massnahme: Suchen schliessen 02_daten/holdout und data/ kuenftig immer aus.

## 2026-10-01 22:15 — PAPER v1.0 FREEZE (vor dem ersten Paper-Signal)

Vorregistrierung `paper/PAPER_PREREG_v1.0.md` (SHA 626fd035f237713c510399381e27c8197ebfc646faafc92cd3dbb73a15664308), Engine `paper/paper_engine.py`, Tageslauf `paper/run_paper.py`, Tests `tests/test_paper.py` (22 gruen, u.a. Trade-fuer-Trade-Gleichheit W2/W6 mit dem eingefrorenen s2lib.run_trend auf Binance bis 2023 und Kraken-Live, Start flach, kein Look-ahead, Kosten, Luecken fail-closed, Revisionserkennung). Liste: `00_doku/paper_freeze_2026-10-01_expected_shas.txt`; der Runner prueft sie vor jedem Lauf fail-closed. Inhalt: W2, W6 (Stufe-2-Prereg §6/§10), Turtle 55/20 (Findings-Digest §2.1), Stufe-2-Universum 10 Coins, Spot long Kraken, Kosten venue_kraken maker_plan (= K1) primaer und taker_K2 als Sensitivitaet, 1'000 USD virtuell je Strategie und Coin, Start flach mit erstem Signalbar 2026-10-02 UTC, Review spaetestens 2027-02-02 (D3: Betrieb und Kosten, kein Leistungsurteil). Festlegungen F1 bis F6 in §2.4. XS21 nicht im Paper; U2-Schattenrechnung in v1.0 nicht umgesetzt (nicht guenstig). Kein Paper-Signal vor diesem Freeze.

## 2026-10-01 22:16 — Funding-Carry (Spot long + Perp short, Kraken, BTC/ETH) VERWORFEN

Entscheid Damian 01.10.2026, 22:16 Zuerich (uebermittelt ueber den Haupt-Agenten): Der delta-neutrale Funding-Carry wird nicht weiterverfolgt. Der Entwurf `01_forschung/13_carry/carry_prereg_v0.9.md` wird mit Status «VERWORFEN (Entscheid Damian 2026-10-01 22:16), nicht eingefroren, nicht gelaufen» abgelegt. Kein Freeze, kein Lauf, kein Review, kein Paper. D-CC bleibt nach F1 hoechstens Forward-Datensammlung (Collector), ohne Sleeve.

Deklaration der Vorbelastung (verbindlich fuer jede Wiederaufnahme, die nur mit neuer Vorregistrierung und unter Zitat dieses Eintrags zulaessig ist):
(1) Informelle Trials: Ideen-Scan v1 (01.10.2026) mit rund 20 informellen Trials, darunter Carry dauerhaft 1.5x Kapital je Jahr und Filter f_7d > 0 fuer BTC/ETH/SOL auf Binance-Funding 2020 bis 2023. Globale Trial-Zahl damit rund 260.
(2) Formale Vortests: Stufe 2 D-CC (16.09.2026) auf Binance-Funding 2020-01 bis 2026-09-14 inklusive Jahresrenditen 2024 bis 2026; nach B5 ist 2024+ fuer D-CC verbraucht.
(3) Kraken-Funding-Exposition: Strategiebewertung 15.09.2026 (PF_XBTUSD 10.09.2025 bis 30.06.2026 +2.69 %, ETH +3.05 % p. a.), Kraken-Gegenprobe Stufe 2 (349 Tage), sowie die Machbarkeitsstudie `/workspace/aurum2/fuer_aurum/andreas_carry_machbarkeit_v1.md` (Eingang 22:15) mit echten Kraken-Reihen PF_XBTUSD/PF_ETHUSD 2022-03-22 bis 2026-10-01 und deren Jahres- und Gesamtstatistik (u.a. BTC 2024 +16.5 %, gesamt +8.1 %; ETH 2022 -17.0 %, gesamt +4.0 % p. a.). Diese Werte gelten als gesehen; Kraken-Funding 2022 bis 2026-10-01 ist fuer Carry-Hypothesen kein unabhaengiger Testzeitraum mehr. Provenienz geprueft: Kraken-Support-ZIP (SHA 65ba6712a6ab6573...) und gelieferte CSV identisch auf 30'431 Stunden, Collector identisch auf 9'091 Stunden.
Keine Strategie-Rendite mit den Regeln des Entwurfs wurde berechnet.

## 2026-10-01 22:35 — Ideen-Scan v2: Deklaration informeller Trials, zwei Prereg-Entwuerfe (nicht eingefroren)

Auftrag Damian (ueber Haupt-Agenten, nach Carry-Verwerfung 22:16): zweite Strategiesuche fuer das Privatkonto (Spot long, <= 1 h/Woche, ohne Derivate). Ergebnis `01_forschung/14_ideen_scan_v2/ideen_scan_v2.md`. Explorativ nur auf Daten < 2024 (Binance Spot BTC/ETH 1d, CoinMetrics Community, alternative.me Fear & Greed, DefiLlama Stablecoins, FRED), Skript `tools/ideen/explorativ_scan_v2.py`, Rohdaten-Pruefsummen `01_forschung/14_ideen_scan_v2/rohdaten_SHA256SUMS.txt`. 10 informelle Trials (t1 bis t10: MVRV-Band, SMA200+MVRV-Bremse, Exchange-Bestand, Stablecoin-Wachstum, Fear & Greed, DXY, Fed-Netto-Liquiditaet, ETH/BTC-Rotation, Dual Momentum, Inverse-Vol). Globale Trial-Zahl damit rund 270. ETH < 2024 erneut verwendet (wie Scan v1); ETH gilt nur ab 2024 als unberuehrt. Keine MVRV- oder Makro-Signalwerte ab 2024 abgerufen oder berechnet; der grobe BTC- und Fed-Bilanz-Pfad 2024 bis 2026 ist als Marktwissen bekannt (Kontext-Vorbelastung). Holdout nicht beruehrt.
Entwuerfe (Status ENTWURF, nicht eingefroren, nicht gelaufen): `makro_liq_prereg_entwurf_v0.1.md` (Fed-Netto-Liquiditaet 13 Wochen, BTC Spot/Cash) und `mvrv_prereg_entwurf_v0.1.md` (MVRV 1.0/3.5, BTC Spot/Cash, Testbarkeit gering). Freeze nur nach Review Claude und Entscheid Damian. NO-GO ohne weitere Arbeit: Exchange-Flows, Stablecoin-Wachstum, Fear & Greed, BTC-Dominanz, ETH/BTC-Rotation, Dual Momentum, Inverse-Vol, Listing/Unlock, Kurzfrist-MR.

## 2026-10-01 22:40 — Ideen-Scan v2: MAKRO_LIQ (A) und MVRV (B) nur als Forward-Paper weiterverfolgen

Entscheid Chief Strategist 01.10.2026, 22:40 Zuerich; Veto Damian vorbehalten. Beide Entwuerfe werden weiterverfolgt, aber ausschliesslich als Forward-Paper (zusaetzliche Sleeves BTC Spot Kraken, Kosten venue_kraken maker_plan = K1, Pflicht-Sensitivitaet taker_K2, eigener Runner und eigene Freeze-Liste; `paper/` und die Freeze-Liste paper-v1.0-freeze bleiben unveraendert). 2024 bis 2026 zaehlt wegen Kontext-Vorbelastung (Marktwissen ueber BTC- und Fed-Bilanz-Pfad) NICHT als Testfenster; zulaessig ist hoechstens ein einmaliger deskriptiver Anhang ohne Entscheidungsgewicht. Entwuerfe auf v0.2 nachgefuehrt: `01_forschung/14_ideen_scan_v2/makro_liq_prereg_v0.2.md` und `mvrv_prereg_v0.2.md` (Datenquellen CoinMetrics Community und FRED WALCL/WTREGEN/RRPONTSYD mit Publikationsverzug, First-Release-As-of ueber Collector-Schnappschuss, kein Look-ahead; Betriebs-Review 2027-02-02 zusammen mit PAPER v1.0, danach jaehrlich im Oktober, ohne Leistungsurteil; Langfrist-Auswertung A fruehestens nach 3 Jahren und 10 Wechseln, spaetestens 2031-10-01; B nach erstem vollem Zyklus, spaetestens 2030-12-31, sonst nicht pruefbar und geschlossen). Status: ENTWURF, nicht eingefroren, nicht gelaufen. Freeze erst nach Review Claude (Auftrag `/workspace/aurum2/fuer_claude/an_claude_scan_v2.md`), ohne Veto Damian und nach Bau und Test von Runner und Collector-Erweiterung. Kein neuer Trial.

## 2026-10-01 22:50 — Sleeves A/B: Infrastruktur gebaut, NICHT eingefroren, NICHT gestartet

Collector 1.2 (`collector/macro_sources.py`, Quellen `coinmetrics_mvrv` und `fred_macro`, First-Release mit Abrufzeit UTC, Revisionen nur protokolliert, Rohantworten mit SHA256) laeuft ab sofort im bestehenden 06:15-Lauf mit. Runner `sleeves/run_sleeves.py` (Ausgabe `/workspace/aurum2/paper_sleeves/`) ist gesperrt (`sleeves/sleeves_config.json` enabled=false, Exit 3) und nicht in cron; Freigabe erst nach Freeze von MAKRO_LIQ/MVRV. Tests `tests/test_collector_macro.py`, `tests/test_sleeves.py`. `paper/` unveraendert.
Deklaration: Beim ersten Abruf (01.10.2026 22:47 Zuerich) wurden aktuelle Werte gesehen: BTC MVRV 2026-09-30 1.559 (Sept. 2026 rund 1.52 bis 1.62), WALCL 2026-09-30 6'743'031, WTREGEN 948'674, RRPONTSYD 2026-10-01 0.350 (2026-09-30 11.539), DTB3 4.03. Kein Signal- oder Renditeverlauf 2024 bis 2026 berechnet; das 13-Wochen-Signal von A wurde nicht ausgewertet. Ein Dry-Run (separates Verzeichnis `/workspace/aurum2/work/sleeves_dryrun`, Startbar 2026-09-30) bestaetigte nur die As-of-Sperre (B mangels vorher abgerufener Daten STOPPED, A ohne Freitagsbar).
