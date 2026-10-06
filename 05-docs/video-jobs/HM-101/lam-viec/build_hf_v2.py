#!/usr/bin/env python3
"""HM-101 v2 HyperFrames composition — heavy GSAP motion, 22 unique scenes, voice reused."""
import json, html
from pathlib import Path

ROOT = Path("/workspace/video-jobs/HM-101")
LV = ROOT / "lam-viec"
HF = LV / "hf_v2"
timings = json.loads((LV / "timings.json").read_text())
sents = timings["sentences"]
assert len(sents) == 22

# Pad scene windows so total = voice length; fill gaps between sentences
TOTAL = 51.74  # match voice (~51.737)

def scene_window(i):
    st = sents[i]["start"]
    # end at next sentence start, or TOTAL for last
    if i + 1 < len(sents):
        en = sents[i + 1]["start"]
    else:
        en = TOTAL
    # first scene starts at 0
    if i == 0:
        st = 0.0  # under presenter hook for first 2.2s
    return round(st, 3), round(en - st, 3)

CAPTIONS = [
    "AI GIẢI 5 BÀI TOÁN MỞ",
    "KHÔNG CÓ ĐÁP ÁN SẴN",
    "TẠO KIẾN THỨC MỚI",
    "02/10 · MUSE SPARK",
    "6 BÀI BÁO",
    "5 LỜI GIẢI MỚI",
    "VÀNG · 5 OLYMPIAD",
    "NGHIÊN CỨU MỞ ≠ ĐỀ THI",
    "NGƯỜI DẪN · AI CỘNG SỰ",
    "NHÓM 2 THẨM ĐỊNH",
    "ĐÁNH DẤU NGƯỜI / AI",
    "BÁC GIẢ THUYẾT 2024",
    "384 PHẦN TỬ",
    "SÓNG SỤP ĐỔ · HỮU HẠN",
    "BỎ NGỎ TỪ 2015",
    "MUSE GADGETS",
    "NGUỒN MỞ · ESP32",
    "5.000 MUSE HOME LINK",
    "CHƯA PEER REVIEW",
    "GIẢI ĐỘC LẬP",
    "CHUYÊN GIA + AI CHAT",
    "FOLLOW HINTON MEDIA",
]

# Scene visual kinds — rotate, never same consecutive full-frame style
# kinds: kenburns, browser, counter, flow, chat, card3d, keyword, paperstack, highlight
KINDS = [
    "kenburns",   # 0 hero
    "card3d",     # 1 no answer
    "browser",    # 2 knowledge
    "kenburns",   # 3 muse spark announce
    "counter",    # 4 six papers  -> 6
    "counter",    # 5 five solutions -> 5
    "counter",    # 6 olympiad -> 5
    "card3d",     # 7 open research
    "chat",       # 8 meta.ai chat
    "flow",       # 9 diagram
    "highlight",  # 10 mark human/AI
    "paperstack", # 11 refute 2024
    "counter",    # 12 384
    "kenburns",   # 13 wave blowup
    "counter",    # 14 2015
    "browser",    # 15 muse gadgets
    "kenburns",   # 16 esp32 boards
    "counter",    # 17 5000
    "card3d",     # 18 caveat
    "browser",    # 19 independent
    "keyword",    # 20 claim
    "cta",        # 21 outro
]

COUNTERS = {
    4: (6, "BÀI BÁO"),
    5: (5, "LỜI GIẢI MỚI"),
    6: (5, "OLYMPIAD VÀNG"),
    12: (384, "PHẦN TỬ"),
    14: (2015, "BỎ NGỎ TỪ"),
    17: (5000, "MUSE HOME LINK"),
}

esc = lambda s: html.escape(s or "", quote=True)

