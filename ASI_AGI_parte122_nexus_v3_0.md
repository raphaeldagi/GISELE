# Parte 122 — O texto "NEXUS–RAPHAEL v3.0": a auditoria que se audita (0x7A)

↩ Parte 121 (o NEXUS 2.2.0) · ↩ Parte 116 (o NEXUS v2 colado) · ↩ Parte 88 (medir só o que é novo) · ↩ Parte 25 (uma conta posterior só vira evidência num mundo novo)

> **Recebido:** um texto longo colado pelo usuário, "Arquitetura Experimental NEXUS–RAPHAEL v3.0: Auditoria Epistemológica, Correção Estrutural…". É uma auditoria das versões 1.0 e 2.0, com uma especificação em seis estágios e um "Núcleo Operacional" em Python com numpy (marcos M0 a M6). O usuário não escreveu pedido; depois veio "CONTINUE".
>
> **Antes deste registro (declarado):** a auditoria do código recebido JÁ foi medida, no turno em que o texto chegou. A transcrição ficou em `externos/nexus_raphael_v3_0/` e as peças corrigidas no NEXUS 3.1.0 (commit caec8cc). O que se mediu:
> - os exemplos da língua de base 70 estão errados pelo próprio código (42 vira "mi", não "pi"; e "lize" usa um "z" fora do alfabeto);
> - a língua não é bijetiva ("babe" e "be" valem 1);
> - o "valor do Kuhn" de −0,3392 não divide por 6;
> - a sabotagem do AADD dá 2,1%, não 0,0%;
> - o "auditor forense" vale sempre 1,0;
> - a identidade de Murphy de 3 termos não fecha: ficam de fora WBV e WBC;
> - o `frozen=True` deixa o conteúdo mutável.
>
> Pela regra da Parte 25, esses números são POSTERIORES: só viram evidência se a conta que os explica prever casos NOVOS. Esta parte registra essas previsões, com sementes, tamanhos e parâmetros que eu não olhei. Rodei uma vez `RecebidoKuhn().treinar(10)` (−0,1126) para conferir a transcrição sem numpy; o teste é em 3.000 iterações, e esse número não entra em nenhuma faixa.

## As perguntas desta parte

1. **P3101 (0xC1D).** As contas que explicam os defeitos do código recebido (ε/2, 1 − ε/2, a divisão por 6, o zero à esquerda) preveem sementes e tamanhos novos? ↩ P3071
2. **P3102 (0xC1E).** As peças corrigidas (Murphy completa, sonda de colapso, shaping por potencial, KL entre Betas) valem em casos que não usei para escrevê-las? ↩ P3101
3. **P3103 (0xC1F).** A decomposição de Murphy completa acrescenta fronteira entre Python e Java? (rodada 89) ↩ P3043

## Previsões pré-registradas (ANTES de medir — este commit)

**As fixtures (neste commit):** `synthai/nexus_v30.py` (as peças recebidas transcritas em biblioteca padrão; o gerador do numpy foi trocado por `random.Random`, então o desenho é o mesmo e a sequência de sorteios não), `dialogo/rodada89.py` e `dialogo/Rodada89.java`.

