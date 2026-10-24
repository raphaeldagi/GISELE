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
- **(a0)** Q-learning, média das sementes 101 a 120, em **[0,20; 0,30]**
- **(b0)** G = 2 − Q, média das sementes 101 a 120, em **[0,04; 0,11]**
