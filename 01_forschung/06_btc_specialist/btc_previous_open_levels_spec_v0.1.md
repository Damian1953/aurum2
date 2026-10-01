# BTC Previous-Open Levels — Spezifikation, Version 0.1

**Project Aurum II, Strang 06_btc_specialist, Teil von BTC YAMATO RTC (`01_forschung/06_btc_specialist/`). 17.09.2026. Status: Spezifikation zur Prüfung. Kein Rechenlauf. Quellenregel dieses Strangs: Hypothesenbildung ausschliesslich aus japanischen `.jp`-Quellen.**

## 0. Hypothese und Quellenlage

Japanische Price-Action-Praxis führt die Eröffnungskurse abgeschlossener Perioden (前日始値, 前週始値, 前月始値) als Referenzniveaus, an denen sich Handel verdichtet, und liest eine überzeugende Rückeroberung (Reclaim) eines solchen Niveaus als Stärke. Die `.jp`-Belege dafür sind praktischer, nicht wissenschaftlicher Art: Indikatoren, die genau diese Niveaus zeichnen (GogoJungle, «前日の始値／終値、先週の始値／終値、先月の始値／終値»), und Marktberichte, die Wochen- und Monatseröffnungen als Bezugspunkte nennen. Eine statistische Prüfung auf BTC ist uns aus `.jp`-Quellen nicht bekannt. Die Hypothese wird deshalb als offen geführt und in der Discovery erstmals geprüft, nicht als gesichert vorausgesetzt.

## 1. Deterministische Niveaus, alle point-in-time

Alle Perioden in UTC, identisch zu den Rohdaten (Tag ab 00:00, Woche ab Montag 00:00, Monat ab dem Ersten 00:00). «Aktuelle Periode» ist die Periode, in der die Kerze t liegt, ihre Eröffnung ist ab der ersten Kerze der Periode bekannt. «Vorige Periode» ist die letzte vollständig abgeschlossene.

| Niveau | Definition, Stand Kerze t (4h) | Bekannt ab |
|---|---|---|
| `open_4h_prev` | O_{t−1} | Schluss t−1 |
| `open_d_cur` | Eröffnung der 4h-Kerze 00:00 des laufenden UTC-Tages | Kerze 00:00 |
| `open_d_prev` | Eröffnung des vorigen UTC-Tages | Vortag 00:00 |
| `open_w_cur` | Eröffnung Montag 00:00 der laufenden Woche | Montag 00:00 |
| `open_w_prev` | Eröffnung der vorigen Woche | vorige Woche |
| `open_m_cur` | Eröffnung des Ersten 00:00 des laufenden Monats | Monatsbeginn |
| `open_m_prev` | Eröffnung des vorigen Monats | voriger Monat |

Aus den Tageskerzen abgeleitete Niveaus (Wochen- und Monatseröffnung) werden aus den 4h-Kerzen gebildet, nicht aus den Tagesdateien, damit Quelle und Raster identisch sind. Für die Tagesebene dieselbe Tabelle mit Tageskerzen.

Merkmale je Niveau L: `dist_L_atr` = (C_t − L) / ATR14_{t−1}, `above_L` = 1 wenn C_t > L, `bars_below_L` = Anzahl aufeinanderfolgender Kerzen bis t−1 mit Schluss unter L.

## 2. Reclaim und Verlust eines Niveaus

`reclaim_L_t` = 1, wenn C_{t−1} ≤ L, C_t > L + 0.10 · ATR14_{t−1} und `bars_below_L` ≥ 3 (der Preis war mindestens einen halben Tag unter dem Niveau, die Rückeroberung ist kein Rauschen). `reclaim_strong_L_t` = `reclaim_L_t` und `close_location_t` ≥ 0.60 und `body_atr_t` ≥ 0.50 (überzeugender Reclaim, die Kerze schliesst stark). `loss_L_t` spiegelbildlich (C_{t−1} ≥ L, C_t < L − 0.10 · ATR, mindestens 3 Kerzen darüber).

Puffer 0.10 ATR, Mindestdauer 3 Kerzen, Schwellen 0.60 und 0.50 sind vorab gesetzt, für alle Niveaus gleich, nicht optimiert. Jitter 0.05 und 0.20 ATR nur als Robustheit.

## 3. Verwendung in YAMATO

Als Bestätigungs-Trigger TC: Nach einem Bottom Candidate gilt der Einstieg als bestätigt, wenn innerhalb der nächsten sechs 4h-Kerzen ein `reclaim` von `open_d_prev` oder `open_w_prev` eintritt (das nächsthöhere der beiden über dem Kandidatenschluss, vorab so definiert, nicht das «passendere»). Einstieg zur Eröffnung der Folgekerze. Als Hold-Bedingung: `above_open_w_prev` als Strukturmerkmal (die Position gilt als in intaktem Trend, solange die Wocheneröffnung der Vorwoche hält, berichtet, in der Hold-Regel als eine von drei Bedingungen, Abschnitt G des Forschungsplans). Als Peak-Kontext: `loss_open_w_cur` nach Peak-Evidenz als Berichtswert.

## 4. Informationswert-Test (Discovery-Fenster, kein Strategietest)

Für jedes Niveau: Ereignisstudie der Folgerendite nach `reclaim` und `reclaim_strong` über 6, 18, 42 Kerzen gegen unbedingt, und Anteil der Berührungen (Kerze mit L innerhalb der Range), nach denen der Schluss auf der Seite bleibt, auf der die Kerze eröffnete (Halte-Quote), gegen die Halte-Quote zufälliger Niveaus gleicher Distanz (Kontrolle, weil jedes Niveau in der Nähe des Preises «hält», wenn die Volatilität klein ist). Block-Bootstrap, Holm über Niveaus mal Horizonte. Nur wenn die Halte-Quote eines Niveaus die der Zufallskontrolle nach Holm übersteigt, gilt das Niveau als informativ. Das Ergebnis ändert keine Regel, es entscheidet, welche Niveaus als Vorregistrierungs-Hypothese in die Validation gehen.

## 5. Look-ahead

Alle Niveaus sind Eröffnungen, die per Definition zu Periodenbeginn bekannt sind. Die einzige Falle ist die Zuordnung: Die Wocheneröffnung «der laufenden Woche» darf erst ab Montag 00:00 verwendet werden, nie für Kerzen des Sonntags. Der Look-ahead-Test permutiert die Kerzen nach t und verlangt unveränderte Niveaus bis t.

## 6. Offene Entscheidungen

1. Reclaim-Puffer 0.10 ATR und Mindestdauer 3 Kerzen bestätigen.
2. TC-Fenster sechs Kerzen bestätigen.
3. Ob `open_4h_prev` in den Tests bleibt (Empfehlung: nur Bericht, zu nah am Preis, um Information zu tragen).
4. Ob die Zufallskontrolle der Halte-Quote mit gleicher Distanz oder gleicher Distanzverteilung gezogen wird (Empfehlung: gleiche Distanz je Ereignis).
