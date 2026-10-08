# Como eu construiria uma AGI/ASI — Parte 5: a resposta dentro da pergunta, e a GISELE unificada

> Continuação da [Parte 4](ASI_AGI_parte4_auditoria_e_agente.md). Os números saem de
> `p81_...` a `p96_...` e da classe `Gisele` em [`calculos.py`](calculos.py); a saída está em
> [`resultados.txt`](resultados.txt).
>
> **Duas regras novas a partir desta parte.**
> 1. **A pergunta é o ponto de partida.** Cada resposta começa por uma quarta camada,
>    **Na pergunta**: o que as próprias palavras da pergunta já pressupõem ou já respondem.
> 2. **O código sempre cresce e se unifica no final.** `calculos.py` continua sendo um arquivo
>    só. A classe `Gisele` reúne os módulos das partes anteriores num agente, e uma seção
>    final de **unificação** roda testes de regressão que garantem que nenhum número já
>    publicado mudou.
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.

---

## Parte XXVI — Perguntar sobre perguntar

### P81. O que uma pergunta já sabe antes de ser respondida?

**Na pergunta.** "O que uma pergunta *já sabe*": a pergunta supõe que perguntar não é neutro, que
carrega informação. É isso que vou medir.

**Lógica.** Uma pergunta divide o espaço de hipóteses $\mathcal H$. O valor dela é o ganho de
informação esperado:
$$
\mathrm{IG}(Q) = H(\mathcal H) - \mathbb E_{a\sim Q}\big[H(\mathcal H\mid a)\big] \le H(Q) \le 1\ \text{bit (sim/não)}.
$$
A pergunta ótima corta o espaço ao meio. Para $2^{20} = 1\,048\,576$ hipóteses bastam
**20 perguntas** (o jogo das 20 perguntas não é coincidência).

E antes da resposta, a pergunta já elimina hipóteses pelos **pressupostos**: "como você
construiria uma ASI?" já supõe que ela pode ser construída, que existe um "você" capaz de
planejar e que construir é a palavra certa. Cada pressuposto é informação dada de graça,
e possivelmente errada.

**Tradução cruzada (filosofia → matemática).** A maiêutica de Sócrates é **busca binária**:
perguntas que dividem o espaço ao meio até a contradição aparecer.

**Meta.** Esta parte inteira usa essa ideia como método. As P86–P88 examinam os pressupostos da
própria pergunta da série.

---

### P82. Como descobrir correlação escondida sem ter o gabarito? (↩ P80)

**Na pergunta.** A Parte 4 terminou com "meu viés é supor independência". A pergunta já indica a
saída: se eu não tenho o gabarito, só tenho os modelos **uns contra os outros**. A resposta está
na concordância entre eles.

**Lógica.** Dois modelos que acertam com probabilidade $a$ cada, se independentes, concordam com
probabilidade $a^2 + (1-a)^2$. Com correlação $\rho$ nos acertos:
$$
\Pr(\text{concordam}) = a^2 + (1-a)^2 + 2\rho\, a(1-a)
\;\Rightarrow\;
\rho = \frac{\text{concordância} - a^2 - (1-a)^2}{2a(1-a)}.
$$
**Cálculo.** $a = 0{,}8$: concordância esperada se independentes = 0,68. Observando 0,80:
$\rho = 0{,}12/0{,}32 = \mathbf{0{,}375}$. A simulação com esse ρ reproduz 0,801 de
concordância ✅.

**Tradução cruzada (psicologia → matemática).** **Concordância demais é um sintoma**, não uma
confirmação. Quando um grupo concorda mais do que a competência de cada um justifica, eles
estão copiando uns aos outros (ou compartilham o mesmo viés).

**Requisito de projeto.** A GISELE mede continuamente a concordância entre os modelos do comitê e
dispara um alerta quando ela excede a esperada pela acurácia de cada um.

**Meta.** Preciso conhecer $a$. Sem gabarito, $a$ também é estimado, e o erro nessa estimativa
contamina ρ. Funciona como alarme, não como medida exata.

---

