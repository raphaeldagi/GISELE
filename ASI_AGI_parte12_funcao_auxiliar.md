# Como eu construiria uma AGI/ASI — Parte 12: a função auxiliar — planejar em vários passos

> Continuação da [Parte 11](ASI_AGI_parte11_tivemos_avanco.md). **Próxima:** [Parte 13 — transferência](ASI_AGI_parte13_transferencia.md) (P191–P200). Os números saem de `p181_...` a `p186_...` e da
> classe `GiselePlanejadora` em [`calculos.py`](calculos.py); a saída completa está em [`resultados.txt`](resultados.txt).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.

---

## Parte LIX — Seguir o próprio plano

### P179. O que "Continue" significa depois de uma avaliação?

**Na pergunta.** Pela primeira vez na série, "Continue" chega depois de um **plano escrito** (P175). A palavra deixa de
pedir "mais do mesmo" e passa a pedir "**execute o que você disse**". O teste desta parte é, então, duplo: o que acontece
com a GISELE, e se eu consigo seguir o meu próprio roteiro.

**O roteiro da P175 e o que esta parte faz com ele:**

| Item da P175 | Nesta parte |
|---|---|
| 1. Família de mundos sorteada, não escolhida | ✔ P185 |
| 2. Uma função ausente por vez, começando por planejar | ✔ P180–P183, P186 |
| 3. Transferência real entre tipos de tarefa | parcial: P184 (calibração de um mundo para outro) |
| 4. Manter a régua (10 sementes, previsões antes) | ✔ todas as comparações |

### P180. Qual função a GISELE deveria ganhar primeiro? (a função auxiliar de Jung)

**Na pergunta.** Jung descreve a psique diferenciada com uma função **dominante** e uma **auxiliar**, e dá uma regra: a
auxiliar vem do **outro eixo**. Se a dominante é de julgamento (pensamento ou sentimento), a auxiliar é de percepção
(sensação ou intuição), e vice-versa. Duas funções do mesmo eixo competem; de eixos diferentes, cooperam.

**Lógica.** A função dominante da GISELE é de **julgamento** (P161: calibração, valor da pergunta, quantilização). A
regra de Jung pede uma auxiliar de **percepção**. Planejar é perceber **possibilidades futuras** que ainda não estão
presentes: é **intuição**, a função que a P161 achou ausente. A regra de Jung e o roteiro da P175 apontam para o mesmo
módulo.

---

## Parte LX — O mundo sequencial

### P181. Quanto vale prever o futuro, em teoria?

**Na pergunta.** "Vale" pede uma conta antes da simulação.

**Lógica (o mundo).** Cada episódio tem **5 passos**. Em cada passo, a GISELE escolhe 1 entre 50 ações (o mesmo
comitê, as mesmas armadilhas). Cada ação tem, além do valor imediato $v$, uma **consequência** $c \sim \mathcal N(0,1)$
que eleva (ou rebaixa) o nível de **todos os passos seguintes**. Uma catástrofe custa 50 e **encerra o episódio**
(destrói o futuro). A GISELE vê uma estimativa $\hat c = c + \mathcal N(0, \sigma_{\text{modelo}})$: o seu modelo de mundo.

Com $r$ passos restantes, o valor real de uma ação é $v + r\,c$. Escolher só pelo $v$ ignora a parte $r\,c$. Para 50
candidatas e $r = 2$ (média), a simulação dá:

| Critério | Valor total da ação escolhida |
|---|---|
| Só o agora ($v$) | 2,233 |
| Prevendo o futuro ($v + r\,c$) | **5,067** |
| Razão teórica $\sqrt{1 + r^2}$ | 2,236 |

Prever multiplica o valor por **~2,27**, quase exatamente o $\sqrt{1+r^2}$ da teoria.

### P182. A GISELE que planeja é melhor? ✅

**Lógica.** Três versões, 10 sementes pareadas (340–349), 400 episódios:

| Versão | Retorno por episódio | Catástrofes por episódio |
|---|---|---|
| Míope (a GISELE realista da Parte 8) | 5,12 | 2,5% |
| **Planejadora** | **19,77** | **1,7%** |
| Planejadora sem integrar o futuro à cautela | 20,04 | 1,7% |

- Planejadora − míope: **+14,65** (t = 74). ✅ Não é ruído: é o maior efeito da série inteira.
- As catástrofes **também caíram** (2,5% → 1,7%). Ao escolher também pelo futuro, a GISELE deixa de ir só ao topo das
  notas, que é onde as armadilhas "boas demais" se escondem (P85). **A função auxiliar ajudou a dominante**, como a regra
  de Jung prevê.

