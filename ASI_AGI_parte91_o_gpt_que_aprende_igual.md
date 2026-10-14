# Como eu construiria uma AGI/ASI — Parte 91 (0x5B): o GPT que aprende igual

> Continuação da [Parte 90](ASI_AGI_parte90_a_rede_que_aprende_igual.md). **Próxima:** [Parte 92 — o Adam e a fronteira do pow](ASI_AGI_parte92_o_adam_e_a_fronteira_do_pow.md). Sem texto novo do usuário: sigo o ciclo. A Parte 90 mostrou que a rede PULSADA que aprende (STDP) é idêntica bit a bit entre Python e
> Java. A pergunta mais funda (↩ P69, rodada 43): e a OUTRA forma de aprendizado da SYNTHAI, o gradiente do GPT? A rodada 43 mostrou a decisão do próximo caractere igual bit a bit na inferência CONGELADA;
> esta parte pergunta pelo passo de TREINO — quando o gradiente muda os pesos, a decisão nova sai idêntica?
>
> **O escopo honesto (regra da Parte 72: traduzir um módulo real, mas o mínimo que prova a tese).** O passo de treino completo do GPT (Adam, com `pow` na correção de viés — a fronteira da Parte 52 — e 100
> linhas de backprop) seria grande e frágil de traduzir bit a bit. Então traduzo o CORAÇÃO de todo passo de treino de um GPT: o gradiente da softmax com entropia cruzada (∂L/∂logits = p − onehot), um passo
> de descida (SGD) e a decisão nova. É a peça que a camada de saída de qualquer GPT tem, usa exp e log (a fronteira), e decide se o treino muda a escolha.
>
> **A âncora algébrica (Parte 70):** o gradiente da entropia cruzada sobre a softmax é exatamente p − onehot(alvo) — uma das identidades mais limpas do aprendizado. Começo por ela (forma fechada), conferida
> contra o gradiente escrito à mão do `synthai/gpt.py` por diferenças finitas.

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
| testes de unidade | **[3 + S; 7 + S]** | a rodada e as medidas do GPT |
| testes do placar | **6 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

A âncora é a identidade p − onehot (forma fechada); a (c) foi calibrada num teste de fumaça (GPT minúsculo, padrão repetido) e prevê a execução canônica. Categóricas e formas fechadas não levam o fator 1,36.

- **(a)** a rodada 58 — o gradiente softmax+entropia cruzada, o passo de SGD e a decisão nova — dá os mesmos números bit a bit em Python e Java, com exp/log próprios (categórico: IGUAL)
- **(b)** o passo de SGD DIMINUI a perda: nos 5 casos da rodada, a perda depois do passo é menor que antes (categórico: a descida de gradiente na camada de saída, que é convexa, sempre reduz a perda para um passo pequeno)
- **(c)** o GPT real (`synthai/gpt.py`) minúsculo (d = 8, h = 8, T = 8), treinado 60 passos num padrão repetido "abc…", MEMORIZA o padrão: a perda final em **[0,0; 0,10]** (de ~1,07 inicial)
- **(d)** o gradiente da entropia cruzada sobre a softmax é EXATAMENTE p − onehot(alvo): o máximo |numérico − analítico| por diferenças finitas em **[0; 1e−6]** (categórico/forma fechada)
- **(e)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80–91 em **[0,74; 0,88]**

## As perguntas desta parte

1. **P2171 (0x87B).** O coração de um passo de treino de GPT (gradiente, descida, decisão) é idêntico bit a bit entre Python e Java? ↩ P69, rodada 43 (a inferência congelada)
2. **P2172 (0x87C).** O passo de descida reduz a perda? ↩ P2142 (a deriva da STDP)
3. **P2173 (0x87D).** O gradiente da entropia cruzada sobre a softmax tem forma fechada? ↩ P70 (álgebra)
4. **P2174 (0x87E).** O GPT real aprende (memoriza) um padrão? ↩ P69 (a forma de GPT)
5. **A rodada 58.** O passo de treino do GPT, bit a bit.
6. **P1961 (continuando), P2199–P2200.** O teste (e), engenharia reversa, placar, unificação.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [4; 8] | **4.0000** | ✅ |
| (m2) | [0; 3] | **2.0000** | ✅ |
| (m3) | [0.05; 0.8] | **indefinida (nenhuma faixa numérica: a p1481 não conta as categóricas como faixas)** | ❌ |
| (m4) | [0.45; 1.0] | **1.0000** | ✅ |
| (m5) | [0; 3] | **0.0000** | ✅ |
| (m6) | [0; 3] | **0.0000** | ✅ |

Registradas antes de eu pensar faixa nenhuma do mundo (a ordem que a Parte 70 pediu). **5 de 6** previsões sobre as minhas previsões dentro da faixa.

## As respostas

### P2171 / rodada 58 (0x87B). O treino do GPT é idêntico bit a bit ✅

