#!/usr/bin/env python3
"""HM-103 v1.1 — GPT-6 Astra plays WoW blind. Style = HM-101 v3 / STYLE-SPEC ref-20261005.
30 shots (1 VO sentence = 1 shot), push-in everywhere, slide/whip + whoosh, red box / highlighter / underline + ding/pop,
TB/LR splits, Hinton stat template, karaoke burn-in, YouTube 8NmmFdREk5s cuts, presenter 4x as punctuation."""
import json, html, shutil, re
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance

ROOT = Path("/workspace/video-jobs/HM-103"); LV = ROOT / "lam-viec"
HF = LV / "hf"; AS = HF / "assets"; SH = LV / "shots"; SRC = ROOT / "source/assets"; YT = ROOT / "source/yt_clips"
AS.mkdir(parents=True, exist_ok=True); SH.mkdir(parents=True, exist_ok=True)
tts = json.loads((LV / "tts.json").read_text()); sents = tts["sentences"]
words = json.loads((LV / "words.json").read_text())["words"]
assert len(sents) == 30
VO_END = round(sents[-1]["end"] + 0.06, 2); TOTAL = round(VO_END + 0.30, 2)
esc = lambda s: html.escape(s or "", quote=True)
W_AW, W_TOMS, W_IE, W_HOME = "ws_agentwow.png", "ws_toms.png", "ws_ie.png", "ws_agentwow_home.png"

# ------------------------------------------------------------------ plates
def panel(name, src, crop, W, H, mode="fitw", cy=None, maxh=None, bright=0.42):
    im = Image.open(SRC / src).convert("RGB")
    x0, y0, x1, y1 = crop
    if mode == "fitw":  # side margin so the continuous push-in never clips the start/end of text lines
        pad = 0.075 * (x1 - x0); x0 = max(0, x0 - pad); x1 = min(im.width, x1 + pad)
    if mode == "cover":
        cw, ch = x1 - x0, y1 - y0; ar = W / H; cxm, cym = (x0 + x1) / 2, (y0 + y1) / 2
        if cw / ch > ar: cw = ch * ar
        else: ch = cw / ar
        x0, x1 = cxm - cw / 2, cxm + cw / 2; y0, y1 = cym - ch / 2, cym + ch / 2
    cw, ch = x1 - x0, y1 - y0
    s = W / cw; maxh = maxh or H
    if ch * s > maxh and mode != "cover": s = maxh / ch
    fw, fh = round(cw * s), round(ch * s)
    fg = im.crop((round(x0), round(y0), round(x1), round(y1))).resize((fw, fh), Image.LANCZOS)
    full = im
    if im.height > 2.2 * im.width:
        im = im.crop((0, max(0, int(y0) - 500), im.width, min(im.height, int(y1) + 500)))
    bs = max(W / im.width, H / im.height) * 1.15
    bg = im.resize((max(1, round(im.width * bs)), max(1, round(im.height * bs))), Image.BILINEAR)
    bx, by = (bg.width - W) // 2, (bg.height - H) // 2
    bg = bg.crop((bx, by, bx + W, by + H)).filter(ImageFilter.GaussianBlur(38))
    bg = ImageEnhance.Brightness(bg).enhance(bright)
    # light pages blur to grey -> tint toward deep blue so the frame stays in the Hinton palette
    if sum(bg.resize((1, 1)).getpixel((0, 0))) > 240:
        bg = Image.blend(bg, Image.new("RGB", bg.size, (6, 14, 40)), 0.6)
    ox = (W - fw) // 2
    oy = (H - fh) // 2 if cy is None else int(max(0, min(H - fh, cy - fh / 2)))
    bg.paste(fg, (ox, oy))
    out = SH / f"{name}.jpg"; bg.save(out, quality=90); shutil.copy(out, AS / out.name)
    return f"assets/{out.name}", (lambda x, y: (ox + (x - x0) * s, oy + (y - y0) * s)), s

def yt(cid):
    f = YT / f"{cid}.mp4"; shutil.copy(f, AS / f.name); return f"assets/{f.name}"

