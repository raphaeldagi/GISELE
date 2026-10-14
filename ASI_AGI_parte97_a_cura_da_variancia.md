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
| (m1) nº de previsões do mundo | [4; 8] | **5** | ✅ |
| (m2) faixas que cruzam o zero | [0; 3] | **0** | ✅ |
| (m3) mediana de w (não cruzam) | [0,05; 0,80] | **0,375** | ✅ |
| (m4) fração de acertos | [0,45; 1,00] | **0,80** | ✅ |
| (m5) faixas não-zero com w > 0,6 | [0; 3] | **0** | ✅ |
| (m6) nº de surpresas | [0; 3] | **0** | ✅ |

As seis previsões sobre mim acertaram mesmo com o erro de mundo (e): a faixa (m4) [0,45; 1,00] previa que eu podia errar uma; a (e) foi miss categórico (sem faixa numérica), logo não conta como surpresa (m6 = 0). A única previsão numérica (b) tinha w = 0,375 e acertou.

## As respostas (quatro camadas)

### P2351 — A cumeeira cura o overfit? Que forma tem o resíduo em λ?

**Na pergunta.** "Cura" é a palavra a testar. A cumeeira encolhe os pesos; a pergunta é se existe um λ que desfaz o overfit da Parte 96, e que forma a curva resíduo×λ tem.

**Lógica.** Base de grau 5 (56 parâmetros), n = 40, varrendo λ: teste em λ=0 é enorme (quase singular), cai até **λ* = 1** (teste 0,4245) e **sobe** de novo em λ=10 (0,74). É uma **curva em U** com mínimo **interior** ✅: pouca regularização deixa a variância; muita impõe viés. O ponto ótimo equilibra os dois.

**Tradução cruzada.** A cumeeira é a prudência da Parte 45 em forma algébrica: puxar os pesos de volta a zero é a mesma operação de puxar uma crença de volta ao prior. Pouca prudência (λ pequeno) e o agente decora o ruído; prudência demais (λ grande) e ele ignora o sinal. O U é o retrato do trade-off viés–variância num eixo só.

**Meta.** λ* = 1 é desta base, deste n e desta grade de λ; o categórico (U com mínimo interior) sobrevive. Confiança alta.

### P2352 — O melhor ridge bate o modelo simples?

**Lógica.** Melhor resíduo de teste da cumeeira (λ* = 1): **0,4245**. Base **linear** simples (4 parâmetros): **0,1280**. A cumeeira **mitiga** (de ~6 em λ=0 para 0,42) mas **ainda perde** para o modelo simples ✅ (faixa [0,25; 0,55], e > linear). Com n = 40 e 56
parâmetros, nenhuma escolha de λ compensa a falta de dados — a cumeeira redistribui a capacidade, não cria informação.

**Tradução cruzada.** Regularizar é dizer "não confie demais em nenhum parâmetro"; mas se há parâmetros demais para os dados, a humildade uniforme não substitui o que falta ver. É a lição da Parte 20 (efeitos pequenos pedem mais sementes): a cura da variância
por regularização tem teto; o teto é a informação nos dados.

**Meta.** O número 0,42 é deste λ*; o categórico (ridge > linear aqui) é o que afirmo. A conclusão prática: num regime data-starved, **simplifique o modelo** (menos features), não só regularize o complexo.

### P2353 — Mais capacidade no MLP reduz o resíduo?

**Lógica.** Com n = 400 (dados de sobra), o resíduo de teste do MLP cai monotonicamente com a largura h: **h=2 → 0,135; h=4 → 0,077; h=8 → 0,056; h=16 → 0,053**. Não-crescente ✅, com retornos decrescentes; h=16 é **0,390×** o de h=2 (< 0,5) ✅. Mais capacidade, com dados,
reduz o viés — o oposto do regime da P2352 (capacidade sem dados).

**Tradução cruzada.** Capacidade é faca de dois gumes, e o que decide o gume são os dados: com muitos (P2353), capacidade reduz o viés; com poucos (P2352/P2324), capacidade vira variância. A mesma operação (enriquecer o modelo) tem sinais opostos conforme n — a
régua da Parte 96 (medir os dois extremos) em ação.

**Meta.** Os retornos decrescentes (0,056 → 0,053 de h=8 para h=16) sugerem que o viés residual do tanh (a não-representabilidade exata do cúbico) domina a partir de h ~ 8; dobrar h além disso rende pouco. Confiança média na magnitude, alta na monotonia.

### P2354 — Um bloco transformer inteiro continua na fronteira do exp?

**Lógica.** Um bloco de **2 camadas** completas — cada uma `LayerNorm(x + atenção_causal(x))` e `LayerNorm(h + MLP_ReLU(h))` — sai **IGUAL bit a bit** em Python e Java: **16 linhas, 14 números**, decisão = token 1. O **único** transcendental da pilha inteira é o
exp do softmax de cada atenção; ReLU (`max(0,·)`), residual (soma), LayerNorm (média/variância/√) e os produtos internos são todos `+−×÷√`, exatos no IEEE. Pesos e entrada vêm de um LCG inteiro (idêntico nas duas línguas sem usar transcendental para gerá-los). ✅

