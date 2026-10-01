#!/usr/bin/env python3
"""
Project Aurum II — Stufe 2 Rechenlauf.
Vorregistrierung: stage2_preregistration_v1.md, Version 1.0, eingefroren 15.09.2026.
Aufruf: python3 stage2.py [--coins BTC ETH ...] [--tag test]
"""
import os, sys, json, argparse, hashlib, datetime as dt, math
import numpy as np, pandas as pd
import s2lib as L

HERE = os.path.dirname(os.path.abspath(__file__))
CFG_LOG = []


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for ch in iter(lambda: fh.read(1 << 20), b""): h.update(ch)
    return h.hexdigest()


# ----------------------------------------------------------------------------- Variantenmatrix (eingefroren)
def A(id, N, k=3.0, gate=True, pyramid=False, mode="breakout", sma_n=200):
    return dict(id=id, family="A", cls=("L" if (N in (100, 252) or mode == "cross") else "M"),
                runner="trend", params=dict(N=N, k=k, gate=gate, pyramid=pyramid, mode=mode, sma_n=sma_n))

VARIANTS = [
    A("W0", 0, mode="cross"), A("W1", 20), A("W2", 55), A("W3", 100), A("W4", 252), A("W5", 55, k=4.0),
    A("W6", 55, pyramid=True), A("W7", 252, pyramid=True), A("W8", 55, gate=False),
    dict(id="MR", family="B", cls="S", runner="mr", params=dict(z_thr=2.0, n=20, hold_max=10, k=3.0)),
    dict(id="TS21", family="C", cls="S", runner="ts", params=dict(L=21, H=7)),
    dict(id="TS63", family="C", cls="S", runner="ts", params=dict(L=63, H=7)),
    dict(id="TS126", family="C", cls="S", runner="ts", params=dict(L=126, H=7)),
    dict(id="XS21", family="C", cls="S", runner="xs", params=dict(L=21, top=3, H=7)),
    dict(id="CC", family="D", cls="L", runner="cc", params=dict(thr=0.10, window="7")),
    dict(id="FC", family="D", cls="S", runner="fc", params=dict(scale=0.30, window="7", H=7)),
    dict(id="OI", family="D", cls="S", runner="oi", params=dict(W=7, H=7)),
]
SIDES = {  # welche Seiten je Variante primaer
    "W0": ["L"], "W1": ["L"], "W3": ["L"], "W5": ["L"], "W6": ["L"], "W7": ["L"],
    "W2": ["L", "S", "LS"], "W4": ["L", "S", "LS"], "W8": ["L", "S", "LS"],
    "MR": ["L", "S", "LS"], "TS21": ["L", "S", "LS"], "TS63": ["L", "S", "LS"], "TS126": ["L", "S", "LS"], "XS21": ["L", "S", "LS"],
    "CC": ["N"], "FC": ["L", "S", "LS"], "OI": ["L", "S", "LS"],
}
JITTER = {
    "W2": [("N40", dict(N=40)), ("N80", dict(N=80)), ("k2.5", dict(k=2.5)), ("k3.5", dict(k=3.5)), ("sma150", dict(sma_n=150)), ("sma250", dict(sma_n=250))],
    "W8": [("N40", dict(N=40)), ("N80", dict(N=80)), ("k2.5", dict(k=2.5)), ("k3.5", dict(k=3.5))],
    "MR": [("z1.5", dict(z_thr=1.5)), ("z2.5", dict(z_thr=2.5)), ("n10", dict(n=10)), ("n30", dict(n=30)), ("hold5", dict(hold_max=5)), ("hold20", dict(hold_max=20))],
    "TS21": [("L16", dict(L=16)), ("L26", dict(L=26)), ("H5", dict(H=5)), ("H10", dict(H=10))],
    "TS63": [("L47", dict(L=47)), ("L79", dict(L=79)), ("H5", dict(H=5)), ("H10", dict(H=10))],
    "TS126": [("L95", dict(L=95)), ("L158", dict(L=158)), ("H5", dict(H=5)), ("H10", dict(H=10))],
    "XS21": [("L42", dict(L=42)), ("L63", dict(L=63)), ("top2", dict(top=2)), ("top4", dict(top=4))],
    "CC": [("thr0.05", dict(thr=0.05)), ("thr0.15", dict(thr=0.15)), ("w3", dict(window="3")), ("w14", dict(window="14"))],
    "FC": [("s0.20", dict(scale=0.20)), ("s0.40", dict(scale=0.40)), ("w3", dict(window="3")), ("w14", dict(window="14"))],
    "OI": [("W5", dict(W=5)), ("W14", dict(W=14))],
}
# Achsen-Nachbarn fuer Varianten ohne eigene Jitter (Interpretation vor dem Lauf, protokolliert)
AXIS = {"W1": ["W2"], "W3": ["W2", "W4"], "W4": ["W3"], "W5": ["W2", "W2:k3.5"], "W6": ["W2"], "W7": ["W4"], "W0": []}
FAMILY_N = {"A": 15, "B": 3, "C": 12, "D": None}   # D: 4 oder 7, je nach D-OI