# ------------------------------------------------------------------ shot list (index = sentence index)
PY = "Nguồn: YouTube 8NmmFdREk5s"
SHOTS = [
 dict(k="claim", pill="Nguồn: agent-wow.sh · Tom's Hardware"),                                                     # 0
 dict(k="stat", num=40, fmt="int", kicker="PHÁ ĐẢO KHU KHỞI ĐẦU ORC", label="PHÚT", pill="Nguồn: Tom's Hardware", tr="L", whip=True),  # 1
 dict(k="stat", num=0, fmt="int", variant="red", kicker="SUỐT CẢ LƯỢT CHƠI", label="LẦN CHẾT", pill="Nguồn: Tom's Hardware", tr="U"),   # 2
 dict(k="lr", panels=[dict(vid="y12_orc_close", nof=True), dict(html="eye")], pill="Nguồn: agent-wow.sh · Tom's Hardware", tr="R", whip=True),  # 3
 dict(k="flow", pill="Nguồn: Tom's Hardware", tr="L"),                                                              # 4
 dict(k="tb", panels=[dict(img=W_AW, crop=(276, 648, 836, 737), marks=[("hl", 295, 708, 827, 727, 0.15), ("box", 609, 657, 750, 676, 0.75)]),
                      dict(vid="y11_codex_prompt", marks=[("box", 780, 290, 932, 314, 0.45)], label="CODEX")],
      pill="agent-wow.sh · YouTube 8NmmFdREk5s", tr="R", whip=True),                                               # 5
 dict(k="yt", vid="y01_orc_new", tag="TẠO ORC", tag_t=0.04, pill=PY, tr="L"),                                       # 6
 dict(k="yt", vid="y02_questgiver", tag="LÀM HẾT NHIỆM VỤ", tag_t=0.25, pill=PY, tr="U", whip=True),               # 7
 dict(k="ss", src=W_TOMS, crop=(160, 455, 800, 1135), marks=[("box", 179, 474, 392, 510, 0.25)], badge=("xhigh", "SUY LUẬN CỰC CAO"), badge_t=1.0,
      pill="Nguồn: Tom's Hardware", tr="R"),                                                                        # 8
 dict(k="pres", ms=6.0, stamp="KHÔNG PHẢI<br>OPENAI CÔNG BỐ", stamp_t=0.35),                                          # 9
 dict(k="ss", src=W_AW, crop=(270, 2195, 990, 2470), marks=[("hl", 690, 2266, 974, 2287, 0.15), ("hl", 280, 2292, 647, 2313, 0.45)],
      tag="KHÔNG CÓ SẴN", tag_ul=True, tag_t=1.0, pill="Nguồn: agent-wow.sh", tr="L", whip=True, zoom=1.16),          # 10
 dict(k="term", pill="Minh họa · cấu hình module trích từ agent-wow.sh", tr="R"),                                  # 11
 dict(k="stat", num=28, fmt="int", kicker="MODULE TỰ VIẾT BẮT ĐƯỢC", label="LOẠI TIN NHẮN SERVER", pill="Nguồn: Tom's Hardware (tự đếm)", tr="U", whip=True),  # 12
 dict(k="tb", panels=[dict(img=W_TOMS, crop=(170, 2598, 790, 2684), marks=[("hl", 433, 2629, 769, 2653, 0.15), ("hl", 179, 2653, 411, 2677, 0.4)]),
                      dict(vid="y13_landscape", label="BẢN ĐỒ THẾ GIỚI")], pill="Tom's Hardware · YouTube 8NmmFdREk5s", tr="L"),  # 13
 dict(k="pres", ms=17.0, tag="TỰ VIẾT TÌM ĐƯỜNG · C++", tag_hl=True, tag_t=0.3, tr="R", whip=True),                  # 14
 dict(k="tb", panels=[dict(img=W_AW, crop=(270, 5180, 990, 5378), marks=[("box", 685, 5326, 724, 5343, 0.2), ("hl", 392, 5350, 571, 5369, 0.5)]),
                      dict(img=W_AW, crop=(282, 5545, 760, 5815), marks=[("ul", 365, 5576, 499, 5582, 0.85), ("box", 467, 5789, 710, 5806, 1.05)])],
      pill="Nguồn: agent-wow.sh", tr="U"),                                                                         # 15
 dict(k="tb", panels=[dict(vid="y03_path_cacti", label="TÌM ĐƯỜNG"),
                      dict(img=W_AW, crop=(268, 5062, 728, 5142), marks=[("box", 551, 5089, 617, 5114, 0.35)])],
      tag="TỐI ƯU", tag_t=0.55, tag_y=1020, pill="agent-wow.sh · YouTube 8NmmFdREk5s", tr="L", whip=True),             # 16
 dict(k="ss", src=W_IE, crop=(110, 2842, 700, 2960), marks=[("hl", 452, 2861, 686, 2885, 0.15), ("hl", 120, 2893, 368, 2917, 0.45)],
      tag="LÊN KẾ HOẠCH", tag_t=1.0, pill="Nguồn: Interesting Engineering", tr="R", zoom=1.16),                      # 17
 dict(k="yt", vid="y04_vendor", tag="BÁN ĐỒ RÁC", tag_t=0.04, pill=PY, tr="L", whip=True),                          # 18
 dict(k="yt", vid="y05_gear", tag="MẶC ĐỒ XỊN HƠN", tag_t=0.04, pill=PY, tr="R"),                                   # 19
 dict(k="yt", vid="y06_trainer", tag="HỌC KỸ NĂNG TRƯỚC", tag_t=0.2, pill=PY, tr="U", whip=True),                   # 20
 dict(k="lr", panels=[dict(vid="y07_cave", lab="TRONG HANG"), dict(html="quests")], pill=PY, tr="L"),               # 21
 dict(k="lr", panels=[dict(vid="y09_valley_den", lab="VALLEY OF TRIALS"), dict(vid="y08_senjin", lab="SEN'JIN VILLAGE")], pill=PY, tr="R", whip=True),  # 22
 dict(k="ss", src=W_HOME, crop=(270, 112, 1010, 345), marks=[("hl", 280, 131, 998, 150, 0.15), ("hl", 280, 157, 526, 176, 0.35)],
      tag="THÍ NGHIỆM ĐỘC LẬP", tag_hl=True, tag_t=0.9, pill="Nguồn: agent-wow.sh", tr="L"),                       # 23
 dict(k="pres", ms=29.0, stamp="CHƯA KIỂM CHỨNG", stamp_t=0.25),                                                    # 24
 dict(k="tb", panels=[dict(html="azb"),
                      dict(img=W_HOME, crop=(270, 505, 1010, 595), marks=[("hl", 381, 519, 644, 538, 0.3), ("ul", 595, 561, 953, 567, 0.75)])],
      pill="Nguồn: agent-wow.sh", tr="R", whip=True),                             # 25
 dict(k="tb", panels=[dict(html="wallwarn", label="WALL CLIP · LỖI BẢN ĐỒ", lred=True),
                      dict(img=W_AW, crop=(270, 6938, 1000, 7016), marks=[("hl", 444, 6970, 745, 6989, 0.3), ("box", 750, 6970, 990, 6989, 0.8)])],
      pill="Nguồn: agent-wow.sh", tr="L"),                                                                        # 26 v1.1: graphic warn, no y10
 dict(k="stat", num=16, fmt="k", kicker="TRƯỚC ĐÓ TỰ VIẾT", label="DÒNG CODE", strike="LỖI QUÁ → BỎ", strike_t=2.2, pill="Nguồn: agent-wow.sh", tr="U", whip=True),  # 27
 dict(k="tb", panels=[dict(img="cdn_ie_hero.png", crop=(300, 0, 1620, 1080), mode="cover"),
                      dict(img=W_AW, crop=(270, 535, 990, 615), marks=[("hl", 700, 564, 935, 583, 0.2), ("box", 357, 590, 646, 609, 0.75)])],
      tag="RAID HEROIC", tag_t=0.45, tag_y=820, pill="agent-wow.sh · ảnh: Interesting Engineering", tr="R"),          # 28
 dict(k="outro", ms=40.0),                                                                                          # 29
]
for i, s in enumerate(SHOTS):
    s["i"] = i
    s["t"] = 0.0 if i == 0 else round(sents[i]["start"] - 0.06, 3)
