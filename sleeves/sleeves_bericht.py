"""Abschnitt «Zusatz-Sleeves A/B» fuer den Paper-Wochenbericht (paper/wochenbericht.py ist nicht in der
paper-v1.0-Freeze-Liste). Liest nur Dateien; jeder Fehler wird als Hinweiszeile ausgegeben, nie geworfen."""
import datetime as dt, json, os

CFG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sleeves_config.json")
SERIEN = [("MVRV (CoinMetrics)", "coinmetrics/btc_CapMVRVCur.csv", "coinmetrics_mvrv", 14),
          ("WALCL (H.4.1)", "fred/WALCL.csv", "fred_macro", 56), ("WTREGEN (H.4.1)", "fred/WTREGEN.csv", "fred_macro", 56),
          ("RRPONTSYD", "fred/RRPONTSYD.csv", "fred_macro", 14), ("DTB3", "fred/DTB3.csv", "fred_macro", 14)]


def _last_row(p):
    with open(p) as fh:
        lines = [l for l in fh.read().splitlines() if l]
    return lines[-1].split(",") if len(lines) > 1 else None


def section_lines(heute, data_live=None, sleeves_out=None):
    data_live = data_live or os.environ.get("AURUM_DATA_LIVE", "/workspace/aurum2/data_live")
    sleeves_out = sleeves_out or os.environ.get("AURUM_SLEEVES_OUT", "/workspace/aurum2/paper_sleeves")
    L = ["## 5b. Zusatz-Sleeves A (Fed-Netto-Liquidität) und B (MVRV), BTC Spot Kraken"]
    try:
        cfg = json.load(open(CFG))
        if not cfg.get("enabled"):
            L.append("- Status: **nicht freigegeben** (Vorregistrierung v0.2 in Review, nicht eingefroren). Nur Datensammlung.")
        else:
            L.append(f"- Status: freigegeben, Startbar {cfg.get('start_bar')}.")
        try:
            ms = json.load(open(os.path.join(data_live, "macro", "status.json")))
        except Exception:
            ms = {}
        L.append("| Reihe | letzte Beobachtung | erster Abruf (UTC) | Alter Tage | Quelle ok |")
        L.append("|---|---|---|---|---|")
        for name, rel, src, max_age in SERIEN:
            p = os.path.join(data_live, "macro", rel)
            r = _last_row(p) if os.path.exists(p) else None
            ok = ms.get(src, {}).get("ok")
            okt = "ja" if ok else ("**nein**" if ok is False else "unbekannt")
            if r is None:
                L.append(f"| {name} | **keine Daten** | – | – | {okt} |"); continue
            age = (heute - dt.date.fromisoformat(r[0])).days
            flag = f"**{age} (veraltet)**" if age > max_age else str(age)
            L.append(f"| {name} | {r[0]} | {r[2]} | {flag} | {okt} |")
        bad = {k: v for k, v in ms.items() if not v.get("ok")}
        for k, v in bad.items():
            L.append(f"- Quellenfehler {k} ({v.get('consecutive_failures')}x in Folge, letzter Erfolg {v.get('last_ok_utc')}): {'; '.join(v.get('errors', [])[:2])}")
        sp = os.path.join(sleeves_out, "state", "state_latest.json")
        if cfg.get("enabled") and os.path.exists(sp):
            st = json.load(open(sp))
            for s, v in st.get("sleeves", {}).items():
                eq = v.get("equity_last", {})
                L.append(f"- Sleeve {s}: Status {v.get('status')}, Zustand {v.get('state') or 'FLACH'}, letzter Bar {v.get('last_bar')}, "
                         f"Wert maker_plan {eq.get('eq_maker_plan_cash0', 0):.0f} USD (Buy and Hold {eq.get('bh_maker_plan', 0):.0f} USD).")
            if st.get("rc"):
                L.append(f"- Runner-Exit-Code {st['rc']} (fail-closed), siehe {sp}.")
        L.append("- Kein Leistungsurteil vor der Langfrist-Auswertung (Vorregistrierung §7).")
    except Exception as e:
        L.append(f"- Abschnitt konnte nicht erstellt werden: {e}")
    L.append("")
    return L
