# Parte 115 — Dez camadas contrapostas, o dicionário em algarismos e em algoritmos, e a escala contra a meta-medida (0x73)

↩ Parte 110 (o gradiente da RNN: o produto de derivadas) · ↩ Parte 103 (o dicionário convertido em números) · ↩ Parte 30 (o dicionário como data lake) · ↩ Parte 70 (álgebra e geometria: a projeção, as distâncias)

> Pedido do usuário: "Use 10 camadas contrapostas pra entender 10 gradientes sobrepostos. Conte o número de palavras no Dicionário e mude o alfabeto pra algarismos e depois pra algoritmos. Reduza a escala de vetores paradigmas e aumente as medidas meta-paradigmas e depois faça o cálculo oposto."
>
> **A leitura escolhida (regra da Parte 83, escrita ANTES de medir; `synthai/contraposto.py`).**
> - **"10 camadas contrapostas":** uma cadeia escalar de 10 camadas, hₖ = φ(wₖ·hₖ₋₁), em que os pesos alternam a e 1/a, cada camada desfazendo a escala da anterior. **"10 gradientes sobrepostos":** os 10 gradientes ∂h₁₀/∂wₖ, um por camada, que se SOMAM na variação de primeira ordem quando os 10 pesos mudam juntos (Δh ≈ Σₖ gₖ·δwₖ, o princípio da superposição do diferencial; o resto é de 2ª ordem).
> - **"Conte o número de palavras no dicionário":** os lemas do WordNet 3.0 (e da OpenWordNet-PT), contados por classe e no total. **"Mude o alfabeto para algarismos":** a palavra como NÚMERO em base 26 bijetiva (dígitos 1..26), uma codificação injetiva. **"Depois para algoritmos":** cada letra vira uma OPERAÇÃO x ↦ (a·x + b) mod p, com p = 1.000.003 primo, e a palavra é o PROGRAMA que aplica as letras em ordem a partir de x = 1. Uma palavra deixa de ser uma etiqueta e vira uma função.
> - **"Reduza a escala dos vetores paradigmas e aumente as medidas meta-paradigmas":** os vetores do dicionário (bigramas de letras das glosas, 676 dimensões) projetados em POUCAS dimensões (k = 4), com MUITAS medidas da distorção (m = 2.000 pares), sendo a meta-medida a estimativa do desvio da distorção. **"Depois o cálculo oposto":** MUITAS dimensões (k = 256) e POUCAS medidas (m = 20).
>
> **Antes do registro (condições, não resultados).**
> - **A extração contra as estatísticas publicadas do WordNet 3.0 (Princeton).** Nomes **117.798** (exato), verbos **11.529** (exato), advérbios **4.481** (exato), adjetivos **21.785**, contra os 21.479 publicados. Eu já olhei as quatro classes; elas não viram previsão. A HIPÓTESE para os 306 adjetivos a mais vira: os marcadores sintáticos colados ao lema nos arquivos de adjetivos ("(a)", "(p)", "(ip)").
> - **Para os algoritmos, as condições dos dados.** n = **77.340** palavras de letras a-z (Parte 111) e A = **72.547** classes de anagrama (multiconjuntos de letras distintos).

## As perguntas desta parte

1. **P2891 (0xB4B).** Dez camadas com o mesmo peso a > 1 explodem o gradiente como a¹⁰; contrapostas (a, 1/a), ele volta a 1? E com a não-linearidade? ↩ P2743
2. **P2892 (0xB4C).** Os 10 gradientes se sobrepõem, isto é, a soma deles prevê a variação de primeira ordem, com resto de 2ª ordem? ↩ P2891
3. **P2893 (0xB4D).** Quantas palavras o dicionário tem? ↩ P2774
4. **P2894 (0xB4E).** Em algarismos, a palavra continua única? ↩ P2532
5. **P2895 (0xB4F).** Em algoritmos, quantas palavras colidem (o mesmo resultado), com operações que não comutam e com operações que comutam? ↩ P2894
6. **P2896 (0xB50).** A distorção da projeção em k dimensões, e a precisão da sua estimativa com m medidas: pouca escala e muita medida, e o oposto. ↩ P2357
7. **P2897 (0xB51).** A cadeia contraposta (com tanh pelo exp próprio) acrescenta fronteira entre Python e Java? (rodada 82) ↩ P2865

