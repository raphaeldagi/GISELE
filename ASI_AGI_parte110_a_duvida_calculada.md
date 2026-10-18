# Parte 110 — A dúvida calculada: gradiente, inferência, RNN, ML, aprendizado contínuo e por reforço (0x6E)

↩ Parte 109 (o NEXUS anexado) · ↩ Parte 31 (substituir ML/DL por inferência exata "se der") · ↩ Parte 34 (Bayes exato só é exato para o seu modelo) · ↩ Parte 32 (unidades que falham juntas) · ↩ Parte 46 (versa/reversa) · ↩ Parte 83 (cada termo do pedido vira uma conta escrita ANTES de medir)

> Pedido do usuário: "Duvide dos gradientes, das inferências, das RNN e de toda a estrutura de uma IA, como também o ML, DL, APRENDIZADO CONTÍNUO E POR REFORÇO. Tudo em metacognição. E depois de duvidar acione a curiosidade e comece a calcular suas dúvidas de forma independente." E depois: "E depois de calculados use processo metacognitivo inverso e subverso."
>
> **A leitura escolhida (regra da Parte 83, escrita ANTES de medir).** Três operações sobre cada uma das seis peças.
> - **Duvidar** é escrever a afirmação que a peça faz sobre si e a conta fechada que diria se ela é verdadeira.
> - **Calcular de forma independente** é medir essa afirmação por um caminho que não é o da peça: a diferença finita contra o gradiente analítico, a cobertura empírica contra o intervalo declarado, a forma fechada contra a simulação. Tudo em `synthai/duvida.py`, biblioteca padrão.
> - **Processo INVERSO** é ir do número medido de volta à premissa. De cada resultado eu resolvo para o parâmetro que o gerou (a ordem do método, o tamanho do aglomerado, o peso da RNN, o número de parâmetros, o ângulo entre as tarefas, o tamanho da amostra). Se a inversão devolve o parâmetro usado, a conta é coerente consigo mesma; se não, alguma premissa está errada. É a versa/reversa da Parte 46 em forma de equação: a resposta tem de conter a pergunta.
> - **Processo SUBVERSO** é derrubar UMA premissa da conta, por baixo, e prever ANTES como o resultado quebra. Se a quebra prevista acontece, eu entendo a premissa; se não acontece, eu não entendia.
>
> Uma conta que eu pensei registrar foi descartada ANTES do registro, por um caso calculado à mão (regra da Parte 47). Eu ia prever uma "conservação da interferência" no aprendizado contínuo (esquecimento + perda que resta = cos²θ). Em 2-D, a projeção ortogonal resolve as duas tarefas ao mesmo tempo (w = (1, 1/sen θ)), então a conservação é falsa. O preço verdadeiro da projeção é a NORMA, e é isso que vai para a previsão (p).

## As perguntas desta parte

1. **P2741 (0xAB5).** O gradiente analítico de uma rede (MLP tanh) está certo? Qual a ordem do erro da diferença finita, e onde fica o piso do arredondamento? ↩ P2321
2. **P2742 (0xAB6).** A inferência bayesiana exata é calibrada, isto é, o intervalo de 90% contém o valor verdadeiro 90% das vezes? E quando as observações não são independentes? ↩ P1813
3. **P2743 (0xAB7).** O gradiente através do tempo numa RNN some ou explode como w^T? E numa tanh com w > 1? ↩ P2741
4. **P2744 (0xAB8).** O erro de generalização de um modelo linear aprendido é o que a conta fechada diz, σ²(1 + p/(n − p − 1))? E com uma variável omitida? ↩ P2357
5. **P2745 (0xAB9).** O esquecimento no aprendizado contínuo é cos²θ do ângulo entre as tarefas? E a projeção ortogonal (OGD) esquece zero de graça? ↩ P2296
6. **P2746 (0xABA).** O aprendizado por reforço sobrestima o valor (o viés de maximização do max)? De quanto, e o estimador duplo corrige? ↩ P2651
7. **P2747 (0xABB).** O passo de aprendizado contínuo (GD em 2-D) acrescenta fronteira entre Python e Java? (rodada 77) ↩ P2716

## Previsões pré-registradas (ANTES de medir — este commit)

