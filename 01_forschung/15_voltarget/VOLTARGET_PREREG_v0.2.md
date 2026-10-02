# VOLTARGET_PREREG v0.2 – Volatilitäts-Targeting als Risiko-Overlay auf W2, W6 und Turtle 55/20 (Forward-Paper)

**Status: ENTWURF v0.2. Nicht eingefroren, nicht gestartet, kein Lauf.** Kein Tag, keine Freeze-Liste, kein Scheduler-Eintrag. Der Runner ist gesperrt (`voltarget/voltarget_config.json` enabled=false, Exit 3).
**Stand:** 2026-10-02, 11:25 Zürich (UTC+2). Branch `voltarget-v0`. Ersetzt `VOLTARGET_PREREG_v0.1.md` (bleibt unverändert als Historie liegen).
**Grundlage v0.2:** Entscheide der Projektleitung Aurum II (Aurum II Bot) vom 2026-10-02 zu den neun Fragen aus v0.1 §12 (Änderungen siehe §0a). Offen für Claude bleiben nur die drei Punkte in §12.
**Freeze erst nach:** Review Claude, kein Veto Damian, datierter ENTSCHEIDE-Eintrag, Freeze-Liste mit SHA-256 (§11).

Grundlagen:
- Ideen-Scan v1 (`01_forschung/12_ideen_scan/ideen_scan_v1.md`) §2: «GO für Vorregistrierung, aber nur als Risiko-Overlay auf den bestehenden Paper-Kandidaten. Gemessen werden soll die Risikotransformation, nicht neue Alpha.»
- Ideen-Scan v2 (`01_forschung/14_ideen_scan_v2/ideen_scan_v2.md`) §1, §2.9, §2.12: Vol-Target-Overlay bleibt GO-Kandidat aus v1.
- PAPER_PREREG v1.0 (`paper/PAPER_PREREG_v1.0.md`, eingefroren 2026-10-01 22:15): Sleeves, Ausführung, Kosten F4, Daten F6.
- `config/cost_model_v1.json` Version 1.1, Abschnitt `venue_kraken` (ENTSCHEIDE C1/C2).
- ENTSCHEIDE 2026-10-01 22:35/22:40 (Trial-Zähler rund 270; 2024–2026 kein Testfenster wegen Kontext-Vorbelastung).

Was immer gilt: keine Keys, keine Orders, keine Börsenverbindung, kein Holdout (`02_daten/holdout/` und alle Dateien mit «validation» im Namen sind im Loader gesperrt). `paper/` und alle Freeze-Dateien bleiben unverändert. Alle Zahlen sind hypothetisch (Paper).

## 0a. Änderungen gegenüber v0.1 (Changelog)

| Nr. aus v0.1 §12 | Entscheid Projektleitung 2026-10-02 | Umsetzung in v0.2 |
|---|---|---|
| 1 Relatives Ziel | angenommen, bleibt | §3.2 unverändert |
| 2 Fenster 365 Tage | angenommen (Krypto handelt täglich) | §3.3 unverändert |
| 3 G2 | Toleranz: Sharpe_VT ≥ Sharpe_Basis − 0.05 (Overlay soll Drawdowns senken, nicht Sharpe maximieren) | §7.1; `voltarget/gates.py` (`G2_SHARPE_TOL`, `g2_ok`); Tests; **offen für Claude** |
| 4 G3 | bleibt Gate (einziger Beleg für mehr als blosse Exposure-Reduktion) | §7.1 |
| 5 Schwellen 0.90 und 1 % p. a. | bleiben, ausdrücklich als gesetzt (nicht hergeleitet) deklariert | §7.1, §8.2; `gates.py`; **offen für Claude** |
| 6 Start | Overlay übernimmt bestehende Basispositionen, skaliert mit dem aktuellen s (konsistent mit Sleeves A und B) | §3.7; Engine (Grund «sync»); Tests; **offen für Claude** |
| 7 Kostenkonvention | wie PAPER F3 (Vergleichbarkeit) | §3.4; Tests (Cash negativ um genau die Kosten, Gleichheit mit `paper_engine.account`) |
| 8 Prüfbarkeit und Frist 2030 | angenommen | §8.1 unverändert |
| 9 Warmup | unter 60 Tagesrenditen s = 1; ab 60 Renditen σ_lang und σ_kurz über die verfügbare Historie (expandierend), bis 365 erreicht sind | §3.3, §3.6; Engine (`vol_state`, `scale_for`, `MIN_RETURNS = 60`); Tests. Ersetzt das STOPPED bei zu kurzer Historie; echte Lücken und ungültige Kurse führen weiterhin zu STOPPED |

Weitere Änderungen: neues Modul `voltarget/gates.py` (Sharpe, MaxDD, Kontrollfaktor c, G1–G3, Urteil, KR3); Konfiguration mit Abschnitt `gates` und Parameter `min_returns`, beide vom Runner gegen den Code geprüft (Exit 4 bei Abweichung).

