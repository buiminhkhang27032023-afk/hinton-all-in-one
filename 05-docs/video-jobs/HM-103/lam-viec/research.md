# HM-103 · Research tin AI
- Job: HM-103 | version: v1 | researched_at: 2026-10-05 16:40 (giờ VN, UTC+7)
- Window: 24–72h; nguồn backlog: HM-101 Tin 2 & Tin 3
- Avoided: dots, Gemini 4 Argon, Astra cancel+WH Accord, Meta Muse Spark (đã chọn HM-101)
- Style note: ưu tiên visual cho fast-cut ~30 cảnh
- Ghi chú: Tin 1–2 tái dùng claim đã verify từ HM-101 (không bịa thêm). Tin mới = WebSearch + WebFetch ngày 05/10/2026. URL visual bổ sung đã fetch từ blog/YouTube/NVIDIA/OpenAI.

---

## TIN 1 — [BACKLOG HM-101 Tin 2] GPT-6 Astra chơi World of Warcraft “mù”: không nhìn màn hình, phá đảo khu khởi đầu Orc trong 40 phút, 0 chết

HM-103|AI agent tự chơi WoW chỉ bằng dữ liệu mạng|Một developer giao cho Codex (chạy GPT-6 Astra, mức suy luận xhigh) đúng 1 câu lệnh "create an orc character and complete all quests in the starting zone"; agent hoàn thành toàn bộ nhiệm vụ trong 40 phút, 0 lần chết, không nhận một khung hình nào, chỉ đọc gói tin mạng của server và file SQL|https://agent-wow.sh/gpt-6-astra-plays-world-of-warcraft-for-the-first-time-with-agent-wow/|Blog gốc 02/10/2026; Tom's Hardware 03/10/2026; Interesting Engineering 04/10/2026 10:07 AM (giờ miền Đông Mỹ) ≈ 21:07–22:07 04/10 giờ VN|Bot5 (backlog HM-101 + bổ sung visual 05/10) + https://agent-wow.sh/gpt-6-astra-plays-world-of-warcraft-for-the-first-time-with-agent-wow/ + https://www.tomshardware.com/tech-industry/artificial-intelligence/gpt-6-astra-plays-world-of-warcraft-blind-and-clears-the-orc-starting-zone-in-40-minutes-with-no-deaths-ai-agent-navigates-by-server-network-traffic-with-pulled-quest-data + https://interestingengineering.com/ai-robotics/openais-gpt-6-astra-plays-world-of-warcraft + video https://www.youtube.com/watch?v=8NmmFdREk5s|trung bình|Đây là thí nghiệm của 1 developer độc lập (dự án nguồn mở agent-wow), không phải công bố của OpenAI, chưa ai kiểm chứng độc lập. Chạy trên server riêng AzerothCore (WoW 3.3.5a), không phải server thật của Blizzard. Agent đọc thẳng file SQL dữ liệu nhiệm vụ của server và còn "lách" qua tường ở chỗ lỗi bản đồ, nên không phải bài test công bằng như người chơi thật. Bản thân developer nói run này không chạy trong sandbox. Có dính tên GPT-6 Astra (TIN-02 đã nói về vụ hủy GPT-6.1 Astra), nhưng đây là câu chuyện khác hẳn|bố chọn tin
- Nguồn gốc: backlog HM-101 Tin 2 — claim giữ nguyên, không thêm số liệu ngoài nguồn đã verify.
- agent-wow **không có sẵn** cơ chế di chuyển, đánh nhau hay tương tác; agent phải **tự viết module**. Nó tạo 1 module bắt **28 loại tin nhắn server** (Tom's Hardware tự đếm), rồi viết script Python để dựng "bản đồ thế giới" và gửi lệnh hành động.
- Tự viết **công cụ tìm đường bằng C++** dùng file navmesh (mmaps) của AzerothCore và thư viện Detour. Developer khen khả năng tìm đường là "optimal".
- Có lên kế hoạch: làm chuỗi nhiệm vụ tiên quyết theo đúng thứ tự, bán đồ rác, mặc đồ xịn hơn, học kỹ năng trước khi vào hang cuối, nhận cả 2 nhiệm vụ trong hang để làm một lần.
- Developer kể từng tự viết **16K dòng code** cho phần di chuyển, lỗi nhiều nên bỏ. Mục tiêu cuối: lấp đầy cả server bằng AI agent để thử đánh raid Icecrown Citadel độ khó heroic.
- **Video gameplay đã lấy được:** YouTube “GPT-6 Astra Clears the Orc Starting Zone in World of Warcraft” — https://www.youtube.com/watch?v=8NmmFdREk5s (cũng youtu.be/8NmmFdREk5s; Tom's Hardware nhúng cùng ID; Softonic/HN xác nhận). Video mô tả: bắt đầu level-1 Orc, làm hết quest Valley of Trials, kết thúc ở Sen’jin Village ~40 phút, 0 chết.
- Visual density: **rất cao** — 1 video dài đủ cắt ~30 cảnh (quest, combat, pathfinding, hang động, Sen’jin), cộng key art WoW / thumbnail Tom's Hardware / IE hero.

---

## TIN 2 — [BACKLOG HM-101 Tin 3] NVIDIA ra “siêu máy tính AI để bàn” DGX Spark 64GB: 4.999 USD, chạy AI agent 24/7 tại bàn

HM-103|NVIDIA DGX Spark 64GB cho AI chạy local|NVIDIA công bố bản DGX Spark 64GB (chip GB10 Grace Blackwell), mở bán từ thứ Sáu 23/10/2026 qua Acer, ASUS, Dell, Gigabyte, HP, MSI, giá từ 4.999 USD; chạy mô hình tới khoảng 100 tỷ tham số ngay trên máy; ghép 2 máy thành 128GB, chạy được tới 200 tỷ tham số, hiệu năng tới 1,7 lần|https://blogs.nvidia.com/blog/local-ai-dgx-spark-64gb-sync/|02/10/2026 (giờ Mỹ) ≈ 02–03/10/2026 giờ VN|Bot5 (backlog HM-101 + bổ sung visual 05/10) + https://blogs.nvidia.com/blog/local-ai-dgx-spark-64gb-sync/ + https://www.tomshardware.com/pc-components/gpus/nvidia-introduces-64gb-dgx-spark-to-throw-local-ai-fans-a-lifeline-amid-the-rampocalypse-new-gb10-config-starts-at-usd4999-for-those-who-can-work-with-less + https://www.nvidia.com/en-us/products/workstations/dgx-spark/ + https://www.storagereview.com/news/nvidia-dgx-spark-64gb-october-23-4999-two-units-cluster-to-128gb|cao|Con số 1,7x là kết quả NVIDIA tự đo (bài test Qwen 3.8 27B). Giá 4.999 USD là giá khởi điểm tại Mỹ, chưa có giá và lịch bán ở Việt Nam. Tom's Hardware cảnh báo giá có thể không giữ được lâu vì giá RAM đang biến động. Đây là tin sản phẩm, độ viral thấp hơn tin game|bố chọn tin
- Nguồn gốc: backlog HM-101 Tin 3 — claim giữ nguyên.
- Vẫn giữ chip **GB10 Grace Blackwell**, DGX OS và đầy đủ phần mềm AI của NVIDIA như bản 128GB; chỉ khác dung lượng RAM (64GB). Bản 128GB vẫn được bán tiếp.
- NVIDIA gợi ý dùng để **chạy AI agent suốt ngày đêm** (review code, phân tích tài liệu, làm tác vụ nhiều bước), riêng tư, không phụ thuộc cloud.
- **NVIDIA Sync Cluster Assistant** tự cấu hình khi ghép 2 máy qua ConnectX-7; cuối tháng có **Sync Model Launcher**.
- Blender là một trong những ứng dụng sáng tạo lớn đầu tiên hỗ trợ nền tảng này.
- Visual: ảnh sản phẩm blog NVIDIA, ảnh 2-node cluster StorageReview, ảnh XDA, trang product NVIDIA (64GB “Coming Soon”).

---

## TIN 3 — [MỚI] ChatGPT Finances mở rộng xuống Free & Go (Mỹ): kết nối ngân hàng + Experian, dashboard tài chính trong chat

HM-103|ChatGPT Finances Free/Go US rollout|Ngày 02/10/2026 OpenAI cập nhật: Finances in ChatGPT bắt đầu rollout cho người dùng Free và Go tại Mỹ (web, iOS, Android); kết nối tài khoản qua Plaid và báo cáo tín dụng Experian; xem spending, bills, subscriptions, net worth, investments, credit score; không chuyển tiền / không trả bill / không tư vấn đầu tư chuyên nghiệp|https://openai.com/index/personal-finance-chatgpt/|Update chính thức 02/10/2026; Release Notes OpenAI Help Center 02/10/2026|Bot5 + https://openai.com/index/personal-finance-chatgpt/ + https://help.openai.com/en/articles/6825453-chatgpt-release-notes + https://help.openai.com/en/articles/20001222-finances-in-chatgpt|cao|Đây là **mở rộng đối tượng** (Free/Go), không phải ra mắt lần đầu (preview Pro từ 15/05/2026, Plus từ 25/06/2026). Chỉ Mỹ. OpenAI nhấn mạnh không thay thế cố vấn tài chính. Visual là UI product (dashboard, connect accounts, goal planning) — đủ cho nhiều cảnh UI nhưng kém “viral/game” hơn WoW|bố chọn tin
- Tính năng mới kể từ launch: weekly updates, credit monitoring, stock watchlists, voice, Android, manual account entry.
- Kết nối >12.000 định chế tài chính qua Plaid; Experian riêng cho credit score.
- Conversations mặc định GPT‑5.5 Thinking khi có tài khoản đã kết nối (theo blog).
- Visual density: **trung bình–cao** cho style UI cut — nhiều screenshot chính chủ OpenAI (connect accounts, goal planning 16:9/3:4, savings widgets, SEO hero).

---

## TIN 4 — [MỚI] Aleph Alpha phát hành Kolibri: mô hình open-weight Đức 78B (3B active), Apache 2.0, context tới 1M token

HM-103|Aleph Alpha Kolibri open-weight EU model|Ngày 03/10/2026 (Ngày thống nhất nước Đức) Aleph Alpha phát hành Kolibri — MoE Transformer Anh–Đức 78,1B tổng / ~3,46B active mỗi token; context tới 1M token; full weights trên Hugging Face giấy phép Apache 2.0; tối ưu cho công việc sovereign / regulated (hành chính công, công nghiệp, hàng không vũ trụ)|https://aleph-alpha.com/en/blog/kolibri-has-landed-a-sovereign-open-weight-model/|03/10/2026|Bot5 + https://aleph-alpha.com/en/blog/kolibri-has-landed-a-sovereign-open-weight-model/ + https://huggingface.co/Aleph-Alpha/Kolibri-1|cao|Nguồn chính chủ EU startup; benchmark do hãng tự chạy. Ít “hot Mỹ” hơn OpenAI/NVIDIA/Meta; visual chủ yếu chart/benchmark + cover art, không có video demo gameplay. Phù hợp khán giả B2B/sovereign AI hơn viral short|bố chọn tin / backlog
- Reasoning mode: none / low / medium / high. Pre-train ~20T token; ~21,3% German organic.
- So với Kolibri Origin (30B, không public): nhảy từ 11/06 → 11/09 pre-train xong, public 03/10.
- Serve qua `aleph-alpha-inference` / vLLM plugin (`Aleph-Alpha/Kolibri-1`).
- Visual density: **thấp–trung bình** (cover JPEG, bảng benchmark, Pareto charts trên blog).

---

## Dự phòng (verify nhẹ / mép cửa sổ)
- **Runway Praxis-1** (Robot Report 02/10/2026): world-action model open-weight cho robot, học từ video; đang early partner (Noble Machines, Standard Bots, Ultra); public weights “coming months”. Visual: https://www.therobotreport.com/wp-content/uploads/2026/10/runway-featured.jpg + env-kitchen.jpeg. Chưa có video demo dài công khai như WoW/Dyna.
- **Dyna Taku / Dyna-2.1**: blog chính chủ **29/09/2026** (ngoài cửa sổ 72h nếu tính chặt từ 05/10); The Rundown đưa 01–02/10. Visual cực mạnh (1 giờ laundry uncut) nhưng **không đưa top** vì ngày công bố gốc ngoài window — chỉ ghi chú nếu bố muốn robot footage.
- Anthropic Claude Frontier Academy (02/10): đã ghi ở HM-101 dự phòng; ít visual.
- Tránh: WH Accord / AI czar / Astra cancel continuation.

---

## Đề xuất mạnh nhất
- Tin #: **1 — GPT-6 Astra chơi WoW “mù” (backlog HM-101 Tin 2)**
- Lý do: Hook cực rõ cho short cắt nhanh (“AI chơi WoW không nhìn màn hình, 40 phút, 0 chết”). **Visual density cao nhất** trong cả 4 tin: có sẵn **video gameplay YouTube đầy đủ** (`8NmmFdREk5s`) đủ cắt ~30 cảnh (tạo nhân vật → quest Valley of Trials → combat → hang → Sen’jin) + thumbnail/key art. Style HM-103 yêu cầu fast-cut ~30 cảnh → tin này khớp hơn DGX (ảnh sản phẩm tĩnh) và Finances (UI). Caveat rõ: thí nghiệm độc lập, AzerothCore private, không phải OpenAI công bố — giữ trong VO. Phương án thay nếu bố muốn sản phẩm hardware: Tin 2 DGX; nếu muốn product UI Mỹ: Tin 3 Finances.

## Danh sách link visual (ưu tiên tin đề xuất; kèm tin khác)

### Tin 1 — WoW (ưu tiên cắt ~30 cảnh)
- [Video gameplay đầy đủ YouTube] https://www.youtube.com/watch?v=8NmmFdREk5s
- [Cùng video short link] https://youtu.be/8NmmFdREk5s
- [Blog gốc agent-wow — nguồn + mô tả recording] https://agent-wow.sh/gpt-6-astra-plays-world-of-warcraft-for-the-first-time-with-agent-wow/
- [Tom's Hardware hero / WoW key art CDN] https://cdn.mos.cms.futurecdn.net/3PafanCD9Ws7RDdJ8SGBji.jpg
- [Tom's Hardware related CMS image] https://cdn.mos.cms.futurecdn.net/6mmVqfQjXAQVMLwxBZ5SQV.jpg
- [Interesting Engineering hero 1920×1080] https://cms.interestingengineering.com/wp-content/uploads/2026/10/image-1920x1080-2026-10-04T135603.874.png
- [HN thread context] https://news.ycombinator.com/item?id=49933251

### Tin 2 — DGX Spark 64GB
- [NVIDIA blog hero 1280×680] https://blogs.nvidia.com/wp-content/uploads/2026/10/nv-blog-1280x680-1.jpg
- [NVIDIA blog body product] https://blogs.nvidia.com/wp-content/uploads/2026/10/10-02-local-AI-blog-body.jpg
- [NVIDIA product OG / family] https://www.nvidia.com/content/dam/en-zz/Solutions/dgx-spark/nvidia-dgx-spark-family-og.jpg
- [StorageReview 2-node cluster front-angle] https://www.storagereview.com/wp-content/uploads/2026/10/Storagereview-NVIDIA-DGX-Spark-2-Node-Cluster-Front-Angle-2.jpg
- [XDA DGX Spark 64GB / Sync graphic] https://static0.xdaimages.com/wordpress/wp-content/uploads/2026/10/local_ai_blog-dgx_spark_64gb_nvidia_sync_10_2.jpg
- [Trang product DGX Spark] https://www.nvidia.com/en-us/products/workstations/dgx-spark/

### Tin 3 — ChatGPT Finances (UI)
- [SEO / hero Personal Finance] https://images.ctfassets.net/kftzwdyauwt9/LOx9hwb9FayMVDsvnMHBI/a50d14deb15ce97f1ae869a7e4afc964/SEO-Personal-Finance.jpg
- [UI Connecting accounts 16:9] https://images.ctfassets.net/kftzwdyauwt9/7yt3eHKhaDHyE3CB4Jp970/e71fd6b45a7311b181e640cbf0d3353e/OAI-ChatGPT-Personal-Finances-Connecting-accounts-16x9.png
- [UI Goal planning 16:9] https://images.ctfassets.net/kftzwdyauwt9/6vqEtiJWI45VyDgCniABzZ/f89ed847a8e956ad4c7dc281d641f817/1-OAI-ChatGPT-Personal-Finances-GoalPlanning-16x9.png
- [UI Goal planning 3:4] https://images.ctfassets.net/kftzwdyauwt9/7prfJ6RkXY65OalJ3mcyvp/099eb31195802577f35fba73fdb2167c/1-OAI-ChatGPT-Personal-Finances-GoalPlanning-3x4.png
- [Widget Savings Plan dark] https://images.ctfassets.net/kftzwdyauwt9/3QsCLAtPHnhCTRU7zVn1EJ/356050f489693bbe1a893190f5b7ccac/Widget-Savings-Plan-DM-1.png
- [Widget Savings Plan light] https://images.ctfassets.net/kftzwdyauwt9/3gk9GULZIyOMj9SGOLnYuT/a6396a80beec93a36cfd37af56f563a7/Widget-Savings-Plan-LM-1.png
- [Blog OpenAI Finances] https://openai.com/index/personal-finance-chatgpt/

### Tin 4 — Kolibri + dự phòng Runway
- [Aleph Alpha Kolibri cover] https://aleph-alpha.com/_astro/00-cover.Du35XCGh_zJqw.jpeg
- [Hugging Face Kolibri-1] https://huggingface.co/Aleph-Alpha/Kolibri-1
- [Runway Praxis-1 featured] https://www.therobotreport.com/wp-content/uploads/2026/10/runway-featured.jpg
- [Runway kitchen env still] https://www.therobotreport.com/wp-content/uploads/2026/10/env-kitchen.jpeg

## Path
/workspace/video-jobs/HM-103/lam-viec/research.md
