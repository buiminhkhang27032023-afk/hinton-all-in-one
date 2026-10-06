#!/usr/bin/env python3
"""MAP-FOOD-HCM-01 v3 — polished HyperFrames map composition (visuals only; reuse voice timings)."""
from __future__ import annotations
import json, shutil
from pathlib import Path

T = Path(__file__).resolve().parent
JOB = T.parent
OUT_VOICE = JOB / "voice"
idx = json.loads((T / "places-index.json").read_text(encoding="utf-8"))
timings = json.loads((OUT_VOICE / "timings.json").read_text(encoding="utf-8"))
sents = timings["sentences"]
total_vo = float(timings["total"])
DURATION = round(total_vo + 2.0, 3)

shutil.copy2(OUT_VOICE / "voice_storytelling.wav", T / "assets" / "voice.wav")

P = idx["places"]
MAP = idx["map"]
MW, MH = MAP["w"], MAP["h"]

# Food emoji fallbacks (Noto Color Emoji) + SVG
FOOD_EMOJI = {
    "banh-xeo-46a": "🥞",
    "com-tam-ba-ghien": "🍚",
    "banh-mi-huynh-hoa": "🥖",
    "oc-dao": "🐚",
    "pho-hoa-pasteur": "🍜",
}
SCREEN = {
    "banh-xeo-46a": {"praise": "👍 Giòn, khổng lồ", "critique": "👎 Hơi dầu, nước chấm loãng"},
    "com-tam-ba-ghien": {"praise": "👍 Sườn đậm vị", "critique": "👎 Sườn khô, giá cao hơn quanh khu"},
    "banh-mi-huynh-hoa": {"praise": "👍 Ổ lớn, nhân dày", "critique": "👎 Giá cao, “overrated”"},
    "oc-dao": {"praise": "👍 Hải sản tươi", "critique": "👎 Đến muộn hết món, chờ lâu", "must": "Ốc hương sốt trứng muối"},
    "pho-hoa-pasteur": {"praise": "👍 Nước dùng vừa miệng, thịt mềm", "critique": "👎 Thịt đặc biệt nhiều mỡ/dai"},
}

SCENES = [
    {"id": "hook", "lo": 0, "hi": 0, "place": None, "zoom": 1.15, "mode": "hook",
     "cam": (P["cho-ben-thanh"]["px"], P["cho-ben-thanh"]["py"])},
    {"id": "countdown", "lo": 1, "hi": 1, "place": None, "zoom": 1.35, "mode": "countdown",
     "cam": (P["cho-ben-thanh"]["px"], P["cho-ben-thanh"]["py"])},
    {"id": "r5_intro", "lo": 2, "hi": 3, "place": "banh-xeo-46a", "zoom": 2.35, "mode": "reveal", "bib": True},
    {"id": "r5_stats", "lo": 4, "hi": 6, "place": "banh-xeo-46a", "zoom": 2.45, "mode": "stats", "bib": True, "price": True},
    {"id": "r4_intro", "lo": 7, "hi": 8, "place": "com-tam-ba-ghien", "zoom": 1.55, "mode": "reveal", "bib": True},
    {"id": "r4_stats", "lo": 9, "hi": 10, "place": "com-tam-ba-ghien", "zoom": 1.6, "mode": "stats", "bib": True},
    {"id": "r3_intro", "lo": 11, "hi": 12, "place": "banh-mi-huynh-hoa", "zoom": 2.3, "mode": "reveal"},
    {"id": "r3_stats", "lo": 13, "hi": 14, "place": "banh-mi-huynh-hoa", "zoom": 2.4, "mode": "stats", "most_reviews": True},
    {"id": "r2_intro", "lo": 15, "hi": 17, "place": "oc-dao", "zoom": 2.3, "mode": "reveal"},
    {"id": "r2_stats", "lo": 18, "hi": 19, "place": "oc-dao", "zoom": 2.35, "mode": "stats"},
    {"id": "r1_intro", "lo": 20, "hi": 21, "place": "pho-hoa-pasteur", "zoom": 2.5, "mode": "reveal", "gold": True},
    {"id": "r1_stats", "lo": 22, "hi": 24, "place": "pho-hoa-pasteur", "zoom": 2.55, "mode": "stats", "price": True, "gold": True},
    {"id": "cta", "lo": 25, "hi": 26, "place": None, "zoom": 1.05, "mode": "cta",
     "cam": (1300, 1200)},
]
for sc in SCENES:
    sc["start"] = sents[sc["lo"]]["start"]
    sc["end"] = sents[sc["hi"]]["end"]
    sc["dur"] = round(sc["end"] - sc["start"], 3)