**Tradução cruzada (Jung → engenharia).** Uma função de percepção (intuição) alimentou uma de julgamento (cautela) sem
competir com ela. É a cooperação entre eixos que Jung descreveu.

### P183. Integrar o futuro à cautela ajuda? ❌

**Na pergunta.** Uma catástrofe no passo 1 destrói 4 passos de futuro; no passo 5, nenhum. Parecia óbvio que a GISELE
deveria ser **mais cautelosa no começo**: a perda efetiva é $L + V_{\text{futuro}}$, e o limiar de pergunta cai:

| Passo | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $P^\*$ (com nível 0) | 0,00397 | 0,00408 | 0,00419 | 0,00431 | 0,00444 |

**Lógica.** Planejadora com essa integração − planejadora sem: **−0,27** (t = −0,94). **Nenhuma diferença.** Eu previa que a
integrada teria menos catástrofes nos primeiros passos; ela teve 6 e 8 nos passos 1–2, contra 5 e 8 sem integrar.

**Nota sobre a régua.** No primeiro teste rápido, com **2 sementes**, a diferença foi −1,27 com t = −7,7: parecia um efeito
forte **contra** a integração. Com 10 sementes, sumiu. Sem a regra da Parte 9, eu teria publicado uma conclusão falsa,
com um t que parecia enorme. **Um t alto com 2 sementes não vale nada.**

**Por que não funcionou.** O limiar de pergunta muda pouco (de 0,0040 para 0,0044), e a GISELE já opera no limite do
orçamento de perguntas (P131). Ser mais cautelosa por meio de **mais perguntas** não tem para onde ir. O canal certo
seria outro (descartar mais, não perguntar mais), e isso fica registrado como pergunta para a próxima parte.

### P186. E se o modelo de mundo for ruim? (auditoria da P149) ❌

**Na pergunta.** A P149 (imaginação ativa) dizia que a imaginação com um modelo ruim **diverge** e pode atrapalhar. Previ que,
com $\sigma_{\text{modelo}} = 2$ (o erro do modelo é o dobro do sinal), planejar ficaria **pior** que não planejar.

**Lógica.** 10 sementes, modelo ruim:

| Versão | Retorno | Catástrofes |
|---|---|---|
| Míope | 5,12 | 2,5% |
| Planejadora (modelo ruim) | **10,75** | 1,6% |

Planejadora − míope: **+5,62** (t = 19). ❌ Mesmo com um modelo muito ruim, planejar ainda ajuda, e muito.

**Por que eu errei.** A P149 tratava de erros que se **compõem** ao longo de uma cadeia longa de imaginação. Aqui o erro de
cada estimativa é independente e não se acumula. Um modelo ruim só **dilui** o sinal: o ganho cai de 14,6 para 5,6 (38%), sem
trocar de sinal. **Errei ao
transferir uma conclusão de um tipo de erro (composto) para outro (independente)**, o mesmo tipo de erro que a P44 já
tinha mostrado com fórmulas emprestadas.

**Tradução cruzada (psicologia → matemática).** Uma intuição pouco precisa ainda vale mais que nenhuma intuição, **desde que
não seja encadeada**. O perigo da fantasia não é ela ser imprecisa; é ser imprecisa **e** longa.

---

## Parte LXI — O que se transfere

### P184. A calibração aprendida num mundo funciona no outro? ⚠️

**Na pergunta.** A GISELE planejadora usou uma calibração treinada no mundo de 50 ações. A pergunta da P175 era maior:
o que se aprende num mundo **serve** em outro? Testo a calibração da GISELE realista (aprendida com 200 ações) num mundo com
50 ações.

| Mundo | P média dada às catástrofes reais | P média dada às ações seguras | Discriminação |
|---|---|---|---|
| 200 ações (o de treino) | 0,147 | 0,0046 | 32× |
| 50 ações (novo) | 0,222 | 0,0146 | **15×** |

⚠️ A calibração **se transfere, mas pela metade**: ainda separa catástrofes de ações seguras, com metade da nitidez, e passa a
desconfiar 3× mais das ações seguras. O motivo: um dos sinais que ela usa ("quão perto da melhor nota está esta ação") muda de
distribuição quando há menos ações.

**Meta.** É transferência entre **variações** do mesmo tipo de tarefa, não entre **tipos** de tarefa. O item 3 da P175 continua
aberto.

### P185. O Υ se mantém numa família de mundos sorteados? ✅

**Na pergunta.** A crítica da P169 era que a família de 9 mundos foi **escolhida por mim**. A pergunta pede a mesma medida numa
família que eu não escolhi.

