# Como eu construiria uma AGI/ASI — Parte 76 (0x4C): a forma do byte

> Continuação da [Parte 75](ASI_AGI_parte75_o_que_se_prova.md). A Parte 75 deixou uma pergunta medível, tirada do texto recebido: o embedding de um caractere como o produto de Kronecker de
> dois fatores, um para cada nibble do byte (W₁[b ≫ 4] ⊗ W₂[b & 0x0F]), serve para a forma de GPT deste projeto? Pedido do usuário, gravado no `CLAUDE.md`: **"Continue sem parar."**

## Previsões sobre as minhas previsões desta parte (num commit só delas, antes de pensar qualquer faixa)

- **(m1)** o número de previsões do mundo em **[3; 8]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]** (uma diferença de bits entre dois modelos pode ter qualquer sinal)
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,02; 0,40]**
- **(m4)** a fração de acertos do mundo em **[0,40; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** o número de surpresas em **[0; 2]**

## Previsões sobre mim (placar separado), antes de escrever

Planejadas: ~4 previsões do mundo, ~3 funções novas e um módulo novo no pacote (`synthai/gpt_kronecker.py`).

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,397; 0,422]** | o estatístico |
| testes de unidade | **[4 + S; 7 + S]** | 3 funções e o módulo |
| testes do placar | **4 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |
