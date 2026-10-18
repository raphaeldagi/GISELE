# Parte 113 — O arrependimento: CFR no pôquer de Kuhn, o teste forte do repertório e o leitor v4 (0x71)

↩ Parte 112 (o Kuhn completo pelo simplex) · ↩ Parte 108 (o jogo fictício: aprender jogando) · ↩ Parte 111 (o estimador de confiança) · ↩ Parte 110 (os expoentes sobrescritos que o leitor não lê)

> Continuação ("Continue sem parar"), com as três pendências que a Parte 112 abriu (`dialogo/PENDENCIAS.md`, rodada 80):
> - **(1) CFR, o Kuhn sem a forma normal.** O simplex da 112 montou a matriz 27×64; o pôquer real explode nessa forma. O CFR (Counterfactual Regret Minimization, Zinkevich et al. 2007) aprende jogando contra si mesmo, conjunto de informação por conjunto de informação, e a estratégia MÉDIA converge para um equilíbrio (`synthai/cfr.py`, determinístico, as 6 distribuições enumeradas).
> - **(2) O teste FORTE da hipótese do repertório (transferência).**
> - **(3) O leitor das minhas previsões, v4, com expoentes sobrescritos.**
>
> **A calibração, rodada ANTES deste registro, em casos que não são o teste:**
> - **CFR em T = 100, 200, 400 e 800 iterações.** A explorabilidade da estratégia média foi 0,0466 / 0,0239 / 0,0222 / 0,0161, com inclinação log-log **−0,47** (t = −4,03, então |t| > 2: a regra da Parte 71 permite extrapolar). A extrapolação para T = 10.000 dá 0,0047. Nas mesmas iterações, α = P(o jogador 1 blefa com o valete) ficou em 0,21 / 0,19 / 0,21 / 0,22, dentro da família de Kuhn e longe dos vértices; e os erros das marginais caíram com oscilação (de 0,10 a 0,003).
> - **A transferência nas sementes 7, 8 e 9.** A AUC das válidas VISTAS (o repertório) contra as inválidas foi 0,89 / 0,79 / 0,68; a das válidas NOVAS, 0,60 / 0,73 / 0,59.
> - **O leitor v4 na Parte 110 (onde conheço os casos).** Recupera (c), (h) e (i), os três de expoente sobrescrito. E o controle: a v4 com o leitor de números VELHO é idêntica à v3.

## As perguntas desta parte

1. **P2831 (0xB0F).** O CFR converge para o equilíbrio de Kuhn sem a forma normal? Com que velocidade, e que explorabilidade deixa em T = 10.000? ↩ P2801
2. **P2832 (0xB10).** Que equilíbrio da família o CFR escolhe? O simplex parou num vértice (α = 1/3); o CFR, que faz MÉDIA, também? ↩ P2803
3. **P2835 (0xB13).** O estimador de confiança treinado no repertório do agente TRANSFERE para palavras que o agente nunca formou? ↩ P2810
4. **P2833/P2834 (0xB11/0xB12).** Quantas faixas o leitor v4 recupera? ↩ P2806
5. **P2836 (0xB14).** O CFR acrescenta fronteira entre Python e Java? (rodada 80) ↩ P2805

## Previsões pré-registradas (ANTES de medir — este commit)

**As fixtures (regra da Parte 111).**
- CFR vanilla, simultâneo, com arrependimento e soma da estratégia acumulados por conjunto de informação, `CFR().iterar(10000)`.
- A transferência roda nas sementes **42 a 51** (dez sementes novas), com `transferencia_do_estimador(Config(seed=s), embutido)`: 5.000 episódios de treino; teste com 5.000 episódios de uma política aleatória em grades da semente + 200.000.
- O leitor compara a v3 (P2806) com a v4 (P2833) nas Partes 53 a 112.

