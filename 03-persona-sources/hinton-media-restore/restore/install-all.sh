#!/usr/bin/env bash
# Khôi phục Hinton Media trên máy/account mới (Linux x86_64, CPU).
# Chạy từ thư mục giải nén:  bash restore/install-all.sh
# Mặc định KHÔNG ghi đè thư mục đã có trong /workspace (đặt FORCE=1 để ghi đè bằng bản trong zip).
set -euo pipefail
PKG="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
W=/workspace; mkdir -p "$W" "$HOME/.local/bin"
export PATH="$HOME/.local/bin:$PATH" HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1

echo "== 0) Công cụ hệ thống"
command -v ffmpeg >/dev/null || { echo "Thiếu ffmpeg → sudo apt-get install -y ffmpeg (hoặc nhờ admin)"; exit 1; }
command -v flock  >/dev/null || { echo "Thiếu flock (util-linux)"; exit 1; }
command -v uv >/dev/null || { curl -LsSf https://astral.sh/uv/install.sh | sh; export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"; }
if ! node --version 2>/dev/null | grep -q '^v22'; then
  echo "== Cài Node 22 vào ~/.local"
  V=$(curl -fsSL https://nodejs.org/dist/latest-v22.x/SHASUMS256.txt | grep -o 'node-v22[^ ]*-linux-x64.tar.xz' | head -1)
  curl -fsSL "https://nodejs.org/dist/latest-v22.x/$V" -o /tmp/node22.tar.xz
  rm -rf "$HOME/.local/node22" && mkdir -p "$HOME/.local/node22" && tar -xJf /tmp/node22.tar.xz -C "$HOME/.local/node22" --strip-components=1
  for b in node npm npx corepack; do ln -sf "$HOME/.local/node22/bin/$b" "$HOME/.local/bin/$b"; done
fi
node --version

echo "== 1) Copy thư mục vào /workspace"
for d in hinton-pipeline-docs AI-auto-generate-video omnivoice-server video-jobs video-learn; do
  if [[ -e "$W/$d" && "${FORCE:-0}" != 1 ]]; then echo "  bỏ qua $W/$d (đã có; FORCE=1 để ghi đè)"; else cp -a "$PKG/$d" "$W/"; echo "  -> $W/$d"; fi
done
touch "$W/video-jobs/.render.lock"

echo "== 2) OmniVoice (venv + model k2-fsa/OmniVoice)"
bash "$W/omnivoice-server/install.sh"

echo "== 3) Pipeline AI-auto-generate-video (npm: hyperframes@0.8.114 + gsap; venv py3.12)"
bash "$W/AI-auto-generate-video/install.sh"
( cd "$W/AI-auto-generate-video" && npx hyperframes browser ensure && npx hyperframes doctor || true )

echo "== 4) (tuỳ chọn) venv cho tools video-learn"
if [[ "${WITH_LEARN_TOOLS:-0}" == 1 ]]; then
  for v in ytdlp whisper cv gallerydl; do uv venv --python 3.13 "$W/.$v-venv"; uv pip install --python "$W/.$v-venv/bin/python" -r "$PKG/extras/env/requirements-$v-venv.txt"; done
fi

echo "== 5) Khởi động OmniVoice (trong render lock, -o để server không giữ lock)"
flock -o "$W/video-jobs/.render.lock" "$W/omnivoice-server/restart.sh"
echo "   Đợi model load (~1–4 phút) rồi: curl -s 127.0.0.1:8123/health  → voice_locked:true, ref voice-lock-vn-v2.wav, speed 1.2"
echo "== XONG. Bước tiếp theo: tạo lại bot theo README-KHOI-PHUC.md mục 6 (agents/*/profile.json)."
