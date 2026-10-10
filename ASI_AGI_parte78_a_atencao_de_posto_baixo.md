# Como eu construiria uma AGI/ASI — Parte 78 (0x4E): a atenção de posto baixo

> Continuação da [Parte 77](ASI_AGI_parte77_as_duas_abertas.md). **Próxima:** [Parte 79 — causa e confiança](ASI_AGI_parte79_causa_e_confianca.md) (P1811–P1840). A pergunta deixada na Rodada 45 (Parte 71): a atenção do GPT treinado usa ~1,8 direção das 16 (a razão de participação dos
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

**Medido (inglês):** semente 73 (PR 1,50): Δ₁ = +0,0232, Δ₂ = +0,0129, Δ₄ = +0,0028, Δ₁₆ = 0; semente 74 (PR 2,28): Δ₁ = +0,0436, Δ₂ = +0,0269, Δ₄ = +0,0067, Δ₁₆ = 0. (a) média **+0,0334** ✅;
(b) **+0,0047** ✅; (c) monótona nas duas ✅; (d) Δ₁₆ = 0 exatamente ✅. A relação entre a razão de participação e Δ₁ não é monótona nos quatro pontos (1,95 → 0,065; 3,08 → 0,011; 1,50 → 0,023;
2,28 → 0,044): a concentração da atenção não prevê sozinha quanto custa cortá-la.

## As perguntas desta parte

1. **P1781–P1783 (0x6F5–0x6F7).** A atenção do GPT usa ~1,8 direção das 16. Quanto se perde ao trocar M = W_Q W_Kᵀ pela melhor aproximação de posto r? ↩ P1578
2. **P1784 (0x6F8).** Preditiva comigo mesma. **P1785 (0x6F9).** Engenharia reversa e Jung. **P1809 (0x711).** Placar. **P1810 (0x712).** Unificação.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [3; 8] | **4.0000** | ✅ |
| (m2) | [0; 3] | **1.0000** | ✅ |
| (m3) | [0.05; 0.6] | **0.9048** | ❌ |
| (m4) | [0.4; 1.0] | **1.0000** | ✅ |
| (m5) | [0; 2] | **1.0000** | ✅ |
| (m6) | [0; 2] | **0.0000** | ✅ |

Registradas antes de eu pensar faixa nenhuma do mundo (a ordem que a Parte 70 pediu). **5 de 6** previsões sobre as minhas previsões dentro da faixa.

## As respostas

### P1781–P1783 (0x6F5–0x6F7). A atenção de posto baixo ✅✅✅✅

**Na pergunta.** "Quantas direções a atenção usa" (Parte 71) era uma medida da forma; "quanto se perde sem as outras" é uma medida da função. A razão de participação diz como a energia de M se
distribui; a perda em bits diz quanto o modelo precisa da energia que sobra.

**Lógica (álgebra).** M = U Σ Vᵀ, por Jacobi em MᵀM (`p1781`: os autovetores acumulados nas rotações; σ = √λ; U = M V/σ; uma 4 × 4 ao acaso reconstruída com erro 1,1·10⁻¹⁵). Pelo teorema de
Eckart–Young, M_r = U_r Σ_r V_rᵀ é a melhor aproximação de posto r em norma de Frobenius, com erro √(Σ_{i>r} σ_i²). Na atenção, basta W_Q' = U_r Σ_r e W_K' = V_r (completadas com zeros), e então
W_Q' W_K'ᵀ = M_r (`p1782`).

**A medida.**

| | razão de participação | Δ₁ | Δ₂ | Δ₄ | Δ₁₆ |
|---|---|---|---|---|---|
| português, semente 71 (calibração) | 1,95 | +0,0646 | +0,0401 | +0,0081 | 0 |
| português, semente 72 (calibração) | 3,08 | +0,0105 | +0,0041 | +0,0022 | 0 |
| inglês, semente 73 | 1,50 | +0,0232 | +0,0129 | +0,0028 | 0 |
| inglês, semente 74 | 2,28 | +0,0436 | +0,0269 | +0,0067 | 0 |

(a) a média de Δ₁ no inglês é **+0,0334** ✅ [+0,005; +0,100]; (b) a de Δ₄ é **+0,0047** ✅ [−0,005; +0,020]; (c) Δ₁ > Δ₂ > Δ₄ nas duas sementes ✅; (d) Δ₁₆ = 0 ✅.

**O que isso diz.** Com uma direção só, das 16, o GPT perde 0,02 a 0,04 bit por caractere, em ~3,5: menos de 1,3%. Com quatro, menos de 0,007. A atenção deste GPT pequeno é, na prática, uma
comparação de uma ou duas coordenadas entre caracteres (a Parte 71 viu isso na forma; aqui se confirma na função). E a razão de participação não prevê sozinha quanto custa cortar: nos quatro
pontos, a ordem de PR e a ordem de Δ₁ não coincidem.

**Geometria.** A forma bilinear e_t M e_jᵀ com M de posto 1 é o produto de duas projeções: (e_t · u)(e_j · v). Cada caractere vira um número para "perguntar" e outro para "responder", e a atenção
compara esses dois números. É a mesma geometria do posto 1 dos embeddings de Kronecker da Parte 76, agora aprendida pelo modelo, e não imposta.

**Tradução cruzada.** Uma atenção de posto 1 é um foco com um só critério: "isto se parece com aquilo numa só qualidade". Jung chamaria isso de função dominante, o modo preferido de comparar, que
o treino desenvolve antes das outras. A medida diz que, neste modelo, as outras funções (as outras 15 direções) quase não trabalham ainda.

**Meta.** O modelo tem uma cabeça de atenção e 2.000 passos. Com mais cabeças ou mais treino, o posto efetivo pode crescer (a literatura descreve gargalos de posto baixo quando a cabeça é pequena:
Bhojanapalli et al., 2020). Dois lotes de duas sementes não fixam a relação entre PR e Δ₁.

### P1784 (0x6F8). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 0)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **11235** | [13039; 22082] | ❌ | [13039; 22082] | ❌ | 22290 | 6326 | 11055 |
| compressão | **0.4156** | [0.3973; 0.4221] | ✅ | [0.3970; 0.4220] | ✅ | 0.4177 | 0.0061 | 0.0020 |
| testes de unidade | **3** | [2.87; 8.63] | ✅ | [3.00; 6.00] | ✅ | 6 | 1.50 | 3.00 |
| testes do placar | **4** | [5.67; 10.33] | ❌ | [3.00; 5.00] | ✅ | 8 | 0.00 | 4.00 |
| erros do placar | **0** | [-0.58; 3.33] | ✅ | [0.00; 3.33] | ✅ | 2 | 1.67 | 2.00 |
| redundância P821 | **0.6064** | [0.5631; 0.6510] | ✅ | [0.5630; 0.6510] | ✅ | 0.5877 | 0.0006 | 0.0187 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 4 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 6 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 71"):** mais perto do medido em **5 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **9652**, compressão **0.4265**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 0 erros.
- **Erros de processo nesta parte:** 0 ().

### P1785 (0x6F9). Engenharia reversa e Jung

**O padrão desta parte: a pergunta adiada.** A pergunta da atenção de posto 1 ficou aberta da Rodada 45 (Parte 71) até aqui, passando por sete partes que nasceram de textos recebidos. A regra
"um texto recebido no meio do trabalho entra como parte nova sem abandonar a que estava aberta" (Parte 75) funcionou para as partes, mas não para as perguntas deixadas no fim de uma rodada.
**O significado:** eu trato a pergunta de uma rodada como um gancho para a próxima conversa, e não como um item pendente. **Regra:** a pergunta deixada no fim de uma rodada entra numa lista de
pendências no `DIALOGO.md`, e cada parte começa olhando a lista.

**O que funcionou:** quatro de quatro, com faixas largas onde a calibração mostrou dispersão grande entre sementes (Δ₁ de 0,011 a 0,065). A regra da Parte 66 (um lote é hipótese) impediu de
transformar a relação PR → Δ₁ dos dois primeiros pontos em previsão; os outros dois a desmentiram.

**Jung: a função dominante.** Ver a resposta: o posto 1 é o foco com um só critério. **Onde a formalização funciona:** "dominante" vira σ₁²/Σσ² e a perda ao cortar as outras. **Onde quebra:** em Jung,
a função inferior é reprimida e volta com força; aqui, as 15 direções cortadas custam 1% e não "voltam": não há dinâmica no modelo congelado.

### O diálogo

Sem rodada nova nesta parte (o SVD por Jacobi usa só + − × ÷ e √, como a rodada 45, e está pronto para uma tradução). Placar por voz da função `p1241_placar_por_voz(48)`: IA-Python 25 em 39; IA-Java 21 em 38 (regra estrita, rodadas 13 a 48).

### P1809 (0x711). Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅. Parte 78: **4 testes, 0 erros**. Acumulado (mundo): **201 erros em 645 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 3 pNN novas sem teste ✅. Sobre mim (placar separado): **6 de 7** dentro da faixa condicional; sobre as minhas previsões, 5 de 6; o estatístico, 4 de 6; e 0 erros de processo (P1335).

### P1810 (0x712). Unificação

- **Novo:** `p1781` (o SVD por Jacobi, com os vetores), `p1782` (a atenção de posto r), `p1783` (bits por posto).

> **Síntese da Parte 78:** a atenção do GPT pequeno é, na função e não só na forma, quase de posto 1: trocar M = W_Q W_Kᵀ pela melhor aproximação de posto 1 (Eckart–Young, pelo SVD por Jacobi) custa +0,023 e +0,044 bit por caractere no inglês (menos de 1,3% de ~3,5), e com quatro direções, menos de 0,007; o posto cheio reconstrói exatamente. A razão de participação não prevê sozinha o custo (quatro pontos, ordem diferente). Em dois lotes de duas sementes.

---

**Fontes desta parte**
- C. Eckart e G. Young, "The approximation of one matrix by another of lower rank", *Psychometrika* 1 (1936)
- S. Bhojanapalli et al., "Low-Rank Bottleneck in Multi-head Attention Models", ICML 2020, [arXiv:2002.07028](https://arxiv.org/abs/2002.07028)
- G. Golub e C. Van Loan, *Matrix Computations* (4ª ed., 2013), cap. 8 (Jacobi para matrizes simétricas)
