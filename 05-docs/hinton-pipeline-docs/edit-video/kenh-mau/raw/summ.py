import json,sys,statistics as st,datetime as dt
def load(f):
    out=[]
    for l in open(f):
        l=l.strip()
        if l: out.append(json.loads(l))
    return out
def fmt(s):
    return f"{int(s)//60}:{int(s)%60:02d}" if s is not None else "?"
for f in sys.argv[1:]:
    v=load(f)
    if not v: print(f,"EMPTY");continue
    durs=[x['duration'] for x in v if x.get('duration')]
    views=[x.get('view_count') or 0 for x in v]
    dates=sorted(x.get('upload_date') or '' for x in v)
    print(f"=== {f} | channel={v[0].get('channel')} uploader={v[0].get('uploader')} n={len(v)} dates {dates[0]}..{dates[-1]}")
    print(f"  dur median {fmt(st.median(durs)) if durs else '?'} mean {fmt(st.mean(durs)) if durs else '?'} | views median {int(st.median(views)):,} max {max(views):,} sum {sum(views):,}")
    b=[0]*5
    for d in durs: b[0 if d<30 else 1 if d<60 else 2 if d<90 else 3 if d<120 else 4]+=1
    print("  dur buckets <30/30-59/60-89/90-119/>=120:",b)
    for x in sorted(v,key=lambda x:-(x.get('view_count') or 0))[:5]:
        print(f"  TOP {x.get('view_count'):,} | {fmt(x.get('duration'))} | {x.get('upload_date')} | {(x.get('description') or x.get('title') or '')[:110]!r} | {x.get('url')}")
    for x in sorted(v,key=lambda x:x.get('upload_date') or '',reverse=True)[:6]:
        print(f"  NEW {x.get('upload_date')} | {x.get('view_count'):,} | {fmt(x.get('duration'))} | {(x.get('description') or '')[:110]!r}")
