# MVRV_PREREG v0.1 — MVRV-Bewertungsband, BTC Spot long/Cash

**Status: ENTWURF. Nicht eingefroren, nicht gelaufen.** Kein Tag, kein Spec-SHA im Run-Log. Erst nach Review Claude und Entscheid Damian einfrieren.
**Erstellt:** 2026-10-01 22:30 (Zürich, UTC+2), aus Ideen-Scan v2 (Kandidat t1).

## 0. Vorbelastung und Deklaration
- Exploration t1 auf Daten < 2024 gesehen: Binance 2017-08 bis 2023 CAGR 51.6 %, Sharpe ex 1.06, MaxDD −63 %, 3 Wechsel; CoinMetrics 2014–2023 CAGR 62.2 %, Sharpe 1.18, 5 Wechsel. **In-Sample**, kein Beleg.
- Die Schwellen 1.0/3.5 stammen aus der Praktiker-Literatur und wurden in Kenntnis der Zyklen 2013/2017 gewählt (Folklore-Vorbelastung). MVRV-Spitzen < 2024 gesehen: 2017-12 4.72, 2021-02 3.96, 2021-10 2.93 (fallend).
- MVRV-Werte ≥ 2024 wurden **nicht** abgerufen oder berechnet. Der grobe BTC-Preispfad 2024–2026 ist als Marktwissen bekannt.
- Globaler Trial-Zähler ca. 270.

## 1. Hypothese
H-MVRV: Eine Regel «BTC halten, ausser MVRV war über 3.5, bis MVRV unter 1.0 fällt» reduziert den Drawdown gegenüber Buy&Hold, ohne die langfristige Rendite wesentlich zu senken.

## 2. Regel (ex ante fixiert)
- Daten: CoinMetrics Community `CapMVRVCur` (BTC, täglich), Wert für Tag t wird an t+1 00:00 UTC verwendet (1 Tag Lag), Ausführung Tages-Open t+1 Kraken BTC/USD Spot.
- Zustand: Start investiert, falls MVRV_Start ≤ 3.5, sonst Cash. Wechsel nach Cash, wenn MVRV > 3.5; Rückkehr in BTC, wenn MVRV < 1.0. Keine weiteren Parameter.
- Cash zu DTB3 (Sensitivität 0 %), Kosten K1 0.47 %/Seite (Sensitivität taker_K2).

## 3. Testbarkeit (ehrlich)
- Im Fenster 2024-01-02 bis 2026-09-30 sind nur 0–2 Ereignisse zu erwarten. Ohne Ereignis ist die Regel identisch mit Buy&Hold → **keine Aussage möglich**.
- Daher zweistufig:
  - Stufe 1 (einmaliger Retro-Lauf 2024–2026): nur Prüfung, ob die Regel mechanisch korrekt arbeitet und ob Ereignisse eintraten; Bericht deskriptiv, **kein Erfolgskriterium**.
  - Stufe 2 (Forward-Paper ab Freeze): Auswertung erst nach dem ersten vollständigen Zyklus (Ausstieg und Wiedereinstieg) oder spätestens 2030-12-31, je nachdem was früher eintritt.

## 4. Gates (Stufe 2)
- G1: MaxDD ≤ 2/3 × MaxDD Buy&Hold über den Auswertungszeitraum.
- G2: CAGR ≥ CAGR Buy&Hold − 5 Pp/J.
- G3: Falls bis 2030-12-31 kein Ausstieg (MVRV nie > 3.5): Hypothese gilt als **nicht prüfbar**, Regel wird verworfen (sie hat dann nur Komplexität ohne Wirkung).
- Mehrfachtest: gemeinsamer Rahmen mit Entwurf A (Holm über 2).

## 5. Kill-Regel
- G1 oder G2 verfehlt oder G3 eintritt → MVRV-Linie geschlossen, keine Nachjustierung der Schwellen (z. B. 3.0 oder MVRV-Z).

## 6. Aufwand Damian
≈ 5 Min./Woche (eine Zahl prüfen), erwartet < 1 Trade/Jahr; steuerlich günstig (wenige Transaktionen, lange Haltedauer).

## 7. Offene Fragen an Claude
1. Lohnt eine Prereg für eine Regel mit N ≈ 1 Ereignis pro 4 Jahre, oder besser als dokumentierte «Kernbestand-Leitplanke» ohne Erfolgsanspruch führen?
2. Sind 3.5/1.0 vertretbar, wenn die Spitzen fallen (2021-10 nur 2.93)? Alternative wäre eine rollierende Perzentil-Schwelle, die aber neue Freiheitsgrade schafft.
3. Ist das Datum 2030-12-31 als Abbruch sinnvoll?
