#!/usr/bin/env python3
"""
Project Aurum II — Stufe 1 Rechenlauf (Regime-Forschung)
Umsetzung der eingefrorenen Vorregistrierung STUFE1_VORREGISTRIERUNG_2026-09-15.md (Version 1.0).

Kein PnL. Keine Handelsregel. Nur Zustandseigenschaften.
Alle Indikatoren strikt trailing (nur Information bis einschliesslich t).
"""
import os, json, hashlib, csv, sys, datetime as dt
import numpy as np
import pandas as pd

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(OUT, "stage1_labels"), exist_ok=True)

COINS = ["BTC", "ETH", "SOL", "XRP", "ADA", "AVAX", "LINK", "DOT", "BNB", "LTC"]
CORE = ["BTC", "ETH"]
KRAKEN = {"BTC": "XBT_USD", "ETH": "ETH_USD", "SOL": "SOL_USD"}
FUNDING = {"BTC": "PF_XBTUSD", "ETH": "PF_ETHUSD", "SOL": "PF_SOLUSD"}

# ---------------------------------------------------------------- eingefrorene Parameter
BASE = dict(ma_fast=100, ma_slow=200, slope_k=10, adx_n=14, atr_n=14, w_vol=252,
            bb_n=20, bb_mult=2.0, w_dd=100, q_lo=0.20, q_hi=0.80, s_atr=0.70,
            vol_conf=0.5, f_thr=0.10, f_hours=168)

CANDIDATES = {
    "R1": dict(d1="a", d2="bbw", d3=False, d4=False, adx_thr=20, dd_thr=None),
    "R2": dict(d1="b", d2="bbw", d3=True,  d4=False, adx_thr=20, dd_thr=-0.30),
    "R3": dict(d1="b", d2="bbw", d3=True,  d4=True,  adx_thr=20, dd_thr=-0.30),
    "R4": dict(d1="b", d2="bbw", d3=True,  d4=False, adx_thr=25, dd_thr=-0.30),
    "R5": dict(d1="b", d2="atr", d3=True,  d4=False, adx_thr=15, dd_thr=-0.20),
}

THR = dict(dwell_frequent=10, dwell_rare=5, one_bar_max=0.25,
           switches={"D1": 30, "D2": 30, "D3": 12, "D4": 30, "D5": 30},
           jitter_mean=0.85, jitter_min=0.75, block_share=0.70, block_factor=2.0,
           min_bars_coin=750, min_bars_block=200, kraken_agree=0.90)

FREQUENT = {"UP", "DOWN", "RANGE", "NORMAL", "CALM", "CONFIRMED", "UNCONFIRMED", "NEUTRAL"}
RARE = {"STRESS_DOWN", "STRESS_UP", "EXPANSION", "SQUEEZE", "POS", "NEG"}

HALVING_BLOCKS = [("H1", "2017-08-01", "2020-05-11"), ("H2", "2020-05-11", "2024-04-20"), ("H3", "2024-04-20", "2030-01-01")]

CONFIG_LOG = []   # jede gerechnete Konfiguration


# ---------------------------------------------------------------- Daten
def load_ohlc(path):
    d = pd.read_csv(path)
    d["t"] = pd.to_datetime(d["t"], utc=True)
    d = d.set_index("t").sort_index()
    for c in ["open", "high", "low", "close", "volume"]:
        d[c] = d[c].astype(float)
    return d


def load_funding(coin, px):
    p = os.path.join(RAW, "funding", f"{FUNDING[coin]}_funding.csv")
    f = pd.read_csv(p)
    f["timestamp"] = pd.to_datetime(f["timestamp"], utc=True)
    f = f.set_index("timestamp").sort_index()
    daily_close = px["close"].reindex(f.index.floor("D"))
    f["rel"] = f["funding_rate"].values / daily_close.values
    f = f.dropna(subset=["rel"])
    return f


# ---------------------------------------------------------------- Indikatoren (trailing)
def wilder(series, n):
    """Wilder-Glaettung: erster Wert = SMA(n), danach (prev*(n-1)+x)/n."""
    x = series.values.astype(float)
    out = np.full_like(x, np.nan)
    if len(x) < n:
        return pd.Series(out, index=series.index)
    first = np.nanmean(x[:n])
    out[n - 1] = first
    for i in range(n, len(x)):
        out[i] = (out[i - 1] * (n - 1) + x[i]) / n
    return pd.Series(out, index=series.index)


