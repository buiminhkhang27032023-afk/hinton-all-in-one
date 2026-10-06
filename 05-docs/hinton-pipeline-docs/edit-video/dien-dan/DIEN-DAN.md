# DIỄN ĐÀN & CỘNG ĐỒNG học dựng video dọc kiểu AI/tech talking-head

Lấy dữ liệu ngày 03/10/2026, khoảng 17:05–18:00 ICT. Không tải video nào; chỉ đọc trang web, metadata và phụ đề tự động YouTube (dạng text). Transcript đã lưu ở `raw/subs/*.txt`.

Ký hiệu độ tin cậy:
- **[ĐÃ MỞ]**: mình đã đọc trực tiếp trang hoặc transcript.
- **[INDEX]**: chỉ đọc được qua bản trích của công cụ tìm kiếm, vì trang chặn truy cập từ máy mình (Reddit timeout, Bilibili 412, Zhihu 500/timeout, Facebook bắt đăng nhập).
- **[TIÊU ĐỀ]**: mới chỉ xác nhận trang tồn tại; bài học suy ra từ tiêu đề hoặc mô tả.

Quy ước về số thành viên: chỉ ghi khi trang tự hiển thị. Reddit đã bỏ hiển thị tổng thành viên, nên số Reddit dưới đây là **ước tính của bên thứ ba** và được ghi rõ như vậy.

---

## 1. Quốc tế

### 1.1 Reddit: r/NewTubers
- URL: https://www.reddit.com/r/NewTubers/
- Quy mô: khoảng 729K thành viên, khoảng 34,5 bài/ngày. Đây là ước tính của prowlo.com (bên thứ ba); Reddit không hiển thị.
- Vì sao hữu ích: nhiều bài hỏi–đáp về hook và retention của Shorts, có người góp ý trực tiếp cho video của nhau. Hoạt động: có bài từ tháng 1 đến tháng 7/2026.

| Thread | Bài học (1 dòng) |
|---|---|
| [INDEX] https://www.reddit.com/r/NewTubers/comments/1syvvot/need_feedback_on_my_youtube_short_is_my_hook_weak/ | Hook là frame đầu chứ không phải câu đầu. Đặt 0,5–1,5s "kết quả/cao trào" lên đầu rồi cắt về từ đầu. Chữ to nêu bối cảnh trong 2s đầu. Không để caption đè 1/3 dưới (nơi có UI). |
| [INDEX] https://www.reddit.com/r/NewTubers/comments/1qjvtx1/any_tips_how_to_make_good_shorts_that_are_good/ | Bỏ hẳn intro, vào giữa câu hoặc giữa hành động. Test: tắt tiếng xem 1 giây đầu, nếu không hiểu video nói gì thì hook hỏng. (Đăng 22/01/2026) |
| [INDEX] https://www.reddit.com/r/NewTubers/comments/1usbo8q/what_caption_style_actually_keeps_people_watching/ | Caption 2–3 chữ/cụm, tránh nháy từng chữ quá nhanh (gây chóng mặt). Chỉ highlight từ khoá. Không để cả câu dài vì người xem sẽ đọc trước rồi lướt đi. |
| [INDEX] https://www.reddit.com/r/NewTubers/comments/1udoczh/forget_hook_in_3_seconds_for_a_second_the_end_of/ | Đoạn kết giết watch time: cắt sạch hơi thở cuối, để câu cuối nối liền vào câu đầu, tạo vòng lặp xem lại. |

### 1.2 Reddit: r/VideoEditing, r/VideoEditors, r/editors, r/CapCut
- URL:
  - https://www.reddit.com/r/VideoEditing/ (khoảng 501K–529K, ước tính bên thứ ba: redpulse, gummysearch)
  - https://www.reddit.com/r/VideoEditors/
  - https://www.reddit.com/r/editors/
  - https://www.reddit.com/r/CapCut/
- Quy mô các sub còn lại: không có số hiển thị.
- Vì sao hữu ích: editor chuyên nghiệp tranh luận về kỹ thuật (punch-in, sound design, caption), kèm cách làm cụ thể trong CapCut/Premiere.

