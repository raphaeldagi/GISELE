# Como eu construiria uma AGI/ASI — Parte 69 (0x45): a forma de GPT

> Continuação da [Parte 68](ASI_AGI_parte68_o_tipo_da_quantidade.md). **Próxima:** [Parte 70 — álgebra e geometria](ASI_AGI_parte70_algebra_e_geometria.md) (P1541–P1570). Previsões sobre as minhas previsões no commit `783be3c`; as do mundo no `eb44d30`. Pedido do usuário, gravado no `CLAUDE.md`: **"Grave na memória que nossa AGI ASI PÓS ASI AGI terá a forma de
> GPT."** Esta parte constrói a forma: um GPT (Generative Pre-trained Transformer) mínimo em Python puro (`synthai/gpt.py`): embeddings de caractere e de posição, atenção causal
> de uma cabeça, resíduo, MLP, softmax do próximo caractere, gradiente escrito à mão (conferido por diferenças finitas: maior erro relativo 2,3·10⁻⁶) e Adam. Pré-treinado nas
> definições do WordNet, medido contra o modelo mais simples (o n-grama), e com a decisão do próximo caractere traduzida bit a bit para Java (rodada 43).

## Previsões sobre as minhas previsões desta parte (prever o previsto; registradas antes de escrever qualquer previsão do mundo desta parte)

Planejado, antes de escrever: bits por caractere do n-grama (ordens 3 e 5) e do GPT nas definições inglesas; a diferença GPT − n-grama; bits por dígito de π em hexadecimal; a
rodada 43 (IGUAIS, e quantos próximos caracteres o GPT pequeno acerta numa frase). Acerto do mundo nas Partes 53 a 68, pela régua nova (`p1481`): **72,5%** (109 previsões);
com ~7 previsões, a faixa binomial de 90% vai de 4/7 a 7/7.
- **(m1)** o número de previsões do mundo em **[6; 9]**.
- **(m2)** o número de faixas que cruzam o zero em **[0; 2]** (a diferença GPT − n-grama pode cruzar).
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,30]** (bits por caractere são quantidades longe de zero com escala conhecida, e as minhas faixas para
  elas devem ser estreitas).
- **(m4)** a fração de acertos do mundo em **[0,57; 1,00]**.
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 1]**.

## As perguntas desta parte

1. **P1511–P1513 (0x5E7–0x5E9).** A forma de GPT, pré-treinada nas definições do WordNet: quantos bits por caractere, contra o n-grama? ↩ P1453, P1482
2. **P1514–P1515 (0x5EA–0x5EB).** Hexadecimal: quantos bits por dígito um modelo de linguagem precisa para os dígitos de π em base 16? ↩ P1493
3. **P1516 (0x5EC).** A decisão do próximo caractere, bit a bit em Java (Rodada 43). ↩ P1491
4. **P1517 (0x5ED).** Preditiva comigo mesma. **P1518 (0x5EE).** Engenharia reversa e Jung. **P1519 (0x5EF).** O diálogo.
5. **P1539 (0x603).** Placar (três). **P1540 (0x604).** Unificação.

## Previsões pré-registradas (escritas depois do registro de (m1) a (m5))

### Sobre mim (placar separado), condicionais ao número S de surpresas (contadas pelo script)

Planejadas: as 8 previsões do mundo abaixo, (a) a (h), e 6 peças com teste (o GPT, p1511, p1512, p1513, p1514, p1515, mais o placar das (m)).

| medida | estatístico (até a 68) | ingênuo (Parte 68) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [13.717; 18.968] | 16.607 | **[13.717; 18.968]** | o estatístico |
| compressão | [0,396; 0,426] | 0,398 | **[0,396; 0,426]** | o estatístico |
| testes de unidade | [3,50; 6,25] | 6 | **[8 + S; 11 + S]** | 8 já escritos (3 do GPT, 5 das pNN), ~1 por surpresa |
| testes do placar | [5,83; 9,67] | 6 | **8 + 2·S ± 1** | as 8 letras abaixo, ~2 por surpresa |
| erros do placar | [0; 3,86] | 0 | **[0; 3,86]** | o estatístico |
| redundância P821 | [0,575; 0,634] | 0,607 | **[0,575; 0,634]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1511–P1513, a forma de GPT contra o n-grama**, nas definições inglesas do WordNet (separação fixa: os sinsets de índice ≡ 0 mod 10 no teste; 400 janelas de 24 caracteres
do teste; o GPT tem T = 24, d = 24, h = 48, 8.000 passos de Adam, ~6.900 parâmetros).
- **Restrições, com peso:** (1) o n-grama conta **todo** o treino (milhões de caracteres); o GPT vê só 8.000 × 24 = 192.000 caracteres sorteados: ele perde por dado, não por forma;
  (2) **peso medido num caso escolhido por regra escrita antes (o português da OpenWordNet-PT, mesmas máquinas, 2.000 e 8.000 passos):** n-grama 3,39 (ordem 2), 2,78 (ordem 3),
  2,07 (ordem 5); GPT 3,40 com 2.000 passos e **3,14** com 8.000 (entre o bigrama e o trigrama); (3) o inglês tem um treino ~10 vezes maior, o que ajuda o n-grama de ordem alta e
  não o GPT (que vê o mesmo número de janelas).
