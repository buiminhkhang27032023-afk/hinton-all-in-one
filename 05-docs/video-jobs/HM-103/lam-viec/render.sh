#!/bin/bash
set -e
cd /workspace/video-jobs/HM-103/lam-viec
export PATH=/home/box/.local/bin:$PATH HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1
curl -s http://127.0.0.1:8123/health > ../qa/omnivoice_health_at_render.json || true
/workspace/AI-auto-generate-video/node_modules/.bin/hyperframes render hf -o render/video.mp4 --fps 30 -q standard -w 4 --crf 18
echo RENDER_DONE
