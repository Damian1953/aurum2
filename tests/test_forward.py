"""Offline-Tests gemeinsamer Heartbeat (forward/heartbeat.py) und VOLTARGET-Abschnitt (forward/voltarget_bericht.py)
des einseitigen Wochenberichts. Kein Netz, kein cron, keine Laeufe."""
import datetime as dt, json, os, sys
import pytest
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "forward"))
import heartbeat as H
import voltarget_bericht as VB

U = dt.timezone.utc
NOW = dt.datetime(2026, 10, 12, 6, 0, tzinfo=U)


def _hist(p, rows):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")


def _cfg(p, enabled):
    json.dump(dict(enabled=enabled), open(p, "w")); return str(p)


def test_heartbeat_one_line_per_runner_and_alarms(tmp_path):
    ok_t = (NOW - dt.timedelta(hours=2)).isoformat()
    _hist(tmp_path / "c.jsonl", [dict(started_utc="2026-10-01T04:15:01Z", ok=True), dict(started_utc=ok_t.replace("+00:00", "Z"), ok=True)])
    _hist(tmp_path / "p.jsonl", [dict(started_utc="2026-10-10T04:50:00+00:00", ok=True)])            # 49 h alt -> Lauf fehlt
    _hist(tmp_path / "s.jsonl", [dict(run_utc=ok_t, rc=7)])                                            # fehlgeschlagen
    entries = [("Collector", str(tmp_path / "c.jsonl"), None), ("PAPER v1.0", str(tmp_path / "p.jsonl"), None),
               ("Sleeves A/B", str(tmp_path / "s.jsonl"), _cfg(tmp_path / "s.json", True)),
               ("VOLTARGET", str(tmp_path / "v.jsonl"), _cfg(tmp_path / "v.json", True)),                # nie gelaufen
               ("Inaktiv", str(tmp_path / "x.jsonl"), _cfg(tmp_path / "x.json", False)),
               ("Fehlt", str(tmp_path / "y.jsonl"), str(tmp_path / "gibtsnicht.json"))]
    r = {x["name"]: x for x in H.check(NOW, entries)}
    assert len(r) == 6
    assert r["Collector"]["status"] == "OK" and not r["Collector"]["alarm"] and "Zürich" in r["Collector"]["text"]
    assert r["PAPER v1.0"]["alarm"] and "Lauf fehlt" in r["PAPER v1.0"]["text"]
    assert r["Sleeves A/B"]["alarm"] and "fehlgeschlagen" in r["Sleeves A/B"]["text"]
    assert r["VOLTARGET"]["alarm"] and "kein Lauf protokolliert" in r["VOLTARGET"]["text"]
    assert r["Inaktiv"]["status"] == "INAKTIV" and not r["Inaktiv"]["alarm"]
    assert r["Fehlt"]["status"] == "INAKTIV" and "nicht vorhanden" in r["Fehlt"]["text"]
    # Grenze 26 h: genau 26 h alt ist noch ok, 26.1 h Alarm
    _hist(tmp_path / "g.jsonl", [dict(started_utc=(NOW - dt.timedelta(hours=26)).isoformat(), ok=True)])
    assert not H.check(NOW, [("G", str(tmp_path / "g.jsonl"), None)])[0]["alarm"]
    _hist(tmp_path / "g.jsonl", [dict(started_utc=(NOW - dt.timedelta(hours=26, minutes=6)).isoformat(), ok=True)])
    assert H.check(NOW, [("G", str(tmp_path / "g.jsonl"), None)])[0]["alarm"]


def test_heartbeat_registry_covers_all_forward_lines_and_no_cron():
    names = [n for n, _, _ in H.runners()]
    assert names == ["Collector", "PAPER v1.0", "Sleeves A/B", "VOLTARGET"]
    sched = open(os.path.join(REPO, "collector", "ensure_scheduler.sh")).read()
    assert "heartbeat" not in sched and "voltarget" not in sched.lower()


def test_heartbeat_main_exit_code(tmp_path, monkeypatch):
    monkeypatch.setattr(H, "runners", lambda: [("X", str(tmp_path / "none.jsonl"), None)])
    assert H.main() == 1
    _hist(tmp_path / "ok.jsonl", [dict(run_utc=dt.datetime.now(U).isoformat(), rc=0)])
    monkeypatch.setattr(H, "runners", lambda: [("X", str(tmp_path / "ok.jsonl"), None)])
    assert H.main() == 0


def test_voltarget_section_fixed_layout(tmp_path, monkeypatch):
    L = VB.section(dt.date(2026, 10, 12), vt_out=str(tmp_path))
    assert len(L) == 2 + 3 + 2 and [l.split(" | ")[0] for l in L[2:5]] == ["| W2", "| W6", "| T55_20"]
    cfg = tmp_path / "vc.json"; json.dump(dict(enabled=True, start_bar="2026-11-06"), open(cfg, "w"))
    monkeypatch.setattr(VB, "CFG", str(cfg))
    os.makedirs(tmp_path / "state")
    json.dump(dict(rc=0, run_utc="2026-10-12T05:00:00+00:00",
                   summary=dict(W2=dict(status="OK", coins_ok=10, coins_total=10, tage_offen=40, tage_offen_s_lt_1=12, sync_kosten_usd=9.4)),
                   s_verteilung=dict(BTC=dict(tage=7, tage_s_lt_1=3, s_min=0.712), ETH=dict(tage=7, tage_s_lt_1=0, s_min=1.0))),
              open(tmp_path / "state/state_latest.json", "w"))
    txt = "\n".join(VB.section(dt.date(2026, 10, 12), vt_out=str(tmp_path)))
    assert "| W2 | OK | 10/10 | 40 | 12 | 9.40 |" in txt and "| W6 | keine Daten |" in txt
    assert "BTC 3/7 (min 0.71), ETH 0/7 (min 1.0)" in txt
    (tmp_path / "state/state_latest.json").write_text("{kaputt")
    assert "nicht lesbar" in "\n".join(VB.section(dt.date(2026, 10, 12), vt_out=str(tmp_path)))   # nie geworfen
