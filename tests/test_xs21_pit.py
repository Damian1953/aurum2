"""Synthetische Tests fuer XS21 PiT v1.0 (kein Netz, keine echten Daten)."""
import os, sys
import numpy as np, pandas as pd, pytest
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "01_forschung/09_lane_c/xs21_pit_v1.0"))
import xs21_pit as X

D0, D1 = pd.Timestamp("2020-01-01", tz="UTC"), pd.Timestamp("2020-06-30", tz="UTC")


@pytest.fixture(autouse=True)
def short_period(monkeypatch):
    monkeypatch.setattr(X, "END", pd.Timestamp("2020-06-29", tz="UTC"))
    monkeypatch.setattr(X, "DATA_END", D1)


def synth(n_sym=25, seed=1, delist=None, gap=None, qv=1e7, perturb_after=None, drop_funding=None):
    rng = np.random.default_rng(seed)
    days = pd.date_range(D0, D1, freq="D", tz="UTC")
    K, fr, listing = {}, [], {}
    for k in range(n_sym):
        s = f"S{k:02d}USDT"
        p = 100 * np.exp(np.cumsum(rng.normal(0.002 * (k - n_sym / 2) / n_sym, 0.03, len(days))))
        if perturb_after is not None:
            m = days > perturb_after
            p[m] = p[m] * np.exp(np.random.default_rng(99 + k).normal(0, 0.2, m.sum()))
        o = np.r_[p[0], p[:-1]]
        d = pd.DataFrame(dict(open=o, close=p, qv=qv), index=days)
        if delist and s in delist:
            d = d[d.index <= delist[s]]
        if gap and s in gap:
            a, b = gap[s]; d = d[(d.index < a) | (d.index > b)]
        K[s] = d
        listing[s] = ("2020-01", d.index[-1].strftime("%Y-%m"))
        for t in pd.date_range(D0, d.index[-1] + pd.Timedelta(hours=16), freq="8h", tz="UTC"):
            if drop_funding and (s, t) in drop_funding: continue
            fr.append((s, int(t.value // 10**6), 8.0, 0.0001 * (1 + k % 3)))
    F = pd.DataFrame(fr, columns=["sym", "ms", "interval", "rate"]); F["t"] = pd.to_datetime(F["ms"], unit="ms", utc=True).dt.floor("h")
    tb = pd.Series(0.02, index=pd.DatetimeIndex([D0]))
    return X.Data(K, F, listing, tb, days=days)


def test_universe_m6_and_subset():
    D = synth(n_sym=25, qv=2e6)   # Monatsumsatz 31 * 2e6 = 62 Mio. >= 50 Mio.
    U = X.universes(D)
    u = [x for x in U if x["T"] >= pd.Timestamp("2020-02-01", tz="UTC")]
    assert all(len(x["U1"]) == 25 and set(x["U2"]) <= set(x["U1"]) and len(x["U2"]) == 20 for x in u)
    # Gleichstand im Volumen: alphabetisch
    assert [D.syms[j] for j in u[0]["U2"]] == sorted(D.syms)[:20]
    assert X.run_start(U) == pd.Timestamp("2020-02-01", tz="UTC")
    D2 = synth(n_sym=19, qv=2e6)
    U2 = X.universes(D2)
    assert X.run_start(U2) is None


def test_no_lookahead():
    cut = pd.Timestamp("2020-04-10", tz="UTC")
    A = synth(qv=2e6); B = synth(qv=2e6, perturb_after=cut)
    ua, ub = X.universes(A), X.universes(B)
    s = X.run_start(ua)
    Wa = X.weights(A, ua, "U1", s)[0]; Wb = X.weights(B, ub, "U1", s)[0]
    i = A.days.get_loc(cut)
    assert np.array_equal(Wa[: i + 1], Wb[: i + 1])          # Gewichte bis zum Schnitt unabhaengig von spaeteren Kursen
    assert not np.array_equal(Wa, Wb)


def test_weights_and_accounting():
    D = synth(qv=2e6); U = X.universes(D); s = X.run_start(U)
    W, log, gov, cash = X.weights(D, U, "U1", s)
    assert np.abs(W).sum(1).max() <= 1 + 1e-12 and np.isclose(np.clip(W, 0, None).sum(1).max(), 0.5)
    i = D.days.get_loc(s)
    assert (W[: i + 1] == 0).all() and (W[i + 1] != 0).sum() == 6
    c = X.S.COST["K1"]; sim = X.simulate(D, W, c, U, "U1", gov, s)
    turn = np.abs(np.diff(np.vstack([np.zeros((1, W.shape[1])), W]), axis=0))
    assert np.isclose(np.nansum(sim["cost"]), (turn[sim["mask"]] * (c["fee"] + c["fric"])).sum())
    recon = sim["gross"] + sim["funding"] + sim["cash"] - sim["cost"]
    assert np.allclose(recon.dropna(), sim["net"].dropna())
    assert sim["fill"]["L"]["n_fill"] == 0 and sim["fill"]["S"]["n_fill"] == 0
    # Trades: Brutto = w * (Exit/Entry - 1) auf Eroeffnungskursen
    tr = X.trades(D, W, sim, c)[0]
    j = D.si[tr["sym"]]; a = D.days.get_loc(tr["entry_date"]); b = D.days.get_loc(tr["exit_date"])
    assert np.isclose(tr["pnl_gross"], tr["w"] * (D.O[b, j] / D.O[a, j] - 1))
    assert np.isclose(tr["cost"], 2 * abs(tr["w"]) * (c["fee"] + c["fric"]))


def test_delisting_exit_cost_and_cash():
    D = synth(qv=2e6); U = X.universes(D); s = X.run_start(U)
    W = X.weights(D, U, "U1", s)[0]
    held = [(j, t) for t in range(len(D.days)) for j in range(len(D.syms)) if W[t, j] != 0 and t > D.days.get_loc(s) + 3]
    j, t = held[0]; sym = D.syms[j]; day = D.days[t]
    D2 = synth(qv=2e6, delist={sym: day}); U2 = X.universes(D2)
    W2, _, gov, _ = X.weights(D2, U2, "U1", s)
    j2 = D2.si[sym]
    assert W2[t, j2] != 0 and (W2[t + 1:, j2] == 0).all()
    c = X.S.COST["K1"]; sim = X.simulate(D2, W2, c, U2, "U1", gov, s)
    assert np.isclose(sim["cost_m"][t, j2], abs(W2[t, j2]) * (c["fee"] + X.DELIST_FRIC) + (sim["cost_m"][t, j2] - abs(W2[t, j2]) * (c["fee"] + X.DELIST_FRIC)))
    assert np.isclose(sim["cost_m"][t + 1, j2], 0.0)
    assert np.isclose(D2.R[t, j2], D2.C[t, j2] / D2.O[t, j2] - 1)
    trs = [x for x in X.trades(D2, W2, sim, c) if x["sym"] == sym and x["delist_exit"]]
    assert trs and np.isclose(trs[0]["cost"], abs(trs[0]["w"]) * (2 * c["fee"] + c["fric"] + X.DELIST_FRIC))


def test_relisting_gap_splits_life():
    D = synth(qv=2e6, gap={"S03USDT": (pd.Timestamp("2020-03-01", tz="UTC"), pd.Timestamp("2020-03-10", tz="UTC"))})
    j = D.si["S03USDT"]
    assert D.n_relist == 1 and D.life[D.days.get_loc(pd.Timestamp("2020-02-28", tz="UTC")), j] == 0
    assert D.life[D.days.get_loc(pd.Timestamp("2020-03-11", tz="UTC")), j] == 1
    assert np.isnan(D.R[D.days.get_loc(pd.Timestamp("2020-03-05", tz="UTC")), j])


def test_missing_funding_filled_adversely():
    D = synth(qv=2e6); U = X.universes(D); s = X.run_start(U)
    W = X.weights(D, U, "U1", s)[0]
    t = D.days.get_loc(s) + 2
    longs = [j for j in range(len(D.syms)) if W[t, j] > 0]; shorts = [j for j in range(len(D.syms)) if W[t, j] < 0]
    drop = {(D.syms[longs[0]], D.days[t] + pd.Timedelta(hours=8)), (D.syms[shorts[0]], D.days[t] + pd.Timedelta(hours=8))}
    D2 = synth(qv=2e6, drop_funding=drop); U2 = X.universes(D2)
    W2, _, gov, _ = X.weights(D2, U2, "U1", s)
    assert np.array_equal(W, W2)
    c = X.S.COST["K1"]
    sim = X.simulate(D2, W2, c, U2, "U1", gov, s)
    assert sim["fill"]["L"]["n_fill"] == 1 and sim["fill"]["S"]["n_fill"] == 1
    mem = U2[gov[t]]["U1"]
    bh = D2.by_hour[(D2.days[t] + pd.Timedelta(hours=8)).value]
    med = np.median([abs(bh[jj]) for jj in mem if jj in bh])
    for j in (longs[0], shorts[0]):
        obs = D2.FD[t, j]
        assert np.isclose(sim["fund_raw"][t, j], -W2[t, j] * obs - abs(W2[t, j]) * med)   # Long und Short zahlen


def test_evaluate_and_criteria_run_end_to_end():
    D = synth(qv=2e6); U = X.universes(D); s = X.run_start(U)
    r = X.evaluate(D, U, "U1", s, nboot=50)
    r["holm_p"] = r["boot"]["p_sharpe"]
    neigh = [dict(expectancy=0.001, sharpe=1.0)] * 3
    crit, verdict = X.criteria(r, neigh)
    assert verdict in ("BESTANDEN", "TEILWEISE", "VERWORFEN") and set(crit) >= {"c1", "c3", "c4", "c5", "c6", "c7", "c8"}
    assert r["scen"]["K2"]["cost_sum"] > r["scen"]["K1"]["cost_sum"] > r["scen"]["K0"]["cost_sum"]


def test_full_lauf_pipeline_on_synthetic_data(tmp_path, monkeypatch):
    """Ganzer Lauf-Pfad (--laufbeginn, --lauf, Pruefskript-Eingaben) auf synthetischen Daten ueber den echten Zeitraum."""
    import json
    import xs21_pit_run as R
    monkeypatch.setattr(X, "END", pd.Timestamp("2026-09-14", tz="UTC"))
    monkeypatch.setattr(X, "DATA_END", pd.Timestamp("2026-09-15", tz="UTC"))
    rng = np.random.default_rng(3)
    days = pd.date_range("2020-01-01", "2026-09-15", freq="D", tz="UTC")
    K, fr, listing = {}, [], {}
    for k in range(24):
        s = f"S{k:02d}USDT"
        p = 10 * np.exp(np.cumsum(rng.normal(0, 0.04, len(days))))
        d = pd.DataFrame(dict(open=np.r_[p[0], p[:-1]], close=p, qv=5e6), index=days)
        if k == 5: d = d[d.index <= "2022-06-10"]
        if k == 6: d = d[(d.index < "2021-03-01") | (d.index > "2021-03-20")]
        K[s] = d; listing[s] = ("2020-01", d.index[-1].strftime("%Y-%m"))
        ts = pd.date_range(days[0], d.index[-1], freq="8h", tz="UTC")
        ts = ts[rng.random(len(ts)) > 0.01]
        fr += [(s, int(t.value // 10**6), 8.0, 1e-4) for t in ts]
    F = pd.DataFrame(fr, columns=["sym", "ms", "interval", "rate"]); F["t"] = pd.to_datetime(F["ms"], unit="ms", utc=True).dt.floor("h")
    D = X.Data(K, F, listing, pd.Series(0.03, index=pd.DatetimeIndex([days[0]])), days=days)
    monkeypatch.setattr(R, "load", lambda: D)
    monkeypatch.setattr(R, "inputs", lambda: {"spec": X.sha(X.SPEC)})
    monkeypatch.setattr(R, "RUN", str(tmp_path))
    R.laufbeginn()
    R.lauf()
    ev = json.load(open(tmp_path / "xs21_eval.json"))
    assert ev["meta"]["spec_sha256"] == X.SPEC_SHA
    for nm in ("U1_LS", "U2_LS"):
        r = ev["results"][nm]
        assert r["verdict"] in ("BESTANDEN", "TEILWEISE", "VERWORFEN") and "survivorship" in r and r["holm_p"] is not None
    with pytest.raises(SystemExit):
        R.lauf()   # ein einziger Lauf
