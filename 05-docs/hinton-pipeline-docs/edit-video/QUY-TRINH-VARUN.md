# QUY TRÌNH DỰNG VIDEO KIỂU VARUN (preset `varun`): từ script có [HÌNH] đến file 720p

Bản mẫu được duyệt là EDIT-FULL-01 v3. Bản kiểm chứng quy trình là **v4**: dựng bằng 1 lệnh và QA đạt 20/20.
Đầu ra: `/workspace/video-jobs/EDIT-FULL-01/output/v4/storytelling_mobile_720p.mp4`.
Kiểu dựng mô phỏng video Varun Mayya R2nesxy7uYU. Mỗi câu nói có 1–3 hình bằng chứng full-frame, mỗi hình dài 1–2 s. Mặt người dẫn chỉ xuất hiện ở hook, ở các chỗ chuyển ý và ở cuối video.

## 0. Lệnh chạy

```bash
cd /workspace/AI-auto-generate-video
./run.sh /workspace/video-jobs/<job>
.venv/bin/python tools/varun_qa.py /workspace/video-jobs/<job> --sub <vN>
```

- Lệnh đầu chạy cả quy trình (one-shot). Phần TTS và phần render tự chạy trong `flock /workspace/video-jobs/.render.lock`.
- Lệnh thứ hai chạy lại riêng bước QA. Lệnh `run.sh` đã tự gọi bước này ở cuối.

Các bước `run.sh` thực hiện khi config có `"preset": "varun"`:

1. **prep** (không lock):
   - Chụp `screenshot_urls.txt` bằng Chrome headless.
   - Gọi `varun_assets.fetch`:
     - Clip trong `broll_urls.txt` tải bằng yt-dlp hoặc curl+ffmpeg.
     - Ảnh chân dung trong `portraits.txt` lấy từ Wikimedia.
     - File PDB/AlphaFold lấy cho mọi cue `render:`.
     - OCR toàn bộ ảnh chụp màn hình.
2. **render** (trong flock):
   - Bỏ cue khỏi script rồi gửi đi TTS OmniVoice (clone giọng nam v2, speed 1.2, cache theo từng câu).
   - Căn thời gian từng chữ (align), rồi cắt bớt khoảng nghỉ (tighten).
   - `varun_assets.resolve` đổi các cue thành shot, ghi ra `lam-viec/varun_beats.auto.json`. Bước này cũng render protein (cache trong `lam-viec/renders/`).
   - `varun.build_plan`:
     - Mốc thời gian của từng shot.
     - Tự đặt whip/zoom.
     - Cảnh báo nếu hai lần lên mặt cách nhau dưới `face_min_gap`.
   - `varun.render`: dựng 1080x1920, 30 fps.
   - `mix`: BGM −20 dB, sfx, chuẩn hóa loudness về −14 LUFS.
   - Xuất file 720p.
   - Ghi báo cáo và ticket.
   - Tạo ảnh so sánh 24 khung với Varun và chạy **QA tự động**. QA KHÔNG ĐẠT thì ticket ghi `Lỗi QA` và `run.sh` thoát với mã 3.

Đầu ra nằm trong `output/<output_subdir>/` (gồm `storytelling_final.mp4` và `storytelling_mobile_720p.mp4`). Phần QA nằm trong `qa/<output_subdir>/`:
- `QA-<sub>.md`, `varun_qa.json`, `varun_plan.json`
- `SO-SANH-varun-R2nesxy7uYU-vs-<sub>.jpg`
- `report.md`, `ticket.txt`

Dựng lại bản mới mà không mất bản cũ: đổi `output_subdir` và `version`. Voice, căn chữ, ảnh chụp, clip, ảnh chân dung, file PDB và render protein đều được cache nên không tải hay tạo lại.

## 1. Thư mục job

