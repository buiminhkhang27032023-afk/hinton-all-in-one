#!/usr/bin/env python3
"""HM-101 v3 — style-match build (ref 2026-10-05). ~34 shots, push-in everywhere, slide/whip + whoosh,
red box / highlighter / underline marks with ding/pop, split layouts, Hinton stat template, karaoke burn-in.
Voice reused from v1 (no TTS)."""
import json, html, shutil
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance

ROOT = Path("/workspace/video-jobs/HM-101"); LV = ROOT / "lam-viec"
HF = LV / "hf_v3"; AS = HF / "assets"; SH = LV / "v3_shots"; SRC = ROOT / "source/assets"
AS.mkdir(parents=True, exist_ok=True); SH.mkdir(parents=True, exist_ok=True)
VO_END = 51.60; TOTAL = 51.90
words = json.loads((LV / "words.json").read_text())["words"]
esc = lambda s: html.escape(s or "", quote=True)

# ---------------------------------------------------------------- plates
def panel(name, src, crop, W, H, mode="fitw", cy=None, maxh=None):
    """Bake a panel JPEG W×H: blurred self background + zoomed foreground crop.
    Returns (rel_path, mapper) where mapper(x,y)->panel px for source coords."""
    im = Image.open(SRC / src).convert("RGB")
    x0, y0, x1, y1 = crop
    if mode == "cover":
        cw, ch = x1 - x0, y1 - y0; ar = W / H; cxm, cym = (x0 + x1) / 2, (y0 + y1) / 2
        if cw / ch > ar: cw = ch * ar
        else: ch = cw / ar
        x0, x1 = cxm - cw / 2, cxm + cw / 2; y0, y1 = cym - ch / 2, cym + ch / 2
        dx = max(0, -x0) - max(0, x1 - im.width); dy = max(0, -y0) - max(0, y1 - im.height)
        x0 += dx; x1 += dx; y0 += dy; y1 += dy
    cw, ch = x1 - x0, y1 - y0
    s = W / cw; maxh = maxh or H
    if ch * s > maxh and mode != "cover": s = maxh / ch
    fw, fh = round(cw * s), round(ch * s)
    fg = im.crop((round(x0), round(y0), round(x1), round(y1))).resize((fw, fh), Image.LANCZOS)
    # background: blurred self, cover
    bs = max(W / im.width, H / im.height) * 1.15
    bg = im.resize((max(1, round(im.width * bs)), max(1, round(im.height * bs))), Image.BILINEAR)
    bx, by = (bg.width - W) // 2, (bg.height - H) // 2
    bg = bg.crop((bx, by, bx + W, by + H)).filter(ImageFilter.GaussianBlur(38))
    bg = ImageEnhance.Brightness(bg).enhance(0.42)
    ox = (W - fw) // 2
    oy = (H - fh) // 2 if cy is None else int(max(0, min(H - fh, cy - fh / 2)))
    bg.paste(fg, (ox, oy))
    out = SH / f"{name}.jpg"; bg.save(out, quality=90)
    shutil.copy(out, AS / out.name)
    return f"assets/{out.name}", (lambda x, y: (ox + (x - x0) * s, oy + (y - y0) * s)), s

