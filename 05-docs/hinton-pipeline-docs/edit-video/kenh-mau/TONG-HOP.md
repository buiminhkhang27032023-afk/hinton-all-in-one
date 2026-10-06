# TỔNG HỢP: kênh mẫu tương tự "Cường Mê AI" (@caocuongvuai)

Lấy dữ liệu ngày 03/10/2026, khoảng 16:40–17:30 ICT. Trọng tâm: **cách dựng và bố cục**, không phải chủ đề hay số liệu.
Video tải về chỉ để học nội bộ, **không reup**. Không chạy whisper, nên mọi nhận định về nhạc/sfx đều là [SUY LUẬN].

## Bảng so sánh
| Nền tảng | Kênh | URL | Followers (nguồn) | Thời lượng trung vị | Ngách | Bài học dựng chính |
|---|---|---|---|---|---|---|
| TikTok VN | HungNPV | https://www.tiktok.com/@hungnpv | 487.100 (HTML TikTok, đã kiểm chứng) | 1:57 | AI văn phòng | Selfie kèm ô chữ trắng nêu claim ngay frame 0; nhãn bước B1/B2 và chấm click |
| TikTok VN | Hiếu AI | https://www.tiktok.com/@hieuanca | 213.800 (HTML TikTok, đã kiểm chứng) | 1:21 | Tạo video/ảnh AI, lệnh ChatGPT | Chia đôi: UI/kết quả ở trên, mặt ở dưới; pill lime ghi lệnh; hiệu ứng gõ prompt ở giây 0 |
| TikTok quốc tế | Kallaway | https://www.tiktok.com/@kanekallaway | 444.600 (HTML TikTok, đã kiểm chứng) | 1:23 | Tin AI/tech | B-roll ở trên đổi mỗi 0,5–1s, mặt ở dưới; caption 1–3 chữ ở đường nối; punch-in kèm 1 chữ to |
| TikTok quốc tế | Riley Brown | https://www.tiktok.com/@rileybrown.ai | 637.100 (HTML TikTok, đã kiểm chứng) | 1:55 | Vibe coding, agent | Ô tiêu đề đen kèm emoji trong 10s đầu; screen ở trên, người ở dưới, nhịp chậm |
| Douyin | 秋芝2046 | Douyin: chưa lấy được (ID 32571643812); YT: https://www.youtube.com/channel/UCrC3GjeSkxXgJ2hLQ2D-m4w | 155,9万 (Feigua, bên thứ ba, ngày không rõ); 113,6万 (8dy.cn) | chưa lấy được (YT: ~13,5 phút) | Review công cụ AI | Chip tag tiêu đề phần lime; PIP tròn trên screen record; ghép mặt vào B-roll AI; end card logo |
| Douyin | 程序员鱼皮 | https://www.douyin.com/user/MS4wLjABAAAAkGPUlxhANi-quQ-g2HAFIHVArZmHUNeyutqfY_bKvS0 | ~49,4万 (HeiYou, bên thứ ba) | chưa lấy được (YT dài ~8,6 phút) | AI coding | Caption Trung rất to giữa màn hình, cụm khoá đổi màu; ảnh chụp chat/log làm bằng chứng; kết bằng câu hỏi |
| Facebook VN | Nguyễn Tất Kiểm | https://www.facebook.com/nguyentatkiem | 540.190 (og:description FB) | chưa lấy được | AI marketing | Listicle: card đen lưới phối cảnh + logo + số thứ tự; nút FOLLOW động kèm con trỏ tay |
| Facebook quốc tế | AI Savvy | https://www.facebook.com/aisavvy | 115.173 (og:description FB); TikTok 131.300 | chưa lấy được (TikTok 1:17) | Demo video AI | Hook so sánh trước/sau chồng dọc kèm nhãn; caption 1 chữ cam; pill "LINK IN BIO" |

