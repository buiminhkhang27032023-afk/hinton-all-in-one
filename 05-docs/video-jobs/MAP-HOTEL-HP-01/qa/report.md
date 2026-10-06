# QA — MAP-HOTEL-HP-01 · Top 5 khách sạn 5 sao Hải Phòng (map animation 9:16)
- Genre G04 (map/ranking) · Format F01 (short dọc 9:16)
- Master: output/storytelling_final.mp4 — H.264 1080x1920 30fps + AAC 48k stereo — 56.43 s — 64.4 MB
- Mobile: output/storytelling_mobile_720p.mp4 — H.264 720x1280 30fps — 56.43 s — 17.8 MB
- Loudness: -14.0 LUFS integrated, true peak -1.6 dBTP, LRA 1.3 LU
- Voice: OmniVoice · male clone v2 locked · 1.2 · voice_locked:true (health OK each run; 20 sentences; no edge-tts/cloud)
- Mix: BGM CC0 gain set to VO-20 LU (-18 dB) + sidechain duck; 41 CC0 SFX events (lam-viec/audio/sfx_events.json)
- ASR verify (faster-whisper small): similarity 0.606 vs phonetic voice text (thấp do tên thương hiệu viết phiên âm + số); kiểm tra riêng các câu số: 4,6/2.100(nghìn mốt) · 4,7/1.600 · 4,7/2.200 · 4,8/1.500 · 4,8/2.100 đều đọc đủ. Round 1 phát hiện "hai nghìn một trăm" bị nuốt chữ "nghìn" → đổi voice thành "hai nghìn mốt", TTS lại câu đó.
- Subtitles: burned-in (60 cue, Be Vietnam Pro 56px, viền đen, highlight vàng tên/số) + output/subtitle.srt; timing từ faster-whisper word fallback (whisperx align collapse).
- Render: HyperFrames 0.8.114, all TTS/render steps in flock /workspace/video-jobs/.render.lock
## Frame QA checklist (qa/contact_sheet.jpg)
- [x] Frame 0 có tiêu đề TOP 5 + map (không khung trống)
- [x] "khoảng N review" một dòng, không dùng "~"
- [x] Chữ lớn, trong safe zone (x 40–960, tránh cột nút TikTok), sub y≈1390–1540
- [x] Footer sát đáy, không che card; attribution Esri luôn hiển thị
- [x] Mỗi card 1 icon pin; review bubble nhãn "Review Google Maps (dịch)"
- [x] Không có ảnh khách sạn (không cần nhãn Ảnh minh hoạ)
- [x] Map phủ kín khung (đã nối thêm 4 hàng tile phía nam sau test)
- Round 1 fixes: pin transform bị GSAP ghi đè (wrapper), confetti hiện sớm, panel trong suốt, bubble thứ 2 chậm, dot dùng left/top → transform, lint multiple roots.