## 0. Festgelegte Werte auf einen Blick

| Punkt | Festlegung | Begründung |
|---|---|---|
| Basis | W2, W6, T55_20 je 10 Coins, unverändert aus PAPER v1.0 | §1 |
| Zielvolatilität | je Coin die eigene realisierte Volatilität der letzten 365 Tage (σ_lang); Skalierung s = min(1, σ_lang / σ_kurz) | §3.2 |
| Messfenster | σ_kurz: EWMA der quadrierten Tagesrenditen, Halbwertszeit **20 Tage**, Fenster **365** Renditen | §3.3 (Harvey et al. 2018) |
| Warmup | unter **60** verfügbaren Renditen s = 1; ab 60 beide Schätzer expandierend über die verfügbare Historie bis 365 | §3.3 |
| Annualisierung | √365 (Krypto handelt 7 Tage) | §3.3 |
| Maximaler Hebel | **1.0**: s ≤ 1, Overlay-Gewicht ≤ Basis-Exposure ≤ 1.0 | §3.4 |
| No-Trade-Band | reine Vol-Anpassung nur bei \|w* − w\| > **0.10** (Anteil Sleeve-Equity); Basis-Ereignisse immer | §3.5 |
| Start | Übernahme bestehender Basispositionen, skaliert mit dem aktuellen s | §3.7 |
| Kostenkonvention | wie PAPER F3: Nominal = Gewicht × Equity vor dem Trade, Kosten zusätzlich | §3.4 |
| Kosten | K1 = `maker_plan` primär (0.47 % je Seite, Stopp-Ausstieg 0.52 %), K2 = `taker_K2` Sensitivität (1.01 % bzw. 1.16 %) | §5 |
| Vergleich | unveränderte Sleeves (Paper-Ledger) und Kontrollrechnung C mit gleicher mittlerer Exposure | §6 |
| Gates (K1) | G1 \|MaxDD_VT\| ≤ 0.90 · \|MaxDD_Basis\| (gesetzt); G2 Sharpe_VT ≥ Sharpe_Basis − 0.05; G3 \|MaxDD_VT\| ≤ \|MaxDD_C\| | §7 |
| Auswertung | frühestens nach 24 Monaten Forward (Oktober-Termin), spätestens 2030-10-01 | §8 |
| Kill | Gate verfehlt → Overlay für die Strategie geschlossen, keine Varianten; Betriebs-Kill sofort; Kosten-Kill > 1.0 % p. a. (gesetzt) | §8 |
| Testpfad | **nur** Forward-Paper ab Freeze; jeder historische Lauf ist deskriptiv | §9 |

## 1. Zweck und Abgrenzung

- **Zweck:** Prüfen, ob eine Volatilitäts-Skalierung der Positionsgrösse die Risikokennzahlen der laufenden Paper-Sleeves verbessert (kleinerer maximaler Drawdown), ohne die Sharpe-Ratio zu verschlechtern.
- **Kein neues Signal.** Das Overlay
  - ist flach, wenn die Basis flach ist;
  - steigt nur ein, wenn die Basis einsteigt (oder beim Start eine Basisposition übernimmt, §3.7);
  - verkauft vollständig, wenn die Basis aussteigt;
  - hält nie mehr als die Basis-Exposure E (W2, T55_20: 1.0 in Position; W6: 0.50 / 0.75 / 1.00).
- **Keine Alpha-Hypothese.** Harvey et al. (2018) finden eine höhere Sharpe-Ratio nur für «Risikoanlagen» (Aktien, Kredit), für Anleihen, Währungen und Rohstoffe einen vernachlässigbaren Effekt, aber über alle Anlageklassen seltenere Extremrenditen und weniger schwere Verluste im linken Rand. Für Krypto liegt aus dieser Quelle **keine** Evidenz vor [unsicher: Übertragbarkeit].
- **Basis bleibt unverändert.** Die Paper-Sleeves laufen weiter nach PAPER v1.0; das Overlay ist ein eigener Runner neben `paper/` mit eigener Ausgabe (`/workspace/aurum2/paper_voltarget/`) und eigener späterer Freeze-Liste.

## 2. Vorbelastung und Trial-Deklaration (Mehrfachtests)