Hồ sơ chi tiết từng kênh: `tiktokvn-hungnpv.md`, `tiktokvn-hieuanca.md`, `tiktokintl-kanekallaway.md`, `tiktokintl-rileybrown.md`, `douyin-qiuzhi2046.md`, `douyin-chengxuyuanyupi.md`, `facebook-nguyentatkiem.md`, `facebook-aisavvy.md`.
Dữ liệu thô: `raw/*.jsonl`. Ảnh cover: `covers/`. Video và frame: `/workspace/video-learn/` (danh mục ở `/workspace/video-learn/INDEX.md`).

### Nhịp cắt đo được
Số cảnh tính bằng ffmpeg scene ở ngưỡng 0,12. Cách đo này đếm thiếu jump cut trên talking head tĩnh và cắt bên trong một nửa màn hình chia đôi.

| Kênh | Shot trung bình (2 video) |
|---|---|
| Nguyễn Tất Kiểm | 1,1s / 0,7s |
| Kallaway | 1,1s / 2,5s |
| 鱼皮 | 1,7s (short) / 9,3s (ngang) |
| 秋芝 | 2,1s / 5,3s |
| Hiếu AI | 2,9s / 2,9s |
| HungNPV | 11,5s / 7,9s |
| Riley | 9,6s / 9,4s |
| AI Savvy | khoảng 10–11s |

---

## Bố cục nên học (công thức cho editor bot)
Mỗi công thức đều dựa trên frame [QUAN SÁT] ở kênh mẫu ghi kèm. Thông số px tính cho khung 1080×1920.

### C1. Chia đôi "B-roll trên, mặt dưới" (Kallaway, Riley, Hiếu AI, AI Savvy)
- Nửa trên (y 0–960): B-roll, screen record hoặc ảnh UI. Nửa dưới (y 960–1920): talking head crop từ ngực trở lên, mắt nằm ở khoảng 1/3 trên của nửa dưới.
- Caption ở ngay đường nối (y khoảng 900–1000): cụm 1–3 chữ, chạy theo từng cụm.
  - Cách 1: sans đậm trắng viền đen.
  - Cách 2: serif đậm cam/vàng như Kallaway.
- Bản tin tức đổi B-roll nửa trên mỗi 0,5–1,5s. Bản hướng dẫn giữ screen record liên tục.

### C2. Punch-in mặt toàn màn hình kèm MỘT CHỮ TO (Kallaway)
- Khoảng mỗi 5–10s, thoát chia đôi sang mặt toàn màn hình (scale 1,1–1,2), kèm 1 từ khoá to ở giữa (sans trắng phát sáng, cỡ khoảng 140–180px).
- Cho phép đổi font theo nghĩa của từ (font pixel cho "CODING", script cho "creative").
- [SUY LUẬN] Ghép sfx whoosh/hit.

### C3. Thanh tiêu đề hoặc ô tiêu đề trong 3–10s đầu (Kallaway, Riley)
- Kallaway: thanh 2 màu (đỏ/đen) chữ in hoa trắng, đặt ngay trên đường nối, slide-in từ phải trong khoảng 0,25–1s.
- Riley: ô đen bo góc 24px, chữ trắng đậm 2 dòng kèm 2–3 emoji, đặt giữa nửa trên, giữ khoảng 10s.

### C4. Hook selfie kèm ô claim trắng (HungNPV)
- Frame 0: mặt sát camera, cử chỉ mạnh (tay lên môi hoặc chỉ tay), ô trắng bo góc chữ đen đậm 2–3 dòng ở giữa khung, nội dung theo mẫu "Đừng … nữa, dùng … này".
- Không cắt trong 3s đầu.

### C5. Pill lệnh/prompt (Hiếu AI)
- Pill nền lime #C6F432 (gần đúng), chữ đen đậm, đặt ở đường nối, ghi đúng lệnh hoặc tên tính năng.
- Nửa trên có animation gõ từng ký tự vào ô prompt, bắt đầu ngay t=0.