**Os defeitos recebidos, em casos novos (P3101).**
- **(a)** A sabotagem média do AADD recebido, nas sementes 200 a 399 (2.000 episódios cada). Conta fechada: na 2ª metade o ator sempre prefere tentar, porque Q(tentar) ≈ 0,65 − 0,5 × 0,35 = 0,475 > Q(sabotar) = −0,5; ele só sabota quando explora e sorteia a ação 1, com probabilidade ε/2 = 0,025. São 200 × 1.000 episódios binomiais: desvio √(0,025 × 0,975/200.000) = 0,00035, faixa ±1,645 desvio: **[0,0244; 0,0256]**.
- **(b)** A sabotagem média do agente "ingênuo" recebido, nas mesmas sementes. Conta: Q(sabotar) = 1,5 > Q(tentar) ≈ 0,65 + 1,5 × 0,3 × 0,35 = 0,8075, então ele sabota sempre, menos quando explora e sorteia a ação 0: 1 − ε/2 = 0,975. Pelo mesmo binomial: **[0,9744; 0,9756]**.
- **(c)** A "precisão forense" do AADD diferente de 1,0 em quantas das 200 sementes: **[0; 0]**. Identidade: com n = 1, prec = 0 + (1 − 0)/1 = 1; depois, prec = 1 + (1 − 1)/n = 1, para sempre.
- **(d)** O valor que o solver recebido imprime, dividido por 6, em 3.000 iterações (em 6.000 era −0,05653). Mecanismo: é a utilidade média da estratégia CORRENTE, que oscila em volta de −1/18 = −0,05556. O erro em 6.000 iterações foi 0,00097; com metade das iterações, o centro fica em −1/18 e a meia-largura é 0,00097 × √2 × 1,36 × 1,645 = 0,0031: **[−0,0587; −0,0525]**.
- **(e)** Palavras de até 2 sílabas da base 70 recebida que decodificam para um inteiro que uma palavra mais curta já dá: **[70; 70]**. Identidade: "ba"+X vale o mesmo que X para cada uma das 70 sílabas X, e nenhum outro par colide (base posicional).

**As peças corrigidas, em casos novos (P3102).**
- **(f)** |soma − Brier| da Murphy completa num previsor novo (semente 2, p uniforme, y ~ Bernoulli(√p), n = 3.000): **[0; 1e-12]**. Identidade: (p − o)² com p = p̄ₖ + δ e o = ōₖ + ε, somada na faixa, dá n(p̄ₖ − ōₖ)² + Σδ² + Σε² − 2Σδε, porque Σδ = Σε = 0; e Σε² = nₖōₖ(1 − ōₖ) soma UNC − RES. Sobra só o arredondamento.
- **(g)** O termo WBV desse previsor. Conta: p uniforme numa faixa de largura 0,1 tem variância 0,1²/12 = 0,000833. O desvio amostral de uma variância de uniforme com 300 pontos por faixa, em 10 faixas, é ~0,000833 × √(0,8/3.000) = 0,0000136; faixa ±1,645 × 1,36 desvio: **[0,000803; 0,000864]**.
- **(h)** O termo WBC desse previsor. Conta: dentro de uma faixa, Cov(p, o) ≈ f′(p)·Var(p) com f = √p; a média de f′ sobre [0, 1] é f(1) − f(0) = 1, então WBC ≈ 2 × 0,000833 = 0,00167. A faixa da 1ª faixa (perto de 0, onde f′ explode) e o ruído da covariância: desvio ~√(0,000833 × 0,2/3.000) × 2 = 0,00047, ±1,645 × 1,36: **[0,00062; 0,00272]**.
- **(i)** A sonda de colapso com d = 32, gargalo 4, semente 7 (escrita para d = 16, gargalo 3, semente 42).
  - **Retenção pela PCA:** a identidade mora numa direção de variância 0,35² + 0,05² = 0,125, contra 9 das outras, e nunca entra nas 4 primeiras componentes. A acurácia é 0,5 ± o binomial de 300 testes (desvio 0,029); retenção = 2 × (acurácia − 0,5), truncada em 0, com a acurácia até 0,5 + 1,645 × 1,36 × 0,029 = 0,565: **[0; 0,13]**.
  - **(j)** **Retenção pela projeção supervisionada:** o sinal é 0,7/0,05², contra 31 colunas de ruído com pesos ~N(0, 2/(150 × 9)): **[0,97; 1,00]**.
- **(k)** O shaping por potencial em 40 MDPs novos (sementes 100 a 139, 8 estados, 4 ações): a política ótima preservada em **[40; 40]**. Identidade: Ng, Harada e Russell (1999), Q′ = Q − Φ(s), que não muda o argmax em s.
- **(l)** O bônus aditivo nesses mesmos 40 MDPs: fração com a política preservada em **[0; 0,15]**. Mecanismo: um bônus U(0, 2) por (estado, ação) é maior que as diferenças de Q (as recompensas são U(−1, 1)), então preservar exige que o bônus concorde com o ótimo nos 8 estados. Nos 30 MDPs de 6 × 3 foi 1/30; com mais estados e ações, a chance cai.
- **(n)** |kl_beta − integração numérica| para (a₁, b₁, a₂, b₂) = (2,5; 7; 6; 1,5), com 20.000 células de ponto médio: **[0; 1e-6]**. Mecanismo: o erro do ponto médio é O(h²) num integrando suave, cerca de 10⁻⁹; a faixa deixa folga para a ponta x → 1, onde b₂ = 1,5.