- **Globaler Zähler: rund 270 informelle Trials** (ENTSCHEIDE 2026-10-01 22:35; Ideen-Scan v2 §4). Diese Vorregistrierung erbt den Zähler vollständig.
- **Direkt einschlägig:** Ideen-Scan v1 §2 hat auf Binance 1d 2018–2023 (BTC, ETH, K1, Umschichtung nur bei Abweichung > 0.1, realisierte 30-Tage-Volatilität) vier Varianten gerechnet: Buy and Hold, Vol-Target 40 %, Vol-Target 40 % + Trend 200, Vol-Target 60 % + Trend 200. Ergebnis dort: Vol-Targeting allein ungefähr gleiche Rendite, deutlich kleinerer Drawdown, Sharpe kaum besser. Diese Varianten sind Teil der rund 20 Trials von Scan v1 und damit im Zähler enthalten.
- **Überschneidung mit v0.1, offen ausgewiesen:**
  - Das No-Trade-Band 0.10 entspricht der Schwelle von Scan v1. Es wird übernommen und nicht neu gewählt, damit kein zusätzlicher Freiheitsgrad entsteht; das Ergebnis von Scan v1 ist dadurch aber bekannt.
  - **Nicht** übernommen: absolute Ziele 40 % und 60 %, 30-Tage-Fenster, Trendfilter SMA200. Die Festlegungen in §3 (relatives Ziel, EWMA 20, 365 Tage) wurden auf keinen Daten gerechnet.
  - Weder für diese Fassung noch für ihre Parameter wurde ein Overlay-Ergebnis auf irgendeinem Datensatz berechnet (auch nicht auf Kraken 2024-09 bis heute).
- **Vorbelastung der Basis:** W2/W6 sind outcome-informierte Stufe-2-Konstruktionen; die Turtle-Zahlen stammen aus dem Altprojekt (PAPER §1). BTC und ETH < 2024 sind durch Scan v1/v2 mehrfach verwendet; der grobe Marktverlauf 2024–2026 ist bekannt.
- **Diese Vorregistrierung fügt keinen Trial hinzu**, solange nur forward geprüft wird. Drei Strategien werden mit derselben Regel geprüft; die Statistik in §7.3 wird über diese drei mit Holm korrigiert.

## 3. Regel

### 3.1 Daten und Zeitkonvention
Kraken-Tageskerzen (USD, UTC-Tag), nur abgeschlossene Bars, gleiche Quelle und Ladefunktion wie PAPER F6 (`data_live/kraken_ohlc/{COIN}USD_1d.csv`). Log-Rendite r_t = ln(C_t / C_{t−1}), nur zwischen lückenlos aufeinanderfolgenden Tagen.

### 3.2 Zielvolatilität
- σ*_{c,t} = σ_lang_{c,t}: realisierte Volatilität des Coins c über die letzten 365 Tagesrenditen bis und mit Schluss t (gleichgewichtet, Mittelwert 0, annualisiert mit √365).
- Skalierung s_{c,t} = min(1, σ_lang_{c,t} / σ_kurz_{c,t}).
- **Begründung:**
  - Harvey et al. (2018) setzen das Ziel durchgehend auf 10 % p. a. und multiplizieren mit einer Konstanten k (ungefähr 1), die **ex post** so gewählt wird, dass über die ganze Stichprobe genau das Ziel realisiert wird. Das Niveau des Ziels ist dort also eine Normierung, keine Entscheidungsgrösse; massgebend ist das Verhältnis Ziel / bedingte Volatilität.
  - Ein festes Ziel von 10 % ist mit Deckel 1.0 auf Krypto nicht sinnvoll: Die Volatilität dieser Coins liegt um ein Vielfaches darüber, das Overlay wäre dauernd stark untergewichtet, ein Drawdown-Rückgang wäre rein mechanisch (weniger Exposure) und kein Effekt der Vol-Steuerung.
  - Absolute Ziele wie 40 % oder 60 % sind durch Scan v1 vorbelastet und würden die zehn Coins sehr ungleich treffen.
  - Das rollende Einjahresniveau ist die Point-in-Time-Entsprechung der Ex-post-Normierung k: kein Blick in die Zukunft, kein freier Parameter für das Niveau, pro Coin gleich definiert. Mit Deckel 1.0 reduziert das Overlay nur dann, wenn die kurzfristige Volatilität über dem eigenen Jahresniveau liegt.
  - Das Einjahresfenster als Referenzniveau ist eine eigene Festlegung (Harvey et al. verwenden die rollende Einjahresvolatilität nur als Auswertungsgrösse, Vol of Vol). Es wurde vor jeder Rechnung gewählt, nicht optimiert und von der Projektleitung am 2026-10-02 bestätigt (relatives Ziel und 365 Tage, weil Krypto täglich handelt).

