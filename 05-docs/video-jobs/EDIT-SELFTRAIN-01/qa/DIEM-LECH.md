# DIEM-LECH — EDIT-SELFTRAIN-01 (mẫu Kallaway 7645299083573267742)
Tham chiếu: `/workspace/video-learn/tiktokintl-kanekallaway/7645299083573267742_breakdown.md` (72,7s). Đo bằng `tools/qa_metrics.sh` + `analyze.py`.
Vòng: r1 = script riêng (kw_render.py) · r2 = pipeline lần đầu (lỗi align) · r3 = pipeline + fix align/TP · **final (r3 config) = caption 50px, nhạc −18 dB**.

| Chỉ số | Tham chiếu | r1 (trước) | Final (sau) | Lệch còn lại | Cách sửa đã làm / còn lại |
|---|---|---|---|---|---|
| Cắt/phút (0,3 / 0,2) | 23,9 / 29,7 | 27,8 / 30,9 | 27,2 / 27,2 | +3,3 / −2,5 | ok; 2 cắt fx→fx (nền tối) không bị bắt ở 0,2 |
| Shot trung vị (0,3) | 1,56s | 1,58s | 1,70s | +0,14s | ok |
| Cắt đầu tiên | 1,17s (0,2) | 1,37s | 1,13s | −0,04s | r2 bị 0,50s do WhisperX gãy timing → thêm fallback faster-whisper |
| Đường chia / hộp mặt | 966 / 270px | 960 / 291px | 958 / 278px | −8 / +8px | face_split_px=270, s_eye_y=320 |
| Caption y / cao / màu / chữ-cụm | 1010 / 58px / #DFAD12 / 2 | 992 / 74px / — / 2 | 1008 / 62px / #CFA121 / 2 | −2 / +4px / tối hơn ~16 | font 62→50px; màu có thể sáng lên #E8B820 |
| Punch-in + chữ to | ×1,18; chữ to mỗi 6–10s | 3 lần ×1,15–1,2 | 3 lần ×1,15–1,2 (≈6–7s/lần) | analyze không nhận là punch (đổi layout S→F) | — |
| Sfx / % cắt có sfx | 14,9/phút, 27,6% | 18/phút, ~30% | 18 đỉnh/19,8s, ~30% | ok | — |
| Nhạc nền liên tục | 94,5% | — | 90,0% | −4,5% | nhạc −20 → −18 dB dưới giọng |
| Khoảng ngừng ≥0,25s | 0 | 0 | 0 | 0 | tighten pause >0,2s |
| LUFS / True peak | −14,4 / — | −14,0 / −1,5 | −14,0 / −1,9 dBTP | ok | r2 TP −0,8 → mix TP −2,0 |
| Tiêu đề hook | 2 dòng IN HOA, lộ chữ ~2s | wipe 1,2s | wipe 1,2s, giữ 2,4s | nhanh hơn ~0,8s | — |

## 5 dòng lệch còn lại (sau fix)
1. Caption cao 62px (tham chiếu 58px) và màu đo #CFA121 hơi tối so với #DFAD12 → hạ font 48px, tăng sáng fill.
2. Nhạc nền liên tục 90% (tham chiếu 94,5%) → nhạc tự tổng hợp có nhịp nghỉ; cần bản nhạc pad liền hơn hoặc −17 dB.
3. Cắt/phút ngưỡng 0,2: 27,2 (tham chiếu 29,7) vì 2 cắt fx nền tối→fx nền tối không đủ khác biệt → cho fx nền sáng xen kẽ.
4. Mặt người dẫn (nền cây, vest) không có PIP tròn trái-trên và mockup điện thoại 3D như Kallaway (chưa làm trong preset).
5. B-roll chủ yếu ảnh chụp bài báo + đồ hoạ tự vẽ (không có clip quay/demo động như Kallaway) → nhịp hình "tĩnh" hơn dù cắt đúng nhịp.
