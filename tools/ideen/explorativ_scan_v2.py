"""Ideen-Scan v2: EXPLORATIVE Plausibilitaetschecks, NICHT vorregistriert (informelle Trials).

Nur oeffentliche Daten, beim Einlesen hart auf t < 2024-01-01 UTC geschnitten.
Kein Holdout (02_daten/holdout, holdout_manifest) wird gelesen. Keine Keys, kein Boersenkontakt.
Quellen: data/raw/binance_full (Spot 1d), data/supplement DTB3, sowie SCAN2_RAW (CoinMetrics Community,
alternative.me Fear&Greed, DefiLlama Stablecoins, FRED), Abruf 01.10.2026 mit end<=2023-12-31 bzw. danach getrimmt.
Kosten K1 Spot je Seite: 0.40 % Gebuehr + 0.02 % Reibung + 0.05 % Slippage = 0.47 % (venue_kraken maker_plan).
"""
import json, os, sys
import numpy as np, pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.path.join(ROOT, "data", "raw")
S2 = os.environ.get("SCAN2_RAW", "/workspace/aurum2/work/scan_v2/raw")
CUT = pd.Timestamp("2024-01-01", tz="UTC")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "01_forschung", "14_ideen_scan_v2", "explorativ_scan_v2.json")
C = 0.0047  # K1 Spot je Seite
D = 365


def cut(s):
    s = s[s.index < CUT]
    assert s.index.max() < CUT
    return s


def spot(c):
    d = pd.read_csv(os.path.join(RAW, "binance_full", f"{c}USDT_1d.csv"), usecols=["t", "close"])
    d["t"] = pd.to_datetime(d["t"], utc=True, format="ISO8601").dt.floor("D")
    return cut(d.set_index("t")["close"].astype(float))


def cm(asset, metric):
    r = json.load(open(os.path.join(S2, f"cm_{asset}_{metric}.json")))["data"]
    s = pd.Series({pd.Timestamp(x["time"]).floor("D"): float(x[metric]) for x in r if x.get(metric) is not None})
    s.index = pd.DatetimeIndex(s.index).tz_convert("UTC") if s.index.tz is not None else pd.DatetimeIndex(s.index).tz_localize("UTC")
    return cut(s.sort_index())


def fred(sid):
    f = pd.read_csv(os.path.join(S2, f"fred_{sid}.csv"))
    f.columns = ["d", "v"]
    f["v"] = pd.to_numeric(f["v"], errors="coerce")
    f["d"] = pd.to_datetime(f["d"]).dt.tz_localize("UTC")
    return cut(f.dropna().set_index("d")["v"])


def tbill(idx):
    t = pd.read_csv(os.path.join(ROOT, "data", "supplement", "DTB3_3m_tbill.csv"))
    t.columns = ["d", "v"]
    t["v"] = pd.to_numeric(t["v"], errors="coerce") / 100
    t["d"] = pd.to_datetime(t["d"]).dt.tz_localize("UTC")
    s = t.dropna().set_index("d")["v"]
    s = s.reindex(idx.union(s.index)).sort_index().ffill().reindex(idx).fillna(0.0)
    return (1 + s) ** (1 / D) - 1


def run(w, rets, rf):
    """w: DataFrame Gewichte je Asset (Signal am Schluss t, gehalten t->t+1). rets: Tagesrenditen. Cash = 1-sum(w) zu rf."""
    w = w.reindex(rets.index).ffill().fillna(0.0)
    wl = w.shift(1).fillna(0.0)
    cost = (w - wl).abs().sum(axis=1).shift(1).fillna(0.0) * C
    r = (wl * rets).sum(axis=1) + (1 - wl.sum(axis=1)) * rf - cost
    return r


def stats(r, rf, w=None):
    r = r.dropna()
    eq = (1 + r).cumprod()
    yrs = len(r) / D
    ex = r - rf.reindex(r.index)
    out = {"von": str(r.index[0].date()), "bis": str(r.index[-1].date()),
           "cagr_pct": round(float(eq.iloc[-1] ** (1 / yrs) - 1) * 100, 1),
           "sharpe_ex": round(float(ex.mean() / ex.std() * np.sqrt(D)), 2) if ex.std() > 0 else None,
           "maxdd_pct": round(float((eq / eq.cummax() - 1).min()) * 100, 1)}
    if w is not None:
        w = w.reindex(r.index).ffill().fillna(0.0)
        out["wechsel"] = int((w.diff().abs().sum(axis=1) > 1e-9).sum())
        out["zeit_im_markt"] = round(float((w.sum(axis=1) > 0).mean()), 2)
    return out


