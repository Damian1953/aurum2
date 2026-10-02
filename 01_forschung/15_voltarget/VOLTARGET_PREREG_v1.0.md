# VOLTARGET_PREREG v1.0 – Volatilitäts-Targeting als Risiko-Overlay auf W2, W6 und Turtle 55/20 (Forward-Paper)

> **v1.0 EINGEFROREN am 2026-10-02 (Freigabe Damian 11:45 Zürich), Tag `voltarget-v1.0-freeze`.**

**Status: v1.0 EINGEFROREN 2026-10-02.** Freeze-Liste `00_doku/voltarget_freeze_2026-10-02_expected_shas.txt`, Tag `voltarget-v1.0-freeze`, ENTSCHEIDE 2026-10-02. Startbar 2026-10-03 (erster voller Tagesbar nach dem Freeze; Basis wie PAPER v1.0 ab 2026-10-02), Runner `voltarget/run_voltarget.sh` täglich 07:00 Zürich (cron `aurum2-voltarget`). Der folgende Text ist unverändert der freigegebene Kandidat.
**Stand:** 2026-10-02 (Zürich, UTC+2). Branch `voltarget-v0`. Ersetzt `VOLTARGET_PREREG_v0.2.md` (bleibt wie v0.1 unverändert als Historie liegen).
**Grundlage v1.0:** Review Claude zu v0.2, zusammengefasst in `review_claude_voltarget_v1.md` (Änderungen siehe §0b). Die Entscheide der Projektleitung zu v0.2 (§0a) gelten weiter.
**Freeze erst nach:** Freigabe des Kandidaten, kein Veto Damian, datierter ENTSCHEIDE-Eintrag, Freeze-Liste mit SHA-256 (§11). **Startvoraussetzung:** gemeinsamer einseitiger Wochenbericht und gemeinsamer Heartbeat aller Forward-Linien (Branch `sleeves-v1`, §4).

Grundlagen:
- Ideen-Scan v1 (`01_forschung/12_ideen_scan/ideen_scan_v1.md`) §2: «GO für Vorregistrierung, aber nur als Risiko-Overlay auf den bestehenden Paper-Kandidaten. Gemessen werden soll die Risikotransformation, nicht neue Alpha.»
- Ideen-Scan v2 (`01_forschung/14_ideen_scan_v2/ideen_scan_v2.md`) §1, §2.9, §2.12: Vol-Target-Overlay bleibt GO-Kandidat aus v1.
- PAPER_PREREG v1.0 (`paper/PAPER_PREREG_v1.0.md`, eingefroren 2026-10-01 22:15): Sleeves, Ausführung, Kosten F4, Daten F6.
- `config/cost_model_v1.json` Version 1.1, Abschnitt `venue_kraken` (ENTSCHEIDE C1/C2).
- ENTSCHEIDE 2026-10-01 22:35/22:40 (Trial-Zähler rund 270; 2024–2026 kein Testfenster wegen Kontext-Vorbelastung).

Was immer gilt: keine Keys, keine Orders, keine Börsenverbindung, kein Holdout (`02_daten/holdout/` und alle Dateien mit «validation» im Namen sind im Loader gesperrt). `paper/` und alle Freeze-Dateien bleiben unverändert. Alle Zahlen sind hypothetisch (Paper).

## 0a. Änderungen v0.1 → v0.2 (Entscheide Projektleitung, Historie; «offen für Claude» dort ist durch §0b erledigt)

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

## 0b. Änderungen gegenüber v0.2 (Review Claude, Changelog)

