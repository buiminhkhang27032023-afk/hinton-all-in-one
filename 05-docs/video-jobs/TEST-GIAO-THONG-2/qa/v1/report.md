# QA report — TEST-GIAO-THONG-2 (v1)

- Engine: HyperFrames 0.8.114 (headless Chrome) · repo `/workspace/AI-auto-generate-video`
- Voice: OmniVoice · male clone v2 locked · 1.2 · voice_locked:true (health ref `voice-lock-vn-v2.wav`, speed_mode post)
- Script: 134 âm tiết · voice 29.17s · loudness {'I_LUFS': -14.0, 'TP_dBFS': -2.8}
- Captions burn: True · BGM: True · SRT sidecar: output/subtitle.srt
- Presenter: video (kallaway split/full-face) · /workspace/hinton-pipeline-docs/assets/presenter-video-novoice.mp4 · crop=608:1072:656:0 · 0 PIP segments (no lip-sync)
- Shots: 1 body shots · hook 0–29.433333333333334s · outro 29.433333333333334–29.433333333333334s · mix {'video': 1}
- ASR verify: similarity 0.503
- 1080p: {'file': '/workspace/video-jobs/TEST-GIAO-THONG-2/output/v1/storytelling_final.mp4', 'size_mb': 22.51, 'duration': 29.433, 'video': 'h264 1080x1920 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- 720p: {'file': '/workspace/video-jobs/TEST-GIAO-THONG-2/output/v1/storytelling_mobile_720p.mp4', 'size_mb': 7.49, 'duration': 29.433, 'video': 'h264 720x1280 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- Contact sheet: /workspace/video-jobs/TEST-GIAO-THONG-2/qa/v1/contact_sheet.jpg (t=[1.18, 8.83, 17.66, 27.96])
- Times (s): {'tts': 72.7, 'align': 22.0, 'asr_verify': 13.1, 'presenter': 1.6, 'kallaway_render': 29.6, 'total_render_stage': 148.6}

## Ghi chú / gaps
- stock footage disabled in config
- kallaway voice tighten {'in': 29.395, 'out': 29.168, 'pieces': 18}
- kallaway: beats.json (manual beat list)

## Nguồn footage (ghi nguồn khi đăng)
- Wikimedia Commons File:Connect to the opposite lane and bypass the traffic accident section.webm — Public domain (CCTV/dashcam footage does not create a copyright; author: none/unknown, originally posted at https://www.douyin.com/video/7464167816963296569). https://commons.wikimedia.org/wiki/File:Connect_to_the_opposite_lane_and_bypass_the_traffic_accident_section.webm

## Bàn giao
```
TEST-GIAO-THONG-2|Hoàn thành|v1-29s|/workspace/video-jobs/TEST-GIAO-THONG-2/output/v1/storytelling_final.mp4|next=bố
```
