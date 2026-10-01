# PORTABLE VERSION, generiert von tools/make_portable.py. NICHT VON HAND AENDERN.
# Quelle (eingefroren): 01_forschung/02_strategien/s2lib.py  sha256 54590393170f6f2263663ba9ab1422a5bc3083b55fa913a38022e6e54d983792
# Regeln: cost:COST=stage2_perp, cost:SPOT_REF=stage2_spot_ref. Arbeitsbereich: AURUM_ROOT (Default: Ordner '..' relativ zu dieser Datei).
import os as _aos; _AR = _aos.environ.get("AURUM_ROOT") or _aos.path.abspath(_aos.path.join(_aos.path.dirname(_aos.path.abspath(__file__)), ".."))
try:
    import aurum_costs as _ac
except ImportError:
    import sys as _asys; _asys.path.append(_aos.path.join(_AR, "pylib")); import aurum_costs as _ac
#!/usr/bin/env python3
"""
Project Aurum II — Stufe 2, Bibliothek
Umsetzung der eingefrorenen Vorregistrierung stage2_preregistration_v1.md (SHA-256 8f576b7a…).

Konventionen
- Signal am Schluss von Bar t, Ausfuehrung zur Eroeffnung von Bar t+1. Gilt auch fuer Stopps.
- Gewicht w_t ist die Position, die waehrend Tag t gehalten wird (gesetzt zur Eroeffnung t).
- Tagesrendite eines Sleeves = w_t * (Open_{t+1}/Open_t - 1)  - Kosten(|w_t - w_{t-1}|) + Funding + Cash.
- Kurse: Spot (lange Historie). Kostenmodell: Perpetual. Funding: Binance USDT-M je Zahlungszeitpunkt.
"""
import os, json, math
import numpy as np
import pandas as pd

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
COINS = ["BTC", "ETH", "SOL", "XRP", "ADA", "AVAX", "LINK", "DOT", "BNB", "LTC"]
CORE = ["BTC", "ETH"]
DAYS = 365

# ----------------------------------------------------------------------------- eingefrorene Kosten (je Seite, Bruchteil)
COST = _ac.load("stage2_perp")  # zentral: config/cost_model_v1.json [stage2_perp]
SPOT_REF = _ac.load("stage2_spot_ref")   # Spot-Referenz, kein Funding  # zentral: config/cost_model_v1.json [stage2_spot_ref]

BLOCKS = [("P1", "2017-08-17", "2020-12-31"), ("P2", "2021-01-01", "2023-12-31"), ("P3", "2024-01-01", "2026-12-31")]
TRADE_CLASS = {"S": (100, 30), "M": (60, 15), "L": (30, 8)}


# ----------------------------------------------------------------------------- Daten
def load_ohlc(path):
    d = pd.read_csv(path)
    d["t"] = pd.to_datetime(d["t"], utc=True)
    d = d.set_index("t").sort_index()
    for c in ["open", "high", "low", "close", "volume"]:
        d[c] = d[c].astype(float)
    return d


def load_tbill():
    t = pd.read_csv(os.path.join(RAW, "DTB3_3m_tbill.csv"))
    t["observation_date"] = pd.to_datetime(t["observation_date"], utc=True)
    s = t.set_index("observation_date")["DTB3"].astype(float) / 100.0
    return s


def load_funding(coin):
    p = os.path.join(RAW, "binance_funding", f"{coin}USDT_funding.csv")
    if not os.path.exists(p):
        return None
    f = pd.read_csv(p)
    f["t"] = pd.to_datetime(f["t"], utc=True, format="ISO8601").dt.floor("h")
    f = f.set_index("t").sort_index()
    f["rate"] = f["rate"].astype(float)
    f["interval_hours"] = pd.to_numeric(f["interval_hours"], errors="coerce").fillna(8.0)
    return f


def load_oi(coin):
    p = os.path.join(RAW, "binance_oi", f"{coin}USDT_oi_1d.csv")
    if not os.path.exists(p):
        return None
    o = pd.read_csv(p)
    o["t"] = pd.to_datetime(o["t"], utc=True)
    o = o.set_index("t").sort_index()
    o["oi"] = o["oi"].astype(float)
    return o


