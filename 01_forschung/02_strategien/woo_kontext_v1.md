# Travis Woo und Market Trend Pro, Interpretationskontext

**Project Aurum II. Stand 15.09.2026. Dieses Dokument enthält Kontext und Hypothesen, keine Regeln. Die Regeln stehen ausschliesslich in `stage2_preregistration_v1.md`.**

## 1. Öffentlich beschriebene Herkunft

Woo nennt Richard Dennis und das Turtle-Trading sowie Mark Minervini als Einflüsse. Für die Rekonstruktion heisst das:

- Donchian- oder N-Tage-Ausbrüche, ATR- und Volatilitätslogik, Pyramiding in laufende Gewinner und ein Ertragsprofil mit vielen kleinen Verlusten und wenigen grossen Gewinnern sind plausible Bausteine.
- Originale Turtle-Parameter (20/10, 55/20, N gleich ATR20, Units zu 0.5N) werden **nicht** als übernommen unterstellt.
- Von Minervini stammt das Prinzip, Stärke zu kaufen und Ausbrüche auf neue Hochs zu bevorzugen. MTP dürfte daher eine Kombination aus langfristigem Filter, New-High-Ausbruch und mechanischem Exit sein, kein Indikator-Mix.

## 2. Woo Legacy gegen MTP 2.4

| Element | Woo Legacy | MTP 2.4 (öffentlich bestätigt) |
|---|---|---|
| Langfristiger Filter | SMA200 Long-Filter | langfristiger Filter, Form nicht präzisiert |
| Einstieg | ATH- und Ausbruchseinstiege, Calendar-Low-Reclaim-Dips | Breakout Buy als Einstieg oder Add-on |
| Stopp | 3 bis 4 ATR | ratcheting, bei weiteren Breakout-Käufen nach oben angepasst |
| Pyramiding | ja | ja, über Breakout-Add-ons |
| Gewinnziel | keines, stark belegt | unklar, widersprüchliche Hinweise |
| Richtung | Long oder Cash | Long oder Cash |
| Parameter | – | über Assets robuste, mittlere Einstellungen |

Keine Legacy-Regel wird automatisch als MTP-2.4-Regel behandelt. Calendar-Low-Reclaim-Dips sind in Stufe 2 nicht enthalten.

## 3. Was Stufe 2 davon testet

Die Matrix W0 bis W8 bildet den gemeinsamen Kern beider Fassungen ab: langfristiger Filter, Ausbruch auf neue N-Tage-Hochs, ATR-Stopp mit Nachziehen, Pyramiding mit Stopp-Anhebung (W6, W7), kein Gewinnziel, Long oder Cash. Die MTP-2.4-Bestätigung, dass ein Breakout Buy Einstieg oder Add-on sein kann und der Stopp bei weiteren Käufen steigt, entspricht der Pyramiding-Definition in Abschnitt 10 der Vorregistrierung.

**Signal-Engine und Risikoschicht sind getrennt.** Positionsgrösse, Prozentrisiko und Teile der Stopp-Einstellungen sind bei MTP nutzerkonfigurierbar. Stufe 2 prüft die Qualität der Signal- und Exit-Logik mit einheitlichem Notional-Sizing und beurteilt nicht Woos persönliche Kapital- oder Hebelwahl.

**Parameterwahl.** Woos eigene Beschreibung, viele Parameter über mehrere Assets zu testen und danach mittlere Einstellungen zu wählen, bestätigt den Plateau-Ansatz der Vorregistrierung (Abschnitt 17). Das ist methodischer Kontext, kein Optimierungsziel und keine Rechtfertigung für eine grössere Matrix.

## 4. Fingerprint, Unsicherheiten

- Signalhäufigkeit: öffentlich rund 8 je Asset und Jahr, an anderer Stelle 1 bis 3 je Monat. Vermutlich verschiedene Zählweisen oder Versionen. Als unsicherer Fingerprint geführt, nicht als hartes Ziel.
- Haltedauer: rund 90 Tage im Mittel, Gewinner deutlich länger. Plausibilitätsmerkmal, kein Optimierungsziel.
- Gewinnziel: bei MTP 2.4 unklar. Nicht als gesicherte Regel behandeln.

## 5. Shorts

Der öffentlich erkennbare MTP-Kern ist Long oder Cash. Die Short-Spiegelungen W2S, W4S, W8S sind Aurum-Erweiterungen und werden nicht als Woo-Strategie bezeichnet und nicht gegen den MTP-Fingerprint gemessen.

## 6. Hypothesen für spätere Versionen, nicht Teil von Stufe 2

- Calendar-Low-Reclaim-Dips als Einstiegsvariante (Legacy).
- ATH-Ausbruch als Sonderfall des 252-Tage-Ausbruchs mit längerem Fenster.
- Nutzerkonfigurierbares Prozentrisiko als Sizing-Schicht, sobald eine Signal-Logik bestanden hat.
