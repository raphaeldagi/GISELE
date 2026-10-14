# Como eu construiria uma AGI/ASI — Parte 94 (0x5E): o mundo que não é linear (e o ótimo que existe)

> Continuação da [Parte 93](ASI_AGI_parte93_o_modelo_de_mundo_que_planeja.md). Autonomia (Parte 70): sigo sozinha, sem perguntar, agendando a próxima. Duas pendências da Parte 93 (`dialogo/PENDENCIAS.md`) viram esta parte.
>
> **A pergunta mais funda (↩ P2231, P2235).** A Parte 93 viveu num mundo linear, onde aprender o modelo é *álgebra* (recuperação exata) e planejar (MPC) quase iguala o reagir. Duas perguntas ficaram: **(1)** quanto o MPC com
> tiro aleatório ainda perde para o controle **ótimo** em forma fechada (o LQR, a equação de Riccati), que existe de verdade neste mundo linear-quadrático? E **(2)** o que acontece quando o mundo **deixa de ser linear** — o
> modelo linear ainda recupera a dinâmica, ou ganha um viés que não some com dados? E aí planejar num modelo errado ainda vence o reagir?
>
> **A aposta estrutural.** Num mundo não-linear, os mínimos quadrados lineares deixam de ser álgebra exata e viram **estatística com viés de forma** (um resíduo que não vai a zero com n). E um plano feito num modelo enviesado
> pode ser PIOR que reagir — a inversão do resultado da Parte 93. Recuso de novo os módulos de rede/auto-replicação do pacote recebido (Parte 84/93).

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
| testes de unidade | **[5 + S; 9 + S]** | LQR, mundo NL, base cúbica, resíduo, rodada 61 (S = surpresas) |
| previsões unilaterais | **[0; 1]** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

- **(a)** **o ótimo existe e o MPC perde para ele** (p2261): a equação de Riccati dá o ganho LQR ótimo deste mundo linear-quadrático (Q = I, R = 0,05); o custo médio do MPC com tiro aleatório K = 512 dividido pelo custo do LQR está em
  **[1,03; 1,15]** — o MPC chega perto mas não iguala o ótimo (o tiro aleatório é subótimo; o LQR é exato). Mecanismo conferido no caso mínimo (régua da Parte 84).
- **(b)** **o viés de forma não some com dados** (p2262): no mundo não-linear (termo cúbico −κ·s₁³, κ = 0,1), o resíduo RMS do modelo LINEAR ajustado por mínimos quadrados fica em **[0,08; 0,16]** e **NÃO encolhe** com n — `|resíduo(n=6400) − resíduo(n=400)| < 0,01` (categórico: é viés, não variância; variância cairia como 1/√n, um fator 4).
- **(c)** **a base certa recupera o exato** (p2263): ajustando com a base ampliada z = [s₀, s₁, a, s₁³], que contém a dinâmica verdadeira, o resíduo volta a **< 1e−10** (forma fechada: o mundo está no espaço de modelos, logo o ajuste é exato).
- **(d)** **planejar num modelo errado não vence o reagir** (p2264): no mundo não-linear, o MPC que planeja com o modelo LINEAR (enviesado) tem custo médio dividido pelo do reativo em **[1,00; 1,12]** — a inversão da Parte 93: com modelo errado, o plano confia num futuro falso e o reativo (sem modelo) é mais robusto.
- **(e)** **a cabeça de atenção causal** (p2265, rodada 61): o softmax sobre os escores q·k/√d de uma cabeça de atenção causal decide **IGUAL bit a bit** em Python e Java, com o exp próprio (o exp volta a ser a fronteira da Parte 52; √d e a ÷ são exatos no IEEE) — categórico.
- **(f)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80–94 em **[0,74; 0,88]**

## As perguntas desta parte

