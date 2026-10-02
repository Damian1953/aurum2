"""Offline-Tests Vol-Target-Overlay v0.1 (Entwurf): Skalierungsmathematik, Deckel 1.0, No-Trade-Band, keine
Signalerzeugung, fehlende Daten (fail-closed), Kosten, Gleichheit mit der Basis bei neutraler Skalierung, Laufzeitsperre.
Nur synthetische Daten; keine Collector-, Holdout- oder Validation-Dateien."""
import csv, datetime as dt, math, os, random, subprocess, sys
import numpy as np, pandas as pd, pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "voltarget"))
import voltarget_engine as V      # noqa: E402
import base_adapter as BA         # noqa: E402
import run_voltarget as R         # noqa: E402

D0 = dt.date(2025, 1, 1)
COST = V.cost_scenarios()["maker_plan"]


def mkdays(n, E=0.0, ret=0.0, start=D0, events=None, seed=None, sigma=0.03):
    rng = random.Random(seed)
    px, out = 100.0, []
    for i in range(n):
        o = px
        r = rng.gauss(0, sigma) if seed is not None else (ret[i] if isinstance(ret, list) else ret)
        px = px * math.exp(r)
        e = E[i] if isinstance(E, list) else E
        out.append(dict(date=start + dt.timedelta(days=i), open=o, close=px, E=e, event=(events or {}).get(i)))
    return out


# ------------------------------------------------------------------ Skalierungsmathematik
def test_vol_estimates_match_hand_calculation():
    rets = [0.01 * ((-1) ** i) * (1 + i % 3) for i in range(10)]
    ss, sl = V.vol_estimates(rets, half_life=2, window=5, ann=365)
    r = rets[-5:]; lam = 0.5 ** 0.5
    w = [lam ** k for k in range(5)]
    var_s = sum(wk * x * x for wk, x in zip(w, reversed(r))) / sum(w)
    assert ss == pytest.approx(math.sqrt(var_s * 365)) and sl == pytest.approx(math.sqrt(sum(x * x for x in r) / 5 * 365))
    # konstante |r|: beide Schaetzer gleich -> s = 1
    ss, sl = V.vol_estimates([0.02, -0.02] * 200)
    assert ss == pytest.approx(sl) and V.scale_factor(ss, sl) == pytest.approx(1.0)
    assert ss == pytest.approx(0.02 * math.sqrt(365))


def test_scale_responds_to_recent_vol_and_cap():
    calm, wild = [0.01, -0.01] * 172, [0.05, -0.05] * 11
    ss, sl = V.vol_estimates(calm + wild[:21])                  # juengste Renditen hoch -> s < 1
    s = V.scale_factor(ss, sl); assert 0 < s < 0.6
    ss, sl = V.vol_estimates(wild * 16 + [0.05] + calm[:20])   # juengste ruhig -> Verhaeltnis > 1, gedeckelt
    assert sl / ss > 1 and V.scale_factor(ss, sl) == 1.0
    assert V.PARAMS == dict(half_life=20, window=365, ann=365, band=0.10, max_lev=1.0, capital=1000.0)


def test_target_weight_cap_and_never_above_base():
    for E in (0.0, 0.5, 0.75, 1.0):
        for s in (0.0, 0.3, 1.0):
            t = V.target_weight(E, s)
            assert 0.0 <= t <= E <= 1.0 and t == pytest.approx(E * s)
    assert V.target_weight(1.0, None) is None and V.target_weight(0.0, None) == 0.0
    with pytest.raises(V.InvariantError):
        V.target_weight(1.25, 1.0)                               # Basis ueber 1.0 waere Hebel
    with pytest.raises(V.InvariantError):
        V.target_weight(1.0, 1.5)


# ------------------------------------------------------------------ No-Trade-Band
def test_band_threshold_and_events():
    assert V.rebalance_target(0.80, 1.0, 0.71, None, flat=False) is None          # |0.71-0.80| = 0.09 <= 0.10
    assert V.rebalance_target(0.80, 1.0, 0.69, None, flat=False) == pytest.approx(0.69)
    assert V.rebalance_target(0.60, 1.0, 0.75, None, flat=False) == pytest.approx(0.75)  # nach oben ebenso, aber <= E
    assert V.rebalance_target(0.40, 0.75, 0.8, "add", flat=False) == pytest.approx(0.60)  # Basis-Ereignis immer
    assert V.rebalance_target(0.0, 1.0, 0.95, "entry", flat=True) == pytest.approx(0.95)
    assert V.rebalance_target(0.0, 1.0, 0.95, None, flat=True) == pytest.approx(0.95)    # Synchronisation (Start)
    assert V.rebalance_target(0.55, 0.0, 0.5, "exit", flat=False) == 0.0                  # Ausstieg immer ganz
    assert V.rebalance_target(0.0, 0.0, 0.5, None, flat=True) is None


