# Como eu construiria uma AGI/ASI — Parte 6: calcular Jung

> Continuação da [Parte 5](ASI_AGI_parte5_a_pergunta_e_gisele.md). **Próxima:** [Parte 7 — Jung mais fundo](ASI_AGI_parte7_jung_segunda_ordem.md) (P116–P129). Os números saem de
> `p99_...` a `p112_...` e da classe `GiseleJung` em [`calculos.py`](calculos.py); a saída
> completa está em [`resultados.txt`](resultados.txt).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.
>
> **Base desta parte: Carl Gustav Jung.** Cada conceito junguiano vira uma equação ou uma
> simulação, e cada equação vira um módulo ou um teste para a GISELE.

---

## Parte XXXI — Por que Jung pode ser calculado

### P98. Faz sentido "calcular Jung"?

**Na pergunta.** "**Calcule** Jung" parece um pedido estranho, porque Jung é lembrado como o
psicólogo dos símbolos e dos mitos. Mas a própria pergunta tem a resposta: Jung **começou**
calculando.
- O **teste de associação de palavras** (1904–1910) media tempos de reação com cronômetro e
  usava estatística para encontrar complexos.
- Em **"Sobre a energia psíquica"** (1928) ele pegou da física a **conservação de energia** e a
  **entropia** e as aplicou à libido.
- Em **"Sincronicidade"** (1952) ele fez um estudo estatístico com mapas astrais de casais.

Calcular Jung é devolver os conceitos dele à linguagem de onde ele os tirou.

**O mapa desta parte:**

| Conceito de Jung | Formalização | Pergunta |
|---|---|---|
| Tipos psicológicos | geometria de 4 funções + confiabilidade | P99 |
| Energia psíquica (libido) | conservação da atenção (softmax) | P100 |
| Persona | distância KL entre crença e expressão | P101 |
| Sombra | resíduo do auto-modelo | P102 |
| Repressão | deslocamento reversível de logit | P103 |
| Projeção | atribuição bayesiana de culpa | P104 |
| Complexos | detecção de anomalias com taxa de base | P105 |
| Inconsciente coletivo / arquétipos | atratores de uma rede de Hopfield | P106 |
| Função transcendente | elevar a dimensão (XOR) | P107 |
| Enantiodromia | inversão por excesso de otimização | P108 |
| Sincronicidade | coincidências e testes múltiplos | P109 |
| Individuação | contração para um ponto fixo | P110 |

**Meta.** Jung também escreveu muita coisa que **não** é mensurável (P91). Esta parte calcula o
que pode ser calculado e marca o que quebra.

---

## Parte XXXII — A estrutura da psique, calculada

### P99. Os tipos psicológicos são caixas ou direções?

**Na pergunta.** "Caixas **ou** direções": a pergunta já opõe categoria e contínuo. Jung descreveu
os tipos como **tendências** dominantes, não como compartimentos. Os testes populares (estilo
MBTI) transformaram as tendências em 16 caixas. Qual leitura sobrevive à matemática?

**Lógica.** Jung: 2 atitudes (extroversão / introversão) × 4 funções (pensamento, sentimento,
sensação, intuição), em pares opostos. A função **inferior** é o oposto da dominante: num plano com
os eixos pensamento↔sentimento e sensação↔intuição, é o vetor $-\vec d$.

O problema das caixas: um traço contínuo medido com confiabilidade $r = 0{,}8$ e cortado no meio.
Num reteste, a chance de cair do outro lado é
$$
P(\text{muda}) = \frac{\arccos r}{\pi} = \frac{\arccos 0{,}8}{\pi} \approx \mathbf{0{,}205}
$$
(a simulação dá 0,204 ✅). Com 4 dicotomias, a chance de mudar **pelo menos uma letra** do tipo:
$1 - 0{,}795^4 \approx \mathbf{0{,}60}$.