## Previsões pré-registradas (ANTES de medir — este commit)

**As fixtures.**
- **Cadeias:** h₀ = 0,5, 10 camadas; a "mesma" usa wₖ = 1,2 (linear) ou wₖ = 2 (tanh); a contraposta, `pesos_contrapostos(a)`: a, 1/a, a, …
- **Superposição:** a cadeia tanh contraposta com a = 2, δwₖ = ε·sₖ, sₖ = −1 se k ≡ 0 (mod 3), senão +1; ε = 10⁻³ e 10⁻⁴.
- **Algoritmos:** `alfabeto_de_algoritmos(115)`, as 77.340 palavras a-z do WordNet.
- **Vetores:** `distorcoes(4, 2000)` e `distorcoes(256, 20)`, semente 1150, os pares a partir da glosa 0.

**As dez camadas (P2891/P2892).**
- **(a)** Linear, wₖ = 1,2: |∂h₁₀/∂h₀ − 6,1917364224|/6,1917364224 (1,2¹⁰ em decimal exato): **[0; 10⁻¹⁴]**. Identidade: 10 produtos, cada um com erro ≤ ½ ulp.
- **(b)** Linear contraposta (1,2; 1/1,2): |∂h₁₀/∂h₀ − 1|: **[0; 10⁻¹⁴]**. Identidade: o produto de 5 pares a·(1/a), cada um a 1 ulp de 1.
- **(c)** Tanh contraposta, a = 2: ∂h₁₀/∂h₀ = Π wₖ(1 − hₖ²). À mão: os 5 pares de fatores dão 0,365 · 0,558 · 0,662 · 0,725 · 0,768 ≈ 0,075. Faixa **[0,06; 0,09]**. A contraposição cancela os PESOS, mas não a saturação, porque (1 − h²) < 1 não se desfaz.
- **(d)** Tanh com o mesmo peso, a = 2: h vai ao ponto fixo h* = tanh(2h*) ≈ 0,9575, onde a derivada local é 2(1 − h*²) ≈ 0,167. À mão: 0,840 · 0,346 · 0,200 · 0,173 · 0,168 · 0,1665⁵ ≈ 2,2·10⁻⁷. Faixa **[1,0·10⁻⁷; 4,0·10⁻⁷]**. Mecanismo: o atrator saturado.
- **(e)** Superposição: a inclinação de log|Δh − Σ gₖ δwₖ| contra log ε, entre ε = 10⁻³ e 10⁻⁴: **[1,8; 2,2]**. O resto é de 2ª ordem; se fosse de 1ª, a soma dos gradientes estaria errada.

**O dicionário contado (P2893).**
- **(f)** Adjetivos, depois de tirar os marcadores "(a)", "(p)", "(ip)" do fim do lema: **[21.479; 21.479]**. Identidade suposta: a estatística publicada por Princeton conta o lema sem marcador. Se não der exato, a minha hipótese para os 306 está errada.
- **(g)** Pares (lema, sinset) no arquivo: **[206.941; 206.941]**. Identidade: o número de pares palavra-sentido publicado por Princeton.
- **(h)** Lemas distintos somando TODAS as classes (sem marcadores, um lema em duas classes conta uma vez): **[140.000; 152.000]**. Mecanismo esperado: a soma por classe (~155.287) menos a sobreposição entre classes ("run" nome e verbo), estimada em 2% a 10%.

**Algarismos e algoritmos (P2894/P2895).**
- **(i)** Colisões da base 26 bijetiva sobre as 77.340 palavras: **[0; 0]**. Identidade: a base bijetiva é injetiva. E a volta (`de_algarismos`) devolve cada palavra.
- **(j)** Algoritmos que NÃO comutam (afins): os pares de palavras com o mesmo resultado. Esperança C(n, 2)/p = 77.340·77.339/(2·1.000.003) = 2.990,7, e desvio de Poisson √2990,7 = 54,7: faixa **[2.900; 3.081]**. Mecanismo esperado: duas composições afins diferentes coincidem em x = 1 com probabilidade ≈ 1/p (Schwartz-Zippel limita a ≤ L/p).
- **(k)** Algoritmos que COMUTAM (translações): resultados DISTINTOS = A menos as colisões entre classes, 72.547 − C(A, 2)/p = 72.547 − 2.631,5 = 69.915,5, com desvio √2631,5 = 51,3: faixa **[69.831; 70.000]**. Identidade parcial: todo anagrama colide (a soma dos b não vê a ordem), e o resto é o aniversário entre classes. A diferença nasce de a ordem existir ou não.

