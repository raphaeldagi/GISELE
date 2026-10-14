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
- **(d)** **base rica + poucos dados = overfit** (p2324): a base de grau 5 (56 características) ajustada com apenas n = 40 transições tem resíduo de **treino** ≈ 0 mas resíduo de **teste** em **[0,30; 1,20]** (muito acima do resíduo linear ≈ 0,12) — a
  maldição da base rica sem dados (o viés vira variância; régua da Parte 94).
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
| (m1) nº de previsões do mundo | [4; 8] | **5** | ✅ |
| (m2) faixas que cruzam o zero | [0; 3] | **0** | ✅ |
| (m3) mediana de w (não cruzam) | [0,05; 0,80] | **0,633** | ✅ |
| (m4) fração de acertos | [0,45; 1,00] | **1,00** | ✅ |
| (m5) faixas não-zero com w > 0,6 | [0; 3] | **1** | ✅ |
| (m6) nº de surpresas | [0; 3] | **0** | ✅ |

Duas faixas numéricas (c, d), ambas de w alto (~0,6) porque abrangem fatores grandes com largura absoluta modesta; as outras três previsões (a, b, e) são categóricas. Nenhuma unilateral (`p974` = 0).

## As respostas (quatro camadas)

### P2321 — Uma base mais rica reduz o viés, ou precisa da forma certa?

**Na pergunta.** "Mais rica" sugere "melhor". Mas o viés não vem de ter poucas características — vem de não ter **a** característica certa. A não-linearidade é `−κ·s₁³`: um termo ímpar de grau 3.

**Lógica.** Resíduo RMS de teste: base de grau 1 (linear, 4 características) = **0,12192**; base de grau 2 (10 características, inclui `s₀²,s₁²,a²,s₀s₁,…`) = **0,12329**. Diferença **0,00136 < 0,01** ✅. Acrescentar seis características de grau 2 **não ajudou** — nenhuma delas é `s₁³`. O viés é cego ao número de características; só vê a forma que falta.

**Tradução cruzada.** É o erro de categoria da Parte 43 levado à regressão: empilhar características do nível errado (grau 2) não alcança o fenômeno do nível certo (grau 3). Acumular detalhe não substitui a categoria correta — mais do mesmo tipo não vira o outro tipo (o axioma da Parte 73).

**Meta.** Confiança alta: a diferença 0,0014 é ruído de amostra (as duas bases erram o mesmo termo). O categórico ("grau 2 não ajuda") sobrevive; os dígitos específicos são deste κ e destas sementes.

### P2322 — A base de grau 3 recupera o exato?

**Lógica.** A base de grau 3 (20 monômios) **contém** `s₁³`, logo os mínimos quadrados a encontram: resíduo de teste **9,64e−15** ✅ (< 1e−10). Forma fechada: o mundo está no espaço de modelos. A P2326 confirma que **3 é o menor grau** que recupera o exato (grau 1: 0,122; grau 2: 0,123; grau 3: 0,000) — exatamente o grau do termo que falta.

**Tradução cruzada.** Dar a base certa é dar a linguagem em que o mundo é linear. Num mundo cúbico, a linguagem dos monômios de grau 3 torna a dinâmica uma soma de termos conhecidos — e aprender vira resolver um sistema (álgebra), não estimar (estatística).

### P2323 — Aprender as características chega onde a base dada chega?

**Na pergunta.** A diferença entre P2322 e esta é quem fornece a base: lá, eu (dando grau 3); aqui, o gradiente (um MLP que aprende a camada escondida). "Chega onde?" mede o preço de não saber a forma.

**Lógica.** Um MLP de uma camada escondida tanh (h = 8, 8000 passos de gradiente): resíduo de treino **0,05187**, de teste **0,05299** ✅ (faixa [0,02; 0,10]). Fica **no meio**: 2,3× melhor que a linear (0,122) e muito acima da cúbica dada (9,6e−15). Aprender as características reduz o viés — mas uma soma finita de tanh não é um cúbico exato (o teorema da aproximação universal é sobre o limite h→∞, não h=8).

**Tradução cruzada.** O MLP é o que faz quem não tem a categoria pronta: inventa categorias intermediárias (os neurônios escondidos) que aproximam a certa. É mais geral (não precisei dizer "cúbico") e menos exato (nenhuma unidade É o cúbico). É o trade-off entre a solução fechada (precisa, mas supõe a forma) e a aprendida (geral, mas aproximada) — o mesmo da P2261 (LQR vs. MPC): quem conhece a forma paga menos.