# ---------------------------------------------------------------- shot list
# kinds: claim, ss, tb, lr, stat, pres, nokey, chat, flow, eq, outro
# marks: (type, x0,y0,x1,y1, t_offset) in SOURCE px; type hl|box|ul
SHOTS = [
 dict(k="claim", t=0.00),
 dict(k="ss", t=1.32, src="img08_meta_blog_title.png", crop=(90, 40, 910, 350), pill="Nguồn: Meta AI Research",
      marks=[("hl", 118, 82, 775, 143, 0.12), ("hl", 118, 154, 662, 217, 0.32), ("ul", 668, 270, 892, 278, 0.85)], tr="L", whip=True),
 dict(k="pres", t=2.92, ms=3.0),
 dict(k="ss", t=4.90, src="img01_meta_hero.png", crop=(420, 0, 1500, 1080), pill="Nguồn: Meta AI Research", tag="TẠO KIẾN THỨC MỚI", tag_t=0.95, tr="L"),
 dict(k="lr", t=5.88, panels=[("img02_fig1_ellipsoid.png", (300, 0, 2700, 2241), "cover", []),
                              ("img05_fig4_relaxation.png", (500, 0, 3900, 3195), "cover", [])],
      pill="Nguồn: Meta (Figure 1 · 4)", tag="KIẾN THỨC MỚI", tag_ul=True, tag_t=0.30, tr="R"),
 dict(k="ss", t=7.12, src="img15_meta_research_home.png", crop=(60, 90, 1240, 880), pill="Nguồn: research.meta.ai",
      marks=[("hl", 118, 158, 805, 208, 0.18)], badge=("02/10", "MUSE SPARK"), badge_t=0.95, tr="U"),
 dict(k="tb", t=9.44, panels=[("img17_paper1_ellipsoid.png", (0, 30, 1080, 700), "fitw", [("ul", 70, 300, 900, 308, 0.5)]),
                              ("img24_arxiv_abs.png", (0, 60, 620, 380), "fitw", [("hl", 18, 104, 575, 136, 0.75), ("hl", 18, 136, 190, 164, 0.9)])],
      pill="Nguồn: Meta · arXiv 2608.10184", tr="L", whip=True),
 dict(k="stat", t=10.70, num=6, fmt="int", kicker="TOÁN HỌC × AI", label="BÀI BÁO NGHIÊN CỨU", tr="R"),
 dict(k="ss", t=11.90, src="img23_arxiv_abs.png", crop=(0, 60, 610, 420), pill="Nguồn: arXiv 2507.12831",
      marks=[("hl", 18, 104, 595, 136, 0.55), ("hl", 18, 136, 160, 164, 0.75), ("ul", 36, 384, 560, 392, 1.25)],
      badge=("5/6", "LỜI GIẢI MỚI"), badge_t=0.10, tr="L", whip=True),
 dict(k="ss", t=14.14, src="img16_meta_logo.png", crop=(40, 110, 720, 440), pill="Nguồn: Meta",
      marks=[("box", 70, 192, 445, 308, 0.72)], tag="ĐẦU NĂM · HUY CHƯƠNG VÀNG", tag_t=1.0, tr="R"),
 dict(k="stat", t=15.50, num=5, fmt="int", kicker="HUY CHƯƠNG VÀNG", label="KỲ OLYMPIAD", medal=True, tr="L"),
 dict(k="ss", t=17.06, src="img06_fig5_mumford.png", crop=(250, 250, 2972, 2972), pill="Nguồn: Meta (Figure 5)",
      tag="NGHIÊN CỨU MỞ THÌ KHÁC", tag_t=0.5, tr="R", whip=True),
 dict(k="nokey", t=18.74, tr="U"),
 dict(k="pres", t=19.90, ms=12.0),
 dict(k="chat", t=21.60, pill="Minh họa · meta.ai", tr="L"),
 dict(k="flow", t=22.85, tr="R"),
 dict(k="tb", t=24.64, panels=[("img25_arxiv_abs.png", (0, 60, 620, 345), "fitw",
                                [("hl", 36, 186, 600, 210, 0.30), ("hl", 36, 207, 600, 231, 0.48), ("hl", 36, 228, 280, 252, 0.62)]),
                               "tags"],
      pill="Nguồn: arXiv 2608.12415", tr="L", whip=True),
 dict(k="ss", t=26.60, src="img19_paper3_galois.png", crop=(0, 40, 1080, 760), pill="Nguồn: Meta AI Research",
      marks=[("ul", 70, 300, 925, 309, 0.25)], badge=("2024", "BÁC GIẢ THUYẾT"), badge_t=0.70, tr="R"),
 dict(k="ss", t=28.54, src="img04_fig3_384group.png", crop=(200, 0, 2140, 1992), pill="Nguồn: Meta (Figure 3)",
      tag="PHẢN VÍ DỤ", tag_t=0.15, tr="L", whip=True),
 dict(k="stat", t=29.70, num=384, fmt="int", kicker="PHẢN VÍ DỤ: MỘT NHÓM CÓ", label="PHẦN TỬ", tr="U"),
 dict(k="ss", t=31.06, src="img03_fig2_blowup.png", crop=(330, 0, 1590, 814), pill="Nguồn: Meta (Figure 2)",
      tag="SÓNG PHẢI SỤP ĐỔ", tag_t=0.5, tr="R"),
 dict(k="ss", t=32.18, src="img18_paper2_blowup.png", crop=(0, 40, 1080, 640), pill="Nguồn: Meta AI Research",
      marks=[("ul", 70, 300, 900, 309, 0.2), ("box", 60, 335, 700, 395, 0.9)], tag="TRONG THỜI GIAN HỮU HẠN", tag_t=0.95, tr="L", whip=True),
 dict(k="stat", t=33.70, num=2015, fmt="year", kicker="CÂU HỎI BỎ NGỎ TỪ NĂM", label="ĐÃ CÓ LỜI ĐÁP", tr="R"),
 dict(k="tb", t=35.69, panels=[("img14_alexandr_announce.png", (30, 280, 730, 660), "fitw",
                                [("hl", 98, 310, 214, 330, 0.25), ("box", 352, 342, 598, 370, 0.80)]),
                               ("img09_muse_gadgets_hero.png", (30, 60, 830, 340), "fitw", [("ul", 56, 128, 634, 136, 1.05)])],
      pill="X - @alexandr_wang · gadgets.muse.ai", tr="L", whip=True),
 dict(k="ss", t=37.42, src="img12_github_readme.png", crop=(30, 740, 900, 1340), pill="GitHub muse-gadget-sdk",
      marks=[("hl", 62, 1068, 872, 1098, 0.12), ("box", 62, 1262, 182, 1322, 0.62)], tr="R"),
 dict(k="lr", t=38.54, panels=[("img13_github_boards.png", (0, 40, 700, 600), "cover", []),
                               ("img11_muse_project_ideas.png", (300, 120, 900, 700), "cover", [])],
      pill="GitHub · gadgets.muse.ai", tag="PHẦN CỨNG NGUỒN MỞ", tag_t=0.15, tr="U"),
 dict(k="stat", t=39.64, num=5000, fmt="int", kicker="TẶNG NGƯỜI ĐĂNG KÝ", label="MUSE HOME LINK", tr="L", whip=True),
 dict(k="ss", t=40.84, src="img10_muse_home_link.png", crop=(640, 20, 1080, 520), pill="Nguồn: gadgets.muse.ai",
      marks=[("box", 748, 40, 1066, 82, 0.18)], tr="R"),
 dict(k="pres", t=41.90, ms=25.0),
 dict(k="ss", t=43.42, src="img27_arxiv_abs.png", crop=(0, 50, 610, 470), pill="arXiv · bản preprint",
      marks=[("box", 14, 82, 172, 106, 0.15)], stamp="CHƯA BÌNH DUYỆT", stamp_t=0.32, tr="L", whip=True),
 dict(k="lr", t=44.70, panels=[("img20_paper4_relax.png", (0, 0, 1080, 1350), "fitw", []),
                               ("img21_paper5_mumford.png", (0, 0, 1080, 1350), "fitw", [])],
      pill="Nguồn: Meta AI Research", tag="NHÓM KHÁC GIẢI ĐỘC LẬP", tag_hl=True, tag_t=0.80, tr="R"),
 dict(k="eq", t=46.69, tr="U"),
 dict(k="tb", t=48.26, panels=[("img22_paper6_extra.png", (0, 40, 1080, 640), "fitw", []),
                               ("img26_arxiv_abs.png", (0, 60, 620, 380), "fitw", [("hl", 18, 104, 600, 136, 0.30)])],
      pill="Nguồn: Meta · arXiv", tag="KẾT QUẢ CẤP NGHIÊN CỨU", tag_hl=True, tag_t=0.35, tr="L", whip=True),
 dict(k="outro", t=49.44, ms=40.0),
]
for i, s in enumerate(SHOTS):
    s["i"] = i
    s["end"] = SHOTS[i + 1]["t"] if i + 1 < len(SHOTS) else VO_END
    s["dur"] = round(s["end"] - s["t"], 3)

