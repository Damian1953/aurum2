"""Vollsimulation MTP-Rekonstruktion mit isolierten Varianten. Eingefroren: CMC, Same-Day-Close-Entry, Wilder-ATR(180), Stop lastLeg-6.5ATR, TP leg1+37.5ATR, Exits intraday."""
import re_lib as R, pandas as pd, numpy as np, sys, itertools
C=R.load("cmc_BTCUSD_1d.csv"); T=R.trades(); TRs=R.tr(C)
AW=TRs.ewm(alpha=1/180,adjust=False,min_periods=180).mean().values; SMA=C.close.rolling(200).mean().values
H=C.high.values; CL=C.close.values; LO=C.low.values; OP=C.open.values; idx=C.index
def pivots(nL):
    piv=np.zeros(len(H),bool)
    for i in range(nL,len(H)-1):
        if H[i]>H[i-nL:i].max() and H[i]>H[i+1]: piv[i]=True
    return piv
def run(nL=5, entry_mode="H", leg_mode="C", k=1.5, minage=20, maxage=365, unbroken_by="high", consume="break", start="2015-01-01"):
    """unbroken_by: 'high' = Pivot gilt als gebrochen, sobald ein Hoch darueber lag; 'close' = erst wenn ein Schluss darueber lag.
       consume: 'break' = gebrochene Pivots scheiden aus; 'action' = Pivot scheidet nur aus, wenn darauf ein Einstieg/Leg erfolgte (oder ein Schluss darueber lag)."""
    piv=pivots(nL); i0=idx.get_loc(pd.Timestamp(start)); trades=[]; pos=None; consumed=set()
    src = H if unbroken_by=="high" else CL
    for i in range(i0,len(idx)):
        d=idx[i]
        if pos is not None:
            if LO[i]<=pos["stop"]: pos.update(exit=d,exit_px=min(OP[i],pos["stop"]),reason="SL"); trades.append(pos); pos=None
            elif H[i]>=pos["tp"]: pos.update(exit=d,exit_px=max(OP[i],pos["tp"]),reason="TP"); trades.append(pos); pos=None
            if pos is None: continue
        # Niveau: juengster Pivot j in [i-maxage, i-minage], nicht gebrochen (nach Kriterium) durch Tage j+1..i-1
        L=None; pj=None
        for j in range(i-minage, max(i-maxage-1,-1), -1):
            if not piv[j]: continue
            if consume=="action":
                if j in consumed: continue
                if CL[j+1:i].max() > H[j]: continue   # ein Schluss darueber verbraucht immer
            else:
                if src[j+1:i].max() > H[j]: continue
            L=H[j]; pj=j; break
        if L is None or CL[i]<=SMA[i]: continue
        if pos is None:
            ok = H[i]>L if entry_mode=="H" else CL[i]>L
            if ok: pos=dict(entry=d,legs=[(d,CL[i],L)],stop=CL[i]-6.5*AW[i],tp=CL[i]+37.5*AW[i]); consumed.add(pj)
        else:
            ok = H[i]>L if leg_mode=="H" else CL[i]>L
            if ok and CL[i]>=pos["legs"][-1][1]+k*AW[i]: pos["legs"].append((d,CL[i],L)); pos["stop"]=CL[i]-6.5*AW[i]; consumed.add(pj)
    if pos is not None: pos.update(exit=None,exit_px=None,reason="open"); trades.append(pos)
    return trades
def score(tr):
    S=pd.DataFrame([dict(entry=t["entry"],exit=t["exit"],legs=len(t["legs"]),exit_px=t["exit_px"]) for t in tr])
    hitE=hitX=hitL=hitP=0; detail=[]
    for n,t in T.iterrows():
        m=S[(S.entry-t.entry).abs().dt.days==0]
        if len(m):
            hitE+=1; s=m.iloc[0]
            if s.exit is not None and (s.exit-t.exit).days==0: hitX+=1
            if s.exit is not None and abs(s.exit_px/t.exit_px-1)<0.001: hitP+=1
            if s.legs==t.legs: hitL+=1
    fp=int((~S.entry.apply(lambda e: ((T.entry-e).abs().dt.days<=0).any())).sum())
    return dict(entry=hitE,exit=hitX,px=hitP,legs=hitL,fp=fp,n=len(S))
def table(tr):
    S=pd.DataFrame([dict(entry=t["entry"],exit=t["exit"],legs=len(t["legs"]),exit_px=t["exit_px"],reason=t["reason"],legdays=[str(x[0].date()) for x in t["legs"]]) for t in tr])
    rows=[]
    for n,t in T.iterrows():
        m=S[(S.entry-t.entry).abs().dt.days<=5]
        if len(m)==0: rows.append(f"T{n:2d} {t.entry.date()} legs {t.legs}: KEIN Trade"); continue
        s=m.iloc[0]
        rows.append(f"T{n:2d} {t.entry.date()} legs {t.legs}: sim {s.entry.date()} dE {(s.entry-t.entry).days:+d} dX {(s.exit-t.exit).days if s.exit is not None else 'na'} legs {s.legs} {s.reason} px {100*(s.exit_px/t.exit_px-1):+.2f}% legs {s.legdays}" if s.exit is not None else f"T{n} open")
    extra=S[~S.entry.apply(lambda e: ((T.entry-e).abs().dt.days<=5).any())]
    rows.append("FP: "+", ".join(f"{e.date()}..{x.date() if x is not None else 'open'}" for e,x in zip(extra.entry,extra.exit)))
    return "\n".join(rows)
if __name__=="__main__":
    base=dict(nL=5,entry_mode="H",leg_mode="C",k=1.5,minage=20,unbroken_by="high",consume="break")
    variants={"BASIS (Stufe 1)":{}, "V-C1 Verbrauch nur durch Aktion oder Schluss":dict(consume="action"), "V-C2 gebrochen nur durch Schluss":dict(unbroken_by="close"),
              "Min Age 60":dict(minage=60), "Must Close Above OFF (Legs per Hoch)":dict(leg_mode="H"), "Must Close Above ON auch Entry":dict(entry_mode="C"),
              "V-C2 + Legs per Hoch":dict(unbroken_by="close",leg_mode="H"), "V-C2 + k=0":dict(unbroken_by="close",k=0.0)}
    for name,ov in variants.items():
        tr=run(**{**base,**ov}); s=score(tr)
        print(f"\n=== {name}: Entry {s['entry']}/16 Exit-Tag {s['exit']}/16 Exit-Preis {s['px']}/16 Legs {s['legs']}/16 FP {s['fp']} Trades {s['n']}")
        print(table(tr))
