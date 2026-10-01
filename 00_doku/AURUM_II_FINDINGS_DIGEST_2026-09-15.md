# Project Aurum II — Findings-Digest

**Stand 15.09.2026. Grundlage sind die Dokumente im Ordner Cryptobot, ausgewertet am 15.09.2026.**

Dieses Dokument fasst zusammen, was aus Project Aurum belegt ist, was davon nach Aurum II übernommen wird und was bewusst zurückbleibt. Es ist die Basis aller weiteren Entscheide. Alle Zahlen stammen aus den genannten Quelldateien. Wo eine Zahl fehlt, steht das ausdrücklich da, statt sie zu schätzen.

---

## 1. Ausgangslage in einem Satz

Project Aurum hat in rund drei Monaten eine grosse Menge an Methodenwissen, belastbaren Negativbefunden und gehärteten Betriebsbausteinen erzeugt, aber keinen einzigen validierten Live-Edge. Die einzige harte Live-Zahl über alle Berichte lautet: alle realisierten Trades zusammen ergaben minus 5.37 USD bei rund 4.30 USD Gebühren, der gesamte Buchgewinn von plus 1.15 Prozent stammte aus offenen, nicht angefassten Positionen (PERFORMANCE_ANALYSE_2026-07-10.md).

Dazu kommt ein zweiter, ebenso wichtiger Befund: Das System steht seit dem 31.07.2026 still, der Kill-Switch ist seit dem 17.07.2026 aktiv, zwei monatliche und rund neun wöchentliche Rebalancings sind ausgefallen (Tagesbriefing_2026-09-15.md). Der Ausfall war kein Marktereignis, sondern ein Betriebsereignis.

**Die zentrale Lehre für Aurum II lautet deshalb: Betriebsrisiko und Kostenrealismus entscheiden vor Signalqualität.**

---

## 2. Was nachweislich funktioniert hat

### 2.1 Der langsame Trendfolge-Kern

Der Turtle-Ansatz in der Shadow-Variante ist der einzige Baustein mit belastbarer Out-of-Sample-Evidenz. Regelwerk: Entry bei Close über dem Hoch der letzten 55 Tage (laufender Bar per shift(1) ausgeschlossen), Exit unter dem Tief der letzten 20 Tage, N als Wilder-ATR(20), Notstopp bei Entry minus 2N mit Vorrang vor dem 20-Tage-Exit.

| Zeitraum | Turtle CAGR | Turtle MaxDD | Turtle Sharpe | BTC Buy-and-Hold CAGR | BTC MaxDD | BTC Sharpe |
|---|---|---|---|---|---|---|
| Voll ab 2018 | 29.8 % | −53.8 % | 0.87 | 30.8 % | −76.6 % | 0.75 |
| Train bis 2022 | 36.0 % | −51.2 % | 0.92 | 20.7 % | −76.6 % | 0.63 |
| Validierung 2023 | 21.9 % | −22.9 % | 0.77 | 154.5 % | −20.0 % | 2.34 |
| **OOS ab 2024** | **20.3 %** | **−28.8 %** | **0.77** | 14.7 % | −53.1 % | 0.53 |

Quelle TURTLE_SLEEVE_ENTSCHEID_2026-07-14.md. Entscheidend ist der Beta-Trennungstest: Eine passive BTC-Quote von 34 Prozent mit derselben Durchschnittsexposure lieferte nur Sharpe 0.53 und Calmar 0.35 gegenüber 0.77 und 0.70. Der Vorteil ist also nicht nur Marktbeta.

Zwei Einschränkungen bleiben. Erstens stammen rund 20 Trades aus acht Jahren, die Ergebnisse hängen an wenigen Ereignissen. Zweitens trug ETH den grössten Teil des OOS-Ergebnisses.

**Der Ansatz ist zudem kaum kostensensitiv.** Im pessimistischen Kostenmodell (0.55 Prozent plus 0.20 Prozent je Seite) sank die Vollperiode nur von 29.8 auf 28.1 Prozent. Das ist bei Krypto-Gebühren der wichtigste strukturelle Vorteil gegenüber allen schnellen Ansätzen.

### 2.2 Die Komplementarität zweier Zeithorizonte

