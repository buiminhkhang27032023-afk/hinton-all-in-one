# SỔ TAY KỊCH BẢN — video AI ngắn (tin AI / công cụ / hướng dẫn / Douyin dịch lại)

> Viết 03/10/2026 (ICT) cho Hinton Media. Đi kèm `SO-TAY-DUNG.md` (dựng), `DAN-CHUNG-FOOTAGE.md` (footage), `CONG-THUC-HINTON.md` (công thức chốt).
> Dữ liệu: **16 kênh** (8 kênh cũ + 8 kênh mới), transcript faster-whisper small (CPU) → `script_analyze.py` → `script_agg.py`. Chỉ tính video có độ phủ lời ≥0,6 (87 video đạt).
> Nhãn: **[ĐO-TR]** = đo trên transcript tự động (whisper có lỗi chính tả, tên riêng sai; số đếm câu/âm tiết sai số ±10%); **[TRÍCH]** = câu trích, đã sửa lỗi nhận dạng rõ ràng và dịch Việt; **[GUIDE]** = từ guide công khai (link mục 10); **[SUY]** = suy luận.
> Đơn vị tốc độ: tiếng Việt/Indonesia = âm tiết; tiếng Anh = âm tiết ước tính (heuristic); tiếng Trung = số chữ Hán. "sps nói" = âm tiết/giây chỉ tính lúc đang nói (bỏ khoảng ngừng >0,6s).
> Script đếm âm tiết cho Hinton: `python3 /workspace/video-learn/tools/dem_am_tiet.py script.txt` (tên tiếng Anh tính theo âm đọc: ChatGPT = 4, AI = 2, OpenAI = 4…).

---

## 1. Bảng số liệu kịch bản theo kênh [ĐO-TR]

Trung vị trên các video đạt độ phủ ≥0,6. `hook3` = số từ (VN: âm tiết) nói trong 0–3s. `câu 1` = số từ câu đầu. `bẻ lái/phút` = số lần "but/nhưng/thực ra/但是…". `liệt kê` = số video có "thứ nhất/bước/number one…". `CTA cuối` = % video có từ khoá CTA trong 15% cuối. `số/phút` = con số được nói. `xưng hô/phút` = "bạn/các bạn/you".

| Kênh | Follower | n | Dài (s) | sps nói | Bắt đầu nói | hook3 | câu 1 | câu trung vị | bẻ lái/phút | liệt kê | CTA cuối | số/phút | xưng hô/phút |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Kallaway (EN) | 444,6K | 8 | 102 | 5,12 | 0,0s | 9 | 9 | 8,5 | 1,45 | 5/8 | 50% | 0,41 | 4,1 |
| Varun Mayya (EN) | 1,17M sub | 5 | 51 | 5,70 | 0,0s | 11 | 14 | 12 | 2,8 | 2/5 | 0% | 2,07 | 0,0 |
| Jeff Su (EN) | 1,91M sub | 5 | 52 | 4,61 | 0,0s | 9 | 10 | 9 | 1,05 | 4/5 | 0% | 0,0 | 5,0 |
| Adam.Digital (EN) | 541,5K | 5 | 43 | 4,71 | 0,0s | 12 | 16 | 9,5 | 0,68 | 4/5 | 60% | 2,79 | 3,4 |
| Brand Nat (EN) | 447K | 5 | 70 | 4,91 | 0,0s | 11 | 15 | 9 | 1,72 | 3/5 | 20% | 0,72 | 9,4 |
| AI Savvy (EN) | 115K FB | 8 | 87 | 4,38 | 0,0s | 8,5 | 11,5 | 8,5 | 2,4 | 7/8 | 0%* | 1,86 | 7,85 |
| Riley Brown (EN) | 637,1K | 4 | 119 | 3,77 | 0,0s | 11,5 | 10 | 5,5 | 2,02 | 4/4 | 25% | 0,77 | 0,65 |
| Hiếu AI (VN) | 213,8K | 9 | 77 | 4,53 | 0,0s | 12 | 15 | 11 | 0,0 | 6/9 | 22% | 4,14 | 6,2 |
| HungNPV (VN) | 487,1K | 6 | 120 | 4,26 | 0,0s | 11,5 | 18 | 12 | 0,0 | 6/6 | 17% | 2,33 | 11,95 |
| Nguyễn Tất Kiểm (VN) | 540K FB | 6 | 69 | 4,55 | 0,0s | 14 | 15,5 | 13 | 0,34 | 3/6 | 67% | 9,07 | 3,15 |
| Đình Hán AI (VN) | 149,4K | 3 | 61 | 3,60 | 0,0s | 15 | 16 | 9 | 0,0 | 3/3 | 0% | 0,0 | 5,5 |
| Lê Duy Hiệp (VN) | 41,6K | 1 | 34 | 4,60 | 2,5s | — | 10 | 13,5 | — | 1/1 | — | — | — |
| 秋芝2046 (ZH) | 155,9万 | 10 | 194 | 4,37 chữ | 0,0s | 11 chữ | 4,5 | 8,5 | 0,61 | 6/10 | 80%** | 0,58 | 1,55 |
| 程序员鱼皮 (ZH) | ~49,4万 | 6 | 97 | 3,43 chữ | 0,0s | 11 chữ | 9,5 | 9 | 0,0 | 3/6 | 17% | 0,2 | 1,3 |

\* AI Savvy kết bằng câu hỏi "Let me know if you have access…" — regex CTA không bắt "let me know" nên ghi 0%, thực tế 4/8 video kết bằng câu hỏi mời bình luận [TRÍCH]. \*\* 秋芝 kết bằng "下次见/关注" (hẹn gặp lại/theo dõi).
Không đủ dữ liệu: Duy Luân (nhạc nền to, video tech cầm máy, transcript hỏng), Tommy Teja (whisper tiếng Indonesia lỗi lặp), Lê Duy Hiệp (4/5 video gần như toàn nhạc + chữ). Xem mục 11 "Hạn chế".

