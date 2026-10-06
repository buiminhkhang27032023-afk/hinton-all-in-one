#!/usr/bin/env bash
# Tạo clip presenter giả (test-pattern 9:16, 20s, không tiếng) cho test nội bộ — KHÔNG BAO GIỜ giao khách.
set -e
OUT=${1:-/tmp/presenter_testpattern.mp4}
ffmpeg -v error -y -f lavfi -i "testsrc2=s=720x1280:r=30:d=20" -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='PRESENTER PLACEHOLDER':x=(w-tw)/2:y=h/3:fontsize=44:fontcolor=white:box=1:boxcolor=black@0.6" -pix_fmt yuv420p "$OUT"
echo "$OUT"