| Nr. | Stelle | Punkt | Umsetzung in v1.0 |
|---|---|---|---|
| M1 | §1 | Erwartung: Overlay selten aktiv, «nicht prüfbar» wahrscheinlich, Überschneidung mit ATR-Stopp und 20-Tage-Ausstieg | §1 «Erwartung» |
| M2 | §7.1 | Zusammenspiel G1/G3: c < 0.90 → G3 strenger; c nahe 1 → G1 greift | §7.1 |
| M3 | §8.2 | KR3 am ersten Review nur, wenn zusätzlich nicht annualisiert > 0.33 % | §8.2; `gates.py` (`KR3_FIRST_REVIEW_MIN`, `kr3_cost_kill(first_review=True)`); Tests |
| M4 | §3.7, §6 | Symmetrische Sync-Buchung für B (E) und C (E·c), gleiche Kosten; Sync-Kosten VT getrennt; Test VT = B = C bei s ≡ 1 inkl. Sync | §3.7, §6; Engine `run_compare`, `sync_costs`, `costs_by_reason`; Runner `eq_base_sync`; Tests |
| bestätigt | §7.1, §3.7, §6 | G2-Toleranz 0.05; Cash 0 % und Sharpe ohne Zinsabzug | unverändert |
| Bericht | §6 | Verteilung von s je Coin (Coin-Tage mit s < 1) | §6; `scale_distribution`; Zustand `s_verteilung`, `summary` |
| Betrieb | §4 | gemeinsamer Wochenbericht inkl. VOLTARGET und gemeinsamer Heartbeat als Startvoraussetzung | §4, §11; Branch `sleeves-v1` |
| **Präzisierung vor dem Freeze** (Entscheid Projektleitung 2026-10-02) | §3.4, §3.5, §6 | Kursdrift löst keine Vol-Anpassung aus: Ziel ohne Basis-Ereignis = aktuelles, driftendes Gewicht der Basis B mal s (w_B(t) · s), nicht E · s; das Band vergleicht das VT-Gewicht mit w_B(t) · s. Mit s ≡ 1 ist VT exakt B. Keine inhaltliche Änderung gegenüber dem Review Claude (VT als skalierte Version von B auf denselben Positionen) | §3.4, §3.5, §6; Engine (`rebalance_target(..., w_base)`, Schattenkonto B in `simulate`); Tests für W2, W6 (E = 0.5, 0.75) und T55_20 |

## 0. Festgelegte Werte auf einen Blick

| Punkt | Festlegung | Begründung |
|---|---|---|
| Basis | W2, W6, T55_20 je 10 Coins, unverändert aus PAPER v1.0 | §1 |
| Zielvolatilität | je Coin die eigene realisierte Volatilität der letzten 365 Tage (σ_lang); Skalierung s = min(1, σ_lang / σ_kurz) | §3.2 |
| Messfenster | σ_kurz: EWMA der quadrierten Tagesrenditen, Halbwertszeit **20 Tage**, Fenster **365** Renditen | §3.3 (Harvey et al. 2018) |
| Warmup | unter **60** verfügbaren Renditen s = 1; ab 60 beide Schätzer expandierend über die verfügbare Historie bis 365 | §3.3 |
| Annualisierung | √365 (Krypto handelt 7 Tage) | §3.3 |
| Maximaler Hebel | **1.0**: s ≤ 1, Overlay-Gewicht ≤ Basis-Exposure ≤ 1.0 | §3.4 |
| No-Trade-Band | reine Vol-Anpassung nur bei \|w_B(t) · s − w\| > **0.10** (Anteil Sleeve-Equity, w_B = driftendes Gewicht der Basis); Basis-Ereignisse immer | §3.5 |
| Start | Übernahme bestehender Basispositionen, skaliert mit dem aktuellen s; B und C buchen dieselbe Übernahme symmetrisch (E bzw. E·c, gleiche Kosten) | §3.7, §6 |
| Kostenkonvention | wie PAPER F3: Nominal = Gewicht × Equity vor dem Trade, Kosten zusätzlich | §3.4 |
| Kosten | K1 = `maker_plan` primär (0.47 % je Seite, Stopp-Ausstieg 0.52 %), K2 = `taker_K2` Sensitivität (1.01 % bzw. 1.16 %) | §5 |
| Vergleich | unveränderte Sleeves (Paper-Ledger) und Kontrollrechnung C mit gleicher mittlerer Exposure | §6 |
| Gates (K1) | G1 \|MaxDD_VT\| ≤ 0.90 · \|MaxDD_Basis\| (gesetzt); G2 Sharpe_VT ≥ Sharpe_Basis − 0.05; G3 \|MaxDD_VT\| ≤ \|MaxDD_C\| | §7 |
| Auswertung | frühestens nach 24 Monaten Forward (Oktober-Termin), spätestens 2030-10-01 | §8 |
| Kill | Gate verfehlt → Overlay für die Strategie geschlossen, keine Varianten; Betriebs-Kill sofort; Kosten-Kill > 1.0 % p. a. (gesetzt), am ersten Review zusätzlich nicht annualisiert > 0.33 % | §8 |
| Testpfad | **nur** Forward-Paper ab Freeze; jeder historische Lauf ist deskriptiv | §9 |

