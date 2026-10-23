# Parte 140 — A régua que não lia tabelas, o dicionário como fluxo e os dígitos hexadecimais como vértices

↩ Nasce das Partes 136 a 139: elas registraram previsões em TABELAS, e a régua do placar (`p2833_minhas_previsoes_v4`) não as lê. Nasce
também das regras permanentes da Parte 30 (o dicionário como data lake e, à parte, o hexadecimal) e da Parte 67 (prever o previsto), que
as Partes 136 a 139 deixaram de cumprir.

## O defeito, medido antes de tudo
A P2837 dá m1 = 0 nas Partes 136, 137 e 138. O leitor v4 só lê uma parte que tenha a linha de placar do mundo (as letras com ✅ ou ❌ depois de "Do mundo" e dois-pontos) e faixas
em negrito, entre colchetes, em itens que começam pela letra entre parênteses. (A primeira versão desta frase citava a linha literal, e o
próprio leitor a tomou pelo placar desta parte: menção lida como uso, no meu texto.) Desde a Parte 128, eu escrevo as previsões em tabela. Por isso as previsões das voltas (128 a
135) e das Partes 136 a 138 estão fora da calibração medida da série (P1961 e as que a leem). Além disso, as Partes 136 a 139 não
registraram as previsões sobre previsões (m): é um lapso da regra da Parte 67, e esta parte volta a cumpri-la.

## Perguntas
**O leitor.**
- **(g)** Quantas previsões com veredito um leitor que também lê tabelas recupera nas Partes 128 a 138?
- **(h)** Qual o acerto delas?
- **(i)** Nas partes que a v4 já lia (as que têm a linha de placar do mundo), a v5 muda alguma coisa?

**O dicionário (data lake).** As 117.659 glosas do WordNet 3.0, na ordem do arquivo, como um FLUXO. Uma memória de reservatório de
k = 500 (a `synthai/reservatorio.py` da Parte 137) não sabe o tamanho do fluxo.
- **(a)** O desvio das médias de comprimento das glosas (em palavras), em 300 reservatórios, é o da amostra sem reposição,
  σ/√k·√((N − k)/(N − 1))?
- **(b)** A média das 300 médias é não viesada?
- **(c)** O reservatório é cego à ordem: a fração da amostra que vem da primeira metade do arquivo é ½?

**O hexadecimal** (à parte do dicionário). Os 16 dígitos são os vértices de {0, 1}⁴.
- **(d)** O posto efetivo dos 16 vértices é 4?
- **(e)** O dos 10 dígitos decimais (0 a 9) é o da conta à mão?
- **(f)** O do primeiro dígito hexadecimal de 3ⁿ (n = 1 a 5.000) é o da lei de Benford na base 16, P(d) = log₁₆(1 + 1/d)?

## A conta à mão de (e), escrita antes
Os bits b3, b2, b1 e b0 dos dígitos 0 a 9:
- b3 = 1 em {8, 9}, então p = 0,2;
- b2 = 1 em {4, 5, 6, 7}, p = 0,4;
- b1 = 1 em {2, 3, 6, 7}, p = 0,4;
- b0 = 1 nos ímpares, p = 0,5.

As covariâncias:
- cov(b3, b2) = 0 − 0,2·0,4 = −0,08, e cov(b3, b1) = −0,08;
- cov(b2, b1) = P{6, 7} − 0,16 = 0,04;
- cov(b3, b0) = P{9} − 0,1 = 0, cov(b2, b0) = P{5, 7} − 0,2 = 0, e cov(b1, b0) = P{3, 7} − 0,2 = 0.

As variâncias são 0,16, 0,24, 0,24 e 0,25. Os autovalores:
- b0 sozinho: 0,25;
- (0, 1, −1, 0): 0,24 − 0,04 = 0,20;
- no plano de (1, 0, 0, 0) e (0, 1, 1, 0)/√2, a matriz [[0,16; −0,08√2]; [−0,08√2; 0,28]], com traço 0,44 e determinante 0,032:
  λ = (0,44 ± √0,0656)/2, isto é, 0,34806 e 0,09194.

Os valores singulares dos dados centrados são √(10λ). O posto efetivo é exp(H(s/Σs)), e a função o calcula por código a partir destes
quatro λ: um caminho que não passa pelo Jacobi.

## Previsões do mundo, registradas antes de qualquer execução
**Procedência:**
- identidades: (d), (e), (i);
- forma fechada: (a), (b), (c), (f);
- contagem de mecanismo: (g), (h).

- **(a)** razão (desvio medido das 300 médias)/(σ/√500·√((N − 500)/(N − 1))) em **[0,933; 1,067]**. O desvio relativo de um desvio-padrão de
  300 amostras é 1/√598 = 0,041, vezes 1,645.
- **(b)** z da média das médias contra a média da população em **[−1,645; 1,645]**. Forma fechada: não viesado.
- **(c)** fração média da amostra vinda da primeira metade do arquivo em **[0,4979; 0,5021]**. ½ ± 1,645·√(¼·(N − k)/(N − 1)/k)/√300.
- **(d)** posto efetivo dos 16 vértices em **[3,999999999; 4,000000001]**. Identidade: as quatro colunas centradas valem ±½, são
  ortogonais e têm a mesma norma.
