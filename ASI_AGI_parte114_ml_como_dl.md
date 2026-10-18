# Parte 114 — Tratar o ML como DL e o DL como ML (0x72)

↩ Parte 110 (a dúvida calculada: o ML e o DL) · ↩ Parte 96 (aprender a base: a MLP como features) · ↩ Parte 97 (a cumeeira; os parâmetros contra n) · ↩ Parte 31 (substituir aprendizado por conta exata "se der")

> Pedido do usuário: "Trate o ML como DL e vice-versa."
>
> **A leitura escolhida (regra da Parte 83, escrita ANTES de medir).** "ML" é o aprendizado de máquina clássico: modelos convexos ou de forma fechada (logística, mínimos quadrados, ridge), solucionadores exatos (Newton, equações normais) e medidas clássicas de complexidade (graus de liberdade). "DL" é a rede: camadas, ativações, treino por retropropagação e descida do gradiente. As duas travessias:
> - **ML como DL:** escrever o modelo clássico como uma rede e treiná-lo como rede. A logística com L2 é uma rede de UMA camada (linear + sigmoide + entropia cruzada); treinada por retropropagação, tem de chegar ao ponto do Newton, porque o problema é fortemente convexo. É uma identidade por teorema, não uma esperança.
> - **DL como ML:** ler a rede pelas ferramentas clássicas.
>   - Uma rede LINEAR profunda (W₂W₁, sem ativação) é um modelo linear sobreparametrizado: deve dar o OLS.
>   - A camada oculta de uma rede são FEATURES. Com elas fixas (aleatórias ou aprendidas), a cabeça é uma ridge em forma fechada.
>   - Os GRAUS DE LIBERDADE de Efron (Σ cov(ŷᵢ, yᵢ)/σ²), uma medida clássica, valem para a cabeça de uma rede e batem com tr(S).
>
> O módulo é `synthai/ml_dl.py`.
>
> **Antes do registro.**
> - **Para (a), as CONDIÇÕES do teorema nos dados do teste** (que não revelam o resultado): μ = λ = 0,01 (convexidade forte), L = λ + λ_max(XᵀX/n)/4 = 0,3272 (suavidade, porque σ′ ≤ 1/4), κ = 32,7. A cota ‖w*‖ ≤ ‖∇f(0)‖/μ = 35,45. Com o passo 1/L, ‖w_T − w*‖ ≤ (1 − μ/L)^(T/2)·‖w*‖, e em T = 2.000 isso dá ≤ 35,45·e^(−1000·0,0306) ≈ 5·10⁻¹².
> - **Para (b) a (i), a calibração na semente 7** (o teste é a 114):
>   - rede linear profunda contra OLS: 8,9·10⁻¹⁶;
>   - MSE de teste: features aleatórias + ridge **0,01306**; rede por retropropagação **0,01567** (razão 1,20); features treinadas + ridge **0,01381** (razão 0,88 da retropropagação);
>   - graus de liberdade com λ = 10⁻³: tr(S) = 35,42 contra Efron 35,21; com λ = 1: 17,90 contra 18,10 (razão 0,505).
>   - Uma surpresa da calibração, que vira previsão: a camada oculta ALEATÓRIA com a cabeça exata bateu a rede INTEIRA treinada. Mecanismo suposto: 3.000 passos de gradiente não resolvem nem a cabeça (um problema de mínimos quadrados mal condicionado), e a forma fechada a resolve num passo.

## As perguntas desta parte

1. **P2861 (0xB2D).** A logística como rede de uma camada, treinada por retropropagação, chega ao mesmo ponto que o Newton? ↩ P2741
2. **P2862 (0xB2E).** A rede linear profunda (duas camadas, sem ativação) chega ao OLS? ↩ P2744
3. **P2863 (0xB2F).** A camada oculta de uma rede, lida como features (ML), com a cabeça em forma fechada, ganha ou perde da rede inteira treinada (DL)? ↩ P2321
4. **P2864 (0xB30).** Os graus de liberdade clássicos valem para a cabeça de uma rede? ↩ P2357
5. **P2865 (0xB31).** O treino da rede linear profunda acrescenta fronteira entre Python e Java? (rodada 81) ↩ P2836

## Previsões pré-registradas (ANTES de medir — este commit)