class CoinData:
    """Alle Reihen eines Coins auf dem Spot-Tagesraster ausgerichtet."""

    def __init__(self, coin, tbill):
        self.coin = coin
        self.spot = load_ohlc(os.path.join(RAW, "binance", f"{coin}USDT_1d.csv"))
        pp = os.path.join(RAW, "binance_perp", f"{coin}USDT_1d.csv")
        self.perp = load_ohlc(pp) if os.path.exists(pp) else None
        self.funding = load_funding(coin)
        self.oi = load_oi(coin)
        idx = self.spot.index
        self.idx = idx
        o = self.spot["open"].values
        # Open-zu-Open-Rendite fuer Tag t (Position von Open t bis Open t+1). Letzter Tag undefiniert.
        r = np.full(len(o), np.nan)
        r[:-1] = o[1:] / o[:-1] - 1
        self.r_o2o = pd.Series(r, index=idx)
        # Cash: T-Bill, auf Tagesraster, vorwaerts gefuellt, als Tagesrate
        tb = tbill.reindex(idx.union(tbill.index)).sort_index().ffill().reindex(idx).fillna(0.0)
        self.cash_daily = (1 + tb) ** (1 / DAYS) - 1
        # Funding je Tag: Summe der Raten mit Zeitstempel im Tag t (UTC). Long zahlt positive Rate.
        fd = pd.Series(0.0, index=idx)
        fdef = pd.Series(False, index=idx)
        if self.funding is not None:
            g = self.funding["rate"].groupby(self.funding.index.floor("D")).sum()
            fd = g.reindex(idx).fillna(0.0)
            fdef = g.reindex(idx).notna()
            # f_7d: Summe der Raten der letzten 7 Tage, annualisiert
            self.f7 = (self.funding["rate"].rolling("7D").sum() * (365 / 7))
            self.f7_daily = self.f7.groupby(self.f7.index.floor("D")).last().reindex(idx)
            self.f3_daily = (self.funding["rate"].rolling("3D").sum() * (365 / 3)).groupby(self.funding.index.floor("D")).last().reindex(idx)
            self.f14_daily = (self.funding["rate"].rolling("14D").sum() * (365 / 14)).groupby(self.funding.index.floor("D")).last().reindex(idx)
        else:
            self.f7_daily = self.f3_daily = self.f14_daily = pd.Series(np.nan, index=idx)
        self.fund_day = fd
        self.fund_defined = fdef
        # Perp-Reihen auf Spot-Raster (fuer D-CC)
        if self.perp is not None:
            po = self.perp["open"].reindex(idx)
            rp = np.full(len(po), np.nan)
            pov = po.values
            rp[:-1] = pov[1:] / pov[:-1] - 1
            self.r_perp = pd.Series(rp, index=idx)
        else:
            self.r_perp = pd.Series(np.nan, index=idx)


# ----------------------------------------------------------------------------- Indikatoren (identisch zu Stufe 1)
def wilder(series, n):
    x = series.values.astype(float)
    out = np.full_like(x, np.nan)
    if len(x) < n:
        return pd.Series(out, index=series.index)
    out[n - 1] = np.nanmean(x[:n])
    for i in range(n, len(x)):
        out[i] = (out[i - 1] * (n - 1) + x[i]) / n
    return pd.Series(out, index=series.index)


def atr14(d, n=14):
    h, l, c = d["high"], d["low"], d["close"]
    pc = c.shift(1)
    tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    return wilder(tr.iloc[1:], n).reindex(d.index)