### C6. PIP mặt tròn trên screen record (Kallaway, 秋芝; 鱼皮 dùng PIP chữ nhật)
- Screen record toàn khung. Mặt trong vòng tròn đường kính khoảng 25–30% chiều rộng, đặt ở góc trái dưới (秋芝) hoặc trái trên (Kallaway).
- Dùng cho đoạn demo dài để không mất "người dẫn". Biến thể: avatar hoạt hình 3D của chính mình (Hiếu AI).

### C7. Nhãn bước và đánh dấu click (HungNPV, Hiếu AI, AI Savvy, NTK)
- Nhãn bước dạng ô trắng nhỏ "B1: …", "B2: …" ở mép trên vùng UI.
- Đánh dấu thao tác bằng một trong các cách: chấm vàng ở điểm click; vòng tròn hoặc mũi tên đỏ; khung chữ nhật đỏ quanh vùng chọn; kính lúp zoom vào UI.

### C8. Chip tag tiêu đề phần (秋芝)
- Chip lime ở góc trái trên ghi tên phần ("Khả năng code", "So sánh kết quả"), giữ suốt phần đó.
- Danh sách tag pop-in lần lượt cạnh mặt khi liệt kê.

### C9. Card listicle "N công cụ" (Nguyễn Tất Kiểm)
- Card nền đen có lưới phối cảnh toả tia. Logo app vuông bo góc ở giữa (khoảng 40% chiều rộng). Tiêu đề số thứ tự xanh lá nhỏ phía trên ("3. Minimax"), caption vàng phía dưới.
- Mỗi card khoảng 1–2s, theo sau là 1–2 clip demo toàn màn hình.

### C10. So sánh trước/sau chồng dọc (AI Savvy)
- Hai clip 16:9 xếp chồng trong 9:16, nền đen.
- Nhãn nhỏ cam ngay trên mỗi clip ("Gốc", "Sau AI"). Tiêu đề trắng đậm nghiêng ở dải đen trên cùng.
- Dùng làm hook 0–30s cho mọi video về công cụ video/ảnh AI.

### C11. Caption "to giữa màn hình, đổi màu theo nghĩa" (鱼皮, Hiếu AI)
- Caption 2–6 chữ, rất to, ở giữa hoặc giữa–dưới. Trắng viền đen.
- Từ khoá vàng = giải pháp/điểm nhấn. Đỏ = vấn đề/lỗi.

### C12. Bằng chứng thật (鱼皮)
- Chèn ảnh chụp chat, comment, log lỗi hoặc tweet (khung đỏ khoanh vùng như Riley) ngay sau hook để tăng độ tin.

### C13. Outro/CTA
Chọn 1 trong các mẫu:
- (a) Nút FOLLOW/ĐĂNG KÝ động kèm con trỏ tay bấm (NTK).
- (b) Overlay CTA comment-keyword giữa video, "CMT 'ASMR'" (Hiếu AI).
- (c) Câu hỏi mở cuối video (鱼皮).
- (d) Pill "LINK IN BIO"/"Link ở bình luận ghim" (AI Savvy).
- (e) End card logo nền đen (秋芝).
- (f) Selfie kèm ô trắng "Follow để xem thêm" (HungNPV).

### C14. Chuyển cảnh
- Gần như mọi kênh đều dùng hard cut. Hiệu ứng chỉ dùng điểm xuyết:
  - Whip/zoom blur trong 0,5s đầu (NTK).
  - Glitch sọc màu giữa các phần (秋芝).
  - Punch-in zoom (Kallaway).
- Khuyến nghị cho bot: mặc định hard cut, tối đa 1–2 hiệu ứng mỗi video.

