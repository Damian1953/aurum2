# Stufe 2 — Strategie-Edge ohne Regimefilter, Vorregistrierung

**Project Aurum II. Version 1.0 vom 15.09.2026. Status: EINGEFROREN am 15.09.2026. Alle Entscheidungen getroffen, siehe Tabelle am Ende. Prüfsumme dieses Dokuments und der Eingabedaten in `00_doku/ENTSCHEIDE.md`.**

Dieses Dokument ist vor dem ersten Rechenlauf eingefroren worden. Es wird keine Definition, kein Parameter, keine Schwelle und kein Kriterium mehr verändert. Alle Zahlen sind a priori gesetzt und stammen nicht aus Backtests auf den Zieldaten. Entdeckt der Lauf einen Effekt, der hier nicht steht, wird er als Hypothese für Version 2 dokumentiert und nicht in den laufenden Test aufgenommen.

Stufe 1 ist abgeschlossen. `frozen_regimes_v1.json` trägt den Status «kein Kandidat tauglich». Diese Entscheidung ist endgültig und wird in Stufe 2 nicht berührt. Es gibt in Stufe 2 keinen diskreten Regimefilter. Kontinuierliche Grössen wie der Abstand zum gleitenden Durchschnitt oder Volatilitätsperzentile, die sich in Stufe 1 als robust erwiesen haben, werden in Stufe 2 **nicht** als Exposure-Gate verwendet. Sie sind für eine spätere Stufe vorgemerkt, siehe Abschnitt 22.

---

## 1. Forschungsfrage

Haben konkrete, vollständig vorab definierte Handelsstrategien auf liquiden Kryptowährungen einen eigenständigen, statistisch und ökonomisch belastbaren Edge, wenn sie ohne vorgeschalteten Regimefilter gehandelt werden und wenn realistische Kosten, Funding und die Trennung vom Marktbeta berücksichtigt sind?

Eine Strategie hat einen Edge, wenn sie nach realistischen Kosten eine positive Erwartung liefert, die über Coins und Zeitblöcke stabil ist, gegen kleine Parameteränderungen unempfindlich bleibt, auf genügend unabhängigen Trades beruht, ein tragbares Tail-Risiko hat und sich von einer passiven Position mit gleicher Marktexposure unterscheidet.

Getrennt davon, in Abschnitt 21, wird untersucht, welche der vorregistrierten Trendfolge-Varianten dem öffentlich beschriebenen Market Trend Pro von Travis Woo strukturell am nächsten kommt. Das ist eine Ähnlichkeitsfrage, keine Edge-Frage, und sie hat keinen Einfluss auf die Bewertung.

---

## 2. Nullhypothesen

Je Strategiefamilie gilt dieselbe Nullhypothese, geprüft je Variante und je Seite:

**H0.** Die Strategie erzeugt nach realistischen Kosten (Szenario K1) keine positive Erwartung, die über eine passive Position mit gleicher durchschnittlicher Marktexposure hinausgeht. Beobachtete Überrenditen sind mit Marktbeta, Zufall und der Zahl der getesteten Varianten vereinbar.

Formal: Der 5-Prozent-Perzentilwert der bootstrappten annualisierten Überrendite gegenüber Cash ist kleiner oder gleich null, oder der Holm-korrigierte Bootstrap-p-Wert für Sharpe grösser null liegt über 5 Prozent, oder die Strategie besteht weder den Alpha- noch den Risikotransformations-Teiltest gegen die exposure-gleiche Passivposition.

Zusätzlich für Familie A:

**H0-A8.** Der SMA200-Filter liefert keinen Mehrwert. Die Variante W2 (mit Filter) ist nach Kosten nicht besser als W8 (ohne Filter) in Sharpe, Calmar und Verhalten in Baissejahren.

**H0-A6.** Pyramiding liefert keinen Mehrwert. Die Varianten W6 und W7 sind nach Kosten nicht besser als W2 und W4 in Sharpe, Calmar und Erwartung je Trade.

---

## 3. Alternativhypothesen

**H1.** Mindestens eine Variante einer Familie erfüllt alle Bestehenskriterien aus Abschnitt 18.

**H1-A.** Trendfolge mit Ausbruch auf Tagesbasis hat einen Edge, der wesentlich aus wenigen grossen Gewinnern stammt, bei einer Trefferquote unter 50 Prozent.

**H1-A8.** Der SMA200-Filter reduziert Drawdown und verbessert Calmar, bei geringerem CAGR.

**H1-A6.** Pyramiding erhöht CAGR und Calmar, bei höherem Drawdown.

**H1-B.** Kurzfristige Überdehnung kehrt in liquiden Krypto-Märkten zurück, aber der Effekt überlebt die Kosten des Szenarios K1 nicht. Diese Alternative wird ausdrücklich erwartet, siehe Strategiebewertung vom 15.09.2026.

**H1-C.** Time-Series-Momentum über 21 bis 126 Tage hat einen Edge, der nach 2021 schwächer ist als davor.

**H1-D.** Funding ist als laufende Carry-Komponente kein eigenständiger Edge, sondern eine Kostenposition, deren Vorzeichen für die Richtungswahl schwach informativ ist.

Die Hypothesen sind Erwartungen. Sie beeinflussen weder Definitionen noch Kriterien.

---

## 4. Strategiefamilien

| Familie | Inhalt | Varianten primär | Seiten |
|---|---|---|---|
| A | Trendfolge und Ausbruch, Woo-artige Testmatrix | W0 bis W8 | Long-only für alle, Short-only und Long+Short für W2, W4, W8 |
| B | Mean Reversion auf Überdehnung | MR | Long-only, Short-only, Long+Short |
| C | Momentum, Trendfortsetzung | TS21, TS63, TS126, XS21 | Long-only, Short-only, Long+Short |
| D | Carry, Funding, Perpetual-Daten | CC, FC, OI (bedingt) | CC marktneutral, FC und OI Long-only, Short-only, Long+Short |

Jede Strategie läuft je Coin als eigenständiger, ungehebelter Einzel-Sleeve. Portfolio-Effekte sind nicht Gegenstand von Stufe 2. Ein gleichgewichteter Durchschnitt der Einzel-Sleeves wird als «gepooltes Ergebnis» berichtet und dient den gepoolten Kriterien in Abschnitt 18.

---

## 5. Exakte Signaldefinitionen, gemeinsame Bausteine

Alle Grössen strikt trailing. Zum Bar t fliesst nur Information bis einschliesslich t ein.

- `SMA(n)` einfacher gleitender Durchschnitt des Schlusskurses über n Bars
- `ATR14` Wilder-ATR mit Periode 14, identische Implementierung wie in Stufe 1 (verifiziert gegen unabhängige Referenz auf 1e-11)
- `HH(N) = max(High[t−N … t−1])`, Ausbruchsniveau ohne den aktuellen Bar
- `LL(N) = min(Low[t−N … t−1])`
- `ret(L) = Close_t / Close_{t−L} − 1`
- `z(n) = (Close_t − SMA(n)_t) / SD(n)_t` mit Stichproben-Standardabweichung über n Bars
- `f_7d` Mittel der relativen stündlichen Funding-Rate über 168 Stunden, annualisiert mit 8760, am UTC-Tagesende
- `basis_t = Perp_Close_t / Spot_Close_t − 1`