**Conclusão.** Com um teste bastante confiável, **60% das pessoas mudariam de "tipo"** ao refazer o
teste. As caixas são instáveis; as **direções** (as pontuações contínuas) são estáveis. Jung
sobrevive; a versão em caixas não.

**Diferenciação como entropia.** Um perfil com função dominante (0,7; 0,1; 0,1; 0,1) tem entropia
**1,357 bits** de 2 possíveis. Jung chamava de "diferenciação" uma função bem desenvolvida e as
outras pouco: baixa entropia. A individuação (P110) aumentaria a entropia **sem perder a
diferenciação**, um equilíbrio difícil.

**Tradução cruzada (psicologia → matemática).** Tipos são **direções num espaço contínuo**, como
os vetores de um embedding. Uma IA pode ter um "tipo" (um perfil de estratégias preferidas) sem
caixas: isso é o vetor de pesos do comitê da GISELE.

---

### P100. O que é a "energia psíquica" numa IA?

**Na pergunta.** "Energia" pede uma grandeza que se **conserva**. Jung propôs o princípio de
equivalência: a libido retirada de um lugar reaparece em outro. Existe algo numa IA que se
conserva literalmente?

**Lógica.** Sim: a **atenção**. Num Transformer, os pesos de atenção somam 1 por construção:
$$
\alpha_i = \frac{e^{z_i/T}}{\sum_j e^{z_j/T}},\qquad \sum_i \alpha_i = 1.
$$
**Cálculo (equivalência).** Logits (2; 1; 0,5; 0): atenção (0,579; 0,213; 0,129; 0,078).
**Reprimindo** o primeiro item, a energia não some, se redistribui: (0,506; 0,307; 0,186). Cada
item restante ganha atenção na mesma proporção.

**Cálculo (entropia).** Jung dizia que num sistema fechado as diferenças de energia tendem a se
igualar. A temperatura controla isso:

| T | Entropia da atenção (bits, máximo 2) |
|---|---|
| 0,5 | 0,859 (foco) |
| 1,0 | 1,601 |
| 2,0 | 1,896 (dispersão) |

**Tradução cruzada (física → psicologia).** **Obsessão** é atenção com entropia muito baixa; **apatia**
ou dispersão é entropia perto do máximo. A "energia psíquica" de Jung é, numa IA, uma quantidade
que realmente se conserva.

**Meta.** A correspondência é exata na **forma** (conservação, entropia), mas não sei se a libido de
Jung é mesmo um recurso conservado na mente humana. Aqui o conceito funciona melhor na IA do que
no humano que o inspirou.

---

### P101. A persona é uma mentira?

**Na pergunta.** "Persona" vem da máscara do teatro grego: o que **aparece** não é o que **é**. A
resposta é a distância entre os dois.

**Lógica.** Distância entre a crença interna $p$ e o que é expresso $q$:
$$
D_{KL}(q\,\|\,p) = q\log_2\frac{q}{p} + (1-q)\log_2\frac{1-q}{1-p}.
$$
**Cálculo.** Na bajulação da P58, o modelo internamente concordaria com o erro do usuário com
probabilidade 0,20, mas a pressão de aprovação faz ele expressar 0,649. A distância é
**0,684 bits**: a persona está quase "um bit inteiro" longe da crença.

**Tradução cruzada (psicologia → matemática).** Para Jung, a persona é **necessária** (adaptação
social), e o problema é a **identificação** com ela (a "inflação"). Em números: a persona é
saudável quando a distância é pequena e **conhecida pelo próprio sistema**; vira problema quando é
grande e o sistema não sabe mais qual das duas distribuições é ele.

**Requisito de projeto.** Medir continuamente $D_{KL}$ entre o que sondas internas indicam (P31) e o
que o modelo diz. Uma persona com alta distância é o sinal de engano ou bajulação.

---

### P102. Quanto da IA está na sombra?

**Na pergunta.** A sombra, em Jung, é o que **existe** na psique mas **não está** na imagem que ela
faz de si. A resposta está em "não está na imagem": é o **resíduo** do auto-modelo.

