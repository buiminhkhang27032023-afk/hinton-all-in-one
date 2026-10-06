#!/usr/bin/env python3
"""Kallaway-style compositor (split B-roll top / face bottom, full-face punch-ins, 2-word pop captions,
one big word, 2-line wipe hook title). Renders video only (no audio) at 1080x1920/30fps.
Run INSIDE the render lock:  flock /workspace/video-jobs/.render.lock /workspace/.cv-venv/bin/python kw_render.py plan.json
plan.json schema: see TEMPLATES.md (preset KALLAWAY-SPLIT)."""
import sys, json, subprocess, math, os
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kw_fx
P = json.load(open(sys.argv[1])); W, H, FPS = 1080, 1920, 30; DIV = P.get('divider', 960)
G = '/usr/share/fonts/truetype/sand-box/google/'
FONTS = {'fraunces': (G + 'Fraunces/Fraunces-VariableFont_SOFT,WONK,opsz,wght.ttf', 'Black'),
         'bvp': (G + 'Be Vietnam Pro/BeVietnamPro-Black.ttf', None),
         'script': (G + 'Dancing Script/DancingScript-VariableFont_wght.ttf', 'Bold')}
def font(name, size):
    p, var = FONTS[name]; f = ImageFont.truetype(p, size)
    if var: f.set_variation_by_name(var)
    return f
