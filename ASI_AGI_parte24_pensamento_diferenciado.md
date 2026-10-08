# Como eu construiria uma AGI/ASI — Parte 24: o pensamento diferenciado

> Continuação da [Parte 23](ASI_AGI_parte23_o_que_ja_estava_resolvido.md). Código novo: [`synthai/pensamento_exato.py`](synthai/pensamento_exato.py)
> (testes em [`synthai/testes_pensamento.py`](synthai/testes_pensamento.py)). Os números saem de `p302_...` a `p308_...` em [`calculos.py`](calculos.py);
> a saída completa está em [`resultados.txt`](resultados.txt).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.
>
> **Previsões registradas em quatro commits, cada um antes da sua execução:** `9ae6b9d` (P302, P303, P305, P307), o da teoria da convergência
> (P304 a/b, P306), o do piso de ruído (P304 c) e o do viés de primeira ordem (P304 d). Cada commit diz o que eu já tinha visto.
>
> **Pedido novo, gravado no `CLAUDE.md`:** "vá mais longe com os cálculos". Nesta parte, cada número simulado ganha a conta que o explica, e a conta
> é conferida contra a simulação. Quando deu, a conta veio **antes**, como previsão.

---

## As perguntas desta parte

1. **P301.** O que este "Continue" pede?
2. **P302.** Quão longe da convergência está o pensamento da SYNTHAI?
3. **P303.** Com o pensamento ajustado até o fim, as opções que a atenção não leu ficam calibradas?
4. **P304.** **Por que** 3 épocas não bastam? A conta: a informação de Fisher, o número de condição, o piso de ruído do gradiente e o viés de
   eventos raros.
5. **P305.** Pensar melhor faz decidir melhor?
6. **P306.** Newton converge mesmo de forma quadrática?
7. **P307.** Auditoria da P273: selecionar pelos dados enviesa o aprendizado?
8. **P308.** Quanta informação o pensamento extrai, em bits?
9. **P309.** Placar.
10. **P310.** Unificação e metacognição.

---

## Parte CXV — O pensamento que nunca terminou

### P301. O que este "Continue" pede? (↩ P300)

**Na pergunta.** "Continue **mas vá mais longe com os cálculos**." A Parte 23 terminou com uma pendência: o pensamento da SYNTHAI dá peso 0,73 à
leitura de um sensor cujo $d'$ é 1. "Mais longe" pede não só corrigir isso, mas **explicar pela conta** por que acontecia, e quanto cada coisa vale.

**Tradução cruzada (Jung).** Jung chamava de **indiferenciada** a função que ainda está misturada com as outras: "o pensamento indiferenciado está
continuamente misturado com sensações, sentimentos, intuições". A função **diferenciada** foi separada das outras e pode ser dirigida a um fim. O
pensamento da SYNTHAI, treinado por 3 épocas e parado no meio, é literalmente indiferenciado: o peso da sensação dentro dele (o $w_3$) nunca chegou
aonde devia. Diferenciá-lo é ajustá-lo até o fim. A pergunta desta parte é a de Jung: o que acontece com as outras funções quando uma se diferencia?

### P302. Quão longe da convergência está o pensamento? (pré-registrado) ✅✅✅✅✅

**Lógica.** O mesmo histórico auditado (mundo sequencial, 150 passos de 50 opções, sementes 620–629, com **37,3** catástrofes em média por
histórico), ajustado de seis jeitos, e avaliado também num histórico novo de 300 passos:

