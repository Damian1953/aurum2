#!/usr/bin/env python3
"""Unabhaengige Nachpruefung des DT-P&L-Laufs v1.0 (Spec 01_forschung/11_delayed_trend/dt_pnl_spec_v1.0.md §10).
Eigene Implementierung von ATR, Tages-ATR, Exit, Kosten, Kontroll-Pool, Matching-Toleranzen und Ersatzniveaus aus den Rohkerzen;
importiert rlib/dtlib/dt_pnl NICHT, ausser fuer den Stoerungstest (Teil G), der die Lauf-Library auf gestoerten echten Daten prueft.
Schreibt run/dt_pnl_check.json."""
import os, sys, json, hashlib
import numpy as np, pandas as pd
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AR = os.environ.get("AURUM_ROOT") or os.path.join(REPO, "build", "root")
RUN = os.path.join(REPO, "01_forschung/11_delayed_trend/dt_pnl_v1.0/run")
CELLS = [("BTC", "S2", "DT1"), ("XRP", "S2", "DT1"), ("XRP", "S2", "DT2"), ("BTC", "S2", "DT2"), ("DOT", "S2", "DT1"), ("DOT", "S2", "DT2")] + [(c, "S1", f) for c in ("BTC", "XRP", "DOT") for f in ("DT1", "DT2")]
CNT = {"BTC": "count_BTC_B", "XRP": "count_XRP", "DOT": "count_DOT"}


def wilder(h, l, c, n=14):
    tr = np.r_[h[0] - l[0], np.maximum.reduce([h[1:] - l[1:], np.abs(h[1:] - c[:-1]), np.abs(l[1:] - c[:-1])])]
    a = np.full(len(h), np.nan); a[n - 1] = tr[:n].mean()
    for i in range(n, len(h)): a[i] = (a[i - 1] * (n - 1) + tr[i]) / n
    return a


def ema(x, n=50):
    out = np.full(len(x), np.nan); a = 2 / (n + 1); out[n - 1] = x[:n].mean()
    for i in range(n, len(x)): out[i] = a * x[i] + (1 - a) * out[i - 1]
    return out


def costs():
    m = json.load(open(os.path.join(REPO, "config/cost_model_v1.json")))["sections"]; s = m["spot_r"]["values"]; v = m["venue_kraken"]["values"]["spot_long_scenarios"]
    out = {k: dict(fi=s[k]["fee"], fo=s[k]["fee"], fc=s[k]["fee"], fr=s[k]["fric"], si=s[k]["slip_in"], ss=s[k]["slip_sl"]) for k in ("K0", "K1", "K2")}
    out["kraken_maker_plan"] = dict(fi=v["maker_plan"]["fee"], fo=v["maker_plan"]["fee"], fc=v["maker_plan"]["fee"], fr=v["maker_plan"]["fric"], si=v["maker_plan"]["slip_in"], ss=v["maker_plan"]["slip_sl"])
    out["kraken_taker_K2"] = dict(fi=v["taker_K2"]["fee"], fo=v["taker_K2"]["fee"], fc=v["taker_K2"]["fee"], fr=v["taker_K2"]["fric"], si=v["taker_K2"]["slip_in"], ss=v["taker_K2"]["slip_sl"])
    d = v["maker_entry_taker_stop"]; out["kraken_maker_entry_taker_stop"] = dict(fi=d["fee_entry"], fo=d["fee_exit_stop"], fc=d["fee_exit_target"], fr=d["fric"], si=d["slip_in"], ss=d["slip_sl"])
    return out