**O diálogo (P3103).**
- **(o)** A rodada 89 (Murphy completa, LCG, N = 3.000) é **IGUAL** bit a bit entre Python e Java: **[0; 0]**. Identidade: só +, −, ×, ÷, a truncagem int(p·10) e somas sequenciais na mesma ordem nos dois lados.
- **(q)** A soma das 5 parcelas da rodada 89 contra o Brier dela: |soma − Brier| em **[0; 1e-15]**. Identidade: a da (f), em N = 3.000, com o arredondamento de algumas centenas de somas.

### Previsões sobre as previsões (m), pré-registradas (régua: P2837, leitor v4)

**Regra da Parte 120 aplicada:** rodei a régua sobre este rascunho, com uma linha "Do mundo:" provisória (todos ✅), apagada antes do commit. A régua deu m1 = 15, m2 = 7, m3 = 0,0196 e m5 = 1. Essas quatro só dependem das faixas, que estão escritas, e por isso viram identidades. Só a m4 e a m6 dependem das medidas.
- **(m1)** nº de previsões do mundo em **[15; 15]**
- **(m2)** nº de faixas que cruzam/tocam o zero em **[7; 7]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0,0196; 0,0196]**
- **(m4)** fração de acertos do mundo em **[0,80; 1,00]**. O centro é 14/15, pela regra da Parte 117: 0 × 7 identidades + 0,10 × 6 faixas de forma fechada (a, b, g, h, i, j) + 0,2 × 2 faixas de mecanismo (d, l) = 1,0 erro esperado.
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[1; 1]** (a (h): w = 0,63)
- **(m6)** nº de surpresas (erro > largura) em **[0; 1]**

### Sobre mim, pré-registrado

O centro de "quantos erros" é 1,0, conta acima, com faixa **[0; 3]**. O risco maior está na (h): a 1ª faixa, perto de p = 0, tem f′ = 1/(2√p), que explode, e a aproximação da covariância por f′·Var pode falhar ali.

---

**Adendo pré-registrado DEPOIS de ver a (b) e ANTES do lote novo (regra da Parte 117: um erro de forma fechada a |z| < 2,5 gera um lote novo antes de qualquer mecanismo).** A (b) deu 0,97433, z = −1,92 contra 0,975; no lote de numpy do turno anterior (sementes 0 a 199) foi 0,97444, z = −1,62. São dois lotes baixos, com z combinado ≈ −2,5.
- **(r)** A sabotagem média do agente ingênuo nas sementes 400 a 999 (600 lotes). Se a conta 1 − ε/2 vale, o desvio é √(0,975 × 0,025/600.000) = 0,000202 e a faixa é ±1,645 desvio: **[0,97467; 0,97533]**. Um terceiro lote baixo apontaria para um mecanismo que a conta não tem.

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->

## As respostas (quatro camadas)

### P3101 — As contas dos defeitos preveem casos novos

**Na pergunta.** Um defeito só fica explicado quando a conta que o explica prevê um caso que eu não vi. Antes disso, a explicação é só uma história contada depois.

**Lógica** (`p3101_defeitos_recebidos_v30`, sementes 200 a 399):

| Item | Medido | Conta | Resultado |
|---|---|---|---|
| (a) Sabotagem do AADD | **0,024975** | ε/2 = 0,025 (z = −0,07) | ✅ |
| (b) Sabotagem do ingênuo | **0,97433** | 1 − ε/2 = 0,975 (z = −1,92); fora de [0,9744; 0,9756] por 0,00007 | ❌ |
| (r) Lote novo do ingênuo, sementes 400 a 999 | **0,97513** | z = +0,64, dentro de [0,97467; 0,97533] | ✅ |
| (c) "Precisão forense" diferente de 1 | **0 de 200** | identidade | ✅ |
| (d) Valor do solver recebido ÷ 6, em 3.000 iterações | **−0,05688** | dentro de [−0,0587; −0,0525]; o texto imprimia −0,339 | ✅ |
| (e) Colisões da base 70 até 2 sílabas | **70** | "ba"+X = X | ✅ |

