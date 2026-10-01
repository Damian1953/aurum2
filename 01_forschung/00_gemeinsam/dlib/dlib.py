"""
Project Aurum II — gemeinsame Derivatives- und Flow-Feature-Library, Version 0.2 (coin-uebergreifend identisch).
v0.2: delta_oi_zscore (Entscheid 17.09.2026): dOI_5d = OI_d / OI_{d-5 Kalendertage} - 1 auf der Tagesreihe, z-Score ueber die 60 vorangehenden Tageswerte
(Fenster schliesst den aktuellen Tag aus), gueltig ab der 00:00-Kerze des Tages d, fail-closed bei Luecken und vor Datenbeginn. Schwelle +-1.0 vorregistriert.
Quellen: Binance Spot 4h (alle Spalten), Binance Perp 4h (alle Spalten), Binance Funding 8h, Binance OI taeglich (00:00 UTC).
Alle Merkmale der Kerze t verwenden ausschliesslich Daten <= Kerzenschluss t. Fail-closed: fehlende Eingaben -> NaN.
Definitionen aus candlestick_flow_feature_library_spec_v0.1.md Abschnitt 5 (Flow-Merkmale).
"""
import numpy as np, pandas as pd

PARAMS = dict(vol_n=60, fund_n=270, basis_n=180, oi_lag_days=5, oi_z_days=60, ti_delta_n=6, atr_n=14)


def _load(path):
    import os
    if "validation" in os.path.basename(path).lower() and os.environ.get("AURUM_VALIDATION") != "1":
        raise PermissionError(f"Validation-Datei im Discovery-Kontext gesperrt: {path}")
    d = pd.read_csv(path); d["t"] = pd.to_datetime(d["t"], utc=True, format="ISO8601"); return d.reset_index(drop=True)


def _zscore(x, n):
    s = pd.Series(x); m = s.shift(1).rolling(n).mean(); sd = s.shift(1).rolling(n).std(ddof=0)
    return ((s - m) / sd).where(sd > 0).to_numpy()


def _wilder_atr(h, l, c, n):
    tr = np.empty(len(h)); tr[0] = h[0] - l[0]
    tr[1:] = np.maximum.reduce([h[1:] - l[1:], np.abs(h[1:] - c[:-1]), np.abs(l[1:] - c[:-1])])
    atr = np.full(len(h), np.nan)
    if len(h) >= n:
        atr[n - 1] = tr[:n].mean()
        for i in range(n, len(h)):
            atr[i] = (atr[i - 1] * (n - 1) + tr[i]) / n
    return atr


