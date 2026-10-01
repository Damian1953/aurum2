"""Taeglicher Paper-Lauf (PAPER_PREREG_v1.0). Keine Keys, keine Orders. Idempotent: rechnet aus den
abgeschlossenen Kraken-Tageskerzen alles neu und schreibt Zustand, Ledger, Tageskurve und Journal.

Aufruf: python paper/run_paper.py [--if-needed]
Umgebung: AURUM_DATA_LIVE (Default /workspace/aurum2/data_live), AURUM_PAPER_OUT (Default /workspace/aurum2/paper)
"""
import argparse, datetime as dt, json, os, sys, uuid
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paper_engine as E

REPO = E.REPO
PREREG = os.path.join(REPO, "paper", "PAPER_PREREG_v1.0.md")
FREEZE_LIST = os.path.join(REPO, "00_doku", "paper_freeze_2026-10-01_expected_shas.txt")
VERSION = "1.0"


def paths():
    live = os.environ.get("AURUM_DATA_LIVE", "/workspace/aurum2/data_live")
    out = os.environ.get("AURUM_PAPER_OUT", "/workspace/aurum2/paper")
    return live, out


def check_freeze():
    """Fail-closed: Code und Vorregistrierung muessen der Freeze-Liste entsprechen."""
    exp = {}
    for line in open(FREEZE_LIST):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        h, p = line.split(None, 1)
        exp[p.strip()] = h
    bad = {p: h for p, h in exp.items() if E.sha256(os.path.join(REPO, p)) != h}
    return exp, bad


