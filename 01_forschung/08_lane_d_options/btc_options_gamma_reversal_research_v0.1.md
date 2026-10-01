# BTC Options Context — Gamma und Verfall als Reversal-Kontext, Forschungsnotiz Version 0.1 (Lane D, vorgemerkt)

**Project Aurum II, `01_forschung/08_lane_d_options/`. 17.09.2026. Status: Vormerkung, keine Vorregistrierung, keine Integration in YAMATO oder RTC, keine Daten geladen. Bearbeitung erst nach den drei aktiven Lanes.**

## Hypothese (vorgemerkt, nicht geprüft)

BTC-Umkehrungen häufen sich um Optionsverfälle (monatlich und quartalsweise auf Deribit, Freitag 08:00 UTC), insbesondere wenn das Open Interest am Geld hoch ist und die Gamma-Exposure der Market Maker negativ ist (Händler müssen in Bewegungsrichtung hedgen, was Bewegungen bis zum Verfall verstärkt und danach umkehrt). Das ist eine Mikrostruktur-Hypothese, die einen Bottom- oder Peak-Kontext liefern könnte, keine Handelsregel.

## Potenzielle Merkmale (point-in-time, alle noch ohne Quelle)

`expiry_proximity` (Kerzen bis zum nächsten monatlichen und quartalsweisen Verfall, deterministisch aus dem Kalender), `atm_oi` (Open Interest der Strikes innerhalb ±5 Prozent des Spot, täglich), `gamma_exposure` (aggregierte Dealer-Gamma nach Standardkonvention, Vorzeichen), `put_call_oi_ratio`, `max_pain` als Bericht. Quellen wären Deribit-Historie (Tardis führt Deribit-Optionsketten seit 2019, dort auch kostenlos über die Deribit-Partnerschaft), Amberdata oder Laevitas. Point-in-time-Anforderung: Kettenschnappschüsse mit Zeitstempel, keine rekonstruierten Gamma-Werte.

## Prüfdesign (skizziert)

Kontextaufteilung bestehender Signale (YAMATO, RTC, BTC-B) nach `expiry_proximity` und Vorzeichen der Gamma-Exposure, ohne Filterwirkung, wie beim Halving. Ereignisstudie der 4h-Renditen um Verfälle gegen Zufallszeitpunkte. Multiplizität: eine Familie, Holm. Der Verdacht, der vorab genannt wird: Die Verfallseffekte sind 2019 bis 2021 anders als ab 2023 (ETF-Optionen seit Ende 2024 ändern die Struktur), also ist die Historie kurz und heterogen.

## Was vor einer Vorregistrierung geklärt sein muss

Datenquelle mit Prüfsummen, Definition der Gamma-Exposure (Konvention, Dealer-Annahme), Verfallskalender, und die Frage, ob der Effekt ohne die Optionsdaten bereits im Preis-Flow sichtbar ist (Redundanzprüfung gegen die Derivatives-Library).
