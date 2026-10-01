"""
Regressionstest: Cross-Coin-Library rlib v1.0 (Modus BTC Stufe A) gegen die eingefrorenen BTC-Stufe-A-Referenzdateien.
Vergleich auf Ereignisebene, exakt (==) fuer Ganzzahlen und Text, Gleitkomma exakt oder mit dokumentierter Toleranz 1e-9 (nur
Rundung beim CSV-Roundtrip der Referenz, siehe Bericht). Ergebnis REGRESSION PASS / FAIL in regress_btc_result.json.
"""
import sys, json, hashlib, time, numpy as np, pandas as pd
sys.path.insert(0, "/home/claude/rtc"); import rlib as R; Y = R.Y
REF = "/home/claude/yamato/data"; OUT = "/home/claude/rtc/regress"
import os; os.makedirs(OUT, exist_ok=True)
TOL = 1e-9   # einzige Toleranz: CSV-Roundtrip der Referenz (float64 -> Text -> float64)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
res = dict(tol_float=TOL, checks=[], fail=False)
def check(name, ok, detail=""):
    res["checks"].append(dict(name=name, ok=bool(ok), detail=detail)); print(("ok  " if ok else "FAIL"), name, detail, flush=True)
    if not ok: res["fail"] = True
def cmp_frame(name, a, b, int_cols, float_cols, str_cols=()):
    check(f"{name}: Zeilenzahl", len(a) == len(b), f"{len(a)} vs {len(b)}")
    if len(a) != len(b): return
    for c in int_cols:
        check(f"{name}: {c} exakt", (a[c].to_numpy().astype(int) == b[c].to_numpy().astype(int)).all())
    for c in str_cols:
        # Textspalten: leerer Text und NaN (CSV-Roundtrip der Referenz liest leere Felder als NaN) werden beide als "" verglichen
        x = a[c].fillna("").astype(str).to_numpy(); y = b[c].fillna("").astype(str).to_numpy()
        check(f"{name}: {c} exakt (NaN und leer normalisiert)", (x == y).all(), f"abweichende Zeilen {int((x != y).sum())}")
    for c in float_cols:
        x = a[c].to_numpy(float); y = b[c].to_numpy(float); m = np.isfinite(x) & np.isfinite(y)
        check(f"{name}: {c} NaN-Muster", (np.isfinite(x) == np.isfinite(y)).all())
        d = float(np.max(np.abs(x[m] - y[m]))) if m.any() else 0.0
        check(f"{name}: {c} |diff|<=tol", d <= TOL, f"max|diff|={d:.3e}")

t0 = time.time()
res["sha_inputs"] = dict(discovery_csv=sha(f"{REF}/BTCUSDT_4h_discovery.csv"), ylib_py=sha("/home/claude/yamato/ylib.py"), rlib_py=sha("/home/claude/rtc/rlib.py"),
                         ref_candidates_y1_y3=sha(f"{REF}/candidates_y1_y3.csv"), ref_candidates_y2=sha(f"{REF}/candidates_y2.csv"), ref_eval=sha(f"{REF}/eval_stufeA.json"),
                         **{f"ref_trades_{k}": sha(f"{REF}/trades_{k}_K1.csv") for k in ("Y1", "Y2", "Y3")}, **{f"ref_controls_{k}": sha(f"{REF}/controls_{k}_K1.csv") for k in ("Y1", "Y2", "Y3")},
                         **{f"ref_pairs_{k}": sha(f"{REF}/pairs_{k}.csv") for k in ("Y1", "Y2", "Y3")})
