"""Ableitung der Basis-Exposure aus den UNVERAENDERTEN Paper-Regeln (paper/paper_engine.py, nur gelesen, nicht geaendert).
Die Basis entscheidet wie im Paper (Start flach ab PAPER START_BAR); das Overlay liest daraus je Tag die nominelle
Exposure E (W2/T55_20: 0 oder 1.0; W6: 0, 0.50, 0.75, 1.00) und die Fill-Ereignisse."""
import os, sys
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "paper"))
import paper_engine as P          # noqa: E402  (eingefroren, paper-v1.0-freeze; hier nur Import)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voltarget_engine as V      # noqa: E402

STRATS = list(P.STRATS)
COINS = list(P.COINS)


def load_bars(path, now_utc=None):
    """Kraken-Tageskerzen wie PAPER F6 (nur abgeschlossene Bars), mit Holdout-/Validation-Sperre."""
    return P.load_kraken_1d(V.guard_path(path), now_utc)


def base_days(d, strat, paper_start=None):
    """Liste dict(date, open, close, E, event) je Bar plus (next_E, next_event) fuer den Tag nach dem letzten Bar."""
    dec = P.decide(d, strat, start_ts=P.START_BAR if paper_start is None else paper_start)
    idx = d.index
    E = pd.Series(0.0, index=idx); ev = {}
    trs = dec["trades"] + ([dec["open"]] if dec["open"] else [])
    for tr in trs:
        exit_t = tr.get("exit_t")
        for k, (_, u, ft) in enumerate(tr["units"]):
            m = (idx >= ft) if exit_t is None else ((idx >= ft) & (idx < exit_t))
            E[m] += u
            ev[ft] = "entry" if k == 0 else "add"
        if exit_t is not None:
            ev[exit_t] = "exit_stop" if tr["exit_reason"] in P.STOP_REASONS else "exit"
    days = [dict(date=t.date(), open=float(d.at[t, "open"]), close=float(d.at[t, "close"]), E=round(float(E[t]), 10),
                 event=ev.get(t)) for t in idx]
    next_E, next_ev = (days[-1]["E"] if days else 0.0), None
    o = dec["order"]
    if o is not None:
        if o["kind"] == "ENTRY":
            next_E, next_ev = (0.5 if strat == "W6" else 1.0), "entry"
        elif o["kind"] == "ADD":
            next_E, next_ev = next_E + 0.25, "add"
        elif o["kind"] == "EXIT":
            next_E, next_ev = 0.0, ("exit_stop" if o["reason"] in P.STOP_REASONS else "exit")
    return days, next_E, next_ev


def start_index(days, start_date):
    for i, x in enumerate(days):
        if x["date"] >= start_date:
            return i
    return len(days)
