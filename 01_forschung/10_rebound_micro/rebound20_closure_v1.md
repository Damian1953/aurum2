# REBOUND-20 v0.1 — Abschluss, Version 1

**Project Aurum II, `01_forschung/10_rebound_micro/rebound20_closure_v1.md`. 18.09.2026. Entscheid (Nutzer): REBOUND-20 v0.1 — Spezifikation abgeschlossen, keine Fortführung. Keine Umetikettierung früherer Ergebnisse, kein Status. ETH und SOL werden für diese Spezifikation nicht verbraucht. Grundlage: `eth_sol_rebound20_prereg_v0.1.md` (SHA im ENTSCHEIDE-Eintrag vom 18.09.2026 02:30 UTC) und Development-Datei `dev_rebound20.json`.**

## 1. Was abgeschlossen wird

Die Hypothese, dass ein 4h-Bottom-Signal im Selloff-Kontext (Failed Breakdown oder Wick plus Volumen, Trigger T0, Stop Strukturtief minus 0.5 ATR) mit einem EMA20-Ziel als eigenständiger Rebound-Sleeve handelbar ist, in der Form der Vorregistrierung v0.1 mit den beiden Mindestbedingungen (Abstand zur EMA20 in ATR, Abstand je Risikoeinheit) und den je zwei Kandidatenwerten.

## 2. Begründung, aus den Development-Coins

Auf BTC, XRP und DOT zeigt die Umsetzung eine strukturell ungünstige Payoff-Geometrie. Erfolgreiche EMA20-Rebounds bringen im Mittel etwa +0.33 bis +0.60 R (XRP X1 +0.52, X3 +0.33, DOT D1 +0.60, D3 +0.43 R). Verlusttrades kosten etwa −1.2 bis −1.4 R (Stop-Fills mit Slippage und Kosten K1, XRP X1 −1.30, DOT D1 −1.24, Stop in der Einstiegskerze bis −1.44 R). Die EMA20 wird in ungefähr der Hälfte der Fälle erreicht (XRP X1 36 von 69, DOT D1 29 von 58, DOT D3 8 von 16, XRP X3 11 von 22).

Referenzrechnung: Mit +0.5 R je Gewinner und −1.3 R je Verlierer liegt die Break-even-Trefferquote bei p_BE = 1.3 / (1.3 + 0.5) = 72.2 Prozent. Die beobachtete Trefferquote von rund 50 Prozent liegt weit darunter. Die Netto-Erwartung war auf allen Familien und Coins negativ: −0.34 bis −0.58 R je Trade bei K1.

Die vorab benannte Auswahlregel für eine Mindestbedingung (kleinster Wert, bei dem die Erwartung auf zwei von drei Coins nicht negativ ist) wurde von keinem der vier Kandidaten erfüllt. Ein grösserer Abstand zur EMA20 erhöhte das Potenzial, aber nicht zuverlässig die Trefferquote, und verschlechterte BTC monoton (Y1 mit T0 von −0.49 R auf −1.20 R bei Potenzial je Risikoeinheit ≥ 1.5). Teilmengen mit positiver Erwartung existierten nur unter 20 Trades (DOT D1 R ≥ 1.5 mit 9 Trades, DOT D3 mit 2) und gelten nach Vorregistrierung nicht als Begründung.

## 3. Was nicht abgeschlossen wird

Die Beobachtung, dass E0 (EMA20-Recovery) auf allen sechs Familien der XRP- und DOT-Läufe die beste Capture Ratio hatte, bleibt als Befund der Cross-Coin-Zusammenfassung v1 bestehen. Die EMA20 bleibt als Kontrollziel Q0 in REBOUND-MICRO. Die Datenklasse (4h-Bottom-Signale, Flow-Merkmale) ist nicht verworfen. Abgeschlossen ist ausschliesslich die Umsetzung «4h-Signal, T0, Strukturstop, EMA20-Ziel, Abstandsbedingung».

## 4. Was daraus in REBOUND-MICRO übergeht

Der strukturelle Grund des Verlusts ist ein zu weiter Invalidationspunkt relativ zum kurzen Ziel: Der 4h-Strukturstop liegt im Median 1.3 bis 2.0 ATR14(4h) unter dem Einstieg, der Weg zur EMA20 im Median 1.0 bis 1.1 Risikoeinheiten darüber. REBOUND-MICRO fragt deshalb nicht nach einem engeren Stop, sondern danach, ob eine bestätigte 1h-Reversal-Struktur einen logisch näheren Invalidationspunkt liefert, ohne dass Stoprate und Kosten den Gewinn aus der Geometrie wieder aufzehren. Das ist eine neue Hypothese mit eigener Vorregistrierung, nicht Version 2 dieser.
