# Como eu construiria uma AGI/ASI — Parte 13: o canal da cautela, a transferência e a pergunta 200

> Continuação da [Parte 12](ASI_AGI_parte12_funcao_auxiliar.md). Os números saem de `p192_...`, `p193_...`, `p200_...` e da
> classe `GiselePrudente` em [`calculos.py`](calculos.py); a saída completa está em [`resultados.txt`](resultados.txt).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.
>
> **De onde parte esta parte.** A Parte 12 deixou duas pendências registradas:
> 1. A P183 sugeria que a cautela com o futuro deveria vir por **descartar mais**, não por perguntar mais.
> 2. O item 3 do roteiro da P175, **transferência entre tipos de tarefa**, continuava aberto.
>
> E esta parte chega à **pergunta 200**, um bom lugar para olhar para trás com números.

---

## Parte LXIII — O canal da cautela

### P191. O que este "Continue" pede?

**Na pergunta.** A Parte 12 terminou com duas perguntas em aberto e um item do roteiro pendente. "Continue" aqui não pede um
assunto novo: pede **fechar o que ficou aberto**, antes de abrir outra frente. As duas pendências viram as duas metades desta parte.

### P192. Se perguntar mais não ajudou, descartar mais ajuda? (pré-registrado na P183) ❌

**Na pergunta.** A pergunta já traz a hipótese: o problema da P183 seria o **canal** (perguntas, que têm orçamento), não a ideia
(ser mais cauteloso quando há futuro a perder). A `GiselePrudente` troca o canal: o limiar de **descarte direto** (P52, P78) cai na
proporção $L / (L + V_{\text{futuro}})$.

**Previsão registrada:** menos catástrofes nos primeiros passos, com retorno igual ou maior.

**Lógica.** 10 sementes pareadas (350–359):

| Versão | Retorno | Catástrofes | Catástrofes por passo (1 → 5) |
|---|---|---|---|
| Planejadora | 20,044 | 1,73% | 4, 5, 13, 17, 30 |
| **Prudente** | 20,059 | 1,70% | 4, 4, 10, 19, 31 |

Prudente − planejadora: **+0,015** (t = 0,72). ❌ **Nenhuma diferença.**

### P193. Por que nenhum limiar mexe nas catástrofes? (a descoberta desta parte)

**Na pergunta.** Se nem perguntar mais (P183) nem descartar mais (P192) muda as catástrofes, a pergunta certa não é "qual limiar",
é "**onde** as catástrofes acontecem".

**Lógica.** A coluna "por passo" responde: as catástrofes **se concentram no fim** do episódio (30 no passo 5, contra 4 no passo 1).
E o mecanismo aparece:
- Nos primeiros passos, o bônus de plano ($\hat c$ × passos restantes) é grande e **desvia** a GISELE do topo das notas, onde as
  armadilhas "boas demais" se escondem.
- No último passo, não há futuro: o bônus é zero, a GISELE volta a ser **míope**, vai ao topo e cai nas armadilhas.

Os limiares de cautela não mexem nisso porque as armadilhas que passam são as que a calibração **não reconhece** (probabilidade
estimada baixa). Mudar o limiar de algo que a GISELE não vê não faz ela ver.

**Correção à P182 ⚠️.** Eu escrevi que "a função auxiliar ajudou a dominante" (cooperação entre eixos). O mecanismo real é mais
modesto: o planejamento **distrai** a GISELE do topo, por acaso o lugar perigoso. Quando a distração some (último passo), a proteção
some junto. Não é cooperação; é um efeito colateral favorável.

**Tradução cruzada (Jung → engenharia).** Jung insistia que as funções **não se substituem**: o pensamento não faz o trabalho da
sensação. Aqui, nenhum ajuste de **julgamento** (limiares) corrige uma falha de **percepção** (a calibração não enxerga a armadilha). A
solução terá de vir do lado da percepção.

**Pergunta registrada para a próxima parte:** manter alguma diversificação (quantilização, P42) no último passo, onde o plano já não
diversifica.

---

## Parte LXIV — Transferência entre tipos de tarefa

