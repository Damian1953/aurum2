# Project Aurum II — Architektur und Umsetzung

**Stand 15.09.2026. Version 0.1, Entwurf zur Freigabe.**

Aurum II ist eine eigenständige Handelsplattform ausschliesslich für Kryptowährungen. Sie nutzt die Erkenntnisse aus Project Aurum, übernimmt aber keinen Code im Bestand. Grundlage dieses Dokuments ist der Findings-Digest vom 15.09.2026.

**Vier Vorgaben stehen fest.**

1. Forschung zuerst, danach Paper, danach allenfalls Live mit kleinem Kapital.
2. Gehandelt werden Spot **und** Perpetual Futures, in beide Richtungen.
3. Nur Kryptowährungen. Keine Aktien, keine tokenisierten Aktien, keine Rohstoffe.
4. Die im Digest belegten Fallen werden baulich ausgeschlossen, nicht durch Disziplin vermieden.

---

## 1. Leitsätze der Architektur

**Ein Kern, drei Betriebsarten.** Backtest, Paper und Live sind derselbe Code mit unterschiedlicher Ausführungsschicht. Es gibt keinen beschleunigten Backtest-Modus mit eigener Signalberechnung. Jede Abweichung zwischen diesen drei Wegen ist ein Fehler, kein Optimierungsspielraum.

**Forschung und Handel sind physisch getrennt.** Zwei Datenbanken, zwei Prozesse, zwei Konfigurationsbäume. Die Forschung darf den Handel niemals berühren, der Handel darf Forschungstabellen nur lesen. Im Altprojekt teilten sich beide eine Datenbank, was zu einem Testlauf führte, der den Not-Aus in der Produktion setzte.

**Das Kostenmodell ist die einzige Wahrheit.** Eine versionierte Datei definiert Gebühren, Spread-Annahmen, Slippage-Funktion und Funding. Kein Modul darf eine eigene Konstante halten. Im Altprojekt existierten vier widersprüchliche Gebührenwerte gleichzeitig.

**Alle Parameter an einem Ort.** Eine versionierte Parameterdatei mit Schema-Prüfung beim Start. Abweichungen zwischen Dokumentation und Code waren im Altprojekt Regel, nicht Ausnahme.

**Fail-closed überall.** Fehlt ein Datum, ist eine Serie zu alt oder wirft eine Berechnung eine Ausnahme, dann wird das Risiko kleiner und nicht grösser. Im Altprojekt gab das Regime-Gate bei Datenausfall den Wert für volles Risiko zurück.

**Eine Order-Pipeline, ein Lock.** Genau ein Prozess darf Orders erzeugen. Er hält ein prozessübergreifendes Lock mit Heartbeat. Jede Position trägt eine Eigentumsmarke, fremde Bestände werden nie angefasst.

---

## 2. Modulplan

```
aurum2/
  core/         Zeit, Typen, Fehler, Konfiguration, Logging
  costs/        Gebühren, Spread, Slippage, Funding. Single Source of Truth
  data/         Ingest, Validierung, Speicher, Point-in-Time-Universum
  features/     Indikatoren. Rein, kausal, ohne Seiteneffekte
  regime/       Zustandsklassifikation, eingefroren und versioniert
  strategy/     Signalgeneratoren. Liefern Zielexposure, keine Orders
  portfolio/    Aggregation der Sleeves zu einem Zielportfolio
  risk/         Vetorecht vor jeder Order. Limits, Stufen, Kill-Switch
  execution/    Orderplanung, Idempotenz, Reconciliation
  venue/        Kraken Spot und Kraken Futures hinter einer Schnittstelle
  sim/          Backtest und Replay. Nutzt execution und venue als Attrappe
  research/     Stufenplan, Auswertung, Berichte. Schreibt nie nach live
  ops/          Heartbeat, Wächter, Alarm, Tagesbericht
  ui/           Lesende Ansicht. Schreibende Endpunkte nur mit Token
```

**Sprache und Laufzeit**: Python 3.12, pandas und numpy, SQLite für die Handelsdatenbank, Parquet für Marktdaten und Forschungsergebnisse, FastAPI nur als lesende Oberfläche. Pytest als Testbasis. Kein Framework-Zuwachs ohne belegten Bedarf.

**Die Abhängigkeitsrichtung ist streng absteigend.** core, costs und data kennen niemanden über sich. strategy kennt features und regime, aber nicht execution. risk kennt portfolio, aber keine Strategie. Kein Modul importiert venue ausser execution.

---

## 3. Datenschicht

### 3.1 Der Datenvertrag

Jede Zeitreihe trägt Metadaten: Quelle, Zeitzone, Bar-Intervall, Regel zur Bar-Vollständigkeit, Erstabruf-Zeitpunkt, letzte Änderung, Versionsnummer. **Ein Bar gilt erst als lesbar, wenn er abgeschlossen ist.** Die Zugriffsschicht gibt einen laufenden Bar gar nicht erst heraus, egal wer fragt. Damit ist der im Altprojekt zweimal dokumentierte Look-ahead im Live-Pfad baulich unmöglich.

Signal auf Bar t, frühestmögliche Ausführung zur Eröffnung von t plus eins. Bei Stop-Fills gilt der ungünstigere Wert aus Stop-Preis und Eröffnung, damit Kurslücken nicht wegmodelliert werden.

### 3.2 Schreiben

Der Schreibpfad ist direkt von der Härtung vom 15.07.2026 übernommen und wird von Beginn an gebaut:

- Klassifikation jeder eingehenden Zeile in kritisch und Warnung. Kritisch sind fehlendes oder ungültiges Datum, fehlende Werte in Kursspalten, Schluss ausserhalb der Hoch-Tief-Spanne, nicht positive Werte, nicht monotone Zeitachse, Duplikate.
- Ein Batch mit auch nur einem kritischen Defekt wird **vollständig** abgelehnt und in Quarantäne gelegt. Die bestehende Datei bleibt unverändert.
- Extremsprünge über einer Schwelle werden markiert, nicht gelöscht.
- Schreiben nur mit Datei-Lock, in eine temporäre Datei im selben Verzeichnis, mit flush und fsync, Validierung der temporären Datei, danach atomares Ersetzen.
- Jede verworfene Zeile wird mit Grund protokolliert.

### 3.3 Universum

Point-in-Time. Ein Coin ist ab seinem tatsächlichen Listing wählbar, nicht früher. Delistete und gescheiterte Coins bleiben in der Historie. Quartalsweise mechanische Neuauswahl nach Mindestliquidität, Handelskontinuität und Datenabdeckung, ohne Ermessen.

**Start mit BTC, ETH, SOL als Kern.** Erweiterung nur, wenn die Forschung zeigt, dass ein Coin Eigenständiges beiträgt. Die belegten Korrelationen zwischen den Majors von 0.85 bis 0.93 machen breite Universen ohnehin weitgehend wirkungslos.

### 3.4 Perpetual-spezifische Serien

Zusätzlich zu Kursen werden erhoben: Funding-Rate je Zahlungsperiode mit tatsächlichem Zeitstempel, Open Interest, Mark-Preis und Index-Preis getrennt, Basis zwischen Spot und Perp, Finanzierungsniveau und Liquidationsschwelle je Position. **Funding ist kein Nebenposten, sondern ein laufender Bestandteil des Ergebnisses** und wird in jeder Kennzahl mitgerechnet.

---

## 4. Kostenmodell

Eine Datei, drei Szenarien, keine Ausnahmen.

| Grösse | Optimistisch | Realistisch | Konservativ |
|---|---|---|---|
| Spot Taker je Seite | 0.26 % | 0.40 % | 0.55 % |
| Spot Maker je Seite | 0.16 % | 0.25 % | 0.35 % |
| Perp Taker je Seite | 0.05 % | 0.075 % | 0.10 % |
| Spread Aufschlag | gemessen | gemessen mal 1.5 | gemessen mal 3 |
| Slippage | grössenabhängig | grössenabhängig | grössenabhängig mal 2 |
| Funding | tatsächlich | tatsächlich | tatsächlich mal 1.5 |

Die Spread-Werte stammen aus eigener Messung, nicht aus einer Annahme. Im Altprojekt lagen die gemessenen Spread-Mediane der Majors bei null bis drei Basispunkten, bei BTC bei 0.016 Basispunkten. Für Alt-Coins gelten diese Werte ausdrücklich nicht.

**Die Entscheidungsregel lautet: Ein Edge, der nur im optimistischen Szenario existiert, existiert nicht.** Jeder Bericht weist alle drei Szenarien aus, nie nur eines.

Ein Kostenfilter ist Pflicht-Gate vor jedem Einstieg: erwarteter Vorteil in Basispunkten muss Gebühr, Spread, Slippage, Funding über die erwartete Haltedauer und einen Sicherheitsaufschlag übersteigen. Ohne diesen Nachweis kein Trade.

---

## 5. Forschungsplan

Die Stufenlogik aus AURUM_CRYPTO_REGIME_RESEARCH_V1 wird übernommen und um zwei Stufen erweitert. Jede Stufe hat eine Vorregistrierung, ein Abbruchkriterium und ein Ergebnisdokument. **Kein Ergebnis wird nachträglich umdefiniert.**

### Stufe 0 — Datenbasis und Kosten
Point-in-Time-Universum aufbauen, Historie beschaffen, Integritätsprüfung über den gesamten Bestand, Spread- und Funding-Messung starten. Abschluss, wenn die Integritätsprüfung über alle Serien ohne kritischen Defekt durchläuft und mindestens sechs Wochen eigene Spread-Messung vorliegen.

### Stufe 1 — Existieren Regime?
Ausschliesslich Zustandsprüfung ohne jeden Bezug zu Gewinn und Verlust. Vorregistrierte Kandidaten mit den harten Ausschlusskriterien aus der Stufe-1-Spezifikation: Median-Verweildauer mindestens zehn Bars, Ein-Bar-Episoden höchstens 25 Prozent, Wechsel je 252 Bars unter der jeweiligen Obergrenze, Jitter-Übereinstimmung im Mittel mindestens 85 Prozent und nie unter 75 Prozent, Stabilität über Zeitblöcke.

**Anpassung gegenüber V1**: Der Zustandsraum wird symmetrisch. Ein Abwärtstrend ist ein eigener handelbarer Zustand und nicht nur die Abwesenheit eines Aufwärtstrends. Die Stress-Definition wird richtungsneutral formuliert.

**Zusätzliche Dimension**: Funding-Regime aus Funding-Rate und Basis, weil es der einzige Zustand ist, der im Spot-System gar nicht existiert.

Ergebnis ist eine eingefrorene Regime-Datei mit Versionsnummer. Jede spätere Änderung erzeugt eine neue Version und macht alle darauf aufbauenden Ergebnisse ungültig.

### Stufe 2 — Hat eine Strategie ohne Filter einen Edge?
Vier Familien, alle long und short: Trendfolge mit Ausbruch, Trend-Pullback, Mean Reversion, Volatilitätsausbruch. Dazu Nicht-Handeln als Vergleich. Benchmarks sind Buy-and-Hold, Cash und ein passives Engagement mit derselben Durchschnittsexposure.

Berichtet wird die **Verteilung** über die Parameterfamilie, nicht der beste Wert. Parameter-Sensitivität ist gleichrangig zur Rendite.

Der Beta-Trennungstest ist Pflicht: Eine Strategie muss eine passive Position mit gleicher Durchschnittsexposure risikoadjustiert schlagen. Genau dieser Test hat im Altprojekt den Turtle-Ansatz als einzigen bestehen lassen.

### Stufe 3 — Bringt der eingefrorene Filter einen Zusatzwert?
Vier Varianten im Vergleich: ohne Filter, mit eingefrorenem Filter, Filter allein, Benchmarks. Zu unterscheiden sind Signalverzögerung, Verminderung der Trade-Zahl, Umschaltverluste und Robustheitsverlust.

### Stufe 4 — Funding und Basis als eigene Ertragsquelle
Neu gegenüber V1. Geprüft wird, ob Funding-Niveau und Basis als Risikofilter, als Bestätigung oder als eigenständige Ertragsquelle taugen. Diese Stufe ist der eigentliche Grund, warum Perpetuals überhaupt in Frage kommen — sie eröffnet eine Ertragsquelle, die im Spot-System schlicht nicht existiert.

### Stufe 5 — Makro- und Flow-Overlays
Wie Stufe 4 in V1: ETF-Nettoflüsse, Stablecoin-Angebot, Dollarindex, Renditen, Aktienindex. Nur objektiv zeitstempelbare Serien in ihrer Erstfassung. Kein Freitext, keine Nachrichten, keine Sprachmodell-Stimmung.

