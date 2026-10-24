# Parte 150 — O tabuleiro em português: a densidade de palavras como conta de peso

↩ Nasce da Parte 149 (a GRPO em português, num tabuleiro com as letras do inglês: o tamanho do dicionário não era a variável) e da regra que ela
gravou: um viés nomeado ganha uma conta de peso antes de prever.

## O recolhimento do contêiner, 8º lote
Despertar às 03h11, depois de cerca de 55 minutos ociosa: "up 0 min", como previsto. Oito lotes a favor.

## A conta de peso, antes de qualquer execução com o tabuleiro novo
`synthai/tabuleiro.py`: as frequências das letras contadas nos 34.384 lemas da OpenWordNet-PT (A 13,9%, E 10,3%, O 9,5%, I 9,3%, R 8,6%, contra
E 12,7%, T 9,1%, A 8,2% do inglês), e um gerenciador de contexto que troca o `LETTER_FREQ` do jogo durante o experimento sem editar o módulo.

**A densidade de palavras** D = Σ_w Π_c p(c), sobre as palavras de 3 a 5 letras: a chance de que uma sequência de letras sorteadas com as frequências
do tabuleiro seja uma palavra do dicionário. Ela não sabe nada de vizinhança na grade nem de quando parar; é a conta mais simples que pesa "quantas
palavras cabem".

| dicionário / tabuleiro | D | aleatório medido | aleatório / D |
|---|---|---|---|
| embutido / inglês | 0,0413 | 0,0090 (23 sementes, Parte 149) | 0,218 |
| português / inglês | 0,0656 | 0,0136 (40 sementes, Parte 149) | 0,207 |
| WordNet / inglês | 0,1962 | 0,0434 (18 sementes, Parte 148) | 0,221 |
| **português / português** | **0,1093** | ? | |

A razão aleatório/D é quase constante nos três dicionários (média 0,2155, desvio 0,0072). Foi isso que a Parte 149 não tinha: o aleatório não
segue o tamanho do dicionário (493, 4.181, 9.686 palavras), segue D. O Q-learning segue outra coisa (o embutido tem D menor e Q maior).

## Previsões, registradas antes de qualquer execução com o tabuleiro português (sementes 101 a 120)
**Procedência:** (a) conta (D) com a constante k calibrada em 3 dicionários; (b) e (c) mecanismo, interpolando entre o português e o WordNet no
tabuleiro inglês, pelo ln do aleatório (fração ln(0,0235/0,0136)/ln(0,0434/0,0136) = 0,473).
- **(a)** aleatório, média das 20 sementes, em **[0,0209; 0,0262]**. Centro 0,2155 · 0,1093 = 0,0235. Binomial √(0,0235 · 0,9765/1000)/√20 = 0,0011; erro de
  k, 0,0072/√3 · 0,1093 = 0,0005; vezes 1,645 · 1,36 (k é calibrado).
- **(b)** Q-learning em **[0,17; 0,25]**. A razão Q/aleatório vai de 10,4 (português) a 7,2 (WordNet); interpolada, 8,9; Q = 8,9 · 0,0235 = 0,209.
- **(c)** GRPO G = 2 − Q em **[0,04; 0,11]**. De 0,0615 (português, Parte 149) a 0,0837 (WordNet, Parte 148), interpolado: 0,072.

O que pode quebrar (a): D ignora a vizinhança (uma palavra precisa de letras ADJACENTES) e o PARAR; se o tabuleiro português muda a fração de caminhos
que chegam a 3 letras, k muda. Os três dicionários da calibração usam o mesmo tabuleiro: o caso de calibração NÃO tem o mecanismo que move o teste
(a troca de tabuleiro). Regra da Parte 71: escrito aqui.