Die Signalzustände auf BTC verteilen sich so (TURTLE_SLEEVE_ENTSCHEID): Momentum und Turtle gleichzeitig long an 2 Prozent der Tage mit plus 3.55 Prozent durchschnittlicher Sieben-Tage-Folgerendite, Momentum draussen und Turtle noch long an 31 Prozent der Tage mit plus 0.61 Prozent, beide draussen an 65 Prozent mit minus 0.24 Prozent. Zwei Zeithorizonte parallel zu führen ist damit besser belegt als einen zu optimieren.

### 2.3 Der schnelle Momentum-Kern in korrigierter Form

Die Einstiegslogik des Krypto-Satelliten war falsch gebaut. Die Oder-Verknüpfung (Kurs über MA50 **oder** 21-Tage-Momentum über 5 Prozent) fügte 54 zusätzliche Slot-Wochen hinzu, die Rendite, Sharpe und Drawdown verschlechterten. Die Und-Verknüpfung ist in beiden Zeiträumen überlegen (MOMENTUM_AUDIT_2026-07-14.md):

| Variante | Voll CAGR | MaxDD | Sharpe | In-Sample | Out-of-Sample |
|---|---|---|---|---|---|
| Baseline (Oder) | 52 % | −53 % | 1.06 | 79 % / 1.35 | 12 % / 0.48 |
| Nur MA50 | 59 % | −49 % | 1.16 | 91 % / 1.48 | 16 % / 0.55 |
| **MA50 UND mom > 0** | **59 %** | **−48 %** | **1.18** | 83 % / 1.42 | **27 % / 0.79** |

Ergänzend belegt: Top-3 gleichgewichtet ist der Sharpe-Optimalpunkt (Top-1 liefert 60 Prozent bei minus 78 Prozent Drawdown), Volatilitätsgewichtung ist schlechter als Gleichgewichtung, Ranking-Hysterese schadet deutlich.

### 2.4 Das graduelle Regime-Gate

Ein Gate, das die Exposure in Stufen skaliert statt binär zu schalten, ist die effizienteste Drawdown-Massnahme im gesamten Bestand: MaxDD von minus 53 auf minus 44 Prozent, Calmar von 0.98 auf 1.12, Kosten rund zwei CAGR-Punkte (MOMENTUM_AUDIT). In einem System mit Hebel wird diese Steuerung noch wichtiger.

Die separat verifizierte Variante Gleichgewichtung plus 200-Tage-Gate lieferte 63.8 Prozent CAGR, Sharpe 1.16 und minus 55.4 Prozent Drawdown gegenüber 59.3 Prozent, 1.06 und minus 62.0 Prozent ohne Gate, im Bärenjahr 2022 minus 23.6 statt minus 45.4 Prozent (UMSETZUNG_2026-07-02.md).

### 2.5 Gehärtete Betriebsbausteine

Diese Module haben sich in Audits bewährt und werden konzeptionell übernommen: die Risk Engine mit Vetorecht vor jeder Order, das Netzwerkmodul mit CA-Bundle, Timeout und Backoff, der Idempotenz- und Reconciliation-Pfad zu Kraken (inklusive der teuer erkauften Erkenntnis, dass Kraken userref und cl_ord_id nicht gemeinsam akzeptiert), das Validierungsmodul mit sechs Blickwinkeln und konservativer Score-Logik, das Exposure-Modul mit Korrelationsmatrix und Beta, sowie die Live-Readiness-Gates mit dem Scope-Test über AddOrder validate=true.

Die Collector-Härtung vom 15.07.2026 ist direkt übertragbar: Validierung vor dem Merge, fail-closed, Quarantäne des ganzen Batches bei kritischem Defekt, Datei-Lock, temporäre Datei plus atomares Ersetzen, Lineage für jede verworfene Zeile, 13 von 13 Tests (PHASE1G_COLLECTOR_HAERTUNG_2026-07-15.md).

---

## 3. Was nachweislich nicht funktioniert hat

### 3.1 Alles Schnelle

Der Intraday-Bounce-Ansatz ist doppelt widerlegt. Formal im Backtest mit Score 30 von 100 und null Trades über alle sechs Coins und alle drei Kostenstufen. Ökonomisch im Live-Betrieb mit 16 Trades, brutto plus 1.49 USD gegen 3.28 USD Gebühren, also einer Fee-to-Gross-Quote von 220 Prozent bei einer durchschnittlichen Positionsgrösse von 28 USD (INTRADAY_NEUKONZEPT_KESTREL_2026-07-02.md, PERFORMANCE_ANALYSE_2026-07-10.md). 14 von 16 Exits waren Zeit-Stopps, und nach fast jedem Zeit-Exit lief das Asset innert 24 Stunden zwei bis sieben Prozent weiter.

