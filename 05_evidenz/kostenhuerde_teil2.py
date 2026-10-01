import math
DAYS=365; VOL_ANN=0.42; SIGMA_D=VOL_ANN/math.sqrt(DAYS)
V={"Spot T1 Taker":1.64,"Spot T1 Maker":0.84,"Spot T5 Maker":0.34,"Perp T1 Taker":0.14,"Perp T1 Maker":0.08}
HOLD=[1,3,5,10,21,55,90]

print("TABELLE 5 — Volatilitaetsgesteuertes Portfolio, Zielvolatilitaet 20 Prozent")
print("  Kosten und Nettoergebnis in Prozent des EIGENKAPITALS, nicht des Notionals")
print("  Annahme Bruttoergebnis: Sharpe 1.5 vor Kosten, also 30 Prozent brutto pro Jahr")
TARGET=0.20; ASSET=VOL_ANN; LEV=TARGET/ASSET; GROSS=1.5*TARGET*100
print(f"  Notional je Eigenkapital: {LEV:.2f}   Bruttoertrag: {GROSS:.0f} % p.a.")
print()
hdr=f"{'Handelsplatz':<18}"+"".join(f"{str(h)+'d':>12}" for h in HOLD)
print(hdr)
for n,rt in V.items():
    row=f"{n:<18}"
    for h in HOLD:
        cost=(DAYS/h)*rt*LEV
        row+=f"{GROSS-cost:>11.0f}%"
    print(row)
print("  (Werte = Nettoergebnis pro Jahr. Negative Zahl bedeutet: Strategie verliert nur durch Kosten.)")
print()

print("TABELLE 6 — Notwendige Trefferquote, damit ein Trade nach Kosten Erwartungswert null hat")
print("  Annahme: Stopp bei einer Standardabweichung des Haltezeitraums, Chance-Risiko-Verhaeltnis 1.5")
R=1.5
print(hdr)
for n,rt in V.items():
    row=f"{n:<18}"
    for h in HOLD:
        L=SIGMA_D*math.sqrt(h)*100
        p=(1+rt/L)/(1+R)
        row+=f"{p*100:>11.0f}%"
    print(row)
print("  (Ohne Kosten waere die Schwelle 40 Prozent. Werte ueber 60 Prozent gelten als unrealistisch.)")
print()

print("TABELLE 7 — Erreichbare Gebuehrenstufe bei kleinem Konto, Spot")
print("  30-Tage-Volumen = Eigenkapital mal Round Trips pro Monat mal 2 Seiten")
tiers=[(0,"T1 0.40/0.80"),(2500,"T2 0.30/0.60"),(10000,"T3 0.22/0.38"),(25000,"T4 0.20/0.35"),(50000,"T5 0.15/0.30"),(100000,"T6 0.12/0.25")]
def tier(v):
    out=tiers[0][1]
    for lim,name in tiers:
        if v>=lim: out=name
    return out
print(f"{'Eigenkapital':<14}"+"".join(f"{str(h)+'d Halte':>16}" for h in [5,10,21,55]))
for A in [5000,10000,25000,50000]:
    row=f"{A:>9,} USD "
    for h in [5,10,21,55]:
        vol30=A*(30/h)*2
        row+=f"{tier(vol30):>16}"
    print(row)
print()
print("TABELLE 8 — Perpetuals, gleiche Rechnung")
ptiers=[(0,"T1 0.02/0.05"),(5_000_000,"T2 0.0175/0.045"),(10_000_000,"T3 0.015/0.04")]
def ptier(v):
    out=ptiers[0][1]
    for lim,name in ptiers:
        if v>=lim: out=name
    return out
print(f"{'Eigenkapital':<14}"+"".join(f"{str(h)+'d Halte':>18}" for h in [5,10,21,55]))
for A in [5000,10000,25000,50000]:
    row=f"{A:>9,} USD "
    for h in [5,10,21,55]:
        vol30=A*LEV*(30/h)*2
        row+=f"{ptier(vol30):>18}"
    print(row)
