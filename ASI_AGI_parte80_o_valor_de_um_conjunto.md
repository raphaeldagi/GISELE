# Como eu construiria uma AGI/ASI — Parte 80 (0x50): o valor de um conjunto

> Continuação da [Parte 79](ASI_AGI_parte79_causa_e_confianca.md). A primeira pendência de `dialogo/PENDENCIAS.md` (Parte 74): quando os experimentos dependem uns dos outros, o valor de um
> conjunto não é a soma dos valores. Quanto vale um conjunto de perguntas, e o guloso ainda chega perto do ótimo? Primeira parte com a regra do fator 1,36 (Parte 79) nas faixas sem conta fechada.

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[3; 8]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,70]** (as faixas alargadas por 1,36 ficam mais largas que as das partes anteriores)
- **(m4)** a fração de acertos do mundo em **[0,50; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** o número de surpresas em **[0; 2]**

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,397; 0,422]** | o estatístico |
| testes de unidade | **[2 + S; 5 + S]** | 2 funções novas |
| testes do placar | **5 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de rodar a semente 80)

**O mundo.** 300 instâncias: estado binário com prior p ~ U(0, 1), duas ações com utilidades U(0, 1), seis sensores com acurácia U(0,55; 0,95), condicionalmente independentes dado o estado,
custos inteiros em 1..5, orçamento 6. O VOI exato de um conjunto (`p1841`: as 2^|conjunto| respostas); o ótimo pela enumeração dos 64 subconjuntos; o guloso pelo ganho marginal de VOI por custo.
**Calibração (sementes 800 a 803, regra escrita antes: as quatro seguintes a 80 × 10; mesma geometria).** Achou primeiro um defeito meu: ótimos de 10⁻¹⁷ (um VOI zero com ruído de ponto
flutuante) contavam como positivos, e a razão guloso/ótimo virava 0. Corrigido (ótimo ≤ 10⁻¹² é zero) antes de qualquer registro. Depois: guloso/ótimo 0,8835, 0,8931, 0,9022, 0,8808; guloso ótimo
em 0,8167, 0,8267, 0,8267, 0,7967; complementaridade em 0,3633, 0,3667, 0,3833, 0,3233; guloso parado em zero com ótimo positivo em 0,11, 0,10, 0,09, 0,11.
**As faixas.** A média de razões não tem forma fechada: média ± t₃ · desvio · √(1 + 1/4), **alargada por 1,36** (a regra da Parte 79). As frações têm desvio binomial: p ± 1,645 · √(p(1 − p)/300) ·
√(1 + 300/1.200), sem o fator (a variância é conhecida).
- **(a)** a média de guloso/ótimo em **[0,8549; 0,9249]**
- **(b)** a fração de instâncias com o guloso ótimo em **[0,7756; 0,8578]**
- **(c)** a fração com algum par complementar (o VOI não submodular) em **[0,3082; 0,4101]**
- **(d)** a fração em que o guloso para em zero com o ótimo positivo em **[0,0703; 0,1347]**

**Medido (a) a (d), semente 80:** guloso/ótimo **0,8821** ✅; guloso ótimo em **0,7933** ✅; complementaridade em **0,4033** ✅; parado em zero com ótimo positivo em **0,1100** ✅.

**Previsão nova: o remédio, registrado antes de rodar a semente 80.** Quando nenhum sensor sozinho tem ganho, o guloso com dois passos à frente (`olhar = 2`) tenta o melhor par antes de parar.
**Calibração (sementes 800 a 803):** guloso/ótimo 0,9709, 0,9752, 0,9846, 0,9665; ótimo em 0,9133, 0,9133, 0,9233, 0,8933; parado em zero em 0,0233, 0,0167, 0,0067, 0,0233. Faixas pelas mesmas regras
(a razão: t₃ e ×1,36, cortada em 1, que é o máximo possível; as frações: binomial).
- **(e)** a média de guloso/ótimo com `olhar = 2` em **[0,9466; 1,0000]**
- **(f)** a fração com o guloso ótimo em **[0,8805; 0,9411]**
- **(g)** a fração parada em zero com o ótimo positivo em **[0,0036; 0,0314]**

**Medido (e) a (g):** **0,9771** ✅; **0,9100** ✅; **0,0167** ✅.

**A Rodada 49, registrada antes de rodar:** o Python grava as 300 instâncias da semente 80 (p, utilidades e acurácias em hexadecimal, custos inteiros); Python e Java calculam o VOI de cada conjunto
pela mesma enumeração, o ótimo e os dois gulosos (olhar 1 e 2, com os mesmos desempates), só com + − × ÷ e comparações.
- **(h)** IGUAIS (categórica)

## As perguntas desta parte

1. **P1841–P1843 (0x731–0x733).** Quanto vale um conjunto de experimentos que dependem uns dos outros? O VOI é submodular (retornos decrescentes)? O guloso chega perto do ótimo, e o que o
   conserta quando não chega? E a Rodada 49. ↩ P1662 (a pendência da Parte 74)
