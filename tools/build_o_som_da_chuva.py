"""Gera o JSON-fonte da aventura O Som da Chuva (Adventure) para o sistema city-of-mist.

Uso: python3 tools/build_o_som_da_chuva.py && node tools/pack.mjs
"""
import hashlib, json, os, re, unicodedata
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASE = "o-som-da-chuva"
MOD = "modules/mesa-alta"
AS = f"{MOD}/assets/{CASE}"
OUT = os.path.join(ROOT, "src", "packs", CASE)
STATS = {"systemId": "city-of-mist", "systemVersion": "4.5.3", "coreVersion": "13.351",
         "createdTime": 1795500000000, "modifiedTime": 1795500000000, "lastModifiedBy": None,
         "compendiumSource": None, "duplicateSource": None}


def gid(*parts):
    h = hashlib.sha1(("somdachuva|" + "|".join(parts)).encode()).hexdigest()
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
CASE_COLOR = "#2a7d84"
SUB = {"adv": ("Adversários", "#a8195f"), "npc": ("NPCs", "#0e6f78"), "amb": ("Ambientação", "#2b2540"), "map": ("Battlemaps", "#3a5a9c")}
ROOT_F = {"Actor": folder("O Som da Chuva", "Actor", CASE_COLOR), "Scene": folder("O Som da Chuva", "Scene", CASE_COLOR)}
F = {
    "adv": folder(SUB["adv"][0], "Actor", SUB["adv"][1], ROOT_F["Actor"]["_id"]),
    "npc": folder(SUB["npc"][0], "Actor", SUB["npc"][1], ROOT_F["Actor"]["_id"]),
    "amb": folder(SUB["amb"][0], "Scene", SUB["amb"][1], ROOT_F["Scene"]["_id"]),
    "map": folder(SUB["map"][0], "Scene", SUB["map"][1], ROOT_F["Scene"]["_id"]),
    "jou": folder("O Som da Chuva", "JournalEntry", CASE_COLOR),
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
    img = f"{AS}/retratos/{portrait}.webp" if portrait else f"{AS}/tokens/{token}.webp"
    items = [spectrum(key, n, t) for n, t in spectra] + [move(key, *m) for m in moves]
    return {
        "_id": aid, "name": name, "type": "threat", "img": img, "folder": F[fold]["_id"], "sort": 0,
        "system": {"locked": False, "biography": bio, "description": "", "short_description": short, "gmnotes": "",
                   "crewThemes": [], "version": "1", "alias": "?????", "useAlias": False, "finalized": False,
                   "mythos": mythos, "logos": logos, "age": 0, "residence": "", "pronouns": "",
                   "is_template": False, "template_ids": [], "collectiveSize": collective,
                   "defaultTags": [], "defaultStatuses": []},
        "prototypeToken": {
            "name": name.split(" — ")[0].split(" (")[0], "displayName": 20, "actorLink": collective == 0,
            "appendNumber": collective > 0,
            "texture": {"src": f"{AS}/tokens/{token}.webp", "scaleX": 1, "scaleY": 1, "fit": "contain"},
            "width": 1, "height": 1, "lockRotation": True, "disposition": disposition, "displayBars": 0,
            "sight": {"enabled": True, "range": 0, "visionMode": "basic"}, "ring": {"enabled": False}},
        "items": items, "effects": [], "ownership": {"default": 0}, "flags": {}, "_stats": STATS}


def P(*paras):
    return "".join(f"<p>{x}</p>" for x in paras)


ACTORS = [
    actor("natan", "Prof. Dr. Natan Arcanjo — Noé", "adv", "prof-natan-arcanjo", "prof-natan-arcanjo", "Noé",
          "Doutor em mitologia comparada e benfeitor do Residencial Monte Ararate", "O assassino. Colecionador de Mythos, dois de cada espécie.",
          P("Sessentão de barba bem aparada, casaco de tweed, sorriso paciente. Aparece na TV toda noite pedindo calma e doações. Reconhece o Mythos de alguém numa frase.",
            "<strong>Quer:</strong> completar a coleção e provar que dois mitos equivalentes geram um terceiro. Para isso, a enchente não pode acabar.",
            "<strong>Trava:</strong> Desmascarado não passa de 2 antes do clímax. Acima disso, só com provas mundanas mostradas em público. Atacado em público, vira mártir.",
            "<em>“Dois de cada. Nunca um só. Um só é sobra.”</em>"),
          [("Desmascarado (diante da cidade)", 5), ("Suspeita (relógio do Natan)", 4), ("Ferir ou Incapacitar", 3)],
          [("custom", "Mártir", "Sempre que um personagem fere ou ataca $name em público sem provas, a multidão o protege e ele ganha [herói-da-enchente] no mesmo nível."),
           ("hard", "Virar a cidade", "Na TV, $name pede calma e aponta os PJs como oportunistas: [desacreditado-2]."),
           ("hard", "Um telefonema", "$name liga para o reitor: a Enkidou é afastada do caso."),
           ("hard", "Antecipar o fechamento", "As portas do Residencial fecham um dia antes."),
           ("soft", "O nome do mito", "$name diz em voz alta o nome do mito por trás de um PJ.", True),
           ("soft", "Uma vaga na arca", "$name oferece abrigo a um PJ, se houver um par.", True)]),
    actor("jade", "Madame Jade — Chalchiuhtlicue", "adv", "madame-jade", "madame-jade", "Chalchiuhtlicue",
          "Dona das Águas de Jade, intermediária de favores", "Causa da chuva e suspeita plantada. Só para com o pedido do Elias.",
          P("Elegante, saia verde-escura, voz baixa. Nunca diz não, diz “isso tem um preço”. Cumpre contratos; não sabia que o Elias queria parar a chuva.",
            "<strong>Travas:</strong> Fala só avança a partir da Sessão 2 e com a amostra da banheira. Convencida só completa com a prova do assassinato e o caderno 48.",
            "<strong>Relógio de atitude (oculto):</strong> suspeita → aliada perigosa → vingativa.",
            "<em>“Um acordo só acaba quando quem pediu diz que acabou.”</em>"),
          [("Convencida (parar a chuva)", 4), ("Fala (revelar o pacto)", 2), ("Vingativa", 3)],
          [("hard", "Portas fechadas", "$name encerra a conversa e fecha as Águas de Jade para os PJs."),
           ("hard", "Atrás do professor", "Avança Vingativa: $name parte sozinha atrás do Natan, e a água sobe com ela."),
           ("hard", "A água leva", "[arrastado-2] ou [encharcado-2] em quem a ameaça."),
           ("soft", "Um favor", "$name cobra um favor em troca de informação.", True),
           ("soft", "Uma apresentação", "$name apresenta os PJs a alguém que vai cobrar depois.", True)], disposition=0),
    actor("frida", "Dra. Frida Vanir — Freyja", "adv", "dra-frida-vanir", "dra-frida-vanir", "Freyja",
          "Diretora do Instituto Fólkvangr", "Cúmplice. Gera bebês em laboratório para um exército que proteja o Odin.",
          P("Alta, cabelo claro preso, jaleco impecável. Encantadora com pacientes, fria com funcionários. General disfarçada de médica.",
            "<strong>Trava:</strong> sem mencionar o Odin, Traição não passa de 1. Ela nunca entrega os bebês.",
            "<strong>Relógio de atitude (oculto):</strong> cúmplice → instável → traidora.",
            "<em>“O professor coleciona. Eu construo.”</em>"),
          [("Traição (entregar o Natan)", 3), ("Recuo (abandonar o projeto)", 2), ("Ferir ou Incapacitar", 3)],
          [("hard", "Sumir com as provas", "O subsolo é limpo: uma prova da cena 3.4 desaparece."),
           ("hard", "Levar a Pietra", "Os seguranças levam a Pietra de volta à clínica."),
           ("hard", "Encanto", "[confiante-demais-2] ou [em-dívida-2] em quem aceita a ajuda dela."),
           ("soft", "Ajuda gentil", "$name oferece tratamento ou ajuda.", True),
           ("soft", "Acompanhante", "$name manda o Bruno “acompanhar” os PJs.", True)]),
    actor("seg", "Seguranças da Frida", "adv", "segurancas-frida", None, "", "Seguranças particulares do Instituto Fólkvangr",
          "Cenas 2.1, 3.2 e 3.4.",
          P("Profissionais, educados e firmes. Preferem cercar e levar a Pietra a lutar. Recuam se o tiroteio chamar atenção.",
            "<em>“A doutora só quer conversar com ela. Vocês não têm nada com isso.”</em>"),
          [("Ferir ou Incapacitar", 3), ("Conter", 3)],
          [("hard", "Golpe", "Tirar alguém do jogo: [atordoado-3]."),
           ("hard", "Levar a Pietra", "A Pietra é levada para a van."),
           ("hard", "Reforço", "Chega o Bruno."),
           ("soft", "Cercar", "Os seguranças fecham um círculo.", True),
           ("soft", "Rota cortada", "Uma rota de fuga é bloqueada.", True)], collective=2),
    actor("bruno", "Bruno, chefe da segurança", "adv", "bruno", None, "", "Chefe da segurança da Dra. Frida",
          "Pode desistir ao ver o subsolo.",
          P("Educado e firme. Não sabe de tudo: ver os bebês no subsolo pode virar o jogo.",
            "<em>“A doutora não atende sem hora marcada.”</em>"),
          [("Ferir ou Incapacitar", 4), ("Convencer", 3)],
          [("hard", "Tiro de aviso", "Atira para assustar e derruba quem estiver na água: [caído-2]."),
           ("hard", "Imobilizar", "[imobilizado-2]."),
           ("soft", "Rádio", "Fala baixo no rádio.", True)]),
    actor("correnteza", "Correnteza", "adv", "correnteza", None, "", "A água que leva", "Cenas 1.4, 2.1 e 4.2. Travessia, não inimigo.",
          P("A água não luta, mas leva. Use como travessia: cada atravessada é uma chance de perder algo."),
          [("Atravessar (Arrastado)", 3)],
          [("hard", "Separar", "O grupo se separa: um PJ fica do outro lado."),
           ("hard", "Levar", "A água leva um objeto ou uma prova."),
           ("soft", "Subir", "O nível da água sobe um palmo.", True)], disposition=0),
    actor("ararate", "Multidão do Ararate", "adv", "ararate", None, "", "Moradores gratos e seguranças do Residencial",
          "Clímax (4.2). Machucar um deles protege o Natan.",
          P("Gente que acredita no professor. Ninguém ali é mau. Machucar um deles avança o relógio contra os PJs.",
            "<strong>Virada:</strong> só avança com provas mostradas às câmeras ou com moradores dos blocos de cima falando por si.",
            "<em>“Deixem o professor em paz!”</em>"),
          [("Virada (duvidar do professor)", 4), ("Conter", 3), ("Dispersar", 3)],
          [("hard", "Proteger o professor", "A multidão fecha um muro humano em volta do Natan."),
           ("hard", "As câmeras gravam", "Alguém cai, e as câmeras culpam os PJs: [vilão-da-noite-2]."),
           ("soft", "Gritos", "Cantam o nome do professor.", True)], collective=3, disposition=0),
]
NPCS = [
    ("elias", "Elias Lil — Enlil", "elias-lil", "elias-lil", "Enlil", "Colunista de fofocas (morto)",
     "A vítima. Ouvia a cidade inteira e enlouqueceu com isso. Aparece em fotos e nos cadernos.",
     "<em>“Ouvi a enfermeira. Agora eu sei para que serve a chuva. Amanhã eu peço que pare.”</em>"),
    ("pietra", "Pietra — Pirra", "pietra", "pietra", "Pirra (despertando)", "Enfermeira do posto e da clínica",
     "A ponte. Escondida num bairro que alaga, caçada pela Frida. Sabe o caminho do subsolo. Relógio de atitude: aliada → instável → ameaça.",
     "<em>“Se ninguém cuidar deles, quem vai?”</em>"),
    ("enkidou", "Detetive Enkidou", "enkidou", None, "", "Detetive responsável pelo caso",
     "Viu a banheira, sabe que não foi acidente e foi mandada arquivar. Não pode registrar Mythos como prova.",
     "<em>“Torneira fechada. Banheira cheia. Água de rio. Me explica.”</em>"),
    ("otavio", "Otávio Brandt", "otavio", None, "", "Editor do jornal",
     "Cansado e defensivo. Publicou os cadernos vazados.", "<em>“O Elias vendia jornal. Ninguém aqui gostava dele.”</em>"),
    ("sueli", "Vereadora Sueli Marques", "sueli", None, "", "Exposta pela coluna",
     "Reabilitada depois do vazamento dos cadernos. Suspeita falsa.", "<em>“Palavras de um louco. A cidade finalmente sabe.”</em>"),
    ("lourival", "Seu Lourival", "lourival", None, "", "Porteiro do prédio do Elias",
     "Ouviu a água correr na noite do crime.", "<em>“A água do prédio tava cortada desde as dez.”</em>"),
    ("celina", "Dona Celina", "celina", None, "", "Moradora do bloco de baixo do Residencial",
     "Grata e devota ao professor.", "<em>“Ele salvou a minha família.”</em>"),
]
for key, name, tok, por, myth, logos, bio, fala in NPCS:
    ACTORS.append(actor(key, name, "npc", tok, por, myth, logos, "", P(bio, fala), disposition=0))
AID = {a["_id"]: a for a in ACTORS}
A = {a_k: gid("actor", a_k) for a_k in ["natan", "jade", "frida", "seg", "bruno", "correnteza", "ararate",
                                         "elias", "pietra", "enkidou", "otavio", "sueli", "lourival", "celina"]}

# ------------------------------------------------------------------ cenas
def scene(key, name, fold, img, w, h, grid=100, battle=False, walls=(), lights=(), tokens=(), darkness=0.0, weather="",
          sort=0, thumb=None):
    sid = gid("scene", key)
    return {
        "_id": sid, "name": name, "folder": F[fold]["_id"], "sort": sort, "navigation": False, "navOrder": sort, "navName": "",
        "active": False, "img": None,
        "background": {"src": img, "anchorX": 0.5, "anchorY": 0.5, "offsetX": 0, "offsetY": 0, "fit": "fill",
                       "scaleX": 1, "scaleY": 1, "rotation": 0, "tint": "#ffffff", "alphaThreshold": 0},
        "foreground": None, "foregroundElevation": 20,
        "thumb": thumb or img.replace("/cenas/", "/thumbs/").replace("/mapas/", "/thumbs/mapa-"),
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
        see = 0 if kind in ("glass", "rail") else 20
        out.append({"_id": gid(skey, "w", str(i), str(j)), "c": c, "move": 20, "sight": see, "light": see,
                    "sound": 0 if kind in ("glass", "rail") else 20, "door": {"door": 1, "secret": 2}.get(kind, 0), "ds": 0,
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
AMB = [("capa", "0.1 Capa", "capa-do-caso", 1792, 2688, "rain"),
       ("abertura", "0.2 Abertura", "abertura-do-caso", 1792, 2688, "rain"),
       ("cortinas", "0.3 A cidade sob a chuva", "por-tras-das-cortinas", 2688, 1792, "rain"),
       ("delegacia", "0.4 Delegacia na chuva", "delegacia-na-chuva", 2688, 1792, "rain"),
       ("apartamento", "1.1 Apartamento do Elias", "apartamento-do-elias", 2912, 1632, "rain"),
       ("redacao", "1.2 Redação do jornal", "redacao-do-jornal", 2912, 1632, "rain"),
       ("gabinete", "1.3 Gabinete da vereadora", "gabinete-da-vereadora", 2912, 1632, "rain"),
       ("rua", "1.4 A rua alagada", "a-rua-alagada", 2912, 1632, "rainStorm"),
       ("aguas", "1.5 Águas de Jade", "aguas-de-jade", 2912, 1632, ""),
       ("enterro", "1.6 O enterro na chuva", "o-enterro-na-chuva", 2944, 1648, "rain"),
       ("bairro", "2.1 Bairro alagado", "bairro-alagado", 2944, 1648, "rain"),
       ("reservada", "2.2 Sala reservada das Águas de Jade", "sala-reservada-das-aguas-de-jade", 2944, 1648, ""),
       ("professor", "2.3 Sala do professor", "sala-do-professor", 2944, 1648, "rain"),
       ("residencial", "2.4 Residencial Monte Ararate", "residencial-monte-ararate", 2944, 1648, "rain"),
       ("triagem", "2.5 Sala da triagem", "sala-da-triagem", 2944, 1648, "rain"),
       ("posto", "3.1 Posto de saúde", "posto-de-saude", 2944, 1648, "rain"),
       ("van", "3.2 A van na madrugada", "a-van-na-madrugada", 2944, 1648, "rainStorm"),
       ("clinica", "3.3 Instituto Fólkvangr — a clínica", "a-clinica", 2944, 1648, "rain"),
       ("subsolo", "3.4 O subsolo", "o-subsolo", 3824, 2144, ""),
       ("escritorio", "3.5 Escritório da diretora", "escritorio-da-diretora", 2944, 1648, "rain"),
       ("fechadas", "4.1 Águas de Jade fechadas", "aguas-de-jade-fechadas", 2912, 1632, ""),
       ("portas", "4.2 As portas do Ararate", "as-portas-do-ararate", 1456, 816, "rainStorm"),
       ("epilogo", "4.3 Primeira manhã seca", "primeira-manha-seca", 2912, 1632, ""),
       ("contracapa", "Fim — Contracapa", "contracapa", 1792, 2688, "rain")]
for i, (k, n, img, w, h, wx) in enumerate(AMB):
    SCENES.append(scene(k, n, "amb", f"{AS}/cenas/{img}.webp", w, h, weather=wx, sort=i * 10))

WARM = "#ffcc66"; AMBER = "#ffb347"; WHITE = "#ffffff"; TEAL = "#3fd0dc"; PINK = "#ff7bd0"; RED = "#ff2a2a"

# --- 2.1 Bairro alagado (2496x1664; exibição 1200 -> 2.08)
s = 2496 / 1200
k = "map-bairro"
SCENES.append(scene(k, "2.1 Bairro alagado", "map", f"{AS}/mapas/bairro-alagado.webp", 2496, 1664,
    grid=100, battle=True, darkness=0.6, weather="rain", sort=10,
    walls=walls(k, s, [
        ("wall", [(0, 298), (150, 298)]), ("door", [(150, 298), (190, 298)]), ("wall", [(190, 298), (300, 298)]),
        ("door", [(300, 298), (340, 298)]), ("wall", [(340, 298), (600, 298)]), ("door", [(600, 298), (645, 298)]),
        ("wall", [(645, 298), (780, 298)]), ("door", [(780, 298), (825, 298)]), ("wall", [(825, 298), (1000, 298)]),
        ("wall", [(1000, 298), (1000, 0)]), ("wall", [(1158, 0), (1158, 600)]),
        ("wall", [(0, 632), (405, 632)]), ("door", [(405, 632), (435, 632)]), ("wall", [(435, 632), (660, 632)]),
        ("door", [(660, 632), (695, 632)]), ("wall", [(695, 632), (1200, 632)]),
        ("rail", [(0, 590), (360, 590)]), ("rail", [(490, 590), (700, 590)]),
    ]),
    lights=[L(k, 0, 110, 268, s, 6, 2, AMBER, 0.3), L(k, 1, 885, 268, s, 6, 2, AMBER, 0.3),
            L(k, 2, 170, 180, s, 2, 1, WARM, 0.25), L(k, 3, 320, 180, s, 2, 1, WARM, 0.25), L(k, 4, 455, 180, s, 2, 1, WARM, 0.25),
            L(k, 5, 625, 250, s, 3, 1, WARM, 0.25, "torch"), L(k, 6, 800, 165, s, 2, 1, WARM, 0.25),
            L(k, 7, 545, 705, s, 2, 1, WARM, 0.25), L(k, 8, 210, 720, s, 2, 1, WARM, 0.25),
            L(k, 9, 1000, 545, s, 4, 1, WHITE, 0.15)],
    tokens=[T(k, 0, "pietra", 625, 330, s, 100, True), T(k, 1, "seg", 1000, 470, s, 100, True),
            T(k, 2, "seg", 1110, 470, s, 100, True), T(k, 3, "correnteza", 520, 440, s, 100, True)]))

# --- 3.2 A van na madrugada (3520x2352; 2.9333)
s = 3520 / 1200
k = "map-van"
SCENES.append(scene(k, "3.2 A van na madrugada", "map", f"{AS}/mapas/a-van-na-madrugada.webp", 3520, 2352,
    grid=120, battle=True, darkness=0.7, weather="rainStorm", sort=20,
    walls=walls(k, s, [
        ("rail", [(150, 150), (500, 150)]), ("wall", [(500, 100), (555, 100)]), ("door", [(555, 100), (715, 100)]),
        ("wall", [(715, 100), (760, 100)]), ("rail", [(760, 160), (1200, 160)]),
    ]),
    lights=[L(k, 0, 205, 230, s, 6, 2, AMBER, 0.3), L(k, 1, 1015, 580, s, 6, 2, AMBER, 0.3),
            L(k, 2, 440, 60, s, 3, 1, WARM, 0.25), L(k, 3, 535, 65, s, 3, 1, WARM, 0.25), L(k, 4, 725, 80, s, 3, 1, WARM, 0.25),
            L(k, 5, 920, 365, s, 3, 1, WARM, 0.2), L(k, 6, 310, 250, s, 2, 1, WARM, 0.2), L(k, 7, 440, 230, s, 2, 1, WARM, 0.2),
            L(k, 8, 330, 555, s, 2, 1, WARM, 0.2), L(k, 9, 215, 575, s, 2, 1, WARM, 0.2),
            L(k, 10, 440, 630, s, 6, 3, WHITE, 0.25), L(k, 11, 612, 662, s, 2, 1, RED, 0.35)],
    tokens=[T(k, 0, "bruno", 520, 700, s, 120, True), T(k, 1, "seg", 600, 170, s, 120, True)]))

# --- 3.4 O subsolo (3520x2352)
k = "map-subsolo"
SCENES.append(scene(k, "3.4 O subsolo", "map", f"{AS}/mapas/o-subsolo.webp", 3520, 2352,
    grid=120, battle=True, darkness=0.6, sort=30,
    walls=walls(k, s, [
        ("wall", [(25, 40), (1165, 40), (1165, 440)]), ("wall", [(25, 40), (25, 610), (100, 610), (100, 790), (860, 790)]),
        ("wall", [(100, 192), (160, 192)]), ("door", [(160, 192), (195, 192)]), ("wall", [(195, 192), (285, 192)]),
        ("door", [(285, 192), (320, 192)]), ("wall", [(320, 192), (420, 192)]), ("door", [(420, 192), (455, 192)]),
        ("wall", [(455, 192), (495, 192)]), ("door", [(495, 192), (555, 192)]), ("wall", [(555, 192), (580, 192), (580, 40)]),
        ("wall", [(600, 40), (600, 232), (650, 232)]), ("door", [(650, 232), (690, 232)]), ("wall", [(690, 232), (880, 232)]),
        ("glass", [(880, 232), (980, 232)]), ("wall", [(980, 232), (1165, 232)]),
        ("wall", [(590, 275), (1165, 275)]), ("wall", [(590, 275), (590, 392), (690, 392)]), ("door", [(690, 392), (725, 392)]),
        ("wall", [(725, 392), (870, 392)]), ("door", [(870, 392), (905, 392)]), ("wall", [(905, 392), (1040, 392)]),
        ("door", [(1040, 392), (1075, 392)]), ("wall", [(1075, 392), (1165, 392)]),
        ("wall", [(825, 275), (825, 392)]), ("wall", [(1000, 275), (1000, 392)]),
        ("wall", [(25, 232), (330, 232)]), ("wall", [(370, 232), (370, 340)]), ("door", [(370, 340), (370, 370)]),
        ("wall", [(370, 370), (370, 385), (255, 385)]), ("door", [(255, 385), (220, 385)]), ("wall", [(220, 385), (25, 385)]),
        ("wall", [(350, 240), (455, 240), (455, 300), (380, 300)]),
        ("wall", [(25, 395), (393, 395), (393, 490)]), ("door", [(393, 490), (393, 530)]), ("wall", [(393, 530), (393, 600), (25, 600)]),
        ("wall", [(440, 445), (480, 445)]), ("door", [(480, 445), (515, 445)]), ("wall", [(515, 445), (665, 445), (665, 600), (620, 600)]),
        ("door", [(620, 600), (590, 600)]), ("wall", [(590, 600), (440, 600), (440, 445)]),
        ("wall", [(675, 440), (725, 440)]), ("door", [(725, 440), (760, 440)]), ("wall", [(760, 440), (880, 440)]),
        ("door", [(880, 440), (915, 440)]), ("wall", [(915, 440), (1020, 440)]), ("door", [(1020, 440), (1055, 440)]),
        ("wall", [(1055, 440), (1145, 440), (1145, 590), (675, 590), (675, 440)]),
        ("wall", [(855, 440), (855, 590)]), ("wall", [(975, 440), (975, 590)]),
        ("wall", [(110, 645), (180, 645)]), ("door", [(180, 645), (215, 645)]), ("wall", [(215, 645), (320, 645)]),
        ("door", [(320, 645), (355, 645)]), ("wall", [(355, 645), (470, 645)]), ("door", [(470, 645), (530, 645)]),
        ("wall", [(530, 645), (640, 645)]), ("door", [(640, 645), (675, 645)]), ("wall", [(675, 645), (800, 645)]),
        ("door", [(800, 645), (830, 645)]), ("wall", [(830, 645), (860, 645), (860, 790)]),
    ]),
    lights=[L(k, i, x, y, s, 3, 1, WHITE, 0.12) for i, (x, y) in enumerate(
                [(300, 215), (450, 215), (700, 255), (900, 255), (1050, 255), (420, 330), (420, 450), (500, 420),
                 (700, 420), (900, 420), (1050, 420), (300, 620), (500, 620), (700, 620)])]
        + [L(k, 20, 900, 110, s, 6, 2, PINK, 0.3), L(k, 21, 660, 720, s, 2, 1, "#b57bff", 0.35, "pulse"),
           L(k, 22, 715, 720, s, 2, 1, "#b57bff", 0.35, "pulse"), L(k, 23, 770, 720, s, 2, 1, "#b57bff", 0.35, "pulse"),
           L(k, 24, 60, 300, s, 3, 1, PINK, 0.35, "pulse"), L(k, 25, 90, 410, s, 2, 1, WARM, 0.25),
           L(k, 26, 345, 575, s, 2, 1, WARM, 0.25), L(k, 27, 560, 480, s, 3, 1, TEAL, 0.3)],
    tokens=[T(k, 0, "bruno", 520, 240, s, 120, True), T(k, 1, "seg", 520, 330, s, 120, True),
            T(k, 2, "seg", 470, 620, s, 120, True), T(k, 3, "seg", 900, 420, s, 120, True)]))

# --- 4.2 As portas do Ararate (3520x2352)
k = "map-portas"
SCENES.append(scene(k, "4.2 As portas do Ararate", "map", f"{AS}/mapas/as-portas-do-ararate.webp", 3520, 2352,
    grid=120, battle=True, darkness=0.55, weather="rainStorm", sort=40,
    walls=walls(k, s, [
        ("rail", [(60, 375), (295, 375)]), ("door", [(295, 375), (460, 375)]), ("rail", [(460, 375), (740, 375)]),
        ("door", [(740, 375), (905, 375)]), ("rail", [(905, 375), (1140, 375)]),
        ("wall", [(380, 140), (570, 140)]), ("door", [(570, 140), (630, 140)]), ("wall", [(630, 140), (830, 140)]),
        ("rail", [(220, 555), (360, 465)]), ("rail", [(410, 550), (560, 575), (790, 560)]), ("rail", [(855, 465), (990, 555)]),
    ]),
    lights=[L(k, i, x, y, s, 3, 1, TEAL, 0.3) for i, (x, y) in enumerate([(550, 320), (600, 320), (650, 320), (560, 435), (640, 435)])]
        + [L(k, 10, 215, 435, s, 6, 3, WHITE, 0.2), L(k, 11, 995, 435, s, 6, 3, WHITE, 0.2)]
        + [L(k, 20 + i, x, y, s, 3, 1, AMBER, 0.3) for i, (x, y) in enumerate(
            [(180, 595), (350, 610), (875, 580), (1030, 655), (1110, 605), (530, 690), (720, 665), (795, 730), (905, 705),
             (565, 775), (285, 750), (380, 715)])]
        + [L(k, 40 + i, x, y, s, 2, 1, WARM, 0.25) for i, (x, y) in enumerate(
            [(185, 130), (1015, 130), (600, 90), (120, 355), (310, 355), (485, 355), (720, 355), (1085, 355)])],
    tokens=[T(k, 0, "natan", 600, 505, s, 120), T(k, 1, "ararate", 300, 620, s, 120), T(k, 2, "ararate", 450, 640, s, 120),
            T(k, 3, "ararate", 650, 640, s, 120), T(k, 4, "ararate", 800, 620, s, 120), T(k, 5, "ararate", 950, 600, s, 120),
            T(k, 6, "seg", 420, 340, s, 120, True), T(k, 7, "seg", 780, 340, s, 120, True),
            T(k, 8, "jade", 200, 700, s, 120, True)]))
SC = {sc["_id"]: sc for sc in SCENES}
S = {sc_k: gid("scene", sc_k) for sc_k in [a[0] for a in AMB] + ["map-bairro", "map-van", "map-subsolo", "map-portas"]}

# ------------------------------------------------------------------ journal
md = open(os.path.join(ROOT, "src", CASE, "caso.md"), encoding="utf-8").read()
md = re.sub(r"^# O Som da Chuva\n+.*?@\w+\n", "", md, flags=re.S)
md = re.sub(r"^\*\*Estilo visual\.\*\*.*\n", "", md, flags=re.M)
md = re.sub(r"^\*Um caso de City of Mist.*?\*\n", "", md, flags=re.M)
md = md.split("\n## Créditos")[0]
# blockquotes seguidos não podem se fundir
_l = md.split("\n"); _o = []
for _i, _ln in enumerate(_l):
    _o.append(_ln)
    if _ln == "" and _i > 0 and _l[_i - 1].startswith(">") and _i + 1 < len(_l) and _l[_i + 1].startswith(">"):
        _o.append("<!-- -->"); _o.append("")
md = "\n".join(_o)

PORTRAITS = {"elias-lil", "madame-jade", "prof-natan-arcanjo", "dra-frida-vanir", "pietra"}
ART_SCENE = {"por-tras-das-cortinas": "cortinas", "delegacia-na-chuva": "delegacia",
             "apartamento-do-elias-ambientacao": "apartamento", "redacao-do-jornal-ambientacao": "redacao",
             "gabinete-da-vereadora-ambientacao": "gabinete", "a-rua-alagada-ambientacao": "rua",
             "aguas-de-jade-ambientacao": "aguas", "o-enterro-na-chuva-ambientacao": "enterro",
             "bairro-alagado-ambientacao": "bairro", "bairro-alagado-battlemap": "map-bairro",
             "sala-reservada-das-aguas-de-jade-ambientacao": "reservada", "sala-do-professor-ambientacao": "professor",
             "residencial-monte-ararate-ambientacao": "residencial", "sala-da-triagem-ambientacao": "triagem",
             "posto-de-saude-ambientacao": "posto", "a-van-na-madrugada-ambientacao": "van",
             "a-van-na-madrugada-battlemap": "map-van", "a-clinica-ambientacao": "clinica",
             "o-subsolo-ambientacao": "subsolo", "o-subsolo-battlemap": "map-subsolo",
             "escritorio-da-diretora-ambientacao": "escritorio", "aguas-de-jade-fechadas-ambientacao": "fechadas",
             "as-portas-do-ararate-ambientacao": "portas", "as-portas-do-ararate-battlemap": "map-portas",
             "primeira-manha-seca-ambientacao": "epilogo"}


def link_scene(key):
    sc = SC[S[key]]
    return f'<p class="adc-cap">@UUID[Scene.{sc["_id"]}]{{Abrir a cena: {sc["name"]}}}</p>'


def fig(m):
    s_ = slug(m.group(1))
    if s_ in PORTRAITS:
        return f'\n<div class="adc-portrait"><img src="{AS}/retratos/{s_}.webp"></div>\n'
    key = ART_SCENE.get(s_)
    if key is None:
        return "\n"
    sc = SC[S[key]]
    cls = "adc-fig adc-map" if key.startswith("map-") else "adc-fig"
    return f'\n<figure class="{cls}"><img src="{sc["background"]["src"]}"></figure>{link_scene(key)}\n'


md = re.sub(r"> \*\*Arte — (.+?)\*\*\s*\n+```text\n.*?```", fig, md, flags=re.S)
html = markdown.markdown(md, extensions=["tables", "sane_lists"])


def bq(m):
    inner = m.group(1)
    txt = re.sub("<.*?>", "", inner).strip()
    cls = "adc-box"
    for key, c in [("Leia em voz alta", "adc-aloud"), ("Post-it", "adc-postit"), ("Resumo", "adc-summary")]:
        if txt.startswith(key):
            cls = c
            break
    if cls == "adc-postit":
        inner = re.sub(r"<p><strong>Post-it — Dicas</strong></p>", '<p class="adc-postit-h">Dicas</p>', inner)
    return f'<blockquote class="{cls}">{inner}</blockquote>'


html = re.sub(r"<blockquote>(.*?)</blockquote>", bq, html, flags=re.S)
html = re.sub(r"<p><strong>(Falas[^<]*)</strong></p>\s*<ul>(.*?)</ul>",
              r'<div class="adc-falas"><p class="adc-falas-h">\1</p><ul>\2</ul></div>', html, flags=re.S)
html = re.sub(r'(<h3>[^<]*</h3>)((?:(?!<h3>).)*?)(<div class="adc-portrait"><img src="[^"]+"></div>)',
              lambda m: m.group(1) + m.group(3) + m.group(2), html, flags=re.S)
html = re.sub(r"(?<=[.”)\"]) <strong>(Mythos|Mythos \(despertando\)|Quer|Queria|Tem|Como interpretar):</strong>",
              r"<br><strong>\1:</strong>", html)


def actor_link(key, label="Abrir a ficha"):
    return f'<p class="adc-cap">@UUID[Actor.{A[key]}]{{{label}}}</p>'


for prefix, key in [("Elias Lil", "elias"), ("Madame Jade", "jade"), ("Prof. Dr. Natan Arcanjo", "natan"),
                    ("Dra. Frida Vanir", "frida"), ("Pietra", "pietra"), ("Detetive Enkidou", "enkidou")]:
    html = re.sub(r"(<h3>" + re.escape(prefix) + r"[^<]*</h3>)", lambda m: m.group(1) + actor_link(key), html, count=1)
html = html.replace("<h3>Figurantes</h3>", "<h3>Figurantes</h3>" + "".join(
    f'<p class="adc-cap">@UUID[Actor.{A[k_]}]{{{n_}}}</p>' for k_, n_ in
    [("otavio", "Otávio Brandt"), ("sueli", "Vereadora Sueli"), ("lourival", "Seu Lourival"), ("celina", "Dona Celina")]), 1)
for title, key in [("Madame Jade, a intermediária", "jade"), ("Prof. Natan Arcanjo, o benfeitor", "natan"),
                   ("Dra. Frida Vanir, a cientista", "frida"), ("A multidão do Ararate", "ararate"),
                   ("Seguranças da Frida (2.1, 3.2, 3.4)", "seg"), ("Bruno, chefe da segurança", "bruno"),
                   ("Correnteza (1.4, 2.1, 4.2)", "correnteza"), ("Seguranças e moradores fiéis do Residencial (4.2)", "ararate")]:
    html = re.sub(r"(<p><strong>" + re.escape(title) + r"</strong>[^<]*</p>)", lambda m: m.group(1) + actor_link(key), html, count=1)

OPEN = {"Visão geral": "abertura-do-caso", "Ganchos": "delegacia-na-chuva", "Sessão 1": "a-rua-alagada",
        "Sessão 2": "bairro-alagado", "Sessão 3": "a-clinica", "Sessão 4": "as-portas-do-ararate",
        "Apêndice": "residencial-monte-ararate"}
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
        body = f'<figure class="adc-hero"><img src="{AS}/cenas/{hero}.webp"></figure>' + body
    pages.append((title, body))
    if title.startswith("Ganchos"):
        pages.append(("O Iceberg do Caso", f'<figure class="adc-fig"><img src="{AS}/journal/iceberg.webp"></figure>'
                      '<p>Cada fio vermelho é uma saída: de uma cena, a galera pode seguir para qualquer polaroide ligada a ela. Os post-its marcam as viradas entre as camadas.</p>'))

JID = gid("journal", "guia")
journal = {
    "_id": JID, "name": "O Som da Chuva — Guia do MC", "folder": F["jou"]["_id"], "sort": 0, "categories": [],
    "pages": [{"_id": gid("page", t), "name": re.sub("<.*?>", "", t), "type": "text", "sort": (i + 1) * 100000,
               "title": {"show": True, "level": 1},
               "text": {"format": 1, "content": f'<div class="mesa-alta o-som-da-chuva">{b}</div>', "markdown": ""},
               "image": {}, "video": {"controls": True, "volume": 0.5}, "src": None, "system": {},
               "ownership": {"default": -1}, "flags": {}, "_stats": STATS, "category": None}
              for i, (t, b) in enumerate(pages)],
    "ownership": {"default": 0}, "flags": {}, "_stats": STATS}

# ------------------------------------------------------------------ aventura
ADV = gid("adventure", CASE)
adventure = {
    "_id": ADV, "_key": f"!adventures!{ADV}", "name": "O Som da Chuva", "img": f"{AS}/cenas/capa-do-caso.webp",
    "caption": "Um caso de City of Mist em quatro sessões",
    "description": "<p>Chove há 35 dias. Elias Lil, o colunista que ouvia a cidade inteira, morreu afogado na própria banheira, e a polícia arquivou como acidente. No alto do morro, um professor gentil abre as portas do Residencial Monte Ararate para quem precisa de abrigo. Faltam cinco dias para a arca se fechar. Depois disso, a chuva não para nunca mais.</p>"
                   f"<p>Importa: o Guia do MC completo com o iceberg do caso, {len(AMB)} cenas de ambientação com chuva, 4 battlemaps com paredes, portas e luzes, "
                   "7 Perigos com espectros, travas e movimentos, 7 NPCs e tokens já posicionados (adversários ocultos).</p>",
    "actors": ACTORS, "combats": [], "items": [], "journal": [journal], "scenes": SCENES, "tables": [], "macros": [],
    "cards": [], "playlists": [], "folders": list(ROOT_F.values()) + list(F.values()), "sort": 20, "flags": {}, "_stats": STATS, "folder": None}

os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    os.remove(os.path.join(OUT, f))
json.dump(adventure, open(os.path.join(OUT, "O_Som_da_Chuva.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("atores", len(ACTORS), "cenas", len(SCENES), "páginas", len(pages))
