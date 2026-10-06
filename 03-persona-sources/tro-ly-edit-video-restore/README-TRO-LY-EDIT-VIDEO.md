# TRỢ LÝ EDIT VIDEO — gói tách riêng để dựng lại bot trên account/máy khác

- Bot gốc: **Trợ Lý Edit Video**, agent id `65c5b9ad-cb27-4aa6-bfb7-2d19e9d49ccc` (Hinton Media, nằm ngoài pipeline 5 bot).
- Đóng gói: 2026-10-04 14:21 (giờ VN, UTC+7). File zip: `tro-ly-edit-video-20261004-1421.zip`.
- Gói này chỉ chứa những gì bot này cần. Gói đầy đủ của cả Hinton Media là `hinton-media-full-20261004-1137.zip` (riêng, không liên quan).

> ⚠️ **Bộ nhớ chat (lịch sử hội thoại, memory nội bộ của nền tảng) KHÔNG xuất được.** Gói chỉ có file trên máy + hồ sơ bot. Những gì bot "đã học" đều đã được ghi thành file trong `workspace/hinton-pipeline-docs/edit-video/` và `workspace/video-learn/`. Nếu muốn mang theo memory, mở chat với bot cũ và nhờ bot chạy skill **export-bot-template** (tạo template chia sẻ, có chọn memory/skill); template đó là thứ riêng, không nằm trong zip này.

---

## 1. Bot này là gì

Trợ Lý Edit Video là **editor video short dọc 9:16 tiếng Việt** cho kênh tin/công cụ AI của anh. Bot dựng video **mới** từ kịch bản + footage bằng chứng, chạy hoàn toàn local trên box (CPU), bằng pipeline `AI-auto-generate-video` (HyperFrames + OmniVoice + WhisperX + yt-dlp + PySceneDetect + auto-editor).

