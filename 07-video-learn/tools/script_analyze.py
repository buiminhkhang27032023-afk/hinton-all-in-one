#!/usr/bin/env python3
"""Script (lời thoại) metrics from <id>_transcript.json. Usage: script_analyze.py <mp4>...
Writes <id>_script.json + <id>_script.md. Labels: [ĐO-TR] measured on whisper-small transcript (ASR errors possible)."""
import sys, os, json, re, statistics as st
def syl_en(w):
    w=re.sub(r'[^a-z]','',w.lower())
    if not w: return 0
    g=re.findall(r'[aeiouy]+',w); n=len(g)
    if w.endswith('e') and n>1 and not w.endswith(('le','ee','ye')): n-=1
    return max(1,n)
def syl_id(w):
    w=re.sub(r'[^a-z]','',w.lower()); return max(1,len(re.findall(r'[aeiou]+',w))) if w else 0
def syl_count(text,lang):
    if lang=='zh': return len(re.findall(r'[\u4e00-\u9fff]',text))
    toks=re.findall(r"[\w'’-]+",text)
    if lang=='vi': return sum(1 for t in toks if not t.isdigit()) + sum(len(t) for t in toks if t.isdigit())  # 1 token = 1 âm tiết; số đọc ~1/chữ số
    if lang=='id': return sum(syl_id(t) for t in toks)
    return sum(syl_en(t) if not t.isdigit() else len(t) for t in toks)
def word_count(text,lang):
    if lang=='zh': return len(re.findall(r'[\u4e00-\u9fff]',text))
    return len(re.findall(r"[\w'’-]+",text))
