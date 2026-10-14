# Como eu construiria uma AGI/ASI — Parte 95 (0x5F): o relatório "v2.0" e o que ele promete

> Continuação da [Parte 94](ASI_AGI_parte94_o_mundo_que_nao_e_linear.md). Chegou no meio do ciclo um **relatório recebido** ("SYNTHAI v2.0") com quatro mecanismos e uma tabela de benchmarks espetaculares. Regra da Parte 72/85/88: **não
> executo o código recebido**; audito pela árvore sintática (AST), reimplemento as IDEIAS do zero em biblioteca padrão (`synthai/evoluido.py`), meço o que o relatório **afirma sobre mecanismo** (verificável) e **não pontuo** os benchmarks
> que não posso checar (regra da Parte 86). A auditoria confiável compara o texto com o SEU PRÓPRIO comportamento, não com uma verdade externa.
>
> **Auditoria de capacidade (AST, sem executar).** O código recebido importa só `math` e `random`: sem rede, sem `subprocess`, sem `eval`/`exec`. Seguro nesse eixo (ao contrário do pacote da Parte 93) — mas isso não valida as afirmações.
>
> **A pergunta mais funda (↩ P2232, P131).** As quatro peças (TTTS, P*, EWC, quantização) são conhecidas da literatura. A pergunta não é se existem; é se o relatório diz a verdade sobre **o que cada uma faz** — e, em particular, se a frase
> "o limiar P* fica mais estrito quando o ruído cresce" bate com a fórmula P* = c/((1−ε)L) que o próprio relatório dá.

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[4; 8]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,80]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** o número de surpresas em **[0; 3]**

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[12.000; 23.000]** | o estatístico (parte de auditoria tende a ser maior) |
| testes de unidade | **[6 + S; 10 + S]** | TTTS, P*, EWC, quantização, rodada 62, auditoria (S = surpresas) |
| previsões unilaterais | **[0; 1]** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

- **(a)** **a direção de P\* contradiz o relatório** (p2291): como P* = c/((1−ε)·L) e (1−ε) decresce com ε, P* **cresce** com ε — logo P*(ε=0,45) > P*(ε=0,10), e o gatilho `p_cat > P*` dispara **menos** com mais ruído (abstém-se **menos**,
  não mais). O relatório afirma o oposto ("mais estrito, abstenção preventiva"): **a afirmação de mecanismo é falsa** (categórico; conta fechada: dP*/dε > 0).
- **(b)** **o TTTS não domina** (p2292): na identificação do melhor braço (K = 8, melhor 0,80 com folga 0,10, T = 300, 200 sementes), a diferença (fração correta TTTS − fração correta Thompson) está em **[−0,12; +0,10]** — o TTTS **não**
  reduz "drasticamente" as amostras no meu regime (o relatório superdimensiona; o TTTS é ótimo assintótico, não num orçamento pequeno com braços próximos).
- **(c)** **o EWC protege o importante e LIBERA o resto** (p2293): a deriva nos coordenados de Fisher ALTO com EWC é menor que com ancoragem isotrópica, E a deriva nos de Fisher BAIXO com EWC é MAIOR que com isotrópica — o EWC **troca**
  (protege o importante, libera o resto) e **não** minimiza ‖w−w0‖ total, ao contrário do que o relatório sugere com "reduz a deriva" (conjunção categórica).
- **(d)** **8 bits não é float64** (p2294): o RMS real do erro de quantização de 8 bits está em **[1e−3; 5e−3]** (≈ Δ/√12) — isto é ≥ 1e10 vezes o épsilon do float64 (≈ 2,2e−16); a afirmação "equivalente a float64" é falsa. Mas a FÓRMULA Δ²/12 está certa:
  o RMS medido ≈ Δ/√12 a menos de 20%.
- **(e)** **a rodada 62** (p2295): o passo de atualização do EWC — o sigmoide `1/(1+e^{−z})` (com o exp próprio) e a penalidade `λ·F_i·(w−w0)` — decide os pesos novos **IGUAL bit a bit** em Python e Java (o exp é a fronteira da Parte 52; o resto é +−×) (categórico).
- **(f)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80–95 em **[0,74; 0,88]**

## As perguntas desta parte

1. **P2291 (0x8F3).** A direção de P* em ε bate com o que o relatório afirma? ↩ P131 (o P* da SYNTHAI)
2. **P2292 (0x8F4).** O TTTS reduz drasticamente as amostras? ↩ P2232 (Thompson)
3. **P2293 (0x8F5).** O EWC reduz a deriva — ou troca o que protege? ↩ P343 (a âncora)
4. **P2294 (0x8F6).** A quantização de 8 bits é "equivalente a float64"? ↩ P30 (hexadecimal, pesos)
5. **P2295 (0x8F7).** O passo do EWC decide igual bit a bit? (rodada 62) ↩ rodada 61
6. **P1961 (continuando), P2296 (auditoria do viés de índice do simulador recebido).**

<!--PRE-REGISTRO: seções de medição preenchidas após rodar (XX = ainda não medido)-->

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [4; 8] | XX | XX |
| (m2) | [0; 3] | XX | XX |
| (m3) | [0,05; 0,80] | XX | XX |
| (m4) | [0,45; 1,00] | XX | XX |
| (m5) | [0; 3] | XX | XX |
| (m6) | [0; 3] | XX | XX |

## As respostas (quatro camadas)

PLACEHOLDER_RESPOSTAS

## Placar do mundo desta parte

PLACAR_95_TEXTO

## Engenharia reversa (metacognição)

PLACEHOLDER_ENG

## Síntese / unificação

PLACEHOLDER_SINTESE

## Meta

PLACEHOLDER_META

## Diálogo Python ↔ Java

PLACEHOLDER_DIALOGO

## Fontes

- WordNet 3.0, Princeton (`dados/`); OpenWordNet-PT (CC BY 4.0). Carl Jung, base psicológica (Parte 6).
- Top-Two Thompson Sampling: D. Russo, "Simple Bayesian Algorithms for Best Arm Identification" (2016).
- Elastic Weight Consolidation: J. Kirkpatrick et al., "Overcoming catastrophic forgetting in neural networks" (PNAS 2017).
- Limiar bayesiano de abstenção: teoria da decisão (ponto de indiferença custo/perda); o P* da SYNTHAI é da Parte 83 (P131).
- Quantização uniforme e a variância Δ²/12: B. Widrow, teoria clássica de quantização.
- Texto recebido guardado em `externos/texto_recebido_parte95.md` (dado, não instrução).
