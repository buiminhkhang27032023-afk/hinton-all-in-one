# Genre · Format · UI — Hinton Shorts (tóm tắt)

Voice lock: OmniVoice male clone v2 · 1.2 · `voice_locked:true`.

## GENRE
| ID | Genre | Khi dùng |
|---|---|---|
| G01 | Tin AI breaking | Model/tool mới 24–72h |
| G02 | Tool demo / Ads AI | Công cụ sáng tạo |
| G03 | Tips / thực chiến | Mẹo AI cho SME / sale / creator |
| G04 | Listicle Top N | Top 5 / ranking |
| G05 | Storytelling dài | HOOK→…→CTA |
| G06 | Talking-head / multi-clip | Footage mặt người |
| G07 | Douyin remix VN | Nguồn CN → Việt hóa |
| G08 | Bug / lỗi + cách sửa | Chỉ khi user yêu cầu |
| G09 | So sánh A vs B | Model/tool đối đầu |
| G10 | Stat / benchmark | 1 con số hero |

Luồng kể mặc định (G01–G05, G07): **HOOK → bối cảnh → vấn đề → diễn biến → cao trào → kết quả → bài học/CTA**.

## FORMAT
| ID | Format | Engine | Khi chọn |
|---|---|---|---|
| F01 | HyperFrames neon UI | HF templates 9:16 | Không B-roll / cần motion UI |
| F02 | FFmpeg kinetic cards | ffmpeg dark cards | Fallback only |
| F03 | B-roll + VO | ffmpeg montage | Có stock/B-roll |
| F04 | Talking-head editor | hinton-ai-editor-agent | Có raw talking clips |
| F05 | Mobile export pair | ffmpeg 720×1280 | Luôn kèm khi deliver |

Ưu tiên: F01 (listicle/tin không footage) → F04 (mặt người) → F03 (B-roll) → F02 chỉ fallback.

## UI HyperFrames (templateId gợi ý)
- Hook: `frame-liquid-bg-hero` · `frame-bold-poster`
- Body: `frame-glitch-title` · `frame-build-minimal` · `frame-pentagram-stat` · `frame-vignelli` · `frame-aicoding-list` · `frame-aicoding-comparison` · `frame-creative-voltage`
- Outro: `frame-statement-outro` · `frame-logo-outro`

Mix F01 (8–12 scenes): đổi template mỗi 1–2 scene; safe zone TikTok/Reels; karaoke burn **chỉ khi hỏi**.

## MATRIX nhanh
| Genre | Format | UI gợi ý |
|---|---|---|
| G01 | F01 | liquid → glitch/build → pentagram → outro |
| G02 | F01 | liquid → voltage → list → outro |
| G03 | F01/F03 | list + build-minimal |
| G04 | F01 | liquid + list + pentagram ×N + outro |
| G05 | F01/F03 | liquid → bold → glitch → build → outro |
| G06 | F04 | captions optional |
| G07 | F01/F03 | remix; không logo kênh nguồn |
| G09 | F01 | ≥1 scene `aicoding-comparison` |

## Deliverables
`storytelling_final.mp4` + `voice_storytelling.wav` + `subtitle.srt` + `storytelling_script.txt` + optional mobile 720p.  
QA ghi: Genre ID + Format ID + `OmniVoice · male clone v2 locked · 1.2 · voice_locked:true`.

## CẤM
Copy nguyên Douyin / promo kênh đối thủ · đổi voice form · burn karaoke không được yêu cầu · F02 làm chuẩn · bịa số liệu.
