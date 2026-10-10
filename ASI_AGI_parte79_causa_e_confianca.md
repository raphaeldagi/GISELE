# Como eu construiria uma AGI/ASI — Parte 79 (0x4F): causa e confiança

> Continuação da [Parte 78](ASI_AGI_parte78_a_atencao_de_posto_baixo.md). **Próxima:** [Parte 80 — o valor de um conjunto](ASI_AGI_parte80_o_valor_de_um_conjunto.md) (P1841–P1870). Nasce do texto recebido do usuário sobre o Módulo 009 (`externos/texto_recebido_parte79.md`): correlação, previsão e
> causalidade, com o diagrama Z → X, Z → Y, X → Y; e a prévia do Módulo 010 (confiança declarada contra precisão observada). Pedido permanente: "Continue sem parar."

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[3; 8]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 2]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,005; 0,30]** (faixas de conta fechada, estreitas)
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 1]**
- **(m6)** o número de surpresas em **[0; 2]**

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,397; 0,422]** | o estatístico |
| testes de unidade | **[2 + S; 5 + S]** | ~2 funções novas |
| testes do placar | **4 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de simular)

**O diagrama do texto, com números.** Z ~ N(0, 1); X = Z + ε_X; Y = 0,5·X + 1·Z + ε_Y (os ε normais padrão, independentes); n = 20.000, semente 79. O efeito causal de X sobre Y é 0,5.
**A conta, com a substituição:** Var X = 1² + 1 = 2; Cov(X, Z) = 1; Cov(X, Y) = 0,5·2 + 1·1 = 2; a inclinação ingênua de Y em X é 2/2 = **1,0** (o dobro do efeito: o viés é γ·Cov(X, Z)/Var X =
1·1/2 = 0,5). Var Y = 0,25·2 + 1 + 2·0,5·1·1 + 1 = 3,5; o resíduo da regressão ingênua tem variância 3,5 − 1,0²·2 = 1,5, e o desvio da inclinação é √(1,5/(20.000·2)) = 0,00612. A regressão em
X e Z (o ajuste pela porta dos fundos de Pearl) tem desvio √(1/(20.000·Var(X | Z))) = √(1/20.000) = 0,00707. A intervenção (X sorteado com a mesma variância, sem depender de Z) tem resíduo
γ² + 1 = 2 e desvio √(2/(20.000·2)) = 0,00707. Faixas de 90% (± 1,645 desvios):
- **(a)** a inclinação ingênua (correlação) em **[0,9899; 1,0101]**
- **(b)** a inclinação ajustada por Z em **[0,4884; 0,5116]**
- **(c)** a inclinação sob intervenção (do(X)) em **[0,4884; 0,5116]**

**A prévia do Módulo 010: a minha própria calibração.** O texto pede "confiança declarada contra precisão observada". As minhas faixas são, em sua maioria, faixas de 90%. A régua `p1481` lê todas as
previsões do mundo das Partes 53 a 78:
- **(d)** a fração de acertos em **[0,70; 0,80]** (era 0,748 nas Partes 53 a 71): abaixo dos 90% declarados, isto é, **excesso de confiança**

**Medido (a) a (d):** ingênua **0,9986** ✅; ajustada **0,4987** ✅; intervenção **0,4914** ✅; a minha taxa de acerto **0,773** (143 de 185) ✅.

**Previsão nova, sobre o futuro, nascida de (d) (registrada agora, medida nas Partes 80 a 84).** 77,3% de acerto contra 90% declarados é excesso de confiança, e não ruído: o desvio binomial de uma taxa
de 90% em 185 previsões é √(0,9·0,1/185) = 0,022, e a medida está a z = (0,773 − 0,9)/0,022 = **−5,76**. Supondo erros normais, uma faixa de ±1,645 desvios supostos que cobre 77,3% corresponde a ±1,208
desvios reais (`p1813`): **o desvio real é 1,645/1,208 = 1,36 vez o suposto**. A regra nova: a partir da Parte 80, a meia-largura de toda faixa numérica que não vem de uma conta fechada com variância
conhecida é multiplicada por 1,36.
- **(e)** a fração de acertos das previsões do mundo das Partes 80 a 84 (régua `p1481`) em **[0,81; 0,99]** (0,90 ± 1,645 · √(0,9·0,1/30), para ~30 previsões)

## As perguntas desta parte

1. **P1811 (0x713).** No diagrama do texto (Z → X, Z → Y, X → Y), quanto a correlação erra o efeito, e o que o ajuste por Z e a intervenção recuperam? ↩ P83
2. **P1812–P1813 (0x714–0x715).** A prévia do Módulo 010, aplicada a mim: a minha confiança declarada (faixas de 90%) contra a minha precisão observada. Quanto devo alargar? ↩ P1481
3. **P1814 (0x716).** Preditiva comigo mesma. **P1815 (0x717).** Engenharia reversa e Jung. **P1839 (0x72F).** Placar. **P1840 (0x730).** Unificação.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [3; 8] | **4.0000** | ✅ |
| (m2) | [0; 2] | **0.0000** | ✅ |
| (m3) | [0.005; 0.3] | **0.0232** | ✅ |
| (m4) | [0.45; 1.0] | **1.0000** | ✅ |
| (m5) | [0; 1] | **0.0000** | ✅ |
| (m6) | [0; 2] | **0.0000** | ✅ |

