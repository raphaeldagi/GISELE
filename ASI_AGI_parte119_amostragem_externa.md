# Parte 119 — A amostragem externa: sortear também o adversário (0x77)

↩ Parte 118 (o MCCFR com o acaso amostrado) · ↩ Parte 113 (o CFR vanilla) · ↩ Parte 105 (o blefe e a indiferença)

> **Continuação autônoma (a pendência da Parte 118, rodada 86).** Na Parte 118 o CFR sorteava só as cartas e percorria as ações dos dois jogadores. A amostragem EXTERNA sorteia também as ações do ADVERSÁRIO, segundo a estratégia corrente dele, e só percorre as do viajante. É a variante que escala para jogos grandes, porque o custo de uma iteração cresce com as ações de UM jogador, e não dos dois.
>
> **Antes do registro (conferências, não previsões).**
> - **A suíte inteira** roda em segundo plano desde o início da parte, pedida pela agenda. O resultado entra no texto.
> - **A calibração** (regras das Partes 62 a 64): sementes de calibração escolhidas por regra (1191, 1193, 1195 e 1197), em T = 500 e T = 5.000 iterações (cada uma com uma travessia por jogador).
>   - **Explorabilidade média:** 0,0831 (T = 500) e 0,0300 (T = 5.000). A razão por década é **2,77**, e o desvio entre sementes em T = 5.000 é ~43% da média (0,011 a 0,042).
>   - **P(paga com a dama | aposta) do jogador 2:** em T = 5.000, ficou ACIMA de 1/3 nas 4 sementes (+0,005, +0,093, +0,063, +0,076; média +0,059). A média "estocástica" da amostragem externa soma σ(I) só quando o adversário passa por I, então o seu viés tem um sinal neste regime.
> - **O mecanismo da calibração está presente no teste?** Sim: o mesmo jogo, o mesmo amostrador e a variável T. As sementes do teste (1192 e, para a rodada, 1195 com T = 3.000) não foram olhadas em T = 50.000.

## As perguntas desta parte

1. **P3011 (0xBC3).** O MCCFR com amostragem externa converge para o equilíbrio de Kuhn? Com que velocidade, contra a amostragem do acaso? ↩ P2982
2. **P3012 (0xBC4).** O viés da média estocástica (a dama paga mais que 1/3) some com T, e em que ritmo? ↩ P3011
3. **P3013 (0xBC5).** Sortear as ações do adversário (o uniforme x/2³¹) acrescenta fronteira entre Python e Java? (rodada 86) ↩ P2983

## Previsões pré-registradas (ANTES de medir — este commit)

**As fixtures (neste commit):** `synthai/mccfr_externo.py`.
- **O teste:** `CFRExterno().iterar_externo(50000, 1192)`.
- **A rodada 86:** `dialogo/rodada86.py`, semente 1195, T = 3.000.

**A convergência (P3011/P3012).**
- **(a)** A explorabilidade da estratégia média em T = 50.000. O mecanismo é o ruído de amostragem, que cai com a razão da calibração (2,77 por década): centro 0,0300/2,77 = 0,0108. A meia-largura é o desvio relativo entre sementes (43%) × 1,645 × 1,36 = 96%: **[0,0004; 0,0213]**. Larga, com o mecanismo escrito: abaixo de 0,0004, a convergência é muito mais rápida que a da calibração; acima de 0,0213, o ruído não cai.
- **(b)** A P(paga com a dama) em T = 50.000. O viés positivo da calibração (+0,059) cai pela mesma razão: +0,059/2,77 = +0,021, centro 0,355. O desvio entre sementes (~0,035) também cai pela razão, para 0,013, e a faixa é ±1,645 × 0,013 × 1,36 = ±0,029: **[0,326; 0,384]**. Se der abaixo de 1/3 por mais de 0,007, o viés tinha o sinal errado.

**O diálogo (P3013).**
- **(c)** A rodada 86 (amostragem externa, T = 3.000) é **IGUAL** bit a bit entre Python e Java: **[0; 0]**. Identidade: o LCG e o uniforme x/2³¹ são exatos (um inteiro abaixo de 2³¹ dividido por uma potência de 2), e o resto são +, −, ×, ÷ e comparações na mesma ordem.
- **(d)** A estratégia média da `rodada86.py` contra a de `synthai.mccfr_externo` (mesma semente e mesmo T): conjuntos que diferem em algum bit, **[0; 0]**. Identidade: a mesma sequência de sorteios (a distribuição antes de cada travessia, o uniforme em cada nó do adversário, na ordem da recursão), o mesmo `no = s₀u₀ + s₁u₁` e as mesmas somas.

