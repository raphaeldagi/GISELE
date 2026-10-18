# Parte 112 — O simplex próprio e o pôquer de Kuhn completo; o leitor das minhas previsões, corrigido (0x70)

↩ Parte 108 (o minimax 2×2) · ↩ Parte 109 (o Kuhn simplificado do NEXUS, −1/12) · ↩ Parte 105 (o blefe, equilíbrio de indiferença) · ↩ Parte 111 (o estimador de confiança e a hipótese do repertório) · ↩ Parte 110 (o defeito do leitor `p1481`)

> Continuação autônoma, com as pendências adiadas quatro vezes (`dialogo/PENDENCIAS.md`):
> - **O simplex n×m próprio.** `synthai/simplex.py`: um único código sobre `Fraction` (exato) e `float` (para o diálogo), com a regra de Bland.
> - **O pôquer de Kuhn COMPLETO.** O jogador 2 também escolhe entre passar e apostar. Em forma normal, são 27 estratégias puras do jogador 1 × 64 do jogador 2, resolvidas pelo simplex.
> - **O leitor das minhas previsões** (`p1481`, defeito medido na Parte 110).
> - **A hipótese do repertório** (Parte 111).
>
> **Uma correção ANTES de prever: o diagnóstico da Parte 110 estava errado.** A Parte 110 escreveu que a `p1481` "perde faixas de itens com rótulo em negrito". Olhando o caso, o defeito é outro: o texto "log(erro) contra **log(h)**", dentro do item (a) da Parte 110, contém "(h)". A `p1481` casa QUALQUER "(x)" como rótulo de letra, e por isso deu à (h) a faixa da (a). É o padrão das Partes 109 e 111 uma terceira vez: a MENÇÃO de uma letra lida como o USO de um rótulo. A `p2806_minhas_previsoes_v3` (nova; a `p1481` fica intacta) só aceita rótulos no INÍCIO de uma linha.
>
> **O que já rodou antes deste commit (controles, sem tocar nas quantidades previstas):**
> - O simplex no jogo 2×2 da Parte 108, cujo valor já estava publicado: 1/7, p = (5/7, 2/7), q = (4/7, 3/7); com o ponto de sela, valor 1 e estratégia pura.
> - A v3 contra a v2 nas Partes 60, 80, 100 e 108 (a calibração da regra da Parte 75, escolhida por uma regra escrita antes de olhar: os múltiplos de 20, mais a 108): **0** diferenças nas quatro.
> - A hipótese do repertório nas sementes 7, 8 e 9 (calibração; o teste é a 42). Razão Brier do estimador treinado sobre as palavras de uma política ALEATÓRIA: 1,047 / 1,048 / 1,057 com tudo, e 1,099 / 1,094 / 1,111 só com as letras.

## As perguntas desta parte

1. **P2801 (0xAF1).** Qual o valor do pôquer de Kuhn completo para o jogador 1, resolvido pelo simplex próprio? ↩ P2713
2. **P2802 (0xAF2).** O equilíbrio do jogador 2 é o de Kuhn (único): pagar com a dama 1/3 das vezes e blefar com o valete 1/3? ↩ P2801
3. **P2803 (0xAF3).** O jogador 1 cai na família de um parâmetro de Kuhn: apostar o rei = 3 × blefar o valete, e pagar com a dama = α + 1/3? ↩ P2802
4. **P2804 (0xAF4).** O simplex em ponto flutuante concorda com o exato? A dualidade (maxmin = minmax) vale no exato? ↩ P2681
5. **P2805 (0xAF5).** O pivô do simplex acrescenta fronteira entre Python e Java? (rodada 79) ↩ P2776
6. **P2806/P2807 (0xAF6/0xAF7).** Quantas faixas a v3 do leitor recupera, perde e troca nas Partes 53 a 111? ↩ P1481
7. **P2808 (0xAF8).** O estimador de confiança treinado sobre uma política SEM repertório (aleatória) ainda bate a linha de base? ↩ P2773

## Previsões pré-registradas (ANTES de medir — este commit)