**Gradientes (P2741).** MLP 3→4→1 com tanh, pesos com semente fixa e perda ½(f − y)². Erro relativo máximo entre o gradiente analítico e a diferença finita, em função do passo h.
- **(a) Duvidar.** Diferença CENTRAL: o erro de truncamento é h²·f‴/6, então a inclinação de log(erro) contra log(h) entre h = 10⁻² e 10⁻³ fica em **[1,8; 2,2]**.
- **(b) Subverso.** Troco a central pela diferença ADIANTADA. O erro passa a ser h·f″/2, e a inclinação cai para **[0,9; 1,1]**. O inverso é ler a ordem do método na inclinação.
- **(c) O piso.** O melhor erro relativo, na grade h = 10⁻¹ … 10⁻¹⁰, onde o truncamento (h²) encontra o arredondamento (ε/h, ε = 2,2·10⁻¹⁶). O ótimo fica em h ~ ε^(1/3) ≈ 6·10⁻⁶, e o erro ali em **[10⁻¹²; 10⁻⁸]**.
- **(d) Subverso, controle plantado.** Troco o sinal de UMA componente do gradiente analítico. O verificador TEM de acusar, e o erro relativo daquela componente fica em **[1,9; 2,1]** (|−g − g|/|g| = 2).

**Inferência (P2742).** p ~ U(0, 1), n = 50 Bernoulli, posterior Beta(1 + k, 1 + n − k) e intervalo central de 90% (quantis por bissecção da CDF binomial exata). São 2.000 mundos.
- **(e) Duvidar.** Bem especificado, Bayes é calibrado por construção (a cobertura média sob o prior é exatamente 0,90). Binomial: desvio √(0,09/2000) = 0,0067, e a faixa (forma fechada, sem o fator 1,36) é **[0,887; 0,913]**.
- **(f) Subverso.** Agora as observações vêm em 25 AGLOMERADOS de 4 idênticas (n = 100 aparentes, 25 reais), e o modelo as trata como independentes. O desvio posterior fica pequeno demais por √4 = 2, e a cobertura cai para P(|Z| < 1,645/2) = 2Φ(0,8225) − 1 ≈ 0,589. Faixa **[0,53; 0,65]** (a lição da Parte 32: unidades que falham juntas).
- **(g) Inverso.** Da cobertura medida, recupero o tamanho do aglomerado, c = (1,645/Φ⁻¹((1 + cob)/2))². Faixa **[3; 5]** (o usado é 4).

**RNN (P2743).**
- **(h) Duvidar + inverso.** RNN linear escalar h_t = w·h_{t−1}. O gradiente por retropropagação no tempo (BPTT), ∂h_T/∂h_0, contra a forma fechada w^T, para w = 0,9 e T = 50 (0,9⁵⁰ = 0,00515). Erro relativo **[0; 10⁻¹²]**. O inverso recupera w de log(grad)/T.
- **(i) Subverso.** RNN tanh com w = 1,1 > 1, h_0 = 0,5, T = 50. A conta ingênua (w^T) diz que o gradiente EXPLODE (1,1⁵⁰ = 117). A saturação diz o contrário: perto do ponto fixo h* = tanh(1,1·h*) ≈ 0,50, a derivada local é 1,1·(1 − h*²) ≈ 0,82 < 1, então o gradiente SOME, ≈ 0,82⁵⁰ ≈ 6·10⁻⁵. Faixa **[10⁻⁵; 5·10⁻⁴]**.

**ML (P2744).** Mínimos quadrados, x ~ N(0, I_p), σ = 1, n = 50 e 2.000 repetições. O erro de teste esperado é ‖β̂ − β‖² + σ² (exato sob Σ = I, sem amostra de teste).
- **(j) Duvidar.** Com p = 10: 1 + 10/39 = 1,2564, faixa **[1,23; 1,28]**.
- **(k) Inverso.** Do excesso medido e = erro − 1, recupero p = e(n − 1)/(1 + e). Faixa **[8,5; 11,5]**.
- **(l) Subverso.** O y verdadeiro tem uma variável z ~ N(0, 1), de coeficiente 1, fora do modelo. Ela vira ruído de variância 2, e o erro fica 2·1,2564 = 2,513. Faixa **[2,44; 2,58]**.