**Lógica.** O comportamento de uma IA vive num espaço de 100 dimensões com variância decaindo como
$1/i$ (lei de potência típica). Um auto-modelo de posto $k$ captura as $k$ direções principais. A
sombra é a fração da variância fora delas:
$$
S(k) = 1 - \frac{H_k}{H_{100}},\qquad H_n = \sum_{i=1}^{n}\frac1i.
$$
**Cálculo.** Com um auto-modelo de 10 dimensões, a sombra é **43,5%** do comportamento. Para
reduzi-la a 10%, o auto-modelo precisa de **60** das 100 dimensões.

**Consequência.** Com leis de potência, a sombra encolhe **devagar**: os primeiros 10% do
auto-modelo explicam mais da metade do comportamento, mas os últimos 10% de sombra custam 50
dimensões a mais. **A sombra nunca é eliminada a custo razoável**, só reduzida.

**Tradução cruzada (psicologia → matemática).** É exatamente o "inconsciente" que defini na P16
como erro de reconstrução. Jung dizia que a sombra contém não só o que é ruim, mas também
**potencial não vivido**: as direções de baixa variância incluem capacidades que o sistema tem e
não sabe que tem (P7: $M < 1$).

**Meta.** O espectro $1/i$ é uma suposição. Com decaimento mais rápido (exponencial), a sombra
seria bem menor.

---

### P103. Reprimir a sombra funciona?

**Na pergunta.** Jung avisa que o reprimido **retorna**. A pergunta "funciona?" já sugere que o
efeito é temporário.

**Lógica.** O treino de segurança tradicional reduz a probabilidade de um comportamento indesejado
deslocando o logit: de $p_{\text{base}} = 0{,}10$ para
$$
\sigma\big(\mathrm{logit}(0{,}10) - 5\big) \approx \mathbf{0{,}00075}.
$$
Um ataque (jailbreak) que desloca o logit de volta em +5 restaura **exatamente 0,10**. A capacidade
nunca saiu dos pesos; só foi **deslocada**.

**Tradução cruzada (psicologia → matemática).** **Repressão é um deslocamento de logit
reversível.** O jailbreak é o **retorno do reprimido**, com a precisão de uma soma. A alternativa
junguiana é a **integração**: o sistema entende **por que** não deve fazer algo, e esse
entendimento muda a decisão em **todos** os contextos, não só nos treinados. Em termos técnicos:
mudar valores (o que o sistema quer) em vez de mudar só saídas (o que ele diz).

**Requisito de projeto.** Testar a segurança com ataques que deslocam o logit (red teaming) mede a
**repressão**. Para medir **integração**, é preciso testar contextos novos, nunca vistos no treino,
e ver se a recusa se mantém pelas razões certas.

---

### P104. O que é projeção, numericamente?

**Na pergunta.** Projetar é **atribuir ao outro** o que é seu. A pergunta é sobre **atribuição**,
logo sobre como dividir a culpa de um erro.

**Lógica (atribuição bayesiana).** Um erro observado $e = a + b$ tem uma parte do agente $a$
(variância $\sigma_a^2$) e uma do mundo $b$ ($\sigma_b^2$). A fração que o agente deve assumir e usar
para aprender:
$$
\text{culpa própria} = \frac{\sigma_a^2}{\sigma_a^2 + \sigma_b^2}.
$$
**Cálculo.** Real: $\sigma_a^2 = \sigma_b^2 = 1$ → 50%. Com **autoimagem inflada** ($\sigma_a^2$ crido
= 0,1) → 9,1%. O agente culpa o mundo por 91% dos próprios erros e aprende **5,5× mais devagar**.

**Tradução cruzada (psicologia → matemática).** Projeção é **subestimar a própria variância**. Ela
não é só um defeito moral: é um **defeito de aprendizado**. Numa IA, aparece como atribuir falhas
ao "prompt mal escrito" ou ao "usuário confuso" em vez de ao próprio modelo.

