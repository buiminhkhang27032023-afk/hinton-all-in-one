# HM-101 v3 — report (style remake theo video mẫu ref 2026-10-05)

- **Job:** HM-101 · REMAKE v3 · theo `/workspace/video-learn/ref-20261005/STYLE-SPEC.md` (ref.mp4 chỉ học style; KHÔNG dùng footage/logo/lưới ô đỏ của kênh mẫu)
- **Ghi đè cho job này:** karaoke burn-in BẬT · BGM BẬT · SFX BẬT
- **Engine:** HyperFrames 0.8.114 · project `lam-viec/hf_v3/` (builder `lam-viec/build_hf_v3.py` + `lam-viec/hf_v3_style.css`); `hyperframes check` = **passed** (0 lỗi). Render bọc `flock /workspace/video-jobs/.render.lock` → `lam-viec/render_v3/video.mp4`, rồi ghép lại audio premix.
- **Voice:** DÙNG LẠI v1 `output/voice_storytelling.wav` (md5 c0293440…), **không TTS**.
- **Output:** 1080×1920@30 H.264 + AAC 192k, **51.90s** (VO kết thúc 51.56s → cắt đen 51.60–51.90s); mobile 720×1280.

## Checklist style
| # | Yêu cầu | Kết quả |
|---|---|---|
| 1 | ~30 cut / 52s | **34 shot = 33 lần chuyển shot + 1 cắt đen** (trung bình 1.52s/shot). Scene-detect ffmpeg (thr 0.18) bắt được 26 cut cứng; các cú slide giữa những shot cùng tông màu bị bỏ sót vì là chuyển động trượt, không phải cut cứng |
| 2 | Push-in liên tục mọi shot | Mọi shot đều có `.cam` scale 1.00→1.12–1.16 (ease none) suốt shot; presenter 1.04→1.17; panel split push-in riêng từng panel |
| 3 | ~90% slide/whip + whoosh | 29/33 transition = slide/whip (18 slide + 11 whip có blur) = **88%**; 4 cú còn lại là cắt cứng vào presenter (có impact). Whoosh (3 biến thể luân phiên) trên mọi slide/whip |
| 4 | Screenshot zoom phủ ngang, nền blur | Plate bake sẵn: crop vào vùng chữ, scale phủ 1080px, nền = blur của chính ảnh (giảm sáng 0.42) — `lam-viec/v3_shots/` |
| 5 | Khung đỏ + highlighter vàng + gạch chân đỏ + ding/pop | 25 dấu vẽ trên screenshot (path SVG khung đỏ, vệt highlighter quét, gạch chân đỏ) + badge/stamp; khung → ding, highlighter → pop + tiếng bút, gạch chân → pop |
| 6 | Split 50/50 trên-dưới & trái-phải | Trên-dưới ×4 (9.4s, 24.6s, 35.7s, 48.3s) · trái-phải ×3 (5.9s, 38.5s, 44.7s); panel trượt vào từ hai phía, vạch chia vàng |
| 7 | Template số Hinton | 6 BÀI BÁO · 5 KỲ OLYMPIAD · 384 PHẦN TỬ · 2015 · 5.000 MUSE HOME LINK — số vàng đổ bóng đỏ trên nền xanh đậm/đen có sọc, đếm kinetic + pop + khung đỏ tự vẽ + ding (không dùng lưới ô đỏ của kênh mẫu). Hook cũng dùng template này |
| 8 | Pill nguồn mọi b-roll | Pill đen chữ trắng góc dưới trái trên mọi shot screenshot/figure/split (Nguồn: Meta AI Research, research.meta.ai, Meta (Figure n), arXiv …, X - @alexandr_wang, GitHub muse-gadget-sdk, gadgets.muse.ai, Minh họa · meta.ai) |
| 9 | Karaoke burn-in | Montserrat wght 900, chữ trắng viền đen + bóng, **từ đang đọc chuyển vàng #FFD400**, 94 cụm 2–4 từ (không tách từ ghép), giữa-dưới y≈1255–1455 (phía trên vùng nút TikTok); sync từ words.json; số hiển thị dạng chữ số (5, 6, 2/10, 2024, 384, 2015, 5.000, meta.ai); không emoji |
| 10 | Presenter full-frame ~4×~2s | **4 nhịp**: 2.92–4.90 · 19.90–21.60 · 41.90–43.42 · 49.44–51.60 (outro) = 7.4s ≈ 14%; không PIP |
| 11 | Hook 0–3s | 0–1.32 thẻ claim "AI GIẢI 5 BÀI TOÁN MỞ" → 1.32–2.92 screenshot blog Meta (highlight tiêu đề + gạch chân "six research papers") → 2.92 presenter. Không mở bằng mặt |
| 12 | Outro | Presenter full-frame + thẻ câu hỏi "AI đã biết tạo kiến thức mới, bạn sẽ dùng nó làm gì?" (highlight vàng) → cắt đen lúc 51.60 |
| 13 | BGM | Nền synth tự tạo 120 BPM (Am–F–C–G), ducking nhẹ dưới giọng: **BGM −24.2 LUFS vs VO −14.0 LUFS** (thấp hơn ~10 LU) |
| 14 | SFX | Tự tạo: whoosh_a/b/c, ding, pop, marker, impact → `source/sfx/` (ghi trong qa/assets.md) |

