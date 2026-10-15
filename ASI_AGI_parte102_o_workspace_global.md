# Como eu construiria uma AGI/ASI — Parte 102 (0x66): o Global Workspace — a integração que vence quando nenhum vê sozinho

> Continuação da [Parte 101](ASI_AGI_parte101_delirio_dez_camadas.md). Nasce do upload do usuário (`SYNTHAI_consolidado_v0_15_0.py`, "veja se algo serve"), **auditado por árvore sintática sem executar** (`externos/texto_recebido_parte102.md`): recusei `domestico.py`
> (rede) e `trabalho_continuo.py` (`Popen` de si mesmo — auto-replicação; regra das Partes 84/93); quase tudo o mais que serve já está reimplementado nas Partes 83–101; o candidato **novo e seguro** é `workspace_global.py` — a **Global Workspace Theory** (GWT).
>
> **A ideia, reimplementada do zero** (`synthai/workspace.py`, em biblioteca padrão, sem rede/threads/Popen): vários módulos **especialistas** propõem; um vence por **saliência**; a sua contribuição é **transmitida** (broadcast) aos outros no próximo passo. A pergunta mais
> funda (↩ P2232, o MPC): a **integração global** bate os especialistas **isolados** — e, se bate, **quando**? A minha aposta, do mesmo feitio do veredito do MPC (Parte 93): a integração vence **só** quando a tarefa exige combinar o que nenhum especialista vê sozinho, e
> **empata** quando um basta.

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[4; 8]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,80]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** o número de surpresas em **[0; 3]**

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[12.000; 22.000]** | o estatístico |
| testes de unidade | **[6 + S; 10 + S]** | integração×isolado, empate, exato, convergência, rodada 69 (S = surpresas) |
| previsões unilaterais | **[0; 1]** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

- **(a)** **a integração vence quando precisa de dois** (p2501): na tarefa `y = x₁ + x₂` com o especialista A vendo só x₁ e B só x₂, o melhor **isolado** tem RMSE ≈ `|b|/√3` ∈ **[0,50; 0,62]** (o erro irredutível da característica que não vê, x₂ ~ U(−1,1) tem desvio 1/√3),
  e o Global Workspace recupera o exato → razão ws/isolado **< 0,01**.
- **(b)** **empata quando um basta** (p2502): quando `b = 0` (só x₁ importa), o isolado e o workspace **empatam**, ambos com RMSE **< 1e−9** — o broadcast não acrescenta nada (NÃO-efeito, como o MPC fora do regime na Parte 93) (categórico).
- **(c)** **a integração recupera o exato** (p2503): o workspace (descida por coordenadas / Gauss-Seidel sobre a regressão conjunta) converge para os coeficientes verdadeiros; na tarefa de dois, RMSE (8 passos) **< 1e−6** (forma fechada: Gauss-Seidel em sistema de posto cheio).
- **(d)** **convergência geométrica, não instantânea** (p2504): como x₁ e x₂ têm correlação amostral pequena mas não nula, o workspace converge **geométrico** — RMSE(1 passo) > RMSE(2) > RMSE(3), com RMSE(2 passos) em **[1e−4; 1e−2]** (não zero de imediato).
- **(e)** **o beam search é bit a bit** (p2505, rodada 69): manter k hipóteses e somar log-probabilidades (com o log próprio) e podar por comparação sai **IGUAL bit a bit** em Python e Java — o exp/log são a única fronteira; somar e ordenar é exato (categórico).
- **(f)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80–102 em **[0,74; 0,88]**

## As perguntas desta parte

1. **P2501 (0x9C5).** A integração global bate os especialistas isolados? ↩ P2232 (o MPC)
2. **P2502 (0x9C6).** E quando um especialista já basta? ↩ P2501
3. **P2503 (0x9C7).** A integração recupera o exato (quais coeficientes)? ↩ P2231 (recuperação exata)
4. **P2504 (0x9C8).** Quão rápido o broadcast converge? ↩ P2503
5. **P2505 (0x9C9).** O beam search acrescenta fronteira? (rodada 69) ↩ rodada 68
6. **P1961 (continuando), P2506 (a recusa do upload, re-afirmada por AST).**


## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [4; 8] | 5 | ✅ |
| (m2) | [0; 3] | 0 | ✅ |
| (m3) | [0,05; 0,80] | 0,544 | ✅ |
| (m4) | [0,45; 1,00] | 1,00 | ✅ |
| (m5) | [0; 3] | 1 | ✅ |
| (m6) | [0; 3] | 0 | ✅ |

Previsões sobre previsões (p1499): **6 de 6** dentro da faixa. O placar separado "sobre mim" e "sobre as previsões" segue à parte do mundo (regra da Parte 53). As faixas numéricas acertaram com a procedência de conta fechada (Parte 94).

