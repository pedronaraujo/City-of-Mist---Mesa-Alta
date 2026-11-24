"""Gera o JSON-fonte da aventura Reflexos no Espelho (Adventure) para o sistema city-of-mist.

Uso: python3 tools/build_reflexos_no_espelho.py && node tools/pack.mjs
"""
import hashlib, json, os, re, unicodedata
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASE = "reflexos-no-espelho"
MOD = "modules/mesa-alta"
AS = f"{MOD}/assets/{CASE}"
OUT = os.path.join(ROOT, "src", "packs", CASE)
STATS = {"systemId": "city-of-mist", "systemVersion": "4.5.3", "coreVersion": "13.351",
         "createdTime": 1795500000000, "modifiedTime": 1795500000000, "lastModifiedBy": None,
         "compendiumSource": None, "duplicateSource": None}


def gid(*parts):
    h = hashlib.sha1(("reflexos|" + "|".join(parts)).encode()).hexdigest()
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
CASE_COLOR = "#6a3fb5"
SUB = {"adv": ("Adversários", "#a8195f"), "npc": ("NPCs", "#0e6f78"), "amb": ("Ambientação", "#2b2540"), "map": ("Battlemaps", "#3a5a9c")}
ROOT_F = {"Actor": folder("Reflexos no Espelho", "Actor", CASE_COLOR), "Scene": folder("Reflexos no Espelho", "Scene", CASE_COLOR)}
F = {
    "adv": folder(SUB["adv"][0], "Actor", SUB["adv"][1], ROOT_F["Actor"]["_id"]),
    "npc": folder(SUB["npc"][0], "Actor", SUB["npc"][1], ROOT_F["Actor"]["_id"]),
    "amb": folder(SUB["amb"][0], "Scene", SUB["amb"][1], ROOT_F["Scene"]["_id"]),
    "map": folder(SUB["map"][0], "Scene", SUB["map"][1], ROOT_F["Scene"]["_id"]),
    "jou": folder("Reflexos no Espelho", "JournalEntry", CASE_COLOR),
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
    actor("tezca", "Teo Tezca — Tezcatlipoca", "adv", "teo-tezca", "teo-tezca", "Tezcatlipoca",
          "O artista do ano, dono da Galeria Quinto Sol", "O Espelho Fumegante. Candidato à Mesa Alta.",
          P("Quarentão, terno preto impecável, faixa de tinta preta sobre os olhos nas noites de gala, um pequeno espelho de obsidiana no peito. Anfitrião perfeito, generoso, curioso sobre a galera. Nunca admite nada e nunca levanta a voz.",
            "<strong>Quer:</strong> ser adorado; não precisa de corpo, só de holofotes.",
            "<strong>Travas:</strong> Abalar fica X até a galera confrontá-lo com pelo menos uma prova concreta da manipulação. Expor a figura fica X até a cena 3.5 e só sobe com o que a galera mostra de fato (provas, testemunhas, a própria Elisa); uma rolagem alta sem prova não marca nenhum nível.",
            "<em>“Arte não é crime. É só a parte do crime que a gente aplaude.”</em>"),
          [("Ferir ou Incapacitar", 3), ("Convencer (X: impossível)", 0), ("Abalar (X até haver prova)", 5),
           ("Expor a figura (X até a cena 3.5)", 6)],
          [("custom", "Mártir", "Sempre que um personagem fere ou ataca $name em público, ele ganha a condição [aclamado] no mesmo nível. Se [aclamado] chegar a 3 ou mais antes de Expor a figura se completar, ele vira mártir da censura à arte e sai mais forte."),
           ("hard", "Gentileza envenenada", "Dá a um personagem um rótulo tentador (um acesso, um contato). Usá-lo cria um débito com $name."),
           ("hard", "Virar a plateia", "[desacreditado-2] para um personagem diante do público ou da imprensa."),
           ("hard", "Os censores", "Incorpora a galera à obra: todos recebem [vilão-da-narrativa-2]."),
           ("hard", "Silenciar uma ponta solta", "Afasta uma testemunha ou some com uma prova."),
           ("soft", "Elogio", "$name elogia algo íntimo de um personagem que ninguém deveria saber.", True),
           ("soft", "Convite", "$name convida, presenteia ou oferece um vinho.", True),
           ("soft", "Onde não devia", "$name aparece num lugar onde não era esperado.", True)]),
    actor("elisa", "Elisa Côrtes — Eco", "adv", "elisa-cortes", "elisa-cortes", "Eco", "Ghostwriter de Nico Valença",
          "A voz por trás de Nico. Escala da mentira para a voz como arma.",
          P("Trinta e poucos anos, roupa escura e discreta, crachá da equipe que ninguém lê. Escreveu cada legenda famosa de Nico. Termina as frases repetindo as últimas palavras de quem fala com ela.",
            "<strong>Quer:</strong> manter vivo o Nico que ela inventou, e finalmente ser ouvida. <strong>Tem:</strong> o espelho de obsidiana e o celular de Nico.",
            "<strong>Escalada:</strong> na Sessão 1 é passiva (mente, aponta para o Amir, vaza as DMs, “perde” o celular). Quando a galera desconfia dela, na Sessão 2, passa ao ataque com a voz.",
            "<strong>Travas:</strong> Encurralar fica X até a cena 2.5. Desmascarar fica X até a galera ter o vídeo original (2.2) ou revistar o santuário (2.1); os níveis 4 e 5 só no confronto direto (2.5) ou em público (3.5). Convencer fica X até ela ver os próprios rascunhos expostos (3.5).",
            "<em>“Esse não era ele. O Nico que vocês conheceram fui eu que escrevi.”</em>"),
          [("Ferir ou Incapacitar", 2), ("Encurralar (X até a cena 2.5)", 4), ("Desmascarar (travado)", 5),
           ("Convencer (X até a cena 3.5)", 5)],
          [("hard", "Com a voz de outro", "Áudio ou ligação falsa: [enganado-2] ou [incriminado-3] em um personagem."),
           ("hard", "Esquecida", "$name escapa da cena. Todos recebem [não-lembra-dela-1]."),
           ("hard", "Vazar", "A imprensa recebe material novo: Amir ou um personagem recebe [suspeito-2]."),
           ("soft", "Lágrimas", "$name chora no momento certo.", True),
           ("soft", "Eco", "$name repete as últimas palavras de quem fala com ela.", True),
           ("soft", "O Amir", "$name muda de assunto para o Amir.", True)]),
    actor("amir", "Amir Neves — Ameínias", "adv", "amir-neves", "amir-neves", "Ameínias (desperta na cena 2.4)",
          "Ex-influencer cancelado", "O suspeito plantado. Segue o relógio de atitude.",
          P("Namorou Nico em segredo e foi destruído por um vídeo dele. Estava no hotel porque Nico o chamou para pedir desculpas; nunca subiu. Desperta no fim da Sessão 2 e carrega uma “espada”: a vontade de cobrar.",
            "<strong>Relógio de atitude (oculto):</strong> marque desde a cena 1.4. Aliado, instável ou ameaça na festa. Comece os espectros com níveis já marcados conforme o relógio.",
            "<em>“Eu fui cancelado por ele uma vez. Agora sou assassino dele. Pelo menos dessa vez eu sei o motivo.”</em>"),
          [("Ferir ou Incapacitar", 3), ("Acalmar", 3), ("Conquistar confiança", 3)],
          [("hard", "A espada", "$name cobra de alguém: [humilhado-3] ou [ferido-2] no alvo, geralmente a Elisa."),
           ("hard", "Explodir em público", "Todos os presentes recebem [escândalo-2]."),
           ("hard", "Desabafo ao vivo", "Abre uma live sem aviso, que pode ajudar ou atrapalhar a galera."),
           ("soft", "Dúvida", "$name pede provas e desconfia da galera.", True),
           ("soft", "Sem ser chamado", "$name aparece sem ser chamado.", True)], disposition=0),
    actor("seg-agencia", "Segurança da agência", "adv", "seguranca-agencia", None, "", "Segurança noturno",
          "Cena 2.2: o cofre.",
          P("Experiente e desconfiado. Não sabe nada da Névoa, só sabe que ninguém sobe sem autorização. Perfil próximo de <strong>Tiras / Seguranças</strong> do Guia da MC (cap. 3).",
            "<em>“O escritório está fechado. Ninguém sobe sem autorização da dona Elisa. Dona Elisa? É… a assistente.”</em>"),
          [("Ferir ou Incapacitar", 3), ("Enganar", 3), ("Despistar", 2)],
          [("hard", "Conter", "[imobilizado-2]."),
           ("hard", "Chamar a polícia", "[procurado-2], e a armadilha da cena 2.3 fica mais perigosa."),
           ("hard", "Golpe", "[ferido-2]."),
           ("soft", "Ronda", "A lanterna passa pelo corredor.", True),
           ("soft", "Rádio", "Ele fala baixo no rádio.", True)]),
    actor("multidao", "Multidão de fãs", "adv", "multidao", None, "", "Fãs revoltados", "Cena 1.4: o cerco.",
          P("Dezenas de fãs com celulares no alto, transmitindo tudo. Ninguém ali é mau sozinho; juntos são perigosos. Ferir dormentes em público é sempre escândalo.",
            "<em>“Ele destruiu o Nico uma vez, agora terminou o serviço! Todo mundo está vendo!”</em>"),
          [("Dispersar", 4), ("Acalmar", 3), ("Ferir (X: gera [escândalo-3])", 0)],
          [("hard", "Empurra-empurra", "[ferido-2] ou [pisoteado-2]."),
           ("hard", "Viraliza", "[exposto-2]: o vídeo da galera circula."),
           ("hard", "Isolar", "[separado-2] de um aliado ou do Amir."),
           ("hard", "Invadir", "A multidão entra no prédio e o Amir corre perigo."),
           ("soft", "Hashtags", "Gritam hashtags e cantam o nome de Nico.", True),
           ("soft", "Cercar", "Cercam um carro e batem no vidro.", True)], collective=3),
    actor("seg-montagem", "Segurança da exposição (montagem)", "adv", "seguranca-exposicao", None, "",
          "Equipe de segurança da galeria", "Cena 3.4: segurança pesada.",
          P("Equipe profissional paga para proteger o segredo da obra. Na noite anterior, numerosa e vigilante.",
            "<strong>Ser pego</strong> aciona uma consequência à escolha da MC: expulsão discreta, escândalo ou “os censores”."),
          [("Ferir ou Incapacitar", 4), ("Enganar", 4), ("Despistar", 4)],
          [("hard", "Flagrante", "A segurança entra em alerta: os espectros de furtividade sobem 1 até o fim da cena."),
           ("hard", "Conter", "[detido-2], mais uma consequência narrativa."),
           ("hard", "Força", "[ferido-2]."),
           ("soft", "Ponto", "Alguém fala baixo no ponto.", True),
           ("soft", "Acesso fechado", "Uma porta de serviço é trancada.", True)], collective=2),
    actor("seg-lancamento", "Segurança da exposição (lançamento)", "adv", "seguranca-exposicao", None, "",
          "Equipe de segurança da galeria", "Cena 3.5: volume normal, misturada aos convidados.",
          P("Na festa, discreta e misturada aos convidados. Qualquer confronto visível vira espetáculo.",
            "<strong>Ser pego</strong> aciona uma consequência à escolha da MC: expulsão discreta, escândalo ou “os censores”."),
          [("Ferir ou Incapacitar", 3), ("Enganar", 3), ("Despistar", 3)],
          [("hard", "Flagrante", "A segurança entra em alerta: os espectros de furtividade sobem 1 até o fim da cena."),
           ("hard", "Conter", "[detido-2], mais uma consequência narrativa."),
           ("hard", "Força", "[ferido-2]. Cada confronto visível dá [aclamado-1] a Tezca."),
           ("soft", "Revista", "Revistam bolsas na entrada.", True)], collective=2),
]
NPCS = [
    ("tiresias", "Dr. Tiago Resende — Tirésias", "dr-tiago-resende", "dr-tiago-resende", "Tirésias", "Terapeuta das celebridades",
     "O contratante. Não tem celular nem redes; telas não dizem nada a ele. Ouve a verdade nas vozes e deixa escapar profecias. Totalmente confiável. Não sabe que foi indicado a Nico por Tezca.",
     "<em>“Leia de novo, por favor. Devagar. As palavras são dele. A voz, não.”</em>"),
    ("nico", "Nico Valença — Narciso", "nico-valenca", "nico-valenca", "Narciso", "Influencer (morto)",
     "A vítima. Aparece em vídeos, lives antigas e na memória dos outros. Quem olha para ele se encanta. Queria largar as redes.",
     "<em>“Doutor, ontem eu vi uma foto minha e não me reconheci. Isso é bom ou ruim?”</em>"),
    ("clara", "Clara Moura", "clara-moura", "clara-moura", "", "Curadora da Galeria Quinto Sol",
     "Dormente. Montou a Espelho e sabe que o conceito mudou de última hora. Pode testemunhar (prova 5).",
     "<em>“O conceito era outro. Mudou na semana em que ele morreu.”</em>"),
    ("rafael", "Rafael, gerente do Aqua Miragem", "rafael", None, "", "Gerente do hotel",
     "Quer abafar tudo antes que o hotel vire ponto turístico mórbido.", "<em>“A reserva era corporativa. Política do hotel.”</em>"),
    ("celia", "Dona Célia", "celia", None, "", "Camareira do 31º andar",
     "Viu Amir no lobby a noite toda, nunca no andar.", "<em>“O rapaz de capuz ficou lá embaixo o tempo todo.”</em>"),
    ("julia", "Júlia", "julia", None, "", "Recepcionista de Tirésias",
     "Lê para ele o mundo digital em voz alta e protege o patrão.", "<em>“Para vocês ele deixou recado. Ele sabia que viriam.”</em>"),
    ("duda", "Duda Prata", "duda", None, "", "Jornalista de fofoca",
     "Dona de um portal de celebridades; quer a exclusiva e transmite tudo ao vivo.", "<em>“Estamos ao vivo, gente! Dá um oi para o chat!”</em>"),
]
for key, name, tok, por, myth, logos, bio, fala in NPCS:
    ACTORS.append(actor(key, name, "npc", tok, por, myth, logos, "", P(bio, fala), disposition=0))
