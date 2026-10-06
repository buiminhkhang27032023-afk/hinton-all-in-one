# MAP-FOOD-HCM-01 — HyperFrames map template

## Layout
- `index.html` — active composition (swapped between test-scene and full)
- `test-scene-5.html` — 5s fly-in to #5 Bánh Xèo 46A
- `full.html` — full ~60s map video (built from scene table + voice timings)
- `assets/` — map mosaic, pins, food icons, badges, fonts, SFX, places-index.json
- `places-index.json` — data-driven place ids + Web Mercator pixel coords
- `ASSETS-LICENSE.md` — tile/SFX/icon licenses

## Place ids (from places.json / chon-top5)
| id | rank | notes |
|---|---|---|
| banh-xeo-46a | #5 | Bib; rating 3.8 / 1977 |
| com-tam-ba-ghien | #4 | Bib; **coord approx — do not zoom tight** |
| banh-mi-huynh-hoa | #3 | |
| oc-dao | #2 | no Michelin label |
| pho-hoa-pasteur | #1 | gold pin |
| cho-ben-thanh, nha-tho-duc-ba, ks-rex, ks-caravelle | landmarks/hotels | |

## Render a scene (after Bot3 scene table + voice ready)

```bash
# 1) Ensure voice WAV + SRT exist
#    lam-viec/voice/voice_storytelling.wav
#    lam-viec/voice/subtitle.srt
#    lam-viec/voice/timings.json

# 2) Build full composition from timings
python3 lam-viec/template/build_full.py

# 3) Render under flock (1080x1920)
flock /workspace/video-jobs/.render.lock bash -c '
  cd /workspace/video-jobs/MAP-FOOD-HCM-01/lam-viec/template
  PATH=/home/box/.local/bin:$PATH
  npx hyperframes render -c full.html -o ../../output/storytelling_final.mp4 \
    --fps 30 --quality delivery --format mp4
'

# 4) Mobile 720p
ffmpeg -y -i output/storytelling_final.mp4 -vf scale=720:1280 \
  -c:v libx264 -pix_fmt yuv420p -c:a aac \
  output/storytelling_mobile_720p.mp4
```

## Plug in voice WAV + SRT
- In `full.html`, `<audio id="vo" src="assets/voice.wav" …>` (copied from `lam-viec/voice/voice_storytelling.wav` by `build_full.py`).
- SRT is sidecar only (`output/subtitle.srt`) — **do not burn karaoke** unless phiếu asks.
- Scene `data-start` / GSAP positions are driven by `timings.json` sentence starts.

## Test preview only
```bash
cd lam-viec/template
npx hyperframes render -c test-scene-5.html -o ../preview/test-scene-5-banh-xeo-46a_720p.mp4 \
  --fps 30 --resolution portrait --format mp4
# then scale to 720x1280 if needed
```

## Map math
Web Mercator on CARTO `dark_all` z15 mosaic (`assets/map/saigon-dark-z15.png`).
`px = (lng_to_tile_x - tx0) * 256`, same for y. Camera: `x = 540 - px*scale`, `y = 960 - py*scale`.
