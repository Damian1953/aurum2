# MAKRO_LIQ_PREREG v1.0 — Fed-Netto-Liquiditäts-Regime, BTC Spot Kraken (Forward-Paper)

> **Kandidat, nicht eingefroren.**

**Status: KANDIDAT v1.0, NICHT EINGEFROREN, nicht gelaufen.** Kein Tag, kein Spec-SHA im Run-Log, Runner gesperrt (`sleeves/sleeves_config.json` enabled=false, Exit 3), kein cron-Eintrag.
**Stand:** 2026-10-02 (Zürich, UTC+2). Grundlage: v0.2 (bleibt unverändert liegen) und Review Claude, zusammengefasst in `review_claude_scan_v2_v1.md`. **Vetorecht Damian vorbehalten.**
**Freeze erst nach:** Freigabe des Kandidaten durch Projektleitung und Claude, kein Veto Damian, eigene Freeze-Liste, ENTSCHEIDE-Eintrag. Voraussetzung: Collector 1.3 (WDTGAL) liefert First-Release-Werte.

## 0. Änderungen gegenüber v0.2
- **M1:** TGA als Mittwochsstand `WDTGAL` statt Wochendurchschnitt `WTREGEN` (passt zum Mittwochsstand `WALCL`). Collector 1.3 lädt `WDTGAL`.
- **M2:** Testfälle vor dem Freeze für Freitagsabruf gescheitert, H.4.1 verspätet/verschoben und RRP fehlt am Mittwoch (§3, grün).
- **M3:** gemeinsamer einseitiger Wochenbericht mit PAPER v1.0 und Leitplanke B, feste Gestaltung (§5).
- **M4:** Redundanzregel gegenüber W2-BTC (§7.3).
- **M5:** A wird allein auf 5 % getestet, keine Holm-Korrektur (§7.2). MVRV ist keine Hypothese mehr (Leitplanke).
- Cash standardmässig zu DTB3, Sensitivität 0 % (§4). Start in gültigem Zustand, Einstieg mit Kosten (§4).
- Calmar und Ulcer-Index nur berichtet; Anzahl Regimephasen > 13 Wochen berichtet (§5).
- Stale-Regel gilt für alle drei Reihen (WALCL, WDTGAL, RRPONTSYD).
- §8: Vermerk «nicht First-Release».

## 0b. Deklarierte Abweichungen
1. **Exploration t7 und v0.2:** t7 (`tools/ideen/explorativ_scan_v2.py`, Zeile 166) hat `WTREGEN` (Wochendurchschnitt) verwendet. v1.0 verwendet `WDTGAL` (Mittwochsstand). Die In-Sample-Zahlen aus §1 beziehen sich daher auf eine andere TGA-Reihe; sie sind ohnehin kein Beleg. t7 wird nicht neu gerechnet (kein neuer Trial).
2. **PAPER v1.0 F3** («kein Zins auf Cash»): Cash von A wird standardmässig zu DTB3 verzinst; Cash 0 % wird als Sensitivität berichtet. Grund: A liegt typischerweise lange in Cash, ohne Zins wäre der Vergleich mit B2 verzerrt.
3. **PAPER v1.0 F5** («Start flach»): A startet in gültigem Zustand (Zustandsregel, kein Kreuzungsereignis). Der Einstieg wird zur Eröffnung des Folgebars **mit Kosten** gebucht.

## 1. Vorbelastung
- Exploration t7 auf Daten < 2024 (In-Sample, kein Beleg, mit `WTREGEN`): CAGR 48.6 %, Sharpe ex 0.98, MaxDD −63 %, 32 Wechsel; ab 2021 Sharpe 0.63 (B&H 0.48).
- Grober Verlauf 2024–2026 von BTC und Fed-Bilanz als Marktwissen bekannt; keine Signalwerte ≥ 2024 berechnet.
- Globaler Trial-Zähler ca. 270; diese Vorregistrierung fügt keinen Trial hinzu (Forward). H-LIQ ist die **einzige** Hypothese dieser Testfamilie.

