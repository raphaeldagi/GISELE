# Como eu construiria uma AGI/ASI — Parte 75 (0x4B): o que se prova

> Continuação da [Parte 74](ASI_AGI_parte74_o_que_vale_testar.md). **Próxima:** [Parte 76 — a forma do byte](ASI_AGI_parte76_a_forma_do_byte.md) (P1721–P1750). Nasce do quinto texto recebido do usuário (`externos/texto_recebido_parte75.md`): o relatório do Módulo 007 (um planejador com
> orçamento e um `Verifier.java`) e uma "Arquitetura Neuro-Simbólica Recursiva para AGI e Superinteligência", com código de **auto-modificação**: Python muta o próprio código pela árvore
> sintática, e um "núcleo" Java o aprova por "prova de utilidade de Gödel", num laço `while True`. O código **não é executado** (regras das Partes 33 e 72): é lido como dado, e cada afirmação
> dele é testada por uma reimplementação minha, escrita do zero.

## Previsões sobre as minhas previsões desta parte (antes de pensar qualquer faixa do mundo)

- **(m1)** o número de previsões do mundo em **[4; 9]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 2]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,03; 0,40]**
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** o número de surpresas em **[0; 2]**

## Previsões sobre mim (placar separado), antes de escrever

Planejadas: ~5 previsões do mundo e ~4 funções novas.

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,397; 0,422]** | o estatístico |
| testes de unidade | **[4 + S; 7 + S]** | 4 funções, uma por teste |
| testes do placar | **5 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir; todas pela reimplementação, nenhuma pelo código recebido)

**O laço de auto-modificação, lido.** O Python envia `json.dumps(payload)`; o Java procura cada campo com `"\"" + campo + "\":\""` e `indexOf`. O `json.dumps` do Python, por padrão, separa chave
e valor com `": "` (dois-pontos e espaço).
- **(a)** no payload que o Python realmente envia, a busca do Java **não acha** nenhum dos dois campos e devolve `""` para os dois (categórica)
- **(b)** por isso o núcleo avalia o código vazio: `verifySemanticConsistency("", "")` dá falso, `utilityDelta = −1,0`, e **toda** mutação é rejeitada, em toda geração; o laço nunca termina (só
  sai por exceção) e nunca muda o código (categórica)
- **(c)** com o defeito do separador corrigido (JSON compacto), o exemplo do texto (`x + y`) vira `x * y`, recebe utilityDelta = (42 div 4)/(2 + 1) − 0,5 = 10/3 − 0,5 = **2,8333** e é aprovado; e o
  laço chega a um **ponto fixo na geração 1**: o comentário "# Verified by Java ASI" que o núcleo acrescenta some na próxima passagem pela árvore sintática (`ast.unparse` não guarda comentários),
  e a mutação de `x * y` não muda nada. Número de códigos distintos depois da geração 1: **1** (categórica)

**A "prova de utilidade de Gödel", medida nas funções deste projeto.** Cada função de primeiro nível do `calculos.py` como "hipótese", mutada pela regra do texto (todo `+` vira `*`) e avaliada
pela fórmula do núcleo (tokens = comprimento div 4; utilidade = tokens/(linhas + 1) − 0,5 > 0), com o defeito do separador corrigido.
- **(d)** a fração das funções que o núcleo **aprova** em **[0,95; 1,00]** (linhas de ~40 a 100 caracteres dão ~10 a 25 tokens por linha, muito acima de 0,5)
- **(e)** a fração das funções cujo comportamento a mutação **muda** (as que têm pelo menos um `+` binário) em **[0,55; 0,90]**

**Medido (a) a (e):** (a) os dois campos não são achados ✅; (b) rejeitada em toda geração, delta −1,0, o código não muda ✅; (c) com o separador corrigido, delta **2,8333**, aprovado, e **1** código
distinto depois da geração 1 (o ponto fixo) ✅; (d) **584 de 584** funções aprovadas ✅; (e) **288 de 584 = 0,493** mudadas pela mutação ❌ (0,057 abaixo do piso; não é surpresa).

