# Como eu construiria uma AGI/ASI — Parte 72 (0x48): o que está disfuncional

> Continuação da [Parte 71](ASI_AGI_parte71_os_autovalores_da_atencao.md). Pedido do usuário: **"Corrija tudo pra ver se há coisas inadequadas e disfuncionais"**, junto com um texto colado de
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
