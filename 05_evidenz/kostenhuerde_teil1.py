import math, json

# --- Annahmen ---------------------------------------------------------------
# Kraken Gebuehren je Seite in Prozent, Stand 15.09.2026 (Fee Schedule)
VENUES = {
    "Spot Tier 1 (0 USD/30d), Taker":      dict(fee=0.80, kind="spot"),
    "Spot Tier 1, Maker":                  dict(fee=0.40, kind="spot"),
    "Spot Tier 3 (10k USD/30d), Taker":    dict(fee=0.38, kind="spot"),
    "Spot Tier 5 (50k USD/30d), Maker":    dict(fee=0.15, kind="spot"),
    "Perp Tier 1 (0 USD/30d), Taker":      dict(fee=0.05, kind="perp"),
    "Perp Tier 1, Maker":                  dict(fee=0.02, kind="perp"),
}
# Spread + Slippage je Round Trip in Prozent (Annahme, in Stufe 0 zu messen)
FRICTION = {"spot": 0.04, "perp": 0.04}

DAYS = 365           # Krypto handelt 24/7
VOL_ANN = 0.42       # annualisierte Vola BTC, 30 Tage, Stand Aug 2026
SIGMA_D = VOL_ANN / math.sqrt(DAYS)

HOLD = [1, 3, 5, 10, 21, 55, 90]

def rt(v):
    return 2*v["fee"] + FRICTION[v["kind"]]

print("ANNAHMEN")
print(f"  Taegliche Standardabweichung BTC: {SIGMA_D*100:.2f} %  (aus {VOL_ANN*100:.0f} % annualisiert)")
print(f"  Spread und Slippage je Round Trip: Spot {FRICTION['spot']:.2f} %, Perp {FRICTION['perp']:.2f} %")
print()

print("TABELLE 1 — Kosten je Round Trip in Prozent des Notionals")
print(f"{'Handelsplatz und Ordertyp':<40}{'Gebuehr 2 Seiten':>18}{'Round Trip total':>18}")
for name, v in VENUES.items():
    print(f"{name:<40}{2*v['fee']:>17.2f}%{rt(v):>17.2f}%")
print()

print("TABELLE 2 — Jaehrlicher Kostenaufwand in Prozent des Notionals, bei durchgehender Investition")
hdr = f"{'Handelsplatz und Ordertyp':<40}" + "".join(f"{str(h)+'d':>10}" for h in HOLD)
print(hdr)
for name, v in VENUES.items():
    row = f"{name:<40}"
    for h in HOLD:
        n = DAYS/h
        row += f"{n*rt(v):>9.1f}%"
    print(row)
print()

print("TABELLE 3 — Kosten je Round Trip als Anteil der Bewegung, die im Haltezeitraum stattfindet")
print("  (Round-Trip-Kosten geteilt durch eine Standardabweichung ueber H Tage)")
print(hdr)
for name, v in VENUES.items():
    row = f"{name:<40}"
    for h in HOLD:
        sig = SIGMA_D*math.sqrt(h)*100
        row += f"{rt(v)/sig*100:>9.0f}%"
    print(row)
print()

print("TABELLE 4 — Notwendige Bruttorendite je Trade, damit nach Kosten null uebrig bleibt")
print("  ausgedrueckt in Standardabweichungen des Haltezeitraums")
print(hdr)
for name, v in VENUES.items():
    row = f"{name:<40}"
    for h in HOLD:
        sig = SIGMA_D*math.sqrt(h)
        row += f"{rt(v)/100/sig:>9.2f}"
    print(row)
