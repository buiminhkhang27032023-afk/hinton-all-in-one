#!/usr/bin/env python3
"""OmniVoice TTS for MAP-FOOD-HCM-01 — male clone v2 locked @1.2."""
import hashlib, json, os, subprocess, time, urllib.request
from pathlib import Path

ENDPOINT = "http://127.0.0.1:8123"
SPEED = 1.2
EXPECTED_REF = "voice-lock-vn-v2.wav"
WORK = Path("/workspace/video-jobs/MAP-FOOD-HCM-01/lam-viec")
CACHE = WORK / "tts_cache"
VOICE = WORK / "voice"
CACHE.mkdir(exist_ok=True)
VOICE.mkdir(exist_ok=True)
GAP = 0.12

def health():
    with urllib.request.urlopen(ENDPOINT + "/health", timeout=10) as r:
        return json.loads(r.read())

def tts(text):
    body = json.dumps({"text": text, "speed": SPEED, "language": "vi"}).encode()
    req = urllib.request.Request(ENDPOINT + "/tts", data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1800) as r:
        locked = r.headers.get("X-Voice-Locked")
        clone = r.headers.get("X-Voice-Clone")
        data = r.read()
    if locked != "true" or not (clone or "").endswith(EXPECTED_REF):
        raise RuntimeError(f"voice lock fail: locked={locked} clone={clone}")
    return data, clone

def dur(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nk=1:nw=1", str(path)], text=True)
    return float(out.strip())

def main():
    h = health()
    print("HEALTH", json.dumps(h))
    if not (h.get("voice_locked") is True and str(h.get("ref_audio","")).endswith(EXPECTED_REF) and abs(float(h.get("speed",0))-SPEED)<1e-6):
        raise SystemExit(f"health not OK for voice lock: {h}")
    sents = json.loads((VOICE/"sentences.json").read_text())
    chunks = []
    for i, s in enumerate(sents):
        key = hashlib.sha1(f"{s}|{SPEED}|{EXPECTED_REF}".encode()).hexdigest()[:16]
        raw = CACHE / f"{key}.raw.wav"
        trimmed = CACHE / f"{key}.trim.wav"
        if not raw.exists():
            for attempt in range(1, 4):
                try:
                    t0 = time.time()
                    data, clone = tts(s)
                    raw.write_bytes(data)
                    print(f"TTS {i+1}/{len(sents)} ok {time.time()-t0:.1f}s clone={clone} :: {s[:60]}")
                    break
                except Exception as e:
                    print(f"TTS {i+1} attempt {attempt} FAIL: {e}")
                    if attempt == 3: raise
                    time.sleep(5)
        else:
            print(f"TTS {i+1}/{len(sents)} cached :: {s[:60]}")
        if not trimmed.exists():
            af = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.04,"
                  "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,areverse")
            subprocess.check_call(["ffmpeg","-v","error","-y","-i",str(raw),"-af",af,"-ar","48000","-ac","1","-c:a","pcm_s16le",str(trimmed)])
        chunks.append((s, trimmed))

    gapf = CACHE / f"gap_{int(GAP*1000)}ms.wav"
    if not gapf.exists():
        subprocess.check_call(["ffmpeg","-v","error","-y","-f","lavfi","-i","anullsrc=r=48000:cl=mono","-t",str(GAP),"-c:a","pcm_s16le",str(gapf)])

    lst = VOICE / "concat.txt"
    lines, timings, cur = [], [], 0.0
    for i, (s, c) in enumerate(chunks):
        d = dur(c)
        timings.append({"i": i, "text": s, "start": round(cur, 3), "end": round(cur + d, 3), "dur": round(d, 3)})
        lines.append(f"file '{c}'"); cur += d
        if i < len(chunks) - 1:
            lines.append(f"file '{gapf}'"); cur += GAP
    lst.write_text("\n".join(lines) + "\n")
    raw_out = VOICE / "voice_raw.wav"
    subprocess.check_call(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",str(lst),"-c","copy",str(raw_out)])
    # loudnorm ~-14 LUFS
    final = VOICE / "voice_storytelling.wav"
    subprocess.check_call([
        "ffmpeg","-v","error","-y","-i",str(raw_out),
        "-af","loudnorm=I=-14:TP=-1.5:LRA=11","-ar","48000","-ac","1","-c:a","pcm_s16le",str(final)])
    (VOICE/"timings.json").write_text(json.dumps({"total": round(dur(final),3), "sentences": timings, "qa": "OmniVoice · male clone v2 locked · 1.2 · voice_locked:true", "health": h}, ensure_ascii=False, indent=2))
    # SRT from sentence timings
    def ts(sec):
        h=int(sec//3600); m=int((sec%3600)//60); s=int(sec%60); ms=int(round((sec-int(sec))*1000))
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    srt = []
    for t in timings:
        srt.append(f"{t['i']+1}\n{ts(t['start'])} --> {ts(t['end'])}\n{t['text']}\n")
    (VOICE/"subtitle.srt").write_text("\n".join(srt), encoding="utf-8")
    print("DONE total", dur(final), "s ->", final)

if __name__ == "__main__":
    main()
