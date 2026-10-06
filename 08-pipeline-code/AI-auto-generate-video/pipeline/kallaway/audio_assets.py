#!/usr/bin/env python3
"""(pipeline copy) Synthesize royalty-free (self-made, CC0) sfx + background music loop with numpy.
Usage: make_audio_assets.py OUTDIR [music_seconds=30] [bpm=120]
Outputs: whoosh.wav pop.wav hit.wav click.wav scan.wav music.wav (48kHz mono 16-bit)."""
import sys, wave, numpy as np
SR = 48000
out = sys.argv[1]; MS = float(sys.argv[2]) if len(sys.argv) > 2 else 30; BPM = float(sys.argv[3]) if len(sys.argv) > 3 else 120
rng = np.random.default_rng(7)
def save(name, x, peak=0.89):
    x = x / (np.max(np.abs(x)) + 1e-9) * peak
    with wave.open(f"{out}/{name}.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes())
def t(d): return np.arange(int(SR * d)) / SR
def lp(x, a):  # one-pole lowpass, a in (0,1) per-sample or array
    y = np.zeros_like(x); s = 0.0; a = np.broadcast_to(a, x.shape)
    for i in range(len(x)): s += a[i] * (x[i] - s); y[i] = s
    return y
# whoosh: noise through sweeping lowpass, swelling envelope
d = 0.45; tt = t(d); n = rng.standard_normal(len(tt))
sweep = 0.02 + 0.5 * np.sin(np.pi * tt / d) ** 2
w = lp(n, sweep) - lp(lp(n, sweep), 0.01)
env = np.sin(np.pi * np.clip(tt / d, 0, 1)) ** 1.5
save("whoosh", w * env, 0.7)
# pop: fast pitch-drop sine blip
tt = t(0.09); f = 900 * np.exp(-tt * 40) + 300
save("pop", np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 45), 0.8)
# hit: sub boom + click transient
tt = t(0.9); f = 110 * np.exp(-tt * 9) + 42
boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 4.5)
click = rng.standard_normal(len(tt)) * np.exp(-tt * 120) * 0.5
save("hit", np.tanh(2.2 * (boom + click)), 0.95)
# click: tiny tick
tt = t(0.03); save("click", rng.standard_normal(len(tt)) * np.exp(-tt * 300), 0.6)
# scan: digital data blips
tt = t(0.6); sq = np.sign(np.sin(2 * np.pi * (1200 + 800 * np.floor(tt * 25 % 4)) * tt))
save("scan", sq * (np.floor(tt * 25) % 2) * np.exp(-tt * 2) * 0.4, 0.45)
# music: 4-chord minor pad + kick + hat + pluck arp, seamless loop
beat = 60 / BPM; tt = t(MS); mus = np.zeros(len(tt))
chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G
mf = lambda m: 440 * 2 ** ((m - 69) / 12)
bar = 4 * beat
for i in range(int(MS / bar) + 1):
    s = int(i * bar * SR); e = min(len(tt), int((i + 1) * bar * SR))
    if s >= len(tt): break
    lt = tt[s:e] - tt[s]; ch = chords[i % 4]
    pad = sum(np.sin(2 * np.pi * mf(m) * lt) + 0.3 * np.sin(2 * np.pi * mf(m) * 2.003 * lt) for m in ch)
    mus[s:e] += 0.08 * pad * np.minimum(1, lt / 0.3) * np.minimum(1, (bar - lt) / 0.2)
    bass = np.sin(2 * np.pi * mf(ch[0] - 24) * lt); mus[s:e] += 0.18 * bass
    for k in range(8):  # 8th-note arp
        ps = s + int(k * beat / 2 * SR); pe = min(e, ps + int(0.25 * SR))
        if ps >= e: break
        pt = tt[ps:pe] - tt[ps]; m = ch[k % 3] + 12
        mus[ps:pe] += 0.06 * np.sign(np.sin(2 * np.pi * mf(m) * pt)) * np.exp(-pt * 14)
nb = int(MS / beat) + 1
for b in range(nb):
    s = int(b * beat * SR); kt = t(0.35); e = min(len(tt), s + len(kt)); kt = kt[:e - s]
    if s >= len(tt): break
    mus[s:e] += 0.55 * np.sin(2 * np.pi * np.cumsum(55 + 90 * np.exp(-kt * 30)) / SR) * np.exp(-kt * 9)
    hs = s + int(beat / 2 * SR); ht = t(0.05); he = min(len(tt), hs + len(ht))
    if hs < len(tt): mus[hs:he] += 0.12 * rng.standard_normal(he - hs) * np.exp(-ht[:he - hs] * 90)
save("music", np.tanh(1.3 * mus), 0.8)
print("ok", out)
