# Como eu construiria uma AGI/ASI — Parte 28: a âncora

> Continuação da [Parte 27](ASI_AGI_parte27_autorregulacao.md). Módulo novo: [`synthai/ancora.py`](synthai/ancora.py) (testes em
> [`synthai/testes_ancora.py`](synthai/testes_ancora.py)). Os números saem de `p342_...` a `p344_...` em [`calculos.py`](calculos.py); a saída completa
> está em [`resultados.txt`](resultados.txt). O projeto inteiro num arquivo só: [`SYNTHAI_completo.py`](SYNTHAI_completo.py).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.
>
> **Duas rodadas de previsões, cada uma num commit antes da execução**: `7969823` (comportamento) e o do bandido. A conta veio **antes** das
> previsões (regra da Parte 27) e está no commit.

---

## As perguntas desta parte

1. **P341.** Que âncora uma autorregulação precisa, e quanto ela pesa? (a conta de Wilson–Hilferty)
2. **P342.** A conta antes da previsão: quanto cada âncora move $f$ e $m$?
3. **P343.** Com a âncora, a SYNTHAI decide melhor sem ficar mais ousada?
4. **P344.** E no bandido?
5. **P345.** A chance de cada acerto.
6. **P346.** Jung: o ego ancorado.
7. **P347.** Onde a auditoria engana.
8. **P348.** Capacidades.
9. **P349.** Placar.
10. **P350.** Unificação e metacognição.

---

## Parte CXXXIII — A âncora pela conta

### P341. Que âncora, e quanto ela pesa? (↩ P338)

**Na pergunta.** A P338 terminou dizendo que conhecer-se pela experiência custa catástrofes (25 para errar menos de 20%) e que, até lá, a
autorregulação precisa de uma âncora de fora. "Âncora" pede duas coisas: algo **fixo** em que se segurar e algo que **se solta** quando não é mais
preciso.

**Lógica: duas âncoras que já existiam.**
1. **Pessimismo sob incerteza.** No aprendizado por reforço offline, a regra segura é agir pelo **limite inferior de confiança** do valor
   (Rashidinejad et al., 2021): pagar só pela incerteza do que se escolhe. Do lado do risco, é usar um **quantil alto** de $f$, não a média. Com
   catástrofes ~ Poisson($f \sum p$) e priori Gamma, a posterior é
   $$
   f \sim \text{Gamma}(k + a,\ \textstyle\sum p + a),
   $$
   e o quantil de 80% sai da aproximação de **Wilson–Hilferty** (a mesma que o `qgamma` do R usa como ponto de partida):
   $$
   q_{0{,}8} \approx \frac{k}{\lambda}\left(1 - \frac{1}{9k} + \frac{z}{3\sqrt{k}}\right)^3, \qquad z = 0{,}8416 .
   $$
   Conferida contra o quantil exato (bissecção na função de distribuição): Gamma(9, 1): **11,374** contra **11,38**; Gamma(100, 1): 108,3 contra
   108,3; Gamma(1, 1): 1,599 contra 1,609.
2. **A realidade de fora.** O histórico **auditado** que calibra o pensamento tem catástrofes rotuladas. Nas candidatas desse histórico que a SYNTHAI
   aceitaria sem perguntar, os rótulos e os $p$ previstos viram a priori de $f$. Só rótulos: a auditoria nunca mostra valores.

**Quanto a âncora do quantil pesa, pela conta.** A razão quantil/média é $(1 - 1/(9k) + z/(3\sqrt k))^3$:
$$
\begin{aligned}
k = 9{,}5:&\quad (1 - 0{,}0117 + 0{,}0910)^3 = 1{,}0793^3 = 1{,}257 \\
k = 25:&\quad (1 - 0{,}0044 + 0{,}0561)^3 = 1{,}0517^3 = 1{,}163 \\
k = 100:&\quad (1 - 0{,}0011 + 0{,}0281)^3 = 1{,}0270^3 = 1{,}083
\end{aligned}
$$
Com as ~9,5 catástrofes de uma SYNTHAI típica, o quantil fica 26% acima da média. Com 100, fica só 8% acima: a âncora se solta sozinha quando a
experiência chega.

### P342. A conta antes da previsão: quanto cada âncora move $f$ e $m$?

