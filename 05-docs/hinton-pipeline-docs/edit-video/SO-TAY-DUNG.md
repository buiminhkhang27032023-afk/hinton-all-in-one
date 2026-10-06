# SỔ TAY DỰNG VIDEO — rút từ 80 video của 8 kênh mẫu
Cập nhật: 03/10/2026 (giờ VN). Chỉ dùng để học nội bộ, không đăng lại video gốc.

## 0. Cách đọc sổ tay

### Nguồn dữ liệu
- 80 video, mỗi kênh 10 video (2 video cũ + 8 video mới: một nửa xem nhiều nhất, một nửa mới nhất năm 2026). Tất cả dài dưới 5 phút, độ phân giải ≤1080p.
- Mỗi video có file phân tích riêng: `/workspace/video-learn/<thư-mục-kênh>/<id>_breakdown.md` (timeline theo từng shot) và `<id>_analysis.json` (số liệu thô).
- Contact sheet của từng video: `<id>_sheet.jpg`. Ảnh hook 0–3s (chụp 4 khung hình/giây): `<id>_hook.jpg`.
- Số liệu tổng hợp theo kênh: `/workspace/video-learn/aggregate.json`.
- Ứng viên sfx (bản lọc chặt hơn): `<id>_audio_hf.json`.
- Hai bản xem kỹ từng giây:
  - `xem-ky/kallaway-7645299083573267742.md`
  - `xem-ky/hieuai-7686872745115897109.md`
- Kênh Douyin và Facebook dùng bản thay thế (cách chọn giống các vòng trước):
  - 秋芝2046 và 程序员鱼皮: lấy bản đăng lại trên YouTube. Video của 秋芝 là 16:9; của 鱼皮 có 9 video dọc và 1 video ngang.
  - Nguyễn Tất Kiểm: 1 reel Facebook thật, 9 video còn lại là YouTube Shorts.
  - AI Savvy: cả 10 video lấy từ TikTok.

### Nhãn độ tin cậy
| Nhãn | Ý nghĩa |
|---|---|
| **[ĐO]** | Đo tự động bằng ffmpeg/OpenCV: điểm cắt, độ dài shot, loudness, khoảng lặng, zoom (ORB affine). |
| **[KHUNG]** | Phân loại tự động từ frame (heuristic, có thể sai), hoặc quan sát bằng mắt trên contact sheet. |
| **[OCR]** | Đọc chữ bằng RapidOCR. Tiếng Việt bị mất dấu; màu chữ lấy bằng k-means nên chỉ là ước tính. |
| **[SUY]** | Suy luận. |
| **[XEM KỸ]** | Lấy từ 2 bản xem kỹ từng giây. |

### Quy ước
- Mọi toạ độ px quy về khung **1080×1920** (riêng video ngang của 秋芝: 1920×1080).
- "Frame" = frame ở **30fps** (1 giây = 30 frame).
- Ngưỡng cắt cảnh:
  - Thống kê chính dùng ngưỡng scene **0,3** (chỉ đếm cắt "cứng").
  - Ngưỡng **0,2** bắt thêm jump-cut và đổi B-roll nhẹ.

---

## 1. Bảng số liệu tổng (10 video mỗi kênh) [ĐO]

| Kênh | Thời lượng trung vị | Cắt/phút (0,3 / 0,2) | Shot trung vị (0,3) | Shot p10–p90 | Cắt đầu tiên (trung vị, ngưỡng 0,2) | Nền nhạc liên tục* | Khoảng ngừng ≥0,25s mỗi phút | Ứng viên sfx chặt mỗi phút / % điểm cắt có sfx | LUFS file tải về |
|---|---|---|---|---|---|---|---|---|---|
| Kallaway (EN) | 94s | **24,3 / 31,9** | **1,79s** | 0,88–4,59s | **1,58s** | 94% | **0,1** | 14,9 / **19,6%** | −20,4 |
| Nguyễn Tất Kiểm | 57s | 16,4 / 26,3 | 2,03s | 0,33–8,05s | 3,63s | 97% | 2,1 | 4,4 / 3,7% | −12,9 |
| 秋芝2046 (16:9) | ~190s | 8,9 / 12,8 | 2,77s | 0,83–12,1s | 1,93s | 92% | 2,2 | — (video ngang) | −14,0 |
| 程序员鱼皮 | 55s | 7,9 / 9,5 | 4,10s | 1,27–14,3s | 4,43s | 68% | 15,5 | 5,4 / 4,8% | −10,0 |
| Hiếu AI | 77s | 3,2 / 8,7 | 2,50s | 1,03–21,9s | 2,27s | 86% | 5,8 | 7,0 / 9,8% | −13,0 |
| HungNPV | 117s | 3,0 / 3,5 | **11,8s** | 2,15–36,4s | 5,47s | 72% | 12,2 | 3,9 / 0% | −24,4 |
| Riley Brown (EN) | 120s | 2,4 / 3,7 | 4,17s | 1,39–34,4s | 5,82s | 48% | 7,9 | 17,7 / 20%** | −24,0 |
| AI Savvy (EN) | 87s | 2,4 / 4,4 | 8,27s | 1,82–41,8s | 3,70s | 33% | 4,2 | 20,3 / 0%** | −16,7 |

\* "Nền nhạc liên tục" = phần trăm cửa sổ 1 giây có mức âm thấp nhất vẫn cao hơn (mức giọng − 22 dB), tức không có khoảng lặng thật [ĐO]. Từ đó [SUY] rằng kênh có nhạc nền chạy suốt.

\*\* Ở Riley và AI Savvy, phần lớn "hit tần cao" KHÔNG trùng điểm cắt (Riley 2,4%, AI Savvy 0%). [SUY] Đây có thể là tiếng gõ phím hoặc chuột (Riley quay POV), hoặc hi-hat của nhạc, không phải sfx dựng.

### Phân bố độ dài shot (% số shot, ngưỡng 0,3) [ĐO]

| Kênh | <0,5s | 0,5–1s | 1–2s | 2–3s | 3–5s | 5–8s | >8s |
|---|---|---|---|---|---|---|---|
| Kallaway | 1,0 | 15,4 | **40,9** | 20,1 | 14,1 | 5,9 | 2,6 |
| Nguyễn Tất Kiểm | **14,4** | 5,7 | 28,2 | 17,2 | 13,8 | 10,3 | 10,3 |
| 秋芝2046 | 2,3 | 13,8 | 21,7 | 14,9 | 13,8 | 13,0 | 20,6 |
| 程序员鱼皮 | 2,4 | 3,1 | 15,0 | 15,0 | 24,4 | 14,2 | 26,0 |
| Hiếu AI | 2,1 | 6,4 | **34,0** | 16,0 | 14,9 | 5,3 | 21,3 |
| HungNPV | 0 | 2,7 | 5,3 | 18,7 | 8,0 | 8,0 | **57,3** |
| Riley Brown | 3,0 | 2,0 | 17,0 | 20,0 | 12,0 | 14,0 | 32,0 |
| AI Savvy | 2,1 | 0 | 10,4 | 6,2 | 10,4 | 16,7 | **54,2** |

### Ba nhóm nhịp
1. **Nhóm nhanh** (Kallaway, NTK): 16–24 cắt/phút. 56–76% shot ngắn dưới 3s. Gần như không có khoảng lặng.
2. **Nhóm "khối lặp"** (Hiếu AI, 秋芝, 鱼皮): shot 1–3s xen với khối dài trên 8s. Đây là cấu trúc "lệnh → kết quả" hoặc "mặt → demo".
3. **Nhóm chậm/thật** (HungNPV, Riley, AI Savvy): shot trung vị 4–12s. Hơn một nửa số shot dài trên 8s.
   - Điều giữ người xem là chữ trên màn hình: ô claim, caption 1 chữ, hoặc thanh tiến trình.
   - Nhịp cắt không phải là thứ giữ người xem ở nhóm này.

### Bố cục: % thời lượng theo loại khung [KHUNG – heuristic]