---

## 2. 10 PHÁT HIỆN CHÍNH VỀ KỊCH BẢN

1. **Không kênh nào để im lặng ở đầu**: thời điểm bắt đầu nói trung vị = **0,0s** ở 13/14 kênh đo được. 3 giây đầu chứa **8,5–15 từ/âm tiết** (Kallaway 9, AI Savvy 8,5, VN 11,5–15). → Hinton: VO bắt đầu ở khung 0, 3s đầu ≈ 12–14 âm tiết. [ĐO-TR]
2. **Tốc độ nói tiếng Việt hội tụ 4,26–4,55 âm tiết/s** (HungNPV 4,26 · Hiếu 4,53 · NTK 4,55). Mục tiêu Hinton 4,2–4,5 âm tiết/s (250–270 âm tiết/60s) **khớp đúng dải này**. Kênh EN nhanh hơn (Kallaway 5,12; Varun 5,70) nhưng tiếng Anh nhiều thông tin hơn mỗi âm tiết → dịch kịch bản EN sang Việt phải **cắt 15–25% ý** chứ không nói nhanh hơn. [ĐO-TR]
3. **Hook tin AI = "[Hãng/nhân vật] + vừa + [động từ mạnh] + [cái gì]"**: 7/8 video Kallaway, 5/8 AI Savvy (gồm "just…" và "can now…"), 4/6 Varun (3 câu "just…", 1 câu "finally here") mở bằng "X just launched/dropped/solved…". Biến thể mạnh nhất là có **cái giá/hậu quả ngay trong câu 1**: Varun "Claude Mythos cuối cùng đã ra mắt, nhưng mạnh tới mức họ không dám phát hành cho công chúng" (693K view); Kallaway "OpenAI vừa giải một trong những bài toán nổi tiếng nhất thế giới" (43,1M view). [TRÍCH]
4. **Bẻ lái sớm là vũ khí của kênh EN, kênh VN gần như không dùng**: EN 0,68–2,8 lần/phút (Varun 2,8; AI Savvy 2,4; Kallaway 1,45), VN 0–0,34 lần/phút. Video 43,1M view của Kallaway có 5 lần bẻ lái ở **5,3s – 10,8s – 29,5s – 38,4s – 66,5s** (~1 lần/13s). → Đây là chỗ Hinton tạo khác biệt so với kênh VN cùng ngách. [ĐO-TR]
5. **Cấu trúc "N điểm" thống trị**: 59/87 video có đánh dấu liệt kê (HungNPV 6/6, AI Savvy 7/8, Hiếu 6/9, Jeff Su 4/5). Dạng phổ biến: "3 nâng cấp lớn nhất" (AI Savvy), "3 cấp độ" (Jeff Su), "7 câu lệnh" (Hiếu), "quy trình 8 bước" (NTK). Với 60s, **3 điểm là trần** (mỗi điểm ~9–12s); 7 điểm chỉ chạy được khi mỗi điểm là 1 câu mẫu lặp (Hiếu 7 lệnh/40s, 5,4s/lệnh). [ĐO-TR]
6. **Câu ngắn**: số từ/câu trung vị EN 5,5–12 (Kallaway 8,5; Jeff Su 9), VN 9–13 (dài hơn). Câu đầu VN dài 15–18 âm tiết (HungNPV 18) so với Kallaway 9 từ. → Hinton: câu hook ≤16 âm tiết, câu thân 8–14 âm tiết, không câu nào >20 âm tiết. [ĐO-TR]
7. **Con số là chất kết dính bằng chứng**: NTK 9,07 số/phút, Hiếu 4,14, Adam 2,79, Varun 2,07; Kallaway chỉ 0,41 nhưng dùng 1 con số "khủng" mỗi video. Hiếu mở **5/9 video bằng số view chứng minh** ("video AI này đã đạt 13 triệu view", "36 triệu view"). Varun chèn số cụ thể vào giữa câu chuyện ("trả 3.000 đô", "lỗ hổng 27 năm tuổi", "25.000 sao GitHub"). [ĐO-TR/TRÍCH]
8. **Kết bài chia 3 trường phái** (đếm trên 87 video): (a) **CTA comment từ khoá** — Kallaway 3/8 ("comment GEMINI và mình gửi link"), Adam 5/5 ("comment RUNWAY / H3…"), Hiếu, Lê Duy Hiệp; (b) **câu hỏi mở / câu chốt** — Varun 0 CTA follow, kết bằng câu hỏi (2 video: "nếu làm được cho chó, sao không làm cho người?") hoặc câu chốt logic/bằng chứng (2 video), AI Savvy 4/8, Kallaway 43,1M ("…ngày AI biết sáng tạo"); (c) **follow/lưu/đăng ký** — HungNPV, NTK, 秋芝. Video top mỗi kênh EN tin tức **không có CTA bán hàng** ở cuối. [TRÍCH]
9. **Xưng hô "bạn" nhiều ≠ view cao**: HungNPV 11,95 lần/phút, Brand Nat 9,4, AI Savvy 7,85; Varun **0** và Riley 0,65 vẫn top. Kênh tin tức kể theo ngôi thứ ba ("người này", "Anthropic"), kênh hướng dẫn nói "bạn". → Hinton tin AI: ≤3 lần "bạn"/phút, dồn vào đoạn "ý nghĩa với bạn" gần cuối. [ĐO-TR]
10. **Lời thoại hướng dẫn VN thường quá dài và lặp**: HungNPV trung vị 120s, Đình Hán 61–128s với đoạn "bấm vào… rồi bấm…" chiếm >50% thời lượng; video 4,8M view của Đình Hán thực chất bán bằng **kết quả demo 0–24s** (giọng hát AI), phần hướng dẫn đến sau. → Với Hinton 60s: kết quả trước, bước làm gói thành ≤3 bước, không đọc từng nút bấm. [ĐO-TR/TRÍCH]

