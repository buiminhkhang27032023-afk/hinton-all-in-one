#!/usr/bin/env python3
"""Footage/B-roll insert stats per video from <id>_analysis.json (+ transcript for script position).
Usage: footage_stats.py <dir>... -> prints table, writes footage_stats.json in /workspace/video-learn.
'Footage' = any layout where inserted material (B-roll/UI/card/screenshot) occupies >= half the frame:
split_mat_duoi, split_mat_tren, split_khong_mat, pip_mat, man_hinh_ui, broll, card_toi. Face-only: mat_can, mat_trung. [KHUNG] heuristic."""
import json,glob,os,sys,statistics as st
R='/workspace/video-learn'
FOOT={'split_mat_duoi','split_mat_tren','split_khong_mat','pip_mat','man_hinh_ui','broll','card_toi'}
FULL={'man_hinh_ui','broll','card_toi','split_khong_mat'}   # footage fills whole frame (no face)
out={}
for d in sys.argv[1:]:
    rows=[]
    for f in sorted(glob.glob(f'{R}/{d}/*_analysis.json')):
        a=json.load(open(f)); s=a['summary']; D=s['duration']; L=a['layout']
        if not L: continue
        lab=lambda t: min(L,key=lambda x:abs(x['t']-t))['lab']
        def pct(t0,t1,S=FOOT):
            xs=[x for x in L if t0<=x['t']<t1]; return round(100*sum(x['lab'] in S for x in xs)/len(xs)) if xs else None
        first=next((x['t'] for x in L if x['lab'] in FOOT),None)
        # insert shots: shots (thr0.2) whose midpoint label is footage
        b=[0]+a['cuts02']+[D]; sh=[(b[i],b[i+1]) for i in range(len(b)-1) if b[i+1]-b[i]>0.1]
        ins=[e-s0 for s0,e in sh if lab((s0+e)/2) in FOOT]
        insf=[e-s0 for s0,e in sh if lab((s0+e)/2) in FULL]
        r=dict(id=s['id'],dur=D,foot_pct=pct(0,D+1),full_pct=pct(0,D+1,FULL),first_foot=first,
               hook_0_3=pct(0,3),early_3_15=pct(3,15),mid=pct(15,D*0.85),end_15=pct(D*0.85,D+1),
               n_insert_shots=len(ins),inserts_per_min=round(len(ins)/(D/60),1),insert_med=round(st.median(ins),2) if ins else None,
               full_insert_med=round(st.median(insf),2) if insf else None, layout_pct=s['layout_pct'])
        rows.append(r)
    out[d]=rows
    if rows:
        med=lambda k:round(st.median([r[k] for r in rows if r[k] is not None]),1) if any(r[k] is not None for r in rows) else None
        print(f"{d:32s} n={len(rows)} foot%={med('foot_pct')} full%={med('full_pct')} first={med('first_foot')}s hook={med('hook_0_3')} 3-15s={med('early_3_15')} mid={med('mid')} end={med('end_15')} ins/min={med('inserts_per_min')} ins_med={med('insert_med')}s full_ins_med={med('full_insert_med')}s")
p=f'{R}/footage_stats.json'
old=json.load(open(p)) if os.path.exists(p) else {}
old.update(out); json.dump(old,open(p,'w'),indent=1)