def indicators(d):
    ind = pd.DataFrame(index=d.index)
    c = d["close"]
    ind["atr"] = atr14(d)
    for n in (150, 200, 250):
        ind[f"sma{n}"] = c.rolling(n).mean()
    ind["sma20"] = c.rolling(20).mean()
    ind["sd20"] = c.rolling(20).std(ddof=1)
    for n in (10, 30):
        ind[f"sma{n}"] = c.rolling(n).mean()
        ind[f"sd{n}"] = c.rolling(n).std(ddof=1)
    for N in (20, 40, 55, 80, 100, 252):
        ind[f"hh{N}"] = d["high"].shift(1).rolling(N).max()
        ind[f"ll{N}"] = d["low"].shift(1).rolling(N).min()
    for L in (7, 16, 21, 26, 42, 47, 63, 79, 95, 126, 158):
        ind[f"ret{L}"] = c / c.shift(L) - 1
    return ind


# ----------------------------------------------------------------------------- Simulator
def simulate(cd, w, cost, extra=None):
    """
    w: Gewicht je Tag (Position waehrend Tag t). cost: dict aus COST.
    extra: optional dict mit 'w_perp' (zweites Bein auf Perp-Kursen) fuer D-CC. Dann gilt:
       w = Spot-Bein (Spot-Kosten), w_perp = Perp-Bein (Perp-Kosten, Funding).
    Rueckgabe DataFrame mit gross, cost, funding, cash, net, turnover.
    """
    idx = cd.idx
    w = w.reindex(idx).fillna(0.0)
    r = cd.r_o2o
    if extra is None:
        gross = w * r
        dw = w.diff().fillna(w)
        turnover = dw.abs()
        costs = turnover * (cost["fee"] + cost["fric"])
        fpnl = -w * cd.fund_day
        fpnl = np.where(fpnl < 0, fpnl * cost["fund_pay"], fpnl)
        fpnl = pd.Series(fpnl, index=idx)
        cash = (1 - w.abs()).clip(lower=0) * cd.cash_daily
        expo = w.abs()
    else:
        wp = extra["w_perp"].reindex(idx).fillna(0.0)
        gross = w * r + wp * cd.r_perp.fillna(0.0)
        dw = w.diff().fillna(w); dwp = wp.diff().fillna(wp)
        turnover = dw.abs() + dwp.abs()
        costs = dw.abs() * (cost["spot_fee"] + cost["spot_fric"]) + dwp.abs() * (cost["fee"] + cost["fric"])
        fpnl = -wp * cd.fund_day
        fpnl = np.where(fpnl < 0, fpnl * cost["fund_pay"], fpnl)
        fpnl = pd.Series(fpnl, index=idx)
        cash = (1 - w.abs()).clip(lower=0) * cd.cash_daily
        expo = (w.abs() + wp.abs()) / 2
    net = gross + fpnl + cash - costs
    out = pd.DataFrame(dict(w=w, gross=gross, cost=costs, funding=fpnl, cash=cash, net=net, turnover=turnover, expo=expo), index=idx)
    out.loc[r.isna(), ["gross", "net"]] = np.nan
    return out


