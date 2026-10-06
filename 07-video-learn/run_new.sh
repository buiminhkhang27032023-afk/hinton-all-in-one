#!/bin/bash
# sequential: frames+sheet, analyze (editing), for new-channel videos
export OMP_NUM_THREADS=2 ORT_THREADS=2
DIRS="tiktok-duyluandethuong tiktok-dinhhanai tiktok-leduyhiep.aihub youtube-VarunMayya youtube-JeffSu tiktokintl-tommythings tiktokintl-adam.digital tiktokintl-brandnat"
for pass in 1 2 3 4 5 6; do
for dd in $DIRS; do for f in /workspace/video-learn/$dd/*.mp4; do [ -f "$f" ] || continue
  d=$(dirname $f); id=$(basename $f .mp4); out=$d/frames/$id
  if [ ! -f $d/${id}_sheet.jpg ]; then mkdir -p $out/1fps $out/scene $out/hook
    nice ffmpeg -v error -y -i $f -vf "fps=1,scale=360:-2" -q:v 4 $out/1fps/%04d.jpg
    nice ffmpeg -v info -y -i $f -vf "select='gt(scene,0.3)',showinfo,scale=360:-2" -vsync vfr -q:v 4 $out/scene/%04d.jpg 2> $out/scene_log.txt
    grep -o 'pts_time:[0-9.]*' $out/scene_log.txt | cut -d: -f2 > $out/scene_times.txt
    nice ffmpeg -v error -y -t 3 -i $f -vf "fps=4,scale=360:-2" -q:v 4 $out/hook/%03d.jpg
    python3 /workspace/video-learn/sheet.py $out $d/${id}_sheet.jpg $d/${id}_hook.jpg && echo "SHEET $id"
  fi
  if [ ! -f $d/${id}_analysis.json ]; then nice /workspace/.cv-venv/bin/python /workspace/video-learn/tools/analyze.py $f 2>&1 | grep -E "^OK|Traceback|Error" | tail -2; fi
done; done
sleep 60
done
echo RUNNEW_DONE
