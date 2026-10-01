# RTC — Reversal-to-Trend Capture, Framework Version 0.1

**Project Aurum II, gemeinsame Strategiefamilie für die Stränge 04_xrp_specialist, 05_dot_specialist und 06_btc_specialist (`01_forschung/00_gemeinsam/`). 17.09.2026, integriert das Final Addendum und das Asian Price-Action Addendum v2 vom selben Tag. Status: Framework zur Prüfung. Kein Rechenlauf, kein Freeze. Alle Freeze-Urteile der Stufen 1, 2 und der MTP-Validierung bleiben unangetastet. Setzt die Candlestick and Flow Feature Library v0.1 voraus. Die drei Coin-Pläne referenzieren dieses Dokument und halten nur coin-spezifische Abweichungen fest.**

## 0. Zweck und ökonomische Hypothese

Aurum II soll starke Übertreibungen nach unten erkennen, nach bestätigter Bodenbildung möglichst günstig einsteigen, einen daraus entstehenden Trend möglichst vollständig halten und erst bei belastbarer Evidenz für Trendbruch oder Peak aussteigen. Die Kette, die dieses Framework prüft, lautet auf der Kaufseite: Liquidity Sweep oder Failed Breakdown, starke Rejection, Volumen und Flow, Bestätigung, Trend halten. Auf der Verkaufsseite: neues Hoch oder Failed Breakout, Upper-Wick-Rejection, Volumen- oder Kaufklimax, Strukturbruch, Exit.

Die ökonomische Hypothese hat drei prüfbare Teile. Erstens: Nach einem Selloff mit volatilitätsnormalisierter Überdehnung an einem definierten Niveau und mit bestätigter Rejection ist die Verteilung der Folgerenditen rechtsschief, weil erzwungene Verkäufer (Stops unter dem Niveau, Liquidationen, Margin-Abbau) den Preis unter das Niveau gedrückt haben, das freiwillige Käufer akzeptieren. Zweitens: Ein Teil dieser Umkehrungen ist der Anfang eines mehrwöchigen Trends, und der Ertrag der Familie liegt in diesem Teil, nicht in der kurzfristigen Rückkehr zum Mittelwert. Drittens: Der Trend endet mit erkennbarer, aber nicht exakt terminierbarer Evidenz (Käufer erschöpfen sich, Struktur bricht, Positionierung überfüllt), die einen früheren Ausstieg als ein rein mechanischer Trailing-Stop erlaubt, ohne die grossen Gewinner abzuschneiden.

Kein Teil des Frameworks behauptet, das echte Tief oder Hoch in Echtzeit zu kennen. Alle Signale sind bestätigte Proxies mit Verzögerung, und die Verzögerung ist der Preis der Bestätigung. Candle-Muster tragen in Krypto über Stunden Information in Basispunkten (Moser und Brauneis 2026, Feature Library Abschnitt 0), nicht in handelbaren Prozenten. RTC nutzt Kerzengeometrie und Muster deshalb nur als Bestätigung des Einstiegs und als Evidenz beim Ausstieg, die Erwartung muss aus dem Halten kommen. Die Konstruktion, die nach demselben Signal am Mittelwert aussteigt, ist die Kontrollarchitektur (Abschnitt 7), nicht die Hypothese.

## 1. Methodische Regel für diese und alle folgenden Familien

Frühere negative Ergebnisse gelten ausschliesslich für die konkret getestete Kombination aus Marktmechanik, Zeitebene, Signal, Exit und Instrument. Eine schwache tägliche Mean Reversion auf XRP (Stufe 2) widerlegt keine 4h-Reversal-Hypothese mit Trend-Hold. Gescheiterte tägliche Trendfolge auf DOT (Stufe 2, MTP-Validierung) widerlegt keinen 4h-Kompressionsausbruch mit Perp-Bestätigung. Ein negativer Test beendet die eingefrorene Hypothese, nicht den Coin. Verboten bleibt die Kette «negativer Test, Parameter ändern, erneut testen, bis positiv». Zulässig ist «neuer ökonomischer Mechanismus, neue Vorregistrierung, neuer Test». Die Formulierung «keine Version 2» in den Plänen v0.1 und im Architektur-Update v1 wird ersetzt durch: Eine Version 2 derselben Hypothese ist nur nach bestandener Version 1 zulässig, eine neue Hypothese auf demselben Coin ist jederzeit zulässig, sie weist ihre Vorbelastung offen aus und führt sie in der Trial-Zahl der Deflated Sharpe Ratio. Frühere Tests sind Dokumentation, kein Veto.

Die zusätzlichen Ideen der Addenda erweitern die Discovery, nicht den zulässigen Parameterraum. Für jede Hypothese gilt: wenige vorab fixierte Varianten, keine Gewinnerwahl aus Dutzenden Lookbacks, kein Parameterersatz nach P&L, Ergebnis einfrieren, neue Vorregistrierung nur bei wirklich neuer Marktmechanik.