# ----------------------------------------------------------------------------- Familie A, Trendfolge (Woo-Matrix)
def run_trend(cd, ind, side=+1, mode="breakout", N=55, k=3.0, gate=True, sma_n=200, pyramid=False):
    """
    mode 'breakout': Einstieg Close > HH(N) [Short: Close < LL(N)], ATR-Stopp nachziehend, Gate-Exit.
    mode 'cross':    W0, Kreuzung SMA, kein Stopp.
    Rueckgabe: w (Series), trades (Liste dicts).
    """
    idx = cd.idx
    n = len(idx)
    c = cd.spot["close"].values; o = cd.spot["open"].values
    sma = ind[f"sma{sma_n}"].values
    atr = ind["atr"].values
    lvl = ind[f"hh{N}"].values if side > 0 else ind[f"ll{N}"].values
    w = np.zeros(n)
    trades = []
    pos = 0; units = 0; wcur = 0.0; stop = np.nan; ext = np.nan; last_fill = np.nan
    pending = None
    tr = None
    u0 = 0.5 if pyramid else 1.0
    fund_day = cd.fund_day.values
    for t in range(n):
        # 1) Ausfuehrung zur Eroeffnung t
        if pending is not None:
            kind, sig_t = pending
            fill = o[t]
            if kind == "ENTRY":
                pos = 1; units = 1; wcur = u0 * side
                a = atr[sig_t]
                stop = fill - side * k * a if mode == "breakout" else np.nan
                ext = c[t]  # hoechster (tiefster) Schluss seit Einstieg, beginnt mit Schluss des Fill-Tags (unten aktualisiert)
                last_fill = fill
                tr = dict(entry_t=t, entry_fill=fill, side=side, units=[(fill, u0)], risk0=(k * a / fill) * u0 if mode == "breakout" else np.nan,
                          funding=0.0, cost_sides=1)
            elif kind == "ADD":
                units += 1; wcur += 0.25 * side
                a = atr[sig_t]
                stop = max(stop, fill - k * a) if side > 0 else min(stop, fill + k * a)
                last_fill = fill
                tr["units"].append((fill, 0.25)); tr["cost_sides"] += 1
            elif kind == "EXIT":
                # P&L in Bruchteilen des Sleeve-Kapitals
                pnl = sum(u * side * (fill / f - 1) for f, u in tr["units"])
                notional = sum(u for _, u in tr["units"])
                tr.update(exit_t=t, exit_fill=fill, exit_reason=pending_reason, pnl_gross=pnl, notional=notional,
                          hold=t - tr["entry_t"], n_units=len(tr["units"]))
                trades.append(tr); tr = None
                pos = 0; units = 0; wcur = 0.0; stop = np.nan
            pending = None
        w[t] = wcur
        if pos:
            tr["funding"] += -wcur * fund_day[t]
        # 2) Signale am Schluss t (nur wenn Daten definiert)
        if t >= n - 1:
            break
        if np.isnan(sma[t]) or np.isnan(atr[t]) or (mode == "breakout" and np.isnan(lvl[t])):
            continue
        if pos:
            if mode == "breakout":
                # Trailing aktualisieren, dann Exit pruefen
                ext = max(ext, c[t]) if side > 0 else min(ext, c[t])
                stop = max(stop, ext - k * atr[t]) if side > 0 else min(stop, ext + k * atr[t])
                hit = (c[t] <= stop) if side > 0 else (c[t] >= stop)
                gate_off = gate and ((c[t] < sma[t]) if side > 0 else (c[t] > sma[t]))
                if hit or gate_off:
                    pending = ("EXIT", t); pending_reason = "stop" if hit else "gate"
                elif pyramid and units < 3:
                    brk = (c[t] > lvl[t]) if side > 0 else (c[t] < lvl[t])
                    dist = (c[t] >= last_fill + 1.0 * atr[t]) if side > 0 else (c[t] <= last_fill - 1.0 * atr[t])
                    if brk and dist:
                        pending = ("ADD", t)
            else:  # cross
                if t >= 1 and ((c[t] < sma[t]) if side > 0 else (c[t] > sma[t])):
                    pending = ("EXIT", t); pending_reason = "cross"
        else:
            if mode == "breakout":
                ok_gate = (not gate) or ((c[t] > sma[t]) if side > 0 else (c[t] < sma[t]))
                brk = (c[t] > lvl[t]) if side > 0 else (c[t] < lvl[t])
                if ok_gate and brk:
                    pending = ("ENTRY", t)
            else:
                if t >= 1 and not np.isnan(sma[t - 1]):
                    cross = (c[t] > sma[t] and c[t - 1] <= sma[t - 1]) if side > 0 else (c[t] < sma[t] and c[t - 1] >= sma[t - 1])
                    if cross:
                        pending = ("ENTRY", t)
    return pd.Series(w, index=idx), trades