| File | Bắt buộc | Nội dung |
|---|---|---|
| `script.txt` | ✓ | Mỗi dòng 1 câu nói, cue `[HÌNH: …]` đặt ở cuối dòng. Dòng bắt đầu bằng `#` là ghi chú. Cue không được đọc thành tiếng. |
| `config.json` | ✓ | Xem mục 1.2 |
| `screenshot_urls.txt` | nếu có `web:`/`phone:` | `URL \| name=<tên> \| w=1100 \| h=2200 \| scale=2 \| wait=12000`. Ảnh ra ở `lam-viec/webshots/<tên>.png`, OCR ở `…/ocr/<tên>.json` |
| `broll_urls.txt` | nếu có `clip:` | `URL \| name=<tên> \| credit=… [\| sections=*12-40] [\| format=…]`. Clip ra ở `lam-viec/yt/<tên>.mp4`. URL là YouTube/X thì tải bằng yt-dlp, URL mp4/webm trực tiếp thì tải bằng curl + ffmpeg |
| `portraits.txt` | nếu có `photo:` | `<tên> \| file=<tên file Commons> \| credit=…` hoặc `<tên> \| url=https://… \| credit=…`. Ảnh ra ở `lam-viec/portraits/<tên>.jpg` |
| `caption_map.txt` | tùy chọn | `lời đọc => chữ hiển thị`, ví dụ số và tên riêng |
| `varun_beats.json` | tùy chọn | Danh sách shot viết tay. Nếu có file này thì cue bị **bỏ qua**, nên muốn dùng cue thì đổi tên nó |

### 1.1 Cú pháp cue `[HÌNH: …]`

Các mục trong cue cách nhau bằng `;`. Một mục có dạng:

```
kind[:ref]  ["chữ cần tìm"[/marker|/underline|/box] …]  [@chữ-neo[#n]]  [key=value …]
```

- `@chữ` chỉ định shot bắt đầu đúng lúc đọc chữ đó, trong cùng dòng. `#2` là lần xuất hiện thứ hai của chữ đó trong dòng.
- Mục không có neo được rải đều trong câu và bắt vào đầu một chữ. Mục đầu tiên của dòng bắt đầu ở chữ đầu tiên của câu.
- Mỗi mục kéo dài đến lúc mục kế tiếp bắt đầu. **Neo phải chọn sao cho mỗi mục dài 1–2 s** (lấy mốc thời gian từ `lam-viec/words_tight.json`, file này có từ lần chạy đầu tiên, kể cả khi script chưa có cue).

| kind | Hình | key hay dùng |
|---|---|---|
| `web:<tên>` | Ảnh chụp đặt trong khung trình duyệt (thanh URL lấy từ `screenshot_urls.txt`). Camera zoom/pan vào dòng chữ, OCR tìm `"chữ"` để tô vàng (`marker`) hoặc gạch chân/đóng khung (`underline`/`box`) | `focus=x,y,w,h` (vùng trên ảnh gốc), `z1=` (độ rộng khung nhìn, px), `zr=`, `cy=`, `crop_bottom=`, `label=` |
| `phone:<tên>` | Bài X đặt trong khung điện thoại | `z1=1500 zr=1.12 cy=0.4 label="X · @handle"` |
| `photo:<tên>` | Ảnh chân dung, tự dò vị trí mặt, kèm lower third `"Tên\|Chức danh"` | `face=fx,fy`, `zoom=` |
| `clip:<tên>` | Clip chính thức | `ss=` (giây bắt đầu), `mode=cover\|fit`, `zoom=`, `cx=`, `cy=` |
| `render:<PDB\|AF-UNIPROT>` | Protein 3D quay (`tools/protein_render.py`) | `style=spacefill\|tube`, `color=cpk\|chain\|rainbow\|plddt`, `bg=dark\|light\|navy`, `fill=`, `deg=`, `file=<mp4 có sẵn>` |
| `stat` | Thẻ số liệu kinetic: nền lưới đen, ô đỏ. Các chữ xen kẽ số lớn và chú thích vàng | `size=`, `seed=`, `strike=1` (gạch ngang), `label="Nguồn: …"` |
| `face` | Mặt người dẫn full-frame | `zoom=`, `big="VÌ SAO?"` (chữ to thay cho phụ đề) |
| `split` | **2 hình bằng chứng xếp trên/dưới (1080x960 mỗi nửa), không có mặt** | `top=kind:ref bottom=kind:ref`. `"chữ 1"` thuộc nửa trên, `"chữ 2"` thuộc nửa dưới (`-` là bỏ trống). Option cho từng nửa đặt tiền tố `top_`/`bottom_` (ví dụ `top_label=`, `bottom_style=tube`, `top_crop_bottom=700`, `top_focus=…`) |

