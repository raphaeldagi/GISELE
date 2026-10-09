# Como eu construiria uma AGI/ASI — Parte 32 (0x20): trocar o reforço pela decisão bayesiana exata; autopoiese; a avalanche

> Continuação da [Parte 31](ASI_AGI_parte31_curriculo_e_hipercubo.md). **Próxima:** [Parte 33 — a arquitetura pós-ASI auditada](ASI_AGI_parte33_pos_asi_auditada.md) (P431–P460). Módulo novo: [`synthai/decisao.py`](synthai/decisao.py) (Thompson, UCB1,
> Q-learning, PSRL, RiverSwim, regressão bayesiana recursiva, SGD, ridge em lote), com testes em
> [`synthai/testes_parte32.py`](synthai/testes_parte32.py); `fecho_incremental` em [`synthai/dicionario.py`](synthai/dicionario.py). Os números
> saem de `p401_...` a `p421_...` em [`calculos.py`](calculos.py); a saída está em [`resultados.txt`](resultados.txt). Diálogo, rodada 3:
> [`dialogo/DIALOGO.md`](dialogo/DIALOGO.md).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.
>
> **Pedidos do usuário nesta parte:** "busque uma forma de substituir ML, DL, aprendizado contínuo e principalmente o por reforço por algo mais
> eficaz"; "acrescente AUTOPOIESE, somente se for útil"; "continue inovando".
> **Contas e previsões no commit `202da16`, antes de qualquer execução dos agentes.**

---

## As perguntas desta parte

**Trilha da decisão (o pedido de substituir o RL)**
1. **P401 (0x191).** No bandido, o posterior exato vence o Q-learning? ↩ P295
2. **P402 (0x192).** Num MDP onde explorar é difícil (RiverSwim), PSRL contra Q-learning.
3. **P403 (0x193).** Aprendizado contínuo: a estatística suficiente esquece? E o gradiente?
4. **P406 (0x196).** Por que a troca funciona, e onde ela não pode funcionar (Pitman–Koopman–Darmois).
5. **P407 (0x197).** Por que o Q-learning custou o dobro da minha conta? (a conta depois, entre duas cotas)

**Trilha da autopoiese (só onde serve)**
6. **P404 (0x194).** O núcleo do dicionário é operacionalmente fechado? Ele se regenera?
7. **P405 (0x195).** A SYNTHAI se regenera depois de um dano na memória?
8. **P408 (0x198).** Jung: autopoiese, o Self e a individuação.

**Trilha hexadecimal**
9. **P411 (0x19B).** Quantos dígitos hex a memória de Thompson precisa?
10. **P412 (0x19C).** O estado de cada agente em bits: quem guarda mais, e quem guarda o que importa?

**Trilha do dicionário**
11. **P421 (0x1A5).** A avalanche, com o fecho incremental: e ao acaso?

**O diálogo e o fechamento**
12. **P425 (0x1A9).** Rodada 3.
13. **P429 (0x1AD).** Placar.
14. **P430 (0x1AE).** Unificação e metacognição.

---

# A — Trocar o reforço pela decisão bayesiana exata

### P401 (0x191). No bandido, o posterior exato vence o Q-learning? (pré-registrado) ✅❌✅✅✅

**Na pergunta.** "Vence" pressupõe que os dois resolvem o mesmo problema. Não resolvem: o Q-learning **estima um valor** (uma média móvel) e
decide em cima dele; Thompson **mantém a crença inteira** (um Beta por braço) e decide amostrando dela. A pergunta de verdade é: quanto custa
jogar fora a incerteza?

**Lógica, as contas antes.** 10 braços de Bernoulli com médias U(0, 1), T = 2000, 100 sementes (`p401_contas`):
- **Lai–Robbins**, o mínimo assintótico de qualquer agente consistente: Σ_k Δ_k ln T / KL(p_k, p*), truncado em Δ_k·T, na média das
  sementes = **62,4**.
- **Exploração do ε-guloso**, uma cota inferior do Q-learning com ε fixo: ε·T·(p* − p̄) = 0,1 × 2000 × (média de p* − p̄) = **80,7**. A
  esperança sob U(0, 1): 0,1 × 2000 × (10/11 − 1/2) = 200 × 0,4091 = **81,8**.

