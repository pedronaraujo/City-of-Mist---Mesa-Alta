"""Gera o JSON-fonte da aventura A Casa Sempre Ganha (Adventure) para o sistema city-of-mist.

Uso: python3 tools/build_a_casa_sempre_ganha.py && node tools/pack.mjs
"""
import hashlib, json, os, re, unicodedata
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASE = "a-casa-sempre-ganha"
MOD = "modules/mesa-alta"
AS = f"{MOD}/assets/{CASE}"
OUT = os.path.join(ROOT, "src", "packs", CASE)
STATS = {"systemId": "city-of-mist", "systemVersion": "4.5.3", "coreVersion": "13.351",
         "createdTime": 1795600000000, "modifiedTime": 1795600000000, "lastModifiedBy": None,
         "compendiumSource": None, "duplicateSource": None}


def gid(*parts):
    h = hashlib.sha1(("casasempreganha|" + "|".join(parts)).encode()).hexdigest()
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
CASE_COLOR = "#b8913a"
SUB = {"adv": ("Adversários", "#a8195f"), "npc": ("NPCs", "#0e6f78"), "amb": ("Ambientação", "#2b2540"), "map": ("Battlemaps", "#3a5a9c")}
ROOT_F = {"Actor": folder("A Casa Sempre Ganha", "Actor", CASE_COLOR), "Scene": folder("A Casa Sempre Ganha", "Scene", CASE_COLOR)}
F = {
    "adv": folder(SUB["adv"][0], "Actor", SUB["adv"][1], ROOT_F["Actor"]["_id"]),
    "npc": folder(SUB["npc"][0], "Actor", SUB["npc"][1], ROOT_F["Actor"]["_id"]),
    "amb": folder(SUB["amb"][0], "Scene", SUB["amb"][1], ROOT_F["Scene"]["_id"]),
    "map": folder(SUB["map"][0], "Scene", SUB["map"][1], ROOT_F["Scene"]["_id"]),
    "jou": folder("A Casa Sempre Ganha", "JournalEntry", CASE_COLOR),
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
    actor("victor", "Victor Gordian — Midas", "adv", "victor-gordian", "victor-gordian", "Midas",
          "Apostador elegante (e falido)", "O apostador que nunca perde. Preso a uma dívida com o Dênis.",
          P("Quarentão elegante, terno impecável, relógio de ouro e olheiras fundas. Ganha tudo e não sorri quando ganha. Aparece na Sessão 1 sem dizer quem é.",
            "<strong>Quer:</strong> parar, mas não consegue. No fundo, quer que alguém o obrigue a perder.",
            "<strong>Trava:</strong> Confissão fica em 2 até a galera mostrar que sabe da falência (extratos) e da dívida (áudios).",
            "<em>“Sorte é para quem perde. Eu só acerto.”</em>"),
          [("Confissão", 3)],
          [("custom", "Toque de Midas", "Tudo em que $name aposta acontece, custe o que custar. Só apostas sobre ele mesmo escapam do toque."),
           ("hard", "Aposta absurda", "$name aposta em algo impossível na cena, e acontece: algo se quebra, alguém se fere ou uma prova se perde."),
           ("hard", "Sumir", "$name paga a conta e vai embora antes que alguém pergunte o nome dele."),
           ("soft", "Piada seca", "$name faz uma piada sobre sorte e muda de assunto.", True),
           ("soft", "Pagar a rodada", "$name aposta que alguém vai pagar a próxima rodada. Viu? Ganhou de novo.", True)], disposition=0),
    actor("denis", "Dênis Bacarat — Dionísio", "adv", "denis-bacarat", "denis-bacarat", "Dionísio",
          "Dono do Tirso, casa noturna e cassino secreto", "Cobra a dívida de Victor e vende os resultados à Mesa Alta.",
          P("Bonito, sempre de taça na mão, nunca parece bêbado. Anfitrião perfeito: a ameaça vem sorrindo. Sem os favores de Victor, é descartável para a Mesa.",
            "<strong>Trava:</strong> Admitir o pacto fica em 3 sem os áudios do Fábio ou o caderno do agenciador. Humilhado diante do Plaut, pode mudar de lado.",
            "<em>“Ninguém sai do Tirso com sede. É a única regra da casa.”</em>"),
          [("Admitir o pacto", 4), ("Ferir ou Incapacitar", 3)],
          [("custom", "Êxtase", "Perto de $name, as pessoas perdem a noção do tempo e do limite."),
           ("hard", "Soltar as mênades", "A festa vira multidão frenética contra os PJs."),
           ("hard", "Mais uma taça", "Quem aceita a bebida dele recebe [embriagado-2] ou [perdido-no-tempo-2]."),
           ("hard", "A Mesa está olhando", "Marque dois segmentos na Paciência da Mesa."),
           ("soft", "Um drink", "$name oferece uma bebida que ninguém consegue recusar.", True),
           ("soft", "Amigos importantes", "$name cita amigos poderosos que não gostam de surpresas.", True)]),
    actor("plaut", "Augusto Plaut — Pluto", "adv", "augusto-plaut", "augusto-plaut", "Pluto",
          "Dono da Cornucópia Bet, membro da Mesa Alta", "Quem encomenda as apostas. Quer o Pactolo F.C. barato.",
          P("Empresário discreto, óculos escuros mesmo à noite. Fala de pessoas como números. Trata o Dênis como funcionário.",
            "<strong>Trava:</strong> Recuar fica em 4 sem o processo da Cornucópia Bet ligado às apostas. Atacá-lo em público faz a Mesa inteira olhar para os PJs.",
            "<em>“Eu não aposto. Eu sou a casa.”</em>"),
          [("Recuar", 5)],
          [("hard", "Chamar os seguranças", "Os Seguranças de Plaut entram na cena."),
           ("hard", "Sumir com uma testemunha", "Alguém que podia depor desaparece."),
           ("hard", "A imprensa", "A mídia vira contra os PJs: [desacreditado-2]."),
           ("soft", "Em números", "$name diz quanto um PJ vale.", True),
           ("soft", "Água com gás", "$name espera, calmo, que os PJs errem.", True)]),
    actor("silvano", "Silvano Arcádio — Pã", "adv", "silvano-arcadio", "silvano-arcadio", "Pã (despertando)",
          "Zagueiro do Sport Club Olímpico", "Suspeito plantado da morte de Davi. Desperta no meio do caso.",
          P("Viril e temperamental. Ameaçou Davi antes do jogo e estava colado nele no lance fatal. Viu o estádio inteiro parar por um segundo.",
            "<strong>Trava:</strong> Confiança fica em 1 enquanto alguém o tratar como suspeito.",
            "<strong>Relógio de atitude (oculto):</strong> aliado → instável → ameaça.",
            "<em>“Eu falei que ia parar ele. Não falei que ia matar!”</em>"),
          [("Confiança", 3), ("Ferir ou Incapacitar", 3)],
          [("custom", "Pânico de Pã", "Quando $name se irrita, quem está perto sente vontade de fugir."),
           ("hard", "Pânico", "Todos ao redor recebem [em-pânico-2]."),
           ("hard", "Explodir", "$name parte para cima de quem o acusa: [machucado-2]."),
           ("soft", "Recuar", "$name vira as costas e chuta a bola contra o alambrado.", True)], disposition=0),
    actor("menades", "Mênades", "adv", "menades", None, "", "Convidados do Tirso em êxtase",
          "Cena 3.3. Não são vilões, são pessoas fora de si.",
          P("Ferir a multidão tem peso moral. O melhor é quebrar o transe (desligar a música, cortar o vinho, usar o pânico de Silvano) ou fugir.",
            "<em>“Por que parar agora? A noite nem começou.”</em>"),
          [("Quebrar o transe", 4), ("Ferir ou Incapacitar", 3), ("Perder o controle", 3)],
          [("hard", "Frenesi", "[machucado-2] em todos ao redor."),
           ("hard", "Para o centro", "Um PJ é arrastado para o meio da multidão: [perdendo-o-controle-2]."),
           ("hard", "Pisotear", "Alguém cai e é pisoteado."),
           ("soft", "Dança", "Puxam um PJ para a dança.", True),
           ("soft", "Vinho", "Oferecem vinho e separam o grupo na pista.", True)], collective=3, disposition=0),
    actor("seg", "Seguranças de Plaut", "adv", "segurancas-plaut", None, "", "Homens de terno escuro, armados e silenciosos",
          "Paciência da Mesa cheia, porta do salão VIP (3.4).",
          P("Aparecem quando a Paciência da Mesa enche ou na porta do salão VIP. Atacar Plaut em público os coloca em ação."),
          [("Subjugar", 4), ("Ferir ou Incapacitar", 3)],
          [("hard", "Sacar a arma", "[ferido-3]."),
           ("hard", "Corredor de serviço", "Arrastam um PJ para o corredor de serviço."),
           ("hard", "Sumir com uma prova", "Uma prova desaparece."),
           ("soft", "Revistar", "Revistam e separam o grupo.", True),
           ("soft", "Escoltar", "Escoltam alguém para fora.", True)], collective=2),
    actor("torcida", "Torcida da Fúria do Rio", "adv", "torcida", None, "", "Organizada do Pactolo F.C.",
          "Cena 1.5. O objetivo é sair inteiro, não vencer.",
          P("Se provocada no protesto, vira uma onda de empurrões, sinalizadores e garrafas.",
            "<em>“Se o Pactolo cair, essa cidade pega fogo.”</em>"),
          [("Dispersar", 3), ("Ferir ou Incapacitar", 3)],
          [("hard", "Pisotear", "[machucado-2]."),
           ("hard", "Sinalizador", "[queimado-2]."),
           ("hard", "Chamar mais gente", "Chega mais torcida."),
           ("soft", "Cercar", "Encurralam os PJs contra o portão.", True),
           ("soft", "Arrancar o celular", "Alguém arranca o celular de um PJ.", True)], collective=3, disposition=0),
    actor("brandao", "Irmãos Brandão", "adv", "brandao", None, "", "Agiotas, credores de Victor",
          "Cena 2.3. Preferem negociar.",
          P("Grandes, pacientes e profissionais. Só partem para a violência se forem humilhados ou se Victor tentar fugir.",
            "<em>“A gente não tem pressa, doutor. Tem juros.”</em>"),
          [("Subjugar", 3), ("Convencer", 2)],
          [("hard", "Golpe pesado", "[machucado-2]."),
           ("hard", "Contra o vidro", "Arremessam alguém contra a parede de vidro da varanda: [ferido-3]."),
           ("soft", "Ameaçar Victor", "Ameaçam Victor na frente de todos.", True),
           ("soft", "Bloquear o elevador", "Quebram um objeto caro ou bloqueiam o elevador.", True)], collective=2),
]
NPCS = [
    ("fabio", "Fábio Junco", "fabio-junco", "fabio-junco", "", "Assistente pessoal de Victor",
     "O “barbeiro” do mito: grava áudios anônimos no aplicativo Juncos. Quer que Victor saia dessa vivo.",
     "<em>“Ele ganhou tudo e não tem nada. Vocês entendem isso?”</em>"),
    ("hugo", "Hugo Ambrosio", "hugo", None, "", "Preparador físico do Pactolo",
     "Suspeito plantado: dava suplementos importados sem registro, irregulares mas inofensivos.",
     "<em>“Era só vitamina! Eu dou para o time inteiro!”</em>"),
    ("wellington", "Wellington Souza", "wellington", None, "", "Garçom do buffet",
     "Suspeito plantado da morte do prefeito. Fugiu porque trabalhava sem registro.",
     "<em>“Eu só servi o canapé, moço. O homem engasgou sozinho.”</em>"),
    ("epidauro", "Dr. Caio Epidauro", "epidauro", None, "", "Médico do Pactolo",
     "Os exames de Davi eram perfeitos. Pode contratar a galera.",
     "<em>“Eu assino embaixo: aquele coração não tinha nada.”</em>"),
    ("tavares", "Marcos Tavares", "tavares", None, "", "Prefeito eleito",
     "Político medíocre e dormente, comprado pela Mesa.", "<em>“Foi uma tragédia, mas a cidade precisa seguir em frente.”</em>"),
    ("helena", "Dra. Helena Moura", "helena", None, "", "Juíza do processo da Cornucópia Bet",
     "Pode ser salva na cena 2.5, mas é afastada por saúde. Salva, vira testemunha contra Plaut.",
     "<em>“Não me importa quem é o dono. Fraude é fraude.”</em>"),
]
for key, name, tok, por, myth, logos, bio, fala in NPCS:
    ACTORS.append(actor(key, name, "npc", tok, por, myth, logos, "", P(bio, fala), disposition=0))