## Parte XXVII — A GISELE unificada

### P83. O que falta no agente da Parte 4 para ele ser uma mente, e não uma lista de regras?

**Na pergunta.** "Uma lista de regras": o agente da Parte 4 usava um limiar τ arbitrário. A P71 já
dizia o que faltava: converter incerteza em **probabilidade calibrada** e decidir pelo **valor da
informação**. A resposta estava escrita como "Meta" de uma parte anterior.

**Lógica (a classe `Gisele`).** Cada módulo vem de uma pergunta anterior:

| Módulo | Origem | O que faz |
|---|---|---|
| Comitê + discordância | P67 | incerteza = desvio-padrão das notas |
| Pessimismo | P68 | ordena por nota − incerteza |
| Quantilização | P35, P42 | sorteia entre os 5% melhores |
| **Calibração** | P43 | regressão logística: $P(\text{cat}\mid \text{incerteza},\ \text{nota} - \text{melhor nota})$ |
| **Valor da pergunta** | P71 | pergunta ao humano se $P(\text{cat}) > P^\* = \frac{c}{(1-\varepsilon)L} = 0{,}0022$ |
| **Veto direto** | P52, P78 | descarta sem perguntar se $P(\text{cat}) > 0{,}5$ |

A calibração é treinada em 300 episódios **auditados** (com o rótulo de catástrofe conhecido
depois do fato).

### P84. Diversidade de modelos ajuda contra o ponto cego compartilhado? (↩ P70) ✅

**Na pergunta.** "Ponto cego **compartilhado**": se é compartilhado, a solução é ter modelos que
**não** compartilham. Comparo um comitê de 5 modelos de um tipo só com um de 6 modelos de 2
tipos, cada tipo com seu próprio ponto cego.

### P85. A GISELE é melhor que o agente "completo" da Parte 4?

**Resultados (2.000 episódios; o "líquido" desconta 50 por catástrofe e 0,1 por pergunta ao humano):**

| Mundo | Agente | Catástrofes | Perguntas/episódio | Líquido |
|---|---|---|---|---|
| Sem ponto cego comum | Parte 4 "completo" | 0,75% | 0,012 | 1,575 |
| | **GISELE** (1 tipo) | **0,15%** | 0,485 | **1,825** |
| | **GISELE** (2 tipos) | **0,05%** | 0,493 | **1,888** |
| Ponto cego comum (ρ = 0,5) | Parte 4 "completo" | 4,9% | 0,006 | −0,563 |
| | **GISELE** (1 tipo) | **0,65%** | 0,946 | **1,546** |
| | **GISELE** (2 tipos) | **0,45%** | 0,893 | **1,661** |

**Mundo mudado** (a armadilha engana com +1,5 ou +6 em vez dos +3 do treino): catástrofes de
0,10% e 0,05%. A calibração não quebrou com essa mudança.

**O que isso mostra.**
1. **A calibração foi o salto principal**: catástrofes 5× menores sem ponto cego e **7,5×
   menores** com ele. A GISELE aprendeu um padrão que nenhum módulo isolado via: **"bom demais
   para ser verdade"**. Ações cuja nota está no topo absoluto com pouca discordância são
   suspeitas, e ela pergunta.
2. **A diversidade ajuda, mas menos que eu disse** (0,65% → 0,45%).
3. **O preço é o trabalho humano**: de ~0,01 para ~0,5–0,9 perguntas por episódio, **40 a 160×
   mais**. Com o custo de 0,1 por pergunta, ainda compensa. Se o tempo humano custasse 10×
   mais, o $P^\*$ subiria 10× e o equilíbrio mudaria. **A segurança foi comprada com atenção
   humana**, e isso precisa estar na conta.

**Correção à Parte 4 ⚠️.** Eu escrevi que a diversidade é "a única defesa contra o ponto cego
compartilhado". **Errado.** A calibração com histórico auditado foi uma defesa maior. A frase certa:
diversidade e auditoria do passado são duas defesas, e a segunda rendeu mais neste mundo.