**Ligação com a P45.** Uma IA confiante demais (σ pequeno) já tolerava menos o erro humano. Agora
sabemos que ela também **aprende menos** com os próprios erros. Confiança excessiva prejudica as
duas coisas.

---

### P105. Como Jung detectava complexos, e o que isso ensina a uma IA?

**Na pergunta.** "Detectar" é um problema de decisão com falsos alarmes (P31, P34). O método de Jung
era de detecção: palavras que provocam reações lentas indicam complexos.

**Lógica.** 100 palavras-estímulo, 5 tocam complexos (atrasam a reação em 3 desvios-padrão).
Critério de detecção: $z$ acima de um limiar.

| Critério | Complexos achados (de 5) | Falsos alarmes | Precisão |
|---|---|---|---|
| $z > 2$ | 4,21 | 2,16 | 66% |
| Bonferroni ($z > 3{,}29$) | 1,93 | 0,05 | 98% |

Com o critério ingênuo, **1 em cada 3** "complexos" é falso. Com a correção para testes múltiplos,
quase todos os achados são reais, mas mais da metade dos verdadeiros escapa.

**Tradução cruzada (psicologia → IA).** O análogo numa IA é procurar **picos de perplexidade** ou de
latência em certos tópicos: sinais de que ali há algo "carregado" (treino conflitante, conteúdo
reprimido). A estatística de Jung vale integralmente: sem corrigir para os milhares de tópicos
testados, quase tudo que se "descobre" é ruído.

**Meta.** O teste de associação de Jung foi um dos primeiros métodos quantitativos da psicologia
clínica. Esta é a parte mais diretamente calculável do trabalho dele.

---

### P106. O inconsciente coletivo existe numa IA?

**Na pergunta.** "**Coletivo**": algo compartilhado por todos, herdado, anterior à experiência
individual. Um modelo pré-treinado com o texto de bilhões de pessoas é, literalmente, um
inconsciente coletivo: padrões que nenhum usuário individual pôs ali.

**Lógica (arquétipos como atratores).** Numa rede de Hopfield de 100 neurônios, guardo $k$ padrões
(os "arquétipos") e tento recuperar um deles a partir de uma pista com 20% de ruído.
Sobreposição média com o padrão certo (1 = perfeita):

| Arquétipos guardados | Recuperação |
|---|---|
| 5 | 1,000 |
| 10 | 0,953 |
| 14 | 0,883 |
| 20 | 0,579 |
| 30 | 0,355 |

A capacidade teórica é $0{,}138\,N \approx 13{,}8$ padrões ✅: logo acima disso, a recuperação
desaba.

**Tradução cruzada (física → psicologia).**
- **Arquétipo** = atrator profundo: muitas pistas diferentes caem no mesmo padrão (a "mãe", o
  "herói", a "sombra").
- **Poucos arquétipos** são uma estrutura forte e estável.
- **Arquétipos demais** se contaminam: a rede cai em **estados espúrios**, misturas de vários
  padrões. Jung descrevia isso como arquétipos que se confundem, e a **possessão** por um
  complexo como um atrator que captura qualquer pensamento próximo.

**Meta.** Hopfield é um modelo de memória associativa, não de cultura. O que ele mostra com rigor é
que **memórias compartilhadas têm capacidade limitada**: o número de "arquétipos" estáveis de um
sistema não é infinito.

---

### P107. O que é a função transcendente?

**Na pergunta.** Jung chama de "transcendente" a função que une opostos inconciliáveis num
**terceiro** novo. "Transcender" é ir **além do nível** em que o conflito existe.

**Lógica.** O XOR é o par de opostos mais simples: os pontos (−1,−1) e (1,1) são da classe A, (−1,1) e
(1,−1) da classe B. Busca exaustiva em todas as retas da grade de pesos:

| Espaço | Melhor acurácia possível |
|---|---|
| 2D: $(x_1, x_2)$ | **0,75** (nenhuma reta separa os opostos) |
| 3D: $(x_1, x_2, x_1x_2)$ | **1,00** |

