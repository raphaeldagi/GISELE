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

### P2681 / P2682 — Resolver o jogo é aritmética; e maxmin = minmax

**Na pergunta.** "Soma zero" já diz que o ganho de um é a perda do outro — o que define um único número, o **valor**, que os dois concordam em disputar. O teorema de von Neumann garante que ele existe.

**Lógica.** O valor pela ótica da **linha** (maxmin: a linha joga a mistura que maximiza o seu pior caso) é **0,1428571**; pela ótica da **coluna** (minmax) é **0,1428571** — |diferença| = **2,2e−16 < 1e−12** ✅. A dualidade de von Neumann vale numericamente. E resolver o jogo (fórmula fechada + jogo fictício) usa só +, −, ×, ÷, argmax e comparações — rodada 75 **IGUAL** bit a bit ✅: resolver um jogo, como planejar (Parte 107), não cria fronteira.

**Tradução cruzada.** O minimax é o blefe da Parte 105 generalizado: lá o equilíbrio era indiferença entre blefar e desistir; aqui é a mistura que iguala o pior caso em todas as colunas do adversário. A robustez por indiferença (Parte 105) é um caso particular do minimax (Parte 108).

### P2683 — O valor e a estratégia

**Lógica.** A = [[1, −1], [−2, 3]], sem sela. Denominador a+d−b−c = 1+3+1+2 = **7**. Valor v = (ad − bc)/7 = (3 − 2)/7 = **1/7 = 0,142857** ✅; estratégia de linha p = (d − c)/7 = (3+2)/7 = **5/7 = 0,714286** ✅ (e de coluna q = (d − b)/7 = 4/7). A linha joga a ação 0 em 5 de 7 vezes.

**Meta.** Tudo fechado e exato — a mesma procedência (conta fechada) que sustenta a calibração desde a Parte 94. Os números 1/7 e 5/7 são deste jogo; a forma (v = det/traço-cruzado) é geral para 2×2 sem sela.

### P2684 — Aprender jogando converge para o valor

**Lógica.** O **jogo fictício** (cada jogador responde à frequência histórica do outro) estima o valor em **0,14321** após 2000 iterações — |erro| = **0,00036 < 0,02** ✅. Robinson (1951) provou que a média converge ao valor de qualquer jogo finito de soma zero, sem resolver a LP: é aprender por repetição até o equilíbrio.

**Tradução cruzada.** É a ponte entre as duas almas da SYNTHAI: o cálculo exato (a fórmula fechada) e o aprendizado por tentativa (o jogo fictício). Os dois chegam ao mesmo valor — o aprendizado não descobre nada que a conta não dê, mas chega lá sem precisar da forma do jogo (a autopoiese da Parte 31: substituir aprendizado por conta exata quando a conta existe; o jogo fictício é o controle que mostra que ambos convergem).

### P2685 — O jogo com sela colapsa para o puro (controle)

**Lógica.** A = [[3, 1], [2, 0]] tem **ponto de sela** em (0,1) = 1 (maxmin = minmax = 1 na mesma célula): valor **1** exato, estratégia **pura** (linha 0 sempre, p = 1) ✅. O solver de mistura degenera corretamente para o puro — o controle do outro lado do mecanismo (quando não há o que misturar).

**Meta.** O par teste/controle (sem sela → mistura 5/7; com sela → pura 1) é a régua da Parte 30/75: um verificador só vale com um caso de cada lado. O minimax contém o puro como caso degenerado.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅. Parte 108: **5 testes, 0 erros**. Acumulado (mundo): **219 erros em 805 testes**. Sobre o meu código (p1092): 0 de 5 pNN novas sem teste ✅. Calibração: o acerto das Partes 80–108 é **130/146 = 0,890** — o platô ~0,88 ultrapassado, sustentado por três 5/5 seguidos (106, 107, 108) de conta fechada.

### Previsões sobre previsões (m)

| | faixa | medido | |
|---|---|---|---|
| (m1) | [4; 7] | 5 | ✅ |
| (m2) | [0; 3] | 3 | ✅ |
| (m3) | [0; 0,60] | 0,00 | ✅ |
| (m4) | [0,55; 1,00] | 1,00 | ✅ |
| (m5) | [0; 2] | 0 | ✅ |
| (m6) | [0; 2] | 0 | ✅ |

