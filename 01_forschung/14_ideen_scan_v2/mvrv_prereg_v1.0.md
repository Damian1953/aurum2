# MVRV_PREREG v1.0 — MVRV-Leitplanke für den BTC-Kernbestand, BTC Spot Kraken (Forward-Paper)

> **Kandidat, nicht eingefroren.**

**Status: KANDIDAT v1.0, NICHT EINGEFROREN, nicht gelaufen.** Kein Tag, kein Spec-SHA im Run-Log, Runner gesperrt (`sleeves/sleeves_config.json` enabled=false, Exit 3), kein cron-Eintrag.
**Stand:** 2026-10-02 (Zürich, UTC+2). Grundlage: v0.2 (bleibt unverändert liegen) und Review Claude, zusammengefasst in `review_claude_scan_v2_v1.md`. **Vetorecht Damian vorbehalten.**
**Freeze erst nach:** Freigabe des Kandidaten durch Projektleitung und Claude, kein Veto Damian, eigene Freeze-Liste (gemeinsam mit MAKRO_LIQ), ENTSCHEIDE-Eintrag.

## 0. Änderungen gegenüber v0.2
- **B ist keine Hypothese mehr, sondern eine Leitplanke für den Kernbestand.** Regel, Schwellen 1.0/3.5 und Datenquelle werden eingefroren und bleiben unverändert. **Keine Gates, kein Erfolgsanspruch, kein Trial, nicht in der Testfamilie** (keine Holm-Korrektur mit MAKRO_LIQ).
- Ausdrücklich: **Erreicht MVRV 3.5 nicht mehr, löst die Regel nie aus; das ist ein zulässiges Ergebnis** (kein «nicht prüfbar», keine Schliessung deswegen).
- Bericht hält fest: **Solange MVRV seit Start nie über 3.5 lag, ist B identisch mit Buy&Hold.**
- Gemeinsamer einseitiger Wochenbericht mit PAPER v1.0 und Sleeve A (§5).
- Cash zu DTB3 als Standard, Sensitivität 0 %; Start in gültigem Zustand, Einstieg mit Kosten (§4).
- Calmar und Ulcer-Index nur berichtet.
- §8: Vermerk «nicht First-Release».

## 0b. Deklarierte Abweichungen
1. **PAPER v1.0 F3** («kein Zins auf Cash»): Cash von B wird standardmässig zu DTB3 verzinst (First-Release, act/360); Cash 0 % als Sensitivität.
2. **PAPER v1.0 F5** («Start flach»): B startet in gültigem Zustand: INVESTIERT, falls MVRV ≤ 3.5, sonst CASH. Der Einstieg wird zur Eröffnung des Folgebars **mit Kosten** gebucht. Grund: Sonst bliebe B bis zu einem MVRV < 1.0, womöglich Jahre, flach.

## 1. Vorbelastung
- Exploration t1 < 2024 (In-Sample): Binance 2017-08 bis 2023 CAGR 51.6 %, Sharpe ex 1.06, MaxDD −63 %, 3 Wechsel; CoinMetrics 2014–2023 CAGR 62.2 %, Sharpe 1.18, 5 Wechsel.
- Schwellen 1.0/3.5 sind Praktiker-Folklore, gewählt in Kenntnis der Zyklen 2013/2017. Gesehene Spitzen: 2017-12 4.72, 2021-02 3.96, 2021-10 2.93 (fallend).
- MVRV ≥ 2024 nicht abgerufen; BTC-Pfad 2024–2026 als Marktwissen bekannt. Globaler Trial-Zähler ca. 270, **kein neuer Trial** (Leitplanke, kein Test).

## 2. Zweck (keine Hypothese)
B ist eine **Leitplanke für den BTC-Kernbestand**: Bei extremer Überbewertung (MVRV > 3.5) wird der Kernbestand in Cash geparkt und erst bei MVRV < 1.0 wieder gekauft. Es wird **kein Erfolg behauptet** und nichts getestet. Die Leitplanke wird forward im Paper mitgeführt, damit ihr Verhalten dokumentiert ist.