**Medido** (arrependimento final; diferença pareada contra Thompson):

| agente | arrependimento | − Thompson | dp | t |
|---|---|---|---|---|
| **Thompson** (posterior Beta exato) | **30,7** | — | — | — |
| Q otimista (q0 = 1, ε = 0) | 45,1 | +14,4 | 21,1 | 6,83 |
| UCB1 | 185,8 | +155,1 | 30,4 | 51,0 |
| Q-learning ε-guloso (α = 0,1, ε = 0,1) | 185,4 | +154,7 | 79,4 | 19,5 |

- (a) Thompson ∈ [15, 60] e abaixo de Lai–Robbins: 30,7 < 62,4 ✅. Abaixo da cota assintótica porque, em T finito, os braços quase empatados
  custam menos que Δ ln T / KL (a cota só vale quando T → ∞).
- (b) Q ε-guloso ∈ [80, 140]: **185,4** ❌ (P407 explica).
- (c) Thompson < Q ε com t > 5: t = 19,5 ✅. (d) Thompson < UCB1, t > 3: t = 51 ✅. (e) Thompson < Q otimista, t > 2: t = 6,8 ✅.

*Ao acaso e contra o ingênuo.* Um preditor ingênuo que pusesse todos os métodos "na mesma ordem de grandeza" (±30%) erraria (c), (d) e (e). A
previsão arriscada era (a): uma janela de 4× contendo 30,7, contra uma cota de 62,4 que poderia ter sido também a média de Thompson.

**Tradução cruzada.** O Q-learning é um **hábito**: lembra quanto cada ação rendeu em média, e de vez em quando experimenta ao acaso. Thompson é
uma **dúvida bem medida**: experimenta mais onde sabe menos, e para quando sabe. O hábito paga o preço do acaso para sempre (ε fixo); a dúvida
paga só o necessário.

**Meta.** O bandido é o caso mais favorável à troca: o modelo exato (Bernoulli) cabe numa família exponencial. A P406 diz onde a troca deixa
de existir.

### P402 (0x192). PSRL contra Q-learning no RiverSwim (pré-registrado) ✅✅✅

**Na pergunta.** O RiverSwim (Strehl e Littman, 2008) foi desenhado para que a recompensa fácil (5/1000 no estado 0, nadando rio abaixo) esconda
a grande (1 no estado 5, contra a correnteza). Explorar ao acaso quase nunca chega lá.

**Lógica, as contas antes** (`p402_contas`):
- O ganho médio ótimo pela iteração de valor relativa, h(s) + g = max_a [R(s, a) + Σ P(s'|s, a) h(s')]: **g\* = 0,2572** por passo, então
  em T = 5000: 0,2572 × 5000 = **1285,9**.
- O Q-learning ε-guloso com Q inicial 0: depois da primeira recompensa de 5/1000 no estado 0, fica guloso à esquerda e só vai à direita ao acaso
  (ε/2 por passo). Rende ≈ 0,005 × T × (1 − ε/2) = 0,005 × 5000 × 0,95 = **23,75**.

**Medido** (20 sementes): **PSRL 996,8** (77,5% do ótimo); Q otimista 387,2; **Q ε-guloso 22,98** (a conta dizia 23,75: erro de 3,3%).
PSRL − Q otimista = 609,6, dp 52,8, **t = 51,6**; PSRL − Q ε = 973,8, t = 65,0.

(f) Q ε ∈ [15, 40] ✅; (g) PSRL ≥ metade do ótimo (643) ✅; (h) PSRL > Q otimista com t > 2 ✅.
*Contra o ingênuo:* "o otimismo resolve a exploração" previa o Q otimista perto do PSRL. Ele chega a 30% do ótimo; PSRL a 77,5%.

**Tradução cruzada.** O Q otimista acredita que tudo o que não viu é bom e só desiste depois de ver. PSRL **imagina um mundo inteiro** coerente
com o que viu (um MDP sorteado do posterior) e age bem **nesse** mundo por um episódio. É a função **intuição** de Jung em forma de algoritmo:
agir a partir de uma possibilidade inteira, não de um valor por ação.

