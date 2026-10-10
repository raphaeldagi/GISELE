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

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,397; 0,422]** | o estatístico |
| testes de unidade | **[3 + S; 6 + S]** | 3 funções novas |
| testes do placar | **4 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir no inglês)

**O teste.** Um GPT (d = 16, T = 16, h = 32, 2.000 passos) treinado nas glosas inglesas, sementes 73 e 74; M = W_Q W_Kᵀ decomposta por Jacobi (`p1781`; reconstrói uma 4 × 4 ao acaso com erro
1,1·10⁻¹⁵), e a atenção trocada pela aproximação de posto r (Eckart–Young: a melhor de posto r em norma de Frobenius). Δ_r = bits(posto r) − bits(original), no teste (300 janelas).
**Calibração, pela regra escrita antes (o português, sementes 71 e 72):** Δ₁ = +0,0646 e +0,0105; Δ₂ = +0,0401 e +0,0041; Δ₄ = +0,0081 e +0,0022; Δ₁₆ = 0,0000 nas duas. A razão de participação foi
1,95 e 3,08: quanto mais concentrada a atenção, mais perde o posto 1? A calibração tem dois pontos e não fixa esse sinal (a regra da Parte 64).
- **(a)** a média de Δ₁ nas duas sementes do inglês em **[+0,005; +0,100]** bit
- **(b)** a média de Δ₄ em **[−0,005; +0,020]** bit
- **(c)** Δ₁ > Δ₂ > Δ₄ nas **duas** sementes (categórica: mais direções, menos perda)
- **(d)** |Δ₁₆| < 10⁻⁶ nas duas (categórica: o posto cheio reconstrói M a menos de arredondamento)