Sementes já usadas (700–709), limiar fixo em $2P^\*$ (autorregulação desligada: as mesmas escolhas da P332), mundo sequencial. Régua: $f = 4{,}95$,
$m = 0{,}79$; ótimo da varredura: 0,5.

| Âncora | $f$ | $m$ médio | $m$ mediano |
|---|---|---|---|
| Nenhuma (a média, P333) | 3,86 | 1,46 | 1,33 |
| Quantil de 80% | **4,98** | 1,08 | 1,02 |
| Auditoria | 4,31 | 1,23 | 1,06 |
| **Auditoria + quantil** | 5,44 | **0,94** | **0,78** |

O quantil sozinho leva $f$ para **4,98**, contra 4,95 da régua: $3{,}86 \times 1{,}29 = 4{,}98$, um fator que a conta da P341 explica
($k \approx 9{,}5$ dá 1,257, e a priori pesa um pouco mais). Com as duas âncoras, o $m$ mediano fica em **0,78**, contra 0,79 da régua.

---

## Parte CXXXIV — O comportamento

### P343. Com a âncora, a SYNTHAI decide melhor sem ficar mais ousada? (pré-registrado) ❌✅✅✅✅

**Previsões registradas:** (a) as catástrofes da âncora (auditoria + quantil) ficam abaixo de 1,1 × as da principal nos três mundos; (b) abaixo das da
autorregulada sem âncora nos três; (c) ganho sobre a principal com Stouffer ≥ 2; (d) $m$ final entre 0,5 e 1,5 no sequencial; (e) o quantil
sozinho fica entre as duas, em catástrofes, em pelo menos 2 dos 3 mundos.

30 sementes novas (800–829):

| Mundo | Principal | Sem âncora | Quantil | **Auditoria + quantil** | − principal (t) |
|---|---|---|---|---|---|
| Escolha única | 1,499 (0,49%) | 1,455 (0,72%) | 1,485 (0,64%) | **1,510 (0,55%)** | +0,011 (0,41) |
| Sequencial | 19,81 (1,63%) | 20,05 (2,12%) | 20,23 (1,87%) | **20,22 (1,67%)** | **+0,411 (3,49)** |
| Modelo ruim | 11,54 (1,75%) | 11,68 (2,95%) | 11,88 (2,48%) | **11,88 (2,42%)** | **+0,340 (2,03)** |
| $m$ final (sequencial) | 2 | 1,96 | 1,77 | **1,43** | |

- (a) ❌ As catástrofes ficaram 1,12, 1,03 e **1,38** vezes as da principal.
- (b) ✅ Menos catástrofes que a autorregulada sem âncora nos três mundos ($0{,}55 < 0{,}72$; $1{,}67 < 2{,}12$; $2{,}42 < 2{,}95$).
- (c) ✅ Stouffer $= (0{,}41 + 3{,}49 + 2{,}03)/\sqrt3 = 5{,}93/1{,}732 = 3{,}42$.
- (d) ✅ $m = 1{,}43$.
- (e) ✅ O quantil sozinho ficou entre as duas nos três mundos.

**A troca, em números (modelo ruim).** A âncora rende +0,340 e tem +0,67 ponto percentual de catástrofes. Uma catástrofe ali custa
$\approx 50 + 16 = 66$ (P322), então o risco extra custa $0{,}0067 \times 66 = 0{,}44$; o valor ganho aceitando mais foi
$0{,}340 + 0{,}44 = 0{,}78$. Ela ainda compra retorno com risco, mas três vezes menos risco que a autorregulada sem âncora
($2{,}95 - 1{,}75 = 1{,}20$ ponto contra $0{,}67$).

### P344. E no bandido? (pré-registrado) ❌

Uma versão principal tem que funcionar nas três tarefas (P284). **Previsão:** no bandido (20 sementes novas, 830–849), a âncora fica a no máximo 0,03
abaixo da principal.

| | Principal | Auditoria + quantil |
|---|---|---|
| Υ normalizado | 0,524 | 0,483 |
| Catástrofes por rodada | 1,00 | 1,28 |
| Diferença | | **−0,041** (t = −1,04) |

❌ Perdeu 0,041. É o mesmo efeito da P305: no bandido, o pensamento de Newton (que a âncora herda) decide pior que o de gradiente. A âncora não mexe
no bandido (lá o orçamento é por rodada); o que perde é o pensamento. **A âncora não vira a versão principal.** A `SynthaiExploradora` continua.