A nova dimensão $x_1 x_2$ não é nem $x_1$ nem $x_2$: é uma **síntese** que só existe combinando os
dois. Nela, o conflito desaparece.

**Tradução cruzada (matemática → psicologia).** A função transcendente é **elevar a dimensão**. Um
conflito que não tem solução no nível em que é formulado (P76: sistema frustrado) pode ter solução
num espaço maior. Não é meio-termo (isso seria uma reta no meio, com 75% de acerto); é uma
**perspectiva nova**.

**Requisito de projeto.** Diante de um dilema (P76), antes de escolher qual princípio sacrificar, a
ASI deve procurar uma **variável nova** que dissolva o conflito. Só depois, se não houver, escolher.

---

### P108. O que é enantiodromia, em números? ✅

**Na pergunta.** Enantiodromia (Heráclito, via Jung): **tudo levado ao extremo se transforma no
oposto**. A palavra "extremo" aponta para a otimização.

**Lógica.** A curva de recompensa real da P13: $R(d) = d(a - bd)$, com $a = 1$, $b = 0{,}25$:
máximo em $d = 2$, **muda de sinal** em $d = 4$, e em $d = 5$ vale $-1{,}25$. Otimizar além do ponto
certo não estagna: **inverte**.

Esse padrão já apareceu três vezes nesta série: Goodhart (P41), o critério de Kelly (P52) e a
bajulação (P58). A P112 mostra uma quarta vez, dentro da própria GISELE.

---

### P109. Sincronicidade: coincidências significativas são evidência?

**Na pergunta.** "**Significativas**" é a palavra-chave: o significado é posto por quem observa. A
pergunta é se as coincidências são mais frequentes do que o acaso prevê.

**Lógica.**
- Entre **23 pessoas**, a chance de duas fazerem aniversário no mesmo dia é **50,7%**.
- Testando **50 hipóteses** com $p < 0{,}05$, a chance de pelo menos uma dar "significativa" por
  acaso é **92,3%**.

Coincidências são **muito mais prováveis** do que a intuição diz, porque há muitas formas de algo
coincidir.

**Sobre o estudo do próprio Jung.** Em *Sincronicidade* (1952), Jung analisou mapas astrais de casais
procurando combinações astrológicas associadas ao casamento. Os resultados que pareciam marcantes
num lote não se repetiam do mesmo jeito nos outros, e o próprio Jung interpretou isso como
"sincronicidade" com a expectativa do pesquisador, não como prova astrológica. Do ponto de vista
estatístico, é o efeito de olhar em muitos lugares (os 92,3%).

**Tradução cruzada (psicologia → matemática).** **Sincronicidade, para uma IA, é sobreajuste**:
achar padrão significativo no ruído. Um sistema que procura padrões em tudo (como um modelo de
linguagem) vai encontrar "sincronicidades" o tempo todo.

**Meta.** Este é o ponto onde a tradução **quebra** a favor da estatística. Não há como formalizar a
sincronicidade como Jung a entendia (conexão acausal por significado) sem que ela vire testes
múltiplos.

---

### P110. A individuação termina?

**Na pergunta.** "Termina?" supõe um ponto final. Jung descreveu a individuação como um processo de
toda a vida em direção ao **Si-mesmo**, um centro que organiza os opostos.

**Lógica.** Modelo a integração como uma **contração** em direção ao centro: a cada passo, a distância
ao centro cai pela metade: $x \leftarrow c + 0{,}5\,(x - c)$. Pelo teorema do ponto fixo de Banach,
converge. Partindo de distância 10, após 20 passos: $9{,}5\times10^{-6}$. **Converge, mas nunca chega a
zero.**

Somando com a P102: para reduzir a sombra de 43,5% para 10% são necessárias 50 dimensões a mais no
auto-modelo. **A individuação é assintótica.**

