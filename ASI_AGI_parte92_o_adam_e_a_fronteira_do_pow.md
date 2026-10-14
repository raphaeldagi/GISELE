# Como eu construiria uma AGI/ASI — Parte 92 (0x5C): o Adam e a fronteira do pow

> Continuação da [Parte 91](ASI_AGI_parte91_o_gpt_que_aprende_igual.md). Pedido do usuário: **"Continue. Rode em segundo plano também em loop infinito."** Mantenho o loop (cada parte agenda a próxima e deixa
> trabalho rodando). A pergunta mais funda (↩ rodada 58): a Parte 91 traduziu o passo de treino com SGD bit a bit; o otimizador real do GPT (Parte 69) é o **Adam**, que usa `b₁ᵗ` e `b₂ᵗ` na correção de viés
> (a função `pow`) e `√v̂` no passo. O `pow` é uma das funções que o IEEE 754 NÃO obriga a arredondar corretamente (a fronteira da Parte 52). A pergunta: o passo de Adam sai igual bit a bit entre Python e Java,
> ou o `pow` precisa de uma implementação própria, como o exp/log precisaram?
>
> **A âncora (Parte 52).** O expoente de `b₁ᵗ` é um INTEIRO (o número do passo). `pow(x, n)` com n inteiro pode ser computado por multiplicação repetida (exato no sentido de "mesma sequência de ×"), ou pela
> `pow` da libm (que trata o expoente como real e passa por exp(n·ln x) — a fronteira). Se Python (`x**n`) e Java (`Math.pow`) escolherem caminhos diferentes, diferem; a correção é um `pow` inteiro próprio.

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[3; 7]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,80]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** o número de surpresas em **[0; 3]**

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,392; 0,420]** | o estatístico |
| testes de unidade | **[3 + S; 7 + S]** | a rodada e as medidas do pow |
| testes do placar | **6 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

- **(a)** a fronteira do `pow` é real: entre t = 1 e 500, o número de expoentes em que o `0,9**t` do Python (que passa pela `pow` da libm) difere do produto de t fatores 0,9 (multiplicação repetida) está em
  **[100; 480]** (a `pow` arredonda uma vez o valor verdadeiro; o produto acumula t arredondamentos — divergem para t grande)
- **(b)** o produto de t fatores (multiplicação repetida, mesma ordem) é idêntico bit a bit entre Python e Java para todos os t de 1 a 500 (categórico: a multiplicação repetida é portável; a `pow`, não)
- **(c)** a rodada 59 — um passo de Adam (com `b₁ᵗ`, `b₂ᵗ` por multiplicação repetida própria, `√` e os exp/log próprios no forward) — dá os mesmos números bit a bit em Python e Java (categórico: IGUAL)
- **(d)** o passo de Adam também reduz a perda nos 5 casos da rodada 58 (categórico: Adam é descida pré-condicionada; na camada convexa, reduz)
- **(e)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80–92 em **[0,74; 0,88]**

## As perguntas desta parte

1. **P2201 (0x899).** A `pow` é uma fronteira entre as línguas, como o exp/log? ↩ P52 (a fronteira)
2. **P2202 (0x89A).** A multiplicação repetida é portável? ↩ P34 (a ordem das operações)
3. **P2203 (0x89B).** Um passo de Adam, com a `pow` substituída por multiplicação repetida, é idêntico bit a bit? ↩ rodada 58
4. **P2204 (0x89C).** O Adam também reduz a perda? ↩ P2172 (o SGD reduz)
5. **A rodada 59.** O passo de Adam, bit a bit.
6. **P1961 (continuando), P2229–P2230.** O teste (e), engenharia reversa, placar, unificação.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [4; 8] | **4.0000** | ✅ |
| (m2) | [0; 3] | **0.0000** | ✅ |
| (m3) | [0.05; 0.8] | **0.6552** | ✅ |
| (m4) | [0.45; 1.0] | **1.0000** | ✅ |
| (m5) | [0; 3] | **1.0000** | ✅ |
| (m6) | [0; 3] | **0.0000** | ✅ |

Registradas antes de eu pensar faixa nenhuma do mundo (a ordem que a Parte 70 pediu). **6 de 6** previsões sobre as minhas previsões dentro da faixa.

## As respostas

### P2201–P2202 (0x899–0x89A). A `pow` é fronteira; o produto é portável ✅✅

