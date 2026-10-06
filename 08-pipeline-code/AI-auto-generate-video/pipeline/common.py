"""Shared helpers: config, logging, subprocess, ffprobe."""
import json, os, subprocess, sys, time, logging, shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LOCK_FILE = "/workspace/video-jobs/.render.lock"
log = logging.getLogger("hinton")


def setup_logging(log_path: Path):
    log_path.parent.mkdir(parents=True, exist_ok=True)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
    log.setLevel(logging.INFO)
    log.handlers.clear()
    fh = logging.FileHandler(log_path, encoding="utf-8"); fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout); sh.setFormatter(fmt)
    log.addHandler(fh); log.addHandler(sh)


def deep_merge(base, over):
    out = dict(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(job: Path) -> dict:
    base = json.loads(strip_json_comments((REPO / "config.default.json").read_text(encoding="utf-8")))
    user = {}
    p = job / "config.json"
    if p.exists():
        user = json.loads(strip_json_comments(p.read_text(encoding="utf-8")))
    cfg = deep_merge(base, user)
    cfg["job_id"] = cfg.get("job_id") or job.name
    return cfg


def strip_json_comments(s: str) -> str:
    # allow "//" full-line comments in config files
    return "\n".join(l for l in s.splitlines() if not l.lstrip().startswith("//"))


def run(cmd, check=True, capture=False, timeout=None, env=None, cwd=None):
    if isinstance(cmd, (list, tuple)):
        shown = " ".join(str(c) for c in cmd)
    else:
        shown = cmd
    log.info("$ %s", shown if len(shown) < 600 else shown[:600] + " …")
    r = subprocess.run(cmd, shell=isinstance(cmd, str), check=False, text=True,
                       capture_output=capture, timeout=timeout, env=env, cwd=cwd)
    if check and r.returncode != 0:
        if capture:
            log.error("stdout: %s\nstderr: %s", (r.stdout or "")[-3000:], (r.stderr or "")[-3000:])
        raise RuntimeError(f"command failed ({r.returncode}): {shown[:300]}")
    return r


def ffprobe_json(path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def media_duration(path) -> float:
    return float(ffprobe_json(path)["format"]["duration"])


def has_audio(path) -> bool:
    return any(s.get("codec_type") == "audio" for s in ffprobe_json(path)["streams"])


def video_size(path):
    for s in ffprobe_json(path)["streams"]:
        if s.get("codec_type") == "video":
            return int(s["width"]), int(s["height"])
    return None


def find_input(job: Path, name: str):
    """Inputs may live at the job root or in job/source/."""
    for p in (job / name, job / "source" / name):
        if p.exists():
            return p
    return None


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class Timer:
    def __init__(self):
        self.t0 = time.time(); self.marks = {}

    def mark(self, name, since):
        self.marks[name] = round(time.time() - since, 1)
        return self.marks[name]
