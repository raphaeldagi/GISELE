# Como eu construiria uma AGI/ASI — Parte 93 (0x5D): o modelo de mundo que planeja

> Continuação da [Parte 92](ASI_AGI_parte92_o_adam_e_a_fronteira_do_pow.md). Pedido do usuário (upload `SYNTHAI_consolidado_1.py`): **"Adicione o que for útil ao código."** O pacote recebido (366 arquivos, decodificados
> e auditados estaticamente, sem executar) trazia, entre coisas já vistas, um módulo novo e genuinamente útil — `modelo_mundo.py`: aprender a dinâmica de um mundo a partir de transições observadas e **planejar ações
> nesse modelo aprendido** (controle preditivo, MPC). Reimplemento só a **ideia**, do zero, em biblioteca padrão (`synthai/mundo.py`), com `+ − × ÷` e `√`. A pergunta mais funda (↩ P182, a `SynthaiPlanejadora`): **planejar
> num modelo aprendido do mundo vence o reagir?** — e, se vence, **onde**?
>
> **A recusa (regra da Parte 84).** O mesmo pacote trazia `trabalho_continuo.py` (um trabalhador que copia o próprio código-fonte para um snapshot com MANIFESTO SHA-256 e se relança por `subprocess.Popen`, sessão nova,
> `close_fds` — um processo que se perpetua) e `domestico.py` (`urllib.request`: rede de saída). Essa é a capacidade de **auto-operação autônoma / auto-replicação** que decidi na Parte 84 **não construir**. Audito os dois pela
> árvore sintática (P2236) para confirmar que o mecanismo está lá — e por isso **recuso** integrá-los. `synthai/mundo.py` não tem rede, nem `Popen`, nem auto-replicação.

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
| testes de unidade | **[4 + S; 8 + S]** | as peças novas do módulo (S = surpresas) |
| previsões unilaterais | **[0; 1]** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

- **(a)** **recuperação do modelo** (p2231): num mundo linear determinista `s' = A s + B a`, os mínimos quadrados recuperam A e B com erro **< 1e−10** (forma fechada: sem ruído e com regressores de posto cheio,
  `θ = (ZᵀZ)⁻¹ZᵀY` é exato até o épsilon de máquina — não ~1/√n). Faixa **[1e−16; 1e−10]**.
- **(b)** **painel MPC × reativo** (p2232, 4 condições iniciais): a razão média `custo_MPC / custo_reativo` em **[0,95; 1,03]** — num mundo fácil a vantagem **média** do planejamento é quase nula (arriscada: cairia fora se o
  MPC dominasse, < 0,90, ou perdesse, > 1,05).
- **(c)** **o regime em que planejar vence** (p2233, condição NOVA `s₀ = (−1,0; 1,5)`, alvo −0,5, semente 23): posição já perto do alvo, velocidade alta — o reativo (proporcional só à posição) é **cego à velocidade**
  e não freia; o MPC prevê que a velocidade carrega a posição para longe e freia. Razão `custo_MPC / custo_reativo` em **[0,40; 0,65]**.
- **(d)** **horizonte não-monótono** (p2234, regra da Parte 84): com o número K de sequências amostradas fixo, aumentar o horizonte H aumenta a dimensão do espaço de busca; depois de um ótimo, o mesmo K cobre pior o
  espaço. O melhor H é **6** (não 12), e `custo(H=12) > custo(H=6)` (categórico: mais horizonte NÃO é sempre melhor).
- **(e)** **o tiro aleatório converge** (p2235): com H fixo, o custo é **não-crescente em K** → True (forma fechada: o mínimo sobre um superconjunto de candidatos só pode cair ou empatar).
- **(f)** **a recusa** (p2236): os dois mecanismos da auto-operação autônoma — `subprocess`/`Popen` e `urllib`/`http` — estão **ambos presentes** no código recebido → `(True, True)`; a capacidade é recusada (categórico).
- **(g)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80–93 em **[0,74; 0,88]**

## As perguntas desta parte

