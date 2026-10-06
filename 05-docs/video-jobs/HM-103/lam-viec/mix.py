#!/usr/bin/env python3
"""HM-103 v1 audio: OmniVoice VO + synth BGM bed + SFX events -> mix_v3.wav (48k stereo)."""
import json, wave, subprocess, re
import numpy as np
from pathlib import Path
ROOT = Path("/workspace/video-jobs/HM-103"); LV = ROOT / "lam-viec"; SFX = ROOT / "source/sfx"
OUTD = LV / "audio"; OUTD.mkdir(exist_ok=True)
plan = json.loads((LV / "plan.json").read_text())
SR = 48000; TOTAL = plan["total"]; VO_END = plan["vo_end"]
N = int(TOTAL * SR)

def rd(p):
    with wave.open(str(p)) as w:
        ch, sr, n = w.getnchannels(), w.getframerate(), w.getnframes()
        x = np.frombuffer(w.readframes(n), dtype="<i2").astype(np.float64) / 32768
    x = x.reshape(-1, ch)
    if ch == 1: x = np.repeat(x, 2, 1)
    assert sr == SR, (p, sr)
    return x

def wr(p, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(str(p), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

def lufs(p):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1]); TP = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1])
    return I, TP

# SFX bus
bank = {}
sfx = np.zeros((N, 2))
for t, name, gdb in plan["sfx"]:
    if name not in bank: bank[name] = rd(SFX / f"{name}.wav")
    s = bank[name]; i0 = max(0, int(t * SR)); i1 = min(N, i0 + len(s))
    if i0 >= N: continue
    sfx[i0:i1] += s[:i1 - i0] * 10 ** (gdb / 20)
wr(OUTD / "sfx_bus.wav", sfx)

vo = rd(LV / "voice.wav")
vo_t = np.zeros((N, 2)); vo_t[:min(N, len(vo))] = vo[:N]
bgm = rd(SFX / "bgm_synth_124bpm.wav")
bgm_t = np.zeros((N, 2)); bgm_t[:min(N, len(bgm))] = bgm[:N]
wr(OUTD / "vo_raw.wav", vo_t); wr(OUTD / "bgm_raw.wav", bgm_t)

I_vo, _ = lufs(OUTD / "vo_raw.wav"); I_bgm, _ = lufs(OUTD / "bgm_raw.wav"); I_sfx, _ = lufs(OUTD / "sfx_bus.wav")
TARGET_VO, TARGET_BGM, TARGET_SFX = -14.0, -21.6, -21.0   # BGM bed (after ducking) ~-24 LUFS, ~10 dB under VO
g_vo = 10 ** ((TARGET_VO - I_vo) / 20); g_bgm = 10 ** ((TARGET_BGM - I_bgm) / 20); g_sfx = 10 ** ((TARGET_SFX - I_sfx) / 20)
# gentle ducking of BGM while VO is active (envelope follower, -3 dB)
env = np.abs(vo_t[:, 0]); k = int(0.15 * SR)
env = np.convolve(env, np.ones(k) / k, mode="same"); duck = 1 - 0.3 * np.clip(env / (env.max() * 0.25), 0, 1)
mix = vo_t * g_vo + bgm_t * g_bgm * duck[:, None] + sfx * g_sfx
# hard stop at VO end (cut to black): 40 ms fade
e0 = int(VO_END * SR); f = int(0.04 * SR)
mix[e0:e0 + f] *= np.linspace(1, 0, f)[:, None]; mix[e0 + f:] = 0
wr(OUTD / "mix_pre.wav", mix)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(OUTD / "mix_pre.wav"), "-af", "alimiter=limit=0.89:level=false",
                "-ar", "48000", "-ac", "2", str(OUTD / "mix.wav")], check=True)
res = dict(I_vo_raw=I_vo, I_bgm_raw=I_bgm, I_sfx_raw=I_sfx, gains_db=dict(vo=20*np.log10(g_vo), bgm=20*np.log10(g_bgm), sfx=20*np.log10(g_sfx)))
# stems at final gain for QA
wr(OUTD / "stem_vo.wav", vo_t * g_vo); wr(OUTD / "stem_bgm.wav", bgm_t * g_bgm * duck[:, None]); wr(OUTD / "stem_sfx.wav", sfx * g_sfx)
for nm in ("stem_vo", "stem_bgm", "stem_sfx", "mix"):
    res[nm] = lufs(OUTD / f"{nm}.wav")
print(json.dumps(res, indent=1, default=float))
(OUTD / "loudness.json").write_text(json.dumps(res, indent=1, default=float))
import shutil; shutil.copy(OUTD / "mix.wav", LV / "hf/assets/mix.wav")
