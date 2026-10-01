#!/usr/bin/env python3
"""
Project Aurum II — 03_mtp_validation: Validierungslauf der MTP Reconstructed Specification v1.
Vorregistrierung v0.2 (SHA-256 733bf2f5…), Spezifikation v1 (ed85be81…), beide eingefroren am 17.09.2026.

Ebenen:  A  Signale und Ausfuehrung auf CMC, Einstieg zum Schluss t, keine Kosten (K0 Zusatzzeile).
         B  Signale auf CMC, Ausfuehrung auf Kraken: Einstieg erster handelbarer Preis nach 00:00 UTC (Kraken-Open t+1) plus Slippage,
            Stop-Market am Niveau, Limit am Ziel, Kosten K0/K1/K2. B-Start je Coin nach Regel (ENTSCHEIDE 17.09.2026).
         B_sameday  wie B, Einstieg zum Kraken-Schluss t (Berichtswert).   B_full  wie B ohne B-Start-Regel (Berichtswert).
         B2 Signale und Ausfuehrung auf Kraken (Berichtswert, in Holm mitgezaehlt).
Sizing:  Sicht 1 Nominal Initial Risk per Leg 2 % des Sleeve-Startkapitals ohne Compounding (massgebend), 1b mit Compounding, 2 Portfolio (Bericht).
Aufruf:  python3 mtp_val.py [--tag full] [--nboot 2000] [--coins BTC ETH ...]
"""
import os, sys, json, math, argparse, hashlib, datetime as dt
import numpy as np, pandas as pd
sys.path.insert(0, "/home/claude/s2"); import s2lib as L
from stage2 import beta_tests

HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, "raw")
COINS = ["BTC", "ETH", "SOL", "XRP", "ADA", "AVAX", "LINK", "DOT", "BNB", "LTC"]
VAL_COINS = [c for c in COINS if c != "BTC"]
SPEC = dict(atr_n=180, sma_n=200, min_age=20, max_age=365, piv_left=5, piv_right=1, sl_mult=6.5, tp_mult=37.5, leg_k=1.5, r_leg=0.02, notional_cap=1.0)
COST = {"K0": dict(fee=0.0016, fric=0.0, slip_in=0.0, slip_sl=0.0), "K1": dict(fee=0.0040, fric=0.0002, slip_in=0.0005, slip_sl=0.0010), "K2": dict(fee=0.0080, fric=0.0006, slip_in=0.0015, slip_sl=0.0030)}
NOCOST = dict(fee=0.0, fric=0.0, slip_in=0.0, slip_sl=0.0)
BLOCKS = [("P1", "1900-01-01", "2020-12-31"), ("P2", "2021-01-01", "2023-12-31"), ("P3", "2024-01-01", "2099-12-31")]
JITTER = {"sl5.5": dict(sl_mult=5.5), "sl7.5": dict(sl_mult=7.5), "tp30": dict(tp_mult=30.0), "tp45": dict(tp_mult=45.0), "piv3": dict(piv_left=3), "piv10": dict(piv_left=10)}
DAYS = 365


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for ch in iter(lambda: fh.read(1 << 20), b""): h.update(ch)
    return h.hexdigest()


def load(path):
    d = pd.read_csv(path); d["t"] = pd.to_datetime(d["t"]); d = d.set_index("t").sort_index()
    return d[["open", "high", "low", "close"]].astype(float)


def tbill_daily(idx):
    t = pd.read_csv("/home/claude/s2/raw/DTB3_3m_tbill.csv"); t["observation_date"] = pd.to_datetime(t["observation_date"])
    s = t.set_index("observation_date")["DTB3"].astype(float) / 100.0
    s = s.reindex(idx.union(s.index)).sort_index().ffill().reindex(idx).fillna(0.0)
    return (1 + s) ** (1 / DAYS) - 1


# ----------------------------------------------------------------------------- Signalebene (Spezifikation v1, Abschnitt 9)
class Signals:
    """Alle Signalgroessen aus einer OHLC-Reihe: Wilder-ATR(180), SMA(200), Pivot-Niveau L_t (Basis-Verbrauch per Tageshoch)."""
    def __init__(self, d, spec):
        self.d = d; self.spec = spec; self.idx = d.index
        H, Lo, C = d.high.values, d.low.values, d.close.values
        pc = np.roll(C, 1); pc[0] = np.nan
        tr = np.nanmax(np.vstack([H - Lo, np.abs(H - pc), np.abs(Lo - pc)]), axis=0)
        self.atr = pd.Series(tr, index=d.index).ewm(alpha=1 / spec["atr_n"], adjust=False, min_periods=spec["atr_n"]).mean().values
        self.sma = pd.Series(C).rolling(spec["sma_n"]).mean().values
        nL, nR = spec["piv_left"], spec["piv_right"]; n = len(H)
        piv = np.zeros(n, bool)
        for i in range(nL, n - nR):
            if H[i] > H[i - nL:i].max() and H[i] > H[i + 1:i + nR + 1].max(): piv[i] = True
        self.piv = piv; self.H = H; self.C = C
        # Niveau je Tag (nur Vergangenheit: Pivots j in [i-max_age, i-min_age], nicht gebrochen durch Hochs j+1..i-1)
        lvl = np.full(n, np.nan); lvl_j = np.full(n, -1)
        mn, mx = spec["min_age"], spec["max_age"]
        for i in range(mx + 1, n):
            for j in range(i - mn, i - mx - 1, -1):
                if piv[j] and H[j + 1:i].max() <= H[j]:
                    lvl[i] = H[j]; lvl_j[i] = j; break
        self.lvl = lvl; self.lvl_j = lvl_j
        self.pos = {d: i for i, d in enumerate(d.index)}

    def at(self, day):
        i = self.pos.get(day)
        if i is None: return None
        return dict(i=i, high=self.H[i], close=self.C[i], atr=self.atr[i], sma=self.sma[i], lvl=self.lvl[i])


# ----------------------------------------------------------------------------- Ausfuehrungsebene
class Sleeve:
    """Ein Coin, eine Ebene, ein Kostenszenario. sig: Signals (CMC oder Kraken). ex: Ausfuehrungsreihe. entry_mode: 'close_t' oder 'open_t1'."""
    def __init__(self, coin, sig, ex, cost, entry_mode, start, spec, cap0=1.0, compounding=False, cash_daily=None, portfolio=None):
        self.coin, self.sig, self.ex, self.cost, self.entry_mode, self.spec = coin, sig, ex, cost, entry_mode, spec
        self.start = pd.Timestamp(start); self.cap0 = cap0; self.compounding = compounding; self.portfolio = portfolio
        self.cash = cap0; self.units = 0.0; self.pos = None; self.trades = []; self.pending = None
        self.eq = []; self.expo = []; self.notl = []; self.cash_daily = cash_daily
        self.exd = {d: i for i, d in enumerate(ex.index)}; self.O, self.Hh, self.Ll, self.Cc = ex.open.values, ex.high.values, ex.low.values, ex.close.values

    def equity(self, px): return self.cash + self.units * px

    def _size(self, atr, px, cap_equity):
        cap = cap_equity if self.compounding else self.cap0
        if self.portfolio is not None: cap = self.portfolio.equity_now
        units = self.spec["r_leg"] * cap / (self.spec["sl_mult"] * atr)
        limit_cap = self.portfolio.equity_now if self.portfolio is not None else cap
        cur_notional = (self.portfolio.notional_now() if self.portfolio is not None else self.units * px)
        room = max(0.0, self.spec["notional_cap"] * limit_cap - cur_notional)
        if units * px > room: units = room / px
        return units

    def _fill_in(self, day, i):
        c = self.cost
        if self.entry_mode == "close_t": return self.Cc[i] * (1 + c["slip_in"])
        return self.O[i] * (1 + c["slip_in"])   # erster handelbarer Preis nach 00:00 UTC = Open t+1

    def _open_leg(self, day, i, s, leg_no):
        px = self._fill_in(day, i); eqn = self.equity(self.Cc[i] if self.entry_mode == "close_t" else self.O[i])
        u = self._size(s["atr"], px, eqn)
        if u <= 0: return False
        fee = self.cost["fee"] + self.cost["fric"]; self.cash -= u * px * (1 + fee); self.units += u
        r_nom = u * self.spec["sl_mult"] * s["atr"]
        stop = s["close"] - self.spec["sl_mult"] * s["atr"]
        if self.pos is None:
            self.pos = dict(coin=self.coin, entry_sig=s["day"], entry_fill_day=day, legs=[], tp=s["close"] + self.spec["tp_mult"] * s["atr"], stop=stop, addons=[])
        else:
            # Open-Risk-Messung je Add-on (Vorregistrierung Abschnitt 6)
            ref = self.Cc[i]; old_stop = self.pos["stop"]; U0 = self.units - u
            avg0 = sum(l["units"] * l["fill"] for l in self.pos["legs"]) / U0
            before = dict(open_risk=U0 * (ref - old_stop), loss_at_stop=sum(l["units"] * (old_stop - l["fill"]) for l in self.pos["legs"]), notional=U0 * ref)
            after = dict(open_risk=self.units * (ref - stop), loss_at_stop=sum(l["units"] * (stop - l["fill"]) for l in self.pos["legs"]) + u * (stop - px), notional=self.units * ref)
            avg1 = (avg0 * U0 + u * px) / self.units
            self.pos["addons"].append(dict(day=str(day.date()), n=leg_no, before=before, after=after, stop_above_avg_after=bool(stop > avg1), sleeve_eq=eqn))
        self.pos["legs"].append(dict(sig_day=s["day"], fill_day=day, fill=px, units=u, atr=s["atr"], lvl=s["lvl"], r_nom=r_nom, stop=stop, sig_close=s["close"]))
        self.pos["stop"] = stop
        return True

    def _close(self, day, i, px, reason):
        fee = self.cost["fee"] + self.cost["fric"]; U = self.units
        self.cash += U * px * (1 - fee); p = self.pos
        gross = sum(l["units"] * (px - l["fill"]) for l in p["legs"])
        costs = sum(l["units"] * l["fill"] * fee for l in p["legs"]) + U * px * fee
        avg = sum(l["units"] * l["fill"] for l in p["legs"]) / U
        R1 = p["legs"][0]["r_nom"]; Rg = sum(l["r_nom"] for l in p["legs"])
        p.update(exit_day=day, exit_fill=px, reason=reason, pnl_gross=gross, cost=costs, pnl_net=gross - costs, R_first=R1, R_total=Rg,
                 mult_first=(gross - costs) / R1, mult_total=(gross - costs) / Rg, avg_entry=avg, n_legs=len(p["legs"]), hold=(day - p["entry_sig"]).days,
                 stop_final=p["stop"], stop_above_avg=bool(p["stop"] > avg), notional_max=max(sum(l["units"] * l["fill"] for l in p["legs"][:k + 1]) for k in range(len(p["legs"]))),
                 pnl_pct_cap=(gross - costs) / self.cap0, ret_on_avg=px / avg - 1)
        self.trades.append(p); self.pos = None; self.units = 0.0

    def step(self, day):
        """Ein Ausfuehrungstag. Reihenfolge: Cash-Zins, ausstehender Einstieg am Open, Exits auf der Kerze, dann Signal am Schluss."""
        i = self.exd.get(day)
        if i is None or day < self.start:
            return
        self.cash *= 1 + (self.cash_daily.get(day, 0.0) if self.cash_daily is not None else 0.0)
        exited = False
        if self.pending is not None and self.entry_mode == "open_t1":
            s, leg_no = self.pending; self.pending = None
            self._open_leg(day, i, s, leg_no)
        if self.pos is not None:
            c = self.cost
            if self.Ll[i] <= self.pos["stop"]:
                px = min(self.O[i], self.pos["stop"]) * (1 - c["slip_sl"]); self._close(day, i, px, "SL"); exited = True
            elif self.Hh[i] >= self.pos["tp"]:
                px = max(self.O[i], self.pos["tp"]); self._close(day, i, px, "TP"); exited = True
        # Signal am Schluss t (nicht am Exit-Tag, wie Basis-Simulation)
        s = self.sig.at(day)
        if exited or s is None or np.isnan(s["lvl"]) or np.isnan(s["sma"]) or np.isnan(s["atr"]) or not (s["close"] > s["sma"]):
            self._mark(i); return
        s = dict(s, day=day)
        if self.pos is None:
            if s["high"] > s["lvl"]:
                if self.entry_mode == "close_t": self._open_leg(day, i, s, 1)
                else: self.pending = (s, 1)
        else:
            if s["high"] > s["lvl"] and s["close"] > s["lvl"] and s["close"] >= self.pos["legs"][-1]["sig_close"] + self.spec["leg_k"] * s["atr"]:
                if self.entry_mode == "close_t": self._open_leg(day, i, s, len(self.pos["legs"]) + 1)
                else: self.pending = (s, len(self.pos["legs"]) + 1)
        self._mark(i)

    def _mark(self, i):
        self.eq.append((self.ex.index[i], self.equity(self.Cc[i]))); self.expo.append((self.ex.index[i], self.units * self.Cc[i] / max(self.equity(self.Cc[i]), 1e-12))); self.notl.append((self.ex.index[i], self.units * self.Cc[i]))

    def finish(self):
        if self.pos is not None:
            i = len(self.ex) - 1; self.pos.update(open_at_end=True); self._close(self.ex.index[i], i, self.Cc[i], "OPEN")
            self.trades[-1]["open_at_end"] = True
        eq = pd.Series(dict(self.eq)).sort_index(); ex = pd.Series(dict(self.expo)).sort_index(); self.notl_s = pd.Series(dict(self.notl)).sort_index()
        return eq, ex