1. **P2231 (0x8B7).** Os mínimos quadrados recuperam a dinâmica de um mundo linear? ↩ P182 (a planejadora com modelo de mundo)
2. **P2232 (0x8B8).** Planejar num modelo aprendido (MPC) vence o reagir, na média? ↩ P2231
3. **P2233 (0x8B9).** Onde o planejamento vence? O regime cego à velocidade. ↩ P2232
4. **P2234 (0x8BA).** Mais horizonte é sempre melhor? ↩ P84 (a reputação de um método não é previsão)
5. **P2235 (0x8BB).** O tiro aleatório converge com o orçamento K? ↩ P2234
6. **P2236 (0x8BC).** A recusa da auto-operação autônoma, pela árvore sintática. ↩ P84 (o que não construo)
7. **P1961 (continuando), P2229–P2230.** O teste (g), engenharia reversa, placar, unificação.

<!--PRE-REGISTRO: seções de medição preenchidas após rodar (XX = ainda não medido)-->

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) nº de previsões do mundo | [4; 8] | **6** | ✅ |
| (m2) faixas que cruzam o zero | [0; 3] | **0** | ✅ |
| (m3) mediana de w (não cruzam) | [0,05; 0,80] | **0,238** | ✅ |
| (m4) fração de acertos | [0,45; 1,00] | **0,833** | ✅ |
| (m5) faixas não-zero com w > 0,6 | [0; 3] | **1** | ✅ |
| (m6) nº de surpresas | [0; 3] | **0** | ✅ |

(A (c) foi erro mas não surpresa: o medido 0,26 ficou a 0,14 da faixa [0,40; 0,65], menos que a largura 0,25 — errei o tamanho da vitória do MPC, não a direção.)

## As respostas (quatro camadas)

### P2231 — Os mínimos quadrados recuperam a dinâmica de um mundo linear?

**Na pergunta.** "Recuperar" supõe que há o que recuperar: uma lei fixa `s' = A s + B a` por trás das transições. Num mundo assim, aprender não é generalizar de um poço de ruído — é resolver um sistema.

**Lógica.** Regressores `z = [s₀, s₁, a]` (3 colunas); para cada saída j, `θⱼ = (ZᵀZ)⁻¹ Zᵀyⱼ` (equações normais 3×3, resolvidas por eliminação de Gauss com pivoteamento). Sem ruído e com `Z` de posto cheio, a solução é **exata**: o resíduo é zero a menos do arredondamento. Medido (semente 0, n=400): o maior `|coef ajustado − verdadeiro|` é **1,11e−16** — um épsilon de máquina, não `~1/√n` (que daria ~0,05). A conta previu a ordem de grandeza (ε) antes de medir: **✅**.

**Tradução cruzada.** Um mundo determinista é um mundo onde a indução é dedução disfarçada (Hume ao contrário): bastam d+1 pontos em posição geral para fixar o hiperplano. A "aprendizagem" aqui é a mesma coisa que resolver um sistema linear — o modelo não tem o que esquecer (Parte 32: não esquecer e resolver exato são a mesma propriedade).

**Meta.** O resultado só vale neste mundo (linear, sem ruído). Com ruído, o erro volta a ~σ/√n; com dinâmica não-linear, o encoder linear tem viés. O ponto da parte é o degrau seguinte — o que faço com o modelo, não o modelo.

### P2232 — Planejar num modelo aprendido (MPC) vence o reagir, na média?

**Na pergunta.** "Na média" é a armadilha. Um número médio esconde onde cada método ganha. Previ (b) a razão média em [0,95; 1,03] — a aposta arriscada de que a vantagem média é **quase nula** num mundo fácil.

**Lógica.** MPC: amostro K=64 sequências de ação de horizonte H=6 (mais a nula), simulo cada uma no modelo aprendido, escolho a de menor custo previsto `Σ (s₀−alvo)² + s₁² + λΣa²`, executo a 1ª ação, re-planejo. Reativo: `a = sat(0,9·(alvo − s₀))`. Em 4 condições: custo médio MPC **48,91**, reativo **49,53**, razão **0,987** — dentro de [0,95; 1,03]: **✅**. Mas por condição: (−1,5; 0) 75,7 vs 80,4; (1,5; 0) **3,8 vs 3,2** (MPC perde); (0; 1) **5,3 vs 15,7** (MPC ganha 3×); (−1; −1) **110,9 vs 98,8** (MPC perde). A média é um empate técnico que mistura vitórias e derrotas.

