# Como eu construiria uma AGI/ASI — Parte 29: compor em vez de herdar, e pensar com mais pesos

> Continuação da [Parte 28](ASI_AGI_parte28_a_ancora.md). **Próxima:** [Parte 30 — hexadecimal e o dicionário](ASI_AGI_parte30_hexadecimal_e_dicionario.md) (P361–P380). Módulos novos: [`synthai/composta.py`](synthai/composta.py) e
> [`synthai/pensamento_rico.py`](synthai/pensamento_rico.py) (testes em [`synthai/testes_composta.py`](synthai/testes_composta.py)). Os números saem
> de `p352_...` a `p357_...` em [`calculos.py`](calculos.py); a saída completa está em [`resultados.txt`](resultados.txt). O projeto inteiro num
> arquivo só: [`SYNTHAI_completo.py`](SYNTHAI_completo.py).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.
>
> **Previsões registradas no commit `792a743`, antes de rodar.** Pedido novo, gravado no `CLAUDE.md`: **o máximo** de cálculos, equações, testes e
> simulações. Esta parte tem uma bateria de equações (B1, B2, B3), 7 testes de unidade novos (47 no pacote), quatro simulações pré-registradas e
> uma conferência de teoria (Takeuchi).

---

## As perguntas desta parte

1. **P351.** Como compor uma SYNTHAI que usa, em cada tarefa, a peça que funciona nela?
2. **P352.** A bateria: as equações das Partes 27–28 (Wilson–Hilferty, delta-método) estão certas em toda a faixa, ou só onde as usei?
3. **P353.** Mais pesos no pensamento: o ganho em especificação paga a variância?
4. **P354.** Com mais pesos, o pensamento fica calibrado onde decide?
5. **P355.** As contas de tamanho: pesos, eventos por peso, otimismo de Akaike.
6. **P356.** A SYNTHAI composta, em sementes novas, nas quatro tarefas.
7. **P357.** Por que a conta de Akaike errou? (Takeuchi)
8. **P358.** Jung: a função transcendente como composição.
9. **P359.** Placar.
10. **P360.** Unificação e metacognição.

---

## Parte CXXXVII — Compor

### P351. Como compor uma SYNTHAI que usa, em cada tarefa, a peça que funciona nela? (↩ P350)

**Na pergunta.** A P350 achou o defeito: as versões novas voltaram a se empilhar por herança (autorregulada → ajustada → pensante → exploradora), e a
âncora herdou um pensamento que perde no bandido. "Compor" é o contrário de "herdar": em vez de **ser** uma versão, **ter** versões.

**Lógica.** O livro *Design Patterns* (1994) diz: "prefira a composição de objetos à herança de classes", e chama a **delegação** de a forma mais
extrema da composição. A `SynthaiComposta` tem duas SYNTHAIs dentro e passa cada decisão para uma delas:
$$
\text{decidir}(s) = \begin{cases} \text{Exploradora}(s) & \text{se } s \text{ é de exploração (bandido)} \\ \text{Ancorada}(s) & \text{senão} \end{cases}
$$
As duas são calibradas com o **mesmo** histórico auditado (um só pedido ao mundo), então cada uma decide exatamente como decidiria sozinha. Os testes
de unidade conferem a **identidade exata**: nos mesmos mundos, a composta dá os mesmos números, até a última casa, que a ancorada fora do bandido e
que a principal no bandido. Um módulo de dentro também pode ser trocado de fora (`composta_rica` troca o pensamento da ancorada pelo rico).

**Tradução cruzada (biologia → engenharia).** É o que o corpo faz com os reflexos: a mão que toca o fogo não consulta o córtex; um circuito
especializado decide naquele tipo de situação, e o córtex decide nos outros. A delegação por **tipo de situação** é a mais antiga das arquiteturas de
controle.

---

## Parte CXXXVIII — A bateria de equações

### P352. As equações das Partes 27–28 estão certas em toda a faixa? (pré-registrado) ✅✅

**B1. Wilson–Hilferty** (o quantil de 80% da Gamma, que a âncora usa), em 17 formas, contra o quantil exato (bissecção na função de distribuição
calculada pela série regularizada):

| Forma $k$ | 0,5 | 1 | 2 | 5 | 9,5 | 25 | 100 |
|---|---|---|---|---|---|---|---|
| Aproximado | 0,8101 | 1,5992 | 2,9851 | 6,7139 | 11,9447 | 29,0783 | 108,3024 |
| Exato | 0,8212 | 1,6094 | 2,9943 | 6,7210 | 11,9502 | 29,0819 | 108,3044 |
| Erro relativo | −1,35% | −0,63% | −0,31% | −0,11% | −0,046% | −0,012% | −0,002% |
| Probabilidade acumulada | 0,7969 | 0,7980 | 0,7986 | 0,7993 | 0,7996 | 0,7998 | 0,7999 |