- **(e)** \|posto pelo Jacobi − posto pela conta à mão\| em **[0; 1e-9]**. Identidade.
- **(f)** \|posto de 3ⁿ − posto de Benford-16\| em **[0; 0,01]**. log₁₆ 3 é irracional, então n·log₁₆ 3 mod 1 é equidistribuído, com
  discrepância da ordem de log N / N.
- **(g)** previsões com veredito que a v5 recupera nas Partes 128 a 138 em **[70; 95]**. Contagem feita num arquivo do mesmo tipo (a Parte 137
  tem 11 linhas na tabela "Medido") e estendida pela regra da Parte 75: 129 6, 130 7, 131 a 134 8 cada, 136 11, 137 11, 138 9; a 128 eu não
  contei.
- **(h)** acerto dessas em **[0,85; 0,95]**. Pelos placares escritos: 69 de 76 sem a 128.
- **(i)** previsões que mudam nas partes com a linha de placar do mundo em **[0; 0]**. Identidade de desenho: a v5 usa as tabelas só quando a parte não tem a
  linha de placar do mundo.

### Previsões sobre as previsões (m), registradas (régua: P2837, leitor v4)
**Regra da Parte 120.** Rodei a régua sobre o rascunho com uma linha de placar provisória, apagada antes do commit. Ela deu m1 = 9, m2 = 4,
m3 = 0,0556 e m5 = 0. A primeira rodada deu m1 = 1, por causa da menção apontada acima: a regra da Parte 120 achou o defeito antes do
registro.

**Regra da Parte 122.** E = 0 × 3 identidades + 0,10 × 4 formas fechadas + 0,25 × 2 contagens de mecanismo = 0,9.
- **(m1)** nº de previsões do mundo em **[9; 10]**
- **(m2)** nº de faixas que cruzam ou tocam o zero em **[4; 5]**
- **(m3)** mediana de w das que não cruzam o zero em **[0,04; 0,08]**
- **(m4)** fração de acertos do mundo em **[0,67; 1,00]** (centro 8,1/9 = 0,90)
- **(m5)** nº de faixas com w > 0,6 em **[0; 0]**
- **(m6)** nº de surpresas (erro maior que a largura) em **[0; 1]**

### Sobre mim, registrado
Erros no mundo em **[0; 3]**, com centro 0,9.

➡ Anterior: [Parte 139](ASI_AGI_parte139_volta8.md).

## Medido (P3188–P3190)
- **(a)** razão dos desvios: 1,0129. ✅
- **(b)** z = 0,203. ✅
- **(c)** fração da primeira metade: **0,50233** (z = 1,81). ❌
- **(d)** posto dos 16 vértices: 4,000000000000. ✅
- **(e)** \|Jacobi − conta à mão\| = 8,9·10⁻¹⁶. ✅
- **(f)** \|3ⁿ − Benford-16\| = 0,00121 (posto de 3ⁿ: 3,95560). ✅
- **(g)** recuperadas: **83** (128: 7, 129: 6, 130: 7, 131 a 134: 8, 8, 8, 8, 136: 11, 137: 11, 138: 9). ✅
- **(h)** acerto: 76 de 83 = 0,916. ✅
- **(i)** a primeira versão da função deu **29**. Ela comparava TODAS as partes de 53 a 127, inclusive as que não têm a linha de placar, e não
  só as que a previsão nomeava. Conferi a régua antes de explicar (Parte 127): as 29 são previsões RECUPERADAS nas Partes 126 (17) e 127
  (12), que também estavam em tabela, e não mudanças. Nas partes com a linha de placar, as mudanças são **0**. A função foi corrigida para
  medir o que (i) diz. ✅, com a régua corrigida; a primeira versão errou a pergunta, e isto fica escrito aqui.

**O que a régua corrigida achou a mais:** as Partes 126 e 127 também estavam fora da calibração, com 29 previsões. A Parte 135 (a volta 8) e a
139 ainda não têm a tabela de vereditos.

### (c): lote novo antes de qualquer mecanismo (regra da Parte 117)
É uma forma fechada (hipergeométrica) que errou com z = 1,81. Registro, antes de rodar: sementes 141000 a 141299, outros 300 reservatórios,
mesma faixa [0,4979; 0,5021]. Se acertar, foi cauda. Se errar de novo para o mesmo lado, a regra da Parte 137 manda trocar o CAMINHO da
medida: contar pela posição sorteada, e não pelo índice.

**Lote novo (sementes 141000+):** 0,50307, z = 2,38, de novo acima: ❌. Os dois lotes juntos dão z ≈ 2,96. Pela regra da Parte 137, troco o
caminho. Registrado antes de rodar:
1. a mesma régua da metade sobre `random.sample(range(N), 500)`, independente do reservatório: 2.000 amostras, faixa [0,49918; 0,50083];
2. mais 1.000 reservatórios (sementes 142000+), faixa [0,49884; 0,50116].

Se só o reservatório desviar, o defeito está nele. Se os dois desviarem, está na régua da metade.
