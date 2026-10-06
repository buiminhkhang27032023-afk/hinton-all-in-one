# KIẾN THỨC LÀM VIDEO & EDIT — Hinton Media (bố của các bot + các bot con)

Tổng hợp ngày 05/10/2026 (ICT). Toàn bộ nội dung lấy từ các file trên box, không thêm gì ngoài file:
`/workspace/hinton-pipeline-docs/` (gồm `edit-video/`), `/workspace/video-learn/`, `/workspace/video-jobs/` và skill `hinton-edit-video`.
Ký hiệu bot phụ trách: **[Bố]** = bố của các bot (điều phối, QA script) · **[B5]** = Bot 5 Săn tin · **[B4]** = Bot 4 Douyin · **[B3]** = Bot 3 Biên kịch · **[B2]** = Bot 2 Tin AI (render) · **[B2B]** = Bot 2B Douyin (render) · **[TLE]** = Trợ Lý Edit Video · **[Chung]** = áp dụng cho mọi bot.

---

## 1. Quy trình tổng & phân vai bot

### 1.1 Roster (BOTS.md, tạo 03/10/2026, ID đã cập nhật 05/10)
| Bot | Vai |
|---|---|
| bố của các bot | điều phối, QA script. Không tự gọi mình là Bot1, không tự render nếu không được giao, giao việc chứ không làm thay |
| Bot 5 — Săn tin và kiến thức AI | săn tin / kiểm chứng. Không viết, không render |
| Bot 4 — Douyin | tải + transcript + dịch Douyin. Không viết script cuối, không render |
| Bot 3 — Biên kịch | viết script. Không render, không tự xác nhận fact còn thiếu |
| Bot 2 — Tin AI | render nhánh Tin AI (local-only). Không tự sửa claim |
| Bot 2B — Douyin | render nhánh remix Douyin (local-only). Không chép nguồn, không tự sửa claim |
| Trợ Lý Edit Video | ngoài pipeline 5 bot. Dựng video MỚI từ kịch bản + footage bằng pipeline `AI-auto-generate-video` preset `varun` (BOTS.md ghi "công thức Cường Mê AI"; skill/hướng dẫn mới hơn ghi kiểu Varun Mayya, ưu tiên mẫu kênh nước ngoài). Bố nghiên cứu tài nguyên anh gửi rồi giao; chưa có file thì không giao |

### 1.2 Luồng (luong-toi-uu.md, hinton-orchestrate)
- **Tin AI:** bố → Bot5 (tìm) → bố chọn 1 → Bot3 → bố QA → **Bot2** → bố trả anh.
- **Douyin (link/file):** bố → Bot4 → Bot5 (verify claim AI) → Bot3 → bố QA → **Bot2B** → bố trả anh.
- Hai nhánh chạy song song được (Bot2 vs Bot2B); cùng một job không để 2 bot viết/render trùng. [Bố]
- **Edit video theo tài nguyên anh gửi:** bố nghiên cứu → giao Trợ Lý Edit Video → TLE báo lại bằng phiếu (anh nhắn thẳng TLE thì TLE làm luôn). [Bố][TLE]

### 1.3 Quy ước vận hành [Chung]
- Mã job `HM-NNN` hoặc slug; thư mục `/workspace/video-jobs/<job-id>/{source,lam-viec,output,qa}/`. [Bố]
- Phiếu 1 dòng cho mọi bàn giao: `JOB|status|version|path|next` (vd `HM-009|Đang sản xuất|v3-60s|/workspace/video-jobs/hm-009-adobe-chatgpt|next=bố`).
- Status chuẩn: `Đã nhận → Đang xử lý nguồn → Đang viết → Đang sản xuất → Đang kiểm tra → Hoàn thành`; lỗi/chờ anh = `Bị chặn`.
- Sửa tối đa **2 vòng/bước**, quá thì bố báo anh kèm phần đã có.
- Ai nói gì: Bot4/5/3 gửi path + tóm tắt ngắn (không dump transcript); Bot2/2B gửi path mp4+wav+srt + size + duration + 1 câu QA giọng; bố → anh chỉ milestone + link cuối, không spam ack.
- Mặc định phiếu (khỏi hỏi lại): ~60s · 9:16 · 1 giọng OmniVoice male clone v2 @1.2 · SRT sidecar · không burn karaoke trừ khi anh hỏi · không BGM · local-only · Hinton remix · không quảng bá kênh TQ · Drive chỉ khi giao.
- Giao video: file 720p + 1 dòng chủ đề + thời lượng; dùng Google Drive connector gom video của batch vào 1 folder (khi giao). [Bố]
- Xưng hô với user: gọi "anh", xưng "em"; không xưng "bố" với anh.
- Chọn chủ đề: đang hot ở nước ngoài hoặc trên YouTube lượt xem cao, không trùng nội dung đã làm. [Bố]
- Tối ưu token (token-optimize.md): lead kết quả; path + tóm tắt; 1 tin = status|version|paths|next; sửa = diff; ack im hoặc priority false; local trước, web khi cần; executor chỉ khi >2 vòng tool; memory 1 câu; transcript chỉ ghi [KHÔNG RÕ] + claims.

