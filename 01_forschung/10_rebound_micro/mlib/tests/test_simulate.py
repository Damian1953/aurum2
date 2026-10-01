"""Tests simulate_micro v1.0 auf synthetischen Pfaden (keine Marktdaten). Gebuehren und Slippage von Hand nachgerechnet."""
import sys, numpy as np
sys.path.insert(0, "/home/claude/micro"); import simulate_micro as S; import mlib as M
K1 = M.COST["K1"]; K0 = M.COST["K0"]


def path(n=40, base=100.0):
    o = np.full(n, base); h = np.full(n, base + 0.5); l = np.full(n, base - 0.5); c = np.full(n, base)
    return o, h, l, c


def test_target_exact_fill_and_fees():
    o, h, l, c = path(); e = 5; stop = 98.0; target = 103.0; h[9] = 103.2
    tr = S.simulate(o, h, l, c, e, stop, target, K1)
    assert tr["reason"] == "target" and tr["exit_b"] == 9 and tr["exit_px"] == 103.0
    entry = 100.0 * 1.0005; R = entry - 98.0; fees = (entry + 103.0) * 0.0042
    assert np.isclose(tr["r_net"], (103.0 - entry - fees) / R) and np.isclose(tr["cost_R"], (fees + (entry - 100.0)) / R)


def test_stop_with_slippage():
    o, h, l, c = path(); e = 5; stop = 98.0; target = 103.0; l[7] = 97.9
    tr = S.simulate(o, h, l, c, e, stop, target, K1)
    assert tr["reason"] == "stop" and tr["exit_b"] == 7 and np.isclose(tr["exit_px"], 98.0 * 0.999)
    entry = 100.0 * 1.0005; R = entry - 98.0; px = 98.0 * 0.999; fees = (entry + px) * 0.0042
    assert np.isclose(tr["r_net"], (px - entry - fees) / R) and np.isclose(tr["cost_R"], (fees + (entry - 100.0) + (98.0 - px)) / R)
    # K0: keine Slippage, r_net = (98 - 100 - fees)/R
    tr0 = S.simulate(o, h, l, c, e, stop, target, K0); assert np.isclose(tr0["exit_px"], 98.0) and np.isclose(tr0["r_net"], (98.0 - 100.0 - 198.0 * 0.0016) / 2.0)


def test_gap_stop_and_gap_target():
    o, h, l, c = path(); e = 5; stop = 98.0; target = 103.0; o[8] = 97.0; l[8] = 96.5; h[8] = 97.5
    tr = S.simulate(o, h, l, c, e, stop, target, K1); assert tr["reason"] == "stop_gap" and np.isclose(tr["exit_px"], 97.0 * 0.999)
    o, h, l, c = path(); o[8] = 104.0; h[8] = 104.5; l[8] = 103.5
    tr = S.simulate(o, h, l, c, e, stop, target, K1); assert tr["reason"] == "target_gap" and tr["exit_px"] == 104.0


def test_ambiguous_is_stop_and_order_of_checks():
    o, h, l, c = path(); e = 5; stop = 98.0; target = 103.0; l[7] = 97.9; h[7] = 103.5
    tr = S.simulate(o, h, l, c, e, stop, target, K1); assert tr["reason"] == "stop_ambiguous" and tr["exit_b"] == 7
    # Ziel in Kerze 6, Stop erst in Kerze 7 -> Ziel
    o, h, l, c = path(); h[6] = 103.1; l[7] = 97.0
    tr = S.simulate(o, h, l, c, e, stop, target, K1); assert tr["reason"] == "target" and tr["exit_b"] == 6
    # Einstiegskerze selbst zaehlt (kein stop_gap in e, aber low-Beruehrung)
    o, h, l, c = path(); l[5] = 97.0
    tr = S.simulate(o, h, l, c, e, stop, target, K1); assert tr["reason"] == "stop" and tr["exit_b"] == 5


def test_time_stop_24_bars_and_cut():
    o, h, l, c = path(60); e = 5; stop = 98.0; target = 103.0; o[29] = 100.7
    tr = S.simulate(o, h, l, c, e, stop, target, K1)
    assert tr["reason"] == "time24" and tr["exit_b"] == 29 and np.isclose(tr["exit_px"], 100.7 * (1 - 0.0005))
    # Kerze 28 ist die 24. gehaltene Kerze: Ziel dort zaehlt noch, in Kerze 29 nicht mehr
    o, h, l, c = path(60); h[28] = 103.5; assert S.simulate(o, h, l, c, e, stop, target, K1)["reason"] == "target"
    o, h, l, c = path(60); h[29] = 103.5; assert S.simulate(o, h, l, c, e, stop, target, K1)["reason"] == "time24"
    o, h, l, c = path(20); tr = S.simulate(o, h, l, c, e, stop, target, K1); assert tr["reason"] == "cut" and tr["exit_b"] == 19


