#!/usr/bin/env bash
# Hinton short-video pipeline — one command per job.
#   ./run.sh /workspace/video-jobs/<job>            # prep (no lock) + render (inside render lock)
#   ./run.sh /workspace/video-jobs/<job> --force    # ignore alignment/presenter caches (TTS cache is per-sentence text)
#   STAGE=prep ./run.sh <job>   |   STAGE=render ./run.sh <job>
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JOB="$(realpath "${1:?usage: ./run.sh /workspace/video-jobs/<job> [--force]}")"; shift || true
LOCK=/workspace/video-jobs/.render.lock
export PATH="/home/box/.local/bin:$HERE/node_modules/.bin:$HERE/.venv/bin:$PATH"
export TZ=Asia/Ho_Chi_Minh HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-4}
PY="$HERE/.venv/bin/python"
cd "$HERE"
START=$(date +%s)
if [[ "${STAGE:-all}" != "render" ]]; then
  "$PY" -m pipeline.run prep "$JOB" "$@"
fi
if [[ "${STAGE:-all}" != "prep" ]]; then
  if ! flock -n "$LOCK" true; then echo "[run.sh] render lock busy — waiting (max ${LOCK_WAIT:-3600}s)…"; fi
  flock -w "${LOCK_WAIT:-3600}" "$LOCK" env HINTON_RENDER_LOCK_HELD=1 "$PY" -m pipeline.run render "$JOB" "$@"
fi
echo "[run.sh] done in $(( $(date +%s) - START ))s — ticket: $(cat "$(ls -t "$JOB"/qa/ticket.txt "$JOB"/qa/*/ticket.txt 2>/dev/null | head -1)" 2>/dev/null)"
