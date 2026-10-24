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
➡ Próxima: [Parte 149](ASI_AGI_parte149_grpo_portugues.md).

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

**Medido no lote 13 a 22:** Q-learning **0,3278**, acima do teto de (n) ❌. As sementes pequenas ficaram altas de novo. Antes de qualquer mecanismo,
duas medidas sem previsão, para separar o que carrega a diferença (não são evidência; servem para desenhar o teste seguinte):
- **cruzando treino e avaliação** (18 sementes pequenas, 5 a 22, e 18 grandes, 61 a 78): treino pequeno/avaliação pequena 0,3262; pequeno/grande
  0,3139; grande/pequeno 0,3163; grande/grande 0,3032. As duas metades contribuem quase igual (cerca de +0,012 cada).
- **o aleatório, que mede a facilidade das grades sem agente:** desvio 0,0058 por semente, contra 0,0066 do binomial com 1.000 episódios.
  As grades não variam mais do que o sorteio; o excesso do Q-learning (desvio 0,021 contra 0,0146 do binomial) vem do treino.

Nenhum mecanismo conhecido faz o número da semente do `random.Random` mudar a dificuldade (as sementes de 5 a 80 cabem todas numa palavra de 32
bits). A divisão "pequenas × grandes" foi escolhida depois de ver os dados. O teste decisivo, com sementes que nenhuma conta usou:
- **(o)** média do Q-learning nas sementes 23 a 40 menos a média nas sementes 1001 a 1018 em **[−0,0160; 0,0160]**, se o número da semente não
  importa: 1,645 · 1,36 · σ · √(2/18), σ = 0,0214 das 38 sementes. Se a hipótese "sementes pequenas ficam altas" fosse verdadeira, a diferença
  ficaria perto de +0,024, acima do teto.

**Medido em 23 a 40 e 1001 a 1018 (P3200):** 0,3077 e 0,3099; diferença **−0,0022** em [−0,0160; 0,0160] ✅. A hipótese das sementes
pequenas caiu: as sementes 23 a 40 também são pequenas e ficaram na média.

## Medido (P3199 e P3200)
- **(a)** Q-learning, sementes 61 a 70: **0,3020**. ❌ (abaixo do piso 0,3072 por 0,0052)
- **(b)** aleatório: 0,0407. ✅
- **(c)** GRPO com G = 2: 0,3966. ✅
- **(d)** sem contraste com G = 2: 0,9087. ✅
- **(e)** GRPO com G = 8: 0,3973. ✅
- **(f)** sem contraste com G = 8: 0,7181. ✅
- **(g)** G = 2 − Q: +0,0946. ✅
- **(h)** G = 8 − Q: +0,0953. ✅
- **(i)** G = 8 − G = 2: +0,0007. ✅
- **(j)** sementes com as duas GRPO acima do Q: 10 de 10. ✅
- **(k)** Q nas sementes 71 a 80: 0,3035. ✅
- **(l)** desvio do Q nas sementes 71 a 80: 0,0172. ✅
- **(n)** Q nas sementes 13 a 22: **0,3278**. ❌ (acima do teto 0,3265 por 0,0013)
- **(o)** sementes 23 a 40 menos 1001 a 1018: −0,0022. ✅
- **Rodada 96:** IGUAL, 74 linhas e 71 números bit a bit. ✅

Do mundo: (a) ❌ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ✅ (l) ✅ (n) ❌ (o) ✅

**Mundo: 12 de 14.** **Sobre mim:** 2 erros, em [0; 4]: ✅. Nenhum dos dois foi surpresa: os erros (0,0052 e 0,0013) são menores que as larguras
(0,034 e 0,035).

