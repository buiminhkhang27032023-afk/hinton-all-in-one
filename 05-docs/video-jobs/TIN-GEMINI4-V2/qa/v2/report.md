# QA report — TIN-GEMINI4-V2 (v2)

- Engine: HyperFrames 0.8.114 (headless Chrome) · repo `/workspace/AI-auto-generate-video`
- Voice: OmniVoice · male clone v2 locked · 1.2 · voice_locked:true (health ref `voice-lock-vn-v2.wav`, speed_mode post)
- Script: 265 âm tiết · voice 58.13s · loudness {'I_LUFS': -14.0, 'TP_dBFS': -2.5}
- Captions burn: True · BGM: True · SRT sidecar: output/subtitle.srt
- Presenter: video (kallaway split/full-face) · /workspace/hinton-pipeline-docs/assets/presenter-video-novoice.mp4 · crop=608:1072:656:0 · 0 PIP segments (no lip-sync)
- Shots: 40 body shots · hook 0–1.94s · outro 58.4–58.4s · mix {'clip/keyart': 1, 'face/face': 5, 'web/gblog': 11, 'clip/cnbc_ann': 2, 'web/reuters_tribune': 3, 'web/dm_cyber': 1, 'phone/x_gdm': 2, 'stat/stat': 5, 'clip/cnbc_chief': 2, 'clip/ev_table': 1, 'clip/ev_auto': 1, 'web/reuters_dd': 2, 'split/split': 3, 'web/tc': 1}
- ASR verify: similarity 0.782
- 1080p: {'file': '/workspace/video-jobs/TIN-GEMINI4-V2/output/v2/storytelling_final.mp4', 'size_mb': 45.15, 'duration': 58.4, 'video': 'h264 1080x1920 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- 720p: {'file': '/workspace/video-jobs/TIN-GEMINI4-V2/output/v2/storytelling_mobile_720p.mp4', 'size_mb': 16.2, 'duration': 58.4, 'video': 'h264 720x1280 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- Contact sheet: /workspace/video-jobs/TIN-GEMINI4-V2/qa/v2/contact_sheet.jpg (t=[2.34, 17.52, 35.04, 55.48])
- Times (s): {'tts': 4.1, 'align': 0.0, 'asr_verify': 0.0, 'presenter': 1.9, 'kallaway_render': 46.3, 'total_render_stage': 72.8}

## Ghi chú / gaps
- stock footage disabled in config
- screenshot timeout/error https://qz.com/google-gemini-4-argon-ai-model-cybersecurity-100126: TimeoutExpired
- screenshot failed: https://qz.com/google-gemini-4-argon-ai-model-cybersecurity-100126
- broll keyart: ok
- broll ev_deepswe: ok
- broll ev_vals: ok
- broll ev_auto: ok
- broll ev_cwe: ok
- broll ev_table: ok
- portrait pichai: ok
- varun: missing screenshots ['web:qz']
- kallaway voice tighten {'in': 58.961, 'out': 58.13, 'pieces': 23}

## Nguồn footage (ghi nguồn khi đăng)
- CNBC — Google announces new frontier model called Gemini 4 Argon (30/09/2026)
- CNBC — Google's Gemini product chief details weeks of company-wide testing (30/09/2026)
- Google DeepMind — bảng benchmark Gemini 4 Argon (X @GoogleDeepMind)
- Google — Gemini 4 Argon evals: AutomationBench (blog.google)
- Google — Gemini 4 key art (blog.google)
- Lukasz Kobus / European Commission, Wikimedia Commons, CC BY 4.0 + Screenshot https://www.devdiscourse.com/article/international/3984852-google-announces-gemini-4-flagship-ai-model-after-months-of-delays
- Screenshot https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/
- Screenshot https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/ + Screenshot https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/
- Screenshot https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/ + Screenshot https://platform.twitter.com/embed/Tweet.html?id=2105388084154056939&theme=light&lang=en
- Screenshot https://deepmind.google/models/gemini/cyber/
- Screenshot https://platform.twitter.com/embed/Tweet.html?id=2105388084154056939&theme=light&lang=en
- Screenshot https://techcrunch.com/2026/09/30/google-releases-gemini-4-argon-called-its-most-powerful-model-yet/
- Screenshot https://tribune.com.pk/story/2632456/google-announces-gemini-4-flagship-ai-model-after-months-of-delays
- Screenshot https://www.devdiscourse.com/article/international/3984852-google-announces-gemini-4-flagship-ai-model-after-months-of-delays

## Bàn giao
```
TIN-GEMINI4-V2|Hoàn thành|v2-58s|/workspace/video-jobs/TIN-GEMINI4-V2/output/v2/storytelling_final.mp4|next=bố
```

## Form fixes applied (v1 → v2)

- **big text**: `big="MẠNH CỠ NÀO?"` → `big="MẠNH?"` (safe-zone pass; no edge cut-off).
- **CNBC / 16:9 clips**: `mode=fit` → `mode=cover` + zoom 1.15–1.25 (keyart, cnbc_ann, cnbc_chief, ev_table, ev_auto) — no letterbox blur bars.
- **Evidence upper half**: web/phone cues set `cy≈0.32–0.36`, `z1≈1100–1300`, `zr=1.12` so OCR highlights sit above caption band; Devdiscourse headline zoomed (`z1=1100 cy=0.32`).
- **Source chip vs caption**: `chip_y=1280` (above), `cap_top=1465` (bottom band); shortened long labels (CNBC · Argon nội bộ, Reuters · Tribune/Devdiscourse, FrontierSWE · GPT hơn, Terminal · Opus hơn, DeepMind · tự công bố, …).
- **Captions shorter**: caption_map maps long clusters (`51,3% AutoBench`, `77,9% DeepSWE`, `91,7% LVBench`, `và 10 USD`); avoids lone “và” / long “trên AutomationBench”.
- **Stat card width**: `"1 TRIỆU"` → `"1M"` on output-token card (side margins).
- **Glyph**: removed unsupported `→` from chip label (`C sang Rust`).

## QA
- **TỔNG: ĐẠT (20/20)** — see `QA-v2.md`.
- Remaining visual note (not QA-fail): full-frame `mode=cover` still paints evidence into the lower third under chips/captions; highlights intentionally kept upper. Phone X table at ~27s still dense under chip — tight zoom on 51.3% helps but table rows remain behind bottom band.

## Outputs
- `/workspace/video-jobs/TIN-GEMINI4-V2/output/v2/storytelling_final.mp4` — 1080x1920 · 58.4s · ~44 MB
- `/workspace/video-jobs/TIN-GEMINI4-V2/output/v2/storytelling_mobile_720p.mp4` — 720x1280 sibling
