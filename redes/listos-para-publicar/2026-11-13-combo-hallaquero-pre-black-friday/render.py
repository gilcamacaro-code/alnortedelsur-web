"""Reel Combo Hallaquero · Pre Black Friday · sábado 14 nov 2026 (1080x1920, 30 fps)."""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
VINO = (74, 14, 46); AMA = (244, 196, 48); NEGRO = (14, 8, 12); BLANCO = (255, 255, 255)
F = '/home/claude/reel/Poppins-%s.ttf'
for _w in ['Bold','Medium','Regular']:
    import shutil; shutil.copy('/usr/share/fonts/truetype/google-fonts/Poppins-%s.ttf' % _w, '/home/claude/reel/Poppins-%s.ttf' % _w)
def font(s, w='Bold'): return ImageFont.truetype(F % w, s)
FOT = '/home/claude/web/redes/fotos/'
P = FOT + 'productos-hallaca/'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'frames'
os.makedirs(OUT, exist_ok=True)

PROD = [  # (foto, nombre en pantalla)
    ('/home/claude/reel/masarepa-goya.png', 'Masarepa\nblanca Goya', 0),
    (FOT + 'hojas-platano-goya.jpg', 'Hoja de plátano\nGoya', 0),
    ('/home/claude/reel/achiote-nativo.png', 'Achiote en grano\nNativo', 0),
    (FOT + 'aji1.jpg', 'Ají dulce\nfresco', 1),
    (P + 'cebolla-fina.jpg', 'Cebollino\nfresco', 0),
    (P + 'pasas-goya.jpg', 'Pasas\nGoya', 0),
    (P + 'alcaparras-goya.jpg', 'Alcaparras\nGoya', 0),
    ('/home/claude/reel/aceituna-rellena-goya.png', 'Aceitunas\nrellenas Goya', 0),
    ('/home/claude/reel/salsa-inglesa-el-rey.png', 'Salsa inglesa\nEl Rey 155 ml', 0),
    ('/home/claude/reel/panela-redonda.png', 'Panela redonda\n454 g', 0),
    ('/home/claude/reel/pabilo.jpg', 'Pabilo\npara amarrar', 0),
]
COMPLETO_ANTES, COMPLETO = 25.89, 23.30
BASICO_ANTES, BASICO = 12.49, 11.90
eur = lambda v: f'{v:.2f}'.replace('.', ',') + ' €'

def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def back(t):
    t = max(0, min(1, t)); c = 1.70158
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2

def cover(im, w, h):
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))