## 2. Hypothese
H-LIQ: Ein BTC-Spot-Sleeve, der nur investiert ist, wenn die Fed-Netto-Liquidität über 13 Wochen gestiegen ist, erzielt forward nach K1-Kosten eine Sharpe-Ratio mindestens gleich wie BTC Buy&Hold und einen MaxDD von höchstens zwei Dritteln des Buy&Hold-MaxDD.

## 3. Daten, Publikationsverzug, As-of
| Reihe | Quelle (ohne Key) | Stichtag | Publikation | Einheit |
|---|---|---|---|---|
| WALCL (Fed-Bilanzsumme, Mittwochsstand) | FRED `fredgraph.csv?id=WALCL`, Quelle H.4.1 | Mittwoch w | H.4.1 donnerstags 16:30 ET (Do 20:30/21:30 UTC je nach Sommer-/Winterzeit; FRED meist am selben Abend) | Mio. USD |
| **WDTGAL** (Treasury General Account, Mittwochsstand) | FRED `fredgraph.csv?id=WDTGAL`, Quelle H.4.1 | Mittwoch w | wie WALCL | Mio. USD |
| RRPONTSYD (Overnight Reverse Repo) | FRED, Quelle NY Fed | täglich, verwendet Mittwoch w | NY Fed am selben Tag nachmittags ET, FRED meist am folgenden Geschäftstag | Mrd. USD |
| BTC/USD 1d | Collector `data_live/kraken_ohlc/BTCUSD_1d.csv` (öffentliche Kraken-API) | Tagesbar UTC | laufend | USD |
| DTB3 | FRED | täglich | Folgetag | % p. a. |

- **Erfassung:** Collector 1.3 lädt täglich um 06:15 Zürich die FRED-Reihen (letzte 200 Tage) append-only mit Abrufzeitpunkt (UTC) und SHA256 der Rohantwort. Massgebend ist je Beobachtung der **Wert beim ersten Abruf** (First-Release); Revisionen werden protokolliert, ändern aber keine Entscheidung. `WDTGAL` wird erst ab Collector 1.3 erfasst; die beim ersten Abruf vorhandenen Werte dienen nur dem Warmup («Warmup ohne PiT», keine Bewertung).
- **As-of-Regel:** Für die Woche w gilt NL_w = WALCL_w − WDTGAL_w − 1000 × RRPONTSYD_(Mittwoch w). Verwendet werden nur Beobachtungen, deren erster Abruf **vor dem Schluss des Signalbars** (Freitag w+2 Tage, 24:00 UTC) liegt. Signal am Schluss des Freitagsbars, Fill zur Eröffnung Samstag.
- **Freitagsabruf gescheitert (M2):** Der reguläre Abruf ist Freitag 06:15 Zürich. Scheitert er, kommt der nächste Abruf erst nach dem Schluss des Freitagsbars; die Werte für w sind dann für diesen Freitag nicht sichtbar → **Zustand unverändert, keine Nachbuchung**. Am Folgefreitag gilt die Regel normal (die nachträglich erfassten Werte dienen dann als gewöhnliche Vergangenheitswerte, auch als Lag w−13).
- **H.4.1 verspätet oder verschoben (M2):** Wird H.4.1 für w (Feiertag, Shutdown) so spät publiziert oder abgerufen, dass der erste Abruf nicht vor dem Freitagsschluss liegt, bleibt der Zustand unverändert; kein Vorwegnehmen eines Wechsels. Liegt der verschobene Abruf noch vor dem Freitagsschluss, wird er verwendet. Fehlt eine Beobachtung mit Stichtag genau Mittwoch w (oder w−13), bleibt der Zustand ebenfalls unverändert.
- **RRP fehlt am Mittwoch (M2):** Es gilt der letzte vorherige Tageswert mit Stichtag ≤ w, dessen erster Abruf vor dem Signalbar-Schluss liegt (auch wenn der Mittwochswert zwar existiert, aber erst später abgerufen wurde).
- **Ausfall:** Liefert eine der drei Reihen WALCL, WDTGAL oder RRPONTSYD ≥ 8 Wochen keine neuen Werte, oder ändert die Fed die Definition einer Reihe, stoppt der Sleeve fail-closed (STOPPED, keine weiteren Buchungen, Meldung im Wochenbericht). Ein Ausfall der Makro-Quellen macht den Collector-Lauf nicht fehlerhaft und verzögert PAPER v1.0 nicht.
- **Kein Look-ahead:** Der Runner prüft bei jedem Lauf, dass jede verwendete Beobachtung einen ersten Abrufzeitpunkt < Signalbar-Schluss hat; sonst Fehler (Exit 5). Tests vor dem Freeze: `tests/test_sleeves.py` (unter anderem die drei M2-Tests).