css = r'''
@font-face { font-family:"BVP"; src:url("assets/BeVietnamPro-Bold.ttf"); font-weight:700; }
@font-face { font-family:"BVP"; src:url("assets/BeVietnamPro-ExtraBold.ttf"); font-weight:800; }
@font-face { font-family:"BVP"; src:url("assets/BeVietnamPro-Black.ttf"); font-weight:900; }
html,body{margin:0;padding:0;background:#000;}
#root{position:relative;width:100%;height:100%;overflow:hidden;font-family:"BVP";color:#fff;}
.bgfill{position:absolute;inset:0;background:#0B0F14;}
.layer{position:absolute;inset:0;overflow:hidden;transform-origin:50% 40%;}
.clip{will-change:transform,opacity;}
.fxbg{background:radial-gradient(120% 80% at 50% 25%,#1B2433 0%,#0B0F14 70%);}
.fxbg2{background:radial-gradient(90% 60% at 50% 45%,#2a1f05 0%,#0B0F14 75%);}
.fxbg3{background:radial-gradient(100% 70% at 50% 30%,#132238 0%,#0B0F14 75%);}
.kbbg{position:absolute;inset:-80px;background-size:cover;background-position:center;filter:blur(32px) brightness(.5);}
.kbfit{position:absolute;left:36px;right:36px;top:210px;height:980px;display:flex;align-items:center;justify-content:center;}
.kbfit img{display:block;max-width:100%;max-height:100%;border-radius:22px;box-shadow:0 30px 80px rgba(0,0,0,.6);}
.browser{position:absolute;left:50px;width:980px;top:230px;height:1000px;border-radius:26px;overflow:hidden;background:#fff;box-shadow:0 40px 90px rgba(0,0,0,.55);}
.browser .bar{height:64px;background:#e9ecf1;display:flex;align-items:center;gap:12px;padding:0 24px;}
.browser .bar i{display:block;width:18px;height:18px;border-radius:50%;background:#ff5f57;}
.browser .bar i:nth-child(2){background:#febc2e;} .browser .bar i:nth-child(3){background:#28c840;}
.browser .bar .url{display:block;flex:1;height:34px;margin-left:18px;border-radius:17px;background:#fff;color:#333;font:600 22px/34px "BVP";padding:0 18px;overflow:hidden;white-space:nowrap;}
.browser .viewport{position:absolute;top:64px;left:0;right:0;bottom:0;overflow:hidden;}
.browser .viewport img{display:block;width:100%;transform-origin:50% 0%;}
.hlbar{position:absolute;left:8%;width:0%;height:10px;background:#F5C518;border-radius:6px;box-shadow:0 0 24px rgba(245,197,24,.8);z-index:5;}
.cardwrap{position:absolute;left:70px;width:820px;top:380px;perspective:1200px;}
.tcard{display:block;width:100%;padding:48px 46px;border-radius:34px;background:rgba(255,255,255,.07);border:2px solid rgba(255,255,255,.14);transform-style:preserve-3d;box-shadow:0 40px 80px rgba(0,0,0,.45);}
.tbar{display:block;width:120px;height:14px;border-radius:7px;background:#F5C518;margin-bottom:30px;}
.ttext{font-weight:900;font-size:78px;line-height:1.12;color:#fff;text-transform:uppercase;}
.counterbox{position:absolute;left:60px;width:960px;top:520px;text-align:center;}
.cnum{display:block;font-weight:900;font-size:220px;line-height:1;color:#F5C518;text-shadow:0 0 60px rgba(245,197,24,.45);}
.clabel{display:block;margin-top:18px;font-weight:900;font-size:56px;letter-spacing:2px;color:#fff;}
.phone{position:absolute;left:210px;width:660px;top:200px;height:1100px;border-radius:70px;background:#111;border:14px solid #2b2f36;box-shadow:0 40px 90px rgba(0,0,0,.6);overflow:hidden;}
.phone .notch{position:absolute;top:18px;left:50%;width:170px;height:36px;margin-left:-85px;border-radius:18px;background:#000;}
.phone .chathd{position:absolute;top:70px;left:0;right:0;text-align:center;font-weight:800;font-size:28px;color:#aab;letter-spacing:1px;}
.phone .chat{position:absolute;left:34px;right:34px;top:130px;display:flex;flex-direction:column;gap:22px;}
.bubble{display:block;font-weight:700;font-size:34px;line-height:1.32;padding:22px 28px;border-radius:30px;max-width:90%;}
.bubble.q{align-self:flex-end;background:#2f6bff;color:#fff;border-bottom-right-radius:8px;}
.bubble.a{align-self:flex-start;background:#23262d;color:#f1f1f1;border-bottom-left-radius:8px;}
.cursor{display:inline-block;width:18px;height:34px;background:#F5C518;margin-left:6px;vertical-align:middle;}
.flow{position:absolute;left:50px;right:50px;top:360px;display:flex;flex-direction:column;gap:36px;align-items:center;}
.fnode{width:900px;padding:36px 40px;border-radius:28px;background:rgba(255,255,255,.08);border:2px solid rgba(255,255,255,.16);font-weight:900;font-size:52px;text-align:center;}
.fnode.acc{border-color:#F5C518;box-shadow:0 0 40px rgba(245,197,24,.35);}
.farr{font-size:48px;color:#F5C518;font-weight:900;}
.kwrap{position:absolute;left:50px;width:980px;top:700px;display:flex;align-items:center;justify-content:center;}
.bigword{display:block;font-weight:900;font-size:110px;line-height:1.05;color:#F5C518;text-align:center;text-shadow:0 0 40px rgba(245,197,24,.45);}
.capclaim{position:absolute;left:50px;width:860px;top:1280px;padding:22px 28px;border-radius:22px;background:rgba(11,15,20,.9);border-left:10px solid #F5C518;font-weight:900;font-size:42px;line-height:1.15;box-shadow:0 18px 40px rgba(0,0,0,.5);}
.capclaim .acc{color:#F5C518;}
.chip{position:absolute;left:40px;top:170px;padding:12px 24px;border-radius:999px;background:#F5C518;color:#111;font-weight:900;font-size:34px;letter-spacing:1px;}
.hookbox{position:absolute;left:50px;width:860px;top:1180px;padding:28px 32px;border-radius:26px;background:rgba(11,15,20,.9);box-shadow:0 0 60px rgba(207,44,78,.4);}
.hl{display:block;font-weight:900;font-size:58px;line-height:1.12;color:#fff;}
.hl.y{color:#F5C518;}
.ctabox{position:absolute;left:60px;width:860px;top:1230px;display:flex;flex-direction:column;gap:18px;}
.pill{display:block;padding:20px 36px;border-radius:999px;background:#F5C518;color:#111;font-weight:900;font-size:48px;}
.ctatext{display:block;font-weight:800;font-size:40px;color:#fff;text-shadow:0 4px 14px rgba(0,0,0,.7);}
#pip{position:absolute;overflow:hidden;background:#111;transform-origin:50% 50%;box-shadow:0 18px 50px rgba(0,0,0,.55);left:60px;top:1260px;width:280px;height:280px;border-radius:50%;}
#pip .pipv{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;}
#pipRing{position:absolute;inset:0;border:6px solid #fff;box-sizing:border-box;border-radius:50%;}
.full{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;}
.shade{background:linear-gradient(180deg,rgba(0,0,0,0) 40%,rgba(0,0,0,.55) 100%);}
.pstack{position:absolute;left:90px;top:280px;width:900px;height:1100px;}
.pcard{position:absolute;left:40px;right:40px;height:420px;border-radius:28px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.5);background:#111;}
.pcard img{width:100%;height:100%;object-fit:cover;}
.uline{position:absolute;height:8px;background:#F5C518;border-radius:4px;left:70px;width:0;top:1180px;box-shadow:0 0 20px rgba(245,197,24,.8);}
'''

