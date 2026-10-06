# Tạo khung điện thoại PNG 1080x1920 (màn hình trong suốt 780x1690 tại 150,115)
from PIL import Image, ImageDraw
W,H=1080,1920; sx,sy,sw,sh=150,115,780,1690
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
d.rounded_rectangle([sx-30,sy-30,sx+sw+30,sy+sh+30],radius=110,fill=(20,20,22,255),outline=(90,90,95,255),width=6)
m=Image.new('L',(W,H),0); ImageDraw.Draw(m).rounded_rectangle([sx,sy,sx+sw,sy+sh],radius=80,fill=255)
im.putalpha(Image.eval(Image.composite(Image.new('L',(W,H),0),im.split()[3],m),lambda v:v))
d=ImageDraw.Draw(im); d.rounded_rectangle([W//2-90,sy+18,W//2+90,sy+58],radius=20,fill=(0,0,0,255))  # dynamic island
im.save('phone_frame.png')