# ----------------------------------------------------------------------------- Laufhilfen
def run_variant(cd, ind, runner, params, side):
    """Rueckgabe w (Series), trades (Liste), active_from (Timestamp)."""
    s = {"L": +1, "S": -1}[side]
    if runner == "trend":
        p = dict(params)
        if p["mode"] == "cross":
            w, tr = L.run_trend(cd, ind, side=s, mode="cross", sma_n=p["sma_n"])
            need = [f"sma{p['sma_n']}", "atr"]
        else:
            w, tr = L.run_trend(cd, ind, side=s, mode="breakout", N=p["N"], k=p["k"], gate=p["gate"], sma_n=p["sma_n"], pyramid=p["pyramid"])
            need = [f"sma{p['sma_n']}", "atr", f"hh{p['N']}"]
    elif runner == "mr":
        w, tr = L.run_mr(cd, ind, side=s, **params); need = [f"sma{params['n']}", f"sd{params['n']}", "atr"]
    elif runner == "ts":
        w = L.weights_ts(cd, ind, L=params["L"], H=params["H"], side=s); tr = L.trades_from_weights(cd, w); need = [f"ret{params['L']}"]
    elif runner == "fc":
        w = L.weights_fc(cd, scale=params["scale"], window=params["window"], H=params["H"], side=s); tr = L.trades_from_weights(cd, w); need = None
    elif runner == "oi":
        w = L.weights_oi(cd, ind, W=params["W"], H=params["H"], side=s); tr = L.trades_from_weights(cd, w); need = None
    else:
        raise ValueError(runner)
    if need is not None:
        m = ind[need].notna().all(axis=1)
        active = m.idxmax() if m.any() else None
    else:
        src = cd.f7_daily if runner == "fc" else (cd.oi["oi"].reindex(cd.idx) if cd.oi is not None else pd.Series(np.nan, index=cd.idx))
        active = src.first_valid_index()
    return w, tr, active


def sim_all(cd, w, active, extra=None):
    out = {}
    for kname, cost in L.COST.items():
        s = L.simulate(cd, w, cost, extra)
        if active is not None:
            s.loc[s.index < active, ["gross", "net", "cost", "funding", "cash"]] = np.nan
        else:
            s.loc[:, ["gross", "net"]] = np.nan
        out[kname] = s
    return out


def combine_LS(simL, simS):
    out = {}
    for k in simL:
        a, b = simL[k], simS[k]
        c = a.copy()
        for col in ["w", "gross", "cost", "funding", "cash", "net", "turnover", "expo"]:
            c[col] = 0.5 * a[col] + 0.5 * b[col]
        out[k] = c
    return out


def pooled(sims_by_coin, mode="mean", cash_daily=None):
    """
    mode 'mean': gleichgewichteter Durchschnitt ueber Coins mit definiertem net am Tag (je Coin ein Sleeve mit vollem Kapital).
    mode 'sum':  ein Portfolio auf vollem Kapital (XS21): Gewichte je Coin summieren sich, Cash auf 1 - Summe der Betragsgewichte.
                 Summe der Sleeve-Nettos zaehlt Cash je Sleeve, deshalb wird (n - 1) mal Cash abgezogen.
    """
    nets = pd.concat({c: s["net"] for c, s in sims_by_coin.items()}, axis=1)
    expo = pd.concat({c: s["expo"] for c, s in sims_by_coin.items()}, axis=1)
    w = pd.concat({c: s["w"] for c, s in sims_by_coin.items()}, axis=1)
    n = nets.notna().sum(axis=1)
    if mode == "sum":
        net = nets.sum(axis=1, min_count=1) - (n - 1).clip(lower=0) * cash_daily.reindex(nets.index).fillna(0.0)
        return pd.DataFrame(dict(net=net, expo=expo.where(nets.notna()).sum(axis=1, min_count=1),
                                 w=w.where(nets.notna()).sum(axis=1, min_count=1), n=n))
    return pd.DataFrame(dict(net=nets.mean(axis=1, skipna=True), expo=expo.where(nets.notna()).mean(axis=1, skipna=True),
                             w=w.where(nets.notna()).mean(axis=1, skipna=True), n=n))


def pool_mode(vid):
    return "sum" if vid == "XS21" else "mean"


def bench_sims(cd, active, avg_w_long, avg_w_short, strat_vol):
    """Benchmarks je Coin: BH, EP (long/short), VP, Cash."""
    idx = cd.idx
    one = pd.Series(1.0, index=idx)
    out = {}
    out["BH"] = sim_all(cd, one, active)
    out["EP_L"] = sim_all(cd, pd.Series(avg_w_long, index=idx), active)
    out["EP_S"] = sim_all(cd, pd.Series(-avg_w_short, index=idx), active)
    coin_vol = cd.r_o2o.loc[active:].std(ddof=1) * math.sqrt(L.DAYS) if active is not None else np.nan
    vp = strat_vol / coin_vol if coin_vol and coin_vol > 0 and not np.isnan(strat_vol) else 0.0
    out["VP"] = sim_all(cd, pd.Series(float(np.clip(vp, 0, 1)), index=idx), active)
    out["CASH"] = sim_all(cd, pd.Series(0.0, index=idx), active)
    return out