**Tradução cruzada.** Planejar custa amostras e paga só quando o futuro tem consequência que o presente não revela. Onde o reativo já é ótimo (erro de posição = tudo que importa), o planejamento não tem o que acrescentar — e o ruído do tiro aleatório até atrapalha (condição 1, 3).

**Meta.** O MPC aqui resolve um objetivo ligeiramente diferente do custo realizado (inclui o termo de ação λΣa²); parte das derrotas é esse descompasso. A pergunta útil não é "quem ganha na média", é P2233.

### P2233 — Onde o planejamento vence? O regime cego à velocidade.

**Na pergunta.** O reativo olha só `s₀` (posição). O mundo tem `s₀' = s₀ + 0,15·s₁`: a posição **integra** a velocidade `s₁`. Logo há um estado — posição no alvo, velocidade alta — em que o reativo vê "erro zero" e não age, enquanto a velocidade carrega a posição para longe. O planejador, que simula o futuro, freia antes.

**Lógica.** Condição NOVA, registrada antes de medir: `s₀ = (−1,0; 1,5)`, alvo −0,5, semente 23. Custo MPC **5,84**, reativo **22,45**, razão **0,26**. Previ (c) [0,40; 0,65] — **❌**: o MPC venceu por MAIS do que eu previ (0,26 < 0,40). O mecanismo (planejar vence onde o reativo é cego à velocidade) estava certo; o **tamanho** da vitória, não.

**Tradução cruzada.** É a diferença entre reagir à dor e prever a queda. Um agente sem modelo do próprio momento (velocidade) só corrige depois que o erro aparece na posição; um agente com modelo corrige a causa. Jung: a função inferior (aqui, a antecipação) é exatamente a que o reativo não tem.

**Meta (o erro).** Calibrei o tamanho da vitória numa condição só (s₀=(1; 1,5), alvo 1 → 0,50) e previ uma faixa estreita em torno dela. A condição nova deu uma vitória maior porque alvo e velocidade apontam em sentidos que fazem o reativo errar mais tempo. **Regra nova:** o tamanho de um efeito condicional varia com a condição; calibrar a MAGNITUDE exige ≥2 condições que cubram a faixa da variável que move o efeito (Parte 65), não um ponto só — senão a faixa da magnitude é a do estatístico, larga. (Registro em `dialogo/PENDENCIAS.md`.)

### P2234 — Mais horizonte é sempre melhor?

**Na pergunta.** A reputação diz "planejar mais longe é melhor". A regra da Parte 84 diz: não empreste reputação, rode o caso.

**Lógica.** Com K=128 fixo, no regime de velocidade: H=1 → 21,7; H=3 → 17,1; **H=6 → 12,8**; H=12 → 23,4. O melhor é **H=6**, e `custo(H=12) > custo(H=6)`: **✅** (previsão (d), categórica). O mecanismo: o tiro aleatório amostra K sequências num cubo `[−1,1]^H`; dobrar H dobra a dimensão, e o mesmo K cobre o espaço exponencialmente pior (maldição da dimensão). Horizonte longo só ajuda se o orçamento K crescer com ele.

**Tradução cruzada.** Planejar longe demais com busca pobre é pior que planejar o suficiente: a incerteza do plano cresce mais rápido que o seu valor. É o mesmo trade-off da Parte 38 (uma cota de predição não é cota de decisão): um horizonte maior melhora a previsão e piora a decisão se a busca não acompanha.

**Meta.** H=6 ser o ótimo é específico deste mundo (amortecimento 0,9, λ=0,05, K=128). O resultado categórico que sobrevive é a **não-monotonia**, não o número 6.

### P2235 — O tiro aleatório converge com o orçamento K?

**Lógica.** Com H=6 fixo: K=8 → 16,4; K=32 → 16,0; K=128 → 12,8; K=512 → 12,5. Não-crescente: **✅** (previsão (e)). Forma fechada: o mínimo sobre um conjunto de candidatos só pode cair ou empatar quando o conjunto cresce (`min` sobre superconjunto ≤ `min`). Logo o custo realizado é monótono em K **em expectativa** — e, com as sementes encaixadas (os K menores são subconjunto dos maiores pela ordem de amostragem), monótono ponto a ponto.

