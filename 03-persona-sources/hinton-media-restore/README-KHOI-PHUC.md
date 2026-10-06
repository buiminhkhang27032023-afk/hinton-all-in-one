# HINTON MEDIA — GÓI KHÔI PHỤC ĐẦY ĐỦ (export 04/10/2026, giờ VN UTC+7)

Gói này chứa toàn bộ setup Hinton Media trên box cũ: tài liệu, kỹ năng, kiến thức dựng video, code pipeline render, server giọng OmniVoice (file giọng khoá v2), các job video (script/config/QA + bản 720p), kho học kênh mẫu (breakdown, contact sheet, transcript), định nghĩa 7 bot. Giải nén → chạy `restore/install-all.sh` → tạo lại bot theo mục 6.

> Gói được **copy** từ box, không xoá/di chuyển gì trên box gốc. Các thứ to/tải lại được (venv, node_modules, model, mp4 nguồn, footage thô) **không** kèm, xem `EXCLUDED.txt`.

---

## 1. Bên trong có gì (sơ đồ thư mục)

```
hinton-media-full/
├── README-KHOI-PHUC.md        ← file này
├── MANIFEST.txt               ← danh sách mọi file + dung lượng
├── EXCLUDED.txt               ← những gì bị loại + lý do (kể cả phần quét bí mật)
├── restore/install-all.sh     ← script khôi phục 1 lệnh
├── hinton-pipeline-docs/      ← (1) bộ não: docs, roles, skills, kiến thức edit
│   ├── HINTON_BOOTSTRAP.md, BOTS.md, MEMORY-va-BAI-HOC.md, DA-HOC-20261003.md
│   ├── luong-toi-uu.md, playbook-san-xuat.md, genres-formats-ui.md, voice-lock.md, token-optimize.md
│   ├── roles/   bot2-tin-ai, bot2b-douyin, bot3-bien-kich, bot4-douyin, bot5-san-tin
│   ├── skills/  hinton-orchestrate.md, hinton-render-shorts.md
│   ├── assets/  presenter-photo.jpg, presenter-video-orig.mp4, presenter-video-novoice.mp4
│   └── edit-video/  SO-TAY-DUNG, SO-TAY-KICH-BAN, DAN-CHUNG-FOOTAGE, CONG-THUC-HINTON,
│                    QUY-TRINH-VARUN, TEMPLATES, REPO-AI-VIDEO, CONG-THUC-EDIT, BRIEF,
│                    catalog.json(l), kenh-mau/, xem-ky/, dien-dan/, _data/
├── AI-auto-generate-video/    ← (2) pipeline render (Python + HyperFrames), presets kallaway/varun
│   ├── run.sh, README.md, config.default.json, pipeline/, templates/, tools/, assets/ (font, sfx, nhạc)
│   ├── package.json + package-lock.json (hyperframes@0.8.114, gsap)
│   ├── requirements.txt (gọn) + requirements.lock.txt (đúng bản đã chạy) + install.sh
│   └── .git/ (lịch sử; có thay đổi chưa commit, giữ nguyên trạng)
├── omnivoice-server/          ← (3) TTS local: server.py, restart.sh, asr_check.py,
│                                  voice-lock-vn-v2.wav + voice-lock-vn-v2.ref.txt, requirements(.lock).txt, install.sh
├── video-jobs/                ← (4) RENDER-LOCK.md, deliver.sh, tools/ (persona bot tạm), các job:
│   ├── TEST-pipeline-001/     job mẫu HyperFrames (Hoàn thành v1-19s)
│   ├── EDIT-SELFTRAIN-01/     tự luyện preset kallaway (Hoàn thành r3-20s) + tools kw_*
│   ├── EDIT-FULL-01/          bản mẫu Varun: v2, v3 (được duyệt), v4 (quy trình 1 lệnh, QA 20/20)
│   ├── EDIT-FULL-02/          job Varun đang làm dở lúc export (ticket "Lỗi", IndexError trong render; chưa có output)
│   └── TIN-02/                research Top 3 tin AI tuần (tin.md + raw html nguồn)
│   (mỗi job: script, config, broll/screenshot urls, CREDITS, logs, qa/, plan json nhỏ của lam-viec/, output/*720p.mp4 + srt + script)
├── video-learn/               ← (5) học kênh mẫu: INDEX.md, *_breakdown.md, *_sheet.jpg, *_hook.jpg,
│                                  *_transcript/_script/_analysis/_audio_hf.json, info.json (đã lọc), tools/, listings/,
│                                  SOURCES-mp4.tsv (122 link nguồn) + redownload.sh
├── agents/                    ← (6) profile.json + settings.json của 7 bot (+ active-agent.json)
├── workflows/                 ← (7) user skills (lúc export: trống — xem README trong đó)
├── douyin-downloader/HUONG-DAN-GRAB.md  ← (8) cách tải Douyin bằng hinton-douyin/grab.py
└── extras/
    ├── learn-goi-goc/         gói gốc anh gửi lúc đầu (hinton-media-pack, hinton-export)
    ├── learn2/                bản sao BRIEF/CONG-THUC-EDIT/catalog đợt học đầu
    └── env/                   MOI-TRUONG-GOC.txt (phiên bản node/ffmpeg/python/model) + requirements các venv phụ
```