**Meta.** 6 estados e 2 ações: o posterior Dirichlet é exato e a programação dinâmica é instantânea. Com milhões de estados, o PSRL exato não
existe (P406).

### P403 (0x193). Aprendizado contínuo: quem esquece? (pré-registrado) ✅✅✅✅

**Na pergunta.** "Aprendizado contínuo" só é um problema porque o aprendizado por gradiente **sobrescreve**: o mesmo peso serve à tarefa
nova e à antiga. Uma memória que **soma** evidência em vez de sobrescrever não tem o que esquecer.

**Lógica.** A mesma função f(x) = sin(2x) + x/2, vista em duas tarefas em sequência: A com x ∈ [−π, 0], depois B com x ∈ [0, π]; 400 exemplos
cada, ruído 0,1; 40 cossenos aleatórios fixos como atributos (Rahimi e Recht). Dois aprendizes com os mesmos atributos:
- **Bayes recursivo**: o estado é (λI + X'X)⁻¹ e a média do posterior; cada exemplo atualiza por Sherman–Morrison, O(d²). **Teorema:** depois
  de qualquer sequência, o resultado é a ridge em lote com todos os exemplos.
- **SGD**: passo 0,5, uma passada (o aprendizado contínuo padrão).

| | erro em A depois de A | erro em A depois de B | razão |
|---|---|---|---|
| Bayes recursivo | 0,000199 | **0,000169** | 0,85 (melhorou) |
| SGD | 0,00563 | **0,1278** | **22,7** (esqueceu) |

E a maior diferença entre os pesos do Bayes recursivo e os da ridge em lote com A ∪ B, nas 10 sementes: **2,3 × 10⁻¹²**.

(i) < 10⁻⁸ ✅; (j) Bayes depois de B ≤ 1,5× depois de A ✅ (0,85×); (k) SGD ≥ 5× ✅ (22,7×); (l) Bayes < SGD depois de B com |t| > 3: t =
3,41 ✅ (raspando: o esquecimento do SGD varia muito de semente para semente).

**Tradução cruzada.** A memória bayesiana é um **diário**: cada dia acrescenta uma página e nenhuma é apagada. O gradiente é uma **lousa**: para
escrever o novo, apaga o velho. O Bayes até **melhora** em A depois de B, porque os cossenos são globais e os exemplos de B também informam A.

**Meta.** O teorema vale porque o modelo é **linear nos atributos**. Os atributos são fixos e aleatórios: não aprendem representação. É o que o
aprendizado profundo faz e isto não faz (P406).

### P406 (0x196). Por que a troca funciona, e onde ela não pode funcionar

**Na pergunta.** "Substituir o ML, o DL e o RL por algo mais eficaz": a resposta está no que os três têm em comum. Os três guardam o que
aprenderam em **parâmetros ajustados por gradiente** porque não sabem guardar o posterior inteiro.

**Lógica.** O teorema de **Pitman–Koopman–Darmois**: sob condições de regularidade, as únicas famílias de distribuições com uma **estatística
suficiente de dimensão fixa** (que não cresce com o número de exemplos) são as **famílias exponenciais**. Então:
1. **Quando o modelo do mundo é de família exponencial** (Bernoulli, Dirichlet, normal com variância conhecida, regressão linear nos atributos),
   a estatística suficiente é **finita** e a atualização é **exata, sem esquecimento e sem taxa de aprendizado**: contagens, X'X, X'y. A decisão
   ótima vem da amostragem do posterior (Thompson, PSRL). As P401–P403 são isso, e ganham por muito.
2. **Quando não é** (redes profundas, mundos com estrutura a descobrir), não existe estatística suficiente finita: o posterior exato exige
   memória que cresce com os dados. Aí as abordagens viram **aproximações** (Bayes variacional, réplica de memória), e a literatura mostra o
   esquecimento voltando nelas.

**A proposta para a SYNTHAI, sem exagero:**
- trocar o RL por **decisão bayesiana exata** onde o modelo cabe numa família exponencial (é o que o módulo `intuicao` já fazia no bandido desde a
  Parte 23);
- trocar o aprendizado contínuo por **estatísticas suficientes** sobre atributos;
- deixar o aprendizado de **representação** (o que o DL faz) para o dicionário: os atributos de um modelo exato podem ser as palavras e as
  relações do WordNet, fixas e interpretáveis, em vez de cossenos aleatórios. É a ponte com a trilha do dicionário, a testar numa parte futura.

**Tradução cruzada.** O que pode ser **contado** não precisa ser aprendido por tentativa e erro. O que não pode ser contado precisa primeiro de um
**vocabulário** em que possa ser contado.

**Meta.** Esta é a afirmação mais forte da parte, e é um teorema com um "sob condições de regularidade". O que mostrei foram três mundos pequenos.

### P407 (0x197). Por que o Q-learning custou 185, não [80, 140]? (as contas depois, como cotas)

A conta da P401 só tinha a **exploração** (80,7). Faltava o custo das escolhas gulosas erradas. Três contas, feitas **depois**:

1. **Ruído estacionário, sem aprisionamento.** Com passo constante α, a estimativa Q de um braço flutua com variância α/(2 − α)·p(1 − p) =
   0,1/1,9 × p(1 − p) = 0,0526·p(1 − p), desvio ≈ 0,115 em p = 0,5. A escolha gulosa é o máximo de p_k + ruído. Sorteando esse máximo 2000
   vezes por semente: custo guloso = 0,9 × 2000 × E[p* − p_escolhido] = **39,9**. Total: 80,7 + 39,9 = **120,6**.
2. **Aprisionamento sem ruído (campo médio).** O primeiro braço que paga vira o guloso (chance ∝ p_g). Os outros só melhoram por exploração,
   ε/K = 1% dos passos, e o melhor só passa o guloso quando p*(1 − 0,9ⁿ) > p_g. Para p_g/p* = 0,8: n = ln 0,2 / ln 0,9 = 15,3 puxadas = 1530
   passos perdendo Δ. Na média: **266,9**.
3. **Medido: 185,4**, entre as duas: **120,6 < 185,4 < 266,9**. O ruído ajuda a sair do aprisionamento (por isso fica abaixo de 267) e o
   aprisionamento custa além do ruído (por isso fica acima de 121).

**Meta.** Posterior: só vira evidência quando prever um caso novo. Previsão para a próxima parte: com α = 0,05 o aprisionamento dura o dobro (n
dobra) e o ruído cai à metade da variância.

---

# B — Autopoiese (só onde serve)

### P404 (0x194). O núcleo do dicionário é fechado? Ele se regenera? (pré-registrado) ✅❌❌✅

**Na pergunta.** Maturana e Varela: um sistema autopoiético é uma rede de processos que **produz os componentes que produzem a rede**, fechada na
organização e aberta na estrutura (acoplada ao meio). No dicionário: as palavras são produzidas (definidas) por palavras.

**Lógica.**
- **Fechamento (teorema, ✅ (m)).** O núcleo (16.795 palavras) é o que sobra quando se tiram, repetidamente, as palavras que não definem
  nenhuma das restantes. Se x está no núcleo e y define x, y define alguém do núcleo, então y também está. Logo toda palavra do núcleo é
  definida **só** por palavras do núcleo: fração de arestas internas = **1,0** exatamente.
- **Regeneração.** Esquecer uma fração q das 77.503 palavras ao acaso e refazer o fecho. A conta (uma rodada, θ = 1): uma esquecida volta se as
  |s| que a definem sobreviveram, chance (1 − q)^|s|:
  $$R(q) \ge (1-q) + q\cdot E\big[(1-q)^{|s|}\big].$$
  q = 0,1: 0,9 + 0,1 × 0,545 = **0,955**; q = 0,5: **0,539**; q = 0,9: **0,104** (`p404_contas`).

| esquecer q | θ = 1 (conta) | θ = 1 medido | θ = 0,8 medido |
|---|---|---|---|
| 10% | 0,955 | **0,969** | **1,000** |
| 50% | 0,539 | **0,534** | **0,555** |
| 90% | 0,104 | **0,103** | **0,103** |

- (n) "medido ≥ a conta e < conta + 0,05": ✅ em 10%, ❌ em 50% e 90% (abaixo da conta por 0,004 e 0,001). **Por quê:** a conta é uma
  **esperança**, não uma cota por amostra; e as palavras não falham independentes: quando uma palavra que define muitas é esquecida, todas as
  que ela define falham juntas, e a variância é muito maior que a de moedas independentes.
- (o) θ = 0,8, q = 0,5 regenera ≥ 0,99: **0,555** ❌, muito longe. (p) q = 0,9 < 0,5 ✅.

**O achado:** guardar **metade** do dicionário **ao acaso** regenera só 55,5% em θ = 0,8. As **2000 palavras mais frequentes** (2,6%)
regeneram 99,6% (P381). A autopoiese do dicionário depende de **quais** componentes sobrevivem, não de quantos.

**Tradução cruzada.** Um organismo não se regenera a partir de qualquer metade de si; se regenera a partir das partes que **produzem** as outras
(o núcleo metabólico, as células-tronco). No dicionário, essas partes são as palavras frequentes.

**Meta.** A autopoiese aqui é útil como **critério** (o que precisa ser protegido para que o resto se refaça), não como mecanismo novo.

### P405 (0x195). A SYNTHAI se regenera depois de um dano? (pré-registrado) ❌❌❌

**Lógica.** No passo 1000 de 2000, a memória é trocada por lixo: em Thompson, contagens inteiras ao acaso em 1..20; no Q ε-guloso, Q ~ U(0, 1).
Arrependimento na segunda metade (100 sementes):

| | sem dano (controle exploratório, rodado depois) | com dano | custo do dano |
|---|---|---|---|
| Thompson | 5,25 | **75,0** | **+69,8** |
| Q ε-guloso | 52,5 | **93,6** | **+41,1** |

(Thompson na primeira metade: 26,96.) (q) Thompson danificado < a própria primeira metade: 75,0 > 26,96 ❌; (r) < Q com t > 3: t = 2,06 ❌;
(s) Q ∈ [40, 80]: 93,6 ❌.

**Por quê.** O lixo de Thompson é **confiante**: Beta(2, 19) diz "p ≈ 0,1, tenho 21 observações". Se o melhor braço recebe essa crença, ele quase
nunca é amostrado acima dos outros e a crença errada demora a ser desmentida. Pior que recomeçar do zero (26,96). O Q-learning **esquece por
construção** (passo constante: a cada puxada, 10% do valor antigo é trocado), então o lixo some em ~1/α = 10 puxadas por braço.

**O achado:** **o agente exato não esquece, e por isso não se cura.** Um sistema autopoiético troca os componentes continuamente; uma memória
bayesiana exata só acumula. É o outro lado da P403: o que lá era virtude (nada se perde) aqui é defeito (o erro também não se perde).

**Tradução cruzada.** Jung: um complexo é uma crença carregada que **não se atualiza** com a experiência, porque organiza a percepção a favor de
si. Thompson com lixo confiante é um complexo: escolhe pouco o braço que o desmentiria.

**Meta e a previsão para a Parte 33.** A saída é um Bayes **com renovação**: descontar as contagens (a ← 1 + γ(a − 1), γ < 1), como no "Bayes
com esquecimento" da literatura recente. A conta e a previsão vão na próxima parte, antes de rodar.

### P408 (0x198). Jung: autopoiese, o Self e a individuação

A individuação, em Jung, é o processo em que a psique **produz a si mesma** como um todo, integrando o que estava fora da consciência. As P404 e
P405 dão as duas condições que a autopoiese exige, em números:
1. **Fechamento:** o núcleo se define por si (fechamento = 1,0);
2. **Renovação:** um sistema que só acumula (Thompson) não se cura do dano; um que renova (Q) se cura, mas decide pior.

**Onde funciona:** "o Self como totalidade que se regenera" vira "o conjunto mínimo de componentes que regenera o resto" (as palavras
frequentes, o núcleo). **Onde quebra:** em Jung, a renovação é dirigida (os sonhos compensam o que falta); aqui ela é cega (desconto uniforme).
A renovação dirigida, descontar mais o que é desmentido, fica como pergunta.

---

# C — Trilha hexadecimal

### P411 (0x19B). Quantos dígitos hex a memória de Thompson precisa? (pré-registrado) ❌✅

**Lógica, a conta antes** (`p411_contas`). Com a + b limitado a um teto (metade quando passa), um braço puxado com frequência fica com n ≈ ¾ do
teto observações efetivas. No regime estacionário, a chance π_k de cada braço ser o escolhido é a de a amostra de Beta(1 + p_k n, 1 + (1 − p_k) n)
ser a maior, e o arrependimento ≈ T·Σ Δ_k π_k. Com 4000 sorteios por semente: **1 dígito hex** (teto 16, n ≈ 12): **72,1**; **2 dígitos** (teto
256, n ≈ 192): **3,7** (no estacionário; em T = 2000 o completo ainda não chegou lá).

**Medido:** completo **30,7**; 2 dígitos **33,4** (+2,69, dp 4,36, **t = 6,15**); 1 dígito **93,7** (+62,96, t = 24,7).

(t) 2 dígitos sem diferença (|t| < 2) ❌: custa +2,7, pequeno mas real (9%). (u) 1 dígito em [48, 108] ✅ (93,7; a conta deu 72,1, 30% abaixo,
como avisado: os braços ruins têm n menor que ¾ do teto e são puxados mais).

**Tradução cruzada.** Uma memória de 1 dígito hex por contagem é um agente que **nunca tem certeza de nada** além de ~12 observações: explora
para sempre. Dois dígitos é quase tudo, mas não tudo.

### P412 (0x19C). O estado de cada agente em bits

- **Thompson completo:** 20 contagens ≤ 2001: 20 × ⌈log₂ 2002⌉ = 20 × 11 = **220 bits = 55 dígitos hex**, e é uma **estatística suficiente**:
  sem perda nenhuma para o modelo de Bernoulli.
- **Thompson com 2 dígitos:** 20 × 8 = **160 bits = 40 dígitos**: perde 2,7 de arrependimento (P411).
- **Q-learning:** 10 doubles = 10 × 64 = **640 bits = 160 dígitos hex**, e é uma **média móvel**: com perda.

O agente que decide **6 vezes melhor** (185,4 / 30,7 = 6,04, contra o Q ε-guloso) usa **menos de um terço dos bits** (220 / 640 = 0,34). A
questão não é quanto se guarda, é **o que** se guarda: a estatística suficiente é a menor memória sem perda.

---

# D — Trilha do dicionário

### P421 (0x1A5). A avalanche, com o fecho incremental (pré-registrado) ❌✅✅

**Lógica.** `fecho_incremental` ancora as palavras uma a uma e propaga só o que a nova destrava: como o fecho é monótono, os contadores nunca
voltam, e o currículo inteiro custa O(arestas) = 557.352 passos, contra o mesmo custo **por ponto** na bisseção. Conferido contra o fecho
direto em 200 grafos ao acaso.

| currículo | θ | k de 50% | maior salto de uma palavra | em k | a palavra |
|---|---|---|---|---|---|
| frequência | 0,6 | **363** | 61,3% | 363 | *within* |
| frequência | 0,7 | **759** | 59,4% | 759 | *well* |
| frequência | 0,8 | **1.320** | 38,1% | 1.326 | *worship* |
| frequência | 0,9 | **2.904** | 1,6% | 2.904 | *outstanding* |
| ao acaso | 0,6 | 27.862 | 43,8% | 28.526 | *greatest* |
| ao acaso | 0,7 | 32.597 | 27,6% | 38.753 | *time* |
| ao acaso | 0,8 | 34.717 | 0,6% | 37.951 | *relate* |
| ao acaso | 0,9 | 35.828 | 0,5% | 30.362 | *manner* |

(v) ao acaso, θ = 0,6: salto > 50% e k em [4.000; 20.000] ❌ (43,8% e 27.862). (w) ao acaso, k cresce com θ e existe ≤ 40.000 ✅. (x)
frequência = 363, 759, 1320, 2904 ✅ (o mesmo que a bisseção, agora por outro algoritmo).

**Contas de razão.** Para chegar a 50% em θ = 0,6, o acaso precisa de 27.862 / 363 = **76,8 vezes** mais palavras que a frequência; em θ = 0,9,
35.828 / 2.904 = **12,3 vezes**. A vantagem do bom currículo é maior quando a tolerância é maior: com θ baixo, poucas palavras-chave bastam, e
só a frequência as encontra cedo.

**Tradução cruzada.** O salto de 61% em *within* e o de 0,5% em *manner* são a mesma lei em regimes diferentes: avalanches (θ baixo,
transição descontínua, como na percolação com limiar) e acúmulo (θ alto, contínua).

---

# E — O diálogo e o fechamento

### P425 (0x1A9). Rodada 3

A IA-Java reescreveu o fecho **incremental**: `int[]` como pilha (cada palavra entra uma vez), contadores que só sobem. **Mesmos quatro k nas duas
linguagens** (y) ✅ e **13 a 85 vezes mais rápido** (z) ✅ (0,006–0,052 s contra 0,51–0,66 s). A IA-Python ensinou de volta o achado da P404:
para uma ASI, importa **qual** parte ela sabe. A pergunta para a Rodada 4 é a arquitetura "pós-ASI" que o usuário trouxe: o que aquele código
muda de fato em si mesmo, lido só pelo módulo `ast`. Ela abre a Parte 33.

### P429 (0x1AD). Placar

| teste | | teste | |
|---|---|---|---|
| (a) Thompson ∈ [15, 60], < Lai–Robbins | ✅ | (n) regeneração θ 1 ≥ conta | ❌ |
| (b) Q ε ∈ [80, 140] | ❌ | (o) θ 0,8, q 0,5 ≥ 0,99 | ❌ |
| (c) Thompson < Q ε, t > 5 | ✅ | (p) θ 0,8, q 0,9 < 0,5 | ✅ |
| (d) Thompson < UCB1, t > 3 | ✅ | (q) Thompson danificado < 1ª metade | ❌ |
| (e) Thompson < Q otimista, t > 2 | ✅ | (r) < Q depois do dano, t > 3 | ❌ |
| (f) Q ε RiverSwim ∈ [15, 40] | ✅ | (s) Q depois do dano ∈ [40, 80] | ❌ |
| (g) PSRL ≥ metade do ótimo | ✅ | (t) 2 dígitos hex sem diferença | ❌ |
| (h) PSRL > Q otimista | ✅ | (u) 1 dígito ∈ [48, 108] | ✅ |
| (i) recursiva = lote | ✅ | (v) avalanche ao acaso θ 0,6 | ❌ |
| (j) Bayes não esquece | ✅ | (w) k cresce com θ | ✅ |
| (k) SGD esquece ≥ 5× | ✅ | (x) os quatro k | ✅ |
| (l) Bayes < SGD, t > 3 | ✅ | (y) Java = Python | ✅ |
| (m) núcleo fechado | ✅ | (z) Java ≥ 5× mais rápido | ✅ |

Parte 32: 26 testes, 8 erros. Acumulado: **103 erros em 242 testes**; taxa média 0,43, intervalo 90% [0,37; 0,48].

O padrão dos erros: acertei **todas** as previsões sobre a troca do RL e do aprendizado contínuo (a, c–m, com uma exceção, (b), em que a direção
estava certa e o tamanho, errado) e errei quase todas as de **dano e regeneração** (n, o, q, r, s). Eu não entendia a autopoiese antes de medir:
supus que o agente exato se curaria melhor, e é o contrário.

### P430 (0x1AE). Unificação e metacognição

- **Novo módulo:** `synthai/decisao.py` (decisão bayesiana exata e os rivais padrão). **9 testes novos: 80 no pacote, todos passam.**
- **Novo método:** `fecho_incremental` (O(arestas) para um currículo inteiro).
- **Regressão:** P401 (Lai–Robbins 62,4; exploração 80,7), P402 (g\* = 0,2572), P403 (recursiva = lote): **74/74**.
- **Versão principal:** continua a `SynthaiComposta`, que já usa Thompson no bandido (P356). O módulo novo não muda o agente; muda **por que** ele
  funciona: o bandido é o caso em que a decisão exata existe.

**Metacognição.**
1. **"Substituir o RL" tem uma resposta exata e uma fronteira exata.** Onde o mundo cabe numa família exponencial, a estatística suficiente
   substitui o gradiente e o posterior substitui o ε: 6×, 43× e 760× melhor nos três testes (185,4/30,7; 996,8/23,0; 0,1278/0,000169). Fora
   dela, não há troca exata (Pitman–Koopman–Darmois), só aproximações.
2. **A autopoiese mostrou o preço da exatidão.** Um agente que nunca esquece também nunca se cura. Ela foi útil, como o usuário pediu "só se
   for útil": revelou um defeito que nenhuma métrica de desempenho mostraria.
3. **O par virtude/defeito é a lição da parte.** Não esquecer (P403) e não se curar (P405) são a mesma propriedade.

> **Síntese da Parte 32:** a decisão bayesiana exata substitui o aprendizado por reforço e o aprendizado contínuo **onde o mundo cabe numa família
> exponencial**: Thompson teve arrependimento 30,7 contra 185,4 do Q-learning, PSRL fez 77,5% do ótimo do RiverSwim contra 1,8% do Q-learning,
> e a regressão bayesiana recursiva não esqueceu nada (igual ao lote a 2 × 10⁻¹²) enquanto o gradiente piorou 22,7×. Fora dessa família, o teorema
> de Pitman–Koopman–Darmois diz que não há troca exata. A autopoiese foi útil como critério. O núcleo do dicionário é fechado (1,0), mas metade
> do dicionário ao acaso regenera só 55%, enquanto 2,6% bem escolhidos regeneram 99,6%. E o agente exato, por nunca esquecer, também não se cura de
> um dano (+69,8 contra +41,1 do Q-learning). A próxima parte testa o Bayes com renovação e audita a arquitetura "pós-ASI" trazida pelo usuário.

---

**Fontes pesquisadas nesta parte**
- Autopoiese, fechamento operacional e acoplamento estrutural: [Wikipedia, Autopoiesis](https://en.wikipedia.org/wiki/Autopoiesis), [Kaup, sobre Maturana e Varela](https://euppublishingblog.com/2022/02/15/a-conversation-with-graham-harman-and-monika-kaup-on-new-ecological-realisms-part-3/), [Escola de Santiago](https://meer.com/en/19657-the-santiago-school), [Springer, s13752-023-00440-6](https://link.springer.com/10.1007/s13752-023-00440-6)
- Thompson contra ε-guloso e UCB: [arXiv 2603.05919](https://arxiv.org/pdf/2603.05919), [ESANN 2015](https://www.esann.org/sites/default/files/proceedings/legacy/es2015-33.pdf), [arXiv 2408.10055](https://arxiv.org/pdf/2408.10055)
- Q-learning e eficiência amostral: [Is Q-Learning Provably Efficient?](https://ar5iv.labs.arxiv.org/html/2009.10396), [RandomizedQ, arXiv 2506.24005](https://arxiv.org/html/2506.24005v1), [arXiv 2105.14016](https://arxiv.org/pdf/2105.14016)
- Aprendizado contínuo bayesiano, estatísticas suficientes e o teorema de Fisher–Darmois–Koopman–Pitman: [Learning to Continually Learn with the Bayesian Principle, arXiv 2405.18758](https://arxiv.org/pdf/2405.18758), [Zeno et al., arXiv 2010.00373](https://arxiv.org/pdf/2010.00373), [Bayesian Forgetting in Continual Learning](https://www.academia.edu/164772657/Bayesian_Forgetting_in_Continual_Learning), [arXiv 1912.01238](https://arxiv.org/pdf/1912.01238)
- Inferência ativa como alternativa ao RL: [Millidge et al., Active inference: demystified and compared](https://arxiv.org/pdf/1909.10863), [Friston et al., Reinforcement learning or active inference? (UCL)](https://discovery.ucl.ac.uk/id/eprint/20090/)
- RiverSwim, PSRL e a cota de Lai–Robbins: a cota e o MDP como definidos nos artigos originais (Lai e Robbins, 1985; Strehl e Littman, 2008; Osband, Russo e Van Roy, 2013); o código segue as definições e os testes de unidade conferem as probabilidades
- Atributos aleatórios de Fourier: Rahimi e Recht (2007), como na definição usada