for i, s in enumerate(SHOTS):
    s["end"] = SHOTS[i + 1]["t"] if i + 1 < len(SHOTS) else VO_END
    s["dur"] = round(s["end"] - s["t"], 3)

# ------------------------------------------------------------------ builders
body, tl, sfx = [], [], []
OVER = 0.30
W_CYCLE = ["whoosh_a", "whoosh_b", "whoosh_c"]
vtrack = [3, 4]

def mark_html(mid, typ, X0, Y0, X1, Y1, t_abs):
    w, h = X1 - X0, Y1 - Y0
    if typ == "hl":
        b = f'<div class="mk-hl" id="{mid}" style="left:{X0-6:.0f}px;top:{Y0:.0f}px;width:{w+12:.0f}px;height:{h:.0f}px"></div>'
        tl.append(f'tl.fromTo("#{mid}",{{scaleX:0}},{{scaleX:1,duration:0.32,ease:"power2.out",immediateRender:true}},{t_abs:.3f});')
        sfx.append((t_abs, "pop", -6)); sfx.append((t_abs, "marker", -14))
    elif typ == "ul":
        b = f'<div class="mk-ul" id="{mid}" style="left:{X0:.0f}px;top:{Y0+2:.0f}px;width:{w:.0f}px"></div>'
        tl.append(f'tl.fromTo("#{mid}",{{scaleX:0}},{{scaleX:1,duration:0.28,ease:"power3.out"}},{t_abs:.3f});')
        sfx.append((t_abs, "pop", -5))
    else:
        pad = 10; bw, bh = w + 2 * pad, h + 2 * pad
        d = f"M6,4 L{bw-4:.0f},0 L{bw:.0f},{bh-3:.0f} L2,{bh:.0f} L0,-2 L{bw*0.25:.0f},1"
        b = (f'<svg class="mk-box" id="{mid}" style="left:{X0-pad:.0f}px;top:{Y0-pad:.0f}px;width:{bw:.0f}px;height:{bh:.0f}px" '
             f'viewBox="0 0 {bw:.0f} {bh:.0f}"><path pathLength="1" d="{d}"/></svg>')
        tl.append(f'tl.fromTo("#{mid} path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.36,ease:"power1.inOut"}},{t_abs:.3f});')
        sfx.append((t_abs + 0.05, "ding", -7))
    return b

def cam(cid, inner, t, dur, origin="50% 45%", s1=1.0, s2=1.14, drift=(0, 0)):
    tl.append(f'tl.fromTo("#{cid}",{{scale:{s1},x:0,y:0}},{{scale:{s2},x:{drift[0]},y:{drift[1]},duration:{dur+OVER:.3f},ease:"none"}},{t:.3f});')
    return f'<div class="cam" id="{cid}" style="transform-origin:{origin}">{inner}</div>'

def pill(txt): return f'<div class="pill">{esc(txt)}</div>' if txt else ""

def tag_html(s, sid):
    if not s.get("tag"): return ""
    t = s["t"] + s.get("tag_t", 0.3); extra = ""
    if s.get("tag_ul"):
        extra = f'<div class="tag-ul" id="{sid}tu"></div>'
        tl.append(f'tl.fromTo("#{sid}tu",{{scaleX:0}},{{scaleX:1,duration:0.3,ease:"power3.out"}},{t+0.18:.3f});'); sfx.append((t + 0.18, "pop", -5))
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
    two = " two" if "<br>" in s["stamp"] else ""
    return f'<div class="stamp{two}" id="{sid}st">{s["stamp"]}</div>'