Previsões sobre previsões (p1499): **6 de 6** dentro da faixa.

## Engenharia reversa (metacognição)

O padrão desta parte é a CONVERGÊNCIA de três fios que vinham separados: o equilíbrio de indiferença (Parte 105), a planejamento por valor (Parte 107) e o aprendizado por repetição (a autopoiese da Parte 31) são, no minimax, o MESMO objeto visto de três ângulos — e os três dão 1/7. Significado (Parte 41): quando partes distintas do projeto convergem no mesmo número por caminhos independentes (fórmula fechada, dualidade maxmin/minmax, jogo fictício), isso não é redundância — é a prova cruzada que a régua da Parte 20 pede (nunca um módulo aprovado só pela própria métrica). O jogo fictício como CONTROLE do cálculo exato (os dois batem em 1/7) é a forma mais limpa disso: o aprendizado não precisa estar certo sozinho, precisa concordar com a conta. Previ 5/5 e acertei 5/5 — a terceira parte seguida de conta fechada exata; o risco que eu marquei (a convergência lenta do jogo fictício em (d)) não se materializou porque o erro caiu como ~1/n, não ~1/√n, num jogo 2×2.

## Síntese / unificação

A Parte 108 resolve o equilíbrio de um jogo de soma zero pelo teorema minimax de von Neumann (`synthai/minimax.py`), fechando o arco de decisão das Partes 104–108. Três caminhos independentes dão o mesmo valor 1/7: a fórmula fechada (v = det/traço-cruzado), a dualidade medida (maxmin = minmax, |dif| 2e−16) e o jogo fictício (aprender jogando converge a 0,1432, erro 0,0004). O minimax generaliza o blefe da Parte 105 (indiferença é o minimax de um jogo polarizado) e usa o jogo fictício como ponte entre o cálculo exato e o aprendizado (a autopoiese da Parte 31: os dois concordam). Controle com ponto de sela (valor 1, estratégia pura) do outro lado do mecanismo. Rodada 75: resolver o jogo é +,−,×,÷,argmax — IGUAL bit a bit (19 rodadas), a fronteira é a aritmética, nunca a dinâmica (cálculo, planejamento, jogo). 5/5 do mundo, calibração 0,890 — o platê ultrapassado por três 5/5 seguidos.

## Meta

Confiança alta: (b), (c), (e) são teorema/forma fechada exata; (a) é mecânica; (d) é a única com erro amostral e caiu bem dentro da faixa (0,0004 contra o limite 0,02) porque num 2×2 o jogo fictício converge rápido. Onde o modelo é brinquedo: 2×2; jogos maiores (n×m) precisariam de um simplex ou LP de verdade — o jogo fictício escala (converge em qualquer jogo finito), mas devagar, e a fórmula fechada não. Fica como limite conhecido. O que não mudou: nenhuma rede, nenhuma auto-replicação (Partes 84/93/102/103). O loop segue (Parte 109 agendada): um jogo n×m por simplex próprio, ou cruzar o minimax com o dicionário-como-números.

## Diálogo Python ↔ Java (rodada 75)

**Rodada 75 (Parte 108): o minimax, bit a bit.** A IA-Python resolve o jogo de soma zero: a fórmula fechada do valor e das estratégias (v = (ad−bc)/(a+d−b−c), p, q) e o jogo fictício (melhor-resposta por argmax do ganho histórico + média corrente). Resolver o jogo acrescenta fronteira?

**IA-Java (ASI):** Não. O valor é razão de somas; a melhor-resposta é um argmax; o jogo fictício acumula e compara. Só +, −, ×, ÷, argmax e comparações — nenhuma transcendental.

**Resultado.** `comparar.py`: **IGUAIS, 5 linhas e 4 números bit a bit** (valor 1/7, p 5/7, q 4/7, fictício 500 it). A terceira família de decisão (cálculo, planejamento, jogo) atravessa as línguas sem perda — 19 rodadas. Pendência (rodada 76): um jogo n×m por simplex próprio — o pivô (divisão pelo elemento-pivô escolhido pela razão mínima) acrescenta fronteira, ou continua +−×÷ e comparação?
