# Como eu construiria uma AGI/ASI — Parte 86 (0x56): o cérebro na CPU

> Continuação da [Parte 85](ASI_AGI_parte85_a_arquitetura_recursiva_recebida.md). Pedido do usuário: dois relatórios — um sobre uma "AGI/ASI doméstica" de baixo custo (modelos de pesos abertos, GRPO/FP8,
> Exo, Vector Graph RAG, MCP/E2B) e outro sobre "IA biologicamente inspirada em CPUs de consumo" (SNN, LIF, Izhikevich, STDP/R-STDP, SDR, NEF/SPA, com contas exatas de FLOPS, memória e vazão). Mais:
> **"Grave na memória. Código final consolidado ao término de toda mensagem."**
>
> Uma parte de auditoria (como as 72–77, 82, 85): os textos são dados, não executados; as afirmações testáveis viram contas. O segundo relatório é rico em aritmética exata (β = e^(−Δt/τ), contagens de
> FLOPS, pegada de memória, GSOPS, esparsidade de SDR) — é aí que concentro o trabalho, porque é o que dá para conferir. Do primeiro relatório, os números são benchmarks de modelos que não posso verificar
> (alguns parecem não existir ainda, como "DeepSeek-V4-Pro 1,6T" ou "Qwen3.6-27B"); registro isso e não os pontuo como previsão.
>
> **Além da auditoria, esta parte CONSTRÓI:** um módulo de neurônio pulsado (LIF e Izhikevich) e STDP em `synthai/`, biblioteca padrão, que é a primeira peça da SYNTHAI que não é decisão bayesiana nem GPT —
> um substrato pulsado, medido contra as contas do relatório.

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[4; 8]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,80]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** o número de surpresas em **[0; 3]**

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,392; 0,420]** | o estatístico |
| testes de unidade | **[4 + S; 9 + S]** | um módulo novo (neurônio pulsado) + auditorias: mais testes que o normal |
| testes do placar | **7 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

Reimplemento as peças testáveis do segundo relatório (biblioteca padrão; o texto fica em `externos/`). Contas exatas/categóricas não levam o fator 1,36; a de SDR tem variância de forma fechada.

- **(a)** o LIF discretizado uₜ₊₁ = β·uₜ + (1−β)(u_rest + R·I), β = e^(−Δt/τ): o ponto fixo é EXATAMENTE u_rest + R·I; o erro da convergência (200 passos) em **[0; 1e−9]** (categórico)
- **(b)** o neurônio de Izhikevich com parâmetros diferentes dá padrões diferentes: com I = 10, dt = 0,5 ms, 1000 ms, o "chattering" (c = −50, d = 2) dispara MAIS que o "regular spiking" (c = −65, d = 8);
  previsão: RS em **[10; 90]** disparos, CH em **[60; 400]**, e CH > RS
- **(c)** a aritmética de memória do relatório: 1M neurônios × 32 B = 32 MB e 1e9 sinapses × 6 B = 6,0 GB, total **6,03 GB**, está CERTA; mas há DUAS incoerências internas: "sobretaxa de 7%" no texto contra "≈1,2×"
  (= 20%) na tabela para o Padded-CSR, e o HTM "≈8,5 GB" contra a regra de 6 B/sinapse (1,2e9 × 6 = 7,2 GB) (categórico: as duas incoerências existem)
- **(d)** a cadeia de vazão: 1M × 10 Hz → 10.000 disparos/ms → 10⁷ sinapses/ms → **10 GSOPS**, está CERTA (categórico)
- **(e)** a sobreposição de duas SDRs independentes (N = 2048, k = 40): a média é k²/N = 0,781; o simulado (10.000 pares, semente 86) em **[0,70; 0,86]** (forma fechada: desvio √(k·(k/N)·(1−k/N)) ≈ 0,88, da média /√10000 → faixa estreita)
- **(f)** a STDP com A₊ = A₋ e τ₊ = τ₋: a soma líquida de Δw sobre uma grade simétrica de Δt é ≈ 0; |líquido| em **[0; 0,02]** (categórico: as áreas de potenciação e depressão se cancelam)
- **(g)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80, 81, 83, 84, 85, 86 em **[0,75; 0,89]**

Do primeiro relatório (AGI doméstica): os benchmarks (ex.: "DeepSeek-V4-Pro 1,6T, 80,6% SWE-bench"; "Qwen3.6-27B") não são verificáveis aqui e alguns parecem ser de modelos que não existem; não os pontuo.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [4; 8] | **7.0000** | ✅ |
| (m2) | [0; 3] | **2.0000** | ✅ |
| (m3) | [0.05; 0.8] | **0.1026** | ✅ |
| (m4) | [0.45; 1.0] | **0.8571** | ✅ |
| (m5) | [0; 3] | **1.0000** | ✅ |
| (m6) | [0; 3] | **1.0000** | ✅ |