| Thread | Bài học (1 dòng) |
|---|---|
| [INDEX] https://www.reddit.com/r/VideoEditing/comments/1w2s1r4/how_do_you_improve_sound_design_for_hooks/ | Hook 3s chỉ 2–3 sự kiện âm thanh (whoosh trước cắt, impact đúng frame lộ ra, riser tuỳ chọn). Một âm chính, lớp phụ thấp hơn 8–10 dB. Dựng câm trước rồi mới thêm âm. Nửa giây im lặng trước câu chính. |
| [INDEX] https://www.reddit.com/r/VideoEditors/comments/1kez8lx/editors_that_cut_or_watch_talking_head/ | Tranh luận về zoom ≤5% để "giấu" jump cut. Nhiều editor cho rằng zoom nhỏ vậy vô nghĩa: hoặc punch-in hẳn sang khung chặt hơn, hoặc chọn điểm cắt đúng (ví dụ lúc người nói ngả ra cười). |
| [INDEX] https://www.reddit.com/r/CapCut/comments/1unxoy8/just_one_simple_question_how_do_i_make_the/ | Ảnh/chữ "trôi vào mượt": Animation In → Fade/Zoom In 0,4–0,6s, tránh kiểu bounce. Hoặc keyframe Scale nhỏ hơn + Opacity 0 → 100% sau vài frame. (Đăng 05/07/2026) |
| [INDEX] https://www.reddit.com/r/editors/comments/1smd65o/should_i_add_music_and_subtitles_in_app_for/ | Với TikTok: dựng hình và sfx trong phần mềm dựng, còn nhạc trending và caption thì thêm trong app để có metadata. Nên A/B giữa caption burn-in và caption in-app. |
| [INDEX] https://www.reddit.com/r/VideoEditing/comments/14zn7v4/how_to_edits_videos_with_facecam_as_top_half_and/ | Cách dựng bố cục facecam nửa trên + màn hình nửa dưới (ngược với C1). Chừa đáy cho UI nền tảng. |
| [INDEX] https://www.reddit.com/r/socialmedia/comments/1rx23nm/current_goto_caption_creation_tools/ | Caption kiểu Hormozi: Premiere Speech-to-Text + mogrt, hoặc CapCut/Submagic để có highlight từng chữ mà không phải keyframe tay. |

### 1.3 Skool: WavyWorld (cộng đồng miễn phí của Kallaway)
- URL: https://www.skool.com/wavyworld/about
- Quy mô **[ĐÃ MỞ]**: 51,7k thành viên, 187 đang online, 3 admin, miễn phí, nhóm private. Trang About của Skool hiển thị số này ngày 03/10/2026.
- Vì sao hữu ích: chính là Kallaway, kênh mẫu C1–C3 của mình. Có hướng dẫn về format, kịch bản, editing và video teardown. Nội dung bên trong cần tham gia nhóm (mình chưa join).
- Tài liệu công khai của cùng tác giả, kênh YouTube Kallaway (465K subs):

| Tài liệu | Bài học (1 dòng) |
|---|---|
| [ĐÃ MỞ, transcript] https://www.youtube.com/watch?v=xnOe8aA9Pmw ("I Studied 100 Viral Hooks…", 324,9K view) | Hook có 4 lớp: lời nói, hình, chữ, âm thanh, và cả 4 phải nói cùng một chủ thể. Mắt người xem đi theo thứ tự hình → nghe → quay lại hình để xác nhận, nên chọn "key visual" trước rồi mới viết lời. Ví dụ của chính anh: chữ "life-size floor plans" kèm mũi tên chỉ đúng vào key visual. |
| [ĐÃ MỞ, transcript] https://www.youtube.com/watch?v=2byPP_9F0-Q ("Give me 15 mins…", 1,03M view) | 4 lỗi hook: chậm vào chủ đề, khó hiểu, không liên quan, không gây tò mò. Phải nêu chủ đề trong 1–2s đầu. Dùng "bạn" thay "tôi". Tạo tương phản A (điều họ tin) với B (điều mình đưa ra). |
| [ĐÃ MỞ, bản tóm tắt + transcript] https://moderncreator.app/2025-12-22-kallaway-how-to-create-a-killer-hook-impossible-to-skip | 4 cách tạo "visual stun" ở 2s đầu: người đặc biệt, chủ thể dễ nhận ra, footage lạ, bố cục lạ. Ví dụ bố cục: người ở nửa dưới, khoảng trống phía trên (tường/trần) làm canvas chiếu B-roll; 2 thanh đen trên/dưới khép dần tạo chờ đợi; viền trắng dày quanh người đã tách nền. Ngoài caption thì nên luôn có thêm "text hook" (tiêu đề). |

