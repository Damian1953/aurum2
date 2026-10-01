import re_lib as R, pandas as pd, numpy as np
C=R.load("cmc_BTCUSD_1d.csv"); T=R.trades(); TRs=R.tr(C)
AW=TRs.ewm(alpha=1/180,adjust=False,min_periods=180).mean(); SMA=C.close.rolling(200).mean()
def level(i, minage=20, maxage=365):
    M=C.high.iloc[i-minage+1:i].max()
    for j in range(i-minage, max(i-maxage-1,-1), -1):
        if C.high.iloc[j] > M: return C.high.iloc[j], C.index[j]
    return None, None
def signals(a,b):
    out=[]
    for d in C.loc[a:b].index:
        i=C.index.get_loc(d); L,p=level(i)
        if L is not None and C.high.iloc[i]>L: out.append(dict(d=d,close=C.close.iloc[i],high=C.high.iloc[i],level=L,p=p,atr=AW.iloc[i],sma_ok=C.close.iloc[i]>SMA.iloc[i]))
    return out