def test_band_limits_trading_in_simulation():
    n = 420
    rets = [0.01 * (-1) ** i for i in range(n)]
    for i in range(380, 400):
        rets[i] = 0.06 * (-1) ** i                                  # Vol-Schock
    days = mkdays(n, E=1.0, ret=rets)
    r_band = V.simulate(days, COST, 370)
    r_zero = V.simulate(days, COST, 370, band=0.0)
    assert len(r_band["trades"]) < len(r_zero["trades"])
    assert any(t["reason"] == "vol" and t["side"] == "sell" for t in r_band["trades"])
    for t in r_band["trades"][1:]:
        assert t["reason"] in ("vol", "exit", "exit_stop", "entry", "add")
    assert min(e["weight"] for e in r_band["equity"][15:]) < 0.6


# ------------------------------------------------------------------ keine Signalerzeugung
def test_no_signal_creation_when_base_flat():
    days = mkdays(500, E=0.0, seed=7, sigma=0.05)
    r = V.simulate(days, COST, 380)
    assert r["trades"] == [] and all(e["weight"] == 0.0 for e in r["equity"]) and r["equity"][-1]["equity"] == 1000.0


@pytest.mark.parametrize("seed", range(5))
def test_random_paths_overlay_never_exceeds_base(seed):
    rng = random.Random(seed); n = 600; E, ev, cur = [], {}, 0.0
    for i in range(n):
        if i > 370 and rng.random() < 0.03:
            nxt = rng.choice([0.0, 0.5, 0.75, 1.0])
            if nxt != cur:
                ev[i] = "entry" if cur == 0 else ("exit" if nxt == 0 else "add")
            cur = nxt
        E.append(cur if i > 370 else 0.0)
    days = mkdays(n, E=E, events=ev, seed=seed, sigma=0.04)
    r = V.simulate(days, COST, 365)
    for e in r["equity"]:
        if e["E"] == 0:
            assert e["weight"] == 0.0
    for t in r["trades"]:
        if t["side"] == "buy":
            day = next(x for x in days if str(x["date"]) == t["date"])
            assert day["E"] > 0 and t["w_target"] <= day["E"] + 1e-12 and t["w_target"] <= 1.0


def test_invariant_raises_if_position_while_base_flat():
    days = mkdays(400, E=[1.0] * 380 + [0.0] * 20)        # Basis flach ohne Ausstiegsereignis -> Overlay folgt trotzdem
    r = V.simulate(days, COST, 370)
    assert r["equity"][-1]["weight"] == 0.0
    with pytest.raises(V.InvariantError):
        V.simulate(days, COST, 370, scale_override=1.5)    # s > 1 ist verboten


# ------------------------------------------------------------------ fehlende Daten (fail-closed)
def test_insufficient_history_blocks_entry():
    days = mkdays(200, E=[0.0] * 100 + [1.0] * 100, events={100: "entry"}, seed=1)
    r = V.simulate(days, COST, 50)
    assert r["status"] == "STOPPED" and "Vol" in r["stop"]["reason"] and r["trades"] == []


def test_gap_stops_and_nan_in_window_blocks_scaling():
    days = mkdays(420, E=1.0, seed=2)
    gap = days[:400] + [dict(x, date=x["date"] + dt.timedelta(days=3)) for x in days[400:]]
    r = V.simulate(gap, COST, 380)
    assert r["status"] == "STOPPED" and "Luecke" in r["stop"]["reason"] and len(r["equity"]) == 20
    bad = [dict(x) for x in days]; bad[300]["close"] = float("nan")
    rets = V.log_returns([x["close"] for x in bad], [x["date"] for x in bad])
    assert V.vol_estimates(rets[:380]) == (None, None)
    r2 = V.simulate(bad, COST, 380)
    assert r2["status"] == "STOPPED" and r2["trades"] == []
    assert V.vol_estimates([0.0] * 365) == (None, None)       # Varianz 0 -> keine Skalierung