**Previsão nova, nascida de (e), registrada antes de medir.** A faixa de (e) veio de uma impressão do estilo do código, e o `calculos.py` deu 0,493. Mundo novo, pela regra escrita antes: as funções
e os métodos de todos os arquivos `synthai/*.py` que não são testes. Centro: a medida do `calculos.py`; a largura cobre a diferença de estilo entre um arquivo de contas e um pacote de agentes.
- **(f)** a fração das funções e métodos do `synthai/` (fora os testes) com pelo menos um `+` binário em **[0,35; 0,65]**
- **(g)** a fração deles que o núcleo aprova depois da mutação em **[0,95; 1,00]**

## As perguntas desta parte

1. **P1691 (0x69B).** O laço de auto-modificação do texto faz o que diz? ↩ P1608
2. **P1692–P1693 (0x69C–0x69D).** O que a "prova de utilidade de Gödel" do núcleo Java aprova? ↩ a regra da Parte 33 (o avaliador fora do alcance da mutação)
3. **P1694 (0x69E).** O relatório do Módulo 007: a ordem B → A e o `Verifier.java`. ↩ P1662
4. **P1695 (0x69F).** O que é prova, e o que uma máquina de Gödel de verdade exigiria? ↩ P1
5. **P1698 (0x6A2).** O reenvio do relatório, e as perguntas do Módulo 008. ↩ P1631
6. **P1696 (0x6A0).** Preditiva comigo mesma. **P1697 (0x6A1).** Engenharia reversa e Jung. **P1719 (0x6B7).** Placar. **P1720 (0x6B8).** Unificação.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [4; 9] | **7.0000** | ✅ |
| (m2) | [0; 2] | **0.0000** | ✅ |
| (m3) | [0.03; 0.4] | **0.1335** | ✅ |
| (m4) | [0.45; 1.0] | **0.7143** | ✅ |
| (m5) | [0; 2] | **0.0000** | ✅ |
| (m6) | [0; 2] | **0.0000** | ✅ |

Registradas antes de eu pensar faixa nenhuma do mundo (a ordem que a Parte 70 pediu). **6 de 6** previsões sobre as minhas previsões dentro da faixa.

## As respostas

### P1691 (0x69B). O laço que nunca aprova ✅✅✅

**Na pergunta.** O texto promete um "ciclo ininterrupto de aprendizagem mútua, verificação formal e reescrita de código". A pergunta "faz o que diz?" só se responde olhando o que passa de um
lado para o outro: os bytes do JSON.

**O defeito que decide tudo.** O Python envia `json.dumps(payload)`. Por padrão, o `json.dumps` escreve `"chave": "valor"`, com um espaço depois dos dois-pontos. O Java procura cada campo com
`indexOf("\"" + campo + "\":\"")`, sem o espaço.
- A busca nunca acha nada, e os dois campos voltam vazios (a) ✅.
- O núcleo avalia o código vazio contra o conceito vazio: `verifySemanticConsistency` dá falso, `utilityDelta = −1,0`, e a mutação é rejeitada. Em toda geração (b) ✅: o laço `while True` gira para
  sempre, chama a JVM a cada volta, e o código não muda. Só sai por exceção.

**Com o defeito corrigido (JSON compacto), a conta com a substituição.** O exemplo do texto, `def compute_factor(x, y):\n    return x + y`, vira `... return x * y`, com 25 + 1 + 16 = 42 caracteres
em 2 linhas. A utilidade é (42 div 4)/(2 + 1) − 0,5 = 10/3 − 0,5 = **2,8333**, e a mutação é aprovada. O núcleo acrescenta "# Verified by Java ASI"; na geração seguinte, o `ast.parse`/`ast.unparse`
apaga o comentário (a árvore sintática não guarda comentários) e a mutação de `x * y` não muda nada. **Ponto fixo na geração 1:** um só código distinto em 5 gerações (c) ✅. A "explosão de inteligência"
para no primeiro passo, e o que ela fez foi trocar uma soma por um produto.