def sim(e, stop0, t, o, h, l, c, atrd, K):
    n = len(o); entry = o[e] * (1 + K["si"])
    if l[e] <= stop0:
        x, px, rs = e, (min(o[e], stop0)) * (1 - K["ss"]), "stop_init"
    else:
        hc = c[e]; fl = hc - 3 * atrd[e] if np.isfinite(atrd[e]) else -np.inf; b = e; x = None
        while x is None:
            b += 1
            if b >= n: x, px, rs = n - 1, c[n - 1] * (1 - K["si"]), "cut"; break
            S = max(stop0, fl)
            if o[b] <= S: x, px, rs = b, o[b] * (1 - K["ss"]), "stop_gap"; break
            if l[b] <= S: x, px, rs = b, S * (1 - K["ss"]), ("stop" if S == stop0 else "chandelier_d"); break
            hc = max(hc, c[b])                                     # nur abgeschlossene Kerze b
            if np.isfinite(atrd[b]): fl = max(fl, hc - 3 * atrd[b])
            if b >= t + 360:
                x, px, rs = (b + 1, o[b + 1] * (1 - K["si"]), "time360") if b + 1 < n else (b, c[b] * (1 - K["si"]), "cut"); break
    fo = K["fc"] if rs == "cut" else K["fo"]
    r = (px - entry - entry * (K["fi"] + K["fr"]) - px * (fo + K["fr"])) / (entry - stop0)
    return x, px, rs, r