AID = {a["_id"]: a for a in ACTORS}
A = {a_k: gid("actor", a_k) for a_k in ["victor", "denis", "plaut", "silvano", "menades", "seg", "torcida", "brandao",
                                         "fabio", "hugo", "wellington", "epidauro", "tavares", "helena"]}


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
V, H = (1792, 2688), (2944, 1648)
AMB = [("capa", "0.1 Capa", "capa-do-caso", *V, "rain"),
       ("abertura", "0.2 Abertura", "abertura-do-caso", *V, ""),
       ("cortinas", "0.3 Por trás das cortinas", "por-tras-das-cortinas", *H, ""),
       ("ganchos", "0.4 Ganchos — Departamento médico do Pactolo", "departamento-medico-do-pactolo", *H, "rain"),
       ("estadio", "1.1 Estádio do Pactolo", "estadio-do-pactolo", *H, "rain"),
       ("medico", "1.2 Departamento médico", "departamento-medico", *H, "rain"),
       ("vestiario", "1.3 Vestiário do Pactolo", "vestiario-do-pactolo", *H, ""),
       ("ct", "1.4 CT do Olímpico", "ct-do-olimpico", *H, ""),
       ("protesto", "1.5 Portão do Pactolo — o protesto da torcida", "protesto-da-torcida", *H, "rain"),
       ("apostas", "1.6 Casa de apostas clandestina", "casa-de-apostas-clandestina", *H, ""),
       ("bar", "1.7 Fim da sessão — Mesa de bar", "mesa-de-bar", *H, "rainStorm"),
       ("festa", "2.1 O vídeo da festa do partido", "festa-do-partido", *H, ""),
       ("buffet", "2.2 Buffet do partido", "buffet-do-partido", *H, "rain"),
       ("cobertura", "2.3 Cobertura de Victor", "cobertura-de-victor", *H, "rain"),
       ("audios", "2.4 Os áudios de Fábio Junco", "audios-de-fabio-junco", *H, "rain"),
       ("forum", "2.5 Fórum — a juíza", "forum", *H, "rain"),
       ("tirso-dia", "2.6 Tirso, de dia", "tirso-de-dia", *H, ""),
       ("convite", "2.7 A virada — o convite", "o-convite", *H, ""),
       ("esconderijo", "3.1 O esconderijo de Fábio", "esconderijo-de-fabio", *H, "rain"),
       ("chegada", "3.2 Chegada ao Tirso", "chegada-ao-tirso", *H, "rain"),
       ("pista", "3.3 A pista — as mênades", "pista-do-tirso", *H, ""),
       ("vip", "3.4 Salão VIP", "salao-vip", *H, ""),
       ("bacara", "3.5 Mesa de bacará — a última aposta", "mesa-de-bacara", *H, ""),
       ("epilogo", "3.6 Epílogo — a última rodada", "epilogo", *H, ""),
       ("contracapa", "Fim — Contracapa", "contracapa", *V, "rain")]
