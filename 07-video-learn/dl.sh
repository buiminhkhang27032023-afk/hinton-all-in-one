#!/bin/bash
# usage: dl.sh <folder> <url>
Y=/workspace/.ytdlp-venv/bin/yt-dlp
mkdir -p "/workspace/video-learn/$1"
$Y -f "bv*[height<=1080]+ba/b[height<=1080]/b" --merge-output-format mp4 --match-filter "duration<=300" --no-playlist \
  -o "/workspace/video-learn/$1/%(id)s.%(ext)s" --write-info-json "$2"
