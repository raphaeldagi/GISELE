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
