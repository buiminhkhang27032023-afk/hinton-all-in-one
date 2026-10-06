"""Repair collapsed word timings (whisperx/fw fallback collapsed some sentences) by re-aligning each bad sentence
with faster-whisper on its own audio segment; unmatched tokens interpolated by syllable length."""
import json, difflib, re, subprocess, tempfile, os
import numpy as np
from faster_whisper import WhisperModel
LV = "/workspace/video-jobs/HM-103/lam-viec"
tts = json.load(open(f"{LV}/tts.json")); W = json.load(open(f"{LV}/words.json"))
words = W["words"]
def norm(s): return re.sub(r"[^\wÀ-ỹ']", "", s.lower())
def bad(ws, st, en):
    d = en - st
    starts = [w["start"] for w in ws]
    cover = ws[-1]["end"] - ws[0]["start"]
    zero = sum(1 for w in ws if w["end"] - w["start"] < 0.03)
    nonmono = any(b < a for a, b in zip(starts, starts[1:]))
    dup = len(set(starts)) < len(starts) * 0.8
    return cover < 0.6 * d or zero > max(1, len(ws) // 4) or nonmono or dup
model = None
report = {}
for si, s in enumerate(tts["sentences"]):
    ws = [w for w in words if w["sent"] == si]
    st, en = s["start"], s["end"]
    if not bad(ws, st, en):
        report[si] = "ok"; continue
    if model is None:
        model = WhisperModel("small", device="cpu", compute_type="int8")
    seg = tempfile.mktemp(suffix=".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, st-0.05):.3f}", "-t", f"{en-st+0.1:.3f}", "-i", f"{LV}/voice.wav", "-ar", "16000", "-ac", "1", seg], check=True)
    import wave as _w
    _f = _w.open(seg); _a = np.frombuffer(_f.readframes(_f.getnframes()), dtype="<i2").astype(np.float32) / 32768; _f.close()
    segs, _ = model.transcribe(_a, language="vi", word_timestamps=True, beam_size=5, initial_prompt=s["text"])
    rec = [(norm(x.word), x.start + max(0, st-0.05), x.end + max(0, st-0.05)) for sg in segs for x in (sg.words or []) if norm(x.word)]
    os.remove(seg)
    a = [norm(w["word"]) for w in ws]; b = [r[0] for r in rec]
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    times = [None] * len(ws)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            times[blk.a + k] = (rec[blk.b + k][1], rec[blk.b + k][2])
    matched = sum(1 for t in times if t)
    # interpolate unmatched by syllable-length weights between anchors
    wts = [max(1, len(norm(w["word"]))) + 1.5 for w in ws]
    anchors = [(-1, st)] + [(k, times[k][0]) for k in range(len(ws)) if times[k]] + [(len(ws), en)]
    for (ka, ta), (kb, tb) in zip(anchors, anchors[1:]):
        gap = list(range(ka + 1, kb))
        if not gap: continue
        t0 = times[ka][1] if ka >= 0 and times[ka] else ta
        tot = sum(wts[k] for k in gap); cur = t0
        for k in gap:
            dd = (tb - t0) * wts[k] / tot; times[k] = (cur, cur + dd); cur += dd
    # enforce monotonic, clamp to sentence
    prev = st
    for k, w in enumerate(ws):
        s0, e0 = times[k]; s0 = max(prev, min(s0, en - 0.05)); e0 = max(s0 + 0.05, min(e0, en))
        w["start"], w["end"] = round(s0, 3), round(e0, 3); w["fix"] = True; prev = s0 + 0.02
    report[si] = f"realigned {matched}/{len(ws)} matched"
json.dump(W, open(f"{LV}/words.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(report, ensure_ascii=False))
