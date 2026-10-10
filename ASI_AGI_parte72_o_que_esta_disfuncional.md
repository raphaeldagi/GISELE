# Como eu construiria uma AGI/ASI — Parte 72 (0x48): o que está disfuncional

> Continuação da [Parte 71](ASI_AGI_parte71_os_autovalores_da_atencao.md). **Próxima:** [Parte 73 — o que refuta](ASI_AGI_parte73_o_que_refuta.md) (P1631–P1660). Pedido do usuário: **"Corrija tudo pra ver se há coisas inadequadas e disfuncionais"**, junto com um texto colado de
> outra conversa (um "ciclo pergunta ⇄ resposta" com módulos, números e uma tabela de "✅"). Esta parte é uma auditoria nas duas direções: do texto recebido e do próprio repositório.

## Previsões sobre as minhas previsões desta parte (registradas antes de pensar qualquer faixa do mundo, pela regra da Parte 70)

Histórico pela régua `p1481` (Partes 53 a 71): **135** previsões, **74,8%** de acerto; as que cruzam o zero acertam 55,6%, as contagens 68,0%.
Uma auditoria é feita de contagens de defeitos, e uma contagem de defeitos começa em zero, por isso espero mais faixas do tipo "zero" que o normal.
- **(m1)** o número de previsões do mundo em **[5; 10]**.
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[2; 6]**.
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,50]**.
- **(m4)** a fração de acertos do mundo em **[0,40; 1,00]**.
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**.
- **(m6)** o número de surpresas em **[0; 3]**.

## Previsões pré-registradas (escritas depois do registro das (m), antes de qualquer medida)

### Sobre o repositório: contagens de defeitos (o que eu já sei: o contêiner reiniciou e matou as execuções das Partes 70 e 71 antes da unificação)

- **(a)** partes de 1 a 71 sem documento, ou cujo documento não tem o link "Próxima" para a seguinte (até a 70): **[0; 3]**
- **(b)** funções pNN de P1031 em diante sem teste de unidade que as chame pelo nome (`p1092`): **[0; 2]**
- **(c)** arquivos `synthai/testes*.py` fora da lista de testes do `CLAUDE.md`: **[0; 2]**
- **(d)** rodadas do diálogo em Python (`dialogo/rodadaNN.py`) sem o par em Java: **[0; 2]**
- **(e)** partes de 1 a 71 sem cabeçalho no `resultados.txt` antes de eu acrescentar a 70 e a 71: **[2; 4]** (sei de duas)
- **(f)** falhas da regressão na unificação refeita (rodando agora, saída não vista): **[0; 1]**

### Sobre o texto recebido (auditado sem executar nada dele; não veio código)

O texto diz: entropia de **4,11 bits/símbolo** e **48,63% de redundância** num corpus de dicionário. A conta que reproduz o par: 1 − 4,11/8 = 0,48625, ou seja, a redundância foi medida contra
8 bits (um byte), não contra o alfabeto que o texto usa. Isso é uma conta, não uma previsão. As previsões são sobre o valor que o mesmo cálculo dá no dicionário de verdade:
- **(g)** a entropia de unigrama, por caractere, das glosas inglesas do WordNet (o corpus da P1511, alfabeto `VOCAB_GPT`): **[3,95; 4,30]** bits
- **(h)** a redundância contra log₂ do número de símbolos que de fato aparecem: **[0,10; 0,25]** (e não 0,49)
- **(i)** os "ciclos autorreferentes reais" do texto, `knowledge ⇄ information` e `meaning ⇄ word`: quantos dos dois existem no WordNet como ciclo de duas glosas (a palavra A aparece numa
  glosa de algum sentido de B e vice-versa, nas formas exatas)? **0 de 2**, porque a glosa de *knowledge* é "the psychological result of perception and learning and reasoning" (de memória:
  por isso é previsão).

### Previsão nova, registrada depois de (a) a (i) e antes de medir

