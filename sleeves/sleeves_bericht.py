"""Abschnitte Sleeve A und Leitplanke B fuer den gemeinsamen einseitigen Wochenbericht (paper/wochenbericht.py,
nicht in der paper-v1.0-Freeze-Liste). Feste Gestaltung (Review Claude M3): jeder Abschnitt hat immer dieselben Zeilen,
fehlende Werte erscheinen als «–». Liest nur Dateien; jeder Fehler wird als Hinweiszeile ausgegeben, nie geworfen."""
import datetime as dt, json, os

CFG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sleeves_config.json")
SERIEN = [("MVRV (CoinMetrics)", "coinmetrics/btc_CapMVRVCur.csv", "coinmetrics_mvrv", 14),
          ("WALCL (H.4.1, Mi)", "fred/WALCL.csv", "fred_macro", 56), ("WDTGAL (H.4.1, Mi)", "fred/WDTGAL.csv", "fred_macro", 56),
          ("RRPONTSYD", "fred/RRPONTSYD.csv", "fred_macro", 14), ("DTB3", "fred/DTB3.csv", "fred_macro", 14)]
MVRV_EXIT = 3.5
SATZ_B_IDENTISCH = ("Solange MVRV seit Start nie über 3.5 lag, ist B identisch mit Buy and Hold "
                    "(gleiche Menge BTC, gleicher Einstieg, gleiche Kosten).")
SATZ_B_LEITPLANKE = ("Leitplanke für den Kernbestand: keine Gates, kein Erfolgsanspruch, kein Test. Erreicht MVRV 3.5 "
                     "nicht mehr, löst die Regel nie aus; das ist ein zulässiges Ergebnis.")


def _paths(data_live, sleeves_out):
    return (data_live or os.environ.get("AURUM_DATA_LIVE", "/workspace/aurum2/data_live"),
            sleeves_out or os.environ.get("AURUM_SLEEVES_OUT", "/workspace/aurum2/paper_sleeves"))


def _last_row(p):
    with open(p) as fh:
        lines = [l for l in fh.read().splitlines() if l]
    return lines[-1].split(",") if len(lines) > 1 else None


def _cfg():
    try:
        return json.load(open(CFG))
    except Exception:
        return {}


def _state(sleeves_out):
    cfg = _cfg(); sp = os.path.join(sleeves_out, "state", "state_latest.json")
    if cfg.get("enabled") and os.path.exists(sp):
        return json.load(open(sp))
    return None


def _usd(x):
    return "–" if x is None else f"{x:,.0f}".replace(",", "'")


def _freigabe():
    cfg = _cfg()
    if not cfg.get("enabled"):
        return "nicht freigegeben (Kandidat v1.0, nicht eingefroren), nur Datensammlung"
    return f"freigegeben, Startbar {cfg.get('start_bar')}"


def status_lines(heute, data_live=None, sleeves_out=None):
    """Eine Zeile je Sleeve fuer Abschnitt Betrieb."""
    _, so = _paths(data_live, sleeves_out)
    try:
        st = _state(so)
        if st is None:
            return [f"- Sleeves A/B: {_freigabe()}."]
        rc = st.get("rc")
        return [f"- Sleeves A/B: letzter Lauf {st.get('run_utc')} UTC, Exit-Code {rc}"
                + (" (fail-closed, siehe state_latest.json)." if rc else ".")]
    except Exception as e:
        return [f"- Sleeves A/B: Status nicht lesbar ({e})."]


