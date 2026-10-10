# Como eu construiria uma AGI/ASI — Parte 74 (0x4A): o que vale testar

> Continuação da [Parte 73](ASI_AGI_parte73_o_que_refuta.md). Nasce do quarto texto recebido do usuário (`externos/texto_recebido_parte74.md`): os Módulos 004 a 007 de outra conversa, sem código,
> com resultados declarados ("8/8 testes"; "corrigi a expectativa: o histórico tinha quatro eventos, não cinco") e duas propostas para escolher o próximo experimento: U(a) = E[ΔK | a]/Custo(a)
> e o "ganho esperado de informação".

## Previsões sobre as minhas previsões desta parte (registradas antes de pensar qualquer faixa do mundo)

- **(m1)** o número de previsões do mundo em **[4; 9]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 2]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,03; 0,40]**
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** o número de surpresas em **[0; 2]**

## Previsões sobre mim (placar separado), antes de escrever

Planejadas: ~5 previsões do mundo e ~4 funções novas. E = erros do mundo, S = surpresas, contados pelo script.

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,397; 0,422]** | o estatístico |
| testes de unidade | **[4 + S; 7 + S]** | 4 funções, uma por teste |
| testes do placar | **5 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |
