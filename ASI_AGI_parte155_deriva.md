# Parte 155 — A deriva do setdefault: a primeira casa puxa o caminho para um canto

↩ Nasce da Parte 154 (o setdefault tira sempre de 1,3% a 3,0% do acerto, e a leitura era "puxa o caminho para o canto de cima à esquerda") e da sua pendência 1:
testar a leitura pela simetria e pela medida direta do caminho.

## O recolhimento do contêiner, 13º lote
Despertar às 10h08, depois de cerca de 55 minutos ociosa: "up 0 min", como previsto. Treze lotes a favor.

## A medida
`synthai/tabuleiro.py`, `estatisticas_exatas`: o enumerador exato com a ordem das vizinhas escolhível (direta, (−1, −1), …, (1, 1); ou reversa) e as esperanças,
no fim do episódio, do deslocamento da casa final em relação à inicial (dr, dc), da distância da casa final à borda e do comprimento. Confere com o
`aleatorio_exato` (B, 3 a 4 letras: 0,3389121371604974 contra 0,33891213716057256, a diferença é a ordem das somas).

**A simetria, escrita antes:** inverter a ordem das vizinhas é a rotação de 180° da grade. Como as letras são sorteadas independentes e a casa inicial é uniforme,
o jogo com a ordem reversa é o jogo direto visto de cabeça para baixo: o acerto é o MESMO e o deslocamento troca de sinal. Com a casa sorteada (uniforme), o
deslocamento médio é zero por simetria. Isso são identidades; o que pode errar é o código.

**A calibração (3 a 4 letras), antes das previsões:**

| caso | casa | acerto | dr | dc | distância à borda | comprimento |
|---|---|---|---|---|---|---|
| B | primeira | 0,33891 | −0,39840 | −0,17914 | 0,16744 | 3,63447 |
| B | uniforme | 0,34320 | 0,00000 | 0,00000 | 0,17148 | 3,64000 |
| A' | primeira | 0,23977 | −0,52659 | −0,24544 | 0,16153 | 3,58308 |
| A' | uniforme | 0,25190 | 0,00000 | 0,00000 | 0,17883 | 3,59135 |

A leitura da Parte 154 se confirma no caso de calibração: com a primeira casa, o caminho deriva para cima (dr < 0) e para a esquerda (dc < 0), mais em linha que
em coluna (as três primeiras vizinhas da ordem têm dr = −1; só uma tem dc = −1 antes das de dc = 0), e termina mais perto da borda.

