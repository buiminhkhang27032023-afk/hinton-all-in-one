# measure caption chunk durations at 10 fps by OCR on caption band crop
import sys,os,json,subprocess,numpy as np,re,difflib
import onnxruntime as _ort
_SO=_ort.SessionOptions
def _so():
    o=_SO(); o.intra_op_num_threads=2; o.inter_op_num_threads=1; return o
_ort.SessionOptions=_so
from rapidocr_onnxruntime import RapidOCR
eng=RapidOCR()
mp4=sys.argv[1]; y0r,y1r=float(sys.argv[2]),float(sys.argv[3])  # fraction of height
t0,t1=float(sys.argv[4]),float(sys.argv[5]); fps=10
w,h=[int(x) for x in subprocess.run(f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "{mp4}"',shell=True,capture_output=True,text=True).stdout.strip().split(',')[:2]]
Y0=int(h*y0r)//2*2; Y1=int(h*y1r)//2*2; W=w
p=subprocess.Popen(f'ffmpeg -v error -ss {t0} -t {t1-t0} -i "{mp4}" -vf "fps={fps},crop={W}:{Y1-Y0}:0:{Y0}" -f rawvideo -pix_fmt bgr24 -',shell=True,stdout=subprocess.PIPE)
n=W*(Y1-Y0)*3;i=0;seq=[]
while True:
    b=p.stdout.read(n)
    if len(b)<n: break
    img=np.frombuffer(b,np.uint8).reshape((Y1-Y0,W,3))
    out,_=eng(img); txt=' '.join(x[1] for x in (out or []) if float(x[2])>0.6).strip()
    seq.append((round(t0+i/fps,2),re.sub(r'\s+',' ',txt))); i+=1
chunks=[]
for t,tx in seq:
    if chunks and (tx==chunks[-1][2] or (tx and chunks[-1][2] and difflib.SequenceMatcher(None,tx,chunks[-1][2]).ratio()>0.8)):
        chunks[-1][1]=t
    else: chunks.append([t,t,tx])
ch=[c for c in chunks if c[2]]
d=[round(c[1]-c[0]+1/fps,2) for c in ch]
gaps=[round(ch[k+1][0]-ch[k][1]-1/fps,2) for k in range(len(ch)-1)]
res=dict(file=mp4,band=[y0r,y1r],win=[t0,t1],n=len(ch),dur_med=float(np.median(d)) if d else None,dur_p10=float(np.percentile(d,10)) if d else None,
         dur_p90=float(np.percentile(d,90)) if d else None,frames30_med=round(30*float(np.median(d))) if d else None,
         gap_zero_pct=round(100*sum(1 for g in gaps if g<=0.01)/max(1,len(gaps))),chunks=[(c[0],round(c[1]-c[0]+1/fps,2),c[2]) for c in ch])
print(json.dumps({k:v for k,v in res.items() if k!='chunks'},ensure_ascii=False)); print(res['chunks'][:14])
os.makedirs('/workspace/video-learn/capchunks',exist_ok=True)
json.dump(res,open('/workspace/video-learn/capchunks/'+os.path.basename(mp4)[:-4]+'.json','w'),ensure_ascii=False)
