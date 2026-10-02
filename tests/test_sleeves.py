"""Offline-Tests Sleeve A / Leitplanke B (Kandidat v1.0): Signale, As-of ohne Look-ahead, Kosten, fail-closed, Runner-Sperre,
M2-Szenarien (Freitagsabruf gescheitert, H.4.1 verspaetet, RRP fehlt am Mittwoch), Auswertung, gemeinsamer Wochenbericht."""
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
    for s in ("WALCL", "WDTGAL", "RRPONTSYD", "DTB3"):
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
    assert "34 (veraltet)" in txt and "Quellenfehler fred_macro (3x" in txt and "WDTGAL" in txt and "WTREGEN" not in txt
    assert B.SATZ_B_IDENTISCH in txt and "zulässiges Ergebnis" in txt
    (live / "macro/status.json").write_text("{kaputt")
    assert "Sleeve A" in B.section_lines(D(2026, 10, 5), data_live=str(live))[0]   # Fehler nie geworfen


# ------------------------------------------------------------------ M2: Pre-Freeze-Szenarien Sleeve A
FRI = D(2026, 10, 2)          # Signalfreitag, w = Mittwoch 2026-09-30
W0 = D(2026, 6, 3)


def _sat(w):                  # Collector-Abruf Samstag 06:15 Zuerich = 04:15 UTC, nach dem Freitagsschluss
    return dt.datetime.combine(w + dt.timedelta(days=3), dt.time(4, 15), U)


def test_m2_friday_fetch_fails_state_unchanged_then_recovers():
    walcl, tga, rrp = _h41(20, W0, 6.6e6, 1000.0)
    # Freitagsabruf gescheitert: H.4.1 vom Mi 09-30 erst Samstag 04:15 UTC abgerufen (nach Schluss Freitagsbar)
    walcl[17] = (walcl[17][0], walcl[17][1], _sat(walcl[17][0])); tga[17] = (tga[17][0], tga[17][1], _sat(tga[17][0]))
    s, info = E.signal_a(walcl, tga, rrp, FRI, "CASH")
    assert s == "CASH" and "unveraendert" in info["note"]          # keine Nachbuchung, kein STOPPED
    # Folgefreitag: neue Woche normal verfuegbar -> Signal wieder regulaer (Daten vom 09-30 jetzt sichtbar, kein Look-ahead)
    s2, info2 = E.signal_a(walcl, tga, rrp, FRI + dt.timedelta(days=7), "CASH")
    assert s2 == "INVESTIERT" and info2["now"]["w"] == "2026-10-07"
    # in der Simulation: NL bricht ab Mi 09-30 ein; Abruf am Fr 10-02 gescheitert -> Wechsel erst Fr 10-09, Fill Sa 10-10
    wl = [(w, v - (60000.0 if i >= 17 else 0.0), ff) for i, (w, v, ff) in enumerate(walcl)]
    bars = _bars(D(2026, 9, 25), 17)
    r = E.simulate(bars, D(2026, 9, 25), lambda d, st: E.signal_a(wl, tga, rrp, d, st), E.cost_scenarios())
    sig = [(e["bar"], e["state"]) for e in r["events"] if e["type"] == "signal"]
    fills = [(e["bar"], e["side"]) for e in r["events"] if e["type"] == "fill"]
    assert r["status"] == "OK" and sig == [("2026-09-25", "INVESTIERT"), ("2026-10-09", "CASH")]
    assert fills == [("2026-09-26", "kauf"), ("2026-10-10", "verkauf")]


