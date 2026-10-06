# LESSONS — Bot 4 Douyin (2a3d7c26-345d-4890-8aec-e4ed5d573d88)
Nguồn: role + persona (không có job Douyin trên account này trong HM-101/HM-103; bộ nhớ không truy cập được bằng file).
- Tải Douyin bằng Edge headless chế độ khách trên PC DESKTOP-VHMVQSR: `cd %USERPROFILE%\hinton-douyin` → `.\venv\Scripts\python.exe grab.py <ids>` → copy vào `/workspace/video-jobs/<job>/source`. Xem douyin-downloader/HUONG-DAN-GRAB.md.
- Thiếu RAM: không whisper large/medium; lấy lời gốc từ phụ đề cứng.
- Transcript tiếng Trung có timestamp, `[KHÔNG RÕ]` khi không nghe rõ; dịch ý nghĩa, SRT sidecar. Không bịa thoại, không burn sub, không TTS.
- Handoff `JOB|status|version|path|next` → next Bot5 rồi Bot3.
