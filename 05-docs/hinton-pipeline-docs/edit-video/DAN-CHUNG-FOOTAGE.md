# DẪN CHỨNG & FOOTAGE — cách các kênh chèn footage và quy trình lấy clip cho Hinton

> Viết 03/10/2026 (ICT). Dùng để học nội bộ, không reup video mẫu.
> Nhãn số liệu: **[ĐO]** = đo tự động trên frame/analysis.json (nhãn bố cục heuristic, có sai số); **[KHUNG]** = xem contact sheet bằng mắt; **[SUY]** = suy luận.
> Script hỗ trợ: `/workspace/video-learn/tools/fx/` (phone_frame.py, news_card.py, bar_chart.py) + các công thức ffmpeg ở mục 4 (đã chạy thử trên box).

## 0. 5 PHÁT HIỆN CHÍNH VỀ FOOTAGE

1. **Kênh tin AI đổi footage cực nhanh, kênh hướng dẫn thì chậm**: Varun **35 lần chèn/phút** (trung vị 1,4s/lần), Kallaway 21,4 (1,6s), NTK 17,3 (1,5s), Adam 13,0 (4,0s) — so với HungNPV 3,0 (17,6s), Riley 4,0 (6,6s), AI Savvy 4,8 (7,6s), Jeff Su 6,2 (12,9s) [ĐO]. Hinton tin AI 60s → mục tiêu ≥20–28 lần đổi hình.
2. **Loại footage số 1 cho tin AI là ảnh chụp tài liệu chính thức** (blog hãng, tweet, bài báo, paper) **có highlight đúng câu đang đọc**: Varun lNTubupxkEM dùng tweet Greg Brockman (1,2s), bài UNSW (3s), bài The Australian (3s), trang AlphaFold (1,2s); Varun R2nesxy7uYU tô đỏ câu trên blog red.anthropic.com; Kallaway 7645 chèn ảnh chụp tiêu đề blog OpenAI đúng câu bẻ lái ở ~6s [KHUNG]. Ảnh tĩnh + zoom = dễ render local nhất.
3. **Footage có mặt ngay trong hook ở 9/13 kênh đo được** (% thời lượng 0–3s là footage ≥80%: Varun 91,5 · Kallaway 100 · AI Savvy 100 · NTK 100 · 鱼皮 100 · Riley 100 · Hiếu 100 · Adam 83 · Đình Hán 83). Ngoại lệ mở bằng mặt: 秋芝 (footage đầu ở 5s), Jeff Su 25%, HungNPV 17%, Brand Nat 0% [ĐO; bỏ Duy Luân/Lê Duy Hiệp/Tommy vì nhãn heuristic sai].
4. **Kênh không cần mặt dùng full khung, kênh "mặt là thương hiệu" dùng split/PIP**: full khung chiếm Varun 76%, 鱼皮 74%, HungNPV 85%, Jeff Su 71% thời lượng; còn Kallaway chỉ 6%, Riley 8,5%, AI Savvy 13% (phần còn lại là split mặt + footage) [ĐO]. → Hinton (không mặt): full khung + card chữ; không cần làm split.
5. **"Kết quả trước" là footage mạnh nhất cho video công cụ; khi không có footage, chữ/bảng động vẫn chạy**: Đình Hán 4,8M view mở bằng demo giọng hát AI 0–24s; Adam 2,7M mở bằng clip quảng cáo AI 0–4s; NTK/AI Savvy mở bằng clip mẫu do tool tạo. Tommy Teja (886K view) chỉ có 1 cảnh 49s + tier list lấp dần; Lê Duy Hiệp dùng slide checklist ~1s/slide → fallback F1/F10/F12 là hợp lệ [KHUNG].

---

## 1. SỐ LIỆU FOOTAGE THEO KÊNH [ĐO]

`footage %` = % thời lượng là footage (split có B-roll, PIP, màn hình UI, B-roll full, card nền tối) theo nhãn bố cục heuristic 2 fps (`tools/footage_stats.py`). `full %` = footage chiếm full khung. `hook / 3–15s` = % thời lượng đoạn đó là footage. `chèn/phút` và `trung vị/lần` = số lần footage xuất hiện & thời lượng mỗi lần.

