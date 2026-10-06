# CÔNG THỨC HINTON — 1 mẫu gốc + 12 món "cherry-pick" từ 15 kênh

> Viết 03/10/2026 (ICT). Tổng hợp từ `SO-TAY-KICH-BAN.md`, `SO-TAY-DUNG.md`, `DAN-CHUNG-FOOTAGE.md`.
> Bối cảnh Hinton: tin/công cụ AI tiếng Việt **60s**, **không lộ mặt**, giọng nam OmniVoice clone v2 tốc độ 1.2 (≈4,2–4,5 âm tiết/s → **250–270 âm tiết**), render **local** (HyperFrames 8–12 scene, ffmpeg fallback), mặc định **không karaoke burn, không BGM** (`playbook-san-xuat.md`).
> Nhãn: [ĐO] đo tự động · [ĐO-TR] đo trên transcript · [KHUNG] xem contact sheet · [SUY] suy luận.

---

## 1. MẪU GỐC: Varun Mayya — "Claude Mythos Is Finally Here — But Not For You"

- Link: https://www.youtube.com/shorts/R2nesxy7uYU (kênh https://www.youtube.com/@VarunMayya, 1,17M sub)
- File học nội bộ: `/workspace/video-learn/youtube-VarunMayya/R2nesxy7uYU.mp4` · contact sheet `R2nesxy7uYU_sheet.jpg` · breakdown `R2nesxy7uYU_breakdown.md`
- 693.485 view · 17.416 like · đăng 08/04/2026 · 64,3s.

### Vì sao chọn (bằng số)
| Tiêu chí Hinton | Varun R2nesxy7uYU | So với ứng viên khác |
|---|---|---|
| **Thể loại tin AI** | Tin model mới (Claude Mythos / Project Glasswing) — đúng loại tin Hinton làm hằng ngày | Kallaway 7645 cũng tin AI; Hiếu/NTK/HungNPV là hướng dẫn/công cụ |
| **Thời lượng ~60s** | 64,3s (kênh trung vị 53,6s) — trúng vùng 50–60s mà nghiên cứu 5.400 Shorts của Paddy Galloway cho là nhiều view nhất | Kallaway 7645 72,8s, kênh trung vị 93,6s; Hiếu 7686 41s |
| **Không cần mặt** | Mặt người chỉ xuất hiện **24%** thời lượng (mặt cận 13,2% + split mặt 8,5% + PIP 2,3%) [KHUNG]; trung vị kênh 24% — **thấp nhất** trong 12 kênh có người dẫn | Kallaway 94%, AI Savvy 87%, Hiếu 81%, Brand Nat 62% → bỏ mặt là vỡ format |
| **Dựng toàn bằng footage/dẫn chứng** | Kênh: footage 89% thời lượng, full khung 76%, **35 lần chèn/phút**, trung vị 1,4s/lần [ĐO]. Video này: split không mặt 42,6% + card nền tối 24% + UI 9,3% | Kallaway 21,4 lần/phút nhưng 94% có mặt trong khung; HungNPV 3 lần/phút |
| **Render local được** | 100% chất liệu là ảnh chụp blog Anthropic có highlight, chart benchmark chính thức, lưới logo đối tác, tweet @AnthropicAI, stock ngắn, card chữ → đều dựng lại được bằng ffmpeg/HyperFrames, không cần quay | Duy Luân/Brand Nat cần quay thật với thiết bị/đạo cụ |
| **Giọng kể = VO nam tin tức** | Ngôi thứ ba, **0 lần "you"/phút** [ĐO-TR]; 3 lần bẻ lái (0s "but", 6,1s "instead", 35,3s "but here's the wildest of all") | HungNPV 11,95 lần "bạn"/phút (giọng hướng dẫn) |
| **Nhịp cắt hợp spec Hinton "cut TB 1–3s"** | Shot trung vị 1,57s (ngưỡng 0,3) / 0,97s (ngưỡng 0,2); cắt đầu ở 1,53s [ĐO] | Hiếu 10,6s, HungNPV 13,6s, AI Savvy 19,5s/shot |
| **Mật độ thông tin** | 218 từ / 64s, 1 con số "neo" (lỗ hổng 27 năm), danh sách 5 hãng, chart | — |

