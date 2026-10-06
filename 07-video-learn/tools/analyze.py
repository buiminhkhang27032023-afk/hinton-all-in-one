#!/usr/bin/env python3
"""Per-video measurement + breakdown. Usage: analyze.py <mp4> [--no-ocr]
Writes <id>_analysis.json and <id>_breakdown.md next to the mp4.
Labels: [ĐO] measured by ffmpeg/opencv, [KHUNG] auto-classified from frames (heuristic), [SUY] inferred."""
import sys, os, json, subprocess, re, statistics as st, math, time
import numpy as np, cv2
cv2.setNumThreads(1)
os.environ.setdefault('OMP_NUM_THREADS','3')
f=sys.argv[1]; NO_OCR='--no-ocr' in sys.argv
d=os.path.dirname(f); vid=os.path.basename(f)[:-4]
tmp=f'/tmp/an_{vid}'; os.makedirs(tmp,exist_ok=True)

def run(cmd): return subprocess.run(cmd,shell=True,capture_output=True,text=True)
pr=json.loads(run(f'ffprobe -v error -show_streams -show_format -of json "{f}"').stdout)
vs=[s for s in pr['streams'] if s['codec_type']=='video'][0]
W,H=int(vs['width']),int(vs['height']); DUR=float(pr['format']['duration'])
num,den=vs.get('avg_frame_rate','30/1').split('/'); FPS=float(num)/float(den or 1)
HAS_A=any(s['codec_type']=='audio' for s in pr['streams'])
VERT=H>=W
RW,RH=(1080,1920) if VERT else (1920,1080)   # reference canvas for px numbers

# ---------- 1. scene scores (all frames) ----------
run(f'ffmpeg -v error -i "{f}" -an -vf "scale=192:-2,select=\'gte(scene,0)\',metadata=print:file={tmp}/sc.txt" -f null -')
times=[];scores=[]
cur=None
for line in open(f'{tmp}/sc.txt'):
    m=re.search(r'pts_time:([0-9.]+)',line)
    if m: cur=float(m.group(1)); continue
    m=re.search(r'scene_score=([0-9.]+)',line)
    if m and cur is not None: times.append(cur); scores.append(float(m.group(1)))
times=np.array(times); scores=np.array(scores)
def cuts_at(th, mingap=0.2):
    c=[];last=-9
    for t,s in zip(times,scores):
        if s>=th and t-last>=mingap and t>0.05: c.append(round(float(t),3)); last=t
    return c
C02=cuts_at(0.2); C03=cuts_at(0.3)
# low-threshold candidates (jump cuts on static talking head): local spikes
cand=[]
for i in range(2,len(scores)-2):
    s=scores[i]
    if 0.06<=s<0.2 and s>4*max(np.median(scores[max(0,i-8):i]),0.01) and s>3*max(scores[i-1],scores[i+1]):
        cand.append(round(float(times[i]),3))
# gradual transitions: >=4 consecutive frames with score 0.04-0.2 and brightness change handled below
def shots_from(c):
    b=[0.0]+c+[DUR]; return [(b[i],b[i+1]) for i in range(len(b)-1) if b[i+1]-b[i]>0.05]
SH=shots_from(C03)
def stats_len(sh):
    L=[e-s for s,e in sh]; 
    return dict(n=len(L),mean=round(st.mean(L),2),median=round(st.median(L),2),p10=round(float(np.percentile(L,10)),2),p90=round(float(np.percentile(L,90)),2),max=round(max(L),2)) if L else {}

