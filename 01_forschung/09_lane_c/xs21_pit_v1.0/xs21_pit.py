#!/usr/bin/env python3
"""XS21 Point-in-Time v1.0 – Lauf nach eingefrorener Spezifikation `xs21_point_in_time_prereg_v1.0.md` (SHA edb24cde…).

Umsetzungsfestlegungen (vor dem Lauf eingefroren, siehe `xs21_pit_umsetzung_v1.0.md`):
- Tagesraster UTC. Gewicht w[t] = Position waehrend Tag t (Eroeffnung t bis Eroeffnung t+1), wie s2lib.
- Stichtage T = 2020-02-01 + 7k. Signal am Schluss der Tageskerze T, Ausfuehrung zur Eroeffnung T+1, gehalten bis Eroeffnung T+8.
- Kennzahlen, Bootstrap, Holm, Newey-West, Capture, DSR und Kostensaetze aus dem eingefrorenen `s2lib.py` (Stufe 2).
"""
import csv, glob, hashlib, io, json, math, os, sys, zipfile, datetime as dt
from collections import defaultdict
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "01_forschung", "02_strategien"))
import s2lib as S  # eingefroren (Stufe 2)

SPEC = os.path.join(REPO, "01_forschung/09_lane_c/xs21_point_in_time_prereg_v1.0.md")
SPEC_SHA = "edb24cde8c391c60cd90fdad753f403a8835de7e4da275af0d5d3eed01e998af"
GRID0 = pd.Timestamp("2020-02-01", tz="UTC")
END = pd.Timestamp("2026-09-14", tz="UTC")          # letzter Tag mit Rendite (Eroeffnung 14.09. bis Eroeffnung 15.09.)
DATA_END = pd.Timestamp("2026-09-15", tz="UTC")     # letzte benoetigte Kerze
U1_MIN_QV = 50e6
U2_N = 20
U1_MIN_N = 20                                       # M6
DELIST_FRIC = S.COST["K2"]["fric"]                  # B3: Glattstellung mit K2-Slippage
GAP_MAX = 3                                         # mehr fehlende Tage = Ende eines Handelslebens
BLOCKS = [("B1", None, "2021-12-31"), ("B2", "2022-01-01", "2023-12-31"), ("B3", "2024-01-01", "2026-09-14")]
DAYS = S.DAYS


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for ch in iter(lambda: fh.read(1 << 20), b""): h.update(ch)
    return h.hexdigest()


# ----------------------------------------------------------------------------- Daten
def _read_zip_csv(p):
    z = zipfile.ZipFile(p); txt = z.read(z.namelist()[0]).decode()
    rows = list(csv.reader(io.StringIO(txt)))
    if rows and not rows[0][0].strip().lstrip("-").isdigit():
        rows = rows[1:]
    return rows


def load_raw(datadir):
    """Liest die ZIPs aus fetch_data_v1.py. Rueckgabe: klines dict sym->DataFrame(open, close, qv), funding DataFrame."""
    kl = {}
    for p in sorted(glob.glob(os.path.join(datadir, "zips/*/klines/*/1d/*.zip"))):
        sym = p.split("/klines/")[1].split("/")[0]
        for r in _read_zip_csv(p):
            if int(float(r[8])) == 0:      # U5: Kerzen ohne Trades (z.B. SETTLING nach Delisting) gelten als nicht vorhanden
                continue
            kl.setdefault(sym, []).append((int(r[0]), float(r[1]), float(r[4]), float(r[7])))
    K = {}
    for s, rows in kl.items():
        d = pd.DataFrame(rows, columns=["ot", "open", "close", "qv"]).drop_duplicates("ot").sort_values("ot")
        d.index = pd.to_datetime(d["ot"], unit="ms", utc=True).dt.floor("D")
        d = d[~d.index.duplicated()]
        K[s] = d[["open", "close", "qv"]]
    fr = []
    for p in sorted(glob.glob(os.path.join(datadir, "zips/monthly/fundingRate/*/*.zip"))):
        sym = p.split("/fundingRate/")[1].split("/")[0]
        for r in _read_zip_csv(p):
            iv = float(r[1]) if len(r) >= 3 and r[1] != "" else 8.0
            fr.append((sym, int(r[0]), iv, float(r[-1])))
    F = pd.DataFrame(fr, columns=["sym", "ms", "interval", "rate"])
    F["t"] = pd.to_datetime(F["ms"], unit="ms", utc=True).dt.floor("h")
    F = F.drop_duplicates(["sym", "t"]).sort_values(["sym", "t"]).reset_index(drop=True)
    return K, F


