from faster_whisper import WhisperModel
import wave, numpy as np
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
for f, off in (("kn_a1.wav", 360), ("kn_a2.wav", 2220)):
    w = wave.open(f); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    segs, _ = m.transcribe(a, language="en", beam_size=1, vad_filter=True)
    with open(f + ".txt", "w") as o:
        for s in segs: o.write(f"{s.start + off:7.1f} {s.text.strip()}\n")
