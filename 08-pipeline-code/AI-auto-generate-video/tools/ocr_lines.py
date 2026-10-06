#!/usr/bin/env python3
"""OCR every text line of a screenshot -> JSON [{box:[x,y,w,h], text, conf}] (runs in /workspace/.cv-venv, rapidocr).
usage: /workspace/.cv-venv/bin/python ocr_lines.py image.png out.json [max_height_px]"""
import sys, json, cv2
from rapidocr_onnxruntime import RapidOCR
img = cv2.imread(sys.argv[1]); H = img.shape[0]; lim = int(sys.argv[3]) if len(sys.argv) > 3 else 99999
eng = RapidOCR(); out = []
for y0 in range(0, min(H, lim), 1400):  # tile tall pages so text stays large
    tile = img[y0:y0 + 1500]
    res, _ = eng(tile)
    for box, text, conf in res or []:
        xs = [p[0] for p in box]; ys = [p[1] + y0 for p in box]
        b = [int(min(xs)), int(min(ys)), int(max(xs) - min(xs)), int(max(ys) - min(ys))]
        if any(abs(b[1] - o['box'][1]) < 8 and abs(b[0] - o['box'][0]) < 8 for o in out): continue
        out.append({'box': b, 'text': text, 'conf': round(float(conf), 3)})
json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, indent=0); print(len(out), 'lines')
