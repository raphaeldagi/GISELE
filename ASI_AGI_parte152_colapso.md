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

## Medido (P3209; rodada 100)

| mundo | medido (desvio entre sementes) | geometria | colapso | medido / colapso | veredito |
|---|---|---|---|---|---|
| (a) letras uniformes | 0,00405 (0,00188) | 0,00393 | 0,00415 | 0,976 | ✅ |
| (b) grade 3 × 3 | 0,03115 (0,00574) | 0,02873 | 0,02896 | 1,076 | ✅ (a 0,00015 do teto) |
| (c) grade 7 × 7 | 0,02150 (0,00411) | 0,02036 | 0,02099 | 1,024 | ✅ |
| (d) 3 a 6 letras | 0,02150 (0,00530) | 0,02059 | 0,02142 | 1,004 | ✅ |
| (e) WordNet 4 a 5 | **0,00945** (0,00327) | 0,00825 | 0,00824 | 1,147 | ❌ (0,00005 acima do teto) |

- **(f)** média das razões: **1,0453**, fora de [0,959; 1,041]. ❌
- **(g)** a mesma média: 1,0453 em [0,945; 1,055]. ✅
- **(h)** o lote novo de (e), sementes 201 a 240: 0,0085 (razão 1,032). ✅
- **Rodada 100:** IGUAL, 10 linhas e 424 números bit a bit. ✅

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ❌ (f) ❌ (g) ✅ (h) ✅

**Mundo: 6 de 8.** **Sobre mim:** 2 erros, em [0; 3]: ✅. Nenhuma surpresa (os dois erros são menores que as larguras).

### Os dois erros
- **(e) era cauda.** O lote novo de 40 sementes deu razão 1,032; as 60 juntas, 0,00882 (razão 1,070). A regra "lote novo antes de mecanismo" (Partes 117,
  137, 148, 149) evitou de novo uma explicação: eu já tinha notado que as razões do tabuleiro inglês ficam altas (1,111, 1,061, 1,147) e estava a um passo
  de dar a isso um nome.
- **(f) foi o lapso de procedência:** a faixa saiu de cabeça (ruído "≈ 5%" para mundos com 4% a 11%) e errou por 0,004; a versão por código, (g), acertou com
  folga. É a regra da Parte 63 ("estimativa de cabeça no texto é previsão: trocar por código antes do commit"), escrita há 89 partes e desobedecida.

### O que o colapso mostrou
Com os 15 casos (10 antigos e 5 novos), a razão medido / colapso tem média **1,009** e desvio 0,060, contra 1,028 da geometria nos 10 antigos. A conta do
colapso, sem nenhum parâmetro ajustado, prevê o braço aleatório em 15 combinações de dicionário, tabuleiro, grade e comprimento, e o que sobra é do tamanho do
ruído de medida (χ² = 14,8 nos 10 antigos). A lei da densidade da Parte 150 ficou inteira explicada: a constante é geometria (a chance de parar) mais o colapso
(as letras repetidas viram uma ação só).

**Onde o campo médio deveria errar e não errou muito:** a grade 3 × 3 (razão 1,076, a maior entre os mundos novos não-cauda), onde quase toda vizinha já foi vista
antes. O sinal é o esperado (uma vizinha já vista tem a mesma letra, e o colapso real é maior que o sorteado), mas um caso não fixa um sinal (Parte 64).

## Engenharia reversa
- **O padrão: a regra que eu mais cito é a que eu deixo de aplicar quando a conta "parece fácil".** A faixa de (f) era uma média de cinco razões, uma conta
  de duas linhas, e eu a fiz de cabeça porque parecia evidente. As Partes 63, 69 e 114 gravaram a mesma regra; o custo foi um erro em 8.
- **Regra (Parte 152):** antes do commit de um registro, toda faixa tem a linha de código que a calcula (no texto, ou numa pNN). "Parece fácil" não é exceção.
  Auditoria simples: no registro, cada faixa diz de que código saiu.
- **A rodada 100.** Cem rodadas do diálogo, todas IGUAIS no fim (algumas depois de corrigir a ordem das somas ou a libm). A lista da fronteira continua a mesma
  das Partes 52 a 106: exp, log, pow e as trigonométricas em faixa larga, mais a ORDEM das somas. Nesta rodada, a pow de expoente inteiro foi trocada por
  multiplicação repetida antes de rodar, e a soma da programação dinâmica foi tirada do dicionário para uma matriz de ordem fixa: as duas armadilhas conhecidas,
  evitadas antes, e a rodada passou na primeira tentativa.

## Funções e testes
- **Funções:** `p3209_aleatorio_colapso` e `_parte_152`; em `synthai/tabuleiro.py`, `_distintas`, `tabela_colapso`, `assinaturas` e `aleatorio_colapso`. Entrada
  P3209 na regressão.
- **Diálogo:** `dialogo/rodada100.py` e `dialogo/Rodada100.java`, IGUAL.
- **Testes:** `synthai/testes_parte152.py`.

**O placar (m):** m1 = 8 em [7; 9] ✅, m2 = 0 em [0; 0] ✅, m3 = 0,092 em [0,07; 0,12] ✅, m4 = 0,75 em [0,7143; 1,0000] ✅, m5 = 0 ✅ e m6 = 0 ✅. **6 de 6.**

➡ Anterior: [Parte 151](ASI_AGI_parte151_geometria_do_acaso.md).