body = []
tl = []
body.append('<div class="bgfill"></div>')

TRANS_EASE = ["power3.out", "power2.inOut", "back.out(1.6)", "power4.out"]

for i, kind in enumerate(KINDS):
    st, du = scene_window(i)
    img = f"assets/s{i:02d}.jpg"
    cap = CAPTIONS[i]
    sid = f"s{i}"
    ease_in = TRANS_EASE[i % len(TRANS_EASE)]

    if kind == "kenburns":
        body.append(
            f'<div class="clip layer" id="{sid}" data-start="{st}" data-duration="{du}" data-track-index="1">'
            f'<div class="kbbg" style="background-image:url({img})"></div>'
            f'<div class="kbfit"><img id="k{i}" src="{img}"/></div>'
            f'<div class="capclaim" id="cap{i}">{esc(cap)}</div></div>'
        )
        # whip/slide in + strong Ken Burns with easing
        dx = 120 if i % 2 == 0 else -120
        rot = 2 if i % 3 == 0 else -2
        tl.append(f'tl.fromTo("#{sid}",{{x:{dx},rotation:{rot},opacity:0}},{{x:0,rotation:0,opacity:1,duration:0.35,ease:"{ease_in}"}},{st});')
        scale_end = 1.04 + min(du * 0.08, 0.22)
        tl.append(f'tl.fromTo("#k{i}",{{scale:1.08,x:{-dx*0.3}}},{{scale:{scale_end:.3f},x:{dx*0.25},duration:{du},ease:"power2.inOut"}},{st});')
        tl.append(f'tl.fromTo("#cap{i}",{{y:40,opacity:0}},{{y:0,opacity:1,duration:0.28,ease:"power3.out"}},{st+0.15:.3f});')

    elif kind == "browser":
        urls = ["research.meta.ai", "research.meta.ai/blog", "gadgets.muse.ai", "github.com/facebookincubator", "arxiv.org"]
        url = urls[i % len(urls)]
        body.append(
            f'<div class="clip layer fxbg" id="{sid}" data-start="{st}" data-duration="{du}" data-track-index="1">'
            f'<div class="browser" id="br{i}"><div class="bar"><i></i><i></i><i></i><span class="url">{esc(url)}</span></div>'
            f'<div class="viewport"><img id="k{i}" src="{img}"/><div class="hlbar" id="hlb{i}" style="top:42%;"></div></div></div>'
            f'<div class="capclaim" id="cap{i}">{esc(cap)}</div></div>'
        )
        # slide/rotate in
        tl.append(f'tl.fromTo("#br{i}",{{y:180,rotation:4,opacity:0,scale:0.92}},{{y:0,rotation:0,opacity:1,scale:1,duration:0.4,ease:"power3.out"}},{st});')
        tl.append(f'tl.fromTo("#k{i}",{{y:0,scale:1}},{{y:-220,scale:1.08,duration:{du},ease:"power2.inOut"}},{st});')
        tl.append(f'tl.fromTo("#hlb{i}",{{width:"0%"}},{{width:"84%",duration:0.55,ease:"power2.out"}},{st+0.35:.3f});')
        tl.append(f'tl.fromTo("#cap{i}",{{x:-60,opacity:0}},{{x:0,opacity:1,duration:0.3,ease:"power3.out"}},{st+0.2:.3f});')

    elif kind == "counter":
        target, label = COUNTERS[i]
        # For 2015 show year as label prefix differently
        if target == 2015:
            body.append(
                f'<div class="clip layer fxbg2" id="{sid}" data-start="{st}" data-duration="{du}" data-track-index="1">'
                f'<div class="kbbg" style="background-image:url({img});opacity:.35"></div>'
                f'<div class="counterbox"><div class="clabel" id="clab{i}">{esc(label)}</div>'
                f'<div class="cnum" id="cnum{i}">2015</div></div>'
                f'<div class="capclaim" id="cap{i}">{esc(cap)}</div></div>'
            )
            tl.append(f'tl.fromTo("#{sid}",{{scale:1.15,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"power3.out"}},{st});')
            tl.append(f'tl.fromTo("#cnum{i}",{{scale:0.5,opacity:0,filter:"blur(12px)"}},{{scale:1,opacity:1,filter:"blur(0px)",duration:0.45,ease:"back.out(2)"}},{st+0.1:.3f});')
            tl.append(f'tl.fromTo("#clab{i}",{{y:-30,opacity:0}},{{y:0,opacity:1,duration:0.25,ease:"power2.out"}},{st+0.05:.3f});')
        else:
            body.append(
                f'<div class="clip layer fxbg2" id="{sid}" data-start="{st}" data-duration="{du}" data-track-index="1">'
                f'<div class="kbbg" style="background-image:url({img});opacity:.3"></div>'
                f'<div class="counterbox"><div class="cnum" id="cnum{i}">0</div>'
                f'<div class="clabel" id="clab{i}">{esc(label)}</div></div>'
                f'<div class="capclaim" id="cap{i}">{esc(cap)}</div></div>'
            )
            tl.append(f'tl.fromTo("#{sid}",{{x:"{"100%" if i%2 else "-100%"}",opacity:0}},{{x:"0%",opacity:1,duration:0.38,ease:"power4.out"}},{st});')
            # GSAP can tween textContent via snap — use onUpdate in a proxy object
            tl.append(f'window.__c{i}={{v:0}};')
            tl.append(
                f'tl.to(window.__c{i},{{v:{target},duration:{min(du*0.7,1.4):.2f},ease:"power2.out",'
                f'onUpdate:()=>{{const el=document.getElementById("cnum{i}");if(el)el.textContent=Math.round(window.__c{i}.v).toLocaleString("vi-VN");}}}},{st+0.15:.3f});'
            )
            tl.append(f'tl.fromTo("#clab{i}",{{y:40,opacity:0}},{{y:0,opacity:1,duration:0.3,ease:"power2.out"}},{st+0.25:.3f});')
        tl.append(f'tl.fromTo("#cap{i}",{{opacity:0}},{{opacity:1,duration:0.25}},{st+0.2:.3f});')

    elif kind == "card3d":
        body.append(
            f'<div class="clip layer fxbg" id="{sid}" data-start="{st}" data-duration="{du}" data-track-index="1">'
            f'<div class="cardwrap"><div class="tcard" id="tc{i}"><div class="tbar"></div>'
            f'<div class="ttext">{esc(cap)}</div></div></div>'
            f'<div class="uline" id="ul{i}"></div></div>'
        )
        tl.append(f'tl.fromTo("#tc{i}",{{rotateY:-55,rotateX:12,opacity:0,z:-200}},{{rotateY:0,rotateX:0,opacity:1,z:0,duration:0.45,ease:"power3.out"}},{st});')
        tl.append(f'tl.to("#tc{i}",{{rotateY:8,rotateX:-4,scale:1.04,duration:{max(du-0.5,0.4):.2f},ease:"power1.inOut",yoyo:true,repeat:1}},{st+0.45:.3f});')
        tl.append(f'tl.fromTo("#ul{i}",{{width:0}},{{width:700,duration:0.5,ease:"power2.out"}},{st+0.35:.3f});')

    elif kind == "chat":
        body.append(
            f'<div class="clip layer fxbg3" id="{sid}" data-start="{st}" data-duration="{du}" data-track-index="1">'
            f'<div class="phone" id="ph{i}"><div class="notch"></div>'
            f'<div class="chathd">meta.ai · Muse Spark</div>'
            f'<div class="chat">'
            f'<div class="bubble q" id="q{i}">Giúp mình chứng minh threshold ellipsoid?</div>'
            f'<div class="bubble a" id="a{i}">OK — mình đề xuất hướng chứng minh, bạn dẫn dắt.</div>'
            f'</div></div>'
            f'<div class="capclaim" id="cap{i}"><span class="acc">NGƯỜI DẪN</span> · AI CỘNG SỰ</div></div>'
        )
        tl.append(f'tl.fromTo("#ph{i}",{{y:200,rotation:-6,opacity:0}},{{y:0,rotation:0,opacity:1,duration:0.4,ease:"power3.out"}},{st});')
        tl.append(f'tl.fromTo("#q{i}",{{scale:0.7,opacity:0}},{{scale:1,opacity:1,duration:0.25,ease:"back.out(2.5)"}},{st+0.25:.3f});')
        tl.append(f'tl.fromTo("#a{i}",{{scale:0.7,opacity:0}},{{scale:1,opacity:1,duration:0.25,ease:"back.out(2.5)"}},{st+0.7:.3f});')
        tl.append(f'tl.fromTo("#cap{i}",{{y:50,opacity:0}},{{y:0,opacity:1,duration:0.3,ease:"power2.out"}},{st+1.0:.3f});')

    elif kind == "flow":
        body.append(
            f'<div class="clip layer fxbg" id="{sid}" data-start="{st}" data-duration="{du}" data-track-index="1">'
            f'<div class="flow">'
            f'<div class="fnode acc" id="fn0">① NGƯỜI DẪN DẮT</div>'
            f'<div class="farr" id="fa0">↓</div>'
            f'<div class="fnode" id="fn1">② AI CỘNG SỰ</div>'
            f'<div class="farr" id="fa1">↓</div>'
            f'<div class="fnode" id="fn2">③ NHÓM THẨM ĐỊNH</div>'
            f'</div>'
            f'<div class="capclaim" id="cap{i}">{esc(cap)}</div></div>'
        )
        for j, fid in enumerate(["fn0", "fa0", "fn1", "fa1", "fn2"]):
            tl.append(f'tl.fromTo("#{fid}",{{x:{-80 if j%2==0 else 80},opacity:0}},{{x:0,opacity:1,duration:0.28,ease:"power3.out"}},{st+0.08*j:.3f});')
        tl.append(f'tl.to("#fn2",{{borderColor:"#F5C518",boxShadow:"0 0 40px rgba(245,197,24,.45)",duration:0.35}},{st+1.0:.3f});')

    elif kind == "highlight":
        body.append(
            f'<div class="clip layer fxbg" id="{sid}" data-start="{st}" data-duration="{du}" data-track-index="1">'
            f'<div class="browser" id="br{i}"><div class="bar"><i></i><i></i><i></i><span class="url">research.meta.ai</span></div>'
            f'<div class="viewport"><img id="k{i}" src="{img}"/>'
            f'<div class="hlbar" id="hlb{i}" style="top:28%;background:#2f6bff;"></div>'
            f'<div class="hlbar" id="hlb2{i}" style="top:55%;"></div></div></div>'
            f'<div class="capclaim" id="cap{i}">ĐÁNH DẤU <span class="acc">NGƯỜI</span> / <span class="acc">AI</span></div></div>'
        )
        tl.append(f'tl.fromTo("#br{i}",{{scale:0.85,opacity:0}},{{scale:1,opacity:1,duration:0.35,ease:"back.out(1.4)"}},{st});')
        tl.append(f'tl.fromTo("#hlb{i}",{{width:"0%"}},{{width:"70%",duration:0.4,ease:"power2.out"}},{st+0.3:.3f});')
        tl.append(f'tl.fromTo("#hlb2{i}",{{width:"0%"}},{{width:"78%",duration:0.4,ease:"power2.out"}},{st+0.55:.3f});')
        tl.append(f'tl.fromTo("#k{i}",{{y:0}},{{y:-120,duration:{du},ease:"power1.inOut"}},{st});')

    elif kind == "paperstack":
        # use current + nearby paper imgs
        imgs = [f"assets/s{i:02d}.jpg", f"assets/s{(i+1)%22:02d}.jpg", f"assets/s{(i+2)%22:02d}.jpg"]
        body.append(
            f'<div class="clip layer fxbg" id="{sid}" data-start="{st}" data-duration="{du}" data-track-index="1">'
            f'<div class="pstack">'
            f'<div class="pcard" id="pc0{i}" style="top:40px;transform:rotate(-6deg);"><img src="{imgs[0]}"/></div>'
            f'<div class="pcard" id="pc1{i}" style="top:220px;transform:rotate(3deg);"><img src="{imgs[1]}"/></div>'
            f'<div class="pcard" id="pc2{i}" style="top:420px;transform:rotate(-2deg);"><img src="{imgs[2]}"/></div>'
            f'</div>'
            f'<div class="capclaim" id="cap{i}">{esc(cap)}</div></div>'
        )
        for j in range(3):
            tl.append(f'tl.fromTo("#pc{j}{i}",{{y:120,rotation:{(j-1)*12},opacity:0}},{{y:0,rotation:{(j-1)*3},opacity:1,duration:0.35,ease:"power3.out"}},{st+0.12*j:.3f});')
        tl.append(f'tl.to("#pc0{i}",{{y:-20,duration:{du},ease:"power1.inOut"}},{st});')

    elif kind == "keyword":
        body.append(
            f'<div class="clip layer fxbg2" id="{sid}" data-start="{st}" data-duration="{du}" data-track-index="1">'
            f'<div class="kbbg" style="background-image:url({img});opacity:.25"></div>'
            f'<div class="kwrap"><div class="bigword" id="bw{i}">{esc(cap)}</div></div></div>'
        )
        tl.append(f'tl.fromTo("#bw{i}",{{scale:1.4,opacity:0,filter:"blur(16px)",rotation:-4}},{{scale:1,opacity:1,filter:"blur(0px)",rotation:0,duration:0.4,ease:"power3.out"}},{st});')
        tl.append(f'tl.to("#bw{i}",{{scale:1.08,duration:{max(du-0.4,0.3):.2f},ease:"power1.inOut"}},{st+0.4:.3f});')

    elif kind == "cta":
        body.append(
            f'<div class="clip layer shade" id="{sid}" data-start="{st}" data-duration="{du}" data-track-index="3"></div>'
        )
        # outro video handled separately

    # scene exit whip for non-cta (except last visual)
    if kind not in ("cta",) and i < 20:
        # slight fade/slide out near end — HyperFrames hides by data-duration, but motion helps
        pass

