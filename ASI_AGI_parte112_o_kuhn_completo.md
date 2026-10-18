# Parte 112 — O simplex próprio e o pôquer de Kuhn completo; o leitor das minhas previsões, corrigido (0x70)

↩ Parte 108 (o minimax 2×2) · ↩ Parte 109 (o Kuhn simplificado do NEXUS, −1/12) · ↩ Parte 105 (o blefe, equilíbrio de indiferença) · ↩ Parte 111 (o estimador de confiança e a hipótese do repertório) · ↩ Parte 110 (o defeito do leitor `p1481`)

> Continuação autônoma, com as pendências adiadas quatro vezes (`dialogo/PENDENCIAS.md`):
> - **O simplex n×m próprio.** `synthai/simplex.py`: um único código sobre `Fraction` (exato) e `float` (para o diálogo), com a regra de Bland.
> - **O pôquer de Kuhn COMPLETO.** O jogador 2 também escolhe entre passar e apostar. Em forma normal, são 27 estratégias puras do jogador 1 × 64 do jogador 2, resolvidas pelo simplex.
> - **O leitor das minhas previsões** (`p1481`, defeito medido na Parte 110).
> - **A hipótese do repertório** (Parte 111).
>
> **Uma correção ANTES de prever: o diagnóstico da Parte 110 estava errado.** A Parte 110 escreveu que a `p1481` "perde faixas de itens com rótulo em negrito". Olhando o caso, o defeito é outro: o texto "log(erro) contra **log(h)**", dentro do item (a) da Parte 110, contém "(h)". A `p1481` casa QUALQUER "(x)" como rótulo de letra, e por isso deu à (h) a faixa da (a). É o padrão das Partes 109 e 111 uma terceira vez: a MENÇÃO de uma letra lida como o USO de um rótulo. A `p2806_minhas_previsoes_v3` (nova; a `p1481` fica intacta) só aceita rótulos no INÍCIO de uma linha.
>
> **O que já rodou antes deste commit (controles, sem tocar nas quantidades previstas):**
> - O simplex no jogo 2×2 da Parte 108, cujo valor já estava publicado: 1/7, p = (5/7, 2/7), q = (4/7, 3/7); com o ponto de sela, valor 1 e estratégia pura.
> - A v3 contra a v2 nas Partes 60, 80, 100 e 108 (a calibração da regra da Parte 75, escolhida por uma regra escrita antes de olhar: os múltiplos de 20, mais a 108): **0** diferenças nas quatro.
> - A hipótese do repertório nas sementes 7, 8 e 9 (calibração; o teste é a 42). Razão Brier do estimador treinado sobre as palavras de uma política ALEATÓRIA: 1,047 / 1,048 / 1,057 com tudo, e 1,099 / 1,094 / 1,111 só com as letras.

## As perguntas desta parte

1. **P2801 (0xAF1).** Qual o valor do pôquer de Kuhn completo para o jogador 1, resolvido pelo simplex próprio? ↩ P2713
2. **P2802 (0xAF2).** O equilíbrio do jogador 2 é o de Kuhn (único): pagar com a dama 1/3 das vezes e blefar com o valete 1/3? ↩ P2801
3. **P2803 (0xAF3).** O jogador 1 cai na família de um parâmetro de Kuhn: apostar o rei = 3 × blefar o valete, e pagar com a dama = α + 1/3? ↩ P2802
4. **P2804 (0xAF4).** O simplex em ponto flutuante concorda com o exato? A dualidade (maxmin = minmax) vale no exato? ↩ P2681
5. **P2805 (0xAF5).** O pivô do simplex acrescenta fronteira entre Python e Java? (rodada 79) ↩ P2776
6. **P2806/P2807 (0xAF6/0xAF7).** Quantas faixas a v3 do leitor recupera, perde e troca nas Partes 53 a 111? ↩ P1481
7. **P2808 (0xAF8).** O estimador de confiança treinado sobre uma política SEM repertório (aleatória) ainda bate a linha de base? ↩ P2773

## Previsões pré-registradas (ANTES de medir — este commit)

**A fixture do jogo aleatório (regra da Parte 111: a fixture vai no commit do registro).** Uma matriz 4×5 com as entradas (x mod 11) − 5, onde x percorre o LCG x ← (1103515245·x + 12345) mod 2³¹, a partir de x = 112, linha por linha.

