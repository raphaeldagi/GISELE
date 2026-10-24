# Parte 149 — A GRPO no jogo de palavras em português

↩ Nasce da Parte 148 (a GRPO no dicionário grande inglês) e da regra do data lake (Parte 30, com o português da OpenWordNet-PT desde a Parte 39).
A pergunta: a dependência entre o tamanho do dicionário e a vantagem da GRPO, vista em dois dicionários ingleses, prevê um terceiro, em outra língua?

## O recolhimento do contêiner, 7º lote
Despertar às 01h45, depois de cerca de 55 minutos ociosa: "up 0 min", como previsto (up < 5 min). Sete lotes, todos a favor.

## O dicionário
`synthai.palavras_rl.lemas_ownpt()`: os lemas da OpenWordNet-PT (CC BY 4.0), em minúsculas, sem acentos e sem cedilha (NFD sem as marcas), só os
formados por a-z: **34.384 lemas, 4.181 deles com 3 a 5 letras** (o tamanho que o jogo aceita). As palavras embutidas do `word_rl_lab` têm 493 com
3 a 5 letras; os lemas do WordNet, 9.686. A grade continua sorteada com as frequências de letras do INGLÊS (`LETTER_FREQ`): o português joga num
tabuleiro de outra língua.

## Previsão de mecanismo, registrada antes de qualquer calibração em português (regra da Parte 24: prever pela conta antes de simular)
**A conta:** interpolar linearmente em ln(nº de palavras de 3 a 5 letras) entre os dois dicionários já medidos. A fração é
(ln 4.181 − ln 493)/(ln 9.686 − ln 493) = 0,718.
- Q: 0,1533 + 0,718 · (0,3020 − 0,1533) = 0,260.
- G = 2 − Q: 0,0484 + 0,718 · (0,0946 − 0,0484) = 0,082.

**O que pode quebrar a conta:** as letras do tabuleiro são inglesas, e o português precisa de vogais em proporção maior; com isso, menos palavras
portuguesas cabem nas grades, e o dicionário "efetivo" fica menor que 4.181. Esse viés empurra os dois números para baixo. Sem uma conta do peso
dele (Parte 62), a faixa é larga e a procedência é "mecanismo sem calibração" (taxa de erro histórica dessas: alta).
- **(s)** (registrada como "(a0)"; renomeada porque a régua só lê rótulos de uma letra) Q-learning, média das sementes 101 a 120, em **[0,20; 0,30]**
- **(t)** G = 2 − Q, média das sementes 101 a 120, em **[0,04; 0,11]**

## A calibração (sementes 101 a 120; 20 sementes, regra da Parte 148)
Média e desvio entre sementes (P3201):

| quantidade | média | desvio |
|---|---|---|
| Q-learning | 0,1403 | 0,0214 |
| aleatório | 0,0131 | 0,0026 |
| GRPO G = 2 | 0,2026 | 0,0215 |
| GRPO G = 8 | 0,2010 | 0,0276 |
| sem contraste G = 2 | 0,9702 | 0,0030 |
| sem contraste G = 8 | 0,8892 | 0,0173 |
| G = 2 − Q | 0,0623 | 0,0280 |
| G = 8 − Q | 0,0607 | 0,0370 |
| G = 8 − G = 2 | −0,0016 | 0,0332 |

As duas GRPO acima do Q-learning em 19 de 20 sementes.

**As previsões de mecanismo:** (s) Q = 0,1403, fora de [0,20; 0,30] ❌; (t) G = 2 − Q = 0,0623, dentro de [0,04; 0,11] ✅. O viés que eu nomeei
(letras inglesas no tabuleiro) era real e GRANDE: com 8,5 vezes mais palavras que o dicionário embutido, o Q-learning em português acha menos
palavras (0,140 contra 0,153). O tamanho do dicionário não é a variável certa; a variável é quantas palavras CABEM no tabuleiro. O aleatório mede
isso sem agente: 0,0131 em português contra 0,047 no inglês grande.

