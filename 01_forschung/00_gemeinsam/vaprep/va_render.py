"""
Project Aurum II — Visual AI Second Opinion: standardisiertes Chart-Rendering, Version 0.1.
Vertrag (visual_ai_second_opinion_plan_v0.1.md Abschnitt 3): 120 Kerzen 4h bis einschliesslich Bewertungskerze, OHLC plus Volumen,
keine Indikatoren, keine Datumsachse, Preise auf den Schluss der Bewertungskerze normiert (Prozent), Achsenbereich nur aus dem
sichtbaren Fenster, feste Groesse und Farben, kein Coin-Name, keine Zukunft. Ausgabe PNG 800x500. Prompt in PROMPT_V01 eingefroren.
"""
import hashlib, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SPEC = dict(lookback=120, width_px=800, height_px=500, dpi=100, up="#2b8a3e", down="#c92a2a", wick="#333333", vol="#9aa5b1", bg="#ffffff")

PROMPT_V01 = """You see a standardized candlestick chart of an unnamed asset on a fixed intraday timeframe. The last candle on the right is the most recent completed candle. Prices are shown in percent relative to the last close. No future information is shown.
Assess the chart and answer only with a JSON object with these five fields, each a number between 0 and 1:
{"bottom_reversal_confidence": ..., "trend_continuation_confidence": ..., "distribution_peak_confidence": ..., "failed_breakdown_or_breakout_confidence": ..., "pattern_confidence": ...}
Do not name the asset, do not give price targets, do not recommend a trade."""


def render(o, h, l, c, v, out_path):
    """o,h,l,c,v: Arrays der letzten <=120 Kerzen, letzte Kerze = Bewertungskerze. Normierung auf c[-1]."""
    S = SPEC; n = len(c); assert n <= S["lookback"]
    ref = c[-1]; O, H, L, C = (np.asarray(x, float) / ref * 100 - 100 for x in (o, h, l, c))
    fig = plt.figure(figsize=(S["width_px"] / S["dpi"], S["height_px"] / S["dpi"]), dpi=S["dpi"], facecolor=S["bg"])
    ax = fig.add_axes([0.06, 0.28, 0.92, 0.68]); axv = fig.add_axes([0.06, 0.06, 0.92, 0.18], sharex=ax)
    x = np.arange(n)
    for i in range(n):
        col = S["up"] if C[i] >= O[i] else S["down"]
        ax.plot([x[i], x[i]], [L[i], H[i]], color=S["wick"], linewidth=0.8, zorder=1)
        ax.add_patch(plt.Rectangle((x[i] - 0.35, min(O[i], C[i])), 0.7, max(abs(C[i] - O[i]), 0.02), color=col, zorder=2))
    axv.bar(x, np.asarray(v, float) / max(np.asarray(v, float).max(), 1e-9), width=0.7, color=S["vol"])
    lo, hi = L.min(), H.max(); pad = (hi - lo) * 0.03
    ax.set_xlim(-1, S["lookback"]); ax.set_ylim(lo - pad, hi + pad)
    ax.set_xticks([]); axv.set_xticks([]); axv.set_yticks([])
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda y, _: f"{y:+.0f}%"))
    ax.tick_params(labelsize=8); ax.grid(False)
    for a in (ax, axv):
        for s in a.spines.values(): s.set_visible(False)
    fig.savefig(out_path, dpi=S["dpi"], facecolor=S["bg"]); plt.close(fig)
    return hashlib.sha256(open(out_path, "rb").read()).hexdigest()


def frozen_manifest(path):
    m = dict(spec=SPEC, prompt=PROMPT_V01, prompt_sha256=hashlib.sha256(PROMPT_V01.encode()).hexdigest(),
             render_code_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest(), model="offen, vor dem Test festzulegen", temperature=0)
    json.dump(m, open(path, "w"), indent=1); return m


if __name__ == "__main__":
    rng = np.random.default_rng(1)   # synthetischer Test ohne Marktbezug
    r = np.cumsum(rng.normal(0, 0.01, 120)); c = 100 * np.exp(r); o = np.concatenate([[100], c[:-1]])
    h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.005, 120))); l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.005, 120)))
    v = rng.lognormal(0, 0.5, 120)
    print(render(o, h, l, c, v, "va_synthetic_test.png")); print(json.dumps(frozen_manifest("va_manifest_v0.1.json"), indent=1)[:400])
