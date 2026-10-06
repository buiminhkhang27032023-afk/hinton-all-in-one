#!/usr/bin/env python3
"""MAP-FOOD-HP-01 — N-stop food-tour HyperFrames builder (data-driven)."""
from __future__ import annotations
import json, math, argparse, shutil
from pathlib import Path

T = Path(__file__).resolve().parent
JOB = T.parent
VOICE = JOB / "voice"
CFG_PATH = T / "route-config.json"


def latlng_to_pixel(lat, lng, meta):
    z = meta["z"]; n = 2 ** z
    x = (lng + 180.0) / 360.0 * n
    lat_rad = math.radians(lat)
    y = (1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi) / 2.0 * n
    return round((x - meta["tx0"]) * meta["tile_size"], 2), round((y - meta["ty0"]) * meta["tile_size"], 2)


def load_all():
    cfg = json.loads(CFG_PATH.read_text(encoding="utf-8"))
    meta = json.loads((T / cfg["map"]["meta"]).read_text(encoding="utf-8"))
    timings = None
    tp = VOICE / "timings.json"
    if tp.exists():
        timings = json.loads(tp.read_text(encoding="utf-8"))
    return cfg, meta, timings


def enrich(cfg, meta):
    MW, MH = meta["mosaic_w"], meta["mosaic_h"]
    places = {}
    for lm in cfg["landmarks"]:
        px, py = latlng_to_pixel(lm["lat"], lm["lng"], meta)
        places[lm["id"]] = {**lm, "px": px, "py": py}
    stops = []
    for s in cfg["stops"]:
        px, py = latlng_to_pixel(s["lat"], s["lng"], meta)
        row = {**s, "px": px, "py": py, "type": "stop"}
        stops.append(row)
        places[s["id"]] = row
    route = [{"id": s["id"], "px": s["px"], "py": s["py"], "diem": s["diem"]} for s in stops]
    index = {
        "map": {"w": MW, "h": MH, **{k: meta[k] for k in ("z", "tx0", "ty0", "tile_size", "attribution")}},
        "places": places, "stops": stops, "route": route, "N": len(stops),
    }
    (T / "places-index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    return index


def fmt_reviews(n):
    # Vietnamese thousand dots
    return f"{n:,}".replace(",", ".")


def star_svgs(fill="#4a4a4a", n=5, size=48):
    path = "M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.9L12 17.8 5.8 21.1 7 14.2 2 9.3l6.9-1z"
    return "".join(f'<svg viewBox="0 0 24 24" width="{size}" height="{size}"><path fill="{fill}" d="{path}"/></svg>' for _ in range(n))


def build_scenes(cfg, index, timings):
    """Map 10 VO paragraphs → scenes; fallback equal split if no timings."""
    N = index["N"]
    stops = index["stops"]
    if timings and timings.get("sentences"):
        sents = timings["sentences"]
        total = float(timings["total"])
        # Expected: 0 hook, 1 intro, 2..8 stops, 9 cta  (10 paras)
        scenes = []
        def span(i):
            if i < len(sents):
                return sents[i]["start"], sents[i]["end"]
            return total, total
        # hook = sent 0
        a,b = span(0)
        scenes.append({"id":"hook","start":a,"end":b,"mode":"hook"})
        # intro landmarks = sent 1
        a,b = span(1)
        scenes.append({"id":"intro","start":a,"end":b,"mode":"intro_landmarks"})
        for i, st in enumerate(stops):
            si = 2 + i
            a,b = span(si) if si < len(sents) else (0,0)
            scenes.append({"id":f"stop{st['diem']}","start":a,"end":b,"mode":"stop","stop_id":st["id"],"diem":st["diem"]})
        # CTA = last sentence
        a,b = span(len(sents)-1) if len(sents) > 2+N else span(9)
        # if last stop already used last sent, pad CTA after VO
        last_end = max(sc["end"] for sc in scenes)
        if a <= scenes[-1]["start"]:
            a, b = last_end, last_end + 4.5
        scenes.append({"id":"cta","start":a,"end":max(b, a+4.5),"mode":"cta"})
        # end card pad
        duration = max(sc["end"] for sc in scenes) + 2.0
        return scenes, duration
    # fallback placeholder timings ~90s
    duration = 90.0
    scenes = [
        {"id":"hook","start":0,"end":6,"mode":"hook"},
        {"id":"intro","start":6,"end":11.5,"mode":"intro_landmarks"},
    ]
    t = 11.5
    spans = [12.5,11,9,11,8,9,10.5]  # approx per stop
    for i, st in enumerate(stops):
        d = spans[i] if i < len(spans) else 10
        scenes.append({"id":f"stop{st['diem']}","start":t,"end":t+d,"mode":"stop","stop_id":st["id"],"diem":st["diem"]})
        t += d
    scenes.append({"id":"cta","start":t,"end":t+7.5,"mode":"cta"})
    return scenes, t+7.5


def build_html(cfg, index, scenes, duration, *, has_voice=False):
    MW, MH = index["map"]["w"], index["map"]["h"]
    N = index["N"]
    mosaic = cfg["map"]["mosaic"]
    attrib = cfg["map"]["attribution"]
    disc = cfg["map"]["disclaimer"]
    stops = index["stops"]

    # camera helpers in JS; precompute targets
    if stops:
        ox = sum(s["px"] for s in stops) / len(stops)
        oy = sum(s["py"] for s in stops) / len(stops)
    else:
        ox, oy = MW/2, MH/2

    # pins HTML
    pins = []
    for lm in cfg["landmarks"]:
        p = index["places"][lm["id"]]
        kind = "hotel" if lm.get("type")=="hotel" else "landmark"
        src = "assets/pins/hotel.svg" if kind=="hotel" else "assets/pins/landmark.svg"
        short = {"nha-hat-lon":"Nhà hát Lớn","cho-sat":"Chợ Sắt","avani":"Avani"}.get(lm["id"], lm["name"])
        side = "right" if p["px"] < MW*0.28 else ("left" if p["px"] > MW*0.72 else "top")
        pins.append(
            f'<div class="pin {kind}" id="pin-{lm["id"]}" style="left:{p["px"]}px;top:{p["py"]}px">'
            f'<div class="label side-{side}">{short}</div>'
            f'<img class="pin-img" src="{src}" alt=""/></div>'
        )
    for s in stops:
        gold = " gold" if s["diem"]==7 else ""
        src = "assets/pins/restaurant-gold.svg" if s["diem"]==7 else "assets/pins/restaurant.svg"
        pins.append(
            f'<div class="pin stop{gold}" id="pin-{s["id"]}" style="left:{s["px"]}px;top:{s["py"]}px">'
            f'<div class="label side-top">Đ{s["diem"]}</div>'
            f'<img class="pin-img" src="{src}" alt=""/>'
            f'<span class="food-emoji" id="foodemoji-{s["id"]}">{s.get("food_emoji","")}</span></div>'
        )

    route_pts = " ".join(f'{r["px"]},{r["py"]}' for r in index["route"])

    # photo cards + info cards + quotes
    photos = []
    cards = []
    quotes = []
    for s in stops:
        rating = s["rating"]
        rev = s.get("reviews_screen") or f'~{fmt_reviews(s["reviews"])} review'
        price = f'<div class="price">💵 {s["price_screen"]}</div>' if s.get("price_screen") else ""
        hours = f'<div class="hours">🕔 {s["hours_tag"]}</div>' if s.get("hours_tag") else ""
        tag = f'<div class="tag">{s["tag"]}</div>' if s.get("tag") else ""
        day = s.get("daypart") or ""
        q = s.get("quote") or {}
        stars_n = int(q.get("stars") or 5)
        photos.append(f'''
    <div class="photo-card" id="photo-{s["id"]}" style="opacity:0">
      <div class="photo-glow"></div>
      <div class="photo-frame">
        <img class="photo-img" id="photoimg-{s["id"]}" src="{s["photo"]}" alt=""/>
        <div class="photo-label">Ảnh minh hoạ</div>
        <div class="photo-steam" aria-hidden="true"></div>
      </div>
    </div>''')
        cards.append(f'''
    <div class="card" id="card-{s["id"]}" style="opacity:0">
      <div class="card-left">
        <img class="rank-badge" src="assets/badges/diem-{s["diem"]}.svg" alt="ĐIỂM {s["diem"]}"/>
        <div class="food-emoji-lg">{s.get("food_emoji","")}</div>
      </div>
      <div class="card-body">
        <div class="daypart">{day}</div>
        <div class="name">{s["short"]}</div>
        <div class="area">{s.get("area","")}</div>
        <div class="rating-row">
          <div class="starwrap"><div class="empty">{star_svgs("#4a4a4a",5,48)}</div>
            <div class="gold" id="gold-{s["id"]}" style="width:0">{star_svgs("#F5C518",5,48)}</div></div>
          <div class="rating-num">⭐ ~{rating:.1f}</div>
        </div>
        <div class="reviews">{rev}</div>
        {price}{hours}{tag}
      </div>
    </div>''')
        quotes.append(f'''
    <div class="quote" id="quote-{s["id"]}" style="opacity:0">
      <div class="quote-stars">{star_svgs("#F5C518", stars_n, 32)}</div>
      <div class="quote-text">“{q.get("text","")}”</div>
      <div class="quote-meta">— {q.get("author","")} · <em>{q.get("label","")}</em></div>
    </div>''')

    # recap row
    recap_items = "".join(
        f'<div class="recap-item" id="recap-{s["id"]}"><span class="ri-emoji">{s.get("food_emoji","")}</span>'
        f'<span class="ri-diem">Đ{s["diem"]}</span></div>'
        for s in stops
    )

    # scene JS targets
    js_scenes = []
    for sc in scenes:
        mode = sc["mode"]; stop_id = sc.get("stop_id")
        cam = (ox, oy); zoom = 1.15
        if mode == "stop" and stop_id:
            p = index["places"][stop_id]
            cam = (p["px"], p["py"]); zoom = 2.2
            # Văn Cao is far — slightly less zoom so context remains
            if stop_id == "bun-ca":
                zoom = 1.85
        elif mode == "intro_landmarks":
            if "nha-hat-lon" in index["places"]:
                p = index["places"]["nha-hat-lon"]; cam = (p["px"], p["py"])
            zoom = 1.35
        elif mode == "hook":
            zoom = 1.05
        elif mode == "cta":
            zoom = 1.0; cam = (ox, oy)
        js_scenes.append({**sc, "cx": cam[0], "cy": cam[1], "zoom": zoom})

    stops_js = json.dumps([{"id":s["id"],"diem":s["diem"],"px":s["px"],"py":s["py"],"rating":s["rating"]} for s in stops])
    scenes_js = json.dumps(js_scenes)
    lm_js = json.dumps([lm["id"] for lm in cfg["landmarks"]])
    N_js = N

    voice_audio = ""
    if has_voice and (T/"assets"/"voice.wav").exists():
        voice_audio = f'<audio id="voice" src="assets/voice.wav" data-start="0" data-duration="{duration}" data-track-index="30" data-volume="1"></audio>'
    # BGM + SFX
    bgm = ""
    # BGM mixed externally into voice or separate — keep SFX in composition
    sfx = f'''
  <audio id="sfx-whoosh" src="assets/sfx/whoosh.wav" data-start="0.1" data-duration="0.45" data-track-index="20" data-volume="0.4"></audio>
  <audio id="sfx-pop" src="assets/sfx/pop.wav" data-start="0.5" data-duration="0.12" data-track-index="20" data-volume="0.7"></audio>
  <audio id="sfx-ding" src="assets/sfx/ding.wav" data-start="1.0" data-duration="0.3" data-track-index="20" data-volume="0.5"></audio>'''

    # photo credit line (end)
    credits = "Ảnh: Wikimedia Commons (CC BY-SA) · Pexels · minh hoạ tự vẽ"

    html = f'''<!doctype html>
<html lang="vi"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<title>MAP-FOOD-HP-01 · 7 điểm Hải Phòng</title>
<script src="assets/gsap.min.js"></script>
<style>
@font-face{{font-family:'BeVietnam';src:url('assets/fonts/BeVietnamPro-Regular.ttf');font-weight:400}}
@font-face{{font-family:'BeVietnam';src:url('assets/fonts/BeVietnamPro-Medium.ttf');font-weight:500}}
@font-face{{font-family:'BeVietnam';src:url('assets/fonts/BeVietnamPro-SemiBold.ttf');font-weight:600}}
@font-face{{font-family:'BeVietnam';src:url('assets/fonts/BeVietnamPro-Bold.ttf');font-weight:700}}
@font-face{{font-family:'BeVietnam';src:url('assets/fonts/BeVietnamPro-ExtraBold.ttf');font-weight:800}}
@font-face{{font-family:'BeVietnam';src:url('assets/fonts/BeVietnamPro-Black.ttf');font-weight:900}}
@font-face{{font-family:'NotoColorEmoji';src:url('assets/fonts/NotoColorEmoji.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#0a0c10;font-family:'BeVietnam',system-ui,sans-serif;color:#fff}}
#root{{width:1080px;height:1920px;position:relative;overflow:hidden}}
#mapWorld{{position:absolute;left:0;top:0;width:{MW}px;height:{MH}px;transform-origin:0 0}}
#mapWorld img.map{{width:100%;height:100%;display:block;filter:brightness(.94) contrast(1.08)}}
.pin{{position:absolute;width:96px;height:120px;margin-left:-48px;margin-top:-120px;transform-origin:50% 100%;opacity:0;z-index:12}}
.pin .pin-img{{width:100%;height:100%;filter:drop-shadow(0 8px 12px rgba(0,0,0,.55))}}
.pin.landmark,.pin.hotel{{width:72px;height:90px;margin-left:-36px;margin-top:-90px}}
.pin .label{{position:absolute;background:rgba(0,0,0,.88);color:#fff;font-size:22px;font-weight:800;padding:6px 14px;border-radius:12px;white-space:nowrap;border:1.5px solid rgba(245,197,24,.45)}}
.pin .label.side-top{{left:50%;bottom:100%;transform:translate(-50%,-8px)}}
.pin .label.side-left{{right:100%;top:8px;transform:translate(-8px,0)}}
.pin .label.side-right{{left:100%;top:8px;transform:translate(8px,0)}}
.pin .food-emoji{{position:absolute;left:70px;top:-28px;font-size:44px;font-family:'NotoColorEmoji',sans-serif;opacity:0;filter:drop-shadow(0 6px 10px rgba(0,0,0,.5))}}
.vignette{{position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at center,transparent 40%,rgba(0,0,0,.5) 100%);z-index:5}}
.ui{{position:absolute;inset:0;pointer-events:none;z-index:20}}
.hook{{position:absolute;top:180px;left:36px;right:36px;opacity:0;z-index:40}}
.hook .glass{{background:rgba(10,12,18,.82);border:2.5px solid rgba(245,197,24,.7);border-radius:28px;padding:32px 28px;box-shadow:0 18px 50px rgba(0,0,0,.55);backdrop-filter:blur(18px);text-align:center}}
.hook-title{{font-size:56px;font-weight:900;line-height:1.15}}
.hook-sub{{font-size:32px;font-weight:700;color:#F5C518;margin-top:12px}}
.progress{{position:absolute;top:100px;right:28px;padding:10px 18px;border-radius:999px;background:rgba(0,0,0,.55);border:1px solid rgba(245,197,24,.5);font-size:28px;font-weight:900;color:#F5C518;opacity:0;z-index:50}}
.dayclock{{position:absolute;top:100px;left:28px;padding:8px 14px;border-radius:999px;background:rgba(0,0,0,.5);font-size:24px;font-weight:800;opacity:0;z-index:50}}
.photo-card{{position:absolute;left:56px;top:200px;width:420px;height:420px;z-index:35}}
.photo-glow{{position:absolute;inset:-10px;border-radius:40px;background:radial-gradient(circle,rgba(245,197,24,.45),transparent 70%);filter:blur(8px)}}
.photo-frame{{position:absolute;inset:0;border-radius:36px;overflow:hidden;border:3px solid rgba(245,197,24,.75);box-shadow:0 16px 40px rgba(0,0,0,.5);background:#111}}
.photo-img{{width:100%;height:100%;object-fit:cover;transform-origin:center center}}
.photo-label{{position:absolute;left:12px;bottom:12px;background:rgba(0,0,0,.65);color:#fff;font-size:20px;font-weight:700;padding:6px 12px;border-radius:10px}}
.photo-steam{{position:absolute;inset:0;background:radial-gradient(circle at 50% 80%,rgba(255,255,255,.12),transparent 55%);pointer-events:none}}
.card{{position:absolute;left:32px;right:32px;bottom:130px;display:flex;gap:18px;align-items:stretch;padding:24px 26px;border-radius:28px;background:rgba(10,12,18,.80);border:2.5px solid rgba(245,197,24,.55);box-shadow:0 18px 50px rgba(0,0,0,.55);backdrop-filter:blur(18px);z-index:40}}
.card-left{{display:flex;flex-direction:column;align-items:center;gap:8px;min-width:130px}}
.rank-badge{{width:160px;height:auto}}
.food-emoji-lg{{font-size:56px;font-family:'NotoColorEmoji',sans-serif;line-height:1}}
.card-body{{flex:1;min-width:0;display:flex;flex-direction:column;gap:6px;justify-content:center}}
.daypart{{font-size:24px;font-weight:800;color:#F5C518}}
.name{{font-size:44px;font-weight:900;line-height:1.12;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.area{{font-size:26px;font-weight:600;color:rgba(255,255,255,.75)}}
.rating-row{{display:flex;align-items:center;gap:12px;margin-top:4px}}
.starwrap{{position:relative;width:260px;height:48px}}
.starwrap .empty,.starwrap .gold{{position:absolute;left:0;top:0;display:flex;gap:4px}}
.starwrap .gold{{overflow:hidden;width:0}}
.rating-num{{font-size:36px;font-weight:900;color:#F5C518}}
.reviews{{font-size:32px;font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.price,.hours{{font-size:28px;font-weight:700;color:#B8F2A0}}
.hours{{color:#FFD Pan}}
.hours{{color:#FFD27A}}
.tag{{display:inline-block;margin-top:4px;padding:6px 14px;border-radius:999px;background:rgba(245,197,24,.2);border:1px solid rgba(245,197,24,.6);font-size:24px;font-weight:800;color:#F5C518;width:fit-content}}
.quote{{position:absolute;left:40px;right:40px;top:640px;padding:20px 24px;border-radius:22px;background:rgba(255,255,255,.94);color:#111;border:2px solid rgba(245,197,24,.45);box-shadow:0 12px 32px rgba(0,0,0,.35);z-index:42}}
.quote-stars{{display:flex;gap:2px;margin-bottom:8px}}
.quote-text{{font-size:30px;font-weight:700;line-height:1.35;color:#111}}
.quote-meta{{margin-top:8px;font-size:22px;font-weight:600;color:#444}}
.cta{{position:absolute;left:32px;right:32px;bottom:160px;opacity:0;z-index:45;text-align:center}}
.cta-box{{background:rgba(10,12,18,.85);border:2.5px solid rgba(245,197,24,.65);border-radius:28px;padding:28px 22px;backdrop-filter:blur(16px)}}
.cta-title{{font-size:48px;font-weight:900}}
.cta-sub{{font-size:30px;font-weight:700;color:#F5C518;margin-top:10px}}
.recap{{display:flex;justify-content:center;gap:10px;margin-top:18px;flex-wrap:wrap}}
.recap-item{{display:flex;flex-direction:column;align-items:center;gap:4px;padding:8px 10px;border-radius:16px;background:rgba(255,255,255,.08);border:1px solid rgba(245,197,24,.35);min-width:78px;opacity:0}}
.ri-emoji{{font-size:36px;font-family:'NotoColorEmoji',sans-serif}}
.ri-diem{{font-size:18px;font-weight:800;color:#F5C518}}
.footer{{position:absolute;left:20px;right:20px;bottom:22px;display:flex;justify-content:space-between;align-items:center;gap:10px;z-index:55}}
.disclaimer{{font-size:18px;font-weight:700;color:rgba(255,255,255,.85);background:rgba(0,0,0,.55);padding:8px 14px;border-radius:10px}}
.attr{{font-size:16px;color:rgba(255,255,255,.5)}}
.credits{{position:absolute;left:20px;right:20px;bottom:70px;font-size:16px;color:rgba(255,255,255,.45);text-align:center;opacity:0;z-index:50}}
</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{duration:.3f}" data-width="1080" data-height="1920" data-fps="30">
  <div id="mapStage" class="clip" data-start="0" data-duration="{duration:.3f}" data-track-index="0">
    <div id="mapWorld">
      <img class="map" src="{mosaic}" width="{MW}" height="{MH}" alt="Hải Phòng"/>
      <svg id="routeSvg" viewBox="0 0 {MW} {MH}" width="{MW}" height="{MH}" style="position:absolute;left:0;top:0;pointer-events:none;opacity:0">
        <polyline id="routeLine" points="{route_pts}" fill="none" stroke="#F5C518" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="18 14" opacity="0.85"/>
      </svg>
      {''.join(pins)}
    </div>
  </div>
  <div class="vignette"></div>
  <div class="ui">
    <div class="hook" id="hook">
      <div class="glass">
        <div class="hook-title">MỘT NGÀY ĂN SẬP<br/><span style="color:#F5C518">HẢI PHÒNG 🔥</span></div>
        <div class="hook-sub">7 điểm · 7 món · Sáng → Tối</div>
      </div>
    </div>
    <div class="dayclock" id="dayclock">☀️ Sáng</div>
    <div class="progress" id="progress"><span id="progressTxt">1/{N_js}</span></div>
    {''.join(photos)}
    {''.join(cards)}
    {''.join(quotes)}
    <div class="cta" id="cta">
      <div class="cta-box">
        <div class="cta-title">LƯU TUYẾN NÀY 🔖</div>
        <div class="cta-sub">Rủ hội bạn đi ăn cùng · Hinton Media</div>
        <div class="recap" id="recap">{recap_items}</div>
      </div>
    </div>
    <div class="credits" id="credits">{credits}</div>
  </div>
  <div class="footer">
    <div class="disclaimer">{disc}</div>
    <div class="attr">{attrib}</div>
  </div>
  {voice_audio}
  {sfx}
</div>
<script>
const W=1080,H=1920,PIN_Y=H*0.36;
const cam=(px,py,s)=>({{x:W/2-px*s,y:PIN_Y-py*s,scale:s}});
const SCENES={scenes_js};
const STOPS={stops_js};
const LM={lm_js};
const N={N_js};
const overview=cam({ox:.2f},{oy:.2f},1.05);
const tl=gsap.timeline({{paused:true}});
gsap.set('#mapWorld',overview);
gsap.set(['#hook','#cta','#progress','#dayclock','.card','.quote','.photo-card','.pin','.food-emoji','#routeSvg','#credits','.recap-item'],{{opacity:0}});
gsap.set('.pin',{{scale:0}});
gsap.set('.card',{{y:50}});
gsap.set('.quote',{{scale:0.86}});
gsap.set('.photo-card',{{scale:0.85,y:20}});

const route=document.getElementById('routeLine');
let routeLen=0; try{{routeLen=route.getTotalLength();}}catch(e){{routeLen=3000;}}
gsap.set(route,{{strokeDasharray:routeLen,strokeDashoffset:routeLen}});

const dayMap={{'Sáng':'☀️ Sáng','Trưa':'🌤️ Trưa','Chiều':'🌇 Chiều','Tối':'🌙 Tối','Tráng miệng':'🍡 Tráng miệng'}};
const stopDay={json.dumps({s["id"]: s.get("daypart","") for s in stops})};

function easeCam(sc){{
  const c=cam(sc.cx,sc.cy,sc.zoom);
  const dur=Math.max(0.45, Math.min(1.8,(sc.end-sc.start)*0.4));
  tl.to('#mapWorld',{{x:c.x,y:c.y,scale:c.scale,duration:dur,ease:'power2.inOut'}},sc.start);
}}

// Hook
tl.to('#hook',{{opacity:1,duration:0.3}},0.05);
tl.to('#hook',{{opacity:0,duration:0.25}}, Math.max(0.5, SCENES[0].end-0.3));

// Landmarks + route begin on intro
const intro=SCENES.find(s=>s.mode==='intro_landmarks')||SCENES[1];
if(intro){{
  easeCam(intro);
  LM.forEach((id,i)=>{{
    tl.to('#pin-'+id,{{opacity:0.95,scale:1,duration:0.35,ease:'back.out(1.8)'}},intro.start+0.1+i*0.1);
  }});
  tl.set('#routeSvg',{{opacity:1}},intro.start+0.3);
  // progressive route across whole tour
  const stopScenes=SCENES.filter(s=>s.mode==='stop');
  const routeEnd=stopScenes.length?stopScenes[stopScenes.length-1].end:intro.end;
  tl.to(route,{{strokeDashoffset:0,duration:Math.max(2,routeEnd-intro.start-0.5),ease:'none'}},intro.start+0.35);
}}

SCENES.forEach((sc)=>{{
  if(sc.mode==='hook') return;
  if(sc.mode!=='intro_landmarks') easeCam(sc);
  if(sc.mode==='stop' && sc.stop_id){{
    const id=sc.stop_id;
    const diem=sc.diem||1;
    const rating=(STOPS.find(s=>s.id===id)||{{}}).rating||4;
    tl.fromTo('#pin-'+id,{{opacity:0,scale:0}},{{opacity:1,scale:1,duration:0.45,ease:'back.out(2.4)'}},sc.start);
    tl.to('#foodemoji-'+id,{{opacity:1,duration:0.3,ease:'back.out(2)'}},sc.start+0.12);
    // photo pop + Ken Burns
    tl.to('#photo-'+id,{{opacity:1,scale:1,y:0,duration:0.4,ease:'back.out(1.6)'}},sc.start+0.08);
    tl.fromTo('#photoimg-'+id,{{scale:1}},{{scale:1.08,duration:Math.max(1.2,sc.end-sc.start-0.3),ease:'sine.inOut'}},sc.start+0.15);
    // card
    tl.to('#card-'+id,{{opacity:1,y:0,duration:0.4,ease:'power2.out'}},sc.start+0.15);
    tl.to('#gold-'+id,{{width:260*(rating/5),duration:0.7,ease:'power2.out'}},sc.start+0.35);
    // quote
    tl.to('#quote-'+id,{{opacity:1,scale:1,duration:0.35,ease:'back.out(1.7)'}},sc.start+0.45);
    // progress + dayclock
    tl.set('#progressTxt',{{textContent:diem+'/'+N}},sc.start);
    tl.to('#progress',{{opacity:1,duration:0.2}},sc.start);
    const dp=stopDay[id];
    if(dp){{ tl.set('#dayclock',{{textContent:dayMap[dp]||dp}},sc.start); tl.to('#dayclock',{{opacity:1,duration:0.2}},sc.start); }}
    // hide near end
    tl.to(['#card-'+id,'#quote-'+id,'#photo-'+id],{{opacity:0,duration:0.25}},sc.end-0.15);
  }}
  if(sc.mode==='cta'){{
    tl.to('#cta',{{opacity:1,duration:0.35}},sc.start);
    tl.to('#progress',{{opacity:0,duration:0.2}},sc.start);
    tl.to('#dayclock',{{opacity:0,duration:0.2}},sc.start);
    STOPS.forEach((s,i)=>{{
      tl.to('#recap-'+s.id,{{opacity:1,duration:0.2}},sc.start+0.2+i*0.08);
    }});
    tl.to('#credits',{{opacity:1,duration:0.3}},sc.start+0.5);
  }}
}});
window.__timelines=window.__timelines||{{}};window.__timelines['main']=tl;
</script>
</body></html>
'''
    # fix accidental typo in CSS if any
    html = html.replace('.hours{color:#FFD Pan}\n.hours{color:#FFD27A}', '.hours{color:#FFD27A}')
    return html


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="full.html")
    ap.add_argument("--duration", type=float, default=None)
    args = ap.parse_args()
    cfg, meta, timings = load_all()
    index = enrich(cfg, meta)
    scenes, duration = build_scenes(cfg, index, timings)
    if args.duration:
        duration = args.duration
    has_voice = False
    vw = VOICE / "voice_storytelling.wav"
    if vw.exists():
        shutil.copy2(vw, T / "assets" / "voice.wav")
        has_voice = True
    # ensure sfx in assets
    sfx_src = JOB / "audio" / "sfx"
    sfx_dst = T / "assets" / "sfx"
    sfx_dst.mkdir(parents=True, exist_ok=True)
    if sfx_src.exists():
        for f in sfx_src.glob("*.wav"):
            shutil.copy2(f, sfx_dst / f.name)
    html = build_html(cfg, index, scenes, duration, has_voice=has_voice)
    out = T / args.out
    out.write_text(html, encoding="utf-8")
    meta_out = {"duration": duration, "scenes": scenes, "N": index["N"], "has_voice": has_voice}
    (T / "full-meta.json").write_text(json.dumps(meta_out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out} duration={duration:.2f}s N={index['N']} voice={has_voice} map={index['map']['w']}x{index['map']['h']}")


if __name__ == "__main__":
    main()
