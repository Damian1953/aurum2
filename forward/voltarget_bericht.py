"""Abschnitt VOLTARGET-Overlay fuer den gemeinsamen einseitigen Wochenbericht (paper/wochenbericht.py).

Liest NUR die Ausgabe des VOLTARGET-Runners (Branch voltarget-v0, eigener Code) und dessen Konfiguration, importiert
keinen VOLTARGET-Code. Dadurch bleibt der Bericht auf diesem Branch und der Overlay-Code auf voltarget-v0 ohne
gemeinsame Dateien (keine Merge-Konflikte). Feste Gestaltung: immer drei Zeilen W2, W6, T55_20 und eine Zeile
«s < 1 je Coin»; fehlende Werte als «–». Fehler werden nie geworfen.
Schnittstelle state/state_latest.json (vom VOLTARGET-Runner geschrieben):
  rc, run_utc,
  summary[strat] = dict(status, coins_ok, coins_total, tage_offen, tage_offen_s_lt_1, sync_kosten_usd)   (maker_plan)
  s_verteilung[coin] = dict(tage, tage_s_lt_1, s_min)
"""
import json, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = os.path.join(REPO, "voltarget", "voltarget_config.json")
STRATS = ("W2", "W6", "T55_20")


def _out(vt_out):
    return vt_out or os.environ.get("AURUM_VOLTARGET_OUT", "/workspace/aurum2/paper_voltarget")


def freigabe():
    if not os.path.exists(CFG):
        return False, "auf diesem Stand nicht vorhanden (Branch voltarget-v0), nicht freigegeben"
    try:
        cfg = json.load(open(CFG))
    except Exception as e:
        return False, f"Konfiguration nicht lesbar ({e})"
    if cfg.get("enabled") is not True:
        return False, "nicht freigegeben (Kandidat, nicht eingefroren)"
    return True, f"freigegeben, Startbar {cfg.get('start_bar')}"


def section(heute, vt_out=None):
    L = ["| Overlay | Status | Coins ok | Coin-Tage Basis offen | davon s < 1 | Sync-Kosten VT (K1, USD) |", "|---|---|---|---|---|---|"]
    try:
        ok, text = freigabe()
        sp = os.path.join(_out(vt_out), "state", "state_latest.json")
        st = json.load(open(sp)) if ok and os.path.exists(sp) else None
        summ = (st or {}).get("summary", {})
        for s in STRATS:
            x = summ.get(s)
            if not x:
                L.append(f"| {s} | {text if st is None else 'keine Daten'} | – | – | – | – |"); continue
            L.append(f"| {s} | {x.get('status')} | {x.get('coins_ok', '–')}/{x.get('coins_total', '–')} | {x.get('tage_offen', '–')} | "
                     f"{x.get('tage_offen_s_lt_1', '–')} | {x.get('sync_kosten_usd', 0):.2f} |")
        sv = (st or {}).get("s_verteilung", {})
        if sv:
            L.append("- s < 1 je Coin (Tage seit Start): " + ", ".join(
                f"{c} {v.get('tage_s_lt_1', '–')}/{v.get('tage', '–')} (min {v.get('s_min') if v.get('s_min') is None else round(v['s_min'], 2)})"
                for c, v in sorted(sv.items())) + ".")
        else:
            L.append("- s < 1 je Coin: –")
        if st and st.get("rc"):
            L.append(f"- Runner-Exit-Code {st['rc']} (fail-closed), siehe {sp}.")
    except Exception as e:
        L.append(f"- Abschnitt nicht lesbar: {e}")
    L.append("- Kein Leistungsurteil vor der Leistungsauswertung (VOLTARGET §8.1); Sync-Kosten getrennt von Vol-Anpassungen.")
    return L
