# MAP-FOOD-HP-01 — Hải Phòng 7-stop food-tour template

## Data-driven
Edit `route-config.json` (N stops). Rebuild:
```bash
python3 build_tour.py --out full.html
```
Map mosaic auto-extends via tile cache when stop/landmark coords change (re-run tile fetch in prep notes).

## Voice
VO script is written by **Bot3** and approved by coordinator — use `lam-viec/storytelling_script.txt` **as-is** (do not rewrite).
OmniVoice male clone v2 @1.2, flock, loudnorm ~-14 → `lam-viec/voice/`.

## Audio mix
```bash
lam-viec/audio/mix_duck.sh voice.wav bgm/sunny-city-loop-100s.wav output/voice_plus_bgm.wav -20 2.8
```

## Render
```bash
flock /workspace/video-jobs/.render.lock bash -c '
  cd lam-viec/template
  npx hyperframes render -c full.html -o ../../output/storytelling_final.mp4 \
    --fps 30 --quality delivery --format mp4 --resolution portrait
'
```
