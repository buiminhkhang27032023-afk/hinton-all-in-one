import sys,glob,os
from PIL import Image,ImageDraw
out,sheetp,hookp=sys.argv[1:4]
fr=sorted(glob.glob(out+'/1fps/*.jpg'))
n=len(fr); k=min(24,n)
idx=[round(i*(n-1)/(k-1)) for i in range(k)] if k>1 else [0]
def tile(paths,labels,cols,p):
    ims=[Image.open(x).convert('RGB') for x in paths]
    w,h=ims[0].size; tw=240; th=int(h*tw/w)
    rows=(len(ims)+cols-1)//cols
    S=Image.new('RGB',(tw*cols,(th+16)*rows),'white'); d=ImageDraw.Draw(S)
    for i,(im,l) in enumerate(zip(ims,labels)):
        S.paste(im.resize((tw,th)),((i%cols)*tw,(i//cols)*(th+16))); d.text(((i%cols)*tw+3,(i//cols)*(th+16)+th+2),l,fill='black')
    S.save(p,quality=85)
cols=8 if Image.open(fr[0]).size[0]<Image.open(fr[0]).size[1] else 6
tile([fr[i] for i in idx],[f"t={i}s" for i in idx],cols,sheetp)
hk=sorted(glob.glob(out+'/hook/*.jpg'))
tile(hk,[f"t={i*0.25:.2f}s" for i in range(len(hk))],6,hookp)
