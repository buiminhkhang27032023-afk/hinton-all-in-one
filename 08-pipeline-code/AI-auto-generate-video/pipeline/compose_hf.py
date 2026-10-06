"""Build the HyperFrames project (lam-viec/hf/index.html + assets/) from the edit plan."""
import html, json, math, os, shutil
from pathlib import Path
from .common import log, run, video_size, media_duration, REPO
from .text_vi import is_foreign_token


def _link(src, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        dst.unlink()
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def prep_shot_clip(v, dur, dst: Path, cfg):
    """Cut + normalise one B-roll clip to exactly `dur` s, 1080x1920@30, muted.
    Landscape sources -> blurred fill + fitted foreground (kept above the PIP zone)."""
    W, H, fps = cfg["width"], cfg["height"], cfg["fps"]
    sw, sh = video_size(v["src"])
    have = float(v.get("dur", dur))
    speed = 1.0
    if have < dur:
        speed = max(have / dur, 0.66)  # slow down up to 1.5x, freeze the rest
    pts = f"setpts=PTS/{speed:.4f}," if speed < 0.999 else ""
    pad = f",tpad=stop_mode=clone:stop_duration={dur:.3f}"
    if sw / sh > 0.75:
        vf = (f"[0:v]{pts}fps={fps},split=2[a][b];"
              f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=28:2,eq=brightness=-0.12[bg];"
              f"[b]scale={W}:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-170{pad},trim=duration={dur:.3f},format=yuv420p[v]")
    else:
        vf = (f"[0:v]{pts}fps={fps},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
              f"{pad},trim=duration={dur:.3f},format=yuv420p[v]")
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{float(v.get('start', 0)):.3f}", "-t", f"{min(have, dur / speed) + 0.1:.3f}",
         "-i", v["src"], "-filter_complex", vf, "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "18",
         "-preset", "fast", "-g", "15", str(dst)])


def esc(s):
    return html.escape(s or "", quote=True)


def keyword_of(words):
    cands = [w.strip(",.;:?!\"“”") for w in words]
    f = [w for w in cands if is_foreign_token(w)]
    if f:
        return max(f, key=len)
    return max(cands, key=len) if cands else ""


