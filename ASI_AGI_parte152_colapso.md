# Parte 152 — O colapso das vizinhas de mesma letra, em conta

↩ Nasce da Parte 151 (a geometria exata do braço aleatório acertou os mundos novos, mas a razão medido/geometria ia de 0,89 a 1,14) e da sua pendência 1.

## O recolhimento do contêiner, 10º lote
Despertar às 05h53, depois de cerca de 55 minutos ociosa: "up 0 min", como previsto. Dez lotes a favor.

## A conta do colapso
O `valid_actions` da Parte 111 guarda as ações num dicionário por LETRA: duas vizinhas livres com a mesma letra viram uma ação só. Com n vizinhas livres de
letras sorteadas independentes com as frequências p, seja K o número de letras distintas entre elas. O braço aleatório escolhe uniforme entre as K letras e o
PARAR, então:
- P(parar | n) = E[1/(K + 1)];
- P(próxima letra = c | n) = E[1{c presente}/(K + 1)] (sem o PARAR, antes de 3 letras: /K).

A distribuição de K, e a de K junto com "c presente", saem EXATAS de uma programação dinâmica sobre as 26 letras, com o peso multinomial
n!·Π p_i^{m_i}/m_i! (`synthai/tabuleiro.py`, `_distintas`, `tabela_colapso`). Com n = 8 vizinhas e as letras do inglês, P(parar) = 0,137, contra 1/9 = 0,111
sem colapso: o colapso faz o braço parar mais cedo, e D₃ pesa mais.

**O que ainda é aproximação** (campo médio): as letras das vizinhas de cada decisão entram como sorteios novos, mas uma vizinha livre já vista na decisão
anterior reaparece com a MESMA letra; e o `setdefault` fica com a primeira casa de cada letra (na ordem (−1, −1), …, (1, 1)), o que puxa o caminho para um lado.
Os caminhos geométricos são agrupados pela sequência dos números de vizinhas livres (315 assinaturas na grade 5 × 5), com os pesos exatos de cada casa.

**Controle:** com um alfabeto de duas letras e um dicionário com TODAS as palavras de 3 a 5 letras, a conta dá 1,0000000000000000: a probabilidade total fecha.

## Contra os 10 casos já medidos (posteriores; regra da Parte 25)

| caso | geometria (151) | colapso | medido | medido / geometria | medido / colapso |
|---|---|---|---|---|---|
| embutido / inglês | 0,0079 | 0,0081 | 0,0090 | 1,137 | 1,111 |
| português / inglês | 0,0132 | 0,0137 | 0,0136 | 1,033 | 0,990 |
| WordNet / inglês | 0,0387 | 0,0409 | 0,0434 | 1,121 | 1,061 |
| português / português | 0,0222 | 0,0227 | 0,0224 | 1,008 | 0,983 |
| WordNet / português | 0,0434 | 0,0465 | 0,0465 | 1,071 | 1,001 |
| embutido / português | 0,0065 | 0,0069 | 0,0062 | 0,956 | 0,901 |
| português / português, 4 × 4 | 0,0239 | 0,0244 | 0,0251 | 1,048 | 1,027 |
| português / português, 6 × 6 | 0,0211 | 0,0217 | 0,0204 | 0,967 | 0,940 |
| português / português, máximo 4 | 0,0351 | 0,0339 | 0,0368 | 1,048 | 1,085 |
| português / português, mínimo 4 | 0,0078 | 0,0076 | 0,0070 | 0,892 | 0,920 |

Razão média: geometria 1,028 (desvio 0,075); colapso **1,002** (desvio 0,070). O colapso tira o viés médio, não o espalhamento. Mas o espalhamento é do
tamanho do RUÍDO DE MEDIDA: cada medido é uma média de 10 a 40 sementes de 1.000 episódios, com desvio binomial relativo de 3,3% a 12,7%. Contra esse ruído,
χ² = Σ ((razão − 1)/desvio)² = 14,8 com 10 graus de liberdade (p ≈ 0,14). O que sobra para o erro do modelo é √(0,00442 − 0,00397) = 0,021.