## Previsões para o teste (3 a 5 letras), registradas antes de rodar
**A conta do centro (por código, no texto):** a deriva por passo da calibração vezes o número esperado de passos no teste. Pela geometria sem colapso (Parte 151),
E[L] = 3,7392 com 3 a 4 letras e 4,2445 com 3 a 5; o fator (4,2445 − 1)/(3,7392 − 1) = 1,1845. **Mecanismo sem calibração do fator:** numa grade 3 × 3 a deriva
satura (não passa de 2), então a conta linear deve exagerar. Faixa ±25% do centro, larga (Parte 62).
- **(a)** nº de casos (B e A') em que o acerto com a ordem reversa é igual ao da direta a menos de 1e-12 em **[2; 2]** (identidade).
- **(b)** nº de deslocamentos (dr e dc, nos 2 casos) em que reversa = −direta a menos de 1e-12 em **[4; 4]** (identidade).
- **(c)** nº de deslocamentos com a casa uniforme iguais a 0 a menos de 1e-12 em **[4; 4]** (identidade).
- **(d)** dr de B, primeira, em **[−0,5899; −0,3539]** (centro −0,3984 · 1,1845 = −0,4719)
- **(e)** dc de B, primeira, em **[−0,2652; −0,1591]** (centro −0,2122)
- **(f)** dr de A', primeira, em **[−0,7797; −0,4678]** (centro −0,6237)
- **(g)** dc de A', primeira, em **[−0,3634; −0,2180]** (centro −0,2907)
- **(h)** nº de casos em que a primeira termina MAIS perto da borda que a uniforme em **[2; 2]** (mecanismo: a deriva leva à borda; nas duas calibrações a diferença
  foi 0,004 e 0,017, e o teste tem um passo a mais).

### Previsões sobre as previsões (m), registradas (régua: P2837)
A régua sobre o rascunho com "Do mundo:" provisória: m1 = 8, m2 = 0, m3 = 0,125, m5 = 0. E = 4 faixas de mecanismo × 0,4 + 1 contagem de mecanismo × 0,2 +
3 identidades × 0 = 1,8; m1 em [8; 8 + 2E] = [8; 11,6], arredondado para cima. Acertos como contagem: 4 a 8 das 8 (4/8 = 0,5000).
- **(m1)** nº de previsões do mundo em **[8; 12]**
- **(m2)** nº que cruzam ou tocam o zero em **[0; 0]**
- **(m3)** mediana de w em **[0,10; 0,15]**
- **(m4)** fração de acertos em **[0,5000; 1,0000]**
- **(m5)** nº com w > 0,6 em **[0; 0]**
- **(m6)** surpresas em **[0; 1]**

### Sobre mim, registrado
Erros no mundo em **[0; 4]**, centro 1,8.

## Medido (P3214)

| caso | versão | acerto | dr | dc | distância à borda | comprimento |
|---|---|---|---|---|---|---|
| B | direta | 0,301690 | −0,33628 | −0,13730 | 0,13922 | 4,01884 |
| B | reversa | 0,301690 | +0,33628 | +0,13730 | 0,13922 | 4,01884 |
| B | uniforme | 0,306377 | 0,00000 | 0,00000 | 0,13684 | 4,02598 |
| A' | direta | 0,241437 | −0,45915 | −0,17743 | 0,14769 | 3,91672 |
| A' | reversa | 0,241437 | +0,45915 | +0,17743 | 0,14769 | 3,91672 |
| A' | uniforme | 0,248427 | 0,00000 | 0,00000 | 0,15026 | 3,92436 |

- **(a)** acerto reverso = direto nos 2 casos (diferenças 8e-15 e 4e-16). ✅
- **(b)** deslocamento reverso = −direto nos 4. ✅
- **(c)** deslocamento uniforme = 0 nos 4 (|x| < 2e-16). ✅
- **(d)** dr de B: **−0,3363**, fora de [−0,5899; −0,3539]. ❌
- **(e)** dc de B: **−0,1373**, fora de [−0,2652; −0,1591]. ❌
- **(f)** dr de A': **−0,4591**, fora de [−0,7797; −0,4678]. ❌
- **(g)** dc de A': **−0,1774**, fora de [−0,3634; −0,2180]. ❌
- **(h)** a primeira termina mais perto da borda: só em A' (0,1477 contra 0,1503); em B termina mais LONGE (0,1392 contra 0,1368). **1 de 2**. ❌

**O erro de mecanismo:** a deriva não cresceu com o caminho mais longo, DIMINUIU (B: dr −0,398 com 3 a 4 letras, −0,336 com 3 a 5). Numa grade 3 × 3, um caminho sem
repetir casa que deriva para um canto bate na borda e tem de voltar; o passo a mais traz o fim de volta para o meio. Eu escalei a deriva linearmente pelo número de
passos a partir de UM comprimento de calibração (a regra da Parte 93: o tamanho de um efeito pede ≥ 2 condições cobrindo a variável que o move), e escrevi "a deriva
satura" ao lado sem deslocar o centro (a regra da Parte 149: um viés nomeado ganha conta de peso ou entra como desvio do centro). As duas regras desobedecidas na
mesma previsão.

## Um lote novo, registrado antes de rodar (B, de 3 a 6 letras)
Antes de qualquer explicação, o próximo comprimento. Com o mecanismo "o fim volta para o meio", |dr| continua caindo, sem chegar a zero (a primeira casa ainda
puxa). Pela tendência de 4 para 5 letras (−0,398 → −0,336, queda de 0,062), mais um passo de queda de mesmo tamanho daria −0,274; faixa larga (2 pontos):
- **(i)** dr de B, primeira, de 3 a 6 letras, em **[−0,336; −0,15]** (centro −0,274, por código: −0,3363 + (−0,3363 − (−0,3984)))
- **(j)** dc de B, primeira, de 3 a 6 letras, em **[−0,137; −0,05]** (centro −0,137 + (−0,137 + 0,179) = −0,095)

**Medido no lote novo (3 a 6 letras):** dr = −0,29525 (i ✅), dc = −0,11634 (j ✅). A deriva cai a cada passo a mais (dr: −0,398, −0,336, −0,295 com máximo 4, 5, 6;
quedas de 0,062 e 0,041), sem trocar de sinal.

### A rodada 103, registrada antes
`estatisticas_exatas` com a ordem REVERSA traduzida (caso B, 3 a 4 letras): o vetor (acerto, dr, dc, borda, comprimento, falha) por caminho, somado por ação na ordem
reversa das vizinhas e dividido por n; o total ponderado por atribuição. Só + × ÷ e min de inteiros. Previsão: **IGUAL**.