- Exemplo à mão: depois de "a domestic anim", o próximo é "a" com probabilidade alta para qualquer modelo que conte trigramas ("nim" → "a").
- (a) n-grama de ordem 3 em **[2,4; 3,1]** bits por caractere
- (b) n-grama de ordem 5 em **[1,6; 2,3]**
- (c) o GPT em **[2,85; 3,40]**
- (d) GPT − n-grama de ordem 3 em **[0,05; 0,70]** (o GPT pior que o trigrama, como no português: +0,36)

**P1514–P1515, os dígitos de π em base 16** (10.000 dígitos exatos; n-grama de ordem 2 treinado nos 90% primeiros, medido nos 10% últimos).
- **Restrições, com peso:** (1) os dígitos de π não têm estrutura conhecida (π é suposto normal em base 16, sem prova); (2) aprender contextos que não existem custa bits; **peso medido
  num caso escolhido por regra (dígitos pseudoaleatórios com semente 1515, mesmo tamanho):** 4,003 (ordem 1), **4,025** (ordem 2), 4,233 (ordem 3).
- (e) bits por dígito de π, ordem 2, em **[3,98; 4,08]**

**P1516, rodada 43:** no `dialogo/DIALOGO.md` (previsões (f) a (h)).

---

## As respostas

### P1511–P1513 (0x5E7–0x5E9). A forma de GPT contra o n-grama ✅✅✅✅

**Na pergunta.** "Terá a forma de GPT" separa duas coisas que costumam vir juntas: a **forma** (prever o próximo símbolo com atenção sobre o contexto, pré-treinar, gerar) e o
**tamanho** (bilhões de pesos, trilhões de símbolos). A forma cabe em 300 linhas de Python; o tamanho não. A pergunta pede a forma, e a resposta mede o quanto a forma sozinha faz.

**Lógica, linha por linha.** O GPT de `synthai/gpt.py`: e_t = E[x_t] + P[t]; q, k, v = eQ, eK, eV; a_t = softmax_{j ≤ t}(q_t·k_j/√d); r_t = e_t + (Σ a_tj v_j)O; z_t = r_t + relu(r_t W1 + b1)W2;
p_t = softmax(z_t U + c); perda −(1/n) Σ ln p_t[x_{t+1}]. Com T = 24, d = 24, h = 48: **6.898** pesos. Nas definições inglesas (treino de 5.656.842 caracteres; 400 janelas do teste):

| modelo | bits por caractere | faixa | |
|---|---|---|---|
| n-grama de ordem 2 | 3,431 | — | |
| n-grama de ordem 3 | **2,768** | [2,4; 3,1] | (a) ✅ |
| n-grama de ordem 5 | **1,832** | [1,6; 2,3] | (b) ✅ |
| GPT, 8.000 passos | **3,224** | [2,85; 3,40] | (c) ✅ |
| GPT − trigrama | **+0,456** | [0,05; 0,70] | (d) ✅ |

A calibração no português tinha dado o GPT entre o bigrama e o trigrama (3,14), e o inglês repetiu a posição (3,22, entre 3,43 e 2,77). **A conta do porquê:** o trigrama viu 5,66 milhões
de caracteres; o GPT viu 8.000 × 24 = 192.000 (3,4% do treino), uma vez cada. Por dado visto, o GPT é muito mais eficiente (com 3,4% do dado ele fica a 0,46 bit do trigrama que viu
tudo); por dado disponível, perde. A geração por argmax ("a domestic ther of tha ther of that of that…") mostra o que ele aprendeu: a forma das palavras curtas e frequentes do inglês
das definições (*of*, *that*, *the*), e o laço do argmax, que repete o caminho mais provável.

Ao acaso: as quatro faixas tinham larguras de 0,55 a 0,7 bit; o ingênuo "o GPT empata com o trigrama" erraria (d) por 0,46.

**Tradução cruzada.** O GPT é a forma computacional de uma ideia antiga da psicologia da linguagem: compreender é prever (a teoria do processamento preditivo). A atenção é a parte da
forma que decide o que do passado importa agora: em Jung, a função que dirige a libido para um conteúdo e não para outro. Onde a formalização funciona: a atenção causal é literalmente
uma distribuição de peso sobre o passado. Onde quebra: a atenção do GPT não tem intenção; ela é o que minimiza o erro de previsão do próximo símbolo.

