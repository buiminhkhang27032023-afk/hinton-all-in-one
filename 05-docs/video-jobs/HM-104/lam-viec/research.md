# HM-104 · 3 ứng viên Tin AI (24–48h)
- researched_at: 06/10/2026 09:35 (giờ VN) · window ≈ 04/10 09:00 → 06/10 09:00 giờ VN
- Tránh (đã làm/backlog): OpenAI Dots, Gemini 4 Argon, Astra cancel + WH Accord, Muse Spark, GPT-6 Astra chơi WoW, DGX Spark 64GB, ChatGPT Finances, Kolibri.
- Loại vì ngoài window: OpenAI sa thải 3 nhà nghiên cứu (BBC 02/10), robot RP1 "Kick Me" (ra mắt 28/09, PR 04/10).
- Mọi giờ Mỹ (PDT, UTC−7) đã đổi sang giờ VN (+14h).

job_id | topic | claim | source_url | published_at | verified_by | confidence | caveats | next

---

## ỨNG VIÊN 1 (Bot5 đề xuất) — OpenAI bắt đầu gắn "watermark vô hình" vào chữ ChatGPT viết (EU)
HM-104 | ChatGPT text watermark | OpenAI sẽ gắn watermark vô hình vào văn bản ChatGPT và Codex tạo ra cho người dùng ở EU (mọi gói), triển khai trong vài tuần tới, để tuân thủ Đạo luật AI của EU; dev dùng API ở bất kỳ đâu có thể tự bật cho một số model từ 05/10 (mặc định tắt). Watermark không phải ký hiệu, mà là "nắn" cách chọn từ của model, tạo mẫu thống kê mắt thường không thấy nhưng máy dò bắt được; copy-paste vẫn đi theo chữ | https://techcrunch.com/2026/10/05/openai-will-start-watermarking-chatgpts-text-in-the-eu/ (blog gốc https://openai.com/index/eu-text-provenance — 403 khi fetch, chỉ thấy qua search) | TechCrunch 05/10 1:36 PM PDT ≈ 06/10 03:36 giờ VN | Bot5 + TechCrunch + https://www.searchenginejournal.com/openai-to-watermark-chatgpt-text-in-the-eu-opens-api-opt-in/592014/ + báo cáo kỹ thuật textGrain https://cdn.openai.com/pdf/e9508624-d767-41b6-a26d-e34ca798ada6/textgrain-entropy-calibrated-watermarking-for-language-model-text.pdf (chưa mở đọc) | cao | CHỈ ở EU; ngoài EU chưa bật mặc định. Công cụ dò chữ CHƯA công khai, chỉ cấp cho nhà nghiên cứu/tổ chức được duyệt. Sửa chữ làm yếu watermark: thay 10% từ bằng từ đồng nghĩa → tỉ lệ phát hiện ~92% xuống ~66%; thay 25% → ~17% (đoạn 400 token tiếng Anh, test của OpenAI). Đoạn ngắn, đáp án toán, văn bản dịch khó dò hơn. OpenAI nói watermark không định danh người dùng, không giảm chất lượng đáng kể. Anthropic đã gắn watermark chữ Claude toàn cầu từ ~2 tháng trước (theo TechCrunch). Hạn tuân thủ EU cho hệ thống ra trước 02/08: 02/12 | bố chọn tin
- Vì sao nóng: đánh thẳng vào người làm nội dung/sale dùng ChatGPT viết bài → "chữ AI giờ có dấu vân tay". Hook mạnh.
- Visual: trung bình (chủ yếu UI ChatGPT, minh họa chữ/heatmap từ, logo EU AI Act, chart 92→66→17%). Cần dựng motion graphic nhiều.

