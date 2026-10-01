"""Ideen-Scan v1: EXPLORATIVE Plausibilitaetschecks, NICHT vorregistriert.

Nur oeffentliche Rohdaten aus data/raw, beim Einlesen auf t < 2024-01-01 UTC geschnitten.
Kein Holdout (02_daten/holdout/validation, holdout_manifest) wird gelesen; Kraken-Futures-Funding
(erst ab 2025-09) wird bewusst NICHT ausgewertet, damit 2024+ fuer einen vorregistrierten Test frei bleibt.
Ergebnisse sind Grobindikationen, keine Evidenz (Mehrfachtests, Survivorship, kein Freeze).
"""
import json, os, sys
import numpy as np, pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.path.join(ROOT, "data", "raw")
CUT = pd.Timestamp("2024-01-01", tz="UTC")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "01_forschung", "12_ideen_scan", "explorativ_scan_v1.json")
COINS = ["BTC", "ETH", "XRP", "LTC", "ADA", "BNB", "LINK", "DOT", "SOL", "AVAX"]
K1_SPOT = 0.004 + 0.0005  # Gebuehr + Slippage je Seite (K1, config/cost_model_v1.json: 0.40 % + 0.05 %)
PERP_TAKER = 0.0005       # Kraken Derivatives Basis-Taker 0.05 % (Gebuehrenseite, 2026)


def ts(s):
    return pd.to_datetime(s, utc=True, format="ISO8601")


def load_funding(c):
    f = pd.read_csv(os.path.join(RAW, "binance_funding", f"{c}USDT_funding.csv"))
    f["t"] = ts(f["t"]).dt.floor("h")
    f = f[f["t"] < CUT].drop_duplicates("t").set_index("t")
    return f["rate"].astype(float)


def load_1d(c):
    d = pd.read_csv(os.path.join(RAW, "binance_full", f"{c}USDT_1d.csv"), usecols=["t", "close"])
    d["t"] = ts(d["t"])
    d = d[d["t"] < CUT].set_index("t")["close"].astype(float)
    return d


def funding_check():
    res = {}
    for c in COINS:
        r = load_funding(c)
        daily = r.resample("D").sum()
        per_year = {str(y): round(float(v.sum() / len(v) * 365 * 100), 2) for y, v in daily.groupby(daily.index.year) if len(v) > 200}
        roll30 = daily.rolling(30).sum()
        res[c] = {
            "von": str(r.index[0].date()), "bis": str(r.index[-1].date()),
            "ann_mittel_pct": round(float(daily.mean() * 365 * 100), 2),
            "ann_median_tag_pct": round(float(daily.median() * 365 * 100), 2),
            "anteil_perioden_positiv": round(float((r > 0).mean()), 3),
            "anteil_tage_negativ": round(float((daily < 0).mean()), 3),
            "schlechteste_30d_summe_pct": round(float(roll30.min() * 100), 2),
            "je_jahr_ann_pct": per_year,
        }
    # Cash-and-carry dauerhaft (BTC, ETH): Funding minus einmalige Ein-/Ausstiegskosten pro Jahr,
    # Kapital = 1 Spot + 0.5 Margin fuer den Short (Annahme), also Rendite / 1.5.
    carry = {}
    rt = 2 * K1_SPOT + 2 * PERP_TAKER
    for c in ["BTC", "ETH"]:
        daily = load_funding(c).resample("D").sum()
        yrs = {}
        for y, v in daily.groupby(daily.index.year):
            if len(v) < 200:
                continue
            g = float(v.sum())
            yrs[str(y)] = {"funding_pct": round(g * 100, 2), "netto_auf_kapital_pct": round((g - rt) / 1.5 * 100, 2)}
        carry[c] = yrs
    # Regel mit Schaltern: im Markt, wenn das 7-Tage-Mittel des Funding > 0 (Entscheid am Tagesende, Wirkung ab Folgetag)
    switch = {}
    for c in ["BTC", "ETH"]:
        daily = load_funding(c).resample("D").sum()
        on = (daily.rolling(7).mean() > 0).shift(1).fillna(False).astype(bool)
        trades = int((on.astype(int).diff().abs() > 0).sum())
        g = float(daily[on].sum())
        yrs = len(daily) / 365
        switch[c] = {"jahre": round(yrs, 2), "anteil_im_markt": round(float(on.mean()), 3), "schaltvorgaenge": trades,
                     "funding_ann_pct": round(g / yrs * 100, 2),
                     "kosten_ann_pct": round(trades / 2 * rt / yrs * 100, 2),
                     "netto_ann_auf_kapital_pct": round((g - trades / 2 * rt) / yrs / 1.5 * 100, 2)}
    return {"funding_binance_2020_2023": res, "carry_dauerhaft": carry, "carry_schalter_7d": switch,
            "annahmen": {"roundtrip_kosten": rt, "kapitalfaktor": 1.5, "hinweis": "Binance-Funding (8h), nicht Kraken; Kraken-Funding stuendlich, eigene Hoehe"}}