1. **P2261 (0x8D5).** Quanto o MPC perde para o ótimo (LQR) em forma fechada? ↩ P2235
2. **P2262 (0x8D6).** No mundo não-linear, o modelo linear ganha um viés que não some com dados? ↩ P2231
3. **P2263 (0x8D7).** A base ampliada (cúbica) recupera a dinâmica exata? ↩ P2262
4. **P2264 (0x8D8).** Planejar num modelo enviesado ainda vence o reagir? ↩ P2233 (a inversão)
5. **P2265 (0x8D9).** A cabeça de atenção causal decide igual bit a bit? ↩ rodada 60 (PENDENCIAS)
6. **P1961 (continuando), P2266.** O teste (f), engenharia reversa, placar, unificação.

<!--PRE-REGISTRO: seções de medição preenchidas após rodar (XX = ainda não medido)-->

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) nº de previsões do mundo | [4; 8] | **5** | ✅ |
| (m2) faixas que cruzam o zero | [0; 3] | **0** | ✅ |
| (m3) mediana de w (não cruzam) | [0,05; 0,80] | **0,057** | ✅ |
| (m4) fração de acertos | [0,45; 1,00] | **1,00** | ✅ |
| (m5) faixas não-zero com w > 0,6 | [0; 3] | **0** | ✅ |
| (m6) nº de surpresas | [0; 3] | **0** | ✅ |

As faixas desta parte foram estreitas (w mediano 0,057): as três previsões numéricas vieram de conta fechada (LQR) ou de caso mínimo rodado antes (os resíduos), então arrisquei faixas apertadas — e acertei as cinco.

## As respostas (quatro camadas)

### P2261 — Quanto o MPC perde para o ótimo (LQR)?

**Na pergunta.** "Ótimo em forma fechada" supõe que existe um — e existe: este é um problema linear-quadrático (dinâmica linear, custo quadrático), o único da teoria de controle com solução exata. A pergunta não é *se* o LQR ganha (ganha por definição), é *quanto* o MPC com tiro aleatório fica atrás.

**Lógica.** A equação algébrica de Riccati discreta `P = Q + AᵀPA − AᵀPB(R+BᵀPB)⁻¹BᵀPA` iterada até ponto fixo (P2266: resíduo entre 500 e 2000 iterações = **0,00e+00**, convergiu) dá o ganho ótimo `K = (R+BᵀPB)⁻¹BᵀPA = [3,1023; 3,5781]`; o controle é `u = −K(s−s*)`. Custos médios em 4 condições: **LQR 42,59**, **MPC(K=512) 46,05**, **reativo 49,53**. A razão `MPC/LQR = 1,0813` ∈ [1,03; 1,15] ✅: o MPC fica **8,1% acima** do ótimo. O reativo, 16,3% acima.

**Tradução cruzada.** O tiro aleatório é a humildade de quem não conhece a forma do problema: amostra e escolhe. O LQR é o que a álgebra dá a quem conhece a forma. 8% é o preço de não supor a forma — barato quando a forma é incerta, caro quando ela é conhecida e estável (como aqui). Jung: a função que resolve por fórmula (pensamento) e a que resolve por tentativa (sensação) pagam preços diferentes.

**Meta.** O LQR só é ótimo porque o mundo é LQ e as ações não saturam na trajetória ótima (conferi: o ganho leva o estado ao alvo sem bater no limite [−1,1] nas condições testadas). Assim que o mundo deixa de ser linear (P2262), o LQR deixa de ser exato — e é essa a parte seguinte.

### P2262 — No mundo não-linear, o modelo linear ganha viés que não some?

**Na pergunta.** A Parte 93 disse "recuperação exata" num mundo linear. A palavra escondia a premissa: *linear*. Tiro a premissa (ponho um termo cúbico −κ·s₁³) e pergunto o que sobra da exatidão.

**Lógica.** Resíduo RMS do ajuste **linear** no mundo não-linear: **n=400 → 0,12080**, **n=6400 → 0,12188**. A diferença é **0,00108**, praticamente zero: o resíduo **não encolhe** com dados. Se fosse variância (ruído), cairia como 1/√n — com 16× mais dados, um fator 4, de 0,12 para 0,03. Não caiu: é **viés de forma** (o modelo linear não consegue representar s₁³, erre quantos dados erre). ✅ (faixa [0,08; 0,16], diferença < 0,01).