**Ausführungsregel für alles.** Signal auf dem Schlusskurs von Bar t, Ausführung zur Eröffnung von Bar t+1. Das gilt auch für Stopps: Ein Stopp gilt als ausgelöst, wenn der Schlusskurs von t das Stoppniveau erreicht oder unterschreitet, ausgeführt wird zur Eröffnung von t+1. Kurslücken werden dadurch vollständig getragen, nicht wegmodelliert. Es gibt keine Intraday-Annahmen.

**Wiedereinstieg.** Nach jedem Ausstieg ist ein neuer Einstieg beim nächsten gültigen Signal erlaubt. Kein Cooldown. Das Altprojekt hat Zeit-Cooldowns als schädlich belegt.

**Warmup.** Eine Strategie beginnt am ersten Bar, an dem alle benötigten Grössen definiert sind. Für Varianten mit SMA200 und 252-Tage-Ausbruch ist das rund 252 Bars nach Datenbeginn.

---

## 6. Familie A, Woo-Untermodelle

Öffentlich rekonstruierbare Kernelemente von Market Trend Pro, wie sie in dieser Vorregistrierung verwendet werden: Tageschart, langfristiger Trendfilter über SMA200, Ausbruchseinstiege, kein fixes Gewinnziel, breite volatilitätsangepasste Stopps um 3 bis 4 ATR, Nachziehen des Stopps bei weiteren Ausbruchskäufen, Long oder Cash. Wir kennen den Code nicht und behaupten das nicht. Wir testen eine kleine, vorab fixierte Matrix öffentlich plausibler Varianten.

**Der SMA200-Filter ist Bestandteil der Strategiedefinition, kein Regimefilter im Sinne von Stufe 1.** W8 prüft seinen Wert.

**Interpretationskontext, Stand 15.09.2026, ohne Wirkung auf Regeln.** Nach öffentlicher Darstellung beruft sich Woo auf Richard Dennis und das Turtle-Trading sowie auf Mark Minervini (Kauf von Stärke, Ausbruch auf neue Hochs). Das stützt Donchian-artige N-Tage-Ausbrüche, ATR-Logik, Pyramiding und einen Ertrag aus wenigen grossen Gewinnern als Rekonstruktionshypothesen, ohne dass Original-Turtle-Parameter unterstellt werden. MTP ist danach eher langfristiger Filter plus New-High-Ausbruch plus mechanischer Exit als ein Indikator-Mix. Öffentlich ist zudem zu trennen zwischen **Woo Legacy** (SMA200-Long-Filter, ATH- und Ausbruchseinstiege, Calendar-Low-Reclaim-Dips, 3 bis 4 ATR Stopps, Pyramiding, kein fixes Gewinnziel) und **MTP 2.4** (langfristiger Filter, Breakout als Einstieg oder Add-on, bei weiteren Breakout-Käufen nachgezogener Stopp, Long oder Cash, über Assets robuste Einstellungen). Keine Legacy-Regel gilt automatisch als MTP-2.4-Regel. Calendar-Low-Reclaim-Dips sind nicht Teil dieser Matrix. Positionsgrösse, Prozentrisiko und Teile der Stopp-Einstellungen sind bei MTP nutzerkonfigurierbar. Stufe 2 testet deshalb die Signal- und Exit-Logik, nicht Woos Kapital- oder Hebelwahl, was mit dem Notional-Sizing in Abschnitt 10 übereinstimmt. Woo beschreibt seine Parameterwahl selbst als Test über mehrere Assets mit anschliessender Wahl mittlerer Einstellungen statt des Backtest-Maximums. Das deckt sich mit dem Plateau-Prinzip in Abschnitt 17 und ist dort methodischer Kontext, kein Optimierungsziel. Vollständige Zusammenstellung in `woo_kontext_v1.md`.

| ID | Filter | Einstieg | Stopp | Zusatz-Exit | Pyramiding |
|---|---|---|---|---|---|
| W0 | – | Close kreuzt über SMA200 | keiner | Close kreuzt unter SMA200 | nein |
| W1 | Close > SMA200 | Close > HH(20) | 3 ATR, nachziehend | Close < SMA200 | nein |
| W2 | Close > SMA200 | Close > HH(55) | 3 ATR, nachziehend | Close < SMA200 | nein |
| W3 | Close > SMA200 | Close > HH(100) | 3 ATR, nachziehend | Close < SMA200 | nein |
| W4 | Close > SMA200 | Close > HH(252) | 3 ATR, nachziehend | Close < SMA200 | nein |
| W5 | wie W2 | wie W2 | 4 ATR, nachziehend | wie W2 | nein |
| W6 | wie W2 | wie W2 | wie W2 | wie W2 | ja, Abschnitt 10 |
| W7 | wie W4 | wie W4 | wie W4 | wie W4 | ja, Abschnitt 10 |
| W8 | – | Close > HH(55) | 3 ATR, nachziehend | keiner | nein |

**Einstieg.** Bedingung am Schluss von t erfüllt und keine offene Position: Kauf zur Eröffnung von t+1. Ein Kreuzen bei W0 bedeutet `Close_t > SMA200_t` und `Close_{t−1} ≤ SMA200_{t−1}`. Für W1 bis W8 genügt `Close_t > HH(N)_t`, ein Kreuzen ist nicht nötig, weil HH(N) den aktuellen Bar ausschliesst.

**Nachziehender Stopp.** Beim Einstieg `stop = Entry_Fill − k · ATR14_t`. An jedem Folgetag `stop = max(stop, HighestClose_seit_Einstieg − k · ATR14_t)`. Der Stopp wird nie gesenkt. `k` ist 3.0, bei W5 4.0.

**Ausstieg.** Zur Eröffnung von t+1, wenn am Schluss von t gilt: `Close_t ≤ stop` oder, bei Varianten mit Filter, `Close_t < SMA200_t`. Der frühere Auslöser gilt.

**Short-Varianten (nur W2, W4, W8).** Spiegelbildlich: Filter `Close < SMA200`, Einstieg `Close < LL(N)`, Stopp `Entry + k · ATR14`, nachziehend auf `LowestClose_seit_Einstieg + k · ATR14`, Zusatz-Exit `Close > SMA200`. Die Short-Varianten heissen W2S, W4S, W8S. **Sie sind Aurum-Hypothesen und werden nicht als Travis-Woo-Strategie bezeichnet.** Long+Short ist die Summe der beiden unabhängigen Sleeves mit je halbem Kapital.

**Parameter-Nachbarschaft (Jitter), nur für W2 und W8.** Ausbruch N ∈ {40, 80} zusätzlich zum Basiswert 55. ATR-Multiplikator k ∈ {2.5, 3.5} zusätzlich zu 3.0. SMA-Länge ∈ {150, 250} zusätzlich zu 200 (nur W2). Je Jitter wird genau ein Parameter verändert. Das ergibt für W2 sechs und für W8 vier Nachbarn. Die Reihe W1, W2, W3, W4 bildet zusätzlich die Ausbruchsachse 20, 55, 100, 252 ab. **Keine Kombinationsmatrix.**

