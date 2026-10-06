#!/bin/bash
# analyze every mp4 lacking analysis.json; 2 parallel
cd /workspace/video-learn
export OMP_NUM_THREADS=2 ORT_THREADS=2
ls */*.mp4 | while read f; do id=$(basename "$f" .mp4); d=$(dirname "$f"); [ -f "$d/${id}_analysis.json" ] && [ "$1" != "force" ] && continue; [ -f "$d/${id}.mp4.part" ] && continue; echo "$f"; done | \
 xargs -P4 -I{} sh -c '/workspace/.cv-venv/bin/python tools/analyze.py "{}" 2>&1 | grep -E "^OK|Traceback|Error:" | tail -3'
echo RUNALL_DONE