# ----------------------------------------------------------------------------- Familie B, Mean Reversion
def run_mr(cd, ind, side=+1, z_thr=2.0, n=20, hold_max=10, k=3.0):
    idx = cd.idx; N = len(idx)
    c = cd.spot["close"].values; o = cd.spot["open"].values
    sma = ind[f"sma{n}"].values; sd = ind[f"sd{n}"].values; atr = ind["atr"].values
    w = np.zeros(N); trades = []; pos = 0; wcur = 0.0; pending = None; tr = None; stop = np.nan
    fund_day = cd.fund_day.values
    for t in range(N):
        if pending is not None:
            kind, sig_t = pending
            fill = o[t]
            if kind == "ENTRY":
                pos = 1; wcur = 1.0 * side
                stop = fill - side * k * atr[sig_t]
                tr = dict(entry_t=t, entry_fill=fill, side=side, units=[(fill, 1.0)], risk0=k * atr[sig_t] / fill, funding=0.0, cost_sides=1)
            else:
                pnl = side * (fill / tr["entry_fill"] - 1)
                tr.update(exit_t=t, exit_fill=fill, exit_reason=pending_reason, pnl_gross=pnl, notional=1.0, hold=t - tr["entry_t"], n_units=1)
                trades.append(tr); tr = None; pos = 0; wcur = 0.0
            pending = None
        w[t] = wcur
        if pos:
            tr["funding"] += -wcur * fund_day[t]
        if t >= N - 1:
            break
        if np.isnan(sma[t]) or np.isnan(sd[t]) or sd[t] == 0 or np.isnan(atr[t]):
            continue
        z = (c[t] - sma[t]) / sd[t]
        if pos:
            back = (c[t] >= sma[t]) if side > 0 else (c[t] <= sma[t])
            hit = (c[t] <= stop) if side > 0 else (c[t] >= stop)
            timeout = (t - tr["entry_t"]) >= hold_max
            if back or hit or timeout:
                pending = ("EXIT", t); pending_reason = "mean" if back else ("stop" if hit else "time")
        else:
            if (z <= -z_thr) if side > 0 else (z >= z_thr):
                pending = ("ENTRY", t)
    return pd.Series(w, index=idx), trades


# ----------------------------------------------------------------------------- Gewichtsbasierte Strategien: Trades aus Gewichtsaenderungen
def trades_from_weights(cd, w, fund_day=None):
    """Jede Positionsaenderung mit anschliessender Halteperiode zaehlt als Trade (fuer Familie C und D)."""
    idx = cd.idx; o = cd.spot["open"].values; wv = w.reindex(idx).fillna(0.0).values
    fd = cd.fund_day.values if fund_day is None else fund_day
    trades = []; cur = None
    for t in range(len(idx)):
        if t == 0 or wv[t] != wv[t - 1]:
            if cur is not None and cur["w"] != 0:
                cur.update(exit_t=t, exit_fill=o[t], pnl_gross=cur["w"] * (o[t] / cur["entry_fill"] - 1), hold=t - cur["entry_t"],
                           notional=abs(cur["w"]), side=np.sign(cur["w"]), n_units=1, exit_reason="rebalance", risk0=np.nan, cost_sides=1)
                trades.append(cur)
            cur = dict(entry_t=t, entry_fill=o[t], w=wv[t], funding=0.0) if wv[t] != 0 else None
        # Funding faellt an den Tagen an, an denen die Position gehalten wird (Open t bis Open t+1), wie in simulate()
        if cur is not None:
            cur["funding"] += -wv[t] * fd[t]
    return trades


def weights_ts(cd, ind, L=21, H=7, side=0):
    """Time-Series-Momentum: alle H Bars w = sign(ret_L). side 0 = long+short, +1 long-only, -1 short-only."""
    idx = cd.idx; r = ind[f"ret{L}"].values; n = len(idx)
    w = np.zeros(n); cur = 0.0
    start = next((i for i in range(n) if not np.isnan(r[i])), None)
    if start is None:
        return pd.Series(w, index=idx)
    for t in range(n):
        if t >= start and (t - start) % H == 0 and not np.isnan(r[t]):
            s = np.sign(r[t])
            if side > 0: s = max(s, 0)
            if side < 0: s = min(s, 0)
            cur = float(s)
        # Signal am Schluss t wirkt ab Tag t+1
        if t + 1 < n:
            w[t + 1] = cur
    return pd.Series(w, index=idx)


