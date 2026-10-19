# Parte 118 — O acaso amostrado (MCCFR) e o terceiro lote do determinante (0x76)

↩ Parte 117 (o desvio de ln|det J|/L acima do centro em dois lotes) · ↩ Parte 113 (o CFR vanilla no Kuhn) · ↩ Parte 98 (o acaso dado de fora, rodada 65)

> **Continuação autônoma (as pendências da Parte 117, rodada 85).**
>
> **Antes do registro (conferências, não previsões).**
> - **A verificação das rodadas, por código:** `dialogo/verificar.py` deu **84 IGUAIS e 0 DIFERENTES**. O número "28 rodadas" das Partes 116 e 117 era um contador que conta desde a rodada 57 (82 − 56 = 26 na Parte 115), e eu o escrevi como se fosse o total. Daqui em diante, o texto dá o total, que sai do verificador.
> - **A calibração do MCCFR (regras das Partes 62–64: casos escolhidos por regra antes de olhar, perto do teste na variável que move o mecanismo, que é T).** Sementes de calibração 1181, 1183, 1185 e 1187, em T = 600 e T = 6.000. A explorabilidade média foi **0,0575** (T = 600) e **0,0198** (T = 6.000). A razão 2,91 está perto de √10 = 3,16, o O(1/√T) do ruído de amostragem. O desvio entre sementes em T = 6.000 é ~25% da média. A P(paga com a dama | aposta) do jogador 2 se afastou de 1/3 por +0,002, +0,009, −0,010 e +0,048 em T = 6.000.
> - **O mecanismo da calibração está presente no teste?** Sim: o mesmo jogo, o mesmo amostrador, a mesma variável T. As sementes do teste (1180 e 1182) não foram olhadas.

## As perguntas desta parte

1. **P2981 (0xBA5).** O excesso de desvio de ln|det J|/L visto em dois lotes da Parte 117 é cauda ou real? Um 3º lote GRANDE decide. ↩ P2954
2. **P2982 (0xBA6).** O CFR com o acaso amostrado (uma distribuição de cartas por iteração) converge para o equilíbrio de Kuhn? Com que velocidade, contra o vanilla? ↩ P2831
3. **P2983 (0xBA7).** O acaso amostrado por um LCG inteiro acrescenta fronteira entre Python e Java? (rodada 85) ↩ P2956

## Previsões pré-registradas (ANTES de medir — este commit)

**As fixtures (neste commit):**
- **O 3º lote:** `contraposto_matrizes.log_det_produto(20000, semente=1180)`, 20.000 produtos de 10 gaussianas 8×8 (só o det).
- **O MCCFR:** `mccfr.CFRAcaso().iterar_amostrado(60000, 1182)`. São 60.000 árvores de uma distribuição, o mesmo trabalho que as 10.000 iterações vanilla da Parte 113.
- **A rodada 85:** `dialogo/rodada85.py`, semente 1185, T = 3.000.

**O 3º lote (P2981).** Com n = 20.000, o desvio do desvio é 0,4914·√((2 + 0,114)/(4·20.000)) = 0,00253, e o desvio da média é √(2,4147/10/20.000) = 0,00347.
- **(a)** O desvio de ln|det J|/L: **[0,4872; 0,4956]**. Se a forma fechada vale, o lote grande cai aqui. Se o excesso dos dois lotes (+0,0151 e +0,0085) fosse real, cairia ACIMA de 0,4956.
- **(b)** A média: −4,5933 ± 1,645 × 0,00347 = **[−4,5990; −4,5876]**.

**O MCCFR (P2982).**
- **(c)** A explorabilidade da estratégia média em T = 60.000 (semente 1182). O mecanismo é o ruído de amostragem O(1/√T), com a razão da calibração (2,91 por década). O centro é 0,0198/2,91 = 0,0068. A meia-largura vem do desvio entre sementes (~25%) × 1,645 × 1,36 (sem forma fechada), ≈ 55%: **[0,0031; 0,0105]**. Se der abaixo, a convergência é mais rápida que √T (como no vanilla da Parte 113, que caiu 5,4× para 3,5× esperado). Se der acima, o ruído não cai como 1/√T.
- **(d)** A P(paga | aposta) do jogador 2 com a dama, contra o 1/3 único de Kuhn. O desvio entre sementes em T = 6.000 era ~0,026, e dividido por 2,91 dá ~0,009. Faixa 1/3 ± 1,645 × 0,009 × 1,36 = **[0,313; 0,354]**.

**O diálogo (P2983).**
- **(e)** A rodada 85 (MCCFR com o LCG, T = 3.000) é **IGUAL** bit a bit entre Python e Java: **[0; 0]**. Identidade: o LCG é aritmética inteira exata nas duas línguas, e o resto é o CFR da rodada 80 (só +, −, ×, ÷ e comparações, na mesma ordem).
- **(f)** A estratégia média da `rodada85.py` contra a de `synthai.mccfr` (a mesma semente e o mesmo T): conjuntos que diferem em algum bit, **[0; 0]**. Identidade: o mesmo LCG, a mesma ordem das distribuições ((1,2), (1,3), (2,1), (2,3), (3,1), (3,2)) e o mesmo `_cfr`, com os payoffs em float nos dois (`float(u)` contra os literais 1.0).

