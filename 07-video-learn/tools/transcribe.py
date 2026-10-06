#!/usr/bin/env python3
"""Transcribe one or more mp4 with faster-whisper (small, int8, CPU). Usage: transcribe.py [--model small] [--lang vi] f1.mp4 ...
Writes <id>_transcript.json (segments + word timestamps) and <id>_transcript.txt next to the mp4. Skips if exists."""
import sys, os, json, time, subprocess
import numpy as np
def load_audio(f):
    raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-vn','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).copy()
args=sys.argv[1:]; model='small'; lang=None
VAD='--vad' in args; FORCE='--force' in args; NT='--nt' in args; args=[a for a in args if a not in ('--vad','--force','--nt')]
if '--model' in args: i=args.index('--model'); model=args[i+1]; del args[i:i+2]
if '--lang' in args: i=args.index('--lang'); lang=args[i+1]; del args[i:i+2]
LANG_BY_DIR={'tiktok-':'vi','facebook-nguyentatkiem':'vi','tiktokintl-tommythings':'id','douyin-':'zh'}
from faster_whisper import WhisperModel
m=WhisperModel(model,device='cpu',compute_type='int8',cpu_threads=4)
for f in args:
    d=os.path.dirname(f); vid=os.path.basename(f)[:-4]; out=f'{d}/{vid}_transcript.json'
    if os.path.exists(out) and not FORCE: print('SKIP',f); continue
    folder=os.path.basename(d); L=lang
    if L is None:
        L='en'
        for k,v in LANG_BY_DIR.items():
            if folder.startswith(k): L=v
    t0=time.time()
    segs,info=m.transcribe(load_audio(f),language=L,word_timestamps=True,vad_filter=VAD,beam_size=5,condition_on_previous_text=False,
                           initial_prompt=None,**(dict(no_speech_threshold=None,log_prob_threshold=None,compression_ratio_threshold=None) if NT else {}))
    S=[]
    for s in segs:
        S.append(dict(start=round(s.start,2),end=round(s.end,2),text=s.text.strip(),
                      words=[dict(w=w.word,s=round(w.start,2),e=round(w.end,2),p=round(w.probability,2)) for w in (s.words or [])]))
    J=dict(file=f,vad=VAD,nt=NT,model=model,lang=L,duration=info.duration,segments=S)
    json.dump(J,open(out,'w'),ensure_ascii=False,indent=1)
    open(f'{d}/{vid}_transcript.txt','w').write('\n'.join(f"[{s['start']:6.2f}-{s['end']:6.2f}] {s['text']}" for s in S))
    print('OK',f,L,round(time.time()-t0,1),'s',flush=True)