# Intro presenter full (hook) — sparse PIP plan:
# intro full 0–2.2, PIP only on chat scene ~19.88–22.73 and maybe counter 17, outro full 49.44–end
# Total PIP+presenter screen time target ≤30%
intro_end = 2.20
outro_st = sents[21]["start"]  # 49.443
outro_du = round(TOTAL - outro_st, 3)

body.append(
    f'<div class="layer" id="introW"><video id="introV" class="full" src="assets/presenter_full.mp4" muted playsinline '
    f'data-start="0" data-duration="{intro_end}" data-media-start="0.000" data-track-index="2"></video></div>'
)
body.append(f'<div class="clip layer shade" data-start="0" data-duration="{intro_end}" data-track-index="3"></div>')
body.append(
    f'<div class="layer" id="outroW"><video id="outroV" class="full" src="assets/presenter_full.mp4" muted playsinline '
    f'data-start="{outro_st}" data-duration="{outro_du}" data-media-start="28.000" data-track-index="2"></video></div>'
)
body.append(f'<div class="clip layer shade" data-start="{outro_st}" data-duration="{outro_du}" data-track-index="3"></div>')

# Hook overlay on intro
body.append(
    f'<div class="clip hook" data-start="0" data-duration="{intro_end}" data-track-index="6">'
    f'<div class="hookbox" id="hookbox"><div class="hl" id="hl0">AI GIẢI 5 BÀI TOÁN MỞ</div>'
    f'<div class="hl y" id="hl1">MUSE SPARK · META</div></div></div>'
)
tl.append(f'tl.fromTo("#introW",{{scale:1}},{{scale:1.08,duration:{intro_end},ease:"power1.inOut"}},0);')
tl.append('tl.fromTo("#hookbox",{scale:0.9,opacity:0},{scale:1,opacity:1,duration:0.25,ease:"power2.out"},0.05);')
tl.append('tl.fromTo("#hl0",{clipPath:"inset(0% 100% 0% 0%)"},{clipPath:"inset(0% 0% 0% 0%)",duration:0.45,ease:"power2.inOut"},0.1);')
tl.append('tl.fromTo("#hl1",{clipPath:"inset(0% 100% 0% 0%)"},{clipPath:"inset(0% 0% 0% 0%)",duration:0.45,ease:"power2.inOut"},0.4);')

