import json,datetime as dt
from notes import N
S={k.lower():v for k,v in json.load(open('search.json')).items()}
H=[h for h in json.load(open('html.json')) if h['cat']!='5']
CAT={'1':'Tự động tạo short end-to-end','2':'Dựng/render bằng code','3':'Phụ đề/ASR','4':'AI cắt clip/highlight','5':'Talking head/lip-sync','6':'Model sinh video mở','7':'B-roll/footage tự động'}
rows=[]
for h in H:
    r=h['repo'];s=S.get(r.lower(),{})
    desc,cpu,fit,note,licov=N[r]
    lic=licov or (h.get('html_lic') if h.get('html_lic') not in (None,'NOASSERTION') else s.get('lic')) or '—'
    if lic in ('NOASSERTION',None): lic='—'
    lang=s.get('lang') or ('TypeScript' if r=='redotvideo/revideo' else '—')
    d=dt.datetime.fromisoformat(h['last_commit'].replace('Z','+00:00')).astimezone(dt.timezone(dt.timedelta(hours=7))).date().isoformat()
    rows.append(dict(cat=h['cat'],repo=r,stars=h['html_stars'],date=d,lic=lic,lang=lang,desc=desc,cpu=cpu,fit=fit,note=note,arch=h.get('archived')))
rows.sort(key=lambda x:-x['stars'])
json.dump(rows,open('rows.json','w'),ensure_ascii=False,indent=1)
def line(i,x,catcol=True):
    a=' (archived)' if x['arch'] else ''
    c=f"{x['cat']}·{CAT[x['cat']]} | " if catcol else ''
    return f"| {i} | [{x['repo']}](https://github.com/{x['repo']}){a} | {c}{x['stars']:,} | {x['date']} | {x['lic']} | {x['lang']} | {x['desc']} | {x['cpu']} | {x['fit']} {x['note']} |"
hdr="| # | Repo | Nhóm | ⭐ Stars | Commit cuối (ICT) | License | Ngôn ngữ | Làm gì | CPU/GPU | Hợp pipeline (★1–5) |\n|---|---|---|---:|---|---|---|---|---|---|"
top=[line(i+1,x) for i,x in enumerate(rows[:20])]
open('top20.md','w').write(hdr+'\n'+'\n'.join(top)+'\n')
out=[]
hdr2="| # | Repo | ⭐ Stars | Commit cuối (ICT) | License | Ngôn ngữ | Làm gì | CPU/GPU | Hợp pipeline (★1–5) |\n|---|---|---:|---|---|---|---|---|---|"
for c in '123467':
    rs=[x for x in rows if x['cat']==c]
    out.append(f"\n### Nhóm {c} — {CAT[c]} ({len(rs)} repo)\n\n"+hdr2+'\n'+'\n'.join(line(i+1,x,False) for i,x in enumerate(rs)))
open('bycat.md','w').write('\n'.join(out)+'\n')
print(open('top20.md').read())
