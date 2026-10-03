#!/usr/bin/env python3
"""Ideen-Scan v3, Screening S1-S3 (Spezifikation: 01_forschung/16_ideen_scan_v3/ideen_scan_v3_plan.md §4, vor dem Rechnen
committet in b1ac555). Nur Daten < 2024-01-01. Kein Holdout. Ausgabe: 01_forschung/16_ideen_scan_v3/screening_v3.json"""
import json, math, os
import numpy as np, pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.path.join(REPO, "data", "raw", "binance_full")
S2 = os.environ.get("SCAN2_RAW", "/workspace/aurum2/work/scan_v2/raw")
CUT = pd.Timestamp("2024-01-01", tz="UTC")
ALTS = ["ADA", "AVAX", "BNB", "DOT", "LINK", "LTC", "XRP"]
K1_RT = 2 * 0.0047


def px(sym):
    d = pd.read_csv(os.path.join(RAW, f"{sym}USDT_1d.csv"), usecols=["t", "close"])
    d["t"] = pd.to_datetime(d["t"], utc=True)
    d = d[d["t"] < CUT].set_index("t")["close"].astype(float)
    assert d.index.max() < CUT
    return d


def tstat(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    return float(x.mean() / (x.std(ddof=1) / math.sqrt(len(x)))) if len(x) > 2 else float("nan")


def halves(s):
    return {"bis2020": s[s.index < "2021-01-01"], "ab2021": s[s.index >= "2021-01-01"]}


def main():
    btc = px("BTC").pct_change()
    alts = pd.DataFrame({a: px(a).pct_change() for a in ALTS})
    alt_next = alts.shift(-1)                           # Rendite t+1, Zeile t
    sd60 = btc.rolling(60).std().shift(1)               # 60 Vortage, ohne Tag t
    sig = (btc > 2 * sd60) & alt_next.notna().any(axis=1)
    ew_next = alt_next.mean(axis=1)                     # ein Wert je Datum
    out = {"hinweis": "Screening Scan v3, informell, Daten < 2024, K1-Roundtrip 0.94 %", "trials": 3}
    # S1
    x = ew_next[sig].dropna(); net = x - K1_RT
    uncond = ew_next.dropna()
    s1 = dict(n_signale=int(len(x)), brutto_mittel_pct=round(x.mean() * 100, 3), netto_mittel_pct=round(net.mean() * 100, 3),
              t_brutto=round(tstat(x), 2), unbedingt_mittel_pct=round(uncond.mean() * 100, 3), median_brutto_pct=round(x.median() * 100, 3),
              haelften={k: dict(n=int(len(v)), brutto_mittel_pct=round(v.mean() * 100, 3), t=round(tstat(v), 2)) for k, v in halves(x).items()},
              je_coin={a: dict(n=int(alt_next.loc[sig, a].notna().sum()), brutto_mittel_pct=round(alt_next.loc[sig, a].mean() * 100, 3))
                       for a in ALTS})
    out["S1_btc_schock_alt_folgetag"] = s1
    # S2: r_alt,t+1 = a + b r_btc,t + c r_alt,t (Datums-Mittel)
    ew_now = alts.mean(axis=1)
    df = pd.DataFrame({"y": ew_next, "b": btc, "c": ew_now}).dropna()
    def ols(d):
        X = np.column_stack([np.ones(len(d)), d["b"], d["c"]]); y = d["y"].values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None); e = y - X @ beta
        # HC1-robuste Standardfehler
        XtXi = np.linalg.inv(X.T @ X); S = (X * e[:, None]).T @ (X * e[:, None]) * len(d) / (len(d) - 3)
        se = np.sqrt(np.diag(XtXi @ S @ XtXi))
        return dict(n=int(len(d)), b=round(beta[1], 4), t_b=round(beta[1] / se[1], 2), c=round(beta[2], 4), t_c=round(beta[2] / se[2], 2))
    out["S2_regression_leadlag"] = dict(gesamt=ols(df), **{k: ols(v) for k, v in halves(df).items()})
    # S3: Halving-Fenster (CoinMetrics PriceUSD 2014-2023), MVRV-Zustand Regel B
    cm = pd.DataFrame(json.load(open(os.path.join(S2, "cm_btc_PriceUSD.json")))["data"])
    cm["t"] = pd.to_datetime(cm["time"], utc=True); p = cm.set_index("t")["PriceUSD"].astype(float)
    mv = pd.DataFrame(json.load(open(os.path.join(S2, "cm_btc_CapMVRVCur.json")))["data"])
    mv["t"] = pd.to_datetime(mv["time"], utc=True); m = mv.set_index("t")["CapMVRVCur"].astype(float)
    p = p[(p.index >= "2014-01-01") & (p.index < CUT)]; m = m[m.index < CUT]
    lr = np.log(p).diff().dropna()
    win = pd.Series(False, index=lr.index)
    for h in ["2016-07-09", "2020-05-11"]:
        h = pd.Timestamp(h, tz="UTC"); win |= (lr.index > h) & (lr.index <= h + pd.Timedelta(days=540))
    state, st = [], "INVESTIERT" if m.iloc[0] <= 3.5 else "CASH"
    for v in m.shift(1).values:  # Regel B mit 1 Tag Lag
        if np.isfinite(v):
            if st == "INVESTIERT" and v > 3.5: st = "CASH"
            elif st == "CASH" and v < 1.0: st = "INVESTIERT"
        state.append(st)
    inv = pd.Series(state, index=m.index).reindex(lr.index).ffill() == "INVESTIERT"
    out["S3_halving_deskriptiv"] = dict(
        tage_fenster=int(win.sum()), tage_rest=int((~win).sum()),
        log_rendite_tag_fenster_pct=round(lr[win].mean() * 100, 3), log_rendite_tag_rest_pct=round(lr[~win].mean() * 100, 3),
        annualisiert_fenster_pct=round((math.exp(lr[win].mean() * 365) - 1) * 100, 1), annualisiert_rest_pct=round((math.exp(lr[~win].mean() * 365) - 1) * 100, 1),
        t_differenz_welch=round(float((lr[win].mean() - lr[~win].mean()) / math.sqrt(lr[win].var() / win.sum() + lr[~win].var() / (~win).sum())), 2),
        anteil_mvrv_investiert_fenster=round(float(inv[win].mean()), 3), anteil_mvrv_investiert_rest=round(float(inv[~win].mean()), 3),
        je_halving={h: round(float(lr[(lr.index > pd.Timestamp(h, tz='UTC')) & (lr.index <= pd.Timestamp(h, tz='UTC') + pd.Timedelta(days=540))].sum()), 3)
                    for h in ["2016-07-09", "2020-05-11"]},
        vorbehalt="N = 2 Zyklen, autokorrelierte Tagesrenditen; t-Wert nicht interpretierbar")
    path = os.path.join(REPO, "01_forschung", "16_ideen_scan_v3", "screening_v3.json")
    json.dump(out, open(path, "w"), indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