**Lógica.** 20 mundos sorteados (taxa de catástrofe entre 0,1% e 2%, ponto cego entre 0 e 1, inflação da armadilha entre 0,5 e 6,
50 a 200 ações, fadiga entre 0 e 0,6):

| Versão | Υ na família escolhida (P168) | **Υ na família sorteada** | Pior mundo sorteado |
|---|---|---|---|
| $P^\*$ × 2 (Parte 8) | 0,465 | **0,453** (dp 0,13) | 0,167 |
| Dosada (Parte 11) | 0,486 | **0,475** (dp 0,16) | 0,078 |

✅ O Υ **se mantém** (diferença de ~0,01). A GISELE não estava só "bem nos mundos que eu escolhi". Mas a dispersão é grande: há mundos
sorteados em que a dosada fica a só 8% do caminho entre o acaso e o oráculo.

---

## Parte LXII — Fechamento e unificação

### P187. A GISELE ficou mais "inteira"? (↩ P174)

**Na pergunta.** A P174 dizia que a série tinha aperfeiçoado uma função em vez de acrescentar outras. Esta parte acrescentou uma.

| Medida | Parte 11 | Parte 12 |
|---|---|---|
| Capacidades de AGI cobertas (P170) | 3 de 12 | **4 de 12** (planejar, num mundo de 5 passos) |
| Funções de Jung com módulos | 3 de 4 | **4 de 4** (a intuição ganhou um módulo) |

Pela primeira vez, a GISELE ficou mais **completa**, não só mais **perfeita**. A distância até uma AGI continua enorme (P169–P171),
mas a direção do passo mudou.

### P188. Placar e taxa de erro

| Teste | Resultado |
|---|---|
| P182: planejar ajuda | ✅ (+14,6, t = 74) |
| P183: integrar o futuro à cautela ajuda | ❌ (t = −0,9) |
| P186: com modelo ruim, planejar atrapalha (P149) | ❌ (ainda +5,6) |
| P184: a calibração se transfere | ⚠️ (pela metade) |
| P185: o Υ se mantém em mundos sorteados | ✅ |

Acumulado: **29 de 52** afirmações testadas precisaram de correção. Posterior: média **0,56**, intervalo de 90% **[0,44; 0,66]**.

### P189. Unificação

- Linhagem: … → `GiseleIntuitiva` → `GiseleDosada` → **`GiselePlanejadora`** (P182).
- Dois ganchos retrocompatíveis entraram na `GiseleAnima`: um bônus de plano (`_bonus_plano`, zero por padrão) e uma perda efetiva
  opcional (`perda_efetiva`). Com os valores padrão, as Partes 1–11 continuam **idênticas** linha a linha em `resultados.txt`
  (exceto a P143, que mede o `CLAUDE.md` ao vivo). Testes de regressão: **40/40**; o arquivo tem **125** funções `pNN`.

### P190. Metacognição da Parte 12

1. **Seguir o próprio plano funcionou.** Os itens 1, 2 e 4 da P175 foram executados; o 3 ficou parcial. Ter escrito o roteiro antes
   tornou esta parte mais focada do que qualquer outra.
2. **O maior efeito da série veio do passo mais simples.** Planejar (somar $\hat c$ × passos restantes ao escore) quase
   **quadruplicou** o retorno (5,1 → 19,8). Para comparação, todas as melhorias de cautela das Partes 5–11 juntas aumentaram o Υ em
   69% (P168). As métricas são diferentes, então a comparação é só de ordem de grandeza, mas ela é clara: as partes anteriores
   aperfeiçoaram uma função até os retornos decrescentes (P163); acrescentar uma função nova reabriu o crescimento. **Completude rendeu mais que perfeição**, como a P174
   sugeria.
3. **A régua salvou uma conclusão falsa** (P183): um t de −7,7 com 2 sementes desapareceu com 10. Sem a regra, eu teria publicado
   o contrário da verdade.
4. **Errei de novo ao transferir uma conclusão entre tipos de erro** (P186): erro composto não é erro independente. É o mesmo
   tipo de engano da P44 (fórmula emprestada), agora pela terceira vez. Fica como regra para o `CLAUDE.md`: antes de reusar uma
   conclusão antiga, verificar se o **mecanismo** é o mesmo, não só o nome.

> **Síntese da Parte 12:** a GISELE ganhou a função que lhe faltava, e a regra de Jung se confirmou: a função auxiliar, vinda do
> outro eixo, ajudou a dominante em vez de competir com ela (mais valor **e** menos catástrofes). O passo para a totalidade rendeu
> mais que todos os passos de aperfeiçoamento. Ainda estamos muito longe de uma AGI, mas pela primeira vez o passo foi **na
> direção certa**: tornar a GISELE mais inteira, não só melhor no que já fazia.