def test_m2_h41_late_or_shifted():
    walcl, tga, rrp = _h41(20, W0, 6.6e6, 1000.0)
    # a) H.4.1 verschoben (Feiertag): Veroeffentlichung Freitag 21:00 UTC, Abruf vor Bar-Schluss -> verwendet
    fr21 = dt.datetime(2026, 10, 2, 21, 0, tzinfo=U)
    a_w = walcl[:17] + [(walcl[17][0], walcl[17][1], fr21)] + walcl[18:]
    a_t = tga[:17] + [(tga[17][0], tga[17][1], fr21)] + tga[18:]
    s, info = E.signal_a(a_w, a_t, rrp, FRI, "CASH")
    assert s == "INVESTIERT" and info["now"]["w"] == "2026-09-30"
    # b) H.4.1 verspaetet bis nach dem Freitagsschluss: Zustand unveraendert, auch INVESTIERT bleibt INVESTIERT
    late = dt.datetime(2026, 10, 3, 0, 0, tzinfo=U)                 # genau Bar-Schluss: nicht < cut
    b_w = walcl[:17] + [(walcl[17][0], walcl[17][1], late)]
    assert E.signal_a(b_w, tga, rrp, FRI, "INVESTIERT")[0] == "INVESTIERT"
    walcl_dn, tga_dn, rrp_dn = _h41(20, W0, 6.6e6, -1000.0)
    b_dn = walcl_dn[:17] + [(walcl_dn[17][0], walcl_dn[17][1], late)]
    s, info = E.signal_a(b_dn, tga_dn, rrp_dn, FRI, "INVESTIERT")
    assert s == "INVESTIERT" and "unveraendert" in info["note"]       # fallendes NL wird NICHT vorweggenommen
    # c) Stichtag verschoben (Beobachtung auf Donnerstag datiert statt Mittwoch): kein exakter Mittwoch -> unveraendert
    c_w = walcl[:17] + [(walcl[17][0] + dt.timedelta(days=1), walcl[17][1], walcl[17][2])]
    assert E.signal_a(c_w, tga, rrp, FRI, "CASH")[0] == "CASH"
    # d) verspaetete Woche wird spaeter als Lag-Wert korrekt genutzt (13 Wochen spaeter sichtbar)
    s, info = E.signal_a(b_w + walcl[18:], tga, rrp, FRI + dt.timedelta(days=7), "CASH")
    assert s == "INVESTIERT"
    # e) H.4.1 >= 8 Wochen ohne neue Werte -> STOPPED (Betriebs-Kill)
    assert E.signal_a(walcl[:8], tga[:8], rrp[:8], FRI, "CASH")[0] == "STOPPED"


def test_m2_rrp_missing_on_wednesday():
    walcl, tga, rrp = _h41(20, W0, 6.6e6, 1000.0)
    w = D(2026, 9, 30); tue = w - dt.timedelta(days=1)
    rrp2 = [x for x in rrp if x[0] != w] + [(tue, 25.0, f(2026, 9, 29, 23))]
    rrp2.sort(key=lambda x: x[0])
    s, info = E.signal_a(walcl, tga, rrp2, FRI, None)
    assert info["now"]["rrp_obs"] == "2026-09-29" and info["now"]["rrp"] == 25.0      # letzter Wert vor Mittwoch
    assert info["nl"] == pytest.approx(walcl[17][1] - 800000.0 - 25000.0)
    # Mittwochswert existiert, aber erst nach Bar-Schluss abgerufen -> ebenfalls Dienstagswert
    rrp3 = rrp2 + [(w, 99.0, dt.datetime(2026, 10, 3, 4, 15, tzinfo=U))]; rrp3.sort(key=lambda x: x[0])
    assert E.signal_a(walcl, tga, rrp3, FRI, None)[1]["now"]["rrp"] == 25.0
    # RRP ganz weg seit > 8 Wochen -> STOPPED
    assert E.signal_a(walcl, tga, [x for x in rrp if x[0] < D(2026, 7, 20)], FRI, "CASH")[0] == "STOPPED"


def test_tga_series_is_wdtgal_and_stale_tga_stops():
    assert E.TGA_SERIES == "WDTGAL" and E.FRED_A == ("WALCL", "WDTGAL", "RRPONTSYD")
    walcl, tga, rrp = _h41(20, W0, 6.6e6, 1000.0)
    s, info = E.signal_a(walcl, tga[:8], rrp, FRI, "CASH")
    assert s == "STOPPED" and "WDTGAL" in info["reason"]


# ------------------------------------------------------------------ Start, Cash, Benchmarks
def test_start_in_valid_state_entry_with_costs():
    walcl, tga, rrp = _h41(20, W0, 6.6e6, 1000.0)
    bars = _bars(FRI, 4)
    costs = E.cost_scenarios()
    r = E.simulate(bars, FRI, lambda d, st: E.signal_a(walcl, tga, rrp, d, st), costs)
    sig = [e for e in r["events"] if e["type"] == "signal"]
    assert sig[0]["bar"] == "2026-10-02" and sig[0]["state"] == "INVESTIERT" and sig[0]["prev"] is None  # kein Kreuzungsereignis
    eq = r["equity"]
    units = 1000 * (1 - costs["maker_plan"]["c_in"]) / bars[1][1]
    assert eq[1]["eq_maker_plan_dtb3"] == pytest.approx(units * bars[1][2])                           # Einstieg mit Kosten
    assert eq[1]["eq_taker_K2_dtb3"] == pytest.approx(1000 * (1 - costs["taker_K2"]["c_in"]) / bars[1][1] * bars[1][2])
    assert R.start_ok(FRI) and not R.start_ok(FRI + dt.timedelta(days=1)) and not R.start_ok(None)


