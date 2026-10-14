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
