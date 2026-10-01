# Forschung

Sechs Stufen. Jede Stufe hat eine Vorregistrierung vor dem ersten Rechenlauf und einen Ergebnisbericht danach. Ein negatives Ergebnis wird gleich sorgfaeltig dokumentiert wie ein positives.

| Stufe | Frage | Ordner |
|---|---|---|
| 0 | Sind Daten und Kosten belastbar? | `00_datenbasis/` |
| 1 | Existieren robuste Regime? | `01_regime/` |
| 2 | Hat eine Strategie ohne Filter einen Edge? | `02_strategien/` |
| 3 | Bringt der eingefrorene Filter Zusatzwert? | `03_regime_wert/` |
| 4 | Sind Funding und Basis eine eigene Ertragsquelle? | `04_funding_basis/` |
| 5 | Helfen Makro- und Flow-Overlays? | `05_overlays/` |

## Regeln fuer jede Stufe

- Nullhypothese zuerst. Geprueft wird, was widerlegt werden soll, nicht was bestaetigt werden soll.
- Walk-Forward mit strikter Trennung. Der Test-Split wird genau einmal und zuletzt verwendet.
- Purging und Embargo an den Fenstergrenzen, mindestens in Laenge der maximalen Haltedauer.
- Jede getestete Konfiguration wird protokolliert, auch die verworfenen.
- Berichtet wird die Verteilung ueber die Parameterfamilie, nie der Bestwert.
- Alle drei Kostenszenarien. Ein Edge nur im optimistischen Szenario ist kein Edge.
- Deflated Sharpe und Probability of Backtest Overfitting sind Pflicht.
- Robustheit gegen Ausreisser wird immer ausgewiesen.
- Point-in-Time, inklusive delisteter und gescheiterter Coins.