Ví dụ (lấy từ EDIT-FULL-01 v4):

```
Nửa còn lại thuộc về giáo sư David Baker, với công trình thiết kế protein bằng máy tính. [HÌNH: web:kva "Chemistry 2024 with one half to" "David Baker, University of Washington" crop_bottom=700 label="kva.se" ; photo:baker "David Baker|ĐH Washington · Seattle" @David ; split @công top=web:kva bottom=render:1QYS "In 2003, David Baker succeeded in using these blocks to design" top_crop_bottom=700 bottom_style=tube bottom_color=rainbow bottom_bg=navy bottom_label="Top7 · protein thiết kế bằng máy tính"]
Vì sao chuyện này quan trọng? [HÌNH: face zoom=1.12 big="VÌ SAO?"]
```

Cách split hiển thị:
- Nửa `web`/`phone` có zoom rộng hơn (1000–1400 px). Ở nửa trên, dòng chữ chính nằm giữa nửa. Ở nửa dưới, dòng chữ chính nằm ở y≈1210, trên vùng phụ đề.
- Nửa `render` được thu nhỏ trên nền mờ.
- Giữa hai nửa có vạch chia ở y=960.
- Mỗi nửa có chip nguồn riêng: nửa trên ở y≈864, nửa dưới ở y=1478.

### 1.2 `config.json`

```json
{ "job_id": "EDIT-FULL-01", "version": "v4", "output_subdir": "v4", "preset": "varun",
  "title": "AI giành Nobel|Hóa học 2024",
  "captions_burn": true, "bgm": true, "bgm_volume_db": -20,
  "presenter": {"mode": "auto", "video": "/workspace/hinton-pipeline-docs/assets/presenter-video-novoice.mp4"},
  "kallaway": {"tail": 0.25, "face_full_px": 420, "f_eye_y": 700},
  "varun": {"hook_hold": 1.94, "face_min_gap": 10.0, "whip_every": 5.0,
            "qa": {"face_max_gap": 20.0, "face_hook_max": 3.0, "min_splits": 2}},
  "footage": {"stock_enabled": false} }
```

- `title` là chữ hook (2 dòng, ngăn bằng `|`), hiện trong `hook_hold` giây.
- Khối `varun` ghi đè lên `kallaway`.
- `varun.compare_ref` (tùy chọn) đổi video tham chiếu dùng cho ảnh so sánh.

## 2. Tìm và lấy bằng chứng

1. **Trang web.**
   - Thêm URL vào `screenshot_urls.txt` (Chrome headless, `scale=2`; trang nhiều JS thì đặt `wait=12000`).
   - Mở PNG kiểm tra. Trang bị paywall, captcha hay hộp cookie thì không dùng (trường hợp Reuters/Guardian ở v3). Tìm bài đăng lại, ví dụ trên Rappler.
   - Câu trích dẫn trong cue phải **khớp với OCR**. OCR đọc "AI" thành "Al". Kiểm tra trong `lam-viec/webshots/ocr/<tên>.json`.
