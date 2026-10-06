#!/usr/bin/env python3
"""24-frame contact sheets (evenly spaced, 4x6) of a reference video and ours, side by side with labels.
usage: sheet24_compare.py ref.mp4 our.mp4 out.jpg "REF label" "OUR label" """
import sys, cv2, numpy as np
def sheet(path, label, tw=180, th=320, cols=6, n=24):
    cap = cv2.VideoCapture(path); dur = cap.get(7) / cap.get(5); tiles = []
    for i in range(n):
        t = (i + 0.5) * dur / n; cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, f = cap.read()
        f = cv2.resize(f, (tw, th)) if ok else np.zeros((th, tw, 3), np.uint8)
        cv2.rectangle(f, (0, th - 22), (52, th), (0, 0, 0), -1); cv2.putText(f, f'{t:.1f}s', (3, th - 6), 0, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
        tiles.append(cv2.copyMakeBorder(f, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=(40, 40, 40)))
    g = np.vstack([np.hstack(tiles[r * cols:(r + 1) * cols]) for r in range(n // cols)])
    head = np.full((70, g.shape[1], 3), 20, np.uint8); cv2.putText(head, label, (12, 46), 0, 1.0, (255, 255, 255), 2, cv2.LINE_AA)
    return np.vstack([head, g])
a = sheet(sys.argv[1], sys.argv[4]); b = sheet(sys.argv[2], sys.argv[5])
gap = np.full((a.shape[0], 24, 3), 255, np.uint8)
cv2.imwrite(sys.argv[3], np.hstack([a, gap, b]), [cv2.IMWRITE_JPEG_QUALITY, 88]); print(sys.argv[3])
