# XS21 Point-in-Time v0.2 – Review durch Claude, Version 1

**Project Aurum II, 01.10.2026. Geprüft: `xs21_point_in_time_prereg_v0.2.md` (Entwurf, nicht eingefroren) und Review-Auftrag vom 01.10.2026. Grundlage: ENTSCHEIDE Schritt 0 v0.2, Holdout- und Börsen-Prüfung v1, Stufe-2-Hypothesen v2, Governance v1.1. Nicht geprüft: die CSV-Listen selbst (`xs21_exclusions_v0.1.csv`, `xs21_unklar_v0.1.csv`), sie lagen nicht vor. Die Aussagen zu einzelnen Symbolen beziehen sich auf die Kategorien im Entwurf.**

## Gesamturteil

Der Entwurf setzt die Entscheide B1 bis B8 korrekt um. Die Etikettierung in §3 ist sauber, die Interpretationstabelle in §5 ist vorab festgelegt. Nach Einarbeitung der Pflichtänderungen M1 bis M7 ist er als v1.0 freigabefähig.

Zur Einordnung der B7-Frage: Fast alle 198 Ausschlüsse sind ab 2026 gelistet. Vor 2026 betrifft die Liste nur PAXG, XAUT und USDC (ab 2025-12). Der wissenschaftlich relevante Teil 2020-02 bis 2023-12 ist von der Liste praktisch nicht berührt. Die B7-Entscheide sind deshalb wichtig für die Sauberkeit und das Forward-Fenster, aber nicht für das Kernergebnis. Sie sollten schnell und regelbasiert entschieden werden, ohne lange Einzelprüfung.

---

## 1. B7-Ausschlussliste

### 1.1 Präzisierung der Regel (M1)

Die Regel «Basiswert ist ein Krypto-Asset» lässt die strittigen Fälle offen. Vorschlag für den Wortlaut in v1.0:

«Zugelassen sind nur Perpetuals auf ein einzelnes Krypto-Asset, dessen ökonomisches Exposure nicht an einen Fiat-Wert, einen Rohstoff, ein Wertpapier oder einen Index gebunden ist. Ausgeschlossen sind Stablecoins, tokenisierte Rohstoffe und Wertpapiere sowie Index- und Korb-Perps.»

Damit entscheiden sich die offenen Fälle aus der Regel, nicht einzeln.

### 1.2 PAXG und XAUT: ausschliessen

Das ökonomische Exposure ist Gold, die Blockchain ist nur die Verpackung. H-C2 ist eine Aussage über den Querschnitt von Krypto-Assets. Ein Gold-Token gehört aus demselben Grund nicht dazu, aus dem XAUUSDT ausgeschlossen wird. Kategorie «tokenisierter Rohstoff», Sicherheit «sicher».

### 1.3 Krypto-Indizes BTCDOM, DEFI, FOOTBALL, BLUEBIRD: ausschliessen

Gründe:
- XS21 rangiert Einzel-Assets. Ein Index ist eine Linearkombination von Symbolen, die selbst im Universum sind. Er erzeugt mechanische Korrelation im Querschnitt und kann dasselbe Exposure doppelt in ein Bein bringen.
- BTCDOM ist kein Asset, sondern ein Spread (BTC gegen einen Altcoin-Korb). Seine Rendite hat eine andere Natur als die eines Coins, ein Ranking mit Coins ist nicht vergleichbar.
- Für U2 und das Ausführbarkeits-Gate sind diese Indizes auf Kraken nicht verfügbar.

Der Ausschluss folgt aus der Struktur, nicht aus einem Ergebnis, und ist deshalb vor dem Lauf unbedenklich.

### 1.4 USTC, FRAX, STABLE, STBL: zulassen, mit Prüfung

