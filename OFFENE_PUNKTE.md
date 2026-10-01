# Offene Punkte (beim Aufräumen gefunden, bewusst NICHT aufgelöst)

Stand 01.10.2026, nachgeführt nach den Schritt-0-Entscheiden (ENTSCHEIDE 2026-10-01). Hier wird nichts stillschweigend korrigiert: Die eingefrorenen Dateien bleiben unverändert. Jeder Punkt braucht einen Entscheid von Damian und danach einen Eintrag in `00_doku/ENTSCHEIDE.md`.

## OP-1 Gebührenwiderspruch 05_evidenz ↔ ENTSCHEIDE ↔ Kostenmodell — ERLEDIGT durch C2 (01.10.2026)

**Auflösung:** ENTSCHEIDE C2 übernommen. Gültig sind die Kraken-Tier-1-Sätze aus ENTSCHEIDE (Spot 0.40 % Maker / 0.80 % Taker, Futures 0.02 % / 0.05 %), jetzt als `venue_kraken` in `config/cost_model_v1.json` v1.1. Spot-Long wird mit Maker geplant, Taker mindestens unter K2 gerechnet. Die Sätze in 05_evidenz sind per `05_evidenz/README_v1.1_gebuehren.md` korrigiert (Original unverändert). Die eingefrorenen K0/K1/K2 bleiben. **Rest für Review (Claude):** (a) Der REBOUND-MICRO-Entscheid (3) sagt «keine Maker-Gutschrift», K1 ist aber nach C2 der Maker-Satz. Das sollte als Lesart vermerkt werden, ohne Umetikettierung. (b) Stops sind Market-Orders und zahlen Taker. Das Szenario `maker_entry_taker_stop` ist nur Entwurf.

Ursprünglicher Befund:

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

## OP-2 «Perps statt Spot» beschlossen, Lane A mit Spot-Kosten gerechnet — ERLEDIGT durch C1 (01.10.2026)

**Auflösung:** Spot für die Long-Seite, Perps nur für ein Short-Bein (XS21) oder ein Carry-Bein (D-CC). «Perps statt Spot» ist damit präzisiert. Lane A mit Spot-Kosten ist konsistent, ein Perp-R-Modell ist für Lane A nicht nötig.

Ursprünglicher Befund:

ENTSCHEIDE (15.09.2026) legt Strategien mit Umschlag auf die Perp-Seite, weil Perps 16- bis 20-mal billiger sind. `spot_r` (Lane A, YAMATO, Rebound, DT) rechnet trotzdem mit Spot-Gebühren. Funding fehlt in `spot_r` ganz. Ein Perp-R-Kostenmodell (Fee + Funding über die Haltedauer) gibt es nicht. Zu klären: ist das gewollt (konservativ) oder ein Versäumnis?

## OP-3 Kostenkopien ausserhalb des zentralen Modells

Die eingefrorenen Dateien `ylib.py`, `mlib.py`, `mtp_val.py`, `s2lib.py`, `spot_ref.py` sowie die abgeleiteten Basispunkte in `dtlib.py` (99 bp/89 bp) behalten ihre eigenen Kopien. Die portablen Versionen laden aus `config/cost_model_v1.json`. Für `dtlib` gibt es keine portable Version, die bp-Werte sind nur per Test (`tests/test_cost_model.py`) an das Modell gebunden. Die Tests der Original-Testdateien enthalten Kostenwerte als Literale. `05_evidenz/kostenhuerde_teil*.py` rechnen mit eigenen Tarif-Tabellen (Illustration, nicht zentralisiert).

## OP-4 Fehlende Eingaben in der Projektkopie

- `02_daten/raw/.../DTB3_3m_tbill.csv` fehlte. Ersatz: FRED neu geladen und bei 2026-07-15 abgeschnitten (`data/supplement`). Die SHA weicht ab (`085e8e38…` statt `26129de6…`), die Stufe-2-Reproduktion ist trotzdem bitgleich. Das Original sollte trotzdem ins Archiv.
- `kraken_funding/PF_{XBT,ETH,SOL}USD_funding.csv` (Eingaben laut `stage2_results.json`, Kraken-Gegenprobe/`spot_ref.py`) fehlen. Der Collector (`collector/`) sammelt diese Reihen ab jetzt neu. Das Kraken-Fenster reicht aber nur rund 1 Jahr zurück, die historische Strecke ist ohne Original nicht wiederherstellbar.

