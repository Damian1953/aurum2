# BTC Sakata Bottom- und Peak-Spezifikation, Version 0.1

**Project Aurum II, Strang 06_btc_specialist, Teil von BTC YAMATO RTC. 17.09.2026. Status: Spezifikation zur Prüfung. Kein Rechenlauf. Quellenregel: Hypothesenbildung ausschliesslich aus `.jp`-Quellen. Baut auf der Candlestick and Flow Feature Library v0.1 auf (Geometrie, Swing-Struktur, Failed Breakdown), definiert die Sakata-Mehrkerzenmuster algorithmisch und legt die Bestätigungsregel fest.**

## 0. Sakata-Grundsatz

Die japanischen Quellen (Monex, Nomura, Okasan, Hoxsin) beschreiben das 酒田五法 als fünf Methoden: 三山 (drei Berge, Top, mit 三尊 als Kopf-Schulter-Form, wenn der mittlere Gipfel der höchste ist), 三川 (drei Flüsse, Boden, mit 逆三尊 als Umkehrung, und als Dreikerzenform 三川明けの明星 und 三川宵の明星), 三空 (drei Lücken, in lückenlosen Märkten nicht anwendbar), 三兵 (drei Soldaten, Fortsetzung), 三法 (Rasten in der Range, Ausbruch handeln). Die für YAMATO tragende Regel steht bei Monex wörtlich: 底を確認してから買え, erst den Boden bestätigen, dann kaufen, und für das Top: erst nach Bruch der Decke verkaufen, nicht am Gipfel selbst. Das ist die Trennung von Kandidat und Einstieg, die YAMATO in Regeln übersetzt.

Die Muster werden nach dem Grundsatz der Library zusätzlich in Geometrie zerlegt: `lw_range`, `lower_wick_atr`, `body_range`, `close_location`, `range_atr` je Kerze, damit ein Muster nie nur ein Name ist.

## 1. Bottom Candidates (Kerze t, 4h, nur mit Kontext K1 bis K3 des RTC-Frameworks)

| Nr | Muster | Algorithmische Definition |
|---|---|---|
| B1 | 下ヒゲ反転, Lower-Wick-Rejection | `lower_wick_atr_t` ≥ 1.0 und LW ≥ 2.0 · B und `close_location_t` ≥ 0.60. Volumen wird nicht verlangt, aber als `volume_zscore` und `lw_x_vol` je Kandidat geführt (kabutech.jp beschreibt den Selling Climax als langen unteren Docht mit dem Dreifachen des normalen Volumens, das ist Hypothese H1 des Frameworks) |
| B2 | はらみ線, Bullish Harami in der Tiefzone | Library `bullish_harami` mit K3 (Niveau) |
| B3 | 明けの明星, Morning-Star-artig | Library `morning_star`, lückenlose Fassung |
| B4 | 三川 / 二番底, bestätigter Double- oder Triple-Bottom | Abschnitt 2 |
| B5 | Failed Breakdown | Library `failed_breakdown` (Intrabar-Bruch eines Swing Low oder Niveaus, Schluss darüber, Rejection) |

`yamato_bottom_any` = B1 oder B2 oder B3 oder B4 oder B5. Jeder Kandidat trägt seine Musterkennung, die Erwartung wird je Muster berichtet, aber nur das Sammelflag ist Test.

## 2. 三川 und 三山 vollständig algorithmisch

**二番底 (Double Bottom), Stand Kerze t:** Zwei bestätigte Swing Lows s1 < s2 (Library 3/3-Bestätigung, s2 bestätigt spätestens auf t) innerhalb der letzten 240 Kerzen, mit L_{s2} ≥ L_{s1} − 0.5 · ATR14 (das zweite Tief liegt nicht deutlich tiefer, ein leicht tieferes zweites Tief ist zulässig und ist dann ein Sweep) und L_{s2} ≤ L_{s1} + 1.0 · ATR14 (nicht deutlich höher, sonst ist es ein Higher Low, kein Doppelboden), Abstand s2 − s1 ≥ 12 Kerzen (zwei Tage), dazwischen ein bestätigtes Swing High h1 mit H_{h1} − max(L_{s1}, L_{s2}) ≥ 2.0 · ATR14 (die Nackenlinie liegt deutlich über den Tiefs). Nackenlinie N = H_{h1}. Das Muster ist Kandidat auf der ersten Kerze t mit C_t > N (Bruch der Nackenlinie), das ist die Sakata-Bestätigung des Bodens. Kandidat verfällt, wenn nach s2 ein Schluss unter L_{s2} − 0.5 · ATR liegt.

**三川 (Triple Bottom) und 逆三尊:** drei bestätigte Swing Lows s1 < s2 < s3 innerhalb 360 Kerzen, paarweise innerhalb des Toleranzbands (jedes Tief höchstens 1.0 ATR über dem tiefsten und höchstens 0.5 ATR unter dem ersten), zwei Zwischenhochs h1, h2, Nackenlinie N = min(H_{h1}, H_{h2}), Kandidat bei C_t > N. 逆三尊, wenn L_{s2} das tiefste der drei ist. Ein Triple Bottom enthält per Definition einen Double Bottom, der Kandidat wird nur einmal gezählt (der frühere Nackenlinienbruch), das Triple-Flag ist Bericht.

