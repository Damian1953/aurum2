"""Synthetische Tests fuer DT P&L v1.0 (keine Marktdaten): Exit von Hand, Zeitstopp, Kosten, Eine-Position-Regel,
Ersatzniveaus der Kontrollen, Look-ahead-Stoerung und ein End-to-End-Lauf von evaluate() auf Zufallsdaten."""
import os, sys
import numpy as np, pandas as pd
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AR = os.environ.get("AURUM_ROOT") or os.path.join(REPO, "build", "root")
for d in ("pylib", "yamato", "rtc", "dt"):
    sys.path.insert(0, os.path.join(AR, d))
sys.path.insert(0, os.path.join(REPO, "01_forschung/11_delayed_trend/dt_pnl_v1.0"))
import rlib as R; import dtlib as D; import dt_pnl as L; import dt_pnl_run as RUN
Y = R.Y
K0 = dict(fee_in=0.0, fee_out=0.0, fee_out_cut=0.0, fric=0.0, slip_in=0.0, slip_sl=0.0)


def mk(o, h, l, c):
    t = pd.date_range("2021-01-01", periods=len(o), freq="4h", tz="UTC")
    return pd.DataFrame(dict(t=t, open=o, high=h, low=l, close=c, volume=np.ones(len(o))))


def flat(n=600, base=100.0):
    o = np.full(n, base); return o.copy(), o + 0.5, o - 0.5, o.copy()


def test_stop_at_entry_bar_and_gap():
    o, h, l, c = flat(); l[50] = 98.0; df = mk(o, h, l, c); atr_d = np.full(len(o), 1.0)
    tr = L.simulate_dt(50, 99.0, 40, df, atr_d, K0)
    assert tr["reason"] == "stop_init" and tr["x"] == 50 and np.isclose(tr["exit"], 99.0) and np.isclose(tr["r_net"], -1.0)
    o, h, l, c = flat(); o[51] = 97.0; l[51] = 96.5; h[51] = 97.2; c[51] = 97.0; df = mk(o, h, l, c)
    tr = L.simulate_dt(50, 99.0, 40, df, atr_d, K0)
    assert tr["reason"] == "stop_gap" and tr["x"] == 51 and np.isclose(tr["exit"], 97.0)


def test_chandelier_highest_close_ratchet():
    o, h, l, c = flat(); atr_d = np.full(len(o), 1.0)
    # Anstieg: Schluesse 101..110 an 51..60, Hochs je +5 (duerfen den Floor NICHT treiben), dann Ruecksetzer
    for i, b in enumerate(range(51, 61)):
        c[b] = 101.0 + i; o[b] = c[b] - 0.5; h[b] = c[b] + 5.0; l[b] = c[b] - 1.0
    o[61] = 109.0; h[61] = 109.5; l[61] = 106.9; c[61] = 107.5     # HC = 110 -> Floor 107.0, L 106.9 -> Ausstieg 107.0
    df = mk(o, h, l, c)
    tr = L.simulate_dt(50, 95.0, 40, df, atr_d, K0)
    assert tr["reason"] == "chandelier_d" and tr["x"] == 61 and np.isclose(tr["exit"], 107.0)
    # Floor sinkt nicht, wenn die Tages-ATR steigt
    atr2 = atr_d.copy(); atr2[61:] = 10.0
    tr2 = L.simulate_dt(50, 95.0, 40, df, atr2, K0)
    assert tr2["reason"] == "chandelier_d" and tr2["x"] == 61


def test_time_stop_t_plus_360_and_cut():
    o, h, l, c = flat(n=600); atr_d = np.full(len(o), 5.0)
    o[401] = 100.2; df = mk(o, h, l, c)
    tr = L.simulate_dt(50, 90.0, 40, df, atr_d, K0)     # t=40 -> Pruefung nach Schluss 400, Ausstieg Eroeffnung 401
    assert tr["reason"] == "time360" and tr["x"] == 401 and np.isclose(tr["exit"], 100.2)
    o, h, l, c = flat(n=300); df = mk(o, h, l, c)
    tr = L.simulate_dt(50, 90.0, 40, df, np.full(300, 5.0), K0)
    assert tr["reason"] == "cut" and tr["x"] == 299


def test_cost_formula_matches_rlib():
    o, h, l, c = flat(); l[51] = 98.0; df = mk(o, h, l, c); atr_d = np.full(len(o), 1.0)
    K = dict(fee_in=0.004, fee_out=0.004, fee_out_cut=0.004, fric=0.0002, slip_in=0.0005, slip_sl=0.001)
    tr = L.simulate_dt(50, 99.0, 40, df, atr_d, K)
    entry = 100.0 * 1.0005; ex = 99.0 * 0.999; fees = (entry + ex) * 0.0042
    assert np.isclose(tr["r_net"], (ex - entry - fees) / (entry - 99.0))
    Kt = dict(K, fee_out=0.008)
    tr2 = L.simulate_dt(50, 99.0, 40, df, atr_d, Kt)
    assert np.isclose(tr2["r_net"], (ex - entry - entry * 0.0042 - ex * 0.0082) / (entry - 99.0))


def test_one_position_per_cell():
    o, h, l, c = flat(); df = mk(o, h, l, c); atr_d = np.full(len(o), 5.0); atr4 = np.ones(len(o))
    ent = pd.DataFrame(dict(t=[40, 45, 300, 410], e=[50, 60, 310, 420], stop=[90.0, 90.0, 90.0, 90.0], struct_bar=[46, 56, 306, 416]))
    tr, lg = L.run_cell(ent, df, atr_d, K0, atr4)
    assert list(tr.e) == [50, 420] and list(tr.x) [:1] == [401] and list(lg.status) == ["traded", "in_position", "in_position", "traded"]


