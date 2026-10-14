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
| (m1) | [4; 8] | XX | XX |
| (m2) | [0; 3] | XX | XX |
| (m3) | [0,05; 0,80] | XX | XX |
| (m4) | [0,45; 1,00] | XX | XX |
| (m5) | [0; 3] | XX | XX |
| (m6) | [0; 3] | XX | XX |

## As respostas (quatro camadas)

PLACEHOLDER_RESPOSTAS

## Placar do mundo desta parte

PLACAR_94_TEXTO

## Engenharia reversa (metacognição)

PLACEHOLDER_ENG

## Síntese / unificação

PLACEHOLDER_SINTESE

## Meta

PLACEHOLDER_META

## Diálogo Python ↔ Java

PLACEHOLDER_DIALOGO

## Fontes

- WordNet 3.0, Princeton (`dados/`); OpenWordNet-PT (CC BY 4.0).
- Carl Jung, base psicológica desde a Parte 6.
- Controle ótimo linear-quadrático (LQR) e a equação algébrica de Riccati discreta (DARE): R. E. Kalman (1960); qualquer texto de controle ótimo. Resolvida aqui por iteração de ponto fixo, em biblioteca padrão.
- Regressão por mínimos quadrados com base de características ampliada (viés de forma vs. variância): teoria estatística clássica.
- Atenção causal (softmax sobre q·k/√d): Vaswani et al., "Attention Is All You Need" (2017); aqui em Python puro, com o exp próprio e traduzida bit a bit para Java.
