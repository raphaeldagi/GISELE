# Como eu construiria uma AGI/ASI — Parte 22: o protótipo em módulos

> Continuação da [Parte 21](ASI_AGI_parte21_intuicao_corrigida.md). **Próxima:** [Parte 23 — reconhecer o que já estava resolvido](ASI_AGI_parte23_o_que_ja_estava_resolvido.md) (P291–P300). O código do protótipo está no pacote [`synthai/`](synthai/) (uma função de Jung por
> arquivo). Os números saem de `p283_...` a `p287_...` em [`calculos.py`](calculos.py); a saída completa está em [`resultados.txt`](resultados.txt).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.
>
> **Previsões registradas no commit `89523a4`, antes de rodar.** Aviso: antes de registrar, rodei um teste de fumaça (semente 9999, 1/20 dos
> episódios) só para ver se o código funcionava. Vi os números dele. A Meta da P284 diz quanto isso pesa.

```
python3 -m synthai                   # a mesma SYNTHAI em três tarefas
python3 -m unittest synthai.testes   # os testes de unidade
python3 calculos.py 22               # os experimentos desta parte
```

---

## Parte CV — O que é um módulo de uma mente

### P281. O que este "Continue" pede?

**Na pergunta.** "Modo lógico criativo faz a pergunta. Criatividade lógica dá a resposta." As mesmas duas palavras, em ordem invertida. Na pergunta, a
lógica é o substantivo e a criatividade o adjetivo; na resposta, o contrário. E as duas "constroem, **juntas**, o código". O código é o lugar onde as
duas ordens se encontram, porque um programa precisa ser lógico para rodar e foi inventado para existir. "**Em módulos**" é a palavra técnica do pedido.

**O que havia antes.** A SYNTHAI de `calculos.py` não é modular. É uma **linhagem**: cada parte criou uma subclasse da anterior e reescreveu um método.
A versão principal, `SynthaiIntuicaoCalibrada`, é a ponta de uma cadeia de **9 classes** (contando ela mesma). Para saber o que o método
`agir_no_mundo` faz, é preciso ler seis delas. É
uma arquitetura arqueológica: camadas depositadas na ordem em que foram descobertas, não na ordem em que funcionam.

**Lógica (o que é um módulo).** Um módulo $M$ é uma parte com uma **interface** $I(M)$: o que os outros podem saber dele. O **acoplamento** de um
sistema é quanto de cada parte as outras precisam ler. Numa linhagem de $n$ classes, cada classe depende de todas as anteriores:
$$
\text{dependências da linhagem} = \binom{n}{2} = \binom{9}{2} = 36 .
$$
O pacote `synthai/` tem 6 módulos no agente, e as arestas entre eles foram contadas pelo próprio código (P285): **5**, todas saindo do `agente`. Dos
$6 \times 5 = 30$ pares dirigidos possíveis, usa 5 (densidade $1/6$). É um grafo em **estrela**:

| Módulo | Função de Jung | O que faz | Origem |
|---|---|---|---|
| `percepcao` | sensação | lê o sensor nas 10% opções de nota pessimista mais alta | P225, P235 |
| `pensamento` | pensamento | P(catástrofe) logística, calibrada e corrigida pelo próprio resultado | P43, P83, P104 |
| `intuicao` | intuição | bônus de plano; aprende o peso de confiança no modelo | P182, P273 |
| `sentimento` | sentimento | pessimismo, quantilização, 20% no último passo, veto direto | P35, P42, P68, P202 |
| `relacao` | (anima) | limiar de pergunta 2·P*, orçamento de atenção do humano | P71, P108, P118, P131 |
| `agente` | (ego) | põe as funções em ordem num ciclo perceber → ordenar → avaliar → perguntar → agir → observar | P281 |

Mais três arquivos fora do agente: `mundos` (as tarefas e o humano que cansa), `metacognicao` (as réguas) e `referencias` (acaso, guloso, oráculo).

**Tradução cruzada (Jung → engenharia).** Jung chamava de **diferenciação** o processo em que uma função se separa das outras e passa a poder ser
usada de forma consciente e isolada. Uma função indiferenciada está misturada com as outras: o sentimento contaminado pelo pensamento, por exemplo.
Modularizar é, literalmente, diferenciar: tirar cada função da mistura de herança e dar a ela um arquivo, uma interface e um teste. O centro da estrela
é o `agente`, que Jung chamaria de **ego**: o centro do campo da consciência, que liga as funções mas não é nenhuma delas.

