"""Gera o JSON-fonte da aventura Asas de Cera (Adventure) para o sistema city-of-mist.

Uso: python3 tools/build.py && node tools/pack.mjs
"""
import hashlib, json, os, re, unicodedata
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = "modules/mesa-alta"
OUT = os.path.join(ROOT, "src", "packs", "asas-de-cera")
STATS = {"systemId": "city-of-mist", "systemVersion": "4.5.3", "coreVersion": "13.351",
         "createdTime": 1795100000000, "modifiedTime": 1795100000000, "lastModifiedBy": None,
         "compendiumSource": None, "duplicateSource": None}


def gid(*parts):
    h = hashlib.sha1("|".join(parts).encode()).hexdigest()
    alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    n = int(h, 16)
    s = ""
    for _ in range(16):
        n, r = divmod(n, 62)
        s += alpha[r]
    return s


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


# ------------------------------------------------------------------ pastas
def folder(name, typ, color, parent=None):
    return {"_id": gid("folder", typ, name, parent or ""), "name": name, "type": typ, "folder": parent, "sorting": "a",
            "sort": 0, "color": color, "description": "", "flags": {}, "_stats": STATS}


# Pasta do caso (cor própria do caso) com subpastas de cor padrão, iguais em todos os casos da Mesa Alta
CASE_COLOR = "#c27f12"
SUB = {"adv": ("Adversários", "#a8195f"), "npc": ("NPCs", "#0e6f78"), "amb": ("Ambientação", "#2b2540"), "map": ("Battlemaps", "#3a5a9c")}
ROOT_F = {"Actor": folder("Asas de Cera", "Actor", CASE_COLOR), "Scene": folder("Asas de Cera", "Scene", CASE_COLOR)}
F = {
    "adv": folder(SUB["adv"][0], "Actor", SUB["adv"][1], ROOT_F["Actor"]["_id"]),
    "npc": folder(SUB["npc"][0], "Actor", SUB["npc"][1], ROOT_F["Actor"]["_id"]),
    "amb": folder(SUB["amb"][0], "Scene", SUB["amb"][1], ROOT_F["Scene"]["_id"]),
    "map": folder(SUB["map"][0], "Scene", SUB["map"][1], ROOT_F["Scene"]["_id"]),
    "jou": folder("Asas de Cera", "JournalEntry", CASE_COLOR),
}

# ------------------------------------------------------------------ atores
def spectrum(owner, name, tier):
    return {"_id": gid(owner, "sp", name), "name": name, "type": "spectrum", "img": "icons/svg/target.svg",
            "system": {"description": "", "locked": False, "version": "1", "free_content": False,
                       "locale_name": "", "systemName": "", "sourceBook": "", "maxTier": tier},
            "effects": [], "folder": None, "sort": 0, "ownership": {"default": 0}, "flags": {}, "_stats": STATS}


def move(owner, sub, name, text, hide=False):
    return {"_id": gid(owner, "mv", sub, name), "name": name, "type": "gmmove", "img": "icons/svg/item-bag.svg",
            "system": {"description": text, "locked": False, "version": "1", "free_content": False, "locale_name": "",
                       "systemName": "", "sourceBook": "", "subtype": sub, "taglist": [], "statuslist": [],
                       "hideName": hide, "header": "symbols" if hide else "text", "superMoveId": ""},
            "effects": [], "folder": None, "sort": 0, "ownership": {"default": 0}, "flags": {}, "_stats": STATS}


def actor(key, name, fold, token, portrait=None, mythos="", logos="", short="", bio="", spectra=(), moves=(),
          collective=0, disposition=-1):
    aid = gid("actor", key)
    img = f"{MOD}/assets/asas-de-cera/retratos/{portrait}.webp" if portrait else f"{MOD}/assets/asas-de-cera/tokens/{token}.webp"
    items = [spectrum(key, n, t) for n, t in spectra] + [move(key, *m) for m in moves]
    return {
        "_id": aid, "name": name, "type": "threat", "img": img, "folder": F[fold]["_id"], "sort": 0,
        "system": {"locked": False, "biography": bio, "description": "", "short_description": short, "gmnotes": "",
                   "crewThemes": [], "version": "1", "alias": "?????", "useAlias": False, "finalized": False,
                   "mythos": mythos, "logos": logos, "age": 0, "residence": "", "pronouns": "",
                   "is_template": False, "template_ids": [], "collectiveSize": collective,
                   "defaultTags": [], "defaultStatuses": []},
        "prototypeToken": {
            "name": name.split(" — ")[0], "displayName": 20, "actorLink": collective == 0, "appendNumber": collective > 0,
            "texture": {"src": f"{MOD}/assets/asas-de-cera/tokens/{token}.webp", "scaleX": 1, "scaleY": 1, "fit": "contain"},
            "width": 1, "height": 1, "lockRotation": True, "disposition": disposition, "displayBars": 0,
            "sight": {"enabled": True, "range": 0, "visionMode": "basic"}, "ring": {"enabled": False}},
        "items": items, "effects": [], "ownership": {"default": 0}, "flags": {}, "_stats": STATS}


def P(*paras):
    return "".join(f"<p>{x}</p>" for x in paras)


