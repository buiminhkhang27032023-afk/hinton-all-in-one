# Luồng tối ưu — bố + bot con

## Routing (không nhầm bot)
| Job type | Chuỗi |
|---|---|
| Tin AI | bố → Bot5(find) → bố chọn 1 → Bot3 → bố QA → **Bot2 Tin AI** → bố trả |
| Douyin link/file | bố → Bot4 → Bot5(verify AI) → Bot3 → bố QA → **Bot2B** → bố trả |

## Phiếu 1 dòng (mọi bàn giao)
`JOB|status|version|path|next`
Ví dụ: `HM-009|Đang sản xuất|v3-60s|/workspace/video-jobs/hm-009-adobe-chatgpt|next=bàn giao bố`

## Status chuẩn
`Đã nhận → Đang xử lý nguồn → Đang viết → Đang sản xuất → Đang kiểm tra → Hoàn thành`
(Lỗi / chờ user: `Bị chặn`)

## Default phiếu (đừng hỏi lại)
~60s · 9:16 · **1 giọng OmniVoice male clone v2 lock** @1.2 (Bot2+Bot2B) · SRT sidecar · **không burn karaoke** trừ khi hỏi · local-only · không BGM · Hinton remix · không promote kênh TQ · Drive chỉ khi delivery

## Ai nói gì
- Bot4/5/3: path + tóm tắt ngắn; không dump transcript
- Bot2/2B: path mp4+wav+srt + size + duration + 1 câu QA voice (`OmniVoice · male clone v2 locked · 1.2 · voice_locked:true`)
- Bố → user: chỉ milestone + link cuối; không spam từng ack bot
- Priority true chỉ khi cần hành động; ack = false/im

## Parallel
Douyin + Tin AI chạy song song OK (2B vs 2). Cùng job: không 2 bot viết/render trùng.

## Sửa lỗi
≤2 lần/bước rồi bố báo user + phần đã có.