---

## 7. Familie B, Mean Reversion

Eine Definition, drei Seiten.

**MR-L.** Einstieg long, wenn `z(20)_t ≤ −2.0`. Ausstieg zur Eröffnung von t+1, wenn `Close_t ≥ SMA(20)_t` oder wenn `Close_t ≤ Entry_Fill − 3 · ATR14_Entry` oder nach 10 Bars Haltedauer. Der früheste Auslöser gilt.

**MR-S.** Spiegelbildlich: Einstieg short bei `z(20)_t ≥ +2.0`, Ausstieg bei `Close_t ≤ SMA(20)_t`, Stopp `Entry + 3 · ATR14_Entry`, Zeitlimit 10 Bars.

**MR-LS.** Beide Sleeves mit je halbem Kapital.

**Jitter.** z-Schwelle ∈ {1.5, 2.5}, Fenster n ∈ {10, 30}, Zeitlimit ∈ {5, 20}. Je Jitter ein Parameter. Sechs Nachbarn je Seite.

Die Kostenhürde aus der Strategiebewertung sagt für Haltedauern von zwei bis fünf Tagen einen jährlichen Kostenaufwand von 10 bis 17 Prozent des Notionals auf Perpetuals voraus. Die Familie wird trotzdem vollständig gerechnet, weil ein sauberes Nein ein gültiges Ergebnis ist.

---

## 8. Familie C, Momentum

**TS(L), Time-Series-Momentum.** Alle sieben Bars, beginnend mit dem ersten definierten Bar, wird die Position neu bestimmt: `w = sign(ret(L)_t)`. Long-only: `w = max(w, 0)`. Short-only: `w = min(w, 0)`. Long+Short: `w` wie berechnet. Zwischen den Stichtagen bleibt die Position unverändert. Kosten fallen nur bei Positionsänderung an. `L ∈ {21, 63, 126}` sind drei getrennte primäre Varianten TS21, TS63, TS126.

**Jitter.** L um 25 Prozent (16 und 26 für 21, 47 und 79 für 63, 95 und 158 für 126), Stichtagabstand ∈ {5, 10}. Je Jitter ein Parameter.

**XS21, Cross-Sectional.** Alle sieben Bars: Unter allen an diesem Tag definierten Coins mit `ret(21) > 0` werden die drei mit dem höchsten `ret(21)` gleichgewichtet long gehalten (Long-only). Short-only: die drei niedrigsten unter den Coins mit `ret(21) < 0`. Long+Short: beide Beine mit je halbem Kapital. Sind weniger als drei Coins geeignet, wird der Rest in Cash gehalten. Kein Gate über gleitende Durchschnitte, weil das in Stufe 2 nicht zulässig ist.

**Jitter XS.** L ∈ {42, 63}, Top-N ∈ {2, 4}.

XS21 läuft auf dem Zehn-Coin-Universum und ist damit survivorship-behaftet, siehe Abschnitt 15. Das wird im Bericht bei jeder XS-Zahl vermerkt. Familie C ist bewusst von Familie A getrennt: kein Ausbruchsniveau, kein Stopp, kein Filter, feste Stichtage.

---

## 9. Familie D, Carry, Funding, Perpetual-Daten

Universum: alle Coins aus Abschnitt 15, für die eine Binance-USDT-M-Perpetual-Reihe existiert, jeweils ab dem ersten Funding-Zeitstempel. Funding wird als kontinuierliche Grösse verwendet, nie als diskreter Zustand. Die Stufe-1-Schwelle von 10 Prozent annualisiert kommt hier nur als Einschaltschwelle für D-CC vor, nicht als Regime.

**D-CC, Cash-and-Carry, marktneutral.** Am Schluss von t gilt `f_7d ≥ 0.10` und keine Position offen: zur Eröffnung von t+1 Kauf Spot Notional 1.0 und Verkauf Perp Notional 1.0. Ausstieg beider Beine zur Eröffnung von t+1, wenn am Schluss von t `f_7d ≤ 0`. Ergebnis je Stunde ist das erhaltene Funding auf dem Short-Bein, dazu die Veränderung der Basis zwischen Ein- und Ausstieg (Perp-Schluss gegen Spot-Schluss), abzüglich der Kosten auf vier Beinen. Die Spot-Beine werden mit dem Spot-Kostenmodell belastet: K0 0.16, K1 0.40 plus 0.02, K2 0.80 plus 0.06 je Seite. Jitter: Einschaltschwelle ∈ {0.05, 0.15}, Fenster ∈ {3 Tage, 14 Tage}.

**D-FC, Funding-konträr, gerichtet, kontinuierlich.** Alle sieben Bars: `w = clip(−f_7d / 0.30, −1, +1)`. Hohes positives Funding bedeutet überfüllte Long-Seite und führt zu einer Short-Gewichtung, negatives Funding zu einer Long-Gewichtung. Long-only `max(w, 0)`, Short-only `min(w, 0)`, Long+Short `w`. Jitter: Skala ∈ {0.20, 0.40}, Fenster ∈ {3 Tage, 14 Tage}. Die konträre Richtung ist die vorregistrierte Hypothese. Eine Funding-Momentum-Variante mit umgekehrtem Vorzeichen wird in Version 1 nicht getestet und ist als Hypothese für Version 2 vorgemerkt.

**D-OI, Open Interest, bedingt.** Entschieden am 15.09.2026: bedingt vorregistriert. Läuft je Coin nur, wenn alle folgenden Bedingungen erfüllt sind, geprüft vor dem Rechenlauf und protokolliert:

- Quelle ist ausschliesslich das Binance-Vision-Archiv `futures/um/daily/metrics/{SYMBOL}/`, Feld `sum_open_interest`, Tageswert gleich letzte Beobachtung vor 00:00 UTC des Folgetags.
- Mindestens 1095 Tageswerte (drei Jahre) je Coin.
- Integrität: alle Werte positiv, Zeitachse monoton, keine Duplikate, keine Lücke über drei Tage. Eine Lücke bis drei Tage hält die Position unverändert. Ein Coin mit einer längeren Lücke oder einem nicht positiven Wert wird für D-OI **ausgeschlossen**, nicht repariert.
- Fail-closed: Erfüllen BTC und ETH die Bedingungen nicht beide, wird D-OI **gar nicht** gerechnet, und N in Familie D ist 4. Erfüllen sie sie, läuft D-OI auf allen Coins, die die Bedingungen erfüllen.
- Die Prüfung erfolgt mechanisch mit `nachladen_historie.py --check` und wird mit Ergebnis in `stage2_results.json` festgehalten, bevor eine einzige Strategie gerechnet wird.

Regel: Alle sieben Bars: `w = sign(OI_t / OI_{t−7} − 1) × sign(ret(7)_t)`, falls das Open Interest gestiegen ist, sonst `w = 0`. Steigendes Open Interest bei steigendem Kurs heisst Long, bei fallendem Kurs Short, fallendes Open Interest heisst keine Position. Seiten wie bei D-FC. Jitter: Fenster ∈ {5, 14}.

