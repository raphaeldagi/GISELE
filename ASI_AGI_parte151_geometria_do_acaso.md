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

### A rodada 99, registrada antes
`paradas_por_comprimento` traduzida: a recursão sobre os caminhos sem repetir casa, nas grades 4 × 4, 5 × 5 e 6 × 6 e nos comprimentos (3, 5), (3, 4), (4, 5), com
as somas p/n acumuladas na MESMA ordem (vizinhas na ordem (−1, −1), (−1, 0), …, (1, 1), casas de partida por linha). Só + e ÷. Previsão: **IGUAL**. O que
poderia quebrar: a ordem em que as parcelas entram em s_L (a soma de ponto flutuante não é associativa); os dois lados fazem a mesma recursão em profundidade.

## Medido (P3207, P3208; rodada 99)
- **(a)** grade 4 × 4: 0,0251 (geometria 0,0239; razão 1,048). ✅
- **(b)** grade 6 × 6: 0,0204 (geometria 0,0211; 0,969). ✅
- **(c)** no máximo 4 letras: 0,0368 (0,0351; 1,048). ✅
- **(d)** no mínimo 4 letras: 0,0070 (0,0078; 0,892). ✅ (a 0,0001 do piso)
- **(e)** distintas, português / inglês: 33,3. ✅
- **(f)** repertório, português / inglês: 0,8844. ✅
- **(g)** distintas, português / português: 50,1. ✅
- **(h)** repertório, português / português: 0,9351. ✅
- **(i)** acerto do Q, embutido: 0,1348. ✅
- **(j)** distintas, embutido: 22,35. ✅
- **(k)** repertório, embutido: 0,9425. ✅
- **(l)** embutido − português, repertório: +0,0582. ✅
- **(n)** tabuleiro português − inglês, repertório: +0,0507. ✅
- **Rodada 99:** IGUAL, 7 linhas e 13 números bit a bit. ✅

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ✅ (l) ✅ (n) ✅

**Mundo: 13 de 13.** **Sobre mim:** 0 erros, em [0; 6]: ✅. A chance de 13 de 13 com p = 0,9 por faixa é 0,9¹³ = 0,25; com as taxas de procedência usadas no
centro (0,85 e 0,75), 0,85⁴ · 0,75⁹ = 0,039. As faixas foram mais largas do que precisavam: o centro de erros (2,85) superestimou, como nas Partes 116 e 117.

Os acertos do português nas sementes 121 a 140 saíram iguais aos das Partes 149 e 150 (0,1431 e 0,2934): a P3208 reproduz o avaliador de outra função pelo
mesmo caminho.

### O que a geometria mostrou
**A constante não é ajustada: é a chance de parar.** A lei da Parte 150, aleatório ≈ 0,21 · D, é Σ_L s_L · D_L com s_L tirado da enumeração exata dos caminhos
(s₃ = 0,194 na grade 5 × 5), e D₃ domina. Em quatro mundos que a calibração não tinha (outras grades, outros comprimentos), a conta com a correção média
1,054 acertou os quatro. A grade quase não importa (4 × 4: 0,0251; 6 × 6: 0,0204): o que muda é a chance de parar cedo (s₃ cai de 0,212 para 0,183, porque com
mais vizinhas o PARAR é uma opção entre mais). O comprimento importa muito: exigir 4 letras dividiu o acaso por 3,2 (0,0224 → 0,0070), porque tira D₃.

**A correção 1,054 não é uma constante.** As razões medido/geometria vão de 0,89 (mínimo 4 letras) a 1,14 (embutido no tabuleiro inglês). O colapso de vizinhas
com a mesma letra (`valid_actions` junta numa ação só) muda o peso de cada letra no caminho de forma diferente em cada dicionário. É o resto da conta; a forma
fechada dele é a pendência.

### O que o repertório mostrou
Em 2 lotes (calibração e teste), nas duas comparações: o embutido repete mais palavras que o português no mesmo tabuleiro (+0,047 e +0,058), com menos
palavras distintas (23 contra 32-33); e o tabuleiro português sobe o repertório do português (+0,044 e +0,051). A leitura da Parte 149 ganha um número: o
Q-learning tabular rende mais onde as palavras se REPETEM entre grades, e o embutido (493 palavras de 3 a 5 letras, comuns) é o caso extremo. Mas a comparação
do tabuleiro português não separa as duas causas: o acerto dobrou junto, e mais acertos repetem mais por pura contagem.

## Engenharia reversa
- **O padrão desta parte é o oposto do das Partes 149-150:** lá eu previ com mecanismos sem peso e errei; aqui a conta exata (a enumeração dos caminhos) veio
  antes, e os quatro mundos novos ficaram dentro. A regra da Parte 24 ("prever pela conta antes de simular") deu 13 de 13.
- **E a minha largura ficou grande demais:** 0 erros para um centro de 2,85. O centro de erros das calibrações com 20 sementes usa a taxa histórica 0,25,
  que vem das calibrações de 3 a 8 sementes. Com 20 sementes, as Partes 149-151 tiveram 0 erros em 9 + 8 + 9 = 26 faixas de calibração.
- **Regra (Parte 151):** a taxa de erro esperada de uma faixa de calibração depende do número de sementes; com ≥ 20, usar a taxa medida nas partes que já
  calibraram assim (0 em 26 até aqui: a cota superior de 90% é 1 − 0,1^(1/26) = 0,085), e não a das calibrações pequenas.

## Funções e testes
- **Funções:** `p3207_aleatorio_geometria`, `p3208_repertorio` e `_parte_151`; em `synthai/tabuleiro.py`, `paradas_por_comprimento`,
  `densidade_por_comprimento` e `aleatorio_geometrico`. Entradas P3207 e P3208 na regressão.
- **Diálogo:** `dialogo/rodada99.py` e `dialogo/Rodada99.java`, IGUAL.
- **Testes:** `synthai/testes_parte151.py`.

**O placar (m):** m1 = 13 em [13; 19] ✅, m2 = 0 em [0; 1] ✅, m3 = 0,123 em [0,09; 0,16] ✅, m4 = 1,0 em [0,5385; 1,0000] ✅, m5 = 1 em [1; 2] ✅ e m6 = 0 ✅.
**6 de 6.** A fração exata no limite (regra da Parte 150) não foi posta à prova: nenhum erro.

➡ Anterior: [Parte 150](ASI_AGI_parte150_tabuleiro_portugues.md).
