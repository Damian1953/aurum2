# Geplante Forschungsstränge nach Stufe 2, Version 1

**Project Aurum II, 16.09.2026. Reihenfolge festgelegt. Nur Priorität 1 ist in Arbeit, die übrigen sind dokumentiert und nicht gestartet.**

## Grundregel

Stufe 2 ist historische Evidenz und wird nicht rückwirkend verändert. Jede neue Erkenntnis erzeugt eine neue Hypothese in einem neuen Strang. Kein Ergebnis eines Strangs wird benutzt, um einen Stufe-2-Test in «bestanden» umzudeuten. Jeder Strang erhält vor dem ersten Rechenlauf einen geprüften Plan mit Prüfsumme in `00_doku/ENTSCHEIDE.md`.

## Priorität 1, in Arbeit: 03_woo_mtp_reverse_engineering

Rekonstruktion der öffentlich sichtbaren Mechanik von Market Trend Pro aus Primärdaten (Defaults des Backtesters, sechzehn BTC-Trades). Prüfung, ob die Stufe-2-Woo-Matrix dasselbe System abgebildet hat. Erfolgsmass ist Reproduktionsgenauigkeit, keine Performancekennzahl. Plan: `03_woo_mtp_reverse_engineering/mtp_reverse_engineering_plan_v1.md`. Status: Plan zur Prüfung, kein Rechenlauf.

## Priorität 2, geplant: 03_xs21_point_in_time

Ziel: Survivorship-Bias des in Stufe 2 bestandenen XS21 Long+Short prüfen. Rekonstruktion eines Point-in-Time-Universums, das zu jedem Stichtag nur die damals auf Binance USDT-M oder Kraken handelbaren Coins enthält, einschliesslich später delisteter. Universum, Regeln und Kriterien werden vor dem Lauf eingefroren, XS21-Regeln aus Stufe 2 unverändert. Offene Punkte für den Plan: Quelle der historischen Listungen und Delistungen, Behandlung von Coins ohne vollständige Historie, Mindestliquidität als Point-in-Time-Regel. Nicht gestartet.

## Priorität 3, geplant: 03_dcc_kraken_validation

Ziel: D-CC Cash-and-Carry mit längerer Kraken-Funding-Historie und einem realistischen Kapital- und Ausführungsmodell unabhängig validieren. Zentral bleibt die in Stufe 2 nicht bestandene Kraken-Vorzeichen-Gegenprobe (78.8 bis 88.3 Prozent statt 90). Offene Punkte für den Plan: Beschaffung der Kraken-Funding-Historie über mehr als ein Jahr, Margin-Modell für Spot long plus Perp short, Ausführung beider Beine, Basisrisiko und Liquidation, Kraken-Gebühren statt Binance-Sätzen. Nicht gestartet.

## Priorität 4, geplant: 03_woo_forward_spot

Ziel: Woo-Long-Ansatz auf Spot im Forward- oder Paper-Test beobachten. Stufe 2 hat gezeigt, dass Spot für die Woo-Long-Seite drei bis sechs Prozentpunkte günstiger war als Perps und dass Shorts keinen Edge zeigten, deshalb primär Spot, Long. Der Forward-Test soll auf der in Priorität 1 rekonstruierten MTP-nahen Mechanik beruhen, nicht vorschnell auf der Stufe-2-Matrix W2, W4, W6, W7. Verwerfungsregel und Beobachtungsdauer werden vor dem Start festgelegt. Nicht gestartet, abhängig von Priorität 1.