# ---------- 2. audio ----------
A={}
if HAS_A:
    run(f'ffmpeg -v error -i "{f}" -vn -af "aresample=16000,asetnsamples=800,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file={tmp}/rms.txt" -f null -')
    at=[];ar=[];cur=None
    for line in open(f'{tmp}/rms.txt'):
        m=re.search(r'pts_time:([0-9.]+)',line)
        if m: cur=float(m.group(1)); continue
        m=re.search(r'RMS_level=(-?[0-9.]+|-inf)',line)
        if m and cur is not None: at.append(cur); ar.append(-90.0 if 'inf' in m.group(1) else max(-90.0,float(m.group(1))))
    at=np.array(at); ar=np.array(ar)
    voiced=ar[ar>np.percentile(ar,30)] if len(ar) else ar
    L=float(np.median(voiced)) if len(voiced) else -30
    # pauses: rms < L-15 for >=0.25s
    pauses=[];s0=None
    for t,r in zip(at,ar):
        if r<L-15:
            if s0 is None: s0=t
        else:
            if s0 is not None and t-s0>=0.25: pauses.append((round(float(s0),2),round(float(t),2)))
            s0=None
    # sfx/hit candidates: jump over local median while not coming from a pause
    hits=[]
    for i in range(10,len(ar)):
        prev=np.median(ar[i-10:i])
        if ar[i]-prev>=8 and ar[i]>L-4 and prev>L-14:
            t=float(at[i])
            if not hits or t-hits[-1]>0.4: hits.append(round(t,2))
    p5=float(np.percentile(ar,5)) if len(ar) else -90
    loud=[ (round(float(t),1), round(float(r),1)) for t,r in zip(at[::10],ar[::10])]  # 0.5s samples
    # 1s windows: min RMS > L-22 -> continuous bed (music likely)
    win=[]
    for k in range(int(at[-1])+1 if len(at) else 0):
        sel=ar[(at>=k)&(at<k+1)]
        if len(sel)>=10: win.append((k, bool(sel.min()>L-22)))
    music_pct=round(100*sum(1 for _,b in win if b)/max(1,len(win)),1)
    A=dict(voice_level_dbfs=round(L,1),floor_p5_dbfs=round(p5,1),pauses=pauses,hit_candidates=hits,
           music_bed_inferred= bool(p5> L-20), music_bed_pct_1s=music_pct, music_win=win, curve_0p5s=loud)
    run(f'ffmpeg -nostats -hide_banner -i "{f}" -vn -af ebur128 -f null - 2> {tmp}/ebu.txt')
    try:
        txt=open(f'{tmp}/ebu.txt').read(); I=re.findall(r'I:\s+(-?[0-9.]+) LUFS',txt); LRA=re.findall(r'LRA:\s+([0-9.]+) LU',txt)
        A['integrated_lufs']=float(I[-1]) if I else None; A['lra']=float(LRA[-1]) if LRA else None
    except Exception: pass

# ---------- 3. frames: layout (2fps) ----------
cas=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
FW=540 if VERT else 640; FH=int(round(H*FW/W/2)*2)
def frames(fps,w,h,gray=False):
    pix='gray' if gray else 'bgr24'; ch=1 if gray else 3
    p=subprocess.Popen(f'ffmpeg -v error -i "{f}" -vf "fps={fps},scale={w}:{h}" -f rawvideo -pix_fmt {pix} -',shell=True,stdout=subprocess.PIPE)
    n=w*h*ch; i=0
    while True:
        b=p.stdout.read(n)
        if len(b)<n: break
        a=np.frombuffer(b,np.uint8).reshape((h,w) if gray else (h,w,3)); yield i/fps, a; i+=1
    p.wait()
def seam_y(g):
    h,w=g.shape; best=None
    dif=np.abs(np.diff(g.astype(np.int16),axis=0))
    for y in range(int(h*0.25),int(h*0.75)):
        frac=(dif[y]>18).mean()
        if frac>0.55 and (best is None or frac>best[1]): best=(y,frac)
    return best[0] if best else None