def weights_fc(cd, scale=0.30, window="7", H=7, side=0):
    f = {"7": cd.f7_daily, "3": cd.f3_daily, "14": cd.f14_daily}[window].values
    idx = cd.idx; n = len(idx); w = np.zeros(n); cur = 0.0
    start = next((i for i in range(n) if not np.isnan(f[i])), None)
    if start is None:
        return pd.Series(w, index=idx)
    for t in range(n):
        if t >= start and (t - start) % H == 0 and not np.isnan(f[t]):
            s = float(np.clip(-f[t] / scale, -1, 1))
            if side > 0: s = max(s, 0)
            if side < 0: s = min(s, 0)
            cur = s
        if t + 1 < n:
            w[t + 1] = cur
    return pd.Series(w, index=idx)


def weights_oi(cd, ind, W=7, H=7, side=0):
    idx = cd.idx; n = len(idx)
    if cd.oi is None:
        return pd.Series(np.zeros(n), index=idx)
    oi = cd.oi["oi"].reindex(idx).values
    c = cd.spot["close"].values
    w = np.zeros(n); cur = 0.0
    start = next((i for i in range(W, n) if not np.isnan(oi[i]) and not np.isnan(oi[i - W])), None)
    if start is None:
        return pd.Series(w, index=idx)
    for t in range(n):
        if t >= start and (t - start) % H == 0 and not np.isnan(oi[t]) and not np.isnan(oi[t - W]):
            d_oi = oi[t] / oi[t - W] - 1
            s = float(np.sign(c[t] / c[t - W] - 1)) if d_oi > 0 else 0.0
            if side > 0: s = max(s, 0)
            if side < 0: s = min(s, 0)
            cur = s
        if t + 1 < n:
            w[t + 1] = cur
    return pd.Series(w, index=idx)


def weights_cc(cd, thr=0.10, window="7"):
    """Cash-and-Carry: Spot long 1.0 und Perp short 1.0, ein bei f >= thr, aus bei f <= 0."""
    f = {"7": cd.f7_daily, "3": cd.f3_daily, "14": cd.f14_daily}[window].values
    idx = cd.idx; n = len(idx); ws = np.zeros(n); on = False
    perp_ok = ~cd.r_perp.isna().values
    for t in range(n):
        if not np.isnan(f[t]) and perp_ok[t]:
            if not on and f[t] >= thr: on = True
            elif on and f[t] <= 0: on = False
        if t + 1 < n:
            ws[t + 1] = 1.0 if on else 0.0
    ws = pd.Series(ws, index=idx)
    return ws, -ws


# ----------------------------------------------------------------------------- Kennzahlen
def equity_stats(net, cash_daily=None):
    """net: taegliche Nettorenditen (NaN am Ende erlaubt)."""
    x = net.dropna()
    if len(x) < 30:
        return None
    eq = (1 + x).cumprod()
    yrs = len(x) / DAYS
    cagr = eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan
    dd = eq / eq.cummax() - 1
    maxdd = dd.min()
    ex = x - (cash_daily.reindex(x.index).fillna(0.0) if cash_daily is not None else 0.0)
    sharpe = ex.mean() / ex.std(ddof=1) * math.sqrt(DAYS) if ex.std(ddof=1) > 0 else np.nan
    down = ex[ex < 0]
    sortino = ex.mean() / down.std(ddof=1) * math.sqrt(DAYS) if len(down) > 5 and down.std(ddof=1) > 0 else np.nan
    calmar = cagr / abs(maxdd) if maxdd < 0 else np.nan
    ulcer = math.sqrt((dd ** 2).mean())
    yearly = eq.resample("YE").last().pct_change()
    yearly.iloc[0] = eq.resample("YE").last().iloc[0] - 1
    roll = eq / eq.shift(DAYS) - 1
    return dict(cagr=cagr, maxdd=maxdd, sharpe=sharpe, sortino=sortino, calmar=calmar, ulcer=ulcer,
                worst_year=float(yearly.min()), worst_roll12=float(roll.min()) if roll.notna().any() else np.nan,
                vol=ex.std(ddof=1) * math.sqrt(DAYS), n_days=len(x), years=yrs,
                yearly={str(k.year): float(v) for k, v in yearly.items()})


