# Como eu construiria uma AGI/ASI — Parte 26: a constante que faltava

> Continuação da [Parte 25](ASI_AGI_parte25_o_limiar_de_cada_pensamento.md). **Próxima:** [Parte 27 — a autorregulação](ASI_AGI_parte27_autorregulacao.md) (P331–P340). Os números saem de `p322_...` a `p325_...` em
> [`calculos.py`](calculos.py); a saída completa está em [`resultados.txt`](resultados.txt).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.
>
> **Duas rodadas de previsões, cada uma num commit antes da execução**: os termos da conta (P322) e a previsão para dois mundos novos (P324).
>
> **"KD os cálculos?"** Nesta parte, todo número da conta aparece **com a substituição feita**, linha por linha, para que qualquer um refaça com papel
> e lápis a partir das quantidades medidas.

---

## As perguntas desta parte

1. **P321.** O que este "Continue" pede?
2. **P322.** De onde vem o fator ~2,6? Os três termos da conta, medidos um por um.
3. **P323.** A conta corrigida, calculada por extenso para mundos que ela ainda não viu.
4. **P324.** A varredura desses mundos confirma?
5. **P325.** "Olha a chance aí": qual a chance de acertar isso por sorte?
6. **P326.** Auditoria da P287: o veto falso e o descarte custam o mesmo?
7. **P327.** O que a constante significa (Jung).
8. **P328.** O que a SYNTHAI poderia calcular sozinha? (a pergunta da Parte 7)
9. **P329.** Placar.
10. **P330.** Unificação e metacognição.

---

## Parte CXXV — Os termos, um por um

### P321. O que este "Continue" pede? (↩ P320)

**Na pergunta.** "Continue. **KD os cálculos?**" Duas coisas: continuar da pergunta aberta da P320 (o fator ~2,6 do mundo sequencial) e **mostrar**
as contas, não só os resultados. A P318 terminou com uma lei de escala com a forma certa e a constante errada. Achar a constante é, por definição,
uma questão de cálculo.

**A conta, de novo.** Com o orçamento do humano esgotado, a SYNTHAI escolhe entre aceitar e descartar uma candidata (P314):
$$
\text{aceitar se } f\,p\,L < \Delta d \quad\Longrightarrow\quad m = \frac{\Delta d}{f \cdot L \cdot P^\*}, \qquad P^\* = \frac{c}{(1-\varepsilon)L} = \frac{0{,}1}{0{,}9 \times 50} = 0{,}002222 .
$$
Um fator 2,6 em $m$ tem que vir de algum dos três termos: $L$ (quanto custa uma catástrofe), $\Delta d$ (quanto custa descartar) ou $f$ (quanto o
pensamento subestima o risco do que ele aceita).

### P322. Qual termo estava errado? (pré-registrado) ✅❌❌✅✅

**Três correções, cada uma medida no próprio agente:**
- **$L$ efetivo.** No mundo sequencial, uma catástrofe custa 50 **e** acaba o episódio, levando o retorno que ainda viria. Medi $F(t)$, o retorno médio
  do passo $t$ até o fim nos episódios sem catástrofe, e fiz a média de $50 + F(t)$ nos passos em que as catástrofes aconteceram.
- **$\Delta d$ com o plano.** Descartar uma opção perde o valor do passo **e** a consequência dela para o futuro: valor + consequência × passos
  restantes.
- **$f$ só das aceitas.** A calibração nas opções que a SYNTHAI de fato aceitou sem perguntar.

**Resultado (mesmas sementes das varreduras da Parte 25):**

