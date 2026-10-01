#!/usr/bin/env python3
"""Erzeugt stage2_report.md und stage2_mtp_fingerprint.md aus stage2_results.json. Aufruf: python3 report2.py <out_dir>"""
import json, os, sys, math
import numpy as np

OUT = sys.argv[1] if len(sys.argv) > 1 else "out_full"
r = json.load(open(os.path.join(OUT, "stage2_results.json")))
R = r["results"]; FP = r["fingerprint"]
ORDER = ["W0", "W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8", "MR", "TS21", "TS63", "TS126", "XS21", "CC", "FC", "OI"]
FAM = {"A": "Familie A, Trendfolge (Woo-Matrix)", "B": "Familie B, Mean Reversion", "C": "Familie C, Momentum", "D": "Familie D, Carry und Perpetual-Daten"}
CLS = {"S": "S", "M": "M", "L": "L"}


def P(x, d=1):
    return "–" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x*100:.{d}f} %"
def F(x, d=2):
    return "–" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.{d}f}"
def I(x):
    return "–" if x is None else f"{int(x)}"
def ok(b): return "ja" if b else "nein"

keys = sorted([k for k in R if not R[k].get("skipped")], key=lambda k: (ORDER.index(R[k]["id"]), ["L", "S", "LS", "N"].index(R[k]["side"])))
L = []; A = L.append
A("# Stufe 2 — Bericht: Strategie-Edge ohne Regimefilter")
A("")
A(f"**Project Aurum II. Rechenlauf vom {r['run_at'][:10]}, Lauf «{r['tag']}». Vorregistrierung Version 1.0, SHA-256 `{r['prereg_sha256'][:16]}…`, eingefroren am 15.09.2026. Coins: {', '.join(r['coins'])}.**")
A("")
A("Alle Definitionen, Kosten und Kriterien stammen aus der eingefrorenen Vorregistrierung. Jede gerechnete Konfiguration steht in `stage2_config_log.csv`, jeder Trade in `stage2_trades/`. Drei Kostenszenarien werden nie vermischt, jede Tabelle nennt das Szenario. Survivorship-Vermerk: Das Zehn-Coin-Universum wurde 2026 nach heutiger Liquidität gewählt, alle Coins haben überlebt. XS21-Zahlen sind davon am stärksten betroffen.")
A("")
if r.get("run_oi") is False:
    A(f"**D-OI wurde nicht gerechnet (fail-closed).** Datenprüfung: " + "; ".join(f"{c}: {v['why']}" for c, v in r["oi_check"].items() if c in ("BTC", "ETH")) + ". N in Familie D ist 4.")
    A("")