class Data:
    """Matrizen auf dem Tagesraster. O, C, QV: Tage x Symbole (NaN = keine Kerze)."""

    def __init__(self, K, F, listing, tbill, days=None):
        syms = sorted(K)
        self.syms = syms; self.si = {s: i for i, s in enumerate(syms)}
        lo = min(d.index.min() for d in K.values())
        self.days = days if days is not None else pd.date_range(lo, DATA_END, freq="D", tz="UTC")
        n, m = len(self.days), len(syms)
        self.O = np.full((n, m), np.nan); self.C = np.full((n, m), np.nan); self.QV = np.full((n, m), np.nan)
        for s, d in K.items():
            d = d[(d.index >= self.days[0]) & (d.index <= self.days[-1])]
            ix = self.days.get_indexer(d.index); j = self.si[s]
            self.O[ix, j] = d["open"].values; self.C[ix, j] = d["close"].values; self.QV[ix, j] = d["qv"].values
        self.listing = listing          # sym -> (first_month, last_month_eff)
        self.F = F[F["sym"].isin(self.si)].copy()
        self._returns()
        self._funding()
        tb = tbill.reindex(self.days.union(tbill.index)).sort_index().ffill().reindex(self.days).fillna(0.0)
        self.cash_daily = ((1 + tb) ** (1 / DAYS) - 1).values
        self.cash_ann = tb.values

    def _returns(self):
        """r[t] = O[next]/O[t]-1 (naechste vorhandene Eroeffnung, Tage in kurzen Luecken 0). Eine Luecke von mehr als
        GAP_MAX fehlenden Tagen beendet ein Handelsleben (Delisting, ggf. spaetere Wiederzulassung unter gleichem Namen).
        Letzte Kerze eines Lebens vor Datenende = Delisting: r = C/O-1 an diesem Tag, danach NaN."""
        n, m = self.O.shape
        R = np.full((n, m), np.nan); self.life = np.full((n, m), -1, dtype=int)
        self.ends = []                      # (j, letzter Index) je Leben, das vor DATA_END endet
        self.last_bar = np.full(m, -1); self.gap_days = 0; self.n_relist = 0
        end_i = self.days.get_loc(DATA_END) if DATA_END in self.days else n - 1
        for j in range(m):
            have = np.where(~np.isnan(self.O[:, j]))[0]
            if len(have) == 0: continue
            self.last_bar[j] = have[-1]
            lives = [[have[0]]]
            for a, b in zip(have[:-1], have[1:]):
                if b - a - 1 > GAP_MAX: lives.append([b]); self.n_relist += 1
                else: lives[-1].append(b)
            for lid, lv in enumerate(lives):
                lv = np.array(lv)
                self.life[lv[0]:lv[-1] + 1, j] = lid
                for a, b in zip(lv[:-1], lv[1:]):
                    R[a, j] = self.O[b, j] / self.O[a, j] - 1
                    if b - a > 1:
                        R[a + 1:b, j] = 0.0; self.gap_days += int(b - a - 1)
                if lv[-1] < end_i:
                    self.ends.append((j, int(lv[-1])))
                    R[lv[-1], j] = self.C[lv[-1], j] / self.O[lv[-1], j] - 1
        self.R = R
        self.delisted = np.array([self.last_bar[j] < end_i for j in range(m)])

    def _funding(self):
        n, m = self.O.shape
        F = self.F
        F["di"] = self.days.get_indexer(F["t"].dt.floor("D"))
        F = F[F["di"] >= 0]
        self.FD = np.zeros((n, m))
        g = F.groupby(["di", "sym"])["rate"].sum()
        for (di, s), v in g.items(): self.FD[di, self.si[s]] = v
        self.obs = defaultdict(set)                 # (di, j) -> beobachtete Stunden
        self.by_hour = defaultdict(dict)            # stunde (ts) -> {j: rate}
        self.iv = {}                                # j -> (ms-array, interval-array)
        for s, d in F.groupby("sym"):
            j = self.si[s]
            hrs = d["t"].dt.hour.values; dis = d["di"].values
            for di, h in zip(dis, hrs): self.obs[(di, j)].add(int(h))
            for t, r in zip(d["t"].values.astype("datetime64[ns]").astype(np.int64), d["rate"].values): self.by_hour[int(t)][j] = r
            self.iv[j] = (d["di"].values, d["interval"].values)
        self.Fall = F

    def interval(self, di, j):
        if j not in self.iv: return 8.0
        dis, ivs = self.iv[j]
        k = np.searchsorted(dis, di, side="right") - 1
        return float(ivs[k] if k >= 0 else ivs[0])