### 1.4 Kênh YouTube dạy đúng kiểu dựng này (quốc tế)

| Video | Kênh (subs hiển thị) | Bài học (1 dòng) |
|---|---|---|
| [ĐÃ MỞ, transcript] https://www.youtube.com/watch?v=sLgHqZSe2o0 (5,84M view) | Learn By Leo (188K) | Có 4 trụ cột: đa dạng hình ảnh, liền mạch, dẫn mắt, âm thanh. Đồ hoạ không được tự hiện ra mà phải chuyển động vào khung hoặc có sfx (shutter/pop) đi kèm. Khi cắt, giữ điểm nhìn (mắt) ở cùng vị trí giữa 2 clip. Dẫn mắt trên ảnh: làm tối/blur xung quanh, đổi hue đỏ (tiêu cực) hoặc vàng/xanh (tích cực), glow chủ thể. Caption ≤3 chữ và chỉ dùng khi cần nhấn. Riser chỉ đặt trước điều thật sự quan trọng; tắt nhạc đột ngột để nhấn; khớp đoạn nhạc lên cao trào với lúc chuyển từ vấn đề sang giải pháp. |
| [ĐÃ MỞ, transcript] https://www.youtube.com/watch?v=Qbntd8yud0o (396,7K view) | Joseph \| Video Editing (197K) | Quy trình sound design 3 bước: (1) whoosh cho mọi zoom/chuyển động, nhẹ hay gắt theo biên độ; (2) sfx có "chất liệu" riêng cho từng graphic (UI click mỗi icon, tiếng máy tính tiền cho chữ "investment", kính vỡ cho hiệu ứng shatter); (3) nhạc nền. Chữ 2 tầng: tầng thường gradient trắng→xám, tầng nhấn gradient đỏ→cam/xanh, kèm glow và light sweep. |
| [ĐÃ MỞ, transcript] https://www.youtube.com/watch?v=tzfzkTAQsnE (1,02M view) | Herman Huang (208K) | Xếp lớp sfx theo dải tần (trầm/trung/cao) để whoosh có lực. Khoét dải mid của nhạc bằng EQ/de-esser để giọng nằm gọn trong đó. Dùng một bộ sfx cùng phong cách. Vào nhạc bằng đoạn beat đầu đảo ngược làm riser; kết nhạc bằng reverb ở beat cuối. |
| [TIÊU ĐỀ] https://www.youtube.com/watch?v=HqPDRa7i97s (103K view) | Joseph \| Video Editing | "Master Viral Sound Design for Short-Form Content". Chưa lấy được phụ đề vì YouTube trả lỗi 429. |

---

## 2. Trung Quốc

Lưu ý quan trọng: B站, 知乎 và 小红书 đều chặn truy cập từ máy mình (B站 HTTP 412; Zhihu 500/timeout; 小红书 cần đăng nhập). Vì vậy phần lớn link Trung Quốc là **[INDEX]/[TIÊU ĐỀ]**. Thông tin kỹ thuật lấy từ snippet công cụ tìm kiếm thường là blog SEO, nên mình ghi rõ nguồn.

### 2.1 Bilibili (B站): kho video dạy 口播剪辑 (dựng talking-head) lớn nhất
- URL: https://www.bilibili.com. Quy mô: không áp dụng (nền tảng). Số view từng video: chưa lấy được (412).
- Vì sao hữu ích: có cả loạt bài "复刻" (dựng lại) phong cách của từng UP主.

