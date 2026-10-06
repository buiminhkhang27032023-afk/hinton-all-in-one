"""[HÌNH: …] visual cues in script.txt (preset varun).
Format: one spoken sentence per line, cue at the end of the line:
  Lần đầu tiên, AI góp phần mang về giải Nobel Hóa học. [HÌNH: clip:nobel_ann ss=104.5 mode=fit ; face @trí ; web:nobel_summary "Nobel Prize in Chemistry"/underline @góp]
Items are separated by ';'. Item = kind[:ref]  ["quoted text"[/style] ...]  [@word[#n]]  [key=value ...]
kinds: web:<shot> phone:<shot> photo:<portrait> clip:<broll> render:<PDB|AF-UNIPROT> stat face split(top=kind:ref bottom=kind:ref)
The cue text is stripped before TTS, so the voice cache (per sentence text) is unaffected."""
import re, shlex
from . import autoplan

CUE = re.compile(r'\[\s*H[ÌI]NH\s*:(.*?)\]', re.I | re.S)

def strip(raw):
    return CUE.sub(' ', raw)

def _val(v):
    if re.fullmatch(r'-?\d+(\.\d+)?', v): return float(v)
    if re.fullmatch(r'-?[\d.]+(,-?[\d.]+)+', v): return [float(x) for x in v.split(',')]
    return v

def parse_items(cue):
    lx = shlex.shlex(cue, posix=True, punctuation_chars=';'); lx.whitespace_split = True; lx.commenters = ''  # '#' = n-th occurrence in @word#n, not a comment
    toks = list(lx); items, cur = [], []
    for t in toks + [';']:
        if t == ';':
            if cur: items.append(cur)
            cur = []
        else: cur.append(t)
    out = []
    for it in items:
        head = it[0]; kind, _, ref = head.partition(':')
        d = {'kind': kind.lower(), 'ref': ref, 'texts': [], 'opt': {}}
        for t in it[1:]:
            if t.startswith('@'): d['anchor'] = t[1:]
            elif re.match(r'^[A-Za-z_][\w]*=', t): k, v = t.split('=', 1); d['opt'][k] = _val(v)
            else: d['texts'].append(t)
        out.append(d)
    return out

def parse_script(raw, normalize):
    """-> list of {text, items, a, b} (a/b = word-token range in the spoken text)."""
    lines = []; pos = 0
    for l in raw.replace('\r', '').split('\n'):
        if not l.strip() or l.strip().startswith('#'): continue
        cues = CUE.findall(l); text = normalize(strip(l))
        if not text: continue
        n = len(text.split()); items = [i for c in cues for i in parse_items(c)]
        lines.append({'text': text, 'items': items, 'a': pos, 'b': pos + n}); pos += n
    return lines

def anchor_time(words, a, b, anc):
    tok, _, nth = anc.partition('#'); hits = [k for k in range(a, b) if autoplan._n(words[k]['word']) == autoplan._n(tok)]
    if not hits: raise KeyError(f'cue anchor @{anc} not found in line "{" ".join(w["word"] for w in words[a:b])}"')
    return words[hits[int(nth or 1) - 1]]['start']

def timeline(lines, words):
    """attach a start time to every cue item (anchors, else evenly spread inside the line, snapped to word starts)."""
    seq = []
    for L in lines:
        a, b = L['a'], min(L['b'], len(words)); t_end = words[b]['start'] if b < len(words) else words[-1]['end']
        its = L['items']
        if not its: continue
        times = [anchor_time(words, a, b, i['anchor']) if i.get('anchor') else None for i in its]
        if times[0] is None: times[0] = words[a]['start']
        k = 0
        while k < len(its):
            if times[k] is None:
                j = k
                while j < len(its) and times[j] is None: j += 1
                t0 = times[k - 1]; t1 = times[j] if j < len(its) else t_end; n = j - k + 1
                starts = [w['start'] for w in words[a:b]]
                for m in range(k, j):
                    target = t0 + (t1 - t0) * (m - k + 1) / n
                    times[m] = min(starts, key=lambda s: abs(s - target))
                k = j
            k += 1
        for i, t in zip(its, times): i['t'] = round(t, 3); i['line'] = L['text']; seq.append(i)
    return seq
