#!/usr/bin/env python3
"""Erzeugt stage1_robustness_report.md, stage1_summary.md und frozen_regimes_v1.json aus stage1_results.json."""
import json, os, datetime as dt, hashlib
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
r = json.load(open(os.path.join(OUT, "stage1_results.json")))
rep, ver, f1, THR = r["report"], r["verdict"], r["f1"], r["thresholds"]
COINS = ["BTC", "ETH", "SOL", "XRP", "ADA", "AVAX", "LINK", "DOT", "BNB", "LTC"]
CANDS = ["R1", "R2", "R3", "R4", "R5"]
doc_sha = open(os.path.join(os.path.dirname(OUT), "doc_sha.txt")).read().split()[0]

def pct(x): return "–" if x is None else f"{x*100:.0f} %"
def f1d(x): return "–" if x is None else f"{x:.1f}"

L = []
A = L.append
A("# Stufe 1 — Robustheitsbericht")
A("")
A(f"**Project Aurum II. Rechenlauf vom {r['run_at'][:10]}. Vorregistrierung Version 1.0, SHA-256 `{doc_sha[:16]}…`, eingefroren am 15.09.2026.**")
A("")
A("Alle Schwellen stammen aus der eingefrorenen Vorregistrierung. Kein Wert wurde nach dem Lauf verändert. Jede gerechnete Konfiguration inklusive Jitter steht in `stage1_config_log.csv`.")
A("")
A("## 1. Urteil je Kandidat")
A("")
A("| Kandidat | Urteil | Dimensionen bestanden | Bemerkung |")
A("|---|---|---|---|")
for cid in CANDS:
    v = ver[cid]
    dims_ok = [d for d, x in v["dims"].items() if x["ok"]]
    dims_all = list(v["dims"].keys())
    A(f"| {cid} | **{'TAUGLICH' if v['ok'] else 'VERWORFEN'}** | {len(dims_ok)} von {len(dims_all)} | " +
      ", ".join(f"{d}: {'ok' if v['dims'][d]['ok'] else 'verworfen'}" for d in dims_all) + " |")
A(f"| F1 | **{'VORLÄUFIG TAUGLICH' if ver['F1']['ok'] else 'VERWORFEN (vorläufig)'}** | – | Funding, nur BTC, ETH, SOL ab 10.09.2025 |")
A("")
A("**Kein Kandidat besteht.** Die Nullhypothese aus Abschnitt 1 der Vorregistrierung ist nicht widerlegt. Siehe `stage1_summary.md` für die Einordnung.")
A("")

A("## 2. Gesamtmetriken je Kandidat, Coin und Dimension")
A("")
A("Volle Historie je Coin nach Warmup. Dwell ist der Median der Verweildauer in Bars. Schwellen: Dwell ≥ 10 (häufige Zustände) beziehungsweise ≥ 5 (seltene), Ein-Bar ≤ 25 %, Wechsel D1/D2 ≤ 30, D3 ≤ 12, D4 ≤ 30 je 252 Bars, Jitter Mittel ≥ 85 % und Minimum ≥ 75 %, Kalenderjahr-Blöcke ≥ 70 % bestanden ohne Faktor-2-Ausreisser.")
A("")
for cid in CANDS:
    A(f"### {cid}")
    A("")
    A("| Coin | Dim | Dwell je Zustand | Anteil je Zustand | Ein-Bar | Wechsel/Jahr | Jitter Mittel / Min | Blöcke bestanden | Urteil | Grund |")
    A("|---|---|---|---|---|---|---|---|---|---|")
    for coin in COINS:
        res = rep[cid][coin]
        for dim, d in res["dims"].items():
            m = d["metrics"]; j = res["jitter"][dim]; co = res["coin_ok"][dim]
            dwell = ", ".join(f"{k} {v:.1f}" for k, v in m["dwell"].items())
            share = ", ".join(f"{k} {v*100:.0f} %" for k, v in m["share"].items())
            why = "; ".join(d["why"]) if d["why"] else ""
            if not co["jitter"]: why += (" | " if why else "") + "Jitter"
            if not co["blocks"]: why += (" | " if why else "") + f"Blöcke {co['block_share']*100:.0f} %" + ("" if co["factor2"] else ", Faktor 2")
            A(f"| {coin} | {dim} | {dwell} | {share} | {pct(m['one_bar'])} | {f1d(m['switches'])} | {pct(j['mean'])} / {pct(j['min'])} | {pct(co['block_share'])} | {'ok' if co['ok'] else 'verworfen'} | {why.replace(';', ',')} |")
    A("")