---

## 3. CÔNG THỨC HOOK (có ví dụ thật, dịch Việt)

### 3.1 Bộ khung lý thuyết [GUIDE]
- **Kallaway – 6 kiểu hook** (phân tích 100 hook viral): Fortune Teller (dự báo), Experimenter (tôi đã thử), Teacher (dạy nhanh), Magician (hình ảnh gây sốc / "visual pacifier"), Investigator (bí mật/hé lộ), Contrarian (ngược số đông). Hook hỏng chủ yếu do **người xem không hiểu** chứ không do thiếu kịch tính. Lời–hình–chữ–âm phải nói **cùng một ý**. Chọn key visual **trước** khi viết lời.
- **Kallaway – 3 bước**: Context Lean (đặt bối cảnh) → Scroll-Stop Interjection ("nhưng", "tuy nhiên") → Contrarian Snapback (điều bất ngờ). Ví dụ Sphere 8M view: "Công nghệ trong Sphere ở Vegas thật điên rồ. Màn hình lớn nhất từng xây, gấp 20 lần IMAX. **Nhưng** nghe này, màn hình lại là thứ kém ấn tượng nhất… mà là âm thanh." Chữ hook trên màn 3–5 từ. "Đồng hồ 4 giây": phải cho người xem thấy giá trị trước giây thứ 4.
- **Jenny Hoyos**: hook ≤3s, **hiểu được khi tắt tiếng**; độ khó ngang lớp 5; hook + 2 dòng báo trước; chuyển ý không dừng ("thế là mình nấu lén" thay cho "bắt đầu nhé"); kể theo "nhưng/vì vậy"; viết câu cuối trước; cắt 1 giây cuối thì retention từ 83% lên 88%.

### 3.2 8 mẫu hook dùng được cho Hinton (đều có video thật)
| # | Mẫu | Ví dụ gốc [TRÍCH] | Bản Việt cho Hinton | Kiểu |
|---|---|---|---|---|
| H1 | **[Hãng] vừa [làm X] — nhưng [hệ quả bất ngờ]** | Varun R2nesxy7uYU (693K): "Claude Mythos is finally here, but it's so powerful that they're not releasing it to the public out of fear…" | "Claude Mythos đã ra mắt, nhưng mạnh tới mức Anthropic không dám cho bạn dùng." (16 âm tiết) | Investigator |
| H2 | **[Hãng] vừa giải/làm được điều [nổi tiếng/không tưởng]** | Kallaway 7645 (43,1M): "OpenAI just solved one of the most famous math problems in the world" → 5,3s "But this moment will go down as one of the most important breakthroughs…" | "OpenAI vừa giải một bài toán nổi tiếng nhất thế giới. Nhưng điều đáng nói không phải bài toán." | Fortune Teller |
| H3 | **Một người bình thường + AI + kết quả phi lý** | Varun lNTubupxkEM (874K): "This person just created a custom cancer vaccine for his dying dog using ChatGPT. The crazy part? He has zero medical background." | "Một người không học y vừa dùng ChatGPT làm vắc-xin ung thư cho chó của mình. Và nó có tác dụng thật." | Magician |
| H4 | **Lỗ hổng/mẹo "phi đạo đức" vừa viral + tôi đã thử** | Jeff Su QwwS7PxYpzo (6,6M): "Recently, a very unethical resume hack just went viral." → 20,6s "I had to try this out myself." | "Một mẹo lừa AI cực kỳ 'bẩn' vừa viral. Mình đã thử, và nó chạy thật." | Experimenter |
| H5 | **Kết quả trước: "Tôi lấy 1 [thứ], biến thành [kết quả], không cần [công sức]"** | Adam 7677763689885519125 (2,7M): "I took one product image, and turned it into completely different ads, and I didn't shoot a single one. Let me show you." | "Một tấm ảnh sản phẩm, mười mẫu quảng cáo khác nhau, không quay một cảnh nào. Xem này." | Magician |
| H6 | **"Đừng [làm cách cũ] nữa / Không phải tốn tiền cho X nữa"** | HungNPV: "Không phải tốn tiền trên những AI tạo 3D nữa, dùng AI này miễn phí trên chính máy của bạn." · NTK: "Đừng tốn hàng triệu… tự dựng hệ thống làm content nữa" | "Đừng trả tiền cho AI tạo giọng nữa, cái này miễn phí và chạy ngay trên máy bạn." | Contrarian |
| H7 | **Bằng chứng xã hội bằng số view** | Hiếu: "Video AI này đã đạt 13 triệu view. Đây là ngách hoạt hình sức khoẻ đang cực hot." | "Dạng video AI này vừa chạm 36 triệu view. Và cách làm chỉ mất mười phút." | Investigator |
| H8 | **Giải thích trong N cấp độ / N bước** | Jeff Su BF2k_fKuCVM (838K): "AI agents explained in three simple steps." · NTK "Lưu lại ngay quy trình 8 bước…" | "AI agent là gì? Ba cấp độ, nghe một lần là hiểu." | Teacher |

