# stricter sfx candidates: high-band (4-10kHz) bursts with spectral tilt above typical speech, sustained >=0.2s
import sys,subprocess,re,json,os,numpy as np
def rms(f,af):
    out=subprocess.run(f'ffmpeg -v error -i "{f}" -vn -af "aresample=22050,{af},asetnsamples=1102,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-" -f null -',shell=True,capture_output=True,text=True).stdout
    t=[];r=[];cur=None
    for line in out.splitlines():
        m=re.search(r'pts_time:([0-9.]+)',line)
        if m: cur=float(m.group(1)); continue
        m=re.search(r'RMS_level=(-?[0-9.]+|-inf)',line)
        if m and cur is not None: t.append(cur); r.append(-100.0 if 'inf' in m.group(1) else max(-100.0,float(m.group(1))))
    return np.array(t),np.array(r)
def run(mp4):
    d=os.path.dirname(mp4); vid=os.path.basename(mp4)[:-4]
    t,h=rms(mp4,'highpass=f=4000,highpass=f=4000'); t2,v=rms(mp4,'lowpass=f=2500')
    n=min(len(h),len(v)); t,h,v=t[:n],h[:n],v[:n]
    if n<20: return None
    tilt=h-v; tmed=np.median(tilt[v>np.percentile(v,40)]) if n else 0
    hp80=np.percentile(h,80)
    hits=[];i=10
    while i<n-4:
        base=np.median(h[i-10:i])
        if h[i]-base>=10 and h[i]>=hp80 and np.all(tilt[i:i+4]>tmed+6):
            hits.append(round(float(t[i]),2)); i+=12
        else: i+=1
    a=json.load(open(f'{d}/{vid}_analysis.json'))
    cuts=a['cuts03']; D=a['summary']['duration']
    on_cut=[c for c in cuts if any(abs(c-x)<=0.25 for x in hits)]
    hit_on_cut=[x for x in hits if any(abs(c-x)<=0.25 for c in cuts)]
    res=dict(hf_hits=hits,hits_per_min=round(60*len(hits)/D,1),pct_cuts_with_hit=round(100*len(on_cut)/max(1,len(cuts)),1),
             pct_hits_on_cut=round(100*len(hit_on_cut)/max(1,len(hits)),1),hits_0_3s=[x for x in hits if x<3])
    json.dump(res,open(f'{d}/{vid}_audio_hf.json','w'))
    return res
if __name__=='__main__':
    for f in sys.argv[1:]:
        r=run(f); print(os.path.basename(f), {k:v for k,v in (r or {}).items() if k!='hf_hits'})
