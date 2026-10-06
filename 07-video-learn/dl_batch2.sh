#!/bin/bash
while IFS=$'\t' read -r folder url id v d dur; do
  ls /workspace/video-learn/$folder/$id.mp4 >/dev/null 2>&1 && { echo "SKIP $id"; continue; }
  echo "== $folder $id"
  bash /workspace/video-learn/dl.sh "$folder" "$url" 2>&1 | grep -E "ERROR|does not pass|Merging|Destination" | tail -3
  sleep 3
done < /workspace/video-learn/dl_batch2.tsv
echo ALLDONE