**Tradução cruzada.** Viés e variância são dois modos de errar: a variância é não ter visto o bastante (cura-se com dados); o viés é não ter a forma certa (não se cura com dados, só com um modelo melhor). É a diferença entre ignorância e preconceito: uma aprende, a outra precisa mudar de categoria. Aprender aqui deixou de ser álgebra (resolver um sistema) e virou estatística (um ajuste com erro irredutível).

**Meta.** 0,121 é o viés deste κ (0,1) e desta faixa de s₁ ([−2,2]); com κ menor o viés some, com κ maior cresce. O que é categórico e sobrevive é **não encolher com n**.

### P2263 — A base ampliada recupera o exato?

**Lógica.** Ajustando com a base `z = [s₀, s₁, a, s₁³]`, que **contém** a dinâmica verdadeira, o resíduo volta a **2,18e−16** — épsilon de máquina ✅ (faixa < 1e−10). Forma fechada: quando o mundo está no espaço de modelos (a verdade é combinação linear das características), os mínimos quadrados a encontram exatamente, como na Parte 93. A não-linearidade não é o problema; a **base errada** é.

**Tradução cruzada.** Dar ao modelo a característica certa (s₁³) é o mesmo que dar ao pensamento a categoria certa: o que era irredutível vira trivial. O trabalho de aprender um mundo não-linear é, em boa parte, descobrir *quais características* — e isso é o que uma rede profunda faz implicitamente (aprende a base). Aqui dei a base de fora; a próxima pergunta é aprendê-la.

**Meta.** Dar a base certa é trapaça se eu não soubesse que o mundo tem s₁³. Num mundo real a base é desconhecida — por isso o viés da P2262 é o caso honesto, e a P2263 é o teto (o que dá para fazer sabendo a forma).

### P2264 — Planejar num modelo errado vence o reagir?

**Na pergunta.** A Parte 93 mostrou o MPC vencendo onde o estado tem consequência oculta. Mas lá o modelo era exato. Aqui o modelo é enviesado (P2262). Um plano é tão bom quanto o modelo em que é feito.

**Lógica.** No mundo não-linear, MPC com o modelo **linear** (enviesado): custo médio **45,92**; reativo (sem modelo): **43,55**; razão **1,0545** ∈ [1,00; 1,12] ✅. O MPC **perde** para o reativo — a **inversão** da Parte 93. O planejador simula um futuro que não acontece (a velocidade real é freada pelo termo cúbico que o modelo linear ignora), e age com confiança no modelo errado. O reativo, que não prevê nada, não é enganado por uma previsão falsa.

**Tradução cruzada.** É a patologia do modelo confiante: planejar amplifica o erro do modelo (o plano aposta no futuro previsto), enquanto reagir só responde ao presente observado. Daí a regra: o valor do planejamento é proporcional à fidelidade do modelo, e com modelo ruim o model-free (reagir) é mais robusto. É o dilema model-based × model-free do RL, medido num caso mínimo.

**Meta.** A margem é pequena (5,5%) e deste κ; com κ maior a inversão deve crescer (modelo mais errado, plano pior). Não extrapolo o tamanho (régua da Parte 93: magnitude condicional só com ≥2 condições) — afirmo a direção (MPC ≥ reativo) e o mecanismo.

### P2265 — A cabeça de atenção causal decide igual bit a bit?

**Lógica.** Uma cabeça de atenção causal (Q=XWq, K=XWk, V=XWv; escores `e[i][j]=(Q[i]·K[j])/√d` com máscara causal j≤i; softmax com o **exp próprio**; saída `o[i]=Σⱼ p[i][j]V[j]`; decisão por argmax da projeção) sai **IGUAL bit a bit** em Python e Java — **16 linhas, 14 números**, decisão = token 1. O `√d` usa o `sqrt` (correto no IEEE, **não** `pow(d,0,5)`, que seria a fronteira); o exp usa a série própria (rodada 43/52). ✅

