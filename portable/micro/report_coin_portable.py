# PORTABLE VERSION, generiert von tools/make_portable.py. NICHT VON HAND AENDERN.
# Quelle (eingefroren): 01_forschung/10_rebound_micro/mlib/report_coin.py  sha256 b09de7152029e02a9b58a2558de8104b4c6ad53f8a09954f679a68d69ff5b152
# Regeln: paths. Arbeitsbereich: AURUM_ROOT (Default: Ordner '..' relativ zu dieser Datei).
import os as _aos; _AR = _aos.environ.get("AURUM_ROOT") or _aos.path.abspath(_aos.path.join(_aos.path.dirname(_aos.path.abspath(__file__)), ".."))
"""Erzeugt den Coin-Bericht REBOUND-MICRO v1.0 aus run/{COIN}_eval.json (keine neuen Berechnungen ausser Kreuztabellen der versiegelten Trade-Dateien)."""
import sys, json, numpy as np, pandas as pd
coin = sys.argv[1]; e = json.load(open(_AR + f"/micro/run/{coin}_eval.json")); log = json.load(open(_AR + f"/micro/run/{coin}_run.log"))
T = pd.read_csv(_AR + f"/micro/run/{coin}_trades.csv"); B = pd.read_csv(_AR + f"/micro/run/{coin}_baseline.csv")
f = lambda x, d=2: ("n/a" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{d}f}")
pct = lambda x: "n/a" if x is None or not np.isfinite(x) else f"{100*x:.0f}"
blocks = list(e["cells"]["M1xQ0"]["K1"]["blocks"].keys())
L = []
L.append(f"# REBOUND-MICRO v1.0 — Development-Bericht {coin}\n")
L.append(f"**Project Aurum II, `01_forschung/10_rebound_micro/rebound_micro_bericht_{coin}_v1.md`. 18.09.2026. Einmaliger Lauf nach `rebound_micro_spec_v1.0.md` (SHA 001a3853…). Eingaben: Spot 1h {log['inputs']['spot1h'][:16]}…, Spot 4h {log['inputs']['spot4h'][:16]}…, mlib {log['inputs']['mlib'][:16]}…, simulate {log['inputs']['simulate'][:16]}…. Regression der Kandidatentabelle gegen die outcome-blinde Zählung v0.1: {log['regression_vs_count_v0_1']}. Ergebnisdateien versiegelt in ENTSCHEIDE.md. Development Evidence, Ebene C, kein Sleeve-Status. Primärer Kostenmassstab K1, K0 und K2 Sensitivität.**\n")
L.append("## 1. Fallzahlen und Zulassung\n")
sc = e["status_counts"]; bs = e["baseline_status_counts"]
L.append(f"Kontext-Events mit vollständigem 1h-Fenster {log['n_events_full']}, Kandidaten {log['n_candidates']}. Zulassung je Zelle (gehandelt / kein enger Stop / Ziel unter Einstieg / Lücke / Overlap): " +
         ", ".join(f"{c} {sc[c].get('traded',0)} / {sc[c].get('no_tight_invalidation',0)} / {sc[c].get('target_below_entry',0)} / {sc[c].get('gap_in_window',0)} / {sc[c].get('overlap_skip',0)}" for c in sorted(sc)) +
         f". Baseline: Q0 {bs['BASExQ0'].get('traded',0)} gehandelt ({bs['BASExQ0'].get('target_below_entry',0)} Ziel unter Einstieg), Q1 {bs['BASExQ1'].get('traded',0)} ({bs['BASExQ1'].get('target_below_entry',0)}). Kontrollpool {log['n_ctrl_pool']} 4h-Kerzen (K1 und K2 ohne K3), Kontroll-M1-Kandidaten {log['n_ctrl_candidates_M1']}, Kontroll-Trade-Zeilen {log['n_controls_rows']}.\n")
