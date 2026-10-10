# Como eu construiria uma AGI/ASI — Parte 78 (0x4E): a atenção de posto baixo

> Continuação da [Parte 77](ASI_AGI_parte77_as_duas_abertas.md). A pergunta deixada na Rodada 45 (Parte 71): a atenção do GPT treinado usa ~1,8 direção das 16 (a razão de participação dos
> valores singulares de M = W_Q W_Kᵀ); quanto se perde, em bits por caractere, quando M é trocada pela sua melhor aproximação de posto r (a soma truncada da decomposição em valores singulares)?
> Pedido permanente: "Continue sem parar."

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[3; 8]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]** (uma perda de bits pode ser quase zero)
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,60]**, ou indefinida se não houver nenhuma (a regra da Parte 77)
- **(m4)** a fração de acertos do mundo em **[0,40; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** o número de surpresas em **[0; 2]**