## 2. Discovery Stage und Validation Stage

**Discovery Stage.** Datenfenster: Beginn der Daten bis 31.12.2023 (Blöcke P1 bis 2020, P2 2021 bis 2023). Zweck: feststellen, ob ein Signal existiert. Erlaubt sind die vorab fixierten Varianten dieses Dokuments (zwei Bottom-Familien, drei Trigger, die Ebenen RTC-0 bis RTC-3, die Exits E0, E1, E2, die Zeitebenen 4h und 8h, die 1h-Bestätigung). Alle Definitionen und Zahlen werden vor dem ersten Lauf eingefroren, der Lauf ist einmalig, das Ergebnis wird nach vorregistrierten Discovery-Kriterien beurteilt. Ein Discovery-Ergebnis erlaubt keine Produktionsfreigabe. Ein negatives Discovery-Ergebnis schliesst die getestete Familie auf diesem Coin, nicht den Coin. Nach der Discovery dürfen Hypothesen für die Validation formuliert werden, aber nur aus Discovery-Daten und nur vor jedem Blick auf das Holdout.

**Validation Stage.** Datenfenster: 01.01.2024 bis Datenende (rund 2.7 Jahre auf 4h, rund 5900 Kerzen je Coin), dazu Venue-Wechsel (Ausführung auf Kraken-Kerzen, Ebene B) und Kostenstress (K2). Mechanik, Parameter, Trigger, Ebene und Musterteilmengen sind aus der Discovery eingefroren, die Validation ist ein einziger Lauf. Erst die Validation entscheidet über einen Sleeve, mit den strengen Kriterien (Abschnitt 13) und voller Multiplizitätskontrolle.

Ehrliche Einschränkung des Holdouts: Die Daten ab 2024 sind für die hier definierten Mechaniken unberührt (keine 4h-Kerze, kein Taker-Merkmal, kein Candle-Flag wurde je berechnet), aber sie sind als Marktverlauf bekannt. Stufe 2 und die MTP-Validierung haben Tageskerzen bis 2026 verwendet, und der Verfasser weiss, dass XRP im November 2024 stark gestiegen ist und DOT nicht. Das Holdout ist deshalb kein unbekanntes Fenster, sondern ein für diese Mechanik ungenutztes Fenster. Vorkehrung: Die Discovery-Läufe rechnen auf einer physisch abgeschnittenen Datenkopie (Prüfsumme der abgeschnittenen Dateien in ENTSCHEIDE), die Validation-Mechanik wird vor dem ersten Zugriff auf das Holdout mit Prüfsumme eingefroren, nach der Validation gibt es keine Revision. Ein Forward-Fenster ab dem Freeze-Datum ist die einzige Ebene ohne diese Einschränkung und wird für jeden Sleeve, der die Validation besteht, als dritte Stufe geführt.

## 3. Bottom Entry Engine (Modul A)

Alle Bedingungen werden am Schluss der Kerze t bewertet, auf der Signalquelle (Binance Spot Klines, 4h primär). Reversal-Kandidat und Trade-Einstieg sind getrennt (Abschnitt 4).

**Kontext (Location), alle drei Bedingungen, für beide Familien:**

K1, Selloff: `dd120_t` ≤ −0.12, der Schluss liegt mindestens 12 Prozent unter dem höchsten Hoch der letzten 120 Kerzen (20 Tage).
K2, Überdehnung: `ext` ≤ −2.0 auf mindestens einer der Kerzen t−5 bis t (innerhalb des letzten Tages mindestens 2 ATR unter dem EMA50).
K3, Niveau: `dist_support_atr_t` ≤ 1.0 oder `at_low_structure_t` = 1, der Preis handelt innerhalb einer ATR eines deterministischen Support-Niveaus (Swing Low, 120-Kerzen-Tief oder mehrfach getestete Zone, Feature Library Abschnitt 5) oder an der lokalen Low-Struktur. Eine identische Kerze mitten in einer Range ohne K1 bis K3 ist kein Kandidat. Der Kontext ist zwingend, nicht gewichtet.

**Familie CR, Candle Reversal (RTC-CR):** `bull_any_t` = 1, also mindestens eines der fünf bullish Muster (Bullish Harami, Bullish Hikkake, Hammer, Bullish Engulfing, Morning Star) ist mit Kerze t vollständig. Zusätzlich als stetige Beschreibung jedes Kandidaten: `lower_wick_atr`, `close_location`, `volume_zscore`, `lw_x_vol`, `taker_imbalance`, `ti_delta6`.