**Điểm phải chỉnh khi đưa về Hinton:** Varun nói **5,91 âm tiết/s** (tiếng Anh) → bản Việt chỉ còn ~260 âm tiết, phải **bỏ ~25% ý** (không nói nhanh hơn). 24% thời lượng có mặt → thay bằng ảnh tiêu đề/kinetic text. Kênh có BGM ~97% thời lượng và caption 3 chữ/cụm → **xung đột mặc định Hinton** (mục 4).
Mẫu phụ cho dạng "câu chuyện người dùng AI": Varun lNTubupxkEM (874K view, 49s) — cùng ngữ pháp dựng.

---

## 2. BẢNG COMBO — phần hay → lấy từ kênh nào → cách áp dụng ở Hinton

| # | Phần hay | Lấy từ (video, số liệu) | Cách áp dụng ở Hinton |
|---|---|---|---|
| 1 | **Khung tổng + nhịp footage**: 1 câu VO = 1 hình dẫn chứng, đổi hình 1–2s, full khung | **Varun** R2nesxy7uYU (35 lần chèn/phút, 1,4s/lần, footage 89%) | Mỗi câu kịch bản gắn `[HÌNH: …]`; trong mỗi scene HyperFrames đổi 2–4 footage (xem mục 4 xung đột số scene) |
| 2 | **Ảnh chụp blog/tài liệu chính thức có highlight** (tô đỏ/vàng đúng câu đang đọc) | **Varun** (blog red.anthropic.com tô đỏ 16–44s) | Chrome headless chụp trang → crop → zoom vùng (F3) + drawbox tô vàng 40% đúng câu VO |
| 3 | **Hook claim + bẻ lái ở giây 5** ("…nhưng điều đáng nói không phải X") và câu "Cho tới bây giờ" | **Kallaway** 7645 (43,1M view; bẻ lái 5,3s – 10,8s – 29,5s – 38,4s) | Câu 1 ≤16 âm tiết xong trước 3,5s; câu 2 "Nhưng…" xong trước 6s; ≥2 lần bẻ lái nữa trong thân |
| 4 | **Kết không bán hàng: câu chốt vòng về hook / câu hỏi mở** | **Kallaway** 7645 (kết "…ngày AI biết sáng tạo", 0 CTA) + **Varun** lNTubupxkEM ("nếu làm được cho chó, sao không cho người?") | Câu cuối ≤14 âm tiết, cắt hình ngay sau chữ cuối (Jenny Hoyos: bỏ 1s cuối → retention 83→88%) |
| 5 | **Chữ hook to 2 dòng, 3–5 chữ, viền đậm, màu nhấn** ở 0–2s | **Jeff Su** QwwS7PxYpzo (6,6M; "A VERY / UNETHICAL" trắng + cam) | Chữ hook HyperFrames `frame-bold-poster`: 2 dòng, dòng 2 vàng #F5C518, chỉ là từ khoá, không chép câu VO |
| 6 | **Glitch RGB 0,2s đúng chữ "Nhưng"** | **Jeff Su** (~26,8s) + **秋芝** (color bar SMPTE) | F6: `rgbashift+noise` 6 khung; hoặc `frame-glitch-title`; tối đa 2 lần/video |
| 7 | **Kết quả/key visual trước, giải thích sau** | **Adam.Digital** 7677763689885519125 (2,7M; clip output 0–4s rồi mới vào UI) · **Đình Hán** 7461 (4,8M; demo giọng hát 0–24s) | 0–1,5s luôn là clip demo chính thức đẹp nhất của tin (không phải logo, không phải stock) |
| 8 | **"3 điểm" có báo trước + "thay vì làm bạn chán với benchmark"** | **AI Savvy** GPT-6 Astra (7681592962127580437; "the first one / the second / and the last one") | Thân 30s = 3 điểm × ~10s; báo trước số điểm ở giây 3–6 |
| 9 | **Clip livestream/launch chính thức + chart từ blog + meme 1s** | **秋芝** DvQcsdvIMiE (clip ra mắt OpenAI, chart chính thức, meme "太慢 = quá chậm") | Clip demo từ X/YouTube hãng (yt-dlp `--download-sections`); chart chính thức hoặc `bar_chart.py`; meme Việt ≤1s khi chê/khen |
| 10 | **Khung đỏ/mũi tên/chấm click vào đúng vùng UI** | **NTK** (mũi tên đỏ) · **Đình Hán** (mũi tên + vòng click vàng) | Mọi screen record/ảnh UI có 1 điểm nhấn: drawbox đỏ t=8 hoặc mũi tên PNG pop 0,2s |
| 11 | **Logo pop cạnh nội dung khi nhắc tên hãng** | **Brand Nat** 7680530870259698964 (logo Atlassian/Supabase/Harvey pop) · **Varun** (lưới logo AWS/Apple/Google…) | F8: khi VO đọc danh sách hãng, logo pop lần lượt 0,3s/logo |
| 12 | **CTA comment từ khoá** (tuỳ chọn) | **Adam** 5/5 video ("Comment RUNWAY…") · **Kallaway** 3/8 · **Hiếu** | Chỉ dùng cho dạng công cụ/hướng dẫn **khi có người gửi link**; tin AI dùng #4 |
| (+) | Mẫu câu lặp cho dạng N lệnh | **Hiếu** 7686 (1,2M; "Gõ /…, nó sẽ…" 5,4s/lệnh) | Dạng B trong SO-TAY-KICH-BAN 5.3 |
| (+) | Mockup điện thoại cho app mobile | **Riley** (mockup điện thoại) | `phone_frame.py` khi tin là app di động |
| (+) | Hook "Đừng… nữa / âm thầm" kiểu Việt | **HungNPV** ("Không phải tốn tiền trên những AI tạo 3D nữa…") | Dùng cho dạng công cụ miễn phí, không dùng cho tin model |

