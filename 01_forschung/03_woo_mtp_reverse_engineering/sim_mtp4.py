import sim_mtp3 as M, numpy as np, pandas as pd, itertools
H=M.H; CL=M.CL; LO=M.LO; OP=M.OP; A=M.A; SMA=M.SMA; idx=M.idx; T=M.T
def pivots_lr(nL,nR=1):
    piv=np.zeros(len(H),bool)
    for i in range(nL,len(H)-nR):
        if H[i]>H[i-nL:i].max() and H[i]>H[i+1:i+nR+1].max(): piv[i]=True
    return piv
def run(nL, entry_mode="H", leg_mode="H", k=0.0, minage=20, maxage=365, start="2015-01-01"):
    piv=pivots_lr(nL); i0=idx.get_loc(pd.Timestamp(start)); trades=[]; pos=None
    for i in range(i0,len(idx)):
        d=idx[i]
        if pos is not None:
            if LO[i]<=pos["stop"]: pos.update(exit=d,exit_px=min(OP[i],pos["stop"]),reason="SL"); trades.append(pos); pos=None
            elif H[i]>=pos["tp"]: pos.update(exit=d,exit_px=max(OP[i],pos["tp"]),reason="TP"); trades.append(pos); pos=None
            if pos is None: continue
        L=M.level(i,piv,minage,maxage)
        if L is None or CL[i]<=SMA[i]: continue
        if pos is None:
            ok = H[i]>L if entry_mode=="H" else CL[i]>L
            if ok: pos=dict(entry=d,legs=[(d,CL[i],L)],stop=CL[i]-6.5*A[i],tp=CL[i]+37.5*A[i])
        else:
            ok = H[i]>L if leg_mode=="H" else CL[i]>L
            if ok and CL[i]>=pos["legs"][-1][1]+k*A[i]: pos["legs"].append((d,CL[i],L)); pos["stop"]=CL[i]-6.5*A[i]
    if pos is not None: pos.update(exit=None,exit_px=None,reason="open"); trades.append(pos)
    return trades
if __name__=="__main__":
    res=[]
    for nL,em,lm,k in itertools.product([2,3,5,8,10],["H","C"],["H","C"],[0.0,1.5]):
        h=M.score(run(nL,em,lm,k)); res.append((nL,em,lm,k)+h)
    df=pd.DataFrame(res,columns=["nL","entry","leg","k","hitE","hitX","hitPx","hitLegs","fp","n"]).sort_values(["hitE","hitX","hitLegs","fp"],ascending=[False,False,False,True])
    print(df.head(15).to_string(index=False))
