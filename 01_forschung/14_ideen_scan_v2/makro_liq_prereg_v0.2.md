# MAKRO_LIQ_PREREG v0.2 — Fed-Netto-Liquiditäts-Regime, BTC Spot Kraken (Forward-Paper)

**Status: ENTWURF v0.2. Nicht eingefroren, nicht gelaufen.** Kein Tag, kein Spec-SHA im Run-Log, kein Runner gebaut.
**Stand:** 2026-10-01 22:40 (Zürich, UTC+2). Grundlage: Entscheid Chief Strategist 2026-10-01 22:40 (ENTSCHEIDE), **Vetorecht Damian vorbehalten**. Ersetzt `makro_liq_prereg_entwurf_v0.1.md` (bleibt unverändert liegen).
**Freeze erst nach:** Review Claude, kein Veto Damian, Runner und Collector-Erweiterung gebaut und getestet.

## 0. Änderungen gegenüber v0.1
- **Kein Retro-Test 2024–2026.** Wegen Kontext-Vorbelastung (Marktwissen über BTC- und Fed-Bilanz-Pfad) zählt 2024–2026 nicht als Testfenster. Erlaubt ist höchstens ein **deskriptiver Anhang ohne Entscheidungsgewicht** (§8).
- Hypothese wird **nur forward** im Paper geprüft, als zusätzlicher Sleeve neben PAPER v1.0, aber mit eigenem Runner und eigener Freeze-Liste. `paper/` und die Dateien der Freeze-Liste `paper-v1.0-freeze` werden nicht verändert.
- Datenquellen, Publikationsverzug und As-of-Regeln präzisiert (§3). Signal einen Tag später ausgeführt (Freitag-Schluss → Samstag-Eröffnung), damit die H.4.1-Daten sicher vor der Entscheidung erfasst sind.
- Review-Termine und Langfrist-Auswertung mit Kill-Regeln (§6, §7).

## 1. Vorbelastung
- Exploration t7 auf Daten < 2024 (In-Sample, kein Beleg): CAGR 48.6 %, Sharpe ex 0.98, MaxDD −63 %, 32 Wechsel; ab 2021 Sharpe 0.63 (B&H 0.48).
- Grober Verlauf 2024–2026 von BTC und Fed-Bilanz als Marktwissen bekannt; keine Signalwerte ≥ 2024 berechnet.
- Globaler Trial-Zähler ca. 270; diese Vorregistrierung fügt keinen Trial hinzu (Forward).

## 2. Hypothese
H-LIQ: Ein BTC-Spot-Sleeve, der nur investiert ist, wenn die Fed-Netto-Liquidität über 13 Wochen gestiegen ist, erzielt forward nach K1-Kosten eine Sharpe-Ratio mindestens gleich wie BTC Buy&Hold und einen MaxDD von höchstens zwei Dritteln des Buy&Hold-MaxDD.

## 3. Daten, Publikationsverzug, As-of
| Reihe | Quelle (ohne Key) | Stichtag | Publikation | Einheit |
|---|---|---|---|---|
| WALCL (Fed-Bilanzsumme) | FRED `fredgraph.csv?id=WALCL`, Quelle Federal Reserve H.4.1 | Mittwoch w | H.4.1 donnerstags 16:30 ET (Do 20:30/21:30 UTC je nach Sommer-/Winterzeit; FRED meist am selben Abend) | Mio. USD |
| WTREGEN (Treasury General Account) | FRED, Quelle H.4.1 | Mittwoch w | wie WALCL | Mio. USD |
| RRPONTSYD (Overnight Reverse Repo) | FRED, Quelle NY Fed | täglich, verwendet Mittwoch w | NY Fed am selben Tag nachmittags ET, FRED meist am folgenden Geschäftstag | Mrd. USD |
| BTC/USD 1d | Collector `data_live/kraken_ohlc/BTCUSD_1d.csv` (öffentliche Kraken-API) | Tagesbar UTC | laufend | USD |
| DTB3 | FRED | täglich | Folgetag | % p. a. |

- **Erfassung:** Eine Collector-Erweiterung (neu, eigene Version, nicht Teil von `paper/`) lädt täglich um 06:15 Zürich die drei FRED-Reihen als vollständigen CSV-Schnappschuss, append-only, mit Abrufzeitpunkt (UTC) und SHA256. Massgebend ist je Beobachtung der **Wert beim ersten Abruf** (First-Release); spätere Revisionen werden protokolliert, ändern aber keine Entscheidung.
- **As-of-Regel:** Für die Woche w gilt NL_w = WALCL_w − WTREGEN_w − 1000 × RRPONTSYD_(Mittwoch w). Diese Werte dürfen nur verwendet werden, wenn ihr erster Abruf **vor dem Schluss des Signalbars** (Freitag w+2 Tage, 24:00 UTC) liegt. Signal am Schluss des Freitagsbars, Fill zur Eröffnung Samstag (Kraken handelt durchgehend).
- **Verspätungen:** Fehlt H.4.1 für w bis zum Freitagsschluss (Feiertag, Shutdown), bleibt der Zustand unverändert; keine Nachbuchung. Fehlt RRPONTSYD für Mittwoch, gilt der letzte vorherige Tageswert mit erstem Abruf vor dem Signalbar.
- **Ausfall:** Liefert eine Reihe ≥ 8 Wochen keine neuen Werte, oder ändert die Fed die Definition der Reihe, stoppt der Sleeve fail-closed (Position bleibt bis Entscheid; Meldung im Wochenbericht).
- **Kein Look-ahead:** Der Runner prüft bei jedem Lauf, dass jede verwendete Beobachtung einen ersten Abrufzeitpunkt < Signalbar-Schluss hat; sonst Fehler. Test dazu vor dem Freeze (synthetische Daten mit verspätetem Abruf).