**三山 (Triple Top) und 三尊, spiegelbildlich:** drei bestätigte Swing Highs innerhalb 360 Kerzen im Toleranzband, Nackenlinie N = max(L der zwei Zwischentiefs), Peak Candidate bei C_t < N. 三尊, wenn das mittlere Hoch das höchste ist. Ein Double Top (zwei Hochs, Nackenlinie = Zwischentief) wird als P4-Vorstufe geführt, Bericht.

Alle Zahlen (240 und 360 Kerzen, 0.5 und 1.0 ATR Toleranz, 12 Kerzen Mindestabstand, 2.0 ATR Mindesthöhe der Nackenlinie) sind vorab gesetzt, für Boden und Top gleich, nicht optimiert. Jitter 180/270 und 360/540 Kerzen, Toleranz 0.25/0.75 und 0.75/1.5 nur als Robustheit.

## 3. Bestätigung des Einstiegs: Kandidat ist nicht Einstieg

Baseline-Trigger TA: Die folgende abgeschlossene 4h-Kerze schliesst über dem Hoch der Kandidatenkerze (bei B4 über dem Hoch der Nackenlinien-Bruchkerze). Einstieg zur Eröffnung der übernächsten Kerze. Ohne Bestätigung verfällt der Kandidat.

Separat vorregistrierte Trigger: TB, Rückeroberung des gebrochenen Swing Low oder Support-Niveaus (Library `reclaim_confirmed`), TC, Rückeroberung eines Previous-Open-Niveaus (`btc_previous_open_levels_spec_v0.1.md`, Abschnitt 3). Jeder Trigger ist ein eigener gepaarter Test gegen TA, kein Trigger wird nach Ergebnis erweitert. Ausführung frühestens nach vollständig abgeschlossener Bestätigungskerze, nie intrabar. Initialer Stop wie Framework (Tief der Kandidatenstruktur minus 0.5 ATR, bei B4 unter L_{s2}).

## 4. Peak Candidates (Kerze t, Position offen)

| Nr | Muster | Algorithmische Definition |
|---|---|---|
| P1 | Upper-Wick-Rejection in der Hochzone | `upper_wick_atr_t` ≥ 1.0 und UW ≥ 2.0 · B und `close_location_t` ≤ 0.40 und (`hh20_t` = 1 oder `dist_resistance_atr` ≤ 1.0) |
| P2 | 宵の明星, Evening Star | Library `evening_star` |
| P3 | 三山 / 三尊 | Abschnitt 2, Kandidat beim Nackenlinienbruch |
| P4 | Failed Breakout | Library `failed_breakout` über bestätigtes Swing High oder Resistance |
| P5 | Lower High nach neuem Hoch | Library `lower_high` mit vorigem Swing High als `hh120` |

`yamato_peak_any` = P1 bis P5. Peak Candidate ist kein automatischer Exit.

## 5. Bestätigung des Exits

Primär (E-Y): Nach einem Peak Candidate wird verkauft, wenn eine 4h-Kerze unter dem zuletzt bestätigten Higher Low schliesst (Library `structure_break` bezogen auf das letzte bestätigte Swing Low seit Einstieg). Exit zur Eröffnung der Folgekerze. Ohne Peak Candidate innerhalb der letzten 30 Kerzen ist ein Strukturbruch allein kein Exit (er ist dann H2-Evidenz und wird berichtet), damit die Regel wirklich «Peak, dann Bestätigung» lautet. Der harte Boden (initialer Stop, Chandelier-Floor als Baseline-Vergleich E1) gilt immer.

Sekundär, Inkrement-Test: Schluss unter der Ichimoku-Kijun nach Peak Candidate (`btc_ichimoku_increment_plan_v0.1.md`).

## 6. Bericht je Muster

Für jedes Bottom- und Peak-Muster: Anzahl Kandidaten, Anteil bestätigt (TA), Erwartung je Trade, Anteil Floor über Einstieg, Capture Ratio, Kerzengrenzen-Stabilität. Keine Auswahl von Mustern nach Ergebnis in der Discovery, Musterteilmengen nur für die Validation und nur aus Discovery-Daten.

## 7. Offene Entscheidungen

1. B1-Schwellen (Docht 1.0 ATR, 2 mal Body, Close-Lage 0.60) bestätigen.
2. Double-Bottom-Zahlen (240 Kerzen, Toleranz 0.5 und 1.0 ATR, 12 Kerzen, Nackenlinie 2 ATR) bestätigen.
3. E-Y-Fenster 30 Kerzen zwischen Peak Candidate und Strukturbruch bestätigen.
4. Ob 三兵 (drei Soldaten) als Fortsetzungs-Bericht geführt wird (Empfehlung: nur Bericht).