**CFR (P2831/P2832), T = 10.000.**
- **(a)** Explorabilidade da estratégia média: centro 0,0047 pela extrapolação. A meia-largura em log é 1,645 × √(0,41² + 0,2²) × 1,36 ≈ 1,0, um fator de ~2,8 para cada lado: **[0,0017; 0,013]**. Mecanismo esperado (a faixa passa de duas ordens? não, mas é larga): a cota O(1/√T) do arrependimento médio.
- **(b)** |valor da estratégia média − (−1/18)|: **[0; 0,013]**. Identidade: o valor do perfil e o do equilíbrio estão ambos entre as duas melhores respostas, então a distância entre eles é ≤ explorabilidade; o teto é o da faixa (a).
- **(c)** |P(o jogador 2 paga com a dama) − 1/3|: **[0; 0,03]** (a calibração caiu de 0,10 a 0,003; a escala 1/√T dá ~0,01).
- **(d)** |P(o jogador 2 blefa com o valete) − 1/3|: **[0; 0,03]**.
- **(e)** α = P(o jogador 1 aposta com o valete): **[0,15; 0,30]**. Mecanismo esperado: o CFR faz MÉDIA de estratégias, e a média de pontos da família é um ponto INTERIOR. Ao contrário do simplex, que anda de vértice em vértice e parou em α = 1/3.
- **(f)** |P(aposta | rei) − 3α|: **[0; 0,03]**.
- **(g)** |P(o jogador 1 passa e paga | dama) − (α + 1/3)|: **[0; 0,03]**.

**Transferência (P2835), média sobre as sementes 42 a 51.**
- **(h)** AUC das válidas NOVAS: calibração 0,643, desvio entre sementes 0,075, faixa 0,643 ± 1,645 × 0,075/√10 × 1,36 = **[0,59; 0,70]**. Acima de 0,5: as letras levam ALGUMA regularidade que transfere.
- **(i)** AUC(vistas) − AUC(novas), média das sementes que têm vistas: calibração 0,143, desvio 0,124, faixa **[0,055; 0,23]**. Acima de 0: o repertório acrescenta além disso. A hipótese da Parte 111 fica PARCIAL: repertório e regularidade, os dois.

**Leitor v4 (P2834), Partes 53 a 112.**
- **(j)** Faixas recuperadas: as 3 da 110, mais as que existirem com sobrescrito em outras partes, **[3; 8]**.
- **(k)** Faixas perdidas: **[0; 0]**. Identidade: o `_numero_pt_v2` delega ao original em qualquer texto sem expoente sobrescrito, e o original devolve None em qualquer texto com expoente sobrescrito; então nenhum número que a v3 lia muda nem some.
- **(l)** Faixas trocadas: **[0; 0]**, pela mesma identidade.

**Diálogo (P2836).**
- **(n)** O CFR em `float`, T = 1.000 (as 24 probabilidades médias), é **IGUAL** bit a bit entre Python e Java: **[0; 0]**. Identidade: só +, −, ×, ÷ e comparações (o max(0, ·) do casamento de arrependimento é uma comparação), na mesma ordem de recursão e de soma nas duas línguas.

### Previsões sobre as previsões (m), pré-registradas (régua: o leitor v4, P2833)

- **(m1)** nº de previsões do mundo em **[12; 16]** (13 agora + ~2 por surpresa)
- **(m2)** nº de faixas que cruzam/tocam o zero em **[6; 10]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0,20; 0,70]**
- **(m4)** fração de acertos do mundo em **[0,60; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 4]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 3]**

### Sobre mim, pré-registrado

Os riscos estão onde a calibração é ruidosa. As marginais (c), (d), (f), (g) oscilam e não caem de forma monótona. (e) aposta que o CFR para no interior. (h)/(i) têm de 8 a 42 positivos por semente. (j) é uma contagem sobre partes que não reli. As identidades (b), (k), (l) e (n) têm a garantia escrita. Espero **1 a 3 erros**, nas marginais ou em (i).

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->

## As respostas (quatro camadas)

### P2831 — O CFR converge para Kuhn sem a forma normal?

**Na pergunta.** "Sem a forma normal" é o ponto. A Parte 112 escreveu as 27 × 64 = 1.728 combinações de estratégias puras; o CFR nunca as escreve. Ele guarda dois números por conjunto de informação (12 conjuntos × 2 ações = 24 arrependimentos) e aprende jogando contra si mesmo. É a diferença entre listar todas as estradas e aprender a dirigir.

**Lógica.** O casamento de arrependimento joga cada ação com probabilidade proporcional ao arrependimento POSITIVO acumulado de não tê-la jogado, R⁺(a)/ΣR⁺. Depois de T = 10.000 iterações (as 6 distribuições enumeradas em cada uma), a explorabilidade da estratégia MÉDIA é **0,00297** ✅ (a), dentro de [0,0017; 0,013]. A extrapolação da calibração (inclinação −0,47) previa 0,0047; o medido ficou 1,6× abaixo, dentro do fator 2,8 da faixa. Pela cota O(1/√T), de T = 800 (0,0161) para T = 10.000 a explorabilidade cairia √(10.000/800) = 3,5 vezes, para 0,0046; caiu 5,4 vezes. A convergência real está um pouco mais rápida que a cota, como costuma acontecer no CFR. O valor do perfil médio é **−0,055531**, a **2,5·10⁻⁵** de −1/18 ✅ (b), bem abaixo do teto que a identidade garante (|v − v*| ≤ explorabilidade = 0,003).