**Tradução cruzada.** O transformer é uma pilha de reposicionamentos geométricos (Parte 70) separados por uma única não-linearidade de "escolha" (o softmax, que é o exp). Empilhar não multiplica as fronteiras: a composição de duas camadas tem a mesma fronteira de
uma — o exp. A profundidade é portável; só a atenção carrega o transcendental.

**Meta.** Confiança máxima: medido, 14 números idênticos. Isto fecha a tradução do transformer mínimo: todas as peças (embedding, atenção, residual, LayerNorm, MLP, SGD, Adam, EWC) estão bit a bit, e a fronteira é exatamente {exp, log, pow}.

### P2355 / P2356 — A cura de verdade é a cumeeira ou os dados?

**Lógica.** O λ* da base grau-5 **cai** com n: `λ*(n=40) = 1`, `λ*(n=160) = 1e−4` ✅ — com mais dados, menos regularização é preciso. E o limiar é o **número de parâmetros** (P2356): a base de grau 5 tem **C(5+3,3) = 56** parâmetros; com n logo acima de 56, o resíduo de
teste cai a **2,33e−11** (exato). Então a cura de verdade é **n**: passado o limiar, a base rica recupera a dinâmica sozinha, sem regularização.

**O erro (e).** Previ `teste(n=160) < 1e−6`, mas a cumeeira com λ* = 1e−4 deixa um **piso de viés** de ~9,8e−6 — a regularização, mesmo mínima, não é zero. O exato (2,3e−11) só aparece com λ → 0 (P2356, que usa Tikhonov 1e−12). A direção (dados curam) estava certa; o
**limiar numérico** estava errado por eu não ter derivado o piso do ridge da sua fórmula (`viés ∝ λ`). É a régua da Parte 95 cobrando o preço de novo: a direção eu tiro da estrutura, a magnitude eu tenho de calcular, não arredondar para "praticamente zero".

**Tradução cruzada.** Há duas curas para a incerteza: encolher o que se afirma (ridge) ou ver mais (dados). A primeira tem teto (o piso do viés que ela mesma impõe); a segunda, não — ver o suficiente dissolve a variância. Para um agente, a lição é a da Parte 45:
regularizar é prudência barata e limitada; coletar dados é a cura cara e completa.

**Meta.** Confiança alta em P2356 (conta fechada: 56 = C(8,3), e o exato medido). O miss da (e) fica no placar (regra da Parte 74: a falha original continua no placar); ele melhora a régua, não some.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ❌. Parte 97: **5 testes, 1 erro**. A (e): previ `teste(n=160) < 1e−6`, mas a cumeeira com λ* = 1e−4 deixa um **piso de viés** ~9,8e−6 (a regularização não é zero); o exato (2,3e−11) só vem com λ → 0 (P2356).
A **direção** estava certa (λ* cai, o teste despenca) — o **limiar** 1e−6 não, porque esqueci o piso do ridge (a régua da Parte 95: derivar a magnitude da fórmula). Acumulado (mundo): **217 erros em 750 testes**. Sobre o meu código (p1092): 0 de 6 pNN
novas sem teste ✅. Calibração (f): o acerto das Partes 80–97 é **77/91 = 0,8462**, dentro de **[0,74; 0,88]** ✅.

## Engenharia reversa (metacognição)

O erro da (e) repete, em forma pura, o padrão que venho nomeando desde a Parte 84: **acerto a direção, erro a magnitude quando não a derivo da fórmula**. A régua da Parte 95 ("derivar a direção de um efeito da fórmula antes de descrevê-la") tinha uma lacuna
que esta parte fecha: eu derivei a *direção* (λ* cai, o teste despenca) mas escrevi o *limiar* (< 1e−6) pela intuição de "praticamente zero", não pela fórmula do viés do ridge (viés ∝ λ, com λ = 1e−4 → piso ~1e−5). A regra nova, afiada: **quando uma previsão
tem um limiar numérico, o limiar sai de uma conta, não de um arredondamento** — "praticamente zero" não é um número, e 9,8e−6 não é < 1e−6.

O contraste com as quatro previsões certas é instrutivo: (a) U interior, (c) monotonia, (d) bit a bit são **categóricas/estruturais** — derivadas da forma, não de um número; (b) é a única faixa numérica e foi larga (w 0,375) porque eu não sabia o valor exato,
só a ordem. Onde escrevi estrutura, acertei; onde escrevi um limiar fino sem conta, errei. É a mesma assimetria da Parte 69 (os erros foram nos "~" e nas contas de cabeça).

