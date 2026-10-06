"""Presenter asset prep (NO lip-sync). Video mode: crop pillarbox bars (cropdetect),
remove dead air with auto-editor, face-centred square PIP + 9:16 full version.
Photo mode (fallback): face-centred crops for PIP + intro/outro card."""
import collections, json, math, re, statistics
from pathlib import Path
from .common import log, run, media_duration, has_audio, video_size, REPO

VENV_BIN = REPO / ".venv" / "bin"


def cropdetect(src: Path):
    total = media_duration(src)
    votes = collections.Counter()
    for frac in (0.15, 0.5, 0.8):
        r = run(["ffmpeg", "-v", "info", "-ss", f"{total*frac:.2f}", "-i", str(src), "-t", "3",
                 "-vf", "cropdetect=24:2:0", "-f", "null", "-"], capture=True, check=False)
        votes.update(re.findall(r"crop=(\d+:\d+:\d+:\d+)", r.stderr))
    if not votes:
        return None
    crop = votes.most_common(1)[0][0]
    w, h, x, y = map(int, crop.split(":"))
    W, H = video_size(src)
    if w >= W - 8 and h >= H - 8:
        return None
    w -= w % 2; h -= h % 2
    return f"{w}:{h}:{x}:{y}"


def detect_face(img_or_frames):
    import cv2
    casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    boxes = []
    for img in img_or_frames:
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        f = casc.detectMultiScale(g, scaleFactor=1.1, minNeighbors=6, minSize=(max(40, g.shape[1] // 12),) * 2)
        if len(f):
            boxes.append(max(f, key=lambda b: b[2] * b[3]))
    if not boxes:
        return None
    return [int(statistics.median(b[i] for b in boxes)) for i in range(4)]  # x,y,w,h


def _square_around(face, W, H, k):
    x, y, w, h = face
    cx, cy = x + w / 2, y + h / 2 + 0.35 * h  # include some chin/shoulders
    side = int(min(W, H, max(w, h) * k)); side -= side % 2
    x0 = int(min(max(0, cx - side / 2), W - side)); y0 = int(min(max(0, cy - side / 2), H - side))
    return side, x0, y0


def prep_video(src: Path, work: Path, cfg, notes):
    import cv2
    d = work / "presenter"; d.mkdir(parents=True, exist_ok=True)
    pc = cfg["presenter"]
    crop = cropdetect(src)
    log.info("presenter cropdetect: %s", crop or "no bars")
    base = d / "p_cropped.mp4"
    vf = (f"crop={crop}," if crop else "") + "fps=30"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", vf, "-c:v", "libx264", "-crf", "16", "-preset", "fast",
         "-pix_fmt", "yuv420p"] + (["-c:a", "aac"] if has_audio(src) else ["-an"]) + [str(base)])
    src_len = media_duration(base)

    # auto-editor: remove silence (audio) or static dead air (motion) when there is no audio track
    cut = base
    if pc["silence_cut"]:
        ae_out = d / "p_cut.mp4"
        method = "audio:threshold=0.04" if has_audio(base) else "motion:threshold=0.02"
        r = run([str(VENV_BIN / "auto-editor"), str(base), "--edit", method, "--margin", "0.15s",
                 "--no-open", "--progress", "none", "-o", str(ae_out)], check=False, capture=True, timeout=900)
        if r.returncode == 0 and ae_out.exists():
            new_len = media_duration(ae_out)
            if new_len >= 0.6 * src_len:
                cut = ae_out
                notes.append(f"auto-editor ({method.split(':')[0]}) presenter {src_len:.1f}s -> {new_len:.1f}s")
            else:
                notes.append(f"auto-editor ({method}) would keep only {new_len:.1f}/{src_len:.1f}s -> ignored, using uncut clip")
        else:
            notes.append(f"auto-editor failed ({r.returncode}); using uncut presenter clip")
        log.info(notes[-1])

    # face box from sampled frames
    cap = cv2.VideoCapture(str(cut)); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); frames = []
    for i in range(12):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(n * (i + 0.5) / 12)); ok, fr = cap.read()
        if ok:
            frames.append(fr)
    cap.release()
    W, H = video_size(cut)
    face = detect_face(frames)
    if not face:
        notes.append("presenter: no face detected, PIP uses upper-centre crop")
        face = [W // 2 - W // 8, H // 6, W // 4, W // 4]
    log.info("presenter face box (in %dx%d): %s", W, H, face)
    side, x0, y0 = _square_around(face, W, H, 2.7)
    pip = d / "presenter_pip.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(cut), "-vf", f"crop={side}:{side}:{x0}:{y0},scale=600:600,fps=30",
         "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-g", "15", "-pix_fmt", "yuv420p", "-an", str(pip)])
    full = d / "presenter_full.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(cut), "-vf",
         "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
         "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-g", "15", "-pix_fmt", "yuv420p", "-an", str(full)])
    return {"mode": "video", "pip": str(pip), "full": str(full), "length": media_duration(pip),
            "source": str(src), "crop": crop, "face": face}


