"""Edit plan (SO-TAY-DUNG 'Tin AI nóng'): hook card -> body shots 1.6-3 s (B-roll full frame + face PIP)
-> outro card. Every cut lands on a word start."""
import math
from .text_vi import salient_phrase


def _snap(t, starts):
    return min(starts, key=lambda s: abs(s - t)) if starts else t


def plan(words, sentences_t, voice_dur, pools, presenter, cfg):
    e = cfg["edit"]; pc = cfg["presenter"]
    fps = cfg["fps"]
    total = math.ceil((voice_dur + 0.45) * fps) / fps
    starts = [w["start"] for w in words]
    has_p = presenter is not None
    hook_end = _snap(e["hook_seconds"], [s for s in starts if 1.4 <= s <= 3.2]) if (has_p and pc["intro_card"]) else 0.0
    if has_p and pc["outro_card"]:
        last_sent_start = sentences_t[-1]["start"]
        cand = [s for s in starts if total - e["outro_seconds"] - 0.8 <= s <= total - 1.6]
        outro_start = _snap(total - e["outro_seconds"], cand) if cand else max(last_sent_start, total - e["outro_seconds"])
    else:
        outro_start = total
    # body cut points: sentence starts + equal splits snapped to word starts
    must = sorted({round(s["start"], 3) for s in sentences_t if hook_end + 0.8 < s["start"] < outro_start - 0.8})
    bounds = [hook_end] + must + [outro_start]
    cuts = [hook_end]
    for a, b in zip(bounds[:-1], bounds[1:]):
        L = b - a
        n = max(1, math.ceil(L / e["shot_max"]))
        if L / n < e["shot_min"] and n > 1:
            n -= 1
        inner = [w for w in starts if a + 0.5 < w < b - 0.5]
        for k in range(1, n):
            t = _snap(a + L * k / n, inner) if inner else a + L * k / n
            if t - cuts[-1] >= e["shot_min"] * 0.75:
                cuts.append(t)
        if b - cuts[-1] < e["shot_min"] * 0.6 and len(cuts) > 1 and b != outro_start:
            cuts.pop()
        cuts.append(b)
    cuts = sorted(set(round(c, 3) for c in cuts))
    shots = []
    for a, b in zip(cuts[:-1], cuts[1:]):
        if b - a < 0.2:
            continue
        ws = [w for w in words if a - 0.01 <= w["start"] < b - 0.01]
        si = ws[0]["sent"] if ws else 0
        shots.append({"start": a, "end": b, "dur": round(b - a, 3), "sent": si, "words": [w["word"] for w in ws]})
    assign(shots, pools, cfg)
    return {"total": round(total, 3), "hook_end": hook_end, "outro_start": outro_start, "shots": shots}


def assign(shots, pools, cfg):
    every = cfg["edit"]["effect_every"]
    demo, stock, shots_img = list(pools.get("demo", [])), pools.get("stock", {}), list(pools.get("screenshots", []))
    used_stock = set(); di = si = 0; last_src = None
    fx_cycle = ["textcard", "phone", "browser", "textcard", "keyword"]
    fx_i = 0
    have_footage = bool(demo or shots_img or any(stock.values()))
    img_style = 0
    for k, sh in enumerate(shots):
        phrase = salient_phrase(sh["words"], 6)
        sh["phrase"] = phrase
        pick = None
        if have_footage and not (every and k % every == every - 1):
            for c in stock.get(sh["sent"], []):
                if c["src"] not in used_stock:
                    pick = dict(c, type="video"); used_stock.add(c["src"]); break
            if not pick:
                use_img = shots_img and (not demo or k % 3 == 2)
                if use_img:
                    img = shots_img[si % len(shots_img)]; si += 1
                    pick = {"type": "kenburns" if img_style % 2 == 0 else "browser", "img": img}
                    img_style += 1
                elif demo:
                    for tries in range(len(demo)):
                        c = demo[di % len(demo)]; di += 1
                        if c["src"] != last_src or len(set(d["src"] for d in demo)) == 1:
                            break
                    pick = dict(c, type="video")
        if not pick:
            fx = fx_cycle[fx_i % len(fx_cycle)]; fx_i += 1
            pick = {"type": fx}
            if fx == "browser" and shots_img:
                pick["img"] = shots_img[si % len(shots_img)]; si += 1
        last_src = pick.get("src")
        sh["visual"] = pick
