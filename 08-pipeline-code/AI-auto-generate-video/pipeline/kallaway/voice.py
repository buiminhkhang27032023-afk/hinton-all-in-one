"""Kallaway-style VO tightening: shrink every pause > maxp to keep seconds; returns a time-map for re-timing."""
import re, subprocess, bisect
from ..common import media_duration

def tighten(inp, out, maxp=0.2, keep=0.2, thr='-35'):
    dur = media_duration(inp)
    log = subprocess.run(['ffmpeg', '-i', str(inp), '-af', f'silencedetect=n={thr}dB:d={maxp}', '-f', 'null', '-'], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: (-?[\d.]+)', log)]; en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
    if len(en) < len(st): en.append(dur)
    keepi = []; cur = 0.0
    for s, e in zip(st, en):
        s = max(0.0, s)
        if s <= 0.01: cur = max(0, e - 0.03); continue
        if e >= dur - 0.01: keepi.append((cur, min(dur, s + 0.05))); cur = None; break
        keepi.append((cur, s + keep / 2)); cur = e - keep / 2
    if cur is not None: keepi.append((cur, dur))
    parts = ''.join(f'[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS[a{i}];' for i, (a, b) in enumerate(keepi))
    fc = parts + ''.join(f'[a{i}]' for i in range(len(keepi))) + f'concat=n={len(keepi)}:v=0:a=1[o]'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(inp), '-filter_complex', fc, '-map', '[o]', '-ar', '48000', '-ac', '1',
                    '-c:a', 'pcm_s16le', str(out)], check=True)
    starts = [a for a, b in keepi]; offs = []; acc = 0.0
    for a, b in keepi: offs.append(acc - a); acc += b - a
    def tmap(t):
        i = max(0, bisect.bisect_right(starts, t) - 1); a, b = keepi[i]
        return round(min(max(t, a), b) + offs[i], 4)
    return tmap, {'in': round(dur, 3), 'out': round(acc, 3), 'pieces': len(keepi)}
