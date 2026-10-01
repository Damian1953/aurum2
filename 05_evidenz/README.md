# Evidenz

## Kostenmodell

Eine versionierte Datei, drei Szenarien, keine Ausnahmen.

| Groesse | Optimistisch | Realistisch | Konservativ |
|---|---|---|---|
| Spot Taker je Seite | 0.26 % | 0.40 % | 0.55 % |
| Spot Maker je Seite | 0.16 % | 0.25 % | 0.35 % |
| Perp Taker je Seite | 0.05 % | 0.075 % | 0.10 % |
| Spread | gemessen | gemessen mal 1.5 | gemessen mal 3 |
| Slippage | groessenabhaengig | groessenabhaengig | groessenabhaengig mal 2 |
| Funding | tatsaechlich | tatsaechlich | tatsaechlich mal 1.5 |

Spread-Werte stammen aus eigener Messung. Ein Edge, der nur im optimistischen Szenario existiert, existiert nicht.

## Gates vor Kapital

- Beta-Trennungstest: Die Strategie muss eine passive Position gleicher Durchschnittsexposure risikoadjustiert schlagen.
- Kostenfilter vor jedem Einstieg: erwarteter Vorteil groesser als Gebuehr plus Spread plus Slippage plus Funding plus Sicherheitsaufschlag.
- Deflated Sharpe und Probability of Backtest Overfitting.
- Bootstrap, Fuenf-Prozent-Perzentil ueber dem Cash-Ertrag.
- Mindestens 90 Tage und 100 Trades fuer ein Urteil. Warnschwelle unter 30 Trades.
- Mindestens sechs Monate fuer Rebalance-Strategien.
- Robustheit ohne die drei besten Ereignisse wird immer ausgewiesen.

## Lauf-Registratur

Jeder Rechenlauf wird eindeutig identifiziert durch Strategie-Version, Daten-Version, Konfigurations-Hash und Zufallsstartwert. Ohne Registratur-Eintrag existiert ein Ergebnis nicht.

## Kennzahlen, die nie vermischt werden

1. Vereinfachtes Signalmodell
2. Modellierter Full-Live-Replay
3. Tatsaechliche Live-P&L

Im Altprojekt lagen diese drei Groessen bei 52 Prozent, 43 Prozent und negativ.