LAY=[]
for t,img in frames(2,FW,FH):
    g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); h,w=g.shape
    faces=cas.detectMultiScale(g,1.1,6,minSize=(int(w*0.06),int(w*0.06)))
    face=None
    if len(faces): face=max(faces,key=lambda r:r[2]*r[3]); face=[int(v) for v in face]
    sy=seam_y(g)
    edges=cv2.Canny(g,80,160); ed=float((edges>0).mean()); br=float(g.mean())
    fw=face[2]/w if face else 0; fcy=(face[1]+face[3]/2)/h if face else 0; fcx=(face[0]+face[2]/2)/w if face else 0
    if face and sy and abs(fcy*h-sy)>face[3]*0.6:
        lab='split_mat_duoi' if fcy*h>sy else 'split_mat_tren'
    elif face and fcy>0.58 and face[1]/h>0.45 and fw<0.45 and VERT:
        lab='split_mat_duoi'
    elif face and fw<0.13 and (fcx<0.3 or fcx>0.7) and (fcy<0.3 or fcy>0.7):
        lab='pip_mat'
    elif face and fw>=0.2: lab='mat_can'          # close face / full face
    elif face: lab='mat_trung'                    # medium shot face
    elif sy: lab='split_khong_mat'
    elif br<60 and ed<0.05: lab='card_toi'
    elif ed>0.07 or br>150: lab='man_hinh_ui'
    else: lab='broll'
    sc=lambda v,ref,base: int(round(v*ref/base))
    LAY.append(dict(t=round(t,2),lab=lab,seam_y=sc(sy,RH,h) if sy else None,
        face=[sc(face[0],RW,w),sc(face[1],RH,h),sc(face[2],RW,w),sc(face[3],RH,h)] if face else None,
        edge=round(ed,3),bright=round(br,1)))

# ---------- 4. motion / zoom (10fps gray) ----------
orb=cv2.ORB_create(600); bf=cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
MW=270 if VERT else 384; MH=int(round(H*MW/W/2)*2)
def affine(a,b):
    k1,d1=orb.detectAndCompute(a,None); k2,d2=orb.detectAndCompute(b,None)
    if d1 is None or d2 is None or len(k1)<15 or len(k2)<15: return None
    m=bf.match(d1,d2)
    if len(m)<15: return None
    p1=np.float32([k1[x.queryIdx].pt for x in m]); p2=np.float32([k2[x.trainIdx].pt for x in m])
    M,inl=cv2.estimateAffinePartial2D(p1,p2,method=cv2.RANSAC,ransacReprojThreshold=2.5)
    if M is None: return None
    ni=int(inl.sum()); s=math.hypot(M[0,0],M[1,0])
    return s,ni,float(M[0,2]),float(M[1,2])
MOT=[];prev=None;pt=None
for t,g in frames(10,MW,MH,gray=True):
    if prev is not None:
        r=affine(prev,g)
        MOT.append((round(pt,2),round(t,2),r))
    prev=g;pt=t
cutset=sorted(set(C03))
def near_cut(t0,t1): return any(t0-0.001<=c<=t1+0.05 for c in cutset)
# punch at cuts (scale between frame before and after cut)
punches=[]
for (t0,t1,r) in MOT:
    if near_cut(t0,t1) and r and r[1]>=25:
        s=r[0]
        if abs(s-1)>=0.06: punches.append(dict(t=t1,scale=round(s,3),kind='punch_in' if s>1 else 'punch_out',inliers=r[1]))
        elif abs(s-1)<0.03: punches.append(dict(t=t1,scale=round(s,3),kind='jump_cut_cung_khung',inliers=r[1]))
# also low-threshold candidate cuts as jump cuts
for c in cand:
    for (t0,t1,r) in MOT:
        if t0<=c<=t1+0.05 and r and r[1]>=25:
            s=r[0]; punches.append(dict(t=t1,scale=round(s,3),kind=('punch_in' if s>1.06 else 'punch_out' if s<0.94 else 'jump_cut_cung_khung'),inliers=r[1],lowthr=True)); break
# push-in drift per shot
drifts=[]
for s0,e0 in SH:
    cum=1.0;n=0;ok=0
    for (t0,t1,r) in MOT:
        if t0>=s0+0.05 and t1<=e0-0.05:
            n+=1
            if r and r[1]>=20 and abs(r[0]-1)<0.05: cum*=r[0]; ok+=1
    dur=e0-s0
    if ok>=8 and dur>=1.0 and abs(cum-1)>=0.03:
        drifts.append(dict(start=round(s0,2),end=round(e0,2),total_pct=round((cum-1)*100,1),pct_per_s=round((cum-1)*100/dur,2),kind='push_in' if cum>1 else 'pull_out'))

