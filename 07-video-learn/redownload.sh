#!/usr/bin/env bash
# Tải lại các mp4 mẫu từ SOURCES-mp4.tsv về đúng thư mục (cần yt-dlp; venv gợi ý: extras/env/requirements-ytdlp-venv.txt).
# Một số link TikTok/Douyin/Facebook có thể đã bị xoá hoặc cần đăng nhập → bỏ qua.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
Y=${YTDLP:-yt-dlp}
tail -n +3 "$HERE/SOURCES-mp4.tsv" | while IFS=$'\t' read -r folder id url rest; do
  [[ -z "$url" ]] && continue
  [[ -f "$HERE/$folder/$id.mp4" ]] && { echo "SKIP $id"; continue; }
  mkdir -p "$HERE/$folder"
  $Y -f "bv*[height<=1080]+ba/b[height<=1080]/b" --merge-output-format mp4 --no-playlist -o "$HERE/$folder/$id.%(ext)s" "$url" || echo "FAIL $folder $id $url"
  sleep 3
done
