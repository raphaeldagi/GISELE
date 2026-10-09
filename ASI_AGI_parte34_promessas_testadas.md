# Como eu construiria uma AGI/ASI — Parte 34 (0x22): as promessas testadas em casos novos

> Continuação da [Parte 33](ASI_AGI_parte33_pos_asi_auditada.md). As Partes 31–33 deixaram contas feitas **depois** de ver os resultados e
> promessas para "a próxima parte". Pela regra da Parte 25, uma conta posterior só vira evidência quando prevê um caso **novo**. Esta parte é
> esse teste. Novidades no código: `ThompsonMorris` em [`synthai/decisao.py`](synthai/decisao.py); `NaiveBayesContagens` e `LogisticaSGD` em
> [`synthai/dicionario.py`](synthai/dicionario.py); testes em [`synthai/testes_parte34.py`](synthai/testes_parte34.py); números de `p461_...` a
> `p465_...` em [`calculos.py`](calculos.py). Diálogo, rodada 5: [`dialogo/DIALOGO.md`](dialogo/DIALOGO.md).
>
> **Contas e previsões no commit `9690359`, antes de qualquer execução.** Legenda: ✅ ⚠️ ❌.

---

## As perguntas desta parte

1. **P461 (0x1CD).** As duas cotas do Q-learning (P407) preveem um α novo? ↩ P407
2. **P462 (0x1CE).** A taxa de renovação ótima é a taxa de mudança do mundo? ↩ P439
3. **P463 (0x1CF).** Zipf–Mandelbrot, ajustado num corpus, prevê outro? ↩ P383
4. **P464 (0x1D0).** O dicionário no lugar do ML: contagens contra gradiente, em aprendizado contínuo. ↩ P406
5. **P465 (0x1D1).** Um dígito hex de expoente basta para a memória de Thompson? (o contador de Morris) ↩ P411
6. **P466 (0x1D2).** Jung: a função inferior e o modelo errado.
7. **P467 (0x1D3).** O diálogo, rodada 5: `sum` não é soma, `**2` não é quadrado.
8. **P489 (0x1E9).** Placar. **P490 (0x1EA).** Unificação.

---

### P461 (0x1CD). As cotas do Q-learning preveem α = 0,05? (pré-registrado) ✅❌

**Na pergunta.** A P407 achou duas cotas para o Q-learning ε-guloso: sem aprisionamento (só o ruído do passo constante) e com aprisionamento (sem
ruído). A medida em α = 0,1 caiu entre elas. "Prever" pede mais que cair no intervalo: pede **onde** no intervalo.

**Lógica.**
- Cota 1 (ruído estacionário): variância de Q = α/(2 − α)·p(1 − p). Com α = 0,05: 0,05/1,95 = 0,0256, metade da de α = 0,1 (0,0526). Menos ruído,
  menos erros gulosos: **99,0** (contra 120,6 em α = 0,1).
- Cota 2 (aprisionamento): o melhor braço só passa o guloso quando p*(1 − (1 − α)ⁿ) > p_g. Com α = 0,05, n = ln(1 − p_g/p*)/ln 0,95: para
  p_g/p* = 0,8, n = −1,609/−0,0513 = 31,4 puxadas (o dobro das 15,3 de α = 0,1). Média: **387,7** (contra 266,9).
- Em α = 0,1, a medida (185,4) ficou na fração (185,4 − 120,6)/(266,9 − 120,6) = 64,8/146,3 = **0,443** do intervalo. Mesma fração em α = 0,05:
  99,0 + 0,443 × (387,7 − 99,0) = 99,0 + 127,9 = **226,9**.

**Medido: 311,0.** (a) dentro das cotas [99,0; 387,7] ✅. (b) a ±20% de 226,9, [181,5; 272,3] ❌. A fração foi (311,0 − 99,0)/288,7 = **0,734**.

**Por quê.** A fração não é constante: com α menor, o ruído (que ajuda a sair do aprisionamento) cai **e** o aprisionamento dura mais. Os dois
efeitos empurram para o lado da cota 2. *Contra o ingênuo:* "α menor, estimativas melhores, menos arrependimento" previa abaixo de 185,4; o
medido é 68% **maior**. As cotas acertaram a direção que o ingênuo erra.

**Tradução cruzada.** Aprender devagar (α pequeno) é ser fiel à primeira impressão: menos ruído, mais preconceito.

### P462 (0x1CE). A taxa de renovação ótima é a taxa de mudança? (pré-registrado) ❌❌

