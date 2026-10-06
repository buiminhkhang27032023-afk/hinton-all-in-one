import sys,re,json,subprocess,datetime
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
for h in sys.argv[1:]:
    html=subprocess.run(["curl","-sL","-A",UA,f"https://www.tiktok.com/@{h}"],capture_output=True,text=True).stdout
    m=re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>',html,re.S)
    rec={"handle":h,"fetched_at":datetime.datetime.now().isoformat(timespec='minutes'),"source":f"https://www.tiktok.com/@{h} (HTML __UNIVERSAL_DATA_FOR_REHYDRATION__)"}
    try:
        d=json.loads(m.group(1))
        ui=d["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]
        u,s=ui["user"],ui.get("stats") or ui.get("statsV2")
        rec.update(nickname=u.get("nickname"),signature=u.get("signature"),verified=u.get("verified"),
                   followerCount=s.get("followerCount"),heartCount=s.get("heartCount") or s.get("heart"),videoCount=s.get("videoCount"),
                   bioLink=(u.get("bioLink") or {}).get("link"))
    except Exception as e:
        rec["error"]=repr(e)[:200]
    print(json.dumps(rec,ensure_ascii=False))