**Familie FB, Failed Breakdown / Liquidity Sweep Bottom (RTC-FB), priorisiert:** `failed_breakdown_t` = 1 auf einem der drei Niveaus: Die Kerze t handelte unter dem Niveau (mindestens 0.1 Prozent), schloss wieder darüber, mit relevanter Lower-Wick-Rejection (`lower_wick_atr` ≥ 0.5 und LW ≥ 1.5 · B). Kein Muster-Flag verlangt. Volumen und Flow (`volume_zscore`, `taker_imbalance`, `ti_delta6`, `sweep_depth_atr`) werden je Kandidat dokumentiert und in RTC-1 verlangt. Kandidaten, die beide Familien erfüllen, zählen zu FB und werden als Schnittmenge berichtet. FB ist keine Variation einer Mean Reversion, sondern eine Preis-Niveau-Hypothese: Stops unter dem Niveau wurden abgeholt, und die Verkäufer konnten den Preis nicht dort halten.

**Inkrementelle Ebenen, streng verschachtelt, für beide Familien:**

| Ebene | Zusätzliche Bedingung zur vorigen Ebene | Datenklasse | Verfügbar ab |
|---|---|---|---|
| RTC-0 | Kontext K1 bis K3 und Familienbedingung (CR oder FB) | Preis | Datenbeginn |
| RTC-1 | `volume_zscore_t` ≥ 1.0 und `taker_imbalance_t` ≥ 0 und `ti_delta6_t` ≥ +0.10 (Volumen expandiert, aggressiver Fluss ist auf die Käuferseite gedreht) | Taker Flow | Datenbeginn (Binance-Klines tragen die Spalten seit 2017) |
| RTC-2 | `funding_zscore_t` ≤ −1.0 oder `delta_open_interest_t` ≤ −0.10 (Perp-Longs kapitulieren oder werden abgebaut) | OI, Funding, Basis | Funding ab 2020, OI ab 2021-12 |
| RTC-3 | `liq_spike_long_t` = 1 (Long-Liquidationen in t oder t−1 mindestens dreimal ihr 30-Tage-Median) | Liquidationen | nur mit Quelle nach `data_upgrade_options_v1.md` |

Keine Ebene ersetzt nachträglich die vorige. Die Frage jeder Ebene ist ausschliesslich der messbare Informationsgewinn der zusätzlichen Datenklasse gegenüber der vorigen Ebene (Abschnitt 12, Tests I1 bis I3). Fehlt ein Merkmal an einer Kerze (fail-closed), ist die Kerze für diese und alle höheren Ebenen «nicht auswertbar» und zählt nur zu den tieferen Ebenen. Höhere Ebenen werden auf dem gemeinsamen Fenster mit der jeweils tieferen Ebene verglichen.

**Initialer Stop:** min(L über t−2 bis t) − 0.5 · ATR14_t, bei FB zusätzlich nie über dem Sweep-Tief. Liegt der Stop mehr als 3 ATR14 unter dem Einstieg, wird kein Trade eröffnet. R = Einstieg − Stop. Sizing wie in allen Stufen, Sicht 1: Notional so, dass der initiale Stop 2 Prozent des Sleeve-Startkapitals riskiert, kein Compounding, Notional-Obergrenze 100 Prozent. Eine Position je Coin, keine Add-ons, nach einem Exit ist ein neuer Einstieg ab der nächsten Kandidatenkerze zulässig.

**Short-Spiegel (Top Entry, tertiär):** Kontext `ru120` ≥ +0.12, `ext` ≥ +2.0, `dist_resistance_atr` ≤ 1.0 oder `at_high_structure`, Familie CR-S mit `bear_any`, Familie FB-S mit `failed_breakout`, Flow-Ebenen spiegelbildlich. Ausführung auf Perp-Daten mit Kraken-Perp-Sätzen und Vermerk. Ein Failed Breakout ist damit primär Long-Exit-Evidenz (Abschnitt 6) und erst tertiär ein Short-Kandidat. Der Short-Spiegel ist eine eigene Familie mit eigenen Tests, nie eine Spiegelannahme.

## 4. Entry Trigger: Reversal-Kandidat ist nicht Trade-Einstieg

Die Signalkerze t liefert einen Kandidaten. Drei vorab fixierte Trigger, die nicht nach Ergebnis erweitert werden:

Trigger T0, sofort: Einstieg zur Eröffnung der Kerze t+1. Baseline, wie im Final Addendum.
Trigger TA, Preisbestätigung: Die nächste abgeschlossene Kerze t+1 schliesst über dem Hoch der Signalkerze (C_{t+1} > H_t). Einstieg zur Eröffnung der Kerze t+2. Schliesst t+1 nicht darüber, verfällt der Kandidat (kein Warten über mehrere Kerzen, damit der Trigger eine Regel bleibt und kein Fenster).
Trigger TB, Niveau-Rückeroberung (nur FB und CR-Kandidaten mit K3 über ein Niveau): C_{t+1} > Niveau L (`reclaim_confirmed`). Einstieg zur Eröffnung von t+2. Für FB-Kandidaten, deren Signalkerze bereits über L geschlossen hat, verlangt TB, dass t+1 nicht wieder unter L schliesst.