## 1. Zweck und Abgrenzung

- **Zweck:** Prüfen, ob eine Volatilitäts-Skalierung der Positionsgrösse die Risikokennzahlen der laufenden Paper-Sleeves verbessert (kleinerer maximaler Drawdown), ohne die Sharpe-Ratio zu verschlechtern.
- **Kein neues Signal.** Das Overlay
  - ist flach, wenn die Basis flach ist;
  - steigt nur ein, wenn die Basis einsteigt (oder beim Start eine Basisposition übernimmt, §3.7);
  - verkauft vollständig, wenn die Basis aussteigt;
  - hält nie mehr als die Basis-Exposure E (W2, T55_20: 1.0 in Position; W6: 0.50 / 0.75 / 1.00).
- **Keine Alpha-Hypothese.** Harvey et al. (2018) finden eine höhere Sharpe-Ratio nur für «Risikoanlagen» (Aktien, Kredit), für Anleihen, Währungen und Rohstoffe einen vernachlässigbaren Effekt, aber über alle Anlageklassen seltenere Extremrenditen und weniger schwere Verluste im linken Rand. Für Krypto liegt aus dieser Quelle **keine** Evidenz vor [unsicher: Übertragbarkeit].
- **Erwartung (v1.0, Review Claude M1):** Das Overlay wird **selten aktiv** sein. Es reduziert nur, wenn die Basis in Position ist **und** die kurzfristige Volatilität über dem eigenen Jahresniveau liegt (s < 1, mit Band 0.10 bei E = 1 erst ab s < 0.90). Genau in solchen Phasen steigender Volatilität greifen oft schon der ATR-Stopp (W2, W6) bzw. der 20-Tage-Ausstieg (T55_20) der Basis und schliessen die Position; das Overlay überschneidet sich also stark mit diesen Ausstiegen und hat wenig eigenen Spielraum. Dass die Prüfbarkeitsbedingungen (§8.1, insbesondere 60 Coin-Tage mit offener Basis und s < 0.80) bis 2030-10-01 nicht erreicht werden und das Urteil **«nicht prüfbar»** lautet, ist **wahrscheinlich** und wird ausdrücklich als mögliches Ergebnis akzeptiert.
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
- Zielgewicht bei Basis-Ereignissen (Einstieg, Add-on) und bei der Sync-Buchung: w*_{c,t+1} = E_{c,t+1} · s_{c,t}, mit 0 ≤ w* ≤ E ≤ 1.0. Gewicht = Wert der Coin-Position / Equity des Overlay-Sleeves.
- **Präzisierung vor dem Freeze (Entscheid Projektleitung 2026-10-02):** Ohne Basis-Ereignis ist das Ziel das **aktuelle, durch Kursdrift veränderte Gewicht der Basis B** zum Schluss t mal s: w*_{c,t+1} = w_B,c(t) · s_{c,t} (gedeckelt bei 1.0). B ist die unveränderte Basis mit s = 1 und derselben Sync-Buchung (§6), in der Engine als Schattenkonto mitgeführt. Damit ist VT eine skalierte Version von B auf denselben Positionen; reine Kursdrift löst keine Umschichtung aus, und mit s ≡ 1 ist VT exakt B (auch bei W6 mit E = 0.50 oder 0.75). Das ist keine inhaltliche Änderung gegenüber dem Review Claude, sondern die Präzisierung der dort beschriebenen Regel. Hinweis: Bei konstantem s < 1 kann das VT-Gewicht bei starker Drift trotzdem um mehr als 0.10 von w_B · s abweichen (die nicht investierte Cash-Quote von VT ist grösser als jene von B); dann wird auf w_B · s zurückgeführt. Das ist gewollt (Gewichtsziel), wird als Grund «vol» gebucht und zählt für KR3.
- **Maximaler Hebel 1.0:** s ist bei 1 gedeckelt, das Overlay erhöht die Exposure nie über die Basis. Anders als bei Harvey et al., die in ruhigen Phasen hebeln, wird hier nur reduziert. Damit fehlt die Hälfte des dort untersuchten Mechanismus [unsicher: ob ein Sharpe-Effekt ohne Hebelseite überhaupt erwartet werden kann].
- **Buchhaltungskonvention wie PAPER F3/`paper_engine.account` (entschieden 2026-10-02, Vergleichbarkeit):** Das Nominal eines Kaufs ist Zielgewicht × Equity vor dem Trade (höchstens die Equity); die Kosten werden zusätzlich vom Cash abgezogen. Nach einem vollen Einstieg ist das Cash also um genau die Kosten negativ, und das Gewicht liegt rechnerisch um höchstens den Kostenanteil über 1.0 (höchstens 1 / (1 − c_in)), genau wie in der Basis. Ein Test belegt, dass das Overlay mit s ≡ 1 die Equity von `paper_engine.account` für W2 und T55_20 exakt reproduziert.