def adx_wilder(h, l, c, n):
    prev_c = c.shift(1)
    tr = pd.concat([h - l, (h - prev_c).abs(), (l - prev_c).abs()], axis=1).max(axis=1)
    up = h.diff()
    dn = -l.diff()
    plus_dm = np.where((up > dn) & (up > 0), up, 0.0)
    minus_dm = np.where((dn > up) & (dn > 0), dn, 0.0)
    atr = wilder(tr.iloc[1:], n).reindex(tr.index)
    pdm = wilder(pd.Series(plus_dm, index=h.index).iloc[1:], n).reindex(h.index)
    mdm = wilder(pd.Series(minus_dm, index=h.index).iloc[1:], n).reindex(h.index)
    pdi = 100 * pdm / atr
    mdi = 100 * mdm / atr
    dx = 100 * (pdi - mdi).abs() / (pdi + mdi)
    adx = wilder(dx.dropna(), n).reindex(h.index)
    return adx, atr


def trailing_pct(series, w):
    """Perzentilrang: Anteil der Werte im Fenster (inkl. aktuellem), die <= aktuell sind."""
    x = series.values.astype(float)
    out = np.full_like(x, np.nan)
    for i in range(w - 1, len(x)):
        win = x[i - w + 1:i + 1]
        if np.isnan(win).any():
            continue
        out[i] = np.sum(win <= x[i]) / w
    return pd.Series(out, index=series.index)


def indicators(d, p):
    c, h, l, v = d["close"], d["high"], d["low"], d["volume"]
    ind = pd.DataFrame(index=d.index)
    ma_f = c.rolling(p["ma_fast"]).mean()
    ma_s = c.rolling(p["ma_slow"]).mean()
    ind["above_f"] = (c > ma_f).where(ma_f.notna())
    ind["above_s"] = (c > ma_s).where(ma_s.notna())
    ind["slope_f"] = np.sign(ma_f - ma_f.shift(p["slope_k"])).where(ma_f.shift(p["slope_k"]).notna())
    adx, atr = adx_wilder(h, l, c, p["adx_n"])
    ind["adx"] = adx
    atr14 = atr if p["atr_n"] == p["adx_n"] else adx_wilder(h, l, c, p["atr_n"])[1]
    ind["atr_pct"] = trailing_pct(atr14 / c, p["w_vol"])
    ma20 = c.rolling(p["bb_n"]).mean()
    sd20 = c.rolling(p["bb_n"]).std(ddof=1)
    bbw = (2 * p["bb_mult"] * sd20) / ma20
    ind["bbw_pct"] = trailing_pct(bbw, p["w_vol"])
    ind["dd"] = c / c.rolling(p["w_dd"]).max() - 1
    ind["du"] = c / c.rolling(p["w_dd"]).min() - 1
    ind["vol_pct"] = trailing_pct(v, p["w_vol"])
    return ind


# ---------------------------------------------------------------- Labels
def labels(ind, cand, p):
    L = pd.DataFrame(index=ind.index)
    # D1
    ok1 = ind["adx"].notna() & ind["above_f"].notna() & (ind["slope_f"].notna() if cand["d1"] == "b" else True)
    strong = ind["adx"] >= cand["adx_thr"]
    up = strong & (ind["above_f"] == True)
    dn = strong & (ind["above_f"] == False)
    if cand["d1"] == "b":
        up &= ind["slope_f"] == 1
        dn &= ind["slope_f"] == -1
    d1 = np.where(up, "UP", np.where(dn, "DOWN", "RANGE"))
    L["D1"] = pd.Series(d1, index=ind.index).where(ok1, None)
    # D2
    src = ind["bbw_pct"] if cand["d2"] == "bbw" else ind["atr_pct"]
    d2 = np.where(src <= p["q_lo"], "SQUEEZE", np.where(src >= p["q_hi"], "EXPANSION", "NORMAL"))
    L["D2"] = pd.Series(d2, index=ind.index).where(src.notna(), None)
    # D3
    if cand["d3"]:
        dd_thr = cand["dd_thr"]
        du_thr = abs(dd_thr) / (1 - abs(dd_thr))
        ok3 = ind["dd"].notna() & ind["atr_pct"].notna() & ind["above_s"].notna()
        sdn = (ind["dd"] <= dd_thr) & (ind["atr_pct"] >= p["s_atr"]) & (ind["above_s"] == False)
        sup = (ind["du"] >= du_thr) & (ind["atr_pct"] >= p["s_atr"]) & (ind["above_s"] == True)
        d3 = np.where(sdn, "STRESS_DOWN", np.where(sup, "STRESS_UP", "CALM"))
        L["D3"] = pd.Series(d3, index=ind.index).where(ok3, None)
    # D4
    if cand["d4"]:
        d4 = np.where(ind["vol_pct"] >= p["vol_conf"], "CONFIRMED", "UNCONFIRMED")
        L["D4"] = pd.Series(d4, index=ind.index).where(ind["vol_pct"].notna(), None)
    # konsolidiert
    lab = []
    for i in range(len(L)):
        r = L.iloc[i]
        if r.isna().any():
            lab.append(None); continue
        if cand["d3"] and r["D3"] != "CALM":
            lab.append(r["D3"])
        elif r["D2"] == "EXPANSION":
            lab.append("EXPANSION")
        elif r["D1"] in ("UP", "DOWN"):
            lab.append(r["D1"])
        elif r["D2"] == "SQUEEZE":
            lab.append("SQUEEZE")
        else:
            lab.append("RANGE")
    L["label"] = lab
    return L