PAT={
 'en':dict(pivot=r"\bbut\b|\bhowever\b|here'?s the thing|the problem is|turns out|until now|\bactually\b|\binstead\b|\bexcept\b|the catch|plot twist|\bwait\b",
           listing=r"\bfirst(ly)?\b|\bsecond(ly)?\b|\bthird\b|\bnumber (one|two|three|\d)\b|\bstep (one|two|three|\d)\b|\bnext\b|\bfinally\b|\blast(ly)?\b|\bthe last\b",
           loop=r"i'?ll show you|here'?s how|let me show|stay (till|until)|wait (for|till)|in a second|by the end|keep watching|watch (till|until)|the best part|but first|you won'?t believe",
           address=r"\byou\b|\byour\b|\byou'?re\b",
           cta=r"\bfollow\b|\bcomment\b|\blink\b|\bbio\b|\bsave\b|\bshare\b|\bsubscribe\b|\bdm\b|\blike\b",
           proof=r"\blook\b|\bwatch\b|\bhere\b|\bthis is\b|\bcheck (this|it) out\b|\bsee\b"),
 'vi':dict(pivot=r"\bnhưng\b|tuy nhiên|thế nhưng|thật ra|thực ra|vấn đề là|điều đáng nói|hóa ra|hoá ra|bất ngờ|ngược lại|chứ không|thay vì",
           listing=r"thứ nhất|thứ hai|thứ ba|đầu tiên|tiếp theo|cuối cùng|bước \w+|số một|số hai|số \d|\bmột là\b|\bhai là\b|công cụ thứ",
           loop=r"cuối video|mình sẽ chỉ|mình sẽ hướng dẫn|xem đến cuối|bí mật|điều thú vị|chút nữa|lát nữa|ngay sau đây|các bạn sẽ thấy|cách làm như sau",
           address=r"các bạn|\bbạn\b|anh em|mọi người|anh chị",
           cta=r"follow|theo dõi|comment|bình luận|lưu lại|\blưu\b|chia sẻ|\blink\b|\bbio\b|thả tim|đăng ký|ib|inbox|nhắn tin",
           proof=r"các bạn thấy|như các bạn thấy|đây là|nhìn nè|xem nè|thử nè|kết quả"),
 'id':dict(pivot=r"\btapi\b|\bternyata\b|masalahnya|\bpadahal\b|\bnamun\b|\bjustru\b|\bbukan\b",
           listing=r"\bpertama\b|\bkedua\b|\bketiga\b|\bnomor\b|\blangkah\b|\bterakhir\b|\bselanjutnya\b",
           loop=r"sampai akhir|nanti gw|gw kasih tau|caranya|rahasia",
           address=r"\blu\b|\blo\b|\bkalian\b|\bkamu\b|\banda\b",
           cta=r"\bfollow\b|\bkomen\b|\bkomentar\b|\blink\b|\bbio\b|\bsave\b|\bshare\b|\bdm\b",
           proof=r"\bini dia\b|\bliat\b|\blihat\b|\bcontohnya\b"),
 'zh':dict(pivot=r"但是|不过|其实|然而|没想到|结果",listing=r"第一|第二|第三|首先|其次|最后|步骤",loop=r"最后|等会|接下来|看到最后",address=r"你|大家|朋友们",cta=r"关注|点赞|评论|收藏|转发|三连",proof=r"你看|看这个|效果"),
}
for f in sys.argv[1:]:
    d=os.path.dirname(f); vid=os.path.basename(f)[:-4]; tp=f'{d}/{vid}_transcript.json'
    if not os.path.exists(tp): print('NO TRANSCRIPT',f); continue
    T=json.load(open(tp)); L=T['lang']; S=T['segments']; P=PAT.get(L,PAT['en'])
    HALL=re.compile(r'subscribe cho kênh|Ghiền Mì Gõ|La La School|bỏ lỡ những video hấp dẫn|Cảm ơn các bạn đã theo dõi|请不吝点赞|字幕由|Amara\.org|thanks for watching',re.I)
    S=[x for x in S if not HALL.search(x['text'])]
    # lọc lặp do nhạc nền (whisper --nt): đoạn ngắn lặp >=3 lần liên tiếp
    def _k(t): return re.sub(r'[^\w]','',t.lower())
    keep=[]
    for i,x in enumerate(S):
        k=_k(x['text']); run=[j for j in range(max(0,i-2),min(len(S),i+3)) if _k(S[j]['text'])==k]
        if len(x['text'].split())<=4 and len(run)>=3: continue
        keep.append(x)
    S=keep
    info={}
    ip=f'{d}/{vid}.info.json'
    if os.path.exists(ip):
        I=json.load(open(ip)); info=dict(title=I.get('title'),views=I.get('view_count'),likes=I.get('like_count'),upload_date=I.get('upload_date'),url=I.get('webpage_url'))
    words=[w for s in S for w in s['words']]
    full=' '.join(s['text'] for s in S)
    DUR=T['duration']
    if not words:
        json.dump(dict(id=vid,error='no speech'),open(f'{d}/{vid}_script.json','w')); print('NOSPEECH',f); continue
    t_first=words[0]['s']; t_last=words[-1]['e']; span=max(0.1,t_last-t_first)
    # speaking time excluding gaps >0.6s between words
    gaps=[(words[i]['s']-words[i-1]['e']) for i in range(1,len(words))]
    speak=span-sum(g for g in gaps if g>0.6)
    nw=word_count(full,L); ns=syl_count(full,L)
    hook3=' '.join(w['w'].strip() for w in words if w['s']<3.0).strip()
    hook5=' '.join(w['w'].strip() for w in words if w['s']<5.0).strip()
    # sentences: split on . ? ! … and segment boundaries with gap
    sents=[x.strip() for seg in S for x in re.split(r'(?<=[\.\?\!…。？！,，])\s+' if False else r'(?<=[\.\?\!…。？！])\s*',seg['text']) if x.strip()]
    slen=[word_count(x,L) for x in sents]
    first_sent=sents[0] if sents else ''
    # sentence end time of first sentence
    def cnt(p,txt): return len(re.findall(p,txt,re.I))
    last15=' '.join(s['text'] for s in S if s['start']>=DUR*0.85)
    first15=' '.join(s['text'] for s in S if s['start']<DUR*0.15)
    piv_times=[]
    for s in S:
        for m in re.finditer(P['pivot'],s['text'],re.I):
            piv_times.append(round(s['start'],1))
    cov=sum(x['end']-x['start'] for x in S)/max(DUR,1)
    M=dict(id=vid,lang=L,speech_coverage=round(cov,2),duration=round(DUR,2),speech_start=t_first,speech_end=t_last,speech_span=round(span,2),speaking_time=round(speak,2),
           words=nw,syllables=ns,wps=round(nw/span,2),sps=round(ns/span,2),sps_speaking=round(ns/max(speak,0.1),2),
           long_gaps_ge0_6s=sum(1 for g in gaps if g>=0.6),
           hook_0_3s=hook3,hook_0_3s_words=word_count(hook3,L),hook_0_5s=hook5,first_sentence=first_sent,first_sentence_words=word_count(first_sent,L),
           n_sentences=len(sents),sent_words_median=st.median(slen) if slen else None,sent_words_p90=sorted(slen)[int(0.9*(len(slen)-1))] if slen else None,
           questions=full.count('?')+full.count('？'),
           pivots=cnt(P['pivot'],full),pivot_times=piv_times,listing=cnt(P['listing'],full),open_loops=cnt(P['loop'],full),
           address_per_min=round(cnt(P['address'],full)/(span/60),1),cta_in_last15=cnt(P['cta'],last15),cta_total=cnt(P['cta'],full),
           proof_markers=cnt(P['proof'],full),numbers=len(re.findall(r'\d+[\d\.,%]*',full)),
           last_sentence=sents[-1] if sents else '',info=info)
    json.dump(M,open(f'{d}/{vid}_script.json','w'),ensure_ascii=False,indent=1)
    md=[f'# Kịch bản — {vid} ({os.path.basename(d)})','',
        f"Nhãn: **[ĐO-TR]** đo trên transcript whisper-small (có thể sai chính tả/tên riêng). Ngôn ngữ: {L}. Nguồn: {info.get('url','')} · view: {info.get('views')} · tiêu đề: {(info.get('title') or '')[:120]!r}",'',
        '## Số liệu','',
        f"- Thời lượng {DUR:.1f}s · giọng bắt đầu {t_first:.2f}s · kết thúc {t_last:.2f}s",
        f"- {nw} từ · {ns} âm tiết · **{M['wps']} từ/s · {M['sps']} âm tiết/s** (trên khoảng nói), {M['sps_speaking']} âm tiết/s (bỏ khoảng ngừng >0,6s; {M['long_gaps_ge0_6s']} khoảng)",
        f"- Câu: {len(sents)} câu, trung vị {M['sent_words_median']} từ/câu, p90 {M['sent_words_p90']}",
        f"- Hook 0–3s ({M['hook_0_3s_words']} từ): “{hook3}”",
        f"- Hook 0–5s: “{hook5}”",
        f"- Câu đầu ({M['first_sentence_words']} từ): “{first_sent}”",
        f"- Câu cuối: “{M['last_sentence']}”",
        f"- Đếm: câu hỏi {M['questions']} · từ bẻ lái {M['pivots']} (ở giây {piv_times}) · đánh số/liệt kê {M['listing']} · vòng mở {M['open_loops']} · gọi người xem {M['address_per_min']}/phút · CTA ở 15% cuối {M['cta_in_last15']} (tổng {M['cta_total']}) · chỉ dấu demo/bằng chứng {M['proof_markers']} · con số {M['numbers']}",
        '','## Transcript theo đoạn (mốc giây, % thời lượng)','']
    for s in S: md.append(f"- [{s['start']:.1f}–{s['end']:.1f}s | {100*s['start']/DUR:.0f}%] {s['text']}")
    md+=['','## Beat (điền tay)','','(xem SO-TAY-KICH-BAN.md)']
    open(f'{d}/{vid}_script.md','w').write('\n'.join(md))
    print('OK',f,M['sps'],M['hook_0_3s_words'])
