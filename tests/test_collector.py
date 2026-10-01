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
