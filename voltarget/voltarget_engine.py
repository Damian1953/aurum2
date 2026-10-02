"""Aurum II Vol-Target-Overlay, KANDIDAT v1.0 (VOLTARGET_PREREG_v1.0, nicht eingefroren). Keine Keys, keine Orders, keine Boersenverbindung.

Reines Risiko-Overlay auf die unveraenderten Paper-Sleeves W2, W6 und T55_20 (PAPER_PREREG v1.0):
  - skaliert nur die Positionsgroesse der Basis, erzeugt nie ein eigenes Signal
    (Basis flach  ->  Overlay flach; Overlay-Ziel <= Basis-Exposure <= 1.0);
  - Skalierungsfaktor s_t = min(1, sigma_lang_t / sigma_kurz_t), beide aus Tagesrenditen bis und mit Schluss t
    (kein Look-ahead), Ausfuehrung zur Eroeffnung t+1 wie die Basis;
  - sigma_kurz: EWMA der quadrierten Log-Renditen (Mittelwert 0), Halbwertszeit 20 Tage
    (Harvey et al. 2018, Standard-Halbwertszeit), Fenster 365 Renditen;
  - sigma_lang: gleichgewichtetes RMS derselben 365 Renditen (rollendes Einjahresfenster);
  - Warmup (v0.2): unter 60 verfuegbaren Renditen s = 1; ab 60 Renditen beide Schaetzer ueber die verfuegbare
    Historie (expandierend) bis 365 erreicht sind; echte Luecken/ungueltige Kurse im Fenster -> STOPPED;
  - kein Hebel (MAX_LEV = 1.0), No-Trade-Band 0.10 (absolute Gewichtsabweichung) fuer reine Vol-Anpassungen;
    Basis-Ereignisse (Einstieg, Add-on, Ausstieg) werden immer ausgefuehrt;
  - fail-closed: fehlt eine gueltige Vol-Schaetzung, wird nie Exposure erhoeht (Status STOPPED);
    Basis-Ausstiege werden auch dann ausgefuehrt.
  - Vergleich (v1.0, Review Claude M4): VT, Basis B (s = 1) und Kontrolle C (s = c) laufen durch dieselbe Engine mit
    SYMMETRISCHER Sync-Buchung am Startbar: B uebernimmt eine laufende Basisposition mit Gewicht E, C mit E * c, VT mit
    E * s, alle mit denselben Kosten (Grund "sync"). Sync-Kosten werden getrennt ausgewiesen (costs_by_reason).
Der Kern (dieses Modul) ist reines Python ohne Datenzugriff; Laden und Basis-Ableitung in base_adapter.py.
"""
import json, math, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COST_PATH = os.path.join(REPO, "config", "cost_model_v1.json")

# Vorregistrierte Konstanten (VOLTARGET_PREREG v0.2 §3). Nicht optimiert, nicht aendern ohne neue Version.
HALF_LIFE = 20          # Tage, EWMA-Halbwertszeit sigma_kurz
WINDOW = 365            # Anzahl Tagesrenditen fuer sigma_kurz und sigma_lang
ANN = 365               # Annualisierung (Krypto handelt 7 Tage)
BAND = 0.10             # No-Trade-Band, absolute Abweichung des Gewichts (Anteil Sleeve-Equity)
MAX_LEV = 1.0           # nur reduzieren, nie hebeln
MIN_RETURNS = 60        # Warmup: darunter s = 1, ab hier expandierende Schaetzung bis WINDOW
CAPITAL = 1000.0        # virtuell je Strategie und Coin (wie PAPER F3)
PARAMS = dict(half_life=HALF_LIFE, window=WINDOW, ann=ANN, band=BAND, max_lev=MAX_LEV, capital=CAPITAL,
              min_returns=MIN_RETURNS)
EPS = 1e-12
EVENTS = (None, "entry", "add", "exit", "exit_stop")


class OverlayError(Exception):
    pass


class InvariantError(OverlayError):
    """Verletzung einer Overlay-Invariante (z. B. Position bei flacher Basis). Betriebs-Kill nach Prereg §8."""


def guard_path(p):
    """Datensperre: Holdout- und Validation-Dateien werden nie geladen (ENTSCHEIDE 2026-09-17, 2026-10-01 22:15)."""
    low = str(p).lower()
    if "holdout" in low or "validation" in low:
        raise PermissionError(f"gesperrter Pfad (Holdout/Validation): {p}")
    return p


