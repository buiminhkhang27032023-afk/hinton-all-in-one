# QA report — EDIT-FULL-01 (v4)

- Engine: HyperFrames 0.8.114 (headless Chrome) · repo `/workspace/AI-auto-generate-video`
- Voice: OmniVoice · male clone v2 locked · 1.2 · voice_locked:true (health ref `voice-lock-vn-v2.wav`, speed_mode post)
- Script: 265 âm tiết · voice 58.59s · loudness {'I_LUFS': -14.0, 'TP_dBFS': -2.7}
- Captions burn: True · BGM: True · SRT sidecar: output/subtitle.srt
- Presenter: video (kallaway split/full-face) · /workspace/hinton-pipeline-docs/assets/presenter-video-novoice.mp4 · crop=608:1072:656:0 · 0 PIP segments (no lip-sync)
- Shots: 42 body shots · hook 0–1.18s · outro 58.86666666666667–58.86666666666667s · mix {'clip/nobel_ann': 2, 'face/face': 5, 'web/nobel_summary': 1, 'web/nobel_pr': 2, 'clip/ap_hall': 1, 'phone/x_nobel': 1, 'photo/hassabis': 1, 'photo/jumper': 1, 'clip/ap_dm': 1, 'clip/dm_50yr': 2, 'web/dm_nobel': 1, 'web/kva': 1, 'photo/baker': 1, 'split/split': 3, 'render/r_hemo': 1, 'clip/dm_explained': 1, 'web/af2_blog': 2, 'render/r_1ubq': 1, 'render/r_af_p53': 1, 'stat/stat': 4, 'web/af_200m': 1, 'web/af3_blog': 1, 'clip/af_server': 2, 'render/r_nucleo': 1, 'render/r_petase': 1, 'phone/x_deepmind': 1, 'clip/dm_making': 2}
- ASR verify: similarity 0.845
- 1080p: {'file': '/workspace/video-jobs/EDIT-FULL-01/output/v4/storytelling_final.mp4', 'size_mb': 39.74, 'duration': 58.867, 'video': 'h264 1080x1920 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- 720p: {'file': '/workspace/video-jobs/EDIT-FULL-01/output/v4/storytelling_mobile_720p.mp4', 'size_mb': 13.59, 'duration': 58.867, 'video': 'h264 720x1280 30/1 yuv420p', 'audio': 'aac 48000Hz ch=2'}
- Contact sheet: /workspace/video-jobs/EDIT-FULL-01/qa/v4/contact_sheet.jpg (t=[2.35, 17.66, 35.32, 55.92])
- Times (s): {'tts': 3.6, 'align': 0.0, 'asr_verify': 0.0, 'presenter': 1.5, 'kallaway_render': 44.8, 'total_render_stage': 64.1}

## Ghi chú / gaps
- stock footage disabled in config
- kallaway voice tighten {'in': 59.297, 'out': 58.585, 'pieces': 21}

## Nguồn footage (ghi nguồn khi đăng)
- AP Archive (YouTube 2mzMKN8HbnY)
- AlphaFold DB AF-P04637 (EMBL-EBI/Google DeepMind, CC BY 4.0), render tools/protein_render.py
- Arthur Petron / WikiPortraits, Wikimedia Commons, CC BY-SA 4.0
- Associated Press (YouTube nKnmhJSx1Xs)
- Google DeepMind — AlphaFold Server Demo (YouTube 9ufplEgtq8w)
- Google DeepMind — AlphaFold: The 50-year grand challenge cracked by AI (YouTube r4-hXO7MLVU)
- Google DeepMind — Protein folding explained (YouTube KpedmJdrTpY)
- Google DeepMind — The Making of AlphaFold (YouTube gg7WjuFs8F4)
- Nobel Prize — Announcement of the 2024 Nobel Prize in Chemistry (YouTube bPjB9NRu8Jc)
- PDB 1BTL (RCSB), render tools/protein_render.py + Screenshot https://www.bbc.com/news/articles/czrm0p2mxvyo
- PDB 1KX5 (RCSB), render tools/protein_render.py
- PDB 1UBQ (RCSB), render tools/protein_render.py
- PDB 4HHB (RCSB), render tools/protein_render.py
- PDB 6EQE (RCSB), render tools/protein_render.py
- Screenshot https://blog.google/technology/ai/google-deepmind-isomorphic-alphafold-3-ai-model/
- Screenshot https://deepmind.google/blog/demis-hassabis-john-jumper-awarded-nobel-prize-in-chemistry/
- Screenshot https://deepmind.google/discover/blog/alphafold-a-solution-to-a-50-year-old-grand-challenge-in-biology/
- Screenshot https://deepmind.google/discover/blog/alphafold-reveals-the-structure-of-the-protein-universe/
- Screenshot https://platform.twitter.com/embed/Tweet.html?id=1843951197960777760&theme=light&lang=en
- Screenshot https://platform.twitter.com/embed/Tweet.html?id=1843960591792185695&theme=light&lang=en
- Screenshot https://www.bbc.com/news/articles/czrm0p2mxvyo + Screenshot https://apnews.com/article/nobel-chemistry-prize-56f4d9e90591dfe7d9d840a8c8c9d553
- Screenshot https://www.kva.se/en/news/the-nobel-prize-in-chemistry-2024/
- Screenshot https://www.kva.se/en/news/the-nobel-prize-in-chemistry-2024/ + PDB 1QYS (RCSB), render tools/protein_render.py
- Screenshot https://www.nobelprize.org/prizes/chemistry/2024/press-release/
- Screenshot https://www.nobelprize.org/prizes/chemistry/2024/summary/
- WikiPortraits, Wikimedia Commons, CC BY-SA 4.0

## Bàn giao
```
EDIT-FULL-01|Hoàn thành|v4-59s|/workspace/video-jobs/EDIT-FULL-01/output/v4/storytelling_final.mp4|next=bố
```
