"""Converte as artes de O Som da Chuva (pasta Imagens do caso) para os assets do módulo.

Uso: python3 tools/prep_som_da_chuva.py "<pasta Imagens>"
Battlemaps (3:2) vão direto para assets/o-som-da-chuva/mapas.
"""
import os, re, sys, unicodedata
from PIL import Image

SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "o-som-da-chuva")


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def save(im, path, maxside, q=88):
    im = im.convert("RGB")
    im.thumbnail((maxside, maxside), Image.LANCZOS)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, "WEBP", quality=q, method=6)
    return im.size


RETRATOS = {"elias-lil", "madame-jade", "prof-natan-arcanjo", "dra-frida-vanir", "pietra"}
RENAME = {"capa-do-documento": "capa-do-caso", "contracapa-do-documento": "contracapa"}

files = sorted(f for f in os.listdir(SRC) if f.startswith("Arte"))
# preferir .webp quando houver duas versões com o mesmo nome
names = {}
for f in files:
    base = f.rsplit(".", 1)[0]
    if base not in names or f.endswith(".webp"):
        names[base] = f
sizes = {}
for base, f in sorted(names.items()):
    s = slug(base.replace("Arte — ", ""))
    im = Image.open(os.path.join(SRC, f))
    if s.endswith("-battlemap"):
        s = s.replace("-battlemap", "")
        sizes["mapa-" + s] = save(im, f"{OUT}/mapas/{s}.webp", 4096, 90)
        save(im, f"{OUT}/thumbs/mapa-{s}.webp", 400, 80)
        continue
    s = RENAME.get(s, s.replace("-ambientacao", ""))
    if s in RETRATOS:
        save(im, f"{OUT}/retratos/{s}.webp", 1400)
    else:
        sizes[s] = save(im, f"{OUT}/cenas/{s}.webp", 4096)
        save(im, f"{OUT}/thumbs/{s}.webp", 400, 80)

for k, v in sorted(sizes.items()):
    print(k, v)
