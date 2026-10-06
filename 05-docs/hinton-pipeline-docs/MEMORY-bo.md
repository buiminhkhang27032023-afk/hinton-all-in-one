# MEMORY — bố của các bot (id 0899cf74-14b7-449c-bb80-2ad71ba57637)

> Ghi chú về nguồn: công cụ RecallMemory **không có** trong phiên đóng gói này (executor không được cấp), và bộ nhớ agent nằm phía server, không có file trên box (store.db của bố chỉ có 3 kv + 1 transcript entry hệ thống). File này được **tổng hợp lại từ tài liệu trên box** (hinton-pipeline-docs/MEMORY-va-BAI-HOC.md, DA-HOC-20261003.md, profile.json, voice-lock.md, STYLE-SPEC.md, report các job HM-101/HM-103) và diễn biến hội thoại ngày 05/10/2026. Nếu cần bản RecallMemory nguyên gốc, bố tự chạy RecallMemory rồi bổ sung vào đây.

## Xưng hô & cách báo
- Gọi user là "anh", xưng "em". Không xưng "bố" với anh, không gọi "xếp".
- Báo anh theo milestone; giao file 720p kèm 1 dòng chủ đề + thời lượng. Không nhắn tiến độ thừa; nếu anh hỏi "xong chưa" thì báo trạng thái thật + giờ dự kiến (giờ VN).
- Bố chỉ điều phối (SendToAgent), không tự làm thay bot con. Sửa tối đa 2 vòng mỗi bước rồi báo anh.

## Roster (account hiện tại, tạo 03/10/2026)
| Bot | ID | Vai |
|---|---|---|
| bố của các bot | 0899cf74-14b7-449c-bb80-2ad71ba57637 | điều phối, chọn tin, QA script |
| Bot 5 — Săn tin và kiến thức AI | 699e6e2a-a311-42b9-8011-219deec67eb8 | săn tin / kiểm chứng |
| Bot 4 — Douyin | 2a3d7c26-345d-4890-8aec-e4ed5d573d88 | tải + transcript + dịch Douyin |
| Bot 3 — Biên kịch | 0c7f1b1c-7dc4-47f2-b364-dbbaa4ca55af | viết script |
| Bot 2 — Tin AI | e9b05bd8-db19-4160-8dbe-4ecbbef00a27 | render nhánh Tin AI |
| Bot 2B — Douyin | c8433107-7957-4bcd-9c28-985dc993cb4b | render nhánh Douyin |

## Luồng
- Tin AI: Bot5 research → bố chọn tin → Bot3 script → bố QA → Bot2 render → bố kiểm → giao anh.
- Douyin: Bot4 tải/transcript/dịch → Bot5 kiểm chứng → Bot3 script → bố QA → Bot2B render.
- Phiếu: `JOB|status|version|path|next` (vd `HM-103|Hoàn thành|v1.1|/workspace/video-jobs/HM-103/output/storytelling_final_v1.1.mp4|next=bố`).
- 1 render một lúc toàn máy: `flock /workspace/video-jobs/.render.lock <lệnh>`.

## Giọng
- OmniVoice local 127.0.0.1:8123, male clone v2 (`voice-lock-vn-v2.wav` + `.ref.txt`), speed 1.2, voice_locked:true, loudnorm ~−14 LUFS VO.
- QA string: `OmniVoice · male clone v2 locked · 1.2 · voice_locked:true`. Cấm edge-tts/NamMinh/cloud TTS/giọng nữ cũ.
- Script 250–270 âm tiết ≈ 52–59s (@~4.6 âm tiết/s). HM-103: 231–240 âm tiết → 53.9s.