### 1.4 Thể loại & format (genres-formats-ui.md)
- **Genre:** G01 Tin AI breaking (24–72h) · G02 Tool demo/Ads AI · G03 Tips thực chiến (SME/sale/creator) · G04 Listicle Top N · G05 Storytelling dài · G06 Talking-head/multi-clip · G07 Douyin remix VN · G08 Bug/lỗi + cách sửa (chỉ khi anh yêu cầu) · G09 So sánh A vs B · G10 Stat/benchmark (1 con số hero).
- **Format:** F01 HyperFrames neon UI · F02 FFmpeg kinetic cards (chỉ fallback) · F03 B-roll + VO · F04 Talking-head editor (hinton-ai-editor-agent) · F05 cặp xuất mobile 720×1280 (luôn kèm khi giao). Ưu tiên F01 → F04 → F03 → F02.
- Template HyperFrames: hook `frame-liquid-bg-hero`/`frame-bold-poster`; thân `frame-glitch-title`, `frame-build-minimal`, `frame-pentagram-stat`, `frame-vignelli`, `frame-aicoding-list`, `frame-aicoding-comparison`, `frame-creative-voltage`; outro `frame-statement-outro`/`frame-logo-outro`. 8–12 scene, đổi template mỗi 1–2 scene. G09 phải có ≥1 scene `aicoding-comparison`.
- QA ghi Genre ID + Format ID + chuỗi QA giọng. [B2][B2B]

---

## 2. Nghiên cứu / săn tin

- **[B5] Tin AI:** tìm tin mới ưu tiên 24–72h từ nguồn đáng tin: tiêu đề, ngày, URL, claim chính, mức chắc chắn. Đối tượng: chủ DN, sale BĐS, nhà sáng tạo.
- **[B5] Douyin:** kiểm claim AI trong nguồn Bot4, đối chiếu nguồn độc lập khi có thể.
- **[B5]** Tách fact / suy luận / chưa rõ; chưa xác minh ghi `CHƯA XÁC MINH`. Không bịa tin/số/quote/ngày/URL/tên sản phẩm; không gọi thông tin nhớ sẵn là "tin mới" nếu thiếu web/X.
- **[B5] Output:** path file research + bảng `job_id | topic | claim | source_url | published_at | verified_by | confidence | caveats | next`.
- **[B4] Douyin:** tải video nếu được phép (không được thì ghi hạn chế, dùng file/link có sẵn) → transcript tiếng Trung có timestamp, chỗ không rõ ghi `[KHÔNG RÕ]` → bản dịch **ý nghĩa** tiếng Việt (không chép nguyên) → SRT sidecar timing kiểm được. Không bịa thoại, không xoá claim chưa rõ, không burn phụ đề, không TTS.
- **[B4] Cách tải Douyin:** Edge headless chế độ khách trên PC của anh (DESKTOP-VHMVQSR): `cd $env:USERPROFILE\hinton-douyin; .\venv\Scripts\python.exe grab.py <ids>`, rồi copy file vào `/workspace/video-jobs/<job>/source`. (yt-dlp trên box bị Douyin chặn, cần cookie.)
- **[B4]** Máy thiếu RAM: không chạy whisper large/medium, lấy lời gốc từ phụ đề cứng.
- **[TLE][Bố] Lấy dẫn chứng/footage (DAN-CHUNG-FOOTAGE.md):**
  - Key visual trước, viết lời sau (Kallaway): không có hình "nhìn là hiểu" cho hook thì cân nhắc bỏ ý tưởng.
  - Mỗi claim → 1 bằng chứng hình trong ≤1 giây kể từ lúc đọc.
  - Thứ tự ưu tiên cho 1 câu: clip demo chính thức > tự quay thử > demo cộng đồng > ảnh chụp tin/tweet có zoom > chart tự vẽ > stock > chữ động.
  - Nguồn: X chính thức các hãng (@OpenAI, @AnthropicAI, @GoogleDeepMind…), YouTube kênh hãng, blog/product page; chart từ blog, model card HF, arXiv; demo cộng đồng từ X, Reddit (r/singularity, r/LocalLLaMA), GitHub README, Product Hunt; stock Pexels/Pixabay/Mixkit (cần API key).
  - Công cụ: `yt-dlp --download-sections`, Chrome headless chụp trang, `gallery-dl`, ghi nguồn nhỏ "Nguồn: …".
  - Douyin dịch lại: giữ footage trung tính (demo/chart/UI); thay/che mặt người dẫn TQ, chữ Hán, logo/QR/watermark; tìm bản gốc nét hơn từ X/YouTube/GitHub/trang hãng; che chữ bằng dải tiêu đề Việt (ưu tiên hơn blur).
- **Kho nghiên cứu kênh:** 16 kênh (80 video vòng 4 + 43 video 8 kênh mới) đo bằng ffmpeg/OpenCV/RapidOCR/faster-whisper small; breakdown ở `/workspace/video-learn/<kênh>/<id>_breakdown.md`; công cụ `video-learn/tools/` (analyze.py, transcribe.py, script_analyze.py, footage_stats.py, dem_am_tiet.py, fx/phone_frame.py, news_card.py, bar_chart.py). Thêm khảo sát Cường Mê AI (94 video metadata), diễn đàn (Reddit, Skool Kallaway, YouTube VN/TQ), và repo GitHub (REPO-AI-VIDEO.md: shortlist HyperFrames, whisperX, MoneyPrinterTurbo-module footage, PySceneDetect + yt-dlp, auto-editor; bỏ hẳn nhóm lip-sync; model sinh video mở đều cần GPU nên không chạy được trên box).

---

## 3. Kịch bản (hook, âm tiết, cấu trúc) — chủ yếu [B3], bố QA

### 3.1 Độ dài
- Giọng nam clone @1.2 ≈ 4,6 âm tiết/giây (voice-lock) → **250–270 âm tiết ≈ 55–60s**; >~280 âm tiết sẽ vượt 60s. Đo thật: 54s, 52s, 59s.
- Số đo kênh VN: 4,26–4,55 âm tiết/s, khớp mục tiêu. Kịch bản dịch từ tiếng Anh phải **cắt 15–25% ý**, không nói nhanh hơn.
- Ngân sách theo thời lượng: 30s = 125–135 âm tiết · 60s = 250–270 · 90s = 380–400.
- Đếm: `python3 /workspace/video-learn/tools/dem_am_tiet.py script.txt` (ChatGPT = 4, AI = 2, OpenAI = 4…).