**Previsão:** para $k \ge 1$, $|P - 0{,}8| \le 0{,}005$ e erro ≤ 1%; para $k = 0{,}5$, erro > 1%. ✅ O erro cai como $\sim 1/k$: de 0,63% em $k = 1$ para
0,0019% em $k = 100$ (fator 330 para $k$ 100 vezes maior).

**B2. O delta-método** para $\mathbb E[1/X \mid X \ge 1]$, $X \sim$ Poisson($\lambda$) (o tamanho do viés de Jensen numa razão de contagens, P334).
Expandindo $g(x) = 1/x$ em torno de $\lambda$ com os momentos centrais da Poisson ($\lambda$, $\lambda$, $\lambda + 3\lambda^2$):
$$
\mathbb E\!\left[\frac1X\right] \approx \frac1\lambda + \frac{\lambda}{\lambda^3} - \frac{\lambda}{\lambda^4} + \frac{\lambda + 3\lambda^2}{\lambda^5}
= \frac1\lambda\left(1 + \frac1\lambda + \frac2{\lambda^2}\right) + O(\lambda^{-4}).
$$

| $\lambda$ | 1 | 2 | 3 | 5 | 9,5 | 15 | 25 | 100 |
|---|---|---|---|---|---|---|---|---|
| Exato | 0,76699 | 0,57659 | 0,43268 | 0,25777 | 0,11994 | 0,07187 | 0,04175 | 0,01010 |
| 2ª ordem: erro | +161% | +30% | +2,7% | −6,9% | −3,0% | −1,1% | −0,35% | −0,02% |
| 3ª ordem: erro | +422% | +73% | +20% | **−0,69%** | **−1,05%** | −0,23% | −0,04% | −0,00% |

**Previsões:** 3ª ordem com erro ≤ 3% para $\lambda \ge 9{,}5$ ✅ (≤ 1,05%); ≥ 10% para $\lambda \le 2$ ✅ (73% e 422%); 3ª ordem melhor que a 2ª para
$\lambda \ge 5$ ✅. A série é **assintótica**: melhora com termos a mais para $\lambda$ grande e piora para $\lambda$ pequeno. Com as ~9,5 catástrofes
de uma SYNTHAI típica (P341), o viés de Jensen numa razão de contagens é $1/\lambda + 2/\lambda^2 = 0{,}105 + 0{,}022 = 12{,}7\%$.

### P355. As contas de tamanho (antes de simular)

$$
\text{pesos} = 1 + d + \frac{d(d+1)}{2} = 1 + 3 + 6 = 10 \quad (d = 3 \text{ variáveis: discordância, nota − melhor, leitura}).
$$

| | Sequencial | Escolha única |
|---|---|---|
| Amostras no histórico ($n$) | 150 × 50 = 7.500 | 150 × 200 = 30.000 |
| Catástrofes no histórico | 37,3 | 150 (medidas: 147,1) |
| Eventos por peso, linear (3) | 37,3/3 = **12,4** | 150/3 = 50 |
| Eventos por peso, rico (9) | 37,3/9 = **4,1** | 150/9 = 16,7 |
| Otimismo de Akaike $k/n$, linear | 4/7.500 = 0,00053 | 4/30.000 = 0,00013 |
| Otimismo de Akaike $k/n$, rico | 10/7.500 = 0,00133 | 10/30.000 = 0,00033 |

Pela regra de Peduzzi et al. (1996), abaixo de ~10 eventos por peso os coeficientes ficam instáveis. A conta previa: o rico **ganha** na escolha única
(16,7) e **perde** no sequencial (4,1).

---

## Parte CXXXIX — Mais pesos

### P353. O ganho em especificação paga a variância? (pré-registrado) ⚠️✅❌

Histórico de treino (150 passos) e de teste (300 passos novos), log-perda média por amostra, Newton (o rico com ridge λ = 1):

| Mundo | Linear: treino → teste (otimismo) | Rico: treino → teste (otimismo) | Rico no teste |
|---|---|---|---|
| Sequencial | 0,00953 → 0,01095 (0,00142) | 0,00851 → **0,01015** (0,00164) | **−7%** |
| Escolha única | 0,01000 → 0,00927 (−0,00073) | 0,00833 → **0,00782** (−0,00050) | **−16%** |