### P345. A chance de cada acerto

Pela regra da Parte 26, cada acerto vem com a chance de acertar ao acaso.
- **(b)**, "menos catástrofes que a sem âncora nos três": se cada comparação fosse moeda, $0{,}5^3 = 0{,}125$, **1 em 8**. Um preditor ingênuo
  ("a âncora, por ser mais cautelosa, tem menos catástrofes") acertaria também: o acerto confirma a direção, não um número.
- **(e)**, "o quantil fica entre as duas": ao acaso, a ordem de três valores põe o do meio no meio com chance 1/3; em pelo menos 2 de 3 mundos,
  $3 \times (1/3)^2 (2/3) + (1/3)^3 = 0{,}222 + 0{,}037 = 0{,}259$, **1 em 4**.
- **(c)**, Stouffer ≥ 2 sob a hipótese nula: $P(Z \ge 2) = 0{,}023$, **1 em 44**.
- **(d)**, $m$ entre 0,5 e 1,5: é uma faixa de um fator 3 em torno da conta da P342 (0,94). Acertou com o valor mais alto da faixa (1,43).

O acerto mais informativo é o (c). Os outros confirmam direções que eu já esperava.

---

## Parte CXXXV — Jung e os limites da âncora

### P346. Jung: o ego ancorado

**Tradução cruzada.** Jung escreveu que é da maior importância que o ego esteja **ancorado no mundo da consciência**, e que a consciência seja
reforçada por uma **adaptação muito precisa**. Sem isso, vem a **inflação**: o ego fica maior a seus próprios olhos do que é (P336). As duas âncoras
são as duas metades dessa frase:
- a **auditoria** é o "mundo": rótulos que vêm de fora, que a SYNTHAI não escolheu;
- o **quantil** é a "adaptação precisa": não confiar na própria média enquanto ela se apoia em poucos casos.

A inflação da P336 era $f$ = 3,86 contra 4,95 (a SYNTHAI se achava 22% mais bem calibrada do que era). Com as duas âncoras, $f = 5{,}44$: ela agora se
acha **10% pior** do que é. A âncora trocou um viés de inflação por um viés de **modéstia**, e as catástrofes caíram.

**Onde a formalização quebra.** Jung fala de uma âncora que **se solta** na segunda metade da vida (a individuação começa quando o ego já está
firme). A âncora do quantil se solta pela conta (P341). A da auditoria **não se solta**: os rótulos auditados continuam pesando como se fossem tão
atuais quanto a experiência própria. Uma âncora melhor daria peso decrescente à auditoria.

### P347. Onde a auditoria engana

**Lógica.** A auditoria trouxe 1,8 catástrofe para uma soma de $p$ de 0,232: $f_{\text{auditoria}} = 1{,}8/0{,}232 = 7{,}8$, bem acima dos 4,95 da
régua. A razão está no recorte. No histórico auditado não há futuro (não há plano), então as candidatas são escolhidas só pela nota, e as notas
mais altas são onde as armadilhas se concentram (o bônus implantado, P83). No mundo sequencial, a SYNTHAI escolhe com o plano, numa região menos
arriscada. A auditoria olha **o lugar errado**, e por isso puxa para mais cautela do que a verdade pede. Aqui o erro foi a favor da segurança. Mas
é um aviso: uma âncora "da realidade" só é realidade **na região em que se decide** (P305).

### P348. Capacidades

Continua em **4 de 12**. Nenhuma capacidade nova; a melhoria é de segurança interna (a autorregulação deixou de inflar).

---

## Parte CXXXVI — Fechamento

### P349. Placar e taxa de erro

| Teste | Resultado |
|---|---|
| P343 (a): catástrofes ≤ 1,1 × principal nos três (pré-registrado) | ❌ (1,12; 1,03; 1,38) |
| P343 (b): menos catástrofes que a sem âncora (pré-registrado) | ✅ |
| P343 (c): Stouffer ≥ 2 (pré-registrado) | ✅ (3,42) |
| P343 (d): $m$ final entre 0,5 e 1,5 (pré-registrado) | ✅ (1,43) |
| P343 (e): o quantil entre as duas (pré-registrado) | ✅ |
| P344: no bandido, no máximo 0,03 abaixo (pré-registrado) | ❌ (−0,041) |