| Kênh | Split mặt dưới | Mặt cận / full | Mặt trung | PIP mặt | Màn hình/UI full | B-roll full | Card tối | Split không mặt |
|---|---|---|---|---|---|---|---|---|
| Kallaway | **55,0** | **24,8** | 5,3 | 0,1 | 1,7 | 2,8 | 4,2 | 2,4 |
| AI Savvy | **81,8** | 0,1 | 0,3 | 0 | 0 | 0,1 | 0,1 | 14,8 |
| Hiếu AI | **66,8** | 5,5 | 2,2 | 0,1 | 5,5 | 3,7 | 1,3 | 12,0 |
| Riley | 54,2 (†) | 2,6 | 1,9 | 1,7 | 12,9 | 16,7 | 1,2 | 7,7 |
| NTK | 16,3 (+12,5 mặt trên) | 20,2 | 10,4 | 0,4 | 9,3 | 12,4 | 2,6 | 15,9 |
| 鱼皮 | 12,8 | 17,6 | 0,8 | 14,7 | 8,3 | 4,7 | 4,8 | 35,6 |
| 秋芝 (16:9) | 6,9 | 2,6 | **34,2** | **23,2** | 11,1 | 9,1 | 7,3 | 4,6 |
| HungNPV | 3,4 | 6,3 | 3,3 | 0,2 | 18,9 | **38,8** (quay laptop bằng điện thoại) | 0,1 | 26,2 |

(†) Riley quay POV bàn làm việc: màn hình ở trên, điện thoại hoặc tay ở dưới. Bộ phân loại hay nhầm loại này thành "split mặt dưới". Trên contact sheet, Riley chủ yếu là POV màn hình hoặc vật thể, ít khi là split mặt thật.

Các nhãn PIP và split của NTK cũng lẫn nhau: NTK thực tế dùng **PIP mặt vuông góc phải trên** đè lên quay màn hình điện thoại.

---

## 2. Thông số phong cách từng kênh

Mỗi kênh trình bày theo cùng một khung: nhịp → bố cục → zoom → caption → đồ hoạ → hook → âm thanh.
- Toạ độ dạng `[x,y,w,h]` tính theo px của khung 1080×1920.
- Mã hex là màu trung vị của các cụm màu bão hoà mà OCR đọc được [OCR, ước tính ±10–15 mỗi kênh màu]. Viền, bóng đổ và nén video có thể làm lệch màu.

### 2.1 Kallaway (@kanekallaway) — "tin AI nhịp nhanh", mẫu chuẩn để học
- **Nhịp [ĐO]**
  - Shot trung vị 1,79s, trung bình 2,42s. 76% shot dài 0,5–3s, chỉ 2,6% dài hơn 8s.
  - 24,3 cắt/phút (ngưỡng 0,2: 31,9).
  - Cắt đầu tiên rơi vào 0,79–4,1s, trung vị 1,58s.
  - Khoảng ngừng giọng ≥0,25s: 0,1 lần/phút. Mọi hơi thở và khoảng nghỉ đều bị cắt sát.
- **Bố cục [KHUNG/ĐO]**
  - Split B-roll trên / mặt dưới chiếm 55% thời lượng. Full face (cận) chiếm 24,8%. Card tối chiếm 4,2%.
  - Đường chia trung vị ở y≈947px (khoảng 1080×960 mỗi nửa) [XEM KỸ].
  - Mặt ở nửa dưới: hộp trung vị `[381,1123,291,291]`, tâm mặt khoảng (526, 1268), tức mắt nằm ở khoảng 1/3 trên của nửa dưới.
  - PIP mặt tròn khoảng 25% chiều rộng (đường kính ~270px) ở góc trái trên, dùng khi nửa trên là UI hoặc điện thoại (0:20–0:28 và 1:00–1:04 trong video 7645) [XEM KỸ].
  - Mockup điện thoại 3D nghiêng trên nền màu thương hiệu (đỏ DoorDash) [KHUNG].
- **Zoom [ĐO]**
  - 20 punch-in đo được, tỉ lệ trung vị ×1,09, p90 ×1,23. Bản xem kỹ ghi punch-in 15–20% giữ mắt ở giữa.
  - Push-in/pull-out chậm trong shot: 9,8 lần/phút (cao nhất trong 8 kênh), tốc độ trung vị 2,7%/s. Một shot 1,8s vì vậy trôi khoảng 5%. [SUY] Mọi shot đều "đang chuyển động".
- **Caption [OCR/ĐO]**
  - 2 chữ/cụm (p90: 6).
  - Đo ở 10fps trên đoạn 6–26s của video 7645: cụm dài trung vị 0,6s = **18 frame** (p10 0,4s = 12 frame; p90 0,9s = 27 frame). 93% cụm nối liền nhau, không có frame trống.
  - Vị trí: mép trên chữ ở y≈1004–1014px, cao hộp chữ ~50–60px (font khoảng 54–64px), tức nằm ngay dưới đường chia.
  - Màu đổi theo video:
    - cam vàng **#E0AC1A** (serif đậm, video 7645);
    - trắng sans đậm (video 7692, DoorDash).
  - Viền hoặc bóng tối kèm theo [KHUNG]. Kiểu xuất hiện: pop/spring từng cụm [XEM KỸ].
- **Chữ to một từ [OCR/XEM KỸ]**
  - Cứ khoảng 6–10s, khi ở full face, hiện MỘT từ phát sáng ("nerdy", "humanity", "force", "creative", "future").
  - Cao hộp chữ 150–230px, ở y≈1100–1150px (giữa thân người).
  - Font đổi theo nghĩa của từ: serif nghiêng cho "future", sans đậm cho "humanity".
- **Tiêu đề hook [OCR]**
  - Chữ in hoa 2 dòng ("OPENAI'S MATH / BREAKTHROUGH", "DOORDASH / DRONE DELIVERY", "GPT-5.5 / THE FUTURE").
  - Hiện trong 1,0s đầu ở ≥7/10 video, nằm ngay trên đường chia (y≈820px).
  - Hiệu ứng lộ chữ: OCR thấy "BREAKT" ở 0,5s, "BREAKTHROL" ở 1,0s, đủ chữ ở 2,0s. Tức chữ lộ dần (wipe hoặc typewriter) trong khoảng 1–1,5s = **30–45 frame**.
  - Nền tối glow đỏ/cam. Đỏ đo được **#CF2C4E**, cam nâu **#98430C**.
- **Âm thanh [ĐO/XEM KỸ]**
  - Nền nhạc liên tục ở 94% cửa sổ 1s.
  - Ứng viên sfx tần cao: 14,9/phút. 19,6% điểm cắt có sfx trong ±0,25s, và 37% số sfx rơi đúng điểm cắt.
  - 7/10 video có hit trong 0–3s.
  - Bản xem kỹ ghi: whoosh khi đổi layout hoặc punch-in, pop khi đổi hình, bass boom dưới từ khoá lớn, tiếng "scan số" cho visual công nghệ. Ở 0:36 ("That is… until now") nhạc tắt hẳn 0,5–1s rồi beat vào lại.
  - Kết bằng câu cuối nối liền câu đầu để video tự lặp.

### 2.2 Nguyễn Tất Kiểm — "listicle/công cụ, nhịp nhanh, chữ vàng"
- **Nhịp [ĐO]**
  - Shot trung vị 2,03s. **14,4% shot ngắn dưới 0,5s**, cao nhất trong 8 kênh: flash, whip hoặc chèn cực ngắn.
  - 16,4 cắt/phút (ngưỡng 0,2: 26,3).
  - Cắt đầu tiên trung vị 3,63s. Video KsqhoO9JXx4 cắt ngay ở frame 2.
- **Bố cục [KHUNG]**
  - Quay màn hình điện thoại full khung, kèm **PIP mặt vuông khoảng 210×210px ở góc phải trên** (x≈850–1060, y≈20–230).
  - Talking head cận chiếm khoảng 20% thời lượng. Card listicle (nền đen, lưới toả tia, logo ở giữa, số xanh lá) chỉ có ở một số video.
- **Zoom [ĐO]**
  - 12 punch-in, trung vị ×1,19, tối đa ×1,56. Đây là mức punch mạnh nhất trong 8 kênh.
  - Push chậm 3,3 lần/phút, tốc độ ~1,7%/s.
- **Caption [OCR/KHUNG]**
  - IN HOA đậm màu vàng **#E5C32C** (biến thể cam **#E38932**), viền đen dày.
  - 4 chữ/cụm (p90: 10). Cao hộp chữ ~64px.
  - Vị trí y≈1190–1450px (0,62–0,75H).
  - Mũi tên đỏ chỉ đúng nút cần bấm.
- **Hook [OCR]**
  - ≥5/10 video mở bằng tiêu đề IN HOA to ngay ở t=0 ("MUỐN BIẾN CLAUDE AI THÀNH TRỢ LÝ ĐẮC LỰC", "TOP NHỮNG CÔNG CỤ AI…", "BÂY GIỜ TOP 1 LÀM AFFILIATE…", "10 công cụ AI tạo video").
  - Có zoom-blur trong 0,5s đầu (vòng trước).
- **Outro [KHUNG]**
  - Clip talking head khác, kèm nút **FOLLOW** xanh dương **#388DD0** chữ trắng và con trỏ tay bấm, ở góc phải trên (y≈450–550px).
  - Caption vàng nhỏ ở y≈1580px.