def main():
    out = {}; ok = True
    log = json.load(open(os.path.join(RUN, "dt_pnl_run.log"))); ev = json.load(open(os.path.join(RUN, "dt_pnl_eval.json")))
    spec_sha = hashlib.sha256(open(os.path.join(REPO, "01_forschung/11_delayed_trend/dt_pnl_spec_v1.0.md"), "rb").read()).hexdigest()
    out["A_spec_sha_im_log"] = log["spec_sha256"] == spec_sha; ok &= out["A_spec_sha_im_log"]
    COST = costs(); detail = {}
    for coin in ("BTC", "XRP", "DOT"):
        sp = os.path.join(AR, "holdout/discovery", f"{coin}USDT_spot4h_discovery.csv"); assert "validation" not in sp
        df = pd.read_csv(sp); df["t"] = pd.to_datetime(df["t"], utc=True)
        o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close")); n = len(df)
        last_ok = df.t.iat[-1] <= pd.Timestamp("2023-12-31 20:00", tz="UTC")
        day = df.t.dt.floor("D"); g = df.groupby(day).agg(h=("high", "max"), l=("low", "min"), c=("close", "last"))
        atrd = pd.Series(wilder(g.h.to_numpy(), g.l.to_numpy(), g.c.to_numpy()), index=g.index).shift(1).reindex(day).to_numpy()
        atr = wilder(h, l, c); atrp = np.r_[np.nan, atr[:-1]]
        hh120 = np.array([h[t - 120:t].max() if t >= 120 else np.nan for t in range(n)])
        dd = c / hh120 - 1; dda = (c - hh120) / atrp; ext = (c - ema(c)) / atrp
        cy = pd.read_csv(os.path.join(AR, "rtc", CNT[coin], "candidates_y1_y3.csv")); y2 = pd.read_csv(os.path.join(AR, "rtc", CNT[coin], "candidates_y2.csv")); y2v = y2[y2.y2]
        excl = set(y2v.t.astype(int)) | {s for s2 in y2v.s2.astype(int) for s in range(s2 - 3, s2 + 4)}
        pool = set(int(t) for t in cy[cy.ctx & ~cy.fb_any & ~cy.y3_any].t if int(t) not in excl)
        FZ = pd.read_csv(os.path.join(REPO, "01_forschung/11_delayed_trend/out", f"{coin}_entries.csv"))
        for (cc, src, fam) in [x for x in CELLS if x[0] == coin]:
            key = f"{coin}_{src}x{fam}"; p = os.path.join(RUN, f"trades_{key}_K1.csv"); dct = dict(last_bar_ok=bool(last_ok))
            if not os.path.exists(p): detail[key] = dict(dct, trades=0); continue
            tr = pd.read_csv(p); ent = FZ[(FZ.src == src) & (FZ.fam == fam) & (FZ.status == "entry")]
            # B Einstieg = eingefrorene Messung, Entscheidungskerzen vor e (nur abgeschlossene Kerzen)
            m_ok = all(bool(((ent.e == r.e) & (ent.t == r.t) & np.isclose(ent.stop, r.stop0)).any()) for _, r in tr.iterrows())
            la = all((r.e == r.struct_bar + 4) if fam == "DT1" else (r.e == r.struct_bar + 2) for _, r in tr.iterrows()) and bool((tr.t < tr.e).all())
            onepos = bool((tr.e.iloc[1:].to_numpy() > tr.x.iloc[:-1].to_numpy()).all())
            # C Exit und Kosten unabhaengig
            mx = 0.0; same_x = True
            for _, r in tr.iterrows():
                x, px, rs, rn = sim(int(r.e), float(r.stop0), int(r.t), o, h, l, c, atrd, COST["K1"])
                same_x &= (x == r.x and rs == r.reason); mx = max(mx, abs(rn - r.r_net))
            cmx = {}
            for cn in COST:
                q = os.path.join(RUN, f"trades_{key}_{cn}.csv") if cn != "K1" else p
                t2 = pd.read_csv(q); cmx[cn] = float(max(abs(sim(int(r.e), float(r.stop0), int(r.t), o, h, l, c, atrd, COST[cn])[3] - r.r_net) for _, r in t2.iterrows()))
            dct.update(trades=int(len(tr)), entries_match_frozen=bool(m_ok), decision_bars_before_entry=bool(la), one_position=bool(onepos), exit_bar_reason_equal=bool(same_x), r_net_K1_maxabw=mx, cost_scen_maxabw=cmx)
            ok &= m_ok and la and onepos and same_x and mx < 1e-9 and all(v < 1e-9 for v in cmx.values()) and last_ok
            # D Kontrollen
            cp = os.path.join(RUN, f"controls_{key}_K1.csv")
            if os.path.exists(cp):
                ct = pd.read_csv(cp); pos = list(zip(tr.e, tr.x)); bad = 0; lv_bad = 0
                tol_key, tol = (dd, 0.03) if coin == "BTC" else (dda, 1.5)
                for _, r in ct.iterrows():
                    cb, st = int(r.ctrl_t), int(r.sig_t)
                    good = cb in pool and 12 < abs(cb - st) <= 540 and abs(tol_key[cb] - tol_key[st]) <= tol + 1e-12 and abs(ext[cb] - ext[st]) <= 0.5 + 1e-12 and not any(e <= cb <= x for e, x in pos)
                    bad += not good
                    lv_bad += not (np.isclose(r.l_ref, l[max(0, cb - 120): cb + 1].min()) and np.isclose(r.P, h[max(0, cb - 18): cb + 1].max()))
                tc = ct[ct.status == "traded"]; cmax = 0.0; cx = True
                for _, r in tc.iterrows():
                    x, px, rs, rn = sim(int(r.e), float(r.stop0), int(r.ctrl_t), o, h, l, c, atrd, COST["K1"]); cmax = max(cmax, abs(rn - r.r_net)); cx &= (x == r.x)
                # gepaarte Differenz neu
                pr = os.path.join(RUN, f"pairs_{key}.csv"); pmx = None
                if os.path.exists(pr):
                    pa = pd.read_csv(pr); sg = tr.set_index("t").r_net; cm = tc.groupby("sig_t").r_net.mean()
                    pmx = float(max(abs(sg[int(r.t)] - cm[int(r.t)] - r.d_r) for _, r in pa.iterrows())) if len(pa) else 0.0
                dct.update(controls=int(len(ct)), controls_traded=int(len(tc)), control_match_violations=int(bad), substitute_level_violations=int(lv_bad), control_r_net_maxabw=cmax, control_exit_equal=bool(cx), pairs_d_r_maxabw=pmx)
                ok &= bad == 0 and lv_bad == 0 and cmax < 1e-9 and cx and (pmx is None or pmx < 1e-9)
            detail[key] = dct
    out["cells"] = detail
    # E Holm und A7 neu
    hv = {k: v for k, v in ev["holm"].items() if v.get("p") is not None}; ordr = sorted(hv, key=lambda k: hv[k]["p"]); prev = 0; hb = 0
    for i, k in enumerate(ordr):
        adj = min(1.0, max(prev, hv[k]["p"] * (len(ordr) - i))); prev = adj; hb += abs(round(adj, 4) - hv[k]["p_holm"]) > 1e-9
    out["E_holm_neu_abweichungen"] = int(hb); ok &= hb == 0
    s = 0.0; nn = 0
    for c_, s_, f_ in CELLS[:3]:
        p = os.path.join(RUN, f"trades_{c_}_{s_}x{f_}_K1.csv")
        if os.path.exists(p): t_ = pd.read_csv(p); s += t_.r_net.sum(); nn += len(t_)
    out["F_a7_summe_neu"] = round(s, 4); out["F_a7_gleich"] = bool(abs(round(s, 4) - ev["a7"]["sum_r_net_K1"]) < 1e-9 and nn == ev["a7"]["n_trades"] and (s < 0) == ev["a7"]["lane_a_closed"]); ok &= out["F_a7_gleich"]
    # G Stoerungstest auf echten Daten (Lauf-Library): Trades mit Ausstieg vor T unveraendert
    for d in ("pylib", "yamato", "rtc", "dt"): sys.path.insert(0, os.path.join(AR, d))
    sys.path.insert(0, os.path.join(REPO, "01_forschung/11_delayed_trend/dt_pnl_v1.0"))
    import rlib as R; import dt_pnl as L; Y = R.Y
    T0 = pd.Timestamp("2022-07-01", tz="UTC"); gt = {}
    for coin in ("BTC", "XRP", "DOT"):
        df = Y.load(os.path.join(AR, "holdout/discovery", f"{coin}USDT_spot4h_discovery.csv")); C = R.cfg_btc_stufeA() if coin == "BTC" else R.cfg_alt()
        T = int((df.t >= T0).idxmax()); d2 = df.copy()
        for k in ("open", "high", "low", "close"): d2.loc[T:, k] = d2.loc[T:, k] * 1.37
        f1 = R.features(df, C); f2 = R.features(d2, C); K = {k: v for k, v in dict(fee_in=COST["K1"]["fi"], fee_out=COST["K1"]["fo"], fee_out_cut=COST["K1"]["fc"], fric=COST["K1"]["fr"], slip_in=COST["K1"]["si"], slip_sl=COST["K1"]["ss"]).items()}
        chk = 0; diff = 0
        for (cc, src, fam) in [x for x in CELLS if x[0] == coin]:
            p = os.path.join(RUN, f"trades_{coin}_{src}x{fam}_K1.csv")
            if not os.path.exists(p): continue
            for _, r in pd.read_csv(p).iterrows():
                if r.x < T - 1:
                    a = L.simulate_dt(int(r.e), float(r.stop0), int(r.t), df, f1["atr_d"].to_numpy(), K); b = L.simulate_dt(int(r.e), float(r.stop0), int(r.t), d2, f2["atr_d"].to_numpy(), K); chk += 1; diff += a != b
        gt[coin] = dict(T=str(df.t.iat[T]), trades_checked=chk, changed=diff); ok &= diff == 0
    out["G_stoerungstest"] = gt
    out["gesamt_ok"] = bool(ok)
    json.dump(out, open(os.path.join(RUN, "dt_pnl_check.json"), "w"), indent=1, default=lambda x: bool(x) if isinstance(x, np.bool_) else (int(x) if isinstance(x, np.integer) else float(x)))
    print(json.dumps(out, indent=1, default=lambda x: bool(x) if isinstance(x, np.bool_) else (int(x) if isinstance(x, np.integer) else float(x))))


if __name__ == "__main__":
    main()