2. **Bài X.** Chụp bản embed `https://platform.twitter.com/embed/Tweet.html?id=<id>&theme=light&lang=en` với `w=560 scale=3`, rồi dùng `phone:<tên>`.
3. **Ảnh chân dung Wikimedia.**
   - Dùng `portraits.txt` với `file=<tên File:…>`. Ảnh được tải qua `Special:FilePath/<File>?width=1400`, nghỉ 3 s giữa các lần tải vì API Commons giới hạn tốc độ.
   - Ghi credit đúng tác giả và giấy phép (ví dụ CC BY-SA 4.0).
4. **Clip chính thức.**
   - `broll_urls.txt` gọi `/workspace/.ytdlp-venv/bin/yt-dlp --js-runtimes node --remote-components ejs:github`. Node phải có trong `~/.local/bin`, `run.sh` đã thêm thư mục này vào PATH.
   - Thiếu flag trên thì YouTube trả lỗi "n challenge"/403.
   - Video dài thì dùng `sections=*a-b`.
   - Để tìm cảnh, xem contact sheet với `ffmpeg -vf fps=1/5,scale=320:-1,tile=6x6`, rồi đặt `ss=`.
5. **Thẻ số liệu.** Dùng `stat` với số lớn và chú thích ngắn, kèm `label="Nguồn: …"`. Số phải là số đã kiểm chứng.
6. **Hình tạo ra.**
   - `render:<PDB>` lấy file từ RCSB.
   - `render:AF-<UniProt>` lấy model từ AlphaFold DB (v6→v4). Model AF nên dùng `color=plddt`.
   - Loại hình tạo ra khác (biểu đồ, thẻ trích dẫn) dùng `stat` hoặc render ra mp4 rồi khai báo dạng `clip`/`render file=`.
7. **CREDITS.** Mỗi shot đều mang `credit`. Danh sách credit nằm ở mục "Nguồn footage" trong `qa/<sub>/report.md`; chép mục này sang `CREDITS-<sub>.md` khi đăng.

## 3. Chỉ tiêu bắt buộc (QA tự kiểm tra, mục nào trượt thì exit ≠ 0)

| Chỉ tiêu | Mục tiêu |
|---|---|
| Evidence full-frame | ≥75% thời lượng |
| Mặt người dẫn | ≤25%. Chỉ ở hook (≤3 s), ở đầu câu chuyển ý (`[MẶT]`) và shot cuối. **Rải đều: khoảng cách giữa hai lần lên mặt từ 10 đến 20 s** |
| Insert | ≥30/phút. Mỗi insert dài 0.95–2.05 s và khớp đúng câu đang đọc |
| Hình khác nhau | ≥25 cho mỗi 60 s. Mỗi **hình** dùng tối đa 2 lần (tức lặp tối đa 1 lần). Một hình = cùng file + cùng mốc clip (±1 s) + cùng câu tô vàng. Đoạn khác của cùng trang hoặc cảnh khác của cùng clip là hình khác. QA in thêm file dùng nhiều nhất |
| Split 2 bằng chứng | ≥2 lần mỗi video (`min_splits`), không có mặt |
| Mỗi câu có hình | Mọi câu có ít nhất 1 evidence. Riêng câu `[MẶT]` ngắn (≤3 s) được phép chỉ có mặt |
| Whip/zoom | Cách nhau 4–6 s (tự đặt) |
| SFX | Nhẹ, ≤16 lần/phút. Build tự bỏ bớt tiếng pop của thẻ số nếu vượt (`varun.sfx_per_min`) |
| Âm thanh | −14 LUFS ±0.5, true peak ≤ −1 dBTP |
| Định dạng | Bản gốc 1080x1920 30 fps, có file 720x1280 |
| Safe zone | Không có chữ ở y<150, y>1590 hoặc x>940. Phụ đề rộng tối đa 780 px, chip tối đa 870 px |
| Dấu tiếng Việt | Mọi ký tự hiển thị đều có trong font Be Vietnam Pro. Font này không có `β` và `→`: viết "Beta-" và "đến" |

