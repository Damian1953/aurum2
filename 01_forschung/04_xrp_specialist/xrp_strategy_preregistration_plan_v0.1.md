# XRP Specialist — Vorregistrierungsplan, Version 0.1

**Project Aurum II, Forschungsstrang 04_xrp_specialist. 17.09.2026. Status: Plan zur Prüfung. Kein Rechenlauf, keine Optimierung. Alle Freeze-Urteile der Stufen 1, 2 und der MTP-Validierung bleiben unberührt und werden hier weder herangezogen noch umgedeutet.**

## 0. Zweck und Abgrenzung

Forschungsfrage: Kann eine XRP-spezifische Architektur aus Mean Reversion und Volatility Expansion einen robusteren Edge erzeugen als eine universelle Trendstrategie? Ziel ist nicht, eine Strategie so lange anzupassen, bis sie besteht, sondern zu prüfen, ob die Marktstruktur von XRP eine eigene Konstruktion verlangt. Deshalb werden drei Kandidaten mit je einem Parametersatz vorregistriert, gemeinsam eingefroren, einmal gerechnet und gemeinsam korrigiert.

Vorbelastung, die offen ausgewiesen wird: In Stufe 2 wurde eine tägliche Mean Reversion (z(20) ±2, Exit SMA20, Stop 3 ATR, 10 Bars) auf zehn Coins verworfen, auf XRP Long mit 5 Prozent CAGR bei Sharpe 0.3, Short negativ. In der MTP-Validierung war XRP der einzige der drei geeigneten Coins mit positiver Erwartung in Ebene B (0.91 R_gesamt, 10 Trades). Beide Ergebnisse sind Vorwissen, kein Freibrief und kein Verbot. Die Kandidaten hier unterscheiden sich von der Stufe-2-MR in Zeitebene (4h), Exit-Logik, Kompressionsbedingung und Kombination, aber der Vorwurf «Mean Reversion so lange variieren, bis sie besteht» wiegt nach Stufe 2 schwerer, nicht leichter. Deshalb gilt: Wenn XRP-A in dieser Form scheitert, gibt es keine XRP-A-Variante 2.

## 1. Marktstruktur-Hypothese

XRP zeigt, so die Ausgangsvermutung aus Recherche und Beobachtung, zwei wiederkehrende Mechaniken: lange Range- und Konsolidierungsphasen mit scharfen kurzfristigen Umkehrungen, und seltene, sehr starke Expansionsphasen (2017, Ende 2020, 2021, Ende 2024). Dazu ein tiefer Perpetual-Markt mit zeitweise stark divergierendem Funding und hohem Open Interest.

Diese Hypothese wird vor dem Strategietest deskriptiv geprüft, ohne Strategie und ohne Auswahlwirkung (Abschnitt 4.1): Anteil der Zeit in Kompression (Bollinger-Bandbreite unter ihrem rollenden 20-Prozent-Perzentil), Verteilung der 4h-Renditen nach Kompressionszustand, Autokorrelation der 4h-Renditen bei ersten und fünften Lags, Häufigkeit und Grösse von Expansionsereignissen (20-Tage-Spanne über dem Dreifachen ihres Medians), im Vergleich zu BTC und ETH auf denselben Definitionen. Fällt die Beschreibung anders aus als vermutet (etwa keine höhere Umkehrneigung in Ranges als bei BTC), wird das protokolliert und die Strategietests laufen trotzdem, weil sie vorregistriert sind, aber die Interpretation eines Erfolgs wäre eine andere.

## 2. Strategiefamilien

Drei Kandidaten, je ein primärer Parametersatz, Long und Short getrennt, ohne Symmetrieannahme.