for i, (k, n, img, w, h, wx) in enumerate(AMB):
    SCENES.append(scene(k, n, "amb", f"{AS}/cenas/{img}.webp", w, h, weather=wx, sort=i * 10))

WARM = "#ffcc66"; AMBER = "#ffb347"; WHITE = "#ffffff"; TEAL = "#3fd0dc"; PURPLE = "#b57bff"; RED = "#ff4a4a"; GOLD = "#ffd27a"

s = 3520 / 1200  # mapas 3520x2352 exibidos com 1200 px

# --- 2.3 Cobertura de Victor
k = "map-cobertura"
SCENES.append(scene(k, "2.3 Cobertura de Victor", "map", f"{AS}/mapas/cobertura-de-victor.webp", 3520, 2352,
    grid=120, battle=True, darkness=0.5, weather="rain", sort=10,
    walls=walls(k, s, [
        ("rail", [(65, 195), (65, 75), (1140, 75), (1140, 190)]),
        ("wall", [(30, 210), (30, 620), (135, 620), (135, 635), (375, 635), (375, 700), (820, 700), (820, 690), (1170, 690), (1170, 190), (1060, 190)]),
        ("wall", [(30, 210), (300, 210), (300, 250), (345, 250), (345, 285), (365, 285)]),
        ("glass", [(365, 280), (420, 230), (500, 207), (565, 200), (640, 205), (710, 222), (760, 262)]),
        ("wall", [(760, 262), (840, 262), (840, 190), (870, 190)]), ("door", [(870, 190), (905, 190)]), ("wall", [(905, 190), (1060, 190)]),
        ("wall", [(320, 285), (320, 345)]), ("door", [(320, 345), (320, 400)]),
        ("wall", [(320, 400), (320, 520), (400, 520), (400, 545), (530, 545)]), ("door", [(530, 545), (600, 545)]),
        ("wall", [(600, 545), (700, 545), (700, 530), (735, 530)]),
        ("wall", [(30, 540), (95, 540)]), ("door", [(95, 540), (130, 540)]), ("wall", [(130, 540), (140, 540), (140, 620)]),
        ("wall", [(140, 540), (225, 540)]), ("door", [(225, 540), (265, 540)]), ("wall", [(265, 540), (285, 540), (285, 635)]),
        ("wall", [(400, 590), (400, 700)]), ("wall", [(720, 590), (720, 700)]),
        ("wall", [(735, 335), (735, 560), (800, 560)]), ("door", [(800, 560), (835, 560)]), ("wall", [(835, 560), (880, 560), (880, 340), (800, 340)]),
        ("wall", [(895, 340), (895, 520)]), ("door", [(895, 520), (895, 560)]), ("wall", [(895, 560), (895, 690)]),
        ("wall", [(895, 375), (940, 375)]), ("door", [(940, 375), (975, 375)]), ("wall", [(975, 375), (1170, 375)]),
        ("wall", [(895, 520), (940, 520)]), ("door", [(940, 520), (975, 520)]), ("wall", [(975, 520), (1170, 520)]),
    ]),
    lights=[L(k, 0, 615, 125, s, 5, 2, TEAL, 0.3), L(k, 1, 190, 165, s, 3, 1, AMBER, 0.3, "torch"),
            L(k, 2, 200, 450, s, 4, 2, WARM, 0.25), L(k, 3, 200, 335, s, 3, 1, WARM, 0.2),
            L(k, 4, 520, 360, s, 4, 2, WARM, 0.2), L(k, 5, 655, 420, s, 3, 1, WARM, 0.2),
            L(k, 6, 815, 470, s, 3, 1, AMBER, 0.3), L(k, 7, 1045, 290, s, 3, 1, WARM, 0.25),
            L(k, 8, 1060, 440, s, 3, 1, WARM, 0.2), L(k, 9, 1030, 580, s, 3, 1, WARM, 0.2),
            L(k, 10, 560, 640, s, 3, 1, WARM, 0.25), L(k, 11, 920, 140, s, 3, 1, WARM, 0.2)],
    tokens=[T(k, 0, "victor", 1050, 300, s, 120, True), T(k, 1, "brandao", 505, 640, s, 120, True),
            T(k, 2, "brandao", 620, 640, s, 120, True)]))

