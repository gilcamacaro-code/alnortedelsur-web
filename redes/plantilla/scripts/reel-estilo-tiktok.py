import sys, os, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
WD = sys.argv[1]  # working dir with img.jpg, pot/, pour/
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
YEL = (255, 199, 44)
WHITE = (255, 255, 255)
PURPLE_D = (38, 10, 64)
PURPLE_L = (104, 38, 150)

_fc = {}
def font(sz):
    sz = int(round(sz))
    if sz not in _fc:
        _fc[sz] = ImageFont.truetype(FONT, sz)
    return _fc[sz]

def ease_back(x):
    x = max(0.0, min(1.0, x))
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

def gradient():
    ys = np.linspace(0, 1, H)[:, None, None]
    a = np.array(PURPLE_D, float)[None, None, :]
    b = np.array(PURPLE_L, float)[None, None, :]
    g = a + (b - a) * ys
    return Image.fromarray(np.repeat(g, W, axis=1).astype(np.uint8))
BG = gradient()

photo = Image.open(os.path.join(WD, "img.jpg")).convert("RGB")
# blurred cover background from photo
s = H / photo.height
cover = photo.resize((int(photo.width * s), H), Image.LANCZOS)
cx = (cover.width - W) // 2
cover = cover.crop((cx, 0, cx + W, H)).filter(ImageFilter.GaussianBlur(28))
cover = Image.eval(cover, lambda v: int(v * 0.40))
PH_W, PH_H = 1080, 810
photo_fit = photo.resize((PH_W, PH_H), Image.LANCZOS)

def load_frames(d):
    fs = sorted(os.listdir(os.path.join(WD, d)))
    return [Image.open(os.path.join(WD, d, f)).convert("RGB") for f in fs]
POT = load_frames("pot")
POUR = load_frames("pour")

def rounded(img, r=40):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, img.width, img.height), r, fill=255)
    out = img.convert("RGBA"); out.putalpha(m)
    return out

