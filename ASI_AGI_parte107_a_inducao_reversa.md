# Parte 107 — A indução reversa: o equilíbrio de duas ruas, e a recursão que não cria fronteira (0x6B)

↩ Parte 106 (a segunda rua) · ↩ Partes 83/84/93 (decisão, planejamento, VOI) · ↩ Parte 52 (a fronteira)

> Continuação autônoma. A Parte 106 deu o valor de duas ruas por contagem; esta resolve a árvore de decisão **de trás para frente** (indução reversa / Bellman): o valor de uma decisão agora inclui o valor da decisão que ela desbloqueia depois. A rodada 74 testa se a **recursão entre as ruas** acrescenta fronteira. Toy MDP exato (sem simulação): estados A, B; ações 0, 1; r(A,0)=1, r(A,1)=0→B; r(B,0)=0→A, r(B,1)=3→B.

## As perguntas desta parte

1. **P2651 (0xA5B).** A indução reversa (resolver a árvore de trás para frente) acrescenta fronteira? (rodada 74) ↩ P2595
2. **P2652 (0xA5C).** Qual o valor ótimo de duas decisões a partir de A? ↩ P2651
3. **P2653 (0xA5D).** A indução reversa bate o guloso (míope) — e quando empata? ↩ P2652
4. **P2654 (0xA5E).** Quanto a segunda decisão acrescenta à primeira? ↩ P2653
5. **P2655 (0xA5F).** Quanto vale saber o estado oculto (qual MDP)? ↩ P2563

## Previsões pré-registradas (ANTES de medir — este commit)

- **(a) P2651.** A indução reversa (iteração de valor, horizonte 2: V₁(s) = maxₐ r, V₂(s) = maxₐ [r + V₁(T)]) é **IGUAL** bit a bit entre Python e Java — só +, −, max e comparações, nenhuma transcendental. A recursão sobre a árvore **não** cria fronteira (como o MPC, Parte 93). Faixa de divergências **[0; 0]**.
- **(b) P2652.** O valor ótimo de duas decisões a partir de A é **V₂(A) = 3** exato (tomar a ação 1 primeiro — recompensa 0 agora — para chegar a B, que vale 3). Risco: qualquer outro inteiro refuta.
- **(c) P2653.** A indução reversa (3) **bate** o guloso/míope (que toma a recompensa imediata 1 e fica em A, somando 2): razão **1,5**. Num MDP de controle **separável por estágio** (recompensa futura independente da ação) a indução reversa **empata** com o guloso (razão **1,0**). Faixa da razão no MDP do teste **[1,5; 1,5]**.
- **(d) P2654.** A segunda decisão acrescenta **V₂(A) − V₁(A) = 3 − 1 = 2** (o payoff adiado que a primeira decisão desbloqueia). Risco: ≠ 2 refuta.
- **(e) P2655.** O valor de **saber** o estado oculto (qual de dois MDPs espelhados, crença 0,5) é **VOI ≥ 0**, e **> 0** quando os dois MDPs preferem primeiras ações diferentes; controle: dois MDPs **idênticos** → VOI = **0** exato. Faixa do VOI no caso espelhado **[0,3; 1,2]**.

### Previsões sobre as previsões (m), pré-registradas

- **(m1)** nº de previsões do mundo em **[4; 7]**
- **(m2)** nº de faixas que cruzam/tocam o zero em **[0; 2]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0; 0,60]**
- **(m4)** fração de acertos do mundo em **[0,55; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 2]**

### Sobre mim, pré-registrado

Quatro das cinco são conta fechada exata de DP (V₂=3, razão 1,5, diferença 2, VOI=0 no controle); a quinta (IGUAL bit a bit) é mecânica. O risco está em (e) (a faixa do VOI no caso espelhado, que depende da forma exata do MDP espelho). Espero **0–1 erro**.

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->

## As respostas (quatro camadas)

RESP_PLACEHOLDER

## Placar do mundo desta parte

PLACAR_107_TEXTO

## Engenharia reversa (metacognição)

ENG_PLACEHOLDER

## Síntese / unificação

SINTESE_PLACEHOLDER

## Meta

META_PLACEHOLDER

## Diálogo Python ↔ Java (rodada 74)

DIALOGO_PLACEHOLDER