def trade_stats(trades, cost):
    """Netto je Trade: brutto - Kosten (Seiten * Notional * Satz) + Funding (K2-Asymmetrie naeherungsweise auf Sleeve-Ebene)."""
    if not trades:
        return dict(n=0)
    per_side = cost["fee"] + cost["fric"]
    pn = []
    for tr in trades:
        if "spot_notional" in tr:   # D-CC: Spot-Beine mit Spot-Kostenmodell, Perp-Beine mit Perp-Kostenmodell
            cost_amt = 2 * tr["spot_notional"] * (cost["spot_fee"] + cost["spot_fric"]) + 2 * tr["perp_notional"] * per_side
        elif "units" in tr:
            cost_amt = per_side * (sum(u for _, u in tr["units"]) * 2)
        else:
            cost_amt = per_side * 2 * tr["notional"]
        f = tr["funding"]
        if f < 0: f *= cost["fund_pay"]
        pn.append(tr["pnl_gross"] - cost_amt + f)
    pn = np.array(pn)
    wins = pn[pn > 0]; losses = pn[pn <= 0]
    gross_profit = wins.sum(); gross_loss = -losses.sum()
    R = np.array([ (p / tr["risk0"]) if (tr.get("risk0") and not np.isnan(tr["risk0"]) and tr["risk0"] > 0) else np.nan for p, tr in zip(pn, trades)])
    Rv = R[~np.isnan(R)]
    srt = np.sort(pn)[::-1]
    top10 = srt[:max(1, int(math.ceil(len(pn) * 0.10)))].sum()
    top5 = srt[:5].sum()
    return dict(n=len(pn), expectancy=float(pn.mean()), win_rate=float((pn > 0).mean()), median=float(np.median(pn)),
                avg_win=float(wins.mean()) if len(wins) else np.nan, avg_loss=float(losses.mean()) if len(losses) else np.nan,
                gain_loss=float(wins.mean() / -losses.mean()) if len(wins) and len(losses) and losses.mean() < 0 else np.nan,
                profit_factor=float(gross_profit / gross_loss) if gross_loss > 0 else np.nan,
                avg_hold=float(np.mean([tr["hold"] for tr in trades])),
                avg_hold_win=float(np.mean([tr["hold"] for tr, p in zip(trades, pn) if p > 0])) if len(wins) else np.nan,
                top10_share=float(top10 / gross_profit) if gross_profit > 0 else np.nan,
                top5_share=float(top5 / gross_profit) if gross_profit > 0 else np.nan,
                worst5=[float(x) for x in np.sort(pn)[:5]],
                R=dict(n=int(len(Rv)), mean=float(Rv.mean()) if len(Rv) else None, median=float(np.median(Rv)) if len(Rv) else None,
                       p5=float(np.percentile(Rv, 5)) if len(Rv) else None, p25=float(np.percentile(Rv, 25)) if len(Rv) else None,
                       p75=float(np.percentile(Rv, 75)) if len(Rv) else None, p90=float(np.percentile(Rv, 90)) if len(Rv) else None,
                       p95=float(np.percentile(Rv, 95)) if len(Rv) else None,
                       skew=float(pd.Series(Rv).skew()) if len(Rv) > 3 else None,
                       share_le_m1=float((Rv <= -1).mean()) if len(Rv) else None),
                pnl=[float(p) for p in pn])


# ----------------------------------------------------------------------------- Statistik
def block_bootstrap(x, n_rep=2000, mean_block=20, seed=7):
    """Stationaerer Block-Bootstrap (Politis-Romano). x: 1D array. Rueckgabe: Array der Mittelwerte und Sharpes."""
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=float); T = len(x); p = 1.0 / mean_block
    means = np.empty(n_rep); sharpes = np.empty(n_rep)
    for b in range(n_rep):
        idx = np.empty(T, dtype=int)
        i = 0
        while i < T:
            start = rng.integers(0, T)
            L = rng.geometric(p)
            L = min(L, T - i)
            idx[i:i + L] = (start + np.arange(L)) % T
            i += L
        s = x[idx]
        m = s.mean(); sd = s.std(ddof=1)
        means[b] = m; sharpes[b] = m / sd * math.sqrt(DAYS) if sd > 0 else 0.0
    return means, sharpes


