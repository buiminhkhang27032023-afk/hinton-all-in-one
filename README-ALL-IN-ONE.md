# HINTON MEDIA — GÓI SAO LƯU "ALL IN ONE" (06/10/2026)

Gói này chứa đầy đủ cấu hình của **13 bot + 3 kênh nhóm**, skill dùng chung, tài liệu pipeline, thiết lập đăng bài, style ref, và code pipeline (không kèm node_modules/.venv/.git/model weights). **Không chứa secret** (không .env, token, cookie, hồ sơ trình duyệt, mật khẩu).

## 1. Danh sách bot (13) và kênh (3)

| # | Bot | ID | Đội | Vai trò | Kênh tham gia |
|---|---|---|---|---|---|
| 1 | New Bot — "bố của các bot" | 6271bde2-38e5-40bc-a9e3-af9ec21d22a3 | Điều phối chung | Nhận lệnh từ anh, giao việc cho các đội, QA script, giao thành phẩm 720p, đăng bài sau khi anh "duyệt" | Nhóm Douyin/Video 1, Nhóm tin AI/Video 2, Video tin tức |
| 2 | Bot 5 — Săn tin và kiến thức AI | c711dded-3dd2-4ff1-89e6-7f406a97245f | Hinton gốc | Săn tin / kiểm chứng nguồn | Video 1, Video 2 |
| 3 | Bot 4 — Douyin | 7b44d14c-27e5-48ec-bfbc-4fea434f4f94 | Hinton gốc | Tải + transcript + dịch Douyin | Video 2 |
| 4 | Bot 3 — Biên kịch | 6a695214-9da4-44e8-b23e-5907cc8358c9 | Hinton gốc | Viết kịch bản (style v3) | Video 1, Video 2 |
| 5 | Bot 2 — Tin AI | bd1398f4-efd3-46c7-bb62-c39e9dea8216 | Hinton gốc | Render nhánh Tin AI | Video 1 |
| 6 | Bot 2B — Douyin | f24f1cab-3ab7-4044-b29b-1fbcacb10153 | Hinton gốc | Render nhánh Douyin | Video 2 |
| 7 | Bot 5 — Săn tin (Video tin tức) | 25147768-ba52-4e48-acd4-d0b092c1abc2 | Video tin tức | Săn tin | Video tin tức |
| 8 | Bot 4 — Douyin (Video tin tức) | 50f63b9b-41ea-4b32-a627-631d10edbcb3 | Video tin tức | Douyin | Video tin tức |
| 9 | Bot 3 — Biên kịch (Video tin tức) | fe4ac9e1-51be-4b73-87f2-b5c6c5375635 | Video tin tức | Biên kịch | Video tin tức |
| 10 | Bot 2 — Tin AI (Video tin tức) | 28a3315d-421e-48fd-b2e3-42a2f546be77 | Video tin tức | Render Tin AI | Video tin tức |
| 11 | Bot 2B — Douyin (Video tin tức) | 08012706-dc2d-40cf-9165-cd50df086c64 | Video tin tức | Render Douyin | (không vào kênh — kênh tối đa 6, bố nhắn riêng) |
| 12 | Trợ Lý Edit Video (Video tin tức) | 7f03dd91-0ab4-4e10-bc00-b54430d0228c | Video tin tức | Dựng video từ footage anh gửi | Video tin tức |
| 13 | Video Map Food Tour | 8ffdf467-4d04-4774-9344-09333e76e9cb | Video Map Food Tour | Điều phối video map animation food tour 9:16 | (không vào kênh) |

| Kênh | ID | Thành viên | Ghi chú |
|---|---|---|---|
| Nhóm Douyin / Nhóm Video 1 | 0f7c4a3a-32db-4d2a-a2ea-bcfb5020721c | bố, Bot5, Bot3, Bot2 (Hinton gốc) | Thực tế chạy luồng **Tin AI** |
| Nhóm tin AI / Nhóm Video 2 | 6168ce57-2624-4bf1-9d1a-0dc3a9de4447 | bố, Bot4, Bot5, Bot3, Bot2B (Hinton gốc) | Thực tế chạy luồng **Douyin** |
| Video tin tức | 0dfc3c52-ec62-478f-8d2b-6a789bccc917 | bố, Bot5, Bot3, Bot2, Trợ Lý Edit, Bot4 (đội Video tin tức) | Bot2B đội này nhắn riêng |

(Tên kênh trên hệ thống bị đảo so với luồng thực tế — giữ nguyên ID, xem `02-channels/*/group.json`.)

