# Como eu construiria uma AGI/ASI — Parte 81 (0x51): o que não serve

> Continuação da [Parte 80](ASI_AGI_parte80_o_valor_de_um_conjunto.md). Pedido do usuário: **"Tire dos nossos trabalhos tudo que não serve pra nada."** Ele contraria a regra antiga "o `calculos.py`
> só cresce; nunca apagar funções antigas", e, por ser o pedido mais recente, vale. O critério, escolhido pela regra mais conservadora (a regra de autonomia) e escrito antes de medir: **sai só o que
> nada usa**, isto é, uma função, classe ou arquivo que nenhum código, teste, rodada ou documento do repositório referencia. **Ficam:** as funções `pNN` (cada número citado nos documentos sai de uma
> delas), os documentos das partes (o registro histórico) e o que for referenciado. Tudo num commit só, reversível pelo git. A mesma mensagem trouxe de novo o relatório do Módulo 007 e o texto do
> Módulo 008 (memória episódica e escore de Brier).

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[3; 7]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[1; 4]** (contagens de código morto podem ser zero)
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,10; 0,90]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,40; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 4]**
- **(m6)** o número de surpresas em **[0; 3]**