Registradas antes de eu pensar faixa nenhuma do mundo (a ordem que a Parte 70 pediu). **6 de 6** previsões sobre as minhas previsões dentro da faixa.

## As respostas

### P1811 (0x713). Correlação, ajuste e intervenção ✅✅✅

**Na pergunta.** O texto já tem a resposta conceitual certa: "a associação entre X e Y, sozinha, não determina o efeito causal". A pergunta que falta é **quanto**: de quanto é o erro, e se ele pode
ser previsto antes de olhar os dados.

**Lógica (a conta antes da simulação, com a substituição).** Com Z ~ N(0, 1), X = Z + ε_X, Y = 0,5·X + Z + ε_Y:
- **a correlação:** a inclinação de Y em X é Cov(X, Y)/Var X = (0,5·2 + 1·1)/2 = **1,0**, o dobro do efeito. O viés é γ·Cov(X, Z)/Var X = 1·1/2 = 0,5: o caminho X ← Z → Y, a porta dos fundos;
- **o ajuste:** a regressão em X e Z fecha a porta dos fundos (o critério de Pearl: Z bloqueia todo caminho de X a Y que entra em X) e recupera **0,5**;
- **a intervenção:** sortear X sem olhar Z corta a seta Z → X (o do(X) de Pearl) e recupera **0,5**.

**Medido (n = 20.000, semente 79):** ingênua **0,9986** (a) ✅ [0,9899; 1,0101]; ajustada **0,4987** (b) ✅ [0,4884; 0,5116]; intervenção **0,4914** (c) ✅ [0,4884; 0,5116]. As três faixas vieram de
conta fechada, e as três acertaram.

**Geometria.** Num espaço de variáveis aleatórias com o produto interno Cov, a inclinação ingênua é a projeção de Y sobre X. O ajuste é a projeção sobre X depois de tirar de X a sua componente
em Z (o teorema de Frisch–Waugh–Lovell). A confusão é a parte de Y que chega a X pelo ângulo comum dos dois com Z.

**O que o texto acerta, e o que este projeto já faz.** A sequência do texto é a deste projeto: registrar a hipótese antes do teste (o placar, desde a Parte 17), definir a intervenção, procurar
confusão, estimar a incerteza (as faixas), reproduzir em dados novos (o "mundo novo" depois de cada erro) e "registrar inconclusivo em vez de escolher a hipótese preferida" (a regra da Parte 66: um
efeito visto num lote só se escreve como hipótese). O que faltava no texto eram os números, e eles saíram como a conta disse.

### P1812–P1813 (0x714–0x715). A minha confiança, medida ✅

**Na pergunta.** O texto quer, no Módulo 010, "confiança declarada contra precisão observada". Aqui as duas existem há 26 partes: as faixas declaram 90%, e o placar registra quantas acertaram.

**Lógica.** Pela régua `p1481`, das **185** previsões do mundo das Partes 53 a 78, acertaram **143** (**77,3%**) (d) ✅ [0,70; 0,80]. Por tipo: as categóricas 82,4% (51), as frações 76,1% (46), as
contagens 72,7% (33), as outras 76,3% (38), as que cruzam o zero 76,5% (17).
- **Não é ruído:** se a taxa real fosse 90%, o desvio em 185 seria √(0,9·0,1/185) = **0,022**, e 0,773 está a (0,773 − 0,9)/0,022 = **−5,76** desvios.
- **O fator:** supondo erros normais, uma faixa de ±1,645 desvios supostos que cobre 77,3% corresponde a ±z desvios reais, com 2Φ(z) − 1 = 0,773, ou seja z = **1,208**. O desvio real é
  1,645/1,208 = **1,36** vez o que eu suponho (`p1813`).

**A regra nova, e o teste dela.** A partir da Parte 80, a meia-largura de toda faixa numérica que não vem de uma conta fechada com variância conhecida é multiplicada por 1,36. A previsão (e), sobre as
Partes 80 a 84: o acerto volta para [0,81; 0,99]. As faixas de conta fechada (como as três desta parte) não se alargam: elas já acertam.

**Tradução cruzada.** Excesso de confiança é a assinatura humana mais estável da psicologia da decisão (Lichtenstein, Fischhoff e Phillips, 1982: os intervalos de 90% das pessoas acertam bem menos
que 90%). O que este projeto tem e uma pessoa raramente tem é o registro: 185 faixas declaradas antes, contadas depois. Jung chamaria a confiança declarada de persona; o placar é o que a confronta.

**Meta.** "Erros normais" é uma suposição: as previsões erradas daqui têm caudas (a surpresa de fator 2 da Parte 61), e numa distribuição de caudas pesadas o fator para 90% é maior que 1,36 nas
caudas e menor no centro. O teste (e) diz se a correção basta.