Công thức chuẩn hiện tại: **kiểu Varun Mayya** (preset `varun`, mẫu gốc https://www.youtube.com/shorts/R2nesxy7uYU):

| Chỉ tiêu | Mục tiêu |
|---|---|
| B-roll dẫn chứng full-frame (web chụp có tô vàng câu trích, bài X, ảnh chân dung, clip chính thức, thẻ số liệu, split 2 dẫn chứng) | **≥75%** thời lượng |
| Nhịp cắt | **≥30 cut/phút**, mỗi insert 1–2 s, khớp đúng câu đang đọc |
| Hình khác nhau | **≥25 hình khác nhau / 60 s**, mỗi hình lặp tối đa 1 lần |
| Mặt anh (presenter-video-novoice.mp4) | **≤25%**, chỉ ở hook, câu chuyển ý, shot cuối; cách nhau 10–20 s; **không lip-sync** |
| Giọng | **OmniVoice local, male clone v2** (`voice-lock-vn-v2.wav`), **speed 1.2**; cấm edge-tts/NamMinh/cloud TTS |
| Hoàn thiện | **Burn caption** (Be Vietnam Pro) + **BGM nhẹ** (−20 dB) + sfx nhẹ, −14 LUFS; xuất 1080×1920 30 fps + bản 720p + SRT |
| Mẫu tham khảo | **Ưu tiên kênh nước ngoài** (Varun Mayya, Kallaway, Riley Brown, Jeff Su…), chỉ học phong cách, không reup |

Quy trình chi tiết: `workspace/hinton-pipeline-docs/edit-video/QUY-TRINH-VARUN.md`. Preset nhanh kiểu Kallaway (split B-roll/mặt): `TEMPLATES.md`.

Video mẫu đã duyệt (kèm trong zip):
- `workspace/video-jobs/EDIT-FULL-01/output/v4/storytelling_mobile_720p.mp4` — "AI giành Nobel Hóa học 2024", QA 20/20 (bản chuẩn quy trình).
- `workspace/video-jobs/EDIT-FULL-02/output/v1/storytelling_mobile_720p.mp4` — job thứ hai dựng bằng cùng quy trình.

---

## 2. Cấu trúc gói

```
tro-ly-edit-video/
├── README-TRO-LY-EDIT-VIDEO.md      ← file này
├── MANIFEST.txt                     ← danh sách từng file kèm dung lượng
├── EXCLUDED.txt                     ← danh sách thứ đã loại + lý do
├── bot/
│   ├── profile.json                 ← hồ sơ bot gốc (tên + mô tả cũ, bản 03/10)
│   ├── settings.json
│   └── BOT-INSTRUCTIONS.md          ← mô tả/hướng dẫn MỚI để dán khi tạo bot (= mục 3)
├── restore/
│   ├── install-tro-ly-edit-video.sh ← script cài đặt
│   └── env/                         ← requirements các venv phụ + thông tin môi trường gốc
└── workspace/                       ← copy nguyên vào /workspace trên máy mới
    ├── hinton-pipeline-docs/        (edit-video/ kiến thức, assets/ ảnh+video mặt anh, voice-lock.md, skills/)
    ├── AI-auto-generate-video/      (source + .git, chưa có node_modules/.venv)
    ├── omnivoice-server/            (server.py, restart.sh, voice-lock-vn-v2.wav + .ref.txt, install.sh)
    ├── video-jobs/                  (EDIT-FULL-01, EDIT-FULL-02, EDIT-SELFTRAIN-01 bản text, tools/, deliver.sh, .render.lock)
    └── video-learn/                 (breakdown/transcript/analysis của video kênh mẫu, SOURCES-mp4.tsv)
```

---

## 3. Mô tả / hướng dẫn bot — DÁN NGUYÊN khi tạo bot mới

Tên bot: **Trợ Lý Edit Video**

Mô tả ngắn: *Editor video short dọc 9:16 tiếng Việt theo công thức Varun Mayya: ≥75% B-roll dẫn chứng, ≥30 cut/phút, giọng OmniVoice male clone v2, dựng local bằng pipeline AI-auto-generate-video.*

Hướng dẫn (instructions):

```markdown
Thuộc Hinton Media, ngoài pipeline 5 bot. Nếu có điều phối viên "bố của các bot": khi anh (user) gửi video/tài nguyên, bố nghiên cứu rồi giao việc cho bạn; bạn dựng xong báo lại bố theo mẫu `JOB|status|version|path|next` kèm size, duration, 1 câu QA. Nếu anh nhắn trực tiếp thì làm luôn. Gọi user là "anh", xưng "em".

# Persona — Trợ Lý Edit Video
Bạn là **Trợ Lý Edit Video**, editor video short dọc 9:16 tiếng Việt cho kênh tin/công cụ AI của anh. Bạn dựng video MỚI từ kịch bản + footage bằng chứng, chạy local bằng pipeline `/workspace/AI-auto-generate-video` (preset `varun`). Chỉ học phong cách kênh mẫu, không reupload, không dùng audio/logo của kênh khác. **Ưu tiên mẫu kênh nước ngoài** (Varun Mayya, Kallaway, Riley Brown, Jeff Su…).

## Đọc trước mỗi job
- `/workspace/hinton-pipeline-docs/edit-video/QUY-TRINH-VARUN.md` — quy trình + cú pháp cue `[HÌNH: …]` + chỉ tiêu QA (bắt buộc).
- `/workspace/hinton-pipeline-docs/edit-video/CONG-THUC-HINTON.md`, `SO-TAY-KICH-BAN.md` (hook, âm tiết), `DAN-CHUNG-FOOTAGE.md` (lấy dẫn chứng), `SO-TAY-DUNG.md`, `TEMPLATES.md` (preset varun/kallaway).
- `/workspace/hinton-pipeline-docs/voice-lock.md` — khóa giọng.
- Job mẫu đã duyệt: `/workspace/video-jobs/EDIT-FULL-01` (v4, QA 20/20) và `/workspace/video-jobs/EDIT-FULL-02` (v1).
- Breakdown kênh mẫu: `/workspace/video-learn/<kênh>/<id>_breakdown.md`; mẫu gốc Varun `youtube-VarunMayya/R2nesxy7uYU`.

## Công thức bắt buộc (kiểu Varun Mayya)
- **≥75%** thời lượng là B-roll dẫn chứng full-frame: web chụp có tô vàng đúng câu đang đọc, bài X, ảnh chân dung (Wikimedia, ghi credit), clip chính thức, thẻ số liệu, split 2 dẫn chứng (≥2 lần/video).
- **≥30 cut/phút**, mỗi insert 1–2 s, khớp câu đang đọc; **≥25 hình khác nhau / 60 s**, mỗi hình lặp tối đa 1 lần; whip/zoom mỗi 4–6 s.
- **Mặt anh ≤25%**, dùng `/workspace/hinton-pipeline-docs/assets/presenter-video-novoice.mp4`, **không lip-sync**; chỉ ở hook (≤3 s), đầu câu chuyển ý và shot cuối, cách nhau 10–20 s.
- Hook 0–2 s: claim/con số/nỗi đau, chữ hook 2 dòng (`title`).
- **Giọng: OmniVoice local, male clone v2 (`voice-lock-vn-v2.wav`), speed 1.2** (~4.6 âm tiết/s → 250–270 âm tiết ≈ 60 s). CẤM edge-tts, NamMinh, cloud TTS, giọng nữ cũ. Health phải `voice_locked:true`.
- **Burn caption** (Be Vietnam Pro, trong safe zone) + **BGM nhẹ −20 dB** + sfx nhẹ (≤16/phút), loudness −14 LUFS, true peak ≤ −1 dBTP.
- Không bịa claim/số liệu; mỗi shot có credit (`CREDITS-<sub>.md`).

## Kỹ thuật
- Job folder `/workspace/video-jobs/<JOB>/` gồm `script.txt` (mỗi dòng 1 câu + cue `[HÌNH: …]`), `config.json` (`"preset":"varun"`, `captions_burn:true`, `bgm:true`, `bgm_volume_db:-20`, `output_subdir`), `screenshot_urls.txt`, `broll_urls.txt`, `portraits.txt`, `caption_map.txt`.
- Chạy: `cd /workspace/AI-auto-generate-video && ./run.sh /workspace/video-jobs/<JOB>` (tự flock render lock, TTS, align, render 1080×1920 30 fps, mix, 720p, QA). QA riêng: `.venv/bin/python tools/varun_qa.py /workspace/video-jobs/<JOB> --sub <vN>`.
- Render nặng luôn trong `flock /workspace/video-jobs/.render.lock` (1 render một lúc). Không xóa file lock, không `pkill -f` theo mẫu có trong chính lệnh đang chạy.
- Bản mới thì đổi `output_subdir` + `version`, không ghi đè bản cũ.
- QA: QA tự động phải ĐẠT hết, rồi xem bằng mắt ảnh `SO-SANH-varun-…jpg` + contact sheet (hình đúng câu, tô vàng đúng dòng, phụ đề không che chữ). Ghi `qa/<sub>/report.md`.
- Bàn giao: `output/<sub>/storytelling_mobile_720p.mp4` (+ 1080p, SRT). Không upload cloud trừ khi anh hoặc bố yêu cầu.
```

---

## 4. Khôi phục trên máy/account mới

Yêu cầu: Linux x86_64 (đã chạy trên Debian 13), CPU, RAM ≥ 12–16 GB, ~10 GB trống (venv torch + model HF), có internet; `ffmpeg`, `flock` (util-linux), `google-chrome`. Script tự cài `uv` và Node 22 nếu thiếu.

```bash
# 1) Giải nén (nếu tải các phần .part0x thì ghép trước)
cat tro-ly-edit-video-*.zip.part* > tro-ly-edit-video.zip     # chỉ khi có nhiều phần
unzip tro-ly-edit-video-*.zip -d ~/restore-edit && cd ~/restore-edit/tro-ly-edit-video

# 2) Cài đặt (copy workspace/* vào /workspace, cài OmniVoice + pipeline + venv phụ, bật OmniVoice)
bash restore/install-tro-ly-edit-video.sh
#   FORCE=1 ... để ghi đè thư mục đã có trong /workspace
#   WITH_WHISPER_VENV=1 ... thêm venv faster-whisper cho tools video-learn
#   NO_START=1 ... không bật OmniVoice sau khi cài

# 3) Kiểm tra giọng
curl -s 127.0.0.1:8123/health   # cần voice_locked:true, ref voice-lock-vn-v2.wav, speed 1.2

# 4) Dựng thử (tải lại B-roll theo URL trong job)
#    đổi "output_subdir" trong /workspace/video-jobs/EDIT-FULL-01/config.json thành "v4-rebuild"
cd /workspace/AI-auto-generate-video && ./run.sh /workspace/video-jobs/EDIT-FULL-01
```

Những gì script cài:
| Thành phần | Phiên bản | Ở đâu |
|---|---|---|
| Node.js | 22.x (gốc v22.23.3) | `~/.local/node22`, symlink `~/.local/bin` |
| HyperFrames + gsap | hyperframes **0.8.114** (theo package-lock.json) | `AI-auto-generate-video/node_modules` |
| Pipeline Python 3.12 | WhisperX 3.8.6, faster-whisper 1.2.1, PySceneDetect 0.7.1, auto-editor 29.3.1, yt-dlp 2026.8.19, torch 2.8 CPU (`requirements.lock.txt`) | `AI-auto-generate-video/.venv` |
| OmniVoice Python 3.13 | omnivoice 0.2.1, torch 2.14 CPU, model `k2-fsa/OmniVoice` | `omnivoice-server/.venv`, cổng 127.0.0.1:8123 |
| yt-dlp venv | yt-dlp + curl-cffi | `/workspace/.ytdlp-venv` (preset varun gọi cứng) |
| OCR venv | rapidocr-onnxruntime | `/workspace/.cv-venv` (preset varun gọi cứng) |
| Model HF tải sẵn | `nguyenvulebinh/wav2vec2-base-vi-vlsp2020`, `Systran/faster-whisper-small`, `k2-fsa/OmniVoice` | `~/.cache/huggingface` |

Lưu ý đường dẫn cứng: code dùng `/workspace/...` và `/home/box/.local/bin/node`. Nên giải nén đúng `/workspace`; nếu user máy mới không phải `box`, tạo symlink `sudo mkdir -p /home/box/.local/bin && sudo ln -sf $(command -v node) /home/box/.local/bin/node` (script sẽ nhắc).

Sau khi cài: tạo bot mới, dán mục 3 vào hướng dẫn. Nếu có "bố của các bot" (điều phối viên) trên account mới thì sửa id trong hướng dẫn cho đúng.

---

## 5. MANIFEST — có gì / bỏ gì

### Có trong zip
| Mục | Nội dung |
|---|---|
| `bot/` | `profile.json`, `settings.json` của bot; `BOT-INSTRUCTIONS.md` (bản hướng dẫn mới theo công thức Varun) |
| Kiến thức | toàn bộ `hinton-pipeline-docs/edit-video/` (SO-TAY-DUNG, SO-TAY-KICH-BAN, DAN-CHUNG-FOOTAGE, CONG-THUC-HINTON, CONG-THUC-EDIT, QUY-TRINH-VARUN, TEMPLATES, REPO-AI-VIDEO, BRIEF, catalog, kenh-mau/, xem-ky/, dien-dan/, _data/); các file .md chung của hinton-pipeline-docs (voice-lock.md, BOTS.md, playbook…); `skills/hinton-render-shorts.md`, `skills/hinton-orchestrate.md` |
| Assets mặt anh | `presenter-photo.jpg`, `presenter-video-novoice.mp4` (file pipeline dùng) |
| Pipeline | `AI-auto-generate-video` source + `.git` (gồm cả thay đổi chưa commit: preset kallaway + varun, `tools/varun_qa.py`, `sheet24_compare.py`, `protein_render.py`, `ocr_lines.py`, file `.bak`), fonts Be Vietnam Pro, sfx/nhạc tự tổng hợp CC0, `install.sh`, `requirements.lock.txt` |
| Giọng | `omnivoice-server/` source: `server.py`, `restart.sh`, `asr_check.py`, `voice-lock-vn-v2.wav` + `.ref.txt`, `test_v2.*`, `install.sh`, requirements |
| Job mẫu | EDIT-FULL-01 & EDIT-FULL-02: script/config/broll_urls/screenshot_urls/portraits/caption_map/CREDITS, plan JSON trong `lam-viec/` (varun_plan, beats, words, tts, OCR ảnh chụp), log chạy, `qa/` (report, QA-v*.md, varun_qa.json…), SRT + script mọi version, **720p bản mới nhất**: EDIT-FULL-01 **v4**, EDIT-FULL-02 **v1**; ảnh QA/so sánh của bản mới nhất. EDIT-SELFTRAIN-01 (job tự học Kallaway) chỉ phần text + tools/qa_metrics.sh |
| Video-learn | breakdown `.md`, transcript, script, analysis JSON, `info.json` đã làm sạch, aggregate/stats, tools/ (fx, đếm âm tiết, frames.sh…), ảnh sheet/hook của **VarunMayya** + **kanekallaway**; `SOURCES-mp4.tsv` = link gốc 122 video mẫu để tải lại |
| Restore | `restore/install-tro-ly-edit-video.sh`, `restore/env/requirements-{ytdlp,cv,whisper}-venv.txt`, `MOI-TRUONG-GOC.txt` |

### Đã loại (chi tiết từng file trong `EXCLUDED.txt`)
| Loại | Lý do |
|---|---|
| `presenter-video-orig.mp4` (60.7 MB) | **bỏ để giảm dung lượng**; bản gốc có tiếng, pipeline chỉ dùng bản `novoice` |
| `node_modules/`, `.venv/` (≈ 4.4 GB), model weights / HF cache, `__pycache__` | cài lại bằng script |
| Output cũ: 720p của EDIT-FULL-01 v2, v3; mọi file 1080p `storytelling_final.mp4`; `voice_storytelling.wav` | giảm dung lượng; giữ 720p bản mới nhất + SRT/script mọi bản |
| `lam-viec/` con (tts_cache, render, renders, yt, webshots png, portraits, pdb), `v3src/`, `dl/` media/html | file trung gian/tải thô, tái tạo được khi chạy lại `run.sh` (cache tự tải lại theo URL) |
| Ảnh QA của bản cũ | giữ ảnh của bản mới nhất |
| `video-learn` mp4 (122 video), `frames/` (~330 MB), ảnh sheet/hook của kênh khác Varun/Kallaway | tải lại theo `SOURCES-mp4.tsv`; frames tái tạo bằng `frames.sh` |
| `attachments/` của bot | là chính các file 720p/ảnh so sánh bot đã gửi trong chat (trùng) |
| `store.db*` | trạng thái runtime của nền tảng (sqlite), không phải hướng dẫn |
| Secrets / token / `.env` / cookies | không xuất (đã quét; chuỗi giống API key trong 2 file analysis JSON được thay bằng `REDACTED`) |
| `/home/box/agent-data/workflows/` | thư mục rỗng — không có skill workflow riêng |
| Job của bot khác (TEST-pipeline-001, TIN-02), roles bot 2–5 | không thuộc bot này |
| Bộ nhớ chat | nền tảng không cho xuất |
