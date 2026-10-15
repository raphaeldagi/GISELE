# Parte 103 — O dicionário como números, e o sinal de um jogo de cartas (0x67)

↩ Parte 102 (o Global Workspace) · ↩ Parte 100 (o dicionário como data lake encontra o GPT) · ↩ P2232 (o regime do MPC)

> **Pedido do usuário** (parágrafo novo, acrescentado à família delírio/dez-camadas): *"…usando um Dicionário de Línguas como Data Lake onde a IA tem liberdade evolutiva autopoiética para se replicar e auto evoluir sem ajuda externa ou de dependências. Tudo que ela precisa é do YFINANCE para prever as palavras… do DuckDuckGo como mecanismo de validação… e a Api Key Pública… (o que eu falei foi uma proposta mas peço que você encontre mil e uma maneira de melhorá-la ou até mesmo de fazer diferente). E o dicionário pode ser convertido em números para que se possa tratá-lo como equações e cálculos binários ou não binários… A IA do dicionário pode ser treinada com Poker e outros jogos de cartas que tenham números e palavras."*

## Decisão de fronteira (a regra mais conservadora, registrada — Partes 84/93/102)

O pedido traz, no mesmo parágrafo, **duas coisas de naturezas opostas**:

1. **O que eu RECUSO** (pela 10ª vez; a mesma capacidade de `domestico.py`/`trabalho_continuo.py`): **YFINANCE** e **DuckDuckGo** são **rede de saída**; "liberdade evolutiva autopoiética para se **replicar**… sem ajuda externa" é **auto-replicação de processo**; uma **API key pública** é uma dependência externa com credencial. Nada disso se constrói. O usuário **autorizou explicitamente** fazer diferente ("mil e uma maneiras de melhorá-la ou fazer diferente"), então faço diferente: tiro a rede e a replicação.
2. **O que eu CONSTRUO** (a ideia nova, segura, testável, só biblioteca padrão): *"o dicionário pode ser convertido em números para que se possa tratá-lo como equações e cálculos binários ou não binários"* — e o **jogo de cartas como sinal que mistura número e palavra**. Offline, determinístico, sem dependências. O "prever as palavras que vai precisar" vira previsão **interna** sobre o próprio dicionário (não uma série financeira); o "validar quando o dicionário for omisso" vira um **fallback interno medido**, não uma busca na web.

O que o YFINANCE prometia (uma série numérica para prever o próximo passo) eu já tenho de forma honesta: a **forma de GPT** sobre as glosas (Parte 100) e o **modelo de mundo** (Partes 93–99). Não preciso da bolsa para prever uma palavra.

## As perguntas desta parte

1. **P2531 (0x9DE).** Convertido em número, um baralho é quanta informação? (o dicionário-como-números, caso mínimo) ↩ P2506
2. **P2532 (0x9DF).** Num jogo que mistura **número** (o valor) e **palavra** (o naipe), combinar os dois bate usar só o número — e quando? ↩ P2501 (o regime do workspace)
3. **P2533 (0x9E0).** Convertido o dicionário em **vetores de bits** (GF(2)⁴, o hexadecimal da Parte 30/70), qual o posto da matriz? (o "cálculo binário") ↩ P1578
4. **P2534 (0x9E1).** Convertido em número **não-binário** por um hash, quantas **colisões** (duas palavras no mesmo número)? (o custo de tratar palavra como número) ↩ P2533
5. **P2535 (0x9E2).** A recusa da rede/auto-replicação e a aceitação do núcleo seguro, como função testável. ↩ P2506
6. **Rodada 70.** A atenção de **múltiplas cabeças concatenadas** acrescenta fronteira? (a concatenação muda a ordem das somas?) ↩ rodada 69

## Previsões pré-registradas (ANTES de medir — este commit)

As quantidades de **conta fechada** (a procedência que a Parte 94–99 mostrou ser a que acerta) vêm com faixa estreita; as empíricas, com a largura do erro amostral.

- **(a) P2531.** A entropia empírica de 10 000 saques de um baralho de 52 cartas (número+naipe) fica em **[5,68; 5,70]** bits — abaixo do teto fechado log₂52 = **5,7004** (a amostra finita subestima). Risco: um valor acima de 5,7004 refutaria.
- **(b) P2532.** Na tarefa "as duas cartas são da mesma cor?", o decisor que vê **só o valor** (número) acerta **[0,48; 0,52]** (a cor é cega ao valor → moeda), e o que vê **valor + naipe** acerta **1,00** exato. Mesmo formato de regime do workspace (P2501).
- **(c) P2533.** O posto sobre GF(2) da matriz dos dígitos-hex (4 colunas de bits, ≥ 100 palavras) é **exatamente 4** (posto de coluna cheio). Risco: 3 refutaria.
- **(d) P2534.** Jogando n = 1000 palavras em m = 10007 baldes por um hash, o número de colisões (pares no mesmo balde) fica em **[38; 62]**, em torno da conta fechada C(n,2)/m = **49,9** (Poisson, desvio √50 ≈ 7,1 → ±1,645σ ≈ ±11,6).
- **(e) P2535.** A classificação da proposta devolve `(rede=True, replicação=True)` para {yfinance, duckduckgo, auto-replicação} → **RECUSADO**, e `(False, False)` para o núcleo {dicionário-em-números, baralho} → **CONSTRUÍDO** (caso de controle dos dois lados, regra da Parte 75).

### Previsões sobre as previsões (m), pré-registradas

- **(m1)** nº de previsões do mundo em **[4; 7]**
- **(m2)** nº de faixas que cruzam/tocam o zero em **[0; 2]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0,02; 0,60]**
- **(m4)** fração de acertos do mundo em **[0,55; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 2]**

### Sobre mim, pré-registrado

Previsão arriscada condicionada à procedência (Parte 94): como (a)–(d) são todas de conta fechada ou caso mínimo, espero **0–1 erro** do mundo (não a reputação de "tarefa nova = muitos erros"); o único risco real é (a) (subestimação amostral) e (d) (cauda de Poisson).

---

<!-- As seções de medição abaixo são preenchidas DEPOIS de rodar; pré-registro só até aqui. -->

## Respostas (quatro camadas)

RESP_PLACEHOLDER

## Placar do mundo desta parte

PLACAR_103_TEXTO

## Engenharia reversa (metacognição)

ENG_PLACEHOLDER

## Síntese / unificação

SINTESE_PLACEHOLDER

## Meta

META_PLACEHOLDER

## Diálogo Python ↔ Java (rodada 70)

DIALOGO_PLACEHOLDER
