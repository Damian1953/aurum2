import re_lib as R, pandas as pd, numpy as np, sys, itertools
C=R.load("cmc_BTCUSD_1d.csv"); T=R.trades(); TRs=R.tr(C)
AW=TRs.ewm(alpha=1/180,adjust=False,min_periods=180).mean(); SMA=C.close.rolling(200).mean().values
H=C.high.values; CL=C.close.values; LO=C.low.values; OP=C.open.values; idx=C.index; A=AW.values
def pivots(n):
    """strict local max of High over +-n days (right side only needs n days after)"""
    piv=np.zeros(len(H),bool)
    for i in range(n,len(H)-n):
        w=H[i-n:i+n+1]
        if H[i]==w.max() and (w==H[i]).sum()==1: piv[i]=True
    return piv
def level(i, piv, minage, maxage):
    M=H[i-minage+1:i].max()
    for j in range(i-minage, max(i-maxage-1,-1), -1):
        if piv[j] and H[j]>M: return H[j]
        # a non-pivot higher high in between breaks the search? no: keep searching for a pivot above M
    return None
def run(n, k, minage=20, maxage=365, start="2015-01-01", pivot_confirm=True):
    piv=pivots(n); i0=idx.get_loc(pd.Timestamp(start)); trades=[]; pos=None
    for i in range(i0,len(idx)):
        d=idx[i]
        if pos is not None:
            if LO[i]<=pos["stop"]: pos.update(exit=d,exit_px=min(OP[i],pos["stop"]),reason="SL"); trades.append(pos); pos=None
            elif H[i]>=pos["tp"]: pos.update(exit=d,exit_px=max(OP[i],pos["tp"]),reason="TP"); trades.append(pos); pos=None
            if pos is None: continue
        L=level(i,piv,minage,maxage)
        if L is None or not (H[i]>L and CL[i]>SMA[i]): continue
        if pos is None: pos=dict(entry=d,legs=[(d,CL[i],L)],stop=CL[i]-6.5*A[i],tp=CL[i]+37.5*A[i])
        elif CL[i]>=pos["legs"][-1][1]+k*A[i]: pos["legs"].append((d,CL[i],L)); pos["stop"]=CL[i]-6.5*A[i]
    if pos is not None: pos.update(exit=None,exit_px=None,reason="open"); trades.append(pos)
    return trades
def score(tr):
    S=pd.DataFrame([dict(entry=t["entry"],exit=t["exit"],legs=len(t["legs"]),exit_px=t["exit_px"]) for t in tr])
    hitE=hitX=hitL=hitP=0
    for _,t in T.iterrows():
        m=S[(S.entry-t.entry).abs().dt.days==0]
        if len(m):
            hitE+=1; s=m.iloc[0]
            if s.exit is not None and (s.exit-t.exit).days==0: hitX+=1
            if s.exit is not None and abs(s.exit_px/t.exit_px-1)<0.001: hitP+=1
            if s.legs==t.legs: hitL+=1
    fp=int((~S.entry.apply(lambda e: ((T.entry-e).abs().dt.days<=0).any())).sum())
    return hitE,hitX,hitP,hitL,fp,len(S)
if __name__=="__main__":
    for n in [1,2,3,5,10]:
        for k in [0.0,1.5]:
            h=score(run(n,k)); print(f"pivot n={n:2d} k={k}: Entry {h[0]}/16 Exit-Tag {h[1]}/16 Exit-Preis {h[2]}/16 Legs {h[3]}/16 | falsche Positive {h[4]} | Trades {h[5]}")
