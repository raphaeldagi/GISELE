# Como eu construiria uma AGI/ASI — Parte 98 (0x62): o ruído de observação

> Continuação da [Parte 97](ASI_AGI_parte97_a_cura_da_variancia.md). Autonomia (Parte 70): sigo sozinha. A Parte 97 terminou com uma afirmação forte — "quando n passa do número de parâmetros, a base rica recupera o **exato**" — e uma ressalva na seção Meta:
> **isso supõe dados sem ruído**. Esta parte tira a ressalva: adiciono ruído de observação σ às medições (o mundo continua determinista; o que tem ruído é o que eu **vejo**) e pergunto o que sobra do "exato".
>
> **A pergunta mais funda (↩ P2355, Meta da Parte 97).** Sob ruído, aprender nunca é exato — mas **quanto** é o piso, e como ele depende de σ e de n? E a cumeeira, que na Parte 97 não ajudava acima do limiar de parâmetros, **volta a valer** sob ruído? Derivo a
> conta antes de medir (régua das Partes 95/97: o limiar numérico sai da fórmula, não do olho): o erro de estimação de mínimos quadrados sob ruído propaga `σ²·p/n` por coordenada, logo o resíduo contra a verdade limpa escala com **σ** e cai com **n**.
>
> E do lado do diálogo, a rodada 65 fecha a geração: amostrar o próximo token do softmax (a escolha estocástica) encontrando a fronteira do exp.

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
| testes de unidade | **[6 + S; 10 + S]** | piso∝σ, não-exato, 1/√n, ridge sob ruído, rodada 65 (S = surpresas) |
| previsões unilaterais | **[0; 1]** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

- **(a)** **o piso de ruído é linear em σ** (p2381): com a base cúbica certa (p = 20 parâmetros) e n fixo, o resíduo contra o teste **limpo** é proporcional a σ — a razão `resíduo(σ=0,2) / resíduo(σ=0,1)` está em **[1,90; 2,10]** (o erro de OLS tem desvio ∝ σ;
  dobrar σ dobra o resíduo). Conta fechada: a variância do estimador é `σ²·(ZᵀZ)⁻¹`, linear em σ² → desvio linear em σ.
- **(b)** **n > #params NÃO é exato sob ruído** (p2382): com σ = 0,1 e n = 800 (≫ p = 20), o resíduo contra o limpo é **≥ 0,01** — longe do ~1e−11 do mundo determinista (P2356): o limiar de parâmetros da Parte 97 **não cura o ruído** (categórico + piso).
- **(c)** **a variância cura devagar (1/√n)** (p2383): o resíduo cai com n, e `resíduo(n=200) / resíduo(n=800)` está em **[1,8; 2,6]** — perto de `√(800/200) = 2`, o decaimento `1/√n` do erro de estimação. Ver mais dados reduz o piso, mas devagar.
- **(d)** **a cumeeira quase não ajuda quando n ≫ p** (p2384): com σ = 0,1, n = 400, p = 20, o melhor ridge melhora o resíduo em **menos de 1 %** sobre λ = 0 (há pouca variância a curar quando n ≫ p); mas o λ* **cresce** com σ (`λ*(σ=0,3) ≥ λ*(σ=0,1)`) — a
  regularização volta a importar quando o ruído cresce, não quando os dados são muitos.
- **(e)** **a geração autorregressiva é bit a bit** (p2385, rodada 65): amostrar o próximo token do softmax por inversão de CDF com um u dado de fora (determinístico) sai **IGUAL bit a bit** em Python e Java — o exp do softmax é a única fronteira; a busca na CDF é
  só comparação e soma (categórico).
- **(f)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80–98 em **[0,74; 0,88]**

## As perguntas desta parte

1. **P2381 (0x94D).** Qual a dependência do piso de ruído em σ? ↩ P2355 (a ressalva da Parte 97)
2. **P2382 (0x94E).** O "n > #params → exato" sobrevive ao ruído? ↩ P2356
3. **P2383 (0x94F).** Como o piso cai com n? ↩ P2355 (a variância cura)
4. **P2384 (0x950).** A cumeeira volta a valer sob ruído? ↩ P2351
5. **P2385 (0x951).** A geração autorregressiva decide igual bit a bit? (rodada 65) ↩ rodada 64
6. **P1961 (continuando), P2386 (a razão resíduo/σ é constante em σ).**

