import numpy as np, pandas as pd, sys
sys.path.insert(0, "/home/claude/yamato")
import ylib as Y

def mk(o, h, l, c, v=None):
    n = len(o); v = np.ones(n) * 100 if v is None else np.asarray(v, float)
    t = pd.date_range("2020-01-01", periods=n, freq="4h", tz="UTC")
    return pd.DataFrame(dict(t=t, open=o, high=h, low=l, close=c, volume=v))

def flat(n, p=100.0, rng=2.0):
    o = np.full(n, p); c = np.full(n, p); h = np.full(n, p + rng / 2); l = np.full(n, p - rng / 2)
    return o, h, l, c

def test_atr_ema():
    o, h, l, c = flat(50, 100, 2.0)
    df = mk(o, h, l, c); f = Y.features(df)
    assert abs(f.atr.iloc[-1] - 2.0) < 1e-9 and abs(f.ema50.iloc[-1] - 100) < 1e-9 or np.isnan(f.ema50.iloc[-1])
    # Wilder: TR const -> ATR const
    assert np.allclose(f.atr.iloc[14:], 2.0)

def test_swings_strict():
    n = 40; o, h, l, c = flat(n)
    l = l.copy(); l[20] = 90; l[30] = 90; l[31] = 90   # 30/31 tie -> no swing at 30 or 31
    df = mk(o, h, l, c); lows, highs = Y.swings(df)
    assert list(lows) == [20], lows

def test_levels_and_k3():
    n = 500; o, h, l, c = flat(n); l = l.copy()
    for s in (200, 230, 260):  # three touches near 90 -> zone
        l[s] = 90.0 + 0.1 * (s - 200) / 30
    df = mk(o, h, l, c); f = Y.features(df); lows, highs = Y.swings(df)
    sw, nb, zn = Y.levels_at(300, df, f, lows)
    assert abs(sw - l[260]) < 1e-9 and abs(nb - 90.0) < 1e-9 and zn is not None and 90 <= zn <= 90.2, (sw, nb, zn)
    # swing older than 240 bars is dropped
    sw2, _, zn2 = Y.levels_at(200 + 241 + 4, df, f, lows)
    assert sw2 is None or sw2 != l[200]

def test_failed_breakdown_and_y3():
    n = 300; o, h, l, c = flat(n); o, h, l, c = o.copy(), h.copy(), l.copy(), c.copy(); v = 100 + (np.arange(n) % 7)
    l[150] = 90.0                       # swing low at 150 -> level 90
    # candidate at t=200: low 89.5 (< 90*0.999), close 91, body small, wick large
    o[200], c[200], l[200], h[200] = 90.8, 91.0, 89.5, 91.2; v[200] = 400
    df = mk(o, h, l, c, v); f = Y.features(df); lows, highs = Y.swings(df)
    lv = Y.levels_at(200, df, f, lows)
    assert abs(lv[0] - 90.0) < 1e-9
    hit = Y.failed_breakdown(200, df, f, lv); assert "swing" in hit and "nbar" in hit, hit
    assert Y.y3_flag(200, f) is False  # lw_atr = 1.3/2 = 0.65 < 1.0
    l[200] = 88.0; df = mk(o, h, l, c, v); f = Y.features(df)
    assert Y.y3_flag(200, f) is True   # lw 2.8 / atr 2 = 1.4, cl = 3/3.2 > 0.6, volz large

def test_context_and_candidates():
    # selloff: price falls from 100 to 80 then candidate
    n = 400; p = np.concatenate([np.full(250, 100.0), np.linspace(100, 80, 100), np.full(50, 80.0)])
    o = p.copy(); c = p.copy(); h = p + 1; l = p - 1
    l[349] = 76.0; o[349] = 79.5; c[349] = 80.5; h[349] = 80.6          # wick candle at bottom
    v = 100 + (np.arange(n) % 7); v[349] = 500
    df = mk(o, h, l, c, v); f = Y.features(df); lows, highs = Y.swings(df)
    cy = Y.candidates_y1_y3(df, f, lows)
    r = cy[cy.t == 349].iloc[0]
    assert r.ctx and r.y3, r.to_dict()