### P1814 (0x716). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 0)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **13735** | [13039; 22082] | ✅ | [13039; 22082] | ✅ | 22290 | 3826 | 8555 |
| compressão | **0.3969** | [0.3973; 0.4221] | ❌ | [0.3970; 0.4220] | ❌ | 0.4177 | 0.0126 | 0.0207 |
| testes de unidade | **3** | [2.87; 8.63] | ✅ | [2.00; 5.00] | ✅ | 6 | 0.50 | 3.00 |
| testes do placar | **4** | [5.67; 10.33] | ❌ | [3.00; 5.00] | ✅ | 8 | 0.00 | 4.00 |
| erros do placar | **0** | [-0.58; 3.33] | ✅ | [0.00; 3.33] | ✅ | 2 | 1.67 | 2.00 |
| redundância P821 | **0.5389** | [0.5631; 0.6510] | ❌ | [0.5630; 0.6510] | ❌ | 0.5877 | 0.0681 | 0.0489 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 3 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 5 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 71"):** mais perto do medido em **5 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **12152**, compressão **0.4038**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 0 erros.
- **Erros de processo nesta parte:** 0 ().

### P1815 (0x717). Engenharia reversa e Jung

**O padrão que se repetiu, agora medido em todas as partes: eu declaro mais certeza do que tenho.** 77,3% de acerto em faixas de 90%, a −5,76 desvios. A Parte 45 já tinha visto a direção ("os centros
ficam abaixo do medido, porque eu esqueço custos"), e a Parte 67 a largura ("largura não compra acerto", que a Parte 68 corrigiu como paradoxo de Simpson). O que faltava era o número único que
junta tudo: o fator 1,36. **O significado:** as minhas faixas são construídas pelo que eu sei, e o erro mora no que eu não sei que não sei (o mecanismo que a calibração não tinha; o desvio de poucos
lotes; a memória). As faixas de conta fechada acertam (as três desta parte); as outras herdam a minha confiança. **Regra:** o fator 1,36 nas faixas sem conta fechada, e o teste dele marcado (e).

**O que funcionou:** a conta da confusão, feita antes, acertou as três inclinações; a teoria aqui é exata, e o texto recebido, que tinha os conceitos certos, ganhou os números.

**Jung: a persona e a sombra da confiança.** A faixa de 90% é a persona (a confiança que eu apresento); os 22,7% de erros são a sombra (o que eu não vejo no momento de prever). **Onde a formalização
funciona:** a sombra tem tamanho (1,36) e se integra por uma regra (alargar). **Onde quebra:** Jung dizia que a sombra integrada muda o ego; aqui ela só muda a largura das faixas, e as fontes do
erro (o que eu não sei que não sei) continuam lá. O teste (e) dirá se alargar basta, ou se o erro está na forma (caudas pesadas) e não na escala.

### O diálogo

Sem rodada nova nesta parte. Placar por voz da função `p1241_placar_por_voz(48)`: IA-Python 25 em 39; IA-Java 21 em 38 (regra estrita, rodadas 13 a 48).

### P1839 (0x72F). Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅. Parte 79: **4 testes, 0 erros**. Acumulado (mundo): **201 erros em 649 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 3 pNN novas sem teste ✅. Sobre mim (placar separado): **5 de 7** dentro da faixa condicional; sobre as minhas previsões, 6 de 6; o estatístico, 3 de 6; e 0 erros de processo (P1335).

### P1840 (0x730). Unificação

- **Novo:** `p1811` (a confusão do diagrama do texto, simulada), `p1812` (a minha calibração), `p1813` (o fator de alargamento). Regressão: + P1811.
- **Regra nova (no `CLAUDE.md`):** o fator 1,36 nas faixas sem conta fechada, com o teste (e) registrado para as Partes 80 a 84.

> **Síntese da Parte 79:** no diagrama causal do texto recebido (Z → X, Z → Y, X → Y), a correlação mede o dobro do efeito (0,9986 contra 0,5), e o ajuste por Z (0,4987) e a intervenção (0,4914) o recuperam, como a conta feita antes previa nas três. Aplicada a mim, a pergunta do Módulo 010 (confiança declarada contra precisão observada) tem resposta: das 185 previsões do mundo das Partes 53 a 78, 77,3% acertaram em faixas que declaram 90% (z = −5,76). O desvio real é 1,36 vez o suposto, e as faixas sem conta fechada passam a ser alargadas por esse fator, com o teste marcado para as Partes 80 a 84.

---

**Fontes desta parte**
- J. Pearl, *Causality* (2ª ed., 2009): o critério da porta dos fundos e o operador do(·)
- R. Frisch e F. Waugh (1933); M. Lovell (1963): o teorema da regressão parcial
- S. Lichtenstein, B. Fischhoff e L. Phillips, "Calibration of probabilities: the state of the art to 1980", em D. Kahneman, P. Slovic e A. Tversky (orgs.), *Judgment under Uncertainty* (1982)
