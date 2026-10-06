#!/usr/bin/env bash
# Mix VO + ducked BGM (~-20 dB) trimmed to voice length + tail, soft fades.
# Usage: ./mix_duck.sh voice.wav bgm.wav out.wav [bgm_db=-20] [tail_sec=2.5]
set -euo pipefail
VOICE="${1:?voice wav}"
BGM="${2:?bgm wav}"
OUT="${3:?out wav}"
BGM_DB="${4:--20}"
TAIL="${5:-2.5}"
DUR=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$VOICE")
TOTAL=$(python3 -c "print(float('$DUR')+float('$TAIL'))")
FADE_OUT=$(python3 -c "print(max(1.0, float('$TAIL')))")
FADE_START=$(python3 -c "print(max(0.0, float('$TOTAL')-float('$FADE_OUT')))")
ffmpeg -y -i "$VOICE" -stream_loop -1 -i "$BGM" -t "$TOTAL" -filter_complex \
  "[1:a]atrim=0:${TOTAL},afade=t=in:st=0:d=1.2,afade=t=out:st=${FADE_START}:d=${FADE_OUT},volume=${BGM_DB}dB[bg];\
   [bg][0:a]sidechaincompress=threshold=0.02:ratio=8:attack=50:release=400:level_sc=0.8[ducked];\
   [0:a]apad=pad_dur=${TAIL}[vo];\
   [vo][ducked]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
  -map "[a]" -ar 48000 -ac 2 -c:a pcm_s16le "$OUT"
echo "Wrote $OUT (VO+${TAIL}s tail, BGM ducked ${BGM_DB}dB, loudnorm~-14)"
