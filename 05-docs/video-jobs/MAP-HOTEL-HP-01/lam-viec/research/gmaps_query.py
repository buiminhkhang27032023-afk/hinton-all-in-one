#!/usr/bin/env python3
"""Query Google Maps public search JSON (tbm=map) for place rating/count/coords. Read-only."""
import json, re, sys, urllib.parse, subprocess, time
PB = open('/workspace/video-jobs/MAP-HOTEL-HP-01/lam-viec/research/pb.txt').read().strip()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
def q(query):
    url = "https://www.google.com/search?tbm=map&authuser=0&hl=vi&gl=vn&q=" + urllib.parse.quote_plus(query) + "&pb=" + PB
    raw = subprocess.check_output(["curl","-sL","-m","25","-A",UA,url]).decode('utf-8','ignore')
    raw = raw[raw.find('\n')+1:] if raw.startswith(")]}'") else raw
    return json.loads(raw)
def g(a,*idx):
    try:
        for i in idx: a=a[i]
        return a
    except Exception: return None
def places(d):
    out=[]
    def walk(x, depth=0):
        if depth>6 or not isinstance(x,list): return
        for el in x:
            if isinstance(el,list) and len(el)>14 and isinstance(g(el,14),list):
                p=el[14]; 
                if isinstance(g(p,11),str): out.append(p)
            walk(el, depth+1)
    walk(d)
    # also direct single result
    return out
if __name__=='__main__':
    res={}
    for query in sys.argv[1:]:
        d=q(query)
        ps=places(d)
        rows=[]
        for p in ps[:3]:
            rows.append({"name":g(p,11),"rating":g(p,4,7),"reviews":g(p,4,8) if isinstance(g(p,4,8),int) else (int(re.sub(r"\D","",g(p,4,3,1))) if isinstance(g(p,4,3,1),str) else None),"reviews_text":g(p,4,3,1),"lat":g(p,9,2),"lng":g(p,9,3),
                         "address":g(p,39) or g(p,18),"categories":g(p,13),"stars_class":g(p,64,0) if isinstance(g(p,64),list) else None,"place_id":g(p,78),"fid":g(p,10),"fetched_at":time.strftime("%Y-%m-%d %H:%M %z")})
        res[query]=rows
        print(json.dumps({query:rows},ensure_ascii=False,indent=1)); time.sleep(1.5)