def test_cash_dtb3_primary_and_b2():
    assert (E.PRIMARY_CASH, E.SENS_CASH) == ("dtb3", "cash0")
    bars = _bars(D(2026, 10, 2), 10)
    r = E.simulate(bars, D(2026, 10, 2), lambda d, s: ("CASH", {}), E.cost_scenarios(), dtb3=[(D(2026, 10, 1), 3.6, f(2026, 10, 2))])
    last = r["equity"][-1]
    assert last["eq_maker_plan_dtb3"] == pytest.approx(1000 * (1 + 0.036 / 360) ** 10)
    assert last["b2_dtb3"] == pytest.approx(last["eq_maker_plan_dtb3"]) and last["eq_maker_plan_cash0"] == 1000.0


def test_b_identical_to_buy_and_hold_while_mvrv_le_35():
    import auswertung as A
    bars = _bars(D(2026, 10, 2), 10)
    mvrv = [(D(2026, 10, 1) + dt.timedelta(days=i), 3.5, f(2026, 10, 2 + i)) for i in range(10)]   # genau 3.5: kein Ausstieg
    costs = E.cost_scenarios()
    r = E.simulate(bars, D(2026, 10, 2), lambda d, s: E.signal_b(mvrv, d, s), costs)
    for row in r["equity"][1:]:
        for sc in costs:
            assert row[f"eq_{sc}_dtb3"] * (1 - costs[sc]["c_out"]) == pytest.approx(row[f"bh_{sc}"])  # gleiche Menge BTC
    assert A.b_identisch_bh(r["equity"])
    hi = mvrv[:5] + [(D(2026, 10, 6), 3.6, f(2026, 10, 7))]
    r2 = E.simulate(bars, D(2026, 10, 2), lambda d, s: E.signal_b(hi, d, s), costs)
    assert not A.b_identisch_bh(r2["equity"]) and r2["state"] == "CASH"


def test_metrics_calmar_ulcer_and_regime_phases():
    eq = [dict(v=x) for x in [100.0] * 200 + [90.0] * 100 + [120.0] * 100]
    m = E.metrics(eq, "v")
    assert m["maxdd_pct"] == pytest.approx(-10.0) and m["calmar"] == pytest.approx(m["cagr_pct"] / 10.0, rel=1e-3)
    assert m["ulcer"] == pytest.approx((100 * 10.0 ** 2 / 400) ** 0.5)
    pos = [dict(position=p) for p in [1] * 92 + [0] * 91 + [1] * 120]
    ph = E.regime_phases(pos)
    assert ph == dict(phasen=3, laenger_13w=2, laengen=[92, 91, 120])                               # 91 Tage = genau 13 Wochen


# ------------------------------------------------------------------ Auswertung A (M4, M5), Leitplanke B
def test_auswertung_gates_redundancy_verdict():
    import auswertung as A
    assert A.ALPHA_A == 0.05 and A.REDUNDANZ_KORR == 0.7 and A.LEITPLANKE_B["gates"] is None and A.LEITPLANKE_B["trial"] is False
    s = dict(sharpe=1.0, maxdd_pct=-30.0, cagr_pct=20.0); b1 = dict(sharpe=0.8, maxdd_pct=-60.0, cagr_pct=25.0)
    b2 = dict(sharpe=None, maxdd_pct=0.0, cagr_pct=4.0)
    g = A.gates_a(s, b1, b2, s, b1)
    assert g == dict(G1=True, G2=True, G3=True, G4=True)
    assert A.gates_a(dict(s, maxdd_pct=-41.0), b1, b2, s, b1)["G2"] is False
    assert A.gates_a(s, b1, b2, dict(s, sharpe=0.7), b1)["G4"] is False
    assert A.korrelation([0, 1, 1, 0], [0, 1, 1, 0]) == pytest.approx(1.0) and A.korrelation([1, 1], [0, 1]) is None
    # M4: redundant nur bei allen Gates, Korrelation > 0.7 und Sharpe A <= Sharpe W2-BTC
    assert A.redundant_a(True, 0.71, 1.0, 1.0) and not A.redundant_a(True, 0.70, 0.5, 1.0)
    assert not A.redundant_a(True, 0.9, 1.01, 1.0) and not A.redundant_a(False, 0.9, 0.5, 1.0) and not A.redundant_a(True, None, 0.5, 1.0)
    v = lambda **k: A.verdict_a(**{**dict(gates=g, p_wert=0.04, n_wechsel=12, jahre=3.1, frist_erreicht=False, korr=0.5,
                                         sharpe_a_cash0=1.0, sharpe_w2=0.9), **k})
    assert v() == "EMPFEHLUNG_MICRO_LIVE"
    assert v(p_wert=0.05) == "EMPFEHLUNG_MICRO_LIVE" and v(p_wert=0.051) == "NICHT_SIGNIFIKANT"   # M5: allein auf 5 %, kein Holm
    assert v(korr=0.8, sharpe_w2=1.2) == "REDUNDANT"
    assert v(gates=dict(g, G3=False)) == "VERWORFEN"
    assert v(n_wechsel=9) == "NOCH_NICHT_FAELLIG" and v(n_wechsel=9, frist_erreicht=True) == "NICHT_PRUEFBAR"


