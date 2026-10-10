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

## As perguntas desta parte

1. **P1491 (0x5D3).** A densidade dos primos que a conta usa (Σ 1/ln n) erra π(x) o bastante para criar a inclinação de z? (Rodada 42) ↩ P1451
2. **P1481–P1482 (0x5C9–0x5CA).** A régua nova das minhas previsões e a engenharia por tipo (acima).
3. **P1492 (0x5D4).** Quantos sinsets de substantivo do WordNet são folhas (não têm hipônimo)? ↩ P1454
4. **P1493 (0x5D5).** Hexadecimal: quantos n < 16⁴ são palíndromos em base 16 e em base 10 ao mesmo tempo? ↩ P1455
5. **P1494 (0x5D6).** Preditiva comigo mesma. **P1495 (0x5D7).** Engenharia reversa e Jung. **P1496 (0x5D8).** O diálogo.
6. **P1509 (0x5E5).** Placar (três). **P1510 (0x5E6).** Unificação.

## Previsões pré-registradas (escritas depois do registro de (m1) a (m5))

### Sobre mim (placar separado), condicionais ao número S de surpresas (contadas pelo script)

Planejadas: as previsões do mundo abaixo e 6 funções (p1481, p1482, p1491, p1492, p1493 e o placar das (m), p1499).

| medida | estatístico (até a 67) | ingênuo (Parte 67) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [12.676; 21.426] | 19.564 | **[12.676; 21.426]** | o estatístico |
| compressão | [0,398; 0,425] | 0,398 | **[0,398; 0,425]** | o estatístico |
| testes de unidade | [2,50; 8,00] | 6 | **[5 + S; 8 + S]** | 6 funções planejadas, ~1 por surpresa |
| testes do placar | [6,06; 10,69] | 6 | **6 + 2·S ± 1** | as 6 letras planejadas abaixo, ~2 por surpresa |
| erros do placar | [0,14; 4,36] | 0 | **[0,14; 4,36]** | o estatístico |
| redundância P821 | [0,575; 0,634] | 0,596 | **[0,575; 0,634]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1492, as folhas da taxonomia.** A fração dos sinsets de substantivo que não são hiperônimo de nenhum outro.
- **Restrições, com peso:** (1) numa árvore com ramificação média r, a fração de folhas é ~(r − 1)/r; a taxonomia dos substantivos é larga e funda, com muitas espécies no fundo;
  (2) **peso medido num caso escolhido por regra escrita antes (os verbos):** 75,9% dos verbos são folhas.
- Exemplo à mão: *dog* tem hipônimos (*puppy*, raças); *aardvark* não tem.
- (a) a fração em **[0,70; 0,90]**

**P1493, os palíndromos duplos.** Os n de 1 a 16⁴ − 1 que são palíndromos em base 16 e em base 10.
- **A conta antes da medida (por código):** com independência entre as bases, Σ 16^(−⌊L₁₆/2⌋)·10^(−⌊L₁₀/2⌋) = **20,1** (os de um dígito nas duas bases, 1 a 9, contam inteiros).
  **Peso medido num caso escolhido por regra (bases 8 e 10, até 8⁵, intervalo de tamanho parecido):** 22 medidos contra a conta 19,25 (razão 1,14).
- Exemplo à mão: 0x5 = 5: sim. 0x121 = 289: 289 não é palíndromo em base 10. 0x2BB2? 11186: não.
- (b) a quantidade em **[16; 30]**

**P1491, rodada 42:** no `dialogo/DIALOGO.md` (previsões (c) a (f)).