def halves(r, rf, w):
    a = r[r.index < pd.Timestamp("2021-01-01", tz="UTC")]
    b = r[r.index >= pd.Timestamp("2021-01-01", tz="UTC")]
    return {"bis2020": stats(a, rf, w) if len(a) > 300 else None, "ab2021": stats(b, rf, w)}


def state_weights(sig_on, sig_off, idx):
    """Hysterese: 1 nach sig_on, 0 nach sig_off."""
    st, cur = [], 0.0
    on, off = sig_on.reindex(idx).fillna(False), sig_off.reindex(idx).fillna(False)
    for t in idx:
        if cur == 0 and on[t]:
            cur = 1.0
        elif cur == 1 and off[t]:
            cur = 0.0
        st.append(cur)
    return pd.Series(st, index=idx)


def main():
    res = {"hinweis": "EXPLORATIV, nicht vorregistriert, t < 2024-01-01, Kosten K1 Spot 0.47 % je Seite, Cash zu DTB3"}
    btc, eth = spot("BTC"), spot("ETH")
    px = pd.concat({"BTC": btc, "ETH": eth}, axis=1).dropna()
    rets = px.pct_change().fillna(0.0)
    idx = px.index
    rf = tbill(idx)
    one = lambda s, a="BTC": pd.DataFrame({a: s})
    trials = []

    # Referenzen
    bh = run(one(pd.Series(1.0, index=idx)), rets, rf)
    res["ref_btc_buyhold"] = stats(bh, rf)
    tr = (btc > btc.rolling(200).mean()).astype(float).reindex(idx)
    trend = run(one(tr), rets, rf)
    res["ref_btc_sma200"] = stats(trend, rf, one(tr))

    def add(name, w, extra=None):
        r = run(w, rets, rf)
        d = stats(r, rf, w)
        d["haelften"] = halves(r, rf, w)
        d["korr_mit_sma200"] = round(float(r.corr(trend)), 2)
        if extra:
            d.update(extra)
        res[name] = d
        trials.append(name)

    # 1 MVRV-Band (klassische Niveaus 1.0 / 3.5), BTC, laengere CM-Historie separat
    mv = cm("btc", "CapMVRVCur")
    w1 = state_weights(mv < 1.0, mv > 3.5, mv.index)
    add("t1_mvrv_band_1_35", one(w1.reindex(idx).ffill()))
    pcm = cm("btc", "PriceUSD")
    rcm = pd.DataFrame({"BTC": pcm.pct_change().fillna(0.0)})
    rfc = tbill(pcm.index)
    w1l = one(state_weights(mv < 1.0, mv > 3.5, pcm.index))
    r1l = run(w1l, rcm, rfc)
    res["t1_mvrv_band_1_35"]["cm_2014_2023"] = stats(r1l, rfc, w1l)
    res["t1_mvrv_band_1_35"]["cm_2014_2023_buyhold"] = stats(run(one(pd.Series(1.0, index=pcm.index)), rcm, rfc), rfc)
    # 2 Trend mit MVRV-Bremse: SMA200, aber Cash bei MVRV > 3.0
    w2 = (tr * (mv.reindex(idx).ffill() <= 3.0)).astype(float)
    add("t2_sma200_mit_mvrv_bremse_3", one(w2))
    # 3 Exchange-Bestand (SplyExNtv), 30-Tage-Aenderung < 0 => long (Achtung Labelrevisionen = Look-ahead)
    ex = cm("btc", "SplyExNtv")
    w3 = (ex.diff(30) < 0).astype(float).reindex(idx).ffill()
    add("t3_exchange_bestand_sinkt_30d", one(w3), {"vorbehalt": "Adress-Labels von CoinMetrics werden rueckwirkend revidiert, Look-ahead moeglich"})
    # 4 Stablecoin-Angebot, 30-Tage-Wachstum > 0 => long (Publikation: Wert von t-1)
    st = json.load(open(os.path.join(S2, "stables.json")))
    sc = pd.Series({pd.Timestamp(int(x["date"]), unit="s", tz="UTC").floor("D"): float(x["totalCirculatingUSD"]["peggedUSD"]) for x in st})
    sc = cut(sc.sort_index())
    w4 = (sc.pct_change(30) > 0).astype(float).shift(1).reindex(idx).ffill()
    add("t4_stablecoin_wachstum_30d", one(w4))
    # 5 Fear & Greed kontraer: Einstieg < 25, Ausstieg > 75
    fg = json.load(open(os.path.join(S2, "fng.json")))["data"]
    f = cut(pd.Series({pd.Timestamp(int(x["timestamp"]), unit="s", tz="UTC"): float(x["value"]) for x in fg}).sort_index())
    w5 = state_weights(f < 25, f > 75, idx)
    add("t5_fear_greed_kontraer_25_75", one(w5))
    fwd = btc.pct_change(30).shift(-30).reindex(f.index)
    buck = pd.cut(f, [0, 25, 45, 55, 75, 100], labels=["extreme_fear", "fear", "neutral", "greed", "extreme_greed"])
    res["t5_fear_greed_kontraer_25_75"]["fwd30_median_pct_je_zustand"] = {str(k): round(float(v) * 100, 1) for k, v in fwd.groupby(buck, observed=True).median().items()}
    # 6 Makro: Dollar-Index unter 100-Tage-Schnitt => long (Wert Vortag)
    dx = fred("DTWEXBGS")
    w6 = (dx < dx.rolling(100).mean()).astype(float).shift(1).reindex(idx).ffill()
    add("t6_dollar_schwach_dxy_sma100", one(w6))
    # 7 Netto-Liquiditaet Fed (WALCL - RRP - TGA), 13-Wochen-Aenderung > 0, eine Woche Publikationsverzug
    wl = fred("WALCL"); tg = fred("WTREGEN"); rr = fred("RRPONTSYD").resample("W-WED").last()
    nl = (wl - tg.reindex(wl.index) - rr.reindex(wl.index).ffill().fillna(0) * 1000).dropna()
    w7 = (nl.diff(13) > 0).astype(float).shift(1)
    w7.index = w7.index + pd.Timedelta(days=1)
    add("t7_netto_liquiditaet_13w", one(w7.reindex(idx, method="ffill").fillna(0.0)))
    # 8 ETH/BTC-Rotation: ETH wenn ETH/BTC > SMA50, sonst BTC (immer investiert)
    ratio = eth / btc
    e = (ratio > ratio.rolling(50).mean()).reindex(idx)
    w8 = pd.DataFrame({"BTC": (~e).astype(float), "ETH": e.astype(float)})
    w8.iloc[:50] = 0.0
    r8b = pd.DataFrame({"BTC": 0.5, "ETH": 0.5}, index=idx)
    add("t8_ethbtc_rotation_sma50", w8)
    res["t8_ethbtc_rotation_sma50"]["vergleich_5050_taeglich_rebalanciert"] = stats(run(r8b, rets, rf), rf)
    # 9 Dual Momentum: staerkeres von BTC/ETH ueber 90 Tage, nur wenn > T-Bill-Rendite, sonst Cash; Pruefung woechentlich (Montag)
    m90 = px.pct_change(90)
    rf90 = (1 + rf).rolling(90).apply(np.prod, raw=True) - 1
    best = m90.fillna(-9.0).idxmax(axis=1)
    ok = m90.max(axis=1) > rf90
    w9 = pd.DataFrame(0.0, index=idx, columns=["BTC", "ETH"])
    for t in idx:
        if ok[t] and isinstance(best[t], str):
            w9.loc[t, best[t]] = 1.0
    w9[idx.dayofweek != 0] = np.nan
    w9 = w9.ffill().fillna(0.0)
    add("t9_dual_momentum_90d_woechentlich", w9)
    # 10 Inverse Volatilitaet BTC/ETH, 60 Tage, monatliches Rebalancing, voll investiert
    vol = rets.rolling(60).std()
    iv = (1 / vol).div((1 / vol).sum(axis=1), axis=0)
    iv[~idx.is_month_start] = np.nan
    iv = iv.ffill().fillna(0.0)
    m5050 = pd.DataFrame({"BTC": 0.5, "ETH": 0.5}, index=idx)
    m5050[~idx.is_month_start] = np.nan
    m5050 = m5050.ffill().fillna(0.0)
    add("t10_inverse_vol_btc_eth_monatlich", iv)
    res["t10_inverse_vol_btc_eth_monatlich"]["vergleich_5050_monatlich"] = stats(run(m5050, rets, rf), rf)

    res["trials"] = trials
    res["anzahl_informelle_trials"] = len(trials)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(res, open(OUT, "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
