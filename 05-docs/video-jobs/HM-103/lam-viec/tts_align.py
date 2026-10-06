"""HM-103: OmniVoice TTS (voice-lock v2) + alignment, using pipeline modules. Run under flock."""
import sys, json, hashlib
from pathlib import Path
sys.path.insert(0, "/workspace/AI-auto-generate-video")
from pipeline.common import setup_logging, load_config, write_json, media_duration, log
from pipeline import text_vi
from pipeline.tts_omnivoice import synth_sentences, loudnorm, QA_STRING
from pipeline.align import align_words, asr_verify, build_srt
job = Path("/workspace/video-jobs/HM-103"); lv = job / "lam-viec"
setup_logging(job / "qa/pipeline.log")
cfg = load_config(job)
text = text_vi.normalize((job / "script.txt").read_text(encoding="utf-8"))
sents = text_vi.split_sentences(text)
log.info("HM-103 TTS: %d sentences, %d syllables", len(sents), text_vi.count_syllables(text))
assert len(sents) == 30, sents
raw, sent_t, info = synth_sentences(sents, lv, cfg)
voice = lv / "voice.wav"
ln = loudnorm(raw, voice, cfg)
vdur = media_duration(voice)
write_json(lv / "tts.json", {"sentences": sent_t, "info": info, "loudnorm_in": ln, "duration": vdur})
log.info("voice %.2fs", vdur)
md5 = hashlib.md5(voice.read_bytes()).hexdigest()
words = align_words(voice, sent_t, cfg)
write_json(lv / "words.json", {"voice_md5": md5, "words": words})
(lv / "subtitle.srt").write_text(build_srt(words), encoding="utf-8")
try:
    a = asr_verify(voice, text, cfg); a["voice_md5"] = md5; write_json(lv / "asr_verify.json", a)
    log.info("ASR similarity %s", a.get("similarity"))
except Exception as e:
    log.warning("asr verify failed %s", e)
print("DONE", vdur, len(words))
