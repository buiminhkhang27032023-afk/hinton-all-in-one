import asyncio, json, sys, edge_tts
VOICE="vi-VN-NamMinhNeural"; RATE=sys.argv[1] if len(sys.argv)>1 else "-8%"; PITCH="-5Hz"
paras=[p.strip() for p in open('/workspace/proj1/script.txt',encoding='utf-8') if p.strip()]
async def run(i,text):
    out={"paragraph":i,"text":text,"words":[],"sentences":[]}
    c=edge_tts.Communicate(text,VOICE,rate=RATE,pitch=PITCH,boundary="WordBoundary")
    with open(f'/workspace/proj1/audio/vo_{i}.mp3','wb') as f:
        async for ch in c.stream():
            if ch["type"]=="audio": f.write(ch["data"])
            elif ch["type"]=="WordBoundary":
                out["words"].append({"text":ch["text"],"start":ch["offset"]/1e7,"end":(ch["offset"]+ch["duration"])/1e7})
    c=edge_tts.Communicate(text,VOICE,rate=RATE,pitch=PITCH,boundary="SentenceBoundary")
    async for ch in c.stream():
        if ch["type"]=="SentenceBoundary":
            out["sentences"].append({"text":ch["text"],"start":ch["offset"]/1e7,"end":(ch["offset"]+ch["duration"])/1e7})
    return out
async def main():
    res=[await run(i+1,t) for i,t in enumerate(paras)]
    json.dump({"voice":VOICE,"rate":RATE,"pitch":PITCH,"paragraphs":res},open('/workspace/proj1/audio/vo_raw_timings.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
asyncio.run(main())