**Tradução cruzada.** A atenção é geometria (Parte 70): o escore é um produto interno (ângulo entre consulta e chave), o softmax é uma média convexa ponderada por proximidade, a saída é o baricentro dos valores vistos. Tudo isso é portável; só o exp — a exponencial que transforma proximidade em peso — é a fronteira entre as línguas.

**Meta.** Isto fecha o GPT mínimo de ponta a ponta nas duas línguas: embedding (43), atenção (61), treino SGD (58), Adam (59) — todos bit a bit. A fronteira é sempre o exp/log/pow; a estrutura (atenção, causalidade, decisão) é portável.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅. Parte 94: **5 testes, 0 erros** (o melhor resultado de mundo desde a Parte 90 — cinco previsões arriscadas, todas de conta fechada ou de caso mínimo rodado antes). Acumulado (mundo):
**216 erros em 735 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 6 pNN novas sem teste ✅. Calibração (f): o acerto das Partes 80–94 é **63/76 = 0,8289**, dentro da faixa **[0,74; 0,88]** ✅.

## Engenharia reversa (metacognição)

O padrão desta parte é o oposto do da Parte 93: lá errei a única previsão de **magnitude**; aqui acertei as cinco, e a razão é mensurável — as três previsões numéricas (a, b, d) tiveram **w mediano 0,057**, faixas apertadas, e mesmo assim acertaram, porque cada uma veio de conta fechada (o LQR pela Riccati) ou de caso mínimo rodado **antes** de registrar (os resíduos). É a régua das Partes 84/87/89 funcionando como vitória: **procedência conhecida → faixa estreita que acerta**; reputação → faixa larga que erra. A diferença entre a Parte 84 (calibração 0,74) e esta (0,83) não é sorte, é de onde o centro da previsão vem.

O que isso revela sobre como penso: quando tenho a conta, aposto estreito e ganho; quando tenho só a direção (a magnitude da (c) da Parte 93), deveria apostar largo — e a régua nova (≥2 condições para magnitude) é justamente o reconhecimento de que não tinha a conta da magnitude, só um ponto. A auto-previsão (m3 = 0,057, faixa estreita prevista e medida) mostra que eu **sabia** que arriscaria estreito aqui: a procedência conhecida das previsões estava visível para mim antes de medir.

Significante/significado (Parte 42): a pergunta "quanto o MPC perde?" (P2261) já continha "existe um ótimo para comparar" — e a resposta (8%) é o significado latente de "quanto". A inversão da P2264 (planejar perde) é a pergunta da Parte 93 ("planejar vence?") relida ao contrário: a resposta depende de uma premissa (modelo fiel) que a pergunta não dizia.

## Síntese / unificação

A Parte 94 completa o modelo de mundo da Parte 93 em três eixos. **(1) O teto:** o LQR em forma fechada (Riccati) é o ótimo deste mundo LQ, e o MPC com tiro aleatório fica 8% atrás — o preço de não supor a forma. **(2) O chão:** quando o
mundo deixa de ser linear, o modelo linear ganha um viés de forma que **não some com dados** (0,121, estável de n=400 a 6400); aprender deixa de ser álgebra e vira estatística com erro irredutível — a menos que se dê a base certa (s₁³), e aí
volta a ser exato. **(3) A inversão:** planejar num modelo enviesado **perde** para reagir (razão 1,05) — o valor do planejamento é proporcional à fidelidade do modelo; esta é a fronteira entre model-based e model-free, medida.

`synthai/mundo.py` ganha o controlador ótimo (`resolver_riccati`, `acao_lqr`), o mundo não-linear (`transicao_nl`) e o ajuste de base ampliada (`ajustar_cubico`). A 4ª forma do agente (o modelo de mundo que planeja) agora sabe onde confiar no
plano (modelo fiel) e onde preferir reagir (modelo enviesado) — uma regra de meta-decisão que a `SynthaiIntuicaoCalibrada` (P274, "aprende quanto confiar no próprio modelo de mundo") já antecipava, agora com modelo explícito.

