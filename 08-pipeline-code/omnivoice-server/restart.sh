#!/usr/bin/env bash
# Restart local OmniVoice server on 127.0.0.1:8123 (voice lock v2: male VN clone voice-lock-vn-v2.wav, since 2026-10-03; speed 1.2)
cd /workspace/omnivoice-server
pkill -f "uvicorn server:app --host 127.0.0.1 --port 8123" 2>/dev/null; sleep 1
source .venv/bin/activate
export OMNIVOICE_SPEED=${OMNIVOICE_SPEED:-1.2}
export OMNIVOICE_REF_AUDIO=${OMNIVOICE_REF_AUDIO:-/workspace/omnivoice-server/voice-lock-vn-v2.wav}
export OMNIVOICE_REF_TEXT=${OMNIVOICE_REF_TEXT:-/workspace/omnivoice-server/voice-lock-vn-v2.ref.txt}
# close inherited fds (e.g. the render lock fd from `flock ... restart.sh`) so uvicorn never holds the render lock
nohup bash -c 'for fd in /proc/$$/fd/*; do n=${fd##*/}; [ "$n" -gt 2 ] 2>/dev/null && eval "exec $n>&-"; done; exec uvicorn server:app --host 127.0.0.1 --port 8123' >> logs/server.log 2>&1 &
echo "started pid $!  (log: /workspace/omnivoice-server/logs/server.log)"