AID = {a["_id"]: a for a in ACTORS}
A = {k: gid("actor", k) for k in ["tezca", "elisa", "amir", "seg-agencia", "multidao", "seg-montagem", "seg-lancamento",
                                   "tiresias", "nico", "clara", "rafael", "celia", "julia", "duda"]}


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
AMB = [("capa", "Reflexos no Espelho — Capa", "capa-do-caso", 1792, 2688, ""),
       ("abertura", "Reflexos no Espelho — Abertura", "abertura-do-caso", 1792, 2688, "rain"),
       ("consultorio", "Consultório de Tirésias", "o-consultorio-de-tiresias", 2944, 1648, ""),
       ("varanda", "Suíte 3101 — A varanda", "a-varanda-da-suite-3101", 2560, 1440, ""),
       ("piscina", "Hotel Aqua Miragem — A piscina de borda infinita", "a-piscina-de-borda-infinita", 2944, 1648, ""),
       ("vigilia", "A vigília", "a-vigilia", 4096, 2304, ""),
       ("cerco", "O cerco — Prédio do Amir", "o-cerco", 2944, 1648, ""),
       ("live", "A live", "a-live", 2560, 1440, ""),
       ("santuario", "O santuário de Elisa", "o-santuario-de-elisa", 2944, 1648, ""),
       ("agencia", "A agência", "a-agencia", 2944, 1648, ""),
       ("estudio", "O estúdio", "o-estudio", 2944, 1648, ""),
       ("galeria", "Galeria Quinto Sol", "galeria-quinto-sol", 2944, 1648, ""),
       ("montagem", "A montagem — Rooftop do Aqua Miragem", "a-montagem", 2944, 1648, ""),
       ("lancamento", "O lançamento da Espelho", "o-lancamento", 2944, 1648, ""),
       ("epilogo", "Epílogo", "epilogo", 2560, 1440, ""),
       ("contracapa", "Reflexos no Espelho — Contracapa", "contracapa", 1792, 2688, "")]
