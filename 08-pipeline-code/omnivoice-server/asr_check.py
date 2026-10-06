import sys, torch
from transformers import pipeline
asr = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3-turbo", device="cpu", torch_dtype=torch.float32)
for f in sys.argv[1:]:
    r = asr(f, generate_kwargs={"language": "vietnamese", "task": "transcribe"}, chunk_length_s=30, return_timestamps=True)
    print("==", f); print(r["text"])
