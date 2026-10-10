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

## Previsões do mundo (registradas depois das (m) e das sobre mim, antes de medir)

**O ganho de informação (P1661).** No mundo da P1632 (semente 73), observar o estado reduz a entropia em H(p) bits, qualquer que seja a utilidade. Escolher pelo "ganho esperado de
informação" é escolher por H(p). **A conta:** H depende só de p, e p é independente da dominância; então os 200 de maior H têm VOI = 0 com chance 1/2 (desvio 0,0354).
- **(a)** a fração com VOI = 0 entre os 200 de maior ganho de informação em **[0,442; 0,558]**
- **Calibração (sementes 730 a 733, regra escrita antes: as quatro seguintes à 73 × 10):** a razão entre o VOI médio dos 200 de maior H e o dos 200 de maior VOI deu 0,277, 0,326, 0,290 e 0,283.
  A faixa de previsão de 90% para um lote novo é a média ± t₃ · desvio · √(1 + 1/4), com t₃ = 2,353.
- **(b)** essa razão na semente 73 em **[0,236; 0,352]**

**O orçamento (P1662).** A U(a) = E[ΔK | a]/Custo(a) do texto: 300 instâncias, 30 experimentos cada, custos inteiros em 1..20, orçamento de 20% do custo total; valor = VOI. O ótimo é exato (mochila
0-1 por programação dinâmica). **Calibração (sementes 740 a 743, mesma geometria do teste):** guloso por VOI/custo = 0,9924, 0,9928, 0,9925, 0,9938 do ótimo; guloso por H/custo = 0,581, 0,555, 0,565,
0,561; o guloso por VOI foi ótimo em 0,627, 0,667, 0,657, 0,640 das instâncias. Faixas pela mesma regra (t₃ = 2,353). Teste: semente 74.
- **(c)** guloso por VOI/custo, em fração do ótimo, em **[0,9912; 0,9946]**
- **(d)** guloso por ganho de informação/custo, em fração do ótimo (em VOI), em **[0,5364; 0,5943]**
- **(e)** a fração de instâncias em que o guloso por VOI é ótimo em **[0,6009; 0,6941]**

**Medido (a) a (e):** (a) **0,510** ✅; (b) **0,251** ✅ (0,0426/0,1696); (c) **0,9922** ✅; (d) **0,568** ✅; (e) **0,573** ❌ (0,028 abaixo do piso; não é surpresa).

**Previsão nova, nascida de (e), registrada antes de rodar.** A faixa de (e) usou o desvio de 4 lotes de calibração (0,0177), e uma fração em 300 instâncias tem um desvio binomial conhecido,
√(p(1 − p)/300) ≈ 0,028: havia uma conta melhor que a estimativa de 4 amostras. Com os 5 lotes (os 4 de calibração e o do teste), p = 0,6327, desvio 0,0278, e a faixa de 90% para um lote novo
é p ± 1,645 · 0,0278 · √(1 + 1/5).
- **(f)** a fração de instâncias em que o guloso por VOI é ótimo, semente 75, em **[0,5825; 0,6828]**

**Medido (f):** **0,620** ✅ (e (c), (d) replicaram: 0,9924 e 0,568).

**A Rodada 48, registrada antes de rodar:** o Python grava as 300 instâncias da semente 74 (valores em hexadecimal, custos inteiros); Java e Python calculam o ótimo da mochila por programação
dinâmica e os dois gulosos (ordenação por razão, empates pelo índice). Só + e comparações sobre os valores, e divisões para as razões: tudo arredondado corretamente pelo IEEE 754.
- **(g)** IGUAIS (categórica)
