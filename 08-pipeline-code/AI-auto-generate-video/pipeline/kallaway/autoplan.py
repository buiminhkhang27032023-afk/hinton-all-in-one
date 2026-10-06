"""Beat list for the kallaway preset. Two modes:
 - beats.json in the job (token-anchored shots/bigwords/sfx/dips, like EDIT-SELFTRAIN-01) -> exact control;
 - automatic: shots ~shot_target s cut on word starts (sentence starts preferred), full-face punch + big word every
   ~punch_every s, B-roll cycled demo clip -> screenshot Ken Burns -> fx fallback, loop ending, sfx map, music dip.
Optional job files: bigwords.txt (one phrase per line, 'spoken phrase => DISPLAY'), caption_map.txt
('spoken phrase => display', e.g. 'năm hai nghìn không trăm hai mươi bốn => năm 2024')."""
import math, re, unicodedata
from ..text_vi import salient_phrase

def _n(w): return re.sub(r'[^\w]', '', unicodedata.normalize('NFC', w.lower()))
PUNCT_END = re.compile(r'[.!?…]$'); PUNCT_SOFT = re.compile(r'[,;:]$')
REVEAL = ('nhưng', 'tệ hơn', 'cho tới', 'thế nhưng', 'vì sao', 'bài học', 'điều đáng nói', 'và đó')

def parse_map(path):
    out = []
    if path and path.exists():
        for l in path.read_text(encoding='utf-8').splitlines():
            l = l.strip()
            if not l or l.startswith('#'): continue
            a, b = (l.split('=>', 1) + [None])[:2]
            a = a.strip(); out.append(([_n(x) for x in a.split()], (b or a).strip()))
    return out

def find_seq(words, toks, start=0):
    n = len(toks)
    for i in range(start, len(words) - n + 1):
        if all(_n(words[i + k]['word']) == toks[k] for k in range(n)): return i
    return -1

def chunks_from_words(words, cmap, per=2):
    items = []; i = 0  # merge caption_map sequences into single display tokens
    while i < len(words):
        hit = None
        for toks, disp in cmap:
            if toks and find_seq(words[i:i + len(toks)], toks) == 0:
                hit = (len(toks), disp); break
        if hit:
            n, disp = hit; tail = words[i + n - 1]['word']; p = tail[-1] if tail[-1] in '.,!?…;:' and disp[-1] not in '.,!?…;:' else ''
            items.append({'text': disp + p, 's': words[i]['start'], 'e': words[i + n - 1]['end'], 'tok': i, 'atom': True}); i += n
        else:
            items.append({'text': words[i]['word'], 's': words[i]['start'], 'e': words[i]['end'], 'tok': i, 'atom': False}); i += 1
    caps = []; cur = []
    for it in items:
        if it['atom'] and cur: caps.append(cur); cur = []
        cur.append(it)
        if it['atom'] or len(cur) >= per or PUNCT_END.search(it['text']) or PUNCT_SOFT.search(it['text']):
            caps.append(cur); cur = []
    if cur: caps.append(cur)
    return [{'text': ' '.join(x['text'] for x in c), 's': c[0]['s'], 'tok': c[0]['tok']} for c in caps]

def cut_points(words, total, target, cmin, cmax, first=None):
    starts = [w['start'] for w in words]; sent_st = {w['start'] for k, w in enumerate(words) if k == 0 or words[k - 1]['sent'] != w['sent']}
    cuts = [0.0]; cur = 0.0
    while total - cur > cmax:
        tg = first if (first and cur == 0.0) else target
        cand = [s for s in starts if cur + cmin <= s <= cur + cmax]
        if not cand: cur += tg; cuts.append(round(cur, 3)); continue
        sc = [s for s in cand if s in sent_st and abs(s - (cur + tg)) < 0.7]
        nxt = min(sc or cand, key=lambda s: abs(s - (cur + tg)))
        cuts.append(nxt); cur = nxt
    if total - cuts[-1] < cmin and len(cuts) > 1: cuts.pop()
    return cuts