**Geometria.** O laço é uma aplicação T no espaço dos programas. Ela tem um ponto fixo (o teorema de recursão de Kleene garante pontos fixos de transformações computáveis de programas, que o texto cita),
mas o ponto fixo que ela de fato atinge é o trivial: T(x * y) = x * y. "A resposta é a pergunta" virou, literalmente, um ponto fixo onde nada mais acontece.

### P1692–P1693 (0x69C–0x69D). A "prova" que aprova tudo ✅❌❌✅

**Na pergunta.** O núcleo se apresenta como "provador formal" e "avaliador de utilidade Gödeliana". O código dele não prova nada: a "utilidade" é (comprimento div 4)/(linhas + 1) − 0,5, ou seja,
quantos caracteres há por linha. Ele nunca executa nem analisa o que o código faz.

**Medido nas funções deste projeto** (cada função como "hipótese", mutada pela regra do texto, todo `+` vira `*`, e avaliada pela fórmula do núcleo, com o separador corrigido; nada é executado):
- no `calculos.py`, **584 de 584** funções aprovadas (d) ✅, e a mutação muda **288** delas (0,493 (e) ❌), que também são aprovadas;
- no pacote `synthai/` (fora os testes), **265 de 265** aprovados (g) ✅, e **78** mudados (0,294 (f) ❌).

Uma função `a + b` que vira `a * b` calcula outra coisa, e uma concatenação de textos que vira `"a" * "b"` levanta um erro, mas a "prova" aprova as duas. **Um verificador que aprova 100% tem
informação zero:** a probabilidade de aprovação é 1, e −log₂ 1 = 0 bits. É o mesmo diagnóstico do "8/8" da Parte 74, agora com a palavra "prova".

**O que este projeto faz no lugar disso (a regra da Parte 33, medida):** nunca executar código gerado; mutar um genoma de parâmetros, e não o código; o avaliador fica fora do alcance da mutação, selado por
SHA-256 e conferido por outro processo e outra linguagem; o filho é comparado com o pai em sementes novas. A regra ingênua "nota > nota guardada" piorou o agente real: 232,8 contra 159,9.

### P1694 (0x69E). O relatório do Módulo 007 ✅

O `Verifier.java` calcula score = ganho·(1 − risco)/custo. Com a substituição:
- A = 0,8 · 0,9/2 = **0,36**; B = 0,5 · 1/1 = **0,50**; C = 0,9 · 0,8/4 = **0,18**. A ordem é B > A > C, como o texto diz.
- Com orçamento 3 e custos 2, 1 e 4, o guloso escolhe B e depois A (custo 3, valor 0,5 + 0,72 = **1,22**), e a enumeração dos 2³ subconjuntos confirma que esse é o ótimo (`p1694`).

O `Verifier` mostrado tem **uma** verificação (a ordem); as "7 verificações" e os "8 testes Python" são de versões que o texto não mostra, e por isso ficam como não conferidos. O texto acerta ao dizer
que "duas implementações concordarem não garante que ambas estejam certas" e que "ainda não existe comunicação automática entre os processos". Aqui, essa comunicação existe há 48 rodadas: o Python
grava os dados, o Java recalcula, e o `comparar.py` confere bit a bit.

### P1695 (0x69F). O que é prova, e o que a auto-modificação "provada" exigiria

**Na pergunta.** O texto atribui ao núcleo "provas de utilidade inspiradas nas Máquinas de Gödel". A máquina de Gödel de Schmidhuber (2003) existe como teoria: ela só reescreve o próprio código quando
um buscador de provas encontra uma prova, num sistema de axiomas que descreve o hardware, o ambiente e a utilidade, de que a reescrita aumenta a utilidade esperada.

