#!/usr/bin/env python3
"""XS21 PiT v1.0 – Lauf. Modi:
  --laufbeginn   M6: bestimmt den Laufbeginn nur aus Listing und quote_volume (keine Renditen), schreibt run/xs21_laufbeginn.json
  --lauf         der einzige Lauf (verweigert, wenn run/xs21_eval.json existiert oder die Spezifikation nicht der eingefrorenen SHA entspricht)
"""
import argparse, csv, datetime as dt, hashlib, json, math, os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import xs21_pit as X
S = X.S
REPO = X.REPO; RUN = os.path.join(HERE, "run"); DATA = os.path.join(REPO, "data", "xs21")
B7 = os.path.join(REPO, "01_forschung/09_lane_c/xs21_pit_v1.0/xs21_exclusions_v1.0.csv")
SENS = os.path.join(REPO, "01_forschung/09_lane_c/xs21_pit_v1.0/xs21_sensitivitaet_ohne_v1.0.csv")
UNI = os.path.join(REPO, "data/raw/binance_um_universe.csv")
SNAP = os.path.join(REPO, "01_forschung/09_lane_c/xs21_pit_v0.2/binance_um_snapshot_2026-10-01.csv")
TBILL = os.path.join(REPO, "data/supplement/DTB3_3m_tbill_to_2026-09-14.csv")
COSTJ = os.path.join(REPO, "config/cost_model_v1.json")


def listing():
    snap = {r["symbol"]: r for r in csv.DictReader(open(SNAP))}
    out = {}
    for r in csv.DictReader(open(UNI)):
        lm = r["last_month"]; sn = snap.get(r["symbol"])
        if sn and sn["last_daily_kline"]:
            lm = max(lm, sn["last_daily_kline"][:7])
        out[r["symbol"]] = (r["first_month"], lm)
    return out


def tbill():
    t = pd.read_csv(TBILL); t["observation_date"] = pd.to_datetime(t["observation_date"], utc=True)
    return t.set_index("observation_date")["DTB3"].astype(float) / 100.0


def check_costs():
    """Kostensaetze aus s2lib muessen dem zentralen Modell (stage2_perp) entsprechen."""
    j = json.load(open(COSTJ))["sections"]["stage2_perp"]["values"]
    for k in ("K0", "K1", "K2"):
        for f in ("fee", "fric", "fund_pay"):
            assert abs(j[k][f] - S.COST[k][f]) < 1e-15, (k, f)
    return "stage2_perp == s2lib.COST"


def load():
    K, F = X.load_raw(DATA)
    excl = {r["symbol"] for r in csv.DictReader(open(B7))}
    bad = sorted(set(K) & excl)
    assert not bad, f"B7-Symbole in den Daten: {bad[:5]}"
    check_costs()
    D = X.Data(K, F, listing(), tbill())
    return D


def inputs():
    files = {"spec": X.SPEC, "b7": B7, "sens": SENS, "universe_csv": UNI, "snapshot": SNAP, "tbill": TBILL, "cost_model": COSTJ,
             "provenance": os.path.join(DATA, "provenance.jsonl"), "lib": os.path.join(HERE, "xs21_pit.py"), "run": os.path.abspath(__file__),
             "s2lib": os.path.join(REPO, "01_forschung/02_strategien/s2lib.py")}
    return {k: X.sha(v) for k, v in files.items()}


def univ_table(D, univ):
    return [dict(T=str(u["T"].date()), n_basis=len(u["basis"]), n_U1=len(u["U1"]), n_U2=len(u["U2"]),
                 U2=" ".join(D.syms[j] for j in u["U2"]), U1=" ".join(D.syms[j] for j in u["U1"])) for u in univ]