# --- 3.3 Tirso
k = "map-tirso"
SCENES.append(scene(k, "3.3 Tirso", "map", f"{AS}/mapas/tirso.webp", 3520, 2352,
    grid=120, battle=True, darkness=0.6, sort=20,
    walls=walls(k, s, [
        ("wall", [(35, 550), (480, 550)]), ("door", [(480, 550), (680, 550)]), ("wall", [(680, 550), (1110, 550)]),
        ("wall", [(35, 550), (35, 40), (400, 40), (400, 10), (745, 10), (745, 40), (855, 40), (855, 30), (1110, 30), (1110, 250)]),
        ("door", [(1110, 250), (1110, 280)]), ("wall", [(1110, 280), (1110, 550)]),
        ("rail", [(440, 145), (745, 145)]),
        ("wall", [(855, 40), (855, 215), (965, 215)]), ("door", [(965, 215), (1000, 215)]), ("wall", [(1000, 215), (1030, 215), (1030, 200)]),
        ("door", [(1030, 200), (1030, 165)]), ("wall", [(1030, 165), (1030, 30)]),
        ("wall", [(855, 215), (855, 290)]), ("door", [(855, 290), (855, 330)]), ("wall", [(855, 330), (855, 450)]),
        ("door", [(855, 450), (855, 485)]), ("wall", [(855, 485), (855, 550)]),
        ("wall", [(905, 300), (905, 260), (1030, 260), (1030, 470), (905, 470), (905, 440)]), ("door", [(905, 440), (905, 410)]),
        ("wall", [(905, 410), (905, 330)]), ("door", [(905, 330), (905, 300)]), ("wall", [(905, 365), (1030, 365)]),
    ]),
    lights=[L(k, 0, 580, 340, s, 6, 3, PURPLE, 0.35, "pulse"), L(k, 1, 580, 200, s, 3, 1, PURPLE, 0.35),
            L(k, 2, 210, 240, s, 5, 2, AMBER, 0.3), L(k, 3, 150, 140, s, 3, 1, GOLD, 0.3),
            L(k, 4, 570, 70, s, 4, 2, WARM, 0.25), L(k, 5, 945, 140, s, 4, 2, WARM, 0.25),
            L(k, 6, 400, 310, s, 2, 1, WARM, 0.25), L(k, 7, 760, 310, s, 2, 1, WARM, 0.25),
            L(k, 8, 340, 375, s, 2, 1, WARM, 0.25), L(k, 9, 810, 375, s, 2, 1, WARM, 0.25),
            L(k, 10, 250, 455, s, 2, 1, WARM, 0.25), L(k, 11, 440, 485, s, 2, 1, WARM, 0.25),
            L(k, 12, 720, 485, s, 2, 1, WARM, 0.25), L(k, 13, 580, 600, s, 5, 2, GOLD, 0.3),
            L(k, 14, 125, 610, s, 4, 2, AMBER, 0.3), L(k, 15, 1055, 610, s, 4, 2, AMBER, 0.3),
            L(k, 16, 965, 360, s, 2, 1, WHITE, 0.15), L(k, 17, 1140, 120, s, 3, 1, AMBER, 0.3)],
    tokens=[T(k, 0, "denis", 600, 160, s, 120), T(k, 1, "menades", 500, 320, s, 120, True),
            T(k, 2, "menades", 660, 320, s, 120, True), T(k, 3, "menades", 580, 420, s, 120, True),
            T(k, 4, "plaut", 575, 70, s, 120, True), T(k, 5, "seg", 520, 115, s, 120, True),
            T(k, 6, "seg", 640, 115, s, 120, True), T(k, 7, "victor", 940, 130, s, 120, True)]))
