# XS21 Point-in-Time v1.0: Bericht zum einzigen Lauf

Stand: 01.10.2026, Zürich. Verfasser: Grok Bot (Aurum II Review). Evidenzklasse: **«Discovery/Robustheit mit Vorbelastung»** (§3). Das ist keine Validation. Der Teil ab 2024 ist für XS21 verbraucht, B3 entscheidet nicht mit.

## 0. Urteil auf einen Blick

| Test | Urteil (Stufe-2-Regel) | verfehlt | CAGR K1 | Sharpe K1 | MaxDD K1 | Holm-p |
|---|---|---|---|---|---|---|
| U1 Top-3 L+S (Forschungsfrage) | **TEILWEISE** | c3 (B2 < 0), c6 (MaxDD) | 31.7 % | 0.75 | −87.3 % | 0.042 |
| U2 Top-3 L+S (Handelbarkeit) | **TEILWEISE** | c6 (MaxDD) | 41.3 % | 0.81 | −75.9 % | 0.042 |

TEILWEISE heisst nach Stufe 2 (Prereg v1, Z. 370): «wird nicht als Edge gewertet». Beide Tests gelten damit als **nicht bestanden**. Nach der eingefrorenen Lesart in §5.3 (Zeile «besteht nicht / besteht nicht») lautet der Befund: **H-C2 auf PiT falsifiziert. Kein Sleeve.**

Einordnung, ohne die Lesart zu ändern: Beide Tests scheitern **nicht** an der Survivorship. Der Fall «besteht nur mit den Überlebenden» tritt nicht ein. Sie scheitern am Risikokriterium c6, U1 ausserdem an B2. Die Ertrags- und Statistikkriterien c1, c5, c7 und c8 sind in beiden Universen erfüllt. Die Spezifikation unterscheidet nicht nach dem Grund des Scheiterns, deshalb gilt die Lesart wie eingefroren.

## 1. Ablauf nach Governance

| Schritt | Zeit (Zürich) | Nachweis |
|---|---|---|
| Freigabe Damian | 01.10.2026 13:07 | ENTSCHEIDE «XS21 PiT v1.0 FREEZE» |
| Freeze Spec, B7 v1.0, Kostenmodell, T-Bill | vor jeder Datenbeschaffung | Commit `0f6aed9`, Tag `xs21-pit-v1.0-freeze`, `00_doku/xs21_freeze_2026-10-01_expected_shas.txt` |
| Datenbeschaffung, Laufbeginn M6, Freeze Lauf-Code | vor dem Lauf | Commit `1eb1b8a`, Tag `xs21-pit-v1.0-runcode`, `00_doku/xs21_runcode_2026-10-01_expected_shas.txt` |
| Korrekturvermerk ENTSCHEIDE (Dateinamen) | 13:39, vor dem Lauf | Commit `3e19223` |
| **Einziger Lauf** | 13:39:37 – 13:43:45 | `run/xs21_run.log`, Spec-SHA `edb24cde…98af` im Log (E3) |
| Unabhängige Nachprüfung, Nachträge | ab 13:44 | `run/xs21_check.json`, `run/xs21_check_erklaerung.json`, `run/xs21_nachtrag_survivorship_bloecke.json` |

Nach dem Freeze wurde kein Code des Laufs geändert. Es gab keinen Abbruch und keine Wiederholung.

## 2. Daten und Eingaben

- **Quelle:** ausschliesslich `data.binance.vision` (USD-M), öffentlich. Kein `fapi`, der Geoblock HTTP 451 wurde nicht umgangen.
- **Umfang:** 673 Symbole einschliesslich der delisteten. Monats-Klines 1d: 20'547. Tages-Klines 2026-09-01..15: 9'660. Funding-Monate: 19'956.
- **Prüfsummen:** Alle 50'163 ZIPs gegen die `.CHECKSUM` des Archivs geprüft, 0 Abweichungen.
- **Ablage der Nachweise:** `daten/xs21_zips_v1.0.sha256` (0dc79a6e…), Provenienz `daten/xs21_provenance_v1.0.jsonl.gz` (0614ef23…), Original `data/xs21/provenance.jsonl` (539cf631…).
- **Fehlendes Funding im Archiv:** 38 Symbol-Monate mit Handel fehlen.
  - BNX 2022-04..2023-01, ICP 2021-05..2022-06, TLM 2021-07..2022-06, JUP 2024-01, QTUM 2020-02.
  - Weitere 1'226 fehlende Monate liegen nach dem Handelsende und sind ohne Belang.
  - Kein STOPP, weil die eingefrorene Regel M4 genau diesen Fall regelt: Füllung mit dem adversen Median.
