"""Tests Paper-Runner v1.0 (PAPER_PREREG_v1.0). Synthetisch plus Aequivalenz gegen das eingefrorene s2lib.run_trend
auf Binance-Tageskerzen bis 2023 (Discovery-Zeitraum) und auf den Kraken-Collector-Daten (nur Entscheidungsgleichheit)."""
import json, os, sys, types
import numpy as np, pandas as pd, pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "paper"))
import paper_engine as E
import run_paper as RP


def synth(n=400, seed=1, start="2025-01-01"):
    rng = np.random.default_rng(seed)
    r = rng.normal(0.001, 0.03, n)
    c = 100 * np.exp(np.cumsum(r))
    o = np.r_[c[0], c[:-1]] * (1 + rng.normal(0, 0.003, n))
    h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.01, n)))
    l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.01, n)))
    idx = pd.date_range(start, periods=n, freq="D", tz="UTC")
    return pd.DataFrame(dict(open=o, high=h, low=l, close=c), index=idx)


def s2_trades(d, pyramid):
    cd = types.SimpleNamespace(idx=d.index, spot=d, fund_day=pd.Series(0.0, index=d.index))
    _, tr = E.S2.run_trend(cd, E.S2.indicators(d), side=+1, mode="breakout", N=55, k=3.0, gate=True, sma_n=200, pyramid=pyramid)
    return [(d.index[x["entry_t"]], round(x["entry_fill"], 10), d.index[x["exit_t"]], x["exit_reason"], len(x["units"])) for x in tr]


def mine(d, strat):
    dec = E.decide(d, strat, start_ts=None)
    return [(x["entry_t"], round(x["entry_fill"], 10), x["exit_t"], x["exit_reason"], len(x["units"])) for x in dec["trades"]]


@pytest.mark.parametrize("seed", [1, 2, 3])
@pytest.mark.parametrize("strat,pyr", [("W2", False), ("W6", True)])
def test_equivalence_synthetic(seed, strat, pyr):
    d = synth(900, seed)
    assert mine(d, strat) == s2_trades(d, pyr)
    assert len(s2_trades(d, pyr)) > 0


@pytest.mark.parametrize("coin", ["BTC", "ETH", "SOL"])
@pytest.mark.parametrize("strat,pyr", [("W2", False), ("W6", True)])
def test_equivalence_binance_bis_2023(coin, strat, pyr):
    f = os.path.join(REPO, "data", "raw", "binance", f"{coin}USDT_1d.csv")
    if not os.path.exists(f):
        pytest.skip("Rohdaten fehlen")
    d = E.S2.load_ohlc(f)
    d = d[d.index < pd.Timestamp("2024-01-01", tz="UTC")][["open", "high", "low", "close"]]
    a, b = mine(d, strat), s2_trades(d, pyr)
    assert a == b and len(a) >= 3


@pytest.mark.parametrize("strat,pyr", [("W2", False), ("W6", True)])
def test_equivalence_kraken_live(strat, pyr):
    f = "/workspace/aurum2/data_live/kraken_ohlc/BTCUSD_1d.csv"
    if not os.path.exists(f):
        pytest.skip("Collector-Daten fehlen")
    d = E.load_kraken_1d(f, pd.Timestamp("2026-10-01", tz="UTC"))
    assert mine(d, strat) == s2_trades(d, pyr)


def test_start_flat_and_no_entry_signal_before_start():
    d = synth(600, 4)
    st = d.index[450]
    for s in E.STRATS:
        dec = E.decide(d, s, start_ts=st)
        for tr in dec["trades"] + ([dec["open"]] if dec["open"] else []):
            assert tr["entry_sig"] >= st and tr["entry_t"] > st


def test_no_lookahead():
    d = synth(700, 5)
    T = d.index[600]
    d2 = d.copy()
    d2.loc[d2.index > T, ["open", "high", "low", "close"]] *= 1.7
    for s in E.STRATS:
        a = [x for x in E.decide(d, s, start_ts=d.index[250])["log"] if x["t"] <= T]
        b = [x for x in E.decide(d2, s, start_ts=d.index[250])["log"] if x["t"] <= T]
        assert a == b


def test_turtle_rules():
    n = 120
    idx = pd.date_range("2025-01-01", periods=n, freq="D", tz="UTC")
    c = np.full(n, 100.0); c[80] = 110.0; c[81:] = 109.0; c[90] = 95.0
    d = pd.DataFrame(dict(open=c.copy(), high=c + 1, low=c - 1, close=c), index=idx)
    d.loc[idx[81], "open"] = 108.0
    dec = E.decide(d, "T55_20", start_ts=idx[60])
    tr = dec["trades"][0]
    assert tr["entry_sig"] == idx[80] and tr["entry_t"] == idx[81] and tr["entry_fill"] == 108.0
    n20 = E.indicators(d)["atr20"].iloc[80]
    # Schluss 95 am Bar 90: unter Notstopp (108 - 2N) -> Notstopp hat Vorrang vor dem 20-Tage-Tief
    assert 95.0 <= 108.0 - 2 * n20
    assert tr["exit_sig"] == idx[90] and tr["exit_reason"] == "notstopp" and tr["exit_t"] == idx[91]


def test_turtle_exit20():
    n = 140
    idx = pd.date_range("2025-01-01", periods=n, freq="D", tz="UTC")
    c = 100 + 0.5 * np.arange(n, dtype=float)
    c[100:] = c[99] - 0.4 * np.arange(1, n - 99)   # langsamer Rueckgang, kein Notstopp zuerst
    d = pd.DataFrame(dict(open=c, high=c + 0.2, low=c - 0.2, close=c), index=idx)
    dec = E.decide(d, "T55_20", start_ts=idx[60])
    assert dec["trades"] and dec["trades"][0]["exit_reason"] in ("exit20", "notstopp")
    ind = E.indicators(d)
    t0 = dec["trades"][0]
    i = d.index.get_loc(t0["exit_sig"])
    assert d["close"].iloc[i] < ind["ll20"].iloc[i] or d["close"].iloc[i] <= t0["entry_fill"] - 2 * ind["atr20"].loc[t0["entry_sig"]]


def test_costs_from_config_and_accounting():
    cs = E.cost_scenarios()
    assert cs["maker_plan"]["c_in"] == pytest.approx(0.004 + 0.0002 + 0.0005)
    assert cs["maker_plan"]["c_out_stop"] == pytest.approx(0.004 + 0.0002 + 0.001)
    assert cs["taker_K2"]["c_in"] == pytest.approx(0.008 + 0.0006 + 0.0015)
    idx = pd.date_range("2025-01-01", periods=5, freq="D", tz="UTC")
    d = pd.DataFrame(dict(open=[100, 100, 110, 120, 120.0], high=[1] * 5, low=[1] * 5, close=[100, 105, 115, 120, 120.0]), index=idx)
    tr = dict(entry_sig=idx[0], entry_t=idx[1], entry_fill=100.0, units=[(100.0, 1.0, idx[1])], exit_sig=idx[2], exit_t=idx[3],
              exit_fill=120.0, exit_reason="stop")
    acc = E.account(d, dict(trades=[tr], open=None), cs["maker_plan"], start_ts=idx[0], capital=1000.0)
    c_in, c_out = cs["maker_plan"]["c_in"], cs["maker_plan"]["c_out_stop"]
    assert acc["equity"].iloc[-1] == pytest.approx(-1000 * c_in + 1200 * (1 - c_out))
    assert acc["trades"][0]["costs_usd"] == pytest.approx(1000 * c_in + 1200 * c_out, abs=1e-3)
    assert acc["equity"].loc[idx[2]] == pytest.approx(-1000 * c_in + 1150)


def test_incomplete_bar_dropped(tmp_path):
    d = synth(10)
    p = tmp_path / "x.csv"
    d.reset_index().rename(columns={"index": "t"}).to_csv(p, index=False)
    now = d.index[-1] + pd.Timedelta(hours=5)
    x = E.load_kraken_1d(str(p), now)
    assert x.index[-1] == d.index[-2]


def _write_live(live, n=600, seed=7, start="2025-01-01"):
    os.makedirs(os.path.join(live, "kraken_ohlc"), exist_ok=True)
    for i, coin in enumerate(E.COINS):
        d = synth(n, seed + i, start)
        d.reset_index().rename(columns={"index": "t"}).to_csv(os.path.join(live, "kraken_ohlc", f"{coin}USD_1d.csv"), index=False)


def test_runner_end_to_end_idempotent_and_revision(tmp_path, monkeypatch):
    live, out = str(tmp_path / "live"), str(tmp_path / "out")
    _write_live(live)
    monkeypatch.setattr(E, "START_BAR", pd.Timestamp("2026-03-01", tz="UTC"))
    now = pd.Timestamp("2026-08-20 05:00", tz="UTC")
    r1 = RP.run(now_utc=now, live=live, out=out, enforce_freeze=False)
    assert r1["ok"], r1
    st = json.load(open(os.path.join(out, "state", "state_latest.json")))
    assert set(st["portfolio"]) == {"W2", "W6", "T55_20", "BH"}
    eq = pd.read_csv(os.path.join(out, "ledger", "equity_daily.csv"))
    assert (eq["date"] >= "2026-03-01").all()
    r2 = RP.run(now_utc=now, live=live, out=out, enforce_freeze=False)
    assert r2["ok"] and r2["new_events"] == 0
    assert not RP.needed(out, now)
    # Vergangenheit veraendern -> Revision wird erkannt
    ev = [json.loads(l) for l in open(os.path.join(out, "ledger", "journal.jsonl"))]
    fill = next(e for e in ev if e["event"].startswith("FILL"))
    f = os.path.join(live, "kraken_ohlc", f"{fill['coin']}USD_1d.csv")
    d = pd.read_csv(f); m = d["t"].str[:10] == fill["t"]; assert m.sum() == 1
    d.loc[m, "open"] *= 1.01; d.to_csv(f, index=False)
    r3 = RP.run(now_utc=now, live=live, out=out, enforce_freeze=False)
    assert not r3["ok"] and any("REVISION" in e for e in r3["errors"])
    # Wochenbericht laeuft
    import subprocess
    env = dict(os.environ, AURUM_PAPER_OUT=out)
    p = subprocess.run([sys.executable, os.path.join(REPO, "paper", "wochenbericht.py"), "--datum", "2026-08-20"], env=env,
                       capture_output=True, text=True, timeout=120)
    assert p.returncode == 0, p.stderr
    txt = open(p.stdout.strip()).read()
    assert "Wochenbericht" in txt and "Betrieb" in txt


def test_gap_fail_closed(tmp_path, monkeypatch):
    live, out = str(tmp_path / "live"), str(tmp_path / "out")
    _write_live(live)
    f = os.path.join(live, "kraken_ohlc", "ETHUSD_1d.csv")
    d = pd.read_csv(f); d = d.drop(d.index[-30]); d.to_csv(f, index=False)
    monkeypatch.setattr(E, "START_BAR", pd.Timestamp("2026-03-01", tz="UTC"))
    r = RP.run(now_utc=pd.Timestamp("2026-08-20 05:00", tz="UTC"), live=live, out=out, enforce_freeze=False)
    assert not r["ok"] and any("ETH" in e and "Luecke" in e for e in r["errors"])
