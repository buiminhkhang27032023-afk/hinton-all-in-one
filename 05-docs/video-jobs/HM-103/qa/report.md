# HM-103 v1 — QA report (Bot 2 · Tin AI)

**Chủ đề:** GPT-6 Astra chơi WoW "mù" (agent-wow). **Style:** STYLE-SPEC ref-20261005, làm y như HM-101 v3.

## Output (ffprobe)
- output/storytelling_final.mp4: 1080×1920, 30fps, H.264 CRF18 + AAC 192k, **53.89s**, 44,369,698 B (42.3 MiB)
- output/storytelling_mobile_720p.mp4: 720×1280, CRF22, 53.91s, 11,502,061 B (11.0 MiB)
- output/voice_storytelling.wav (53.53s), output/subtitle.srt (30 cue, mỗi câu 1 cue), output/storytelling_script.txt (= script.txt bố đã duyệt, đã sửa câu 23 và 28)

## Chuỗi giọng đọc
OmniVoice · male clone v2 locked · 1.2 · voice_locked:true. Ref voice: /workspace/omnivoice-server/voice-lock-vn-v2.wav, speed_mode post, seed 1234, num_step 32, vi, 24kHz. Đã kiểm /health trước TTS và lưu lại lúc render (qa/omnivoice_health_at_render.json). TTS và render đều chạy trong `flock /workspace/video-jobs/.render.lock`. Không dùng edge-tts hay dịch vụ cloud.
- 30 câu, 231 âm tiết, loudnorm −14 LUFS. ASR so lại với script: similarity **0.842**
- Căn timing từng từ: WhisperX hỏng nên pipeline tự chuyển sang faster-whisper. Câu 1, 6, 16, 17, 18 bị lệch nên đã căn lại riêng từng câu (lam-viec/fix_words.py, file gốc giữ ở words_orig.json). Giờ toàn bộ từ đã khớp.

## Âm thanh
- VO −14.0 LUFS · BGM synth −24.1 LUFS (thấp hơn VO 10 LU) · SFX bus −21.0 LUFS · mix −13.2 LUFS, TP −0.8 dBTP. File final đo lại bằng ebur128: I = −13.2 LUFS, LRA 1.8. **Giọng nổi rõ hơn BGM.**
- SFX tự synth (126 lần phát): whoosh 27 · pop 48 · ding 23 · marker 17 · impact 11. BGM và SFX đều tự tạo (synth_sfx.py, seed 103).

## Checklist style
- [x] 30 cảnh, mỗi câu VO một cảnh mới; không ảnh full-frame nào lặp lại; mỗi clip YT chỉ dùng 1 lần, không chồng lấn
- [x] Mọi shot đều push-in liên tục (GSAP scale)
- [x] Chuyển cảnh: 13 slide + 13 whip, 3 hard cut vào presenter, 1 cảnh mở → **26/29 ≈ 90% slide/whip**, mỗi lần có whoosh
- [x] Khung đỏ tự vẽ, highlighter vàng quét câu, gạch chân đỏ, mỗi cái kèm ding/pop/marker
- [x] Split 50/50: trên-dưới ×8, trái-phải ×3
- [x] Template số liệu Hinton (vàng/đỏ trên nền đen/xanh đậm): 40 PHÚT, 0 LẦN CHẾT, 28, 16K. Không dùng logo/lưới đỏ của kênh mẫu
- [x] Pill nguồn đen ở góc dưới trái trên mọi b-roll
- [x] Karaoke burn-in Montserrat 900, chữ trắng, từ đang đọc chuyển vàng, 84 cụm 1–4 từ, ở giữa phía dưới, sync theo word timing
- [x] Presenter full-frame 4 lần (cảnh 10, 15, 25, 30) ≈ 8.3s ≈ 15%. **Không mở đầu bằng mặt** (hook là graphic claim → bằng chứng → presenter)
- [x] Outro: presenter + câu hỏi mở trên màn hình → cắt đen (53.60–53.89s)

## QA kỹ thuật
- **Đếm cut:** theo plan có 29 lần chuyển cảnh + 1 cắt đen = 30 shot. Kiểm từng ranh giới cảnh: độ lệch khung hình trước/sau từ 23.6 đến 92.3 (mean abs, thang 0–255), không ranh giới nào yếu, tức cả 29 lần chuyển đều đổi hình thật. Lọc scene của ffmpeg (ngưỡng 0.18) chỉ bắt được 14 hard cut vì slide/whip là chuyển cảnh có chuyển động (HM-101 v3 cũng vậy).
- **Màn đen:** blackdetect (d=0.06, pix_th=0.08) chỉ thấy đúng 53.60–53.83s, là đoạn cắt đen cuối. Giữa video không có màn đen.
- **Đứng hình:** freezedetect (1s) không thấy chỗ nào.
- **Chữ:** đã soát qua contact sheet 16 khung và nhiều vòng snapshot (lam-viec/snaps*/). Không lỗi font tiếng Việt, không chữ tràn/cắt mép, karaoke không đè lên nội dung.
- **Lint:** `hyperframes lint` 0 error. Khoảng 120 warning về cấu trúc lồng nhau, giống HM-101 v3.
- **Contact sheet:** qa/contact_sheet.jpg, 4×4 = 16 khung từ 16 cảnh khác nhau.

