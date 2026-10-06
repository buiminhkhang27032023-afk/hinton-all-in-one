# QA report — HM-101 (v1)

- Engine: HyperFrames 0.8.114 (headless Chrome) · repo `/workspace/AI-auto-generate-video`
- Voice: OmniVoice · male clone v2 locked · 1.2 · voice_locked:true (health ref `voice-lock-vn-v2.wav`, speed_mode post)
- Script: 250 âm tiết · voice 51.74s · loudness {'I_LUFS': -13.9, 'TP_dBFS': -3.4}
- Captions burn: False · BGM: False · SRT sidecar: output/subtitle.srt
- Presenter: video · /workspace/hinton-pipeline-docs/assets/presenter-video-novoice.mp4 · crop=608:1072:656:0 · 20 PIP segments (no lip-sync)
- Shots: 20 body shots · hook 0–2.26s · outro 49.56–52.2s · mix {'kenburns': 8, 'browser': 8, 'textcard': 2, 'phone': 1, 'keyword': 1}
- ASR verify: similarity 0.864
- 1080p: {'file': '/workspace/video-jobs/HM-101/output/storytelling_final.mp4', 'size_mb': 31.82, 'duration': 52.2, 'video': 'h264 1080x1920 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- 720p: {'file': '/workspace/video-jobs/HM-101/output/storytelling_mobile_720p.mp4', 'size_mb': 6.6, 'duration': 52.2, 'video': 'h264 720x1280 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- Contact sheet: /workspace/video-jobs/HM-101/qa/contact_sheet.jpg (t=[2.09, 15.66, 31.32, 49.59])
- Times (s): {'tts': 737.6, 'align': 32.4, 'asr_verify': 6.7, 'presenter': 50.7, 'compose': 0.0, 'hyperframes_render': 63.0, 'total_render_stage': 900.3}

## Ghi chú / gaps
- stock footage SKIPPED: no PEXELS_API_KEY / PIXABAY_API_KEY env var
- no broll_urls.txt -> no demo clips
- voice duration 51.7s is far from target 60s
- auto-editor (motion) presenter 54.0s -> 54.0s

## Nguồn footage (ghi nguồn khi đăng)

## Bàn giao
```
HM-101|Hoàn thành|v1-52s|/workspace/video-jobs/HM-101/output/storytelling_final.mp4|next=bố
```
