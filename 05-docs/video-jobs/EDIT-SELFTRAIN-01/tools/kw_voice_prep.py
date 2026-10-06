#!/usr/bin/env python3
"""Tighten VO like Kallaway: trim lead/tail silence, shrink every internal pause > MAXP to KEEP seconds.
Usage: kw_voice_prep.py in.wav out.wav [maxp=0.12] [keep=0.06] [thr_db=-35]"""
import sys, subprocess, re
inp, out = sys.argv[1:3]; MAXP = float(sys.argv[3]) if len(sys.argv) > 3 else 0.12
KEEP = float(sys.argv[4]) if len(sys.argv) > 4 else 0.06; THR = sys.argv[5] if len(sys.argv) > 5 else '-35'
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', inp]))
log = subprocess.run(['ffmpeg', '-i', inp, '-af', f'silencedetect=n={THR}dB:d={MAXP}', '-f', 'null', '-'], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]; en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
if len(en) < len(st): en.append(dur)
keep = []; cur = 0.0
for s, e in zip(st, en):
    if s <= 0.01: cur = max(0, e - 0.03); continue          # lead silence
    if e >= dur - 0.01: keep.append((cur, s + 0.05)); cur = None; break  # tail
    keep.append((cur, s + KEEP / 2)); cur = e - KEEP / 2
if cur is not None: keep.append((cur, dur))
parts = ''.join(f'[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS[a{i}];' for i, (a, b) in enumerate(keep))
fc = parts + ''.join(f'[a{i}]' for i in range(len(keep))) + f'concat=n={len(keep)}:v=0:a=1[o]'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', inp, '-filter_complex', fc, '-map', '[o]', '-ar', '48000', '-ac', '1', out], check=True)
nd = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out]))
print(f'{inp} {dur:.2f}s -> {out} {nd:.2f}s ({len(keep)} pieces)')
