# MVRV_PREREG v0.2 — MVRV-Bewertungsband, BTC Spot Kraken (Forward-Paper)

**Status: ENTWURF v0.2. Nicht eingefroren, nicht gelaufen.** Kein Tag, kein Spec-SHA im Run-Log, kein Runner gebaut.
**Stand:** 2026-10-01 22:40 (Zürich, UTC+2). Grundlage: Entscheid Chief Strategist 2026-10-01 22:40 (ENTSCHEIDE), **Vetorecht Damian vorbehalten**. Ersetzt `mvrv_prereg_entwurf_v0.1.md` (bleibt unverändert liegen).
**Freeze erst nach:** Review Claude, kein Veto Damian, Runner und Collector-Erweiterung gebaut und getestet.

## 0. Änderungen gegenüber v0.1
- **Kein Retro-Test 2024–2026** (Kontext-Vorbelastung); nur deskriptiver Anhang ohne Entscheidungsgewicht (§8). Die Stufe-1-Retroprüfung aus v0.1 entfällt.
- Forward-Paper als zusätzlicher Sleeve, eigener Runner und eigene Freeze-Liste; `paper/` unverändert.
- Datenquelle, Verzug und As-of präzisiert (§3); Review-Termine und Kill-Regeln (§6, §7).

## 1. Vorbelastung
- Exploration t1 < 2024 (In-Sample): Binance 2017-08 bis 2023 CAGR 51.6 %, Sharpe ex 1.06, MaxDD −63 %, 3 Wechsel; CoinMetrics 2014–2023 CAGR 62.2 %, Sharpe 1.18, 5 Wechsel.
- Schwellen 1.0/3.5 sind Praktiker-Folklore, gewählt in Kenntnis der Zyklen 2013/2017. Gesehene Spitzen: 2017-12 4.72, 2021-02 3.96, 2021-10 2.93 (fallend).
- MVRV ≥ 2024 nicht abgerufen; BTC-Pfad 2024–2026 als Marktwissen bekannt. Globaler Trial-Zähler ca. 270, kein neuer Trial.

## 2. Hypothese
H-MVRV: Ein BTC-Spot-Sleeve, der bei MVRV > 3.5 in Cash wechselt und erst bei MVRV < 1.0 wieder kauft, hat forward einen deutlich kleineren MaxDD als BTC Buy&Hold, bei einer CAGR höchstens 5 Prozentpunkte pro Jahr darunter.

## 3. Daten, Publikationsverzug, As-of
- **MVRV:** CoinMetrics Community API (ohne Key), `https://community-api.coinmetrics.io/v4/timeseries/asset-metrics?assets=btc&metrics=CapMVRVCur&frequency=1d`. Zeitstempel t (00:00 UTC) = Tageswert für Tag t, verfügbar erst nach Tagesende, erfahrungsgemäss mit einigen Stunden Verzug.
- **Preise:** Collector `data_live/kraken_ohlc/BTCUSD_1d.csv`. DTB3 über FRED.
- **Erfassung:** Collector-Erweiterung (neu, nicht Teil von `paper/`) lädt täglich um 06:15 Zürich die letzten 30 Tage, append-only, mit Abrufzeitpunkt (UTC) und SHA256. Massgebend ist der **Wert beim ersten Abruf**; Revisionen werden protokolliert, ändern aber keine Entscheidung.
- **As-of-Regel:** Am Schluss des Kraken-Tagesbars t gilt der neueste MVRV-Wert mit Zeitstempel ≤ t−1, dessen erster Abruf **vor dem Schluss von Bar t** (t+1 00:00 UTC) liegt. Fill zur Eröffnung t+1. Fehlt ein solcher Wert, bleibt der Zustand unverändert.
- **Ausfall:** ≥ 14 Tage ohne neuen Wert, Änderung der Metrik-Definition durch CoinMetrics oder Wegfall des Community-Zugangs → fail-closed (Position bleibt bis Entscheid, Meldung). Ersatzquelle nur mit neuer Version und ENTSCHEIDE-Eintrag.
- **Kein Look-ahead:** Runner prüft die Abrufzeit jeder verwendeten Beobachtung; Test vor dem Freeze mit synthetischen Daten.