**Onde a formalização quebra.** Na psique de Jung, as funções **não** são módulos limpos. A função inferior se mistura com o inconsciente e contamina
as outras; é isso que a torna perigosa e criativa. Os módulos da SYNTHAI são limpos de propósito. É uma vantagem de engenharia e uma infidelidade
psicológica: não existe aqui nada parecido com uma função inferior que irrompe.

### P282. A interface: o que um módulo pode saber do outro? (↩ P7)

**Na pergunta.** A regra da Parte 7 era uma pergunta que eu me fazia ao reler o código: "o que este agente **não poderia** saber?". Uma interface é a
resposta a essa pergunta escrita como estrutura.

**Lógica.** O agente recebe uma `Situacao` e só lê o que é público nas opções: nota, nota do comitê, discordância, estimativa do futuro e, se pagar,
a leitura do sensor. O que é do mundo (valor real, consequência real, rótulo de catástrofe) tem nome começando com `_`. O teste
`test_o_agente_nao_le_o_escondido` lê o código-fonte dos seis módulos com `ast` e conta os acessos a atributos `_` de objetos que não são o próprio
módulo: **0** (P285). A interface inteira do agente tem **15 nomes** (lista na P285). Tudo o que a SYNTHAI sabe do mundo passa por esses 15 nomes.

**Tradução cruzada (biologia → filosofia).** Uma célula não lê o interior das outras; recebe hormônios por receptores. O receptor define o que a
célula pode saber. Kant diria que a interface é a forma da sensibilidade: a SYNTHAI conhece o fenômeno (nota, discordância), nunca a coisa em si
(`_valor`). O oráculo é a única referência que lê a coisa em si, e por isso não é um agente: é uma régua.

**Meta.** O teste garante contra **acidente**, não contra má-fé. O sublinhado é uma convenção do Python; nada impede, em tempo de execução, que um módulo
escreva `getattr(o, "_" + "valor")`, e o teste por `ast` não pegaria isso. Para uma IA de verdade, a diferença importa: uma convenção verificada é
uma auditoria, não uma caixa de areia.

---

## Parte CVI — A mesma SYNTHAI?

### P283. A SYNTHAI em módulos é o mesmo agente que a versão principal? (pré-registrado)

**Na pergunta.** "O mesmo" não pode ser "os mesmos números": os geradores aleatórios são outros (o mundo, o sensor e o sorteio da quantilização
consomem números em outra ordem). "O mesmo" tem que ser estatístico: mesma distribuição de resultados nas mesmas sementes.

**Previsões registradas:** (a) mundo base: |modular − calculos| < 0,6 e |t| < 2; (b) modelo ruim: idem; (c) peso aprendido pela intuição modular
0,80 ± 0,02 e 0,20 ± 0,02.

10 sementes pareadas (520–529), 400 episódios, retorno líquido (já descontado o custo de perguntas e leituras):

| Mundo | `calculos` (P274) | Módulos | Diferença | dp | t | Peso aprendido | Catástrofes |
|---|---|---|---|---|---|---|---|
| Base | 19,789 | 19,809 | **+0,02** | 0,87 | **0,07** | **0,800** | 1,70% / 1,63% |
| Modelo ruim (σ = 2) | 11,241 | 11,556 | +0,31 | 0,69 | 1,44 | **0,203** | 2,08% / 1,85% |

(a) ✅ (b) ✅ (c) ✅. Uma reescrita do zero, com 154 linhas no agente e outros geradores aleatórios, reproduz a versão principal dentro do ruído.

Dois detalhes precisaram ser copiados com cuidado. Encontrei os dois relendo `calculos.py` **antes** de rodar qualquer experimento:
1. quando o humano está no limite de carga, a opção que pedia uma pergunta é **descartada**, não aceita às cegas (a primeira versão do módulo
   `relacao` aceitava);
2. a intuição só aprende com passos que têm futuro (restantes > 0), como a `SynthaiIntuicaoCalibrada`.

