#!/usr/bin/env python3
"""MAP-HOTEL-HP-01 — HyperFrames builder: Top 5 khách sạn Hải Phòng (map animation, 9:16)."""
from __future__ import annotations
import json, math, re, argparse
from pathlib import Path

T = Path(__file__).resolve().parent
JOB = T.parent
W, H, FY = 1080, 1920, 560

def ll2px(lat, lng, m):
    n = 2 ** m["z"]; x = (lng + 180) / 360 * n; r = math.radians(lat)
    y = (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * n
    return round((x - m["tx0"]) * 256, 1), round((y - m["ty0"]) * 256, 1)

def fmt_int(n): return f"{n:,}".replace(",", ".")
def fmt_rating(r): return f"{r:.1f}".replace(".", ",")

STAR = "M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.9L12 17.8 5.8 21.1 7 14.2 2 9.3l6.9-1z"
def stars(fill, n=5, size=44, gap=4):
    return "".join(f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" style="margin-right:{gap}px"><path fill="{fill}" d="{STAR}"/></svg>' for _ in range(n))

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

NAMES = ["Pearl River Hotel", "Sheraton", "Mercure", "Pullman", "Meliá", "Vinpearl", "Rivera", "Google Maps", "Google", "Hinton Media", "Đồ Sơn", "Hải Phòng"]
def hl(text):
    t = esc(text)
    for n in sorted(NAMES, key=len, reverse=True):
        t = t.replace(n, f"\u0001{n}\u0002")
    t = re.sub(r"(\d[\d.,]*)", lambda m: f"\u0001{m.group(1)}\u0002", t)
    # collapse nested markers
    out, depth = "", 0
    for ch in t:
        if ch == "\u0001":
            if depth == 0: out += '<span class="hl">'
            depth += 1
        elif ch == "\u0002":
            depth -= 1
            if depth == 0: out += "</span>"
        else: out += ch
    return out

def load():
    places = json.loads((JOB / "places.json").read_text())
    script = json.loads((JOB / "script.json").read_text())
    import os
    tim = json.loads(Path(os.environ.get("TIMINGS", JOB / "voice" / "timings.json")).read_text())
    meta = json.loads((T / "assets/map/map-meta.json").read_text())
    cues = None
    cp = JOB / "voice" / "cues.json"
    if cp.exists(): cues = json.loads(cp.read_text())
    return places, script, tim, meta, cues

def phrase_cues(tim):
    """Fallback: split each sentence's duration across phrases by voice syllable count."""
    cues = []
    for s in tim["sentences"]:
        ph = s["phrases"]; n = [max(1, len(p[1].split())) for p in ph]; tot = sum(n)
        t = s["start"]; d = s["end"] - s["start"]
        for p, k in zip(ph, n):
            e = t + d * k / tot
            cues.append({"start": round(t, 3), "end": round(e, 3), "text": p[0], "scene": s["scene"]})
            t = e
    return cues

def build(places, script, tim, meta, cues):
    hotels = {h["id"]: h for h in places["hotels"]}
    sents = tim["sentences"]
    total_vo = tim["total"]
    scene_ids = [sc["id"] for sc in script["scenes"]]
    sc_t = {}
    for sid in scene_ids:
        ss = [s for s in sents if s["scene"] == sid]
        sc_t[sid] = {"start": ss[0]["start"], "end": ss[-1]["end"], "sents": [(s["start"], s["end"]) for s in ss]}
    DUR = round(total_vo + 2.6, 3)
    order = [sc for sc in script["scenes"] if sc.get("rank")]
    # pixel coords
    for h in hotels.values():
        h["px"], h["py"] = ll2px(h["lat"], h["lng"], meta)
    ranked = [hotels[sc["id"]] | {"rank": sc["rank"], "scene": sc["id"]} for sc in order]
    cx = sum(h["px"] for h in ranked) / len(ranked); cy = sum(h["py"] for h in ranked) / len(ranked)
    if cues is None: cues = phrase_cues(tim)

    # landmarks (map-space labels)
    lms = [
        ("SÔNG CẤM", 20.8705, 106.6800, "river"), ("SÔNG LẠCH TRAY", 20.8265, 106.6560, "river"),
        ("Hồ Tam Bạc", 20.8560, 106.6745, "lm"), ("Nhà hát Lớn", 20.857122, 106.681811, "lm"),
        ("Sân bay Cát Bi", 20.8215, 106.7230, "lm"), ("Hồ An Biên", 20.8517, 106.6790, "lm"),
    ]
    lm_html = []
    for name, la, ln, kind in lms:
        x, y = ll2px(la, ln, meta)
        lm_html.append(f'<div class="mlabel {kind}" style="left:{x}px;top:{y}px"><span>{name}</span></div>')

    # pins
    pin_html = []
    for h in ranked:
        gold = h["rank"] == 1
        crown = '<img class="crown" src="assets/icons/crown.svg"/>' if gold else ""
        pin_html.append(f'''<div class="pin" id="pin-{h["id"]}" style="left:{h["px"]}px;top:{h["py"]}px">
  <div class="cs"><div class="ripple" id="rip-{h["id"]}"></div></div><div class="cs"><div class="ripple r2" id="rip2-{h["id"]}"></div></div>
  <div class="cs"><div class="pin-inner" id="pinin-{h["id"]}">{crown}<img class="pin-img" src="assets/icons/pin-{"gold" if gold else "red"}.svg"/>
  <div class="tagpos" id="tag-{h["id"]}"><div class="pin-tag">#{h["rank"]} {esc(h["short"])}</div></div></div></div>
  <div class="cs"><div class="qpin" id="qpin-{h["id"]}">?</div></div>
</div>''')

    # arcs between consecutive ranked hotels (route order #5 -> #1)
    arcs, dots, arc_meta = [], [], []
    prev = None
    for h in ranked:
        if prev is not None:
            x1, y1, x2, y2 = prev["px"], prev["py"], h["px"], h["py"]
            dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy)
            nx, ny = -dy / L, dx / L
            k = 0.28 * L
            qx, qy = (x1 + x2) / 2 + nx * k, (y1 + y2) / 2 + ny * k
            if qy > (y1 + y2) / 2:  # always bow upward (north) for a "flight" feel
                qx, qy = (x1 + x2) / 2 - nx * k, (y1 + y2) / 2 - ny * k
            d = f"M{x1},{y1} Q{qx:.1f},{qy:.1f} {x2},{y2}"
            pts = []
            for i in range(25):
                t = i / 24
                px = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * qx + t * t * x2
                py = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * qy + t * t * y2
                pts.append((round(px, 1), round(py, 1)))
            aid = f"{prev['id']}-{h['id']}"
            arcs.append(f'<path class="arc-glow" id="arcg-{aid}" d="{d}"/><path class="arc" id="arc-{aid}" d="{d}"/>')
            dots.append(f'<div class="dot" id="dot-{aid}" style="left:0;top:0;transform:translate({x1}px,{y1}px)"><div class="dot-in"></div></div>')
            arc_meta.append({"id": aid, "to": h["id"], "pts": pts})
        prev = h

    # cards & bubbles
    card_html, bub_html = [], []
    for h in ranked:
        rid = h["id"]
        qs = h["reviews_quotes"][:2]
        card_html.append(f'''<div class="card" id="card-{rid}">
  <div class="medal{" gold" if h["rank"]==1 else ""}"><div class="medal-top">HẠNG</div><div class="medal-n">{h["rank"]}</div></div>
  <div class="cbody">
    <div class="cname">{esc(h["short"])}</div>
    <div class="carea"><img src="assets/icons/gpin.svg" class="gp"/> {esc(h["area"])}</div>
    <div class="crow"><div class="starwrap"><div class="st-empty">{stars("#3b4250")}</div><div class="st-gold" id="stg-{rid}">{stars("#FFC93C")}</div></div>
      <div class="cnum"><span id="rnum-{rid}">0,0</span><small>/5</small></div></div>
    <div class="crev"><span class="gg">Google Maps</span> · khoảng <b id="rev-{rid}">0</b> review</div>
    <div class="chips"><span class="chip">Khách sạn 5 sao</span><span class="chip c2">{esc(h["area"].split("·")[-1].strip())}</span></div>
  </div>
</div>''')
        for qi, q in enumerate(qs):
            words = " ".join(f'<span class="w">{esc(w)}</span>' for w in q["text_vi"].split())
            bub_html.append(f'''<div class="bubble b{qi}" id="bub-{rid}-{qi}">
  <div class="bhead"><img src="assets/icons/avatar.svg" class="av"/><div><div class="bname">Khách lưu trú</div><div class="bstars">{stars("#FFC93C", int(q["stars"]), 30, 2)}</div></div></div>
  <div class="btext">“{words}”</div>
  <div class="blabel">{esc(q["label"])}</div>
</div>''')

    ladder = "".join(f'<div class="lad" id="lad-{h["id"]}"><span>{h["rank"]}</span></div>' for h in ranked)
    recap = "".join(
        f'<div class="rrow" id="rrow-{h["id"]}"><div class="rr">#{h["rank"]}</div><div class="rn">{esc(h["short"])}</div>'
        f'<div class="rs"><svg viewBox="0 0 24 24" width="30" height="30"><path fill="#FFC93C" d="{STAR}"/></svg>{fmt_rating(h["rating"])}</div></div>'
        for h in sorted(ranked, key=lambda x: x["rank"]))

    cue_html = "".join(f'<div class="cue" id="cue{i}">{hl(c["text"])}</div>' for i, c in enumerate(cues))

    data = {
        "DUR": DUR, "W": W, "H": H, "FY": FY, "center": [cx, cy],
        "scenes": sc_t, "ranked": [{"id": h["id"], "rank": h["rank"], "px": h["px"], "py": h["py"], "rating": h["rating"],
                                    "reviews": h["reviews"], "nq": len(h["reviews_quotes"][:2])} for h in ranked],
        "arcs": arc_meta, "cues": cues,
    }
    html = TEMPLATE.replace("/*DATA*/", json.dumps(data, ensure_ascii=False)) \
        .replace("<!--LANDMARKS-->", "".join(lm_html)).replace("<!--PINS-->", "".join(pin_html)) \
        .replace("<!--ARCS-->", "".join(arcs)).replace("<!--DOTS-->", "".join(dots)) \
        .replace("<!--CARDS-->", "".join(card_html)).replace("<!--BUBBLES-->", "".join(bub_html)) \
        .replace("<!--LADDER-->", ladder).replace("<!--RECAP-->", recap).replace("<!--CUES-->", cue_html) \
        .replace("{DUR}", f"{DUR:.3f}").replace("{MW}", str(meta["mosaic_w"])).replace("{MH}", str(meta["mosaic_h"])) \
        .replace("{ATTR}", "Ảnh vệ tinh © Esri, Maxar, Earthstar Geographics").replace("{DISC}", "Số liệu Google Maps 06/10/2026 · tham khảo")
    return html, data

TEMPLATE = (T / "tpl.tmpl").read_text(encoding="utf-8")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="index.html"); ap.add_argument("--duration", type=float)
    a = ap.parse_args()
    places, script, tim, meta, cues = load()
    html, data = build(places, script, tim, meta, cues)
    if a.duration:
        html = html.replace(f'data-duration="{data["DUR"]:.3f}"', f'data-duration="{a.duration:.3f}"')
    (T / a.out).write_text(html, encoding="utf-8")
    (T / "build-data.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
    print("wrote", a.out, "DUR", data["DUR"], "cues", len(data["cues"]))
