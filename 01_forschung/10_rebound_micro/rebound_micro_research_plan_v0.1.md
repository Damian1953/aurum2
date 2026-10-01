# REBOUND-MICRO — Forschungsplan, Version 0.1

**Project Aurum II, `01_forschung/10_rebound_micro/rebound_micro_research_plan_v0.1.md`. 18.09.2026. Status: Entwurf vor Freeze, kein P&L-Lauf. Neue outcome-informed Hypothese, Ebene C. Keine Version 2 von REBOUND-20 (abgeschlossen, `rebound20_closure_v1.md`). Development-Märkte: BTC, XRP, DOT, Development Evidence only. ETH und SOL bleiben unberührt: keine Daten geladen, keine Kandidaten, keine Merkmale, keine Outcomes. Begleitdokumente: `rebound_micro_1h_feature_spec_v0.1.md`, `equilibrium_target_research_v0.1.md`, `rebound_micro_promotion_rules_v0.1.md`, `rebound_micro_trial_accounting_v0.1.md`, `rebound_micro_1h_data_audit_v0.1.md`.**

## 1. Kernfrage

Kann derselbe grobe 4h-Selloff-Kontext durch 1h-Struktur und Flow zeitlich so präzisiert werden, dass ein tatsächlich bestätigtes 1h-Reversal einen logisch näheren Invalidationspunkt liefert, und verbessert das die Reward/Loss-Geometrie fundamental, ohne dass Stoprate, Kosten und Fehltrades den Vorteil aufzehren. Nicht: Wie machen wir den Stop enger.

## 2. Architektur

4h bestimmt Location und Kontext und erzeugt keinen Trade. 1h bestimmt Reversal und Ausführung. Flow prüft Seller Exhaustion. Ein vorab festgelegtes Equilibrium (Q0 EMA20, Q1 Anchored VWAP) bestimmt das kurzfristige Ziel. Alle Berechnungen auf Binance Spot (Signal und Ausführungsmodell), Perp-1h nur als vorregistrierte Diagnose der Flow-Merkmale, nicht als Trigger.

## 3. 4h Context Engine (ausschliesslich Location, keine neue Optimierung)

Kontextkerze t (4h) nach der bestehenden Library rlib v1.0 im Modus `cfg_alt`, einheitlich für alle drei Development-Coins: K1 in ATR-Form (`dd120_atr` ≤ −6.0), K2 (`ext` ≤ −2.0 ATR in sechs Kerzen), K3 (innerhalb 1 ATR eines Niveaus oder `at_low_structure` in ATR-Form). Für BTC ist das eine Abweichung von der eingefrorenen Stufe-A-Form (12 Prozent), zulässig, weil BTC hier Development-Markt ist, ausgewiesen. Der Kontext ist am Schluss der 4h-Kerze t vollständig bekannt. Er setzt `reversal_search_active = true` für die 1h-Kerzen der folgenden sechs 4h-Kerzen (t+1 bis t+6, 24 Stunden). Ist eine spätere 4h-Kerze ebenfalls Kontextkerze, verlängert sich das Fenster entsprechend. Ein Kontext-Event ist ein zusammenhängender aktiver Abschnitt, Beginn mit der ersten Kontextkerze. Niveaus für M1: die drei 4h-Niveaus Stand t−1 (`swing_low_level`, `nbar_low_level`, `zone_low_level`, Definitionen wie XRP v1.0 Abschnitt 4) und zusätzlich das Tief der Kontextkerze t selbst (`context_low`), alle bekannt am 4h-Schluss t.

## 4. 1h Execution Engine, exakt drei Mechanismen

Alle 1h-Merkmale nur aus vollständig abgeschlossenen 1h-Kerzen, Einstieg frühestens zur Eröffnung der nächsten handelbaren 1h-Kerze, ATR14(1h) Wilder, für Kerzenvergleiche ATR14(1h)_{b−1}. Definitionen der Kerzenmerkmale und Flow-Merkmale in der Feature-Spezifikation.