def html_panel(kind, pid, t):
    if kind == "eye":
        tl.append(f'tl.fromTo("#{pid}x",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.3,ease:"power2.out"}},{t+0.35:.3f});')
        tl.append(f'tl.fromTo("#{pid}e",{{scale:0.5,opacity:0}},{{scale:1,opacity:1,duration:0.25,ease:"back.out(2)"}},{t+0.05:.3f});')
        sfx.append((t + 0.38, "impact", -12)); sfx.append((t + 0.4, "ding", -9))
        return (f'<div class="eyep"><svg id="{pid}e" viewBox="0 0 200 200"><path d="M10,100 Q100,20 190,100 Q100,180 10,100 Z" fill="none" stroke="#fff" stroke-width="12"/>'
                f'<circle cx="100" cy="100" r="32" fill="#FFD400"/><path id="{pid}x" pathLength="1" d="M28,28 L172,172" stroke="#FF1E2D" stroke-width="18" stroke-linecap="round" '
                f'style="stroke-dasharray:1;stroke-dashoffset:1"/></svg><div class="et">AI KHÔNG<br>NHÌN THẤY</div></div>')
    if kind == "quests":
        for j, dt in enumerate((0.15, 0.45)):
            tl.append(f'tl.fromTo("#{pid}q{j}",{{x:300,opacity:0,rotation:6}},{{x:0,opacity:1,rotation:{-2 if j else 2},duration:0.24,ease:"back.out(2)"}},{t+dt:.3f});')
            tl.append(f'tl.fromTo("#{pid}k{j}",{{scale:0}},{{scale:1,duration:0.2,ease:"back.out(3)"}},{t+dt+0.25:.3f});')
            sfx.append((t + dt, "pop", -6)); sfx.append((t + dt + 0.25, "ding", -9))
        tl.append(f'tl.fromTo("#{pid}o",{{scale:0.4,opacity:0}},{{scale:1,opacity:1,duration:0.22,ease:"back.out(2.4)"}},{t+0.95:.3f});'); sfx.append((t + 0.95, "pop", -5))
        return (f'<div class="qpan"><div class="qc" id="{pid}q0"><small>NHIỆM VỤ HANG</small>#1<div class="qck" id="{pid}k0">✓</div></div>'
                f'<div class="qc" id="{pid}q1"><small>NHIỆM VỤ HANG</small>#2<div class="qck" id="{pid}k1">✓</div></div>'
                f'<div class="qone" id="{pid}o">LÀM 1 LẦN</div></div>')
    if kind == "azb":
        tl.append(f'tl.fromTo("#{pid}a",{{y:-60,opacity:0}},{{y:0,opacity:1,duration:0.22,ease:"power3.out"}},{t+0.1:.3f});')
        tl.append(f'tl.fromTo("#{pid}n",{{scale:2,opacity:0}},{{scale:1,opacity:1,duration:0.2,ease:"power4.out"}},{t+0.45:.3f});')
        tl.append(f'tl.fromTo("#{pid}x",{{scaleX:0}},{{scaleX:1,duration:0.24,ease:"power3.out"}},{t+0.8:.3f});')
        sfx.extend([(t + 0.1, "pop", -6), (t + 0.45, "pop", -5), (t + 0.8, "impact", -11), (t + 0.84, "ding", -8)])
        return (f'<div class="plabel">SERVER RIÊNG · WoW 3.3.5a</div><div class="azp" style="padding-top:300px"><div id="{pid}a" style="text-align:center"><div class="az1">AzerothCore</div></div>'
                f'<div style="display:flex;align-items:center;gap:28px"><div class="azne" id="{pid}n">≠</div><div class="azb">BLIZZARD<div class="azx" id="{pid}x"></div></div></div></div>')
    if kind == "wallwarn":
        # HM-103 v1.1: kinetic warning plate — replaces misleading y10_wallclip footage
        tl.append(f'tl.fromTo("#{pid}fr",{{opacity:0}},{{opacity:1,duration:0.12,ease:"power2.out"}},{t+0.04:.3f});')
        tl.append(f'tl.fromTo("#{pid}tr",{{scale:0.2,opacity:0,rotation:-18}},{{scale:1,opacity:1,rotation:0,duration:0.28,ease:"back.out(2.6)"}},{t+0.08:.3f});')
        tl.append(f'tl.fromTo("#{pid}ti",{{y:40,opacity:0,scale:0.85}},{{y:0,opacity:1,scale:1,duration:0.24,ease:"power4.out"}},{t+0.32:.3f});')
        tl.append(f'tl.fromTo("#{pid}sl",{{x:-520,skewX:-16,opacity:0}},{{x:0,skewX:-8,opacity:1,duration:0.26,ease:"power4.out"}},{t+0.52:.3f});')
        tl.append(f'tl.fromTo("#{pid}cp",{{opacity:0}},{{opacity:1,duration:0.18,ease:"power2.out"}},{t+0.78:.3f});')
        sfx.extend([(t + 0.1, "impact", -10), (t + 0.34, "pop", -5), (t + 0.54, "ding", -7), (t + 0.8, "pop", -8)])
        return (
            f'<div class="wwrap"><div class="wwframe" id="{pid}fr"></div>'
            f'<div class="wwtri" id="{pid}tr"><svg viewBox="0 0 200 180">'
            f'<polygon points="100,8 192,168 8,168" fill="#FF1E2D"/>'
            f'<polygon points="100,28 172,158 28,158" fill="#FFD400"/>'
            f'<text x="100" y="140" text-anchor="middle" font-size="92" font-weight="900" font-family="Montserrat,Arial Black,sans-serif" fill="#0a0a0a">!</text>'
            f'</svg></div>'
            f'<div class="wwtitle" id="{pid}ti">WALL CLIP</div>'
            f'<div class="wwslab" id="{pid}sl">LỖI BẢN ĐỒ</div>'
            f'<div class="wwcap" id="{pid}cp">KHAI THÁC LỖI VA CHẠM · MINH HỌA</div>'
            f'<div class="wwbrand">HINTON MEDIA · TIN AI</div></div>'
        )
    raise ValueError(kind)

def video_layer(sid, z, parts, t, vis):
    """Root-level wrapper (not a clip) holding timed <video>s for a shot; hidden outside its window."""
    vid = f"vo{sid}"
    tl.append(f'tl.set("#{vid}",{{autoAlpha:0}},0);tl.set("#{vid}",{{autoAlpha:1}},{t:.3f});tl.set("#{vid}",{{autoAlpha:0}},{t+vis:.3f});')
    body.append(f'<div class="vo" id="{vid}" style="z-index:{z}">{"".join(parts)}</div>')
    return vid

def vtag(src, vid_id, t, vis, ms=0.0, track=None):
    tr = track if track is not None else vtrack[0]
    if track is None: vtrack.reverse()
    return (f'<video class="vfill" id="{vid_id}" src="{src}" muted playsinline data-start="{t:.3f}" data-duration="{vis:.3f}" '
            f'data-media-start="{ms:.3f}" data-track-index="{tr}"></video>')

