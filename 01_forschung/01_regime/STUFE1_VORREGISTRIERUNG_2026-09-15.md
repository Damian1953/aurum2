# Stufe 1 — Regime-Forschung, Vorregistrierung

**Project Aurum II. Version 1.0 vom 15.09.2026. Status: EINGEFROREN am 15.09.2026, alle vier Punkte aus Abschnitt 12 bestätigt (Schwellen unverändert, Kalenderjahre plus Halving-Zyklen, zehn Coins, F1 mitgerechnet).**

Nach der Freigabe wird dieses Dokument mit Datum und Prüfsumme eingefroren. Danach wird keine Zahl darin mehr verändert. Alle Schwellen sind a priori gesetzte Vernunftgrenzen, keine Messwerte und nicht aus Daten abgeleitet.

Grundlage ist die Stufe-1-Spezifikation der AURUM_CRYPTO_REGIME_RESEARCH_V1 vom 03.08.2026. Übernommen wird ihre Methodik vollständig. Geändert wird, was für ein System mit Long und Short auf Perpetuals nötig ist. Jede Änderung ist in Abschnitt 11 aufgeführt.

---

## 1. Frage und Nullhypothese

**Frage.** Existieren im Krypto-Tageschart Zustände, die lange genug dauern, selten genug wechseln, gegen kleine Parameteränderungen unempfindlich sind und über Coins und Zeitblöcke hinweg stabil bleiben?

**Nullhypothese.** Es existieren keine solchen Zustände. Jeder Kandidat muss sie widerlegen, indem er alle Schwellen aus Abschnitt 7 erfüllt.

**Was hier ausdrücklich nicht geschieht.** Kein Gewinn, kein Verlust, kein Sharpe, kein Drawdown, keine Handelsregel. Ein Zustand wird ausschliesslich nach seinen Zustandseigenschaften beurteilt. Es gibt keinerlei Rückkopplung aus späteren Stufen auf diese Definitionen.

---

## 2. Datengrundlage

**Quelle.** Binance Vision, Spot, Tageskerzen in USDT, ab dem jeweils ersten verfügbaren Monat, bis zum letzten abgeschlossenen Tag vor dem Rechenlauf. Geladen mit `02_daten/nachladen_historie.py`, validiert fail-closed, mit Prüfsumme in `provenance.json`.

**Assets.** Kern BTC und ETH ab 2017-08, SOL ab 2020-08. Breite: XRP, ADA, AVAX, LINK, DOT, BNB, LTC, jeweils ab Listing. Ein Coin geht nur in die Auswertung ein, wenn er nach Warmup mindestens 750 Bars liefert.

**Gegenprobe.** Kraken, Spot, USD, die letzten 720 Tage. Im Überlappungsfenster muss die Label-Übereinstimmung zwischen Binance- und Kraken-Reihe je Kandidat mindestens 90 Prozent betragen. Das ist eine Datenkonsistenz-Prüfung, kein Kandidatenkriterium. Die beiden Quellen werden nicht zu einer Reihe zusammengeführt.

**Funding.** Kraken Perpetual, stündliche relative Funding-Rate, verfügbar ab 10.09.2025 für BTC, ETH, SOL. Nur für Dimension D5, siehe Abschnitt 4.5.

**Zeitrahmen.** Tageskerzen, UTC-Tagesgrenze. Kein Intraday in Stufe 1.

**Warmup.** Jede Kennzahl mit Lookback L oder Fenster W liefert erst nach Erreichen der Mindesthistorie ein Label. Vorher gilt `undefined`, und solche Bars gehen nicht in die Statistik ein.

**Datenflags.** Extremsprünge über 400 Prozent an einem Tag, Lücken über einen Tag und Bars aus der Quarantäne werden markiert und in der Robustheitsauswertung gesondert ausgewiesen, nie stillschweigend geglättet.

**Point in time.** Zum Bar t fliesst nur Information bis einschliesslich t ein. Alle Perzentile und Extrema auf trailing Fenstern.

---

## 3. Zustandsraum, fünf orthogonale Dimensionen

| Dimension | Werte | Zweck |
|---|---|---|
| D1 Richtung | `UP` `RANGE` `DOWN` | gerichtete Persistenz, symmetrisch |
| D2 Volatilität | `SQUEEZE` `NORMAL` `EXPANSION` | Kompression und Ausdehnung |
| D3 Stress | `STRESS_DOWN` `STRESS_UP` `CALM` | Extremphasen in beide Richtungen |
| D4 Bestätigung | `CONFIRMED` `UNCONFIRMED` | Volumen, optional |
| D5 Funding | `NEG` `NEUTRAL` `POS` | Perp-eigener Zustand, reduzierte Stichprobe |

