"""HyperFrames render, deliverables via /workspace/video-jobs/deliver.sh, ffprobe QA, contact sheet, report."""
import json, os, shutil, time
from pathlib import Path
from .common import log, run, ffprobe_json, media_duration, REPO

HF_BIN = REPO / "node_modules" / ".bin" / "hyperframes"
DELIVER = "/workspace/video-jobs/deliver.sh"


def hf_env():
    env = dict(os.environ)
    env["PATH"] = "/home/box/.local/bin:" + env.get("PATH", "")
    env["HYPERFRAMES_NO_TELEMETRY"] = "1"; env["DO_NOT_TRACK"] = "1"
    return env


def hf_render(hf_dir: Path, out_mp4: Path, cfg):
    env = hf_env()
    r = run([str(HF_BIN), "lint", str(hf_dir)], check=False, capture=True, env=env)
    log.info("hyperframes lint:\n%s", (r.stdout + r.stderr)[-2500:])
    if r.returncode != 0:
        raise RuntimeError("hyperframes lint failed (see log)")
    rc = cfg["render"]
    cmd = [str(HF_BIN), "render", str(hf_dir), "-o", str(out_mp4), "--fps", str(cfg["fps"]),
           "-q", rc["quality"], "-w", str(rc["workers"]), "--crf", str(rc["crf"])]
    t0 = time.time()
    r = run(cmd, check=False, capture=True, env=env, timeout=7200)
    tail = "\n".join(l for l in (r.stdout + r.stderr).splitlines() if "Render:trace" not in l and "Streaming frame" not in l)
    log.info("hyperframes render (%.0fs):\n%s", time.time() - t0, tail[-2500:])
    if r.returncode != 0 or not out_mp4.exists():
        raise RuntimeError("hyperframes render failed")
    return round(time.time() - t0, 1)


def contact_sheet(mp4: Path, dst: Path, n=4):
    d = media_duration(mp4)
    tmp = dst.parent / "_cs"; tmp.mkdir(exist_ok=True)
    pts = [d * f for f in (0.04, 0.3, 0.6, 0.95)][:n]
    files = []
    for i, t in enumerate(pts):
        f = tmp / f"f{i}.jpg"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(mp4), "-frames:v", "1",
             "-vf", f"scale=540:960,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
                    f"text='t={t:.1f}s':x=16:y=16:fontsize=34:fontcolor=white:box=1:boxcolor=black@0.6", str(f)])
        files.append(f)
    inputs = sum([["-i", str(f)] for f in files], [])
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex",
         "".join(f"[{i}:v]" for i in range(len(files))) + f"hstack=inputs={len(files)}", "-q:v", "3", str(dst)])
    shutil.rmtree(tmp, ignore_errors=True)
    return [round(p, 2) for p in pts]


def probe_summary(p: Path):
    j = ffprobe_json(p)
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), {})
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    return {"file": str(p), "size_mb": round(int(j["format"]["size"]) / 1e6, 2), "duration": round(float(j["format"]["duration"]), 3),
            "video": f'{v.get("codec_name")} {v.get("width")}x{v.get("height")} {v.get("r_frame_rate")} {v.get("pix_fmt")}',
            "audio": (f'{a.get("codec_name")} {a.get("sample_rate")}Hz ch={a.get("channels")}' if a else None)}


def loudness(p: Path):
    r = run(["ffmpeg", "-v", "info", "-i", str(p), "-af", "ebur128=peak=true", "-f", "null", "-"], capture=True, check=False)
    txt = r.stderr[r.stderr.rfind("Summary:"):]
    import re
    I = re.search(r"I:\s+(-?[\d\.]+) LUFS", txt); TP = re.search(r"Peak:\s+(-?[\d\.]+) dBFS", txt)
    return {"I_LUFS": float(I.group(1)) if I else None, "TP_dBFS": float(TP.group(1)) if TP else None}