**As fixtures (regra da Parte 111).**
- Logística: `dados_logistica(300, 114)`, λ = 0,01, Newton com 30 iterações; a rede com lr = 1/L e T = 2.000 passos, a partir de zero.
- Regressão: treino `dados_regressao(200, 114)`, teste `dados_regressao(1000, 114114)`.
- Rede linear profunda: d = 3 (x₁, x₂, 1), h = 4, 3.000 passos, lr 0,02, inicialização N(0; 0,1²), semente 114.
- Features aleatórias e MLP: h = 40, tanh, λ = 10⁻³, a mesma inicialização (semente 114); a MLP com 3.000 passos de GD de lote inteiro, lr 0,05.
- Graus de liberdade: features W ~ N(0, 1), b ~ U(−2, 2) por `random.Random(1144)`, h = 40, sobre o x do treino, f = sen(x₁) + 0,5x₂², σ = 0,1, 400 repetições, semente 3.

- **(a) P2861** max |w_rede − w_Newton|: **[0; 10⁻⁸]**. Identidade: convexidade forte + passo 1/L, com a cota de 5·10⁻¹² calculada acima (o Newton converge quadraticamente a ~10⁻¹⁵).
- **(b) P2862** max |β_rede − β_OLS|, com β_rede = W₂W₁: **[0; 10⁻¹⁰]**. Mecanismo esperado: a convergência global das redes lineares profundas a partir de uma inicialização pequena; na calibração, 9·10⁻¹⁶.
- **(c) P2863** MSE de teste das features aleatórias + ridge: **[0,0091; 0,020]**. O piso é o ruído (σ² = 0,01) menos 2 desvios da média de 1.000 ruídos ao quadrado (0,01·√(2/1000) = 0,00045).
- **(d) P2863** Razão MSE(retropropagação) / MSE(features aleatórias + ridge): calibração 1,20, faixa **[0,80; 1,60]**. Mecanismo esperado: a descida não resolveu a cabeça em 3.000 passos.
- **(e) P2863** Razão MSE(features TREINADAS + ridge) / MSE(retropropagação): calibração 0,88, faixa **[0,60; 0,99]**. A mesma rede, com a cabeça refeita em forma fechada, melhora. É uma identidade no TREINO (o ridge é o mínimo exato da cabeça), mas não no teste.
- **(f) P2864** tr(S) com λ = 10⁻³ nas 40 features: **[30; 41]**. Mecanismo esperado: 40 tanh de um x de 2 dimensões são quase colineares, e o posto efetivo fica abaixo dos 41 parâmetros.
- **(g) P2864** |df_Efron − tr(S)| com λ = 10⁻³: o desvio de Monte Carlo ≈ √(2·35/400) = 0,42, então 1,645 × 0,42 × 1,36 ≈ 0,94, faixa **[0; 1,0]**.
- **(h) P2864** |df_Efron − tr(S)| com λ = 1: **[0; 1,0]**.
- **(i) P2864** tr(S)(λ = 1) / tr(S)(λ = 10⁻³): calibração 0,505, faixa **[0,40; 0,65]**. Mecanismo esperado: a cumeeira encolhe as direções de autovalor pequeno, a maioria entre 40 features colineares.
- **(j) P2865** A rede linear profunda (d = 3, h = 4, n = 50 pontos de um LCG inteiro, 500 passos de GD) é **IGUAL** bit a bit entre Python e Java: **[0; 0]**. Identidade: só +, −, × e a mesma ordem de somas (laços sequenciais, sem o `sum()` compensado; regra da Parte 34).

### Previsões sobre as previsões (m), pré-registradas (régua: P2837, leitor v4)

- **(m1)** nº de previsões do mundo em **[9; 13]**
- **(m2)** nº de faixas que cruzam/tocam o zero em **[4; 7]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0,10; 0,50]**
- **(m4)** fração de acertos do mundo em **[0,60; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 3]**

### Sobre mim, pré-registrado

(a) e (j) são identidades com a garantia escrita. (b) tem um teorema de convergência (Arora et al.) e uma calibração. Os riscos estão em (d) e (e): uma calibração só, num efeito que depende de quanto a descida avançou. E em (i), que depende do espectro das features da semente 1144. Espero **1 a 2 erros**, em (d), (e) ou (i).

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->

## As respostas (quatro camadas)

### P2861 — A logística como rede de uma camada

**Na pergunta.** "Tratar o ML como DL" pressupõe que haja uma fronteira entre os dois. A pergunta a mede: se o modelo clássico, escrito como rede e treinado como rede, chega ao mesmo lugar, a fronteira é de VOCABULÁRIO, não de matemática.