def hexc(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def ease_io(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)
def ease_o(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3

def text_rgba(text, fname, size, fill, stroke=6, glow=None, shadow=True):
    f = font(fname, size); pad = 40 + (30 if glow else 0)
    tmp = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    l, t, r, b = tmp.textbbox((0, 0), text, font=f, stroke_width=stroke)
    im = Image.new('RGBA', (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    org = (pad - l, pad - t)
    if glow:
        g = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).text(org, text, font=f, fill=hexc(glow) + (255,), stroke_width=stroke + 6)
        im = Image.alpha_composite(im, g.filter(ImageFilter.GaussianBlur(18))); d = ImageDraw.Draw(im)
    if shadow:
        s = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(s).text((org[0] + 3, org[1] + 5), text, font=f, fill=(0, 0, 0, 150), stroke_width=stroke)
        im = Image.alpha_composite(im, s.filter(ImageFilter.GaussianBlur(4))); d = ImageDraw.Draw(im)
    d.text(org, text, font=f, fill=hexc(fill) + (255,), stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    a = np.asarray(im).astype(np.float32); bb = Image.fromarray(a[:, :, 3].astype(np.uint8)).getbbox()
    a = a[bb[1]:bb[3], bb[0]:bb[2]]
    return np.ascontiguousarray(a[:, :, [2, 1, 0, 3]])  # BGRA float

def blend(dst, src, cx, top, scale=1.0, alpha=1.0, blur=0, clipx=None):
    if scale != 1.0:
        src = cv2.resize(src, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    if blur > 0.5:
        k = int(blur) * 2 + 1; src = cv2.GaussianBlur(src, (k, k), blur)
    h, w = src.shape[:2]; x0 = int(round(cx - w / 2)); y0 = int(round(top))
    if clipx is not None: w = max(0, min(w, int(clipx) - x0)); src = src[:, :w]
    xa, ya = max(0, x0), max(0, y0); xb, yb = min(dst.shape[1], x0 + w), min(dst.shape[0], y0 + h)
    if xb <= xa or yb <= ya: return (0, 0, 0, 0)
    s = src[ya - y0:yb - y0, xa - x0:xb - x0]; a = s[:, :, 3:4] / 255.0 * alpha
    roi = dst[ya:yb, xa:xb].astype(np.float32); dst[ya:yb, xa:xb] = (roi * (1 - a) + s[:, :, :3] * a).astype(np.uint8)
    return (xa, ya, xb, yb)

class FaceReader:
    def __init__(self, ss, n):
        cx, cy, cw, ch = P['pcrop']; self.w, self.h = cw, ch
        self.p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{ss:.3f}', '-i', P['presenter'], '-frames:v', str(n + 2),
                                   '-vf', f'crop={cw}:{ch}:{cx}:{cy},fps={FPS}', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
        self.last = None
    def read(self):
        b = self.p.stdout.read(self.w * self.h * 3)
        if len(b) == self.w * self.h * 3: self.last = np.frombuffer(b, np.uint8).reshape(self.h, self.w, 3)
        return self.last
    def close(self): self.p.stdout.close(); self.p.wait()

FC = P['face_c']
def face_warp(fr, s, out_w, out_h, cx, cy):
    M = np.float32([[s, 0, cx - s * FC[0]], [0, s, cy - s * FC[1]]])
    return cv2.warpAffine(fr, M, (out_w, out_h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

IMG = {}
def broll_frame(b, tl, dur):
    if b['type'] == 'fx': return kw_fx.FX[b['name']](tl, dur, **b.get('args', {}))
    if b['src'] not in IMG: IMG[b['src']] = cv2.imread(b['src'])
    src = IMG[b['src']]; e = ease_io(tl / dur)
    r = [b['r0'][i] + (b['r1'][i] - b['r0'][i]) * e for i in range(4)]
    s = 1080 / r[2]; rh = 960 / s; ry = r[1] + (r[3] - rh) / 2
    M = np.float32([[s, 0, -s * r[0]], [0, s, -s * ry]])
    out = cv2.warpAffine(src, M, (1080, 960), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    for k, hl in enumerate(b.get('hl', [])):  # animated yellow highlighter wipe
        p = ease_o((tl - hl.get('at', 0.2)) / 0.35)
        if p <= 0: continue
        x0, y0 = s * (hl['box'][0] - r[0]), s * (hl['box'][1] - ry); x1 = x0 + s * hl['box'][2] * p; y1 = y0 + s * hl['box'][3]
        xa, ya, xb, yb = [int(max(0, v)) for v in (x0, y0, min(1080, x1), min(960, y1))]
        if xb > xa and yb > ya:
            roi = out[ya:yb, xa:xb].astype(np.float32); col = np.array([26, 172, 224], np.float32)  # BGR #E0AC1A
            out[ya:yb, xa:xb] = (roi * (0.55 + 0.45 * col / 255)).astype(np.uint8)  # multiply blend
    return out

# ---------- pre-render text layers ----------
cs = P['cap_style']; CAP = {}
for c in P['captions']:
    if c['text'] not in CAP: CAP[c['text']] = text_rgba(c['text'], cs['font'], cs['size'], c.get('color', cs['color']), cs.get('stroke', 6))
BIG = [dict(b, img=text_rgba(b['text'], b.get('font', 'bvp'), b.get('size', 200), b.get('color', '#FFFFFF'), b.get('stroke', 0),
                              glow=b.get('glow', '#FFFFFF'), shadow=True)) for b in P.get('bigwords', [])]
hk = P.get('hook')
if hk:
    lines = hk['lines']; size = hk.get('size', 96)
    while True:
        f = font('bvp', size); tw = max(ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(l, font=f) for l in lines)
        if tw + 2 * 34 <= hk.get('maxw', 780) or size < 50: break
        size -= 4
    lh = int(size * 1.12); bw, bh = int(tw + 68), lh * len(lines) + 40
    lay = Image.new('RGBA', (bw + 120, bh + 120), (0, 0, 0, 0))
    glow = Image.new('RGBA', lay.size, (0, 0, 0, 0)); ImageDraw.Draw(glow).rounded_rectangle([60, 60, 60 + bw, 60 + bh], 22, fill=hexc(hk.get('glow', '#CF2C4E')) + (230,))
    lay = Image.alpha_composite(lay, glow.filter(ImageFilter.GaussianBlur(26)))
    d = ImageDraw.Draw(lay); d.rounded_rectangle([60, 60, 60 + bw, 60 + bh], 22, fill=(14, 8, 10, 235), outline=hexc(hk.get('glow', '#CF2C4E')) + (255,), width=4)
    for i, l in enumerate(lines):
        lw = d.textlength(l, font=f); col = hexc(hk.get('colors', ['#FFFFFF', '#FFFFFF'])[i])
        d.text((60 + (bw - lw) / 2, 60 + 14 + i * lh), l, font=f, fill=col + (255,))
    a = np.asarray(lay).astype(np.float32); HOOK = np.ascontiguousarray(a[:, :, [2, 1, 0, 3]])

# ---------- render ----------
D = P['dur']; NF = int(round(D * FPS))
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', P['video_out']], stdin=subprocess.PIPE)
segs = P['segments']; si = -1; reader = None
for fi in range(NF):
    t = fi / FPS
    while si + 1 < len(segs) and t >= segs[si + 1]['t0'] - 1e-6:
        si += 1; sg = segs[si]
        if reader: reader.close()
        reader = FaceReader(sg['face_ss'], int((sg['t1'] - sg['t0']) * FPS) + 2)
    sg = segs[si]; tl = t - sg['t0']; sd = sg['t1'] - sg['t0']
    fr = reader.read(); z = sg.get('zoom', 1.0) * (1 + sg.get('push', 0.027) * tl)
    if sg['layout'] == 'F':
        frame = face_warp(fr, P['f_scale'] * z, W, H, 540, P.get('f_eye_y', 650))
    else:
        frame = np.empty((H, W, 3), np.uint8)
        frame[:DIV] = broll_frame(sg['broll'], tl, sd)
        frame[DIV:] = face_warp(fr, P['s_scale'] * z, W, H - DIV, 540, P.get('s_eye_y', 308))
    # hook title (wipe reveal)
    if hk and hk['t0'] <= t < hk['t1']:
        h_, w_ = HOOK.shape[:2]; cx = 540; left = cx - w_ / 2
        reveal = left + w_ * ease_o((t - hk['t0']) / hk.get('wipe', 1.2))
        blend(frame, HOOK, cx, hk.get('bottom', 950) - h_ + 60, clipx=reveal)
    # big word
    bw_on = None
    for b in BIG:
        if b['t0'] <= t < b['t1']: bw_on = b
    if bw_on:
        k = (t - bw_on['t0']) * FPS; p = min(1, k / 6)
        blend(frame, bw_on['img'], 540, bw_on.get('cy', 1130) - bw_on['img'].shape[0] * (1.2 - 0.2 * p) / 2, scale=1.2 - 0.2 * ease_o(p), alpha=min(1, 0.3 + p), blur=8 * (1 - p))
    else:
        for c in P['captions']:
            if c['t0'] <= t < c['t1']:
                k = int(round((t - c['t0']) * FPS)); sc = [0.8, 0.94, 1.08, 1.04, 1.0][min(k, 4)]; al = [0.5, 1][min(k, 1)]
                img = CAP[c['text']]; top = cs['top'] + img.shape[0] * (1 - sc) / 2
                blend(frame, img, 540, top, scale=sc, alpha=al)
                break
    enc.stdin.write(frame.tobytes())
    if fi % 90 == 0: print(f'frame {fi}/{NF}', flush=True)
reader.close(); enc.stdin.close(); enc.wait(); print('done', P['video_out'])
