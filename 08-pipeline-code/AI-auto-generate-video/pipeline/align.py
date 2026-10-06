"""Forced alignment of the KNOWN script to the TTS audio (WhisperX align, CPU, VI wav2vec2).
No ASR needed. Optional faster-whisper pass only for QA (did the voice read the script?)."""
import difflib, gc, re
from .common import log
from .text_vi import words as split_words


def _clean(w):
    return re.sub(r"[^\w]", "", w.lower())


def align_words(voice_wav, sentences_t, cfg):
    import torch, whisperx
    torch.set_num_threads(4)
    device = cfg["align"]["device"]
    model, meta = whisperx.load_align_model(language_code="vi", device=device, model_name=cfg["align"]["model"])
    audio = whisperx.load_audio(str(voice_wav))
    segs = [{"start": s["start"], "end": s["end"], "text": s["text"]} for s in sentences_t]
    res = whisperx.align(segs, model, meta, audio, device, return_char_alignments=False)
    del model; gc.collect()

    # map whisperx words back onto our tokens, per sentence
    out = []
    wx = [w for seg in res.get("segments", []) for w in seg.get("words", [])]
    for si, s in enumerate(sentences_t):
        toks = split_words(s["text"])
        # sequential greedy matching within the sentence time window
        cand = [w for w in wx if w.get("start") is not None and (s["start"] - 0.05 <= w["start"] <= s["end"] + 0.05)]
        j = 0
        row = []
        for t in toks:
            ct, hit = _clean(t), None
            for k in range(j, min(j + 4, len(cand))):
                if _clean(cand[k].get("word", "")) == ct:
                    hit = cand[k]; j = k + 1; break
            row.append({"word": t, "start": hit.get("start") if hit else None,
                        "end": hit.get("end") if hit else None, "sent": si})
        _fill(row, s["start"], s["end"])
        out.extend(row)
    n_missing = sum(1 for w in out if w.get("interp"))
    log.info("aligned %d words (%d interpolated)", len(out), n_missing)
    # sanity check: wav2vec2-VI has no f/j/w/z, so sentences with Latin brand names (OpenAI, AlphaFold, GPT…) can
    # collapse into a tiny time span. Re-time such sentences from faster-whisper word timestamps.
    bad = []
    for si, s in enumerate(sentences_t):
        row = [w for w in out if w["sent"] == si]
        if not row: continue
        span = row[-1]["end"] - row[0]["start"]; dur = s["end"] - s["start"]
        if dur > 0.8 and (span < 0.7 * dur or len(row) / max(span, 0.05) > 8.5):
            bad.append(si)
    if bad:
        log.warning("whisperx alignment collapsed in sentences %s -> faster-whisper word timing fallback", bad)
        try:
            fw = fw_word_times(voice_wav, [w["word"] for w in out], cfg)
            for i, w in enumerate(out):
                if w["sent"] in bad and fw[i]:
                    w["start"], w["end"], w["fw"] = round(fw[i][0], 3), round(fw[i][1], 3), True
            for si in bad:
                row = [w for w in out if w["sent"] == si]
                for w in row:
                    if not w.get("fw"): w["start"] = None
                _fill(row, sentences_t[si]["start"], sentences_t[si]["end"])
        except Exception as e:
            log.warning("faster-whisper fallback failed: %s", e)
    return out


