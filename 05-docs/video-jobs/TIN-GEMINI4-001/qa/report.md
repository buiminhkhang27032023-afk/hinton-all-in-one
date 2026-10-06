# QA report — TIN-GEMINI4-001 (v1)

- Engine: HyperFrames 0.8.114 (headless Chrome) · repo `/workspace/AI-auto-generate-video`
- Voice: OmniVoice · male clone v2 locked · 1.2 · voice_locked:true (health ref `voice-lock-vn-v2.wav`, speed_mode post)
- Script: 194 âm tiết · voice 44.83s · loudness {'I_LUFS': -13.9, 'TP_dBFS': -3.2}
- Captions burn: True · BGM: False · SRT sidecar: output/subtitle.srt
- Presenter: video · /workspace/hinton-pipeline-docs/assets/presenter-video-novoice.mp4 · crop=608:1072:656:0 · 14 PIP segments (no lip-sync)
- Shots: 21 body shots · hook 0–2.36s · outro 42.72–45.3s · mix {'video/demo': 10, 'kenburns': 3, 'textcard': 2, 'browser': 4, 'phone': 1, 'keyword': 1}
- ASR verify: similarity 0.704
- 1080p: {'file': '/workspace/video-jobs/TIN-GEMINI4-001/output/storytelling_final.mp4', 'size_mb': 22.93, 'duration': 45.3, 'video': 'h264 1080x1920 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- 720p: {'file': '/workspace/video-jobs/TIN-GEMINI4-001/output/storytelling_mobile_720p.mp4', 'size_mb': 5.69, 'duration': 45.3, 'video': 'h264 720x1280 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- Contact sheet: /workspace/video-jobs/TIN-GEMINI4-001/qa/contact_sheet.jpg (t=[1.81, 13.59, 27.18, 43.03])
- Times (s): {'tts': 1400.5, 'align': 39.0, 'asr_verify': 9.2, 'presenter': 94.3, 'compose': 17.4, 'hyperframes_render': 121.0, 'total_render_stage': 1696.1}

## Ghi chú / gaps
- script length 194 syllables (target 200-280)
- stock footage disabled in config
- yt-dlp FAILED for https://commons.wikimedia.org/wiki/File:Google_Data_Center.webm: ERROR: [wikimedia.org] Google_Data_Center.webm: Unable to extract video info; please report this issue on  https://github.com/yt-dlp/yt-dlp/issues?q= , filling out the appropriate issue template. Confirm you are on the latest version using  yt-dlp -U

- yt-dlp FAILED for https://commons.wikimedia.org/wiki/File:Server_room.webm: ERROR: [wikimedia.org] Server_room.webm: Unable to extract video info; please report this issue on  https://github.com/yt-dlp/yt-dlp/issues?q= , filling out the appropriate issue template. Confirm you are on the latest version using  yt-dlp -U

- yt-dlp FAILED for https://commons.wikimedia.org/wiki/File:Coding.webm: ERROR: [wikimedia.org] Coding.webm: Unable to extract video info; please report this issue on  https://github.com/yt-dlp/yt-dlp/issues?q= , filling out the appropriate issue template. Confirm you are on the latest version using  yt-dlp -U

- auto-editor (motion) presenter 54.0s -> 54.0s

## Nguồn footage (ghi nguồn khi đăng)
- Protein folding explained | Google DeepMind | https://www.youtube.com/watch?v=KpedmJdrTpY | NA

## Bàn giao
```
TIN-GEMINI4-001|Hoàn thành|v1-45s|/workspace/video-jobs/TIN-GEMINI4-001/output/storytelling_final.mp4|next=bố
```