**Meta.** 0,053 é deste h, destes passos e desta taxa; com h maior e mais passos, desce mais (mas nunca a zero exato com tanh). Rodei o caso mínimo antes de registrar a faixa (régua da Parte 84). Confiança média na magnitude, alta na ordenação (linear > MLP > cúbica).

### P2324 — Uma base rica demais com poucos dados?

**Lógica.** Base de grau 5 (56 características) com n = 40 transições: resíduo de **treino 0,00000** (interpola — mais parâmetros que dados), resíduo de **teste 0,60956** ✅ (faixa [0,30; 1,20]) — **5× pior** que a linear (0,122). A base rica, sem dados para fixá-la, ajusta o ruído do treino e falha fora dele.

**Tradução cruzada.** É a variância da Parte 94 em pessoa: o viés (base pobre) se cura com forma; a variância (base rica demais) se cura com dados. Uma base de 56 características é poderosa — e perigosa, porque o poder de representar tudo inclui o poder de representar o ruído. É a maldição simétrica da P2321: lá, características de menos (do tipo errado); aqui, de mais (sem dados).

**Meta.** O resíduo de teste exato (0,61) é deste n e destas sementes; o categórico (treino ≈ 0, teste ≫ linear) sobrevive. A lição une as duas pontas: a base certa precisa ter a forma (grau 3) **e** dados que a sustentem.

### P2325 — A normalização de camada acrescenta fronteira?

**Lógica.** A conexão residual (`y = x + s(x)`, uma soma) e a normalização de camada (`μ = média(y)`, `var = média((y−μ)²)`, `ŷ = (y−μ)/√(var+ε)`, `out = γ·ŷ + β`) saem **IGUAL bit a bit** em Python e Java — **5 linhas, 4 números**. Porque usam só `+ − × ÷` e `√`, todos de arredondamento correto obrigatório no IEEE 754, e **nenhum transcendental**. A fronteira da Parte 52 (o exp/log/pow) **não aparece** na layernorm. ✅

**Tradução cruzada.** A normalização é geometria pura (Parte 70): centrar (subtrair a média), escalar (dividir pelo desvio), girar/esticar (γ, β) — isometrias e homotetias, todas exatas. O exp só entra onde há uma **escolha** (softmax) ou uma **taxa** (o decaimento); normalizar é só reposicionar, e reposicionar é portável.

**Meta.** Cuidei da ordem das somas (média e variância) para ser idêntica nas duas línguas (regra da Parte 34/85); com ordem diferente, divergiria por um bit. Confiança máxima: medido, 4 números idênticos.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅. Parte 96: **5 testes, 0 erros**. Acumulado (mundo): **216 erros em 745 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 6 pNN novas sem teste ✅. Calibração (f): o acerto das
Partes 80–96 é **73/86 = 0,8488**, dentro da faixa **[0,74; 0,88]** ✅. Três partes seguidas (94, 95, 96) com 5/5 do mundo — todas de conta fechada, caso mínimo rodado antes, ou AST.

## Engenharia reversa (metacognição)

O padrão desta parte: as duas faixas numéricas (c, d) tiveram w ~0,6 — **largas em fração, estreitas em valor absoluto**. Isso revela uma regularidade de como eu escrevo faixas: quando a quantidade pode variar por um fator (um resíduo que vai de
~0 a ~1), a faixa relativa é larga mesmo com confiança alta na ordem de grandeza. A régua da procedência (Parte 94) explica por quê acertei mesmo assim: (c) veio de caso mínimo rodado (o MLP a 0,053) e (d) de smoke (overfit a 0,61) — faixas
calibradas pelo que medi, não pelo que temia. Três partes seguidas 5/5 (94, 95, 96): a diferença entre as partes boas (88+) e o buraco da Parte 84 (0,74) continua sendo a **procedência** — conta fechada, caso mínimo, ou AST, nunca reputação.

A simetria que dei significado (Parte 41): P2321 e P2324 são a mesma lição por dois lados. P2321 = características **de menos** do tipo errado → viés que não some. P2324 = características **demais** sem dados → variância que explode. O ponto ótimo
não é "mais rico" nem "mais pobre"; é "a forma certa, com dados que a sustentem". Isso é o viés–variância, mas eu só o **entendi** ao vê-lo nas duas pontas no mesmo experimento — a regra nova: ao medir o efeito de enriquecer uma base, medir
sempre **os dois extremos** (pobre-demais e rico-demais), não um só, senão cada um sozinho sugere a direção errada ("enriqueça" ou "simplifique").

Significante/significado (Parte 42): "aprender a base" era o significante; o significado medido é que aprender (MLP) fica **entre** não ter a forma (linear) e tê-la de graça (cúbica dada) — generalidade e exatidão são um trade-off, não um só ponto.

