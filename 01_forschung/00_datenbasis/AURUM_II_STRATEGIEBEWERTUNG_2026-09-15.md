# Project Aurum II — Strategiebewertung und Kostenhürde

**Stand 15.09.2026. Abschluss des Bewertungsteils von Stufe 0.**

## 1. Zweck und Methode

Dieses Dokument beantwortet eine Frage: Welche Strategieklassen dürfen überhaupt in die Forschung von Aurum II, und welche werden vorher ausgeschlossen.

**Bewusst nicht gemacht** wurde eine Bewertungstabelle mit Noten von eins bis zehn über elf Dimensionen. Solche Tabellen sehen aus wie Daten und sind Meinung. Genau diese Verwechslung hat Project Aurum Geld gekostet. Stattdessen gilt für jede Klasse eine zweistufige Prüfung.

**Erste Stufe, gerechnet**: Übersteigt der in der Literatur gemessene Brutto-Edge die Handelskosten auf der tatsächlichen Gebührenstufe? Diese Prüfung ist Arithmetik und braucht keine Meinung. Wer sie nicht besteht, scheidet aus, unabhängig davon wie überzeugend die Idee ist.

**Zweite Stufe, belegt**: Gibt es für die überlebenden Klassen belastbare empirische Evidenz, und wie aktuell ist sie?

---

## 2. Die Kostenhürde, gerechnet

### 2.1 Annahmen

Gebühren nach Kraken Fee Schedule, abgerufen am 15.09.2026. Spread und Slippage mit 0.04 Prozent je Round Trip angesetzt, das entspricht der im Altprojekt gemessenen Spanne bei Majors und ist in Stufe 0 durch eigene Messung zu ersetzen. Tägliche Standardabweichung von BTC 2.20 Prozent, abgeleitet aus 42 Prozent annualisiert, dem Stand von August 2026. Krypto handelt 365 Tage.

### 2.2 Kosten je Round Trip

| Handelsplatz und Ordertyp | Gebühr zwei Seiten | Round Trip total |
|---|---|---|
| Spot Tier 1, Taker | 1.60 % | 1.64 % |
| Spot Tier 1, Maker | 0.80 % | 0.84 % |
| Spot Tier 3, Taker | 0.76 % | 0.80 % |
| Spot Tier 5, Maker | 0.30 % | 0.34 % |
| Perp Tier 1, Taker | 0.10 % | 0.14 % |
| Perp Tier 1, Maker | 0.04 % | 0.08 % |

### 2.3 Jährlicher Kostenaufwand in Prozent des Notionals

Bei durchgehender Investition und einer mittleren Haltedauer von H Tagen.

| Handelsplatz | 1 d | 3 d | 5 d | 10 d | 21 d | 55 d | 90 d |
|---|---|---|---|---|---|---|---|
| Spot T1 Taker | 599 % | 200 % | 120 % | 60 % | 28 % | 11 % | 7 % |
| Spot T1 Maker | 307 % | 102 % | 61 % | 31 % | 15 % | 6 % | 3 % |
| Spot T5 Maker | 124 % | 41 % | 25 % | 12 % | 6 % | 2 % | 1 % |
| Perp T1 Taker | 51 % | 17 % | 10 % | 5 % | 2 % | 1 % | 1 % |
| Perp T1 Maker | 29 % | 10 % | 6 % | 3 % | 1 % | 0.5 % | 0.3 % |

### 2.4 Die aussagekräftigste Zahl

Kosten je Round Trip, gemessen an der Bewegung, die im Haltezeitraum überhaupt stattfindet. Die Werte sind der Anteil einer Standardabweichung, der allein für Gebühren draufgeht.

| Handelsplatz | 1 d | 3 d | 5 d | 10 d | 21 d | 55 d | 90 d |
|---|---|---|---|---|---|---|---|
| Spot T1 Taker | 75 % | 43 % | 33 % | 24 % | 16 % | 10 % | 8 % |
| Spot T1 Maker | 38 % | 22 % | 17 % | 12 % | 8 % | 5 % | 4 % |
| Spot T5 Maker | 15 % | 9 % | 7 % | 5 % | 3 % | 2 % | 2 % |
| Perp T1 Taker | 6 % | 4 % | 3 % | 2 % | 1 % | 1 % | 1 % |
| Perp T1 Maker | 4 % | 2 % | 2 % | 1 % | 1 % | 0 % | 0 % |

Ein Tageshandel auf Spot zum Taker-Tarif muss drei Viertel einer Tagesbewegung richtig treffen, nur um die Kosten zu decken. Das ist keine Strategiefrage mehr.

### 2.5 Nettoergebnis bei volatilitätsgesteuertem Portfolio

