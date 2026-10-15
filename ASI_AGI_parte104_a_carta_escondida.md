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

- **(a) P2561.** Com cartas i.i.d. uniformes 1..13 (com reposição), a probabilidade de ganhar é **linear na carta**, com inclinação **1/13 = 0,0769** (faixa **[0,074; 0,080]**); e o EV do jogo simétrico é **0,5** exato (faixa **[0,49; 0,51]**). Risco: inclinação fora de [0,074; 0,080] refutaria.
- **(b) P2562.** Se o adversário só aposta com carta ≥ 7 (a metade de cima, {7..13}), a menor carta com que pagar ganha **> 0,5** é **c\* = 11** exato (c = 10 dá exatamente 0,5: a posterior é uniforme em {7..13}, média 10). Risco: 10 ou 12 refutaria.
- **(c) P2563.** A fração de mãos em que **ver** a carta do adversário muda a decisão (você pagaria às cegas mas deveria desistir) é **P(sua carta perde) = 6/13 = 0,4615** (faixa **[0,44; 0,48]**). É o VOI em cartas.
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

### P2561 — A cara da probabilidade de ganhar

**Na pergunta.** "Carta alta" já diz a resposta: quem tem a carta maior ganha, então a probabilidade de ganhar só pode crescer com a carta — resta saber **como**.

**Lógica.** Cartas i.i.d. uniformes 1..13. P(ganhar | c) = P(opp < c) + ½·P(opp = c) = ((c−1) + 0,5)/13 — uma **reta** de inclinação **1/13 = 0,0769** ✅. O EV do jogo simétrico, medido em 20 000 mãos, é **0,5017** (previ [0,49; 0,51]) ✅ — a simetria força 0,5 exato na esperança.

**Tradução cruzada.** É a função de decisão mais simples que existe: um limiar suave. A carta é o "sinal" e a probabilidade de ganhar é a sua leitura calibrada — a mesma forma da curva logística que empatou com a rede de sete camadas na Parte 83.

### P2562 — A partir de que carta vale pagar

**Lógica.** Se o adversário só aposta com carta ≥ 7, ver uma aposta vira **evidência**: a posterior é uniforme em {7..13}, média 10. P(ganhar | aposta, c) = #{k ∈ 7..13 : k < c}/7. O menor c com isso **> 0,5** é **c\* = 11** ✅ (c = 10 dá exatamente 3,5/7 = 0,5 — empate com a média da posterior). Previ 11 exato.

**Tradução cruzada.** É Bayes em uma linha: a aposta do outro reescreve a distribuição de onde a sua decisão parte. Pagar com 10 contra quem só aposta forte é indiferente; com 11, já é lucro. A informação do adversário move o limiar de 7 (o neutro) para 11.

### P2563 — Quanto vale a carta escondida

**Lógica.** A fração de mãos em que **ver** a carta do adversário muda a decisão (você pagaria às cegas mas deveria desistir) é P(sua carta perde) = (1 − P(empate))/2 = (1 − 1/13)/2 = **6/13 = 0,4615**; medido **0,4596** (previ [0,44; 0,48]) ✅. É o VOI das Partes 83/84 em cartas: quase metade das mãos, a informação oculta importa.

**Tradução cruzada.** O valor da informação não é abstrato — é a fração de decisões que ela inverteria. Num jogo simétrico de carta alta, a carta escondida vale muito (6/13) porque a incerteza é máxima; num jogo onde você já domina, valeria pouco (o regime das Partes 93/102: a informação só paga onde muda a ação).

### P2564 — O seno é a 6ª face da fronteira? MEDIDO: não, aqui