Die Dimensionen werden einzeln geprüft. Ein konsolidiertes Einzel-Label entsteht nur über die vorregistrierte Präzedenz in Abschnitt 6.

---

## 4. Variablen und Ableitungen

### 4.1 Preislage und Steigung

`MA100 = SMA(Close, 100)`, `MA200 = SMA(Close, 200)`
`dist100 = (Close − MA100) / MA100`, `above100 = Close > MA100`, `above200 = Close > MA200`
`slope100 = sign(MA100_t − MA100_{t−10})`

### 4.2 Trendstärke

`ADX14` nach Wilder, Periode 14, fix. Schwellenfamilie `adx_thr ∈ {15, 20, 25}`, je Kandidat genau ein Wert.

### 4.3 Volatilität

`ATR14` nach Wilder. `atr_norm = ATR14 / Close`. `atr_pct` = Perzentilrang von `atr_norm` im trailing Fenster `W_vol = 252`.
`BBW = (2 · 2 · SD20) / MA20` mit Stichproben-Standardabweichung. `bbw_pct` = Perzentilrang im trailing Fenster 252.

### 4.4 Drawdown und Drawup

`roll_high = max(Close, letzte 100 Bars)`, `dd = Close / roll_high − 1`, Wertebereich kleiner oder gleich null.
`roll_low = min(Close, letzte 100 Bars)`, `du = Close / roll_low − 1`, Wertebereich grösser oder gleich null.

### 4.5 Funding

`f_rel` = stündliche absolute Funding-Zahlung geteilt durch Kurs. `f_7d` = Mittel von `f_rel` über die letzten 168 Stunden, annualisiert mit Faktor 8760. Nur für Coins mit Funding-Reihe.

### 4.6 Bestätigung

`vol_pct` = Perzentilrang des Volumens im trailing Fenster 252. `vol_confirm = vol_pct ≥ 0.5`.

---

## 5. Zustandsregeln

### D1 Richtung

```
UP     falls ADX14 ≥ adx_thr und above100 = wahr   [D1b zusätzlich: slope100 = +1]
DOWN   falls ADX14 ≥ adx_thr und above100 = falsch [D1b zusätzlich: slope100 = −1]
RANGE  sonst
```

Variante D1a ohne Steigungsbedingung, Variante D1b mit. Die Richtung kommt aus der Lage zum MA100, die Stärke aus dem ADX. Das ist die einzige Stelle, an der die alte Definition ihre Long-Färbung hatte. Jetzt ist `DOWN` ein eigener Zustand mit denselben Anforderungen wie `UP`.

### D2 Volatilität

```
SQUEEZE     falls bbw_pct ≤ 0.20
EXPANSION   falls bbw_pct ≥ 0.80
NORMAL      sonst
```

Variante D2-atr verwendet `atr_pct` mit denselben Bandkanten, nur als Gegenprobe in Kandidat R5.

### D3 Stress

```
STRESS_DOWN  falls dd ≤ dd_thr  und atr_pct ≥ 0.70  und above200 = falsch
STRESS_UP    falls du ≥ du_thr  und atr_pct ≥ 0.70  und above200 = wahr
CALM         sonst
```

`dd_thr ∈ {−0.20, −0.30}`. `du_thr` ist keine freie Grösse, sondern der Drawup, der den Drawdown genau umkehrt: `du_thr = |dd_thr| / (1 − |dd_thr|)`, also 0.25 für −0.20 und 0.43 für −0.30. Damit bleibt ein einziger Freiheitsgrad, und die Definition ist in Kursverhältnissen spiegelsymmetrisch.

Drei gleichzeitige Bedingungen, damit Stress selten und eindeutig bleibt. `STRESS_UP` ist neu und beschreibt parabolische Phasen mit hoher Volatilität, die für eine Short-Seite dasselbe sind wie ein Crash für eine Long-Seite.

### D4 Bestätigung

```
CONFIRMED    falls vol_confirm
UNCONFIRMED  sonst
```

### D5 Funding

```
POS      falls f_7d ≥ +0.10
NEG      falls f_7d ≤ −0.10
NEUTRAL  sonst
```