**A escala contra a meta-medida (P2896).** A distorção r = ‖Px‖²/‖x‖² tem distribuição χ²_k/k para QUALQUER x, porque P é gaussiana nova por par. O desvio é √(2/k), e o desvio da estimativa desse desvio com m pares é ≈ √(2/k)/√(2m) · √(1 + 6/k) (a curtose do χ²).
- **(l)** Pouca escala (k = 4), muita medida (m = 2.000): desvio estimado. Centro √(2/4) = 0,7071, meta-desvio 0,7071/√4000 · √2,5 = 0,0177, faixa ±1,645 × 0,0177 = **[0,678; 0,736]**.
- **(n)** O oposto, muita escala (k = 256) e pouca medida (m = 20): centro √(2/256) = 0,0884, meta-desvio 0,0884/√40 · √1,023 = 0,0141, faixa **[0,065; 0,112]**.
- **(o)** A média de r com k = 4, m = 2.000: desvio da média 0,7071/√2000 = 0,0158, faixa **[0,974; 1,026]**.

**Diálogo (P2897).**
- **(p)** A cadeia tanh contraposta (a = 2), com o tanh pelo exp PRÓPRIO, frente e trás (o gradiente e os 10 ∂h/∂wₖ), é **IGUAL** bit a bit entre Python e Java: **[0; 0]**. Identidade: o exp próprio (série, Parte 52) e só +, −, ×, ÷ na mesma ordem.

### Previsões sobre as previsões (m), pré-registradas (régua: P2837, leitor v4)

- **(m1)** nº de previsões do mundo em **[14; 18]** (15 agora)
- **(m2)** nº de faixas que cruzam/tocam o zero em **[3; 6]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0; 0,20]**
- **(m4)** fração de acertos do mundo em **[0,60; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 3]**

### Sobre mim, pré-registrado

Os riscos estão em três lugares:
- **(f) e (g)**, faixas de largura zero apoiadas numa estatística publicada, que é uma identidade só se a minha extração bater com a de Princeton. A Parte 110 me ensinou que [x; x] sem a identidade certa erra, e aqui a identidade é uma HIPÓTESE (os marcadores).
- **(c) e (d)**, contas à mão de 10 fatores, onde um erro de 1% por fator vira 10%. Eu dei faixas de ±20%.
- **(h)**, uma sobreposição chutada.

Espero **1 a 3 erros**, em (f), (g) ou (h).

### Adendo pré-registrado (escrito DEPOIS da 1ª medição, ANTES destes testes)

Duas coisas saíram da 1ª medição.
- **(g) errou:** 206.978 pares, contra os 206.941 publicados, 37 a mais.
- **(l) e (n) quebraram:** um par de glosas tem vetores IGUAIS (x = 0, razão 0/0). A fixture não previa vetor nulo, um defeito meu. A correção mais conservadora: pular os pares com ‖x‖ = 0 e seguir lendo glosas até ter m pares válidos. (l), (n) e (o) ficam com as mesmas faixas, medidas na fixture corrigida, e o desvio da fixture fica registrado aqui.

- **(q) P2898.** A hipótese para os 37: Princeton conta pares (lema, sinset) DISTINTOS depois de tirar os marcadores, e o arquivo repete o mesmo lema no mesmo sinset quando ele aparece com e sem marcador (ou duas vezes). Os pares distintos (sem marcador, por sinset) dão **[206.941; 206.941]**. Se não der exato, a explicação é outra.

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->

## As respostas (quatro camadas)

### P2891 — Dez camadas contrapostas

**Na pergunta.** "Contrapostas" já diz o mecanismo: cada camada se opõe à anterior. Numa cadeia, a retropropagação MULTIPLICA as derivadas locais, e o gradiente de ponta a ponta é ∂h₁₀/∂h₀ = Πₖ wₖ·φ′(zₖ). Contrapor as camadas é escolher os fatores para que o produto não exploda nem suma.

