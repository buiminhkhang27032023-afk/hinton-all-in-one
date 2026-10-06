#!/usr/bin/env python3
"""MAP-HOTEL-HP-01 — OmniVoice TTS, male clone v2 locked @1.2 (voice-lock.md). Run inside flock render lock."""
import hashlib, json, subprocess, time, urllib.request
from pathlib import Path
ENDPOINT="http://127.0.0.1:8123"; SPEED=1.2; EXPECTED_REF="voice-lock-vn-v2.wav"
WORK=Path("/workspace/video-jobs/MAP-HOTEL-HP-01/lam-viec"); CACHE=WORK/"tts_cache"; VOICE=WORK/"voice"
CACHE.mkdir(exist_ok=True)
GAP_IN=0.14; GAP_SCENE=0.38; HEAD=0.0
def health():
    with urllib.request.urlopen(ENDPOINT+"/health",timeout=10) as r: return json.loads(r.read())
def tts(text):
    body=json.dumps({"text":text,"speed":SPEED,"language":"vi"}).encode()
    req=urllib.request.Request(ENDPOINT+"/tts",data=body,headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=1800) as r:
        locked=r.headers.get("X-Voice-Locked"); clone=r.headers.get("X-Voice-Clone"); data=r.read()
    if locked!="true" or not (clone or "").endswith(EXPECTED_REF): raise RuntimeError(f"voice lock fail locked={locked} clone={clone}")
    return data, clone
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",str(p)],text=True))
def silence(sec):
    f=CACHE/f"gap_{int(sec*1000)}ms.wav"
    if not f.exists(): subprocess.check_call(["ffmpeg","-v","error","-y","-f","lavfi","-i","anullsrc=r=48000:cl=mono","-t",str(sec),"-c:a","pcm_s16le",str(f)])
    return f
def main():
    h=health(); print("HEALTH",json.dumps(h),flush=True)
    if not (h.get("voice_locked") is True and str(h.get("ref_audio","")).endswith(EXPECTED_REF) and abs(float(h.get("speed",0))-SPEED)<1e-6):
        raise SystemExit(f"health not OK: {h}")
    sc=json.loads((WORK/"script.json").read_text())
    items=[]
    for si,scene in enumerate(sc["scenes"]):
        for ji,s in enumerate(scene["sentences"]):
            items.append({"scene":scene["id"],"scene_i":si,"j":ji,"voice":" ".join(p[1] for p in s),"display":" ".join(p[0] for p in s),"phrases":s})
    for i,it in enumerate(items):
        key=hashlib.sha1(f"{it['voice']}|{SPEED}|{EXPECTED_REF}".encode()).hexdigest()[:16]
        raw=CACHE/f"{key}.raw.wav"; trim=CACHE/f"{key}.trim.wav"
        if not raw.exists():
            for att in range(1,4):
                try:
                    t0=time.time(); data,clone=tts(it["voice"]); raw.write_bytes(data)
                    print(f"TTS {i+1}/{len(items)} ok {time.time()-t0:.1f}s clone={clone} :: {it['voice'][:60]}",flush=True); break
                except Exception as e:
                    print(f"TTS {i+1} attempt {att} FAIL: {e}",flush=True)
                    if att==3: raise
                    time.sleep(5)
        else: print(f"TTS {i+1}/{len(items)} cached :: {it['voice'][:60]}",flush=True)
        if not trim.exists():
            af=("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,areverse,"
                "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,areverse")
            subprocess.check_call(["ffmpeg","-v","error","-y","-i",str(raw),"-af",af,"-ar","48000","-ac","1","-c:a","pcm_s16le",str(trim)])
        it["file"]=str(trim)
    lines=[]; cur=0.0; tim=[]
    for i,it in enumerate(items):
        d=dur(it["file"]); tim.append({**{k:it[k] for k in ("scene","scene_i","j","voice","display","phrases")},"i":i,"start":round(cur,3),"end":round(cur+d,3)})
        lines.append(f"file '{it['file']}'"); cur+=d
        if i<len(items)-1:
            g=GAP_SCENE if items[i+1]["scene_i"]!=it["scene_i"] else GAP_IN
            lines.append(f"file '{silence(g)}'"); cur+=g
    (VOICE/"concat.txt").write_text("\n".join(lines)+"\n")
    rawo=VOICE/"voice_raw.wav"
    subprocess.check_call(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",str(VOICE/"concat.txt"),"-c","copy",str(rawo)])
    final=VOICE/"voice_storytelling.wav"
    subprocess.check_call(["ffmpeg","-v","error","-y","-i",str(rawo),"-af","loudnorm=I=-14:TP=-1.5:LRA=11","-ar","48000","-ac","1","-c:a","pcm_s16le",str(final)])
    (VOICE/"timings.json").write_text(json.dumps({"total":round(dur(final),3),"sentences":tim,"qa":"OmniVoice · male clone v2 locked · 1.2 · voice_locked:true","health":h},ensure_ascii=False,indent=2))
    print("DONE total",dur(final),flush=True)
if __name__=="__main__": main()