**XRP-A, Mean Reversion, 4h primär, 8h Robustheit.** Gleichgewicht ist der EMA(20) der 4h-Schlusskurse, Abweichung ist z = (Close − EMA20) / SD(20) der 4h-Schlusskurse. Long-Einstieg am Schluss einer 4h-Kerze mit z ≤ −2.0, Short-Einstieg bei z ≥ +2.0. Exit, wenn z das Vorzeichen wechselt (Rückkehr zum Gleichgewicht), spätestens nach 30 Kerzen (fünf Tage), Stop bei 3 mal ATR(14 Kerzen) vom Einstieg, nicht nachgezogen. Ein Einstieg je Signal, keine Add-ons, kein Regime-Label. Kein Filter über gleitende Durchschnitte. Die 8h-Variante verwendet dieselben Zahlen auf 8h-Kerzen (EMA20, SD20, ATR14, 15 Kerzen maximale Haltedauer) und ist Robustheitsvergleich, kein eigener Test.

**XRP-B, Volatility Breakout, Tagesbasis primär, 4h Robustheit.** Kompression: Bollinger-Bandbreite BBW = (oberes − unteres Band) / Mittelband mit SMA(20) und 2 Standardabweichungen liegt unter dem 20-Prozent-Perzentil ihrer eigenen letzten 180 Tage (rollend, nur Vergangenheit). Expansion: Schluss über dem höchsten Hoch der letzten 20 Tage (Long) oder unter dem tiefsten Tief (Short), an einem Tag, an dem die Kompressionsbedingung an mindestens einem der letzten fünf Tage erfüllt war. Einstieg zur Eröffnung des Folgetages. Stop volatilitätsangepasst: höchster Schluss seit Einstieg minus 3 mal ATR(20 Tage) (Chandelier), täglich nachgezogen, nie gesenkt. Kein Ziel, Gewinner laufen bis zum Stop. Die 4h-Variante rechnet dieselben Fenster in 4h-Kerzen (BBW 20 Kerzen, Perzentil über 1080 Kerzen, Donchian 20 Kerzen, ATR 20 Kerzen).

**XRP-C, Hybrid.** Beide Motoren laufen gleichzeitig auf 4h (A) und Tagesbasis (B). Die Kapitalgewichtung ist kontinuierlich: p = Kaufman Efficiency Ratio über 20 Tage der Tagesschlüsse (Betrag der 20-Tage-Nettobewegung geteilt durch die Summe der 20 täglichen Betragsbewegungen, Wert zwischen 0 und 1). Gewicht für B: w_B = clip((p − 0.20) / 0.40, 0, 1), Gewicht für A: w_A = 1 − w_B. Bei p ≤ 0.20 (Bewegung ohne Richtung) nur A, bei p ≥ 0.60 (stark gerichtet) nur B, dazwischen linear. Die Gewichte werden am Tagesschluss berechnet und gelten für den Folgetag. Kein Schalter, keine Zustandsbezeichnung. Die Schwellen 0.20 und 0.60 sind vorab gesetzt (0.20 ist der typische ER einer Zufallsbewegung über 20 Tage, 0.60 ein klar gerichteter Abschnitt) und werden nicht optimiert. Jitter: 0.15/0.55 und 0.25/0.65.

**Referenzlinien, keine Tests.** Zum Vergleich «robuster als universelle Trendstrategie» werden auf denselben Daten, Kosten und Blöcken berichtet: MTP-Spezifikation v1 auf XRP (eingefroren, aus der Validierung bekannt) und W2 aus Stufe 2 auf XRP. Beides sind Berichtszeilen ohne Kriterienwirkung.

## 3. Exakte minimale Inputs

