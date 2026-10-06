# HM-101 · Research tin AI
- Job: HM-101 | version: v1 | researched_at: 2026-10-05 15:30 (giờ VN, UTC+7)
- Window: 24–72h trước researched_at (≈ 15:30 02/10 → 15:30 04/10/2026 giờ VN; tin công bố đến trưa 05/10 vẫn ghi nhận)
- Avoided (đã dùng): OpenAI dots, Gemini 4 Argon, Astra cancel + WH Accord
- Ghi chú: mọi claim dưới đây lấy từ trang đã mở đọc trực tiếp (WebFetch) ngày 05/10/2026. Nguồn Mỹ chỉ ghi ngày, không ghi giờ → quy đổi giờ VN theo ngày (+14h so với giờ PDT). Không thêm số liệu ngoài nguồn.

---

## TIN 1 — Meta: AI Muse Spark giúp các nhà toán học giải 5 bài toán mở (kèm bộ đồ chơi phần cứng nguồn mở Muse Gadgets)

HM-101|Meta Muse Spark giải bài toán nghiên cứu mở|Meta công bố 6 bài báo toán học làm cùng Muse Spark (bản 1.1 và 1.2, Thinking Mode, dùng ngay trong giao diện chat meta.ai, không có scaffold nghiên cứu riêng); 5 bài đưa ra lời giải cho câu hỏi nghiên cứu trước đó chưa có lời giải|https://research.meta.ai/blog/solving-open-research-problems-together|02/10/2026 (giờ Mỹ) ≈ 02–03/10/2026 giờ VN; India Today đưa tin 03/10 11:13 IST (12:43 giờ VN)|Bot5 + https://research.meta.ai/blog/solving-open-research-problems-together + https://www.indiatoday.in/amp/technology/news/story/meta-says-muse-spark-helped-solve-6-major-math-problems-releases-open-source-project-for-ai-hardware-3008599-2026-10-03|cao|Đây là thông tin do Meta tự công bố, các bài báo chưa qua bình duyệt (peer review) của tạp chí. Con người dẫn dắt nghiên cứu, AI chỉ là cộng sự. Meta tự thừa nhận một số bài toán đã được các nhóm khác ngoài Meta giải độc lập, bằng cách khác (VD: 3 nhóm với bài Gaussian ellipsoid, agent Nilradical với bài group theory ngày 16/09). Muse chưa rõ có ở Việt Nam hay không. Giờ đăng chính xác không có, nên có thể sát mép đầu cửa sổ 72h|bố chọn tin
- Quy trình: một nhóm nhà toán học dẫn dắt và cùng Muse Spark phát triển lập luận, sau đó **một nhóm thứ hai thẩm định**. Mỗi bài báo **đánh dấu rõ đoạn nào người viết, đoạn nào AI soạn**.
- 6 lĩnh vực: xác suất (ngưỡng "fit ellipsoid" với điểm Gaussian), phương trình vi phân (chứng minh sóng phải "sụp đổ" trong thời gian hữu hạn, giải câu hỏi bỏ ngỏ từ **2015**, xác nhận dự đoán mô phỏng năm **2002**), lý thuyết nhóm (bác bỏ giả thuyết của M. Kida năm 2024 bằng phản ví dụ là một nhóm có **384 phần tử**; Muse Spark viết chương trình tìm kiếm bằng GAP), tối ưu hóa, "arithmetic physics" (nối lý thuyết số với lý thuyết dây p-adic theo hướng Yuri Manin từ thập niên 1980; Muse Spark soạn **3 phần kỹ thuật cốt lõi**), đại số không kết hợp (phản ví dụ 3 chiều).
- Meta nói đầu năm nay các mô hình của hãng đạt mức **huy chương vàng ở 5 kỳ Olympiad** toán, lý, hóa cấp trung học. Bài toán nghiên cứu mở thì khác: "There is no answer key".
- Cùng đợt (02/10), Alexandr Wang công bố **Muse Gadgets**: firmware ESP32 + Linux SDK nguồn mở để ai cũng làm được phần cứng chạy với Muse. Meta ra kèm thiết bị **Muse Home Link** (cấp nguồn USB-C, điều khiển TV, loa...). Meta sản xuất lô **5.000 chiếc** để tặng cho người đăng ký Muse (theo India Today).
- Bối cảnh (India Today): app Muse từng đứng top bảng xếp hạng app store ở Mỹ; trước đó OpenAI từng tuyên bố giải bài toán Navier-Stokes nhưng bị hai nhà nghiên cứu phản bác.
- Nguồn phụ (chưa mở đọc, chỉ thấy trong kết quả search): https://pasqualepillitteri.it/en/news/20210/meta-announces-muse-gadgets-esp32-firmware (bài này trích post X của @alexandr_wang ngày 02/10 và repo GitHub Apache 2.0); https://www.newsbytesapp.com/news/science/meta-releases-open-source-muse-ai-code-for-diy-devices/tldr
- Visual gợi ý: các hình minh họa (Figure 1–5) trên blog Meta, post X của Alexandr Wang, ảnh Muse Home Link.

