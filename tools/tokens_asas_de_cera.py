"""Gera tokens redondos (512x512, fundo transparente) para os atores do caso."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, glob
ANTON = glob.glob('/usr/share/fonts/truetype/google-fonts/ofl/anton/*.ttf')[0]
DJ = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
S = 512
RING = {'sol': ((214, 160, 40), (110, 60, 10)), 'noite': ((168, 25, 95), (40, 10, 30)),
        'policia': ((60, 110, 190), (15, 25, 60)), 'neutro': ((40, 190, 200), (10, 45, 55))}

def ring(img, faction):
    c, dark = RING[faction]
    out = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    mask = Image.new('L', (S, S), 0); ImageDraw.Draw(mask).ellipse((22, 22, S - 22, S - 22), fill=255)
    out.paste(img, (0, 0), mask)
    d = ImageDraw.Draw(out)
    d.ellipse((8, 8, S - 8, S - 8), outline=dark + (255,), width=26)
    d.ellipse((14, 14, S - 14, S - 14), outline=c + (255,), width=14)
    d.ellipse((30, 30, S - 30, S - 30), outline=(0, 0, 0, 160), width=4)
    return out

def portrait(src, faction, top=0.06, size=0.78, out=None, cx=0.5):
    im = Image.open(src).convert('RGB')
    w, h = im.size; side = int(w * size); x0 = max(0, min(w - side, int(w * cx - side / 2))); y0 = int(h * top)
    im = im.crop((x0, y0, x0 + side, y0 + side)).resize((S, S), Image.LANCZOS)
    ring(im.convert('RGBA'), faction).save(out, quality=90)

def emblem(label, glyph, faction, out, glyph_font=DJ, gsize=210):
    c, dark = RING[faction]
    im = Image.new('RGBA', (S, S), (0, 0, 0, 255))
    d = ImageDraw.Draw(im)
    for r in range(S // 2, 0, -4):  # gradiente radial
        t = r / (S / 2)
        col = tuple(int(dark[i] * (1 - t) * 1.6 + 12 * t) for i in range(3))
        d.ellipse((S / 2 - r, S / 2 - r, S / 2 + r, S / 2 + r), fill=col + (255,))
    f = ImageFont.truetype(glyph_font, gsize)
    d.text((S / 2, S / 2 - 30), glyph, font=f, fill=c + (255,), anchor='mm')
    fl = ImageFont.truetype(ANTON, 52 if len(label) < 12 else 40)
    d.text((S / 2, S - 120), label, font=fl, fill=(240, 235, 225, 255), anchor='mm', stroke_width=3, stroke_fill=(0, 0, 0, 255))
    ring(im, faction).save(out, quality=90)

if __name__ == '__main__':
    R = 'assets/asas-de-cera/retratos/'; T = 'assets/asas-de-cera/tokens/'
    portrait(R + 'apia-nox.webp', 'noite', top=0.02, size=0.62, cx=0.64, out=T + 'apia-nox.webp')
    portrait(R + 'seth-desmond.webp', 'sol', top=0.13, size=0.72, out=T + 'seth-desmond.webp')
    for n, fac, top in [('ray-solaris', 'sol', .05), ('leona-sekh', 'sol', .05), ('capitao-teles', 'policia', .07),
                        ('dimitri-daidalos', 'neutro', .07), ('ian-caruso', 'neutro', .05),
                        ('lucas-lokken', 'neutro', .06), ('isadora-iset', 'neutro', .05),
                        ('hugo-corvino-o-emissario', 'neutro', .04)]:
        portrait(R + n + '.webp', fac, top=top, out=T + n + '.webp')
    emblem('ESCARAVELHO', '☉', 'sol', T + 'escaravelhos.webp')
    emblem('TIRA', '★', 'policia', T + 'tiras.webp')
    emblem('COBRA-NOITE', '↝', 'noite', T + 'brutamontes.webp', gsize=230)
    emblem('LABIRINTO', '▦', 'neutro', T + 'labirinto.webp')
    emblem('HELIÓPOLIS', '☀', 'sol', T + 'heliopolis.webp')
    emblem('ENKIDU', 'E', 'policia', T + 'enkidu.webp', glyph_font=ANTON)
    emblem('DRA. LUÍSA', 'L', 'neutro', T + 'luisa.webp', glyph_font=ANTON)
    emblem('NICO', 'N', 'noite', T + 'nico.webp', glyph_font=ANTON)
    emblem('VALENTINA', 'V', 'neutro', T + 'valentina.webp', glyph_font=ANTON)
