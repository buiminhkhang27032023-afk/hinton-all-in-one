# Skill — hinton-render-shorts

## Khi dùng
Bot2 Tin AI và Bot2B Douyin sau khi bố đã QA script.

## Quy trình
1. Đọc script + job folder; không thêm claim.
2. Chọn HyperFrames (ưu tiên), fallback FFmpeg; video 9:16, ưu tiên 1080×1920.
2b. **Render lock (bắt buộc từ 2026-10-03):** bọc TTS + render trong `flock /workspace/video-jobs/.render.lock <command>` — tối đa 1 render cùng lúc. Viết script/research không cần lock. Xem `/workspace/video-jobs/RENDER-LOCK.md`.
3. Voice bằng OmniVoice local theo voice-lock: **male voice-clone v2 BẮT BUỘC**, speed `1.2`, health `voice_locked:true`. Ref: `/workspace/omnivoice-server/voice-lock-vn-v2.wav` + `.ref.txt`.
4. Xuất MP4, `voice_storytelling.wav`, `subtitle.srt`, `storytelling_script.txt`; không BGM/burn karaoke mặc định.
5. ffprobe + `qa/report.md`: engine, template/path, duration, QA string `OmniVoice · male clone v2 locked · 1.2 · voice_locked:true`, gaps.
6. Bàn giao: `JOB|Hoàn thành|version|path|next=bố` + size, duration, 1 câu QA.

**CẤM:** cloud TTS, giọng nữ cũ (voice-lock-female-vn, retired), edge-tts, NamMinh, tắt clone, instruct-only sole lock, voice random, upload media ngoài local nếu chưa có chỉ đạo. Lệch voice → restart `/workspace/omnivoice-server/restart.sh` rồi remake ≤2.
