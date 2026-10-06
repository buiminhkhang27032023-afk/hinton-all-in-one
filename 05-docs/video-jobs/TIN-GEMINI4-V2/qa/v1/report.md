# Report — TIN-GEMINI4-V2 v1

## Delivery
- Finished from **existing** `lam-viec/render/video.mp4` (no full re-render).
- `deliver.sh` → `output/v1/` (1080p + 720p + srt + voice).

## Varun QA
- **TỔNG: KHÔNG ĐẠT (19/20)**
- Chỉ fail: Safe zone — overlay `big="MẠNH CỠ NÀO?"` rộng 1573px (QA yêu cầu nửa khung ≤980px sau glow).
- Để ĐẠT cần re-render với `big="MẠNH?"` (hoặc chữ ngắn hơn) trên câu hook “Vậy nó mạnh cỡ nào?”.

## Gaps vs sample Varun
- Captions: `cap_top=1465` (bottom-ish safe); chip_y=1385 — OK vs sample bottom zone.
- Presenter: face 9.8% (5 lần), full-frame evidence 90.2% — đạt mật độ; presenter không full-frame (crop kallaway face_full_px=420).
- Evidence density: 36 insert/phút, 38 visual khác nhau — đạt.
- Safe-zone big text: lệch sample (chữ lớn tràn cạnh).
