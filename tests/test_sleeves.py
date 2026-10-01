"""Offline-Tests Sleeves A/B (Entwurf v0.2): Signale, As-of ohne Look-ahead, Kosten, fail-closed, Runner-Sperre."""
import csv, datetime as dt, json, os, sys
import pytest
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "sleeves"))
import sleeve_engine as E
import run_sleeves as R

U = dt.timezone.utc
D = dt.date


def f(y, m, d, h=4):
    return dt.datetime(y, m, d, h, 15, tzinfo=U)


def test_mvrv_lookahead_and_states():
    # Wert fuer 09-30 erst am 10-02 04:15 abgerufen -> fuer Bar 10-01 (Schluss 10-02 00:00) nicht sichtbar
    mvrv = [(D(2026, 9, 29), 1.5, f(2026, 9, 30)), (D(2026, 9, 30), 3.6, f(2026, 10, 2))]
    s, info = E.signal_b(mvrv, D(2026, 10, 1), None)
    assert s == "INVESTIERT" and info["mvrv_obs"] == "2026-09-29"
    s, info = E.signal_b(mvrv, D(2026, 10, 2), "INVESTIERT")       # jetzt sichtbar: 3.6 > 3.5
    assert s == "CASH" and info["mvrv"] == 3.6
    mid = [(D(2026, 10, 1), 2.0, f(2026, 10, 2))]
    assert E.signal_b(mid, D(2026, 10, 2), "CASH")[0] == "CASH"      # Hysterese: erst < 1.0 wieder kaufen
    low = [(D(2026, 10, 1), 0.95, f(2026, 10, 2))]
    assert E.signal_b(low, D(2026, 10, 2), "CASH")[0] == "INVESTIERT"
    assert E.signal_b([(D(2026, 9, 1), 1.5, f(2026, 9, 2))], D(2026, 10, 2), "INVESTIERT")[0] == "STOPPED"  # veraltet
    assert E.signal_b([(D(2026, 9, 1), 4.0, f(2026, 9, 2))], D(2026, 9, 3), None)[0] == "CASH"            # Start > 3.5


def test_check_raises_on_lookahead():
    with pytest.raises(E.LookAheadError):
        E._check((D(2026, 9, 30), 1.0, f(2026, 10, 2)), dt.datetime(2026, 10, 2, 0, 0, tzinfo=U))


def _h41(weeks, start, base, step, fetch_lag_days=1):
    walcl, tga, rrp = [], [], []
    for i in range(weeks):
        w = start + dt.timedelta(days=7 * i)
        ff = dt.datetime.combine(w + dt.timedelta(days=fetch_lag_days), dt.time(20, 50), U)  # Donnerstagabend
        walcl.append((w, base + step * i, ff)); tga.append((w, 800000.0, ff)); rrp.append((w, 10.0, f(w.year, w.month, w.day, 23)))
    return walcl, tga, rrp


def test_signal_a_friday_only_and_nl():
    w0 = D(2026, 6, 3)  # Mittwoch
    walcl, tga, rrp = _h41(20, w0, 6.6e6, 1000.0)
    fri = D(2026, 10, 2); assert fri.weekday() == 4
    s, info = E.signal_a(walcl, tga, rrp, fri, None)
    assert s == "INVESTIERT" and info["now"]["w"] == "2026-09-30" and info["delta"] == pytest.approx(13000.0)
    assert info["nl"] == pytest.approx(walcl[17][1] - 800000.0 - 10000.0)
    assert E.signal_a(walcl, tga, rrp, D(2026, 10, 1), "CASH") == ("CASH", None)    # kein Freitag
    walcl2, tga2, rrp2 = _h41(20, w0, 6.6e6, -1000.0)
    assert E.signal_a(walcl2, tga2, rrp2, fri, "INVESTIERT")[0] == "CASH"
    # H.4.1 fuer w erst am Samstag abgerufen -> Zustand unveraendert
    late = walcl[:17] + [(walcl[17][0], walcl[17][1], f(2026, 10, 3))]
    s, info = E.signal_a(late, tga, rrp, fri, "CASH")
    assert s == "CASH" and "unveraendert" in info["note"]
    old, t_, r_ = _h41(5, w0, 6.6e6, 1000.0)
    assert E.signal_a(old, t_, r_, fri, "INVESTIERT")[0] == "STOPPED"


def _bars(start, n, price=100.0, drift=1.0):
    return [(start + dt.timedelta(days=i), price + drift * i, price + drift * i + 0.5) for i in range(n)]


def test_simulate_fill_next_open_costs_and_benchmark():
    costs = E.cost_scenarios()
    assert costs["maker_plan"]["c_in"] == pytest.approx(0.0047) and costs["taker_K2"]["c_in"] == pytest.approx(0.0101)
    bars = _bars(D(2026, 10, 2), 5)
    sig = lambda d, s: ("INVESTIERT", {}) if d == D(2026, 10, 2) else (s, None)
    r = E.simulate(bars, D(2026, 10, 2), sig, costs)
    fill = [e for e in r["events"] if e["type"] == "fill"][0]
    assert fill["bar"] == "2026-10-03" and fill["price"] == 101.0
    eq = r["equity"]
    assert eq[0]["eq_maker_plan_cash0"] == 1000.0 and eq[0]["position"] == 0
    units = 1000 * (1 - 0.0047) / 101.0
    assert eq[1]["eq_maker_plan_cash0"] == pytest.approx(units * 101.5)
    assert eq[1]["bh_maker_plan"] == pytest.approx(units * 101.5 * (1 - 0.0047))
    assert eq[1]["eq_taker_K2_cash0"] < eq[1]["eq_maker_plan_cash0"]


