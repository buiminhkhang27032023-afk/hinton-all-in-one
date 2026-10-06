#!/usr/bin/env python3
"""Side-by-side: reference contact sheet (video-learn <id>_sheet.jpg) vs a 24-frame sheet of our video, labeled.
Usage: compare_sheet.py ref_sheet.jpg our.mp4 out.jpg "REF label" "OUR label" [n=24] [cols=8]"""
import sys, subprocess
from PIL import Image, ImageDraw, ImageFont
ref, vid, out, lr, lo = sys.argv[1:6]; n = int(sys.argv[6]) if len(sys.argv) > 6 else 24; cols = int(sys.argv[7]) if len(sys.argv) > 7 else 8
R = Image.open(ref).convert('RGB'); tw = R.width // cols; th = tw * 16 // 9
d = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', vid]))
rows = (n + cols - 1) // cols; S = Image.new('RGB', (tw * cols, (th + 14) * rows), 'white'); dr = ImageDraw.Draw(S)
for i in range(n):
    t = d * (i + 0.5) / n
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.2f}', '-i', vid, '-frames:v', '1', '-vf', f'scale={tw}:{th}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    if len(b) == tw * th * 3: S.paste(Image.frombytes('RGB', (tw, th), b), ((i % cols) * tw, (i // cols) * (th + 14)))
    dr.text(((i % cols) * tw + 2, (i // cols) * (th + 14) + th + 1), f't={t:.1f}s', fill='black')
H = max(R.height, S.height); f = ImageFont.truetype('/usr/share/fonts/truetype/sand-box/google/Be Vietnam Pro/BeVietnamPro-Bold.ttf', 30)
O = Image.new('RGB', (R.width + S.width + 30, H + 60), 'white'); d2 = ImageDraw.Draw(O)
d2.text((10, 12), lr, font=f, fill='black'); d2.text((R.width + 40, 12), lo, font=f, fill='black')
O.paste(R, (0, 60)); O.paste(S, (R.width + 30, 60)); O.save(out, quality=88); print(out)