Zielvolatilität 20 Prozent bei Assetvolatilität 42 Prozent ergibt ein Notional von 0.48 je Eigenkapital. Angenommen wird ein Bruttoergebnis von Sharpe 1.5, also 30 Prozent pro Jahr vor Kosten. Die Werte sind das **Nettoergebnis in Prozent des Eigenkapitals**.

| Handelsplatz | 1 d | 3 d | 5 d | 10 d | 21 d | 55 d | 90 d |
|---|---|---|---|---|---|---|---|
| Spot T1 Taker | −255 % | −65 % | −27 % | +1 % | +16 % | +25 % | +27 % |
| Spot T1 Maker | −116 % | −19 % | +1 % | +15 % | +23 % | +27 % | +28 % |
| Spot T5 Maker | −29 % | +10 % | +18 % | +24 % | +27 % | +29 % | +29 % |
| Perp T1 Taker | +6 % | +22 % | +25 % | +28 % | +29 % | +30 % | +30 % |
| Perp T1 Maker | +16 % | +25 % | +27 % | +29 % | +29 % | +30 % | +30 % |

Dieselbe Strategie mit demselben Signal liefert bei fünf Tagen Haltedauer auf Spot zum Taker-Tarif **minus 27 Prozent** und auf Perpetuals zum Maker-Tarif **plus 27 Prozent**. Der Unterschied ist nicht das Signal, sondern der Handelsplatz.

### 2.6 Notwendige Trefferquote

Stopp bei einer Standardabweichung des Haltezeitraums, Chance-Risiko-Verhältnis 1.5. Ohne Kosten läge die Schwelle bei 40 Prozent.

| Handelsplatz | 1 d | 3 d | 5 d | 10 d | 21 d | 55 d |
|---|---|---|---|---|---|---|
| Spot T1 Taker | 70 % | 57 % | 53 % | 49 % | 47 % | 44 % |
| Spot T1 Maker | 55 % | 49 % | 47 % | 45 % | 43 % | 42 % |
| Perp T1 Taker | 43 % | 41 % | 41 % | 41 % | 41 % | 40 % |

### 2.7 Gebührenstufe bei kleinem Konto

Die Stufe richtet sich nach dem Handelsvolumen der letzten 30 Tage. Ein aktives Konto klettert schneller als erwartet, allerdings gilt die Tabelle für vollen Kapitaleinsatz je Round Trip. Bei volatilitätsgesteuerter Grösse halbiert sich das Volumen etwa, was in der Regel eine Stufe kostet. In den ersten dreissig Tagen gilt immer Tier 1.

| Eigenkapital | 5 d Haltedauer | 10 d | 21 d | 55 d |
|---|---|---|---|---|
| 5'000 USD | T5 | T4 | T3 | T2 |
| 10'000 USD | T6 | T5 | T4 | T3 |
| 25'000 USD | T6 | T6 | T5 | T4 |
| 50'000 USD | T6 | T6 | T6 | T5 |

Auf Perpetuals bleibt jedes realistische Privatkonto auf Tier 1, weil die nächste Stufe fünf Millionen USD Monatsvolumen verlangt. Das ist unerheblich, weil Tier 1 dort bereits 0.02 und 0.05 Prozent kostet.

---

## 3. Funding, gemessen an eigenen Daten

Grundlage sind die Kraken-Funding-Reihen aus dem Ordner market_data, stündliche Werte. Die absoluten Funding-Beträge wurden durch den jeweiligen Kurs geteilt, um relative Raten zu erhalten.

| Kontrakt | Zeitraum | Mittel annualisiert | Median annualisiert | negative Stunden | 30-Tage-Fenster min bis max |
|---|---|---|---|---|---|
| PF_XBTUSD | 10.09.2025 bis 30.06.2026 | +2.69 % | +2.84 % | 32 % | −3.7 % bis +8.8 % |
| PF_ETHUSD | 10.09.2025 bis 13.09.2026 | +3.05 % | +3.06 % | 32 % | −1.9 % bis +17.2 % |
| PF_SOLUSD | 10.09.2025 bis 13.09.2026 | −0.31 % | +0.76 % | 47 % | −10.2 % bis +13.4 % |

Der BTC-Zeitraum endet früher, weil die zugehörige Kursreihe nur bis zum 30.06.2026 reicht.

**Drei Folgerungen.**

Erstens bestätigt die Messung die Literatur: Funding-Carry trägt aktuell zwei bis drei Prozent pro Jahr. Als eigenständiger Ertragsbaustein ist das weniger als eine Staatsanleihe, bei erheblich grösserem Risiko. Bei SOL war die mittlere Rate im Messzeitraum sogar negativ.

