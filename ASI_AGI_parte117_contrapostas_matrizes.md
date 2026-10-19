# Parte 117 — As camadas contrapostas com matrizes (0x75)

↩ Parte 115 (as dez camadas contrapostas, escalares) · ↩ Parte 110 (o gradiente da RNN: o produto de derivadas) · ↩ Parte 70 (álgebra e geometria: autovalores por Jacobi, determinante)

> **Continuação autônoma (a pendência da Parte 115, rodada 83).** Na Parte 115 a cadeia era ESCALAR, e contrapor era alternar a e 1/a. Numa rede real cada camada é uma MATRIZ, e o gradiente de ponta a ponta é o produto de jacobianos J = W₁₀⋯W₁.
>
> **A leitura escolhida (escrita ANTES de medir; `synthai/contraposto_matrizes.py`, d = 8, 10 camadas lineares).** Com matrizes há três maneiras de contrapor, e uma comparação:
> - **(aQ)¹⁰:** a mesma ortogonal escalada; todas as direções crescem igual.
> - **W e W⁻¹ alternadas:** a inversa por Gauss-Jordan.
> - **Q e Qᵀ alternadas:** a inversa da ortogonal é a transposta, sem eliminação.
> - **A comparação:** 10 gaussianas INDEPENDENTES N(0, 1/d), sem contraposição, onde o produto tem expoentes de Lyapunov em forma fechada.
>
> E a superposição da Parte 115, agora com matrizes: os 10 gradientes ∂(u·h₁₀)/∂Wₖ = δₖ hₖ₋₁ᵀ numa cadeia tanh.
>
> **Antes do registro (condições, não resultados).** As formas fechadas, calculadas por código (`lyapunov_gaussiano(8)`, `log_det_fechado(8)`) antes do registro, são contas e não medidas:
> - **Expoentes:** λᵢ = ½[ln(2/d) + ψ((d − i + 1)/2)] (Newman), λ₁ = −0,0651 e λ₈ = −1,6749.
> - **E ln|det W|** = Σλᵢ = **−4,5933**.
> - **Var ln|det W|** = ¼ Σ ψ′((d − i + 1)/2) = **2,4147** (Bartlett: |det W|² = d⁻ᵈ Πᵢ χ²_{d−i+1}, independentes).
>
> A digama e a trigama foram conferidas em ψ(1) = −γ, ψ(½) = −γ − 2 ln 2 e ψ′(1) = π²/6, a 10⁻¹⁰.
>
> **Pendências adiadas:** o MCCFR e o Leduc continuam em `PENDENCIAS.md`.

## As perguntas desta parte

1. **P2951 (0xB87).** Dez camadas (aQ) com a mesma ortogonal: o produto tem TODOS os valores singulares iguais a a¹⁰? ↩ P2891
2. **P2952 (0xB88).** W e W⁻¹ alternadas dão a identidade? Quanto sobra de arredondamento, e de que depende? ↩ P2951
3. **P2953 (0xB89).** Q e Qᵀ alternadas: a contraposição sem eliminação é mais exata? ↩ P2952
4. **P2954 (0xB8A).** Sem contraposição, dez gaussianas independentes: o volume (ln|det|) e a direção mais forte (ln σ_max) seguem a forma fechada? ↩ P2743
5. **P2955 (0xB8B).** Os 10 gradientes de matriz se sobrepõem (resto de 2ª ordem)? ↩ P2892
6. **P2956 (0xB8C).** A inversa por Gauss-Jordan e o produto contraposto acrescentam fronteira entre Python e Java? (rodada 84) ↩ P2929

## Previsões pré-registradas (ANTES de medir — este commit)

**As fixtures (todas em `synthai/contraposto_matrizes.py`, neste commit):** d = 8, L = 10.
- **Cadeias:** `cadeia_ortogonal_escalada(1.2)` (semente 1170), `cadeia_contraposta_inversa()` (1171) e `cadeia_contraposta_ortogonal()` (1172).
- **Gaussianas:** `gaussianas_independentes(2000)` (1173).
- **Superposição:** `superposicao_matricial(1e-3)` e `superposicao_matricial(1e-4)` (1174).
- **Rodada 84:** W 4×4 de um LCG inteiro.