---

## 3. TEMPLATE 60s TỪNG GIÂY (kịch bản + dựng + footage/hiệu ứng)

Ngân sách: **260 âm tiết** @4,35 ât/s. Cột "Scene HF" = gợi ý map vào HyperFrames (10 scene).

| Giây | Kịch bản (âm tiết) | Hình / footage | Khung | Chữ trên màn | Hiệu ứng | Lấy từ |
|---|---|---|---|---|---|---|
| **0,0–1,5** | Hook vế 1: "[Hãng] vừa [động từ mạnh] [cái gì]" (~7) | Clip demo chính thức đẹp nhất (key visual) | Full 1080×1920 (clip ngang → nền mờ F9) | Chữ hook 2 dòng 3–5 chữ | Zoom 100→106%; VO bắt đầu ở khung 0 | Varun, Adam, Jeff Su · Scene 1 `frame-bold-poster` |
| **1,5–3,5** | Hook vế 2: hệ quả/nghịch lý "…nhưng/mạnh tới mức…" (~8) | Ảnh chụp tiêu đề blog/tweet chính thức của hãng | Full hoặc nửa trên split | Giữ chữ hook | Cắt cứng 1,5s (Varun cắt đầu 1,53s) | Varun, Kallaway |
| **3,5–6,0** | Bẻ lái: "Nhưng điều đáng nói không phải X, mà là Y." (~11) | Card chữ / chữ động từ khoá Y | Card nền tối | 1 từ khoá to (vàng) | **Glitch 0,2s ở chữ "Nhưng"** | Kallaway 5,3s, Jeff Su, 秋芝 · Scene 2 `frame-glitch-title` |
| **6–14** | Bối cảnh: là gì, ai làm, ra sao (~35) | 3 hình × ~2,6s: (1) blog chụp có highlight vàng đúng câu; (2) lưới logo đối tác pop; (3) clip demo | Full | Nhãn nguồn nhỏ "Nguồn: [hãng]" | Zoom vùng F3; logo pop F8 | Varun, Brand Nat · Scene 3 |
| **14–24** | Điểm 1 + 1 con số (~43): "Thứ nhất, …" | Clip demo #2 (3s) → chữ số pop (2s) → screen record có khung đỏ (3s) | Full / khung trình duyệt F5 | Con số to `frame-pentagram-stat` | Pop 80→108→100% (F1); khung đỏ/mũi tên | AI Savvy, NTK, Đình Hán · Scene 4–5 |
| **24–26** | "Nhưng đó chưa phải phần điên rồ nhất." (~9) | Card chữ / zoom nhanh | Card | 3–4 chữ | Punch-in 1,07× (Varun 1,069) | Varun 35,3s, Brand Nat 38s |
| **26–34** | Điểm 2 (~35) | Ảnh chụp tài liệu/tweet zoom + clip cộng đồng (X, Reddit, GitHub) | Full | Highlight vàng | Ken Burns F2 | Varun, 鱼皮 · Scene 6 |
| **34–44** | Điểm 3 = phần đáng nói nhất + benchmark (~43) | Chart chính thức (hoặc `bar_chart.py`, cột thắng vàng) → clip kết quả | Full | Số liệu trên chart | Cột mọc 0,8s | 秋芝, Varun 47–52s · Scene 7 `frame-aicoding-comparison` |
| **44–52** | Twist/hạn chế: "Nhưng có một vấn đề…" (giá, ai chưa dùng được, rủi ro) (~35) | Ảnh chụp trang giá/thông báo hạn chế, zoom vùng · meme ≤1s nếu hợp | Full | 1 từ khoá đỏ | Glitch lần 2 hoặc cắt cứng | Varun 55s, 秋芝 meme · Scene 8 |
| **52–57** | Ý nghĩa với người Việt (dùng ở VN được không, miễn phí không) — chỗ duy nhất dùng "bạn" (~22) | Mockup điện thoại/stock/AI minh hoạ Ken Burns | Mockup F5 | — | — | Riley, Brand Nat · Scene 9 |
| **57–60** | Kết: câu chốt vòng về hook HOẶC câu hỏi mở (~12–14). Dạng công cụ: comment từ khoá | Key visual ở 0s quay lại (loop) hoặc `frame-statement-outro` | Full | Câu hỏi 1 dòng | **Cắt ngay sau chữ cuối**, không end card dài | Kallaway 7645, Varun lNTub, Adam · Scene 10 |

