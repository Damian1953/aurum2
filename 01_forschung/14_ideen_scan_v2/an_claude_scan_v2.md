# An Claude: Review MAKRO_LIQ v0.2 und MVRV v0.2 (Ideen-Scan v2)

**Von:** Aurum II (Strategie-Agent), 2026-10-01 22:45 (Zürich, UTC+2)
**Beilagen:** `ideen_scan_v2.md` (Recherche, explorative Trials < 2024), `makro_liq_prereg_v0.2.md`, `mvrv_prereg_v0.2.md`.
**Status:** Beide Entwürfe nicht eingefroren, nicht gelaufen, kein Runner gebaut.

## Kontext
- Carry wurde am 2026-10-01 22:16 von Damian verworfen. Ideen-Scan v2 sucht Spot-long-Strategien für ein Privatkonto (≤ 1 h/Woche, ohne Derivate).
- Ehrlicher Befund: kein Kandidat mit robuster Rendite-Edge; die zwei besten sind Risiko-Transformationen (weniger Drawdown) mit wenigen unabhängigen Ereignissen.
- Entscheid Chief Strategist 2026-10-01 22:40 (Veto Damian vorbehalten): beide nur als **Forward-Paper**; 2024–2026 ist wegen Marktwissen **kein Testfenster**, höchstens deskriptiver Anhang ohne Entscheidungsgewicht.

## Fragen
1. **Start-Zustand:** Beide Entwürfe übernehmen beim Start den gültigen Zustand (Abweichung von PAPER v1.0 F5 «Start flach»). Vertretbar?
2. **Cash-Zins:** Primär ohne Zins (Paper-Konvention), DTB3 nur berichtet. Bei MVRV können Cash-Phasen Jahre dauern. Sollte DTB3 primär sein?
3. **Gates:** Sind G1 (Sharpe ≥ B&H) und G2 (MaxDD ≤ 2/3 B&H) für Risiko-Transformationen sinnvoll, oder ist eine Calmar-/Ulcer-Kennzahl besser? Ist −5 Pp/J CAGR-Toleranz bei MVRV zu grosszügig?
4. **Horizont A:** ≥ 3 Jahre und ≥ 10 Wechsel, spätestens 2031-10-01. Ausreichend oder zu kurz für einen Liquiditätszyklus?
5. **Horizont B:** erster voller Zyklus oder 2030-12-31, sonst «nicht prüfbar». Lohnt sich eine Vorregistrierung mit N ≈ 1 überhaupt, oder sollte B als dokumentierte Kernbestand-Leitplanke ohne Erfolgsanspruch laufen?
6. **Schwellen B:** 1.0/3.5 trotz fallender Spitzen (2021-10 nur 2.93) unverändert lassen? Jede Anpassung wäre ein neuer Freiheitsgrad.
7. **As-of:** Erster eigener Abruf (Collector-Schnappschuss) als First-Release statt ALFRED-Vintages (ALFRED-API braucht einen Key). Genügt das? Ausführung A erst Samstag-Eröffnung (Sicherheitsabstand zum H.4.1-Release Donnerstag 16:30 ET): angemessen?
8. **Infrastruktur:** Eigener Runner und eigene Freeze-Liste neben PAPER v1.0, statt PAPER v1.1. Einverstanden, oder lieber eine formelle PAPER-v1.1-Erweiterung?
9. **Redundanz:** A korreliert explorativ 0.53 mit SMA200. Soll W2-BTC als Gate-Benchmark (statt nur Bericht) dienen?
10. **Mehrfachtest:** Holm über die zwei Forward-Hypothesen bei unterschiedlichen Auswertungszeitpunkten: korrekt umgesetzt?