- **USTC:** zulassen, sofern das Binance-UM-Listing nach der Entkopplung im Mai 2022 liegt. Dann war das Symbol während seiner ganzen Handelszeit kein gebundener Stablecoin. Prüfung über `first_month`.
- **FRAX, STABLE, STBL:** zulassen, wenn die Binance-Ankündigung als Underlying einen Governance- oder Chain-Token nennt. Bei FRAX besonders prüfen, weil der Name früher den Stablecoin bezeichnete. Liegt das Listing vor einer Umbenennung, gilt der damalige Basiswert.

### 1.5 «wahrscheinlich» (55) und «unklar» (59)

- Die Prüfung gegen die Binance-Ankündigung (Feld «Underlying») ist richtig und bleibt Pflicht vor dem Freeze.
- **Auffangregel (M2):** Bleibt ein Symbol nach der Prüfung unklar, entscheidet eine feste Rangfolge.
  - Ein Binance-Spot-Paar oder ein identifizierbarer On-Chain-Token führt zur Zulassung.
  - Fehlt beides, wird das Symbol ausgeschlossen.
  - Jeder Eintrag erhält Quelle und Datum der Prüfung.
- Die 9 unklaren Symbole mit Spot-Paar (CHIP, GENIUS, GRAM, KAT, MARSCOIN, OPG, OPN, RE, ROBO) sind danach zuzulassen, sofern die Ankündigung nicht widerspricht.
- **Sensitivität:** Zusätzlich wird ein Lauf ohne alle Symbole mit Sicherheit «wahrscheinlich» oder Auffangregel berichtet. Er ist deskriptiv und kein Primärtest.
- Die Listen werden nur aus Namen, Listing-Monaten und Ankündigungen erstellt, wie im Entwurf. Kurse und Volumen bleiben ausser Betracht, das ist richtig so.

---

## 2. Offene Punkte §8

### 2.1 Schwellen des Ausführbarkeits-Gates (B6), vor dem Lauf festlegen (M3)

Die Schwellen müssen jetzt eingefroren werden. Würden sie nach dem Lauf gesetzt, wäre bekannt, welche Symbole U2 tatsächlich wählt. Vorschlag:

- **Messgrundlage:** Forward-Daten des Collectors ab 15.09.2026, Kraken Futures. Eine Rückrechnung ist nicht möglich, weil die meisten PF-Perps erst seit 22.03.2022 existieren und keine historischen Volumen vorliegen.
- **Je gewählte Position:** Symbol auf Kraken Futures handelbar und Median des 24h-Volumens der letzten 30 Tage mindestens 2 Mio. USD.
- **Gate bestanden:** In den ersten 8 Rebalancings des Forward-Fensters sind mindestens 90 Prozent der gewählten Positionen nach dieser Regel handelbar.
- **Nicht handelbares Symbol im Betrieb:** Die Position bleibt in Cash. Es wird nicht auf den nächsten Rang ausgewichen, weil das eine neue Regel wäre.
- **Positionsgrösse:** höchstens 0.1 Prozent des 24h-Volumens je Symbol. Bei den Volumen aus der Börsen-Prüfung ist das für ein Privatkonto keine Einschränkung, die Regel dient als Sicherung.

### 2.2 Tie-Break in U2: alphabetisch bestätigen

Bei stetigen Volumen praktisch ohne Wirkung. Bestätigen.

### 2.3 Fehlendes Funding: weder null noch Ausschluss (M4)

- **Null ist nicht konservativ.** Funding fällt je nach Richtung als Kosten oder Ertrag an. Mit null würde ein Short-Bein in Aufwärtsphasen bevorteilt.
- **Ausschluss verzerrt.** Fehlende Daten hängen oft mit jungen oder später delisteten Symbolen zusammen. Ein Ausschluss würde genau die Survivorship-Verzerrung wieder einführen, die der Lauf messen soll.
- **Vorschlag:** Fehlendes Funding wird mit dem Median des absoluten Fundings aller Universumssymbole zum selben Settlement gefüllt, immer zulasten der Position (long und short zahlen). Anzahl und Anteil der gefüllten Settlements werden je Bein berichtet. Liegt der Anteil über 5 Prozent der Positions-Settlements, steht das als Vorbehalt im Bericht.

