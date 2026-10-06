# HM-103 QA report — v1.1 (patch)

## Ticket
HM-103|Hoàn thành|v1.1|/workspace/video-jobs/HM-103/output/storytelling_final_v1.1.mp4|next=bố

## Outputs
- `output/storytelling_final_v1.1.mp4` — 1080×1920, 53.9s, ~42.1 MB (không ghi đè v1)
- `output/storytelling_mobile_720p_v1.1.mp4` — 720×1280, 53.9s, ~13.6 MB
- Voice: **không TTS lại** — reuse `lam-viec/voice.wav` + remixed `audio/mix.wav` (SFX timings shot 27 cập nhật)
- `qa/contact_sheet_v1.1.jpg` (16 khung)
- `qa/shot27_v1.1_check.jpg` — khung giữa shot 27

## Thay đổi so với v1
### Shot 27 (plan i=26, ~43.54–45.51s)
- **Trước:** TB split — top = `y10_wallclip.mp4` + nhãn "LÁCH TƯỜNG" (footage mờ đỏ, dễ hiểu nhầm)
- **Sau:** TB split — top = kinetic HTML graphic **WALL CLIP · LỖI BẢN ĐỒ** (Hinton vàng/đỏ trên nền tối, khung tự vẽ, không lưới đỏ kênh mẫu); bottom giữ blog agent-wow + highlight "exploit map bugs by phasing through walls" (`sh26p1.jpg`)
- Pill: chỉ `Nguồn: agent-wow.sh` (bỏ YouTube vì không còn footage YT làm bằng chứng)
- Plate tham chiếu: `lam-viec/shots/sh26p0_wallwarn.jpg`
- `hf/index.html` **không** còn tham chiếu `y10_wallclip`

### Shot 19 (plan i=18, y04_vendor ~30.03–30.86s)
- Đã quét thêm khung quanh 1180–1739s trong `wow_blind.mp4`
- Không tìm thấy cửa sổ vendor/NPC rõ hơn đoạn hiện tại (ghi chú bake_yt: "không thấy cửa sổ vendor")
- **Giữ nguyên** y04_vendor

## Self-check
- [x] Shot 27 không dùng y10_wallclip
- [x] Graphic WALL CLIP / LỖI BẢN ĐỒ đọc được trên khung kiểm
- [x] Bottom split blog + highlight còn
- [x] Duration ~54s (53.9s)
- [x] Voice không đổi (không OmniVoice lại)
- [x] Output tên *_v1.1.mp4, không ghi đè v1
- [x] Render dưới `flock /workspace/video-jobs/.render.lock`

## Pipeline
`build_hf.py` (wallwarn) → `mix.py` (SFX mới shot 27) → `hyperframes render` → copy `*_v1.1.mp4` + scale 720p
