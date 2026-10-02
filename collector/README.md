# Datensammler (Schritt 2)

Nur öffentliche Endpunkte, keine Keys, kein Trading. Code `collector/collect.py`, Ausgabe nach `/workspace/aurum2/data_live/` (über `AURUM_DATA_LIVE` änderbar).

| Quelle | Endpunkt | Ablage | Spalten |
|---|---|---|---|
| Kraken Futures Funding, 15 Symbole wie `02_daten/raw/kraken_futures_funding` | `futures.kraken.com/derivatives/api/v4/historicalfundingrates` (rollendes Jahr, stündlich) | `kraken_futures_funding/<SYM>.csv` | `t,fundingRate,relativeFundingRate` |
| Kraken Spot OHLC, 10 Coins, 1h/4h/1d | `api.kraken.com/0/public/OHLC` (je 720 Bars), **nur abgeschlossene Bars** | `kraken_ohlc/<COIN>USD_<tf>.csv` | `t,open,high,low,close,volume,trades` (t = Bar-Beginn UTC) |
| Binance USDM Funding, 10 Projekt-Symbole | `data.binance.vision` Monats-ZIPs `fundingRate`, CHECKSUM geprüft | `binance_funding/<SYM>_funding.csv` | `t,rate,interval_hours,calc_time_ms` |
| Binance USDM Universum | S3-Listing `data/futures/um/daily/klines/` + HEAD auf die 1d-Kline von gestern/vorgestern | `binance_universe/snapshot_<datum>.csv`, `first_seen.csv` | `symbol,active_proxy,last_daily_kline` |
| Kraken Futures Instrumente (ab v1.1) | `futures.kraken.com/derivatives/api/v3/instruments`, nur Perpetuals `PF_*`/`PI_*` | `kraken_futures_instruments/snapshot_<datum>.csv`, `first_seen.csv` | `symbol,type,tradeable,base,quote,opening_date` |
| Kraken Futures Ticker (ab v1.1, XS21-Gate M3) | `.../api/v3/tickers`, `tag=perpetual`, ein Snapshot je Lauf (Schluessel = `serverTime`) | `kraken_futures_tickers/<symbol>.csv` | `t,tradeable,suspended,vol24h_usd,vol24h_base,open_interest,last,last_time,mark_price,opening_date` (`vol24h_usd` = `volumeQuote`, rollende 24h; fuer Tagesmediane den ersten Snapshot je UTC-Tag nehmen) |
| Kraken Spot Ticker (ab v1.1) | `api.kraken.com/0/public/Ticker`, 10 Projekt-Coins | `kraken_spot_tickers/<coin>.csv` | `t,last,vol24h_base,vwap24h,vol24h_usd,trades24h` (`vol24h_usd` = 24h-Volumen × 24h-VWAP, rollend) |
| CoinMetrics MVRV (ab v1.2, Sleeve B) | `community-api.coinmetrics.io/v4/timeseries/asset-metrics` BTC `CapMVRVCur` 1d, letzte 30 Tage, ohne Key | `macro/coinmetrics/btc_CapMVRVCur.csv` | `obs_date,value,first_fetch_utc,run_id,initial_load` (First-Release: nur neue Beobachtungen angehaengt, Revisionen in `macro/revisions.jsonl`, Rohantwort in `macro/_raw/`) |
| FRED Makro (ab v1.2, Sleeve A) | `fred.stlouisfed.org/graph/fredgraph.csv` (ohne Key) `WALCL`, `WDTGAL` (ab v1.3, Mittwochsstand; bis v1.2 `WTREGEN`), `RRPONTSYD`, `DTB3`, letzte 200 Tage | `macro/fred/<serie>.csv` | wie MVRV; FRED antwortet nicht auf eigene User-Agents, daher Python-Standard-UA |

`fapi.binance.com` ist von der Box geoblockt (HTTP 451). Nach Vorgabe gibt es keinen Umweg. Deshalb kommt Binance Funding mit bis zu einem Monat Verzug, und das Universum ist nur eine Näherung (siehe `OFFENE_PUNKTE.md` OP-6).

## Garantien

- Append-only mit Dedup über den Zeitstempel. Bestehende Zeilen werden nie verändert. Weicht ein neuer Wert für einen bestehenden Schlüssel ab, wird das in `conflicts.jsonl` protokolliert und nicht überschrieben.
- Validierung nach `02_daten/README.md`: Ein Batch mit kritischem Defekt landet vollständig in `_quarantine/` und wird nicht geschrieben.
- Lock je Datei und für den Gesamtlauf. Geschrieben wird in eine temporäre Datei, dann fsync und `os.replace`.
- Retries mit exponentiellem Backoff (Netzfehler, 429, 5xx), Timeout 30 s. Der Wrapper macht nach 15 min einen zweiten Versuch.
- `provenance.jsonl`: ein Eintrag je Batch mit URL, HTTP-Status, SHA-256 der Antwort, Zählern und Zeitraum.
- `last_run_status.json`: run_id, Zeiten, `ok`, Status und Fehler je Quelle. `run_history.jsonl` hält alle Läufe fest. Logs liegen unter `logs/`.
- Exit-Codes: 0 ok, 1 mindestens eine Quelle fehlerhaft, 2 anderer Lauf aktiv.
- Zeitstempel einheitlich `YYYY-MM-DDTHH:MM:SSZ` (UTC). Bei Binance bleibt die exakte `calc_time` in Millisekunden erhalten.

Einmalig mit Historie aus dem Projekt vorbefüllt (`--seed-from data/raw`, Provenance `source=seed`). Grund: Das rollende Kraken-Fenster liefert die Funding-Daten ab 2025-09-17 nicht mehr.

## Planung auf der Box

- Die Box hat kein systemd (PID 1 ist `tini`). cron wurde per `apt-get install cron` installiert und wird als `/usr/sbin/cron` gestartet.
- Eintrag in der crontab des Users `box`: `CRON_TZ=Europe/Zurich` und `15 6 * * * /workspace/aurum2/repo/collector/run_collector.sh`.
- `collector/ensure_scheduler.sh` startet cron, falls er nicht läuft, setzt den Eintrag, falls er fehlt, und holt einen verpassten Tageslauf nach (nach 06:15 und heute noch kein erfolgreicher Lauf).
- `ensure_scheduler.sh` wird aus `~/.bashrc` aufgerufen. Nach einem Neustart der Box läuft cron also erst wieder, wenn irgendeine Shell geöffnet wird (z.B. durch einen Agenten). Der verpasste Lauf wird dann nachgeholt, die Daten selbst gehen nicht verloren, weil die Quellen 30 bis 720 Bars bzw. ein Jahr zurückreichen.

Manuell: `make collect` oder `collector/run_collector.sh`. Status: `cat /workspace/aurum2/data_live/last_run_status.json`.

- Seit 01.10.2026 setzt `ensure_scheduler.sh` zusätzlich die Paper-Einträge `aurum2-paper` (06:50, `paper/run_paper.sh --if-needed`) und `aurum2-paper-bericht` (montags 07:10) und holt einen verpassten Paper-Lauf nach 06:50 nach (siehe `paper/README.md`).