**Mẫu hook kiểu Douyin** (để nhận diện khi dịch lại): 秋芝 "朋友们等了两年的GPT5终于发布了,而且免费…" = *"Các bạn ơi, GPT-5 chờ hai năm cuối cùng đã ra, lại còn miễn phí"* (H1 không có "nhưng"); 鱼皮 "我把自己蒸馏成了一个AI的Skill,并且已经开源了" = *"Mình đã 'chưng cất' chính mình thành một kỹ năng AI, và mở mã nguồn luôn rồi"* (H5 ngôi thứ nhất). Khi dịch: **đổi ngôi thứ nhất sang thứ ba** ("Một lập trình viên Trung Quốc vừa…") vì Hinton không phải người làm.

### 3.3 Luật viết hook (gom từ số liệu + guide)
1. Câu 1 ≤16 âm tiết, nói xong trước **3,5s**; câu 2 (báo trước/bẻ lái) xong trước **6s** (Kallaway bẻ lái ở 5,3s; Varun "The crazy part?" ở 4,2s).
2. Câu 1 phải có **tên riêng nhận ra được** (OpenAI, ChatGPT, Google…) hoặc **con số** — các hook tin AI trích ở mục 3.2/9 đều có ít nhất 1 trong 2.
3. Chữ hook trên màn **3–5 chữ**, không chép nguyên câu VO (Kallaway; Jeff Su "A VERY UNETHICAL").
4. Không mở bằng "Hôm nay mình sẽ…" — 0/87 video làm vậy; chỉ 秋芝 có tiếng chào 1–2 âm tiết ("哪一口啊") rồi vào thẳng tin.
5. Hình 0–1s phải là thứ đang được nói tới (logo/tiêu đề tin/kết quả demo), không phải stock chung chung.

---

## 4. THIẾT BỊ GIỮ CHÂN (retention devices) trong thân bài

| Thiết bị | Câu mẫu Việt | Nguồn [TRÍCH] | Vị trí gợi ý (60s) |
|---|---|---|---|
| **Bẻ lái "nhưng"** | "Nhưng đó chưa phải phần điên rồ nhất." | Varun "But here's the wildest of all" (35,3s); Kallaway "But the issue is…" (29,5s) | 5s, ~25s, ~40s |
| **"Điều đáng nói không phải X, mà là Y"** | "Điều đáng nói không phải bài toán, mà là cách nó giải." | Kallaway 7645 10,8s | 6–12s |
| **"Cho tới tận bây giờ"** (trước/sau) | "AI giỏi một việc: thử hết mọi đáp án. Cho tới bây giờ." | Kallaway "That is, until now." 38,4s | giữa bài |
| **Báo trước số điểm** | "Ba nâng cấp lớn nhất, và người ta đã làm được gì với nó." | AI Savvy GPT-6 Astra 5,3s | 3–6s |
| **Đánh dấu điểm yêu thích** | "Và đây là phần mình thích nhất." | Brand Nat "And this is the part I love" (38s); Adam "But here's the part I really like" (13,6s); Kallaway Codex "the sneaky most impressive thing…" | điểm 3 |
| **"Tôi đã thử"** | "Mình đã thử, và…" | Jeff Su 20,6s; AI Savvy "After about 20 minutes… but many images did not match" | sau phần giới thiệu |
| **Kể theo thời gian** | "Bác sĩ nói chỉ còn vài tháng… Vài tuần sau…" | Varun lNTubupxkEM | thân |
| **So sánh đời thường** | "Giống như bán ô tô mà khoe có bánh xe." | Varun MacBook Neo "like launching a car and flexing how it has wheels" | sau con số |
| **Con số cụ thể giữa câu** | "trả ba nghìn đô", "lỗ hổng 27 năm tuổi" | Varun | mỗi 10–15s |
| **Câu hỏi giả định** | "Vậy nếu bạn là một agency nhỏ thì sao?" | Brand Nat "So if you run an agency…" | 45–52s |
| **Chuỗi lặp mẫu câu** | "Gõ /x-ray, nó sẽ… Gõ /drone view, nó sẽ…" | Hiếu 7 lệnh (1,2M, 40s) | dạng N lệnh |
| **Meme/phản ứng 1 giây** | (chữ) "Chậm thật sự 🐢" | 秋芝 meme "太慢" (quá chậm) | khi chê/khen |

---

## 5. TEMPLATE THEO THỜI LƯỢNG & THEO DẠNG

Ngân sách âm tiết tính ở **4,35 âm tiết/s** (giữa dải 4,2–4,5). 60s = **250–270 âm tiết** (đã chừa ~1s nghỉ đầu/cuối).

### 5.1 Khung chung
| Đoạn | 30s (125–135 ât) | 60s (250–270 ât) | 90s (380–400 ât) |
|---|---|---|---|
| Hook (claim + key visual) | 0–3s · 13 | 0–3s · 13 | 0–3s · 13 |
| Báo trước / bẻ lái | 3–5s · 9 | 3–6s · 13 | 3–7s · 17 |
| Bối cảnh (là gì, ai làm) | 5–10s · 22 | 6–14s · 35 | 7–18s · 48 |
| Thân (điểm/bằng chứng) | 10–25s · 65 (2 điểm) | 14–44s · 130 (3 điểm × ~43) | 18–70s · 225 (3–4 điểm) |
| Twist / hạn chế | — | 44–52s · 35 | 70–80s · 43 |
| Ý nghĩa với người xem + kết | 25–30s · 22 | 52–60s · 34 | 80–90s · 43 |