SC = {sc["_id"]: sc for sc in SCENES}
S = {sc_k: gid("scene", sc_k) for sc_k in [a[0] for a in AMB] + ["map-cobertura", "map-tirso"]}

# ------------------------------------------------------------------ journal
md = open(os.path.join(ROOT, "src", CASE, "caso.md"), encoding="utf-8").read()
md = re.sub(r"^# A Casa Sempre Ganha\n+.*?@\w+\n", "", md, flags=re.S)
md = re.sub(r"^\*\*Estilo visual[.:]\*\*.*\n", "", md, flags=re.M)
md = md.replace(" Os prompts de arte servem para gerar as imagens no Midjourney.", "")
md = md.split("\n### Créditos")[0]
# blockquotes seguidos não podem se fundir
_l = md.split("\n"); _o = []
for _i, _ln in enumerate(_l):
    _o.append(_ln)
    if _ln == "" and _i > 0 and _l[_i - 1].startswith(">") and _i + 1 < len(_l) and _l[_i + 1].startswith(">"):
        _o.append("<!-- -->"); _o.append("")
md = "\n".join(_o)

PORTRAITS = {"victor-gordian", "denis-bacarat", "augusto-plaut", "silvano-arcadio", "fabio-junco"}
ART_SCENE = {"por-tras-das-cortinas": "cortinas", "departamento-medico-do-pactolo": "ganchos",
             "estadio-do-pactolo-ambientacao": "estadio", "departamento-medico-ambientacao": "medico",
             "vestiario-do-pactolo-ambientacao": "vestiario", "ct-do-olimpico-ambientacao": "ct",
             "protesto-da-torcida-ambientacao": "protesto", "casa-de-apostas-clandestina-ambientacao": "apostas",
             "mesa-de-bar-ambientacao": "bar", "festa-do-partido-ambientacao": "festa", "buffet-do-partido-ambientacao": "buffet",
             "cobertura-de-victor-ambientacao": "cobertura", "cobertura-de-victor-battlemap": "map-cobertura",
             "audios-de-fabio-junco-ambientacao": "audios", "forum-ambientacao": "forum", "tirso-de-dia-ambientacao": "tirso-dia",
             "o-convite-ambientacao": "convite", "esconderijo-de-fabio-ambientacao": "esconderijo",
             "chegada-ao-tirso-ambientacao": "chegada", "pista-do-tirso-ambientacao": "pista", "tirso-battlemap": "map-tirso",
             "salao-vip-ambientacao": "vip", "mesa-de-bacara-ambientacao": "bacara", "epilogo-ambientacao": "epilogo"}