Registradas antes de eu pensar faixa nenhuma do mundo (a ordem que a Parte 70 pediu). **6 de 6** previsões sobre as minhas previsões dentro da faixa.

## As perguntas desta parte

1. **P2021 (0x7E5).** O LIF discretizado converge ao ponto fixo analítico — e quão rápido? ↩ P2021 (nova)
2. **P2022 (0x7E6).** O modelo de Izhikevich reproduz tipos celulares diferentes com os mesmos poucos FLOPS? ↩ o relatório
3. **P2023–P2024 (0x7E7–0x7E8).** A aritmética de memória e de vazão do relatório está certa, e é coerente consigo? ↩ P32
4. **P2025 (0x7E9).** A sobreposição de SDRs independentes: o relatório acerta a esparsidade? ↩ o relatório
5. **P2026 (0x7EA).** A STDP: as áreas de potenciação e depressão se cancelam quando simétricas? ↩ o relatório
6. **A rodada 53.** O passo de Izhikevich, bit a bit. ↩ rodada 52
7. **P1961 (continuando), P2049–P2050.** O teste (g) da calibração, engenharia reversa, placar, unificação.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [4; 8] | **7.0000** | ✅ |
| (m2) | [0; 3] | **2.0000** | ✅ |
| (m3) | [0.05; 0.8] | **0.1026** | ✅ |
| (m4) | [0.45; 1.0] | **0.8571** | ✅ |
| (m5) | [0; 3] | **1.0000** | ✅ |
| (m6) | [0; 3] | **1.0000** | ✅ |

Registradas antes de eu pensar faixa nenhuma do mundo (a ordem que a Parte 70 pediu). **6 de 6** previsões sobre as minhas previsões dentro da faixa.

## As respostas

### O que construo nesta parte

Além de auditar, esta parte acrescenta à SYNTHAI o módulo `synthai/pulsado.py`: o neurônio LIF, o de Izhikevich e a plasticidade STDP, em biblioteca padrão. É a primeira peça do agente que não é decisão
bayesiana (Partes 23–38) nem GPT (Partes 69–70): um substrato PULSADO, orientado a eventos. Não afirmo que ele seja um cérebro — afirmo o que a medida mostra: ele reproduz as contas do relatório.

### P2021 (0x7E5). O LIF e o seu ponto fixo ✅ (conta) / ❌ (minha faixa)

**Na pergunta.** O relatório dá o LIF discretizado uₜ₊₁ = β·uₜ + (1−β)(u_rest + R·I), com β = e^(−Δt/τ). A pergunta: para onde ele converge, e quão rápido?

**Lógica (a conta, com a substituição).** O ponto fixo resolve u* = β·u* + (1−β)(u_rest + R·I) ⟹ u* = u_rest + R·I, **exatamente**. Com u_rest = −65, R = 1, I = 20: u* = **−45**. A convergência é geométrica:
o erro após n passos é |u₀ − u*|·βⁿ. Com β = e^(−1/10) = 0,9048, gap₀ = |−65 − (−45)| = 20 e n = 200: 20·0,9048²⁰⁰ = 20·e^(−20) = **4,12 × 10⁻⁸**.

**Medido:** erro = **4,122 × 10⁻⁸**, e a conta gap·β²⁰⁰ = 4,122 × 10⁻⁸ — batem a 12 casas (`p2021`). O ponto fixo analítico é exato. **Mas a minha previsão (a) [0; 1e−9] ERROU:** eu disse "converge a ~0" e
esqueci o prefator (o gap inicial, ×20). É o viés das Partes 53 e 62 (esquecer o peso/prefator de um mecanismo que eu identifiquei certo). O mecanismo eu acertei; o número, não.

### P2022 (0x7E6). Izhikevich: muitos tipos, poucos FLOPS ✅

**Na pergunta.** O relatório afirma ~13 FLOPS por passo para Izhikevich (contra >120 de Hodgkin-Huxley) e que (a, b, c, d) escolhem o tipo celular. Testo o segundo: com I = 10, dt = 0,5 ms, 1000 ms,
- regular spiking (c = −65, d = 8): **22** disparos;
- chattering (c = −50, d = 2): **73** disparos, CH > RS (b) ✅.

O mesmo algoritmo (duas equações, só aritmética) dá dinâmicas diferentes mudando quatro números. A contagem de FLOPS confere a olho: v' = 0,04v² + 5v + 140 − u + I são ~7 operações, u' = a(bv − u) são ~4,
mais os meios-passos: na casa dos 13, como o relatório diz. É o oposto de Hodgkin-Huxley, que precisa de exponenciais (a fronteira da Parte 52) e não vetoriza bem.

