#!/bin/bash
# extract 1fps + scene frames + contact sheets for each mp4
for f in $(find /workspace/video-learn -name '*.mp4' | sort); do
  d=$(dirname $f); id=$(basename $f .mp4); out=$d/frames/$id; mkdir -p $out/1fps $out/scene
  [ -f $d/${id}_sheet.jpg ] && continue
  nice ffmpeg -v error -y -i $f -vf "fps=1,scale=360:-2" -q:v 4 $out/1fps/%04d.jpg
  nice ffmpeg -v info -y -i $f -vf "select='gt(scene,0.3)',showinfo,scale=360:-2" -vsync vfr -q:v 4 $out/scene/%04d.jpg 2> $out/scene_log.txt
  grep -o 'pts_time:[0-9.]*' $out/scene_log.txt | cut -d: -f2 > $out/scene_times.txt
  # hook frames 0-3s every 0.25s
  mkdir -p $out/hook; nice ffmpeg -v error -y -t 3 -i $f -vf "fps=4,scale=360:-2" -q:v 4 $out/hook/%03d.jpg
  python3 /workspace/video-learn/sheet.py $out $d/${id}_sheet.jpg $d/${id}_hook.jpg
done