- (a) Otimismo do rico − do linear a um fator 2 de $6/n$: sequencial 0,00022 (faixa 0,0004–0,0016) ❌; escolha única 0,00023 (faixa 0,0001–0,0004)
  ✅. Conta como ❌ (a previsão era para os dois).
- (b) ✅ Na escolha única, o rico tem menos perda no teste (−16%).
- (c) ❌ No sequencial **também** (−7%), apesar dos 4,1 eventos por peso.

**Por que (c) errou.** A regra dos 10 eventos por peso fala de **viés nos coeficientes**, não de erro de **previsão** (o próprio debate posterior,
Riley et al. 2019, trocou a regra por critérios de desempenho). E o ridge (uma priori normal de variância 1 nos pesos) segura a variância. O ganho de
especificação (o linear não consegue representar que o risco sobe **e depois desce** com a nota) foi maior que o custo.

### P357. Por que a conta de Akaike errou? (Takeuchi; conferência de teoria, depois de ver a P353)

**Lógica.** Akaike supõe o modelo **certo**. Com o modelo mal especificado, o otimismo esperado é o critério de Takeuchi (1976):
$$
\mathbb E[\text{teste} - \text{treino}] \approx \frac{\operatorname{tr}(J I^{-1})}{n}, \qquad
J = \frac1n\sum (y_i - p_i)^2\, x_i x_i^\top, \qquad I = \frac1n \sum p_i(1-p_i)\, x_i x_i^\top .
$$
Com o modelo certo, $J = I$ e o traço vale $k$ (Akaike).

| Mundo | tr linear | tr rico | Δ/n de Takeuchi | Δ/n de Akaike | Δ medido |
|---|---|---|---|---|---|
| Sequencial | 4,23 | 7,82 | (7,82 − 4,23)/7.500 = **0,00048** | 6/7.500 = 0,00080 | 0,00022 |
| Escolha única | 4,69 | 8,79 | (8,79 − 4,69)/30.000 = **0,00014** | 6/30.000 = 0,00020 | 0,00023 |

Dois resultados. (1) O rico "gasta" **7,8 a 8,8 pesos efetivos**, não 10: o ridge encolhe os pesos que os dados não sustentam. (2) Takeuchi fica mais
perto do medido que Akaike no sequencial (0,00048 contra 0,00080, para 0,00022). As duas contas ainda erram por um fator ~2, porque a diferença
medida tem seu próprio ruído (o otimismo do linear na escolha única deu **negativo**, −0,00073: o histórico de teste por acaso foi mais fácil). Uma
conta de otimismo com 10 sementes tem barra de erro do mesmo tamanho que a conta.

### P354. Com mais pesos, o pensamento fica calibrado onde decide? (pré-registrado) ❌

O fator $f$ (real / previsto nas opções aceitas sem perguntar, P316), limiar fixo $2P^\*$, sementes das P316/P322:

| Mundo | Linear (Newton) | **Rico** | Previsão |
|---|---|---|---|
| Escolha única | 6,15 | **3,05** | entre 0,5 e 2,5 ❌ |
| Sequencial | 4,95 | **1,71** | entre 0,5 e 3,0 ✅ |

A subestimação do risco onde se decide caiu pela metade na escolha única e quase sumiu no sequencial (1,71). A previsão era para os dois mundos e
falhou num deles: ❌. Mas a direção é a da tese das Partes 24–25: **o defeito era de especificação**, e mais pesos o reduzem.

---

## Parte CXL — A SYNTHAI composta

### P356. A composta, em sementes novas, nas quatro tarefas (pré-registrado)

**Previsões registradas:** (a) no bandido, a composta (e a composta rica) é **idêntica** à principal, diferença exatamente 0; (b) Stouffer ≥ 2 nos três
mundos sem bandido; (c) catástrofes ≤ 1,4 × as da principal em cada um; (d) o pensamento rico ganha da composta na escolha única e perde no
sequencial; (e) o rico tem menos catástrofes na escolha única.

30 sementes novas (850–879; bandido: 20, 880–899):

| Tarefa | Principal | **Composta** | − principal (t) | Composta rica | rica − composta (t) |
|---|---|---|---|---|---|
| Escolha única | 1,4950 (0,49%) | 1,5005 (0,57%) | +0,005 (0,20) | 1,4671 (0,59%) | −0,033 (−1,17) |
| Sequencial | 19,913 (1,56%) | **20,250** (1,67%) | **+0,337 (3,39)** | 20,276 (1,69%) | +0,026 (0,23) |
| Modelo ruim | 11,357 (1,99%) | **11,826** (2,39%) | **+0,469 (3,49)** | 11,857 (2,28%) | +0,031 (0,26) |
| Bandido (Υ) | 0,60307 (0,68) | **0,60307** (0,68) | **0 exato** | 0,60307 | 0 exato |