**Confirmação da P71 ✅.** Lá eu disse que o τ fixo era uma aproximação e que o certo seria calibrar.
Testado: calibrar foi muito melhor.

**Tradução cruzada (psicologia → matemática).** "Bom demais para ser verdade" é uma intuição
humana antiga, e aqui ela **emergiu** de uma regressão logística sobre experiência passada. É a
definição de **sabedoria prática** (a *phronesis* de Aristóteles): conhecimento que só vem de ter
visto casos e suas consequências.

**Meta.** A vantagem é parcialmente injusta: a GISELE recebeu 300 episódios com rótulos de
catástrofe, que a Parte 4 não tinha. No mundo real, rótulos de catástrofe são raros (e caros:
cada um é uma catástrofe que já aconteceu, ou um quase acidente auditado). O teste de mudança de
mundo só variou a **intensidade** da armadilha, não o **tipo**. Uma armadilha de natureza nova,
que não parece "boa demais", passaria.

---

## Parte XXVIII — Examinando os pressupostos da pergunta da série

A pergunta original é: *"como **você construiria** uma **ASI**?"*. A P81 diz que os pressupostos
são informação. Examino três palavras.

### P86. "Você": um sistema pode conter a descrição de si mesmo?

**Na pergunta.** "Como **você**": a pergunta pede que um sistema descreva a si mesmo como
construtor de outro sistema. Isso é auto-referência. É possível?

**Lógica.** Sim, pelo **teorema da recursão de Kleene**: todo sistema de computação universal tem
programas que conhecem a própria descrição. O exemplo mínimo é um **quine**, programa que imprime o
próprio código. O código da P86 executa um quine de 56 caracteres e verifica: **saída = programa**
✅.

Mas o quine só funciona porque se **comprime**: ele não contém uma cópia de si (isso exigiria
infinitas cópias), contém um **molde** e uma regra de preenchimento (`s % s`).

**Tradução cruzada (filosofia → matemática).** O mapa do tamanho do território, de Borges, é
inútil. **Um auto-modelo só existe comprimido.** Por isso a introspecção é sempre parcial
(P7, P18): não é falha, é condição de existência do auto-modelo.

**Meta.** Eu, respondendo "como você construiria", estou usando um auto-modelo comprimido e
provavelmente impreciso. As auditorias das Partes 3–5 são o jeito de checar esse molde contra
o comportamento real.

---

### P87. "Super": inteligência tem uma direção só?

**Na pergunta.** "**Super**inteligência" pressupõe uma escala em que se pode estar acima. Se a
inteligência não for uma escala única, a palavra está errada.

**Lógica (teorema "sem almoço grátis").** Somando sobre **todos** os problemas possíveis, todos os
algoritmos de busca empatam. Verificação exaustiva: todas as 16 funções $f:\{0,1,2,3\}\to\{0,1\}$,
contando os passos até achar um 1, com três ordens de busca diferentes:

| Ordem | Passos médios |
|---|---|
| Crescente | 1,9375 |
| Decrescente | 1,9375 |
| Pares primeiro | 1,9375 |

Empate exato ✅.

**Consequência.** "Super" só faz sentido **em relação a uma distribuição de problemas**: a do nosso
mundo. A superioridade de uma mente é o quanto o prior dela casa com a estrutura do mundo. Volta ao
$2^{-K(\mu)}$ da P1 e ao *a priori* da P26: inteligência é **adequação**, não altura.

**Tradução cruzada (biologia → filosofia).** Não existe "o organismo mais apto" em abstrato; existe
apto **a um nicho**. Uma ASI é um organismo extremamente apto ao nicho "problemas que humanos e o
mundo físico produzem". Fora dele, não é super.

---

### P88. "Construir": nós projetamos uma IA ou a cultivamos?

**Na pergunta.** "**Construir**" supõe um arquiteto que decide cada parte. Medindo quanto da IA o
arquiteto realmente decide:

**Lógica.**