- **Laufbeginn M6:** 2020-04-04. Bestimmt vor dem Lauf nur aus Listing und Volumen, `run/xs21_laufbeginn.json` 4a012b94….
- **Raster:** 337 Stichtage, 2020-04-04 bis 2026-09-12. Auswertung bis 2026-09-14, 2'355 Tage.
- **Universen:**
  - U1: 21 bis 494 Symbole, Median 172.
  - U2: immer 20 Symbole (Top 20 nach Vormonatsvolumen, §2.3).
  - Cash-Stichtage nach M6: 0.
  - Lebensenden: 169. Delistete Symbole: 157. Relistings: 12. Überbrückte Lückentage: 247.
- **Eingaben im Log:**
  - Spec edb24cde…, B7 7f68fe16…, Sensitivitätsliste c0a8f32d…, Universum f5563c09…, Snapshot bff906a0…;
  - T-Bill 8b287e3c…, Kostenmodell c652caa5…, Provenienz 539cf631…;
  - Lib deca0c29…, Lauf 48370287…, s2lib 54590393….

## 3. Ergebnisse je Primärtest (K1, nach Kosten)

«Erwartung» bedeutet den Netto-Ertrag je Trade in Prozent des Portfoliokapitals. Eine Position hat 1/6 Gewicht. Die Blöcke werden nach Einstiegsdatum zugeordnet (M5).

### 3.1 Kriterien

| Kriterium | U1 Top-3 L+S | U2 Top-3 L+S |
|---|---|---|
| c1 Erwartung > 0 und CAGR > Cash (2.9 % p.a.) | ja: 0.302 %, 31.7 % | ja: 0.223 %, 41.3 % |
| c3 Erwartung B1 > 0 und B2 > 0 (M5) | **nein**: B1 +0.788 % (n 306), B2 **−0.085 %** (n 405) | ja: B1 +0.583 % (n 260), B2 +0.038 % (n 295) |
| B3 (nur berichtet) | +0.317 % (n 550) | +0.128 % (n 410) |
| c4 Jitter (≥ 2/3 Erwartung > 0, Sharpe ≤ 1.5 × Median, Median > 0) | ja: 4/4 positiv, Median-Sharpe 0.71 | ja: 4/4 positiv, Median-Sharpe 0.77 |
| c5 ≥ 100 Trades | ja: 1'261 | ja: 965 |
| c6 MaxDD ≥ MaxDD EP | **nein**: −87.3 % gegenüber −53.5 % | **nein**: −75.9 % gegenüber −52.0 % |
| c7 Alpha- oder Risikotest | ja: ALPHA, α 81.7 % p.a., t 1.98, p 0.024, β −0.04 | ja: ALPHA, α 59.3 % p.a., t 2.20, p 0.014, β −0.06 |
| c8 Bootstrap-p5 > 0 und Holm-p < 0.05 | ja: p5 0.158, p 0.021, Holm 0.042 | ja: p5 0.104, p 0.022, Holm 0.042 |
| Robust unter K2 | ja: CAGR 12.2 %, Sharpe 0.60 | ja: CAGR 24.7 %, Sharpe 0.63 |
| **Urteil** | **TEILWEISE** | **TEILWEISE** |

Holm über die zwei Primärtests: Die Roh-p-Werte sind 0.021 und 0.022, daraus folgt Holm-p 0.042 für beide.

### 3.2 Kennzahlen

