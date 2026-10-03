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
    ok_t = (NOW - dt.timedelta(hours=1)).isoformat()                     # 07:00 Zuerich, nach allen Fahrplanterminen
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


def _box_pause_entries(tmp_path, day2_runs):
    """Laeufe am 02.10. planmaessig (06:15/06:50/06:55/07:00 Zuerich), am 03.10. nur die angegebenen."""
    z = H.ZH
    def at(d, hm):
        return dt.datetime(2026, 10, d, *map(int, hm.split(":")), tzinfo=z).astimezone(U).isoformat()
    ent = []
    for name, hm in H.SCHEDULE.items():
        rows = [dict(run_utc=at(2, hm), rc=0)] + ([dict(run_utc=at(3, day2_runs[name]), rc=0)] if name in day2_runs else [])
        f = tmp_path / f"{len(ent)}.jsonl"; _hist(f, rows)
        ent.append((name, str(f), _cfg(tmp_path / f"{len(ent)}.json", True)))
    return ent


def test_heartbeat_alarms_when_todays_scheduled_run_missing_box_pause(tmp_path):
    """Vorfall 2026-10-03: cron hat 06:15-07:00 ausgelassen, Vortagslaeufe ~25 h alt; um 07:30 muss ALARM kommen."""
    now = dt.datetime(2026, 10, 3, 7, 30, tzinfo=H.ZH).astimezone(U)
    r = H.check(now, _box_pause_entries(tmp_path, {}))
    assert all(x["alarm"] for x in r) and all("Lauf fehlt (faellig 2026-10-03" in x["text"] for x in r)
    assert all(x["alter_h"] < H.MAX_AGE_H for x in r)                      # die alte 26-h-Regel haette OK gemeldet
    # nach dem Nachholen (07:40 bis 08:02) ist alles OK
    r = H.check(dt.datetime(2026, 10, 3, 8, 30, tzinfo=H.ZH).astimezone(U),
                _box_pause_entries(tmp_path, {"Collector": "07:38", "PAPER v1.0": "08:02", "Sleeves A/B": "08:02", "VOLTARGET": "08:02"}))
    assert not any(x["alarm"] for x in r)
    # vor Ablauf der Karenz (06:30 < 06:15 + 20 min) zaehlt noch der Vortag; danach Alarm
    e = _box_pause_entries(tmp_path, {})
    assert not H.check(dt.datetime(2026, 10, 3, 6, 30, tzinfo=H.ZH).astimezone(U), e[:1])[0]["alarm"]
    assert H.check(dt.datetime(2026, 10, 3, 6, 36, tzinfo=H.ZH).astimezone(U), e[:1])[0]["alarm"]
    # ein Lauf vor dem Termin (z. B. 05:00) zaehlt nicht fuer heute
    f = tmp_path / "frueh.jsonl"; _hist(f, [dict(started_utc="2026-10-03T03:00:00Z", ok=True)])
    assert H.check(now, [("Collector", str(f), None)])[0]["alarm"]
    assert H.last_due(now, "06:15") == dt.datetime(2026, 10, 3, 4, 15, tzinfo=U)


def test_missed_run_is_fehler_not_ok_and_cron_daemon_check(tmp_path, monkeypatch):
    now = dt.datetime(2026, 10, 3, 7, 30, tzinfo=H.ZH).astimezone(U)
    r = H.check(now, _box_pause_entries(tmp_path, {}))
    assert all(x["status"] == "FEHLER" and "FEHLER, letzter Lauf" in x["text"] and "OK" not in x["text"] for x in r)
    assert H.cron_status(lambda: True) == dict(alarm=False, text="- OK cron-Daemon: läuft.")
    c = H.cron_status(lambda: False); assert c["alarm"] and "FEHLER" in c["text"]
    monkeypatch.setattr(H, "runners", lambda: [])
    monkeypatch.setattr(H, "cron_status", lambda: c)
    assert H.main() == 1                                                   # toter cron allein ergibt Exit 1


def test_scheduler_layered_safeguards():
    sched = open(os.path.join(REPO, "collector", "ensure_scheduler.sh")).read()
    for tag in ("aurum2-ensure", "aurum2-ensure-reboot", "aurum2-catchup-hourly"):
        assert f"# {tag}\"" in sched
    assert "@reboot $REPO/collector/ensure_scheduler.sh" in sched and "5 7-12 * * * $REPO/collector/ensure_scheduler.sh" in sched
    assert "/workspace/aurum2/ALARM" in sched