Zweitens kostet eine Long-Position über Perpetuals statt über Spot rund drei Prozent pro Jahr an Funding. Gegen die Gebührenersparnis aus Abschnitt 2.3 ist das bei jeder Haltedauer unter neunzig Tagen ein sehr gutes Geschäft.

Drittens bekommt die Short-Seite im Mittel Funding gutgeschrieben. Das ist ein kleiner struktureller Rückenwind für den Short-Teil eines symmetrischen Trendsystems und mildert einen Teil des Nachteils, gegen die langfristige Aufwärtsdrift zu handeln.

---

## 4. Evidenzstatus je Strategieklasse

| Klasse | Kostenprüfung | Evidenz | Entscheid |
|---|---|---|---|
| Time-Series-Momentum, Trendfolge | bestanden auf Perp ab 3 d | **solide**, Han, Kang und Ryu, Review of Asset Pricing Studies, 471 Coins bis Aug 2023, Netto-Sharpe 1.51 bei Lookback 7 bis 28 Tagen | **Kern von Aurum II** |
| Volatility Breakout, Donchian | wie oben | **dünn**, Hudson und Urquhart mit Daten bis 2017, eigener Out-of-Sample-Test 2018 gescheitert | als Umsetzungsvariante der Trendfolge, nicht als eigene Klasse |
| Volatilitätsskalierung | kostenneutral | **solide als Risikokontrolle**, **umstritten als Alpha**, Cederburg et al., Journal of Financial Economics: 53 Gewinne gegen 50 Verluste bei 103 Strategien | als Risikomodul, nicht als Renditemodul |
| Funding- und Basis-Carry | bestanden | Ertrag von rund 25 Prozent (Q1 2024) auf unter Treasury-Niveau gefallen, eigene Messung 2.7 bis 3.1 Prozent, Tail-Ereignis 10.10.2025 mit über 19 Mrd USD Liquidationen und Auto-Deleveraging der Delta-neutralen Teilnehmer | **nicht als Sleeve**, nur als Filter für die Haltekosten einer Perp-Position |
| Cross-Sectional Momentum | grenzwertig, Rotation bis 85 Prozent pro Woche | **weitgehend widerlegt**, Grobys et al.: nach Juli 2020 negativ und insignifikant, ein Coin verursachte minus 255 Prozent in einer Woche | nein |
| Cointegration, Pairs Trading | grenzwertig, nur auf Perp | **widersprüchlich**, funktionierende Varianten schätzen wöchentlich neu, eine Arbeit findet negative Netto-Renditen schon bei 0.08 Prozent Kosten | zurückgestellt, frühestens nach Stufe 3 |
| Kurzfrist-Mean-Reversion | **durchgefallen** | gemessener Brutto-Edge 1.3 Basispunkte gegen 5 Basispunkte Kosten, auf Kraken Spot Faktor 60 bis 120 | nein |
| Orderflow, Microstructure | **durchgefallen** | Netto-Sharpe zwischen −10.7 und −52.1 bei Retail-Gebühren | nein |
| Market Making, Avellaneda-Stoikov | **durchgefallen** | beste optimierte Variante Median-Sharpe −0.26, Kraken bietet Co-Location an, die Gegenseite nutzt sie | nein |
| Grid Trading | **durchgefallen** | Erwartungswert null unter Random Walk, formal ein Gambler's-Ruin-Problem | nein |
| Elliott Wave, Fibonacci | nicht anwendbar | Batchelor und Ramyar: 15 von 144 Ratios signifikant, also Zufallsniveau, für Krypto keine seriöse Studie | nein |

### Die grösste Lücke

Die jüngste saubere Out-of-Sample-Evidenz zu Krypto-Trendfolge endet im **August 2023**. Für die Zeit nach Einführung der Spot-ETFs existiert keine begutachtete Arbeit. Gleichzeitig ist die Volatilität von BTC auf 42 Prozent annualisiert gefallen, den engsten je gemessenen Abstand zum S&P 500. Diese Evidenz muss Aurum II selbst erzeugen. Genau dafür ist der Stufenplan da.

---

## 5. Befund zur vorhandenen Datenlage

Der Ordner market_data im Altprojekt ist deutlich besser als erwartet, hat aber eine Lücke an der entscheidenden Stelle.

**Vorhanden**: 1'544 Kraken-Tagesreihen, aktuell bis 13.09.2026. Stündliche Funding-Reihen für BTC, ETH und SOL seit 10.09.2025. Binance-Vision-Historie für sechs Symbole ab 2017 beziehungsweise ab Listing, bis 30.06.2026, mit Herkunftsnachweis und Prüfsumme. 36 Cross-Asset-Reihen, 31 Futures-Reihen, eine Referenzreihe für dreimonatige Treasury-Bills. Ein Universum-Archiv mit 40 Tagesständen seit dem 17.07.2026. Eine Qualitätsregistratur mit 1'635 Einträgen, davon 137 mit Status LIMITED und 1'498 mit Status REJECTED.

