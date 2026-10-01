# PORTABLE VERSION, generiert von tools/make_portable.py. NICHT VON HAND AENDERN.
# Quelle (eingefroren): 01_forschung/06_btc_specialist/stufeA/lookahead_test.py  sha256 f9be222dc1774de477870f185c31b1a426760841148de478893366864af3316b
# Regeln: paths. Arbeitsbereich: AURUM_ROOT (Default: Ordner '..' relativ zu dieser Datei).
import os as _aos; _AR = _aos.environ.get("AURUM_ROOT") or _aos.path.abspath(_aos.path.join(_aos.path.dirname(_aos.path.abspath(__file__)), ".."))
import numpy as np, pandas as pd, sys, json, time
sys.path.insert(0, _AR + "/yamato"); import ylib as Y
t0 = time.time()
df = Y.load("data/BTCUSDT_4h_discovery.csv")
def run(d):
    f = Y.features(d); lo, hi = Y.swings(d)
    cy = Y.candidates_y1_y3(d, f, lo); y2 = Y.candidates_y2(d, f, lo, hi)
    return f, lo, hi, cy, y2
f, lo, hi, cy, y2 = run(df)
res = {}
# 1) Truncation 2022-06-30
cut = int((df.t < pd.Timestamp("2022-07-01", tz="UTC")).sum()) - 1
d2 = df.iloc[:cut + 1].reset_index(drop=True)
f2, lo2, hi2, cy2, y22 = run(d2)
k = cut - 4
fe = f.iloc[:k + 1].to_numpy(dtype=float); fe2 = f2.iloc[:k + 1].to_numpy(dtype=float)
eq_feat = bool(np.array_equal(np.nan_to_num(fe, nan=-9e9), np.nan_to_num(fe2, nan=-9e9)))
lo_a = lo[lo + 3 <= k]; lo_b = lo2[lo2 + 3 <= k]
eq_sw = bool(np.array_equal(lo_a, lo_b) and np.array_equal(hi[hi + 3 <= k], hi2[hi2 + 3 <= k]))
ca = cy[cy.t <= k].reset_index(drop=True); cb = cy2[cy2.t <= k].reset_index(drop=True)
eq_cand = bool(ca.astype(str).equals(cb.astype(str)))
ya = y2[y2.t <= k].reset_index(drop=True); yb = y22[y22.t <= k].reset_index(drop=True)
eq_y2 = bool(ya.astype(str).equals(yb.astype(str)))
res["truncation"] = dict(cut_bar=int(cut), cut_time=str(df.t.iat[cut]), compare_upto=int(k), features_equal=eq_feat,
                         swings_equal=eq_sw, candidates_equal=eq_cand, y2_equal=eq_y2, n_y2_compared=int(len(ya)))
# 2) Permutation of future bars at 25 random points
rng = np.random.default_rng(20260917); pts = sorted(rng.integers(500, len(df) - 400, 25).tolist())
perm_ok = True; details = []
for t in pts:
    d3 = df.copy(); fut = d3.iloc[t + 1:].sample(frac=1.0, random_state=int(t)).reset_index(drop=True)
    d3 = pd.concat([d3.iloc[:t + 1], fut], ignore_index=True); d3["t"] = df["t"].to_numpy()
    f3 = Y.features(d3); lo3, hi3 = Y.swings(d3)
    a = f.iloc[:t + 1].to_numpy(dtype=float); b = f3.iloc[:t + 1].to_numpy(dtype=float)
    ok_f = np.array_equal(np.nan_to_num(a, nan=-9e9), np.nan_to_num(b, nan=-9e9))
    ok_lv = Y.levels_at(t, df, f, lo) == Y.levels_at(t, d3, f3, lo3)
    ok_ctx = Y.context_at(t, df, f, lo)[0] == Y.context_at(t, d3, f3, lo3)[0]
    ok_fb = Y.failed_breakdown(t, df, f, Y.levels_at(t, df, f, lo)) == Y.failed_breakdown(t, d3, f3, Y.levels_at(t, d3, f3, lo3))
    ok_y3 = Y.y3_flag(t, f) == Y.y3_flag(t, f3)
    y2_3 = Y.candidates_y2(d3, f3, lo3, hi3)
    ok_y2 = y2[y2.t <= t - 3].astype(str).reset_index(drop=True).equals(y2_3[y2_3.t <= t - 3].astype(str).reset_index(drop=True))
    ok = bool(ok_f and ok_lv and ok_ctx and ok_fb and ok_y3 and ok_y2)
    perm_ok &= ok; details.append(dict(t=int(t), ok=ok, f=bool(ok_f), lv=bool(ok_lv), ctx=bool(ok_ctx), fb=bool(ok_fb), y3=bool(ok_y3), y2=bool(ok_y2)))
res["permutation"] = dict(points=len(pts), all_ok=bool(perm_ok), details=details)
res["runtime_s"] = round(time.time() - t0, 1)
json.dump(res, open("data/lookahead_test.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "permutation"}, indent=1)); print("permutation all_ok", perm_ok, [d for d in details if not d["ok"]])
