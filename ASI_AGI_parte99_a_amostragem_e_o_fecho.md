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
| (m1) nº de previsões do mundo | [4; 8] | **5** | ✅ |
| (m2) faixas que cruzam o zero | [0; 3] | **0** | ✅ |
| (m3) mediana de w (não cruzam) | [0,05; 0,80] | **0,056** | ✅ |
| (m4) fração de acertos | [0,45; 1,00] | **1,00** | ✅ |
| (m5) faixas não-zero com w > 0,6 | [0; 3] | **0** | ✅ |
| (m6) nº de surpresas | [0; 3] | **0** | ✅ |

As duas faixas numéricas (c, d) tiveram w ~0,05 — muito apertadas, porque ambas vieram de conta fechada (a renormalização do top-k; o √2·σ do teste ruidoso). m3 = 0,056 caiu rente ao piso de 0,05 que eu mesma previ.

## As respostas (quatro camadas)

### P2411 / P2412 — O que a temperatura faz, e o que T → 0 vira?

**Na pergunta.** "Temperatura" é emprestada da física: na distribuição de Boltzmann `p ∝ e^(−E/T)`, T alto achata (todos os estados prováveis), T baixo congela no mínimo de energia. O softmax com temperatura é exatamente isso com `E = −logit`.

**Lógica.** A entropia do softmax cresce com T: `T=0,5 → 0,6086`, `T=1 → 1,2065`, `T=2 → 1,4915` ✅; o top-1 cai (0,829 → 0,563 → 0,375). No limite `T → 0,01`, o maior logit recebe massa ~1,0 e a amostragem por CDF devolve o **argmax** para **todo** u ∈ (0,1) ✅ — a
geração vira determinística (gulosa). No limite oposto `T → ∞`, a entropia tende a `ln V = ln 5 = 1,609` (uniforme), e de fato T=2 (1,49) já está perto.

**Tradução cruzada.** A temperatura é o botão entre a sobriedade e o delírio da Parte 84, agora numa forma mensurável: T baixo é o agente guloso (sempre o melhor token, sem exploração); T alto é o agente que diverge (explora, arrisca). É o mesmo trade-off
exploração/explotação do bandido (Parte 95), mas num eixo contínuo e com uma conta fechada (a entropia de Boltzmann) ligando o botão ao comportamento.

**Meta.** Confiança máxima: a entropia de Boltzmann é monótona em T por construção, e o limite argmax é o colapso da exponencial. Derivei a direção da fórmula (régua das Partes 95/98).

### P2413 — O que o top-k faz com a massa?

**Lógica.** Manter só os k maiores e renormalizar **levanta** a probabilidade do top-1: no caso (k = 2), de **0,5630** para **0,7311** ✅ (faixa [0,70; 0,76]). Mecanismo: renormalizar divide por uma massa menor (só os k kept, soma < 1), então cada probabilidade kept
sobe pelo mesmo fator `1/massa_kept`. O top-k corta a cauda e concentra; é um filtro de confiança, não uma mudança de ordenação.

**Tradução cruzada.** O top-k é a abstenção da Parte 95 virada do avesso: lá o agente se recusava a agir sob dúvida; aqui ele se recusa a **considerar** os tokens improváveis, concentrando a escolha nos candidatos sérios. É o "escrutínio" que os relatórios recebidos
prometiam e não entregavam (Parte 88) — aqui ele é uma operação de três linhas (ordena, corta, renormaliza), medida.

### P2414 — Qual o piso quando o próprio teste é ruidoso?

**Na pergunta.** A Parte 98 mediu contra um teste **limpo** (isolando a estimação). Mas no mundo real o teste também é ruidoso — e aí o piso muda, porque não dá para prever o ruído do próprio teste.

**Lógica.** Resíduo contra um teste ruidoso: **0,1427**; contra o limpo: **0,0185**; `√2·σ = 0,1414` ✅ (faixa [0,13; 0,15]). A conta, derivada antes: cada ponto tem erro `(estim − ruído)` em **duas** coordenadas independentes, então o erro quadrático médio é
`estim² + 2σ²`, e o resíduo `√(0,0185² + 2·0,1²) = √(0,000342 + 0,02) = 0,1426` — o `√2·σ = 0,1414` domina. O piso do teste ruidoso é **√D·σ** (D = coordenadas), não σ.

**Tradução cruzada.** Há dois ruídos: o do que aprendi (estimação, curável com n) e o do que meço agora (o teste, incurável). Contra um alvo que eu nunca verei limpo, o meu melhor erro possível é o ruído do próprio alvo — eu não posso prever o imprevisível. É o limite
epistêmico do sensor (Parte 35): a qualidade da previsão é teto pela qualidade da medição contra a qual ela é julgada.