| Kênh | n | footage % | full % | footage đầu | hook 0–3s % | 3–15s % | chèn/phút | trung vị/lần |
|---|---|---|---|---|---|---|---|---|
| Varun Mayya | 6 | 89 | 76 | 0,0s | 91,5 | 88 | **35,0** | **1,4s** |
| Kallaway | 10 | 70 | 6 | 0,0s | 100 | 75 | 21,4 | 1,6s |
| Nguyễn Tất Kiểm | 10 | 68 | 33,5 | 0,0s | 100 | 64,5 | 17,3 | 1,5s |
| Adam.Digital | 5 | 89 | 54 | 0,0s | 83 | 96 | 13,0 | 4,0s |
| 程序员鱼皮 | 10 | 85 | 74 | 0,0s | 100 | 87,5 | 9,6 | 3,6s |
| Hiếu AI | 10 | 98 | 19 | 0,0s | 100 | 100 | 9,3 | 3,5s |
| 秋芝2046 | 10 | 61 | 36 | 5,0s | 0 | 58 | 8,6 | 2,6s |
| Đình Hán AI | 5 | 72 | 50 | 0,5s | 83 | 50 | 6,5 | 5,5s |
| Jeff Su | 6 | 87,5 | 71 | 1,8s | 25 | 94 | 6,2 | 12,9s |
| Brand Nat | 5 | 38 | 38 | 6,0s | 0 | 21 | 5,7 | 3,1s |
| AI Savvy | 10 | 100 | 13 | 0,0s | 100 | 100 | 4,8 | 7,6s |
| Riley Brown | 10 | 99 | 8,5 | 0,0s | 100 | 100 | 4,0 | 6,6s |
| HungNPV | 10 | 92 | 85 | 0,8s | 17 | 79 | 3,0 | 17,6s |
| Tommy Teja* | 3 | 52 | 17 | 0,0s | 100 | 75 | 7,4 | 2,5s |
| Lê Duy Hiệp* | 5 | 88 | 0 | 0,0s | 100 | 100 | 3,1 | 15,4s |
| Duy Luân* | 5 | 96 | 47 | 0,0s | 100 | 92 | 1,7 | 36,3s |

\* Nhãn sai: Tommy = tier list đè lên mặt bị tính là footage; Lê Duy Hiệp = dải tiêu đề + bullet; Duy Luân = selfie cầm thiết bị bị tính là B-roll. Dùng phần [KHUNG] ở mục 2 cho 3 kênh này.

---

## 2. CATALOG CÁC LẦN CHÈN TIÊU BIỂU [KHUNG + ĐO mốc giây]

Loại: **CLIP-CT** clip demo chính thức (site/X/YouTube launch) · **SR** screen record · **CHỤP** ảnh chụp tin/tweet/blog/tài liệu · **CHART** · **STOCK** · **AI** clip/ảnh do AI tạo (kết quả tool) · **MEME** · **CARD** card chữ/đồ hoạ tự làm · **TỰ QUAY** · **LOGO**.
Khung: FULL · SPLIT (trên/dưới) · PIP · MOCKUP-ĐT (điện thoại) · TRÌNH DUYỆT · CARD.