**Aprendizado contínuo (P2745).** Pesos w ∈ ℝ². A tarefa A fixa a direção e₁ (perda (w₁ − 1)²); a tarefa B fixa a direção u = (cos θ, sen θ), com resíduo inicial 1. GD com passo 0,1 por 2.000 passos em cada uma.
- **(n) Duvidar.** O esquecimento de A depois de B é cos²θ. Em θ = 45°: **[0,499; 0,501]**. O inverso recupera θ = arccos √(esquecimento).
- **(o) OGD.** Projetar o gradiente de B ortogonal a e₁ esquece **[0; 0]** exatamente (a componente e₁ do passo é u₁ − u₁·1 = 0 em ponto flutuante).
- **(p) O preço do OGD.** B fica resolvida andando só por e₂, até t = 1/sen θ: a norma do passo é √2 ≈ 1,414 em 45°, contra 1 do GD. Faixa **[1,41; 1,42]**.
- **(q) Subverso.** Em θ = 0 (conflito total), o gradiente projetado é nulo e o OGD NÃO aprende B. A perda de B fica **[1; 1]**.

**Reforço (P2746).** k ações de valor verdadeiro 0; cada estimativa é a média de m = 10 recompensas N(0, 1), isto é, N(0, 1/m). São 20.000 ensaios.
- **(r) Duvidar.** Com k = 2, o viés do max (o que o Q-learning faz no alvo) é E[max] = σₑ/√π = 0,3162/1,7725 = 0,1784. O desvio de um ensaio é σₑ√(1 − 1/π) = 0,261, e o erro padrão 0,0018. Faixa **[0,175; 0,182]**.
- **(s) A correção.** Estimador DUPLO (escolhe por um conjunto, avalia pelo outro, independente): sem viés, faixa **[−0,004; 0,004]**.
- **(t) Inverso.** Do viés medido, recupero m = 1/(π·viés²). Faixa **[9; 11]**.
- **(u) Subverso.** Com k = 10 ações, E[max de 10 normais] = 1,5388, e o viés é 1,5388/√10 = 0,4866. Desvio por ensaio ≈ 0,186, erro padrão 0,0013. Faixa **[0,483; 0,490]**.

**Diálogo (P2747).**
- **(v)** O GD/OGD em 2-D (só +, −, ×, ÷ e √, que é IEEE) é **IGUAL** bit a bit entre Python e Java. Divergências **[0; 0]**.

(A letra (m) fica reservada para as previsões sobre previsões.)

### Previsões sobre as previsões (m), pré-registradas

- **(m1)** nº de previsões do mundo em **[19; 23]**. São 21 agora, e somo ~2 por surpresa esperada (regra da Parte 60, que eu esqueci na 109).
- **(m2)** nº de faixas que cruzam/tocam o zero em **[3; 6]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0; 0,60]**
- **(m4)** fração de acertos do mundo em **[0,60; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 4]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 4]**

### Sobre mim, pré-registrado

Quinze das 21 faixas saem de forma fechada com variância conhecida. As arriscadas:
- (c), o piso do arredondamento, que depende da escala da perda;
- (f), a aproximação normal com n pequeno e p perto das pontas;
- (i), o transiente antes do ponto fixo;
- (j)/(l), a cauda pesada do ‖β̂ − β‖² com n − p − 1 = 39.

Espero **2 a 4 erros**, entre essas cinco. Antes de prever o contador de passos, fiz o que a 109 pediu: não há contador aqui, e as contagens são de ensaios fixos.

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->

## As respostas (quatro camadas)

### P2741 — O gradiente

**Na pergunta.** "Duvidar do gradiente" pede uma segunda testemunha que não dependa da primeira. A retropropagação é a regra da cadeia aplicada à mão; a diferença finita só precisa saber AVALIAR a perda. Se as duas concordam, a dúvida se dissolve pela medida, não pela confiança.

