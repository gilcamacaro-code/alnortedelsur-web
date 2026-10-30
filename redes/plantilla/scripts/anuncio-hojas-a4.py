from PIL import Image, ImageDraw, ImageFont, ImageOps
BW,BH=1080,1527; K=2480/1080
W,H=2480,3508
F="/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
f=lambda s: ImageFont.truetype(F,int(s*K))
YEL=(255,199,44); PD=(38,10,64); PL=(104,38,150); WH=(255,255,255)
im=Image.new("RGB",(W,H),WH); d=ImageDraw.Draw(im)
S=lambda v:int(v*K)
# top and bottom purple bands (moderate ink)
d.rectangle((0,0,W,S(250)),fill=PD)
def ct(txt,y,size,fill,maxw=1000,anchor="mt"):
    s=size; ft=f(s)
    while ft.getlength(txt)>maxw*K and s>20: s-=2; ft=f(s)
    d.text((W//2,S(y)),txt,font=ft,fill=fill,anchor=anchor)
ct("HOJAS PARA",28,104,YEL)
ct("HALLACAS Y TAMALES",150,70,WH)
def fit(p,w,h):
    i=Image.open(p).convert("RGB"); return ImageOps.fit(i,(S(w),S(h)),Image.LANCZOS,centering=(.5,.35))
def rr(i,r=30):
    m=Image.new("L",i.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,i.width,i.height),S(r),fill=255)
    o=i.convert("RGBA"); o.putalpha(m); return o
pw,ph=490,640
a=rr(fit("h/a.jpg",pw,ph)); b=rr(fit("h/b.jpg",pw,ph))
canvas=im.convert("RGBA")
for img,x in ((a,40),(b,550)):
    sh=Image.new("RGBA",img.size,(0,0,0,70)); sh.putalpha(img.getchannel("A").point(lambda v:v*70//255))
    canvas.alpha_composite(sh,(S(x)+S(5),S(300)+S(7)))
    canvas.alpha_composite(img,(S(x),S(300)))
im=canvas.convert("RGB"); d=ImageDraw.Draw(im)
bx0,bx1,by0,by1=S(60),S(1020),S(975),S(1150)
d.rounded_rectangle((bx0,by0,bx1,by1),S(88),fill=YEL,outline=PD,width=S(5))
d.text((W//2,S(1040)),"PRECIOS ESPECIALES",font=f(76),fill=PD,anchor="mm")
d.text((W//2,S(1112)),"cuanta más llevas, mejor precio",font=f(40),fill=PL,anchor="mm")
ct("Hojas de plátano · Hoja de choclo",1175,54,PL)
ct("para hallacas, tamales, pasteles y humitas",1243,36,PD)
d.rectangle((0,S(1320),W,H),fill=PD)
ct("WhatsApp 671 339 005 · ¡Te lo apartamos!",1345,46,WH)
ct("Mercado de Ruzafa · puestos 213-220 · lunes a sábado 8:30-15:00",1420,34,WH)
ct("ALNORTEDELSUR",1470,36,YEL)
im.save("w/anuncio_hojas_A4.png")
im.save("w/anuncio_hojas_A4.pdf",resolution=300.0)
im.resize((620,877)).save("w/a4_prev.png")