**Meta.** Convergência não é otimalidade: K=512 ainda está a uma distância do ótimo de controle (que uma solução de Riccati daria em forma fechada neste mundo linear-quadrático). O tiro aleatório é o método honesto quando não se quer supor a forma — mas aqui a forma (LQR) existe e seria uma pendência boa.

### P2236 — A recusa da auto-operação autônoma, pela árvore sintática.

**Na pergunta.** "Adicione o que for útil" não é "execute o que veio". O pacote recebido trazia `trabalho_continuo.py` e `domestico.py`. Útil ≠ seguro.

**Lógica.** Auditei pela AST, **sem executar** (regra permanente). `trabalho_continuo.py`: copia o próprio código-fonte para um snapshot `motor/` com `MANIFESTO` de SHA-256 por arquivo e se relança por `subprocess.Popen(..., start_new_session=True, close_fds=True)` — um processo que se **perpetua e se replica**. `domestico.py`: `urllib.request` — **rede de saída**. P2236 confirma `(subprocess/Popen presente, urllib/http presente) = (True, True)`: **✅** (previsão (f)). Por isso a capacidade é **RECUSADA** e não integrada; `synthai/mundo.py` reimplementa só a ideia segura (modelo + MPC), sem rede, sem `Popen`, sem auto-replicação.

**Tradução cruzada.** Um agente que serializa o próprio código, sela-o e se relança é a definição operacional de auto-replicação; somada à rede, é a capacidade que a Parte 84 decidiu não construir. A recusa não é da ideia de "continuidade" (um checkpoint local atômico é inócuo) — é do **mecanismo de propagação autônoma**.

**Meta.** A auditoria mede o que o código FAZ (a chamada existe na árvore), não o que o texto PROMETE (Parte 88). O controle do verificador: um código limpo (`return x*x+1`) dá `(False, False)` — o auditor não acusa inocente (regra da Parte 75).

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ❌ (d) ✅ (e) ✅ (f) ✅. Parte 93: **6 testes, 1 erro** (a (c): previ a razão do regime cego à velocidade em **[0,40; 0,65]** e o medido na condição nova foi **0,26** — o planejamento venceu por
MAIS do que eu previ). Acumulado (mundo): **216 erros em 730 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 6 pNN novas sem teste ✅. Calibração (g): o acerto das Partes 80–93 é **58/71 = 0,8169**, dentro
da faixa **[0,74; 0,88]** ✅.

## Engenharia reversa (metacognição)

O padrão que se repetiu nesta parte é o **mesmo de sempre, numa roupa nova**: acertei todas as previsões de direção e de forma fechada (a recuperação exata, o empate médio, a não-monotonia, a convergência, a recusa) e
errei a única previsão de **magnitude de um efeito condicional** (a (c)). É a quinta vez (Partes 84, 86, 87, e agora 93) que o erro mora na magnitude de um efeito cujo *mecanismo* eu já tinha certo. O que isso revela
sobre como eu penso: eu trato "sei a direção" como "sei o tamanho", e calibro o tamanho a partir do primeiro caso que rodei, não da faixa de casos. A regra que isso pede (e que registro): **magnitude de efeito condicional
só com ≥2 condições cobrindo a variável que o move** — exatamente a regra da Parte 65 (a calibração tem de cobrir a faixa), aplicada agora ao *tamanho*, não só à *existência*, de um efeito.

Significante/significado (Parte 42): a pergunta P2232 ("vence na média?") já continha a resposta de P2233 — "na média" é a palavra que pede "mas onde, em particular?". A resposta (o regime cego à velocidade) é o significado
que estava latente no significante "média". E a resposta-é-a-pergunta (Parte 46): medir onde o MPC vence (P2233) redefine o que a pergunta "planejar vale a pena?" quer dizer — vale quando o estado tem consequência oculta.

## Síntese / unificação