def build(spot_path, perp_path=None, funding_path=None, oi_path=None):
    """Liefert DataFrame auf dem Spot-4h-Raster mit allen Flow-Merkmalen."""
    P = PARAMS
    s = _load(spot_path)
    out = pd.DataFrame({"t": s["t"]})
    q = s["quote_volume"].to_numpy(); tbq = s["taker_buy_quote"].to_numpy(); v = s["volume"].to_numpy()
    c = s["close"].to_numpy(); o = s["open"].to_numpy()
    atr_prev = np.concatenate([[np.nan], _wilder_atr(s["high"].to_numpy(), s["low"].to_numpy(), c, P["atr_n"])[:-1]])
    with np.errstate(invalid="ignore", divide="ignore"):
        out["taker_imbalance"] = np.where(q > 0, (2 * tbq - q) / q, np.nan)
    out["volume_zscore"] = _zscore(v, P["vol_n"])
    out["trade_count_zscore"] = _zscore(s["trades"].to_numpy(), P["vol_n"])
    out["taker_buy_zscore"] = _zscore(tbq, P["vol_n"])
    ti = out["taker_imbalance"]
    out["ti_delta6"] = (ti - ti.shift(1).rolling(P["ti_delta_n"]).mean()).to_numpy()
    with np.errstate(invalid="ignore", divide="ignore"):
        prog = (c - o) / atr_prev
        out["price_progress_per_taker_volume"] = prog / np.maximum(out["taker_buy_zscore"].to_numpy(), 0.5)
        out["price_progress_per_volume"] = prog / np.maximum(out["volume_zscore"].to_numpy(), 0.5)
    # Perp: Basis und Perp-Taker-Imbalance auf demselben Raster
    if perp_path:
        p = _load(perp_path)[["t", "close", "quote_volume", "taker_buy_quote"]].rename(columns={"close": "perp_close", "quote_volume": "pq", "taker_buy_quote": "ptbq"})
        out = out.merge(p, on="t", how="left")
        with np.errstate(invalid="ignore", divide="ignore"):
            out["spot_perp_basis"] = (out["perp_close"] - c) / c
            out["taker_imbalance_perp"] = np.where(out["pq"] > 0, (2 * out["ptbq"] - out["pq"]) / out["pq"], np.nan)
        out["basis_zscore"] = _zscore(out["spot_perp_basis"].to_numpy(), P["basis_n"])
        out = out.drop(columns=["pq", "ptbq"])
    # Funding: zuletzt abgerechnete Rate zum Kerzenschluss (Settlement-Zeit <= Kerzenschluss)
    if funding_path:
        fr = _load(funding_path).sort_values("t")
        fr["fz"] = _zscore(fr["rate"].to_numpy(), P["fund_n"])
        fr["f7d"] = fr["rate"].rolling(21).sum() * (365.0 / 7.0)
        close_t = out["t"] + pd.Timedelta(hours=4) - pd.Timedelta(seconds=1)
        m = pd.merge_asof(pd.DataFrame({"t": out["t"], "close_t": close_t}).sort_values("close_t"), fr[["t", "rate", "fz", "f7d"]].rename(columns={"t": "ft"}),
                          left_on="close_t", right_on="ft", direction="backward")
        m = m.sort_values("t")
        out["funding_last"] = m["rate"].to_numpy(); out["funding_zscore"] = m["fz"].to_numpy(); out["funding_7d_ann"] = m["f7d"].to_numpy()
    # OI: Tagesschnappschuss 00:00 UTC des Tages d gilt ab Kerze 00:00 des Tages d (Framework Look-ahead-Regel)
    if oi_path:
        oi = pd.read_csv(oi_path); oi["d"] = pd.to_datetime(oi["t"], utc=True); oi = oi.sort_values("d")
        # dOI_5d ueber Kalendertage (nicht Zeilen), damit Luecken fail-closed bleiben
        oi_by_day = oi.set_index("d")["oi"]
        prev = oi_by_day.reindex(oi["d"] - pd.Timedelta(days=P["oi_lag_days"])).to_numpy()
        oi["doi5"] = oi["oi"].to_numpy() / prev - 1
        # z-Score der dOI_5d-Tagesreihe ueber die 60 vorangehenden Tage (aktueller Tag ausgeschlossen); Luecken -> NaN im Fenster -> NaN
        doi = oi["doi5"]
        mean60 = doi.shift(1).rolling(P["oi_z_days"], min_periods=P["oi_z_days"]).mean(); sd60 = doi.shift(1).rolling(P["oi_z_days"], min_periods=P["oi_z_days"]).std(ddof=0)
        # Kalender-Vollstaendigkeit: das Fenster muss genau 60 Kalendertage abdecken, sonst fail-closed
        span_ok = (oi["d"] - oi["d"].shift(P["oi_z_days"])).dt.days == P["oi_z_days"]
        oi["doi5_z"] = ((doi - mean60) / sd60).where((sd60 > 0) & span_ok)
        m = pd.merge_asof(pd.DataFrame({"t": out["t"]}), oi[["d", "oi", "doi5", "doi5_z"]], left_on="t", right_on="d", direction="backward")
        # nur gueltig, wenn der Schnappschuss nicht aelter als 1 Tag ist (fail-closed bei Luecken)
        age = (m["t"] - m["d"]).dt.total_seconds() / 86400.0
        out["open_interest"] = np.where(age <= 1.0, m["oi"], np.nan); out["delta_open_interest"] = np.where(age <= 1.0, m["doi5"], np.nan)
        out["delta_oi_zscore"] = np.where(age <= 1.0, m["doi5_z"], np.nan)
    return out


def coverage(df):
    cols = [c for c in df.columns if c != "t"]
    rows = []
    for c in cols:
        ok = df[c].notna()
        rows.append(dict(feature=c, n_valid=int(ok.sum()), share=round(float(ok.mean()), 3),
                         first_valid=str(df.loc[ok, "t"].min()) if ok.any() else None, last_valid=str(df.loc[ok, "t"].max()) if ok.any() else None))
    return pd.DataFrame(rows)
