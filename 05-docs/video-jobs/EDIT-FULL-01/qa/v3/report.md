# QA report — EDIT-FULL-01 (v3)

- Engine: HyperFrames 0.8.114 (headless Chrome) · repo `/workspace/AI-auto-generate-video`
- Voice: OmniVoice · male clone v2 locked · 1.2 · voice_locked:true (health ref `voice-lock-vn-v2.wav`, speed_mode post)
- Script: 265 âm tiết · voice 58.59s · loudness {'I_LUFS': -14.0, 'TP_dBFS': -2.7}
- Captions burn: True · BGM: True · SRT sidecar: output/subtitle.srt
- Presenter: video (kallaway split/full-face) · /workspace/hinton-pipeline-docs/assets/presenter-video-novoice.mp4 · crop=608:1072:656:0 · 0 PIP segments (no lip-sync)
- Shots: 42 body shots · hook 0–1.18s · outro 58.86666666666667–58.86666666666667s · mix {'clip/bPjB9NRu8Jc.full': 2, 'face/face': 5, 'web/nobel_summary': 1, 'web/nobel_pr': 2, 'clip/nKnmhJSx1Xs.full': 1, 'phone/x_nobel': 1, 'photo/hassabis': 1, 'photo/jumper': 1, 'clip/2mzMKN8HbnY.full': 1, 'clip/r4-hXO7MLVU.full': 2, 'web/dm_nobel': 1, 'web/kva': 2, 'photo/baker': 1, 'render/r_top7': 1, 'render/r_hemo': 1, 'clip/KpedmJdrTpY.full': 1, 'web/af2_blog': 2, 'render/r_1ubq': 1, 'render/r_af_p53': 1, 'stat/stat': 3, 'web/af_200m': 1, 'web/af3_blog': 1, 'clip/9ufplEgtq8w.full': 2, 'render/r_nucleo': 1, 'web/nobel_pop': 1, 'render/r_btl': 1, 'render/r_petase': 1, 'web/bbc': 1, 'web/apnews': 1, 'phone/x_deepmind': 1}
- ASR verify: similarity 0.845
- 1080p: {'file': '/workspace/video-jobs/EDIT-FULL-01/output/v3/storytelling_final.mp4', 'size_mb': 41.27, 'duration': 58.867, 'video': 'h264 1080x1920 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- 720p: {'file': '/workspace/video-jobs/EDIT-FULL-01/output/v3/storytelling_mobile_720p.mp4', 'size_mb': 14.05, 'duration': 58.867, 'video': 'h264 720x1280 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- Contact sheet: /workspace/video-jobs/EDIT-FULL-01/qa/v3/contact_sheet.jpg (t=[2.35, 17.66, 35.32, 55.92])
- Times (s): {'tts': 3.5, 'align': 0.0, 'asr_verify': 0.0, 'presenter': 1.5, 'kallaway_render': 42.7, 'total_render_stage': 62.7}

## Ghi chú / gaps
- stock footage disabled in config
- screenshot timeout/error https://www.theguardian.com/science/2024/oct/09/google-deepmind-scientists-win-nobel-chemistry-prize: TimeoutExpired
- screenshot failed: https://www.theguardian.com/science/2024/oct/09/google-deepmind-scientists-win-nobel-chemistry-prize
- kallaway voice tighten {'in': 59.297, 'out': 58.585, 'pieces': 21}

## Nguồn footage (ghi nguồn khi đăng)
- AP Archive (YouTube 2mzMKN8HbnY)
- AP News (screenshot)
- AlphaFold DB model AF-P04637-F1 (EMBL-EBI/Google DeepMind, CC BY 4.0), render tools/protein_render.py
- Arthur Petron / WikiPortraits, Wikimedia Commons, CC BY-SA 4.0
- Associated Press (YouTube nKnmhJSx1Xs)
- BBC News (screenshot)
- Google DeepMind (YouTube 9ufplEgtq8w)
- Google DeepMind (YouTube r4-hXO7MLVU)
- Google DeepMind blog (screenshot)
- Google DeepMind blog 28/7/2022 (screenshot)
- Google DeepMind blog 30/11/2020 (screenshot)
- Google DeepMind — AlphaFold Server Demo (YouTube 9ufplEgtq8w)
- Google DeepMind — AlphaFold: The 50-year grand challenge cracked by AI (YouTube r4-hXO7MLVU)
- Google DeepMind — Protein folding explained (YouTube KpedmJdrTpY)
- Google blog — AlphaFold 3 (screenshot)
- Nobel Prize announcement slide (YouTube bPjB9NRu8Jc)
- Nobel Prize — Announcement of the 2024 Nobel Prize in Chemistry (YouTube bPjB9NRu8Jc)
- Render từ PDB 1BTL (RCSB) bằng tools/protein_render.py
- Render từ PDB 1KX5 (RCSB) bằng tools/protein_render.py
- Render từ PDB 1QYS (RCSB, CC0) bằng tools/protein_render.py
- Render từ PDB 1UBQ (RCSB) bằng tools/protein_render.py
- Render từ PDB 4HHB (RCSB) bằng tools/protein_render.py
- Render từ PDB 6EQE (RCSB) bằng tools/protein_render.py
- Royal Swedish Academy of Sciences kva.se (screenshot)
- WikiPortraits, Wikimedia Commons, CC BY-SA 4.0
- X post @GoogleDeepMind 1843960591792185695 (embed screenshot)
- X post @NobelPrize 1843951197960777760 (embed screenshot)
- kva.se (screenshot)
- nobelprize.org popular information (screenshot)
- nobelprize.org press release (screenshot)
- nobelprize.org summary page (screenshot)

## Bàn giao
```
EDIT-FULL-01|Hoàn thành|v3-59s|/workspace/video-jobs/EDIT-FULL-01/output/v3/storytelling_final.mp4|next=bố
```
