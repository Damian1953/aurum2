"""Offline-Tests des Schreibpfads des Collectors (kein Netz)."""
import json, os, sys
import pytest
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "collector"))
import collect as C

H = ["t", "open", "high", "low", "close", "volume", "trades"]


@pytest.fixture
def store(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "OUT", str(tmp_path))
    return C.Store("testrun", C.Prov("testrun"))


def bar(t, c="10"):
    return [t, "10", "11", "9", c, "1.5", "3"]


def test_append_dedup_and_prefix(store, tmp_path):
    r1 = store.append("k/x.csv", H, [bar("2026-01-01T00:00:00Z"), bar("2026-01-01T01:00:00Z")], C.validate_ohlc, "t", {})
    old = open(tmp_path / "k/x.csv", "rb").read()
    r2 = store.append("k/x.csv", H, [bar("2026-01-01T01:00:00Z"), bar("2026-01-01T02:00:00Z")], C.validate_ohlc, "t", {})
    assert (r1["new"], r2["new"], r2["unchanged"], r2["total"]) == (2, 1, 1, 3)
    assert open(tmp_path / "k/x.csv", "rb").read().startswith(old)


def test_conflict_not_overwritten(store, tmp_path):
    store.append("k/x.csv", H, [bar("2026-01-01T00:00:00Z", "10")], C.validate_ohlc, "t", {})
    r = store.append("k/x.csv", H, [bar("2026-01-01T00:00:00Z", "10.5")], C.validate_ohlc, "t", {})
    assert r["conflicts"] == 1 and r["new"] == 0
    assert "10.5" not in open(tmp_path / "k/x.csv").read()
    assert json.loads(open(tmp_path / "conflicts.jsonl").readline())["key"] == "2026-01-01T00:00:00Z"


def test_critical_batch_quarantined(store, tmp_path):
    bad = [bar("2026-01-01T00:00:00Z"), [ "2026-01-01T01:00:00Z", "10", "11", "9", "12", "1", "1"]]  # close > high
    with pytest.raises(ValueError):
        store.append("k/x.csv", H, bad, C.validate_ohlc, "t", {})
    assert not (tmp_path / "k/x.csv").exists()
    assert any(p.name.endswith(".reason.txt") for p in (tmp_path / "_quarantine").iterdir())


def test_non_monotonic_and_bad_dates_are_critical():
    assert C.validate_ohlc([bar("2026-01-01T01:00:00Z"), bar("2026-01-01T00:00:00Z")])
    assert C.validate_ohlc([bar("2026-01-01")])
    assert C.validate_ohlc([bar("2099-01-01T00:00:00Z")])


def test_main_nonzero_exit_and_status_on_failure(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "OUT", str(tmp_path))
    def boom(store, args):
        raise RuntimeError("Netz weg")
    monkeypatch.setattr(C, "SOURCES", {"x": boom, "y": lambda s, a: ({"ok": 1}, [])})
    monkeypatch.setattr(sys, "argv", ["collect.py"])
    assert C.main() == 1
    st = json.load(open(tmp_path / "last_run_status.json"))
    assert st["ok"] is False and st["sources"]["x"]["ok"] is False and st["sources"]["y"]["ok"] is True
    assert "Netz weg" in st["errors"][0]


# ------------------------------------------------------------------ ab 1.1: Kraken Futures / Spot Ticker (offline, http gemockt)
def _fake_http(payloads):
    def f(url, method="GET", **kw):
        for k, v in payloads.items():
            if k in url:
                return 200, json.dumps(v).encode()
        raise AssertionError(url)
    return f