def test_substitute_levels_and_control_entry():
    rng = np.random.default_rng(3); n = 700
    c = 100 + np.cumsum(rng.normal(0, 1, n)); o = np.r_[c[0], c[:-1]]; h = np.maximum(o, c) + 0.5; l = np.minimum(o, c) - 0.5
    df = mk(o, h, l, c); f = R.features(df, R.cfg_alt()); lo, _ = Y.swings(df); atr4 = f["atr"].to_numpy()
    cb = 300; lref, P = L.substitute_levels(cb, df)
    assert np.isclose(lref, l[180:301].min()) and np.isclose(P, h[282:301].max())
    end, inv = L.ctx_end(cb, lref, df)
    exp = D.dt1(cb, lref, float(atr4[cb]), end, df, atr4, lo)
    got = L.control_entry(cb, "DT1", df, atr4, lo, D)
    assert got["status"] == exp["status"] or (exp["status"] == "entry" and got["status"] == "entry_below_stop")


def test_no_lookahead_perturbation():
    rng = np.random.default_rng(5); n = 900
    c = 100 + np.cumsum(rng.normal(0, 1.2, n)); o = np.r_[c[0], c[:-1]]; h = np.maximum(o, c) + 0.6; l = np.minimum(o, c) - 0.6
    df = mk(o, h, l, c); f = R.features(df, R.cfg_alt()); atr_d = f["atr_d"].to_numpy()
    T = 600; c2 = c.copy(); c2[T:] = c2[T:] * 1.3 + 5; o2 = o.copy(); o2[T:] = o2[T:] * 0.7; h2 = np.maximum(o2, c2) + 2; l2 = np.minimum(o2, c2) - 2
    h2[:T] = h[:T]; l2[:T] = l[:T]
    df2 = mk(o2, h2, l2, c2); f2 = R.features(df2, R.cfg_alt()); atr_d2 = f2["atr_d"].to_numpy()
    K = dict(fee_in=0.004, fee_out=0.004, fee_out_cut=0.004, fric=0.0002, slip_in=0.0005, slip_sl=0.001)
    checked = 0
    for e in range(200, 500, 7):
        stop = l[e - 1] - 1.0
        if o[e] <= stop: continue
        a = L.simulate_dt(e, stop, e - 10, df, atr_d, K)
        if a["x"] < T - 1:
            b = L.simulate_dt(e, stop, e - 10, df2, atr_d2, K); checked += 1
            assert a == b
    assert checked >= 5


def synth_coin(seed):
    rng = np.random.default_rng(seed); n = 2600
    ret = rng.normal(0, 0.012, n); ret[np.arange(n) % 300 < 25] -= 0.012          # wiederkehrende Selloffs
    c = 100 * np.exp(np.cumsum(ret)); o = np.r_[c[0], c[:-1]]
    h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.006, n))); l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.006, n)))
    t = pd.date_range("2019-01-01", periods=n, freq="4h", tz="UTC")
    return pd.DataFrame(dict(t=t, open=o, high=h, low=l, close=c, volume=rng.uniform(1, 2, n)))


def test_end_to_end_evaluate(tmp_path):
    data = {}
    for coin, seed in (("BTC", 11), ("XRP", 12), ("DOT", 13)):
        df = synth_coin(seed); C = R.cfg_btc_stufeA() if coin == "BTC" else R.cfg_alt()
        f = R.features(df, C); lo, hi = Y.swings(df)
        cy = R.candidates_y1_y3(df, f, lo, C); y2 = R.candidates_y2(df, f, lo, hi, C); c2 = y2[y2.y2] if len(y2) else y2
        ctx = D.contexts(cy, y2 if len(y2) else pd.DataFrame(columns=["t", "s2", "neck", "y2"]).astype({"y2": bool}), df, f)
        E = D.entries(ctx, df, f, lo, coin)
        pool = Y.control_pool(cy, c2, df, f); blk = np.array([R.block_of(x, coin) for x in df["t"]])
        data[coin] = dict(df=df, f=f, lo=lo, C=C, FZ=E, pool=pool, blk=blk, year=df.t.dt.year.to_numpy(), BLOCKS=[b for b in dict.fromkeys(blk) if b != "none"],
                          atr_d=f["atr_d"].to_numpy(), atr4=f["atr"].to_numpy())
    COSTS = L.costs(Y, None)
    res, holm, a7 = RUN.evaluate(data, str(tmp_path), COSTS, R, D, L, np.random.default_rng(1))
    assert set(holm) == {f"{c}_{s}x{f}" for c, s, f in RUN.PRIMARY + RUN.SECONDARY}
    assert "lane_a_closed" in a7 and a7["n_trades"] == sum(res[f"{c}_{s}x{f}"].get("signals", 0) for c, s, f in RUN.PRIMARY)
    ntr = 0
    for k, r in res.items():
        p = tmp_path / f"trades_{k}_K1.csv"
        if not r.get("signals"): continue
        tr = pd.read_csv(p); ntr += len(tr)
        assert (tr.e.iloc[1:].to_numpy() > tr.x.iloc[:-1].to_numpy()).all()     # eine Position je Zelle
        assert (tr.reason.isin(["stop_init", "stop_gap", "stop", "chandelier_d", "time360", "cut"])).all()
        cp = tmp_path / f"controls_{k}_K1.csv"
        if cp.exists():
            ct = pd.read_csv(cp); pool = set(data[k.split("_")[0]]["pool"].tolist())
            assert set(ct.ctrl_t.astype(int)) <= pool
    assert ntr > 0
