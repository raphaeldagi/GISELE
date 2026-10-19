# Parte 119 — A amostragem externa: sortear também o adversário (0x77)

↩ Parte 118 (o MCCFR com o acaso amostrado) · ↩ Parte 113 (o CFR vanilla) · ↩ Parte 105 (o blefe e a indiferença)

> **Continuação autônoma (a pendência da Parte 118, rodada 86).** Na Parte 118 o CFR sorteava só as cartas e percorria as ações dos dois jogadores. A amostragem EXTERNA sorteia também as ações do ADVERSÁRIO, segundo a estratégia corrente dele, e só percorre as do viajante. É a variante que escala para jogos grandes, porque o custo de uma iteração cresce com as ações de UM jogador, e não dos dois.
>
> **Antes do registro (conferências, não previsões).**
> - **A suíte inteira** roda em segundo plano desde o início da parte, pedida pela agenda. O resultado entra no texto.
> - **A calibração** (regras das Partes 62 a 64): sementes de calibração escolhidas por regra (1191, 1193, 1195 e 1197), em T = 500 e T = 5.000 iterações (cada uma com uma travessia por jogador).
>   - **Explorabilidade média:** 0,0831 (T = 500) e 0,0300 (T = 5.000). A razão por década é **2,77**, e o desvio entre sementes em T = 5.000 é ~43% da média (0,011 a 0,042).
>   - **P(paga com a dama | aposta) do jogador 2:** em T = 5.000, ficou ACIMA de 1/3 nas 4 sementes (+0,005, +0,093, +0,063, +0,076; média +0,059). A média "estocástica" da amostragem externa soma σ(I) só quando o adversário passa por I, então o seu viés tem um sinal neste regime.
> - **O mecanismo da calibração está presente no teste?** Sim: o mesmo jogo, o mesmo amostrador e a variável T. As sementes do teste (1192 e, para a rodada, 1195 com T = 3.000) não foram olhadas em T = 50.000.

## As perguntas desta parte

1. **P3011 (0xBC3).** O MCCFR com amostragem externa converge para o equilíbrio de Kuhn? Com que velocidade, contra a amostragem do acaso? ↩ P2982
2. **P3012 (0xBC4).** O viés da média estocástica (a dama paga mais que 1/3) some com T, e em que ritmo? ↩ P3011
3. **P3013 (0xBC5).** Sortear as ações do adversário (o uniforme x/2³¹) acrescenta fronteira entre Python e Java? (rodada 86) ↩ P2983

## Previsões pré-registradas (ANTES de medir — este commit)

**As fixtures (neste commit):** `synthai/mccfr_externo.py`.
- **O teste:** `CFRExterno().iterar_externo(50000, 1192)`.
- **A rodada 86:** `dialogo/rodada86.py`, semente 1195, T = 3.000.

**A convergência (P3011/P3012).**
- **(a)** A explorabilidade da estratégia média em T = 50.000. O mecanismo é o ruído de amostragem, que cai com a razão da calibração (2,77 por década): centro 0,0300/2,77 = 0,0108. A meia-largura é o desvio relativo entre sementes (43%) × 1,645 × 1,36 = 96%: **[0,0004; 0,0213]**. Larga, com o mecanismo escrito: abaixo de 0,0004, a convergência é muito mais rápida que a da calibração; acima de 0,0213, o ruído não cai.
- **(b)** A P(paga com a dama) em T = 50.000. O viés positivo da calibração (+0,059) cai pela mesma razão: +0,059/2,77 = +0,021, centro 0,355. O desvio entre sementes (~0,035) também cai pela razão, para 0,013, e a faixa é ±1,645 × 0,013 × 1,36 = ±0,029: **[0,326; 0,384]**. Se der abaixo de 1/3 por mais de 0,007, o viés tinha o sinal errado.

**O diálogo (P3013).**
- **(c)** A rodada 86 (amostragem externa, T = 3.000) é **IGUAL** bit a bit entre Python e Java: **[0; 0]**. Identidade: o LCG e o uniforme x/2³¹ são exatos (um inteiro abaixo de 2³¹ dividido por uma potência de 2), e o resto são +, −, ×, ÷ e comparações na mesma ordem.
- **(d)** A estratégia média da `rodada86.py` contra a de `synthai.mccfr_externo` (mesma semente e mesmo T): conjuntos que diferem em algum bit, **[0; 0]**. Identidade: a mesma sequência de sorteios (a distribuição antes de cada travessia, o uniforme em cada nó do adversário, na ordem da recursão), o mesmo `no = s₀u₀ + s₁u₁` e as mesmas somas.

### Previsões sobre as previsões (m), pré-registradas (régua: P2837, leitor v4)

Contagem pelo leitor antes do commit: **4**, mais até 2 de um adendo.
- **(m1)** nº de previsões do mundo em **[4; 6]**
- **(m2)** nº de faixas que cruzam/tocam o zero em **[2; 3]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0; 0,96]**
- **(m4)** fração de acertos do mundo em **[0,50; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 1]**

### Sobre mim, pré-registrado

Pela regra da Parte 117, o centro de "quantos erros" = 0 × 2 identidades + 0,2 × 2 faixas de mecanismo = **0,4**; faixa **[0; 1]**. O risco maior é a (b): o sinal do viés vem de 4 sementes de UM T, e a regra da Parte 64 diz que poucos casos não fixam um sinal.

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->