Familie D wird zusätzlich mit dem Kraken-Funding im Überlappungsjahr gegengeprüft. Die Übereinstimmung der Vorzeichen von `f_7d` zwischen Binance und Kraken muss mindestens 90 Prozent betragen, sonst führt der Bericht das als Datenvorbehalt.

---

## 10. Pyramiding (W6, W7) und Position Sizing

### 10.1 Grundgrösse

Jeder Einzel-Sleeve hat ein Kapital von 1.0. Eine Position ohne Pyramiding hat ein Notional von 1.0 (100 Prozent des Sleeves), ungehebelt. Damit ist die Position bei Einstieg exakt so gross wie die Buy-and-Hold-Referenz, und der Vergleich in Abschnitt 13 misst Timing, nicht Grösse.

Risikobasiertes Sizing (fester Prozentsatz des Kapitals je Trade, dividiert durch den Stoppabstand) ist **nicht** Teil des primären Tests. Es ist unter den offenen Entscheidungen am Ende aufgeführt.

### 10.2 Pyramiding, vollständig deterministisch

Gilt nur für W6 (Basis W2) und W7 (Basis W4). Alle anderen Elemente sind mit W2 beziehungsweise W4 identisch, damit der Unterschied allein dem Pyramiding zurechenbar ist.

| Regel | Festlegung |
|---|---|
| Einstiegsunit | Notional 0.50 |
| Maximale Zahl Units | 3 (Einstieg plus zwei Add-ons) |
| Grösse jedes Add-ons | Notional 0.25, damit **maximal 1.00 Notional je Sleeve**, exakt gleich viel Kapital wie W2 beziehungsweise W4 |
| Trigger Add-on | Am Schluss von t gilt **beides**: `Close_t > HH(N)_t` mit demselben N wie beim Einstieg (neues N-Tage-Hoch) **und** `Close_t ≥ Fill_der_unmittelbar_vorhergehenden_Unit + 1.0 · ATR14_t`. Dazu weniger als 3 Units offen. Referenz für den Abstand ist immer der Ausführungspreis der zuletzt gekauften Unit, nicht der Ersteinstieg |
| Ausführung | Eröffnung t+1 |
| Stopp-Anhebung | Nach jedem Add-on `stop = max(stop, AddOnFill − k · ATR14_t)`, danach normales Nachziehen für die Gesamtposition |
| Ausstieg | Die gesamte Position wird auf einmal geschlossen, keine Teilausstiege |
| Gesamtrisiko | Durch die Obergrenze von 1.00 Notional und den gemeinsamen Stopp begrenzt. Kein Hebel, kein separates Risikobudget |

Damit setzen W6 und W7 nie mehr Kapital ein als W2 und W4. Der Unterschied liegt im Zeitpunkt des Kapitaleinsatzes: W2 ist ab dem ersten Ausbruch voll investiert, W6 baut in drei Schritten auf. Der Vergleich misst das Pyramiding-Timing, nicht höhere Exposure. Weil die Einstiegsunit kleiner ist, wird der Vergleich W6 gegen W2 und W7 gegen W4 auf exposure-adjustierten Grössen geführt: Return je Einheit Exposure, Sharpe, Calmar, Erwartung je Trade in R-Multiples (Abschnitt 21). Der absolute CAGR wird berichtet, ist aber für diesen Vergleich nicht massgebend.

### 10.3 Familie D

CC: Notional 1.0 Spot long und 1.0 Perp short. FC und OI: Notional gleich dem berechneten Gewicht, betragsmässig höchstens 1.0.

---

## 11. Stops und Exits, Zusammenfassung

| Familie | Stopp | Exit-Regel | Zeitlimit |
|---|---|---|---|
| A W0 | keiner | Kreuzen unter SMA200 | keines |
| A W1 bis W7 | k · ATR14 nachziehend | Stopp oder Close unter SMA200 | keines |
| A W8 | 3 ATR14 nachziehend | nur Stopp | keines |
| B | 3 ATR14 fix ab Einstieg | Rückkehr zum SMA20 | 10 Bars |
| C | keiner | Neubestimmung am Stichtag | 7 Bars Stichtagabstand |
| D CC | keiner | `f_7d ≤ 0` | keines |
| D FC, OI | keiner | Neubestimmung am Stichtag | 7 Bars |

Kein fixes Gewinnziel in irgendeiner Familie. Keine Teilverkäufe. Das Altprojekt hat fixe Gewinnmitnahmen als schädlich belegt.

---

## 12. Kostenszenarien

Aurum II handelt auf Kraken Perpetuals, siehe Entscheidprotokoll vom 15.09.2026. Das primäre Kostenmodell ist deshalb das Perpetual-Modell. Alle Sätze je Seite in Prozent des gehandelten Notionals.

| Szenario | Gebühr je Seite | Spread und Slippage je Seite | Funding |
|---|---|---|---|
| K0 theoretisch | 0.02 (Maker) | 0.00 | tatsächlich |
| K1 realistisch | 0.05 (Taker) | 0.02 | tatsächlich |
| K2 Stress | 0.10 | 0.06 | tatsächlich, Kostenseite mal 1.5 |

**Funding.** Für jede offene Perp-Position wird jede Stunde die tatsächliche relative Funding-Rate auf das Notional angewandt. Long zahlt bei positivem Funding und erhält bei negativem, Short spiegelbildlich. Unter K2 werden Zahlungen mit 1.5 multipliziert und Erhalte mit 1.0, also asymmetrisch zu Lasten der Strategie. Funding wird nie ignoriert und nie durch einen Durchschnitt ersetzt.

**Umschlag.** Turnover je Jahr = Summe der gehandelten Notionals (Käufe plus Verkäufe) geteilt durch durchschnittliches Sleeve-Kapital, annualisiert. Jede Positionsänderung, auch ein Add-on, ist ein Handel.

**Spot-Referenz.** Für die Long-only-Varianten von Familie A wird zusätzlich das Spot-Modell Kraken Tier 1 Maker (0.40 je Seite plus 0.02 Reibung, kein Funding) berichtet, weil das öffentliche Market Trend Pro ein Spot-System ist. Diese Zahl ist Bericht, kein Kriterium.

**Cash-Ertrag.** Kapital ausserhalb einer Position verzinst sich zum dreimonatigen Treasury-Bill-Satz (Reihe DTB3, im Altprojekt vorhanden). Das gilt für Strategien und für die Cash-Benchmark gleichermassen.

Nichts an diesem Abschnitt wird nach Kenntnis der Ergebnisse angepasst.

---

## 13. Beta-Trennungstest

Die zentrale Frage: Produziert die Strategie einen eigenständigen Timing-Edge, oder ist sie eine komplizierte Form von Long-Beta?

### 13.1 Benchmarks je Coin