def test_stopped_still_executes_base_exit():
    n = 800; E = [0.0] * 380 + [1.0] * 390 + [0.0] * 30
    days = mkdays(n, E=E, events={380: "entry", 770: "exit"}, seed=3)
    for i in range(381, n):                                   # ab Tag 381 konstanter Kurs -> Varianz 0 -> s undefiniert
        days[i]["open"] = days[i]["close"] = days[380]["close"]
    r = V.simulate(days, COST, 370)
    assert r["status"] == "STOPPED" and "Vol" in r["stop"]["reason"]
    assert r["trades"][0]["side"] == "buy" and r["trades"][-1]["side"] == "sell" and r["trades"][-1]["reason"] == "exit"
    assert not any(t["reason"] == "vol" and t["date"] > r["stop"]["date"] for t in r["trades"])
    assert r["equity"][-1]["weight"] == 0.0


# ------------------------------------------------------------------ Kosten und Basis-Gleichheit
def test_costs_entry_and_stop_exit():
    E = [0.0] * 380 + [1.0] * 20 + [0.0] * 5
    days = mkdays(405, E=E, events={380: "entry", 400: "exit_stop"}, ret=0.0)
    for i, x in enumerate(days):
        x["close"] = 100.0 + (0.5 if i % 2 else -0.5); x["open"] = 100.0
    r = V.simulate(days, COST, 370, scale_override=1.0)
    buy, sell = r["trades"][0], r["trades"][-1]
    assert buy["fee"] == pytest.approx(buy["value"] * 0.0047) and sell["fee"] == pytest.approx(sell["value"] * 0.0052)
    assert buy["value"] == pytest.approx(1000.0)                       # Konvention PAPER F3: Kosten zusaetzlich
    assert r["equity"][-1]["equity"] == pytest.approx(1000 - 1000 * 0.0047 - 1000 * 0.0052)


def synth(n=900, seed=1):
    rng = np.random.default_rng(seed)
    c = 100 * np.exp(np.cumsum(rng.normal(0.001, 0.03, n)))
    o = np.r_[c[0], c[:-1]] * (1 + rng.normal(0, 0.003, n))
    h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.01, n)))
    l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.01, n)))
    return pd.DataFrame(dict(open=o, high=h, low=l, close=c), index=pd.date_range("2024-01-01", periods=n, freq="D", tz="UTC"))


@pytest.mark.parametrize("seed", [1, 2, 3])
@pytest.mark.parametrize("strat", ["W2", "T55_20"])
def test_neutral_scale_reproduces_unchanged_sleeve(seed, strat):
    d = synth(900, seed); st = pd.Timestamp("2024-08-01", tz="UTC")
    days, nE, nEv = BA.base_days(d, strat, paper_start=st)
    i0 = BA.start_index(days, st.date())
    for cname, cost in V.cost_scenarios().items():
        r = V.simulate(days, cost, i0, nE, nEv, band=float("inf"), scale_override=1.0)
        acc = BA.P.account(d, BA.P.decide(d, strat, start_ts=st), cost, start_ts=st)
        mine = pd.Series([e["equity"] for e in r["equity"]], index=pd.to_datetime([e["date"] for e in r["equity"]], utc=True))
        assert len(acc["trades"]) > 0
        assert np.allclose(mine.values, acc["equity"].loc[mine.index].values, rtol=1e-12, atol=1e-9)


@pytest.mark.parametrize("seed", [1, 2])
@pytest.mark.parametrize("strat", ["W2", "W6", "T55_20"])
def test_adapter_overlay_flat_when_base_flat(seed, strat):
    d = synth(900, seed); st = pd.Timestamp("2025-02-01", tz="UTC")  # >= 365 Renditen Warmup
    days, nE, nEv = BA.base_days(d, strat, paper_start=st)
    assert {x["E"] for x in days} <= ({0.0, 0.5, 0.75, 1.0} if strat == "W6" else {0.0, 1.0})
    r = V.simulate(days, COST, BA.start_index(days, st.date()), nE, nEv)
    E_by = {str(x["date"]): x["E"] for x in days}
    assert all(e["weight"] == 0.0 for e in r["equity"] if E_by[e["date"]] == 0.0)
    i0 = BA.start_index(days, st.date())
    assert r["status"] == "OK"
    if any(x["E"] > 0 for x in days[i0 + 1:]):
        assert any(e["weight"] > 0 for e in r["equity"])
    # Konvention PAPER F3: Kosten zusaetzlich zum Nominal -> Gewicht hoechstens um Kostenfinanzierung ueber 1.0
    assert all(e["weight"] <= 1.0 + 0.02 for e in r["equity"])
    for t in r["trades"]:
        if t["side"] == "buy":
            assert t["w_target"] <= 1.0 and t["w_target"] <= E_by[t["date"]] + 1e-12