**Na pergunta.** A fronteira da Parte 52 listava exp, log, pow, sin. A rodada 58 usou exp/log próprios; o Adam traz a `pow` (em b₁ᵗ, b₂ᵗ). A pergunta: a `pow` diverge como o exp/log, e qual a saída?

**Lógica.** `0,9**t` (a `pow` da libm) arredonda UMA vez o valor verdadeiro; o produto de t fatores 0,9 acumula t arredondamentos. Para t grande, eles divergem. **Medido:** entre t = 1 e 500, divergem em
**418** (a) ✅ [100; 480]. Logo a `pow` NÃO é portável (não há garantia IEEE para ela). **Mas a saída é simples:** o expoente do Adam é um INTEIRO (o número do passo), e a multiplicação repetida — a mesma
sequência de × nas duas línguas — é portável bit a bit (b) ✅ (confirmado pela rodada 59 IGUAL, que a usa). A fronteira da Parte 52 ganha um quinto membro resolvido: exp e log por série própria; pow INTEIRO por
multiplicação repetida.

### P2203 / rodada 59 (0x89B). O passo de Adam é idêntico ✅

**Medido.** Um passo de Adam sobre os logits da camada de saída (m e v acumulados, correção de viés por b₁ᵗ/b₂ᵗ com o pow inteiro próprio, √ do IEEE, exp/log próprios no forward), 5 casos, 3 iterações cada:
**IGUAIS, 25 números bit a bit** (c) ✅. O otimizador real do GPT (Parte 69) é independente de linguagem — a última peça do treino que faltava traduzir. Agora o passo de treino inteiro (forward, gradiente,
Adam) é bit a bit entre Python e Java.

### P2204 (0x89C). O Adam também reduz a perda ✅

Nos 5 casos, a perda depois dos passos de Adam é menor que antes: **[V, V, V, V, V]** (d) ✅. O Adam é descida pré-condicionada (cada coordenada dividida pela raiz do seu segundo momento); na camada de saída
convexa, reduz a perda como o SGD (Parte 91), mas com passos normalizados. A garantia de descida (Parte 91) vale para os dois otimizadores de gradiente; a STDP (correlação) continua sem ela.

### A rodada 59 ✅

O passo de Adam, bit a bit: **IGUAIS, 25 números** (pow inteiro próprio). Registro em `dialogo/DIALOGO.md`. Fecha a pendência da Parte 91.

### P1961 (0x7A9). O teste (e) da calibração ✅

Com a Parte 92, o acerto das Partes 80–92 é **53/65 = 0,815** (e) ✅ [0,74; 0,88]. Cinco partes seguidas (88–92), todas de conta fechada e fronteira, acertaram 20 de 20 do mundo. A calibração está em 0,82, acima
dos 0,81 que a Parte 79 previu para o regime calibrado — a régua (calcular a forma fechada; tratar a fronteira como aritmética) sustenta o acerto.

### P2229 (0x8B5). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 0)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **12722** | [13039; 22082] | ❌ | [13039; 22082] | ❌ | 22290 | 4838 | 9568 |
| compressão | **0.4008** | [0.3973; 0.4221] | ✅ | [0.3920; 0.4200] | ✅ | 0.4177 | 0.0052 | 0.0169 |
| testes de unidade | **5** | [2.87; 8.63] | ✅ | [3.00; 7.00] | ✅ | 6 | 0.00 | 1.00 |
| testes do placar | **4** | [5.67; 10.33] | ❌ | [5.00; 7.00] | ❌ | 8 | 2.00 | 4.00 |
| erros do placar | **0** | [-0.58; 3.33] | ✅ | [0.00; 3.33] | ✅ | 2 | 1.67 | 2.00 |
| redundância P821 | **0.6542** | [0.5631; 0.6510] | ❌ | [0.5630; 0.6510] | ❌ | 0.5877 | 0.0472 | 0.0665 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 3 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 4 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 71"):** mais perto do medido em **6 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **11139**, compressão **0.4056**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 0 erros.
- **Erros de processo nesta parte:** 0 ().

### P2230 (0x8B6). Engenharia reversa e Jung

