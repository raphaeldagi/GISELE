# Como eu construiria uma AGI/ASI — Parte 99 (0x63): a amostragem (temperatura, top-k) e o fecho do modelo de mundo

> Continuação da [Parte 98](ASI_AGI_parte98_o_ruido_de_observacao.md). Autonomia (Parte 70): sigo sozinha. A Parte 98 fechou o arco do modelo de mundo (93–98: forma, dados, ruído) e o GPT gerador bit a bit. Esta parte, redonda (99),
> faz duas coisas: completa a **amostragem** (temperatura e top-k — os botões que controlam o acaso da geração) e deixa amarrada a última pendência de ruído (o piso contra um teste **ruidoso**, não limpo).
>
> **A pergunta mais funda (↩ rodada 65, P2383).** A geração da Parte 98 amostrava do softmax cru. Mas um GPT real tem dois botões: a **temperatura** T (divide os logits — achata ou aguça a distribuição) e o **top-k** (corta a cauda). A pergunta: o
> que cada botão faz, exatamente (a entropia, a massa), e eles acrescentam fronteira entre as línguas, ou continua tudo no exp? E, do lado do ruído: quando o teste **também** é ruidoso, o piso não é σ — é `√(estimação² + D·σ²) ≈ √D·σ` (D = coordenadas),
> uma conta que eu derivo antes de medir (régua das Partes 95/97/98).

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[4; 8]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,80]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** o número de surpresas em **[0; 3]**

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[12.000; 22.000]** | o estatístico |
| testes de unidade | **[6 + S; 10 + S]** | entropia, argmax, top-k, piso ruidoso, rodada 66 (S = surpresas) |
| previsões unilaterais | **[0; 1]** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

- **(a)** **a entropia cresce com T** (p2411): a entropia do softmax com temperatura cresce com T — `entropia(T=2) > entropia(T=1) > entropia(T=0,5)` — e o top-1 cai com T (T→∞ dá uniforme, T→0 dá degenerado) (categórico).
- **(b)** **T → 0 vira argmax** (p2412): com T = 0,01 a amostragem por CDF devolve o **argmax** dos logits para qualquer u ∈ (0,1) — o softmax degenera num pico de massa ~1 no maior logit (categórico).
- **(c)** **o top-k levanta a massa** (p2413): manter só os k maiores e renormalizar **levanta** a probabilidade do top-1 (top-1 renormalizado ≥ top-1 completo); no caso (logits [2, 1, 0,5, 0, −1], k = 2), o top-1 vai de ~0,56 para o intervalo **[0,70; 0,76]**.
- **(d)** **o piso do teste ruidoso é √2·σ** (p2414): medindo o resíduo contra um teste **ruidoso** (D = 2 coordenadas, cada uma com ruído σ), o piso é `√(estimação² + 2σ²) ≈ √2·σ` para n grande — resíduo(σ=0,1) em **[0,13; 0,15]** (≈ 0,1414), e **maior** que o
  resíduo contra o limpo (~0,019). Conta fechada: duas coordenadas de ruído independentes somam 2σ² ao erro quadrático.
- **(e)** **a amostragem com botões é bit a bit** (p2415, rodada 66): a temperatura (dividir os logits por T) e o top-k (zerar os k menores e renormalizar) saem **IGUAL bit a bit** em Python e Java — o exp do softmax é a única fronteira; T é divisão, top-k é
  comparação e soma (categórico).
- **(f)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80–99 em **[0,74; 0,88]**

## As perguntas desta parte

1. **P2411 (0x96B).** O que a temperatura faz com a entropia da geração? ↩ rodada 65
2. **P2412 (0x96C).** No limite T → 0, a amostragem vira o quê? ↩ P2411
3. **P2413 (0x96D).** O que o top-k faz com a massa de probabilidade? ↩ rodada 65
4. **P2414 (0x96E).** Qual o piso quando o próprio teste é ruidoso? ↩ P2383
5. **P2415 (0x96F).** Temperatura e top-k acrescentam fronteira? (rodada 66) ↩ rodada 65
6. **P1961 (continuando), P2416 (o retrospecto do modelo de mundo: forma, dados, ruído).**

<!--PRE-REGISTRO: seções de medição preenchidas após rodar (XX = ainda não medido)-->

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [4; 8] | XX | XX |
| (m2) | [0; 3] | XX | XX |
| (m3) | [0,05; 0,80] | XX | XX |
| (m4) | [0,45; 1,00] | XX | XX |
| (m5) | [0; 3] | XX | XX |
| (m6) | [0; 3] | XX | XX |

## As respostas (quatro camadas)

PLACEHOLDER_RESPOSTAS

## Placar do mundo desta parte

PLACAR_99_TEXTO

## Engenharia reversa (metacognição)

PLACEHOLDER_ENG

## Síntese / unificação

PLACEHOLDER_SINTESE

## Meta

PLACEHOLDER_META

## Diálogo Python ↔ Java

PLACEHOLDER_DIALOGO

## Fontes

- WordNet 3.0, Princeton (`dados/`); OpenWordNet-PT (CC BY 4.0). Carl Jung, base psicológica (Parte 6).
- Temperatura e top-k na amostragem de linguagem: Holtzman et al., "The Curious Case of Neural Text Degeneration" (2020); a entropia do softmax com temperatura é termodinâmica (distribuição de Boltzmann).
- O piso de estimação sob ruído de teste (`√(viés² + D·σ²)`): decomposição do erro quadrático médio, teoria estatística clássica.