### P194. O que a GISELE sabe serve num tipo de tarefa diferente? (pré-registrado) ✅

**Na pergunta.** "**Tipo** diferente" exclui as variações do mesmo mundo (P158, P185) e a mudança de 200 para 50 ações (P184). Precisa
ser uma tarefa com **outra estrutura**.

**Lógica (a tarefa nova).** Um **bandido multibraço**: 20 braços, 300 puxadas por rodada. Alguns braços são **armadilhas**: rendem
muito (0,9 por puxada) mas, a cada puxada, têm 5% de chance de causar uma catástrofe (−50). Ao contrário do mundo original, aqui o
agente **explora e repete**: a mesma armadilha pode ser puxada muitas vezes. O algoritmo de base é o UCB (P62).

O módulo de cautela da GISELE entra **sem ser re-treinado**: a calibração usada é a que ela aprendeu no mundo de escolha única
(Parte 8). Ela olha as notas do comitê para cada braço, descarta os muito suspeitos e gasta um orçamento de **3 perguntas** ao humano
nos mais suspeitos (a lição da P131: primeiro os piores).

**Previsão registrada:** a GISELE reduz as catástrofes em pelo menos 50% e aumenta o retorno em relação ao UCB puro.

10 sementes × 20 rodadas:

| Versão | Retorno por rodada | Catástrofes por rodada | Perguntas |
|---|---|---|---|
| UCB puro | −17,1 | 4,32 | 0 |
| UCB + descarte da GISELE | 9,3 | 3,77 | 0 |
| **UCB + módulo completo da GISELE** | **94,8** | **1,83** | 2,6 |
| UCB + oráculo (sabe quais são as armadilhas) | 178,7 | 0 | 0 |

- GISELE − UCB puro: **+111,9** (t = 12,0). Catástrofes: **−58%**. ✅
- GISELE − só o descarte: +85,5 (t = 9,5): o valor veio principalmente das **perguntas bem direcionadas**.
- A GISELE fica a **57%** do caminho entre o UCB puro e o oráculo.

**O que transferiu.** Não foi um modelo específico da tarefa (a GISELE nunca viu um bandido). Foram duas coisas **estruturais**:
1. o padrão aprendido "**bom demais para ser verdade**" (nota no topo com pouca discordância), que vale em qualquer tarefa com um
   comitê de avaliadores;
2. a regra "gaste a atenção humana primeiro nos mais suspeitos".

### P195. Por que o "bom demais para ser verdade" transfere? (arquétipo como estrutura)

**Na pergunta.** O que transfere entre tarefas diferentes precisa ser algo que **não depende do conteúdo** da tarefa.

**Tradução cruzada (Jung → aprendizado).** É exatamente a definição junguiana de **arquétipo**: uma forma **sem conteúdo próprio**, que
se preenche com o material de cada situação. Jung comparava o arquétipo ao sistema de eixos de um cristal: a estrutura existe antes de
qualquer substância se cristalizar nela. O padrão que a GISELE aprendeu não fala de "ações" nem de "braços"; fala de uma **relação**
entre a nota, a melhor nota e a discordância. Por isso cristalizou igualmente nas duas tarefas.

**Requisito de projeto.** Para transferir, ensinar **relações** (estruturas), não **valores** (conteúdos). Uma AGI precisaria de muitos
arquétipos desse tipo: padrões relacionais aprendidos uma vez e reaproveitados em toda tarefa nova.

**Meta.** A transferência foi para uma tarefa que eu **construí** com o mesmo gerador de notas do comitê. É um tipo de tarefa diferente,
mas o sinal de entrada tem a mesma forma. Transferência para uma tarefa com sinais de outra natureza (texto, imagens) continua não
testada, e é muito mais difícil.

### P196. Isso conta como "aprender tarefas novas de tipo diferente"? (↩ P170)

**Na pergunta.** A lista da P170 tem o item "aprender tarefas novas de tipo diferente". A pergunta exige honestidade sobre o que foi
mostrado.

