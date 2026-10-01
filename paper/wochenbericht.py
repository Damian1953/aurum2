"""Wochenbericht Paper-Trading (Deutsch, Schweizer Schreibweise, ca. 5 Minuten Lesezeit).
Liest nur Ausgaben des Runners. Risikoloser Satz: FRED DTB3 (oeffentlich, ohne Key), Cache im state-Ordner.
Aufruf: python paper/wochenbericht.py [--datum JJJJ-MM-TT]
"""
import argparse, datetime as dt, io, json, os, sys, urllib.request
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paper_engine as E

REVIEW_DATUM = dt.date(2027, 2, 2)          # PAPER_PREREG §9 (D3: hoechstens 4 Monate nach Start)
STAKING_REF = {"ETH": 0.0258, "SOL": 0.0569}  # Kraken CH, abgerufen 01.10.2026 (PAPER_PREREG §8)
NAMEN = {"W2": "W2 (Ausbruch 55, SMA200, 3 ATR)", "W6": "W6 (wie W2 mit Pyramiding)", "T55_20": "Turtle 55/20", "BH": "Buy and Hold (Korb)"}
DTB3_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DTB3"


def dtb3(out):
    cache = os.path.join(out, "state", "dtb3.csv")
    try:
        with urllib.request.urlopen(DTB3_URL, timeout=20) as r:
            txt = r.read().decode()
        open(cache, "w").write(txt)
    except Exception:
        if not os.path.exists(cache):
            return None
        txt = open(cache).read()
    s = pd.read_csv(io.StringIO(txt))
    s.columns = ["date", "v"]
    s["v"] = pd.to_numeric(s["v"], errors="coerce")
    s = s.dropna()
    s["date"] = pd.to_datetime(s["date"], utc=True)
    return s.set_index("date")["v"] / 100.0


def chf(x):
    return f"{x:,.0f}".replace(",", "'")