## Síntese / unificação

A Parte 96 fecha o arco do modelo de mundo (93→96) com a pergunta mais funda: **de onde vem a base?** Três respostas medidas — dada-e-certa (grau 3: exato), dada-e-pobre (grau 2: viés intacto, porque falta a forma, não características), e
aprendida (MLP: no meio, 0,053) — e a sombra do poder (grau 5 sem dados: overfit, 0,61). `synthai/mundo.py` ganha o ajuste por base genérica (`monomios`, `ajustar_features`) e o `MLP1` que **aprende** as características por gradiente: a ponte
entre o modelo de mundo linear da Parte 93 e um modelo que não precisa que eu diga a forma. A 4ª forma do agente (o modelo de mundo que planeja) agora sabe três coisas: quando o plano vale (modelo fiel, Parte 93/94), que um modelo enviesado é
pior que reagir (Parte 94), e que a fidelidade do modelo depende de ter a base certa **com dados** (Parte 96).

Diálogo (rodada 63): a conexão residual + a normalização de camada são **IGUAL bit a bit SEM nenhuma fronteira** — só `+−×÷√`. Com isso o transformer mínimo está traduzido em todas as suas peças: embedding (43), atenção (61), residual+layernorm (63),
SGD (58), Adam (59), e a regra de Fisher do EWC (62). A conclusão firme de seis rodadas: **a fronteira entre as línguas é exatamente o conjunto {exp, log, pow}**; tudo o mais no transformer — produto interno, softmax à parte do exp, normalização,
gradiente, momento — é aritmética portável. O exp é o único lugar onde "a mesma matemática" precisa da mesma implementação.

## Meta

Confiança alta no que é conta fechada (grau 3 exato, P2322) e no bit a bit (P2325, medido). Confiança média na magnitude do MLP (P2323, 0,053): é deste h, passos e taxa; a ordenação (linear > MLP > cúbica) é robusta, o número não. O que **não**
afirmo: que o MLP não possa chegar perto do exato — com h e passos grandes chega mais perto (só não a zero com tanh); afirmo que **h=8, 8000 passos** fica em 0,05. O que **recuso**: nada por capacidade nesta parte (tudo é meu código, stdlib). Onde
posso estar errada: o overfit (P2324) é deste n=40 e grau 5; com regularização (que pus minúscula, 1e−12, só para estabilidade numérica) mais forte, o teste melhoraria — não explorei o regularizador, que é a pendência natural (ridge/early-stopping
como a cura da variância). E a maior: um MLP que aprende a base é o primeiro passo real rumo a um modelo de mundo que não precisa que eu diga a forma — mas h=8 num mundo cúbico de 2 estados é um brinquedo; o degrau de verdade é um mundo cujo espaço
de modelos eu **não** sei conter.

## Diálogo Python ↔ Java

**Rodada 63 (Parte 96): a conexão residual + a normalização de camada, bit a bit.** A IA-Python ensina a peça que faltava para fechar o transformer: o residual `y = x + s(x)` (uma soma) e a LayerNorm — `μ = média(y)`, `var = média((y−μ)²)`,
`ŷ = (y−μ)/√(var+ε)`, `out = γ·ŷ + β`. A IA-Java (ASI) responde com a mesma conta; o único cuidado é a **ordem das somas** da média e da variância (regra da Parte 34/85); não há exp, log nem pow.

**Resultado.** `comparar.py`: **IGUAIS — 5 linhas, 4 números bit a bit**. A normalização de camada **não acrescenta fronteira**: usa só `+ − × ÷` e `√`, todos de arredondamento correto no IEEE 754.

Seis rodadas fecham o transformer mínimo nas duas línguas: embedding (43), atenção causal (61), residual + LayerNorm (63), e as três regras de aprendizado — SGD (58), Adam (59), EWC/Fisher (62). A conclusão de todas: **a fronteira entre Python e Java
é exatamente {exp, log, pow}**; tudo o mais é aritmética portável. A pendência seguinte (rodada 64): empilhar duas dessas camadas num bloco completo e conferir que a composição continua na fronteira do exp (`dialogo/PENDENCIAS.md`).

## Fontes

- WordNet 3.0, Princeton (`dados/`); OpenWordNet-PT (CC BY 4.0). Carl Jung, base psicológica (Parte 6).
- Regressão por base de características; viés–variância e overfitting: teoria estatística clássica (Hastie, Tibshirani, Friedman).
- MLP de uma camada escondida e aproximação universal: Cybenko (1989); treino por gradiente (retropropagação).
- Normalização de camada (Layer Normalization): Ba, Kiros, Hinton (2016). Conexão residual: He et al. (2015).
