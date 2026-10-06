# HM-103 v1 — Nguồn asset

## Video YouTube (b-roll gameplay)
- Nguồn: https://www.youtube.com/watch?v=8NmmFdREk5s, tải bằng yt-dlp (format 18, 640×360, 2400s) → `source/yt/wow_blind.mp4` (log: qa/ytdlp.log)
- Bản quyền: video của bên thứ ba, **chưa xác nhận license**. Chỉ dùng đoạn ngắn 3.4s để minh họa tin tức; pill nguồn "YouTube 8NmmFdREk5s" có trên mọi cảnh dùng clip. Gameplay WoW © Blizzard (chạy trên server AzerothCore).
- Đã cắt 13 clip, không chồng lấn nhau (script bake_yt.py có assert kiểm tra), crop vùng cửa sổ game 316×254+12+58 (riêng y11 lấy cả desktop):

| Clip | Thời điểm gốc | Bố cục | Nội dung |
|---|---|---|---|
| y01_orc_new | 219.6–223.0s (3:39.6) | full | Orc level 1 mới xuất hiện ở điểm khởi đầu |
| y02_questgiver | 388.4–391.8s (6:28.4) | full | NPC giao nhiệm vụ (dấu ?) — Valley of Trials |
| y03_path_cacti | 487.0–490.4s (8:07.0) | tb | Chạy đường giữa các điểm nhiệm vụ (pathfinding) |
| y04_vendor | 1213.6–1217.0s (20:13.6) | full | Khu NPC/thùng hàng ở trại — đoạn bán đồ (không thấy cửa sổ vendor) |
| y05_gear | 1739.6–1743.0s (28:59.6) | full | Cận cảnh orc đã khoác giáp mới (áo giáp đỏ) |
| y06_trainer | 1880.0–1883.4s (31:20.0) | full | Đứng ở trainer (thảm, trại Den) trước khi vào hang |
| y07_cave | 2017.0–2020.4s (33:37.0) | lr | Trong hang — đánh quái nhiệm vụ hang |
| y08_senjin | 2343.0–2346.4s (39:03.0) | lr | Sen'jin Village (nhà troll, cây cọ) — cuối run |
| y09_valley_den | 640.0–643.4s (10:40.0) | lr | Trại Den ở Valley of Trials |
| y10_wallclip | 1963.2–1966.6s (32:43.2) | tb | Camera/nhân vật xuyên địa hình ở vách đá (lỗi va chạm bản đồ) |
| y11_codex_prompt | 29.0–32.4s (0:29.0) | tbfit | Desktop: WoW + Codex vừa nhận câu lệnh 'Create an orc character…' |
| y12_orc_close | 1069.0–1072.4s (17:49.0) | lr | Cận cảnh orc (dùng cho cảnh 'không nhận khung hình') |
| y13_landscape | 1409.0–1412.4s (23:29.0) | tb | Toàn cảnh Durotar — 'bản đồ thế giới' |

Lưu ý: y04 (bán đồ) không thấy cửa sổ vendor, chỉ là cảnh khu NPC/thùng hàng ở trại, dùng làm cảnh minh họa. y10 (lách tường) là camera xuyên vào vách đá; khớp với claim "khai thác lỗi bản đồ" nhưng **chưa xác nhận** đây đúng là lần xuyên tường trong bài viết.