Die Alt-Coins NEAR, ARB, SEI und APT hatten Markttiefen von 30'000 bis 80'000 USD. Die Bewegung pro Handelsfenster war kleiner als die Kosten. Eine NEAR-Serie mit sechs Engagements in unter vier Stunden kostete 2.13 USD.

### 3.2 Fixe Gewinnmitnahmen

Der Profit-Guard mit Teilverkauf eines Drittels bei plus 25 Prozent kostete vier CAGR-Punkte ohne Drawdown-Nutzen. 35 von 56 Auslösungen (62 Prozent) schnitten grosse Gewinner ab, nur 20 (36 Prozent) vermieden Verluste (MOMENTUM_REPLAY_VALIDIERUNG_2026-07-14.md). In einem System mit positiver Schiefe ist das strukturell falsch.

Die rangbasierte Variante PG2 sah im Shadow besser aus (27.8× gegen 19.1×), aber ihre direkte Markt-Timing-P&L der früh verkauften Drittel beträgt minus 3'239 USD. Der Vorsprung ist ein Lot-, Cash- und Sequenzartefakt über das Compounding und ausdrücklich kein belastbarer Grund (PG_SHADOW_ABSCHLUSSBERICHT_2026-07-14.md). Der Entscheid lautete: keine Umstellung, kein Profit-Guard ist die konsistente Wahl.

### 3.3 Pauschale Cooldowns

Zeit-Cooldowns nach einem Guard-Exit kosten drei bis vier CAGR-Punkte. Nur die Regel "Wiedereinstieg erst bei neuem Hoch" verbessert etwas (45 Prozent CAGR, minus 45 Prozent Drawdown, Sharpe 1.04). Das Problem ist der Guard-Exit selbst, nicht der Wiedereinstieg.

### 3.4 Das Growth- und Elliott-Konstrukt

Vier Trades in zwei Jahren, 0 Prozent Trefferquote, Profit-Faktor 0.0, Validierungsscore 37 bis 44 von 100, Monte-Carlo mit 100 Prozent Verlustwahrscheinlichkeit auf allen drei Risikostufen (VALIDATION_REPORT.md, VALIDATION_growth.md). Das Elliott-Modul ist per Design auf maximal 25 Prozent Gewicht gedeckelt, subjektiv und nie isoliert als profitabel nachgewiesen. Beides fällt ersatzlos weg.

### 3.5 Inverse Volatilitätsgewichtung

Auf den echten Projektdaten getestet und verworfen: 48.2 Prozent CAGR gegen 63.8 Prozent bei Gleichgewichtung plus Gate, bei höherem Turnover (24.9× gegen 17.9×). Wichtig ist hier weniger das Ergebnis als das Vorgehen — die Empfehlung stammte aus einem Audit und wurde vor dem Einbau gemessen.

### 3.6 Manuelle Eingriffe

Der ETH-Kauf ohne Regelsignal und der NVDAx-Teilverkauf gegen die Systemlogik gehören zu den grössten Einzelverlusten. Die ETH-Runde allein kostete rund 4.55 USD netto bei einem Konto von rund 1'050 USD.

---

## 4. Die belegten methodischen Fallen

Diese Liste ist der eigentliche Wert aus Project Aurum. Jeder Punkt ist im Altprojekt tatsächlich passiert.

**1. Kostenannahme um Faktor drei zu tief.** Die Research rechnete mit 0.10 Prozent pro Umschlag, real sind Kraken-Spot-Taker 0.26 bis 0.40 Prozent plus Spread. Im Projekt existierten vier widersprüchliche Gebührenkonstanten gleichzeitig (0.001, 0.0026, 0.003, real 0.004 je Seite).

**2. Backtest und Live messen verschiedene Ausführungspfade.** Der Backtest füllte als Maker-Limit 0.15 Prozent unter Signalkurs, live wurde Taker-Market gekauft. Differenz rund 0.30 Prozent pro Trade bei Zielgrössen von 1.5 bis 2 Prozent. Das allein erklärt einen scheinbaren Edge vollständig.

**3. Look-ahead im Live-Pfad, nicht im Backtest.** Der Live-Signalpfad wertete die laufende, unfertige Kerze aus, der Backtest den bestätigten Schluss. Dieser Befund wurde zweimal dokumentiert und nie gefixt.