## Loudness (`lam-viec/audio_v3/loudness.json`)
VO stem −14.0 LUFS · BGM stem −24.2 LUFS · bus SFX −21.0 LUFS · **file final −13.2 LUFS integrated, true peak −0.9 dBFS** (alimiter). Giọng vẫn trội hơn nhạc.

## Shot list (t bắt đầu → loại)
0.00 hook claim · 1.32 SS blog Meta · 2.92 PRESENTER · 4.90 hero Meta · 5.88 LR Fig1|Fig4 · 7.12 SS research.meta.ai + badge 02/10 · 9.44 TB paper1|arXiv · 10.70 STAT 6 · 11.90 SS arXiv + badge 5/6 · 14.14 thẻ Meta×Muse Spark + khung đỏ · 15.50 STAT 5 Olympiad · 17.06 Fig5 · 18.74 KHÔNG CÓ CHÌA ĐÁP ÁN · 19.90 PRESENTER · 21.60 chat meta.ai (minh họa) · 22.85 sơ đồ flow + khung đỏ · 24.64 TB arXiv | NGƯỜI VIẾT/AI SOẠN · 26.60 paper3 + badge 2024 · 28.54 Fig3 · 29.70 STAT 384 · 31.06 Fig2 · 32.18 paper2 + khung "Finite-time wave collapse" · 33.70 STAT 2015 · 35.69 TB X post @alexandr_wang | gadgets.muse.ai · 37.42 SS GitHub README · 38.54 LR boards | project ideas · 39.64 STAT 5.000 · 40.84 SS Claim Muse Home Link · 41.90 PRESENTER · 43.42 SS arXiv + dấu CHƯA BÌNH DUYỆT · 44.70 LR paper4|paper5 · 46.69 phương trình chuyên gia + AI chat · 48.26 TB paper6|arXiv · 49.44 PRESENTER outro + câu hỏi · 51.60 ĐEN

## Output
- `/workspace/video-jobs/HM-101/output/storytelling_final_v3.mp4` (54,948,057 bytes · 51.90s · 1080×1920)
- `/workspace/video-jobs/HM-101/output/storytelling_mobile_720p_v3.mp4` (9,775,758 bytes · 51.90s · 720×1280)
- `/workspace/video-jobs/HM-101/output/subtitle_v3.srt` (22 cue, sidecar)
- `/workspace/video-jobs/HM-101/qa/contact_sheet_v3.jpg` (16 khung từ 16 shot khác nhau, lưới 4×4)

## Ghi chú
- Claim giữ nguyên theo script v1; mockup chat được gắn nhãn "Minh họa".
- Ảnh v2 có vài thẻ paper tự thiết kế ghi arXiv ID không khớp với trang abs (vd thẻ paper3 ghi 2608.27372, mà đó lại là bài ellipsoid). v3 crop bỏ phần ID dưới đáy của các thẻ này, và pill trên những shot đó chỉ ghi "Meta AI Research" để không gắn sai nguồn.
- Không dùng img28 (dải thiết bị). India Today vẫn bị chặn (giống v2).
- File 1080 dùng CRF 16 (mặc định "looks" của HyperFrames) → ~55MB; nếu cần file nhẹ hơn có thể nén lại.
- v1/v2 (mp4/wav/srt) không bị động tới.