| Video/khoá | Bài học (1 dòng) |
|---|---|
| [TIÊU ĐỀ] https://www.bilibili.com/video/BV1ApK6zHESu/ "三招复刻阿Test硬核科普风【跟着博主学剪辑Vol.09】" | Loạt "跟着博主学剪辑" (Vol.01–09) mổ xẻ phong cách từng kênh (鹿式片头, 文字拆分, 影视飓风节奏, 阿Test 科普). Đây đúng là dạng "kênh mẫu → công thức" mình đang làm. |
| [TIÊU ĐỀ] https://www.bilibili.com/cheese/play/ep2561238 "【影视飓风】剪辑全能必修课" (khoá trả phí) | Bài 2 về "口播精剪 + A/B-roll". Theo mô tả trong index: giữ lại "好气口" (khoảng thở có ý nghĩa), không xoá mọi khoảng lặng; dùng B-roll che chỗ lặp hoặc lỗi. |
| [TIÊU ĐỀ] https://www.bilibili.com/video/BV1KrkiBJEbd/ "1400 款剪映字幕预设，口播调字再也不头疼" | Kho 1.400 preset caption cho 剪映. Gợi ý cho bot: dùng preset cố định để giữ font, màu và vị trí đồng nhất. |
| [TIÊU ĐỀ] https://www.bilibili.com/video/BV13a411e7s7/ "【两分钟学剪映】蒙版圈圈、花字动画、跳剪、特效素材" | Các kỹ thuật cơ bản: mask vòng tròn khoanh vùng, chữ 花字 có animation, jump cut. |
| [TIÊU ĐỀ] https://www.bilibili.com/video/BV1q54y1b7Ks/ "2分钟学会3个讲解类教程的制作小技巧" | Mẹo cho video giảng giải/hướng dẫn. |

### 2.2 Douyin: trang chủ đề 剪辑教程 (một số trang đọc được)
- URL chủ đề: https://www.douyin.com/shipin/7443419125470513178
  - **[ĐÃ MỞ]** "1分钟学会多机位多轨道混剪技巧" (đăng 27/06/2025).
  - Nội dung: trong 剪映, chọn tất cả cảnh → "新建多机位片段", căn theo âm thanh. Vừa phát vừa bấm chọn góc máy. Kéo ranh giới để tinh chỉnh.
  - Bài học: quay 2 góc rồi chuyển góc thật, thay cho punch-in giả.
- Các trang chủ đề khác (7485911669210662953, 7486688592748873743) chỉ trả về ngày đăng. Video 影视飓风 口播剪辑作业 (douyin.com/video/7650115606619950378) không mở được.

### 2.3 Kênh YouTube tiếng Trung dạy 口播剪辑 (xác minh được qua metadata)

| Video | Kênh (subs hiển thị) | Bài học (1 dòng) |
|---|---|---|
| [TIÊU ĐỀ+mô tả] https://www.youtube.com/watch?v=XwxCTQS0-rg "口播剪輯4大方法，提高影片節奏感" (09/12/2024) | 虚空光影CosmosFilm (12,8K; cũng có trên B站/抖音) | "网感" nghĩa là làm cho cảnh talking-head đơn điệu bớt nhàm. Theo snippet index: keyframe scale để nhấn, mask khoanh người/thông tin, picture-in-picture, viền tách nền. Chưa xem được nội dung. |
| [TIÊU ĐỀ+chương] https://www.youtube.com/watch?v=czKdhX1k-rY "人物口播剪輯三大定律" (2023) | 映美剪輯學院 (969) | Có chương "定律一/二" (0:25, 2:27). Nội dung chưa lấy được vì video không có phụ đề. |
| [TIÊU ĐỀ] https://www.youtube.com/watch?v=Ki2ewWnwmgw "怎么剪辑出灵动有节奏感的口播视频？这5个常用技巧" | Xiamen Jiujiu (9,15K) | 5 kỹ thuật để talking-head "có nhịp". Chưa có transcript. |
| [TIÊU ĐỀ] https://www.youtube.com/watch?v=_ZFO4Qm0QT8 "如何说话不卡壳？影视飓风口播技巧分享" (214K view) | Mediastorm影视飓风 (936K) | Về cách nói trước camera (tiền kỳ), giúp giảm số lần phải cắt. |