### 2.4 Zeitblöcke für Kriterium 4 (M5)

Die Stufe-2-Blöcke passen nicht. P1 würde mit dem Start 2020-02 nur elf Monate umfassen. Vorschlag:
- B1: 2020-02-01 bis 2021-12-31
- B2: 2022-01-01 bis 2023-12-31
- B3: 2024-01-01 bis 2026-09-14

2026 wird kein eigener Block, weil 8.5 Monate für eine Blockaussage zu kurz sind.

**Zusatzbedingung, wegen B5:** Ein Bestehen verlangt positive Werte in B1 **und** B2. B3 wird berichtet, darf aber nicht die fehlende Stimme liefern. Sonst würde der vorbelastete Zeitraum über das Urteil mitentscheiden, was §3 gerade ausschliesst. Das ist strenger als Stufe 2 und wird in §0 als Abweichung ausgewiesen.

### 2.5 Dezil-Vergleich in U2: streichen

Ein Dezil von 20 sind 2 Symbole. Das ist identisch mit dem Jitter Top-N = 2. In U2 streichen und vermerken «identisch mit Jitter Top-2». In U1 bleibt das Dezil.

### 2.6 Mindestgrösse von U1 je Stichtag (M6)

Vorschlag: Ein Stichtag zählt, wenn U1 mindestens 20 Symbole hat, also mindestens so viele wie U2. Der Laufbeginn ist der erste Stichtag, der diese Bedingung erfüllt. Er wird vor dem Lauf nur aus Listing und Volumen bestimmt, ohne Renditen, und für U1 und U2 gemeinsam verwendet. Fällt U1 später unter 20, hält der Stichtag Cash, und die Anzahl solcher Stichtage wird berichtet. Nach Lane-C-Befund ist das ab 2020 kaum zu erwarten.

---

## 3. Weitere Befunde aus dem Entwurf

### 3.1 Signalquelle ist nicht «wörtlich» Stufe 2 (M7)

Stufe 2 hat ret(21) auf **Binance-Spot**-Tageskerzen berechnet (Holdout- und Börsen-Prüfung v1, 2.1). v0.2 §4 verwendet **Binance-Perp**-Tageskerzen. Für das PiT-Universum ist das richtig, weil viele Symbole kein Spot-Paar haben. Es ist aber eine Abweichung und muss in §0 und §4 ausgewiesen werden, mit Begründung. Der Satz «wörtlich aus Stufe 2» ist entsprechend einzuschränken.

### 3.2 Kosten in U1 sind nicht ausführbar zu lesen

Das einheitliche Perp-Kostenmodell unterschätzt die Kosten für die dünnen Extremwert-Symbole, die U1 typischerweise wählt. Für U1 ist das hinnehmbar, weil U1 die Forschungsfrage beantwortet. In §6 sollte stehen: «Netto-Ergebnisse von U1 sind nicht als handelbare Renditen zu lesen. Über die Handelbarkeit entscheidet nur U2.»

### 3.3 Kleinere Punkte

- **U2 ⊆ U1** sollte als Prüfbedingung im Code stehen. Ein U2-Symbol unter 50 Mio. USD Umsatz wäre ein Datenfehler.
- **T-Bill-Datei:** `DTB3_3m_tbill.csv` fehlte in der Kopie (Review v1, Bug 2). Für den Cash-Ertrag vor dem Lauf mit SHA ablegen.
- **Survivorship-Zerlegung:** Stichtag 2026-09-14 ist richtig. Zusätzlich die Zerlegung nach dem Stand 2023-12-31 berichten, damit der Vergleich mit dem Lane-C-Befund (81 Symbole bis Ende 2023 delistet) möglich ist.
- **Holm über 2 Tests:** U1 und U2 sind stark korreliert, Holm ist damit konservativ. Das ist in Ordnung und braucht keine Änderung.

