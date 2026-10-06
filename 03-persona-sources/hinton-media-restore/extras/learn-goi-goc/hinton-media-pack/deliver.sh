#!/usr/bin/env bash
# deliver.sh <pipelineOutDir> <jobDir>  — copy deliverables per Hinton playbook + mobile 720p
set -e
S=$1; J=$2; O=$J/output
cp "$S/video.mp4" "$O/storytelling_final.mp4"
cp "$S/voice.wav" "$O/voice_storytelling.wav"
cp "$S/subtitle.srt" "$O/subtitle.srt"
cp "$S/script.json" "$J/lam-viec/script.json"; cp "$S/timings.json" "$J/lam-viec/timings.json"; cp "$S/script.txt" "$J/lam-viec/vo.txt"
ffmpeg -v error -y -i "$O/storytelling_final.mp4" -vf scale=720:1280 -c:v libx264 -crf 22 -preset medium -pix_fmt yuv420p -c:a copy -movflags +faststart "$O/storytelling_mobile_720p.mp4"
ls -la "$O"