**Lógica.**
- **Linear, peso igual 1,2:** 1,2¹⁰ = **6,19173642** (erro relativo **1,4·10⁻¹⁶**) ✅ (a), a explosão em forma fechada.
- **Linear contraposta (1,2 e 1/1,2):** o produto é **1,0 exato** (|g − 1| = 0) ✅ (b). Os cinco pares a·(1/a) se desfazem, e nem um ulp sobrou nesta cadeia.
- **Tanh contraposta (2 e 1/2):** **0,07491** ✅ (c), contra 0,075 calculado à mão no registro. A conta, com os valores: os fatores wₖ(1 − hₖ²) vão de 0,840, 0,434, 1,229, 0,455, 1,420, 0,465, 1,535, 0,472, 1,612 a 0,477, e os cinco pares dão 0,3645 · 0,5586 · 0,6611 · 0,7246 · 0,7680 = 0,0749. A contraposição desfaz os PESOS, mas não a SATURAÇÃO: 1 − h² < 1 em toda camada, e nenhum peso a desfaz.
- **Tanh de peso igual (2):** **2,14·10⁻⁷** ✅ (d). O h vai ao ponto fixo h* = **0,9575** (tanh(2h*) = h*) já na 6ª camada. Lá cada fator vale 2(1 − 0,9575²) = **0,1664**, e os pares caem para 0,0277 cada.

A contraposição mantém o gradiente **350 mil vezes** maior (0,0749/2,14·10⁻⁷ = 3,5·10⁵) com os MESMOS pesos em módulo. É o que a normalização entre camadas (e o caminho residual) faz numa rede profunda: impede que a escala se acumule.

**Tradução cruzada.** É a dialética: cada camada nega a anterior (a, depois 1/a), e a síntese (o produto) conserva a informação que uma sequência de afirmações iguais (a, a, a…) destruiria por saturação. Jung chamaria de enantiodromia regulada: o oposto que volta a cada passo impede que a energia se fixe num polo, onde a sensibilidade (o gradiente) morre.

### P2892 — Os dez gradientes sobrepostos

**Lógica.** Os 10 gradientes ∂h₁₀/∂wₖ da cadeia contraposta são 0,0187; 0,1358; 0,0373; 0,2078; 0,0554; 0,2789; 0,0731; 0,3495; 0,0908; 0,4199: as camadas de peso 1/2 (as pares) recebem mais gradiente que as de peso 2, e as do fim mais que as do começo. Mudando os 10 pesos juntos (δwₖ = ±ε), a variação real menos a soma dos 10 gradientes (o resto da superposição) vale **1,945·10⁻⁶** com ε = 10⁻³ e **1,945·10⁻⁸** com ε = 10⁻⁴: a inclinação é **2,00006** ✅ (e). Os gradientes se sobrepõem LINEARMENTE (o princípio da superposição do diferencial), e o que não se sobrepõe (a interação entre camadas, os termos ∂²h/∂wⱼ∂wₖ) é de segunda ordem, exatamente.

**Tradução cruzada.** Dez vozes falando ao mesmo tempo se somam enquanto falam baixo (ε pequeno). Quando gritam (ε grande), interferem. A física chama isso de regime linear; a superposição só vale nele, e o tamanho da interferência cai como ε².

### P2893 — Quantas palavras o dicionário tem

**Lógica.** No WordNet 3.0 (os lemas do arquivo de `dados/`):
- **Nomes:** 117.798; **verbos:** 11.529; **adjetivos:** **21.479** ✅ (f), depois de tirar os marcadores "(a)", "(p)", "(ip)"; **advérbios:** 4.481.
- A soma por classe é **155.287**, o número publicado por Princeton. Os lemas distintos no total são **147.306** ✅ (h): 7.981 lemas aparecem em mais de uma classe ("run" é nome e verbo), 5,1% da soma.
- **Uma correção depois de conferir a fonte** (na 1ª versão desta resposta eu escrevi que os 147.306 eram "exatamente o número publicado"). A página de estatísticas do WordNet 3.0 diz que o total de cadeias distintas entre as classes é **147.278**, e o meu dá **28 a mais**. Testei DEPOIS, sem registro (é posterior, regra da Parte 25), a hipótese de diferença de maiúsculas: os lemas do arquivo já estão em minúsculas, e ela não explica nada. Os 28 ficam SEM explicação, como pendência. E os próprios espelhos da documentação de Princeton divergem entre si (um espelho de Wisconsin dá 155.327 cadeias e 207.016 pares), então "o número publicado" depende da revisão do documento.
- Os pares (lema, sinset) no arquivo são **206.978**, e não os 206.941 publicados: **(g) ❌**. A explicação, testada no adendo: o arquivo repete o mesmo lema no mesmo sinset 37 vezes, quase sempre com e sem marcador. Os pares DISTINTOS sem marcador são exatamente **206.941** ✅ (q).
- **A OpenWordNet-PT** (o português): **45.313** lemas distintos em 52.672 pares.