**Lógica.** A logística com L2 é uma rede de uma camada: z = w·x, p = σ(z), perda = entropia cruzada + (λ/2)‖w‖². A retropropagação dá ∇ = Xᵀ(p − y)/n + λw, o mesmo gradiente que o ML clássico escreve à mão, e a regra da cadeia sobre a sigmoide e a entropia cruzada cancela o σ′ e sobra p − y. Treinada como DL (2.000 passos de descida com lr = 1/L, a partir de zero), ela chega a **4,4·10⁻¹⁶** do Newton ✅ (a), contra a cota de 5·10⁻¹² que o teorema dava ANTES de rodar. O Newton chega a |∇| = **3,3·10⁻¹⁸**. A conta da cota, com a substituição: μ = λ = 0,01, L = 0,3272, κ = 32,72, e (1 − 1/32,72)^1000 × 35,45 = **1,18·10⁻¹²** (por código; no rascunho eu tinha aproximado ln(1 − x) ≈ −x e escrito 1,9·10⁻¹², e o pré-registro, com uma conta mais folgada, 5·10⁻¹²). A descida foi mais rápida que a cota porque a cota usa a curvatura MÍNIMA (μ = λ), e a real é maior: no ótimo, a média de σ′ = p(1 − p) é **0,139** (medida; no rascunho eu tinha chutado "≈ 0,15"), o que acrescenta 0,139·λ_max(XᵀX/n) à curvatura, muito acima do λ = 0,01 da cota.

**Tradução cruzada.** A mesma montanha descida de dois jeitos: o Newton olha a curvatura e salta; a descida do gradiente dá passos pequenos e segue a inclinação. Os dois chegam ao mesmo vale porque a montanha só tem UM vale (convexidade forte). "ML" e "DL" são dois estilos de descer; a montanha é a mesma.

### P2862 — A rede linear profunda é o OLS

**Lógica.** W₂W₁ (h = 4, sem ativação) treinada por descida: o produto β fica a **1,1·10⁻¹⁵** do OLS ✅ (b). Uma rede "profunda" sem não-linearidade é um modelo linear com parâmetros REDUNDANTES (12 + 4 = 16 pesos para 3 coeficientes). A paisagem não é convexa, mas não tem mínimos locais ruins (Arora et al.: com inicialização pequena e quase balanceada, a descida converge linearmente ao ótimo global). A profundidade, sozinha, não compra nada; o que compra é a não-linearidade.

**Meta.** No diálogo (rodada 81, 500 passos, outros dados), a rede ainda NÃO tinha chegado ao OLS: 0,6685 contra 0,7005 no 1º coeficiente. O que a rodada mede é a igualdade entre as línguas, não a convergência. A sobreparametrização não atrapalha o destino, mas atrasa a chegada: a inicialização pequena começa num ponto de sela (W = 0), e sair dele leva passos.

### P2863 — A camada oculta como features

**Lógica.** Três modelos, a mesma arquitetura (40 tanh + cabeça linear), a mesma inicialização, MSE de teste (ruído σ² = 0,01):
- **Features ALEATÓRIAS + ridge** (DL lido como ML: a camada congelada, a cabeça em forma fechada): **0,01270** ✅ (c), só 27% acima do piso do ruído.
- **A rede INTEIRA por retropropagação** (3.000 passos): **0,01535**, **1,21×** pior ✅ (d).
- **As features que a retropropagação aprendeu, com a cabeça refeita por ridge:** **0,01270**, **0,83×** a retropropagação ✅ (e).

Duas leituras, as duas registradas antes:
- A rede treinada PERDE para a rede não treinada com a cabeça exata. A descida não resolveu nem o problema convexo da cabeça (mal condicionado: 40 tanh quase colineares, tr(S) ≈ 30 de 41) em 3.000 passos, e a forma fechada o resolve num passo.
- As features aprendidas, com a cabeça exata, empatam com as aleatórias (0,012702 contra 0,012700). Nesta tarefa, 3.000 passos de retropropagação não ensinaram à camada oculta nada que 40 direções aleatórias já não tivessem. O ganho de "aprender as features" (o DL de verdade) não apareceu aqui: a tarefa (sen x₁ + 0,5x₂²) é suave demais, e 40 features aleatórias já a cobrem.