### 3.3 Messfenster (bedingte Volatilität)
- σ_kurz_{c,t} = √(365 · Σ_i λ^i r²_{t−i} / Σ_i λ^i), i = 0 … 364, λ = 0.5^(1/20), d. h. Halbwertszeit 20 Tage, Mittelwert 0.
- **Begründung aus Harvey et al. (2018):**
  - Volatilität als Standardabweichung der Tagesrenditen mit exponentiell abnehmenden Gewichten, mit «stated zero mean» (quadrierte Renditen), um Mittelwerte mit grossem Schätzfehler zu vermeiden.
  - Untersucht werden mehrere Halbwertszeiten bis 90 Tage; die Abbildungen und die Portfolio-Auswertungen (u. a. Exhibits 6, 7, 12, 14–17, 19) verwenden durchgehend **20 Tage**. Diese Standardwahl wird übernommen, nicht optimiert.
  - Die Autoren verlangen 270 Handelstage Vorlauf (drei Halbwertszeiten der langsamsten Schätzung). Hier: 365 Renditen, also mehr als 18 Halbwertszeiten; das Abschneiden ist vernachlässigbar (Restgewicht 0.5^(365/20), rund 3 · 10⁻⁶).
  - Gleichgewichtete Fenster liefern dort ähnliche Ergebnisse («not reported»).
- **Abweichung:** Harvey et al. skalieren die Rendite von Tag t mit einer Schätzung aus Renditen bis t−2 (24 Stunden Vorlauf). Hier wird die Schätzung aus Renditen bis und mit Schluss t verwendet und zur Eröffnung t+1 umgesetzt, wie die Basis (PAPER §2). Kein Look-ahead, aber ohne den zusätzlichen Tag Puffer.
- **Warmup (v0.2):** n = Zahl der verfügbaren, lückenlosen Tagesrenditen bis und mit Schluss t (höchstens 365).
  - n < 60: s = 1 (keine Skalierung; das Overlay verhält sich wie die Basis).
  - 60 ≤ n < 365: σ_kurz (EWMA, Halbwertszeit 20, Gewichte über die n Renditen normiert) und σ_lang (RMS über die n Renditen) werden **expandierend** über die verfügbare Historie gerechnet.
  - n = 365: Regelbetrieb wie oben.
  - Relevanz: Bei Start mit Kraken-Daten ab 2024-09-27 liegen für alle Coins mit durchgehender Historie mehr als 365 Renditen vor; der Warmup betrifft Coins mit kurzer Kraken-Historie oder einen Neubeginn nach einer Lücke, die ausserhalb des Fensters liegt.
  - Die Schwelle 60 ist gesetzt (Entscheid Projektleitung), nicht hergeleitet; sie entspricht drei Halbwertszeiten des EWMA (analog zur Vorlaufregel von Harvey et al.: drei Halbwertszeiten der langsamsten Schätzung).
- Annualisierung √365, weil Kraken an allen Kalendertagen handelt (Harvey et al. annualisieren je nach Datensatz über Kalender- oder Wochentage).

### 3.4 Zielgewicht und maximaler Hebel
- E_{c,t+1}: nominelle Basis-Exposure für Tag t+1 aus den unveränderten Paper-Regeln (bekannt am Schluss t, weil die Basisorder dann feststeht).
- Zielgewicht w*_{c,t+1} = E_{c,t+1} · s_{c,t}, mit 0 ≤ w* ≤ E ≤ 1.0. Gewicht = Wert der Coin-Position / Equity des Overlay-Sleeves.
- **Maximaler Hebel 1.0:** s ist bei 1 gedeckelt, das Overlay erhöht die Exposure nie über die Basis. Anders als bei Harvey et al., die in ruhigen Phasen hebeln, wird hier nur reduziert. Damit fehlt die Hälfte des dort untersuchten Mechanismus [unsicher: ob ein Sharpe-Effekt ohne Hebelseite überhaupt erwartet werden kann].
- **Buchhaltungskonvention wie PAPER F3/`paper_engine.account` (entschieden 2026-10-02, Vergleichbarkeit):** Das Nominal eines Kaufs ist Zielgewicht × Equity vor dem Trade (höchstens die Equity); die Kosten werden zusätzlich vom Cash abgezogen. Nach einem vollen Einstieg ist das Cash also um genau die Kosten negativ, und das Gewicht liegt rechnerisch um höchstens den Kostenanteil über 1.0 (höchstens 1 / (1 − c_in)), genau wie in der Basis. Ein Test belegt, dass das Overlay mit s ≡ 1 die Equity von `paper_engine.account` für W2 und T55_20 exakt reproduziert.

### 3.5 Umschichtung und No-Trade-Band
- **Basis-Ereignisse werden immer ausgeführt:** Einstieg und Add-on mit w* = E · s, Ausstieg vollständig auf 0 (auch im Status STOPPED).
- **Reine Vol-Anpassungen** (Basis unverändert in Position) nur, wenn |w*_{t+1} − w_t| > 0.10, sonst kein Trade. w_t ist das Gewicht zum Schluss t (nach Kursdrift). Ausführung zur Eröffnung t+1, nach oben höchstens bis E · s.
- **Begründung:** Harvey et al. rechnen mit 1 Basispunkt Kosten je Seite für Aktien und täglicher Anpassung; ihr Umschlag liegt bei Aktien zwischen rund fünf Roundtrips pro Jahr (reaktivste Schätzung) und weniger als einem (trägste). K1 kostet hier 47 Basispunkte je Seite, also rund das 47-Fache. Ein Band begrenzt die Zahl kleiner Umschichtungen; jede reine Vol-Anpassung bewegt mindestens 10 % der Sleeve-Equity und kostet unter K1 mindestens 0.047 % der Equity. Der Wert 0.10 stammt aus Scan v1 (§2) und wird nicht optimiert. [unsicher: tatsächliche Umschlaghäufigkeit auf Krypto; wird forward gemessen und durch den Kosten-Kill KR3 in §8.2 begrenzt.]

