---
name: Map animation video remake
description: >-
  Use when the user sends a sample TikTok map-animation (news/war/ranking) video
  and wants a new, non-identical Vietnamese remake: script, 7 scenes generated
  with Grok Imagine, editing, voiceover and final MP4.
---
# Map animation video remake (7 bước)

Input: one sample vertical map-animation video (TikTok style). Output: a new ~1-minute 9:16 Vietnamese video in pure map-animation style, similar but not a copy (to avoid reupload flags).

Work folder: `/workspace/<project>/` with `sample.mp4`, `shots/`, `clean/`, `gen/`, `audio/`, `edit/`, `final/`. Helper scripts live in this skill's `scripts/` folder if installed from the zip.

## Bước 1 — Analyze + script
1. Copy the sample under `/workspace/<project>/` (video must be under /workspace to be watched) and have a video-watching subagent return: full transcript with timestamps, on-screen text, topic/facts/places, shot-by-shot breakdown (map base, camera moves, highlights, icons, transitions, SFX, music), watermark positions, and a split into 7 parts with one clean screenshot timestamp each.
2. Rewrite the content in Vietnamese with these rules:
   - Giọng văn đanh thép, kịch tính; mở bài đi thẳng vào trọng tâm, căng thẳng.
   - Giữ nguyên cấu trúc bài và cấu trúc tin tức; chỉ đổi giọng văn.
   - Thay chữ “im” bằng “yên”. Ngày tháng viết ra chữ đọc: 1/1/2026 → “ngày 1 tháng 1 năm 2026”.
   - Né từ cấm TikTok (tử vong, giết, máu, bạo lực, rơi máy bay… → dùng từ nhẹ hơn).
   - ~240 chữ cho 1 phút (nhịp minimax 1.0); count with `wc -w`.
   - Tiêu đề bao quát toàn bộ nội dung và nêu nguyên nhân/lý do; hashtag chữ thường, không dấu.
   - One paragraph per scene (7 paragraphs) saved to `script.txt`.
   - Keep facts as in the sample; say they were not re-verified.

## Bước 2 — 7-scene breakdown
Describe each of 7 scenes: camera (zoom in/out, pan, tilt, orbit), highlight style (flag fill, glowing stroke, extrusion), icons/3D assets, mood, 9:16.

## Bước 3 — 7 screenshots
`ffmpeg -ss <t> -i sample.mp4 -frames:v 1 -q:v 2 shots/sceneN.jpg`, then remove subtitles and channel watermark with `delogo` (keep boxes inside the frame, not touching edges) into `clean/`. Check each with Read.

## Bước 4 — Grok prompts
English prompts (Grok follows English best). Common prefix: “Vertical 9:16 cinematic map animation, photorealistic satellite Earth imagery, deep teal oceans, natural terrain, smooth eased camera, subtle 3D tilt, soft drop shadows. No text, no subtitles, no watermark, no logos.” + scene-specific motion/icons. Pick clip length per scene from the paragraph length (6s or 10s).

## Bước 5 — Generate on Grok Imagine (box browser)
- Browser subagent opens https://grok.com/imagine. If “Sign in” shows, hand the box to the user to sign in ON THE BOX (they may sign in on their own computer by mistake — explain). Grok may also ask year-of-birth confirmation: user-only step.
- For each scene, a NEW generation: Video mode, 9:16, 720p, duration, upload `clean/sceneN.jpg`, paste prompt, submit, wait, download. Do scene 1 first as a test, then 2–7 in one dispatch.
- Downloads land in `/home/box/Downloads/grok-video-<id>.mp4`; map them to scenes by mtime order and copy to `gen/sceneN.mp4`. Make a contact sheet to check.

## Bước 7 (do in parallel with 5) — Voiceover, music, SFX
- Free voice: `edge-tts` with `vi-VN-NamMinhNeural`, pitch -5Hz; this voice is slow, so rate ~+20–25% to fit ~60s. Generate per paragraph + combined with 0.4s gaps; save WordBoundary timings to `vo_timings.json`. Process with ffmpeg: highpass 70Hz, bass +3.5dB@110Hz, presence +1.5dB@3kHz, 3:1 compression, light echo, loudnorm -16 LUFS.
- Music/SFX: Freesound CC0 only (verify license on each page); epic/suspense track, whooshes, pops, dings, impacts, a riser. Record sources in `LICENSES.txt`.
- Note: Edge TTS output has no clear commercial license — tell the user; offer MiniMax with an API key.
- Audio can't be attached alone in chat: wrap a preview in an MP4 with a still image.

## Bước 6 — Edit (professional editor)
- Timeline: scene N spans VO paragraph N; retime clips 0.85–1.15x, slow push-in/out zoom, no frozen frames. Upscale to 1080x1920 lanczos, unified light grade, vignette. Drop Grok audio.
- Transitions ~0.33s xfade (zoomin, smoothleft, fadewhite, slideup, circleopen), centered on paragraph boundaries, each with a whoosh.
- Vietnamese ASS subtitles via libass, font Be Vietnam Pro ExtraBold (OFL), synced from timings, 1–4 words, phrase-grouped so 2-syllable words aren't split, white with black outline, current word yellow, names/numbers gold, pop-in. SIZE: keep it modest — users found the first version too big; aim for roughly 55–65px at 1080 width (≈5% of width), position ~62% height, inside TikTok safe zone.
- Title cards (rank/topic) at top, number callouts with pop/ding SFX, a teaser + impact + music swell on the big reveal; riser under the suspense scene.
- Blur any leftover watermark ghosts. Mix: VO -16 LUFS, music sidechain-ducked ~20–25dB under VO, final -14 LUFS, TP ≤ -1 dB.
- QA: extract frames at every scene/transition and view them; check diacritics, overlap, sync, no black frames. Output `final/final_video.mp4` (H.264/AAC, 30fps, faststart).

## Deliver
Send the script (title, body, hashtags) after Bước 1, scene stills after Bước 4, scene 1 after the test, the contact sheet after Bước 5, the VO preview, then the final MP4 with any known flaws (e.g. garbled Grok-generated badges) and offer a regenerate.
