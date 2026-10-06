#!/usr/bin/env python3
"""Grid of frames at given times with labels. Usage: frames_grid.py video.mp4 out.jpg t1,t2,... [thumb_w=270] [cols=7]"""
import sys, subprocess, numpy as np
from PIL import Image, ImageDraw
v, out, ts = sys.argv[1:4]; tw = int(sys.argv[4]) if len(sys.argv) > 4 else 270; cols = int(sys.argv[5]) if len(sys.argv) > 5 else 7
ts = [float(x) for x in ts.split(',')]; th = tw * 16 // 9; ims = []
for t in ts:
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', v, '-frames:v', '1', '-vf', f'scale={tw}:{th}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    im = Image.frombytes('RGB', (tw, th), b) if len(b) == tw * th * 3 else Image.new('RGB', (tw, th))
    d = ImageDraw.Draw(im); d.rectangle([0, th - 22, 70, th], fill='white'); d.text((4, th - 18), f't={t:g}s', fill='black'); ims.append(im)
rows = (len(ims) + cols - 1) // cols; g = Image.new('RGB', (cols * tw, rows * th), 'white')
for i, im in enumerate(ims): g.paste(im, ((i % cols) * tw, (i // cols) * th))
g.save(out, quality=88); print(out)