### 3.6 Fehlende Daten (fail-closed)
- **Lücke** in den Tageskerzen seit dem Start oder ungültiger Kurs (fehlt, ≤ 0, nicht endlich): Coin-Sleeve **STOPPED**, Auswertung endet dort, Meldung (wie PAPER F6), keine Reparatur nach Sicht.
- **Kurze Historie ist kein Fehler (v0.2):** Weniger als 365 Renditen führen nicht mehr zu STOPPED, sondern zum Warmup nach §3.3 (s = 1 unter 60 Renditen, danach expandierend).
- **Keine gültige Vol-Schätzung** (fehlende Rendite im Fenster wegen Lücke oder ungültigem Kurs, Varianz 0): Status **STOPPED**. Danach wird die Exposure nie mehr erhöht und nicht mehr umgeschichtet; nur Basis-Ausstiege werden ausgeführt. Ein Einstieg der Basis wird vom Overlay dann **nicht** nachvollzogen. Aufhebung nur durch ENTSCHEIDE-Eintrag.
- Invariantenverletzung (Position bei flacher Basis, Ziel über E oder über 1.0, s > 1): Laufabbruch (Exit 5), Betriebs-Kill §8.2.

### 3.7 Start
- Erster Signalbar = erster Bar nach dem Freeze (Konfiguration `start_bar`).
- **Zustandsübernahme (entschieden 2026-10-02):** Hält die Basis zum Start eine Position, übernimmt das Overlay sie zur ersten Eröffnung nach dem Startbar, skaliert mit dem aktuellen s (w* = E · s_Startbar), und bezahlt die Einstiegskosten unter dem jeweiligen Kostenszenario (Trade-Grund «sync»). Das ist kein neues Signal, sondern die Abbildung einer bestehenden Basisposition. Konsistent mit der Zustandsregel der Sleeves A und B (MAKRO_LIQ v0.2 §4), bewusste Abweichung von PAPER F5 («Start flach»). Weiter zur Prüfung bei Claude (§12).
- Ist die Basis am Start flach, bleibt das Overlay flach bis zum nächsten Basis-Einstieg.
- Kapital virtuell 1'000 USD je Strategie und Coin, Zinseszins, kein Zins auf Cash (wie PAPER F3).

## 4. Daten und Betrieb
- Nur öffentliche Kraken-Daten aus dem bestehenden Collector (keine neue Quelle, keine Keys).
- Loader-Sperre: Pfade mit «holdout» oder «validation» werden verweigert (`voltarget_engine.guard_path`).
- Runner `voltarget/run_voltarget.py`, Ausgabe `/workspace/aurum2/paper_voltarget/` (state, ledger, logs). Kein cron-Eintrag in v0.1; ein Scheduler-Eintrag wäre Teil der Freeze-Entscheidung (§11).

## 5. Kosten
- Quelle `config/cost_model_v1.json`, `venue_kraken.values.spot_long_scenarios`, Zuordnung wie PAPER F4:
  - Kauf (Einstieg, Add-on, Vol-Anpassung nach oben): fee + fric + slip_in;
  - Verkauf nach Stopp/Notstopp der Basis: fee + fric + slip_sl;
  - übrige Verkäufe (Filter- oder 20-Tage-Ausstieg, Vol-Anpassung nach unten): fee + fric + slip_in.
- **Primär K1 = `maker_plan`:** 0.40 + 0.02 + 0.05 = 0.47 % je Seite, Stopp-Ausstieg 0.52 %.
- **Sensitivität K2 = `taker_K2`:** 0.80 + 0.06 + 0.15 = 1.01 % je Seite, Stopp-Ausstieg 1.16 %.
- Keine Funding-Kosten (Spot).

## 6. Vergleich