### 3.5 Umschichtung und No-Trade-Band
- **Basis-Ereignisse werden immer ausgeführt:** Einstieg und Add-on mit w* = E · s, Ausstieg vollständig auf 0 (auch im Status STOPPED).
- **Reine Vol-Anpassungen** (Basis unverändert in Position) nur, wenn |w_B(t) · s_t − w_t| > 0.10, sonst kein Trade. w_t ist das VT-Gewicht und w_B(t) das Gewicht der Basis B, beide zum Schluss t nach Kursdrift (Präzisierung vor dem Freeze, §3.4). Ausführung zur Eröffnung t+1 auf w_B(t) · s_t.
- **Begründung:** Harvey et al. rechnen mit 1 Basispunkt Kosten je Seite für Aktien und täglicher Anpassung; ihr Umschlag liegt bei Aktien zwischen rund fünf Roundtrips pro Jahr (reaktivste Schätzung) und weniger als einem (trägste). K1 kostet hier 47 Basispunkte je Seite, also rund das 47-Fache. Ein Band begrenzt die Zahl kleiner Umschichtungen; jede reine Vol-Anpassung bewegt mindestens 10 % der Sleeve-Equity und kostet unter K1 mindestens 0.047 % der Equity. Der Wert 0.10 stammt aus Scan v1 (§2) und wird nicht optimiert. [unsicher: tatsächliche Umschlaghäufigkeit auf Krypto; wird forward gemessen und durch den Kosten-Kill KR3 in §8.2 begrenzt.]

### 3.6 Fehlende Daten (fail-closed)
- **Lücke** in den Tageskerzen seit dem Start oder ungültiger Kurs (fehlt, ≤ 0, nicht endlich): Coin-Sleeve **STOPPED**, Auswertung endet dort, Meldung (wie PAPER F6), keine Reparatur nach Sicht.
- **Kurze Historie ist kein Fehler (v0.2):** Weniger als 365 Renditen führen nicht mehr zu STOPPED, sondern zum Warmup nach §3.3 (s = 1 unter 60 Renditen, danach expandierend).
- **Keine gültige Vol-Schätzung** (fehlende Rendite im Fenster wegen Lücke oder ungültigem Kurs, Varianz 0): Status **STOPPED**. Danach wird die Exposure nie mehr erhöht und nicht mehr umgeschichtet; nur Basis-Ausstiege werden ausgeführt. Ein Einstieg der Basis wird vom Overlay dann **nicht** nachvollzogen. Aufhebung nur durch ENTSCHEIDE-Eintrag.
- Invariantenverletzung (Position bei flacher Basis, Ziel über E oder über 1.0, s > 1): Laufabbruch (Exit 5), Betriebs-Kill §8.2.

### 3.7 Start
- Erster Signalbar = erster Bar nach dem Freeze (Konfiguration `start_bar`).
- **Zustandsübernahme (entschieden 2026-10-02):** Hält die Basis zum Start eine Position, übernimmt das Overlay sie zur ersten Eröffnung nach dem Startbar, skaliert mit dem aktuellen s (w* = E · s_Startbar), und bezahlt die Einstiegskosten unter dem jeweiligen Kostenszenario (Trade-Grund «sync»). Das ist kein neues Signal, sondern die Abbildung einer bestehenden Basisposition. Konsistent mit der Zustandsregel der Sleeves A und B (MAKRO_LIQ §4), bewusste Abweichung von PAPER F5 («Start flach»).
- **Symmetrische Sync-Buchung (v1.0, Review Claude M4):** Die Vergleichsreihen buchen dieselbe Übernahme zur selben Eröffnung mit denselben Kosten: die Basis **B mit Gewicht E** (s = 1) und die Kontrolle **C mit Gewicht E · c**. So startet keine der drei Reihen mit einem Vorteil aus einem früheren Einstieg zu einem anderen Preis. Umsetzung: `voltarget_engine.run_compare` (eine Engine für VT, B und C). Die Sync-Kosten von VT werden getrennt ausgewiesen (§6). Test: Mit s ≡ 1 sind VT, B und C identisch, inklusive Sync.
- Ist die Basis am Start flach, bleibt das Overlay flach bis zum nächsten Basis-Einstieg.
- Kapital virtuell 1'000 USD je Strategie und Coin, Zinseszins, kein Zins auf Cash (wie PAPER F3).

