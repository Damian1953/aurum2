"""Gemeinsamer einseitiger Wochenbericht PAPER v1.0, Sleeve A und Leitplanke B (Deutsch, Schweizer Schreibweise,
feste Gestaltung LAYOUT, Review Claude M3).
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


# Feste Gestaltung des gemeinsamen einseitigen Wochenberichts (Review Claude M3): immer genau diese Abschnitte in dieser
# Reihenfolge; fehlt etwas, steht «–» oder ein Hinweis. Ein Fehler in einem Abschnitt verhindert den Bericht nie.
LAYOUT = (
    "## 1. Betrieb",
    "## 2. PAPER v1.0: Stand (maker_plan = K1; in Klammern taker_K2)",
    "## 3. PAPER v1.0: diese Woche, offene Positionen und Orders",
    "## 4. Sleeve A MAKRO_LIQ (Fed-Netto-Liquidität)",
    "## 5. Leitplanke B MVRV (kein Test)",
    "## 6. Datenquellen und Kosten",
    "## 7. Was Damian tun muss",
)
MAX_ZEILEN = 60      # eine Seite
MAX_ORDERZEILEN = 8


def _sleeves():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sleeves"))
    import sleeves_bericht
    return sleeves_bericht


def _read(out):
    st = json.load(open(os.path.join(out, "state", "state_latest.json")))
    hist = [json.loads(l) for l in open(os.path.join(out, "logs", "run_history.jsonl"))]
    def csv_or_empty(name):
        p = os.path.join(out, "ledger", name)
        return pd.read_csv(p) if os.path.exists(p) and os.path.getsize(p) > 1 else pd.DataFrame()
    return st, hist, csv_or_empty("equity_daily.csv"), csv_or_empty("trades.csv")


def sec_betrieb(ctx):
    st, hist, heute = ctx["st"], ctx["hist"], ctx["heute"]; woche_von = heute - dt.timedelta(days=7)
    h7 = [r for r in hist if r.get("started_utc", "")[:10] >= woche_von.isoformat()]
    ok7 = sum(1 for r in h7 if r.get("ok")); err7 = [e for r in h7 for e in r.get("errors", [])]
    L = [f"- PAPER v1.0: Läufe der letzten 7 Tage {len(h7)}, davon erfolgreich {ok7}; letzter Tagesbar "
         f"{min(v['last_bar'] for v in st['coins'].values()) if st.get('coins') else 'keine'}; "
         f"Fehler: {'keine' if not err7 else '; '.join(sorted(set(err7))[:3])}."]
    if st.get("warnings"):
        L.append(f"- Hinweise PAPER: {'; '.join(st['warnings'][:2])}.")
    L += _sleeves().status_lines(heute)
    return L


def sec_stand(ctx):
    st, heute, out = ctx["st"], ctx["heute"], ctx["out"]
    L = ["| Reihe | Wert USD | seit Start | MaxDD |", "|---|---|---|---|"]
    pf = st.get("portfolio", {})
    for s in ["W2", "W6", "T55_20", "BH"]:
        if s not in pf:
            L.append(f"| {NAMEN[s]} | – | – | – |"); continue
        p = pf[s]["maker_plan"]; q = pf[s].get("taker_K2", p)
        L.append(f"| {NAMEN[s]} | {chf(p['equity_usd'])} ({chf(q['equity_usd'])}) | {pct(p['equity_usd'] / p['start_usd'] - 1)} | {p['max_dd'] * 100:.1f} % |")
    start_usd = E.SLEEVE_USD * len(E.COINS)
    r = dtb3(out)
    tage = max((pd.Timestamp(heute, tz="UTC") - pd.Timestamp(st["start_bar"], tz="UTC")).days, 0)
    if r is not None and tage > 0:
        rate = float(r[r.index <= pd.Timestamp(heute, tz="UTC")].iloc[-1])
        rf = start_usd * ((1 + rate) ** (tage / 365) - 1)
        L.append(f"| Risikoloser USD-Satz (DTB3 {rate * 100:.2f} %) | {chf(start_usd + rf)} | {pct(rf / start_usd)} | 0.0 % |")
    else:
        L.append("| Risikoloser USD-Satz (DTB3) | – | – | – |")
    stak = sum(STAKING_REF.values()) * E.SLEEVE_USD * tage / 365
    L.append(f"- Staking-Referenz: Buy and Hold plus Staking auf ETH und SOL (2.58 % / 5.69 % p. a.) ergäbe zusätzlich etwa {chf(stak)} USD.")
    return L


def sec_woche(ctx):
    st, tr, heute = ctx["st"], ctx["tr"], ctx["heute"]; woche_von = heute - dt.timedelta(days=7)
    L = []
    if not tr.empty:
        tw = tr[(tr["scenario"] == "maker_plan") & (tr["exit_date"] >= woche_von.isoformat())]
        for _, x in tw.head(MAX_ORDERZEILEN).iterrows():
            L.append(f"- Geschlossen: {x['strategy']} {x['coin']}, {x['entry_date']} bis {x['exit_date']} ({x['exit_reason']}), netto {x['pnl_net_usd']:+.0f} USD.")
    neu = sum(1 for coins in st.get("strategies", {}).values() for v in coins.values()
              if v.get("position") and v["position"]["entry_date"] >= woche_von.isoformat())
    L.append(f"- Neu eröffnete Positionen diese Woche: {neu}.")
    rows = []
    for s, coins in st.get("strategies", {}).items():
        for c, v in coins.items():
            pos = v.get("position"); od = v.get("order_next_open")
            if pos:
                rows.append(f"| {s} | {c} | seit {pos['entry_date']} | {pos['stop']:g} | {od['kind'] + ' (' + od['reason'] + ')' if od else '–'} |")
            elif od:
                rows.append(f"| {s} | {c} | flach | – | {od['kind']} ({od['reason']}) am {od['fill_bar']} |")
    L += ["", "| Strategie | Coin | Position | Stopp | Order nächste Eröffnung |", "|---|---|---|---|---|"]
    L += rows[:MAX_ORDERZEILEN] or ["| – | – | alles flach | – | keine Order offen |"]
    if len(rows) > MAX_ORDERZEILEN:
        L.append(f"- … und {len(rows) - MAX_ORDERZEILEN} weitere (siehe state_latest.json).")
    return L


def sec_a(ctx):
    return _sleeves().section_a(ctx["heute"])


def sec_b(ctx):
    return _sleeves().section_b(ctx["heute"])


def sec_daten(ctx):
    st, tr = ctx["st"], ctx["tr"]
    tot = sum(v["scenarios"]["maker_plan"]["costs_usd"] for coins in st.get("strategies", {}).values() for v in coins.values())
    n_tr = 0 if tr.empty else int((tr["scenario"] == "maker_plan").sum())
    return [f"- Kosten PAPER v1.0 seit Start (maker_plan): {chf(tot)} USD, {n_tr} abgeschlossene Trades.", ""] + _sleeves().data_lines(ctx["heute"])


def sec_damian(ctx):
    return ["- Nichts, solange Abschnitt 1 keine Fehler zeigt. Bei Fehlern behebt der Agent und vermerkt es in ENTSCHEIDE.",
            "- _Hinweis: In 4 Monaten fallen nur wenige Trades an. Der Review prüft vor allem Betrieb und Kosten, nicht die Strategiegüte._"]


SECTIONS = (sec_betrieb, sec_stand, sec_woche, sec_a, sec_b, sec_daten, sec_damian)


def build(out, heute):
    """Gemeinsamer einseitiger Wochenbericht PAPER v1.0, Sleeve A und Leitplanke B (feste Gestaltung LAYOUT)."""
    try:
        st, hist, eq, tr = _read(out)
    except Exception as e:
        st, hist, eq, tr = {"start_bar": str(heute), "coins": {}}, [], pd.DataFrame(), pd.DataFrame()
        st["warnings"] = [f"PAPER-Ausgaben nicht lesbar: {e}"]
    ctx = dict(st=st, hist=hist, eq=eq, tr=tr, heute=heute, out=out)
    L = [f"# Wochenbericht Aurum II {heute.isoformat()}: PAPER v1.0, Sleeve A, Leitplanke B", "",
         f"PAPER_PREREG_v1.0 (SHA {str(st.get('prereg_sha256'))[:12]}…), Startbar {st.get('start_bar')}, Review spätestens "
         f"{REVIEW_DATUM.isoformat()} (noch {(REVIEW_DATUM - heute).days} Tage). Keine Keys, keine Orders: alle Zahlen hypothetisch."]
    for head, fn in zip(LAYOUT, SECTIONS):
        L += ["", head]
        try:
            L += fn(ctx)
        except Exception as e:
            L.append(f"- Abschnitt nicht verfügbar: {e}")
    return L


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--datum")
    a = ap.parse_args()
    out = os.environ.get("AURUM_PAPER_OUT", "/workspace/aurum2/paper")
    heute = dt.date.fromisoformat(a.datum) if a.datum else dt.date.today()
    L = build(out, heute)
    os.makedirs(os.path.join(out, "berichte"), exist_ok=True)
    p = os.path.join(out, "berichte", f"paper_wochenbericht_{heute.isoformat()}.md")
    open(p, "w").write("\n".join(L) + "\n")
    print(p)


if __name__ == "__main__":
    main()
