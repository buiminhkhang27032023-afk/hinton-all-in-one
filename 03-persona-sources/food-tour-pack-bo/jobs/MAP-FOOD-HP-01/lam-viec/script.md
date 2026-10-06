# Một ngày ăn sập Hải Phòng — food tour 7 điểm, 7 món (bản đồ động)

## Metadata
| Trường | Giá trị |
|---|---|
| Job | MAP-FOOD-HP-01 |
| Phiên bản | **v2 — 7 điểm** (Bot3 biên kịch) — 2026-10-05, theo `chon-tuyen.md` bố chốt 17:19 |
| Định dạng | 9:16, map animation (template HyperFrames trong `lam-viec/template`, kế thừa MAP-FOOD-HCM-01) |
| Thời lượng mục tiêu | **~90s** (VO ~85–87s + end card ~2,5s) |
| Giọng | Nam, OmniVoice male clone v2 @1.2, SRT sidecar |
| Số âm tiết VO | **391** (token khoảng trắng / regex bỏ dấu câu trên `storytelling_script.txt`, hai cách đếm khớp) → ~85s @4,6 âm tiết/giây; "Avani Harbour View", "Hinton Media" đọc dài hơn số token → thực tế ~86–87s |
| Thứ tự | Food tour theo **nhịp một ngày ăn** (sáng → trưa → chiều → tối → tráng miệng), **KHÔNG xếp hạng**: ① Bún cá miền duyên hải (Văn Cao) → ② Bánh Mỳ Cay Bà Già (Lê Lợi) → ③ Quán Nga Nem Cua Bể (Trần Nhật Duật) → ④ Bánh đúc tàu Cô Chuyền (Hai Bà Trưng) → ⑤ Bánh Đa Cua Bà Cụ (Cầu Đất) → ⑥ Lẩu Cua Đồng Đất Cảng (Dư Hàng) → ⑦ Sủi dìn Cô Út (Cầu Đất) |
| 7 món | bún cá cay · bánh mì que cay · nem cua bể · bánh đúc tàu · bánh đa cua · lẩu cua đồng · sủi dìn |
| Pin phụ intro | Nhà hát Lớn Hải Phòng, TTTM Chợ Sắt, Avani Harbour View Hotel |
| Quote đọc trong VO | **2**: ① Bún cá — "phần ăn đầy đặn so với ba mươi lăm nghìn, mình rất thích" · ② Bà Già — "theo tôi, đây là bánh mì cay ngon nhất phố, ba nghìn một chiếc" |
| Quote chỉ trên màn | 7 bong bóng (1/điểm); 5 bong bóng silent (Nga, Cô Chuyền, Bà Cụ, Lẩu, Cô Út) |
| File kèm | `storytelling_script.txt` (VO thuần), `scene-table.md` (bảng cảnh ~0:00–1:30 + ghi chú Bot2) |
| Bản cũ | v1 5 điểm (post-QA 267 âm tiết): `v1-5diem/` (script.md, storytelling_script.txt, scene-table.md); pre-QA 257: `*.v1.*` |

