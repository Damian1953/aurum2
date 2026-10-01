# PORTABLE VERSION, generiert von tools/make_portable.py. NICHT VON HAND AENDERN.
# Quelle (eingefroren): 01_forschung/11_delayed_trend/dtlib/measure_dt.py  sha256 05014537d686877b886ddf8cb6ebf6f80a2f25fb21c72c383d6d126b2561ad12
# Regeln: paths, sha_self. Arbeitsbereich: AURUM_ROOT (Default: Ordner '..' relativ zu dieser Datei).
import os as _aos; _AR = _aos.environ.get("AURUM_ROOT") or _aos.path.abspath(_aos.path.join(_aos.path.dirname(_aos.path.abspath(__file__)), ".."))
_FROZEN_SELF = _aos.path.join(_aos.path.dirname(_aos.path.abspath(__file__)), "measure_dt.py")  # eingefrorenes Original im Arbeitsbereich
"""Outcome-blinde Messung DELAYED-TREND v1.0 je Coin. Aufruf: python3 measure_dt.py COIN -> out/{COIN}_entries.csv, out/{COIN}_contexts.csv, out/{COIN}_measure.json"""
import sys, os, json, hashlib, numpy as np, pandas as pd
sys.path.insert(0, _AR + "/dt"); sys.path.insert(0, _AR + "/rtc"); import dtlib as D; import rlib as R; Y = R.Y
COIN = sys.argv[1]; OUT = _AR + "/dt/out"; os.makedirs(OUT, exist_ok=True)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
CNT = {"BTC": _AR + "/rtc/count_BTC_B", "XRP": _AR + "/rtc/count_XRP", "DOT": _AR + "/rtc/count_DOT"}[COIN]
JS = {"BTC": "count_BTC_B.json", "XRP": "count_XRP.json", "DOT": "count_DOT.json"}[COIN]
cnt = json.load(open(f"{CNT}/{JS}"))
spot = _AR + f"/holdout/discovery/{COIN}USDT_spot4h_discovery.csv"; assert "validation" not in spot and os.environ.get("AURUM_VALIDATION") is None
assert sha(spot) == cnt["sha"]["spot"] and sha(f"{CNT}/candidates_y1_y3.csv") == cnt["sha"]["candidates_y1_y3"] and sha(f"{CNT}/candidates_y2.csv") == cnt["sha"]["candidates_y2"]
C = R.cfg_btc_stufeA() if COIN == "BTC" else R.cfg_alt()
df = Y.load(spot); f = R.features(df, C); lo, hi = Y.swings(df); n = len(df)
cy = pd.read_csv(f"{CNT}/candidates_y1_y3.csv"); y2 = pd.read_csv(f"{CNT}/candidates_y2.csv")
ctx = D.contexts(cy, y2, df, f); E = D.entries(ctx, df, f, lo, COIN)
blk = np.array([R.block_of(x, COIN) for x in df["t"]]); E["block"] = [blk[int(e)] if np.isfinite(e) else blk[int(t)] for e, t in zip(E.get("e", pd.Series([np.nan] * len(E))), E.t)]
E["year"] = [int(df.t.iat[int(e)].year) if np.isfinite(e) else int(df.t.iat[int(t)].year) for e, t in zip(E.get("e", pd.Series([np.nan] * len(E))), E.t)]
ctx.to_csv(f"{OUT}/{COIN}_contexts.csv", index=False); E.to_csv(f"{OUT}/{COIN}_entries.csv", index=False)
q = lambda x: (lambda v: dict(n=int(len(v)), p25=round(float(np.percentile(v, 25)), 3), median=round(float(np.median(v)), 3), p75=round(float(np.percentile(v, 75)), 3)) if len(v) else dict(n=0))(np.asarray(pd.Series(x).dropna(), float))
rep = dict(coin=COIN, mode="cfg_btc_stufeA" if COIN == "BTC" else "cfg_alt", sha=dict(spot=sha(spot), candidates_y1_y3=cnt["sha"]["candidates_y1_y3"], candidates_y2=cnt["sha"]["candidates_y2"], dtlib=sha(_AR + "/dt/dtlib.py"), rlib=sha(_AR + "/rtc/rlib.py"), measure=sha(_FROZEN_SELF)),
           params=D.P, bars=int(n))
# 1. Kontexte
rep["contexts"] = {}
for src in ("S1", "S2"):
    c_ = ctx[ctx.src == src]
    rep["contexts"][src] = dict(n=int(len(c_)), invalidated_within_window=int((c_.inv_bar >= 0).sum()), bars_to_invalidation_median=float((c_.inv_bar - c_.t)[c_.inv_bar >= 0].median()) if (c_.inv_bar >= 0).any() else None,
                                no_target=int(c_.h_pre.isna().sum()), by_block={b: int((blk[c_.t.astype(int)] == b).sum()) for b in sorted(set(blk)) if b != "none"})
