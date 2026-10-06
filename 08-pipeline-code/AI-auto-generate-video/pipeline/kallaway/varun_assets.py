"""Evidence fetching (prep, no lock) and cue -> shot resolution (render, inside lock) for preset varun.
Job inputs: script.txt with [HÌNH: …] cues, screenshot_urls.txt (name=…), broll_urls.txt (name=…), portraits.txt."""
import json, re, subprocess, time, urllib.parse, os
from pathlib import Path
from ..common import log, write_json
from ..common import find_input
from .. import text_vi
from . import cues as C

REPO = Path(__file__).resolve().parents[2]
YTDLP = '/workspace/.ytdlp-venv/bin/yt-dlp'
CVPY = '/workspace/.cv-venv/bin/python'
UA = 'HintonVideoBot/1.0 (educational news video)'

def _opts_lines(path):
    """'URL | k=v | k=v' lines -> list of (url, {k: v})"""
    out = []
    if path and path.exists():
        for l in path.read_text(encoding='utf-8').splitlines():
            l = l.strip()
            if not l or l.startswith('#'): continue
            parts = [p.strip() for p in l.split('|')]
            out.append((parts[0], dict(p.split('=', 1) for p in parts[1:] if '=' in p)))
    return out

def script_lines(job):
    raw = find_input(job, 'script.txt').read_text(encoding='utf-8')
    return C.parse_script(raw, text_vi.normalize)

# ------------------------------------------------------------------ prep: fetch everything the cues need
def fetch(job, cfg, d, notes):
    work = d['lam-viec']; lines = script_lines(job); items = [i for L in lines for i in L['items']]
    subs = []
    for i in items:
        subs.append(i)
        for k in ('top', 'bottom'):
            if isinstance(i['opt'].get(k), str): kd, _, rf = i['opt'][k].partition(':'); subs.append({'kind': kd, 'ref': rf, 'opt': {}, 'texts': []})
    # 1) official clips (yt-dlp with the node JS runtime fix) / direct media URLs
    yd = work / 'yt'; yd.mkdir(exist_ok=True)
    env = dict(os.environ, PATH=f"{Path.home()}/.local/bin:" + os.environ.get('PATH', ''))
    for url, o in _opts_lines(find_input(job, 'broll_urls.txt')):
        name = o.get('name') or re.sub(r'\W+', '_', url)[-40:]; dst = yd / f'{name}.mp4'
        if dst.exists(): continue
        if 'youtu' in url or 'x.com' in url or 'twitter.com' in url:
            cmd = [YTDLP, '--js-runtimes', 'node', '--remote-components', 'ejs:github', '-f', o.get('format', 'bv*[height<=720][vcodec^=avc1]/bv*[height<=720]/b[height<=720]'),
                   '--merge-output-format', 'mp4', '-o', str(dst)]
            if o.get('sections'): cmd += ['--download-sections', o['sections'], '--force-keyframes-at-cuts']
            r = subprocess.run(cmd + [url], capture_output=True, text=True, env=env, timeout=900)
        else:
            raw = yd / f'{name}.raw'; r = subprocess.run(['curl', '-sfL', '-A', UA, '-o', str(raw), url], capture_output=True, text=True, timeout=600)
            if raw.exists():  # direct mp4/webm, or a still image (png/webp/jpg -> 1-frame mp4, held by the reader; use mode=fit)
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-an', '-vf', "scale='trunc(min(1920,iw)/2)*2':-2", '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', str(dst)]); raw.unlink()
        notes.append(f'broll {name}: {"ok" if dst.exists() else "FAILED " + (r.stderr or "")[-160:]}'); log.info(notes[-1])
    # 2) portraits (Wikimedia Commons file title or direct URL), polite pacing to avoid API rate limits
    pd = work / 'portraits'; pd.mkdir(exist_ok=True)
    for name, o in [(u, o) for u, o in _opts_lines(find_input(job, 'portraits.txt'))]:
        nm, src = name, o.get('file') or o.get('url')
        dst = pd / f'{nm}.jpg'
        if dst.exists() or not src: continue
        url = src if src.startswith('http') else 'https://commons.wikimedia.org/wiki/Special:FilePath/' + urllib.parse.quote(src) + '?width=1400'
        subprocess.run(['curl', '-sfL', '-A', UA, '-o', str(dst), url], timeout=120); time.sleep(3)
        notes.append(f'portrait {nm}: {"ok" if dst.exists() and dst.stat().st_size > 5000 else "FAILED"}')
    # 3) PDB / AlphaFold DB structures for render:<id>
    dd = work / 'pdb'; dd.mkdir(exist_ok=True)
    for i in subs:
        if i['kind'] != 'render': continue
        pid = i['ref']; dst = dd / f'{pid}.pdb'
        if dst.exists(): continue
        if pid.upper().startswith('AF-'):
            for v in ('v6', 'v5', 'v4'):
                if subprocess.run(['curl', '-sf', '-o', str(dst), f'https://alphafold.ebi.ac.uk/files/{pid}-F1-model_{v}.pdb']).returncode == 0: break
        else: subprocess.run(['curl', '-sf', '-o', str(dst), f'https://files.rcsb.org/download/{pid}.pdb'])
        notes.append(f'pdb {pid}: {"ok" if dst.exists() else "FAILED"}')
    # 4) OCR of every captured page (for "find the key line" highlights)
    wd = work / 'webshots'; od = wd / 'ocr'; od.mkdir(parents=True, exist_ok=True)
    for i in subs:
        if i['kind'] in ('web', 'phone') and (wd / f"{i['ref']}.png").exists() and not (od / f"{i['ref']}.json").exists():
            subprocess.run([CVPY, str(REPO / 'tools' / 'ocr_lines.py'), str(wd / f"{i['ref']}.png"), str(od / f"{i['ref']}.json")], capture_output=True)
    missing = [f"{i['kind']}:{i['ref']}" for i in subs if i['kind'] in ('web', 'phone') and not (wd / f"{i['ref']}.png").exists()]
    if missing: notes.append(f'varun: missing screenshots {missing}'); log.warning(notes[-1])