ACTORS = [
    actor("ray", "Ray Sólaris — Rá", "adv", "ray-solaris", "ray-solaris", "Rá", "CEO da Heliópolis Energia",
          "O Sol da Cidade. Membro da Mesa Alta.",
          P("CEO da Heliópolis Energia, dona de quase toda a eletricidade da Cidade. Terno branco, sempre iluminado, nunca suado.",
            "<strong>Quer:</strong> que ninguém brilhe além do que ele permite. <strong>Fraqueza:</strong> entre 23h50 e o amanhecer desce ao Duat; ali os espectros caem dois níveis e ele não usa o Feixe do Sol.",
            "<em>“Eu não matei ninguém. Eu apenas brilhei.”</em>"),
          [("Ferir ou Incapacitar (4 à noite)", 6), ("Convencer ou Enganar (3 à noite)", 5), ("Humilhar em Público", 3), ("Expor no Logos", 4)],
          [("custom", "Ninguém olha para o sol", "Quem encara $name de frente sob a luz do dia recebe [ofuscado-2] antes de agir."),
           ("custom", "A noite", "Entre 23h50 e o amanhecer, os espectros de $name caem dois níveis e ele não usa o Feixe do Sol. Cada portão do Duat atravessado sem ataque devolve um nível."),
           ("hard", "Feixe do Sol", "Ergue a mão aberta e o mundo vira meio-dia: [queimado-4] em um alvo, ou queime um rótulo de equipamento (ele derrete)."),
           ("hard", "Eu sou o dia", "Ao amanhecer, $name remove até três níveis de condições de si mesmo."),
           ("hard", "Comprar a Cidade", "A galera perde um aliado mundano: demitido, preso ou comprado."),
           ("soft", "Uma lâmpada acende", "Uma luz acende sobre quem tenta se esconder.", True),
           ("soft", "Oferta gentil", "$name oferece, com gentileza paternal, um emprego à galera.", True),
           ("soft", "Calor", "A temperatura da sala sobe até todos suarem.", True)]),
    actor("leona", "Leona Sekh — Sekhmet", "adv", "leona-sekh", "leona-sekh", "Sekhmet", "Chefe de segurança da Heliópolis",
          "O Olho do Rá.",
          P("Leal, feroz, adora a caça. Limpou a cena do crime e incrimina Enkidu na virada da Sessão 2.",
            "<em>“Sabe o que eu mais gosto no meu trabalho? Quando a presa ainda acha que é caçadora.”</em>"),
          [("Ferir ou Incapacitar", 4), ("Convencer (a trair o Rá)", 5), ("Enganar ou Despistar", 3)],
          [("custom", "A leoa caça", "Quando a galera foge de $name, ela sempre sabe para onde foram, a menos que tenham passado por água ou escuridão total."),
           ("hard", "Garras de fogo", "[feridas-3] ou [queimado-3]."),
           ("hard", "Sede de sangue", "$name ataca dois personagens de uma vez."),
           ("hard", "Incriminar", "Provas forjadas: [procurado-3] em um personagem."),
           ("soft", "Rugido", "$name ruge e o ar treme.", True),
           ("soft", "Farejar", "Para tudo para cheirar o ar.", True),
           ("soft", "Marca de garra", "Deixa um sinal de que esteve ali: marcas de garra na porta.", True)]),
    actor("escaravelhos", "Escaravelhos — Segurança da Heliópolis", "adv", "escaravelhos", None, "", "Segurança de Elite",
          "Ternos claros, broche de escaravelho dourado.",
          P("Coletivo. Baseado no perfil genérico <strong>Segurança de Elite</strong> do Guia da MC (cap. 3): ajuste os espectros aos do livro."),
          [("Ferir ou Incapacitar", 3), ("Convencer ou Subornar", 3), ("Despistar", 2)],
          [("hard", "Golpe treinado", "Imobilizam ou espancam: [ferido-2] ou [imobilizado-2]."),
           ("hard", "Limpar a cena", "Somem com uma prova antes de a galera alcançá-la."),
           ("soft", "Rádio", "Um deles fala baixo no rádio: reforços a caminho.", True)], collective=2),
    actor("tiras", "Tiras do Capitão Teles", "adv", "tiras", None, "", "Polícia comprada",
          "Policiais que arquivam casos para quem paga.",
          P("Coletivo. Baseado no perfil genérico <strong>Tiras / Seguranças</strong> do Guia da MC (cap. 3)."),
          [("Ferir ou Incapacitar", 2), ("Convencer", 2)],
          [("hard", "Algemas", "[detido-3]."), ("soft", "Circulando", "“Circulando, gente. Acidente.”", True)],
          collective=2),
    actor("teles", "Capitão Ambrósio Teles", "adv", "capitao-teles", "capitao-teles", "", "Capitão de polícia",
          "Chefe de Enkidu. Covarde, não cruel.",
          P("Arquiva casos para a Heliópolis. Perfil <strong>Detetive</strong> do Guia da MC, com Convencer baixo: é fácil de pressionar.",
            "<em>“Eu só arquivo! Eles mandam a pasta, eu fecho a pasta.”</em>"),
          [("Convencer ou Intimidar", 2), ("Ferir ou Incapacitar", 2)],
          [("hard", "Arquivar", "Fecha um local da investigação com uma ordem judicial."),
           ("soft", "Telefone", "Teles liga para alguém e olha o relógio de ouro.", True)], disposition=0),
    actor("apia", "Ápia Nox — Apep", "adv", "apia-nox", "apia-nox", "Apep", "Líder da Cobra-Noite",
          "A Rainha da Meia-Noite.",
          P("Domina a noite: boates, geradores, gasolina, mercado negro de energia. Tem a foto do feixe. Quer usar a galera para matar o sol.",
            "<em>“Não se preocupem com o preço agora. Eu cobro sempre no escuro.”</em>"),
          [("Ferir ou Incapacitar", 4), ("Convencer ou Negociar", 3), ("Enganar", 5)],
          [("custom", "Apagão", "$name apaga as luzes de um quarteirão inteiro: todos recebem [no-escuro-2], exceto a Cobra-Noite."),
           ("hard", "Veneno lento", "[envenenado-3], que sobe um nível por cena sem tratamento."),
           ("hard", "Cobrar a dívida", "Exige o favor prometido no pior momento possível."),
           ("soft", "Cobra", "Uma cobra passa por baixo da mesa.", True),
           ("soft", "Geradores", "Todos os geradores falham por um segundo.", True),
           ("soft", "Sorriso", "$name sorri e não responde.", True)], disposition=0),
    actor("brutamontes", "Brutamontes da Cobra-Noite", "adv", "brutamontes", None, "", "Capangas",
          "Os punhos da Rainha da Meia-Noite.",
          P("Coletivo. Baseado no perfil genérico <strong>Brutamontes</strong> do Guia da MC (cap. 3)."),
          [("Ferir ou Incapacitar", 3), ("Intimidar", 2)],
          [("hard", "Pancadaria", "[ferido-3]."), ("soft", "Estalar os dedos", "Estalam os dedos e fecham a porta.", True)],
          collective=2),
    actor("labirinto", "O Labirinto de Dédalo", "adv", "labirinto", None, "", "Perigo de ambiente",
          "As Galerias Creta.",
          P("Atravessar pede Investigar ou Correr o Risco. Quem segue o fio vermelho deixado por Dédalo passa sem rolar."),
          [("Atravessar", 3)],
          [("hard", "Os corredores mudam", "[perdido-2]."), ("hard", "Separar a galera", "Um personagem fica sozinho numa ala distante."),
           ("soft", "Eco", "Um eco repete a fala de alguém.", True), ("soft", "Reflexo", "Uma vitrine reflete Ian voando.", True)]),
    actor("heliopolis", "Heliópolis Energia", "adv", "heliopolis", None, "", "Perigo institucional",
          "Pressão entre as cenas.",
          P("Use entre as cenas, como pressão sobre a galera."),
          [("Expor ou Derrubar no Logos", 5)],
          [("hard", "Processo", "Uma advogada da empresa (perfil Advogada Particular) congela um aliado ou uma prova."),
           ("hard", "Corte de energia", "O esconderijo da galera fica sem luz e sem internet."),
           ("hard", "Imprensa comprada", "A galera vira suspeita na TV: [procurado-2].")]),
]
NPCS = [
    ("enkidu", "Detetive Enkidu", "enkidu", None, "Enkidu", "Detetive de homicídios",
     "Aliada honesta. Jogável (folio do Starter Box) ou NPC. Use o retrato oficial do folio.",
     "<em>“Quarenta e oito horas. É o tempo que me deram para chamar um assassinato de acidente.”</em>"),
    ("dimitri", "Dimitri Daidalos — Dédalo", "dimitri-daidalos", "dimitri-daidalos", "Dédalo", "Engenheiro e arquiteto",
     "Pai de Ian. Escondido nas Galerias Creta com a caixa-preta do ÍCARO-1. Só fala se a galera prometer protegê-lo.",
     "<em>“Eu ensinei meu filho a voar. Devia ter ensinado a cair.”</em>"),
    ("ian", "Ian Caruso — Ícaro", "ian-caruso", "ian-caruso", "Ícaro", "Bilionário da aviação (morto)",
     "A vítima. Aparece em vídeos, diário e flashbacks.", "<em>“O chão é para quem tem medo.”</em>"),
    ("seth", "Seth Desmond — Set", "seth-desmond", "seth-desmond", "Set", "Vice-presidente da Heliópolis",
     "Quer o trono do Rá. Oferece crachás, plantas e acesso à Barca e à Assembleia. Vai trair a galera logo depois.",
     "<em>“Eu não quero que vocês confiem em mim. Quero que vocês precisem de mim.”</em>"),
    ("lokken", "Lucas Lokken — Loki", "lucas-lokken", "lucas-lokken", "Loki", "Socialite",
     "Filmou a queda. Ajuda por diversão e cobra um favor sem nome.", "<em>“Que tipo de convidado não filma um homem pegando fogo?”</em>"),
    ("isadora", "Isadora Iset — Ísis", "isadora-iset", "isadora-iset", "Ísis", "Curadora do Museu de Antiguidades",
     "Conhece o Nome Secreto do Rá e o troca pelo direito de guardar o papiro.", "<em>“Um nome é uma chave. Eu empresto a chave. A porta continua minha.”</em>"),
    ("corvino", "Hugo Corvino — o emissário", "hugo-corvino-o-emissario", "hugo-corvino-o-emissario", "Odin (gancho)", "Observador da Mesa Alta",
     "Só observa e anota. Gancho de Odin para a série.", "<em>“Não me peçam ajuda. Me deem algo para anotar.”</em>"),
    ("luisa", "Dra. Luísa Prado", "luisa", None, "", "Legista", "Honesta e assustada. Viu as queimaduras e a cera.",
     "<em>“Isso aqui não é queimadura de fio. É de forno.”</em>"),
    ("nico", "Nico, o olheiro", "nico", None, "", "Olheiro da Cobra-Noite", "Tirou a foto do feixe. Sabe demais e foge de todos.",
     "<em>“Aí o céu acendeu e eu apertei o botão.”</em>"),
    ("valentina", "Valentina Rocha", "valentina", None, "", "Sócia da Asas Ltda.", "Sabe dos e-mails para a Heliópolis e teme pela empresa.",
     "<em>“O Ian bebia água com gás antes de voar. Sempre.”</em>"),
]
for key, name, tok, por, myth, logos, bio, fala in NPCS:
    ACTORS.append(actor(key, name, "npc", tok, por, myth, logos, "", P(bio, fala), disposition=0))