---

## TIN 2 — GPT-6 Astra chơi World of Warcraft "mù": không nhìn màn hình, phá đảo khu khởi đầu của Orc trong 40 phút, không chết lần nào

HM-101|AI agent tự chơi WoW chỉ bằng dữ liệu mạng|Một developer giao cho Codex (chạy GPT-6 Astra, mức suy luận xhigh) đúng 1 câu lệnh "create an orc character and complete all quests in the starting zone"; agent hoàn thành toàn bộ nhiệm vụ trong 40 phút, 0 lần chết, không nhận một khung hình nào, chỉ đọc gói tin mạng của server và file SQL|https://agent-wow.sh/gpt-6-astra-plays-world-of-warcraft-for-the-first-time-with-agent-wow/|Blog gốc 02/10/2026; Tom's Hardware 03/10/2026; Interesting Engineering 04/10/2026 10:07 AM (giờ miền Đông Mỹ) ≈ 21:07–22:07 04/10 giờ VN|Bot5 + https://agent-wow.sh/gpt-6-astra-plays-world-of-warcraft-for-the-first-time-with-agent-wow/ + https://www.tomshardware.com/tech-industry/artificial-intelligence/gpt-6-astra-plays-world-of-warcraft-blind-and-clears-the-orc-starting-zone-in-40-minutes-with-no-deaths-ai-agent-navigates-by-server-network-traffic-with-pulled-quest-data + https://interestingengineering.com/ai-robotics/openais-gpt-6-astra-plays-world-of-warcraft|trung bình|Đây là thí nghiệm của 1 developer độc lập (dự án nguồn mở agent-wow), không phải công bố của OpenAI, chưa ai kiểm chứng độc lập. Chạy trên server riêng AzerothCore (WoW 3.3.5a), không phải server thật của Blizzard. Agent đọc thẳng file SQL dữ liệu nhiệm vụ của server và còn "lách" qua tường ở chỗ lỗi bản đồ, nên không phải bài test công bằng như người chơi thật. Bản thân developer nói run này không chạy trong sandbox. Có dính tên GPT-6 Astra (TIN-02 đã nói về vụ hủy GPT-6.1 Astra), nhưng đây là câu chuyện khác hẳn|bố chọn tin
- agent-wow **không có sẵn** cơ chế di chuyển, đánh nhau hay tương tác; agent phải **tự viết module**. Nó tạo 1 module bắt **28 loại tin nhắn server** (Tom's Hardware tự đếm), rồi viết script Python để dựng "bản đồ thế giới" và gửi lệnh hành động.
- Tự viết **công cụ tìm đường bằng C++** dùng file navmesh (mmaps) của AzerothCore và thư viện Detour. Developer khen khả năng tìm đường là "optimal".
- Có lên kế hoạch: làm chuỗi nhiệm vụ tiên quyết theo đúng thứ tự, bán đồ rác, mặc đồ xịn hơn, học kỹ năng trước khi vào hang cuối, nhận cả 2 nhiệm vụ trong hang để làm một lần.
- Developer kể từng tự viết **16K dòng code** cho phần di chuyển, lỗi nhiều nên bỏ. Mục tiêu cuối: lấp đầy cả server bằng AI agent để thử đánh raid Icecrown Citadel độ khó heroic.
- Có video ghi lại toàn bộ lượt chơi (Tom's Hardware nhắc tới một video YouTube; blog gốc có link "full gameplay recording"). URL video chưa trích được, cần lấy từ blog gốc trước khi dựng.
- Nguồn phụ: Hacker News thread https://news.ycombinator.com/item?id=49933251 (chưa mở đọc).

---

## TIN 3 — NVIDIA ra "siêu máy tính AI để bàn" DGX Spark 64GB: 4.999 USD, chạy AI agent 24/7 ngay tại bàn, không phụ thuộc cloud

HM-101|NVIDIA DGX Spark 64GB cho AI chạy local|NVIDIA công bố bản DGX Spark 64GB (chip GB10 Grace Blackwell), mở bán từ thứ Sáu 23/10/2026 qua Acer, ASUS, Dell, Gigabyte, HP, MSI, giá từ 4.999 USD; chạy mô hình tới khoảng 100 tỷ tham số ngay trên máy; ghép 2 máy thành 128GB, chạy được tới 200 tỷ tham số, hiệu năng tới 1,7 lần|https://blogs.nvidia.com/blog/local-ai-dgx-spark-64gb-sync/|02/10/2026 (giờ Mỹ) ≈ 02–03/10/2026 giờ VN|Bot5 + https://blogs.nvidia.com/blog/local-ai-dgx-spark-64gb-sync/ + https://www.tomshardware.com/pc-components/gpus/nvidia-introduces-64gb-dgx-spark-to-throw-local-ai-fans-a-lifeline-amid-the-rampocalypse-new-gb10-config-starts-at-usd4999-for-those-who-can-work-with-less + https://forums.developer.nvidia.com/t/nvidia-dgx-spark-64gb-gives-developers-more-ways-to-build-and-scale-local-ai/384838|cao|Con số 1,7x là kết quả NVIDIA tự đo (bài test Qwen 3.8 27B). Giá 4.999 USD là giá khởi điểm tại Mỹ, chưa có giá và lịch bán ở Việt Nam. Tom's Hardware cảnh báo giá có thể không giữ được lâu vì giá RAM đang biến động; bình luận độc giả chê "ít RAM hơn mà đắt hơn". Bài forum NVIDIA không ghi tên ASUS, còn blog chính thức thì có. Đây là tin sản phẩm, độ "nóng" viral thấp hơn Tin 1–2|bố chọn tin
- Vẫn giữ chip **GB10 Grace Blackwell**, DGX OS và đầy đủ phần mềm AI của NVIDIA như bản 128GB; chỉ khác dung lượng RAM (64GB). Bản 128GB vẫn được bán tiếp.
- NVIDIA gợi ý dùng để **chạy AI agent suốt ngày đêm** (review code, phân tích tài liệu, làm tác vụ nhiều bước), riêng tư, không phụ thuộc cloud.
- **NVIDIA Sync Cluster Assistant** tự cấu hình khi ghép 2 máy qua ConnectX-7; cuối tháng có **Sync Model Launcher**, bấm vài nút là chạy được Qwen3.8 27B.
- Tom's Hardware: hiện mua máy GB10 128GB phải trả khoảng **7.000–9.000 USD**; mô hình dense như Qwen 3.8 27B giờ chạy vừa trong 32GB RAM (context có hạn).
- Blender là một trong những ứng dụng sáng tạo lớn đầu tiên hỗ trợ nền tảng này (sắp có bộ cài).
- Nguồn phụ: https://mediarelease.co/us/mr01159-nvidia-dgx-spark-64gb-gives-developers-more-ways-to-build-02102026.html (bản phát hành của NVIDIA, đã đọc); https://www.marktechpost.com/2026/10/02/nvidia-announces-dgx-spark-64gb-a-1-petaflop-grace-blackwell-desktop-for-local-ai-agents-fine-tuning-and-inference/ (đã đọc; bài có NVIDIA tài trợ: thông số 1 petaFLOP FP4 có sparsity, nặng 1,2 kg, kích thước 150×150×50,5 mm).

---

## Dự phòng (đã verify, không đưa vào top 3)
- Anthropic **Claude Frontier Academy**: đầu tư 100 triệu USD để đào tạo 10.000 "Frontier Deployed Engineers" trước cuối 2027. Lứa đầu có kỹ sư của Accenture, Bain, Capgemini, CBA, Deloitte, McKinsey, Morgan Stanley, Novo Nordisk. Công bố 02/10/2026. Đã đọc: https://www.anthropic.com/news/claude-frontier-academy. Hợp với khán giả là chủ doanh nghiệp, nhưng ít viral.
- Google **Project Suncatcher**: vệ tinh mẫu mang 4 chip TPU đã lên quỹ đạo trên chuyến Transporter-18 của SpaceX. Công bố 01/10/2026, **nằm ngoài cửa sổ 72h**. Đã đọc: https://blog.google/innovation-and-ai/models-and-research/google-research/project-suncatcher-prototype/
- Trump bổ nhiệm Jay Clayton làm "AI czar", lập "Super Intelligence Force" (04/10, NPR/CBS/Reuters). **Không chọn** vì là phần tiếp nối WH Accord đã dùng ở TIN-02. Chưa mở đọc đầy đủ, mới chỉ xem trích đoạn search.

---

## Đề xuất mạnh nhất
- Tin #: 1 — Meta Muse Spark giúp giải 5 bài toán nghiên cứu mở (+ Muse Gadgets)
- Lý do: Hook mạnh và dễ hiểu: "AI không còn chỉ làm bài có sẵn đáp án, nó bắt đầu giúp tạo ra kiến thức mới". Nguồn chính chủ (blog Meta Research), độ tin cậy cao, không trùng TIN-02 và mở ra "người chơi thứ 4" là Meta. Visual: figure minh họa trên blog, chân dung Alexandr Wang, thiết bị Muse Home Link. Thông điệp cho chủ doanh nghiệp/creator: chuyên gia + AI dùng ngay giao diện chat bình thường đã tạo ra kết quả cấp nghiên cứu, mấu chốt là con người dẫn dắt và kiểm chứng. Vừa một short ~60s nếu giữ caveat "Meta tự công bố, có nhóm khác giải độc lập". Phương án thay thế nếu bố muốn visual game viral: Tin #2 (WoW, có sẵn video gameplay).
- Path: /workspace/video-jobs/HM-101/lam-viec/research.md