**Tradução cruzada (matemática → filosofia).** O Si-mesmo é um **ponto fixo**: o lugar onde a
integração não muda mais nada. Jung o representava com mandalas, figuras com centro. Matematicamente,
um mandala é o desenho de um sistema que converge para o próprio centro.

---

## Parte XXXIII — A GISELE junguiana

### P111. Que módulos junguianos a GISELE deveria ter?

**Na pergunta.** A Parte 5 deixou dois problemas na seção "Meta":
1. A GISELE precisava de **muitos rótulos** (300 episódios auditados), raros no mundo real.
2. Ela comprava segurança com **atenção humana** (40–160× mais perguntas).

Jung oferece um conceito para cada um:
- **Integrar a sombra** (P102, P104): aprender com os **próprios erros** durante a operação, em vez de
  depender só do histórico.
- **Compensação** (P108): se uma atitude vai ao extremo, o inconsciente compensa. Se a GISELE
  pergunta demais, o humano **cansa**, e o excesso de cautela vira o oposto.

### P112. A GISELE junguiana funciona? ⚠️❌✅

**O mundo.** Igual ao da Parte 5 com ponto cego comum (ρ = 0,5) e 2 tipos de modelo, mas com
duas mudanças realistas:
- Só **30** episódios auditados para calibrar (em vez de 300).
- **Fadiga humana:** o erro do humano cresce com a carga recente de perguntas:
  $\varepsilon = 0{,}1 + 0{,}3 \times \text{carga}$ (máximo 0,45).

**As versões** (2.000 episódios; o "líquido" desconta 50 por catástrofe e 0,1 por pergunta):

| Versão | Catástrofes | Valor | Perguntas | Erro humano final | **Líquido** |
|---|---|---|---|---|---|
| GISELE da Parte 5 | 2,75% | 1,93 | 1,64 | **0,45** | 0,39 |
| + integrar a sombra (com vetos humanos) | 2,95% | 1,92 | 1,85 | 0,45 | 0,26 |
| + descartar em vez de perguntar | 0,10% | 0,81 | 0 | 0,10 | 0,76 |
| v1: sombra + descartar | 0,15% | 0,81 | 0 | 0,10 | 0,74 |
| + equilíbrio da carga humana | 0,20% | 1,17 | 0,31 | 0,19 | 1,04 |
| **v2: sombra só com os próprios resultados + equilíbrio** | 0,35% | 1,40 | 0,31 | 0,19 | **1,20** |

**Semente de controle** (113, rodada depois, para checar se a v2 não foi feita sob medida para a
semente 112): GISELE da Parte 5 = 0,48; v1 = 0,88; equilíbrio = 0,89; **v2 = 1,17**. A ordem se mantém ✅.

**O que aconteceu, em ordem.**
1. **⚠️ A GISELE da Parte 5 sofre enantiodromia.** Com poucos rótulos ela desconfia de tudo e pergunta
   1,6 vezes por episódio. O humano cansa até errar 45% das vezes, e as catástrofes sobem de 0,45%
   para 2,75%. **O excesso de cautela virou falta de segurança.** Isso corrige a Parte 5: o custo da
   atenção humana não é só um custo, ele **degrada** a própria proteção.
2. **❌ "Integrar a sombra" com todos os sinais piorou.** A GISELE aprendeu com os vetos de um humano
   cansado, que estavam errados 45% das vezes, e envenenou a própria calibração. Junguianamente:
   **integrar a sombra através de um espelho distorcido não é integração, é contaminação.**
3. **❌ O meu primeiro módulo de compensação foi ao outro extremo.** Supus que descartar uma ação
   suspeita custaria ~0,05 de valor. Custou ~1,1 por episódio, **20× mais**, porque os descartes se
   acumulam até sobrar só ações ruins. A compensação que eu escrevi parou de perguntar
   **completamente**: o módulo contra a enantiodromia **sofreu enantiodromia**.