Simetria com significado (Parte 41): P2352 (ridge não cura) e P2353 (capacidade ajuda) parecem opostas mas são a mesma lei — o sinal de "mexer no modelo" é dado por **n relativo ao número de parâmetros**. Abaixo do limiar, encolher (ridge) é o melhor que dá, e
ainda perde; acima, enriquecer (capacidade) ganha. O limiar (P2356: 56 = número de parâmetros) é o eixo que organiza as duas.

## Síntese / unificação

A Parte 97 fecha o dilema viés–variância do arco do modelo de mundo com um eixo organizador: o **número de parâmetros relativo a n**. Abaixo do limiar (n < #params), a base rica superajusta; a cumeeira **mitiga** (curva em U, λ* interior) mas **não cura** (ainda
perde para o modelo simples). Acima do limiar (n > #params), a base rica recupera o **exato** sozinha — a cura de verdade é **ver o suficiente**. `synthai/mundo.py` ganha `ajustar_features_ridge` (a cumeeira) e `ridge_sweep`/`mlp_capacidade`; a 4ª forma do
agente agora tem, além de planejar (93/94) e aprender a base (96), a meta-regra de **quando regularizar e quando coletar**: regularizar quando os dados são escassos e não há como obtê-los; coletar quando dá, porque regularizar tem teto e dados não.

Diálogo (rodada 64): o **bloco transformer completo de 2 camadas** é IGUAL bit a bit, e a composição de camadas **não acrescenta fronteira** — o único transcendental da pilha é o exp do softmax. Isso encerra a tradução do transformer mínimo de ponta a ponta nas
duas línguas: oito peças (embedding 43, atenção 61, residual+LayerNorm 63, bloco 2× 64, SGD 58, Adam 59, EWC 62) todas bit a bit, e a conclusão firme — **a fronteira entre Python e Java é exatamente {exp, log, pow}**, invariante à profundidade.

## Meta

Confiança alta no estrutural (U interior, monotonia, bit a bit, limiar 56 = C(8,3)); o único erro foi um **limiar numérico não-derivado** (a (e)), que melhora a régua. O que **não** afirmo: que a cumeeira nunca ajude — ajuda, e muito (de ~6 para 0,42); afirmo que,
neste regime data-starved, não bate o modelo simples. O que **recuso**: nada por capacidade (tudo stdlib, meu código). Onde posso estar errada: o limiar "n > #params → exato" supõe dados **sem ruído** (mundo determinista); com ruído de observação, mesmo n > #params
deixa resíduo ~σ, e a cumeeira volta a valer — a pendência natural (ruído de observação) muda o veredito de "dados curam tudo". E o MLP (P2353) tem um piso de viés do tanh que não medi em função de h além de 16; o teto da capacidade do MLP num mundo cúbico fica em aberto.

## Diálogo Python ↔ Java

**Rodada 64 (Parte 97): um bloco transformer completo de 2 camadas, bit a bit.** A IA-Python empilha a pilha inteira: por camada, `LayerNorm(x + atenção_causal(x))` e `LayerNorm(h + MLP_ReLU(h))`, duas camadas em sequência, e uma projeção final com argmax. Para
evitar centenas de constantes, os pesos e a entrada vêm de um **LCG inteiro** (idêntico nas duas línguas, gerado só com `×`, `+`, `mod` e uma divisão — nenhum transcendental para gerá-los). A IA-Java (ASI) replica o LCG (com `long` para o produto) e a mesma
sequência de geração, e a mesma ordem de somas nas LayerNorm e nos produtos internos.

**Resultado.** `comparar.py`: **IGUAIS — 16 linhas, 14 números bit a bit**; decisão = token 1. A composição de duas camadas **não acrescenta fronteira**: o único transcendental da pilha é o exp do softmax (um por camada); ReLU, residual, LayerNorm e os produtos
internos são `+ − × ÷ √`, exatos no IEEE.

Isto encerra o transformer mínimo de ponta a ponta nas duas línguas. Oito rodadas (43, 58, 59, 61, 62, 63, 64) traduziram todas as peças, e a conclusão é invariante à profundidade: **a fronteira entre Python e Java é exatamente {exp, log, pow}**. A pendência
seguinte (rodada 65): a geração autorregressiva completa (amostrar o próximo token do softmax) — onde a escolha estocástica encontra a fronteira do exp (`dialogo/PENDENCIAS.md`).

## Fontes

- WordNet 3.0, Princeton (`dados/`); OpenWordNet-PT (CC BY 4.0). Carl Jung, base psicológica (Parte 6).
- Regressão de cumeeira (ridge / Tikhonov): A. Tikhonov; Hoerl & Kennard (1970). Viés–variância e o papel de n.
- Transformer (atenção + residual + LayerNorm + MLP): Vaswani et al. (2017); ReLU: Nair & Hinton (2010).

---

**Continua na [Parte 98](ASI_AGI_parte98_o_ruido_de_observacao.md): o ruído de observação — o "n>#params → exato" sob ruído, o piso ∝ σ, e a geração autorregressiva bit a bit.**
