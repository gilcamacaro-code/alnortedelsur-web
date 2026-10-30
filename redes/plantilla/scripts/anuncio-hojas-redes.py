import numpy as np, math
from PIL import Image, ImageDraw, ImageFont, ImageOps
W,H=1080,1350
F="/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
f=lambda s: ImageFont.truetype(F,s)
YEL=(255,199,44); PD=(38,10,64); PL=(104,38,150); WH=(255,255,255)
ys=np.linspace(0,1,H)[:,None,None]
g=np.array(PD,float)+(np.array(PL,float)-np.array(PD,float))*ys
im=Image.fromarray(np.repeat(g,W,axis=1).astype(np.uint8)).convert("RGBA")
d=ImageDraw.Draw(im)
def ctext(txt,y,size,fill=WH,stroke=0,maxw=1000):
    s=size; ft=f(s)
    while ft.getlength(txt)>maxw and s>20: s-=2; ft=f(s)
    d.text((W//2+3,y+4),txt,font=ft,fill=(0,0,0,150),anchor="mt",stroke_width=stroke)
    d.text((W//2,y),txt,font=ft,fill=fill,anchor="mt",stroke_width=stroke,stroke_fill=(30,8,50))
ctext("HOJAS PARA",40,104,YEL,3)
ctext("HALLACAS Y TAMALES",150,76,WH,3)
def fit(p,w,h):
    i=Image.open(p).convert("RGB"); return ImageOps.fit(i,(w,h),Image.LANCZOS,centering=(.5,.35))
def rr(i,r=34):
    m=Image.new("L",i.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,i.width,i.height),r,fill=255)
    o=i.convert("RGBA"); o.putalpha(m); return o
pw,ph=480,520
a=rr(fit("h/a.jpg",pw,ph)); b=rr(fit("h/b.jpg",pw,ph))
# slight tilt
a=a.rotate(3,expand=True,resample=Image.BICUBIC); b=b.rotate(-3,expand=True,resample=Image.BICUBIC)
im.alpha_composite(a,(28,265)); im.alpha_composite(b,(1080-28-b.width,275))
# badge
bw,bh=860,150
bx,by=(W-bw)//2,805
d.rounded_rectangle((bx,by,bx+bw,by+bh),75,fill=YEL)
d.text((W//2,by+50),"PRECIOS ESPECIALES",font=f(66),fill=PD,anchor="mm")
d.text((W//2,by+112),"cuanta más llevas, mejor precio",font=f(38),fill=PL,anchor="mm")
ctext("Hojas de plátano · Hoja de choclo",985,50,YEL,2)
ctext("para hallacas, tamales, pasteles y humitas",1050,36,WH,0)
d.rounded_rectangle((90,1125,990,1205),40,fill=WH)
d.text((W//2,1165),"WhatsApp 671 339 005 · ¡Te lo apartamos!",font=f(38),fill=PD,anchor="mm")
ctext("Mercado de Ruzafa · puestos 213-220 · L-S 8:30-15:00",1235,34,WH,0)
ctext("ALNORTEDELSUR",1285,36,YEL,0)
im.convert("RGB").save("w/anuncio_hojas_1080x1350.jpg",quality=93)