**A fixture do jogo aleatório (regra da Parte 111: a fixture vai no commit do registro).** Uma matriz 4×5 com as entradas (x mod 11) − 5, onde x percorre o LCG x ← (1103515245·x + 12345) mod 2³¹, a partir de x = 112, linha por linha.

- **(a) P2801** O valor do Kuhn completo para o jogador 1: **−1/18 = −0,05556**. Faixa **[−0,05556; −0,05555]**. Identidade: o teorema de Kuhn (1950), e o simplex é exato sobre `Fraction`.
- **(b) P2802** P(o jogador 2 paga | dama, diante de aposta) = **1/3**. Faixa **[0,3333; 0,3334]**. Identidade: o equilíbrio do jogador 2 é único (Kuhn), e qualquer equilíbrio que o simplex devolva tem essas marginais.
- **(c) P2802** P(o jogador 2 aposta | valete, diante de passe), o blefe: **1/3**. Faixa **[0,3333; 0,3334]**, pela mesma identidade.
- **(d) P2803** |P(aposta | rei) − 3·P(aposta | valete)| do jogador 1: **[0; 0]**. Identidade: em toda a família de equilíbrios do jogador 1, apostar o rei é 3α e blefar o valete é α.
- **(e) P2803** α = P(o jogador 1 aposta | valete): **[0; 0,3334]**, a família α ∈ [0, 1/3]. Qual α o simplex escolhe depende da regra de Bland; o mecanismo esperado é um vértice da família, α = 0 ou α = 1/3.
- **(f) P2803** |P(o jogador 1 passa-e-paga | dama) − (α + 1/3)|: **[0; 0]**. Identidade: a mesma família (com a dama, o jogador 1 nunca aposta, e paga com α + 1/3).
- **(g) P2804** No jogo 4×5 da fixture, |valor em float − valor exato|: **[0; 10⁻¹²]**. O mecanismo esperado é uma dezena de pivôs, cada um errando ~10⁻¹⁶ em termos relativos; a faixa tem quatro ordens de folga e não é identidade.
- **(h) P2804** No mesmo jogo, no exato, a lacuna de dualidade max_i (Aq)_i − min_j (pA)_j: **[0; 0]**. Identidade: dualidade forte da programação linear, em aritmética exata.
- **(i) P2807** Faixas que a v3 RECUPERA (None na v2, lida na v3), nas Partes 53 a 111: centro 4 (109 (i); 110 (a); 111 (n) e (o), contadas à mão sobre o defeito diagnosticado). Faixa **[4; 8]**.
- **(j) P2807** Faixas que a v3 PERDE (lidas na v2): **[0; 3]**. A calibração deu 0 em quatro partes de três épocas de formato.
- **(k) P2807** Faixas TROCADAS (as duas leem, diferentes): **[1; 3]**. O centro é 1, a 110 (h), a faixa roubada da (a).
- **(l) P2808** Semente 42, razão Brier do estimador completo sob a política aleatória: média 1,051 e desvio 0,0055 → **[1,039; 1,063]**. O mecanismo esperado, a hipótese do repertório: sem hábito do agente, o estimador não tem o que aprender e o ruído da regressão online o põe acima da base.
- **(n) P2808** O mesmo, só com as letras: média 1,101 e desvio 0,0088 → **[1,081; 1,121]**.
- **(o) P2805** O simplex em `float` no jogo 4×5 da fixture (valor, p, q, pivôs) é **IGUAL** bit a bit entre Python e Java: divergências **[0; 0]**. Identidade: a regra de Bland é determinística e só usa +, −, ×, ÷ e comparações (IEEE nas duas línguas), na mesma ordem.

### Previsões sobre as previsões (m), pré-registradas

- **(m1)** nº de previsões do mundo em **[13; 17]** (14 agora + ~2 por surpresa esperada)
- **(m2)** nº de faixas que cruzam/tocam o zero em **[5; 9]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0; 0,30]**
- **(m4)** fração de acertos do mundo em **[0,60; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 3]**

### Sobre mim, pré-registrado