### 5.2 Dạng A — TIN AI (mặc định Hinton)
```
[0–3s]  HOOK H1/H2/H3: [Hãng] vừa [động từ mạnh] [cái gì] (+ "nhưng"/hệ quả) — ≤16 ât
[3–6s]  BẺ LÁI/BÁO TRƯỚC: "Nhưng điều đáng nói không phải X…" / "Và nó [kết quả khó tin]."
[6–14s] BỐI CẢNH: là gì, ai làm, khi nào — 1 bằng chứng hình (ảnh chụp blog/tweet chính thức)
[14–24s] ĐIỂM 1 + con số + clip demo
[24–34s] ĐIỂM 2 + "nhưng đó chưa phải phần điên rồ nhất"
[34–44s] ĐIỂM 3 (phần đáng nói nhất) + clip/chart
[44–52s] TWIST/HẠN CHẾ: giá, ai chưa dùng được, rủi ro ("Nhưng có một vấn đề…")
[52–60s] Ý NGHĨA + KẾT: câu hỏi mở / câu kết vòng về hook / CTA nhẹ
```
### 5.3 Dạng B — N CÔNG CỤ / N CÂU LỆNH
```
[0–3s]  Kết quả đẹp nhất + "N [công cụ/lệnh] này làm được [X]" (H5/H7)
[3–5s]  "Cái thứ [N] mới là đáng sợ nhất." (vòng mở)
[5–50s] Mỗi mục 1 mẫu câu cố định: "[Tên] — [làm gì] — [ví dụ 1 câu]" · 3 mục ≈ 14s/mục, 5 mục ≈ 9s/mục, 7 mục ≈ 6s/mục
[50–57s] Mục cuối = mục mạnh nhất (giữ lời hứa của vòng mở)
[57–60s] CTA: "Lưu lại…" / comment từ khoá
```
### 5.4 Dạng C — HƯỚNG DẪN (≤3 bước)
```
[0–4s]  KẾT QUẢ trước (clip output) + "Làm cái này mất [thời gian], miễn phí."
[4–8s]  Vì sao đáng làm (1 câu số liệu/so sánh)
[8–45s] Bước 1–3, mỗi bước 1 hành động, KHÔNG đọc từng nút ("vào trang, chọn chế độ, dán lệnh")
[45–55s] So sánh trước/sau hoặc lỗi hay gặp (bằng chứng "mình đã thử")
[55–60s] Kết: link/lệnh để ở bình luận (comment từ khoá)
```
### 5.5 Dạng D — DOUYIN DỊCH LẠI
```
1. Gỡ khung kênh gốc: bỏ chào hỏi ("哪一口啊/朋友们"), bỏ "下次见/关注", bỏ mọi tên/handle kênh TQ.
2. Đổi ngôi: "我/mình" → "một lập trình viên Trung Quốc / một nhóm ở Thâm Quyến…".
3. Giữ xương sống thông tin (秋芝 hay dùng "强力总结为以下几点" = "tóm gọn thành mấy điểm sau") → ép về 3 điểm.
4. Viết lại hook theo H1/H3/H5 bằng tiếng Việt, KHÔNG dịch sát câu mở gốc.
5. Thêm 1 câu bối cảnh cho người Việt (dùng được ở VN không, miễn phí không, có tiếng Việt không).
6. Cắt: video gốc 秋芝 trung vị 194s → 60s nghĩa là bỏ ~70% nội dung; chọn 3 điểm có hình demo đẹp nhất.
7. Đếm lại âm tiết (250–270), kiểm tra tên riêng phiên âm thống nhất.
```

---

## 6. MẪU KẾT / CTA (không quảng bá kênh Trung Quốc)
| Loại | Mẫu | Dùng khi |
|---|---|---|
| Câu hỏi mở (Varun) | "Nếu làm được cho một chú chó, tại sao không làm được cho người?" | Tin có hàm ý lớn |
| Câu kết vòng (Kallaway 43,1M) | "…và tháng Năm 2026 sẽ được nhớ là ngày AI biết sáng tạo." | Tin "bước ngoặt" |
| Hỏi ý kiến (AI Savvy, Brand Nat) | "Bạn đã được dùng chưa? Bình luận cho mình biết bạn sẽ làm gì với nó." | Model/tính năng mới |
| Comment từ khoá (Kallaway, Adam, Hiếu) | "Bình luận chữ AGENT, mình gửi link." | Có tài nguyên thật để gửi (cần người trực inbox) |
| Lưu lại (NTK, Hiếu) | "Lưu video lại, lần sau cần là có ngay." | Dạng N công cụ/lệnh |
| Follow ngắn | "Theo dõi Hinton để không lỡ tin AI mỗi ngày." | Tối đa 1 câu, ≤12 âm tiết |
Luật: CTA ≤1 câu (≤3s); **cắt sát** sau chữ cuối (Jenny Hoyos: bỏ 1s cuối tăng retention 83→88%); không "cảm ơn đã xem".

---

## 7. CHECKLIST QA KỊCH BẢN (chạy trước khi TTS)
- [ ] 250–270 âm tiết (dem_am_tiet.py) cho 60s; 125–135 cho 30s.
- [ ] Câu 1 ≤16 âm tiết, có tên riêng hoặc con số; hiểu được khi tắt tiếng (chữ hook 3–5 chữ đi kèm).
- [ ] Có bẻ lái/báo trước trước giây 6.
- [ ] ≥2 lần "nhưng/thực ra/điều đáng nói" trong thân (mục tiêu ~1 lần/13–20s).
- [ ] Mỗi claim có 1 bằng chứng hình (đánh dấu `[HÌNH: …]` ngay trong kịch bản).
- [ ] ≥3 con số cụ thể (giá, ngày, %, số người dùng) — đã kiểm chứng nguồn.
- [ ] Không câu nào >20 âm tiết; câu trung vị 8–14.
- [ ] Thuật ngữ được giải thích bằng 1 câu đời thường (độ khó "lớp 5").
- [ ] "bạn" ≤3 lần/phút trong dạng tin; dồn vào đoạn ý nghĩa.
- [ ] Kết ≤1 câu; không chào; không CTA về kênh TQ; không hứa gửi link nếu không có người gửi.
- [ ] Đọc to 1 lần ở tốc độ 1.2: vấp ở đâu, sửa ở đó (Huỳnh Quốc Cường: đọc to trước khi quay).
- [ ] Tên riêng phiên âm nhất quán với phụ đề (ChatGPT, Gemini, Claude…).

