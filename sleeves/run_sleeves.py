#!/usr/bin/env python3
"""Tageslauf Sleeve A und Leitplanke B (Forward-Paper, v1.0-Kandidat, NICHT eingefroren). Fail-closed:
  - ohne Freigabe (sleeves_config.json enabled=false) kein Lauf (Exit 3), ausser --dry-run in ein separates Verzeichnis
  - start_bar muss ein Freitag sein (Start in gueltigem Zustand), sonst Exit 3
  - Freeze-Liste: SHA jeder gelisteten Datei muss stimmen, sonst Exit 4
  - Look-ahead -> Exit 5, Revision frueher protokollierter Ereignisse -> Exit 6, gestoppter Sleeve -> Exit 7
Ausgaben (Standard /workspace/aurum2/paper_sleeves/): state/state_latest.json, ledger/equity_daily_{A,B}.csv,
ledger/events_{A,B}.csv, ledger/journal.jsonl (append-only), logs/run_history.jsonl.
"""
import argparse, csv, datetime as dt, hashlib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sleeve_engine as E
import auswertung as A

DATA = os.environ.get("AURUM_DATA_LIVE", "/workspace/aurum2/data_live")
OUT = os.environ.get("AURUM_SLEEVES_OUT", "/workspace/aurum2/paper_sleeves")
CFG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sleeves_config.json")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def check_freeze(listfile):
    bad = []
    for line in open(os.path.join(E.REPO, listfile)):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        h, p = line.split(None, 1)
        fp = os.path.join(E.REPO, p)
        if not os.path.exists(fp) or sha(fp) != h:
            bad.append(p)
    return bad


def write_csv(path, rows):
    if not rows:
        return
    tmp = path + ".tmp"
    with open(tmp, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n", extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    os.replace(tmp, path)


def start_ok(start):
    """Start in gueltigem Zustand: der Startbar muss ein Freitag sein (Signaltag von A), sonst kein Lauf."""
    return start is not None and start.weekday() == 4


def run(data, out, start, now=None):
    now = now or dt.datetime.now(E.UTC)
    for sub in ("state", "ledger", "logs"):
        os.makedirs(os.path.join(out, sub), exist_ok=True)
    fr = lambda *p: E.load_first_release(os.path.join(data, "macro", *p))
    mvrv = fr("coinmetrics", "btc_CapMVRVCur.csv")
    walcl, tga, rrp, dtb3 = (fr("fred", f"{s}.csv") for s in (*E.FRED_A, "DTB3"))
    bars = [b for b in E.load_bars(os.path.join(data, "kraken_ohlc", "BTCUSD_1d.csv")) if E.cutoff(b[0]) <= now]
    costs = E.cost_scenarios()
    sleeves = {"A": lambda d, s: E.signal_a(walcl, tga, rrp, d, s), "B": lambda d, s: E.signal_b(mvrv, d, s)}
    res, rc = {}, 0
    jpath = os.path.join(out, "ledger", "journal.jsonl")
    old = set()
    if os.path.exists(jpath):
        old = {(j["sleeve"], j["key"]) for j in map(json.loads, open(jpath))}
    seen = set()
    for name, fn in sleeves.items():
        try:
            r = E.simulate(bars, start, fn, costs, dtb3)
        except E.LookAheadError as e:
            res[name] = dict(status="LOOKAHEAD", error=str(e)); rc = max(rc, 5); continue
        write_csv(os.path.join(out, "ledger", f"equity_daily_{name}.csv"), r["equity"])
        write_csv(os.path.join(out, "ledger", f"events_{name}.csv"),
                  [dict(e, info=json.dumps(e.get("info"), default=str)) for e in r["events"]])
        with open(jpath, "a") as fh:
            for e in r["events"]:
                seen.add((name, e["key"]))
                if (name, e["key"]) not in old:
                    fh.write(json.dumps(dict(sleeve=name, logged_utc=now.isoformat(timespec="seconds"), **e), default=str) + "\n")
        last = r["equity"][-1] if r["equity"] else {}
        res[name] = dict(status=r["status"], stop=r["stop"], state=r["state"], pending_fill=r["pending"], last_bar=last.get("bar"),
                         n_events=len(r["events"]), equity_last={k: v for k, v in last.items() if k.startswith(("eq_", "bh_", "b2_"))},
                         n_wechsel=sum(1 for e in r["events"] if e["type"] == "fill"),
                         kennzahlen={c: E.metrics(r["equity"], c) for c in (f"eq_maker_plan_{E.PRIMARY_CASH}", "bh_maker_plan")}
                         if r["equity"] else {})
        if name == "A":
            res[name]["regimephasen"] = E.regime_phases(r["equity"]) if r["equity"] else None
        if name == "B":
            res[name]["identisch_bh"] = A.b_identisch_bh(r["equity"])
        if r["status"] == "STOPPED":
            rc = max(rc, 7)
    missing = sorted(old - seen)
    if missing:
        rc = max(rc, 6)
    st = dict(run_utc=now.isoformat(timespec="seconds"), start_bar=str(start), sleeves=res, revisions=[list(m) for m in missing],
              inputs={k: (sha(p) if os.path.exists(p) else None) for k, p in {
                  "mvrv": os.path.join(data, "macro/coinmetrics/btc_CapMVRVCur.csv"),
                  **{s: os.path.join(data, f"macro/fred/{s}.csv") for s in (*E.FRED_A, "DTB3")},
                  "btc_1d": os.path.join(data, "kraken_ohlc/BTCUSD_1d.csv")}.items()}, rc=rc)
    tmp = os.path.join(out, "state", "state_latest.json.tmp")
    json.dump(st, open(tmp, "w"), indent=1, default=str); os.replace(tmp, os.path.join(out, "state", "state_latest.json"))
    with open(os.path.join(out, "logs", "run_history.jsonl"), "a") as fh:
        fh.write(json.dumps(dict(run_utc=st["run_utc"], rc=rc, status={k: v["status"] for k, v in res.items()})) + "\n")
    return rc, st


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Betriebstest ohne Freigabe, nur in separates Verzeichnis, keine Bewertung")
    ap.add_argument("--start", help="Startbar YYYY-MM-DD (nur --dry-run)")
    ap.add_argument("--out", default="/workspace/aurum2/work/sleeves_dryrun")
    a = ap.parse_args()
    cfg = json.load(open(CFG))
    if a.dry_run:
        if os.path.abspath(a.out) == os.path.abspath(OUT):
            print("dry-run darf nicht ins Produktionsverzeichnis schreiben"); return 3
        rc, st = run(DATA, a.out, dt.date.fromisoformat(a.start))
        print(json.dumps(st, indent=1, default=str)); return rc
    if not cfg.get("enabled") or not cfg.get("start_bar") or not cfg.get("freeze_list"):
        print("Sleeves A/B nicht freigegeben (vor Freeze): kein Lauf."); return 3
    if not start_ok(dt.date.fromisoformat(cfg["start_bar"])):
        print("start_bar muss ein Freitag sein (Signaltag Sleeve A): kein Lauf."); return 3
    bad = check_freeze(cfg["freeze_list"])
    if bad:
        print(f"Freeze-Pruefung fehlgeschlagen: {bad}"); return 4
    rc, st = run(DATA, OUT, dt.date.fromisoformat(cfg["start_bar"]))
    print(json.dumps(st, indent=1, default=str)); return rc


if __name__ == "__main__":
    sys.exit(main())