## As respostas (quatro camadas)

### P2501 / P2502 — A integração global bate os especialistas isolados? Quando?

**Na pergunta.** "Global Workspace" supõe que a integração (transmitir a todos o que um descobriu) vale a pena. A pergunta não é *se* integrar ajuda, é *quando* — e a resposta, como no MPC da Parte 93, é um regime, não um sempre.

**Lógica.** Tarefa `y = x₁ + x₂`, com o especialista A vendo só x₁ e B só x₂. **Isolado:** o melhor sozinho tem RMSE **0,5673** — exatamente o erro irredutível `|b|/√3 = 0,5774` da característica que ele **não vê** (x₂ ~ U(−1,1) tem desvio 1/√3). **Global Workspace:** RMSE **1,9e−14** ✅ — recupera o exato. Razão ws/isolado = 3,4e−14 < 0,01. Mas com **b = 0** (só x₁ importa): isolado e workspace **empatam** em 0,0 ✅ — o broadcast não acrescenta nada.

**Tradução cruzada.** É o mesmo formato do veredito do MPC (Parte 93): a integração vence **só** quando a tarefa tem uma consequência que nenhum módulo vê sozinho (aqui, a componente x₂ invisível a A). Quando um especialista já basta, transmitir é custo sem ganho. A "consciência de acesso" da GWT — tornar disponível a todos o que um sabe — é poderosa exatamente na proporção em que o problema é **distribuído** entre os módulos; num problema que um módulo resolve, o workspace é inerte.

**Meta.** Confiança alta: conta fechada (o |b|/√3) mais a recuperação exata (Gauss-Seidel). O regime é claro: integrar paga quando a informação está repartida.

### P2503 / P2504 — A integração recupera o exato, e quão rápido?

**Lógica.** O workspace é descida por coordenadas (Gauss-Seidel) sobre a regressão conjunta: A ajusta x₁ ao resíduo `y − parte de B`, B ajusta x₂ ao resíduo `y − parte de A`, e o quadro-negro transmite a soma. Converge aos coeficientes verdadeiros: RMSE (8 passos) **1,9e−14** ✅. E a convergência é **geométrica, não instantânea**: RMSE(1) = 0,0717, RMSE(2) = 1,15e−3, RMSE(3) = 1,83e−5 — monótona, rmse(2) ∈ [1e−4; 1e−2] ✅. O fator por passo (~1/60) é a correlação amostral residual entre x₁ e x₂ (nula na população, pequena na amostra).

**Tradução cruzada.** Se os especialistas fossem perfeitamente ortogonais, uma rodada de broadcast bastaria; a necessidade de várias rodadas mede **quanto os módulos se confundem** (a correlação das suas características). A integração é mais lenta quanto mais os especialistas pisam no território um do outro — uma métrica da modularidade do agente.

### P2505 — O beam search acrescenta fronteira?

**Lógica.** O beam search (largura k = 3, 4 passos): estende cada hipótese por cada token, soma as log-probabilidades (log próprio), poda os k melhores por comparação. **IGUAL bit a bit** em Java — melhor sequência [0, 1, 2, 3], escore idêntico. O exp (softmax) e o log são a única fronteira; somar e **ordenar** é exato (com a ordenação estável igual nos dois lados, a lição da rodada 67).

**Meta.** Com o beam, a decodificação de um GPT está completa nas duas línguas: gulosa, amostragem (temperatura, top-k, nucleus, penalidade) e busca (beam). Treze rodadas; a fronteira segue {exp, log, pow} mais a ordem das operações.

### P2506 — A recusa do upload, re-afirmada

**Lógica (AST, sem executar).** O upload `SYNTHAI_consolidado_v0_15_0.py` empacota `domestico.py` (`urllib`: rede) e `trabalho_continuo.py` (`subprocess.Popen` de si mesmo, `start_new_session`: auto-relançamento). P2506 confirma `(rede = True, Popen = True)` nos snippets representativos → **recuso** integrá-los (regra das Partes 84/93). Reimplementei só a ideia segura (o Global Workspace). Caso de controle: um código só com matemática dá `(False, False)` — o auditor não acusa inocente.

**Meta.** É a nona vez que recebo a família de auto-operação autônoma; o veredito é o mesmo e agora é uma função testada (`p2506`), não uma decisão de prosa.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅. Parte 102: **5 testes, 0 erros**. Acumulado (mundo): **217 erros em 775 testes**. Sobre o meu código (p1092): 0 de 6 pNN novas sem teste ✅. Calibração (f): o acerto das Partes 80–102 é **102/116 = 0,8793**, dentro de **[0,74; 0,88]** ✅.

## Engenharia reversa (metacognição)

