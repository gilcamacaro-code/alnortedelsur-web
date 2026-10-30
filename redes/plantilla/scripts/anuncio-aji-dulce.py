from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
F="/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
YEL=(255,199,44); PD=(38,10,64); PL=(104,38,150); WH=(255,255,255)
PHOTO="/mnt/user-data/uploads/alnortedelsur-web/redes/fotos/aji1.jpg"
def build(Wpx,Hpx,Hd,dark,out):
    K=Wpx/1080; S=lambda v:int(v*K); f=lambda s:ImageFont.truetype(F,max(8,int(s*K)))
    if dark:
        ys=np.linspace(0,1,Hpx)[:,None,None]; g=np.array(PD,float)+(np.array(PL,float)-np.array(PD,float))*ys
        im=Image.fromarray(np.repeat(g,Wpx,axis=1).astype(np.uint8))
    else:
        im=Image.new("RGB",(Wpx,Hpx),WH)
    d=ImageDraw.Draw(im)
    if not dark: d.rectangle((0,0,Wpx,S(250)),fill=PD)
    d.text((Wpx//2,S(30)),"¡LLEGÓ EL",font=f(80),fill=YEL,anchor="mt")
    d.text((Wpx//2,S(125)),"AJÍ DULCE!",font=f(110),fill=WH,anchor="mt")
    py=270; ph_h=620 if Hd<1400 else 800
    ph=ImageOps.fit(Image.open(PHOTO).convert("RGB"),(S(1000),S(ph_h)),Image.LANCZOS)
    m=Image.new("L",ph.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,ph.width,ph.height),S(40),fill=255)
    im.paste(ph,(S(40),S(py)),m)
    # badge over photo bottom
    by=py+ph_h-45
    d.rounded_rectangle((S(110),S(by),S(970),S(by+120)),S(60),fill=YEL,outline=PD if not dark else None,width=S(4))
    d.text((Wpx//2,S(by+60)),"DE TEMPORADA · FRESCO EN TIENDA",font=f(40),fill=PD,anchor="mm")
    y=by+150
    tc=WH if dark else PD
    d.text((Wpx//2,S(y)),"El alma del guiso de tus hallacas",font=f(46),fill=YEL if dark else PL,anchor="mt")
    d.text((Wpx//2,S(y+66)),"Llévatelo ahora y congélalo para diciembre",font=f(36),fill=tc,anchor="mt")
    fy=Hd-170
    if not dark: d.rectangle((0,S(fy),Wpx,Hpx),fill=PD)
    d.text((Wpx//2,S(fy+18)),"WhatsApp 671 339 005 · ¡Te lo apartamos!",font=f(42),fill=WH,anchor="mt")
    d.text((Wpx//2,S(fy+84)),"Mercado de Ruzafa · puestos 213-220 · lunes a sábado 8:30-15:00",font=f(30),fill=WH,anchor="mt")
    d.text((Wpx//2,S(fy+126)),"ALNORTEDELSUR",font=f(32),fill=YEL,anchor="mt")
    if out.endswith(".pdf"): im.save(out,resolution=300.0)
    else: im.save(out,quality=93)
build(1080,1350,1350,True,"w/aji_dulce_1080x1350.jpg")
build(2480,3508,1527,False,"w/aji_dulce_A4.pdf")