# --- Pins with edge-aware labels ---
pins_html = []
for pid, p in P.items():
    kind = p["type"] if p["type"] in ("hotel", "landmark") else "restaurant"
    src = {"hotel": "assets/pins/hotel.svg", "landmark": "assets/pins/landmark.svg"}.get(kind, "assets/pins/restaurant.svg")
    if p.get("rank") == 1:
        src = "assets/pins/restaurant-gold.svg"
    # label side: flip if near mosaic left/right edges
    # edge-aware + manual overrides for crowded Dist1 hotels
    side = "right" if p["px"] < MW * 0.22 else ("left" if p["px"] > MW * 0.78 else "top")
    if pid == "ks-rex":
        side = "left"
    elif pid == "ks-caravelle":
        side = "right"
    elif pid == "nha-tho-duc-ba":
        side = "top"
    elif pid == "cho-ben-thanh":
        side = "left"
    if p.get("rank"):
        label_txt = f'#{p["rank"]}'
    elif kind != "restaurant":
        label_txt = (p["name"].replace("Khách sạn ", "KS ")
                     .replace("Nhà thờ Đức Bà Sài Gòn", "Đức Bà")
                     .replace("Chợ Bến Thành", "Bến Thành")
                     .replace("Caravelle Hotel", "Caravelle")
                     .replace("KS Rex Sài Gòn", "KS Rex"))
    else:
        label_txt = ""
    label = f'<div class="label side-{side}">{label_txt}</div>' if label_txt else ""
    food_float = ""
    if p.get("food_icon"):
        if pid == "banh-xeo-46a":
            food_float = (f'<img class="food-float" id="foodfloat-{pid}" src="assets/food/banh-xeo.svg" alt="banh xeo"/>')
        else:
            food_float = (f'<span class="food-emoji" id="foodemoji-{pid}" aria-hidden="true">{FOOD_EMOJI.get(pid,"")}</span>')
    pins_html.append(
        f'<div class="pin {kind}" id="pin-{pid}" data-place="{pid}" style="left:{p["px"]}px;top:{p["py"]}px">'
        f'{label}<img class="pin-img" src="{src}" alt=""/><span class="pin-emoji" aria-hidden="true">{"🍽️" if kind=="restaurant" else ("🏨" if kind=="hotel" else "🏛️")}</span>{food_float}</div>'
    )

route_pts = " ".join(f'{r["px"]},{r["py"]}' for r in idx["route"])
route_svg = f'''<svg id="routeSvg" viewBox="0 0 {MW} {MH}" width="{MW}" height="{MH}"
  style="position:absolute;left:0;top:0;pointer-events:none;opacity:0">
  <polyline id="routeLine" points="{route_pts}" fill="none" stroke="#F5C518" stroke-width="10"
    stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="18 14" opacity="0.85"/>
</svg>'''

star_svg = '<svg viewBox="0 0 24 24" width="44" height="44"><path fill="CUR" d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.9L12 17.8 5.8 21.1 7 14.2 2 9.3l6.9-1z"/></svg>'
empty_stars = "".join(star_svg.replace("CUR", "#4a4a4a") for _ in range(5))
gold_stars = "".join(star_svg.replace("CUR", "#F5C518") for _ in range(5))