| | U1 L+S | U2 L+S |
|---|---|---|
| CAGR K0 / K1 / K2 | 36.1 % / 31.7 % / 12.2 % | 44.8 % / 41.3 % / 24.7 % |
| Sharpe K1 (Bootstrap-KI) | 0.75 (0.15 – 1.35) | 0.81 (0.15 – 1.44) |
| MaxDD K1 | −87.3 % | −75.9 % |
| Volatilität p.a. | 106 % | 71 % |
| Sortino / Calmar | 1.06 / 0.36 | 1.05 / 0.54 |
| schlechtestes Jahr / schlechteste 12 Monate | −31.5 % / −66.0 % | −15.4 % / −53.2 % |
| Trefferquote | 48.5 % | 48.9 % |
| DSR (2 Versuche, Sensitivität) | 0.973 | 0.978 |
| Trade-Bootstrap p5 der Erwartung | −0.109 % | −0.152 % |
| Benchmark EP: CAGR / Sharpe / MaxDD | 17.2 % / 0.52 / −53.5 % | 8.8 % / 0.34 / −52.0 % |
| Benchmark EW-Universum: CAGR / MaxDD | 11.0 % / −91.4 % | −5.2 % / −94.5 % |
| Delisting-Ausstiege (K2-Reibung) | 17 | 2 |

**Jahresrenditen K1**

| Test | 2020 (ab 04.04.) | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (bis 14.09.) |
|---|---|---|---|---|---|---|---|
| U1 | +102.0 % | −31.5 % | −24.4 % | −14.0 % | +21.0 % | +63.0 % | +233.7 % |
| U2 | +74.0 % | +36.0 % | −1.0 % | +12.3 % | −15.4 % | −8.5 % | +355.8 % |

Ohne 2026, also bis 31.12.2025 (deskriptiver Nachtrag):

| Test | CAGR | Sharpe | MaxDD |
|---|---|---|---|
| U1 | 10.5 % | 0.56 | −80.3 % |
| U2 | 13.2 % | 0.52 | −75.9 % |

Ein grosser Teil des Gesamtertrags stammt aus 2026, also aus dem verbrauchten Zeitraum.

### 3.3 Survivorship-Zerlegung (§5.3)

Die Beiträge sind in Einheiten des Portfoliokapitals angegeben. «Tag» ist die Summe der Tagesbeiträge (Brutto + Funding − Kosten), «Trades» die Summe der Trade-Erträge.

**Stand 2026-09-14** (aus dem Lauf):

| | U1 überlebend | U1 delistet | U2 überlebend | U2 delistet |
|---|---|---|---|---|
| Trades (n) | 924 | 337 | 853 | 112 |
| Summe Trades | +2.889 | +0.921 | +2.306 | −0.152 |
| Erwartung je Trade | +0.313 % | +0.273 % | +0.270 % | −0.136 % |
| Summe Tagesbeiträge | +3.662 | +1.645 | +3.922 | −0.071 |
| gehandelte Symbole | 302 | 92 | 171 | 34 |

**Stand 2023-12-31** (nur bis 2023-12-31):

| | U1 überlebend | U1 delistet | U2 überlebend | U2 delistet |
|---|---|---|---|---|
| Trades (n) | 652 | 59 | 539 | 16 |
| Summe Trades | +2.131 | −0.066 | +1.799 | −0.173 |
| Erwartung je Trade | +0.327 % | −0.112 % | +0.334 % | −1.079 % |
| Summe Tagesbeiträge | +1.467 | −0.242 | +1.555 | −0.137 |

**Je Block, Stand 2026-09-14** (Nachtrag aus den Trades: Summe Trades und n, siehe Abweichung A6):

| Block | U1 überlebend | U1 delistet | U2 überlebend | U2 delistet |
|---|---|---|---|---|
| B1 | +2.209 (216) | +0.202 (90) | +1.740 (227) | −0.225 (33) |
| B2 | −0.219 (266) | −0.127 (139) | +0.050 (232) | +0.062 (63) |
| B3 | +0.899 (442) | +0.845 (108) | +0.516 (394) | +0.011 (16) |