### Previsões sobre as previsões (m), pré-registradas (régua: P2837, leitor v4)

Contagem pelo leitor antes do commit: **4**, mais até 2 de um adendo.
- **(m1)** nº de previsões do mundo em **[4; 6]**
- **(m2)** nº de faixas que cruzam/tocam o zero em **[2; 3]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0; 0,96]**
- **(m4)** fração de acertos do mundo em **[0,50; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 1]**

### Sobre mim, pré-registrado

Pela regra da Parte 117, o centro de "quantos erros" = 0 × 2 identidades + 0,2 × 2 faixas de mecanismo = **0,4**; faixa **[0; 1]**. O risco maior é a (b): o sinal do viés vem de 4 sementes de UM T, e a regra da Parte 64 diz que poucos casos não fixam um sinal.

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->

## As respostas (quatro camadas)

### P3011 — A amostragem externa converge

**Na pergunta.** "Sortear o adversário" é tratar o outro como parte do acaso: a estratégia dele, naquele momento, é uma distribuição como a das cartas. O viajante aprende contra amostras do adversário, não contra o adversário inteiro.

**Lógica.**
- Em T = 50.000 iterações (semente 1192), a explorabilidade da estratégia média é **0,01017** ✅ (a), contra o centro 0,0108. A razão de T = 5.000 para T = 50.000 foi 0,0300/0,01017 = **2,95**, entre a da calibração (2,77) e √10 (3,16).
- **O custo** (P3012, contado por código: chamadas da recursão por iteração): o vanilla visita **54,0** nós (6 distribuições × 9), o do acaso **9,0** (uma distribuição) e o externo **10,63** (duas travessias, cada uma com o adversário sorteado).
- **Com o mesmo número de nós** (~530 mil: o acaso com 60.000 iterações, Parte 118, e o externo com 50.000), o externo explora **1,9 vez mais** (0,0102 contra 0,0053).

No Kuhn, a amostragem externa NÃO ganha. Cada jogador tem 2 ações, então sortear o adversário economiza pouco por travessia e acrescenta variância. Ela foi feita para árvores largas: no Leduc e no pôquer real, o número de ações do adversário multiplica o custo de percorrê-lo.

**Tradução cruzada.** Imaginar o outro inteiro (todas as respostas possíveis dele) contra imaginar UMA resposta provável de cada vez. Num diálogo de duas falas possíveis, imaginar tudo é barato e mais exato; num mundo de muitas, só a amostra cabe. É o regime das Partes 93, 102 e 107 de novo: o método mais econômico só vence onde a tarefa é grande o bastante para precisar da economia.

### P3012 — O viés da média estocástica

**Lógica.** A P(paga com a dama | aposta) do jogador 2 é **0,3485** ✅ (b): +0,0152 acima de 1/3, com o sinal da calibração.
- O viés de T = 5.000 (+0,059) caiu **3,9 vezes** em uma década, mais rápido que a razão da explorabilidade (2,95).
- A média estocástica soma σ(I) só nas visitas do adversário, que são sorteadas, então o seu peso é ruidoso. O viés se desfaz com o número de visitas.

**Meta.** O sinal veio de 4 sementes de um T (a regra da Parte 64 pedia cautela) e se manteve na 5ª. Ainda é UM mecanismo, visto em dois T: fica como hipótese que o viés é sempre positivo neste jogo.

### P3013 — rodada 86

**Lógica.** A amostragem externa com o LCG, T = 3.000, em Python × Java: **IGUAIS, 4 linhas e 12 números bit a bit** ✅ (c). A rodada reproduz o módulo do pacote em **0 de 12** conjuntos diferentes ✅ (d).

