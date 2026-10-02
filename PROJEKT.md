# Aurum II – Projektbeschreibung

## Ziel

Ein profitables und robustes Krypto-Trading-Tool für ein Schweizer Privatkonto.
Robust heisst: Eine Strategie wird nur weiterverfolgt, wenn sie ausserhalb der
Stichprobe trägt. Gute Zahlen in der Stichprobe genügen nicht.

## Rollen

| Rolle | Wer | Verantwortung |
|---|---|---|
| Eigentümer | Damian | Entscheidet über Geld und Keys |
| Projektleitung | Aurum II Bot | Strategie, Anforderungen, Risikoregeln, Review, Reporting |
| Chefprogrammierer | Andreas | Umsetzung von Engine, Collector, Runner und Tests |
| Methodik und Zweitmeinung | Claude | Methodik-Reviews und unabhängige Zweitmeinungen |

## Aktueller Strategiestatus

- **Lane A:** geschlossen.
- **XS21:** falsifiziert.
- **Carry:** verworfen.
- **Paper W2/W6/Turtle 55/20:** läuft seit 2026-10-02, Review spätestens 2027-02-02.
- **Sleeves A (Fed-Liquidität) und B (MVRV):** gebaut, warten auf Claudes Review.
  Sie sind nicht eingefroren, nicht in cron und nicht gelaufen.

Massgeblich sind die einzelnen Entscheide in `00_doku/ENTSCHEIDE.md`.

## Governance

1. **Vorregistrierung:** Hypothese, Daten, Parameter und Abbruchkriterien werden
   vor dem Lauf schriftlich festgelegt.
2. **Freeze mit SHA:** Code, Konfiguration und Prereg werden mit Prüfsummen
   eingefroren und getaggt. Danach werden eingefrorene Dateien nicht mehr geändert.
3. **Genau ein Lauf:** Pro Freeze gibt es genau einen Lauf. Es gibt kein
   Nachjustieren und keine Wiederholung mit anderen Parametern.
4. **Holdout nie geöffnet:** Holdout- und Validation-Daten werden ausserhalb
   des vorregistrierten Laufs weder gelesen noch angezeigt oder durchsucht.
5. **Alle Trials deklariert:** Jede getestete Variante wird gezählt und
   dokumentiert, auch die verworfenen.

## Risiko- und Sicherheitsregeln

- Vorerst gibt es nur Backtests und Paper-Trading, keinen Live-Handel.
- Künftige Live-Keys:
  - haben nur Trade-Rechte und keine Withdrawal-Rechte;
  - haben feste Limits je Trade;
  - liegen auf Damians eigenem Server und nie auf der geteilten Bot-Maschine.
- Jede echte Order braucht Damians Freigabe.
- Im Repo liegen keine Secrets: keine Keys, Tokens oder Passwörter, auch nicht
  in der History.

## Zeitbudget

Damian investiert höchstens 1 Stunde pro Woche. Berichte und Entscheidvorlagen
sind deshalb knapp und enthalten eine klare Empfehlung.

## Weiterführende Dokumente

- [`00_doku/ENTSCHEIDE.md`](00_doku/ENTSCHEIDE.md): Entscheidprotokoll (append-only)
- [`OFFENE_PUNKTE.md`](OFFENE_PUNKTE.md): offene Punkte und Pendenzen
- [`DATA.md`](DATA.md): Datenquellen, Ablage und Holdout-Regeln
- [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md): Reproduzierbarkeit, Freeze und Verifikation
