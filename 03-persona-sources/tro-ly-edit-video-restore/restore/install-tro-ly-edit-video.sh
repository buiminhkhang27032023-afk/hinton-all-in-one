#!/usr/bin/env bash
# Khôi phục môi trường cho bot "Trợ Lý Edit Video" trên máy/account mới (Linux x86_64, CPU).
# Chạy từ thư mục giải nén:   bash restore/install-tro-ly-edit-video.sh
# Mặc định KHÔNG ghi đè thư mục đã có trong /workspace (FORCE=1 để ghi đè bằng bản trong zip).
# Biến tuỳ chọn: WITH_WHISPER_VENV=1 (venv faster-whisper cho tools video-learn), NO_START=1 (không bật OmniVoice).
set -euo pipefail
PKG="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
W=/workspace; mkdir -p "$W" "$HOME/.local/bin"
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH" HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1

echo "== 0) Công cụ hệ thống (ffmpeg, flock, google-chrome, uv, Node 22)"
command -v ffmpeg >/dev/null || { echo "Thiếu ffmpeg → sudo apt-get install -y ffmpeg"; exit 1; }
command -v flock  >/dev/null || { echo "Thiếu flock (gói util-linux)"; exit 1; }
command -v google-chrome >/dev/null || echo "CẢNH BÁO: thiếu google-chrome (dùng để chụp screenshot_urls) → cài Google Chrome stable."
command -v uv >/dev/null || { curl -LsSf https://astral.sh/uv/install.sh | sh; export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"; }
if ! node --version 2>/dev/null | grep -q '^v22'; then
  echo "   Cài Node 22 vào ~/.local/node22"
  V=$(curl -fsSL https://nodejs.org/dist/latest-v22.x/SHASUMS256.txt | grep -o 'node-v22[^ ]*-linux-x64.tar.xz' | head -1)
  curl -fsSL "https://nodejs.org/dist/latest-v22.x/$V" -o /tmp/node22.tar.xz
  rm -rf "$HOME/.local/node22" && mkdir -p "$HOME/.local/node22" && tar -xJf /tmp/node22.tar.xz -C "$HOME/.local/node22" --strip-components=1
  for b in node npm npx corepack; do ln -sf "$HOME/.local/node22/bin/$b" "$HOME/.local/bin/$b"; done
fi
node --version
# run.sh + pipeline/footage.py trỏ cứng /home/box/.local/bin/node
if [[ ! -x /home/box/.local/bin/node ]]; then
  echo "CẢNH BÁO: pipeline gọi /home/box/.local/bin/node. Máy này HOME=$HOME → tạo symlink:"
  echo "   sudo mkdir -p /home/box/.local/bin && sudo ln -sf $(command -v node) /home/box/.local/bin/node"
fi

echo "== 1) Copy thư mục vào /workspace"
for d in hinton-pipeline-docs AI-auto-generate-video omnivoice-server video-jobs video-learn; do
  if [[ -e "$W/$d" && "${FORCE:-0}" != 1 ]]; then
    echo "   $W/$d đã có → chỉ bổ sung file còn thiếu (FORCE=1 để ghi đè)"; cp -a -n "$PKG/workspace/$d/." "$W/$d/"
  else cp -a "$PKG/workspace/$d" "$W/"; echo "   -> $W/$d"; fi
done
touch "$W/video-jobs/.render.lock"

echo "== 2) OmniVoice server (venv py3.13 + model k2-fsa/OmniVoice, cổng 127.0.0.1:8123)"
bash "$W/omnivoice-server/install.sh"

echo "== 3) Pipeline AI-auto-generate-video (npm: hyperframes@0.8.114 + gsap; venv py3.12: WhisperX, faster-whisper, PySceneDetect, auto-editor, yt-dlp)"
bash "$W/AI-auto-generate-video/install.sh"
( cd "$W/AI-auto-generate-video" && npx hyperframes browser ensure && npx hyperframes doctor || true )

echo "== 4) venv phụ mà preset varun gọi cứng"
#  /workspace/.ytdlp-venv : yt-dlp + curl-cffi (tải clip broll, cần --js-runtimes node --remote-components ejs:github)
#  /workspace/.cv-venv    : rapidocr-onnxruntime (OCR ảnh chụp web để tô vàng câu trích)
VENVS="ytdlp cv"; [[ "${WITH_WHISPER_VENV:-0}" == 1 ]] && VENVS="$VENVS whisper"
for v in $VENVS; do
  uv venv --python 3.13 "$W/.$v-venv"
  uv pip install --python "$W/.$v-venv/bin/python" -r "$PKG/restore/env/requirements-$v-venv.txt" || \
  uv pip install --python "$W/.$v-venv/bin/python" $(sed 's/==.*//' "$PKG/restore/env/requirements-$v-venv.txt" | grep -v '^pip$')
done

if [[ "${NO_START:-0}" != 1 ]]; then
  echo "== 5) Bật OmniVoice (flock -o để server không giữ render lock)"
  flock -o "$W/video-jobs/.render.lock" "$W/omnivoice-server/restart.sh"
  echo "   Đợi model load 1–4 phút rồi: curl -s 127.0.0.1:8123/health  → voice_locked:true, ref voice-lock-vn-v2.wav, speed 1.2"
fi
echo "== XONG. Dựng thử (tải lại B-roll theo URL trong job): đổi \"output_subdir\" trong /workspace/video-jobs/EDIT-FULL-01/config.json thành \"v4-rebuild\" rồi: cd /workspace/AI-auto-generate-video && ./run.sh /workspace/video-jobs/EDIT-FULL-01"
echo "   Tạo lại bot: mở README-TRO-LY-EDIT-VIDEO.md mục 3 (dán mô tả/hướng dẫn bot)."