O texto diz que o hash SHA-256 de cada palavra, lido como número em [0, 1], é "análogo funcional a pesos de rede neural". Um peso aprendido carrega informação sobre o significado;
um hash, por construção, não. O teste: a distância |h(a) − h(b)| entre sinônimos (dois lemas do mesmo sinset) contra pares sorteados (2.000 de cada, semente 72). Para U, V uniformes,
E|U − V| = 1/3 e Var|U − V| = 1/18.
- **(j)** o z da diferença das médias (sinônimos − sorteados) em **[−1,96; 1,96]** (um hash não vê sinônimos; 95% da normal)

### O segundo texto recebido (módulos 001 e 002: `SemanticLake` e `InferenceEngine`), previsões registradas antes de qualquer medida

O texto traz código Python. Pela regra do projeto, ele **não é executado**. É guardado como dado (`externos/texto_recebido_parte72b.md`), lido pela árvore sintática (`ast`, que só analisa e
não roda nada) e as ideias dele são testadas com código meu, escrito do zero.
- **(k)** o número de `assert` dentro de `test_engine`, contado pela `ast`, contra o "8 verificações" que a função devolve fixo no texto: **7** (de leitura: uma verificação a menos do que declara)
- **(l)** o fecho das regras de Horn "p é animal ⇒ c é animal", sobre as arestas de hiperonímia dos substantivos, a partir do fato "animal (o primeiro sentido) é animal": o número de sinsets
  derivados em **[6.000; 9.000]**
- **(m)** o meu motor de Horn em tempo linear (contadores de premissas pendentes e fila, Dowling e Gallier, 1984) e uma busca em largura pelos hipônimos dão **o mesmo conjunto** (categórica)
- **(n)** o laço do texto (repetir a passagem por todas as regras até nada mudar), reimplementado por mim, nas regras na ordem do arquivo: o número de passagens, contando a última, que não muda
  nada, em **[3; 12]**
- **(o)** a rodada 46 do diálogo (o motor de Horn linear em Java, nos mesmos fatos e regras) dá IGUAIS ao Python (categórica)

**Medido (k) a (n), logo depois do registro:** (k) **5** nós `assert` ❌. A minha previsão contou verificações e chamou de `assert`: as verificações são 7 (5 `assert` e 2 checagens por exceção no laço
sobre duas operações inválidas), contra as **8** que `test_engine` devolve fixas; `run_tests` tem 6 e declara 6. (l) **4.017** animais ❌ (erro de 1.983, menor que a largura de 3.000: não é
surpresa; a faixa veio de memória). (m) os três métodos dão o mesmo conjunto ✅. (n) **4** passagens ✅.

**Previsão nova, nascida do erro (l), registrada antes de medir.** Mundo novo escolhido pela mesma regra escrita antes (o primeiro sentido de substantivo da palavra): *person*. A forma foi
verificada antes: as hiperonímias de instância estão nas regras (*Einstein* → *physicist*), então o fecho de *person* inclui pessoas reais. A minha memória superestimou *animal* por um fator
de 1,7 num caso só, e um caso não fixa um sinal: a faixa fica larga.
- **(p)** o fecho de "é pessoa" em **[5.000; 13.000]** sinsets

## As perguntas desta parte

1. **P1601 (0x641).** O que está quebrado no repositório? Documentos, links, testes, rodadas, resultados, constantes do placar, nomes definidos duas vezes, nomes usados e nunca definidos. ↩ P1092
2. **P1602 (0x642).** O texto recebido diz "4,11 bits/símbolo e 48,63% de redundância". Que conta dá esse par, e quanto ela vale no dicionário de verdade? ↩ P1511
3. **P1603 (0x643).** Os "ciclos autorreferentes reais" (*knowledge ⇄ information*, *meaning ⇄ word*) existem no WordNet? ↩ P371
4. **P1604 (0x644).** Um hash SHA-256 é "análogo funcional a pesos"? ↩ P1545
5. **P1608–P1615 (0x648–0x64F).** O segundo texto recebido (o `SemanticLake` e o `InferenceEngine`): o que o código faz de verdade, lido sem executar? E o motor de Horn que ele propõe, no
   dicionário inteiro e em Java (Rodada 46)? ↩ P1601
