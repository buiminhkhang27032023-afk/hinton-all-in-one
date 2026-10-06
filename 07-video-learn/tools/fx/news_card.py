#!/usr/bin/env python3
"""Thẻ 'dẫn chứng' dựng lại (khi không có ảnh chụp dùng được, hoặc nguồn tiếng Trung cần Việt hoá).
Usage: news_card.py out.png "Nguồn (vd: OpenAI Blog)" "Tiêu đề tiếng Việt ngắn" "03/10/2026" [accent_hex]
Ra PNG 1080x960 (nửa trên split) nền tối, thẻ trắng bo góc. Ghi rõ nguồn trên thẻ."""
import sys, textwrap
from PIL import Image, ImageDraw, ImageFont
out,src,title,date=sys.argv[1:5]; acc=sys.argv[5] if len(sys.argv)>5 else '#F5C518'
F='/usr/share/fonts/truetype/sand-box/google/Be Vietnam Pro/BeVietnamPro-Bold.ttf'
W,H=1080,960; im=Image.new('RGB',(W,H),'#111114'); d=ImageDraw.Draw(im)
d.rounded_rectangle([80,180,W-80,H-180],radius=36,fill='white')
d.rectangle([80,180,96,H-180],fill=acc)
d.text((130,215),src.upper(),font=ImageFont.truetype(F,34),fill='#666')
y=285
for line in textwrap.wrap(title,26)[:4]:
    d.text((130,y),line,font=ImageFont.truetype(F,60),fill='#111'); y+=78
d.text((130,H-250),date,font=ImageFont.truetype(F,30),fill='#888')
im.save(out); print(out)