def trade_bootstrap(pnl, n_rep=2000, seed=11):
    rng = np.random.default_rng(seed); pnl = np.asarray(pnl, dtype=float)
    if len(pnl) < 5:
        return None
    m = np.array([rng.choice(pnl, size=len(pnl), replace=True).mean() for _ in range(n_rep)])
    return float(np.percentile(m, 5))


def newey_west_alpha_beta(y, x, lags=10):
    """y, x: Ueberrenditen (taeglich). Rueckgabe alpha (taeglich), beta, t_alpha, p_alpha (einseitig)."""
    m = ~(np.isnan(y) | np.isnan(x)); y = y[m]; x = x[m]; T = len(y)
    if T < 60:
        return dict(alpha=np.nan, beta=np.nan, t_alpha=np.nan, p_alpha=np.nan)
    X = np.column_stack([np.ones(T), x])
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ y
    e = y - X @ b
    S = np.zeros((2, 2))
    for l in range(0, lags + 1):
        wgt = 1.0 if l == 0 else 1 - l / (lags + 1)
        for t in range(l, T):
            v = X[t] * e[t]; u = X[t - l] * e[t - l]
            S += wgt * (np.outer(v, u) + (np.outer(u, v) if l > 0 else 0))
    V = XtX_inv @ S @ XtX_inv
    se = math.sqrt(max(V[0, 0], 1e-18))
    t_a = b[0] / se
    from math import erf, sqrt
    p_one = 1 - 0.5 * (1 + erf(t_a / sqrt(2)))
    return dict(alpha=float(b[0]), beta=float(b[1]), t_alpha=float(t_a), p_alpha=float(p_one))


def capture(strat, bench):
    """Up/Down-Capture auf Monatsrenditen."""
    s = (1 + strat.dropna()).resample("ME").prod() - 1
    b = (1 + bench.reindex(strat.dropna().index).fillna(0)).resample("ME").prod() - 1
    up = b > 0; dn = b < 0
    uc = s[up].mean() / b[up].mean() if up.sum() > 3 and b[up].mean() != 0 else np.nan
    dc = s[dn].mean() / b[dn].mean() if dn.sum() > 3 and b[dn].mean() != 0 else np.nan
    return float(uc), float(dc)


def deflated_sharpe(sr_daily, T, skew, kurt, n_trials, var_sr_trials):
    """Bailey & Lopez de Prado. sr_daily: nicht annualisierte Sharpe. Rueckgabe DSR (Wahrscheinlichkeit)."""
    from math import erf, sqrt, exp, log
    from statistics import NormalDist
    nd = NormalDist()
    if n_trials < 1 or np.isnan(sr_daily):
        return np.nan
    gamma = 0.5772156649
    sd_tr = math.sqrt(max(var_sr_trials, 1e-12))
    sr0 = sd_tr * ((1 - gamma) * nd.inv_cdf(1 - 1 / n_trials) + gamma * nd.inv_cdf(1 - 1 / (n_trials * math.e))) if n_trials > 1 else 0.0
    denom = math.sqrt(max(1 - skew * sr_daily + (kurt - 1) / 4 * sr_daily ** 2, 1e-12))
    z = (sr_daily - sr0) * math.sqrt(T - 1) / denom
    return float(nd.cdf(z))


def holm(pvals):
    """Holm-Korrektur. pvals: dict name->p. Rueckgabe dict name->adjusted p."""
    items = sorted(pvals.items(), key=lambda kv: kv[1]); m = len(items); adj = {}; prev = 0.0
    for i, (k, p) in enumerate(items):
        a = min(1.0, (m - i) * p); a = max(a, prev); adj[k] = a; prev = a
    return adj