**Lógica (duvidar).** A MLP 3→4→1 tanh tem 21 parâmetros. O erro relativo máximo, por passo h, é **3,5·10⁻³** em 10⁻¹, **3,6·10⁻⁵** em 10⁻², **3,6·10⁻⁷** em 10⁻³ e **3,6·10⁻⁹** em 10⁻⁴. Depois sobe: **6,8·10⁻⁹** em 10⁻⁵ … **5,4·10⁻⁴** em 10⁻¹⁰. A inclinação entre 10⁻² e 10⁻³ é **2,0000** ✅ (a), contra a conta h²·f‴/6. O piso é **3,6·10⁻⁹** ✅ (c), na faixa [10⁻¹²; 10⁻⁸], mas em h = 10⁻⁴ e não em h ≈ 6·10⁻⁶. O mecanismo do ótimo eu previ errado: o erro relativo MÁXIMO é dominado pela MENOR componente do gradiente, e ali o arredondamento ε·|L|/h pesa mais. O ótimo em ε^(1/3) vale para uma componente de escala 1, não para a pior de 21.

**Inverso.** A inclinação lê a premissa que eu não disse ao verificador, a ordem do método: central **2,0000**, adiantada **0,9997** ✅ (b). O verificador reconstrói, só pela forma da curva, qual fórmula de diferença foi usada.

**Subverso.** Troquei o sinal de uma componente (o defeito clássico da retropropagação à mão): erro relativo **2,0000** ✅ (d), acusado. E o caso limpo passa (teste `test_gradiente_caso_limpo`). Com os dois lados, o verificador é um verificador (regra da Parte 75).

**Tradução cruzada.** Duas testemunhas independentes que concordam valem mais que uma testemunha mais confiante: é o princípio do juiz que não aceita a confissão sem a prova material. O gradiente analítico é a confissão (a rede "diz" para onde descer); a diferença finita é a prova material.

### P2742 — A inferência

**Lógica (duvidar).** Bem especificada, a inferência bayesiana exata é calibrada: cobertura de **0,8995** ✅ (e) em 2.000 mundos. Não é fé no teorema, é a medida que bate com ele (0,90 ± 0,007).

**Subverso.** As MESMAS 100 observações, mas em 25 aglomerados de 4 idênticas: cobertura **0,591** ✅ (f), contra a previsão 2Φ(0,8225) − 1 = 0,589. O intervalo de "90%" acerta 59% das vezes. O cálculo está perfeito; a premissa (independência) é que é falsa. Bayes exato é exato para o SEU modelo (Parte 34), e o modelo errado dá uma confiança errada com toda a exatidão.

**Inverso.** Da cobertura medida, sem saber o desenho, recupero c = **3,97** ✅ (g), e o usado era 4. A calibração ruim não é só um defeito, é uma MEDIDA da premissa violada. É exatamente o que a Parte 79 fez comigo: o meu fator 1,36 é o "c" das minhas previsões, √c = 1,36 ⇒ c ≈ 1,85. As minhas previsões se comportavam como se cada uma valesse ~1,85 previsões correlacionadas.

**Tradução cruzada.** Quatro testemunhas que repetem o mesmo boato não são quatro testemunhas. A psicologia chama isso de cascata de informação; a estatística, de tamanho efetivo de amostra.

### P2743 — A RNN

**Lógica (duvidar + inverso).** BPTT na RNN linear, w = 0,9, T = 50: **0,0051538**, igual a 0,9⁵⁰ com erro relativo **0** ✅ (h). O inverso, grad^(1/T), devolve **w = 0,9** exato. O gradiente através do tempo é, de fato, o produto das derivadas locais: some como w^T se |w| < 1 e explode se |w| > 1.

**Subverso.** Na RNN tanh com w = 1,1, a conta ingênua (w^T) previa explosão, 1,1⁵⁰ = 117. O medido é **5,56·10⁻⁵** ✅ (i): o gradiente SOME. A saturação leva h ao ponto fixo h* = **0,5029** (tanh(1,1·0,5029) = 0,5029), onde a derivada local é 1,1·(1 − 0,5029²) = **0,822** < 1. Um w grande não basta para explodir; o que conta é w·tanh′ no ATRATOR. Esta é a raiz do problema que motivou a LSTM e o caminho residual: não é o peso, é o produto de derivadas ao longo do caminho.

**Tradução cruzada.** É a dinâmica do hábito: uma tendência forte (w > 1) que satura se estabiliza num ponto fixo, e ali a sensibilidade às origens se apaga. Quanto mais estável o atrator, menos o presente lembra o começo.