def cost_scenarios(path=COST_PATH):
    """Wie PAPER F4: venue_kraken maker_plan (= K1, primaer) und taker_K2 (Sensitivitaet), Bruchteile je Seite."""
    v = json.load(open(path))["sections"]["venue_kraken"]["values"]["spot_long_scenarios"]
    out = {}
    for name in ("maker_plan", "taker_K2"):
        s = v[name]
        out[name] = dict(c_in=s["fee"] + s["fric"] + s["slip_in"], c_out=s["fee"] + s["fric"] + s["slip_in"],
                         c_out_stop=s["fee"] + s["fric"] + s["slip_sl"])
    return out


def _finite_pos(x):
    return x is not None and isinstance(x, (int, float)) and math.isfinite(x) and x > 0


def log_returns(closes, dates=None):
    """r_i = ln(c_i / c_{i-1}); None, wenn ein Kurs fehlt/ungueltig ist oder (mit dates) die Tage nicht lueckenlos sind."""
    out = [None]
    for i in range(1, len(closes)):
        a, b = closes[i - 1], closes[i]
        ok = _finite_pos(a) and _finite_pos(b)
        if ok and dates is not None:
            ok = (dates[i] - dates[i - 1]).days == 1
        out.append(math.log(b / a) if ok else None)
    return out


def vol_state(rets, half_life=HALF_LIFE, window=WINDOW, ann=ANN, min_n=MIN_RETURNS):
    """(sigma_kurz, sigma_lang, modus) annualisiert aus den letzten min(len, window) Renditen (letzte = juengste,
    bis Schluss t). rets enthaelt nur echte Renditen (kein Platzhalter fuer den ersten Bar).
    modus: "full" (window Renditen), "expanding" (min_n <= n < window, verfuegbare Historie),
           "warmup" (n < min_n, Skalierung s = 1), "invalid" (fehlende Rendite = Luecke/ungueltiger Kurs im Fenster
           oder Varianz <= 0; fail-closed)."""
    r = list(rets[-window:])
    if any(x is None or not math.isfinite(x) for x in r):
        return None, None, "invalid"
    n = len(r)
    if n < min_n:
        return None, None, "warmup"
    lam = 0.5 ** (1.0 / half_life)
    num = den = 0.0
    for i, x in enumerate(reversed(r)):           # i = 0 juengste Rendite
        w = lam ** i
        num += w * x * x; den += w
    var_s = num / den
    var_l = sum(x * x for x in r) / n
    if not (var_s > 0 and var_l > 0):
        return None, None, "invalid"
    return math.sqrt(var_s * ann), math.sqrt(var_l * ann), ("full" if n >= window else "expanding")


def vol_estimates(rets, half_life=HALF_LIFE, window=WINDOW, ann=ANN, min_n=MIN_RETURNS):
    """(sigma_kurz, sigma_lang) oder (None, None) bei Warmup bzw. ungueltigem Fenster."""
    ss, sl, _ = vol_state(rets, half_life, window, ann, min_n)
    return ss, sl


def scale_for(rets, **kw):
    """(s, modus, sigma_kurz, sigma_lang): s = 1 im Warmup, None bei ungueltigem Fenster (fail-closed)."""
    ss, sl, mode = vol_state(rets, **kw)
    if mode == "warmup":
        return 1.0, mode, None, None
    if mode == "invalid":
        return None, mode, None, None
    return scale_factor(ss, sl), mode, ss, sl


def scale_factor(sig_s, sig_l, max_lev=MAX_LEV):
    """s = min(max_lev, sigma_lang / sigma_kurz); None bei ungueltiger Eingabe (fail-closed)."""
    if not (_finite_pos(sig_s) and _finite_pos(sig_l)):
        return None
    return min(max_lev, sig_l / sig_s)


def target_weight(E, s, max_lev=MAX_LEV):
    """Overlay-Zielgewicht = Basis-Exposure E (0..1, nominell) mal s, nie ueber max_lev, nie ueber E."""
    if E is None or not math.isfinite(E) or E < -EPS or E > max_lev + EPS:
        raise InvariantError(f"Basis-Exposure ausserhalb [0, {max_lev}]: {E}")
    if E <= EPS:
        return 0.0
    if s is None:
        return None
    if not (0.0 <= s <= max_lev + EPS):
        raise InvariantError(f"Skalierung ausserhalb [0, {max_lev}]: {s}")
    return min(max_lev, E * s, E)