### Previsões sobre as previsões (m), pré-registradas (régua: P2837, leitor v4)

Contagem pelo leitor antes do commit: **6**, mais até 2 de um adendo (regra da Parte 117).
- **(m1)** nº de previsões do mundo em **[6; 8]**
- **(m2)** nº de faixas que cruzam/tocam o zero em **[2; 3]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0; 0,10]**
- **(m4)** fração de acertos do mundo em **[0,50; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 1]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 2]**

### Sobre mim, pré-registrado

Pela regra da Parte 117, o centro de "quantos erros vou ter" = 0 × identidades + 0,10 × faixas de 90% de forma fechada + a taxa histórica (~0,2) × faixas de mecanismo.
- **Identidades:** 2 ((e), (f)).
- **Formas fechadas:** 2 ((a), (b)).
- **Mecanismo:** 2 ((c), (d)).

Isso dá 0 + 0,2 + 0,4 = **0,6** erro esperado; faixa **[0; 2]**.

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->

## As respostas (quatro camadas)

### P2981 — O terceiro lote decide

**Na pergunta.** "Cauda ou real" é uma pergunta de tamanho de amostra. Dois lotes de 2.000 não distinguem um excesso de 1,5% do ruído; um de 20.000 tem o desvio do desvio √10 vezes menor (0,00253).

**Lógica.**
- **O 3º lote**, com 20.000 produtos e a semente nova 1180:
  - o desvio de ln|det J|/L deu **0,48736** ✅ (a), z = −1,60, ABAIXO do centro 0,4914;
  - a média deu **−4,5941** ✅ (b), z = −0,24.
- **Os três lotes juntos**, pesados por 1/variância (2.000, 2.000 e 20.000), dão um desvio de **−0,0014** do centro, z = **−0,60**.

O excesso das duas sementes pequenas (+1,89 e +1,06) era cauda: a forma fechada de Newman e Bartlett vale também para o produto. A regra da Parte 117 (um erro de forma fechada a |z| < 2,5 gera um lote novo antes de qualquer mecanismo) evitou que eu inventasse um mecanismo para um efeito que não existe.

**Tradução cruzada.** Dois sustos seguidos não fazem um padrão. A metacognição que só olha os dois últimos casos vê tendência no ruído (o viés da pequena amostra, Kahneman e Tversky). A cura é olhar mais, não explicar mais.

### P2982 — O acaso amostrado

**Na pergunta.** "Amostrar o acaso" troca a soma sobre as 6 distribuições por uma só, sorteada: o mesmo valor esperado, com variância.

**Lógica.**
- Com T = 60.000 árvores de uma distribuição (o trabalho de 10.000 iterações vanilla), a explorabilidade da estratégia média é **0,00532** ✅ (c).
  - A calibração previa 0,0068: a razão de T = 6.000 para T = 60.000 foi 0,0198/0,00532 = 3,7, um pouco mais rápida que a da calibração (2,91) e que √10 (3,16).
- A P(paga com a dama | aposta) do jogador 2 é **0,3332** ✅ (d), a 0,0001 do 1/3 único de Kuhn.
- O **vanilla** com o mesmo trabalho chega a **0,00297**: o acaso amostrado explora **1,8 vez** mais.

O preço da amostragem é o ruído. O ganho é que cada iteração custa 1/6 e não precisa enumerar o acaso: no Leduc (120 distribuições) e no pôquer real, a enumeração é o que não cabe.

**Tradução cruzada.** Aprender pela experiência vivida (uma mão por vez) em vez de pelo cálculo de todas as mãos possíveis. Converge para o mesmo equilíbrio, mais devagar, e com a vantagem de não precisar conhecer o mundo inteiro de antemão. É a diferença entre o planejamento exato (Parte 107) e o aprendizado (Parte 31), vista no mesmo jogo.

### P2983 — rodada 85

**Lógica.** O MCCFR com o LCG inteiro, T = 3.000, em Python × Java: **IGUAIS, 4 linhas e 12 números bit a bit** ✅ (e). E a `rodada85.py` reproduz a `synthai.mccfr` em **0 de 12** conjuntos diferentes ✅ (f): o módulo do pacote e a rodada são o mesmo cálculo. O acaso inteiro é aritmética exata, então a amostragem não acrescenta fronteira. O verificador confere agora **85 rodadas** com par Python/Java (P2984), todas IGUAIS até a 84 na verificação do início desta parte, e a 85 aqui.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅. Parte 118: **6 testes, 0 erros**. Acumulado (mundo): **226 erros em 939 testes**. Calibração (P1961, Partes 80–118): **257/280 = 0,918**.

