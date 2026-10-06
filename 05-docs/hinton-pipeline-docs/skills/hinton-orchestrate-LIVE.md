---
name: hinton-orchestrate
description: >-
  Dùng khi anh yêu cầu làm video Tin AI hoặc remake Douyin theo pipeline Hinton
  Media.
---
# Skill — hinton-orchestrate

## Khi dùng
User yêu cầu video **Tin AI** hoặc **remake Douyin**.

## Roster (xem /workspace/hinton-pipeline-docs/BOTS.md)
- bố: 9b5b478f-7ec1-4c73-8aeb-f721ec3153fc
- Bot5: dccdedf5-3a17-4677-9623-3e6a441ddde4
- Bot4: ea3a7d5e-ce74-4c35-aa08-2a22d91a6e8e
- Bot3: f4c9ac9f-0715-49df-aaa7-18bb221fd654
- Bot2 Tin AI: c37c25f1-6933-435a-a372-1582f92dbce8
- Bot2B Douyin: 7713f135-8129-4e7f-abe9-501faa4f4cf1
- Trợ Lý Edit Video: 551e61f7-f454-428a-9649-be28d3be5cee

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

## Giọng
OmniVoice male clone v2 speed 1.2; cấm edge-tts/cloud TTS. Script ~250–270 âm tiết. 1 render một lúc (flock).
