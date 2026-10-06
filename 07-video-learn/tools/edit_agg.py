#!/usr/bin/env python3
"""Trung vị chỉ số dựng theo kênh từ *_analysis.json. Usage: edit_agg.py dir..."""
import json,glob,sys,statistics as st
def med(v): v=[x for x in v if x is not None]; return round(st.median(v),2) if v else None
print('kênh|n|dài s|cắt/phút(0.3)|shot med s(0.3)|cắt đầu s|chữ/cụm|y caption|cao chữ px|punch|push-in/video|LUFS|giọng dBFS|BGM %|mặt %')
for d in sys.argv[1:]:
    S=[json.load(open(f))['summary'] for f in sorted(glob.glob(f'/workspace/video-learn/{d}/*_analysis.json'))]
    if not S: continue
    face=[sum(v for k,v in s['layout_pct'].items() if k in('mat_can','mat_trung','split_mat_duoi','split_mat_tren','pip_mat')) for s in S]
    row=[d,len(S),med([s['duration'] for s in S]),med([s['cuts_thr0_3']/s['duration']*60 for s in S]),med([s['shot_len_thr0_3']['median'] for s in S]),
         med([s['first_cut_s'] for s in S]),med([s.get('caption_words_median') for s in S]),med([s.get('caption_y_median') for s in S]),med([s.get('caption_h_median') for s in S]),
         med([s['punches'].get('punch_in',0) for s in S]),med([s.get('pushins') for s in S]),med([s['audio'].get('integrated_lufs') for s in S]),
         med([s['audio'].get('voice_level_dbfs') for s in S]),med([s['audio'].get('music_bed_pct_1s') for s in S]),med(face)]
    print('|'.join(map(str,row)))
