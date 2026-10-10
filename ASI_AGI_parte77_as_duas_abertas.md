# Como eu construiria uma AGI/ASI — Parte 77 (0x4D): as duas abertas

> Continuação da [Parte 76](ASI_AGI_parte76_a_forma_do_byte.md). Fecha os dois itens que a auditoria das duas linguagens (`p1722`) deixou abertos: as rodadas 09 e 14, em que o Java usa o log da
> biblioteca e o Python o usa dentro de peças medidas (`synthai/decisao.py` e a `p732`). Pedido permanente: "Continue sem parar."

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[2; 6]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 2]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,00; 0,40]** (previsões de igualdade têm w = 0)
- **(m4)** a fração de acertos do mundo em **[0,40; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 1]**
- **(m6)** o número de surpresas em **[0; 2]**

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,397; 0,422]** | o estatístico |
| testes de unidade | **[2 + S; 5 + S]** | ~2 funções novas |
| testes do placar | **5 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de mexer nas rodadas)

**Rodada 14.** O Python passa a calcular os pesos dentro da rodada (a mesma conta da `p732`, que fica intacta), com o `log_` de `dialogo/exatas.py`; o Java troca `Math.log` pelo mesmo `log_`.
- **(a)** IGUAIS (categórica)
- **(b)** as duas listas de 12 trigramas impressas ficam **iguais** às da versão com a biblioteca (a ordem sai de comparações de pesos; um ulp só troca a ordem se dois pesos estiverem a menos de um
  ulp um do outro: a regra da Parte 55) (categórica)

**Rodada 09.** Duas fronteiras: o log e o exp da biblioteca, e o `sum()` compensado do Python 3.12 (a regra da Parte 34) dentro da `ThompsonMistura`. O Python passa a usar uma cópia exata das duas
classes dentro da rodada (laços de soma simples, `exp_` e `log_`), e o `synthai/decisao.py` fica intacto; o Java troca `Math.exp` e `Math.log`.
- **(c)** IGUAIS (categórica)
- **(d)** a maior diferença relativa entre os números impressos pela versão nova e pela antiga do Python em **[0; 1·10⁻¹²]** (as duas diferem só por ulps de log, exp e da compensação da soma)

**A auditoria.**
- **(e)** depois das duas, a `p1722` lista só a 48 (só na preparação) (categórica)