**4. Failsafe in die falsche Richtung.** Bei Datenausfall gab das Regime-Gate den Wert 1.0 zurück, ein Datenausfall führte also zu mehr Risiko statt zu weniger.

**5. Ein Datenfehler perpetuiert sich selbst.** Eine Zeile in DOT_1d.csv mit leerem Datumsfeld und einem Preis von 2.03 USD bei tatsächlich 0.85 USD (plus 140 Prozent) blieb dauerhaft in der Datei, weil eine Zeile ohne Datum nie als Duplikat erkannt wird und die Sortierung sie ans Ende schiebt. Ein Scan aller 137 OHLC-Dateien fand elf betroffene Dateien in elf Defektklassen, darunter 183 Duplikate in einer Datei und Schlusskurse ausserhalb der Hoch-Tief-Spanne.

**6. Filter sind kein Schutz.** Dass der defekte DOT-Kurs das Live-Ziel nicht vergiftete, lag an einem Notna-Filter, der im Bericht selbst als Zufallsschutz und nicht als Design bezeichnet wird. Eine Zeile mit gültigem Datum und falschem Preis wäre durchgelaufen.

**7. Survivorship im Universum.** Sechs heute überlebende Coins für eine Top-3-Auswahl. Niemand hätte 2018 genau diese sechs gewählt. Bei den Aktien wurde mit einem Universum aus heutigen Gewinnern inklusive NVDA und TSLA gearbeitet, was die Schlagzeilenzahl CAGR 23.1 Prozent und Profit-Faktor 7.98 erzeugte.

**8. Tuning und Validierung auf denselben Daten.** Rund 25 Stellschrauben, getunt und validiert auf denselben zwölf Monaten. Ein Volumen-Gate war faktisch abgeschaltet (Wert minus 99) im Widerspruch zur Dokumentation.

**9. In-Sample-Kennzahlen in der Kommunikation.** Der Turtle-Profit-Faktor von 6.71 war In-Sample. Die Zahl "52 Prozent CAGR" war das idealisierte Signalmodell, der modellierte Full-Live-Replay ergab 43 Prozent, die tatsächliche Live-P&L war negativ. Drei Grössen, die nie vermischt werden dürfen.

**10. Ablation ist keine Kausalattribution.** Die Reihenfolge des Zuschaltens beeinflusst die Zuordnung. Ein früherer Befund "Chandelier neutral" stellte sich als Interaktionsartefakt heraus.

**11. Aggregatvorteile können Sequenzartefakte sein.** Siehe Profit-Guard PG2 oben.

**12. Sechs parallele Order-Pfade, ein Kill-Switch mit null Checks in vier davon.** Dazu kein prozessübergreifender Lock und ein Rebalancer, der jede fremde Position einfaltet. Ergebnis war Ping-Pong auf echtem Geld und ein Doppelausführungs-Bug mit rund 339 USD unbeabsichtigtem Zusatzvolumen.

**13. API-Server ohne Authentifizierung mit CORS-Wildcard.** Jede beliebige Webseite im Browser konnte Endpunkte wie Autopilot-Start, Kill-Switch-Reset und Live-Rebalancing auslösen.

**14. Zähler am Prozessstart statt am Kalender.** Tages- und Wochen-Verluststopps massen seit Prozessstart, das Tageslimit für Orders wurde nie zurückgesetzt, der Drawdown-Anker stand auf einem Paper-Default von 100'000 statt auf dem echten Kontostand.

**15. Betrieb auf macOS mit launchd scheiterte an den Systemberechtigungen.** Status 126 und "Operation not permitted" im Dokumente-Ordner. Die Datensammlung stand deshalb wochenlang still, ohne dass jemand alarmiert wurde.

**16. Die Überwachungsgrösse war selbst falsch.** Das Feld stale_days meldete 0, weil es die letzten 21 Prüfzeilen auswertete statt Kalendertage. Ein Vorwarnsignal vom 25.07. ("Daten veraltet, 4 Tage") wurde nie eskaliert.

**17. Gebühren dominieren bei kleinem Konto.** Bei 2'941 USD Handelsvolumen auf einem Konto von 1'050 USD entstand ein 2.8-facher Kontoumschlag. Fünf von zwölf brutto profitablen Trades wurden netto negativ.