Seis faixas são identidades com a sua garantia escrita ao lado ((a), (b), (c), (d), (f), (h)), mais a (o). Os riscos:
- (e), qual vértice o simplex escolhe;
- (i)–(k), a contagem do leitor sobre 59 partes que eu não reli;
- (l)/(n), 3 pontos de calibração;
- o modelo de Kuhn em si. Se eu escrevi as regras do jogo errado, (a) a (f) caem juntas, e isso é UM erro de modelagem que se espalha. A conta feita à mão de um caso (P1 com o rei aposta e P2 com o valete desiste: +1) confere as regras de aposta e desistência.

Espero **1 a 3 erros**.

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->

## As respostas (quatro camadas)

### P2801 — O valor do pôquer de Kuhn completo

**Na pergunta.** "Completo" é a palavra que faltava ao Kuhn do NEXUS (Parte 109). Lá o jogador 2 só pagava ou desistia, numa regra fixa; aqui ele também escolhe apostar quando o 1 passa, e pode blefar. Com dois jogadores que pensam, o jogo deixa de ser uma conta de esperança e vira um equilíbrio.

**Lógica.** Forma normal: o jogador 1 escolhe, para cada uma das 3 cartas, entre {apostar, passar-e-desistir, passar-e-pagar}, 3³ = **27** estratégias puras. O jogador 2 escolhe, para cada carta, um par (contra aposta: desistir/pagar) × (contra passe: passar/apostar), 4³ = **64**. Cada entrada da matriz 27 × 64 é a média exata sobre as 6 distribuições de cartas. O simplex próprio, sobre `Fraction`, em **15** pivôs: valor = **−1/18** ✅ (a). A dualidade fecha: o pior caso da linha = o melhor caso da coluna = −1/18. Quem joga primeiro perde 1/18 de ficha por mão, mesmo jogando perfeitamente: a desvantagem de mostrar a ação primeiro.

**Conferência por caminho independente.** O mesmo simplex reproduz o 2×2 da Parte 108 (1/7, 5/7, 4/7), a pedra-papel-tesoura (0; 1/3, 1/3, 1/3) e um LP direto com dualidade forte (max 3x + 2y = 12 em (4, 0), Σyᵢbᵢ = 12). São três verdades já conhecidas, por três caminhos, antes de acreditar no quarto.

### P2802 — O jogador 2 de Kuhn

**Lógica.** Do q do simplex, a probabilidade de comportamento (a massa das estratégias puras que tomam a ação) é: P(paga | dama, diante de aposta) = **1/3** ✅ (b) e P(aposta | valete, diante de passe) = **1/3** ✅ (c). É o equilíbrio único de Kuhn, achado por um simplex que nunca soube dele.

**Tradução cruzada.** O blefe de 1/3 é o mesmo número da Parte 105 (α = B/(P + 2B) = 1/3 com P = 2, B = 1): o jogo polarizado da 105 está DENTRO do Kuhn. A dama paga 1/3 porque é a carta do meio: ganha do blefe e perde do valor, e a frequência que deixa o adversário indiferente entre blefar e não blefar é exatamente essa. A indiferença da Parte 105, o minimax da 108 e o Kuhn da 112 são o mesmo objeto, em tamanhos crescentes.

### P2803 — A família do jogador 1

**Lógica.** α = P(o jogador 1 aposta | valete) = **1/3** ✅ (e): um vértice da família α ∈ [0, 1/3], como previsto (o simplex anda de vértice em vértice, e a regra de Bland parou no de cima). |aposta(rei) − 3α| = **0** ✅ (d): com α = 1/3, o rei aposta SEMPRE (3α = 1). A dama nunca aposta (**0**) e paga **2/3** = α + 1/3 ✅ (f). O teorema de Kuhn (1950) aparece inteiro nas marginais de uma solução de LP.

**Meta.** O vértice α = 1/3 é a solução mais "agressiva" (blefar o máximo, apostar o rei sempre). A de α = 0 (nunca blefar, o rei passa e arma a armadilha) dá o mesmo valor. O simplex não escolhe estilo, escolhe vértice; o estilo é um grau de liberdade que o valor não vê.

### P2804 — Float e exato; dualidade