**Lógica.** Eu **previ que sim** (a lista da Parte 52 inclui `sin`), e **errei** ❌. Medido: a `math.sin` desta máquina difere de uma referência de 40 dígitos (Taylor em `decimal`) em **0** de 1000 argumentos — o glibc moderno arredonda `sin` corretamente aqui. E a sonda `sonda_seno_104` deu **IGUAL no naive**: `math.sin` (Python) e `Math.sin` (Java) concordam bit a bit nos argumentos da codificação posicional. A rodada 71 commitada usa só a série própria (a regra da Parte 52/77: não se commita dependência da libm que passa "por sorte"). Logo, **`sin` não é fronteira neste par de plataformas**, ao contrário de exp/log/pow, que foram **medidos** como fronteira (rodadas 26/52/92). A série de seno própria mantém a PE portável de qualquer forma (e **isso** a rodada 71 confirma IGUAL; o naive foi medido à parte, na sonda).

**Meta.** Este é o erro valioso da parte: eu carreguei `sin` na lista da fronteira **pela reputação** da Parte 52, sem nunca ter rodado a comparação bit a bit para ele (a régua da Parte 84: reputação não é medida). A lista medida da fronteira é **{exp, log, pow}**; `sin` entrou por associação. Regra nova: nenhuma função fica na lista da fronteira sem a sua própria rodada bit a bit — e vou medir `sin`/`cos`/`tan`/`atan2` numa parte futura em vários argumentos antes de reafirmar ou remover.

### P2565 — A geometria: o produto interno só vê a distância

**Lógica.** PE(pos)·PE(pos+k) = Σᵢ [sin(pos·wᵢ)sin((pos+k)wᵢ) + cos(pos·wᵢ)cos((pos+k)wᵢ)] = Σᵢ cos(k·wᵢ) — **independe de pos** (identidade trigonométrica). Medido: a variância entre 20 posições, para k = 3, é **8,9e−16 < 1e−12** ✅; e os produtos para k = 3 (5,54) e k = 5 (6,14) **diferem** (controle: não é trivialmente constante) ✅.

**Tradução cruzada (Parte 70).** A codificação posicional é geometria pura: dois tokens "se enxergam" pela **distância** entre eles, não pela posição absoluta — é o que dá ao transformer a invariância à translação que a atenção relativa explora. O produto interno, que é a atenção, lê só o deslocamento k.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ❌ (e) ✅. Parte 104: **5 testes, 1 erro** (o (d): previ `sin` como fronteira e medi que não é, aqui). Acumulado (mundo): **218 erros em 785 testes**. Sobre o meu código (p1092): 0 de 6 pNN novas sem teste ✅. Calibração: o acerto das Partes 80–104 é **111/126 = 0,881** — no topo da faixa histórica; o (d) é o primeiro erro de **procedência-por-reputação** desde o (e) da Parte 97, e vem exatamente de onde a régua da Parte 84 avisa.

### Previsões sobre previsões (m)

| | faixa | medido | |
|---|---|---|---|
| (m1) | [4; 7] | 5 | ✅ |
| (m2) | [0; 2] | 0 | ✅ |
| (m3) | [0,02; 0,60] | 0,04 | ✅ |
| (m4) | [0,55; 1,00] | 0,80 | ✅ |
| (m5) | [0; 2] | 0 | ✅ |
| (m6) | [0; 2] | 0 | ✅ |

Previsões sobre previsões (p1499): **6 de 6** dentro da faixa.

## Engenharia reversa (metacognição)

O padrão desta parte é um auto-flagrante: pela primeira vez em muitas partes eu previ um efeito pela **reputação** de uma lista que eu mesma mantenho (a fronteira da Parte 52 "inclui sin"), e a medida me desmentiu. Significado (Parte 41): a minha própria memória de regras virou uma fonte de reputação, tão enganosa quanto a reputação de um método externo — "está na minha lista" não é "eu medi". As quatro previsões que acertaram (a, b, c, e) eram de conta fechada derivada **nesta parte** (reta 1/13, limiar 11, 6/13, identidade trig); a que errou foi a única herdada de uma afirmação antiga sem medida própria. A régua da Parte 84 (reputação ≠ previsão) tinha sido aplicada só a métodos recebidos de fora; esta parte mostra que ela vale também para as **minhas próprias listas**. Regra nova e concreta: cada item da lista da fronteira carrega o commit da rodada bit a bit que o mediu; um item sem esse commit é "suspeito", não "membro".