def perf(ret):
    ret = ret.dropna()
    eq = (1 + ret).cumprod()
    yrs = len(ret) / 365
    cagr = eq.iloc[-1] ** (1 / yrs) - 1
    vol = ret.std() * np.sqrt(365)
    dd = (eq / eq.cummax() - 1).min()
    return {"cagr_pct": round(cagr * 100, 1), "vol_pct": round(vol * 100, 1), "sharpe_0": round(ret.mean() / ret.std() * np.sqrt(365), 2), "maxdd_pct": round(dd * 100, 1)}


def rebalancing_check():
    basket = ["BTC", "ETH", "XRP", "LTC", "ADA", "BNB"]  # alle ab 2018-05 verfuegbar
    px = pd.concat({c: load_1d(c) for c in basket}, axis=1).dropna()
    px = px[px.index >= "2018-06-01"]
    r = px.pct_change().fillna(0)
    out = {"basket": basket, "von": str(px.index[0].date()), "bis": str(px.index[-1].date())}
    # Buy-and-hold gleichgewichtet ab Start
    w0 = np.repeat(1 / len(basket), len(basket))
    bh_eq = (px / px.iloc[0]) @ w0
    out["buy_and_hold"] = perf(bh_eq.pct_change())
    for freq, lab in [("MS", "monatlich"), ("QS", "quartalsweise")]:
        dates = set(pd.date_range(px.index[0], px.index[-1], freq=freq, tz="UTC"))
        w = w0.copy(); eqv = 1.0; rets = []; turn = 0.0
        for t, row in r.iterrows():
            gross = float(w @ (1 + row.values))
            w = w * (1 + row.values) / gross
            cost = 0.0
            if t in dates:
                tv = float(np.abs(w - w0).sum())
                cost = tv * K1_SPOT; turn += tv; w = w0.copy()
            rets.append(gross * (1 - cost) - 1)
        rr = pd.Series(rets, index=r.index)
        p = perf(rr); p["turnover_summe"] = round(turn, 2)
        out[f"rebal_{lab}_K1"] = p
    out["btc_buy_and_hold"] = perf(px["BTC"].pct_change())
    return out


def voltarget_check():
    out = {}
    for c in ["BTC", "ETH"]:
        p = load_1d(c)
        p = p[p.index >= "2018-01-01"]
        r = p.pct_change()
        vol = r.rolling(30).std() * np.sqrt(365)
        res = {"buy_and_hold": perf(r)}
        for tgt in [0.4, 0.6]:
            w = (tgt / vol).clip(upper=1.0)
            trend = (p > p.rolling(200).mean()).astype(float)
            for lab, ww in [("vt", w), ("vt_trend200", w * trend)]:
                # Band: nur umschichten, wenn |Abweichung| > 0.1 (Kostenbegrenzung); Entscheid Tagesende, Wirkung Folgetag
                held = []; cur = 0.0
                for x in ww.fillna(0).values:
                    if abs(x - cur) > 0.1 or (x == 0 and cur != 0):
                        cur = x
                    held.append(cur)
                h = pd.Series(held, index=ww.index).shift(1).fillna(0)
                cost = h.diff().abs().fillna(0) * K1_SPOT
                net = h * r - cost
                pr = perf(net); pr["umschichtungen"] = int((h.diff().abs() > 0).sum()); pr["mittl_gewicht"] = round(float(h.mean()), 2)
                res[f"{lab}_{int(tgt*100)}"] = pr
        out[c] = res
    return out