# Chip TIN AI for mid section
chip_st = intro_end
chip_du = round(outro_st - chip_st, 3)
body.append(f'<div class="clip" data-start="{chip_st}" data-duration="{chip_du}" data-track-index="6"><div class="chip" id="chip">TIN AI</div></div>')
tl.append(f'tl.fromTo("#chip",{{x:-40,opacity:0}},{{x:0,opacity:1,duration:0.25,ease:"power2.out"}},{chip_st});')

# Sparse PIP: only during chat (s8) and counter 5000 (s17) — ~2.85+2.26 ≈ 5.1s + intro/outro presenter full
# Presenter full intro+outro ≈ 2.2+2.3=4.5; PIP 5.1; total presenter presence ≈ 9.6/51.74 ≈ 18.5%
pip_windows = [
    (sents[8]["start"], scene_window(8)[1], 10.0),
    (sents[17]["start"], scene_window(17)[1], 22.0),
]
body.append('<div id="pip">')
for pi, (pst, pdu, mstart) in enumerate(pip_windows):
    body.append(
        f'<video id="pv{pi}" class="pipv" src="assets/presenter_pip.mp4" muted playsinline '
        f'data-start="{pst}" data-duration="{pdu}" data-media-start="{mstart}" data-track-index="4"></video>'
    )