**18. Positive Schiefe ist ein Strukturmerkmal.** Ohne die drei besten Wochen bleiben von 31.4× nur 11.1×. Beim Turtle-SOL-Sleeve ohne die drei besten Trades minus 38 Prozent. Jede Regel, die Gewinner kappt, greift genau diese Struktur an.

---

## 5. Was der Regime-Research-Ansatz beiträgt

Das Teilprojekt AURUM_CRYPTO_REGIME_RESEARCH_V1 vom 03.08.2026 ist methodisch das Beste, was im Altprojekt entstanden ist. Es ist eine Vorregistrierung im Sinne strenger Quant-Forschung: vier Stufen (Existenz von Regimen ohne jeden Bezug zu Gewinn und Verlust, Strategie-Edge ohne Filter, inkrementeller Wert des eingefrorenen Filters, Overlays), Nullhypothese zuerst, Walk-Forward mit genau einmaliger Nutzung des Test-Splits, Protokollierung jeder getesteten Konfiguration, Multiple-Testing-Korrektur, drei Kostenszenarien mit der Regel, dass ein Edge nur unter optimistischen Kosten als nicht vorhanden gilt, Point-in-Time-Universum inklusive delisteter Coins.

Die Stufe-1-Spezifikation definiert vier orthogonale Zustandsdimensionen mit konkreten, vorregistrierten Schwellen und harten Ausschlusskriterien (Median-Verweildauer mindestens zehn Bars, Ein-Bar-Episoden höchstens 25 Prozent, Jitter-Übereinstimmung im Mittel mindestens 85 Prozent).

**Der Stand ist jedoch: alles spezifiziert, nichts gerechnet.** Im Ordner existieren nur das README, der Design-Bericht und die Stufe-1-Spezifikation. Keine Daten, keine Notebooks, keine eingefrorenen Regime, kein einziges Ergebnis. Die Ordner für die Stufen 2 bis 4 und das Universum fehlen ganz.

**Zwei Dinge daran müssen für Aurum II geändert werden.** Erstens ist der Guardrail "Long/Flat Spot, kein Short, kein Leverage" nicht mehr gültig, weil Aurum II auch Perpetual Futures handeln soll. Das ist keine Kleinigkeit: Die Regime-Definitionen sind long-gefärbt (Stress wird als "unter der 200-Tage-Linie" kodiert, also als Gefahr statt als Chance), und die Benchmarks Cash und Nicht-Handeln sind nicht mehr die natürliche Untergrenze. Zweitens fehlt in sämtlichen Dokumenten alles, was Perpetuals ausmacht: Margin und Liquidation, Funding als laufender Bestandteil des Ergebnisses, Basis zwischen Spot und Perp, Netting über beide Beine, Short-Squeeze- und Gap-Risiko, Gegenparteirisiko bei Derivaten.

Ein Widerspruch ist zu bereinigen: Die Regime-Spezifikation baut auf ADX(14) und Bollinger-Band-Breite, die ältere Trading-Engine-Spezifikation bewertet ADX als optional und Bollinger als weitgehend redundant zu ATR plus EMA-Abstand. Ferner nutzt die Research SMA 100 und 200 auf Tagesbasis, die Blueprints EMA 20/50/200 sowie Wochenkerzen als primären Regime-Zeitrahmen.

---

## 6. Übernahmeentscheid für Aurum II

### Wird übernommen

**Methodik und Governance vollständig.** Vorregistrierung, Nullhypothese zuerst, Walk-Forward, einmaliger Test-Split, Konfigurationsprotokoll, Multiple-Testing-Korrektur, drei Kostenszenarien, Point-in-Time, Survivorship-freies Universum inklusive gescheiterter Coins. Diese Ebene ist richtungsneutral und gilt für Short und Hebel unverändert.

**Der langsame Trendfolge-Kern** mit 55/20-Donchian auf bestätigten Bars, Wilder-ATR(20), 2N-Stopp mit Vorrang.

**Der schnelle Rotationskern in der Und-Form** (MA50 und positives Momentum), Top-3 gleichgewichtet, wöchentlich.

**Das graduelle Regime-Gate** als Exposure-Steuerung statt als Ein-Aus-Schalter.

**Das Chandelier-Trailing mit 3× ATR** als einziger aktiver Gewinn-Exit. Zwei ATR erzeugen Whipsaw (64 Exits und 52 Wiedereinstiege), vier und fünf bringen nichts.

