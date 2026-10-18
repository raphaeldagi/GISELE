# Parte 113 — O arrependimento: CFR no pôquer de Kuhn, o teste forte do repertório e o leitor v4 (0x71)

↩ Parte 112 (o Kuhn completo pelo simplex) · ↩ Parte 108 (o jogo fictício: aprender jogando) · ↩ Parte 111 (o estimador de confiança) · ↩ Parte 110 (os expoentes sobrescritos que o leitor não lê)

> Continuação ("Continue sem parar"), com as três pendências que a Parte 112 abriu (`dialogo/PENDENCIAS.md`, rodada 80):
> - **(1) CFR, o Kuhn sem a forma normal.** O simplex da 112 montou a matriz 27×64; o pôquer real explode nessa forma. O CFR (Counterfactual Regret Minimization, Zinkevich et al. 2007) aprende jogando contra si mesmo, conjunto de informação por conjunto de informação, e a estratégia MÉDIA converge para um equilíbrio (`synthai/cfr.py`, determinístico, as 6 distribuições enumeradas).
> - **(2) O teste FORTE da hipótese do repertório (transferência).**
> - **(3) O leitor das minhas previsões, v4, com expoentes sobrescritos.**
>
> **A calibração, rodada ANTES deste registro, em casos que não são o teste:**
> - **CFR em T = 100, 200, 400 e 800 iterações.** A explorabilidade da estratégia média foi 0,0466 / 0,0239 / 0,0222 / 0,0161, com inclinação log-log **−0,47** (t = −4,03, então |t| > 2: a regra da Parte 71 permite extrapolar). A extrapolação para T = 10.000 dá 0,0047. Nas mesmas iterações, α = P(o jogador 1 blefa com o valete) ficou em 0,21 / 0,19 / 0,21 / 0,22, dentro da família de Kuhn e longe dos vértices; e os erros das marginais caíram com oscilação (de 0,10 a 0,003).
> - **A transferência nas sementes 7, 8 e 9.** A AUC das válidas VISTAS (o repertório) contra as inválidas foi 0,89 / 0,79 / 0,68; a das válidas NOVAS, 0,60 / 0,73 / 0,59.
> - **O leitor v4 na Parte 110 (onde conheço os casos).** Recupera (c), (h) e (i), os três de expoente sobrescrito. E o controle: a v4 com o leitor de números VELHO é idêntica à v3.

## As perguntas desta parte

1. **P2831 (0xB0F).** O CFR converge para o equilíbrio de Kuhn sem a forma normal? Com que velocidade, e que explorabilidade deixa em T = 10.000? ↩ P2801
2. **P2832 (0xB10).** Que equilíbrio da família o CFR escolhe? O simplex parou num vértice (α = 1/3); o CFR, que faz MÉDIA, também? ↩ P2803
3. **P2835 (0xB13).** O estimador de confiança treinado no repertório do agente TRANSFERE para palavras que o agente nunca formou? ↩ P2810
4. **P2833/P2834 (0xB11/0xB12).** Quantas faixas o leitor v4 recupera? ↩ P2806
5. **P2836 (0xB14).** O CFR acrescenta fronteira entre Python e Java? (rodada 80) ↩ P2805

## Previsões pré-registradas (ANTES de medir — este commit)

**As fixtures (regra da Parte 111).**
- CFR vanilla, simultâneo, com arrependimento e soma da estratégia acumulados por conjunto de informação, `CFR().iterar(10000)`.
- A transferência roda nas sementes **42 a 51** (dez sementes novas), com `transferencia_do_estimador(Config(seed=s), embutido)`: 5.000 episódios de treino; teste com 5.000 episódios de uma política aleatória em grades da semente + 200.000.
- O leitor compara a v3 (P2806) com a v4 (P2833) nas Partes 53 a 112.