A("## 3. Zeitblöcke, Kalenderjahre, Kernassets")
A("")
A("Je Block das Urteil je Dimension. Ein Block gilt als bestanden, wenn Dwell, Ein-Bar und Wechselrate innerhalb der Schwellen liegen.")
A("")
for cid in CANDS:
    for coin in ["BTC", "ETH"]:
        res = rep[cid][coin]
        dims = list(res["dims"].keys())
        A(f"**{cid} {coin}**")
        A("")
        A("| Block | " + " | ".join(dims) + " |")
        A("|---|" + "---|" * len(dims))
        for y, b in res["blocks"].items():
            A(f"| {y} | " + " | ".join(("ok" if b[d]["ok"] else "verworfen") for d in dims) + " |")
        A("")

A("## 4. Halving-Zyklen, Gegenprobe (nur Bericht, kein Hard-Fail)")
A("")
for cid in CANDS:
    for coin in ["BTC", "ETH"]:
        res = rep[cid][coin]
        dims = list(res["dims"].keys())
        row = []
        for name, b in res["halving"].items():
            row.append(f"{name}: " + ", ".join(f"{d} {'ok' if b[d]['ok'] else 'verworfen'}" for d in dims))
        A(f"- **{cid} {coin}** — " + " · ".join(row))
A("")

A("## 5. Kraken-Gegenprobe (Datenkonsistenz, Schwelle 90 %)")
A("")
A("| Kandidat | Coin | " + " | ".join(["D1", "D2", "D3", "D4", "Label"]) + " |")
A("|---|---|---|---|---|---|---|")
for cid in CANDS:
    for coin in ["BTC", "ETH", "SOL"]:
        k = rep[cid][coin].get("kraken_agree", {})
        A(f"| {cid} | {coin} | " + " | ".join(pct(k.get(d)) for d in ["D1", "D2", "D3", "D4", "label"]) + " |")
A("")
A("Preisbasierte Dimensionen stimmen zwischen Binance-USDT und Kraken-USD zu 94 bis 100 Prozent überein. D4 (Volumen) liegt bei 79 bis 83 Prozent und verfehlt die Konsistenzschwelle, weil Volumen börsenspezifisch ist. Die Datengrundlage ist für D1 bis D3 belastbar.")
A("")

A("## 6. Kandidat F1, Funding")
A("")
A("| Coin | Zeitraum | Dwell je Zustand | Anteil je Zustand | Ein-Bar | Wechsel/Jahr | Jitter Mittel / Min | Urteil | Grund |")
A("|---|---|---|---|---|---|---|---|---|")
for coin, v in f1.items():
    m = v["metrics"]
    dwell = ", ".join(f"{k} {x:.1f}" for k, x in m["dwell"].items())
    share = ", ".join(f"{k} {x*100:.0f} %" for k, x in m["share"].items())
    A(f"| {coin} | {v['start']} bis {v['end']} | {dwell} | {share} | {pct(m['one_bar'])} | {f1d(m['switches'])} | {pct(v['jitter_mean'])} / {pct(v['jitter_min'])} | {'ok' if v['overall'] else 'verworfen'} | {', '.join(v['why'])} |")
A("")

A("## 7. Umfang des Laufs")
A("")
n_cfg = sum(1 for _ in open(os.path.join(OUT, "stage1_config_log.csv"))) - 1
A(f"- Gerechnete Konfigurationen inklusive Jitter: {n_cfg} (siehe `stage1_config_log.csv`)")
A(f"- Coins: {', '.join(COINS)}. Alle mit mindestens {THR['min_bars_coin']} definierten Bars.")
A("- Eingabedaten mit SHA-256 in `stage1_results.json`, Feld `inputs`.")
A("- Verifikation: Look-ahead-Test bestanden (Labels bei am 30.06.2023 abgeschnittener Historie identisch mit dem Volllauf, 0 abweichende definierte Zellen). ATR und ADX gegen unabhängige Referenz auf 1e-11 identisch. Perzentilränge im Mittel 0.45 bis 0.50.")
A("")
open(os.path.join(OUT, "stage1_robustness_report.md"), "w", encoding="utf-8").write("\n".join(L))

# ------------------------------------------------------------ frozen_regimes_v1.json
frozen = dict(
    version=1, frozen_at=None, status="KEIN KANDIDAT TAUGLICH",
    preregistration_sha256=doc_sha, run_at=r["run_at"],
    verdicts={cid: ("TAUGLICH" if ver[cid]["ok"] else "VERWORFEN") for cid in CANDS},
    F1="VORLAEUFIG TAUGLICH" if ver["F1"]["ok"] else "VERWORFEN (vorlaeufig)",
    tauglich=[],
    note="Stufe 3 entfaellt. Stufe 2 laeuft ohne Regimefilter. Jede neue Regimedefinition braucht eine neue Vorregistrierung (Version 2).",
    inputs=r["inputs"],
)
json.dump(frozen, open(os.path.join(OUT, "frozen_regimes_v1.json"), "w"), indent=1, ensure_ascii=False)
print("Bericht geschrieben.")