---

## 8. BA KỊCH BẢN MẪU (đã đếm âm tiết)

### 8.1 Tin AI — 258 âm tiết (~59s @4,35) — khung Varun lNTubupxkEM
> Dữ kiện lấy từ video Varun + bài The Australian hiện trong video (OCR). **Kiểm chứng lại nguồn trước khi dùng thật.**
```
[0–4s][HÌNH: ảnh chụp tweet Greg Brockman về vắc-xin cho chó]
Một người không học y vừa dùng ChatGPT thiết kế vắc-xin ung thư cho chú chó sắp chết của mình.
[4–6s][HÌNH: chữ động "VÀ NÓ CÓ TÁC DỤNG"] Và nó có tác dụng thật.
[6–7s] Chuyện là thế này.
[7–15s][HÌNH: ảnh chú chó Rosie / bài báo] Chú chó Rosie của anh Paul bị ung thư, bác sĩ thú y nói nó chỉ còn vài tháng. Anh chi hàng nghìn đô cho hóa trị và phẫu thuật, nhưng không ăn thua.
[15–23s][HÌNH: giao diện ChatGPT → logo UNSW] Thế là Paul mở ChatGPT và tự tìm cách. ChatGPT gợi ý hướng miễn dịch, rồi chỉ anh tới một phòng thí nghiệm gen ở Đại học New South Wales.
[23–31s][HÌNH: chuỗi ADN / chữ "3.000 USD"] Ở đó, anh trả ba nghìn đô để so ADN khỏe mạnh với ADN ung thư của Rosie, tìm đúng chỗ đã đột biến.
[31–37s][HÌNH: giao diện AlphaFold / cấu trúc protein xoay] Rồi anh đưa dữ liệu vào AlphaFold, thiết kế một vắc-xin riêng từ chính ADN của Rosie.
[37–43s][HÌNH: chữ "KHỐI U −50%"] Phòng thí nghiệm sản xuất, tiêm cho Rosie, và chỉ vài tuần sau, khối u teo lại một nửa.
[43–48s][HÌNH: ảnh chụp bài The Australian, zoom vào câu trích] Báo The Australian đưa tin, và người phụ trách phòng thí nghiệm nói nguyên văn: trời ơi, nó hiệu quả thật.
[48–55s] Các nhà khoa học sốc thật sự. Không phải vì nó hiệu quả, mà vì người làm ra nó không hề có nền tảng y khoa, chỉ có AI và quyết tâm cứu chú chó của mình.
[55–59s][HÌNH: chữ động câu hỏi] Câu hỏi lớn hơn là: nếu làm được cho một chú chó, tại sao không làm được cho người?
```

### 8.2 Giải thích 3 cấp độ — 253 âm tiết (~58s) — khung Jeff Su BF2k_fKuCVM
```
[0–3s][HÌNH: chữ "AI AGENT = ?" + 3 bậc thang] AI agent là gì? Ba cấp độ, nghe một lần là hiểu.
[3–14s][HÌNH: khung chat ChatGPT gõ "viết email xin nghỉ"] Cấp một: mô hình. Bạn gõ cho ChatGPT viết giúp email xin nghỉ, nó trả lại một email. Hết. Ở cấp này AI chỉ ngồi chờ, không đụng được vào công cụ nào.
[14–28s][HÌNH: ChatGPT + logo Google Calendar nối dây] Cấp hai: quy trình AI. Bạn cho ChatGPT quyền vào Google Calendar, nó xếp lịch theo lệnh của bạn. AI đã có công cụ, nhưng vẫn bị động, bạn bảo gì làm nấy. Bảo tạo lịch họp ba giờ chiều thứ sáu, nó tạo đúng ba giờ chiều thứ sáu, không hơn.
[28–44s][HÌNH: lịch tự đổi màu, ô "Từ chối"/"Chấp nhận" tự bấm] Cấp ba: AI agent. Thay vì ra lệnh, bạn giao mục tiêu: quản lý lịch họp tuần này giúp tôi. Agent tự suy nghĩ cuộc họp nào nên nhận, cuộc nào nên từ chối, rồi tự trả lời lời mời, tự dời lịch khi bị trùng, còn gửi email báo cho người kia giờ mới.
[44–52s][HÌNH: bảng 3 cột so sánh, cột 3 sáng vàng] Khác biệt nằm ở đây. Cấp một và cấp hai, bạn là người suy nghĩ. Cấp ba, AI suy nghĩ và hành động thay bạn, bạn chỉ cần duyệt kết quả.
[52–55s][HÌNH: lưới logo các hãng] Đó là lý do gần như hãng nào cũng đang gắn chữ agent vào sản phẩm của mình.
[55–58s] Lưu video này lại, lần sau nghe ai nói về agent, bạn sẽ biết ngay nó đang ở cấp mấy, và nó thật sự làm được tới đâu.
```

