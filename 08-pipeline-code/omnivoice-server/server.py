"""Minimal local OmniVoice TTS server (k2-fsa/OmniVoice) with male voice-clone lock (v2).

GET  /health -> status json (voice_locked, ref_audio, speed, ...)
POST /tts    -> audio/wav. JSON body: {"text": str, "speed": float?, "language": str?, "instruct": str? (ignored when locked)}
"""
import io, os, time, logging, threading, subprocess, tempfile
import numpy as np, soundfile as sf, torch
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from omnivoice import OmniVoice
from omnivoice.models.omnivoice import OmniVoiceGenerationConfig

HERE = os.path.dirname(os.path.abspath(__file__))
REF_AUDIO = os.environ.get("OMNIVOICE_REF_AUDIO", os.path.join(HERE, "voice-lock-vn-v2.wav"))
REF_TEXT_FILE = os.environ.get("OMNIVOICE_REF_TEXT", os.path.join(HERE, "voice-lock-vn-v2.ref.txt"))
SPEED = float(os.environ.get("OMNIVOICE_SPEED", "1.2"))
SEED = int(os.environ.get("OMNIVOICE_SEED", "1234"))
NUM_STEP = int(os.environ.get("OMNIVOICE_NUM_STEP", "32"))
# speed_mode "post": synthesize at model speed 1.0 then pitch-preserving ffmpeg atempo=SPEED
# (model-native speed>1 dropped words in Vietnamese/English-mixed text during QA). "model": pass speed to OmniVoice.
SPEED_MODE = os.environ.get("OMNIVOICE_SPEED_MODE", "post")
LANG = os.environ.get("OMNIVOICE_LANG", "vi")
MODEL_ID = os.environ.get("OMNIVOICE_MODEL", "k2-fsa/OmniVoice")
torch.set_num_threads(int(os.environ.get("OMNIVOICE_THREADS", str(os.cpu_count() or 4))))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("omnivoice-server")

log.info("loading %s on cpu (float32)...", MODEL_ID)
model = OmniVoice.from_pretrained(MODEL_ID, device_map="cpu", dtype=torch.float32)
ref_text = open(REF_TEXT_FILE, encoding="utf-8").read().strip()
voice_prompt = model.create_voice_clone_prompt(ref_audio=REF_AUDIO, ref_text=ref_text)
log.info("voice lock ready: ref_audio=%s ref_text=%r", REF_AUDIO, ref_text)
SR = getattr(model, "sampling_rate", 24000)
lock = threading.Lock()
app = FastAPI()

class TTSReq(BaseModel):
    text: str
    speed: float | None = None
    language: str | None = None
    instruct: str | None = None

@app.get("/health")
def health():
    return {"status": "ok", "engine": "OmniVoice", "model": MODEL_ID, "device": "cpu",
            "voice_mode": "clone", "voice_locked": True, "ref_audio": REF_AUDIO,
            "ref_text": REF_TEXT_FILE, "speed": SPEED, "speed_mode": SPEED_MODE, "seed": SEED, "num_step": NUM_STEP,
            "language": LANG, "sample_rate": SR}

@app.post("/tts")
def tts(req: TTSReq):
    text = req.text.strip()
    if not text:
        raise HTTPException(400, "empty text")
    speed = req.speed or SPEED
    t0 = time.time()
    with lock:
        torch.manual_seed(SEED); np.random.seed(SEED)
        audio = model.generate(text=text, language=req.language or LANG, voice_clone_prompt=voice_prompt,
                               speed=(1.0 if SPEED_MODE == "post" else speed),
                               generation_config=OmniVoiceGenerationConfig(num_step=NUM_STEP))
    wav = np.asarray(audio[0]).reshape(-1)
    buf = io.BytesIO(); sf.write(buf, wav, SR, format="WAV", subtype="PCM_16")
    if SPEED_MODE == "post" and abs(speed - 1.0) > 1e-3:
        r = subprocess.run(["ffmpeg", "-v", "error", "-f", "wav", "-i", "pipe:0", "-af", f"atempo={speed}",
                            "-c:a", "pcm_s16le", "-f", "wav", "pipe:1"], input=buf.getvalue(), capture_output=True, check=True)
        buf = io.BytesIO(r.stdout)
        wav = np.zeros(int(len(wav) / speed))
    log.info("tts chars=%d dur=%.2fs took=%.1fs speed=%.2f(%s) voice_clone=%s instruct_ignored=%s",
             len(text), len(wav) / SR, time.time() - t0, speed, SPEED_MODE, os.path.basename(REF_AUDIO), bool(req.instruct))
    return Response(buf.getvalue(), media_type="audio/wav",
                    headers={"X-Voice-Locked": "true", "X-Voice-Clone": os.path.basename(REF_AUDIO)})