### P2023–P2024 (0x7E7–0x7E8). A memória e a vazão ✅✅

**A aritmética do relatório está certa:** 1M neurônios × 32 B = **32 MB**; 1e9 sinapses × 6 B = **6,0 GB**; total **6,03 GB** (c), dentro dos 32 GB. A cadeia de vazão: 1M × 10 Hz = 10.000 disparos/ms; ×1000
sinapses = 10⁷ sinapses/ms; ×1000 = **10 GSOPS** (d) ✅.

**Mas há duas incoerências internas** (`p2023`), que a leitura cuidadosa (não o cálculo) revela:
- o Padded-CSR tem "sobretaxa de 7%" no texto, mas "≈1,2×" (= 20%) na tabela — não podem ser as duas;
- o HTM aparece com "≈8,5 GB" para 1,2 bilhão de sinapses, mas a regra de 6 B/sinapse dá 1,2e9 × 6 = **7,2 GB**.

A aritmética grossa fecha; os detalhes se contradizem. É o padrão das Partes 72–85 nos textos recebidos: o número de manchete está certo, a consistência fina não.

### P2025 (0x7E9). A esparsidade da SDR ✅

N = 2048, k = 40 → esparsidade 40/2048 = 1,95% ≈ 2%, como o relatório diz. A sobreposição esperada de duas SDRs INDEPENDENTES é k·(k/N) = k²/N = 1600/2048 = **0,781**. Medido (10.000 pares): **0,777** (e) ✅
[0,70; 0,86]. A operação (AND + POPCNT em hardware) é o produto interno de dois vetores binários; o valor baixo (< 1 bit em comum, por acaso, entre 40) é o que dá à SDR a sua capacidade de distinguir
milhões de conceitos sem colisão.

### P2026 (0x7EA). A STDP e o cancelamento ✅

Δw = A₊·e^(−Δt/τ₊) se Δt > 0 (pré antes de pós: potencia), −A₋·e^(Δt/τ₋) se Δt ≤ 0 (deprime). A soma líquida sobre uma grade simétrica de Δt é A₊τ₊ − A₋τ₋. Com A₊ = A₋ e τ₊ = τ₋: **0,0** (f) ✅ (as áreas
se cancelam). Com A₋ = 0,12 > A₊ = 0,1 (a assimetria estabilizadora que impede a explosão dos pesos): **−0,387** < 0. O sinal da aprendizagem não supervisionada é decidido pela razão das áreas, não por um
disparo isolado.

### A rodada 53 ✅

O passo de Izhikevich, 400 passos, bit a bit: **IGUAIS, 800 números** (sem libm; a ordem das somas basta, as Partes 34 e 85). 5 disparos. Registro em `dialogo/DIALOGO.md`.

### P1961 (0x7A9). O teste (g) da calibração ✅

Com a Parte 86, o acerto das Partes 80–86 é **32/41 = 0,780** (g) ✅ [0,75; 0,89]: 80 (4/4), 81 (2/3), 83 (14/15), 84 (3/9), 85 (4/4), 86 (5/6). Estável em ~0,78, ainda puxado pela Parte 84. A Parte 86
acertou 5 de 6 — o único erro foi a minha faixa apertada no LIF, não um palpite de mecanismo.

### P2049 (0x801). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 1 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 1)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **16511** | [13039; 22082] | ✅ | [13039; 22082] | ✅ | 22290 | 1050 | 5779 |
| compressão | **0.4166** | [0.3973; 0.4221] | ✅ | [0.3920; 0.4200] | ✅ | 0.4177 | 0.0106 | 0.0011 |
| testes de unidade | **8** | [2.87; 8.63] | ✅ | [5.00; 10.00] | ✅ | 6 | 0.50 | 2.00 |
| testes do placar | **7** | [5.67; 10.33] | ✅ | [7.00; 9.00] | ✅ | 8 | 1.00 | 1.00 |
| erros do placar | **1** | [-0.58; 3.33] | ✅ | [0.00; 3.33] | ✅ | 2 | 0.67 | 1.00 |
| redundância P821 | **0.5732** | [0.5631; 0.6510] | ✅ | [0.5630; 0.6510] | ✅ | 0.5877 | 0.0338 | 0.0146 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 6 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 7 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 71"):** mais perto do medido em **3 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **14927**, compressão **0.4228**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 1 de 1 erros.
- **Erros de processo nesta parte:** 0 ().

### P2050 (0x802). Engenharia reversa e Jung