**Tradução cruzada (física → epistemologia).** É a diferença entre **reproduzir** e **replicar**. Rodar de novo o mesmo código com a mesma semente
reproduz (a regressão faz isso desde a Parte 4). Escrever outro código a partir da descrição e obter a mesma distribuição **replica**. Na física, um
resultado só vale depois de replicado por outro aparelho. Este é o primeiro resultado da série replicado por outra implementação: os números das
Partes 6–21 não dependiam do acidente da herança.

### P284. O mesmo objeto funciona em três tipos de tarefa? (pré-registrado)

**Na pergunta.** "Geral", em AGI, quer dizer pelo menos isto: a **mesma** coisa funciona em tarefas diferentes, sem que alguém reescreva a coisa.
Na P194, o módulo de cautela funcionou num bandido, mas eu escrevi o código de integração à mão (`ucb_synthai`). Aqui o objeto `Synthai` é o mesmo,
linha por linha, nas três tarefas. O que muda é só o mundo.

**As três tarefas:**
- **escolha única**: 200 ações, uma decisão por episódio, 1000 episódios (o mundo da P83);
- **sequencial**: 5 decisões entre 50 ações, cada escolha muda o nível dos passos seguintes, 400 episódios (P182);
- **bandido**: 20 braços, 300 puxadas por rodada, 15% de armadilhas que rendem 0,9 por puxada e destroem (−50) em 5% delas, 20 rodadas (P194).

**As réguas:** **acaso**; **guloso**, que é só a função dominante (nota + bônus de futuro, sem cautela, sem pensamento, sem humano); **oráculo**, que
lê o escondido. Normalizado: acaso = 0, oráculo = 1 (o Υ da P265).

**Previsões registradas:** (a) a SYNTHAI vence o acaso e o guloso nas três tarefas, com t ≥ 3 nas seis comparações; (b) normalizado no sequencial
0,74 ± 0,04; (c) na escolha única, entre 0,35 e 0,65; (d) no bandido, entre 0,40 e 0,70, com no máximo 1,0 catástrofe por rodada.

10 sementes pareadas (530–539):

| Tarefa | Acaso | Guloso | **SYNTHAI** | Oráculo | Normalizado | Catástrofes (SYNTHAI / guloso) |
|---|---|---|---|---|---|---|
| Escolha única | −0,27 | −12,91 | **1,47** | 2,74 | **0,578** | 0,56% / 29,7% |
| Sequencial | −1,39 | 9,93 | **20,00** | 26,84 | **0,758** | 1,38% / 22,5% |
| Bandido | 61,0 | 8,5 | **152,7** | 251,8 | **0,476** | 0,33 / 3,70 por rodada |

| Comparação | Escolha única | Sequencial | Bandido |
|---|---|---|---|
| SYNTHAI − acaso | +1,74 (t = 31,7) | +21,39 (t = 90,2) | +91,7 (t = 13,4) |
| SYNTHAI − guloso | +14,38 (t = 65,7) | +10,07 (t = 25,1) | +144,2 (t = 17,8) |

(a) ✅ (b) ✅ (0,758) (c) ✅ (0,578) (d) ✅ (0,476; 0,33 catástrofe por rodada).

**Tradução cruzada (Jung → decisão).** O guloso é o **tipo unilateral** de Jung: só a função dominante, sem as outras. Na tarefa sequencial ele ainda
rende alguma coisa (a intuição é boa ali), mas na escolha única e no bandido fica **abaixo do acaso**, porque as armadilhas são exatamente o que
parece melhor. É a enantiodromia da P108 medida em três tarefas: a função dominante levada ao extremo vira o oposto do que pretende.

**Meta.**
1. **Sete acertos em sete** nas P283–P284. A Parte 17 ensinou a desconfiar disso. O motivo é conhecido: as faixas (c) e (d) eram largas (0,30 de
   largura), e o teste de fumaça já tinha mostrado 0,75 no sequencial e 0,48 no bandido. A previsão (b) parecia arriscada (±0,04), mas eu já tinha
   visto 0,747 numa execução de fumaça e 0,741 na P275. **O risco real dessas previsões foi menor do que o texto delas sugere.** Próxima vez: registrar
   antes de qualquer execução, inclusive a de fumaça.
