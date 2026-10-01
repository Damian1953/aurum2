# Vorregistrierung ENTWURF v0.1: Delta-neutraler Funding-Carry (Kraken, BTC/ETH)

Stand 01.10.2026. **ENTWURF, nicht eingefroren, kein Lauf.** Freigabe durch Damian und Review durch Claude ausstehend. Grundlage: `ideen_scan_v1.md` §1. Die explorativen Zahlen dort (bis 2023) haben diesen Entwurf informiert, die Evidenzklasse ist deshalb höchstens Development.

## 1. Hypothese
- **H-CARRY:** Eine Position aus 1× Spot long und 1× Perp short (BTC, ETH; Kraken-Kosten) erzielt nach Kosten einen Ertrag über dem risikolosen USD-Satz (FRED DTB3).
- **H0:** Der Überschuss ist ≤ 0.

## 2. Daten und Zeiträume
- **Testperiode A:** Binance-USDT-Perp-Funding (8 h), 2024-01-01 bis 2026-08-31. Bisher nie als Carry-Outcome ausgewertet; Vorbehalt siehe Scan.
- **Testperiode B:** Kraken PF_XBTUSD und PF_ETHUSD, stündlich, 2025-09-17 bis Datenende vor dem Freeze. Massgeblich für die Venue.
- **Forward:** Collector-Daten ab Freeze.
- Keine Holdout-Dateien der Lane-A-Governance.

## 3. Regeln (zu bestätigen)
- **R1 Dauerhaft:** Einstieg am ersten Tag, Rebalancing der Beine, sobald der Delta-Fehler über 5 % liegt, Ausstieg am Periodenende.
- **R2 Filter (sekundär):** Im Markt, wenn das 7-Tage-Mittel des Funding > 0. Entscheid zum Tagesschluss, Wirkung am Folgetag.
- **Kosten:**
  - Spot gemäss `venue_kraken` (maker_plan; Pflicht-Sensitivität taker_K2);
  - Perp: Maker 0.02 %, Taker 0.05 % plus 0.02 % Reibung;
  - Funding mit Vorzeichen, je Abrechnungsperiode.
- **Kapital:** Spot plus Margin von 50 % des Nominals für den Short (Sensitivität 33 % und 100 %). Die Margin ist unverzinst.
- **Margin-Stress:** Steigt der Kurs seit dem letzten Rebalancing um mehr als 30 %, gilt ein Zwangs-Rebalancing zu Taker-Kosten.

## 4. Metriken und Kriterien
- **Primär:** Überschussrendite p. a. auf das Kapital minus DTB3. Dazu ein Block-Bootstrap-Konfidenzintervall mit 30-Tage-Blöcken.
- **Bestanden**, wenn alle drei Bedingungen gelten:
  - (a) Überschuss in Periode A > 0 mit Bootstrap-p < 0.05;
  - (b) Periode B nicht negativ;
  - (c) schlechteste 30-Tage-Rendite > −3 % auf das Kapital.
- **Sekundär:** R2 gegen R1, Anteil negativer Tage, Taker-Szenario.
- Holm über die primären Zellen BTC und ETH.

## 5. Offene Fragen für Damian (Entscheidvorlage, ca. 15 Minuten)
1. Venue für den Perp: nur Kraken (Empfehlung), oder auch Binance als Referenz?
2. Kapitalfaktor 1.5 als Primärannahme?
3. D4/Steuer: Klärung vor einem Live-Einsatz (Funding vermutlich Einkommen) – einverstanden?

## 6. Verbote
- Kein Lauf vor dem Freeze.
- Keine Coins ausser BTC und ETH.
- Keine Parameteränderung nach Sicht.
- Keine Keys.
