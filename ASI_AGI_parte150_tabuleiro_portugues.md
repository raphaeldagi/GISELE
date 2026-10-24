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

## A calibração no tabuleiro português (sementes 101 a 120, P3205)

| quantidade | média | desvio |
|---|---|---|
| Q-learning | 0,2867 | 0,0319 |
| aleatório | 0,0226 | 0,0043 |
| GRPO G = 2 | 0,3443 | 0,0227 |
| GRPO G = 8 | 0,3552 | 0,0225 |
| sem contraste G = 2 | 0,9451 | 0,0059 |
| sem contraste G = 8 | 0,8169 | 0,0156 |
| G = 2 − Q | 0,0576 | 0,0367 |
| G = 8 − Q | 0,0685 | 0,0408 |
| G = 8 − G = 2 | 0,0110 | 0,0300 |

As duas GRPO acima do Q em 19 de 20 sementes.

**As previsões de mecanismo:** (a) aleatório 0,0226 em [0,0209; 0,0262] ✅ (a densidade previu 0,0235); (b) Q-learning **0,2867**, fora de [0,17; 0,25]
❌; (c) G = 2 − Q = 0,0576 em [0,04; 0,11] ✅. A conta de peso funcionou para o que ela pesa (o aleatório). O Q-learning dobrou (0,142 → 0,287) com o
aleatório subindo 1,7 vez: a razão Q/aleatório subiu (10,4 → 12,7) em vez de cair para 8,9 como a interpolação dizia. A interpolação pegou a tendência
da razão entre DOIS DICIONÁRIOS diferentes e a aplicou à troca de TABULEIRO; são mecanismos diferentes (regra da Parte 12).

## Previsões do teste, registradas antes de rodar as sementes 121 a 140 (e 141 a 150)
Meia-largura 1,645 · 1,36 · σ · √(1/20 + 1/20). Centro de "quantos erros" nas 12 abaixo: 8 de calibração × 0,25 + 2 de forma fechada × 0,10 + 2 de conta
com k calibrado × 0,15 = 2,5.
- **(d)** Q-learning em **[0,2641; 0,3093]**
- **(e)** aleatório em **[0,0202; 0,0250]**: binomial, √(0,0226 · 0,9774/1000) = 0,0047 por semente; 1,645 · √2 · 0,0047/√20.
- **(f)** GRPO G = 2 em **[0,3282; 0,3604]**
- **(g)** sem contraste G = 2 em **[0,9409; 0,9493]**
- **(h)** GRPO G = 8 em **[0,3393; 0,3711]**
- **(i)** sem contraste G = 8 em **[0,8059; 0,8279]**
- **(j)** G = 2 − Q em **[0,0316; 0,0836]**
- **(k)** G = 8 − Q em **[0,0396; 0,0974]**
- **(l)** G = 8 − G = 2 em **[−0,0102; 0,0322]**. Cruza o zero: P(G = 8 > G = 2) = Φ(0,011/0,0134) = 0,79 < 0,9; registro a diferença.
- **(n)** nº de sementes, em 20, com as duas GRPO acima do Q em **[17; 20]**: binomial com p = 19/20, P(17..20) = 0,984.

**A densidade num mundo novo.** Com k = 0,2133 (média dos 4 casos, agora com o português no tabuleiro português; desvio 0,0073), o aleatório de dois
dicionários que ainda não jogaram no tabuleiro português, sementes 141 a 150, só o braço aleatório (P3202):
- **(o)** WordNet no tabuleiro português, D = 0,2200: em **[0,0419; 0,0520]**. Centro 0,0469; binomial /√10 e erro de k /√4, vezes 1,645 · 1,36.
- **(p)** embutido no tabuleiro português, D = 0,0339: em **[0,0053; 0,0092]**. Centro 0,0072.

### Previsões sobre as previsões (m), registradas (régua: P2837)
A régua sobre o rascunho com "Do mundo:" provisória: m1 = 15, m2 = 1, m3 = 0,107, m5 = 0. E ≈ 2,5 nas 12 que faltam; m1 em [15; 15 + 2E].
Acertos como contagem: 9 a 14 das 15.
- **(m1)** nº de previsões do mundo em **[15; 20]**
- **(m2)** nº que cruzam ou tocam o zero em **[1; 2]**
- **(m3)** mediana de w em **[0,08; 0,14]**
- **(m4)** fração de acertos em **[0,60; 0,93]**
- **(m5)** nº com w > 0,6 em **[0; 0]**
- **(m6)** surpresas em **[0; 1]**

### Sobre mim, registrado
Erros no mundo em **[1; 6]**: o (b) já errou; centro 1 + 2,5.

### A rodada 98, registrada antes
A conta de peso de `synthai/tabuleiro.py` traduzida: as frequências de letras de uma lista fixa de 40 palavras portuguesas (A a Z na ordem do
alfabeto, total em laço, piso 0,01) e a densidade D das que têm 3 a 5 letras, mais a mesma D com as frequências do inglês. Só + × ÷ em laço, nenhuma
função transcendental. Previsão: **IGUAL**. O que poderia quebrar: a ordem da soma das frequências (o módulo usa `sum()` de floats, compensado no
Python 3.12; a rodada usa laço, nos dois lados).
