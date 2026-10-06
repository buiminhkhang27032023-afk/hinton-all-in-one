import json, re
from PIL import ImageFont
FD="/usr/share/fonts/truetype/sand-box/google/Be Vietnam Pro/"
BLACK=FD+"BeVietnamPro-Black.ttf"; XB=FD+"BeVietnamPro-ExtraBold.ttf"
def width(txt,size,font=BLACK):
    return ImageFont.truetype(font,size).getlength(txt)
def fit(txt,maxw,maxs,font=BLACK):
    s=maxs
    while width(txt,s,font)>maxw: s-=2
    return int(s*1.526)
def ts(t):
    t=max(0,t); h=int(t//3600); m=int(t%3600//60); s=t%60
    return f"{h}:{m:02d}:{s:05.2f}"
d=json.load(open('/workspace/proj1/audio/vo_timings.json'))
plan=json.load(open('/workspace/proj1/edit/plan.json'))
B=[b/30 for b in plan['B']]
YEL="&H0000E8FF&"; GOLD="&H0000C0FF&"; KEYC="&H0000B4FF&"
ev=[]; sfx=[]
def E(layer,st,en,style,text): ev.append(f"Dialogue: {layer},{ts(st)},{ts(en)},{style},,0,0,0,,{text}")
# ---------- subtitles ----------
KEY=set("emirates qatar airways qantas cathay pacific etihad iosa abu dhabi úc hồng kông năm tư ba hai trăm phần bảy sao cộng".split())
COMP=set(x.strip() for x in 'hàng không,tiểu vương,vương quốc,ả rập,thống nhất,bảo dưỡng,khắt khe,hệ thống,giám sát,phi hành,hành đoàn,huấn luyện,chiến binh,xa hoa,đáng gờm,kỷ luật,vượt qua,hàng loạt,kiểm định,quốc tế,tuân thủ,một trăm,phần trăm,thế kỷ,chinh phục,chặng bay,khắc nghiệt,hành tinh,kỷ lục,nể phục,toàn bộ,kỷ nguyên,máy bay,phản lực,sinh mạng,trả giá,hồng kông,dữ liệu,nhiễu động,truyền thẳng,phi công,thời gian,gian thực,truyền thống,đầu tiên,xếp hạng,an toàn,bảy sao,sao cộng,kiểm tra,độc lập,khoảnh khắc,quyết định,tất cả,gang tấc,lịch sử,tai nạn,tỷ lệ,sự cố,danh sách,abu dhabi,chính thức,ngôi vương,thế giới,đỉnh cao,sai lầm,cathay pacific,qatar airways,etihad airways,một vụ,một sinh,cái tên,một cuộc,một cái,đứng trên,vụ tai'.split(','))
NOBREAK=set("qatar cathay etihad abu hồng ả tiểu các một bảy".split())
for p in d['paragraphs']:
    toks=p['text'].split(); words=p['words']
    assert len(toks)==len(words),(p['paragraph'],len(toks),len(words))
    G=open('/workspace/proj1/edit/groups.txt').read().splitlines()[p['paragraph']-1].split(' / ')
    groups=[];k=0
    for gtxt in G:
        n=len(gtxt.split()); g=list(zip(toks[k:k+n],words[k:k+n]))
        assert [t for t,_ in g]==gtxt.split(),(gtxt,g); groups.append(g); k+=n
    assert k==len(toks)
    for gi,g in enumerate(groups):
        gst=g[0][1]['global_start']
        nxt=groups[gi+1][0][1]['global_start'] if gi+1<len(groups) else None
        gen=g[-1][1]['global_end']+0.35
        if nxt is not None: gen=min(gen,nxt)
        else: gen=min(gen, p['global_end']+0.3, 63.3)
        disp=[re.sub(r'[.,:?!]','',t).upper() for t,_ in g]
        line=" ".join(disp); brk=None
        if (width(line,45,XB)>900 or len(disp)>4) and len(disp)>=3:
            best=None
            for c in range(1,len(disp)):
                if (disp[c-1]+" "+disp[c]).lower() in COMP: continue
                w=max(width(" ".join(disp[:c]),80,XB),width(" ".join(disp[c:]),80,XB))
                if best is None or w<best[0]: best=(w,c)
            brk=best[1]; size=min(fit(" ".join(disp[:brk]),900,45,XB),fit(" ".join(disp[brk:]),900,45,XB))
        else: size=fit(line,900,45,XB)
        for wi,(tok,w) in enumerate(g):
            st=w['global_start']; en=g[wi+1][1]['global_start'] if wi+1<len(g) else gen
            parts=[]
            for k,(t2,_) in enumerate(g):
                bare=re.sub(r'[^\w]','',t2).lower()
                if k==wi: parts.append("{\\1c"+YEL+"}"+disp[k]+"{\\1c&H00FFFFFF&}")
                elif bare in KEY: parts.append("{\\1c"+KEYC+"}"+disp[k]+"{\\1c&H00FFFFFF&}")
                else: parts.append(disp[k])
            pre=f"{{\\fs{size}\\pos(540,1195)"
            if wi==0: pre+="\\fscx70\\fscy70\\t(0,80,\\fscx110\\fscy110)\\t(80,150,\\fscx100\\fscy100)"
            pre+="}"
            body=" ".join(parts) if brk is None else " ".join(parts[:brk])+"\\N"+" ".join(parts[brk:])
            E(2,st,en,"Sub",pre+body)
# ---------- title cards ----------
def plate(st,en,y0,h,w=980):
    x0=(1080-w)//2; r=36
    path=f"m {r} 0 l {w-r} 0 b {w} 0 {w} 0 {w} {r} l {w} {h-r} b {w} {h} {w} {h} {w-r} {h} l {r} {h} b 0 {h} 0 {h} 0 {h-r} l 0 {r} b 0 0 0 0 {r} 0"
    E(5,st,en,"Plate",f"{{\\an7\\pos({x0},{y0})\\p1\\fad(120,150)\\t(0,120,\\fscx100)}}{path}")
def glowtext(st,en,x,y,txt,size,color=GOLD,pop=True,layer=6,fadeout=150):
    anim="\\fscx0\\fscy0\\t(0,130,\\fscx118\\fscy118)\\t(130,230,\\fscx100\\fscy100)" if pop else ""
    E(layer,st,en,"Title",f"{{\\pos({x},{y})\\fs{size}\\1a&HFF&\\3c{color}\\bord14\\blur10\\3a&H50&\\shad0{anim}\\fad(60,{fadeout})}}{txt}")
    E(layer+1,st,en,"Title",f"{{\\pos({x},{y})\\fs{size}\\1c{color}\\3c&H101010&\\bord5\\shad4{anim}\\fad(60,{fadeout})}}{txt}")
def label(st,en,y,txt):
    E(8,st,en,"Label",f"{{\\pos(540,{y})\\fad(80,150)\\fscx0\\t(0,120,\\fscx100)}}{txt}")
# hook (scene 1)
st,en=0.15,B[1]-0.17
plate(st,en,215,300)
s=fit("AN TOÀN NHẤT THẾ GIỚI",900,96)
glowtext(st,en,540,305,"TOP 5 HÃNG BAY",s+10,"&H00FFFFFF&")
glowtext(st+0.25,en,540,420,"AN TOÀN NHẤT THẾ GIỚI",s,GOLD)
sfx+= [("pop_a",st),("pop_b",st+0.25)]
ranks=[(1,"#5 EMIRATES"),(2,"#4 QATAR AIRWAYS"),(3,"#3 QANTAS"),(4,"#2 CATHAY PACIFIC")]
for si,txt in ranks:
    st=B[si]+0.2; en=B[si+1]-0.17
    plate(st,en,215,250)
    label(st,en,275,"TOP 5")
    sz=fit(txt,900,118)
    glowtext(st+0.12,en,540,385,txt,sz)
    sfx+=[("pop_a",st),("pop_b",st+0.12)]
# teaser in scene 6 -> scene 7 reveal
t_tease=51.50; t_rev=58.64
plate(t_tease,B[5+1]-0.17,215,250); label(t_tease,B[6]-0.17,275,"TOP 1")
glowtext(t_tease+0.1,B[6]-0.17,540,385,"#1 ???",170)
plate(B[6]+0.2,t_rev,215,250); label(B[6]+0.2,t_rev,275,"TOP 1")
glowtext(B[6]+0.3,t_rev,540,385,"#1 ???",170,fadeout=0)
sfx+=[("pop_b",t_tease+0.1),("pop_b",B[6]+0.3)]
en7=63.43
plate(t_rev,en7,215,250); label(t_rev,en7,275,"TOP 1 THẾ GIỚI")
sz=fit("#1 ETIHAD AIRWAYS",900,118)
glowtext(t_rev,en7,540,385,"#1 ETIHAD AIRWAYS",sz,fadeout=0)
# flash on reveal
E(9,t_rev,t_rev+0.45,"Plate","{\\an7\\pos(0,0)\\1c&HFFFFFF&\\1a&H40&\\fad(0,400)\\p1}m 0 0 l 1080 0 l 1080 1920 l 0 1920")
sfx+=[("impact_a",t_rev-0.05)]
# callouts
def callout(st,en,txt,size=250,y=840):
    glowtext(st,en,540,y,txt,size,GOLD,layer=10)
callout(25.82,B[3]-0.12,"100%"); sfx+=[("ding_a",25.82)]
callout(29.55,32.9,"HƠN 100 NĂM",fit("HƠN 100 NĂM",900,140)); sfx+=[("ding_a",29.55)]
callout(46.59,48.95,"7{\\fnNoto Sans Symbols\\b1}★{\\fnBe Vietnam Pro Black}+"); sfx+=[("ding_a",46.59)]
hdr="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Be Vietnam Pro ExtraBold,68,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,1,4.3,2.5,5,40,40,0,1
Style: Title,Be Vietnam Pro Black,110,&H0000C0FF,&H00FFFFFF,&H00101010,&H96000000,0,0,0,0,100,100,1,0,1,5,4,5,40,40,0,1
Style: Label,Be Vietnam Pro ExtraBold,62,&H00FFFFFF,&H00FFFFFF,&H001A1AE0,&H00000000,0,0,0,0,100,100,6,0,3,10,0,5,40,40,0,1
Style: Plate,Be Vietnam Pro,20,&H00000000,&H00000000,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
# plate alpha
ev=[e.replace("Plate,,0,0,0,,{\\an7","Plate,,0,0,0,,{\\1a&H78&\\an7") if "\\p1\\fad(120" in e else e for e in ev]
open('/workspace/proj1/edit/overlay.ass','w').write(hdr+"\n".join(ev)+"\n")
json.dump(sfx,open('/workspace/proj1/edit/sfx_text.json','w'))
print(len(ev),"events;",len(sfx),"text sfx")