**Die Lücken.**

Erstens: **Die Kraken-Datei für Bitcoin ist leer.** XBT_USD_1d.csv enthält nur die Kopfzeile und wurde zuletzt am 17.07.2026 geschrieben, während ETH, SOL, XRP, LINK, DOT, ADA und AVAX sauber bis zum 13.09.2026 laufen. Insgesamt sind 71 der 1'544 Dateien leer, vier davon USD-Paare. Das ist exakt das Muster aus dem Findings-Digest: ein stiller Ausfall im Schreibpfad ohne Validierung und ohne Alarm, der zwei Monate unbemerkt blieb, und er traf die wichtigste Reihe überhaupt.

Zweitens: Die Kraken-Historie reicht nur zwei Jahre zurück, vom 23.09.2024 bis heute, weil die öffentliche Schnittstelle 720 Kerzen liefert. Für Stufe 1 ist das zu wenig. Die lange Historie liegt nur in den sechs Binance-Dateien und endet am 30.06.2026.

Drittens: Das Universum-Archiv enthält für alle 1'449 Symbole ein leeres Listing- und Delisting-Datum sowie den Status unbekannt. Es ist damit eine Momentaufnahme-Sammlung, kein Point-in-Time-Universum. Vorwärts gerichtet funktioniert es ab dem 17.07.2026, rückwärts nicht.

Viertens: Funding liegt nur für ein Jahr und nur für drei Kontrakte vor.

---

## 6. Konsequenzen

1. **Aurum II handelt auf Perpetuals, nicht auf Spot.** Begründung ist nicht der Hebel, sondern der Kostenfaktor von 16 bis 20. Spot bleibt Referenz für Kursdaten und für eine mögliche Basis-Betrachtung.
2. **Die mittlere Haltedauer liegt bei mindestens drei Tagen, angestrebt fünf bis zwanzig.** Alles Schnellere ist auf jeder erreichbaren Gebührenstufe ein Verlustgeschäft.
3. **Funding ist kein Ertragsbaustein, sondern eine Kostenposition.** Es gehört in den Kostenfilter vor jedem Einstieg, mit tatsächlicher Rate über die erwartete Haltedauer.
4. **Sechs Strategieklassen sind ausgeschlossen** und werden nicht mehr diskutiert: Kurzfrist-Mean-Reversion, Orderflow, Market Making, Grid, Elliott und Fibonacci, Cross-Sectional Momentum.
5. **Stufe 0 ist nicht abgeschlossen.** Die Bewertung steht, die Datenbasis nicht.

---

## 7. Quellen

Kraken Fee Schedule, abgerufen 15.09.2026, kraken.com/features/fee-schedule

Han, Kang, Ryu, Momentum in the Cryptocurrency Market, Review of Asset Pricing Studies, SSRN 4675565

Grobys, Kolari, Sandretto, Shahzad, Äijö, Cryptocurrency momentum has (not) its moments, Financial Markets and Portfolio Management, 2025

Fieberg, Liedtke, Zaremba, Cryptocurrency anomalies and economic constraints, International Review of Financial Analysis 94, 2024

Mercik, Zaremba, Demir, Crypto factor zoo, International Review of Financial Analysis 113, 2026

Cederburg, O'Doherty, Wang, Yan, On the performance of volatility-managed portfolios, Journal of Financial Economics 138, 2020

Hudson, Urquhart, Technical trading and cryptocurrencies, Annals of Operations Research, 2021

Kitron, Wengrowicz, Short-horizon mean reversion in cryptocurrency markets, arXiv 2608.21888, 2026

Chen, Chen, Jang, Dynamic Grid Trading Strategy, arXiv 2506.11921, 2025

Taranto, Khan, Gambler's ruin problem and bi-directional grid constrained trading, Investment Management and Financial Innovations 17, 2020

Batchelor, Ramyar, Magic numbers in the Dow, Cass Business School, 2006

Falces Marin, Díaz Pardo de Vera, Lopez Gonzalo, A reinforcement learning approach to improve the Avellaneda-Stoikov market-making algorithm, PLOS ONE 17, 2022

CoinDesk Research, Inside Crypto's 19 Billion Liquidation Event, 2025, sowie BitMEX Research zum Auto-Deleveraging vom 10.10.2025

Glassnode über Bitcoin Futures Basis unter Treasury-Rendite, Week 30, 2026

Eigene Messung: market_data/funding, Kraken PF_XBTUSD, PF_ETHUSD, PF_SOLUSD, ausgewertet am 15.09.2026