# ---------------------------------------------------------------- html builders
body, tl, sfx = [], [], []   # sfx: (time, name, gain_db)
OVER = 0.30                   # outgoing shot stays under incoming slide
W_CYCLE = ["whoosh_a", "whoosh_b", "whoosh_c"]

def mark_html(sid, j, typ, X0, Y0, X1, Y1, t_abs):
    mid = f"{sid}m{j}"
    w, h = X1 - X0, Y1 - Y0
    if typ == "hl":
        body_ = f'<div class="mk-hl" id="{mid}" style="left:{X0-6:.0f}px;top:{Y0:.0f}px;width:{w+12:.0f}px;height:{h:.0f}px"></div>'
        tl.append(f'tl.fromTo("#{mid}",{{scaleX:0}},{{scaleX:1,duration:0.32,ease:"power2.out",immediateRender:true}},{t_abs:.3f});')
        sfx.append((t_abs, "pop", -6)); sfx.append((t_abs, "marker", -14))
    elif typ == "ul":
        body_ = f'<div class="mk-ul" id="{mid}" style="left:{X0:.0f}px;top:{Y0+2:.0f}px;width:{w:.0f}px"></div>'
        tl.append(f'tl.fromTo("#{mid}",{{scaleX:0}},{{scaleX:1,duration:0.28,ease:"power3.out"}},{t_abs:.3f});')
        sfx.append((t_abs, "pop", -5))
    else:  # box — hand-drawn red rectangle via SVG path (pathLength=1)
        pad = 10; bw, bh = w + 2 * pad, h + 2 * pad
        d = f"M{6},{4} L{bw-4},{0} L{bw},{bh-3} L{2},{bh} L{0},{-2} L{bw*0.25:.0f},{1}"
        body_ = (f'<svg class="mk-box" id="{mid}" style="left:{X0-pad:.0f}px;top:{Y0-pad:.0f}px;width:{bw:.0f}px;height:{bh:.0f}px" '
                 f'viewBox="0 0 {bw:.0f} {bh:.0f}"><path pathLength="1" d="{d}"/></svg>')
        tl.append(f'tl.fromTo("#{mid} path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.36,ease:"power1.inOut"}},{t_abs:.3f});')
        sfx.append((t_abs + 0.05, "ding", -7))
    return body_

def cam(cid, inner, t, dur, origin="50% 45%", s1=1.0, s2=1.14, drift=(0, 0)):
    tl.append(f'tl.fromTo("#{cid}",{{scale:{s1},x:0,y:0}},{{scale:{s2},x:{drift[0]},y:{drift[1]},duration:{dur+OVER:.3f},ease:"none"}},{t:.3f});')
    return f'<div class="cam" id="{cid}" style="transform-origin:{origin}">{inner}</div>'

def pill(txt):
    return f'<div class="pill">{esc(txt)}</div>' if txt else ""

def tag_html(s, sid):
    if not s.get("tag"): return ""
    t = s["t"] + s.get("tag_t", 0.3)
    extra = ""
    if s.get("tag_ul"):
        extra = f'<div class="tag-ul" id="{sid}tu"></div>'
        tl.append(f'tl.fromTo("#{sid}tu",{{scaleX:0}},{{scaleX:1,duration:0.3,ease:"power3.out"}},{t+0.18:.3f});')
        sfx.append((t + 0.18, "pop", -5))
    if s.get("tag_hl"):
        extra = f'<div class="tag-hl" id="{sid}th"></div>'
        tl.append(f'tl.fromTo("#{sid}th",{{scaleX:0}},{{scaleX:1,duration:0.32,ease:"power2.out"}},{t+0.12:.3f});')
        sfx.append((t + 0.12, "pop", -6)); sfx.append((t + 0.12, "marker", -14))
    tl.append(f'tl.fromTo("#{sid}tg",{{scale:0.6,opacity:0,rotation:-3}},{{scale:1,opacity:1,rotation:-1.5,duration:0.22,ease:"back.out(2.4)"}},{t:.3f});')
    if not (s.get("tag_ul") or s.get("tag_hl")): sfx.append((t, "pop", -6))
    ty = s.get("tag_y", 880 if s["k"] == "tb" else (1110 if s["k"] == "lr" else 1095))
    return f'<div class="tagwrap" style="top:{ty}px"><div class="tag" id="{sid}tg">{extra}<span>{esc(s["tag"])}</span></div></div>'

