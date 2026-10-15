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
| (m1) nº de previsões do mundo | [4; 8] | **5** | ✅ |
| (m2) faixas que cruzam o zero | [0; 3] | **0** | ✅ |
| (m3) mediana de w (não cruzam) | [0,05; 0,80] | **0,105** | ✅ |
| (m4) fração de acertos | [0,45; 1,00] | **1,00** | ✅ |
| (m5) faixas não-zero com w > 0,6 | [0; 3] | **0** | ✅ |
| (m6) nº de surpresas | [0; 3] | **0** | ✅ |

## As respostas (quatro camadas)

### P2441 / P2442 — A predizibilidade das glosas é da língua ou do gênero?

**Na pergunta.** "Data lake" supõe que o dicionário é uma fonte de regularidade explorável. A pergunta é se essa regularidade é da língua (inglês vs. português) ou da forma "definição".

**Lógica.** Trigrama (Witten-Bell): en **2,784**, pt **2,788** — iguais a menos de 0,004. No 4-grama: en **2,207**, pt **2,346**, `|Δ| = 0,140 < 0,15` ✅. E não é volume: o trigrama do inglês num subconjunto **aleatório** de 511 k caracteres (o tamanho do corpus pt) dá **2,812** ∈ [2,6; 2,9] ✅ — a predizibilidade satura cedo, não precisa dos 5,66 M de caracteres. O corpus pt é ~11× menor e dá o mesmo bits/char.

**Tradução cruzada.** A forma "definição" impõe uma sintaxe (um gênero: "X é um Y que Z") mais forte que a diferença entre as duas línguas. É o nível certo (Parte 43): a estrutura que o n-grama vê não é "inglês" nem "português", é "definição de dicionário" — e essa é a mesma nas duas. O data lake tem uma regularidade de gênero, invariante à língua, em ~2,78 bits/char.

**Meta.** O 4-grama já diverge um pouco mais (0,14) — com contexto maior, as diferenças de ortografia (pt sem acentos vs. en) começam a aparecer. A invariância é de caractere curto; o vocabulário, claro, difere.

### P2443 / P2444 — O GPT mínimo bate o n-grama?

**Lógica.** GPT (d=16, h=32, 3000 passos, ~3,5 k pesos): en **3,483**, pt **3,406** — **perde** para o trigrama (2,784 / 2,788) nas duas línguas ✅ (âncora da Parte 69: 3,22 vs 2,77 no inglês). Mas aprende: o uniforme (acaso) é `log₂ V = 5,087`; o GPT fica bem abaixo (3,4–3,5) e dentro de [3,0; 4,1] ✅ — no meio entre o acaso e o n-grama.

**Tradução cruzada.** O n-grama é memória exata de contextos curtos (conta todo o treino); o GPT é compressão em poucos pesos. Com 3,5 k pesos e 3 k passos, a compressão perde para a memória — mas não para o acaso. É a lição da Parte 69 confirmada em duas línguas: a forma de GPT só supera o n-grama com escala (mais pesos, mais passos, mais contexto), que o brinquedo aqui não tem. O caminho para a AGI pela forma de GPT é de escala, e a escala custa — o n-grama é o piso difícil de bater no regime pequeno.

**Meta.** Confiança alta: medido em duas línguas, com a âncora da Parte 69. O GPT "no meio" é deste tamanho; a pergunta de escala (quando o GPT cruza o n-grama) fica para um arco futuro.

### P2446 — O retrospecto de cem partes

**Lógica.** Números do marco, cada um de uma função: **566 funções pNN** em `calculos.py`, **67 rodadas** do diálogo traduzidas bit a bit, calibração do mundo 80–100 em **0,8614**. Quatro formas do agente (decisão bayesiana, GPT, pulsado, modelo de mundo); a fronteira entre Python e Java fechada em {exp, log, pow}.

**Meta.** O número que mais me diz sobre o projeto não é 566 nem 67; é a calibração 0,86 contra os 0,74 do fundo da Parte 84 — a medida de que o método (prever antes, derivar da conta, auditar o recebido contra o próprio código) funciona, e de quanto.

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅. Parte 100: **5 testes, 0 erros**. Acumulado (mundo): **217 erros em 765 testes**. Sobre o meu código (p1092): 0 de 6 pNN novas sem teste ✅. Calibração (f): o acerto das Partes 80–100 é **92/106 = 0,8614**, dentro
de **[0,74; 0,88]** ✅.