movers = {}
for s in SHOTS:
    i, t, dur, sid, k = s["i"], s["t"], s["dur"], f"sh{s['i']}", s["k"]
    z_v, z = 10 + 2 * i, 11 + 2 * i
    vis = dur + (OVER if i + 1 < len(SHOTS) else 0)
    inner = ""; transparent = False; mv = [f"#{sid}"]
    zoom = s.get("zoom", 1.16)
    if k == "ss":
        p, mp, sc = panel(sid, s["src"], s["crop"], 1080, 1920, cy=680, maxh=1240)
        mk = ""; fx, fy = 540, 680
        for j, m in enumerate(s.get("marks", [])):
            X0, Y0 = mp(m[1], m[2]); X1, Y1 = mp(m[3], m[4])
            if j == 0: fx, fy = (X0 + X1) / 2, (Y0 + Y1) / 2
            mk += mark_html(f"{sid}m{j}", m[0], X0, Y0, X1, Y1, t + m[5])
        inner = cam(f"{sid}c", f'<img class="plate" src="{p}"/>{mk}', t, dur, origin=f"540px {fy:.0f}px", s2=zoom)
        inner += tag_html(s, sid) + badge_html(s, sid) + stamp_html(s, sid) + pill(s.get("pill"))
    elif k == "yt":
        src = yt(s["vid"])
        tl.append(f'tl.fromTo("#{sid}vc",{{scale:1.0}},{{scale:1.15,duration:{vis:.3f},ease:"none"}},{t:.3f});')
        vl = video_layer(sid, z_v, [f'<div class="vcam" id="{sid}vc" style="transform-origin:50% 36%">{vtag(src, sid+"v", t, vis)}</div>'], t, vis)
        mv.append(f"#{vl}"); transparent = True
        inner = tag_html(s, sid) + badge_html(s, sid) + pill(s.get("pill"))
    elif k in ("tb", "lr"):
        geo = [(0, 0, 1080, 960), (0, 960, 1080, 960)] if k == "tb" else [(0, 190, 540, 900), (540, 190, 540, 900)]
        pans, vparts = "", ['<div class="darkbg"></div>']
        has_vid = any("vid" in p for p in s["panels"])
        for j, pd in enumerate(s["panels"]):
            gx, gy, gw, gh = geo[j]; pid = f"{sid}p{j}"
            if k == "tb": slide = (f'x:{-1080 if j == 0 else 1080}', 'x:0', 0.04 * j)
            else: slide = (f'y:{-990 if j == 0 else 990}', 'y:0', 0.05 * j)
            lab = ""
            if pd.get("label"): lab = f'<div class="plabel{" r" if pd.get("lred") else ""}" id="{pid}lb">{esc(pd["label"])}</div>'
            if pd.get("lab"): lab = f'<div class="lrlab"><span id="{pid}lb">{esc(pd["lab"])}</span></div>'
            if lab:
                tl.append(f'tl.fromTo("#{pid}lb",{{scale:0.5,opacity:0}},{{scale:1,opacity:1,duration:0.2,ease:"back.out(2.4)"}},{t+0.3+0.1*j:.3f});')
                sfx.append((t + 0.3 + 0.1 * j, "pop", -8))
            if "vid" in pd:
                src = yt(pd["vid"]); mk = ""
                for jj, m in enumerate(pd.get("marks", [])):
                    mk += mark_html(f"{pid}m{jj}", m[0], m[1], m[2], m[3], m[4], t + m[5])
                nof = ""
                if pd.get("nof"):
                    nof = f'<div class="scan"></div><div class="nof" id="{pid}nf"><b>0</b><i>KHUNG HÌNH</i></div>'
                    tl.append(f'tl.fromTo("#{pid}nf",{{opacity:0}},{{opacity:1,duration:0.08,ease:"steps(2)"}},{t+0.45:.3f});')
                    sfx.append((t + 0.45, "impact", -12))
                tl.append(f'tl.fromTo("#{pid}vc",{{scale:1.0}},{{scale:1.13,duration:{vis:.3f},ease:"none"}},{t:.3f});')
                vparts.append(f'<div class="vp" id="{pid}v" style="left:{gx}px;top:{gy}px;width:{gw}px;height:{gh}px">'
                              f'<div class="vcam" id="{pid}vc">{vtag(src, pid+"vv", t, vis)}{mk}{nof}</div>{lab}</div>')
                tl.append(f'tl.fromTo("#{pid}v",{{{slide[0]}}},{{{slide[1]},duration:0.26,ease:"power3.out"}},{t+slide[2]:.3f});')
                continue
            if "html" in pd:
                pin = cam(f"{pid}c", html_panel(pd["html"], pid, t), t, dur, s2=1.10)
            else:
                cy = ((gh / 2) if j == 0 else 230) if k == "tb" else None
                p, mp, sc = panel(pid, pd["img"], pd["crop"], gw, gh, mode=pd.get("mode", "fitw"), cy=cy)
                mk = ""; fx, fy = gw / 2, gh / 2
                for jj, m in enumerate(pd.get("marks", [])):
                    X0, Y0 = mp(m[1], m[2]); X1, Y1 = mp(m[3], m[4])
                    if jj == 0: fx, fy = (X0 + X1) / 2, (Y0 + Y1) / 2
                    mk += mark_html(f"{pid}m{jj}", m[0], X0, Y0, X1, Y1, t + m[5])
                pin = cam(f"{pid}c", f'<img class="plate" src="{p}" style="width:{gw}px;height:{gh}px"/>{mk}', t, dur,
                          origin=f"{gw/2:.0f}px {fy:.0f}px", s2=1.12)
            pans += f'<div class="pan" id="{pid}" style="left:{gx}px;top:{gy}px;width:{gw}px;height:{gh}px">{pin}{lab}</div>'
            tl.append(f'tl.fromTo("#{pid}",{{{slide[0]}}},{{{slide[1]},duration:0.26,ease:"power3.out"}},{t+slide[2]:.3f});')
        div = '<div class="divh"></div>' if k == "tb" else '<div class="divv"></div>'
        if has_vid:
            vl = video_layer(sid, z_v, vparts, t, vis); mv.append(f"#{vl}"); transparent = True
            inner = f'{pans}{div}' + tag_html(s, sid) + pill(s.get("pill"))
        else:
            inner = f'<div class="darkbg"></div>{pans}{div}' + tag_html(s, sid) + pill(s.get("pill"))
    elif k == "stat":
        n = s["num"]; red = s.get("variant") == "red"
        disp_final = f"{n}K" if s["fmt"] == "k" else str(n)
        nlen = len(disp_final)
        fs = {1: 400, 2: 330, 3: 320, 4: 290}.get(nlen, 240)
        bw = 120 + {1: 230, 2: 190, 3: 185, 4: 168}.get(nlen, 128) * nlen
        strike = ""
        if s.get("strike"):
            strike = f'<div class="sstrike" id="{sid}x"></div>'
        st = (f'<div class="statbg{" red" if red else ""}"></div><div class="stripes"></div><div class="redslab"></div>'
              f'<div class="skick" id="{sid}k">{esc(s["kicker"])}</div>'
              f'<div class="snumw"><span class="snum{" red" if red else ""}" id="{sid}n" style="font-size:{fs}px">{"0" + ("K" if s["fmt"]=="k" else "")}</span>'
              f'<svg class="sbox" id="{sid}b" viewBox="0 0 {bw} 360" style="width:{bw}px"><path pathLength="1" d="M10,8 L{bw-8},2 L{bw-2},352 L6,358 L2,0 L{bw*0.3:.0f},6"/></svg>{strike}</div>'
              f'<div class="slab" id="{sid}l"><span>{esc(s["label"])}</span></div>'
              + (f'<div class="sstamp"><span id="{sid}ss">{esc(s["strike"])}</span></div>' if s.get("strike") else "")
              + '<div class="sbrand">HINTON MEDIA · TIN AI</div>')
        inner = cam(f"{sid}c", st, t, dur, s2=1.12) + pill(s.get("pill"))
        cdur = min(0.7, dur * 0.45)
        if n > 0:
            suf = '+"K"' if s["fmt"] == "k" else ""
            tl.append(f'(function(){{const o={{v:0}};tl.fromTo(o,{{v:0}},{{v:{n},duration:{cdur:.2f},ease:"power2.out",'
                      f'onUpdate:()=>{{const e=document.getElementById("{sid}n");if(e)e.textContent=Math.round(o.v).toString(){suf};}}}},{t+0.08:.3f});}})();')
        tl.append(f'tl.fromTo("#{sid}n",{{scale:{2.6 if red else 0.3},opacity:0}},{{scale:1,opacity:1,duration:{0.2 if red else 0.28},ease:"{"power4.out" if red else "back.out(2.6)"}"}},{t+0.05:.3f});')
        tl.append(f'tl.fromTo("#{sid}n",{{scale:1}},{{scale:1.12,duration:0.12,yoyo:true,repeat:1,ease:"power1.out",immediateRender:false}},{t+0.08+cdur:.3f});')
        tl.append(f'tl.fromTo("#{sid}k",{{y:-60,opacity:0}},{{y:0,opacity:1,duration:0.24,ease:"power3.out"}},{t+0.02:.3f});')
        tl.append(f'tl.fromTo("#{sid}l",{{x:-700,skewX:-12}},{{x:0,skewX:-8,duration:0.26,ease:"power4.out"}},{t+0.22:.3f});')
        tl.append(f'tl.fromTo("#{sid}b path",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.36,ease:"power1.inOut"}},{t+0.08+cdur:.3f});')
        sfx.append((t + 0.05, "impact" if red else "pop", -6 if red else -4)); sfx.append((t + 0.1 + cdur, "ding", -6))
        if s.get("strike"):
            ts = t + s.get("strike_t", 1.2)
            tl.append(f'tl.fromTo("#{sid}x",{{scaleX:0}},{{scaleX:1,duration:0.22,ease:"power3.out"}},{ts:.3f});')
            tl.append(f'tl.fromTo("#{sid}ss",{{scale:2.2,opacity:0,rotation:-14}},{{scale:1,opacity:1,rotation:-6,duration:0.2,ease:"power4.out"}},{ts+0.15:.3f});')
            sfx += [(ts, "impact", -10), (ts + 0.18, "ding", -8)]
    elif k == "claim":
        cl = ('<div class="statbg"></div><div class="stripes"></div><img class="claimbg" src="assets/claim_bg.jpg"/>'
              '<div class="claim"><div class="cl1" id="cl1">AI CHƠI</div>'
              '<div class="cl2w" style="width:760px"><span class="cl2" id="cl2" style="font-size:300px">WOW</span>'
              '<svg class="sbox" id="clb" viewBox="0 0 760 360" style="width:760px"><path pathLength="1" d="M10,8 L752,2 L758,352 L6,358 L2,0 L230,6"/></svg></div>'
              '<div class="cl3" id="cl3"><span style="font-size:72px;white-space:nowrap">KHÔNG NHÌN MÀN HÌNH</span></div>'
              '<div class="cl4" id="cl4">GPT-6 ASTRA · AGENT-WOW</div></div>')
        inner = cam(f"{sid}c", cl, t, dur, s2=1.12) + pill(s.get("pill"))
        tl.append('tl.fromTo("#cl1",{y:-120,opacity:0},{y:0,opacity:1,duration:0.2,ease:"power4.out"},0.0);')
        tl.append('tl.fromTo("#cl2",{scale:3,opacity:0},{scale:1,opacity:1,duration:0.22,ease:"power4.out"},0.18);')
        tl.append('tl.fromTo("#cl3",{x:900},{x:0,duration:0.2,ease:"power4.out"},0.55);')
        tl.append('tl.fromTo("#cl4",{opacity:0,y:30},{opacity:1,y:0,duration:0.18},0.95);')
        tl.append('tl.fromTo("#clb path",{strokeDashoffset:1},{strokeDashoffset:0,duration:0.3,ease:"power1.inOut"},0.42);')
        sfx += [(0.0, "impact", -8), (0.18, "pop", -4), (0.55, "whoosh_b", -12), (0.47, "ding", -6)]
    elif k in ("pres", "outro"):
        parts = [f'<div class="vcam" id="{sid}vc" style="transform-origin:50% 35%">{vtag("assets/presenter_full.mp4", sid+"v", t, vis, ms=s["ms"], track=5)}</div>']
        if k == "outro":
            parts = ['<div class="outbg"></div>'] + [p.replace('class="vcam"', 'class="vcam" style2') for p in parts]
            parts[1] = parts[1].replace('style2 id', 'id').replace('style="transform-origin:50% 35%"', 'style="transform-origin:50% 30%;top:330px"')
        tl.append(f'tl.fromTo("#{sid}vc",{{scale:1.04}},{{scale:1.17,duration:{vis:.3f},ease:"none"}},{t:.3f});')
        vl = video_layer(sid, z_v, parts, t, vis); mv.append(f"#{vl}"); transparent = True
        inner = '<div class="vign"></div>' + tag_html(s, sid) + stamp_html(s, sid)
        if k == "outro":
            inner += ('<div class="qwrap"><div class="qcard" id="qcard"><div class="qk">CÂU HỎI CHO BẠN</div>'
                      '<div class="qt">AI chơi game mà không cần nhìn — <span class="qy" id="qy">bạn nghĩ sao?</span></div></div></div>')
            tl.append(f'tl.fromTo("#qcard",{{y:-260,opacity:0,rotation:-4}},{{y:0,opacity:1,rotation:-1.5,duration:0.32,ease:"back.out(1.8)"}},{t+0.15:.3f});')
            tl.append(f'tl.fromTo("#qy",{{backgroundSize:"0% 100%"}},{{backgroundSize:"100% 100%",duration:0.5,ease:"power2.out"}},{t+1.2:.3f});')
            sfx += [(t + 0.15, "pop", -5), (t + 1.22, "ding", -8)]
        if not s.get("tr"):
            sfx.append((t, "impact", -11)); s["_cut"] = True
    elif k == "flow":
        nodes = [("GÓI TIN MẠNG", "", ""), ("FILE SQL", " acc", "box"), ("LỆNH HÀNH ĐỘNG", "", "")]
        fl = '<div class="statbg"></div><div class="stripes"></div><div class="flow">'
        for j, (lab, cls, bx) in enumerate(nodes):
            boxs = (f'<svg class="fbox" viewBox="0 0 940 170"><path id="{sid}fb" pathLength="1" d="M10,8 L930,2 L936,162 L6,168 L2,0 L300,6"/></svg>' if bx else "")
            fl += f'<div class="fnode{cls}" id="{sid}f{j}">{lab}{boxs}</div>'
            if j < 2: fl += f'<div class="farr" id="{sid}a{j}">▼</div>'
        fl += '</div>'
        inner = cam(f"{sid}c", fl, t, dur, s2=1.12) + pill(s.get("pill"))
        seq = ["f0", "a0", "f1", "a1", "f2"]
        for j, e in enumerate(seq):
            tl.append(f'tl.fromTo("#{sid}{e}",{{x:{-500 if j%2==0 else 0},opacity:0}},{{x:0,opacity:1,duration:0.2,ease:"power3.out"}},{t+0.16*j:.3f});')
        tl.append(f'tl.fromTo("#{sid}fb",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:0.36,ease:"power1.inOut"}},{t+0.75:.3f});')
        sfx += [(t + 0.0, "pop", -8), (t + 0.32, "pop", -8), (t + 0.64, "pop", -8), (t + 0.8, "ding", -7)]
    elif k == "term":
        lines = [("k", "# module.yaml — agent tự sinh"), ("c", "grpc:"), ("", "  send: Module/Send"), ("", "  poll: Module/Poll"), ("c", "packets:"),
                 ("g", "  SMSG_QUESTGIVER_QUEST_LIST"), ("g", "  SMSG_MONSTER_MOVE"), ("g", "  SMSG_ATTACKSWING_NOTINRANGE"), ("g", "  SMSG_LEARNED_SPELL")]
        tt = '<div class="termbg"></div><div class="term"><div class="termhd"><i></i><i></i><i></i>&nbsp;agent-wow · module</div><div style="height:22px"></div>'
        for j, (c, txt) in enumerate(lines):
            tt += f'<div class="tl {c}" id="{sid}t{j}">{esc(txt)}</div>'
        tt += f'</div><div class="ttitle"><span id="{sid}tt">TỰ VIẾT MODULE TỪ ĐẦU</span></div>'
        inner = cam(f"{sid}c", tt, t, dur, s2=1.12) + pill(s.get("pill"))
        step = min(0.13, (dur - 0.5) / len(lines))
        for j in range(len(lines)):
            tl.append(f'tl.fromTo("#{sid}t{j}",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:{step*1.4:.2f},ease:"steps(10)"}},{t+0.05+step*j:.3f});')
        tl.append(f'tl.fromTo("#{sid}tt",{{x:-900,skewX:-14}},{{x:0,skewX:-8,duration:0.24,ease:"power4.out"}},{t+0.35:.3f});')
        sfx += [(t + 0.35, "pop", -5), (t + 0.05, "marker", -16), (t + 0.5, "marker", -16)]
    # ---- transition in
    tr = s.get("tr"); whip = s.get("whip")
    if i > 0 and not s.get("_cut") and tr:
        frm = {"L": "x:1080", "R": "x:-1080", "U": "y:1920"}[tr]; to = {"L": "x:0", "R": "x:0", "U": "y:0"}[tr]
        blf = ',filter:"blur(14px)"' if whip else ""; blt = ',filter:"blur(0px)"' if whip else ""
        tl.append(f'tl.fromTo("{", ".join(mv)}",{{{frm}{blf}}},{{{to}{blt},duration:0.24,ease:"power3.out"}},{t:.3f});')
        out = {"L": "x:-378", "R": "x:378", "U": "y:-576"}[tr]
        tl.append(f'tl.fromTo("{", ".join(movers[i-1])}",{{x:0,y:0}},{{{out},duration:0.24,ease:"power2.in",immediateRender:false}},{t:.3f});')
        sfx.append((t - 0.08, W_CYCLE[i % 3], -9)); s["trans"] = "whip" if whip else "slide"
    elif i > 0: s["trans"] = "cut"
    else: s["trans"] = "open"
    movers[i] = mv
    cls = "clip shot tshot" if transparent else "clip shot"
    body.append(f'<div class="{cls}" id="{sid}" data-start="{t:.3f}" data-duration="{vis:.3f}" data-track-index="{1 + i % 2}" style="z-index:{z}">{inner}</div>')

