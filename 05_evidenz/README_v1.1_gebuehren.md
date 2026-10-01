# 05_evidenz — Korrekturvermerk Gebührensätze (v1.1, 01.10.2026)

**Status:** Korrektur nach ENTSCHEIDE C2 (Damian, 01.10.2026). `05_evidenz/README.md` (SHA `1ad05bc7e3efafbf…`) bleibt eingefroren und unverändert. Diese Datei ersetzt dort **nur die Gebührentabelle** (Zeilen 9 bis 11). Alles andere in der README gilt weiter.

## Was falsch war

`README.md` nennt Spot-Taker 0.26 / 0.40 / 0.55 %, Spot-Maker 0.16 / 0.25 / 0.35 % und Perp-Taker 0.05 / 0.075 / 0.10 % je Seite (optimistisch / mittel / konservativ). Diese Sätze passen zu keinem dokumentierten Kraken-Tier. Eine Quelle ist nicht dokumentiert. Sie widersprechen ENTSCHEIDE (15.09.2026, Kraken Fee Schedule, Tier 1) und `05_evidenz/kostenhuerde_teil1.py`.

## Gültige Sätze (Quelle: `config/cost_model_v1.json` v1.1, Abschnitt `venue_kraken`)

| Kraken Tier 1, je Seite | Maker | Taker |
|---|---|---|
| Spot | 0.40 % | 0.80 % |
| Futures (PF-Perps) | 0.02 % | 0.05 % |

Kostenszenarien für Spot-Long auf Kraken (C2):
- **Maker-Plan** (primär): 0.40 % plus 0.02 % Reibung, Slippage 5 bp beim Einstieg und 10 bp beim Stop (entspricht K1).
- **Taker** (Pflicht-Sensitivität): mindestens unter K2, also 0.80 % plus 0.06 % Reibung, Slippage 15 und 30 bp.

Eingefrorene Läufe behalten ihre damaligen Werte (`spot_r`, `stage2_perp`, `stage2_spot_ref` K0/K1/K2).

## Folge für bisherige Ergebnisse

Keine Umetikettierung. In den eingefrorenen Spot-R-Läufen ist K1 (0.40 %) als Maker-Ausführung zu lesen. Taker-Ausführung entspricht K2 (0.80 %).