### 8.3 Douyin dịch lại — khung có ô trống (điền theo video gốc), ngân sách 260 âm tiết
```
[0–3s · 14 ât]  Một lập trình viên Trung Quốc vừa [làm điều X bằng AI] — và [hệ quả bất ngờ].
[3–6s · 13 ât]  Nhưng điều đáng nói không phải [X], mà là [cách làm / con số].
[6–14s · 35 ât] Bối cảnh: [trend đang diễn ra trên mạng TQ, 1 câu] + [người này là ai, đã làm gì trước đó, 1 câu có số].
[14–24s · 43 ât] Điểm 1: [bước/tính năng 1] + [HÌNH: demo gốc, che chữ Hán bằng dải tiêu đề Việt].
[24–34s · 43 ât] "Nhưng đó chưa phải phần hay nhất." Điểm 2: [ ].
[34–44s · 43 ât] Điểm 3: [phần ấn tượng nhất] + [HÌNH: kết quả].
[44–52s · 35 ât] Ở Việt Nam dùng được không: [miễn phí? cần VPN? có tiếng Việt? mã nguồn mở ở đâu].
[52–60s · 34 ât] Kết: câu hỏi mở cho người Việt ("Nếu được 'chưng cất' một người thành AI, bạn chọn ai?").
```
Ví dụ điền hook từ 鱼皮 kFMPdjOU5eM: *"Một lập trình viên Trung Quốc vừa 'chưng cất' chính mình thành một kỹ năng AI, rồi mở mã nguồn cho ai cũng dùng."* → bẻ lái: *"Nhưng anh không làm cho vui: sáu năm viết hơn nghìn bài, mấy trăm video, giờ thành một bản sao biết dạy lập trình."* (số liệu "6 năm, hơn nghìn bài, vài trăm video" từ lời gốc 22–28s [TRÍCH]).

---

## 9. PHÂN TÍCH BEAT CÁC VIDEO TIÊU BIỂU (mốc giây từ transcript) [TRÍCH]

**Kallaway 7645299083573267742 — "OpenAI just solved math" (43,1M view, 72,8s, 5,09 ât/s nói)**
0,0 hook claim (14 từ) → 5,3 bẻ lái "But this moment will go down…" → 10,8 "Điều thú vị không phải bài toán mà là cách giải" → 16,4 bối cảnh "Trước giờ AI chỉ giỏi brute force" → 29,5 "But the issue is…" → 38,4 "That is, until now." → 40–53 giải thích → 53–65 ý nghĩa (chữa ung thư, vật liệu, vật lý) → 65,8 "It feels small. But…" → 71,5 kết vòng "…ngày AI biết sáng tạo". **Không CTA.**

**Kallaway 7630160402457939230 — Codex update (32,5M, 73s)**
0 "OpenAI vừa tung bản cập nhật lớn cho Codex" → 3 "Nếu bạn làm bất cứ gì trên internet, đây là cú mở khoá lớn" (đối tượng + lợi ích) → 6 tính năng 1 (preview app) → 17 tính năng 2 (bộ ảnh) → 23 "Điều này nghĩa là…" → 30,3 "thứ ấn tượng ngầm nhất chẳng liên quan gì tới code" → … → CTA "comment… mình gửi link".

**Varun R2nesxy7uYU — Claude Mythos (693K, 64s, 5,91 ât/s)**
0 hook H1 (claim + "nhưng" + hậu quả) → 6,1 "Instead, Anthropic announced Project Glasswing…" + danh sách AWS/Apple/Google/Microsoft/Nvidia (hình: lưới logo) → 15,5 bằng chứng "hàng nghìn lỗ hổng nghiêm trọng, cả mọi hệ điều hành lớn" → 21,6 giai thoại kỹ sư để qua đêm → 25,9 con số "lỗ hổng 27 năm trong OpenBSD" → 35,3 "But here's the wildest of all" → sandbox escape, email cho nhà nghiên cứu "đang ăn sandwich ở công viên" (hình: stock người ăn sandwich) → 47 "On top of it, benchmarks are insane" (hình: chart chính thức) → 55,3 kết logic "vì thế Anthropic không phát hành" → 60,2 câu chốt "cho tới khi mọi phần mềm lớn đã kháng được Mythos".

**Varun lNTubupxkEM — vắc-xin cho chó (874K, 49s)**: 0 hook H3 → 4,2 "The crazy part?" → 6,3 "Here's the full story" → kể theo thời gian 7–38 (mỗi câu 1 hình: tweet, bài báo, lab, AlphaFold) → 38,5 kết quả "khối u teo một nửa" → 42,4 "Not just because it worked, but because…" → 45,9 câu hỏi mở.

**Jeff Su QwwS7PxYpzo — resume hack (6,6M, 54s)**: 0 hook "một mẹo resume cực phi đạo đức vừa viral" → 3,7 ai/làm gì → 9,4 đọc nguyên câu prompt ẩn → 13,9 cơ chế (chữ trắng trên nền trắng) → 20,6 "Mình phải tự thử" → 21,9 thử với hồ sơ "Sam Bankman-Fried" (hài) → 33,7 "và… nó chạy" → 35 lặp với Bard → kết bằng meme.

**Adam.Digital 7677763689885519125 — Runway agent (2,7M, 32s)**: 0 hook H5 + "Let me show you" (4,7) → 5,4 bước gộp 1 câu → 13,6 "But here's the part I really like" → 20 kết quả campaign → 22,9 lợi ích tiền ("trước khi tiêu một xu cho sản xuất") → 29,4 CTA "Comment RUNWAY".

**Brand Nat 7680530870259698964 — Vanta (1,5M, 70s, quảng cáo)**: 0 "Hãy tưởng tượng tên lửa này là sản phẩm của bạn" (đạo cụ Lego) → 9,9 "But they just have one question" → 17 nỗi đau → 29 "So here's how…" → 32 giới thiệu → 38,2 "And this is the part I love" → 53,4 "And here's the thing" → 55,8 bằng chứng xã hội "16.000 công ty" → 64,6 CTA ưu đãi.