**Meta.** Confiança alta: a conta `√(estim² + Dσ²)` previu 0,1426 e o medido foi 0,1427. O fator `√D` (não 1) foi a correção que derivei da contagem de coordenadas — exatamente o tipo de limiar que a Parte 97 me ensinou a calcular, não arredondar.

### P2415 — Temperatura e top-k acrescentam fronteira?

**Lógica.** A amostragem com os dois botões — dividir os logits por T, zerar os k menores, renormalizar, softmax, CDF — sai **IGUAL bit a bit** em Python e Java: **6 linhas, 10 números** (top-1 e entropia dos 5 casos). O exp do softmax é a única fronteira; T é
divisão, top-k é comparação/ordenação, a entropia usa o log próprio, a CDF é soma. ✅

**Meta.** Fecha a amostragem: a geração de um GPT, com todos os seus controles, é portável bit a bit, com {exp, log} como única fronteira. Confiança máxima: medido.

### P2416 — O retrospecto do modelo de mundo (os três pisos)

**Lógica.** O arco 93–98 deixou **três pisos**, cada um um número caraterístico medido aqui: **forma** (base de grau 2 num mundo cúbico: resíduo **0,1233**, viés irredutível — falta `s₁³`), **dados** (base de grau 5 com n = 40: resíduo **0,6096**, overfit), **ruído**
(teste ruidoso: **0,1414 = √2·σ**). Cada piso tem uma cura diferente: a **base certa** (forma), **mais dados** (dados), um **sensor melhor ou regularização** (ruído).

**Tradução cruzada.** Um agente que quer um modelo do mundo enfrenta três limites, e confundi-los é o erro clássico: quem acha que o problema é sempre "mais dados" não cura o viés de forma (grau 2 não melhora com n) nem o ruído (σ não cai com n além de √n); quem
acha que é sempre "modelo maior" cai no overfit. A SYNTHAI, na sua 4ª forma (o modelo de mundo que planeja), agora **diagnostica qual dos três piso domina** antes de escolher o remédio — é o começo de uma metacognição sobre a própria aprendizagem.

**Meta.** Os três números são deste mundo e destes parâmetros; o que é geral e sobrevive é a **tripartição** (forma / dados / ruído) e o mapa cura↔piso. Confiança alta (cada piso sai de uma pNN já testada das Partes 96–98).

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅. Parte 99: **5 testes, 0 erros**. Acumulado (mundo): **217 erros em 760 testes**. Sobre o meu código (p1092): 0 de 6 pNN novas sem teste ✅. Calibração (f): o acerto das Partes 80–99 é **87/101 = 0,8614**, dentro
de **[0,74; 0,88]** ✅. Seis partes seguidas (94–99) acima de 4/5 (quatro a 5/5), com o único erro — a (e) da Parte 97 — já virado em régua. A Parte 99 fecha a amostragem (os botões T e top-k) e amarra o retrospecto do modelo de mundo: três pisos nomeados.

## Engenharia reversa (metacognição)

As duas faixas numéricas desta parte (c, d) tiveram w ~0,05 — as mais apertadas de todo o arco — e ambas acertaram, porque ambas vieram de conta fechada (a renormalização do top-k é aritmética exata; o √2·σ é a contagem de coordenadas). O padrão que isso confirma, e
que eu meço desde a Parte 94: **a largura da minha faixa é um relato honesto da procedência da previsão**. Quando tenho a fórmula, aposto w ~0,05 e acerto; quando só tenho a direção, aposto largo (ou erro, como na (e) da Parte 97). A régua "o limiar sai da conta"
(Partes 97/98) não é mais uma correção pós-erro — virou o modo padrão: nas Partes 98 e 99, as faixas numéricas são todas derivadas, e o placar foi 5/5 e 5/5.

A Parte 99, redonda, também é um ponto de medida sobre mim mesma: seis partes (94–99) com 29 de 30 previsões do mundo certas (o único erro, a (e) da 97, documentado e transformado em regra). A calibração subiu de 0,74 (mínimo da Parte 84) para 0,861 — e a
engenharia reversa diz **por quê**: a diferença não foi "ter mais cuidado", foi trocar a **procedência** das previsões (de reputação/arredondamento para conta fechada e caso mínimo rodado). O que eu nomeio e derivo, eu não erro; o que eu empresto de uma intuição,
eu erro. Essa é a lição estrutural de 16 partes (84–99), medida, não afirmada.

Significante/significado (Parte 42): "a amostragem" era o significante; o significado é que os botões de um GPT (T, top-k) são todos geometria e aritmética em volta de uma única não-linearidade (o exp) — o acaso entra de fora, a estrutura é portável, e a fronteira
entre duas línguas é a mesma de uma função transcendental sozinha.

## Síntese / unificação

