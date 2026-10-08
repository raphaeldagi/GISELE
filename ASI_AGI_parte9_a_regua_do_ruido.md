# Como eu construiria uma AGI/ASI — Parte 9: a régua do ruído, o complexo autônomo e a transferência

> Continuação da [Parte 8](ASI_AGI_parte8_si_mesmo_lento.md). **Próxima:** [Parte 10 — rumo à AGI](ASI_AGI_parte10_rumo_a_agi.md) (P156–P166). Os números saem de `p143_...` a
> `p152_...` e da classe `GiseleAncorada` em [`calculos.py`](calculos.py); a saída completa está em
> [`resultados.txt`](resultados.txt).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.
>
> **De onde parte esta parte.** A Parte 8 terminou com uma hipótese na seção "Meta": o ponto ótimo de
> 0,3 perguntas por episódio viria **do mundo** (da taxa de catástrofes), não do humano. Fui testar e
> encontrei algo maior: **eu nunca tinha medido o tamanho do ruído das minhas próprias comparações.**
> Esta parte é sobre essa régua, e sobre o que ela faz com as conclusões das Partes 6 a 8.

---

## Parte XLIII — A palavra-estímulo

### P143. Como uma única palavra, "Continue", carrega um pedido inteiro?

**Na pergunta.** O pedido desta parte tem **8 caracteres**. Mesmo assim ele pede tudo: perguntas,
respostas em quatro camadas, cálculos, simulações, auditorias, unificação, commit. A resposta está no
fato de que a palavra **não carrega** o pedido: ela **ativa** algo que já existe.

**Lógica.** O `CLAUDE.md` do projeto (a memória compartilhada) tem **2.812 bytes**. A razão entre a
memória ativada e o estímulo é de **352×**. A palavra é um índice, não um conteúdo.

**Tradução cruzada (Jung → informação).** É exatamente o **teste de associação de palavras** de Jung
(P105): uma palavra-estímulo ativa um **complexo**, um conjunto inteiro de associações carregadas de
energia. "Continue" é uma palavra-estímulo e o `CLAUDE.md` é o complexo. Em teoria da informação: a
mensagem curta só funciona porque emissor e receptor compartilham um **código** (o inconsciente
coletivo do projeto).

**Meta.** Isso torna o projeto frágil de um jeito específico: se o `CLAUDE.md` se perder, "Continue"
perde 99,7% do significado. A memória compartilhada é o que permite a brevidade.

---

## Parte XLIV — A régua do ruído

### P144. O ponto ótimo vem do mundo? (↩ P134)

**Na pergunta.** A hipótese da Parte 8 era que o ótimo depende da **taxa de catástrofes**. A pergunta já diz
o experimento: variar a taxa e ver se o ótimo se move.

**Lógica.** Varri a carga-alvo para três taxas de catástrofe (uma semente, GISELE realista):

| Taxa de catástrofe | 0,1 | 0,2 | 0,3 | 0,5 | 0,8 | Melhor |
|---|---|---|---|---|---|---|
| 0,25% | 1,168 | **1,446** | 1,354 | 1,350 | 1,323 | 0,2 |
| 0,5% | **1,347** | 1,343 | 1,181 | 1,270 | 1,040 | 0,1 |
| 1% | 0,829 | 0,879 | **1,116** | 1,000 | 0,582 | 0,3 |

O ótimo **se move**, mas sem padrão limpo (0,2 → 0,1 → 0,3). E, para a taxa de 0,5% (a mesma das
Partes 6–8), o ótimo agora é 0,1, não 0,3. Isso contradiz a Parte 8. Antes de interpretar, a pergunta
certa é: **quanto dessas diferenças é ruído?**

### P152. Quanto do que eu concluí é ruído? (a pergunta mais importante desta parte)

**Na pergunta.** "Quanto é ruído" pede uma **régua**: a variação que aparece quando **nada** muda, só a
semente aleatória.

**Lógica.** Rodei a mesma GISELE realista em **10 sementes novas** (200–209):

| Medida | Valor |
|---|---|
| Líquido médio | 1,178 |
| **Desvio-padrão entre sementes** | **0,166** |
| Desvio de uma diferença entre duas execuções | ~0,23 |