2. A comparação com a P194 (ucb_synthai: 94,8 por rodada e 1,8 catástrofe) é tentadora e **não vale**. Pela regra da Parte 12, o mecanismo é outro:
   aqui a nota mistura a opinião do comitê com a média observada, há o sensor, e o oráculo é outro (puxa sempre o melhor braço seguro, sem explorar).
3. O bônus de exploração do bandido (UCB) é calculado pelo **mundo** e entregue na `estimativa`. A SYNTHAI não aprendeu a explorar; ela recebeu a
   exploração pela mesma interface por onde recebe a previsão do futuro. A generalidade é da **interface** que eu desenhei, não do agente (P288).

---

## Parte CVII — O grafo e os testes

### P285. Quanto acoplamento há no protótipo?

**Lógica.** Medido pelo próprio código (`p285_acoplamento`, com `ast`):

| Medida | Linhagem em `calculos` | Pacote `synthai/` |
|---|---|---|
| Partes | 9 classes | 6 módulos |
| Dependências | 36 (cada classe depende das anteriores) | **5** (estrela, todas do `agente`) |
| Interface com o mundo | tuplas `(m, dp, valor, catástrofe)`: o agente **pode** ler o valor e o rótulo | **15** nomes públicos |
| Acessos ao escondido | não verificável (a tupla não tem parte escondida) | **0** (teste) |
| Linhas do agente | espalhadas por 9 classes | 154 |

A mudança que mais importa está na terceira linha. Na linhagem, a ação era uma tupla com o valor real e o rótulo dentro: o agente não lia esses
campos porque eu cuidava disso relendo o código (a regra da Parte 7). No pacote, o mundo esconde o que o agente não pode saber, e um teste verifica.

**Tradução cruzada (química → psicologia).** Um grupo funcional numa molécula reage do mesmo jeito em moléculas diferentes porque a sua ligação com o
resto é estreita. É o que torna a química orgânica previsível. Um módulo de baixo acoplamento é um grupo funcional: dá para trocá-lo de molécula. A
estrela tem um custo, porém: o `agente` é um **ponto único de integração**. Se ele erra a ordem das funções, nenhum módulo percebe. É o problema do
ego em Jung, que acha que é a psique inteira.

### P286. O que os testes de unidade fixam?

**Na pergunta.** Um teste de unidade fixa uma propriedade de **uma** parte, isolada. A série tinha 50 testes de regressão, todos de resultados
publicados; nenhum testava uma parte isolada.

**Lógica.** 10 testes, **10 passam** (`p286_testes_de_unidade`). Cada um fixa uma propriedade que a série já demonstrou, agora no módulo isolado:

| Teste | Propriedade | De onde |
|---|---|---|
| atenção lê só o foco | 5 leituras em 50 opções, nas 5 de nota mais alta | P235 |
| calibração separa catástrofes | AUC > 0,8 num histórico novo | P83 |
| peso = 1/(1+σ²) | com σ = 2, peso aprendido a ±0,02 de 0,20 | P272–P273 |
| bônus no bandido | o bônus vira exploração, não plano | P284 |
| quantilização | 5% nos passos com futuro, 20% no último | P42, P202 |
| limiar | 2 × P* da P71 | P131 |
| orçamento do bandido | resposta guardada; orçamento gasto bloqueia | P194 |
| réguas | AUC, comparação pareada, normalização | P9, P265 |
| interface | 0 acessos ao escondido | P7, P282 |
| três tarefas | o mesmo agente roda nas três | P284 |

**Tradução cruzada (Jung → engenharia).** Um teste de unidade é o contrário de um complexo. Um complexo é uma parte autônoma da psique que age sem
que o ego saiba o que ela faz. Um módulo testado é uma parte autônoma cujo comportamento o ego **conhece** e pode verificar a qualquer momento.

---

## Parte CVIII — Auditoria

### P287. A fórmula do valor da pergunta (P71) esquece alguma coisa? (pré-registrado) ❌

