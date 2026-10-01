"""Offline-Tests Collector 1.2 Makro-Quellen (First-Release, Revisionen, Validierung). Kein Netz."""
import csv, datetime as dt, json, os, sys
import pytest
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "collector"))
import collect as C
import macro_sources as M

TODAY = dt.date(2026, 10, 1)


@pytest.fixture
def store(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "OUT", str(tmp_path))
    return C.Store("run1", C.Prov("run1"))


def rows(p):
    return list(csv.DictReader(open(p)))


def test_first_release_kept_and_revision_logged(store, tmp_path):
    rel = "macro/fred/WALCL.csv"
    M.append_first_release(store, rel, "WALCL", [("2026-09-23", "6747704"), ("2026-09-30", "6743031")], "2026-10-01T20:50:00Z", "t", {}, TODAY)
    store.run_id = "run2"
    r = M.append_first_release(store, rel, "WALCL", [("2026-09-30", "6743999"), ("2026-10-07", "6740000")], "2026-10-09T04:15:00Z", "t", {}, dt.date(2026, 10, 9))
    assert (r["new"], r["revisions"]) == (1, 1)
    rs = rows(tmp_path / rel)
    assert [x["value"] for x in rs] == ["6747704", "6743031", "6740000"]          # First-Release bleibt
    assert [x["initial_load"] for x in rs] == ["1", "1", "0"]
    assert rs[2]["first_fetch_utc"] == "2026-10-09T04:15:00Z" and rs[1]["first_fetch_utc"] == "2026-10-01T20:50:00Z"
    rev = [json.loads(l) for l in open(tmp_path / "macro/revisions.jsonl")]
    assert rev[0]["obs_date"] == "2026-09-30" and rev[0]["first_release"] == "6743031"
    M.append_first_release(store, rel, "WALCL", [("2026-09-30", "6743999")], "2026-10-10T04:15:00Z", "t", {}, dt.date(2026, 10, 10))
    assert len(open(tmp_path / "macro/revisions.jsonl").readlines()) == 1        # gleiche Revision nur einmal


def test_out_of_range_quarantined(store, tmp_path):
    with pytest.raises(ValueError):
        M.append_first_release(store, "macro/coinmetrics/btc_CapMVRVCur.csv", "CapMVRVCur", [("2026-09-29", "1.5"), ("2026-09-30", "55")],
                               "2026-10-01T04:15:00Z", "t", {}, TODAY)
    assert not (tmp_path / "macro/coinmetrics/btc_CapMVRVCur.csv").exists()
    assert M.validate_obs("CapMVRVCur", [("2026-10-05", "1.5")], TODAY)       # Zukunft
    assert M.validate_obs("CapMVRVCur", [("2026-09-30", "1.5"), ("2026-09-29", "1.4")], TODAY)  # nicht monoton


def test_parsers():
    obs, miss = M.parse_fredgraph("RRPONTSYD", b"observation_date,RRPONTSYD\n2026-09-29,11.446\n2026-09-30,.\n2026-10-01,0.350\n")
    assert obs == [("2026-09-29", "11.446"), ("2026-10-01", "0.350")] and miss == 1
    with pytest.raises(ValueError):
        M.parse_fredgraph("WALCL", b"DATE,OTHER\n")
    body = json.dumps({"data": [{"asset": "btc", "time": "2026-09-30T00:00:00.000000000Z", "CapMVRVCur": "1.55"}]}).encode()
    assert M.parse_coinmetrics(body) == [("2026-09-30", "1.55")]
    with pytest.raises(ValueError):
        M.parse_coinmetrics(json.dumps({"data": [], "next_page_token": "x"}).encode())


def test_src_fred_macro_with_stub(store, tmp_path, monkeypatch):
    monkeypatch.setattr(C, "utcnow", lambda: dt.datetime(2026, 10, 2, 4, 15, tzinfo=dt.timezone.utc))
    data = {"WALCL": "6743031", "WTREGEN": "850000", "RRPONTSYD": "11.5", "DTB3": "3.9"}
    def getter(url):
        sid = url.split("id=")[1].split("&")[0]
        if sid == "DTB3":
            raise TimeoutError("kein Netz")
        return 200, f"observation_date,{sid}\n2026-09-30,{data[sid]}\n".encode()
    res, errs = M.src_fred_macro(store, None, getter=getter)
    assert set(res) == {"WALCL", "WTREGEN", "RRPONTSYD"} and len(errs) == 1 and "DTB3" in errs[0]
    r = rows(tmp_path / "macro/fred/WALCL.csv")[0]
    assert r["first_fetch_utc"] == "2026-10-02T04:15:00Z" and r["run_id"] == "run1"
    assert any(p.name == "run1.csv" for p in (tmp_path / "macro/_raw/fred_WALCL").iterdir())


def test_sources_registered():
    assert "coinmetrics_mvrv" in C.SOURCES and "fred_macro" in C.SOURCES and C.VERSION == "1.2"
