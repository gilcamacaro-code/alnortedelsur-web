from PIL import Image, ImageDraw, ImageFont, ImageOps
F="/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
YEL=(255,199,44); PD=(38,10,64); PL=(104,38,150); WH=(255,255,255); LIL=(243,235,250)
GROUPS=[("LA BASE MORADA",["Maíz morado en grano","Harina de maíz morado","Flor de Jamaica","Panela"]),
        ("LOS AROMAS",["Canela en rama","Clavo de olor","Pimienta de olor","Hierba luisa","Cedrón","Anís estrella"]),
        ("LAS FRUTAS",["Mortiño","Mora (pulpa)","Lulo / naranjilla"])]
def build(Wpx,Hpx,Hd,photo,dark,out):
    K=Wpx/1080; S=lambda v:int(v*K); f=lambda s:ImageFont.truetype(F,max(8,int(s*K)))
    bg=PD if dark else WH
    im=Image.new("RGB",(Wpx,Hpx),bg); d=ImageDraw.Draw(im)
    if dark:
        import numpy as np
        ys=np.linspace(0,1,Hpx)[:,None,None]; g=np.array(PD,float)+(np.array(PL,float)-np.array(PD,float))*ys
        im=Image.fromarray(np.repeat(g,Wpx,axis=1).astype(np.uint8)); d=ImageDraw.Draw(im)
    else:
        d.rectangle((0,0,Wpx,S(235)),fill=PD)
    tc=YEL
    d.text((Wpx//2,S(30)),"TODOS LOS INGREDIENTES",font=f(70),fill=tc,anchor="mt")
    d.text((Wpx//2,S(125)),"PARA TU COLADA MORADA",font=f(70),fill=WH,anchor="mt")
    d.text((Wpx//2,S(200)),"Tradición ecuatoriana · 2 de noviembre",font=f(34),fill=(230,220,245),anchor="mt")
    y=255
    if photo:
        ph=Image.open("w/img.jpg").convert("RGB"); ph=ImageOps.fit(ph,(S(1000),S(photo)),Image.LANCZOS,centering=(.5,.5))
        m=Image.new("L",ph.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,ph.width,ph.height),S(34),fill=255)
        im.paste(ph,(S(40),S(y)),m); y+=photo+25
    lh=62 if Hd<1400 else 54
    for name,items in GROUPS:
        rows=(len(items)+1)//2; ch=84+rows*lh+16
        d.rounded_rectangle((S(40),S(y),S(1040),S(y+ch)),S(34),fill=(255,255,255) if dark else LIL)
        d.rounded_rectangle((S(40),S(y),S(1040),S(y+70)),S(34),fill=YEL)
        d.rectangle((S(40),S(y+40),S(1040),S(y+70)),fill=YEL)
        d.text((S(540),S(y+36)),name,font=f(40),fill=PD,anchor="mm")
        for i,t in enumerate(items):
            cx=S(75) if i%2==0 else S(550); cy=S(y+70+22+(i//2)*lh+lh//2-4)
            d.ellipse((cx,cy-S(9),cx+S(18),cy+S(9)),fill=PL)
            d.text((cx+S(34),cy),t,font=f(33),fill=PD,anchor="lm")
        y+=ch+18
    d.text((Wpx//2,S(y+8)),"Y la guagua de pan para acompañar",font=f(38),fill=YEL if dark else PL,anchor="mt")
    fy=Hd-175
    if not dark: d.rectangle((0,S(fy),Wpx,Hpx),fill=PD)
    d.text((Wpx//2,S(fy+22)),"WhatsApp 671 339 005 · ¡Te lo apartamos!",font=f(42),fill=WH,anchor="mt")
    d.text((Wpx//2,S(fy+88)),"Mercado de Ruzafa · puestos 213-220 · lunes a sábado 8:30-15:00",font=f(30),fill=WH,anchor="mt")
    d.text((Wpx//2,S(fy+130)),"ALNORTEDELSUR",font=f(32),fill=YEL,anchor="mt")
    if out.endswith(".pdf"): im.save(out,resolution=300.0)
    else: im.save(out,quality=93)
build(2480,3508,1527,300,False,"w/colada_ingredientes_A4.pdf")
build(1080,1350,1350,0,True,"w/colada_ingredientes_1080x1350.jpg")
Image.open("w/colada_ingredientes_1080x1350.jpg").save("w/c_prev.png")
