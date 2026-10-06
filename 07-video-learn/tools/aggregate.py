import json,glob,os,collections,statistics as st,numpy as np
R='/workspace/video-learn'
out={}
def q(v,p): return round(float(np.percentile(v,p)),2) if len(v) else None
for d in sorted(glob.glob(R+'/*/')):
    fs=sorted(glob.glob(d+'*_analysis.json'))
    if not fs: continue
    ch=os.path.basename(d.rstrip('/'))
    V=[json.load(open(f)) for f in fs]
    shots=[];shots2=[];dur=0;cpm=[];cpm2=[];first=[];lay=collections.Counter();pun=collections.Counter();scales=[];push=0
    wpc=[];ys=[];hs=[];cols=collections.Counter();lufs=[];mus=[];paus=0;hits=0;vids=[];orient=collections.Counter()
    capcl=collections.Counter(); ncap=0; acc_cap=collections.Counter(); acc_all=collections.Counter()
    for a in V:
        band=(0.40*1920,0.90*1920) if a['summary']['h']>a['summary']['w'] else (0.68*1080,0.97*1080)
        for o in a['ocr']:
            for it in o['items']:
                if it.get('color'):
                    for hx,sh in it['color']['clusters']:
                        r0,g0,b0=[int(hx[i:i+2],16) for i in (1,3,5)]
                        if sh>=0.12 and max(r0,g0,b0)-min(r0,g0,b0)>=90 and max(r0,g0,b0)>=140: acc_all['#%02X%02X%02X'%tuple(min(255,int(round(x/24)*24)) for x in (r0,g0,b0))]+=1
                cy=(it['box'][1]+it['box'][3])/2
                if band[0]<=cy<=band[1] and it['h_px']>=40 and it.get('color') and len(it['text'])<=24:
                    ncap+=1
                    for hx,sh in it['color']['clusters']:
                        r0,g0,b0=[int(hx[i:i+2],16) for i in (1,3,5)]
                        if sh>=0.12 and max(r0,g0,b0)-min(r0,g0,b0)>=90 and max(r0,g0,b0)>=140:
                            acc_cap['#%02X%02X%02X'%tuple(min(255,int(round(x/24)*24)) for x in (r0,g0,b0))]+=1
                        if sh>=0.12:
                            r,g,b=[min(255,int(round(int(hx[i:i+2],16)/32)*32)) for i in (1,3,5)]
                            capcl['#%02X%02X%02X'%(r,g,b)]+=1
        s=a['summary'];D=s['duration'];dur+=D
        orient['doc' if s['h']>s['w'] else 'ngang']+=1
        c=[0]+a['cuts03']+[D]; shots+= [c[i+1]-c[i] for i in range(len(c)-1)]
        c2=[0]+a['cuts02']+[D]; shots2+=[c2[i+1]-c2[i] for i in range(len(c2)-1)]
        cpm.append(60*s['cuts_thr0_3']/D); cpm2.append(60*s['cuts_thr0_2']/D)
        if s.get('first_cut_s_thr0_2') is not None: first.append(s['first_cut_s_thr0_2'])
        for k,v in s['layout_pct'].items(): lay[k]+=v*D/100
        for p in a['punches']:
            pun[p['kind']]+=1
            if p['kind'] in('punch_in','punch_out'): scales.append(p['scale'])
        push+=len(a['drifts'])
        for cp in a['captions']:
            if cp['words']<=15 and cp['h']>=26: wpc.append(cp['words']); ys.append(cp['y']); hs.append(cp['h'])
            if cp['color']: cols[cp['color'][:2]+cp['color'][2].upper()+'0'+cp['color'][4].upper()+'0'+cp['color'][6].upper()+'0' if False else cp['color']]+=1
        au=s.get('audio') or {}
        if au:
            if au.get('integrated_lufs') is not None: lufs.append(au['integrated_lufs'])
            mus.append(au.get('music_bed_pct_1s',0)); paus+=len(au['pauses']); hits+=len(au['hit_candidates'])
        vids.append(dict(id=s['id'],dur=round(D,1),cuts03=s['cuts_thr0_3'],cuts02=s['cuts_thr0_2'],med03=s['shot_len_thr0_3']['median'],
             mean03=s['shot_len_thr0_3']['mean'],first=s.get('first_cut_s_thr0_2'),lay=max(s['layout_pct'],key=s['layout_pct'].get) if s['layout_pct'] else None,
             wpc=s['caption_words_median'],lufs=au.get('integrated_lufs'),mus=au.get('music_bed_pct_1s')))
    # coarse colour bins
    def bin_(h):
        r,g,b=int(h[1:3],16),int(h[3:5],16),int(h[5:7],16)
        mx=max(r,g,b);mn=min(r,g,b)
        if mx<60: return 'đen/tối'
        if mn>200: return 'trắng'
        if mx-mn<30: return 'xám'
        if r>180 and g>140 and b<80: return 'vàng/cam vàng'
        if r>180 and g<120 and b<100: return 'đỏ/cam đỏ'
        if g>150 and r<170 and b<120: return 'xanh lá/lime'
        if b>150 and r<120: return 'xanh dương'
        return 'khác'
    cb=collections.Counter()
    for h,n in cols.items(): cb[bin_(h)]+=n
    bins=[0,0.5,1,2,3,5,8,1e9];hist=np.histogram(shots,bins=bins)[0]
    out[ch]=dict(n=len(V),orient=dict(orient),total_s=round(dur,1),
      shot03=dict(n=len(shots),mean=round(float(np.mean(shots)),2),median=q(shots,50),p10=q(shots,10),p25=q(shots,25),p75=q(shots,75),p90=q(shots,90)),
      shot02=dict(mean=round(float(np.mean(shots2)),2),median=q(shots2,50)),
      hist_pct={f'{bins[i]}-{bins[i+1] if bins[i+1]<1e8 else "+"}':round(100*hist[i]/len(shots),1) for i in range(len(hist))},
      cuts_per_min03=round(st.median(cpm),1),cuts_per_min02=round(st.median(cpm2),1),first_cut_median=q(first,50) if first else None,
      layout_pct={k:round(100*v/dur,1) for k,v in lay.most_common()},punches=dict(pun),punch_scale_med=q(scales,50) if scales else None,
      punch_scale_range=[q(scales,10),q(scales,90)] if scales else None,drifts_per_min=round(60*push/dur,2),
      cap_words_med=q(wpc,50) if wpc else None,cap_words_p90=q(wpc,90) if wpc else None,cap_y_med=q(ys,50) if ys else None,cap_y_p10_p90=[q(ys,10),q(ys,90)] if ys else None,
      cap_h_med=q(hs,50) if hs else None,cap_color_bins=dict(cb.most_common(6)),top_hex=cols.most_common(6),
      cap_items=ncap,accent_caption=acc_cap.most_common(6),accent_all_text=acc_all.most_common(6),consistent_colors=[(c,round(100*n/max(1,ncap))) for c,n in capcl.most_common(8)],lufs_med=q(lufs,50) if lufs else None,music_pct_med=q(mus,50) if mus else None,pauses_per_min=round(60*paus/dur,1),hits_per_min=round(60*hits/dur,1),videos=vids)
json.dump(out,open(R+'/aggregate.json','w'),ensure_ascii=False,indent=1)
for ch,o in out.items():
    print(f"\n## {ch} n={o['n']} {o['orient']} tot={o['total_s']}s")
    for k in ['shot03','shot02','hist_pct','cuts_per_min03','cuts_per_min02','first_cut_median','layout_pct','punches','punch_scale_med','punch_scale_range','drifts_per_min','cap_words_med','cap_words_p90','cap_y_med','cap_y_p10_p90','cap_h_med','cap_color_bins','top_hex','cap_items','consistent_colors','accent_caption','accent_all_text','lufs_med','music_pct_med','pauses_per_min','hits_per_min']:
        print(' ',k,o[k])
    for v in o['videos']: print('   ',v)
