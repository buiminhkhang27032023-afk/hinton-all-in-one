#!/usr/bin/env bash
# Cài pipeline AI-auto-generate-video trên máy mới (Linux x86_64, CPU).
# Yêu cầu: ffmpeg, uv, Node 22 (xem restore/install-all.sh), Google Chrome/Chromium headless do HyperFrames tự tải.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; cd "$HERE"
export PATH="$HOME/.local/bin:$PATH" HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1
node --version | grep -q '^v22' || { echo "Cần Node 22 (node --version hiện là $(node --version 2>/dev/null))"; exit 1; }
# 1) Node deps: hyperframes@0.8.114 + gsap (theo package-lock.json)
npm ci || npm install
# 2) Python 3.12 venv. Mặc định cài đúng phiên bản đã chạy (requirements.lock.txt); LOOSE=1 để dùng requirements.txt gọn.
uv venv --python 3.12 .venv
REQ=requirements.lock.txt; [[ "${LOOSE:-0}" == 1 ]] && REQ=requirements.txt
uv pip install --python .venv/bin/python --extra-index-url https://download.pytorch.org/whl/cpu --index-strategy unsafe-best-match -r "$REQ"
# 3) Tải trước model (cache HF): align VI + QA whisper small
.venv/bin/python - <<'PY'
from huggingface_hub import snapshot_download
for m in ["nguyenvulebinh/wav2vec2-base-vi-vlsp2020","Systran/faster-whisper-small"]:
    print("download", m); snapshot_download(m)
PY
# 4) Tạo thư mục job + file lock
mkdir -p /workspace/video-jobs && touch /workspace/video-jobs/.render.lock
echo "OK. Chạy thử: ./run.sh /workspace/video-jobs/TEST-pipeline-001"
