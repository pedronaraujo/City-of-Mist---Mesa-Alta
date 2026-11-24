"""Converte as artes de Reflexos no Espelho (pasta Imagens do caso) para os assets do módulo.

Uso: python3 tools/prep_reflexos.py "<pasta Imagens>"
"""
import os, re, sys, unicodedata
from PIL import Image

SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "reflexos-no-espelho")


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def save(im, path, maxside, q=88):
    im = im.convert("RGB")
    im.thumbnail((maxside, maxside), Image.LANCZOS)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, "WEBP", quality=q, method=6)
    return im.size


RETRATOS = {"dr-tiago-resende", "nico-valenca", "elisa-cortes", "teo-tezca", "amir-neves", "clara-moura", "o-espelho-de-obsidiana"}
RENAME = {"capa-do-documento": "capa-do-caso", "contracapa-do-documento-ultima-pagina": "contracapa",
          "abertura-do-caso-pagina-do-capitulo": "abertura-do-caso", "a-varanda-da-suite-3101": "a-varanda-da-suite-3101"}

sizes = {}
for f in sorted(os.listdir(SRC)):
    p = os.path.join(SRC, f)
    if os.path.isdir(p) or not f.startswith("Arte"):
        continue
    s = slug(f.replace("Arte — ", "").rsplit(".", 1)[0])
    im = Image.open(p)
    if "battlemap" in s:
        continue  # mapas vêm da pasta 3x2
    s = RENAME.get(s, s.replace("-ambientacao", "").replace("-cena-digital", ""))
    if s in RETRATOS:
        save(im, f"{OUT}/retratos/{s}.webp", 1400)
    else:
        sizes[s] = save(im, f"{OUT}/cenas/{s}.webp", 4096)
        save(im, f"{OUT}/thumbs/{s}.webp", 400, 80)

M = os.path.join(SRC, "mapas 3x2")
for f in sorted(os.listdir(M)):
    s = slug(f.replace("Arte — ", "").replace(" 3x2", "").rsplit(".", 1)[0]).replace("-battlemap", "")
    im = Image.open(os.path.join(M, f))
    sizes["mapa-" + s] = save(im, f"{OUT}/mapas/{s}.webp", 4096, 90)
    save(im, f"{OUT}/thumbs/mapa-{s}.webp", 400, 80)

for k, v in sorted(sizes.items()):
    print(k, v)