def _fut_payload(server="2026-09-01T10:00:00.123Z", n=60, vol=3e6):
    inst = [dict(symbol=f"PF_C{i}USD", type="flexible_futures", tradeable=True, base=f"C{i}", quote="USD", openingDate="2022-03-22T00:00:00Z") for i in range(n)]
    inst += [dict(symbol="FF_XBTUSD_261225", type="flexible_futures", tradeable=True)]  # Termin, wird ignoriert
    tick = [dict(symbol=f"PF_C{i}USD", tag="perpetual", suspended=False, volumeQuote=vol, vol24h=10.0, openInterest=5.0, last=1.5,
                 lastTime="2026-10-01T09:59:00Z", markPrice=1.5) for i in range(n)]
    tick += [dict(symbol="FF_XBTUSD_261225", tag="quarter", volumeQuote=1.0)]
    return {"v3/instruments": dict(result="success", serverTime=server, instruments=inst),
            "v3/tickers": dict(result="success", serverTime=server, tickers=tick)}


def test_kraken_futures_tickers_snapshot_dedup(store, tmp_path, monkeypatch):
    monkeypatch.setattr(C, "http", _fake_http(_fut_payload()))
    res, errs = C.src_kraken_futures_tickers(store, None)
    assert not errs and res["_summary"]["symbols_written"] == 60 and res["_summary"]["ge_2m_usd"] == 60
    assert not (tmp_path / "kraken_futures_tickers" / "FF_XBTUSD_261225.csv").exists()
    f = tmp_path / "kraken_futures_tickers" / "PF_C0USD.csv"
    hdr, row = open(f).read().splitlines()
    assert hdr.split(",") == C.KFT_HDR and row.startswith("2026-09-01T10:00:00Z,1,0,3000000.0,10.0,5.0,1.5,")
    res2, _ = C.src_kraken_futures_tickers(store, None)  # gleiche Antwort -> keine neue Zeile, Snapshot nicht dupliziert
    assert res2["PF_C0USD"] == dict(new=0, total=1)
    assert sorted(p.name for p in (tmp_path / "kraken_futures_instruments").iterdir()) == ["first_seen.csv", "snapshot_2026-09-01.csv"]
    monkeypatch.setattr(C, "http", _fake_http(_fut_payload(server="2026-09-02T10:00:00Z", vol=1e6)))
    old = open(f, "rb").read()
    C.src_kraken_futures_tickers(store, None)
    assert open(f, "rb").read().startswith(old) and len(open(f).read().splitlines()) == 3


def test_kraken_futures_tickers_bad_symbol_quarantined_others_written(store, tmp_path, monkeypatch):
    p = _fut_payload(); p["v3/tickers"]["tickers"][0]["volumeQuote"] = -5
    monkeypatch.setattr(C, "http", _fake_http(p))
    res, errs = C.src_kraken_futures_tickers(store, None)
    assert len(errs) == 1 and "PF_C0USD" in errs[0] and res["_summary"]["symbols_written"] == 59
    assert not (tmp_path / "kraken_futures_tickers" / "PF_C0USD.csv").exists()


def test_kraken_futures_tickers_implausible_listing_fails(store, monkeypatch):
    monkeypatch.setattr(C, "http", _fake_http(_fut_payload(n=5)))
    with pytest.raises(ValueError):
        C.src_kraken_futures_tickers(store, None)


def test_kraken_spot_tickers(store, tmp_path, monkeypatch):
    v = {"a": ["1", "1", "1"], "b": ["1", "1", "1"], "c": ["100.5", "0.1"], "v": ["5", "20"], "p": ["99", "100"], "t": [10, 42]}
    monkeypatch.setattr(C, "http", _fake_http({"Ticker": dict(error=[], result={"XXBTZUSD": v})}))
    monkeypatch.setattr(C.time, "sleep", lambda s: None)
    res, errs = C.src_kraken_spot_tickers(store, None)
    assert not errs and res["BTCUSD"]["vol24h_usd"] == 2000
    row = open(tmp_path / "kraken_spot_tickers" / "BTCUSD.csv").read().splitlines()[1].split(",")
    assert row[1:] == ["100.5", "20.0", "100.0", "2000.0", "42"]