M1 Failed Breakdown / Reclaim: Innerhalb des aktiven Fensters eine 1h-Kerze b mit L_b ≤ Niveau − 0.05 · ATR14(4h)_t und C_b > Niveau auf mindestens einem der vier Niveaus, wobei mindestens eine 1h-Kerze im Fenster vor oder bei b unter dem Niveau gehandelt hat (Sweep). Sweep-Tief = min(L) über die 1h-Kerzen des Fensters von der ersten Kerze unter dem Niveau bis b. Einstieg Eröffnung b+1. Stop = Sweep-Tief − 0.25 · ATR14(1h)_b.
M2 Rejection plus Confirmation: 1h-Kerze b mit `lower_wick_atr` ≥ 1.0 (ATR14(1h)_{b−1}), unterer Docht ≥ 2 · Körper, `close_location` ≥ 0.60. Bestätigung: die nächste vollständig abgeschlossene Kerze b+1 mit C_{b+1} > C_b und L_{b+1} > L_b. Einstieg Eröffnung b+2. Stop = L_b − 0.25 · ATR14(1h)_b.
M3 Flow Transition / Seller Exhaustion: Sequenz innerhalb des Fensters. (i) Absorptionskerze a: `sell_volume_zscore` ≥ 1.0 und `sell_efficiency` ≤ 0.25 (starkes aggressives Verkaufen bei geringem Preisfortschritt nach unten, Feature-Spezifikation). (ii) Flow-Wende: Kerze b mit a < b ≤ a+6, `delta_taker_imbalance` ≥ +0.15 und `taker_imbalance` ≥ 0. (iii) Price Reclaim: C_b > H_a. Einstieg Eröffnung b+1. Stop = min(L, a..b) − 0.25 · ATR14(1h)_b. M3 wird zweifach geführt: als Flow-Flag auf M1- und M2-Einstiegen (nested, dasselbe strukturelle Setup mit und ohne Flow-Transition im Fenster bis zur Einstiegskerze) und als eigenständiger Trigger für Fälle, die weder M1 noch M2 erfüllen, separat gekennzeichnet.

Ausschluss für alle drei (Definitionselement der Hypothese, nicht Optimierung): Liegt Einstieg − Stop über 1.0 · ATR14(4h)_t, liefert die 1h-Struktur keinen näheren Invalidationspunkt als die 4h-Struktur, der Kandidat wird als `no_tight_invalidation` ausgeschlossen und gezählt. Je Kontext-Event höchstens ein Einstieg je Mechanismus (der erste), eine offene Position je Zelle, weitere Kandidaten während einer Position verfallen (`in_position`). Kein Kandidat in einem Fenster mit Datenlücke (Audit).

## 5. Ziele und Exits

Q0 EMA20: Wert der EMA20 der 4h-Schlusskurse am letzten abgeschlossenen 4h-Schluss vor der Einstiegskerze, als fester Limit-Zielpreis ab Einstieg (Fill am Ziel ohne Slippage, wenn das 1h-Hoch es erreicht, bei Eröffnung darüber Fill an der Eröffnung). Q1 Anchored VWAP: Wert des AVWAP der laufenden Selloff-Episode am letzten abgeschlossenen 1h-Schluss vor der Einstiegskerze, ebenfalls fester Limit-Zielpreis (`equilibrium_target_research_v0.1.md`). Liegt ein Ziel unter dem Einstiegspreis, ist die Zelle für diesen Kandidaten nicht anwendbar (`target_below_entry`, gezählt). Exit sonst: initialer Stop als Stop-Market intraday (Eröffnung unter Stop → Eröffnung), Zeitstopp 24 1h-Kerzen nach Einstieg → Exit zur Eröffnung der Folgekerze. Kein Chandelier, kein Strukturbruch, kein Scale-out, keine Restposition.

## 6. Kosten, Sizing, Fills

