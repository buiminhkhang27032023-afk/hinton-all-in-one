# QA report — TEST-CHU-DE-MOI (v1)

- Engine: HyperFrames 0.8.114 (headless Chrome) · repo `/workspace/AI-auto-generate-video`
- Voice: OmniVoice · male clone v2 locked · 1.2 · voice_locked:true (health ref `voice-lock-vn-v2.wav`, speed_mode post)
- Script: 114 âm tiết · voice 26.16s · loudness {'I_LUFS': -14.0, 'TP_dBFS': -2.8}
- Captions burn: True · BGM: True · SRT sidecar: output/subtitle.srt
- Presenter: video (kallaway split/full-face) · /workspace/hinton-pipeline-docs/assets/presenter-video-novoice.mp4 · crop=608:1072:656:0 · 0 PIP segments (no lip-sync)
- Shots: 1 body shots · hook 0–26.433333333333334s · outro 26.433333333333334–26.433333333333334s · mix {'video': 1}
- ASR verify: similarity 0.886
- 1080p: {'file': '/workspace/video-jobs/TEST-CHU-DE-MOI/output/v1/storytelling_final.mp4', 'size_mb': 24.37, 'duration': 26.433, 'video': 'h264 1080x1920 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- 720p: {'file': '/workspace/video-jobs/TEST-CHU-DE-MOI/output/v1/storytelling_mobile_720p.mp4', 'size_mb': 7.91, 'duration': 26.433, 'video': 'h264 720x1280 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- Contact sheet: /workspace/video-jobs/TEST-CHU-DE-MOI/qa/v1/contact_sheet.jpg (t=[1.06, 7.93, 15.86, 25.11])
- Times (s): {'tts': 673.0, 'align': 19.6, 'asr_verify': 5.0, 'presenter': 1.5, 'kallaway_render': 28.2, 'total_render_stage': 736.8}

## Ghi chú / gaps
- stock footage disabled in config
- kallaway voice tighten {'in': 26.405, 'out': 26.158, 'pieces': 20}
- kallaway: beats.json (manual beat list)

## Nguồn footage (ghi nguồn khi đăng)
- Wikimedia Commons File:Smithy- steel forging (2).webm — CC BY 3.0, Sounds of Changes / Museum of Municipal Engineering; video Piotr Leszczyński. https://commons.wikimedia.org/wiki/File:Smithy-_steel_forging_(2).webm

## Bàn giao
```
TEST-CHU-DE-MOI|Hoàn thành|v1-26s|/workspace/video-jobs/TEST-CHU-DE-MOI/output/v1/storytelling_final.mp4|next=bố
```