# ---------- 5. OCR (1fps) ----------
OCR=[]
if not NO_OCR:
    import onnxruntime as _ort
    _SO=_ort.SessionOptions
    def _so():
        o=_SO(); o.intra_op_num_threads=int(os.environ.get('ORT_THREADS','2')); o.inter_op_num_threads=1; return o
    _ort.SessionOptions=_so
    from rapidocr_onnxruntime import RapidOCR
    eng=RapidOCR()
    def color_of(img,box):
        x0,y0,x1,y1=box; crop=img[max(0,y0):y1,max(0,x0):x1]
        if crop.size<30: return None
        Z=crop.reshape(-1,3).astype(np.float32)
        K=3 if len(Z)>=30 else 1
        _,lab,cent=cv2.kmeans(Z,K,None,(cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,10,1.0),2,cv2.KMEANS_PP_CENTERS)
        cnt=np.bincount(lab.flatten(),minlength=K); order=np.argsort(-cnt)
        cl=[(cent[i][::-1],cnt[i]/cnt.sum()) for i in order]   # rgb
        hx=lambda c:'#%02X%02X%02X'%tuple(int(v) for v in c)
        bg=cl[0][0]
        def sat_lum(c):
            mx,mn=max(c),min(c); return (mx-mn)+0.5*mx
        cands=[c for c in cl[1:] if c[1]>=0.12] or cl[1:] or cl
        fill=max(cands,key=lambda c: np.linalg.norm(c[0]-bg)+0.3*sat_lum(c[0]))
        return dict(fill_guess=hx(fill[0]),clusters=[(hx(c),round(float(p),2)) for c,p in cl])
    prev_small=None; prev_res=None
    for t,img in frames(1,FW,FH):
        small=cv2.resize(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY),(60,int(60*FH/FW)))
        if prev_small is not None and np.abs(small.astype(int)-prev_small).mean()<1.5 and prev_res is not None:
            res=prev_res
        else:
            out,_=eng(img); res=[]
            for box,txt,sc in (out or []):
                if float(sc)<0.6 or not txt.strip(): continue
                xs=[p[0] for p in box]; ys=[p[1] for p in box]
                b=[int(min(xs)),int(min(ys)),int(max(xs)),int(max(ys))]
                res.append(dict(text=txt.strip(),box=[int(b[0]*RW/FW),int(b[1]*RH/FH),int(b[2]*RW/FW),int(b[3]*RH/FH)],
                                h_px=int((b[3]-b[1])*RH/FH),score=round(float(sc),2),color=color_of(img,b)))
        prev_small=small; prev_res=res
        OCR.append(dict(t=float(t),items=res))
# classify text: persistent (same text >=3 consecutive samples) = title/UI; caption band
def is_cjk(s): return any('\u4e00'<=ch<='\u9fff' for ch in s)
def wc(s): return len([c for c in s if '\u4e00'<=c<='\u9fff']) if is_cjk(s) else len(s.split())
seen={}
for i,o in enumerate(OCR):
    for it in o['items']: seen.setdefault(it['text'],[]).append(i)
def persistent(txt):
    idx=seen.get(txt,[]); 
    if len(idx)<3: return False
    run_=1;best=1
    for a,b in zip(idx,idx[1:]):
        run_=run_+1 if b==a+1 else 1; best=max(best,run_)
    return best>=3
band=(0.40,0.88) if VERT else (0.70,0.97)
caps=[]   # (t,text,ybox,h,color)
for o in OCR:
    cs=[it for it in o['items'] if band[0]*RH<= (it['box'][1]+it['box'][3])/2 <=band[1]*RH and it['h_px']>=(26 if VERT else 22) and not persistent(it['text'])]
    if cs:
        cs=sorted(cs,key=lambda it:it['box'][1])
        caps.append(dict(t=o['t'],text=' / '.join(it['text'] for it in cs),y=cs[0]['box'][1],y2=cs[-1]['box'][3],h=int(np.median([it['h_px'] for it in cs])),
                         color=cs[0]['color']['fill_guess'] if cs[0]['color'] else None,words=sum(wc(it['text']) for it in cs)))
chunks=[];last=None
for c in caps:
    if c['text']!=last: chunks.append(c); last=c['text']
titles=[]
for txt,idx in seen.items():
    if persistent(txt) and len(txt)>=3:
        it=[x for x in OCR[idx[0]]['items'] if x['text']==txt][0]
        titles.append(dict(text=txt,t0=OCR[idx[0]]['t'],t1=OCR[idx[-1]]['t'],box=it['box'],h=it['h_px'],color=it['color']['fill_guess'] if it['color'] else None))