def badge_html(s, sid):
    if not s.get("badge"): return ""
    t = s["t"] + s.get("badge_t", 0.5); big, small = s["badge"]
    bw = 90 + 95 * len(big)
    tl.append(f'tl.fromTo("#{sid}bd",{{scale:0.4,opacity:0,y:40}},{{scale:1,opacity:1,y:0,duration:0.26,ease:"back.out(2.2)"}},{t:.3f});')
    tl.append(f'tl.fromTo("#{sid}bdb path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.34,ease:"power1.inOut"}},{t+0.12:.3f});')
    sfx.append((t, "pop", -5)); sfx.append((t + 0.16, "ding", -7))
    return (f'<div class="badge" id="{sid}bd"><div class="bnum">{esc(big)}'
            f'<svg class="bbox" id="{sid}bdb" viewBox="0 0 {bw} 210" style="width:{bw}px"><path pathLength="1" d="M8,6 L{bw-6},2 L{bw-2},204 L4,208 L2,0 L{bw*0.3:.0f},4"/></svg>'
            f'</div><div class="blabel">{esc(small)}</div></div>')

def stamp_html(s, sid):
    if not s.get("stamp"): return ""
    t = s["t"] + s.get("stamp_t", 0.3)
    tl.append(f'tl.fromTo("#{sid}st",{{scale:2.2,opacity:0,rotation:-14}},{{scale:1,opacity:1,rotation:-8,duration:0.2,ease:"power4.out"}},{t:.3f});')
    sfx.append((t + 0.05, "impact", -10)); sfx.append((t + 0.05, "ding", -9))
    return f'<div class="stamp" id="{sid}st">{esc(s["stamp"])}</div>'

def karaoke_none(): pass