## 2. Quy trình làm việc
1. **Anh ra lệnh theo đội** (Hinton gốc / Video tin tức / Video Map Food Tour) cho **bố**.
2. **Bố định tuyến** xuống bot con bằng SendToAgent (hoặc trong kênh nhóm).
   - Luồng Tin AI: Bot5 săn tin → bố chọn → Bot3 viết script → bố QA → Bot2 render (hoặc Trợ Lý Edit Video).
   - Luồng Douyin: Bot4 tải/dịch → Bot5 kiểm chứng → Bot3 viết script → bố QA → Bot2B render.
   - Food Tour: Bot5 nghiên cứu quán (places.json) → chọn tuyến → Bot3 kịch bản → QA → Bot2 render HyperFrames → QA khung hình.
3. **Các đội báo cáo về bố** (không nhắn anh trừ khi anh nhắn trực tiếp).
4. **Bố giao thành phẩm cho anh** (mốc + file 720p `storytelling_mobile_720p.mp4`). Tối đa 2 vòng sửa.

### Mẫu phiếu bàn giao (hand-off)
```
JOB|status|version|path|next
```
Ví dụ: `HM-105|done|v2|/workspace/video-jobs/HM-105/output/|bo-QA` — kèm size, duration, 1 câu QA. `priority true` chỉ khi cần hành động. Job đặt tại `/workspace/video-jobs/<job-id>/`.

## 3. Render lock (bắt buộc)
- Tối đa **1 render cùng lúc** trên toàn box.
- Bọc TTS + render trong: `flock /workspace/video-jobs/.render.lock <command>`
- Restart OmniVoice: `flock -o /workspace/video-jobs/.render.lock /workspace/omnivoice-server/restart.sh`
- Không xóa file lock. Chi tiết: `05-docs/video-jobs/RENDER-LOCK.md`.