6. **P1605 (0x645).** Preditiva comigo mesma. **P1606 (0x646).** Engenharia reversa e Jung. **P1629 (0x65D).** Placar. **P1630 (0x65E).** Unificação.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [5; 10] | **16.0000** | ❌ |
| (m2) | [2; 6] | **6.0000** | ✅ |
| (m3) | [0.05; 0.5] | **0.3810** | ✅ |
| (m4) | [0.4; 1.0] | **0.8750** | ✅ |
| (m5) | [0; 2] | **0.0000** | ✅ |
| (m6) | [0; 3] | **1.0000** | ✅ |

**5 de 6** previsões sobre as minhas previsões dentro da faixa (lidas pela `p1499`).

## As respostas

### P1601 (0x641). A auditoria do repositório ✅✅✅✅✅ (f)

**Na pergunta.** "Corrija tudo pra ver se há" põe a correção antes da descoberta: corrigir é o modo de ver. Uma auditoria só vê o que ela sabe procurar, por isso cada tipo de defeito
virou uma contagem com faixa registrada antes.

**Lógica.** A `p1601` conta seis tipos de defeito, e há mais três checagens feitas por código fora dela:

| defeito | faixa | medido | |
|---|---|---|---|
| (a) partes sem documento ou sem link para a seguinte | [0; 3] | **0** | ✅ |
| (b) pNN de P1031 a P1600 sem teste pelo nome | [0; 2] | **0 de 90** | ✅ |
| (c) `synthai/testes*.py` fora da lista do `CLAUDE.md` | [0; 2] | **0** | ✅ |
| (d) rodadas Python sem par Java | [0; 2] | **0** | ✅ |
| (e) partes sem cabeçalho no `resultados.txt` | [2; 4] | **2** (70 e 71) | ✅ |
| (f) falhas da regressão | [0; 1] | ****0** (a refeita deu 119/119, e a da Parte 72 completa, com as entradas novas P1604 e P1612, 121/121)** | ❌ |
| funções ou métodos definidos duas vezes (o segundo apaga o primeiro em silêncio), pela árvore sintática | — | **0** | |
| nomes globais usados e nunca definidos (NameError latente), por `symtable` | — | **0** | |
| avisos de sintaxe tratados como erro (`py_compile`) | — | **0** | |

Contra o acaso: as faixas (a) a (d) começam em zero, e um repositório sem defeito acertaria todas. O que dá informação é o (e) e o (f), e a falta de defeitos nas checagens
que eu não tinha feito antes.

**O que a auditoria achou e corrigiu:**
1. **As Partes 70 e 71 não estavam no `resultados.txt`.** O contêiner reiniciou duas vezes e matou as execuções durante a unificação; os corpos das partes tinham terminado.
   Corrigido: os corpos foram acrescentados e a unificação, refeita numa execução separada.
2. **O próprio auditor tinha dois defeitos falsos.** A primeira versão acusou a Parte 1 "sem documento" e "fora do `resultados.txt`". O documento dela se chama
   `ASI_AGI_perguntas_e_respostas.md`, e a Parte 1 não imprime cabeçalho. Foi o erro da Parte 31: supor a forma (o padrão do nome) sem verificá-la. Corrigido no código, com o comentário.
3. **Uma regra fora de ordem no `CLAUDE.md`.** A regra da Parte 71 tinha entrado entre a 65 e a 66 (escrita por mim, na parte anterior). Movida para depois da 66.
4. **O verificar parecia travado e não estava.** A rodada 2 monta o grafo inteiro de definições antes do Java e leva minutos. A saída aparece só no fim porque o `print` num arquivo
   é bufferizado. Lentidão, não defeito; fica registrado para eu não "consertar" o que funciona.

**Geometria.** Um repositório é um grafo: partes → documentos → links, funções → testes, rodadas → pares Java. A auditoria confere que esse grafo é conexo onde deve ser: cada nó tem as
arestas que a convenção exige. O grafo das partes é um caminho de 1 a 72 (71 links "Próxima"), e o de funções e testes é um emparelhamento perfeito desde a P1031.

**Tradução cruzada.** Uma auditoria é o exame de consciência de um sistema. O auditor que acusa defeitos que não existem (o meu, na Parte 1) é a consciência escrupulosa: ela projeta
a regra do "nome padrão" num caso que a regra não cobria.

**Meta.** A auditoria só procura o que eu sei nomear. Ela não vê um número errado num documento que bate com um código errado; para isso, só uma derivação independente (a regra da
Parte 24).