| Grösse | Definition | Ebene | Bekannt am |
|---|---|---|---|
| EMA20, SD20 (A) | auf 4h-Schlusskursen, einschliesslich aktueller Kerze | 4h | Kerzenschluss |
| ATR14 (A), ATR20 (B) | Wilder-Glättung der True Range | 4h bzw. Tag | Kerzenschluss |
| BBW und Perzentil (B) | SMA20 ± 2 SD, Bandbreite relativ, Perzentil über 180 Tage rollend | Tag | Tagesschluss |
| Donchian 20 (B) | höchstes Hoch / tiefstes Tief der letzten 20 Tage ohne den aktuellen Tag | Tag | Tagesschluss |
| ER20 (C) | Kaufman Efficiency Ratio, 20 Tage | Tag | Tagesschluss |
| Funding f_8h, f_7d, Funding-z | 8h-Rate Binance USDT-M, 7-Tage-Summe annualisiert, z über 90 Tage | 8h | Settlement-Zeitpunkt, für die Kerze gilt die letzte abgerechnete Rate |
| OI, ΔOI_5d | Tageswert 00:00 UTC, Veränderung über fünf Tage | Tag | Tagesschluss (Schnappschuss 00:00 des Folgetages zählt für den Folgetag) |
| Basis | (Perp-Schluss − Spot-Schluss) / Spot-Schluss, Binance, täglich und 4h | Tag, 4h | Kerzenschluss |
| Volumen, Taker-Kaufanteil | Binance-Kline-Spalten Volumen und Taker-Buy-Volumen | Tag, 4h | Kerzenschluss |

Nicht verwendet: Liquidationsdaten (keine belastbare öffentliche Historie vor 2021, fail-closed), Orderbuch-Imbalance (keine Historie).

## 4. Datenbedarf und Datenstand

**Vorhanden (Stufe 2, MTP-Validierung):** Binance Spot Tageskerzen XRPUSDT ab 2018-05-04, Binance Perp Tageskerzen ab 2020-01-06, Funding 8h ab 2020-01-06 bis 2026-08-31, Open Interest täglich ab 2021-12-01, Kraken Spot Tageskerzen ab 2017-05-18 (Archiv, mit API-Ergänzung), CMC ab 2013-08-04. Alle mit Prüfsummen.

**Fehlend, nachzuladen vor dem Freeze:** Binance Spot und Perp 4h-Kerzen XRPUSDT (Binance Vision, monatliche Dateien, alle zwölf Kline-Spalten, damit Taker-Buy-Volumen und Anzahl Trades verfügbar sind). Binance Spot und Perp Tageskerzen erneut mit allen Spalten (für Volumen-Filter und Taker-Anteil). Kraken 240-Minuten-Kerzen XRPUSD aus dem bereits geladenen Archiv 2026Q2 (Datei `XRPUSD_240.csv`, liegt im Zip unter `_download/`) plus API-Ergänzung ab Juli 2026. Funding September 2026, sobald Binance die Monatsdatei publiziert.

**Fail-closed-Regeln:** OI-Filter werden nur auf dem Fenster ab 2021-12-01 getestet, Funding-Filter nur ab 2020-01-06, ohne Rückrechnung. Fehlt an einem Tag ein Wert, ist der Filter an diesem Tag «nicht auswertbar» und der Trade zählt zur ungefilterten Basis, nicht zur gefilterten Gruppe. Die Filter-Tests werden auf demselben Fenster mit und ohne Filter verglichen, nicht gegen die volle Historie.

**Abdeckung und Blöcke:** Tagesbasis ab 2018-05 (Binance) beziehungsweise 2017-05 (Kraken). Zeitblöcke wie Stufe 2: P1 bis 2020, P2 2021 bis 2023, P3 ab 2024. Für XRP-A auf 4h beginnt der Test mit den 4h-Daten (Binance ab 2018-05).

### 4.1 Deskriptive Vorprüfung ohne Auswahlwirkung

Vor dem Strategielauf, mit denselben eingefrorenen Definitionen: Kompressionsanteil, Autokorrelation, Expansionsereignisse, Funding-Verteilung, OI-Verlauf, jeweils XRP gegen BTC und ETH. Ergebnis ist ein Bericht, der die Marktstruktur-Hypothese stützt oder nicht. Er ändert keinen Parameter der Kandidaten. Parameter, die nach dieser Vorprüfung geändert würden, wären Optimierung.