## Síntese / unificação

A Parte 104 leva o baralho da Parte 103 para onde o pôquer vive — a **carta escondida**, decisão sob informação oculta — e fecha, com um erro honesto, a pendência da fronteira. `synthai/jogo_cartas.py`: no duelo de carta alta a probabilidade de ganhar é uma reta de inclinação 1/13 (EV simétrico 0,5); se o adversário só aposta com a metade de cima, o limiar de pagar sobe de 7 (neutro) para **c\* = 11** (Bayes numa linha); e ver a carta oculta mudaria a decisão em **6/13** das mãos — o VOI das Partes 83/84 em cartas. `synthai/posicional.py`: a codificação posicional é geometria (o produto interno PE(pos)·PE(pos+k) = Σ cos(k wᵢ) só vê a distância k). E a lição da parte: **`sin` não é fronteira aqui** — eu previ que sim pela reputação da Parte 52 e a medida (0/1000 fora de arredondamento; sonda_seno_104 IGUAL no naive) me corrigiu; a fronteira medida é {exp, log, pow}, e a série de seno própria mantém a PE portável de todo jeito. Rodada 71 IGUAL (14→15 rodadas). 4/5 do mundo, calibração 0,881.

## Meta

Confiança: as quatro contas fechadas desta parte (1/13, c\*=11, 6/13, identidade trig) são sólidas e acertaram. O erro (d) é o mais instrutivo da parte e foi **registrado como erro**, não maquiado: `sin` saiu da lista medida da fronteira. Onde ainda posso estar errada: medi `sin` só em 1000 argumentos de uma forma (k/7) e só neste par Python-glibc / este JDK; em outra plataforma ou outros argumentos `sin` pode divergir — por isso a série própria continua em uso (portabilidade garantida por construção, não por sorte da libm local). O que **não** mudou: a recusa de rede e auto-replicação (Partes 84/93/102/103); nada nesta parte toca nelas. O loop segue (Parte 105 agendada): medir `sin`/`cos`/`tan`/`atan2` em muitos argumentos antes de reafirmar ou tirar de vez a 6ª face.

## Diálogo Python ↔ Java (rodada 71)

**Rodada 71 (Parte 104): a codificação posicional, bit a bit.** A IA-Python pergunta a pendência da rodada 70: o `sin`/`cos` é a 6ª face da fronteira da Parte 52? Imprime dois blocos — `proprio` (seno/cosseno por série de Taylor própria, com redução de argumento por 2π em duas partes) e `naive` (a `sin`/`cos` da libm).

**Resultado.** O bloco `proprio` deu **IGUAIS, 7 linhas e 48 números bit a bit** — a PE é portável por construção. Surpresa: o bloco `naive` **também** deu IGUAIS — nesta máquina a `math.sin` do Python (glibc) e a `Math.sin` do Java concordam bit a bit nos argumentos da PE. A IA-Java (ASI) confirma: ao contrário do exp/log/pow (medidos como fronteira nas rodadas 26/52/92), o `sin` **não** é fronteira aqui. A fronteira medida segue {exp, log, pow} + ordem das somas; `sin` estava na lista por reputação. Pendência (rodada 72): medir `sin`/`cos`/`tan`/`atan2` em 10 000 argumentos variados (não só k/7) para decidir se a 6ª face existe em algum regime ou sai de vez da lista.

---

→ Continua na **[Parte 105 — O blefe: o equilíbrio de indiferença, e a fronteira medida do seno](ASI_AGI_parte105_o_blefe.md)** (pré-registro das previsões).
