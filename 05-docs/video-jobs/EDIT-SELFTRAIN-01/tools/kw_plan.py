#!/usr/bin/env python3
"""Beat list -> render plan. Anchors everything (caption chunks, shot cuts, big words, sfx, music dips) to script
token indices, using word timings from kw_words.py.
Usage: kw_plan.py spec.json words.json plan.json"""
import sys, json
S, Wd, out = sys.argv[1:4]; S = json.load(open(S)); Wj = json.load(open(Wd)); words = Wj['words']
D = S.get('dur') or round(Wj['duration'] + S.get('tail', 0.1), 2)
st = lambda tok: 0.0 if tok == 0 else max(0.0, words[tok]['s'] - S.get('lead', 0.04))
# caption chunks: contiguous, each from first-token start to next chunk start
caps = []; tok = 0
for disp, n in S['chunks']:
    caps.append({'tok': tok, 'text': disp}); tok += n
assert tok == len(words), f'chunk tokens {tok} != words {len(words)}'
for i, c in enumerate(caps):
    c['t0'] = round(st(c['tok']), 3); c['t1'] = round(st(caps[i + 1]['tok']) if i + 1 < len(caps) else D, 3)
segs = []; ss = S.get('face_start', 3.0)
for i, sh in enumerate(S['shots']):
    t0 = st(sh['tok']); t1 = st(S['shots'][i + 1]['tok']) if i + 1 < len(S['shots']) else D
    seg = {k: v for k, v in sh.items() if k != 'tok'}; seg.update(t0=round(t0, 3), t1=round(t1, 3), face_ss=round(ss, 3))
    segs.append(seg); ss += (t1 - t0) + S.get('face_skip', 0.4)
    if ss > 50: ss = 2.0
big = []
for b in S.get('bigwords', []):
    t0 = st(b['tok']); end = next(s['t1'] for s in segs if s['t0'] <= t0 + 1e-3 < s['t1'])
    big.append(dict({k: v for k, v in b.items() if k != 'tok'}, t0=round(t0, 3), t1=round(min(end, t0 + b.get('max', 2.5)), 3)))
sfx = [{'name': x['name'], 't': round(x['t'] if 't' in x else st(x['tok']) + x.get('off', 0), 3), 'db': x.get('db', 0)} for x in S.get('sfx', [])]
dips = [[round(st(d['tok']) - d['len'], 3), round(st(d['tok']), 3)] for d in S.get('music_dips', [])]
plan = dict(S['base'], dur=D, captions=caps, segments=segs, bigwords=big, sfx=sfx, music_dips=dips, hook=S.get('hook'))
json.dump(plan, open(out, 'w'), ensure_ascii=False, indent=1)
sl = [s['t1'] - s['t0'] for s in segs]; print(f'dur {D}s shots {len(segs)} median {sorted(sl)[len(sl)//2]:.2f}s first cut {segs[1]["t0"] if len(segs)>1 else D}s; caps {len(caps)}')