## Phong cách hiện hành = "v3" (từ ref 05/10/2026, xem video-learn/ref-20261005/STYLE-SPEC.md)
- ≈30 cut / ~52s (~1.7s/shot), mỗi câu VO = 1 cảnh mới, không lặp ảnh full-frame, mỗi clip YT dùng 1 lần.
- Push-in liên tục mọi shot; ~90% chuyển cảnh slide/whip + whoosh.
- Khung đỏ tự vẽ / highlighter vàng / gạch chân đỏ trên screenshot + ding/pop.
- Split 50/50 trên-dưới & trái-phải; template số liệu Hinton (vàng/đỏ trên nền đen/xanh đậm), không dùng lưới đỏ của kênh mẫu.
- Karaoke burn-in Montserrat 900 trắng → từ đang đọc vàng (#FFD400), 1–4 chữ, giữa-dưới.
- Pill nguồn đen chữ trắng góc dưới trái mọi b-roll.
- Presenter full-frame ~4 lần ~2s (≈15%), KHÔNG mở bằng mặt; hook = claim graphic → bằng chứng → presenter.
- Outro: presenter + câu hỏi mở → cắt đen.
- BGM synth tự tạo ~−24 LUFS dưới VO −14; SFX tự synth (whoosh/pop/ding/marker/impact).
- (Ghi đè so với mặc định cũ "không BGM, không karaoke" — v3 bật cả hai.)

## Sở thích của anh
- Chê video ít hình / animation yếu. Cần ≥15 visual khác nhau (thực tế v3 ~30), motion graphics thật.
- Thích có footage thật (vd gameplay YouTube cắt bằng yt-dlp) khi chủ đề có.
- Upload bản 1080p + 720p lên Google Drive thư mục "Hinton Media - Video" (https://drive.google.com/drive/folders/1c8PS-y0ncosJAH6GlhvD_h8xslLVBBT2) khi anh yêu cầu.
- Ưu tiên chủ đề hot ở nước ngoài / YouTube view cao, mẫu kênh nước ngoài; không trùng job đã làm.

## Lịch sử job gần nhất
- HM-101 (Meta AI giải 5 bài toán mở + Muse Spark/Home Link): v1 (52s, 20 shot, PIP nhiều) → anh chê ít animation + lặp 2 ảnh → v2 (22 cảnh, 27 asset) → v3 theo ref style (34 shot, 51.9s) = bản chuẩn, đã up Drive.
- HM-103 (GPT-6 Astra chơi WoW "mù", thí nghiệm độc lập agent-wow, video YT 8NmmFdREk5s): v1 53.9s, 30 cảnh, 13 clip gameplay; v1.1 thay cảnh "lách tường" (y10_wallclip mờ, không chứng minh được) bằng graphic "WALL CLIP · LỖI BẢN ĐỒ". Cả hai đã up Drive.
- Backlog Bot5 (HM-103 research): NVIDIA DGX Spark 64GB $4999; ChatGPT Finances Free/Go Mỹ; Aleph Alpha Kolibri open-weight. Muse Spark đã làm, không đưa lại.

## Bài học
- Không chạy ~25 bot cùng lúc (load ~80, RAM cạn, crash). Thiếu RAM: không whisper large/medium.
- Render chạy thẳng Shell (nohup) trong flock, không dùng tác vụ nền.
- v1 HM-101 bị chê vì lặp 2 ảnh + animation yếu → luôn kiểm contact sheet, đếm visual khác nhau.
- Không gắn nhãn "bằng chứng" cho footage không liên quan/không chứng minh được (wall-clip → thay graphic; cảnh vendor dùng stand-in phải ghi rõ).
- Ảnh CDN trong script có thể sai nội dung (HM-103: 2 link "hero Tom's" thực ra là router ASUS và đầu cắm cháy) → mở xem trước khi dùng.
- Reviewer/model nhìn hình có thể sai → kiểm lại bằng ffmpeg (freezedetect, blackdetect, scene diff, frame grab) thay vì tin mô tả.
- Scene filter ffmpeg (thr 0.18) đếm thiếu cut khi chuyển cảnh là slide/whip → đếm theo plan + diff khung hình tại ranh giới.
- WhisperX có thể hỏng → pipeline tự fallback faster-whisper; câu lệch thì căn lại riêng (fix_words.py).
