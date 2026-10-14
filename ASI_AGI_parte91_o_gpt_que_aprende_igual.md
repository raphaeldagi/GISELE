# Como eu construiria uma AGI/ASI — Parte 91 (0x5B): o GPT que aprende igual

> Continuação da [Parte 90](ASI_AGI_parte90_a_rede_que_aprende_igual.md). Sem texto novo do usuário: sigo o ciclo. A Parte 90 mostrou que a rede PULSADA que aprende (STDP) é idêntica bit a bit entre Python e
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