---

## 4. Kosten-Lesart, Kostenmodell, E3

### 4.1 Kosten-Lesart REBOUND-MICRO: einverstanden

Vermerk als Lesart, ohne Umetikettierung: «K1 Spot 0.40 Prozent entspricht dem Kraken-Spot-Maker-Satz (Tier 1). Der REBOUND-MICRO-Entscheid ‹keine Maker-Gutschrift› bleibt gültig. Stops sind Market-Orders und damit Taker. Das Szenario maker_entry_taker_stop ist ein Entwurf und wird auf keinen eingefrorenen Lauf angewendet.» Am Urteil von REBOUND-MICRO ändert das nichts, weil schon K0 negativ war.

### 4.2 JSON statt costs.yaml: einverstanden

Der Zweck von C2 war eine einzige Quelle, nicht das Format. Zwei Bedingungen:
- Die duplizierten Konstanten in `ylib.py`, `s2lib.py` und `mtp_val.py` werden in neuen Dateiversionen durch Lesen von `config/cost_model_v1.json` ersetzt, oder ein CI-Test prüft ihre Gleichheit mit dem JSON. Eingefrorene Versionen bleiben unverändert.
- Die abweichenden Sätze in `05_evidenz/README.md` werden mit Vermerk korrigiert.

### 4.3 E3: Vermerk präzisieren

Wenn sich nicht belegen lässt, welcher Zeitstempel falsch ist, kann der Vermerk nicht einfach festhalten, «FREEZE vor Lauf» sei massgeblich. Das wäre eine Behauptung. Belastbar ist ein anderer Nachweis: Enthält die Lauf-Ausgabe die SHA der Spezifikation, und stimmt sie mit der eingefrorenen v1.0 überein, ist belegt, dass der Lauf mit dem eingefrorenen Inhalt gerechnet wurde, unabhängig von der Uhrzeit. Vorschlag für den Vermerk: «Die Reihenfolge der Zeitstempel ist nicht belegbar. Massgeblich ist die SHA-Übereinstimmung der Spezifikation im Lauf-Log mit dem Freeze (SHA …).» Ist die SHA im Log nicht enthalten, wird das ebenso offen vermerkt.

---

## 5. Checkliste für v1.0

| Nr. | Änderung | Abschnitt |
|---|---|---|
| M1 | Regelwortlaut B7 (Einzel-Krypto-Asset, Ausschluss tokenisierter Rohstoffe, Index- und Korb-Perps) | §2.4 |
| M2 | Auffangregel für unklare Symbole, Quelle und Datum je Eintrag, Sensitivitätslauf deskriptiv | §2.4 |
| M3 | Schwellen Ausführbarkeits-Gate eingefroren | §5 |
| M4 | Fehlendes Funding: adverses Median-Funding, Bericht des Anteils | §7 |
| M5 | Blöcke B1/B2/B3, Bestehen verlangt B1 und B2 positiv | §5 |
| M6 | Mindestgrösse U1 von 20, Laufbeginn vorab bestimmt | §2.2, §3 |
| M7 | Signalquelle Perp statt Spot als Abweichung ausgewiesen | §0, §4 |
| – | PAXG, XAUT, BTCDOM, DEFI, FOOTBALL, BLUEBIRD ausschliessen. USTC, FRAX, STABLE, STBL nach Prüfung zulassen | Liste |
| – | Dezil in U2 streichen, Tie-Break bestätigen | §4, §2.3 |
| – | Kostenvermerk U1, U2 ⊆ U1 als Prüfung, DTB3 ablegen, Zerlegung auch per 2023-12-31 | §5, §6, §7 |

Nach Einarbeitung: v1.0 mit SHA in ENTSCHEIDE, danach Datenbeschaffung nach §7, danach ein einziger Lauf. Die B7-Liste wird vor der Datenbeschaffung eingefroren, nicht danach.
