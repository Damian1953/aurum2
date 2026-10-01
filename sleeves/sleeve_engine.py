"""Aurum II Sleeves A (MAKRO_LIQ v0.2) und B (MVRV v0.2): Forward-Paper-Engine, BTC Spot Kraken.

ENTWURF zur Vorregistrierung v0.2 (nicht eingefroren). Getrennt von paper/ (PAPER v1.0). Keine Keys, keine Orders.
Konventionen
  - Kraken-Tagesbar d: Beginn d 00:00 UTC, Schluss (cutoff) d+1 00:00 UTC. Signal am Schluss von d, Fill zur Eroeffnung d+1.
  - Makro-/On-Chain-Beobachtungen zaehlen nur, wenn ihr ERSTER Abruf (first_fetch_utc, Collector 1.2) VOR dem Schluss des
    Signalbars liegt (kein Look-ahead). Massgebend ist der First-Release-Wert.
  - Sleeve B: MVRV neuester Wert mit obs_date <= d-1; INVESTIERT -> CASH bei > 3.5, CASH -> INVESTIERT bei < 1.0;
    Start INVESTIERT, falls MVRV <= 3.5.
  - Sleeve A: Signal nur an Freitagsbars d; w = d-2 (Mittwoch). NL = WALCL - WTREGEN - 1000*RRPONTSYD (RRP: letzter Wert <= w).
    S = 1 wenn NL_w - NL_(w-13 Wochen) > 0. Fehlt H.4.1 fuer w oder w-13: Zustand unveraendert.
  - Fail-closed: Luecke in den Kraken-Tagesbars seit Start, MVRV aelter als 14 Tage, WALCL/WTREGEN aelter als 8 Wochen
    -> Sleeve STOPPED (keine weiteren Buchungen, Meldung).
  - Kosten config/cost_model_v1.json venue_kraken: maker_plan (primaer), taker_K2 (Pflicht-Sensitivitaet);
    Einstieg und Ausstieg je fee+fric+slip_in. Cash primaer ohne Zins, Variante DTB3 (act/360, First-Release).
"""
import csv, datetime as dt, json, math, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COST_PATH = os.path.join(REPO, "config", "cost_model_v1.json")
MVRV_EXIT, MVRV_ENTRY = 3.5, 1.0
MVRV_STALE_DAYS, H41_STALE_DAYS = 14, 56
LOOKBACK_DAYS = 91  # 13 Wochen
CAPITAL = 1000.0
UTC = dt.timezone.utc


class LookAheadError(Exception):
    pass


def parse_utc(s):
    t = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    if t.tzinfo is None:
        raise ValueError(f"Zeit ohne Zone: {s}")
    return t.astimezone(UTC)


def cutoff(d):
    """Schluss des Tagesbars d (= Beginn d+1, UTC)."""
    return dt.datetime.combine(d + dt.timedelta(days=1), dt.time(0), UTC)


def cost_scenarios(path=COST_PATH):
    v = json.load(open(path))["sections"]["venue_kraken"]["values"]["spot_long_scenarios"]
    return {n: dict(c_in=v[n]["fee"] + v[n]["fric"] + v[n]["slip_in"], c_out=v[n]["fee"] + v[n]["fric"] + v[n]["slip_in"])
            for n in ("maker_plan", "taker_K2")}


# ------------------------------------------------------------------ Daten
def load_first_release(path):
    """Collector-1.2-Datei -> sortierte Liste (obs_date, value, first_fetch_utc)."""
    out = []
    if not os.path.exists(path):
        return out
    with open(path, newline="") as fh:
        rd = csv.DictReader(fh)
        for r in rd:
            out.append((dt.date.fromisoformat(r["obs_date"]), float(r["value"]), parse_utc(r["first_fetch_utc"])))
    out.sort(key=lambda x: x[0])
    return out


