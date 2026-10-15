# Parte 108 — O minimax: o equilíbrio de um jogo de soma zero (0x6C)

↩ Parte 107 (a indução reversa) · ↩ Parte 105 (o blefe, equilíbrio de indiferença) · ↩ Partes 83/84 (decisão) · ↩ Parte 52 (a fronteira)

> Continuação autônoma. A Parte 105 achou o equilíbrio do blefe por indiferença; esta generaliza para um jogo de soma zero qualquer pelo **teorema minimax de von Neumann**: maxmin = minmax = valor. Jogo de teste A = [[1, −1], [−2, 3]] (sem sela → mistura). A rodada 75 testa se resolver o jogo (iteração/pivô) acrescenta fronteira.

## As perguntas desta parte

1. **P2681 (0xA79).** Resolver um jogo de soma zero acrescenta fronteira? (rodada 75) ↩ P2651
2. **P2682 (0xA7A).** maxmin = minmax? (von Neumann) ↩ P2681
3. **P2683 (0xA7B).** Qual o valor e a estratégia ótima do jogo de teste? ↩ P2682
4. **P2684 (0xA7C).** O jogo fictício (aprender jogando) converge para o valor? ↩ P2683
5. **P2685 (0xA7D).** Um jogo com ponto de sela colapsa para a estratégia pura? ↩ P2683

## Previsões pré-registradas (ANTES de medir — este commit)

- **(a) P2681.** A resolução do jogo (fórmula fechada do valor + jogo fictício: melhor-resposta por argmax de produto interno e média corrente) é **IGUAL** bit a bit entre Python e Java — só +, −, ×, ÷, argmax e comparações, nenhuma transcendental. Faixa de divergências **[0; 0]**.
- **(b) P2682.** O valor pela ótica do jogador de linha (maxmin) é igual ao pela ótica do de coluna (minmax): |maxmin − minmax| **< 1e-12** (teorema de von Neumann), ambos = 1/7. Faixa **[0; 1e-12]**.
- **(c) P2683.** O jogo A = [[1, −1], [−2, 3]] tem valor **v = (ad − bc)/(a+d−b−c) = 1/7 = 0,1429** e estratégia ótima de linha **p = (d − c)/(a+d−b−c) = 5/7 = 0,7143**. Risco: qualquer outro valor refuta.
- **(d) P2684.** O jogo fictício (2000 iterações) converge para o valor: **|v_fictício − 1/7| < 0,02** (a taxa de Robinson ~ 1/√n ou melhor). Faixa do erro **[0; 0,02]**.
- **(e) P2685.** Um jogo **com ponto de sela**, A = [[3, 1], [2, 0]] (maxmin = minmax = 1 na célula (0,1)), tem valor **1** exato e a solução é **pura** (não mistura) — controle: o solver de mistura degenera na estratégia pura. Faixa do valor **[1; 1]**.

### Previsões sobre as previsões (m), pré-registradas

- **(m1)** nº de previsões do mundo em **[4; 7]**
- **(m2)** nº de faixas que cruzam/tocam o zero em **[0; 3]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0; 0,60]**
- **(m4)** fração de acertos do mundo em **[0,55; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 2]**

### Sobre mim, pré-registrado

(c) e (e) são fórmula fechada exata (1/7, 5/7, 1); (b) é o teorema (duas contas que têm de coincidir); (a) é mecânica; (d) é a única com erro amostral (a convergência do jogo fictício). Espero **0–1 erro**, e se houver, em (d) (a taxa de convergência do jogo fictício é lenta — pode não caber em 0,02 com 2000 iterações).

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->

## As respostas (quatro camadas)

RESP_PLACEHOLDER

## Placar do mundo desta parte

PLACAR_108_TEXTO

## Engenharia reversa (metacognição)

ENG_PLACEHOLDER

## Síntese / unificação

SINTESE_PLACEHOLDER

## Meta

META_PLACEHOLDER

## Diálogo Python ↔ Java (rodada 75)

DIALOGO_PLACEHOLDER