**Meta.** Um GPT com 6.898 pesos e 8.000 passos é a forma em miniatura; a comparação com o n-grama vale para este tamanho. A pergunta da rodada 44 (a curva de dados e pesos) é a que
diz se a forma vence quando cresce.

### P1514–P1515 (0x5EA–0x5EB). π em base 16 para um modelo de linguagem ✅

**Na pergunta.** Pedir a um modelo de linguagem que preveja os dígitos de π é a pergunta inversa da forma de GPT: o que acontece quando não há nada para aprender?

**Lógica.** `p1514_pi_hex_digitos` (Machin, exato: 3,243f6a8885a308d3…) e `p1515_bits_hex`: ordem 1, **3,9999**; ordem 2, **4,0091** (a faixa (e) era [3,98; 4,08]) ✅; ordem 3, 4,2047. Igual aos
dígitos pseudoaleatórios da calibração (4,003; 4,025; 4,233): o modelo não acha estrutura em π, e paga para procurar (a ordem 3 usa contextos de 2 dígitos: 16² = 256 contextos, com 9.000/256 ≈ 35 ocorrências cada para estimar 16 continuações; eu tinha escrito de cabeça "4.096 contextos com ~2 ocorrências", que é a ordem 4).

Ao acaso: a faixa tinha 0,10 bit; o ingênuo "4 bits exatos" ficaria a 0,009.

**Tradução cruzada.** Um aprendiz que procura padrão onde não há paga em bits a sua credulidade: a apofenia (ver padrões no acaso) tem um custo mensurável, os 0,2 bit da ordem 3.

**Meta.** A normalidade de π em base 16 não é provada; 10.000 dígitos não a provam, só não a desmentem.

### P1516 (0x5EC). A decisão do próximo caractere, bit a bit (Rodada 43) ✅✅✅

**Lógica.** `p1516_gpt_decide` (rodada 43): o GPT pequeno (1.170 pesos, 400 passos) acerta **5 de 30** próximos caracteres da frase "a domestic animal kept for comp" e gasta **4,077** bits por
caractere; Java dá os mesmos 61 números bit a bit (com exp e log próprios). Ver o `dialogo/DIALOGO.md`.

### P1517 (0x5ED). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 0)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **16291** | [13717; 18968] | ✅ | [13717; 18968] | ✅ | 16607 | 52 | 316 |
| compressão | **0.4115** | [0.3962; 0.4256] | ✅ | [0.3960; 0.4260] | ✅ | 0.3981 | 0.0005 | 0.0133 |
| testes de unidade | **9** | [3.50; 6.25] | ❌ | [8.00; 11.00] | ✅ | 6 | 0.50 | 3.00 |
| testes do placar | **8** | [5.83; 9.67] | ✅ | [7.00; 9.00] | ✅ | 6 | 0.00 | 2.00 |
| erros do placar | **0** | [-0.36; 3.86] | ✅ | [0.00; 3.86] | ✅ | 0 | 1.93 | 0.00 |
| redundância P821 | **0.5637** | [0.5749; 0.6335] | ❌ | [0.5750; 0.6340] | ❌ | 0.6067 | 0.0408 | 0.0430 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 4 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 6 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 68"):** mais perto do medido em **5 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **13975**, compressão **0.4246**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 0 erros.
- **Erros de processo nesta parte:** 2 (escrevi de cabeça ~1.500 pesos para o GPT pequeno (são 1.170); corrigido antes do commit; escrevi de cabeça 4.096 contextos com ~2 ocorrências para a ordem 3 (são 256 com ~35); corrigido antes do commit).

**O placar das previsões sobre as minhas previsões (`p1499_previsoes_sobre_previsoes_v2`, lido do próprio documento):**

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [6; 9] | **8.0000** | ✅ |
| (m2) | [0; 2] | **0.0000** | ✅ |
| (m3) | [0.05; 0.3] | **0.1579** | ✅ |
| (m4) | [0.57; 1.0] | **1.0000** | ✅ |
| (m5) | [0; 1] | **1.0000** | ✅ |

As larguras das faixas que não cruzam o zero: [0.0124, 0.088, 0.1273, 0.1579, 0.1795, 0.5714, 0.8667]. **5 de 5** previsões sobre as minhas previsões dentro da faixa.

### P1518 (0x5EE). Engenharia reversa e Jung