- (a) ✅ No bandido, as três dão o **mesmo número até a última casa**: a composição é exata.
- (b) ✅ Stouffer $= (0{,}20 + 3{,}39 + 3{,}49)/\sqrt3 = 7{,}08/1{,}732 = 4{,}08$. Ao acaso, $P(Z \ge 4{,}08) \approx 2 \times 10^{-5}$. Contra um preditor
  ingênuo ("a composta é a ancorada fora do bandido, e a ancorada já ganhou na P343"), o acerto é esperado: a novidade não é o ganho, é o ganho
  **sem perda** no bandido.
- (c) ✅ Catástrofes: $0{,}57/0{,}49 = 1{,}15$; $1{,}67/1{,}56 = 1{,}07$; $2{,}39/1{,}99 = 1{,}20$, todas ≤ 1,4.
- (d) ❌ O pensamento rico não mudou o comportamento (−0,033 e +0,026, t < 1,2).
- (e) ❌ Nem as catástrofes (0,59% contra 0,57%).

**A composta vira a versão principal.** Ela foi desenhada depois da P343/P344 e validada em sementes de controle novas (850–899), como a regra
pede. Ganha onde a ancorada ganha e é exatamente a principal antiga no bandido: é uma melhoria **de Pareto** nas quatro tarefas, em retorno.

**O pensamento rico, de novo.** Ele previu melhor (−7% e −16% de perda no teste, P353) e ficou mais bem calibrado onde decide (P354), e mesmo assim
não decidiu melhor. É o padrão das Partes 23–25 pela terceira vez: medir melhor uma peça não basta. Aqui a explicação mais provável é que a
autorregulação (P331) ajusta o limiar ao pensamento que tiver: um pensamento mais bem calibrado leva a um limiar diferente, e o resultado final
fica parecido. A âncora **compensa** o pensamento, que é o que ela foi feita para fazer.

---

## Parte CXLI — Jung, placar e unificação

### P358. Jung: a função transcendente como composição

**Tradução cruzada.** Jung chamava de **função transcendente** o que nasce do encontro de dois opostos sem que nenhum vença: um terceiro que contém
os dois. A herança de classes é o contrário: a versão nova **substitui** a antiga, e o que a antiga sabia fazer melhor se perde (a Parte 28 perdeu o
bandido). A composição mantém as duas e as **põe em relação**: a exploradora onde explorar importa, a ancorada onde a cautela calculada importa. É a
quaternidade de Jung num grão menor: funções diferenciadas (P301), cada uma no seu domínio, sob um centro que não é nenhuma delas.

**Onde a formalização quebra.** A composta escolhe a peça por um sinal **dado pelo mundo** (a situação diz se é de exploração). Na psique, a
escolha de qual função usar é ela mesma um problema, e Jung dizia que é aí que mora a unilateralidade. Uma SYNTHAI que **aprendesse** qual peça usar
em cada situação seria o próximo passo.

### P359. Placar e taxa de erro

| Teste | Resultado |
|---|---|
| B1: Wilson–Hilferty em 17 formas (pré-registrado) | ✅ |
| B2: delta-método, 9 valores de λ (pré-registrado) | ✅ |
| P353 (a): otimismo a um fator 2 de 6/n nos dois mundos (pré-registrado) | ❌ |
| P353 (b): o rico ganha no teste na escolha única (pré-registrado) | ✅ (−16%) |
| P353 (c): o rico perde no teste no sequencial (pré-registrado) | ❌ (ganha 7%) |
| P354: f do rico nas duas faixas (pré-registrado) | ❌ (3,05 fora; 1,71 dentro) |
| P356 (a): bandido idêntico (pré-registrado) | ✅ |
| P356 (b): Stouffer ≥ 2 (pré-registrado) | ✅ (4,08) |
| P356 (c): catástrofes ≤ 1,4× (pré-registrado) | ✅ |
| P356 (d): o rico ganha na única e perde no sequencial (pré-registrado) | ❌ |
| P356 (e): o rico com menos catástrofes (pré-registrado) | ❌ |

Esta parte: **11** testes, **5** errados. Acumulado: **83 de 181**. Posterior: média **0,46**, intervalo de 90% **[0,40; 0,52]**.

