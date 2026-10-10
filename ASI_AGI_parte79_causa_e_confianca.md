# Como eu construiria uma AGI/ASI — Parte 79 (0x4F): causa e confiança

> Continuação da [Parte 78](ASI_AGI_parte78_a_atencao_de_posto_baixo.md). Nasce do texto recebido do usuário sobre o Módulo 009 (`externos/texto_recebido_parte79.md`): correlação, previsão e
> causalidade, com o diagrama Z → X, Z → Y, X → Y; e a prévia do Módulo 010 (confiança declarada contra precisão observada). Pedido permanente: "Continue sem parar."

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[3; 8]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 2]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,005; 0,30]** (faixas de conta fechada, estreitas)
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 1]**
- **(m6)** o número de surpresas em **[0; 2]**

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,397; 0,422]** | o estatístico |
| testes de unidade | **[2 + S; 5 + S]** | ~2 funções novas |
| testes do placar | **4 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de simular)

**O diagrama do texto, com números.** Z ~ N(0, 1); X = Z + ε_X; Y = 0,5·X + 1·Z + ε_Y (os ε normais padrão, independentes); n = 20.000, semente 79. O efeito causal de X sobre Y é 0,5.
**A conta, com a substituição:** Var X = 1² + 1 = 2; Cov(X, Z) = 1; Cov(X, Y) = 0,5·2 + 1·1 = 2; a inclinação ingênua de Y em X é 2/2 = **1,0** (o dobro do efeito: o viés é γ·Cov(X, Z)/Var X =
1·1/2 = 0,5). Var Y = 0,25·2 + 1 + 2·0,5·1·1 + 1 = 3,5; o resíduo da regressão ingênua tem variância 3,5 − 1,0²·2 = 1,5, e o desvio da inclinação é √(1,5/(20.000·2)) = 0,00612. A regressão em
X e Z (o ajuste pela porta dos fundos de Pearl) tem desvio √(1/(20.000·Var(X | Z))) = √(1/20.000) = 0,00707. A intervenção (X sorteado com a mesma variância, sem depender de Z) tem resíduo
γ² + 1 = 2 e desvio √(2/(20.000·2)) = 0,00707. Faixas de 90% (± 1,645 desvios):
- **(a)** a inclinação ingênua (correlação) em **[0,9899; 1,0101]**
- **(b)** a inclinação ajustada por Z em **[0,4884; 0,5116]**
- **(c)** a inclinação sob intervenção (do(X)) em **[0,4884; 0,5116]**

**A prévia do Módulo 010: a minha própria calibração.** O texto pede "confiança declarada contra precisão observada". As minhas faixas são, em sua maioria, faixas de 90%. A régua `p1481` lê todas as
previsões do mundo das Partes 53 a 78:
- **(d)** a fração de acertos em **[0,70; 0,80]** (era 0,748 nas Partes 53 a 71): abaixo dos 90% declarados, isto é, **excesso de confiança**
