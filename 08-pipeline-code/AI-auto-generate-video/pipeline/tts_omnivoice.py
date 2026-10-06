"""OmniVoice local TTS (voice-lock v2). NEVER edge-tts / cloud TTS.

Per-sentence synthesis, cached by sha1(text|speed|ref) in lam-viec/tts_cache/, then
silence-trimmed and concatenated with a fixed small gap. Returns sentence timings.
"""
import hashlib, json, os, subprocess, time, urllib.request, urllib.error
from pathlib import Path
from .common import log, run, media_duration, LOCK_FILE

QA_STRING = "OmniVoice · male clone v2 locked · 1.2 · voice_locked:true"


def health(endpoint, timeout=5):
    try:
        with urllib.request.urlopen(endpoint.rstrip("/") + "/health", timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception as e:  # noqa
        return {"_error": str(e)}


def health_ok(h, cfg):
    t = cfg["tts"]
    return (h.get("status") == "ok" and h.get("voice_locked") is True
            and str(h.get("ref_audio", "")).endswith(t["expected_ref"])
            and abs(float(h.get("speed", 0)) - float(t["speed"])) < 1e-6)


def restart_server(cfg):
    t = cfg["tts"]
    if os.environ.get("HINTON_RENDER_LOCK_HELD") == "1":
        # we already hold /workspace/video-jobs/.render.lock (run.sh wraps us in flock);
        # restart.sh closes inherited fds so uvicorn never keeps the lock.
        cmd = [t["restart_script"]]
    else:
        cmd = ["flock", "-o", LOCK_FILE, t["restart_script"]]
    log.warning("OmniVoice not healthy/locked -> restarting: %s", " ".join(cmd))
    subprocess.run(cmd, check=False, close_fds=True)
    deadline = time.time() + t["restart_wait_s"]
    while time.time() < deadline:
        time.sleep(5)
        h = health(t["endpoint"])
        if health_ok(h, cfg):
            log.info("OmniVoice back up: %s", h)
            return h
    raise RuntimeError("OmniVoice did not come back healthy after restart")


def ensure_health(cfg):
    h = health(cfg["tts"]["endpoint"])
    if not health_ok(h, cfg):
        log.warning("health check failed: %s", h)
        h = restart_server(cfg)
    log.info("OmniVoice health OK: voice_locked=%s ref=%s speed=%s speed_mode=%s",
             h.get("voice_locked"), os.path.basename(h.get("ref_audio", "")), h.get("speed"), h.get("speed_mode"))
    return h


def _tts_request(text, cfg):
    t = cfg["tts"]
    body = json.dumps({"text": text, "speed": t["speed"], "language": t["language"]}).encode()
    req = urllib.request.Request(t["endpoint"].rstrip("/") + "/tts", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=t["timeout_s"]) as r:
        locked = r.headers.get("X-Voice-Locked")
        clone = r.headers.get("X-Voice-Clone")
        data = r.read()
    if locked != "true" or not (clone or "").endswith(t["expected_ref"]):
        raise RuntimeError(f"voice lock header mismatch: X-Voice-Locked={locked} X-Voice-Clone={clone}")
    return data, clone


def synth_sentences(sentences, work: Path, cfg):
    """Returns (voice_raw.wav path, [{'text','start','end','file'}], info)."""
    cache = work / "tts_cache"; cache.mkdir(parents=True, exist_ok=True)
    t = cfg["tts"]
    h = ensure_health(cfg)
    chunks, total_tts_s = [], 0.0
    for i, s in enumerate(sentences):
        key = hashlib.sha1(f"{s}|{t['speed']}|{t['expected_ref']}".encode()).hexdigest()[:16]
        raw = cache / f"{key}.raw.wav"
        trimmed = cache / f"{key}.trim.wav"
        if not raw.exists():
            for attempt in range(1, 4):  # first try + remake ≤2
                try:
                    t0 = time.time()
                    data, clone = _tts_request(s, cfg)
                    raw.write_bytes(data)
                    dt = time.time() - t0; total_tts_s += dt
                    log.info("TTS %d/%d ok in %.1fs voice_clone=%s : %s", i + 1, len(sentences), dt, clone, s[:70])
                    break
                except Exception as e:
                    log.error("TTS %d attempt %d failed: %s", i + 1, attempt, e)
                    if attempt == 3:
                        raise
                    restart_server(cfg)
        else:
            log.info("TTS %d/%d cached: %s", i + 1, len(sentences), s[:70])
        if not trimmed.exists():
            # trim leading/trailing silence (keep 40 ms), resample to 48 kHz mono
            af = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.04,"
                  "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,areverse")
            run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", af, "-ar", "48000", "-ac", "1",
                 "-c:a", "pcm_s16le", str(trimmed)])
        chunks.append(trimmed)

    # concat with fixed gap
    gap = float(t["gap_s"])
    gapf = cache / f"gap_{int(gap*1000)}ms.wav"
    run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", f"{gap}",
         "-c:a", "pcm_s16le", str(gapf)])
    lst = work / "tts_concat.txt"
    lines, timings, cur = [], [], 0.0
    for i, (s, c) in enumerate(zip(sentences, chunks)):
        d = media_duration(c)
        timings.append({"i": i, "text": s, "start": round(cur, 3), "end": round(cur + d, 3), "file": str(c)})
        lines.append(f"file '{c}'"); cur += d
        if i < len(chunks) - 1:
            lines.append(f"file '{gapf}'"); cur += gap
    lst.write_text("\n".join(lines) + "\n")
    out = work / "voice_raw.wav"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:a", "pcm_s16le", str(out)])
    info = {"health": h, "qa": QA_STRING, "tts_seconds_this_run": round(total_tts_s, 1)}
    return out, timings, info


def loudnorm(src: Path, dst: Path, cfg):
    """Two-pass EBU R128 loudnorm (~-14 LUFS VO-only)."""
    L = cfg["loudness"]
    r = run(["ffmpeg", "-v", "info", "-y", "-i", str(src), "-af",
             f"loudnorm=I={L['I']}:TP={L['TP']}:LRA={L['LRA']}:print_format=json", "-f", "null", "-"], capture=True)
    txt = r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1]
    m = json.loads(txt)
    af = (f"loudnorm=I={L['I']}:TP={L['TP']}:LRA={L['LRA']}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", af, "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(dst)])
    return m