## Screenshot web (puppeteer-core + /usr/bin/google-chrome headless; scripts: lam-viec/webshots/grab.js, jobs*.json, rects*.json)
- ws_agentwow.png: https://agent-wow.sh/gpt-6-astra-plays-world-of-warcraft-for-the-first-time-with-agent-wow/ (cảnh 6, 11, 16, 17, 27, 29)
- ws_agentwow_home.png: https://agent-wow.sh/ (cảnh 24, 26)
- ws_toms.png: https://www.tomshardware.com/tech-industry/artificial-intelligence/gpt-6-astra-plays-world-of-warcraft-blind-and-clears-the-orc-starting-zone-in-40-minutes-with-no-deaths-ai-agent-navigates-by-server-network-traffic-with-pulled-quest-data (trang live bị timeout nên render từ HTML đã tải về, bỏ script: lam-viec/preview/toms_noscript.html) (cảnh 9, 14)
- ws_ie.png: https://interestingengineering.com/ai-robotics/openais-gpt-6-astra-plays-world-of-warcraft (chặn script) (cảnh 18)
- toms_hero_wow.png: og:image của Tom's https://cdn.mos.cms.futurecdn.net/ujZwJwwyt3MAzvTPaTAe34-1920-80.png (screenshot WoW, credit Blizzard), làm nền cảnh hook 1 (đã blur)
- cdn_ie_hero.png: https://cms.interestingengineering.com/wp-content/uploads/2026/10/image-1920x1080-2026-10-04T135603.874.png (artwork WoW), cảnh 29
- Mỗi cảnh dùng một vùng crop khác nhau (lam-viec/hf/assets/sh*.jpg), không có ảnh full-frame nào lặp lại.

### KHÔNG dùng (ảnh sai trong script.md)
- https://cdn.mos.cms.futurecdn.net/3PafanCD9Ws7RDdJ8SGBji.jpg → ảnh router ASUS, không liên quan (đã tải về: source/assets/cdn_toms_hero.jpg)
- https://cdn.mos.cms.futurecdn.net/6mmVqfQjXAQVMLwxBZ5SQV.jpg → ảnh đầu cắm nguồn bị cháy, không liên quan (source/assets/cdn_toms_related.jpg)

## Presenter
- presenter_full.mp4 lấy từ /workspace/hinton-pipeline-docs/assets/presenter-video-novoice.mp4 (asset nội bộ Hinton, dùng lại như HM-101 v2/v3). 4 beat (cảnh 10, 15, 25, 30).

## Đồ họa tự thiết kế (HTML/CSS/GSAP trong HyperFrames, màu Hinton vàng/đỏ trên nền đen/xanh đậm; không dùng logo/lưới đỏ của kênh mẫu)
Thẻ claim hook, counter 40 PHÚT / 0 LẦN CHẾT / 28 / 16K DÒNG CODE, icon mắt gạch chéo, sơ đồ GÓI TIN MẠNG→FILE SQL→LỆNH HÀNH ĐỘNG, terminal module.yaml (gắn nhãn "Minh họa"), khối code DetourNavMesh.h, thẻ nhiệm vụ #1/#2, đồ họa AzerothCore ≠ BLIZZARD, stamp caveat (KHÔNG PHẢI OPENAI CÔNG BỐ / THÍ NGHIỆM ĐỘC LẬP / CHƯA KIỂM CHỨNG / LỖI QUÁ → BỎ), thẻ câu hỏi outro.

## Font và thư viện
- Montserrat (wght 900), SIL Open Font License, lấy từ HM-101 hf_v3/assets/Montserrat.ttf
- GSAP (gsap.min.js) lấy từ HM-101 hf_v3

## Âm thanh, toàn bộ tự tạo, không lấy từ nguồn ngoài
- `lam-viec/synth_sfx.py` (numpy, seed 103) → source/sfx/: bgm_synth_124bpm.wav (Dm–Bb–F–C, 60s), whoosh_a/b/c, ding, pop, marker, impact. Có thể dùng không cần license.
- Mix (lam-viec/mix.py → audio/loudness.json): VO −14.0 LUFS · BGM −24.1 LUFS · SFX bus −21.0 LUFS · mix −13.2 LUFS, true peak −0.8 dBTP. Cắt hết ở VO_END.
- Giọng đọc: OmniVoice (k2-fsa/OmniVoice), clone nam v2 (voice-lock-vn-v2.wav), speed 1.2, voice_locked:true.


## v1.1 note (2026-10-05)
- Shot 27: **không còn dùng** `y10_wallclip.mp4` trong composition. Thay bằng kinetic graphic `sh26p0_wallwarn.jpg` / HTML `wallwarn`.
- Clip `source/yt_clips/y10_wallclip.mp4` vẫn giữ trên disk (không xóa) nhưng không vào final v1.1.
- Shot 19 (y04_vendor): giữ nguyên sau khi quét lại — không có vendor UI rõ hơn.
