# Como eu construiria uma AGI/ASI — Parte 87 (0x57): compressão, plasticidade e GRPO

> Continuação da [Parte 86](ASI_AGI_parte86_o_cerebro_na_cpu.md). Pedido do usuário: um relatório sobre "Otimização Holística em ML/DL/CL/RL" — compressão (poda, quantização, destilação) e o pipeline
> co-compressivo; aprendizado contínuo e a perda de plasticidade (norma dos pesos, posto efetivo, neurônios dormentes; Shrink&Perturb, ReDo); e a transição PPO → GRPO (livre de crítico, vantagem
> normalizada por grupo, 2-GRPO). Parte de auditoria, como as 72–86: os textos são dados; cada afirmação testável vira conta, reimplementada na biblioteca padrão.
>
> Este relatório encaixa na história do projeto: a Parte 34 já mediu esquecimento catastrófico (só quando as tarefas conflitam) e Naive Bayes vs SGD; a Parte 86 trouxe o substrato pulsado. Aqui testo a
> aritmética da quantização, a álgebra da vantagem do GRPO, e simulo a perda de plasticidade e a sua mitigação.

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[4; 8]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,80]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** o número de surpresas em **[0; 3]**