Lesart:
- **U1:** Auch die delisteten Symbole tragen über den ganzen Zeitraum positiv bei. Der Effekt hängt also nicht an den Überlebenden. Das Scheitern von U1 an B2 betrifft beide Gruppen.
- **U2:** Die delisteten Symbole tragen leicht negativ bei (−0.15 bei 112 Trades). Die Überlebenden tragen den Ertrag. U2 besteht aber auch mit ihnen nicht, weil c6 scheitert.
- Der Fall «besteht nur mit den Überlebenden» (§5.3) tritt in keinem Universum ein.

### 3.4 Gefülltes Funding (M4)

| | Long gefüllt | Short gefüllt | Ersatz 30-Tage-Median (§8.3) | Vorbehalt (> 5 %) |
|---|---|---|---|---|
| U1 | 221 von 32'097 = **0.69 %** | 282 von 29'604 = **0.95 %** | 13 | nein |
| U2 | 130 von 22'632 = **0.57 %** | 62 von 27'870 = **0.22 %** | 76 | nein |

Das Funding ist ein grosser Ertragsteil: In U1 beträgt die Summe +2.21 (Long-Bein +2.01), in U2 +0.47. Das Vorzeichen ist an den Rohdaten geprüft. Beispiel TRB, September 2023: Die Funding-Summe über 7 Tage war −0.41, der Long erhält. Die Gewinner-Coins mit Short-Squeeze haben oft stark negatives Funding. Unter K2 (Funding-Zahlungen × 1.5) sinkt das Funding in U2 auf −0.05.

## 4. Vorregistrierte Vergleiche (keine Primärtests, keine Auswahl)

| Variante | CAGR K1 | Sharpe | MaxDD | Trades | Erwartung | B1 | B2 | B3 |
|---|---|---|---|---|---|---|---|---|
| U1 L42 | 140.8 % | 1.36 | −58.7 % | 937 | 0.871 % | +1.183 % | −0.052 % | +1.400 % |
| U1 L63 | 17.9 % | 0.58 | −69.5 % | 839 | 0.201 % | +0.492 % | +0.076 % | +0.142 % |
| U1 Top-2 | −6.6 % | 0.74 | −98.4 % | 899 | 0.848 % | +1.067 % | −0.211 % | +1.551 % |
| U1 Top-4 | 28.7 % | 0.68 | −78.6 % | 1'629 | 0.144 % | +0.463 % | −0.081 % | +0.129 % |
| U2 L42 | 58.8 % | 0.95 | −60.7 % | 795 | 0.312 % | +0.829 % | −0.180 % | +0.396 % |
| U2 L63 | 32.2 % | 0.70 | −77.7 % | 635 | 0.336 % | +0.768 % | −0.189 % | +0.465 % |
| U2 Top-2 | 26.5 % | 0.72 | −92.1 % | 726 | 0.221 % | +0.570 % | −0.045 % | +0.199 % |
| U2 Top-4 | 39.4 % | 0.81 | −65.9 % | 1'176 | 0.155 % | +0.437 % | +0.015 % | +0.076 % |
| U1 Long-only | 42.6 % | 0.97 | −97.8 % | 570 | 1.436 % | +5.514 % | −0.570 % | +0.692 % |
| U2 Long-only | 34.8 % | 0.78 | −91.7 % | 464 | 0.829 % | +3.430 % | −0.527 % | +0.022 % |
| U1 Dezil L+S | 15.1 % | 0.48 | −57.3 % | 7'893 | 0.027 % | +0.328 % | −0.032 % | +0.005 % |
| U1 ohne 11 B7-Sensitivitätssymbole | 32.1 % | 0.75 | −87.3 % | 1'261 | 0.304 % | +0.788 % | −0.085 % | +0.320 % |
| U2 ohne 11 B7-Sensitivitätssymbole | 41.3 % | 0.81 | −75.9 % | 965 | 0.223 % | +0.583 % | +0.038 % | +0.128 % |

