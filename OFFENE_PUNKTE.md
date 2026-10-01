# Offene Punkte (beim Aufräumen gefunden, bewusst NICHT aufgelöst)

Stand 01.10.2026. Hier wird nichts stillschweigend korrigiert: Die eingefrorenen Dateien bleiben unverändert. Jeder Punkt braucht einen Entscheid von Damian und danach einen Eintrag in `00_doku/ENTSCHEIDE.md`.

## OP-1 Gebührenwiderspruch 05_evidenz ↔ ENTSCHEIDE ↔ Kostenmodell

| Quelle | Spot Maker | Spot Taker | Perp Maker | Perp Taker |
|---|---|---|---|---|
| `05_evidenz/README.md` (Szenarien optimistisch/mittel/konservativ) | 0.16 / 0.25 / 0.35 % | 0.26 / 0.40 / 0.55 % | – | 0.05 / 0.075 / 0.10 % |
| `00_doku/ENTSCHEIDE.md` Z. 33 (Kraken Fee Schedule, 15.09.2026), ebenso `05_evidenz/kostenhuerde_teil1.py` | 0.40 % | 0.80 % | 0.02 % | 0.05 % |
| `config/cost_model_v1.json` `spot_r` (= eingefrorene `ylib`/`mlib`/`mtp_val`) | K0 0.16 % · K1 0.40 % (+0.02 % Reibung, +5/10 bp Slippage) · K2 0.80 % (+0.06 %, +15/30 bp) | | | |
| `config/cost_model_v1.json` `stage2_perp` | | | | K0 0.02 % · K1 0.05 % · K2 0.10 % |

Widersprüche:
- Laut ENTSCHEIDE ist K1 (0.40 %) der Spot-**Maker**-Tarif von Kraken Tier 1. Der REBOUND-MICRO-Entscheid (3) vom 18.09.2026 sagt aber «K1 alleiniger Primary-Kostenmassstab, **keine Maker-Gutschrift**». Mit Taker-Ausführung wäre K1 nach ENTSCHEIDE 0.80 % (= K2). Nach 05_evidenz wäre 0.40 % dagegen der *mittlere Taker*.
- Die Tabelle in 05_evidenz passt zu keinem dokumentierten Kraken-Tier (eher zu Tier 2/3 oder einer anderen Börse). Eine Quelle fehlt.
- Folge: Alle Spot-R-Ergebnisse (Lane A, Rebound, MTP-Validation, DT-Gate B «K1-Kosten ≤ 0.40 R») hängen davon ab, wie K1 gelesen wird. Bei Taker 0.80 % wären die Kosten je Roundtrip etwa 1.8-mal so hoch.

Entscheid nötig: Welche Quelle gilt, und ist K1 Spot Maker oder Taker? Danach `cost_model_v2.json` mit neuem ENTSCHEIDE-Eintrag. Die eingefrorenen Ergebnisse bleiben, wie sie sind.

## OP-2 «Perps statt Spot» beschlossen, Lane A mit Spot-Kosten gerechnet

ENTSCHEIDE (15.09.2026) legt Strategien mit Umschlag auf die Perp-Seite, weil Perps 16- bis 20-mal billiger sind. `spot_r` (Lane A, YAMATO, Rebound, DT) rechnet trotzdem mit Spot-Gebühren. Funding fehlt in `spot_r` ganz. Ein Perp-R-Kostenmodell (Fee + Funding über die Haltedauer) gibt es nicht. Zu klären: ist das gewollt (konservativ) oder ein Versäumnis?

## OP-3 Kostenkopien ausserhalb des zentralen Modells

Die eingefrorenen Dateien `ylib.py`, `mlib.py`, `mtp_val.py`, `s2lib.py`, `spot_ref.py` sowie die abgeleiteten Basispunkte in `dtlib.py` (99 bp/89 bp) behalten ihre eigenen Kopien. Die portablen Versionen laden aus `config/cost_model_v1.json`. Für `dtlib` gibt es keine portable Version, die bp-Werte sind nur per Test (`tests/test_cost_model.py`) an das Modell gebunden. Die Tests der Original-Testdateien enthalten Kostenwerte als Literale. `05_evidenz/kostenhuerde_teil*.py` rechnen mit eigenen Tarif-Tabellen (Illustration, nicht zentralisiert).

## OP-4 Fehlende Eingaben in der Projektkopie

- `02_daten/raw/.../DTB3_3m_tbill.csv` fehlte. Ersatz: FRED neu geladen und bei 2026-07-15 abgeschnitten (`data/supplement`). Die SHA weicht ab (`085e8e38…` statt `26129de6…`), die Stufe-2-Reproduktion ist trotzdem bitgleich. Das Original sollte trotzdem ins Archiv.
- `kraken_funding/PF_{XBT,ETH,SOL}USD_funding.csv` (Eingaben laut `stage2_results.json`, Kraken-Gegenprobe/`spot_ref.py`) fehlen. Der Collector (`collector/`) sammelt diese Reihen ab jetzt neu. Das Kraken-Fenster reicht aber nur rund 1 Jahr zurück, die historische Strecke ist ohne Original nicht wiederherstellbar.

## OP-5 Zeitstempel in ENTSCHEIDE.md

«2026-09-18 14:35 UTC — REBOUND-MICRO v1.0 Lauf BTC VERSIEGELT» liegt zeitlich **vor** «2026-09-18 14:40 UTC — REBOUND-MICRO v1.0 FREEZE». Nach Governance muss der Freeze vor jedem Lauf stehen. Vermutlich ein Tippfehler oder eine nachträgliche Protokollierung, das ist zu bestätigen.

## OP-6 Binance von dieser Box geoblockt

`fapi.binance.com` antwortet von der Box mit HTTP 451. Nach Vorgabe gibt es keinen Proxy und keinen Ausweich-Endpunkt. Der Collector nutzt `data.binance.vision`:
- Funding: Monats-ZIPs mit Prüfsumme, Verzug bis ein Monat.
- Universum: S3-Listing der Daily-Kline-Ordner, «aktiv» heisst: gestern oder vorgestern gibt es eine 1d-Kline-Datei.

Das ist kein echtes `exchangeInfo`: Listing-Datum, Status und Kontrakttyp fehlen. Entscheid nötig, ob das reicht oder ob die Binance-Sammlung von einem nicht geblockten Rechner aus laufen soll (z.B. Damians Mac).

## OP-7 Expected-SHA-Liste rm_2026-09-18

Sie nennt `mlib.py` noch als v0.1 (`cfe1f7aa…`), die Datei ist v1.0 (`6b7e7ba8…`). Die Abweichung ist in `tools/frozen_allowlist.txt` begründet. Eine nachgeführte Liste wäre sauberer, als neue Datei und nicht als Überschreibung.