## 4. Regel
- Signal S_w = 1, wenn NL_w − NL_(w−13) > 0, sonst 0. Benötigt 14 Wochen; für das Warmup vor dem Start dürfen die beim ersten Collector-Abruf vorhandenen Werte verwendet werden (gekennzeichnet, keine Bewertung).
- Position: 100 % des Sleeve-Kapitals BTC bei S=1, 0 % (Cash) bei S=0. Keine Hebel, keine Derivate.
- **Start in gültigem Zustand (Abweichung F5):** Startbar ist der erste Signalfreitag nach dem Freeze (der Runner verweigert einen Startbar, der kein Freitag ist). Der Sleeve übernimmt den dann gültigen Zustand ohne Kreuzungsereignis. Ist dieser INVESTIERT, wird der Einstieg zur Eröffnung des Samstags **mit Kosten** (c_in) gebucht. Sind die H.4.1-Werte am Startfreitag nicht sichtbar, bleibt A flach bis zum nächsten Freitag mit gültigem Signal.
- Sizing: virtuell 1'000 USD, Zinseszins.
- Kosten: `config/cost_model_v1.json` `venue_kraken`, **primär `maker_plan`** (= K1, 0.47 % je Seite), **Pflicht-Sensitivität `taker_K2`**.
- **Cash (Abweichung F3):** primär zu DTB3 (First-Release, act/360, Tageswert mit erstem Abruf vor Bar-Schluss); Sensitivität Cash 0 %.

## 5. Benchmarks, Metriken, Wochenbericht
- B1: BTC Buy&Hold Kraken, Kauf zur Eröffnung des ersten Fill-Tags, gleiche Kosten.
- B2: 1'000 USD zu DTB3 aufgezinst (gleiche Zinsregel wie das Cash von A).
- R1 (nur Bericht und Redundanzregel §7.3): W2-BTC-Sleeve aus PAPER v1.0.
- Berichtet: DXY-Sensitivität (DTWEXBGS < SMA100) **rein deskriptiv**, keine zweite Hypothese.
- Metriken: Sharpe ex (täglich, annualisiert), CAGR, MaxDD, Anzahl Wechsel, Zeit im Markt, Kosten kumuliert.
- **Nur Bericht, keine Gates:** Calmar-Ratio, Ulcer-Index, **Anzahl Regimephasen länger als 13 Wochen** (Phase = ununterbrochene Folge gleicher Position, länger als 91 Tage).
- **Wochenbericht (M3):** gemeinsamer einseitiger Bericht mit PAPER v1.0 und Leitplanke B (`paper/wochenbericht.py`), feste Gestaltung: 1 Betrieb, 2 PAPER Stand, 3 PAPER Woche/Orders, 4 Sleeve A, 5 Leitplanke B, 6 Datenquellen und Kosten, 7 Was Damian tun muss. Höchstens 60 Zeilen; fehlende Werte erscheinen als «–». Kein Leistungsurteil.

## 6. Review-Termine (Betrieb, kein Leistungsurteil)
- **2027-02-02** (gleichzeitig mit dem PAPER-v1.0-Review): nur Betrieb. Prüfen: Collector-Abrufe vollständig, First-Release-Protokoll, As-of-Prüfung ohne Fehler, Signale reproduzierbar aus dem Schnappschuss-Archiv, Kosten korrekt gebucht, Feiertagsfälle. Kein Urteil über Rendite oder Drawdown.
- Danach jährlich im Oktober (2027-10, 2028-10, …) gleiche Betriebsprüfung.
- Zwischen den Terminen nur Betriebs-Kill (§3 Ausfall, nachgewiesener Look-ahead oder Codefehler). Ein Codefehler wird nur mit neuer Version und ENTSCHEIDE-Eintrag behoben; betroffene Periode wird gekennzeichnet.