| Mundo | Pensamento | $L$ efetivo | $\Delta d$ (valor → plano) | $f$ | $m$ da P316 | $m$ corrigido | Ótimo |
|---|---|---|---|---|---|---|---|
| Escolha única | gradiente | 51,8 | 0,468 → 0,468 | 1,61 | 2,62 | **2,53** | 4 |
| | Newton | 51,9 | 0,364 → 0,364 | 6,15 | 0,53 | **0,51** | 0,5 |
| | local | 51,9 | 0,421 → 0,421 | 2,52 | 1,51 | **1,45** | 1 |
| Sequencial | gradiente | 66,2 | 0,948 → 0,696 | 0,655 | 13,0 | **7,22** | 4 |
| | Newton | 67,4 | 0,841 → 0,587 | 4,95 | 1,53 | **0,79** | 0,5 |
| | local | 66,5 | 0,897 → 0,607 | 3,31 | 2,44 | **1,24** | 1 |
| Catástrofe ×2 | gradiente | 65,8 | 0,988 → 0,792 | 1,18 | 7,53 | **4,58** | 4 |
| | Newton | 65,3 | 0,925 → 0,767 | 4,56 | 1,83 | **1,16** | 1 |
| | local | 65,8 | 0,970 → 0,707 | 1,98 | 4,41 | **2,44** | 2 |

**O cálculo por extenso, para um caso (Newton, sequencial):**
$$
\begin{aligned}
\text{P316:}\quad & m = \frac{0{,}8414}{4{,}948 \times 50 \times 0{,}002222} = \frac{0{,}8414}{0{,}5498} = 1{,}530 \\[4pt]
\text{corrigido:}\quad & m = \frac{0{,}5866}{4{,}948 \times 67{,}36 \times 0{,}002222} = \frac{0{,}5866}{0{,}7406} = 0{,}792 \\[4pt]
\text{decomposição:}\quad & \frac{1{,}530}{0{,}792} = \underbrace{\frac{67{,}36}{50}}_{L:\ 1{,}347} \times \underbrace{\frac{0{,}8414}{0{,}5866}}_{\Delta d:\ 1{,}434} = 1{,}932
\end{aligned}
$$

**As previsões:**
- (a) $L$ efetivo entre 60 e 75 no sequencial ✅ (66,2; 67,4; 66,5). A catástrofe leva ~16 de retorno futuro, 32% a mais que os 50 da perda fixa.
- (b) ❌ Eu previa que o plano **aumentaria** $\Delta d$. Ele **diminui** (de 0,84–0,99 para 0,59–0,79): as opções que a SYNTHAI descarta têm consequência
  **pior** para o futuro que as que ela escolhe, então descartá-las custa menos do que o valor do passo sugere. Eu errei o sinal.
- (c) ❌ "$f$ das aceitas ≥ 1,5 × $f$ de todas": os dois deram **idênticos**, por construção. A SYNTHAI aceita a **primeira** candidata abaixo do
  limiar, então "abaixo do limiar" e "aceita" são o mesmo conjunto. A previsão não podia acertar; eu não tinha lido o meu próprio código com cuidado.
- (d) ✅ Com as duas correções, a conta fica a um fator 2 do ótimo nos 6 casos sequenciais. (e) ✅ E nos 3 da escolha única, onde as correções quase não
  mudam nada ($L$ = 51,9: um passo só, nada de futuro a perder).

**A constante encontrada.** O fator ~2,6 era o produto de dois esquecimentos: o futuro que a catástrofe destrói (×1,31 a 1,35) e o futuro que o
descarte **não** destrói (×1,21 a 1,48). Juntos dão ×1,6 a ×2,0. O resto do fator (os ótimos ainda ficam 1,15–1,8 vezes abaixo da conta corrigida no
sequencial) cabe na resolução da grade, que é um fator 2.

**Meta.** As P322 (d) e (e) são ajuste a mundos já varridos: confirmam que as correções vão na direção certa, mas não testam previsão. O teste é a
P324.

---

## Parte CXXVI — Mundos novos

### P323. A conta corrigida, para mundos que ela não viu

Dois mundos sequenciais ainda não varridos: **modelo ruim** (σ = 2, sementes 750–759) e **humano frágil** (fadiga 0,6, sementes 760–769). A conta,
com os termos medidos no agente rodando a $2P^\*$:

