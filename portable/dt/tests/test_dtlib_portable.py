# PORTABLE VERSION, generiert von tools/make_portable.py. NICHT VON HAND AENDERN.
# Quelle (eingefroren): 01_forschung/11_delayed_trend/dtlib/tests/test_dtlib.py  sha256 105fdb3578a1ffff4dcf3c834a058e3f7082de31ab0f118599ae5ac9eda328f8
# Regeln: paths. Arbeitsbereich: AURUM_ROOT (Default: Ordner '../..' relativ zu dieser Datei).
import os as _aos; _AR = _aos.environ.get("AURUM_ROOT") or _aos.path.abspath(_aos.path.join(_aos.path.dirname(_aos.path.abspath(__file__)), "../.."))
"""Tests dtlib v1.0: Handrechnung DT1/DT2/DT3 auf konstruierten Pfaden, Invalidierung, Look-ahead. Keine Marktdaten."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, _AR + "/dt"); sys.path.insert(0, _AR + "/rtc"); import dtlib as D; import rlib as R; Y = R.Y


def flat(n=400, base=100.0):
    o = np.full(n, base); h = o + 0.5; l = o - 0.5; c = o.copy()
    return o, h, l, c


def mk(o, h, l, c):
    t = pd.date_range("2021-01-01", periods=len(o), freq="4h", tz="UTC")
    df = pd.DataFrame(dict(t=t, open=o, high=h, low=l, close=c, volume=np.ones(len(o))))
    C = R.cfg_alt(); f = R.features(df, C); return df, f


def test_dt1_hand_and_confirmation_timing():
    o, h, l, c = flat(); atr_t = 1.0
    # Kontext t=200, l_ref=90. Anstieg: Hoch 105 bei 210..214, Swing Low bei s=220 mit L=101 (>= 90+0.5), Tiefs davor/danach hoeher
    h[210:215] = 105.0; l[217:224] = 102.0; l[220] = 101.0
    df, f = mk(o, h, l, c); lo, hi = Y.swings(df); atr = np.full(len(o), atr_t)
    d = D.dt1(200, 90.0, atr_t, 380, df, atr, lo)
    assert d["status"] == "entry" and d["struct_bar"] == 220 and d["e"] == 224 and np.isclose(d["stop"], 101.0 - 0.5 * atr_t)
    # Rise-Bedingung: ohne Hoch >= L_s + 1 ATR kein Einstieg
    o2, h2, l2, c2 = flat(); l2[217:224] = 102.0; l2[220] = 101.0; df2, _ = mk(o2, h2, l2, c2); lo2, _ = Y.swings(df2)
    assert D.dt1(200, 90.0, atr_t, 380, df2, atr, lo2)["status"] == "no_higher_low"
    # Swing Low unter l_ref + 0.5 ATR wird uebersprungen
    assert D.dt1(200, 100.8, atr_t, 380, df, atr, lo)["status"] == "no_higher_low"
    # Fenster: e = s+4 muss <= end_bar sein
    assert D.dt1(200, 90.0, atr_t, 223, df, atr, lo)["status"] == "window_or_invalidated"


def test_dt2_hand_hold_and_fail():
    o, h, l, c = flat(base=101.0); P_ = 100.0; atr_t = 1.0; atr = np.full(len(o), atr_t)   # Basis ueber P + 0.25: flache Kerzen sind kein Retest
    # t=100. Retest bei b=110: L=100.1 (<= 100.25), C=100.0 (>= 99.5). Hold b+1: C=100.3 > P. e=112, Stop=min(L110,L111)-0.5
    l[110] = 100.1; c[110] = 100.0; c[111] = 100.3; l[111] = 100.2
    df, f = mk(o, h, l, c)
    d = D.dt2(100, P_, atr_t, 300, df, atr)
    assert d["status"] == "entry" and d["struct_bar"] == 110 and d["e"] == 112 and np.isclose(d["stop"], 100.1 - 0.5) and d["failed_holds"] == 0
    # Hold scheitert (C_{111} = 100.0 <= P), zweiter Retest bei 120 mit Hold
    o, h, l, c = flat(base=101.0); l[110] = 100.1; c[110] = 100.0; c[111] = 100.0; l[111] = 100.3; l[120] = 100.2; c[120] = 100.1; c[121] = 100.4
    df, _ = mk(o, h, l, c); d = D.dt2(100, P_, atr_t, 300, df, atr)
    assert d["status"] == "entry" and d["struct_bar"] == 120 and d["e"] == 122
    # Gescheiterter Retest (C < P - 0.5 ATR) beendet die Familie, auch wenn spaeter ein Hold kaeme
    o, h, l, c = flat(base=101.0); l[110] = 99.0; c[110] = 99.2; l[120] = 100.2; c[120] = 100.1; c[121] = 100.4
    df, _ = mk(o, h, l, c); d = D.dt2(100, P_, atr_t, 300, df, atr); assert d["status"] == "retest_failed" and d["detail"] == 110
    # Vor t+3 kein Retest
    o, h, l, c = flat(base=101.0); l[101] = 100.1; c[101] = 100.0; c[102] = 100.3
    df, _ = mk(o, h, l, c); assert D.dt2(100, P_, atr_t, 300, df, atr)["status"] == "no_retest_hold"


def test_dt3_hand_box_and_breakout():
    o, h, l, c = flat(); atr_t = 1.0; atr = np.full(len(o), atr_t); t = 50
    # Box t+1..t+18: h 100.5, l 99.5, Breite 1.0 <= 3.0; l_ref 95. Breakout: Schluss 101 bei b=80
    c[80] = 101.0; h[80] = 101.2
    df, _ = mk(o, h, l, c); d = D.dt3(t, 95.0, atr_t, 300, df, atr)
    assert d["status"] == "entry" and d["struct_bar"] == 80 and d["e"] == 81 and np.isclose(d["stop"], 99.5 - 0.5) and np.isclose(d["box_high"], 100.5)
    # Hoch ueber Boxhoch ohne Schluss darueber ist kein Breakout
    o, h, l, c = flat(); h[80] = 102.0; df, _ = mk(o, h, l, c); assert D.dt3(t, 95.0, atr_t, 300, df, atr)["status"] == "no_breakout"
    # Box zu breit
    o, h, l, c = flat(); h[60] = 104.0; c[80] = 105.0; df, _ = mk(o, h, l, c); assert D.dt3(t, 95.0, atr_t, 300, df, atr)["status"] == "no_consolidation"
    # Breakout innerhalb der Box (b < t+19) zaehlt nicht: Schluss bei 60 ueber 100.5 erhoeht nur das Boxhoch
    o, h, l, c = flat(); c[60] = 101.0; h[60] = 101.0; df, _ = mk(o, h, l, c); d = D.dt3(t, 95.0, atr_t, 300, df, atr); assert d["status"] == "no_breakout" and np.isclose(d["box_width_atr"], 1.5)


def test_contexts_invalidation_and_geometry():
    o, h, l, c = flat(); c[230] = 89.0; l[230] = 88.5   # Invalidierung bei 230 fuer l_ref 90
    h[60:120] = 110.0   # pre-selloff high fuer ref=200: max(H, 80..199) = 110
    df, f = mk(o, h, l, c)
    cy = pd.DataFrame(dict(t=[200], y1=[True], tb_lvl_y1=[100.0])); y2 = pd.DataFrame(columns=["t", "s2", "neck", "y2"])
    l[200] = 90.0; df, f = mk(o, h, l, c)
    ctx = D.contexts(cy, y2, df, f); r = ctx.iloc[0]
    assert r.src == "S2" and r.inv_bar == 230 and r.end_bar == 230 and np.isclose(r.h_pre, 110.0) and np.isclose(r.l_ref, 90.0)
    g = D.geometry(100.0, 98.0, 110.0, 1.0)
    assert np.isclose(g["stop_pct"], 2.0) and np.isclose(g["cost_R_K1"], 99 / 200) and np.isclose(g["rr_geo_gross"], 5.0) and np.isclose(g["rr_geo_net_K1"], (10 - 0.89) / (2 + 0.99))
    assert D.geometry(100.0, 98.0, 99.0, 1.0)["target_below_entry"] and D.geometry(100.0, 98.0, 99.0, 1.0)["rr_geo_gross"] == 0.0


def test_lookahead():
    rng = np.random.default_rng(7); n = 3000
    r = rng.normal(0, 0.01, n); c = 100 * np.exp(np.cumsum(r)); o = np.concatenate([[100], c[:-1]]); h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.004, n))); l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.004, n)))
    df, f = mk(o, h, l, c); lo, hi = Y.swings(df)
    cy = pd.DataFrame(dict(t=list(range(300, 2400, 150)), y1=True, tb_lvl_y1=[l[t] * 1.01 for t in range(300, 2400, 150)]))
    y2 = pd.DataFrame(dict(t=[900, 1800], s1=[850, 1750], s2=[880, 1780], neck=[h[880] * 1.02, h[1780] * 1.02], y2=[True, True]))
    ctx = D.contexts(cy, y2, df, f); E = D.entries(ctx, df, f, lo, "SYN")
    T = 1500; o2, h2, l2, c2 = o.copy(), h.copy(), l.copy(), c.copy(); c2[T:] *= rng.uniform(0.8, 1.2, n - T); h2[T:] = np.maximum(o2[T:], c2[T:]) * 1.01; l2[T:] = np.minimum(o2[T:], c2[T:]) * 0.99
    df2, f2 = mk(o2, h2, l2, c2); lo2, _ = Y.swings(df2); ctx2 = D.contexts(cy, y2, df2, f2); E2 = D.entries(ctx2, df2, f2, lo2, "SYN")
    a = E[(E.status == "entry") & (E.e < T - 4)].reset_index(drop=True); b = E2[(E2.status == "entry") & (E2.e < T - 4)].reset_index(drop=True)
    # Kontexte, deren Fenster T erreicht, koennen sich in end_bar/inv_bar unterscheiden, Einstiege vor T-4 nicht
    m = a.merge(b, on=["src", "t", "fam"], suffixes=("_a", "_b")); assert len(m) == len(a) == len(b), (len(a), len(b), len(m))
    for col in ("e", "stop", "entry", "rr_geo_gross", "stop_atr"):
        assert np.allclose(np.nan_to_num(m[f"{col}_a"].astype(float), nan=-9), np.nan_to_num(m[f"{col}_b"].astype(float), nan=-9)), col
    assert len(a) > 0


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