- **Basis (B):** die unveränderten Paper-Sleeves, tägliche Equity aus dem Paper-Ledger (`/workspace/aurum2/paper/ledger/equity_daily.csv`), gleiches Kostenszenario, normiert auf den Overlay-Startbar. Der Overlay-Runner rechnet die Basis zusätzlich mit `paper_engine.account` nach; Abweichung zum Ledger ist ein Betriebsfehler (R3).
- **Overlay (VT):** nach §3.
- **Kontrolle (C), exposure-gleich:** Basis mit konstantem Faktor c statt s, Umschichtung nur bei Basis-Ereignissen. c = mittleres Overlay-Gewicht / mittlere Basis-Exposure über alle Coin-Tage mit offener Basisposition im Auswertungsfenster (ex post, nicht handelbar, analog zur Normierung k bei Harvey et al.). Berechnet mit derselben Engine (`simulate(..., scale_override=c, band=inf)`). Zweck: Ein kleinerer Drawdown allein durch weniger mittlere Exposure gilt nicht als Effekt der Vol-Steuerung.
- **Ebene:** je Strategie das Portfolio der zehn Coin-Sleeves (Summe der Equities, 10'000 USD). Je Coin nur deskriptiv.
- **Metriken:**
  - Sharpe: tägliche einfache Renditen der Portfolio-Equity, Mittelwert / Standardabweichung · √365, ohne Abzug eines Zinses (Cash 0 % wie PAPER F3); daneben Überschuss über DTB3 berichtet.
  - MaxDD: tägliche Schluss-Equity (wie PAPER §5).
  - berichtet: CAGR, Volatilität, Vol of Vol und Mean Shortfall (Harvey et al.: rollende Einmonatsrenditen, unteres 5 %-Quantil), mittlere Exposure, Umschlag, Kosten in USD und nach Grund (Basis-Ereignis, Vol-Anpassung, Synchronisation), Anzahl Tage mit s < 1.

## 7. Gates (je Strategie, Kosten K1, Portfolio-Ebene, Auswertungsfenster §8.1)

### 7.1 Definition
- **G1 MaxDD-Reduktion:** |MaxDD_VT| ≤ 0.90 · |MaxDD_B|, d. h. mindestens 10 % relative Reduktion. **Die Schwelle 0.90 ist gesetzt, nicht hergeleitet** (Mindestrelevanz; keine Datengrundlage). Zur Prüfung bei Claude (§12).
- **G2 keine wesentliche Sharpe-Verschlechterung (v0.2):** Sharpe_VT ≥ Sharpe_B − 0.05, Punktschätzer, beide netto K1, gleiche Tage. Begründung (Entscheid Projektleitung 2026-10-02): Das Overlay soll Drawdowns senken, nicht die Sharpe-Ratio maximieren; eine kleine Einbusse, etwa durch die Umschichtungskosten, ist zulässig. Die Toleranz 0.05 ist gesetzt. Zur Prüfung bei Claude (§12).
- **G3 Effekt über Exposure hinaus:** |MaxDD_VT| ≤ |MaxDD_C|. Bleibt Gate (Entscheid 2026-10-02): G3 ist der einzige Beleg dafür, dass der Drawdown-Rückgang mehr ist als eine blosse Reduktion der mittleren Exposure.
- Umsetzung: `voltarget/gates.py` (`G1_MAXDD_RATIO = 0.90`, `G2_SHARPE_TOL = 0.05`, `evaluate`, `verdict`); die Werte stehen auch in `voltarget_config.json` (`gates`) und werden vom Runner gegen den Code geprüft.
- **Urteil je Strategie:** «bestanden» nur, wenn G1, G2 und G3 unter K1 erfüllt sind; sonst «nicht bestanden». Fehlende Prüfbarkeit (§8.1): «nicht prüfbar».

### 7.2 K2-Sensitivität
- G1–G3 werden unter `taker_K2` gleich gerechnet und berichtet.
- Besteht eine Strategie unter K1, verfehlt aber G2 unter K2: Urteil «bestanden mit Kostenvorbehalt». Dann keine Empfehlung für Micro-Live vor einer Prüfung der Ausführung (Maker-Quote) und der Kraken-Tarife.

### 7.3 Statistik (berichtet, ohne Gate-Wirkung)
- Stationärer Block-Bootstrap der täglichen Renditepaare (VT, B), mittlere Blocklänge 20 Tage, 2'000 Ziehungen, Seed fest im Auswertungsskript: Verteilung von ΔSharpe und ΔMaxDD, einseitige p-Werte.
- Holm über die drei Strategien.
- Lesart: Bei kleiner Trade-Zahl ist die Teststärke gering; «bestanden» heisst «nicht widerlegt», kein Beleg.

## 8. Zeitplan und Kill-Regeln

### 8.1 Termine
- **Betriebs-Review** zusammen mit dem PAPER-v1.0-Review (spätestens 2027-02-02), falls das Overlay dann läuft, danach jährlich im Oktober. Geprüft wird nur der Betrieb: Invarianten 0 Verletzungen, Läufe vollständig, Trades aus den Rohdaten reproduzierbar, Kosten nach §5 gebucht, Basis-Nachrechnung gleich Paper-Ledger. **Keine Leistungszahlen**, kein Leistungsurteil.
- **Leistungsauswertung:** am ersten Oktober-Termin, an dem gleichzeitig gilt:
  - mindestens 24 Monate Forward seit dem Overlay-Start;
  - je Strategie mindestens 20 abgeschlossene Basis-Trades über alle Coins;
  - je Strategie mindestens 60 Coin-Tage mit offener Basisposition und s < 0.80.
- Erreicht eine Strategie diese Bedingungen bis 2030-10-01 nicht: Urteil «nicht prüfbar» für diese Strategie, Auswertung dann mit dem vorhandenen Material nur deskriptiv.

### 8.2 Kill-Regeln
- **KR1 Gate-Kill:** Verfehlt eine Strategie bei der Leistungsauswertung ein Gate unter K1, wird das Overlay für diese Strategie geschlossen. Verfehlen alle drei, ist die Linie geschlossen. Keine Varianten auf denselben Forward-Daten (andere Halbwertszeit, anderes Fenster, anderes Band, absolutes Ziel, Untergrenze, Hebel > 1, Trendfilter). Eine Wiederaufnahme ist nur mit neuer Vorregistrierung zulässig, die diesen Eintrag zitiert.
- **KR2 Betriebs-Kill (sofort):** Invariantenverletzung (Overlay-Position bei flacher Basis, Ziel über E oder 1.0, s > 1), nachgewiesener Look-ahead oder nicht reproduzierbare Trades. Folge: Runner stoppen, ENTSCHEIDE-Eintrag, Behebung nur mit neuer Version und neuer Freeze-Liste; die betroffene Periode wird gekennzeichnet und getrennt ausgewiesen.
- **KR3 Kosten-Kill (an jedem Betriebs-Review):** Liegen die annualisierten Kosten der reinen Vol-Anpassungen (Grund «vol») unter K1 über **1.0 % des mittleren Overlay-Kapitals** einer Strategie, wird das Overlay für diese Strategie gestoppt. Das entspricht grob 21 Mindest-Umschichtungen (0.10 · 0.47 %) je Coin und Jahr. **Die Grenze 1.0 % p. a. ist gesetzt, nicht hergeleitet** (keine Datengrundlage); sie verwendet nur Kosten, keine Leistungszahl. Umsetzung `gates.kr3_cost_kill` (`KR3_COST_LIMIT = 0.01`). Zur Prüfung bei Claude (§12).
- **KR4 Nicht prüfbar:** Sind bis 2030-10-01 für keine Strategie die Bedingungen §8.1 erfüllt, wird die Linie als «nicht prüfbar» geschlossen.
- Zwischen den Terminen werden Leistungszahlen des Overlays nicht für Entscheidungen verwendet.

### 8.3 Erfolg
Nur eine Empfehlung an Damian (z. B. Overlay als Sizing-Regel für eine allfällige Micro-Live-Phase); Entscheid D2 bei Damian.

## 9. Gültiger Testpfad

- **Einziger gültiger Test: Forward-Paper ab dem Freeze.** Der Zeitraum 2024–2026 ist durch Marktkenntnis kontaminiert (ENTSCHEIDE 2026-10-01 22:40), BTC und ETH < 2024 zusätzlich durch Scan v1/v2.
- Jeder historische Lauf (Binance < 2024, Kraken 2024-09 bis Freeze oder andere) ist **deskriptiv**: höchstens einmal, erst nach dem Freeze, gekennzeichnet «deskriptiv, kein Test, Vorbelastung», ohne Einfluss auf Regel, Parameter, Gates oder Urteil. Er wird bei der Leistungsauswertung nicht berücksichtigt.
- Vor dem Freeze wird kein historischer Lauf gerechnet.

## 10. Umsetzung (Stand v0.2, gesperrt)

- `voltarget/voltarget_engine.py`: Kern ohne Datenzugriff (Schätzer mit Warmup, Skalierung, Band, Simulation mit Zustandsübernahme, Invarianten, Loader-Sperre).
- `voltarget/gates.py`: Sharpe, MaxDD, Kontrollfaktor c, G1–G3, Urteil, Kosten-Kill KR3.
- `voltarget/base_adapter.py`: Basis-Exposure aus `paper/paper_engine.py` (nur Import, keine Änderung).
- `voltarget/run_voltarget.py`: Tageslauf; verweigert ohne Freigabe (Exit 3, kein Dry-Run-Bypass), prüft Parameter gegen die Engine (Exit 4) und die Freeze-Liste (Exit 4).
- `voltarget/voltarget_config.json`: enabled=false, start_bar=null, freeze_list=null, Parameter und Gates wie §0.
- `tests/test_voltarget.py`: synthetische Tests (Skalierungsmathematik, Warmup und expandierende Schätzung, Deckel 1.0, Band, keine Signalerzeugung, fehlende Daten, Zustandsübernahme, Kostenkonvention PAPER F3, Gleichheit mit der Basis bei s ≡ 1, Gates inkl. G2-Toleranz, KR3, Laufzeitsperre, kein Scheduler-Eintrag).
- Kein Scheduler-Eintrag (`collector/ensure_scheduler.sh` unverändert), kein Shell-Wrapper.

## 11. Freeze-Voraussetzungen (nicht Teil von v0.1)
1. Review Claude zu dieser Fassung und Antworten auf §12.
2. Kein Veto Damian; datierter ENTSCHEIDE-Eintrag.
3. Fassung v1.0 mit Freeze-Liste `00_doku/voltarget_freeze_<datum>_expected_shas.txt` (mindestens: Prereg, Engine, Gates, Adapter, Runner, Konfiguration, Tests, `config/cost_model_v1.json`, `paper/paper_engine.py`, `01_forschung/02_strategien/s2lib.py`), Tag `voltarget-v1.0-freeze`.
4. Erst dann: enabled=true, start_bar, freeze_list, allenfalls Scheduler-Eintrag nach dem Paper-Lauf.

## 12. Offene Fragen an Claude

Alle übrigen Punkte aus v0.1 §12 sind von der Projektleitung entschieden (§0a). Offen zur Prüfung sind nur:

1. **G2-Toleranz (v0.1 Frage 3):** Ist Sharpe_VT ≥ Sharpe_Basis − 0.05 angemessen? Die Toleranz ist gesetzt; Begründung: Das Overlay soll Drawdowns senken, nicht die Sharpe-Ratio maximieren. Zu prüfen ist, ob 0.05 bei der erwarteten kleinen Trade-Zahl eher zu eng (Rauschen) oder zu weit (lässt eine echte Verschlechterung durch) ist.
2. **Gesetzte Schwellen 0.90 und 1 % p. a. (v0.1 Frage 5):** G1 (|MaxDD_VT| ≤ 0.90 · |MaxDD_Basis|) und der Kosten-Kill KR3 (Kosten reiner Vol-Anpassungen > 1.0 % p. a. des mittleren Kapitals) sind ausdrücklich gesetzt und nicht hergeleitet. Sind die Werte vertretbar, oder gibt es eine begründbare Alternative?
3. **Übernahme bestehender Basispositionen beim Start (v0.1 Frage 6):** Das Overlay übernimmt am Start bestehende Basispositionen, skaliert mit dem aktuellen s und mit Einstiegskosten (konsistent mit Sleeves A/B, abweichend von PAPER F5 «Start flach»). Ist das für den Vergleich gegen die unveränderten Sleeves (§6, normiert auf den Startbar) sauber, oder verzerrt die Übernahme (Kosten, Einstiegszeitpunkt mitten in einem Trade) die Gates?

## 13. Quellen
- Harvey, C. R., E. Hoyle, R. Korgaonkar, S. Rattray, M. Sargaison, O. Van Hemert (2018): «The Impact of Volatility Targeting». *Journal of Portfolio Management* 45(1), 14–33. DOI 10.3905/jpm.2018.45.1.014. Volltext: https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf; SSRN 3175538: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3175538 (abgerufen 2026-10-02). Verwendete Aussagen: Ziel 10 % p. a. mit Ex-post-Konstante k; EWMA der Tagesrenditen mit Mittelwert 0; Halbwertszeiten bis 90 Tage, Standard in den Abbildungen 20 Tage; 270 Handelstage Vorlauf; Schätzung 24 Stunden vor der skalierten Rendite (Renditen bis t−2); Kosten 1 Basispunkt für Aktien; Umschlag rund fünfmal bis unter einmal pro Jahr (Aktien); Sharpe-Verbesserung nur bei Risikoanlagen über den Leverage-Effekt; geringere Wahrscheinlichkeit von Extremrenditen über alle Anlageklassen; tieferer maximaler Drawdown bei US-Aktien sowie beim Balanced- und Risk-Parity-Portfolio. Exakte Tabellenwerte (Exhibits 5, 8, 11, 13, 16) sind in der abgerufenen Textfassung nicht lesbar und werden deshalb nicht zitiert.
- Moreira, A., T. Muir (2017): «Volatility Managed Portfolios». *Journal of Finance* 72(4), 1611–1644 (nur als Hintergrund, zitiert nach Harvey et al. und Ideen-Scan v2 §2.12).
- Intern: `01_forschung/12_ideen_scan/ideen_scan_v1.md` §2 und Trial-Accounting; `01_forschung/14_ideen_scan_v2/ideen_scan_v2.md` §0, §4; `paper/PAPER_PREREG_v1.0.md`; `config/cost_model_v1.json` v1.1; `00_doku/ENTSCHEIDE.md` (2026-10-01 C1, C2, 22:15, 22:35, 22:40).