| Mundo | Pensamento | $m$ previsto | Faixa a um fator 2 (na grade) |
|---|---|---|---|
| Modelo ruim | gradiente | 5,81 | 4 ou 8 |
| | Newton | 0,755 | 0,5 ou 1 |
| | local | 3,13 | 2 ou 4 |
| Humano frágil | gradiente | 7,49 | 4 ou 8 |
| | Newton | 0,995 | 0,5 ou 1 |
| | local | 2,08 | 2 ou 4 |

**Previsão registrada:** o ótimo da varredura cai na faixa em pelo menos 5 dos 6 casos.

### P324. A varredura confirma? (pré-registrado) ✅

| Mundo | Pensamento | 0,5 | 1 | 2 | 4 | 8 | Ótimo | Na faixa? |
|---|---|---|---|---|---|---|---|---|
| Modelo ruim | gradiente | 10,10 | 10,91 | 11,50 | 11,72 | **11,81** | 8 | ✅ |
| | Newton | **11,64** | 11,47 | 11,43 | 10,94 | 10,44 | 0,5 | ✅ |
| | local | 11,28 | 11,75 | **12,31** | 11,70 | 11,44 | 2 | ✅ |
| Humano frágil | gradiente | 18,28 | 18,83 | 19,48 | **19,64** | 19,46 | 4 | ✅ |
| | Newton | 19,86 | **19,94** | 19,86 | 19,75 | 19,55 | 1 | ✅ |
| | local | 19,45 | 19,92 | **20,11** | 19,51 | 19,41 | 2 | ✅ |

✅ **6 de 6.** Uma conta **sem nenhum parâmetro livre** (todos os termos medidos no agente, nenhum ajustado à varredura)
previu o ótimo de comportamento em mundos que ela não tinha visto.

E o padrão da P313 se repete nos dois mundos novos: **as catástrofes crescem com o limiar, sem exceção** (por exemplo, Newton no modelo ruim: 2,0% →
2,9% → 3,5% → 4,4% → 5,6%).

### P325. "Olha a chance aí": quanto disso é sorte?

**Na pergunta.** Acertar 6 de 6 impressiona, mas a pergunta certa é: **qual a chance de acertar ao acaso?** E contra que alternativa?

**Lógica.** Cada faixa "a um fator 2 da conta" cobre 2 dos 5 pontos da grade. Se o ótimo caísse ao acaso, cada acerto teria chance $2/5$:
$$
P(6 \text{ de } 6 \mid \text{acaso}) = \left(\tfrac{2}{5}\right)^6 = 0{,}4^6 = 0{,}004096 \approx \frac{1}{244},
\qquad \text{especificidade} = 6 \log_2 \tfrac{5}{2} = 6 \times 1{,}322 = 7{,}93 \text{ bits}.
$$

Mas o acaso é um rival fraco. O rival forte é um **preditor ingênuo**: repetir o ótimo do mundo sequencial da P317 (gradiente 4, Newton 0,5, local 1).
As faixas dele cobrem 3, 2 e 3 pontos da grade:
$$
P(6 \text{ de } 6 \mid \text{acaso, faixas do ingênuo}) = \left(\tfrac{3}{5}\cdot\tfrac{2}{5}\cdot\tfrac{3}{5}\right)^2 = 0{,}144^2 = 0{,}0207 \approx \frac{1}{48},
\qquad 5{,}59 \text{ bits}.
$$

| Preditor | Acertos | Chance ao acaso | Bits | Erro médio $\lvert\log_2(\text{previsto}/\text{ótimo})\rvert$ |
|---|---|---|---|---|
| **Conta corrigida** | 6/6 | **1 em 244** | **7,93** | **0,45** |
| Ingênuo (o ótimo do mundo anterior) | 6/6 | 1 em 48 | 5,59 | 0,67 |