class Portfolio:
    def __init__(self): self.sleeves = []; self.equity_now = 0.0
    def notional_now(self): return sum(s.units * s.Cc[s.exd[s._day]] for s in self.sleeves if s._day in s.exd)
    def run(self, days):
        for d in days:
            for s in self.sleeves: s._day = d
            self.equity_now = sum(s.cash for s in self.sleeves) + sum(s.units * s.Cc[s.exd[d]] for s in self.sleeves if d in s.exd)
            for s in self.sleeves: s.step(d)


# ----------------------------------------------------------------------------- Kennzahlen
def trade_metrics(trades, cap0=1.0):
    T = [t for t in trades if not t.get("open_at_end")]
    if not T: return dict(n=0)
    m1 = np.array([t["mult_first"] for t in T]); mg = np.array([t["mult_total"] for t in T]); pn = np.array([t["pnl_net"] for t in T]) / cap0
    wins = pn[pn > 0]; loss = pn[pn <= 0]; gp = wins.sum(); gl = -loss.sum()
    hold = np.array([t["hold"] for t in T]); legs = np.array([t["n_legs"] for t in T])
    q = lambda a, p: float(np.percentile(a, p)) if len(a) else np.nan
    srt = np.sort(pn)[::-1]
    return dict(n=len(T), exp_R_first=float(m1.mean()), med_R_first=float(np.median(m1)), exp_R_total=float(mg.mean()), med_R_total=float(np.median(mg)),
                R_total_pct=dict(p5=q(mg, 5), p25=q(mg, 25), p75=q(mg, 75), p90=q(mg, 90), p95=q(mg, 95), share_below_m1=float((mg < -1).mean()), share_above_3=float((mg > 3).mean())),
                R_first_pct=dict(p5=q(m1, 5), p25=q(m1, 25), p75=q(m1, 75), p90=q(m1, 90), p95=q(m1, 95)),
                profit_factor=float(gp / gl) if gl > 0 else (np.inf if gp > 0 else np.nan), win_rate=float((pn > 0).mean()),
                avg_win_pct=float(wins.mean()) if len(wins) else np.nan, avg_loss_pct=float(loss.mean()) if len(loss) else np.nan,
                avg_win_R=float(mg[pn > 0].mean()) if len(wins) else np.nan, avg_loss_R=float(mg[pn <= 0].mean()) if len(loss) else np.nan,
                gain_loss=float(wins.mean() / -loss.mean()) if len(wins) and len(loss) and loss.mean() < 0 else np.nan,
                exp_pct_cap=float(pn.mean()), sum_pct_cap=float(pn.sum()), legs_mean=float(legs.mean()), legs_max=int(legs.max()),
                hold_mean=float(hold.mean()), hold_win=float(hold[pn > 0].mean()) if len(wins) else np.nan, hold_loss=float(hold[pn <= 0].mean()) if len(loss) else np.nan,
                share_sl=float(np.mean([t["reason"] == "SL" for t in T])), share_tp=float(np.mean([t["reason"] == "TP" for t in T])),
                share_sl_above_avg=float(np.mean([t["stop_above_avg"] for t in T if t["reason"] == "SL"])) if any(t["reason"] == "SL" for t in T) else np.nan,
                top1_share=float(srt[0] / gp) if gp > 0 else np.nan, top3_share=float(srt[:3].sum() / gp) if gp > 0 else np.nan, top5_share=float(srt[:5].sum() / gp) if gp > 0 else np.nan,
                top10pct_share=float(srt[:max(1, int(math.ceil(len(pn) * 0.1)))].sum() / gp) if gp > 0 else np.nan,
                sum_ex_top1=float(pn.sum() - srt[:1].sum()), sum_ex_top3=float(pn.sum() - srt[:3].sum()), sum_ex_top5=float(pn.sum() - srt[:5].sum()),
                exp_ex_top1=float((pn.sum() - srt[0]) / max(len(pn) - 1, 1)), worst=float(pn.min()), best=float(pn.max()),
                trade_boot_p5_R=L.trade_bootstrap(mg, n_rep=2000))


def block_metrics(trades):
    out = {}
    for name, a, b in BLOCKS:
        T = [t for t in trades if not t.get("open_at_end") and pd.Timestamp(a) <= t["exit_day"] <= pd.Timestamp(b)]
        mg = [t["mult_total"] for t in T]
        out[name] = dict(n=len(T), exp_R_total=float(np.mean(mg)) if mg else np.nan, exp_R_first=float(np.mean([t["mult_first"] for t in T])) if T else np.nan,
                         pf=(sum(t["pnl_net"] for t in T if t["pnl_net"] > 0) / -sum(t["pnl_net"] for t in T if t["pnl_net"] <= 0)) if any(t["pnl_net"] <= 0 for t in T) and any(t["pnl_net"] > 0 for t in T) else np.nan,
                         valid=len(T) >= 5)
    return out


def path_metrics(eq, cash_daily):
    r = eq.pct_change().dropna()
    st = L.equity_stats(r, cash_daily)
    if st is None: return None
    dd = eq / eq.cummax() - 1
    # Recovery: je Drawdown-Episode Tage vom Tief bis zum alten Hoch
    rec = []; in_dd = False; trough = None; trough_d = None; peak_d = None
    for d, v in dd.items():
        if v < 0 and not in_dd: in_dd = True; trough = v; trough_d = d
        elif v < 0 and in_dd and v < trough: trough = v; trough_d = d
        elif v >= 0 and in_dd: rec.append((d - trough_d).days); in_dd = False
    st.update(rec_longest=int(max(rec)) if rec else 0, rec_mean=float(np.mean(rec)) if rec else 0.0, unrecovered_days=int((eq.index[-1] - trough_d).days) if in_dd else 0, dd_open_at_end=float(dd.iloc[-1]))
    return st