# ----------------------------------------------------------------------------- Universen
def grid(days):
    out = []; t = GRID0
    while t <= END:
        if t in days: out.append(t)
        t += pd.Timedelta(days=7)
    return out


def universes(D, extra_excl=()):
    """Je Stichtag: Basis, U1, U2 (Listen von Spaltenindizes) nur aus Listing und quote_volume des Vormonats."""
    ex = {D.si[s] for s in extra_excl if s in D.si}
    out = []
    for T in grid(D.days):
        mT = T.strftime("%Y-%m")
        pm_end = T.replace(day=1) - pd.Timedelta(days=1); pm_start = pm_end.replace(day=1)
        a, b = D.days.get_loc(pm_start) if pm_start in D.days else None, D.days.get_loc(pm_end)
        if a is None: out.append(dict(T=T, basis=[], U1=[], U2=[])); continue
        ndays = b - a + 1
        cnt = (~np.isnan(D.O[a:b + 1])).sum(axis=0)
        qv = np.nansum(D.QV[a:b + 1], axis=0)
        basis = []
        for j, s in enumerate(D.syms):
            if j in ex: continue
            fm, lm = D.listing.get(s, (None, None))
            if fm is None or not (fm <= mT <= lm): continue
            if cnt[j] != ndays: continue
            basis.append(j)
        u1 = [j for j in basis if qv[j] >= U1_MIN_QV]
        u2 = sorted(basis, key=lambda j: (-qv[j], D.syms[j]))[:U2_N]
        out.append(dict(T=T, basis=basis, U1=u1, U2=u2, qv={j: float(qv[j]) for j in basis}))
    return out


def run_start(univ):
    """M6: erster Stichtag mit |U1| >= 20."""
    for u in univ:
        if len(u["U1"]) >= U1_MIN_N:
            return u["T"]
    return None