# ---------- 6. hook OCR (0-3s @4fps) ----------
HOOK=[]
if not NO_OCR:
    for t,img in frames(4,FW,FH):
        if t>=3: break
        if int(t*4)%2: continue   # every 0.5s
        out,_=eng(img)
        HOOK.append(dict(t=t,text=[x[1] for x in (out or []) if float(x[2])>0.6][:8]))

# ---------- 7. aggregate ----------
from collections import Counter
labc=Counter(x['lab'] for x in LAY); tot=sum(labc.values()) or 1
layout_pct={k:round(100*v/tot,1) for k,v in labc.most_common()}
seams=[x['seam_y'] for x in LAY if x['lab'].startswith('split') and x['seam_y']]
facebox=[x['face'] for x in LAY if x['face']]
summary=dict(id=vid,folder=os.path.basename(d),duration=round(DUR,2),w=W,h=H,fps=round(FPS,2),
    cuts_thr0_2=len(C02),cuts_thr0_3=len(C03),cut_candidates_lowthr=len(cand),
    shot_len_thr0_3=stats_len(SH),shot_len_thr0_2=stats_len(shots_from(C02)),
    first_cut_s=C03[0] if C03 else None,first_cut_s_thr0_2=C02[0] if C02 else None,
    layout_pct=layout_pct,seam_y_median=int(np.median(seams)) if seams else None,
    face_box_median=[int(np.median([b[i] for b in facebox])) for i in range(4)] if facebox else None,
    punches=dict(Counter(p['kind'] for p in punches)),punch_scale_median=round(float(np.median([p['scale'] for p in punches if p['kind']=='punch_in'])),3) if any(p['kind']=='punch_in' for p in punches) else None,
    pushins=len([x for x in drifts if x['kind']=='push_in']),
    caption_chunks=len(chunks),caption_words_median=st.median([c['words'] for c in chunks]) if chunks else None,
    caption_y_median=int(np.median([c['y'] for c in chunks])) if chunks else None,caption_h_median=int(np.median([c['h'] for c in chunks])) if chunks else None,
    caption_colors=Counter(c['color'] for c in chunks if c['color']).most_common(4),
    audio={k:v for k,v in A.items() if k!='curve_0p5s'} if A else None)
J=dict(summary=summary,cuts03=C03,cuts02=C02,cand=cand,layout=LAY,punches=punches,drifts=drifts,captions=chunks,titles=titles,hook_ocr=HOOK,audio=A,ocr=OCR)
json.dump(J,open(f'{d}/{vid}_analysis.json','w'),ensure_ascii=False)

# ---------- 8. breakdown.md ----------
def rows():
    R=[]
    for s0,e0 in SH:
        t=s0
        while t<e0-0.05:
            e=min(e0,t+3.0) if e0-t>4.0 else e0
            R.append((t,e,t==s0)); t=e
    return R
def labs_in(s,e):
    c=Counter(x['lab'] for x in LAY if s<=x['t']<e) or Counter(min(LAY,key=lambda x:abs(x['t']-s))['lab'] for _ in [0]) if LAY else Counter()
    return c
NAMES=dict(split_mat_duoi='SPLIT (trên: B-roll/UI, dưới: mặt)',split_mat_tren='SPLIT (trên: mặt, dưới: B-roll)',split_khong_mat='SPLIT/2 khung không mặt',
    pip_mat='PIP mặt góc trên nền màn hình/B-roll',mat_can='MẶT CẬN/full face',mat_trung='MẶT TRUNG CẢNH',card_toi='CARD nền tối',man_hinh_ui='MÀN HÌNH/UI sáng',broll='B-ROLL/full khác')
