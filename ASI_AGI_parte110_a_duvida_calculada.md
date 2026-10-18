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
