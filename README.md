# Asas de Cera — um caso de City of Mist

Módulo de aventura para o Foundry VTT (v13–v14) e o sistema **City of Mist / Mist Engine** (`city-of-mist`).

Um bilionário cai em chamas diante de cem testemunhas que não lembram de nada. Uma detetive teimosa vê no caso a ponta de uma rede que manda na Cidade. E, no alto da torre mais brilhante, um sol que não aceita ser ofuscado.

## O que o módulo traz

- **Guia do MC** num journal com 11 páginas (uma por capítulo): narração para ler em voz alta, falas dos NPCs, Dicas, regras e o iceberg do caso. Links diretos para as cenas e fichas.
- **14 cenas de ambientação**, da capa à contracapa.
- **4 battlemaps** com paredes, portas, vidros e iluminação: Terraço do Hotel Zênite, Clube Meia-Noite, Oficina escondida de Dédalo e A Barca no Duat.
- **9 Perigos** com espectros e movimentos (customizados, fortes e fracos, com condições prontas para aplicar), e **10 NPCs**.
- **Tokens redondos** já posicionados nos battlemaps. Os adversários começam **ocultos**.

## Instalação

No Foundry: *Add-on Modules → Install Module* e cole o manifesto:

```
https://github.com/pedronaraujo/City-of-Mist---Asas-de-Cera/releases/latest/download/module.json
```

Ative o módulo num mundo com o sistema City of Mist, abra o compêndio **Asas de Cera (Aventura)** e clique em **Import Adventure**.

## Desenvolvimento

```
python3 tools/tokens.py   # tokens redondos
python3 tools/build.py    # gera src/packs a partir de src/caso.md
node tools/pack.mjs       # compila o compêndio LevelDB em packs/
```

## Créditos e aviso

Escrito por Pedro Tostes. Material comunitário **não oficial**. City of Mist é marca da Son of Oak Game Studio. Artes geradas com IA (Midjourney). Uso em mesa pessoal.
