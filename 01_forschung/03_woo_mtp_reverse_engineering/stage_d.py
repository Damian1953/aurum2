import re_lib as R, pandas as pd, numpy as np, itertools, sys
src = sys.argv[1] if len(sys.argv)>1 else "binance_BTCUSDT_1d.csv"
B=R.load(src); T=R.trades(); TRs=R.tr(B)
ATR={"sma":TRs.rolling(180).mean(),"wilder":TRs.ewm(alpha=1/180,adjust=False,min_periods=180).mean(),"ema":TRs.ewm(span=180,adjust=False,min_periods=180).mean()}
def sim(t, ref_mode, atr_name, timing, mult=6.5):
    a=ATR[atr_name]; e=t.entry
    if e not in B.index or np.isnan(a.loc[e]): return None
    days=B.loc[e:].index
    ref=t.avg_entry; a0=a.loc[e]; stop=None
    for i,d in enumerate(days):
        r=B.loc[d]
        if i>0 and stop is not None:
            if r.low<=stop:
                px = min(r.open, stop)  # Gap: Ausfuehrung am Open, sonst am Niveau
                return d, stop, px
        # update ref after the day's close
        if ref_mode=="hc": ref=max(ref, r.close)
        elif ref_mode=="hh": ref=max(ref, r.high)
        elif ref_mode=="fix": pass
        at = a0 if timing=="entry" else a.loc[d]
        stop=ref-mult*at
        if i>800: break
    return None
rows=[]
for n in range(6,17):
    t=T.loc[n]
    if t.ret>0: continue
    for ref_mode,atr_name,timing in itertools.product(["fix","hc","hh"],["sma","wilder","ema"],["entry","daily"]):
        s=sim(t,ref_mode,atr_name,timing)
        if s is None: rows.append((n,ref_mode,atr_name,timing,None,None,None,None)); continue
        d,stop,px=s
        rows.append((n,ref_mode,atr_name,timing,(d-t.exit).days,round(100*(stop/t.exit_px-1),2),round(100*(px/t.exit_px-1),2),str(d.date())))
df=pd.DataFrame(rows,columns=["trade","ref","atr","timing","dday","lvl_dev%","px_dev%","pred_exit"])
pd.set_option("display.width",200); pd.set_option("display.max_rows",500)
for n,g in df.groupby("trade"):
    t=T.loc[n]; print(f"\n=== T{n} legs {t.legs} entry {t.entry.date()} exit {t.exit.date()} exit_px {t.exit_px:.2f} ret {100*t.ret:+.1f}%")
    print(g.drop(columns="trade").to_string(index=False))
df.to_csv("stage_d_loss_trades.csv",index=False)