# ------------------------------------------------------------------ M3: gemeinsamer einseitiger Wochenbericht
def _wb():
    sys.path.insert(0, os.path.join(REPO, "paper"))
    import wochenbericht as WB
    return WB


def _heads(L):
    return [l for l in L if l.startswith("## ")]


def _isolate(monkeypatch, tmp_path):
    for k in ("AURUM_PAPER_OUT", "AURUM_VOLTARGET_OUT"):
        monkeypatch.setenv(k, str(tmp_path / k.lower()))


def test_m3_weekly_report_fixed_layout_without_data(tmp_path, monkeypatch):
    WB = _wb(); monkeypatch.setattr(WB, "dtb3", lambda out: None); _isolate(monkeypatch, tmp_path)
    monkeypatch.setenv("AURUM_DATA_LIVE", str(tmp_path / "live")); monkeypatch.setenv("AURUM_SLEEVES_OUT", str(tmp_path / "so"))
    L = WB.build(str(tmp_path / "leer"), D(2026, 10, 12))
    assert _heads(L) == list(WB.LAYOUT) and len(L) <= WB.MAX_ZEILEN
    txt = "\n".join(L)
    assert "Wochenbericht" in txt and "nicht lesbar" in txt and "nicht freigegeben" in txt
    assert "**ALARM** Collector" in txt and "**ALARM** PAPER v1.0" in txt and "Heartbeat-Alarm" in txt   # keine Laeufe
    assert "VOLTARGET" in txt and "| T55_20 |" in txt
    assert "identisch mit Buy and Hold" in txt and "zulässiges Ergebnis" in txt and "ß" not in txt


def test_m3_weekly_report_with_sleeve_state(tmp_path, monkeypatch):
    WB = _wb(); import sleeves_bericht as SB
    monkeypatch.setattr(WB, "dtb3", lambda out: None); _isolate(monkeypatch, tmp_path)
    live, so = tmp_path / "live", tmp_path / "so"
    _write_live(live, [["2026-10-10", "2.10", "2026-10-11T04:15:00Z", "r", "0"]], _bars(D(2026, 10, 2), 2))
    os.makedirs(so / "state")
    json.dump(dict(run_utc="2026-10-12T04:30:00+00:00", rc=0, sleeves=dict(
        A=dict(status="OK", state="INVESTIERT", n_wechsel=1, equity_last=dict(eq_maker_plan_dtb3=1012.0, eq_taker_K2_dtb3=1006.0, bh_maker_plan=1020.0),
               regimephasen=dict(phasen=1, laenger_13w=0)),
        B=dict(status="OK", state="INVESTIERT", identisch_bh=True))), open(so / "state/state_latest.json", "w"))
    cfg = dict(json.load(open(SB.CFG)), enabled=True, start_bar="2026-10-02")
    monkeypatch.setattr(SB, "_cfg", lambda: cfg)
    monkeypatch.setenv("AURUM_DATA_LIVE", str(live)); monkeypatch.setenv("AURUM_SLEEVES_OUT", str(so))
    out = tmp_path / "paper"; os.makedirs(out / "state"); os.makedirs(out / "logs"); os.makedirs(out / "ledger")
    json.dump(dict(start_bar="2026-10-02", prereg_sha256="626fd035f237", coins={"BTC": {"last_bar": "2026-10-11"}},
                   strategies={"W2": {c: dict(position=dict(entry_date="2026-10-05", stop=1.0), order_next_open=None,
                                                    scenarios=dict(maker_plan=dict(costs_usd=4.7))) for c in "ABCDEFGHIJ"}}),
              open(out / "state/state_latest.json", "w"))
    (out / "logs/run_history.jsonl").write_text(json.dumps(dict(started_utc="2026-10-11T04:20:00Z", ok=True, errors=[])) + "\n")
    L = WB.build(str(out), D(2026, 10, 12))
    txt = "\n".join(L)
    assert _heads(L) == list(WB.LAYOUT) and len(L) <= WB.MAX_ZEILEN
    assert "| A | OK | INVESTIERT | 1'012 (1'006) | 1'020 | 1 | 0 von 1 |" in txt
    assert "| B | OK | INVESTIERT | 2.10 (2026-10-10) | +1.40 | ja |" in txt
    assert "… und 4 weitere" in txt and "Läufe der letzten 7 Tage 1, davon erfolgreich 1" in txt