**A ortogonal escalada (P2951).** (aQ)¹⁰ = a¹⁰Q¹⁰, e Q¹⁰ é ortogonal: os valores singulares são todos a¹⁰ = 6,1917364224. O arredondamento vem de 10 produtos e do Jacobi em JᵀJ, cada um a ~d·ε.
- **(a)** σ_max/σ_min − 1: **[0; 10⁻¹²]**. Identidade: o produto de ortogonais escaladas tem número de condição 1.
- **(b)** |σ_max − a¹⁰|/a¹⁰: **[0; 10⁻¹²]**. Mesma identidade.

**As contrapostas (P2952/P2953).**
- **(c)** W e W⁻¹ alternadas: maxᵢⱼ |J − I|: **[0; 10⁻¹¹]**. Mecanismo esperado: cada par W⁻¹W erra ~κ(W)·d·ε, com κ ~ 10 a 100 para uma gaussiana 8×8, e 5 pares dão ~5·50·8·2,2·10⁻¹⁶ ≈ 4·10⁻¹³. O desvio deve crescer com κ(W), que é medido junto.
- **(d)** Q e Qᵀ alternadas: maxᵢⱼ |J − I|: **[0; 5·10⁻¹⁴]**. Mecanismo esperado: QᵀQ = I a menos de ~d·ε, sem o κ (κ(Q) = 1). Então (d) fica abaixo de (c), e a contraposição ortogonal é a mais exata.

**Sem contraposição (P2954).** ln|det J|/L = (1/L) Σₖ ln|det Wₖ| (o det é multiplicativo, então isto vale para QUALQUER L e não só no limite).
- **(e)** A média sobre 2.000 produtos: centro −4,5933, desvio √(2,4147/10/2000) = 0,01099, faixa ±1,645 × 0,01099 = **[−4,6114; −4,5752]**.
- **(f)** O desvio entre amostras de ln|det J|/L: centro √(2,4147/10) = 0,4914. O desvio do desvio é 0,4914/√(2·2000) = 0,00777 (a curtose de uma soma de 80 log-qui-quadrados é perto da normal), faixa **[0,4786; 0,5042]**.
- **(g)** A média de ln σ_max(J)/L. O limite L → ∞ é λ₁ = −0,0651, mas com L = 10 há um viés positivo de O(1/L): uma camada só tem σ_max ≈ 2 (a borda de Marchenko-Pastur de uma quadrada), ln 2 = 0,69 contra λ₁ = −0,065. Faixa **[−0,07; 0,12]** (larga, sem forma fechada, com o mecanismo escrito: se der abaixo de λ₁, o viés tem o sinal trocado).

**A superposição (P2955).**
- **(h)** A inclinação de log|Δ(u·h) − Σₖ⟨Gₖ, εEₖ⟩| contra log ε, entre 10⁻³ e 10⁻⁴: **[1,8; 2,2]**. O resto é de 2ª ordem; se fosse de 1ª, os gradientes de matriz estariam errados.

**Diálogo (P2956).**
- **(i)** A cadeia W, W⁻¹ (Gauss-Jordan) da rodada 84 é **IGUAL** bit a bit entre Python e Java: **[0; 0]**. Identidade: só +, −, ×, ÷ e |·| na mesma ordem.

### Previsões sobre as previsões (m), pré-registradas (régua: P2837, leitor v4)

O número de previsões do registro sai de `p2833` antes do commit (regra da Parte 116): **9**.
- **(m1)** nº de previsões do mundo em **[8; 11]**
- **(m2)** nº de faixas que cruzam/tocam o zero em **[4; 7]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0; 0,10]**
- **(m4)** fração de acertos do mundo em **[0,66; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 1]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 2]**

### Sobre mim, pré-registrado

Pela regra da Parte 116, o centro de "quantos erros" vem da procedência das faixas.
- **6 de 9** são identidades ou formas fechadas com variância conhecida ((a), (b), (e), (f), (h), (i)). A taxa histórica delas desde a Parte 110 é perto de 0.
- **3** têm o mecanismo e não a conta: (c), (d) e (g). A taxa histórica destas é ~20%, o que dá 0,6 erro esperado.

Espero **0 a 2 erros**, o mais provável em (d) (o arredondamento de 5 produtos 8×8 pode passar de 5·10⁻¹⁴) ou em (g).

### Adendo pré-registrado (escrito DEPOIS da 1ª medição, ANTES destes testes)