### Validierungsregeln für alle Stufen
Walk-Forward mit strikter Trennung, Test-Split genau einmal und zuletzt. Purging und Embargo an den Fenstergrenzen, mindestens in der Länge der maximalen Haltedauer — dieser Punkt fehlte in V1 und wird ergänzt. Protokollierung jeder getesteten Konfiguration in einer Lauf-Registratur aus Strategie-Version, Daten-Version, Konfigurations-Hash und Zufallsstartwert. Deflated Sharpe und Probability of Backtest Overfitting als Pflicht-Kennzahlen. Bootstrap-Konfidenzintervall, dessen Fünf-Prozent-Perzentil über dem Cash-Ertrag liegen muss. Robustheit gegen Ausreisser wird immer ausgewiesen, weil die Schiefe in Krypto strukturell ist.

---

## 6. Strategien

### 6.1 Sleeve A — Langsame Trendfolge, Spot und Perp

Der belegte Kern. Entry bei Schluss über dem Hoch der letzten 55 Bars ohne den laufenden Bar, Exit unter dem Tief der letzten 20 Bars, N als Wilder-ATR(20), Notstopp bei Entry minus 2N mit Vorrang vor dem Zeitreihen-Exit.

**Erweiterung für Aurum II**: dieselbe Logik gespiegelt für die Short-Seite über Perpetuals. Die Spiegelung ist **nicht** selbstverständlich — Krypto-Abwärtstrends verlaufen schneller und enden abrupter als Aufwärtstrends, und Funding ist auf der Short-Seite meist positiv für den Halter. Das ist genau die Frage, die Stufe 2 beantworten muss, bevor irgendetwas gebaut wird.

Pyramiding bleibt zunächst aus. Es wird erst nach Stufe 2 und nur mit eigenem Nachweis erwogen.

### 6.2 Sleeve B — Schnellere Rotation, Spot

Und-Verknüpfung aus Kurs über MA50 und positivem 21-Tage-Momentum, wöchentliche Auswahl, Top-3 gleichgewichtet. Kein Profit-Guard, keine fixe Gewinnmitnahme. Chandelier-Trailing mit 3× ATR als einziger Gewinn-Exit.

### 6.3 Sleeve C — Funding, nur bei positivem Nachweis aus Stufe 4

Wird erst spezifiziert, wenn Stufe 4 abgeschlossen ist. Vorher existiert er nicht.

### 6.4 Zusammenführung

Die Sleeves liefern Zielexposure, keine Orders. Das Portfoliomodul führt sie zusammen, verrechnet Spot- und Perp-Beine gegeneinander (Netting) und übergibt genau ein Zielportfolio an die Risikoschicht. Bei Konflikt zwischen Sleeves gilt eine vorab festgelegte Rangfolge, nie eine Laufzeitentscheidung.

---

## 7. Risikoschicht

Die Risikoschicht hat Vetorecht vor jeder Order und kann von keiner Strategie umgangen werden.

### 7.1 Ebenen

| Ebene | Auslöser | Wirkung |
|---|---|---|
| Positionsrisiko | Verlust bis zum Stopp | Begrenzt die Positionsgrösse, nicht umgekehrt |
| Tagesverlustgrenze | Tagesverlust erreicht | Keine neuen Positionen bis zum Folgetag |
| Freeze | Grösserer Tagesverlust | Alle Positionen werden geschlossen, Handel ruht |
| Hard-Kill | Schwelle über mehrere Tage | System bleibt aus bis zur manuellen Freigabe |
| Liquidationsabstand | Perp, Abstand unter Schwelle | Zwangsweise Reduktion vor der Börse |

Alle Zähler laufen gegen den **Kalender**, nicht gegen den Prozessstart. Im Altprojekt waren Tages- und Wochenlimits an die Prozesslaufzeit gebunden, das Tageslimit wurde nie zurückgesetzt, und der Drawdown-Anker stand auf einem Testwert.

### 7.2 Positionsgrösse

Grösse ergibt sich aus Verlustbudget geteilt durch Stopp-Abstand in Prozent, nicht aus einer Prozentzahl des Kontos. Zusätzlich gilt ein absoluter Deckel je Position und je Asset über alle Sleeves hinweg.

### 7.3 Perp-spezifisch

Isolierte Margin je Position, kein Cross-Margin. Ein Hebel-Deckel, der so gesetzt ist, dass ein Kursereignis in der Grösse des historisch schlechtsten Tages die Position nicht liquidiert. Zwangsreduktion durch das System, bevor die Börse liquidiert. Funding-Kosten über die erwartete Haltedauer sind Teil des Kostenfilters vor dem Einstieg.