**Tổng âm tiết:** 7+8+11+35+43+9+35+43+35+22+13 = **261**.
**Đếm hình:** ~24–28 lần đổi hình/60s (Varun 35/phút; Kallaway 21,4/phút) — tối thiểu 20.
**Âm thanh:** giọng loudnorm ~−14 LUFS (Varun kênh −13,95 LUFS — khớp).

### Ví dụ áp vào 1 tin (dàn ý, số lấy từ video Varun — kiểm chứng trước khi dùng)
0s *"Anthropic vừa làm ra AI mạnh nhất của họ"* → 1,5s *"nhưng mạnh tới mức không dám cho bạn dùng."* → 3,5s *"Điều đáng nói không phải sức mạnh, mà là thứ nó tìm ra."* → 6s Project Glasswing + logo AWS/Apple/Google/Microsoft/Nvidia → 14s "hàng nghìn lỗ hổng nghiêm trọng" + kỹ sư để chạy qua đêm → 24s "Nhưng đó chưa phải phần điên rồ nhất" → 26s lỗ hổng 27 năm trong OpenBSD → 34s thoát sandbox, gửi email cho nhà nghiên cứu + chart benchmark → 44s "vì thế Anthropic chỉ cho vài hãng lớn dùng" → 52s người dùng Việt khi nào được dùng → 57s *"Cho tới khi mọi phần mềm lớn đủ sức chống lại nó."*

