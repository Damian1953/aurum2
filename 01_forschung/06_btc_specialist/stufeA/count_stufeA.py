"""Kandidatenzaehlung, Abdeckung, Kontrollgruppen-Matching. Keine Performance-Auswertung: Outcome-Spalten werden nicht ausgegeben."""
import numpy as np, pandas as pd, sys, json, hashlib
sys.path.insert(0, "/home/claude/yamato"); import ylib as Y
df = Y.load("data/BTCUSDT_4h_discovery.csv")
f = Y.features(df); lo, hi = Y.swings(df)
cy = Y.candidates_y1_y3(df, f, lo); y2 = Y.candidates_y2(df, f, lo, hi)
P2 = pd.Timestamp("2021-01-01", tz="UTC"); block = np.where(df.t < P2, "P1", "P2")
rep = {}
rep["bars"] = dict(total=len(df), warmup=Y.WARMUP, evaluated=int((cy.t >= Y.WARMUP).sum()))
rep["swings"] = dict(lows=int(len(lo)), highs=int(len(hi)))
ctx = cy[cy.ctx]; rep["context_bars"] = dict(total=int(len(ctx)), P1=int((block[ctx.t] == "P1").sum()), P2=int((block[ctx.t] == "P2").sum()),
                                            k1_only=int(f.k1.iloc[Y.WARMUP:].sum()), k1_and_k2=int((f.k1 & f.k2).iloc[Y.WARMUP:].sum()))
# Episoden: zusammenhaengende Abschnitte mit K1
k1 = f.k1.to_numpy(); starts = int(((k1[1:]) & (~k1[:-1])).sum()); rep["k1_episodes"] = starts
def blk(ts): return dict(P1=int((block[ts] == "P1").sum()), P2=int((block[ts] == "P2").sum()))
y1c = cy[cy.y1]; y3c = cy[cy.y3]; y2c = y2[y2.y2] if len(y2) else y2
rep["candidates"] = dict(Y1=dict(total=int(len(y1c)), **blk(y1c.t.to_numpy())), Y2=dict(total=int(len(y2c)), **blk(y2c.t.to_numpy().astype(int)) if len(y2c) else {}, pairs_all=int(len(y2)), ctx_false=int((~y2.ctx).sum()) if len(y2) else 0, dup=int(y2.dup.sum()) if len(y2) else 0, triple=int(y2c.triple.sum()) if len(y2c) else 0),
                         Y3=dict(total=int(len(y3c)), **blk(y3c.t.to_numpy())),
                         fb_without_ctx=int((cy.fb_any & ~cy.ctx).sum()), y3_without_ctx=int((cy.y3_any & ~cy.ctx).sum()))
s1 = set(y1c.t); s3 = set(y3c.t); s2 = set(y2c.t.astype(int)) if len(y2c) else set()
rep["overlap"] = dict(Y1_and_Y3=len(s1 & s3), Y1_and_Y2=len(s1 & s2), Y2_and_Y3=len(s2 & s3), all3=len(s1 & s2 & s3), union=len(s1 | s2 | s3))
rep["y1_levels"] = y1c.y1_levels.value_counts().to_dict()
# Sleeves: Trigger/Status (Outcomes werden nicht ausgegeben)
trades = {}; logs = {}
for kind, c in (("Y1", y1c), ("Y2", y2c), ("Y3", y3c)):
    tr, lg = Y.run_sleeve(c.sort_values("t"), df, f, lo, kind); trades[kind] = tr; logs[kind] = lg
    st = lg.status.value_counts().to_dict() if len(lg) else {}
    tt = tr.t.to_numpy() if len(tr) else np.array([], int)
    sd = tr.stop_dist_atr if len(tr) else pd.Series(dtype=float)
    rep.setdefault("signals", {})[kind] = dict(status=st, traded=int(len(tr)), **blk(tt), stop_dist_atr=dict(median=round(float(sd.median()),2), min=round(float(sd.min()),2), max=round(float(sd.max()),2), over3=int((sd>3).sum())) if len(sd) else {},
                                                confirm_rate=round(len(tr) / max(1, len(c)), 3), open_at_cut=int((tr.reason == "cut").sum()) if len(tr) else 0)
    tr.to_csv(f"data/_private/trades_{kind}.csv", index=False)
# Kontrollpool und Matching
pool = Y.control_pool(cy, y2c, df, f); rep["control_pool"] = dict(size=int(len(pool)), **blk(pool))
match = {}
for kind in ("Y1", "Y2", "Y3"):
    tr = trades[kind]
    if not len(tr): match[kind] = "keine Signale"; continue
    pos = list(zip(tr.e.astype(int), tr.x.astype(int)))
    if kind == "Y2":   # U21: Referenzkerze s2
        ref = y2c.set_index("t").loc[tr.t, "s2"].astype(int).to_numpy()
        m = Y.match_controls(pd.DataFrame(dict(t=ref)), pool, f, pos); m["t_break"] = tr.t.to_numpy()
    else:
        m = Y.match_controls(tr[["t"]], pool, f, pos)
    cov = m.n_ctrl.value_counts().sort_index().to_dict()
    used = pd.Series([c for cs in m.ctrls for c in cs]); reuse = int((used.value_counts() > 1).sum()) if len(used) else 0
    # TA-Verfall auf Kontrollen
    ctrl_all = sorted(set(used.tolist()))
    conf = sum(1 for c in ctrl_all if Y.trigger_ta(c, df) is not None)
    match[kind] = dict(signals=int(len(m)), coverage={int(k): int(v) for k, v in cov.items()}, mean_ctrl=round(m.n_ctrl.mean(), 2),
                       unique_controls=len(ctrl_all), controls_reused=reuse, control_ta_confirm_rate=round(conf / max(1, len(ctrl_all)), 3),
                       median_pool_in_window=float(m.n_pool_window.median()))
    m.to_csv(f"data/_private/controls_{kind}.csv", index=False)
rep["matching"] = match
# Prüfsummen
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
cy.to_csv("data/candidates_y1_y3.csv", index=False); y2.to_csv("data/candidates_y2.csv", index=False)
rep["sha256"] = dict(input=sha("data/BTCUSDT_4h_discovery.csv"), ylib=sha("ylib.py"), candidates_y1_y3=sha("data/candidates_y1_y3.csv"), candidates_y2=sha("data/candidates_y2.csv"))
json.dump(rep, open("data/count_stufeA.json", "w"), indent=1)
print(json.dumps(rep, indent=1))