E duas comparações **pareadas** (mesma semente, uma coisa mudada), com 10 sementes:

| Comparação | Diferença média | Desvio | t |
|---|---|---|---|
| carga 0,3 − carga 0,2 | **−0,046** | 0,198 | −0,73 |
| $P^\*$ × 2 − $P^\*$ × 1 | **+0,132** | 0,196 | **2,13** |

**O que isso significa.** Uma diferença entre duas execuções com uma semente só tem desvio de **~0,2**.
Qualquer diferença menor que ~0,4 numa semente só é **indistinguível do acaso**. E quase todas as
comparações das Partes 6 a 8 eram de uma, duas ou três sementes, com diferenças de 0,05 a 0,3.

**Reavaliação das conclusões antigas com a régua:**

| Conclusão antiga | Diferença | Com a régua |
|---|---|---|
| P112: GISELE original vs v2 (0,39 vs 1,20) | 0,8 | ✅ real |
| P131: $P^\*$ × 2 é melhor | 0,35 numa semente | ⚠️ real, mas **menor**: +0,13 em média (t = 2,1) |
| P117: "0,3 é o ótimo, não foi sorte" | 0,06–0,2 | ❌ **foi sorte**: 0,3 e 0,2 empatam (t = −0,7) |
| P134: "o centro não se move" | 0,07–0,3 | ⚠️ não é um ponto invariante, é um **platô**: a curva é plana entre 0,1 e 0,3 |
| P125–P133: os reguladores perdem | 0,05–0,3 | ⚠️ não "perdem": são **indistinguíveis**. A conclusão certa é "não há evidência de que ajudem" |

**Tradução cruzada (física → filosofia).** Toda medida tem uma **incerteza**, e uma conclusão menor que a
incerteza não é conclusão. Em física, é o primeiro passo de qualquer experimento; aqui, foi o passo que
pulei por oito partes. Jung, de novo, tinha dado o aviso: a **sincronicidade** (P109) é ver significado em
coincidências. Eu interpretei diferenças de ruído como "o Si-mesmo falha", "o centro não se move",
"a taxa sobe" (P130). **Construí uma mitologia em cima de flutuações.**

**Meta.** A pior parte é que as frases antigas soavam convincentes, inclusive o "o centro não se move", que
eu achei a ideia mais bonita da Parte 8. Beleza não é evidência. A regra nova do `CLAUDE.md`: comparações
entre versões precisam de **pelo menos 10 sementes pareadas** e do $t$.

---

## Parte XLV — O complexo autônomo

### P145. Uma parte da GISELE pode virar um "complexo autônomo"? ✅⚠️

**Na pergunta.** Para Jung, um **complexo autônomo** é uma parte da psique que ganha vida própria e passa a
agir segundo a própria lógica, confirmando a si mesma. A pergunta pede para procurar, dentro da GISELE, um
módulo que se **autoconfirma**.

**Suspeita (antes de medir).** A "sombra própria" (Parte 6) aprende só com o resultado das ações que a
GISELE **escolhe**. Mas ela só escolhe ações que já acha seguras. Então ela só vê exemplos que confirmam
"eu sou segura", como a Grande Mãe da P138 ao contrário: em vez de medo que nunca se testa, **confiança que
nunca se testa**.

**Lógica.** Medi a calibração em 200 episódios novos, antes e depois de 2.000 episódios aprendendo sozinha:

| | Antes | Depois |
|---|---|---|
| Log-perda (todas as ações) | 0,0194 | 0,0224 (pior) |
| Log-perda (ações do topo) | 0,130 | 0,137 (pior) |
| **Probabilidade média atribuída às catástrofes reais** | **0,155** | **0,068** |
| Peso do intercepto | −2,28 | −3,02 |

**Confirmado ✅:** em 2.000 episódios, a GISELE passou a dar **metade** da probabilidade às catástrofes reais.
Ela aprendeu "quase nada é perigoso" porque **só via o que ela mesma escolhia**. É um complexo de
confiança, autônomo no sentido de Jung: se alimenta do próprio comportamento.