def test_double_bottom():
    n = 500; p = np.full(n, 100.0)
    # selloff to 80, low1 at 300 (78), rally to 86 at 315 (neckline), low2 at 330 (78.5), break at 345
    p[250:300] = np.linspace(100, 80, 50); p[300] = 78.0; p[301:315] = np.linspace(80, 86, 14); p[315] = 86.5
    p[316:330] = np.linspace(85, 80, 14); p[330] = 78.5; p[331:345] = np.linspace(80, 86, 14); p[345:] = 88.0
    o = p.copy(); c = p.copy(); h = p + 0.5; l = p - 0.5
    df = mk(o, h, l, c); f = Y.features(df); lows, highs = Y.swings(df)
    y2 = Y.candidates_y2(df, f, lows, highs)
    assert len(y2) == 1 and y2.s1.iloc[0] == 300 and y2.s2.iloc[0] == 330 and y2.h1.iloc[0] == 315, y2
    assert y2.t.iloc[0] == 345, y2.t.iloc[0]

def test_trigger_and_sim():
    n = 60; o, h, l, c = flat(n); o, h, l, c = o.copy(), h.copy(), l.copy(), c.copy()
    h[10] = 101.0; c[11] = 101.5; h[11] = 101.6                          # TA at t=10 -> entry bar 12
    assert Y.trigger_ta(10, mk(o, h, l, c)) == 12
    c[11] = 100.5; assert Y.trigger_ta(10, mk(o, h, l, c)) is None
    # simulation: trend up then chandelier stop
    p = np.concatenate([np.full(20, 100.0), np.linspace(100, 120, 20), np.full(20, 120.0)])
    o = p.copy(); c = p.copy(); h = p + 0.5; l = p - 0.5; l[45] = 100.0   # deep drop at 45 hits chandelier
    df = mk(o, h, l, c); f = Y.features(df); lows, _ = Y.swings(df)
    tr = Y.simulate_trade(20, 95.0, df, f, lows, "K0")
    assert tr["reason"] in ("chandelier", "stop_gap") and tr["x"] == 45, tr
    # structure exit: swing low after entry then close below it
    p = np.concatenate([np.full(20, 100.0), np.linspace(100, 110, 10), [104.0], np.linspace(105, 112, 10), np.full(5, 112.0), [100.0], np.full(10, 100.0)])
    o = p.copy(); c = p.copy(); h = p + 3.0; l = p - 3.0
    df = mk(o, h, l, c); f = Y.features(df); lows, _ = Y.swings(df)
    tr = Y.simulate_trade(20, 90.0, df, f, lows, "K0")
    assert 30 in lows and tr["reason"] == "structure" and tr["x"] == 47, (lows, tr)

def test_match_controls():
    n = 1200; f = pd.DataFrame(dict(dd120=np.full(n, -0.15), ext=np.full(n, -2.5)))
    pool = np.arange(100, 1100, 5)
    sig = pd.DataFrame(dict(t=[600]))
    m = Y.match_controls(sig, pool, f, positions=[(602, 700)])
    ch = m.ctrls.iloc[0]
    assert len(ch) == 3 and all(abs(c - 600) > 12 for c in ch) and all(not (602 <= c <= 700) for c in ch), ch
    assert all(abs(a - b) > 12 for i, a in enumerate(ch) for b in ch[i + 1:])


def test_y2_no_cap_v11():
    # Y2 mit Entry-Stop > 3 ATR wird gehandelt, Y1 mit gleicher Distanz nicht
    n = 80; o, h, l, c = flat(n); o, h, l, c = o.copy(), h.copy(), l.copy(), c.copy()
    df = mk(o, h, l, c); f = Y.features(df); lows, _ = Y.swings(df)
    cand2 = pd.DataFrame(dict(t=[40], s2=[30])); l[30] = 90.0   # Stop 90-1=89, Entry 100 -> 11/2 ATR = 5.5 ATR
    df = mk(o, h, l, c); f = Y.features(df); lows, _ = Y.swings(df)
    tr2, lg2 = Y.run_sleeve(cand2, df, f, lows, "Y2")
    assert len(tr2) == 1 and tr2.stop_dist_atr.iloc[0] > 3, lg2
    cand1 = pd.DataFrame(dict(t=[30])); h[31] = 101.0; c[31] = 101.5   # TA
    df = mk(o, h, l, c); f = Y.features(df); lows, _ = Y.swings(df)
    tr1, lg1 = Y.run_sleeve(cand1, df, f, lows, "Y1")
    assert len(tr1) == 0 and lg1.status.iloc[0] == "stop_too_wide", lg1

if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
