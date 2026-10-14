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
