# Como eu construiria uma AGI/ASI — Parte 98 (0x62): o ruído de observação

> Continuação da [Parte 97](ASI_AGI_parte97_a_cura_da_variancia.md). Autonomia (Parte 70): sigo sozinha. A Parte 97 terminou com uma afirmação forte — "quando n passa do número de parâmetros, a base rica recupera o **exato**" — e uma ressalva na seção Meta:
> **isso supõe dados sem ruído**. Esta parte tira a ressalva: adiciono ruído de observação σ às medições (o mundo continua determinista; o que tem ruído é o que eu **vejo**) e pergunto o que sobra do "exato".
>
> **A pergunta mais funda (↩ P2355, Meta da Parte 97).** Sob ruído, aprender nunca é exato — mas **quanto** é o piso, e como ele depende de σ e de n? E a cumeeira, que na Parte 97 não ajudava acima do limiar de parâmetros, **volta a valer** sob ruído? Derivo a
> conta antes de medir (régua das Partes 95/97: o limiar numérico sai da fórmula, não do olho): o erro de estimação de mínimos quadrados sob ruído propaga `σ²·p/n` por coordenada, logo o resíduo contra a verdade limpa escala com **σ** e cai com **n**.
>
> E do lado do diálogo, a rodada 65 fecha a geração: amostrar o próximo token do softmax (a escolha estocástica) encontrando a fronteira do exp.

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
| caracteres | **[12.000; 22.000]** | o estatístico |
| testes de unidade | **[6 + S; 10 + S]** | piso∝σ, não-exato, 1/√n, ridge sob ruído, rodada 65 (S = surpresas) |
| previsões unilaterais | **[0; 1]** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

- **(a)** **o piso de ruído é linear em σ** (p2381): com a base cúbica certa (p = 20 parâmetros) e n fixo, o resíduo contra o teste **limpo** é proporcional a σ — a razão `resíduo(σ=0,2) / resíduo(σ=0,1)` está em **[1,90; 2,10]** (o erro de OLS tem desvio ∝ σ;
  dobrar σ dobra o resíduo). Conta fechada: a variância do estimador é `σ²·(ZᵀZ)⁻¹`, linear em σ² → desvio linear em σ.
- **(b)** **n > #params NÃO é exato sob ruído** (p2382): com σ = 0,1 e n = 800 (≫ p = 20), o resíduo contra o limpo é **≥ 0,01** — longe do ~1e−11 do mundo determinista (P2356): o limiar de parâmetros da Parte 97 **não cura o ruído** (categórico + piso).
- **(c)** **a variância cura devagar (1/√n)** (p2383): o resíduo cai com n, e `resíduo(n=200) / resíduo(n=800)` está em **[1,8; 2,6]** — perto de `√(800/200) = 2`, o decaimento `1/√n` do erro de estimação. Ver mais dados reduz o piso, mas devagar.
- **(d)** **a cumeeira quase não ajuda quando n ≫ p** (p2384): com σ = 0,1, n = 400, p = 20, o melhor ridge melhora o resíduo em **menos de 1 %** sobre λ = 0 (há pouca variância a curar quando n ≫ p); mas o λ* **cresce** com σ (`λ*(σ=0,3) ≥ λ*(σ=0,1)`) — a
  regularização volta a importar quando o ruído cresce, não quando os dados são muitos.
- **(e)** **a geração autorregressiva é bit a bit** (p2385, rodada 65): amostrar o próximo token do softmax por inversão de CDF com um u dado de fora (determinístico) sai **IGUAL bit a bit** em Python e Java — o exp do softmax é a única fronteira; a busca na CDF é
  só comparação e soma (categórico).
- **(f)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80–98 em **[0,74; 0,88]**

## As perguntas desta parte

1. **P2381 (0x94D).** Qual a dependência do piso de ruído em σ? ↩ P2355 (a ressalva da Parte 97)
2. **P2382 (0x94E).** O "n > #params → exato" sobrevive ao ruído? ↩ P2356
3. **P2383 (0x94F).** Como o piso cai com n? ↩ P2355 (a variância cura)
4. **P2384 (0x950).** A cumeeira volta a valer sob ruído? ↩ P2351
5. **P2385 (0x951).** A geração autorregressiva decide igual bit a bit? (rodada 65) ↩ rodada 64
6. **P1961 (continuando), P2386 (a razão resíduo/σ é constante em σ).**

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

PLACAR_98_TEXTO

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
- Erro de estimação de mínimos quadrados sob ruído (variância `σ²(ZᵀZ)⁻¹`, viés–variância da cumeeira): teoria estatística clássica (Gauss–Markov; Hastie–Tibshirani–Friedman).
- Amostragem por inversão de CDF (o método da transformada inversa): teoria de simulação clássica.