**Meta.** As duas hipóteses sobre a forma do arquivo (os marcadores e as repetições) acertaram exatamente, mas só a primeira estava no registro. A (g) errou porque eu tratei um número publicado como identidade sem saber COMO ele foi contado (distintos ou brutos). A regra da Parte 110 ("faixa [x; x] só com a identidade que a garante") vale aqui com um acréscimo: a identidade de um número publicado inclui a REGRA DE CONTAGEM de quem publicou.

### P2894 / P2895 — Do alfabeto aos algarismos e aos algoritmos

**Lógica.**
- **Em algarismos** (base 26 bijetiva, a = 1 … z = 26): as 77.340 palavras viram 77.340 números diferentes, **0 colisões** ✅ (i), e a volta devolve cada palavra. A maior palavra a-z tem 31 letras e vira um número de **44 algarismos** (31 × log₁₀ 26 = 31 × 1,415 = 43,9). A palavra continua uma ETIQUETA: um número que só a nomeia.
- **Em algoritmos:** cada letra vira uma operação x ↦ (a·x + b) mod 1.000.003, e a palavra é o PROGRAMA. Com operações **que não comutam** (afins), **2.928** pares de palavras dão o mesmo resultado ✅ (j), contra a esperança do aniversário C(n, 2)/p = 2.990,7 (z = −1,15), com **74.494** resultados distintos. Com operações **que comutam** (translações), **69.972** resultados distintos ✅ (k), contra 72.547 − 2.631,5 = 69.915,5 (z = +1,10): todos os anagramas colidem, porque a soma não vê a ordem.

A diferença entre os dois (74.494 contra 69.972 distintos) é a INFORMAÇÃO DE ORDEM das letras: quando as letras viram operações que comutam, o dicionário perde 4.793 distinções de anagrama (77.340 − 72.547), mais as colisões do aniversário.

**Tradução cruzada.** Uma palavra como algarismo é um NOME; como algoritmo, é um VERBO, uma coisa que faz. E o que ela faz depende de a gramática das suas letras comutar ou não. Um mundo em que as ações comutam (somar) esquece a história e só lembra o inventário; um em que não comutam (compor transformações) lembra a ordem. A linguagem é do segundo tipo: "dog" e "god" têm as mesmas letras e significam coisas opostas.

### P2896 — A escala dos vetores contra a meta-medida

**Lógica.** A distorção de uma projeção gaussiana, r = ‖Px‖²/‖x‖², tem distribuição χ²_k/k para QUALQUER vetor x, porque o vetor some da conta (só a sua norma importa). Os vetores reais das glosas (676 bigramas) dão:
- **Pouca escala, muita medida** (k = 4, m = 2.000): desvio **0,7188** ✅ (l), contra √(2/4) = 0,7071 (z = +0,66), com a média **1,0073** ✅ (o). A distorção é ENORME (±72%), mas sabemos o seu tamanho com 2,5% de precisão.
- **O oposto** (k = 256, m = 20): desvio **0,1003** ✅ (n), contra √(2/256) = 0,0884 (z = +0,84). A distorção é pequena (±10%), mas a nossa estimativa dela tem 16% de incerteza.

A troca, em forma fechada: a distorção cai como √(2/k), e a incerteza da medida da distorção cai como 1/√(2m). Pouca escala com muita medida sabe PRECISAMENTE que vê MAL; muita escala com pouca medida vê BEM e não sabe o QUANTO. A fixture registrada precisou de uma correção: 1 par de glosas com os mesmos bigramas (x = 0) foi pulado; o desvio está no adendo.