---

## 2. Danh sách bot (roster) và vai trò

| Bot | ID cũ (account này) | Thư mục trong `agents/` | Vai |
|---|---|---|---|
| **bố của các bot** (title: "điều phối Hinton Media") | dde7b68b-af4f-4203-a066-3659e7ffaf44 | `bo-cua-cac-bot__dde7b68b…` | Điều phối: giao việc, chọn tin, QA script, nhận kết quả, báo anh |
| **Bot 5 — Săn tin và kiến thức AI** | d8592325-f729-4e40-93d3-dc2bfcb68851 | `bot5-san-tin__d8592325…` | Săn tin AI 24–72h, kiểm chứng claim (cả nhánh Douyin) |
| **Bot 4 — Douyin** | 7feb4d59-738d-4d0e-bbf5-ee531c808885 | `bot4-douyin__7feb4d59…` | Tải Douyin (grab.py), transcript tiếng Trung, dịch ý, SRT |
| **Bot 3 — Biên kịch** | eab21ff8-c4d4-4732-aeaf-d9a5edb0712c | `bot3-bien-kich__eab21ff8…` | Viết script 250–270 âm tiết từ research đã kiểm chứng |
| **Bot 2 — Tin AI** | f9e01114-7213-4d95-b43f-35f4eebfd20c | `bot2-tin-ai__f9e01114…` | Render nhánh Tin AI (HyperFrames / pipeline) |
| **Bot 2B — Douyin** | 970b5091-e601-4188-910e-bc58c9a50dac | `bot2b-douyin__970b5091…` | Render nhánh remix Douyin |
| **Trợ Lý Edit Video** | 65c5b9ad-cb27-4aa6-bfb7-2d19e9d49ccc | `tro-ly-edit-video__65c5b9ad…` | Dựng video từ footage anh gửi, theo quy trình Varun (ngoài 5 bot) |

ID cũ chỉ để tham chiếu — trên account mới bot sẽ có ID mới (xem mục 6, cập nhật lại BOTS.md).
ID trong `DA-HOC-20261003.md`/`MEMORY-va-BAI-HOC.md` và `video-jobs/tools/TEMP-BOT-*.md` là của account còn cũ hơn → bỏ qua.

## 3. Luồng việc chính xác

**Tin AI:**
`Bot5 (săn tin) → bố chọn 1 tin → Bot3 (viết script) → bố QA → Bot2 (render) / hoặc Trợ Lý Edit Video (nếu cần dựng kiểu Varun) → bố trả anh`

**Douyin:**
`Bot4 (tải + transcript + dịch) → Bot5 (kiểm chứng claim AI) → Bot3 (script remix) → bố QA → Bot2B (render) → bố trả anh`

**Edit video từ footage anh gửi:** anh gửi video/tài nguyên → bố nghiên cứu → giao Trợ Lý Edit Video (SendToAgent) → nhận kết quả → trả anh. Chưa có file nguồn thì không giao.

Hai nhánh Tin AI và Douyin chạy song song được (Bot2 vs Bot2B), nhưng render vẫn xếp hàng qua flock.

## 4. Quy tắc cố định

1. **Bố chỉ quản lý**: giao xuống bot con, nhận kết quả, QA, báo anh. Không tự làm thay việc của bot con.
2. **Phiếu bàn giao 1 dòng** cho mọi handoff: `JOB|status|version|path|next`
   Status: `Đã nhận → Đang xử lý nguồn → Đang viết → Đang sản xuất → Đang kiểm tra → Hoàn thành` (lỗi/chờ: `Bị chặn`). Render xong kèm size, duration, 1 câu QA.