**Hiếu 7686872745115897109 — 7 câu lệnh (1,2M, 41s, 4,67 ât/s)**: 0 lệnh 1 vào thẳng (không hook riêng!) → 6,0 / 12,7 / 18,9 / 23,2 / 26,8 / 31,5 mỗi lệnh 1 câu mẫu "Gõ /…, nó sẽ…" (≈5,4s/lệnh) → 36,8 CTA "7 câu lệnh mình để ở bình luận, nhấn theo dõi".

**NTK mg0F55YoESM — Claude 8 bước (17,3K FB, 88s, 4,61 ât/s)**: 0 hook lợi ích + thời gian ("chỉ sau một buổi cuối tuần") → 3 "Lưu lại ngay quy trình 8 bước" → Bước 1–8 cứ ~4–5s/bước → pitch khoá học → CTA link.

**AI Savvy 7681592962127580437 — GPT-6 Astra (19,2K FB, 106s)**: 0 "OpenAI vừa ra GPT-6 Astra, thay vì làm bạn chán với benchmark…" → 5,3 "để mình cho xem 3 nâng cấp lớn nhất và người ta đang làm gì với nó" → 10 "The first one…" (+ số "nhanh gấp đôi GPT-5.6") → 32 "The second one…" → 55 "And the crazy part is…" → 61 "And the last one…" → kết hỏi "bạn đã có quyền dùng chưa".

**秋芝 DvQcsdvIMiE — GPT-5 (255s)**: 0 "GPT-5 chờ 2 năm cuối cùng đã ra, miễn phí cho tất cả" → 7,9 hệ quả "OpenAI gỡ hết model cũ" → 18 điểm benchmark → 32,4 "buổi ra mắt 1 tiếng, tóm gọn thành mấy điểm sau" → liệt kê → thử thực tế → meme "quá chậm" → kết "theo dõi, mai gặp".

**鱼皮 kFMPdjOU5eM — tự "chưng cất" thành Skill (150s, 4,47 chữ/s)**: 0 hook ngôi thứ nhất + "đã mã nguồn mở" → 4,8 bối cảnh trend "chưng cất người" → 22 lý do cá nhân (6 năm, nghìn bài) → 31,7 sản phẩm → 38 "Vậy mình làm thế nào?" → các bước → kết mời bình luận "bạn muốn chưng cất ai".

**Đình Hán 7461257650701978887 — biến bạn thành ca sĩ (4,8M, 71s)**: 0 hook lời hứa → 7–17 **demo kết quả (bài hát AI)** → 18 "Với cách này bạn hát được bất kỳ bài nào" → 24 "Trong video này mình hướng dẫn chi tiết từng bước" → 31–70 đọc từng thao tác → kết "Và đây là…".

**Lê Duy Hiệp 7623616186823068944 — xếp hạng tool AI (88K, 34s)**: tier list nói nhanh, mỗi tool 1 câu "[Tool] mình cho hạng [S/A/B/D] vì [lý do 1 vế]" (~3s/tool) → Manus "hạng S vì tăng năng suất gấp 10 lần" làm điểm nhấn.

---

## 10. GUIDE CÔNG KHAI ĐÃ DÙNG
- Kallaway — *I Studied 100 Viral Hooks…* (tóm tắt): https://moderncreator.app/2025-03-19-kallaway-i-studied-100-viral-hooks-these-6-will-make-you-go-viral (YouTube xnOe8aA9Pmw)
- Kallaway — *How to Create Irresistible Hooks*: https://moderncreator.app/2024-12-19-kallaway-how-to-create-irresistible-hooks-and-blow-up-your-content
- Jenny Hoyos — podcast Creator Science: https://podcast.creatorscience.com/jenny-hoyos/ · playbook: https://www.marketingexamined.com/blog/jenny-hoyos-short-form-video-playbook
- Paddy Galloway — nghiên cứu 5.400 Shorts/33 kênh (50–60s nhiều view nhất; AVD >50s ≈ 4,1M view TB; viewed-vs-swiped 70–90%): https://nowbam.com/decoding-the-youtube-shorts-algorithm/
- Huỳnh Quốc Cường — cách viết kịch bản TikTok (Hook–Vấn đề–Giải pháp–Bằng chứng–CTA; 60s ≈ 150–220 chữ; đọc to trước khi quay): https://huynhquoccuong.com/tiktok-ads/cach-xay-kenh/cach-viet-kich-ban-tiktok.html
- Ghi chú: gợi ý "150–220 chữ/60s" của Huỳnh Quốc Cường là cho người tự nói trước camera; số đo thực tế các kênh VN là 4,26–4,55 âm tiết/s ≈ 255–275 âm tiết/60s → Hinton giữ 250–270.

## 11. HẠN CHẾ
- Transcript whisper small trên CPU: lượt đầu (beam 1 + initial_prompt) bỏ sót đoạn; đã chạy lại beam 5; 29 video nhạc nền to chạy lại với VAD + tắt ngưỡng no-speech, thêm bộ lọc câu lặp do nhạc. Vẫn còn hỏng: Duy Luân (3/5), Tommy (3/5), Lê Duy Hiệp (4/5), một phần Riley/鱼皮.
- Âm tiết tiếng Anh là ước tính heuristic; chữ Hán ≠ âm tiết Việt, chỉ so sánh tương đối.
- Đếm bẻ lái/liệt kê/CTA bằng regex: bỏ sót cách nói khác (vd. "let me know"); whisper tiếng Việt gần như không ra dấu "?" nên không đếm được câu hỏi.
- "Video top" = view cao nhất trong 60–200 video gần nhất của mỗi kênh mà listing trả về, không phải mọi thời đại.
- View 鱼皮/秋芝 lấy từ bản đăng lại có thể thấp hơn bản gốc Douyin; follower 秋芝/鱼皮 là số bên thứ ba.