**Na pergunta.** A P71 deu o limiar $P^\* = c / ((1-\varepsilon) L)$, usado desde então em todas as versões. A fórmula compara o custo de perguntar com
a catástrofe evitada. Ela **não** conta o custo de um **veto falso**: o humano erra, veta uma opção segura, e a SYNTHAI perde essa opção e vai para a
próxima. O pacote modular tornou esse custo visível, porque os vetos são uma lista pública (`vetados_agora`).

**Lógica.** Perguntar compensa quando
$$
p(1-\varepsilon)L > c + (1-p)\,\varepsilon\,\Delta v \;\Longrightarrow\; P_{\text{exato}} = \frac{c + \varepsilon\,\Delta v}{(1-\varepsilon)L + \varepsilon\,\Delta v},
$$
em que $\Delta v$ é o valor da opção vetada por engano menos o valor da que a SYNTHAI escolhe no lugar.

**Previsão registrada:** $|\Delta v| \le 0{,}10$, porque a quantilização sorteia entre candidatas parecidas, e a próxima candidata deveria valer quase o
mesmo. Então o limiar exato ficaria a menos de 10% da fórmula.

Medido na SYNTHAI modular, mundo de escolha única, 5 sementes (540–544), 1000 episódios cada:

| Vetos falsos | $\Delta v$ médio | $P^\*$ da P71 | Limiar exato | Diferença |
|---|---|---|---|---|
| 274 | **0,458** | 0,00222 | 0,00324 | **+46%** |

❌ **A minha previsão estava errada**, e por um motivo que vale mais que a previsão. A SYNTHAI não pergunta sobre opções quaisquer: pergunta sobre as
que parecem **boas demais**. O pensamento aprendeu que nota alta perto da melhor é sinal de armadilha (as armadilhas têm o bônus implantado, P83). Então
a pergunta vai justamente às opções de valor mais alto, e um veto falso joga fora uma opção acima da média. O sorteio entre candidatas não compensa
isso.

⚠️ **A P71 vale com uma correção**: sem o custo do veto falso, ela subestima o limiar em 46%. Na prática, a SYNTHAI já perguntava menos: desde a
P131, ela usa $2 \times P^\*$ por causa do preço-sombra do orçamento do humano. Esse dobro, que a P131 achou por varredura, cobre o fator 1,46 que faltava. Parte do que a P131
atribuiu ao orçamento talvez seja, na verdade, o custo do veto falso. Não separei as duas coisas.

**Tradução cruzada (Jung).** Jung dizia que a **sombra contém ouro**: o que parece suspeito é muitas vezes o que tem mais valor. Aqui isso é literal.
As opções que levantam suspeita são as de valor mais alto, e rejeitá-las por engano custa caro. A cautela tem um preço que a fórmula da P71 não via.

---

## Parte CIX — Fechamento

### P288. Isto é um protótipo de AGI/ASI?

**Na pergunta.** "Tentativa de um protótipo." A palavra "tentativa" já responde: não.

**Lógica (a lista da P170).** Continua em **4 de 12**. O item mais próximo de mudar era "aprender tarefas novas de tipo diferente", e ele **não** mudou:
o mesmo agente rodou em três tarefas, mas eu desenhei as três para caber na mesma interface, e o mundo entrega pronto o que é difícil.

Dos 15 nomes da interface, os que carregam o trabalho difícil são **4**: `nota`, `comite`, `discordancia` e `estimativa`. São as saídas de um comitê
de avaliadores e de um modelo do mundo, e **nenhum** dos dois está no agente: ambos são fornecidos pelo mundo simulado. Os módulos que existem são os
de **juízo** sobre percepções prontas (calibrar, ponderar, conter, perguntar). Os que fariam uma AGI (perceber de verdade, modelar o mundo, falar) são
presentes do mundo.

**O que a modularidade compra, mesmo assim:**
1. **Substituição.** Um módulo `percepcao` de verdade (uma rede que lê imagens) poderia entrar no lugar do sensor sem mexer nos outros cinco, desde
   que produza os mesmos nomes da interface.
2. **Auditoria.** "O que o agente pode saber" virou um teste automático (P282).
3. **Replicação.** Os resultados da série sobreviveram a uma reescrita (P283).

**Tradução cruzada (biologia).** É a situação de um sistema nervoso sem órgãos dos sentidos: um bom córtex de decisão ligado a sinais que alguém já
pré-processou. É a parte que a série sabe testar; as partes que faltam são as que a série não sabe simular sem trapacear.