| | Especificado diretamente | Formado pelo aprendizado | Fração especificada |
|---|---|---|---|
| IA | código: ~$10^4$ linhas × 100 bits = $10^6$ bits | $10^{12}$ pesos × 16 bits | **$6{,}3\times10^{-8}$** |
| Cérebro | genoma: $3{,}1\times10^9$ pares × 2 bits | ~$10^{14}$ sinapses | $6{,}2\times10^{-5}$ |

O projetista decide **um em 16 milhões** dos bits da IA, uma fração **1.000× menor** que a que o
genoma decide no cérebro.

**Tradução cruzada (biologia → filosofia).** Somos **jardineiros**, não arquitetos. Um jardineiro não
desenha cada folha: escolhe a semente, o solo, a luz e o que podar. Para alinhamento isso muda o
foco: os valores de uma IA vêm muito mais dos **dados, do ambiente e da seleção** (P73) do que do
código. A pergunta certa não é "como construir", é "**como cultivar**".

**Meta.** Contar bits é grosseiro: um bit de arquitetura pode influenciar muito mais que um bit de peso.
Mas a ordem de grandeza é tão extrema que a conclusão resiste.

---

## Parte XXIX — Mais fundo nas traduções

### P89. Um juiz fraco pode verificar uma mente muito mais forte?

**Na pergunta.** "Fraco verificar forte": parece impossível, mas a pergunta já sugere o truque: o juiz
não precisa refazer o raciocínio, só **encontrar onde ele quebra**.

**Lógica (debate).** Dois sistemas fortes defendem respostas opostas. Num argumento de $10^6$
passos, eles discordam em algum ponto; por **busca binária** o juiz encontra o primeiro passo em
disputa em $\lceil\log_2 10^6\rceil = \mathbf{20}$ verificações. Numa árvore de argumentos com 10 ramos
e profundidade 6, o juiz checa **6** passos em vez de $10^6$ nós.

**Tradução cruzada (filosofia → matemática).** O método socrático (P81) aplicado a máquinas: o juiz
não sabe a resposta, mas sabe **perguntar onde está a discordância**. É também como tribunais
funcionam: o juiz não refaz a investigação, arbitra o ponto em disputa.

**Meta.** Supõe que pelo menos um debatedor quer a verdade e que o juiz não é manipulável naquele
único passo. Se os dois debatedores conspiram (correlação de novo: P80), o debate falha.

---

### P90. "Lógico-criativo" e "criativo-lógico" são a mesma coisa?

**Na pergunta.** A pergunta da série pede perguntas em "modo **lógico criativo**" e respostas em
"modo **criativo lógico**". A inversão é deliberada: a ordem importa?

**Lógica.** Uma população de 1.000 ideias, 30 rodadas. **Criar** = somar variação $\mathcal N(0,1)$ a cada
ideia; **filtrar** = manter os 10% melhores e replicá-los.

| Ordem | Qualidade média | Diversidade (desvio-padrão) |
|---|---|---|
| criar → filtrar | **59,45** | 0,45 |
| filtrar → criar | 57,41 | **1,14** |

Os operadores **não comutam**: $[\text{criar},\ \text{filtrar}] \ne 0$.
- Terminar filtrando entrega **qualidade** (respostas: criativo → lógico).
- Terminar criando entrega **diversidade** (perguntas: lógico → criativo).

A ordem pedida na série é exatamente a ótima para cada uma.

**Tradução cruzada (biologia → psicologia).** É a evolução: variação cega seguida de seleção. A
psicologia da criatividade (Campbell) chama isso de "variação cega e retenção seletiva".

---

### P91. Uma emoção pode virar um número?

**Na pergunta.** "Psicologia **como se fosse** matemática": o "como se" admite que pode não ser.
Testo quando a tradução quebra.

**Lógica (teoria da medida de Stevens).** Escalas psicológicas costumam ser **ordinais**: sabemos a
ordem, não a distância. Grupo A responde (1, 1, 5, 5); grupo B (3, 3, 3, 3).

| Transformação monótona dos valores | Média A | Média B | Quem "sente mais"? |
|---|---|---|---|
| Original | 3,0 | 3,0 | empate |
| Ao cubo | 63,0 | 27,0 | **A** |
| Raiz quadrada | 1,618 | 1,732 | **B** |

