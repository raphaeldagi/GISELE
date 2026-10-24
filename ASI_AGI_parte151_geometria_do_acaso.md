# Parte 151 — A constante da lei da densidade vem da geometria da grade; e o repertório do Q-learning

↩ Nasce da Parte 150 (a lei da densidade, aleatório ≈ 0,21·D, com a constante ajustada) e das suas duas pendências.

## O recolhimento do contêiner, 9º lote
Despertar às 04h31, depois de cerca de 55 minutos ociosa: "up 0 min", como previsto. Nove lotes a favor.

## A constante, deduzida (sem ajuste)
`synthai/tabuleiro.py`, `paradas_por_comprimento`: a enumeração EXATA dos caminhos do braço aleatório na grade 5 × 5 com vizinhança de rei. Começa numa casa
uniforme; em cada casa escolhe uniforme entre as vizinhas não visitadas e o PARAR (que só existe com 3 letras ou mais); com 5 letras, só PARAR; sem ação,
falha. O resultado é a chance de parar com L letras:

s₃ = 0,1940, s₄ = 0,1685, s₅ = 0,6375 (soma 1, sem falhas: com 3 letras o PARAR sempre existe).

Se as letras da grade são sorteadas independentes com as frequências p(c), a chance de achar uma palavra é **Σ_L s_L · D_L**, com D_L a densidade das palavras
de L letras. A "constante" 0,21 da Parte 150 é s₃ ponderado: D₃ domina D em todos os dicionários. Contra os 6 casos já medidos (são posteriores, não evidência;
regra da Parte 25):

| caso | geometria Σ s_L D_L | medido | medido / geometria |
|---|---|---|---|
| embutido / inglês | 0,0079 | 0,0090 | 1,137 |
| português / inglês | 0,0132 | 0,0136 | 1,033 |
| WordNet / inglês | 0,0387 | 0,0434 | 1,121 |
| português / português | 0,0222 | 0,0224 | 1,008 |
| WordNet / português | 0,0434 | 0,0465 | 1,071 |
| embutido / português | 0,0065 | 0,0062 | 0,956 |

A razão média é 1,054 (desvio 0,069). A conta ignora o colapso: quando duas vizinhas têm a mesma letra, o `valid_actions` as junta numa ação só, e o PARAR
fica mais provável. Isso empurra o medido para cima da geometria, e é o sinal da média.

## Previsões em mundos novos, registradas antes de qualquer execução (português no tabuleiro português, sementes 161 a 180, só o braço aleatório)
Centro = 1,054 · Σ s_L D_L com a geometria do mundo novo. Meia-largura 1,645 · √(binomial/20 + (0,069 · geometria)²): a razão varia de caso a caso com desvio
0,069, e não é dividida por √6. Procedência: conta (geometria exata) com uma correção calibrada em 6 casos.
- **(a)** grade 4 × 4 (s₃ = 0,2119, s₄ = 0,1870, s₅ = 0,6011): aleatório em **[0,0220; 0,0285]**
- **(b)** grade 6 × 6 (s₃ = 0,1826): aleatório em **[0,0193; 0,0252]**
- **(c)** grade 5 × 5, no máximo 4 letras (s₃ = 0,1940, s₄ = 0,8060): aleatório em **[0,0325; 0,0416]**
- **(d)** grade 5 × 5, no mínimo 4 letras (s₄ = 0,2111, s₅ = 0,7889): aleatório em **[0,0069; 0,0097]**

O que a conta diz que a intuição não diria: a grade maior quase não muda nada (de 4 × 4 para 6 × 6 o centro cai só 12%), e exigir 4 letras divide o acaso por
quase 3. O mecanismo que move o teste (o tamanho da grade, os comprimentos) NÃO está nos 6 casos de calibração, que são todos 5 × 5 de 3 a 5 letras (regra da
Parte 71); a correção 1,054 pode não valer neles.