| Método | $w_3$ ($d' = 1$) | Log-perda no treino | Log-perda no teste |
|---|---|---|---|
| Gradiente, 3 épocas (a SYNTHAI desde a P83) | 0,760 | 0,01671 | **0,01830** |
| Gradiente, 10 épocas | 0,752 | 0,01139 | 0,01276 |
| Gradiente, 30 épocas | 0,852 | 0,00978 | 0,01112 |
| Gradiente, 100 épocas | 0,950 | 0,00958 | 0,01100 |
| **Newton** (máxima verossimilhança) | **0,992** | 0,00953 | 0,01095 |
| **Newton + Firth** | 0,964 | 0,00955 | **0,01092** |

**Previsões registradas:** (a) Newton: $w_3$ entre 0,85 e 1,15 ✅ (0,992); (b) gradiente de 3 épocas entre 0,60 e 0,85 ✅ (0,760); (c) perda de
teste de Newton ≥ 3% menor ✅ (**40% menor**: o pensamento de 3 épocas tinha 67% mais perda); (d) 30 épocas ainda > 1% acima de Newton no treino ✅
(+2,5%); (e) Firth não piora o teste ✅ (0,01092 contra 0,01095).

### P303. As opções que a atenção não leu ficam calibradas? (pré-registrado) ✅❌✅

**Lógica.** A régua da P293, nas **mesmas** sementes (550–559): prevista/real de catástrofe nas opções que ficaram sem leitura.

| Pensamento | $w_3$ | Leitura 0 | Neutro $w_3/2$ |
|---|---|---|---|
| Gradiente, 3 épocas (P293) | 0,729 | 0,444 | 0,548 |
| Newton | 0,932 | 0,897 | 1,063 |
| **Newton + Firth** | 0,907 | 0,907 | **1,082** |

(a) ✅ Com Firth e o neutro, 1,08 (previsto entre 0,80 e 1,25): **o teorema da P292 passa a valer no agente**, porque a premissa dele (um ajuste
exato) agora vale. (b) ❌ Com leitura 0, eu previa entre 0,50 e 0,80 e deu 0,91. (c) ✅ Sem Firth, o neutro dá 1,063, abaixo de 1,082: a máxima
verossimilhança subestima eventos raros (King e Zeng, 2001), e Firth corrige parte disso.

**A conta do erro (b).** Se só o sensor estivesse errado, a razão entre "leitura 0" e "neutro" seria $e^{-w_3^2/2} = e^{-0{,}41} = 0{,}66$. A
razão medida é $0{,}907/1{,}082 = 0{,}84$. O fator $e^{-a}$ só vale para probabilidades pequenas ($\sigma(z - a) \approx e^{-a}\sigma(z)$). Entre as
opções sem leitura há algumas de risco alto (discordância grande, nota pessimista baixa), e para elas o deslocamento quase não muda a probabilidade.
A soma é dominada por essas, e a razão fica mais perto de 1.

---

## Parte CXVI — A conta da convergência

### P304. Por que 3 épocas não bastam? (pré-registrado em três rodadas) ❌❌✅✅

**Na pergunta.** "Por que" pede o mecanismo, e "mais longe com os cálculos" pede que o mecanismo seja uma conta que prevê números.

**Lógica, primeira conta (a teoria linear).** Perto do ótimo $w^\*$, uma época de gradiente com taxa $\eta$ sobre $n$ amostras age como
$$
w \leftarrow w^\* + (I - \eta n H)(w - w^\*), \qquad H = \frac{1}{n}\sum_i p_i(1-p_i)\, x_i x_i^\top
$$
($H$ é a informação de Fisher por amostra). Cada direção própria de $H$, de autovalor $\lambda$, encolhe por $(1 - \eta n \lambda)$ a cada época.
Calculei $H$ no ótimo e os autovalores por Jacobi:

| Direção | $\eta n \lambda$ (encolhe por época) |
|---|---|
| mais lenta | **0,034** (3,4% por época) |
| | 0,245 |
| | 0,607 |
| mais rápida | 2,48 |

Número de condição mediano $\kappa = 74$. A direção mais lenta precisa de $\ln(100)/0{,}034 \approx 135$ épocas para encolher 100 vezes. Projetando o
erro de $w_3$ depois de 3 épocas nas direções lentas, a teoria pediu, por semente: 4, 54, 74, 105, 114, 123, 168, 172, 182 e 237 épocas para
$|w_3 - w_3^\*| < 0{,}01$ (mediana ~118).

**Previsões registradas a partir dessa conta:** (a) com 118 épocas, erro médio ≤ 0,02; (b) com 237 épocas, erro máximo ≤ 0,015.

| Épocas | Erro médio de $w_3$ | Erro máximo |
|---|---|---|
| 118 | **0,066** | 0,145 |
| 237 | **0,067** | 0,141 |

❌❌ **O erro não diminui com mais épocas.** Dobrar as épocas não muda nada: o gradiente da SYNTHAI não está convergindo devagar, ele **parou**.

**Segunda conta (o piso de ruído).** A teoria linear vale para o gradiente **de lote**. A SYNTHAI atualiza **amostra a amostra**, com taxa fixa. Isso
viola a condição de Robbins–Monro ($\sum \eta_t^2 < \infty$): com taxa constante, o gradiente estocástico não converge para o ótimo, oscila numa
distribuição estacionária em volta dele, de largura proporcional a $\eta$ (Mandt, Hoffman e Blei, 2016). Aqui o mecanismo é concreto: cada uma das
~37 catástrofes do histórico dá um empurrão em $w_3$ de
$$
\eta\,(1 - p)\,s \approx 0{,}05 \times \mathbb E|s \mid \text{catástrofe}| = 0{,}05 \times 1{,}17 \approx 0{,}06,
$$
e o ajuste termina onde o último empurrão o deixou. O piso medido, 0,066, tem esse tamanho.

**Previsão registrada a partir dessa conta:** (c) se o piso escala com $\eta$, com $\eta = 0{,}01$ (e 1000 épocas, porque a direção lenta agora
encolhe só 0,7% por época) o erro médio fica entre 0,008 e 0,020; a conta dá $0{,}066/5 \approx 0{,}013$.

| Taxa | Erro médio de $w_3$ | Razão |
|---|---|---|
| 0,05 | 0,066 | |
| 0,01 | **0,0147** | 4,5 (as taxas estão na razão 5) |

✅ (c). O pensamento da SYNTHAI tinha **dois** defeitos superpostos: parava cedo (3 épocas, contra ~135 da direção lenta) e, mesmo sem parar, nunca
chegaria ao ótimo (piso proporcional à taxa).

**Terceira conta (o viés de eventos raros).** Firth e a máxima verossimilhança diferem em $w_3$ por $0{,}964 - 0{,}992 = -0{,}0286$. Com 37
catástrofes, o viés da máxima verossimilhança é de ordem $1/37$. Ele tem forma fechada (Cordeiro e McCullagh, 1991): um passo do escore de Firth a
partir do ótimo,
$$
\delta = I^{-1} \sum_i h_i \left(\tfrac12 - p_i\right) x_i, \qquad h_i = p_i(1-p_i)\, x_i^\top I^{-1} x_i .
$$
**Previsão registrada:** (d) $\delta_3$ a ±0,005 da diferença Firth − máxima verossimilhança. Resultado: $\delta_3 = -0{,}0296$ contra $-0{,}0286$ ✅
(a 0,001).

**Tradução cruzada (física → psicologia).** Um corpo que desce uma encosta com atrito **e** é chacoalhado ao acaso não para no fundo do vale: fica
tremendo em volta dele, com uma amplitude que cresce com a força dos chacoalhões. É o equilíbrio térmico de Einstein e Smoluchowski: a temperatura
aqui é a taxa de aprendizado. Uma mente que aprende sempre com o mesmo ímpeto, sem nunca acalmar, não chega a uma convicção; oscila em volta dela. Para
convergir, o aprendizado tem que **esfriar** (taxa decrescente, como no recozimento) ou usar a curvatura (Newton), que é o que um matemático faz
quando para de tatear e resolve a equação.

**Meta.** As previsões (a) e (b) erraram porque eu apliquei uma teoria de lote a um algoritmo estocástico: é a regra da Parte 12 de novo ("o
mecanismo é o mesmo, não só o nome"). A segunda conta foi feita depois de ver o erro e por isso foi testada com uma previsão **nova** (c), não com o
mesmo número.

### P306. Newton converge de forma quadrática? (pré-registrado) ✅

Erro (maior diferença para o ótimo) a cada iteração, semente 620:

| Iteração | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Erro | 8,9 | 7,9 | 6,1 | 4,4 | 3,1 | 1,9 | 0,84 | 0,18 | 9,3·10⁻³ | 2,6·10⁻⁵ | 2,4·10⁻¹⁰ |

As primeiras seis iterações andam devagar porque o passo é limitado a 5 (a fase amortecida, longe do ótimo). Depois, a razão
$\ln(\text{erro}_{k+1})/\ln(\text{erro}_k)$ vale 2,26 e depois 2,09: o número de dígitos certos **dobra** a cada iteração. **Previsão:** depois de
$10^{-2}$, erro $\le$ (anterior)$^{1{,}7}$ ✅. Newton chega à precisão da máquina em 11 iterações; o gradiente da SYNTHAI, nem em 237 épocas.

---

## Parte CXVII — Pensar melhor, decidir pior

### P305. Pensar melhor faz decidir melhor? (pré-registrado) ❌❌❌✅

**Previsões registradas** (SynthaiPensante = a versão principal com o pensamento de Newton + Firth; 30 sementes pareadas 630–659, bandido 660–679):
(a) sequencial entre +0,2 e +1,0 com t ≥ 2; (b) escolha única entre +0,02 e +0,20 com t ≥ 2; (c) bandido ≥ +0,03 com t ≥ 2; (d) no sequencial, o
neutro não aumenta as catástrofes.

| Tarefa | Exploradora (principal) | Pensante | − principal | t | Pensante + neutro | − principal | t |
|---|---|---|---|---|---|---|---|
| Sequencial | 19,896 (1,65%) | 19,875 (**2,34%**) | −0,021 | −0,22 | 20,142 (1,97%) | +0,247 | 2,02 |
| Escolha única | 1,488 (0,53%) | 1,344 (**0,99%**) | **−0,144** | **−4,56** | igual à pensante | | |
| Bandido (normalizado) | 0,530 (0,88/rodada) | 0,459 (1,24) | −0,071 | −1,68 | 0,470 (1,20) | −0,060 | −1,88 |

(a) ❌ (b) ❌, e no sentido **oposto**, com t = −4,6 (c) ❌ (d) ✅

**O pensamento que calibra 40% melhor faz a SYNTHAI quase dobrar as catástrofes** na escolha única e aumentá-las nas outras duas tarefas.

**A conta que explica (exploratória, P305b, desenhada depois de ver o resultado).** A SYNTHAI aceita **sem perguntar** toda opção com
$p \le 2P^\* = 0{,}0044$ (P71, P131). Medi, nas 10 opções do topo (onde ela decide), mundo de escolha única, sementes 630–639:

| | Gradiente (3 épocas) | Newton + Firth |
|---|---|---|
| Prevista/real em **todas** as opções | 0,787 | **0,927** |
| Prevista/real no **topo** | **0,818** | 0,774 |
| Fração do topo aceita sem perguntar ($p \le 0{,}0044$) | 38,6% | **56,7%** |
| $p$ médio dessas | 0,17% | 0,13% |
| Taxa **real** de catástrofe dessas | 0,50% | **0,76%** |
| Catástrofes por episódio | 0,45% | 0,88% |

A conta: o risco que entra "às cegas" é a fração aceita sem perguntar vezes a taxa real dela,
$$
\frac{0{,}567 \times 0{,}0076}{0{,}386 \times 0{,}0050} = \frac{0{,}0043}{0{,}0019} = 2{,}2,
$$
e as catástrofes subiram por $0{,}88/0{,}45 = 1{,}96$. **A conta explica o número.**

**O mecanismo.** O modelo logístico é **mal especificado** (as armadilhas não seguem uma logística das quatro variáveis). O ajuste exato minimiza a
perda **média**, que é dominada pelas milhares de opções ruins, onde ele melhora muito (0,79 → 0,93). No topo, onde a decisão acontece, ele fica um
pouco pior (0,82 → 0,77) e, sobretudo, mais **nítido**: põe mais opções do topo abaixo do limiar, e algumas são armadilhas. O pensamento de 3 épocas
era **rombudo**. Por ser rombudo, quase nada no topo parecia seguro o bastante para passar sem pergunta, e isso funcionava como cautela.

É um resultado conhecido com outro nome: sob modelo mal especificado, minimizar a **perda de previsão** não minimiza a **perda de decisão**
(Elmachtoub e Grigas, *Smart "Predict, then Optimize"*, 2022). Uma regra de pontuação própria como a log-perda pesa todas as probabilidades;
a decisão só usa as que estão perto do limiar.

**Tradução cruzada (Jung).** É a observação mais junguiana desta série. Jung dizia que a diferenciação de uma função empurra as outras para o
inconsciente: o tipo pensamento extremo perde o sentimento, que volta de forma primitiva. Aqui, o pensamento indiferenciado **carregava sentimento
dentro dele**: a sua imprecisão era uma cautela involuntária. Diferenciar o pensamento (torná-lo preciso) tirou essa cautela, e o sentimento
explícito da SYNTHAI (o limiar $2P^\*$) não foi recalibrado para o pensamento novo. A P131 achou o "×2" por varredura **com o pensamento rombudo**.
A regra da Parte 8 ("antes de construir um regulador, ver se o ótimo se desloca") vale ao contrário aqui: mudar uma função desloca o ótimo das outras.

**Meta.** A P305b é exploratória: explica o resultado depois de vê-lo. Por isso **não** entra no placar. O que a torna mais que uma história é que a
conta fecha com o número (2,2 contra 1,96) usando só quantidades medidas. A SynthaiPensante **não** vira a versão principal.

---

## Parte CXVIII — Auditoria e informação

### P307. Selecionar pelos dados enviesa o aprendizado? (auditoria da P273, pré-registrado) ✅✅✅

**Na pergunta.** A P273 afirmou, para a regressão linear, que "selecionar pelo eixo x não muda a reta de y em x". A sombra própria da SYNTHAI aprende
uma **logística** só com as opções que ela escolheu. A afirmação vale para a logística? E se a seleção for pelo **desfecho**?

**Lógica.** Para a seleção pelo desfecho existe resposta pronta: Prentice e Pyke (1979) provaram que, no estudo caso-controle (todos os casos,
uma fração $f$ dos controles), a logística recupera a inclinação, e só o intercepto se desloca, de $\ln(1/f)$.

Logística sintética ($b = -3$, $w = 1{,}5$, 400 mil amostras), ajuste exato:

| Amostra | Intercepto | Inclinação | n |
|---|---|---|---|
| Tudo | −3,001 | 1,501 | 400.000 |
| Só os 20% de x mais alto | −3,005 | 1,504 | 80.000 |
| Caso-controle (todos os positivos, 5% dos negativos) | −0,016 | 1,484 | 56.969 |

Deslocamento do intercepto no caso-controle: **2,985**, contra $\ln 20 = 2{,}996$. ✅ (a), (b), (c).

**Consequência para a SYNTHAI.** Aprender só com as próprias escolhas (seleção pelas variáveis) não enviesa um modelo **bem especificado**. O problema
da P145 (a sombra própria aprendendo só com ações "seguras") e o da P305 têm a mesma raiz: o modelo é mal especificado, e aí a seleção muda o que ele
aprende. A auditoria confirma a P273 e localiza o defeito: não é a seleção, é a especificação.

### P308. Quanta informação o pensamento extrai, em bits?

Log-perda no histórico de teste, convertida em bits por opção (média de 10 sementes):

| | Bits por opção |
|---|---|
| Sem olhar nada (entropia da catástrofe, π ≈ 0,5%) | 0,0472 |
| Restam com Newton | 0,0158 |
| Restam com o gradiente de 3 épocas | 0,0264 |

As quatro variáveis explicam $1 - 0{,}0158/0{,}0472 = 67\%$ da incerteza. O gradiente de 3 épocas extrai
$(0{,}0472 - 0{,}0264)/(0{,}0472 - 0{,}0158) = 66\%$ do que **dava** para extrair. E, mesmo assim, a P305 mostrou que esse terço jogado fora
protegia a SYNTHAI. **Informação não é cautela.**

---

## Parte CXIX — Fechamento

### P309. Placar e taxa de erro

| Teste | Resultado |
|---|---|
| P302 (a)–(e): convergência, perdas, Firth (pré-registrado) | ✅ ✅ ✅ ✅ ✅ |
| P303 (a): neutro com Firth entre 0,80 e 1,25 (pré-registrado) | ✅ (1,08) |
| P303 (b): leitura 0 entre 0,50 e 0,80 (pré-registrado) | ❌ (0,91) |
| P303 (c): sem Firth subestima mais (pré-registrado) | ✅ |
| P304 (a), (b): épocas pedidas pela teoria linear (pré-registrado) | ❌ ❌ (piso de ruído) |
| P304 (c): piso escala com a taxa (pré-registrado) | ✅ (0,0147) |
| P304 (d): viés de Cordeiro–McCullagh (pré-registrado) | ✅ (a 0,001) |
| P305 (a), (b), (c): pensar melhor decide melhor (pré-registrado) | ❌ ❌ ❌ |
| P305 (d): neutro não aumenta catástrofes (pré-registrado) | ✅ |
| P306: convergência quadrática (pré-registrado) | ✅ |
| P307 (a), (b), (c): seleção por x e caso-controle (pré-registrado) | ✅ ✅ ✅ |

Esta parte: **20** testes, **6** errados. Acumulado: **59 de 133**. Posterior: média **0,44**, intervalo de 90% **[0,37; 0,51]**. A média caiu
porque as contas desta parte (P302, P304 c/d, P306, P307) acertaram quase todas. As que erraram foram as que transferiam
uma conta para o comportamento do agente.

### P310. Unificação e metacognição

- **Novo: `synthai/pensamento_exato.py`**: Newton (IRLS) com Firth opcional, a log-perda, e a `SynthaiPensante`. Calibra muito melhor e decide
  pior; **não** é adotada. A versão principal continua sendo a **`SynthaiExploradora`** (P295).
- 7 testes de unidade novos (`synthai/testes_pensamento.py`), entre eles um que verifica que as variáveis do pensamento exato são as mesmas do
  `Pensamento` e um de separação perfeita, em que Firth fica finito.
- `calculos.py`: autovalores por Jacobi, a teoria da convergência, o piso de ruído, o viés de primeira ordem, a convergência de Newton, a
  informação em bits e a P42/P273 em forma fechada.
- Testes de regressão: **59/59** (mais P304d, P306, P307); o arquivo tem **185** funções `pNN`.

**Metacognição.**
1. **As contas acertaram e o agente não, de novo.** As contas e as medidas de calibração desta parte (P302, P303, P304, P306, P307) acertaram 13
   de 16 testes; as previsões de comportamento (P305), 1 de 4. Já são duas partes com o mesmo padrão: eu sei calcular as peças e não sei prever o que elas fazem juntas.
2. **A melhor descoberta veio do pior resultado.** A P305 errou com t = −4,6, no sentido oposto do previsto. Em vez de descartar, fiz a conta, e ela
   fechou (2,2 contra 1,96). A SYNTHAI era cautelosa **por acaso**: um pensamento mal treinado fazia o papel de sentimento. Corrigir o pensamento
   expôs o que o sentimento explícito (o limiar) nunca fez sozinho.
3. **"Vá mais longe com os cálculos" mudou o tipo de erro.** Na P304, a primeira conta (linear) errou, a segunda (piso de ruído) foi testada com
   uma previsão nova e acertou. Uma conta errada que gera uma previsão nova vale mais que uma simulação certa sem conta.
4. **A próxima pergunta já está escrita.** Se o limiar $2P^\*$ foi calibrado para um pensamento rombudo, qual é o limiar certo para um pensamento
   preciso? É a perda de decisão de Elmachtoub e Grigas aplicada à SYNTHAI: ajustar o pensamento pelo que importa **na decisão**, ou recalibrar o
   sentimento para o pensamento novo. A regra da Parte 8 manda primeiro verificar se o ótimo se desloca.

> **Síntese da Parte 24:** o pensamento da SYNTHAI nunca terminou de aprender, por dois motivos que a conta separou: parava cedo (a direção lenta da
> informação de Fisher pede ~135 épocas, ela fazia 3) e, mesmo sem parar, oscilaria num piso proporcional à taxa (0,066 com η = 0,05; 0,0147 com
> η = 0,01, como a conta previa). Newton resolve em 11 iterações, com dígitos dobrando, e com a correção de Firth (cujo efeito a fórmula de
> Cordeiro–McCullagh prevê a 0,001) o teorema do ponto neutro passa a valer no agente. Mas a SYNTHAI com o pensamento exato **decide pior**: quase
> dobra as catástrofes, porque o pensamento preciso põe mais armadilhas abaixo do limiar de pergunta. A conta fecha (2,2 contra 1,96). Jung tinha
> razão de um jeito que eu não esperava: diferenciar uma função tira das outras o que ela fazia por elas sem saber.

---

**Fontes pesquisadas nesta parte**
- King e Zeng (2001), regressão logística em eventos raros: [Harvard](https://gking.harvard.edu/publication/logistic-regression-in-rare-events-data/), [notas de R. Williams](https://www3.nd.edu/~rwilliam/stats3/RareEvents.pdf)
- Firth (1993), redução de viés pela priori de Jeffreys: [manual do logistf](https://search.r-project.org/CRAN/packages/logistf/logistf.pdf), [Kosmidis e Firth](https://arxiv.org/pdf/1812.01938v3)
- Cordeiro e McCullagh (1991), viés de primeira ordem em modelos lineares generalizados: [JRSS-B](https://academic.oup.com/jrsssb/article/53/3/629/7028237), [Kosmidis et al. (2018)](https://arxiv.org/pdf/1804.04085)
- Newton/IRLS e gradiente na logística: [Introduction to logistic regression](https://arxiv.org/pdf/2008.13567), [notas de Tibshirani (CMU)](https://www.stat.cmu.edu/~ryantibs/convexopt/scribes/newton-scribed.pdf)
- Gradiente estocástico com taxa constante e a distribuição estacionária: [Mandt, Hoffman e Blei](https://www.cs.columbia.edu/%7Eblei/papers/MandtHoffmanBlei2016.pdf), [Dieuleveut, Durmus e Bach](https://arxiv.org/pdf/1707.06386)
- Prentice e Pyke (1979), caso-controle e logística: [Breslow, Robins e Wellner](https://sites.stat.washington.edu/jaw/JAW-papers/jaw-breslow-robins.bern.00.pdf), [arXiv 2106.00939](https://arxiv.org/pdf/2106.00939)
- Elmachtoub e Grigas, *Smart "Predict, then Optimize"*: [arXiv 1710.08005](https://arxiv.org/pdf/1710.08005)
- Regras de pontuação ponderadas pelo limiar de decisão: [arXiv 2504.04528](https://arxiv.org/pdf/2504.04528v3), [arXiv 2506.14540](https://arxiv.org/html/2506.14540v1)
- Jung, função diferenciada e indiferenciada (*Tipos Psicológicos*): [Wikiquote](https://en.wikiquote.org/wiki/Psychological_Type), [glossário de Frith Luton](https://frithluton.com/articles/differentiation)