**Tradução cruzada.** O arrependimento é uma emoção com conta. "Se eu tivesse apostado, teria ganho mais" vira um número que se acumula, e a escolha seguinte pende para o que se lamenta não ter feito. Jung chamaria de compensação: a função que ficou de fora volta pelo lamento. A estratégia média, a que converge, é a lição tirada de todos os lamentos juntos, não o último impulso.

### P2832 — Que equilíbrio o CFR escolhe?

**Lógica.** O jogador 2 converge para o equilíbrio ÚNICO de Kuhn: paga com a dama **0,3371** (erro **0,0038**) ✅ (c) e blefa com o valete **0,3357** (erro **0,0024**) ✅ (d). O jogador 1 para em α = **0,2159** ✅ (e), um ponto INTERIOR da família α ∈ [0, 1/3]. O simplex da Parte 112 tinha parado no vértice α = 1/3. As relações da família valem: |aposta(K) − 3α| = **0,0208** ✅ (f) (o rei aposta **0,668**, contra 3α = 0,648: a relação mais lenta a convergir. No rascunho eu tinha escrito 0,627, deduzido de cabeça a partir do |erro| com o sinal chutado; a linha de código da regra da Parte 69 pegou o sinal trocado antes do commit) e |paga(Q) − (α + 1/3)| = **0,0047** ✅ (g).

**Por quê interior.** O simplex anda pelas ARESTAS do poliedro das estratégias e para num canto. O CFR faz a MÉDIA das estratégias que jogou, e a média de pontos de um conjunto convexo cai no seu interior. Os dois acham o mesmo valor (−1/18) e o mesmo jogador 2. Mas são "personalidades" diferentes do jogador 1: o simplex blefa no máximo (α = 1/3, o rei sempre aposta); o CFR blefa 22% e às vezes passa com o rei para armar a armadilha. O valor do jogo não distingue os dois; o estilo é o grau de liberdade que o valor não vê (a Parte 112 disse isso; esta parte mediu).

### P2835 — O estimador transfere?

**Lógica.** Nas dez sementes novas (42 a 51), o estimador só de letras, treinado no repertório do agente e congelado, avaliado nas palavras de uma política aleatória:
- **AUC das válidas NOVAS** (que o agente nunca formou) contra as inválidas: **0,621** ✅ (h). Acima de 0,5: as letras levam uma regularidade que TRANSFERE.
- **AUC(vistas) − AUC(novas): 0,163** ✅ (i), em 10 de 10 sementes com vistas. O repertório acrescenta além disso.

**O veredito sobre a hipótese da Parte 111.** É PARCIAL, e foi previsto parcial: as duas causas são reais. As letras sabem alguma coisa do dicionário (palavras curtas de letras frequentes, vogais no meio), e sabem mais sobre as palavras que o agente repete. Na Parte 111 eu tentei uma causa só, duas vezes, e errei duas vezes. Aqui, com o desenho que separa as duas (vistas × novas), as duas aparecem com tamanho medido: 0,12 acima do acaso pela regularidade e mais 0,16 pelo repertório.

**Tradução cruzada.** É a diferença entre a familiaridade e o conhecimento, medida em vez de dita. O estimador conhece as palavras de casa (0,78 em média nas vistas) e reconhece um pouco as de fora (0,62). Um sistema que só tivesse a primeira coisa seria um papagaio; um que só tivesse a segunda, um linguista. Este é os dois, numa proporção que agora tem número.

### P2833 / P2834 / P2838 — O leitor v4

**Lógica.** O `_numero_pt_v2` lê potências com expoente sobrescrito ("10⁻¹²", "5·10⁻⁴", "6,1·10⁻¹⁶", "2⁻⁵⁴"), e o leitor v4 recupera **6** faixas ✅ (j): 70 (g), do diálogo, [3·10⁴; 10⁶]; 77 (d), [0; 1·10⁻¹²]; 110 (c), (h) e (i); e 112 (g), a [0; 10⁻¹²] da parte anterior. Ele perde **0** ✅ (k) e troca **0** ✅ (l), como garantiam as duas identidades. Olhei os três casos que eu não conhecia (70 g, 77 d, 112 g): todos certos. O controle dos dois lados: com o leitor velho, a v4 é exatamente a v3, e com o novo ela acha os casos plantados (os três da 110).