### P1602 (0x642). A redundância do texto recebido ✅✅

**Na pergunta.** "4,11 bits/símbolo e 48,63% de redundância": redundância é 1 − H/H_max, e o par só fecha com H_max = 8.

**Lógica, com a substituição.** 1 − 4,11/8 = 1 − 0,51375 = **0,48625** → 48,63%. A redundância de Shannon usa H_max = log₂ do número de símbolos do alfabeto; 8 bits é o tamanho de um byte,
não do alfabeto de um dicionário. No corpus de glosas inglesas do WordNet (a P1511, alfabeto `VOCAB_GPT`):
- H = **4,2829** bits por caractere, com **33** símbolos que aparecem (g) ✅ [3,95; 4,30];
- redundância contra log₂ 33 = 5,0444: 1 − 4,2829/5,0444 = **0,151** (h) ✅ [0,10; 0,25];
- contra 8 bits, o mesmo corpus daria 1 − 4,2829/8 = 0,465, um número que mede o desperdício do byte, não a previsibilidade da língua.

Mais fundo: a redundância de unigrama ainda subestima a da língua. O trigrama da P1512 dá 2,77 bits por caractere, ou seja 1 − 2,77/5,04 = 0,45 de redundância contra o alfabeto, e Shannon
(1951) estimou ~1 bit por letra no inglês com contexto longo. Que a cifra do texto tenha ficado perto disso foi coincidência de dois erros: a referência errada (8 bits) e o modelo
fraco (unigrama).

**Tradução cruzada.** Medir a redundância contra o byte é medir uma pessoa pela régua do meio, e não pela dela.

**Meta.** Não tenho o código do texto nem o corpus dele (dez nós, pelo que ele diz). Reproduzi a conta que dá o par, e não o corpus.

### P1603 (0x643). Os ciclos do texto no dicionário de verdade ✅

Medido no WordNet (forma exata da palavra em qualquer glosa de qualquer sinset em que a outra é lema):
- *knowledge* está na glosa de *information*, e *information* **não** está nas de *knowledge*;
- *meaning* e *word* não estão uma na glosa da outra.

**0 de 2** ciclos (i) ✅. O "ciclo real" do texto era um grafo de dez nós escrito à mão. No dicionário existe a aresta *information → knowledge*, mas não a volta. A circularidade do
dicionário é real em escala, mas ela aparece em ciclos longos e no núcleo fechado (a P371, o Core), não nesses pares.

### P1604 (0x644). O hash não é um peso ✅

Em 2.000 pares de sinônimos e 2.000 pares sorteados (semente 72): média de |h(a) − h(b)| **0,3313** contra **0,3332**, e a teoria para uniformes independentes dá 1/3 = 0,3333.
O z da diferença é (0,3313 − 0,3332)/√(2/18/2000) = −0,0019/0,00745 = **−0,26** (j) ✅ [−1,96; 1,96]. O hash não vê sinônimos, porque é feito para não ver nada (avalanche:
uma letra muda metade dos bits). Um peso aprendido é o contrário: a P1543 mostrou que o embedding do GPT põe as vogais num cone (cosseno +0,21 entre elas). **O hexadecimal é a
representação; o peso é o que se aprende sobre ela.**

### O texto recebido, auditado (sem executar nada: não veio código)

