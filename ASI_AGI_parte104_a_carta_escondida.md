# Parte 104 — A carta escondida: decisão sob informação oculta, e a fronteira do seno (0x68)

↩ Parte 103 (o baralho como número+palavra) · ↩ Partes 83/84 (decisão sob incerteza, VOI) · ↩ Parte 52 (a fronteira das transcendentais)

> Continuação autônoma (o pedido permanente: "não pare mais"). A Parte 103 deixou o baralho como um sinal número+palavra, mas com informação **completa**. O pôquer, que o usuário pediu, só é interessante quando há uma **carta escondida**: decisão sob informação oculta. É a volta ao tema das Partes 83/84 (o valor da informação, a decisão bayesiana), agora com cartas. E a rodada 71 fecha a pendência da 70: o seno/cosseno da codificação posicional é a 6ª face da fronteira da Parte 52?

## As perguntas desta parte

1. **P2561 (0x9F9).** No duelo de carta alta, qual a cara da probabilidade de ganhar em função da carta? ↩ P2532
2. **P2562 (0x9FA).** Se o adversário só aposta com a metade de cima, a partir de que carta vale pagar? ↩ P2561
3. **P2563 (0x9FB).** Quanto vale ver a carta escondida do adversário? (o VOI das Partes 83/84, agora em cartas) ↩ P1662
4. **P2564 (0x9FC).** O seno/cosseno da codificação posicional é a 6ª face da fronteira da Parte 52? (rodada 71) ↩ rodada 70
5. **P2565 (0x9FD).** O produto interno de duas codificações posicionais depende só da distância entre elas? (a geometria, Parte 70) ↩ P2564

## Previsões pré-registradas (ANTES de medir — este commit)

- **(a) P2561.** Com cartas i.i.d. uniformes 1..13 (com reposição), a probabilidade de ganhar é **linear na carta**, com inclinação **1/13 = 0,0769** (faixa [0,074; 0,080]); e o EV do jogo simétrico é **0,5** exato (faixa [0,49; 0,51] na simulação). Risco: inclinação fora de [0,074; 0,080] refutaria.
- **(b) P2562.** Se o adversário só aposta com carta ≥ 7 (a metade de cima, {7..13}), a menor carta com que pagar ganha **> 0,5** é **c\* = 11** exato (c = 10 dá exatamente 0,5: a posterior é uniforme em {7..13}, média 10). Risco: 10 ou 12 refutaria.
- **(c) P2563.** A fração de mãos em que **ver** a carta do adversário muda a decisão (você pagaria às cegas mas deveria desistir) é **P(sua carta perde) = 6/13 = 0,4615** (faixa [0,44; 0,48] na simulação). É o VOI em cartas.
- **(d) P2564.** A `sin`/`cos` da libm **não é corretamente arredondada**: comparada a uma referência de 40 dígitos (Taylor em `decimal`), difere em **≥ 1** de 1000 argumentos (a 6ª face da fronteira da Parte 52). E a codificação posicional calculada com uma **série de seno própria** fica **IGUAL** bit a bit em Java (rodada 71). Risco: 0 diferenças refutaria a 1ª parte.
- **(e) P2565.** O produto interno PE(pos)·PE(pos+k) depende **só de k**, não de pos (identidade trigonométrica: Σᵢ cos(k·wᵢ)): a variância entre as posições, para k fixo, é **< 1e-12**. Controle: para k₁ ≠ k₂ os produtos diferem (não é trivialmente constante).

### Previsões sobre as previsões (m), pré-registradas

- **(m1)** nº de previsões do mundo em **[4; 7]**
- **(m2)** nº de faixas que cruzam/tocam o zero em **[0; 2]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0,02; 0,60]**
- **(m4)** fração de acertos do mundo em **[0,55; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 2]**

### Sobre mim, pré-registrado

(a), (b), (c), (e) são de conta fechada (linearidade, limiar inteiro, 6/13, identidade trig); (d) é a fronteira já conhecida (Parte 52) aplicada a uma função nova. Espero **0–1 erro** do mundo; o risco real é (c) (a cauda amostral da fração) e a 1ª parte de (d) (se a libm desta máquina for, por acaso, corretamente arredondada nestes 1000 args).

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->

## As respostas (quatro camadas)

RESP_PLACEHOLDER

## Placar do mundo desta parte

PLACAR_104_TEXTO

## Engenharia reversa (metacognição)

ENG_PLACEHOLDER

## Síntese / unificação

SINTESE_PLACEHOLDER

## Meta

META_PLACEHOLDER

## Diálogo Python ↔ Java (rodada 71)

DIALOGO_PLACEHOLDER