def load_bars(path):
    """Kraken 1d (Collector) -> Liste (date, open, close)."""
    out = []
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            t = parse_utc(r["t"])
            if (t.hour, t.minute, t.second) != (0, 0, 0):
                raise ValueError(f"1d-Bar nicht auf 00:00 UTC: {r['t']}")
            out.append((t.date(), float(r["open"]), float(r["close"])))
    out.sort()
    return out


def visible(obs, cut, max_date=None):
    """Nur Beobachtungen mit erstem Abruf vor cut (und obs_date <= max_date)."""
    return [o for o in obs if o[2] < cut and (max_date is None or o[0] <= max_date)]


def _check(o, cut):
    if o is not None and not o[2] < cut:
        raise LookAheadError(f"Beobachtung {o[0]} erst {o[2].isoformat()} abgerufen, Signalbar-Schluss {cut.isoformat()}")
    return o


def latest(obs, cut, max_date):
    v = visible(obs, cut, max_date)
    return _check(v[-1], cut) if v else None


def exact(obs, cut, day):
    for o in visible(obs, cut, day):
        if o[0] == day:
            return _check(o, cut)
    return None


# ------------------------------------------------------------------ Signale
def signal_b(mvrv, d, prev_state):
    """Rueckgabe (zustand, info) am Schluss von Bar d. zustand in {INVESTIERT, CASH, STOPPED}."""
    cut = cutoff(d)
    o = latest(mvrv, cut, d - dt.timedelta(days=1))
    if o is None or (d - o[0]).days > MVRV_STALE_DAYS:
        return "STOPPED", dict(reason=f"MVRV fehlt oder aelter als {MVRV_STALE_DAYS} Tage", mvrv_obs=str(o[0]) if o else None)
    x = o[1]; info = dict(mvrv=x, mvrv_obs=str(o[0]), mvrv_first_fetch=o[2].isoformat())
    if prev_state is None:
        return ("INVESTIERT" if x <= MVRV_EXIT else "CASH"), info
    if prev_state == "INVESTIERT" and x > MVRV_EXIT:
        return "CASH", info
    if prev_state == "CASH" and x < MVRV_ENTRY:
        return "INVESTIERT", info
    return prev_state, info


def net_liquidity(walcl, tga, rrp, cut, w):
    a, b, c = exact(walcl, cut, w), exact(tga, cut, w), latest(rrp, cut, w)
    if a is None or b is None or c is None:
        return None, dict(w=str(w), walcl=a and a[1], tga=b and b[1], rrp=c and c[1])
    return a[1] - b[1] - 1000.0 * c[1], dict(w=str(w), walcl=a[1], tga=b[1], rrp=c[1], rrp_obs=str(c[0]))


def signal_a(walcl, tga, rrp, d, prev_state):
    """Nur an Freitagsbars aktiv. Rueckgabe (zustand, info); zustand None = noch kein Signal."""
    if d.weekday() != 4:
        return prev_state, None
    cut = cutoff(d); w = d - dt.timedelta(days=2)
    lw = latest(walcl, cut, w)
    if lw is None or (w - lw[0]).days > H41_STALE_DAYS:
        return "STOPPED", dict(reason=f"WALCL fehlt oder aelter als {H41_STALE_DAYS // 7} Wochen", w=str(w))
    nl, i0 = net_liquidity(walcl, tga, rrp, cut, w)
    nl13, i13 = net_liquidity(walcl, tga, rrp, cut, w - dt.timedelta(days=LOOKBACK_DAYS))
    info = dict(now=i0, lag13=i13)
    if nl is None or nl13 is None:
        info["note"] = "H.4.1 fuer w oder w-13 nicht verfuegbar: Zustand unveraendert"
        return prev_state, info
    info.update(nl=nl, nl13=nl13, delta=nl - nl13)
    return ("INVESTIERT" if nl - nl13 > 0 else "CASH"), info


