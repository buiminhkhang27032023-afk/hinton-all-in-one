# HM-101 v2 — report

- **Job:** HM-101 · remake v2 (anh chê v1: ít animation / lặp 2 ảnh)
- **Engine:** HyperFrames 0.8.114 (`lam-viec/hf_v2/`)
- **Voice:** REUSED from v1 (`voice_storytelling.wav` / `lam-viec/voice.wav`) — **no TTS / no OmniVoice**
- **Duration:** 51.77s · 1080×1920@30 H.264/AAC yuv420p + mobile 720×1280
- **Assets:** 27 distinct files logged in `qa/assets.md` (≥15 required)
- **Scenes:** 22 unique scenes (1 per sentence), no consecutive same full-frame image
- **Animation features:** kinetic claim captions; counters (6 / 5 / 5 Olympiad / 384 / 2015 / 5000); flow diagram Người→AI→Nhóm thẩm định; mock meta.ai chat typing; card 3D tilt/parallax; browser highlight/underline; slide/whip/rotate scene ins; Ken Burns with power2/power3 easing; bold #F5C518 claim captions
- **PIP / presenter:** sparse — full presenter intro 0–2.2s + outro 49.44–51.74s + PIP only on chat + 5.000 Home Link beats → **≈18.8%** of runtime (≤30%)
- **BGM:** none · **karaoke burn:** none (SRT sidecar only) · **claims:** unchanged from v1 script
- **Outputs:**
  - `/workspace/video-jobs/HM-101/output/storytelling_final_v2.mp4` (26051352 bytes)
  - `/workspace/video-jobs/HM-101/output/storytelling_mobile_720p_v2.mp4` (6266412 bytes)
  - `/workspace/video-jobs/HM-101/output/subtitle_v2.srt`
  - `/workspace/video-jobs/HM-101/qa/contact_sheet_v2.jpg` (12 unique frames)
- **ffprobe final:** 1080x1920 h264+aac duration≈51.77s
- **Gaps / notes:** India Today Access Denied — substituted Muse Home Link from gadgets.muse.ai; paper covers = designed cards + arXiv abs screenshots citing Meta blog links; first render attempt failed JS (`-100%` unquoted) then fixed and re-rendered with timeline ready
- **Lock:** render wrapped in `flock /workspace/video-jobs/.render.lock`
- **v1 preserved:** `storytelling_final.mp4` / `voice_storytelling.wav` untouched