| Kênh / video | t (s) | Loại | Vị trí kịch bản | Thời lượng | Khung | Ghi chú |
|---|---|---|---|---|---|---|
| Varun lNTubupxkEM | 1,2–2,3 | CHỤP tweet (Greg Brockman @gdb) | Hook (chứng minh claim) | 1,1s | FULL | Có handle + avatar → tăng tin cậy |
| Varun lNTubupxkEM | 5,0–6,3 | CARD "Zero MEDICAL" | Hook vế 2 ("The crazy part?") | 1,3s | CARD tối | Push-in 4,7%/s |
| Varun lNTubupxkEM | 8,9–11,9 | CHỤP bài báo UNSW | Bằng chứng (bối cảnh) | 3,0s | SPLIT không mặt | Ngày tháng hiện rõ |
| Varun lNTubupxkEM | 19,8–22,8 | CHỤP báo The Australian | Bằng chứng | 3,0s | SPLIT không mặt | Câu trích "holy crap, it worked" |
| Varun lNTubupxkEM | 28,7–32,4 | SR (PyMOL/AlphaFold UI) | Demo cơ chế | ~3,7s | FULL | Pull-out chậm |
| Varun lNTubupxkEM | 44,6–45,9 | CHỤP khung chat ChatGPT | Bằng chứng cuối | 1,3s | FULL | — |
| Varun R2nesxy7uYU | 0,0–1,5 | LOGO Claude Mythos | Hook | 1,5s | SPLIT (trên logo, dưới mặt) | — |
| Varun R2nesxy7uYU | ~11 | CARD lưới logo AWS/Apple/Google/Microsoft/Nvidia… | Bối cảnh | ~3s | CARD tối | Logo đối tác chính thức |
| Varun R2nesxy7uYU | ~14 | STOCK code chạy | Bằng chứng ("fix their code") | ~2s | FULL | — |
| Varun R2nesxy7uYU | 16–19, 33–44 | CHỤP blog red.anthropic.com tô đỏ câu | Bằng chứng | 3–8s | FULL / SPLIT 2 khung | Highlight đúng câu VO |
| Varun R2nesxy7uYU | ~27 | CARD động "27 YEAR OLD" lưới ô đỏ | Con số | ~3s | CARD tối | Đồ hoạ tự làm |
| Varun R2nesxy7uYU | ~47 | STOCK người ăn sandwich | Minh hoạ giai thoại | ~1,5s | FULL | Stock đúng nghĩa đen câu VO |
| Varun R2nesxy7uYU | 49–55 | CHART benchmark chính thức | Bằng chứng | ~5s | FULL | Thanh trắng vs gạch chéo |
| Varun R2nesxy7uYU | ~58 | CHỤP tweet @AnthropicAI | Kết | ~2s | FULL | — |
| Kallaway 7645299083573267742 | ~6 | CHỤP tiêu đề blog OpenAI | Bẻ lái ("but this moment") | ~1,5s | SPLIT (trên) | Đúng câu bẻ lái |
| Kallaway 7645… | 10–30 | STOCK bảng đen, coder, robot cờ vua; CARD lưới chấm/đồ thị | Bối cảnh | 1–2s/shot | SPLIT | Motion graphic tự làm |
| Kallaway 7645… | ~34 | Clip phim (Good Will Hunting) | Minh hoạ "sáng tạo" | ~1,5s | SPLIT | — |
| Kallaway 7630160402457939230 | 6–40 | CHỤP trang sản phẩm/UI Codex chính thức | Tính năng 1–3 | 1–3s/shot | SPLIT (trên UI, dưới mặt) | Đổi ảnh mỗi câu |
| Jeff Su QwwS7PxYpzo | 3,4–20 | CHỤP tài liệu (resume) + zoom punch tới câu ẩn chữ đỏ | Giải thích mẹo | ~17s, 4–5 lần zoom | FULL + PIP mặt chữ nhật góc phải | Zoom thay cho cắt |
| Jeff Su QwwS7PxYpzo | ~26,8 | Glitch RGB chuyển cảnh | Chuyển "mình đã thử" | 0,2s | FULL | — |
| Jeff Su QwwS7PxYpzo | 36–47 | SR Google Bard, câu trả lời tô đỏ | Bằng chứng thử nghiệm | ~11s | FULL | Highlight kết quả |
| Jeff Su QwwS7PxYpzo | ~50 | MEME "Doubt" (X) | Kết | ~1s | Đè lên mặt | — |
| Adam 7677763689885519125 | 0–4 | AI (clip quảng cáo do Runway tạo) | Hook = kết quả | 4s | FULL | Output tool trước |
| Adam 7677… | 6–20 | SR Runway Agent, caption 1 từ trong hộp đen | Demo các bước | 14s (cắt 2s/lần) | FULL | — |
| Adam 7677… | 20–28 | AI kết quả "Final Video" + prompt bên dưới | Bằng chứng | 2s/kết quả | FULL (khung app) | — |
| Adam 7677… | ~30 | Mặt + bong bóng comment giả "RUNWAY" | CTA | 2s | FULL | CTA dạng hình |
| Brand Nat 7680530870259698964 | 0–8 | TỰ QUAY đạo cụ Lego (tên lửa, tiền) | Hook ẩn dụ | 4s | FULL | Pill tiêu đề tím |
| Brand Nat 7680… | 30–48 | SR website Vanta (có lúc quay màn hình bằng máy) | Demo | ~18s | FULL | — |
| Brand Nat 7680… | ~61 | LOGO Atlassian/Supabase/Harvey pop | Bằng chứng xã hội | ~2s | Đè cạnh người | — |
| Tommy 7679412987274218753 | 0–49 | CARD tier list lấp dần | Toàn bài (vòng mở) | 49s, đổi trạng thái mỗi ~3s | Nửa dưới, tiêu đề cố định trên | Không có footage ngoài |
| 秋芝 DvQcsdvIMiE | ~5 trở đi | CLIP-CT livestream ra mắt OpenAI | Bằng chứng | 2–3s | FULL/PIP | Footage đầu ở 5s |
| 秋芝 DvQcsdvIMiE | — | CHART từ blog chính thức; CHỤP trang giá | Bằng chứng | 2–3s | FULL | — |
| 秋芝 DvQcsdvIMiE | — | Glitch color bar SMPTE; MEME "太慢" (quá chậm) + ảnh động vật | Chuyển ý / phản ứng | 0,3–1s | FULL | — |
| 鱼皮 kFMPdjOU5eM | — | CHỤP bài đăng/chart; SR terminal & web | Bối cảnh / demo | 3–4s | FULL + PIP mặt trái dưới | — |
| AI Savvy Seedance (7672308029345271061) | 0–3 | AI kết quả trước/sau | Hook | 3s | SPLIT + dải tiêu đề đen | — |
| AI Savvy Seedance | — | SR Runway có khung đỏ; CLIP-CT promo + pill "LINK IN BIO" | Demo / kết | 5–8s | SPLIT | — |
| NTK (nhiều video) | 0–3 | AI clip mẫu | Hook | 2–3s | FULL | — |
| NTK | — | SR điện thoại + mũi tên đỏ; TỰ QUAY sự kiện/khoá học; nút "ĐĂNG KÝ NGAY" | Bước / CTA | 1–2s | FULL | — |
| Riley (nhiều video) | — | SR + MOCKUP điện thoại app vừa build | Demo | 5–7s | MOCKUP-ĐT, mặt dưới | — |
| HungNPV | — | Quay màn hình laptop bằng điện thoại, ngón tay chỉ, chấm click vàng | Demo | ~17s/lần | FULL | Selfie đầu/cuối |
| Hiếu AI | 0–3 | AI video kết quả "video bên cạnh mình" | Hook | 3s | SPLIT (mặt + kết quả) | — |
| Đình Hán 7461257650701978887 | 0–24 | AI (giọng hát/avatar clone) | Hook = kết quả | ~24s | FULL | 4,8M view |
| Đình Hán | 30–70 | SR web tool, mũi tên vàng + vòng click vàng | Các bước | 5–7s | FULL | Caption to highlight xanh lá |
| Lê Duy Hiệp 7595412800491539733 | ~10–19 | CARD slide checklist 6 bước | Kết "lưu lại" | ~1s/slide | CARD | Nền trang trí Tết, chuyển lục giác |
| Duy Luân 7683605021639904520 | 0–36 | TỰ QUAY cầm thiết bị (Apple Park) | Toàn bài | 36s | FULL | Chữ "Trên tay iPhone Duo" |