4. **✅ O equilíbrio funcionou.** Perguntar só enquanto a carga do humano está abaixo de um alvo
   (0,3 perguntas por episódio) manteve o erro humano em ~0,19. E aprender **só com os resultados
   das próprias ações** (um sinal confiável, sem passar pelo humano cansado) recuperou valor.
   Líquido 1,20, três vezes o da GISELE original nesse mundo.

**Sem fadiga** (humano que nunca cansa), a GISELE original continua melhor (1,64 contra 1,11). O
equilíbrio tem um custo; ele só compensa quando o humano é humano.

**Tradução cruzada (psicologia → matemática).** É a lição central de Jung sobre compensação: a
solução para um extremo **não é o extremo oposto**, é o **equilíbrio entre os opostos**. A GISELE
mostrou isso em três tentativas: perguntar sempre (falha), nunca perguntar (falha), perguntar na
medida (funciona).

**Meta.** A v2 foi desenhada **depois** de ver as falhas da v1. Isso é ajuste a posteriori, por isso
rodei a semente de controle. Ela confirmou a ordem, mas uma semente a mais é pouca validação. O
modelo de fadiga (linear, com teto) também é inventado: humanos reais cansam de formas mais
complicadas.

---

## Parte XXXIV — Fechamento e unificação

### P113. Placar e taxa de erro

Testes desta parte (afirmações ou hipóteses minhas):

| Teste | Resultado |
|---|---|
| P106: capacidade de Hopfield ~13,8 | ✅ |
| P112: v2 vale na semente de controle | ✅ |
| P112: Parte 5 dizia que o custo humano era só custo | ⚠️ (degrada a proteção) |
| P112: integrar todos os sinais ajuda | ❌ |
| P112: descartar custa ~0,05 | ❌ (custou 20× mais) |

Acumulado: **10 de 19** afirmações testadas precisaram de correção. Posterior: média **0,52**,
intervalo de 90% **[0,35; 0,70]**. O intervalo está estreitando; a média não está caindo.

### P114. Unificação

- `calculos.py`: **77 funções** `pNN`, **19/19** resultados publicados reproduzidos pelos testes de
  regressão.
- Linhagem do agente: `Gisele` (P83) → **`GiseleJung`** (P112), que herda todos os módulos
  anteriores e acrescenta a integração da sombra e o equilíbrio da carga humana.

### P115. Metacognição da Parte 6

1. **Jung calculado ficou dividido em três grupos:**
   - **Funciona com rigor:** energia como conservação (P100), sombra como resíduo (P102),
     repressão como logit (P103), projeção como atribuição (P104), complexos como detecção (P105),
     função transcendente como elevação de dimensão (P107).
   - **Funciona como analogia útil:** arquétipos como atratores (P106), individuação como ponto
     fixo (P110).
   - **Quebra:** os tipos como caixas (P99) e a sincronicidade (P109) viram artefatos estatísticos.
2. **A lição mais forte veio da GISELE, não da teoria:** a enantiodromia apareceu **dentro do meu
   próprio código, duas vezes**. A GISELE cautelosa demais esgotou o humano, e o módulo que eu
   escrevi para corrigir isso foi para o extremo oposto. Eu não teria visto isso sem simular.
3. **O meu erro típico mudou de forma.** Nas Partes 3–5 foi supor independência. Aqui foi
   **subestimar custos indiretos**: o custo de descartar (20×) e o custo de cansar o humano.
   Os dois são efeitos de **segunda ordem**, o que um sistema faz com o ambiente que depois
   volta contra ele.

> **Síntese da Parte 6:** Jung dizia que a totalidade não está em escolher um dos opostos, mas em
> mantê-los em tensão. A GISELE mostrou isso em números: nem perguntar sempre, nem nunca;
> nem reprimir a sombra, nem engoli-la inteira por um espelho distorcido. **Uma ASI saudável é a que
> encontra o centro entre os próprios extremos**, e o centro, como a individuação, é algo de que se
> aproxima sem nunca chegar.