### 3.2 Khung bắt buộc của Bot3
`HOOK → bối cảnh → 2–4 ý chính → bằng chứng/nguồn → ý nghĩa → CTA`, câu ngắn, hook mạnh 0–3s, đánh dấu `[CẦN QA]` cho claim/số/tên riêng thiếu nguồn, không thêm tin ngoài research, remix (không copy câu chữ/cấu trúc Douyin), CTA hướng Hinton hoặc trung tính. Bảng cảnh: `thời gian | lời thoại | hình ảnh | chữ trên màn | âm thanh`. Output `storytelling_script.txt`.
Luồng kể mặc định (G01–G05, G07): HOOK → bối cảnh → vấn đề → diễn biến → cao trào → kết quả → bài học/CTA.

### 3.3 Hook (SO-TAY-KICH-BAN)
- Không kênh nào để im lặng ở đầu: VO bắt đầu ở khung 0; 3s đầu ≈ 12–14 âm tiết.
- Câu 1 ≤16 âm tiết, xong trước 3,5s, có **tên riêng hoặc con số**; câu 2 (bẻ lái/báo trước) xong trước 6s.
- Chữ hook trên màn 3–5 chữ, không chép nguyên câu VO; hiểu được khi tắt tiếng. Không mở "Hôm nay mình sẽ…".
- Hình 0–1s phải là thứ đang được nói tới (logo/tiêu đề tin/kết quả demo), không phải stock chung chung.
- Khung lý thuyết: 6 kiểu hook Kallaway (Fortune Teller, Experimenter, Teacher, Magician, Investigator, Contrarian); 3 bước Context Lean → "nhưng" → Contrarian Snapback; "đồng hồ 4 giây"; Jenny Hoyos (hook ≤3s, hiểu khi tắt tiếng, viết câu cuối trước, cắt 1s cuối tăng retention 83→88%).
- 8 mẫu hook: H1 "[Hãng] vừa [làm X] — nhưng [hệ quả]" · H2 "[Hãng] vừa giải/làm được điều không tưởng" · H3 người thường + AI + kết quả phi lý · H4 mẹo "bẩn" vừa viral + mình đã thử · H5 kết quả trước ("một tấm ảnh, mười mẫu quảng cáo…") · H6 "Đừng trả tiền cho X nữa" · H7 bằng chứng số view · H8 "N cấp độ/N bước".
- Douyin: đổi ngôi thứ nhất → thứ ba ("Một lập trình viên Trung Quốc vừa…").

### 3.4 Thân bài & giữ chân
- Bẻ lái "nhưng" là chỗ tạo khác biệt (kênh EN 0,68–2,8 lần/phút, kênh VN gần 0): ≥2 lần trong thân, khoảng 1 lần/13–20s. Câu mẫu: "Nhưng đó chưa phải phần điên rồ nhất", "Điều đáng nói không phải X, mà là Y", "Cho tới tận bây giờ", báo trước số điểm, "Và đây là phần mình thích nhất", "Mình đã thử…", so sánh đời thường, con số cụ thể giữa câu mỗi 10–15s.
- 60s: **3 điểm là trần** (mỗi điểm 9–12s); 7 điểm chỉ khi mỗi điểm là 1 câu mẫu lặp (Hiếu: 7 lệnh/40s).
- Câu hook ≤16 âm tiết, câu thân 8–14, không câu nào >20.
- ≥3 con số cụ thể đã kiểm chứng; thuật ngữ giải thích bằng câu đời thường (độ khó "lớp 5").
- "bạn" ≤3 lần/phút trong dạng tin, dồn vào đoạn "ý nghĩa với bạn" gần cuối (Varun 0 lần vẫn top).
- Hướng dẫn: kết quả trước, gói ≤3 bước, không đọc từng nút bấm.

### 3.5 Template theo dạng (60s)
- **A — Tin AI (mặc định):** 0–3 hook · 3–6 bẻ lái · 6–14 bối cảnh + 1 bằng chứng hình · 14–24 điểm 1 + số + demo · 24–34 điểm 2 + "chưa phải phần điên rồ nhất" · 34–44 điểm 3 + chart · 44–52 twist/hạn chế (giá, ai chưa dùng được) · 52–60 ý nghĩa + kết.
- **B — N công cụ/lệnh:** kết quả đẹp nhất + "N cái này làm được X" → "cái thứ N mới đáng sợ nhất" → mỗi mục 1 câu mẫu → mục cuối mạnh nhất → CTA lưu/comment.
- **C — Hướng dẫn ≤3 bước:** kết quả trước → vì sao đáng làm → bước 1–3 → trước/sau → link/lệnh ở bình luận.
- **D — Douyin dịch lại:** bỏ chào hỏi/"下次见/关注"/handle kênh TQ → đổi ngôi → ép về 3 điểm → viết lại hook H1/H3/H5 → thêm 1 câu bối cảnh VN (dùng được ở VN không, miễn phí không, có tiếng Việt không) → cắt (秋芝 trung vị 194s → 60s là bỏ ~70%) → đếm lại âm tiết.
- CONG-THUC-HINTON có bảng 60s từng giây (261 âm tiết, ~24–28 lần đổi hình) theo mẫu gốc Varun R2nesxy7uYU.

