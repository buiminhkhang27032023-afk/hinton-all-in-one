#!/usr/bin/env python3
"""MAP-HOTEL-HP-01 audio mix: VO (-14 LUFS) + CC0 BGM ~20 LU under voice (sidechain duck) + CC0 SFX at timeline events.
Writes audio/mix.wav and audio/sfx_events.json. Run inside flock."""
import json, subprocess, re, sys
from pathlib import Path
A = Path(__file__).resolve().parent; L = A.parent
data = json.loads((L / "template/build-data.json").read_text())
VO = L / "voice/voice_storytelling.wav"
BGM = A / "bgm/upbeat_seth_696111_hq.mp3"
DUR = data["DUR"]; S = data["scenes"]; R = data["ranked"]

def lufs(path, extra=""):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", (extra + "," if extra else "") + "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1])

ev = []  # (t, file, gain_db, trim)
def add(t, f, g, trim=None): ev.append({"t": round(max(0, t), 3), "f": f, "g": g, "trim": trim})
add(0.0, "impact_a", -15, 1.4)
for i in range(len(R)): add(0.35 + i * 0.22, "pop_a", -12)
add(S["rule"]["start"] - 0.15, "whoosh_c", -16)
order = ["hook", "rule"] + [h["id"] for h in R] + ["cta"]
wh = ["whoosh_a", "whoosh_b", "whoosh_d", "whoosh_a", "whoosh_b"]
for i, h in enumerate(R):
    s = S[h["id"]]["start"]
    if h["rank"] == 1: add(s - 2.2, "riser_a", -15)
    add(s - 0.62, wh[i], -14)
    add(s - 0.02, "impact_a", -13, 1.3)
    add(s + 0.3, "pop_a", -10)
    add(s + 1.45, "ding_a", -18, 1.2)
    sents = S[h["id"]]["sents"]; q = sents[2] if len(sents) > 2 else sents[-1]
    add(q[0] - 0.1, "pop_a", -11)
    if h["nq"] > 1: add(q[0] + (q[1] - q[0]) * 0.45, "pop_a", -11)
    if h["rank"] == 1: add(s + 0.3, "ding_b", -17, 2.0)
cs = S["cta"]["start"]
add(cs - 0.5, "whoosh_c", -14); add(cs, "ding_b", -18, 1.6)
(A / "sfx_events.json").write_text(json.dumps(ev, indent=1))

vo_l = lufs(VO); bgm_l = lufs(BGM)
bgm_gain = (vo_l - 20) - bgm_l
print(f"VO {vo_l} LUFS, BGM raw {bgm_l} LUFS -> BGM gain {bgm_gain:.1f} dB")
inputs = ["-i", str(VO), "-stream_loop", "-1", "-i", str(BGM)]
fc = [f"[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={DUR}[vo]",
      f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{DUR},asetpts=PTS-STARTPTS,volume={bgm_gain:.2f}dB,afade=t=in:st=0:d=0.6,afade=t=out:st={DUR-1.8:.2f}:d=1.8[bg]",
      "[vo]asplit=2[vo1][vosc]",
      "[bg][vosc]sidechaincompress=threshold=0.03:ratio=4:attack=40:release=450:level_sc=1[bgd]"]
labels = ["[vo1]", "[bgd]"]
for k, e in enumerate(ev):
    inputs += ["-i", str(A / "sfx" / f"{e['f']}.wav")]
    idx = k + 2; ms = int(e["t"] * 1000)
    tr = f"atrim=0:{e['trim']},afade=t=out:st={max(0, e['trim']-0.4):.2f}:d=0.4," if e["trim"] else ""
    fc.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,{tr}volume={e['g']}dB,adelay={ms}|{ms}[s{k}]")
    labels.append(f"[s{k}]")
fc.append("".join(labels) + f"amix=inputs={len(labels)}:duration=first:dropout_transition=0:normalize=0,atrim=0:{DUR}[mx]")
fc.append("[mx]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[out]")
out = A / "mix.wav"
cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(fc), "-map", "[out]", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", str(out)]
subprocess.run(cmd, check=True)
# BGM-alone loudness (pre-duck) for QA
print("mix", lufs(out), "LUFS; events", len(ev))
