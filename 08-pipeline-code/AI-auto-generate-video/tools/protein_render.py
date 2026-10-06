#!/usr/bin/env python3
"""CPU 3D protein renderer -> rotating mp4 (no GPU/WebGL needed).
usage: protein_render.py in.pdb out.mp4 [--style spacefill|tube] [--color cpk|chain|rainbow|plddt|het]
                         [--dur 2.2] [--deg 50] [--bg dark|light|navy] [--w 1080 --h 1920] [--fill 0.82] [--tilt 15]
Spacefill = shaded atom spheres (painter's algorithm); tube = Catmull-Rom CA trace drawn as overlapping spheres.
pLDDT colouring uses the AlphaFold DB palette (B-factor column)."""
import argparse, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFilter

CPK = {'C': (144, 144, 144), 'N': (48, 80, 248), 'O': (255, 13, 13), 'S': (255, 200, 50), 'P': (255, 128, 0)}
VDW = {'C': 1.7, 'N': 1.55, 'O': 1.52, 'S': 1.8, 'P': 1.8}
CHAIN = [(66, 133, 244), (234, 67, 53), (251, 188, 5), (52, 168, 83), (171, 71, 188), (0, 172, 193), (255, 112, 67), (124, 179, 66)]
def plddt_col(b):
    return (0, 83, 214) if b > 90 else (101, 203, 243) if b > 70 else (255, 219, 19) if b > 50 else (255, 125, 69)
def rainbow(f):
    import colorsys; r, g, b = colorsys.hsv_to_rgb(0.68 * (1 - f), 0.75, 1.0); return (int(r * 255), int(g * 255), int(b * 255))

def parse(path, hetatm=True):
    A = []
    for l in open(path):
        if l.startswith('ATOM') or (hetatm and l.startswith('HETATM') and l[17:20] != 'HOH'):
            if l[16] not in ' A': continue
            el = (l[76:78].strip() or l[12:14].strip())[:1].upper()
            A.append(dict(x=float(l[30:38]), y=float(l[38:46]), z=float(l[46:54]), el=el, name=l[12:16].strip(), chain=l[21],
                          res=int(l[22:26]), b=float(l[60:66] or 0), het=l.startswith('HETATM'), resn=l[17:20]))
        if l.startswith('ENDMDL'): break
    return A

def sprite(r, col, light=True):
    s = max(3, int(r * 2 + 2)); y, x = np.mgrid[0:s, 0:s]; c = (s - 1) / 2
    d = np.sqrt((x - c) ** 2 + (y - c) ** 2) / (r + 1e-6); inside = d <= 1
    nz = np.sqrt(np.clip(1 - d ** 2, 0, 1)); nx = (x - c) / (r + 1e-6); ny = (y - c) / (r + 1e-6)
    L = np.array([-0.45, -0.55, 0.70]); L = L / np.linalg.norm(L)
    dif = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1); spec = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1) ** 28
    shade = 0.28 + 0.72 * dif; rim = 1 - 0.35 * (d ** 6)
    rgb = np.clip(np.array(col)[None, None, :] * (shade * rim)[..., None] + 255 * 0.55 * spec[..., None], 0, 255)
    a = np.clip((1 - d) * r * 1.5, 0, 1) * inside
    return Image.fromarray(np.dstack([rgb, a * 255]).astype(np.uint8), 'RGBA')

def catmull(P, n=6):
    out = []
    for i in range(len(P) - 1):
        p0, p1, p2, p3 = P[max(i - 1, 0)], P[i], P[i + 1], P[min(i + 2, len(P) - 1)]
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(P[-1]); return np.array(out)