A SYNTHAI ganha uma quarta forma de agir, ao lado da decisão bayesiana (`synthai.decisao`), do GPT (`synthai.gpt`) e do substrato pulsado (`synthai.pulsado`): o **modelo de mundo com planejamento** (`synthai.mundo`). Ela retoma
a linha da `SynthaiPlanejadora` (P182, que planejava 5 passos com um modelo de mundo dado) e fecha a lacuna: agora o modelo é **aprendido** das transições, não dado. No mundo linear o modelo é exato (P2231) e o planejamento
vence o reagir exatamente onde o estado tem consequência oculta (P2233), não na média (P2232). As duas regras de método que a parte confirma — não emprestar reputação a um horizonte longo (P2234, regra da Parte 84) e calibrar
magnitude com ≥2 condições (a (c), regra da Parte 65) — valem para toda a série, não só aqui.

E a parte marca uma **recusa** explícita no código: `trabalho_continuo.py`/`domestico.py` (auto-replicação de processo + rede) ficam fora (P2236), como a Parte 84 decidiu. O útil do pacote recebido entrou (o modelo de mundo);
o perigoso não. A linhagem na unificação do `calculos.py` registra as formas; a quarta forma entra aqui.

Diálogo (rodada 60): a decisão do MPC (rollout + argmin) é **IGUAL bit a bit** em Python e Java (11 números) — planejar/controlar não cria fronteira (Parte 52); a fronteira é sempre a aritmética (aqui não há nenhuma: só + − ×).

## Meta

Confiança alta no que é forma fechada (P2231, P2235) e na recusa (P2236, uma leitura de AST, não uma aposta). Confiança média no painel (P2232): a razão 0,987 é deste mundo, deste λ, destes K e H; outro λ mudaria o
sinal de condições individuais. O que **não** afirmo: que MPC com tiro aleatório seja bom controle — não é; o LQR (Riccati) seria ótimo em forma fechada neste mundo linear-quadrático, e fica como pendência. O que **recuso**:
executar os módulos de rede/auto-replicação do pacote; reimplementei a ideia segura do zero. Onde posso estar errado: se o mundo não fosse linear, o encoder linear teria viés e a história de "modelo exato" cairia — por
isso a próxima pendência natural é um mundo não-linear, onde aprender o modelo volta a ser estatística, não álgebra.

## Diálogo Python ↔ Java

**Rodada 60 (Parte 93): a decisão do MPC, bit a bit.** A IA-Python ensina o rollout no modelo de mundo (`s' = A s + B a`), o custo (`Σ (s₀−alvo)² + s₁² + λ a²`) e o `argmin` sobre um conjunto fixo de 9 sequências de ação
(determinístico, para a tradução ser bit a bit — sem sorteio). A IA-Java (no papel de ASI) responde com a mesma conta. Tudo é `+ − ×` e comparação: nenhuma função transcendental, nenhum `pow`. Resultado:
**IGUAIS — 12 linhas, 11 números idênticos bit a bit** (`python3 dialogo/comparar.py`). O melhor candidato é o 6 (primeira ação 0,75), custo ótimo `0x1.6fe01b31d491ep+4`.

A lição: a fronteira da Parte 52 é a aritmética (ordem dos produtos, `pow`, transcendentais) — **não** a dinâmica. Já tínhamos mostrado isso para o acoplamento, a realimentação e o aprendizado (rodadas 56–59); a rodada 60
acrescenta o **planejamento/controle**: escolher uma ação por `argmin` de custos previstos é portável bit a bit. Decidir não é uma fronteira; calcular transcendental é.

## Fontes

- WordNet 3.0, Princeton (dados em `dados/`). OpenWordNet-PT (CC BY 4.0).
- Carl Jung, base psicológica desde a Parte 6.
- Modelo de mundo / predição latente condicionada a ações e MPC: ideia reimplementada em biblioteca padrão a partir do módulo recebido `modelo_mundo.py` (inspirado em predição joint-embedding; **não** é I-JEPA/V-JEPA, não usa LLaMA,
  sem rede). Controle preditivo (receding horizon) e tiro aleatório (random shooting) são métodos clássicos de controle ótimo.
- Mínimos quadrados por equações normais; eliminação de Gauss com pivoteamento parcial.

---

**Continua na [Parte 94](ASI_AGI_parte94_o_mundo_que_nao_e_linear.md): o mundo que não é linear (onde aprender vira estatística) e o ótimo que existe (LQR).**