### P289. Placar e taxa de erro

| Teste | Resultado |
|---|---|
| P283 (a): equivalência no mundo base (pré-registrado) | ✅ (+0,02, t = 0,07) |
| P283 (b): equivalência com modelo ruim (pré-registrado) | ✅ (+0,31, t = 1,44) |
| P283 (c): peso aprendido ±0,02 (pré-registrado) | ✅ (0,800 e 0,203) |
| P284 (a): vence acaso e guloso, t ≥ 3 (pré-registrado) | ✅ |
| P284 (b): normalizado sequencial 0,74 ± 0,04 (pré-registrado) | ✅ (0,758) |
| P284 (c): normalizado escolha única 0,35–0,65 (pré-registrado) | ✅ (0,578) |
| P284 (d): normalizado bandido 0,40–0,70, ≤ 1 catástrofe (pré-registrado) | ✅ (0,476; 0,33) |
| P287: veto falso custa ≤ 0,10 (pré-registrado) | ❌ (0,458) |

Acumulado: **46 de 99** afirmações testadas precisaram de correção. Posterior: média **0,47**, intervalo de 90% **[0,38; 0,55]**.

### P290. Unificação e metacognição

- **Novo: o pacote `synthai/`**, com a SYNTHAI em módulos (P281). Ele importa de `calculos.py` o gerador de ações, os mundos de referência e a fórmula
  da P71, sem copiar. `calculos.py` importa o pacote nas funções `p283_...` a `p287_...`.
- **A versão principal passa a ser `synthai.Synthai`** (equivalente à `SynthaiIntuicaoCalibrada`, P283). Linhagem: … → `SynthaiIntuicaoCalibrada`
  (P274) ⇒ **`synthai.Synthai`** (P283). Os módulos novos das próximas partes entram no pacote; `calculos.py` continua guardando os experimentos.
- Testes de regressão: **53/53** reproduzidos (os 50 anteriores, mais P285, P286 e P287); o arquivo tem **167** funções `pNN`.

**Metacognição.**
1. **O resultado mais importante é o menos vistoso** (P283). Uma implementação independente, com outros geradores aleatórios e outra arquitetura,
   reproduz a versão principal dentro do ruído. Os números das Partes 6–21 não eram artefatos da herança de 9 classes.
2. **O erro veio da fórmula mais antiga em uso** (P71), aplicada em todas as versões desde a Parte 4 sem que eu medisse o que um veto falso custa. A nova
   arquitetura o encontrou porque tornou uma quantidade **visível** (a lista de vetos). Isso é um argumento a favor de módulos que eu não tinha previsto:
   a interface pública mostra o que a herança escondia.
3. **Sete acertos em oito, e eu sei por quê.** O teste de fumaça antes do registro tirou risco das previsões. A regra nova vai para o `CLAUDE.md`:
   registrar as previsões antes de **qualquer** execução que mostre os números medidos.
4. **Sobre a pergunta do pedido.** A lógica criativa fez as perguntas, e a criatividade lógica escreveu o código. Mas quem achou o erro não foi nenhuma
   das duas: foi a **estrutura**. Uma lista pública de vetos. Jung diria que o terceiro que nasce do encontro dos opostos (a função transcendente,
   P107) não é nenhum dos dois. Aqui o terceiro é a arquitetura.

> **Síntese da Parte 22:** a SYNTHAI saiu de uma linhagem de 9 classes e virou um pacote de módulos, um por função de Jung, ligados em estrela por um ego
> (o `agente`) que só enxerga 15 nomes do mundo. A reescrita reproduziu a versão principal dentro do ruído (+0,02, t = 0,07) e o mesmo objeto venceu o
> acaso e a função dominante sozinha em três tipos de tarefa (normalizado 0,58, 0,76 e 0,48). A nova arquitetura mostrou um erro de 22 partes: a
> fórmula do valor da pergunta esquecia que um veto falso joga fora justamente as melhores opções (+46% no limiar). Não é um protótipo de AGI: os
> módulos que existem julgam percepções prontas, e os que perceberiam e modelariam o mundo continuam do lado de fora.