def ep_benchmark(ex, start, avg_w, cash_daily):
    r = ex.close.pct_change(); r = r[r.index >= pd.Timestamp(start)]
    net = avg_w * r + (1 - avg_w) * cash_daily.reindex(r.index).fillna(0.0)
    eq = (1 + net.fillna(0)).cumprod()
    return L.equity_stats(net.dropna(), cash_daily), r


# ----------------------------------------------------------------------------- Lauf je Ebene
def run_level(level, coins, data, spec, cost, sicht="1", starts=None, cash_daily=None):
    """Rueckgabe dict coin -> (trades, eq, expo, start, sleeve)."""
    out = {}
    port = Portfolio() if sicht == "2" else None
    sleeves = []
    for c in coins:
        C, K = data[c]["cmc"], data[c]["kraken"]
        if level == "A": sig, ex, mode = data[c]["sigC"] if spec is SPEC else Signals(C, spec), C, "close_t"
        elif level in ("B", "B_full"): sig, ex, mode = data[c]["sigC"] if spec is SPEC else Signals(C, spec), K, "open_t1"
        elif level == "B_sameday": sig, ex, mode = data[c]["sigC"], K, "close_t"
        elif level == "B2": sig, ex, mode = data[c]["sigK"], K, "open_t1"
        start = starts[c][level if level in starts[c] else ("B" if level.startswith("B") else "A")]
        cd = cash_daily.reindex(ex.index).fillna(0.0)
        sl = Sleeve(c, sig, ex, cost, mode, start, spec, compounding=(sicht == "1b"), cash_daily=cd.to_dict(), portfolio=port)
        sleeves.append(sl)
    if port is not None:
        port.sleeves = sleeves; days = sorted(set().union(*[set(s.ex.index) for s in sleeves])); port.run(days)
    else:
        for s in sleeves:
            for d in s.ex.index: s.step(d)
    for s in sleeves:
        eq, ex = s.finish(); out[s.coin] = dict(trades=s.trades, eq=eq, expo=ex, start=s.start)
    if port is not None:
        # Portfolio-Equity = Summe der Sleeve-Equities (gemeinsames Kapital), Exposure = Summe Notional / Portfolio-Equity
        idx = pd.DatetimeIndex(sorted(set().union(*[set(out[c]["eq"].index) for c in out])))
        E = sum(out[c]["eq"].reindex(idx).ffill().fillna(1.0) for c in out); N = sum(s.notl_s.reindex(idx).fillna(0.0) for s in sleeves)
        out["_portfolio"] = dict(eq=E, expo=N / E)
    return out


def pool_daily(res, coins, cash_daily):
    """Sleeve-Mittel der Tagesrenditen ueber Coins mit definiertem Wert (wie Stufe 2)."""
    if "_portfolio" in res:
        E = res["_portfolio"]["eq"]; net = E.pct_change().dropna(); return net, res["_portfolio"]["expo"].reindex(net.index)
    R = pd.concat({c: res[c]["eq"].pct_change() for c in coins if c in res}, axis=1)
    net = R.mean(axis=1, skipna=True).dropna()
    ex = pd.concat({c: res[c]["expo"] for c in coins if c in res}, axis=1).reindex(net.index).mean(axis=1, skipna=True)
    return net, ex


def evaluate_pool(res, coins, data, cash_daily, nboot, label):
    trades = [t for c in coins if c in res for t in res[c]["trades"]]
    net, expo = pool_daily(res, coins, cash_daily)
    eq = (1 + net).cumprod()
    pm = path_metrics(eq, cash_daily); tm = trade_metrics(trades); bm = block_metrics(trades)
    # EP: exposure-gleiche Passivposition je Coin, gepoolt gleich
    avg_w = float(expo.mean()) if len(expo) else 0.0
    bench = pd.concat({c: data[c]["kraken" if label.startswith("B") else "cmc"].close.pct_change().reindex(net.index) for c in coins if c in res}, axis=1).mean(axis=1, skipna=True)
    ep_net = avg_w * bench + (1 - avg_w) * cash_daily.reindex(net.index).fillna(0.0)
    ep = L.equity_stats(ep_net.dropna(), cash_daily)
    beta = beta_tests(net, bench, cash_daily, ep, pm) if pm and ep else None
    ex_r = (net - cash_daily.reindex(net.index).fillna(0.0)).values
    if len(ex_r) > 100:
        means, shs = L.block_bootstrap(ex_r, n_rep=nboot)
        boot = dict(p5_ann=float(np.percentile(means, 5) * DAYS), p_sharpe=float((shs <= 0).mean()), sharpe_ci=[float(np.percentile(shs, 5)), float(np.percentile(shs, 95))])
    else: boot = dict(p5_ann=np.nan, p_sharpe=1.0)
    coin_share = {}
    tot = sum(t["pnl_net"] for t in trades if not t.get("open_at_end"))
    if "_portfolio" in res: pm["portfolio_note"] = "Sicht 2: Pfadkennzahlen auf Portfolio-Equity, Sleeve-Equities nicht einzeln interpretierbar" if pm else None
    for c in coins:
        if c in res: coin_share[c] = float(sum(t["pnl_net"] for t in res[c]["trades"] if not t.get("open_at_end")) / tot) if tot else np.nan
    return dict(label=label, trades=tm, blocks=bm, path=pm, ep=ep, avg_expo=avg_w, beta=beta, boot=boot, coin_share=coin_share, n_days=int(len(net)), _net=net, _trades=trades)


def per_coin(res, c, cash_daily, data, level):
    tr = res[c]["trades"]; eq = res[c]["eq"]; pm = path_metrics(eq, cash_daily) if "_portfolio" not in res else None; tm = trade_metrics(tr); bm = block_metrics(tr)
    T = [t for t in tr if not t.get("open_at_end")]
    ex_top = None
    if T:
        srt = sorted(T, key=lambda t: -t["pnl_net"]); rest = srt[1:]
        ex_top = dict(sum_ex_largest=float(sum(t["pnl_net"] for t in rest)), exp_R_total_ex_largest=float(np.mean([t["mult_total"] for t in rest])) if rest else np.nan, largest_share=float(srt[0]["pnl_net"] / sum(t["pnl_net"] for t in T if t["pnl_net"] > 0)) if any(t["pnl_net"] > 0 for t in T) else np.nan)
    expo_days = float((res[c]["expo"] > 0).mean()) if len(res[c]["expo"]) else np.nan
    return dict(coin=c, start=str(res[c]["start"].date()), trades=tm, blocks=bm, path=pm, ex_largest=ex_top, expo_days=expo_days, avg_expo=float(res[c]["expo"].mean()) if len(res[c]["expo"]) else np.nan,
                addons=[a for t in tr for a in t["addons"]], blocks_positive=int(sum(1 for b in bm.values() if b["valid"] and b["exp_R_total"] > 0)))