## 5. Look-ahead-Risiken

| Risiko | Vorkehrung |
|---|---|
| 4h-Kerze und Funding-Zeitpunkt: Funding wird um 00:00, 08:00, 16:00 UTC abgerechnet, exakt an 4h-Grenzen | Für Signale am Schluss einer Kerze zählt die zuletzt abgerechnete Rate, nie die vorhergesagte nächste |
| OI-Tageswert ist ein Schnappschuss um 00:00 UTC | Der Wert vom 00:00 des Tages t+1 ist erst ab Kerze 1 des Tages t+1 bekannt und wird so zugeordnet |
| Rollende Perzentile und z-Scores | Fenster enden mit der aktuellen Kerze einschliesslich, nie darüber hinaus, Test wie Stufe 2 mit abgeschnittener Historie |
| Donchian-Niveau | ohne den aktuellen Tag berechnet, damit der Ausbruch über ein vorher bekanntes Niveau geht |
| Chandelier-Stop | höchster Schluss bis einschliesslich Vortag, ATR bis einschliesslich Vortag, Stop gilt für den laufenden Tag |
| Hybrid-Gewichte | am Tagesschluss berechnet, gelten für den Folgetag |
| Einstieg | Signal am Kerzenschluss, Fill zur Eröffnung der Folgekerze plus Slippage, wie in der MTP-Validierung |
| 4h-Kerzen Binance gegen Kraken: unterschiedliche Kerzengrenzen sind ausgeschlossen (beide UTC 00/04/08 …), aber Kraken-4h haben dünne Frühphase | B-Start-Regel wie MTP-Validierung: später Datum aus Warmup-Ende und erstem Tag nach der letzten fehlenden Kerze |
| Survivorship: XRP ist ein Überlebender | Vermerk, XRP wird als Einzelmarkt getestet, keine Generalisierung |

Look-ahead-Test vor dem Volllauf: Signale auf abgeschnittener Historie (30.06.2023) identisch mit dem Volllauf, für jeden Kandidaten und jede Zeitebene.

## 6. Kostenmodell

Perpetual-Modell wie Stufe 2 (K0 0.02, K1 0.05 plus 0.02, K2 0.10 plus 0.06 je Seite, tatsächliches Funding je 8h-Periode, unter K2 Zahlungen mal 1.5), weil Short-Seiten nur auf Perps handelbar sind und XRP-A mit fünf Tagen Haltedauer die Kostenhürde aus der Strategiebewertung direkt trifft. Für Long-Seiten zusätzlich das Spot-Modell (Kraken Tier 1, 0.40 plus 0.02 je Seite) und, wie in der MTP-Validierung, eine Ebene B mit Ausführung auf Kraken-Spot-4h-Kerzen (Einstieg erster handelbarer Preis der Folgekerze, Stop-Market am Niveau mit 0.10 Prozent Slippage unter K1, 0.30 unter K2). Short-Seiten laufen auf Binance-Perp-Daten mit Kraken-Perp-Gebührensätzen und tragen den Vermerk «Kraken-Perp-Historie nicht verfügbar». Cash zum T-Bill-Satz. Turnover und Kostenanteil am Brutto-P&L werden je Kandidat ausgewiesen, für XRP-A auf 4h ist die Kostenquote ein eigener Berichtswert, weil sie den Ausgang wahrscheinlich entscheidet.

## 7. Long- und Short-Logik

Jeder Kandidat wird Long-only, Short-only und Long+Short (zwei Sleeves zu je 0.5) getrennt ausgewertet. Keine Annahme der Symmetrie: Die Short-Seite von XRP-A verwendet z ≥ +2.0 mit denselben Fenstern, aber ihr Ergebnis wird nicht als Spiegelbild interpretiert, und ein Scheitern der Short-Seite entwertet die Long-Seite nicht. Für XRP-B ist die Short-Seite ein Ausbruch unter das 20-Tage-Tief nach Kompression mit Chandelier-Stop über dem tiefsten Schluss. Für XRP-C werden die Seiten der beiden Motoren einzeln gewichtet, Long+Short ist die Summe. Funding wird für Long positiv belastet und für Short positiv gutgeschrieben, nach tatsächlicher Rate.