def test_simulate_gap_fail_closed_and_dtb3():
    bars = _bars(D(2026, 10, 2), 3) + _bars(D(2026, 10, 7), 2)
    r = E.simulate(bars, D(2026, 10, 2), lambda d, s: ("CASH", {}), E.cost_scenarios(),
                   dtb3=[(D(2026, 10, 1), 3.6, f(2026, 10, 2))])
    assert r["status"] == "STOPPED" and "Luecke" in r["stop"]["reason"] and len(r["equity"]) == 3
    assert r["equity"][-1]["eq_maker_plan_dtb3"] > 1000.0 and r["equity"][-1]["eq_maker_plan_cash0"] == 1000.0


def _write_live(tmp, mvrv_rows, bars):
    os.makedirs(tmp / "macro/coinmetrics"); os.makedirs(tmp / "macro/fred"); os.makedirs(tmp / "kraken_ohlc")
    hdr = ["obs_date", "value", "first_fetch_utc", "run_id", "initial_load"]
    with open(tmp / "macro/coinmetrics/btc_CapMVRVCur.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(hdr); w.writerows(mvrv_rows)
    for s in ("WALCL", "WTREGEN", "RRPONTSYD", "DTB3"):
        with open(tmp / f"macro/fred/{s}.csv", "w", newline="") as fh:
            csv.writer(fh).writerow(hdr)
    with open(tmp / "kraken_ohlc/BTCUSD_1d.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["t", "open", "high", "low", "close", "volume", "trades"])
        for d, o, c in bars:
            w.writerow([f"{d}T00:00:00Z", o, max(o, c), min(o, c), c, 1, 1])


def test_runner_disabled_and_freeze_check(tmp_path, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["run_sleeves.py"])
    assert json.load(open(R.CFG))["enabled"] is False
    assert R.main() == 3                                                    # vor Freeze gesperrt
    lst = tmp_path / "fl.txt"; lst.write_text("0" * 64 + "  sleeves/sleeve_engine.py\n")
    monkeypatch.setattr(R.E, "REPO", REPO)
    assert R.check_freeze(str(lst)) == ["sleeves/sleeve_engine.py"]
    monkeypatch.setattr(sys, "argv", ["run_sleeves.py", "--dry-run", "--start", "2026-10-02", "--out", R.OUT])
    assert R.main() == 3                                                    # dry-run nie ins Produktionsverzeichnis


def test_runner_dry_run_outputs_and_revision(tmp_path):
    live = tmp_path / "live"; out = tmp_path / "out"
    mv = [["2026-10-01", "1.5", "2026-10-02T04:15:00Z", "r", "1"], ["2026-10-02", "1.5", "2026-10-03T04:15:00Z", "r", "0"],
          ["2026-10-03", "1.5", "2026-10-04T04:15:00Z", "r", "0"]]
    _write_live(live, mv, _bars(D(2026, 10, 2), 4))
    now = dt.datetime(2026, 10, 6, 5, 0, tzinfo=U)
    rc, st = R.run(str(live), str(out), D(2026, 10, 3), now=now)
    assert st["sleeves"]["B"]["state"] == "INVESTIERT" and st["sleeves"]["B"]["status"] == "OK"
    assert st["sleeves"]["A"]["status"] == "OK" and st["sleeves"]["A"]["state"] is None   # kein Freitag im Fenster
    assert (out / "ledger/equity_daily_B.csv").exists() and rc == 0
    n = len(open(out / "ledger/journal.jsonl").readlines())
    rc2, _ = R.run(str(live), str(out), D(2026, 10, 3), now=now)
    assert rc2 == 0 and len(open(out / "ledger/journal.jsonl").readlines()) == n            # idempotent
    with open(out / "ledger/journal.jsonl", "a") as fh:
        fh.write(json.dumps(dict(sleeve="B", key="signal|2026-10-03|CASH")) + "\n")
    rc3, st3 = R.run(str(live), str(out), D(2026, 10, 3), now=now)
    assert rc3 == 6 and st3["revisions"] == [["B", "signal|2026-10-03|CASH"]]


def test_bericht_section(tmp_path):
    import sleeves_bericht as B
    live = tmp_path / "live"
    L = B.section_lines(D(2026, 10, 5), data_live=str(live), sleeves_out=str(tmp_path / "o"))
    txt = "\n".join(L)
    assert "nicht freigegeben" in txt and "keine Daten" in txt and "Kein Leistungsurteil" in txt
    _write_live(live, [["2026-09-01", "1.5", "2026-09-02T04:15:00Z", "r", "1"]], _bars(D(2026, 10, 2), 2))
    os.makedirs(live / "macro", exist_ok=True)
    json.dump({"fred_macro": {"ok": False, "errors": ["Timeout"], "consecutive_failures": 3, "last_ok_utc": None},
               "coinmetrics_mvrv": {"ok": True}}, open(live / "macro/status.json", "w"))
    txt = "\n".join(B.section_lines(D(2026, 10, 5), data_live=str(live), sleeves_out=str(tmp_path / "o")))
    assert "34 (veraltet)" in txt and "Quellenfehler fred_macro (3x" in txt
    (live / "macro/status.json").write_text("{kaputt")
    assert "## 5b" in B.section_lines(D(2026, 10, 5), data_live=str(live))[0]   # Fehler nie geworfen