def fw_word_times(voice_wav, tokens, cfg):
    """faster-whisper small int8 word timestamps mapped onto known script tokens with difflib (None if unmatched)."""
    from faster_whisper import WhisperModel
    import whisperx
    a = cfg["asr_verify"]
    m = WhisperModel(a["model"], device="cpu", compute_type=a["compute_type"], cpu_threads=4)
    audio = whisperx.load_audio(str(voice_wav))
    segs, _ = m.transcribe(audio, language="vi", beam_size=5, vad_filter=False, word_timestamps=True)
    hw = [(p, w.start, w.end) for sg in segs for w in sg.words for p in w.word.split()]
    del m; gc.collect()
    A = [_clean(t) for t in tokens]; B = [_clean(h[0]) for h in hw]
    res = [None] * len(tokens)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1): res[i1 + k] = (hw[j1 + k][1], hw[j1 + k][2])
        elif tag == "replace" and j2 > j1:
            s0, e0, n = hw[j1][1], hw[j2 - 1][2], i2 - i1
            for k in range(n): res[i1 + k] = (s0 + (e0 - s0) * k / n, s0 + (e0 - s0) * (k + 1) / n)
    log.info("faster-whisper word timing: %d/%d tokens matched", sum(1 for r in res if r), len(tokens))
    return res


def _fill(row, s0, s1):
    n = len(row)
    known = [i for i, w in enumerate(row) if w["start"] is not None]
    if not known:
        step = (s1 - s0) / max(n, 1)
        for i, w in enumerate(row):
            w["start"], w["end"], w["interp"] = s0 + i * step, s0 + (i + 1) * step, True
        return
    for i, w in enumerate(row):
        if w["start"] is not None:
            continue
        prev = max([k for k in known if k < i], default=None)
        nxt = min([k for k in known if k > i], default=None)
        a = row[prev]["end"] if prev is not None else s0
        b = row[nxt]["start"] if nxt is not None else s1
        lo = prev if prev is not None else -1
        hi = nxt if nxt is not None else n
        span = hi - lo - 1
        pos = i - lo - 1
        step = max(b - a, 0.05) / max(span, 1)
        w["start"], w["end"], w["interp"] = a + pos * step, a + (pos + 1) * step, True
    for i, w in enumerate(row):  # monotonic + clamp
        w["start"] = round(max(s0, min(w["start"], s1)), 3)
        w["end"] = round(max(w["start"] + 0.04, min(w["end"], s1)), 3)
        if i and w["start"] < row[i - 1]["start"]:
            w["start"] = row[i - 1]["start"]


def asr_verify(voice_wav, script_text, cfg):
    from faster_whisper import WhisperModel
    a = cfg["asr_verify"]
    m = WhisperModel(a["model"], device="cpu", compute_type=a["compute_type"], cpu_threads=4)
    import whisperx
    audio = whisperx.load_audio(str(voice_wav))  # numpy 16 kHz (avoids PyAV API mismatch)
    segs, _ = m.transcribe(audio, language="vi", beam_size=1, vad_filter=False)
    hyp = " ".join(s.text.strip() for s in segs)
    del m; gc.collect()
    ref_t = [_clean(w) for w in script_text.split() if _clean(w)]
    hyp_t = [_clean(w) for w in hyp.split() if _clean(w)]
    ratio = difflib.SequenceMatcher(None, ref_t, hyp_t).ratio()
    log.info("ASR verify (faster-whisper %s): token similarity %.3f", a["model"], ratio)
    return {"similarity": round(ratio, 3), "hypothesis": hyp}


def build_srt(words, max_words=7, max_dur=2.8):
    """Sidecar SRT: cues of ≤7 words / ≤2.8s, never crossing a sentence."""
    cues, cur = [], []
    for w in words:
        if cur and (w["sent"] != cur[0]["sent"] or len(cur) >= max_words or w["end"] - cur[0]["start"] > max_dur):
            cues.append(cur); cur = []
        cur.append(w)
        if re.search(r"[,;:]$", w["word"]) and len(cur) >= 3:
            cues.append(cur); cur = []
    if cur:
        cues.append(cur)
    lines = []
    for i, c in enumerate(cues, 1):
        st = c[0]["start"]
        en = c[-1]["end"]
        if i < len(cues):
            en = min(max(en, st + 0.3), cues[i][0]["start"])
        txt = " ".join(x["word"] for x in c).rstrip(",;:")
        lines += [str(i), f"{_ts(st)} --> {_ts(en)}", txt, ""]
    return "\n".join(lines)


def _ts(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
