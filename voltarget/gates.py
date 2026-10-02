"""Gates und Kill-Regel KR3 des Vol-Target-Overlays (VOLTARGET_PREREG v0.2 §6-§8). Reine Funktionen auf
taeglichen Equity-Reihen (Listen gleicher Laenge, gleiche Tage). Kein Datenzugriff; wird erst bei der
Leistungsauswertung bzw. am Betriebs-Review verwendet. Schwellen sind GESETZT, nicht hergeleitet (Prereg §7.1, §8.2)."""
import math

ANN = 365
G1_MAXDD_RATIO = 0.90    # G1: |MaxDD_VT| <= 0.90 * |MaxDD_B|            (gesetzt, nicht hergeleitet)
G2_SHARPE_TOL = 0.05     # G2: Sharpe_VT >= Sharpe_B - 0.05                (v0.2, Entscheid Projektleitung)
KR3_COST_LIMIT = 0.01    # KR3: Kosten reiner Vol-Anpassungen <= 1.0 % p. a. (gesetzt, nicht hergeleitet)
GATES = dict(g1_maxdd_ratio=G1_MAXDD_RATIO, g2_sharpe_tol=G2_SHARPE_TOL, kr3_cost_limit=KR3_COST_LIMIT)
EPS = 1e-12


def daily_returns(eq):
    return [eq[i] / eq[i - 1] - 1.0 for i in range(1, len(eq))]


def sharpe(eq, ann=ANN):
    """Mittelwert / Standardabweichung (ddof 1) der taeglichen einfachen Renditen * sqrt(ann); ohne Zinsabzug (Cash 0 %)."""
    r = daily_returns(eq)
    if len(r) < 2:
        return float("nan")
    m = sum(r) / len(r)
    sd = math.sqrt(sum((x - m) ** 2 for x in r) / (len(r) - 1))
    return m / sd * math.sqrt(ann) if sd > 0 else float("nan")


def max_dd(eq):
    peak, dd = -float("inf"), 0.0
    for x in eq:
        peak = max(peak, x)
        dd = min(dd, x / peak - 1.0)
    return dd


def control_factor(w_overlay, E_base):
    """c fuer die Kontrolle C: mittleres Overlay-Gewicht / mittlere Basis-Exposure ueber Coin-Tage mit offener Basis."""
    pairs = [(w, e) for w, e in zip(w_overlay, E_base) if e > EPS]
    if not pairs:
        return float("nan")
    return min(1.0, sum(w for w, _ in pairs) / sum(e for _, e in pairs))


def g2_ok(sh_vt, sh_b, tol=G2_SHARPE_TOL):
    """G2 (v0.2): keine Sharpe-Verschlechterung um mehr als tol: Sharpe_VT >= Sharpe_B - tol."""
    if sh_vt is None or sh_b is None or math.isnan(sh_vt) or math.isnan(sh_b):
        return False
    return sh_vt >= sh_b - tol - EPS


def evaluate(eq_vt, eq_b, eq_c, g1=G1_MAXDD_RATIO, g2_tol=G2_SHARPE_TOL):
    """G1-G3 fuer ein Kostenszenario. Rueckgabe dict mit Kennzahlen, Gate-Flags und ok (alle drei erfuellt)."""
    if not (len(eq_vt) == len(eq_b) == len(eq_c)) or len(eq_vt) < 3:
        raise ValueError("Equity-Reihen ungleich lang oder zu kurz")
    dd_vt, dd_b, dd_c = abs(max_dd(eq_vt)), abs(max_dd(eq_b)), abs(max_dd(eq_c))
    sh_vt, sh_b = sharpe(eq_vt), sharpe(eq_b)
    G1 = dd_vt <= g1 * dd_b + EPS
    G2 = g2_ok(sh_vt, sh_b, g2_tol)
    G3 = dd_vt <= dd_c + EPS
    return dict(maxdd_vt=-dd_vt, maxdd_b=-dd_b, maxdd_c=-dd_c, sharpe_vt=sh_vt, sharpe_b=sh_b,
                G1=G1, G2=G2, G3=G3, ok=G1 and G2 and G3)


def verdict(k1, k2, testable=True):
    """Urteil je Strategie (§7.1/§7.2): k1, k2 = evaluate(...) unter maker_plan bzw. taker_K2."""
    if not testable:
        return "nicht pruefbar"
    if not k1["ok"]:
        return "nicht bestanden"
    if not k2["G2"]:
        return "bestanden mit Kostenvorbehalt"
    return "bestanden"


def kr3_cost_kill(vol_cost_usd, mean_capital_usd, days, limit=KR3_COST_LIMIT):
    """True = Kosten-Kill: annualisierte Kosten der reinen Vol-Anpassungen (Grund "vol") > limit * mittleres Kapital."""
    if days <= 0 or mean_capital_usd <= 0:
        raise ValueError("ungueltige Basis fuer KR3")
    return vol_cost_usd * (ANN / days) / mean_capital_usd > limit + EPS