## Previsões em cinco mundos novos, registradas antes de rodar (sementes 181 a 200, só o braço aleatório)
Centro = a conta do colapso, sem nenhum fator ajustado. Meia-largura 1,645 · √(binomial/20 + (0,021 · 1,36 · centro)²): o ruído de medida mais o erro do
modelo, este vezes o fator da Parte 79 (ele foi estimado de 10 casos). Procedência: conta (campo médio) com um erro de modelo calibrado.
- **(a)** português num tabuleiro de letras UNIFORMES: em **[0,0034; 0,0049]** (centro 0,00415; geometria sem colapso 0,00393)
- **(b)** português / português, grade 3 × 3: em **[0,0266; 0,0313]** (centro 0,02896). A grade pequena é onde o campo médio mais erra: das 8 casas que
  cercam uma, quase todas já foram vistas.
- **(c)** português / português, grade 7 × 7: em **[0,0190; 0,0229]** (centro 0,02099)
- **(d)** português / português, de 3 a 6 letras: em **[0,0195; 0,0234]** (centro 0,02142)
- **(e)** WordNet / inglês, de 4 a 5 letras: em **[0,0071; 0,0094]** (centro 0,00824)
- **(f)** a média das cinco razões medido / colapso em **[0,959; 1,041]**: ruído relativo médio de cada mundo ≈ 5%, dividido por √5, mais 1% de modelo.
- **(g)** a mesma média de (f), com a faixa calculada por código (o ruído relativo de cada mundo é 11%, 4,1%, 4,8%, 4,8% e 7,8%; o desvio da média é 0,0312; o
  erro de modelo, 0,021 · 1,36/√5 = 0,0128): em **[0,945; 1,055]**.

**Lapso registrado antes de rodar:** a faixa de (f) saiu de uma estimativa de cabeça ("≈ 5%", regra da Parte 63 desobedecida); o mundo uniforme tem 11%. (f) fica
como foi registrada e conta no placar; (g) é a versão por código, registrada antes de qualquer execução dos mundos novos.

### Previsões sobre as previsões (m), registradas (régua: P2837)
A régua sobre o rascunho com "Do mundo:" provisória: m1 = 7, m2 = 0, m3 = 0,091, m5 = 0. As 7 são de conta com erro calibrado: E = 7 × 0,10 = 0,7; m1 em
[7; 7 + 2E] = [7; 8]. (f) e (g) medem a mesma coisa e erram juntas ou acertam juntas, salvo se a média cair entre 1,041 e 1,055 (ou entre 0,945 e 0,959).
Acertos como contagem: 5 a 7 das 7 (5/7 = 0,7143).
- **(m1)** nº de previsões do mundo em **[7; 9]**
- **(m2)** nº que cruzam ou tocam o zero em **[0; 0]**
- **(m3)** mediana de w em **[0,07; 0,12]**
- **(m4)** fração de acertos em **[0,7143; 1,0000]**
- **(m5)** nº com w > 0,6 em **[0; 0]**
- **(m6)** surpresas em **[0; 1]**

### Sobre mim, registrado
Erros no mundo em **[0; 3]**, centro 0,7.

## Um lote novo depois de (e), registrado antes de rodar (WordNet / inglês, 4 a 5 letras, sementes 201 a 240)
Os cinco mundos rodaram (resultado em "Medido"); (e) ficou 0,00005 acima do teto, com razão medido/colapso 1,147, z ≈ 1,8 contra o ruído binomial e o erro do
modelo juntos. Antes de qualquer mecanismo (Partes 117 e 148), 40 sementes novas, o mesmo centro:
- **(h)** aleatório, WordNet / inglês, 4 a 5 letras, média das sementes 201 a 240, em **[0,0074; 0,0091]**: 1,645 · √(binomial/40 + (0,021 · 1,36 · 0,00824)²).

### A rodada 100, registrada antes (a centésima)
A tabela do colapso traduzida: a programação dinâmica sobre as 26 letras (estados (sorteios usados, distintas) numa matriz percorrida na ordem fixa t, k
crescentes, em vez do dicionário do módulo), o peso multinomial com p^m por MULTIPLICAÇÃO REPETIDA (a `**` do módulo é a pow da libm; expoente inteiro sai
portável assim, regra da Parte 92) e m! exato; P(parar | n) e P(c | n) com e sem PARAR para n = 1..8, com as letras do inglês. Só + × ÷. Previsão: **IGUAL**.
O que poderia quebrar: a ordem das somas dentro da programação dinâmica (os dois lados percorrem a matriz na mesma ordem).
