#!/usr/bin/env python3
"""HM-101 v3 — procedurally synthesized SFX + BGM (numpy only, no samples, no third-party audio)."""
import numpy as np, wave
from pathlib import Path
SR = 48000
OUT = Path("/workspace/video-jobs/HM-101/source/sfx")
rng = np.random.default_rng(101)

def save(name, x, stereo=False):
    x = np.asarray(x, dtype=np.float64)
    peak = np.max(np.abs(x)) or 1.0
    if peak > 0.98: x = x / peak * 0.98
    if stereo and x.ndim == 1: x = np.stack([x, x], 1)
    ch = 2 if x.ndim == 2 else 1
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(str(OUT / name), "wb") as w:
        w.setnchannels(ch); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print("wrote", OUT / name, f"{len(x)/SR:.2f}s")

def t_(d): return np.arange(int(d * SR)) / SR

def onepole_lp(x, fc):
    """Time-varying one-pole low-pass; fc may be array."""
    fc = np.broadcast_to(np.asarray(fc, dtype=float), x.shape)
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a[i]) * x[i] + a[i] * s; y[i] = s
    return y

# --- whoosh: pink-ish noise through sweeping LP/HP band, swell envelope
def whoosh(d=0.42, f0=400, f1=6000, seed=0):
    r = np.random.default_rng(seed)
    t = t_(d); n = r.standard_normal(len(t))
    sweep = f0 * (f1 / f0) ** (np.sin(np.pi * t / d * 0.5) ** 1.5)
    lp = onepole_lp(n, sweep)
    hp = lp - onepole_lp(lp, sweep * 0.25)
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2.2
    env *= np.exp(-1.2 * t / d)
    return hp * env

w1 = whoosh(0.40, 300, 7000, 1); save("whoosh_a.wav", w1 / np.max(np.abs(w1)) * 0.8)
w2 = whoosh(0.32, 600, 9000, 2); save("whoosh_b.wav", w2 / np.max(np.abs(w2)) * 0.8)
w3 = whoosh(0.50, 200, 5000, 3); save("whoosh_c.wav", w3 / np.max(np.abs(w3)) * 0.8)

# --- ding: bell partials with exponential decay
t = t_(0.9)
ding = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, a, k in
           [(1568, 0.6, 5.5), (3136, 0.25, 8), (4704, 0.12, 11), (2349, 0.18, 7)])
ding *= np.minimum(1, t / 0.003)
save("ding.wav", ding / np.max(np.abs(ding)) * 0.8)

# --- pop: fast pitch drop sine + click
t = t_(0.14)
f = 950 * np.exp(-t * 28) + 220
ph = 2 * np.pi * np.cumsum(f) / SR
pop = np.sin(ph) * np.exp(-t * 32) + 0.25 * rng.standard_normal(len(t)) * np.exp(-t * 300)
save("pop.wav", pop / np.max(np.abs(pop)) * 0.8)

# --- marker squeak (highlighter): filtered noise 0.3s
t = t_(0.30); n = rng.standard_normal(len(t))
mk = onepole_lp(n, 3500) - onepole_lp(n, 1200)
mk *= np.sin(np.pi * t / 0.30) ** 0.7
save("marker.wav", mk / np.max(np.abs(mk)) * 0.6)

# --- thump/impact for presenter cut-ins
t = t_(0.45)
f = 110 * np.exp(-t * 9) + 45
th = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
th += 0.15 * onepole_lp(rng.standard_normal(len(t)), 800) * np.exp(-t * 30)
save("impact.wav", th / np.max(np.abs(th)) * 0.85)

# --- BGM: 120 BPM synth bed, Am-F-C-G, pad + pluck arp + soft kick + hats (stereo)
BPM = 120; beat = 60 / BPM; D = 52.2
T = t_(D); N = len(T)
L = np.zeros(N); R = np.zeros(N)
chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G (midi)
mid = lambda m: 440 * 2 ** ((m - 69) / 12)
bar = 4 * beat
for bi in range(int(D / bar) + 1):
    ch = chords[bi % 4]; s0 = int(bi * bar * SR); s1 = min(N, int((bi + 1) * bar * SR))
    if s0 >= N: break
    tt = np.arange(s1 - s0) / SR
    pad = np.zeros_like(tt)
    for m in ch:
        for det in (-0.08, 0.08):
            fr = mid(m) * 2 ** (det / 12)
            # soft saw approx (5 harmonics)
            pad += sum(np.sin(2 * np.pi * fr * k * tt) / k for k in range(1, 6)) * 0.05
    envp = np.minimum(1, tt / 0.4) * np.minimum(1, (bar - tt) / 0.3)
    # sidechain pump each beat
    pump = 0.55 + 0.45 * np.minimum(1, ((tt % beat) / (beat * 0.6)))
    pad *= envp * pump
    L[s0:s1] += pad; R[s0:s1] += pad
    # bass root
    bass = np.sin(2 * np.pi * mid(ch[0] - 12) * tt) * 0.22 * pump
    L[s0:s1] += bass; R[s0:s1] += bass
# arp plucks on 8ths
step = beat / 2
for si in range(int(D / step)):
    s0 = int(si * step * SR)
    ch = chords[int(si * step / bar) % 4]
    m = ch[si % 3] + 12 * (1 + (si // 3) % 2)
    tt = np.arange(int(0.25 * SR)) / SR
    pl = (np.sin(2 * np.pi * mid(m) * tt) + 0.3 * np.sin(4 * np.pi * mid(m) * tt)) * np.exp(-tt * 14) * 0.10
    e = min(N, s0 + len(tt)); pan = 0.3 if si % 2 else -0.3
    L[s0:e] += pl[:e - s0] * (1 - pan); R[s0:e] += pl[:e - s0] * (1 + pan)
# kick each beat (soft), hats offbeat
for bi in range(int(D / beat)):
    s0 = int(bi * beat * SR); tt = np.arange(int(0.25 * SR)) / SR
    f = 120 * np.exp(-tt * 30) + 48
    k = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 14) * 0.35
    e = min(N, s0 + len(tt)); L[s0:e] += k[:e - s0]; R[s0:e] += k[:e - s0]
    s1 = int((bi + 0.5) * beat * SR); th = np.arange(int(0.05 * SR)) / SR
    hn = rng.standard_normal(len(th)); hh = (hn - onepole_lp(hn, 6000)) * np.exp(-th * 80) * 0.06
    e = min(N, s1 + len(th))
    if s1 < N: L[s1:e] += hh[:e - s1] * 0.8; R[s1:e] += hh[:e - s1]
fade = np.minimum(1, T / 0.8)
L *= fade; R *= fade
save("bgm_synth_120bpm.wav", np.stack([L, R], 1))