# ----------------------------------------------------------------------------- Diagnostik A gegen B, A gegen B2
def match_trades(TA, TB, tol):
    m = []
    for a in TA:
        cand = [b for b in TB if abs((b["entry_sig"] - a["entry_sig"]).days) <= tol]
        m.append((a, cand[0] if cand else None))
    return m


def diag_A_vs_B(resA, resB, data, coins):
    rows = dict(n_A=0, n_B=0, matched=0, same_reason=0, phantom_sl=0, phantom_sl_rev=0, tp_only_one=0, exit_diff_days=[], fill_dev_in=[], fill_dev_sl=[], fill_dev_tp=[], b_not_in_a=0)
    for c in coins:
        if c not in resA or c not in resB: continue
        bstart = resB[c]["start"]
        TA = [t for t in resA[c]["trades"] if t["entry_sig"] >= bstart and not t.get("open_at_end")]; TB = [t for t in resB[c]["trades"] if not t.get("open_at_end")]
        rows["n_A"] += len(TA); rows["n_B"] += len(TB)
        C, K = data[c]["cmc"], data[c]["kraken"]
        for a, b in match_trades(TA, TB, 0):
            if b is None: continue
            rows["matched"] += 1
            if a["reason"] == b["reason"]: rows["same_reason"] += 1
            if b["reason"] == "SL" and a["reason"] != "SL": rows["phantom_sl"] += 1
            if a["reason"] == "SL" and b["reason"] != "SL": rows["phantom_sl_rev"] += 1
            if (a["reason"] == "TP") != (b["reason"] == "TP"): rows["tp_only_one"] += 1
            rows["exit_diff_days"].append((b["exit_day"] - a["exit_day"]).days)
            for la, lb in zip(a["legs"], b["legs"]): rows["fill_dev_in"].append(lb["fill"] / la["fill"] - 1)
            if a["reason"] == b["reason"] == "SL": rows["fill_dev_sl"].append(b["exit_fill"] / a["exit_fill"] - 1)
            if a["reason"] == b["reason"] == "TP": rows["fill_dev_tp"].append(b["exit_fill"] / a["exit_fill"] - 1)
        aset = set(t["entry_sig"] for t in TA); rows["b_not_in_a"] += sum(1 for b in TB if b["entry_sig"] not in aset)
    f = lambda x: dict(n=len(x), mean=float(np.mean(x)) if x else np.nan, p95=float(np.percentile(np.abs(x), 95)) if x else np.nan, share_gt_1pct=float(np.mean(np.abs(x) > 0.01)) if x else np.nan)
    return dict(n_A_window=rows["n_A"], n_B=rows["n_B"], matched=rows["matched"], same_reason_share=rows["same_reason"] / max(rows["matched"], 1), diff_reason_share=1 - rows["same_reason"] / max(rows["matched"], 1),
                phantom_sl=rows["phantom_sl"], phantom_sl_rev=rows["phantom_sl_rev"], tp_only_one=rows["tp_only_one"], b_not_in_a=rows["b_not_in_a"],
                exit_diff=dict(exact=float(np.mean([d == 0 for d in rows["exit_diff_days"]])) if rows["exit_diff_days"] else np.nan, within1=float(np.mean([abs(d) <= 1 for d in rows["exit_diff_days"]])) if rows["exit_diff_days"] else np.nan, mean_abs=float(np.mean(np.abs(rows["exit_diff_days"]))) if rows["exit_diff_days"] else np.nan),
                fill_in=f(rows["fill_dev_in"]), fill_sl=f(rows["fill_dev_sl"]), fill_tp=f(rows["fill_dev_tp"]))


def diag_A_vs_B2(resA, resB2, data, coins):
    out = dict(n_A=0, n_B2=0, entry_exact=0, entry_pm1=0, exit_exact=0, exit_pm1=0, legs_same=0, reason_same=0, identical=0, stop_dev=[], sma_agree=[], atr_ratio=[], lvl_agree=[])
    for c in coins:
        if c not in resA or c not in resB2: continue
        bstart = resB2[c]["start"]
        TA = [t for t in resA[c]["trades"] if t["entry_sig"] >= bstart and not t.get("open_at_end")]; TB = [t for t in resB2[c]["trades"] if not t.get("open_at_end")]
        out["n_A"] += len(TA); out["n_B2"] += len(TB)
        for a, b in match_trades(TA, TB, 1):
            if b is None: continue
            de = (b["entry_sig"] - a["entry_sig"]).days; dx = (b["exit_day"] - a["exit_day"]).days
            out["entry_exact"] += de == 0; out["entry_pm1"] += 1; out["exit_exact"] += dx == 0; out["exit_pm1"] += abs(dx) <= 1
            out["legs_same"] += a["n_legs"] == b["n_legs"]; out["reason_same"] += a["reason"] == b["reason"]
            out["identical"] += (a["n_legs"] == b["n_legs"] and a["reason"] == b["reason"] and abs(dx) <= 1)
            for la, lb in zip(a["legs"], b["legs"]): out["stop_dev"].append(lb["stop"] / la["stop"] - 1)
        sC, sK = data[c]["sigC"], data[c]["sigK"]
        common = sC.idx.intersection(sK.idx); common = common[common >= bstart]
        iC = [sC.pos[d] for d in common]; iK = [sK.pos[d] for d in common]
        fC = sC.C[iC] > sC.sma[iC]; fK = sK.C[iK] > sK.sma[iK]; ok = ~np.isnan(sC.sma[iC]) & ~np.isnan(sK.sma[iK])
        out["sma_agree"].extend((fC == fK)[ok].tolist())
        ar = sK.atr[iK] / sC.atr[iC]; out["atr_ratio"].extend(ar[~np.isnan(ar)].tolist())
        lC, lK = sC.lvl[iC], sK.lvl[iK]; both = ~np.isnan(lC) & ~np.isnan(lK); out["lvl_agree"].extend((np.abs(lK[both] / lC[both] - 1) < 0.005).tolist())
    n = max(out["n_A"], 1)
    return dict(n_A_window=out["n_A"], n_B2=out["n_B2"], entry_exact_share=out["entry_exact"] / n, entry_pm1_share=out["entry_pm1"] / n, exit_exact_share=out["exit_exact"] / n, exit_pm1_share=out["exit_pm1"] / n,
                legs_same_share=out["legs_same"] / n, reason_same_share=out["reason_same"] / n, identical_share=out["identical"] / n,
                stop_dev=dict(mean=float(np.mean(out["stop_dev"])) if out["stop_dev"] else np.nan, p95_abs=float(np.percentile(np.abs(out["stop_dev"]), 95)) if out["stop_dev"] else np.nan),
                sma_agree=float(np.mean(out["sma_agree"])) if out["sma_agree"] else np.nan, atr_ratio=dict(mean=float(np.mean(out["atr_ratio"])) if out["atr_ratio"] else np.nan, min=float(np.min(out["atr_ratio"])) if out["atr_ratio"] else np.nan, max=float(np.max(out["atr_ratio"])) if out["atr_ratio"] else np.nan),
                lvl_agree=float(np.mean(out["lvl_agree"])) if out["lvl_agree"] else np.nan)


