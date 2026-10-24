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