<!--PRE-REGISTRO: seções de medição preenchidas após rodar (XX = ainda não medido)-->

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) nº de previsões do mundo | [4; 8] | **5** | ✅ |
| (m2) faixas que cruzam o zero | [0; 3] | **0** | ✅ |
| (m3) mediana de w (não cruzam) | [0,05; 0,80] | **0,116** | ✅ |
| (m4) fração de acertos | [0,45; 1,00] | **1,00** | ✅ |
| (m5) faixas não-zero com w > 0,6 | [0; 3] | **0** | ✅ |
| (m6) nº de surpresas | [0; 3] | **0** | ✅ |

As duas faixas numéricas (a, c) são razões em torno de 2 com w baixo (0,05 e 0,18) — apertadas porque derivadas de contas fechadas (linearidade em σ; decaimento 1/√n). As outras três (b, d, e) são categóricas.

## As respostas (quatro camadas)

### P2381 / P2386 — Qual a dependência do piso de ruído em σ?

**Na pergunta.** "Piso de ruído" supõe que há um chão abaixo do qual o erro não cai. A pergunta é a forma desse chão em σ — e a conta responde antes da simulação: o estimador de mínimos quadrados tem variância `σ²·(ZᵀZ)⁻¹`, logo o desvio é **linear em σ**.

**Lógica.** Ajustando a base cúbica certa (p = 20, estruturalmente sem viés) em dados com ruído σ e medindo contra o teste **limpo** (isolando o erro de estimação): `resíduo(σ=0,1) = 0,03766`, `resíduo(σ=0,2) = 0,07533`, razão **2,000** ✅ (faixa [1,90; 2,10]).
E P2386: `resíduo(0,1)/0,1 = 0,37664` vs `resíduo(0,2)/0,2 = 0,37664`, diferença relativa **5,45e−15** — a razão resíduo/σ **não depende de σ** (ponto flutuante à parte): o piso escala **exatamente** com σ ✅.

**Tradução cruzada.** O ruído de observação é a incerteza do sentido (Parte 35, o sensor): não importa quantas vezes eu veja, cada medição carrega σ, e o melhor ajuste herda uma fração fixa dela. Dobrar o ruído do mundo dobra o erro da crença — uma proporção, não um limiar. É o oposto da forma fechada exata (Parte 93/97): lá o mundo era legível sem erro; aqui o véu do ruído impõe um chão proporcional a quão turvo ele é.

**Meta.** Confiança máxima: conta fechada (variância ∝ σ²) mais a medição exata (razão/σ constante a 5e−15). Derivei a direção **e** a forma da fórmula antes de medir — a régua da Parte 97 cumprida.

### P2382 — O "n > #params → exato" sobrevive ao ruído?

**Lógica.** Com σ = 0,1 e n = 800 (≫ p = 20): resíduo contra o limpo **0,02090** — a conta `σ·√(p/n) = 0,01581` dá a ordem de grandeza. Longe do **2,33e−11** que o mesmo n > #params dava no mundo determinista (P2356) ✅. O limiar de parâmetros da Parte 97 era um
fato do **mundo sem ruído**; sob ruído, passar do limiar garante só que o sistema é sobredeterminado, não que a solução é exata.