1. **B&H Coin.** Buy-and-Hold desselben Coins, Notional 1.0, ohne Kosten ausser einmaligem Einstieg.
2. **B&H BTC.** Buy-and-Hold Bitcoin.
3. **Cash.** Treasury-Bill-Satz.
4. **Exposure-gleiche Passivposition (EP).** Konstante Position im selben Coin mit Notional gleich der durchschnittlichen Exposure der Strategie über den gesamten Zeitraum, Rest in Cash. Hat die Strategie im Mittel 0.37 Notional gehalten, hält EP konstant 0.37. Für Short-Strategien ist EP eine konstante Short-Position mit dem Betrag der durchschnittlichen Short-Exposure, inklusive Funding.
5. **Volatilitätsgleiche Passivposition (VP).** Konstante Position im selben Coin, skaliert so, dass die realisierte Volatilität der Strategie getroffen wird.

### 13.2 Messgrössen

Je Variante, Coin, Seite und Kostenszenario gegenüber EP und B&H Coin:

- Überrendite (CAGR-Differenz)
- Sharpe- und Calmar-Differenz
- Drawdown-Reduktion (MaxDD Strategie geteilt durch MaxDD Benchmark)
- Upside Capture und Downside Capture auf Monatsrenditen
- Alpha und Beta aus einer Regression der täglichen Strategie-Überrenditen auf die täglichen Coin-Überrenditen, Newey-West-Standardfehler mit 10 Lags
- Return je Einheit Exposure: CAGR geteilt durch durchschnittliche Betragsexposure
- Verhalten in Baissejahren: Rendite und MaxDD in allen Kalenderjahren mit negativer BTC-Jahresrendite, mechanisch bestimmt, inklusive laufendem Jahr falls negativ

### 13.3 Bestehenskriterium, zwei getrennte Teiltests

Die Beta-Trennung wird in zwei Teiltests beurteilt, die verschiedene Fragen beantworten. Beide werden im Szenario K1 auf dem gepoolten Ergebnis gegen die exposure-gleiche Passivposition EP geführt.

**13.3a Alpha-Test, echter Return-Effekt.** Bestanden, wenn Alpha aus der Regression grösser als null ist (Newey-West, einseitig, 5 Prozent) **und** die Sharpe Ratio grösser als die von EP ist. Frage: Verdient die Strategie je Einheit Marktrisiko mehr als das Halten des Marktes?

**13.3b Risikotransformations-Test.** Bestanden, wenn MaxDD kleiner als MaxDD von EP **und** Calmar grösser als Calmar von EP **und** Downside Capture höchstens 0.8 mal Upside Capture. Frage: Formt die Strategie das Marktbeta so um, dass Verluste kleiner und Gewinne im Verhältnis grösser werden, auch wenn kein zusätzlicher Ertrag entsteht?

**Urteil.** Kriterium 7 in Abschnitt 18 gilt als erfüllt, wenn mindestens einer der beiden Teiltests besteht. Das Ergebnis trägt die Kennzeichnung **ALPHA**, **RISIKOTRANSFORMATION** oder **BEIDES**. Eine Strategie ohne nachweisbares Alpha, aber mit klarer Risikotransformation, ist ein gültiges, wertvolles Ergebnis und wird so benannt. Eine Strategie, die keinen der beiden Teiltests besteht, ist eine komplizierte Form von Beta.

Für Short-only spiegelbildlich gegen die Short-EP. Für Long+Short gegen die Long-EP der Long-Exposure und Cash.

---

## 14. Datenanforderungen

| Reihe | Quelle | Stand | Verwendung |
|---|---|---|---|
| Spot-Tageskerzen, 10 Coins, USDT | Binance Vision, geladen 15.09.2026, Prüfsummen in `provenance.json` | vorhanden, 2017-08 bis 2026-09-14 | alle Familien |
| Spot-Tageskerzen Kraken USD, BTC ETH SOL | Kraken, 720 Tage | vorhanden | Gegenprobe |
| Perp-Funding stündlich, Kraken | Altprojekt `market_data/funding` | vorhanden, ab 10.09.2025, nur BTC ETH SOL | Gegenprobe Familie D |
| **Perp-Funding, Binance USDT-M** | Binance Vision, Archiv `futures/um/monthly/fundingRate` | **wird vor dem Lauf geladen**, historisch ab 2019-09 für BTC, Erweiterung von `nachladen_historie.py` | Familie D primär, tatsächliche Funding-Cashflows aller Familien |
| **Perp-Tageskerzen, Binance USDT-M** | Binance Vision, `futures/um/monthly/klines` | **wird vor dem Lauf geladen** | Basis für D-CC |
| Open Interest, Binance | Binance Vision, `futures/um/daily/metrics` | **zu prüfen**, vermutlich ab 2021-12 | D-OI, nur bei Verfügbarkeit |
| Treasury-Bill 3 Monate | Altprojekt `market_data/reference/DTB3_3m_tbill.csv` | vorhanden, zu kopieren | Cash-Ertrag |

**Entschieden.** Die Binance-Funding-Historie und die Perp-Tageskerzen werden vor dem Rechenlauf über eine Erweiterung von `nachladen_historie.py` geladen, mit demselben fail-closed-Schreibpfad und Prüfsummen. Das Nachladen ist Datenbeschaffung, kein Rechenlauf, und verändert keine Definition in diesem Dokument. Kraken-Funding bleibt Gegenprobe im Überlappungsjahr.

**Regeln.** Alle Daten sind archivierte Originalwerte mit Zeitstempel, keine Rekonstruktionen. Ein Datensatz wird nur verwendet, wenn er die Integritätsprüfung aus `nachladen_historie.py` besteht. Funding-Zeitstempel sind die tatsächlichen Zahlungszeitpunkte. Für Tage vor Beginn einer Funding-Reihe wird bei Familien A bis C **kein** Funding angesetzt, und der Bericht weist den Anteil der Handelstage ohne Funding-Daten je Coin aus. Für Familie D beginnt jede Reihe erst mit dem ersten Funding-Datum.

**Umgang mit fehlenden Daten.** Fehlt eine Kerze, bleibt die Position unverändert, es gibt kein Signal und keinen Handel an diesem Tag. Fehlt eine Reihe ganz, wird der Coin für die betroffene Familie ausgeschlossen und das dokumentiert. Nichts wird interpoliert.

**Kein Look-ahead.** Die Umsetzung übernimmt die Struktur von `stage1.py`. Vor dem Bericht wird derselbe Abschneide-Test wie in Stufe 1 gefahren: Signale und Fills auf einer am 30.06.2023 abgeschnittenen Historie müssen mit dem Volllauf identisch sein.

---

## 15. Coin Universe

Dasselbe Universum wie Stufe 1: BTC, ETH, SOL, XRP, ADA, AVAX, LINK, DOT, BNB, LTC. Kern sind BTC und ETH. Jeder Coin läuft ab seinem ersten definierten Bar nach Warmup.

**Survivorship-Vermerk, ausdrücklich.** Diese zehn Coins wurden im September 2026 nach heutiger Bekanntheit und Liquidität ausgewählt. Alle zehn haben überlebt. Das Universum ist damit rückwirkend verzerrt, am stärksten für Cross-Sectional-Varianten (XS21), bei denen die Auswahl unter Gewinnern stattfindet, und für Long-only-Varianten, bei denen Buy-and-Hold der Überlebenden eine zu hohe Latte ist. Für Time-Series-Varianten je Coin ist die Verzerrung geringer, aber vorhanden. Ein Point-in-Time-Universum mit delisteten Coins ist für eine spätere Stufe vorgesehen. Jede Kennzahl im Bericht trägt diesen Vermerk, XS-Kennzahlen zusätzlich hervorgehoben.

