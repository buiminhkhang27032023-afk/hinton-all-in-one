"""Audio mix for the kallaway preset: voice @-16 LUFS, BGM at (voice - music_under dB) with dips + end fade,
sfx one-shots, then 2-pass loudnorm to cfg loudness (default -14 LUFS / TP -1.5) and mux with the rendered video."""
import json, re, subprocess
GAIN = {'whoosh': -12, 'pop': -10, 'hit': -6, 'click': -18, 'scan': -16}

def lufs(path):
    e = subprocess.run(['ffmpeg', '-nostats', '-i', str(path), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', e)[-1])

def mix(P, video_in, out_mp4, loud=None):
    loud = loud or {'I': -14, 'TP': -1.5, 'LRA': 11}
    A = P['assets_dir']; D = P['dur']; VT = -16.0
    vg = VT - lufs(P['voice'])
    ins = ['-i', str(video_in), '-i', P['voice']]; fc = [f'[1:a]aresample=48000,volume={vg:.2f}dB,apad=whole_dur={D}[v]']; labels = ['[v]']
    if P.get('music'):
        mg = (VT - P.get('music_under', 20)) - lufs(P['music'])
        ins += ['-stream_loop', '-1', '-i', P['music']]
        dips = '+'.join(f'between(t,{a},{b})' for a, b in P.get('music_dips', [])) or '0'
        fc.append(f"[2:a]aresample=48000,atrim=0:{D},volume={mg:.2f}dB,volume='if({dips},0.0,1)':eval=frame,afade=t=out:st={max(0, D-0.35)}:d=0.35[m]")
        labels.append('[m]')
    base = len(ins) // 2 if P.get('music') is None else 3
    k = 2 + (1 if P.get('music') else 0)
    for i, s in enumerate(P.get('sfx', [])):
        ins += ['-i', f"{A}/{s['name']}.wav"]; ms = int(max(0, s['t']) * 1000)
        fc.append(f"[{k + i}:a]aresample=48000,volume={GAIN[s['name']] + s.get('db', 0)}dB,adelay={ms}|{ms}[s{i}]"); labels.append(f'[s{i}]')
    fc.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{D}[mix]')
    pre = str(out_mp4).replace('.mp4', '_premix.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(fc), '-map', '[mix]', '-ac', '2', pre], check=True)
    L = f"I={loud['I']}:TP={loud['TP']}:LRA={loud['LRA']}"
    e = subprocess.run(['ffmpeg', '-nostats', '-i', pre, '-af', f'loudnorm={L}:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
    j = json.loads(e[e.rindex('{'):e.rindex('}') + 1])
    ln = (f"loudnorm={L}:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:"
          f"measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(video_in), '-i', pre, '-filter_complex', f'[1:a]{ln},aresample=48000[a]',
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', str(D), '-movflags', '+faststart', str(out_mp4)], check=True)
    return lufs(out_mp4)