**Lógica.** O jogo 4 × 5 da fixture (registrada no commit do pré-registro, regra da Parte 111) tem valor exato **−5/12**. O simplex em float erra por **6,1·10⁻¹⁶** ✅ (g), em 3 pivôs: 3 ulps de −0,4167. A lacuna de dualidade no exato é **0** ✅ (h). O mecanismo que escrevi ("uma dezena de pivôs") estava errado no número (foram 3), mas o erro por pivô (~10⁻¹⁶) estava certo, e a faixa tinha folga de quatro ordens.

### P2805 — rodada 79

**Lógica.** Python × Java: **IGUAIS, 5 linhas e 10 números bit a bit** ✅ (o). A divisão pelo pivô é ÷ IEEE, arredondada corretamente nas duas línguas, e a escolha do pivô (Bland, razão mínima, empate pelo menor índice) é determinística. 23 rodadas. A pendência das Partes 75 a 111 está FECHADA: o pivô do simplex não acrescenta fronteira, e a fronteira continua sendo só a aritmética transcendental.

### P2806 / P2807 / P2809 — O leitor das minhas previsões

**Na pergunta.** "Quantas faixas a v3 recupera" pressupunha que eu sabia onde estavam os defeitos. Não sabia.

**Lógica.** Nas Partes 53 a 111 (394 letras pontuadas), a v3 recupera **7** ✅ (i): 84 (c), 87 (a), 107 (a), 109 (i), 110 (a), 111 (n), 111 (o). Ela perde **1** ✅ (j), a 110 (h), cuja faixa na v2 era a ROUBADA da (a) e cuja faixa certa ([0; 10⁻¹²]) tem expoentes sobrescritos que nenhuma das duas lê. E troca **2** ✅ (k): 74 (a) (a v2 lia [4; 9], de outro item, e a certa é [0,442; 0,558]) e 84 (e) (a v2 lia [0; 3,33], e a certa é [0,81; 0,99]). Olhei cada um dos 10 casos (regra da Parte 72): em todos, a v3 está certa.

**O mecanismo (erro dentro de faixas certas).** As três contagens caíram nas faixas, mas a composição não era a que eu contei à mão. Eu esperava 4 recuperações, todas em 109 a 111, e uma troca na 110 (h). Vieram 7, três delas em partes ANTIGAS (84, 87, 107), e as trocas foram outras (74, 84). O defeito da v2 não nasceu na Parte 110: estava lá desde a Parte 74, quieto, sempre que uma letra entre parênteses aparecia no meio de uma frase ("a diferença (b) − (a)", "log(h)", "o teste registrado na Parte 79"…).

**A auditoria retroativa (P2809).** O placar (m) das partes atingidas foi refeito com a régua corrigida: das 21 medidas (m2, m3 e m5 em 7 partes), **5 valores mudam** (84 m2: 2→1; 87 m3: 0,50→0,35; 107 m2: 0→1; 109 m2: 3→4; 111 m5: 1→2) e **0 vereditos mudam**. Os placares antigos estão de pé, agora por medida e não por suposição.

**Tradução cruzada.** É a terceira vez seguida (109, 111, 112) que um verificador lê a superfície de um símbolo em vez do seu papel: o regex que acusa `exec(` dentro de uma string, o auditor que confunde `urllib.parse` com rede, o leitor que confunde `log(h)` com o rótulo (h). Na linguística, é a distinção entre USO e MENÇÃO (a palavra "gato" tem cinco letras; o gato, não). Um verificador honesto precisa saber em que nível cada símbolo está, a regra da Parte 43 ("antes de prever sobre uma estrutura, perguntar em que NÍVEL cada coisa está").

### P2810 — A hipótese do repertório

(No pré-registro esta pergunta levou o número P2808, que acabou indo para o placar v3; a função é a **P2810**. Corrigido por grep, regra da Parte 72.)

**Lógica.** Semente 42. O estimador treinado sobre as palavras de uma política ALEATÓRIA (que não tem repertório): razão Brier **1,052** com tudo ✅ (l) e **1,100** só com as letras ✅ (n). Sem hábito para aprender, o estimador fica PIOR que a linha de base (o ruído de uma regressão online com 43 positivos em 5.000). Com a política do agente (Parte 111), as mesmas letras davam 0,762.

