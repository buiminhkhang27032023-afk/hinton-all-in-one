# RENDER LOCK — Hinton Media video pipeline

Ngày áp dụng: 2026-10-03. Áp dụng cho MỌI bot (kể cả bot tạm thời) chạy TTS/render trên box.

## Vì sao
Box chỉ có CPU; OmniVoice (127.0.0.1:8123) + HyperFrames/FFmpeg render rất nặng. Nhiều bot render cùng lúc → TTS chậm gấp nhiều lần (đã thấy 1 scene mất >1000s), dễ timeout, hỏng job.

## Quy tắc
- **Tối đa 1 render tại một thời điểm** trên toàn box.
- Bọc toàn bộ bước **TTS + render** (cùng 1 lệnh) trong flock:

```bash
flock /workspace/video-jobs/.render.lock <command>
```

Ví dụ:

```bash
flock /workspace/video-jobs/.render.lock bash -c 'cd /workspace/AI-auto-generate-video && npm run pipeline -- <outputDir>/script.json'
```

- `flock` chờ (block) đến khi bot khác nhả lock rồi mới chạy; lock tự nhả khi lệnh kết thúc (kể cả crash). KHÔNG xóa file lock.
- Muốn kiểm tra không chờ: `flock -n /workspace/video-jobs/.render.lock true && echo free || echo busy`.
- Muốn giới hạn thời gian chờ: `flock -w 3600 /workspace/video-jobs/.render.lock <command>` (hết 3600s → exit 1, báo bố).
- **Không cần lock:** viết script, research, QA script, tải nguồn Douyin, đọc file.
- **Cần lock:** gọi OmniVoice `/tts`, render HyperFrames/FFmpeg, remake voice/video.
- Restart OmniVoice (`/workspace/omnivoice-server/restart.sh`) cũng nên chạy trong lock để không cắt ngang job đang TTS:
  `flock /workspace/video-jobs/.render.lock /workspace/omnivoice-server/restart.sh`

File lock: `/workspace/video-jobs/.render.lock` (rỗng, chỉ dùng để flock).