## OP-5 Zeitstempel in ENTSCHEIDE.md — ERLEDIGT durch E3 (01.10.2026)

**Auflösung:** Korrekturvermerk als neuer Eintrag in ENTSCHEIDE. Der alte Eintrag bleibt, massgeblich ist die Reihenfolge FREEZE vor Lauf. Welcher Zeitstempel falsch ist, lässt sich nicht mehr belegen.

Ursprünglicher Befund:

«2026-09-18 14:35 UTC — REBOUND-MICRO v1.0 Lauf BTC VERSIEGELT» liegt zeitlich **vor** «2026-09-18 14:40 UTC — REBOUND-MICRO v1.0 FREEZE». Nach Governance muss der Freeze vor jedem Lauf stehen. Vermutlich ein Tippfehler oder eine nachträgliche Protokollierung, das ist zu bestätigen.

## OP-6 Binance von dieser Box geoblockt — teilweise geregelt (D1-Ausnahme)

D1: Der Collector darf vorläufig auf der Agent-Box laufen, bis ein eigener Server bereitsteht. Der Binance-Teil bleibt auf data.binance.vision beschränkt (Funding mit Monatsverzug, Universum nur genähert). Auf einem eigenen Server ohne Geoblock wäre fapi direkt nutzbar.


`fapi.binance.com` antwortet von der Box mit HTTP 451. Nach Vorgabe gibt es keinen Proxy und keinen Ausweich-Endpunkt. Der Collector nutzt `data.binance.vision`:
- Funding: Monats-ZIPs mit Prüfsumme, Verzug bis ein Monat.
- Universum: S3-Listing der Daily-Kline-Ordner, «aktiv» heisst: gestern oder vorgestern gibt es eine 1d-Kline-Datei.

Das ist kein echtes `exchangeInfo`: Listing-Datum, Status und Kontrakttyp fehlen. Entscheid nötig, ob das reicht oder ob die Binance-Sammlung von einem nicht geblockten Rechner aus laufen soll (z.B. Damians Mac).

## OP-7 Expected-SHA-Liste rm_2026-09-18 — ERLEDIGT durch E3 (01.10.2026)

**Auflösung:** Ergänzung `00_doku/rm_2026-09-18_expected_shas.addendum_2026-10-01.txt` (mlib v1.0, 6b7e7ba8…). `make verify-frozen` wendet Ergänzungen an, die Ausnahme in der Allowlist ist entfernt.

Ursprünglicher Befund:

Sie nennt `mlib.py` noch als v0.1 (`cfe1f7aa…`), die Datei ist v1.0 (`6b7e7ba8…`). Die Abweichung ist in `tools/frozen_allowlist.txt` begründet. Eine nachgeführte Liste wäre sauberer, als neue Datei und nicht als Überschreibung.

## OP-8 Offen nach Schritt 0 (neu, 01.10.2026)

- **D2** Kapitalrahmen (Micro-Live in CHF, Totalverlust-Obergrenze in CHF): Zahlen von Damian ausstehend.
- **D3** Zeitbudget — ERLEDIGT (01.10.2026): höchstens 1 Std./Woche, Review höchstens 4 Monate nach Start des Paper-Tradings (ca. Anfang Februar 2027). Siehe ENTSCHEIDE 01.10.2026 15:45.
- **D5:** Status von Altsystem und Keys, Bestätigung durch Damian ausstehend.
- **XS21 PiT v0.2 (ENTWURF):** Review durch Claude/Damian, insbesondere B7-Liste (55 «wahrscheinlich», 59 «unklar», PAXG/XAUT/USTC), Schwellen des Ausführbarkeits-Gates, Tie-Break U2, Behandlung fehlenden Fundings, Zeitblöcke. Erst danach v1.0 und ein Lauf.
  - **Stand 01.10.2026 (Nachmittag):** Review Claude eingearbeitet, `01_forschung/09_lane_c/xs21_point_in_time_prereg_v1.0.md` ist FREEZE-KANDIDAT (nicht eingefroren), B7-Liste v1.0 in `xs21_pit_v1.0/` (220 Ausschluesse, 0 unklar). Offen: Freigabe Damian; Kraken-Futures-Volumen werden seit 01.10.2026 erfasst (Collector v1.1), 30-Tage-Median ab 30.10.2026, Gate fruehestens 19.12.2026 entscheidbar; Lesart «erste 8 Rebalancings» bestaetigen (v1.0 §8.2); drei Regelergaenzungen in v1.0 §8.3 bestaetigen.
