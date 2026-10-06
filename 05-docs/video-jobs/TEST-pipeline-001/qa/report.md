# QA report — TEST-pipeline-001 (v1)

- Engine: HyperFrames 0.8.114 (headless Chrome) · repo `/workspace/AI-auto-generate-video`
- Voice: OmniVoice · male clone v2 locked · 1.2 · voice_locked:true (health ref `voice-lock-vn-v2.wav`, speed_mode post)
- Script: 78 âm tiết · voice 18.71s · loudness {'I_LUFS': -13.9, 'TP_dBFS': -3.1}
- Captions burn: False · BGM: False · SRT sidecar: output/subtitle.srt
- Presenter: video · /workspace/hinton-pipeline-docs/assets/presenter-video-novoice.mp4 · crop=608:1072:656:0 · 6 PIP segments (no lip-sync)
- Shots: 5 body shots · hook 0–1.508s · outro 16.242–19.167s · mix {'video/demo': 3, 'kenburns': 1, 'textcard': 1}
- ASR verify: similarity 0.88
- 1080p: {'file': '/workspace/video-jobs/TEST-pipeline-001/output/storytelling_final.mp4', 'size_mb': 13.27, 'duration': 19.2, 'video': 'h264 1080x1920 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- 720p: {'file': '/workspace/video-jobs/TEST-pipeline-001/output/storytelling_mobile_720p.mp4', 'size_mb': 3.19, 'duration': 19.2, 'video': 'h264 720x1280 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- Contact sheet: /workspace/video-jobs/TEST-pipeline-001/qa/contact_sheet.jpg (t=[0.77, 5.76, 11.52, 18.24])
- Times (s): {'tts': 567.7, 'align': 0.0, 'asr_verify': 0.0, 'presenter': 72.4, 'compose': 5.9, 'hyperframes_render': 58.7, 'total_render_stage': 712.6}

## Ghi chú / gaps
- stock footage SKIPPED: no PEXELS_API_KEY / PIXABAY_API_KEY env var
- auto-editor (motion) presenter 54.0s -> 54.0s

## Nguồn footage (ghi nguồn khi đăng)
- Protein Folding | Cookatoo.ergo.ZooM | https://commons.wikimedia.org/wiki/File:Protein_Folding.ogv | Creative Commons Attribution-Share Alike 4.0
- Visualisation of the SARS-CoV-2 Omicron Spike Protein | Maximilian Schönherr | https://commons.wikimedia.org/wiki/File:Visualisation_of_the_SARS-CoV-2_Omicron_Spike_Protein.webm | Creative Commons Attribution-Share Alike 4.0

## Bàn giao
```
TEST-pipeline-001|Hoàn thành|v1-19s|/workspace/video-jobs/TEST-pipeline-001/output/storytelling_final.mp4|next=bố
```