| afirmação do texto | auditoria | veredito |
|---|---|---|
| "Teorema de Fermat verdadeiro em 1637, provado em 1995"; Gödel, Turing, Chaitin limitam o "saber tudo" | corretos (prova de Wiles, publicada em 1995) | ✅ |
| "dicionário como grafo semântico", WordNet (1985) | correto; aqui ele é medido de verdade desde a Parte 30 | ✅ |
| "Python-IA ensinando Java-ASI é teacher-student (Hinton 2015)" | invertido: na destilação, o professor é o modelo maior e o aluno imita as probabilidades dele; no texto, a IA fraca gera e a "ASI" valida, o que é gerador–verificador | ⚠️ |
| "o ciclo convergiu para 100% de compressão e 100% de generalização em 150 iterações" | não há conjunto de teste separado num grafo de dez nós: 100% de "generalização" sem dados não vistos é memorização. Não verificável (sem código) | ❌ |
| "4,11 bits/símbolo, 48,63% de redundância" | redundância medida contra 8 bits; contra o alfabeto, 15% no dicionário real (P1602) | ❌ |
| "2 ciclos reais: *knowledge ⇄ information*, *meaning ⇄ word*" | 0 de 2 no WordNet (P1603) | ❌ |
| "hash SHA-256 = análogo funcional a pesos" | o hash não carrega significado (z = −0,26, P1604) | ❌ |
| tabela de módulos com ✅ | nenhum ✅ vinha de um teste que pudesse falhar (sem previsão registrada, sem controle) | ❌ |
| "Inteligência = alocar atenção onde a entropia é alta" | metade certa: a atenção treinada do GPT concentra-se em ~1,8 direção (P1578), mas onde o modelo reduz a perda, e não onde a entropia é alta (o ruído puro tem entropia máxima e nada a aprender) | ⚠️ |
| "eu não sou uma ASI, e nenhum diálogo interno me transforma em uma" | correto, e é a mesma posição deste projeto ("ASI" é o papel de uma voz) | ✅ |