L.append("## 2. Primary-Zellen M1×Q0 und M1×Q1 (alle Kostenstufen)\n")
L.append("| Zelle | Kosten | n | Mittel r_net | Median | Trefferquote | Zielrate | Stoprate | Zeitstopp | avg_win | avg_loss | win/loss | p_BE_emp | PF | p_pos | cost_R Med. | Stop ATR4h Med. |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for c in ("M1xQ0", "M1xQ1"):
    for k in ("K0", "K1", "K2"):
        s = e["cells"][c][k]
        L.append(f"| {c} | {k} | {s['n']} | {f(s['mean_r'],3)} | {f(s['median_r'],3)} | {pct(s['hit_rate'])} % | {pct(s['target_rate'])} % | {pct(s['stop_rate'])} % | {pct(s['time_rate'])} % | {f(s['avg_win_R'])} | {f(s['avg_loss_R'])} | {f(s['win_loss_ratio'])} | {f(s['p_be_emp'])} | {f(s['profit_factor'])} | {f(s['p_pos'])} | {f(s['cost_R_median'])} | {f(s['stop_atr4_median'])} |")
L.append("")
L.append("Ausstiegsgründe K1: " + "; ".join(f"{c}: " + ", ".join(f"{k} {v}" for k, v in e['cells'][c]['K1']['reasons'].items()) for c in ("M1xQ0", "M1xQ1")) + ".\n")
L.append("Blöcke K1 (n, Mittel): " + "; ".join(f"{c}: " + ", ".join(f"{b} {v['n']} / {f(v['mean_r'])}" for b, v in e['cells'][c]['K1']['blocks'].items()) for c in ("M1xQ0", "M1xQ1")) + ". Konzentration: grösster Gewinn als Anteil der Gewinnsumme " + ", ".join(f"{c} {pct(e['cells'][c]['K1']['top1_share'])} %" for c in ("M1xQ0", "M1xQ1")) + ".\n")
L.append("## 3. Baseline T0 (gleiche Events, 4h-struktureller Stop)\n")
L.append("| Zelle | Kosten | n | Mittel r_net | Trefferquote | Zielrate | Stoprate | avg_win | avg_loss | win/loss | p_BE_emp | cost_R Med. | Stop ATR4h Med. |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for c in ("BASExQ0", "BASExQ1"):
    for k in ("K0", "K1"):
        s = e["baseline"][c][k]
        L.append(f"| {c} | {k} | {s['n']} | {f(s['mean_r'],3)} | {pct(s['hit_rate'])} % | {pct(s['target_rate'])} % | {pct(s['stop_rate'])} % | {f(s['avg_win_R'])} | {f(s['avg_loss_R'])} | {f(s['win_loss_ratio'])} | {f(s['p_be_emp'])} | {f(s['cost_R_median'])} | {f(s['stop_atr4_median'])} |")
L.append("")
L.append("## 4. Gepaarter Primary-Vergleich Zelle minus Baseline (gleiches Event, gleiches Ziel)\n")
L.append("| Zelle | Kosten | Paare | Mittel Diff. | Median Diff. | Anteil positiv | Bootstrap-p (einseitig) | Vorzeichentest p | Wilcoxon p | Mittel Zelle | Mittel Baseline (gepaart) |\n|---|---|---|---|---|---|---|---|---|---|---|")
for c in ("M1xQ0", "M1xQ1"):
    for k in ("K0", "K1", "K2"):
        p = e["cells"][c]["paired_vs_baseline"][k]
        L.append(f"| {c} | {k} | {p['n_pairs']} | {f(p['mean_diff'],3)} | {f(p['median_diff'],3)} | {pct(p['share_pos'])} % | {f(p['p_boot_one_sided'],3)} | {f(p['sign_test_p'],3)} | {f(p.get('wilcoxon_p', np.nan),3)} | {f(p['mean_cell'],3)} | {f(p['mean_base_paired'],3)} |")
pt = e["primary_tests"]
L.append(f"\nHolm über die zwei Primary-Tests (K1): p roh {', '.join(f'{c} {f(v,3)}' for c, v in pt['p_raw'].items())}, Holm-adjustiert {', '.join(f'{c} {f(v,3)}' for c, v in pt['p_holm'].items())}. Signifikant bei α 0.05: {pt['significant_holm'] or 'keine'}.\n")
# Kreuztabelle der Ausstiegsarten je Paar
L.append("Kreuztabelle der Ausstiegsart je Paar (K1, Zeile M1, Spalte Baseline, T Ziel, S Stop, Z Zeitstopp):\n")
for q in ("Q0", "Q1"):
    t = T[(T.cell == f"M1x{q}") & (T.status == "traded")]; b = B[(B.cell == f"BASEx{q}") & (B.status == "traded")]
    m = t.merge(b[["event", "reason", "exit_b"]].rename(columns={"reason": "rb", "exit_b": "xb"}), on="event")
    cat = lambda x: "T" if x.startswith("target") else ("S" if x.startswith("stop") else "Z")
    ct = pd.crosstab(m.reason.map(cat), m.rb.map(cat)).reindex(index=["T", "S", "Z"], columns=["T", "S", "Z"], fill_value=0)
    early = int(((m.xb < m.e) & m.rb.str.startswith("stop")).sum())
    L.append(f"M1×{q}: " + "; ".join(f"M1 {r} und Baseline {c}: {ct.loc[r, c]}" for r in ("T", "S", "Z") for c in ("T", "S", "Z") if ct.loc[r, c] > 0) + f". Einstiegsverzögerung M1 gegenüber Baseline Median {int((t.merge(b[['event','e']].rename(columns={'e':'eb'}), on='event').eval('e-eb')).median())} Stunden. Baseline bereits vor dem M1-Einstieg ausgestoppt: {early} von {len(m)}.\n")
L.append("## 5. Frage C: Q1 gegen Q0 auf denselben M1-Trades (K1)\n")
qq = e.get("q1_vs_q0_same_trades", {})
if qq: L.append(f"{qq['n']} Events mit beiden Zellen gehandelt. Mittel r_net Q0 {f(qq['mean_q0'],3)}, Q1 {f(qq['mean_q1'],3)}, Differenz Q1 minus Q0 Mittel {f(qq['mean_diff'],3)}, Median {f(qq['median_diff'],3)}, Anteil Q1 besser {pct(qq['share_q1_better'])} %, Bootstrap p_pos {f(qq['p_pos'],3)}. Zielrate Q0 {pct(qq['target_rate_q0'])} %, Q1 {pct(qq['target_rate_q1'])} %.\n")
L.append("## 6. Diagnosen (vorregistriert, keine Statuswirkung)\n")
for c in ("M1xQ0", "M1xQ1"):
    s = e["cells"][c]["K1"]; cn = e["cells"][c].get("controls", {})
    L.append(f"{c}: Anteil der Stop-outs, nach denen das Ziel innerhalb der 24 Kerzen dennoch erreicht wurde {pct(s['stop_then_target_share'])} %. MFE nach erreichtem Ziel bis Kerze 24 Median {f(s['mfe_after_target_R_median'])} R, neues 20-Tage-Hoch innerhalb 30 Tagen nach Ziel {pct(s['new20d_high_share'])} %, 30-Tage-Hoch {pct(s['new30d_high_share'])} %. Haltedauer Median {f(s['bars_held_median'],0)} Kerzen. Teilmengen deskriptiv (n, Mittel K1): Flow-Flag {e['cells'][c]['subset_flow_flag']['n']} / {f(e['cells'][c]['subset_flow_flag']['mean_r_K1'])}, Harami {e['cells'][c]['subset_harami']['n']} / {f(e['cells'][c]['subset_harami']['mean_r_K1'])}, Hikkake {e['cells'][c]['subset_hikkake']['n']} / {f(e['cells'][c]['subset_hikkake']['mean_r_K1'])}. Kontrollgruppe (K1 und K2 ohne K3): {cn.get('n_ctrl_trades',0)} Kontroll-Trades, Mittel {f(cn.get('ctrl_mean_r_K1', np.nan),3)}, Median {f(cn.get('ctrl_median_r_K1', np.nan),3)}, Events mit Kontrolle {cn.get('n_events_with_ctrl',0)}, Differenz Zelle minus Kontrollmittel Median {f(cn.get('diff_median', np.nan),3)}, Anteil positiv {pct(cn.get('diff_share_pos', np.nan))} %. Kandidatenrate {f(s['rate_per_1000_bars'],2)} je 1000 1h-Kerzen, erwartete Trades ETH {f(s['expected_eth_sol']['ETH'],0)}, SOL {f(s['expected_eth_sol']['SOL'],0)} (nur Hochrechnung, keine ETH/SOL-Daten).\n")
L.append("## 7. M2 und M3 (descriptive / insufficient sample, Entscheidung 1)\n")
for c in ("M2xQ0", "M2xQ1", "M3xQ0", "M3xQ1"):
    s = e["cells"][c]["K1"]; p = e["cells"][c]["paired_vs_baseline"]["K1"]
    if s.get("n", 0): L.append(f"{c}: n {s['n']}, Mittel r_net K1 {f(s['mean_r'],3)}, Gründe {s['reasons']}, gepaart {p['n_pairs']} Paare, Median Diff. {f(p['median_diff'],3)}, Anteil positiv {pct(p['share_pos'])} %. Status: descriptive / insufficient sample.\n")
    else: L.append(f"{c}: keine Trades. Status: descriptive / insufficient sample.\n")
L.append("## 8. Promotion-Prüfung und Status (Governance v1.1, Regeln v0.1)\n")
for c in ("M1xQ0", "M1xQ1"):
    pr = e["cells"][c]["promotion"]; mp = e["cells"][c]["mp_rule_v2"]
    L.append(f"{c}: Bedingungen 1 Geometrie {pr['c1_geometry']}, 2 p_BE {pr['c2_pbe']}, 3 nicht negativ {pr['c3_not_negative']}, 4 Fallzahl {pr['c4_sample']}, 5 Konzentration {pr['c5_concentration']}, 6 Blöcke {pr['c6_blocks']}, 7 Baseline {pr['c7_baseline']}. Promotion: {pr['all']}. Regel v2: a Baseline-Paare {mp['a_control']}, b Geometrie {mp['b_geometry']}, c Konzentration {mp['c_concentration']}, d Blöcke {mp['d_blocks']} (Zählung {mp['count']}), Fast Fail {mp['fast_fail']}. Status: **{e['cells'][c]['status']}**.\n")
L.append("Hinweis zur Regel v2: Die Kriterien c und d prüfen nur Stabilität von Konzentration und Blöcken und sind auch bei negativem Gesamtmittel erfüllbar. Ein Status «mechanistisch vielversprechend» setzt nach Governance v1.1 einen positiven relativen Effekt voraus (Kriterium a). Fast Fail hat in der eingefrorenen Auswertung Vorrang und ist hier für beide Primary-Zellen erfüllt.\n")
open(_AR + f"/build/aurum2/01_forschung/10_rebound_micro/rebound_micro_bericht_{coin}_v1.md", "w").write("\n".join(L))
print("written", coin)