## 4. Daten und Betrieb
- Nur öffentliche Kraken-Daten aus dem bestehenden Collector (keine neue Quelle, keine Keys).
- Loader-Sperre: Pfade mit «holdout» oder «validation» werden verweigert (`voltarget_engine.guard_path`).
- Runner `voltarget/run_voltarget.py`, Ausgabe `/workspace/aurum2/paper_voltarget/` (state, ledger, logs). Kein cron-Eintrag; ein Scheduler-Eintrag wäre Teil der Freeze-Entscheidung (§11).
- **Gemeinsamer Wochenbericht und Heartbeat (v1.0, Startvoraussetzung):** VOLTARGET erscheint im gemeinsamen einseitigen Wochenbericht aller Forward-Linien (`paper/wochenbericht.py`, Abschnitt «VOLTARGET-Overlay»: je Strategie Status, Coins ok, Coin-Tage mit offener Basis und davon s < 1, Sync-Kosten VT; dazu s < 1 je Coin). Der gemeinsame Heartbeat (`forward/heartbeat.py`) zeigt eine Statuszeile je Runner (Collector, PAPER v1.0, Sleeves A/B, VOLTARGET) und Alarm, wenn ein erwarteter Lauf fehlt (> 26 h) oder fehlgeschlagen ist. Beides liegt auf Branch `sleeves-v1`; VOLTARGET liefert nur `state/state_latest.json` (Schlüssel `summary`, `s_verteilung`, `rc`, `run_utc`) und `logs/run_history.jsonl` (`run_utc`, `rc`) nach der dort dokumentierten Schnittstelle. Kein cron.

## 5. Kosten
- Quelle `config/cost_model_v1.json`, `venue_kraken.values.spot_long_scenarios`, Zuordnung wie PAPER F4:
  - Kauf (Einstieg, Add-on, Vol-Anpassung nach oben): fee + fric + slip_in;
  - Verkauf nach Stopp/Notstopp der Basis: fee + fric + slip_sl;
  - übrige Verkäufe (Filter- oder 20-Tage-Ausstieg, Vol-Anpassung nach unten): fee + fric + slip_in.
- **Primär K1 = `maker_plan`:** 0.40 + 0.02 + 0.05 = 0.47 % je Seite, Stopp-Ausstieg 0.52 %.
- **Sensitivität K2 = `taker_K2`:** 0.80 + 0.06 + 0.15 = 1.01 % je Seite, Stopp-Ausstieg 1.16 %.
- Keine Funding-Kosten (Spot).

## 6. Vergleich

- **Basis (B, v1.0):** die unveränderten Paper-Regeln mit **s = 1**, gerechnet mit derselben Engine ab dem Overlay-Startbar, mit symmetrischer Sync-Buchung (Gewicht E, gleiche Kosten, §3.7) und ohne Vol-Anpassungen (Spalte `eq_base_sync`). Diese Reihe ist die Vergleichsbasis der Gates. Die Paper-Ledger-Nachrechnung mit `paper_engine.account` (Spalte `eq_base`) bleibt Betriebsprüfung R3 (Trades nach dem Start müssen übereinstimmen).
- **Overlay (VT):** nach §3.
- **Kontrolle (C), exposure-gleich:** Basis mit konstantem Faktor c statt s, Umschichtung nur bei Basis-Ereignissen, Sync-Buchung am Startbar mit Gewicht E · c und denselben Kosten (§3.7).
  - **Konsistenz mit der Präzisierung (§3.4):** C kauft bei jedem Basis-Ereignis E · c und lässt die Position danach mit dem Kurs driften (kein Band, keine Umschichtung). Zwischen zwei Ereignissen hält C damit dieselbe Coin-Menge, die Position driftet wie die von B; das Gewicht von C folgt w_B · c nur näherungsweise (die Cash-Quote von C ist grösser). C ist daher «B-Position mal c zum Zeitpunkt der Basis-Ereignisse», ohne Drift-Umschichtung; mit c = 1 ist C exakt B (Test). c = mittleres Overlay-Gewicht / mittlere Basis-Exposure über alle Coin-Tage mit offener Basisposition im Auswertungsfenster (ex post, nicht handelbar, analog zur Normierung k bei Harvey et al.). Berechnet mit derselben Engine (`simulate(..., scale_override=c, band=inf)`). Zweck: Ein kleinerer Drawdown allein durch weniger mittlere Exposure gilt nicht als Effekt der Vol-Steuerung.