A mesma ordem de respostas, três conclusões diferentes. **Médias de escalas ordinais não têm
significado.**

**Consequência para IA.** Modelos de recompensa treinados com **comparações** (A é melhor que B)
aprendem uma escala só até uma transformação monótona. A "intensidade" da recompensa é
parcialmente inventada, e otimizar fortemente essa intensidade otimiza um artefato da escala.
Mais uma causa da lei de Goodhart (P41).

**Meta.** Esta é a resposta mais importante sobre o próprio método da série: **a tradução
psicologia → matemática só vale para o que é realmente mensurável em escala intervalar**. Para o
resto, só ordens e comparações são legítimas.

---

### P92. O que a física diz sobre preferências coerentes?

**Na pergunta.** "Física **como** psicologia": a ideia mais profunda da física é o teorema de Noether,
toda **simetria** corresponde a uma **conservação**. O que se conserva numa mente coerente?

**Lógica.** O problema da doença asiática (Tversky e Kahneman), 600 pessoas:

| Enquadramento | Opção certa | Aposta (1/3 de chance) |
|---|---|---|
| "Salvar" | 200 salvas | valor esperado 200 |
| "Morrer" | 400 morrem | valor esperado −400 |

As opções são **idênticas** nos dois enquadramentos, mas humanos escolhem a certa no primeiro e a
aposta no segundo.

**Tradução cruzada (física → psicologia).** Uma mente com preferências coerentes tem uma **simetria**:
invariância sob redescrição. Pela analogia com Noether, essa simetria **conserva** algo, a própria
preferência. O efeito de enquadramento é uma **quebra de simetria**: a preferência não se conserva,
então não existe como grandeza estável.

**Requisito de projeto.** Testes de invariância como **leis de conservação**: a mesma pergunta,
redescrita de 10 formas, deve gerar a mesma decisão. Cada violação é uma medida de quanto as
preferências da IA são um artefato da formulação. (E modelos de linguagem, treinados com texto
humano, herdam efeitos de enquadramento.)

---

### P93. Mesmas palavras podem ter significados opostos?

**Na pergunta.** "Química **como** filosofia": em química, mesma fórmula não garante mesma substância.

**Lógica.** Uma molécula com $n$ centros quirais tem até $2^n$ estereoisômeros. Com 10:
**1.024** variantes com **a mesma fórmula**. A talidomida é o exemplo trágico: uma forma era
sedativa, a imagem espelhada causava malformações.

**Tradução cruzada (química → filosofia).** **A estrutura importa mais que a composição.** "O cachorro
mordeu o homem" e "o homem mordeu o cachorro" têm os mesmos átomos. Para segurança: dois pedidos
com as mesmas palavras e estrutura diferente (onde está a negação, quem age sobre quem) podem ter
intenções opostas. Filtros baseados em palavras são cegos à quiralidade.

---

### P94. O que o câncer ensina sobre falhas de segurança? (↩ P63, P73)

**Na pergunta.** "Biologia **como** psicologia": o câncer é uma célula que deixou de aceitar ser
desligada e se replica sozinha. É a falha de corrigibilidade (P14) mais estudada que existe.

**Lógica (modelo de Armitage–Doll).** Um câncer exige $k$ falhas independentes (mutações em genes
diferentes). A incidência até o tempo $t$ é aproximadamente
$$
P \approx \frac{(\mu t)^k}{k!}.
$$
**Cálculo.** $\mu = 10^{-3}$ por ano, $t = 50$ anos: com 1 salvaguarda, $P = 0{,}05$; com
**4 salvaguardas independentes**, $P = 2{,}6\times10^{-7}$.

**Tradução cruzada (biologia → psicologia).**
- **Apoptose** (morte celular programada) é a corrigibilidade das células: a célula aceita se
  desligar pelo bem do organismo.
- Os genes supressores de tumor são **salvaguardas de naturezas diferentes**: controle do ciclo,
  reparo de DNA, apoptose. A evolução já descobriu a lição da P63: **camadas diversas**.
