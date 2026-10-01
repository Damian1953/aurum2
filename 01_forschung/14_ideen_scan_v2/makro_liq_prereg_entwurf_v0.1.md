# MAKRO_LIQ_PREREG v0.1 — Fed-Netto-Liquiditäts-Regime, BTC Spot long/Cash

**Status: ENTWURF. Nicht eingefroren, nicht gelaufen.** Kein Tag, kein Spec-SHA im Run-Log. Erst nach Review Claude und Entscheid Damian einfrieren.
**Erstellt:** 2026-10-01 22:30 (Zürich, UTC+2), aus Ideen-Scan v2 (Kandidat t7).

## 0. Vorbelastung und Deklaration
- Exploration t7 (und t6, DXY) auf Daten < 2024 gesehen: 2017-08 bis 2023 CAGR 48.6 %, Sharpe ex 0.98, MaxDD −63 %, 32 Wechsel; ab 2021 Sharpe 0.63. Diese Periode ist **In-Sample** und zählt nicht als Beleg.
- Für das Signal (Netto-Liquidität) wurden **keine** Resultate ≥ 2024 berechnet. Aber: der grobe BTC-Preispfad 2024–2026 und der grobe Pfad der Fed-Bilanz (QT, Abbau Reverse Repo) sind dem Team als allgemeines Marktwissen bekannt. Das ist eine unvermeidbare Kontext-Vorbelastung; sie wird hiermit offengelegt.
- Kraken-Spot-Preise ≥ 2024 sind nicht Teil von `02_daten/holdout/` (Binance-basiert); der Holdout bleibt geschlossen.
- Globaler Trial-Zähler beim Einfrieren: ca. 270 (siehe `ideen_scan_v2.md` §4).

## 1. Hypothese
H-LIQ: Eine BTC-Spot-Position, die nur gehalten wird, wenn die Fed-Netto-Liquidität über 13 Wochen gestiegen ist (sonst Cash), liefert im Testfenster eine **bessere risikoadjustierte Rendite und einen deutlich kleineren Drawdown** als BTC Buy&Hold, nach K1-Kosten.

## 2. Regel (vollständig, ex ante fixiert)
- NL_w = WALCL_w − WTREGEN_w − RRPONTSYD_(Mittwoch w) × 1000 (alle in Mio. USD; RRP in Mrd. → ×1000). Wert für Mittwoch w.
- Signal S_w = 1, wenn NL_w − NL_(w−13) > 0, sonst 0.
- Point-in-Time: nur Werte, die laut ALFRED-Vintage (realtime_start) am Entscheidungszeitpunkt verfügbar waren. H.4.1 erscheint donnerstags 16:30 ET → Entscheid Freitag 00:00 UTC, Ausführung Freitag zum Tages-Open (Kraken BTC/USD Spot, 1d). Fehlt ein Wert (Feiertag), gilt der letzte verfügbare.
- Position: 100 % BTC bei S=1, 100 % Cash bei S=0. Keine Hebel, keine Derivate.
- Cash verzinst mit DTB3 (Sensitivität: 0 %).
- Kosten: K1 Spot 0.47 % je Seite. Sensitivität: taker_K2 (gemäss Kostenmodell im Repo).

## 3. Daten
- Kraken BTC/USD Spot 1d (Collector/Archiv), FRED/ALFRED `WALCL`, `WTREGEN`, `RRPONTSYD`, `DTB3`. SHA256 aller Eingaben im Run-Log.
- Testfenster: **2024-01-05 bis 2026-09-25** (Freitage), einmaliger Lauf.

## 4. Kennzahlen und Gates (alle müssen erfüllt sein)
- G1: Sharpe ex (täglich, annualisiert) ≥ Sharpe ex Buy&Hold.
- G2: MaxDD ≤ 2/3 × MaxDD Buy&Hold (absolut).
- G3: CAGR > DTB3-Rendite im Fenster.
- G4: Robustheit: G1–G3 auch mit taker_K2 und Cash 0 %.
- Berichtet (nicht Gate): Vergleich gegen SMA200-Regel (W2-Nähe), Korrelation mit W2-Exposition, Anzahl Wechsel, Sensitivität DXY < SMA100 (t6) rein deskriptiv.
- Statistik: Sharpe-Differenz H-LIQ vs. B&H mit Ledoit-Wolf-(2008)-Bootstrap, einseitig. Bei ≈ 2.7 Jahren ist die Teststärke gering; ein p-Wert > 0.10 bei erfüllten Gates heisst «nicht widerlegt», nicht «bestätigt».
- Mehrfachtest: gemeinsamer Rahmen mit MVRV-Entwurf B, Holm über 2 Hypothesen.

## 5. Kill-Regel
- Ein Gate verfehlt → Makro-Liquiditätslinie geschlossen (ENTSCHEIDE-Eintrag), keine Varianten (andere Fenster, DXY, Realzinsen) nachschieben.
- Gates erfüllt → nur Paper-Erweiterung (PAPER v1.1, eigene Prereg) neben W2/W6/Turtle, ≥ 6 Monate; Micro-Live nur mit Entscheid Damian.

## 6. Aufwand Damian
≈ 10 Min./Woche (Freitag Signal ablesen), ≈ 5 Trades/Jahr, nur Spot.

## 7. Offene Fragen an Claude
1. Ist 2024–2026 trotz Kontextwissen über BTC- und Fed-Pfad als Test vertretbar, oder nur Forward-Paper?
2. Gate G2 (2/3 MaxDD) sinnvoll oder zu leicht, da Buy&Hold-Drawdowns in Krypto gross sind?
3. Soll die Hypothese relativ zu SMA200 statt zu Buy&Hold formuliert werden (Redundanz mit W2)?
4. ALFRED-Vintages Pflicht oder genügen aktuelle FRED-Werte (geringe Revisionen der H.4.1-Daten)?
