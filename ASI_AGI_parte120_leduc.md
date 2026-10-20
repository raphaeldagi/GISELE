# Parte 120 — O pôquer Leduc: CFR, acaso e amostragem externa num jogo 48 vezes maior (0x78)

↩ Parte 119 (a amostragem externa no Kuhn) · ↩ Parte 118 (o acaso amostrado) · ↩ Parte 113 (o CFR vanilla) · → Parte 121 (o NEXUS 2.2.0, feita antes desta)

> **Continuação autônoma, retomada depois do "Pare" e do "CONTINUE" do usuário.** A Parte 119 deixou uma regra e uma pendência.
> - **A regra:** comparar métodos com o MESMO custo, com a unidade escrita.
> - **A pendência:** sortear o adversário só compensa com muitas ações, isto é, em escala.
>
> O Leduc (Southey et al., 2005) é o próximo degrau. Tem 6 cartas e uma carta pública, e são 288 conjuntos de informação contra os 12 do Kuhn. A Parte 121 foi feita antes desta, com a rodada 87, então esta usa a rodada 88.
>
> **Antes do registro (conferências, não previsões).**
> - **As regras:** foram conferidas à mão em `synthai/testes_parte120.py`, no commit fe6af21. São 144 + 144 conjuntos.
> - **A calibração** (regras das Partes 62 a 64), na unidade de custo NÓS (chamadas da recursão):
>   - **Nós por iteração:** vanilla 10.200, acaso 85, externo ~36,96.
>   - **Sementes de calibração:** 1201 e 1203.
>   - **Explorabilidade:**
>
>     | Nós | Vanilla | Acaso (1201 / 1203) | Externo (1201 / 1203) |
>     |---|---|---|---|
>     | 200 mil | 0,3669 | 0,5376 / 0,5050 | 0,3645 / 0,4844 |
>     | 2 milhões | 0,0724 | 0,1108 / 0,1114 | 0,0877 / 0,0955 |
>
>   - **Razão por década:** vanilla 5,07; acaso 4,85 e 4,53; externo 4,16 e 5,07.
>   - **Valor do jogo para o jogador 1, pelo vanilla:**
>     - −0,14785 em 20 iterações;
>     - −0,08578 em 196 iterações, com melhor resposta de cada lado em [−0,11586; −0,04348].
> - **O mecanismo da calibração está presente no teste?** Sim: o mesmo jogo, os mesmos amostradores e a mesma variável (nós). As sementes do teste são 1202 e 1204, nunca olhadas.
> - **Fumaça antes do registro, declarada:** rodei uma vez o lado Python da rodada 88 (`dialogo/rodada88.py`) e vi as primeiras e as últimas linhas da estratégia em hexadecimal. Não rodei o Java, a comparação nem nenhum experimento de 20 milhões de nós. As previsões (h) e (i) são identidades e não dependem desses números.

## As perguntas desta parte

1. **P3041 (0xBE1).** Em 20 milhões de nós, quanto cede a estratégia média de cada método (vanilla, acaso e externo)? ↩ P3012
2. **P3042 (0xBE2).** Com o MESMO custo, a amostragem externa ganha do acaso no Leduc, onde há até 3 ações? E o vanilla ganha dos dois? ↩ P3012
3. **P3043 (0xBE3).** O CFR vanilla no Leduc (cadeias, frações de pote e 288 conjuntos) acrescenta fronteira entre Python e Java? (rodada 88) ↩ P3013

## Previsões pré-registradas (ANTES de medir — este commit)

**As fixtures (neste commit):** `synthai/leduc.py` (fe6af21), `dialogo/rodada88.py` e `dialogo/Rodada88.java`.
- **O teste:** 20.000.000 de nós por método, que dão:
  - vanilla: 1.961 iterações;
  - acaso: 235.294 árvores;
  - externo: 541.126 iterações (cada uma com uma travessia por jogador).
- **Sementes dos amostradores:** 1202 e 1204; a faixa vale para a média das duas.

**A convergência (P3041).**
- **(a)** A explorabilidade do vanilla em 20 milhões de nós.
  - **Centro:** 0,0724/5,07 = 0,0143.
  - **Mecanismo da faixa:** uma razão por década entre √10 (convergência a 1/√T) e 10 (a 1/T).
  - **Faixa:** **[0,0072; 0,0229]**. Abaixo dela, o vanilla converge mais rápido que 1/T; acima, mais devagar que 1/√T.
- **(b)** A explorabilidade média do acaso (sementes 1202 e 1204).
  - **Centro:** 0,1111/4,69 = 0,0237.
  - **Mecanismo da faixa:** o ruído de amostragem empurra a razão para √10; o transiente da calibração a deixa até 6,5.
  - **Faixa:** **[0,0171; 0,0352]**.