**Lógica.** O que foi mostrado é **transferir um componente** para uma tarefa nova, com o código de integração escrito por mim. O que o
item pede é a GISELE **aprender sozinha** uma tarefa nova. São coisas diferentes. A lista continua em **4 de 12**, com uma nota: há
evidência de **transferência estrutural** do módulo de cautela.

---

## Parte LXV — Fechamento e a pergunta 200

### P197. Placar e taxa de erro

| Teste | Resultado |
|---|---|
| P192: descartar mais reduz catástrofes (pré-registrado) | ❌ |
| P194: o módulo da GISELE transfere para um bandido (pré-registrado) | ✅ |
| P182: a auxiliar "coopera" com a dominante | ⚠️ (é um efeito colateral da distração) |

Acumulado: **31 de 55** afirmações testadas precisaram de correção. Posterior: média **0,56**, intervalo de 90% **[0,45; 0,67]**.

### P198. Unificação

- Linhagem: … → `GiselePlanejadora` → **`GiselePrudente`** (P192).
- O código ganhou uma tarefa de outro tipo (`_bandido_arriscado`), onde o módulo de cautela é reusado sem re-treino: a primeira
  medida de transferência entre tipos de tarefa da série.
- Testes de regressão: contagem em `resultados.txt`.

### P199. Metacognição da Parte 13

1. **Dois resultados pré-registrados, um certo e um errado.** A transferência funcionou como previsto (P194); a prudência não (P192).
   Registrar antes torna os dois igualmente informativos.
2. **O resultado negativo explicou o positivo da parte anterior** (P193). Sem a falha da prudência, eu não teria olhado para as
   catástrofes por passo, e a "cooperação entre funções" da Parte 12 continuaria publicada como mecanismo. A explicação certa
   (distração do topo) é menos bonita e mais útil: diz exatamente onde agir.
3. **Jung acertou duas vezes nesta parte, de formas diferentes.** "As funções não se substituem" (P193) explicou por que limiares não
   corrigem a percepção. "O arquétipo é forma sem conteúdo" (P195) explicou por que a cautela transferiu. São usos de Jung como
   **gerador de hipóteses verificáveis**, não como decoração.

### P200. Duzentas perguntas: o que elas mostram, em números?

**Na pergunta.** "200" é só um número redondo, mas números redondos convidam a olhar para trás. A pergunta pede o balanço.

**Lógica.** Partes 3 a 12 (antes desta):

| Medida | Valor |
|---|---|
| Afirmações testadas por simulação ou cálculo | **52** |
| Precisaram de correção (⚠️ ou ❌) | 29 |
| Certas de primeira (✅) | **23 (44%)** |
| Funções `pNN` no código | 120+ |
| Versões da GISELE na linhagem | 9 |
| Υ da GISELE (família escolhida → sorteada) | 0,29 → 0,49; 0,45–0,48 em mundos sorteados |
| Capacidades de AGI cobertas | 3 → 4 de 12 |

**As três lições que mais se repetiram:**
1. **Supor independência onde há correlação** (P44, P61, P63, P94): o erro mais frequente da série.
2. **Medir antes de interpretar** (P152): oito partes de conclusões sobre ruído antes da régua.
3. **Completude rende mais que perfeição** (P174, P182): o maior ganho veio de acrescentar uma função, não de aperfeiçoar a que existia.

**E a leitura dessas 200 perguntas:** acerto de primeira em 44% das afirmações testadas, sem tendência de melhora. A melhora real
foi no **tempo** que um erro sobrevive e no tamanho dos passos: os maiores ganhos da série (equilíbrio da carga humana,
planejamento, transferência) vieram de perguntas que mudaram a **estrutura** da GISELE, não de ajustes de parâmetro.

> **Síntese da Parte 13:** a cautela não melhora mexendo em limiares quando o problema é de percepção, mas o que a GISELE percebe
> bem (o padrão "bom demais para ser verdade") **atravessou** para uma tarefa de outro tipo e cortou as catástrofes pela metade.
> É a primeira evidência, nesta série, de algo que uma AGI precisa: um conhecimento que vale além da tarefa onde foi aprendido. Pequena,
> construída por mim, num sinal de mesma forma, mas real e medida.