### P2744 — O ML

**Lógica (duvidar).** Mínimos quadrados, n = 50, p = 10: erro de teste **1,2530** ✅ (j), contra a forma fechada 1 + 10/39 = 1,2564. Aprender 10 parâmetros com 50 exemplos custa 25% de erro acima do ruído, um preço exato e calculável antes de treinar.

**Inverso.** Do excesso medido, p = e(n − 1)/(1 + e) = **9,89** ✅ (k): o erro de teste "sabe" quantos parâmetros o modelo tinha. É o raciocínio do AIC/Cp ao contrário.

**Subverso.** Uma variável omitida de coeficiente 1: **2,5158** ✅ (l), contra 2 × 1,2564 = 2,513. Ela não aparece como viés: aparece como RUÍDO extra, e o mesmo fator (1 + p/(n − p − 1)) a multiplica. Mais dados não a curam (o piso de FORMA da Parte 99).

### P2745 — O aprendizado contínuo

**Lógica (duvidar).** Com o GD, o esquecimento de A depois de B em 45° é **0,500000** ✅ (n) = cos²45°, e em 60° é exatamente `0x1p-2` = 0,25 = cos²60°, bit a bit. O esquecimento catastrófico não é um mistério: é a projeção do passo de B sobre a direção de A.

**Inverso.** θ = arccos √0,5 = **45,000000°** ✅. O esquecimento medido revela o ÂNGULO entre as tarefas.

**OGD.** A projeção ortogonal não move w₁ (o passo ao longo de e₁ é 0 em ponto flutuante). Mas o "esquecimento" medido foi **4,9·10⁻³²** e não 0: **(o) ❌**. O que eu medi foi a PERDA de A, (w₁ − 1)², e a própria tarefa A parou a 1 ulp de 1 ((2,2·10⁻¹⁶)²). Previ "não esquece = perda zero" e confundi a variação com o nível; era uma faixa fina sem conta, de novo a regra da Parte 97. A norma do passo OGD é **1,414214** ✅ (p) = √2 = 1/sen 45°. Não esquecer custa um passo maior.

**Subverso.** Em θ = 0 (as duas tarefas querem a MESMA coordenada com alvos diferentes), o OGD não aprende B: a perda fica **1,0** ✅ (q). Nenhum truque de projeção resolve um conflito verdadeiro; ele só escolhe QUEM perde. Contra a dúvida da Parte 31 ("trocar aprendizado contínuo por algo melhor se der"): a conta diz quando dá (θ > 0: há uma direção livre) e quando não dá (θ = 0: só resta escolher).

### P2746 — O reforço

**Lógica (duvidar).** O alvo do Q-learning usa o max das estimativas, e o max de estimativas ruidosas é otimista. Com k = 2 ações de valor 0 e m = 10 amostras: viés **0,1794** ✅ (r), contra 1/√(10π) = 0,1784. O estimador duplo (Double Q) dá **0,0002** ✅ (s): escolher por um conjunto e avaliar pelo outro quebra a correlação entre o erro e a escolha.

**Inverso.** m = 1/(π·viés²) = **9,89** ✅ (t). O otimismo de um agente revela quantas experiências ele teve.

**Subverso.** Com k = 10 ações, **0,4840** ✅ (u), contra a previsão 1,5388/√10 = 0,4866, a z ≈ −2 do centro (no limite da faixa, dentro). Mais opções, mais otimismo: o viés cresce como √(2 ln k)/√m. É a maldição do vencedor da Parte 33 (escolher pela nota guardada piorou o agente) em forma fechada.

**Tradução cruzada.** É a psicologia do "a grama do vizinho": quem escolhe entre muitas opções pela melhor ESTIMATIVA fica, em média, decepcionado com a escolha, porque escolheu justamente onde o ruído estava a favor. A correção (avaliar em amostra independente) é o que a ciência chama de replicação.

### P2747 — rodada 77

**Lógica.** GD/OGD em ℝ², Python × Java: **IGUAIS, 7 linhas e 18 números bit a bit** ✅ (v), com u de √ e não de sin/cos (a fronteira medida da Parte 105). 21 rodadas.