### 3.6 Kết / CTA
Câu hỏi mở (Varun) · câu kết vòng về hook (Kallaway 43,1M) · hỏi ý kiến · comment từ khoá (chỉ khi có người trực inbox gửi link thật) · "Lưu lại" (dạng N lệnh) · follow ≤12 âm tiết. CTA ≤1 câu (≤3s), cắt sát sau chữ cuối, không "cảm ơn đã xem", không CTA kênh TQ. Tin AI dùng kết câu hỏi/câu chốt, không CTA bán hàng.

### 3.7 Checklist QA kịch bản (chạy trước TTS) [Bố]
250–270 âm tiết · câu 1 ≤16 âm tiết có tên riêng/số · bẻ lái trước giây 6 · ≥2 lần "nhưng" · mỗi claim có `[HÌNH: …]` · ≥3 con số đã kiểm chứng · không câu >20 âm tiết · "bạn" ≤3/phút · kết ≤1 câu · đọc to 1 lần ở tốc độ 1.2 · tên riêng thống nhất với phụ đề. QA của bố: nguồn, claim, hook, remix, CTA, ~60s.

---

## 4. Dựng / edit

### 4.1 Công thức Varun (preset `varun`, chuẩn hiện tại của [TLE]) — QUY-TRINH-VARUN.md + skill hinton-edit-video
- Mẫu: Varun Mayya "Claude Mythos…" R2nesxy7uYU (693K view, 64,3s). Chọn vì đúng thể loại tin AI, ~60s, mặt chỉ 24%, 89% footage, 35 lần chèn/phút, render local được, giọng kể ngôi thứ ba.
- Mỗi câu có 1–3 hình bằng chứng full-frame, mỗi hình 1–2s; mặt người dẫn chỉ ở hook, chỗ chuyển ý và cuối.
- **Chỉ tiêu QA (tự kiểm, trượt thì exit ≠ 0):** evidence full-frame ≥75% · mặt ≤25%, hook ≤3s, cách nhau 10–20s, shot cuối là mặt · insert ≥30/phút, mỗi insert 0,95–2,05s khớp câu đang đọc · ≥25 hình khác nhau/60s, mỗi hình dùng tối đa 2 lần · split 2 bằng chứng ≥2 lần, không mặt · mọi câu có ≥1 evidence (câu `[MẶT]` ≤3s được chỉ có mặt) · whip/zoom mỗi 4–6s · SFX ≤16/phút · −14 LUFS ±0,5, true peak ≤ −1 dBTP · 1080×1920 30fps + 720×1280 · safe zone · đủ glyph Be Vietnam Pro.
- Script: mỗi dòng 1 câu + cue `[HÌNH: …]` cuối dòng. Loại shot: `web` (ảnh chụp trong khung trình duyệt, OCR tô vàng/gạch chân/đóng khung đúng câu, zoom/pan vào dòng) · `phone` (bài X trong khung điện thoại) · `photo` (chân dung Wikimedia + lower-third) · `clip` (clip chính thức) · `render` (protein 3D từ PDB/AlphaFold) · `stat` (thẻ số liệu nền lưới đen ô đỏ) · `face` (mặt full khung, `big=` chữ to) · `split` (2 bằng chứng trên/dưới). Neo `@chữ` để mỗi mục dài 1–2s (mốc trong `lam-viec/words_tight.json`).
- Rải mặt: lần 1 ở hook, ~1 lần mỗi chuyển ý (đặt `face` làm mục đầu câu chuyển ý, kèm `big=` nếu là câu hỏi), lần cuối là shot cuối; không dồn mặt về cuối.
- Mẹo: ảnh tĩnh cũng khai trong `broll_urls.txt`; trang nền tối dùng `/underline` hoặc `/box`; trang paywall thì lưu HTML bằng curl rồi chụp local; câu 2s chỉ chứa 1–2 hình (nhồi sẽ ra insert <1s).
- Bằng chứng: câu trích phải khớp OCR (OCR đọc "AI" thành "Al"); X chụp qua embed `platform.twitter.com/embed/Tweet.html?id=`; Wikimedia nghỉ 3s giữa các lần tải, ghi credit đúng giấy phép; YouTube cần `--js-runtimes node --remote-components ejs:github`; số trong `stat` phải đã kiểm chứng; mỗi shot có `credit` → `CREDITS-<sub>.md`.
- QA tự động không thay mắt: xem ảnh so sánh 24 khung với Varun + contact sheet (hình đúng câu, tô vàng đúng dòng, phụ đề không che chữ chính, split rõ 2 nửa).