for s in SHOTS:
    i, t, dur, sid = s["i"], s["t"], s["dur"], f"sh{s['i']}"
    k = s["k"]; z = 10 + i
    vis = dur + (OVER if i + 1 < len(SHOTS) else 0)
    inner = ""
    if k == "ss":
        p, mp, sc = panel(sid, s["src"], s["crop"], 1080, 1920, cy=680, maxh=1240)
        mk = ""
        fx, fy = 540, 680
        for j, m in enumerate(s.get("marks", [])):
            X0, Y0 = mp(m[1], m[2]); X1, Y1 = mp(m[3], m[4])
            if j == 0: fx, fy = (X0 + X1) / 2, (Y0 + Y1) / 2
            mk += mark_html(sid, j, m[0], X0, Y0, X1, Y1, t + m[5])
        origin = f"{fx:.0f}px {fy:.0f}px"
        inner = cam(f"{sid}c", f'<img class="plate" src="{p}"/>{mk}', t, dur, origin=origin, s1=1.0, s2=1.16)
        inner += tag_html(s, sid) + badge_html(s, sid) + stamp_html(s, sid) + pill(s.get("pill"))
    elif k in ("tb", "lr"):
        if k == "tb": geo = [(0, 0, 1080, 960), (0, 960, 1080, 960)]
        else: geo = [(0, 190, 540, 900), (540, 190, 540, 900)]
        pans = ""
        for j, pdef in enumerate(s["panels"]):
            gx, gy, gw, gh = geo[j]
            pid = f"{sid}p{j}"
            if pdef == "tags":
                tg = (f'<div class="ptags"><div class="ptag human" id="{pid}a">NGƯỜI VIẾT</div>'
                      f'<div class="ptag ai" id="{pid}b">AI SOẠN</div></div>')
                tl.append(f'tl.fromTo("#{pid}a",{{x:-300,opacity:0}},{{x:0,opacity:1,duration:0.22,ease:"back.out(2)"}},{t+0.66:.3f});')
                tl.append(f'tl.fromTo("#{pid}b",{{x:300,opacity:0}},{{x:0,opacity:1,duration:0.22,ease:"back.out(2)"}},{t+1.16:.3f});')
                sfx.append((t + 0.66, "pop", -5)); sfx.append((t + 1.16, "pop", -5)); sfx.append((t + 1.2, "ding", -9))
                pin = cam(f"{pid}c", f'<div class="pbg"></div>{tg}', t, dur, s2=1.10)
            else:
                src, crop, mode, marks = pdef
                cy = None
                if k == "tb": cy = (gh / 2) if j == 0 else 330
                p, mp, sc = panel(pid, src, crop, gw, gh, mode=mode, cy=cy)
                mk = ""
                for jj, m in enumerate(marks):
                    X0, Y0 = mp(m[1], m[2]); X1, Y1 = mp(m[3], m[4])
                    mk += mark_html(pid, jj, m[0], X0, Y0, X1, Y1, t + m[5])
                pin = cam(f"{pid}c", f'<img class="plate" src="{p}" style="width:{gw}px;height:{gh}px"/>{mk}', t, dur,
                          s2=1.13, drift=((-14 if j else 14), 0) if k == "lr" else (0, 0))
            pans += f'<div class="pan" id="{pid}" style="left:{gx}px;top:{gy}px;width:{gw}px;height:{gh}px">{pin}</div>'
            # panels slide in from opposite sides
            if k == "tb":
                tl.append(f'tl.fromTo("#{pid}",{{x:"{"-" if j==0 else ""}100%"}},{{x:"0%",duration:0.26,ease:"power3.out"}},{t+0.04*j:.3f});')
            else:
                tl.append(f'tl.fromTo("#{pid}",{{y:"{"-" if j==0 else ""}110%"}},{{y:"0%",duration:0.26,ease:"power3.out"}},{t+0.05*j:.3f});')
        div = '<div class="divh"></div>' if k == "tb" else '<div class="divv"></div>'
        inner = f'<div class="darkbg"></div>{pans}{div}' + tag_html(s, sid) + pill(s.get("pill"))
        s["_noslide"] = False
    elif k == "stat":
        n = s["num"]
        start_v = 1990 if s["fmt"] == "year" else 0
        txt0 = str(start_v)
        medal = '<div class="medal" id="%sme"><span>GOLD</span></div>' % sid if s.get("medal") else ""
        nlen = len(f"{n:,}".replace(",", ".")) if s["fmt"] != "year" else 4
        bw = 120 + {1:190,2:190,3:185,4:168}.get(nlen,128) * nlen
        st = (f'<div class="statbg"></div><div class="stripes"></div><div class="redslab"></div>{medal}'
              f'<div class="skick" id="{sid}k">{esc(s["kicker"])}</div>'
              f'<div class="snumw"><span class="snum" id="{sid}n" style="font-size:{ {1:330,2:330,3:320,4:290}.get(nlen,240) }px">{txt0}</span>'
              f'<svg class="sbox" id="{sid}b" viewBox="0 0 {bw} 360" style="width:{bw}px"><path pathLength="1" d="M10,8 L{bw-8},2 L{bw-2},352 L6,358 L2,0 L{bw*0.3:.0f},6"/></svg></div>'
              f'<div class="slab" id="{sid}l"><span>{esc(s["label"])}</span></div>'
              f'<div class="sbrand">HINTON MEDIA · TIN AI</div>')
        inner = cam(f"{sid}c", st, t, dur, s2=1.12)
        cdur = min(0.75, dur * 0.5)
        fmtjs = ('Math.round(o.v).toString()' if s["fmt"] == "year"
                 else 'Math.round(o.v).toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g,".")')
        tl.append(f'(function(){{const o={{v:{start_v}}};tl.fromTo(o,{{v:{start_v}}},{{v:{n},duration:{cdur:.2f},ease:"power2.out",'
                  f'onUpdate:()=>{{const e=document.getElementById("{sid}n");if(e)e.textContent={fmtjs};}}}},{t+0.08:.3f});}})();')
        tl.append(f'tl.fromTo("#{sid}n",{{scale:0.3,opacity:0}},{{scale:1,opacity:1,duration:0.28,ease:"back.out(2.6)"}},{t+0.05:.3f});')
        tl.append(f'tl.fromTo("#{sid}n",{{scale:1}},{{scale:1.12,duration:0.12,yoyo:true,repeat:1,ease:"power1.out",immediateRender:false}},{t+0.08+cdur:.3f});')
        tl.append(f'tl.fromTo("#{sid}k",{{y:-60,opacity:0}},{{y:0,opacity:1,duration:0.24,ease:"power3.out"}},{t+0.02:.3f});')
        tl.append(f'tl.fromTo("#{sid}l",{{x:-700,skewX:-12}},{{x:0,skewX:-8,duration:0.26,ease:"power4.out"}},{t+0.22:.3f});')
        tl.append(f'tl.fromTo("#{sid}b path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.36,ease:"power1.inOut"}},{t+0.08+cdur:.3f});')
        if s.get("medal"):
            tl.append(f'tl.fromTo("#{sid}me",{{scale:0,rotation:-120}},{{scale:1,rotation:0,duration:0.4,ease:"back.out(1.8)"}},{t+0.1:.3f});')
        sfx.append((t + 0.05, "pop", -4)); sfx.append((t + 0.1 + cdur, "ding", -6))
    elif k == "claim":
        cl = ('<div class="statbg"></div><div class="stripes"></div>'
              '<img class="claimbg" src="assets/claim_bg.jpg"/>'
              '<div class="claim">'
              '<div class="cl1" id="cl1">AI GIẢI</div>'
              '<div class="cl2w"><span class="cl2" id="cl2">5</span>'
              '<svg class="sbox" id="clb" viewBox="0 0 330 360" style="width:330px"><path pathLength="1" d="M10,8 L322,2 L328,352 L6,358 L2,0 L100,6"/></svg></div>'
              '<div class="cl3" id="cl3"><span>BÀI TOÁN MỞ</span></div>'
              '<div class="cl4" id="cl4">CHƯA CÓ LỜI GIẢI</div></div>')
        inner = cam(f"{sid}c", cl, t, dur, s1=1.0, s2=1.12)
        tl.append('tl.fromTo("#cl1",{y:-120,opacity:0},{y:0,opacity:1,duration:0.2,ease:"power4.out"},0.0);')
        tl.append('tl.fromTo("#cl2",{scale:3,opacity:0},{scale:1,opacity:1,duration:0.22,ease:"power4.out"},0.12);')
        tl.append('tl.fromTo("#cl3",{x:900},{x:0,duration:0.2,ease:"power4.out"},0.30);')
        tl.append('tl.fromTo("#cl4",{opacity:0,y:30},{opacity:1,y:0,duration:0.18},0.55);')
        tl.append('tl.fromTo("#clb path",{strokeDashoffset:1},{strokeDashoffset:0,duration:0.3,ease:"power1.inOut"},0.62);')
        # numeral 5 must not appear before it is spoken at 1.12 -> show placeholder '?' ... keep simple: number pops at 1.08
        sfx += [(0.0, "impact", -8), (0.12, "pop", -4), (0.30, "whoosh_b", -12), (0.66, "ding", -6)]
    elif k in ("pres", "outro"):
        dv = dur
        dv = dur + (OVER if i + 1 < len(SHOTS) else 0)
        body.append(f'<video class="full pv" id="{sid}v" src="assets/presenter_full.mp4" muted playsinline '
                    f'data-start="{t:.3f}" data-duration="{dv:.3f}" data-media-start="{s["ms"]:.3f}" data-track-index="5" '
                    f'style="z-index:{z};transform-origin:50% 35%"></video>')
        tl.append(f'tl.fromTo("#{sid}v",{{scale:1.04}},{{scale:1.17,duration:{dv:.3f},ease:"none"}},{t:.3f});')
        inner = '<div class="vign"></div>'
        s["_transparent"] = True
        if k == "outro":
            inner += ('<div class="qwrap"><div class="qcard" id="qcard"><div class="qk">CÂU HỎI CHO BẠN</div>'
                      '<div class="qt">AI đã biết tạo kiến thức mới, <span class="qy" id="qy">bạn sẽ dùng nó làm gì?</span></div></div></div>')
            tl.append(f'tl.fromTo("#qcard",{{y:-260,opacity:0,rotation:-4}},{{y:0,opacity:1,rotation:-1.5,duration:0.32,ease:"back.out(1.8)"}},{t+0.15:.3f});')
            tl.append(f'tl.fromTo("#qy",{{backgroundSize:"0% 100%"}},{{backgroundSize:"100% 100%",duration:0.5,ease:"power2.out"}},{t+0.6:.3f});')
            sfx += [(t + 0.15, "pop", -5), (t + 0.62, "ding", -8)]
        sfx.append((t, "impact", -11))
        s["_cut"] = True
    elif k == "nokey":
        nk = ('<div class="statbg"></div><div class="stripes"></div>'
              f'<div class="nk"><div class="nk1" id="{sid}a">KHÔNG CÓ</div>'
              f'<div class="nk2w"><span class="nk2" id="{sid}b">CHÌA ĐÁP ÁN</span>'
              f'<div class="nkx" id="{sid}x"></div></div>'
              f'<div class="nk3" id="{sid}c3">ĐỀ THI ≠ NGHIÊN CỨU MỞ</div></div>')
        inner = cam(f"{sid}c", nk, t, dur, s2=1.12)
        tl.append(f'tl.fromTo("#{sid}a",{{y:-80,opacity:0}},{{y:0,opacity:1,duration:0.2,ease:"power3.out"}},{t+0.02:.3f});')
        tl.append(f'tl.fromTo("#{sid}b",{{scale:1.6,opacity:0}},{{scale:1,opacity:1,duration:0.22,ease:"power4.out"}},{t+0.25:.3f});')
        tl.append(f'tl.fromTo("#{sid}x",{{scaleX:0}},{{scaleX:1,duration:0.22,ease:"power3.out"}},{t+0.55:.3f});')
        tl.append(f'tl.fromTo("#{sid}c3",{{opacity:0}},{{opacity:1,duration:0.2}},{t+0.7:.3f});')
        sfx += [(t + 0.25, "pop", -5), (t + 0.55, "impact", -11), (t + 0.58, "ding", -8)]
    elif k == "chat":
        ch = ('<div class="chatbg"></div><div class="phone" id="%sph"><div class="notch"></div>'
              '<div class="chathd">meta.ai</div><div class="chat">'
              '<div class="bubble q" id="%sq"><span class="ty" id="%sqt">Gợi ý hướng chứng minh?</span></div>'
              '<div class="bubble a" id="%sa"><span class="ty" id="%sat">Thử phản ví dụ nhóm cấp nhỏ…</span></div>'
              '</div></div>') % (sid, sid, sid, sid, sid)
        inner = cam(f"{sid}c", ch, t, dur, s2=1.15) + pill(s.get("pill"))
        tl.append(f'tl.fromTo("#{sid}q",{{scale:0.6,opacity:0}},{{scale:1,opacity:1,duration:0.18,ease:"back.out(2.4)"}},{t+0.1:.3f});')
        tl.append(f'tl.fromTo("#{sid}qt",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.4,ease:"steps(12)"}},{t+0.15:.3f});')
        tl.append(f'tl.fromTo("#{sid}a",{{scale:0.6,opacity:0}},{{scale:1,opacity:1,duration:0.18,ease:"back.out(2.4)"}},{t+0.6:.3f});')
        tl.append(f'tl.fromTo("#{sid}at",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.5,ease:"steps(14)"}},{t+0.65:.3f});')
        sfx += [(t + 0.1, "pop", -7), (t + 0.6, "pop", -7)]
    elif k == "flow":
        fl = ('<div class="statbg"></div><div class="stripes"></div><div class="flow">'
              f'<div class="fnode" id="{sid}f0">NGƯỜI DẪN DẮT</div><div class="farr" id="{sid}a0">▼</div>'
              f'<div class="fnode" id="{sid}f1">AI CỘNG SỰ</div><div class="farr" id="{sid}a1">▼</div>'
              f'<div class="fnode acc" id="{sid}f2">NHÓM THẨM ĐỊNH'
              f'<svg class="fbox" viewBox="0 0 940 170"><path id="{sid}fb" pathLength="1" d="M10,8 L930,2 L936,162 L6,168 L2,0 L300,6"/></svg></div></div>')
        inner = cam(f"{sid}c", fl, t, dur, s2=1.12)
        for j, e in enumerate(["f0", "a0", "f1", "a1", "f2"]):
            tl.append(f'tl.fromTo("#{sid}{e}",{{x:{-500 if j%2==0 else 0},opacity:0}},{{x:0,opacity:1,duration:0.2,ease:"power3.out"}},{t+0.07*j:.3f});')
        tl.append(f'tl.fromTo("#{sid}fb",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.36,ease:"power1.inOut"}},{t+0.5:.3f});')
        sfx += [(t + 0.28, "pop", -8), (t + 0.55, "ding", -7)]
    elif k == "eq":
        eq = ('<div class="statbg"></div><div class="stripes"></div><div class="eq">'
              f'<div class="eqa" id="{sid}e0">CHUYÊN GIA</div><div class="eqp" id="{sid}e1">+</div>'
              f'<div class="eqa y" id="{sid}e2">AI CHAT THƯỜNG</div><div class="eqp" id="{sid}e3">=</div>'
              f'<div class="eqr" id="{sid}e4"><span>KẾT QUẢ CẤP NGHIÊN CỨU</span></div></div>')
        inner = cam(f"{sid}c", eq, t, dur, s2=1.12)
        for j, tt in enumerate([0.0, 0.25, 0.5, 1.15, 1.3]):
            tl.append(f'tl.fromTo("#{sid}e{j}",{{scale:0.4,opacity:0}},{{scale:1,opacity:1,duration:0.2,ease:"back.out(2.4)"}},{t+tt:.3f});')
        sfx += [(t + 0.0, "pop", -6), (t + 0.5, "pop", -6), (t + 1.3, "ding", -7)]

    # ---- transition in
    tr = s.get("tr"); whip = s.get("whip")
    if i > 0 and not s.get("_cut") and tr:
        frm = {"L": 'x:"100%"', "R": 'x:"-100%"', "U": 'y:"100%"'}[tr]
        to = {"L": 'x:"0%"', "R": 'x:"0%"', "U": 'y:"0%"'}[tr]
        bl_from = ',filter:"blur(14px)"' if whip else ""
        bl_to = ',filter:"blur(0px)"' if whip else ""
        tl.append(f'tl.fromTo("#{sid}",{{{frm}{bl_from}}},{{{to}{bl_to},duration:0.24,ease:"power3.out"}},{t:.3f});')
        prev = f"sh{i-1}"
        out = {"L": 'x:"-35%"', "R": 'x:"35%"', "U": 'y:"-30%"'}[tr]
        tl.append(f'tl.fromTo("#{prev}",{{x:"0%",y:"0%"}},{{{out},duration:0.24,ease:"power2.in",immediateRender:false}},{t:.3f});')
        sfx.append((t - 0.08, W_CYCLE[i % 3], -9))
        s["trans"] = "whip" if whip else "slide"
    elif i > 0:
        s["trans"] = "cut"
    else:
        s["trans"] = "open"
    cls = "clip shot tshot" if s.get("_transparent") else "clip shot"
    body.append(f'<div class="{cls}" id="{sid}" data-start="{t:.3f}" data-duration="{vis:.3f}" data-track-index="{1 + i % 2}" style="z-index:{z}">{inner}</div>')

