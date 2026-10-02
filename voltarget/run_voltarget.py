#!/usr/bin/env python3
"""Tageslauf Vol-Target-Overlay (VOLTARGET_PREREG v1.0, KANDIDAT, nicht eingefroren). GESPERRT, solange voltarget_config.json enabled=false.

Fail-closed:
  - ohne Freigabe (enabled=false, start_bar oder freeze_list fehlt) kein Lauf: Exit 3. Es gibt keinen Dry-Run-Bypass.
  - Parameter/Gates der Konfiguration != voltarget_engine.PARAMS bzw. gates.GATES: Exit 4
  - Freeze-Liste: SHA jeder gelisteten Datei muss stimmen, sonst Exit 4
  - Invariantenverletzung (Position bei flacher Basis, Ziel ueber Basis-Exposure): Exit 5
  - gestoppter Coin (Luecke, keine Vol-Schaetzung): Exit 7
Kein Scheduler-Eintrag (bewusst). Keine Keys, keine Orders, keine Boersenverbindung: nur lokale Collector-Dateien.
Ausgaben (Standard /workspace/aurum2/paper_voltarget/): state/state_latest.json, ledger/equity_daily.csv,
ledger/trades.csv, logs/run_history.jsonl.
state_latest.json enthaelt fuer den gemeinsamen Wochenbericht (Branch sleeves-v1, forward/voltarget_bericht.py):
  summary[strat] = dict(status, coins_ok, coins_total, tage_offen, tage_offen_s_lt_1, sync_kosten_usd, sync_kosten_b_usd,
                        kosten_nach_grund)    (maker_plan, VT)
  s_verteilung[coin] = voltarget_engine.scale_distribution (Tage seit Start, Tage mit s < 1, s_min, Klassen)
Basis B fuer die Gates = Basis mit symmetrischer Sync-Buchung (Spalte eq_base_sync); eq_base = Paper-Ledger-Nachrechnung (R3).
"""
import csv, datetime as dt, hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voltarget_engine as V      # noqa: E402
import gates as G                 # noqa: E402

DATA = os.environ.get("AURUM_DATA_LIVE", "/workspace/aurum2/data_live")
OUT = os.environ.get("AURUM_VOLTARGET_OUT", "/workspace/aurum2/paper_voltarget")
CFG = os.path.join(HERE, "voltarget_config.json")


class Disabled(Exception):
    pass


def load_cfg(path=CFG):
    return json.load(open(path))


def require_enabled(cfg):
    """Laufzeitsperre: wirft Disabled, solange das Overlay nicht freigegeben ist."""
    if cfg.get("enabled") is not True or not cfg.get("start_bar") or not cfg.get("freeze_list"):
        raise Disabled("Vol-Target-Overlay nicht freigegeben (VOLTARGET_PREREG v0.2 ist ein Entwurf): kein Lauf.")


def params_ok(cfg):
    p, g = cfg.get("params") or {}, cfg.get("gates") or {}
    return (all(k in p and float(p[k]) == float(v) for k, v in V.PARAMS.items())
            and all(k in g and float(g[k]) == float(v) for k, v in G.GATES.items()))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def check_freeze(listfile):
    bad = []
    for line in open(os.path.join(V.REPO, listfile)):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        h, p = line.split(None, 1)
        fp = os.path.join(V.REPO, p)
        if not os.path.exists(fp) or sha(fp) != h:
            bad.append(p)
    return bad


