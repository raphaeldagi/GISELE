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

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->
