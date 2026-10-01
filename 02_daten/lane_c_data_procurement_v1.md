# Lane C — Datenbeschaffung: Kraken-Futures-Funding und Point-in-Time-Universum, Version 1

**Project Aurum II, `02_daten/lane_c_data_procurement_v1.md`. 17.09.2026. Zweck: Kosten und Nutzen der Beschaffungswege für die zwei Lane-C-Lücken (Kraken-Funding-Historie für D-CC, Delisting-Universum für XS21) mit Empfehlung. Keine Outcomes, keine Änderung an den Stufe-2-Ergebnissen. Lane C läuft parallel zu XRP und DOT.**

## 1. Was fehlt und wofür

D-CC (Funding-Carry, Stufe 2 bestanden mit Datenvorbehalt) wurde auf Binance-Funding gerechnet. Für die Validation auf Kraken fehlt die Kraken-Futures-Funding-Historie vor 2025-09, also der Nachweis, dass das Vorzeichen und die Höhe des Carry auf dem Ausführungsplatz mit Binance übereinstimmen (Stufe 2: Vorzeichenübereinstimmung 79 bis 88 Prozent auf dem kurzen vorhandenen Fenster). Benötigt wird eine 8h- oder 4h-Funding-Reihe je Kraken-Perp (PF_XBTUSD, PF_ETHUSD, PF_XRPUSD, PF_DOTUSD, PF_SOLUSD und die übrigen fünf Coins des D-CC-Universums) über mindestens zwei Jahre, besser seit Beginn der Kraken-Perps (PI-Kontrakte ab 2018 bis 2019, PF-Kontrakte ab 2021 bis 2022). Tick-Daten sind nicht nötig, Funding wird stündlich beziehungsweise pro Settlement gebucht.

XS21 (Cross-sectional, Stufe 2 bestanden mit Survivorship-Vorbehalt) wurde auf dem heutigen Binance-UM-Universum gerechnet. Für die Point-in-Time-Vorregistrierung fehlt die Liste aller Symbole, die zu jedem Monatsstichtag handelbar waren, einschliesslich der seither delisteten, und ein Rang- oder Grössenkriterium zum Stichtag, das keine spätere Information verwendet.

## 2. Wege für die Kraken-Funding-Historie

**Weg K1, Kraken-Futures-Endpunkt, kostenlos, offiziell.** `GET https://futures.kraken.com/derivatives/api/v3/historical-funding-rates?symbol=PF_XBTUSD` liefert ohne Schlüssel Zeitstempel, Funding-Rate und relative Funding-Rate je Settlement. Die Tiefe ist nicht dokumentiert. Der Loader `nachladen_lane_c.py` (Launcher `Daten-Lane-C.command`) fragt alle PF- und PI-Symbole ab, schreibt je Symbol eine CSV nach `raw/kraken_futures_funding/`, protokolliert erste und letzte Zeit sowie das Intervall und legt `raw/provenance_lane_c.json` an. Kosten: null, ein Lauf von wenigen Minuten. Nutzen: Falls die Tiefe zwei Jahre oder mehr beträgt, ist die Lücke geschlossen. Risiko: Die Tiefe könnte auf einige Monate begrenzt sein, dann bleibt der Weg als laufende Sammlung ab heute nützlich, löst das Historienproblem aber nicht.

**Weg K2, CoinGlass API, 29 bis 79 USD je Monat.** Aggregator mit Kraken unter den unterstützten Futures-Börsen, Funding- und OI-Historie auf Tages- und 8h-Basis, laut Preisseite «all-time» für Tagesintervalle in allen bezahlten Stufen, für kürzere Intervalle nach Stufe begrenzt. Ein bis zwei Monate Hobbyist (29 USD) oder Startup (79 USD) genügen, um die Historie einmal zu ziehen und mit Weg K1 auf dem überlappenden Fenster zu vergleichen. Kosten: 29 bis 160 USD einmalig. Nutzen: schliesst die Lücke wahrscheinlich für 2021 bis 2025, Aggregator-Daten ohne Primärnachweis. Risiko: Die tatsächliche Kraken-Tiefe bei CoinGlass ist vor dem Kauf nicht einsehbar, ein Testmonat klärt das. Mittel: Abgleich mit K1 auf dem Überlappungsfenster als Pflicht, Abweichungen über 1 Basispunkt je Settlement werden protokolliert.