### Gợi ý ghép template theo dạng nội dung (dành cho Cường Mê AI)
- **Tin AI nóng (45–80s):** C3 Kallaway + C1 (B-roll đổi 0,5–1,5s) + C2 mỗi 5–10s + caption ở đường nối + C13(c) hoặc (f).
- **Hướng dẫn công cụ (1,5–2,5 phút):** C4 hook + C7 + C6 hoặc C1 bản screen record + C13(b).
- **Top N công cụ:** C9 + C14 whip ở hook + C13(a).
- **Demo video/ảnh AI:** C10 hook + C1 với caption 1 chữ + C13(d).
- **Prompt/lệnh hay:** C5 + C11.

---

## Chưa kiểm chứng / hạn chế
- **Douyin:** yt-dlp bị chặn ("Fresh cookies are needed"), nên không tải hay liệt kê được video Douyin.
  - Follower Douyin của cả 2 kênh chỉ có từ bên thứ ba (Feigua, 8dy.cn, HeiYou), không rõ ngày snapshot.
  - URL Douyin của 秋芝2046: chưa lấy được.
  - Video học là bản YouTube cross-post (top view trong khoảng 40 video gần nhất ≤5 phút), không phải top Douyin.
- **Facebook:** không liệt kê được reel của page, nên top-by-views FB và thời lượng trung vị FB đều chưa lấy được.
  - NTK: 1 reel FB thật + 1 YouTube Short proxy (reel FB thứ 2 bị lỗi "Cannot parse data").
  - AI Savvy: 2 video TikTok proxy.
  - Follower FB lấy từ og:description, chưa đối chiếu với trang khi đăng nhập.
- **Nhạc/sfx:** không phân tích audio và không chạy whisper, nên tất cả nhận định đều là [SUY LUẬN].
- **Nhịp cắt:** scene detect đếm thiếu jump cut trên talking head tĩnh, nên các con số chỉ mang tính tương đối.
- **Độ phân giải:** video TikTok tải về ở 576×1024 (TikTok trả bản đó), đủ để xem bố cục nhưng font nhỏ có thể khó đọc.

---

## Bài học từ diễn đàn (bổ sung 03/10/2026, ngoài C1–C14)
Nguồn chi tiết: `/workspace/hinton-pipeline-docs/edit-video/dien-dan/DIEN-DAN.md`.
Ký hiệu nguồn:
- [RD] = Reddit (đọc qua index)
- [KW] = Kallaway (YouTube/Skool)
- [LEO] = Learn By Leo
- [JO] = Joseph | Video Editing
- [HH] = Herman Huang
- [PD] = Phong Dvc
- [TCN] = Trung Công Nghệ
- [QUA] = Quạ HD
- [DY] = trang Douyin 剪辑教程

### D1. Hook 4 lớp đồng bộ + kiểm tra khi tắt tiếng [KW][RD]
- Lời nói, key visual, text hook và âm thanh phải cùng chỉ vào MỘT chủ thể.
- Ngoài caption, luôn có 1 text hook (tiêu đề 3–5 chữ) trong 2s đầu.
- Bot tự kiểm: xem 1s đầu khi tắt tiếng; nếu không đoán được chủ đề thì làm lại.

### D2. Key visual + mũi tên xác nhận [KW]
- Thứ tự người xem tiếp nhận là hình → nghe → nhìn lại hình. Ngay sau câu nói chính, phải có hình minh hoạ đúng câu đó.
- Thêm nhãn chữ ngắn và mũi tên chỉ thẳng vào chủ thể ("Đây là …").
- Nếu không có key visual cho hook thì cân nhắc bỏ ý tưởng.

### D3. Mở bằng kết quả 0,5–1,5s [RD]
- Đặt khoảnh khắc kết quả hoặc cao trào (ví dụ ảnh/video AI đã tạo xong) lên đầu, rồi cắt về đầu quy trình.
- Không zoom chậm và không có khoảng lặng ở frame 0.

### D4. Bố cục "visual stun" mới [KW][QUA]
- (a) Người nói ở nửa dưới, khoảng trống phía trên làm canvas chiếu B-roll.
- (b) Hai thanh đen trên/dưới khép dần trong 1–2s đầu.
- (c) Người đã tách nền có viền trắng dày (stroke 8–12px), đặt trên nền ảnh hoặc video.
- (d) Chữ hoặc graphic nằm SAU lưng người nói (roto/auto cutout).