# ------------------------------------------------------------------ render: cues -> beats
def _ensure_render(work, pid, o, dur):
    rd = work / 'renders'; rd.mkdir(exist_ok=True)
    style, color, bg = o.get('style', 'spacefill'), o.get('color', 'chain'), o.get('bg', 'dark')
    fill = float(o.get('fill', 1.0 if style == 'tube' else 1.05)); deg = float(o.get('deg', 55))
    out = rd / f'{pid}_{style}_{color}_{bg}_{fill:g}_{dur:.1f}.mp4'
    if not out.exists():
        subprocess.run([str(REPO / '.venv/bin/python'), str(REPO / 'tools/protein_render.py'), str(work / 'pdb' / f'{pid}.pdb'), str(out),
                        '--style', style, '--color', color, '--bg', bg, '--fill', str(fill), '--deg', str(deg), '--dur', f'{dur:.1f}'], check=True, capture_output=True)
    return str(out)

def _face_pos(path):
    import cv2
    from .. import presenter as PR
    im = cv2.imread(path); f = PR.detect_face([im])
    if not f: return [0.5, 0.3]
    h, w = im.shape[:2]; return [round((f[0] + f[2] / 2) / w, 3), round((f[1] + f[3] / 2) / h, 3)]

def _hl(texts):
    out = []
    for t in texts:
        st = 'marker'
        if '/' in t and t.rsplit('/', 1)[1] in ('marker', 'underline', 'box'): t, st = t.rsplit('/', 1)
        out.append({'find': t, 'style': st, 'at': 0.2 + 0.35 * len(out)})
    return out

PASS = ('ss', 'mode', 'zoom', 'cx', 'cy', 'focus', 'z1', 'z0', 'zr', 'zmin', 'zmax', 'crop_bottom', 'push', 'speed', 'seed', 'label', 'big', 'y', 'band', 'band_scale', 'band_focus', 'band_dy')

