# Voice lock — Hinton Shorts (Bot 2 + Bot 2B)

Áp dụng mọi job storytelling Tin AI / Douyin trừ khi bố/user ghi rõ khác.

| Field | Value |
|---|---|
| Engine | OmniVoice local only |
| Endpoint | `http://127.0.0.1:8123` |
| Form | **Nam cố định qua voice-clone (lock v2, từ 2026-10-03)** |
| Ref audio | `/workspace/omnivoice-server/voice-lock-vn-v2.wav` |
| Ref text | `/workspace/omnivoice-server/voice-lock-vn-v2.ref.txt` |
| speed | `1.2` (từ 2026-10-03; trước đó 1.12) |
| Tốc độ đọc | ~4.6 âm tiết/giây @1.2 |
| Loudnorm | ~−14 LUFS VO-only |

## Ghi chú cho biên kịch (Bot3)
Ở speed 1.2 giọng nam chạy ~4.6 âm tiết/giây → script nhắm **~250–270 âm tiết cho ~55–60s**. `script.json` không cần ghi `voice.speed` (mặc định 1.2); nếu ghi thì phải là `1.2`.

## Vì sao bắt buộc clone
`instruct` kiểu `male, moderate pitch` **không** khóa 1 giọng — mỗi lần `/tts` OmniVoice design lại → bố nghe từng đoạn một tông. Clone + cùng `voice_clone_prompt` trên server = 1 form cho mọi scene.

## QA bắt buộc
- Health: `voice_locked: true`, `ref_audio: voice-lock-vn-v2.wav`
- Log mỗi scene: `voice_clone=<file>` (server-side). Client có thể vẫn gửi instruct nhưng **server bỏ instruct khi đã lock**.
- Chuỗi QA: `OmniVoice · male clone v2 locked · 1.2 · voice_locked:true`
- Lệch / `voice_locked:false` = FAIL → restart `/workspace/omnivoice-server/restart.sh` rồi remake ≤2 lần rồi báo bố.

CẤM: edge-tts / NamMinh / giọng nữ cũ `voice-lock-female-vn*` (retired 2026-10-03) / cloud TTS / tắt clone / đổi ref giữa scene / seed random / TTS không qua OmniVoice local / instruct-only làm sole lock.

## Changelog
- **2026-10-03 (speed 1.2):** speed mặc định 1.12 → **1.2** (user duyệt). `server.py` + `restart.sh` + `AI-auto-generate-video/src/cli.ts` default + `qa_report.py` đã đổi. ~4.6 âm tiết/s → 250–270 âm tiết ≈ 55–60s.
- **2026-10-03 (lock v2):** đổi từ giọng **nữ** (`voice-lock-female-vn.wav`) sang giọng **nam** clone từ audio user gửi (đoạn 33.40–42.30s, 8.9s, 48 kHz mono, ~−16 LUFS).
  - Ref text v2: "Anh còn được biết đến như một chuyên gia hàng đầu về video ngắn và ứng dụng AI thực chiến, luôn đi đầu trong việc tối ưu hóa quy trình sản xuất."
  - Backup giọng cũ: `/workspace/omnivoice-server/voice-lock-female-vn.old-2026-10-03.wav` + `.old-2026-10-03.ref.txt`.
  - `voice-lock-female-vn.wav/.ref.txt` giờ chỉ là symlink tương thích → v2 (KHÔNG còn là giọng nữ). Dùng tên v2 trong mọi tài liệu/QA.
  - Server default (`server.py`) + `restart.sh` trỏ v2. Job render trước giờ switch (HM-001…HM-025) dùng giọng nữ cũ; không trộn 2 giọng trong 1 video — nếu remake job cũ thì TTS lại toàn bộ scene.
