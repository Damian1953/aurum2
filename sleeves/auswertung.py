"""Langfrist-Auswertung Sleeve A (MAKRO_LIQ v1.0-Kandidat, NICHT EINGEFROREN) und Status der Leitplanke B (MVRV).

Nur Funktionen, kein Lauf. Wird erst zum Auswertungszeitpunkt (MAKRO_LIQ §7) verwendet.
  - A wird ALLEIN auf dem Niveau 5 % getestet (M5), keine Holm-Korrektur: B ist kein Test und nicht in der Testfamilie.
  - Gates G1-G4 (maker_plan, Cash zu DTB3; G4 = G1-G3 unter taker_K2) entscheiden ueber Kill.
  - Redundanzregel (M4): A besteht alle Gates, Expositions-Korrelation mit W2-BTC (PAPER v1.0) > 0.7 und
    Sharpe A nicht hoeher als Sharpe W2-BTC -> A redundant, keine Micro-Live-Empfehlung.
    Vergleich mit gleicher Cash-Konvention wie PAPER F3 (A-Konto cash0, maker_plan, gleiches Fenster).
  - Calmar und Ulcer-Index sowie Regimephasen > 13 Wochen: nur Bericht, keine Gates.
  - B (MVRV) ist eine Kernbestand-Leitplanke: keine Gates, kein Erfolgsanspruch, kein Trial.
"""
import math

ALPHA_A = 0.05
REDUNDANZ_KORR = 0.7
MIN_WECHSEL, MIN_JAHRE = 10, 3
G2_DD_ANTEIL = 2.0 / 3.0
LEITPLANKE_B = dict(gates=None, trial=False, testfamilie=False, erfolgsanspruch=False,
                    hinweis="Erreicht MVRV 3.5 nicht mehr, loest die Regel nie aus; das ist ein zulaessiges Ergebnis.")


def korrelation(x, y):
    """Pearson-Korrelation zweier gleich langer Reihen; None, wenn eine Reihe konstant oder zu kurz ist."""
    if len(x) != len(y):
        raise ValueError("Reihen ungleich lang")
    n = len(x)
    if n < 2:
        return None
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x); syy = sum((b - my) ** 2 for b in y)
    if sxx == 0 or syy == 0:
        return None
    return sxy / math.sqrt(sxx * syy)


def gates_a(sleeve, b1, b2, sleeve_k2, b1_k2):
    """Argumente: metrics()-Dicts (sharpe, maxdd_pct, cagr_pct). Rueckgabe dict G1..G4 -> bool."""
    def g123(s, b, r):
        return dict(G1=s["sharpe"] is not None and b["sharpe"] is not None and s["sharpe"] >= b["sharpe"],
                    G2=abs(s["maxdd_pct"]) <= G2_DD_ANTEIL * abs(b["maxdd_pct"]),
                    G3=s["cagr_pct"] is not None and r["cagr_pct"] is not None and s["cagr_pct"] > r["cagr_pct"])
    g = g123(sleeve, b1, b2)
    g["G4"] = all(g123(sleeve_k2, b1_k2, b2).values())
    return g


def redundant_a(alle_gates, korr, sharpe_a, sharpe_w2):
    """M4. korr None (nicht bestimmbar) -> nicht redundant, aber im Bericht zu melden."""
    if not alle_gates or korr is None:
        return False
    return korr > REDUNDANZ_KORR and sharpe_a <= sharpe_w2


def verdict_a(gates, p_wert, n_wechsel, jahre, frist_erreicht, korr, sharpe_a_cash0, sharpe_w2):
    """Ergebnis der Langfrist-Auswertung A. p_wert: zweiseitig, Ledoit-Wolf-(2008)-Bootstrap der Sharpe-Differenz A - B1."""
    if not frist_erreicht and (n_wechsel < MIN_WECHSEL or jahre < MIN_JAHRE):
        return "NOCH_NICHT_FAELLIG"
    if n_wechsel < MIN_WECHSEL:
        return "NICHT_PRUEFBAR"
    if not all(gates.values()):
        return "VERWORFEN"
    if p_wert is None or p_wert > ALPHA_A:
        return "NICHT_SIGNIFIKANT"
    if redundant_a(True, korr, sharpe_a_cash0, sharpe_w2):
        return "REDUNDANT"
    return "EMPFEHLUNG_MICRO_LIVE"


def b_identisch_bh(equity):
    """True, solange B seit dem ersten Fill nie ausgestiegen ist (MVRV seit Start nie > 3.5): dann haelt B dieselbe
    Menge BTC wie B1 (gleicher Einstiegstag, gleiche Kosten) und ist mit Buy&Hold identisch."""
    pos = [r["position"] for r in equity[1:]]
    return bool(pos) and all(p == 1 for p in pos)