Keine Intrabar-Annahme: Mit OHLC-Daten wird ein Trigger nur am Kerzenschluss festgestellt, nie «sobald der Preis das Hoch überschreitet». Der Einstieg erfolgt zur Eröffnung der Folgekerze (Binance) beziehungsweise zum ersten handelbaren Preis nach der Kerzengrenze (Kraken, Ebene B), plus Slippage nach Kostenszenario. Der initiale Stop bleibt der der Signalkerze, R vergrössert sich bei TA und TB entsprechend, die Zahl der verfallenen Kandidaten wird berichtet.

Hypothese H3 (Abschnitt 11): Die Bestätigung verbessert die Qualität des Einstiegs mehr, als sie durch den späteren Einstieg an Trend Capture verliert. Prüfbar gepaart auf denselben Kandidaten (T0 gegen TA, T0 gegen TB), mit der Zahl der verfallenen Kandidaten als Teil des Ergebnisses (ein Trigger, der die Hälfte der grossen Gewinner verpasst, hat verloren, auch wenn die Erwartung je ausgeführtem Trade steigt).

## 5. Hold Engine (Modul H)

Ein erfolgreicher Einstieg wird nicht am Mittelwert, nicht bei RSI 50 und nicht bei einem festen Gewinnziel geschlossen. Die Position wird gehalten, solange die Price Action einen intakten Trend zeigt.

**E1, mechanische Baseline, Chandelier:** `floor_t` = max(`floor_{t−1}`, HH_seit_Einstieg_t − k · ATR14_t) mit k = 3.0, berechnet am Schluss der Kerze t, gültig für Kerze t+1. Der Floor steigt nur, nie sinkt er. Wirksamer Stop ist max(initialer Stop, `floor`). Exit intraday am Niveau als ruhende Stop-Market-Order mit Slippage. k wird nicht optimiert, Jitter k = 2.5 und 3.5 als Robustheit.

**H2, Strukturvariante (Bericht und Robustheitsvariante):** Position halten, solange `hh_hl_intact` = 1 oder noch kein neues Swing-Paar seit dem Einstieg bestätigt ist. Exit-Evidenz ist `structure_break` = 1, ausgeführt zur Eröffnung der Folgekerze, initialer Stop und Floor bleiben als harter Boden. Die Strukturmerkmale (`hh_hl_intact`, `lower_high`, `structure_break`, Schluss unter Swing Low) werden für jeden Trade und jede Kerze berichtet, auch unter E1.

Trades, deren Floor nie über den Einstieg steigt, sind Fehlsignale der Bottom-Engine und werden als eigene Gruppe berichtet.

## 6. Peak Evidence Engine (Modul P)

Kein exakter Peak-Call. Ein deterministischer Peak Evidence Score PES_t als Summe binärer Komponenten, Gewicht 1, keine Gewichtung nach Ergebnis.

| Nr | Komponente | Definition (Kerze t) | Klasse |
|---|---|---|---|
| P1 | Bearish Candle | `bear_any_t` = 1 | Candle |
| P2 | Higher High, schwacher Close | `hh20_t` = 1 und `close_location_t` ≤ 0.40 | Struktur |
| P3 | Grosse obere Wick | `upper_wick_atr_t` ≥ 1.0 und UW ≥ 2 · B | Struktur |
| P4 | Lower High nach neuem Hoch | `lower_high_t` = 1 und das vorige Swing High war ein `hh120` | Struktur |
| P5 | Structure Break | `structure_break_t` = 1 | Struktur |
| P6 | Aggressives Kaufen ohne Preisfortschritt | `taker_imbalance_t` ≥ +0.20 und `close_location_t` ≤ 0.40 | Flow |
| P7 | Preis Higher High, Flow kein Higher High | `hh20_t` = 1 und `taker_imbalance_t` < Median(`taker_imbalance`, t−20..t−1) | Flow |
| P8 | OI-Expansion bei stagnierendem Preis | `delta_open_interest_t` ≥ +0.10 und abs(`mom10_t`) < 1.0 | OI |
| P9 | Crowding | `funding_zscore_t` ≥ +2.0 | Funding |
| P10 | Momentum-Divergenz | `hh20_t` = 1 und `mom10_t` < `mom10` beim letzten vorherigen `hh20` innerhalb der letzten 30 Kerzen | Momentum |
| P11 | Short-Liquidation, Buy Climax | `liq_spike_short_t` = 1 | Liquidation |
| P12 | Price Rejection plus Volume Climax | (`hh20_t` = 1 oder H_t ≥ 0.98 · max(H, t−120..t−1)) und (`upper_wick_atr_t` ≥ 1.0 oder `close_location_t` ≤ 0.30) und `volume_zscore_t` ≥ 2.0, optional verschärft durch `price_progress_per_taker_volume_t` ≤ 0.25 (Absorption, als eigene Komponente P12b nur mit Taker-Daten) | Klimax |
| P13 | Failed Breakout, Swing Failure High | `failed_breakout_t` = 1 (Kerze handelte über Swing High oder Resistance, schloss darunter, Upper-Wick-Rejection) | Niveau |

