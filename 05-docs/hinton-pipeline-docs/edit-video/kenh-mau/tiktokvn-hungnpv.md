# HungNPV (TikTok VN)

- URL: https://www.tiktok.com/@hungnpv
- Followers: 487.100, likes 4,1M, 525 video. Nguồn: HTML profile TikTok (đã kiểm chứng), lấy ngày 03/10/2026 khoảng 16:45 ICT
- Chủ đề (1 dòng): AI cho dân văn phòng (Canva, Excel, Gemini, ChatGPT). Thời lượng trung vị 1:57 (60 video gần nhất, lấy bằng yt-dlp)
- Top video: 642,5K view https://www.tiktok.com/@hungnpv/video/7616786351685405973 · 214,3K view …/7654555020423204117 · 197,3K view …/7617129356313251093

## Video đã tải để học (chỉ học nội bộ, không reup)
| Video | Thời lượng | View | Contact sheet | Hook 0–3s |
|---|---|---|---|---|
| /workspace/video-learn/tiktok-hungnpv/7616786351685405973.mp4 | 149s | 642,5K | /workspace/video-learn/tiktok-hungnpv/7616786351685405973_sheet.jpg | …/7616786351685405973_hook.jpg |
| /workspace/video-learn/tiktok-hungnpv/7654555020423204117.mp4 | 95s | 214,3K | /workspace/video-learn/tiktok-hungnpv/7654555020423204117_sheet.jpg | …/7654555020423204117_hook.jpg |

Frames: `frames/<id>/1fps`, `frames/<id>/scene` (scene>0.3), `frames/<id>/scene_times.txt`.

## Cách dựng / bố cục
**[QUAN SÁT]** = thấy trực tiếp trên frame hoặc contact sheet. **[SUY LUẬN]** = đoán, chưa kiểm chứng.

- **Khung hình [QUAN SÁT]:** dọc 9:16, không chia đôi màn hình. Có 2 loại cảnh:
  - (a) Selfie camera trước, quay ở nhà (rèm hoa phía sau). Mặt chiếm khoảng 60% khung.
  - (b) Dùng điện thoại quay thẳng màn hình laptop/monitor. Đây là camera thật, không phải screen record: thấy moiré và tay chỉ vào UI.
- **Caption [QUAN SÁT]:**
  - Ô chữ nhật trắng bo góc, chữ đen đậm sans, 2–3 dòng, đặt ở giữa khung ngang ngực.
  - Cả câu nằm cố định trong một ô, không chạy từng chữ, không có màu highlight.
  - Kiểu caption này giống TikTok native text.
- **Hook 2s đầu [QUAN SÁT]:**
  - Ngay frame 0 đã có ô trắng ghi câu claim "Đừng thiết kế slides với AI trên Canva nữa, dùng AI này với Canva".
  - Đặt ngón tay lên môi (cử chỉ "bí mật"), mặt sát camera, biểu cảm mạnh.
  - Trong 3s đầu không cắt cảnh.
- **Nhịp cắt [QUAN SÁT]:** chậm. Shot trung bình 11,5s và 7,9s (scene detect ở ngưỡng 0,12, có thể bỏ sót jump cut). Gần như không zoom hậu kỳ. Phần thân video là quay màn hình liên tục.
- **Đồ hoạ trên màn hình [QUAN SÁT]:**
  - Nhãn bước dạng ô trắng nhỏ ("B1: Vào AI này", "B2: Tạo hình AI").
  - Chấm vàng đánh dấu chỗ click.
  - Không có mock UI, icon hay mũi tên động phức tạp.
- **Chuyển cảnh [QUAN SÁT]:** cắt thẳng (hard cut), không có hiệu ứng chuyển cảnh.
- **Nhạc/sfx [SUY LUẬN]:** chưa phân tích audio. Khả năng cao là chỉ có giọng nói, có thể kèm nhạc nền nhỏ.
- **Outro/CTA [QUAN SÁT]:** quay lại cảnh selfie, ô trắng "Follow để xem thêm" (dạng Follow for more).

## Bài học cho Hinton Media
1. Kiểu "lo-fi đáng tin": selfie + ô chữ trắng nêu claim ngay frame 0. Rẻ, dễ tự động hoá, hợp với tệp dân văn phòng VN.
2. Nhãn bước B1/B2 kèm chấm click giúp người xem làm theo được. Editor bot chỉ cần một template ô trắng.
3. Nhịp chậm vẫn đạt 642K view, tức nội dung "mẹo dùng được ngay" quan trọng hơn hiệu ứng. Nhưng không nên học nhịp này cho video tin tức.