def card_html(pid):
    p = P[pid]
    rank = p["rank"]
    food = p["food_icon"]
    emoji = FOOD_EMOJI.get(pid, "")
    bib = f'<img class="bib" id="bib-{pid}" src="assets/badges/bib-gourmand.svg" alt="Bib Gourmand"/>' if p.get("bib_gourmand") else ""
    price = f'<div class="price" id="price-{pid}">💵 {p["price_screen"]}</div>' if p.get("price_screen") else ""
    scr = SCREEN.get(pid, {})
    must = f'<div class="must">{scr["must"]}</div>' if scr.get("must") else ""
    most = f'<div class="most" id="most-{pid}">🏆 Nhiều review nhất top 5</div>' if pid == "banh-mi-huynh-hoa" else ""
    if pid == "banh-xeo-46a":
        food_visual = f'<img class="food-crepe-lg" src="assets/food/banh-xeo.svg" alt="banh xeo"/>'
    else:
        food_visual = f'<div class="food-emoji-lg" aria-hidden="true">{emoji}</div>'
    return f'''
    <div class="card glass title-card" id="card-{pid}">
      <div class="card-left">
        <img class="rank-badge" src="assets/badges/rank-{rank}.svg" alt="#{rank}"/>
        {food_visual}
      </div>
      <div class="title-text">
        <h1>#{rank} {p["name"].upper()}</h1>
        <div class="sub">{p.get("district") or ""}</div>
        {must}
        <div class="rating-block" id="ratingblock-{pid}">
          <div class="starwrap"><div class="empty">{empty_stars}</div><div class="gold" id="gold-{pid}">{gold_stars}</div></div>
          <div class="reviews">⭐ <span class="hi" id="rating-{pid}">0.0</span>
            · khoảng <span class="hi" id="reviews-{pid}">0</span> review</div>
        </div>
        {most}
        <div class="pros" id="pros-{pid}">{scr.get("praise","")}</div>
        <div class="cons" id="cons-{pid}">{scr.get("critique","")}</div>
        {price}
        {bib}
      </div>
    </div>'''

cards = "\n".join(
    f'<div class="safe-card clip place-card" id="ui-{pid}" style="opacity:0">'
    f'<svg class="connector" id="conn-{pid}" viewBox="0 0 1080 400" preserveAspectRatio="none">'
    f'<line x1="540" y1="8" x2="540" y2="118" stroke="#F5C518" stroke-width="4" stroke-dasharray="10 7" opacity="0.9"/>'
    f'</svg>{card_html(pid)}</div>'
    for pid in idx["top5_order"]
)

# SFX
sfx_cues = []
def add_sfx(src, start, vol=0.55, dur=0.4):
    add_sfx.n = getattr(add_sfx, "n", 0) + 1
    sfx_cues.append(
        f'<audio id="sfx{add_sfx.n}" src="assets/sfx/{src}" data-start="{start:.3f}" '
        f'data-duration="{dur}" data-track-index="8" data-volume="{vol}"></audio>'
    )
add_sfx("whoosh.wav", SCENES[0]["start"] + 0.05, 0.5, 0.45)
for i in range(4):
    add_sfx("pop.wav", SCENES[0]["start"] + 0.35 + i * 0.28, 0.75, 0.1)
add_sfx("tick.wav", SCENES[1]["start"], 0.5, 0.05)
for sc in SCENES:
    if sc["mode"] == "reveal":
        add_sfx("whoosh-short.wav", sc["start"], 0.55, 0.25)
        add_sfx("pop.wav", sc["start"] + 0.4, 0.9, 0.1)
        if sc.get("bib"):
            add_sfx("ding.wav", sc["start"] + 0.85, 0.55, 0.35)
    if sc["mode"] == "stats":
        add_sfx("ding.wav", sc["start"] + 0.1, 0.45, 0.3)
    if sc["id"] == "r1_intro":
        add_sfx("impact.wav", sc["start"], 0.7, 0.4)
for i, pid in enumerate(idx["top5_order"]):
    add_sfx("pop.wav", SCENES[-1]["start"] + 0.35 + i * 0.12, 0.7, 0.1)