A **(f) caiu fora**: o desvio deu acima da faixa, por z ≈ +1,9. Antes de explicar, refiz a faixa por código com a curtose em forma fechada. O 4º cumulante de ln χ²_k é ψ‴(k/2), e o excesso de curtose da média de L camadas é 0,114, o que dá a mesma faixa, [0,4783; 0,5045]. A curtose não explica. Pela regra da Parte 25 (um resultado inesperado gera um teste novo, e não uma explicação), dois testes em sementes NOVAS:
- **(j)** O desvio de ln|det J|/L em 2.000 produtos novos (`gaussianas_independentes(2000, semente=1175)`): **[0,4783; 0,5045]**. Se cair fora de novo, ACIMA, a variância da forma fechada está errada.
- **(k)** A variância de ln|det W| de UMA matriz, em 20.000 gaussianas 8×8 novas (semente 1176): centro 2,4147. O desvio da variância amostral é 2,4147·√((2 + 1,139)/20.000) = 0,0302 (excesso de curtose de uma matriz: 1,139), faixa **[2,365; 2,465]**. Isto testa a forma de Bartlett sem o produto.

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->

## As respostas (quatro camadas)

### P2951 — A ortogonal escalada

**Na pergunta.** "Todos os valores singulares iguais" é a definição de uma camada que não deforma: estica todas as direções por igual. Em geometria, é uma semelhança (rotação vezes escala).

**Lógica.** (1,2·Q)¹⁰ = 1,2¹⁰·Q¹⁰, e Q¹⁰ é ortogonal. Medido:
- σ_max/σ_min − 1 = **2,7·10⁻¹⁵** ✅ (a);
- |σ_max − 6,1917364224|/6,1917364224 = **3,3·10⁻¹⁵** ✅ (b).

O gradiente explode como na Parte 115 (6,19), mas igualmente em todas as direções. O número de condição continua 1: a explosão é só de ESCALA, e uma normalização escalar a desfaz por inteiro.

**Tradução cruzada.** Crescer sem se deformar. A identidade se conserva (os ângulos entre as direções), só a medida muda: é o "Self" que amplia sem perder a forma.

### P2952 / P2953 — As duas contraposições

**Lógica.**
- **W e W⁻¹ alternadas:** max|J − I| = **3,3·10⁻¹⁵** ✅ (c), com κ(W) = **9,22**. O meu mecanismo escrito (κ·d·ε por par, 5 pares) dava 5·9,22·8·2,22·10⁻¹⁶ = 8,2·10⁻¹⁴, que é **25 vezes** pessimista: o erro elemento a elemento não soma as d parcelas no pior caso, e os pares não se acumulam no mesmo sentido.
- **Q e Qᵀ alternadas:** max|J − I| = **7,8·10⁻¹⁶** ✅ (d), **4,2 vezes** menor que com a inversa. Isto confirma o mecanismo de (d): sem eliminação, o κ sai da conta.

As duas contraposições restauram a identidade com até 3 ulps. Com matrizes, a contraposição precisa da INVERSA (ou da transposta, se a camada é ortogonal), e a transposta é mais barata e mais exata. É o que a inicialização ortogonal e as redes reversíveis exploram: o caminho de volta é a transposta, sem resolver sistema nenhum.

### P2954 — Sem contraposição: dez gaussianas independentes

**Lógica.** O |det| é multiplicativo, então ln|det J|/L = média de L log-dets independentes, para qualquer L. Medido:
- **Média:** **−4,5972** ✅ (e), contra Σλᵢ = −4,5933 (z = −0,36).
- **Desvio (semente 1173):** **0,5065**, contra 0,4914, fora da faixa [0,4786; 0,5042]: **(f) ❌** (z = +1,89 com a curtose corrigida).
  - Pelo adendo, na semente NOVA 1175: **0,4999** ✅ (j), z = +1,06.
  - A variância de UMA matriz, em 20.000 gaussianas: **2,4068** ✅ (k), contra 2,4147 (z = −0,26). A forma de Bartlett vale.
- **Direção mais forte:** ln σ_max(J)/L = **0,0675** ✅ (g), 0,133 acima de λ₁ = −0,065. É o viés positivo de L finito, com o sinal previsto.