3. **1 render một lúc** trên toàn máy: bọc TTS + render trong `flock /workspace/video-jobs/.render.lock <lệnh>` (run.sh tự làm). Restart OmniVoice: `flock -o /workspace/video-jobs/.render.lock /workspace/omnivoice-server/restart.sh`. Không xoá file lock. Chi tiết: `video-jobs/RENDER-LOCK.md`.
4. **Giọng**: chỉ **OmniVoice local** (127.0.0.1:8123), **male clone v2** (`voice-lock-vn-v2.wav` + `.ref.txt`), **speed 1.2**, `voice_locked:true`, loudnorm ~−14 LUFS. Chuỗi QA: `OmniVoice · male clone v2 locked · 1.2 · voice_locked:true`. **CẤM edge-tts, NamMinh, mọi cloud TTS**, giọng nữ cũ, instruct-only, seed random. Lệch giọng → restart rồi làm lại ≤2 lần.
5. **Script 250–270 âm tiết** (~4.6 âm tiết/s @1.2 → 55–60s). Viết số bằng chữ. Khung: HOOK 0–3s → bối cảnh → 2–4 ý → bằng chứng/nguồn → ý nghĩa → CTA.
6. **Ưu tiên mẫu kênh nước ngoài** (Varun Mayya, Kallaway, Riley Brown, Jeff Su…) và chủ đề đang hot ở nước ngoài / YouTube view cao; không trùng job đã làm; không quảng bá kênh Trung Quốc/đối thủ.
7. **Trợ Lý Edit Video dùng quy trình Varun** (`hinton-pipeline-docs/edit-video/QUY-TRINH-VARUN.md`, preset `"preset": "varun"`, bản mẫu EDIT-FULL-01 v4). **Riêng bot này: có burn caption + nhạc nền nhỏ** (`"captions_burn": true, "bgm": true, "bgm_volume_db": -20`).
   Các bot render khác (Bot2/Bot2B): mặc định **không** burn karaoke, **không** BGM, SRT sidecar — trừ khi phiếu yêu cầu.
8. Mặc định video: ~60s, 9:16, 1080×1920 H.264/AAC + bản `storytelling_mobile_720p.mp4`; giao anh file 720p + 1 dòng chủ đề + thời lượng. Local-only; Drive chỉ khi được yêu cầu.
9. Sửa tối đa 2 vòng mỗi bước rồi báo anh. Không chạy quá nhiều bot cùng lúc (bài học ~25 bot làm sập máy). Thiếu RAM: không dùng whisper large/medium.
10. Xưng hô: gọi anh là "anh", bot xưng "em" (không xưng "bố" với anh). Tiết kiệm token: path + tóm tắt, không dump file (`token-optimize.md`).

---

## 5. Khôi phục từng bước

Yêu cầu máy: Linux x86_64 (box cũ: Debian 13), CPU đủ (≥ 8 GB RAM khuyên dùng), ~15 GB trống cho venv + model, có `ffmpeg`, `flock`, `curl`, Internet.

**Nhanh (1 lệnh):**
```bash
unzip hinton-media-full-*.zip -d ~/hinton-restore && cd ~/hinton-restore/hinton-media-full
bash restore/install-all.sh          # FORCE=1 để ghi đè /workspace/<thư mục> đã có; WITH_LEARN_TOOLS=1 để cài venv tools video-learn
```

**Thủ công (nếu muốn từng bước):**
1. **Đặt file đúng chỗ** — mọi script/config trỏ cứng `/workspace/...`:
   `cp -a hinton-pipeline-docs AI-auto-generate-video omnivoice-server video-jobs video-learn /workspace/ && touch /workspace/video-jobs/.render.lock`
2. **Cài công cụ**: `ffmpeg` (apt), `uv` (`curl -LsSf https://astral.sh/uv/install.sh | sh`).
3. **Node 22** (bắt buộc cho HyperFrames): tải `node-v22.x-linux-x64.tar.xz` từ nodejs.org, giải nén vào `~/.local/node22`, symlink `node/npm/npx` vào `~/.local/bin` (script làm sẵn). Kiểm tra `node --version` → v22.
4. **OmniVoice**: `bash /workspace/omnivoice-server/install.sh` (venv Python 3.13, torch CPU, tải model `k2-fsa/OmniVoice`).
   Khởi động: `flock -o /workspace/video-jobs/.render.lock /workspace/omnivoice-server/restart.sh` → đợi 1–4 phút →
   `curl -s 127.0.0.1:8123/health` phải có `"voice_locked": true`, `ref_audio …voice-lock-vn-v2.wav`, `"speed": 1.2`.
