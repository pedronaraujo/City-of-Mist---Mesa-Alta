# City of Mist — Mesa Alta

Módulo de aventuras para o Foundry VTT (v13–v14) e o sistema **City of Mist / Mist Engine** (`city-of-mist`).

Várias aventuras ao redor da lore da **Mesa Alta**, o clube secreto de deuses que manda na Cidade. Cada caso roda sozinho e vem num compêndio próprio: importe só o que for jogar. Juntos, formam uma série.

## Aventuras incluídas

### Asas de Cera

Um bilionário cai em chamas diante de cem testemunhas que não lembram de nada. Uma detetive teimosa vê no caso a ponta de uma rede que manda na Cidade. E, no alto da torre mais brilhante, um sol que não aceita ser ofuscado.

- Guia do MC em journal (11 páginas), 14 cenas de ambientação e 4 battlemaps com paredes, portas, vidros e luzes.
- 9 Perigos com espectros e movimentos, 10 NPCs e tokens já posicionados (adversários ocultos).

### Reflexos no Espelho

Nico Valença tinha dois milhões de seguidores e nenhum espelho em casa. Três dias depois de cair na piscina de borda infinita do Hotel Aqua Miragem, ele faz uma live. Um terapeuta que nunca teve celular diz que aquela não é a voz dele. E, num rooftop da Cidade, alguém prepara a obra de arte do ano.

- Guia do MC em journal (13 páginas, com o iceberg do caso), 16 cenas de ambientação e 6 battlemaps com paredes, portas e luzes (o rooftop tem um mapa para a montagem e outro para o lançamento).
- 7 Perigos com espectros, travas e movimentos, 7 NPCs e tokens já posicionados (adversários ocultos).
- Apêndice no Guia do MC para ligar o caso ao Asas de Cera numa campanha.

### O Som da Chuva

Chove há 35 dias. O colunista que ouvia a cidade inteira morreu afogado na própria banheira, e a polícia arquivou como acidente. No alto do morro, um professor gentil abre as portas de um conjunto habitacional para quem precisa de abrigo. Faltam cinco dias para a arca se fechar.

- Guia do MC em journal (13 páginas, com o iceberg do caso), 24 cenas de ambientação com chuva e 4 battlemaps com paredes, portas e luzes.
- 7 Perigos com espectros, travas e movimentos, 7 NPCs e tokens já posicionados (adversários ocultos).
- Adendo para PJs Portais de deuses da chuva e apêndice para ligar o caso à Mesa Alta numa campanha.

## Instalação

No Foundry: *Add-on Modules → Install Module* e cole o manifesto:

```
https://raw.githubusercontent.com/pedronaraujo/City-of-Mist---Mesa-Alta/main/module.json
```

Ative o módulo num mundo com o sistema City of Mist. Na aba de compêndios, abra a pasta **Mesa Alta**, escolha a aventura e clique em **Import Adventure**.

> **Vindo da versão 1 (asas-de-cera)?** O ID do módulo mudou para `mesa-alta`. Desinstale o módulo antigo, instale este e reimporte a Asas de Cera nos mundos onde ela já estava (as imagens importadas pela versão antiga apontam para a pasta do módulo antigo).

## Desenvolvimento

```
python3 tools/tokens_asas_de_cera.py              # tokens redondos (Asas de Cera)
python3 tools/prep_reflexos.py "<pasta Imagens>"  # artes de Reflexos no Espelho -> assets/
python3 tools/tokens_reflexos.py                  # tokens redondos (Reflexos no Espelho)
python3 tools/build_asas_de_cera.py               # src/packs/asas-de-cera a partir de src/asas-de-cera/caso.md
python3 tools/build_reflexos_no_espelho.py        # src/packs/reflexos-no-espelho a partir de src/reflexos-no-espelho/caso.md
python3 tools/prep_som_da_chuva.py "<pasta Imagens>"  # artes de O Som da Chuva -> assets/
python3 tools/tokens_som_da_chuva.py              # tokens redondos (O Som da Chuva)
python3 tools/build_o_som_da_chuva.py             # src/packs/o-som-da-chuva a partir de src/o-som-da-chuva/caso.md
python3 tools/preview.py reflexos-no-espelho      # confere paredes, luzes e tokens dos battlemaps
node tools/pack.mjs                               # compila os compêndios LevelDB em packs/
# depois gere dist/mesa-alta.zip com module.json, README.md, styles, assets e packs
```

Cada aventura tem sua pasta em `assets/<aventura>/` e `src/<aventura>/`.

## Créditos e aviso

Escrito por Pedro Tostes. Material comunitário **não oficial**. City of Mist é marca da Son of Oak Game Studio. Artes geradas com IA (Midjourney). Uso em mesa pessoal.