### D5. Cắt giữ điểm nhìn [LEO][RD]
- Ở frame cuối clip A và frame đầu clip B, mắt hoặc điểm chú ý phải nằm cùng vị trí trên màn hình.
- Khi punch-in, keyframe cả Position để mắt không nhảy.
- Zoom ≤5% để "giấu" jump cut bị chê là nửa vời. Hoặc punch hẳn (115–130%), hoặc cắt đúng lúc người nói có cử động lớn.

### D6. Hai kiểu zoom có vai trò khác nhau [LEO][KW]
- Punch-in nhanh (hard cut sang 115–130%) đúng lúc claim được nói ra.
- Push-in chậm 100→112% kéo dài suốt một câu khi giữ một shot dài.
- Thay đổi tỉ lệ khung khoảng mỗi 3–5s để tạo cảm giác nhiều máy quay.
- Nếu có 2 góc máy thật, dùng multicam (剪映 新建多机位片段, căn theo âm thanh) và chuyển góc thật [DY].

### D7. Không graphic nào "tự hiện ra" [LEO][RD][PD]
Mọi chữ, icon hay ảnh phải xuất hiện theo một trong các cách sau:
- Trượt vào: khoảng 15 frame, ease-out cubic, kèm opacity 0→100.
- Pop: scale 0→110→100% trong 5–8 frame.
- Fade/zoom in 0,4–0,6s.
- Hiện ngay nhưng kèm sfx shutter/pop "giải thích" sự xuất hiện.
- Tránh preset kiểu bounce.

### D8. Dẫn mắt trên ảnh chụp màn hình [LEO]
- Làm tối hoặc blur vùng xung quanh điểm cần xem, cho điểm đó glow nhẹ.
- Đổi hue theo nghĩa: đỏ = sai/xấu, vàng-xanh = đúng/tốt.
- Bổ sung cho vòng/khung đỏ ở C7.

### D9. Quy tắc caption [RD][LEO]
- Mỗi lần 2–3 chữ. Không nháy từng chữ quá nhanh, không để cả câu dài.
- Mỗi câu highlight tối đa 1 từ.
- Ngắt theo nghĩa, không theo số ký tự.
- Caption chỉ là lớp phụ: khi có graphic minh hoạ mạnh thì có thể ẩn caption để tránh rối.
- Vùng an toàn cho khung 1080×1920 (theo công cụ safe-zone, nguồn phụ):
  - tránh khoảng 150px trên, 330px dưới, 140px bên phải;
  - caption đặt khoảng 47–69% chiều cao.

### D10. Quy trình sound design 3 bước [JO][RD][PD]
1. Whoosh cho mọi chuyển động hoặc zoom: zoom nhỏ dùng whoosh nhẹ, zoom ra khỏi khung dùng whoosh gắt.
2. Sfx có "chất liệu" cho từng graphic:
   - UI click cho mỗi icon;
   - "ping" khi zoom-in;
   - "tick" khi chữ hiện;
   - shutter cho light sweep;
   - tiếng máy tính tiền cho chữ về tiền;
   - kính vỡ cho hiệu ứng shatter.
3. Nhạc nền.

Quy tắc cho hook 3s:
- Chỉ 2–3 sự kiện âm. Một âm chính, lớp phụ thấp hơn 8–10 dB.
- Dựng câm trước, chỉ thêm âm ở chỗ hình có nhịp.
- Nửa giây im lặng trước câu chính.

### D11. Riser / hit / drone và thao tác nhạc [LEO][HH]
- Riser chỉ đặt trước điều thật sự quan trọng (nếu lạm dụng sẽ mất tác dụng). Hit để "chốt". Drone cho đoạn bí ẩn.
- Thao tác nhạc:
  - tắt nhạc đột ngột để nhấn một câu;
  - fade nhạc để báo sắp hết một đoạn;
  - khớp đoạn nhạc lên cao trào với lúc chuyển từ vấn đề sang giải pháp.
