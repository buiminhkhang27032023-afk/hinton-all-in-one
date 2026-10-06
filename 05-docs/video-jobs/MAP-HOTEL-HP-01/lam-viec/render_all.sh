#!/usr/bin/env bash
# Run INSIDE flock /workspace/video-jobs/.render.lock
set -euo pipefail
L=/workspace/video-jobs/MAP-HOTEL-HP-01/lam-viec; J=$(dirname $L); O=$J/output
export PATH=/home/box/.local/bin:$PATH
HF=/workspace/AI-auto-generate-video/node_modules/.bin/hyperframes
echo "[$(date +%T)] align"; [ -f $L/voice/cues.json ] || /workspace/AI-auto-generate-video/.venv/bin/python $L/voice/align_cues.py
echo "[$(date +%T)] build"; cd $L/template && python3 build_hotel.py --out index.html
echo "[$(date +%T)] render"; mkdir -p $L/render
$HF render -c index.html -o $L/render/silent.mp4 --fps 30 --quality delivery --format mp4
echo "[$(date +%T)] mix"; python3 $L/audio/mix.py
echo "[$(date +%T)] mux"
ffmpeg -y -hide_banner -loglevel error -i $L/render/silent.mp4 -i $L/audio/mix.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart $O/storytelling_final.mp4
ffmpeg -y -hide_banner -loglevel error -i $O/storytelling_final.mp4 -vf scale=720:1280:flags=lanczos -c:v libx264 -preset slow -crf 22 -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart $O/storytelling_mobile_720p.mp4
cp $L/voice/voice_storytelling.wav $O/ ; cp $L/storytelling_script.txt $O/
echo "[$(date +%T)] DONE"