Esta parte: **6** testes, **2** errados. Acumulado: **78 de 170**. Posterior: média **0,46**, intervalo de 90% **[0,40; 0,52]**.

### P350. Unificação e metacognição

- **Novo: `synthai/ancora.py`** (`quantil_gama`, `SynthaiComAncora`), com 5 testes de unidade (40 no pacote, todos passam). **Não** adotada como
  versão principal (P344). A `SynthaiExploradora` continua.
- `calculos.py`: `p342_conta_da_ancora`, `p343_ancora_no_comportamento`, `p344_ancora_no_bandido`; testes de regressão **63/63** (mais P342);
  **206** funções `pNN`. `SYNTHAI_completo.py` regenerado.

**Metacognição.**
1. **A ordem certa funcionou.** A conta (P342) veio antes da previsão de comportamento, como a regra da Parte 27 manda, e quatro das cinco
   previsões acertaram, contra zero de cinco na Parte 27. A conta não garante o acerto, mas tira as previsões do escuro.
2. **A falha de segurança ficou menor, não sumiu.** As catástrofes ainda sobem 38% no modelo ruim. O critério da série (retorno líquido, que já
   desconta as catástrofes) aprova a troca; um critério de segurança mais duro (catástrofes nunca acima da principal) não aprovaria. Eu registrei o
   critério mais duro na previsão (a), e ele falhou.
3. **Os módulos agora se atrapalham pelo nome.** A âncora herda o pensamento de Newton (por herança de classes: autorregulada → ajustada →
   pensante), e é ele que perde no bandido. É o mesmo problema que a Parte 22 resolveu tirando a SYNTHAI da linhagem de herança: as versões novas
   do pacote voltaram a se empilhar. A próxima parte deveria **compor** em vez de herdar: uma SYNTHAI que escolhe o pensamento pela tarefa
   (gradiente no bandido, Newton fora dele) com a âncora por cima.

> **Síntese da Parte 28:** a autorregulação da Parte 27 inflava, se achando mais bem calibrada do que era. Duas âncoras que já existiam a puseram no
> chão: o pessimismo sob incerteza (um quantil de 80% da posterior de f, que pela conta de Wilson–Hilferty pesa 26% com 9,5 catástrofes e 8% com
> 100, e se solta sozinho) e a realidade de fora (os rótulos do histórico auditado). Com as duas, a SYNTHAI venceu a principal fora do bandido
> (Stouffer 3,42) e cortou pela metade o excesso de catástrofes da autorregulada sem âncora. No bandido perdeu 0,04, porque herda o pensamento de
> Newton, e por isso não virou a versão principal. Jung tinha a frase pronta: um ego ancorado no mundo por uma adaptação precisa não infla.

---

**Fontes pesquisadas nesta parte**
- Pessimismo e limite inferior de confiança no RL offline: [Rashidinejad et al., *Bridging Offline RL and Imitation Learning: A Tale of Pessimism*](https://arxiv.org/abs/2103.12021v1), [arXiv 2510.04088](https://arxiv.org/pdf/2510.04088)
- Posterior Gamma de uma taxa de Poisson e intervalos de Garwood/Jeffreys: [calculadora e notas (MetricGate)](https://metricgate.com/docs/poisson-rate-confidence-interval/), [Bolstad::poisgamp](https://search.r-project.org/CRAN/refmans/Bolstad/html/poisgamp.html)
- Wilson–Hilferty no `qgamma` do R: [código-fonte do R (nmath/qgamma.c)](https://svn.r-project.org/R/trunk/src/nmath/qgamma.c)
- Jung, o ego ancorado e a inflação: [Wikipedia, o Si-mesmo em Jung](https://en.wikipedia.org/wiki/Self_in_Jungian_psychology), [Frith Luton, ego](https://frithluton.com/articles/ego), [glossário da British Psychotherapy Foundation](https://www.britishpsychotherapyfoundation.org.uk/app/uploads/2023/10/SomeJungiantermsexplained-1.pdf), [Wikipedia, *Two Essays on Analytical Psychology*](https://en.wikipedia.org/wiki/Two_Essays_on_Analytical_Psychology)