css = f'''
@font-face{{font-family:'BeVietnam';src:url('assets/fonts/BeVietnamPro-Regular.ttf');font-weight:400}}
@font-face{{font-family:'BeVietnam';src:url('assets/fonts/BeVietnamPro-Medium.ttf');font-weight:500}}
@font-face{{font-family:'BeVietnam';src:url('assets/fonts/BeVietnamPro-SemiBold.ttf');font-weight:600}}
@font-face{{font-family:'BeVietnam';src:url('assets/fonts/BeVietnamPro-Bold.ttf');font-weight:700}}
@font-face{{font-family:'BeVietnam';src:url('assets/fonts/BeVietnamPro-ExtraBold.ttf');font-weight:800}}
@font-face{{font-family:'BeVietnam';src:url('assets/fonts/BeVietnamPro-Black.ttf');font-weight:900}}
@font-face{{font-family:'NotoColorEmoji';src:url('assets/fonts/NotoColorEmoji.ttf');font-weight:400}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#0a0c10;
  font-family:'BeVietnam','NotoColorEmoji',system-ui,sans-serif}}
#root{{width:1080px;height:1920px;position:relative;overflow:hidden;background:#0a0c10}}
#mapStage{{position:absolute;inset:0;overflow:hidden}}
#mapWorld{{position:absolute;left:0;top:0;width:{MW}px;height:{MH}px;transform-origin:0 0;will-change:transform}}
#mapWorld img.map{{width:100%;height:100%;display:block;filter:brightness(.94) contrast(1.1) saturate(1.08)}}
.pin{{position:absolute;width:96px;height:120px;margin-left:-48px;margin-top:-120px;transform-origin:50% 100%;opacity:0;z-index:3}}
.pin .pin-img{{width:100%;height:100%;display:block;filter:drop-shadow(0 8px 12px rgba(0,0,0,.55))}}
.pin-emoji{{position:absolute;left:50%;top:28%;transform:translate(-50%,-50%);font-size:34px;line-height:1;font-family:'NotoColorEmoji',sans-serif;pointer-events:none;filter:drop-shadow(0 2px 4px rgba(0,0,0,.5))}}
.pin.landmark,.pin.hotel{{width:78px;height:98px;margin-left:-39px;margin-top:-98px}}
.pin .label{{position:absolute;background:rgba(0,0,0,.88);color:#fff;font-size:22px;font-weight:800;
  padding:6px 14px;border-radius:12px;white-space:nowrap;border:1.5px solid rgba(245,197,24,.45);
  box-shadow:0 4px 14px rgba(0,0,0,.4);pointer-events:none}}
.pin .label.side-top{{left:50%;bottom:100%;transform:translate(-50%,-8px)}}
.pin .label.side-left{{right:100%;top:8px;transform:translate(-8px,0)}}
.pin .label.side-right{{left:100%;top:8px;transform:translate(8px,0)}}
.pin .food-float{{position:absolute;left:70px;top:-30px;width:110px;height:110px;opacity:0;
  filter:drop-shadow(0 6px 10px rgba(0,0,0,.5))}}
.pin .food-emoji{{position:absolute;left:70px;top:-40px;font-size:110px;opacity:0;line-height:1;
  font-family:'NotoColorEmoji',sans-serif;filter:drop-shadow(0 6px 12px rgba(0,0,0,.55))}}
.glow{{position:absolute;width:180px;height:180px;margin-left:-90px;margin-top:-90px;border-radius:50%;
  background:radial-gradient(circle,rgba(245,197,24,.55),transparent 70%);opacity:0;pointer-events:none;z-index:2}}
.ui{{position:absolute;inset:0;pointer-events:none;z-index:20}}
/* TikTok safe: top 150, bottom 380, right 140 */
.safe-top{{position:absolute;top:160px;left:40px;right:150px}}
.safe-card{{position:absolute;top:1080px;left:32px;right:150px;bottom:160px}}
.connector{{position:absolute;left:0;right:0;top:-100px;height:100px;width:100%;overflow:visible}}
.glass{{background:rgba(10,12,18,.78);border:2.5px solid rgba(245,197,24,.65);border-radius:28px;
  padding:28px 30px;box-shadow:0 18px 50px rgba(0,0,0,.6), inset 0 1px 0 rgba(255,255,255,.08);
  backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px)}}
.title-card{{display:flex;align-items:flex-start;gap:20px}}
.card-left{{display:flex;flex-direction:column;align-items:center;gap:10px;flex:0 0 auto}}
.rank-badge{{width:110px;height:110px;filter:drop-shadow(0 6px 10px rgba(0,0,0,.45))}}
.food-emoji-lg{{font-size:140px;line-height:1;font-family:'NotoColorEmoji',sans-serif;text-align:center;
  filter:drop-shadow(0 8px 14px rgba(0,0,0,.5));margin-top:4px}}
.food-crepe-lg{{width:200px;height:200px;filter:drop-shadow(0 8px 14px rgba(0,0,0,.5));margin-top:4px}}
.pin .food-float{{position:absolute;left:64px;top:-50px;width:130px;height:130px;opacity:0;
  filter:drop-shadow(0 6px 12px rgba(0,0,0,.55))}}
.title-text{{flex:1;min-width:0}}
.title-text h1{{font-size:64px;font-weight:900;color:#fff;line-height:1.12;letter-spacing:-0.02em;
  text-shadow:0 3px 12px rgba(0,0,0,.5)}}
.title-text .sub{{font-size:36px;font-weight:700;color:#F5C518;margin-top:6px}}
.must{{font-size:34px;font-weight:800;color:#fff;margin-top:8px}}
.rating-block{{margin-top:10px;opacity:0;max-height:0;overflow:hidden;margin-top:0}}
.starwrap{{position:relative;width:248px;height:44px;margin:8px 0 8px}}
.starwrap .empty,.starwrap .gold{{position:absolute;left:0;top:0;display:flex;gap:6px}}
.starwrap .gold{{overflow:hidden;width:0}}
.reviews{{font-size:36px;font-weight:800;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.4);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}}
.reviews .hi{{color:#F5C518}}
.pros,.cons{{font-size:34px;font-weight:700;margin-top:10px;color:#e8e8e8;opacity:0}}
.cons{{color:#ff9a9a}}
.price{{font-size:36px;font-weight:800;color:#F5C518;margin-top:12px;opacity:0}}
.most{{font-size:34px;font-weight:800;color:#F5C518;margin-top:8px;opacity:0}}
.bib{{width:300px;margin-top:14px;opacity:0;filter:drop-shadow(0 4px 8px rgba(0,0,0,.4))}}
.hook-card h1{{font-size:90px;font-weight:900;color:#fff;line-height:1.15;text-align:center;
  text-shadow:0 4px 20px rgba(0,0,0,.65)}}
.hook-card em{{color:#F5C518;font-style:normal}}
.hook-foods{{display:flex;justify-content:center;gap:16px;margin-top:22px}}
.hook-food{{width:120px;height:120px;opacity:0;filter:drop-shadow(0 8px 14px rgba(0,0,0,.55))}}
.countdown{{text-align:center;font-size:64px;font-weight:900;color:#F5C518;
  text-shadow:0 4px 16px rgba(0,0,0,.5)}}
.cta-card{{text-align:center}}
.cta-card h1{{font-size:72px;font-weight:900;color:#fff;text-shadow:0 4px 16px rgba(0,0,0,.5)}}
.cta-card .brand{{font-size:42px;font-weight:800;color:#F5C518;margin-top:14px}}
.cta-card .subcta{{margin-top:10px;font-size:32px;font-weight:700;color:#ccc}}
.recap-row{{display:flex;justify-content:center;gap:18px;margin-top:22px;flex-wrap:wrap}}
.recap-item{{display:flex;flex-direction:column;align-items:center;gap:4px}}
.recap-item img{{width:88px;height:88px;filter:drop-shadow(0 4px 8px rgba(0,0,0,.45))}}
.recap-item .rk{{font-size:28px;font-weight:900;color:#F5C518}}
.footer{{position:absolute;left:20px;right:20px;bottom:28px;display:flex;justify-content:space-between;
  align-items:center;gap:10px;z-index:50;pointer-events:none}}
.disclaimer{{font-size:18px;font-weight:700;color:rgba(255,255,255,.85);background:rgba(0,0,0,.72);
  padding:7px 12px;border-radius:10px;max-width:700px;font-family:'BeVietnam',sans-serif;
  box-shadow:0 2px 10px rgba(0,0,0,.4)}}
.attr{{font-size:15px;font-weight:700;color:rgba(255,255,255,.7);text-align:right;max-width:280px;
  background:rgba(0,0,0,.55);padding:6px 10px;border-radius:8px}}
.vignette{{position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(ellipse at center,transparent 38%,rgba(0,0,0,.55) 100%);z-index:5}}
'''