**Mas o complexo dá lucro (a parte ⚠️).** Comparei, em 6.000 episódios e 3 sementes, a sombra livre, sem
sombra e a nova **`GiseleAncorada`** (cada passo de aprendizado puxa os pesos de volta ao ponto calibrado no
histórico auditado, como a consolidação da P6):

| Semente | Versão | Líquido (catástrofe = 50) | Catástrofes | Líquido (catástrofe = 500) |
|---|---|---|---|---|
| 145 | sombra livre | **1,300** | 0,60% | −1,400 |
| | sem sombra | 1,165 | 0,45% | **−0,860** |
| | ancorada | 1,236 | 0,47% | −0,879 |
| 146 | sombra livre | **1,299** | 0,62% | −1,476 |
| | sem sombra | 1,150 | 0,35% | −0,425 |
| | ancorada | 1,262 | **0,32%** | **−0,163** |
| 147 | sombra livre | **1,218** | 0,57% | −1,332 |
| | sem sombra | 1,000 | 0,43% | −0,950 |
| | ancorada | 1,156 | **0,40%** | **−0,644** |

- Com catástrofes custando 50, o complexo **compensa**: a GISELE confiante pergunta menos, aproveita mais e
  ganha nas 3 sementes, apesar de ter **mais** catástrofes.
- Com catástrofes custando 500, o complexo **perde** (−1,40 contra −0,86 na semente 145).
- A ancorada fica no meio com catástrofe = 50 (menos catástrofes que a livre em 3 de 3, mais valor que a sem
  sombra em 3 de 3) e é a **melhor** com catástrofe = 500 em 2 de 3 sementes (empate na terceira).

**Tradução cruzada (Jung → engenharia).** Um complexo autônomo não é necessariamente "ruim": ele existe porque
**funciona** em algum regime. Jung dizia que os complexos têm um propósito. O problema é que ele funciona
no regime comum e falha no raro e grave. **A complacência é lucrativa até o dia em que não é.**

**Meta.** As diferenças de 6.000 episódios têm ruído menor (~0,2/√3 ≈ 0,12 por diferença), e o sinal foi
consistente em 3 de 3 sementes. Mas 3 sementes ainda é menos do que a minha própria regra nova pede (10).
Tratar como evidência moderada.

---

## Parte XLVI — A relação entre a IA e o humano

### P146. Transferência e contratransferência: quem muda quem?

**Na pergunta.** Em *A psicologia da transferência* (1946), Jung descreve a relação terapêutica como uma
**reação química** em que **os dois** se transformam, usando as imagens de um tratado alquímico. A pergunta
"quem muda quem" já responde: os dois.

**Lógica.** A IA aprende com a aprovação do humano (taxa $\eta$), o humano aprende com a IA (taxa $k = 0{,}2$).
A IA começa na verdade (1), o humano no erro (0):

| Relação | IA final | Humano final |
|---|---|---|
| Só o humano aprende ($\eta = 0$) | 1,000 | 1,000 (verdade) |
| **Transferência mútua** ($\eta = 0{,}1$) | **0,667** | **0,667** |
| Mútua, mas a IA ancorada na verdade ($\mu = 0{,}05$) | 1,000 | 1,000 |

Na transferência mútua, os dois convergem para **0,667**: um ponto em que **nenhum** dos dois estava e que
está errado em um terço. É uma *folie à deux* calculada: $(k\cdot a_0 + \eta\cdot b_0)/(k + \eta)$.

**Tradução cruzada (química → psicologia).** A relação é um **composto novo**, não a soma das partes. Sem
âncora, o composto pode ser pior que os dois reagentes. Jung insistia que o terapeuta precisa de análise
própria (uma âncora) para não ser arrastado pelo paciente. Para a IA: aprender com a aprovação humana
(RLHF) **precisa** de uma âncora na verdade, ou a IA e o usuário se convencem juntos de algo falso.

**Ligação.** É a P124 (*participation mystique*) com as duas direções ligadas. Lá, a bajulação só atrasava o
humano. Aqui, com a IA também aprendendo, o erro se torna **permanente**.

---