Fehlende Komponenten (kein OI vor 2021-12, keine Liquidationen ohne Quelle) zählen null. PES wird deshalb auch als Anteil der verfügbaren Komponenten berichtet, und der Vergleich E2 gegen E1 wird auf dem Fenster geführt, in dem P1 bis P10, P12 und P13 verfügbar sind.

**E2, Chandelier als harter Boden plus Peak Evidence als früherer Exit:** Exit zur Eröffnung der Kerze t+1, wenn am Schluss der Kerze t gilt: PES_t ≥ 3 und `floor_t` ≥ Einstiegspreis. Die zweite Bedingung ist die mechanische Definition von «ein Trend hat sich etabliert»: Vor diesem Zeitpunkt gilt nur der harte Boden, weil Peak-Evidenz auf einem noch nicht bestätigten Boden die Umkehr abschneiden würde, die die Hypothese sucht. Schwelle 3 vorab, Jitter 2 und 4. Eine Variante ohne Risikofrei-Bedingung läuft als Bericht.

**Inkrementelle Peak-Evidenz (Test P-Inc):** P12 und P13 sind die Addendum-Komponenten. Ihr Informationsgewinn wird getrennt gemessen: E2 mit P1 bis P11 gegen E2 mit P1 bis P13, gepaart auf denselben Trades, Kennzahlen Giveback und Erwartung. Kein Peak-Feature wird als Short-Signal angenommen, alle sind zunächst Long-Exit-Evidenz.

Primäre Forschungsfrage der Peak Engine: Sichert E2 gegenüber E1 Gewinne früher (weniger Giveback vom maximalen Buchgewinn, gemessen als MFE minus realisiertes R je Trade), ohne die grossen Gewinner systematisch abzuschneiden (Erwartung je Trade und Summe der Top-10-Prozent-Trades nicht schlechter)? Beides gepaart auf denselben Einstiegen.

## 7. Kontrollarchitektur: Mean-Reversion-Exit

E0: identischer Einstieg, Exit zum Schluss der ersten Kerze mit C ≥ EMA20 (4h), spätestens nach 30 Kerzen, initialer Stop unverändert, kein Trailing. Das ist die klassische Mean Reversion auf denselben Signalen. Der gepaarte Vergleich E0 gegen E1 beantwortet: Ist der Wert eines bestätigten Bodens die kurzfristige Rückkehr zum Gleichgewicht oder das gelegentliche Einfangen eines grossen Trends? Erwartet unter der Hypothese: E0 mit höherer Trefferquote und kleinerem mittleren R, E1 mit niedrigerer Trefferquote, aber höherer Erwartung aus einem rechten Schwanz.

## 8. Multi-Timeframe-Kontext

Hierarchie, ohne harten Regime-Schalter: Tag als langsamer struktureller Kontext (berichtet je Kandidat: `ext` auf Tagesbasis, Lage zum Tages-Swing-Low, Tages-`er20`, keine Bedingung, keine Gewichtung in Version 0.1), 4h als primärer Setup-Timeframe, 1h als optionale Entry-Bestätigung, keine 15-Minuten-Ebene.

RTC-MTF: derselbe 4h-Kandidat mit 1h-Bestätigung statt 4h-Trigger. Trigger T1h: Innerhalb der vier 1h-Kerzen der Folgekerze t+1 schliesst eine 1h-Kerze über dem Hoch der 4h-Signalkerze (CR) beziehungsweise über dem Niveau L (FB), Einstieg zur Eröffnung der nächsten 1h-Kerze. Vergleich gepaart gegen T0 und TA: Erwartung je Trade, Einstiegspreis relativ zum Signalkerzen-Schluss, Anteil verfallener Kandidaten. Die Frage ist, ob die 1h-Bestätigung Information hinzufügt oder Trades nur verspätet beziehungsweise, gegenüber TA, vorzieht. Voraussetzung sind 1h-Kerzen, die noch nicht geladen sind.

## 9. Kerzengrenzen-Robustheit (Diagnose, nie Basis)

