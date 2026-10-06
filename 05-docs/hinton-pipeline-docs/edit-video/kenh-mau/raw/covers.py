import json,subprocess,sys,os
from PIL import Image,ImageDraw
OUT='/workspace/hinton-pipeline-docs/edit-video/kenh-mau/covers'
for h in sys.argv[1:]:
    v=[json.loads(l) for l in open(f'tt_{h}.jsonl') if l.strip()]
    top=sorted(v,key=lambda x:-(x.get('view_count') or 0))[:6]
    new=sorted(v,key=lambda x:x.get('upload_date') or '',reverse=True)
    pick=top+[x for x in new if x not in top][:6]
    ims=[]
    os.makedirs(f'{OUT}/{h}',exist_ok=True)
    for i,x in enumerate(pick):
        th={t.get('id'):t['url'] for t in (x.get('thumbnails') or [])}
        url=th.get('originCover') or th.get('cover')
        if not url: continue
        p=f"{OUT}/{h}/{i:02d}_{x['id']}.jpg"
        subprocess.run(['curl','-sL','-m','20','-o',p,url])
        try: ims.append((Image.open(p).convert('RGB'),x))
        except Exception as e: print('bad',p,e)
    W,H=270,480
    sheet=Image.new('RGB',(W*6,(H+20)*2),'white'); d=ImageDraw.Draw(sheet)
    for i,(im,x) in enumerate(ims[:12]):
        sheet.paste(im.resize((W,H)),((i%6)*W,(i//6)*(H+20)))
        d.text(((i%6)*W+4,(i//6)*(H+20)+H+3),f"{i} {x.get('view_count'):,} {x.get('upload_date')}",fill='black')
    sheet.save(f'{OUT}/{h}_sheet.jpg',quality=85); print(h,len(ims))