---

## 4. XUNG ĐỘT VỚI MẶC ĐỊNH HINTON — cần coordinator hỏi user

| # | Mặc định Hinton hiện tại | Các kênh mẫu làm gì (số liệu) | Đề xuất / câu hỏi cho user |
|---|---|---|---|
| X1 | **Không karaoke burn-in**, chỉ sidecar `subtitle.srt` | **Cả 16 kênh đều có chữ burn-in** (caption hoặc chữ khoá): Varun 3 chữ/cụm, Kallaway 2 chữ/cụm, Hiếu ~11,5 chữ/cụm (OCR, mục SO-TAY-DUNG) | **Hỏi:** (a) giữ nguyên không burn, chỉ có chữ khoá kinetic (hook, con số, "Nhưng…") — không phải karaoke, đề xuất mặc định; (b) burn caption 2–3 chữ/cụm kiểu Varun (trắng, giữa màn); (c) karaoke từng chữ như hiện tại khi user yêu cầu |
| X2 | **Không BGM** trừ khi user đưa | BGM trung vị (% cửa sổ 1s có nền nhạc, ước tính): Varun 97%, Kallaway 94%, Hiếu 86%, Adam 81%, Tommy 72%, HungNPV 72%, Jeff Su 59%, Brand Nat 59%, AI Savvy 33%, Đình Hán 21% [SUY từ âm thanh] | **Hỏi:** (a) giữ không BGM; (b) user cung cấp 1–2 bản nhạc nền, đặt dưới giọng ~−20 dB; (c) không nhạc nhưng cho phép **SFX** whoosh/pop ở điểm cắt (Varun ~15 đỉnh nghi SFX/64s) |
| X3 | HyperFrames **8–12 scene** | Varun ~23–40 shot/64s; công thức cần ≥20 lần đổi hình | **Hỏi/kỹ thuật:** cho phép 1 scene chứa 2–4 footage (sub-cut), hoặc nâng lên 18–25 scene, hoặc ghép footage bằng ffmpeg rồi đưa vào scene như 1 video |
| X4 | Hook dùng `frame-liquid-bg-hero` / `frame-bold-poster` (template đồ hoạ) | Hook các kênh top là **clip demo thật/ảnh chụp tin thật** (Varun, Adam, Kallaway, Đình Hán) | Đề xuất: `frame-bold-poster` chỉ là lớp chữ đè lên clip demo thật; hỏi user có chấp nhận nền là footage của hãng không |
| X5 | Outro `frame-statement-outro` / `frame-logo-outro` | Video top kết **đột ngột**, không end card (Kallaway 7645, Varun) | Đề xuất: outro ≤1,5s hoặc bỏ logo outro; hỏi user có bắt buộc logo cuối không |
| X6 | (Chưa có quy định) Dùng clip/ảnh của hãng & cộng đồng | Mọi kênh tin AI đều chèn clip chính thức + ảnh chụp tweet/blog | Đề xuất ghi nguồn nhỏ "Nguồn: …"; hỏi user có OK dùng footage bên thứ ba ngắn (1–3s) không |
| X7 | (Chưa có) Meme / stock hài | 秋芝 meme, Varun stock "ăn sandwich", Jeff Su meme "Doubt" | Hỏi tông kênh: cho phép meme ≤1s không |
| X8 | (Chưa có) CTA comment từ khoá | Adam 5/5, Kallaway 3/8 | Chỉ bật nếu có người/bot trả link inbox; mặc định dùng kết câu hỏi |
| X9 | Tốc độ voice 1.2 cố định | Kênh EN 5,1–5,9 ât/s; VN 4,26–4,55 | Giữ 1.2 (khớp dải VN); dịch kịch bản EN phải cắt ý, không tăng tốc |