## 7. Langfrist-Auswertung, Test, Redundanz, Kill
### 7.1 Zeitpunkt und Gates
- **Auswertungszeitpunkt:** erster Oktober-Termin, an dem **≥ 3 Jahre Forward und ≥ 10 Signalwechsel** vorliegen; spätestens **2031-10-01** (dann mit der vorhandenen Anzahl Wechsel).
- **Gates** (alle, maker_plan, Cash zu DTB3):
  - G1: Sharpe ex Sleeve ≥ Sharpe ex B1.
  - G2: |MaxDD Sleeve| ≤ 2/3 × |MaxDD B1|.
  - G3: CAGR Sleeve > CAGR B2.
  - G4: G1–G3 auch unter taker_K2 erfüllt.
### 7.2 Test (M5)
- H-LIQ wird **allein** getestet, Niveau **5 %**, **keine Holm-Korrektur** (die Testfamilie besteht nur aus H-LIQ; MVRV ist eine Leitplanke ohne Test).
- Statistik: zweiseitiger p-Wert des Ledoit-Wolf-(2008)-Bootstraps der Sharpe-Differenz Sleeve − B1 (maker_plan, Cash DTB3).
- p ≤ 0.05 bei erfüllten Gates = «signifikant». p > 0.05 bei erfüllten Gates = «nicht widerlegt, nicht signifikant», keine Empfehlung.
### 7.3 Redundanzregel (M4)
- Besteht A alle Gates, ist die Korrelation der Exposition mit W2-BTC (PAPER v1.0) **> 0.7** und ist die Sharpe-Ratio von A **nicht höher** als jene von W2-BTC, gilt A als **redundant** und erhält **keine Micro-Live-Empfehlung**.
- Exposition = tägliche Position 0/1 am Bar-Schluss, gleiches Fenster ab Startbar; Korrelation nach Pearson. Sharpe-Vergleich mit gleicher Cash-Konvention wie PAPER F3 (A mit Cash 0 %), maker_plan. Ist die Korrelation nicht bestimmbar (eine Reihe konstant), greift die Regel nicht; das wird gemeldet.
### 7.4 Ergebnis
- **Kill:** Ein Gate verfehlt → «verworfen», Linie geschlossen, keine Varianten (andere Fenster, DXY, Realzinsen) nachschieben. Unter 10 Wechseln bis 2031-10-01 → «nicht prüfbar», Linie geschlossen.
- **Empfehlung:** nur wenn alle Gates erfüllt, p ≤ 0.05 und nicht redundant: Empfehlung an Damian für Micro-Live; Entscheid D2 bei Damian.
- Umsetzung: `sleeves/auswertung.py` (`gates_a`, `redundant_a`, `verdict_a`), Tests in `tests/test_sleeves.py`.

## 8. Deskriptiver Anhang 2024–2026 (ohne Entscheidungsgewicht)
- Darf nach dem Freeze **einmal** gerechnet und gezeigt werden, Kennzeichnung «deskriptiv, kein Test, Kontext-Vorbelastung, **nicht First-Release**».
- FRED-Werte nach Möglichkeit als ALFRED-Vintage; falls ohne Key nicht verfügbar, aktuelle (revidierte) Werte mit Vermerk «nicht First-Release».
- Ergebnis darf weder Regel, Parameter noch Gates ändern und wird bei der Auswertung (§7) nicht berücksichtigt.

## 9. Aufwand Damian
≈ 10 Min./Woche (gemeinsamer Wochenbericht), ≈ 5 Signalwechsel/Jahr, Spot, keine Derivate.

## 10. Umsetzung
- Code: `sleeves/sleeve_engine.py`, `sleeves/auswertung.py`, `sleeves/run_sleeves.py`, `sleeves/sleeves_bericht.py`, `paper/wochenbericht.py`, `collector/macro_sources.py` (Collector 1.3).
- Tests: `tests/test_sleeves.py`, `tests/test_collector_macro.py`.