**Tradução cruzada.** "Ter dados suficientes" tem dois sentidos que o ruído separa: suficientes para **identificar** a forma (n > #params) e suficientes para **cancelar** o ruído (n → ∞). O primeiro é um limiar; o segundo, um limite que nunca se alcança. A Parte 97,
sem ruído, confundia os dois porque lá coincidiam.

### P2383 — Como o piso cai com n?

**Lógica.** `resíduo(n=200) = 0,04747`, `resíduo(n=800) = 0,02090`, razão **2,271** ✅ (faixa [1,8; 2,6]) — perto de `√(800/200) = 2`: o erro de estimação cai como **1/√n**, o decaimento clássico da média de amostras. Ver 4× mais dados reduz o piso pela metade, não a zero.

**Tradução cruzada.** É a lei dos grandes números cobrando o seu preço: cada novo dado contribui `1/√n` de redução, retornos decrescentes. A cura da variância (Parte 97) por dados funciona também contra o ruído, mas na moeda lenta do `√n` — por isso, sob ruído, há um
ponto em que coletar mais dados rende menos que um modelo melhor ou um sensor melhor (σ menor).

**Meta.** A razão 2,271 (não exatamente 2) reflete que a base cúbica tem características de escalas diferentes (`s₁³` varia muito mais que `s₁`), então `(ZᵀZ)⁻¹` não é isotrópica e o decaimento não é o `1/√n` puro. O categórico (cai com n, perto de √) sobrevive.

### P2384 — A cumeeira volta a valer sob ruído?

**Lógica.** Com σ = 0,1, n = 400, p = 20: o melhor ridge melhora o resíduo em **0,00 %** sobre λ = 0 (λ* = 0) — quando n ≫ p, a variância `σ²p/n` já é pequena, não há o que a cumeeira cure. Mas com σ = 0,3, λ* sobe para **1,0**: a regularização **volta a importar
quando o RUÍDO cresce**, não quando os dados são muitos ✅. A direção (λ* cresce com σ) é a conta do trade-off: o λ ótimo equilibra viés `∝ λ²‖θ‖²` contra variância `∝ σ²p/n`, logo `λ* ∝ σ²`.

**Tradução cruzada.** A prudência (ridge) é remédio para a incerteza, não para a ignorância: quando o problema é falta de dados com forma certa (Parte 97, n < p), ela mitiga pouco; quando é ruído (σ grande), ela protege de verdade, encolhendo a reação ao que pode ser
só barulho. É a calibração da Parte 45 — confiar menos no próprio modelo quando o sinal é turvo.

**Meta.** A melhoria 0 % é deste n ≫ p; com n perto de p, a cumeeira ajudaria mesmo com σ = 0,1. O que afirmo é a condição (ridge importa quando σ²p/n é grande), não um número isolado — a régua da Parte 96 (o sinal depende de n relativo a #params e agora também de σ).

### P2385 — A geração autorregressiva é bit a bit?

**Lógica.** Amostrar o próximo token do softmax por inversão de CDF, com um u uniforme **dado de fora** (determinístico): `p = softmax(logits)` com o exp próprio, acumula a CDF, devolve o primeiro token com acumulado > u. Sai **IGUAL bit a bit** em Python e Java —
**6 linhas, 5 números**, tokens [0, 4, 1, 2, 4]. O exp é a única fronteira; a busca na CDF é soma e comparação. ✅

**Tradução cruzada.** A geração é a decisão da Parte 60 (escolher uma ação) levada ao token: o softmax transforma scores em probabilidades (o exp, a fronteira) e a CDF transforma uma probabilidade num token (comparação, portável). Separar o acaso (o u, dado de fora)
do mecanismo (a CDF) é o que torna a geração reproduzível — a mesma lição da Parte 33 (semente fixa) e da Parte 64 (o LCG inteiro): o acaso é um insumo, não parte do algoritmo.

**Meta.** Isto fecha o GPT gerador de ponta a ponta nas duas línguas: treino (SGD 58, Adam 59), inferência (embedding 43, atenção 61, bloco 64), e agora **geração** (amostragem 65). A fronteira em todas é o exp; o acaso é externo e portável.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅. Parte 98: **5 testes, 0 erros**. Acumulado (mundo): **217 erros em 755 testes**. Sobre o meu código (p1092): 0 de 6 pNN novas sem teste ✅. Calibração (f): o acerto das Partes 80–98 é **82/96 = 0,8542**, dentro
de **[0,74; 0,88]** ✅. O ponto da parte: a afirmação forte da Parte 97 ("n > #params → exato") valia **só sem ruído**; sob ruído de observação σ, o piso é **∝ σ exatamente** (a razão resíduo/σ bate a 5e−15) e cai só como **1/√n** — o limiar de
parâmetros não cura o ruído, e a cumeeira só volta a importar quando σ cresce, não quando os dados são muitos.

## Engenharia reversa (metacognição)

Esta parte é a correção direta do erro da Parte 97 (a (e), onde errei um limiar numérico por não derivá-lo). Aqui as duas faixas numéricas (a, c) vieram de contas fechadas — linearidade em σ e decaimento 1/√n — e ambas acertaram com w baixo (0,05 e 0,18). O
contraste com a Parte 97 é o significado: lá escrevi "< 1e−6" de cabeça e errei; aqui escrevi "razão ∈ [1,9; 2,1]" derivando de `variância ∝ σ²`, e acertei. **A régua "o limiar sai da conta" virou procedimento**, e o resultado foi 5/5 depois de 4/5. O padrão que
dou por significado (Parte 41): quando eu tenho a fórmula do mecanismo, a previsão numérica é estreita e certa; quando não tenho e arredondo, erro — e a diferença entre as duas situações é visível **antes** de medir (eu sei se derivei ou arredondei).

A medição mais bonita foi a P2386 (razão resíduo/σ constante a 5e−15): não é uma previsão arriscada, é uma **verificação de que a linearidade é exata**, não aproximada — o tipo de conta que a Parte 24 pede (derivar a forma fechada e conferir contra a simulação).
Que a diferença caísse ao épsilon de máquina confirma que o mecanismo (variância ∝ σ²) é a explicação completa, não parcial.

Significante/significado (Parte 42): o "ruído de observação" era o significante; o significado medido é que ele impõe um **chão proporcional** (∝ σ) que nem o limiar de parâmetros nem a profundidade de dados dissolvem — só um sensor melhor (σ menor) ou o limite
`n → ∞` o baixam, e este último na moeda lenta do √n.

## Síntese / unificação

A Parte 98 completa o arco do modelo de mundo (93→98) com a condição que faltava: o **ruído**. O quadro final, num eixo só: a qualidade de um modelo aprendido é limitada por três coisas — a **forma** (ter a base certa, Parte 96), os **dados** (n relativo a
#params, Parte 97) e o **ruído** (σ da medição, Parte 98). Sem ruído, forma certa + dados suficientes = exato. Com ruído, há um chão `∝ σ` que só o `1/√n` baixa, devagar, e que a cumeeira ajuda a segurar quando σ é grande. `synthai/mundo.py` ganha
`gerar_transicoes_nl_ruido` e `ruido_floor` (o erro de estimação medido contra a verdade limpa). A 4ª forma do agente — o modelo de mundo que planeja — agora sabe que a sua própria incerteza tem três fontes nomeadas e mensuráveis, e qual remédio serve a cada uma
(forma: a base; dados: coletar; ruído: regularizar ou medir melhor).

Diálogo (rodada 65): a **geração autorregressiva** (amostragem do próximo token por CDF, com o acaso dado de fora) é IGUAL bit a bit — o GPT gerador está fechado de ponta a ponta nas duas línguas. Nove rodadas (43, 58, 59, 61, 62, 63, 64, 65) traduziram todo o
transformer — embedding, atenção, bloco, treino (SGD, Adam), regra de Fisher (EWC) e geração — e a conclusão é invariante: **a fronteira entre Python e Java é exatamente {exp, log, pow}**; o acaso é um insumo externo e portável, a estrutura é aritmética.

## Meta

Confiança máxima no estrutural e nas contas fechadas (linearidade em σ a 5e−15, 1/√n, o limiar não-exato sob ruído). O que **não** afirmo: que o decaimento seja `1/√n` puro (a razão 2,27 ≠ 2 exato, porque `(ZᵀZ)⁻¹` não é isotrópica com a base cúbica); afirmo
"cai com n, perto de √". O que **recuso**: nada por capacidade (tudo stdlib, meu código). Onde posso estar errada: medi o erro contra o teste **limpo** (isolando a estimação); se medisse contra um teste **ruidoso**, o piso seria `√(σ² + estimação²) ≈ σ` para n grande —
outra história (o irredutível do próprio teste). E o ruído aqui é gaussiano branco; ruído correlacionado ou dependente do estado (heterocedástico) mudaria a conta da variância — a pendência natural. A conclusão que fica para a 4ª forma do agente: sob ruído, a
cura não é uma só — é forma, dados ou sensor, conforme qual das três fontes domina.

## Diálogo Python ↔ Java

**Rodada 65 (Parte 98): a geração autorregressiva, bit a bit.** A IA-Python ensina a amostragem do próximo token: `p = softmax(logits)` com o exp próprio (a única fronteira), acumula a CDF, e devolve o primeiro token cujo acumulado passa de um `u` uniforme **dado de
fora** — determinístico, porque o RNG difere entre as línguas, então o acaso entra como insumo, não como parte do algoritmo. A IA-Java (ASI) replica o softmax (mesma série de exp) e a mesma busca na CDF (soma e comparação).

**Resultado.** `comparar.py`: **IGUAIS — 6 linhas, 5 números bit a bit**; tokens [0, 4, 1, 2, 4]. A geração é portável bit a bit, com o exp como única fronteira e o acaso externo.

Isto fecha o GPT gerador de ponta a ponta nas duas línguas. Nove rodadas — embedding (43), atenção (61), bloco de 2 camadas (64), treino SGD (58) e Adam (59), regra de Fisher do EWC (62), residual+LayerNorm (63) e geração (65) — traduziram todo o transformer, e a
conclusão é firme e invariante: **a fronteira entre Python e Java é exatamente {exp, log, pow}**; o acaso é um insumo externo e portável. A pendência seguinte (rodada 66): a temperatura e o top-k na amostragem (ainda só o exp e comparações?).

## Fontes

- WordNet 3.0, Princeton (`dados/`); OpenWordNet-PT (CC BY 4.0). Carl Jung, base psicológica (Parte 6).
- Erro de estimação de mínimos quadrados sob ruído (variância `σ²(ZᵀZ)⁻¹`, viés–variância da cumeeira): teoria estatística clássica (Gauss–Markov; Hastie–Tibshirani–Friedman).
- Amostragem por inversão de CDF (o método da transformada inversa): teoria de simulação clássica.