def write_csv(path, rows):
    if not rows:
        return
    tmp = path + ".tmp"
    with open(tmp, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n", extrasaction="ignore")
        w.writeheader(); w.writerows(rows)
    os.replace(tmp, path)


def run(cfg, data, out, now=None):
    """Ein Tageslauf. Verweigert ohne Freigabe (require_enabled) und schreibt nie ins Produktionsverzeichnis,
    wenn die Datei-Konfiguration nicht freigegeben ist."""
    require_enabled(cfg)
    if os.path.abspath(out) == os.path.abspath(OUT):
        require_enabled(load_cfg())
    V.guard_path(data); V.guard_path(out)
    import pandas as pd
    import base_adapter as BA
    now_ts = pd.Timestamp(now) if now is not None else pd.Timestamp.now(tz="UTC")
    start = dt.date.fromisoformat(cfg["start_bar"])
    costs = V.cost_scenarios()
    for sub in ("state", "ledger", "logs"):
        os.makedirs(os.path.join(out, sub), exist_ok=True)
    eq_rows, tr_rows, res, rc = [], [], {}, 0
    summ = {s: dict(status="OK", coins_ok=0, coins_total=len(BA.COINS), tage_offen=0, tage_offen_s_lt_1=0,
                    sync_kosten_usd=0.0, sync_kosten_b_usd=0.0, kosten_nach_grund={}) for s in BA.STRATS}
    sverteil = {}
    for coin in BA.COINS:
        f = os.path.join(data, "kraken_ohlc", f"{coin}USD_1d.csv")
        if not os.path.exists(f):
            res[coin] = dict(status="STOPPED", reason="Datei fehlt"); rc = max(rc, 7)
            for s_ in BA.STRATS:
                summ[s_]["status"] = "STOPPED"
            continue
        d = BA.load_bars(f, now_ts)
        for strat in BA.STRATS:
            days, nE, nEv = BA.base_days(d, strat)
            i0 = BA.start_index(days, start)
            dec = BA.P.decide(d, strat)
            coin_ok = True
            for scen, cost in costs.items():
                try:
                    cmp_ = V.run_compare(days, cost, i0, nE, nEv)
                except V.InvariantError as e:
                    res[f"{strat}_{coin}_{scen}"] = dict(status="INVARIANT", error=str(e)); rc = max(rc, 5); coin_ok = False; continue
                r, rb = cmp_["vt"], cmp_["b"]
                acc = BA.P.account(d, dec, cost)["equity"]     # unveraenderte Basis wie Paper-Ledger (ab PAPER START_BAR), R3
                eqb = {row["date"]: row["equity"] for row in rb["equity"]}
                for row in r["equity"]:
                    t = pd.Timestamp(row["date"], tz="UTC")
                    eq_rows.append(dict(date=row["date"], strat=strat, coin=coin, scenario=scen, eq_overlay=round(row["equity"], 6),
                                        eq_base_sync=round(eqb.get(row["date"], float("nan")), 6),
                                        eq_base=round(float(acc.get(t, float("nan"))), 6), weight=round(row["weight"], 6),
                                        E_base=row["E"], scale=None if row["scale"] is None else round(row["scale"], 6),
                                        status=row["status"]))
                for t in r["trades"]:
                    tr_rows.append(dict(strat=strat, coin=coin, scenario=scen, run="VT", **t))
                for t in rb["trades"]:
                    tr_rows.append(dict(strat=strat, coin=coin, scenario=scen, run="B", **t))
                res[f"{strat}_{coin}_{scen}"] = dict(status=r["status"], stop=r["stop"], pending=r["pending"],
                                                     sync_kosten_usd=V.sync_costs(r["trades"]), sync_kosten_b_usd=V.sync_costs(rb["trades"]),
                                                     kosten_nach_grund=V.costs_by_reason(r["trades"]))
                if r["status"] == "STOPPED":
                    rc = max(rc, 7); coin_ok = False; summ[strat]["status"] = "STOPPED"
                if scen == "maker_plan":
                    dist = V.scale_distribution(r["equity"]); sm = summ[strat]
                    sm["tage_offen"] += dist["tage_offen"]; sm["tage_offen_s_lt_1"] += dist["tage_offen_s_lt_1"]
                    sm["sync_kosten_usd"] += V.sync_costs(r["trades"]); sm["sync_kosten_b_usd"] += V.sync_costs(rb["trades"])
                    for k, v in V.costs_by_reason(r["trades"]).items():
                        sm["kosten_nach_grund"][k] = sm["kosten_nach_grund"].get(k, 0.0) + v
                    if coin not in sverteil:                    # s haengt nur vom Coin ab (nicht von der Strategie)
                        sverteil[coin] = {k: v for k, v in dist.items() if k not in ("tage_offen", "tage_offen_s_lt_1")}
            summ[strat]["coins_ok"] += int(coin_ok)
    write_csv(os.path.join(out, "ledger", "equity_daily.csv"), eq_rows)
    write_csv(os.path.join(out, "ledger", "trades.csv"), tr_rows)
    st = dict(run_utc=now_ts.isoformat(), start_bar=str(start), params=V.PARAMS, results=res, summary=summ,
              s_verteilung=sverteil, rc=rc)
    tmp = os.path.join(out, "state", "state_latest.json.tmp")
    json.dump(st, open(tmp, "w"), indent=1, default=str); os.replace(tmp, os.path.join(out, "state", "state_latest.json"))
    with open(os.path.join(out, "logs", "run_history.jsonl"), "a") as fh:
        fh.write(json.dumps(dict(run_utc=st["run_utc"], rc=rc)) + "\n")
    return rc, st


def main():
    cfg = load_cfg()
    try:
        require_enabled(cfg)
    except Disabled as e:
        print(str(e)); return 3
    if not params_ok(cfg):
        print("Parameter in voltarget_config.json weichen von voltarget_engine.PARAMS ab: kein Lauf."); return 4
    bad = check_freeze(cfg["freeze_list"])
    if bad:
        print(f"Freeze-Pruefung fehlgeschlagen: {bad}"); return 4
    rc, st = run(cfg, DATA, OUT)
    print(json.dumps(st, indent=1, default=str)); return rc


if __name__ == "__main__":
    sys.exit(main())