for i, (k, n, img, w, h, wx) in enumerate(AMB):
    SCENES.append(scene(k, n, "amb", f"{AS}/cenas/{img}.webp", w, h, weather=wx, sort=i * 10))

# --- Suíte 3101 e varanda (2688x1792; exibição 1200 -> fator 2.24)
s = 2688 / 1200
k = "map-suite"
SCENES.append(scene(k, "Battlemap — Suíte 3101 e varanda", "map", f"{AS}/mapas/suite-3101-e-varanda.webp", 2688, 1792,
    grid=100, battle=True, darkness=0.5, sort=10,
    walls=walls(k, s, [
        ("wall", [(45, 470), (45, 68), (440, 68)]), ("door", [(440, 68), (550, 68)]),
        ("wall", [(550, 68), (935, 68), (935, 130), (1155, 130), (1155, 470)]),
        ("wall", [(870, 68), (870, 295)]), ("door", [(870, 295), (870, 380)]), ("wall", [(870, 380), (870, 470)]),
        ("wall", [(45, 468), (110, 468)]), ("glass", [(110, 468), (530, 468)]), ("door", [(530, 468), (650, 468)]),
        ("glass", [(650, 468), (850, 468)]), ("wall", [(850, 468), (915, 468)]), ("glass", [(915, 468), (1085, 468)]),
        ("wall", [(1085, 468), (1155, 468)]),
        ("wall", [(45, 470), (45, 595)]), ("wall", [(1155, 470), (1155, 595)]),
        ("rail", [(45, 590), (1155, 590)]),
    ]),
    lights=[L(k, 0, 122, 178, s, 3, 1, "#ffcc66", 0.2, "torch"), L(k, 1, 125, 392, s, 3, 1, "#ffcc66", 0.2, "torch"),
            L(k, 2, 455, 205, s, 3, 1, "#ffcc66", 0.2, "torch"), L(k, 3, 700, 395, s, 3, 1, "#ffcc66", 0.2, "torch"),
            L(k, 4, 665, 110, s, 3, 1, "#ffcc66", 0.2), L(k, 5, 985, 158, s, 3, 1, "#ffe3a8", 0.2),
            L(k, 6, 1123, 158, s, 3, 1, "#ffe3a8", 0.2), L(k, 7, 70, 555, s, 3, 1, "#ffb347", 0.25),
            L(k, 8, 1128, 555, s, 3, 1, "#ffb347", 0.25), L(k, 9, 575, 660, s, 9, 2, "#3fd0dc", 0.3, "wave")],
    tokens=[T(k, 0, "rafael", 495, 140, s, 100)]))