Feature Library Abschnitt 8a: Primäre Konvention UTC 00/04/08/12/16/20, unveränderlich. Ausschliesslich als Robustheitsdiagnose werden aus 1h-Kerzen die Aggregationen +1h und +2h gebildet, die Discovery-Läufe von RTC-CR und RTC-FB werden auf allen drei gerechnet, und berichtet werden je Coin und Familie: Pattern Overlap, Trade Overlap, Vorzeichen der Erwartung je Aggregation, qualitative Stabilität. Keine Aggregation wird ausgewählt, keine wird zur Basis, das Ergebnis geht in keine Parameterwahl ein. Ein Kandidatentyp, dessen Erwartung nur auf der UTC-Aggregation positiv ist, wird als grenzabhängig vermerkt und geht nicht in die Validation. Das ist die einzige Wirkung der Diagnose, und sie ist vorab festgelegt.

## 10. Venue-Robustheit und Cross-Venue-Bericht

Eine grosse Wick kann aus geringer Liquidität, einem einzelnen Venue oder einer Liquidationsspitze entstehen. Für jeden RTC-Kandidaten wird, soweit Daten vorhanden (Kraken 240 ab Datenbeginn, OKX-Kerzen ab Juli 2023, OKX-Funding ab März 2022), berichtet: Richtung der Rejection auf Binance, Kraken und OKX übereinstimmend (alle drei mit `lower_wick_atr` ≥ 0.5 und Schluss über dem Niveau), Swing-Niveau ähnlich (Abweichung höchstens 0.5 ATR), Close-Recovery auf mehreren Venues, Verhältnis der ATR (0.8 bis 1.25), Flow-, OI- und Funding-Richtung ähnlich. Das Signal erhält das Attribut «marktweit» oder «venue-spezifisch». Zunächst nur Bericht, kein Filter, weil ein Filter nach Venue-Übereinstimmung eine neue Regel wäre. Hypothese H4 (Cross-Venue-Übereinstimmung erhöht die Signalqualität) wird als bedingte Aufteilung der Trades geprüft, ohne Wirkung auf das Urteil.

## 11. Priorisierte Hypothesen

Drei Hypothesen mit der besten Kombination aus Plausibilität und Datenlage, je mit genau einem Test:

H1, Wick mal Volumen: Die Rejection (unten wie oben) trägt mehr Information, wenn Docht und aussergewöhnliches Volumen gemeinsam auftreten. Test: innerhalb RTC-0 (beide Familien) die Kandidaten mit `lower_wick_atr` ≥ 1.0 und `volume_zscore` ≥ 1.5 gegen die übrigen, gepaart auf dem Fenster, Erwartung je Trade und Anteil Floor über Einstieg. Spiegelbildlich für P12 als Peak-Evidenz (Test P-Inc). Keine Schwellenwahl nach Ergebnis, die Schwellen 1.0 und 1.5 sind vorab gesetzt.

H2, Failed Breakdown: Das kurzzeitige Brechen eines Niveaus mit Schluss zurück in die Range trägt mehr Reversal-Information als Kerzengeometrie allein. Test: RTC-FB gegen RTC-CR ohne FB-Schnittmenge, Erwartung je Trade, Anteil Floor über Einstieg, Capture Ratio, auf demselben Fenster, mit Trade-Bootstrap der Differenz. Spiegelbildlich P13 als Peak-Evidenz.

H3, Bestätigung: TA (und TB) gegen T0, gepaart, mit verfallenen Kandidaten als Verlust. RTC-MTF gegen TA als Zusatz, sobald 1h-Daten vorliegen.

Optional H4 (Cross-Venue, Abschnitt 10) und H5 (Visual AI, eigener Plan).

## 12. Tests, Nullhypothesen, Multiplizität (Discovery)

Je Coin, 4h, K1, Sicht 1, Trigger T0 als Baseline, sofern nicht anders genannt.

Primäre Familie (Holm über vier): T1-CR (RTC-CR-0, E1, Long gegen exposure-gleiche Passivposition), T1-FB (RTC-FB-0, E1, Long gegen Passivposition), T2 (E2 gegen E1, gepaart, auf der Vereinigung beider Familien), T3 (E0 gegen E1, gepaart).

Hypothesen-Familie (Holm über vier): H1 (Wick mal Volumen), H2 (FB gegen CR), H3a (TA gegen T0), H3b (TB gegen T0). Dazu, sobald 1h-Daten vorliegen, H3c (RTC-MTF gegen TA) als fünfter Test derselben Familie.

Inkrement-Familie (Holm über drei): I1 (RTC-1 gegen RTC-0), I2 (RTC-2 gegen RTC-1), I3 (RTC-3 gegen RTC-2, nur mit Quelle). Dazu P-Inc (E2 mit P12, P13 gegen ohne) als vierter Test.

