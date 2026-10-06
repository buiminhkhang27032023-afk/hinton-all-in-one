#!/usr/bin/env python3
"""Audio mix + mux for a plan: voice @-16 LUFS, music at (voice - music_under dB) with dips, sfx hits, final
2-pass loudnorm -14 LUFS / TP -1.5. Run INSIDE the render lock.
Usage: kw_mix.py plan.json  (uses plan keys: voice, music, music_under, music_dips, sfx, video_out, final_out, dur)"""
import sys, json, subprocess, re
P = json.load(open(sys.argv[1])); A = P['assets_dir']; D = P['dur']
def lufs(path, af=''):
    e = subprocess.run(['ffmpeg', '-nostats', '-i', path, '-af', (af + ',' if af else '') + 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', e)[-1])
VT = -16.0; vg = VT - lufs(P['voice']); mg = (VT - P.get('music_under', 20)) - lufs(P['music'])
GAIN = {'whoosh': -12, 'pop': -10, 'hit': -6, 'click': -18, 'scan': -16}
ins = ['-i', P['video_out'], '-i', P['voice'], '-stream_loop', '-1', '-i', P['music']]; fc = []
fc.append(f'[1:a]aresample=48000,volume={vg:.2f}dB,apad=whole_dur={D}[v]')
dips = '+'.join(f'between(t,{a},{b})' for a, b in P.get('music_dips', [])) or '0'
fc.append(f"[2:a]aresample=48000,atrim=0:{D},volume={mg:.2f}dB,volume='if({dips},0.0,1)':eval=frame,afade=t=out:st={D-0.35}:d=0.35[m]")
labels = ['[v]', '[m]']
for i, s in enumerate(P.get('sfx', [])):
    ins += ['-i', f"{A}/{s['name']}.wav"]; k = 3 + i; ms = int(s['t'] * 1000)
    fc.append(f"[{k}:a]aresample=48000,volume={GAIN[s['name']] + s.get('db', 0)}dB,adelay={ms}|{ms}[s{i}]"); labels.append(f'[s{i}]')
fc.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{D}[mix]')
pre = P['final_out'].replace('.mp4', '_premix.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(fc), '-map', '[mix]', '-ac', '2', pre], check=True)
e = subprocess.run(['ffmpeg', '-nostats', '-i', pre, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
j = json.loads(e[e.rindex('{'):e.rindex('}') + 1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:"
      f"measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', P['video_out'], '-i', pre, '-filter_complex', f'[1:a]{ln},aresample=48000[a]',
                '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', str(D), '-movflags', '+faststart', P['final_out']], check=True)
print('final', P['final_out'], 'LUFS', lufs(P['final_out']))