### 4.2 Preset Kallaway (TEMPLATES.md) — tin AI nhịp nhanh, split B-roll/mặt
- Tham chiếu Kallaway 7645299083573267742 (cắt/phút 23,9/29,7; shot trung vị 1,56s; cắt đầu 1,17s; caption 2 chữ/cụm #DFAD12; −14,4 LUFS).
- Bố cục S: B-roll 1080×960 trên, mặt dưới (push-in 3%/s); bố cục F: full face zoom 1,15/1,20 + 1 chữ to. Nhịp shot 1,7s (0,9–3,2s), cắt đúng đầu từ, F mỗi ~6,5s, shot cuối loop về shot đầu.
- Caption Fraunces Black 50px #E0AC1A viền đen, 2 chữ/cụm, pop 5 frame; chữ to Be Vietnam Pro Black 190px; tiêu đề hook 2 dòng IN HOA, wipe 1,2s, giữ 2,4s.
- Sfx whoosh/hit/pop/scan (~25–30% cắt có sfx); nhạc −18…−20 dB, ngắt nhạc 0,6s trước câu "Nhưng/Tệ hơn/Vì sao…"; cắt mọi khoảng ngừng >0,2s về 0,2s; −14 LUFS, TP −2,0.
- File phụ: `bigwords.txt` (chữ to), `caption_map.txt` (số hiển thị), `beats.json`. Gap còn lại: chưa có PIP mặt tròn và mockup điện thoại 3D; caption hơi to/tối; B-roll động phụ thuộc nguồn.

### 4.3 Công thức Cường Mê AI (CONG-THUC-EDIT.md, BRIEF.md) — học phong cách, không reupload
- Kênh @caocuongvuai: 94 video (22/3–28/9/2026), ~119,3K follower; tiếng Việt thân mật "ae/anh em"; chủ đề agent/automation, Claude/Claude Code, tip ChatGPT/Gemini, tin nóng, tiết kiệm chi phí; độ dài trung vị 1:28.
- Hook 0–2s: claim, nỗi đau hoặc con số ("X10", "thứ 3", "5 mã"); split graphic/B-roll trên – mặt dưới, hoặc mặt full + chữ claim.
- Hình: người nói ngực trở lên cầm mic, nói liền; jump cut + zoom mặt theo câu; cut-out trên gradient đào/trắng; caption karaoke sans trắng highlight cam từng từ; mock UI, icon 3D, flowchart, logo tool; nhạc synth dưới giọng.
- Cấu trúc: hook claim → tool/tin → workflow/listicle/ví dụ → lợi ích → CTA (bio, lưu, comment, follow) → outro logo tròn.
- Không làm: video ngang, interview 2 người, nền trắng tối giản, intro dài trước claim; không copy footage/audio/logo kênh gốc.

### 4.4 Cut rate / nhịp (SO-TAY-DUNG)
| Dạng | Shot trung vị | Cắt/phút | Cắt đầu | Punch-in |
|---|---|---|---|---|
| Tin AI nóng | 1,6–2,0s | 20–30 | ≤1,6s | ×1,10–1,20 mỗi 6–10s, push 2–3%/s |
| Top N / listicle | 2,0s (cho 10–15% shot <0,5s) | 15–25 | ≤3,6s | ×1,15–1,30 |
| Lệnh → kết quả | 1–2s (lệnh) + 2–5s (kết quả) | 8–12 | ≤2,3s | luân phiên 100% ↔ 115–125%, Ken Burns 5% |
| Hướng dẫn thật | 4–12s | 3–5 | 4–6s | không |
- Jump-cut cùng khung là "xương sống"; punch-in chỉ ~5% điểm cắt. Khi punch giữ mắt cùng vị trí. Chọn nhịp theo dạng nội dung, đừng cắt nhanh chỉ để nhanh. Talking head tĩnh >10–15s thì chèn pattern interrupt. Ảnh tĩnh luôn có chuyển động; không để hình tĩnh đứng >3s.
- Hard cut là chính; hiệu ứng (zoom-blur, glitch 0,2s ở chữ "Nhưng", whoosh) tối đa 1–2 lần/video.

### 4.5 B-roll
- Tin AI 60s: ≥20–28 lần đổi hình (Varun 35/phút, Kallaway 21,4/phút); loại footage số 1 là **ảnh chụp tài liệu chính thức có highlight đúng câu đang đọc**.
- "Kết quả trước" là footage mạnh nhất cho video công cụ (Đình Hán 4,8M, Adam 2,7M).
- Kênh không mặt dùng full khung + card chữ, không cần split.
- Fallback khi thiếu footage F1–F12: chữ động pop · Ken Burns ảnh chụp tin · zoom vùng + khung highlight · news card dựng lại · mockup điện thoại/khung trình duyệt · glitch 0,2s · chart tự vẽ (`bar_chart.py`) · lưới logo pop · clip ngang → dọc nền mờ · tier list lấp dần · ảnh AI minh hoạ (ghi "Ảnh minh hoạ AI") · slide checklist "lưu lại". Cứ 2–3 hình tĩnh thì xen 1 clip động thật hoặc F6/F7.
- 12 món cherry-pick (CONG-THUC-HINTON): khung Varun · ảnh blog highlight · hook + bẻ lái giây 5 (Kallaway) · kết vòng/câu hỏi mở · chữ hook 2 dòng (Jeff Su) · glitch ở "Nhưng" · kết quả trước (Adam, Đình Hán) · "3 điểm" báo trước (AI Savvy) · clip launch + chart + meme 1s (秋芝) · khung đỏ/mũi tên (NTK, Đình Hán) · logo pop (Brand Nat) · CTA comment từ khoá (tuỳ chọn).

### 4.6 Caption
- Quy tắc: 2–3 chữ/lần (tin nhanh 2, punchy 1, hướng dẫn tối đa 4–5), ngắt theo nghĩa, mỗi câu tối đa 1 từ màu nhấn, màu nhấn thống nhất cả kênh; mỗi cụm 12–27 frame (trung vị 18), nối liền nhau; animation vào ≤6 frame (pop 80→108→100%).
- Font sans đậm đủ dấu Việt (Be Vietnam Pro Black, Montserrat ExtraBold, SVN-Gilroy Heavy), 56–64px, trắng viền đen 6–8px.
- Vị trí: y≈980–1060 khi split (ngay dưới đường chia 960); y≈1190–1400 khi full khung. Safe zone: không chữ ở y<150, y>1590, x>940.
- Chữ to một từ 150–230px ở y≈1100–1200, kèm bass hit. Tiêu đề hook 2 dòng IN HOA 3–5 chữ, hiện xong trước 1–2s.
- Font Be Vietnam Pro không có `β` và `→`: viết "Beta-" và "đến".
- **Mặc định pipeline 5 bot: KHÔNG burn caption** (chỉ SRT sidecar). Preset varun/kallaway của TLE thì burn caption. Có burn hay không là quyết định của anh (xung đột X1 trong CONG-THUC-HINTON).

### 4.7 Mặt người
- Hinton mặc định không lộ mặt / mặt chỉ là PIP từ clip quay sẵn, **không lip-sync** (đã bỏ hẳn nhóm LivePortrait, Wav2Lip…). File: `/workspace/hinton-pipeline-docs/assets/presenter-video-novoice.mp4` (có video thì dùng video, không thì ảnh `presenter-photo.jpg`).
- Kiểu Varun: mặt ≤25%, 10–20s một lần. Kiểu Kallaway: split mặt dưới ~55%, full face ~25%, mắt ở y≈1230–1290.
- PIP: tròn 260–300px góc trái trên (Kallaway), vuông 210px góc phải trên (NTK, né cột phải x≤920), tròn 211px góc trái dưới (Hiếu); dùng cho đoạn demo >4s.
- Douyin: thay scene người dẫn TQ bằng ảnh chụp tin, chữ động, mockup, hoặc giữ ≤1s nếu là phản ứng.

---

## 5. Giọng đọc & âm thanh

- **Khoá giọng [B2][B2B][TLE]:** OmniVoice local `http://127.0.0.1:8123`; giọng **nam clone v2** (`/workspace/omnivoice-server/voice-lock-vn-v2.wav` 8,9s 48kHz mono, cắt 33,40–42,30s từ audio anh gửi + `.ref.txt`); speed **1.2** (từ 03/10, trước là 1.12); loudnorm ~−14 LUFS VO; health phải `voice_locked:true`.
- Chuỗi QA: `OmniVoice · male clone v2 locked · 1.2 · voice_locked:true`.
- Vì sao clone: `instruct` kiểu "male, moderate pitch" không khoá giọng — mỗi lần `/tts` lại ra một tông; clone + cùng `voice_clone_prompt` = 1 giọng cho mọi scene. Server bỏ instruct khi đã lock.
- Giọng nữ cũ đã bỏ (03/10); file `voice-lock-female-vn.*` giờ chỉ là symlink sang v2. Job HM-001…HM-025 dùng giọng nữ cũ; remake job cũ phải TTS lại toàn bộ scene, không trộn 2 giọng trong 1 video.
- Lệch giọng / `voice_locked:false` = FAIL → restart `restart.sh` (chạy trong lock với `flock -o`) rồi remake ≤2 lần rồi báo bố.
- Kiểm tra: `curl -s 127.0.0.1:8123/health`; server chết thì restart, đợi 1–4 phút.
- `voiceText` / script: số viết bằng chữ tiếng Việt, không emoji; cue `[HÌNH]` không được đọc.
- **Nhạc nền:** pipeline 5 bot mặc định KHÔNG BGM (chỉ khi anh đưa nhạc). Preset varun BGM −20 dB, kallaway −18…−20 dB (TLE). Kênh mẫu: Varun 97%, Kallaway 94% thời lượng có nhạc; nhưng Đình Hán 21% vẫn có video 4,8M → không BGM không phải rào cản lớn nếu nhịp hình đủ nhanh [SUY trong file].
- **SFX:** ~15–25% điểm cắt (Kallaway ~20%), không gắn whoosh cho mọi cắt; ưu tiên đổi layout (whoosh), chữ to (bass hit), đổi B-roll (pop/click), visual công nghệ (scan); hook 1–2 sfx; varun ≤16/phút. Dùng một bộ sfx thống nhất cả kênh.
- Ngắt nhạc 0,5–1s trước câu reveal rồi vào lại; tin nhanh cắt mọi khoảng ngừng ≥0,25s (pipeline tighten >0,2s về 0,2s); hướng dẫn giữ 10–15 khoảng ngừng/phút.
- Loudness xuất: **−14 LUFS, true peak ≤ −1 dBTP** (pipeline mix TP −2,0).
- Kết loop: câu cuối nối vào câu đầu; cắt sạch hơi thở cuối.

---

## 6. Kỹ thuật render / xuất / QA

- **Render lock [Chung]:** tối đa 1 render toàn box; bọc TTS + render trong `flock /workspace/video-jobs/.render.lock <command>`. Không cần lock cho viết script, research, QA script, tải Douyin. Kiểm tra `flock -n … true && echo free || echo busy`; giới hạn chờ `flock -w 3600`. KHÔNG xoá file lock. Lý do: box chỉ CPU, nhiều bot render cùng lúc làm 1 scene TTS mất >1000s.
- **Pipeline 1 lệnh** (`/workspace/AI-auto-generate-video`): `./run.sh /workspace/video-jobs/<JOB>` → tự flock, TTS OmniVoice (kiểm voice-lock), align WhisperX → SRT (gãy timing thì fallback faster-whisper), dựng (HyperFrames/kallaway/varun), `deliver.sh` 1080p + 720p, QA. [B2][B2B][TLE]
- Input job: `script.txt` (bắt buộc), `config.json` (`title`, `preset`, `presenter`, `captions_burn`, `bgm`, `output_subdir`, `version`…), tuỳ chọn `broll_urls.txt`, `screenshot_urls.txt`, `portraits.txt`, `caption_map.txt`, `bigwords.txt`.
- Đường cũ (playbook): HyperFrames `npm run pipeline -- <outputDir>/script.json` trong lock (Node 22 ở `~/.local/bin`), 8–12 scene; FFmpeg kinetic chỉ fallback; talking-head qua `hinton-ai-editor-agent`.
- **Spec xuất:** 9:16 **1080×1920** H.264/AAC yuv420p 30fps + bản `storytelling_mobile_720p.mp4` (720×1280).
- **Deliverables:** `storytelling_final.mp4` + `voice_storytelling.wav` + `subtitle.srt` + `storytelling_script.txt` + `qa/report.md`, `qa/ticket.txt`, `qa/contact_sheet.jpg`, `qa/pipeline.log`.
- Dựng bản mới: đổi `output_subdir` + `version`, không ghi đè bản cũ (voice, align, ảnh chụp, clip đều cache).
- **QA checklist render:** ffprobe 1080×1920 h264+aac, duration OK · voice_locked:true + male clone v2 · không bịa · không BGM/karaoke trừ khi được yêu cầu · report ngắn · phiếu handoff. TLE thêm `tools/varun_qa.py` (ĐẠT/KHÔNG ĐẠT) + ảnh so sánh 24 khung + xem bằng mắt.
- Tự đo lại video: cắt cảnh `ffmpeg … select='gte(scene,0.3)'`, loudness `-af ebur128`, khoảng ngừng `silencedetect`, phân tích đầy đủ `/workspace/.cv-venv/bin/python /workspace/video-learn/tools/analyze.py out.mp4`.
- **Job mẫu đã có:**
  - TEST-pipeline-001: 19,2s test, 78 âm tiết, ra 1080p + 720p (stock bị bỏ qua vì không có key Pexels/Pixabay).
  - EDIT-SELFTRAIN-01: tự học theo Kallaway 7645, so số đo từng vòng (DIEM-LECH.md).
  - EDIT-FULL-01 (AI giành Nobel Hóa học 2024): v3 preset kallaway 58,9s; **v4 preset varun QA 20/20** (evidence 89,4%, mặt 10,6%, 37,7 insert/phút, 40 hình, −14,0 LUFS). Là bản mẫu được duyệt.
  - EDIT-FULL-02 (OpenAI DevDay 2026 / dots / GPT-6.1 Sol): v1 52,5s, 248 âm tiết, QA 20/20 (evidence 85,1%, mặt 14,9%, 41,1 insert/phút).
  - HM-047 DoorDash đặt món bằng tin nhắn, 58s, giọng nam v2 (theo DA-HOC; không kèm file).

---

## 7. Kênh mẫu đã học (thư mục `/workspace/video-learn/`)

| Kênh (thư mục) | Bài học 1 dòng |
|---|---|
| Varun Mayya (youtube-VarunMayya) | **Mẫu gốc Hinton**: mặt chỉ ~24%, full-frame bằng chứng (blog tô đỏ, tweet, chart, lưới logo), 26,9 cắt/phút, shot 1,52s, ngôi thứ ba, kết câu hỏi/câu chốt |
| Kallaway (tiktokintl-kanekallaway) | Tin AI nhịp nhanh: split B-roll trên/mặt dưới, caption 2 chữ vàng, punch-in + 1 chữ to mỗi 6–10s, bẻ lái ~13s/lần, ngắt nhạc trước reveal, kết loop |
| Jeff Su (youtube-JeffSu) | Chữ hook 2 dòng to viền đậm; "zoom thay cắt" trên ảnh tài liệu; glitch RGB chuyển cảnh; meme kết |
| Adam.Digital (tiktokintl-adam.digital) | Kết quả trước (clip AI 0–4s) rồi mới vào UI; caption 1 từ trong hộp đen; CTA comment từ khoá bằng bong bóng comment giả |
| Brand Nat (tiktokintl-brandnat) | Đạo cụ vật lý (Lego) làm ẩn dụ; caption 1 từ trộn serif nghiêng; logo khách hàng pop cạnh người |
| Riley Brown (tiktokintl-rileybrown.ai) | POV build app, ít cắt; ô tiêu đề đen ở t=0 giữ ~10s; mockup điện thoại cho app mobile |
| Tommy Teja (tiktokintl-tommythings) | 1 cảnh talking head cố định + tier list lấp dần nửa dưới làm "vòng mở" suốt video |
| AI Savvy (facebook-aisavvy) | Split mặt dưới ~82%, caption 1 chữ cam; hook trước/sau chồng dọc; báo trước "3 nâng cấp lớn nhất"; pill "LINK IN BIO" |
| Nguyễn Tất Kiểm (facebook-nguyentatkiem) | Listicle nhịp nhanh, punch mạnh nhất (×1,19), caption IN HOA vàng, PIP mặt vuông góc phải trên, mũi tên đỏ, nút FOLLOW động |
| Hiếu AI (tiktok-hieuanca) | Cấu trúc "lệnh → kết quả": split gõ lệnh + pill lime → kết quả full khung Ken Burns; mỗi lệnh ~5,4s; mở bằng số view chứng minh |
| HungNPV (tiktok-hungnpv) | Hook selfie + ô claim trắng ở t=0 ("Đừng… nữa"), quay laptop bằng điện thoại, nhãn B1/B2; nhịp chậm vẫn giữ được nhờ chữ trên màn |
| Đình Hán AI (tiktok-dinhhanai) | Mở bằng demo kết quả (giọng hát AI, 4,8M view) rồi mới hướng dẫn; mũi tên + vòng click vàng; BGM thấp vẫn nhiều view |
| Lê Duy Hiệp – AI Hub (tiktok-leduyhiep.aihub) | Mẹo 20–40s: tier list nói nhanh ~3s/tool; slide checklist "lưu lại" ~1s/slide |
| Duy Luân Dễ Thương (tiktok-duyluandethuong) | Tự quay cầm thiết bị 1 cảnh liền ("Trên tay…"); hướng dẫn = screen record phóng to + PIP mặt |
| 秋芝2046 (douyin-qiuzhi2046, bản YouTube) | Talking head + demo 16:9, PIP tròn trái dưới, chip tag lime theo phần, clip launch + chart chính thức + meme 1s; hook "chờ 2 năm cuối cùng đã ra, miễn phí" |
| 程序员鱼皮 (douyin-chengxuyuanyupi, bản YouTube) | Caption Trung rất to giữa khung, đổi màu theo nghĩa; ảnh chụp chat/log làm bằng chứng ngay sau hook; kết câu hỏi |

Ngoài thư mục video-learn: **Cường Mê AI** (@caocuongvuai, chỉ metadata 94 video + xem 5 clip) — xem mục 4.3. Bản xem kỹ từng giây: Kallaway 7645 và Hiếu AI 7686 (`edit-video/xem-ky/`).

---

## 8. Bài học / lỗi đã gặp

Từ MEMORY-va-BAI-HOC.md và DA-HOC-20261003.md:
- Chạy ~25 bot cùng lúc làm máy load ~80, cạn RAM, tác vụ nền crash, tốn token → mỗi lần chỉ chạy vài bot. [Bố]
- Render một cái một lúc trong `flock`, chạy thẳng bằng Shell (nohup, nền), không dùng tác vụ nền. [B2][B2B][TLE]
- Thiếu RAM thì không chạy whisper large/medium; lấy lời gốc từ phụ đề cứng. [B4]
- QA gọn: đọc `storytelling_script.txt`, kiểm caveat, ghi `qa/notify.txt`, tự nhắn kết quả cho bot. [Bố]
- Giao: file 720p + 1 dòng chủ đề + thời lượng, không nhắn tiến độ thừa. [Bố]
- 250–270 âm tiết ra 52–59 giây (đo thật 54s, 52s, 59s). [B3]
- ID bot trong DA-HOC/MEMORY là account cũ, bỏ qua (BOTS.md có ID mới).
- ⚠ Mâu thuẫn trong file: MEMORY ghi "batch N video: tạo N bot tạm", còn DA-HOC (mới hơn) ghi "không tạo bot tạm, không Bot6 trong luồng, không chạy ~25 bot".

Từ job & log:
- EDIT-FULL-01 v4 lần chạy đầu KHÔNG ĐẠT 18/20: một câu thiếu hình bằng chứng; font thiếu glyph `→` → sửa xong ĐẠT 20/20.
- EDIT-FULL-02 v1 lần chạy đầu KHÔNG ĐẠT 16/20: 22 insert ngắn dưới 0,95s (nhồi hình), hai lần lên mặt cách nhau <10s, SFX 24/phút (>16), chữ to "CHƯA HẾT!" bị báo lỗi safe zone → sửa xong ĐẠT 20/20.
- EDIT-FULL-01 v3: Reuters/Guardian dính paywall/cookie khi chụp headless → không dùng, tìm bài đăng lại (vd Rappler).
- EDIT-SELFTRAIN-01: WhisperX (wav2vec2-VI) gãy timing ở câu có tên Latin (cắt đầu ra 0,50s) → thêm fallback faster-whisper; true peak −0,8 → chỉnh mix TP −2,0; caption hơi to/tối, nhạc liên tục 90% so với 94,5%, thiếu PIP tròn + mockup điện thoại 3D, B-roll toàn ảnh nên nhịp "tĩnh" hơn.
- TEST-pipeline-001: stock footage bị bỏ qua vì không có PEXELS_API_KEY/PIXABAY_API_KEY.
- YouTube trên box báo lỗi "n challenge"/403 nếu thiếu `--js-runtimes node --remote-components ejs:github`; phụ đề YouTube 429 thì chạy faster-whisper small trong flock.
- Lỗi cue hay gặp: `OCR phrase not found` (chép đúng chữ từ JSON OCR); insert <1s hoặc >2s (dời neo `@chữ`); "lặp nguồn" trượt vì 2 nửa split tính 2 lượt.
- Không bao giờ `pkill -f` theo mẫu có trong chính lệnh đang chạy; không xoá file lock.
- Douyin/Facebook: yt-dlp không tải/liệt kê được (cần cookie / không parse reel) → học qua bản đăng lại YouTube/TikTok.

---

## 9. Điều cấm

**Giọng [B2][B2B][TLE]:** edge-tts · NamMinh · giọng nữ cũ `voice-lock-female-vn*` (retired 03/10) · cloud TTS · tắt clone · instruct-only làm lock duy nhất · đổi ref giữa scene · seed/voice random · TTS không qua OmniVoice local · trộn 2 giọng trong 1 video · đổi voice form.

**Nội dung [B3][B4][B5][Bố]:** bịa tin, số liệu, quote, ngày, URL, tên sản phẩm, thoại · tự điền claim thiếu bằng suy đoán · thêm tin ngoài research · gọi thông tin nhớ sẵn là "tin mới" · xoá claim chưa rõ · copy nguyên câu chữ/cấu trúc Douyin · quảng bá kênh đối thủ/kênh TQ (kể cả logo kênh nguồn, handle, "下次见/关注") · hứa gửi link khi không có người gửi.

**Dựng/xuất mặc định pipeline 5 bot [B2][B2B]:** burn karaoke khi anh chưa yêu cầu · BGM khi anh chưa đưa · dùng F02 FFmpeg kinetic làm chuẩn · upload cloud/Drive khi chưa được bảo · đăng lại nội dung.

**Edit [TLE]:** reupload hình/tiếng gốc kênh mẫu · dùng audio/logo kênh khác · lip-sync mặt · ghi đè bản cũ (đổi `output_subdir`) · video ngang/intro dài trước claim (theo CONG-THUC-EDIT).

**Vận hành [Chung]:** render >1 cái cùng lúc / render ngoài flock · xoá file lock · `pkill -f` theo mẫu nằm trong chính lệnh · chạy ~25 bot cùng lúc · whisper large/medium khi thiếu RAM · dùng cookie/tài khoản để vượt chặn X · dump transcript/file dài vào chat · bố tự làm thay bot con · xưng "bố" với anh.
