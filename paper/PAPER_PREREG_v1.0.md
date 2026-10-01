# PAPER_PREREG v1.0 – Paper-Trading W2, W6, Turtle 55/20 (Spot long, Kraken, K1)

Stand 01.10.2026, 22:15 Zürich. **Wird vor dem ersten Paper-Signal eingefroren** (Git-Tag `paper-v1.0-freeze`, SHA dieser Datei in `00_doku/paper_freeze_2026-10-01_expected_shas.txt`).

Grundlagen:
- ENTSCHEIDE 01.10.2026: 15:55 Paper-Umfang, D1 (22:03) und D3 (15:45).
- Review Claude zu XS21 PiT v1.0.

Was gilt immer:
- Keine Keys, keine Orders, kein Holdout. Alle Zahlen sind hypothetisch.
- Der Runner läuft auf der Agent-Box (D1).

## 1. Zweck und Evidenz

- **Zweck:** Forward-Betrieb der eingefrorenen Regeln unter echten Bedingungen.
  - Datenfluss, Signale, Kosten und Buchhaltung Tag für Tag nachweisen;
  - eine Forward-Reihe aufbauen, die vor dem Start nicht existierte.
- **Evidenz:**
  - W2 und W6 sind Stufe-2-Konstruktionen. Sie sind outcome-informiert ausgewählt (Stufe-2-Bericht, Hypothesen H-A1, H-A4).
  - Die Turtle-Zahlen stammen aus dem Altprojekt und sind in Aurum II nicht nachgerechnet.
  - Dieser Lauf ist deshalb ein **Forward-Test (Klasse FwdV-Kandidat)**, keine Entdeckung.
- **Kein Leistungsurteil nach 4 Monaten:** Stufe 2 zählte für W2 rund 2.2 Einstiegssignale je Coin und Jahr (BTC 2.23, ETH 2.11; `stage2_results.json`, Fingerprint). In 4 Monaten über 10 Coins sind also nur etwa 5–10 Einstiege je Strategie zu erwarten. Der Review (§9) prüft deshalb vor allem **Betrieb und Kosten**.

## 2. Strategien und Regeln (unverändert übernommen)

Gemeinsame Konventionen:
- Tageskerzen Kraken Spot (USD), nur **abgeschlossene** Bars (UTC-Tag).
- Signal am Schluss von Bar t, Ausführung (Paper-Fill) zur Eröffnung von Bar t+1. Das gilt auch für Stopps.
- Kein Hebel, keine Teilausstiege, kein Gewinnziel, Wiedereinstieg ohne Cooldown.

### 2.1 W2
Quelle: `01_forschung/02_strategien/stage2_preregistration_v1.md` §5, §6.
- Filter: `Close > SMA200`.
- Einstieg: `Close > HH(55)`, wobei `HH(55) = max(High[t−55 … t−1])`.
- Stopp: `Entry_Fill − 3·ATR14_t`, nachziehend `max(stop, HighestClose_seit_Einstieg − 3·ATR14_t)`, nie gesenkt.
- Ausstieg: `Close ≤ stop` oder `Close < SMA200`.
- Indikatoren: `s2lib.indicators` / `s2lib.atr14` (eingefroren, Wilder-ATR14).

### 2.2 W6
Quelle: wie W2, plus §10.2.
- Einstiegsunit 0.50, zwei Add-ons zu 0.25, maximal 1.00.
- Add-on, wenn `Close_t > HH(55)_t` **und** `Close_t ≥ Fill_letzte_Unit + 1.0·ATR14_t`.
- Nach jedem Add-on gilt `stop = max(stop, AddOnFill − 3·ATR14_t)`.
- Ausstieg der Gesamtposition auf einmal.

### 2.3 Turtle 55/20 (T55_20)
Quelle: `00_doku/AURUM_II_FINDINGS_DIGEST_2026-09-15.md` §2.1.
- Einstieg: `Close > Hoch der letzten 55 Tage` (laufender Bar ausgeschlossen).
- Ausstieg: `Close < Tief der letzten 20 Tage` (laufender Bar ausgeschlossen).
- `N = Wilder-ATR(20)`, gleiche True-Range-Definition wie ATR14.
- Notstopp `Entry_Fill − 2·N` (N des Signalbars), mit **Vorrang** vor dem 20-Tage-Ausstieg.
- Kein SMA-Filter.