df = Y.load(f"{REF}/BTCUSDT_4h_discovery.csv")
C = R.cfg_btc_stufeA(); f = R.features(df, C); lo, hi = Y.swings(df)
cy = R.candidates_y1_y3(df, f, lo, C); y2 = R.candidates_y2(df, f, lo, hi, C)
cy.to_csv(f"{OUT}/candidates_y1_y3_rlib.csv", index=False); y2.to_csv(f"{OUT}/candidates_y2_rlib.csv", index=False)
print("Kandidaten", round(time.time() - t0), "s", flush=True)
cy0 = pd.read_csv(f"{REF}/candidates_y1_y3.csv"); y20 = pd.read_csv(f"{REF}/candidates_y2.csv")
cmp_frame("Kandidaten Y1/Y3", cy, cy0, ["t", "ctx", "y1", "y3", "fb_any", "y3_any"], ["lv_swing", "lv_nbar", "lv_zone"], ["y1_levels"])
check("Kandidaten Y1 Anzahl", int(cy.y1.sum()) == int(cy0.y1.sum()), f"{int(cy.y1.sum())} vs {int(cy0.y1.sum())}")
check("Kandidaten Y3 Anzahl", int(cy.y3.sum()) == int(cy0.y3.sum()), f"{int(cy.y3.sum())} vs {int(cy0.y3.sum())}")
cmp_frame("Kandidaten Y2", y2, y20, ["t", "s1", "s2", "h1", "ctx", "triple", "gyaku", "dup", "y2"], ["neck"])
ref = json.load(open(f"{REF}/eval_stufeA.json"))
rows_summary = {}
for kind, cand in (("Y1", cy[cy.y1]), ("Y2", y2[y2.y2]), ("Y3", cy[cy.y3])):
    trs = {}
    for cost in ("K0", "K1", "K2"):
        tr, lg = R.run_sleeve(cand.sort_values("t"), df, f, lo, kind, "TA", "EU", cost, C); trs[cost] = tr
        m0 = ref[kind]["costs"][f"r_net_{cost}"]; m1 = round(float(tr.r_net.mean()), 3) if len(tr) else None
        check(f"{kind} {cost}: n und mean r_net (3 Dez.) wie eval_stufeA.json", m0.get("n", 0) == len(tr) and (m0.get("mean") == m1), f"{m0.get('n')}/{m0.get('mean')} vs {len(tr)}/{m1}")
    tr = trs["K1"]; tr.to_csv(f"{OUT}/trades_{kind}_K1_rlib.csv", index=False)
    tr0 = pd.read_csv(f"{REF}/trades_{kind}_K1.csv")
    cmp_frame(f"Trades {kind} K1", tr, tr0, ["t", "e", "x", "bars"], ["entry", "stop0", "R", "exit", "r_net", "r_gross", "mfe_r", "mae_r", "stop_dist_atr"], ["reason"])
    # Kontrollen
    pool = Y.control_pool(cy, y2[y2.y2], df, f); pos = list(zip(tr.e.astype(int), tr.x.astype(int)))
    sigs = pd.DataFrame(dict(t=y2[y2.y2].set_index("t").loc[tr.t, "s2"].astype(int).to_numpy())) if kind == "Y2" else tr[["t"]]
    m = R.match_controls(sigs, pool, f, pos, C); ctr = R.run_controls(m, tr.t, df, f, lo, "TA", "EU", C); ctr.to_csv(f"{OUT}/controls_{kind}_K1_rlib.csv", index=False)
    c0 = pd.read_csv(f"{REF}/controls_{kind}_K1.csv")
    cmp_frame(f"Kontrollen {kind} alle Zeilen", ctr, c0, ["sig_t", "ctrl_t"], [], ["status"])
    ct = ctr[ctr.status == "traded"].reset_index(drop=True); ct0 = c0[c0.status == "traded"].reset_index(drop=True)
    cmp_frame(f"Kontrollen {kind} gehandelt", ct, ct0, ["e", "x", "bars", "t"], ["entry", "stop0", "R", "exit", "r_net", "r_gross", "mfe_r", "mae_r"], ["reason"])
    # gepaarte Differenzen d_r (aus Referenz-Paardatei) gegen Neuberechnung
    p0 = pd.read_csv(f"{REF}/pairs_{kind}.csv")
    prs = []
    for st in tr.t:
        cc = ct[ct.sig_t == st]
        if len(cc): prs.append(dict(t=st, d_r=float(tr[tr.t == st].r_net.iloc[0] - cc.r_net.mean()), n_ctrl=len(cc)))
    prs = pd.DataFrame(prs); prs.to_csv(f"{OUT}/pairs_{kind}_rlib.csv", index=False)
    cmp_frame(f"Paare {kind}", prs, p0, ["t", "n_ctrl"], ["d_r"])
    check(f"{kind}: Kontrollen matched/traded wie eval_stufeA.json", ref[kind]["controls"]["matched"] == len(m) and ref[kind]["controls"]["traded"] == len(ct), f"{ref[kind]['controls']['matched']}/{ref[kind]['controls']['traded']} vs {len(m)}/{len(ct)}")
    rows_summary[kind] = dict(signals=len(tr), controls_traded=len(ct), pairs=len(prs))
res["summary"] = rows_summary; res["seconds"] = round(time.time() - t0)
res["verdict"] = "REGRESSION FAIL" if res["fail"] else "REGRESSION PASS"
res["sha_outputs"] = {fn: sha(f"{OUT}/{fn}") for fn in sorted(os.listdir(OUT)) if fn.endswith(".csv")}
json.dump(res, open(f"{OUT}/regress_btc_result.json", "w"), indent=1)
print(res["verdict"], res["summary"], res["seconds"], "s")