Befunde:
- **B2 ist schwach.** Das positive B2 von U2 (+0.038 %) ist knapp. In 3 der 4 U2-Jitter-Varianten ist B2 negativ, ebenso in Long-only und im U1-Dezil. B2 (2022–2023) ist über fast alle Varianten der schwache Block.
- **B7-Sensitivität ohne Einfluss:** Die 11 Symbole wurden nie oder nur unwesentlich gehandelt.

## 5. Unabhängige Prüfungen

| Prüfung | Ergebnis |
|---|---|
| Spec-SHA im Lauf-Log (E3) | ok, `edb24cde…98af` |
| U2 ⊆ U1 an jedem Stichtag | ok: im Lauf-Code (Abbruchbedingung) und unabhängig aus `xs21_universen.csv` |
| Kein Lookahead | Auswahl = Top/Bottom-3 nach `ret(21)` aus den Schlusskursen T und T−21 der Roh-ZIPs, unabhängig neu berechnet. Gewichte ändern sich nur ab T+1 (Eröffnung) oder nach einem Delisting (Prüfung im Lauf). |
| Auswahl unabhängig neu berechnet | 0 Abweichungen mit U5a. Das eingefrorene Prüfskript meldet 30 (U1) und 8 (U2), weil es U5a (Kerzen mit count = 0) nicht anwendet. Mit U5a passen alle (`run/xs21_check_erklaerung.json`). |
| Brutto aus unabhängig rekonstruierten Gewichten | max. Abweichung je Tag 2·10⁻¹⁶ (U1) und 1·10⁻¹⁶ (U2); Summen gleich |
| Bilanzidentität netto = Brutto + Funding + Cash − Kosten | max. Abweichung 3·10⁻¹⁶ |
| Kosten K1 | Die Differenz Lauf minus unabhängig beträgt 0.001133 (U1) und 0.000133 (U2). Das entspricht exakt 17 bzw. 2 Delisting-Ausstiegen × 1/6 × (0.0006 − 0.0002) K2-Reibung nach §2.5. Erklärt. |
| Gefülltes Funding | Anteile siehe 3.4, alle unter 5 % |
| Extremtage | Die grössten Tagesbewegungen, z.B. +95 % am 07.06.2022 und −60 % am 28.01.2021, sind echte Ereignisse in den Rohkerzen, keine Artefakte: UNFI +450 % Eröffnung zu Eröffnung, DOGE +390 %, ALPACA-Delisting-Pump +520 % am 30.04.2025. |

`xs21_check.json` enthält `gesamt_ok: false`. Das liegt an den zwei erklärten Punkten oben. Das eingefrorene Prüfskript bleibt unverändert, die Erklärung steht in einem eigenen Nachtragsskript.

## 6. Abweichungen und Festlegungen