**Tradução cruzada.** É a tese de Rahimi e Recht (2007), em miniatura: features aleatórias + um solucionador linear exato competem com redes treinadas. Na linguagem da Parte 96, a BASE (a camada oculta) importa menos que a cabeça bem resolvida quando a base aleatória já é rica o bastante. O DL ganha quando a base certa é rara, e não ganha quando ela é abundante.

### P2864 — Os graus de liberdade da cabeça de uma rede

**Lógica.** Os graus de liberdade (a "complexidade efetiva" do ML clássico), aplicados à cabeça ridge sobre 40 features tanh:
- **λ = 10⁻³:** tr(S) = **30,10** ✅ (f), no limite de [30; 41]; a definição de Efron (Σ cov(ŷᵢ, yᵢ)/σ², 400 simulações) dá **29,75**, |dif| = **0,35** ✅ (g).
- **λ = 1:** tr(S) = **14,77**; Efron **14,74**, |dif| = **0,03** ✅ (h).
- **A razão** é **0,491** ✅ (i).

A rede tem 41 parâmetros na cabeça e usa 30: as features tanh de um x de 2 dimensões são quase colineares, e 11 direções não têm sinal. Com λ = 1, sobram 15. "Quantos parâmetros a rede tem" e "quantos ela USA" são números diferentes, e o segundo é o que decide o sobreajuste (a Parte 97 organizou o viés e a variância por #params/n; este é o #params certo).

**Tradução cruzada.** É o grau de liberdade como ATENÇÃO: um sistema com 41 botões, dos quais só 30 respondem ao mundo. A covariância de Efron mede quanto a saída SEGUE o dado (quanto a resposta muda quando o ruído muda), a definição operacional de "quanto o modelo escuta". Um modelo de df alto escuta tudo, inclusive o ruído; um de df baixo escuta pouco, e erra pela surdez.

### P2865 — rodada 81

**Lógica.** A rede linear profunda (500 passos de GD), Python × Java: **IGUAIS, 2 linhas e 3 números bit a bit** ✅ (j). 25 rodadas: o treino de uma rede "profunda" é aritmética portável, como tudo antes.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅. Parte 114: **10 testes, 0 erros**. Os mecanismos escritos dentro das faixas, conferidos:
- (a): a cota foi folgada, porque a curvatura real é maior que a do pior caso;
- (d): a descida não resolveu a cabeça, confirmado por (e);
- (f): o posto efetivo, confirmado (30 de 41), mas no limite da faixa: 30,10 contra o piso 30.

Acumulado (mundo): **224 erros em 887 testes**. Calibração (P1961, Partes 80–114): **207/228 = 0,908**.

### Previsões sobre previsões (m)

Régua: P2837 (leitor v4).

| | faixa | medido | |
|---|---|---|---|
| (m1) | [9; 13] | 10 | ✅ |
| (m2) | [4; 7] | 5 | ✅ |
| (m3) | [0,10; 0,50] | 0,25 | ✅ |
| (m4) | [0,60; 1,00] | 1,00 | ✅ |
| (m5) | [0; 2] | 0 | ✅ |
| (m6) | [0; 3] | 0 | ✅ |

Previsões sobre previsões: **6 de 6**.

## Engenharia reversa (metacognição)

**O padrão: as estimativas de cabeça no texto, de novo.** As 10 previsões acertaram, e os dois erros desta parte estavam na PROSA, depois da medida, e foram pegos pela regra da Parte 69 antes do commit:
- a cota escrita com ln(1 − x) ≈ −x (1,9·10⁻¹² em vez de 1,18·10⁻¹²);
- o "σ′ ≈ 0,15" chutado (é 0,139).

Na Parte 113 foi o sinal do rei. **Significado:** quando a previsão está garantida (o registro, as faixas, o placar), o meu cuidado relaxa no texto que EXPLICA o resultado, e é ali que eu volto a fazer contas de cabeça. A explicação parece menos "medida" que a previsão, e por isso eu a trato com menos rigor. Mas um número na explicação é um número no texto, e a regra vale igual. **Regra (afiando a da Parte 69):** depois de escrever as respostas, todo número que não saiu de uma saída impressa NESTA sessão passa por uma linha de código, INCLUSIVE os da explicação do mecanismo, onde eu mais erro.

**O segundo padrão: a fronteira ML/DL é de vocabulário.** As cinco travessias acharam a MESMA matemática dos dois lados:
- a logística é uma rede (e chega ao mesmo ponto);
- a rede linear profunda é o OLS;
- a camada oculta é uma base de features (e, com a cabeça exata, a base aleatória empata com a treinada);
- os graus de liberdade são a complexidade da rede.

O que separa o "ML" do "DL" não é a matemática, é o REGIME:
- no ML, o solucionador é exato e a base é dada;
- no DL, a base é aprendida e o solucionador é aproximado (a descida).

Esta parte mostrou o preço de cada lado: a descida aproximada perdeu 21% para a forma fechada numa cabeça convexa (o custo do solucionador do DL), e aprender a base não ganhou nada numa tarefa suave (o benefício do DL só aparece quando a base certa é rara). **Regra:** antes de treinar uma rede inteira por retropropagação, resolver em forma fechada tudo o que for convexo (a cabeça), e só pagar a descida no que não tem forma fechada (a base). É a autopoiese da Parte 31 ("substituir aprendizado por conta exata se der") com endereço: dá na cabeça, não dá na base.

## Síntese / unificação

A Parte 114 trata o ML como DL e o DL como ML (`synthai/ml_dl.py`):
- **ML → DL:** a logística como rede de uma camada, treinada por retropropagação, chega a 4,4·10⁻¹⁶ do Newton (a cota do teorema era 1,2·10⁻¹²).
- **DL → ML:** a rede linear profunda W₂W₁ é o OLS (1,1·10⁻¹⁵). A camada oculta tanh lida como features, com a cabeça ridge em forma fechada, bate a rede inteira treinada por 3.000 passos (MSE 0,0127 contra 0,0154), e as features que a rede aprendeu, com a cabeça exata, empatam com as aleatórias. Os graus de liberdade de Efron (Σ cov/σ²) batem com tr(S) a 0,35 e a 0,03, e mostram que a cabeça de 41 parâmetros usa 30 (com λ = 10⁻³) ou 15 (com λ = 1).

A fronteira é de regime, não de matemática: solucionador exato com base dada (ML) contra base aprendida com solucionador aproximado (DL). E a regra prática fica medida: forma fechada em tudo que é convexo, descida só no resto. Rodada 81: a rede linear profunda IGUAL bit a bit (25 rodadas). 10/10 do mundo, 6/6 (m), calibração **0,908**.

## Meta

Confiança alta em (a), (b), (g), (h) (identidades e teoremas, conferidos por cotas calculadas antes) e em (c) a (e) (uma tarefa, uma semente de teste, a direção prevista na calibração). Onde é brinquedo: 40 neurônios, uma tarefa suave de 2 dimensões, descida de lote inteiro sem Adam. Em tarefas onde a base certa é rara (imagens, linguagem), aprender a base é o que faz o DL ganhar, e esta parte NÃO mediu esse regime; a conclusão "aprender a base não ganhou" vale para esta tarefa (um lote), escrita como hipótese pela regra da Parte 66. Os 3.000 passos da retropropagação são um orçamento fixo: com mais passos, ou com Adam (Parte 92), a cabeça da rede se aproximaria da forma fechada.

## Diálogo Python ↔ Java (rodada 81)

Ver `dialogo/DIALOGO.md`: a rede linear profunda, 500 passos de GD, é **IGUAL**: 2 linhas e 3 números bit a bit.

## Fontes

- Convergência da descida em redes lineares profundas: [Arora, Cohen, Golowich e Hu, "A Convergence Analysis of Gradient Descent for Deep Linear Neural Networks", ICLR 2019 (arXiv 1810.02281)](https://arxiv.org/pdf/1810.02281); [ICLR 2019](https://iclr.cc/virtual/2019/poster/789).
- Features aleatórias + solucionador linear: [Rahimi e Recht, "Random Features for Large-Scale Kernel Machines", NIPS 2007](https://papers.neurips.cc/paper/3182-random-features-for-large-scale-kernel-machines); [PDF](https://people.eecs.berkeley.edu/~brecht/papers/07.rah.rec.nips.pdf).
- Graus de liberdade como penalidade de covariância: [Efron, "The Estimation of Prediction Error: Covariance Penalties and Cross-Validation", JASA 99 (2004)](https://ideas.repec.org/a/bes/jnlasa/v99y2004p619-632.html); [PDF (Wisconsin)](https://pages.stat.wisc.edu/~wahba/stat860public/pdf1/efron.covariance.04.pdf).