- **ENTSCHEIDE-Schreibweise:** Die neuen Einträge folgen der Konvention der Datei (Umlaute umschrieben, z.B. «Empfehlung uebernommen»).

## OP-9 XS21 PiT v1.0 nach dem Lauf (neu, 01.10.2026)

- **Lauf erledigt** (01.10.2026, 13:39–13:43 Zürich): U1 und U2 je TEILWEISE (c6 MaxDD, U1 zusätzlich c3/B2). Nach §5.3: H-C2 auf PiT falsifiziert, kein Sleeve. Bericht `01_forschung/09_lane_c/xs21_pit_v1.0/xs21_pit_v1.0_bericht.md`.
- **Entscheid Damian offen:** Gate M3 (31.10.–19.12.2026) und Forward-Fenster ab 15.09.2026 weiterführen oder einstellen? Ohne Sleeve-Kandidat sieht die Spezifikation keinen Paper-Betrieb vor. Der Collector v1.1 läuft unverändert weiter, bis entschieden ist.
- **Vorbehalt Konvention U9 (Stufe 2):** Tagesrenditen mit konstantem Gewicht (implizite tägliche Rückführung ohne Kosten) gegenüber Buy-and-Hold-Trades. Bei extremen Coins weicht das stark ab (U1 2026: Tagesbeiträge +2.27, Trades −0.14). Gilt auch für die Stufe-2-Ergebnisse. Prüfen, ob künftige Spezifikationen das ändern sollen (nur neu vorregistriert).
- **Lauf-Code-Lücke:** Die Survivorship-Zerlegung je Block (§5.3) fehlte im Lauf-Code und ist deskriptiv nachgetragen.

## OP-10 DT P&L v1.0 nach dem Lauf (neu, 01.10.2026)

- **Lauf erledigt** (01.10.2026, 14:35 Zürich): Netto-K1 der Primärzellen −8.47 R < 0. A7 greift: Lane A vollständig geschlossen. Bericht `01_forschung/11_delayed_trend/dt_pnl_v1.0/dt_pnl_v1.0_bericht.md`.
- **Befund Kontrolldesign DT2:** Ersatzniveau-Kontrollen kommen fast nie zum Einstieg (`retest_failed`), deshalb ist ΔR für DT2 nicht messbar. Nur relevant bei einer allfälligen neuen Vorregistrierung mit Forward-Daten (A7).
- **Vermerke Nachprüfung (ENTSCHEIDE 15:45):** `xs21_check.json` hat `gesamt_ok: false`, erklärt durch das fehlende U5a im Prüfskript und die K2-Delisting-Reibung (17/2 Ausstiege). Die Survivorship-Zerlegung je Block (A6) ist nach dem Lauf nachgetragen.
- **Review Claude zum XS21-Lauf:** noch nicht abgelegt, weil der Text auf der Box nicht vorliegt. Ablageort, sobald geliefert: `01_forschung/09_lane_c/xs21_pit_v1.0/xs21_pit_v1.0_review_claude_v1.md`.

## OP-11 Ideen-Scan v1 (neu, 01.10.2026)

- `01_forschung/12_ideen_scan/ideen_scan_v1.md` (Kopie `/workspace/aurum2/ideen/ideen_scan_v1.md`): Shortlist neuer Ansätze, explorative Checks nur bis 2023, nicht vorregistriert.
- Vorregistrierungs-ENTWURF Funding-Carry v0.1 (nicht eingefroren). Entscheid Damian nötig, ob er weiterverfolgt wird; Steuerfrage D4 (Funding-Erträge, Derivate) vor jedem Live-Einsatz klären.