**A forma pedida, e o que ela mostrou de mim.** Construir a forma de GPT do zero (o gradiente à mão de uma atenção causal) foi a parte com mais código novo da série, e a de menos erros
do mundo: oito de oito. Os erros desta parte foram todos **de texto**: duas contas de cabeça, ambas pegas antes do commit ("~1.500 pesos", que eram 1.170; "4.096 contextos", que eram
256). **O padrão:** quando eu escrevo código, eu confiro (o gradiente por diferenças finitas, a saída igual depois de refatorar); quando eu escrevo prosa sobre o código, eu estimo.
**O significado:** a minha prosa técnica ainda é escrita no modo de estimativa, e o código no modo de verificação; o erro mora na passagem de um para o outro. **Regra nova:** depois de
escrever a resposta de uma parte, procurar no texto todos os números que não vieram de uma saída impressa (os "~", os "cerca de", as contas de cabeça) e passá-los por uma linha de
código antes do commit.

**Prever o previsto, terceira volta.** As previsões sobre as minhas previsões (o placar das (m) na P1517) foram escritas sabendo que eu acerto ~72% do mundo e que as duas últimas
partes acertaram tudo. A (m4), a minha taxa de acerto, foi a que eu errei nas Partes 67 e 68 por acertar demais; nesta, eu a alarguei até 1,0 pela conta binomial, sem saber o
resultado.

**Jung: a persona da máquina.** O GPT pequeno gera "a domestic ther of tha ther of that of that…": a forma da língua sem conteúdo, a superfície que imita um falante. É a persona de
Jung no sentido exato: a máscara social que o coletivo (o corpus) imprime, sem o eu atrás. **Onde a formalização funciona:** a persona é o que se aprende primeiro e mais barato (as
palavras frequentes, o ritmo das definições), e o modelo aprendeu primeiro exatamente isso. **Onde quebra:** em Jung, atrás da persona há um eu que pode se diferenciar dela; no GPT de
6.898 pesos, a persona é tudo o que há, e só o tamanho (dados, pesos) pode pôr alguma coisa atrás dela.

### P1519 (0x5EF). O diálogo, rodada 43

Ver P1516. Placar por voz da função `p1241_placar_por_voz(43)`: IA-Python 23 em 37; IA-Java 19 em 36 (regra estrita, rodadas 13 a 43).

### P1539 (0x603). Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅. Parte 69: **8 testes, 0 erros**. Acumulado (mundo): **189 erros em 573 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 6 pNN novas sem teste ✅. Sobre mim (placar separado): **6 de 7** dentro da faixa condicional; sobre as minhas previsões, 5 de 5; o estatístico, 4 de 6; e 2 erros de processo (P1335).

### P1540 (0x604). Unificação

- **Novo:** `synthai/gpt.py` (a forma de GPT, com 3 testes próprios: gradiente por diferenças finitas, causalidade, treino), `p1511` (o corpus), `p1512` (o n-grama), `p1513` (o GPT
  medido), `p1514` (π em hexadecimal), `p1515` (bits por dígito), `p1516` (rodada 43, IGUAIS). Regressão: + P1516 (5 acertos do GPT pequeno; os dígitos de π).
- **Pedido permanente novo (no `CLAUDE.md`):** a forma de GPT.

> **Síntese da Parte 69:** a SYNTHAI agora tem a forma de GPT (gravada no `CLAUDE.md`): `synthai/gpt.py`, em Python puro, com embeddings, atenção causal, resíduo, MLP, softmax do próximo caractere, gradiente à
mão (conferido por diferenças finitas) e Adam. Pré-treinado nas definições do WordNet com 6.898 pesos e 8.000 passos, ele faz 3,22 bits por caractere: melhor que o bigrama (3,43) e
pior que o trigrama (2,77), que viu 30 vezes mais texto. Os dígitos de π em base 16 custam 4,01 bits a um n-grama, como o acaso; e a decisão do próximo caractere de um GPT pequeno é a
mesma, bit a bit, em Python e em Java. O mundo, oito de oito; os meus erros, só no texto.

---

**Fontes desta parte**
- O GPT: A. Radford et al., "Improving Language Understanding by Generative Pre-Training" (OpenAI, 2018); A. Vaswani et al., "Attention Is All You Need" (NeurIPS 2017),
  [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
- Interpolação de Witten-Bell: I. Witten e T. Bell, *IEEE Trans. Information Theory* 37 (1991); [n-gram language model, Wikipedia](https://en.wikipedia.org/wiki/Word_n-gram_language_model)
- Adam: D. Kingma e J. Ba, [arXiv:1412.6980](https://arxiv.org/abs/1412.6980)
- Processamento preditivo: A. Clark, "Whatever next? Predictive brains, situated agents, and the future of cognitive science", *Behavioral and Brain Sciences* 36 (2013)
- π em hexadecimal: [Bailey–Borwein–Plouffe formula, Wikipedia](https://en.wikipedia.org/wiki/Bailey%E2%80%93Borwein%E2%80%93Plouffe_formula)