---

## 3. QUY TRÌNH LẤY FOOTAGE (thực dụng)

### 3.0 Nguyên tắc chọn (rút từ catalog)
1. **Key visual trước, viết lời sau** (Kallaway): tìm được 1 clip "nhìn là hiểu" cho hook thì mới chốt câu hook. Không có thì dùng hook chữ + ảnh chụp tin (fallback F1/F2).
2. **Mỗi claim → 1 bằng chứng trong ≤1 giây**: câu "OpenAI vừa ra mắt…" phải đi kèm ảnh chụp tiêu đề blog/tweet chính thức ngay lúc đọc tên sản phẩm (Kallaway 7645 chèn ảnh chụp blog đúng câu "but this moment" ở ~6s; Varun mở bằng ảnh chụp tweet có handle).
3. **Kết quả trước, cách làm sau**: video tool/hướng dẫn mở bằng output đẹp nhất (Adam.Digital: clip quảng cáo nước hoa AI 0–4s rồi mới vào UI; Đình Hán: avatar AI clone; NTK: clip mẫu AI).
4. **Nhịp thay footage**: tin AI 1,5–3,5s/lần (Kallaway trung vị 1,6s, NTK 1,5s, 秋芝 2,6s, 鱼皮 3,6s [ĐO]); demo/hướng dẫn 5–8s/lần (AI Savvy 7,6s, Riley 6,6s [ĐO]).
5. **Khung**: tin AI → split trên/dưới (footage trên, VO/caption dưới) hoặc full; screen record dài → full + PIP mặt (không có mặt thì bỏ PIP, dùng khung trình duyệt/zoom); app mobile → mockup điện thoại.