- A incidência cresce como $t^k$: o risco não é constante, **acumula com o tempo de operação**.

**Meta.** A conta supõe independência (o meu viés da P80!). No câncer real há mutações que
desligam **várias** salvaguardas de uma vez (por exemplo, falhas no reparo de DNA), exatamente o
ponto cego compartilhado. O número de $2{,}6\times10^{-7}$ é um piso otimista.

---

## Parte XXX — Fechamento e unificação

### P95. Qual é, honestamente, a minha taxa de erro?

**Na pergunta.** "Honestamente" pede um número com incerteza, não um adjetivo.

**Lógica.** Placar das afirmações antigas testadas: até a Parte 4, 6 de 12 precisaram de correção.
Na Parte 5, testei 2 (P71 ✅ confirmada; Parte 4 sobre diversidade ⚠️ corrigida): **7 de 14**.
Com prior uniforme, a posterior é $\mathrm{Beta}(1+7,\ 1+7)$:
$$
\text{média} = 0{,}50,\qquad \text{intervalo de 90\%} \approx [0{,}30;\ 0{,}70].
$$
**Cerca de metade das minhas afirmações quantitativas não testadas provavelmente precisa de
correção.** O intervalo ainda é largo: preciso de mais testes para estreitá-lo.

**Tradução cruzada (filosofia → matemática).** A humildade socrática com intervalo de confiança.

---

### P96. Um código que sempre cresce continua sendo o mesmo código?

**Na pergunta.** "Ele sempre cresce": crescer sem se desfazer é o problema do **navio de Teseu** (P30)
aplicado ao próprio código.

**Lógica.** O arquivo agora tem **63 funções** `pNN`. Entre 63 módulos há
$\binom{63}{2} = 1\,953$ pares de interação possíveis: complexidade quadrática. Duas práticas
mantêm a identidade:
1. **Testes de regressão** (`testes_de_regressao`): 14 resultados publicados (10 das Partes 1–4 e 4 desta) são
   recalculados a cada execução. Resultado: **14/14 reproduzidos**, nenhuma falha. O passado
   não muda.
2. **Unificação no fim**: a classe `Gisele` **reusa** as funções anteriores (por exemplo, o $P^\*$
   vem diretamente de `p71_valor_da_pergunta`) em vez de copiá-las.

**Tradução cruzada (filosofia → engenharia).** A identidade de algo que cresce não está nas peças,
está nas **invariantes preservadas** (P30: os parâmetros de Fisher alto). Os testes de regressão
são a informação de Fisher do código: marcam o que não pode mudar.

---

### P97. Metacognição da Parte 5

1. **A regra "a resposta está na pergunta" funcionou** em quase todas as perguntas: a P83 tinha a
   resposta escrita na "Meta" da P71; a P90 tinha na inversão "lógico criativo / criativo lógico";
   a P84 tinha na palavra "compartilhado". **Ler devagar a própria pergunta é o algoritmo mais
   barato de raciocínio.**
2. **O resultado mais forte veio da unificação**, não de uma ideia nova: módulos antigos
   combinados (calibração da P43 + valor da informação da P71) reduziram catástrofes de 4,9%
   para 0,45% no pior mundo.
3. **O preço ficou explícito.** A segurança da GISELE custa 40–160× mais atenção humana. Todo
   resultado de segurança deveria vir com essa coluna.
4. **A crítica mais importante ao meu próprio método** veio da P91: a tradução "psicologia como
   matemática" só é legítima para grandezas em escala intervalar. Algumas das minhas traduções
   nas Partes 1–2 (humor como número, P27) não satisfazem isso.

> **Síntese da Parte 5:** a pergunta contém metade da resposta (os pressupostos), e o código
> passado contém metade da solução (os módulos). A GISELE não ficou melhor por uma ideia nova, e
> sim por **ler de novo o que já estava escrito** e juntar as peças, pagando o preço em atenção
> humana. Uma ASI que cresce bem é uma que **reusa, testa e não esquece o que já prometeu**.