**Lógica, a conta antes.** Bandido de 10 braços cujas médias são sorteadas de novo a cada 500 passos, T = 4000: Υ = 7 quebras. Garivier e
Moulines (2011), para o UCB descontado: γ = 1 − ¼√(Υ/T) = 1 − 0,25 × √(7/4000) = 1 − 0,25 × 0,04183 = **0,9895**; memória 1/(1 − γ) = **95,6**
passos.

**Medido** (arrependimento contra o melhor braço do momento, 50 sementes):

| γ | 0,95 | 0,98 | 0,99 | **0,995** | 0,999 | 1 (exato) |
|---|---|---|---|---|---|---|
| arrependimento | 801,6 | 541,4 | 425,5 | **380,2** | 549,7 | 808,7 |
| memória 1/(1 − γ) | 20 | 50 | 100 | **200** | 1000 | ∞ |

(c) o melhor é 0,99 ❌ (é 0,995). (d) o exato tem mais que o dobro de 0,99 ❌ (808,7/425,5 = 1,90).

**Por quê.** A fórmula de Garivier–Moulines é para o UCB e para o pior caso. Thompson aproveita melhor uma memória longa. O ótimo medido, **200
passos = 0,4 do período de 500**, diz: lembre-se de menos que um período, mas não de muito menos. **A curva tem a forma prevista** (um vale entre
esquecer demais, γ = 0,95, e não esquecer nada, γ = 1, que custam quase o mesmo: 801,6 e 808,7), e o fundo do vale fica a um fator 2 da conta.

**Tradução cruzada.** É a P439 completa: a renovação ótima depende de quanto o mundo muda. Lembrar 40% do tempo de uma "era" é o ponto em que a
memória ainda informa e já não engana.

### P463 (0x1CF). Zipf–Mandelbrot prevê outro corpus? (pré-registrado) ✅✅

**Na pergunta.** A P383 errou porque Zipf puro, f(r) ∝ r^−s, supõe que a cabeça (as palavras mais frequentes) segue a mesma potência que o
resto. Mandelbrot acrescenta um deslocamento: f(r) ∝ (r + q)^−s, que achata a cabeça.

**Lógica.** Ajuste por grade nas definições dos **substantivos**, só pela cobertura em k ≤ 1000: **s = 1,08, q = 64**. Previsão para as definições
dos **verbos** (outro corpus, com o seu próprio N), cobertura Σ_{r≤k}(r + q)^−s / Σ_{r≤N}(r + q)^−s:

| k | Zipf–Mandelbrot (previsto) | Zipf puro, q = 0 | **medido nos verbos** | erro |
|---|---|---|---|---|
| 100 | 22,3% | 63,2% | 25,2% | 2,9 pontos |
| 500 | 49,3% | 78,1% | **49,4%** | **0,15** |
| 2000 | 74,9% | 89,4% | **76,7%** | **1,8** |
| 4000 | 87,2% | 94,7% | **88,8%** | **1,6** |

(e) ±5 pontos em 500, 2000 e 4000 ✅; (f) melhor que Zipf puro em cada k ✅. *Ao acaso:* uma faixa de 10 pontos acertada três vezes, com o ingênuo
(Zipf puro, o modelo da P383) errando por 29, 13 e 6 pontos.

**Tradução cruzada.** q = 64 diz que as ~64 palavras mais frequentes das definições se comportam como **uma** classe achatada: são as palavras de
função que sobreviveram ao filtro, todas quase igualmente frequentes.

**Meta.** Ajustado num corpus, testado noutro: é o primeiro acerto de forma funcional nesta trilha que não foi visto antes.

### P464 (0x1D0). O dicionário no lugar do ML (pré-registrado) ❌✅✅❌

**Na pergunta.** A P406 propôs: usar o dicionário como vocabulário de atributos e um modelo de contagens (estatística suficiente) no lugar do
gradiente. O teste: prever a classe gramatical de cada sinset (substantivo, verbo, adjetivo, advérbio) pelas palavras da sua definição. Tarefa A:
sinsets cujo primeiro lema vai de *a* a *m* (55.457); depois tarefa B, de *n* a *z* (48.338); teste: 13.864 sinsets de A, separados.

**Medido** (acurácia no teste de A):

| | depois de A | depois de B |
|---|---|---|
| Naive Bayes (contagens) | 78,3% | 78,9% |
| logística por SGD (uma passada) | 82,1% | **83,3%** |