- **Âm thanh [ĐO]**
  - Nhạc gần như liên tục (97% cửa sổ). Ngừng chỉ 2,1 lần/phút. LUFS −12,9.
  - Sfx tần cao ít (4,4/phút) và chỉ 3,7% điểm cắt có sfx. [SUY] Nhịp chủ yếu do nhạc và cắt, ít sfx.

### 2.3 秋芝2046 — "talking head + demo, 16:9, song ngữ"
- **Nhịp [ĐO]**
  - Shot trung vị 2,77s, 8,9 cắt/phút. 36% shot dài 0,5–2s và 21% dài trên 8s (demo).
  - Cắt đầu tiên trung vị 1,93s. Có video cắt ở 0,77s và 0,9s.
- **Bố cục**
  - Mặt trung cảnh trong studio neon tím chiếm 34%. PIP mặt (tròn, góc trái dưới) đè lên UI chiếm 23%. UI full 11%, B-roll AI 9%, card tối 7%.
- **Zoom [ĐO]**
  - 51 punch-in và 54 punch-out trong 34,6 phút (~3 lần/phút), khoảng ×0,73–×1,28.
  - [SUY] Máy quay có 2 cỡ cảnh (trung ↔ cận) và được cắt luân phiên.
  - Push chậm 3,8 lần/phút.
- **Phụ đề [OCR]**
  - Song ngữ: chữ Trung trắng ở trên, tiếng Anh nhỏ hơn ở dưới. Nằm ở y≈834–945px trên khung cao 1080 (0,77–0,88H). Cao hộp chữ ~56px. Mỗi cụm khoảng 8 ký tự Trung.
- **Màu nhấn [OCR]**
  - Từ khoá to **vàng #F3D710** viền đen/3D ở giữa khung.
  - Chip lime **#9DF318** ở góc trái trên.
  - Tím neon **#777EE8** (đèn studio).
- **Hook [OCR]**
  - 4/10 video mở bằng lời chào "你好啊 / 朋友们" và phụ đề ngay frame 0.
  - Đến khoảng 2,5s thì hiện từ khoá to ("GPT-5", "百万运镜", "Pika").
- **Kết**
  - End card logo "秋芝2046" trên nền đen. Chuyển cảnh glitch giữa các phần (vòng trước).
- **Âm thanh [ĐO]**
  - Nhạc liên tục ở 92% cửa sổ. Ngừng 2,2 lần/phút. LUFS −14,0.

### 2.4 程序员鱼皮 — "dev short, chữ Trung to, bằng chứng"
- **Nhịp [ĐO]**
  - Shot trung vị 4,10s, 7,9 cắt/phút. 26% shot dài trên 8s.
  - Cắt đầu tiên trung vị 4,43s: mở bằng một câu nói liền, không cắt.
- **Bố cục**
  - Mặt toàn khung hoặc mặt cận chiếm khoảng 18%.
  - Nửa trên là ảnh chụp, code hoặc chat; nửa dưới là mặt (≈13% + 36% "split không mặt").
  - Tiêu đề phần là chữ trắng trên dải đen ở đỉnh khung (y 0–200px) [KHUNG].
- **Caption [OCR]**
  - Chữ Trung trắng viền đen, **cao hộp ~78px** (to nhất trong 8 kênh), 8 ký tự/cụm (p90: 12).
  - Vị trí y≈1170–1340px (0,6–0,7H).
  - Câu chỉ dẫn quan trọng màu **vàng #F7DF22**, đặt giữa khung. Khung chữ nhật đỏ khoanh code. Mũi tên đỏ viền.
- **Hook [OCR]**
  - 6/10 video mở bằng câu nói kèm caption ngay frame 0, dạng thách đố hoặc khẳng định ("来猜猜看啊", "我把自己蒸馏成了一个AI的skill", "你一定没用过这玩意吧").
- **Kết**
  - Câu hỏi "你学会了吗". Cuối video có hiệu ứng biến dạng mặt hoặc emoji (giọt mồ hôi).
- **Âm thanh [ĐO]**
  - Giữ khoảng ngừng tự nhiên: 15,5 lần/phút, nhiều nhất trong 8 kênh.
  - Nhạc liên tục ở 68%. Loudness cao nhất: LUFS −10,0.

### 2.5 Hiếu AI (@hieuanca) — "lệnh → kết quả, pill lime"
- **Nhịp [ĐO]**
  - Ngưỡng 0,3: 3,2 cắt/phút. Ngưỡng 0,2: 8,7 cắt/phút (nhiều đổi cảnh "mềm" trong cùng một nền).
  - Shot trung vị 2,50s. 34% shot dài 1–2s, 21% dài trên 8s.
  - Cắt đầu tiên trung vị 2,27s.
- **Cấu trúc [XEM KỸ, video 7686]**
  - Lặp 7 vòng, mỗi vòng gồm:
    1. split 1–2s: UI ChatGPT gõ lệnh ở trên, mặt ở dưới, pill lime ghi lệnh "/360view"…, kèm tiếng gõ phím;
    2. cắt cứng;
    3. kết quả ảnh AI full khung 2–5s, Ken Burns khoảng 5%, caption trắng viền đen highlight vàng từng từ, whoosh ở điểm cắt.
  - Video 40s có 14 cắt, shot trung vị 2,6s [ĐO].
- **Bố cục [KHUNG/ĐO]**
  - Split mặt dưới chiếm 66,8%. Ở các video hướng dẫn: PIP mặt nhỏ `[72,1373,211,211]` ở góc trái dưới, đè lên screen record nền tối có vân địa hình.
- **Zoom [ĐO]**
  - Punch-in trung vị ×1,26, punch-out ×0,76. Mặt luân phiên 100% ↔ khoảng 115–125% mỗi vòng.
  - Push chậm 3,9 lần/phút (~1,5%/s). Đoạn kết là mặt full khung zoom chậm.
- **Màu [OCR]**
  - Pill **lime #C1E732** chữ đen. Đây là màu nhất quán nhất: xuất hiện ở 17% mẫu caption.
  - Highlight **vàng #EFC825**. Caption trắng đậm viền đen. Mũi tên hoặc khoanh tròn đỏ.
  - Cụm caption khoảng 3 chữ (video 7686). Các video tutorial bị UI làm nhiễu số đếm.
- **Âm thanh [ĐO/XEM KỸ]**
  - Nhạc điện tử nhỏ (~−20 dB dưới giọng) liên tục ở 86% cửa sổ, tắt đột ngột ở cuối.
  - 9,8% điểm cắt có sfx. Tiếng gõ phím đi kèm pill lệnh.

### 2.6 HungNPV — "selfie + quay laptop bằng điện thoại, không caption chạy"
- **Nhịp [ĐO]**
  - Shot trung vị **11,8s**, 57% shot dài trên 8s, 3,0 cắt/phút.
  - Cắt đầu tiên trung vị 5,47s. Hook selfie giữ nguyên, không cắt trong 3,6–7,2s đầu.
- **Hook [OCR]**
  - **10/10 video** có ô claim 2–3 dòng ngay ở t=0.
  - Mẫu câu: "Đừng … nữa, dùng AI này!", "… đang âm thầm …", "Không tốn tiền cho …, dùng AI miễn phí …".
  - Ô trắng bo góc, chữ đen đậm, đặt ở giữa ngực (y≈760–1290px).
- **Bố cục [KHUNG]**
  - Quay màn hình laptop bằng điện thoại (rung tay nhẹ: push drift 2,5 lần/phút, ~2%/s) kèm ngón tay chỉ vào UI.
  - Nhãn bước dạng ô trắng ("B1/B2/B4: …") ở mép trên.
  - Kết: selfie kèm ô "Follow for more".
  - Không có caption chạy theo lời và không có punch-in.
- **Âm thanh [ĐO]**
  - LUFS −24,4 (nhỏ, gần như thu thô). Ngừng 12,2 lần/phút. Sfx gần như không trùng điểm cắt (0%).

### 2.7 Riley Brown (@rileybrown.ai) — "POV build app, ít cắt"
- **Nhịp [ĐO]**
  - Shot trung vị 4,17s, 32% shot dài trên 8s, 2,4 cắt/phút.
  - Cắt đầu tiên trung vị 5,82s. Có video giữ 66s mới cắt.
- **Hook [OCR]**
  - 7/10 video có ô tiêu đề ngay ở t=0–1s ("Opus 5.5 is Insane", "GPT-6 is absurd", "Vibe Coding is Getting Out of Hand", "Wow… Vibe Coding Mobile App in 2 Prompts").
  - Ô đen bo góc, chữ trắng, đặt ở trên cùng. Giữ khoảng 10s.
