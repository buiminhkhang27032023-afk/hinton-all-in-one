#!/usr/bin/env python3
"""Tổng hợp *_script.json theo kênh (chỉ video coverage>=0.6). Ghi script_stats.json + in bảng."""
import json,glob,os,statistics as st
R={}
for p in sorted(glob.glob('/workspace/video-learn/*/*_script.json')):
    d=json.load(open(p)); ch=p.split('/')[-2]
    if 'error' in d or d.get('speech_coverage',0)<0.6: continue
    R.setdefault(ch,[]).append(d)
def med(L,k):
    v=[x[k] for x in L if x.get(k) is not None]; return round(st.median(v),2) if v else None
out={}
print('kênh\tn\tdur\tsps_spk\twps\tstart\thook3w\tfirst_sent_w\tsent_med\tpivot/min\tlist\tcta_end%\tnum/min\taddr/min')
for ch,L in R.items():
    pm=[x['pivots']/(x['duration']/60) for x in L]; nm=[x['numbers']/(x['duration']/60) for x in L]
    o=dict(n=len(L),dur=med(L,'duration'),sps_speaking=med(L,'sps_speaking'),wps=med(L,'wps'),speech_start=med(L,'speech_start'),
           hook3_words=med(L,'hook_0_3s_words'),first_sentence_words=med(L,'first_sentence_words'),sent_words_median=med(L,'sent_words_median'),
           pivots_per_min=round(st.median(pm),2),listing_videos=sum(1 for x in L if x['listing']>0),cta_end_pct=round(100*sum(1 for x in L if x['cta_in_last15']>0)/len(L)),
           numbers_per_min=round(st.median(nm),2),address_per_min=med(L,'address_per_min'),ids=[x['id'] for x in L])
    out[ch]=o
    print(ch,o['n'],o['dur'],o['sps_speaking'],o['wps'],o['speech_start'],o['hook3_words'],o['first_sentence_words'],o['sent_words_median'],o['pivots_per_min'],f"{o['listing_videos']}/{o['n']}",o['cta_end_pct'],o['numbers_per_min'],o['address_per_min'],sep='\t')
json.dump(out,open('/workspace/video-learn/script_stats.json','w'),ensure_ascii=False,indent=1)
