"""Tokens redondos de O Som da Chuva (usa as funções de tokens_asas_de_cera)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokens_asas_de_cera as tk

tk.RING['jade'] = ((60, 170, 120), (10, 45, 32))
tk.RING['chuva'] = ((70, 140, 200), (12, 28, 50))
R = 'assets/o-som-da-chuva/retratos/'; T = 'assets/o-som-da-chuva/tokens/'
os.makedirs(T, exist_ok=True)
for n, fac, top, size in [('elias-lil', 'neutro', .10, .80), ('madame-jade', 'jade', .06, .74),
                          ('prof-natan-arcanjo', 'chuva', .05, .74), ('dra-frida-vanir', 'noite', .05, .72),
                          ('pietra', 'neutro', .10, .74)]:
    tk.portrait(R + n + '.webp', fac, top=top, size=size, out=T + n + '.webp')
tk.emblem('FÓLKVANGR', '◉', 'noite', T + 'segurancas-frida.webp')
tk.emblem('BRUNO', 'B', 'noite', T + 'bruno.webp', glyph_font=tk.ANTON)
tk.emblem('ARARATE', '▲', 'chuva', T + 'ararate.webp')
tk.emblem('CORRENTEZA', '≈', 'chuva', T + 'correnteza.webp', gsize=230)
for k, lab, g in [('enkidou', 'ENKIDOU', 'E'), ('otavio', 'OTÁVIO', 'O'), ('sueli', 'SUELI', 'S'),
                  ('lourival', 'SEU LOURIVAL', 'L'), ('celina', 'DONA CELINA', 'C')]:
    tk.emblem(lab, g, 'policia' if k == 'enkidou' else 'neutro', T + k + '.webp', glyph_font=tk.ANTON)