Vorregistrierte Derivate-Filter, je als bedingte Aufteilung der Trades desselben Kandidaten, nicht als neue Strategie:

- **F1 (Breakout-Überhitzung):** Long-Ausbrüche von XRP-B mit Funding-z (90 Tage) ≥ +2 und ΔOI_5d ≥ +10 Prozent am Signaltag gegen die übrigen Long-Ausbrüche. Hypothese: schlechtere Folgeerträge.
- **F2 (Kapitulation):** Long-Einstiege von XRP-A mit Funding-z ≤ −2 am Signaltag gegen die übrigen. Hypothese: bessere Erwartung je Trade.
- **F3 (Bestätigung):** Ausbrüche von XRP-B mit ΔOI_5d ≥ +10 Prozent gegen solche ohne, beide Seiten. Hypothese: höhere Trefferquote und Erwartung.

Die Schwellen 2 (z) und 10 Prozent (ΔOI) sind vorab gesetzt. Ein Filter «besteht», wenn die Differenz der Erwartung je Trade zwischen den Gruppen im Trade-Bootstrap auf dem 5-Prozent-Niveau von null verschieden ist, mit Holm über die Filter. Ein bestandener Filter ändert nichts am Urteil über den Kandidaten. Er wird als Hypothese für eine spätere Stufe festgehalten. Kein Filter wird nach dem Lauf hinzugefügt, um ein Ergebnis zu retten.

## 8. Robustheitskriterien

Bestanden gilt je Kandidat und Seite unter K1, primäre Zeitebene, Sicht 1 (feste Risikoregel: Notional so, dass der initiale Stop 2 Prozent des Sleeve-Startkapitals riskiert, ohne Compounding):

1. Erwartung je Trade netto grösser null und CAGR über Cash, Profit-Faktor mindestens 1.3.
2. Mindestens zwei von drei Zeitblöcken mit positiver Erwartung.
3. Jitter-Region: mindestens zwei Drittel der Nachbarn positiv, Sharpe der Basis höchstens 1.5 mal Nachbar-Median. Nachbarn: A z 1.5 und 2.5, EMA 15 und 30, Halten 20 und 40 Kerzen. B Perzentil 10 und 30, Donchian 15 und 30, Stop 2.5 und 3.5 ATR. C Schwellen 0.15/0.55 und 0.25/0.65, ER 15 und 30.
4. Trade-Mindestzahl nach Klasse: A Klasse S (mindestens 100 Trades), B Klasse M (mindestens 40), C Long+Short (mindestens 100 kombiniert).
5. MaxDD nicht schlechter als die exposure-gleiche Passivposition.
6. Beta-Trennung: Alpha-Teiltest oder Risikotransformations-Teiltest (Stufe 2, Abschnitt 13.3).
7. Bootstrap-5-Prozent-Perzentil der Überrendite grösser null und Holm-korrigierter p-Wert unter 0.05 innerhalb der Familie (Abschnitt 9).
8. Kostenstress: Vorzeichen der Erwartung bleibt unter K2 erhalten.
9. Edge-Retention (Long-Seiten): Erwartung je Trade auf Kraken-Ausführung mindestens 60 Prozent der Binance-Ausführung, abweichender Exit-Grund höchstens 15 Prozent.

Berichtet, nicht Kriterium: R-Multiples (Mittel, Median, Verteilung), Sortino, Recovery Time, Exposure, Haltedauer Gewinner und Verlierer, Konzentration (Top 1, 3, 5), Ergebnis ohne grössten Gewinner, Kostenquote, 8h- beziehungsweise 4h-Robustheitsvariante, Referenzlinien MTP v1 und W2 auf XRP.