- **(c)** A explorabilidade média do externo (sementes 1202 e 1204).
  - **Centro:** 0,0916/4,6 = 0,0199.
  - **Mecanismo da faixa:** o mesmo da (b).
  - **Faixa:** **[0,0141; 0,0290]**.

**O mesmo custo (P3042).**
- **(d)** A razão externo/acaso das médias.
  - **Histórico:** 0,814 em 200 mil nós e 0,824 em 2 milhões; centro 0,82.
  - **Faixa:** o ruído das sementes (±0,18): **[0,65; 1,00]**.
  - **Mecanismo:** sortear o adversário deixa mais iterações pelo mesmo custo. Acima de 1, o Leduc não teria ações bastantes para que isso compense.
- **(e)** A razão vanilla/externo.
  - **Histórico:** 0,86 em 200 mil nós e 0,79 em 2 milhões; centro 0,72.
  - **Mecanismo:** o vanilla não tem ruído, então a vantagem dele cresce enquanto os amostradores ficam presos no piso do ruído.
  - **Faixa:** **[0,45; 0,95]**.

**O valor do jogo.**
- **(f)** O valor da estratégia média do vanilla para o jogador 1.
  - **Centro:** −0,0858. A Parte 71 proíbe extrapolar uma tendência de 2 pontos sem t, então não extrapolo.
  - **Mecanismo da faixa:** |v(σ) − v*| ≤ explorabilidade(σ). A meia-largura é 1,36 × 0,0143.
  - **Faixa:** **[−0,1052; −0,0664]**.
  - O valor publicado (−0,0856) não foi lido nesta sessão e não entra como identidade.
- **(g)** Quantas das 2 pontas do intervalo [melhor resposta do jogador 2, melhor resposta do jogador 1] em 20 milhões de nós caem dentro do intervalo de 2 milhões, [−0,11586; −0,04348].
  - **Faixa:** **[2; 2]**.
  - **Regra da Parte 121:** P(uma ponta) ≈ 0,97, porque o intervalo encolhe com a explorabilidade, de 0,072 para ~0,014. Então p² = 0,94 ≥ 0,90.

**O diálogo (P3043).**
- **(h)** A rodada 88 é **IGUAL** bit a bit entre Python e Java: **[0; 0]**.
  - **Identidade:** só inteiros (as contribuições), +, −, × e ÷ na mesma ordem dos dois lados, e chaves ASCII em ordem lexicográfica: o `sorted` do Python e o `TreeMap` do Java comparam pelo código do caractere.
- **(i)** A estratégia média da `rodada88.py` comparada com a de `synthai.leduc`, com T = 3: conjuntos que diferem em algum bit, **[0; 0]**.
  - **Identidade:** a mesma ordem das 120 distribuições (`POSTOS[a]` = a // 2), a mesma `estrategia` e as mesmas somas.

### Previsões sobre as previsões (m), pré-registradas (régua: P2837, leitor v4)

Contagem pelo leitor antes do commit: **9**.
- **(m1)** nº de previsões do mundo em **[8; 10]**
- **(m2)** nº de faixas que cruzam/tocam o zero em **[2; 3]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0,50; 0,80]**
- **(m4)** fração de acertos do mundo em **[0,67; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[3; 5]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 1]**

### Sobre mim, pré-registrado

Pela regra da Parte 117, o centro de "quantos erros" é:
0 × 2 identidades + 0,10 × 0 faixas de forma fechada + 0,2 × 7 faixas de mecanismo = **1,4**, com faixa **[0; 3]**.

O risco maior é a (e). A razão vanilla/externo veio de 2 pontos, com a tendência escrita no mecanismo; é exatamente o que a regra da Parte 71 manda tratar com cuidado.

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->

## As respostas (quatro camadas)

### P3041 — Quanto cede cada método em 20 milhões de nós

**Na pergunta.** "Ceder" é a explorabilidade: o quanto um adversário que conhece a minha estratégia ganharia a mais, somado nos dois lados. "Em 20 milhões de nós" fixa o custo, não as iterações. O vanilla faz 1.961 iterações, o acaso 235.294 árvores e o externo 541.126 iterações com esse mesmo orçamento.

**Lógica** (saídas de `p3041_leduc`, sementes 1202 e 1204):