def laufbeginn():
    D = load(); univ = X.universes(D)
    T0 = X.run_start(univ)
    out = dict(laufbeginn=str(T0.date()) if T0 is not None else None, rule="M6: erster Stichtag mit |U1| >= 20, nur Listing und quote_volume",
               n_symbols=len(D.syms), first_stichtag=str(univ[0]["T"].date()), inputs=inputs(),
               first_10=[dict(T=r["T"], n_U1=r["n_U1"], n_basis=r["n_basis"]) for r in univ_table(D, univ)[:10]],
               computed_at=dt.datetime.now(dt.timezone.utc).isoformat())
    os.makedirs(RUN, exist_ok=True)
    json.dump(out, open(os.path.join(RUN, "xs21_laufbeginn.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "inputs"}, indent=1))


def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items() if not str(k).startswith("_")}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)): return None if math.isnan(float(o)) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, pd.Timestamp): return str(o.date())
    return o


def lauf():
    assert X.sha(X.SPEC) == X.SPEC_SHA, "Spezifikation weicht vom Freeze ab"
    ev = os.path.join(RUN, "xs21_eval.json")
    if os.path.exists(ev):
        raise SystemExit("Lauf existiert bereits (ein einziger Lauf). Abbruch.")
    lb = json.load(open(os.path.join(RUN, "xs21_laufbeginn.json")))
    t_start = dt.datetime.now(dt.timezone.utc)
    inp = inputs()
    D = load(); univ = X.universes(D)
    start = pd.Timestamp(lb["laufbeginn"], tz="UTC")
    assert X.run_start(univ) == start, "Laufbeginn weicht ab"
    # Pruefbedingungen
    checks = {}
    viol = [str(u["T"].date()) for u in univ if u["T"] >= start and len(u["U1"]) >= X.U1_MIN_N and not set(u["U2"]) <= set(u["U1"])]
    assert not viol, f"U2 nicht Teilmenge von U1: {viol[:5]}"
    checks["U2_subset_U1"] = "OK an allen Stichtagen mit |U1| >= 20"
    res = {}
    def ev_(name, ukey, univ_=univ, **kw):
        r = X.evaluate(D, univ_, ukey, start, **kw); res[name] = r; print("fertig:", name, flush=True); return r
    p1 = ev_("U1_LS", "U1"); p2 = ev_("U2_LS", "U2")
    # Holm ueber die zwei Primaertests
    adj = S.holm({"U1_LS": p1["boot"]["p_sharpe"], "U2_LS": p2["boot"]["p_sharpe"]})
    p1["holm_p"], p2["holm_p"] = adj["U1_LS"], adj["U2_LS"]
    neigh = {}
    for uk in ("U1", "U2"):
        neigh[uk] = []
        for nm, kw in [("L42", dict(L=42)), ("L63", dict(L=63)), ("top2", dict(top=2)), ("top4", dict(top=4))]:
            r = ev_(f"{uk}_LS_{nm}", uk, full=False, **kw)
            eq = r["scen"]["K1"]["equity"]
            neigh[uk].append(dict(name=nm, expectancy=r["scen"]["K1"]["expectancy"], sharpe=eq["sharpe"] if eq else float("nan"),
                                  cagr=eq["cagr"] if eq else float("nan"), maxdd=eq["maxdd"] if eq else float("nan"), n_trades=r["scen"]["K1"]["n_trades"]))
    for nm, r in (("U1_LS", p1), ("U2_LS", p2)):
        r["criteria"], r["verdict"] = X.criteria(r, neigh[nm[:2]])
        r["neighbours"] = neigh[nm[:2]]
        r["survivorship"] = X.survivorship(D, r, start)
    # DSR (Sensitivitaet, 2 Versuche)
    srs = []
    for r in (p1, p2):
        x = r["_sim"]["net"].dropna(); exr = x - pd.Series(D.cash_daily, index=D.days).reindex(x.index); srs.append((exr, exr.mean() / exr.std(ddof=1)))
    var_sr = float(np.var([s for _, s in srs], ddof=1))
    for r, (exr, sr) in zip((p1, p2), srs):
        r["dsr"] = S.deflated_sharpe(sr, len(exr), float(exr.skew()), float(exr.kurt() + 3), 2, var_sr)
    # Vergleiche (keine Primaertests)
    ev_("U1_L", "U1", side="L"); ev_("U2_L", "U2", side="L")
    ev_("U1_LS_dezil", "U1", decile=True, full=False)
    sens = [r["symbol"] for r in csv.DictReader(open(SENS))]
    univ_s = X.universes(D, extra_excl=sens)
    ev_("U1_LS_sens_b7", "U1", univ_=univ_s, full=False); ev_("U2_LS_sens_b7", "U2", univ_=univ_s, full=False)
    # Pruefungen auf den Primaerlaeufen
    for nm in ("U1_LS", "U2_LS"):
        r = res[nm]; W = r["_W"]; sim = r["_sim"]
        assert np.abs(W).sum(1).max() <= 1 + 1e-9
        chg = np.where(np.abs(np.diff(W, axis=0)).sum(1) > 0)[0] + 1
        okdays = {D.days.get_loc(u["T"]) + 1 for u in univ} | {e + 1 for _, e in D.ends} | {D.days.get_loc(X.END) + 1}
        assert set(chg) <= okdays, "Gewichtsaenderung ausserhalb Stichtag+1 bzw. Delisting"
        checks[f"{nm}_weights"] = "Summe |w| <= 1, Aenderungen nur an T+1 oder nach Delisting"
    meta = dict(spec="xs21_point_in_time_prereg_v1.0.md", spec_sha256=X.sha(X.SPEC), inputs=inp, laufbeginn=lb["laufbeginn"],
                n_symbols=len(D.syms), gap_days_bridged=D.gap_days, n_relistings=D.n_relist, n_life_ends=len(D.ends),
                n_delisted_symbols=int(D.delisted.sum()), started_utc=t_start.isoformat(), finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                checks=checks, holm=adj, nboot=2000)
    out = dict(meta=meta, results={k: clean(v) for k, v in res.items()}, universes=univ_table(D, univ))
    json.dump(out, open(ev, "w"), indent=1)
    json.dump(meta, open(os.path.join(RUN, "xs21_run.log"), "w"), indent=1)
    for nm in ("U1_LS", "U2_LS", "U1_L", "U2_L"):
        pd.DataFrame(res[nm]["_trades"]).to_csv(os.path.join(RUN, f"xs21_trades_{nm}.csv"), index=False)
        pd.DataFrame(res[nm]["_log"]).to_csv(os.path.join(RUN, f"xs21_auswahl_{nm}.csv"), index=False)
    pd.DataFrame({nm: res[nm]["_sim"]["net"] for nm in ("U1_LS", "U2_LS", "U1_L", "U2_L")}).dropna(how="all").to_csv(os.path.join(RUN, "xs21_daily_net_K1.csv"))
    for nm in ("U1_LS", "U2_LS"):
        sm = res[nm]["_sim"]
        pd.DataFrame({k: sm[k] for k in ("gross", "cost", "funding", "cash", "net", "expo", "long")}).dropna(how="all").to_csv(os.path.join(RUN, f"xs21_daily_components_{nm}_K1.csv"))
    pd.DataFrame(univ_table(D, univ)).to_csv(os.path.join(RUN, "xs21_universen.csv"), index=False)
    for nm in ("U1_LS", "U2_LS"):
        r = res[nm]; e = r["scen"]["K1"]["equity"]
        print(nm, r["verdict"], {k: v for k, v in r["criteria"].items()}, "CAGR", e["cagr"], "Sharpe", e["sharpe"], "MaxDD", e["maxdd"], "holm", r["holm_p"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--laufbeginn", action="store_true"); g.add_argument("--lauf", action="store_true")
    a = ap.parse_args()
    laufbeginn() if a.laufbeginn else lauf()