Tertiär: Short-Spiegel T1S-CR, T1S-FB, I1S bis I3S, eigene Familie. Berichte ohne Test: H2-Variante, Jitter, 8h, Kerzengrenzen, Cross-Venue-Aufteilung (H4), Capture Efficiency (Abschnitt 14), Tageskontext-Aufteilung.

Statistik wie in den bisherigen Stufen: Trade-Bootstrap 2000 für gepaarte Differenzen, Block-Bootstrap für Equity-Kennzahlen, Holm innerhalb der Familie, Deflated Sharpe Ratio mit Trial-Zahl gleich Anzahl aller Tests dieses Frameworks auf dem Coin (12 bis 14) plus Jitter plus die dokumentierte Vorbelastung des Coins. Jitter-Nachbarn: k 2.5 und 3.5, PES-Schwelle 2 und 4, K1 0.10 und 0.15, K2 1.5 und 2.5, Stop-Puffer 0.25 und 0.75 ATR, Niveau-Fenster 90/180 und 180/360 Kerzen, je einzeln variiert. Keine Auswahl nach CAGR.

## 13. Kriterien

**Discovery, «Signal vorhanden» je Test:** Erwartung je Trade netto K1 grösser null, Bootstrap-5-Prozent-Perzentil grösser null nach Holm in der Familie, mindestens 30 Trades, Erwartung in beiden Discovery-Blöcken (P1, P2) nicht negativ, sofern der Block mindestens 10 Trades hat, kein einzelner Trade trägt mehr als 40 Prozent des Bruttogewinns, und das Vorzeichen der Erwartung bleibt auf mindestens einer der beiden verschobenen Kerzenaggregationen erhalten (Abschnitt 9). Bei 30 Trades ist die statistische Kraft gering, das wird ausgewiesen und nicht durch Lockerung umgangen. Eine Familie (CR oder FB) geht in die Validation, wenn ihr T1 «Signal vorhanden» zeigt. Die Konfiguration für die Validation folgt vorab festgelegten Regeln: E2 nur bei bestandenem T2, Trigger TA oder TB nur bei bestandenem H3a beziehungsweise H3b (bei beiden: TB für FB, TA für CR), höhere Ebene nur bei bestandenem Inkrement, sonst E1, T0, RTC-0.

**Validation, Sleeve-Entscheidung:** die neun Kriterien der Coin-Pläne auf dem Holdout, einmalig, mit eingefrorener Mechanik.

## 14. Trend Capture Efficiency (Diagnose, nie Signal)

Rein diagnostische Kennzahlen, die ex post bekannte Tiefs und Hochs verwenden und deshalb im Handelssystem nirgends vorkommen dürfen, auch nicht in Filtern, Gewichten oder Stops. Sie werden nach dem Lauf aus Trades und Kursen berechnet, in einem getrennten Modul, das keinen Zugriff auf die Signalbildung hat.

Je Trade wird das «relevante Tief» definiert als das tiefste Tief der 120 Kerzen vor dem Einstieg bis 12 Kerzen nach dem Einstieg, das «relevante Hoch» als das höchste Hoch zwischen Einstieg und 60 Kerzen nach dem Exit, die Trendspanne als Hoch minus Tief (alle Fenster vorab gesetzt, für alle Coins gleich). Dann: `entry_efficiency` = 1 − (Einstieg − Tief) / Spanne, `exit_efficiency` = 1 − (Hoch − Exit) / Spanne, `capture_ratio` = (Exit − Einstieg) / Spanne, alle auch als Verteilung über Trades, je Exit (E0, E1, E2), je Trigger (T0, TA, TB) und je Familie. Frage: Kauft RTC ausreichend früh und verkauft es ausreichend spät? Die Kennzahlen entscheiden nichts, P&L und risikoadjustierte Rendite bleiben die wirtschaftlichen Kriterien.

## 15. Zeitebenen und Datenquellen

4h primär für alle RTC-Stränge, 8h (aus 4h aggregiert, 00/08/16 UTC) als Robustheit, 1h für Trigger T1h und Kerzengrenzen-Diagnose, Tag als Kontextbericht. Signalquelle Binance Spot (Form, Volumen, Taker) und Binance Perp (Perp-Flow, Funding, OI, Basis). Ausführung Ebene B auf Kraken-240-Minuten-Kerzen mit B-Start-Regel. Cross-Venue OKX nach `data_upgrade_options_v1.md`. Fehlend für dieses Framework nach dem laufenden 4h-Lauf: 1h-Kerzen (Binance Spot und Perp 1h, Kraken 60 aus dem Archiv), OI in 4h-Auflösung (Binance-Metrics-Aggregation), Liquidationen (keine Quelle), OKX-Kerzen.

## 16. Look-ahead-Risiken