# ----------------------------------------------------------------------------- Kriterien (Vorregistrierung Abschnitt 8)
def criteria(poolB, coinsB, poolA, diag, min_trades=10):
    tm = poolB["trades"]; crit = {}
    crit["c1"] = bool(tm.get("n", 0) > 0 and tm["exp_R_total"] > 0 and tm["profit_factor"] >= 1.5)
    eth = coinsB.get("ETH", {}).get("trades", {})
    others = [c for c in VAL_COINS if c != "ETH" and c in coinsB and coinsB[c]["trades"].get("n", 0) >= min_trades]
    pos = [c for c in others if coinsB[c]["trades"]["exp_R_total"] > 0]
    crit["c2"] = bool(eth.get("n", 0) >= min_trades and eth["exp_R_total"] > 0 and (len(pos) > len(others) / 2 if others else False))
    crit["c2_detail"] = dict(eth_n=eth.get("n", 0), eth_exp=eth.get("exp_R_total"), others_eligible=others, others_positive=pos)
    valid = [b for b in poolB["blocks"].values() if b["valid"]]; crit["c3"] = bool(sum(b["exp_R_total"] > 0 for b in valid) >= 2)
    crit["c4"] = bool(poolB["boot"]["p5_ann"] > 0 and poolB.get("holm_p", 1.0) < 0.05)
    crit["c5"] = bool(poolB["beta"] and (poolB["beta"]["alpha_test"] or poolB["beta"]["risk_test"]))
    ret = (tm["exp_R_total"] / poolA["trades"]["exp_R_total"]) if poolA["trades"].get("n", 0) and poolA["trades"]["exp_R_total"] > 0 else np.nan
    crit["c6"] = bool(not np.isnan(ret) and ret >= 0.6 and diag["diff_reason_share"] <= 0.15); crit["c6_detail"] = dict(retention=ret, diff_reason_share=diag["diff_reason_share"])
    crit["c7"] = bool(tm.get("n", 0) >= 60 and eth.get("n", 0) >= 10); crit["c7_note"] = "geringe Trade-Basis" if tm.get("n", 0) < 100 else ""
    crit["c8_report"] = dict(sum_ex_top1=tm.get("sum_ex_top1"), sum_ex_top3=tm.get("sum_ex_top3"), sum_ex_top5=tm.get("sum_ex_top5"),
                             coins_positive_ex_largest=[c for c in coinsB if coinsB[c]["ex_largest"] and coinsB[c]["ex_largest"]["exp_R_total_ex_largest"] > 0],
                             blocks_positive_per_coin={c: coinsB[c]["blocks_positive"] for c in coinsB})
    return crit


def criteria_A(poolA, coinsA):
    tm = poolA["trades"]; c = {}
    c["c1"] = bool(tm.get("n", 0) > 0 and tm["exp_R_total"] > 0 and tm["profit_factor"] >= 1.5)
    eth = coinsA.get("ETH", {}).get("trades", {}); others = [x for x in VAL_COINS if x != "ETH" and x in coinsA and coinsA[x]["trades"].get("n", 0) >= 10]
    pos = [x for x in others if coinsA[x]["trades"]["exp_R_total"] > 0]
    c["c2"] = bool(eth.get("n", 0) >= 10 and eth["exp_R_total"] > 0 and (len(pos) > len(others) / 2 if others else False))
    valid = [b for b in poolA["blocks"].values() if b["valid"]]; c["c3"] = bool(sum(b["exp_R_total"] > 0 for b in valid) >= 2)
    c["c4"] = bool(poolA["boot"]["p5_ann"] > 0 and poolA.get("holm_p", 1.0) < 0.05)
    c["c5"] = bool(poolA["beta"] and (poolA["beta"]["alpha_test"] or poolA["beta"]["risk_test"]))
    return c


# ----------------------------------------------------------------------------- Kontrollen
def btc_replication(resA_btc):
    obs = pd.read_csv("/home/claude/re/mtp_btc_trades_observed_v1.csv", parse_dates=["entry", "exit"])
    T = [t for t in resA_btc["trades"]]
    rows = []; hitE = hitX = hitP = 0
    for _, o in obs.iterrows():
        m = [t for t in T if abs((t["entry_sig"] - o.entry).days) <= 5]
        if not m: rows.append(dict(obs_entry=str(o.entry.date()), sim="-")); continue
        t = m[0]; dE = (t["entry_sig"] - o.entry).days; dX = (t["exit_day"] - o.exit).days; px = t["exit_fill"] / o.exit_px - 1
        hitE += dE == 0; hitX += dX == 0; hitP += abs(px) < 0.001
        rows.append(dict(obs_entry=str(o.entry.date()), sim=str(t["entry_sig"].date()), dE=dE, dX=dX, legs_obs=int(o.legs), legs_sim=t["n_legs"], px_dev=round(px * 100, 3), reason=t["reason"]))
    return dict(entry_hits=hitE, exit_hits=hitX, px_hits=hitP, rows=rows, n_sim=len(T))