# ---------------------------------------------------------------- karaoke
MERGE = {(0, 5): (1, "5"), (3, 1): (3, "2/10"), (4, 7): (1, "6"), (5, 0): (1, "5"), (6, 10): (1, "5"),
         (11, 5): (5, "2024"), (12, 7): (5, "384"), (14, 7): (5, "2015"), (17, 0): (2, "5.000"), (8, 11): (3, "meta.ai")}
toks = []
by_sent = {}
for wd in words: by_sent.setdefault(wd["sent"], []).append(wd)
for si in sorted(by_sent):
    ws = by_sent[si]; j = 0
    while j < len(ws):
        if (si, j) in MERGE:
            n, disp = MERGE[(si, j)]; grp = ws[j:j + n]
            raw = grp[-1]["word"]
        else:
            n, grp = 1, ws[j:j + 1]; raw = grp[0]["word"]; disp = raw
        punct = raw[-1] in ",.:;!?"
        disp = disp.rstrip(",.:;!?")
        toks.append(dict(sent=si, text=disp, start=grp[0]["start"], end=grp[-1]["end"], brk=punct))
        j += n
COMP = ["phản ví dụ", "muse home link", "bài toán", "nghiên cứu", "lời giải", "đề thi", "đáp án", "kiến thức", "bắt đầu",
        "công bố", "toán học", "bài báo", "câu hỏi", "trước đó", "bỏ ngỏ", "mô hình", "huy chương", "con người", "dẫn dắt",
        "cộng sự", "thẩm định", "lập luận", "đánh dấu", "giả thuyết", "phần tử", "xác nhận", "sụp đổ", "thời gian", "hữu hạn",
        "phần cứng", "nguồn mở", "đăng ký", "bình duyệt", "tạp chí", "độc lập", "chuyên gia", "kết quả", "theo dõi", "mỗi ngày",
        "muse spark", "muse gadgets", "hinton media", "mỗi đoạn", "người viết", "chưa có", "có sẵn", "đầu năm", "một số",
        "nhóm thứ hai", "các nhà", "đáng nói", "chìa đáp án", "chat meta.ai", "tự công bố", "ai chat", "nhóm khác", "bài báo",
        "đưa ra", "từng lập luận", "chạy cùng", "cũng chạy", "tặng người", "người đăng ký", "kỳ olympiad", "cấp nghiên cứu", "tin ai"]
