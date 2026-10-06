"""Procedural B-roll generators for the top half (1080x960, BGR numpy). Self-made graphics, no third-party assets.
Each fx(tl, dur, **kw) -> np.uint8 (960,1080,3). Text in Vietnamese with Be Vietnam Pro."""
import numpy as np, math
from PIL import Image, ImageDraw, ImageFont
G = '/usr/share/fonts/truetype/sand-box/google/'
BVP = G + 'Be Vietnam Pro/BeVietnamPro-Black.ttf'
BVPB = G + 'Be Vietnam Pro/BeVietnamPro-Bold.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
_fc = {}
def F(path, size):
    k = (path, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]
W, H = 1080, 960
YEL = (0xE0, 0xAC, 0x1A); RED = (0xE5, 0x39, 0x35); WHITE = (245, 245, 245)
def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def bg_dark(seed=0):
    im = Image.new('RGB', (W, H), (10, 10, 14)); d = ImageDraw.Draw(im)
    for x in range(60, W, 90):
        for y in range(60, H, 90): d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(40, 40, 48))
    return im, d
def to_bgr(im): return np.ascontiguousarray(np.asarray(im)[:, :, ::-1])
def ctext(d, y, s, font, fill, stroke=0):
    w = d.textlength(s, font=font); d.text(((W - w) / 2, y), s, font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))

def checklist(tl, dur, title='BÀI THỬ AN TOÀN', rows=('Trung thực', 'Xin phép trước khi làm', 'Dùng công cụ an toàn')):
    im, d = bg_dark(); ctext(d, 150, title, F(BVP, 70), YEL)
    for i, r in enumerate(rows):
        y = 330 + i * 150; a = ease((tl - 0.15 - i * 0.28) / 0.18)
        d.rounded_rectangle([140, y, 940, y + 112], 22, fill=(28, 28, 36), outline=(60, 60, 70), width=3)
        d.text((185, y + 26), r, font=F(BVPB, 50), fill=WHITE)
        if a > 0:
            cx, cy, s = 860, y + 56, 34 * (0.6 + 0.4 * a) * (1.15 if a < 1 else 1)
            d.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], fill=RED)
            d.line([cx - s * .6, cy - s * .6, cx + s * .6, cy + s * .6], fill=WHITE, width=11)
            d.line([cx - s * .6, cy + s * .6, cx + s * .6, cy - s * .6], fill=WHITE, width=11)
    return to_bgr(im)