# --- A rua do Amir (2688x1792)
k = "map-rua"
SCENES.append(scene(k, "Battlemap — A rua do Amir", "map", f"{AS}/mapas/a-rua-do-amir.webp", 2688, 1792,
    grid=90, battle=True, darkness=0.55, sort=20,
    walls=walls(k, s, [
        ("wall", [(100, 300), (430, 300), (430, 85), (745, 85), (745, 300), (965, 300)]),
        ("wall", [(430, 300), (465, 300), (465, 390)]), ("wall", [(745, 300), (705, 300), (705, 390)]),
        ("wall", [(465, 390), (510, 390)]), ("door", [(510, 390), (660, 390)]), ("wall", [(660, 390), (705, 390)]),
        ("rail", [(100, 392), (465, 392)]), ("rail", [(705, 392), (965, 392)]),
        ("wall", [(975, 400), (975, 175), (1040, 175)]), ("door", [(1040, 175), (1095, 175)]),
        ("wall", [(1095, 175), (1120, 175), (1120, 400)]),
    ]),
    lights=[L(k, 0, 163, 415, s, 6, 2, "#ffb347", 0.25), L(k, 1, 930, 415, s, 6, 2, "#ffb347", 0.25),
            L(k, 2, 600, 170, s, 4, 1, "#ffcc66", 0.2), L(k, 3, 487, 350, s, 2, 1, "#ffb347", 0.25, "torch"),
            L(k, 4, 686, 350, s, 2, 1, "#ffb347", 0.25, "torch"), L(k, 5, 1065, 110, s, 3, 1, "#ffcc66", 0.25)],
    tokens=[T(k, 0, "multidao", 300, 470, s, 90), T(k, 1, "multidao", 420, 450, s, 90), T(k, 2, "multidao", 560, 470, s, 90),
            T(k, 3, "multidao", 760, 460, s, 90), T(k, 4, "multidao", 860, 480, s, 90), T(k, 5, "duda", 690, 520, s, 90)]))