def test_heartbeat_registry_covers_all_forward_lines_and_cron():
    names = [n for n, _, _ in H.runners()]
    assert names == ["Collector", "PAPER v1.0", "Sleeves A/B", "VOLTARGET"]
    sched = open(os.path.join(REPO, "collector", "ensure_scheduler.sh")).read()   # seit Freeze 2026-10-02 in cron
    assert "forward/heartbeat.py" in sched and "# aurum2-heartbeat" in sched
    assert "# aurum2-sleeves" in sched and "# aurum2-voltarget" in sched


def test_heartbeat_main_exit_code(tmp_path, monkeypatch):
    monkeypatch.setattr(H, "cron_status", lambda: dict(alarm=False, text="- OK cron-Daemon: läuft."))
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


# ------------------------------------------------------------------ Nachhol-Kette collector/ensure_scheduler.sh
def _due_script():
    src = open(os.path.join(REPO, "collector", "ensure_scheduler.sh")).read()
    body = src.split("DUE=$(python3 - \"$REPO\" \"$OUT\" <<'PY' 2>>\"$CLOG\"\n", 1)[1].split("\nPY\n", 1)[0]
    return body


def _due(tmp_path, now_zh, hist, monkeypatch):
    import subprocess
    env = dict(os.environ, AURUM_CATCHUP_NOW=now_zh, AURUM_PAPER_OUT=str(tmp_path / "p"),
               AURUM_SLEEVES_OUT=str(tmp_path / "s"), AURUM_VOLTARGET_OUT=str(tmp_path / "v"))
    for k, rows in hist.items():
        _hist(str(tmp_path / {"c": "c/run_history.jsonl", "p": "p/logs/run_history.jsonl", "s": "s/logs/run_history.jsonl",
                              "v": "v/logs/run_history.jsonl"}[k]), rows)
    os.makedirs(tmp_path / "c", exist_ok=True)
    r = subprocess.run([sys.executable, "-", REPO, str(tmp_path / "c")], input=_due_script(), capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    return r.stdout.split()


def test_catchup_chain_box_pause_order_and_idempotence(tmp_path, monkeypatch):
    """Vorfall 2026-10-03: nach der Box-Pause alles faellig, in fester Reihenfolge; nach dem Nachholen nichts mehr."""
    y = dict(c=[dict(started_utc="2026-10-02T04:15:01Z", ok=True)], p=[dict(started_utc="2026-10-02T04:50:02+00:00", ok=True)],
             s=[dict(run_utc="2026-10-02T04:55:00+00:00", rc=0)], v=[dict(run_utc="2026-10-02T05:00:00+00:00", rc=0)])
    assert _due(tmp_path, "2026-10-03T07:35:00+02:00", y, monkeypatch) == ["collector", "paper", "sleeves", "voltarget"]
    assert _due(tmp_path, "2026-10-03T06:00:00+02:00", y, monkeypatch) == []              # vor 06:15 nichts
    done = dict(c=y["c"] + [dict(started_utc="2026-10-03T05:38:42Z", ok=True)],
                p=y["p"] + [dict(started_utc="2026-10-03T06:02:36+00:00", ok=True)],
                s=y["s"] + [dict(run_utc="2026-10-03T06:02:36+00:00", rc=0)], v=y["v"] + [dict(run_utc="2026-10-03T06:02:36+00:00", rc=0)])
    assert _due(tmp_path, "2026-10-03T08:30:00+02:00", done, monkeypatch) == []
    # Runner lief heute, aber VOR dem nachgeholten Collector-Lauf -> erneut faellig (neue Daten)
    early = dict(done, s=y["s"] + [dict(run_utc="2026-10-03T05:10:00+00:00", rc=0)])
    assert _due(tmp_path, "2026-10-03T08:30:00+02:00", early, monkeypatch) == ["sleeves"]
    # Collector-Fehlversuch vor 30 min -> kein erneuter Collector-Versuch (hoechstens stuendlich)
    fail = dict(y, c=y["c"] + [dict(started_utc="2026-10-03T05:10:00Z", ok=False)])
    assert "collector" not in _due(tmp_path, "2026-10-03T07:40:00+02:00", fail, monkeypatch)