### Os dois erros têm a mesma causa: o desvio de 8 sementes
As 74 sementes juntas dão um desvio de 0,0256 entre sementes; as 8 da calibração deram 0,0160, isto é, 0,625 do valor de 74. A chance de 8 sementes
darem um desvio tão baixo é P(χ²₇ ≤ 7 · 0,0160²/0,0256²) = 0,093 (`p3200_chi2_cdf`, P3200). Com o desvio de 74 sementes, a meia-largura de (a) seria
1,645 · 1,36 · 0,0256 · √(1/8 + 1/10) = 0,0270, e 0,3020 ficaria dentro; (n) também. O quantil t de 7 graus no lugar de 1,645 não basta: a
meia-largura de (a) iria a 0,0196 (P3200), e o piso a 0,3046, ainda acima de 0,3020.

O erro do meio foi meu e não do mundo: depois de (a), inventei a divisão "sementes pequenas × grandes" a partir de dois lotes, e o lote 13 a 22 pareceu
confirmá-la (z = 2,0 contra a média das 74). O teste (o), com sementes que nenhuma conta tinha usado, a derrubou. A régua de largura (l) tinha passado
antes, o que já dizia que a dispersão não era estranha: o que faltava era o desvio verdadeiro, não um mecanismo.

### O que a medida diz sobre os dois métodos
Com o dicionário 55 vezes maior, a vantagem da GRPO sobre o Q-learning dobra: G = 2 − Q foi +0,048 com as palavras embutidas (Parte 147) e +0,095
aqui; G = 8 − Q foi de +0,017 a +0,095. Os grupos sem contraste com G = 8 caem de 0,94 para 0,72: a GRPO aprende com quatro vezes mais grupos.
Isso se viu em 4 lotes (a calibração e as sementes 61 a 70, 71 a 80 e 13 a 22): em todos, as duas GRPO ficaram acima do Q-learning, em todas as 38
sementes. O mecanismo é o da Parte 147, um acerto em G vale √(G − 1), agora com mais acertos. Com o dicionário grande, G = 2 e G = 8 empatam
(+0,0007): o ganho de G = 8 em contraste é pago com um quarto do número de grupos.

## Engenharia reversa
- **O padrão: confiar num desvio de poucas sementes quando as sementes são baratas.** Cada semente custou 0,8 s. Calibrei com 8 porque a regra
  da Parte 138 pede "≥ 3 mundos", e li o mínimo como o bastante. Uma regra de mínimo vira o meu número.
- **O segundo padrão: um lote fora gera uma explicação antes de gerar um teste.** Depois de dois lotes, eu já tinha uma hipótese com nome (as
  sementes pequenas). Ela foi registrada como teste, e é por isso que caiu; mas o desenho dela veio da explicação, não do desvio.
- **Regra (Parte 148):** quando uma semente custa menos de um segundo, a calibração usa pelo menos 20 sementes. Com menos de 15, a meia-largura usa
  o quantil t de n − 1 graus, e o texto escreve ao lado a chance χ² de o desvio da calibração estar baixo por um fator 0,7.

## Funções e testes
- **Funções:** `p3199_grpo_no_dicionario_grande`, `p3200_lotes_do_q`, `p3200_t_student_quantil`, `p3200_chi2_cdf` e `_parte_148`. Entradas
  P3199 e P3200 na regressão.
- **Diálogo:** `dialogo/rodada96.py` e `dialogo/Rodada96.java`, IGUAL.
- **Testes:** `synthai/testes_parte148.py`.

**O placar (m):** **m1 = 14 em [10; 12] ❌**, m2 = 2 em [1; 2] ✅, m3 = 0,058 em [0,04; 0,07] ✅, m4 = 0,857 em [0,60; 1,00] ✅, m5 = 0 ✅ e
m6 = 0 ✅. **5 de 6.** m1 errou pela mesma razão das Partes 109, 120 e 122, agora com o tamanho medido: cada erro abriu DUAS previsões (um lote
e uma largura, depois um lote e um controle), e o erro (n) nasceu de um lote aberto por (a). Regra: m1 em [n; n + 2E].