## ỨNG VIÊN 2 — ChatGPT chèn quảng cáo hình ảnh ngay cạnh ảnh AI người dùng tạo
HM-104 | ChatGPT visual ads | OpenAI thêm định dạng quảng cáo hình ảnh (visual display ads) hiện cạnh ảnh người dùng yêu cầu ChatGPT tạo; bắt đầu cuối tháng 10, chỉ ở Mỹ, với nhóm nhà quảng cáo thử nghiệm đầu tiên; mở rộng công cụ đo lường (AppsFlyer, Adjust, Branch, Triple Whale…) và thử đánh giá an toàn thương hiệu với DoubleVerify, IAS | https://openai.com/index/new-chatgpt-ads-format-and-measurement/ | 05/10/2026 10:04 UTC ≈ 05/10 17:04 giờ VN | Bot5 + OpenAI + https://techcrunch.com/2026/10/05/openai-launches-visual-ads-that-appear-alongside-image-generation-results/ | cao | Chỉ Mỹ, chưa có lịch VN. OpenAI cam kết quảng cáo được gắn nhãn rõ, không ảnh hưởng câu trả lời, hội thoại riêng tư (lời hãng). Quảng cáo ChatGPT có từ đầu năm, mở sang Ấn Độ tháng 8. TechCrunch đặt bối cảnh cạnh tranh với app Muse miễn phí của Meta (suy luận của báo) | bố chọn tin
- Vì sao nóng: chủ DN/marketer — kênh quảng cáo mới; người dùng — "ảnh AI kèm quảng cáo".
- Visual: trung bình–cao (ảnh minh họa ad format trên blog OpenAI, UI tạo ảnh, logo đối tác đo lường).

## ỨNG VIÊN 3 — Reflection AI ra Beam: model mở 501 tỷ tham số, "đấu" model Trung Quốc mà tốn ít tính toán hơn
HM-104 | Reflection Beam open-weight | Beam là model MoE 501B tổng / 23B active, mạnh code–suy luận–agent; Reflection nói ngang GLM-5.2 trên benchmark suy luận nâng cao nhưng dùng ít hơn 3–4 lần tính toán khi chạy; RL trên 10.500 GPU GB300 trong 4 tuần, >100 triệu lượt rollout; pretrain 23,8 nghìn tỷ token; context 1M token; weights Apache 2.0 sẽ phát hành trong tháng 10 | https://reflection.ai/blog/introducing-beam | 05/10/2026 (TechCrunch 12:33 PM PDT ≈ 06/10 02:33 giờ VN) | Bot5 + Reflection blog (đã đọc) + https://techcrunch.com/2026/10/05/reflection-debuts-beam-a-open-weight-ai-model-to-rival-chinese-models-at-lower-compute-cost/ | trung bình–cao | Benchmark do hãng tự chạy, CHƯA kiểm chứng độc lập. Weights CHƯA phát hành (đang red-team, hiện chỉ early access/waitlist). Chỉ text, không đa phương thức. Chính Reflection thừa nhận Kimi K3 vẫn mạnh hơn về năng lực thô; ưu thế của Beam là hiệu quả | bố chọn tin
- Vì sao nóng: cuộc đua model mở Mỹ vs Trung (DeepSeek, Qwen, GLM). Hợp khán giả tech hơn chủ DN.
- Visual: trung bình (demo trên blog: game phi hành gia né thiên thạch p5.js, bản đồ tàu điện NYC live, bảng benchmark, chart hiệu quả).

---
## Dự phòng (đã thấy, chưa đào sâu)
- Google DeepMind SynthID Bio — watermark cho protein do AI thiết kế (SingularityHub 05/10): https://singularityhub.com/2026/10/05/google-deepmind-gives-ai-designed-proteins-a-watermark/ — ghép được với Ứng viên 1 thành chủ đề "AI bị đóng dấu".
- Binance Intelligence — AI miễn phí cho mọi user Binance từ 05/10 (PRNewswire 05/10).
- Hội đồng NYC chất vấn Anthropic/OpenAI/Meta/Google 05/10; xAI (SpaceX) vắng mặt dù có trát (NYT qua DNYUZ 06/10) — chính trị, ít visual.
- Amazon Nova 2.5 Sonic (voice agent), GLM 5.3 lên Bedrock (AWS 05/10) — tin sản phẩm B2B.

## Gợi ý Bot5
Chọn **Ứng viên 1** nếu ưu tiên hook + đúng khán giả (người dùng ChatGPT viết content). Chọn **Ứng viên 2** nếu ưu tiên visual dày cho ~30 cut.
