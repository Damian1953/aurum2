# Bottom Engine — Architekturnotiz, Version 1

**Project Aurum II, `00_doku/bottom_engine_architecture_v1.md`. 18.09.2026. Zentrale neue Architekturhypothese nach den Läufen BTC Stufe A, XRP v1.0, DOT v1.0 und der Cross-Coin-Zusammenfassung v1. Keine Spezifikation, keine Zahlen, die vor einem Freeze eingefroren wären. Ersetzt in `architecture_update_v2.md` den Abschnitt zum Reversal-to-Trend-Layer, ändert nichts an Lane B, Lane C, Lane D oder an eingefrorenen Urteilen.**

## 1. Was die drei Läufe gezeigt haben

Ein einzelner 4h-Trade, der am Boden kauft, die Reversion mitnimmt, wochenlang den Trend hält und nahe am Hoch verkauft, existiert in den Daten nicht. Die Bottom-Signale (Failed Breakdown, Wick plus Volumen) liefern, wo überhaupt etwas messbar ist, eine kurze Reversion Richtung EMA20 (E0 mit bester Capture Ratio auf allen sechs Familien), aber mit einem Auszahlungsverhältnis, das bei K1 negativ bleibt. Die Strukturen (bestätigte Double Bottoms) liefern einen Kontext, in dem Trends häufiger beginnen als ohne Struktur (47 bis 71 Prozent gegen 34 bis 35 Prozent), aber erst nach Wochen, und keine der bisherigen Exit-Logiken hat diese Zeit gehalten. Reversion und Trend sind zwei verschiedene Zeitskalen, zwei verschiedene Exit-Logiken und zwei verschiedene Risiken. Sie in einen Trade zu zwingen, hat auf drei Coins denselben Fehler erzeugt.

## 2. Architektur

Die Bottom Engine ist eine reine Erkennungsschicht ohne Trade. Sie berechnet auf dem 4h-Raster aus der bestehenden Library (rlib v1.0, Feature Library v0.1, Derivatives Library v0.2) zwei getrennte Ausgaben, die von zwei getrennten Verbrauchern gelesen werden.

Ausgabe A, Bottom Signal: eine Kerze mit Kontext K1 bis K3 und qualifiziertem Rejection-Muster (Failed Breakdown, Wick plus Volumen, später weitere aus der Feature Library). Verbraucher: ein Short-horizon Rebound Sleeve, der Reversion monetarisiert, mit eigenem Einstieg, eigenem Stop, eigenem kurzen Ziel (EMA20 oder Gleichgewichtsregel) und eigener Entry-Ökonomie, die vor jedem Test festgelegt ist (REBOUND-20-Vorregistrierung). Haltedauer Stunden bis wenige Tage. Kein Trend-Exit.

Ausgabe B, Trend Context: ein Zustand, der durch eine bestätigte Struktur geöffnet wird (heute: Double Bottom mit Nackenlinienbruch, später gegebenenfalls Triple Bottom, 逆三尊, Zonenreclaim) und durch Zeit oder Invalidierung geschlossen wird. Der Kontext erzeugt keinen Trade. Verbraucher: ein Delayed Trend Entry Sleeve, der innerhalb des Kontextfensters auf einen eigenen, späteren Einstieg wartet (Retest, Higher Low, Konsolidierungsbreakout, DB-CONTEXT-Vorregistrierung), mit Trend-Exit auf Tagesbasis. Haltedauer Wochen. Kein Reversionsziel.

Kein Trade muss beide Aufgaben erfüllen. Ein Bottom Signal kann innerhalb eines offenen Trend Context auftreten, dann handeln beide Sleeves unabhängig nach ihren eigenen Regeln, ohne Kenntnis voneinander. Eine Kombination oder Priorisierung ist eine spätere Portfolio-Frage, keine Signalfrage.

## 3. Was die Trennung methodisch bedeutet

Jeder Sleeve hat seine eigene Kontrollgruppe: für Rebound die Kontextkerzen ohne Muster, für Delayed Trend die Selloff-Kontexte ohne bestätigte Struktur. Jeder Sleeve hat seine eigene Statuszuweisung, Evidenzklasse und sein eigenes Economic Validation Gate. Die drei Development-Coins (BTC, XRP, DOT) sind für beide Sleeves Hypothesengenerator, ETH und SOL die unabhängigen Tests. Die alten RTC-Spezifikationen (Stufe A v1.1, XRP v1.0, DOT v1.0) bleiben eingefroren und werden nicht fortgeführt, sie sind der Beleg dafür, warum die Trennung nötig ist.

## 4. Was offen bleibt

Ob die Reversion nach Selloff überhaupt eine positive Entry-Ökonomie hat, ist nach der Development-Prüfung (REBOUND-20 v0.1, Abschnitt 2) nicht belegt, das Auszahlungsverhältnis von rund 0.5 R Gewinn zu 1.3 R Verlust bei 50 Prozent Trefferquote ist auf drei Coins strukturell negativ. Ob der Trend Context nach Retest, Higher Low oder Breakout eine handelbare Erwartung hat, ist auf keinem Coin simuliert, weil die Mechanismen erst für ETH und SOL definiert wurden. Die Architektur ist damit eine Hypothese über die richtige Zerlegung, nicht über den Ertrag.