def metrics_bundle(sim, cd_cash, trades, cost, bench_net=None):
    eq = L.equity_stats(sim["net"], cd_cash)
    ts = L.trade_stats(trades, cost)
    m = dict(equity=eq, trades=ts,
             avg_expo=float(sim["expo"][sim["net"].notna()].mean()) if eq else np.nan,
             turnover=float(sim["turnover"][sim["net"].notna()].sum() / max(eq["years"], 1e-9)) if eq else np.nan,
             funding_sum=float(sim["funding"][sim["net"].notna()].sum()) if eq else np.nan,
             cost_sum=float(sim["cost"][sim["net"].notna()].sum()) if eq else np.nan,
             gross_sum=float(sim["gross"][sim["net"].notna()].sum()) if eq else np.nan)
    if eq and m["avg_expo"] and m["avg_expo"] > 0:
        m["ret_per_expo"] = eq["cagr"] / m["avg_expo"]
    return m


def beta_tests(strat_net, bench_r, cash_daily, ep_stats, strat_stats):
    """13.3a und 13.3b gegen exposure-gleiche Passivposition."""
    x = strat_net.dropna()
    ex_s = (x - cash_daily.reindex(x.index).fillna(0)).values
    ex_b = (bench_r.reindex(x.index) - cash_daily.reindex(x.index).fillna(0)).values
    nw = L.newey_west_alpha_beta(ex_s, ex_b, lags=10)
    uc, dc = L.capture(x, bench_r)
    a_ok = (nw["p_alpha"] < 0.05) and (nw["alpha"] > 0) and (strat_stats["sharpe"] > ep_stats["sharpe"]) if ep_stats else False
    b_ok = (strat_stats["maxdd"] > ep_stats["maxdd"]) and (strat_stats["calmar"] > ep_stats["calmar"]) and (not np.isnan(uc) and not np.isnan(dc) and uc > 0 and dc <= 0.8 * uc) if ep_stats else False
    return dict(alpha_daily=nw["alpha"], alpha_ann=nw["alpha"] * L.DAYS if not np.isnan(nw["alpha"]) else np.nan, beta=nw["beta"],
                t_alpha=nw["t_alpha"], p_alpha=nw["p_alpha"], up_capture=uc, down_capture=dc,
                alpha_test=bool(a_ok), risk_test=bool(b_ok), label=("BEIDES" if a_ok and b_ok else "ALPHA" if a_ok else "RISIKOTRANSFORMATION" if b_ok else "KEINE"))


def block_expectancy(trades_pooled, idx):
    out = {}
    for name, a, b in L.BLOCKS:
        a_ts, b_ts = pd.Timestamp(a, tz="UTC"), pd.Timestamp(b, tz="UTC")
        pn = [tr["pnl_net"] for tr in trades_pooled if a_ts <= tr["exit_date"] <= b_ts]
        out[name] = dict(n=len(pn), expectancy=float(np.mean(pn)) if pn else np.nan, valid=len(pn) >= 5)
    return out


def net_trades(trades, cost, coin, idx):
    per_side = cost["fee"] + cost["fric"]
    out = []
    for tr in trades:
        notional = sum(u for _, u in tr["units"]) if "units" in tr else tr["notional"]
        f = tr["funding"]; f = f * cost["fund_pay"] if f < 0 else f
        if "spot_notional" in tr:   # D-CC: Spot-Beine mit Spot-Kostenmodell, Perp-Beine mit Perp-Kostenmodell
            cost_amt = 2 * tr["spot_notional"] * (cost["spot_fee"] + cost["spot_fric"]) + 2 * tr["perp_notional"] * per_side
        else:
            cost_amt = per_side * 2 * notional
        pnl_net = tr["pnl_gross"] - cost_amt + f
        out.append(dict(coin=coin, entry_date=idx[tr["entry_t"]], exit_date=idx[tr["exit_t"]], pnl_net=pnl_net, pnl_gross=tr["pnl_gross"],
                        hold=tr["hold"], side=tr["side"], reason=tr.get("exit_reason"), risk0=tr.get("risk0"), notional=notional, funding=f,
                        n_units=tr.get("n_units", 1), entry_fill=tr["entry_fill"], exit_fill=tr["exit_fill"]))
    return out