def run(now_utc=None, live=None, out=None, enforce_freeze=True):
    live0, out0 = paths()
    live = live or live0; out = out or out0
    now_utc = now_utc or pd.Timestamp.now(tz="UTC")
    for sub in ("state", "ledger", "logs", "berichte"):
        os.makedirs(os.path.join(out, sub), exist_ok=True)
    run_id = now_utc.strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:6]
    rec = dict(run_id=run_id, started_utc=now_utc.isoformat(), version=VERSION, ok=False, errors=[], warnings=[])
    if os.path.exists("/home/claude"):
        rec["errors"].append("/home/claude existiert (Guard)")
    exp, bad = check_freeze() if enforce_freeze else ({}, {})
    if bad:
        rec["errors"].append(f"Freeze verletzt: {sorted(bad)}")
    if rec["errors"]:
        _finish(out, rec); return rec
    rec["prereg_sha256"] = E.sha256(PREREG) if os.path.exists(PREREG) else None
    costs = E.cost_scenarios()
    state = dict(run_id=run_id, generated_utc=now_utc.isoformat(), version=VERSION, prereg_sha256=rec["prereg_sha256"],
                 start_bar=str(E.START_BAR.date()), sleeve_usd=E.SLEEVE_USD, costs=costs, coins={}, strategies={})
    trades_rows, eq_rows, journal = [], [], []
    eq_tot = {(s, sc): None for s in E.STRATS for sc in costs}
    bh_tot = {sc: None for sc in costs}
    for coin in E.COINS:
        f = os.path.join(live, "kraken_ohlc", f"{coin}USD_1d.csv")
        if not os.path.exists(f):
            rec["errors"].append(f"{coin}: Datei fehlt"); continue
        d = E.load_kraken_1d(f, now_utc)
        g = E.gaps_after(d, E.START_BAR)
        info = dict(file_sha256=E.sha256(f), bars=len(d), last_bar=str(d.index[-1].date()), gaps_since_start=g)
        exp_last = (now_utc - pd.Timedelta(days=1)).floor("D")
        if d.index[-1] < exp_last:
            rec["warnings"].append(f"{coin}: letzter abgeschlossener Bar {d.index[-1].date()} < erwartet {exp_last.date()}")
        if g:
            rec["errors"].append(f"{coin}: {g} Luecke(n) seit Start, Coin fail-closed"); state["coins"][coin] = info; continue
        state["coins"][coin] = info
        ind = E.indicators(d)
        for s in E.STRATS:
            dec = E.decide(d, s, ind=ind)
            st = state["strategies"].setdefault(s, {})
            cs = {}
            for sc, cost in costs.items():
                acc = E.account(d, dec, cost)
                key = (s, sc)
                eq_tot[key] = acc["equity"] if eq_tot[key] is None else eq_tot[key].add(acc["equity"], fill_value=E.SLEEVE_USD)
                cs[sc] = dict(equity_usd=round(float(acc["equity"].iloc[-1]), 2) if len(acc["equity"]) else E.SLEEVE_USD,
                              costs_usd=round(acc["costs_paid"], 2), closed_trades=len(acc["trades"]))
                for r in acc["trades"]:
                    trades_rows.append(dict(strategy=s, coin=coin, scenario=sc, **r))
            op = dec["open"]
            st[coin] = dict(
                position=None if op is None else dict(entry_date=str(op["entry_t"].date()), entry_fill=op["entry_fill"],
                                                      units=[[u, str(t.date()), fl] for fl, u, t in op["units"]],
                                                      stop=round(op["stop"], 8), last_close=float(d["close"].iloc[-1])),
                order_next_open=None if dec["order"] is None else dict(kind=dec["order"]["kind"], reason=dec["order"]["reason"],
                                                                        signal_bar=str(dec["order"]["signal_bar"].date()),
                                                                        fill_bar=str(dec["order"]["fill_bar"].date())),
                scenarios=cs)
            for ev in dec["log"]:
                if ev["t"] >= E.START_BAR:
                    journal.append(dict(strategy=s, coin=coin, t=str(ev["t"].date()), **{k: v for k, v in ev.items() if k != "t"}))
        for sc, cost in costs.items():
            b = E.buy_and_hold(d, cost)
            bh_tot[sc] = b if bh_tot[sc] is None else bh_tot[sc].add(b, fill_value=E.SLEEVE_USD)
    # Portfolio-Kurven
    for (s, sc), ser in eq_tot.items():
        if ser is None:
            continue
        for t, v in ser.items():
            eq_rows.append(dict(series=s, scenario=sc, date=str(t.date()), equity_usd=round(float(v), 4)))
    for sc, ser in bh_tot.items():
        if ser is None:
            continue
        for t, v in ser.items():
            eq_rows.append(dict(series="BH", scenario=sc, date=str(t.date()), equity_usd=round(float(v), 4)))
    state["portfolio"] = {}
    for (s, sc), ser in list(eq_tot.items()) + [(("BH", sc), v) for sc, v in bh_tot.items()]:
        if ser is None or len(ser) == 0:
            continue
        state["portfolio"].setdefault(s, {})[sc] = dict(equity_usd=round(float(ser.iloc[-1]), 2), max_dd=round(E.max_dd(ser), 4),
                                                       start_usd=E.SLEEVE_USD * len(E.COINS))
    # Journal: Revisionen erkennen (frueher protokollierte Entscheidungen muessen bestehen bleiben)
    jpath = os.path.join(out, "ledger", "journal.jsonl")
    seen = set()
    if os.path.exists(jpath):
        for l in open(jpath):
            seen.add(l.strip())
    cur = set(json.dumps(j, sort_keys=True) for j in journal)
    revised = sorted(seen - cur)
    if revised:
        rec["errors"].append(f"REVISION: {len(revised)} frueher protokollierte Ereignisse fehlen im Neulauf")
        with open(os.path.join(out, "ledger", "revisionen.jsonl"), "a") as fh:
            for r in revised:
                fh.write(json.dumps(dict(run_id=run_id, missing=json.loads(r))) + "\n")
    new = sorted(cur - seen)
    with open(jpath, "a") as fh:
        for j in new:
            fh.write(j + "\n")
    rec["new_events"] = len(new)
    pd.DataFrame(trades_rows).to_csv(os.path.join(out, "ledger", "trades.csv"), index=False)
    pd.DataFrame(eq_rows).to_csv(os.path.join(out, "ledger", "equity_daily.csv"), index=False)
    state["warnings"] = rec["warnings"]; state["errors"] = rec["errors"]
    with open(os.path.join(out, "state", "state_latest.json"), "w") as fh:
        json.dump(state, fh, indent=1, ensure_ascii=False, default=str)
    last_bars = [v["last_bar"] for v in state["coins"].values()]
    rec["last_bar_min"] = min(last_bars) if last_bars else None
    rec["ok"] = not rec["errors"]
    _finish(out, rec)
    return rec


def _finish(out, rec):
    os.makedirs(os.path.join(out, "logs"), exist_ok=True)
    rec["finished_utc"] = pd.Timestamp.now(tz="UTC").isoformat()
    with open(os.path.join(out, "logs", "run_history.jsonl"), "a") as fh:
        fh.write(json.dumps(rec, default=str) + "\n")


def needed(out, now_utc=None):
    """True, wenn der letzte erfolgreiche Lauf den gestern abgeschlossenen Bar nicht enthielt."""
    now_utc = now_utc or pd.Timestamp.now(tz="UTC")
    exp_last = str((now_utc - pd.Timedelta(days=1)).floor("D").date())
    p = os.path.join(out, "logs", "run_history.jsonl")
    if not os.path.exists(p):
        return True
    for l in reversed(open(p).read().splitlines()):
        r = json.loads(l)
        if r.get("ok"):
            return (r.get("last_bar_min") or "") < exp_last
    return True


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--if-needed", action="store_true")
    a = ap.parse_args()
    live, out = paths()
    if a.if_needed and not needed(out):
        sys.exit(0)
    r = run()
    print(json.dumps({k: r[k] for k in ("run_id", "ok", "errors", "warnings", "last_bar_min", "new_events") if k in r}, ensure_ascii=False))
    sys.exit(0 if r["ok"] else 1)
