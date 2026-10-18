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