def lookahead_test(data, cutoff="2023-06-30"):
    out = {}
    for c in ["BTC", "ETH"]:
        C = data[c]["cmc"]; Ccut = C[C.index <= pd.Timestamp(cutoff)]
        full = Signals(C, SPEC); cut = Signals(Ccut, SPEC)
        n = len(Ccut); dl = np.nansum(np.abs(np.nan_to_num(full.lvl[:n] - cut.lvl, nan=0.0)) > 1e-9)
        da = np.nanmax(np.abs(full.atr[:n] - cut.atr)); ds = np.nanmax(np.abs(full.sma[:n] - cut.sma))
        # Pivot am Rand: die letzte Kerze kann in cut kein Pivot sein (braucht Folgetag) -> nur bis n-2 vergleichen
        dp = int((full.piv[:n - 1] != cut.piv[:n - 1]).sum())
        out[c] = dict(level_diffs=int(dl), atr_maxdiff=float(da), sma_maxdiff=float(ds), pivot_diffs=dp)
    return out


# ----------------------------------------------------------------------------- Hauptlauf
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--tag", default="full"); ap.add_argument("--nboot", type=int, default=2000); ap.add_argument("--coins", nargs="*", default=COINS)
    ap.add_argument("--checks-only", action="store_true"); args = ap.parse_args()
    coins = args.coins; OUT = os.path.join(HERE, f"out_{args.tag}"); os.makedirs(os.path.join(OUT, "trades"), exist_ok=True)
    data = {}; inputs = {}
    for c in coins:
        pc, pk = os.path.join(RAW, "coinmarketcap", f"{c}USD_1d.csv"), os.path.join(RAW, "kraken_merged", f"{c}USD_1d.csv")
        data[c] = dict(cmc=load(pc), kraken=load(pk)); inputs[f"coinmarketcap/{c}USD_1d.csv"] = sha(pc); inputs[f"kraken_merged/{c}USD_1d.csv"] = sha(pk)
        data[c]["sigC"] = Signals(data[c]["cmc"], SPEC); data[c]["sigK"] = Signals(data[c]["kraken"], SPEC)
    all_idx = pd.DatetimeIndex(sorted(set().union(*[set(data[c]["cmc"].index) | set(data[c]["kraken"].index) for c in coins])))
    cash_daily = tbill_daily(all_idx)
    # Starts: A = CMC-Tag 365 (erstes moegliches Niveau), B = max(A-Start, erster Kraken-Tag nach letzter Luecke), B_full = max(A-Start, Kraken-Beginn)
    starts = {}
    for c in coins:
        C, K = data[c]["cmc"], data[c]["kraken"]; a = C.index[SPEC["max_age"]]
        g = K.index.to_series().diff().dt.days; gaps = g[g > 1]; after_gap = gaps.index.max() if len(gaps) else K.index.min()
        starts[c] = dict(A=a, B=max(a, after_gap), B_full=max(a, K.index.min()), B2=max(K.index[SPEC["max_age"]] if len(K) > SPEC["max_age"] else K.index.max(), after_gap))
    print("Starts:", {c: {k: str(v.date()) for k, v in s.items()} for c, s in starts.items()})
    # ---- Kontrollen
    la = lookahead_test(data); print("Look-ahead:", la)
    resA_nocost = run_level("A", coins, data, SPEC, NOCOST, "1", starts, cash_daily)
    rep = btc_replication(resA_nocost["BTC"]) if "BTC" in coins else None
    if rep: print(f"BTC-Replikation: Entry {rep['entry_hits']}/16 Exit {rep['exit_hits']}/16 Preis {rep['px_hits']}/16, sim Trades {rep['n_sim']}")
    la_ok = all(v["level_diffs"] == 0 and v["pivot_diffs"] == 0 and v["atr_maxdiff"] < 1e-6 and v["sma_maxdiff"] < 1e-6 for v in la.values())
    rep_ok = rep is None or (rep["entry_hits"] >= 13 and rep["exit_hits"] >= 13)
    json.dump(dict(lookahead=la, replication=rep, la_ok=la_ok, rep_ok=rep_ok), open(os.path.join(OUT, "controls.json"), "w"), indent=1, default=str)
    if not (la_ok and rep_ok):
        print("KONTROLLEN NICHT BESTANDEN, Volllauf wird nicht gestartet."); sys.exit(1)
    if args.checks_only: print("Kontrollen bestanden (checks-only)."); return
    # ---- Volllauf
    results = dict(levels={}, coins={}, diag={}, jitter={}, sicht={}, starts={c: {k: str(v.date()) for k, v in s.items()} for c, s in starts.items()})
    runs = {}
    runs[("A", "none")] = resA_nocost
    runs[("A", "K0")] = run_level("A", coins, data, SPEC, COST["K0"], "1", starts, cash_daily)
    for lv in ["B", "B_sameday", "B_full", "B2"]:
        for k in ["K0", "K1", "K2"]:
            runs[(lv, k)] = run_level(lv, coins, data, SPEC, COST[k], "1", starts, cash_daily)
    runs[("B", "K1", "1b")] = run_level("B", coins, data, SPEC, COST["K1"], "1b", starts, cash_daily)
    runs[("B", "K1", "2")] = run_level("B", coins, data, SPEC, COST["K1"], "2", starts, cash_daily)
    runs[("A", "none", "1b")] = run_level("A", coins, data, SPEC, NOCOST, "1b", starts, cash_daily)
    # Pools und Coins
    pools = {}
    for key, res in runs.items():
        lv, k = key[0], key[1]; s = key[2] if len(key) > 2 else "1"; label = f"{lv}|{k}|{s}"
        pv = evaluate_pool(res, VAL_COINS, data, cash_daily, args.nboot, lv)
        pa = evaluate_pool(res, coins, data, cash_daily, args.nboot, lv)
        pools[label] = dict(exBTC=pv, all=pa)
        results["coins"][label] = {c: per_coin(res, c, cash_daily, data, lv) for c in coins}
        print(f"  {label}: exBTC n={pv['trades'].get('n',0)} E[R_ges]={pv['trades'].get('exp_R_total',float('nan')):.3f} PF={pv['trades'].get('profit_factor',float('nan')):.2f} WR={pv['trades'].get('win_rate',float('nan')):.2f} | mit BTC n={pa['trades'].get('n',0)} E[R_ges]={pa['trades'].get('exp_R_total',float('nan')):.3f}")
    # Holm ueber A, B, B2 (K1 fuer B-Ebenen, A ohne Kosten), Pool ohne BTC
    pv = {"A|none|1": pools["A|none|1"]["exBTC"]["boot"]["p_sharpe"], "B|K1|1": pools["B|K1|1"]["exBTC"]["boot"]["p_sharpe"], "B2|K1|1": pools["B2|K1|1"]["exBTC"]["boot"]["p_sharpe"]}
    adj = L.holm(pv)
    for k, v in adj.items(): pools[k]["exBTC"]["holm_p"] = v
    # Diagnostik
    results["diag"]["A_vs_B_K1"] = diag_A_vs_B(runs[("A", "none")], runs[("B", "K1")], data, coins)
    results["diag"]["A_vs_B_K0"] = diag_A_vs_B(runs[("A", "none")], runs[("B", "K0")], data, coins)
    results["diag"]["A_vs_B2_K1"] = diag_A_vs_B2(runs[("A", "none")], runs[("B2", "K1")], data, coins)
    results["diag"]["A_vs_Bsameday_K1"] = diag_A_vs_B(runs[("A", "none")], runs[("B_sameday", "K1")], data, coins)
    # A im B-Fenster (fuer Retention): A-Trades mit Entry >= B-Start
    resA_win = {c: dict(runs[("A", "none")][c]) for c in coins}
    for c in coins:
        b0 = starts[c]["B"]; resA_win[c]["trades"] = [t for t in resA_win[c]["trades"] if t["entry_sig"] >= b0]; resA_win[c]["eq"] = resA_win[c]["eq"][resA_win[c]["eq"].index >= b0]; resA_win[c]["expo"] = resA_win[c]["expo"][resA_win[c]["expo"].index >= b0]
    pools["A_window|none|1"] = dict(exBTC=evaluate_pool(resA_win, VAL_COINS, data, cash_daily, args.nboot, "A"), all=evaluate_pool(resA_win, coins, data, cash_daily, args.nboot, "A"))
    results["coins"]["A_window|none|1"] = {c: per_coin(resA_win, c, cash_daily, data, "A") for c in coins}
    # Jitter (B K1 und A, Pool ohne BTC, nur Bericht)
    for jn, ov in JITTER.items():
        sp = dict(SPEC, **ov)
        rb = run_level("B", coins, data, sp, COST["K1"], "1", starts, cash_daily); ra = run_level("A", coins, data, sp, NOCOST, "1", starts, cash_daily)
        vc = [c for c in VAL_COINS if c in coins]; tb, ta = trade_metrics([t for c in vc for t in rb[c]["trades"]]), trade_metrics([t for c in vc for t in ra[c]["trades"]])
        results["jitter"][jn] = dict(params=ov, B=dict(n=tb.get("n"), exp_R_total=tb.get("exp_R_total"), pf=tb.get("profit_factor"), wr=tb.get("win_rate")), A=dict(n=ta.get("n"), exp_R_total=ta.get("exp_R_total"), pf=ta.get("profit_factor"), wr=ta.get("win_rate")))
        print(f"  Jitter {jn}: B exBTC n={tb.get('n')} E[R]={tb.get('exp_R_total',float('nan')):.3f} PF={tb.get('profit_factor',float('nan')):.2f}")
    # Kriterien
    crit = criteria(pools["B|K1|1"]["exBTC"], results["coins"]["B|K1|1"], pools["A_window|none|1"]["exBTC"], results["diag"]["A_vs_B_K1"])
    critA = criteria_A(pools["A|none|1"]["exBTC"], results["coins"]["A|none|1"])
    b_all = all(crit[k] for k in ["c1", "c2", "c3", "c4", "c5", "c6", "c7"]); a15 = all(critA[k] for k in ["c1", "c2", "c3", "c4", "c5"])
    verdict = "BESTANDEN" if b_all else ("TEILWEISE" if a15 else "VERWORFEN")
    results.update(criteria_B=crit, criteria_A=critA, verdict=verdict, holm=adj, spec=SPEC, cost=COST, inputs=inputs, run_at=dt.datetime.now(dt.timezone.utc).isoformat(), nboot=args.nboot,
                   prereg_sha256="733bf2f5ccd709e81f6ced77485d3f3de5c395cd22e99409662150aa49a62bf9", spec_sha256="ed85be81521284bdd8627156a29b863f216d3c4acd2341ea2d75f641d416b4a8", controls=dict(lookahead=la, replication=rep))
    results["levels"] = {k: dict(exBTC={kk: vv for kk, vv in v["exBTC"].items() if not kk.startswith("_")}, all={kk: vv for kk, vv in v["all"].items() if not kk.startswith("_")}) for k, v in pools.items()}
    # Trades exportieren
    for key, res in runs.items():
        label = "_".join(key); rows = []
        for c in coins:
            for t in res[c]["trades"]:
                rows.append(dict(coin=c, entry_sig=t["entry_sig"].date(), entry_fill_day=t["entry_fill_day"].date(), exit_day=t["exit_day"].date(), reason=t["reason"], n_legs=t["n_legs"], avg_entry=t["avg_entry"], exit_fill=t["exit_fill"],
                                 pnl_net_pct=t["pnl_net"] * 100, R_first=t["R_first"], R_total=t["R_total"], mult_first=t["mult_first"], mult_total=t["mult_total"], hold=t["hold"], stop_final=t["stop_final"], tp=t["tp"], stop_above_avg=t["stop_above_avg"], open_at_end=t.get("open_at_end", False),
                                 legs=";".join(f"{l['sig_day'].date()}@{l['fill']:.4f}x{l['units']:.6f}" for l in t["legs"])))
        pd.DataFrame(rows).to_csv(os.path.join(OUT, "trades", f"{label}.csv"), index=False)
    def clean(o):
        if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items() if not str(k).startswith("_")}
        if isinstance(o, (list, tuple)): return [clean(v) for v in o]
        if isinstance(o, (pd.Timestamp, dt.date)): return str(o)[:10]
        if isinstance(o, (np.floating, float)): return None if (isinstance(o, float) and (math.isnan(o) or math.isinf(o))) or (isinstance(o, np.floating) and (np.isnan(o) or np.isinf(o))) else float(o)
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.bool_,)): return bool(o)
        if isinstance(o, (pd.Series, pd.DataFrame)): return None
        return o
    json.dump(clean(results), open(os.path.join(OUT, "mtp_val_results.json"), "w"), indent=1)
    print(f"\nURTEIL (B K1 Sicht 1 Pool ohne BTC): {verdict}"); print("Kriterien B:", {k: v for k, v in crit.items() if k.startswith("c") and isinstance(v, bool)}); print("Kriterien A:", critA)


if __name__ == "__main__":
    main()