Quy tắc rải mặt người dẫn:
- Lần 1 ở hook: một chữ trong câu 1, hoặc câu bẻ lái thứ 2 nếu câu này bắt đầu trước giây 3 (`qa.face_hook_max`).
- Khoảng 1 lần cho mỗi chuyển ý. Đặt `face` làm mục **đầu tiên** của câu chuyển ý, kèm `big=` nếu là câu hỏi.
- Lần cuối là shot cuối cùng (câu kết/CTA).
- Hai lần liên tiếp cách nhau 10–20 s. Không dồn các lần lên mặt về cuối video.

## 4. QA tự động và ảnh so sánh

```bash
.venv/bin/python tools/varun_qa.py /workspace/video-jobs/<job> --sub v4
.venv/bin/python tools/sheet24_compare.py /workspace/video-learn/youtube-VarunMayya/R2nesxy7uYU.mp4 \
    /workspace/video-jobs/<job>/output/v4/storytelling_final.mp4 qa/v4/SO-SANH-varun-R2nesxy7uYU-vs-v4.jpg "VARUN R2nesxy7uYU" "<job> v4"
```

- Lệnh QA in bảng ĐẠT/KHÔNG ĐẠT và ghi ra `qa/v4/QA-v4.md` và `varun_qa.json`.
- Lệnh so sánh tạo ảnh 24 khung chia đều của mỗi video (lưới 4x6), đặt cạnh nhau. `run.sh` đã tự chạy cả hai lệnh.
- QA không thay được việc xem bằng mắt. Mở ảnh so sánh và contact sheet, kiểm tra:
  - Mỗi hình đúng với câu đang đọc.
  - Chữ được tô vàng đúng dòng.
  - Phụ đề không che dòng chữ chính.
  - Split rõ cả hai nửa.

## 4b. Mẹo khi đặt cue
- Ảnh tĩnh (png/webp/jpg, ví dụ ảnh CDN của hãng) cũng khai trong `broll_urls.txt`. Prep tự đổi ảnh sang mp4 1 khung. Dùng `clip:<tên> mode=fit zoom=1.0–1.6`.
- Clip/ảnh nằm trong split: đặt `top_mode=fit top_zoom=1.0`, ảnh sẽ được canh giữa nửa khung, nền mờ.
- Trang nền tối (ví dụ openai.com Recap): highlight vàng gần như không thấy, dùng `/underline` hoặc `/box`. Chữ nhỏ (ngày đăng) thì đặt `z1=520`.
- Trang dính paywall khi chụp headless: lưu HTML bằng `curl`, mở qua `python3 -m http.server` ở 127.0.0.1, rồi chụp bằng `google-chrome --headless=new --screenshot`. Khai `url=` trong cue để thanh địa chỉ hiện URL thật.
- Tìm mốc trong keynote dài:
  - Contact sheet `fps=1/30,tile=10x11` để thấy các slide.
  - Nếu yt-dlp tải phụ đề bị 429 thì chạy faster-whisper `small` trên đoạn audio nghi ngờ, **chạy trong flock**.
- Câu thoại nhanh (khoảng 4.7 âm tiết/s): câu 2 s chỉ chứa được 1–2 hình. Đừng nhồi hình, sẽ có insert dưới 1 s.

## 5. Lỗi hay gặp
- `OCR phrase not found`: câu trích trong cue không khớp OCR (ví dụ "AI" bị đọc thành "Al", dấu gạch, hoặc ký tự `‑`). Chép đúng chữ từ file json OCR.
- Insert ngắn hơn 1 s hoặc dài hơn 2 s: dời neo `@chữ` sang chữ khác, hoặc thêm hay bớt một mục.
- "Lặp nguồn tối đa" KHÔNG ĐẠT: hai nửa của một split cũng tính là 2 lượt dùng.
- Không bao giờ `pkill -f` theo một mẫu có trong chính dòng lệnh đang chạy. Không xóa file lock.
