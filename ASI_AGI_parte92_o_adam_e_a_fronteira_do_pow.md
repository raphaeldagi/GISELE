# Como eu construiria uma AGI/ASI — Parte 92 (0x5C): o Adam e a fronteira do pow

> Continuação da [Parte 91](ASI_AGI_parte91_o_gpt_que_aprende_igual.md). Pedido do usuário: **"Continue. Rode em segundo plano também em loop infinito."** Mantenho o loop (cada parte agenda a próxima e deixa
> trabalho rodando). A pergunta mais funda (↩ rodada 58): a Parte 91 traduziu o passo de treino com SGD bit a bit; o otimizador real do GPT (Parte 69) é o **Adam**, que usa `b₁ᵗ` e `b₂ᵗ` na correção de viés
> (a função `pow`) e `√v̂` no passo. O `pow` é uma das funções que o IEEE 754 NÃO obriga a arredondar corretamente (a fronteira da Parte 52). A pergunta: o passo de Adam sai igual bit a bit entre Python e Java,
> ou o `pow` precisa de uma implementação própria, como o exp/log precisaram?
>
> **A âncora (Parte 52).** O expoente de `b₁ᵗ` é um INTEIRO (o número do passo). `pow(x, n)` com n inteiro pode ser computado por multiplicação repetida (exato no sentido de "mesma sequência de ×"), ou pela
> `pow` da libm (que trata o expoente como real e passa por exp(n·ln x) — a fronteira). Se Python (`x**n`) e Java (`Math.pow`) escolherem caminhos diferentes, diferem; a correção é um `pow` inteiro próprio.

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[3; 7]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,80]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** o número de surpresas em **[0; 3]**