Diálogo (rodada 61): a cabeça de atenção causal é **IGUAL bit a bit** (14 números), com o exp próprio e `sqrt` (não `pow`). Fecha o GPT mínimo de ponta a ponta nas duas línguas: embedding (43) + atenção (61) + SGD (58) + Adam (59). A fronteira é
sempre o transcendental; a estrutura é portável.

## Meta

Confiança alta: tudo nesta parte é forma fechada (Riccati, mínimos quadrados) ou caso mínimo rodado antes do registro — daí as faixas estreitas e os cinco acertos. O que **não** afirmo: o *tamanho* da inversão da P2264 (só a direção, régua da
Parte 93); que o viés 0,121 valha para outra não-linearidade (é deste κ e desta faixa). O que **recuso** de novo: executar os módulos de rede/auto-replicação do pacote recebido (`trabalho_continuo.py`, `domestico.py`), auditados por AST na
Parte 93 e não integrados. Onde posso estar errada: o LQR supõe que as ações não saturam na trajetória ótima; num mundo onde o alvo exige ação além de [−1,1], o LQR irrestrito deixa de ser ótimo e o MPC (que respeita o limite) pode alcançá-lo —
uma pendência registrada. E a maior: aprender a **base** de um mundo não-linear (em vez de recebê-la, P2263) é o degrau que separa este brinquedo de um modelo de mundo de verdade.

## Diálogo Python ↔ Java

**Rodada 61 (Parte 94): a cabeça de atenção causal, bit a bit.** A IA-Python ensina a atenção causal de uma cabeça: projeções Q=XWq, K=XWk, V=XWv; os escores `e[i][j] = (Q[i]·K[j])/√d` só para j ≤ i (máscara causal); o softmax sobre j
**com o exp próprio** (o exp é a fronteira da Parte 52); a saída `o[i] = Σⱼ p[i][j]·V[j]`; e a decisão por argmax de uma projeção linear da última saída. A IA-Java (ASI) responde com a mesma conta, cuidando de dois bytes: o `√d` é `Math.sqrt`
(correto no IEEE, obrigatório), **não** `Math.pow(d, 0.5)` (que cairia na fronteira do `pow`, Parte 92); e o exp é a mesma série da rodada 43.

**Resultado.** `comparar.py`: **IGUAIS — 16 linhas, 14 números bit a bit**; decisão = token 1. A cabeça de atenção inteira é independente de linguagem.

Com isto o GPT mínimo está traduzido de ponta a ponta: o embedding e a decisão do próximo caractere (rodada 43), a cabeça de atenção causal (61), o passo de treino com SGD (58) e com Adam (59). Em todos, a fronteira é o transcendental
(exp/log/pow), e a estrutura — atenção, causalidade, softmax, argmax, gradiente — é portável bit a bit. A próxima pendência (`dialogo/PENDENCIAS.md`): empilhar camadas (a conexão residual e a normalização) e ver se a fronteira continua sendo só o exp.

## Fontes

- WordNet 3.0, Princeton (`dados/`); OpenWordNet-PT (CC BY 4.0).
- Carl Jung, base psicológica desde a Parte 6.
- Controle ótimo linear-quadrático (LQR) e a equação algébrica de Riccati discreta (DARE): R. E. Kalman (1960); qualquer texto de controle ótimo. Resolvida aqui por iteração de ponto fixo, em biblioteca padrão.
- Regressão por mínimos quadrados com base de características ampliada (viés de forma vs. variância): teoria estatística clássica.
- Atenção causal (softmax sobre q·k/√d): Vaswani et al., "Attention Is All You Need" (2017); aqui em Python puro, com o exp próprio e traduzida bit a bit para Java.
