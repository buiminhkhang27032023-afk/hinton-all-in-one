#!/usr/bin/env python3
"""Biểu đồ cột động (fallback khi không có chart chính thức). Usage:
bar_chart.py out.mp4 "Tiêu đề" "Nhãn1:giá trị1,Nhãn2:giá trị2,..." [đơn vị] [highlight_label]
Ra mp4 1080x960, 30fps, 3s: cột mọc 0→100% trong 0,8s (ease-out), số chạy theo. Cột highlight màu vàng #F5C518, còn lại xám."""
import sys, subprocess
from PIL import Image, ImageDraw, ImageFont
out,title,data=sys.argv[1:4]; unit=sys.argv[4] if len(sys.argv)>4 else ''; hl=sys.argv[5] if len(sys.argv)>5 else None
F='/usr/share/fonts/truetype/sand-box/google/Be Vietnam Pro/BeVietnamPro-Bold.ttf'
items=[(k,float(v)) for k,v in (x.split(':') for x in data.split(','))]
W,H,FPS,DUR=1080,960,30,3.0; mx=max(v for _,v in items)
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-pix_fmt','yuv420p','-c:v','libx264','-crf','18',out],stdin=subprocess.PIPE)
fT,fL,fV=ImageFont.truetype(F,54),ImageFont.truetype(F,34),ImageFont.truetype(F,40)
n=len(items); gap=40; bw=(W-160-gap*(n-1))//n; base=H-140; top=270
for i in range(int(FPS*DUR)):
    t=min(1,i/(FPS*0.8)); e=1-(1-t)**3
    im=Image.new('RGB',(W,H),'#111114'); d=ImageDraw.Draw(im)
    d.text((80,70),title,font=fT,fill='white')
    for j,(k,v) in enumerate(items):
        x=80+j*(bw+gap); h=(base-top)*v/mx*e; c='#F5C518' if (k==hl or (hl is None and v==mx)) else '#6B6B75'
        d.rounded_rectangle([x,base-h,x+bw,base],radius=12,fill=c)
        val=f'{v*e:.1f}'.rstrip('0').rstrip('.')+unit
        d.text((x+bw/2,base-h-12),val,font=fV,fill='white',anchor='md')
        d.text((x+bw/2,base+20),k,font=fL,fill='#BBBBBB',anchor='ma')
    p.stdin.write(im.tobytes())
p.stdin.close(); p.wait(); print(out)