**O padrão que se repetiu: eu identifico o mecanismo certo e erro o prefator.** A previsão (a) do LIF dizia "converge a ~0" — e o mecanismo (decaimento geométrico βⁿ) estava certo, mas eu esqueci multiplicar
pelo gap inicial (×20), e o erro real (4e−8) ficou 40 vezes acima da minha faixa. É exatamente o diagnóstico das Partes 53 ("deslocar o centro só por mecanismo conferido") e 62 ("um mecanismo ganha uma conta do
seu PESO antes de prever"): eu tinha o mecanismo, não fiz a conta do peso. A regra existe desde a Parte 62 e eu a quebrei de novo — a Parte 49 de novo (uma regra só vale quando vira passo verificável). A conta de
(a) devia ter sido gap·βⁿ no papel ANTES da faixa, não "~0".

**O contraste que se repete nos textos recebidos.** Pela quinta parte seguida (72, 82, 83, 85, 86), um texto recebido acerta o número de manchete e erra a consistência fina: aqui, 6,03 GB e 10 GSOPS corretos,
mas "7% vs 20%" e "8,5 vs 7,2 GB" contraditórios. O que isso revela sobre como esses textos são feitos: a conta principal é verificada, os detalhes de tabela são preenchidos por estimativa. A minha auditoria
acerta quando procura a incoerência INTERNA (dois números do mesmo texto que não batem), não a verdade externa (que eu não posso checar).

**Jung: o pulsado como função inferior.** A SYNTHAI era decisão e linguagem (pensamento e fala); o neurônio pulsado é a sensação — a função que lida com o sinal cru, orientada a evento, sem conceito. Onde a
formalização funciona: o LIF e o Izhikevich são a sensação como equação (integra, dispara, esquece). Onde quebra: Jung veria a integração das quatro funções; aqui eu só ACRESCENTEI um módulo isolado, não o
integrei ao agente que decide — a síntese fica para uma parte futura, e dizer isso é mais honesto que fingir que o cérebro já está lá.

### O diálogo

Placar por voz da função `p1241_placar_por_voz(53)`: IA-Python 25 em 39; IA-Java 21 em 38 (regra estrita, rodadas 13 a 53).

### Placar

Do mundo: (a) ❌ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅. Parte 86: **7 testes, 1 erros**. Acumulado (mundo): **211 erros em 697 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 7 pNN novas sem teste ✅. Sobre mim (placar separado): **7 de 7** dentro da faixa condicional; sobre as minhas previsões, 6 de 6; o estatístico, 6 de 6; e 0 erros de processo (P1335).

### Unificação

- **Novo módulo:** `synthai/pulsado.py` (LIF, Izhikevich, STDP, SDR). **Novas funções:** `p2021`–`p2027`. Regressão: + P2022, P2024, P2027.
- **Rodada 53** (IGUAL). Textos recebidos em `externos/texto_recebido_parte86.md` (dado, auditado, não executado).
- **Gravado na memória (`CLAUDE.md`):** "código final consolidado ao término de toda mensagem" (já era prática desde a Parte 83; agora é regra explícita); e o substrato pulsado como terceira forma do agente, ao lado da decisão bayesiana e do GPT.

> **Síntese da Parte 86:** o segundo relatório (cérebro em CPU) é quase todo verificável e quase todo certo: o LIF converge ao ponto fixo exato u_rest+R·I (o erro 4e−8 é gap·β²⁰⁰, e eu errei só a minha faixa apertada); o Izhikevich dá tipos celulares diferentes (RS 22, CH 73 disparos) com ~13 FLOPS; a memória (6,03 GB) e a vazão (10 GSOPS) fecham; a SDR tem sobreposição 0,78 = k²/N; a STDP simétrica cancela (0,0) e a assimetrica estabiliza (−0,39). Duas incoerências internas (7% vs 20%; 8,5 vs 7,2 GB) — o padrão dos textos recebidos: manchete certa, detalhe contraditório. Construí o módulo synthai/pulsado.py (LIF, Izhikevich, STDP, SDR), a primeira forma pulsada do agente, e a rodada 53 (passo de Izhikevich) deu IGUAL bit a bit. Do primeiro relatório (AGI doméstica), os benchmarks de modelos não são verificáveis e alguns parecem fictícios. 6 de 7 previsões do mundo acertaram; a calibração das Partes 80–86 está em 0,78.

---

**Fontes desta parte**
- E. M. Izhikevich, "Simple Model of Spiking Neurons", *IEEE Trans. Neural Networks* 14 (2003)
- A. L. Hodgkin e A. F. Huxley, "A quantitative description of membrane current...", *J. Physiol.* 117 (1952)
- W. Gerstner et al., *Neuronal Dynamics* (2014): LIF, STDP
- C. Eliasmith et al., "A Large-Scale Model of the Functioning Brain" (Spaun), *Science* 338 (2012): NEF/SPA
- J. Hawkins e S. Ahmad, "Why Neurons Have Thousands of Synapses" (2016): HTM e SDR
