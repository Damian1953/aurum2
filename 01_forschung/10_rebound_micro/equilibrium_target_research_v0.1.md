# REBOUND-MICRO — Equilibrium-Ziel, Version 0.1

**Project Aurum II, `01_forschung/10_rebound_micro/equilibrium_target_research_v0.1.md`. 18.09.2026. Genau zwei Zielkandidaten, beide vor Outcome festgelegt: Q0 EMA20 (Kontrolle, unverändert) und Q1 Anchored VWAP mit genau einer Ankerregel. Kein Volume Profile in diesem Zyklus. Keine Zielsuche anhand von P&L.**

## 1. Was mit den vorhandenen Daten sauber berechenbar ist

Vorhanden: 1h-OHLCV mit Quote-Volumen und Taker-Aufteilung (Binance Spot und Perp), 4h und 1d daraus. Nicht vorhanden: 5m- oder 1m-Klines, Trades, Tickdaten. Ein Price-by-Volume-Level (Volume Profile POC, Value Area) braucht die Volumenverteilung innerhalb der Kerze. 1h-Klines enthalten sie nicht. Ein POC aus 1h-Kerzen wäre eine Verteilung des Kerzenvolumens auf ein angenommenes Preisband (zum Beispiel gleichverteilt zwischen Hoch und Tief), also eine Konstruktion, deren Ergebnis von der Annahme abhängt und nicht von den Daten. Er wird nicht gebaut. Nötig für ein echtes Volume Profile wären mindestens 1m-Klines (Binance Vision hat sie, rund 60-mal so gross wie 1h) oder aggTrades. Das ist ein späterer, eigener Beschaffungsentscheid. Das SOL-Volume-Profile-Paper (SSRN, nicht peer-reviewt, Previous-Day Volume Profile und Tape Speed) ist Hypothesengenerator, nicht Grundlage.

Sauber berechenbar aus 1h-Klines: jede Form von VWAP, weil VWAP nur Kerzenpreis und Kerzenvolumen braucht. Rolling VWAP (Fenster fix), Session VWAP (UTC-Tag) und Anchored VWAP (Anker algorithmisch) sind alle reproduzierbar. Gewählt wird Anchored VWAP, weil die Hypothese ein Gleichgewicht der laufenden Selloff-Episode meint, nicht eines Kalendertages.

## 2. Q0 EMA20, unverändert

EMA20 der 4h-Schlusskurse (Initialisierung Mittel der ersten 20, Faktor 2/21), Wert am letzten abgeschlossenen 4h-Schluss vor der Einstiegskerze, als fester Limit-Zielpreis ab Einstieg. Das ist die bestehende Kontrollarchitektur aus REBOUND-20 und E0, mit dem einzigen Unterschied, dass das Ziel als Limit fixiert wird statt als «Schluss über EMA20» dynamisch, damit die Geometrie ex ante feststeht. Diese Fixierung ist eine Umsetzungsentscheidung, die vor Outcome gilt.

## 3. Q1 Anchored VWAP, Definition

Preisinput: typical price (H + L + C) / 3 der 1h-Kerze. Volumen: Basisvolumen `volume` der 1h-Kerze (Spot). AVWAP_b = Σ(tp_i · vol_i) / Σ(vol_i) über alle 1h-Kerzen i vom Anker bis einschliesslich b. Quelle Binance Spot 1h. Datenlücken: fehlende Kerzen werden übersprungen (keine Füllung), eine Lücke innerhalb der Episode wird geflaggt, der AVWAP läuft weiter. Mehrere Tage: kein Tagesreset, der AVWAP läuft über die ganze Episode. Wert für das Ziel: AVWAP am letzten abgeschlossenen 1h-Schluss vor der Einstiegskerze, danach fester Limit-Zielpreis.

## 4. Anker- und Resetregel (rein mechanisch, outcome-blind)

K1-Episode auf 4h: Sie beginnt mit der ersten 4h-Kerze t0, an deren Schluss K1 (`dd120_atr` ≤ −6.0) von falsch auf wahr wechselt. Der Anker ist die erste 1h-Kerze der 4h-Kerze t0 (t_b = Beginn von t0). Der Anker ist damit am Schluss von t0 bekannt und wird nie rückwirkend anhand eines späteren Tiefs verschoben. Eine laufende Episode behält denselben Anker, solange K1 wahr ist oder höchstens fünf aufeinanderfolgende 4h-Kerzen falsch war. Die Episode endet am Schluss der sechsten aufeinanderfolgenden 4h-Kerze mit K1 falsch (24 Stunden ohne Selloff-Kontext). Nach dem Ende erzeugt der nächste Wechsel falsch → wahr einen neuen Anker. Der AVWAP endet mit der Episode; ein Kandidat ausserhalb einer laufenden Episode hat keinen Q1 (`no_episode`, gezählt). Begründung der Sechs-Kerzen-Toleranz: identisch mit der Länge des Reversal-Suchfensters (Abschnitt 3 des Forschungsplans), sodass Kontext, Suchfenster und Episode dieselbe Zeitskala haben. Keine zweite Toleranz wird geprüft.

## 5. Anwendbarkeit

Liegt Q1 (oder Q0) am Einstiegszeitpunkt unter dem Einstiegspreis, ist das Ziel nicht anwendbar, der Kandidat gehört nicht zur Zelle (`target_below_entry`, gezählt). Liegt das Ziel oberhalb, ergibt sich die Geometrie `entry_to_Q_ATR` und das Reward/Risk direkt.

## 6. Freigabe

Q1 ist mit den vorhandenen 1h-Klines technisch sauber berechenbar und wird freigegeben. Genau ein Anker (Episode-Beginn nach Abschnitt 4), keine Alternative.
