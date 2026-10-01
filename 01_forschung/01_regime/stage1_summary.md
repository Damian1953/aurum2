# Stufe 1 — Fazit

**Project Aurum II. Rechenlauf vom 15.09.2026 auf der eingefrorenen Vorregistrierung Version 1.0.**

## Ergebnis in einem Satz

Kein Kandidat besteht. Die Nullhypothese «es existieren keine Zustände, die lange genug dauern, selten genug wechseln, parameterrobust sind und über Coins und Zeitblöcke stabil bleiben» ist nach den eingefrorenen Regeln **nicht widerlegt**. Das ist ein gültiges Ergebnis, kein Scheitern des Laufs.

## Was die Daten zeigen

Über alle fünf Kandidaten, zehn Coins und die Dimensionen D1 bis D3 ergeben sich 140 Coin-Dimension-Paare. Davon liegen

- **140 von 140** innerhalb der Jitter-Schwellen (Übereinstimmung 88 bis 98 Prozent). Die Definitionen sind nicht parameterfragil. Eine Änderung der ADX-Schwelle um zwei Punkte oder des MA-Fensters um zehn Prozent kippt fast kein Label.
- **121 von 140** innerhalb der Wechselraten (D1 typisch 10 bis 14 Wechsel pro Jahr bei Grenze 30, D2 17 bis 23). Die Zustände wechseln nicht hektisch.
- **105 von 140** innerhalb des Ein-Bar-Anteils.
- **36 von 140** innerhalb der Median-Verweildauer.

Das Bild ist eindeutig: **Die Kandidaten scheitern fast ausschliesslich am Median der Verweildauer.** Bei D1 liegt der Median für UP und DOWN je nach Coin und Kandidat zwischen 3 und 9.5 Tagen, die Schwelle war 10. Gleichzeitig liegt der Mittelwert derselben Episoden bei 15 bis 23 Tagen, das Maximum bei 95 bis 111 Tagen, und 87 bis 92 Prozent aller Bars gehören zu Episoden von mindestens zehn Tagen. Rund ein Drittel aller Episoden dauert drei Tage oder kürzer.

Mit anderen Worten: Es gibt lange, stabile Phasen, aber sie werden von vielen kurzen Flackerern an den Rändern begleitet, in denen der ADX um die Schwelle oder der Kurs um den MA100 pendelt. Der Median sieht die Flackerer, der Mittelwert die Phasen. Die Vorregistrierung hat den Median gewählt, und diese Wahl gilt.

**D3 Stress** scheitert deutlicher. Median 2 bis 4.5 Tage in allen Zuständen, Ein-Bar-Anteil 26 bis 31 Prozent. Die Definition mit drei gleichzeitigen Bedingungen und einer Volatilitätsperzentil-Schwelle von 0.70 schaltet an jedem Tag um, an dem eine der drei Bedingungen knapp kippt. Das ist kein Zustand, das ist ein Schalter.

**D4 Volumenbestätigung** ist reines Rauschen: Median 2 Tage, 57 bis 84 Wechsel pro Jahr, und die Kraken-Gegenprobe zeigt nur 78 bis 83 Prozent Übereinstimmung, weil Volumen börsenspezifisch ist. Das war erwartbar und ist jetzt belegt.

**D2 Volatilität** ist die stärkste Dimension. Sie besteht die Gesamtmetriken bei sieben von zehn Coins (Median 8 bis 13 Tage, Ein-Bar 5 bis 7 Prozent) und scheitert nur am Blockkriterium, weil in einzelnen Kalenderjahren ein Zustand fast nicht vorkommt und dann Kurzepisoden den Median drücken.

**F1 Funding** ist im Messjahr zu 88 bis 99 Prozent NEUTRAL. Eine Schwelle von zehn Prozent annualisiert markiert bei BTC und ETH nur wenige Tage. SOL besteht formal, ist aber mit 88 Prozent NEUTRAL ebenso kein Zustandsraum. Gemäss Vorregistrierung wird F1 nach einem weiteren Jahr Daten wiederholt.

## Was die Gegenproben zeigen

Die Kraken-Reihen stimmen bei den preisbasierten Dimensionen zu 94 bis 100 Prozent mit Binance überein. Die Datengrundlage ist belastbar. Der Look-ahead-Test bestand: Labels auf einer am 30.06.2023 abgeschnittenen Historie sind mit dem Volllauf identisch. ATR und ADX stimmen mit einer unabhängigen Referenzimplementierung auf 1e-11 überein.

## Zwei Lesarten, eine Entscheidung

Die Daten lassen zwei Lesarten zu. Erstens: Es gibt Regime, sie flackern nur an den Rändern, und eine Hysterese- oder Mindestdauer-Regel würde sie sauber machen. Zweitens: Schwellenbasierte Tageslabels sind kein Regime, sondern Momentaufnahmen.

Die Vorregistrierung entscheidet für die zweite Lesart, weil das Kriterium so gesetzt wurde. Das Kriterium jetzt vom Median auf den Mittelwert zu wechseln, weil der Mittelwert bestehen würde, wäre exakt die nachträgliche Anpassung, die Abschnitt 10 der Vorregistrierung verbietet. Sie wird nicht gemacht.

## Konsequenzen nach Freeze-Protokoll

1. `frozen_regimes_v1.json` enthält keine taugliche Definition. **Stufe 3 entfällt.**
2. **Stufe 2 läuft ohne Regimefilter.** Das ist kein Umweg. Stufe 2 fragt, ob eine Strategie ohne Filter einen Edge hat, und braucht dafür kein Regime. Sie war ohnehin der nächste Schritt.
3. Die erste Lesart darf nicht verworfen, aber auch nicht nachträglich hineinoptimiert werden. Sie wird als **Hypothese für eine Version 2 der Regime-Vorregistrierung** festgehalten: Zustandswechsel erst nach k Bestätigungstagen, oder Verweildauer über den Mittelwert statt den Median beurteilt. Eine Version 2 ist eine neue Vorregistrierung mit neuen Schwellen, die ehrlich als in-sample-informiert deklariert wird. Sie ist optional und nicht Voraussetzung für Stufe 2.
4. Für die spätere Exposure-Steuerung ist das Ergebnis ein Hinweis, keine Vorschrift: Die kontinuierlichen Grössen hinter den Labels (Abstand zum MA, Volatilitätsperzentil) sind robust, ihre Diskretisierung in Zustände nicht. Ein graduelles Gate auf kontinuierlichen Grössen, wie es im Altprojekt gemessen wurde, ist mit diesem Befund vereinbar. Ein diskreter Regime-Schalter ist es nicht.

## Dateien

- `stage1_robustness_report.md` — alle Metriken je Kandidat, Coin, Dimension, Block
- `stage1_results.json` — vollständige Rohergebnisse mit Prüfsummen der Eingaben
- `stage1_config_log.csv` — jede gerechnete Konfiguration inklusive Jitter
- `stage1_labels/{coin}.csv` — Zustandslabels je Tag und Kandidat
- `frozen_regimes_v1.json` — Status «kein Kandidat tauglich»
- `stage1.py`, `report.py` — Rechenlauf und Berichtgenerator, reproduzierbar
