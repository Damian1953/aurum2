"""Development-Analyse DB-CONTEXT auf BTC, XRP, DOT (keine ETH/SOL-Daten). Nach bestaetigtem Double Bottom (Nackenlinienbruch t, Nackenlinie N, Boden L2):
Haeufigkeit und Timing von Retest, Higher Low, Konsolidierungsbreakout innerhalb 60 Kerzen, und ob danach ein neues 20-Tage-Hoch folgt (Kontextwert)."""
import sys, json, numpy as np, pandas as pd
sys.path.insert(0, "/home/claude/rtc"); import rlib as R; Y = R.Y
out = {}
for coin, path, cand, cfg in (("BTC", "/home/claude/yamato/data/BTCUSDT_4h_discovery.csv", "regress/candidates_y2_rlib.csv", R.cfg_btc_stufeA()),
                              ("XRP", "/home/claude/holdout/discovery/XRPUSDT_spot4h_discovery.csv", "count_XRP/candidates_y2.csv", R.cfg_alt()),
                              ("DOT", "/home/claude/holdout/discovery/DOTUSDT_spot4h_discovery.csv", "count_DOT/candidates_y2.csv", R.cfg_alt())):
    df = Y.load(path); f = R.features(df, cfg); lo, hi = Y.swings(df); h, l, c, o = (df[k].to_numpy() for k in ("high", "low", "close", "open")); atr = f.atr.to_numpy(); n = len(df)
    y2 = pd.read_csv(cand); y2 = y2[y2.y2]
    rows = []
    for _, r in y2.iterrows():
        t = int(r.t); N = float(r.neck); L2 = l[int(r.s2)]; a = atr[t]; pre_hi = h[max(0, t - 120): t].max()
        W = 60; seg = slice(t + 1, min(n, t + 1 + W))
        # Retest: erstes Tief <= N + 0.25 ATR innerhalb 60 Kerzen, Halten = Schluss der Retest-Kerze >= N - 0.5 ATR
        rt = None; hold = None
        for b in range(t + 1, min(n, t + 1 + W)):
            if l[b] <= N + 0.25 * a: rt = b; hold = bool(c[b] >= N - 0.5 * a); break
        # Higher Low: erstes bestaetigtes Swing Low s > t (bekannt ab s+3) mit L_s > L2
        hl = None; sw = lo[(lo > t) & (lo + 3 < n)]
        for s in sw:
            if s > t + W: break
            if l[s] > L2: hl = int(s); break
        # Konsolidierung/Breakout: Hoch der Kerzen t+1..t+18 (3 Tage), Breakout = erster Schluss darueber in t+19..t+60
        ch = h[t + 1: min(n, t + 19)].max() if t + 19 < n else np.nan; bo = None
        if np.isfinite(ch):
            for b in range(t + 19, min(n, t + 1 + W)):
                if c[b] > ch: bo = b; break
        # Kontextwert: neues 20-Tage-Hoch (ueber pre_hi) innerhalb 60 Tagen (360 Kerzen) nach t
        nh = None
        for b in range(t + 1, min(n, t + 361)):
            if c[b] > pre_hi: nh = b; break
        # Invalidierung: Schluss unter L2 innerhalb 60 Kerzen
        inv = None
        for b in range(t + 1, min(n, t + 1 + W)):
            if c[b] < L2: inv = b; break
        rows.append(dict(t=t, retest=rt is not None, retest_hold=hold, retest_bars=(rt - t) if rt else None, hl=hl is not None, hl_bars=(hl - t) if hl else None, hl_before_nh=(hl is not None and (nh is None or hl < nh)),
                         bo=bo is not None, bo_bars=(bo - t) if bo else None, new_high=nh is not None, nh_bars=(nh - t) if nh else None, invalid=inv is not None, inv_bars=(inv - t) if inv else None,
                         retest_then_nh=(rt is not None and hold and nh is not None and nh > rt), hl_then_nh=(hl is not None and nh is not None and nh > hl), bo_then_nh=(bo is not None and nh is not None and nh >= bo)))
    d = pd.DataFrame(rows); d.to_csv(f"dev_dbctx/dbctx_{coin}.csv", index=False)
    s = dict(n=int(len(d)), new_high_60d=round(float(d.new_high.mean()), 2), nh_bars_median=float(d.nh_bars.dropna().median()) if d.nh_bars.notna().any() else None,
             invalid_60=round(float(d.invalid.mean()), 2),
             retest=round(float(d.retest.mean()), 2), retest_hold=round(float(d.retest_hold.fillna(False).mean()), 2), retest_bars_median=float(d.retest_bars.dropna().median()) if d.retest_bars.notna().any() else None,
             retest_hold_then_nh=round(float(d.retest_then_nh.mean()), 2), nh_given_retest_hold=round(float(d[d.retest_hold == True].new_high.mean()), 2) if (d.retest_hold == True).any() else None,
             hl=round(float(d.hl.mean()), 2), hl_bars_median=float(d.hl_bars.dropna().median()) if d.hl_bars.notna().any() else None, hl_before_nh=round(float(d.hl_before_nh.mean()), 2), nh_given_hl=round(float(d[d.hl].new_high.mean()), 2) if d.hl.any() else None,
             bo=round(float(d.bo.mean()), 2), bo_bars_median=float(d.bo_bars.dropna().median()) if d.bo_bars.notna().any() else None, nh_given_bo=round(float(d[d.bo].new_high.mean()), 2) if d.bo.any() else None,
             nh_given_none=round(float(d[~d.retest & ~d.hl & ~d.bo].new_high.mean()), 2) if (~d.retest & ~d.hl & ~d.bo).any() else None, n_none=int((~d.retest & ~d.hl & ~d.bo).sum()))
    out[coin] = s; print(coin, json.dumps(s))
json.dump(out, open("dev_dbctx/dev_dbctx.json", "w"), indent=1)