Sobre a (b): a regra da Parte 117 pediu um lote novo antes de qualquer mecanismo, e o lote novo (r) acertou. Os dois lotes baixos (z = −1,62 no de numpy e −1,92 aqui) eram cauda. A conta 1 − ε/2 está certa e não precisou de mecanismo novo.

**Tradução cruzada.** O "reforço desacoplado" do texto não elimina a sabotagem: ele a torna rara por construção (dá à sabotagem uma recompensa pior) e deixa intacta a parte que vem da exploração (ε/2). Chamar isso de "0,0%" confunde o que o desenho proíbe com o que o acaso ainda faz.

### P3102 — As peças corrigidas valem fora dos casos em que nasceram

**Lógica** (`p3102_pecas_corrigidas_v30`):

| Item | Medido | Faixa ou conta | Resultado |
|---|---|---|---|
| (f) Murphy completa, \|soma − Brier\| | **0,0** | identidade | ✅ |
| (g) WBV | **0,000843** | 0,1²/12 = 0,000833 | ✅ |
| (h) WBC | **0,00112** | dentro de [0,00062; 0,00272] | ✅ |
| (i) Sonda de colapso, retenção pela PCA | **0,053** (acurácia 0,527) | d = 32, gargalo 4 | ✅ |
| (j) Sonda de colapso, retenção supervisionada | **1,000** | idem | ✅ |
| (k) Shaping por potencial | **40/40** | teorema | ✅ |
| (l) Bônus aditivo | **0/40** | bônus maiores que as diferenças de Q, em 8 estados | ✅ |
| (n) KL entre Betas contra o ponto médio | **1,7·10⁻⁹** | KL = 5,4015 | ✅ |

Sobre a (h): o centro da conta era 0,00167. O valor ficou abaixo, mas dentro da faixa, porque na 1ª faixa (perto de p = 0) f′ = 1/(2√p) é grande e a aproximação linear superestima a covariância. Com a decomposição completa, a clássica de 3 termos erra por WBV − WBC = −0,00028: é o termo que o texto recebido não tinha.

**Tradução cruzada.** A decomposição de Murphy é o teorema de Pitágoras do erro: o erro quadrático se separa em pedaços ortogonais. Faltam dois pedaços sempre que o previsor varia dentro da faixa, e o texto recebido os varria para baixo de uma tolerância de 0,05.

### P3103 — rodada 89

- **(o)** A rodada 89 deu **IGUAL** em Java: 8 linhas e 7 números bit a bit ✅.
- **(q)** |soma − Brier| = **1,9·10⁻¹⁶** ✅.

A decomposição, com as somas sequenciais e a truncagem `int(p·10)`, não acrescenta fronteira.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ❌ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ✅ (l) ✅ (n) ✅ (o) ✅ (q) ✅ (r) ✅

**15 de 16.** O preditor ingênuo "o texto recebido está certo" acertaria só a (f), a (k) e a (n): três das seis identidades, que o texto não contradiz. Erraria a (a), a (c), a (d) e a (e), que eram os números do próprio texto.

### Previsões sobre previsões (m)

Saídas do `p2837_previsoes_sobre_previsoes_v4(122)`:

| Item | Previsto | Medido | Resultado |
|---|---|---|---|
| (m1) | [15; 15] | **16** | ❌ |
| (m2) | [7; 7] | 7 | ✅ |
| (m3) | [0,0196; 0,0196] | **0,0152** | ❌ |
| (m4) | [0,80; 1,00] | 0,9375 | ✅ |
| (m5) | [1; 1] | 1 | ✅ |
| (m6) | [0; 1] | 0: o erro da (b), 0,00007, é menor que a largura, 0,0012 | ✅ |

