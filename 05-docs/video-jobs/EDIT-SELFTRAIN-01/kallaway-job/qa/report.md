# QA report — EDIT-SELFTRAIN-01 (r3)

- Engine: HyperFrames 0.8.114 (headless Chrome) · repo `/workspace/AI-auto-generate-video`
- Voice: OmniVoice · male clone v2 locked · 1.2 · voice_locked:true (health ref `voice-lock-vn-v2.wav`, speed_mode post)
- Script: 94 âm tiết · voice 19.55s · loudness {'I_LUFS': -14.0, 'TP_dBFS': -1.9}
- Captions burn: True · BGM: True · SRT sidecar: output/subtitle.srt
- Presenter: video (kallaway split/full-face) · /workspace/hinton-pipeline-docs/assets/presenter-video-novoice.mp4 · crop=608:1072:656:0 · 0 PIP segments (no lip-sync)
- Shots: 11 body shots · hook 0–1.12s · outro 19.833333333333332–19.833333333333332s · mix {'image': 5, 'face': 3, 'fx/terminal': 1, 'fx/escape': 1, 'fx/killswitch': 1}
- ASR verify: similarity 0.876
- 1080p: {'file': '/workspace/video-jobs/EDIT-SELFTRAIN-01/kallaway-job/output/storytelling_final.mp4', 'size_mb': 13.83, 'duration': 19.833, 'video': 'h264 1080x1920 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- 720p: {'file': '/workspace/video-jobs/EDIT-SELFTRAIN-01/kallaway-job/output/storytelling_mobile_720p.mp4', 'size_mb': 4.71, 'duration': 19.833, 'video': 'h264 720x1280 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- Contact sheet: /workspace/video-jobs/EDIT-SELFTRAIN-01/kallaway-job/qa/contact_sheet.jpg (t=[0.79, 5.95, 11.9, 18.84])
- Times (s): {'tts': 1.7, 'align': 0.0, 'asr_verify': 0.0, 'presenter': 1.5, 'kallaway_render': 17.8, 'total_render_stage': 27.5}

## Ghi chú / gaps
- stock footage disabled in config
- no broll_urls.txt -> no demo clips
- kallaway voice tighten {'in': 19.66, 'out': 19.555, 'pieces': 3}
- kallaway: beats.json (manual beat list)

## Nguồn footage (ghi nguồn khi đăng)

## Bàn giao
```
EDIT-SELFTRAIN-01|Hoàn thành|r3-20s|/workspace/video-jobs/EDIT-SELFTRAIN-01/kallaway-job/output/storytelling_final.mp4|next=bố
```
