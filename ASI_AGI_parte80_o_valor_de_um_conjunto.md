# Como eu construiria uma AGI/ASI — Parte 80 (0x50): o valor de um conjunto

> Continuação da [Parte 79](ASI_AGI_parte79_causa_e_confianca.md). A primeira pendência de `dialogo/PENDENCIAS.md` (Parte 74): quando os experimentos dependem uns dos outros, o valor de um
> conjunto não é a soma dos valores. Quanto vale um conjunto de perguntas, e o guloso ainda chega perto do ótimo? Primeira parte com a regra do fator 1,36 (Parte 79) nas faixas sem conta fechada.

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[3; 8]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,70]** (as faixas alargadas por 1,36 ficam mais largas que as das partes anteriores)
- **(m4)** a fração de acertos do mundo em **[0,50; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** o número de surpresas em **[0; 2]**

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,397; 0,422]** | o estatístico |
| testes de unidade | **[2 + S; 5 + S]** | 2 funções novas |
| testes do placar | **5 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de rodar a semente 80)

**O mundo.** 300 instâncias: estado binário com prior p ~ U(0, 1), duas ações com utilidades U(0, 1), seis sensores com acurácia U(0,55; 0,95), condicionalmente independentes dado o estado,
custos inteiros em 1..5, orçamento 6. O VOI exato de um conjunto (`p1841`: as 2^|conjunto| respostas); o ótimo pela enumeração dos 64 subconjuntos; o guloso pelo ganho marginal de VOI por custo.
**Calibração (sementes 800 a 803, regra escrita antes: as quatro seguintes a 80 × 10; mesma geometria).** Achou primeiro um defeito meu: ótimos de 10⁻¹⁷ (um VOI zero com ruído de ponto
flutuante) contavam como positivos, e a razão guloso/ótimo virava 0. Corrigido (ótimo ≤ 10⁻¹² é zero) antes de qualquer registro. Depois: guloso/ótimo 0,8835, 0,8931, 0,9022, 0,8808; guloso ótimo
em 0,8167, 0,8267, 0,8267, 0,7967; complementaridade em 0,3633, 0,3667, 0,3833, 0,3233; guloso parado em zero com ótimo positivo em 0,11, 0,10, 0,09, 0,11.
**As faixas.** A média de razões não tem forma fechada: média ± t₃ · desvio · √(1 + 1/4), **alargada por 1,36** (a regra da Parte 79). As frações têm desvio binomial: p ± 1,645 · √(p(1 − p)/300) ·
√(1 + 300/1.200), sem o fator (a variância é conhecida).
- **(a)** a média de guloso/ótimo em **[0,8549; 0,9249]**
- **(b)** a fração de instâncias com o guloso ótimo em **[0,7756; 0,8578]**
- **(c)** a fração com algum par complementar (o VOI não submodular) em **[0,3082; 0,4101]**
- **(d)** a fração em que o guloso para em zero com o ótimo positivo em **[0,0703; 0,1347]**

**Medido (a) a (d), semente 80:** guloso/ótimo **0,8821** ✅; guloso ótimo em **0,7933** ✅; complementaridade em **0,4033** ✅; parado em zero com ótimo positivo em **0,1100** ✅.

**Previsão nova: o remédio, registrado antes de rodar a semente 80.** Quando nenhum sensor sozinho tem ganho, o guloso com dois passos à frente (`olhar = 2`) tenta o melhor par antes de parar.
**Calibração (sementes 800 a 803):** guloso/ótimo 0,9709, 0,9752, 0,9846, 0,9665; ótimo em 0,9133, 0,9133, 0,9233, 0,8933; parado em zero em 0,0233, 0,0167, 0,0067, 0,0233. Faixas pelas mesmas regras
(a razão: t₃ e ×1,36, cortada em 1, que é o máximo possível; as frações: binomial).
- **(e)** a média de guloso/ótimo com `olhar = 2` em **[0,9466; 1,0000]**
- **(f)** a fração com o guloso ótimo em **[0,8805; 0,9411]**
- **(g)** a fração parada em zero com o ótimo positivo em **[0,0036; 0,0314]**

**Medido (e) a (g):** **0,9771** ✅; **0,9100** ✅; **0,0167** ✅.

**A Rodada 49, registrada antes de rodar:** o Python grava as 300 instâncias da semente 80 (p, utilidades e acurácias em hexadecimal, custos inteiros); Python e Java calculam o VOI de cada conjunto
pela mesma enumeração, o ótimo e os dois gulosos (olhar 1 e 2, com os mesmos desempates), só com + − × ÷ e comparações.
- **(h)** IGUAIS (categórica)