**Weg K3, Tardis.dev, 700 bis 3000 USD je Monat.** Primärdaten (Websocket-Mitschnitt) für Kraken Futures ab 2019-03-30, Kanal `derivative_ticker` mit Funding, OI, Mark- und Indexpreis. Kein Einzelbörsen-Plan mehr, kein Einmalkauf fester Zeiträume. Monatliche Abrechnung schaltet nur vier Monate Historie frei, das nützt nichts. Jahresabrechnung Solo (700 USD je Monat, 8400 USD je Jahr) schaltet vier Jahre frei (ab etwa 2022-09), nur Business (3000 USD je Monat, 36000 USD je Jahr) die volle Historie. Kosten: 8400 bis 36000 USD. Nutzen: Primärqualität, zusätzlich Tick-Daten für spätere Ausführungsmodelle (Spread, Book-Tiefe auf Kraken), die für die Slippage-Annahmen K1 und K2 nützlich wären. Risiko: Kosten stehen in keinem Verhältnis zu einem Sleeve, das noch nicht validiert ist.

**Weg K4, Amberdata, Kaiko, CoinAPI.** Institutionelle Anbieter, Preise auf Anfrage, üblicherweise vierstellig je Monat, für Kraken-Futures-Funding nicht besser als K3. Nicht weiter verfolgt.

## 3. Wege für das Point-in-Time-Universum

**Weg U1, Binance Vision S3-Listing, kostenlos, offiziell.** Das Bucket `data.binance.vision` listet unter `data/futures/um/monthly/klines/` jedes Symbol, das je Tages-Klines hatte, einschliesslich delisteter, mit erstem und letztem Monat. Der Loader schreibt `raw/binance_um_universe.csv` mit Symbol, erstem und letztem Monat und dem heutigen Status aus `exchangeInfo`. Das ergibt die Liste «wer war zu Monat M handelbar» ohne Survivorship. Kosten: null. Grenze: Kein Grössen- oder Liquiditätsrang zum Stichtag, den liefert man aus den Klines selbst (Dollar-Volumen des Vormonats aus `quote_volume`), was point-in-time ist und in XS21 ohnehin als Liquiditätsfilter dient.

**Weg U2, CoinMarketCap-Historienseiten, kostenlos.** Wöchentliche Ranglisten nach Marktkapitalisierung seit 2013 als Webseiten, per Skript lesbar, für ein Marktkapitalisierungs-Kriterium zum Stichtag. Kosten: null, Aufwand einige Stunden, Nutzungsbedingungen prüfen. Nutzen: nur nötig, wenn XS21 nach Marktkapitalisierung statt nach Dollar-Volumen selektiert. Die XS21-Spezifikation aus Stufe 2 verwendet Volumen, deshalb zunächst nicht nötig.

**Weg U3, CoinGecko oder CMC API, 129 bis 300 USD je Monat.** Historische Marktkapitalisierung je Coin per API. Nur bei Bedarf nach Weg U2.

## 4. Empfehlung

Sofort und kostenlos: `Daten-Lane-C.command` auf dem Mac ausführen. Das liefert die Kraken-Funding-Tiefe (Weg K1) und das Universum (Weg U1) in einem Lauf. Erst der Befund entscheidet über Geld.

Wenn K1 mindestens bis 2023-09 zurückreicht: Kein Kauf. D-CC-Validation auf Kraken kann vorregistriert werden, sobald XRP und DOT gezählt sind. Wenn K1 kürzer ist: Einen Monat CoinGlass Startup (79 USD, wegen 8h-Intervall) kaufen, Kraken-Funding für die zehn Coins ziehen, mit K1 auf dem Überlappungsfenster abgleichen, Abgleichprotokoll in `raw/provenance_lane_c.json` ergänzen, danach kündigen. Gesamtkosten unter 100 USD. Tardis (K3) wird nicht empfohlen, solange kein Lane-C-Sleeve die Holdout-Validation bestanden hat. Sollte später ein Ausführungsmodell auf Kraken-Tick-Daten nötig werden, ist Tardis Solo mit Jahresabrechnung (vier Jahre Historie) die erste Wahl, das ist eine Entscheidung nach der Validation, nicht davor.

Für XS21: Weg U1 genügt für die Point-in-Time-Vorregistrierung. Selektion nach Vormonats-Dollar-Volumen aus den Klines, Universum aus der S3-Liste zum Stichtag, delistete Symbole bleiben bis zu ihrem letzten Monat im Universum. Marktkapitalisierung (U2, U3) wird nicht beschafft.

## 5. Reihenfolge mit XRP und DOT

Lane C blockiert nichts in Lane A. Der Loader-Lauf dauert Minuten, die Auswertung der Tiefe eine Stunde. Die D-CC-Kraken-Vorregistrierung und die XS21-Point-in-Time-Vorregistrierung werden in Woche 2 der Roadmap v1.1 geschrieben, parallel zu den XRP- und DOT-Berichten, und in Woche 3 gerechnet. Beide sind Stufe-2-Fortsetzungen mit bereits bestandener Discovery, ihre Evidenzklasse ist nach dem Kraken-Lauf «Holdout validation» oder «no evidence», nicht «Development», weil die Regeln vor Sicht auf Kraken-Daten eingefroren wurden.
