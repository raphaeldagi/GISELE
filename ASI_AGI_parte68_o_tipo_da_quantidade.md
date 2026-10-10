# Como eu construiria uma AGI/ASI — Parte 68 (0x44): o tipo da quantidade

> Continuação da [Parte 67](ASI_AGI_parte67_prever_o_previsto.md). O loop continua (pedido permanente: programar sem parar, prever o que foi previsto e fazer engenharia reversa
> disso). A Parte 67 leu as minhas previsões com uma régua que perdia as faixas da linha seguinte, e concluiu que "as faixas largas acertam menos". Esta parte troca a régua, refaz a
> conta por tipo de quantidade, e acha que a conclusão era um paradoxo de Simpson.

## A régua nova e a conclusão desfeita (dados passados, medidos antes deste registro)

`p1481_minhas_previsoes_v2` lê a faixa de cada letra também na linha seguinte (até 400 caracteres, sem passar por outra letra), só na seção "Sobre o mundo" do documento (a
primeira versão pegava a tabela sobre mim, num caso) e converte porcentagens em frações. Nas Partes 53 a 67: **103** previsões, **75** com faixa (a P1452 lia 51). Cada faixa
ganha um tipo. `p1482_engenharia_por_tipo` (com a Parte 67):

| tipo | previsões | acerto | w mediana | acerto das estreitas | acerto das largas |
|---|---|---|---|---|---|
| cruza o zero | 8 | 0,500 | — (w = 1 sempre) | — | — |
| fração | 21 | 0,714 | 0,368 | **0,800** | **0,600** |
| contagem | 18 | 0,611 | 0,252 | **0,556** | **0,667** |
| outra | 28 | 0,750 | 0,333 | **0,643** | **0,917** |
| sem faixa (categórica) | 28 | 0,786 | — | — | — |

**A conclusão da Parte 67 era um paradoxo de Simpson.** "As largas acertam menos" vinha da mistura de tipos: as faixas em torno de zero têm w = 1 (caem todas no terço mais
largo) e acertam pouco (50%, e 33% até a Parte 66). Dentro de cada tipo, a largura compra acerto nas contagens e nas outras (largas acertam mais), e só nas frações vale o
contrário. O que acerta pouco não é a faixa larga: é a pergunta em torno de zero (uma diferença, uma inclinação, uma média de z), em que eu não sei nem o sinal.

## Previsões sobre as minhas previsões desta parte (registradas antes de escrever qualquer previsão do mundo desta parte)

Planejado, antes de escrever: uma pergunta do dicionário, uma do hexadecimal e a rodada 42 (a correção de segunda ordem da densidade dos primos: a inclinação de z, que é
uma quantidade em torno de zero).
- **(m1)** o número de previsões do mundo (letras na linha "Do mundo") em **[6; 9]**.
- **(m2)** o número de faixas do tipo "cruza o zero" (lidas pela P1481) em **[1; 3]** (a rodada 42 é sobre uma inclinação e uma média de z).
- **(m3)** a mediana de w das faixas que **não** cruzam o zero em **[0,25; 0,37]** (as medianas por tipo, de 0,25 a 0,37).
- **(m4)** a fração de acertos do mundo em **[0,43; 0,86]** (a média dos acertos por tipo, ponderada pelos tipos planejados, ~0,66, ± a faixa binomial de ~7 previsões).
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 (a regra da Parte 67: faixa larga pede uma calibração do nível, não mais largura) em **[0; 1]**.