def screenshot_regions(path, k):
    import cv2
    im = cv2.imread(str(path)); h, w = im.shape[:2]; a = 960 / 1080
    v = k % 3
    if v == 0: return [0, 0, w, w * a], [w * 0.12, h * 0.04, w * 0.72, w * 0.72 * a]
    if v == 1: return [w * 0.05, h * 0.18, w * 0.8, w * 0.8 * a], [w * 0.05, h * 0.30, w * 0.75, w * 0.75 * a]
    return [w * 0.15, h * 0.10, w * 0.62, w * 0.62 * a], [0, h * 0.06, w, w * a]

def auto(words, total, pools, cfg, job):
    kc = cfg.get('kallaway', {})
    cmap = parse_map(job / 'caption_map.txt' if (job / 'caption_map.txt').exists() else job / 'source' / 'caption_map.txt')
    bmap = parse_map(job / 'bigwords.txt' if (job / 'bigwords.txt').exists() else job / 'source' / 'bigwords.txt')
    caps = chunks_from_words(words, cmap, kc.get('caption_words', 2))
    cuts = cut_points(words, total, kc.get('shot_target', 1.7), kc.get('shot_min', 0.9), kc.get('shot_max', 3.2), kc.get('first_cut', 1.3))
    # big-word anchors: force a cut on the anchor word so the punch-in + big word land together, hold >= f_hold s
    anchors = []
    for toks, disp in bmap:
        i = find_seq(words, toks)
        if i >= 0: anchors.append((round(max(0.0, words[i]['start'] - 0.04), 3), disp))
    anchors.sort(); hold = kc.get('f_hold', 1.3)
    for t, _ in anchors:
        if t < 1.0 or t > total - hold - 0.5: continue
        cuts = [c for c in cuts if not (t - 0.6 < c < t + hold)] + [t]
        cuts.sort()
    bounds = list(zip(cuts, cuts[1:] + [total]))
    layout = ['S'] * len(bounds); big = []; lastF = -99; every = kc.get('punch_every', 6.5)
    for j, (a, b) in enumerate(bounds):
        if j == 0 or j == len(bounds) - 1: continue
        if a - lastF < every * 0.7: continue
        hit = next(((t, d) for t, d in anchors if a - 0.05 <= t < b - 0.3), None)
        if not hit and not anchors and a - lastF >= every:
            ws = [w for w in words if a <= w['start'] < b]
            if ws:
                pick = max(ws, key=lambda w: (bool(re.search(r'\d', w['word'])) * 3 + w['word'][:1].isupper() * 2 + len(_n(w['word'])) / 4))
                hit = (pick['start'], _n(pick['word']).upper())
        if hit:
            layout[j] = 'F'; lastF = b; big.append({'t0': round(hit[0], 3), 't1': round(min(b, hit[0] + 2.5), 3), 'text': hit[1]})
    # B-roll cycle
    skip = set(kc.get('skip_demo', []))  # indices of demo clips with burnt-in text/title cards
    trim = {int(k): float(v) for k, v in kc.get('demo_trim', {}).items()}  # idx -> seconds to skip at clip head
    demo = [dict(c, start=c['start'] + trim.get(i, 0), dur=c['dur'] - trim.get(i, 0)) for i, c in enumerate(pools.get('demo', [])) if i not in skip]; shots = list(pools.get('screenshots', [])); di = si = fxi = 0
    first_broll = None
    if kc.get('first_broll'):  # key visual for shot 1 (and the loop shot)
        import cv2
        fb = kc['first_broll']; h, w = cv2.imread(fb).shape[:2]; a = 960 / 1080
        first_broll = {'type': 'image', 'src': fb, 'r0': [0, max(0, (h - w * a) / 2), w, w * a], 'r1': [w * 0.06, max(0, (h - w * a) / 2) + w * a * 0.06, w * 0.88, w * a * 0.88]}
    order = kc.get('broll_order', ['demo', 'shot', 'demo', 'shot', 'fx'])
    segs = []; oi = 0; ss = kc.get('face_start', 3.0); plen = kc.get('_presenter_len', 50)
    for j, (a, b) in enumerate(bounds):
        seg = {'t0': round(a, 3), 't1': round(b, 3), 'layout': layout[j], 'face_ss': round(ss, 3)}
        ss += (b - a) + 0.4
        if ss > plen - 3: ss = 1.0
        if layout[j] == 'F':
            seg.update(zoom=1.15 if len([s for s in segs if s['layout'] == 'F']) % 2 == 0 else 1.2, push=0.03)
        elif (j == len(bounds) - 1 and first_broll and kc.get('loop', True)) or (j == 0 and first_broll):
            seg['broll'] = dict(first_broll)
        else:
            br = None
            for _ in range(len(order)):
                kind = order[oi % len(order)]; oi += 1
                if kind == 'demo' and demo:
                    c = demo[di % len(demo)]; di += 1
                    br = {'type': 'video', 'src': c['src'], 'start': c['start'], 'credit': c.get('credit')}; break
                if kind == 'shot' and shots:
                    r0, r1 = screenshot_regions(shots[si % len(shots)], si // max(1, len(shots)) + si); 
                    br = {'type': 'image', 'src': shots[si % len(shots)], 'r0': r0, 'r1': r1}; si += 1; break
                if kind == 'fx':
                    cs_ = [c['text'] for c in caps if a - 0.05 <= c['s'] < b]
                    key = [c for c in cs_ if re.search(r'\d|[A-ZĐ]', c[1:] if c[:1].isupper() else c)] or sorted(cs_, key=len, reverse=True)
                    phrase = (key[0] if key else salient_phrase([w['word'] for w in words if a <= w['start'] < b], 3)).strip(' ,.;:?!').upper()
                    br = {'type': 'fx', 'name': 'textcard', 'args': {'text': phrase}} if fxi % 2 == 0 else {'type': 'fx', 'name': 'dotgrid'}
                    fxi += 1; break
            if br is None: br = {'type': 'fx', 'name': 'dotgrid'}
            seg['broll'] = br
            if first_broll is None: first_broll = br
        segs.append(seg)
    # sfx map
    sfx = [{'name': 'whoosh', 't': 0.0}]
    for j, s in enumerate(segs[1:], 1):
        if s['layout'] == 'F': sfx.append({'name': 'whoosh', 't': max(0, s['t0'] - 0.12)})
        elif s.get('broll', {}).get('type') == 'fx' and s['broll'].get('name') == 'dotgrid': sfx.append({'name': 'scan', 't': s['t0']})
        elif j % 4 == 0 and segs[j - 1]['layout'] == 'S': sfx.append({'name': 'pop', 't': s['t0']})
    for bw in big: sfx.append({'name': 'hit', 't': bw['t0']})
    dips = []
    for k, w in enumerate(words):
        if w['start'] > 4 and (k == 0 or words[k - 1]['sent'] != w['sent']):
            head = ' '.join(_n(x['word']) for x in words[k:k + 3])
            if any(head.startswith(r) for r in REVEAL): dips.append([round(float(w['start']) - 0.6, 3), round(float(w['start']), 3)]); break
    return caps, segs, big, sfx, dips

def from_beats(B, words, total):
    st = lambda tok: 0.0 if tok == 0 else max(0.0, words[tok]['start'] - B.get('lead', 0.04))
    caps = []; tok = 0
    for disp, n in B['chunks']:
        caps.append({'text': disp, 's': st(tok), 'tok': tok}); tok += n
    if tok != len(words): raise SystemExit(f'beats.json chunks cover {tok} tokens, script has {len(words)}')
    segs = []; ss = B.get('face_start', 3.0)
    for i, sh in enumerate(B['shots']):
        a = st(sh['tok']); b = st(B['shots'][i + 1]['tok']) if i + 1 < len(B['shots']) else total
        seg = {k: v for k, v in sh.items() if k != 'tok'}; seg.update(t0=round(a, 3), t1=round(b, 3), face_ss=round(ss, 3)); segs.append(seg)
        ss += (b - a) + B.get('face_skip', 0.4)
    big = []
    for bw in B.get('bigwords', []):
        a = st(bw['tok']); end = next(s['t1'] for s in segs if s['t0'] <= a + 1e-3 < s['t1'])
        big.append(dict({k: v for k, v in bw.items() if k != 'tok'}, t0=round(a, 3), t1=round(min(end, a + bw.get('max', 2.5)), 3)))
    sfx = [{'name': x['name'], 't': round(x['t'] if 't' in x else st(x['tok']) + x.get('off', 0), 3), 'db': x.get('db', 0)} for x in B.get('sfx', [])]
    dips = [[round(st(d['tok']) - d['len'], 3), round(st(d['tok']), 3)] for d in B.get('music_dips', [])]
    return caps, segs, big, sfx, dips