## O processo metacognitivo INVERSO e SUBVERSO, aplicado às minhas próprias contas

**Inverso sobre mim.** Do placar desta parte, de volta à premissa com que eu escrevi as faixas. 20 de 21 acertaram, e o único erro foi uma faixa de largura ZERO ([0; 0]) que eu escrevi sem conta. As que acertaram tinham todas uma variância conhecida (binomial, forma fechada) ou uma identidade. Invertendo: a premissa que eu uso sem dizer é "quando a conta existe, a faixa é a da conta; quando não existe, eu escrevo zero e chamo de exato". Desta vez a premissa errada estava num [0; 0], como na Parte 97 estava num "< 10⁻⁶". O padrão se repetiu: **os meus erros moram nas faixas que não têm largura**.

**Subverso sobre mim.** A premissa que mais sustenta este placar é que as faixas vêm de contas fechadas, e derrubá-la mostra o quanto ele depende disso. Das 21 previsões, 3 vieram de mecanismos que eu nunca tinha rodado: o piso do gradiente, a cobertura aglomerada e a saturação da tanh. As três acertaram, mas uma, (c), pelo mecanismo errado (o ótimo foi h = 10⁻⁴, não 6·10⁻⁶). Se a faixa de (c) fosse estreita em torno do MEU h ótimo, eu teria errado. A largura de (c) (quatro ordens de grandeza) comprou o acerto e escondeu o erro de mecanismo. A dúvida de tudo inclui a dúvida do meu acerto: um acerto numa faixa larga não confirma o mecanismo.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ✅ (l) ✅ (n) ✅ (o) ❌ (p) ✅ (q) ✅ (r) ✅ (s) ✅ (t) ✅ (u) ✅ (v) ✅. Parte 110: **21 testes, 1 erro** ((o): uma faixa [0; 0] sem conta). Erro de mecanismo dentro de faixa certa: (c), o h ótimo. Acumulado (mundo): **221 erros em 835 testes**. Calibração (P1961, Partes 80–110): **158/176 = 0,898**.

### Previsões sobre previsões (m)

| | faixa | medido | |
|---|---|---|---|
| (m1) | [19; 23] | 21 | ✅ |
| (m2) | [3; 6] | 3 | ✅ |
| (m3) | [0; 0,60] | 0,03 | ✅ |
| (m4) | [0,60; 1,00] | 0,95 | ✅ |
| (m5) | [0; 4] | 0 | ✅ |
| (m6) | [0; 4] | 1 | ✅ |

Previsões sobre previsões (p1499): **6 de 6**. Um defeito de MEDIDA meu, achado nesta parte: o leitor `p1481` perde a faixa das letras cujo item começa com um rótulo em negrito ("**(a) Duvidar.**") e atribui à (h) a faixa da (a). O placar do mundo usa `VEREDITOS` e não é afetado. As (m2)/(m3) leem 18 das 21 faixas; vai como pendência de correção (uma `p1481_v3`), sem editar a antiga.

## Engenharia reversa (metacognição)

**O padrão:** cada uma das seis peças falhou exatamente onde uma premissa não-dita deixou de valer, e funcionou perfeitamente onde ela valia:
- Bayes com os aglomerados;
- a RNN com a saturação;
- o OLS com a omitida;
- o OGD com o conflito total;
- o Q-learning com o max.

Nenhuma falhou "um pouco": falharam em forma fechada, com o tamanho previsto. **Significado:** duvidar de uma peça de IA não é duvidar da conta dela, que nas seis estava certa. É duvidar da PREMISSA que a conta herda em silêncio. A dúvida produtiva tem endereço, e o processo subverso é o método para achá-lo (derrubar uma premissa por vez e ver se a quebra tem o tamanho que a conta diz). **O processo inverso** mostrou o outro lado: cada falha medida devolve o parâmetro da premissa violada (c = 3,97, p = 9,89, m = 9,89, θ = 45°). Um sistema que sabe inverter os próprios erros sabe O QUE está errado, não só QUE está.