### 2.4 Festlegungen (wo die Quellen schweigen; vor dem Start fixiert)

- **F1 Turtle-Ausführung:** Alle Auslöser beziehen sich auf den Schlusskurs, der Fill erfolgt zur Eröffnung t+1 (Stufe-2-Konvention). Die Original-Shadow-Implementierung des Altprojekts liegt in Aurum II nicht vor.
- **F2 Universum:** Für alle drei Strategien das Stufe-2-Universum §15: BTC, ETH, SOL, XRP, ADA, AVAX, LINK, DOT, BNB, LTC.
  - Je Coin ein unabhängiger Sleeve.
  - Das Turtle-Universum des Altprojekts ist in Aurum II nicht dokumentiert (genannt sind BTC, ETH, SOL). Diese drei werden im Review zusätzlich deskriptiv ausgewiesen.
- **F3 Sizing:** virtuell 1'000 USD je Strategie und Coin, also 10'000 USD je Strategie.
  - W2 und T55_20 investieren beim Einstieg 100 % des Sleeve-Kapitals.
  - W6 investiert 0.50 / 0.25 / 0.25 des Sleeve-Kapitals zum Zeitpunkt des Ersteinstiegs.
  - Zinseszins über die Trades eines Sleeves, kein Zins auf Cash.
- **F4 Kosten:** `config/cost_model_v1.json`, Abschnitt `venue_kraken` (C1/C2).
  - **Primär `maker_plan`** (= K1): Einstieg und Add-on fee 0.40 % + fric 0.02 % + slip_in 0.05 %.
  - Ausstieg nach Stopp oder Notstopp: fee + fric + slip_sl 0.10 %. Übrige Ausstiege (Filter, 20-Tage-Tief): fee + fric + slip_in.
  - **Pflicht-Sensitivität `taker_K2`** mit gleicher Zuordnung.
  - Keine Funding-Kosten (Spot).
- **F5 Start:** **erster Signalbar 2026-10-02 (UTC)**, erster möglicher Fill zur Eröffnung am 2026-10-03.
  - Alle Strategien starten **flach**: Einstiegssignale vor dem Startbar zählen nicht.
  - Kraken-Tageskerzen ab 2024-09-27 aus dem Collector dienen nur dem Warmup der Indikatoren und werden nicht ausgewertet.
- **F6 Daten:**
  - Quelle: Collector-Dateien `data_live/kraken_ohlc/{COIN}USD_1d.csv` (öffentliche Kraken-API).
  - Fehlt ein Bar seit dem Start (Lücke), wird der Coin **fail-closed** gestoppt und gemeldet, ohne Reparatur nach Sicht.
  - Der Runner rechnet täglich alles neu. Fehlt ein früher protokolliertes Ereignis im Neulauf, gilt das als **Revision**: Fehler wird gemeldet, das Journal bleibt bestehen.
  - Verspätete Daten ändern keine Fill-Preise, nur den Buchungszeitpunkt.

## 3. Betrieb

- **Taktung:**
  - cron 06:50 Zürich (`paper/run_paper.sh --if-needed`), nach dem Collector um 06:15;
  - Nachholen über `collector/ensure_scheduler.sh` (Prüfroutine 07:35 und jede Shell);
  - Wochenbericht montags 07:10 nach `/workspace/aurum2/paper/berichte/`.
- **Ausgaben** (`/workspace/aurum2/paper/`):
  - `state/state_latest.json`;
  - `ledger/trades.csv`, `ledger/equity_daily.csv`, `ledger/journal.jsonl` (append-only);
  - `logs/run_history.jsonl`.
- **Fail-closed:** Der Runner prüft vor jedem Lauf die SHAs der eingefrorenen Dateien (Freeze-Liste) und läuft bei Abweichung nicht.

## 4. Benchmarks

