"""Entry point of the kallaway preset (called from pipeline.run inside the render lock)."""
import json, math, subprocess, sys
from pathlib import Path
from ..common import log, write_json, read_json, media_duration, REPO
from .. import presenter as PR
from . import autoplan, render as R, mix as M

ASSETS = REPO / 'assets' / 'kallaway'

def ensure_assets():
    if not (ASSETS / 'music.wav').exists():
        ASSETS.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, str(Path(__file__).parent / 'audio_assets.py'), str(ASSETS), '90', '120'], check=True)
    return ASSETS

def presenter_geom(src: Path, work: Path):
    import cv2
    pj = work / 'kallaway_presenter.json'; key = f'{src}|{src.stat().st_mtime}'
    if pj.exists() and read_json(pj).get('key') == key: return read_json(pj)
    crop = PR.cropdetect(src); L = media_duration(src)
    cap = cv2.VideoCapture(str(src)); W0, H0 = int(cap.get(3)), int(cap.get(4))
    cw, ch, cx, cy = [int(v) for v in crop.split(':')] if crop else (W0, H0, 0, 0)
    frames = []
    for i in range(10):
        cap.set(cv2.CAP_PROP_POS_MSEC, (i + 0.5) * L / 10 * 1000); ok, fr = cap.read()
        if ok: frames.append(fr[cy:cy + ch, cx:cx + cw])
    cap.release()
    face = PR.detect_face(frames) or [cw // 2 - cw // 8, ch // 4, cw // 4, cw // 4]
    g = {'key': key, 'pcrop': [cx, cy, cw, ch], 'face': face, 'length': L,
         'face_c': [face[0] + face[2] / 2, face[1] + face[3] / 2]}
    write_json(pj, g); return g

def build(job: Path, cfg, d, words, voice: Path, vdur, pools, notes):
    kc = cfg.setdefault('kallaway', {}); work = d['lam-viec']; fps = cfg['fps']
    total = math.ceil((vdur + kc.get('tail', 0.25)) * fps) / fps
    src = Path(cfg['presenter']['video']); g = presenter_geom(src, work); kc['_presenter_len'] = g['length']
    if cfg.get('preset') == 'varun':  # full-frame evidence preset (Varun Mayya grammar)
        from . import varun
        return varun.build(job, cfg, d, words, voice, vdur, pools, notes, g, total)
    fw = g['face'][2]; cw, ch = g['pcrop'][2], g['pcrop'][3]
    s_scale = max(kc.get('face_split_px', 270) / fw, 1080 / cw); f_scale = max(kc.get('face_full_px', 330) / fw, 1080 / cw, 1920 / ch)
    bj = job / 'beats.json' if (job / 'beats.json').exists() else job / 'source' / 'beats.json'
    if bj.exists():
        caps, segs, big, sfx, dips = autoplan.from_beats(json.loads(bj.read_text(encoding='utf-8')), words, total)
        for s in segs:  # relative image paths in beats.json are relative to the job dir
            b = s.get('broll') or {}
            if b.get('src') and not Path(b['src']).is_absolute(): b['src'] = str(job / b['src'])
        notes.append('kallaway: beats.json (manual beat list)')
    else:
        caps, segs, big, sfx, dips = autoplan.auto(words, total, pools, cfg, job)
        notes.append('kallaway: automatic beat list')
    for i, c in enumerate(caps):
        c['t0'] = round(c['s'], 3); c['t1'] = round(caps[i + 1]['s'] if i + 1 < len(caps) else total, 3)
    ensure_assets()
    title = [t.strip().upper() for t in (cfg.get('title') or '').split('|') if t.strip()]
    big_style = kc.get('bigword_style', {'font': 'bvp', 'size': 190, 'color': '#FFFFFF', 'glow': '#FFFFFF', 'cy': 1140})
    plan = {'presenter': str(src), 'pcrop': g['pcrop'], 'face_c': g['face_c'], 's_scale': round(s_scale, 4), 's_eye_y': kc.get('s_eye_y', 320),
            'f_scale': round(f_scale, 4), 'f_eye_y': 650, 'divider': 960, 'dur': total, 'crf': cfg['render'].get('crf', 18),
            'cap_style': kc.get('cap_style', {'font': 'fraunces', 'size': 50, 'color': '#E0AC1A', 'stroke': 5, 'top': 1008}),
            'captions': [{'t0': c['t0'], 't1': c['t1'], 'text': c['text']} for c in caps] if cfg.get('captions_burn') else [],
            'segments': segs, 'bigwords': [dict(big_style, **b) for b in big], 'sfx': sfx, 'music_dips': dips,
            'hook': ({'t0': 0, 't1': kc.get('hook_hold', 2.4), 'lines': title[:2], 'colors': ['#FFFFFF', '#E0AC1A'], 'wipe': 1.2,
                      'size': 96, 'maxw': 780, 'bottom': 952, 'glow': '#CF2C4E'} if title else None),
            'voice': str(voice), 'assets_dir': str(ASSETS), 'music_under': -cfg.get('bgm_volume_db', -20),
            'music': (cfg.get('bgm_path') or str(ASSETS / 'music.wav')) if cfg.get('bgm') else None,
            'video_out': str(d['render'] / 'video_noaudio.mp4')}
    write_json(work / 'kallaway_plan.json', plan)
    log.info('kallaway plan: %d shots (%d F), %d captions, %d bigwords, %d sfx, dips %s, total %.2fs',
             len(segs), sum(s['layout'] == 'F' for s in segs), len(plan['captions']), len(big), len(sfx), dips, total)
    R.render(plan)
    I = M.mix(plan, plan['video_out'], d['render'] / 'video.mp4', dict(cfg.get('loudness') or {}, TP=kc.get('tp', -2.0)))
    log.info('kallaway mix LUFS %.1f', I)
    shots = []
    for s in segs:
        b = s.get('broll') or {}
        vis = {'type': 'face' if s['layout'] == 'F' else b.get('type', 'fx'), 'kind': b.get('name', '')}
        if b.get('credit'): vis['credit'] = b['credit']
        shots.append({'start': s['t0'], 'end': s['t1'], 'dur': round(s['t1'] - s['t0'], 3), 'visual': vis})
    return {'total': total, 'hook_end': segs[1]['t0'] if len(segs) > 1 else total, 'outro_start': total, 'shots': shots}