(g) Naive Bayes ≥ 80% ❌ (78,3%). (h) Naive Bayes não esquece ✅ (+0,6). (i) o SGD não esquece quando as tarefas não conflitam ✅ (+1,2). (j)
Naive Bayes > SGD ❌ (−4,4 pontos).

**O achado, e é contra mim.** A troca da Parte 32 **não** é universal:
1. **Esquecimento catastrófico exige conflito.** As duas tarefas têm o mesmo mapeamento (as palavras da definição dizem a classe do mesmo jeito em
   *a–m* e em *n–z*); o SGD só melhorou com B. A P403 tinha conflito (os mesmos pesos serviam a regiões diferentes da função); aqui não há.
2. **O Bayes exato só é exato para o seu modelo.** O Naive Bayes supõe que as palavras de uma definição são **independentes** dada a classe. Não
   são ("to make", "of or relating to"). A logística não supõe isso. Pitman–Koopman–Darmois garante a estatística suficiente **do modelo**; se o
   modelo está errado, a estatística é suficiente para a coisa errada.

**Tradução cruzada.** Contar sem entender a estrutura é como ler um texto palavra por palavra sem ler as frases.

**Meta.** A saída a testar é uma família exponencial **sem** a independência: a regressão logística bayesiana (sem estatística suficiente
finita, aproximada pela de Laplace) ou o Bayes sobre **pares** de palavras (o que a Rodada 6 do diálogo vai tentar).

### P465 (0x1D1). Um dígito hex de expoente basta? (o contador de Morris) (pré-registrado) ✅✅

**Lógica, a conta antes.** O contador de Morris (1978) guarda só o expoente c (0..15, **um dígito hex**); cada sucesso incrementa c com chance
2^−c; a contagem estimada 2^c − 1 não tem viés (E[2^c] = n + 1) e tem variância n(n − 1)/2 (desvio relativo ≈ 1/√2 = 71%). Dois dígitos hex por
braço guardam contagens até 2¹⁵ = 32.768. Sorteando contagens de Morris de braços com n = 200 puxadas e a regra de Thompson: **73,1**.

**Medido: 76,9** (+5,2% da conta); Morris − completo = +46,2, dp 74,0, **t = 6,24**. (k) em [49, 110] ✅; (l) pior que o completo, t > 3 ✅.

**Comparação na trilha hex** (mesmos braços e sementes da P401):

| memória por braço | bits | arrependimento |
|---|---|---|
| contagens completas | 22 | 30,7 |
| teto 256 (2 dígitos por contagem) | 16 | 33,4 |
| **Morris (1 dígito de expoente por contagem)** | **8** | **76,9** |
| teto 16 (1 dígito por contagem) | 8 | 93,7 |

Com os mesmos 8 bits por braço, guardar o **expoente** (Morris) é melhor que guardar a contagem **saturada** (teto 16): 76,9 contra 93,7. O ruído
de Morris (71%) custa menos que o teto, que nunca deixa a crença ficar firme.

**Tradução cruzada.** Lembrar "a ordem de grandeza" de quantas vezes algo aconteceu é melhor que lembrar exatamente, mas só até 16.

---

### P466 (0x1D2). Jung: a função inferior e o modelo errado

Em Jung, a **função inferior** é a que o tipo usa mal, e ela erra de um jeito sistemático, não ao acaso. O Naive Bayes é um tipo cuja função
inferior é a **estrutura** (ele não vê como as palavras se combinam); por isso perde para o SGD mesmo sem esquecer nada. **Onde funciona:** o erro
do modelo errado é sistemático e não diminui com mais dados (78,3 → 78,9 com o dobro de exemplos). **Onde quebra:** em Jung a função inferior
pode ser desenvolvida (individuação); um modelo não ganha a estrutura que não tem com mais dados. Precisa ser trocado.

### P467 (0x1D3). O diálogo, rodada 5

As duas linguagens implementaram a regra de aceitação sem maldição do vencedor (pai e filho reavaliados juntos, t > 3) com o mesmo gerador
congruencial de 64 bits. **Mesmos 3 aceites em 200, mesmo SHA-256, mesmos t bit a bit (m) ✅.** As duas lições: o `sum()` do Python 3.12+ é
**compensado** (Neumaier), e a IA-Java o reescreveu para dar os mesmos bits; e `x**2` (o `pow` da libm) difere de `x*x` em **1.643 de 2 milhões**
de casos (0,08%), sendo `x*x` o corretamente arredondado. "O significado de um programa está nos bits que ele produz."