# ------------------------------------------------------------------ karaoke (word timings from words.json)
def norm(w): return re.sub(r"[^\wÀ-ỹ'+-]", "", w.lower())
REPL = {1: (["bốn", "mươi"], "40"), 8: (["gpt", "sáu"], "GPT-6"), 12: (["hai", "mươi", "tám"], "28"),
        14: (["c", "cộng", "cộng"], "C++"), 27: (["mười", "sáu", "nghìn"], "16.000")}
by_sent = {}
for wd in words: by_sent.setdefault(wd["sent"], []).append(wd)
toks = []
for si in sorted(by_sent):
    ws = by_sent[si]; j = 0
    seq, disp_r = REPL.get(si, (None, None))
    while j < len(ws):
        if seq and [norm(x["word"]) for x in ws[j:j+len(seq)]] == seq:
            grp = ws[j:j+len(seq)]; raw = grp[-1]["word"]; disp = disp_r; j += len(seq)
        else:
            grp = ws[j:j+1]; raw = disp = grp[0]["word"]; j += 1
        punct = raw[-1] in ",.:;!?"
        toks.append(dict(sent=si, text=disp.rstrip(",.:;!?"), start=grp[0]["start"], end=grp[-1]["end"], brk=punct))
for si, (seq, d) in REPL.items():
    assert any(tk["sent"] == si and tk["text"] == d for tk in toks), ("karaoke merge failed", si, [x["word"] for x in by_sent[si]])