| Nr. | Art | Inhalt |
|---|---|---|
| A1 | vorregistriert (M7) | Signal auf Perp-Kerzen statt Spot wie in Stufe 2 |
| A2 | Festlegung vor dem Lauf (U5a) | Kerzen mit count = 0 gelten als nicht vorhanden. Das Archiv führt delistete Symbole im Status SETTLING mit 54'122 flachen Kerzen weiter. |
| A3 | Datenlücke, nach M4 behandelt | 38 Symbol-Monate Funding fehlen im Archiv (siehe 2). Füllanteil unter 1 %, kein Vorbehalt. |
| A4 | M6 | Laufbeginn 2020-04-04 statt 2020-02-01. B1 beginnt am Laufbeginn. |
| A5 | Dokumentationspanne vor dem Lauf | Im ENTSCHEIDE-Eintrag 13:37 fehlten durch einen Shell-Fehler die Dateinamen. Korrekturvermerk 13:39, vor dem Lauf. SHAs und Inhalt waren nicht betroffen. |
| A6 | Lücke im Lauf-Code, Nachtrag | §5.3 verlangt die Survivorship-Zerlegung auch je Block. Der Lauf gab sie nur für den Gesamtzeitraum und per 2023-12-31 aus. Die Zerlegung je Block wurde nach dem Lauf deskriptiv aus den Trades nachgetragen (`tools/xs21/nachtrag_survivorship_bloecke_v1.py`). Die Gesamtsummen stimmen mit dem Lauf überein. Kein Einfluss auf das Urteil. |
| A7 | Prüfskript | U5a fehlt im Prüfskript, siehe 5. Erklärt, kein Fehler im Lauf. |
| A8 | Bugfix vor dem Freeze des Lauf-Codes | Nach dem Lebensende gilt Cash bis zum nächsten Rebalancing, keine Wiederaufnahme bei Relisting. Gefunden im synthetischen Test, vor dem Tag `xs21-pit-v1.0-runcode`. Keine Abweichung nach dem Freeze. |
| A9 | Hinweis zur Konvention (U9, wie Stufe 2) | Tagesrendite = konstantes Gewicht × Tagesrendite. Das entspricht einer impliziten täglichen Rückführung auf 1/6, ohne Kosten für diesen Umsatz. Der Trade-Ertrag ist dagegen Buy-and-Hold über die Haltedauer. Bei extremen Coins weicht das stark ab: U1 2026 hat Tagesbeiträge von +2.27, die Trades nur −0.14; U2 2025 +0.50 gegenüber −0.67. CAGR, Sharpe, MaxDD und Bootstrap beruhen auf der Tageskonvention, die Erwartung je Trade und c3 auf den Trades. Das ist keine Abweichung, aber ein wesentlicher Vorbehalt für die Lesart der Renditezahlen. |

Es gab nach dem Freeze keine Codeänderung, keinen zweiten Lauf und keine Änderung der Spezifikation.

## 7. Was es bedeutet (Kurzfassung in 5 Sätzen)

1. Im einzigen eingefrorenen Lauf auf einem Universum ohne Survivorship-Verzerrung (2020-04 bis 2026-09, 673 Symbole einschliesslich der delisteten) erreichen beide Tests nur TEILWEISE: positive Erwartung, Signifikanz nach Holm (p = 0.042) und Alpha, aber Drawdowns von −87 % (U1) und −76 % (U2), weit tiefer als die Passivposition (−54 % bzw. −52 %).
2. Nach der eingefrorenen Regel gilt TEILWEISE nicht als Edge; damit ist H-C2 auf Point-in-Time als falsifiziert zu lesen, und es gibt keinen Sleeve-Kandidaten.
3. Die Survivorship ist nicht der Grund: Delistete Symbole tragen in U1 sogar positiv bei, und in U2 ist ihr negativer Beitrag klein.
4. Der Ertrag ist sehr ungleich verteilt: Er hängt an wenigen extremen Squeeze- und Delisting-Ereignissen, an viel negativem Funding auf Gewinner-Coins und zu einem grossen Teil am verbrauchten Jahr 2026, während der Block 2022–2023 schwach bis negativ ist.
5. Für ein Privatkonto ist das kein handelbarer Effekt; eine weitere Prüfung wäre nur über eine neue, vorab registrierte Fragestellung (z.B. Risikobegrenzung) und das Forward-Fenster möglich, nicht über diesen Lauf.

## 8. Dateien

- Spezifikation: `01_forschung/09_lane_c/xs21_point_in_time_prereg_v1.0.md` (EINGEFROREN, edb24cde…)
- Umsetzung: `01_forschung/09_lane_c/xs21_pit_v1.0/xs21_pit_umsetzung_v1.0.md`
- Code: `xs21_pit_v1.0/xs21_pit.py`, `xs21_pit_v1.0/xs21_pit_run.py`
- Lauf-Ausgaben: `01_forschung/09_lane_c/xs21_pit_v1.0/run/` (SHAs in `00_doku/xs21_run_2026-10-01_expected_shas.txt`)
- Prüfung: `tools/xs21/check_run_v1.py`; Nachträge `tools/xs21/check_run_v1_erklaerung.py` und `tools/xs21/nachtrag_survivorship_bloecke_v1.py`
- Kopie dieses Berichts: `/workspace/aurum2/fuer_claude/xs21_pit_v1.0_bericht.md`