def test_constant_control_scales_down():
    d = synth(900, 1); st = pd.Timestamp("2024-08-01", tz="UTC")
    days, nE, nEv = BA.base_days(d, "W2", paper_start=st)
    r = V.simulate(days, COST, BA.start_index(days, st.date()), nE, nEv, band=float("inf"), scale_override=0.5)
    assert max(e["weight"] for e in r["equity"]) < 0.75 and all(t["reason"] != "vol" for t in r["trades"])


# ------------------------------------------------------------------ Sperre, Datenschutz, kein Scheduler
def test_runtime_guard_refuses_while_disabled(monkeypatch, tmp_path):
    cfg = R.load_cfg()
    assert cfg["enabled"] is False and cfg["start_bar"] is None and cfg["freeze_list"] is None
    assert R.params_ok(cfg)
    monkeypatch.setattr(sys, "argv", ["run_voltarget.py"])
    assert R.main() == 3
    with pytest.raises(R.Disabled):
        R.run(cfg, str(tmp_path), str(tmp_path / "out"))
    with pytest.raises(R.Disabled):                           # Produktionsverzeichnis nur mit echter Freigabe
        R.run(dict(cfg, enabled=True, start_bar="2026-10-03", freeze_list="x"), str(tmp_path), R.OUT)
    assert not (tmp_path / "out").exists()
    bad = dict(cfg, params=dict(cfg["params"], band=0.05))
    assert not R.params_ok(bad)
    r = subprocess.run([sys.executable, os.path.join(REPO, "voltarget", "run_voltarget.py")], capture_output=True, text=True)
    assert r.returncode == 3 and "nicht freigegeben" in r.stdout


def test_guard_path_blocks_holdout_and_validation():
    for p in ("/x/02_daten/holdout/a.csv", "/x/BTCUSDT_spot4h_validation.csv"):
        with pytest.raises(PermissionError):
            V.guard_path(p)
        with pytest.raises(PermissionError):
            BA.load_bars(p)
    assert V.guard_path("/workspace/aurum2/data_live/kraken_ohlc/BTCUSD_1d.csv")


def test_no_scheduler_entry_and_no_wrapper():
    sched = open(os.path.join(REPO, "collector", "ensure_scheduler.sh")).read()
    assert "voltarget" not in sched.lower()
    assert not [f for f in os.listdir(os.path.join(REPO, "voltarget")) if f.endswith(".sh")]
    cr = subprocess.run(["crontab", "-l"], capture_output=True, text=True) if os.path.exists("/usr/bin/crontab") else None
    if cr is not None and cr.returncode == 0:
        assert "voltarget" not in cr.stdout.lower()


def test_runner_on_synthetic_live_dir(tmp_path):
    live = tmp_path / "live"; (live / "kraken_ohlc").mkdir(parents=True)
    d = synth(900, 2)
    d.index = pd.date_range("2024-03-01", periods=900, freq="D", tz="UTC")
    for coin in BA.COINS:
        with open(live / "kraken_ohlc" / f"{coin}USD_1d.csv", "w", newline="") as fh:
            w = csv.writer(fh); w.writerow(["t", "open", "high", "low", "close", "volume", "trades"])
            for t, row in d.iterrows():
                w.writerow([t.strftime("%Y-%m-%dT%H:%M:%SZ"), row.open, row.high, row.low, row.close, 1, 1])
    cfg = dict(R.load_cfg(), enabled=True, start_bar="2026-01-01", freeze_list="unbenutzt.txt")
    now = pd.Timestamp("2026-08-20", tz="UTC")
    rc, st = R.run(cfg, str(live), str(tmp_path / "out"), now=now)
    assert rc == 0 and (tmp_path / "out/ledger/equity_daily.csv").exists()
    rows = list(csv.DictReader(open(tmp_path / "out/ledger/equity_daily.csv")))
    assert {r["strat"] for r in rows} == set(BA.STRATS) and {r["scenario"] for r in rows} == {"maker_plan", "taker_K2"}
    assert all(float(r["weight"]) == 0.0 for r in rows if float(r["E_base"]) == 0.0)