def shot_from_item(i, job, work, urls, brolls, portraits, dur):
    k, ref, o = i['kind'], i['ref'], i['opt']; s = {'type': k}
    s.update({p: o[p] for p in PASS if p in o})
    if 'seed' in s: s['seed'] = int(s['seed'])
    if k in ('web', 'phone'):
        s['src'] = str(work / 'webshots' / f'{ref}.png'); s['ocr'] = str(work / 'webshots' / 'ocr' / f'{ref}.json'); s['hl'] = _hl(i['texts'])
        u = o.get('url') or urls.get(ref, ''); s['url'] = re.sub(r'^https?://(www\.)?', '', u).split('?')[0][:70]
        s.setdefault('label', o.get('label') or (s['url'].split('/')[0] if k == 'web' else 'X'))
        s['credit'] = f'Screenshot {u}'
        if k == 'phone': s.setdefault('z1', 1500)
    elif k == 'photo':
        s['src'] = str(work / 'portraits' / f'{ref}.jpg'); s['face'] = o.get('face') or _face_pos(s['src'])
        nm, _, role = (i['texts'][0] if i['texts'] else ref).partition('|'); s['name'], s['role'] = nm.strip(), role.strip()
        s['credit'] = portraits.get(ref, {}).get('credit', 'Wikimedia Commons')
    elif k == 'clip':
        s['src'] = str(work / 'yt' / f'{ref}.mp4'); b = brolls.get(ref, ('', {}))
        s['credit'] = b[1].get('credit') or b[0]
    elif k == 'render':
        s['type'] = 'render'  # file=<mp4 relative to job> reuses an existing render, else tools/protein_render.py (cached in lam-viec/renders/)
        s['src'] = str(job / o['file']) if o.get('file') else _ensure_render(work, ref, o, max(2.4, dur + 0.4))
        s['credit'] = (f'AlphaFold DB {ref} (EMBL-EBI/Google DeepMind, CC BY 4.0)' if ref.upper().startswith('AF-') else f'PDB {ref} (RCSB)') + ', render tools/protein_render.py'
        s.setdefault('label', o.get('label') or ref)
    elif k == 'stat':
        if o.get('strike'): s['lines'] = [{'text': t, 'size': int(o.get('size', 150)), 'color': [235, 235, 235], 'strike': True, 'at': 0.25 * n} for n, t in enumerate(i['texts'])]
        else: s['lines'] = [({'text': t, 'size': int(o.get('size', 200)), 'color': [255, 255, 255], 'at': 0.25 * n} if n % 2 == 0 else
                             {'text': t, 'size': 76, 'color': [255, 196, 0], 'w': 'Bold', 'at': 0.25 * n - 0.05}) for n, t in enumerate(i['texts'])]
        s.setdefault('y', 640 if len(i['texts']) <= 2 else 420)
    elif k == 'face': pass
    elif k == 'split':
        halves = []
        for n, pos in enumerate(('top', 'bottom')):
            kd, _, rf = str(o[pos]).partition(':')
            txt = [i['texts'][n]] if len(i['texts']) > n and i['texts'][n] not in ('-', '') else []
            sub = shot_from_item({'kind': kd, 'ref': rf, 'opt': {kk[len(pos) + 1:]: v for kk, v in o.items() if kk.startswith(pos + '_')}, 'texts': txt},
                                 job, work, urls, brolls, portraits, dur)
            halves.append(sub)
        s['top'], s['bottom'] = halves; s.pop('label', None)
        s['credit'] = ' + '.join(h.get('credit', '') for h in halves)
    else: raise ValueError(f'unknown cue kind {k}')
    return s

def resolve(job, cfg, d, words, total):
    work = d['lam-viec']; lines = script_lines(job)
    seq = C.timeline(lines, words)
    urls = {o.get('name'): u for u, o in _opts_lines(find_input(job, 'screenshot_urls.txt')) if o.get('name')}
    brolls = {o.get('name'): (u, o) for u, o in _opts_lines(find_input(job, 'broll_urls.txt')) if o.get('name')}
    portraits = {u: o for u, o in _opts_lines(find_input(job, 'portraits.txt'))}
    shots = []
    for n, i in enumerate(seq):
        nxt = seq[n + 1]['t'] if n + 1 < len(seq) else total
        s = shot_from_item(i, job, work, urls, brolls, portraits, nxt - i['t']); s['at'] = i['t']; s['_line'] = i['line'][:60]; shots.append(s)
    title = [t.strip().upper() for t in (cfg.get('title') or '').split('|') if t.strip()]
    kc = cfg.get('varun', {})
    B = {'hook': {'t0': 0, 't1': kc.get('hook_hold', 1.94), 'lines': title[:2], 'top': 250, 'wipe': 0.5} if title else None, 'shots': shots,
         'lines': [{'text': L['text'], 'a': L['a'], 'b': L['b'], 'n_items': len(L['items'])} for L in lines]}
    write_json(work / 'varun_beats.auto.json', B)
    return B