def seasonality_check():
    d = pd.read_csv(os.path.join(RAW, "binance_full", "BTCUSDT_1h.csv"), usecols=["t", "open", "close"])
    d["t"] = ts(d["t"]); d = d[(d["t"] < CUT) & (d["t"] >= "2018-01-01")].set_index("t")
    r = np.log(d["close"] / d["open"])
    hr = r.groupby(r.index.hour).agg(["mean", "std", "count"])
    hr["t"] = hr["mean"] / (hr["std"] / np.sqrt(hr["count"]))
    dr = np.log(d["close"].resample("D").last() / d["open"].resample("D").first()).dropna()
    dw = dr.groupby(dr.index.dayofweek).agg(["mean", "std", "count"])
    dw["t"] = dw["mean"] / (dw["std"] / np.sqrt(dw["count"]))
    def half(x):
        a = x[x.index < "2021-01-01"]; b = x[x.index >= "2021-01-01"]
        return a.groupby(a.index.hour).mean(), b.groupby(b.index.hour).mean()
    a, b = half(r)
    return {"stunde_mittel_bp": {int(k): round(v * 1e4, 2) for k, v in hr["mean"].items()},
            "stunde_t": {int(k): round(v, 2) for k, v in hr["t"].items()},
            "max_abs_t_stunde": round(float(hr["t"].abs().max()), 2),
            "stunden_korrelation_2018_20_vs_2021_23": round(float(np.corrcoef(a.values, b.values)[0, 1]), 2),
            "wochentag_mittel_bp": {int(k): round(v * 1e4, 1) for k, v in dw["mean"].items()},
            "wochentag_t": {int(k): round(v, 2) for k, v in dw["t"].items()},
            "k1_roundtrip_bp": round(2 * K1_SPOT * 1e4, 1)}


def cross_exchange_check():
    k = pd.read_csv(os.path.join(RAW, "kraken_1h", "BTCUSD_1h.csv"), usecols=["t", "close"])
    k["t"] = ts(k["t"]); k = k.drop_duplicates("t").set_index("t")["close"]
    k = k[k.index < CUT]
    kd = k[k.index.hour == 23]; kd.index = kd.index.floor("D")  # Schluss 23:00-Kerze = 24:00 UTC
    out = {}
    for ex in ["coinbase", "bitstamp"]:
        e = pd.read_csv(os.path.join(RAW, ex, "BTCUSD_1d.csv"), usecols=["t", "close"])
        e["t"] = pd.to_datetime(e["t"], utc=True); e = e.set_index("t")["close"]
        j = pd.concat([kd, e], axis=1, keys=["k", "e"]).dropna()
        j = j[j.index >= "2019-01-01"]
        sp = (j["k"] / j["e"] - 1).abs() * 1e4
        out[ex] = {"tage": int(len(sp)), "median_abs_bp": round(float(sp.median()), 1), "p95_abs_bp": round(float(sp.quantile(0.95)), 1),
                   "anteil_ueber_k1_roundtrip": round(float((sp > 2 * K1_SPOT * 1e4).mean()), 3),
                   "hinweis": "Tagesschluss, Zeitstempel je Boerse nicht exakt synchron; ueberschaetzt eher"}
    return out


if __name__ == "__main__":
    res = {"status": "EXPLORATIV, nicht vorregistriert", "daten_bis_exklusiv": str(CUT.date()),
           "funding": funding_check(), "rebalancing": rebalancing_check(), "voltarget": voltarget_check(),
           "saisonalitaet": seasonality_check(), "cross_exchange": cross_exchange_check()}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))