body.append('<div id="pipRing"></div></div>')
# show/hide pip
tl.append(f'tl.set("#pip",{{opacity:0,scale:0.6}},0);')
for pst, pdu, _ in pip_windows:
    tl.append(f'tl.to("#pip",{{opacity:1,scale:1,duration:0.25,ease:"back.out(2)"}},{pst});')
    tl.append(f'tl.to("#pip",{{opacity:0,scale:0.7,duration:0.2}},{pst+pdu-0.15:.3f});')

# Outro CTA
body.append(
    f'<div class="clip cta" data-start="{outro_st}" data-duration="{outro_du}" data-track-index="6">'
    f'<div class="ctabox" id="ctabox"><div class="pill">FOLLOW @hintonmedia</div>'
    f'<div class="ctatext">Tin AI mỗi ngày · Hinton Media</div></div></div>'
)
tl.append(f'tl.fromTo("#outroW",{{scale:1}},{{scale:1.1,duration:{outro_du},ease:"power1.inOut"}},{outro_st});')
tl.append(f'tl.fromTo("#ctabox",{{y:80,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:"back.out(2)"}},{outro_st+0.15:.3f});')

# Voice
body.append(f'<audio id="vo" src="assets/voice.wav" data-start="0" data-duration="{TOTAL}" data-track-index="9" data-volume="0.82"></audio>')

html_out = f'''<!doctype html>
<html lang="vi"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=1080, height=1920"/>
<title>HM-101 v2</title>
<script src="assets/gsap.min.js"></script>
<style>{css}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{TOTAL}" data-fps="30">
{"".join(body)}
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tl)}
window.__timelines["main"] = tl;
</script>
</body></html>
'''

HF.mkdir(parents=True, exist_ok=True)
(HF / "index.html").write_text(html_out)
print("Wrote", HF / "index.html", "bytes", len(html_out))
print("Scenes", len(KINDS), "duration", TOTAL)
pip_t = sum(w[1] for w in pip_windows) + intro_end + outro_du
print(f"presenter_screen_s≈{pip_t:.2f} pip_pct≈{100*pip_t/TOTAL:.1f}%")