COMP = sorted({tuple(c.split()) for c in COMP}, key=len, reverse=True)
clusters = []
sents_tok = {}
for tk in toks: sents_tok.setdefault(tk["sent"], []).append(tk)
for si in sorted(sents_tok):
    ts = sents_tok[si]; units = []; j = 0
    while j < len(ts):
        for c in COMP:
            n = len(c)
            if tuple(x["text"].lower() for x in ts[j:j+n]) == c and not any(x["brk"] for x in ts[j:j+n-1]):
                units.append(ts[j:j+n]); j += n; break
        else:
            units.append(ts[j:j+1]); j += 1
    cl_s = []; cur = []
    for u in units:
        if cur and len(cur) + len(u) > 3:
            cl_s.append(cur); cur = []
        cur = cur + u
        if cur[-1]["brk"] and len(cur) >= 1:
            cl_s.append(cur); cur = []
    if cur: cl_s.append(cur)
    # merge single-word leftovers into neighbour when result <= 4
    k = 0
    while k < len(cl_s):
        if len(cl_s[k]) == 1 and len(cl_s) > 1:
            if k > 0 and len(cl_s[k-1]) + 1 <= 4 and not cl_s[k-1][-1]["brk"]:
                cl_s[k-1] += cl_s.pop(k); continue
            if k + 1 < len(cl_s) and len(cl_s[k+1]) + 1 <= 4 and not cl_s[k][-1]["brk"]:
                cl_s[k+1] = cl_s[k] + cl_s[k+1]; cl_s.pop(k); continue
        k += 1
    clusters += cl_s