### 3.1 Dạng "TIN AI" (Hinton tự viết, VO giọng nam)
| Bước | Việc | Lấy ở đâu | Lệnh |
|---|---|---|---|
| 1 | Xác định 3–5 "khoảnh khắc nhìn được" của tin: demo chính, 1 con số/benchmark, giá/ngày ra mắt, phản ứng cộng đồng | Bài blog chính thức | — |
| 2 | **Clip demo chính thức** | (a) X chính thức: @OpenAI @AnthropicAI @GoogleDeepMind @GeminiApp @xai @MetaAI @Alibaba_Qwen @deepseek_ai @Kimi_Moonshot @MiniMax__AI @runwayml @pika_labs @LumaLabsAI; (b) YouTube kênh hãng (livestream/launch video); (c) blog/product page (thường nhúng mp4 trực tiếp) | `yt-dlp -f "bv*[height<=1080]+ba/b" --merge-output-format mp4 -o "raw/%(id)s.%(ext)s" URL` ; chỉ lấy đoạn: thêm `--download-sections "*0:12-0:20"` |
| 3 | **Ảnh chụp tiêu đề tin / tweet** (dẫn chứng) | Blog hãng, tweet CEO (Sam Altman, Demis Hassabis, Dario Amodei…), The Verge/TechCrunch | Chụp trang: `google-chrome --headless=new --no-sandbox --hide-scrollbars --window-size=1080,1350 --screenshot=shot.png URL` (đã test trên box). Ảnh trong tweet: `gallery-dl URL` |
| 4 | **Chart/benchmark** | Blog hãng, model card Hugging Face, paper arXiv (Figure 1) | Chụp vùng chart (chrome headless hoặc crop ảnh). Không có ảnh đẹp → tự vẽ `bar_chart.py` (F7) |
| 5 | **Demo cộng đồng** (khi hãng chỉ có text) | Search X: `"<tên model>" filter:videos` sắp theo Top; Reddit r/singularity, r/LocalLLaMA; GitHub README (gif/mp4 trong `user-attachments`); Product Hunt (video gallery) | `yt-dlp URL_tweet` / `gallery-dl URL_reddit` / tải asset GitHub bằng `curl -L -o demo.mp4 <link asset>` |
| 6 | **Tự quay màn hình thử tool** (bằng chứng mạnh nhất, "mình đã thử") | Máy local | OBS/QuickTime → crop 1080 rộng |
| 7 | **Stock lấp chỗ** (khái niệm trừu tượng: "việc làm", "chip", "data center") | Pexels / Pixabay / Mixkit (chọn dọc) | Pexels API (cần key miễn phí): `curl -H "Authorization: $PEXELS_KEY" "https://api.pexels.com/videos/search?query=data%20center&orientation=portrait&per_page=5"` |
| 8 | **Chuẩn hoá** về 30fps, không tiếng, đúng khung | — | Split nửa trên: `ffmpeg -ss 12 -t 3 -i raw.mp4 -vf "scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960,fps=30" -an -c:v libx264 -crf 18 -pix_fmt yuv420p clip_top.mp4` ; Full dọc: thay `1080:960` → `1080:1920` (clip ngang thì dùng nền mờ, xem F9) |
| 9 | Đặt tên theo beat: `b01_hook_demo.mp4`, `b02_proof_blog.png`, `b03_chart.mp4`… để map với timeline kịch bản | — | — |