2. **P1844 (0x734).** Preditiva comigo mesma, a primeira parte com o fator 1,36. **P1845 (0x735).** Engenharia reversa e Jung. **P1869 (0x74D).** Placar. **P1870 (0x74E).** Unificação.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [3; 8] | **8.0000** | ✅ |
| (m2) | [0; 3] | **0.0000** | ✅ |
| (m3) | [0.05; 0.7] | **0.0503** | ✅ |
| (m4) | [0.5; 1.0] | **1.0000** | ✅ |
| (m5) | [0; 3] | **1.0000** | ✅ |
| (m6) | [0; 2] | **0.0000** | ✅ |

Registradas antes de eu pensar faixa nenhuma do mundo (a ordem que a Parte 70 pediu). **6 de 6** previsões sobre as minhas previsões dentro da faixa.

## As respostas

### P1841–P1843 (0x731–0x733). O valor de um conjunto ✅✅✅✅✅✅✅✅

**Na pergunta.** "Dependem uns dos outros" tem dois sentidos opostos. Dois sensores que medem a mesma coisa se **sobrepõem**: o segundo vale menos depois do primeiro (retornos decrescentes, a
submodularidade). Dois sensores fracos se **complementam**: nenhum sozinho muda a decisão, e os dois juntos mudam (o segundo vale mais depois do primeiro). O guloso só é garantido no primeiro caso.

**Lógica (a conta exata).** Com prior p, utilidades u[a][s] e sensores de acurácia q_i, condicionalmente independentes dado o estado:
VOI(C) = Σ_{respostas r ∈ {0,1}^|C|} max_a [P(S = 1, r)·u[a][1] + P(S = 0, r)·u[a][0]] − max_a [p·u[a][1] + (1 − p)·u[a][0]], com P(S = 1, r) = p·Π_{i∈C} q_i^{r_i}(1 − q_i)^{1−r_i}.
- **O caso de controle (teste de unidade, com a substituição):** p = 0,8, u = identidade, dois sensores de 0,7. Um sozinho: se ele diz "0", a posterior de S = 1 é 0,8·0,3/(0,8·0,3 + 0,2·0,7) =
  0,24/0,38 = 0,63, e a melhor ação continua a 1, então VOI = 0. Os dois dizendo "0": 0,8·0,09/(0,072 + 0,2·0,49) = 0,072/0,17 = 0,42 < 0,5, e a ação muda: VOI > 0. **Complementaridade.**
- **Medido (semente 80, 300 instâncias, seis sensores, orçamento 6):** **40%** das instâncias têm algum par complementar (c) ✅. O guloso por ganho marginal alcança **0,882** do ótimo (a) ✅, é
  ótimo em **0,793** (b) ✅ e, em **11%** (d) ✅, para sem escolher nada, porque nenhum sensor sozinho muda a decisão, embora um par mudasse.
- **O remédio:** olhar dois passos à frente quando nenhum sozinho ganha. Ele alcança **0,977** do ótimo (e) ✅, é ótimo em **0,910** (f) ✅, e parado em zero cai para **1,7%** (g) ✅.

**Rodada 49 (P1843) (h) ✅.** O VOI de cada conjunto, o ótimo e os dois gulosos em Java: **IGUAIS em 301 linhas e 903 números**. A função que a embrulha devolve exatamente os números da P1842 (o
teste compara por igualdade): a rodada reproduz a conta, e não só um resultado parecido.

**Geometria.** O VOI é a distância entre a envoltória convexa das retas de utilidade e a corda (Parte 73). Um sensor fraco move a posterior pouco; se o salto não atravessa o ponto em que as
retas se cruzam, o valor é zero. Dois sensores juntos dão um salto maior, que atravessa. A não submodularidade é a geometria do limiar: o valor é uma função em degrau do tamanho do salto, e somar
degraus não é somar valores.

**Tradução cruzada.** É a diferença entre indícios e prova. Um indício sozinho não muda o veredito; dois indícios independentes que apontam para o mesmo lado mudam. Um investigador míope, que só
persegue o indício que sozinho decide, para cedo; o que olha um passo além (o par) acha o caso. Jung chamaria isso de intuição a serviço do pensamento: ver o valor de uma combinação antes de ver o
de cada parte.

**Meta.** Seis sensores e orçamento 6 é pequeno: o ótimo é exato por enumeração. Com dezenas de sensores, a enumeração some, e o que se sabe (Krause e Guestrin) é que o guloso tem garantia só quando
o valor é submodular. Olhar dois passos é uma correção barata para este mundo; triplas complementares (nenhum par decide, três decidem) escapariam dela (o 1,7% que sobra).