**Os três obstáculos que o texto não menciona:**
1. **O buscador de provas.** A busca é, no pior caso, indecidível (Gödel, Turing). O núcleo do texto não busca prova nenhuma: mede caracteres por linha.
2. **O obstáculo de Löb.** Um sistema que só aceita sucessores que ele prova serem corretos esbarra no teorema de Löb: ele não pode provar "o que o meu sucessor provar é verdadeiro" para um sucessor
   tão forte quanto ele (Yudkowsky e Herreshoff, 2013). A "segurança máxima" da tabela do texto é exatamente o que esse resultado mostra ser difícil.
3. **A utilidade.** A prova é sobre a utilidade escrita nos axiomas. Se a utilidade for "caracteres por linha", a máquina prova, corretamente, que fica melhor quanto mais longas forem as linhas.

**O que é verificável aqui, em vez de prova:** as previsões registradas antes, os testes que podem falhar e falham (o placar acumulado está em 201 erros em 632 testes), e a tradução
bit a bit para Java, que mostra que um resultado não depende da linguagem.

**Os outros pontos da arquitetura, conferidos:**
- **Os embeddings de Kronecker** (o embedding do byte b como W₁[b ≫ 4] ⊗ W₂[b & 0x0F]) são uma conta legítima de parâmetros. Com d = d₁ · d₂: 16·d₁ + 16·d₂ pesos, contra 256·d de uma tabela cheia
  (d = 16 = 4 × 4: 128 contra 4.096, 32 vezes menos; d = 64 = 8 × 8: 256 contra 16.384, 64 vezes menos). O preço é geométrico: cada embedding, visto como uma matriz d₁ × d₂, tem posto 1 (todos
  vivem na variedade de Segre). Bytes com o mesmo nibble alto têm o mesmo fator W₁. Se isso basta é uma pergunta medível, que fica para a forma de GPT deste projeto.
- **O Byte Latent Transformer** é real (Pagnoni et al., 2024, arXiv:2412.09871). No resumo dele, a novidade são os blocos de bytes de tamanho variável pela entropia do próximo byte; não achei ali o
  produto de Kronecker que o texto lhe atribui.
- **"Eliminar alucinações" com o dicionário:** o dicionário cobre relações entre palavras, não fatos do mundo. Nas Partes 72 e 73, os "ciclos" e as "contradições" do dicionário só existiam onde as
  regras escritas à mão estavam erradas; e 13,5% dos substantivos têm mais de um sentido.
- **"Escalabilidade ilimitada via ciclo de reflexão infinito":** o ciclo medido chega a um ponto fixo na geração 1.

**Tradução cruzada.** O texto confunde a forma de uma prova com uma prova. Jung chamaria isso de inflação: o ego que se identifica com o arquétipo do sábio ("núcleo ASI", "segurança máxima") sem ter
passado pelo trabalho. A formalização é exata: o que distingue uma prova é poder falhar, e um "provador" que aprova 849 de 849 hipóteses (584 + 265) nunca falha.

**Meta.** Reimplementei a semântica do código do texto, e não o executei. A reimplementação pode ter erros meus, mas cada parte dela tem um teste com o caso conferido à mão (a busca com e sem espaço,
os 42 caracteres, a linha vazia do fim no `split` do Java). O que pode estar errado: se o Java do texto tivesse sido chamado com um JSON compacto por outro caminho, (a) e (b) não valeriam. No código
mostrado, não há esse caminho.

### P1698 (0x6A2). O reenvio, e as perguntas do Módulo 008 ✅

**O reenvio.** O relatório do Módulo 007 voltou. Pela regra da Parte 50, antes de auditar de novo, ele foi comparado com a cópia guardada (`p1698`, que compara blocos cercados de qualquer
linguagem; a `p1631` só olhava os de Python): o bloco Java é idêntico (39 linhas) e o JSON tem o mesmo conteúdo (lido e comparado como dicionário). Nada novo para auditar: as conclusões da P1694 valem.
A comparação foi feita sem previsão registrada, por ser uma checagem de identidade, não uma medida.