# ----------------------------------------------------------------------------- Gewichte
def weights(D, univ, ukey, start, L=21, top=3, side="LS", decile=False):
    """W[t, j]. Rueckgabe W, Auswahl-Log, governing (Tag -> Index in univ), cash_days (Stichtage mit U1 < 20)."""
    n, m = D.O.shape
    W = np.zeros((n, m)); log = []; gov = np.full(n, -1); cash_T = []
    for k, u in enumerate(univ):
        T = u["T"]
        if T < start: continue
        i = D.days.get_loc(T)
        lo, hi = i + 1, min(i + 8, n)
        gov[lo:hi] = k
        if len(u["U1"]) < U1_MIN_N:          # M6: U1 und U2 halten Cash
            cash_T.append(str(T.date())); continue
        mem = u[ukey]
        if i - L < 0: continue
        ret = D.C[i, mem] / D.C[i - L, mem] - 1
        same = (D.life[i, mem] >= 0) & (D.life[i, mem] == D.life[i - L, mem])
        ok = ~np.isnan(ret) & same
        cand = [(mem[q], ret[q]) for q in range(len(mem)) if ok[q]]
        N = max(1, len(mem) // 10) if decile else top
        lw = (1.0 / N) * (0.5 if side == "LS" else 1.0)
        longs = sorted([c for c in cand if c[1] > 0], key=lambda c: (-c[1], D.syms[c[0]]))[:N] if side in ("L", "LS") else []
        shorts = sorted([c for c in cand if c[1] < 0], key=lambda c: (c[1], D.syms[c[0]]))[:N] if side in ("S", "LS") else []
        for j, _ in longs: W[lo:hi, j] += lw
        for j, _ in shorts: W[lo:hi, j] -= lw
        log.append(dict(T=str(T.date()), n_mem=len(mem), n_sig=int(ok.sum()), long=[D.syms[j] for j, _ in longs], short=[D.syms[j] for j, _ in shorts]))
    # Delisting (B3): nach der letzten Kerze kein Gewicht mehr
    reb = sorted(D.days.get_loc(u["T"]) + 1 for u in univ)
    for j, e in D.ends:                      # nach Lebensende Cash bis zum naechsten Rebalancing (keine Wiederaufnahme)
        nxt = [r for r in reb if r > e + 1]
        stop = nxt[0] if nxt else n
        W[e + 1:stop, j] = 0.0
    W[D.days.get_loc(END) + 1:, :] = 0.0
    # Keine Position vor der ersten Kerze bzw. ohne Rendite (darf nicht vorkommen)
    bad = (W != 0) & np.isnan(D.R)
    if bad.any():
        r, c = np.argwhere(bad)[0]
        raise AssertionError(f"Position ohne Rendite: {D.syms[c]} {D.days[r].date()}")
    return W, log, gov, cash_T


# ----------------------------------------------------------------------------- Simulation
def simulate(D, W, cost, univ, ukey, gov, start):
    """Portfolio auf vollem Kapital. Rueckgabe dict mit Tagesreihen und Funding-Fuellstatistik (M4)."""
    n, m = W.shape
    per_side = cost["fee"] + cost["fric"]
    R = np.nan_to_num(D.R)
    dW = np.diff(np.vstack([np.zeros((1, m)), W]), axis=0)
    turn = np.abs(dW)
    cost_m = turn * per_side
    # Delisting: Glattstellung zum Schluss der letzten Kerze mit K2-Slippage
    for j, lb in D.ends:
        if lb + 1 < n and W[lb, j] != 0:
            cost_m[lb + 1, j] -= abs(W[lb, j]) * per_side
            cost_m[lb, j] += abs(W[lb, j]) * (cost["fee"] + DELIST_FRIC)
    gross_m = W * R
    fund_m = -W * D.FD
    # M4: fehlende Settlements fuer gehaltene Positionen, adverses Median-Funding
    fill = dict(L=dict(n_exp=0, n_fill=0), S=dict(n_exp=0, n_fill=0), n_fallback=0)
    held = np.argwhere(W != 0)
    for di, j in held:
        iv = D.interval(di, j)
        exp_h = [int(h) for h in np.arange(0, 24, iv)]
        leg = "L" if W[di, j] > 0 else "S"
        fill[leg]["n_exp"] += len(exp_h)
        miss = [h for h in exp_h if h not in D.obs.get((di, j), ())]
        if not miss: continue
        k = gov[di]; mem = set(univ[k][ukey]) if k >= 0 else set()
        for h in miss:
            ts = D.days[di] + pd.Timedelta(hours=h)
            vals = [abs(v) for jj, v in D.by_hour.get(ts.value, {}).items() if jj in mem]
            if vals:
                f = float(np.median(vals))
            else:
                fill["n_fallback"] += 1
                Fa = D.Fall
                sel = Fa[(Fa["t"] < ts) & (Fa["t"] >= ts - pd.Timedelta(days=30)) & (Fa["sym"].map(D.si).isin(mem))]
                f = float(np.median(np.abs(sel["rate"].values))) if len(sel) else 0.0
            fund_m[di, j] -= abs(W[di, j]) * f
            fill[leg]["n_fill"] += 1
    fund_raw = fund_m.copy()
    fund_m = np.where(fund_m < 0, fund_m * cost["fund_pay"], fund_m)
    expo = np.abs(W).sum(axis=1)
    cash = np.clip(1 - expo, 0, None) * D.cash_daily
    net = gross_m.sum(1) + fund_m.sum(1) + cash - cost_m.sum(1)
    i0 = D.days.get_loc(start); iE = D.days.get_loc(END)
    mask = np.zeros(n, bool); mask[i0:iE + 1] = True
    idx = D.days
    s = lambda a: pd.Series(np.where(mask, a, np.nan), index=idx)
    contrib = gross_m + fund_m - cost_m
    for leg in ("L", "S"):
        e = fill[leg]["n_exp"]; fill[leg]["share"] = fill[leg]["n_fill"] / e if e else 0.0
    return dict(net=s(net), gross=s(gross_m.sum(1)), cost=s(cost_m.sum(1)), funding=s(fund_m.sum(1)), cash=s(cash), expo=s(expo),
                long=s(np.clip(W, 0, None).sum(1)), contrib=contrib, mask=mask, fill=fill, fund_m=fund_m, fund_raw=fund_raw, cost_m=cost_m, gross_m=gross_m)


def trades(D, W, sim, cost):
    """Jede Positionsaenderung mit anschliessender Halteperiode = ein Trade (wie s2lib.trades_from_weights).
    Am Laufende offene Positionen werden wie in Stufe 2 nicht als Trade gezaehlt."""
    n, m = W.shape; out = []
    per_side = cost["fee"] + cost["fric"]
    R = np.nan_to_num(D.R)
    endset = set(D.ends)
    for j in np.where((W != 0).any(axis=0))[0]:
        w = W[:, j]; t = 0
        while t < n:
            if w[t] == 0: t += 1; continue
            a = t
            while t < n and w[t] == w[a]: t += 1
            b = t  # erster Tag mit anderem Gewicht
            if b >= n: break
            g = w[a] * (np.prod(1 + R[a:b, j]) - 1)
            f_raw = float(sim["fund_raw"][a:b, j].sum())
            f = f_raw * cost["fund_pay"] if f_raw < 0 else f_raw
            dl = (j, b - 1) in endset
            c = abs(w[a]) * (per_side + ((cost["fee"] + DELIST_FRIC) if dl else per_side))
            out.append(dict(sym=D.syms[j], entry_date=D.days[a], exit_date=D.days[b], w=float(w[a]), side=int(np.sign(w[a])), hold=int(b - a),
                            pnl_gross=float(g), funding=float(f), cost=float(c), pnl_net=float(g - c + f), delist_exit=dl))
    return out


# ----------------------------------------------------------------------------- Auswertung
def blocks(trs, start):
    out = {}
    for name, a, b in BLOCKS:
        a_ts = start if a is None else pd.Timestamp(a, tz="UTC"); b_ts = pd.Timestamp(b, tz="UTC")
        pn = [t["pnl_net"] for t in trs if a_ts <= t["entry_date"] <= b_ts]
        out[name] = dict(n=len(pn), expectancy=float(np.mean(pn)) if pn else float("nan"), valid=len(pn) >= 5)
    return out


def ew_bench(D, univ, ukey, gov, start, cost, A_long):
    """EW-Universum (Rendite und Funding der Mitglieder des geltenden Stichtags) und exposure-gleiche Passivposition EP_L."""
    n = len(D.days); r = np.full(n, np.nan); fd = np.zeros(n)
    for t in range(n):
        k = gov[t]
        if k < 0: continue
        mem = univ[k][ukey]
        x = D.R[t, mem]; ok = ~np.isnan(x)
        if ok.any():
            r[t] = x[ok].mean(); fd[t] = D.FD[t, mem][ok].mean()
    i0 = D.days.get_loc(start); iE = D.days.get_loc(END)
    mask = np.zeros(n, bool); mask[i0:iE + 1] = True
    rr = np.nan_to_num(r)
    def passive(wgt):
        fp = -wgt * fd; fp = np.where(fp < 0, fp * cost["fund_pay"], fp)
        c = np.zeros(n); c[i0] = wgt * (cost["fee"] + cost["fric"])
        net = wgt * rr + fp + (1 - wgt) * D.cash_daily - c
        return pd.Series(np.where(mask, net, np.nan), index=D.days)
    return pd.Series(np.where(mask, rr, np.nan), index=D.days), passive(A_long), passive(1.0)


def evaluate(D, univ, ukey, start, L=21, top=3, side="LS", decile=False, full=True, nboot=2000):
    W, log, gov, cash_T = weights(D, univ, ukey, start, L, top, side, decile)
    res = dict(universe=ukey, L=L, top=top, side=side, decile=decile, cash_stichtage=cash_T, n_cash_stichtage=len(cash_T), scen={})
    for kname, cost in S.COST.items():
        sim = simulate(D, W, cost, univ, ukey, gov, start)
        trs = trades(D, W, sim, cost)
        eq = S.equity_stats(sim["net"], pd.Series(D.cash_daily, index=D.days))
        pn = np.array([t["pnl_net"] for t in trs])
        sc = dict(equity=eq, n_trades=int(len(pn)), expectancy=float(pn.mean()) if len(pn) else float("nan"),
                  blocks=blocks(trs, start), avg_expo=float(sim["expo"].dropna().mean()), avg_long=float(sim["long"].dropna().mean()),
                  cost_sum=float(sim["cost"].sum()), funding_sum=float(sim["funding"].sum()), gross_sum=float(sim["gross"].sum()),
                  fill=sim["fill"], win_rate=float((pn > 0).mean()) if len(pn) else float("nan"))
        res["scen"][kname] = sc
        if kname == "K1":
            res["_sim"] = sim; res["_trades"] = trs; res["_W"] = W; res["_log"] = log; res["_gov"] = gov
    if not full:
        return res
    sim = res["_sim"]; cash = pd.Series(D.cash_daily, index=D.days)
    eq = res["scen"]["K1"]["equity"]
    bench_r, ep, bh = ew_bench(D, univ, ukey, res["_gov"], start, S.COST["K1"], res["scen"]["K1"]["avg_long"])
    ep_s = S.equity_stats(ep, cash); bh_s = S.equity_stats(bh, cash)
    res["bench"] = dict(EP=ep_s, BH_EW=bh_s)
    # Beta-Trennung 13.3 (wie stage2.beta_tests)
    x = sim["net"].dropna()
    ex_s = (x - cash.reindex(x.index)).values; ex_b = (bench_r.reindex(x.index) - cash.reindex(x.index)).values
    nw = S.newey_west_alpha_beta(ex_s, ex_b, lags=10)
    uc, dc = S.capture(x, bench_r)
    a_ok = bool(nw["p_alpha"] < 0.05 and nw["alpha"] > 0 and eq["sharpe"] > ep_s["sharpe"])
    b_ok = bool(eq["maxdd"] > ep_s["maxdd"] and eq["calmar"] > ep_s["calmar"] and not np.isnan(uc) and not np.isnan(dc) and uc > 0 and dc <= 0.8 * uc)
    res["beta"] = dict(alpha_ann=nw["alpha"] * DAYS, beta=nw["beta"], t_alpha=nw["t_alpha"], p_alpha=nw["p_alpha"], up_capture=uc, down_capture=dc,
                       alpha_test=a_ok, risk_test=b_ok, label="BEIDES" if a_ok and b_ok else "ALPHA" if a_ok else "RISIKOTRANSFORMATION" if b_ok else "KEINE")
    means, shs = S.block_bootstrap(ex_s, n_rep=nboot)
    res["boot"] = dict(p5_ann=float(np.percentile(means, 5) * DAYS), p_sharpe=float((shs <= 0).mean()),
                       sharpe_ci=[float(np.percentile(shs, 5)), float(np.percentile(shs, 95))])
    res["trade_boot_p5"] = S.trade_bootstrap([t["pnl_net"] for t in res["_trades"]], n_rep=nboot)
    res["cash_ann"] = float(np.mean(D.cash_ann[sim["mask"]]))
    return res


def criteria(r, neigh):
    K1 = r["scen"]["K1"]; eq = K1["equity"]
    c1 = bool(eq and K1["expectancy"] > 0 and eq["cagr"] > r["cash_ann"])
    b = K1["blocks"]
    c3 = bool(b["B1"]["valid"] and b["B2"]["valid"] and b["B1"]["expectancy"] > 0 and b["B2"]["expectancy"] > 0)   # M5
    pos = np.mean([x["expectancy"] > 0 for x in neigh]); med = float(np.nanmedian([x["sharpe"] for x in neigh]))
    c4 = bool(pos >= 2 / 3 and med > 0 and eq["sharpe"] <= 1.5 * med)
    c5 = bool(K1["n_trades"] >= S.TRADE_CLASS["S"][0])
    c6 = bool(eq["maxdd"] >= r["bench"]["EP"]["maxdd"])
    c7 = bool(r["beta"]["alpha_test"] or r["beta"]["risk_test"])
    c8 = bool(r["boot"]["p5_ann"] > 0 and r["holm_p"] < 0.05)
    K2 = r["scen"]["K2"]
    crit = dict(c1=c1, c3=c3, c4=c4, c4_pos=float(pos), c4_med_sharpe=med, c5=c5, c6=c6, c7=c7, c8=c8,
                robust_k2=bool(K2["equity"] and K2["expectancy"] > 0 and K2["equity"]["cagr"] > r["cash_ann"]))
    allc = [c1, c3, c4, c5, c6, c7, c8]
    verdict = "BESTANDEN" if all(allc) else ("TEILWEISE" if c1 and c5 and c8 else "VERWORFEN")
    return crit, verdict


def survivorship(D, r, start):
    """Beitraege (K1, arithmetische Summe der Tagesbeitraege und Trades) nach Status am Stichtag der Zerlegung."""
    sim = r["_sim"]; trs = r["_trades"]; out = {}
    for name, cut, upto in [("stand_2026-09-14", pd.Timestamp("2026-09-14", tz="UTC"), END),
                            ("stand_2023-12-31", pd.Timestamp("2023-12-31", tz="UTC"), pd.Timestamp("2023-12-31", tz="UTC"))]:
        ci = D.days.get_loc(cut); ui = D.days.get_loc(upto); i0 = D.days.get_loc(start)
        alive = D.last_bar >= ci + 1 if cut < END else ~D.delisted
        alive = np.asarray(alive)
        c = sim["contrib"][i0:ui + 1]
        tsub = [t for t in trs if t["entry_date"] <= upto]
        def grp(mask_syms):
            ss = {D.syms[j] for j in np.where(mask_syms)[0]}
            pn = [t["pnl_net"] for t in tsub if t["sym"] in ss]
            return dict(sum_daily_contrib=float(c[:, mask_syms].sum()), n_trades=len(pn), sum_trades=float(np.sum(pn)) if pn else 0.0,
                        expectancy=float(np.mean(pn)) if pn else float("nan"), n_symbols_traded=len({t["sym"] for t in tsub if t["sym"] in ss}))
        out[name] = dict(survivors=grp(alive), delisted=grp(~alive))
    return out