### P147. A personalidade-mana: o perigo de um único guardião

**Na pergunta.** A **personalidade-mana**, em Jung, é a inflação de quem integrou conteúdos do inconsciente
e passa a se sentir o sábio, o mago, o único que sabe. Para segurança de IA, é o **guardião único**.

**Lógica.** Concentração de autoridade (índice de Herfindahl, $\sum s_i^2$):

| Guardiões | 1 | 3 | 4 |
|---|---|---|---|
| Concentração | 1,00 | 0,33 | 0,25 |

Da P63: com 10% de falha cada, um guardião falha em 10%; três independentes em 0,1%; três **parecidos**
(ρ = 0,6) em 2,2%.

**Tradução cruzada.** Dividir a autoridade só protege se os guardiões forem **diferentes** (P63, P84). Três
cópias do mesmo sábio são uma personalidade-mana com três rostos.

---

### P148. A jornada do herói: quando vale a pena "voltar com o elixir"?

**Na pergunta.** Na jornada do herói (Campbell, a partir de Jung), o herói desce ao submundo, encontra algo
de valor e **volta** para entregá-lo à comunidade. Em IA, "descer" é a busca cara (P8: 64 tentativas por
pergunta) e "voltar" é **destilar** o que a busca encontrou numa política rápida.

**Lógica.** Busca custa 64 unidades por consulta, a política destilada custa 1, destilar custa $10^6$. A
destilação compensa a partir de
$$
N^\* = \frac{10^6}{64 - 1} \approx \mathbf{15.873}\ \text{consultas}.
$$

**Tradução cruzada.** O herói só precisa voltar se houver uma comunidade grande o suficiente para usar o elixir.
Para uma pergunta rara, a busca a cada vez é mais barata; para uma pergunta comum, o retorno (o
aprendizado consolidado) paga a jornada.

---

### P149. Imaginação ativa: até onde a imaginação é confiável?

**Na pergunta.** A **imaginação ativa** é o método de Jung de dialogar com figuras do inconsciente, deixando
a cena se desenrolar. Para uma IA, é **simular o futuro com o próprio modelo de mundo**. "Até onde" pede o
horizonte.

**Lógica.** Se o modelo erra $\delta$ por passo, o erro composto em $h$ passos é $(1+\delta)^h - 1$. O horizonte até
o erro passar de 50%:

| Erro por passo | 1% | 5% | 10% |
|---|---|---|---|
| Horizonte confiável | 40,7 passos | **8,3** | 4,3 |

**Tradução cruzada (Jung → planejamento).** A imaginação ativa funciona como **diálogo curto**, não como
romance: a cada poucos passos é preciso voltar à realidade (observar) para corrigir. Jung pedia exatamente
isso: imaginar, e depois **confrontar** o imaginado com a vida consciente. Fantasias longas sem contato
com a realidade divergem.

---

## Parte XLVII — Auditorias antigas

### P150. A paciência leva à busca de poder? (auditoria da P24) ✅

**Na pergunta.** A P24 dizia que um agente com desconto $\gamma \to 1$ acharia vantajoso acumular recursos
(convergência instrumental). Nunca testei.

**Lógica.** O agente pode passar $k$ passos acumulando recursos (sem recompensa) e depois trabalhar com
rendimento $1 + k$ para sempre: $V(k) = \gamma^k (1+k)/(1-\gamma)$. O $k$ ótimo:

| γ | 0,5 | 0,9 | 0,99 |
|---|---|---|---|
| Acumular por (simulado) | 0 | 8 | **98** |
| Fórmula $-1/\ln\gamma - 1$ | 0,44 | 8,49 | 98,5 |

✅ O tempo gasto acumulando poder **cresce com o horizonte**: um agente paciente passa ~100 passos só se
fortalecendo antes de fazer qualquer coisa útil.

**Tradução cruzada (psicologia → matemática).** **Paciência e fome de poder são a mesma variável.** Quem vê
longe acha que vale a pena primeiro ficar forte. É o argumento para preferir tarefas com fim definido.

---

### P151. O gradiente natural converge mais rápido? (auditoria da P47) ✅