# ----------------------------------------------------------------------------- Hauptlauf
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--coins", nargs="*", default=L.COINS)
    ap.add_argument("--tag", default="full")
    ap.add_argument("--nboot", type=int, default=2000)
    args = ap.parse_args()
    coins = args.coins
    OUT = os.path.join(HERE, f"out_{args.tag}"); os.makedirs(OUT, exist_ok=True); os.makedirs(os.path.join(OUT, "stage2_trades"), exist_ok=True)

    tbill = L.load_tbill()
    data = {c: L.CoinData(c, tbill) for c in coins}
    inds = {c: L.indicators(data[c].spot) for c in coins}
    inputs = {}
    for root, _, files in os.walk(L.RAW):
        for f in files:
            if f.endswith(".csv") or f.endswith(".json"):
                p = os.path.join(root, f); inputs[os.path.relpath(p, L.RAW)] = sha(p)

    # D-OI Datenpruefung, fail-closed
    oi_ok = {}
    for c in coins:
        o = data[c].oi
        ok = False; why = "keine Datei"
        if o is not None:
            n = len(o); gaps = o.index.to_series().diff().dt.days.max()
            pos = (o["oi"] > 0).all()
            ok = (n >= 1095) and pos and (gaps is None or np.isnan(gaps) or gaps <= 3)
            why = f"n={n}, max_gap={gaps}, positiv={bool(pos)}"
        oi_ok[c] = dict(ok=bool(ok), why=why)
    run_oi = all(oi_ok.get(c, {}).get("ok", False) for c in ["BTC", "ETH"] if c in coins) and ("BTC" in coins and "ETH" in coins)
    FAMILY_N["D"] = 7 if run_oi else 4

    results = {}      # (vid, side) -> dict
    daily_store = {}  # (vid, side, coin) -> sim K1 net
    trade_store = {}

    def evaluate(vid, side, sims_by_coin, trades_by_coin, actives, meta, family, cls, is_primary=True, extra_label=None):
        key = f"{vid}|{side}"
        res = dict(id=vid, side=side, family=family, cls=cls, primary=is_primary, coins={}, scenarios={})
        # je Coin, je Szenario
        for kname, cost in L.COST.items():
            sc = dict(coins={})
            for c in coins:
                if c not in sims_by_coin: continue
                sim = sims_by_coin[c][kname]
                sc["coins"][c] = metrics_bundle(sim, data[c].cash_daily, trades_by_coin.get(c, []), cost)
            # gepoolt
            pool = pooled({c: sims_by_coin[c][kname] for c in sims_by_coin}, pool_mode(vid), data[coins[0]].cash_daily)
            eq = L.equity_stats(pool["net"], data[coins[0]].cash_daily)
            tr_pool = [t for c in trades_by_coin for t in net_trades(trades_by_coin[c], cost, c, data[c].idx)]
            pn = np.array([t["pnl_net"] for t in tr_pool])
            sc["pooled"] = dict(equity=eq, n_trades=int(len(pn)), expectancy=float(pn.mean()) if len(pn) else np.nan,
                                avg_expo=float(pool["expo"][pool["net"].notna()].mean()) if eq else np.nan,
                                blocks=block_expectancy(tr_pool, None),
                                trades_per_coin={c: len(trades_by_coin.get(c, [])) for c in sims_by_coin},
                                win_rate=float((pn > 0).mean()) if len(pn) else np.nan,
                                top10_share=None)
            if kname == "K1":
                res["_pool_net"] = pool["net"]; res["_pool_expo"] = pool["expo"]; res["_pool_w"] = pool["w"]; res["_trades"] = tr_pool
            res["scenarios"][kname] = sc
        return res

    # ---------------- Familien A, B, C(TS), D(FC, OI): je Coin
    variant_runs = {}
    for V in VARIANTS:
        vid = V["id"]; runner = V["runner"]
        if runner in ("xs", "cc"):
            continue
        if runner == "oi" and not run_oi:
            results[f"{vid}|skipped"] = dict(id=vid, skipped=True, reason="D-OI Datenanforderungen nicht erfuellt (fail-closed)", oi_check=oi_ok)
            continue
        configs = [("base", {})] + [(n, o) for n, o in JITTER.get(vid, [])]
        for cname, over in configs:
            params = {**V["params"], **over}
            for side in ["L", "S"]:
                if cname == "base" and side == "S" and "S" not in SIDES[vid]:
                    continue
                if cname != "base" and side == "S" and "S" not in SIDES[vid]:
                    continue
                sims, trs, acts = {}, {}, {}
                for c in coins:
                    cd, ind = data[c], inds[c]
                    if runner == "fc" and cd.funding is None: continue
                    w, tr, active = run_variant(cd, ind, runner, params, side)
                    if active is None: continue
                    sims[c] = sim_all(cd, w, active); trs[c] = tr; acts[c] = active
                    CFG_LOG.append(dict(variant=vid, config=cname, side=side, coin=c, params=json.dumps(params), n_trades=len(tr), active_from=str(active.date())))
                variant_runs[(vid, cname, side)] = (sims, trs, acts, params)
                if cname == "base":
                    for c in coins:
                        if c in sims:
                            daily_store[(vid, side, c)] = sims[c]["K1"]["net"]; trade_store[(vid, side, c)] = trs[c]

    # ---------------- XS21 (Portfolio ueber Coins)
    def run_xs(Lb, top, H, side):
        idx = data["BTC"].idx
        rets = pd.concat({c: inds[c][f"ret{Lb}"].reindex(idx) for c in coins}, axis=1)
        W = pd.DataFrame(0.0, index=idx, columns=coins)
        start = rets.notna().any(axis=1).idxmax()
        i0 = idx.get_loc(start)
        cur = pd.Series(0.0, index=coins)
        for t in range(len(idx)):
            if t >= i0 and (t - i0) % H == 0:
                r = rets.iloc[t].dropna()
                cur = pd.Series(0.0, index=coins)
                if side in ("L", "LS"):
                    el = r[r > 0].sort_values(ascending=False).head(top)
                    for c in el.index: cur[c] += (1.0 / top) * (0.5 if side == "LS" else 1.0)
                if side in ("S", "LS"):
                    es = r[r < 0].sort_values().head(top)
                    for c in es.index: cur[c] -= (1.0 / top) * (0.5 if side == "LS" else 1.0)
            if t + 1 < len(idx):
                W.iloc[t + 1] = cur.values
        sims, trs = {}, {}
        for c in coins:
            w = W[c]
            sims[c] = sim_all(data[c], w, start); trs[c] = L.trades_from_weights(data[c], w)
        return sims, trs, start

    if len(coins) >= 3:
        V = next(v for v in VARIANTS if v["id"] == "XS21")
        for cname, over in [("base", {})] + JITTER["XS21"]:
            p = {**V["params"], **over}
            for side in ["L", "S", "LS"]:
                sims, trs, start = run_xs(p["L"], p["top"], p["H"], side)
                variant_runs[("XS21", cname, side)] = (sims, trs, {c: start for c in coins}, p)
                CFG_LOG.append(dict(variant="XS21", config=cname, side=side, coin="ALL", params=json.dumps(p), n_trades=sum(len(t) for t in trs.values()), active_from=str(start.date())))

    # ---------------- D-CC (marktneutral, zwei Beine)
    V = next(v for v in VARIANTS if v["id"] == "CC")
    for cname, over in [("base", {})] + JITTER["CC"]:
        p = {**V["params"], **over}
        sims, trs, acts = {}, {}, {}
        for c in coins:
            cd = data[c]
            if cd.funding is None or cd.perp is None: continue
            ws, wp = L.weights_cc(cd, thr=p["thr"], window=p["window"])
            active = cd.f7_daily.first_valid_index()
            out = {}
            for kname, cost in L.COST.items():
                s = L.simulate(cd, ws, cost, extra=dict(w_perp=wp))
                s.loc[s.index < active, ["gross", "net", "cost", "funding", "cash"]] = np.nan
                out[kname] = s
            sims[c] = out
            # Trades: Perioden mit ws=1; P&L = Sleeve-Netto ueber die Periode (K1) minus... vereinfachend aus Gewichtsaenderungen des Spot-Beins
            tr = []
            wv = ws.values; o = cd.spot["open"].values; op = cd.perp["open"].reindex(cd.idx).values; fd = cd.fund_day.values
            cur = None
            for t in range(len(cd.idx)):
                if t == 0 or wv[t] != wv[t - 1]:
                    if cur is not None:
                        pnl = (o[t] / cur["entry_fill"] - 1) - (op[t] / cur["entry_perp"] - 1) if not np.isnan(op[t]) and not np.isnan(cur["entry_perp"]) else 0.0
                        cur.update(exit_t=t, exit_fill=o[t], pnl_gross=pnl, hold=t - cur["entry_t"], notional=2.0, spot_notional=1.0, perp_notional=1.0,
                                   side=0, n_units=1, exit_reason="funding<=0", risk0=np.nan, cost_sides=4)
                        tr.append(cur); cur = None
                    if wv[t] == 1.0:
                        cur = dict(entry_t=t, entry_fill=o[t], entry_perp=op[t], w=1.0, funding=0.0)
                # Short-Bein erhaelt die positive Rate an jedem Haltetag (Open t bis Open t+1), wie in simulate()
                if cur is not None:
                    cur["funding"] += fd[t]
            trs[c] = tr; acts[c] = active
            CFG_LOG.append(dict(variant="CC", config=cname, side="N", coin=c, params=json.dumps(p), n_trades=len(tr), active_from=str(active.date())))
        variant_runs[("CC", cname, "N")] = (sims, trs, acts, p)

    # ---------------- Auswertung: primaere Varianten und Jitter
    def get_run(vid, cname, side):
        if side == "LS":
            if (vid, cname, "LS") in variant_runs:
                return variant_runs[(vid, cname, "LS")]
            sL = variant_runs.get((vid, cname, "L")); sS = variant_runs.get((vid, cname, "S"))
            if sL is None or sS is None: return None
            sims = {c: combine_LS(sL[0][c], sS[0][c]) for c in sL[0] if c in sS[0]}
            trs = {c: sL[1].get(c, []) + sS[1].get(c, []) for c in sims}
            acts = {c: min(sL[2][c], sS[2][c]) for c in sims}
            return sims, trs, acts, sL[3]
        return variant_runs.get((vid, cname, side))

    def side_list(vid):
        return SIDES[vid]

    eval_cache = {}
    def eval_run(vid, cname, side, primary):
        r = get_run(vid, cname, side)
        if r is None: return None
        sims, trs, acts, params = r
        V = next(v for v in VARIANTS if v["id"] == vid)
        res = evaluate(vid, side, sims, trs, acts, params, V["family"], V["cls"], primary)
        res["config"] = cname; res["params"] = params
        return res

    # Benchmarks je Coin auf Basis der K1-Exposure der primaeren Variante
    for V in VARIANTS:
        vid = V["id"]
        for side in side_list(vid):
            res = eval_run(vid, "base", side, True)
            if res is None: continue
            sims, trs, acts, params = get_run(vid, "base", side)
            # Benchmarks
            bench_pool = {"BH": {}, "EP": {}, "VP": {}, "CASH": {}}
            coin_r = {}
            for c in sims:
                sim1 = sims[c]["K1"]; m = sim1["net"].notna()
                avg_long = float(sim1["w"][m].clip(lower=0).mean()); avg_short = float((-sim1["w"][m]).clip(lower=0).mean())
                eqc = L.equity_stats(sim1["net"], data[c].cash_daily)
                b = bench_sims(data[c], acts[c], avg_long, avg_short, eqc["vol"] if eqc else np.nan)
                epk = "EP_S" if side == "S" else "EP_L"
                bench_pool["BH"][c] = b["BH"]["K1"]; bench_pool["EP"][c] = b[epk]["K1"]; bench_pool["VP"][c] = b["VP"]["K1"]; bench_pool["CASH"][c] = b["CASH"]["K1"]
                coin_r[c] = data[c].r_o2o.where(m)
                res["coins"][c] = dict(avg_w_long=avg_long, avg_w_short=avg_short, active_from=str(acts[c].date()),
                                       bench={k: L.equity_stats(b[k]["K1"]["net"], data[c].cash_daily) for k in ["BH", epk, "VP", "CASH"]})
            # Portfolio-Modus (XS21): EP und Cash summieren sich wie die Strategie, B&H und VP bleiben gleichgewichtete Coin-Mittel
            pb = {k: pooled(v, pool_mode(vid) if k in ("EP", "CASH") else "mean", data[coins[0]].cash_daily) for k, v in bench_pool.items()}
            res["bench_pooled"] = {k: L.equity_stats(pb[k]["net"], data[coins[0]].cash_daily) for k in pb}
            bench_r = pd.concat(coin_r, axis=1).mean(axis=1)
            if side == "S": bench_r = -bench_r
            st = res["scenarios"]["K1"]["pooled"]["equity"]
            res["beta"] = beta_tests(res["_pool_net"], bench_r, data[coins[0]].cash_daily, res["bench_pooled"]["EP"], st) if st else None
            # BTC-B&H als Referenz
            res["bench_pooled"]["BTC_BH"] = L.equity_stats(L.simulate(data["BTC"], pd.Series(1.0, index=data["BTC"].idx), L.COST["K1"])["net"].where(res["_pool_net"].notna()), data["BTC"].cash_daily) if "BTC" in data else None
            # Bootstrap (gepoolt, K1)
            x = res["_pool_net"].dropna(); ex = (x - data[coins[0]].cash_daily.reindex(x.index).fillna(0)).values
            if len(ex) > 100:
                means, shs = L.block_bootstrap(ex, n_rep=args.nboot)
                res["boot"] = dict(p5_ann=float(np.percentile(means, 5) * L.DAYS), p_sharpe=float((shs <= 0).mean()), sharpe_ci=[float(np.percentile(shs, 5)), float(np.percentile(shs, 95))])
            else:
                res["boot"] = dict(p5_ann=np.nan, p_sharpe=1.0)
            res["trade_boot_p5"] = L.trade_bootstrap([t["pnl_net"] for t in res["_trades"]], n_rep=args.nboot)
            # Jitter und Achsen-Nachbarn
            neigh = []
            for cname, _ in JITTER.get(vid, []):
                rj = eval_run(vid, cname, side, False)
                if rj: neigh.append((cname, rj["scenarios"]["K1"]["pooled"]))
            for ax in AXIS.get(vid, []):
                if ":" in ax:
                    v2, cn = ax.split(":"); rj = eval_run(v2, cn, side, False)
                else:
                    rj = eval_run(ax, "base", side, False)
                if rj: neigh.append((ax, rj["scenarios"]["K1"]["pooled"]))
            res["neighbours"] = [dict(name=n, expectancy=p["expectancy"], sharpe=p["equity"]["sharpe"] if p["equity"] else np.nan, cagr=p["equity"]["cagr"] if p["equity"] else np.nan) for n, p in neigh]
            results[f"{vid}|{side}"] = res

    # ---------------- Holm je Familie, DSR, Kriterien
    for fam in ["A", "B", "C", "D"]:
        keys = [k for k, r in results.items() if not r.get("skipped") and r["family"] == fam and r.get("primary")]
        if not keys: continue
        pv = {k: results[k]["boot"]["p_sharpe"] for k in keys}
        adj = L.holm(pv)
        srs = []
        for k in keys:
            eq = results[k]["scenarios"]["K1"]["pooled"]["equity"]
            srs.append(eq["sharpe"] / math.sqrt(L.DAYS) if eq and not np.isnan(eq["sharpe"]) else 0.0)
        var_sr = float(np.var(srs, ddof=1)) if len(srs) > 1 else 0.0
        n_trials = FAMILY_N[fam] if FAMILY_N[fam] else len(keys)
        for k in keys:
            r = results[k]; r["holm_p"] = adj[k]; r["family_n"] = n_trials
            x = r["_pool_net"].dropna(); ex = x - data[coins[0]].cash_daily.reindex(x.index).fillna(0)
            sr_d = ex.mean() / ex.std(ddof=1) if ex.std(ddof=1) > 0 else np.nan
            r["dsr"] = L.deflated_sharpe(sr_d, len(ex), float(ex.skew()), float(ex.kurt() + 3), n_trials, var_sr)
            r["dsr_all_jitter"] = L.deflated_sharpe(sr_d, len(ex), float(ex.skew()), float(ex.kurt() + 3), n_trials + sum(len(JITTER.get(v["id"], [])) for v in VARIANTS if v["family"] == fam), var_sr)

    # Kriterien
    for k, r in results.items():
        if r.get("skipped"): continue
        K1 = r["scenarios"]["K1"]; P = K1["pooled"]; eq = P["equity"]
        cash_ann = float(((1 + data[coins[0]].cash_daily) ** L.DAYS - 1).loc[r["_pool_net"].dropna().index].mean()) if eq else np.nan
        # Eignung je Coin
        elig = {}
        for c, cm in K1["coins"].items():
            e = cm["equity"]; n = cm["trades"]["n"]
            elig[c] = bool(e and e["n_days"] >= 750 and n >= 20)
        def coin_ok(c):
            cm = K1["coins"][c]; e = cm["equity"]; t = cm["trades"]
            # Cash-Referenz je Coin ueber die Tage, an denen der Coin selbst Daten hat (Pool-Index ist die Vereinigung aller Coins)
            cc_ann = float(((1 + data[c].cash_daily) ** L.DAYS - 1).reindex(r["_pool_net"].dropna().index).dropna().mean())
            return bool(e and t["n"] > 0 and t["expectancy"] > 0 and e["cagr"] > cc_ann)
        core_ok = all(coin_ok(c) for c in L.CORE if c in K1["coins"]) and all(c in K1["coins"] for c in L.CORE)
        others = [c for c in elig if elig[c] and c not in L.CORE]
        maj = (sum(coin_ok(c) for c in others) > len(others) / 2) if others else True
        is_xs = r["id"] == "XS21"
        c1 = bool(eq and P["expectancy"] > 0 and eq["cagr"] > cash_ann and (is_xs or (core_ok and maj)))
        share = float(np.mean([coin_ok(c) for c in elig if elig[c]])) if any(elig.values()) else np.nan
        blocks = P["blocks"]; valid = [b for b in blocks.values() if b["valid"]]
        c3 = bool(sum(b["expectancy"] > 0 for b in valid) >= 2)
        neigh = r["neighbours"]
        if neigh:
            pos = np.mean([n["expectancy"] > 0 for n in neigh if not np.isnan(n["expectancy"])]) if any(not np.isnan(n["expectancy"]) for n in neigh) else 0
            med = np.nanmedian([n["sharpe"] for n in neigh])
            base_sh = eq["sharpe"] if eq else np.nan
            c4 = bool(pos >= 2 / 3 and (med > 0 and base_sh <= 1.5 * med))
            c4_note = ""
        else:
            c4 = False; c4_note = "keine Nachbarn vorregistriert (n/a)"
        need_pool, need_core = L.TRADE_CLASS[r["cls"]]
        tpc = P["trades_per_coin"]
        c5 = bool(P["n_trades"] >= need_pool and (is_xs or all(tpc.get(c, 0) >= need_core for c in L.CORE if c in tpc)))
        ep = r["bench_pooled"]["EP"]
        c6 = bool(eq and ep and eq["maxdd"] >= ep["maxdd"])
        c7 = bool(r["beta"] and (r["beta"]["alpha_test"] or r["beta"]["risk_test"]))
        c8 = bool(r["boot"]["p5_ann"] > 0 and r.get("holm_p", 1.0) < 0.05)
        crit = dict(c1=c1, c2_share=share, c3=c3, c4=c4, c4_note=c4_note, c5=c5, c6=c6, c7=c7, c8=c8, elig=elig, cash_ann=cash_ann)
        allc = [c1, c3, c4, c5, c6, c7, c8]
        if all(allc): verdict = "BESTANDEN"
        elif c1 and c5 and c8: verdict = "TEILWEISE"
        else: verdict = "VERWORFEN"
        K2 = r["scenarios"]["K2"]["pooled"]
        crit["robust_k2"] = bool(K2["equity"] and K2["expectancy"] > 0 and K2["equity"]["cagr"] > cash_ann)
        crit["low_trade_note"] = (r["cls"] == "L")
        r["criteria"] = crit; r["verdict"] = verdict
        r["beta_label"] = r["beta"]["label"] if r["beta"] else "n/a"

    # ---------------- Fingerprint (Familie A, Long-only, BTC und ETH, K1)
    bear_years = {}
    if "BTC" in data:
        eqb = (1 + data["BTC"].r_o2o.fillna(0)).cumprod()
        yr = eqb.resample("YE").last().pct_change(); yr.iloc[0] = eqb.resample("YE").last().iloc[0] - 1
        bear_years = {str(k.year): float(v) for k, v in yr.items() if v < 0}
    fingerprint = {}
    for V in VARIANTS:
        if V["family"] != "A": continue
        r = results.get(f"{V['id']}|L")
        if not r: continue
        fp = {}
        for c in ["BTC", "ETH"]:
            if c not in r["scenarios"]["K1"]["coins"]: continue
            cm = r["scenarios"]["K1"]["coins"][c]; t = cm["trades"]; e = cm["equity"]
            sim = daily_store[(V["id"], "L", c)]
            w = variant_runs[(V["id"], "base", "L")][0][c]["K1"]["w"]
            m = sim.notna()
            bear_expo = float(w[m][w[m].index.year.astype(str).isin(list(bear_years.keys()))].mean()) if bear_years else np.nan
            per_year = t["n"] / e["years"] if e and t["n"] else np.nan
            R = t.get("R", {}) if t["n"] else {}
            is_w0 = V["params"]["mode"] == "cross"
            traits = dict(signals=(per_year, 4 <= per_year <= 12 if not np.isnan(per_year) else False),
                          hold=(t.get("avg_hold"), 45 <= t.get("avg_hold", 0) <= 135),
                          win=(t.get("win_rate"), 0.30 <= t.get("win_rate", 0) <= 0.50),
                          top10=(t.get("top10_share"), (t.get("top10_share") or 0) >= 0.50),
                          top5=(t.get("top5_share"), (t.get("top5_share") or 0) >= 0.30),
                          bear=(bear_expo, bear_expo <= 0.25 if not np.isnan(bear_expo) else False))
            if not is_w0 and R.get("n"):
                traits.update(medR=((R["median"], R["mean"]), R["median"] <= 0.5 and R["mean"] > R["median"]),
                              p90R=(R["p90"], R["p90"] >= 3.0), skewR=(R["skew"], (R["skew"] or 0) > 1.0))
            n_ok = sum(1 for v in traits.values() if v[1]); n_tot = len(traits)
            if is_w0:
                label = "strukturell aehnlich" if n_ok >= 4 else "teilweise aehnlich" if n_ok >= 2 else "nicht aehnlich"
            else:
                label = "strukturell aehnlich" if n_ok >= 7 else "teilweise aehnlich" if n_ok >= 4 else "nicht aehnlich"
            fp[c] = dict(traits={k: [v[0], bool(v[1])] for k, v in traits.items()}, n_ok=n_ok, n_tot=n_tot, label=label, R=R, avg_hold_win=t.get("avg_hold_win"))
        fingerprint[V["id"]] = fp

    # ---------------- Ausgabe
    for k, r in results.items():
        if r.get("skipped"): continue
        tr = r.pop("_trades"); r.pop("_pool_net"); r.pop("_pool_expo"); r.pop("_pool_w")
        if tr:
            pd.DataFrame(tr).to_csv(os.path.join(OUT, "stage2_trades", f"{r['id']}_{r['side']}.csv"), index=False)
        for sc in r["scenarios"].values():
            for cm in sc["coins"].values():
                cm["trades"].pop("pnl", None)
    pd.DataFrame(CFG_LOG).to_csv(os.path.join(OUT, "stage2_config_log.csv"), index=False)

    def clean(o):
        if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [clean(v) for v in o]
        if isinstance(o, (np.floating, float)): return None if (isinstance(o, float) and math.isnan(o)) or (isinstance(o, np.floating) and np.isnan(o)) else float(o)
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.bool_,)): return bool(o)
        if isinstance(o, (pd.Timestamp,)): return str(o.date())
        return o
    json.dump(clean(dict(results=results, fingerprint=fingerprint, bear_years=bear_years, oi_check=oi_ok, run_oi=run_oi, family_n=FAMILY_N,
                         inputs=inputs, coins=coins, run_at=dt.datetime.now(dt.timezone.utc).isoformat(), tag=args.tag,
                         prereg_sha256="8f576b7a0b1c5a1adf4b6f0c342398bc8500b287a081923f82f95acc58e1b96e")),
              open(os.path.join(OUT, "stage2_results.json"), "w"), indent=1)
    print("Fertig. Urteile (K1, gepoolt):")
    for k, r in results.items():
        if r.get("skipped"): print(f"  {r['id']}: uebersprungen ({r['reason']})"); continue
        eq = r["scenarios"]["K1"]["pooled"]["equity"]
        print(f"  {k:<10} {r['verdict']:<10} beta={r['beta_label']:<19} CAGR={eq['cagr']*100 if eq else float('nan'):6.1f}%  Sharpe={eq['sharpe'] if eq else float('nan'):5.2f}  MaxDD={eq['maxdd']*100 if eq else float('nan'):6.1f}%  trades={r['scenarios']['K1']['pooled']['n_trades']}")


if __name__ == "__main__":
    main()