## Danh sách cảnh
| # | t (s) | dur | loại | nội dung |
|---|---|---|---|---|
| 1 | 0.00 | 1.66 | claim | Claim hook: AI CHƠI WOW / KHÔNG NHÌN MÀN HÌNH (nền og:image Tom's, blur) |
| 2 | 1.66 | 0.76 | stat | Counter 40 PHÚT |
| 3 | 2.42 | 1.10 | stat | Counter 0 LẦN CHẾT (đỏ) |
| 4 | 3.52 | 1.26 | lr | LR: y12 orc + '0 KHUNG HÌNH' | mắt gạch chéo |
| 5 | 4.78 | 1.65 | flow | Sơ đồ GÓI TIN MẠNG→FILE SQL(khung đỏ)→LỆNH HÀNH ĐỘNG |
| 6 | 6.43 | 2.02 | tb | TB: agent-wow highlight prompt + khung 'GPT-6 Astra (xhigh)' | y11 desktop Codex |
| 7 | 8.45 | 0.76 | yt | y01 orc mới · TẠO ORC |
| 8 | 9.21 | 1.48 | yt | y02 NPC nhiệm vụ |
| 9 | 10.69 | 2.29 | ss | Tom's headline, khung 'ChatGPT-6 Astra' + badge xhigh |
| 10 | 12.97 | 1.61 | pres | PRESENTER + stamp KHÔNG PHẢI OPENAI CÔNG BỐ |
| 11 | 14.59 | 2.25 | ss | agent-wow highlight 'doesn't define any gameplay mechanics…' |
| 12 | 16.84 | 1.77 | term | Terminal module.yaml (nhãn Minh họa) |
| 13 | 18.61 | 1.74 | stat | Counter 28 loại message |
| 14 | 20.35 | 1.87 | tb | TB: Tom's highlight Python script | y13 bản đồ thế giới |
| 15 | 22.22 | 1.95 | pres | PRESENTER + TỰ VIẾT TÌM ĐƯỜNG · C++ |
| 16 | 24.17 | 2.21 | tb | TB: agent-wow mmaps/Detour | code DetourNavMesh.h |
| 17 | 26.38 | 1.65 | tb | TB: y03 chạy đường | 'pathfinding abilities were optimal' + TỐI ƯU |
| 18 | 28.03 | 1.99 | ss | IE highlight 'created a plan … prerequisite quests in sequence' |
| 19 | 30.03 | 0.84 | yt | y04 BÁN ĐỒ RÁC |
| 20 | 30.86 | 1.00 | yt | y05 MẶC ĐỒ XỊN HƠN |
| 21 | 31.87 | 1.68 | yt | y06 HỌC KỸ NĂNG TRƯỚC |
| 22 | 33.55 | 1.76 | lr | LR: y07 hang | thẻ nhiệm vụ #1 #2 LÀM 1 LẦN |
| 23 | 35.31 | 2.21 | lr | LR: y09 VALLEY OF TRIALS | y08 SEN'JIN VILLAGE |
| 24 | 37.52 | 2.29 | ss | agent-wow home 'open-source project' + THÍ NGHIỆM ĐỘC LẬP |
| 25 | 39.80 | 1.24 | pres | PRESENTER + stamp CHƯA KIỂM CHỨNG |
| 26 | 41.04 | 2.50 | tb | TB: AzerothCore ≠ BLIZZARD | agent-wow home 'private servers running AzerothCore' |
| 27 | 43.54 | 1.97 | tb | TB: y10 LÁCH TƯỜNG | agent-wow 'exploit map bugs by phasing through walls' |
| 28 | 45.51 | 3.32 | stat | Counter 16K DÒNG CODE + gạch + stamp LỖI QUÁ → BỎ |
| 29 | 48.83 | 2.43 | tb | TB: IE hero RAID HEROIC | agent-wow 'Icecrown Citadel on heroic' |
| 30 | 51.27 | 2.32 | outro | OUTRO presenter + câu hỏi 'AI chơi game mà không cần nhìn — bạn nghĩ sao?' → cắt đen |

## Lưu ý / caveat
1. **Cảnh 19 (bán đồ rác):** trong video gốc không thấy cửa sổ vendor, nên dùng cảnh khu NPC/thùng hàng ở trại (phút 20:13) làm minh họa. **Cảnh 27 (lách tường):** dùng đoạn camera xuyên vách đá (phút 32:43), khớp với claim nhưng chưa xác nhận là đúng lần xuyên tường trong bài.
2. Hai ảnh CDN mà script.md ghi là hero Tom's (3PafanCD9Ws7RDdJ8SGBji.jpg là router ASUS, 6mmVqfQjXAQVMLwxBZ5SQV.jpg là đầu cắm nguồn cháy) không liên quan nên **không dùng**. Thay bằng og:image thật của bài Tom's (ujZwJwwyt3MAzvTPaTAe34).
3. Cảnh 12 terminal module.yaml là đồ họa minh họa, có gắn nhãn "Minh họa".
4. Bản thân headline của Tom's ghi "ChatGPT-6 Astra". Trong video đóng khung đúng chữ đó làm bằng chứng; VO giữ nguyên.
5. Trang Tom's live bị timeout nên screenshot được render từ HTML đã tải về (bỏ script). Nội dung chữ vẫn là bài gốc.
6. Clip YT 8NmmFdREk5s là của bên thứ ba, chưa xác nhận license; chỉ dùng đoạn ngắn kèm pill nguồn.
7. Không sửa claim nào trong VO. Các stamp caveat (KHÔNG PHẢI OPENAI CÔNG BỐ / THÍ NGHIỆM ĐỘC LẬP / CHƯA KIỂM CHỨNG) bám theo đúng câu VO tương ứng.

Pipeline: lam-viec/tts_align.py → fix_words.py → synth_sfx.py → mix.py → bake_yt.py → webshots/grab.js → build_hf.py → render.sh (flock) → mux → 720p.