**Thứ tự ưu tiên khi chọn clip cho 1 câu:** clip demo chính thức > tự quay thử > demo cộng đồng > ảnh chụp tin/tweet có zoom > chart tự vẽ > stock > chữ động.
**Ghi nguồn tối giản:** 1 dòng chữ nhỏ góc dưới "Nguồn: OpenAI" / "@handle" khi dùng clip/ảnh của bên khác — vừa tăng độ tin, vừa đủ thực dụng (không đi sâu bản quyền ở đây).

### 3.2 Dạng "DOUYIN DỊCH LẠI"
| Bước | Việc | Ghi chú |
|---|---|---|
| 1 | Tải video gốc (đã có pipeline Hinton) + tách scene: `ffmpeg -i src.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 \| grep pts_time` | Lấy danh sách mốc cắt cảnh |
| 2 | Phân loại scene gốc: (a) footage trung tính (demo, chart, UI) → **giữ**; (b) mặt người dẫn TQ, chữ Hán cứng, logo/QR/watermark kênh → **thay/che** | Không giữ CTA/handle kênh TQ (không quảng bá kênh TQ) |
| 3 | Với mỗi demo trong video gốc, **tìm bản gốc chất lượng cao**: tên sản phẩm (OCR chữ Hán → dịch) → X/YouTube/GitHub chính thức; sản phẩm TQ: trang chủ hãng, Bilibili chính thức, WeChat article (chụp màn hình) | Bản gốc thường nét hơn và không dính phụ đề Hán |
| 4 | Che chữ Hán còn sót: `delogo=x=..:y=..:w=..:h=..` hoặc phủ dải tiêu đề/caption Việt lên đúng vùng; crop bỏ vùng phụ đề dưới | Ưu tiên phủ dải tiêu đề Hinton đè lên thay vì blur |
| 5 | Scene người dẫn → thay bằng: ảnh chụp tin (F2), chữ động (F1), mockup (F5) hoặc giữ ngắn ≤1s nếu là phản ứng | 秋芝 dùng PIP tròn góc dưới trái cho mặt — Hinton không có mặt nên thay bằng icon/logo tròn hoặc bỏ |
| 6 | Meme/phản ứng (kiểu "太慢" + ảnh động vật của 秋芝): thay bằng meme Việt quen thuộc hoặc sticker chữ "Chậm thật sự 🐢" | 0,5–1s, đúng câu chê/khen |

### 3.3 Mẹo tải nhanh
- Xem trước danh sách định dạng: `yt-dlp -F URL`. Chỉ tải 8 giây cần: `--download-sections "*1:05-1:13" --force-keyframes-at-cuts`.
- X/Twitter công khai: `yt-dlp URL` thường chạy; nếu bị chặn → quay màn hình lại đoạn đó (không dùng cookie/tài khoản để vượt).
- Ảnh hàng loạt (tweet nhiều ảnh, Reddit gallery): `/workspace/.gallerydl-venv/bin/gallery-dl -d raw/ URL`.
- Clip nhúng trong trang web: thử `yt-dlp URL_trang` (generic extractor) trước; không được thì mở DevTools → Network → lọc `mp4`.
- GIF trên GitHub → mp4: `ffmpeg -i demo.gif -movflags +faststart -pix_fmt yuv420p -vf "scale=1080:-2:flags=lanczos,fps=30" demo.mp4`.

---

## 4. FALLBACK KHI KHÔNG CÓ FOOTAGE

Đã chạy thử trên box (file mẫu `/tmp/fx`). Kích thước mặc định nửa trên split = **1080×960**; full = 1080×1920.