LBL = 26
def card(path, size=360, label=None, fill=False):
    c = Image.new('RGBA', (size, size + (110 if label else 0)), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((0, 0, size - 1, size - 1), 36, fill=BLANCO)
    if fill:
        im = cover(Image.open(path).convert('RGB'), size, size)
        mk = Image.new('L', (size, size), 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, size - 1, size - 1), 36, fill=255)
        c.paste(im, (0, 0), mk)
        if label:
            ImageDraw.Draw(c).multiline_text((size // 2, size + 12), label, font=font(LBL, 'SemiBold'), fill=BLANCO, anchor='ma', align='center', spacing=2)
        return c
    im = Image.open(path).convert('RGB'); im.thumbnail((size - 40, size - 40), Image.LANCZOS)
    if im.width < size - 60 and im.height < size - 60:  # foto pequeña: escalar
        r = (size - 60) / max(im.size); im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    c.paste(im, ((size - im.width) // 2, (size - im.height) // 2))
    if label:
        f = font(LBL, 'SemiBold')
        d.multiline_text((size // 2, size + 12), label, font=f, fill=BLANCO, anchor='ma', align='center', spacing=2)
    return c

def card_lbl(f, size, n, z):
    base = card(f, size, None, z)
    c = Image.new('RGBA', (size + 80, size + 100), (0, 0, 0, 0)); c.alpha_composite(base, (40, 0))
    ImageDraw.Draw(c).multiline_text((c.width // 2, size + 12), n, font=font(LBL, 'SemiBold'), fill=BLANCO, anchor='ma', align='center', spacing=2)
    return c
CARDS = [card_lbl(f, 220, n, bool(z)) for f, n, z in PROD]
SMALL = [card(f, 250, None, bool(z)) for f, _, z in PROD]
HALL = Image.open(FOT + 'hallacas.jpg').convert('RGB')

logo = Image.open('/home/claude/web/redes/plantilla/logo.png').convert('RGBA').resize((300, 300), Image.LANCZOS)
m = Image.new('L', (300, 300), 0); ImageDraw.Draw(m).ellipse((4, 4, 295, 295), fill=255); logo.putalpha(m)

def paste_alpha(base, im, xy, a=1.0, scale=None):
    if scale is not None:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.LANCZOS)
        xy = (int(xy[0] - im.width / 2), int(xy[1] - im.height / 2))
    if a < 1:
        im = im.copy(); al = im.getchannel('A').point(lambda v: int(v * a)); im.putalpha(al)
    base.alpha_composite(im, (int(xy[0]), int(xy[1])))

def strip_text(base, text, cy, size, a=1.0, dy=0, pad=34, bg=VINO, fg=AMA):
    f = font(size, 'ExtraBold') if os.path.exists(F % 'ExtraBold') else font(size)
    lay = Image.new('RGBA', base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    bb = d.multiline_textbbox((W // 2, cy + dy), text, font=f, anchor='mm', align='center', spacing=8)
    d.rounded_rectangle((bb[0] - pad, bb[1] - pad * 0.7, bb[2] + pad, bb[3] + pad * 0.7), 24, fill=bg + (int(235 * a),))
    d.multiline_text((W // 2, cy + dy), text, font=f, fill=fg + (int(255 * a),), anchor='mm', align='center', spacing=8)
    base.alpha_composite(lay)

def text(base, s, xy, size, fill=BLANCO, a=1.0, w='Bold', anchor='mm'):
    lay = Image.new('RGBA', base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f = font(size, w) if os.path.exists(F % w) else font(size)
    d.multiline_text(xy, s, font=f, fill=fill + (int(255 * a),), anchor=anchor, align='center', spacing=6)
    base.alpha_composite(lay)

def bf_badge(base, cy, t, txt='PRE BLACK FRIDAY', bg=None, fg=None, pulse=0):
    s = back(t)
    if s <= 0: return
    b = Image.new('RGBA', (760, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.rounded_rectangle((0, 0, 759, 119), 60, fill=(bg or NEGRO) + (255,), outline=AMA, width=6)
    fs = 62 if len(txt) <= 16 else 54
    d.text((380, 62), txt, font=font(fs, 'ExtraBold'), fill=fg or AMA, anchor='mm')
    paste_alpha(base, b, (W // 2, cy), 1, max(0.01, s * (1 + pulse)))

def burst(base, cx, cy, r, txt, t, size=78):
    s = back(t)
    if s <= 0: return
    n = 18; R = int(r * s)
    lay = Image.new('RGBA', (2 * r + 40, 2 * r + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    o = r + 20; pts = []
    for i in range(2 * n):
        rr = r if i % 2 == 0 else r * 0.82; ang = math.pi * i / n + t * 0.3
        pts.append((o + rr * math.cos(ang), o + rr * math.sin(ang)))
    d.polygon(pts, fill=(220, 30, 40, 255))
    d.multiline_text((o, o), txt, font=font(size, 'ExtraBold') if os.path.exists(F % 'ExtraBold') else font(size), fill=BLANCO, anchor='mm', align='center', spacing=0)
    paste_alpha(base, lay, (cx, cy), 1, s)

def bg_vino(t):
    im = Image.new('RGBA', (W, H), VINO + (255,)); d = ImageDraw.Draw(im)
    for i in range(14):  # rayas diagonales suaves en movimiento
        x = (i * 180 + t * 60) % (W + 600) - 300
        d.polygon([(x, 0), (x + 70, 0), (x - 500, H), (x - 570, H)], fill=(90, 22, 58, 255))
    return im

SC = [  # (nombre, duración s)
    ('gancho', 3.0), ('productos', 4.6), ('combos', 4.4), ('sabado', 3.4), ('cta', 4.4)]
TOTAL = sum(d for _, d in SC)

def frame(T):
    acc = 0
    for name, dur in SC:
        if T < acc + dur or name == 'cta': t = T - acc; break
        acc += dur
    if name == 'gancho':
        z = 1.0 + 0.10 * (t / dur)
        bg = cover(HALL, int(W / z * 1.0), int(H / z)).resize((W, H), Image.LANCZOS) if False else cover(HALL, W, H)
        bg = bg.resize((int(W * z), int(H * z)), Image.LANCZOS).crop((int(W * (z - 1) / 2), int(H * (z - 1) / 2), int(W * (z - 1) / 2) + W, int(H * (z - 1) / 2) + H))
        im = bg.convert('RGBA')
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((0, 0, W, H), fill=(0, 0, 0, 90)); im.alpha_composite(sh)
        bf_badge(im, 470, t / 0.5)
        a = ease((t - 0.35) / 0.4); strip_text(im, '¿Ya tienes todo\npara tus hallacas?', 900, 78, a, int(60 * (1 - a)))
        a2 = ease((t - 1.0) / 0.4); strip_text(im, 'Combo Hallaquero', 1150, 66, a2, int(40 * (1 - a2)), bg=AMA, fg=VINO)
        a3 = ease((t - 1.5) / 0.35); strip_text(im, 'SOLO ESTE SÁBADO 14', 1340, 70, a3, int(40 * (1 - a3)), bg=(220, 30, 40), fg=BLANCO)
        return im
    im = bg_vino(T)
    if name == 'productos':
        bf_badge(im, 250, 1, 'SOLO ESTE SÁBADO 14', (220, 30, 40), BLANCO, 0.04 * math.sin(T * 7))
        text(im, 'COMBO HALLAQUERO', (W // 2, 400), 76, AMA, ease(t / 0.3), 'ExtraBold')
        text(im, 'Todo para la masa, la hoja y el guiso', (W // 2, 480), 38, BLANCO, ease((t - 0.2) / 0.3), 'Medium')
        xs = [W // 2 - 375, W // 2 - 125, W // 2 + 125, W // 2 + 375]; ys = [550, 880, 1210]
        for i, c in enumerate(CARDS):
            st = 0.3 + i * 0.24; e = back((t - st) / 0.5)
            if t < st: continue
            r, k = divmod(i, 4); n = min(4, len(CARDS) - r * 4)
            cx = xs[k] + (4 - n) * 125
            x = cx - c.width // 2; y = ys[r] - int(220 * (1 - min(1, e)))
            paste_alpha(im, c, (x, y), ease((t - st) / 0.25))
        return im
    if name == 'combos':
        bf_badge(im, 250, 1, 'SOLO ESTE SÁBADO 14', (220, 30, 40), BLANCO, 0.04 * math.sin(T * 7))
        text(im, 'ELIGE TU COMBO', (W // 2, 400), 76, AMA, ease(t / 0.3), 'ExtraBold')
        a = ease((t - 0.2) / 0.3)
        strip_text(im, 'COMPLETO · 11 productos', 530, 50, a, int(30 * (1 - a)), bg=AMA, fg=VINO, pad=26)
        for i, c in enumerate(SMALL):
            r, k = divmod(i, 6); n = 6 if r == 0 else 5
            x = (W - n * 168 + 10) // 2 + k * 168
            paste_alpha(im, c.resize((156, 156), Image.LANCZOS), (x, 610 + r * 172), ease((t - 0.3 - i * 0.07) / 0.3))
        a = ease((t - 0.9) / 0.3)
        strip_text(im, 'BÁSICO · masarepa + hoja + achiote', 1050, 50, a, int(30 * (1 - a)), bg=AMA, fg=VINO, pad=26)
        for i, c in enumerate([SMALL[0], SMALL[1], SMALL[2]]):
            x = 242 + i * 202; paste_alpha(im, c.resize((185, 185), Image.LANCZOS), (x, 1120), ease((t - 1.0 - i * 0.08) / 0.3))
        e = back((t - 1.8) / 0.5)
        if e > 0:
            b = Image.new('RGBA', (1000, 330), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
            d.text((500, 80), 'AHORRA HASTA', font=font(80, 'ExtraBold'), fill=BLANCO, anchor='mm')
            d.text((500, 220), 'UN 10 %', font=font(170, 'ExtraBold'), fill=AMA, anchor='mm')
            paste_alpha(im, b, (W // 2, 1490), 1, e)
        return im
    if name == 'sabado':
        on = int(t * 4) % 2 == 0 and t > 0.8
        im = Image.new('RGBA', (W, H), ((150, 15, 25) if on else NEGRO) + (255,))
        bf_badge(im, 420, t / 0.4)
        p = 1 + 0.04 * math.sin(t * 9)
        e = back((t - 0.3) / 0.5)
        if e > 0:
            b = Image.new('RGBA', (1000, 520), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
            d.text((500, 120), 'SOLO ESTE', font=font(84, 'ExtraBold'), fill=BLANCO, anchor='mm')
            d.text((500, 270), 'SÁBADO 14', font=font(170, 'ExtraBold'), fill=AMA, anchor='mm')
            d.text((500, 420), 'DE NOVIEMBRE', font=font(84, 'ExtraBold'), fill=BLANCO, anchor='mm')
            paste_alpha(im, b, (W // 2, 860), 1, e * p)
        text(im, 'Un solo día · 8:30 a 15:00\nHasta agotar existencias', (W // 2, 1260), 46, BLANCO, ease((t - 0.9) / 0.4), 'Medium')
        return im
    # CTA
    e = back(t / 0.5); paste_alpha(im, logo, (W // 2, 470), 1, max(0.01, e))
    text(im, 'ALNORTEDELSUR', (W // 2, 690), 80, AMA, ease((t - 0.2) / 0.3), 'ExtraBold')
    text(im, 'Mercado de Russafa · Valencia', (W // 2, 770), 42, BLANCO, ease((t - 0.3) / 0.3), 'Medium')
    a = ease((t - 0.5) / 0.4)
    strip_text(im, 'SOLO SÁBADO 14\nPuestos 213-220 · 8:30 a 15:00', 950, 52, a, int(30 * (1 - a)), bg=AMA, fg=VINO)
    a2 = ease((t - 0.9) / 0.4)
    text(im, 'Puestos 213-220: L-S 8:30-15:00\nPuestos 107-108: L-V 17:00-21:00', (W // 2, 1150), 40, BLANCO, a2, 'Medium')
    a3 = ease((t - 1.3) / 0.4)
    text(im, 'Apártalo por WhatsApp 671 339 005', (W // 2, 1300), 44, AMA, a3, 'Bold')
    return im

if __name__ == '__main__':
    n = int(TOTAL * FPS)
    only = sys.argv[2:]  # opcional: lista de segundos para previsualizar
    if only:
        for s in only: frame(float(s)).convert('RGB').save(f'{OUT}/prev_{s}.jpg', quality=85)
    else:
        for i in range(n):
            frame(i / FPS).convert('RGB').save(f'{OUT}/f{i:04d}.jpg', quality=92)
    print('total', TOTAL, 's', n, 'frames')