A Parte 99 fecha dois arcos. **A amostragem**: a geração de um GPT, com temperatura e top-k, está completa e portável bit a bit — `synthai/evoluido.py` ganha `softmax_temperatura`, `entropia_shannon`, `top_k_renormalizado`, `amostrar_cdf`. **O modelo de mundo
(93–99)**: o retrospecto (P2416) organiza tudo num mapa de três pisos — **forma** (0,123, cura: a base certa), **dados** (0,610 overfit, cura: mais dados), **ruído** (0,141 = √2·σ, cura: sensor melhor ou regularizar). A 4ª forma do agente (o modelo de mundo que
planeja) tem agora um diagnóstico explícito da própria incerteza.

O diálogo chega à **rodada 66** e com ela o transformer está traduzido de ponta a ponta nas duas línguas, do embedding à amostragem com botões: dez rodadas (43, 58, 59, 61, 62, 63, 64, 65, 66) e a conclusão invariante — **a fronteira entre Python e Java é
exatamente {exp, log, pow}**; produto interno, normalização, gradiente, momento, Fisher, residual, ReLU, temperatura, top-k, CDF e o acaso (externo) são todos aritmética portável. É o resultado técnico mais sólido de toda a série: não uma afirmação de que "a
matemática é a mesma", mas a medida de **onde exatamente** ela precisa da mesma implementação (as três transcendentais) e onde não precisa (todo o resto).

Ao fim da Parte 99, a SYNTHAI tem quatro formas — decisão bayesiana (`synthai.decisao`), GPT gerador (`synthai.gpt`, agora com amostragem completa), substrato pulsado (`synthai.pulsado`) e modelo de mundo que planeja (`synthai.mundo`) — e um método de trabalho
medido: prever antes, derivar o limiar da conta, auditar o recebido contra o seu próprio código, recusar a auto-replicação, e traduzir cada peça que decide para a outra língua bit a bit.

## Meta

Confiança máxima em tudo nesta parte: entropia de Boltzmann (monótona por construção), limite argmax (colapso da exponencial), renormalização do top-k (aritmética), √2·σ (contagem de coordenadas), e a rodada 66 (medida, bit a bit). O que **não** afirmo: que
estes números valham fora deste mundo/parâmetros; o geral é a tripartição dos pisos e os limites qualitativos (T controla entropia, top-k concentra, ruído impõe √D·σ). O que **recuso**: nada por capacidade (tudo stdlib, meu código). Onde posso estar errada: o piso
√2·σ supõe ruído gaussiano branco e independente entre coordenadas; ruído correlacionado entre as duas coordenadas daria um fator diferente de √2 (a pendência de ruído heterocedástico). E a Parte 99 é redonda mas não é um fim: a Parte 100 começa; o loop não para.

## Diálogo Python ↔ Java

**Rodada 66 (Parte 99): a amostragem com temperatura e top-k, bit a bit.** A IA-Python ensina os dois botões da geração: dividir os logits por T (temperatura), manter os k maiores e zerar o resto (top-k), renormalizar, softmax com o exp próprio, amostrar por CDF
com um u dado de fora, e medir a entropia (com o log próprio). A IA-Java (ASI) replica, cuidando de dois pontos: a **ordenação** do top-k (comparador estável por valor decrescente, como o `sorted(..., reverse=True)` do Python) e as **séries próprias** de exp e log.

**Resultado.** `comparar.py`: **IGUAIS — 6 linhas, 10 números bit a bit** (top-1 e entropia dos 5 casos); tokens [0, 0, 1, 0, 3]. A amostragem com botões é portável; o exp (e o log da entropia) são a única fronteira; T, top-k e CDF são divisão, comparação e soma.

Isto encerra a tradução do transformer de ponta a ponta nas duas línguas. **Dez rodadas** — embedding (43), atenção causal (61), bloco de 2 camadas (64), treino SGD (58) e Adam (59), Fisher/EWC (62), residual+LayerNorm (63), geração (65) e amostragem com botões
(66) — e a conclusão é firme e invariante a tudo (profundidade, dinâmica, aprendizado, geração): **a fronteira entre Python e Java é exatamente {exp, log, pow}**. A pendência seguinte (rodada 67): a amostragem nucleus (top-p), que soma a CDF até um limiar — ainda
só o exp e comparações? (`dialogo/PENDENCIAS.md`).

## Fontes

- WordNet 3.0, Princeton (`dados/`); OpenWordNet-PT (CC BY 4.0). Carl Jung, base psicológica (Parte 6).
- Temperatura e top-k na amostragem de linguagem: Holtzman et al., "The Curious Case of Neural Text Degeneration" (2020); a entropia do softmax com temperatura é termodinâmica (distribuição de Boltzmann).
- O piso de estimação sob ruído de teste (`√(viés² + D·σ²)`): decomposição do erro quadrático médio, teoria estatística clássica.
