import pandas as pd, numpy as np, struct
def load(path):
    d = pd.read_csv(path); d["t"] = pd.to_datetime(d["t"], utc=True, format="ISO8601").dt.tz_localize(None).dt.normalize()
    d = d.set_index("t")[["open","high","low","close"]].astype(float).sort_index()
    return d
def tr(d):
    pc = d["close"].shift(1)
    return pd.concat([d["high"]-d["low"], (d["high"]-pc).abs(), (d["low"]-pc).abs()], axis=1).max(axis=1)
def atr_sma(d, n=180): return tr(d).rolling(n).mean()
def atr_wilder(d, n=180): return tr(d).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
def trades():
    t = pd.read_csv("mtp_btc_trades_observed_v1.csv", parse_dates=["entry","exit"]); t.index = range(1, len(t)+1); return t
def is_f32(x): return struct.unpack('f', struct.pack('f', x))[0] == x