**Eignung je Coin und Familie.** Ein Coin geht in die Auswertung ein, wenn er nach Warmup mindestens 750 Bars und in der betreffenden Variante mindestens 20 abgeschlossene Trades liefert. Andernfalls wird er berichtet, zählt aber nicht für die Mehrheitskriterien.

---

## 16. Zeitblöcke

Drei feste, nicht überlappende Kalenderblöcke, vor dem Lauf gesetzt:

| Block | Zeitraum | Inhalt |
|---|---|---|
| P1 | 2017-08-17 bis 2020-12-31 | Baisse 2018, Erholung 2019, 2020 |
| P2 | 2021-01-01 bis 2023-12-31 | Hausse 2021, Baisse 2022, Erholung 2023 |
| P3 | 2024-01-01 bis 2026-09-14 | ETF-Ära, gesunkene Volatilität |

Ein Block zählt für einen Coin nur, wenn er mindestens 250 definierte Bars und mindestens 5 abgeschlossene Trades enthält. Zusätzlich werden Kalenderjahre berichtet.

**Walk-forward und rollende Fenster entfallen.** Es gibt keine In-Sample-Anpassung, alle Parameter sind vorab fixiert. Die Zeitblöcke und der Jitter leisten, was Walk-forward bei optimierten Systemen leisten muss. Rollende 12-Monats-Renditen werden berichtet (Worst Rolling 12 Months), sind aber kein Kriterium.

---

## 17. Robustheits- und Jitter-Tests

**Jitter.** Wie in den Abschnitten 6 bis 8 je Variante festgelegt. Jeder Nachbar wird vollständig gerechnet und in `stage2_config_log.csv` eingetragen. Bewertet wird die **Region**, nicht der Bestwert: Eine Variante ist parameterrobust, wenn mindestens zwei Drittel ihrer Nachbarn unter K1 eine positive gepoolte Erwartung je Trade haben **und** die Sharpe Ratio der Basisvariante nicht mehr als 50 Prozent über dem Median der Nachbarn liegt. Ein isolierter Gipfel ist ein Warnsignal und wird als «nicht robust» gewertet.

**Coins.** BTC und ETH müssen bestehen, dazu die Mehrheit der übrigen geeigneten Coins.

**Zeitblöcke.** Gepoolte Erwartung je Trade unter K1 positiv in mindestens zwei der drei Blöcke.

**Trades, gestuft nach Konstruktion.** Die Mindestzahl richtet sich nach der Signalfrequenz, die sich aus der Definition ergibt, nicht aus gerechneten Ergebnissen. Die Zuordnung ist vollständig und wird nicht verändert.

| Klasse | Zuordnung nach Konstruktion | gepoolt | je Kerncoin |
|---|---|---|---|
| S schnell | Signalprüfung täglich oder an festen Stichtagen ohne Ausbruchsfilter: MR, TS21, TS63, TS126, XS21, D-FC, D-OI | ≥ 100 | ≥ 30 |
| M mittel | Ausbruch N ≤ 55 mit Stopp: W1, W2, W5, W6, W8 und ihre Short- und Long+Short-Varianten | ≥ 60 | ≥ 15 |
| L langsam | Ausbruch N ≥ 100, Kreuzung SMA200, Carry-Schalter: W0, W3, W4, W7, W4S, D-CC | ≥ 30 | ≥ 8 |

Die Trade-Mindestzahl ist ein eigenständiges Evidenzkriterium und wird durch kein anderes Verfahren ersetzt. Der Block-Bootstrap auf täglichen Renditen (unten) prüft die statistische Signifikanz der Renditereihe, aber tägliche Renditen innerhalb eines Trades sind wirtschaftlich nicht unabhängig: Ein System mit zwölf Trades in neun Jahren liefert über 3000 Tagesrenditen, davon stammen jedoch alle aus zwölf Entscheidungen. Der Bootstrap kann deshalb signifikant ausfallen, obwohl die Zahl unabhängiger Entscheidungen für ein Urteil nicht ausreicht. Beide Kriterien müssen unabhängig voneinander erfüllt sein, und bei Systemen der Klasse L wiegt die Trade-Zahl schwerer als der Bootstrap. Eine Variante der Klasse L, die besteht, erhält den Vermerk **«bestanden mit geringer Trade-Basis»** und gilt erst nach Bestätigung im Paper-Betrieb (Phase P6 des Architekturdokuments) als belastbar. Für Familie C zählt jede Positionsänderung mit anschliessender Halteperiode als Trade.

**Bootstrap.** Stationärer Block-Bootstrap auf den täglichen Strategie-Überrenditen gegenüber Cash, mittlere Blocklänge 20 Bars, 2000 Wiederholungen. Berichtet wird das 5-Prozent-Perzentil der annualisierten Überrendite und ein einseitiger p-Wert für Sharpe grösser null. Der Bootstrap beurteilt die Renditereihe, nicht die Zahl der Entscheidungen. Er ersetzt die gestuften Trade-Schwellen nicht, siehe oben. Zusätzlich wird für jede Variante ein Trade-Bootstrap berichtet (Ziehen mit Zurücklegen aus den abgeschlossenen Trades, 2000 Wiederholungen, 5-Prozent-Perzentil der mittleren Erwartung je Trade), der die Unsicherheit auf Ebene der Entscheidungen zeigt. Er ist Bericht, kein Kriterium, weil bei Klasse L die Stichprobe dafür zu klein ist.

**Ausreisser.** Ergebnis ohne die drei besten Trades und ohne die beste Woche, gepoolt. Kein Kriterium, immer berichtet.

---

## 18. Erfolgs- und Scheiterkriterien

Je Variante und Seite, gepoolt über die geeigneten Coins, im Szenario K1.

| Nr | Kriterium | Schwelle |
|---|---|---|
| 1 | Positive Erwartung nach Kosten | Erwartung je Trade > 0 und CAGR > Cash, auf BTC, ETH und der Mehrheit der geeigneten Coins |
| 2 | Coin-Robustheit | wie 1, ausgewiesen als Anteil bestandener Coins |
| 3 | Zeitblöcke | Erwartung je Trade > 0 in ≥ 2 von 3 Blöcken |
| 4 | Jitter | ≥ 2/3 der Nachbarn mit Erwartung > 0, Basis-Sharpe ≤ 1.5 × Median der Nachbarn |
| 5 | Trades | Klasse S ≥ 100 gepoolt und ≥ 30 je Kerncoin, Klasse M ≥ 60 und ≥ 15, Klasse L ≥ 30 und ≥ 8 (Abschnitt 17) |
| 6 | Drawdown und Tail | MaxDD ≤ MaxDD der exposure-gleichen Passivposition, Worst Rolling 12 Months berichtet |
| 7 | Beta-Trennung | mindestens einer der Teiltests 13.3a Alpha oder 13.3b Risikotransformation bestanden, Kennzeichnung im Urteil |
| 8 | Statistik | Bootstrap-5-Prozent-Perzentil > 0 und Holm-korrigierter Bootstrap-p-Wert < 0.05 innerhalb der Familie (Abschnitt 19), Deflated Sharpe Ratio als Sensitivität berichtet |