| Risiko | Vorkehrung |
|---|---|
| Swing-Bestätigung (drei Kerzen rechts) | Flags erst auf s+3 gesetzt, Look-ahead-Test der Bibliothek mit Permutation der Folgekerzen |
| Niveaus (Swing, Zone) | Stand t−1 für die Bewertung der Kerze t, ein Niveau, das erst durch Kerze t bestätigt wird, gilt ab t+1 |
| Hikkake-Bestätigung | Flag auf der Bestätigungskerze |
| Trigger TA, TB, T1h | ausschliesslich am Schluss der Bestätigungskerze festgestellt, Einstieg danach |
| Rollende Perzentile, z-Scores, Median | Fenster enden mit t−1 |
| OI-Tagesschnappschuss auf 4h-Kerzen | Wert von 00:00 gilt ab der Kerze 00:00 desselben Tages |
| Funding-Settlement | zuletzt abgerechnete Rate |
| Chandelier-Floor | aus HH und ATR bis t, gilt für t+1 |
| PES-Komponenten mit Fensterbezug | ausschliesslich bestätigte Niveaus und vergangene Fenster |
| Capture-Efficiency | getrenntes Modul ohne Zugriff auf die Signalbildung |
| Discovery gegen Holdout | physisch abgeschnittene Datenkopie mit Prüfsumme, Mechanik vor Holdout-Zugriff eingefroren |
| Kraken-240-Frühphase dünn | B-Start-Regel |
| Kenntnis des Marktverlaufs 2024 bis 2026 | prozedural (Abschnitt 2), Forward-Fenster als dritte Stufe |

Look-ahead-Test vor dem Volllauf: Kandidaten, Trigger, Stops, Floors, Scores und Niveaus auf abgeschnittener Historie (30.06.2022) identisch mit dem Volllauf bis zum Schnitt minus vier Kerzen.

## 17. Grösster Overfitting-Ort

Die Peak Evidence Engine hat dreizehn Komponenten und eine Schwelle, die Bottom Engine drei Kontextschwellen, zwei Familien, drei Trigger und ein Sammelflag über fünf Muster, dazu drei Niveaudefinitionen. Das sind mehr Freiheitsgrade als in jeder bisherigen Stufe. Vorkehrungen: gleiche Gewichte, eine Schwelle, keine Auswahl von Komponenten, Triggern oder Niveaus nach Ergebnis (die Konfigurationsregeln in Abschnitt 13 sind vorab fixiert), Musterteilmengen nur aus dem Informationswert-Test und nur für die Validation, ein Holdout, das die Discovery nie berührt, Kerzengrenzen-Diagnose, und die DSR mit der vollen Trial-Zahl. Was nicht ausgeschlossen werden kann: dass die Zahlen dieses Dokuments aus Erfahrung mit denselben Märkten stammen. Deshalb sind Änderungen bis zum Freeze frei, danach für diese Hypothese ausgeschlossen, und der Jitter zeigt, ob die Basis auf einer Spitze steht.

## 18. Offene Entscheidungen vor dem Freeze des Frameworks

1. Kontextschwellen K1 (12 Prozent), K2 (2 ATR über 6 Kerzen), K3 (1 ATR zum Niveau) bestätigen.
2. Stop-Puffer 0.5 ATR und Abbruchgrenze 3 ATR bestätigen.
3. k = 3.0 für den Chandelier bestätigen.
4. PES-Schwelle 3 und Risikofrei-Bedingung für E2 bestätigen, P12 mit Volumen-z 2.0 bestätigen.
5. RTC-1-Bedingung (Volumen-z 1.0, Taker-Imbalance nicht negativ, Flow-Wechsel 0.10) bestätigen.
6. RTC-2 als «oder»-Bedingung bestätigen.
7. Discovery-Schnitt 31.12.2023 bestätigen.
8. Trade-Mindestzahl 30 in der Discovery bestätigen.
9. Trigger TA als Ein-Kerzen-Regel (verfällt nach t+1) bestätigen, oder Fenster von zwei Kerzen.
10. FB-Familie als priorisiert (T1-FB gleichrangig mit T1-CR) bestätigen.
11. 1h-Daten laden für T1h und Kerzengrenzen-Diagnose (Empfehlung: ja, nach dem laufenden 4h-Lauf).
12. Kerzengrenzen-Bedingung im Discovery-Kriterium (Vorzeichen auf mindestens einer verschobenen Aggregation erhalten) bestätigen.
13. Capture-Efficiency-Fenster (120 vor, 12 nach Einstieg, 60 nach Exit) bestätigen.
14. Short-Spiegel tertiär, Cross-Venue nur Bericht bestätigen.

Nach Klärung: Version 1.0 des Frameworks, Prüfsumme in ENTSCHEIDE, gemeinsam mit Feature Library v1.0 und den drei Coin-Plänen v1.0 eingefroren.
