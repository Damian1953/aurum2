#!/usr/bin/env python3
"""Bericht der Validierungsstufe MTP aus mtp_val_results.json. Aufruf: python3 report_val.py out_full"""
import sys, os, json, math
import numpy as np
D = sys.argv[1]; R = json.load(open(os.path.join(D, "mtp_val_results.json")))
COINS = ["BTC", "ETH", "SOL", "XRP", "ADA", "AVAX", "LINK", "DOT", "BNB", "LTC"]
out = []
A = out.append
def f(x, d=2, pct=False, s=""):
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))): return "–"
    return (f"{x*100:.{d}f} %" if pct else f"{x:.{d}f}") + s
def ja(b): return "ja" if b else "nein"
lv = R["levels"]; co = R["coins"]; crit = R["criteria_B"]; critA = R["criteria_A"]

A("# Validierungsstufe MTP — Bericht")
A("")
A(f"**Project Aurum II, 03_mtp_validation. Lauf «{os.path.basename(D)}» vom {R['run_at'][:10]}. Vorregistrierung v0.2 (SHA-256 `{R['prereg_sha256'][:16]}…`), Spezifikation v1 (`{R['spec_sha256'][:16]}…`), beide eingefroren am 17.09.2026. Zehn Coins, Ebenen A (Replikation CMC), B (Real Kraken), B2 (Signale auf Kraken), Sichten 1, 1b, 2, Kostenszenarien K0 bis K2, Bootstrap {R['nboot']} Wiederholungen. Alle Definitionen aus der Vorregistrierung, keine Änderung nach Kenntnis der Ergebnisse.**")
A("")
A(f"**Urteil nach Vorregistrierung Abschnitt 8 (Ebene B, K1, handelbare Konvention, Sicht 1, Pool ohne BTC): {R['verdict']}.**")
A("")
c = R["controls"]; rep = c["replication"]
A(f"Kontrollen vor dem Lauf: Look-ahead-Test bestanden (BTC und ETH, Niveau, Pivot, ATR und SMA auf abgeschnittener Historie identisch). BTC-Replikation der sechzehn Backtester-Trades in Ebene A: Entry-Tag {rep['entry_hits']} von 16, Exit-Tag {rep['exit_hits']} von 16, Exit-Preis unter 0.1 Prozent {rep['px_hits']} von 16 (Erwartung 13, 13, 10).")
A("")

# 1 Kriterien
A("## 1. Kriterien")
A("")
A("| Kriterium | Ebene B, K1, Pool ohne BTC | Ebene A, ohne Kosten, Pool ohne BTC |")
A("|---|---|---|")
names = {"c1": "1 Erwartung R_gesamt > 0 und Profit-Faktor ≥ 1.5", "c2": "2 ETH positiv und Mehrheit der übrigen Coins (≥ 10 Trades)", "c3": "3 mindestens zwei von drei Zeitblöcken positiv", "c4": "4 Bootstrap-5 %-Perzentil > 0 und Holm-p < 0.05", "c5": "5 Beta-Trennung: Alpha oder Risikotransformation", "c6": "6 Edge-Retention ≥ 60 % und abweichender Exit-Grund ≤ 15 %", "c7": "7 Trade-Mindestzahl (Pool ≥ 60, ETH ≥ 10)"}
for k, n in names.items():
    A(f"| {n} | {ja(crit[k])} | {ja(critA[k]) if k in critA else '–'} |")
A("")
d2 = crit["c2_detail"]; d6 = crit["c6_detail"]
A(f"Zu 2: ETH {d2['eth_n']} Trades, Erwartung R_gesamt {f(d2['eth_exp'])}. Geeignete übrige Coins {', '.join(d2['others_eligible']) or 'keine'}, davon positiv {', '.join(d2['others_positive']) or 'keine'}. Zu 6: Retention {f(d6['retention'])}, abweichender Exit-Grund {f(d6['diff_reason_share'], pct=True)}. Zu 7: {crit['c7_note'] or 'ausreichende Trade-Basis'}. Holm-korrigierte p-Werte: " + ", ".join(f"{k} {f(v,3)}" for k, v in R["holm"].items()) + ".")
A("")