**BESTANDEN**: alle acht Kriterien erfüllt. Das Urteil trägt die Beta-Kennzeichnung aus 13.3 (ALPHA, RISIKOTRANSFORMATION oder BEIDES) und bei Klasse L den Vermerk zur Trade-Basis.
**TEILWEISE**: Kriterien 1, 5 und 8 erfüllt, aber mindestens eines von 3, 4, 6, 7 verfehlt. Wird nicht als Edge gewertet, aber mit Begründung berichtet.
**VERWORFEN**: alles andere.

Zusätzliche Kennzeichnung **ROBUST GEGEN STRESS**, wenn Kriterium 1 auch unter K2 erfüllt ist.

Die absolute Rendite ist kein Kriterium. Unter bestandenen Varianten wird nicht nach CAGR gereiht. Der Bericht listet bestandene Varianten in der Reihenfolge Calmar, dann Sharpe, dann Return je Einheit Exposure, und sagt das ausdrücklich.

**Stufen-Ergebnis.** Eine Familie «hat einen Edge», wenn mindestens eine Variante BESTANDEN ist. Besteht in keiner Familie eine Variante, ist die Nullhypothese nicht widerlegt, und der Abbruchpunkt aus dem Architekturdokument (zwischen P3 und P4) ist erreicht.

**H0-A8 und H0-A6** werden getrennt beantwortet, durch direkten Vergleich W2 gegen W8 und W6/W7 gegen W2/W4 in Sharpe, Calmar, Erwartung je Trade und Baissejahren, mit Bootstrap-Konfidenzintervall der Differenz.

---

## 19. Umgang mit Multiple Testing

Zahl der primären Tests, vorab gezählt:

| Familie | Primäre Varianten mal Seiten | N |
|---|---|---|
| A | W0 bis W8 long-only (9), W2S W4S W8S (3), Long+Short W2 W4 W8 (3) | 15 |
| B | MR-L, MR-S, MR-LS | 3 |
| C | TS21, TS63, TS126 mal 3 Seiten (9), XS21 mal 3 Seiten (3) | 12 |
| D | CC marktneutral (1), FC mal 3 Seiten (3), OI mal 3 Seiten bedingt (3) | 4 bis 7 |
| **Gesamt** | | **34 bis 37** |

Jitter-Nachbarn sind Robustheitsprüfungen und zählen nicht als eigene Tests, weil sie nicht zur Auswahl herangezogen werden.

**Zwei Verfahren, zwei Fehlerquellen.** Die Holm-Korrektur kontrolliert die familienweise Fehlerrate: Wer N Tests rechnet, findet auch ohne Edge mit wachsender Wahrscheinlichkeit einen scheinbar signifikanten. Sie arbeitet auf p-Werten und lässt offen, woher diese stammen. Die Deflated Sharpe Ratio korrigiert die Sharpe-Schätzung eines einzelnen Ergebnisses um zwei Dinge zugleich: erstens um die Zahl der Versuche (die erwartete Höhe des besten Ergebnisses unter der Nullhypothese steigt mit N) und zweitens um Nicht-Normalität und Stichprobenlänge (Schiefe und Kurtosis der Renditen machen die Sharpe-Schätzung unsicherer). Der erste Teil überschneidet sich mit Holm. Beide Verfahren zusammen als Pflicht anzuwenden, würde die Multiplizität doppelt bestrafen.

**Primärverfahren.** Holm-Korrektur der einseitigen Block-Bootstrap-p-Werte für Sharpe grösser null, innerhalb jeder Familie, Niveau 5 Prozent. Der Block-Bootstrap erzeugt die p-Werte nicht-parametrisch aus den tatsächlichen Renditen und trägt Schiefe, Kurtosis und Autokorrelation damit bereits in sich. Holm behandelt danach die Multiplizität genau einmal.

**Sensitivitätsanalyse.** Deflated Sharpe Ratio nach Bailey und López de Prado mit N gleich der Zahl der primären Tests der Familie, zusätzlich mit N inklusive aller Jitter. Sie wird für jede Variante berichtet, ist aber kein Bestehenskriterium. Weicht ihr Urteil vom Primärverfahren ab, wird das im Bericht ausgewiesen und diskutiert.

Kein Ergebnis wird als Edge bezeichnet, das nur vor Korrektur signifikant ist.

---

## 20. Reporting-Schema

Ausgaben unter `01_forschung/02_strategien/`:

- `stage2_results.json` — alle Rohergebnisse mit Prüfsummen der Eingaben, Datum, Version dieser Vorregistrierung
- `stage2_config_log.csv` — jede gerechnete Konfiguration inklusive Jitter, Seite, Kostenszenario, Coin
- `stage2_trades/{variante}_{coin}_{seite}.csv` — jeder Trade mit Einstieg, Ausstieg, Grund, Notional, Kosten, Funding, Ergebnis
- `stage2_report.md` — je Familie eine Tabelle mit allen unten aufgeführten Kennzahlen je Variante, Seite, Coin und Szenario, dazu Blocktabellen, Jitter-Tabellen, Beta-Trennung, Kriterienmatrix mit Urteil
- `stage2_summary.md` — Klartext, auch bei «kein Edge»
- `stage2_mtp_fingerprint.md` — Abschnitt 21, getrennt
- `stage2_hypotheses_v2.md` — alles, was auffiel und nicht vorregistriert war
- `stage2.py`, `report2.py` — reproduzierbar

**Kennzahlen je Zelle:** CAGR, Max Drawdown, Sharpe, Sortino, Calmar, Ulcer Index, Profit Factor, Erwartung je Trade, Trefferquote, Median-Trade, mittlerer Gewinner, mittlerer Verlierer, Gain/Loss Ratio, Trade Count, durchschnittliche Exposure, Turnover, mittlere Haltedauer, Worst Year, Worst Rolling 12 Months, die fünf grössten Verluste, Anteil des Bruttogewinns aus den besten 10 Prozent der Trades, Funding-Saldo, Kostenanteil am Bruttoergebnis.

**Drei Grössen, nie vermischt:** Signalmodell ohne Kosten (K0), realistisch (K1), Stress (K2). Jede Tabelle trägt das Szenario in der Überschrift.

---

## 21. MTP-Fingerprint, getrennte Analyse

Nach Abschluss der Edge-Bewertung und ohne Rückwirkung auf sie: Welche Variante aus W0 bis W8 ähnelt dem öffentlich beschriebenen Market Trend Pro strukturell am ehesten?

Öffentliche Merkmale, als Bänder vorab gesetzt:

**R-Multiples.** Für jeden Trade `R = Ergebnis je Notional / Anfangsrisiko je Notional`, mit Anfangsrisiko gleich Abstand zwischen Einstiegs-Fill und Anfangsstopp (k · ATR14 zum Einstieg). Bei Pyramiding gilt das Anfangsrisiko der Einstiegsunit für die Gesamtposition. W0 verwendet keinen ATR-Stopp und hat deshalb kein definiertes Anfangsrisiko. Für W0 werden R-Multiples und alle daraus abgeleiteten Fingerprint-Merkmale als `n/a` ausgewiesen. Es wird kein künstliches Risiko unterstellt. Die R-basierten Merkmale gehen bei W0 weder in die Ähnlichkeitszählung ein noch in den Nenner, W0 wird auf den verbleibenden fünf Merkmalen beurteilt, mit Bändern «ähnlich» ab vier, «teilweise» bei zwei bis drei, «nicht» bei höchstens einem.

| Merkmal | Öffentlich genannt oder abgeleitet | Band «ähnlich» |
|---|---|---|
| Signale je Asset und Jahr | rund 8 | 4 bis 12 |
| Mittlere Haltedauer | rund 90 Tage | 45 bis 135 Tage |
| Trefferquote | relevanter Anteil Verlusttrades | 30 bis 50 Prozent |
| Median R gegen Mittel R | viele kleine Verluste, wenige grosse Gewinner | Median R ≤ 0.5 **und** Mittel R > Median R |
| Obere R-Perzentile | Gewinner sollen laufen | 90. Perzentil von R ≥ 3.0 |
| Schiefe der R-Verteilung | positiv schief | Schiefe > 1.0 |
| Gewinnkonzentration Top 10 Prozent | Edge aus grossen Gewinnern | Beste 10 Prozent der Trades liefern ≥ 50 Prozent des Bruttogewinns |
| Gewinnkonzentration Top 5 Trades | wenige Ausreisser tragen das Ergebnis | Beste 5 Trades liefern ≥ 30 Prozent des Bruttogewinns je Coin |
| Baisseverhalten | Cash in negativen Phasen | Exposure in Baissejahren ≤ 25 Prozent |

Berichtet werden je Variante zusätzlich die vollständige R-Verteilung (Perzentile 5, 25, 50, 75, 90, 95), Mittel und Median R getrennt für Gewinner und Verlierer sowie der Anteil der Trades mit R ≤ −1.

**Anmerkungen zu einzelnen Merkmalen, ohne Änderung der Bänder.** Die Signalhäufigkeit ist öffentlich uneinheitlich, eine Darstellung nennt rund 8 je Asset und Jahr, eine andere 1 bis 3 je Monat, vermutlich verschiedene Zählweisen oder Versionen. Das Merkmal gilt deshalb als **unsicherer Fingerprint**, das Band bleibt bestehen, der Bericht weist beide Lesarten aus. Die Haltedauer von rund 90 Tagen ist ein Mittelwert, Gewinner können deutlich länger laufen, weshalb zusätzlich die Haltedauer der Gewinner getrennt berichtet wird. Ein fixes Gewinnziel ist für Woo Legacy klar verneint, für MTP 2.4 öffentlich widersprüchlich. Die Matrix verwendet in keiner Variante ein Gewinnziel und behandelt dessen Fehlen nicht als gesicherte MTP-2.4-Regel. Die Short-Varianten W2S, W4S, W8S sind Aurum-Erweiterungen und werden im Fingerprint nicht gegen MTP gemessen.

Bewertung: sieben bis neun von neun Merkmalen im Band heisst «strukturell ähnlich», vier bis sechs «teilweise ähnlich», höchstens drei «nicht ähnlich». Gemessen wird auf BTC und ETH, Long-only, Szenario K1. Ergebnis ist eine Zuordnung, keine Performance-Aussage. Wir stellen nicht fest, Woos Code gefunden zu haben. Das Fingerprint-Ergebnis ist von der Edge-Bewertung getrennt und beeinflusst sie nicht.

---

## 22. Nicht Teil von Stufe 2, vorgemerkt

- **Kontinuierliches Exposure-Gating** über Abstand zum gleitenden Durchschnitt oder Volatilitätsperzentil. Stufe 1 hat diese Grössen als robust gezeigt. Sie werden erst in einer späteren Stufe auf bestandene Strategien angewandt, nie auf verworfene.
- Diskrete Regime aus Stufe 1, in jeder Form.
- Risikobasiertes Sizing, Volatilitätsskalierung, Portfoliokonstruktion über Coins.
- Point-in-Time-Universum mit delisteten Coins.
- Intraday-Signale.

---

## 23. Freeze-Protokoll

Eingefroren werden mit Freigabe dieses Dokuments: Strategiedefinitionen, Parameter, Jitter-Nachbarn, Kostenszenarien, Funding-Behandlung, Coin-Universum, Datenquellen, Zeitblöcke, Mindestzahl Trades, Robustheitskriterien, Bestehens- und Scheiterkriterien, Beta-Trennung, Long/Short-Auswertung, Umgang mit fehlenden Daten, Zahl der Tests für die Korrektur, Fingerprint-Bänder.

Ablauf: Freigabe der offenen Entscheidungen, Status im Kopf auf EINGEFROREN, SHA-256 des Dokuments und der Eingabedaten in `00_doku/ENTSCHEIDE.md`, dann erst Umsetzung und Rechenlauf. Look-ahead-Test vor dem Bericht. Jede Abweichung nach dem Einfrieren erzeugt Version 2 und macht Ergebnisse von Version 1 nicht ungültig, aber getrennt.

Wird ein Effekt entdeckt, der hier nicht steht, geht er in `stage2_hypotheses_v2.md`. Nicht in den laufenden Test.

---

## Entscheidungen vor dem Einfrieren, getroffen am 15.09.2026

Alle früher offenen Punkte sind entschieden und in den jeweiligen Abschnitten verankert. Es gibt keine offenen Punkte mehr.

| Nr | Punkt | Entscheid | Verankert in |
|---|---|---|---|
| 1 | Funding-Datenquelle | Binance-Archiv wird vor dem Lauf geladen, Kraken als Gegenprobe | Abschnitt 14 |
| 2 | Pyramiding-Obergrenze | Einstieg 0.50, Add-ons 0.25 und 0.25, Maximum 1.00, kein Hebel | Abschnitt 10 |
| 3 | Mindestzahl Trades | gestuft nach Konstruktion, Klassen S, M, L, eigenständiges Kriterium | Abschnitt 17 |
| 4 | Risikobasiertes Sizing als Zweitlauf | **nein**, nicht in Version 1 | Abschnitt 10 und 22 |
| 5 | Short-Spiegelungen in Familie A | **nur W2, W4, W8** | Abschnitt 6 |
| 6 | XS21 trotz Survivorship | **ja**, jede XS-Kennzahl klar gekennzeichnet | Abschnitt 8 und 15 |
| 7 | D-OI | **ja, bedingt**, mit exakten Datenanforderungen und Fail-closed-Regeln | Abschnitt 9 |
| 8 | W0 und R-Multiples | R-Multiples bei W0 als `n/a`, kein künstliches Risiko | Abschnitt 21 |
| 9 | Bootstrap und Trade-Zahl | Bootstrap ersetzt die Trade-Schwellen nicht, beide unabhängig zu erfüllen | Abschnitt 17 |

---

*Dieses Dokument ist eine Vorregistrierung. Sein Wert liegt darin, dass Definitionen, Kosten und Kriterien feststehen, bevor ein einziger Backtest gesehen wurde.*