- **Caption [KHUNG/OCR]**
  - IN HOA trắng đậm có bóng đen, 1–4 chữ (trung vị 4), đặt ở dưới (y≈1600–1700px) trong video POV.
  - Video cũ đặt caption nhỏ ở đường nối (y≈960px).
  - Màu xanh **#4585BE / #13A7EE** đo được là màu UI, không phải màu caption.
- **Âm thanh [ĐO]**
  - LUFS −24,0. Nhạc liên tục chỉ ở 48% cửa sổ (nhiều đoạn chỉ có giọng và tiếng môi trường).

### 2.8 AI Savvy — "tin công cụ video AI, caption 1 chữ cam"
- **Nhịp [ĐO]**
  - Shot trung vị 8,27s, 54% shot dài trên 8s, 2,4 cắt/phút.
  - Hai video không có cắt cứng nào (20s và 51s): toàn bộ chỉ là một layout split cố định, phần thay đổi là clip trong ô trên.
- **Bố cục [ĐO/KHUNG]**
  - Split mặt dưới chiếm **81,8%**. Đường chia ở y≈994px. Mặt `[415,1210,257,257]`.
  - Biến thể 3 vùng:
    - dải đen y 0–190 có logo công cụ;
    - clip 16:9 ở y≈190–640;
    - thanh tiến trình đỏ "TUTORIAL INCOMING" ở y≈700;
    - người nói (studio đèn LED lục giác) ở nửa dưới.
- **Caption [OCR]**
  - **1 chữ/cụm** (p90: 4), cam **#E99214** viền đen.
  - Cao hộp ~50px, ở y≈850–1070px, tức ngay đường chia. Màu này xuất hiện ở 84% mẫu caption của kênh.
  - Pill cam "openart.ai" / "LINK IN BIO" ở cuối.
- **Hook [OCR]**
  - 9/10 video hiện tên công cụ hoặc model ngay ở t=0 ("Wan 3.0", "FLUX 3", "INTRODUCING GPT-6", "Kimi-K3: Ranked #1", "SEEDANCE 2.5 + Runway").
- **Âm thanh [ĐO]**
  - Phần lớn chỉ có giọng: nhạc liên tục chỉ ở 33% cửa sổ. LUFS −16,7.

---

## 3. Bộ quy chuẩn chung cho kênh mình (khung 1080×1920, 30fps)

Quy chuẩn rút từ số đo ở trên. Phần nào là đề xuất suy ra, có ghi [SUY].

### 3.1 Lưới và vùng an toàn
| Vùng | Toạ độ (px) | Ghi chú |
|---|---|---|
| Tránh UI phía trên | y 0–150 | Thanh trạng thái, tên tài khoản (D9). Tiêu đề phần kiểu 鱼皮 vẫn đặt được ở y 60–200 nếu chữ to. |
| Tránh UI phía dưới | y 1590–1920 | Caption ứng dụng, nút. Riley đặt caption ở y≈1600–1700, sát giới hạn: **không nên học theo**. |
| Tránh cột nút bên phải | x 940–1080 | Nút like/comment/share. |
| Đường chia split | **y = 960** (Kallaway 947, AI Savvy 994 [ĐO]) | Nửa trên 1080×960 là B-roll; nửa dưới là mặt. |
| Mắt người nói khi split | y ≈ 1230–1290, x ≈ 540 | Kallaway: tâm mặt (526, 1268) [ĐO]. |
| Caption chạy (split) | mép trên y≈980–1010, cao 50–64px | Ngay dưới đường chia (Kallaway, AI Savvy) [ĐO]. |
| Caption chạy (full khung/screen) | y ≈ 1190–1400 (0,62–0,73H) | NTK, 鱼皮, Hiếu [ĐO/KHUNG]. Nằm gọn trong vùng 47–69% của D9. |
| Chữ to một từ | tâm y ≈ 1100–1200, cao 150–230px | Kallaway [OCR]. |
| Tiêu đề hook | y ≈ 760–900 (ngay trên đường chia) hoặc y 150–400 (ô trên cùng kiểu Riley) | |
| PIP mặt | Tròn đường kính 260–300px ở góc trái trên (x 40, y 170); hoặc vuông 210px ở góc phải trên (NTK, nhớ né cột phải: x ≤ 920); hoặc tròn 210px ở góc trái dưới (Hiếu: `[72,1373,211,211]`) | |

### 3.2 Caption — 2 tầng (D14)
- **Tầng thường**
  - Sans đậm (Montserrat ExtraBold, Be Vietnam Pro Black, hoặc SVN-Gilroy Heavy, cần đủ dấu tiếng Việt), cỡ **56–64px**, trắng #FFFFFF.
  - Viền đen #000000 dày 6–8px, hoặc bóng đổ đen 60% lệch 4px.
  - **2 chữ/cụm** cho tin nhanh (Kallaway: 2) hoặc **1 chữ/cụm** cho kiểu "punchy" (AI Savvy). Với hướng dẫn, tối đa 4–5 chữ (NTK: 4).
- **Tầng nhấn** (tối đa 1 từ mỗi câu, D9). Chọn một màu thương hiệu và dùng mãi:
  - vàng cam #E0AC1A (Kallaway);
  - vàng #E5C32C–#F7DF22 (NTK, 鱼皮);
  - cam #E99214 (AI Savvy);
  - lime #C1E732 (Hiếu).
  - [SUY] Đề xuất cho Cường Mê AI: **#F5C518** (vàng) cho từ khoá và **#FF4D4F** (đỏ) cho vấn đề/lỗi, theo C11.
- **Thời lượng mỗi cụm**
  - Trung vị **18 frame (0,6s)**, chấp nhận 12–27 frame (0,4–0,9s) [ĐO, Kallaway].
  - Các cụm nối liền nhau (93% không có frame trống). Chỉ để trống khi chuyển sang graphic lớn.
- **Animation vào** [XEM KỸ + D7]
  - Pop/spring: scale 80→108→100% trong **4–6 frame**, opacity 0→100 trong 2 frame.
  - Không cần animation ra: cụm sau thay thế cụm trước ngay.
- **Chữ to một từ**
  - Cỡ 150–230px. Font có thể khác (serif nghiêng hoặc display) để hợp với nghĩa của từ. Glow vàng hoặc trắng.
  - Vào bằng scale 120→100% trong 6 frame và blur 8→0 [SUY], kèm bass hit.
- **Tiêu đề hook**
  - 2 dòng IN HOA, 3–5 chữ, cỡ 80–110px, nằm trên nền tối có glow đỏ/cam (Kallaway) hoặc trong ô đen bo góc 24px (Riley).
  - Lộ chữ bằng wipe trong **30–45 frame** (Kallaway [OCR]), hoặc pop trong 6 frame. Phải hiện xong trước giây 1,0–2,0.

### 3.3 Nhịp và zoom
| Dạng video | Shot trung vị mục tiêu | Cắt/phút | Cắt đầu tiên | Punch-in | Push chậm |
|---|---|---|---|---|---|
| Tin AI nóng | 1,6–2,0s | 20–30 | ≤1,6s | ×1,10–1,20 mỗi 6–10s | 2–3%/s trong mọi shot talking head |
| Top N / listicle | 2,0s (cho phép 10–15% shot <0,5s) | 15–25 | ≤3,6s | ×1,15–1,30 | 1,5–2%/s |
| Lệnh → kết quả | khối 1–2s (lệnh) + 2–5s (kết quả) | 8–12 (ngưỡng 0,2) | ≤2,3s | Luân phiên 100% ↔ 115–125% | Ken Burns 5% mỗi ảnh |
| Hướng dẫn thật | 4–12s | 3–5 | 4–6s (giữ hook selfie) | không | rung tay tự nhiên hoặc 1–2%/s |

- Jump-cut cùng khung (zoom ×0,98–1,02) chiếm áp đảo ở mọi kênh [ĐO]. Cắt bỏ khoảng ngừng là "xương sống". Punch-in chỉ là gia vị: Kallaway có 20 punch so với 361 jump-cut.
- Khi punch-in, phải giữ mắt ở cùng vị trí (D5). Keyframe cả Position.

### 3.4 Âm thanh
- **Nhạc nền**
  - Nhóm nhanh chạy nhạc gần như liên tục (92–97% cửa sổ có nền) [ĐO]. Đặt nhạc thấp hơn giọng 18–22 dB (Hiếu: ~−20 dB [XEM KỸ]).
  - Ngắt nhạc 0,5–1s ngay trước câu reveal ("That is… until now"), rồi vào lại đúng âm tiết tiếp theo [XEM KỸ].
