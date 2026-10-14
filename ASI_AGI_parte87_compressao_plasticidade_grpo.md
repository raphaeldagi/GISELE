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

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,392; 0,420]** | o estatístico |
| testes de unidade | **[4 + S; 9 + S]** | um módulo novo (plasticidade) + auditorias |
| testes do placar | **7 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

Reimplemento as peças testáveis (biblioteca padrão; texto em `externos/`). Contas fechadas não levam o fator 1,36; a simulação de plasticidade leva.

- **(a)** o erro de quantização uniforme Q(x) = round(x/s) + z: a MSE ∝ passo² ∝ 4⁻ᵇ, então a razão MSE(INT4)/MSE(INT8) = 4⁽⁸⁻⁴⁾ = **256**; o simulado (gaussiana, 100.000 amostras, semente 87) em
  **[205; 310]** (center 256, dispersão de amostragem)
- **(b)** a vantagem normalizada do GRPO Âᵢ = (rᵢ − média)/(desvio): a média das vantagens de um grupo é **0** para qualquer G (exato); e com G = 2 e recompensas distintas, as duas vantagens são
  exatamente **+1 e −1** (o sinal contrastivo puro) — categórico
- **(c)** a perda de plasticidade (posto): numa MLP de 1 camada oculta (d_in = 10, d_oculta = 20) treinada por SGD em 20 tarefas aleatórias seguidas, o posto estável das ativações ocultas na tarefa 20
  dividido pelo da tarefa 1 é **< 1** (colapso); razão em **[0,30; 0,95]**, e o Shrink&Perturb dá uma razão MAIOR que o SGD puro (mantém mais posto)
- **(d)** a norma dos pesos: no mesmo experimento, ‖W‖ cresce no SGD puro (razão tarefa 20 / tarefa 1 > 1), e o Shrink&Perturb a mantém mais contida (razão do S&P < razão do SGD); predigo a razão do SGD
  puro em **[1,0; 3,0]** e a do S&P abaixo dela
- **(e)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80–87 em **[0,74; 0,88]**

Do relatório, a ordem do pipeline co-compressivo (poda → QAT → destilação) e as leis de escala da plasticidade não são testáveis aqui sem treinar redes grandes; registro e não pontuo.