### 2.4 知乎 / 小红书
- 知乎:
  - https://www.zhihu.com/tardis/jm/art/2038317229956191026 ("3 个隐藏设置让口播一遍过率…")
  - https://zhuanlan.zhihu.com/p/1999792865560270278
  - Cả hai **không mở được** (timeout/500). Snippet index chỉ có lời khuyên chung: BGM khoảng 20% âm lượng giọng, chuyển cảnh fade 0,5s, đổi khung PIP/biểu đồ khoảng mỗi 30s.
- 小红书: **không truy cập được** (cần đăng nhập). Không có link bài cụ thể nào được xác minh.

---

## 3. Việt Nam

Nhận xét chung: ở VN, phần bàn sâu về **phong cách dựng** chủ yếu nằm trong nhóm Facebook (cần đăng nhập, mình không đọc được) và trên kênh YouTube dạy edit. VOZ và Tinhte rất ít thảo luận về kỹ thuật dựng.

### 3.1 Nhóm Facebook dựng video/CapCut (cần đăng nhập)
- "Cộng đồng học edit video Việt Nam": https://www.facebook.com/groups/212165367075171/
- "Cộng đồng CapCut Việt Nam": https://www.facebook.com/groups/563314284677176/ (tên miền thay thế: groups/capcutcreatorvn)
- "Edit Capcut - Việc Làm Video Editor Tiktok", "Editor nghiệp dư 2.0" (https://www.facebook.com/groups/1122559666202072/): tìm thấy qua index.
- Quy mô và mức hoạt động: **chưa lấy được**, vì Facebook chuyển hướng về trang /login.
- Bài viết cụ thể: chưa lấy được.

### 3.2 VOZ (voz.vn): đọc được, đang hoạt động, nhưng nặng về nghề và giá hơn kỹ thuật

| Thread | Bài học (1 dòng) |
|---|---|
| [ĐÃ MỞ] https://voz.vn/t/sinh-vien-nam-2-muon-hoc-edit-video-can-duoc-tu-van-a.1270801/ (16–17/08/2026) | Thị trường: "giờ toàn đòi edit video short 10k/video". "CapCut nó sup hiệu ứng tận răng", nên giá trị nằm ở quay tốt và tư duy dựng, không ở hiệu ứng. |
| [ĐÃ MỞ] https://voz.vn/t/lop-day-edit-video-mien-phi-cho-vozer.751887/ (04/2023–12/2024) | Lớp dạy edit miễn phí cho Vozer, nhu cầu cao. Ít nội dung kỹ thuật công khai trong thread. |

### 3.3 Kênh YouTube Việt dạy edit (nguồn VN có nội dung kỹ thuật thật)

| Video | Kênh (subs hiển thị) | Bài học (1 dòng) |
|---|---|---|
| [ĐÃ MỞ, transcript] https://www.youtube.com/watch?v=ysCbRwtAto8 "Full Quy Trình Edit Video Shorts Talking Heads cho Newbie" (16/05/2026) | Phong Dvc (2,59K) | Quy trình DaVinci:<br>• Tạo phụ đề trước, tối đa 1 từ/dòng để căn chữ. Dùng AI dịch và ghi ý tưởng edit theo mốc thời gian.<br>• Chữ trượt lên từ dưới trong khoảng 15 frame (ease-out cubic) kèm opacity. Chữ nhấp nháy bằng opacity 0/1 ở frame 0–3. Rung nhẹ (camera shake) cho cụm từ khoá.<br>• Icon bay lên lệch nhau. "Match move": icon bay vào đúng vị trí logo kế tiếp.<br>• Meme đặt trong khung bo góc. Screen record đóng băng làm nền.<br>• Chuẩn hoá giọng theo preset nền tảng (Normalize). Đặt tên track Voice/SFX/Ambient/Music.<br>• SFX: "ping" khi zoom-in, "tick" khi chữ hiện, shutter khi có light sweep, riser đạt đỉnh ở cuối đoạn, UI impact ở mức −10 dB. |
| [ĐÃ MỞ, transcript] https://www.youtube.com/watch?v=H97fWHUL-xg "[HOOK] 6 BÍ MẬT mở đầu video TRIỆU VIEW" (26/07/2025) | Trung Công Nghệ (22,1K) | Hook 3 bước: bối cảnh + tò mò → "phanh gấp" bằng từ tương phản (nhưng, thế mà) → bẻ lái. Ngay đầu video có 3–5 từ khoá chữ to đậm. Chuyển động vừa đủ (nghiêng đầu, cử chỉ tay, đập dép). Câu ngắn ở phần hook. Đưa giá trị đầu tiên trong khoảng 4s. |
| [ĐÃ MỞ, transcript] https://www.youtube.com/watch?v=bNP8_Jt1TZ4 "TOP 5 KỸ THUẬT EDIT…" (123K view) | Quạ HD (499K) | 5 nền tảng: tách người (Roto/mask; CapCut có Auto removal) để đặt chữ hoặc graphic SAU lưng người nói; tracking 2D gắn graphic hoặc giữ mặt luôn ở giữa khung; speed ramp nhanh–chậm (nếu cần slow thì quay 60fps); shake nhấn nhịp; color key. Mẹo: muốn tách nền dễ thì mặc tương phản với nền. |
| [ĐÃ MỞ, transcript] https://www.youtube.com/watch?v=-Rm72yDkD9U "Hướng dẫn edit CapCut: TƯ DUY và PHƯƠNG PHÁP" (64K view) | Mean Tính (77,1K) | Lọc cảnh trên timeline (J/K/L để tua). Cắt trước khi cú máy kết thúc. Áp LUT lên một lớp adjustment chung rồi chỉnh từng clip bên dưới. Dùng Paste attributes để chép thông số. Crossfade âm thanh thủ công (CapCut thiếu tính năng này), theo dõi meter để tránh vượt 0 dB. |
| [TIÊU ĐỀ] https://www.youtube.com/watch?v=zhRh-9GDn2o "13 Tiếng Dạy Bạn Edit Video Bằng CapCut (Miễn Phí)" (11/07/2026, 208K view) | Sean Kang (54,5K) | Khoá CapCut miễn phí dài 12,7 giờ. Chưa trích nội dung. |

### 3.4 Tinhte
- https://tinhte.vn/thread/cach-dung-capcut-cho-youtube-shorts-ty-le-khung-hinh-phu-de-va-xuat-file-chuan-2026.4130749/ (30/04/2026)
- https://tinhte.vn/thread/top-template-capcut-dep-de-viral-cho-tiktok-reels-va-youtube-shorts.4130009/
- **[ĐÃ MỞ]** Cả hai do nhà bán bản quyền phần mềm (CentriX Software Asia) viết, nội dung cơ bản (9:16, phụ đề, xuất file). Giá trị học thấp.

---

## 4. Không truy cập / chưa xác minh được
- **Reddit:** fetch trực tiếp bị timeout hoặc 403, nên mọi thread đọc qua index (nội dung có thể bị cắt). Tổng thành viên Reddit chỉ có ước tính bên thứ ba.
- **Bilibili:** HTTP 412 cho cả trang web, API và yt-dlp, nên không lấy được view, độ dài hay nội dung.
- **知乎:** 500 hoặc timeout. **小红书:** cần đăng nhập. **Douyin:** chỉ đọc được một số trang chủ đề `shipin/`.
- **Nhóm Facebook:** bắt đăng nhập, nên không lấy được quy mô, mức hoạt động hay bài viết.
- **Skool WavyWorld:** private, chưa tham gia, nên chỉ có số thành viên ở trang About.
- **Discord:** không tìm thấy server công khai nào chuyên về kiểu dựng này mà xác minh được. Theo index, cộng đồng học viên Quạ HD dùng Discord, nhưng đó là nhóm trả phí.
- **Phụ đề YouTube:** bị 429 ở một số video (HqPDRa7i97s và các video tiếng Trung không có phụ đề). Không tải video hay audio nào để tự chép lời.