def terminal(tl, dur, lines=('$ agent.run(task)', '> cần quyền truy cập...', '> CHƯA ĐƯỢC DUYỆT', '> vẫn tiếp tục...', '> vẫn tiếp tục...'), cps=38):
    im = Image.new('RGB', (W, H), (6, 8, 6)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([60, 110, 1020, 860], 26, fill=(16, 18, 20), outline=(70, 70, 80), width=3)
    for i, c in enumerate([(237, 106, 94), (245, 191, 79), (98, 197, 84)]): d.ellipse([100 + i * 44, 140, 128 + i * 44, 168], fill=c)
    n = int(tl * cps); y = 220; cur_x = 110; y += 112
    y -= 112
    for ln in lines:
        if n <= 0: break
        s = ln[:n]; n -= len(ln)
        col = RED if ('CHƯA' in ln or 'vẫn' in ln) else (120, 230, 120)
        d.text((110, y), s, font=F(MONO, 50), fill=col); y += 112
        cur_x = 110 + d.textlength(s, font=F(MONO, 50))
    if int(tl * 4) % 2 == 0: d.rectangle([cur_x + 6, y - 100, cur_x + 32, y - 46], fill=(120, 230, 120))
    return to_bgr(im)

def escape(tl, dur):
    im = Image.new('RGB', (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 170, 200, 790, 820
    d.text((x0, y0 - 90), 'SANDBOX', font=F(BVP, 56), fill=WHITE)
    d.line([x0, y0, x1, y0], fill=WHITE, width=6); d.line([x0, y1, x1, y1], fill=WHITE, width=6); d.line([x0, y0, x0, y1], fill=WHITE, width=6)
    gap = (470, 550); d.line([x1, y0, x1, gap[0]], fill=WHITE, width=6); d.line([x1, gap[1], x1, y1], fill=WHITE, width=6)
    for gx in range(5):
        for gy in range(5):
            cx = x0 + 70 + gx * 120; cy = y0 + 70 + gy * 120
            if (gx, gy) == (4, 2): continue
            d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=YEL)
    p = ease(tl / max(0.6, dur * 0.8)); sx, sy = x0 + 70 + 4 * 120, y0 + 70 + 2 * 120; ex = 1000
    cx = sx + (ex - sx) * p
    for k in range(12):
        tx = cx - k * 16
        if tx < sx: break
        r = 13 - k; d.ellipse([tx - r, sy - r, tx + r, sy + r], fill=(255, 80 - 5 * k, 60))
    d.ellipse([cx - 16, sy - 16, cx + 16, sy + 16], fill=RED, outline=WHITE, width=3)
    return to_bgr(im)

def killswitch(tl, dur):
    im, d = bg_dark(); cx, cy = 540, 430
    pressed = 0.25 < tl < 0.45; r = 220 * (0.92 if pressed else 1)
    d.ellipse([cx - 260, cy - 260, cx + 260, cy + 260], fill=(40, 40, 46))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 30, 36) if not pressed else (150, 20, 26), outline=(255, 120, 120), width=6)
    ctext(d, cy - 55, 'STOP', F(BVP, 100), WHITE)
    if tl > 0.45 and int(tl * 6) % 2 == 0: ctext(d, 760, 'KHÔNG PHẢN HỒI', F(BVP, 72), RED, stroke=4)
    return to_bgr(im)

FX = {'checklist': checklist, 'terminal': terminal, 'escape': escape, 'killswitch': killswitch}

def textcard(tl, dur, text='', sub=''):
    """Generic fallback: dark dot-grid card with a 1–3 word phrase popping in (yellow), optional sub line."""
    im, d = bg_dark(); f = F(BVP, 110)
    words = text.split(); lines = [' '.join(words[:3]), ' '.join(words[3:6])] if len(words) > 3 else [text]
    p = ease(tl / 0.18); sz = int(110 * (0.85 + 0.15 * p))
    while max(d.textlength(l, font=F(BVP, sz)) for l in lines) > 900 and sz > 50: sz -= 6
    y = 480 - len(lines) * sz * 0.6
    for i, l in enumerate(lines):
        ctext(d, y + i * sz * 1.15, l, F(BVP, sz), YEL if i == 0 else WHITE, stroke=4)
    if sub: ctext(d, 760, sub, F(BVPB, 44), (170, 170, 180))
    return to_bgr(im)

def dotgrid(tl, dur, n=9):
    """Kallaway-style animated yellow dot lattice (self-made): dots appear then lines connect."""
    im = Image.new('RGB', (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    step = 760 // (n - 1); x0 = (W - step * (n - 1)) // 2; y0 = (H - step * (n - 1)) // 2
    shown = int(n * n * ease(tl / max(0.5, dur * 0.6)))
    pts = [(x0 + (k % n) * step, y0 + (k // n) * step) for k in range(n * n)]
    if tl > dur * 0.5:
        a = ease((tl - dur * 0.5) / (dur * 0.4))
        for k, (x, y) in enumerate(pts):
            if k % n < n - 1: d.line([x, y, x + step * a, y], fill=(120, 100, 40), width=3)
            if k // n < n - 1: d.line([x, y, x, y + step * a], fill=(120, 100, 40), width=3)
    for k, (x, y) in enumerate(pts[:shown]): d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=YEL)
    return to_bgr(im)

FX.update({'textcard': textcard, 'dotgrid': dotgrid})