# --- GSAP ---
js = []
js.append(f"const W=1080,H=1920,PIN_Y=H*0.40,PLACES={json.dumps({k:{'px':v['px'],'py':v['py'],'rating':v.get('rating'),'reviews':v.get('reviews')} for k,v in P.items()}, ensure_ascii=False)};")
js.append("const cam=(px,py,s,fy=PIN_Y)=>({x:W/2-px*s,y:fy-py*s,scale:s});")
js.append("const EASE='power3.inOut';")
js.append("const tl=gsap.timeline({paused:true});")
js.append('const overview=cam(PLACES["cho-ben-thanh"].px,PLACES["cho-ben-thanh"].py,1.15);')
js.append("gsap.set('#mapWorld', overview);")
js.append("gsap.set('.pin', {opacity:0, scale:0});")
js.append("gsap.set('.place-card', {opacity:0, y:40, scale:0.92});")
js.append("gsap.set('.glow', {opacity:0});")
js.append("gsap.set('#routeSvg', {opacity:0});")
js.append("gsap.set('#hookUi', {opacity:0, y:20});")
js.append("gsap.set('#countUi', {opacity:0});")
js.append("gsap.set('#ctaUi', {opacity:0, y:30});")
js.append("gsap.set('.food-emoji,.food-float', {opacity:0, scale:0});")
js.append("gsap.set('.rating-block', {opacity:0});")
js.append("gsap.set('.pros,.cons,.price,.most,.bib', {opacity:0});")