def funding_labels(f, f_thr, hours):
    f7 = f["rel"].rolling(f"{hours}h").mean() * 8760
    daily = f7.groupby(f7.index.floor("D")).last()
    lab = np.where(daily >= f_thr, "POS", np.where(daily <= -f_thr, "NEG", "NEUTRAL"))
    s = pd.Series(lab, index=daily.index)
    # ersten 7 Tage undefined (Fenster nicht voll)
    s.iloc[:7] = None
    return s


# ---------------------------------------------------------------- Metriken
def episodes(seq):
    """Liste (state, laenge) fuer eine Sequenz ohne None."""
    eps = []
    cur, n = None, 0
    for s in seq:
        if s == cur:
            n += 1
        else:
            if cur is not None:
                eps.append((cur, n))
            cur, n = s, 1
    if cur is not None:
        eps.append((cur, n))
    return eps


def _defined(x):
    if x is None:
        return False
    if isinstance(x, float) and np.isnan(x):
        return False
    return True


def dim_metrics(seq):
    seq = [s for s in seq if _defined(s)]
    if len(seq) < 2:
        return None
    eps = episodes(seq)
    by_state = {}
    for s, n in eps:
        by_state.setdefault(s, []).append(n)
    dwell = {s: float(np.median(v)) for s, v in by_state.items()}
    shares = {s: sum(v) / len(seq) for s, v in by_state.items()}
    one_bar = sum(1 for _, n in eps if n == 1) / len(eps)
    switches = (len(eps) - 1) / len(seq) * 252
    return dict(n=len(seq), dwell=dwell, share=shares, one_bar=one_bar, switches=switches, n_eps=len(eps))


def passes(m, dim):
    """Hard-Fail je Dimension auf einer Sequenz. Rueckgabe (ok, gruende)."""
    if m is None:
        return False, ["zu wenig Daten"]
    why = []
    for s, dw in m["dwell"].items():
        need = THR["dwell_rare"] if s in RARE else THR["dwell_frequent"]
        if dw < need:
            why.append(f"Dwell {s} {dw:.1f} < {need}")
    if m["one_bar"] > THR["one_bar_max"]:
        why.append(f"Ein-Bar {m['one_bar']:.0%} > 25%")
    if m["switches"] > THR["switches"][dim]:
        why.append(f"Wechsel {m['switches']:.1f} > {THR['switches'][dim]}")
    return len(why) == 0, why


def agreement(a, b):
    m = a.notna() & b.notna()
    if m.sum() == 0:
        return np.nan
    return float((a[m] == b[m]).mean())


# ---------------------------------------------------------------- Jitter-Varianten
def jitter_variants(cand):
    """Liste (name, params_override, cand_override, betroffene Dimensionen)."""
    out = []
    out.append(("adx-2", {}, {"adx_thr": cand["adx_thr"] - 2}, {"D1"}))
    out.append(("adx+2", {}, {"adx_thr": cand["adx_thr"] + 2}, {"D1"}))
    out.append(("ma90", {"ma_fast": 90}, {}, {"D1"}))
    out.append(("ma110", {"ma_fast": 110}, {}, {"D1"}))
    out.append(("band-0.05", {"q_lo": 0.15, "q_hi": 0.85}, {}, {"D2"}))
    out.append(("band+0.05", {"q_lo": 0.25, "q_hi": 0.75}, {}, {"D2"}))
    wdims = {"D2", "D4"} | ({"D3"} if cand["d3"] else set())
    out.append(("wvol189", {"w_vol": 189}, {}, wdims))
    out.append(("wvol315", {"w_vol": 315}, {}, wdims))
    if cand["d3"]:
        out.append(("dd-0.05", {}, {"dd_thr": cand["dd_thr"] - 0.05}, {"D3"}))
        out.append(("dd+0.05", {}, {"dd_thr": cand["dd_thr"] + 0.05}, {"D3"}))
    return out