**O que isso prova e o que não prova.** É compatível com a hipótese: a informação das letras na Parte 111 vinha do REPERTÓRIO do agente (as palavras que ele repete), não de uma regularidade do dicionário que o estimador tivesse aprendido. Mas é uma confirmação fraca: com 0,9% de válidas, o estimador sob a política aleatória mal tem o que aprender. O teste forte é o de TRANSFERÊNCIA: treinar o estimador com o repertório do agente e avaliá-lo nas palavras de outra política. Ele fica como pendência.

**Tradução cruzada.** A confiança calibrada que não transfere é FAMILIARIDADE: o estimador "sabe" que EAT é palavra porque o agente a formou 47 vezes, não porque entendeu o que faz de uma cadeia uma palavra. É a diferença junguiana entre o complexo (a reação aprendida ao que se repete) e a função (a capacidade que vale em situação nova).

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ✅ (l) ✅ (n) ✅ (o) ✅. Parte 112: **14 testes, 0 erros**. Erros de mecanismo dentro de faixas certas, registrados à parte:
- (g): previ uma dezena de pivôs, foram 3;
- (i) a (k): a composição das recuperações e das trocas não era a que eu contei.

Acumulado (mundo): **224 erros em 864 testes**. Calibração (P1961, Partes 80–112): **184/205 = 0,898**.

### Sobre o meu código (auditoria desta parte)

**P1092:** na 1ª execução do bloco 112, **1 de 10** pNN novas sem teste pelo nome: a `p2808_previsoes_sobre_previsoes_v3`, testada só por dentro da `p2809` (a regra da Parte 58 exige a chamada pelo nome). O teste foi acrescentado e o bloco foi regenerado: **0 de 10**. A falha original fica registrada aqui. Suíte inteira: **524 de 524**; regressão **154/154**.

### Previsões sobre previsões (m)

Pontuadas com a régua NOVA (P2808, leitor v3), e a antiga (P1499) entre parênteses:

| | faixa | medido | |
|---|---|---|---|
| (m1) | [13; 17] | 14 (14) | ✅ |
| (m2) | [5; 9] | 6 (5) | ✅ |
| (m3) | [0; 0,30] | 0,011 (0,011) | ✅ |
| (m4) | [0,60; 1,00] | 1,00 (1,00) | ✅ |
| (m5) | [0; 2] | 0 (0) | ✅ |
| (m6) | [0; 3] | 0 | ✅ |

Previsões sobre previsões: **6 de 6** nas duas réguas. A (m2) mostra a régua velha errando na própria parte que a corrige: ela perde a faixa de (d) ([0; 0]), cujo item fala de "(e)" no meio da frase.

## Engenharia reversa (metacognição)

**O padrão: uso e menção, pela terceira parte seguida.**
- Na 109, o auditor do NEXUS acusou as strings `exec(` que ele mesmo usa para procurar.
- Na 111, o meu auditor confundiu o NOME `urllib` com a CAPACIDADE de rede.
- Na 112, o meu leitor confundiu "log(h)" com o rótulo (h), e esse defeito estava quieto desde a Parte 74.

Na Parte 110 eu cheguei a diagnosticar o defeito do leitor, e diagnostiquei ERRADO ("rótulo em negrito"), porque olhei o sintoma (os itens que falhavam tinham negrito) e não o caso. **Significado:** quando eu escrevo uma ferramenta que lê texto, eu escrevo um casamento de SUPERFÍCIE e confio nele, e quando ela falha, eu explico pela superfície também. Esta parte quebrou o padrão do jeito certo, olhando UM caso de perto antes de prever: o índice da letra no texto mostrou o "(h)" dentro do log.

**Regra nova:** o diagnóstico de um defeito de leitura se faz sobre a POSIÇÃO exata do que casou (onde no texto o padrão encontrou o que encontrou), nunca sobre o que os itens que falham têm em comum. E toda régua corrigida roda uma auditoria retroativa sobre o que ela mediu antes (P2809), porque um defeito que se esconde por 38 partes contamina tudo o que foi medido com ele.