def fly_to(pid, zoom, t0, dur, fy="PIN_Y"):
    p = P[pid]
    js.append(
        f"tl.to('#mapWorld',{{x:cam({p['px']},{p['py']},{zoom},{fy}).x,"
        f"y:cam({p['px']},{p['py']},{zoom},{fy}).y,scale:{zoom},"
        f"duration:{dur},ease:EASE}},{t0});"
    )
def fly_cam(px, py, zoom, t0, dur, fy="PIN_Y"):
    js.append(
        f"tl.to('#mapWorld',{{x:cam({px},{py},{zoom},{fy}).x,"
        f"y:cam({px},{py},{zoom},{fy}).y,scale:{zoom},"
        f"duration:{dur},ease:EASE}},{t0});"
    )
def drop_pin(pid, t0):
    js.append(f"tl.to('#pin-{pid}',{{opacity:1,scale:1,duration:0.4,ease:'back.out(2.8)'}},{t0});")
def pop_food(pid, t0):
    js.append(f"tl.to('#foodemoji-{pid},#foodfloat-{pid}',{{opacity:1,scale:1,duration:0.4,ease:'back.out(3)'}},{t0});")
def show_card(pid, t0):
    js.append(f"tl.to('#ui-{pid}',{{opacity:1,y:0,scale:1,duration:0.4,ease:'back.out(1.5)'}},{t0});")
def hide_card(pid, t0):
    js.append(f"tl.to('#ui-{pid}',{{opacity:0,y:24,duration:0.25}},{t0});")
def fill_stars(pid, rating, reviews, t0):
    w = round(248 * (rating / 5), 1)
    js.append(f"tl.to('#ratingblock-{pid}',{{opacity:1,maxHeight:220,marginTop:10,duration:0.25}},{t0});")
    js.append(f"tl.to('#gold-{pid}',{{width:{w},duration:0.9,ease:'power2.out'}},{t0});")
    js.append(
        f"{{const ro={{v:0}},rv={{v:0}};"
        f"tl.to(ro,{{v:{rating},duration:0.8,ease:'power1.out',onUpdate:()=>{{"
        f"const e=document.getElementById('rating-{pid}');if(e)e.textContent=ro.v.toFixed(1);}}}},{t0});"
        f"tl.to(rv,{{v:{reviews},duration:1.05,ease:'power1.out',onUpdate:()=>{{"
        f"const e=document.getElementById('reviews-{pid}');"
        f"if(e)e.textContent=Math.round(rv.v).toLocaleString('vi-VN');}}}},{t0});}}"
    )

# HOOK — closer Dist1, landmark pops, food icons fly in
sc = SCENES[0]
js.append(f"tl.to('#hookUi',{{opacity:1,y:0,duration:0.4,ease:'power2.out'}},{sc['start']});")
js.append("gsap.set('.hook-food',{opacity:0,scale:0});")
for i in range(5):
    js.append(f"tl.to('#hookfood-{i}',{{opacity:1,scale:1,duration:0.35,ease:'back.out(2.8)'}},{sc['start']+0.25+i*0.12});")