**Die Datenintegritäts-Schicht** aus PHASE1G in voller Härte, als Eigenschaft des Datenmodells und nicht als Codekonvention.

**Die Betriebsdisziplin**: Shadow vor Live, getrennte Freigabe je Änderung, ein Parameter je Variante, definierter Rollback, additive Tabellen mit Eindeutigkeitsbedingung, automatisierter Isolationsbeweis, künstlicher Ende-zu-Ende-Test statt Warten auf ein Marktsignal.

**Die Risiko-Ebenen-Struktur** mit gestufter Eskalation: Verlustbudget je Trade, Tagesverlustgrenze, Freeze, Hard-Kill.

**Die Evidenz-Schwellen**: mindestens 90 Tage und 100 Trades für ein Urteil, mindestens sechs Monate für Rebalance-Strategien, Warnschwelle unter 30 Trades, Deflated Sharpe und Probability of Backtest Overfitting als Pflicht-Gates.

### Wird zurückgelassen

Der gesamte xStock- und Aktienteil. Alles Intraday und alles Scalping. Der Profit-Guard in jeder Form. Pauschale Zeit-Cooldowns. Das Growth- und Elliott-Konstrukt. Die inverse Volatilitätsgewichtung. Der leichte Backtest-Modus, der zur Beschleunigung eine andere Signalberechnung nutzt als der Live-Pfad und damit genau das Leitprinzip bricht, mit dem die Architektur begründet wurde. Die Bot-Gewichtung anhand von 14 Trades. Der Modus-Wildwuchs aus sechs Dashboard-Reitern, drei umschaltbaren Strategien, einem LaunchAgent und acht Start-Skripten.

Ebenso die alte Codebasis als Ganzes. Sie enthält eine Datei mit 107'000 Zeichen und 81 Endpunkten, zwei parallele Datenbanken, tote Schemata, widersprüchliche Parameter an drei Orten und einen als tot markierten Turtle-Motor. Übernommen werden Bausteine und Erkenntnisse, nicht der Bestand.

### Muss neu gedacht werden

Alles, was mit der Short-Seite und mit Hebel zu tun hat. Dafür existiert im gesamten Altbestand **kein einziger validierter Wert**. Der Futures-Zweig hat eine leere Backtest-Tabelle und sechs Paper-Momentaufnahmen mit unverändertem Wert. Die einzige Futures-Zahl überhaupt (plus 121.7 Prozent ungebremst, mit Verlustbremsen Drawdown von minus 49.6 auf minus 11.5 Prozent, Validierungsscore 67 von 100) stammt aus einer frühen Phase und ist regimeabhängig.

Interessant ist ein Detail: Pyramiding und Unit-Sizing wurden im Altprojekt nur deshalb verworfen, weil vier Units bei einem Konto von 1'000 USD 126 Prozent des Kapitals gebunden hätten. Mit Perpetuals entfällt genau diese Kapitalschranke, weil Margin statt Notional gebunden wird. Der Ablehnungsgrund war Kapital, nicht Regelqualität. Damit werden diese Regeln wieder verhandelbar, allerdings tauscht man die Kapitalschranke gegen Liquidations- und Funding-Risiko ein.

---

## 7. Die einzige belegte Korrelationszahl

SOL zu BTC 0.57 und SOL zu ETH 0.64 im Turtle-Kontext, im Exposure-Modul auf echten Daten dagegen 0.85 bis 0.93 zwischen den Majors bei einem Alt-Beta von 1.1 bis 1.24. Für ein reines Krypto-System ist das die wichtigste Einzelzahl überhaupt, weil sie Diversifikation innerhalb des Universums weitgehend als Illusion entlarvt. Ein Korrelationslimit war im Altprojekt als eine der drei lohnenden Massnahmen benannt, wurde aber nie gebaut und nie getestet.

---

## 8. Ehrliche Erwartungshaltung

Aus GESAMTSTRATEGIE_2026-07-13.md, Szenarien mit Erwartungswert, Volatilität und Worst Case:

| Szenario | Erwartung p.a. | Volatilität | Worst Case | Wahrscheinlichkeit negatives Jahr |
|---|---|---|---|---|
| Defensiv | 6.0 % | 11 % | −18 % | 29 bis 32 % |
| Ausgewogen | 9.5 % | 17 % | −28 % | 29 bis 32 % |
| Offensiv | 13.0 % | 28 % | −45 % | 29 bis 32 % |