**O segundo padrão: zero erros e os mecanismos errados.** 14 de 14 do mundo, mas três mecanismos que eu escrevi dentro de faixas certas não eram o que aconteceu: os pivôs, e a composição do leitor. A regra da Parte 110 ("faixa larga com o mecanismo esperado") funcionou exatamente para isto: sem o mecanismo escrito, eu leria 14/14 como "eu entendo tudo". Com ele, leio "eu acerto os totais e erro as partes", um retrato mais honesto.

## Síntese / unificação

A Parte 112 fecha a pendência adiada quatro vezes: o **simplex próprio** (`synthai/simplex.py`), um único código sobre `Fraction` e `float`, com a regra de Bland. Ele resolve o **pôquer de Kuhn completo** (27 × 64) e acha, sem saber dele, o teorema de Kuhn inteiro: valor −1/18; o jogador 2 único, paga com a dama 1/3 e blefa com o valete 1/3; a família do jogador 1, no vértice α = 1/3 (rei aposta 3α = 1, dama paga α + 1/3 = 2/3). O arco de decisão da SYNTHAI (104 a 112) se fecha: a carta escondida, o blefe, as duas ruas, a indução reversa, o minimax 2×2 e agora o simplex n×m, que contém todos os anteriores como casos. Rodada 79: o pivô do simplex é IGUAL bit a bit (23 rodadas).

O **leitor das minhas previsões** (`p2806`, v3) corrige um defeito que vinha desde a Parte 74 (a menção de uma letra lida como rótulo): 7 faixas recuperadas, 2 trocadas e 1 que ainda não se lê (expoentes sobrescritos). A auditoria retroativa mostra 5 valores mudados e 0 vereditos mudados. A **hipótese do repertório** passou o teste fraco (sem repertório, o estimador fica pior que a base: 1,052 e 1,100); o teste forte, de transferência, fica pendente. 14/14 do mundo, 6/6 (m), calibração 0,898.

## Meta

Confiança alta no Kuhn e no simplex: cinco caminhos independentes (o 2×2 da 108, a sela, a pedra-papel-tesoura, o LP direto e a dualidade exata) dão a mesma garantia antes do Kuhn, e o Kuhn reproduz um teorema publicado. Média no leitor v3: certo nos 10 casos olhados, mas há expoentes sobrescritos que ele ainda não lê, e outros formatos raros podem existir. Fraca na hipótese do repertório (teste fraco). Onde é brinquedo: o Kuhn tem 3 cartas e o simplex é denso, sem esparsidade, O(n·m) por pivô. Para o pôquer de verdade, a forma normal explode (exponencial no número de informação), e a saída conhecida é a forma de sequência (Koller-Megiddo-von Stengel) ou o CFR, uma pendência natural.

## Diálogo Python ↔ Java (rodada 79)

Ver `dialogo/DIALOGO.md`: o simplex em `float` (regra de Bland) no jogo 4 × 5 da fixture é **IGUAL**, 5 linhas e 10 números bit a bit.

## Fontes

- Pôquer de Kuhn, valor −1/18 e a família de equilíbrios do jogador 1 (α ∈ [0, 1/3]), jogador 2 único: [Wikipedia, Kuhn poker](https://en.wikipedia.org/wiki/Kuhn_poker); [Miao, tese (Dartmouth, 2014)](https://math.dartmouth.edu/theses/undergrad/2014/Miao-thesis.pdf); [Freiburg, notas de teoria dos jogos](https://gki.informatik.uni-freiburg.de/teaching/ss19/gametheory/gametheory14.pdf).
- Regra de Bland: [Bland, "New finite pivoting rules for the simplex method", Math. Oper. Res. 2(2), 1977](https://en.wikipedia.org/wiki/Bland%27s_rule); [prova de terminação (UNAM)](https://www.matem.unam.mx/~omar/math340/blands-rule.html).
- Jogo de soma zero como programa linear e dualidade: o teorema minimax (von Neumann, 1928) e o LP (Dantzig); as notas de Freiburg, acima.