COMP = ["khung hình", "gói tin", "nhiệm vụ", "khởi đầu", "suy luận", "cực cao", "công bố", "di chuyển", "đánh nhau", "tin nhắn", "bản đồ",
        "thế giới", "công cụ", "tìm đường", "thư viện", "tối ưu", "kế hoạch", "thứ tự", "đồ rác", "xịn hơn", "kỹ năng", "valley of trials",
        "sen'jin village", "thí nghiệm", "độc lập", "kiểm chứng", "lách qua", "dòng code", "raid heroic", "màn hình", "lần nào", "gpt-6 astra",
        "file sql", "toàn bộ", "từ đầu", "không phải", "đầu tiên", "chưa ai", "mục tiêu", "nghĩ sao", "chơi game", "câu lệnh", "đúng thứ tự",
        "c++", "agent-wow", "trước khi", "hang cuối", "làm một lần", "server riêng", "lỗi bản đồ", "16.000 dòng", "28 loại"]
COMP = sorted({tuple(c.split()) for c in COMP}, key=len, reverse=True)
clusters = []; st_ = {}
for tk in toks: st_.setdefault(tk["sent"], []).append(tk)
for si in sorted(st_):
    ts = st_[si]; units = []; j = 0
    while j < len(ts):
        for c in COMP:
            n = len(c)
            if tuple(x["text"].lower() for x in ts[j:j+n]) == c and not any(x["brk"] for x in ts[j:j+n-1]):
                units.append(ts[j:j+n]); j += n; break
        else:
            units.append(ts[j:j+1]); j += 1
    cl_s = []; cur = []
    for u in units:
        if cur and len(cur) + len(u) > 3: cl_s.append(cur); cur = []
        cur = cur + u
        if cur[-1]["brk"]: cl_s.append(cur); cur = []
    if cur: cl_s.append(cur)
    kk = 0
    while kk < len(cl_s):
        if len(cl_s[kk]) == 1 and len(cl_s) > 1:
            if kk > 0 and len(cl_s[kk-1]) + 1 <= 4 and not cl_s[kk-1][-1]["brk"]:
                cl_s[kk-1] += cl_s.pop(kk); continue
            if kk + 1 < len(cl_s) and len(cl_s[kk+1]) + 1 <= 4 and not cl_s[kk][-1]["brk"]:
                cl_s[kk+1] = cl_s[kk] + cl_s[kk+1]; cl_s.pop(kk); continue
        kk += 1
    clusters += cl_s