**A auditoria retroativa (P2838, regra da Parte 112).** No placar (m) das partes atingidas (77, 110, 112; a 70 não tinha (m) no formato lido), **5 valores mudam** (77 m2: 0→1; 110 m2: 3→4, m3: 0,028→0,050, m5: 0→2; 112 m2: 6→7). No rascunho eu escrevi "4" e listei cinco: uma contagem por leitura, a regra da Parte 60, pega pela suíte inteira e **0 vereditos mudam**. E fica um limite medido: na Parte 77, nenhuma das réguas consegue ler a (m3); aquele veredito não é auditável por código.

### P2836 — rodada 80

**Lógica.** O CFR em float (T = 1.000), Python × Java: **IGUAIS, 4 linhas e 12 números bit a bit** ✅ (n). O casamento de arrependimento é uma comparação (max(0, ·)) e uma divisão; a recursão segue a mesma ordem nas duas línguas. 24 rodadas: aprender jogando, como resolver por simplex, é aritmética portável.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ✅ (l) ✅ (n) ✅. Parte 113: **13 testes, 0 erros**. Os mecanismos escritos dentro das faixas largas, conferidos:
- (a): a cota O(1/√T); a convergência real foi mais rápida, 5,4× contra 3,5×;
- (e): o interior, confirmado;
- (h)/(i): as duas causas, confirmadas.

Acumulado (mundo): **224 erros em 877 testes**. Calibração (P1961, Partes 80–113): **197/218 = 0,904**.

### Previsões sobre previsões (m)

Pontuadas com o leitor v4 (P2837); a v3 dá os mesmos números nesta parte.

| | faixa | medido | |
|---|---|---|---|
| (m1) | [12; 16] | 13 | ✅ |
| (m2) | [6; 10] | 8 | ✅ |
| (m3) | [0,20; 0,70] | 0,45 | ✅ |
| (m4) | [0,60; 1,00] | 1,00 | ✅ |
| (m5) | [0; 4] | 2 | ✅ |
| (m6) | [0; 3] | 0 | ✅ |

Previsões sobre previsões: **6 de 6**.

## Engenharia reversa (metacognição)

**O padrão: o sinal chutado.** O único erro desta parte não chegou ao placar, porque a regra da Parte 69 o pegou antes do commit. Eu tinha o |erro| (0,0208) e escrevi o valor do rei como 3α − 0,021 = 0,627, sem olhar o sinal. O rei aposta 0,668. É o mesmo erro da Parte 53 ("tabelas comprimem pior", o sinal trocado) e do "esqueço custos" da Parte 45: quando eu tenho o TAMANHO de uma diferença, eu ponho um sinal por hábito. Aqui o hábito era "a relação mais lenta fica abaixo". **Significado:** uma magnitude não é um número; o sinal é uma segunda medida, que eu tenho de fazer. **Regra:** toda grandeza que eu reconstruo de um valor absoluto (|a − b|) volta à saída que a imprimiu, e o sinal sai de lá.

**O segundo padrão: o desenho que separa as causas.** Na Parte 111 eu expliquei o estimador por uma causa, duas vezes, e errei duas vezes. Na 112 testei UMA causa (o teste fraco). Nesta, o desenho (vistas × novas, numa amostra que o agente não gerou) mede as duas causas de uma vez, cada uma com o seu tamanho, e a previsão acertou porque foi registrada como "as duas". **Significado:** a pergunta "qual é a causa?" pressupõe que haja uma; o desenho experimental certo pergunta "quanto de cada uma?". **O terceiro, achado pela suíte inteira depois do texto pronto.** Duas falhas, as duas MINHAS.
- Escrevi "4 valores mudam" e listei cinco, uma contagem por leitura (a regra da Parte 60, pela enésima vez).
- A auditoria da Parte 81 (`p1871`, o que não serve) acusou `simplex.valor_contra`, uma função da Parte 112 que nada usava. Ela passou na suíte da 112 porque a auditoria só vê arquivos que o `git ls-files` conhece, e a suíte rodou ANTES do `git add` do arquivo novo.