def prep_photo(src: Path, work: Path, cfg, notes):
    import cv2
    d = work / "presenter"; d.mkdir(parents=True, exist_ok=True)
    img = cv2.imread(str(src)); H, W = img.shape[:2]
    face = detect_face([img])
    if not face:
        notes.append("photo: no face detected, using upper-centre crop")
        face = [W // 2 - W // 8, H // 8, W // 4, W // 4]
    crops = []
    for name, k in (("face", 2.4), ("upper", 3.6)):
        side, x0, y0 = _square_around(face, W, H, k)
        p = d / f"photo_{name}.jpg"
        cv2.imwrite(str(p), cv2.resize(img[y0:y0 + side, x0:x0 + side], (600, 600), interpolation=cv2.INTER_AREA),
                    [cv2.IMWRITE_JPEG_QUALITY, 92])
        crops.append(str(p))
    card = d / "photo_card.jpg"
    cv2.imwrite(str(card), img, [cv2.IMWRITE_JPEG_QUALITY, 92])
    log.info("photo presenter face=%s crops=%s", face, crops)
    return {"mode": "photo", "pip_images": crops, "card": str(card), "source": str(src), "face": face}


def resolve(job: Path, cfg):
    pc = cfg["presenter"]
    def _p(v):
        if not v:
            return None
        p = Path(v)
        if not p.is_absolute():
            p = job / p
        return p if p.exists() else None
    vid, photo = _p(pc.get("video")), _p(pc.get("photo"))
    mode = pc.get("mode", "auto")
    if mode == "none":
        return None, None
    if mode == "video" or (mode == "auto" and vid):
        if vid:
            return "video", vid
    if photo:
        return "photo", photo
    return None, None


def plan_segments(windows, length, seg_min, seg_max, cut_points=()):
    """Cut presenter footage into short segments; each segment takes a different source offset
    (golden-ratio stride, avoiding the last 3 used ranges) so the loop is not obvious."""
    phi = 0.6180339887
    segs, recent, k = [], [], 0
    cuts = sorted(cut_points)
    for (a, b) in windows:
        t = a
        while t < b - 0.05:
            # prefer to change segment at a shot cut inside [t+seg_min, t+seg_max]
            cand = [c for c in cuts if t + seg_min <= c <= t + seg_max and c < b]
            e = cand[-1] if cand else min(b, t + (seg_min + seg_max) / 2)
            if b - e < seg_min * 0.6:
                e = b
            dur = e - t
            span = max(0.01, length - dur - 0.05)
            off = None
            for tries in range(12):
                k += 1
                o = (k * phi % 1.0) * span
                if all(abs(o - r) > max(dur, 1.0) for r in recent[-3:]):
                    off = o; break
            if off is None:
                off = (k * phi % 1.0) * span
            recent.append(off)
            segs.append({"start": round(t, 3), "dur": round(dur, 3), "media_start": round(off, 3), "idx": len(segs)})
            t = e
    return segs
