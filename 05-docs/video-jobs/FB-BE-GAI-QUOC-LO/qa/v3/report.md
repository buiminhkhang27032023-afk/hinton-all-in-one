# QA report — FB-BE-GAI-QUOC-LO (v3)

- Engine: HyperFrames 0.8.114 (headless Chrome) · repo `/workspace/AI-auto-generate-video`
- Voice: OmniVoice · male clone v2 locked · 1.2 · voice_locked:true (health ref `voice-lock-vn-v2.wav`, speed_mode post)
- Script: 137 âm tiết · voice 27.99s · loudness {'I_LUFS': -14.0, 'TP_dBFS': -2.7}
- Captions burn: True · BGM: True · SRT sidecar: output/subtitle.srt
- Presenter: video (kallaway split/full-face) · /workspace/hinton-pipeline-docs/assets/presenter-video-novoice.mp4 · crop=608:1072:656:0 · 0 PIP segments (no lip-sync)
- Shots: 1 body shots · hook 0–28.266666666666666s · outro 28.266666666666666–28.266666666666666s · mix {'video': 1}
- ASR verify: similarity 0.926
- 1080p: {'file': '/workspace/video-jobs/FB-BE-GAI-QUOC-LO/output/v3/storytelling_final.mp4', 'size_mb': 22.08, 'duration': 28.267, 'video': 'h264 1080x1920 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- 720p: {'file': '/workspace/video-jobs/FB-BE-GAI-QUOC-LO/output/v3/storytelling_mobile_720p.mp4', 'size_mb': 7.41, 'duration': 28.267, 'video': 'h264 720x1280 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- Contact sheet: /workspace/video-jobs/FB-BE-GAI-QUOC-LO/qa/v3/contact_sheet.jpg (t=[1.13, 8.48, 16.96, 26.85])
- Times (s): {'tts': 3.1, 'align': 0.0, 'asr_verify': 0.0, 'presenter': 1.5, 'kallaway_render': 20.6, 'total_render_stage': 33.6}

## Ghi chú / gaps
- script length 137 syllables (target 250-270)
- stock footage disabled in config
- kallaway voice tighten {'in': 28.227, 'out': 27.988, 'pieces': 18}
- kallaway: beats.json (manual beat list)

## Nguồn footage (ghi nguồn khi đăng)
- CCTV crop of Facebook watch 1599860208291400 (road only, no host)

## Bàn giao
```
FB-BE-GAI-QUOC-LO|Hoàn thành|v3-28s|/workspace/video-jobs/FB-BE-GAI-QUOC-LO/output/v3/storytelling_final.mp4|next=bố
```