kar = []
for ci, cl in enumerate(clusters):
    st = cl[0]["start"]
    en = clusters[ci + 1][0]["start"] if ci + 1 < len(clusters) else VO_END
    cid = f"k{ci}"
    spans = "".join(f'<span class="kw" id="{cid}w{j}">{esc(tk["text"])}</span>' for j, tk in enumerate(cl))
    kar.append(f'<div class="clip kc" id="{cid}" data-start="{st:.3f}" data-duration="{en-st:.3f}" data-track-index="8"><div class="kin" id="{cid}i">{spans}</div></div>')
    tl.append(f'tl.fromTo("#{cid}i",{{scale:0.82,y:14}},{{scale:1,y:0,duration:0.12,ease:"back.out(2.5)"}},{st:.3f});')
    for j, tk in enumerate(cl):
        tl.append(f'tl.set("#{cid}w{j}",{{color:"#FFD400"}},{tk["start"]:.3f});')
        if j + 1 < len(cl):
            tl.append(f'tl.set("#{cid}w{j}",{{color:"#FFFFFF"}},{cl[j+1]["start"]:.3f});')
body += kar
body.append(f'<div class="clip blackout" id="blackout" data-start="{VO_END}" data-duration="{TOTAL-VO_END:.3f}" data-track-index="9"></div>')
body.append(f'<audio id="mix" src="assets/mix_v3.wav" data-start="0" data-duration="{TOTAL}" data-track-index="10" data-volume="1"></audio>')

# claim background (blur of hero)
im = Image.open(SRC / "img01_meta_hero.png").convert("RGB").resize((1080 * 2, 1215 * 2))
im = im.crop((540, 0, 540 + 1080, 1920)) if im.height >= 1920 else im.resize((1080, 1920))
im = ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(6))).enhance(0.35)
im.save(AS / "claim_bg.jpg", quality=85); shutil.copy(AS / "claim_bg.jpg", SH / "claim_bg.jpg")

css = (LV / "hf_v3_style.css").read_text()
doc = f'''<!doctype html>
<html lang="vi"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=1080, height=1920"/>
<title>HM-101 v3</title>
<script src="assets/gsap.min.js"></script>
<style>{css}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{TOTAL}" data-fps="30">
{chr(10).join(body)}
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tl)}
window.__timelines["main"] = tl;
</script>
</body></html>
'''
(HF / "index.html").write_text(doc)
meta = dict(total=TOTAL, vo_end=VO_END, shots=[{k: v for k, v in s.items() if k in ("i", "k", "t", "end", "dur", "trans", "src", "pill", "panels")} for s in SHOTS],
            sfx=sorted(sfx), clusters=[[{"text": x["text"], "start": x["start"], "end": x["end"]} for x in c] for c in clusters])
(LV / "v3_plan.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1, default=str))
print("shots", len(SHOTS), "clusters", len(clusters), "sfx", len(sfx), "html bytes", len(doc))
print("trans:", {x: sum(1 for s in SHOTS if s.get("trans") == x) for x in ("slide", "whip", "cut", "open")})
