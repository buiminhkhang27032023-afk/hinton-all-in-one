#!/usr/bin/env bash
# Cài OmniVoice server (k2-fsa/OmniVoice, CPU) tại /workspace/omnivoice-server, cổng 127.0.0.1:8123.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; cd "$HERE"
[[ "$HERE" == /workspace/omnivoice-server ]] || echo "CẢNH BÁO: restart.sh + config pipeline trỏ cứng /workspace/omnivoice-server — nên giải nén đúng đường dẫn đó."
uv venv --python 3.13 .venv
REQ=requirements.lock.txt; [[ "${LOOSE:-0}" == 1 ]] && REQ=requirements.txt
uv pip install --python .venv/bin/python --extra-index-url https://download.pytorch.org/whl/cpu --index-strategy unsafe-best-match -r "$REQ"
mkdir -p logs
# tải model trước (~vài GB, cache ~/.cache/huggingface)
.venv/bin/python -c "from huggingface_hub import snapshot_download; snapshot_download('k2-fsa/OmniVoice')"
echo "OK. Khởi động: flock -o /workspace/video-jobs/.render.lock ./restart.sh ; kiểm tra: curl -s 127.0.0.1:8123/health"