def rebalance_target(w_now, E_next, s, event, flat, band=BAND):
    """Zielgewicht fuer die naechste Eroeffnung oder None (kein Trade).
    w_now: aktuelles Overlay-Gewicht (Schluss t); E_next: Basis-Exposure fuer t+1; s: Skalierung aus Schluss t;
    event: Basis-Fill zur Eroeffnung t+1 (None/entry/add/exit/exit_stop); flat: Overlay haelt nichts."""
    if event not in EVENTS:
        raise ValueError(f"unbekanntes Ereignis {event}")
    if E_next <= EPS:
        return 0.0 if not flat else None             # Basis flach -> Overlay flach, nie ein eigenes Signal
    tgt = target_weight(E_next, s)
    if tgt is None:
        return None                                  # fail-closed, Aufrufer setzt STOPPED
    if event in ("entry", "add") or flat:            # Basis-Ereignis oder Synchronisation (Start, Zustandsuebernahme)
        return tgt
    if abs(tgt - w_now) > band:
        return tgt
    return None


def simulate(days, cost, start_idx, next_E=0.0, next_event=None, capital=CAPITAL, band=BAND, scale_override=None):
    """Overlay je Coin. Zustandsuebernahme (§3.7): haelt die Basis am Start (oder spaeter, solange das Overlay flach
    ist) eine Position, wird sie zur naechsten Eroeffnung mit dem aktuellen s skaliert uebernommen (Grund "sync").
    Kostenkonvention wie PAPER F3: Kauf-Nominal = Zielgewicht x Equity vor dem Trade, Kosten zusaetzlich aus dem Cash.
    days: Liste dict(date, open, close, E, event) chronologisch inkl. Warmup vor start_idx;
    E = nominelle Basis-Exposure waehrend des Tages (nach Fills zur Eroeffnung), event = Basis-Fill zur Eroeffnung.
    next_E/next_event: Basis-Zustand fuer den Tag nach dem letzten Bar (offene Order der Basis).
    scale_override: konstantes s (Kontrollrechnung C, Prereg §6) statt Vol-Schaetzung.
    Rueckgabe dict(equity, trades, status, stop, pending)."""
    closes = [d["close"] for d in days]
    dates = [d["date"] for d in days]
    rets = log_returns(closes, dates)
    cash, qty = float(capital), 0.0
    status, stop, pending = "OK", None, None
    equity, trades = [], []
    for i in range(start_idx, len(days)):
        d = days[i]
        o, c, E = d["open"], d["close"], d["E"]
        if i > start_idx and (dates[i] - dates[i - 1]).days != 1:
            status, stop = "STOPPED", dict(date=str(dates[i]), reason="Luecke in den Tageskerzen")
            pending = None
            break
        if not (_finite_pos(o) and _finite_pos(c)):
            status, stop = "STOPPED", dict(date=str(dates[i]), reason="ungueltiger Kurs")
            pending = None
            break
        # ---- Ausfuehrung zur Eroeffnung (Entscheid vom Schluss des Vortags)
        if pending is not None:
            w_tgt, reason = pending
            eq_open = cash + qty * o
            cur = qty * o
            if w_tgt <= EPS and qty > 0:
                val = cur; rate = cost["c_out_stop"] if reason == "exit_stop" else cost["c_out"]
                fee = val * rate; cash += val - fee; qty = 0.0
                trades.append(dict(date=str(dates[i]), side="sell", reason=reason, price=o, value=val, fee=fee, w_target=0.0))
            else:
                tgt_val = w_tgt * eq_open
                if tgt_val > cur + EPS * max(1.0, eq_open):
                    buy = tgt_val - cur
                    if cur + buy > MAX_LEV * eq_open + 1e-9:
                        raise InvariantError("Kauf ueber MAX_LEV")
                    fee = buy * cost["c_in"]; cash -= buy + fee; qty += buy / o
                    trades.append(dict(date=str(dates[i]), side="buy", reason=reason, price=o, value=buy, fee=fee, w_target=w_tgt))
                elif tgt_val < cur - EPS * max(1.0, eq_open):
                    sell = cur - tgt_val; fee = sell * cost["c_out"]; cash += sell - fee; qty -= sell / o
                    trades.append(dict(date=str(dates[i]), side="sell", reason=reason, price=o, value=sell, fee=fee, w_target=w_tgt))
            pending = None
        if E <= EPS and qty > 0:
            raise InvariantError(f"{dates[i]}: Overlay-Position bei flacher Basis (Signalerzeugung)")
        # ---- Bewertung zum Schluss
        eq = cash + qty * c
        w = qty * c / eq if eq > 0 else 0.0
        if scale_override is None:
            s, mode, ss, sl = scale_for(rets[1: i + 1])           # rets[0] ist der Platzhalter des ersten Bars
        else:
            ss = sl = None; s = float(scale_override); mode = "override"
        equity.append(dict(date=str(dates[i]), equity=eq, cash=cash, weight=w, E=E, scale=s, vol_mode=mode,
                           sig_short=ss, sig_long=sl, status=status))
        # ---- Entscheid fuer die Eroeffnung t+1
        if i + 1 < len(days):
            E_n, ev_n = days[i + 1]["E"], days[i + 1]["event"]
        else:
            E_n, ev_n = next_E, next_event
        flat = qty <= 0
        if status == "STOPPED":
            if E_n <= EPS and not flat:
                pending = (0.0, ev_n or "exit")      # Ausstiege der Basis immer
            continue
        if E_n > EPS and s is None:
            status, stop = "STOPPED", dict(date=str(dates[i]), reason="keine gueltige Vol-Schaetzung (Luecke/ungueltiger Kurs im Fenster oder Varianz 0, fail-closed)")
            equity[-1]["status"] = status
            continue
        tgt = rebalance_target(w, E_n, s, ev_n, flat, band)
        if tgt is not None:
            if tgt > E_n + EPS or tgt > MAX_LEV + EPS or tgt < 0:
                raise InvariantError(f"Ziel {tgt} ueber Basis-Exposure {E_n}")
            reason = ev_n if ev_n else ("sync" if flat else "vol")
            pending = (tgt, reason)
    return dict(equity=equity, trades=trades, status=status, stop=stop,
                pending=None if pending is None else dict(w_target=pending[0], reason=pending[1]))