## 3. Daten, Publikationsverzug, As-of (eingefroren)
- **MVRV:** CoinMetrics Community API (ohne Key), `https://community-api.coinmetrics.io/v4/timeseries/asset-metrics?assets=btc&metrics=CapMVRVCur&frequency=1d`. Zeitstempel t (00:00 UTC) = Tageswert für Tag t, verfügbar erst nach Tagesende, erfahrungsgemäss mit einigen Stunden Verzug.
- **Preise:** Collector `data_live/kraken_ohlc/BTCUSD_1d.csv`. DTB3 über FRED.
- **Erfassung:** Collector (ab 1.2) lädt täglich um 06:15 Zürich die letzten 30 Tage, append-only, mit Abrufzeitpunkt (UTC) und SHA256. Massgebend ist der **Wert beim ersten Abruf**; Revisionen werden protokolliert, ändern aber keine Entscheidung.
- **As-of-Regel:** Am Schluss des Kraken-Tagesbars t gilt der neueste MVRV-Wert mit Zeitstempel ≤ t−1, dessen erster Abruf **vor dem Schluss von Bar t** (t+1 00:00 UTC) liegt. Fill zur Eröffnung t+1.
- **Ausfall:** ≥ 14 Tage ohne neuen Wert, Änderung der Metrik-Definition durch CoinMetrics oder Wegfall des Community-Zugangs → fail-closed (STOPPED, Meldung). Ersatzquelle nur mit neuer Version und ENTSCHEIDE-Eintrag.
- **Kein Look-ahead:** Runner prüft die Abrufzeit jeder verwendeten Beobachtung (Tests `tests/test_sleeves.py`).

## 4. Regel (eingefroren)
- Zustandsmaschine mit zwei Zuständen: INVESTIERT, CASH.
  - INVESTIERT → CASH, wenn MVRV > 3.5.
  - CASH → INVESTIERT, wenn MVRV < 1.0.
- **Start in gültigem Zustand (Abweichung F5):** am Startbar (gemeinsam mit MAKRO_LIQ, ein Freitag) INVESTIERT, falls MVRV ≤ 3.5, sonst CASH; Einstieg zur Eröffnung des Folgebars mit Kosten.
- Sizing: virtuell 1'000 USD. Kosten: `venue_kraken` **primär `maker_plan`** (K1, 0.47 % je Seite), **Pflicht-Sensitivität `taker_K2`**.
- **Cash (Abweichung F3):** primär zu DTB3, Sensitivität 0 %.

## 5. Bericht (keine Gates)
- Vergleichsreihen: B1 BTC Buy&Hold Kraken ab gleichem Fill-Tag mit gleichen Kosten; B2 DTB3; R1 W2-BTC aus PAPER v1.0 (nur Bericht).
- Kennzahlen nur berichtet: CAGR, MaxDD, Sharpe ex, Calmar, Ulcer-Index, Zeit im Markt, Zustand, aktueller MVRV-Wert und Abstand zu 3.5.
- **Pflichtsatz im Bericht:** «Solange MVRV seit Start nie über 3.5 lag, ist B identisch mit Buy and Hold (gleiche Menge BTC, gleicher Einstieg, gleiche Kosten).» Der Bericht zeigt zusätzlich, ob das aktuell zutrifft.
- **Pflichtsatz im Bericht:** «Erreicht MVRV 3.5 nicht mehr, löst die Regel nie aus; das ist ein zulässiges Ergebnis.»
- Gemeinsamer einseitiger Wochenbericht mit PAPER v1.0 und Sleeve A (`paper/wochenbericht.py`, feste Gestaltung, Abschnitt «Leitplanke B MVRV (kein Test)»).

## 6. Review-Termine (Betrieb)
- **2027-02-02** (mit dem PAPER-v1.0-Review): nur Betrieb (Abrufe vollständig, First-Release-Protokoll, As-of-Prüfung fehlerfrei, Zustand reproduzierbar, Kosten).
- Danach jährlich im Oktober gleiche Betriebsprüfung. Dazwischen nur Betriebs-Kill (§3 Ausfall, Look-ahead, Codefehler mit neuer Version und ENTSCHEIDE-Eintrag).

## 7. Keine Langfrist-Auswertung
- Keine Gates, kein Erfolgsurteil, kein Test, keine Holm-Korrektur, keine Micro-Live-Empfehlung aus B.
- Keine nachträglichen Schwellen (3.0, MVRV-Z, Perzentile); Änderungen an Regel, Schwellen oder Quelle nur mit neuer Version, Begründung und ENTSCHEIDE-Eintrag, nie wegen gesehener Ergebnisse.
- Löst die Regel nie aus, bleibt B identisch mit Buy&Hold; das ist zulässig und kein Grund zur Schliessung.

## 8. Deskriptiver Anhang 2024–2026 (ohne Entscheidungsgewicht)
- Einmal nach dem Freeze rechenbar, gekennzeichnet «deskriptiv, kein Test, Kontext-Vorbelastung, **nicht First-Release**». CoinMetrics-Werte sind dafür nicht First-Release (aktueller Stand), was vermerkt wird. Ändert weder Regel noch Schwellen.

## 9. Aufwand Damian
≈ 5 Min./Woche (Abschnitt im gemeinsamen Wochenbericht), erwartet < 1 Wechsel/Jahr, Spot; steuerlich günstig (wenige Transaktionen).
