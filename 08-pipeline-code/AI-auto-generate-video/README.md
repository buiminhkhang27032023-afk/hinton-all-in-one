# AI-auto-generate-video — pipeline render short tự động (Hinton Media)

Một lệnh: job folder (kịch bản tiếng Việt + config) → video 9:16 1080×1920 30fps + bản 720p + SRT + log + QA report.
Chỉ chạy local, không push lên đâu. Box chỉ có CPU, nên pipeline chạy tuần tự và dùng model nhỏ.

```
script.txt ─► OmniVoice (127.0.0.1:8123, male clone v2, speed 1.2, voice_locked) ─► loudnorm −14 LUFS
          └─► WhisperX align (biết trước kịch bản, CPU, wav2vec2 VI) ─► timing từng từ ─► subtitle.srt
broll_urls.txt ─► yt-dlp (lấy 1 đoạn) ─► PySceneDetect ─► clip 1–3s      ┐
screenshot_urls.txt / screenshots/ ─► Ken Burns / khung browser          ├─► edit plan (cắt đúng đầu từ)
Pexels/Pixabay (chỉ khi có API key) ─► stock theo keyword từng câu      ┘        │
presenter video ─► cropdetect (bỏ viền đen) ─► auto-editor ─► PIP tròn ───────────┤
(fallback: presenter photo ─► crop quanh mặt + "thở"/Ken Burns)                    ▼
                         HyperFrames (HTML+GSAP ─► MP4) ─► deliver.sh (copy + 720p) ─► ffprobe/QA/contact sheet
```

## Chạy nhanh
```bash
cd /workspace/AI-auto-generate-video
./run.sh /workspace/video-jobs/<JOB>            # prep (không lock) + render (trong flock render lock)
./run.sh /workspace/video-jobs/<JOB> --force    # bỏ cache alignment/presenter (TTS vẫn cache theo từng câu)
STAGE=prep ./run.sh <JOB>     # chỉ tải footage / kiểm tra kịch bản
STAGE=render ./run.sh <JOB>   # chỉ TTS + dựng + render (dùng lại footage đã tải)
```
`run.sh` tự bọc bước render trong `flock /workspace/video-jobs/.render.lock` (RENDER-LOCK.md): mỗi lúc chỉ 1 render. Nếu lock đang bận, lệnh sẽ chờ tối đa `LOCK_WAIT` giây (mặc định 3600).
TTS mất khoảng **12s cho mỗi 1s audio**, nên video 60s cần ~12 phút TTS. Như vậy là bình thường. Audio từng câu được cache trong `lam-viec/tts_cache/`, chạy lại sẽ không tốn thời gian TTS cho câu cũ (chỉ câu nào sửa chữ mới phải TTS lại).

## Job folder (input)
```
/workspace/video-jobs/<JOB>/
  script.txt            # BẮT BUỘC. Tiếng Việt, viết số bằng chữ, 250–270 âm tiết ≈ 55–60s. Dòng bắt đầu bằng # bị bỏ qua.
  config.json           # tuỳ chọn, chỉ cần ghi các key muốn đổi so với config.default.json
  broll_urls.txt        # tuỳ chọn: mỗi dòng "URL [start-end]" (giây hoặc mm:ss), ví dụ: https://youtu.be/xxx 0:30-1:10
  screenshot_urls.txt   # tuỳ chọn: URL trang web → Chrome headless chụp màn hình
  screenshots/          # tuỳ chọn: ảnh png/jpg (dùng Ken Burns hoặc khung browser)
  keywords.txt          # tuỳ chọn: mỗi dòng = keyword tiếng Anh cho câu tương ứng (stock search)
```
Các file input đặt ở gốc job hoặc trong `source/` đều được.

## Output
| File | Ý nghĩa |
|---|---|
| `output/storytelling_final.mp4` | 1080×1920 H.264/AAC 30fps |
| `output/storytelling_mobile_720p.mp4` | bản 720p (do `deliver.sh` tạo) |
| `output/subtitle.srt` | phụ đề sidecar (timing từ WhisperX) |
| `output/voice_storytelling.wav`, `output/storytelling_script.txt` | voice + kịch bản |
| `qa/report.md`, `qa/ticket.txt`, `qa/contact_sheet.jpg`, `qa/pipeline.log` | QA, ticket `JOB\|status\|version\|path\|next`, 4 frame, log |
| `lam-viec/` | file trung gian: `tts_cache/`, `words.json`, `plan.json`, `hf/index.html` (project HyperFrames), `render/` |

## Config hay chỉnh (`config.json` của job)
| Key | Mặc định | Ghi chú |
|---|---|---|
| `title` | "" | Tiêu đề hook 2 dòng, ngăn cách bằng `\|`, ví dụ `"AI góp phần giành\|Nobel Hóa học 2024"` |
| `captions_burn` | `false` | `true` = burn caption 2 chữ/cụm (y≈1110, phía trên PIP) |
| `bgm`, `bgm_path`, `bgm_volume_db` | `false`, "", −20 | Nhạc nền, đặt thấp hơn giọng ~20 dB |
| `presenter.video` / `presenter.photo` | "" | `mode: auto` sẽ dùng video nếu có, không có thì dùng ảnh. `none` = tắt presenter |
| `presenter.pip_x/pip_y/pip_size/pip_shape` | 60/1260/300/circle | PIP góc trái dưới, nằm trong vùng an toàn của SO-TAY |
| `presenter.intro_card` / `outro_card` | true | Hook full-frame presenter + tiêu đề; outro có CTA FOLLOW |
| `edit.shot_min/shot_max` | 1.6/3.0 | Độ dài shot (nhịp "Tin AI nóng") |
| `edit.effect_every` | 4 | Cứ mỗi N shot thì chèn 1 hiệu ứng (text card / mockup điện thoại / browser / chữ to) |
| `brand.*` | accent #F5C518… | màu, handle, CTA, chip "TIN AI" |
| `render.workers` | 2 | Mỗi worker là 1 Chrome (~256MB). Nếu RAM thiếu thì đặt 1 |
| `asr_verify.enabled` | true | faster-whisper small int8 nghe lại voice để QA (in độ giống kịch bản) |

Muốn đổi giao diện thì sửa `templates/hinton.css` (toạ độ đã ghi chú theo SO-TAY-DUNG §3.1). Muốn đổi cách dựng thì sửa `pipeline/compose_hf.py`. Muốn đổi nhịp cắt hoặc cách chọn hình thì sửa `pipeline/timeline.py`.

## Quy tắc bắt buộc
- Voice: **chỉ OmniVoice local**. Pipeline kiểm tra `/health` (`voice_locked:true`, ref `voice-lock-vn-v2.wav`, speed 1.2) và header `X-Voice-Locked` của từng câu. Nếu lệch, pipeline tự chạy `restart.sh` rồi làm lại tối đa 2 lần. **CẤM edge-tts và mọi cloud TTS.**
- Không lip-sync. Presenter chỉ là PIP, được cắt thành nhiều đoạn 1.5–3.5s lấy từ các vị trí khác nhau trong clip để người xem không thấy lặp.
- Mặc định không burn caption và không BGM (theo playbook). Chỉ bật khi user yêu cầu.
- Footage từ yt-dlp: chỉ dùng đoạn ngắn và **ghi nguồn**. Danh sách nguồn có sẵn trong `qa/report.md`.

## Cài đặt (đã cài sẵn trên box)
- Node 22 ở `/home/box/.local/bin`. `npm install` cài `hyperframes@0.8.114` + `gsap` (telemetry đã tắt bằng `HYPERFRAMES_NO_TELEMETRY=1`).
- Python 3.12 venv `.venv`: `uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python --extra-index-url https://download.pytorch.org/whl/cpu --index-strategy unsafe-best-match -r requirements.txt`
  (OpenCV phải dùng bản **<5**, vì bản 5 đã bỏ CascadeClassifier.)
- Model: `nguyenvulebinh/wav2vec2-base-vi-vlsp2020` (align) và `Systran/faster-whisper-small` (QA), lưu trong cache HF.
- YouTube: yt-dlp được gọi kèm `--js-runtimes node:/home/box/.local/bin/node`.

## Lỗi thường gặp
- `render lock busy`: đang có bot khác render, cứ để lệnh chờ. Kiểm tra bằng `flock -n /workspace/video-jobs/.render.lock true && echo free || echo busy`.
- `stock footage SKIPPED`: chưa có `PEXELS_API_KEY`/`PIXABAY_API_KEY`. Khi không có footage, pipeline dùng screenshot, clip demo và hiệu ứng thay thế.
- `yt-dlp FAILED`: URL bị chặn hoặc cần đăng nhập. Hãy thay URL khác hoặc bỏ dòng đó.
- Muốn xem hoặc sửa project HyperFrames bằng tay: `cd <JOB>/lam-viec/hf && npx hyperframes preview` (chạy từ thư mục repo để dùng CLI local).
- Clip presenter thử nghiệm: dùng `tools/make_test_pattern.sh` (chỉ để test nội bộ, không bao giờ giao khách).

## Preset `kallaway` (03/10/2026)
`"preset": "kallaway"` trong config.json → không dùng HyperFrames; dựng bằng `pipeline/kallaway/` (split B-roll 1080×960 / mặt dưới, full-face punch-in + chữ to, caption 2 chữ pop, tiêu đề hook wipe, sfx, BGM, loop). Thông số + cách dùng: `/workspace/hinton-pipeline-docs/edit-video/TEMPLATES.md`.
Ghi chú align: nếu WhisperX gãy timing (câu có tên Latin), `align.py` tự chuyển sang faster-whisper word timestamps cho các câu đó.