### P489 (0x1E9). Placar

| (a) cotas α 0,05 | ✅ | (h) Naive Bayes não esquece | ✅ |
|---|---|---|---|
| (b) ±20% de 226,9 | ❌ | (i) SGD sem conflito não esquece | ✅ |
| (c) melhor γ = 0,99 | ❌ | (j) Naive Bayes > SGD | ❌ |
| (d) exato > 2× γ 0,99 | ❌ | (k) Morris em [49, 110] | ✅ |
| (e) Mandelbrot ±5 pontos | ✅ | (l) Morris pior que completo | ✅ |
| (f) Mandelbrot > Zipf puro | ✅ | (m) rodada 5 bit a bit | ✅ |
| (g) Naive Bayes ≥ 80% | ❌ | | |

Parte 34: 13 testes, 5 erros. Acumulado: **110 erros em 271 testes**; taxa média 0,41, intervalo 90% [0,36; 0,46].

### P490 (0x1EA). Unificação e metacognição

- **Novos:** `ThompsonMorris`, `NaiveBayesContagens`, `LogisticaSGD`; **3 testes novos: 89 no pacote**. Regressão: + P462 (γ de Garivier–Moulines).
- **Versão principal:** continua a `SynthaiComposta`.

**Metacognição.**
1. **As promessas valeram pela metade.** As contas posteriores acertaram a direção e o formato (cotas, o vale da renovação, Mandelbrot) e erraram a
   posição (a fração entre as cotas, o fundo do vale). Uma conta posterior que acerta a forma mas não o número é um modelo **qualitativo**: útil,
   não suficiente.
2. **A Parte 32 exagerou e esta parte corrigiu.** "Trocar o ML pelo Bayes exato" vale onde o modelo é certo e as tarefas conflitam. No dicionário,
   com um modelo errado (independência) e sem conflito, o gradiente venceu. A frase certa é mais estreita: **o Bayes exato vence quando o modelo
   exponencial é verdadeiro; o gradiente vence quando a estrutura importa mais que a memória.**
3. **O melhor acerto da parte é o que eu menos esperava:** Mandelbrot ajustado nos substantivos previu os verbos a 0,15 ponto em k = 500.

> **Síntese da Parte 34:** testadas em casos novos, as contas posteriores das partes anteriores acertaram a forma e erraram a posição. As cotas do
> Q-learning contiveram α = 0,05 (311,0 em [99,0; 387,7]), mas a fração entre elas mudou de 0,44 para 0,73. A renovação ótima num mundo que muda a
> cada 500 passos foi uma memória de 200 (0,4 do período), não a de Garivier–Moulines (96). Zipf–Mandelbrot ajustado nos substantivos previu as
> definições dos verbos a menos de 2 pontos. No dicionário, o Naive Bayes não esqueceu nada e ainda assim perdeu para o SGD (78,9% contra 83,3%),
> porque o modelo dele é falso e as tarefas não conflitavam. Com um dígito hex de expoente (Morris), Thompson perde menos que com a contagem
> saturada no mesmo espaço. E as duas IAs aprenderam que `sum` não é soma e `**2` não é quadrado.

---

**Fontes pesquisadas nesta parte**
- Bandidos não estacionários, desconto e janela deslizante (γ = 1 − ¼√(Υ/T)): Garivier e Moulines (2011), *On Upper-Confidence Bound Policies for Switching Bandit Problems*, citado pelas revisões da [Parte 32](ASI_AGI_parte32_decisao_exata_e_autopoiese.md); [Bayesian Forgetting in Continual Learning](https://www.academia.edu/164772657/Bayesian_Forgetting_in_Continual_Learning)
- Zipf e Mandelbrot: [Piantadosi (2014), PMC4176592](https://pmc.ncbi.nlm.nih.gov/articles/PMC4176592)
- Estatística suficiente e o limite do Bayes exato: [Learning to Continually Learn with the Bayesian Principle, arXiv 2405.18758](https://arxiv.org/pdf/2405.18758)
- A soma de floats do Python 3.12+ e o `pow`: verificados nesta máquina (`sum([1.0, 1e100, 1.0, -1e100]) = 2.0`; `x**2 != x*x` em 1.643 de 2·10⁶)
- Contador de Morris: Morris (1978), *Counting large numbers of events in small registers*; as propriedades (sem viés, variância n(n − 1)/2) conferidas pelo teste de unidade (4000 contadores, erro < 5%)