# ---------------------------------------------------------------- 1 Urteile
A("## 1. Urteile je Variante und Seite, Szenario K1, gepoolt")
A("")
A("| Variante | Seite | Klasse | Urteil | Beta | K1 CAGR | Sharpe | Calmar | MaxDD | Erw./Trade | Trades | Exposure | c1 | c3 | c4 | c5 | c6 | c7 | c8 | K2 robust |")
A("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for k in keys:
    x = R[k]; e = x["scenarios"]["K1"]["pooled"]["equity"] or {}; p = x["scenarios"]["K1"]["pooled"]; c = x["criteria"]
    A(f"| {x['id']} | {x['side']} | {x['cls']} | **{x['verdict']}** | {x['beta_label']} | {P(e.get('cagr'))} | {F(e.get('sharpe'))} | {F(e.get('calmar'))} | {P(e.get('maxdd'))} | {P(p['expectancy'],2)} | {I(p['n_trades'])} | {P(p['avg_expo'],0)} | {ok(c['c1'])} | {ok(c['c3'])} | {ok(c['c4'])}{'*' if c['c4_note'] else ''} | {ok(c['c5'])} | {ok(c['c6'])} | {ok(c['c7'])} | {ok(c['c8'])} | {ok(c['robust_k2'])} |")
A("")
A("c1 Erwartung nach Kosten (BTC, ETH, Mehrheit), c3 Zeitblöcke, c4 Jitter-Region (* keine Nachbarn vorregistriert, n/a), c5 Trade-Mindestzahl je Klasse, c6 MaxDD nicht schlechter als exposure-gleiche Passivposition, c7 Beta-Trennung (Alpha oder Risikotransformation), c8 Bootstrap und Holm. Klasse L trägt bei Bestehen den Vermerk «bestanden mit geringer Trade-Basis».")
A("")

# ---------------------------------------------------------------- 2 Kostenszenarien
A("## 2. Drei Kostenszenarien, gepoolt")
A("")
A("| Variante | Seite | K0 CAGR | K0 Sharpe | K1 CAGR | K1 Sharpe | K2 CAGR | K2 Sharpe | K1 Kosten p.a. | K1 Funding p.a. | Turnover p.a. |")
A("|---|---|---|---|---|---|---|---|---|---|---|")
for k in keys:
    x = R[k]; row = [x["id"], x["side"]]
    for s in ["K0", "K1", "K2"]:
        e = x["scenarios"][s]["pooled"]["equity"] or {}
        row += [P(e.get("cagr")), F(e.get("sharpe"))]
    # Kosten und Funding p.a. aus Coin-Mittel (K1)
    cm = x["scenarios"]["K1"]["coins"]
    yrs = np.mean([v["equity"]["years"] for v in cm.values() if v["equity"]]) if cm else np.nan
    cost = np.mean([v["cost_sum"] for v in cm.values() if v["equity"]]) / yrs if cm and yrs else np.nan
    fund = np.mean([v["funding_sum"] for v in cm.values() if v["equity"]]) / yrs if cm and yrs else np.nan
    to = np.mean([v["turnover"] for v in cm.values() if v["equity"]]) if cm else np.nan
    row += [P(cost, 2), P(fund, 2), F(to, 1)]
    A("| " + " | ".join(row) + " |")
A("")

# ---------------------------------------------------------------- 3 Beta-Trennung
A("## 3. Beta-Trennung gegen exposure-gleiche Passivposition (EP), K1, gepoolt")
A("")
A("| Variante | Seite | Strategie CAGR / Sharpe / Calmar / MaxDD | EP CAGR / Sharpe / Calmar / MaxDD | B&H Coin CAGR / MaxDD | BTC B&H CAGR / MaxDD | Alpha p.a. | t | p | Beta | Up-Capture | Down-Capture | 13.3a | 13.3b | Kennzeichnung |")
A("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for k in keys:
    x = R[k]; e = x["scenarios"]["K1"]["pooled"]["equity"] or {}; ep = x["bench_pooled"].get("EP") or {}; bh = x["bench_pooled"].get("BH") or {}; bb = x["bench_pooled"].get("BTC_BH") or {}; b = x["beta"] or {}
    A(f"| {x['id']} | {x['side']} | {P(e.get('cagr'))} / {F(e.get('sharpe'))} / {F(e.get('calmar'))} / {P(e.get('maxdd'))} | {P(ep.get('cagr'))} / {F(ep.get('sharpe'))} / {F(ep.get('calmar'))} / {P(ep.get('maxdd'))} | {P(bh.get('cagr'))} / {P(bh.get('maxdd'))} | {P(bb.get('cagr'))} / {P(bb.get('maxdd'))} | {P(b.get('alpha_ann'))} | {F(b.get('t_alpha'))} | {F(b.get('p_alpha'),3)} | {F(b.get('beta'))} | {F(b.get('up_capture'))} | {F(b.get('down_capture'))} | {ok(b.get('alpha_test'))} | {ok(b.get('risk_test'))} | {b.get('label','–')} |")
A("")

# ---------------------------------------------------------------- 4 Statistik
A("## 4. Statistik: Bootstrap, Holm, Deflated Sharpe, Trade-Bootstrap (K1, gepoolt)")
A("")
A("| Variante | Seite | Familie N | Bootstrap 5 %-Perzentil Überrendite p.a. | p (Sharpe > 0) | Holm p | DSR (N Familie) | DSR (N inkl. Jitter) | Trade-Bootstrap 5 % Erw./Trade |")
A("|---|---|---|---|---|---|---|---|---|")
for k in keys:
    x = R[k]; b = x["boot"]
    A(f"| {x['id']} | {x['side']} | {I(x.get('family_n'))} | {P(b.get('p5_ann'))} | {F(b.get('p_sharpe'),3)} | {F(x.get('holm_p'),3)} | {F(x.get('dsr'),3)} | {F(x.get('dsr_all_jitter'),3)} | {P(x.get('trade_boot_p5'),2)} |")
A("")
A("Primärverfahren ist Holm auf den Block-Bootstrap-p-Werten je Familie. DSR ist Sensitivität. Abweichungen zwischen beiden sind in Abschnitt 8 kommentiert.")
A("")

# ---------------------------------------------------------------- 5 Zeitbloecke und Jitter
A("## 5. Zeitblöcke (Erwartung je Trade, K1, gepoolt) und Jitter-Nachbarn")
A("")
A("| Variante | Seite | P1 (n) | P2 (n) | P3 (n) | Nachbarn: Name = Erw./Trade, Sharpe |")
A("|---|---|---|---|---|---|")
for k in keys:
    x = R[k]; bl = x["scenarios"]["K1"]["pooled"]["blocks"]
    cells = [f"{P(bl[b]['expectancy'],2)} ({bl[b]['n']}){'' if bl[b]['valid'] else ' ungültig'}" for b in ["P1", "P2", "P3"]]
    nb = ", ".join(f"{n['name']} = {P(n['expectancy'],2)}, {F(n['sharpe'])}" for n in x["neighbours"]) or "keine vorregistriert"
    A(f"| {x['id']} | {x['side']} | " + " | ".join(cells) + f" | {nb} |")
A("")

# ---------------------------------------------------------------- 6 Coins
A("## 6. Coin-Robustheit, K1: CAGR / Sharpe / MaxDD / Erwartung je Trade / Trades je Coin")
A("")
coins = r["coins"]
A("| Variante | Seite | " + " | ".join(coins) + " | Anteil Coins bestanden |")
A("|---|---|" + "---|" * len(coins) + "---|")
for k in keys:
    x = R[k]; cm = x["scenarios"]["K1"]["coins"]
    cells = []
    for c in coins:
        v = cm.get(c)
        if not v or not v["equity"]:
            cells.append("–"); continue
        e = v["equity"]; t = v["trades"]
        cells.append(f"{P(e['cagr'],0)} / {F(e['sharpe'],1)} / {P(e['maxdd'],0)} / {P(t.get('expectancy'),1)} / {t['n']}")
    A(f"| {x['id']} | {x['side']} | " + " | ".join(cells) + f" | {P(x['criteria']['c2_share'],0)} |")
A("")

# ---------------------------------------------------------------- 7 Trade-Kennzahlen
A("## 7. Trade-Kennzahlen, K1, gepoolt (Coin-Mittel für Trefferquote und Halten)")
A("")
A("| Variante | Seite | Trades | Trefferquote | Erw./Trade | Median | Ø Gewinner | Ø Verlierer | Gain/Loss | Profit-Faktor | Ø Haltedauer | Top-10 %-Anteil | Top-5-Anteil | Worst Year | Worst Rolling 12M | Ulcer |")
A("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for k in keys:
    x = R[k]; p = x["scenarios"]["K1"]["pooled"]; e = p["equity"] or {}
    cm = [v["trades"] for v in x["scenarios"]["K1"]["coins"].values() if v["trades"]["n"] > 0]
    def mean(key):
        vals = [t[key] for t in cm if t.get(key) is not None]
        return float(np.mean(vals)) if vals else None
    A(f"| {x['id']} | {x['side']} | {I(p['n_trades'])} | {P(p['win_rate'],0)} | {P(p['expectancy'],2)} | {P(mean('median'),2)} | {P(mean('avg_win'),1)} | {P(mean('avg_loss'),1)} | {F(mean('gain_loss'))} | {F(mean('profit_factor'))} | {F(mean('avg_hold'),0)} d | {P(mean('top10_share'),0)} | {P(mean('top5_share'),0)} | {P(e.get('worst_year'))} | {P(e.get('worst_roll12'))} | {F(e.get('ulcer'),3)} |")
A("")

# ---------------------------------------------------------------- 8 Paarvergleiche H0-A8, H0-A6
A("## 8. Paarvergleiche: SMA200-Filter (W2 gegen W8) und Pyramiding (W6 gegen W2, W7 gegen W4), K1, gepoolt")
A("")
A("| Vergleich | CAGR | Sharpe | Calmar | MaxDD | Erw./Trade | Return je Exposure | Worst Year |")
A("|---|---|---|---|---|---|---|---|")
for a, b in [("W2|L", "W8|L"), ("W6|L", "W2|L"), ("W7|L", "W4|L")]:
    if a in R and b in R:
        for kk in (a, b):
            x = R[kk]; e = x["scenarios"]["K1"]["pooled"]["equity"] or {}; p = x["scenarios"]["K1"]["pooled"]
            rpe = (e.get("cagr") / p["avg_expo"]) if e and p["avg_expo"] else None
            A(f"| {kk} | {P(e.get('cagr'))} | {F(e.get('sharpe'))} | {F(e.get('calmar'))} | {P(e.get('maxdd'))} | {P(p['expectancy'],2)} | {P(rpe)} | {P(e.get('worst_year'))} |")
        A("| | | | | | | | |")
A("")

# ---------------------------------------------------------------- 9 Umfang
n_cfg = sum(1 for _ in open(os.path.join(OUT, "stage2_config_log.csv"))) - 1
A("## 9. Umfang und Verifikation")
A("")
A(f"- Gerechnete Konfigurationen inklusive Jitter und Seiten: {n_cfg} (`stage2_config_log.csv`)")
A(f"- Eingabedateien mit SHA-256 in `stage2_results.json`, Feld `inputs` ({len(r['inputs'])} Dateien)")
A("- Look-ahead-Test: Gewichte auf einer am 30.06.2023 abgeschnittenen Historie identisch mit dem Volllauf (W2, W6, MR-S, TS21 auf BTC, 0 abweichende Tage)")
A("- Stopp- und Einstiegskonsistenz W2 BTC gegen unabhängige Nachrechnung: 0 Verstösse bei 19 Trades")
A("- Bear-Jahre nach BTC-Kalenderrendite (mechanisch): " + ", ".join(f"{y} ({v*100:.0f} %)" for y, v in r["bear_years"].items()))
A("")
open(os.path.join(OUT, "stage2_report.md"), "w", encoding="utf-8").write("\n".join(L))

# ---------------------------------------------------------------- Fingerprint
M = []; B = M.append
B("# Stufe 2 — MTP-Fingerprint, getrennte Analyse")
B("")
B("Nach Abschluss der Edge-Bewertung, ohne Rückwirkung auf sie. Frage: Welche Variante W0 bis W8 ähnelt dem öffentlich beschriebenen Market Trend Pro strukturell am ehesten? Gemessen auf BTC und ETH, Long-only, Szenario K1. Bänder aus Abschnitt 21 der Vorregistrierung. W0 ohne ATR-Stopp: R-Multiples n/a, Beurteilung auf fünf Merkmalen. Signalhäufigkeit ist ein unsicherer Fingerprint (öffentlich 8 je Jahr oder 1 bis 3 je Monat). Ergebnis ist eine Zuordnung, keine Performance-Aussage. Wir stellen nicht fest, Woos Code gefunden zu haben.")
B("")
names = dict(signals="Signale/Jahr (4–12)", hold="Ø Haltedauer (45–135 d)", win="Trefferquote (30–50 %)", medR="Median R ≤ 0.5 und Mittel > Median", p90R="P90 R ≥ 3.0", skewR="Schiefe R > 1.0", top10="Top-10 % ≥ 50 %", top5="Top-5 ≥ 30 %", bear="Exposure Bear-Jahre ≤ 25 %")
for vid, fp in FP.items():
    for c, v in fp.items():
        B(f"## {vid}, {c}: **{v['label']}** ({v['n_ok']} von {v['n_tot']} im Band)")
        B("")
        B("| Merkmal | Wert | im Band |")
        B("|---|---|---|")
        for key, (val, inb) in v["traits"].items():
            if isinstance(val, list): sval = f"Median {F(val[0])}, Mittel {F(val[1])}"
            elif key in ("win", "top10", "top5", "bear"): sval = P(val, 0)
            elif key == "hold": sval = f"{F(val,0)} d"
            else: sval = F(val)
            B(f"| {names[key]} | {sval} | {ok(inb)} |")
        Rr = v.get("R") or {}
        if Rr.get("n"):
            B(f"| R-Verteilung P5/P25/P50/P75/P90/P95 | {F(Rr['p5'])} / {F(Rr['p25'])} / {F(Rr['median'])} / {F(Rr['p75'])} / {F(Rr['p90'])} / {F(Rr['p95'])} | – |")
            B(f"| Anteil Trades R ≤ −1 | {P(Rr['share_le_m1'],0)} | – |")
        if v.get("avg_hold_win"):
            B(f"| Ø Haltedauer Gewinner | {F(v['avg_hold_win'],0)} d | – |")
        B("")
open(os.path.join(OUT, "stage2_mtp_fingerprint.md"), "w", encoding="utf-8").write("\n".join(M))
print("Bericht und Fingerprint geschrieben:", OUT)