# ---------------------------------------------------------------- Hauptlauf
def main():
    prov = json.load(open(os.path.join(RAW, "provenance.json")))
    prov_map = {e["file"]: e for e in prov}
    data, kraken = {}, {}
    for c in COINS:
        data[c] = load_ohlc(os.path.join(RAW, "binance", f"{c}USDT_1d.csv"))
    for c, k in KRAKEN.items():
        kraken[c] = load_ohlc(os.path.join(RAW, "kraken", f"{k}_1d.csv"))

    report = {}          # cand -> coin -> dict
    verdict = {}
    label_frames = {c: pd.DataFrame(index=data[c].index) for c in COINS}
    ind_cache = {}

    def get_ind(coin, p, src="binance"):
        key = (coin, src, tuple(sorted(p.items())))
        if key not in ind_cache:
            d = data[coin] if src == "binance" else kraken[coin]
            ind_cache[key] = indicators(d, p)
        return ind_cache[key]

    for cid, cand in CANDIDATES.items():
        dims = ["D1", "D2"] + (["D3"] if cand["d3"] else []) + (["D4"] if cand["d4"] else [])
        report[cid] = {}
        for coin in COINS:
            ind = get_ind(coin, BASE)
            L = labels(ind, cand, BASE)
            CONFIG_LOG.append(dict(candidate=cid, coin=coin, variant="base", params=json.dumps({**BASE, **cand}),
                                   n_defined=int(L["label"].notna().sum())))
            for col in L.columns:
                label_frames[coin][f"{cid}_{col}"] = L[col]
            defined = L["label"].notna()
            n_def = int(defined.sum())
            res = dict(n_defined=n_def, dims={}, blocks={}, halving={}, jitter={}, eligible=n_def >= THR["min_bars_coin"])
            # Gesamtmetriken
            for dim in dims:
                m = dim_metrics(L[dim].tolist())
                ok, why = passes(m, dim)
                res["dims"][dim] = dict(metrics=m, ok=ok, why=why)
            # Jitter
            jit = {dim: [] for dim in dims}
            for name, p_over, c_over, affected in jitter_variants(cand):
                p2 = {**BASE, **p_over}
                c2 = {**cand, **c_over}
                L2 = labels(get_ind(coin, p2), c2, p2)
                CONFIG_LOG.append(dict(candidate=cid, coin=coin, variant=name, params=json.dumps({**p2, **c2}),
                                       n_defined=int(L2["label"].notna().sum())))
                for dim in dims:
                    if dim in affected:
                        jit[dim].append((name, agreement(L[dim], L2[dim])))
            for dim in dims:
                vals = [a for _, a in jit[dim] if not np.isnan(a)]
                res["jitter"][dim] = dict(items=jit[dim], mean=float(np.mean(vals)) if vals else np.nan,
                                          min=float(np.min(vals)) if vals else np.nan)
            # Zeitbloecke: Kalenderjahre
            years = sorted(set(L.index[defined].year))
            for y in years:
                Ly = L[(L.index.year == y)]
                if Ly["label"].notna().sum() < THR["min_bars_block"]:
                    continue
                blk = {}
                for dim in dims:
                    m = dim_metrics(Ly[dim].tolist())
                    ok, why = passes(m, dim)
                    blk[dim] = dict(metrics=m, ok=ok, why=why)
                res["blocks"][str(y)] = blk
            # Halving-Zyklen (Gegenprobe, nur Bericht)
            for name, a, b in HALVING_BLOCKS:
                Lh = L[(L.index >= pd.Timestamp(a, tz="UTC")) & (L.index < pd.Timestamp(b, tz="UTC"))]
                if Lh["label"].notna().sum() < THR["min_bars_block"]:
                    continue
                blk = {}
                for dim in dims:
                    m = dim_metrics(Lh[dim].tolist())
                    ok, why = passes(m, dim)
                    blk[dim] = dict(metrics=m, ok=ok, why=why)
                res["halving"][name] = blk
            # Kraken-Gegenprobe
            if coin in kraken:
                Lk = labels(get_ind(coin, BASE, "kraken"), cand, BASE)
                res["kraken_agree"] = {dim: agreement(L[dim], Lk[dim].reindex(L.index)) for dim in dims}
                res["kraken_agree"]["label"] = agreement(L["label"], Lk["label"].reindex(L.index))
            # Coin-Urteil je Dimension
            coin_ok = {}
            for dim in dims:
                g = res["dims"][dim]["ok"]
                j = res["jitter"][dim]
                jok = (not np.isnan(j["mean"])) and j["mean"] >= THR["jitter_mean"] and j["min"] >= THR["jitter_min"]
                blocks = [b[dim] for b in res["blocks"].values()]
                bshare = np.mean([b["ok"] for b in blocks]) if blocks else 0.0
                # Faktor-2-Regel auf Wechselrate und Dwell des haeufigsten Zustands
                sw = [b["metrics"]["switches"] for b in blocks if b["metrics"]]
                f2 = True
                if len(sw) >= 3:
                    med = np.median(sw)
                    if med > 0 and any(s > THR["block_factor"] * med or s < med / THR["block_factor"] for s in sw):
                        f2 = False
                bok = bshare >= THR["block_share"] and f2
                coin_ok[dim] = dict(overall=g, jitter=jok, blocks=bok, block_share=float(bshare), factor2=f2,
                                    ok=bool(g and jok and bok))
            res["coin_ok"] = coin_ok
            report[cid][coin] = res

        # Kandidaten-Urteil
        v = {}
        for dim in dims:
            elig = [c for c in COINS if report[cid][c]["eligible"]]
            core_ok = all(report[cid][c]["coin_ok"][dim]["ok"] for c in CORE)
            others = [c for c in elig if c not in CORE]
            maj = sum(report[cid][c]["coin_ok"][dim]["ok"] for c in others) > len(others) / 2 if others else False
            v[dim] = dict(core=core_ok, majority=maj, ok=bool(core_ok and maj),
                          coins_ok=[c for c in elig if report[cid][c]["coin_ok"][dim]["ok"]])
        verdict[cid] = dict(dims=v, ok=all(x["ok"] for x in v.values()))

    # ---------------- F1 Funding
    f1 = {}
    for coin in ["BTC", "ETH", "SOL"]:
        f = load_funding(coin, data[coin])
        base = funding_labels(f, BASE["f_thr"], BASE["f_hours"])
        CONFIG_LOG.append(dict(candidate="F1", coin=coin, variant="base", params=json.dumps({"f_thr": 0.10}), n_defined=int(base.notna().sum())))
        m = dim_metrics(base.tolist())
        ok, why = passes(m, "D5")
        jit = []
        for name, thr in [("f-0.025", 0.075), ("f+0.025", 0.125)]:
            alt = funding_labels(f, thr, BASE["f_hours"])
            CONFIG_LOG.append(dict(candidate="F1", coin=coin, variant=name, params=json.dumps({"f_thr": thr}), n_defined=int(alt.notna().sum())))
            jit.append((name, agreement(base, alt)))
        jm = float(np.mean([a for _, a in jit])); jmin = float(np.min([a for _, a in jit]))
        jok = jm >= THR["jitter_mean"] and jmin >= THR["jitter_min"]
        f1[coin] = dict(metrics=m, ok=ok, why=why, jitter=jit, jitter_mean=jm, jitter_min=jmin, jitter_ok=jok,
                        overall=bool(ok and jok), start=str(base.index.min().date()), end=str(base.index.max().date()))
        label_frames[coin]["F1_D5"] = base.reindex(label_frames[coin].index.floor("D")).values
    verdict["F1"] = dict(ok=all(v["overall"] for v in f1.values()), coins=f1, provisional=True)

    # ---------------- Ausgaben
    for coin in COINS:
        lf = label_frames[coin].copy()
        lf.index = lf.index.date
        lf.index.name = "date"
        lf.to_csv(os.path.join(OUT, "stage1_labels", f"{coin}.csv"))
    pd.DataFrame(CONFIG_LOG).to_csv(os.path.join(OUT, "stage1_config_log.csv"), index=False)

    def clean(o):
        if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [clean(v) for v in o]
        if isinstance(o, (np.floating, float)): return None if np.isnan(o) else float(o)
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.bool_,)): return bool(o)
        return o
    json.dump(clean(dict(report=report, verdict=verdict, f1=f1, thresholds=THR, base=BASE, candidates=CANDIDATES,
                         inputs={k: v["sha256"] for k, v in prov_map.items()},
                         run_at=dt.datetime.now(dt.timezone.utc).isoformat())),
              open(os.path.join(OUT, "stage1_results.json"), "w"), indent=1)
    print("Fertig. Urteile:")
    for cid, v in verdict.items():
        print(f"  {cid}: {'TAUGLICH' if v['ok'] else 'VERWORFEN'}" + (" (vorlaeufig)" if v.get("provisional") else ""))


if __name__ == "__main__":
    main()