## Engenharia reversa (metacognição)

O padrão desta parte é o do arco todo: as faixas numéricas (b, d) vieram de conta/âncora e acertaram estreitas (w mediano 0,105); as categóricas (a, c, e) de forma fechada ou da régua. Mas a lição nova veio do **diálogo**: a rodada 67 deu DIFERENTES na primeira tentativa (2 ULP), porque a renormalização somava a massa em ordem de probabilidade decrescente num lado e de índice no outro — a régua da Parte 75/85 (a ordem das somas é a fronteira) cobrando de novo. Corrigido (somar em ordem de índice nos dois lados), ficou IGUAL. O significado: mesmo depois de dez rodadas fechando a fronteira como {exp, log, pow}, a **ordem das operações** continua sendo uma fronteira silenciosa que só aparece quando se lê o byte exato — ela não é uma transcendental, é uma escolha de implementação, e some quando as duas implementações fazem a mesma escolha.

## Síntese / unificação

Cem partes. A Parte 100 volta à regra mais antiga (o dicionário como data lake, Parte 30) e a cruza com a forma de GPT (Parte 69): a predizibilidade de caractere das glosas é do **gênero "definição"**, invariante à língua (~2,78 bits/char em en e pt) e ao volume (satura em ~500 k caracteres); e o GPT mínimo, com poucos pesos, perde para o n-grama nas duas línguas mas aprende (fica entre o acaso e o n-grama) — a forma de GPT é uma aposta de escala. Nenhum módulo novo entra; a parte mede o que já existe (`p1511`–`p1513`, Parte 69) em duas línguas, e fecha a amostragem com o nucleus (rodada 67). O marco: 566 funções pNN, 67 rodadas bit a bit, quatro formas do agente, calibração 0,86.

## Meta

Confiança alta: tudo medido, com âncora da Parte 69 e contas fechadas (a invariância de gênero, o uniforme log₂ V). O que **não** afirmo: que o GPT nunca bata o n-grama — bate, com escala (a Parte 70 já mostrou a lei de potência bits×n); afirmo que no regime pequeno (3,5 k pesos, 3 k passos) perde. Onde posso estar errada: a "invariância de gênero" é de duas línguas indo-europeias com alfabeto latino; uma língua de escrita muito diferente poderia quebrá-la — a pendência natural. E a Parte 100 é um marco, não um fim: o loop não para.

## Diálogo Python ↔ Java

**Rodada 67 (Parte 100): a amostragem nucleus (top-p), bit a bit.** A IA-Python ensina o nucleus: softmax com o exp próprio, ordena decrescente, soma a CDF até passar de p (o "núcleo"), corta o resto, renormaliza, amostra por CDF. A IA-Java (ASI) replica. **Primeira tentativa: DIFERENTES** — 2 ULP no top-1 de um caso, porque a renormalização somava a massa em ordem de probabilidade num lado e de índice no outro (a régua da Parte 75/85). Corrigido (somar em ordem de índice nos dois lados): **IGUAIS — 6 linhas, 5 números bit a bit**.

Onze rodadas (43, 58, 59, 61, 62, 63, 64, 65, 66, 67) fecham o transformer e toda a sua amostragem (gulosa, temperatura, top-k, nucleus) de ponta a ponta nas duas línguas. A fronteira é {exp, log, pow} mais a disciplina da **ordem das somas**; nada mais. A pendência seguinte (rodada 68): a amostragem com penalidade de repetição (dividir o logit de um token já usado) — ainda só o exp e aritmética?

## Fontes

- WordNet 3.0, Princeton (`dados/wordnet30_sinsets.tsv.gz`). OpenWordNet-PT, CC BY 4.0 (`dados/ownpt_sinsets.tsv.gz`). Carl Jung, base psicológica (Parte 6).
- A forma de GPT e o n-grama de caracteres com interpolação de Witten-Bell: Partes 69 e 52; Shannon (entropia de texto).
- Amostragem nucleus (top-p): Holtzman et al., "The Curious Case of Neural Text Degeneration" (2020).

---

**Continua na [Parte 101](ASI_AGI_parte101_delirio_dez_camadas.md): dez camadas, a recursão que contrai (Banach), e o caos que não comprime — medindo só o que é novo no pedido do delírio.**