K1 (Gebühr 0.40 Prozent je Seite, Reibung 0.02, Slippage 0.05 Einstieg, 0.10 Stop, Ziel-Limit ohne Slippage), K0 und K2 als Bericht. Sicht 1, 2 Prozent Risiko je Trade, R = Einstieg − Stop. Kosten je Trade in R werden ausgewiesen, weil R hier klein ist und die Kosten den Vorteil der Geometrie aufzehren können.

## 7. Development-Matrix

Je Coin höchstens sechs Zellen: M1×Q0, M1×Q1, M2×Q0, M2×Q1, M3×Q0, M3×Q1, dazu der nested Flow-Vergleich auf M1 und M2 je Ziel. Keine Erweiterung nach Outcome. Überschneidungen M1/M2/M3 auf Kandidatenebene werden berichtet.

## 8. Baseline und Kontrolle

Strukturelle Baseline: für dasselbe Kontext-Event der 4h-Trade nach REBOUND-20-Umsetzung (T0 auf der ersten Kontextkerze mit Muster, Stop Strukturtief minus 0.5 ATR14(4h), Ziel EMA20 als Limit, Zeitstopp 30 4h-Kerzen), berechnet mit denselben Kosten. Gepaarte Differenz je Kontext-Event zwischen 1h-Zelle und 4h-Baseline ist der primäre Vergleich. Zusätzlich Kontrollgruppe: dieselben 1h-Mechanismen in Fenstern von 4h-Kerzen mit K1 und K2, aber ohne K3 (kein Niveau in der Nähe), gematcht ±540 4h-Kerzen und `dd120_atr` ±1.5, bis zu drei je Event, um zu isolieren, ob die Location etwas beiträgt.

## 9. Diagnoseblock vor jedem P&L (outcome-blind, im Vorbericht)

Je Kandidat: `entry_to_stop_ATR` (in ATR14(4h)_t und ATR14(1h)), `entry_to_Q0_ATR`, `entry_to_Q1_ATR`, geometrisches Reward/Risk zu Q0 und Q1, geometrische Break-even-Trefferquote p_BE_geo = 1 / (1 + RR) nach Kosten (Ziel minus Kosten, Stop plus Kosten in R). Verteilung der 1h-Stopdistanz gegen die 4h-T0-Stopdistanz desselben Events. Diese Werte enthalten keine Outcomes.

## 10. Diagnoseblock nach dem Lauf (erst nach Freeze)

avg_win_R, avg_loss_R, Trefferquote, Stoprate, Zielrate, Zeitstopp-Anteil, empirische p_BE = |avg_loss| / (avg_win + |avg_loss|), Zeit bis Stop, Anteil Stop-outs, die danach innerhalb 24 Kerzen Q0 beziehungsweise Q1 erreichen, Kosten je Trade in R, Slippage-Sensitivität (K0, K1, K2), Blöcke, Konzentration, gepaarte Differenz gegen Baseline und Kontrollen. Zusätzlich diagnostisch nach erreichtem Ziel: MFE nach Ziel, neues 20- und 30-Tage-Hoch, Zeit Ziel bis Trend. Kein Scale-out, keine Trend-Regel.

## 11. Statuszuweisung und Promotion

Regel v2 (Governance v1.1) mit Low-Frequency-Stufung (unter 20 deskriptiv, 20 bis 29 höchstens mechanistically promising low-frequency, ab 30 normal), je Coin, je Zelle, Holm über sechs Zellen je Coin. Promotion Richtung ETH/SOL nur nach `rebound_micro_promotion_rules_v0.1.md`, numerisch vor Outcome festgelegt. Economic Validation Gate bleibt vor jeder späteren Holdout-Validation bestehen.

## 12. Was nicht Teil dieses Zyklus ist

Kein Volume Profile, keine OI-, Funding- oder Liquidationsdaten, keine Visual AI, kein Pattern Mining (Bullish Harami und Hikkake nur als benannte Diagnoseflags), keine Trend-Hold-Regel, keine Vermischung mit DB-CONTEXT.