for i, pid in enumerate(idx["landmarks"]):
    js.append(f"tl.to('#pin-{pid}',{{opacity:1,scale:1.15,duration:0.35,ease:'back.out(2.5)'}},{sc['start']+0.3+i*0.22});")
# ghost restaurant pins + food icons pop
for i, pid in enumerate(idx["top5_order"]):
    t0 = sc["start"] + 0.25 + i * 0.18
    js.append(f"tl.to('#pin-{pid}',{{opacity:0.7,scale:0.9,duration:0.3,ease:'back.out(2)'}},{t0});")
    pop_food(pid, t0 + 0.08)
js.append(f"tl.to('#hookUi',{{opacity:0,y:-16,duration:0.25}},{sc['end']-0.12});")

# COUNTDOWN
sc = SCENES[1]
fly_cam(sc["cam"][0], sc["cam"][1], sc["zoom"], sc["start"], min(0.7, sc["dur"]))
js.append(f"tl.to('#countUi',{{opacity:1,duration:0.25}},{sc['start']});")
js.append(f"tl.to('#countUi',{{opacity:0,duration:0.15}},{sc['end']-0.05});")

prev = None
for sc in SCENES[2:]:
    if sc["mode"] in ("reveal", "stats"):
        pid = sc["place"]
        if sc["mode"] == "reveal":
            if prev and prev != pid:
                hide_card(prev, max(sc["start"] - 0.08, 0))
                js.append(f"tl.to('#glow-{prev}',{{opacity:0,duration:0.2}},{sc['start']});")
                # hide previous food float a bit
                js.append(f"tl.to('#foodemoji-{prev},#foodfloat-{prev}',{{opacity:0.55,duration:0.2}},{sc['start']});")
            fly_dur = min(1.4, max(0.75, sc["dur"] * 0.48))
            fly_to(pid, sc["zoom"], sc["start"], fly_dur)
            drop_pin(pid, sc["start"] + fly_dur * 0.72)
            pop_food(pid, sc["start"] + fly_dur * 0.78)
            js.append(f"tl.to('#glow-{pid}',{{opacity:1,duration:0.3}},{sc['start']+fly_dur*0.72});")
            show_card(pid, sc["start"] + fly_dur * 0.82)
            # DO NOT show rating yet on intro
            if sc.get("bib"):
                js.append(f"tl.to('#bib-{pid}',{{opacity:1,duration:0.35}},{sc['start']+fly_dur*0.82+0.3});")
            js.append(f"tl.to('#routeSvg',{{opacity:0.85,duration:0.35}},{sc['start']});")
            prev = pid
        else:
            fly_to(pid, sc["zoom"], sc["start"], 0.45)
            fill_stars(pid, P[pid]["rating"], P[pid]["reviews"], sc["start"] + 0.08)
            if sc.get("bib"):
                js.append(f"tl.to('#bib-{pid}',{{opacity:1,duration:0.3}},{sc['start']+0.15});")
            js.append(f"tl.to('#pros-{pid}',{{opacity:1,duration:0.25}},{sc['start']+0.35});")
            js.append(f"tl.to('#cons-{pid}',{{opacity:1,duration:0.25}},{sc['start']+0.6});")
            if sc.get("price"):
                js.append(f"tl.to('#price-{pid}',{{opacity:1,duration:0.25}},{sc['start']+0.85});")
            if sc.get("most_reviews"):
                js.append(f"tl.to('#most-{pid}',{{opacity:1,scale:1,duration:0.3,ease:'back.out(2)'}},{sc['start']+0.4});")
            prev = pid
    elif sc["mode"] == "cta":
        if prev:
            hide_card(prev, sc["start"] - 0.05)
            js.append(f"tl.to('#glow-{prev}',{{opacity:0,duration:0.2}},{sc['start']});")
        fly_cam(sc["cam"][0], sc["cam"][1], sc["zoom"], sc["start"], 1.1, "H*0.42")
        for i, pid in enumerate(idx["top5_order"]):
            drop_pin(pid, sc["start"] + 0.35 + i * 0.1)
            pop_food(pid, sc["start"] + 0.4 + i * 0.1)
            js.append(f"tl.to('#pin-{pid}',{{scale:1.2,duration:0.25}},{sc['start']+0.5+i*0.08});")
        for pid in idx["landmarks"]:
            js.append(f"tl.to('#pin-{pid}',{{opacity:0.9,scale:1.1,duration:0.25}},{sc['start']+0.55});")
        js.append(f"tl.to('#routeSvg',{{opacity:0.95,duration:0.3}},{sc['start']+0.3});")
        js.append(f"tl.to('#ctaUi',{{opacity:1,y:0,duration:0.4,ease:'back.out(1.4)'}},{sc['start']+0.25});")

