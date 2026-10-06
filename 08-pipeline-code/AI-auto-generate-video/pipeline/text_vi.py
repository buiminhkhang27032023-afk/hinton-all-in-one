"""Vietnamese script helpers: normalisation, sentence split, syllable count, keyword guess."""
import re, unicodedata

SENT_END = re.compile(r"(?<=[\.\!\?…])\s+")


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\r", "")
    # drop comment lines (# ...) so writers can annotate script.txt
    lines = [l for l in text.split("\n") if not l.strip().startswith("#")]
    text = " ".join(l.strip() for l in lines if l.strip())
    text = re.sub(r"\s+", " ", text).strip()
    return text


def split_sentences(text: str, max_syll: int = 40):
    """Split on . ! ? … ; very long sentences are split again on , ; :"""
    out = []
    for s in SENT_END.split(text):
        s = s.strip()
        if not s:
            continue
        if count_syllables(s) <= max_syll:
            out.append(s); continue
        parts, cur = re.split(r"(?<=[,;:])\s+", s), ""
        for p in parts:
            cand = (cur + " " + p).strip()
            if cur and count_syllables(cand) > max_syll:
                out.append(cur); cur = p
            else:
                cur = cand
        if cur:
            out.append(cur)
    return out


def words(text: str):
    return [w for w in text.split() if re.search(r"\w", w)]


def count_syllables(text: str) -> int:
    """Vietnamese ≈ one syllable per space-separated token (Latin brand names count 1)."""
    return len(words(text))


def digits_present(text: str):
    return re.findall(r"\d+", text)


# --- keyword guess for stock search (MoneyPrinterTurbo-style, without LLM) ---
VI_EN = {
    "trí tuệ nhân tạo": "artificial intelligence", "ai": "artificial intelligence",
    "protein": "protein molecule", "tế bào": "cell biology microscope", "hóa học": "chemistry lab",
    "nhà khoa học": "scientist laboratory", "khoa học": "science laboratory", "phòng thí nghiệm": "laboratory",
    "giải thưởng": "award ceremony", "nobel": "nobel prize", "máy tính": "computer", "lập trình": "coding programmer",
    "dữ liệu": "data center", "điện thoại": "smartphone", "robot": "robot", "chip": "microchip",
    "thuốc": "medicine pills", "kháng sinh": "antibiotics bacteria", "nhựa": "plastic waste", "enzyme": "enzyme molecule",
    "bệnh viện": "hospital", "bác sĩ": "doctor", "xe tự lái": "self driving car", "ô tô": "car", "tiền": "money",
    "công ty": "office business", "thị trường": "stock market", "nghiên cứu": "research scientist",
    "học sinh": "students classroom", "giáo dục": "education classroom", "video": "video editing", "hình ảnh": "photography",
    "âm nhạc": "music studio", "internet": "internet network", "mạng xã hội": "social media phone",
    "bảo mật": "cyber security", "hacker": "hacker", "điện": "electricity", "năng lượng": "energy power plant",
}


VN_SYL = re.compile(r"^(ngh|ng|nh|ch|gh|gi|kh|ph|qu|th|tr|[bcdghklmnpqrstvx])?[aeiouy]{1,3}(ch|nh|ng|c|m|n|p|t)?$")


def is_foreign_token(w: str) -> bool:
    """True for Latin brand/product names (AlphaFold, Google, Baker), False for ASCII Vietnamese syllables (Theo, Khoa)."""
    if re.search(r"[^\x00-\x7F]", w):
        return False
    if re.search(r"[a-z][A-Z]|\d", w):
        return True
    return not VN_SYL.match(w.lower())


def guess_keywords(sentence: str, n: int = 2):
    s = sentence.lower()
    kws = []
    for vi, en in sorted(VI_EN.items(), key=lambda kv: -len(kv[0])):
        if re.search(r"(?<!\w)" + re.escape(vi) + r"(?!\w)", s) and en not in kws:
            kws.append(en)
    # Latin-only tokens with capitals (brand / product names) are good search terms too
    for w in re.findall(r"\b[A-Z][A-Za-z0-9\-]{2,}\b", sentence):
        if is_foreign_token(w) and w.lower() not in [k.lower() for k in kws]:
            kws.insert(0, w)
    if not kws:
        kws = ["technology abstract"]
    return kws[:n]


def salient_phrase(ws, max_words=5):
    """Pick a short on-screen phrase from a list of words (for text cards)."""
    clean = [re.sub(r"[\"“”()]", "", w) for w in ws]
    clean = [w for w in clean if w]
    if len(clean) <= max_words:
        return " ".join(clean).strip(" ,.;:")
    # prefer a window containing capitalised / numeric words
    best, best_score = 0, -1
    for i in range(0, len(clean) - max_words + 1):
        win = clean[i:i + max_words]
        score = sum(2 for w in win if w[:1].isupper()) + sum(1 for w in win if len(w) > 4)
        if score > best_score:
            best, best_score = i, score
    return " ".join(clean[best:best + max_words]).strip(" ,.;:")
