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

PLACAR_102_TEXTO

## Engenharia reversa (metacognição)

PLACEHOLDER_ENG

## Síntese / unificação

PLACEHOLDER_SINTESE

## Meta

PLACEHOLDER_META

## Diálogo Python ↔ Java

PLACEHOLDER_DIALOGO

## Fontes

- WordNet 3.0 / OpenWordNet-PT (`dados/`). Carl Jung, base psicológica (Parte 6).
- Global Workspace Theory: B. Baars (1988); o "quadro-negro" e o broadcast. Ideia reimplementada em biblioteca padrão a partir do `workspace_global.py` recebido (auditado, não executado).
- Descida por coordenadas / Gauss-Seidel sobre as equações normais: álgebra linear numérica clássica (Parte 70).
- Beam search: busca em feixe clássica de decodificação.
