# Como eu construiria uma AGI/ASI — Parte 69 (0x45): a forma de GPT

> Continuação da [Parte 68](ASI_AGI_parte68_o_tipo_da_quantidade.md). Pedido do usuário, gravado no `CLAUDE.md`: **"Grave na memória que nossa AGI ASI PÓS ASI AGI terá a forma de
> GPT."** Esta parte constrói a forma: um GPT (Generative Pre-trained Transformer) mínimo em Python puro (`synthai/gpt.py`): embeddings de caractere e de posição, atenção causal
> de uma cabeça, resíduo, MLP, softmax do próximo caractere, gradiente escrito à mão (conferido por diferenças finitas: maior erro relativo 2,3·10⁻⁶) e Adam. Pré-treinado nas
> definições do WordNet, medido contra o modelo mais simples (o n-grama), e com a decisão do próximo caractere traduzida bit a bit para Java (rodada 43).

## Previsões sobre as minhas previsões desta parte (prever o previsto; registradas antes de escrever qualquer previsão do mundo desta parte)

Planejado, antes de escrever: bits por caractere do n-grama (ordens 3 e 5) e do GPT nas definições inglesas; a diferença GPT − n-grama; bits por dígito de π em hexadecimal; a
rodada 43 (IGUAIS, e quantos próximos caracteres o GPT pequeno acerta numa frase). Acerto do mundo nas Partes 53 a 68, pela régua nova (`p1481`): **72,5%** (109 previsões);
com ~7 previsões, a faixa binomial de 90% vai de 4/7 a 7/7.
- **(m1)** o número de previsões do mundo em **[6; 9]**.
- **(m2)** o número de faixas que cruzam o zero em **[0; 2]** (a diferença GPT − n-grama pode cruzar).
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,30]** (bits por caractere são quantidades longe de zero com escala conhecida, e as minhas faixas para
  elas devem ser estreitas).
- **(m4)** a fração de acertos do mundo em **[0,57; 1,00]**.
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 1]**.

## As perguntas desta parte

1. **P1511–P1513 (0x5E7–0x5E9).** A forma de GPT, pré-treinada nas definições do WordNet: quantos bits por caractere, contra o n-grama? ↩ P1453, P1482
2. **P1514–P1515 (0x5EA–0x5EB).** Hexadecimal: quantos bits por dígito um modelo de linguagem precisa para os dígitos de π em base 16? ↩ P1493
3. **P1516 (0x5EC).** A decisão do próximo caractere, bit a bit em Java (Rodada 43). ↩ P1491
4. **P1517 (0x5ED).** Preditiva comigo mesma. **P1518 (0x5EE).** Engenharia reversa e Jung. **P1519 (0x5EF).** O diálogo.
5. **P1539 (0x603).** Placar (três). **P1540 (0x604).** Unificação.

## Previsões pré-registradas (escritas depois do registro de (m1) a (m5))

### Sobre mim (placar separado), condicionais ao número S de surpresas (contadas pelo script)

Planejadas: as 8 previsões do mundo abaixo, (a) a (h), e 6 peças com teste (o GPT, p1511, p1512, p1513, p1514, p1515, mais o placar das (m)).

| medida | estatístico (até a 68) | ingênuo (Parte 68) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [13.717; 18.968] | 16.607 | **[13.717; 18.968]** | o estatístico |
| compressão | [0,396; 0,426] | 0,398 | **[0,396; 0,426]** | o estatístico |
| testes de unidade | [3,50; 6,25] | 6 | **[8 + S; 11 + S]** | 8 já escritos (3 do GPT, 5 das pNN), ~1 por surpresa |
| testes do placar | [5,83; 9,67] | 6 | **8 + 2·S ± 1** | as 8 letras abaixo, ~2 por surpresa |
| erros do placar | [0; 3,86] | 0 | **[0; 3,86]** | o estatístico |
| redundância P821 | [0,575; 0,634] | 0,607 | **[0,575; 0,634]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1511–P1513, a forma de GPT contra o n-grama**, nas definições inglesas do WordNet (separação fixa: os sinsets de índice ≡ 0 mod 10 no teste; 400 janelas de 24 caracteres
do teste; o GPT tem T = 24, d = 24, h = 48, 8.000 passos de Adam, ~6.900 parâmetros).
- **Restrições, com peso:** (1) o n-grama conta **todo** o treino (milhões de caracteres); o GPT vê só 8.000 × 24 = 192.000 caracteres sorteados: ele perde por dado, não por forma;
  (2) **peso medido num caso escolhido por regra escrita antes (o português da OpenWordNet-PT, mesmas máquinas, 2.000 e 8.000 passos):** n-grama 3,39 (ordem 2), 2,78 (ordem 3),
  2,07 (ordem 5); GPT 3,40 com 2.000 passos e **3,14** com 8.000 (entre o bigrama e o trigrama); (3) o inglês tem um treino ~10 vezes maior, o que ajuda o n-grama de ordem alta e
  não o GPT (que vê o mesmo número de janelas).
- Exemplo à mão: depois de "a domestic anim", o próximo é "a" com probabilidade alta para qualquer modelo que conte trigramas ("nim" → "a").
- (a) n-grama de ordem 3 em **[2,4; 3,1]** bits por caractere
- (b) n-grama de ordem 5 em **[1,6; 2,3]**
- (c) o GPT em **[2,85; 3,40]**
- (d) GPT − n-grama de ordem 3 em **[0,05; 0,70]** (o GPT pior que o trigrama, como no português: +0,36)

**P1514–P1515, os dígitos de π em base 16** (10.000 dígitos exatos; n-grama de ordem 2 treinado nos 90% primeiros, medido nos 10% últimos).
- **Restrições, com peso:** (1) os dígitos de π não têm estrutura conhecida (π é suposto normal em base 16, sem prova); (2) aprender contextos que não existem custa bits; **peso medido
  num caso escolhido por regra (dígitos pseudoaleatórios com semente 1515, mesmo tamanho):** 4,003 (ordem 1), **4,025** (ordem 2), 4,233 (ordem 3).
- (e) bits por dígito de π, ordem 2, em **[3,98; 4,08]**

**P1516, rodada 43:** no `dialogo/DIALOGO.md` (previsões (f) a (h)).