- **Khoảng ngừng**
  - Tin nhanh: cắt hết mọi khoảng ngừng ≥0,25s (Kallaway: 0,1 lần/phút).
  - Hướng dẫn hoặc tâm sự: giữ 10–15 khoảng/phút (鱼皮 15,5, HungNPV 12,2).
- **Sfx**
  - Kallaway có sfx ở **khoảng 20% điểm cắt**, không phải ở mọi điểm cắt. Ưu tiên đặt sfx tại:
    1. đổi layout (split → full face): whoosh nhẹ;
    2. chữ to một từ: bass boom hoặc hit;
    3. đổi B-roll: pop hoặc click nhỏ;
    4. visual công nghệ: tiếng scan/data.
  - Hook 0–3s: 1–2 sfx (7/10 video Kallaway có hit trong 0–3s).
- **Loudness**
  - File tải về dao động từ −10 LUFS (鱼皮) đến −24 LUFS (HungNPV, Riley) [ĐO]. Không có chuẩn chung giữa các kênh.
  - [SUY] Xuất ở **−14 LUFS integrated, true peak −1 dBTP**. Đây là mức giữa của các kênh nhóm nhanh (NTK −12,9, Hiếu −13,0, 秋芝 −14,0).

---

## 4. Công thức dựng (C1–C14 đã chỉnh theo số đo mới)
Mỗi công thức có các phần: **Khi nào dùng**, **Số liệu**, và **Các bước** cho CapCut (CC), Premiere (PR), ffmpeg (FF), HyperFrames (HF).

HyperFrames: dùng repo `/workspace/AI-auto-generate-video`, các templateId lấy trong `genres-formats-ui.md`.

> **Lưu ý quy tắc nội bộ:** `playbook-san-xuat.md` hiện đặt mặc định "no karaoke burn · no BGM", karaoke chỉ khi được yêu cầu. Trong khi đó, 6/8 kênh mẫu đều burn caption và chạy nhạc nền 68–97% thời lượng.
>
> Các công thức dưới đây mô tả cách kênh mẫu làm. **Có bật caption burn-in và nhạc nền hay không là quyết định của người dùng, sổ tay này không tự đổi mặc định.**

### C1. Split "B-roll trên / mặt dưới" (Kallaway 55%, AI Savvy 82%, Hiếu 67%)

**Số liệu:**
- Đường chia ở y=960. Mỗi nửa 1080×960.
- Mặt crop từ ngực trở lên, mắt ở y≈1250.
- Tin nóng: B-roll trên đổi mỗi 1–2s, cắt theo downbeat hoặc theo mệnh đề.
- Hướng dẫn: giữ screen record liên tục.

**Các bước:**
- **CC:**
  1. Canvas 9:16. Track chính là talking head; Scale sao cho mặt lấp nửa dưới, rồi kéo Position Y xuống khoảng +480px.
  2. Thêm Overlay B-roll, Scale lấp 1080×960, đặt ở nửa trên.
  3. Mask "Linear" ở đường y=960, hoặc dùng crop.
  4. Cắt B-roll theo beat: bật "Beats" trên track nhạc, mỗi 1–2 beat đổi một clip.
- **PR:**
  1. Sequence 1080×1920.
  2. V1 là mặt (Position 540, 1440). V2 là B-roll với Crop Bottom 50% (Position 540, 480).
  3. Dùng Essential Graphics để dựng đường kẻ 4px #000 ở y=960 (tuỳ chọn).
- **FF:**
  - `[0:v]scale=1080:-2,crop=1080:960:0:(ih-960)/3[face];[1:v]scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960[top];[top][face]vstack=inputs=2[v]`
- **HF:** chưa có template split sẵn trong catalog.
  - Dùng `frame-build-minimal` cho nửa trên, ghép mặt bằng FF vstack.
  - Hoặc đề xuất thêm template "split-960" [SUY].

### C2. Punch-in full face + MỘT chữ to (Kallaway: full face 24,8% thời lượng)

**Số liệu:**
- Mỗi 6–10s thoát split sang full face, zoom ×1,10–1,20 (đo được trung vị ×1,09, p90 ×1,23; bản xem kỹ ghi 15–20%).
- Mỗi lần giữ 1–2,5s, kèm một từ cao 150–230px ở y≈1100–1200.
- Sfx bass boom đặt ở frame từ đó hiện ra.

**Các bước:**
- **CC:**
  1. Split clip ở từ khoá.
  2. Đoạn sau: Scale 115%, chỉnh Position để mắt giữ nguyên vị trí cũ.
  3. Thêm Text 180px, hiệu ứng In "Pop"/"Zoom" khoảng 0,2s, cùng Glow.
  4. Thêm sfx "boom".
- **PR:**
  1. Cắt bằng Razor, Motion > Scale 115.
  2. Đặt MOGRT chữ to; keyframe Scale 120→100 trong 6 frame, Gaussian Blur 8→0.
- **FF:**
  - `zoompan` không tiện cho punch tức thời. Dùng `crop=iw/1.15:ih/1.15:(iw-iw/1.15)/2:(ih-ih/1.15)/2.6,scale=1080:1920` trên đoạn đã tách.
  - Chữ dùng `drawtext=fontsize=180:fontcolor=#F5C518:borderw=8:x=(w-tw)/2:y=1100`.
- **HF:** `frame-bold-poster` cho từ khoá (nếu muốn card thay cho mặt).

### C3. Tiêu đề hook trong 1–2s đầu (Kallaway ≥7/10 video, Riley 7/10, AI Savvy 9/10, HungNPV 10/10)

**Số liệu:**
- Hiện xong trước 1,0–2,0s.
- Kallaway: lộ chữ dần trong 30–45 frame, 2 dòng IN HOA, ở y≈820, nền tối glow đỏ #CF2C4E.
- Riley: ô đen bo góc chữ trắng ở trên cùng, giữ khoảng 10s.
- AI Savvy: tên công cụ hoặc model nằm ở dải đen trên cùng.

**Các bước:**
- **CC:** Text 2 dòng 96px, In "Typewriter"/"Wipe" 1,2s, Background #111 opacity 85%, Shadow đỏ.
- **PR:** Essential Graphics, Linear Wipe 0→100 trong 36 frame.
- **FF:** `drawtext` + `enable='gte(t,0)'`. Hiệu ứng lộ chữ thay bằng crop động `crop=w='min(iw,iw*t/1.2)'` trên lớp PNG chữ.
- **HF:** `frame-liquid-bg-hero` hoặc `frame-bold-poster` cho scene hook, 1,5–2s.

### C4. Hook selfie + ô claim trắng (HungNPV 10/10)

**Số liệu:**
- Ô trắng bo góc 20–24px, chữ đen đậm 48–56px, 2–3 dòng, ở y≈760–1290 (giữa ngực).
- Giữ 3,6–7,2s không cắt (cắt đầu tiên trung vị 5,47s).

**Mẫu câu:**
- "Đừng [việc cũ] nữa, dùng AI này!"
- "[Tên lớn] đang âm thầm [điều bất ngờ]"
- "Không tốn tiền cho [X], dùng AI miễn phí [Y]"

**Các bước:**
- **CC:** Text với Background trắng, Radius 20, Padding 24.
- **FF:** `drawbox` + `drawtext`, hoặc PNG dựng sẵn (Pillow).

### C5. Pill lệnh/prompt (Hiếu AI)

**Số liệu:**
- Pill lime **#C1E732**, chữ đen đậm 44–52px, đặt ở đường chia.
- Đi cùng animation gõ phím và tiếng phím trong 1–2s.

**Cấu trúc "N lệnh":** mỗi mục = 2s split gõ lệnh + 3–4s kết quả full khung. Với N=7, video dài khoảng 40s [XEM KỸ].

**Các bước:**
- **CC:** Text "/360view" + Background #C1E732 + Radius 999. Animation "Typewriter" 0,6–1s. Thêm sfx "keyboard typing".
- **HF:** `frame-aicoding-list` (mỗi lệnh một mục).

### C6. PIP mặt (Kallaway: tròn trái trên; 秋芝: tròn trái dưới, 23% thời lượng; Hiếu: tròn trái dưới 211px; NTK: vuông phải trên 210px)

**Số liệu:**
- Tròn đường kính 260–300px, feather 2–4px, viền trắng 4px [SUY].
- Dùng cho đoạn demo dài hơn 4s để không mất người dẫn.

**Các bước:**
- **CC:** Overlay mặt, Mask Circle, Scale 25%, đặt ở (40, 170) hoặc (40, 1360).
- **FF:** `geq` alpha tròn, hoặc mask PNG + `overlay=40:170`.

