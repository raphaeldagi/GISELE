# Parte 148 — A GRPO no jogo de palavras com o dicionário GRANDE, e o passo dela bit a bit

↩ Nasce da Parte 147 (a GRPO de `rl_grupos.py` no jogo de `word_rl_lab`, com as 1.400 palavras embutidas) e da Parte 111 (o data lake: os
77.340 lemas do WordNet multiplicaram o aleatório por 6,2). A pergunta: com um dicionário 55 vezes maior, o que muda entre a GRPO e o Q-learning?

## O recolhimento do contêiner, 6º lote
Este despertar (00h07) veio depois de cerca de 60 minutos de ociosidade, e o contêiner estava "up 0 min", como a hipótese previa (up < 5 min).
São 6 lotes, todos com a condição escrita desde a Parte 145.

## O caso mínimo, rodado antes (regra da Parte 84)
Calibração com as sementes 5 a 12 (8 mundos, regra da Parte 138), 5.000 episódios, avaliação de 1.000, os 77.340 lemas:

| semente | Q | aleatório | GRPO G = 2 | sem contraste G = 2 | GRPO G = 8 | sem contraste G = 8 |
|---|---|---|---|---|---|---|
| 5 | 0,320 | 0,041 | 0,392 | 0,9120 | 0,426 | 0,7168 |
| 6 | 0,339 | 0,053 | 0,391 | 0,9140 | 0,405 | 0,7184 |
| 7 | 0,323 | 0,054 | 0,417 | 0,9080 | 0,392 | 0,7184 |
| 8 | 0,354 | 0,043 | 0,393 | 0,9204 | 0,407 | 0,7136 |
| 9 | 0,300 | 0,047 | 0,364 | 0,9124 | 0,411 | 0,7200 |
| 10 | 0,316 | 0,053 | 0,373 | 0,9060 | 0,401 | 0,7360 |
| 11 | 0,320 | 0,040 | 0,432 | 0,9192 | 0,408 | 0,7104 |
| 12 | 0,322 | 0,043 | 0,392 | 0,9220 | 0,379 | 0,7248 |

**O mecanismo, escrito antes:** com o dicionário grande, mais caminhos são palavras, então mais grupos têm contraste (sem contraste com G = 8 cai
de 0,94 na Parte 147 para 0,72). A GRPO aprende só com os grupos com contraste, e eles passam de 6% para 28% dos grupos com G = 8: a vantagem
da GRPO sobre o Q-learning deve crescer (na calibração, G = 2 − Q = +0,070, contra +0,048 na Parte 147).

**O teste:** sementes 61 a 70 (10 mundos, nenhuma usada antes nesta comparação), o mesmo desenho, a média das 10.

## Previsões, registradas antes de qualquer execução do caso de teste
A meia-largura de cada média é 1,645 · 1,36 · √(σ²/8 + σ²/10), com σ o desvio entre as 8 sementes da calibração: o erro do centro (Parte 123)
mais o da medida, vezes o fator da Parte 79. Contas em `scratchpad/p148/faixas.py`, depois em `p3199`.

**Procedência:** todas de calibração, inclusive as frações sem contraste (regra da Parte 147: o p delas depende do aprendizado), menos (j), que
é uma contagem com P(todas) escrita. O centro de "quantos erros" é 9 × 0,25 + 1 × 0,015 = 2,3.

- **(a)** Q-learning, média das 10 sementes, em **[0,3072; 0,3413]**
- **(b)** aleatório em **[0,0406; 0,0529]**
- **(c)** GRPO com G = 2 em **[0,3711; 0,4174]**
- **(d)** fração sem contraste com G = 2 em **[0,9081; 0,9204]**
- **(e)** GRPO com G = 8 em **[0,3890; 0,4183]**
- **(f)** fração sem contraste com G = 8 em **[0,7115; 0,7281]**
- **(g)** G = 2 − Q em **[0,0452; 0,0948]**
- **(h)** G = 8 − Q em **[0,0563; 0,1024]**
- **(i)** G = 8 − G = 2 em **[−0,0196; 0,0383]**. Cruza o zero: P(G = 8 > G = 2) = Φ(0,0094/0,0129) = 0,77 < 0,9, então registro a diferença, não a
  ordem (Parte 145).