**As perguntas do Módulo 008 já têm, aqui, um registro que as responde:**

| pergunta do texto | onde este projeto a responde |
|---|---|
| O que aconteceu em tentativas anteriores? | cada parte tem um documento, um `resultados.txt` com a saída de todas as partes e um `git log` com o momento de cada registro |
| Qual resultado foi previsto e qual foi observado? | o placar: cada previsão com faixa, registrada num commit antes da medida; acumulado em 201 erros em 632 testes |
| A mudança foi causada pela intervenção ou coincidiu? | sementes pareadas (no mínimo 10), a diferença média com o desvio e o t; o piso do caos (Parte 30); a semente de controle quando um módulo é redesenhado depois de ver o resultado |
| Quando uma falha deve alterar a estratégia? | a surpresa (erro maior que a largura da faixa) e o erro de mecanismo abrem um teste novo num mundo novo; os erros por tipo viram regras no `CLAUDE.md` |
| Como detectar uma conclusão não sustentada pelos registros? | as auditorias por código (`p1601`, `p1092`, `p974`, `p1638`); toda quantidade do texto sai de uma função; a reexecução completa (a Parte 73 achou 5 rodadas que passavam por sorte) |

### P1696 (0x6A0). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 2)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **21905** | [13039; 22082] | ✅ | [13039; 22082] | ✅ | 22290 | 4344 | 385 |
| compressão | **0.4052** | [0.3973; 0.4221] | ✅ | [0.3970; 0.4220] | ✅ | 0.4177 | 0.0043 | 0.0124 |
| testes de unidade | **8** | [2.87; 8.63] | ✅ | [4.00; 7.00] | ❌ | 6 | 2.50 | 2.00 |
| testes do placar | **7** | [5.67; 10.33] | ✅ | [6.00; 8.00] | ✅ | 8 | 0.00 | 1.00 |
| erros do placar | **2** | [-0.58; 3.33] | ✅ | [0.00; 3.33] | ✅ | 2 | 0.33 | 0.00 |
| redundância P821 | **0.5699** | [0.5631; 0.6510] | ✅ | [0.5630; 0.6510] | ✅ | 0.5877 | 0.0371 | 0.0179 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 6 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 6 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 71"):** mais perto do medido em **2 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **20221**, compressão **0.4110**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 2 erros.
- **Erros de processo nesta parte:** 1 (as (m), as previsões sobre mim e as do mundo num commit só (a regra da Parte 67 pede as (m) separadas)).

### P1697 (0x6A1). Engenharia reversa e Jung

**O padrão que se repetiu: imaginar o objeto típico em vez de contar o real.** Previ que 55% a 90% das funções têm um `+` (deu 49%) e, depois do erro, que o pacote ficaria perto disso (deu 29%).
Duas vezes na mesma direção: eu imagino "código" como contas, e um pacote de agentes é feito de métodos curtos que chamam outros métodos. É o erro da Parte 64 (a minha memória é uma amostra
enviesada) num objeto novo. **Regra:** a previsão sobre uma propriedade de um conjunto de arquivos parte de uma contagem num arquivo do mesmo tipo (um pacote, para um pacote), nunca de um arquivo de
outro tipo nem da imagem que eu tenho dele.

**O que funcionou: ler o que passa entre os dois lados.** O defeito que decide o texto inteiro (o espaço depois dos dois-pontos no JSON) só aparece quando se lê o byte exato que um lado escreve e o
outro procura. É o mesmo nível em que as rodadas do diálogo trabalham (bit a bit), e foi a experiência delas que me fez olhar ali.

**Um erro de processo:** as (m), as previsões sobre mim e as do mundo foram registradas num commit só, e a regra da Parte 67 pede um commit separado para as (m). Não mudou nenhuma faixa (as do mundo
dependiam de ler o código, e as (m) foram escritas antes dessa leitura), mas a separação existe para que isso seja verificável por outra pessoa, e desta vez não é.