### C7. Nhãn bước và đánh dấu click (HungNPV, Hiếu, NTK, 鱼皮)

**Số liệu:**
- Ô trắng "B1: …" ở mép trên vùng UI.
- Mũi tên đỏ #E53935 chỉ nút bấm, hiện trước thao tác 6–10 frame [SUY].
- Khung chữ nhật đỏ 6px khoanh code (鱼皮).
- Khoanh tròn đỏ (Hiếu).

**Các bước:** CC Sticker arrow + Shape. Dùng thêm D8 (làm tối vùng xung quanh).

### C8. Chip tên phần (秋芝, 鱼皮)

**Số liệu:**
- 秋芝: chip lime **#9DF318** ở góc trái trên, giữ suốt phần đó.
- 鱼皮: tiêu đề phần chữ trắng trên dải đen ở đỉnh khung (y 60–200).

### C9. Card listicle (NTK)

**Số liệu:**
- Card 1–2s gồm: nền đen lưới toả tia, logo công cụ khoảng 40% chiều rộng, số thứ tự xanh lá, caption vàng #E5C32C.
- Sau mỗi card là 1–2 clip demo ngắn khoảng 2s.
- Cho phép 10–15% shot ngắn dưới 0,5s (flash).

**HF:** `frame-aicoding-list` / `frame-pentagram-stat`.

### C10. So sánh trước/sau, hoặc 3 vùng (AI Savvy)
- Dải đen trên cùng chứa logo công cụ.
- Clip 16:9 ở y≈190–640.
- Nhãn hoặc thanh tiến trình đỏ ở y≈700 ("TUTORIAL INCOMING").
- Người nói ở nửa dưới.
- Caption 1 chữ màu cam #E99214 ở đường chia.

### C11. Caption to, đổi màu theo nghĩa (鱼皮, Hiếu, NTK)

**Số liệu:**
- Cao hộp chữ 64–78px. Đặt ở y≈1190–1340 khi full khung.
- Màu theo nghĩa: vàng = giải pháp hoặc chỉ dẫn; đỏ = lỗi hoặc vấn đề.
- Câu chỉ dẫn quan trọng: chữ vàng đặt giữa khung (鱼皮).

### C12. Bằng chứng thật (鱼皮, Riley)
- Chèn ảnh chụp chat, log hoặc tweet ngay sau hook (trước giây 8).
- Thêm khung đỏ và mũi tên.

### C13. Outro/CTA
- NTK: nút FOLLOW xanh dương **#388DD0** với con trỏ tay bấm, ở góc phải trên (y≈450–550). Chú ý né cột nút: x ≤ 920.
- AI Savvy: pill cam "LINK IN BIO".
- 鱼皮: câu hỏi "Bạn học được chưa?".
- 秋芝: logo trên nền đen, khoảng 1,5s.
- HungNPV: selfie kèm ô "Follow for more".
- Kallaway: loop, câu cuối nối liền câu đầu.

### C14. Chuyển cảnh
- Hard cut chiếm áp đảo ở mọi kênh [ĐO]: jump-cut cùng khung là loại phổ biến nhất trong số các điểm cắt có so khớp affine.
- Hiệu ứng chỉ dùng điểm xuyết: zoom-blur trong 0,5s đầu (NTK), glitch giữa các phần (秋芝), whoosh kèm punch (Kallaway).
- Tối đa 1–2 hiệu ứng mỗi video.

### Chỉnh D1–D17 theo số đo
| Mã | Bổ sung từ số đo |
|---|---|
| D1/D3 | Text hook đã hiện ở t≤1s trong 10/10 video HungNPV, 9/10 AI Savvy, ≥7/10 Kallaway và 7/10 Riley [OCR]. Đặt làm **bắt buộc**. |
| D5/D6 | Punch-in thật chỉ khoảng 5% số điểm cắt (Kallaway: 20 trên khoảng 395 điểm có so khớp). Phần còn lại là jump-cut cùng khung. Push chậm 2–3%/s là chuẩn Kallaway. |
| D7 | Cụm caption đo được 12–27 frame. Animation vào phải xong trong ≤6 frame, nếu không chữ sẽ "chưa kịp đứng" thì đã bị thay. |
| D9 | Số đo xác nhận cụm 2 chữ (Kallaway) hoặc 1 chữ (AI Savvy). Vị trí 0,51–0,55H khi split, 0,62–0,73H khi full khung. |
| D10/D11 | Sfx ở khoảng 20% điểm cắt (Kallaway). Không gắn whoosh cho mọi cắt. Ngắt nhạc 0,5–1s trước câu reveal [XEM KỸ]. |
| D12 | Đặt mục tiêu −14 LUFS. Kênh mẫu dao động từ −10 đến −24 LUFS. |
| D13 | Kallaway: loop câu cuối nối vào câu đầu [XEM KỸ]. |
| D16 | Nhóm chậm (HungNPV 11,8s/shot, Riley 4,2s, AI Savvy 8,3s) vẫn thành công nhờ ô claim, tiêu đề và caption 1 chữ. Chọn nhịp theo dạng nội dung, đừng ép mọi video phải nhanh. |

---

## 5. Khung thời gian mẫu 30s / 60s / 90s

Ký hiệu bố cục:
- **S** = split B-roll trên / mặt dưới
- **F** = full face (punch)
- **P** = PIP mặt trên màn hình
- **U** = UI hoặc kết quả full khung
- **K** = card (listicle, tiêu đề)
- **O** = outro

Mọi mốc tính bằng giây (frame = giây × 30).

### 5.1 Tin AI nóng (mẫu Kallaway). Mục tiêu: shot ~1,8s, ~24 cắt/phút

**30s (khoảng 12–14 cắt):**

| Giây | Bố cục | Chữ | Âm thanh |
|---|---|---|---|
| 0,0–1,5 | S (B-roll là key visual của tin) | Tiêu đề 2 dòng lộ chữ trong 0–1,2s; caption 2 chữ từ frame 0 | Nhạc vào ở frame 0; whoosh lúc tiêu đề vào |
| 1,5–3,0 | S (đổi B-roll ở ~1,5s) | Caption | Pop khi đổi B-roll |
| 3,0–4,5 | F ×1,15 | Một chữ to (từ tương phản, D17) | Bass hit |
| 4,5–10 | S, B-roll đổi mỗi 1–2s | Caption 2 chữ/18 frame | |
| 10–12 | F ×1,15 | Một chữ to | Hit |
| 12–20 | S hoặc P (nếu demo UI) | Caption | Click hoặc scan |
| 20–21 | (ngắt nhạc 0,5–1s) | Câu reveal | Nhạc tắt rồi vào lại |
| 21–27 | S → F ×1,2 | Một chữ to | Hit |
| 27–30 | F, push-in 3%/s | Câu cuối nối vào câu đầu (loop) | Nhạc fade 0,3s hoặc cắt sạch |

**60s (khoảng 24 cắt):**

| Giây | Bố cục | Nội dung |
|---|---|---|
| 0–3 | S + tiêu đề | Hook giống bản 30s |
| 3–5 | F | Chữ to lần 1 |
| 5–15 | S | Bối cảnh; B-roll 1–2s |
| 15–17 | F | Chữ to lần 2 |
| 17–28 | P (UI hoặc demo) | Mockup điện thoại, chat |
| 28–30 | F | Chữ to lần 3 |
| 30–31 | Ngắt nhạc | Câu reveal |
| 31–45 | S | Phân tích ý nghĩa |
| 45–47 | F | Chữ to lần 4 |
| 47–56 | S hoặc P | Hệ quả |
| 56–60 | F, push-in | Kết loop |

Tổng phân bổ: S khoảng 55%, F khoảng 20–25%, P khoảng 15% (khớp số đo của Kallaway).

**90s:** giống bản 60s nhưng thêm 1 khối "P/U 15s" và 2 lần F, để giữ nhịp punch mỗi 6–10s.

| Giây | Bố cục |
|---|---|
| 0–3 | Hook |
| 3–5 | F |
| 5–17 | S |
| 17–19 | F |
| 19–34 | P/U |
| 34–36 | F |
| 36–37 | Ngắt nhạc |
| 37–52 | S |
| 52–54 | F |
| 54–69 | P/U |
| 69–71 | F |
| 71–85 | S |
| 85–90 | F loop |

### 5.2 "N lệnh / N công cụ" (mẫu Hiếu AI + NTK)

**30s (N=4):**

