"""Aurum II Paper-Engine v1.0 (PAPER_PREREG_v1.0). Keine Keys, keine Orders, nur oeffentliche Kraken-Tageskerzen.

Strategien (Definitionen unveraendert uebernommen):
  W2, W6  : Stufe-2-Vorregistrierung §5/§6/§10 (stage2_preregistration_v1.md); Indikatoren aus dem
            eingefrorenen s2lib (indicators, atr14). Entscheidungslogik 1:1 wie s2lib.run_trend (per Test geprueft).
  T55_20  : Turtle 55/20 laut AURUM_II_FINDINGS_DIGEST_2026-09-15.md §2.1: Einstieg Close > Hoch der letzten 55 Tage
            (ohne laufenden Bar), Ausstieg Close < Tief der letzten 20 Tage, N = Wilder-ATR(20), Notstopp
            Entry - 2N mit Vorrang. Ausfuehrungskonvention wie Stufe 2 (Signal am Schluss t, Fill Eroeffnung t+1).
Start flach: Einstiegssignale erst ab dem Startbar (PAPER_PREREG §4).
"""
import hashlib, importlib.util, json, os
import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S2LIB_PATH = os.path.join(REPO, "01_forschung", "02_strategien", "s2lib.py")
COST_PATH = os.path.join(REPO, "config", "cost_model_v1.json")
COINS = ["BTC", "ETH", "SOL", "XRP", "ADA", "AVAX", "LINK", "DOT", "BNB", "LTC"]  # Stufe-2-Universum §15
STRATS = ["W2", "W6", "T55_20"]
START_BAR = pd.Timestamp("2026-10-02", tz="UTC")       # erster Signalbar (PAPER_PREREG §4)
SLEEVE_USD = 1000.0                                      # virtuelles Kapital je Strategie und Coin
STOP_REASONS = {"stop", "notstopp"}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _load_s2lib():
    spec = importlib.util.spec_from_file_location("s2lib_frozen", S2LIB_PATH)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


S2 = _load_s2lib()


def cost_scenarios(path=COST_PATH):
    """Kosten je Seite aus config/cost_model_v1.json, venue_kraken (C1/C2). Einstieg: fee+fric+slip_in;
    Ausstieg nach Stopp: fee+fric+slip_sl; uebrige Ausstiege: fee+fric+slip_in."""
    v = json.load(open(path))["sections"]["venue_kraken"]["values"]["spot_long_scenarios"]
    out = {}
    for name in ("maker_plan", "taker_K2"):
        s = v[name]
        out[name] = dict(c_in=s["fee"] + s["fric"] + s["slip_in"], c_out=s["fee"] + s["fric"] + s["slip_in"],
                         c_out_stop=s["fee"] + s["fric"] + s["slip_sl"])
    return out


def load_kraken_1d(path, now_utc=None):
    """Nur abgeschlossene Tageskerzen (Bar t ist abgeschlossen, wenn t + 1 Tag <= jetzt)."""
    d = pd.read_csv(path)
    d["t"] = pd.to_datetime(d["t"], utc=True)
    d = d.drop_duplicates("t", keep="last").set_index("t").sort_index()
    for c in ["open", "high", "low", "close"]:
        d[c] = d[c].astype(float)
    now_utc = now_utc or pd.Timestamp.now(tz="UTC")
    d = d[d.index + pd.Timedelta(days=1) <= now_utc]
    return d[["open", "high", "low", "close"]]


def gaps_after(d, ts):
    x = d.index[d.index >= ts - pd.Timedelta(days=1)]
    return int((pd.Series(x).diff().dropna() != pd.Timedelta(days=1)).sum())


def indicators(d):
    ind = S2.indicators(d)                    # eingefroren: atr (Wilder 14), sma200, hh55, ll20, ...
    ind["atr20"] = S2.atr14(d, n=20)          # Turtle N = Wilder-ATR(20), gleiche TR-Definition
    return ind