O uniforme x/2³¹ é exato porque é um inteiro abaixo de 2³¹ dividido por uma potência de 2, então a comparação com σ(I) decide igual nas duas línguas. O verificador confere agora **86 rodadas** com par Python/Java (P2984).

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅. Parte 119: **4 testes, 0 erros**. Acumulado (mundo): **226 erros em 943 testes**. Calibração (P1961, Partes 80–119): **261/284 = 0,919**.

### Previsões sobre previsões (m)

Régua: P2837 (leitor v4).

| | faixa | medido | |
|---|---|---|---|
| (m1) | [4; 6] | 4 | ✅ |
| (m2) | [2; 3] | 2 | ✅ |
| (m3) | [0; 0,96] | 0,52 | ✅ |
| (m4) | [0,50; 1,00] | 1,00 | ✅ |
| (m5) | [0; 2] | 1 | ✅ |
| (m6) | [0; 1] | 0 | ✅ |

Previsões sobre previsões: **6 de 6**.

### Sobre mim

**"[0; 1] erros, centro 0,4": ✅ (0).**

## Engenharia reversa (metacognição)

**O padrão: quando a faixa é larga por honestidade, o centro acerta.**
- A (a) tinha meia-largura de 96%, porque a calibração mostrou 43% de dispersão entre sementes, e o medido caiu a 6% do centro.
- A (b) tinha o sinal do viés tirado de 4 sementes, e o sinal se manteve.

Nas duas, a largura veio da dispersão MEDIDA na calibração, e não da minha impressão. **Significado:** a parte difícil de prever não é o centro, é a largura. Quando eu meço a largura antes, ela deixa de ser um chute, e o (m3) desta parte (w mediano 0,52, o mais alto em várias partes) reflete isso. A largura alta não foi falta de conhecimento: foi conhecimento da dispersão.

**O segundo: um método mais esperto perdeu, e a previsão não disse nada sobre isso.** Eu não registrei a comparação externo contra acaso com o mesmo custo (1,9× pior), só a medi depois. É posterior e conta como hipótese (regra da Parte 25): no Kuhn, sortear o adversário não compensa. **Regra:** quando uma parte troca um método por outro, a comparação com o mesmo custo vai para o REGISTRO, com a unidade de custo escrita (aqui, nós visitados), e não para o texto depois.

**O terceiro: a regra da 118 (cada função nova com o seu teste) foi aplicada antes da suíte.** A `explorabilidade_externa` nasceu com o teste da calibração, e a p1871 não tem o que acusar.

## Síntese / unificação

- **O MCCFR com amostragem externa** (`synthai/mccfr_externo.py`) converge para o equilíbrio de Kuhn: explorabilidade 0,0102 em 50.000 iterações. O viés da média estocástica (a dama paga 0,3485) cai 3,9× por década.
- **Com o mesmo número de nós**, o externo explora 1,9× mais que a amostragem do acaso. Num jogo de 2 ações, sortear o adversário custa mais em variância do que economiza em nós. A vantagem do externo é de ESCALA, e fica para o Leduc.
- **Rodada 86:** IGUAL. O verificador confere 86 rodadas.

4/4 do mundo, 6/6 (m), calibração **0,919**.

## Meta

**Confiança.** Alta em (c) e (d). (a) e (b) acertaram com a calibração.

**Onde pode estar errado.** A comparação de custo conta nós da recursão, não tempo nem a memória dos conjuntos de informação. Num jogo grande, a unidade certa pode ser outra. E é UMA semente de teste.

**Pendência.** O Leduc (6 cartas, duas rodadas de aposta), onde a escala deveria inverter a comparação: que fique registrada ANTES, com a unidade de custo.

## Diálogo Python ↔ Java (rodada 86)

Ver `dialogo/DIALOGO.md`: a amostragem externa com o LCG é **IGUAL**, com 4 linhas e 12 números bit a bit.

## Fontes

- A amostragem externa e a média estocástica: [Lanctot, Waugh, Zinkevich e Bowling, "Monte Carlo Sampling for Regret Minimization in Extensive Games", NIPS 2009](https://proceedings.neurips.cc/paper/2009/hash/00411460f7c92d2124a67ea0f4cb5f85-Abstract.html) (lida na Parte 118, nesta mesma sessão) e a [versão corrigida no laboratório de Bowling](https://webdocs.cs.ualberta.ca/~bowling/publications/b2hd-09nips-mccfr-w-trws.html).