## Disclaimer số liệu
Cố định góc dưới màn hình suốt video: **"Số liệu Google Maps tham khảo, 10/2026"**.
Sao/review lấy qua trung gian (Exa Places — Google-derived; RestaurantGuru cho Bà Cụ), fetch 05/10/2026. VO luôn nói "khoảng / gần / hơn"; màn hình dùng "~".
Bong bóng là **trích review**: review tiếng Anh hiện bản dịch ngắn + nhãn "Review Google Maps (dịch)"; Cô Chuyền nhãn "Review toididau". Anon/Thực khách → "Thực khách". Sao trong bong bóng là sao của người review, tách khỏi thẻ sao Google.
Lẩu Đất Cảng ~4.9★: chỉ nói "khoảng bốn phẩy chín sao", **không** khen "cao nhất / đỉnh nhất tuyến", không tag nổi bật (xem [CẦN QA] #2).

## Ghi chú phát âm cho VO
- "Bánh Mỳ" → bánh mì · "pa tê" → pa-tê · "Sủi dìn" → sủi-dìn (dìn thanh huyền) · "Dư Hàng", "Văn Cao" đọc rõ.
- "Avani Harbour View" → a-va-ni ha-bơ viu · "Hinton Media" → hin-tơn mê-đi-a.
- "Trần Nhật Duật" đọc rõ từng tiếng, không nuốt "Duật".
- Số viết thành chữ: 4.5 → bốn phẩy năm · 360 → hơn ba trăm rưỡi · 35k → ba mươi lăm nghìn · 06:00 → sáu giờ · 4.3 → bốn phẩy ba · 292 → gần ba trăm · 3k → ba nghìn · 3.9 → ba phẩy chín · 757 → hơn bảy trăm năm mươi · 4.4 → bốn phẩy bốn · 198 → gần hai trăm · 12–20k → mười hai đến hai mươi nghìn · 17:00 → năm giờ chiều · 3.8 → ba phẩy tám · 1771 → gần một nghìn tám trăm · 22:30 → mười giờ rưỡi tối · 4.9 → bốn phẩy chín · 287 → gần ba trăm · 205 → hơn hai trăm · 15:00 → ba giờ chiều · 10–15k → mười đến mười lăm nghìn.
- 2 câu quote: nghỉ ~0,3s sau "Một thực khách viết:" / "Một thực khách khác viết:", hạ giọng sắc "kể lại".
- Mốc thời gian trong ngày ("Gần trưa", "Chiều xuống", "Tối đến") nhấn nhẹ — là xương sống nhịp "một ngày ăn".

---

## Full script

### HOOK (0:00–0:06) — 28 âm tiết
> Một ngày ăn sập Hải Phòng, đi đâu, ăn gì? Bảy điểm dừng, bảy món khác nhau, từ bữa sáng tới tráng miệng. Chuẩn bị bụng, xuất phát!

*Màn hình: bản đồ Hải Phòng từ cao lao xuống; 7 icon món nảy lên quanh tuyến (chưa lộ tên quán); chữ **MỘT NGÀY ĂN SẬP HẢI PHÒNG 🔥** · 7 điểm · 7 món · đồng hồ mini 6:00 → 22:00 quay nhanh.*

### Intro bối cảnh (0:06–0:11.5) — 24 âm tiết
> Mốc định vị: Nhà hát Lớn, Chợ Sắt và khách sạn Avani Harbour View. Phần lớn tuyến ăn nằm quanh trung tâm thành phố.

*Màn hình: 3 pin phụ pop (Chợ Sắt → Nhà hát Lớn → Avani); đường tuyến 7 điểm vẽ mờ; điểm ① Văn Cao nằm lệch đông-nam ngoài cụm (khớp lời "phần lớn").*

### ① Bún cá miền duyên hải — 227 Văn Cao (0:11.5–0:24) — 56 âm tiết
> Điểm một, khởi động hơi xa trung tâm, Bún cá miền duyên hải trên phố Văn Cao, mở bữa sáng từ sáu giờ. Bún cá cay, cá giòn. Khoảng bốn phẩy năm sao, hơn ba trăm rưỡi đánh giá. Một thực khách viết: phần ăn đầy đặn so với ba mươi lăm nghìn, mình rất thích!

*Màn hình: ĐIỂM 1 · 🐟🌶️ bún cá cay · 🕕 6:00–13:00 · Bữa sáng · ⭐ ~4.5 · ~360 review. Bong bóng (ĐỌC trong VO): "Phần ăn đầy đặn so với 35k, mình rất thích!" — Thực khách · Review Google Maps (dịch) · ★5. Không tag giá riêng — 35k chỉ nằm trong quote.*

### ② Bánh Mỳ Cay Bà Già — 57A Lê Lợi (0:24–0:35) — 49 âm tiết
> Điểm hai, vào phố Lê Lợi, Bánh Mỳ Cay Bà Già. Bánh mì que nướng giòn, pa tê, tương ớt. Khoảng bốn phẩy ba sao, gần ba trăm đánh giá. Một thực khách khác viết: theo tôi, đây là bánh mì cay ngon nhất phố, ba nghìn một chiếc!

*Màn hình: ĐIỂM 2 · 🥖 bánh mì que · ⭐ ~4.3 · ~292 review. Bong bóng (ĐỌC trong VO): "Bánh mì cay ngon nhất phố, theo tôi. 3k một chiếc." — Thực khách · Review Google Maps (dịch) · ★5. Không tag giá riêng; không hiện giờ (nguồn lệch).*

### ③ Quán Nga Nem Cua Bể — 92 Trần Nhật Duật (0:35–0:44) — 40 âm tiết
> Gần trưa, điểm ba, rẽ sang Trần Nhật Duật, gần Nhà hát Lớn, Quán Nga Nem Cua Bể. Nem cua bể chiên giòn, ăn kèm bún, thịt nướng. Khoảng ba phẩy chín sao, hơn bảy trăm năm mươi đánh giá.

*Màn hình: ĐIỂM 3 · 🦀 nem cua bể · ⭐ ~3.9 · ~757 review. Bong bóng silent: "Nem cua bể tươi, nóng, giòn, đầy cua." — Thực khách · Review Google Maps (dịch) · ★5. **Không** giá (blog), **không** giờ (lệch nguồn).*

### ④ Bánh đúc tàu Cô Chuyền — 159 Hai Bà Trưng (0:44–0:55) — 49 âm tiết
> Điểm bốn, sang Hai Bà Trưng, bánh đúc tàu Cô Chuyền. Bánh đúc với tôm, thịt, đu đủ, kèm nước mắm giấm. Khoảng bốn phẩy bốn sao, gần hai trăm đánh giá. Giá tham khảo mười hai đến hai mươi nghìn một bát, nhớ ghé trước năm giờ chiều.

*Màn hình: ĐIỂM 4 · 🥣 bánh đúc tàu · ⭐ ~4.4 · ~198 review · 💵 ~12–20k/bát (tham khảo) · 🕔 Đóng 17:00. Bong bóng silent: "Ăn lạ lạ mà cũng rất ngon. Một bát 15k." — Tran N. Y. · Review toididau · ★5. Pin toạ độ places.json (20.852667, 106.677718), không zoom sát số nhà.*

### ⑤ Bánh Đa Cua Bà Cụ — 179 Cầu Đất (0:55–1:03) — 37 âm tiết
> Chiều xuống, điểm năm, về Cầu Đất, Bánh Đa Cua Bà Cụ. Bánh đa cua bể, thêm nem cua chiên. Khoảng ba phẩy tám sao, gần một nghìn tám trăm đánh giá, nhiều đánh giá nhất tuyến.

*Màn hình: ĐIỂM 5 · 🍜 bánh đa cua · ⭐ ~3.8 · ~1.771 review · tag "Nhiều review nhất tuyến". Bong bóng silent: "Nem cua và bánh đa cua ngon, ăn rất thích." — Thực khách · Review Google Maps (dịch) · ★4. **Không** giá blog; không giờ.*

### ⑥ Lẩu Cua Đồng Đất Cảng — 22 Dư Hàng (1:03–1:12) — 39 âm tiết
> Tối đến, điểm sáu, Lẩu Cua Đồng Đất Cảng, phố Dư Hàng, quận Lê Chân. Nồi lẩu cua đồng, nước cua đậm đà, mở tới mười giờ rưỡi tối. Khoảng bốn phẩy chín sao, gần ba trăm đánh giá.

*Màn hình: ĐIỂM 6 · 🍲🦀 lẩu cua đồng · 🕙 Đến 22:30 · ⭐ ~4.9 · ~287 review (thẻ sao style thường, **không** tag/glow nổi bật, **không** chữ "cao nhất"). Bong bóng silent: "Nước dùng cua tuyệt vời." — Thực khách · Review Google Maps (dịch) · ★5. **Không** giá (Tadiha ~120k/nồi vs Toplist ~200–300k/người — lệch, xem [CẦN QA] #3).*

### ⑦ Sủi dìn Cô Út — 163 Cầu Đất (1:12–1:22.5) — 46 âm tiết
> Điểm bảy, quay lại Cầu Đất, ngay sát Bà Cụ, Sủi dìn Cô Út chốt tour, mở từ ba giờ chiều. Sủi dìn nóng, chè vừng, chè đậu. Khoảng bốn phẩy bốn sao, hơn hai trăm đánh giá. Chỉ mười đến mười lăm nghìn một bát.

*Màn hình: ĐIỂM 7 · KẾT TOUR · 🍡 sủi dìn · 🕒 Từ 15:00 · ⭐ ~4.4 · ~205 review · 💵 ~10–15k/bát. Bong bóng silent: "Sủi dìn ngon nhất! Nước đường không quá ngọt." — Thực khách · Review Google Maps (dịch) · ★5.*

### CTA (1:22.5–1:27.5) — 23 âm tiết + end card (1:27.5–1:30)
> Lưu ngay tuyến này, rủ hội bạn đi ăn cùng, và theo dõi Hinton Media để xem bản đồ ăn uống tiếp theo!

*Màn hình: recap toàn tuyến 1→7 + 3 pin phụ, timeline mini "Sáng → Tối", logo Hinton Media, disclaimer.*

**Tổng: 28 + 24 + 56 + 49 + 40 + 49 + 37 + 39 + 46 + 23 = 391 âm tiết.**

---

## Bảng nguồn (places.json / research.md, fetch 2026-10-05)
| Điểm | Quán (địa chỉ) | Sao / review dùng | Nguồn số | Giá dùng | Giờ dùng | Mô tả món (nguồn) | Bong bóng (quote gốc → dịch) |
|---|---|---|---|---|---|---|---|
| ① | Bún cá miền duyên hải (227 Văn Cao, An Khê, Ngô Quyền) | 4.5 / 360 → "hơn ba trăm rưỡi" | Exa (Google-derived), conf medium | 35k **chỉ trong quote** (places: "khoảng 35.000đ/bát đặc biệt (quote Exa)") | "mở bữa sáng từ sáu giờ" (Exa 06:00–13:00) | bún cá cay (places dish); "cá giòn" từ review Exa ★4 "the fish is crispy" | Thực khách ★5 Exa: "Generous serving for 35k I loved it!" → "Phần ăn đầy đặn so với 35k, mình rất thích!" (**VO quote 1**) |
| ② | Bánh Mỳ Cay Bà Già (57A Lê Lợi, Máy Tơ, Ngô Quyền) | 4.3 / 292 | Exa | 3k chỉ trong quote | Không (Exa vs Foody lệch) | bánh mì que, pate, tương ớt (research); "nướng giòn" (Foody) | Anon ★5 Exa: "Best Banh My Cay in town, I think. 3k each." → "Bánh mì cay ngon nhất phố, theo tôi. 3k một chiếc." (**VO quote 2**) |
| ③ | Quán Nga Nem Cua Bể (92 Trần Nhật Duật) | 3.9 / 757 | Exa (haiphongreview ~849) | Bỏ (blog) | Bỏ (lệch) | nem cua bể + bún, thịt nướng (research); "gần Nhà hát Lớn" (research) | Anon ★5 Exa: "Nem cua be fresh, hot, crunchy, filled with crab." → "Nem cua bể tươi, nóng, giòn, đầy cua." |
| ④ | Bánh đúc tàu Cô Chuyền (159 Hai Bà Trưng, An Biên, Lê Chân) | 4.4 / 198 | Exa/Google (Maps UI xác nhận 4.4) | 12–20k/bát "tham khảo" (VnExpress 2023; toididau ~15–20k) | "trước năm giờ chiều" (06:30–17:00, Exa/Google + toididau khớp) | tôm–thịt–đu đủ + nước mắm giấm (research) | Tran N. Y. ★5 toididau: "Ăn lạ lạ mà cũng rất ngon. Một bát 15k." (giữ nguyên) |
| ⑤ | Bánh Đa Cua Bà Cụ (179 Cầu Đất) | 3.8 / 1.771 | RestaurantGuru (Exa ~1.512) | Bỏ (blog 40–80k) | Không đọc (07:00–21:00) | bánh đa cua bể, nem cua (research) | Anon ★4 Exa: "Good crab springrolls and bun da cua. Enjoyed the food." → "Nem cua và bánh đa cua ngon, ăn rất thích." |
| ⑥ | Lẩu Cua Đồng Đất Cảng (22 Dư Hàng, Lê Chân) | 4.9 / 287 → "gần ba trăm" | Exa/Google, **conf medium** (Toplist cảnh báo ưu đãi review; trước ghi 4.0/59) | Bỏ (nguồn lệch) | "mở tới mười giờ rưỡi tối" (Exa/Google 10:00–22:30; Toplist khớp) | lẩu cua đồng (places); "nước cua đậm đà" ← Exa "Great crab broth" + Tadiha "1 nồi đậm đà" | Anon ★5 Exa: "Great crab broth" → "Nước dùng cua tuyệt vời." |
| ⑦ | Sủi dìn chè nóng Cô Út (163 Cầu Đất) | 4.4 / 205 | Exa | ~10–15k/bát (Exa / HPBook) | "từ ba giờ chiều" (Exa + HPBook khớp giờ mở) | sủi dìn, chè vừng / chè đậu nóng (research) | Anon ★5 Exa: "The best sui din! Syrup is not sickening sweet." → "Sủi dìn ngon nhất! Nước đường không quá ngọt." |

Pin phụ (OSM Nominatim, không sao/review): Nhà hát Lớn HP (20.857122, 106.681811), TTTM Chợ Sắt (20.855849, 106.67095 — xấp xỉ khu vực), Avani Harbour View (20.864069, 106.689622).
Claim suy từ chính data tuyến (không thêm nguồn ngoài): "khởi động hơi xa trung tâm" (Văn Cao lệch đông-nam, de-xuat-tuyen-moi caveat); "phần lớn tuyến ăn nằm quanh trung tâm" (6/7 điểm trong cụm Lê Lợi–Cầu Đất–Hai Bà Trưng–Dư Hàng); "nhiều đánh giá nhất tuyến" (Bà Cụ 1.771 > Nga 757 > Bún cá 360 > Bà Già 292 > Lẩu 287 > Cô Út 205 > Cô Chuyền 198); "ngay sát Bà Cụ" (163 & 179 Cầu Đất, research "rất sát"); mốc "Gần trưa / Chiều xuống / Tối đến" là nhịp kể chuyện, không phải giờ mở cửa.
**Chủ động KHÔNG dùng:** "cao nhất tuyến" cho Lẩu; giá lẩu; tuổi quán / "500 bát/ngày" / "Sở Du lịch đưa vào bản đồ" (Cô Chuyền); giá blog Nga & Bà Cụ; giờ Bà Già & Nga (lệch nguồn); giờ đóng Bún cá 13:00 chỉ trên màn, không đọc; không Michelin.

## Danh sách [CẦN QA]
1. **2 quote VO có giá trong lời review** — Bún cá "35k" và Bà Già "3k" đều là 1 review qua Exa, đọc như *lời trích*, không như giá niêm yết. Nếu bố muốn thay quote Bún cá bằng "Nước dùng ngon, cá giòn." (Exa ★4 "Soup is good, and the fish is crispy.") thì VO đổi thành "Một thực khách viết: nước dùng ngon, cá giòn!" (−8 âm tiết → 383, vẫn trong 380–400) và **bỏ** "cá giòn" ở câu mô tả để khỏi lặp (−2 → 381).
2. **Lẩu Đất Cảng 4.9★ / 287** — confidence medium; Toplist cảnh báo quán có ưu đãi khi review Google, trước ghi 4.0/59. VO chỉ "khoảng bốn phẩy chín sao", không khen nổi bật. Bố cân nhắc có giữ sao trên màn không (bỏ câu sao: −11 âm tiết → 380, vẫn đạt sát đáy).
3. **Giá lẩu** — không đọc/hiện vì Tadiha "nồi ~120k" vs Toplist "~200–300k/người tùy gọi thêm". Nếu bố muốn: màn hình "💵 nồi lẩu tham khảo ~120k (Tadiha)", không đổi VO.
4. **Nhãn "Review Google Maps (dịch)"** cho quote Exa (Google-derived, trung gian), không đọc từ Maps UI gốc — giữ quy ước v1 bố đã duyệt.
5. **Bún cá miền duyên hải** — dữ liệu Exa conf medium; places ghi "popular times còn hiện tối — giờ Exa đến 13:00; xác minh lại lúc quay". VO chỉ nói "mở bữa sáng từ sáu giờ" (an toàn); màn hình 6:00–13:00.
6. **Giá Cô Chuyền 12–20k** — VnExpress 2023 (toididau ~15–20k); VO nói "giá tham khảo". Giờ đóng 17:00 (Exa/Google + toididau khớp) → "nhớ ghé trước năm giờ chiều".
7. **"nhiều đánh giá nhất tuyến"** (Bà Cụ) — là số đếm, không xếp hạng chất lượng; bố đã duyệt ở v1. Muốn bỏ: −5 âm tiết → 386.
8. **Count lệch nguồn** — Bà Cụ 1.771 (RG) vs ~1.512 (Exa) → "gần một nghìn tám trăm" theo số bố chọn; Nga 757 vs ~849 → "hơn bảy trăm năm mươi" phủ cả hai.
9. **Tile cache Bot2** — pin Bún cá (20.834096, 106.701893) rơi vào tile z16 (52192, 28888), **ngoài** cache hiện tại (y 28880–28887) → cần tải thêm hàng y 28888–28889 (x 52186–52193).
10. **Thời lượng** — 391 âm tiết ≈ 85s @4,6/s + end card 2,5s ≈ 88–90s. Timestamp ước tính; căn lại theo SRT thật sau TTS.

## Handoff
`JOB|Chờ QA|v2|/workspace/video-jobs/MAP-FOOD-HP-01|next=bố` — VO **391 âm tiết** (~85–87s @1.2, tổng ~90s), 7 điểm đúng thứ tự chốt, 2 quote đọc trong VO (Bún cá 35k + Bà Già 3k), 7 bong bóng trên màn.