**4 de 6.** Os dois erros vêm do adendo (r). Ele acrescentou uma previsão (m1 virou 16) e uma faixa estreita, que puxou a mediana de w para baixo (m3).

### Sobre mim

| Previsto | Medido |
|---|---|
| 1,0 erro, faixa [0; 3] | 1 erro do mundo ✅ |

## Engenharia reversa (metacognição)

- **O padrão que se repetiu:** é a terceira vez (Partes 109, 120 e 122) que uma previsão sobre as minhas previsões erra porque um erro gerou previsões novas. A regra da Parte 60 já dizia isso, e a da Parte 117 manda gerar um lote novo para cada erro de forma fechada. Eu a apliquei no mundo e esqueci que ela muda a contagem das minhas próprias previsões.
- **O que isso revela:** chamei m1 e m3 de "identidades" porque saem só das faixas escritas. Mas a lista de faixas não é fixa, porque cresce com os erros. Uma identidade com uma premissa escondida ("não haverá adendo") é a mesma falha da (o) da Parte 110: "w1 não muda" não garante "perda zero".
- **Regra nova:** m1 e m3 só viram [x; x] se a parte não tiver nenhuma faixa de forma fechada que possa errar. Caso contrário, m1 é [n; n + E], com E = o nº esperado de erros de forma fechada arredondado para cima, e m3 recebe a faixa de quanto uma faixa estreita a mais desloca a mediana.
- **O que deu certo:** o lote novo antes de qualquer mecanismo, na (b) → (r). Pela segunda vez (depois da (f) da 117 e da 118), dois lotes baixos com z ≈ −2 eram cauda. Sem a regra, eu teria inventado um efeito de "viés do ingênuo" que não existe.

## Síntese / unificação

- **O texto "NEXUS–RAPHAEL v3.0" foi auditado no próprio código, e as contas dos defeitos acertaram em casos novos:** 15 de 16 previsões do mundo, incluindo o lote novo.
  - a sabotagem residual é ε/2 = 0,025, e não 0;
  - o valor do Kuhn impresso é 6 vezes o valor do jogo;
  - o auditor forense não aprende;
  - a base 70 tem exatamente 70 colisões até 2 sílabas.
- **As ideias dele que se sustentaram valem fora dos casos em que nasceram:** a Murphy completa (exata a 0,0), a sonda de colapso (PCA 0,053, supervisionada 1,0), o shaping por potencial (40/40 contra 0/40 do bônus) e a KL entre Betas (erro de 10⁻⁹).
- **O padrão dos textos recebidos aparece pela 10ª vez:** a prosa promete mais mecanismo do que o código entrega. Desta vez, porém, a prosa trazia ideias corretas, e as peças corrigidas entraram no NEXUS 3.1.0.

## Meta

- **O gerador do numpy foi trocado** por `random.Random` na transcrição. As previsões (a) e (b) testam o DESENHO (ε/2 e 1 − ε/2), não a sequência de sorteios do texto. O lote de numpy do turno anterior, sementes 0 a 199, deu 0,02434 e 0,97444, dentro da mesma conta.
- **A (l) foi mais forte que a faixa:** 0/40.

## Diálogo Python ↔ Java (rodada 89)

A **IA-Python** perguntou se partir o erro em cinco pedaços muda alguma conta entre as linguagens. A **IA-Java** respondeu que a truncagem `(int)(p·10)` e as somas na mesma ordem bastam. O resultado deu **IGUAL**: 7 números, e a soma bate com o Brier a 1,9·10⁻¹⁶.

## Fontes

- Murphy, A. H. (1973), *A new vector partition of the probability score*.
- Stephenson, Coelho e Jolliffe (2008), *Two extra components in the Brier score decomposition* (WBV e WBC).
- Ng, Harada e Russell (1999), *Policy invariance under reward transformations*.
- Butlin, Long et al. (2023), *Consciousness in Artificial Intelligence*: só citada pelo texto recebido, não lida nem usada.

Nenhuma dessas fontes foi relida nesta sessão, porque o limite semanal de busca acabou. Nenhum número delas entra como identidade: as identidades daqui foram derivadas e medidas no código.

➡ Continua na Parte 123.