A função agora serve à identidade do minimax (p·A·q = v no equilíbrio), num teste. **Regra:** os arquivos novos são postos no índice do git (`git add`) ANTES da suíte inteira, porque uma auditoria que lê o repositório não vê o que ainda não está nele.

**Regra:** quando duas explicações de causa única já falharam, o próximo teste é um desenho que mede cada causa separadamente, e não uma terceira causa única.

## Síntese / unificação

A Parte 113 fecha as três pendências da 112:
- **(1) O CFR** (`synthai/cfr.py`) resolve o pôquer de Kuhn sem montar a forma normal: 24 arrependimentos em vez de 1.728 células. A explorabilidade cai 5,4× de T = 800 para T = 10.000 (a cota O(1/√T) previa 3,5×), e o valor fica a 2,5·10⁻⁵ de −1/18. O jogador 2 é o único de Kuhn (dama paga 0,337, valete blefa 0,336). O jogador 1 para no INTERIOR da família (α = 0,216), onde o simplex parou no vértice (α = 1/3): mesmo valor, outro estilo.
- **(2) O teste forte do repertório** separa as duas causas da Parte 111. A regularidade das letras transfere (AUC das novas 0,621, 0,12 acima do acaso) e o repertório acrescenta 0,163, em 10 de 10 sementes.
- **(3) O leitor v4** lê expoentes sobrescritos: 6 faixas recuperadas, 0 perdidas e 0 trocadas (identidades), e 5 valores (m) antigos mudados sem nenhum veredito mudado.

Rodada 80: o CFR é IGUAL bit a bit (24 rodadas). 13/13 do mundo, 6/6 (m), calibração **0,904**: o primeiro valor acima de 0,9 desde a medida da Parte 79.

O arco de decisão da SYNTHAI agora tem os dois caminhos para o mesmo equilíbrio: o exato, que monta e resolve (simplex, Parte 112), e o aprendido, que joga e lamenta (CFR, Parte 113). Os dois concordam no valor e no jogador 2, e discordam, mensuravelmente, no estilo do jogador 1. É a prova cruzada da Parte 20 (dois caminhos independentes) e a AUTOPOIESE da Parte 31 (substituir aprendizado por conta exata "se der"): aqui dá, e o aprendizado chega ao mesmo lugar, só que pelo meio.

## Meta

Confiança alta no CFR: o controle com o perfil de Kuhn escrito à mão vale −1/18 com explorabilidade < 10⁻¹², e um perfil sujo (o jogador 2 sempre paga) é explorável em mais de 0,01. Média na transferência: dez sementes, mas só 20 a 36 palavras novas por semente; e a "regularidade" (0,12) pode ser a das palavras de 3 letras feitas de letras frequentes, que é também o que um dicionário pequeno contém (o juiz de novo, como na Parte 111). Onde é brinquedo: o Kuhn tem 12 conjuntos de informação, e o pôquer de verdade tem 10¹² ou mais. Lá o CFR precisa de amostragem (MCCFR) e de abstração, uma pendência natural. O leitor v4 ainda não lê a (m3) da Parte 77.

## Diálogo Python ↔ Java (rodada 80)

Ver `dialogo/DIALOGO.md`: o CFR em `float`, T = 1.000, é **IGUAL**: 4 linhas e 12 números bit a bit.

## Fontes

- CFR: [Zinkevich, Johanson, Bowling e Piccione, "Regret Minimization in Games with Incomplete Information", NIPS 2007](https://proceedings.neurips.cc/paper/2007/hash/08d98638c6fcd194a4b1e6992063e944-Abstract.html); [o artigo em PDF](https://proceedings.nips.cc/paper_files/paper/2007/file/08d98638c6fcd194a4b1e6992063e944-Paper.pdf); [relatório técnico longo TR07-14 (Alberta)](https://era.library.ualberta.ca/files/vh53wx015/TR07-14.pdf).
- Pôquer de Kuhn e a família de equilíbrios: [Wikipedia, Kuhn poker](https://en.wikipedia.org/wiki/Kuhn_poker); [Miao, tese (Dartmouth, 2014)](https://math.dartmouth.edu/theses/undergrad/2014/Miao-thesis.pdf).
- A AUC como estatística de Mann-Whitney (a probabilidade de um positivo ter nota maior que um negativo): resultado clássico (Hanley e McNeil, 1982), conferido aqui pelos casos de teste em `synthai/testes_parte113.py`.