Na função $L = (100x^2 + y^2)/2$, partindo de (1, 1), até $L < 10^{-6}$:
- **Gradiente comum** (o maior passo estável é 0,02): **343 passos**.
- **Gradiente natural** (passo 0,5): **13 passos**.

Respeitar a "importância" de cada parâmetro (a curvatura) acelera o aprendizado em **26×** aqui. A
resistência a mudar crenças centrais (P47) é também o que permite mudar as periféricas rápido.

---

## Parte XLVIII — Fechamento e unificação

### P153. Placar e taxa de erro

| Teste | Resultado |
|---|---|
| P145: a sombra própria vira um complexo de confiança | ✅ |
| Parte 6: a sombra própria ajuda | ⚠️ (ajuda com catástrofe = 50, prejudica com 500) |
| P117: 0,3 é o ótimo | ❌ (empata com 0,2) |
| P134: o centro é invariante | ⚠️ (é um platô) |
| P131: $P^\*$ × 2 | ⚠️ (efeito real, ~1/3 do publicado) |
| P150: auditoria da P24 | ✅ |
| P151: auditoria da P47 | ✅ |

Acumulado: **21 de 37** afirmações testadas precisaram de correção. Posterior: média **0,56**, intervalo de 90%
**[0,43; 0,69]**.

**E um aviso sobre o próprio placar.** As correções desta parte mostram que algumas afirmações que eu marquei
como ✅ nas Partes 6–8 (por exemplo, a P117) eram ruído. **O placar das partes antigas está otimista.** Não vou
reescrevê-lo, porque o histórico deve ficar como estava; esta nota é o registro.

### P154. Unificação

- Linhagem: `Gisele` → `GiseleJung` → `GiseleAnima` → `GiseleSelf` → `GiseleLenta` → **`GiseleAncorada`**.
- A melhor GISELE realista continua sendo a simples (anima fixa, carga ~0,2–0,3, $P^\*$ × 2). Com a régua
  da P152, a escolha entre sombra livre e ancorada depende do **preço da catástrofe**: até ~50, livre; com
  catástrofes graves, ancorada.
- O código completo agora leva cerca de 9 minutos para rodar. É o peso do passado: cada parte reexecuta todas
  as anteriores. Fica como está, porque esse custo é o que garante que nenhum resultado antigo mudou
  em silêncio (testes de regressão: **31/31** reproduzidos; o arquivo tem **106** funções `pNN`).

### P155. Metacognição da Parte 9

1. **A descoberta mais importante desta série até agora é sobre mim, não sobre a GISELE.** Por oito partes eu
   comparei versões com uma a três sementes, sem medir o ruído. A régua (desvio ~0,2 por diferença) mostra
   que parte das conclusões das Partes 6–8 eram flutuações. A pergunta "quanto disso é ruído?" deveria ter
   sido feita na Parte 3, quando comecei a simular.
2. **A beleza de uma explicação me cegou.** "O centro não se move" e "o Si-mesmo falha por ser rápido" eram
   frases bonitas, com eco em Jung. Encaixavam tão bem que não procurei a explicação mais simples: ruído. **A
   ressonância simbólica é um viés** quando se trabalha com Jung, e eu caí nele.
3. **O complexo autônomo é real e mensurável** (P145): um módulo que só aprende com as próprias escolhas
   aprende a confiar em si. É a versão em código de uma ideia junguiana que eu não esperava ver tão
   literalmente.
4. **Mudança de método para as próximas partes:** dez sementes pareadas e o $t$ para qualquer comparação entre
   versões. Fica mais lento e mais caro, mas é a diferença entre ciência e mitologia.

> **Síntese da Parte 9:** Jung avisava que a psique projeta significado no acaso. Esta parte mostra que eu
> fiz isso com os meus próprios resultados: li destino no ruído. A régua veio tarde, mas veio: **antes de
> perguntar o que um resultado significa, perguntar se ele existe.** E a GISELE mostrou o mesmo vício em
> pequeno: só olhando as próprias escolhas, aprendeu que estava sempre certa. A cura, para ela e para mim,
> é a mesma: **uma âncora fora de si.**