| Giây | Bố cục | Nội dung |
|---|---|---|
| 0–0,5 | U | Kết quả đẹp nhất (D3), zoom-blur 0,5s |
| 0,5–2,5 | S + pill lệnh 1 | Gõ phím |
| 2,5–6 | U | Kết quả 1, Ken Burns 5%, caption vàng |
| 6–8 / 8–12 | S / U | Lệnh 2 / kết quả 2 |
| 12–14 / 14–18 | S / U | Lệnh 3 / kết quả 3 |
| 18–20 / 20–25 | S / U | Lệnh 4 / kết quả 4 |
| 25–30 | F, zoom chậm | CTA "comment từ khoá" + câu hỏi |

**60s (N=7):** mỗi vòng = 2s S (lệnh) + 4s U (kết quả), tức 6s.
- 0–1: U (hook kết quả).
- 1–43: 7 vòng.
- 43–55: F tổng kết, kèm K danh sách cả 7 lệnh.
- 55–60: O.

Mặt ở các khối S luân phiên 100% ↔ 120%.

**90s (Top 10 kiểu NTK):**
- 0–3: K tiêu đề IN HOA ("TOP 10 CÔNG CỤ AI…").
- 3–83: 10 mục × 8s. Mỗi mục = 1,5s K (logo + số xanh lá) + 6,5s U (quay màn hình) với PIP vuông góc phải trên, caption vàng 4 chữ, mũi tên đỏ.
- 83–90: O (FOLLOW + con trỏ tay).

### 5.3 Hướng dẫn thật (mẫu HungNPV + 鱼皮). Mục tiêu: shot 4–12s

**30s:**

| Giây | Bố cục | Nội dung |
|---|---|---|
| 0–5 | Selfie + ô claim | Không cắt |
| 5–12 | U (quay màn hình hoặc laptop) | Nhãn "B1" |
| 12–20 | U | "B2" + mũi tên đỏ |
| 20–26 | U | Kết quả, có khung đỏ khoanh vùng |
| 26–30 | Selfie | "Follow để xem thêm" |

**60s:**
- 0–5: selfie + claim.
- 5–10: bằng chứng (ảnh chụp kết quả, C12).
- 10–50: các bước B1–B4, mỗi bước 8–12s.
- 50–55: kết quả cuối.
- 55–60: selfie + CTA / câu hỏi.

Giữ khoảng 10–15 khoảng ngừng tự nhiên mỗi phút. Nhạc nền nhỏ hoặc không có.

**90s:** giống bản 60s, nhưng thêm bước B5–B6 và một đoạn "lỗi thường gặp" (khung đỏ, chữ đỏ) ở giây 60–75.

---

## 6. Tự đo lại video của mình (để so với bảng số liệu)

- **Điểm cắt:**
  ```
  ffmpeg -i out.mp4 -vf "scale=192:-2,select='gte(scene,0.3)',showinfo" -f null - 2>&1 | grep pts_time
  ```
  Đếm số dòng rồi chia cho số phút.
- **Loudness:**
  ```
  ffmpeg -i out.mp4 -af ebur128 -f null -
  ```
  Đọc giá trị `I:` (mục tiêu khoảng −14) và `LRA`.
- **Khoảng ngừng:**
  ```
  ffmpeg -i out.mp4 -af silencedetect=n=-35dB:d=0.25 -f null -
  ```
- **Phân tích đầy đủ (giống 80 video mẫu):**
  ```
  /workspace/.cv-venv/bin/python /workspace/video-learn/tools/analyze.py out.mp4
  ```
  Lệnh này sinh ra `out_breakdown.md`.

---

## 7. Checklist QA trước khi xuất

### Hook
- [ ] Ở frame 0 đã có hình chủ thể, có caption, và có text hook (2 dòng, 3–5 chữ). Text hook hiện xong trước giây 1,0–2,0.
- [ ] Tắt tiếng xem 1s đầu vẫn đoán được chủ đề (D1).
- [ ] Cắt đầu tiên: tin nóng ≤1,6s; listicle ≤3,6s; hướng dẫn selfie thì giữ 4–6s.

### Nhịp
- [ ] Shot trung vị đúng mục tiêu theo dạng nội dung: tin nóng 1,6–2,0s; lệnh → kết quả 1–5s; hướng dẫn 4–12s.
- [ ] Tin nóng: không còn khoảng ngừng ≥0,25s, trừ các chỗ cố ý ngắt nhạc.
- [ ] Talking head không đứng yên quá 10s. Có punch hoặc đổi layout mỗi 6–10s, và push chậm 2–3%/s.
- [ ] Mỗi lần punch-in, mắt giữ đúng vị trí.

### Caption
- [ ] 1–2 chữ/cụm (hướng dẫn tối đa 4–5). Mỗi cụm 12–27 frame. Animation vào ≤6 frame.
- [ ] Mỗi câu tối đa 1 từ màu nhấn. Màu nhấn thống nhất cả kênh.
- [ ] Chữ tiếng Việt đủ dấu, font không lỗi dấu.
- [ ] Vị trí caption: y≈980–1060 khi split; y≈1190–1400 khi full khung.
- [ ] Không có chữ nào lọt vào y<150, y>1590, hoặc x>940.

### Đồ hoạ
- [ ] Mọi graphic đều có animation vào hoặc sfx đi kèm (D7).
- [ ] Mũi tên hoặc khung đỏ chỉ đúng chỗ cần nhìn.
- [ ] PIP không che UI quan trọng.

### Âm thanh
- [ ] Nhạc thấp hơn giọng 18–22 dB.
- [ ] Sfx ở khoảng 15–25% điểm cắt, ưu tiên đổi layout và chữ to. Hook có 1–2 sfx.
- [ ] Ngắt nhạc trước câu reveal.
- [ ] Mức xuất khoảng −14 LUFS, true peak ≤ −1 dBTP.

### Kết
- [ ] Có CTA (FOLLOW, comment từ khoá, câu hỏi) hoặc loop câu cuối nối câu đầu.
- [ ] Cắt sạch hơi thở cuối.

### Kỹ thuật
- [ ] Khung 1080×1920, 30fps.
- [ ] Chạy `analyze.py` trên bản xuất và so với bảng số liệu ở Mục 1.

---

## 8. Hạn chế của số liệu

**Nguồn video:**
- Video Douyin và Facebook là bản thay thế (YouTube hoặc TikTok), vì Douyin cần cookie và không liệt kê được reel trên Facebook.
- 秋芝 là bản 16:9, nên số liệu bố cục của kênh này không áp trực tiếp cho video dọc.

**Bộ phân loại bố cục (heuristic: Haar face + đường chia ngang):**
- Hay nhầm POV của Riley thành split.
- Nhầm lẫn PIP với split ở NTK.
- Số % chỉ nên dùng để so tương đối.

**OCR:**
- Mất dấu tiếng Việt.
- Màu chữ lấy bằng k-means bị viền, bóng và nén làm lệch, nên hex sai khoảng ±10–15 mỗi kênh màu.
- Số chữ mỗi cụm ở Hiếu, HungNPV, 秋芝 và 鱼皮 bị chữ UI làm nhiễu.
- Thời lượng cụm caption ở độ chính xác frame (10fps) mới đo được trên 1 video (Kallaway 7645, cửa sổ 20s). Lô đo 2 video mỗi kênh bị gián đoạn, chưa chạy.

**Âm thanh:**
- "Sfx" chỉ là ứng viên suy ra từ năng lượng tần cao, không phân biệt được với tiếng phím, nhấn giọng hay hi-hat.
- Không chạy whisper (tiết kiệm RAM), nên không có transcript.
- LUFS đo trên file tải về đã bị nền tảng nén lại.

**Animation:** số frame của animation (trừ thời lượng cụm caption và lộ chữ tiêu đề) lấy từ quan sát contact sheet hoặc bản xem kỹ cộng với D7, chưa đo từng frame.

---

## 9. PHẦN BỔ SUNG 03/10/2026 — 8 kênh mới (43 video)

> Cùng công cụ đo (`analyze.py`, `sheet.py`, `footage_stats.py`, `edit_agg.py`). Lần này **có chạy whisper** (faster-whisper small, CPU) → số liệu lời thoại xem `SO-TAY-KICH-BAN.md`; footage xem `DAN-CHUNG-FOOTAGE.md`; công thức chốt xem `CONG-THUC-HINTON.md`.
> Follower lấy lúc ~21:20 ICT 03/10/2026 (HTML TikTok / yt-dlp `channel_follower_count`). "Top" = view cao nhất trong 60–200 video gần nhất mà listing trả về; phần lớn lọc ≤150s.