# --- O escritório da agência (4096x2731; fator 3.4133)
s = 4096 / 1200
k = "map-agencia"
SCENES.append(scene(k, "Battlemap — O escritório da agência", "map", f"{AS}/mapas/o-escritorio-da-agencia.webp", 4096, 2731,
    grid=110, battle=True, darkness=0.65, sort=30,
    walls=walls(k, s, [
        ("wall", [(40, 95), (1160, 95), (1160, 710), (40, 710), (40, 95)]),
        ("wall", [(200, 95), (200, 250)]), ("door", [(200, 250), (200, 290)]), ("wall", [(200, 290), (200, 315)]),
        ("wall", [(200, 192), (245, 192)]), ("door", [(245, 192), (280, 192)]), ("wall", [(280, 192), (803, 192)]),
        ("door", [(803, 192), (838, 192)]), ("wall", [(838, 192), (905, 192)]),
        ("wall", [(200, 318), (350, 318)]), ("door", [(350, 318), (395, 318)]), ("wall", [(395, 318), (555, 318)]),
        ("door", [(555, 318), (600, 318)]), ("wall", [(600, 318), (850, 318)]), ("door", [(850, 318), (895, 318)]),
        ("wall", [(895, 318), (905, 318)]),
        ("wall", [(905, 95), (905, 250)]), ("door", [(905, 250), (905, 292)]), ("wall", [(905, 292), (905, 318)]),
        ("glass", [(905, 302), (1160, 302)]),
        ("wall", [(40, 300), (140, 300), (140, 328)]), ("door", [(140, 328), (140, 362)]), ("wall", [(140, 362), (140, 393)]),
        ("door", [(140, 393), (140, 427)]), ("wall", [(140, 427), (140, 440), (40, 440)]), ("wall", [(40, 375), (140, 375)]),
        ("wall", [(165, 305), (305, 305), (305, 435), (215, 435)]), ("door", [(215, 435), (175, 435)]),
        ("wall", [(175, 435), (165, 435), (165, 305)]),
        ("wall", [(345, 318), (345, 470)]),
        ("wall", [(945, 385), (1160, 385)]), ("wall", [(945, 385), (945, 560)]), ("door", [(945, 560), (945, 610)]),
        ("wall", [(945, 610), (945, 655), (1160, 655)]),
    ]),
    lights=[L(k, 0, 1060, 195, s, 3, 1, "#ffcc66", 0.2), L(k, 1, 1115, 235, s, 3, 1, "#ffcc66", 0.2),
            L(k, 2, 715, 370, s, 5, 1, "#ff3fa4", 0.3), L(k, 3, 660, 400, s, 3, 1, "#ffffff", 0.15),
            L(k, 4, 830, 410, s, 3, 1, "#ffffff", 0.15), L(k, 5, 218, 565, s, 3, 1, "#ffcc66", 0.2),
            L(k, 6, 68, 640, s, 3, 1, "#ffcc66", 0.2), L(k, 7, 1050, 450, s, 4, 1, "#ff3fa4", 0.3),
            L(k, 8, 240, 330, s, 3, 1, "#3fd0dc", 0.3), L(k, 9, 410, 250, s, 2, 1, "#ffe3a8", 0.2),
            L(k, 10, 590, 250, s, 2, 1, "#ffe3a8", 0.2), L(k, 11, 720, 250, s, 2, 1, "#ffe3a8", 0.2)],
    tokens=[T(k, 0, "seg-agencia", 240, 385, s, 110, True)]))