- **(j)** nº de sementes, em 10, em que as DUAS GRPO superam o Q-learning em **[10; 10]**. Por semente, P(G = 2 > Q) = Φ(0,070/0,0234) = 0,9986 e
  P(G = 8 > Q) = Φ(0,079/0,0217) = 0,9999; P(uma) ≈ 0,9985 e P(todas) = 0,9985¹⁰ = 0,985 ≥ 0,90 (regra da Parte 121).

### A rodada 96, registrada antes
O passo da GRPO de `synthai/grpo_palavras.py` num jogo de palavras de brinquedo (alfabeto {a, b, c}, até 3 letras, 5 palavras): softmax
tabular por prefixo com o exp PRÓPRIO, vantagem com √, a atualização REINFORCE, 40 grupos de G = 4. Só usa + − × ÷, √ e o exp próprio; o
dicionário de logits só endereça (a ordem de iteração não entra em nenhuma soma). Previsão: **IGUAL**.

### Previsões sobre as previsões (m), registradas (régua: P2837)
A régua rodou sobre o rascunho com uma linha "Do mundo:" provisória (regra da Parte 120): m1 = 10, m2 = 1, m3 = 0,053, m5 = 0. Cada erro gera um
lote novo (Parte 122), então m1 vai a [10; 10 + E] com E = 2,3. A fração de acertos vai como contagem (regra da Parte 147): 6 a 10 acertos em 10.
- **(m1)** nº de previsões do mundo em **[10; 12]**
- **(m2)** nº que cruzam ou tocam o zero em **[1; 2]**
- **(m3)** mediana de w em **[0,04; 0,07]**
- **(m4)** fração de acertos em **[0,60; 1,00]** (6 a 10 de 10)
- **(m5)** nº com w > 0,6 em **[0; 0]**
- **(m6)** surpresas em **[0; 1]**

### Sobre mim, registrado
Erros no mundo em **[0; 4]**, com centro 2,3 (binomial de 9 faixas a 0,25: desvio 1,3).

➡ Anterior: [Parte 147](ASI_AGI_parte147_grpo_palavras.md).

## Um lote novo antes de qualquer mecanismo (registrado depois de ver o teste, antes de rodar as sementes 71 a 80)
O teste (sementes 61 a 70) já rodou, e o Q-learning ficou abaixo do piso de (a): 0,3020 contra [0,3072; 0,3413]. O t de Welch entre as 10 sementes
de teste e as 8 de calibração é −2,33. Antes de procurar um mecanismo (regra das Partes 25 e 117), um lote novo, com o centro e o desvio das 18
sementes juntas (média 0,3119, desvio 0,0234):
- **(k)** Q-learning, média das sementes 71 a 80, em **[0,2912; 0,3325]**: 1,645 · 1,36 · √(0,0234²/18 + 0,0234²/10).
- **(l)** desvio do Q-learning entre as sementes 71 a 80 em **[0,0142; 0,0321]**: σ · √(χ²₉/9) com os quantis 5% e 95% do χ² de 9 graus (3,325 e
  16,919), σ = 0,0234. A forma é fechada se o desvio de 18 sementes for o σ verdadeiro, o que não é (o fator de 18 sementes não entra aqui).

**Medido no lote 71 a 80:** Q-learning 0,3035 (k ✅) e desvio 0,0172 (l ✅). O lote ficou de novo abaixo da média da calibração (0,3242): agora
são 20 sementes de teste contra 8 de calibração, t = −2,95. Lotes depois do que disparou, do mesmo lado: 1 de 1 (P = 0,5 ao acaso). A largura
passou; falta um caminho independente (regra da Parte 143). As sementes da calibração (5 a 12) são pequenas e vizinhas; as de teste, grandes.
Se o número da semente não importa, um lote de sementes PEQUENAS novas (13 a 22) cai na média das 28:
- **(n)** Q-learning, média das sementes 13 a 22, em **[0,2913; 0,3265]**: média 0,3089 e desvio 0,0214 das 28, 1,645 · 1,36 · √(σ²/28 + σ²/10).
  Se as sementes pequenas fossem diferentes de verdade, o lote ficaria perto de 0,324, acima do teto.