# ------------------------------------------------------------------ Simulation
def simulate(bars, start, signal_fn, costs, dtb3=None):
    """bars ab Warmup; Signale ab Bar start. Rueckgabe dict(events, equity, status, stop, pending).
    signal_fn(d, prev_state) -> (state, info). Positionen 0/1, Fill zur Eroeffnung des Folgebars."""
    days = [b for b in bars if b[0] >= start]
    status, stop = "OK", None
    for i in range(1, len(days)):  # Luecken seit Start: fail-closed
        if (days[i][0] - days[i - 1][0]).days != 1:
            days = days[:i]; status, stop = "STOPPED", dict(reason=f"Luecke Kraken 1d nach {days[-1][0]}", bar=str(days[-1][0]))
            break
    events, state, target, pending = [], None, 0, None
    acct = {(s, c): dict(cash=CAPITAL, units=0.0) for s in costs for c in ("cash0", "dtb3")}
    bh = {s: None for s in costs}
    equity, sig_stop = [], False
    for k, (d, o, c) in enumerate(days):
        # 1) Fill eines am Vortag beschlossenen Wechsels zur Eroeffnung von d
        if pending is not None:
            for (s, cv), a in acct.items():
                cs = costs[s]
                if pending == 1 and a["units"] == 0:
                    a["units"] = a["cash"] * (1 - cs["c_in"]) / o; a["cash"] = 0.0
                elif pending == 0 and a["units"] > 0:
                    a["cash"] = a["units"] * o * (1 - cs["c_out"]); a["units"] = 0.0
            events.append(dict(key=f"fill|{d}|{pending}", type="fill", bar=str(d), side="kauf" if pending else "verkauf", price=o))
            pending = None
        if k == 1:  # Benchmark B1: Kauf zur Eroeffnung des ersten moeglichen Fill-Tags
            for s in costs:
                bh[s] = CAPITAL * (1 - costs[s]["c_in"]) / o
        # 2) Cash-Verzinsung (Variante dtb3), First-Release vor Bar-Schluss
        r = 0.0
        if dtb3:
            x = latest(dtb3, cutoff(d), d)
            r = (x[1] / 100.0 / 360.0) if x else 0.0
        for (s, cv), a in acct.items():
            if cv == "dtb3" and a["units"] == 0:
                a["cash"] *= 1 + r
        # 3) Signal am Schluss von d
        if not sig_stop:
            new, info = signal_fn(d, state)
            if new == "STOPPED":
                status, stop, sig_stop = "STOPPED", dict(bar=str(d), **(info or {})), True
            elif new is not None and new != state:
                events.append(dict(key=f"signal|{d}|{new}", type="signal", bar=str(d), state=new, prev=state, info=info))
                state = new
                want = 1 if new == "INVESTIERT" else 0
                if want != target:
                    target = want; pending = want
        row = dict(bar=str(d), close=c, state=state or "FLACH", position=target if pending is None else 1 - pending)
        for (s, cv), a in acct.items():
            row[f"eq_{s}_{cv}"] = round(a["cash"] + a["units"] * c, 6)
        for s in costs:
            row[f"bh_{s}"] = round(bh[s] * c * (1 - costs[s]["c_out"]), 6) if bh[s] is not None else CAPITAL
        equity.append(row)
        if sig_stop:
            break
    return dict(events=events, equity=equity, status=status, stop=stop, pending=pending, state=state)


def metrics(equity, col):
    v = [r[col] for r in equity]
    if len(v) < 2:
        return dict(n_days=len(v))
    peak, mdd = v[0], 0.0
    for x in v:
        peak = max(peak, x); mdd = min(mdd, x / peak - 1)
    rets = [v[i] / v[i - 1] - 1 for i in range(1, len(v))]
    m = sum(rets) / len(rets); sd = math.sqrt(sum((x - m) ** 2 for x in rets) / max(1, len(rets) - 1))
    yrs = len(rets) / 365.0
    return dict(n_days=len(v), total_pct=round((v[-1] / v[0] - 1) * 100, 3),
                cagr_pct=round(((v[-1] / v[0]) ** (1 / yrs) - 1) * 100, 3) if yrs >= 1 else None,
                maxdd_pct=round(mdd * 100, 3), sharpe=round(m / sd * math.sqrt(365), 3) if sd > 0 else None)
