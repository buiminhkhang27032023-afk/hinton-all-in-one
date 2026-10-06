
### Nhóm 1 — Tự động tạo short end-to-end (14 repo)

| # | Repo | ⭐ Stars | Commit cuối (ICT) | License | Ngôn ngữ | Làm gì | CPU/GPU | Hợp pipeline (★1–5) |
|---|---|---:|---|---|---|---|---|---|
| 1 | [harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) | 128,199 | 2026-10-03 | MIT | Python | Chủ đề → kịch bản LLM → TTS → tự tìm footage Pexels/Pixabay theo keyword → phụ đề → BGM → render (MoviePy); WebUI/API/CLI | ✅ CPU | ★★★★ Gần pipeline nhất. Mượn module tìm/ghép B-roll + timing phụ đề; thay TTS bằng OmniVoice; tự thêm PIP mặt |
| 2 | [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) | 62,604 | 2026-09-06 | AGPL-3.0 | Python | Hệ thống sản xuất video agentic: 12 pipeline, research→script→asset (stock/AI)→dựng bằng Remotion | ✅ CPU (gen model qua API) | ★★ Tham khảo kiến trúc agent + kho footage free; nặng, AGPL (lây license nếu phân phối/dịch vụ) |
| 3 | [ATH-MaaS/Pixelle-Video](https://github.com/ATH-MaaS/Pixelle-Video) | 28,606 | 2026-06-14 | Apache-2.0 | Python | Chủ đề → văn án → ảnh/video AI (ComfyUI/RunningHub/API) → TTS → BGM → ghép; có pipeline 数字人口播 | ⚠️ Điều phối CPU, ảnh/video AI cần GPU/API | ★★ Hướng 'ảnh AI minh hoạ', không phải tin tức + footage thật; tham khảo template |
| 4 | [hypit-ai/hypit](https://github.com/hypit-ai/hypit) | 19,010 | 2026-10-03 | Apache-2.0 sửa đổi | TypeScript | Agent skill 'clone' video viral: footage, caption, B-roll, effect neo theo TỪ (SVML), WhisperX align | ✅ CPU phần dựng (gen model tuỳ chọn/API) | ★★★ Ý tưởng neo B-roll/caption theo từ rất hợp; còn mới, cần thử; license Apache sửa đổi (cấm multi-tenant SaaS) |
| 5 | [chatfire-AI/huobao-drama](https://github.com/chatfire-AI/huobao-drama) | 15,646 | 2026-10-02 | CC BY-NC-SA 4.0 | Vue | Nền tảng tạo phim ngắn (短剧) từ 1 câu: kịch bản → nhân vật → ảnh/video AI → ghép | ⚠️ Cần API/GPU cho gen | ★ Khác thể loại; CC BY-NC-SA 4.0 (phi thương mại) |
| 6 | [FujiwaraChoki/MoneyPrinter](https://github.com/FujiwaraChoki/MoneyPrinter) | 14,018 | 2026-03-27 | MIT | Python | Bản gốc: tự tạo YouTube Shorts bằng MoviePy + stock footage | ✅ CPU | ★★ Đã bị MoneyPrinterTurbo vượt; chỉ tham khảo |
| 7 | [krillinai/OpenCreator](https://github.com/krillinai/OpenCreator) | 12,579 | 2026-10-03 | Apache-2.0 | TypeScript | Workspace AI cho creator (trước là KrillinAI): dịch/lồng tiếng video, avatar, edit | ⚠️ CPU + nhiều API | ★★ Mạnh về dịch/lồng tiếng; không trọng tâm short tin tức |
| 8 | [HKUDS/ViMax](https://github.com/HKUDS/ViMax) | 12,538 | 2026-09-30 | MIT | Python | Video agentic: đạo diễn/biên kịch/producer + model gen video | ❌ Cần API/GPU gen video | ★ Thiên về phim AI, không phải tin + footage |
| 9 | [elebumm/RedditVideoMakerBot](https://github.com/elebumm/RedditVideoMakerBot) | 12,537 | 2026-03-18 | GPL-3.0 | Python | Bài Reddit → TTS + screenshot + video nền → MP4 | ✅ CPU | ★ Format khác (Reddit); GPL-3.0 |
| 10 | [linyqh/NarratoAI](https://github.com/linyqh/NarratoAI) | 11,274 | 2026-09-17 | MIT | Python | LLM xem video có sẵn → viết lời bình → cắt cảnh khớp lời → TTS → phụ đề | ✅ CPU (≥4 core, 8GB RAM) | ★★★ Hợp dạng 'bình luận clip demo/keynote'; tham khảo logic khớp cảnh ↔ lời |
| 11 | [RayVentura/ShortGPT](https://github.com/RayVentura/ShortGPT) | 7,997 | 2025-02-11 | MIT | Python | Framework tự động YouTube Shorts/TikTok: script, TTS, footage, caption, dịch | ✅ CPU | ★★ Commit cuối 02/2025 – gần như ngừng; chỉ tham khảo |
| 12 | [GuanYixuan/pyJianYingDraft](https://github.com/GuanYixuan/pyJianYingDraft) | 4,472 | 2026-09-26 | Apache-2.0 | Python | Python sinh draft 剪映/CapCut (track, text, effect) để mở/xuất trong app | ✅ CPU (cần app JianYing/CapCut Windows/mac để xuất) | ★★ Hợp nếu muốn người dựng tinh chỉnh trên CapCut; không render trên Linux |
| 13 | [FireRedTeam/FireRed-OpenStoryline](https://github.com/FireRedTeam/FireRed-OpenStoryline) | 3,456 | 2026-07-31 | Apache-2.0 | Python | Agent edit video bằng ngôn ngữ tự nhiên (chọn cảnh, nhạc, phụ đề) | ⚠️ CPU + LLM/VLM API | ★★ Tham khảo workflow 'edit theo ý định' |
| 14 | [SamurAIGPT/Text-To-Video-AI](https://github.com/SamurAIGPT/Text-To-Video-AI) | 835 | 2026-08-24 | MIT | Jupyter Notebook | Text → script → TTS → tìm video Pexels → caption → ghép | ✅ CPU | ★★ Bản tối giản dễ đọc của ý tưởng MoneyPrinterTurbo |

### Nhóm 2 — Dựng/render bằng code (11 repo)

| # | Repo | ⭐ Stars | Commit cuối (ICT) | License | Ngôn ngữ | Làm gì | CPU/GPU | Hợp pipeline (★1–5) |
|---|---|---:|---|---|---|---|---|---|
| 1 | [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | 61,663 | 2026-10-03 | Remotion License (source-available) | TypeScript | Dựng video bằng React (TSX) → MP4 qua headless Chromium; có @remotion/captions | ✅ CPU (chậm hơn ffmpeg, ~2–4GB RAM/luồng) | ★★★ Mạnh nhưng trùng vai HyperFrames; license riêng: miễn phí cá nhân/công ty ≤3 người, lớn hơn phải mua |
| 2 | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | 56,165 | 2026-10-03 | Apache-2.0 | TypeScript | HTML/CSS/GSAP → MP4 tất định, có CLI + skills cho AI agent (HeyGen) | ✅ CPU (headless Chrome + ffmpeg) | ★★★★★ Đã là engine ưu tiên trong playbook; dùng cho layout 9:16, caption động, PIP mặt (thẻ <video> bo tròn), title card |
| 3 | [motion-canvas/motion-canvas](https://github.com/motion-canvas/motion-canvas) | 19,227 | 2026-07-03 | MIT | TypeScript | Thư viện animation bằng TypeScript + editor realtime | ✅ CPU | ★★ Hợp motion graphics; render headless kém (dùng Revideo nếu cần) |
| 4 | [Zulko/moviepy](https://github.com/Zulko/moviepy) | 14,945 | 2026-08-26 | MIT | Python | Thư viện dựng video Python (cắt, ghép, overlay, text, audio) v2 | ✅ CPU (render 60s 1080×1920 mất vài phút) | ★★★★ Keo Python dễ nhất cho PIP/B-roll/ghép âm; dự phòng khi không dùng HyperFrames |
| 5 | [kkroening/ffmpeg-python](https://github.com/kkroening/ffmpeg-python) | 11,011 | 2022-07-12 | Apache-2.0 | Python | Wrapper Python cho ffmpeg, dựng filter_complex dạng graph | ✅ CPU | ★★★ Không còn commit từ 2022 nhưng ổn định; tiện cho PIP overlay + loudnorm |
| 6 | [mifi/editly](https://github.com/mifi/editly) | 5,515 | 2025-02-20 | MIT | TypeScript | Dựng video khai báo bằng JSON5 (clip, text, transition) → ffmpeg; CLI + API Node | ✅ CPU | ★★★ Đơn giản cho slideshow/B-roll; commit cuối 02/2025 |
| 7 | [WyattBlue/auto-editor](https://github.com/WyattBlue/auto-editor) | 5,410 | 2026-10-03 | Unlicense | Nim | Tự cắt khoảng lặng/đoạn thừa theo âm lượng/chuyển động; xuất MP4 hoặc timeline Premiere/Resolve | ✅ CPU, rất nhanh | ★★★★ Cắt lặng clip presenter / voice trước khi dựng; Unlicense |
| 8 | [nexu-io/html-video](https://github.com/nexu-io/html-video) | 4,633 | 2026-06-21 | Apache-2.0 | HTML | HTML/CSS/data → MP4 cho coding agent, engine render thay được, 21 template | ✅ CPU | ★★ Cùng ý tưởng HyperFrames nhưng nhỏ hơn |
| 9 | [redotvideo/revideo](https://github.com/redotvideo/revideo) | 4,078 | 2026-07-16 | MIT | TypeScript | Fork Motion Canvas để render headless/API (TS → MP4) | ✅ CPU | ★★ Thay thế Remotion có license MIT; cộng đồng nhỏ hơn |
| 10 | [PyAV-Org/PyAV](https://github.com/PyAV-Org/PyAV) | 3,298 | 2026-10-03 | BSD-3-Clause | Python | Binding Python cấp thấp cho thư viện FFmpeg | ✅ CPU | ★★ Dùng khi cần xử lý frame trực tiếp |
| 11 | [diffusionstudio/core](https://github.com/diffusionstudio/core) | 1,246 | 2025-11-19 | MPL-2.0 | TypeScript | Engine compositing video chạy trong trình duyệt (WebCodecs) | ✅ CPU/browser | ★ Hợp app web, không hợp pipeline server |

### Nhóm 3 — Phụ đề/ASR (10 repo)

| # | Repo | ⭐ Stars | Commit cuối (ICT) | License | Ngôn ngữ | Làm gì | CPU/GPU | Hợp pipeline (★1–5) |
|---|---|---:|---|---|---|---|---|---|
| 1 | [openai/whisper](https://github.com/openai/whisper) | 109,904 | 2026-09-01 | MIT | Python | ASR gốc của OpenAI (99 ngôn ngữ, có tiếng Việt) | ⚠️ CPU chậm (model large) | ★★ Dùng bản tối ưu (faster-whisper/whisper.cpp) thay vì bản gốc |
| 2 | [ggml-org/whisper.cpp](https://github.com/ggml-org/whisper.cpp) | 54,104 | 2026-10-02 | MIT | C++ | Whisper bản C/C++, lượng tử hoá, rất nhanh trên CPU, xuất SRT/VTT/JSON có timestamp | ✅ CPU tốt | ★★★★ Lựa chọn nhẹ nhất cho ASR/timestamp trên box; ít phụ thuộc Python |
| 3 | [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) | 25,681 | 2026-10-01 | MIT | Python | Whisper chạy trên CTranslate2, int8 CPU nhanh ~4x, có word_timestamps | ✅ CPU (small/medium int8) | ★★★★ Lõi ASR cho clip nguồn/QA; nền của WhisperX |
| 4 | [m-bain/whisperX](https://github.com/m-bain/whisperX) | 24,348 | 2026-09-27 | BSD-2-Clause | Python | faster-whisper + forced alignment wav2vec2 → timestamp từng từ chính xác (+diarization) | ✅ CPU (int8, chậm hơn GPU) | ★★★★★ Có align model tiếng Việt; dùng hàm align() với KỊCH BẢN ĐÃ BIẾT + wav OmniVoice → word-level SRT chuẩn, không lo ASR sai chính tả |
| 5 | [WEIFENG2333/VideoCaptioner](https://github.com/WEIFENG2333/VideoCaptioner) | 16,148 | 2026-05-24 | GPL-3.0 | Python | Trợ lý phụ đề LLM: ASR → ngắt câu thông minh → sửa lỗi → dịch → xuất/burn | ✅ CPU (ASR whisper.cpp/faster-whisper hoặc API) | ★★★ Ý tưởng ngắt câu bằng LLM hay; chủ yếu GUI, GPL-3.0 |
| 6 | [k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) | 15,091 | 2026-09-22 | Apache-2.0 | C++ | ASR/TTS/VAD/diarization trên onnxruntime, không cần mạng, chạy được cả mobile | ✅ CPU tốt | ★★ Phương án ASR/VAD nhẹ dự phòng |
| 7 | [tmoroney/auto-subs](https://github.com/tmoroney/auto-subs) | 4,309 | 2026-10-02 | MIT | TypeScript | Tạo phụ đề on-device, cắm thẳng vào DaVinci Resolve/Premiere/After Effects | ✅ CPU | ★ Cho dựng tay trên NLE, không cho pipeline headless |
| 8 | [m1guelpf/auto-subtitle](https://github.com/m1guelpf/auto-subtitle) | 2,289 | 2023-11-16 | MIT | Python | Whisper + ffmpeg: tạo và burn phụ đề vào video bằng 1 lệnh | ⚠️ CPU chậm (whisper gốc) | ★★ Ngừng từ 2023; tự viết bằng faster-whisper còn tốt hơn |
| 9 | [jianfch/stable-ts](https://github.com/jianfch/stable-ts) (archived) | 2,281 | 2026-05-31 | MIT | Python | Whisper + forced alignment, chỉnh timestamp ổn định | ✅ CPU | ★★ ĐÃ ARCHIVED → tránh, dùng WhisperX |
| 10 | [VinAIResearch/PhoWhisper](https://github.com/VinAIResearch/PhoWhisper) | 257 | 2024-11-12 | BSD-3-Clause | — | Whisper fine-tune cho tiếng Việt (VinAI), weights trên HuggingFace | ✅ CPU (tiny/base/small; convert CTranslate2) | ★★★ ASR tiếng Việt tốt nhất để nhận dạng clip nguồn; repo chỉ chứa info, weights ở HF |

### Nhóm 4 — AI cắt clip/highlight (4 repo)

| # | Repo | ⭐ Stars | Commit cuối (ICT) | License | Ngôn ngữ | Làm gì | CPU/GPU | Hợp pipeline (★1–5) |
|---|---|---:|---|---|---|---|---|---|
| 1 | [modelscope/FunClip](https://github.com/modelscope/FunClip) | 6,361 | 2026-09-16 | MIT | Python | FunASR nhận dạng → chọn đoạn bằng text/LLM → cắt clip + phụ đề, Gradio UI | ✅ CPU | ★★ ASR FunASR mạnh tiếng Trung, tiếng Việt yếu |
| 2 | [Anil-matcha/AI-Youtube-Shorts-Generator](https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator) | 5,222 | 2026-09-29 | MIT | Python | Video YouTube dài → LLM chọn highlight → Whisper → crop mặt 9:16 → shorts | ✅ CPU (LLM qua API) | ★★★ Dùng khi muốn cắt đoạn keynote/podcast làm B-roll/nguồn tin |
| 3 | [ClipsAI/clipsai](https://github.com/ClipsAI/clipsai) | 544 | 2024-01-17 | MIT | Python | Thư viện Python tự cắt clip từ video dài theo transcript + resize 16:9→9:16 theo người nói | ⚠️ CPU được (WhisperX + pyannote) | ★★ Ngừng từ 01/2024; ý tưởng auto-reframe 9:16 hữu ích |
| 4 | [RafaelGodoyEbert/ViralCutter](https://github.com/RafaelGodoyEbert/ViralCutter) | 418 | 2026-09-10 | GPL-3.0 | Python | YouTube → clip viral 9:16 có transcript + phụ đề | ⚠️ CPU chậm, GPU khuyến nghị | ★★ GPL-3.0; giống AI-Youtube-Shorts-Generator |

### Nhóm 6 — Model sinh video mở (10 repo)

| # | Repo | ⭐ Stars | Commit cuối (ICT) | License | Ngôn ngữ | Làm gì | CPU/GPU | Hợp pipeline (★1–5) |
|---|---|---:|---|---|---|---|---|---|
| 1 | [hpcaitech/Open-Sora](https://github.com/hpcaitech/Open-Sora) | 29,853 | 2026-04-09 | Apache-2.0 | Python | Model text/image-to-video Open-Sora 2.0 (11B) | ❌ GPU lớn (H100/H800, đa GPU) | ★ Không chạy được trên box |
| 2 | [Wan-Video/Wan2.2](https://github.com/Wan-Video/Wan2.2) | 17,706 | 2026-09-21 | Apache-2.0 | Python | Model video Wan 2.2 (T2V/I2V/TI2V-5B, A14B MoE) | ❌ GPU (TI2V-5B ~24GB; A14B ~80GB) | ★ Chỉ qua API/cloud nếu cần B-roll AI |
| 3 | [Wan-Video/Wan2.1](https://github.com/Wan-Video/Wan2.1) | 17,087 | 2026-03-05 | Apache-2.0 | Python | Model video Wan 2.1 (T2V-1.3B / 14B, I2V, VACE) | ❌ GPU (1.3B cần ~8.2GB VRAM) | ★ Không chạy trên box CPU |
| 4 | [zai-org/CogVideo](https://github.com/zai-org/CogVideo) | 13,056 | 2025-11-04 | Apache-2.0 | Python | CogVideoX 2B/5B text/image-to-video | ❌ GPU (≥4–10GB VRAM với diffusers, rất chậm) | ★ Không thực tế trên CPU |
| 5 | [Tencent-Hunyuan/HunyuanVideo](https://github.com/Tencent-Hunyuan/HunyuanVideo) | 12,583 | 2026-06-29 | Tencent Hunyuan Community | Python | HunyuanVideo 13B text-to-video | ❌ GPU 45–80GB | ★ Không chạy trên box; license Tencent (không áp dụng EU/UK/KR) |
| 6 | [Lightricks/LTX-Video](https://github.com/Lightricks/LTX-Video) | 11,012 | 2026-01-06 | Apache-2.0 (code) + OpenRail-M (weights) | Python | LTX-Video 2B/13B, nhanh, có bản distilled/fp8 | ❌ GPU (bản nhỏ vài GB VRAM; CPU offload chỉ một phần) | ★ Model video mở 'nhẹ' nhất nhưng vẫn cần GPU |
| 7 | [Lightricks/LTX-2](https://github.com/Lightricks/LTX-2) | 9,576 | 2026-10-02 | LTX Community License | Python | LTX-2/2.5: model sinh audio+video đồng bộ | ❌ GPU lớn (có fp8 + offload) | ★ Không chạy trên box |
| 8 | [Tencent-Hunyuan/HunyuanVideo-1.5](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5) | 4,570 | 2026-04-10 | Tencent Hunyuan Community | Python | HunyuanVideo 1.5 (8.3B), nhẹ hơn bản gốc | ❌ GPU ≥14GB (offload) | ★ Không chạy trên box |
| 9 | [hao-ai-lab/FastVideo](https://github.com/hao-ai-lab/FastVideo) | 4,542 | 2026-10-03 | Apache-2.0 | Python | Framework tăng tốc inference/post-train model video (Wan, Hunyuan…) | ❌ GPU | ★ Chỉ hữu ích khi có GPU |
| 10 | [genmoai/mochi](https://github.com/genmoai/mochi) | 3,735 | 2025-11-14 | Apache-2.0 | Python | Mochi 1 (10B) text-to-video | ❌ GPU ~60GB (1 GPU) | ★ Không chạy trên box |

### Nhóm 7 — B-roll/footage tự động (3 repo)

| # | Repo | ⭐ Stars | Commit cuối (ICT) | License | Ngôn ngữ | Làm gì | CPU/GPU | Hợp pipeline (★1–5) |
|---|---|---:|---|---|---|---|---|---|
| 1 | [yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp) | 195,181 | 2026-09-28 | Unlicense | Python | Tải video/audio từ YouTube, TikTok, X… (cắt theo đoạn --download-sections, chọn chất lượng) | ✅ CPU | ★★★★ Lấy clip nguồn tin (demo, keynote) làm B-roll; cẩn thận bản quyền, chỉ dùng đoạn ngắn + ghi nguồn |
| 2 | [mlfoundations/open_clip](https://github.com/mlfoundations/open_clip) | 14,183 | 2026-09-30 | MIT-style (custom) | Python | CLIP mã nguồn mở: embedding ảnh/text để tìm ảnh/khung hình theo mô tả | ✅ CPU (ViT-B/32 nhẹ) | ★★★ Xếp hạng footage Pexels/khung hình theo câu kịch bản (semantic B-roll matching) |
| 3 | [Breakthrough/PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | 5,217 | 2026-09-21 | BSD-3-Clause | Python | Phát hiện điểm cắt cảnh (content/adaptive/threshold) → tách clip, xuất timecode | ✅ CPU, nhanh | ★★★★ Chặt video nguồn thành shot 1–3s để chèn B-roll; chọn shot đẹp tự động |
