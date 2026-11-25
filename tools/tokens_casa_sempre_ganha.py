"""Tokens redondos de A Casa Sempre Ganha (usa as funções de tokens_asas_de_cera)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokens_asas_de_cera as tk

tk.RING['ouro'] = ((212, 170, 70), (70, 48, 10))
tk.RING['vinho'] = ((150, 30, 60), (45, 8, 20))
tk.RING['cego'] = ((110, 110, 125), (25, 25, 32))
tk.RING['mato'] = ((90, 150, 70), (20, 40, 15))
R = 'assets/a-casa-sempre-ganha/retratos/'; T = 'assets/a-casa-sempre-ganha/tokens/'
os.makedirs(T, exist_ok=True)
for n, fac, top, size in [('victor-gordian', 'ouro', .05, .74), ('denis-bacarat', 'vinho', .05, .74),
                          ('augusto-plaut', 'cego', .06, .74), ('silvano-arcadio', 'mato', .07, .74),
                          ('fabio-junco', 'neutro', .06, .74)]:
    tk.portrait(R + n + '.webp', fac, top=top, size=size, out=T + n + '.webp')
tk.emblem('MÊNADES', '❦', 'vinho', T + 'menades.webp', gsize=230)
tk.emblem('SEGURANÇA', '◉', 'cego', T + 'segurancas-plaut.webp')
tk.emblem('FÚRIA DO RIO', '⚑', 'ouro', T + 'torcida.webp')
tk.emblem('BRANDÃO', '$', 'noite', T + 'brandao.webp', glyph_font=tk.ANTON)
for k, lab, g, fac in [('hugo', 'HUGO', 'H', 'neutro'), ('wellington', 'WELLINGTON', 'W', 'neutro'),
                       ('epidauro', 'DR. EPIDAURO', 'E', 'neutro'), ('tavares', 'TAVARES', 'T', 'policia'),
                       ('helena', 'DRA. HELENA', 'H', 'policia')]:
    tk.emblem(lab, g, fac, T + k + '.webp', glyph_font=tk.ANTON)
