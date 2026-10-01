# Engine

Noch nicht gebaut. Beginn erst nach Abschluss der Forschungsstufe 2 mit positivem Ergebnis.

## Modulplan

```
core/       Zeit, Typen, Fehler, Konfiguration, Logging
costs/      Gebuehren, Spread, Slippage, Funding
data/       Ingest, Validierung, Speicher, Universum
features/   Indikatoren, rein und kausal
regime/     Zustandsklassifikation, eingefroren und versioniert
strategy/   Signalgeneratoren, liefern Zielexposure
portfolio/  Aggregation der Sleeves, Netting Spot gegen Perp
risk/       Vetorecht, Limits, Stufen, Kill-Switch
execution/  Orderplanung, Idempotenz, Reconciliation
venue/      Kraken Spot und Futures hinter einer Schnittstelle
sim/        Backtest und Replay
research/   Stufenplan und Auswertung, schreibt nie nach live
ops/        Heartbeat, Waechter, Alarm, Tagesbericht
ui/         Lesende Ansicht
```

Abhaengigkeiten streng absteigend. Kein Modul importiert `venue` ausser `execution`. Keine Strategie kennt `execution`.

## Nicht erlaubt

Ein beschleunigter Backtest-Modus mit eigener Signalberechnung. Eine zweite Gebuehrenkonstante. Ein Order-Pfad ohne Kill-Switch-Pruefung. Ein Zaehler, der gegen die Prozesslaufzeit statt gegen den Kalender laeuft.
