# Review Claude zu Ideen-Scan v2: Sleeve A (MAKRO_LIQ) und Sleeve B (MVRV), Zusammenfassung v1

**Stand:** 2026-10-02 (Zürich, UTC+2). Zusammenfassung durch Aurum II Bot im Auftrag der Projektleitung, Grundlage: Review Claude zu `makro_liq_prereg_v0.2.md` und `mvrv_prereg_v0.2.md`.
**Status:** Umsetzung als Kandidaten `makro_liq_prereg_v1.0.md` und `mvrv_prereg_v1.0.md` (**Kandidat, nicht eingefroren**). Kein Freeze, kein Start, kein Trial. v0.2 bleibt unverändert liegen. Der Eintrag in `00_doku/ENTSCHEIDE.md` wird hier nicht verändert.

## 1. Pflichtänderungen

| Nr. | Punkt | Umsetzung |
|---|---|---|
| M1 | TGA von `WTREGEN` (Wochendurchschnitt) auf `WDTGAL` (Mittwochsstand) umstellen, auch im Collector. Prüfen, welche Reihe die Exploration t7 verwendet hat; falls `WTREGEN`, als Abweichung deklarieren. | Collector 1.3 lädt `WDTGAL` statt `WTREGEN`; Engine und Runner rechnen NL = WALCL − WDTGAL − 1000 × RRPONTSYD. **t7 (`tools/ideen/explorativ_scan_v2.py`, Zeile 166) hat `WTREGEN` verwendet** → als Abweichung deklariert (MAKRO_LIQ v1.0 §0b). |
| M2 | Testfälle vor dem Freeze für drei Szenarien: Freitagsabruf scheitert; H.4.1 verspätet oder verschoben; RRP fehlt am Mittwoch. Müssen grün sein. | `tests/test_sleeves.py`: `test_m2_friday_fetch_fails_state_unchanged_then_recovers`, `test_m2_h41_late_or_shifted`, `test_m2_rrp_missing_on_wednesday` (grün). |
| M3 | Ein gemeinsamer einseitiger Wochenbericht für PAPER v1.0, A und B mit fester Gestaltung. | `paper/wochenbericht.py` (nicht in einer Freeze-Liste, geprüft) mit festem `LAYOUT` (7 Abschnitte, höchstens 60 Zeilen), Abschnitte A und B aus `sleeves/sleeves_bericht.py`. Tests M3. |
| M4 | Redundanzregel A gegenüber W2-BTC: Besteht A alle Gates, ist die Korrelation der Exposition > 0.7 und die Sharpe-Ratio von A nicht höher als jene von W2-BTC, gilt A als redundant und erhält keine Micro-Live-Empfehlung. | MAKRO_LIQ v1.0 §7.3, `sleeves/auswertung.py` `redundant_a`, `verdict_a`, Tests. |
| M5 | A wird allein auf 5 % getestet; Holm-Korrektur entfällt. | MAKRO_LIQ v1.0 §7.2, `auswertung.ALPHA_A = 0.05`; MVRV ist nicht mehr in der Testfamilie. |

## 2. Weitere Punkte

- **Cash:** Standard Cash zu DTB3 (First-Release, act/360), Sensitivität Cash 0 %. Deklariert als **Abweichung von PAPER v1.0 F3** («kein Zins auf Cash»).
- **Start:** Start in gültigem Zustand (A übernimmt am ersten Signalfreitag den dann gültigen Zustand, B ist INVESTIERT bei MVRV ≤ 3.5). Deklariert als **Abweichung von PAPER v1.0 F5** («Start flach»). Der Einstieg wird mit Kosten gebucht.
- **Bericht B:** Ausdrücklich festhalten: Solange MVRV seit Start nie über 3.5 lag, ist B identisch mit Buy&Hold.
- **Calmar und Ulcer-Index:** nur berichten, keine Gates.
- **A:** Anzahl Regimephasen länger als 13 Wochen berichten.
- **B wird Kernbestand-Leitplanke:** Regel, Schwellen 1.0/3.5 und Datenquelle eingefroren und unverändert. Keine Gates, kein Erfolgsanspruch, kein Trial, nicht in der Testfamilie. Ausdrücklich: Erreicht MVRV 3.5 nicht mehr, löst die Regel nie aus, und das ist ein zulässiges Ergebnis.
- **Anhang §8:** Vermerk «nicht First-Release» (beide Vorregistrierungen).

## 3. Deklarierte Abweichungen (Übersicht)

1. TGA-Reihe `WDTGAL` statt `WTREGEN` gegenüber Exploration t7 und v0.2 (M1).
2. Cash zu DTB3 als Standard gegenüber PAPER v1.0 F3 (Cash 0 % nur noch Sensitivität).
3. Start in gültigem Zustand gegenüber PAPER v1.0 F5 (Einstieg mit Kosten gebucht).

## 4. Auslegungen der Umsetzung (zur Bestätigung durch die Projektleitung)

- M5: «allein auf 5 %» umgesetzt als zweiseitiger p-Wert des Ledoit-Wolf-(2008)-Bootstraps der Sharpe-Differenz A − B1; eine Micro-Live-Empfehlung setzt erfüllte Gates **und** p ≤ 0.05 voraus (sonst «nicht signifikant», keine Empfehlung).
- M4: Sharpe-Vergleich A gegen W2-BTC mit gleicher Cash-Konvention wie PAPER F3 (A-Konto Cash 0 %, maker_plan, gleiches Fenster); Expositions-Korrelation = Pearson der täglichen Positionen 0/1. Ist die Korrelation nicht bestimmbar (eine Reihe konstant), greift die Regel nicht, wird aber gemeldet.
- Stale-Regel: «eine Reihe ≥ 8 Wochen ohne neue Werte → STOPPED» gilt neu für WALCL, WDTGAL und RRPONTSYD (v0.2-Code prüfte nur WALCL).
