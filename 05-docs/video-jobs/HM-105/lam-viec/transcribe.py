import json
from faster_whisper import WhisperModel
import wave,numpy as np
w=wave.open("/workspace/video-jobs/HM-105/source/audio16k.wav");A=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768.0
m=WhisperModel("small",device="cpu",compute_type="int8",cpu_threads=6)
segs,info=m.transcribe(A,language="zh",vad_filter=True,beam_size=5,initial_prompt="以下是普通话的句子，关于AI、GPT Images 2.5、ChatGPT、画图。")
out=[{"start":round(s.start,2),"end":round(s.end,2),"text":s.text.strip(),"avg_logprob":round(s.avg_logprob,3)} for s in segs]
json.dump({"model":"faster-whisper small int8","lang":"zh","duration":info.duration,"segments":out},open("/workspace/video-jobs/HM-105/source/transcript_zh.json","w"),ensure_ascii=False,indent=1)
print("done",len(out))