# ------------------------------------------------------------------ Vergleich VT / B / C (v1.0, Prereg §3.7, §6)
def run_compare(days, cost, start_idx, next_E=0.0, next_event=None, c=None, capital=CAPITAL):
    """VT (Vol-Skalierung, Band), B (s = 1, ohne Vol-Anpassungen) und optional C (s = c konstant, ohne Vol-Anpassungen).
    Alle drei mit derselben Engine und derselben Sync-Buchung am Startbar (Gewicht E * s, E * 1 bzw. E * c, gleiche
    Kosten). Rueckgabe dict(vt=..., b=..., c=... oder None)."""
    inf = float("inf")
    vt = simulate(days, cost, start_idx, next_E, next_event, capital=capital)
    b = simulate(days, cost, start_idx, next_E, next_event, capital=capital, band=inf, scale_override=1.0)
    cc = None if c is None else simulate(days, cost, start_idx, next_E, next_event, capital=capital, band=inf, scale_override=c)
    return dict(vt=vt, b=b, c=cc)


def costs_by_reason(trades):
    """Kosten in USD je Trade-Grund (sync, entry, add, exit, exit_stop, vol)."""
    out = {}
    for t in trades:
        out[t["reason"]] = out.get(t["reason"], 0.0) + t["fee"]
    return out


def sync_costs(trades):
    """Kosten der Zustandsuebernahme (Grund "sync"), getrennt ausgewiesen (Prereg §6)."""
    return costs_by_reason(trades).get("sync", 0.0)


def scale_distribution(equity):
    """Verteilung von s je Coin (nur Bericht): Tage, Tage mit s < 1, Coin-Tage mit offener Basis und s < 1,
    Minimum und Mittel von s, Klassen [<0.5, 0.5-0.8, 0.8-1, =1]."""
    xs = [(e["scale"], e["E"]) for e in equity if e.get("scale") is not None]
    lt = [s for s, _ in xs if s < 1.0 - EPS]
    return dict(tage=len(xs), tage_s_lt_1=len(lt),
                tage_offen=sum(1 for _, E in xs if E > EPS),
                tage_offen_s_lt_1=sum(1 for s, E in xs if E > EPS and s < 1.0 - EPS),
                s_min=min((s for s, _ in xs), default=None),
                s_mittel=(sum(s for s, _ in xs) / len(xs)) if xs else None,
                klassen={"<0.5": sum(1 for s in lt if s < 0.5), "0.5-0.8": sum(1 for s in lt if 0.5 <= s < 0.8),
                         "0.8-1": sum(1 for s in lt if s >= 0.8), "=1": len(xs) - len(lt)})