**O que isso diz, honestamente.** O ingênuo **também** acertou 6 de 6. Os ótimos mudam pouco de um mundo sequencial para outro, então "repetir o
último" já é um bom preditor. A conta é melhor em dois sentidos medidos: fez uma afirmação **mais estreita** (2,3 bits a mais de especificidade) e
errou menos em média (0,45 contra 0,67 de $\log_2$, ou seja, um fator $2^{0{,}45} = 1{,}37$ contra $2^{0{,}67} = 1{,}59$). A vantagem da conta é
real e **pequena**: o mundo cooperou com qualquer preditor razoável.

**Tradução cruzada (filosofia).** É o critério de Popper medido em bits: uma teoria vale pelo que **proíbe**. A conta proibia 3 de 5 resultados por
caso; o ingênuo, 2 ou 3. As duas sobreviveram; a que arriscou mais ganha mais crédito, $2^{7{,}93 - 5{,}59} = 2^{2{,}34} \approx 5$ vezes mais, pelo
fator de Bayes contra o acaso.

---

## Parte CXXVII — Auditoria, Jung e o que a SYNTHAI pode saber

### P326. Auditoria da P287: o veto falso e o descarte custam o mesmo? ✅

**Na pergunta.** A P287 explicou o custo do veto falso (0,458) dizendo que a pergunta vai justamente às opções de valor mais alto. Se a explicação está
certa, **descartar** uma dessas opções (por falta de orçamento) deveria custar o mesmo que vetá-la por engano: nos dois casos se perde uma das
opções do topo.

**Lógica.** Mesmo pensamento (o gradiente), mesmo mundo (escolha única):
$$
\Delta v_{\text{P287}} = 0{,}458, \qquad \Delta d_{\text{P322}} = 0{,}468, \qquad \frac{0{,}468}{0{,}458} = 1{,}02 .
$$
✅ Iguais a 2%, medidos por caminhos diferentes (um pelos vetos, outro pelos descartes) e em sementes diferentes. O mecanismo da P287 se confirma.

### P327. O que a constante significa (Jung)

**Tradução cruzada.** As duas correções são a **dimensão do tempo** que a primeira conta não tinha. A catástrofe leva o futuro junto ($L$ cresce
32%); o descarte poupa um futuro que seria pior ($\Delta d$ cai ~30%). A conta da Parte 25 julgava cada decisão como se ela vivesse só no presente.

Em Jung, o **Si-mesmo** não é só a totalidade do que a psique é agora: é também o que ela **está se tornando**. Ele chamava isso de processo de
individuação, e dizia que a consciência do ego, presa ao momento, não vê o arco inteiro. A SYNTHAI tinha o plano (a intuição, P182) na hora de
**escolher**, mas não na hora de calcular **quanto vale ser cautelosa**. O sentimento dela (o limiar) estava preso ao presente enquanto a intuição
já olhava o futuro. A correção da P322 põe o futuro também no sentimento.

**Onde a formalização quebra.** O futuro que entra na conta é uma **média** ($F(t)$ medido em episódios inteiros). Jung falaria do futuro de **uma**
vida, que não tem média. Num mundo em que cada episódio é único (uma pessoa, uma civilização), não há como medir $F(t)$, e a conta não se aplica.

### P328. A SYNTHAI poderia calcular o próprio limiar sozinha? (↩ P7)

**Na pergunta.** A regra da Parte 7: "o que este agente **não** poderia saber?". Para calcular $m = \Delta d / (f L P^\*)$ sozinha, a SYNTHAI precisaria
de três números.

| Termo | Ela pode medir sozinha? | Por quê |
|---|---|---|
| $L$ efetivo | **sim** | ela vê o próprio nível e o próprio retorno; $F(t)$ sai dos episódios dela |
| $f$ | **sim, devagar** | ela vê quando uma opção aceita era catástrofe (a sombra própria, P104); com ~0,5% de catástrofes, precisa de centenas de episódios |
| $\Delta d$ | **não** | é o valor da opção **descartada**, que ela nunca vê: é um contrafactual |