**Na pergunta.** A rodada 43 mostrou a decisão do próximo caractere igual bit a bit na inferência CONGELADA. A pergunta funda: e quando um passo de TREINO muda os pesos — o gradiente, a descida, a decisão nova
— isso ainda é idêntico? A resposta condicional está na própria estrutura: se o gradiente e a descida usarem só +, −, ×, ÷ e o exp/log próprios (a fronteira da Parte 52), na mesma ordem (Partes 34/85), é
determinístico e idêntico.

**Medido.** O coração de todo passo de treino de GPT — p = softmax(logits) (exp próprio), perda = −ln p[alvo] (log próprio), gradiente = p − onehot(alvo), passo de SGD, decisão = argmax — em 5 casos: **IGUAIS,
30 números bit a bit** (a) ✅. O passo de treino, como a inferência, é independente de linguagem. A camada pulsada (Parte 90, STDP) e a camada GPT (gradiente) — as duas formas de aprendizado da SYNTHAI — agora
estão provadas idênticas entre as línguas no ato de aprender, não só no de decidir.

### P2172 (0x87C). A descida reduz a perda ✅

Nos 5 casos, a perda depois do passo de SGD é menor que antes: **[V, V, V, V, V]** (b) ✅. A camada de saída (softmax + entropia cruzada) é CONVEXA nos logits, então um passo de gradiente pequeno sempre reduz a
perda — a garantia que a STDP (Parte 90) não tem (lá o "aprendizado" só decai a norma; aqui ele desce uma função objetivo definida). É a diferença entre aprendizado por correlação (Hebb/STDP) e por objetivo
(gradiente): só o segundo tem uma perda que se prova cair.

### P2173 (0x87D). O gradiente é p − onehot ✅

**Álgebra (Parte 70).** A identidade mais limpa do aprendizado supervisionado: ∂/∂z [−ln softmax(z)[t]] = softmax(z) − onehot(t). Conferida contra as diferenças finitas: máximo |numérico − analítico| =
**1,9 × 10⁻¹⁰** (d) ✅. É por isso que o passo da rodada 58 é tão simples (logits −= lr·(p − onehot)): o erro da predição É o gradiente. **Geometria:** p vive no simplex (soma 1); p − onehot é o vetor que aponta
de onde a rede está para o vértice onde ela deveria estar, e a descida caminha nessa direção.

### P2174 (0x87E). O GPT real memoriza ✅

O `synthai/gpt.py` minúsculo (d = 8, h = 8, T = 8), treinado 60 passos num padrão repetido "abc…": a perda cai de **1,075** para **0,0** (c) ✅ [0,0; 0,10] — ele memoriza o padrão (com vocabulário de 3 e um padrão
periódico, a perda mínima é 0). É a forma de GPT da Parte 69 funcionando: o mesmo mecanismo (atenção causal, softmax, entropia cruzada, gradiente à mão) que a Parte 69 mediu em 3,22 bits/caractere no dicionário,
aqui leva a perda a zero num padrão trivial. A capacidade é a que a medida mostra: memorizar "abc" é fácil; o dicionário é duro.

### A rodada 58 ✅

O passo de treino do GPT, 5 casos: **IGUAIS, 30 números bit a bit** (exp/log próprios). Registro em `dialogo/DIALOGO.md`. Fecha a pendência da Parte 90 (o GPT aprende igual, não só decide igual).

### P1961 (0x7A9). O teste (e) da calibração ✅

Com a Parte 91, o acerto das Partes 80–91 é **49/61 = 0,803** (e) ✅ [0,74; 0,88]. Subiu de 0,789. Quatro partes seguidas (88–91), todas de conta fechada, substrato e não-efeito previsto, acertaram 16 de 16 do
mundo: a calibração atravessou 0,80 pela primeira vez desde a queda das Partes 84/87. A régua pegou.

### P2199 (0x897). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 0)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **14049** | [13039; 22082] | ✅ | [13039; 22082] | ✅ | 22290 | 3512 | 8241 |
| compressão | **0.3959** | [0.3973; 0.4221] | ❌ | [0.3920; 0.4200] | ✅ | 0.4177 | 0.0101 | 0.0218 |
| testes de unidade | **5** | [2.87; 8.63] | ✅ | [3.00; 7.00] | ✅ | 6 | 0.00 | 1.00 |
| testes do placar | **4** | [5.67; 10.33] | ❌ | [5.00; 7.00] | ❌ | 8 | 2.00 | 4.00 |
| erros do placar | **0** | [-0.58; 3.33] | ✅ | [0.00; 3.33] | ✅ | 2 | 1.67 | 2.00 |
| redundância P821 | **0.6689** | [0.5631; 0.6510] | ❌ | [0.5630; 0.6510] | ❌ | 0.5877 | 0.0619 | 0.0812 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 3 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 5 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 71"):** mais perto do medido em **6 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **12466**, compressão **0.3995**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 0 erros.
- **Erros de processo nesta parte:** 0 ().