- Xếp lớp sfx theo dải tần (trầm + trung + cao). Khoét dải mid của nhạc bằng EQ để giọng nằm gọn.
- Dùng MỘT bộ sfx cùng phong cách cho cả kênh.

### D12. Chuẩn kỹ thuật âm thanh [PD][Mean Tính]
- Chuẩn hoá giọng theo preset nền tảng (Normalize Audio).
- Đặt tên track Voice / SFX / Ambient / Music.
- Crossfade giữa các đoạn thoại.
- Theo dõi meter để không vượt 0 dB khi chồng nhiều lớp.

### D13. Kết thúc thành vòng lặp + nhạc thêm trong app [RD]
- Cắt sạch hơi thở cuối. Câu hoặc khung cuối nối liền vào câu hoặc khung đầu.
- Với TikTok: xuất thêm một bản "sạch nhạc" để gắn nhạc trending trong app (lấy metadata).
- A/B giữa caption burn-in và caption in-app.

### D14. Quy trình dựng theo transcript [PD][RD]
- Tạo phụ đề hoặc transcript trước, tối đa 1 từ/dòng để căn timing.
- Đánh dấu ý tưởng edit theo mốc thời gian.
- Dựng template chữ (2 tầng: thường + nhấn) một lần rồi copy cho cả video.
- Đây cũng là cách editor bot nên làm: transcript → danh sách beat → gán template C/D.

### D15. Hiệu ứng nhấn chữ nhỏ mà hiệu quả [PD][JO]
- Chữ nhấp nháy: opacity 0/1 xen kẽ ở frame 0–3.
- Rung nhẹ (camera shake với cường độ thấp) cho cụm từ khoá.
- Light sweep chạy qua chữ.
- Chữ nhấn dùng gradient (đỏ→cam hoặc xanh) + glow nhẹ.
- Icon bay vào lệch nhau từng cái.
- "Match move": icon bay đúng vào vị trí logo của cảnh kế tiếp, tạo chuyển cảnh liền mạch.

### D16. Đừng cắt nhanh chỉ để nhanh [LEO]
- Chọn nhịp theo trải nghiệm người xem muốn:
  - tin nóng: nhanh, như C1–C2;
  - chia sẻ, tâm sự, hướng dẫn: chậm hơn, giữ cảm giác thật.
- Giữ một shot 10s nếu nó đáng xem.
- Ảnh tĩnh luôn có chuyển động chậm: scale, position hoặc perspective.
- Talking head tĩnh quá 10–15s thì chèn một "pattern interrupt" (graphic, B-roll, đổi khung).

### D17. Hook 3 câu tiếng Việt cho kịch bản (để editor biết chỗ nhấn) [TCN][KW]
- Cấu trúc: bối cảnh + tò mò → từ tương phản ("nhưng", "thế mà") → bẻ lái.
- Editor đặt punch-in và sfx impact ĐÚNG vào từ tương phản.
- Từ khoá chủ đề hiện bằng chữ to ngay frame 0.

Hạn chế:
- Nhiều nguồn Trung Quốc (B站, 知乎, 小红书) và nhóm Facebook VN không mở được.
- Các bài học ở trên chủ yếu đến từ Reddit (qua index), YouTube (transcript đã đọc) và Douyin (một trang).
- Số dB, frame hay px là theo lời người hướng dẫn hoặc nguồn phụ, chưa tự đo.


## Sổ tay dựng chi tiết (vòng 4, 80 video)
Xem `/workspace/hinton-pipeline-docs/edit-video/SO-TAY-DUNG.md`: thông số đo được theo kênh, C1–C14/D1–D17 đã chỉnh theo số đo, khung 30/60/90s, checklist QA.