# --- O estúdio (2688x1792; fator 2.24)
s = 2688 / 1200
k = "map-estudio"
SCENES.append(scene(k, "Battlemap — O estúdio", "map", f"{AS}/mapas/o-estudio.webp", 2688, 1792,
    grid=100, battle=True, darkness=0.55, sort=40,
    walls=walls(k, s, [
        ("wall", [(1005, 95), (45, 95), (45, 660), (570, 660)]), ("door", [(570, 660), (630, 660)]),
        ("wall", [(630, 660), (1155, 660), (1155, 95), (1080, 95)]), ("door", [(1005, 95), (1080, 95)]),
        ("wall", [(880, 95), (880, 550)]), ("door", [(880, 550), (880, 605)]), ("wall", [(880, 605), (880, 660)]),
        ("wall", [(880, 205), (1000, 205)]), ("wall", [(1080, 205), (1155, 205)]),
    ]),
    lights=[L(k, i, x, y, s, 3, 1, "#ff4a4a", 0.25) for i, (x, y) in enumerate([(280, 125), (375, 125), (500, 125), (615, 125)])]
        + [L(k, 10, 350, 235, s, 2, 1, "#ffcc66", 0.2, "torch"), L(k, 11, 568, 235, s, 2, 1, "#ffcc66", 0.2, "torch"),
           L(k, 12, 688, 285, s, 5, 2, "#ffffff", 0.15), L(k, 13, 170, 315, s, 2, 1, "#ffb347", 0.25, "torch"),
           L(k, 14, 930, 315, s, 3, 1, "#ffcc66", 0.2), L(k, 15, 175, 545, s, 2, 1, "#ffcc66", 0.2),
           L(k, 16, 1105, 128, s, 3, 1, "#ff2a2a", 0.3, "pulse"), L(k, 17, 523, 690, s, 2, 1, "#ffb347", 0.25),
           L(k, 18, 680, 690, s, 2, 1, "#ffb347", 0.25)],
    tokens=[T(k, 0, "elisa", 590, 410, s, 100)]))

# --- Rooftop do Aqua Miragem (3226x2151; fator 2.6883) — duas versões: montagem e lançamento
s = 3226 / 1200
ROOF_WALLS = [
    ("rail", [(95, 165), (95, 135), (1115, 135), (1115, 590), (1050, 658), (95, 658), (95, 550)]),
    ("wall", [(55, 165), (210, 165), (210, 250)]), ("door", [(210, 250), (210, 290)]), ("wall", [(210, 290), (210, 405)]),
    ("door", [(210, 405), (210, 462)]), ("wall", [(210, 462), (210, 550), (55, 550), (55, 165)]),
]
ROOF_LIGHTS = [(620, 385, 4, 2, "#ffffff", 0.2, None), (500, 230, 5, 1, "#b57bff", 0.3, None), (740, 230, 5, 1, "#b57bff", 0.3, None),
               (620, 180, 6, 1, "#ff3fa4", 0.3, None), (620, 500, 8, 2, "#3fd0dc", 0.3, "wave"), (600, 600, 8, 2, "#3fd0dc", 0.3, "wave"),
               (1060, 300, 4, 1, "#ffb347", 0.25, None), (275, 245, 2, 0, "#ffcc66", 0.25, "torch"), (445, 300, 2, 0, "#ffcc66", 0.25, "torch"),
               (800, 305, 2, 0, "#ffcc66", 0.25, "torch"), (920, 280, 2, 0, "#ffcc66", 0.25, "torch"), (458, 378, 2, 0, "#ffcc66", 0.25, "torch"),
               (785, 380, 2, 0, "#ffcc66", 0.25, "torch"), (437, 440, 2, 0, "#ffcc66", 0.25, "torch"), (822, 440, 2, 0, "#ffcc66", 0.25, "torch"),
               (313, 505, 2, 1, "#ffb347", 0.25, None), (968, 500, 2, 1, "#ffb347", 0.25, None)]