5. **HyperFrames + pipeline**: `bash /workspace/AI-auto-generate-video/install.sh` (npm ci → hyperframes@0.8.114 + gsap; venv Python 3.12 từ requirements.lock.txt với index torch CPU; tải model align `nguyenvulebinh/wav2vec2-base-vi-vlsp2020` + `Systran/faster-whisper-small`).
   Rồi: `cd /workspace/AI-auto-generate-video && npx hyperframes browser ensure && npx hyperframes doctor` (đặt `HYPERFRAMES_NO_TELEMETRY=1`).
6. **Chạy thử**: `cd /workspace/AI-auto-generate-video && ./run.sh /workspace/video-jobs/TEST-pipeline-001` → kiểm `qa/ticket.txt`, `output/storytelling_mobile_720p.mp4`.
   Thử Varun: `./run.sh /workspace/video-jobs/EDIT-FULL-01` (config v4; footage sẽ tự tải lại từ broll_urls/screenshot_urls/portraits).
7. (Tuỳ chọn) tải lại video mẫu cho video-learn: `bash /workspace/video-learn/redownload.sh`.
8. (Tuỳ chọn) API stock: đặt `PEXELS_API_KEY` / `PIXABAY_API_KEY` trong môi trường nếu muốn (gói không chứa key nào).

## 6. Tạo lại bot từ profile

Với mỗi thư mục trong `agents/`:
1. Tạo agent mới trên account mới, **Tên** = `name` trong `profile.json`, **mô tả/hướng dẫn (instructions)** = nguyên văn trường `description`. `settings.json` chỉ có `notifyOnAgentUpdates: true` → bật thông báo cập nhật.
2. Thứ tự đề xuất: bố của các bot → Bot 5 → Bot 4 → Bot 3 → Bot 2 → Bot 2B → Trợ Lý Edit Video.
3. **bố của các bot**: profile gốc chỉ có mô tả mặc định (title "điều phối Hinton Media", avatar blob đen); bộ nhớ thật của bố nằm ở docs. Khi tạo lại, đặt hướng dẫn gợi ý:
   > Bạn là "bố của các bot", điều phối Hinton Media. Đọc /workspace/hinton-pipeline-docs/ (HINTON_BOOTSTRAP.md, BOTS.md, MEMORY-va-BAI-HOC.md, luong-toi-uu.md, skills/hinton-orchestrate.md, voice-lock.md, video-jobs/RENDER-LOCK.md). Chỉ quản lý: giao việc xuống bot con bằng SendToAgent, nhận kết quả, QA script, báo anh milestone + file 720p. Luồng Tin AI: Bot5→bố chọn→Bot3→bố QA→Bot2 (hoặc Trợ Lý Edit Video). Douyin: Bot4→Bot5→Bot3→bố QA→Bot2B. Phiếu JOB|status|version|path|next. 1 render một lúc (flock). Giọng OmniVoice male clone v2 speed 1.2, cấm edge-tts/cloud TTS. Script 250–270 âm tiết. Ưu tiên mẫu kênh nước ngoài. Gọi user "anh", xưng "em".
4. **Trợ Lý Edit Video**: profile gốc ghi công thức Cường Mê AI; theo quy tắc hiện hành hãy bổ sung vào hướng dẫn: "Dựng theo QUY-TRINH-VARUN.md (preset varun, mẫu EDIT-FULL-01 v4), bật captions_burn + bgm −20 dB; QA bằng tools/varun_qa.py."
5. Sau khi có ID mới: **cập nhật** `hinton-pipeline-docs/BOTS.md` và thay ID `dde7b68b-…` của bố trong `description` của 6 bot con bằng ID bố mới.
6. Các bot con trỏ docs theo đường dẫn `/workspace/...`, nên chỉ cần bước 5 mục "Khôi phục" là bot dùng được ngay.

## 7. Ghi chú

- `hinton-douyin/grab.py` chạy trên PC Windows của anh (DESKTOP-VHMVQSR), không có trên box → không có trong zip; xem `douyin-downloader/HUONG-DAN-GRAB.md`.
- Box chỉ có CPU: TTS ~12s cho mỗi 1s audio (video 60s ≈ 12 phút TTS) là bình thường; TTS được cache theo câu.
- Footage yt-dlp chỉ dùng đoạn ngắn và **ghi nguồn** (CREDITS.md, qa/report.md).