AID = {a["_id"]: a for a in ACTORS}
A = {k: gid("actor", k) for k in ["ray", "leona", "escaravelhos", "tiras", "teles", "apia", "brutamontes", "labirinto",
                                   "heliopolis", "enkidu", "dimitri", "ian", "seth", "lokken", "isadora", "corvino", "luisa", "nico", "valentina"]}

# ------------------------------------------------------------------ cenas
def scene(key, name, fold, img, w, h, grid=100, battle=False, walls=(), lights=(), tokens=(), darkness=0.0, weather="", sort=0):
    sid = gid("scene", key)
    return {
        "_id": sid, "name": name, "folder": F[fold]["_id"], "sort": sort, "navigation": False, "navOrder": sort, "navName": "",
        "active": False, "img": None,
        "background": {"src": img, "anchorX": 0.5, "anchorY": 0.5, "offsetX": 0, "offsetY": 0, "fit": "fill",
                       "scaleX": 1, "scaleY": 1, "rotation": 0, "tint": "#ffffff", "alphaThreshold": 0},
        "foreground": None, "foregroundElevation": 20, "thumb": img.replace("/cenas/", "/thumbs/").replace("/mapas/", "/thumbs/mapa-"),
        "width": w, "height": h, "padding": 0, "initial": {"x": w // 2, "y": h // 2, "scale": 0.5}, "backgroundColor": "#000000",
        "grid": {"type": 0, "size": grid, "style": "solidLines", "thickness": 1, "color": "#000000", "alpha": 0.2,
                 "distance": 1, "units": "m"},
        "tokenVision": battle,
        "fog": {"exploration": battle, "overlay": None, "colors": {"explored": None, "unexplored": None}},
        "environment": {"darknessLevel": darkness, "darknessLock": False,
                        "globalLight": {"enabled": not battle, "alpha": 0.5, "bright": False, "color": None, "coloration": 1,
                                        "luminosity": 0, "saturation": 0, "contrast": 0, "shadows": 0, "darkness": {"min": 0, "max": 1}},
                        "cycle": True},
        "weather": weather, "drawings": [], "tokens": list(tokens), "lights": list(lights), "notes": [], "sounds": [],
        "regions": [], "templates": [], "tiles": [], "walls": list(walls), "playlist": None, "playlistSound": None,
        "journal": None, "journalEntryPage": None, "ownership": {"default": 0}, "flags": {}, "_stats": STATS}


def W(skey, i, pts, s, kind="wall"):
    """Polilinha em coordenadas de exibição (largura 1200) -> paredes."""
    out = []
    for j in range(len(pts) - 1):
        (x1, y1), (x2, y2) = pts[j], pts[j + 1]
        c = [round(x1 * s), round(y1 * s), round(x2 * s), round(y2 * s)]
        sight = 0 if kind == "glass" else 20
        out.append({"_id": gid(skey, "w", str(i), str(j)), "c": c, "move": 20, "sight": sight, "light": sight,
                    "sound": 0 if kind == "glass" else 20, "door": {"door": 1, "secret": 2}.get(kind, 0), "ds": 0,
                    "dir": 0, "threshold": {"light": None, "sight": None, "sound": None, "attenuation": False}, "flags": {}})
    return out


def walls(skey, s, spec):
    out = []
    for i, (kind, pts) in enumerate(spec):
        out += W(skey, i, pts, s, kind)
    return out


def L(skey, i, x, y, s, dim, bright, color, alpha=0.2, anim=None):
    return {"_id": gid(skey, "l", str(i)), "x": round(x * s), "y": round(y * s), "rotation": 0, "walls": True, "vision": False,
            "elevation": 0, "hidden": False,
            "config": {"negative": False, "priority": 0, "alpha": alpha, "angle": 360, "bright": bright, "color": color,
                       "coloration": 1, "dim": dim, "attenuation": 0.5, "luminosity": 0.5, "saturation": 0, "contrast": 0,
                       "shadows": 0, "animation": {"type": anim, "speed": 3, "intensity": 3, "reverse": False},
                       "darkness": {"min": 0, "max": 1}}, "flags": {}}


def T(skey, i, akey, x, y, s, grid, hidden=False):
    a = AID[A[akey]]
    pt = a["prototypeToken"]
    return {"_id": gid(skey, "t", str(i)), "name": pt["name"], "actorId": a["_id"], "actorLink": pt["actorLink"],
            "x": round(x * s - grid / 2), "y": round(y * s - grid / 2), "elevation": 0, "width": 1, "height": 1,
            "texture": dict(pt["texture"]), "hidden": hidden, "disposition": pt["disposition"], "displayName": 20,
            "displayBars": 0, "lockRotation": True, "rotation": 0, "alpha": 1, "locked": False,
            "sight": {"enabled": True, "range": 0, "visionMode": "basic"}, "ring": {"enabled": False},
            "delta": {}, "flags": {}}


SCENES = []
AMB = [("capa", "00 Capa", "capa-do-caso", 1792, 2688, ""),
       ("crime", "01 Avenida Zênite — Cena do crime", "cena-do-crime-na-avenida-zenite", 2944, 1648, "rain"),
       ("necro", "02 Necrotério", "necroterio", 2944, 1648, ""),
       ("terraco-amb", "03 Hotel Zênite — Terraço", "terraco-do-hotel-zenite", 2944, 1648, ""),
       ("hangar", "04 Asas Ltda. — Hangar", "hangar-da-asas-ltda", 2944, 1648, ""),
       ("cobertura", "05 Cobertura de Ian", "cobertura-de-ian", 2944, 1648, ""),
       ("galerias", "07 Galerias Creta", "galerias-creta", 2944, 1648, ""),
       ("torre", "08 Torre da Heliópolis", "torre-da-heliopolis", 1792, 2688, "rain"),
       ("enkidu", "09 A queda de Enkidu", "a-queda-de-enkidu", 2960, 1648, "rain"),
       ("museu", "10 Museu de Antiguidades — Sala egípcia", "sala-egipcia-do-museu", 2944, 1648, ""),
       ("duat", "11 O Duat", "o-duat", 2944, 1648, ""),
       ("alvorada", "12 Assembleia da Alvorada", "assembleia-da-alvorada", 2944, 1648, ""),
       ("epilogo", "13 Epílogo", "epilogo", 2944, 1648, ""),
       ("contracapa", "Fim — Contracapa", "contracapa", 1792, 2688, "")]
for i, (k, n, img, w, h, wx) in enumerate(AMB):
    SCENES.append(scene(k, n, "amb", f"{MOD}/assets/asas-de-cera/cenas/{img}.webp", w, h, weather=wx, sort=i * 10))

# Terraço do Hotel Zênite (4096x2737) — exibição 1200 -> fator 3.4133
s = 4096 / 1200
k = "map-terraco"
SCENES.append(scene(k, "03 Terraço do Hotel Zênite", "map", f"{MOD}/assets/asas-de-cera/mapas/terraco-do-hotel-zenite.webp", 4096, 2737,
    grid=150, battle=True, darkness=0.55, sort=10,
    walls=walls(k, s, [
        ("glass", [(40, 40), (970, 40)]), ("glass", [(40, 40), (40, 745)]), ("glass", [(40, 745), (1165, 745)]),
        ("glass", [(1165, 230), (1165, 745)]),
        ("wall", [(1165, 225), (1165, 20), (970, 20), (970, 225), (1060, 225)]), ("door", [(1060, 225), (1165, 225)]),
    ]),
    lights=[L(k, 0, 600, 140, s, 9, 3, "#3fd0dc", 0.25), L(k, 1, 885, 365, s, 5, 1, "#ff3fa4", 0.3, "pulse"),
            L(k, 2, 1005, 365, s, 5, 1, "#ff3fa4", 0.3, "pulse"), L(k, 3, 150, 380, s, 5, 1, "#ffb347", 0.2, "torch"),
            L(k, 4, 435, 300, s, 3, 1, "#ffcc66", 0.2, "torch"), L(k, 5, 720, 300, s, 3, 1, "#ffcc66", 0.2, "torch"),
            L(k, 6, 555, 480, s, 3, 1, "#ffcc66", 0.2, "torch"), L(k, 7, 200, 650, s, 3, 1, "#ffcc66", 0.2, "torch"),
            L(k, 8, 950, 650, s, 3, 1, "#ffcc66", 0.2, "torch"), L(k, 9, 1070, 130, s, 4, 1, "#d6a028", 0.3)],
    tokens=[T(k, 0, "escaravelhos", 1000, 300, s, 150, True), T(k, 1, "escaravelhos", 1080, 300, s, 150, True),
            T(k, 2, "lokken", 300, 520, s, 150)]))

# Clube Meia-Noite (2560x1440)
s = 2560 / 1200
k = "map-clube"
SCENES.append(scene(k, "06 Clube Meia-Noite", "map", f"{MOD}/assets/asas-de-cera/mapas/clube-meia-noite.webp", 2560, 1440,
    grid=110, battle=True, darkness=0.7, sort=20,
    walls=walls(k, s, [
        ("wall", [(15, 15), (855, 15)]), ("wall", [(15, 15), (15, 590), (575, 590)]),
        ("door", [(575, 590), (665, 590)]), ("wall", [(665, 590), (1040, 590)]),
        ("wall", [(15, 455), (140, 455), (140, 505)]), ("door", [(140, 505), (140, 545)]), ("wall", [(140, 545), (140, 590)]),
        ("wall", [(855, 15), (855, 165), (880, 185)]), ("door", [(880, 185), (905, 205)]), ("wall", [(905, 205), (1040, 205)]),
        ("wall", [(1040, 205), (1040, 315)]), ("door", [(1040, 315), (1040, 375)]), ("wall", [(1040, 375), (1040, 590)]),
        ("wall", [(855, 15), (1095, 15)]), ("secret", [(1095, 15), (1150, 15)]), ("wall", [(1150, 15), (1165, 15), (1165, 600), (1040, 600)]),
        ("wall", [(1090, 205), (1090, 560)]),
    ]),
    lights=[L(k, i, x, y, s, 3, 1, "#ffb347", 0.25, "torch") for i, (x, y) in enumerate(
        [(155, 128), (280, 128), (540, 80), (780, 128), (318, 285), (160, 400), (915, 312), (915, 425), (915, 537),
         (295, 545), (490, 545), (770, 545)])]
        + [L(k, 20, 590, 325, s, 8, 2, "#ff3fa4", 0.3, "radialrainbow"), L(k, 21, 75, 525, s, 3, 1, "#3fd0dc", 0.3),
           L(k, 22, 960, 110, s, 4, 1, "#7cff9e", 0.25, "flame"), L(k, 23, 1125, 300, s, 4, 1, "#3fd0dc", 0.2)],
    tokens=[T(k, 0, "apia", 540, 110, s, 110), T(k, 1, "brutamontes", 595, 545, s, 110, True),
            T(k, 2, "brutamontes", 645, 545, s, 110, True), T(k, 3, "brutamontes", 1010, 345, s, 110, True)]))

# Oficina escondida de Dédalo (2560x1440)
k = "map-oficina"
SCENES.append(scene(k, "07 Oficina escondida de Dédalo", "map", f"{MOD}/assets/asas-de-cera/mapas/oficina-escondida-de-dedalo.webp", 2560, 1440,
    grid=100, battle=True, darkness=0.65, sort=30,
    walls=walls(k, s, [
        ("wall", [(95, 70), (185, 70)]), ("glass", [(185, 70), (545, 70)]), ("wall", [(545, 70), (555, 70)]),
        ("wall", [(650, 70), (660, 70)]), ("glass", [(660, 70), (1015, 70)]), ("wall", [(1015, 70), (1105, 70)]),
        ("wall", [(95, 70), (95, 300)]), ("wall", [(95, 375), (95, 600)]), ("wall", [(1105, 70), (1105, 300)]), ("wall", [(1105, 375), (1105, 600)]),
        ("wall", [(95, 600), (190, 600)]), ("glass", [(190, 600), (545, 600)]), ("wall", [(545, 600), (650, 600)]),
        ("glass", [(650, 600), (1015, 600)]), ("wall", [(1015, 600), (1105, 600)]),
        ("wall", [(232, 145), (540, 145)]), ("wall", [(425, 165), (425, 300)]), ("wall", [(150, 100), (150, 300)]),
        ("wall", [(150, 375), (150, 580)]), ("wall", [(235, 330), (375, 330)]), ("wall", [(250, 330), (250, 460)]),
        ("wall", [(355, 395), (530, 395)]), ("wall", [(385, 505), (535, 505)]), ("wall", [(745, 145), (930, 145)]),
        ("wall", [(840, 215), (965, 215)]), ("wall", [(940, 240), (940, 390)]), ("wall", [(820, 300), (820, 440), (735, 440)]),
        ("wall", [(1045, 100), (1045, 290)]), ("wall", [(1050, 380), (1050, 585)]),
    ]),
    lights=[L(k, 0, 690, 255, s, 6, 2, "#ffcc66", 0.25), L(k, 1, 775, 215, s, 4, 1, "#ff6a2a", 0.3, "torch"),
            L(k, 2, 600, 40, s, 5, 1, "#ff3fa4", 0.3), L(k, 3, 1160, 335, s, 5, 1, "#3fd0dc", 0.3), L(k, 4, 40, 335, s, 5, 1, "#ff3fa4", 0.3)],
    tokens=[T(k, 0, "dimitri", 620, 380, s, 100), T(k, 1, "escaravelhos", 40, 335, s, 100, True),
            T(k, 2, "escaravelhos", 1160, 335, s, 100, True), T(k, 3, "escaravelhos", 600, 40, s, 100, True)]))

# A Barca no Duat (2560x1440)
k = "map-barca"
SCENES.append(scene(k, "11 A Barca no Duat", "map", f"{MOD}/assets/asas-de-cera/mapas/a-barca-no-duat.webp", 2560, 1440,
    grid=100, battle=True, darkness=0.75, sort=40,
    walls=walls(k, s, [
        ("wall", [(115, 195), (380, 195), (380, 20), (810, 20), (810, 195), (1085, 195)]),
        ("wall", [(115, 435), (380, 435), (380, 655), (810, 655), (810, 435), (1085, 435)]),
        ("door", [(112, 200), (112, 430)]), ("door", [(1090, 200), (1090, 430)]),
    ]),
    lights=[L(k, i, x, y, s, 4, 1, "#ffcc66", 0.25) for i, (x, y) in enumerate(
        [(130, 205), (285, 205), (430, 205), (545, 205), (745, 205), (885, 205), (1068, 205),
         (130, 430), (285, 430), (430, 430), (545, 430), (745, 430), (885, 430), (1068, 430)])]
        + [L(k, 20, 850, 315, s, 6, 2, "#ff3fa4", 0.3), L(k, 21, 55, 315, s, 5, 1, "#ff2a2a", 0.35, "pulse"),
           L(k, 22, 1145, 315, s, 5, 1, "#ff2a2a", 0.35, "pulse"), L(k, 23, 595, 90, s, 6, 0, "#3fd0dc", 0.2, "wave"),
           L(k, 24, 595, 550, s, 6, 0, "#3fd0dc", 0.2, "wave")],
    tokens=[T(k, 0, "ray", 850, 315, s, 100), T(k, 1, "leona", 700, 240, s, 100, True),
            T(k, 2, "escaravelhos", 600, 240, s, 100, True), T(k, 3, "escaravelhos", 800, 400, s, 100, True),
            T(k, 4, "apia", 600, 560, s, 100, True), T(k, 5, "brutamontes", 520, 520, s, 100, True),
            T(k, 6, "brutamontes", 680, 110, s, 100, True)]))

# ------------------------------------------------------------------ journal
md = open(os.path.join(ROOT, "src", "asas-de-cera", "caso.md"), encoding="utf-8").read()
md = re.sub(r"^# Asas de Cera\n+\*Um caso.*?\*\n+.*?@\w+\n", "", md, flags=re.S)
md = re.sub(r"\nDetalhes que inventei.*?\n", "\n", md)
md = re.sub(r"\s*\*\*\\\[revisar\\\]\*\*", "", md)
md = re.sub(r"\n### Como usar os prompts no Midjourney.*", "\n", md, flags=re.S)
md = md.replace(" Todos os retratos usam o mesmo estilo e proporção 2:3, para virar token depois.", "")
PORTRAITS = set(x[:-5] for x in os.listdir(os.path.join(ROOT, "assets", "asas-de-cera", "retratos")))
SCENE_BY_IMG = {}
for sc in SCENES:
    SCENE_BY_IMG.setdefault(os.path.basename(sc["background"]["src"])[:-5] + ("-map" if sc["tokenVision"] else ""), sc)


def fig(m):
    s_ = slug(m.group(1))
    if s_ == "capa-do-caso":
        return "\n"
    if s_ in PORTRAITS:
        return f'\n<div class="adc-portrait"><img src="{MOD}/assets/asas-de-cera/retratos/{s_}.webp"></div>\n'
    if "battlemap" in s_:
        base = s_.replace("-battlemap", "")
        sc = SCENE_BY_IMG.get(base + "-map")
        link = f' <p class="adc-cap">@UUID[Scene.{sc["_id"]}]{{Abrir a cena: {sc["name"]}}}</p>' if sc else ""
        return f'\n<figure class="adc-fig adc-map"><img src="{MOD}/assets/asas-de-cera/mapas/{base}.webp"></figure>{link}\n'
    base = s_.replace("-ambientacao", "")
    sc = SCENE_BY_IMG.get(base)
    link = f'<p class="adc-cap">@UUID[Scene.{sc["_id"]}]{{Abrir a cena: {sc["name"]}}}</p>' if sc else ""
    return f'\n<figure class="adc-fig"><img src="{MOD}/assets/asas-de-cera/cenas/{base}.webp"></figure>{link}\n'


md = re.sub(r"> \*\*Arte — (.+?)\*\*\s*\n+```text\n.*?```", fig, md, flags=re.S)
html = markdown.markdown(md, extensions=["tables", "sane_lists"])


def bq(m):
    inner = m.group(1)
    txt = re.sub("<.*?>", "", inner).strip()
    cls = "adc-box"
    for key, c in [("Leia em voz alta", "adc-aloud"), ("Regra", "adc-rule"), ("Dica do MC", "adc-tip"),
                   ("Resumo", "adc-summary"), ("Palestrinha", "adc-tip")]:
        if txt.startswith(key):
            cls = c
            break
    return f'<blockquote class="{cls}">{inner}</blockquote>'


html = re.sub(r"<blockquote>(.*?)</blockquote>", bq, html, flags=re.S)
html = re.sub(r"<p><strong>(Falas[^<]*)</strong></p>\s*<ul>(.*?)</ul>",
              r'<div class="adc-falas"><p class="adc-falas-h">\1</p><ul>\2</ul></div>', html, flags=re.S)
html = re.sub(r'(<h3>[^<]*</h3>)((?:(?!<h3>).)*?)(<div class="adc-portrait"><img src="[^"]+"></div>)',
              lambda m: m.group(1) + m.group(3) + m.group(2), html, flags=re.S)
# Nomes de atores viram links para as fichas
LINKS = {"Ray Sólaris — Rá, o Sol da Cidade": "ray", "Leona Sekh — Sekhmet, o Olho do Rá": "leona",
         "Escaravelhos — segurança da Heliópolis": "escaravelhos", "Tiras do Capitão Teles": "tiras",
         "Ápia Nox e a Cobra-Noite": "apia", "O Labirinto de Dédalo (Perigo de ambiente)": "labirinto",
         "Heliópolis Energia (Perigo institucional)": "heliopolis"}
for title, key in LINKS.items():
    html = html.replace(f"<h3>{title}</h3>", f'<h3>{title}</h3><p class="adc-cap">@UUID[Actor.{A[key]}]{{Abrir a ficha}}</p>', 1)

for prefix, key in [("Detetive Enkidu", "enkidu"), ("Ian Caruso", "ian"), ("Dimitri Daidalos", "dimitri"), ("Ray Sólaris — Rá (", "ray"),
                    ("Leona Sekh — Sekhmet (", "leona"), ("Capitão Ambrósio Teles", "teles"), ("Ápia Nox — Apep", "apia")]:
    html = re.sub(r"(<h3>" + re.escape(prefix) + r"[^<]*</h3>)", lambda m: m.group(1) + f'<p class="adc-cap">@UUID[Actor.{A[key]}]{{Abrir a ficha}}</p>', html, count=1)
for name, key in [("Seth Desmond", "seth"), ("Lucas Lokken", "lokken"), ("Isadora Iset", "isadora")]:
    html = html.replace(f"<strong>{name} — ", f"@UUID[Actor.{A[key]}]{{{name}}} <strong>— ", 1)

OPEN = {"Por trás das cortinas": "torre-da-heliopolis", "Sessão 1": "terraco-do-hotel-zenite",
        "Sessão 2": "galerias-creta", "Sessão 3": "o-duat", "Epílogo": "epilogo", "Visão geral": "capa-do-caso"}
chunks = re.split(r"(?=<h2>)", html)
pages = []
for ch in chunks:
    m = re.match(r"<h2>(.*?)</h2>", ch)
    if not m:
        continue
    title = m.group(1)
    body = ch[m.end():]
    hero = next((v for k_, v in OPEN.items() if title.startswith(k_)), None)
    if hero:
        body = f'<figure class="adc-hero"><img src="{MOD}/assets/asas-de-cera/cenas/{hero}.webp"></figure>' + body
    pages.append((title, body))
    if title.startswith("Por trás das cortinas"):
        pages.append(("O Iceberg do Caso", f'<figure class="adc-fig"><img src="{MOD}/assets/asas-de-cera/journal/iceberg.webp"></figure>'
                      '<p>Cada fio vermelho é uma saída: a Dica de um local aponta para o próximo. Quanto mais fundo, mais protegida está a verdade.</p>'))

JID = gid("journal", "guia")
journal = {
    "_id": JID, "name": "Asas de Cera — Guia do MC", "folder": F["jou"]["_id"], "sort": 0, "categories": [],
    "pages": [{"_id": gid("page", t), "name": re.sub("<.*?>", "", t), "type": "text", "sort": (i + 1) * 100000,
               "title": {"show": True, "level": 1},
               "text": {"format": 1, "content": f'<div class="asas-de-cera">{b}</div>', "markdown": ""},
               "image": {}, "video": {"controls": True, "volume": 0.5}, "src": None, "system": {},
               "ownership": {"default": -1}, "flags": {}, "_stats": STATS, "category": None}
              for i, (t, b) in enumerate(pages)],
    "ownership": {"default": 0}, "flags": {}, "_stats": STATS}

# ------------------------------------------------------------------ aventura
ADV = gid("adventure", "asas-de-cera")
adventure = {
    "_id": ADV, "_key": f"!adventures!{ADV}", "name": "Asas de Cera", "img": f"{MOD}/assets/asas-de-cera/cenas/capa-do-caso.webp",
    "caption": "Um caso de City of Mist em três sessões",
    "description": "<p>Um bilionário cai em chamas diante de cem testemunhas que não lembram de nada. Uma detetive teimosa vê no caso a ponta de uma rede que manda na Cidade. E, no alto da torre mais brilhante, um sol que não aceita ser ofuscado.</p>"
                   "<p>Importa: o Guia do MC completo, 14 cenas de ambientação, 4 battlemaps com paredes, portas e luzes, "
                   "9 Perigos com espectros e movimentos, 10 NPCs e tokens já posicionados (adversários ocultos).</p>",
    "actors": ACTORS, "combats": [], "items": [], "journal": [journal], "scenes": SCENES, "tables": [], "macros": [],
    "cards": [], "playlists": [], "folders": list(ROOT_F.values()) + list(F.values()), "sort": 0, "flags": {}, "_stats": STATS, "folder": None}

os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    os.remove(os.path.join(OUT, f))
json.dump(adventure, open(os.path.join(OUT, "Asas_de_Cera.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("atores", len(ACTORS), "cenas", len(SCENES), "páginas", len(pages))
