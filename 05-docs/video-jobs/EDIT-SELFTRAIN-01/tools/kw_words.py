#!/usr/bin/env python3
"""Word timestamps for a KNOWN script: faster-whisper small int8 (CPU) word timings, then align to script tokens
with difflib; unmatched script tokens are interpolated by syllable position. Run with /workspace/.whisper-venv/bin/python.
Usage: kw_words.py voice.wav script.txt words.json"""
import sys, json, re, difflib, unicodedata
from faster_whisper import WhisperModel
import subprocess, numpy as np
wav, txt, out = sys.argv[1:4]
script = open(txt).read().split()
norm = lambda w: re.sub(r'[^\w]', '', unicodedata.normalize('NFC', w.lower()))
m = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=4)
audio = np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',wav,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True,check=True).stdout, np.float32)
segs, info = m.transcribe(audio, language='vi', word_timestamps=True, beam_size=5, vad_filter=False)
hw = []
for s in segs:
    for w in s.words:
        for k, piece in enumerate(w.word.split()):  # whisper may glue words
            hw.append({'w': piece, 's': w.start, 'e': w.end})
dur = info.duration
A = [norm(w) for w in script]; B = [norm(h['w']) for h in hw]
times = [None] * len(script)
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1): times[i1 + k] = (hw[j1 + k]['s'], hw[j1 + k]['e'])
    elif tag == 'replace' and j2 > j1:   # spread the hypothesis span over the script span
        s0, e0 = hw[j1]['s'], hw[j2 - 1]['e']; n = i2 - i1
        for k in range(n): times[i1 + k] = (s0 + (e0 - s0) * k / n, s0 + (e0 - s0) * (k + 1) / n)
# interpolate gaps
for i in range(len(times)):
    if times[i] is None:
        p = next((times[j][1] for j in range(i - 1, -1, -1) if times[j]), 0.0)
        q = next((times[j][0] for j in range(i + 1, len(times)) if times[j]), dur)
        j0 = i; j1 = i
        while j1 + 1 < len(times) and times[j1 + 1] is None: j1 += 1
        n = j1 - j0 + 1
        for k in range(n): times[j0 + k] = (p + (q - p) * k / n, p + (q - p) * (k + 1) / n)
res = [{'i': i, 'w': w, 's': round(t[0], 3), 'e': round(t[1], 3)} for i, (w, t) in enumerate(zip(script, times))]
json.dump({'duration': dur, 'words': res, 'hyp': ' '.join(h['w'] for h in hw)}, open(out, 'w'), ensure_ascii=False, indent=1)
print('hyp:', ' '.join(h['w'] for h in hw)); print('matched', sum(1 for a in A if a in B), '/', len(A))