Schwelle zehn Prozent annualisiert, gesetzt vor dem Lauf. Die eigene Messung vom 15.09.2026 zeigt 30-Tage-Fenster zwischen −10 und +17 Prozent, die Schwelle liegt also im oberen Bereich des Beobachteten und soll nur ausgeprägte Phasen markieren. D5 läuft auf rund einem Jahr Daten und wird deshalb getrennt beurteilt, siehe Kandidat F1.

---

## 6. Vorregistrierte Kandidaten

Der vollständige Kandidatenraum. Nichts anderes wird gerechnet.

| ID | D1 | D2 | D3 | D4 | adx_thr | dd_thr |
|---|---|---|---|---|---|---|
| R1 | D1a | BBW | aus | aus | 20 | – |
| R2 | D1b | BBW | an | aus | 20 | −0.30 |
| R3 | D1b | BBW | an | Volumen | 20 | −0.30 |
| R4 | D1b | BBW | an | aus | 25 | −0.30 |
| R5 | D1b | ATR | an | aus | 15 | −0.20 |
| F1 | – | – | – | – | – | Funding allein, Schwelle 0.10 |

Gegenüber V1 ist bei R4 die Relative-Strength-Bestätigung entfallen, weil sie gegen BTC definiert war und in einem System, das BTC selbst short handeln kann, keinen klaren Sinn mehr hat.

### Konsolidiertes Einzel-Label, Präzedenz

```
1. STRESS_DOWN oder STRESS_UP
2. EXPANSION
3. UP oder DOWN  (D2 ungleich EXPANSION)
4. SQUEEZE       (D1 = RANGE)
5. RANGE
```

---

## 7. Robustheitsmetriken und Hard-Fail-Schwellen

Ein Kandidat gilt als **TAUGLICH**, wenn er alle Schwellen erfüllt. Eine Verfehlung genügt für **VERWORFEN**.

| Metrik | Schwelle |
|---|---|
| Median-Verweildauer, häufige Zustände (UP, DOWN, RANGE, NORMAL, CALM) | ≥ 10 Bars |
| Median-Verweildauer, seltene Zustände (STRESS, EXPANSION, SQUEEZE) | ≥ 5 Bars |
| Anteil Ein-Bar-Episoden je Dimension | ≤ 25 % |
| Wechsel je 252 Bars, D1 | ≤ 30 |
| Wechsel je 252 Bars, D2 | ≤ 30 |
| Wechsel je 252 Bars, D3 | ≤ 12 |
| Jitter-Übereinstimmung, Mittel über alle Einzel-Jitter | ≥ 85 % |
| Jitter-Übereinstimmung, schlechtester Einzel-Jitter | ≥ 75 % |
| Coin-Abdeckung | BTC und ETH und Mehrheit der übrigen Coins |
| Zeitblock-Abdeckung | Schwellen in ≥ 70 % der Blöcke, keine Kennzahl weicht in einem Block um mehr als Faktor 2 vom Median über die Blöcke ab |

Die D1-Grenze liegt bei 30 statt 26, weil drei Zustände eine zusätzliche Grenze haben, an der gewechselt werden kann. Das ist eine bewusste, vorab gesetzte Anpassung.

**Jitter-Stufen.** `adx_thr ±2`, Bandkanten `±0.05`, `dd_thr ±0.05` (und damit `du_thr` mitlaufend), MA100 → {90, 110}, `W_vol` → {189, 315}, Funding-Schwelle `±0.025`.

**Zeitblöcke, primär.** Nicht überlappende Kalenderjahre 2018 bis 2025, dazu 2026 als Teilblock, falls mindestens 200 Bars vorliegen.

**Zeitblöcke, Gegenprobe.** Halving-Zyklen, weil sie durch das Protokoll und nicht durch den Kurs bestimmt sind: 2017-08 bis 2020-05, 2020-05 bis 2024-04, 2024-04 bis heute.

**Interne Konsistenz.** Überlappung der EXPANSION-Bars zwischen `atr_pct` und `bbw_pct` ≥ 60 Prozent. Verfehlung ist ein Warnhinweis, kein Hard-Fail.

**Kandidat F1** wird nur auf BTC, ETH, SOL und nur ab 10.09.2025 geprüft. Es gelten Verweildauer ≥ 5 Bars, Ein-Bar-Anteil ≤ 25 Prozent, Wechsel ≤ 30 je 252 Bars, Jitter ≥ 85 und ≥ 75 Prozent. Zeitblöcke und Coin-Mehrheit entfallen wegen der kurzen Historie. Ein Bestehen von F1 wird als **VORLÄUFIG TAUGLICH** geführt und muss nach einem weiteren Jahr Daten wiederholt werden.

