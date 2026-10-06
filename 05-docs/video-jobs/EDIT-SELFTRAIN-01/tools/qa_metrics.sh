#!/usr/bin/env bash
# qa_metrics.sh video.mp4 — cuts/min @0.3/0.2, median shot, first cut, LUFS/TP, pauses>=0.25s, size/fps/dur
V=$1
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
for th in 0.3 0.2; do
  ffmpeg -v info -i "$V" -vf "scale=192:-2,select='gte(scene,$th)',showinfo" -f null - 2>&1 | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 > /tmp/cuts_$th.txt
  python3 - "$D" "$th" <<'PY'
import sys; D=float(sys.argv[1]); th=sys.argv[2]; c=[float(x) for x in open(f'/tmp/cuts_{th}.txt') if x.strip()]
b=[0]+c+[D]; sl=sorted(b[i+1]-b[i] for i in range(len(b)-1)); med=sl[len(sl)//2] if len(sl)%2 else (sl[len(sl)//2-1]+sl[len(sl)//2])/2
print(f"scene{th}: cuts={len(c)} cuts/min={len(c)/D*60:.1f} median_shot={med:.2f}s first_cut={c[0] if c else D:.2f}s cuts={[round(x,2) for x in c]}")
PY
done
ffmpeg -nostats -i "$V" -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|Peak|LRA):' | tr -s ' ' | tr '\n' ' '; echo
echo "pauses>=0.25s: $(ffmpeg -i "$V" -af silencedetect=n=-35dB:d=0.25 -f null - 2>&1 | grep -c silence_start)"
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 "$V"; echo "dur=$D audio_streams=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$V" | wc -l)"