def pct(x):
    return f"{x * 100:+.1f} %"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--datum")
    a = ap.parse_args()
    out = os.environ.get("AURUM_PAPER_OUT", "/workspace/aurum2/paper")
    heute = dt.date.fromisoformat(a.datum) if a.datum else dt.date.today()
    st = json.load(open(os.path.join(out, "state", "state_latest.json")))
    hist = [json.loads(l) for l in open(os.path.join(out, "logs", "run_history.jsonl"))]
    eq = pd.read_csv(os.path.join(out, "ledger", "equity_daily.csv")) if os.path.getsize(os.path.join(out, "ledger", "equity_daily.csv")) > 1 else pd.DataFrame()
    tr = pd.read_csv(os.path.join(out, "ledger", "trades.csv")) if os.path.getsize(os.path.join(out, "ledger", "trades.csv")) > 1 else pd.DataFrame()
    woche_von = heute - dt.timedelta(days=7)
    L = []
    L.append(f"# Paper-Trading Wochenbericht {heute.isoformat()}")
    L.append("")
    L.append(f"Vorregistrierung PAPER_PREREG_v1.0 (SHA {str(st.get('prereg_sha256'))[:12]}…). Startbar {st['start_bar']}. Review spätestens {REVIEW_DATUM.isoformat()} "
             f"(noch {(REVIEW_DATUM - heute).days} Tage). Keine Keys, keine Orders: alle Zahlen sind hypothetisch.")
    L.append("")
    # 1 Betrieb
    h7 = [r for r in hist if r.get("started_utc", "")[:10] >= woche_von.isoformat()]
    ok7 = sum(1 for r in h7 if r.get("ok")); err7 = [e for r in h7 for e in r.get("errors", [])]
    L.append("## 1. Betrieb")
    L.append(f"- Läufe der letzten 7 Tage: {len(h7)}, davon erfolgreich {ok7}.")
    L.append(f"- Letzter abgeschlossener Tagesbar in den Daten: {min(v['last_bar'] for v in st['coins'].values()) if st['coins'] else 'keine'}.")
    L.append(f"- Fehler: {'keine' if not err7 else '; '.join(sorted(set(err7))[:5])}.")
    if st.get("warnings"):
        L.append(f"- Hinweise aus dem letzten Lauf: {'; '.join(st['warnings'][:3])}.")
    L.append("")
    # 2 Stand
    L.append("## 2. Stand (Szenario maker_plan = K1; in Klammern taker_K2)")
    L.append("| Reihe | Wert USD | seit Start | MaxDD |")
    L.append("|---|---|---|---|")
    pf = st.get("portfolio", {})
    for s in ["W2", "W6", "T55_20", "BH"]:
        if s not in pf:
            continue
        p = pf[s]["maker_plan"]; q = pf[s].get("taker_K2", p)
        L.append(f"| {NAMEN[s]} | {chf(p['equity_usd'])} ({chf(q['equity_usd'])}) | {pct(p['equity_usd'] / p['start_usd'] - 1)} | {p['max_dd'] * 100:.1f} % |")
    if not any(s in pf for s in ["W2", "W6", "T55_20", "BH"]):
        L.append("| noch keine Bewertung (vor dem ersten Tag nach dem Startbar) | – | – | – |")
    start_usd = E.SLEEVE_USD * len(E.COINS)
    r = dtb3(out)
    start = pd.Timestamp(st["start_bar"], tz="UTC")
    tage = max((pd.Timestamp(heute, tz="UTC") - start).days, 0)
    if r is not None and tage > 0:
        rate = float(r[r.index <= pd.Timestamp(heute, tz="UTC")].iloc[-1])
        rf = start_usd * ((1 + rate) ** (tage / 365) - 1)
        L.append(f"| Risikoloser USD-Satz (DTB3 {rate * 100:.2f} %) | {chf(start_usd + rf)} | {pct(rf / start_usd)} | 0.0 % |")
    if "BH" in pf:
        stak = sum(STAKING_REF.values()) * E.SLEEVE_USD * tage / 365
        L.append(f"- Staking-Referenz: Buy and Hold plus Staking auf ETH und SOL (2.58 % / 5.69 % p. a.) ergäbe zusätzlich etwa {chf(stak)} USD.")
    L.append("")
    # 3 Woche
    L.append("## 3. Diese Woche")
    if not tr.empty:
        tw = tr[(tr["scenario"] == "maker_plan") & (tr["exit_date"] >= woche_von.isoformat())]
        if len(tw):
            for _, x in tw.iterrows():
                L.append(f"- Geschlossen: {x['strategy']} {x['coin']}, {x['entry_date']} bis {x['exit_date']} ({x['exit_reason']}), netto {x['pnl_net_usd']:+.0f} USD, Kosten {x['costs_usd']:.0f} USD.")
    neu = []
    for s, coins in st.get("strategies", {}).items():
        for c, v in coins.items():
            pos = v.get("position")
            if pos and pos["entry_date"] >= woche_von.isoformat():
                neu.append(f"- Eröffnet: {s} {c} am {pos['entry_date']} zu {pos['entry_fill']:g}, Stopp {pos['stop']:g}.")
    L += neu or ["- Keine neuen Positionen."]
    L.append("")
    # 4 Offene Positionen und Orders
    L.append("## 4. Offene Positionen und Orders für die nächste Eröffnung")
    rows = []
    for s, coins in st.get("strategies", {}).items():
        for c, v in coins.items():
            pos = v.get("position"); od = v.get("order_next_open")
            if pos:
                rows.append(f"| {s} | {c} | seit {pos['entry_date']} ({len(pos['units'])} Unit) | {pos['last_close']:g} | {pos['stop']:g} | {od['kind'] + ' (' + od['reason'] + ')' if od else '–'} |")
            elif od:
                rows.append(f"| {s} | {c} | flach | – | – | {od['kind']} ({od['reason']}) am {od['fill_bar']} |")
    if rows:
        L.append("| Strategie | Coin | Position | Schluss | Stopp | Order |")
        L.append("|---|---|---|---|---|---|")
        L += rows
    else:
        L.append("- Alles flach, keine Order offen.")
    L.append("")
    # 5 Kosten
    L.append("## 5. Kosten (maker_plan)")
    tot = sum(v["scenarios"]["maker_plan"]["costs_usd"] for coins in st.get("strategies", {}).values() for v in coins.values())
    n_tr = 0 if tr.empty else int((tr["scenario"] == "maker_plan").sum())
    L.append(f"- Bezahlte Kosten seit Start: {chf(tot)} USD über alle drei Strategien, {n_tr} abgeschlossene Trades.")
    L.append("")
    # 5b Zusatz-Sleeves A/B (eigener Runner, nicht Teil von PAPER v1.0); Fehler duerfen den Bericht nie verhindern
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sleeves"))
        import sleeves_bericht
        L += sleeves_bericht.section_lines(heute)
    except Exception as e:
        L += [f"## 5b. Zusatz-Sleeves A/B", f"- Abschnitt nicht verfügbar: {e}", ""]
    L.append("## 6. Was Damian tun muss")
    L.append("- Nichts, solange Abschnitt 1 keine Fehler zeigt. Bei Fehlern behebt der Agent und vermerkt es in ENTSCHEIDE.")
    L.append("")
    L.append("_Hinweis: In 4 Monaten fallen nur wenige Trades an. Der Review prüft deshalb vor allem Betrieb und Kosten, nicht die Strategiegüte._")
    os.makedirs(os.path.join(out, "berichte"), exist_ok=True)
    p = os.path.join(out, "berichte", f"paper_wochenbericht_{heute.isoformat()}.md")
    open(p, "w").write("\n".join(L) + "\n")
    print(p)


if __name__ == "__main__":
    main()