Dazu die Kostenschwellen: Ein Coin-Round-Trip kostet als Maker rund 0.52 Prozent und als Taker rund 0.82 Prozent. Bei einem Chance-Risiko-Verhältnis von 1.5 braucht es mindestens 45 Prozent Trefferquote, bei 1.0 mindestens 52 Prozent plus Kosten. Jede Strategie, die diese Schwelle nicht klar überspringt, ist eine Gebührenmaschine.

---

## 9. Die zehn Sätze, die Aurum II tragen

1. Das Kostenmodell wird vor der ersten Strategie festgelegt und ist die einzige Wahrheit im System.
2. Backtest, Paper und Live rechnen mit demselben Code und demselben Ausführungsmodell.
3. Signale entstehen ausschliesslich auf abgeschlossenen Bars, erzwungen im Datenmodell.
4. Datenschreiben ist validierend, fail-closed und atomar. Ein defekter Batch wird ganz verworfen.
5. Ein Motor, ein Lock, klare Eigentumszuordnung je Position.
6. Kein fixer Gewinn-Exit. Trends dürfen laufen.
7. Exposure wird graduell gesteuert, nicht ein- und ausgeschaltet.
8. Der Kill-Switch gilt für jeden Pfad ohne Ausnahme, auch für neue.
9. Kapital folgt der Evidenz, nicht die Evidenz dem Kapital.
10. Ein System, das nicht läuft, verliert zuverlässiger als eines, das falsch handelt. Überwachung ist Teil der Strategie.

---

## 10. Quellenverzeichnis

Alle Dateien liegen unter Dokumente/Claude/Projects/Cryptobot.

**Forschung und Konzept**: Crypto-Only/AURUM_CRYPTO_REGIME_RESEARCH_V1/00_report/AURUM_CRYPTO_REGIME_RESEARCH_V1_Design.md, Crypto-Only/AURUM_CRYPTO_REGIME_RESEARCH_V1/01_regime_research/STUFE1_REGIME_SPEC.md, AURUM_Crypto_Bot_Blueprint.docx, AURUM_Trading_Engine_Spec.docx, AURUM_Engineering_Implementation_Blueprint.docx, INTRADAY_NEUKONZEPT_KESTREL_2026-07-02.md

**Audits und Performance**: aurum-trader/AUDIT_BERICHT_2026-07-02.md, AUDIT_XQUANT_2026-07-02.md, PERFORMANCE_ANALYSE_2026-07-10.md, REBALANCE_UND_ASSETS_ANALYSE_2026-07-13.md, GESAMTSTRATEGIE_2026-07-13.md, QRP_PHASE0_BESTANDSAUFNAHME_2026-07-15.md, UMSETZUNG_2026-07-02.md

**Strategie-Berichte**: TURTLE_ANALYSE_2026-07-14.md, TURTLE_SLEEVE_ENTSCHEID_2026-07-14.md, TURTLE_SHADOW_ABSCHLUSSBERICHT_2026-07-14.md, TURTLE_MICRO_LIVE_PLAN_FINAL_2026-07-14.md, TURTLE_PHASE0_DIGEST_2026-09-07.md, MOMENTUM_KERN_HANDBUCH_2026-07-14.md, MOMENTUM_AUDIT_2026-07-14.md, MOMENTUM_REPLAY_VALIDIERUNG_2026-07-14.md, MOMENTUM_FULL_LIVE_REPLAY_2026-07-14.md, PG_SHADOW_ABSCHLUSSBERICHT_2026-07-14.md, PG_SHADOW_REDUNDANZ_ANALYSE_2026-07-14.md

**Daten und Betrieb**: PHASE1G_COLLECTOR_HAERTUNG_2026-07-15.md, PHASE1G_DOT_DEFEKT_BEFUND_2026-07-15.md, DESIGN.md, README.md, MAJOR_UPDATE.md, CODE_REVIEW.md, FINALISIERUNG.md, LIVE_ANLEITUNG.md

**Strategie-Bewertungen**: STRATEGIE_BEWERTUNG.md, VALIDATION_REPORT.md, VALIDATION_growth.md, VALIDATION_intraday_bounce.md, ELLIOTT.md, INTRADAY_BOUNCE.md

**Laufender Stand**: Tagesbriefing_2026-09-15.md, Tagesbriefing_2026-09-11.md
