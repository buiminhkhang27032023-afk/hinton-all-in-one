# QA report — EDIT-FULL-02 (v1)

- Engine: HyperFrames 0.8.114 (headless Chrome) · repo `/workspace/AI-auto-generate-video`
- Voice: OmniVoice · male clone v2 locked · 1.2 · voice_locked:true (health ref `voice-lock-vn-v2.wav`, speed_mode post)
- Script: 248 âm tiết · voice 52.26s · loudness {'I_LUFS': -14.0, 'TP_dBFS': -2.5}
- Captions burn: True · BGM: True · SRT sidecar: output/subtitle.srt
- Presenter: video (kallaway split/full-face) · /workspace/hinton-pipeline-docs/assets/presenter-video-novoice.mp4 · crop=608:1072:656:0 · 0 PIP segments (no lip-sync)
- Shots: 40 body shots · hook 0–1.3s · outro 52.53333333333333–52.53333333333333s · mix {'clip/v01': 1, 'phone/x_dots': 1, 'face/face': 4, 'clip/v06': 1, 'stat/stat': 6, 'clip/keynote': 6, 'web/recap': 2, 'clip/v12': 1, 'web/dots': 4, 'split/split': 4, 'clip/v20': 1, 'web/sol': 6, 'clip/v37': 1, 'clip/v32': 1, 'web/wired': 1}
- ASR verify: similarity 0.758
- 1080p: {'file': '/workspace/video-jobs/EDIT-FULL-02/output/v1/storytelling_final.mp4', 'size_mb': 28.77, 'duration': 52.533, 'video': 'h264 1080x1920 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- 720p: {'file': '/workspace/video-jobs/EDIT-FULL-02/output/v1/storytelling_mobile_720p.mp4', 'size_mb': 10.62, 'duration': 52.533, 'video': 'h264 720x1280 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- Contact sheet: /workspace/video-jobs/EDIT-FULL-02/qa/v1/contact_sheet.jpg (t=[2.1, 15.76, 31.52, 49.91])
- Times (s): {'tts': 4.3, 'align': 0.0, 'asr_verify': 0.0, 'presenter': 1.5, 'kallaway_render': 42.1, 'total_render_stage': 61.6}

## Ghi chú / gaps
- script length 248 syllables (target 250-270)
- stock footage disabled in config
- broll v01: ok
- broll v13: ok
- broll v06: ok
- broll v08: ok
- broll v12: ok
- broll v16: ok
- broll v19: ok
- broll v20: ok
- broll v22: ok
- broll v23: ok
- broll v26: ok
- broll v32: ok
- broll v37: ok
- broll v40: ok
- broll v47: ok
- kallaway voice tighten {'in': 52.584, 'out': 52.255, 'pieces': 23}

## Nguồn footage (ghi nguồn khi đăng)
- OpenAI — DevDay 2026 Keynote (FULL) (YouTube Fls_onRviPM)
- OpenAI — DevDay 2026 Recap (openai.com) + OpenAI — Introducing dots (openai.com)
- OpenAI — GPT-6.1 Sol (openai.com)
- OpenAI — GPT-6.1 Sol / Luna art (openai.com)
- OpenAI — GPT-6.1 Sol key art (openai.com)
- OpenAI — Introducing dots (openai.com)
- OpenAI — Introducing dots (video, X @OpenAI 2104984504133918973)
- OpenAI — dots art card (openai.com)
- Screenshot https://openai.com/index/devday-2026-recap
- Screenshot https://openai.com/index/devday-2026-recap + OpenAI — Introducing dots (openai.com)
- Screenshot https://openai.com/index/introducing-dots/
- Screenshot https://openai.com/index/introducing-dots/ + OpenAI — Dots Vision Film (openai.com)
- Screenshot https://openai.com/index/introducing-gpt-6-1-sol/
- Screenshot https://openai.com/index/introducing-gpt-6-1-sol/ + OpenAI — DevDay 2026 Keynote (FULL) (YouTube Fls_onRviPM)
- Screenshot https://platform.twitter.com/embed/Tweet.html?id=2104984504133918973&theme=light&lang=en
- Screenshot wired.com/story/openai-dots-always-on-ai-agents

## Bàn giao
```
EDIT-FULL-02|Hoàn thành|v1-53s|/workspace/video-jobs/EDIT-FULL-02/output/v1/storytelling_final.mp4|next=bố
```