**Vorsicht bei einer bekannten Illusion**: Ein Markt-Verkauf am Schluss garantiert keinen Fill. Bei Kurslücke, Illiquidität, Handelsaussetzung oder Ausfall der Schnittstelle greift kein Schutz. Bei Hebel wird daraus Liquidationsrisiko. Der Schutz muss also in der Positionsgrösse liegen, nicht im Notausstieg.

### 7.4 Korrelationslimit

Neu und im Altprojekt nie gebaut: Die Summe der gleichgerichteten Exposure über hoch korrelierte Assets wird begrenzt. Bei Korrelationen von 0.85 bis 0.93 zwischen den Majors sind drei Positionen wirtschaftlich fast eine.

### 7.5 Kill-Switch

Zustand in der Datenbank, wird von **jedem** Pfad vor jeder Order gelesen. Ein Test stellt sicher, dass ein neuer Order-Pfad ohne Kill-Switch-Prüfung nicht in die Auslieferung gelangt. Im Altprojekt hatten vier von sechs Pfaden keine einzige Prüfung.

---

## 8. Ausführung

Deterministische Auftragskennung aus der Entscheidungs-Kennung. Zustand wird **vor** dem Aufruf der Börse geschrieben, nicht danach. Bei ausbleibender Antwort wird zuerst abgeglichen und dann erneut versucht, nie blind wiederholt. Beim Start wird immer abgeglichen.

Marktfähiges Limit als Regel, mit definierter Preistoleranz und einmaligem Nachpreisen nach kurzer Wartezeit. Marktorder nur im Notfall und mit Preisband. Vor dem ersten echten Auftrag erfolgt eine Rechteprüfung über die Validierungsfunktion der Börse, die nichts platziert.

Jede Position trägt eine Eigentumsmarke. Fremde Bestände werden nie verkauft. Ungewollte Reduktionen werden erkannt und gemeldet statt stillschweigend nachgeführt.

Ein prozessübergreifendes Lock mit Heartbeat. Ein zweiter Prozess bekommt eine klare Antwort und handelt nicht.

---

## 9. Betrieb

### 9.1 Die wichtigste Entscheidung

**Aurum II läuft nicht als Fenster-App auf dem Mac.** Genau diese Bauweise hat das Altprojekt sechs Wochen lang still stehen lassen, ohne dass jemand alarmiert wurde. Die Systemberechtigungen von macOS haben die Hintergrunddienste blockiert (Status 126, "Operation not permitted"), und die Datensammlung lief nur, solange ein Fenster offen war.

Zwei Optionen stehen zur Wahl. Erstens ein dauerhaft laufender kleiner Rechner, etwa ein Raspberry Pi, wie er im Altprojekt bereits vorbereitet war. Zweitens ein kleiner Server in der Cloud. Beides ist dem Mac vorzuziehen. Diese Entscheidung ist vor Beginn der Umsetzung zu treffen.

### 9.2 Wächter und Alarm

- **Heartbeat** jede Minute in die Datenbank. Ausbleiben über eine Schwelle löst Alarm aus.
- **Frische in Kalendertagen**, nicht in Datensatz-Zeilen. Genau dieser Fehler hat im Altprojekt eine Null gemeldet, während die Daten 38 Tage alt waren.
- **Eskalation**: Eine Warnung, die zweimal wiederkehrt, wird zum Alarm. Ein Alarm geht als Nachricht auf das Telefon, nicht in eine Protokolldatei. Der Vorwarnhinweis "Daten veraltet, vier Tage" vom 25.07.2026 blieb ungelesen und kostete sechs Wochen.
- **Täglicher Bericht** mit Datenfrische, Heartbeat, offenen Positionen, Funding-Saldo, Abgleich zwischen Soll und Ist, Kill-Switch-Zustand.

### 9.3 Oberfläche

Lesend. Jeder schreibende Endpunkt erfordert ein Token, und die Freigabe für andere Ursprünge ist geschlossen. Im Altprojekt konnte jede beliebige Webseite im Browser den Autopiloten starten und den Not-Aus zurücksetzen.

### 9.4 Freigabedisziplin