for k, n, sort, darkness, toks in [
        ("map-montagem", "Battlemap — Rooftop do Aqua Miragem (montagem)", 50, 0.7,
         [("seg-montagem", 240, 455, True), ("seg-montagem", 330, 330, True), ("seg-montagem", 700, 260, True),
          ("seg-montagem", 950, 420, True), ("seg-montagem", 1000, 600, True), ("seg-montagem", 140, 600, True)]),
        ("map-lancamento", "Battlemap — Rooftop do Aqua Miragem (lançamento)", 60, 0.45,
         [("tezca", 620, 375, False), ("elisa", 560, 440, False), ("seg-lancamento", 240, 455, True),
          ("seg-lancamento", 950, 420, True), ("seg-lancamento", 700, 255, True)])]:
    SCENES.append(scene(k, n, "map", f"{AS}/mapas/rooftop-do-aqua-miragem.webp", 3226, 2151, grid=100, battle=True,
                        darkness=darkness, sort=sort, walls=walls(k, s, ROOF_WALLS),
                        lights=[L(k, i, x, y, s, d, b, c, a, an) for i, (x, y, d, b, c, a, an) in enumerate(ROOF_LIGHTS)],
                        tokens=[T(k, i, a_, x, y, s, 100, h) for i, (a_, x, y, h) in enumerate(toks)]))
SC = {sc["_id"]: sc for sc in SCENES}
S = {k: gid("scene", k) for k in ["capa", "abertura", "consultorio", "varanda", "piscina", "vigilia", "cerco", "live", "santuario",
                                   "agencia", "estudio", "galeria", "montagem", "lancamento", "epilogo", "contracapa", "map-suite",
                                   "map-rua", "map-agencia", "map-estudio", "map-montagem", "map-lancamento"]}

# ------------------------------------------------------------------ journal
md = open(os.path.join(ROOT, "src", CASE, "caso.md"), encoding="utf-8").read()
md = re.sub(r"^# Reflexos no Espelho\n+.*?@\w+\n", "", md, flags=re.S)
md = re.sub(r"^\*\*Estilo visual:\*\*.*\n", "", md, flags=re.M)
md = re.sub(r" Os \*\*Post-its de Dicas\*\*.*?Todo o resto é só para você\.",
            " Os **Post-its de Dicas** listam o que cada cena pode revelar. Todo o resto é só para você.", md)
md = re.sub(r"^\*Um caso de City of Mist.*?\*\n", "", md, flags=re.M)

PORTRAITS = {"dr-tiago-resende", "nico-valenca", "elisa-cortes", "teo-tezca", "amir-neves", "clara-moura", "o-espelho-de-obsidiana"}
ART_SCENE = {"a-piscina-de-borda-infinita-ambientacao": "piscina", "a-vigilia-ambientacao": "vigilia", "o-cerco-ambientacao": "cerco",
             "a-live-cena-digital": "live", "o-santuario-de-elisa-ambientacao": "santuario", "a-agencia-ambientacao": "agencia",
             "o-estudio-ambientacao": "estudio", "galeria-quinto-sol-ambientacao": "galeria", "a-montagem-ambientacao": "montagem",
             "o-lancamento-ambientacao": "lancamento", "epilogo": "epilogo", "a-varanda-da-suite-3101": "varanda",
             "o-consultorio-de-tiresias-ambientacao": "consultorio",
             "suite-3101-e-varanda-battlemap": "map-suite", "a-rua-do-amir-battlemap": "map-rua",
             "o-escritorio-da-agencia-battlemap": "map-agencia", "o-estudio-battlemap": "map-estudio",
             "rooftop-do-aqua-miragem-battlemap": "map-lancamento"}


def link_scene(key):
    sc = SC[S[key]]
    return f'<p class="adc-cap">@UUID[Scene.{sc["_id"]}]{{Abrir a cena: {sc["name"]}}}</p>'


def fig(m):
    s_ = slug(m.group(1))
    if s_ in ("capa-do-documento", "abertura-do-caso-pagina-do-capitulo", "contracapa-do-documento-ultima-pagina"):
        return "\n"
    if s_ in PORTRAITS:
        return f'\n<div class="adc-portrait"><img src="{AS}/retratos/{s_}.webp"></div>\n'
    key = ART_SCENE.get(s_)
    if key is None:
        return "\n"
    sc = SC[S[key]]
    src = sc["background"]["src"]
    cls = "adc-fig adc-map" if key.startswith("map-") else "adc-fig"
    extra = link_scene("map-montagem") if key == "map-lancamento" else ""
    return f'\n<figure class="{cls}"><img src="{src}"></figure>{link_scene(key)}{extra}\n'


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
# retrato logo abaixo do título do personagem
html = re.sub(r'(<h3>[^<]*</h3>)((?:(?!<h3>).)*?)(<div class="adc-portrait"><img src="[^"]+"></div>)',
              lambda m: m.group(1) + m.group(3) + m.group(2), html, flags=re.S)
# tópicos do perfil em linhas próprias
html = re.sub(r"(?<=[.”)]) <strong>(Mythos|Quer|Tem|Sabia|Como interpretar):</strong>", r"<br><strong>\1:</strong>", html)


def actor_link(key, label="Abrir a ficha"):
    return f'<p class="adc-cap">@UUID[Actor.{A[key]}]{{{label}}}</p>'