def test_stop_init_and_invalid():
    o, h, l, c = path(); e = 5; o[5] = 97.5   # Eroeffnung unter dem Stop: R <= 0, nicht handelbar (valid_stop verlangt open[e] > Stop)
    tr = S.simulate(o, h, l, c, e, 98.0, 103.0, K1); assert tr["reason"] == "invalid_stop"
    o, h, l, c = path(); assert S.simulate(o, h, l, c, 5, 101.0, 103.0, K1)["reason"] == "invalid_stop"
    assert S.simulate(o, h, l, c, 5, 98.0, 99.0, K1)["reason"] == "target_below_entry"


def test_diagnostics():
    o, h, l, c = path(2000); e = 5; stop = 98.0; target = 103.0; l[7] = 97.0; h[15] = 103.2
    tr = S.simulate(o, h, l, c, e, stop, target, K1); d = S.diagnostics(o, h, l, c, e, stop, target, tr, tr["R"])
    assert d["stop_then_target"] is True
    o, h, l, c = path(2000); h[9] = 103.2; h[20] = 105.0; h[400] = 110.0
    tr = S.simulate(o, h, l, c, e, stop, target, K1); d = S.diagnostics(o, h, l, c, e, stop, target, tr, tr["R"])
    assert np.isclose(d["mfe_after_target_R"], (105.0 - 103.0) / tr["R"]) and d["new20d_high"] is True and d["new30d_high"] is True



def test_pipeline_synthetic():
    """Smoke-Test der gesamten Kette (Kandidaten -> Zellen -> Baseline -> Kontrollen -> Auswertung) auf synthetischen Daten."""
    sys.path.insert(0, "/home/claude/micro/tests"); sys.path.insert(0, "/home/claude/rtc")
    import pandas as pd, rlib as R, eval_micro as E
    from test_mlib import synth_1h, agg_4h
    df1 = synth_1h(9000, seed=21); df4 = agg_4h(df1); C = R.cfg_alt(); f4 = R.features(df4, C)
    f1 = M.features_1h(df1); J = M.join_4h(df1, df4, f4, C); A = M.avwap_episodes(df1, df4, f4, J); J["t4_ts"] = M._ts(df4["t"])
    cands = M.candidates(df1, f1, J, A, "SYN")
    blk1 = np.array(["P1" if i < 4500 else "P2" for i in range(len(df1))])
    if len(cands):
        tr = S.run_cells(df1, cands, blk1, "SYN", "cell"); assert set(tr.status) <= {"traded", "gap_in_window", "invalid_stop", "no_tight_invalidation", "target_below_entry", "no_episode", "overlap_skip"}
        t = tr[tr.status == "traded"]
        if len(t): assert (t.exit_b - t.e + 1 <= 25).all() and t.reason.isin(["target", "target_gap", "stop", "stop_gap", "stop_ambiguous", "time24", "cut"]).all()
    ev_full = pd.DataFrame([dict(event=int(e), t4=int(J["ctx_src"][np.where((J["event_id"] == e) & J["ctx_active"])[0][0]])) for e in sorted(set(J["ev4"][J["ev4"] >= 0]))])
    if len(ev_full):
        bt = S.baseline_table(df1, J, A, ev_full, "SYN"); assert (bt.e - 1 == bt.b).all()
        # Baseline-Einstieg ist die erste 1h-Kerze nach Ende der Kontextkerze
        t1 = M._ts(df1["t"]); assert all(t1[int(r.e)] == J["t4_ts"][int(r.t4)] + 4 * 3600 for _, r in bt.iterrows())
        base = S.run_cells(df1, bt, blk1, "SYN", "baseline")
    # Holm und Bootstrap-Helfer
    h = E.holm({"a": 0.01, "b": 0.04}); assert np.isclose(h["a"], 0.02) and np.isclose(h["b"], 0.04)
    bm = E.boot_mean(np.array([1.0, 2.0, 3.0])); assert bm["p_pos"] == 1.0 and np.isclose(bm["mean"], 2.0)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