**Sobre mim:** o meu único erro foi, de novo, uma faixa de largura zero escrita sem conta (a 97 e a 110). E o erro de mecanismo escondido por uma faixa larga, (c), é o espelho dele: a faixa estreita sem conta erra, e a faixa larga sem mecanismo acerta sem informar. **Regra nova:** uma faixa [x; x] só com a identidade que a garante escrita ao lado (aqui: "w₁ não muda" não garantia "perda zero"); e uma faixa de mais de duas ordens de grandeza vem acompanhada do mecanismo que eu ESPERO dentro dela, para que o acerto possa refutar o mecanismo.

## Síntese / unificação

A Parte 110 duvida das seis peças da estrutura de uma IA e calcula cada dúvida por um caminho independente (`synthai/duvida.py`), com o processo inverso (do número à premissa) e o subverso (uma premissa derrubada, com a quebra prevista antes):

| Peça | Duvidar (conferido) | Inverso (recupera) | Subverso (quebra prevista e medida) |
|---|---|---|---|
| Gradiente | inclinação 2,0000; piso 3,6·10⁻⁹ | a ordem do método (2 e 1) | sinal plantado: erro 2,0000 |
| Inferência | cobertura 0,8995 | c = 3,97 (usado 4) | aglomerados: 0,591 (previsto 0,589) |
| RNN | BPTT = w^T exato | w = 0,9 exato | tanh, w = 1,1: SOME (5,6·10⁻⁵), não explode |
| ML | 1,2530 (1,2564) | p = 9,89 (usado 10) | omitida: 2,516 (2,513) |
| Contínuo | esquecimento cos²θ = 0,5 | θ = 45,000° | θ = 0: o OGD não aprende (1,0) |
| Reforço | viés 0,1794 (0,1784); duplo ~0 | m = 9,89 (usado 10) | k = 10: 0,4840 (0,4866) |

Rodada 77: o aprendizado contínuo atravessa as línguas bit a bit (21 rodadas). 20/21 do mundo, 6/6 (m), calibração 0,898. O que esta parte acrescenta à SYNTHAI é um **verificador de premissas**: cada peça, além do resultado, devolve o parâmetro que a explicaria. A substituição de ML por inferência exata "se der" (Parte 31) ganha o seu critério: dá quando a premissa da conta exata vale, e a inversão diz quando não vale.

## Meta

Confiança alta nas 15 faixas de forma fechada; as três de mecanismo nunca rodado ((c), (f), (i)) acertaram, uma com o mecanismo errado. Onde é brinquedo: MLP de 21 parâmetros, RNN escalar, tarefas de posto 1 em ℝ², ações sem estado. As formas fechadas são exatas nesses casos e servem de ÂNCORA (regra da Parte 89) para as versões grandes, onde não há forma fechada. A dúvida não termina aqui: o leitor `p1481` tem um defeito medido, e o simplex n×m e o Kuhn completo seguem pendentes (Parte 111).

## Diálogo Python ↔ Java (rodada 77)

Ver `dialogo/DIALOGO.md`: GD e OGD em ℝ², com u por √ e não por sin/cos. **IGUAL**, 7 linhas e 18 números bit a bit; o esquecimento em 60° é `0x1p-2` exato nas duas línguas.

## Fontes

- Gradiente que some/explode em RNNs, análise dinâmica: [Pascanu, Mikolov e Bengio, ICML 2013 (PMLR 28)](https://proceedings.mlr.press/v28/pascanu13.html); [arXiv 1211.5063](https://arxiv.org/abs/1211.5063).
- Viés de maximização e estimador duplo: [van Hasselt, Double Q-learning, NIPS 2010](https://papers.nips.cc/paper/3964-double-q-learning); [NeurIPS 2010, pôster](https://neurips.cc/virtual/2010/poster/2040).
- Projeção ortogonal no aprendizado contínuo: [Farajtabar et al., OGD, AISTATS 2020 (PMLR 108)](https://proceedings.mlr.press/v108/farajtabar20a.html); [arXiv 1910.07104](https://arxiv.org/abs/1910.07104v1).
- Erro de generalização de mínimos quadrados sob design gaussiano, E‖β̂ − β‖² = σ²p/(n − p − 1): a esperança da Wishart inversa (resultado clássico, conferido aqui por simulação, P2744).

---

➡ Continua na [Parte 111 — O laboratório de palavras](ASI_AGI_parte111_o_laboratorio_de_palavras.md).
