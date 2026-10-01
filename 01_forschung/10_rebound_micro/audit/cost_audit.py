"""Outcome-blinder arithmetischer Audit des K1-Kostenmodells (REBOUND-MICRO v0.1).
Keine Parameteränderung, keine Outcomes. Liest nur die Kandidatentabellen der outcome-blinden Zählung."""
import json, sys, numpy as np, pandas as pd
sys.path.insert(0, "/home/claude/micro"); import mlib as M

BP = 1e4
rows = {}; checks = {}
for coin in ("BTC", "XRP", "DOT"):
    d = pd.read_csv(f"/home/claude/micro/count_{coin}.csv")
    m = d[(d.mech == "M1") & d.tight & ~d.gap_in_window & d.valid_stop].copy()
    # Einheitenpruefung, unabhaengig vom Bibliothekscode
    assert (m.entry > m.stop).all() and np.allclose(m.R, m.entry - m.stop) and np.allclose(m.entry_to_stop_atr4, m.R / m.atr4)
    stop_pct = (m.R / m.entry) * 100.0
    q = stop_pct.quantile([0.25, 0.5, 0.75]).to_dict()
    base = ((m.baseline_entry - (m.entry - m.R * 0)) * 0)  # Platzhalter, Baseline-Stop in % unten direkt aus ATR
    base_pct = (m.baseline_entry_to_stop_atr4 * m.atr4 / m.baseline_entry * 100.0).quantile([0.25, 0.5, 0.75]).to_dict()
    out = {"n": int(len(m)), "stop_pct_p25": q[0.25], "stop_pct_med": q[0.5], "stop_pct_p75": q[0.75],
           "baseline_stop_pct_p25": base_pct[0.25], "baseline_stop_pct_med": base_pct[0.5], "baseline_stop_pct_p75": base_pct[0.75],
           "entry_med": float(m.entry.median()), "R_med_price": float(m.R.median())}
    for k, K in M.COST.items():
        fee = K["fee"] * BP; fric = K["fric"] * BP; si = K["slip_in"] * BP; ss = K["slip_sl"] * BP
        entry_leg = fee + fric + si; target_leg = fee + fric; stop_leg = fee + fric + ss
        rt_target = entry_leg + target_leg; rt_stop = entry_leg + stop_leg
        comp = dict(entry_fee_bp=fee, exit_fee_target_bp=fee, exit_fee_stop_bp=fee, fric_per_side_bp=fric, slip_entry_bp=si, slip_target_bp=0.0, slip_stop_bp=ss,
                    roundtrip_target_bp=rt_target, roundtrip_stop_bp=rt_stop)
        # Kosten in R = Kosten in bp / (Stopdistanz in bp)
        for lab, sp in (("p25", q[0.25]), ("med", q[0.5]), ("p75", q[0.75])):
            sd_bp = sp * 100.0
            comp[f"cost_R_stop_path_{lab}"] = rt_stop / sd_bp
            comp[f"cost_R_target_path_{lab}"] = rt_target / sd_bp
            comp[f"entry_fee_R_{lab}"] = fee / sd_bp; comp[f"slip_stop_R_{lab}"] = ss / sd_bp; comp[f"slip_entry_R_{lab}"] = si / sd_bp
        # Unabhaengige Nachrechnung der in der Zaehlung ausgewiesenen cost_R (K1, Stop-Pfad)
        if k == "K1":
            recomputed = (rt_stop / BP) * m.entry / m.R
            comp["cost_R_recomputed_med"] = float(recomputed.median()); comp["cost_R_file_med"] = float(m.cost_R.median())
            comp["max_abs_diff_vs_file"] = float((recomputed - m.cost_R).abs().max())
            # alternative Sicht: Median der Verhaeltnisse vs Verhaeltnis der Mediane
            comp["cost_R_from_median_stop"] = rt_stop / (q[0.5] * 100.0)
        out[k] = comp
    rows[coin] = out
json.dump(rows, open("/home/claude/micro/audit/cost_audit_v1.json", "w"), indent=1)
for c, o in rows.items():
    print(c, "n", o["n"], "stop%% p25/med/p75 %.2f %.2f %.2f" % (o["stop_pct_p25"], o["stop_pct_med"], o["stop_pct_p75"]),
          "baseline stop%% med %.2f" % o["baseline_stop_pct_med"],
          "K1 stop-path R med %.3f" % o["K1"]["cost_R_stop_path_med"], "file med %.3f" % o["K1"]["cost_R_file_med"],
          "maxdiff %.1e" % o["K1"]["max_abs_diff_vs_file"])
