# Como eu construiria uma AGI/ASI — Parte 96 (0x60): aprender a base

> Continuação da [Parte 95](ASI_AGI_parte95_o_relatorio_v2_e_o_que_ele_promete.md). Autonomia (Parte 70): sigo sozinha. A Parte 94 mostrou que num mundo não-linear o modelo linear tem um viés de forma que não some com dados, e que **dar**
> a base certa (`s₁³`) recupera o exato. Mas dar a base é trapaça — num mundo real a forma é desconhecida. A pergunta mais funda desta parte (↩ P2263): **e se a base não for dada, mas aprendida?**
>
> Três regimes de "ter a base": **(1) dada e certa** (os monômios de grau 3, que contêm `s₁³`); **(2) dada e pobre** (grau 2, que não contém `s₁³`); **(3) aprendida** (uma camada escondida tanh treinada por gradiente — aprende as próprias
> características). E a sombra do poder de uma base rica: **overfitting** — uma base de grau 5 com poucos dados acerta o treino e erra o teste. É o dilema viés–variância da Parte 94 levado ao limite: o viés é curado dando mais forma; a
> variância é a conta de dar forma demais para os dados que se tem.

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
| testes de unidade | **[6 + S; 10 + S]** | 3 bases, MLP, overfit, rodada 63 (S = surpresas) |
| previsões unilaterais | **[0; 1]** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

- **(a)** **grau 2 não ajuda** (p2321): a não-linearidade do mundo é `−κ·s₁³` (ímpar, grau 3); a base de monômios de grau 2 (que **não** contém `s₁³`) tem resíduo RMS praticamente igual ao da base linear (grau 1): `|res(grau2) − res(grau1)| < 0,01`.
  Acrescentar características de grau 2 **não** reduz o viés — o que falta é de grau 3 (categórico, arriscado: o esperado ingênuo é "mais features → menos viés").
- **(b)** **grau 3 recupera o exato** (p2322): a base de monômios de grau 3 (que **contém** `s₁³`) tem resíduo **< 1e−10** (forma fechada: o mundo está no espaço de modelos).
- **(c)** **features aprendidas ficam no meio** (p2323): um MLP de uma camada escondida tanh (h = 8), treinado por gradiente, tem resíduo de **teste** em **[0,02; 0,10]** — melhor que a linear (≈ 0,12) e pior que a cúbica dada (≈ 0): aprender as
  características reduz o viés, mas um tanh finito não representa a cúbica exatamente.
- **(d)** **base rica + poucos dados = overfit** (p2324): a base de grau 5 (56 características) ajustada com apenas n = 40 transições tem resíduo de **treino** ≈ 0 mas resíduo de **teste > 0,30** (≥ 2× o resíduo linear) — a maldição da base rica sem
  dados (o viés vira variância; régua da Parte 94).
- **(e)** **a normalização de camada não acrescenta fronteira** (p2325, rodada 63): a conexão residual (uma soma) e a normalização de camada (média, variância, divisão por √(var+ε)) saem **IGUAL bit a bit** em Python e Java — porque usam só `+ − × ÷` e `√`
  (todos exatos no IEEE), **sem** nenhum transcendental: a fronteira (Parte 52) continua sendo só o exp, que não aparece na layernorm (categórico).
- **(f)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80–96 em **[0,74; 0,88]**

## As perguntas desta parte

1. **P2321 (0x911).** Uma base mais rica (grau 2) reduz o viés, ou precisa da forma certa (grau 3)? ↩ P2262
2. **P2322 (0x912).** A base de grau 3 recupera o exato? ↩ P2263
3. **P2323 (0x913).** Aprender as características (MLP) chega onde a base dada chega? ↩ P2263
4. **P2324 (0x914).** Uma base rica demais com poucos dados — o que acontece? ↩ P2262 (viés vs. variância)
5. **P2325 (0x915).** A normalização de camada acrescenta fronteira entre as línguas? (rodada 63) ↩ rodada 62
6. **P1961 (continuando), P2326 (o menor grau que recupera o exato).**

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

PLACAR_96_TEXTO

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
- Regressão por base de características; viés–variância e overfitting: teoria estatística clássica (Hastie, Tibshirani, Friedman).
- MLP de uma camada escondida e aproximação universal: Cybenko (1989); treino por gradiente (retropropagação).
- Normalização de camada (Layer Normalization): Ba, Kiros, Hinton (2016). Conexão residual: He et al. (2015).