## 4. Regel
- Zustandsmaschine mit zwei Zuständen: INVESTIERT, CASH.
  - INVESTIERT → CASH, wenn MVRV > 3.5.
  - CASH → INVESTIERT, wenn MVRV < 1.0.
- Start: am ersten Signalbar nach dem Freeze INVESTIERT, falls MVRV ≤ 3.5, sonst CASH. Abweichung von PAPER v1.0 F5 («Start flach») bewusst, weil die Regel sonst bis zu einem MVRV < 1.0 (womöglich Jahre) flach bliebe; Frage an Claude.
- Sizing: virtuell 1'000 USD. Kosten: `venue_kraken` **primär `maker_plan`** (K1, 0.47 % je Seite), **Pflicht-Sensitivität `taker_K2`**. Cash primär ohne Zins (PAPER-v1.0-Konvention), berichtet: Cash zu DTB3.

## 5. Benchmarks und Metriken
- B1: BTC Buy&Hold Kraken ab gleichem Fill-Tag; B2: DTB3; R1 (Bericht): W2-BTC-Sleeve aus PAPER v1.0.
- Metriken: CAGR, MaxDD, Sharpe ex, Zeit im Markt, Zustand und aktueller MVRV-Wert im Wochenbericht.

## 6. Review-Termine (Betrieb, kein Leistungsurteil)
- **2027-02-02** (mit dem PAPER-v1.0-Review): nur Betrieb (Abrufe vollständig, First-Release-Protokoll, As-of-Prüfung fehlerfrei, Zustand reproduzierbar, Kosten).
- Danach jährlich im Oktober gleiche Betriebsprüfung. Dazwischen nur Betriebs-Kill (§3 Ausfall, Look-ahead, Codefehler mit neuer Version und ENTSCHEIDE-Eintrag).

## 7. Langfrist-Auswertung und Kill-Regel
- **Auswertungszeitpunkt:** nach dem ersten vollständigen Zyklus (Ausstieg > 3.5 und Wiedereinstieg < 1.0), am nächsten Oktober-Termin; spätestens **2030-12-31**.
- **Gates** (maker_plan):
  - G1: |MaxDD Sleeve| ≤ 2/3 × |MaxDD B1|.
  - G2: CAGR Sleeve ≥ CAGR B1 − 5 Pp/J.
  - G3: auch unter taker_K2 erfüllt.
- **Nicht prüfbar:** Kein Ausstieg bis 2030-12-31 (MVRV nie > 3.5) → Hypothese «nicht prüfbar», Linie geschlossen (Regel hätte nur Komplexität ohne Wirkung).
- **Kill:** G1, G2 oder G3 verfehlt → Linie geschlossen; keine nachträglichen Schwellen (3.0, MVRV-Z, Perzentile).
- Holm gemeinsam mit H-LIQ (siehe MAKRO_LIQ v0.2 §7). Erfolg → nur Empfehlung an Damian (D2).

## 8. Deskriptiver Anhang 2024–2026 (ohne Entscheidungsgewicht)
- Einmal nach dem Freeze rechenbar, gekennzeichnet «deskriptiv, kein Test, Kontext-Vorbelastung». CoinMetrics-Werte sind dafür nicht First-Release (aktueller Stand), was vermerkt wird. Ändert weder Regel noch Gates.

## 9. Aufwand Damian
≈ 5 Min./Woche, erwartet < 1 Wechsel/Jahr, Spot; steuerlich günstig (wenige Transaktionen).

## 10. Fragen an Claude
Siehe `an_claude_scan_v2.md`.