### P360. Unificação e metacognição

- **Nova versão principal: `synthai.SynthaiComposta`** (P356), exportada pelo pacote. Linhagem: … → `SynthaiExploradora` (P295) ⇒
  **`SynthaiComposta`** (P356): a exploradora no bandido, a ancorada (P343) fora dele.
- **Novos módulos:** `composta.py` (composição por delegação) e `pensamento_rico.py` (10 pesos, Newton com ridge); `ajustar_logistica` ganhou a
  opção `ridge` (com 0, igual ao antigo, testado). 7 testes de unidade novos: **47 no pacote, todos passam**.
- `calculos.py`: a bateria (`p352_...`), o pensamento rico (`p353`, `p354`), a composta (`p356`) e Takeuchi (`p357`). Testes de regressão **65/65**
  (mais P352 e P355); **213** funções `pNN`. `SYNTHAI_completo.py` regenerado.

**Metacognição.**
1. **O máximo de cálculos mudou o tipo de acerto.** A bateria (B1, B2) acertou tudo e mostrou **onde** as fórmulas das Partes 27–28 deixam de valer
   (Wilson–Hilferty abaixo de forma 1; o delta-método abaixo de λ ≈ 5). Antes eu só tinha conferido as fórmulas nos pontos em que as usava.
2. **As contas de tamanho erraram, e por um bom motivo.** A regra dos 10 eventos por peso e a conta de Akaike supõem coisas (coeficientes,
   modelo certo) que não valiam. Takeuchi, que não supõe o modelo certo, chegou mais perto. É a regra da Parte 23 de novo: antes de usar uma
   resposta pronta, verificar as premissas dela.
3. **A melhor decisão da parte foi de arquitetura, não de estatística.** O pensamento com mais pesos foi o maior ganho de **medida** (−16% de perda,
   f de 6,15 para 3,05) e o menor de **comportamento** (zero). A composição foi o menor esforço de código (60 linhas) e o maior ganho de
   comportamento (Stouffer 4,08, empate exato no bandido).

> **Síntese da Parte 29:** a SYNTHAI deixou de herdar e passou a compor: uma versão nova que tem as duas melhores antigas e passa cada decisão para a
> que funciona naquele tipo de tarefa. Em sementes novas, ela ganhou da principal fora do bandido (Stouffer 4,08) e foi idêntica a ela no bandido,
> até a última casa: virou a versão principal. A bateria de equações conferiu Wilson–Hilferty em 17 formas e o delta-método em 9 valores, e mostrou
> onde cada um deixa de valer. O pensamento com 10 pesos previu 7% a 16% melhor e ficou mais bem calibrado onde decide, mas não decidiu melhor: a
> âncora compensa o pensamento que tiver. Jung chamaria a composta de função transcendente em miniatura: um terceiro que contém os dois.

---

**Fontes pesquisadas nesta parte**
- Composição em vez de herança, e delegação: [Wikipedia, *Design Patterns*](https://en.wikipedia.org/wiki/Design_Patterns), [notas de curso (Freiburg)](https://proglang.informatik.uni-freiburg.de/teaching/swt/2012/design-patterns.pdf), [KSU, Gang of Four](https://textbooks.cs.ksu.edu/cc410/i-oop/09-design-patterns/02-gang-of-four/)
- Eventos por variável (Peduzzi et al., 1996) e o debate posterior: [BMC Med Res Methodol (2016)](https://link.springer.com/article/10.1186/s12874-016-0267-3), [PMC5045274](https://pmc.ncbi.nlm.nih.gov/articles/PMC5045274), [CASRAI](https://casrai.org/guides/events-per-variable-and-the-minimum-sample-size-for-regression)
- Otimismo de Akaike e Takeuchi: [Lin, AIC](https://web.stanford.edu/~linkewei/blog/aic), [arXiv 1911.10191](https://arxiv.org/pdf/1911.10191), [MetricGate, AIC e KL](https://metricgate.com/blogs/aic-and-kl-divergence-link/)
- Delta-método e momentos inversos: [Wikipedia, Delta method](https://en.wikipedia.org/wiki/Delta_method), [Cichoń, Delta Method](https://cs.pwr.edu.pl/cichon/prace/DeltaMethod.pdf)
- Wilson–Hilferty e o quantil da Gamma: [código-fonte do R (qgamma.c)](https://svn.r-project.org/R/trunk/src/nmath/qgamma.c), [EnvStats::eqgamma](https://search.r-project.org/CRAN/refmans/EnvStats/html/eqgamma.html)