| # | Kỹ thuật | Khi dùng | ffmpeg / script | CapCut |
|---|---|---|---|---|
| F1 | **Chữ động (kinetic typography)** — 1 từ/số khóa pop 80→108→100% | Con số "gấp 2 lần", "miễn phí", tên model | `drawtext=fontfile='…/BeVietnamPro-Bold.ttf':text='MIỄN PHÍ':fontcolor=0xF5C518:x=(w-tw)/2:y=(h-th)/2:fontsize='100*if(lt(t,0.1),0.8+2.8*t,if(lt(t,0.27),1.08-0.47*(t-0.1),1))'` | Text → Animation In "Pop/Nảy" 0,3s; tô vàng từ khoá |
| F2 | **Zoom ảnh chụp tin (Ken Burns)** | Có ảnh chụp blog/tweet nhưng không có clip | `-loop 1 -i shot.png -vf "scale=2160:-2,zoompan=z='min(1+0.0015*on,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=90:s=1080x960:fps=30" -t 3` | Keyframe Scale 100%→112% trong 3s |
| F3 | **Zoom vào vùng + khung highlight** | Chỉ vào đúng dòng "price: $0", con số benchmark | zoompan nội suy z 1→2 và x/y về tâm vùng: `z='1+on/45':x='(X0-iw/zoom/2)*min(on/45,1)'…` + `drawbox=x=..:y=..:w=..:h=..:color=red@0.9:t=8` | Keyframe zoom + sticker khung đỏ / mũi tên (kiểu NTK, Đình Hán) |
| F4 | **Thẻ tin dựng lại** (news card) | Ảnh chụp xấu/khó đọc, tin tiếng Anh/Trung cần Việt hoá | `python3 tools/fx/news_card.py` → PNG 1080×960 (nguồn, tiêu đề Việt, ngày) rồi F2 | Template "news headline" |
| F5 | **Mockup điện thoại / khung trình duyệt** | Ảnh chụp app mobile / web tĩnh | Điện thoại: `python3 tools/fx/phone_frame.py` → overlay screen 780×1690 tại (150,115). Trình duyệt: `pad=w=iw+40:h=ih+110:x=20:y=90:color=0x1e1e1e,drawbox=x=0:y=0:w=iw:h=70:color=0x2b2b2b:t=fill` + 3 chấm `drawbox` đỏ/vàng/xanh | Sticker "phone frame"/"browser" |
| F6 | **Glitch chuyển cảnh** 6 khung (0,2s) | Đúng câu bẻ lái "Nhưng…", tin "nóng" | `rgbashift=rh=-12:bh=12:enable='between(t,1,1.2)',noise=alls=40:allf=t:enable='between(t,1,1.2)'` | Effects → "Glitch"/"Lỗi tín hiệu", 0,2s (Jeff Su dùng glitch RGB ở ~27s; 秋芝 dùng color bar) |
| F7 | **Chart tự vẽ động** | Có số liệu nhưng không có chart đẹp | `python3 tools/fx/bar_chart.py out.mp4 "Điểm SWE-bench (%)" "GPT-6:78.2,Claude:74.5,Gemini:71" "%"` → 3s, cột mọc 0,8s, cột thắng màu vàng | Template chart / keyframe scale Y |
| F8 | **Lưới logo/icon** | "So với ChatGPT, Gemini, Claude…", "5 công cụ" | Overlay logo PNG lần lượt `enable='gte(t,0.3*N)'` + pop scale | Sticker logo pop lần lượt (Brand Nat pop logo Atlassian/Supabase/Harvey cạnh người) |
| F9 | **Clip ngang → dọc nền mờ** | Clip 16:9 chính thức | `-filter_complex "[0]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30[bg];[0]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2"` | Canvas → Blur |
| F10 | **Bảng xếp hạng/tier list lấp dần** | Video "N công cụ", so sánh | Vẽ PNG từng trạng thái (Pillow) → concat theo mốc VO | Tommy Teja giữ nguyên 1 cảnh 49s, chỉ có tier list lấp dần ở nửa dưới làm "vòng mở" [KHUNG] |
| F11 | **Ảnh AI minh hoạ** (khái niệm trừu tượng) | "AI thay thế việc làm", "siêu trí tuệ" | Tạo ảnh 1080×960 → F2 Ken Burns | Ghi nhỏ "Ảnh minh hoạ AI" |
| F12 | **Checklist/slide "lưu lại"** | Kết video hướng dẫn | Slide nền tối, mỗi dòng hiện 1 nhịp | Lê Duy Hiệp: slide 6 bước, mỗi slide ~1s [KHUNG] |

**Quy tắc fallback:** không để 1 hình tĩnh đứng >3s không chuyển động (zoom/pop/đổi khung); cứ 2–3 hình tĩnh thì xen 1 clip động thật hoặc F6/F7.