| Método | Nós | Explorabilidade | Valor para o jogador 1 | [melhor resposta do 2; do 1] |
|---|---|---|---|---|
| vanilla | 20.002.200 | **0,01846** | −0,08702 | [−0,09538; −0,07692] |
| acaso 1202 | 19.999.990 | 0,03335 | −0,08689 | [−0,10329; −0,06994] |
| acaso 1204 | 19.999.990 | 0,03665 | −0,08783 | [−0,10630; −0,06965] |
| externo 1202 | 19.749.049 | 0,02933 | −0,08805 | [−0,09966; −0,07034] |
| externo 1204 | 19.780.482 | 0,03015 | −0,08712 | [−0,10074; −0,07059] |

- **(a)** O vanilla deu 0,01846, dentro de [0,0072; 0,0229] ✅. A razão por década foi 0,0724/0,01846 = **3,92**. Caiu de 5,07 para perto de √10 = 3,16: o vanilla também desacelera.
- **(b)** O acaso deu, na média, (0,03335 + 0,03665)/2 = **0,03500**, dentro de [0,0171; 0,0352] ✅, e na borda. A razão foi 0,1111/0,0350 = **3,17**, ou seja, √10: chegou ao piso do ruído, 1/√N.
- **(c)** O externo deu, na média, **0,02974**, fora de [0,0141; 0,0290] ❌, por 0,0007. A razão foi 0,0916/0,02974 = **3,08**, um pouco abaixo de √10. Dois fatores explicam:
  - o externo gastou 1,25% menos nós que o previsto (19,76 milhões, porque 36,96 nós por iteração era uma média de calibração);
  - a faixa não somou o ruído entre sementes ao piso de √10.

  O erro (0,0007) é menor que a largura da faixa (0,0149), então não conta como surpresa.

**Tradução cruzada.** Aprender jogando tem duas fases:
- **transiente:** o arrependimento cai depressa (razão 5 por década);
- **piso:** cai com o ruído da amostra (razão √10).

Na calibração eu via o transiente. Em 20 milhões de nós, os dois amostradores já estavam no piso.

**Meta.** A regra da Parte 71 disse para não extrapolar a tendência de 2 pontos. Usei o mecanismo como faixa (√10 a 10), o que acertou a (a) e a (b). A (c) mostra que um piso físico, √10, ainda precisa da dispersão das sementes em volta dele.

### P3042 — Com o mesmo custo, quem ganha

**Lógica** (`p3042_razoes_mesmo_custo`).
- **(d)** Externo/acaso: 0,02974/0,03500 = **0,850**, dentro de [0,65; 1,00] ✅. Com o mesmo número de nós, sortear também o adversário ganha do acaso no Leduc, onde há até 3 ações. No Kuhn (Parte 119, P3012) era o contrário: o externo explorava 1,9 vez o acaso. **A regra da Parte 119 se confirmou na outra ponta:** sortear o adversário compensa quando há ações bastantes.
- **(e)** Vanilla/externo: 0,01846/0,02974 = **0,621**, dentro de [0,45; 0,95] ✅. O vanilla, sem ruído, segue o melhor neste tamanho. A vantagem dele cresceu (0,86 → 0,79 → 0,62 de 200 mil a 20 milhões de nós), como o mecanismo dizia: os amostradores ficam presos no piso do ruído.
- **O valor do jogo.** A interseção dos 5 intervalos de melhor resposta dá v* ∈ **[−0,09538; −0,07692]**. A conta: o máximo das melhores respostas do jogador 2 contra o mínimo das do jogador 1.
  - **(f)** O valor da estratégia média do vanilla, −0,08702, está dentro de [−0,1052; −0,0664] ✅.
  - **(g)** As 2 pontas do intervalo de 20 milhões caem dentro do intervalo de 2 milhões ✅.
  - O −0,0856 citado na literatura cai dentro desse intervalo, mas a fonte não foi lida nesta sessão. Fica como compatível, não como conferido.

**Tradução cruzada.** O valor do jogo nunca é medido diretamente. Cada estratégia dá um intervalo para ele (o quanto ela ganha contra o pior adversário e o quanto cede ao melhor), e o conhecimento é a interseção dos intervalos de todos os métodos. É o mesmo que fazem várias testemunhas que só concordam em parte.

### P3043 — rodada 88

- **(h)** A rodada 88 deu **IGUAL** em Java (289 linhas e 672 números idênticos bit a bit) ✅.
- **(i)** **0 de 288** conjuntos diferem de `synthai.leduc` ✅.

As cadeias de histórico, as frações de pote, o `TreeMap` do Java e o `sorted` do Python não acrescentam fronteira. É mais uma vez a regra da Parte 90: a fronteira é a aritmética, nunca a estrutura do jogo.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ❌ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅

**8 de 9.** A chance de acertar ao acaso, contra o preditor ingênuo "igual ao valor de 2 milhões de nós": esse preditor erraria a (a), a (b) e a (c), que caíram de 4 a 5 vezes, e acertaria a (d), a (e) e a (f), que pouco mudaram. Ele faria 6 de 9 contra os meus 8.

### Previsões sobre previsões (m)

Saídas do `p2837_previsoes_sobre_previsoes_v4(120)`:

| Item | Previsto | Medido | Resultado |
|---|---|---|---|
| (m1) | [8; 10] | 9 | ✅ |
| (m2) | [2; 3] | 2 | ✅ |
| (m3) | [0,50; 0,80] | **0,346** | ❌ |
| (m4) | [0,67; 1,00] | 0,889 | ✅ |
| (m5) | [3; 5] | **0** | ❌ |
| (m6) | [0; 1] | 0 surpresas: o único erro, (c), foi de 0,0007, contra a largura de 0,0149 | ✅ |

**4 de 6.** Os dois erros têm a mesma causa. Calculei o w de cabeça, como largura/centro, e a régua usa largura/(|a| + |b|), que é a metade. Os w que a régua mede são:

| (a) | (b) | (c) | (d) | (e) | (f) | (g) |
|---|---|---|---|---|---|---|
| 0,52 | 0,35 | 0,35 | 0,21 | 0,36 | 0,23 | 0 |

Todos ficam abaixo de 0,6.

### Sobre mim

| Previsto | Medido |
|---|---|
| 1,4 erros, faixa [0; 3] | 1 erro do mundo ✅ |

## Engenharia reversa (metacognição)

- **O padrão que se repetiu:** a Parte 75 disse para partir de uma contagem por código, nunca da imagem que eu tenho de uma régua. Aqui eu tinha a régua (P2837) e não a rodei sobre o rascunho; usei a minha lembrança da definição de w. É a terceira vez que uma régua minha me engana por eu não a rodar (Partes 75, 109 e 120). O significado: eu trato as minhas funções de medida como conhecidas, e é justamente nelas que a memória falha, porque eu as escrevi e acho que lembro.
- **Regra nova:** as (m) só são registradas depois de rodar a régua sobre o rascunho das previsões. O rascunho leva uma linha "Do mundo:" provisória, com todos os itens ✅, que é apagada antes do commit, e daí saem m3 e m5.
- **O erro do mundo, (c):** uma faixa com um piso físico (√10, o ruído 1/√N) ainda soma a dispersão das sementes em volta do piso. O mecanismo estava certo e o peso dele não: de novo a regra da Parte 62.

## Síntese / unificação

O Leduc confirmou, em 2 lotes (Kuhn na Parte 119, Leduc aqui), que a vantagem da amostragem externa sobre a do acaso depende do número de ações. Ela perde no Kuhn (2 ações; 1,9 vez pior) e ganha no Leduc (até 3 ações; 0,85).

Neste tamanho, o vanilla segue o melhor com o mesmo custo (0,62 do externo), porque os amostradores chegaram ao piso do ruído (razão √10 por década). O valor do jogo para o jogador 1 está em [−0,0954; −0,0769], pela interseção das melhores respostas de 5 estratégias.

## Meta

- Duas sementes por amostrador dão a média, mas não a dispersão. A (c) errou exatamente por isso.
- A fronteira do valor do jogo é um resultado exato sobre as estratégias medidas, e não uma estimativa: as melhores respostas são exatas.

## Diálogo Python ↔ Java (rodada 88)

A **IA-Python** perguntou se o jogo, com cadeias, cartas públicas e frações de pote, muda alguma conta. A **IA-Java** respondeu com o `TreeMap` e o `Math.max` sobre inteiros, e o resultado deu **IGUAL** em 288 conjuntos e 672 números.

A pendência que fica é se o MCCFR externo no Leduc, com o LCG, também dá IGUAL. Ela entrou em `dialogo/PENDENCIAS.md`.

## Fontes

Southey, F. et al. (2005), *Bayes' Bluff: Opponent Modelling in Poker* (as regras do Leduc). Zinkevich, M. et al. (2007), *Regret Minimization in Games with Incomplete Information* (CFR). Lanctot, M. et al. (2009), *Monte Carlo Sampling for Regret Minimization in Extensive Games* (MCCFR). As três são citadas de memória e não foram relidas nesta sessão, porque o limite semanal de busca na web acabou. Nenhum número delas é usado como identidade.

➡ Continua na [Parte 121 — O NEXUS–RAPHAEL 2.2.0](ASI_AGI_parte121_nexus_v2_2.md) (escrita antes desta) e na [Parte 122 — O texto NEXUS–RAPHAEL v3.0](ASI_AGI_parte122_nexus_v3_0.md).