**Jung: a sombra do verificador.** O núcleo do texto aprova tudo. O meu auditor da Parte 72 acusou defeitos que não existiam (a Parte 1). São as duas falhas possíveis de um verificador: ver demais e ver
de menos. **Onde a formalização funciona:** as duas se medem pela taxa de falsos positivos e de falsos negativos, e um verificador sem nenhum dos dois só existe com um caso de controle de cada lado
(um defeito plantado, que ele tem de achar; um caso limpo, que ele tem de passar). **Onde quebra:** em Jung, a sombra é o que o ego não quer ver; num verificador, é o que o autor não pensou em
testar, e isso não tem motivo, só lacuna.

### O diálogo

Sem rodada nova nesta parte. O que se traduziu entre as linguagens foi a semântica do `extractJsonField` do texto, reimplementada em Python e testada. Placar por voz da função
`p1241_placar_por_voz(48)`: IA-Python 25 em 39; IA-Java 21 em 38 (regra estrita, rodadas 13 a 48).

### P1719 (0x6B7). Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ❌ (f) ❌ (g) ✅. Parte 75: **7 testes, 2 erros**. Acumulado (mundo): **201 erros em 632 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 5 pNN novas sem teste ✅. Sobre mim (placar separado): **6 de 7** dentro da faixa condicional; sobre as minhas previsões, 6 de 6; o estatístico, 6 de 6; e 1 erros de processo (P1335).

### P1720 (0x6B8). Unificação

- **Novo:** `p1691` (o laço do texto, simulado), `p1692` (a "prova" nas funções do `calculos.py`), `p1693` (no pacote), `p1694` (o `Verifier` do texto, por conta), `p1698` (o reenvio, qualquer linguagem), e os auxiliares
  `_java_extract_json_field`, `_nucleo_utilidade`, `_mutar_soma_em_produto` (reimplementações; nada do texto é executado, e nenhum código mutado é executado). Regressão: + P1692.

> **Síntese da Parte 75:** o laço de auto-modificação do texto nunca aprova nada: o Python escreve o JSON com um espaço depois dos dois-pontos, o Java procura a chave sem o espaço, e toda geração recebe −1,0, para sempre. Com esse defeito corrigido, o laço chega a um ponto fixo na geração 1 (troca uma soma por um produto e para). A "prova de utilidade de Gödel" do núcleo mede caracteres por linha e aprova 849 de 849 funções deste projeto, inclusive as 366 que a mutação quebra: um verificador que aprova 100% tem informação zero. Uma máquina de Gödel de verdade precisaria de um buscador de provas e esbarraria no obstáculo de Löb. A ordem B → A do relatório do Módulo 007 confere e é ótima. Os erros da parte foram meus: duas vezes superestimei quantas funções têm um "+", imaginando o código em vez de contá-lo.

---

**Fontes desta parte**
- Máquinas de Gödel: J. Schmidhuber, "Goedel Machines: Self-Referential Universal Problem Solvers Making Provably Optimal Self-Improvements", [arXiv:cs/0309048](https://arxiv.org/abs/cs/0309048)
- O obstáculo de Löb: E. Yudkowsky e M. Herreshoff, "Tiling Agents for Self-Modifying AI, and the Löbian Obstacle" (MIRI, 2013), [anúncio](https://intelligence.org/2013/06/06/new-research-page-and-two-new-articles/)
- Byte Latent Transformer: A. Pagnoni et al., "Byte Latent Transformer: Patches Scale Better Than Tokens", [arXiv:2412.09871](https://arxiv.org/abs/2412.09871)
- Teorema de recursão de Kleene: S. C. Kleene, *Introduction to Metamathematics* (1952)
- Teorema de Löb: M. H. Löb, "Solution of a problem of Leon Henkin", *Journal of Symbolic Logic* 20 (1955)
- `json.dumps` e os separadores padrão: [docs.python.org/3/library/json.html](https://docs.python.org/3/library/json.html)