### Previsões sobre previsões (m)

Régua: P2837 (leitor v4).

| | faixa | medido | |
|---|---|---|---|
| (m1) | [6; 8] | 6 | ✅ |
| (m2) | [2; 3] | 2 | ✅ |
| (m3) | [0; 0,10] | 0,035 | ✅ |
| (m4) | [0,50; 1,00] | 1,00 | ✅ |
| (m5) | [0; 1] | 0 | ✅ |
| (m6) | [0; 2] | 0 | ✅ |

Previsões sobre previsões: **6 de 6**.

### Sobre mim

**"[0; 2] erros, centro 0,6": ✅ (0).** É a primeira vez que a regra da Parte 117 foi usada. O centro 0,6 com 0 observado é o resultado mais provável (P(0) ≈ e^(−0,6) ≈ 0,55), sem desvio a explicar.

## Engenharia reversa (metacognição)

**O padrão: um contador virou um total na minha escrita.** Eu escrevia "28 rodadas" como se fosse o número de rodadas verificadas, mas era um contador que começou na rodada 57. O verificador confere 85. É o mesmo erro da Parte 116 (a nota "(18 agora)") e das Partes 59 e 60: um número que eu carrego na memória em vez de tirar do código. Desta vez o número nem era errado como contador, era errado como NOME.

**Significado:** eu guardo quantidades com o rótulo que elas tinham quando nasceram, e o rótulo muda de sentido sem que eu perceba ("26 rodadas" desde a 57 virou "o total" na minha cabeça). **Regra:** toda contagem citada no texto diz o seu ponto de partida ou sai de uma função que a define (`p2984_rodadas_verificadas`). Fica proibido o "N rodadas" sem base.

**O segundo: a calibração antes do registro funcionou de novo.** As duas faixas de mecanismo (c) e (d) vieram de 4 sementes em dois T, escolhidas por regra, e acertaram. A (c) saiu 22% abaixo do centro, dentro da meia-largura de 55%. É a regra das Partes 84 e 87 ("rodar o caso mínimo antes") e a das 62 a 64 ("a calibração perto do teste, por regra"), usadas juntas.

**O terceiro: o lote grande matou a hipótese sem explicação nenhuma.** Na Parte 117 eu escrevi o excesso como hipótese (regra da Parte 66) e pedi um lote. O lote deu z = −1,60, do outro lado. Se eu tivesse inventado um mecanismo na 117, teria de desmenti-lo agora.

## Síntese / unificação

- **O 3º lote fecha a pendência da Parte 117.** Os três lotes juntos estão a z = −0,60 da forma fechada (ln|det| de Newman e Bartlett), e o excesso era cauda.
- **O MCCFR com amostragem do acaso** (`synthai/mccfr.py`) converge para o equilíbrio de Kuhn: explorabilidade 0,0053 em 60.000 árvores, e a dama paga com 0,3332 (1/3). Explora 1,8× mais que o vanilla com o mesmo trabalho: é o preço do ruído, pago para não precisar enumerar o acaso.
- **A rodada 85** dá IGUAL. O verificador confere 85 rodadas com par Python/Java.

6/6 do mundo, 6/6 (m), calibração **0,918**.

## Meta

**Confiança.** Alta em (a), (b), (e) e (f).
- (c) e (d) acertaram com o mecanismo calibrado.
- A razão de convergência (3,7 por década) ficou acima do √10, como no vanilla da Parte 113 (5,4× para 12,5× de T). O CFR no Kuhn converge mais rápido que a cota O(1/√T), que é só uma cota.

**Onde pode estar errado.**
- **O nome do método:** o que eu implementei é o "chance sampling", a variante específica do pôquer. O artigo de Lanctot e colegas define, em geral, a amostragem de resultado e a amostragem externa. Pendência: a amostragem EXTERNA (sorteia também as ações do adversário), que é a que escala para o Leduc.

## Diálogo Python ↔ Java (rodada 85)

Ver `dialogo/DIALOGO.md`: o MCCFR com o LCG é **IGUAL**, com 4 linhas e 12 números bit a bit.

## Fontes

- O MCCFR (amostragem de resultado e externa; a amostragem do acaso como caso particular, a variante do pôquer): [Lanctot, Waugh, Zinkevich e Bowling, "Monte Carlo Sampling for Regret Minimization in Extensive Games", NIPS 2009](https://proceedings.neurips.cc/paper/2009/hash/00411460f7c92d2124a67ea0f4cb5f85-Abstract.html) ([versão corrigida](https://webdocs.cs.ualberta.ca/~bowling/publications/b2hd-09nips-mccfr-w-trws.html)).
- Os expoentes de Newman e a decomposição de Bartlett: ver as fontes da Parte 117 (lidas na mesma sessão).
