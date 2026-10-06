# Hinton Media: bộ nhớ và bài học (bố của các bot), cập nhật 03/10/2026

## Quy tắc cố định
- Có 5 bot cố định: Bot5 Săn tin, Bot4 Douyin, Bot3 Biên kịch, Bot2 render Tin AI, Bot2B render Douyin. ID xem trong bots/ và hinton-pipeline-docs.
- Batch N video: tạo N bot tạm, mỗi bot làm 1 video. Xong batch thì user tự xoá các bot tạm trong sidebar (chuột phải → Delete).
- Điều phối viên giao việc cho bot con, không tự làm thay.
- Chọn chủ đề đang hot ở nước ngoài hoặc trên YouTube có lượt xem cao, không trùng nội dung đã làm.
- Giọng đọc: giọng nam v2, clone từ mp3 của user, tốc độ 1.2 (omnivoice/voice-lock-vn-v2.wav + .ref.txt). Script khoảng 250–270 âm tiết thì ra 52–59 giây (đo thật: 54s, 52s, 59s).
- Xưng hô với user: gọi "anh", xưng "em". Không xưng "bố" với user.
- Handoff giữa các bot theo mẫu: JOB|status|version|path|next.

## Luồng việc
- Tin AI: bố → Bot5 research → chọn → Bot3 viết script → bố QA → Bot2 render.
- Douyin: bố → Bot4 chọn và tải → Bot5 kiểm chứng → Bot3 viết script → bố QA → Bot2B render.
- Tải Douyin: chạy Edge headless chế độ khách trên PC của user (DESKTOP-VHMVQSR):
  cd $env:USERPROFILE\hinton-douyin; .\venv\Scripts\python.exe grab.py <ids>
  Sau đó copy file vào /workspace/video-jobs/<job>/source.

## Bài học (03/10)
- Không chạy khoảng 25 bot cùng lúc: máy bị load khoảng 80, RAM cạn, tác vụ nền crash và tốn token. Mỗi lần chỉ chạy vài bot.
- Render một cái một lúc: bọc trong flock /workspace/video-jobs/.render.lock, chạy thẳng bằng Shell (nohup, nền), không dùng tác vụ nền.
- Nếu máy thiếu RAM thì không chạy whisper large hoặc medium; lấy lời gốc từ phụ đề cứng.
- QA gọn: đọc storytelling_script.txt, kiểm các caveat, ghi qa/notify.txt, rồi tự nhắn kết quả cho bot.
- Giao video: gửi file 720p kèm 1 dòng chủ đề và thời lượng. Không nhắn tiến độ thừa.
- Dùng Google Drive connector để gom video của batch vào 1 folder.

## Nội dung gói
- hinton-pipeline-docs/: toàn bộ spec, role từng bot, skills (hinton-orchestrate, hinton-render-shorts).
- bots/: profile và cài đặt của tất cả bot (gồm cả bot tạm).
- omnivoice/: server.py, restart.sh, file giọng khoá v2.
- video-jobs-tools/: RENDER-LOCK.md, persona bot tạm, công cụ remix Douyin (build.py, tts.py, config).
- deliver.sh, render-repo.txt: script giao video và repo render AI-auto-generate-video.