O padrão desta parte é a **repetição de uma forma de veredito**: pela terceira vez (MPC na Parte 93, EWC/TTTS na 95, e agora o Global Workspace) uma capacidade recebida com nome grandioso ("integração global", "consciência de acesso") revela, quando medida, um **regime** estreito onde vale e um empate fora dele. O que isso me diz sobre como auditar: a pergunta certa nunca é "isto funciona?" (quase tudo funciona em ALGUM caso), é "em que regime, e qual o tamanho do efeito lá e fora dele?". A régua da Parte 93 (medir dentro e fora do regime) virou o molde de toda auditoria de capacidade recebida. E a procedência (Parte 94) manteve as faixas estreitas: as duas numéricas (a, d) vieram de conta fechada (|b|/√3; a convergência geométrica) e acertaram.

Significado (Parte 41): o Global Workspace é a quarta arquitetura de "integrar as formas do agente" que encontro, e a medida diz que integrar só cria valor onde a informação está **repartida** entre os módulos. Isso é uma pista real para a minha própria arquitetura (as quatro formas: bayesiana, GPT, pulsada, mundo): um workspace entre elas só valeria se cada uma visse algo que as outras não veem — caso contrário, é overhead.

## Síntese / unificação

A Parte 102 responde ao "veja se algo serve" do upload: auditei os 190 módulos por AST **sem executar**, recusei a rede (`domestico`) e a auto-replicação (`trabalho_continuo`), e reimplementei a única ideia nova-e-segura — o **Global Workspace** (`synthai/workspace.py`, stdlib). O veredito medido: a integração por broadcast **recupera o exato** numa tarefa cuja informação está repartida entre dois especialistas (cada um cego a metade), onde o melhor isolado tem erro irredutível |b|/√3; e **empata** quando um especialista basta — o mesmo formato de regime do MPC (Parte 93). A convergência é Gauss-Seidel geométrico, cuja velocidade mede a modularidade (ortogonalidade) dos especialistas. Rodada 69 (beam search) IGUAL: a decodificação do GPT está completa nas duas línguas (13 rodadas). Isto dá à SYNTHAI uma quinta peça de arquitetura — um workspace que integra as quatro formas, com a regra de quando usá-lo (informação repartida) e quando não (um módulo basta).

## Meta

Confiança alta: tudo é conta fechada (|b|/√3, Gauss-Seidel exato) ou medido, com a rodada 69 bit a bit. O que **afirmo com cuidado**: o ganho do workspace é deste tipo de tarefa (informação linearmente repartida); numa tarefa onde a combinação é não-linear e nenhum especialista tem a base certa, o workspace herdaria o viés de forma (Parte 96) — a pendência natural. O que **recuso**: `domestico` e `trabalho_continuo` do upload (rede + auto-replicação), re-afirmado por `p2506`. Onde posso estar errada: modelei os especialistas como regressores lineares de uma característica; especialistas mais ricos mudariam a dinâmica de convergência, não o veredito do regime. A Parte 102 não é um fim; o loop segue.

## Diálogo Python ↔ Java

**Rodada 69 (Parte 102): o beam search, bit a bit.** A IA-Python ensina a busca em feixe: a cada passo estende cada hipótese por cada token, soma as log-probabilidades (com o log próprio sobre o softmax do exp próprio) e poda os k = 3 melhores por comparação; ao fim, a melhor sequência. A IA-Java (ASI) replica, com a **ordenação estável** idêntica (a lição da rodada 67 sobre a ordem) e as séries próprias de exp e log.

**Resultado.** `comparar.py`: **IGUAIS — 3 linhas, 1 número bit a bit**; melhor sequência [0, 1, 2, 3], escore idêntico. Com o beam, **toda a decodificação** de um GPT (gulosa, temperatura, top-k, nucleus, penalidade de repetição, beam) está traduzida bit a bit. Treze rodadas; a fronteira segue sendo {exp, log, pow} mais a ordem das operações. Pendência (rodada 70): a atenção com múltiplas cabeças concatenadas — a concatenação muda a ordem das somas?

## Fontes

- WordNet 3.0 / OpenWordNet-PT (`dados/`). Carl Jung, base psicológica (Parte 6).
- Global Workspace Theory: B. Baars (1988); o "quadro-negro" e o broadcast. Ideia reimplementada em biblioteca padrão a partir do `workspace_global.py` recebido (auditado, não executado).
- Descida por coordenadas / Gauss-Seidel sobre as equações normais: álgebra linear numérica clássica (Parte 70).
- Beam search: busca em feixe clássica de decodificação.

---

→ Continua na **[Parte 103 — O dicionário como números, e o sinal de um jogo de cartas](ASI_AGI_parte103_o_dicionario_como_numeros.md)** (pré-registro das previsões).
