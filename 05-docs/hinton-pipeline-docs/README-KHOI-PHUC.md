# Gói "bố của các bot" — bot điều phối Hinton Media (đóng gói 05/10/2026)

## Bot này là gì
Bot điều phối (coordinator) của Hinton Media. Chỉ quản lý: giao việc cho bot con qua SendToAgent, QA kịch bản, báo mốc cho anh và gửi thành phẩm 720p, không tự render. Xưng "em", gọi chủ là "anh", nói tiếng Việt. Tự quyết chi tiết pipeline, chỉ báo mốc và thành phẩm cuối.

## Nội dung gói
- bot/profile.json, bot/settings.json: tên, mô tả và cài đặt của bot điều phối.
- hinton-pipeline-docs/: toàn bộ quy trình gồm HINTON_BOOTSTRAP.md, skills/hinton-orchestrate.md, voice-lock.md, RENDER-LOCK.md, luong-toi-uu.md, BOTS.md (danh sách bot con và id).
- jobs/MAP-FOOD-HCM-01, jobs/MAP-FOOD-HP-01: dữ liệu quán, kịch bản, bảng cảnh, template bản đồ (không kèm audio/cache nặng).
- BO-NHO.md: các quy tắc làm việc bot đã học.

## Khôi phục
1. Tạo một bot mới, đặt tên và mô tả theo bot/profile.json.
2. Giải nén gói vào /workspace (hinton-pipeline-docs → /workspace/hinton-pipeline-docs, jobs/* → /workspace/video-jobs/).
3. Nói với bot: "Đọc /workspace/hinton-pipeline-docs/HINTON_BOOTSTRAP.md và BO-NHO.md, làm bot điều phối Hinton". Bot sẽ tạo lại hoặc nhận các bot con theo BOTS.md.
4. Giọng OmniVoice và AI-auto-generate-video vẫn cài từ gói hinton-media-full.zip (restore/install-all.sh) như cũ.

## Lưu ý dung lượng
Gói này bỏ hinton-pipeline-docs/assets (khoảng 116 MB, giọng mẫu và tài nguyên) và edit-video (phần trợ lý edit, anh không dùng). Hai thư mục đó đã có sẵn trong hinton-media-full.zip trên Drive; khi khôi phục, giải nén gói gốc trước rồi chép gói này đè lên.