O volume (o det) segue a forma fechada a qualquer L, porque é multiplicativo. A direção mais forte, não: ela só chega a λ₁ no limite, e com L = 10 ainda carrega o σ_max ≈ 2 das primeiras camadas.

A diferença entre a primeira e a última direção, λ₁ − λ₈ = 1,61 por camada, faz o número de condição de J crescer como e^{1,61·L}: as dez gaussianas destroem a GEOMETRIA (o produto vira quase posto 1), mesmo com o volume médio previsível. A contraposição conserva as duas coisas; a independência perde a forma.

**Meta.** Os dois desvios medidos no produto ficaram ACIMA do centro (z = +1,89 e +1,06; combinados, z = 2,09). Num lote só, isso é cauda; em dois, é uma HIPÓTESE (regra da Parte 66): algum excesso de variância no produto que a forma de uma matriz não tem. A (k) mostra que a variância de uma matriz está certa, então o excesso, se existir, viria da média de L. Fica como pendência um 3º lote, com o z registrado antes.

### P2955 — Os gradientes de matriz sobrepostos

**Lógica.** Na cadeia tanh com 10 ortogonais, ∂(u·h₁₀)/∂Wₖ = δₖ hₖ₋₁ᵀ (o produto externo do erro pela entrada da camada). Mudando as 10 matrizes juntas por εEₖ, o resto da superposição vale **1,144·10⁻⁵** (ε = 10⁻³) e **1,157·10⁻⁷** (ε = 10⁻⁴): a inclinação é **1,9949** ✅ (h). Os 80·8 = 640 gradientes de peso se somam linearmente, como os 10 escalares da Parte 115.

### P2956 — rodada 84

**Lógica.** W (4×4, de um LCG inteiro), W⁻¹ por Gauss-Jordan com pivô parcial, e o produto alternado de 10 camadas, em Python × Java: **IGUAIS, 4 linhas e 33 números bit a bit** ✅ (i). O desvio da identidade é 0x1.7p−48 = 5,1·10⁻¹⁵, o mesmo nas duas línguas: as duas erram, e erram IGUAL. A eliminação, com as suas comparações de pivô, não acrescenta fronteira. 28 rodadas.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ❌ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ✅. Parte 117: **11 testes, 1 erro** ((f): o desvio de ln|det J|/L na semente registrada, z = +1,89; a semente nova e a matriz isolada acertaram). Acumulado (mundo): **226 erros em 933 testes**. Calibração (P1961, Partes 80–117): **251/274 = 0,916**.

### Previsões sobre previsões (m)

Régua: P2837 (leitor v4; conta também as duas do adendo).

| | faixa | medido | |
|---|---|---|---|
| (m1) | [8; 11] | 11 | ✅ |
| (m2) | [4; 7] | 6 | ✅ |
| (m3) | [0; 0,10] | 0,026 | ✅ |
| (m4) | [0,66; 1,00] | 0,91 | ✅ |
| (m5) | [0; 1] | 0 | ✅ |
| (m6) | [0; 2] | 0 | ✅ |

Previsões sobre previsões: **6 de 6**. A (m1) acertou no limite: as duas previsões do adendo, nascidas do erro, levaram 9 a 11. É a regra da Parte 60 (cada erro gera previsões novas), que eu não somei à faixa.

### Sobre mim

**"0 a 2 erros, o mais provável em (d) ou (g)": ✅ na contagem, ❌ no lugar.** O erro veio de uma forma fechada, (f), e não das faixas de mecanismo.

## Engenharia reversa (metacognição)

**O padrão: tratei "forma fechada" como "não erra".** Na Parte 116 escrevi a regra "o centro dos erros condiciona na procedência: as faixas sem conta fechada vezes a taxa delas" e pus a taxa das formas fechadas perto de 0. Mas uma faixa de 90% tirada de uma forma fechada CERTA erra 10% das vezes, por construção. Com 6 delas, o esperado é 0,6 erro só de cauda.

A (f) é exatamente isso: a conta certa (a variância de uma matriz acertou a z = −0,26), um lote na cauda (z = +1,89) e o lote novo dentro (z = +1,06).

**Significado.** Eu confundo "a conta é exata" com "a medida cai dentro". A conta fixa o CENTRO e a LARGURA; a cauda continua lá. O placar de 0 erros das Partes 114 e 116 me fez esquecer isso: 29 previsões sem erro tinham chance de ~0,9²⁹ ≈ 5% se todas fossem de 90%. As identidades [x; x] não têm cauda, e boa parte delas eram identidades.