def link_scene(key):
    sc = SC[S[key]]
    return f'<p class="adc-cap">@UUID[Scene.{sc["_id"]}]{{Abrir a cena: {sc["name"]}}}</p>'


def fig(m):
    s_ = slug(m.group(1))
    if s_ in PORTRAITS:
        return f'\n<div class="adc-portrait"><img src="{AS}/retratos/{s_}.webp"></div>\n'
    if s_ == "perigos-de-combate":
        return f'\n<figure class="adc-fig"><img src="{AS}/cenas/perigos-de-combate.webp"></figure>\n'
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
html = re.sub(r"(?<=[.”)\"]) <strong>(Mythos|Quer|Tem|Como interpretar):</strong>",
              r"<br><strong>\1:</strong>", html)


def actor_link(key, label="Abrir a ficha"):
    return f'<p class="adc-cap">@UUID[Actor.{A[key]}]{{{label}}}</p>'


for prefix, key in [("Victor Gordian", "victor"), ("Dênis Bacarat", "denis"), ("Augusto Plaut", "plaut"),
                    ("Silvano Arcádio", "silvano"), ("Fábio Junco", "fabio"), ("Torcida da Fúria do Rio", "torcida"),
                    ("Irmãos Brandão", "brandao"), ("Seguranças de Plaut", "seg"), ("As mênades", "menades")]:
    html = re.sub(r"(<h3>" + re.escape(prefix) + r"[^<]*</h3>)", lambda m: m.group(1) + actor_link(key), html, count=1)