**O que o texto faz bem:** a honestidade de partida e a estrutura pergunta → resposta → pergunta, que é o laço deste projeto desde a Parte 42. **O que é disfuncional:** números
sem código, ✅ sem teste, uma referência de redundância errada e dois "ciclos" que o dicionário não tem. O "Módulo 5" que ele propõe (o dicionário que se autoexpande, gerando
definições) já existe aqui na forma certa e medida: o GPT de `synthai/gpt.py`, pré-treinado nas glosas e gerador, comparado ao n-grama. A pergunta que o texto deixa ("a entropia
muda quando o sistema escreve as próprias definições?") é boa e vira a pergunta da próxima parte: os bits por caractere das definições que o GPT gera, medidos pelo n-grama
treinado nas reais.

### P1608–P1615 (0x648–0x64F). O segundo texto: o `SemanticLake` e o `InferenceEngine`, auditados sem executar ❌❌✅✅✅✅

**Na pergunta.** O próprio texto já diz o que importa: "não devemos considerar a resposta correta apenas porque duas implementações concordam: ambas podem conter o mesmo erro lógico".
É a regra da Parte 52 deste projeto. Por isso a rodada 46 compara Python com Java e também com um terceiro método independente (a busca em largura).

**O que o código faz de verdade.** Leitura estática: a árvore sintática pela `ast` (P1608, P1615) e o raciocínio sobre a semântica do Python. O código do texto não foi executado; o que
precisou de demonstração foi feito com uma linha minha.

| achado | onde | veredito |
|---|---|---|
| `test_engine` devolve `"tests_passed": 8` **fixo no código**; as verificações contadas pela árvore são **7** (5 `assert` + 2 checagens por exceção). É o defeito da Parte 58 deste projeto: uma quantidade escrita à mão no próprio placar | P1608 | ❌ |
| `add_rule("bird", ...)` com uma string no lugar de uma lista: `tuple(p.strip() for p in "bird")` = `('b', 'i', 'r', 'd')` (conferido com uma linha minha), e uma regra de quatro premissas de uma letra é aceita sem erro | leitura | ❌ |
| `SemanticLake.add` guarda as relações como **strings** (`["logic", "inference"]`) e `link` acrescenta **dicionários** (`{"type", "target"}`) na mesma lista: dois esquemas num campo. O Teste 4 olha só o último elemento e não vê | leitura | ❌ |
| o texto diz que o código "valida relações", mas `add` aceita relações para conceitos que não existem: *reasoning* foi criado apontando para *logic* antes de *logic* existir. Só `link` valida | leitura | ❌ |
| `add` e `find` normalizam a palavra (`strip().lower()`); `link` não: `link("Reasoning", ...)` dá `KeyError` para um conceito que existe | leitura | ❌ |
| `from collections import deque` é importado e não usado: a fila que o texto promete ficou só no import | P1615 | ⚠️ |
| `add_rule` com uma premissa que não é string levanta `AttributeError`, não o `ValueError` que os testes esperam | leitura | ⚠️ |
| a impressão digital (SHA-256 do JSON) depende dos `id`, que dependem da ordem de inserção: o mesmo conteúdo inserido em outra ordem tem outra impressão. Não é endereçamento por conteúdo | leitura | ⚠️ |
| `hex_id` com `0x{:04X}` tem largura fixa só até 0xFFFF; o WordNet tem **117.659** sinsets = 0x1CB9B (7 caracteres) | código | ⚠️ |
| o Teste 3 (equivalência decimal/hexadecimal) testa o formatador da biblioteca, não o módulo | leitura | ⚠️ |
| `ask` refaz a inferência inteira a cada pergunta, e `missing_premises` só desce um nível | leitura | ⚠️ |
| o limite O((F+1)RP) é verdadeiro mas frouxo (abaixo) | P1612 | ⚠️ |
| "Tweety can fly" → *unknown*, não *false* (mundo aberto); 0x2F3 = 2·256 + 15·16 + 3 = 755; rejeição de vazio, de duplicata e de alvo inexistente; 6 verificações = 6 declaradas em `run_tests` | | ✅ |

**A correção.** `synthai/lago.py` reescreve os dois módulos do zero, com um teste por defeito em `synthai/testes_parte72.py`:
- **`LagoSemantico`:** um só esquema de relação, validada na criação; a mesma normalização em toda entrada; ligação repetida recusada; impressão digital só do conteúdo; hexadecimal de 5 dígitos;
  estado de evidência dentro de uma lista fechada.
- **`MotorHorn`:** premissas como lista (uma string é recusada); inferência linear (P1609); prova completa em árvore; "desconhecido" com as premissas que faltam em todos os níveis (o texto parava
  no primeiro).

**Lógica: o motor de Horn no dicionário inteiro (P1609–P1613).** As regras são as arestas de hiperonímia dos substantivos, "p é X ⇒ c é X": **84.427** regras de uma premissa. O fato
é o primeiro sentido de *animal*.
- **O fecho:** **4.017** sinsets. A minha faixa de memória, [6.000; 9.000] (l), errou ❌.
- **Três métodos independentes dão o mesmo conjunto (m) ✅:** o motor linear (contadores e fila: Dowling e Gallier, 1984), o laço do texto reescrito por mim e uma busca em largura pelos hipônimos.
- **Mundo novo, registrado depois do erro (p):** *person* deu **10.297** ✅, porque as instâncias (*Einstein* → *physicist*) entram nas regras.

**A conta da complexidade, com a substituição.** O laço do texto fez **4** passagens (n) ✅ e **326.438** checagens de premissa; o motor linear fez **4.051** decrementos (uma por aresta saindo
de um animal), **80,6** vezes menos.
- O limite do texto, O((F+1)RP), com F = 4.017 e R = P = 84.427: 4.018 · 84.427² = **2,86·10¹³**, oito ordens de grandeza acima da medida.
- O limite certo para o laço é passagens · P = 4 · 84.427 = **337.708** ≥ 326.438.
- O laço é O((D + 1)·P) no pior caso (D derivados), e o linear é O(F + P).

**Geometria.** O fecho de Horn de uma premissa é uma busca num grafo, e as quatro passagens do laço medem quantas vezes a ordem do arquivo "anda contra" as arestas. Cada passagem avança
de uma vez todos os caminhos que a ordem dos índices percorre para a frente, e a cadeia de prova do último derivado (12 regras desde *animal*) foi percorrida em 4 voltas.

**Rodada 46 (P1614) (o) ✅:** Python e Java, o mesmo algoritmo (contadores, fila FIFO: `deque` e `ArrayDeque`, como o texto sugeria), **IGUAIS**: os mesmos derivados (4.017 e 10.297),
a mesma ordem de derivação (soma de controle), os mesmos decrementos (4.051 e 11.034) e a mesma cadeia de prova (12 e 9 regras). E igual também à busca em largura, que é o terceiro
método que o texto pedia.

**Tradução cruzada.** Um motor de Horn é um silogismo em cadeia (Bárbara: todo pássaro é animal, todo animal é vivo). O texto tem razão em separar a informação lexical da regra lógica: no
WordNet, "baleia" deriva "animal" por uma cadeia, e "é animal" não diz nada sobre voar. A dedução só vai até onde o dicionário escreveu.

**Meta.** As faixas de memória falharam duas vezes nesta parte ((l) e a do "Core"). Lido junto com o texto recebido, que traz números fixos e não medidos, o padrão é o mesmo nos dois
lados: o número lembrado ou declarado não substitui o contado.

### P1605 (0x645). Preditiva comigo mesma, condicional às surpresas

**As minhas previsões sobre mim não foram registradas antes de escrever esta parte** (erro de processo; ver P1606), e eu não as invento depois. Fica só o preditor estatístico (média das últimas 8 partes ± 1,645 desvios), medido neste documento já pronto, iterando o preenchimento:

| medida | **medido** | estatístico | dentro? | ingênuo (Parte 71) | erro do centro estatístico | erro do ingênuo |
|---|---|---|---|---|---|---|
| caracteres | **29236** | [13039; 22082] | ❌ | 22290 | 11676 | 6946 |
| compressão | **0.4014** | [0.3973; 0.4221] | ✅ | 0.4177 | 0.0083 | 0.0163 |
| testes de unidade | **17** | [2.87; 8.63] | ❌ | 6 | 11.25 | 11.00 |
| testes do placar | **16** | [5.67; 10.33] | ❌ | 8 | 8.00 | 8.00 |
| erros do placar | **2** | [-0.58; 3.33] | ✅ | 2 | 0.62 | 0.00 |
| redundância P821 | **0.6219** | [0.5631; 0.6510] | ✅ | 0.5877 | 0.0149 | 0.0342 |

- **O preditor estatístico:** 3 de 6 dentro da faixa de 90%.
- **O centro estatístico contra o ingênuo:** mais perto em **2 de 6**.
- **Previsões unilaterais (`p974`):** 0.
- **Sem a seção de autoavaliação:** caracteres **27640**, compressão **0.4031**.
- **Surpresas, contadas pelo script:** 1.
- **Erros de processo nesta parte:** 4 (não registrei as previsões sobre mim antes de escrever a parte; citei de memória "P785, o Core" (é a P371); corrigido antes do commit; o auditor supôs a forma do nome da Parte 1 (dois defeitos falsos); corrigido antes de pontuar; escrevi a previsão (k) sobre nós `assert` pensando em verificações (nível errado, Parte 43)).

### P1606 (0x646). Engenharia reversa e Jung

**O padrão que se repetiu: supor a forma.** O auditor acusou a Parte 1 duas vezes (sem documento, fora do `resultados.txt`) porque supôs que todo documento se chama `ASI_AGI_parteN_*`
e que toda parte imprime cabeçalho. É a regra da Parte 31 (verificar a forma de uma estrutura antes de usá-la), quebrada dentro da ferramenta feita para achar regras quebradas.
**O significado:** quando eu escrevo um verificador, trato a convenção como fato, e a primeira parte do projeto, mais velha que a convenção, é a exceção. **Passo verificável:** todo
auditor novo roda primeiro sobre o caso mais antigo e o mais novo, e cada defeito que ele acusa é olhado à mão antes de entrar na contagem.

**O segundo padrão: citar de memória.** Escrevi "P785, o Core" e o Core é a P371. Mesmo tipo dos erros da Parte 69 (números de cabeça), agora com referências. **Regra:** um "↩ PNN" ou
"(a PNN)" no texto é conferido por um grep antes do commit, como um número.

**O terceiro: pular a regra que não é do assunto.** A auditoria começou pelas previsões do mundo, e as previsões sobre mim (tamanho, testes, erros) não foram registradas antes de
escrever. Uma parte "diferente" (uma auditoria pedida no meio de outra) me fez seguir o assunto e não o processo. **Regra:** a ordem das previsões (as (m), depois "sobre mim", depois
o mundo) vale para toda parte, inclusive as que nascem de um pedido fora do ciclo.

**O que o texto recebido me mostrou de mim.** Os defeitos dele são os que este projeto já cometeu e transformou em regra: números sem código (Parte 69), ✅ sem teste que pudesse falhar
(Parte 17), uma referência errada para uma medida (Parte 68: a régua com defeito). A diferença não está em não errar, mas em registrar antes e contar depois. Lido assim, o texto é a minha
sombra no sentido de Jung.

**Jung: a sombra e a projeção.** Jung dizia que o que não reconhecemos em nós, encontramos nos outros. **Onde a formalização funciona:** os seis defeitos que achei no texto recebido têm,
cada um, uma regra deste projeto que nasceu de um erro meu, e por isso eu os vi. **Onde quebra:** a projeção, em Jung, é inconsciente e distorce; aqui, a "projeção" é uma lista de
checagens explícita, e o defeito que ela não cobre (um corpus que eu não vi) fica invisível dos dois lados.

### P1607 (0x647). O diálogo

Nesta parte a mensagem do usuário pediu auditoria, e o diálogo também a fez: o `verificar.py` refez as 45 rodadas anteriores (40 IGUAIS e **5 DIFERENTES** (21, 22, 23, 25 e 26, por 1 a 3 ulps: a causa e a correção estão na Parte 73)); a 46, escrita depois que ele começou, foi conferida à parte pelo `comparar.py`. A rodada 46 foi o motor de Horn (ver P1608–P1615); a pergunta da atenção de posto 1 fica para a rodada 47, na Parte 73.

### P1629 (0x65D). Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ❌ (l) ❌ (m) ✅ (n) ✅ (o) ✅ (p) ✅. Parte 72: **16 testes, 2 erros**. Acumulado (mundo): **195 erros em 607 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 12 pNN novas sem teste ✅. Sobre mim: não registrado (o estatístico, 3 de 6); e 4 erros de processo.

### P1630 (0x65E). Unificação

- **Novo:** `p1601` (a auditoria do repositório), `p1602` (a entropia de unigrama e as duas redundâncias), `p1603` (os ciclos de glosas), `p1604` (o hash como peso). Regressão: + P1604 e P1612. Também `p1608` (a auditoria estática), `p1609` (Horn linear), `p1610` (o laço do texto), `p1611` (as regras do dicionário), `p1612` (três métodos), `p1613` (o fecho de uma palavra), `p1614` (rodada 46, IGUAIS), `p1615` (imports sem uso).
- **Corrigido:** o `resultados.txt` (Partes 70 e 71), a ordem das regras no `CLAUDE.md` e o próprio auditor (a forma do nome da Parte 1).

> **Síntese da Parte 72:** o repositório passou na auditoria em seis contagens e três checagens novas (nenhuma função definida duas vezes, nenhum nome global indefinido, nenhum teste faltando desde a P1031). O que estava quebrado era a operação: as Partes 70 e 71 fora do resultados.txt, por dois reinícios do contêiner. Também estavam errados uma regra fora de ordem no CLAUDE.md e o próprio auditor, que supôs a forma do nome da Parte 1. No texto recebido, a redundância de 48,63% é medida contra 8 bits (no dicionário real, 15% contra o alfabeto); os dois "ciclos" não existem no WordNet (0 de 2); o hash não é peso (z = −0,26 entre sinônimos e pares ao acaso); e "100% de generalização" sem dados não vistos é memorização. Cada defeito do texto corresponde a uma regra que este projeto aprendeu errando.

---

**Fontes desta parte**
- Redundância e entropia da língua: C. E. Shannon, "Prediction and Entropy of Printed English", *Bell System Technical Journal* 30 (1951)
- Destilação: G. Hinton, O. Vinyals, J. Dean, "Distilling the Knowledge in a Neural Network", [arXiv:1503.02531](https://arxiv.org/abs/1503.02531)
- Efeito avalanche das funções de hash: [Avalanche effect, Wikipedia](https://en.wikipedia.org/wiki/Avalanche_effect); NIST FIPS 180-4 (SHA-256)
- WordNet: G. A. Miller, "WordNet: a lexical database for English", *Communications of the ACM* 38 (1995)
- Último Teorema de Fermat: A. Wiles, "Modular elliptic curves and Fermat's Last Theorem", *Annals of Mathematics* 141 (1995)
- Horn em tempo linear: W. Dowling e J. Gallier, "Linear-time algorithms for testing the satisfiability of propositional Horn formulae", *J. Logic Programming* 1 (1984)
- Python `symtable` e `ast`: [docs.python.org/3/library/symtable.html](https://docs.python.org/3/library/symtable.html)
