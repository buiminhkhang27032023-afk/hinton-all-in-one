import json, subprocess, re
A='/workspace/proj1/audio'
raw=json.load(open(f'{A}/vo_raw_timings.json',encoding='utf-8'))
FX=("highpass=f=70,equalizer=f=110:width_type=o:width=1.2:g=3.5,equalizer=f=3000:width_type=o:width=1.5:g=1.5,"
    "acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=2,"
    "aecho=0.85:0.8:35|60:0.10|0.06,loudnorm=I=-16:TP=-1.5:LRA=7")
PAUSE=0.4
def dur(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]))
out={"voice":raw["voice"],"rate":raw["rate"],"pitch":raw["pitch"],"pause_between_paragraphs_s":PAUSE,
     "note":"Per-paragraph times are relative to vo_N.mp3; 'global' times are relative to vo_full.mp3 (seconds).","paragraphs":[]}
t=0.0; parts=[]
for p in raw["paragraphs"]:
    i=p["paragraph"]; src=f'{A}/raw/vo_{i}_raw.mp3'
    log=subprocess.run(['ffmpeg','-i',src,'-af','silencedetect=n=-45dB:d=0.05','-f','null','-'],capture_output=True,text=True).stderr
    ends=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',log)]
    starts=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',log)]
    lead=max(0.0,ends[0]-0.08) if ends and starts and starts[0]<0.01 else 0.0
    last_word_end=max(w["end"] for w in p["words"])
    tail=starts[-1] if starts and starts[-1]>last_word_end-0.3 else last_word_end
    end=tail+0.15
    dst=f'{A}/vo_{i}.wav'
    subprocess.run(['ffmpeg','-y','-v','error','-i',src,'-ss',f'{lead:.3f}','-to',f'{end:.3f}','-af',FX,'-ar','48000','-ac','1',dst],check=True)
    subprocess.run(['ffmpeg','-y','-v','error','-i',dst,'-c:a','libmp3lame','-b:a','192k',f'{A}/vo_{i}.mp3'],check=True)
    d=dur(f'{A}/vo_{i}.mp3')
    sh=lambda xs:[{"text":x["text"],"start":round(x["start"]-lead,3),"end":round(x["end"]-lead,3),
                   "global_start":round(x["start"]-lead+t,3),"global_end":round(x["end"]-lead+t,3)} for x in xs]
    out["paragraphs"].append({"paragraph":i,"text":p["text"],"duration":round(d,3),"global_start":round(t,3),"global_end":round(t+d,3),
                              "sentences":sh(p["sentences"]),"words":sh(p["words"])})
    parts.append(dst); t+=d+PAUSE
subprocess.run(['ffmpeg','-y','-v','error','-f','lavfi','-i','anullsrc=r=48000:cl=mono','-t',str(PAUSE),f'{A}/sil.wav'],check=True)
with open(f'{A}/concat.txt','w') as f:
    for k,pp in enumerate(parts):
        f.write(f"file '{pp}'\n")
        if k<len(parts)-1: f.write(f"file '{A}/sil.wav'\n")
subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',f'{A}/concat.txt','-ar','48000','-c:a','libmp3lame','-b:a','192k',f'{A}/vo_full.mp3'],check=True)
out["total_duration"]=round(dur(f'{A}/vo_full.mp3'),3)
json.dump(out,open(f'{A}/vo_timings.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
for p in out["paragraphs"]: print(p["paragraph"],p["duration"],p["global_start"],len(p["words"]),len(p["sentences"]))
print("total",out["total_duration"])