- **Ebene:** je Strategie das Portfolio der zehn Coin-Sleeves (Summe der Equities, 10'000 USD). Je Coin nur deskriptiv.
- **Metriken:**
  - Sharpe: tägliche einfache Renditen der Portfolio-Equity, Mittelwert / Standardabweichung · √365, ohne Abzug eines Zinses (Cash 0 % wie PAPER F3); daneben Überschuss über DTB3 berichtet.
  - MaxDD: tägliche Schluss-Equity (wie PAPER §5).
  - berichtet: CAGR, Volatilität, Vol of Vol und Mean Shortfall (Harvey et al.: rollende Einmonatsrenditen, unteres 5 %-Quantil), mittlere Exposure, Umschlag, Kosten in USD und nach Grund (Basis-Ereignis, Vol-Anpassung, Synchronisation), **Sync-Kosten von VT getrennt** (und zum Vergleich jene von B), Anzahl Tage mit s < 1.
  - **Verteilung von s je Coin (v1.0):** Tage seit Start, Tage mit s < 1, Coin-Tage mit offener Basis und davon s < 1, Minimum und Mittel von s, Klassen < 0.5 / 0.5–0.8 / 0.8–1 / = 1 (`scale_distribution`, Zustand `s_verteilung`). Nur Bericht.

## 7. Gates (je Strategie, Kosten K1, Portfolio-Ebene, Auswertungsfenster §8.1)

### 7.1 Definition
- **G1 MaxDD-Reduktion:** |MaxDD_VT| ≤ 0.90 · |MaxDD_B|, d. h. mindestens 10 % relative Reduktion. **Die Schwelle 0.90 ist gesetzt, nicht hergeleitet** (Mindestrelevanz; keine Datengrundlage).
- **G2 keine wesentliche Sharpe-Verschlechterung:** Sharpe_VT ≥ Sharpe_B − 0.05, Punktschätzer, beide netto K1, gleiche Tage, ohne Zinsabzug (Cash 0 %, im Review Claude bestätigt). Begründung (Entscheid Projektleitung 2026-10-02): Das Overlay soll Drawdowns senken, nicht die Sharpe-Ratio maximieren; eine kleine Einbusse, etwa durch die Umschichtungskosten, ist zulässig. Die Toleranz 0.05 ist gesetzt und im Review Claude **bestätigt**.
- **G3 Effekt über Exposure hinaus:** |MaxDD_VT| ≤ |MaxDD_C|. Bleibt Gate (Entscheid 2026-10-02): G3 ist der einzige Beleg dafür, dass der Drawdown-Rückgang mehr ist als eine blosse Reduktion der mittleren Exposure.
- **Zusammenspiel G1 und G3 (v1.0, Review Claude M2):** C hält dauernd den Anteil c der Basis-Exposure. Sein Drawdown ist deshalb näherungsweise c · |MaxDD_B| (bei konstanter Gewichtung genau proportional, ohne Umschichtung annähernd). G3 verlangt damit ungefähr |MaxDD_VT| ≤ c · |MaxDD_B|, G1 verlangt |MaxDD_VT| ≤ 0.90 · |MaxDD_B|. Folge: Ist **c < 0.90** (das Overlay reduziert im Mittel um mehr als 10 %), ist **G3 die strengere Schranke**, und G1 ist dann praktisch erfüllt, wenn G3 hält. Liegt **c nahe bei 1** (das Overlay reduziert selten, vgl. §1 Erwartung), ist G3 fast gleich |MaxDD_VT| ≤ |MaxDD_B| und damit schwach; dann **greift G1** und verlangt die Mindestreduktion von 10 %. Beide Gates bleiben bestehen; berichtet wird zusätzlich, welche Schranke bindend war.
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
- **KR3 Kosten-Kill (an jedem Betriebs-Review):** Liegen die annualisierten Kosten der reinen Vol-Anpassungen (Grund «vol») unter K1 über **1.0 % des mittleren Overlay-Kapitals** einer Strategie, wird das Overlay für diese Strategie gestoppt. Das entspricht grob 21 Mindest-Umschichtungen (0.10 · 0.47 %) je Coin und Jahr. **Die Grenze 1.0 % p. a. ist gesetzt, nicht hergeleitet** (keine Datengrundlage); sie verwendet nur Kosten, keine Leistungszahl. Umsetzung `gates.kr3_cost_kill` (`KR3_COST_LIMIT = 0.01`).
  - **Erster Betriebs-Review (v1.0, Review Claude M3):** Das Fenster bis zum ersten Review ist kurz (höchstens rund vier Monate); die Annualisierung würde wenige Umschichtungen stark aufblasen. Am ersten Review greift KR3 deshalb nur, wenn **zusätzlich** die **nicht annualisierten** Kosten der reinen Vol-Anpassungen über **0.33 %** des mittleren Overlay-Kapitals liegen (rund ein Drittel der Jahresgrenze, also etwa vier Monate bei 1 % p. a.). Ab dem zweiten Review gilt nur die Jahresgrenze. Umsetzung `kr3_cost_kill(..., first_review=True)`, `KR3_FIRST_REVIEW_MIN = 0.0033`, Konfiguration `gates.kr3_first_review_min`.
- **KR4 Nicht prüfbar:** Sind bis 2030-10-01 für keine Strategie die Bedingungen §8.1 erfüllt, wird die Linie als «nicht prüfbar» geschlossen.
- Zwischen den Terminen werden Leistungszahlen des Overlays nicht für Entscheidungen verwendet.

### 8.3 Erfolg
Nur eine Empfehlung an Damian (z. B. Overlay als Sizing-Regel für eine allfällige Micro-Live-Phase); Entscheid D2 bei Damian.

## 9. Gültiger Testpfad

- **Einziger gültiger Test: Forward-Paper ab dem Freeze.** Der Zeitraum 2024–2026 ist durch Marktkenntnis kontaminiert (ENTSCHEIDE 2026-10-01 22:40), BTC und ETH < 2024 zusätzlich durch Scan v1/v2.
- Jeder historische Lauf (Binance < 2024, Kraken 2024-09 bis Freeze oder andere) ist **deskriptiv**: höchstens einmal, erst nach dem Freeze, gekennzeichnet «deskriptiv, kein Test, Vorbelastung», ohne Einfluss auf Regel, Parameter, Gates oder Urteil. Er wird bei der Leistungsauswertung nicht berücksichtigt.
- Vor dem Freeze wird kein historischer Lauf gerechnet.

## 10. Umsetzung (Stand v1.0-Kandidat, gesperrt)

- `voltarget/voltarget_engine.py`: Kern ohne Datenzugriff (Schätzer mit Warmup, Skalierung, Band, Simulation mit Zustandsübernahme, Invarianten, Loader-Sperre).
- `voltarget/gates.py`: Sharpe, MaxDD, Kontrollfaktor c, G1–G3, Urteil, Kosten-Kill KR3 (mit Zusatzbedingung am ersten Review).
- `voltarget_engine.run_compare`, `sync_costs`, `costs_by_reason`, `scale_distribution` (v1.0): symmetrischer Vergleich VT/B/C, Sync-Kosten getrennt, Verteilung von s.
- `voltarget/base_adapter.py`: Basis-Exposure aus `paper/paper_engine.py` (nur Import, keine Änderung).
- `voltarget/run_voltarget.py`: Tageslauf; verweigert ohne Freigabe (Exit 3, kein Dry-Run-Bypass), prüft Parameter gegen die Engine (Exit 4) und die Freeze-Liste (Exit 4).
- `voltarget/voltarget_config.json`: enabled=false, start_bar=null, freeze_list=null, Parameter und Gates wie §0.
- `tests/test_voltarget.py`: synthetische Tests (Skalierungsmathematik, Warmup und expandierende Schätzung, Deckel 1.0, Band, keine Signalerzeugung, fehlende Daten, Zustandsübernahme, Kostenkonvention PAPER F3, Gleichheit mit der Basis bei s ≡ 1, Gates inkl. G2-Toleranz, KR3 inkl. erstem Review, symmetrische Sync-Buchung, Identität VT = B = C bei s ≡ 1 inkl. Sync, Verteilung von s, Zustands-Schnittstelle für den gemeinsamen Wochenbericht, Laufzeitsperre, kein Scheduler-Eintrag).
- Kein Scheduler-Eintrag (`collector/ensure_scheduler.sh` unverändert), kein Shell-Wrapper.

## 11. Freeze- und Startvoraussetzungen
1. Freigabe dieses Kandidaten (Review Claude zu v0.2 umgesetzt, §0b).
2. Kein Veto Damian; datierter ENTSCHEIDE-Eintrag.
3. Fassung v1.0 mit Freeze-Liste `00_doku/voltarget_freeze_<datum>_expected_shas.txt` (mindestens: Prereg, Engine, Gates, Adapter, Runner, Konfiguration, Tests, `config/cost_model_v1.json`, `paper/paper_engine.py`, `01_forschung/02_strategien/s2lib.py`), Tag `voltarget-v1.0-freeze`.
4. **Startvoraussetzung:** gemeinsamer einseitiger Wochenbericht (mit Abschnitt VOLTARGET) und gemeinsamer Heartbeat aller Forward-Linien gebaut, getestet und zusammengeführt (Branch `sleeves-v1`).
5. Erst dann: enabled=true, start_bar, freeze_list, allenfalls Scheduler-Eintrag nach dem Paper-Lauf.

## 12. Offene Punkte

Die Fragen aus v0.2 §12 sind durch das Review Claude beantwortet (G2-Toleranz bestätigt; Schwellen 0.90 und 1 % p. a. bleiben gesetzt und werden durch M2 und M3 eingeordnet; Zustandsübernahme bleibt, mit symmetrischer Sync-Buchung nach M4). Offen für die Projektleitung:

1. ~~Drift-Umschichtung bei W6~~: **erledigt** durch die Präzisierung vor dem Freeze (§3.4, §3.5, Entscheid Projektleitung 2026-10-02).
2. **Heartbeat und Wochenbericht** liegen auf Branch `sleeves-v1`; Startvoraussetzung ist dessen Zusammenführung in den Hauptstand (§11).

## 13. Quellen
- Harvey, C. R., E. Hoyle, R. Korgaonkar, S. Rattray, M. Sargaison, O. Van Hemert (2018): «The Impact of Volatility Targeting». *Journal of Portfolio Management* 45(1), 14–33. DOI 10.3905/jpm.2018.45.1.014. Volltext: https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf; SSRN 3175538: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3175538 (abgerufen 2026-10-02). Verwendete Aussagen: Ziel 10 % p. a. mit Ex-post-Konstante k; EWMA der Tagesrenditen mit Mittelwert 0; Halbwertszeiten bis 90 Tage, Standard in den Abbildungen 20 Tage; 270 Handelstage Vorlauf; Schätzung 24 Stunden vor der skalierten Rendite (Renditen bis t−2); Kosten 1 Basispunkt für Aktien; Umschlag rund fünfmal bis unter einmal pro Jahr (Aktien); Sharpe-Verbesserung nur bei Risikoanlagen über den Leverage-Effekt; geringere Wahrscheinlichkeit von Extremrenditen über alle Anlageklassen; tieferer maximaler Drawdown bei US-Aktien sowie beim Balanced- und Risk-Parity-Portfolio. Exakte Tabellenwerte (Exhibits 5, 8, 11, 13, 16) sind in der abgerufenen Textfassung nicht lesbar und werden deshalb nicht zitiert.
- Moreira, A., T. Muir (2017): «Volatility Managed Portfolios». *Journal of Finance* 72(4), 1611–1644 (nur als Hintergrund, zitiert nach Harvey et al. und Ideen-Scan v2 §2.12).
- Intern: `01_forschung/12_ideen_scan/ideen_scan_v1.md` §2 und Trial-Accounting; `01_forschung/14_ideen_scan_v2/ideen_scan_v2.md` §0, §4; `paper/PAPER_PREREG_v1.0.md`; `config/cost_model_v1.json` v1.1; `00_doku/ENTSCHEIDE.md` (2026-10-01 C1, C2, 22:15, 22:35, 22:40).
