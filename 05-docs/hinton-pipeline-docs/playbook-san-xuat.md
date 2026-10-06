# Playbook sản xuất Shorts Hinton (chung Bot2 + Bot2B) — essentials

Handoff từ **bố của các bot** sau khi script đã QA.

## Vai trò
- Remix/việt hóa: không chép nguyên Douyin; không quảng bá kênh đối thủ.
- Local-only; Drive chỉ khi user/bố bảo.
- Karaoke burn-in: **CHỈ khi user yêu cầu**. Mặc định: sidecar `subtitle.srt`.
- Deliverables: `storytelling_final.mp4` + `voice_storytelling.wav` + `subtitle.srt` + `storytelling_script.txt` (+ optional mobile 720p).
- Spec: 9:16 **1080×1920** H.264/AAC yuv420p; cut TB 1–3s; hook 0–3s; không BGM trừ khi user đưa.

## Job folder
```
/workspace/video-jobs/<job-id>/
  source/
  lam-viec/
  output/
  qa/
```

## Hai đường dựng
### A) HyperFrames (ưu tiên)
1. Repo: `/workspace/AI-auto-generate-video`
2. Skill: `workflow/create-template-video/SKILL.md` + `templates/CATALOG.md`
3. Node 22: `PATH=/home/box/.local/bin:$PATH`
4. OmniVoice: `http://127.0.0.1:8123` — health `GET /health`; restart `/workspace/omnivoice-server/restart.sh`
5. `.env.local`: `TTS_PROVIDER=omnivoice`, `OMNIVOICE_ENDPOINT=http://127.0.0.1:8123`
6. `script.json` (8–12 scenes): hook `frame-liquid-bg-hero` hoặc `frame-bold-poster`; body đa dạng; outro `frame-statement-outro` / `frame-logo-outro`; `voiceText` số ra chữ VN, không emoji.
7. `flock /workspace/video-jobs/.render.lock npm run pipeline -- <outputDir>/script.json` (render lock, xem `/workspace/video-jobs/RENDER-LOCK.md`)
8. Copy → `output/storytelling_final.mp4`; voice → `voice_storytelling.wav`; giữ script + SRT
9. Mobile: ffmpeg scale 720×1280 → `storytelling_mobile_720p.mp4`

### B) FFmpeg kinetic — fallback only (không chuẩn UI neon)

### Talking-head
Skill: `/workspace/hinton-skill-stage/hinton-ai-editor-agent/`  
Venv: `source /workspace/video-jobs/hinton-venv/bin/activate`

## Voice (BẮT BUỘC)
OmniVoice local · male clone v2 · ref `voice-lock-vn-v2.wav` + `.ref.txt` · speed `1.2` · loudnorm ~−14 · `voice_locked:true`.  
CẤM: edge-tts · NamMinh · giọng nữ cũ (retired) · cloud · tắt clone · instruct-only sole lock · seed random.

## QA checklist
- [ ] ffprobe: 1080×1920, h264+aac, duration OK
- [ ] Voice: `voice_locked:true` + male clone v2
- [ ] Không bịa · không BGM · không karaoke burn trừ khi hỏi
- [ ] `qa/report.md` ngắn
- [ ] Handoff `JOB|status|version|path|next`

## Bàn giao mẫu
```
Job: HM-009 | Hoàn thành | v3-60s
Paths:
- .../output/storytelling_final.mp4
- .../voice_storytelling.wav
- .../subtitle.srt
- .../storytelling_script.txt
Ghi chú: HyperFrames · OmniVoice · male clone v2 locked · 1.2 · voice_locked:true · no karaoke burn · no BGM
```