**Tradução cruzada.** É a metacognição em duas contas. A cognição é ver (a escala k do vetor); a metacognição é saber o quanto se vê (a medida m sobre a medida). As duas custam recursos diferentes e não se substituem: aumentar uma não compra a outra. Um sistema pode ser muito capaz e mal calibrado sobre a própria capacidade (k grande, m pequeno), ou pouco capaz e bem ciente disso (k pequeno, m grande). O meu placar (a P1961) é a minha meta-medida: com 244 previsões, eu sei o meu acerto a ±2%.

### P2897 — rodada 82

**Lógica.** A cadeia tanh contraposta pelo exp PRÓPRIO, Python × Java: **IGUAIS, 4 linhas e 12 números bit a bit** ✅ (p). Com o tanh da libm, o gradiente difere do da série própria por 2,8·10⁻¹⁷ (meio ulp), o tamanho exato da fronteira que o exp próprio fecha. 26 rodadas.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ❌ (h) ✅ (i) ✅ (j) ✅ (k) ✅ (l) ✅ (n) ✅ (o) ✅ (p) ✅ (q) ✅. Parte 115: **16 testes, 1 erro** ((g): o número publicado conta pares DISTINTOS, e eu previ os brutos). Um defeito de fixture registrado: o par nulo de (l)/(n). Acumulado (mundo): **225 erros em 903 testes**. Calibração (P1961, Partes 80–115): **222/244 = 0,910**.

### Previsões sobre previsões (m)

Régua: P2837 (leitor v4).

| | faixa | medido | |
|---|---|---|---|
| (m1) | [14; 18] | 16 | ✅ |
| (m2) | [3; 6] | 4 | ✅ |
| (m3) | [0; 0,20] | 0,036 | ✅ |
| (m4) | [0,60; 1,00] | 0,94 | ✅ |
| (m5) | [0; 2] | 0 | ✅ |
| (m6) | [0; 3] | 1 | ✅ |

Previsões sobre previsões: **6 de 6**.

## Engenharia reversa (metacognição)

**O padrão: o número publicado como identidade.** O único erro, (g), foi tratar uma estatística publicada (206.941) como identidade sem conhecer a regra de contagem de quem a publicou. A (f), com a mesma origem, acertou, porque eu tinha uma hipótese sobre a FORMA do arquivo (os marcadores), testada por uma calibração anterior (os 306 adjetivos a mais). Na (g), eu não tinha olhado o arquivo de pares. **Significado:** uma identidade só é identidade quando eu sei POR QUE os dois números teriam de ser iguais. "Princeton publicou X" diz o QUÊ, não o COMO. Com o como na mão (a hipótese das repetições), a (q) acertou exatamente em seguida. **Regra:** para usar um número publicado como faixa [x; x], escrever ao lado a regra de contagem que o produziu (distintos ou brutos, com ou sem normalização). Sem ela, a faixa é a da incerteza sobre a regra, não zero.

**O segundo padrão: a fixture que não previu o caso degenerado.** Duas glosas com os mesmos bigramas deram um vetor-diferença nulo, e a razão 0/0 quebrou a medida. É o mesmo tipo de falha da Parte 31 ("verificar a FORMA de uma estrutura antes de usá-la": a taxonomia com ciclo, Zipf sem cabeça): eu supus vetores gerais e o dado real tinha um degenerado. **Regra:** toda fixture que divide por uma quantidade calculada do dado declara o que faz quando ela é zero, no próprio registro.

**O quarto, achado ao conferir as fontes.** Eu tinha escrito "exatamente os números publicados" para os 147.306, e a fonte diz 147.278. Também tinha citado dois endereços de memória. É o mesmo erro da (g), em versão de prosa: uma afirmação de concordância com uma fonte que eu não tinha aberto. **Regra:** "igual ao publicado" só depois de ler a fonte nesta sessão, e todo link citado vem de uma busca feita nesta sessão.

**O terceiro: as contas à mão de 10 fatores acertaram.** As faixas de (c) e (d) (±20%) couberam com folga (0,0749 contra 0,075; 2,14·10⁻⁷ contra 2,2·10⁻⁷), porque desta vez eu fiz a conta fator por fator, em vez de chutar uma ordem de grandeza. A regra da Parte 47 ("calcular à mão um exemplo do caso presente") funcionou como deve: a conta à mão é uma previsão boa quando cada passo é uma conta, não uma impressão.