for prefix, key in [("Dr. Tiago Resende", "tiresias"), ("Nico Valença", "nico"), ("Elisa Côrtes —", "elisa"),
                    ("Teo Tezca —", "tezca"), ("Amir Neves —", "amir"), ("Clara Moura", "clara")]:
    html = re.sub(r"(<h3>" + re.escape(prefix) + r"[^<]*</h3>)", lambda m: m.group(1) + actor_link(key), html, count=1)
html = html.replace("<h3>Figurantes</h3>", "<h3>Figurantes</h3>" + "".join(
    f'<p class="adc-cap">@UUID[Actor.{A[k_]}]{{{n_}}}</p>' for k_, n_ in
    [("rafael", "Rafael"), ("celia", "Dona Célia"), ("julia", "Júlia"), ("duda", "Duda Prata")]), 1)
for title, key in [("<h3>Teo Tezca</h3>", "tezca"), ("<h3>Elisa Côrtes</h3>", "elisa"), ("<h3>Amir Neves</h3>", "amir"),
                   ("<h3>Segurança da agência (cena 2.2)</h3>", "seg-agencia"), ("<h3>Multidão de fãs (cena 1.4)</h3>", "multidao")]:
    html = html.replace(title, title + actor_link(key), 1)
html = html.replace("<h3>Segurança da exposição (cenas 3.4 e 3.5)</h3>",
                    "<h3>Segurança da exposição (cenas 3.4 e 3.5)</h3>" + actor_link("seg-montagem", "Abrir a ficha (montagem)")
                    + actor_link("seg-lancamento", "Abrir a ficha (lançamento)"), 1)
# cenas sem arte própria: link direto
for h4, key in [("3.4 A montagem", "map-montagem"), ("1.1 O consultório", "consultorio")]:
    html = re.sub(r"(<h4>" + re.escape(h4) + r"[^<]*</h4>)", lambda m: m.group(1) + link_scene(key), html, count=1)

OPEN = {"Visão geral": "abertura-do-caso", "Por trás das cortinas": "a-varanda-da-suite-3101", "Ganchos": "o-consultorio-de-tiresias",
        "Sessão 1": "a-piscina-de-borda-infinita", "Sessão 2": "o-santuario-de-elisa", "Sessão 3": "o-lancamento",
        "Apêndice": "galeria-quinto-sol"}
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
    if title.startswith("Por trás das cortinas"):
        pages.append(("O Iceberg do Caso", f'<figure class="adc-fig"><img src="{AS}/journal/iceberg.webp"></figure>'
                      '<p>Cada fio vermelho é uma saída: as Dicas de um local apontam para o próximo. Quanto mais fundo, mais protegida está a verdade.</p>'))

JID = gid("journal", "guia")
journal = {
    "_id": JID, "name": "Reflexos no Espelho — Guia do MC", "folder": F["jou"]["_id"], "sort": 0, "categories": [],
    "pages": [{"_id": gid("page", t), "name": re.sub("<.*?>", "", t), "type": "text", "sort": (i + 1) * 100000,
               "title": {"show": True, "level": 1},
               "text": {"format": 1, "content": f'<div class="mesa-alta reflexos-no-espelho">{b}</div>', "markdown": ""},
               "image": {}, "video": {"controls": True, "volume": 0.5}, "src": None, "system": {},
               "ownership": {"default": -1}, "flags": {}, "_stats": STATS, "category": None}
              for i, (t, b) in enumerate(pages)],
    "ownership": {"default": 0}, "flags": {}, "_stats": STATS}

# ------------------------------------------------------------------ aventura
ADV = gid("adventure", CASE)
adventure = {
    "_id": ADV, "_key": f"!adventures!{ADV}", "name": "Reflexos no Espelho", "img": f"{AS}/cenas/capa-do-caso.webp",
    "caption": "Um caso de City of Mist em três sessões",
    "description": "<p>Nico Valença tinha dois milhões de seguidores e nenhum espelho em casa. Três dias depois de cair na piscina de borda infinita do Hotel Aqua Miragem, ele faz uma live. Um terapeuta que nunca teve celular diz que aquela não é a voz dele. E, num rooftop da Cidade, alguém prepara a obra de arte do ano.</p>"
                   "<p>Importa: o Guia do MC completo com o iceberg do caso, 16 cenas de ambientação, 6 battlemaps com paredes, portas e luzes, "
                   "7 Perigos com espectros e movimentos (com travas), 7 NPCs e tokens já posicionados (adversários ocultos).</p>",
    "actors": ACTORS, "combats": [], "items": [], "journal": [journal], "scenes": SCENES, "tables": [], "macros": [],
    "cards": [], "playlists": [], "folders": list(ROOT_F.values()) + list(F.values()), "sort": 10, "flags": {}, "_stats": STATS, "folder": None}

os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    os.remove(os.path.join(OUT, f))
json.dump(adventure, open(os.path.join(OUT, "Reflexos_no_Espelho.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("atores", len(ACTORS), "cenas", len(SCENES), "páginas", len(pages))
