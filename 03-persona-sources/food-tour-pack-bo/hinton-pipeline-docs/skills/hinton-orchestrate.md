# Skill — hinton-orchestrate

## Khi dùng
User yêu cầu video **Tin AI** hoặc **remake Douyin**.

## Quy trình
1. Tạo `job-id`, folder job, phiếu `JOB|Đã nhận|v1|path|next`.
2. Route **Tin AI:** Bot5 → bố chọn → Bot3. Route **Douyin:** Bot4 → Bot5 → Bot3.
3. Status: `Đã nhận → Đang xử lý nguồn → Đang viết → Đang sản xuất → Đang kiểm tra → Hoàn thành`.
4. QA script: nguồn, claim, hook, remix, CTA, ~60s; max 2 vòng sửa / bước.
5. Gửi **Bot2 Tin AI** hoặc **Bot2B Douyin** (SendToAgent) kèm path script + yêu cầu **male clone v2 voice lock**.
6. Nhận render/QA; kiểm deliverables; cập nhật `Hoàn thành`.
7. Drive chỉ khi user/bố yêu cầu; trả milestone + link/path cuối.

## Handoff
Mọi tin điều phối: `JOB|status|version|path|next`. Ack ngắn; không dump file. Bị chặn → nêu nguyên nhân + phần đã có.