def section_a(heute, data_live=None, sleeves_out=None):
    _, so = _paths(data_live, sleeves_out)
    L = ["| Sleeve A | Status | Zustand | Wert maker_plan, Cash DTB3 (taker_K2) | B1 Buy and Hold | Wechsel | Phasen > 13 Wochen |",
         "|---|---|---|---|---|---|---|"]
    try:
        st = _state(so); a = (st or {}).get("sleeves", {}).get("A")
        if not a:
            L.append(f"| A | {_freigabe()} | – | – | – | – | – |")
        else:
            eq = a.get("equity_last", {}); ph = a.get("regimephasen") or {}
            L.append(f"| A | {a.get('status')} | {a.get('state') or 'FLACH'} | {_usd(eq.get('eq_maker_plan_dtb3'))} "
                     f"({_usd(eq.get('eq_taker_K2_dtb3'))}) | {_usd(eq.get('bh_maker_plan'))} | {a.get('n_wechsel', '–')} | "
                     f"{ph.get('laenger_13w', '–')} von {ph.get('phasen', '–')} |")
    except Exception as e:
        L.append(f"| A | Abschnitt nicht lesbar ({e}) | – | – | – | – | – |")
    L.append("- Kein Leistungsurteil vor der Langfrist-Auswertung (MAKRO_LIQ §7). Sensitivität Cash 0 % in state_latest.json.")
    return L


def section_b(heute, data_live=None, sleeves_out=None):
    dl, so = _paths(data_live, sleeves_out)
    L = ["| Leitplanke B | Status | Zustand | MVRV (Stand) | Abstand zu 3.5 | identisch mit Buy and Hold |", "|---|---|---|---|---|---|"]
    try:
        p = os.path.join(dl, "macro", "coinmetrics", "btc_CapMVRVCur.csv")
        r = _last_row(p) if os.path.exists(p) else None
        mv = f"{float(r[1]):.2f} ({r[0]})" if r else "keine Daten"
        ab = f"{MVRV_EXIT - float(r[1]):+.2f}" if r else "–"
        st = _state(so); b = (st or {}).get("sleeves", {}).get("B")
        if not b:
            L.append(f"| B | {_freigabe()} | – | {mv} | {ab} | – |")
        else:
            idt = b.get("identisch_bh"); idt = "ja" if idt else ("nein" if idt is False else "–")
            L.append(f"| B | {b.get('status')} | {b.get('state') or 'FLACH'} | {mv} | {ab} | {idt} |")
    except Exception as e:
        L.append(f"| B | Abschnitt nicht lesbar ({e}) | – | – | – | – |")
    L.append(f"- {SATZ_B_IDENTISCH}")
    L.append(f"- {SATZ_B_LEITPLANKE}")
    return L


def data_lines(heute, data_live=None, sleeves_out=None):
    dl, _ = _paths(data_live, sleeves_out)
    L = ["| Reihe | letzte Beobachtung | erster Abruf (UTC) | Alter Tage | Quelle ok |", "|---|---|---|---|---|"]
    try:
        try:
            ms = json.load(open(os.path.join(dl, "macro", "status.json")))
        except Exception:
            ms = {}
        for name, rel, src, max_age in SERIEN:
            p = os.path.join(dl, "macro", rel)
            r = _last_row(p) if os.path.exists(p) else None
            ok = ms.get(src, {}).get("ok")
            okt = "ja" if ok else ("**nein**" if ok is False else "unbekannt")
            if r is None:
                L.append(f"| {name} | **keine Daten** | – | – | {okt} |"); continue
            age = (heute - dt.date.fromisoformat(r[0])).days
            flag = f"**{age} (veraltet)**" if age > max_age else str(age)
            L.append(f"| {name} | {r[0]} | {r[2]} | {flag} | {okt} |")
        for k, v in {k: v for k, v in ms.items() if not v.get("ok")}.items():
            L.append(f"- Quellenfehler {k} ({v.get('consecutive_failures')}x in Folge, letzter Erfolg {v.get('last_ok_utc')}): "
                     f"{'; '.join(v.get('errors', [])[:2])}")
    except Exception as e:
        L.append(f"- Datenquellen nicht lesbar: {e}")
    return L


def section_lines(heute, data_live=None, sleeves_out=None):
    """Rueckwaertskompatibel: A, B und Datenquellen als ein Block."""
    L = ["## Sleeve A und Leitplanke B"]
    for fn in (status_lines, section_a, section_b, data_lines):
        try:
            L += fn(heute, data_live, sleeves_out)
        except Exception as e:
            L.append(f"- Abschnitt konnte nicht erstellt werden: {e}")
    L.append("")
    return L