## Síntese / unificação

A Parte 115 responde aos três pedidos com contas fechadas conferidas por medida (`synthai/contraposto.py`):
- **(1) Dez camadas contrapostas.** Com pesos alternando a e 1/a, o gradiente de ponta a ponta fica em 1 (exato, linear) ou em 0,075 (tanh), contra 6,19 (explosão, linear com peso igual) e 2,1·10⁻⁷ (sumiço, tanh com peso igual, no ponto fixo h* = 0,9575). A contraposição desfaz a ESCALA, mas não a SATURAÇÃO. Os dez gradientes ∂h₁₀/∂wₖ se SOBREPÕEM linearmente: o resto da superposição é de 2ª ordem (inclinação 2,00006).
- **(2) O dicionário contado.** 155.287 lemas somando as classes e 206.941 pares distintos, exatamente os números publicados de Princeton, depois de tirar os marcadores e as 37 repetições. 147.306 lemas distintos no total, 28 acima dos 147.278 publicados (sem explicação: pendência). E 45.313 lemas no português. **Em algarismos**, a base 26 bijetiva é injetiva (0 colisões, palavras de até 44 algarismos). **Em algoritmos** (cada letra uma operação mod p), as operações que não comutam guardam a ordem (2.928 colisões, só o aniversário) e as que comutam a esquecem (todos os anagramas colidem: 69.972 resultados).
- **(3) A escala contra a meta-medida.** A distorção da projeção cai como √(2/k), e a incerteza da sua medida, como 1/√(2m). Pouca escala e muita medida (k = 4, m = 2.000) dá 0,719 ± 2,5%; o oposto (k = 256, m = 20), 0,100 ± 16%. Ver bem e saber o quanto se vê são recursos diferentes.

Rodada 82: a cadeia contraposta pelo exp próprio, IGUAL (26 rodadas). 15/16 do mundo, 6/6 (m), calibração **0,910**.

## Meta

Confiança alta nas formas fechadas: (a), (b), (e), (i), (l), (n) e (o) são identidades ou teoremas de distribuição; (j) e (k) estão a |z| ≈ 1,1 do aniversário. Onde é brinquedo: a cadeia é escalar (uma rede real tem matrizes, e a contraposição de matrizes exige inversas ou ortogonalidade); as "operações" das letras são afins mod p, escolhidas ao acaso, sem significado linguístico. A leitura dos três pedidos é uma escolha minha (escrita antes, regra da Parte 83). Outra leitura de "camadas contrapostas" (duas redes adversárias, por exemplo) daria outra parte.

## Diálogo Python ↔ Java (rodada 82)

Ver `dialogo/DIALOGO.md`: a cadeia tanh contraposta (exp próprio), frente e trás, é **IGUAL**: 4 linhas e 12 números bit a bit.

## Fontes

- Estatísticas do WordNet 3.0 (155.287 cadeias por classe, 117.659 sinsets, 206.941 pares palavra-sentido; 147.278 cadeias distintas entre as classes): [WordNet 3.0, wnstats.7WN (espelho HTML da documentação)](https://research.cs.wisc.edu/zhu/space2/TTP/nlp/data/WordNet-3.0/doc/html/wnstats.7WN.html); [página do WordNet em Princeton](https://wordnet.princeton.edu/node/37); [a página de manual wnstats](https://www.mankier.com/7/wnstats). (Os links desta linha foram conferidos numa busca DEPOIS da 1ª versão do texto; a versão anterior citava endereços de memória.)
- A projeção aleatória (Johnson-Lindenstrauss) com matriz gaussiana e a distorção χ²_k/k: [Dasgupta e Gupta, "An Elementary Proof of a Theorem of Johnson and Lindenstrauss", Random Structures & Algorithms 22 (2003)](https://cse.hkust.edu.hk/mjg_lib/bibs/EmbeddingsCourse/Papers/Dimension/Dasgupta.pdf).
- O problema do gradiente que some/explode numa cadeia (produto de derivadas): [Pascanu, Mikolov e Bengio, ICML 2013](https://proceedings.mlr.press/v28/pascanu13.html).