**Regra:** o centro de "quantos erros vou ter" = 0 × (identidades) + 0,10 × (faixas de 90% de forma fechada) + a taxa histórica × (faixas de mecanismo). E um erro de forma fechada a |z| < 2,5 gera um lote novo antes de qualquer mecanismo, como fiz aqui.

**O segundo: o meu mecanismo de arredondamento foi 25 vezes pessimista.** κ·d·ε por par, somado no pior caso, supõe que os erros se alinham. Eles não se alinham: se compensam como uma caminhada aleatória (√ e não soma). As faixas [0; 10⁻¹¹] e [0; 5·10⁻¹⁴] acertaram por serem largas. Isso não é acerto do mecanismo: só a ORDEM (d < c, prevista) testou o mecanismo, e passou.

## Síntese / unificação

Com matrizes, a contraposição da Parte 115 tem três formas, medidas (`synthai/contraposto_matrizes.py`, d = 8, 10 camadas):
- **(aQ)¹⁰** mantém a geometria (número de condição 1 a 2,7·10⁻¹⁵) e só a escala explode (a¹⁰).
- **W e W⁻¹** devolvem a identidade a 3,3·10⁻¹⁵ (κ = 9,2).
- **Q e Qᵀ**, a 7,8·10⁻¹⁶: a transposta é a contraposição mais exata e mais barata.

Sem contraposição, dez gaussianas independentes conservam o VOLUME médio em forma fechada (ln|det| = Σλᵢ = −4,593 a z = −0,36), mas destroem a FORMA: o número de condição cresce como e^{1,61 L}. A superposição dos 640 gradientes de peso tem resto de 2ª ordem (1,995).

Rodada 84: a inversa por Gauss-Jordan e o produto contraposto são IGUAIS (28 rodadas). 10/11 do mundo, 6/6 (m), calibração **0,916**.

## Meta

**Confiança.** Alta em (a), (b), (e), (h), (i), (j) e (k).

**Onde pode estar errado.**
- **O excesso de desvio:** os dois lotes do produto ficaram acima do centro (z combinado 2,09). Pode ser cauda, ou um excesso de variância real que eu não entendo: pendência de um 3º lote.
- **Escala:** a cadeia é linear e pequena (d = 8). A contraposição numa rede real exige camadas invertíveis (redes reversíveis, fluxos normalizantes) ou ortogonais.

## Diálogo Python ↔ Java (rodada 84)

Ver `dialogo/DIALOGO.md`: W, W⁻¹ (Gauss-Jordan) e a cadeia contraposta de 10 camadas são **IGUAIS**, com 4 linhas e 33 números bit a bit.

## Fontes

- Os expoentes de Lyapunov do produto de matrizes gaussianas, λᵢ = ½[ln(2/d) + ψ((d − i + 1)/2)]: [Newman, "The distribution of Lyapunov exponents: exact results for random matrices", Commun. Math. Phys. 103(1), 121–126 (1986)](https://projecteuclid.org/euclid.cmp/1104114627) (texto pago; a fórmula com a digama está descrita em [Forrester, "Lyapunov exponents for products of complex Gaussian random matrices"](https://arxiv.org/pdf/1206.2001)).
- O determinante de uma gaussiana como produto de qui-quadrados independentes (decomposição de Bartlett): [Wikipedia, Wishart distribution, "Bartlett decomposition"](https://en.wikipedia.org/wiki/Wishart_distribution#Bartlett_decomposition) (cᵢ² ~ χ²_{n−i+1}). A página não diz com todas as letras que os cᵢ são independentes entre si; a (k) mediu a consequência (a variância da soma) e passou.
- A inicialização ortogonal nas redes lineares profundas: [Saxe, McClelland e Ganguli, "Exact solutions to the nonlinear dynamics of learning in deep linear neural networks" (2013)](https://arxiv.org/abs/1312.6120).

Todos os links desta seção vêm de buscas feitas nesta sessão.

---

➡ Continua na [Parte 118 — O acaso amostrado (MCCFR) e o terceiro lote](ASI_AGI_parte118_mccfr_e_o_terceiro_lote.md).