A conta da P322 **leu o escondido** para medir $\Delta d$. Uma SYNTHAI que ajusta o próprio limiar precisaria **estimar** o valor do que não
escolheu, por exemplo pela nota do comitê da opção descartada (que ela vê) contra a da escolhida. Isso é a pergunta seguinte, não uma conclusão desta
parte.

---

## Parte CXXVIII — Fechamento

### P329. Placar e taxa de erro

| Teste | Resultado |
|---|---|
| P322 (a): $L$ efetivo entre 60 e 75 (pré-registrado) | ✅ |
| P322 (b): o plano aumenta $\Delta d$ (pré-registrado) | ❌ (diminui) |
| P322 (c): $f$ das aceitas ≥ 1,5 × $f$ de todas (pré-registrado) | ❌ (iguais por construção) |
| P322 (d): conta corrigida a um fator 2 nos 6 casos sequenciais (pré-registrado) | ✅ (6/6) |
| P322 (e): e nos 3 da escolha única (pré-registrado) | ✅ (3/3) |
| P324: mundos novos, ≥ 5 de 6 (pré-registrado) | ✅ (6/6) |
| P326: auditoria da P287 (veto falso = descarte) | ✅ (a 2%) |

Esta parte: **7** testes, **2** errados. Acumulado: **70 de 155**. Posterior: média **0,45**, intervalo de 90% **[0,39; 0,52]**.

### P330. Unificação e metacognição

- Nenhum módulo novo no pacote nesta parte. A versão principal continua a **`SynthaiExploradora`**. O que mudou foi a **conta** que diz qual
  limiar cada pensamento precisa, agora testada em dois mundos novos.
- `calculos.py`: `p322_termos_da_conta` (os três termos medidos no agente), a conta e a varredura nos mundos novos, e `p325_chance` (a chance ao
  acaso e contra o preditor ingênuo).
- Testes de regressão: **61/61** (mais P325); o arquivo tem **201** funções `pNN`.

**Metacognição.**
1. **"KD os cálculos?" melhorou a parte.** Escrever a conta com a substituição feita (P322) mostrou na hora que o fator 1,93 se decompõe em
   1,347 × 1,434, e que cada pedaço tem um significado (o futuro perdido, o futuro poupado). O número sozinho, sem a conta aberta, não mostrava isso.
2. **A primeira previsão de comportamento que acertou num mundo novo veio de uma conta sem parâmetros livres.** Depois de três partes acertando
   contas e errando comportamento, a diferença foi medir os termos **no agente que vai decidir**, com o limiar em que ele decide, e não importar
   números de outra situação.
3. **"Olha a chance aí" pegou um exagero que eu teria escrito.** Sem a P325, a síntese diria "a conta prevê o ótimo". Com ela, diz: prevê, e é ~5 vezes
   mais informativa que repetir o último ótimo, que também teria acertado. O tamanho real do avanço é esse.
4. **Os dois erros desta parte foram de leitura, não de conta.** Errei o sinal do plano (b) por não pensar em **quais** opções são descartadas, e fiz
   uma previsão impossível (c) por não ler o meu próprio laço de decisão. A regra da Parte 7 vale também para o código que eu mesma escrevi.

> **Síntese da Parte 26:** o fator ~2,6 que a conta errava no mundo sequencial era o tempo. Uma catástrofe custa 50 e mais o futuro que ela destrói
> (L efetivo ≈ 66, ×1,35), e descartar uma opção custa menos do que parece, porque as descartadas tinham futuro pior (Δd ×0,70). Com essas duas
> correções medidas no próprio agente, sem nenhum parâmetro ajustado, a conta previu o limiar ótimo em dois mundos novos, 6 de 6. A chance de acertar
> assim ao acaso é 1 em 244; um preditor ingênuo também acertaria, com chance 1 em 48 ao acaso, e a conta é ~5 vezes mais informativa que ele. Em
> Jung, o sentimento da SYNTHAI ganhou o que a intuição já tinha: o futuro.