Neue Regel zuerst im Schatten, dann getrennte Freigabe, ein Parameter je Variante, definierter Rückweg. Ein künstlicher Ende-zu-Ende-Test über Einstieg, Halten, Stopp und Ausstieg im Trockenlauf statt Warten auf ein Marktsignal. Versionsverwaltung mit Git von Tag eins — das Altprojekt behalf sich mit Prüfsummen, weil es kein Repository hatte.

---

## 10. Phasenplan

| Phase | Inhalt | Abschlusskriterium |
|---|---|---|
| **P0** Fundament | Projektgerüst, Kostenmodell, Parameterdatei, Datenvertrag, Integritätsprüfung, Tests | Integritätsprüfung läuft über den gesamten Datenbestand ohne kritischen Defekt durch |
| **P1** Datenbasis | Historie beschaffen, Point-in-Time-Universum, Spread- und Funding-Messung starten | Sechs Wochen eigene Spread- und Funding-Messung liegen vor |
| **P2** Stufe 1 | Regime-Forschung, symmetrisch, inklusive Funding-Dimension | Eingefrorene Regime-Datei oder begründetes "kein Regime robust" |
| **P3** Stufe 2 | Strategie-Edge ohne Filter, long und short, alle Kostenszenarien | Mindestens eine Familie besteht den Beta-Trennungstest im konservativen Kostenszenario |
| **P4** Stufen 3 bis 5 | Filterwert, Funding, Overlays | Ergebnisberichte, auch negative |
| **P5** Engine | Portfolio, Risiko, Ausführung, Schattenbetrieb ohne Orders | 30 Tage Schattenbetrieb ohne Fehler, Abgleich täglich deckungsgleich |
| **P6** Paper | Paper-Handel auf echten Kursen, echte Ausführungsmodellierung | 90 Tage und 100 Trades, danach Urteil |
| **P7** Micro-Live | Kleinstes vertretbares Kapital, ring-fenced | Rein technische Kriterien. Gewinn ist ausdrücklich kein Freigabekriterium |

**Zwischen P3 und P4 steht ein echter Abbruchpunkt.** Wenn keine Strategiefamilie im konservativen Kostenszenario einen Vorteil gegenüber passiver Exposure zeigt, dann ist das ein gültiges Ergebnis, und Aurum II wird nicht als Handelssystem weitergeführt. Genau dieser Punkt fehlte im Altprojekt.

---

## 11. Offene Entscheide

Diese Punkte sind vor Beginn von P0 zu klären.

1. **Betriebsort**: Raspberry Pi, Cloud-Server oder doch der Mac mit allen bekannten Nachteilen.
2. **Kapitalrahmen**: Welches Kapital soll Aurum II in P7 höchstens bewegen, und welcher Betrag ist ein akzeptabler Totalverlust.
3. **Börse für Perpetuals**: Kraken Futures aus Kontinuität, oder eine Börse mit besserer Perp-Liquidität. Das entscheidet über Funding-Niveau und Gegenparteirisiko.
4. **Rechtliches und Steuern in der Schweiz**: Gehebelter Krypto-Handel kann die Einordnung als privater Vermögensverwalter beeinflussen. Das ist vor Live zu klären, nicht danach. Ich bin kein Steuerberater, diese Einschätzung ersetzt keine Fachauskunft.
5. **Zeitbudget**: Der Stufenplan bis P6 ist Monatsarbeit, nicht Wochenarbeit. Ohne realistisches Budget endet er wie die Regime-Research V1, nämlich vollständig spezifiziert und nie gerechnet.
6. **Umgang mit dem Altsystem**: Der Kill-Switch von Aurum steht seit dem 17.07.2026 auf aktiv, offene Positionen und ein Fremdbestand SOL sind vorhanden. Es ist zu entscheiden, ob das Altsystem sauber abgewickelt, eingefroren oder weiterbetrieben wird. Aurum II sollte nicht neben einem halb laufenden Vorgänger starten.

---

## 12. Was dieses Dokument nicht ist

Es enthält keine Renditeerwartung für Aurum II. Jede Zahl im Findings-Digest stammt aus Backtests oder Replays auf Long-only-Spot-Daten mit Survivorship-Vorbehalt. **Für die Short-Seite, für Hebel und für Funding existiert im gesamten Altbestand kein einziger validierter Wert.** Die Erwartung wird erst nach Stufe 2 formuliert, und zwar aus gerechneten Ergebnissen, nicht aus Absichten.