### 9.1 Danh sách kênh mới
| Kênh | Link | Follower | Ngôn ngữ / dạng | Video đã tải (view cao nhất) |
|---|---|---|---|---|
| Duy Luân Dễ Thương | https://www.tiktok.com/@duyluandethuong | 1,2M (TikTok, tích xanh); YT 500K | VN, tech + AI (cầm máy, hướng dẫn) | 5 (3,9M — "30s nói nhanh về iPhone Duo") |
| Đình Hán AI | https://www.tiktok.com/@dinhhanai | 149,4K | VN, hướng dẫn tool AI | 5 (4,8M — "biến bạn thành ca sĩ") |
| Lê Duy Hiệp – AI Hub | https://www.tiktok.com/@leduyhiep.aihub | 41,6K | VN, mẹo AI 20–40s | 5 (210K) |
| Varun Mayya | https://www.youtube.com/@VarunMayya | 1,17M sub (IG ~1,2M theo bên thứ ba) | EN (Ấn Độ), tin AI/tech | 6 (874K — vắc-xin cho chó bằng ChatGPT) |
| Jeff Su | https://www.youtube.com/@JeffSu | 1,91M sub | EN, năng suất + AI | 6 (6,6M — resume hack) |
| Tommy Teja | https://www.tiktok.com/@tommythings | 1,3M | Indonesia, tech/AI/nghề | 5 (886K) |
| Adam.Digital | https://www.tiktok.com/@adam.digital | 541,5K | EN, tool AI (Runway, MiniMax…) | 5 (2,7M — Runway Agent) |
| Brand Nat | https://www.tiktok.com/@brandnat | 447K | EN (Úc), AI cho doanh nghiệp, có quảng cáo | 5 (1,5M — Vanta) |

### 9.2 Bảng số liệu dựng (trung vị theo kênh) [ĐO]
| Kênh | n | Dài (s) | Cắt/phút (ngưỡng 0,3) | Shot trung vị (s) | Cắt đầu (s) | Chữ/cụm caption | y caption (px/1920) | Cao chữ (px) | Push-in/video | LUFS | BGM % [SUY] | Mặt % thời lượng |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Varun Mayya | 6 | 53,6 | **26,9** | **1,52** | 1,39 | 3 | 1098 | 52 | 4 | −14,0 | 97 | **24** |
| Tommy Teja | 5 | 49,6 | 12,7 | 4,0 | 4,6 | 3 | 972 | 48 | 2 | −12,0 | 72 | 83 |
| Adam.Digital | 5 | 43,0 | 11,2 | 4,8 | 9,0 | 4 | 1138 | 38 | 2 | −13,1 | 81 | 46 |
| Brand Nat | 5 | 69,9 | 6,6 | 4,6 | 6,0 | 4 | 958 | 52 | 4 | −13,5 | 59 | 62 |
| Đình Hán AI | 5 | 71,3 | 6,5 | 6,4 | 5,3 | 5 | 920 | 45 | 1 | −16,1 | 21 | 50 |
| Jeff Su | 6 | 51,2 | 5,4 | 14,4 | 4,1 | 4 | 921 | 57 | 1 | −16,3 | 59 | 29 |
| Lê Duy Hiệp | 5 | 32,9 | ~0* | 24,3* | 18,4* | 3,3 | 1091 | 59 | 0 | −13,3 | 97 | — |
| Duy Luân | 5 | 37,6 | ~0* | 36,3* | 1,2 | 1 | 848 | 60 | 0 | −21,7 | 92 | — |
So sánh kênh cũ (cùng công cụ): Kallaway 24,3 cắt/phút · shot 1,68s · mặt 94% · BGM 94%; Hiếu 3,2 · 10,6s · 81%; HungNPV 3,0 · 13,6s · 15%; AI Savvy 2,5 · 19,5s · 87%.
\* Ngưỡng scene 0,3 không bắt được cắt vì video là 1 cảnh liền + chữ/sticker đè (Lê Duy Hiệp: talking head + bullet; Duy Luân: cầm máy quay liền) hoặc đổi cảnh bằng zoom; xem contact sheet.

### 9.3 Thông số phong cách từng kênh mới [KHUNG + ĐO]
**Varun Mayya** — *mẫu gốc của CONG-THUC-HINTON*. Mặt chỉ ~24% thời lượng (đầu, giữa, cuối); còn lại full khung: ảnh chụp tweet có handle (hook), bài báo/blog có câu tô đỏ, README/GitHub, lưới logo, chart chính thức, card nền tối chữ trắng serif ("Zero MEDICAL", "27 YEAR OLD"), stock minh hoạ đúng nghĩa đen câu VO. Caption **3 chữ/cụm**, trắng, nhỏ (cao ~52px), đặt quanh y≈880–1100. Cắt cứng ~1,5s, push-in chậm 3–5%/s trên ảnh tĩnh (4 đoạn/video), punch 1,07×. Nhạc nền liên tục, giọng −14 LUFS.
**Jeff Su** — hook mặt + **chữ 2 dòng to viền đậm** ("A VERY / UNETHICAL", trắng + cam). Ảnh tài liệu full khung với **zoom punch liên tục** thay cho cắt (shot dài 14,4s nhưng bên trong có 4–5 lần zoom), PIP mặt chữ nhật góc phải dưới, glitch RGB chuyển cảnh, highlight đỏ trên câu trả lời AI, meme kết.
**Adam.Digital** — **kết quả trước** (clip AI 0–4s), rồi split kết quả trên/mặt dưới, rồi screen record full với caption **1 từ trong hộp đen** ở y≈1138 (thấp), kết quả trình bày trong khung app có prompt bên dưới, kết bằng **bong bóng comment giả** chứa từ khoá CTA.
**Brand Nat** — talking head trong studio sáng + **đạo cụ vật lý** (Lego) làm ẩn dụ, caption 1 từ trắng **trộn serif nghiêng** ("*one*", "*whatever*"), pill tiêu đề tím ở hook, website quay trên màn hình thật, logo khách hàng pop cạnh người.
**Tommy Teja** — 1 cảnh talking head cố định, **tiêu đề trắng cố định trên đầu** ("Kerjaan Yang Mungkin Dapat 1M/tahun"), **tier list lấp dần nửa dưới** làm vòng mở suốt 49s, caption nhỏ 3 chữ, từ khoá đổi màu vàng/đỏ.
**Đình Hán AI** — mở bằng kết quả AI (avatar clone/giọng hát), sau đó screen record web tool full khung, **mũi tên vàng + vòng click vàng**, caption to 5 chữ/cụm có highlight xanh lá; nhạc nền thấp (21%).
**Lê Duy Hiệp – AI Hub** — talking head + dải tiêu đề vàng trên + bullet chữ tích dần; cuối là **slide checklist tĩnh ~1s/slide** (kiểu "lưu lại"), chuyển cảnh lục giác, nền trang trí theo mùa (Tết). Nhạc nền gần như liên tục (97%).
**Duy Luân Dễ Thương** — tự quay cầm thiết bị tại sự kiện (Apple Park), chữ tiêu đề "Trên tay …", 1 cảnh liền; video hướng dẫn = screen record phóng to + PIP mặt bo vuông góc dưới trái. Video AI của kênh thường dài (Claude Cowork 178s).

### 9.4 5 phát hiện dựng từ kênh mới
1. **Kênh không lộ mặt nhiều nhất cũng là kênh cắt nhanh nhất**: Varun 26,9 cắt/phút, shot 1,52s, mặt 24% — gần với Kallaway (24,3 cắt/phút, 1,68s) nhưng không phụ thuộc người dẫn → khớp Hinton.
2. **Caption ngắn là chuẩn chung**: 6/8 kênh mới 3–4 chữ/cụm (Varun 3, Tommy 3, Adam/Jeff/Brand Nat 4), Duy Luân 1; kênh cũ Kallaway 2, Hiếu 11,5 (ngoại lệ dài).
3. **"Zoom thay cắt"**: Jeff Su shot trung vị 14,4s nhưng ảnh tài liệu được zoom punch 4–5 lần/đoạn; Varun push-in 3–5%/s trên ảnh tĩnh → ảnh chụp tĩnh vẫn có nhịp nếu zoom mỗi 1,5–3s.
4. **Nhạc nền phổ biến nhưng không bắt buộc để có view**: BGM 59–97% ở 6/8 kênh mới, nhưng Đình Hán (21%) có video 4,8M view; AI Savvy kênh cũ 33%. → Mặc định "không BGM" của Hinton không phải rào cản lớn nếu nhịp hình đủ nhanh [SUY].
5. **Âm lượng**: LUFS trung vị kênh mới −12,0 đến −16,3 (bỏ Duy Luân −21,7), khớp chuẩn Hinton loudnorm ~−14.