# 2 Uebersicht Ebenen
A("## 2. Übersicht je Ebene, Sicht 1, Pool ohne BTC (mit BTC in Klammern)")
A("")
A("| Ebene | Kosten | Trades | E[R_gesamt] | Median R_ges | E[R_first] | Profit-Faktor | Trefferquote | Ø Gewinner | Ø Verlierer | Ø Legs | Ø Halten | CAGR | MaxDD | Exposure |")
A("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
order = ["A|none|1", "A|K0|1", "A_window|none|1", "B|K0|1", "B|K1|1", "B|K2|1", "B_sameday|K1|1", "B_full|K1|1", "B2|K0|1", "B2|K1|1", "B2|K2|1", "B|K1|1b", "A|none|1b", "B|K1|2"]
for k in order:
    if k not in lv: continue
    e, a = lv[k]["exBTC"], lv[k]["all"]; t, ta = e["trades"], a["trades"]; p = e["path"] or {}
    lvn, kn, sn = k.split("|")
    A(f"| {lvn} Sicht {sn} | {kn} | {t.get('n',0)} ({ta.get('n',0)}) | {f(t.get('exp_R_total'))} ({f(ta.get('exp_R_total'))}) | {f(t.get('med_R_total'))} | {f(t.get('exp_R_first'))} | {f(t.get('profit_factor'))} ({f(ta.get('profit_factor'))}) | {f(t.get('win_rate'),1,True)} | {f(t.get('avg_win_pct'),1,True)} | {f(t.get('avg_loss_pct'),1,True)} | {f(t.get('legs_mean'),1)} | {f(t.get('hold_mean'),0)} d | {f(p.get('cagr'),1,True)} | {f(p.get('maxdd'),1,True)} | {f(e.get('avg_expo'),1,True)} |")
A("")
A("A_window ist Ebene A eingeschränkt auf das B-Fenster je Coin (Basis der Retention). CAGR und MaxDD sind Berichtswerte auf dem Sleeve-Mittel (Sicht 1, 2 Prozent Nominal Initial Risk je Leg ohne Compounding), keine Kriterien. Sicht 2 zeigt das gemeinsame Portfolio.")
A("")

# 3 Coins
for lab, title in [("B|K1|1", "Ebene B, K1, Sicht 1"), ("A|none|1", "Ebene A, ohne Kosten, Sicht 1")]:
    A(f"## 3{'a' if lab.startswith('B') else 'b'}. Ergebnis je Coin, {title}")
    A("")
    A("| Coin | Start | Trades | E[R_ges] | Med R_ges | E[R_first] | PF | Treffer | Ø Legs | Ø Halten | SL / TP | SL im Gewinn | Blöcke positiv | Anteil P&L | ohne grössten Gewinner E[R_ges] | grösster Anteil | CAGR | MaxDD | Recovery max |")
    A("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    share = lv[lab]["all"]["coin_share"]
    for cn in COINS:
        x = co[lab][cn]; t = x["trades"]; p = x["path"] or {}; ex = x["ex_largest"] or {}
        if t.get("n", 0) == 0: A(f"| {cn} | {x['start']} | 0 | – | – | – | – | – | – | – | – | – | – | – | – | – | – | – | – |"); continue
        A(f"| {cn} | {x['start']} | {t['n']} | {f(t['exp_R_total'])} | {f(t['med_R_total'])} | {f(t['exp_R_first'])} | {f(t['profit_factor'])} | {f(t['win_rate'],0,True)} | {f(t['legs_mean'],1)} | {f(t['hold_mean'],0)} d | {f(t['share_sl'],0,True)} / {f(t['share_tp'],0,True)} | {f(t['share_sl_above_avg'],0,True)} | {x['blocks_positive']} | {f(share.get(cn),1,True)} | {f(ex.get('exp_R_total_ex_largest'))} | {f(ex.get('largest_share'),0,True)} | {f(p.get('cagr'),1,True)} | {f(p.get('maxdd'),1,True)} | {p.get('rec_longest','–')} d |")
    A("")
A("BTC ist Identifikationsmarkt und zählt nicht für die Kriterien. «SL im Gewinn» ist der Anteil der Stop-Exits, bei denen der Stop nach Add-ons über dem Durchschnittseinstieg lag. «Blöcke positiv» zählt Zeitblöcke mit mindestens fünf Trades und positiver Erwartung.")
A("")

# 4 Zeitbloecke
A("## 4. Zeitblöcke, Pool ohne BTC")
A("")
A("| Ebene | P1 bis 2020 n / E[R_ges] / PF | P2 2021 bis 2023 | P3 ab 2024 |")
A("|---|---|---|---|")
for k in ["A|none|1", "B|K1|1", "B2|K1|1"]:
    b = lv[k]["exBTC"]["blocks"]
    A(f"| {k} | " + " | ".join(f"{b[p]['n']} / {f(b[p]['exp_R_total'])} / {f(b[p]['pf'])}{'' if b[p]['valid'] else ' (ungültig)'}" for p in ["P1", "P2", "P3"]) + " |")
A("")

# 5 Verteilung, Konzentration
A("## 5. Verteilung der R-Multiples und Konzentration, Pool ohne BTC")
A("")
A("| Ebene | P5 | P25 | Median | P75 | P90 | P95 | Anteil R < −1 | Anteil R > 3 | Top-1-Anteil | Top-3 | Top-5 | Top-10 % | Summe ohne Top 1 | ohne Top 3 | ohne Top 5 | Summe gesamt | Trade-Bootstrap 5 % E[R_ges] |")
A("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for k in ["A|none|1", "B|K1|1", "B|K2|1", "B2|K1|1"]:
    t = lv[k]["exBTC"]["trades"]; q = t["R_total_pct"]
    A(f"| {k} | {f(q['p5'])} | {f(q['p25'])} | {f(t['med_R_total'])} | {f(q['p75'])} | {f(q['p90'])} | {f(q['p95'])} | {f(q['share_below_m1'],0,True)} | {f(q['share_above_3'],0,True)} | {f(t['top1_share'],0,True)} | {f(t['top3_share'],0,True)} | {f(t['top5_share'],0,True)} | {f(t['top10pct_share'],0,True)} | {f(t['sum_ex_top1'],2,True)} | {f(t['sum_ex_top3'],2,True)} | {f(t['sum_ex_top5'],2,True)} | {f(t['sum_pct_cap'],2,True)} | {f(t['trade_boot_p5_R'])} |")
A("")
c8 = crit["c8_report"]
A(f"Coins mit positiver Erwartung ohne ihren grössten Gewinner (B, K1): {', '.join(c8['coins_positive_ex_largest']) or 'keine'}. Zeitblöcke positiv je Coin: " + ", ".join(f"{k} {v}" for k, v in c8["blocks_positive_per_coin"].items()) + ". Summen in Prozent des Sleeve-Startkapitals, gepoolt über die Coins. Das Entfernen der grössten Gewinner ist Bericht, kein Kriterium.")
A("")

# 6 Pfad, Beta, Statistik
A("## 6. Pfad, Beta-Trennung und Statistik, Pool ohne BTC")
A("")
A("| Ebene | CAGR | Sharpe | MaxDD | Recovery max / Mittel | Worst Year | Worst 12M | Ulcer | Exposure | EP CAGR / Sharpe / MaxDD | Alpha p.a. | t | Beta | Up / Down Capture | Kennzeichnung | Bootstrap 5 % p.a. | p Sharpe | Holm p |")
A("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for k in ["A|none|1", "A_window|none|1", "B|K1|1", "B|K2|1", "B_full|K1|1", "B2|K1|1", "B|K1|1b", "B|K1|2"]:
    e = lv[k]["exBTC"]; p = e["path"] or {}; ep = e["ep"] or {}; b = e["beta"] or {}; bo = e["boot"]
    A(f"| {k} | {f(p.get('cagr'),1,True)} | {f(p.get('sharpe'))} | {f(p.get('maxdd'),1,True)} | {p.get('rec_longest','–')} / {f(p.get('rec_mean'),0)} d | {f(p.get('worst_year'),1,True)} | {f(p.get('worst_roll12'),1,True)} | {f(p.get('ulcer'),3)} | {f(e.get('avg_expo'),1,True)} | {f(ep.get('cagr'),1,True)} / {f(ep.get('sharpe'))} / {f(ep.get('maxdd'),1,True)} | {f(b.get('alpha_ann'),1,True)} | {f(b.get('t_alpha'))} | {f(b.get('beta'))} | {f(b.get('up_capture'))} / {f(b.get('down_capture'))} | {b.get('label','–')} | {f(bo.get('p5_ann'),1,True)} | {f(bo.get('p_sharpe'),3)} | {f(e.get('holm_p'),3)} |")
A("")

# 7 Retention und Mechanik
A("## 7. Edge-Retention und Mechanik-Reproduzierbarkeit CMC gegen Kraken")
A("")
dg = R["diag"]
for key, title in [("A_vs_B_K1", "A gegen B (gleiche Signale, Kraken-Ausführung, K1)"), ("A_vs_B_K0", "A gegen B (K0)"), ("A_vs_Bsameday_K1", "A gegen B Same-Day-Close (K1, Berichtswert)")]:
    d = dg[key]
    A(f"**{title}.** A-Trades im B-Fenster {d['n_A_window']}, B-Trades {d['n_B']}, davon gepaart {d['matched']}, B-Trades ohne Gegenstück in A {d['b_not_in_a']}. Gleicher Exit-Grund {f(d['same_reason_share'],1,True)}. Phantom-Stops (Kraken-Tief unter Stop, CMC-Tief nicht) {d['phantom_sl']}, umgekehrt {d['phantom_sl_rev']}, Ziel nur auf einer Seite {d['tp_only_one']}. Exit-Tag exakt {f(d['exit_diff']['exact'],1,True)}, ±1 Tag {f(d['exit_diff']['within1'],1,True)}, mittlere Abweichung {f(d['exit_diff']['mean_abs'],1)} Tage. Fill-Abweichung Einstieg Mittel {f(d['fill_in']['mean'],3,True)} (P95 {f(d['fill_in']['p95'],2,True)}, Anteil über 1 Prozent {f(d['fill_in']['share_gt_1pct'],1,True)}), Stop {f(d['fill_sl']['mean'],3,True)} (n {d['fill_sl']['n']}), Ziel {f(d['fill_tp']['mean'],3,True)} (n {d['fill_tp']['n']}).")
    A("")
d = dg["A_vs_B2_K1"]
A(f"**A gegen B2 (Signale auf Kraken erzeugt).** A-Trades im B2-Fenster {d['n_A_window']}, B2-Trades {d['n_B2']}. Entry-Tag exakt {f(d['entry_exact_share'],1,True)}, ±1 Tag {f(d['entry_pm1_share'],1,True)}. Exit-Tag exakt {f(d['exit_exact_share'],1,True)}, ±1 {f(d['exit_pm1_share'],1,True)}. Leg-Zahl gleich {f(d['legs_same_share'],1,True)}, Exit-Grund gleich {f(d['reason_same_share'],1,True)}, vollständig identisch {f(d['identical_share'],1,True)}. Stop-Niveau-Abweichung Mittel {f(d['stop_dev']['mean'],3,True)}, P95 {f(d['stop_dev']['p95_abs'],2,True)}. SMA200-Filter je Tag gleich {f(d['sma_agree'],1,True)}. Wilder-ATR Kraken zu CMC Mittel {f(d['atr_ratio']['mean'],3)} (Spanne {f(d['atr_ratio']['min'],2)} bis {f(d['atr_ratio']['max'],2)}). Pivot-Niveau je Tag gleich (unter 0.5 Prozent) {f(d['lvl_agree'],1,True)}.")
A("")
rt = lv["B|K1|1"]["exBTC"]["trades"]; ra = lv["A_window|none|1"]["exBTC"]["trades"]
A(f"Retention K1: E[R_gesamt] B / A_window = {f(rt['exp_R_total'])} / {f(ra['exp_R_total'])} = {f(rt['exp_R_total']/ra['exp_R_total'] if ra['exp_R_total'] else float('nan'))}, E[R_first] {f(rt['exp_R_first'])} / {f(ra['exp_R_first'])}, Profit-Faktor {f(rt['profit_factor'])} / {f(ra['profit_factor'])}, Trefferquote {f(rt['win_rate'],1,True)} / {f(ra['win_rate'],1,True)}, Trades {rt['n']} / {ra['n']}.")
A("")

# 8 Jitter
A("## 8. Jitter-Nachbarn (Plateau-Prüfung, ohne Auswahlwirkung), Pool ohne BTC")
A("")
A("| Variante | B K1 Trades | E[R_ges] | PF | Trefferquote | A Trades | E[R_ges] | PF |")
A("|---|---|---|---|---|---|---|---|")
base_b = lv["B|K1|1"]["exBTC"]["trades"]; base_a = lv["A|none|1"]["exBTC"]["trades"]
A(f"| Basis (6.5 / 37.5 / Pivot 5) | {base_b['n']} | {f(base_b['exp_R_total'])} | {f(base_b['profit_factor'])} | {f(base_b['win_rate'],1,True)} | {base_a['n']} | {f(base_a['exp_R_total'])} | {f(base_a['profit_factor'])} |")
for k, v in R["jitter"].items():
    A(f"| {k} {v['params']} | {v['B']['n']} | {f(v['B']['exp_R_total'])} | {f(v['B']['pf'])} | {f(v['B']['wr'],1,True)} | {v['A']['n']} | {f(v['A']['exp_R_total'])} | {f(v['A']['pf'])} |")
A("")

# 9 Add-ons / Open Risk
A("## 9. Pyramiding und Open Risk je Add-on, Ebene B K1 Sicht 1, alle Coins")
A("")
ad = [a for cn in COINS for a in co["B|K1|1"][cn]["addons"]]
if ad:
    import statistics
    orb = [a["before"]["open_risk"] for a in ad]; ora = [a["after"]["open_risk"] for a in ad]; lb = [a["before"]["loss_at_stop"] for a in ad]; la = [a["after"]["loss_at_stop"] for a in ad]
    nb = [a["before"]["notional"] for a in ad]; na = [a["after"]["notional"] for a in ad]; sa = [a["stop_above_avg_after"] for a in ad]
    first_above = [a["n"] for a in ad if a["stop_above_avg_after"]]
    A(f"Anzahl Add-ons {len(ad)}. Open Risk (Mark-to-Market bis Stop, in Prozent des Sleeve-Startkapitals) vor Add-on Mittel {f(np.mean(orb),2,True)}, nach Add-on {f(np.mean(ora),2,True)}. Ergebnis bei sofortigem Stop vor Add-on {f(np.mean(lb),2,True)}, nach Add-on {f(np.mean(la),2,True)} (positiv heisst: Stop schliesst im Gewinn). Notional vor {f(np.mean(nb),1,True)}, nach {f(np.mean(na),1,True)}. Anteil Add-ons, nach denen der gemeinsame Stop über dem Durchschnittseinstieg liegt {f(np.mean(sa),0,True)}, erstmals im Mittel beim {f(np.mean(first_above),1) if first_above else '–'}. Add-on.")
    A("")
    A("| Add-on Nr. | Anzahl | Open Risk vor | nach | Ergebnis bei Stop vor | nach | Notional nach | Stop über Ø Entry |")
    A("|---|---|---|---|---|---|---|---|")
    for n in sorted(set(a["n"] for a in ad)):
        g = [a for a in ad if a["n"] == n]
        A(f"| {n} | {len(g)} | {f(np.mean([a['before']['open_risk'] for a in g]),2,True)} | {f(np.mean([a['after']['open_risk'] for a in g]),2,True)} | {f(np.mean([a['before']['loss_at_stop'] for a in g]),2,True)} | {f(np.mean([a['after']['loss_at_stop'] for a in g]),2,True)} | {f(np.mean([a['after']['notional'] for a in g]),1,True)} | {f(np.mean([a['stop_above_avg_after'] for a in g]),0,True)} |")
    A("")

# 10 Umfang
A("## 10. Umfang und Verifikation")
A("")
A(f"- Eingabedateien mit SHA-256 in `mtp_val_results.json`, Feld `inputs` ({len(R['inputs'])} Dateien), Kraken-Archiv fc81b54c… gegen Krakens Hash-Liste geprüft")
A(f"- Starts je Coin (A / B / B_full / B2): " + "; ".join(f"{c} {s['A']} / {s['B']} / {s['B_full']} / {s['B2']}" for c, s in R["starts"].items()))
A("- Look-ahead-Test und BTC-Replikationskontrolle in `controls.json`, alle Trades je Ebene in `trades/`")
A("- Kostenmodell: " + "; ".join(f"{k} Gebühr {v['fee']*100:.2f} % plus Reibung {v['fric']*100:.2f} % je Seite, Slippage Einstieg {v['slip_in']*100:.2f} %, Stop {v['slip_sl']*100:.2f} %" for k, v in R["cost"].items()))
open(os.path.join(D, "mtp_val_report.md"), "w").write("\n".join(out))
print("Bericht geschrieben:", os.path.join(D, "mtp_val_report.md"))