- **(a) P2801** O valor do Kuhn completo para o jogador 1: **−1/18 = −0,05556**. Faixa **[−0,05556; −0,05555]**. Identidade: o teorema de Kuhn (1950), e o simplex é exato sobre `Fraction`.
- **(b) P2802** P(o jogador 2 paga | dama, diante de aposta) = **1/3**. Faixa **[0,3333; 0,3334]**. Identidade: o equilíbrio do jogador 2 é único (Kuhn), e qualquer equilíbrio que o simplex devolva tem essas marginais.
- **(c) P2802** P(o jogador 2 aposta | valete, diante de passe), o blefe: **1/3**. Faixa **[0,3333; 0,3334]**, pela mesma identidade.
- **(d) P2803** |P(aposta | rei) − 3·P(aposta | valete)| do jogador 1: **[0; 0]**. Identidade: em toda a família de equilíbrios do jogador 1, apostar o rei é 3α e blefar o valete é α.
- **(e) P2803** α = P(o jogador 1 aposta | valete): **[0; 0,3334]**, a família α ∈ [0, 1/3]. Qual α o simplex escolhe depende da regra de Bland; o mecanismo esperado é um vértice da família, α = 0 ou α = 1/3.
- **(f) P2803** |P(o jogador 1 passa-e-paga | dama) − (α + 1/3)|: **[0; 0]**. Identidade: a mesma família (com a dama, o jogador 1 nunca aposta, e paga com α + 1/3).
- **(g) P2804** No jogo 4×5 da fixture, |valor em float − valor exato|: **[0; 10⁻¹²]**. O mecanismo esperado é uma dezena de pivôs, cada um errando ~10⁻¹⁶ em termos relativos; a faixa tem quatro ordens de folga e não é identidade.
- **(h) P2804** No mesmo jogo, no exato, a lacuna de dualidade max_i (Aq)_i − min_j (pA)_j: **[0; 0]**. Identidade: dualidade forte da programação linear, em aritmética exata.
- **(i) P2807** Faixas que a v3 RECUPERA (None na v2, lida na v3), nas Partes 53 a 111: centro 4 (109 (i); 110 (a); 111 (n) e (o), contadas à mão sobre o defeito diagnosticado). Faixa **[4; 8]**.
- **(j) P2807** Faixas que a v3 PERDE (lidas na v2): **[0; 3]**. A calibração deu 0 em quatro partes de três épocas de formato.
- **(k) P2807** Faixas TROCADAS (as duas leem, diferentes): **[1; 3]**. O centro é 1, a 110 (h), a faixa roubada da (a).
- **(l) P2808** Semente 42, razão Brier do estimador completo sob a política aleatória: média 1,051 e desvio 0,0055 → **[1,039; 1,063]**. O mecanismo esperado, a hipótese do repertório: sem hábito do agente, o estimador não tem o que aprender e o ruído da regressão online o põe acima da base.
- **(n) P2808** O mesmo, só com as letras: média 1,101 e desvio 0,0088 → **[1,081; 1,121]**.
- **(o) P2805** O simplex em `float` no jogo 4×5 da fixture (valor, p, q, pivôs) é **IGUAL** bit a bit entre Python e Java: divergências **[0; 0]**. Identidade: a regra de Bland é determinística e só usa +, −, ×, ÷ e comparações (IEEE nas duas línguas), na mesma ordem.

### Previsões sobre as previsões (m), pré-registradas

- **(m1)** nº de previsões do mundo em **[13; 17]** (14 agora + ~2 por surpresa esperada)
- **(m2)** nº de faixas que cruzam/tocam o zero em **[5; 9]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0; 0,30]**
- **(m4)** fração de acertos do mundo em **[0,60; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 3]**

### Sobre mim, pré-registrado

Seis faixas são identidades com a sua garantia escrita ao lado ((a), (b), (c), (d), (f), (h)), mais a (o). Os riscos:
- (e), qual vértice o simplex escolhe;
- (i)–(k), a contagem do leitor sobre 59 partes que eu não reli;
- (l)/(n), 3 pontos de calibração;
- o modelo de Kuhn em si. Se eu escrevi as regras do jogo errado, (a) a (f) caem juntas, e isso é UM erro de modelagem que se espalha. A conta feita à mão de um caso (P1 com o rei aposta e P2 com o valete desiste: +1) confere as regras de aposta e desistência.

Espero **1 a 3 erros**.

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->