def build(A, style, color):
    chains = sorted({a['chain'] for a in A}); pts, cols, rad = [], [], []
    if style == 'spacefill':
        for a in A:
            if color == 'cpk' or (color == 'het' and a['het']): c = CPK.get(a['el'], (200, 200, 200))
            elif color == 'het': c = (230, 230, 235) if a['resn'] not in ('DA', 'DT', 'DG', 'DC') else (255, 170, 60)
            elif color == 'plddt': c = plddt_col(a['b'])
            else: c = CHAIN[chains.index(a['chain']) % len(CHAIN)]
            if color == 'chain' and a['resn'] in ('DA', 'DT', 'DG', 'DC'): c = (245, 245, 245) if a['chain'] in chains[-2:] else c
            pts.append((a['x'], a['y'], a['z'])); cols.append(c); rad.append(VDW.get(a['el'], 1.7))
    else:
        for ch in chains:
            ca = [a for a in A if a['chain'] == ch and a['name'] in ('CA', 'P') and not a['het']]
            if len(ca) < 4: continue
            P = np.array([(a['x'], a['y'], a['z']) for a in ca]); S = catmull(P, 7); bs = np.repeat([a['b'] for a in ca], 7)[:len(S)]
            for k, p in enumerate(S):
                f = k / max(1, len(S) - 1)
                c = plddt_col(bs[min(k, len(bs) - 1)]) if color == 'plddt' else rainbow(f) if color == 'rainbow' else CHAIN[chains.index(ch) % len(CHAIN)]
                pts.append(tuple(p)); cols.append(c); rad.append(1.9 if ca[0]['name'] == 'CA' else 2.6)
        het = [a for a in A if a['het']]
        for a in het: pts.append((a['x'], a['y'], a['z'])); cols.append(CPK.get(a['el'], (200, 200, 200))); rad.append(VDW.get(a['el'], 1.7))
    P = np.array(pts); P -= P.mean(0); return P, cols, np.array(rad)

def rot(deg_y, deg_x):
    a, b = np.radians(deg_y), np.radians(deg_x)
    Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
    Rx = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]); return Rx @ Ry

def background(W, H, kind):
    y = np.linspace(0, 1, H)[:, None, None]
    top, bot = {'dark': ((18, 20, 28), (4, 5, 9)), 'light': ((250, 250, 252), (222, 226, 234)), 'navy': ((16, 36, 84), (4, 10, 30))}[kind]
    g = np.array(top) * (1 - y) + np.array(bot) * y; img = np.broadcast_to(g, (H, W, 3)).astype(np.uint8)
    im = Image.fromarray(img.copy()); return im

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('pdb'); ap.add_argument('out')
    ap.add_argument('--style', default='spacefill'); ap.add_argument('--color', default='chain'); ap.add_argument('--dur', type=float, default=2.2)
    ap.add_argument('--deg', type=float, default=50); ap.add_argument('--bg', default='dark'); ap.add_argument('--w', type=int, default=1080)
    ap.add_argument('--h', type=int, default=1920); ap.add_argument('--fill', type=float, default=0.82); ap.add_argument('--tilt', type=float, default=15)
    ap.add_argument('--start', type=float, default=0); ap.add_argument('--fps', type=int, default=30); ap.add_argument('--cy', type=float, default=0.47)
    a = ap.parse_args()
    P, cols, rad = build(parse(a.pdb), a.style, a.color)
    ext = max(np.linalg.norm(P, axis=1).max() + rad.max(), 1); scale = a.fill * min(a.w, a.h * 0.62) / (2 * ext)
    bg = background(a.w, a.h, a.bg); n = int(a.dur * a.fps); cache = {}
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{a.w}x{a.h}', '-r', str(a.fps), '-i', '-',
                            '-c:v', 'libx264', '-crf', '18', '-preset', 'fast', '-pix_fmt', 'yuv420p', a.out], stdin=subprocess.PIPE)
    for f in range(n):
        R = rot(a.start + a.deg * f / max(1, n - 1), a.tilt); Q = P @ R.T
        zoom = 1 + 0.04 * f / max(1, n - 1)
        order = np.argsort(Q[:, 2]); im = bg.copy()
        zmin, zmax = Q[:, 2].min(), Q[:, 2].max()
        for i in order:
            fog = 0.55 + 0.45 * (Q[i, 2] - zmin) / (zmax - zmin + 1e-6)
            r = rad[i] * scale * zoom; key = (int(r * 2) / 2, tuple(int(c * fog) // 6 * 6 for c in cols[i]))
            if key not in cache: cache[key] = sprite(key[0], key[1])
            sp = cache[key]; x = a.w / 2 + Q[i, 0] * scale * zoom - sp.size[0] / 2; y = a.h * a.cy - Q[i, 1] * scale * zoom - sp.size[1] / 2
            im.alpha_composite(sp, (int(x), int(y))) if im.mode == 'RGBA' else im.paste(sp, (int(x), int(y)), sp)
        enc.stdin.write(im.convert('RGB').tobytes())
    enc.stdin.close(); enc.wait(); print('ok', a.out, len(P), 'spheres')
if __name__ == '__main__': main()