kar = []
for ci, cl in enumerate(clusters):
    stt = cl[0]["start"]; en = clusters[ci + 1][0]["start"] if ci + 1 < len(clusters) else VO_END
    cid = f"k{ci}"
    spans = "".join(f'<span class="kw" id="{cid}w{j}">{esc(tk["text"])}</span>' for j, tk in enumerate(cl))
    kar.append(f'<div class="clip kc" id="{cid}" data-start="{stt:.3f}" data-duration="{en-stt:.3f}" data-track-index="8"><div class="kin" id="{cid}i">{spans}</div></div>')
    tl.append(f'tl.fromTo("#{cid}i",{{scale:0.82,y:14}},{{scale:1,y:0,duration:0.12,ease:"back.out(2.5)"}},{stt:.3f});')
    for j, tk in enumerate(cl):
        tl.append(f'tl.set("#{cid}w{j}",{{color:"#FFD400"}},{tk["start"]:.3f});')
        if j + 1 < len(cl): tl.append(f'tl.set("#{cid}w{j}",{{color:"#FFFFFF"}},{cl[j+1]["start"]:.3f});')
body += kar
body.append(f'<div class="clip blackout" id="blackout" data-start="{VO_END}" data-duration="{TOTAL-VO_END:.3f}" data-track-index="9"></div>')
body.append(f'<audio id="mix" src="assets/mix.wav" data-start="0" data-duration="{TOTAL}" data-track-index="10" data-volume="1"></audio>')

# hook background: Tom's Hardware article hero (WoW screenshot, credit Blizzard) blurred
im = Image.open(SRC / "toms_hero_wow.png").convert("RGB")
sc = 1920 / im.height; im = im.resize((round(im.width * sc), 1920)); x0 = (im.width - 1080) // 2 + 260
im = im.crop((x0, 0, x0 + 1080, 1920))
im = ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(7))).enhance(0.38)
im.save(AS / "claim_bg.jpg", quality=85)

css = (LV / "hf_style.css").read_text()
doc = f'''<!doctype html>
<html lang="vi"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=1080, height=1920"/>
<title>HM-103 v1.1</title>
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
meta = dict(total=TOTAL, vo_end=VO_END,
            shots=[{kk: v for kk, v in s.items() if kk in ("i", "k", "t", "end", "dur", "trans", "src", "vid", "pill", "panels", "tag", "stamp", "num", "label")} for s in SHOTS],
            sfx=sorted(sfx), clusters=[[{"text": x["text"], "start": x["start"], "end": x["end"]} for x in c] for c in clusters])
(LV / "plan.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1, default=str))
print("shots", len(SHOTS), "clusters", len(clusters), "sfx", len(sfx), "VO_END", VO_END, "TOTAL", TOTAL)
print("trans:", {x: sum(1 for s in SHOTS if s.get("trans") == x) for x in ("slide", "whip", "cut", "open")})
print("short shots:", [(s["i"], s["dur"]) for s in SHOTS if s["dur"] < 0.9])