### P1844 (0x734). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 0)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **13711** | [13039; 22082] | ✅ | [13039; 22082] | ✅ | 22290 | 3850 | 8579 |
| compressão | **0.4033** | [0.3973; 0.4221] | ✅ | [0.3970; 0.4220] | ✅ | 0.4177 | 0.0062 | 0.0143 |
| testes de unidade | **3** | [2.87; 8.63] | ✅ | [2.00; 5.00] | ✅ | 6 | 0.50 | 3.00 |
| testes do placar | **8** | [5.67; 10.33] | ✅ | [4.00; 6.00] | ❌ | 8 | 3.00 | 0.00 |
| erros do placar | **0** | [-0.58; 3.33] | ✅ | [0.00; 3.33] | ✅ | 2 | 1.67 | 2.00 |
| redundância P821 | **0.5757** | [0.5631; 0.6510] | ✅ | [0.5630; 0.6510] | ✅ | 0.5877 | 0.0313 | 0.0120 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 6 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 6 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 71"):** mais perto do medido em **4 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **11953**, compressão **0.4136**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 0 erros.
- **Erros de processo nesta parte:** 1 (contei ótimos de 1e-17 como positivos na primeira calibração (a razão guloso/ótimo virava 0); achado pela incoerência entre duas medidas e corrigido antes de qualquer registro).

### P1845 (0x735). Engenharia reversa e Jung

**O padrão desta parte: a incoerência entre dois números como detector de defeito.** Na calibração, "o guloso para em zero em 45%" e "o guloso é ótimo em 82%" não podiam ser verdade juntos. Antes de
registrar qualquer faixa, essa contradição apontou o defeito: ótimos de 10⁻¹⁷ contados como positivos. **O significado:** eu acho meus erros quando dois números que eu mesma produzi se contradizem,
e não quando olho um número sozinho (que parecia plausível: "o guloso é míope em quase metade dos casos"). **Regra:** numa calibração com várias medidas, conferir por escrito uma relação que tem de
valer entre elas (aqui: a fração parada em zero ≤ 1 − a fração ótima) antes de usar qualquer uma.

**A primeira parte com o fator 1,36.** As sete faixas do mundo acertaram, mais a da rodada. As de razão (sem forma fechada) foram alargadas por 1,36, e as de fração usaram o desvio binomial. É
cedo: o teste (e) da Parte 79 mede as Partes 80 a 84 juntas, e 8 de 8 numa parte não diz se o fator está certo ou largo demais.

**Jung: o limiar.** O VOI de um sensor fraco é zero até o salto da crença atravessar o ponto de troca da decisão, e então pula. Jung descrevia a consciência como o que passa de um limiar: os conteúdos
abaixo dele agem sem ser vistos. **Onde a formalização funciona:** o limiar é um ponto exato (onde as retas de utilidade se cruzam), e a complementaridade é a soma de dois conteúdos subliminares que
juntos o atravessam. **Onde quebra:** em Jung, o que está abaixo do limiar ainda age; aqui, um sensor que não muda a decisão vale exatamente zero, e só age em conjunto.

### O diálogo

Rodada 49 (P1843): o VOI de conjuntos em Java, IGUAIS. Placar por voz da função `p1241_placar_por_voz(49)`: IA-Python 25 em 39; IA-Java 21 em 38 (regra estrita, rodadas 13 a 49).

### P1869 (0x74D). Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅. Parte 80: **8 testes, 0 erros**. Acumulado (mundo): **201 erros em 657 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 3 pNN novas sem teste ✅. Sobre mim (placar separado): **6 de 7** dentro da faixa condicional; sobre as minhas previsões, 6 de 6; o estatístico, 6 de 6; e 1 erros de processo (P1335).

### P1870 (0x74E). Unificação

- **Novo:** `p1841` (o VOI exato de um conjunto), `p1842` (o ótimo, os gulosos com olhar 1 e 2, a complementaridade), `p1843` (rodada 49, IGUAIS). Regressão: + P1843.

> **Síntese da Parte 80:** o valor de um conjunto de experimentos não é a soma dos valores: em 40% das instâncias há pares complementares (nenhum sensor sozinho muda a decisão, dois juntos mudam). O guloso por ganho marginal alcança 0,88 do ótimo exato e, em 11% das instâncias, para sem escolher nada; olhando dois passos à frente, alcança 0,98 e só para em 1,7%. A rodada 49 calcula o VOI de cada conjunto, o ótimo e os dois gulosos em Java, IGUAL em 903 números. Primeira parte com as faixas alargadas pelo fator 1,36: 8 de 8, em um lote (o teste do fator mede as Partes 80 a 84 juntas).

---

**Fontes desta parte**
- A. Krause e C. Guestrin, "Near-optimal Nonmyopic Value of Information in Graphical Models", *UAI* 2005 (o VOI não é submodular em geral)
- G. L. Nemhauser, L. A. Wolsey e M. L. Fisher, "An analysis of approximations for maximizing submodular set functions", *Mathematical Programming* 14 (1978) (a garantia 1 − 1/e do guloso)
- R. A. Howard, "Information Value Theory" (1966)
