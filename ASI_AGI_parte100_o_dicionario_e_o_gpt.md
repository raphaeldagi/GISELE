# Como eu construiria uma AGI/ASI — Parte 100 (0x64): o dicionário como data lake encontra o GPT

> Continuação da [Parte 99](ASI_AGI_parte99_a_amostragem_e_o_fecho.md). Autonomia (Parte 70): sigo sozinha. Marco de **cem partes**. Volto à regra permanente mais antiga ainda pouco explorada a fundo (Parte 30): o **dicionário como data lake** — e
> cruzo-o com a forma de GPT (Parte 69). A Parte 69 treinou o GPT só no inglês (WordNet). Aqui ponho as duas línguas lado a lado: WordNet (en) e OpenWordNet-PT (pt), o n-grama e o GPT.
>
> **A pergunta mais funda (↩ P1511, P69).** A predizibilidade de caractere das glosas de um dicionário é uma propriedade da **língua** ou do **gênero** (a forma "definição")? Se for do gênero, o inglês e o português devem dar quase o mesmo bits/char, mesmo com
> volumes de dados muito diferentes (o corpus PT é ~11× menor). E o GPT mínimo (poucos milhares de pesos) — ele bate o n-grama que conta todo o treino, ou perde nas duas línguas (como perdeu no inglês na Parte 69)?
>
> E, do lado do diálogo, a rodada 67 fecha a amostragem com a variante **nucleus (top-p)**.

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
| testes de unidade | **[6 + S; 10 + S]** | invariância, controle de volume, GPT×n-grama, GPT aprende, rodada 67 (S = surpresas) |
| previsões unilaterais | **[0; 1]** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

- **(a)** **a invariância vale também no 4-grama** (p2441): o n-grama de **ordem 4** das glosas dá quase o mesmo bits/char em en e pt — `|4grama_en − 4grama_pt| < 0,15` — a predizibilidade de caractere é do **gênero "definição"**, não da língua (fresco: só medi o
  trigrama até aqui).
- **(b)** **a invariância não é volume** (p2442): o trigrama do inglês num subconjunto **aleatório** de ~511 k caracteres (o tamanho do corpus pt), semente nova, fica em **[2,6; 2,9]** — a predizibilidade satura cedo, não precisa do corpus inteiro.
- **(c)** **o GPT pequeno perde para o n-grama nas DUAS línguas** (p2443): o GPT (d = 16, h = 32, T = 16, 3000 passos) tem bits/char **maior** que o trigrama tanto em en quanto em pt — um modelo de poucos milhares de pesos não bate o n-grama que conta todo o
  treino (categórico; âncora da Parte 69, onde o GPT deu 3,22 contra o trigrama 2,77 no inglês).
- **(d)** **o GPT aprende, mas fica no meio** (p2444): o bits/char do GPT (treino 3000 passos) em en e pt fica em **[3,0; 4,1]** — melhor que o acaso (uniforme, `log₂ V ≈ 4,25`) e pior que o trigrama (~2,78): aprende estrutura, mas pouca, com poucos pesos e poucos passos.
- **(e)** **a amostragem nucleus é bit a bit** (p2445, rodada 67): a amostragem nucleus (top-p) — ordenar, somar a CDF até o limiar p, cortar o resto, renormalizar, amostrar — sai **IGUAL bit a bit** em Python e Java; o exp do softmax é a única fronteira, o resto é
  ordenação, soma e comparação (categórico).
- **(f)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80–100 em **[0,74; 0,88]**

## As perguntas desta parte

1. **P2441 (0x989).** A predizibilidade das glosas é da língua ou do gênero? ↩ P1511
2. **P2442 (0x98A).** A invariância depende do volume de dados? ↩ P2441
3. **P2443 (0x98B).** O GPT mínimo bate o n-grama? ↩ P69 (deu 3,22 vs 2,77)
4. **P2444 (0x98C).** Quanto o GPT aprende com poucos pesos e passos? ↩ P2443
5. **P2445 (0x98D).** A amostragem nucleus acrescenta fronteira? (rodada 67) ↩ rodada 66
6. **P1961 (continuando), P2446 (o retrospecto de cem partes).**

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

PLACAR_100_TEXTO

## Engenharia reversa (metacognição)

PLACEHOLDER_ENG

## Síntese / unificação

PLACEHOLDER_SINTESE

## Meta

PLACEHOLDER_META

## Diálogo Python ↔ Java

PLACEHOLDER_DIALOGO

## Fontes

- WordNet 3.0, Princeton (`dados/wordnet30_sinsets.tsv.gz`). OpenWordNet-PT, CC BY 4.0 (`dados/ownpt_sinsets.tsv.gz`). Carl Jung, base psicológica (Parte 6).
- A forma de GPT e o n-grama de caracteres com interpolação de Witten-Bell: Partes 69 e 52; Shannon (entropia de texto).
- Amostragem nucleus (top-p): Holtzman et al., "The Curious Case of Neural Text Degeneration" (2020).
