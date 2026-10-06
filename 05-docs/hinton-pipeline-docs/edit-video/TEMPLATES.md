# TEMPLATES — preset dựng video (Hinton)
Cập nhật 03/10/2026 (ICT). Mỗi preset = bộ thông số đo từ kênh mẫu + code chạy được trong `/workspace/AI-auto-generate-video`.

## Preset KALLAWAY (`"preset": "kallaway"`) — tin AI nhịp nhanh, split B-roll/mặt
- **Khi dùng:** tin AI nóng 20–90s có người dẫn (presenter video), muốn nhịp ~1,7s/shot, caption burn 2 chữ, nhạc nền nhỏ.
- **Tham chiếu:** Kallaway 7645299083573267742 (cắt/phút 23,9/29,7 · shot trung vị 1,56s · cắt đầu 1,17s · caption y 1010, cao 58px, #DFAD12, 2 chữ/cụm · LUFS −14,4). Bản tự học: `/workspace/video-jobs/EDIT-SELFTRAIN-01/` (so sánh `qa/SO-SANH-kallaway-7645-vs-hinton.jpg`, lệch `qa/DIEM-LECH.md`).
- **Code:** `pipeline/kallaway/` — `build.py` (entry), `autoplan.py` (beat list), `render.py` (compositor numpy/OpenCV/Pillow → ffmpeg), `mix.py` (voice/BGM/sfx + loudnorm 2-pass), `voice.py` (cắt ngừng), `fx.py` (đồ hoạ tự vẽ: terminal, escape, killswitch, checklist, textcard, dotgrid), `audio_assets.py` (tự tổng hợp whoosh/pop/hit/click/scan + nhạc 120 BPM, CC0 → `assets/kallaway/`). Chạy trong render lock qua `run.sh`.

### Thông số (khung 1080×1920, 30fps)
| Hạng mục | Giá trị |
|---|---|
| Bố cục S | B-roll 1080×960 trên (y 0–960); mặt dưới: mặt rộng `face_split_px`=270px, tâm mặt y = 960+`s_eye_y`(320), x=540; push-in 3%/s |
| Bố cục F | full face, mặt ~330px × zoom 1,15/1,20 luân phiên, tâm mặt (540, 650); kèm 1 chữ to |
| Presenter | `presenter.video`; tự cropdetect bỏ viền đen + Haar face (cache `lam-viec/kallaway_presenter.json`); mỗi shot lấy đoạn kế tiếp +0,4s (jump-cut), không lip-sync |
| Nhịp | `shot_target` 1,7s, `shot_min` 0,9, `shot_max` 3,2; cắt đúng đầu từ, ưu tiên đầu câu; F mỗi `punch_every` 6,5s, giữ `f_hold` ≥1,3s; shot cuối = B-roll shot đầu (loop) |
| Caption | Fraunces Black 50px (#E0AC1A, viền đen 5px, bóng), mép trên y=1008, 2 chữ/cụm (ngắt ở dấu câu), cụm nối liền; pop 0,8→0,94→1,08→1,04→1,0 trong 5 frame; ẩn khi có chữ to |
| Chữ to | Be Vietnam Pro Black 190px trắng glow (hoặc Dancing Script vàng), tâm y≈1140, vào 6 frame scale 1,2→1 + blur 8→0, tối đa 840px rộng |
| Tiêu đề hook | `title` "Dòng 1\|Dòng 2" → IN HOA, Be Vietnam Pro Black 96px (tự thu nhỏ để hộp ≤780px), dòng 2 #E0AC1A, hộp tối viền + glow #CF2C4E, đáy y≈950, wipe trái→phải 1,2s, giữ 2,4s |
| Sfx | whoosh t=0 + mỗi lần vào F (−0,12s); hit ở mỗi chữ to; pop mỗi ~4 cắt S→S; scan cho fx dotgrid (≈25–30% cắt có sfx) |
| Nhạc | `bgm:true` (mặc định nhạc tự tổng hợp hoặc `bgm_path`), `bgm_volume_db` −18…−20 dưới giọng; ngắt nhạc 0,6s trước câu mở đầu "Nhưng/Tệ hơn/Vì sao/Bài học…" |
| Giọng | OmniVoice clone v2 speed 1.2 (pipeline); cắt mọi khoảng ngừng >0,2s về 0,2s (`max_pause`/`keep_pause`) |
| Loudness | −14 LUFS, true peak −2,0 (`kallaway.tp`) → đo ra ≈ −1,9 dBTP sau AAC |

### Cách tạo video mới
```bash
mkdir -p /workspace/video-jobs/<JOB> && cd /workspace/video-jobs/<JOB>
# script.txt (tiếng Việt, số viết bằng chữ) + config.json:
{"job_id":"<JOB>","preset":"kallaway","title":"Dòng 1|Dòng 2","captions_burn":true,"bgm":true,"bgm_volume_db":-18,
 "target_duration":60,"presenter":{"video":"/workspace/hinton-pipeline-docs/assets/presenter-video-novoice.mp4"},
 "footage":{"stock_enabled":false}}
# tuỳ chọn: broll_urls.txt (yt-dlp "URL start-end"), screenshot_urls.txt, screenshots/,
#   bigwords.txt  ("cụm nói => CHỮ TO", mỗi dòng 1 lần punch-in),
#   caption_map.txt ("hai trăm triệu => 200 triệu" — hiện số trong caption),
#   beats.json (beat list thủ công neo theo chỉ số từ: chunks/shots/bigwords/sfx/music_dips — mẫu: EDIT-SELFTRAIN-01/kallaway-job/beats.json)
cd /workspace/AI-auto-generate-video && ./run.sh /workspace/video-jobs/<JOB>
```
Ra: `output/storytelling_final.mp4` (1080×1920) + `storytelling_mobile_720p.mp4`, `qa/report.md`, `lam-viec/kallaway_plan.json`.
QA nhanh: `/workspace/video-jobs/EDIT-SELFTRAIN-01/tools/qa_metrics.sh out.mp4`; so sánh: `tools/compare_sheet.py ref_sheet.jpg out.mp4 out.jpg "REF" "OUR"`.

### Gap đã biết so với Kallaway
- Chưa có PIP mặt tròn trái-trên và mockup điện thoại 3D; B-roll động phụ thuộc nguồn (YouTube tải đoạn từ box hay bị chặn → dùng ảnh chụp + clip CC + fx).
- Caption đo 62px (ref 58), màu hơi tối; nhạc nền liên tục 90% (ref 94,5%).
- Chữ to tự động (không có bigwords.txt) chọn từ theo heuristic (số/viết hoa/dài) — nên viết bigwords.txt.
- WhisperX align (wav2vec2-VI) hay "gãy" timing ở câu có tên Latin → pipeline tự fallback faster-whisper word timestamps (align.py).

### Tùy chọn kallaway bổ sung (từ EDIT-FULL-01)
- `first_cut` (mặc định 1.3s): độ dài shot đầu, để cắt lần đầu ≤1.6s.
- `first_broll`: đường dẫn ảnh key-visual cho shot 1 và shot loop cuối.
- `skip_demo`: danh sách index clip demo (theo footage.json) bị bỏ vì có chữ in sẵn hoặc title card.
- `demo_trim`: {"idx": giây}, bỏ phần đầu clip (ví dụ chữ đang cuộn ra).
- Textcard giờ lấy cụm caption (sau caption_map), ưu tiên cụm có chữ hoa hoặc số.

## VARUN (full-frame evidence) — preset `varun` (EDIT-FULL-01 v3, 04/10/2026)
Mẫu: Varun Mayya R2nesxy7uYU. Code: `pipeline/kallaway/varun.py` (gọi từ `kallaway/build.py` khi `"preset": "varun"`; dùng chung voice-tighten, caption 2 chữ, mix).
- Job cần `varun_beats.json`: `hook` {lines, t0, t1, top} + `shots[]`, mỗi shot `at` = `"S5:hình"` (từ đầu tiên của câu 5) / `"S7:hai#2"` / `"S3.4"` + `type`:
  - `web`: ảnh chụp (khung trình duyệt + URL), `ocr` json, `hl`: [{find:"cụm chữ", style: marker|underline|box}] → tự zoom vào dòng (~55px chữ), dòng dài thì pan trái→phải; `focus`/`z1` cho shot tổng quan; `crop_bottom` cắt banner cookie.
  - `phone`: post X (ảnh embed `platform.twitter.com/embed/Tweet.html?id=`) trong khung điện thoại + highlight.
  - `photo`: chân dung, `face`:[fx,fy], `name`/`role` → lower-third vàng/đen.
  - `stat`: card chữ động nền lưới đen + ô đỏ (kiểu Varun), `lines`[{text,size,color,at,strike}].
  - `clip`/`render`: video (`ss`, `mode` cover|fit, `cx`, `zoom`); render protein 3D bằng `tools/protein_render.py` (CPU, PDB/AlphaFold DB, spacefill|tube, màu cpk|chain|rainbow|plddt).
  - `face`: người dẫn full khung (chỉ hook / chuyển ý / kết), `big` = chữ to.
  - `label` = chip nguồn (tự co ≤870px), `credit` → CREDITS.
- Tự động: whip/zoom mỗi `kallaway.whip_every` (5s, khoảng 4–6s), sfx = whoosh ở mỗi chuyển cảnh + pop ở stat; transitions blend shot trước không kèm chữ.
- Công cụ: `tools/ocr_lines.py` (rapidocr, chạy bằng /workspace/.cv-venv), `tools/varun_qa.py` (đo % mặt / insert/phút / số hình khác nhau / lặp / transitions), `tools/sheet24_compare.py` (24 khung tham chiếu vs mình).
- `screenshot_urls.txt` hỗ trợ `URL | name=x | w=1100 | h=2600 | scale=2 | wait=12000 | timeout=60`; config `output_subdir` giữ bản cũ (output/v3/, qa/v3/).
- YouTube trên box: cần `--js-runtimes node --remote-components ejs:github` (node ở ~/.local/bin) — đã tải được clip chính thức Nobel/DeepMind/AP.

> **Cập nhật v4 (EDIT-PACK-01):** quy trình đầy đủ nằm trong `QUY-TRINH-VARUN.md`.
> - Script dùng cue `[HÌNH: …]` theo từng câu. Không cần `varun_beats.json` nữa: file này chỉ còn là cách viết tay, nếu có thì cue bị bỏ qua.
> - Có thêm kiểu shot `split` (2 hình bằng chứng xếp trên/dưới, không mặt).
> - Mặt người dẫn rải đều, cách nhau 10–20 s.
> - Chạy 1 lệnh `./run.sh <job>`. QA `tools/varun_qa.py` in ĐẠT/KHÔNG ĐẠT, có mục trượt thì exit ≠ 0.