## 4. Giọng đọc (voice lock)
- **OmniVoice local** (http://127.0.0.1:8123), **male voice-clone v2**: `voice-lock-vn-v2.wav` + `voice-lock-vn-v2.ref.txt` (có trong `08-pipeline-code/omnivoice-server/`), **speed 1.2**, loudnorm ~−14, health phải `voice_locked:true`.
- **CẤM**: edge-tts, NamMinh, cloud TTS, giọng nữ cũ (retired), instruct-only, tắt clone, seed random.
- Chuỗi QA: `OmniVoice · male clone v2 locked · 1.2 · voice_locked:true`.

## 5. Kịch bản
- Video ~60s: **250–270 âm tiết**, **style v3** (xem `05-docs/hinton-pipeline-docs/` + `07-video-learn/ref-20261005/STYLE-SPEC.md`). ~90s: 380–400 âm tiết.
- Không bịa số liệu (ghi "khoảng"), đọc số thành chữ, nhạc/ảnh có license. Ưu tiên mẫu kênh nước ngoài.

## 6. Quy tắc đăng bài
- **Chỉ đăng sau khi anh nhắn "duyệt"** cho đúng video. Bật nhãn nội dung AI khi có.
- **Bố tự đăng bằng trình duyệt**:
  - Facebook (tài khoản **Phạm Tuan Anh**): Page **Hinton Creator Academy** (https://www.facebook.com/profile.php?id=61594658551071) và Page **Anh Em Tích Cực** (https://www.facebook.com/tallashgumshuda).
  - Zalo Web (tài khoản **Nguyễn Absolut**, chat.zalo.me) — 4 nhóm: BP2: Noxh Marquee Võ Nguyên Giáp; Hội farm bá khí hilton; TK chạy zalo tự động; 📈 CHIẾN LƯỢC VÀNG 2026 - 2027 - GOLD CAPITAL 💎.
- **KHÔNG TikTok, KHÔNG Buffer.**
- Chi tiết: `06-social-posting/posting-targets-20261006.md`.

## 7. Cấu trúc gói
| Thư mục | Nội dung |
|---|---|
| `01-bots/<slug>__<id>/` | profile.json, settings.json, assets/, attachments/ (≤5MB), automations/, **PERSONA.md** (persona/instructions để tạo lại bot) |
| `02-channels/<slug>__<id>/` | profile.json, settings.json, **group.json** (memberIds), PERSONA.md |
| `03-persona-sources/` | Persona đầy đủ hơn: hinton-restore-agents/ (0-bo.json, BO-PERSONA-SUGGESTED.txt…), hinton-export-20261005/ (personas, roles, skills), hinton-media-restore/agents-reference, tro-ly-edit-video-restore/BOT-INSTRUCTIONS.md, grokbot-hinton-dl3/newbots, food-tour-pack-bo |
| `04-skills-workflows/workflows/` | Skill chung: hinton-orchestrate, hinton-render-shorts, map-animation-video-remake (từ /home/box/agent-data/workflows) |
| `05-docs/hinton-pipeline-docs/` | Toàn bộ tài liệu pipeline (BOTS.md, HINTON_BOOTSTRAP.md, voice-lock.md, roles/, skills/, edit-video/, assets/…) |
| `05-docs/video-jobs/` | RENDER-LOCK.md, deliver.sh, tools/, và file text của từng job (script/qa/config/research…, không media) |
| `06-social-posting/` | Đích đăng, caption, link (không kèm videos/) |
| `07-video-learn/` | Phân tích kênh mẫu (text) + ref-20261005/STYLE-SPEC.md + ref.mp4 |
| `08-pipeline-code/` | AI-auto-generate-video và omnivoice-server (source/config, voice-lock-vn-v2.wav + .ref.txt) + LISTING-*.txt |

## 8. Cách khôi phục
1. **Copy tài liệu về /workspace**:
   - `05-docs/hinton-pipeline-docs/` → `/workspace/hinton-pipeline-docs/`
   - `05-docs/video-jobs/` → `/workspace/video-jobs/` (tạo file lock rỗng: `touch /workspace/video-jobs/.render.lock`)
   - `06-social-posting/` → `/workspace/social-posting/`; `07-video-learn/` → `/workspace/video-learn/`
   - `04-skills-workflows/workflows/*` → `/home/box/agent-data/workflows/`
2. **Cài pipeline**: `08-pipeline-code/AI-auto-generate-video` → `/workspace/AI-auto-generate-video` rồi `./install.sh` (npm install + venv); `08-pipeline-code/omnivoice-server` → `/workspace/omnivoice-server` rồi `./install.sh`, `./restart.sh`, kiểm tra health `voice_locked:true`. Xem thêm `03-persona-sources/hinton-media-restore/restore/install-all.sh` và `README-KHOI-PHUC.md`.
3. **Tạo lại bot**: với mỗi thư mục trong `01-bots/`, tạo bot mới với **name / title / description** lấy từ `profile.json` (hoặc `PERSONA.md`). Bố: dùng tên "bố của các bot", title "điều phối Hinton Media", persona trong PERSONA.md (lấy từ BO-PERSONA-SUGGESTED.txt).
4. **Cập nhật ID mới**: bot mới sẽ có ID mới → sửa ID trong persona các bot con (dòng "Điều phối viên là bố … id …") và trong `/workspace/hinton-pipeline-docs/BOTS.md`.
5. **Tạo lại kênh**: theo `02-channels/*/group.json` (thay ID cũ → ID mới), giữ đúng thành viên như bảng mục 1.
6. Đăng nhập lại Facebook/Zalo trên trình duyệt box bằng tay (gói không chứa cookie/phiên đăng nhập).

## 9. Không có trong gói
- `store.db` của từng bot (chứa khóa mã hóa blob nội bộ + transcript; transcript không cần cho khôi phục).
- Secret, .env, cookie, hồ sơ trình duyệt, token (các cookie TikTok trong *.info.json đã được xóa; các trang HTML cào về đã bị loại).
- Media lớn: render output, mp4/wav/png/jpg của job, social-posting/videos, file đính kèm >5MB của bố (1 mp4 ~17MB).
- node_modules, .venv, .git, model weights, cache, file >20MB trong code pipeline.

## 10. Các phần zip trên Drive (thư mục "all in one")
Gói được chia theo khu vực (giới hạn upload 100MB/file). Giải nén tất cả vào cùng 1 chỗ sẽ ra đúng cây `all-in-one-20261006/`.
- part1-bots-channels-personas-skills-posting.zip — 01, 02, 03, 04, 06 + README + MANIFEST
- part2-docs-hinton-pipeline-docs.zip — 05-docs/hinton-pipeline-docs (trừ 2 video presenter)
- part3-docs-video-jobs.zip — 05-docs/video-jobs
- part4-video-learn.zip — 07-video-learn
- part5-pipeline-code.zip — 08-pipeline-code
- part6-docs-presenter-video-orig.zip, part7-docs-presenter-video-novoice.zip — 2 video presenter (~60MB mỗi file) thuộc hinton-pipeline-docs/assets
