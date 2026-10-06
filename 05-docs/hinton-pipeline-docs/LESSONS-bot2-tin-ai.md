# LESSONS — Bot 2 Tin AI (e9b05bd8-db19-4160-8dbe-4ecbbef00a27)
Nguồn: qa/report*.md HM-101 (v1/v2/v3), HM-103 (v1/v1.1), build scripts. Bộ nhớ không truy cập được bằng file.
- Engine: HyperFrames 0.8.114, project `lam-viec/hf/` sinh bởi `build_hf.py` + `hf_style.css`; GSAP; Montserrat.
- Pipeline HM-103: tts_align.py → fix_words.py → synth_sfx.py → mix.py → bake_yt.py → webshots/grab.js → build_hf.py → render.sh (flock) → mux → 720p.
- Footage YT: tải bằng yt-dlp, cắt clip ngắn (bake_yt.py), mỗi clip dùng 1 lần, có pill nguồn; ghi license chưa xác nhận.
- Screenshot: plate bake sẵn, crop vào vùng chữ, phủ 1080px, nền blur chính ảnh.
- Không TTS lại khi chỉ sửa hình (reuse voice.wav, chỉ remix SFX).
- Output mới không ghi đè bản cũ (`*_v1.1.mp4`).
- QA: ffprobe; blackdetect; freezedetect; diff khung tại ranh giới cảnh; contact sheet 16 khung; kiểm /health OmniVoice lưu `qa/omnivoice_health_at_render.json`.
- Lỗi đã gặp: JS `-100%` không quote làm render fail (v2); WhisperX hỏng → faster-whisper; CRF16 ra file 55MB (dùng CRF18 cho 1080, CRF22 cho 720).
- Không dán nhãn bằng chứng cho footage không chắc (y10_wallclip) → thay graphic kinetic.
- Stand-in phải ghi rõ trong report (shot 19 vendor = NPC camp).