html = html.replace("<h3>Os suspeitos mundanos</h3>", "<h3>Os suspeitos mundanos</h3>" + "".join(
    f'<p class="adc-cap">@UUID[Actor.{A[k_]}]{{{n_}}}</p>' for k_, n_ in
    [("hugo", "Hugo Ambrosio"), ("silvano", "Silvano Arcádio"), ("wellington", "Wellington Souza")]), 1)
html = html.replace("<h3>Outros NPCs</h3>", "<h3>Outros NPCs</h3>" + "".join(
    f'<p class="adc-cap">@UUID[Actor.{A[k_]}]{{{n_}}}</p>' for k_, n_ in
    [("epidauro", "Dr. Caio Epidauro"), ("tavares", "Marcos Tavares"), ("helena", "Dra. Helena Moura"),
     ("brandao", "Irmãos Brandão")]), 1)
html = re.sub(r"(<h2>Perigos sociais</h2>.*?</table>)", lambda m: m.group(1) + "".join(
    actor_link(k_, n_) for k_, n_ in [("victor", "Victor Gordian"), ("denis", "Dênis Bacarat"),
                                       ("plaut", "Augusto Plaut"), ("silvano", "Silvano Arcádio")]), html, count=1, flags=re.S)

OPEN = {"Visão geral": "abertura-do-caso", "Sessão 1": "estadio-do-pactolo", "Sessão 2": "festa-do-partido",
        "Sessão 3": "pista-do-tirso", "Provas": "casa-de-apostas-clandestina", "Apêndice": "tirso-de-dia"}
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
    "_id": JID, "name": "A Casa Sempre Ganha — Guia do MC", "folder": F["jou"]["_id"], "sort": 0, "categories": [],
    "pages": [{"_id": gid("page", t), "name": re.sub("<.*?>", "", t), "type": "text", "sort": (i + 1) * 100000,
               "title": {"show": True, "level": 1},
               "text": {"format": 1, "content": f'<div class="mesa-alta a-casa-sempre-ganha">{b}</div>', "markdown": ""},
               "image": {}, "video": {"controls": True, "volume": 0.5}, "src": None, "system": {},
               "ownership": {"default": -1}, "flags": {}, "_stats": STATS, "category": None}
              for i, (t, b) in enumerate(pages)],
    "ownership": {"default": 0}, "flags": {}, "_stats": STATS}