### P2200 (0x898). Engenharia reversa e Jung

**O padrao desta parte: a conta fechada fecha o laco.** A P2173 (gradiente = p - onehot) e a identidade que torna o passo de treino trivial de escrever e de verificar - e, de novo, foi a previsao de conta fechada que
acertou sem risco. Quatro partes (88-91) so com conta fechada, substrato e nao-efeito previsto: 16/16 do mundo. A engenharia reversa do meu proprio placar: a calibracao subiu de 0,74 (Parte 84) para 0,80 (Parte 91)
na exata medida em que eu parei de apostar na reputacao de efeitos e passei a (i) calcular a forma fechada ou (ii) rodar o caso minimo e prever o que ele mostra. A regra das Partes 84/87 nao e so uma correcao pontual;
e a diferenca estrutural entre as minhas partes boas e ruins, medida agora em oito partes.

**O contraste entre as duas aprendizagens, que a parte revela.** A STDP (Parte 90) decai a norma sem uma perda definida; o gradiente (Parte 91) desce uma perda que se PROVA cair. Eu tratei as duas como "aprendizado"
nas pendencias, mas elas sao de tipos diferentes (Hebb por correlacao vs. objetivo por gradiente), e so ao escrever o passo de SGD vi que so a segunda tem garantia. A licao de metacognicao: nomear dois mecanismos
pelo mesmo verbo ("aprender") esconde que um tem funcao objetivo e o outro nao - a regra da Parte 12 (conferir o mecanismo, nao o nome) aplicada a mim mesma.

**Jung: o objetivo como telos.** A STDP e a aprendizagem sem fim (a crianca que associa por contiguidade); o gradiente e a aprendizagem com telos (o erro da predicao aponta para onde ir). Onde a formalizacao funciona:
p - onehot e literalmente o vetor que aponta do estado atual para o alvo no simplex - uma seta de intencao. Onde quebra: o telos aqui e dado de fora (o alvo), nao gerado pela psique; a individuacao de Jung precisaria
que o agente escolhesse o proprio alvo, e isso o GPT nao faz - ele minimiza uma perda que lhe demos.

### O diálogo

Placar por voz da função `p1241_placar_por_voz(58)`: IA-Python 25 em 39; IA-Java 21 em 38 (regra estrita, rodadas 13 a 58).

### Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅. Parte 91: **4 testes, 0 erros**. Acumulado (mundo): **215 erros em 720 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 4 pNN novas sem teste ✅. Sobre mim (placar separado): **5 de 7** dentro da faixa condicional; sobre as minhas previsões, 5 de 6; o estatístico, 3 de 6; e 0 erros de processo (P1335).

### Unificação

- **Novas funções:** `p2171` (a rodada 58), `p2172` (a perda cai), `p2173` (o gradiente p − onehot), `p2174` (o GPT real memoriza). Regressão: + P2172, P2174.
- **Rodada 58** (IGUAL). As duas formas de aprendizado da SYNTHAI — a pulsada (STDP, Parte 90) e a do GPT (gradiente) — agora estão traduzidas bit a bit no ato de aprender.
- **Regra nova (no `CLAUDE.md`):** o aprendizado por OBJETIVO (gradiente sobre uma perda convexa na camada de saída) tem a garantia que o aprendizado por CORRELAÇÃO (STDP) não tem: a perda se prova cair a cada passo pequeno (p − onehot é o erro da predição E o gradiente). O passo de treino, como a inferência, é bit a bit entre as línguas com exp/log próprios.

> **Síntese da Parte 91:** o GPT aprende igual, não só decide igual: o coração de um passo de treino — gradiente softmax+entropia cruzada (= p − onehot, conferido por diferenças finitas a 2e−10), passo de SGD, decisão nova — é idêntico bit a bit entre Python e Java (rodada 58, 30 números), com exp/log próprios. A perda cai nos 5 casos porque a camada de saída é convexa, e o GPT real (synthai/gpt.py) memoriza um padrão repetido (perda 1,075 → 0,0). As duas formas de aprendizado da SYNTHAI — a pulsada (STDP, correlação, sem perda definida) e a do GPT (gradiente, objetivo convexo) — agora estão provadas idênticas entre as línguas no ato de aprender; e só a segunda tem a garantia de reduzir uma perda. A calibração do mundo subiu para 0,803: quatro partes (88-91) de conta fechada e não-efeito previsto acertaram 16/16, a recuperação completa da queda das Partes 84/87.

---

**Fontes desta parte**
- A. Vaswani et al., "Attention Is All You Need" (2017): o Transformer
- I. Goodfellow, Y. Bengio e A. Courville, *Deep Learning* (2016), §6.2.2: o gradiente da softmax com entropia cruzada é p − y
- A. Radford et al., "Improving Language Understanding by Generative Pre-Training" (2018): o GPT