js.append(f"tl.to('#mapWorld',{{scale:'+=0.06',duration:2.0,ease:'sine.inOut'}},{SCENES[-1]['end']});")
js.append("window.__timelines=window.__timelines||{}; window.__timelines['main']=tl;")

glows = "\n".join(
    f'<div class="glow" id="glow-{pid}" style="left:{P[pid]["px"]}px;top:{P[pid]["py"]}px"></div>'
    for pid in idx["top5_order"]
)

recap = "".join(
    f'<div class="recap-item"><img src="assets/food/{P[pid]["food_icon"]}.svg"/><div class="rk">#{P[pid]["rank"]}</div></div>'
    for pid in idx["top5_order"]
)

html = f'''<!doctype html>
<html lang="vi">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=1080, height=1920"/>
<title>MAP-FOOD-HCM-01 v3</title>
<script src="assets/gsap.min.js"></script>
<style>{css}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DURATION}"
     data-width="1080" data-height="1920" data-fps="30">
  <div id="mapStage" class="clip" data-start="0" data-duration="{DURATION}" data-track-index="0">
    <div id="mapWorld">
      <img class="map" src="assets/map/saigon-dark-z16.png" alt="map"/>
      {route_svg}
      {glows}
      {''.join(pins_html)}
    </div>
  </div>
  <div class="vignette"></div>
  <div class="ui">
    <div class="safe-top clip" id="hookUi" data-start="{SCENES[0]['start']}" data-duration="{SCENES[0]['dur']}" data-track-index="2">
      <div class="glass hook-card"><h1>QUÁN NÀO SÀI GÒN<br>ĐƯỢC GOOGLE<br><em>CHẤM CAO NHẤT?</em></h1></div>
      <div class="hook-foods" id="hookFoods"><img class="hook-food" id="hookfood-0" src="assets/food/banh-xeo.svg" alt=""/><img class="hook-food" id="hookfood-1" src="assets/food/com-tam.svg" alt=""/><img class="hook-food" id="hookfood-2" src="assets/food/banh-mi.svg" alt=""/><img class="hook-food" id="hookfood-3" src="assets/food/oc.svg" alt=""/><img class="hook-food" id="hookfood-4" src="assets/food/pho.svg" alt=""/></div>
    </div>
    <div class="safe-top clip" id="countUi" data-start="{SCENES[1]['start']}" data-duration="{SCENES[1]['dur']}" data-track-index="2">
      <div class="glass"><div class="countdown">TOP 5 · ĐẾM NGƯỢC</div></div>
    </div>
    {cards}
    <div class="safe-card clip" id="ctaUi" data-start="{SCENES[-1]['start']}" data-duration="{round(DURATION-SCENES[-1]['start'],3)}" data-track-index="2">
      <div class="glass cta-card">
        <h1>BẠN CHỌN QUÁN NÀO? 👇</h1>
        <div class="brand">Hinton Media</div>
        <div class="subcta">Theo dõi để xem bản đồ tiếp theo</div>
        <div class="recap-row">{recap}</div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div class="disclaimer">Số liệu Google Maps tham khảo, 10/2026</div>
    <div class="attr">Tiles © Esri</div>
  </div>
  <audio id="vo" src="assets/voice.wav" data-start="0" data-duration="{total_vo}" data-track-index="9" data-volume="0.9"></audio>
  {''.join(sfx_cues)}
</div>
<script>
{chr(10).join(js)}
</script>
</body>
</html>
'''
(T / "full.html").write_text(html, encoding="utf-8")
(T / "index.html").write_text(html, encoding="utf-8")
meta = {"duration": DURATION, "vo": total_vo, "version": "v4",
        "scenes": [{k: sc[k] for k in ("id", "start", "end", "dur", "place", "mode") if k in sc} for sc in SCENES]}
(T / "full-meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print("Wrote full.html v4 duration=", DURATION, "bytes=", len(html))