# ------------------------------------------------------------------ aventura
ADV = gid("adventure", CASE)
n_adv = sum(1 for a in ACTORS if a["folder"] == F["adv"]["_id"])
n_npc = len(ACTORS) - n_adv
adventure = {
    "_id": ADV, "_key": f"!adventures!{ADV}", "name": "A Casa Sempre Ganha", "img": f"{AS}/cenas/capa-do-caso.webp",
    "caption": "Um caso de City of Mist em três sessões",
    "description": "<p>Acréscimos. Sessenta mil pessoas de pé. O artilheiro arma o chute que salvaria o clube, e cai. Ninguém tocou nele. O coração estava perfeito. Para quem enxerga através das Brumas, é o começo de um padrão: mortes que chegam sempre na hora exata e um apostador elegante que acerta tudo e nunca sorri.</p>"
                   f"<p>Importa: o Guia do MC completo com o iceberg do caso, {len(AMB)} cenas de ambientação, 2 battlemaps com paredes, portas e luzes, "
                   f"{n_adv} Perigos com espectros, travas e movimentos, {n_npc} NPCs e tokens já posicionados (adversários ocultos).</p>",
    "actors": ACTORS, "combats": [], "items": [], "journal": [journal], "scenes": SCENES, "tables": [], "macros": [],
    "cards": [], "playlists": [], "folders": list(ROOT_F.values()) + list(F.values()), "sort": 30, "flags": {}, "_stats": STATS, "folder": None}

os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    os.remove(os.path.join(OUT, f))
json.dump(adventure, open(os.path.join(OUT, "A_Casa_Sempre_Ganha.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("atores", len(ACTORS), "cenas", len(SCENES), "páginas", len(pages))
