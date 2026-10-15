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

### P2651 — A recursão entre ruas não cria fronteira

**Na pergunta.** "Indução reversa" já diz o método: resolve-se de trás para frente. A pergunta herdada da rodada 73 é se essa recursão — um valor que chama o valor seguinte — acrescenta fronteira entre as línguas.

**Lógica.** A iteração de valor V[h][s] = maxₐ (r(s,a) + V[h−1][T(s,a)]) usa só somas, `max` e comparações. Rodada 74: **IGUAIS, 3 linhas e 4 números bit a bit** (V₁(A)=1, V₂(A)=3) ✅. A recursão é dinâmica (o estado futuro realimenta o presente), mas a **aritmética** é +/max — e a fronteira é sempre a aritmética transcendental, nunca a dinâmica (a lição das Partes 90/93 reafirmada no 18º round).

**Tradução cruzada.** A indução reversa é a SynthaiPlanejadora (P182/P93) feita exata: onde o MPC amostrava trajetórias, a árvore pequena permite resolver o ótimo por programação dinâmica. Planejar é compor valores — e compor +/max não sai da aritmética portável.

### P2652 / P2654 — O valor de olhar adiante

**Lógica.** A partir de A, a indução reversa escolhe a ação 1 (recompensa **0** agora) para alcançar B, que vale 3 — total **V₂(A) = 3** ✅. A segunda decisão acrescenta V₂(A) − V₁(A) = 3 − 1 = **2** ✅: o payoff adiado que a primeira decisão desbloqueia. Sem olhar adiante (horizonte 1) o melhor de A é só 1.

**Tradução cruzada.** É a definição operacional de "futuro": a diferença entre o valor com e sem a decisão seguinte. Uma ASI que planeja n passos ganha exatamente o que os passos extras desbloqueiam — aqui, dobrar o horizonte triplicou o valor (1 → 3), porque o prêmio (B) só é alcançável por uma ação que parece ruim agora.

### P2653 — Quando planejar vale (o regime)

**Lógica.** No MDP do teste a indução reversa (3) **bate** o guloso/míope (2): razão **1,5** ✅. Num MDP **separável** (T(s,a)=s: a ação de agora não muda o estado futuro) os dois **empatam**: razão **1,0** ✅. Planejar só paga quando a ação de agora tem **consequência de estado** — exatamente o regime do MPC (Parte 93) e do Global Workspace (Parte 102): integrar/planejar cria valor só onde a estrutura (futuro/informação repartida) exige.

**Meta.** É a terceira vez que o mesmo formato de regime aparece (MPC P93, workspace P102, agora planejamento P107): a vantagem de um método "mais esperto" é proporcional a quanto a tarefa precisa do que o método vê. O guloso não é pior em geral — é pior só onde o futuro depende da ação.

### P2655 — Quanto vale saber o estado oculto

**Lógica.** Com dois MDPs **espelhos** (as ações trocadas, de modo que preferem primeiras ações opostas) e crença 0,5, o valor de **saber** qual é o MDP menos o de só **crer** é **VOI = 0,5 > 0** ✅ (∈ [0,3; 1,2]). Com dois MDPs **idênticos** (controle), saber não acrescenta nada: **VOI = 0** exato ✅.

**Tradução cruzada (Partes 83/84).** Fecha o arco das Partes 104–107: o valor da informação oculta, que começou como "ver a carta" (6/13), agora é o valor de saber **qual jogo** se está jogando — e vale exatamente quando o conhecimento mudaria a primeira ação. Informação sobre a regra do mundo vale como informação sobre uma carta: na proporção em que muda a decisão.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅. Parte 107: **5 testes, 0 erros**. Acumulado (mundo): **219 erros em 800 testes**. Sobre o meu código (p1092): 0 de 5 pNN novas sem teste ✅. Calibração: o acerto das Partes 80–107 é **125/141 = 0,886**. Dois 5/5 seguidos (106, 107) com conta fechada exata; a calibração sobe de volta rumo ao platô ~0,88.

### Previsões sobre previsões (m)

| | faixa | medido | |
|---|---|---|---|
| (m1) | [4; 7] | 5 | ✅ |
| (m2) | [0; 2] | 0 | ✅ |
| (m3) | [0; 0,60] | 0,30 | ✅ |
| (m4) | [0,55; 1,00] | 1,00 | ✅ |
| (m5) | [0; 2] | 0 | ✅ |
| (m6) | [0; 2] | 0 | ✅ |