## Previsões do teste, registradas antes de rodar as sementes 121 a 140
Meia-largura 1,645 · 1,36 · σ · √(1/20 + 1/20) (erro do centro mais o da medida; 20 sementes de calibração, então 1,645 e não o t, regra da
Parte 148). Centro de "quantos erros": 9 faixas de calibração × 0,25 + 1 de forma fechada × 0,10 + 1 contagem × 0,10 + 1 de mecanismo × 0,4 ≈ 2,9.
- **(a)** Q-learning em **[0,1252; 0,1554]**
- **(b)** aleatório em **[0,0112; 0,0150]**. Forma fechada: o p do aleatório não depende de aprendizado (Parte 147); binomial com 1.000 episódios,
  √(0,0131 · 0,9869/1000) = 0,0036 por semente, 0,0008 na média de 20 e 0,0008 de erro do centro: 1,645 · √2 · 0,0008.
- **(c)** GRPO G = 2 em **[0,1874; 0,2178]**
- **(d)** sem contraste G = 2 em **[0,9681; 0,9723]**
- **(e)** GRPO G = 8 em **[0,1815; 0,2205]**
- **(f)** sem contraste G = 8 em **[0,8770; 0,9014]**
- **(g)** G = 2 − Q em **[0,0425; 0,0821]**
- **(h)** G = 8 − Q em **[0,0345; 0,0869]**
- **(i)** G = 8 − G = 2 em **[−0,0251; 0,0219]**. Cruza o zero; registro a diferença, não a ordem.
- **(j)** nº de sementes, em 20, com as duas GRPO acima do Q em **[17; 20]**: binomial com p = 19/20; P(≤ 16) = 0,016 e P(≤ 17) = 0,075, então
  [17; 20] tem 0,984.
- **(k)** o aleatório no dicionário EMBUTIDO, sementes 43 a 45 (as da Parte 147), em **[0,004; 0,011]**. Mecanismo: a Parte 111 mediu que os 77.340
  lemas multiplicam o aleatório por 6,2; 0,047/6,2 = 0,0076; binomial 0,0027 por semente, 0,0016 na média de 3, mais o erro do centro. Se acertar,
  o Q-learning NÃO é função só do aleatório: o embutido teria aleatório menor que o português (0,0076 contra 0,0131) e Q maior (0,153 contra 0,140).

### A auditoria retroativa com o quantil t (pendência 1 da Parte 148), registrada antes
Faixas de CALIBRAÇÃO das Partes 147 e 148 que erraram, refeitas trocando 1,645 pelo quantil t de n_cal − 1 graus (as outras partes não escrevem
n_cal de forma que uma régua leia: fica pendente). Os erros de calibração foram 147 (b) (n_cal = 3), 148 (a) (n_cal = 8) e 148 (n) (n_cal = 28).
A (d) da 147 tinha procedência binomial e não entra. A conta, feita à mão e conferida por código antes do registro: só a 147 (b) passa a acertar.
- **(r)** nº de erros de calibração das Partes 147-148 que viram acerto com o quantil t em **[1; 1]**. É uma identidade (a conta é determinística
  sobre faixas já escritas); o código pode errar, a conta não.

### Previsões sobre as previsões (m), registradas (régua: P2837)
A régua rodou sobre o rascunho com uma linha "Do mundo:" provisória (regra da Parte 120): m1 = 14, m2 = 1, m3 = 0,108, m5 = 0. O primeiro rascunho
deu m1 = 0, porque o leitor só aceita rótulos de uma letra e "(a0)" quebrava a linha do placar; renomeei para (s) e (t). Erros esperados nas 12 que
faltam: E ≈ 2,5, então m1 em [14; 14 + 2E] (regra da Parte 148). Acertos como contagem: 9 a 13 das 14 registradas.
- **(m1)** nº de previsões do mundo em **[14; 19]**
- **(m2)** nº que cruzam ou tocam o zero em **[1; 2]**
- **(m3)** mediana de w em **[0,08; 0,14]**
- **(m4)** fração de acertos em **[0,60; 0,93]**
- **(m5)** nº com w > 0,6 em **[0; 0]**
- **(m6)** surpresas em **[0; 1]**

### Sobre mim, registrado
Erros no mundo em **[1; 6]**: o (s) já errou, e as 12 que faltam têm centro 2,5 (desvio binomial ≈ 1,4).
