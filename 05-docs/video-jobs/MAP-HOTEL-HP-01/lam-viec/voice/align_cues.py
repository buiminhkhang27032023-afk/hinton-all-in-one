#!/usr/bin/env python3
"""Forced-align VO (known voice text) -> phrase cues (display text) -> voice/cues.json + output/subtitle.srt; ASR QA."""
import json, sys
from pathlib import Path
sys.path.insert(0, "/workspace/AI-auto-generate-video")
from pipeline.align import align_words, asr_verify
from pipeline.text_vi import words as split_words
V = Path(__file__).resolve().parent; JOB = V.parent.parent
tim = json.loads((V / "timings.json").read_text())
cfg = {"align": {"model": "nguyenvulebinh/wav2vec2-base-vi-vlsp2020", "device": "cpu"}, "asr_verify": {"model": "small", "compute_type": "int8"}}
wav = V / "voice_storytelling.wav"
sents = [{"start": s["start"], "end": s["end"], "text": s["voice"]} for s in tim["sentences"]]
words = align_words(wav, sents, cfg)
cues = []
wi = 0
for si, s in enumerate(tim["sentences"]):
    sw = [w for w in words if w["sent"] == si]
    k = 0
    for disp, voice in s["phrases"]:
        n = len(split_words(voice))
        seg = sw[k:k + n]; k += n
        if not seg: continue
        cues.append({"start": round(seg[0]["start"], 3), "end": round(seg[-1]["end"], 3), "text": disp, "scene": s["scene"]})
    if k != len(sw): print("WARN token mismatch sent", si, k, len(sw))
# monotonic clean-up
for i in range(1, len(cues)):
    if cues[i]["start"] < cues[i-1]["end"]: cues[i]["start"] = cues[i-1]["end"]
(V / "cues.json").write_text(json.dumps(cues, ensure_ascii=False, indent=1))
def ts(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60); return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s-int(s))*1000)):03d}"
srt = []
for i, c in enumerate(cues):
    nx = cues[i+1]["start"] if i + 1 < len(cues) else c["end"] + 0.4
    srt.append(f"{i+1}\n{ts(c['start'])} --> {ts(min(c['end']+0.15, nx))}\n{c['text']}\n")
(JOB / "output").mkdir(exist_ok=True)
(JOB / "output/subtitle.srt").write_text("\n".join(srt), encoding="utf-8")
try:
    qa = asr_verify(wav, " ".join(s["voice"] for s in tim["sentences"]), cfg)
except Exception as e:
    qa = {"error": str(e)}
(V / "asr_qa.json").write_text(json.dumps(qa, ensure_ascii=False, indent=1))
print("cues", len(cues), "asr", qa.get("similarity"), qa.get("error"))
