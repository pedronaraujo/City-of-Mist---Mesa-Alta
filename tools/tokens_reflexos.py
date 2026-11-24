"""Tokens redondos de Reflexos no Espelho (usa as funções de tokens_asas_de_cera)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokens_asas_de_cera as tk

tk.RING['obsidiana'] = ((205, 205, 220), (25, 22, 32))
R = 'assets/reflexos-no-espelho/retratos/'; T = 'assets/reflexos-no-espelho/tokens/'
os.makedirs(T, exist_ok=True)
for n, fac, top in [('teo-tezca', 'obsidiana', .05), ('elisa-cortes', 'noite', .07), ('amir-neves', 'neutro', .06),
                    ('dr-tiago-resende', 'neutro', .07), ('nico-valenca', 'neutro', .12), ('clara-moura', 'neutro', .06)]:
    tk.portrait(R + n + '.webp', fac, top=top, size=(0.92 if n == 'nico-valenca' else 0.78), out=T + n + '.webp')
tk.emblem('SEGURANÇA', '◉', 'policia', T + 'seguranca-agencia.webp')
tk.emblem('FÃS', '♥', 'sol', T + 'multidao.webp')
tk.emblem('EXPOSIÇÃO', '◐', 'obsidiana', T + 'seguranca-exposicao.webp')
for k, lab in [('rafael', 'RAFAEL'), ('celia', 'DONA CÉLIA'), ('julia', 'JÚLIA'), ('duda', 'DUDA PRATA')]:
    tk.emblem(lab, lab[0] if k != 'celia' else 'C', 'neutro', T + k + '.webp', glyph_font=tk.ANTON)