## O repertório (pendência 1 das Partes 149 e 150)
**A medida (P3208):** nas 1.000 avaliações do Q-learning guloso (cada uma numa grade nova), a fração dos acertos cuja palavra aparece em pelo menos DOIS
episódios: o repertório. Um agente que aprendeu palavras que se repetem de grade em grade tem repertório alto; um que acha palavras novas a cada grade, baixo.

**A calibração (sementes 101 a 120, rodada antes das previsões abaixo):**

| condição | acerto | palavras distintas | repertório |
|---|---|---|---|
| português, tabuleiro inglês | 0,1403 (0,0214) | 32,1 (5,18) | 0,8886 (0,0255) |
| português, tabuleiro português | 0,2867 (0,0319) | 49,9 (6,41) | 0,9323 (0,0143) |
| embutido, tabuleiro inglês | 0,1343 (0,0254) | 23,2 (3,98) | 0,9356 (0,0278) |

(entre parênteses, o desvio entre as 20 sementes)

A leitura da Parte 149 (o embutido tem Q maior que o português com aleatório menor porque as poucas palavras dele se REPETEM) cabe: o embutido acha 23
palavras distintas contra 32 e repete 0,936 contra 0,889. Um cuidado: o repertório cresce mecanicamente com o número de acertos (mais acertos, mais chance de
repetir), e as duas condições inglesas têm acertos parecidos (0,134 e 0,140): a comparação embutido × português é justa nesse ponto. A do tabuleiro
português não é (o dobro de acertos).

## Previsões do repertório, registradas antes de rodar as sementes 121 a 140
O acerto do português nas sementes 121 a 140 já foi medido nas Partes 149 e 150 (mesmas sementes, mesmo procedimento): não entra como previsão. Meia-largura
1,645 · 1,36 · σ · √(1/20 + 1/20). Centro de "quantos erros" nas 13 previsões da parte (contadas pela P2833): 4 de conta com correção calibrada × 0,15 + 9 de calibração × 0,25 = 2,85.
- **(e)** palavras distintas, português no tabuleiro inglês, em **[28,4; 35,8]**
- **(f)** repertório, português no tabuleiro inglês, em **[0,8705; 0,9067]**
- **(g)** palavras distintas, português no tabuleiro português, em **[45,3; 54,4]**
- **(h)** repertório, português no tabuleiro português, em **[0,9222; 0,9424]**
- **(i)** acerto do Q, embutido no tabuleiro inglês, em **[0,1163; 0,1522]**
- **(j)** palavras distintas, embutido, em **[20,4; 26,0]**
- **(k)** repertório, embutido, em **[0,9159; 0,9552]**
- **(l)** repertório do embutido menos o do português (tabuleiro inglês) em **[0,0165; 0,0775]**. P(> 0) = Φ(0,047/0,0136) > 0,999: a faixa não toca o zero.
- **(n)** repertório do português, tabuleiro português menos inglês, em **[0,0245; 0,0629]**

### Previsões sobre as previsões (m), registradas (régua: P2837)
A régua sobre o rascunho com "Do mundo:" provisória: m1 = 13, m2 = 0, m3 = 0,123, m5 = 1 (a (l), w = 0,649). E = 2,85; m1 em [13; 13 + 2E]. Acertos como contagem:
7 a 13 das 13, e a fração exata 7/13 = 0,5385 (regra da Parte 150).
- **(m1)** nº de previsões do mundo em **[13; 19]**
- **(m2)** nº que cruzam ou tocam o zero em **[0; 1]**
- **(m3)** mediana de w em **[0,09; 0,16]**
- **(m4)** fração de acertos em **[0,5385; 1,0000]**
- **(m5)** nº com w > 0,6 em **[1; 2]**
- **(m6)** surpresas em **[0; 1]**

### Sobre mim, registrado
Erros no mundo em **[0; 6]**, centro 2,85 (desvio binomial ≈ 1,5).