def decide(d, strat, start_ts="default", ind=None):
    """Signal- und Positionslogik. Rueckgabe: trades (abgeschlossen), offene Position, offene Order fuer die
    naechste Eroeffnung, Entscheidungsprotokoll. Preise in Kurs, Grössen in Bruchteilen des Trade-Kapitals."""
    start_ts = START_BAR if isinstance(start_ts, str) else start_ts
    ind = indicators(d) if ind is None else ind
    idx = d.index; n = len(idx)
    o = d["open"].values; c = d["close"].values
    start_i = int(np.searchsorted(idx.values, start_ts.to_datetime64())) if start_ts is not None else 0
    turtle = strat == "T55_20"
    pyramid = strat == "W6"
    k = 3.0
    sma = ind["sma200"].values; atr = ind["atr"].values; hh = ind["hh55"].values
    ll20 = ind["ll20"].values; n20 = ind["atr20"].values
    u0 = 0.5 if pyramid else 1.0
    pos = 0; units = 0; stop = np.nan; ext = np.nan; last_fill = np.nan
    pending = None; tr = None; trades = []; log = []
    for t in range(n):
        if pending is not None:
            kind, sig_t, reason = pending
            fill = o[t]
            if kind == "ENTRY":
                pos = 1; units = 1
                if turtle:
                    stop = fill - 2.0 * n20[sig_t]
                else:
                    stop = fill - k * atr[sig_t]
                ext = c[t]; last_fill = fill
                tr = dict(entry_sig=idx[sig_t], entry_t=idx[t], entry_fill=fill, units=[(fill, u0, idx[t])])
            elif kind == "ADD":
                units += 1
                stop = max(stop, fill - k * atr[sig_t]); last_fill = fill
                tr["units"].append((fill, 0.25, idx[t]))
            elif kind == "EXIT":
                tr.update(exit_sig=idx[sig_t], exit_t=idx[t], exit_fill=fill, exit_reason=reason)
                trades.append(tr); tr = None; pos = 0; units = 0; stop = np.nan
            log.append(dict(t=idx[t], event="FILL_" + kind, fill=float(fill), reason=reason))
            pending = None
        if turtle:
            if np.isnan(hh[t]) or np.isnan(ll20[t]) or np.isnan(n20[t]):
                continue
            if pos:
                if c[t] <= stop:
                    pending = ("EXIT", t, "notstopp")
                elif c[t] < ll20[t]:
                    pending = ("EXIT", t, "exit20")
            elif t >= start_i and c[t] > hh[t]:
                pending = ("ENTRY", t, "breakout55")
        else:
            lvl = hh[t] if t >= start_i or pos else np.nan   # Start flach: vor dem Startbar kein Einstieg
            if np.isnan(sma[t]) or np.isnan(atr[t]) or np.isnan(lvl):
                continue
            if pos:
                ext = max(ext, c[t])
                stop = max(stop, ext - k * atr[t])
                hit = c[t] <= stop
                gate_off = c[t] < sma[t]
                if hit or gate_off:
                    pending = ("EXIT", t, "stop" if hit else "gate")
                elif pyramid and units < 3 and c[t] > lvl and c[t] >= last_fill + 1.0 * atr[t]:
                    pending = ("ADD", t, "addon")
            elif c[t] > sma[t] and c[t] > lvl:
                pending = ("ENTRY", t, "breakout55")
        if pending is not None and pending[1] == t:
            log.append(dict(t=idx[t], event="SIGNAL_" + pending[0], reason=pending[2], close=float(c[t])))
    open_pos = None
    if tr is not None:
        open_pos = dict(tr, stop=float(stop), n_units=units)
    order = None
    if pending is not None:
        order = dict(kind=pending[0], signal_bar=idx[pending[1]], reason=pending[2],
                     fill_bar=idx[-1] + pd.Timedelta(days=1))
    return dict(trades=trades, open=open_pos, order=order, log=log, last_bar=idx[-1] if n else None)


def account(d, dec, cost, start_ts=None, capital=SLEEVE_USD):
    """Buchhaltung je Sleeve in USD, Zinseszins ueber Trades, Tagesbewertung zum Schluss. Kein Cash-Zins."""
    start_ts = START_BAR if start_ts is None else start_ts
    days = d.index[d.index >= start_ts]
    eq_series = pd.Series(np.nan, index=days)
    eq = capital
    rows = []
    cur = None; base = None; cash = None; costs_paid = 0.0
    allt = dec["trades"] + ([dec["open"]] if dec["open"] else [])
    by_entry = {tr["entry_t"]: tr for tr in allt}
    for day in days:
        if cur is None and day in by_entry:
            cur = by_entry[day]; base = eq; cash = eq; cur["_costs"] = 0.0
        if cur is not None:
            for (f, u, ft) in cur["units"]:
                if ft == day:
                    amt = u * base; fee = amt * cost["c_in"]
                    cash -= amt + fee; cur["_costs"] += fee
            if cur.get("exit_t") == day:
                val = sum(u * base * cur["exit_fill"] / f for f, u, _ in cur["units"])
                co = cost["c_out_stop"] if cur["exit_reason"] in STOP_REASONS else cost["c_out"]
                fee = val * co; cur["_costs"] += fee
                eq_new = cash + val - fee
                gross = sum(u * base * (cur["exit_fill"] / f - 1) for f, u, _ in cur["units"])
                rows.append(dict(entry_signal=str(cur["entry_sig"].date()), entry_date=str(cur["entry_t"].date()),
                                 entry_fill=cur["entry_fill"], n_units=len(cur["units"]),
                                 exit_signal=str(cur["exit_sig"].date()), exit_date=str(day.date()), exit_fill=cur["exit_fill"],
                                 exit_reason=cur["exit_reason"], capital_before=round(base, 4), pnl_gross_usd=round(gross, 4),
                                 costs_usd=round(cur["_costs"], 4), pnl_net_usd=round(eq_new - base, 4),
                                 hold_days=int((day - cur["entry_t"]).days)))
                costs_paid += cur["_costs"]
                eq = eq_new; cur = None
                eq_series[day] = eq
                continue
            close = d.at[day, "close"]
            eq_series[day] = cash + sum(u * base * close / f for f, u, ft in cur["units"] if ft <= day)
        else:
            eq_series[day] = eq
    open_costs = cur["_costs"] if cur is not None else 0.0
    return dict(equity=eq_series, trades=rows, costs_paid=costs_paid + open_costs)


def buy_and_hold(d, cost, start_ts=None, capital=SLEEVE_USD):
    """Kauf zur Eroeffnung des ersten Bars nach dem Startbar, Bewertung zum Schluss netto inkl. hypothetischer
    Ausstiegskosten (c_out)."""
    start_ts = START_BAR if start_ts is None else start_ts
    days = d.index[d.index > start_ts]
    if len(days) == 0:
        return pd.Series(dtype=float)
    f = d.at[days[0], "open"]
    qty_val = capital / (1 + cost["c_in"])
    eq = qty_val * d.loc[days, "close"] / f * (1 - cost["c_out"])
    s = pd.Series(capital, index=d.index[d.index >= start_ts], dtype=float)
    s.loc[days] = eq
    return s


def max_dd(s):
    s = s.dropna()
    if len(s) == 0:
        return 0.0
    return float((s / s.cummax() - 1).min())
