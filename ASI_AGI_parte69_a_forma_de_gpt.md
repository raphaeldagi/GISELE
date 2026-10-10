# Como eu construiria uma AGI/ASI — Parte 69 (0x45): a forma de GPT

> Continuação da [Parte 68](ASI_AGI_parte68_o_tipo_da_quantidade.md). Pedido do usuário, gravado no `CLAUDE.md`: **"Grave na memória que nossa AGI ASI PÓS ASI AGI terá a forma de
> GPT."** Esta parte constrói a forma: um GPT (Generative Pre-trained Transformer) mínimo em Python puro (`synthai/gpt.py`): embeddings de caractere e de posição, atenção causal
> de uma cabeça, resíduo, MLP, softmax do próximo caractere, gradiente escrito à mão (conferido por diferenças finitas: maior erro relativo 2,3·10⁻⁶) e Adam. Pré-treinado nas
> definições do WordNet, medido contra o modelo mais simples (o n-grama), e com a decisão do próximo caractere traduzida bit a bit para Java (rodada 43).

## Previsões sobre as minhas previsões desta parte (prever o previsto; registradas antes de escrever qualquer previsão do mundo desta parte)

Planejado, antes de escrever: bits por caractere do n-grama (ordens 3 e 5) e do GPT nas definições inglesas; a diferença GPT − n-grama; bits por dígito de π em hexadecimal; a
rodada 43 (IGUAIS, e quantos próximos caracteres o GPT pequeno acerta numa frase). Acerto do mundo nas Partes 53 a 68, pela régua nova (`p1481`): **72,5%** (109 previsões);
com ~7 previsões, a faixa binomial de 90% vai de 4/7 a 7/7.
- **(m1)** o número de previsões do mundo em **[6; 9]**.
- **(m2)** o número de faixas que cruzam o zero em **[0; 2]** (a diferença GPT − n-grama pode cruzar).
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,30]** (bits por caractere são quantidades longe de zero com escala conhecida, e as minhas faixas para
  elas devem ser estreitas).
- **(m4)** a fração de acertos do mundo em **[0,57; 1,00]**.
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 1]**.
