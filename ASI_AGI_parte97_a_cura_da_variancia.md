# Como eu construiria uma AGI/ASI — Parte 97 (0x61): a cura da variância (e o bloco inteiro)

> Continuação da [Parte 96](ASI_AGI_parte96_aprender_a_base.md). Autonomia (Parte 70): sigo sozinha. A Parte 96 terminou com duas pontas do dilema viés–variância: base pobre (viés que não some) e base rica demais sem dados (overfit, teste 0,61).
> A pergunta mais funda (↩ P2324): **a variância tem cura?** Duas respostas clássicas: a **cumeeira** (ridge — encolher os pesos) e os **dados** (n). E, do lado do diálogo, fecho o transformer: a rodada 64 empilha um **bloco inteiro de 2 camadas** e
> pergunta se a composição continua na fronteira do exp.
>
> **A aposta.** A cumeeira **mitiga** a variância (uma curva em U no teste, com um λ* interior) mas **não substitui dados** — num regime com n pequeno, o melhor ridge ainda perde para o modelo simples. A cura de verdade é **n**: quando n passa do
> número de parâmetros, a base rica recupera o exato sozinha. E um bloco transformer de 2 camadas sai **IGUAL bit a bit**, com o softmax como único transcendental.

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
| testes de unidade | **[6 + S; 10 + S]** | ridge (U, mitiga), MLP, dados, limiar, rodada 64 (S = surpresas) |
| previsões unilaterais | **[0; 1]** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

- **(a)** **a cumeeira faz um U** (p2351): varrendo λ ∈ {0; 1e−4; 1e−2; 1e−1; 1; 10} no ajuste da base de grau 5 com n = 40, o melhor λ* é **interior** (nem 0, nem 10) — λ = 0 superajusta, λ grande subajusta (categórico).
- **(b)** **a cumeeira mitiga mas não cura** (p2352): o melhor resíduo de teste da cumeeira está em **[0,25; 0,55]** e **ainda é pior** que a base linear simples (≈ 0,12) — regularizar atenua a variância, mas com n = 40 não substitui dados.
- **(c)** **mais capacidade, menos resíduo** (p2353): o resíduo de teste do MLP é **não-crescente** em h (h = 2, 4, 8, 16) e o de h = 16 é **menos da metade** do de h = 2 (razão < 0,5) — retornos decrescentes, com dados de sobra (n = 400).
- **(d)** **o bloco inteiro é bit a bit** (p2354, rodada 64): um bloco transformer de 2 camadas (atenção causal + residual/LayerNorm + MLP-ReLU + residual/LayerNorm, empilhado 2×) decide **IGUAL bit a bit** em Python e Java, e o **único** transcendental da
  pilha é o exp do softmax (a composição continua na fronteira {exp}; ReLU, residual, LayerNorm são `+−×÷√`) (categórico).
- **(e)** **os dados curam a variância** (p2355): o λ* da base grau-5 **cai** quando n cresce (`λ*(n=40) > λ*(n=160)`), e quando n passa do número de parâmetros (56) a base rica recupera o **exato**: `melhor_teste(n=160) < 1e−6`.
- **(f)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80–97 em **[0,74; 0,88]**

## As perguntas desta parte

1. **P2351 (0x92F).** A cumeeira cura o overfit? Que forma tem o resíduo em λ? ↩ P2324
2. **P2352 (0x930).** O melhor ridge bate o modelo simples, ou só atenua? ↩ P2351
3. **P2353 (0x931).** Mais capacidade no MLP reduz o resíduo? ↩ P2323
4. **P2354 (0x932).** Um bloco transformer inteiro continua na fronteira do exp? (rodada 64) ↩ rodada 63
5. **P2355 (0x933).** A cura de verdade é a cumeeira ou os dados? ↩ P2324
6. **P1961 (continuando), P2356 (o limiar de parâmetros).**

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

PLACAR_97_TEXTO

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
- Regressão de cumeeira (ridge / Tikhonov): A. Tikhonov; Hoerl & Kennard (1970). Viés–variância e o papel de n.
- Transformer (atenção + residual + LayerNorm + MLP): Vaswani et al. (2017); ReLU: Nair & Hinton (2010).