cells = {}
for src in ("S1", "S2"):
    for fam in ("DT1", "DT2", "DT3"):
        x = E[(E.src == src) & (E.fam == fam)]; ent = x[x.status == "entry"].sort_values("e")
        d = dict(contexts=int(len(x)), status=x.status.value_counts().to_dict(), entries=int(len(ent)), share_contexts_with_entry=round(float(len(ent) / max(1, len(x))), 3))
        if len(ent):
            d["delay_bars"] = q(ent.delay); d["delay_days"] = q(ent.delay / 6.0)
            d["stop_atr"] = q(ent.stop_atr); d["stop_pct"] = q(ent.stop_pct); d["cost_R_K1"] = q(ent.cost_R_K1)
            d["dist_target_atr"] = q(ent.dist_target_atr); d["dist_target_pct"] = q(ent.dist_target_pct); d["target_below_entry"] = int(ent.target_below_entry.sum())
            d["entry_above_level"] = int((ent.entry > ent.level).sum())
            d["rr_geo_gross"] = q(ent.rr_geo_gross); d["rr_geo_net_K1"] = q(ent.rr_geo_net_K1); d["p_be_geo"] = q(ent.p_be_geo)
            d["share_entries_meeting_A_B_C"] = round(float(((ent.stop_atr <= 3.0) & (ent.cost_R_K1 <= 0.40) & (ent.rr_geo_gross >= 1.5)).mean()), 3)
            # Ueberlappung: Einstieg innerhalb 180 Kerzen nach dem vorigen Einstieg derselben Zelle (Obergrenze/Untergrenze)
            e_ = ent.e.to_numpy(); ov = int(sum(1 for i in range(1, len(e_)) if e_[i] - e_[i - 1] <= D.P["window"]))
            d["overlap_within_180"] = ov; d["expected_lower"] = int(len(ent) - ov); d["expected_upper"] = int(len(ent))
            d["by_block"] = ent.block.value_counts().to_dict(); d["by_year"] = {int(k): int(v) for k, v in ent.year.value_counts().sort_index().items()}
            if fam == "DT2": d["failed_holds_before_entry"] = q(ent.failed_holds)
            if fam == "DT3": d["box_width_atr"] = q(ent.box_width_atr)
            # Gate (Zellenebene)
            gate = dict(A_stop_median_le_3=bool(d["stop_atr"]["median"] <= 3.0), B_cost_median_le_0_40=bool(d["cost_R_K1"]["median"] <= 0.40),
                        C_rr_gross_median_ge_1_5=bool(d["rr_geo_gross"]["median"] >= 1.5), D_rr_gross_p25_ge_1=bool(d["rr_geo_gross"]["p25"] >= 1.0), E_expected_ge_20=bool(d["expected_lower"] >= 20))
            gate["pass"] = all(gate.values()); d["gate"] = gate
        else: d["gate"] = {"pass": False, "note": "no entries"}
        cells[f"{src}x{fam}"] = d
rep["cells"] = cells
# 12. Ueberschneidung der Familien je Kontext
ov = {}
for src in ("S1", "S2"):
    x = E[(E.src == src) & (E.status == "entry")]; g = x.groupby("t").fam.apply(set)
    ov[src] = dict(contexts_with_entry_any=int(len(g)), DT1_DT2=int(sum(1 for s in g if {"DT1", "DT2"} <= s)), DT1_DT3=int(sum(1 for s in g if {"DT1", "DT3"} <= s)), DT2_DT3=int(sum(1 for s in g if {"DT2", "DT3"} <= s)), all3=int(sum(1 for s in g if len(s) == 3)),
                   same_entry_bar=int(sum(1 for _, gg in x.groupby("t") if gg.e.nunique() < len(gg))))
rep["overlap_families"] = ov
# 14. Hochrechnung ETH/SOL nach Kerzenzahl (Manifest v1.1: ETH 13950, SOL 7427 4h-Kerzen)
rep["expected_eth_sol"] = {c: {k: dict(lower=round(v["expected_lower"] / n * m, 1), upper=round(v["expected_upper"] / n * m, 1)) for k, v in cells.items() if "expected_lower" in v} for c, m in (("ETH", 13950), ("SOL", 7427))}
rep["sha_outputs"] = dict(entries=sha(f"{OUT}/{COIN}_entries.csv"), contexts=sha(f"{OUT}/{COIN}_contexts.csv"))
json.dump(rep, open(f"{OUT}/{COIN}_measure.json", "w"), indent=1, default=lambda x: None if isinstance(x, float) and np.isnan(x) else (int(x) if isinstance(x, (np.integer,)) else (float(x) if isinstance(x, np.floating) else (bool(x) if isinstance(x, np.bool_) else str(x)))))
for k, v in cells.items():
    print(COIN, k, "ctx", v["contexts"], "entries", v["entries"], "delay", v.get("delay_bars", {}).get("median"), "stop_atr", v.get("stop_atr", {}).get("median"), "cost", v.get("cost_R_K1", {}).get("median"),
          "rr", v.get("rr_geo_gross", {}), "gate", v["gate"].get("pass"), v["status"])