md=[f'# Breakdown {vid} ({os.path.basename(d)})','',
 f'File: `{f}` · {W}×{H} · {FPS:.2f} fps · {DUR:.1f}s · px quy về khung {RW}×{RH}.','',
 'Nhãn: **[ĐO]** đo bằng ffmpeg/OpenCV · **[KHUNG]** phân loại tự động từ frame (heuristic, có thể sai) · **[SUY]** suy luận. Bản tự động; xem thêm contact sheet `'+vid+'_sheet.jpg` và hook `'+vid+'_hook.jpg`.','',
 '## Chỉ số tổng','',
 f'- [ĐO] Số cắt: {len(C03)} (ngưỡng scene 0,3) · {len(C02)} (ngưỡng 0,2) · ứng viên jump-cut ngưỡng thấp: {len(cand)}',
 f'- [ĐO] Độ dài shot (ngưỡng 0,3): {summary["shot_len_thr0_3"]}',
 f'- [ĐO] Độ dài shot (ngưỡng 0,2): {summary["shot_len_thr0_2"]}',
 f'- [ĐO] Cắt đầu tiên: {summary["first_cut_s"]}s (0,3) · {summary["first_cut_s_thr0_2"]}s (0,2)',
 f'- [KHUNG] % thời gian theo bố cục: '+', '.join(f'{NAMES.get(k,k)} {v}%' for k,v in layout_pct.items()),
 f'- [KHUNG] Đường chia split (y trung vị): {summary["seam_y_median"]} px · hộp mặt trung vị [x,y,w,h]: {summary["face_box_median"]}',
 f'- [ĐO] Zoom tại điểm cắt: {summary["punches"]} · tỉ lệ punch-in trung vị: {summary["punch_scale_median"]} · số đoạn push-in chậm: {summary["pushins"]}',
 f'- [ĐO/OCR] Caption: {len(chunks)} cụm (mẫu 1 fps, sẽ hụt cụm <1s) · số chữ/cụm trung vị: {summary["caption_words_median"]} (tiếng Trung = số ký tự) · y trung vị: {summary["caption_y_median"]} px · cao chữ trung vị: {summary["caption_h_median"]} px · màu fill ước tính: {summary["caption_colors"]}',
]
if A: md.append(f'- [ĐO] Âm thanh: giọng ~{A["voice_level_dbfs"]} dBFS RMS · sàn P5 {A["floor_p5_dbfs"]} dBFS · LUFS tích hợp {A.get("integrated_lufs")} · LRA {A.get("lra")} · {len(A["pauses"])} khoảng ngừng ≥0,25s · {len(A["hit_candidates"])} đỉnh nghi sfx · [SUY] nhạc nền: {"có khả năng" if A["music_bed_inferred"] else "ít khả năng/không rõ"} ({A["music_bed_pct_1s"]}% cửa sổ 1s có nền liên tục)')
md+=['','## Hook 0–3s','']
hook_l=[x['lab'] for x in LAY if x['t']<3]
md.append(f'- [KHUNG] Bố cục 0–3s: {", ".join(NAMES.get(k,k) for k,_ in Counter(hook_l).most_common())}')
md.append(f'- [ĐO] Cắt trong 0–3s: {[c for c in C02 if c<3]} (0,2)')
if A: md.append(f'- [ĐO] Đỉnh âm 0–3s: {[h for h in A["hit_candidates"] if h<3]} · ngừng giọng 0–3s: {[p for p in A["pauses"] if p[0]<3]}')
for h in HOOK: md.append(f'- [OCR] t={h["t"]:.1f}s chữ trên màn hình: {" | ".join(h["text"]) if h["text"] else "(không có)"}')
if titles:
    md+=['','## Chữ cố định (tiêu đề/nhãn/UI giữ ≥3s) [OCR]','','| t | chữ | hộp [x0,y0,x1,y1] px | cao px | màu ước tính |','|---|---|---|---|---|']
    for ti in sorted(titles,key=lambda x:x['t0'])[:25]: md.append(f'| {ti["t0"]:.0f}–{ti["t1"]:.0f}s | {ti["text"][:40]} | {ti["box"]} | {ti["h"]} | {ti["color"]} |')