## 4. Regel
- Signal S_w = 1, wenn NL_w − NL_(w−13) > 0, sonst 0. Benötigt 14 First-Release-Wochen; für das Warmup vor dem Start dürfen die beim ersten Collector-Abruf vorhandenen Werte verwendet werden (als «Warmup ohne PiT» gekennzeichnet, keine Bewertung).
- Position: 100 % des Sleeve-Kapitals BTC bei S=1, 0 % (Cash) bei S=0. Keine Hebel, keine Derivate.
- Start: erster Signal-Freitag nach dem Freeze. Der Sleeve übernimmt den dann gültigen Zustand (Zustandsregel, kein Kreuzungsereignis). Abweichung von PAPER v1.0 F5 («Start flach») bewusst; Frage an Claude.
- Sizing: virtuell 1'000 USD, Zinseszins.
- Kosten: `config/cost_model_v1.json` `venue_kraken`, **primär `maker_plan`** (= K1, 0.47 % je Seite), **Pflicht-Sensitivität `taker_K2`**.
- Cash: primär ohne Zins (Konvention PAPER v1.0 F3); berichtet: Cash zu DTB3.

## 5. Benchmarks und Metriken
- B1: BTC Buy&Hold Kraken, Kauf zur Eröffnung des ersten Fill-Tags, gleiche Kosten.
- B2: DTB3 aufgezinst.
- R1 (nur Bericht): W2-BTC-Sleeve aus PAPER v1.0 (Redundanz-Prüfung), Korrelation der Exposition.
- Berichtet: DXY-Sensitivität (DTWEXBGS < SMA100) **rein deskriptiv**, keine zweite Hypothese.
- Metriken: Sharpe ex (täglich, annualisiert), CAGR, MaxDD, Anzahl Wechsel, Zeit im Markt, Kosten kumuliert.

## 6. Review-Termine (Betrieb, kein Leistungsurteil)
- **2027-02-02** (gleichzeitig mit dem PAPER-v1.0-Review): nur Betrieb. Prüfen: Collector-Abrufe vollständig, First-Release-Protokoll, As-of-Prüfung ohne Fehler, Signale reproduzierbar aus dem Schnappschuss-Archiv, Kosten korrekt gebucht, Feiertagsfälle. Kein Urteil über Rendite oder Drawdown; Leistungszahlen werden im Review nicht diskutiert.
- Danach jährlich im Oktober (2027-10, 2028-10, …) gleiche Betriebsprüfung.
- Zwischen den Terminen nur Betriebs-Kill (§3 Ausfall, nachgewiesener Look-ahead oder Codefehler). Ein Codefehler wird nur mit neuer Version und ENTSCHEIDE-Eintrag behoben; betroffene Periode wird gekennzeichnet.

## 7. Langfrist-Auswertung und Kill-Regel
- **Auswertungszeitpunkt:** erster Oktober-Termin, an dem **≥ 3 Jahre Forward und ≥ 10 Signalwechsel** vorliegen; spätestens **2031-10-01** (dann mit der vorhandenen Anzahl Wechsel).
- **Gates** (alle, maker_plan):
  - G1: Sharpe ex Sleeve ≥ Sharpe ex B1.
  - G2: |MaxDD Sleeve| ≤ 2/3 × |MaxDD B1|.
  - G3: CAGR Sleeve > CAGR B2.
  - G4: G1–G3 auch unter taker_K2 erfüllt.
- Statistik berichtet: Ledoit-Wolf-(2008)-Bootstrap der Sharpe-Differenz; Holm über die zwei Forward-Hypothesen (H-LIQ, H-MVRV) jeweils zum Zeitpunkt der zweiten Auswertung. p > 0.10 bei erfüllten Gates = «nicht widerlegt».
- **Kill:** Ein Gate verfehlt → Linie geschlossen, keine Varianten (andere Fenster, DXY, Realzinsen) nachschieben. Unter 10 Wechseln bis 2031-10-01 → «nicht prüfbar», Linie geschlossen.
- **Erfolg:** nur Empfehlung an Damian für Micro-Live; Entscheid D2 bei Damian.

## 8. Deskriptiver Anhang 2024–2026 (ohne Entscheidungsgewicht)
- Darf nach dem Freeze **einmal** gerechnet und gezeigt werden, Kennzeichnung «deskriptiv, kein Test, Kontext-Vorbelastung».
- FRED-Werte nach Möglichkeit als ALFRED-Vintage (First-Release); falls ohne Key nicht verfügbar, aktuelle Werte mit Vermerk.
- Ergebnis darf weder Regel, Parameter noch Gates ändern und wird bei der Auswertung (§7) nicht berücksichtigt.

## 9. Aufwand Damian
≈ 10 Min./Woche (Wochenbericht lesen), ≈ 5 Signalwechsel/Jahr, Spot, keine Derivate.

## 10. Fragen an Claude
Siehe `an_claude_scan_v2.md`.