def build(plan, words, presenter, voice_wav, hf_dir: Path, cfg, notes):
    W, H = cfg["width"], cfg["height"]
    b, e, pc = cfg["brand"], cfg["edit"], cfg["presenter"]
    A = hf_dir / "assets"; A.mkdir(parents=True, exist_ok=True)
    for f in ("BeVietnamPro-Bold.ttf", "BeVietnamPro-ExtraBold.ttf", "BeVietnamPro-Black.ttf"):
        _link(REPO / "assets" / "fonts" / f, A / f)
    _link(REPO / "assets" / "vendor" / "gsap.min.js", A / "gsap.min.js")
    _link(voice_wav, A / "voice.wav")
    T, hook_end, outro_start = plan["total"], plan["hook_end"], plan["outro_start"]
    body, tl = [], []
    push = e["push_in_per_s"]

    # ---------- body shots ----------
    for i, sh in enumerate(plan["shots"]):
        v, st, du = sh["visual"], sh["start"], sh["dur"]
        if v["type"] == "video":
            dst = A / f"shot_{i:02d}.mp4"
            prep_shot_clip(v, du, dst, cfg)
            body.append(f'<div class="layer" id="w{i}"><video id="v{i}" class="full" src="assets/{dst.name}" muted playsinline '
                        f'data-start="{st}" data-duration="{du}" data-track-index="1"></video></div>')
            tl.append(f'tl.fromTo("#w{i}",{{scale:1}},{{scale:{1+push*du:.4f},duration:{du},ease:"none"}},{st});')
        elif v["type"] in ("kenburns", "browser") and v.get("img"):
            name = f"img_{i:02d}{Path(v['img']).suffix.lower()}"; _link(v["img"], A / name)
            if v["type"] == "kenburns":
                body.append(f'<div class="clip layer" id="s{i}" data-start="{st}" data-duration="{du}" data-track-index="1">'
                            f'<div class="kbbg" style="background-image:url(assets/{name})"></div>'
                            f'<div class="kbfit"><img id="k{i}" src="assets/{name}"/></div></div>')
                dx = 30 if i % 2 else -30
                tl.append(f'tl.fromTo("#k{i}",{{scale:1.04,x:{-dx}}},{{scale:{1.04+push*du*1.6:.4f},x:{dx},duration:{du},ease:"none"}},{st});')
            else:
                body.append(f'<div class="clip layer fxbg" id="s{i}" data-start="{st}" data-duration="{du}" data-track-index="1">'
                            f'<div class="browser" id="br{i}"><div class="bar"><i></i><i></i><i></i><span class="url"></span></div>'
                            f'<div class="viewport"><img id="k{i}" src="assets/{name}"/></div></div></div>')
                tl.append(f'tl.fromTo("#br{i}",{{y:60,opacity:0}},{{y:0,opacity:1,duration:0.25,ease:"power3.out"}},{st});')
                tl.append(f'tl.fromTo("#k{i}",{{y:0,scale:1.0}},{{y:-160,scale:1.06,duration:{du},ease:"none"}},{st});')
        elif v["type"] == "phone":
            body.append(f'<div class="clip layer fxbg" id="s{i}" data-start="{st}" data-duration="{du}" data-track-index="1">'
                        f'<div class="phone" id="ph{i}"><div class="notch"></div><div class="chat">'
                        f'<div class="bubble q" id="q{i}">Có gì mới về AI hôm nay?</div>'
                        f'<div class="bubble a" id="a{i}">{esc(" ".join(sh["words"]))}</div></div></div></div>')
            tl.append(f'tl.fromTo("#ph{i}",{{y:120,rotation:-4,opacity:0}},{{y:0,rotation:0,opacity:1,duration:0.3,ease:"power3.out"}},{st});')
            tl.append(f'tl.fromTo("#q{i}",{{scale:0.8,opacity:0}},{{scale:1,opacity:1,duration:0.18,ease:"back.out(3)"}},{st+0.15:.3f});')
            tl.append(f'tl.fromTo("#a{i}",{{scale:0.8,opacity:0}},{{scale:1,opacity:1,duration:0.18,ease:"back.out(3)"}},{st+0.55:.3f});')
        elif v["type"] == "keyword":
            kw = keyword_of(sh["words"])
            body.append(f'<div class="clip layer fxbg2" id="s{i}" data-start="{st}" data-duration="{du}" data-track-index="1">'
                        f'<div class="kwrap"><div class="bigword" id="bw{i}">{esc(kw)}</div></div></div>')
            tl.append(f'tl.fromTo("#bw{i}",{{scale:1.2,opacity:0,filter:"blur(8px)"}},{{scale:1,opacity:1,filter:"blur(0px)",duration:0.2,ease:"power2.out"}},{st});')
            tl.append(f'tl.to("#bw{i}",{{scale:1.06,duration:{max(du-0.2,0.1):.3f},ease:"none"}},{st+0.2:.3f});')
        else:  # textcard
            body.append(f'<div class="clip layer fxbg" id="s{i}" data-start="{st}" data-duration="{du}" data-track-index="1">'
                        f'<div class="cardwrap"><div class="tcard" id="tc{i}"><div class="tbar"></div>'
                        f'<div class="ttext">{esc(sh.get("phrase", ""))}</div></div></div></div>')
            tl.append(f'tl.fromTo("#tc{i}",{{scale:0.8,opacity:0}},{{scale:1,opacity:1,duration:0.18,ease:"back.out(2.5)"}},{st});')
            tl.append(f'tl.to("#tc{i}",{{scale:1.05,duration:{max(du-0.18,0.1):.3f},ease:"none"}},{st+0.18:.3f});')

    # ---------- presenter: intro / outro cards + PIP ----------
    pres_html, cards = [], []
    if presenter:
        if presenter["mode"] == "video":
            _link(presenter["full"], A / "presenter_full.mp4"); _link(presenter["pip"], A / "presenter_pip.mp4")
            L = presenter["length"]
        else:
            _link(presenter["card"], A / "presenter_card.jpg")
            for k, p in enumerate(presenter["pip_images"]):
                _link(p, A / f"presenter_pip{k}.jpg")

        def card(cid, st, du, media_start):
            if du <= 0.05:
                return
            if presenter["mode"] == "video":
                cards.append(f'<div class="layer" id="{cid}W"><video id="{cid}V" class="full" src="assets/presenter_full.mp4" muted playsinline '
                             f'data-start="{st}" data-duration="{du}" data-media-start="{media_start:.3f}" data-track-index="2"></video></div>')
                tl.append(f'tl.fromTo("#{cid}W",{{scale:1.0}},{{scale:{1+0.03*du:.4f},duration:{du},ease:"none"}},{st});')
            else:
                cards.append(f'<div class="clip layer photocard" id="{cid}" data-start="{st}" data-duration="{du}" data-track-index="2">'
                             f'<div class="pcbg"></div><div class="pcframe"><img id="{cid}I" src="assets/presenter_card.jpg"/></div></div>')
                tl.append(f'tl.fromTo("#{cid}I",{{scale:1.0,y:0}},{{scale:1.06,y:-20,duration:{du},ease:"sine.inOut"}},{st});')
            cards.append(f'<div class="clip layer shade" data-start="{st}" data-duration="{du}" data-track-index="3"></div>')

        if hook_end > 0:
            card("intro", 0, hook_end, 0.0)
        if outro_start < T:
            card("outro", outro_start, round(T - outro_start, 3), (L * 0.5) if presenter["mode"] == "video" else 0)

        # PIP over the body
        segs = presenter.get("segments", [])
        inner = []
        for s in segs:
            if presenter["mode"] == "video":
                inner.append(f'<video id="pv{s["idx"]}" class="pipv" src="assets/presenter_pip.mp4" muted playsinline '
                             f'data-start="{s["start"]}" data-duration="{s["dur"]}" data-media-start="{s["media_start"]}" data-track-index="4"></video>')
            else:
                k = s["idx"] % len(presenter["pip_images"])
                inner.append(f'<div class="clip pipimg" data-start="{s["start"]}" data-duration="{s["dur"]}" data-track-index="4">'
                             f'<img id="pi{s["idx"]}" src="assets/presenter_pip{k}.jpg"/></div>')
                sc0, sc1 = (1.0, 1.05) if s["idx"] % 2 == 0 else (1.05, 1.0)
                tl.append(f'tl.fromTo("#pi{s["idx"]}",{{scale:{sc0},y:0}},{{scale:{sc1},y:-6,duration:{s["dur"]},ease:"sine.inOut"}},{s["start"]});')
        size, px, py = pc["pip_size"], pc["pip_x"], pc["pip_y"]
        radius = "50%" if pc["pip_shape"] == "circle" else "36px"
        pres_html.append(f'<div id="pip" style="left:{px}px;top:{py}px;width:{size}px;height:{size}px;border-radius:{radius}">'
                         + "".join(inner) + f'<div id="pipRing" style="border-radius:{radius}"></div></div>')
        if segs:
            tl.append(f'tl.fromTo("#pip",{{scale:0.6,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2)"}},{hook_end});')
            tl.append(f'tl.to("#pip",{{opacity:0,duration:0.15}},{max(outro_start-0.15, hook_end+0.3):.3f});')

    # ---------- hook title ----------
    title = cfg.get("title") or ""
    lines = [l.strip() for l in title.split("|") if l.strip()] or [plan["shots"][0].get("phrase", "") if plan["shots"] else ""]
    hook_d = max(hook_end, 2.0)
    over = [f'<div class="clip hook" data-start="0" data-duration="{hook_d}" data-track-index="6"><div class="hookbox" id="hookbox">'
            + "".join(f'<div class="hl" id="hl{k}">{esc(l.upper())}</div>' for k, l in enumerate(lines[:2])) + '</div></div>']
    tl.append('tl.fromTo("#hookbox",{scale:0.92,opacity:0},{scale:1,opacity:1,duration:0.2,ease:"power2.out"},0);')
    for k in range(len(lines[:2])):
        tl.append(f'tl.fromTo("#hl{k}",{{clipPath:"inset(0% 100% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.4,ease:"power2.inOut"}},{0.05+0.3*k:.2f});')
    # brand chip during body
    if b.get("chip"):
        over.append(f'<div class="clip chipc" data-start="{hook_end}" data-duration="{round(outro_start-hook_end,3)}" data-track-index="6">'
                    f'<div class="chip" id="chip">{esc(b["chip"])}</div></div>')
    # outro CTA
    if outro_start < T:
        over.append(f'<div class="clip cta" data-start="{outro_start}" data-duration="{round(T-outro_start,3)}" data-track-index="6">'
                    f'<div class="ctabox" id="ctabox"><div class="pill">FOLLOW {esc(b["handle"])}</div>'
                    f'<div class="ctatext">{esc(b["cta"])}</div></div></div>')
        tl.append(f'tl.fromTo("#ctabox",{{y:80,opacity:0}},{{y:0,opacity:1,duration:0.3,ease:"back.out(2)"}},{outro_start+0.1:.3f});')

    # ---------- optional burned captions (2 words / cluster) ----------
    if cfg.get("captions_burn"):
        n = max(1, int(e["caption_words"]))
        clusters, cur = [], []
        for w in words:
            if cur and (len(cur) >= n or w["sent"] != cur[0]["sent"]):
                clusters.append(cur); cur = []
            cur.append(w)
        if cur:
            clusters.append(cur)
        for k, c in enumerate(clusters):
            st = c[0]["start"]
            en = clusters[k + 1][0]["start"] if k + 1 < len(clusters) and clusters[k + 1][0]["sent"] == c[0]["sent"] else c[-1]["end"] + 0.1
            du = round(max(0.2, en - st), 3)
            txt = " ".join(x["word"] for x in c).strip(",.;:")
            over.append(f'<div class="clip capc" data-start="{st:.3f}" data-duration="{du}" data-track-index="7">'
                        f'<div class="cap" id="cap{k}">{esc(txt)}</div></div>')
            tl.append(f'tl.fromTo("#cap{k}",{{scale:0.8,opacity:0}},{{scale:1,opacity:1,duration:0.15,ease:"back.out(3)"}},{st:.3f});')

    # ---------- audio ----------
    audio = [f'<audio id="vo" src="assets/voice.wav" data-start="0" data-duration="{T}" data-track-index="9" data-volume="{cfg.get('vo_volume', 0.79)}"></audio>']
    if cfg.get("bgm") and cfg.get("bgm_path") and Path(cfg["bgm_path"]).exists():
        bgm = A / "bgm.wav"
        L = cfg["loudness"]
        run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1", "-i", cfg["bgm_path"], "-t", f"{T}", "-af",
             f"loudnorm=I={L['I']}:TP={L['TP']},afade=t=out:st={max(T-1.0,0):.2f}:d=1.0", "-ar", "48000", "-ac", "2", str(bgm)])
        vol = round(10 ** (cfg["bgm_volume_db"] / 20), 4)
        audio.append(f'<audio id="bgm" src="assets/bgm.wav" data-start="0" data-duration="{T}" data-track-index="10" data-volume="{vol}"></audio>')
    elif cfg.get("bgm"):
        notes.append("bgm=true but bgm_path missing -> rendered without music")

    css = (REPO / "templates" / "hinton.css").read_text(encoding="utf-8")
    css = (css.replace("__ACCENT__", b["accent"]).replace("__BG__", b["bg"]).replace("__BG2__", b["bg2"])
              .replace("__ALERT__", b["alert"]))
    doc = f"""<!doctype html>
<html lang="vi"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width={W}, height={H}"/>
<title>{esc(cfg['job_id'])}</title>
<script src="assets/gsap.min.js"></script>
<style>
{css}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-width="{W}" data-height="{H}" data-duration="{T}" data-fps="{cfg['fps']}">
<div class="bgfill"></div>
{chr(10).join(body)}
{chr(10).join(cards)}
{chr(10).join(pres_html)}
{chr(10).join(over)}
{chr(10).join(audio)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tl)}
window.__timelines["main"] = tl;
</script>
</body></html>
"""
    (hf_dir / "index.html").write_text(doc, encoding="utf-8")
    log.info("HyperFrames project written: %s (%d shots, %d tweens)", hf_dir / "index.html", len(plan["shots"]), len(tl))
    return hf_dir / "index.html"