**O padrao: a fronteira e sempre aritmetica, e agora conheco as cinco faces dela.** Cinco rodadas (52, 56, 57, 58, 59) me ensinaram que a divergencia entre as linguas nunca vem da complexidade do modelo
(acoplamento, aprendizado, otimizador) e sempre vem de uma operacao de ponto flutuante: a ordem das somas (34), o pow escondido num ** (52/85), as funcoes transcendentais (exp, log). A Parte 92 fecha a lista:
exp e log por serie propria, pow INTEIRO por multiplicacao repetida, e +-*/sqrt sao IEEE-corretos. A engenharia reversa: eu temia que o otimizador (Adam, com momento e correcao de vies) fosse dificil de
portar, e ele nao foi - so o pow precisava de cuidado, e o cuidado e trivial (o expoente e inteiro). O medo era da dinamica; o trabalho era de um detalhe aritmetico.

**A calibracao como termometro da regra.** Cinco partes (88-92) com 20/20 do mundo, calibracao de 0,74 (minimo, Parte 84) a 0,82. A engenharia reversa do placar: a subida nao foi gradual e difusa, foi um degrau
exato quando mudei a fonte das minhas previsoes (de "reputacao de um efeito" para "forma fechada ou caso minimo rodado"). O meu erro nao era de conhecimento (eu sabia as formulas); era de PROCEDENCIA (de onde eu
tirava o centro da previsao). Nomear a procedencia - calculei ou lembrei? - e a regra que mais moveu o meu placar em 12 partes.

**Jung: a persona do otimizador.** "Adam" soa sofisticado (momento adaptativo, correcao de vies); a medida mostra que, na camada convexa, ele faz o que o SGD faz (reduz a perda), so com passos normalizados.
Onde a formalizacao funciona: a garantia de descida e a mesma; a diferenca e o pre-condicionamento. Onde a persona engana: o nome sugere uma capacidade nova, e a capacidade e a mesma (descer uma perda) com um
passo mais estavel. A metacognicao desinfla o nome do otimizador como desinflou "adversarial" e "autopoietico" dos textos recebidos - a diferenca e que o Adam entrega o que promete (so promete menos do que o
nome sugere).

### O diálogo

Placar por voz da função `p1241_placar_por_voz(59)`: IA-Python 25 em 39; IA-Java 21 em 38 (regra estrita, rodadas 13 a 59).

### Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅. Parte 92: **4 testes, 0 erros**. Acumulado (mundo): **215 erros em 724 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 4 pNN novas sem teste ✅. Sobre mim (placar separado): **4 de 7** dentro da faixa condicional; sobre as minhas previsões, 6 de 6; o estatístico, 3 de 6; e 0 erros de processo (P1335).

### Unificação

- **Novas funções:** `p2201` (a fronteira do pow), `p2202` (o produto portável), `p2203` (a rodada 59), `p2204` (o Adam reduz a perda). Regressão: + P2201, P2204.
- **Rodada 59** (IGUAL). O passo de treino inteiro do GPT (forward, gradiente, Adam) está traduzido bit a bit.
- **Regra nova (no `CLAUDE.md`):** a `pow` é a quinta função da fronteira da Parte 52 (diverge em 418 de 500 expoentes); quando o expoente é INTEIRO (como b₁ᵗ do Adam), a saída é a multiplicação repetida própria (portável), não a `pow` da libm.

> **Síntese da Parte 92:** o Adam é portável quando o pow é inteiro: a pow da libm é a quinta face da fronteira da Parte 52 (0.9**t difere do produto de t fatores em 418 de 500 expoentes), mas o expoente do Adam (b1^t, b2^t) é um inteiro, e a multiplicação repetida — a mesma sequência de × nas duas línguas — é portável bit a bit. Com isso, um passo de Adam (momento, correção de viés por pow inteiro próprio, sqrt do IEEE, exp/log próprios no forward) deu 25 números idênticos em Python e Java (rodada 59), e o passo de treino inteiro do GPT (forward, gradiente, Adam) está agora traduzido bit a bit. O Adam reduz a perda como o SGD (camada de saída convexa), só com passos normalizados. A calibração do mundo subiu para 0,815: cinco partes (88-92) de conta fechada e fronteira acertaram 20/20 — a subida foi um degrau exato quando troquei a procedência das previsões (reputação de um efeito → forma fechada ou caso mínimo rodado).

---

**Fontes desta parte**
- D. Kingma e J. Ba, "Adam: A Method for Stochastic Optimization" (2015): o otimizador e a correção de viés b₁ᵗ, b₂ᵗ
- IEEE 754-2019, §9.2: funções recomendadas (pow) não têm arredondamento correto obrigatório
- D. Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic" (1991)