md+=['','## Timeline theo shot (shot >4s được chia đoạn ≤3s)','','| t | bố cục [KHUNG] | khung hình & zoom [ĐO] | caption [OCR] | đồ hoạ/chữ khác [OCR] | chuyển cảnh [ĐO/SUY] | âm thanh [ĐO/SUY] |','|---|---|---|---|---|---|---|']
for s,e,first in rows():
    lc=labs_in(s,e); lay=', '.join(f'{NAMES.get(k,k)}' for k,_ in lc.most_common(2)) if lc else '?'
    sm=[x for x in LAY if s<=x['t']<e]
    sy=[x['seam_y'] for x in sm if x['seam_y']]; fb=[x['face'] for x in sm if x['face']]
    if sy and any(x['lab'].startswith('split') for x in sm): lay+=f'; chia y≈{int(np.median(sy))}px'
    if fb: b=fb[len(fb)//2]; lay+=f'; mặt [{b[0]},{b[1]},{b[2]}×{b[3]}]'
    z=[]
    for p in punches:
        if s-0.05<=p['t']<=s+0.2 and first: z.append(f'{p["kind"]} ×{p["scale"]}')
    for dr in drifts:
        if dr['start']<e and dr['end']>s: z.append(f'{dr["kind"]} {dr["pct_per_s"]}%/s'); break
    zoom=', '.join(z) if z else '—'
    cs=[c for c in chunks if s-0.5<=c['t']<e]
    cap='; '.join(f'"{c["text"][:40]}" ({c["words"]}w, y{c["y"]}, h{c["h"]}, {c["color"]})' for c in cs[:3]) or '—'
    oth=[]
    for o in OCR:
        if s<=o['t']<e:
            for it in o['items']:
                cy=(it['box'][1]+it['box'][3])/2
                if not (band[0]*RH<=cy<=band[1]*RH) or persistent(it['text']):
                    oth.append(f'{it["text"][:22]}@y{it["box"][1]}')
    oth=list(dict.fromkeys(oth))[:3]; gfx='; '.join(oth) or '—'
    if first and s>0:
        sc=float(scores[np.argmin(np.abs(times-s))]) if len(times) else 0
        tr=f'cắt cứng (score {sc:.2f})'
    elif first: tr='mở video'
    else: tr='(cùng shot)'
    au='—'
    if A:
        seg=[r for t_,r in A['curve_0p5s'] if s<=t_<e]
        hs=[h for h in A['hit_candidates'] if s<=h<e]; ps=[p for p in A['pauses'] if s<=p[0]<e]
        mw=[b for k,b in A['music_win'] if s<=k+0.5<e]
        mus=('nền liên tục(nhạc?)' if mw and sum(mw)/len(mw)>=0.5 else 'có lặng giữa câu') if mw else ''
        au=(f'RMS {np.mean(seg):.0f} dB; {mus}' if seg else '')+(f'; đỉnh nghi sfx {hs}' if hs else '')+(f'; ngừng {ps}' if ps else '')
    md.append(f'| {s:.1f}–{e:.1f} | {lay} | {zoom} | {cap} | {gfx} | {tr} | {au} |')
md+=['','## Ghi chú phương pháp','',
 '- Scene score: ffmpeg `select=gte(scene,0)` trên khung 192px; cắt = score ≥0,2/0,3 (cách ≥0,2s). Ứng viên jump-cut = đỉnh cục bộ 0,06–0,2.',
 '- Zoom: ORB + estimateAffinePartial2D giữa các frame 10 fps; tỉ lệ ở điểm cắt = punch; trôi tỉ lệ tích luỹ trong shot ≥3% = push-in/pull-out. Split-screen làm sai số tăng (chỉ một nửa khung zoom).',
 '- Bố cục: Haar face + dò đường chia ngang + mật độ cạnh/độ sáng (2 fps). Caption: RapidOCR 1 fps (bỏ dấu tiếng Việt có thể sai), màu = k-means trong hộp chữ (ước tính, viền/đổ bóng làm lệch).',
 '- Âm thanh: RMS 50 ms (astats), ngừng = thấp hơn mức giọng 15 dB ≥0,25s; đỉnh nghi sfx = nhảy ≥8 dB so với trung vị 0,5s trước khi đang có tiếng (không phân biệt được sfx với nhấn giọng → [SUY]).']
open(f'{d}/{vid}_breakdown.md','w').write('\n'.join(md))
print('OK',vid,round(DUR),'s',summary['cuts_thr0_3'],'cuts',layout_pct)