- **B1 Buy and Hold:** gleiche 10 Coins zu je 1'000 USD, Kauf zur Eröffnung am 2026-10-03 mit Einstiegskosten. Bewertung täglich zum Schluss, netto nach hypothetischen Ausstiegskosten.
- **B2 Risikoloser USD-Satz:** FRED DTB3 (öffentlich, ohne Key), jeweils letzter verfügbarer Wert, auf 10'000 USD aufgezinst.
- **B3 Staking-Referenz:** B1 plus Staking-Ertrag auf ETH 2.58 % und SOL 5.69 % p. a. (Kraken Schweiz, abgerufen 01.10.2026), nur berichtet.

## 5. Metriken

**Primär** je Strategie, Szenario maker_plan, Taker-Szenario daneben:
1. Netto-Rendite seit Start minus B1 (Prozentpunkte);
2. Netto-Rendite minus B2 (bzw. B3 berichtet);
3. MaxDD der täglichen Portfoliokurve (Schlusskurse) gegen den MaxDD von B1.

**Sekundär:**
- Anzahl Einstiege, Add-ons und Ausstiege nach Grund;
- bezahlte Kosten in USD und Kostenquote (Kosten / Brutto-P&L);
- mittlere Exposure;
- Betriebskennzahlen (§9).

## 6. Was nicht erlaubt ist

- Keine Parameter-, Regel-, Universums- oder Kostenänderung nach dem Freeze.
- Keine Aufnahme von XS21 (ENTSCHEIDE 15:55).
- Keine Keys, keine Orders.
- Ein Bugfix im Lauf-Code ist nur mit datiertem ENTSCHEIDE-Eintrag und neuer Freeze-Liste zulässig. Der Bericht weist ihn aus, Ergebnisse vor und nach dem Fix werden getrennt gezeigt.

## 7. XS21 U2 als Schattenrechnung

In v1.0 **nicht umgesetzt**. Es bräuchte das Point-in-Time-Universum und eine tägliche Binance-Download-Pipeline, das ist nicht günstig. Falls später ergänzt:
- eigene Vorregistrierung;
- öffentliche Binance-Daten, Trade-Basis;
- **ohne Entscheidgewicht vor 12 Monaten**.

## 8. Quellen der Referenzwerte

- Staking: https://www.kraken.com/ch/features/staking/ethereum, https://www.kraken.com/ch/features/staking/solana (01.10.2026).
- DTB3: https://fred.stlouisfed.org/series/DTB3.

## 9. Review (D3)

**Termin:** spätestens **2027-02-02**, Datenstand Bar 2027-01-31, also höchstens 4 Monate nach dem Start. Damian setzt dafür höchstens 1 Stunde ein (D3); der Agent liefert eine Entscheidvorlage.

**Prüffragen:**
- **R1 Betrieb:**
  - Anteil Tage, deren Bar bis 08:00 Zürich verarbeitet war (Ziel ≥ 95 %);
  - Nachholungen;
  - Lücken und Revisionen (Ziel: 0 unerklärte);
  - Freeze-Verletzungen (Ziel: 0).
- **R2 Kosten:** Die Kosten je Trade entsprechen F4. Die Kostenquote wird berichtet. Dazu ein Vergleich mit den Kraken-Tarifen zum Review-Zeitpunkt.
- **R3 Reproduzierbarkeit:** Ein unabhängiger Neulauf mit eingefrorenem `s2lib.run_trend` (W2/W6) ergibt dieselben Trades. Turtle wird nach §2.3 von Hand nachgerechnet.
- **R4 Deskriptiv:** Metriken §5 mit dem ausdrücklichen Hinweis auf die kleine Trade-Zahl.

**Mögliche Ergebnisse:** «weiterführen», «Betriebsmangel beheben und weiterführen» oder «einstellen» (z. B. bei nicht behebbaren Datenproblemen).
- Ein Leistungsurteil fällt beim Review **nicht**.
- Dafür ist eine eigene Vorregistrierung nötig. Als Vorschlag aus `stage2_hypotheses_v2.md` H-A1: Verwerfen, wenn Alpha-t unter 1.0 nach 24 Monaten liegt oder der MaxDD tiefer ist als der Stufe-2-Wert. Das wird hier nicht beschlossen.
