#!/usr/bin/env python3
"""Cut short, non-overlapping clips from YouTube 8NmmFdREk5s and bake them into vertical plates/panels."""
import subprocess, json
from pathlib import Path
SRC = "/workspace/video-jobs/HM-103/source/yt/wow_blind.mp4"
OUT = Path("/workspace/video-jobs/HM-103/source/yt_clips")
GAME = "crop=316:254:12:58"        # game client window inside the 640x360 recording
CODEX = "crop=628:268:12:46"      # whole desktop: WoW client + Codex panel (prompt)
# id: (start_s, dur_s, layout, region, label)
CLIPS = {
 "y01_orc_new":      (219.6, 3.4, "full", GAME,  "Orc level 1 mới xuất hiện ở điểm khởi đầu"),
 "y02_questgiver":   (388.4, 3.4, "full", GAME,  "NPC giao nhiệm vụ (dấu ?) — Valley of Trials"),
 "y03_path_cacti":   (487.0, 3.4, "tb",   GAME,  "Chạy đường giữa các điểm nhiệm vụ (pathfinding)"),
 "y04_vendor":       (1213.6, 3.4, "full", GAME, "Khu NPC/thùng hàng ở trại — đoạn bán đồ (không thấy cửa sổ vendor)"),
 "y05_gear":         (1739.6, 3.4, "full", GAME, "Cận cảnh orc đã khoác giáp mới (áo giáp đỏ)"),
 "y06_trainer":      (1880.0, 3.4, "full", GAME, "Đứng ở trainer (thảm, trại Den) trước khi vào hang"),
 "y07_cave":         (2017.0, 3.4, "lr", GAME, "Trong hang — đánh quái nhiệm vụ hang"),
 "y08_senjin":       (2343.0, 3.4, "lr",   GAME, "Sen'jin Village (nhà troll, cây cọ) — cuối run"),
 "y09_valley_den":   (640.0, 3.4, "lr",    GAME, "Trại Den ở Valley of Trials"),
 "y10_wallclip":     (1963.2, 3.4, "tb",   GAME, "Camera/nhân vật xuyên địa hình ở vách đá (lỗi va chạm bản đồ)"),
 "y11_codex_prompt": (29.0, 3.4, "tbfit",  CODEX, "Desktop: WoW + Codex vừa nhận câu lệnh 'Create an orc character…'"),
 "y12_orc_close":    (1069.0, 3.4, "lr",   GAME, "Cận cảnh orc (dùng cho cảnh 'không nhận khung hình')"),
 "y13_landscape":    (1409.0, 3.4, "tb",   GAME, "Toàn cảnh Durotar — 'bản đồ thế giới'"),
}
def bake(cid, start, dur, layout, region):
    out = OUT / f"{cid}.mp4"
    if layout == "full":
        W, H, fgH, top = 1080, 1920, 868, 246
        fc = (f"[0:v]{region},split[a][b];[a]scale={W}:{fgH}:flags=lanczos,unsharp=5:5:0.7[fg];"
              f"[b]scale=-2:{H},crop={W}:{H},boxblur=28:2,eq=brightness=-0.28:saturation=1.1[bg];[bg][fg]overlay=0:{top},format=yuv420p")
    elif layout == "tb":
        W, H = 1080, 960
        fc = f"[0:v]{region},scale=-2:{H}:flags=lanczos,crop={W}:{H},unsharp=5:5:0.6,format=yuv420p"
    elif layout == "lr":
        W, H = 540, 900
        fc = f"[0:v]{region},scale=-2:{H}:flags=lanczos,crop={W}:{H},unsharp=5:5:0.6,format=yuv420p"
    elif layout == "tbfit":
        W, H = 1080, 960
        fc = (f"[0:v]{region},split[a][b];[a]scale={W}:-2:flags=lanczos,unsharp=5:5:0.9[fg];"
              f"[b]scale=-2:{H},crop={W}:{H},boxblur=20:2,eq=brightness=-0.2[bg];[bg][fg]overlay=0:(H-h)/2,format=yuv420p")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", str(dur), "-i", SRC, "-filter_complex", fc,
                    "-an", "-r", "30", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-g", "10", "-movflags", "+faststart", str(out)], check=True)
    return str(out)
meta = {}
for cid, (s, d, lay, reg, lab) in CLIPS.items():
    meta[cid] = dict(src_start=s, src_end=round(s + d, 2), layout=lay, label=lab, file=bake(cid, s, d, lay, reg))
    print("baked", cid)
# overlap check
iv = sorted((m["src_start"], m["src_end"], k) for k, m in meta.items())
for a, b in zip(iv, iv[1:]):
    assert a[1] <= b[0], ("overlap", a, b)
(OUT / "clips.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
print("ok", len(meta))