---

## 8. Ablauf des Rechenlaufs

1. Prüfsummen der Eingabedateien aus `provenance.json` in das Laufprotokoll übernehmen.
2. Je Coin alle Variablen aus Abschnitt 4 berechnen, strikt trailing.
3. Je Kandidat und Coin die Labels je Bar erzeugen, `undefined` im Warmup.
4. Je Kandidat, Dimension, Coin und Zeitblock die Metriken aus Abschnitt 7 berechnen.
5. Jitter-Varianten rechnen und jede einzelne in `stage1_config_log.csv` eintragen.
6. Hard-Fail-Tabelle mechanisch auswerten. Kein Ermessen.
7. Bericht schreiben, taugliche Definitionen einfrieren.

Der Lauf erfolgt in der Claude-Umgebung auf einer Kopie der Rohdaten. Ergebnisse werden in diesen Ordner zurückgeschrieben.

---

## 9. Ergebnisdateien

- `frozen_regimes_v1.json` — taugliche Definitionen mit allen Parametern, Präzedenz, Prüfsummen der Eingaben, Datum des Einfrierens
- `stage1_labels/{coin}.csv` — je Bar das Tupel (D1, D2, D3, D4, D5) und das konsolidierte Label
- `stage1_robustness_report.md` — alle Metriken je Kandidat, Coin, Block, mit Hard-Fail-Tabelle und Urteil
- `stage1_config_log.csv` — jede gerechnete Konfiguration inklusive Jitter
- `stage1_summary.md` — Fazit in Klartext, auch bei «kein Kandidat tauglich»

---

## 10. Freeze-Protokoll

Taugliche Definitionen werden mit exakten Parametern eingefroren und erhalten die Versionsnummer 1. Jede spätere Änderung erzeugt Version 2 und macht alle darauf aufbauenden Stufe-3-Ergebnisse ungültig. In Stufe 3 wird der Filter nicht an Handelsperformance nachgezogen.

Besteht kein Kandidat, ist die Nullhypothese nicht widerlegt. Das wird als gültiges Ergebnis dokumentiert. Stufe 2 läuft dann ohne Regimefilter, und Stufe 3 entfällt.

---

## 11. Änderungen gegenüber der Spezifikation vom 03.08.2026

1. D1 ist dreiwertig und symmetrisch. `DOWN` ist ein eigener Zustand.
2. D3 hat mit `STRESS_UP` einen gespiegelten Zustand. `du_thr` ist aus `dd_thr` abgeleitet, kein zusätzlicher Freiheitsgrad.
3. D5 Funding ist neu. Sie ist die einzige Dimension, die es auf Spot nicht gibt, und läuft als getrennter Kandidat F1 auf reduzierter Stichprobe.
4. Relative-Strength-Bestätigung gegen BTC ist entfallen.
5. D1-Wechselgrenze 30 statt 26 wegen des dritten Zustands.
6. Datenquelle ist Binance Vision für die lange Historie, Kraken nur als Gegenprobe. Beide werden nicht zusammengeführt.
7. Zeitblöcke sind konkret festgelegt: Kalenderjahre primär, Halving-Zyklen als Gegenprobe.
8. Ein Coin braucht mindestens 750 Bars nach Warmup.

Der Guardrail «Long/Flat Spot, kein Short, kein Leverage» aus V1 gilt für Aurum II nicht mehr. Für Stufe 1 hat das keine Auswirkung, weil hier nicht gehandelt wird.

---

## 12. Vor dem Einfrieren zu bestätigen

Diese vier Punkte sind Entscheidungen, keine Messungen. Sie werden vor dem ersten Rechenlauf bestätigt und danach nicht mehr verändert.

1. Schwellen in Abschnitt 7 so belassen oder vorab anders setzen.
2. Zeitblöcke: Kalenderjahre primär, Halving-Zyklen als Gegenprobe.
3. Universum: Kern BTC, ETH, SOL, Breite XRP, ADA, AVAX, LINK, DOT, BNB, LTC.
4. D5 Funding als Kandidat F1 mitführen oder auf Stufe 4 verschieben.

Nach Bestätigung: Datum, Prüfsumme dieses Dokuments und Prüfsummen der Eingabedaten in `00_doku/ENTSCHEIDE.md` eintragen. Dann beginnt der Rechenlauf.
