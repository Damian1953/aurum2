# Lane C — Datenbefund: Kraken-Futures-Funding und Binance-UM-Universum, Version 1

**Project Aurum II, `02_daten/lane_c_datenbefund_v1.md`. 17.09.2026. Ergebnis des Loaders `nachladen_lane_c.py` v1.1 (SHA 17c8f2fc…), Lauf 21:27 bis 21:44 UTC auf dem Mac. Ausschliesslich Historientiefe und Abdeckung, keine Strategiezahlen, keine Outcomes. Protokoll `raw/nachladen_lane_c.log` (SHA 046a0edb…), Herkunft `raw/provenance_lane_c.json` (SHA 61a6d102…).**

## 1. Kraken-Futures-Funding (Weg K1, kostenloser Endpunkt)

15 Symbole abgefragt, 14 aktiv: PF_XBTUSD, PF_ETHUSD, PF_SOLUSD, PF_XRPUSD, PF_ADAUSD, PF_AVAXUSD, PF_LINKUSD, PF_DOTUSD, PF_BNBUSD, PF_LTCUSD sowie PI_XBTUSD, PI_ETHUSD, PI_XRPUSD, PI_LTCUSD. Jedes liefert 8764 bis 8766 Settlements von 2025-09-17 08:00 bis 2026-09-17 21:00 UTC im Stundenraster, mit vereinzelten 2h- und 3h-Lücken. PI_BCHUSD ist tot (ein Eintrag vom 2025-04-04). Zwei Läufe im Abstand von zwei Stunden (19:09 und 21:27 UTC) zeigen dasselbe Startdatum 2025-09-17 08:00 bei fortlaufendem Ende, der Endpunkt ist also ein rollendes Fenster von exakt einem Jahr, das täglich vorne abschneidet. Historie vor September 2025 ist über diesen Weg nicht erreichbar, weder über den Loader noch über CCXT (`krakenfutures`), das dieselbe API nutzt.

Konsequenz: Die Kraken-Funding-Lücke für D-CC (benötigt ab mindestens 2023-09, besser ab Kontraktbeginn) bleibt bestehen. Weg K2 (ein Monat CoinGlass Startup, 79 USD, mit Pflichtabgleich auf dem Überlappungsfenster ab 2025-09) ist damit der empfohlene nächste Schritt, sobald die D-CC-Kraken-Vorregistrierung geschrieben ist. Unabhängig davon sollte der Loader ab jetzt monatlich laufen und die 15 Reihen fortschreiben, weil jeder Tag ohne Sicherung am Anfang des Fensters verloren geht. Felder: `t`, `fundingRate` (absolut, in Quote je Kontrakt), `relativeFundingRate` (Anteil, für D-CC massgebend, vergleichbar mit Binance-Rate nach Umrechnung 1h zu 8h).

## 2. Binance-UM-Universum (Weg U1, S3-Listing)

1018 Symbole im Archiv `data/futures/um/monthly/klines/`, 1014 ausgewertet, 4 mit Nicht-ASCII-Namen übersprungen (chinesische Meme-Ticker aus 2025/2026, für XS21 irrelevant und protokolliert). Datei `raw/binance_um_universe.csv` (SHA f5563c09…) mit Symbol, erstem und letztem Monat mit Tages-Klines, Anzahl Monate, heutigem Status aus `exchangeInfo`. Status heute: 748 TRADING, 130 SETTLING, 136 NOT_LISTED, zusammen 266 nicht mehr handelbar.

Survivorship-Bias, den XS21 in Stufe 2 getragen hat, beziffert am Stichtag: Ende 2020 waren 80 Symbole handelbar, davon sind heute 22 nicht mehr TRADING (28 Prozent), Ende 2021 150 und 57 (38 Prozent), Ende 2022 199 und 88 (44 Prozent), Ende 2023 298 und 120 (40 Prozent), Ende 2024 403 und 104 (26 Prozent), Ende 2025 656 und 141. 81 Symbole wurden bis Ende 2023 delistet und fehlten in der Stufe-2-Rechnung vollständig. Das Point-in-Time-Universum ist damit verfügbar: Zum Stichtag M gehört jedes Symbol mit `first_month` ≤ M ≤ `last_month`, die Klines der delisteten Symbole liegen im selben Archiv und werden mit dem bestehenden 4h- und 1d-Loader nachgeladen, sobald die XS21-Vorregistrierung die Liste festlegt.

Grenze, ausgewiesen: Das Monatsarchiv beginnt 2020-01, obwohl Binance-UM-Perps ab September 2019 gehandelt wurden. Für 2019 gibt es keine Point-in-Time-Liste aus dieser Quelle, XS21 startet deshalb frühestens 2020-01 (Stufe 2 begann ohnehin später). Der Loader liefert Handelbarkeit, nicht Liquidität, der Vormonats-Dollar-Umsatz aus den Klines bleibt das Selektionskriterium.

## 3. Was daraus folgt

Lane C hat beide Datenfragen beantwortet, ohne Geld auszugeben: Für XS21 ist das Universum vollständig und kostenlos, die Point-in-Time-Vorregistrierung kann geschrieben werden. Für D-CC bleibt die Kraken-Historie die einzige Lücke, sie kostet nach Weg K2 unter 100 USD. Beide Vorregistrierungen folgen in Woche 2 der Roadmap v1.1, parallel zu den XRP- und DOT-Berichten. Keine D-CC- oder XS21-Outcomes werden gerechnet, bevor die jeweilige Validation-Vorregistrierung eingefroren ist.