Previsões sobre previsões (p1499): **6 de 6** dentro da faixa.

## Engenharia reversa (metacognição)

O padrão desta parte é o reaparecimento de uma FORMA: pela terceira vez (MPC na 93, workspace na 102, planejamento na 107) a vantagem de um método mais esperto é um REGIME, não um sempre — e desta vez eu previ isso de antemão (o controle separável com razão 1,0 estava pré-registrado), em vez de descobri-lo medindo. Significado (Parte 41): depois de muitas partes encontrando "o efeito só vale no regime X", a forma virou uma EXPECTATIVA que eu testo com um controle construído para o não-efeito — e acertar o não-efeito (razão 1,0 no separável) é tão informativo quanto o efeito (1,5 no teste). É a lição das Partes 87/89 (prever o não-efeito) aplicada a um terceiro domínio. A recursão (indução reversa) não criar fronteira também era previsível pela lição das Partes 90/93 (a fronteira é a aritmética, não a dinâmica) — e previ sem medir antes.

## Síntese / unificação

A Parte 107 resolve a árvore de decisão de duas ruas por INDUÇÃO REVERSA (Bellman) exata, `synthai/duas_ruas.py` — a SynthaiPlanejadora (P182/P93) feita exata por programação dinâmica num toy MDP. Quatro resultados de conta fechada: (1) olhar adiante vale V₂(A)−V₁(A) = 2 (o payoff adiado que a primeira decisão desbloqueia; horizonte 1→2 leva o valor de 1 a 3); (2) a indução reversa bate o guloso (razão 1,5) só quando a ação tem consequência de estado — num MDP separável empatam (1,0): o terceiro aparecimento do regime MPC/workspace, agora PREVISTO com controle; (3) o valor de saber o estado oculto (qual MDP) é 0,5 no caso espelho e 0 no idêntico — o VOI das Partes 83/84 estendido de "ver a carta" para "saber o jogo". Rodada 74: a recursão entre ruas é +/max, IGUAL bit a bit (18 rodadas) — a fronteira é a aritmética, nunca a dinâmica. 5/5 do mundo, calibração 0,886.

## Meta

Confiança alta: quatro previsões são DP exato (V₂=3, razão 1,5/1,0, diferença 2, VOI=0 no controle), e a quinta é mecânica (IGUAL). O VOI do caso espelho (0,5) caiu dentro da faixa [0,3; 1,2] que eu dei exatamente porque não tinha derivado o número à mão — a faixa larga foi honesta sobre a minha incerteza. Onde o modelo é um brinquedo: o MDP tem 2 estados e 2 ações; a conclusão de regime (planejar vale só com consequência de estado) é geral, mas os NÚMEROS (1,5, 2, 0,5) são deste MDP e não se estendem. O que não mudou: nenhuma rede, nenhuma auto-replicação (Partes 84/93/102/103). O loop segue (Parte 108 agendada).

## Diálogo Python ↔ Java (rodada 74)

**Rodada 74 (Parte 107): a indução reversa, bit a bit.** A IA-Python resolve a árvore de trás para frente: V[0]=0; V[h][s] = maxₐ (r(s,a) + V[h−1][T(s,a)]). A pendência da rodada 73: a recursão entre as ruas acrescenta fronteira?

**IA-Java (ASI):** Não. O valor futuro realimenta o presente — a dinâmica é recursiva —, mas cada passo é só soma, `max` e comparação. A fronteira é a aritmética transcendental (exp/log/pow, sin em faixa larga), nunca a dinâmica.

**Resultado.** `comparar.py`: **IGUAIS, 3 linhas e 4 números bit a bit** (V₁(A)=1, V₂(A)=3). A programação dinâmica atravessa as línguas sem perda — 18 rodadas. Pendência (rodada 75): a resolução de um jogo de soma zero por programação linear (o equilíbrio por minimax) — o pivô do simplex acrescenta fronteira, ou continua +−×÷ e comparação?

---

→ Continua na **[Parte 108 — O minimax: o equilíbrio de um jogo de soma zero](ASI_AGI_parte108_o_minimax.md)** (pré-registro das previsões).