**CFR (P2831/P2832), T = 10.000.**
- **(a)** Explorabilidade da estratégia média: centro 0,0047 pela extrapolação. A meia-largura em log é 1,645 × √(0,41² + 0,2²) × 1,36 ≈ 1,0, um fator de ~2,8 para cada lado: **[0,0017; 0,013]**. Mecanismo esperado (a faixa passa de duas ordens? não, mas é larga): a cota O(1/√T) do arrependimento médio.
- **(b)** |valor da estratégia média − (−1/18)|: **[0; 0,013]**. Identidade: o valor do perfil e o do equilíbrio estão ambos entre as duas melhores respostas, então a distância entre eles é ≤ explorabilidade; o teto é o da faixa (a).
- **(c)** |P(o jogador 2 paga com a dama) − 1/3|: **[0; 0,03]** (a calibração caiu de 0,10 a 0,003; a escala 1/√T dá ~0,01).
- **(d)** |P(o jogador 2 blefa com o valete) − 1/3|: **[0; 0,03]**.
- **(e)** α = P(o jogador 1 aposta com o valete): **[0,15; 0,30]**. Mecanismo esperado: o CFR faz MÉDIA de estratégias, e a média de pontos da família é um ponto INTERIOR. Ao contrário do simplex, que anda de vértice em vértice e parou em α = 1/3.
- **(f)** |P(aposta | rei) − 3α|: **[0; 0,03]**.
- **(g)** |P(o jogador 1 passa e paga | dama) − (α + 1/3)|: **[0; 0,03]**.

**Transferência (P2835), média sobre as sementes 42 a 51.**
- **(h)** AUC das válidas NOVAS: calibração 0,643, desvio entre sementes 0,075, faixa 0,643 ± 1,645 × 0,075/√10 × 1,36 = **[0,59; 0,70]**. Acima de 0,5: as letras levam ALGUMA regularidade que transfere.
- **(i)** AUC(vistas) − AUC(novas), média das sementes que têm vistas: calibração 0,143, desvio 0,124, faixa **[0,055; 0,23]**. Acima de 0: o repertório acrescenta além disso. A hipótese da Parte 111 fica PARCIAL: repertório e regularidade, os dois.

**Leitor v4 (P2834), Partes 53 a 112.**
- **(j)** Faixas recuperadas: as 3 da 110, mais as que existirem com sobrescrito em outras partes, **[3; 8]**.
- **(k)** Faixas perdidas: **[0; 0]**. Identidade: o `_numero_pt_v2` delega ao original em qualquer texto sem expoente sobrescrito, e o original devolve None em qualquer texto com expoente sobrescrito; então nenhum número que a v3 lia muda nem some.
- **(l)** Faixas trocadas: **[0; 0]**, pela mesma identidade.

**Diálogo (P2836).**
- **(n)** O CFR em `float`, T = 1.000 (as 24 probabilidades médias), é **IGUAL** bit a bit entre Python e Java: **[0; 0]**. Identidade: só +, −, ×, ÷ e comparações (o max(0, ·) do casamento de arrependimento é uma comparação), na mesma ordem de recursão e de soma nas duas línguas.

### Previsões sobre as previsões (m), pré-registradas (régua: o leitor v4, P2833)

- **(m1)** nº de previsões do mundo em **[12; 16]** (13 agora + ~2 por surpresa)
- **(m2)** nº de faixas que cruzam/tocam o zero em **[6; 10]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0,20; 0,70]**
- **(m4)** fração de acertos do mundo em **[0,60; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 4]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 3]**

### Sobre mim, pré-registrado

Os riscos estão onde a calibração é ruidosa. As marginais (c), (d), (f), (g) oscilam e não caem de forma monótona. (e) aposta que o CFR para no interior. (h)/(i) têm de 8 a 42 positivos por semente. (j) é uma contagem sobre partes que não reli. As identidades (b), (k), (l) e (n) têm a garantia escrita. Espero **1 a 3 erros**, nas marginais ou em (i).

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->