Die Frage «robuster als universelle Trendstrategie» wird beantwortet, indem der bestandene Kandidat (falls einer besteht) mit den Referenzlinien auf denselben Blöcken und Kriterien verglichen wird. Besteht keiner, ist die Antwort nein, unabhängig von den Referenzlinien.

## 9. Nullhypothesen und Multiple Testing

H0-A: XRP-A erzeugt nach K1 auf 4h keine positive Erwartung je Trade, die über eine exposure-gleiche Passivposition hinausgeht, weder Long noch Short.
H0-B: XRP-B erzeugt nach K1 keine positive Erwartung, die über die Passivposition hinausgeht, weder Long noch Short.
H0-C: Die kontinuierliche Gewichtung von A und B nach ER erzeugt keine Erwartung, die über dem besseren der beiden Einzelkandidaten liegt (C wird zusätzlich gegen A und B einzeln geprüft, nicht nur gegen die Passivposition).
H0-F1 bis H0-F3: Die bedingte Aufteilung nach Funding oder OI erzeugt keine Differenz der Erwartung je Trade zwischen den Gruppen.

Primäre Familie für Holm: sieben Tests (A-L, A-S, B-L, B-S, C-L, C-S, C-LS). Sekundäre Familie: sechs Filter-Tests (F1 L, F2 L, F3 L, F3 S, dazu F1 S und F2 S als Spiegel). Robustheitsvarianten (8h, 4h für B), Jitter-Nachbarn, Kostenszenarien und Referenzlinien sind keine Tests. Deflated Sharpe Ratio mit N gleich 7 plus Jitter als Sensitivität. Kein Kandidat wird nach CAGR gewählt.

## 10. Offene Entscheidungen vor dem Freeze

1. 4h-Daten: Binance Vision Spot und Perp 4h mit allen Spalten nachladen (Loader-Erweiterung, Mac-Launcher) und Kraken 240-Minuten aus dem vorhandenen Archiv extrahieren. Empfehlung: ja, beides, vor dem Freeze, weil XRP-A ohne 4h nicht definiert ist.
2. Primäre Zeitebene für XRP-B: Tag (Empfehlung, weil Kompression über Wochen läuft und die Kostenhürde auf 4h für einen Trendmotor unnötig ist) oder 4h.
3. Short-Seiten auf Binance-Perp-Daten mit Kraken-Gebühren und Vermerk, oder Short-Seiten nur berichten ohne Kriterien (Empfehlung: mit Kriterien, mit Vermerk, weil sonst die Asymmetriefrage nicht beantwortbar ist).
4. Trade-Mindestzahlen (100 für A, 40 für B, 100 für C) bestätigen oder anpassen.
5. Profit-Faktor-Schwelle 1.3 für Kandidaten mit hoher Trade-Frequenz (gegen 1.5 in der MTP-Validierung) bestätigen.
6. Ob die deskriptive Vorprüfung (4.1) vor oder nach dem Freeze der Kandidaten läuft. Empfehlung: nach dem Freeze, vor dem Strategielauf, damit sie keine Auswahlwirkung haben kann.
7. Filter-Schwellen (Funding-z 2, ΔOI 10 Prozent, Fenster 90 Tage und 5 Tage) bestätigen. Jede Änderung vor dem Freeze ist erlaubt, danach keine.
8. Ob die Referenzlinie W2 aus Stufe 2 mitläuft oder nur MTP v1. Empfehlung: beide, weil sie zwei verschiedene Trendkonstruktionen sind.
9. Sizing-Regel für XRP-C: Gewicht mal Sleeve-Kapital je Motor (Empfehlung) oder feste Hälften.

Nach Klärung: Version 1.0, Prüfsumme in ENTSCHEIDE, Datenbeschaffung mit Prüfsummen und Abdeckung, Look-ahead-Test, deskriptive Vorprüfung, ein Volllauf.