def text_c(base, txt, y, size, fill=WHITE, t0=0.0, t=0.0, pop=True, stroke=0, maxw=1000):
    """Centered text with pop-in starting at t0."""
    k = ease_back((t - t0) / 0.28) if pop else 1.0
    if t < t0 or k <= 0:
        return
    sz = size
    f = font(sz)
    while f.getlength(txt) > maxw and sz > 20:
        sz -= 2; f = font(sz)
    f = font(max(8, sz * k)) if k != 1 else f
    w = f.getlength(txt)
    lay = Image.new("RGBA", (int(w) + 40, int(sz * 1.9 * max(k, .2)) + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.text((22, 22 + 5), txt, font=f, fill=(0, 0, 0, 150), stroke_width=stroke)
    d.text((20, 20), txt, font=f, fill=fill + (255,), stroke_width=stroke, stroke_fill=(30, 8, 50, 255))
    cxp = W // 2 - lay.width // 2
    cyp = int(y - (lay.height - 40) * (0.5 if pop else 0) + (0 if not pop else 0))
    base.alpha_composite(lay, (max(0, cxp), int(y)))

def pill(base, txt, y, size, t0, t, bg=YEL, fg=PURPLE_D):
    k = ease_back((t - t0) / 0.22)
    if t < t0:
        return
    f = font(size)
    w = int(f.getlength(txt)) + 90
    h = int(size * 1.9)
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((0, 0, w, h), h // 2, fill=bg + (255,))
    d.text((w // 2, h // 2 + 2), txt, font=f, fill=fg + (255,), anchor="mm")
    if k != 1:
        lay = lay.resize((max(2, int(w * k)), max(2, int(h * k))), Image.LANCZOS)
    base.alpha_composite(lay, (W // 2 - lay.width // 2, int(y + (h - lay.height) // 2)))

def brand(base):
    d = ImageDraw.Draw(base)
    d.text((W // 2, 1722), "ALNORTEDELSUR  ·  Mercado de Ruzafa", font=font(34), fill=(255, 255, 255, 230), anchor="mm")

def zoomed(img, z):
    w, h = img.size
    nw, nh = int(w * z), int(h * z)
    im = img.resize((nw, nh), Image.BILINEAR)
    l, tp = (nw - w) // 2, (nh - h) // 2
    return im.crop((l, tp, l + w, tp + h))

# ---------- scenes ----------
def scene_A(t):  # 0-3
    base = cover.convert("RGBA")
    z = 1.0 + 0.05 * (t / 3.0)
    p = rounded(zoomed(photo_fit, z), 44)
    base.alpha_composite(p, (0, 640))
    text_c(base, "¡NO TE QUEDES", 150, 112, YEL, 0.05, t, stroke=3)
    text_c(base, "SIN TUS", 285, 112, WHITE, 0.20, t, stroke=3)
    text_c(base, "INGREDIENTES!", 420, 112, YEL, 0.35, t, stroke=3)
    pill(base, "Colada morada · lunes 2 de noviembre", 1520, 40, 1.0, t)
    brand(base)
    return base

def clip_scene(frames, t, dur, topA, topB, slow=1.0):
    base = BG.convert("RGBA")
    idx = min(len(frames) - 1, int((t / dur) * (len(frames) - 1) * slow))
    fr = frames[idx]
    base.alpha_composite(rounded(fr, 44), (0, 560))
    text_c(base, topA, 190, 96, YEL, 0.05, t, stroke=3)
    text_c(base, topB, 320, 96, WHITE, 0.18, t, stroke=3)
    return base

ITEMS = ["Maíz morado", "Harina morada", "Flor de Jamaica", "Hierba luisa y cedrón",
         "Canela, clavo y pimienta", "Mora y mortiño"]
def scene_B(t):  # 3-6
    base = clip_scene(POT, t, 3.0, "TODO PARA TU", "COLADA MORADA")
    i = min(len(ITEMS) - 1, int(t / 0.5))
    pill(base, ITEMS[i], 1585, 52, i * 0.5, t)
    brand(base)
    return base

def scene_C(t):  # 6-9
    base = clip_scene(POUR, t, 3.0, "CALIENTE Y CON", "GUAGUA DE PAN")
    pill(base, "Como manda el 2 de noviembre", 1585, 44, 0.6, t)
    brand(base)
    return base

def scene_D(t):  # 9-12
    base = BG.convert("RGBA")
    d = ImageDraw.Draw(base)
    pulse = 1 + 0.03 * math.sin(t * 9)
    text_c(base, "¡HOY", 300, 150, YEL, 0.0, t, stroke=4)
    text_c(base, "SÁBADO!", 470, 150, YEL, 0.12, t, stroke=4)
    text_c(base, "8:30 a 15:00", 720, 118, WHITE, 0.45, t, stroke=3)
    text_c(base, "Puestos 213-220", 890, 76, WHITE, 0.70, t)
    text_c(base, "Mercado de Ruzafa", 990, 76, WHITE, 0.85, t)
    pill(base, "SOLO este domingo: 10:00 a 14:00", 1165, 40, 1.30, t)
    text_c(base, "Puestos 107-108", 1262, 48, WHITE, 1.45, t, maxw=980)
    text_c(base, "Que no se te acaben", 1360, 66, YEL, 1.7, t, maxw=980)
    text_c(base, "los ingredientes", 1450, 66, YEL, 1.85, t, maxw=980)
    return base

def scene_E(t):  # 12-14.6
    base = BG.convert("RGBA")
    text_c(base, "ALNORTEDELSUR", 420, 108, YEL, 0.0, t, stroke=3)
    text_c(base, "Mercado de Ruzafa · Valencia", 570, 54, WHITE, 0.25, t)
    pill(base, "WhatsApp 671 339 005", 760, 52, 0.55, t, bg=WHITE)
    text_c(base, "¿Te apartamos lo que necesites?", 960, 52, WHITE, 0.9, t, maxw=980)
    text_c(base, "Receta en alnortedelsurvlc.com/colada-morada", 1130, 38, YEL, 1.2, t, pop=False, maxw=1000)
    return base

SUN_ITEMS = ["Maíz y harina morada", "Flor de Jamaica", "Hierba luisa y cedrón",
             "Hojas de plátano", "Hoja de choclo", "Harina para tamales"]

def sA(t):
    base = cover.convert("RGBA")
    z = 1.0 + 0.05 * (t / 3.0)
    base.alpha_composite(rounded(zoomed(photo_fit, z), 44), (0, 640))
    text_c(base, "¡ESTE DOMINGO", 150, 112, YEL, 0.05, t, stroke=3)
    text_c(base, "ABRIMOS", 285, 112, WHITE, 0.20, t, stroke=3)
    text_c(base, "10:00 A 14:00!", 420, 112, YEL, 0.35, t, stroke=3)
    pill(base, "Sáb 8:30-15:00 · Solo este dom 10:00-14:00", 1520, 34, 1.0, t)
    brand(base)
    return base

def sB(t):
    base = clip_scene(POT, t, 3.0, "COLADA MORADA", "Y TAMALES")
    i = min(len(SUN_ITEMS) - 1, int(t / 0.5))
    pill(base, SUN_ITEMS[i], 1585, 52, i * 0.5 + 0.02, t)
    brand(base)
    return base

def sC(t):
    base = clip_scene(POUR, t, 3.0, "DÍA DE MUERTOS", "EN TU MESA")
    pill(base, "Todo lo que lleva, en el puesto", 1585, 44, 0.6, t)
    brand(base)
    return base

def sD(t):
    base = BG.convert("RGBA")
    text_c(base, "¡DOMINGO", 300, 150, YEL, 0.0, t, stroke=4)
    text_c(base, "ABIERTO!", 470, 150, YEL, 0.12, t, stroke=4)
    text_c(base, "10:00 a 14:00", 720, 118, WHITE, 0.45, t, stroke=3)
    text_c(base, "Puestos 107-108", 890, 76, WHITE, 0.70, t)
    text_c(base, "Mercado de Ruzafa", 990, 76, WHITE, 0.85, t)
    pill(base, "Horario especial · domingo 1 de noviembre", 1180, 38, 1.30, t)
    text_c(base, "Colada morada, tamales", 1360, 62, YEL, 1.7, t, maxw=980)
    text_c(base, "y Día de Muertos", 1450, 62, YEL, 1.85, t, maxw=980)
    return base

ATT = "/mnt/user-data/attachments/28cd0837-c4a7-5448-877b-d47794e30be1/"
VP = Image.open(ATT + "a5f3f7e8-image.jpg").convert("RGB")   # 768x1024 cesto + velas
HP = Image.open(ATT + "588d845e-image.jpg").convert("RGB")   # 1024x768 cesto + velas

def sC1(t):  # velas, vertical photo cropped to panel with slow zoom
    base = BG.convert("RGBA")
    z = 1.0 + 0.12 * (t / 2.2)
    ww = 768 / z
    hh = ww * 982 / 1080
    cx, cy = 384, 480
    box = (cx - ww / 2, cy - hh / 2, cx + ww / 2, cy + hh / 2)
    panel = VP.resize((1080, 982), Image.LANCZOS, box=box)
    base.alpha_composite(rounded(panel, 44), (0, 560))
    text_c(base, "DÍA DE MUERTOS", 190, 96, YEL, 0.05, t, stroke=3)
    text_c(base, "EN TU MESA", 320, 96, WHITE, 0.18, t, stroke=3)
    pill(base, "Velas del Día de los Muertos", 1585, 46, 0.5, t)
    brand(base)
    return base

def sC2(t):  # horizontal photo, productos mexicanos y centroamericanos
    base = BG.convert("RGBA")
    z = 1.0 + 0.06 * (t / 2.0)
    pw, ph = 1024, 768
    ww = pw / z; hh = ph / z
    box = ((pw - ww) / 2, (ph - hh) / 2, (pw + ww) / 2, (ph + hh) / 2)
    panel = HP.resize((1080, 810), Image.LANCZOS, box=box)
    base.alpha_composite(rounded(panel, 44), (0, 650))
    text_c(base, "Y PARA TUS TAMALES", 190, 84, YEL, 0.05, t, stroke=3, maxw=1000)
    text_c(base, "Y TUS PLATOS", 320, 84, WHITE, 0.18, t, stroke=3)
    pill(base, "Tomatillo · nopalitos · salsas · tortillas", 1560, 40, 0.5, t)
    brand(base)
    return base


def leaves_img():
    S=2; Wd,Hd=1080*S,900*S
    im=Image.new("RGBA",(Wd,Hd),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,Wd,Hd),44*S,fill=(24,52,30,255))
    # banana leaf: big diagonal leaf with midrib and veins
    def leaf(cx,cy,L,Wl,ang,col,vein):
        lay=Image.new("RGBA",(Wd,Hd),(0,0,0,0)); ld=ImageDraw.Draw(lay)
        pts=[]
        N=60
        for i in range(N+1):
            u=i/N; x=-L/2+L*u; w=Wl/2*math.sin(math.pi*u)**0.8
            pts.append((cx+x,cy-w))
        for i in range(N,-1,-1):
            u=i/N; x=-L/2+L*u; w=Wl/2*math.sin(math.pi*u)**0.8
            pts.append((cx+x,cy+w))
        ld.polygon(pts,fill=col)
        ld.line((cx-L/2,cy,cx+L/2,cy),fill=vein,width=7*S)
        for i in range(1,40):
            u=i/40; x=-L/2+L*u; w=Wl/2*math.sin(math.pi*u)**0.8
            ld.line((cx+x,cy,cx+x+36*S,cy-w*0.96),fill=vein,width=2*S)
            ld.line((cx+x,cy,cx+x+36*S,cy+w*0.96),fill=vein,width=2*S)
        return lay.rotate(ang,center=(cx,cy),resample=Image.BICUBIC)
    im.alpha_composite(leaf(560*S,300*S,1200*S,330*S,12,(46,125,50,255),(28,84,34,255)))
    im.alpha_composite(leaf(520*S,420*S,1100*S,280*S,-8,(70,150,60,255),(40,105,42,255)))
    # corn husks
    def husk(cx,base_y,hgt,wd,tilt,col,line):
        lay=Image.new("RGBA",(Wd,Hd),(0,0,0,0)); ld=ImageDraw.Draw(lay)
        pts=[(cx-wd/2,base_y),(cx-wd*0.62,base_y-hgt*0.45),(cx,base_y-hgt),(cx+wd*0.62,base_y-hgt*0.45),(cx+wd/2,base_y)]
        ld.polygon(pts,fill=col)
        for k in range(-4,5):
            ld.line((cx+k*wd/10,base_y,cx+k*wd/22,base_y-hgt*0.93),fill=line,width=3*S)
        return lay.rotate(tilt,center=(cx,base_y),resample=Image.BICUBIC)
    for cx,tl,col in [(300,-18,(232,206,128,255)),(540,0,(244,222,150,255)),(780,18,(232,206,128,255))]:
        im.alpha_composite(husk(cx*S,880*S,430*S,300*S,tl,col,(190,160,90,255)))
    return im.resize((1080,900),Image.LANCZOS)
LEAVES=leaves_img()

LA=Image.open(os.path.join(os.path.dirname(os.path.abspath(WD)),"h","a.jpg")).convert("RGB")
LB=Image.open(os.path.join(os.path.dirname(os.path.abspath(WD)),"h","b.jpg")).convert("RGB")
def _fit(im,w,h):
    r=max(w/im.width,h/im.height); nw,nh=int(im.width*r)+1,int(im.height*r)+1
    im=im.resize((nw,nh),Image.LANCZOS); l=(nw-w)//2; tp=(nh-h)//2
    return im.crop((l,tp,l+w,tp+h))
PA=_fit(LA,520,690); PB=_fit(LB,520,690)
def sL(t):
    base = BG.convert("RGBA")
    ka=ease_back(t/0.4); kb=ease_back((t-0.25)/0.4)
    base.alpha_composite(rounded(PA,36),(int(-540+(10+540)*min(1,ka)),640))
    base.alpha_composite(rounded(PB,36),(int(1080-(1080-550)*min(1,kb)),640))
    text_c(base, "HOJAS PARA", 170, 100, YEL, 0.05, t, stroke=3)
    text_c(base, "TUS TAMALES", 300, 100, WHITE, 0.18, t, stroke=3)
    text_c(base, "Hojas de plátano", 1420, 60, YEL, 0.7, t, stroke=2)
    pill(base, "También hoja de choclo", 1585, 46, 1.0, t)
    brand(base)
    return base

def sD2(t):
    base = BG.convert("RGBA")
    text_c(base, "¡ABRIMOS", 150, 120, YEL, 0.0, t, stroke=4)
    text_c(base, "ESTE FIN DE SEMANA!", 285, 76, WHITE, 0.12, t, stroke=3, maxw=1000)
    def card(y,day,hours,stalls,t0):
        k=ease_back((t-t0)/0.3)
        if t<t0: return
        lay=Image.new("RGBA",(960,420),(0,0,0,0)); d=ImageDraw.Draw(lay)
        d.rounded_rectangle((0,0,960,420),50,fill=(255,255,255,235))
        d.text((480,70),day,font=font(64),fill=PURPLE_L+(255,),anchor="mm")
        d.text((480,190),hours,font=font(104),fill=PURPLE_D+(255,),anchor="mm")
        d.text((480,310),stalls,font=font(54),fill=PURPLE_L+(255,),anchor="mm")
        d.text((480,375),"Mercado de Ruzafa",font=font(34),fill=PURPLE_D+(255,),anchor="mm")
        if k!=1:
            lay=lay.resize((max(2,int(960*k)),max(2,int(420*k))),Image.LANCZOS)
        base.alpha_composite(lay,(W//2-lay.width//2,int(y+(420-lay.height)//2)))
    card(430,"SÁBADO 31","8:30 a 15:00","Puestos 213-220",0.35)
    card(900,"SOLO ESTE DOMINGO 1","10:00 a 14:00","Puestos 107-108",0.8)
    text_c(base, "Colada morada, tamales,", 1400, 56, YEL, 1.4, t, maxw=980)
    text_c(base, "hojas y Día de Muertos", 1480, 56, YEL, 1.55, t, maxw=980)
    return base

if len(sys.argv) > 3 and sys.argv[3] == "sun":
    SCENES = [(0.0, 3.0, sA), (3.0, 6.0, sB), (6.0, 8.2, sC1), (8.2, 10.2, sC2), (10.2, 12.8, sL), (12.8, 16.0, sD2), (16.0, 18.0, scene_E)]
    if len(sys.argv) > 4:  # export still of the schedule card
        sD2(3.0).convert("RGB").save(sys.argv[4]); sys.exit(0)
else:
    SCENES = [(0.0, 3.0, scene_A), (3.0, 6.0, scene_B), (6.0, 9.0, scene_C), (9.0, 12.0, scene_D), (12.0, 14.6, scene_E)]
TOTAL = SCENES[-1][1]
XF = 0.15

def render(tt):
    for i, (a, b, fn) in enumerate(SCENES):
        if a <= tt < b or (i == len(SCENES) - 1 and tt >= a):
            img = fn(tt - a)
            if i + 1 < len(SCENES) and tt > b - XF:
                nxt = SCENES[i + 1][2](0.0)
                alpha = (tt - (b - XF)) / XF
                img = Image.blend(img, nxt, max(0, min(1, alpha)))
            dt = tt - a
            if dt < 0.3:
                z = 1.0 + 0.05 * max(0.0, 1 - dt / 0.3)
                if z > 1.001:
                    img = zoomed(img.convert("RGBA"), z)
                if dt < 0.16:
                    wh = Image.new("RGBA", (W, H), (255, 255, 255, 255))
                    img = Image.blend(img.convert("RGBA"), wh, 0.55 * (1 - dt / 0.16))
            if tt > TOTAL - 0.25:
                black = Image.new("RGBA", (W, H), (0, 0, 0, 255))
                img = Image.blend(img, black, (tt - (TOTAL - 0.25)) / 0.25)
            return img.convert("RGB")

out = sys.argv[2]
n = int(TOTAL * FPS)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                      "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an",
                      "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", out],
                     stdin=subprocess.PIPE)
for i in range(n):
    p.stdin.write(render(i / FPS).tobytes())
p.stdin.close(); p.wait()
print("done", out, n)
