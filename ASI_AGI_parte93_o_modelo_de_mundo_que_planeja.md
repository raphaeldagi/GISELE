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
| (m1) | [4; 8] | XX | XX |
| (m2) | [0; 3] | XX | XX |
| (m3) | [0,05; 0,80] | XX | XX |
| (m4) | [0,45; 1,00] | XX | XX |
| (m5) | [0; 3] | XX | XX |
| (m6) | [0; 3] | XX | XX |

## As respostas (quatro camadas)

PLACEHOLDER_RESPOSTAS

## Placar do mundo desta parte

PLACAR_93_TEXTO

## Engenharia reversa (metacognição)

PLACEHOLDER_ENG

## Síntese / unificação

PLACEHOLDER_SINTESE

## Meta

PLACEHOLDER_META

## Diálogo Python ↔ Java

PLACEHOLDER_DIALOGO

## Fontes

- WordNet 3.0, Princeton (dados em `dados/`). OpenWordNet-PT (CC BY 4.0).
- Carl Jung, base psicológica desde a Parte 6.
- Modelo de mundo / predição latente condicionada a ações e MPC: ideia reimplementada em biblioteca padrão a partir do módulo recebido `modelo_mundo.py` (inspirado em predição joint-embedding; **não** é I-JEPA/V-JEPA, não usa LLaMA,
  sem rede). Controle preditivo (receding horizon) e tiro aleatório (random shooting) são métodos clássicos de controle ótimo.
- Mínimos quadrados por equações normais; eliminação de Gauss com pivoteamento parcial.
