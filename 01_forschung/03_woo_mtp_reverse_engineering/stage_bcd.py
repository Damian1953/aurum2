import re_lib as R, pandas as pd, numpy as np, itertools, sys
src=sys.argv[1]; B=R.load(src); T=R.trades(); TRs=R.tr(B)
ATR={"sma":TRs.rolling(180).mean(),"wilder":TRs.ewm(alpha=1/180,adjust=False,min_periods=180).mean()}
pd.set_option("display.width",250)
print(f"=== Quelle {src}: {B.index.min().date()}..{B.index.max().date()}")
# ---- Stage B: exit classification
print("\n-- Stufe B: Exit-Preis gegen Exit-Tagesbar")
for n in range(1,17):
    t=T.loc[n]; d=t.exit
    if d not in B.index: continue
    r=B.loc[d]; pv=B.loc[:d].iloc[-2]
    updown="UP" if r.close>pv.close else "DOWN"
    print(f"T{n:2d} {d.date()} {('WIN ' if t.ret>0 else 'LOSS')} exit {t.exit_px:9.2f} | O {r.open:9.2f} H {r.high:9.2f} L {r.low:9.2f} C {r.close:9.2f} {updown:4s} | in-range {r.low<=t.exit_px<=r.high} | vsC {100*(t.exit_px/r.close-1):+6.2f}% vsO {100*(t.exit_px/r.open-1):+6.2f}%")
# ---- Stage C/D: stop simulation for losses
def sim_stop(t, ref_mode, atr_name, timing, mult=6.5):
    a=ATR[atr_name]; e=t.entry
    if e not in B.index or np.isnan(a.loc[e]): return None
    days=B.loc[e:].index; ref=B.loc[e].close; a0=a.loc[e]; stop=None
    for i,d in enumerate(days):
        r=B.loc[d]
        if i>0 and stop is not None and r.low<=stop:
            return d, stop, min(r.open,stop)
        if ref_mode=="hc": ref=max(ref,r.close)
        elif ref_mode=="hh": ref=max(ref,r.high)
        stop=ref-mult*(a0 if timing=="entry" else a.loc[d])
        if i>900: break
    return None
print("\n-- Stufe C/D: Stop-Simulation Verlusttrades (ref0 = Close am Entry-Tag)")
rows=[]
for n in range(1,17):
    t=T.loc[n]
    if t.ret>0 or t.entry not in B.index: continue
    for ref_mode,atr_name,timing in itertools.product(["fix","hc","hh"],["sma","wilder"],["entry","daily"]):
        s=sim_stop(t,ref_mode,atr_name,timing)
        if s is None: rows.append((n,ref_mode,atr_name,timing,None,None,None)); continue
        d,stop,px=s; rows.append((n,ref_mode,atr_name,timing,(d-t.exit).days,round(100*(stop/t.exit_px-1),2),str(d.date())))
df=pd.DataFrame(rows,columns=["trade","ref","atr","timing","dday","lvl_dev%","pred_exit"])
piv=df.pivot_table(index=["ref","atr","timing"],columns="trade",values="dday",aggfunc="first")
print("Tage Abweichung Exit (0 = Treffer):"); print(piv.to_string())
piv2=df.pivot_table(index=["ref","atr","timing"],columns="trade",values="lvl_dev%",aggfunc="first")
print("\nNiveau-Abweichung % (pred/obs - 1):"); print(piv2.to_string())
df.to_csv(f"stage_d_{src.split('_')[0]}.csv",index=False)
# ---- Stage E: TP check for winners: level = avg_entry + 37.5*ATR; first day high >= level
print("\n-- Stufe E: TP = avgEntry + 37.5*ATR, erster Tag mit High >= Niveau")
for n in range(1,17):
    t=T.loc[n]
    if t.ret<=0 or t.entry not in B.index: continue
    out=[]
    for atr_name,timing in itertools.product(["sma","wilder"],["entry","daily"]):
        a=ATR[atr_name]; days=B.loc[t.entry:].index; hit=None
        for i,d in enumerate(days[1:],1):
            lvl=t.avg_entry+37.5*(a.loc[t.entry] if timing=="entry" else a.loc[days[i-1]])
            if B.loc[d].high>=lvl: hit=(d,lvl); break
            if i>900: break
        out.append(f"{atr_name}/{timing}: " + (f"{(hit[0]-t.exit).days:+d}d lvl {100*(hit[1]/t.exit_px-1):+.2f}%" if hit else "kein Treffer"))
    print(f"T{n:2d} exit {t.exit.date()} @ {t.exit_px:.2f} | " + " | ".join(out))
