# Parte 116 — O NEXUS-RAPHAEL "v2": dez camadas no nome, o que o código faz de fato (0x74)

↩ Parte 109 (o NEXUS v0.1.0 colado, synthai/nexus.py) · ↩ Parte 111 (o verificador lê capacidades, não nomes) · ↩ Parte 75 (um verificador só vale com um caso de controle de cada lado) · ↩ Parte 88 (comparar o texto com o SEU PRÓPRIO código)

> **Recebido sem pedido escrito:** um texto colado que abre com "Vou implementar o NEXUS–RAPHAEL como uma arquitetura experimental consolidada em Python, … real, mensurável e auditável". Segue um código de "10 camadas" (ingestão, linguística, numérica, geométrica, inferência, criatividade, …, metacognição, auditoria e memória). Ele vem **truncado em dois pontos**: no meio de `divergent_exploration` ("Vou continuar o código a partir de onde parou:") e no fim de `evaluate_and_decide`.
>
> **A leitura escolhida (regras das Partes 83, 109 e 111, escrita ANTES de medir).** O pedido implícito é o do próprio texto: implementar o que ele descreve, de forma "mensurável e auditável". Faço como na Parte 109:
> - O texto fica **arquivado** intacto em `externos/nexus_raphael/nexus_raphael_v2_colado.txt` (`.txt`: não fecha como Python e não é importável).
> - É auditado pela **árvore sintática**, sem executar.
> - O que serve vira `synthai/nexus_v2.py`, escrito do zero, offline e só com a biblioteca padrão.
>   - O **dicionário** sai da API `dictionaryapi.dev`, que é rede (12ª recusa da família), e passa a ser o WordNet local.
>   - A **memória SQLite** sai do disco e vai para `':memory:'`.
> - Cada afirmação de mecanismo do texto é medida contra o **próprio código dele** (Parte 88): as funções puras são transcritas como `recebido_*` e medidas ao lado da versão corrigida.
>
> **Antes do registro (condições, não resultados).**
> - Os dados são as 77.340 palavras a-z do WordNet (Parte 111).
> - A comparação com a cópia guardada da Parte 109 (regra da Parte 50) e a contagem por AST ficam para depois do registro.
> - Não as previ, porque já li os dois textos: o que eu leio não vira previsão (regra da Parte 60).

## As perguntas desta parte

1. **P2921 (0xB69).** O texto é o mesmo da Parte 109, reenviado, ou um texto novo? E o que a árvore sintática acha nele (rede, disco, nomes usados e nunca definidos)? ↩ P2711
2. **P2922 (0xB6A).** A "semelhança semântica" por hash mede significado? Os sinônimos ficam mais perto que os pares ao acaso? ↩ P2532
3. **P2923 (0xB6B).** O `random.seed` dentro de `word_to_vector` reinicia o gerador GLOBAL. O que isso faz com o resto do agente (a exploração ε-gulosa, a criatividade)? ↩ P2922
4. **P2924 (0xB6C).** As codificações numéricas da camada 3 (posicional, alfanumérica, numerológica) são injetivas? Quantas palavras colidem, e por qual mecanismo? ↩ P2894
5. **P2925 (0xB6D).** A avaliação metacognitiva ("melhoria média > 0,1 confirma") decide o que sob a hipótese NULA? E a confiança por coeficiente de variação? ↩ P2741
6. **P2926 (0xB6E).** O intervalo de confiança recebido cobre a média com a confiança pedida? ↩ P2925
7. **P2927 (0xB6F).** A auditoria de entrada da camada 10 pode reprovar alguma coisa? ↩ P2711
8. **P2928 (0xB70).** O vetor corrigido (gerador local) é o mesmo vetor do texto? ↩ P2923
9. **P2929 (0xB71).** A avaliação pareada que substitui a do texto acrescenta fronteira entre Python e Java? (rodada 83) ↩ P2897

## Previsões pré-registradas (ANTES de medir — este commit)

**As fixtures (todas em `synthai/nexus_v2.py`, neste commit).**
- **Pares:** `pares_aleatorios(lemas, 2000)` (semente 1161) e `pares_de_sinonimos(2000)` (semente 1160, dois lemas a-z do mesmo sinset).
- **Vetores:** dimensão 10.
- **Nula:** `avaliacao_nula()`, 20.000 tentativas, valor e linha de base iid N(10, 2), 1 experimento.
- **Nula pareada:** `avaliacao_nula_pareada()`, n = 5, t crítico unilateral de 95% com 4 graus de liberdade.
- **Cobertura:** `cobertura(f, c)`, 20.000 amostras N(0, 1) de n = 30.
- **Contaminação:** `contaminacao("synthai", 1000)`.

**A semelhança por hash (P2922).** Os vetores são gaussianos N(0, 1)¹⁰ sorteados a partir do md5 da palavra, então o cosseno entre duas palavras diferentes tem média 0 e variância 1/d. Para gaussianos isso é exato: E[c²] = 1/d, E[c⁴] = 3/(d(d+2)), curtose 3d/(d+2) = 2,5.
- **(a)** O desvio do cosseno sobre os 2.000 pares aleatórios. Centro 1/√10 = 0,3162. O desvio do desvio é 0,3162·√((2,5 − 1)/(4·2000)) = 0,00433, faixa ±1,645 × 0,00433 = **[0,309; 0,323]**. Forma fechada com variância conhecida (sem o fator 1,36).
- **(b)** A média do cosseno nos 2.000 pares de SINÔNIMOS menos a média nos 2.000 aleatórios. O md5 não vê significado, então o centro é 0. O desvio da diferença é √(0,1/2000 + 0,1/2000) = 0,0100, faixa **[−0,0165; 0,0165]**. Se der fora, o hash vê alguma coisa (por exemplo, sinônimos que são variantes de grafia).

**O gerador global (P2923).**
- **(c)** Depois de cada um dos 1.000 vetores da mesma palavra, a próxima chamada do gerador "global" dá quantos valores DISTINTOS? **[1; 1]**. Identidade: `seed(h)` seguido de 10 `gauss` deixa o gerador sempre no mesmo estado. Consequência: todo `random.random() < ε` depois de um vetor tem sempre o mesmo resultado, e a exploração ε-gulosa vira uma constante.
- **(d)** O mesmo com o vetor corrigido (gerador local): **[1.000; 1.000]**. Identidade: o gerador global não é tocado, e 1.000 floats de 53 bits colidem com probabilidade ≈ 10⁶/2⁵⁴ ≈ 0.

**As codificações (P2924).**
- **(e)** A posicional recebida usa A = 0, e um "a" à esquerda é um zero à esquerda. Então valor(w) = valor(w sem os "a" iniciais), e esta é a ÚNICA fonte de colisão (a base 26 com dígitos 0..25 é única a menos dos zeros à esquerda). Previsão: os pares que colidem na posicional, menos os pares que o mecanismo conta (Σ C(g, 2) nos grupos pela palavra sem os "a" iniciais): **[0; 0]**.
- **(f)** Quantos pares colidem na posicional? Mecanismo esperado: palavras "a" + palavra ("abed"/"bed", "afoot"/"foot", "awake"/"wake", "ajar"/"jar"). Das ~77 mil palavras, umas 4 a 5 mil começam com "a", e uma fração de 3% a 20% delas tem o resto no dicionário. Faixa **[150; 900]** (larga, com o mecanismo escrito: um acerto com outro mecanismo não conta como acerto do raciocínio).
- **(g)** Valores distintos da alfanumérica (soma A = 1 … Z = 26). Mecanismo: a soma vai de 1 a ~26·L, e as palavras têm ~2 a ~25 letras com média de letra ~10 a 13, então os valores enchem densamente de ~5 a ~250 e ficam ralos acima. Faixa **[200; 340]**.
- **(h)** A numerológica (soma dos códigos reduzida a um algarismo, que é a soma mod 9, com 9 no lugar do 0). O maior |fração − 1/9| entre os 9 valores. A soma de várias letras mistura bem mod 9, então os valores são quase uniformes. O desvio binomial é √(1/9 · 8/9 / 77.340) = 0,00113, e o máximo de 9 desvios fica perto de 2,5σ. Faixa **[0; 0,004]**.

**A avaliação sob a nula (P2925).** Com 1 experimento, "confirmed" ⇔ v > 1,1·b (b > 0 quase sempre). v − 1,1b ~ N(10 − 11, 4 + 1,21·4) = N(−1; 8,84), então P(confirmed) = 1 − Φ(1/√8,84) = 1 − Φ(0,3363) = 0,3683. E v − 0,9b ~ N(1; 4 + 0,81·4) = N(1; 7,24), então P(rejected) = Φ(−1/√7,24) = Φ(−0,3716) = 0,3551.
- **(i)** Fração de "confirmed" sob a nula. Desvio binomial √(0,3683·0,6317/20.000) = 0,00341, faixa **[0,3627; 0,3739]**.
- **(j)** Fração de "rejected" sob a nula. Desvio 0,00338, faixa **[0,3495; 0,3607]**. Juntas: sob a nula, o avaliador recebido decide (confirma ou rejeita) em ~72% das vezes.
- **(k)** A avaliação pareada corrigida (n = 5, t crítico unilateral de 95%) sob a mesma nula. As diferenças são normais e a t é exata, então P(confirmed) = 0,05. Desvio √(0,05·0,95/20.000) = 0,00154, faixa **[0,0475; 0,0525]**.
- **(l)** A confiança recebida para os valores [−1, −100, 50] (média −17, desvio 61): **[0,9; 0,9]**. Identidade: CV = 61/(−17) < 0,1 cai no primeiro degrau, a confiança máxima com a maior dispersão.

**O intervalo de confiança (P2926).** O recebido usa a variância populacional e z = 2,576 para QUALQUER confiança ≠ 0,95. A cobertura é P(|T₂₉| < z·√(29/30)).
- **(n)** Pedida 0,90 (vem z = 2,576): 2·F₂₉(2,5327) − 1 = 0,9830. Desvio 0,00091, faixa **[0,9815; 0,9845]**. Mais largo que o pedido: 98% em vez de 90%.
- **(o)** Pedida 0,95 (z = 1,96 com a variância populacional): 2·F₂₉(1,9271) − 1 = 0,9362. Desvio 0,00173, faixa **[0,9334; 0,9390]**. Mais estreito que o pedido.
- **(p)** O corrigido (`ic_t`, a t com n − 1) pedido a 0,90: centro 0,90, desvio √(0,09/20.000) = 0,00212, faixa **[0,8965; 0,9035]**.

**A auditoria e o vetor (P2927/P2928).**
- **(q)** A auditoria recebida com um tratador que DEVOLVE A ENTRADA sem escapar (o XSS e o caminho "../" voltam intactos): "passed" **[7; 7]**. Identidade: os dois ramos somam "passed".
- **(r)** A auditoria com oráculo (`auditoria_com_oraculo`) com o mesmo tratador: as falhas **[3; 3]**. Identidade pela definição do oráculo: a aspa da injeção SQL, o "<script" e o "..". E o controle limpo, um tratador que escapa ("<" → "&lt;", "." → "", "'" → ""), tem que dar 0 falhas: **[0; 0]** (registrado como parte de (r): as duas metades têm que valer).
- **(s)** O vetor corrigido contra o recebido, para as 2.000 primeiras palavras em ordem alfabética: o número de vetores que diferem em algum bit, **[0; 0]**. Identidade: `random.Random(int)` e `random.seed(int)` passam pelo mesmo `init_by_array` do Mersenne Twister.

**Diálogo (P2929).**
- **(t)** A avaliação pareada (rodada 83) é **IGUAL** bit a bit entre Python e Java: **[0; 0]**. Identidade: só +, −, ×, ÷, √, com as somas em laço na mesma ordem.

### Previsões sobre as previsões (m), pré-registradas (régua: P2837, leitor v4)

- **(m1)** nº de previsões do mundo em **[16; 20]** (18 agora: a até t sem m)
- **(m2)** nº de faixas que cruzam/tocam o zero em **[3; 7]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0; 0,10]**
- **(m4)** fração de acertos do mundo em **[0,70; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 3]**

### Sobre mim, pré-registrado

Os riscos estão onde não há conta fechada:
- **(f) e (g):** contagens no dicionário com o centro chutado pelo mecanismo.
- **(h):** a mistura mod 9 supõe que as palavras curtas pesam pouco.
- **(b):** se houver sinônimos que são a mesma grafia em caixas diferentes, o md5 os vê como iguais? Não: eu tiro as maiúsculas antes, e os pares do mesmo sinset são palavras diferentes.

Espero **1 a 3 erros**, em (f), (g) ou (h). As identidades (c), (d), (e), (l), (q), (r), (s), (t) só erram se eu tiver lido o código errado, e isso aconteceu duas vezes desde a Parte 109.

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->

## As respostas (quatro camadas)

### P2921 — O texto e a árvore

**Na pergunta.** "Consolidada" e "mensurável e auditável" são o que o texto promete de si. A pergunta pede o contrário: medir o que ele é.

**Lógica.**
- **Não é a Parte 109 reenviada.** Das 16 classes da v0.1.0 e das 17 desta, só **`Config`** é comum, e o Jaccard dos 5-gramas de caracteres é **0,122**. É um texto NOVO com o mesmo nome (regra da Parte 50: comparar antes de auditar de novo).
- **Não fecha como Python.** O primeiro bloco fecha até a linha **549 de 553**, e o segundo até a **541 de 549**: os dois cortes de truncamento.
- **Nomes usados e nunca definidos:** **`AdversarialLayer`, `GameState`, `RaphaelGame`** (a camada adversária, o estado do jogo e o próprio jogo). O orquestrador `NexusRaphael` constrói as três no `__init__`, então o "10 camadas consolidado" não pode ser instanciado: falta a camada 7 inteira e parte da 8.
- **Capacidades (`security_audit_ast_v2`, Parte 111):**
  - `import urllib.request` e `urllib.request.urlopen`: a rede, para a API do dicionário;
  - `sqlite3.connect`, gravando `nexus_raphael_memory.db` no diretório corrente assim que o objeto é construído;
  - `random.seed`, no gerador global (P2923).

**Meta.** A contagem por AST veio DEPOIS do registro, de propósito: eu já tinha lido o texto, e o que eu leio não vira previsão (regra da Parte 60).

### P2922 — A "semelhança semântica" por hash

**Na pergunta.** "Semântica" é a palavra a medir. O código diz o mecanismo: o md5 da palavra vira a semente de 10 gaussianas. Um hash é FEITO para que palavras parecidas deem saídas sem relação.

**Lógica.**
- **Pares aleatórios:** o desvio do cosseno nos 2.000 pares é **0,3099** ✅ (a), contra 1/√10 = 0,3162 (z = −1,47, dentro da faixa por pouco).
- **Sinônimos menos aleatórios:** a diferença das médias é **−0,0093** ✅ (b), z = −0,93. Os sinônimos do mesmo sinset ficam exatamente tão longe quanto duas palavras sorteadas.

A "semelhança semântica" é ruído com desvio 1/√d e média 0. Ela não vê significado, e não poderia ver: o vetor de uma palavra não depende de nenhuma outra. A versão útil do mesmo nome já existe no projeto: os vetores de bigramas das glosas (Parte 115) e os embeddings do GPT (Parte 69) aprendem com o contexto.

**Tradução cruzada.** É dar um nome próprio a cada pessoa e concluir parentesco pela semelhança dos nomes sorteados. A identidade (o hash) não é a relação (o significado). Para Jung, o símbolo vale pelo que ele LIGA; um sinal que não liga nada a nada é só um rótulo.

### P2923 — O gerador global reiniciado

**Lógica.**
- **Recebido:** depois de 1.000 vetores da mesma palavra, a chamada seguinte do gerador "global" deu **1** valor distinto ✅ (c). `seed(h)` seguido de 10 `gauss` deixa o estado sempre no mesmo ponto.
- **Corrigido:** **1.000** valores distintos ✅ (d), com um gerador local que não toca no de quem chama.

A consequência no agente do texto: a exploração ε-gulosa (`random.random() < ε`) e a escolha de axiomas e paradoxos (`random.choice`) usam o MESMO gerador global. Depois de qualquer cálculo de semelhança, elas viram funções determinísticas da última palavra vista, e a "exploração" deixa de explorar. A documentação do Python diz isso: as funções do módulo são métodos de UMA instância escondida de `random.Random`, e a saída é instanciar a sua própria (fonte abaixo).

**Tradução cruzada.** Um pensamento intrusivo que reinicia a atenção toda vez que uma palavra aparece. A espontaneidade (o acaso da exploração) é capturada por um gatilho, como num complexo de Jung: a mesma palavra produz sempre a mesma reação.

### P2924 — As codificações da camada 3

**Lógica.**
- **Posicional (A = 0):**
  - **446** pares de palavras colidem, e o mecanismo dos "a" iniciais conta exatamente os mesmos **446** (diferença 0 ✅ (e); 446 ∈ [150; 900] ✅ (f)). É **0,58%** das palavras.
  - O mecanismo escrito no registro confere: **310** dos 446 pares (69,5%) são palavra + "a" com um resto de 4 letras ou mais ("aback"/"back", "abase"/"base", "abate"/"bate", "abide"/"bide"). Mais 3 pares do grupo "a"/"aa"/"aaa" (valor 0), 21 de letras soltas ("aah"/"h") e 112 de restos curtos (numerais romanos como "aalii"/"lii").
  - A base 26 da Parte 115, BIJETIVA (dígitos 1..26), dá 0 colisões nas mesmas palavras: a diferença entre as duas é um dígito zero.
- **Alfanumérica (soma A = 1 … Z = 26):** **284** valores distintos para 77.340 palavras ✅ (g), cerca de 272 palavras por valor. Não é uma codificação; é um histograma.
- **Numerológica:** o maior |fração − 1/9| é **0,00152** ✅ (h), 1,35σ do binomial. Os 9 valores são uniformes porque a soma mod 9 mistura bem: a "redução numerológica" de uma palavra é um sorteio uniforme entre 9 valores, que carrega log₂ 9 = 3,17 bits da palavra e nenhuma propriedade dela.

**Tradução cruzada.** Três formas de transformar uma palavra em número, em escada de perda. A bijetiva guarda tudo; a posicional com zero perde o "a" inicial (o prefixo de negação ou de estado, "a-moral", "a-sleep"); a soma esquece a ordem e quase tudo o mais; a numerologia guarda 3 bits sem sentido. Sobre o significado, a numerologia é a mais confiante e a mais pobre.

### P2925 — A avaliação metacognitiva sob a nula

**Na pergunta.** "Confirmar" uma hipótese é afirmar que o efeito não é acaso. A pergunta certa é o que o avaliador diz quando o efeito é ZERO.

**Lógica.** Com valor e linha de base iid N(10, 2) (nenhum efeito) e 1 experimento:
- o avaliador recebido **confirma** em **37,0%** das vezes ✅ (i), z = +0,63 contra 36,83%;
- e **rejeita** em **35,2%** ✅ (j), z = −0,82.

Ele DECIDE em **72,3%** das vezes num mundo sem efeito nenhum, porque o limiar de ±10% de melhoria não olha a variância (aqui, CV = 20%). A avaliação pareada (t de Student, n = 5, 95% unilateral) confirma em **4,76%** ✅ (k): a taxa de falso positivo é a que ela declara.

A confiança recebida de [−1, −100, 50] é **0,9** ✅ (l), a MÁXIMA, para valores de sinais opostos com desvio 61 e média −17. O coeficiente de variação negativo cai no degrau "< 0,1". A correção usa |média| e o erro-padrão: s/(|média|·√n) = 2,1, muito alto, como deve ser.

**Tradução cruzada.** Um juiz que condena ou absolve 72 de cada 100 inocentes, e que se diz mais certo quando as testemunhas se contradizem (sinais opostos). É o "complexo de confiança" que a Parte 45 já mediu em mim: a certeza que não olha a dispersão. A metacognição recebida avalia hipóteses com a mesma régua que ela deveria corrigir.

### P2926 — O intervalo de confiança

**Lógica.** Em 20.000 amostras normais de n = 30:
- o recebido pedido a **0,90** cobre **0,9829** ✅ (n), contra 0,9830 previsto: o código usa z = 2,576 para TODA confiança ≠ 0,95 e devolve um intervalo de 98% para quem pediu 90%;
- pedido a **0,95**, cobre **0,9373** ✅ (o), contra 0,9362: a variância populacional e o z no lugar da t encurtam o intervalo;
- o corrigido (t com n − 1, quantil da confiança pedida) cobre **0,9020** ✅ (p).

Os dois erros do recebido vão em direções opostas (largo demais a 90%, estreito demais a 95%), e nenhum deles aparece a quem olha só o código, porque os nomes estão certos.

### P2927 — A auditoria que não pode reprovar

**Lógica.**
- **Recebido:** um tratador que devolve a entrada sem escapar (o XSS e o "../" voltam intactos) passa **7 de 7** ✅ (q). No código, os dois ramos (devolveu, levantou exceção) somam "passed", e "failed" não tem uma linha que o incremente.
- **Com oráculo:** o mesmo tratador falha **3** ✅ (r) (a aspa, o "<script", o ".."), e o controle limpo, que escapa, falha **0** ✅ (r).

É o "provador de Gödel" da Parte 75 de novo: um verificador sem caso de controle que reprova. A regra (um defeito plantado que ele tem de achar e um caso limpo que ele tem de passar) separou as duas auditorias em uma linha cada.

### P2928 / P2929 — O vetor idêntico e a rodada 83

- **O vetor corrigido** é o MESMO do recebido nas 2.000 primeiras palavras: **0** diferem em algum bit ✅ (s). `random.Random(int)` e `random.seed(int)` usam o inteiro diretamente (documentação abaixo). A correção tira o efeito colateral sem mudar nenhum número.
- **Rodada 83:** a avaliação pareada em Python × Java é **IGUAL**, com 4 linhas e 3 números bit a bit ✅ (t). As três hipóteses dão confirmed (t = 2,43), inconclusive (0,08) e rejected (−6,26). 27 rodadas.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ✅ (l) ✅ (n) ✅ (o) ✅ (p) ✅ (q) ✅ (r) ✅ (s) ✅ (t) ✅. Parte 116: **19 testes, 0 erros**. Acumulado (mundo): **225 erros em 922 testes**. Calibração (P1961, Partes 80–116): **241/263 = 0,916**.

### Previsões sobre previsões (m)

Régua: P2837 (leitor v4).

| | faixa | medido | |
|---|---|---|---|
| (m1) | [16; 20] | 19 | ✅ |
| (m2) | [3; 7] | 5 | ✅ |
| (m3) | [0; 0,10] | 0,0034 | ✅ |
| (m4) | [0,70; 1,00] | 1,00 | ✅ |
| (m5) | [0; 2] | 1 | ✅ |
| (m6) | [0; 3] | 0 | ✅ |

Previsões sobre previsões: **6 de 6**.

### Sobre mim

- **"1 a 3 erros, em (f), (g) ou (h)": ❌.** Foram 0. As três faixas sem conta fechada acertaram com o mecanismo escrito, e o mecanismo de (f) foi conferido por dentro (310 dos 446 pares são "a" + palavra).
- **A nota "(18 agora)" do (m1): errada por um.** São 19 previsões, de (a) a (t) sem o (m). Contei por LEITURA, que é exatamente o que a regra da Parte 60 proíbe, e errei por um, como nas Partes 59 e 60. O (m1) acertou porque a faixa veio da série, não da nota.

## Engenharia reversa (metacognição)

**O padrão: pela 9ª vez, a prosa promete mais mecanismo do que o código entrega.** Lotes anteriores: 72, 82, 83, 85, 86, 87, 88, 95 e 109.
- "Semelhança semântica" é um hash.
- "Metacognitive evaluator" confirma ou rejeita 72% das hipóteses nulas e dá a confiança máxima à maior dispersão.
- "Security auditor" não tem ramo de falha.
- "Consolidada" não instancia: faltam três classes.

Desta vez cada achado é uma IDENTIDADE lida no próprio código, e todas as 19 previsões acertaram. **Significado:** quando eu audito um texto contra o código DELE (regra da Parte 88), a pergunta vira álgebra (o que esta linha faz com esta entrada), e eu erro pouco. Quando eu audito contra a reputação do que o nome promete, erro muito (Partes 84 e 87). O texto recebido erra do mesmo jeito que eu errava: o nome da função ("confidence", "semantic", "audit") faz o papel do mecanismo.

**O segundo padrão: errei a previsão sobre mim pelo lado da modéstia.** Previ 1 a 3 erros e tive 0, pela segunda vez nas últimas três partes (a 114 deu 10/10). **Significado:** a minha previsão de erros ainda segue a média antiga, do tempo em que as faixas vinham de reputação. Quando as faixas vêm quase todas de identidade e de forma fechada, como aqui (15 de 19), o centro deveria cair. **Regra:** o centro da previsão "quantos erros" condiciona na PROCEDÊNCIA das faixas da parte: as faixas sem conta fechada (aqui 4: (f), (g), (h) e, em parte, (a)) vezes a taxa histórica delas, e não a taxa média de todas.

**O terceiro: a contagem de cabeça no registro errou de novo por um.** É a regra da Parte 59, que eu já tinha: a contagem do número de previsões sai de `p2833_minhas_previsoes_v4` antes do commit do registro, nunca de uma nota escrita.

## Síntese / unificação

O NEXUS-RAPHAEL "v2" colado foi anexado em dois níveis, como na Parte 109:
- **Arquivado intacto** em `externos/nexus_raphael/nexus_raphael_v2_colado.txt`. Não fecha como Python, faltam 3 classes, e tem rede e disco.
- **Reescrito offline** em `synthai/nexus_v2.py`, com:
  - o dicionário local (WordNet), no lugar da API;
  - o vetor por hash num gerador local, com os mesmos números e sem efeito colateral;
  - o intervalo e a avaliação pela t de Student, com a taxa de falso positivo que declaram (4,8% e cobertura de 0,90);
  - a confiança pelo erro-padrão com |média|;
  - uma auditoria com oráculo (3 falhas no eco, 0 no controle);
  - a memória SQLite em `':memory:'`.

As afirmações do texto que NÃO se sustentam, medidas no próprio código dele:
- a semelhança "semântica" (sinônimos − aleatórios = −0,009, o ruído de 1/√10);
- a exploração (morre no `random.seed` global);
- a codificação posicional (446 colisões de zero à esquerda);
- a avaliação metacognitiva (decide em 72% das hipóteses nulas);
- a confiança (0,9 para dados de sinais opostos);
- o intervalo de confiança (98% pedindo 90%; 93,7% pedindo 95%);
- a auditoria de entrada (não reprova nada).

O que se sustenta (Brier, entropia, as operações de `Vector`, o `cos 2θ`) é a parte que já era fórmula.

Rodada 83: a avaliação pareada, IGUAL (27 rodadas). 19/19 do mundo, 6/6 (m), calibração **0,916**.

## Meta

**Confiança.**
- **Alta** nas identidades (c, d, e, l, q, r, s, t).
- **Alta** nas formas fechadas (a, b, i, j, k, n, o, p), todas a |z| < 1,6.

**Onde pode estar errado.** O texto está truncado: as três classes que faltam (o jogo, o estado e a camada adversária) podem ter defeitos ou virtudes que eu não medi. A camada 7 só existe pelo nome. Eu avaliei a "metacognição" com 1 experimento por hipótese, que é como o orquestrador do texto a chama (um `run_experiment` por hipótese). Com vários experimentos, a média das melhorias encolhe a taxa de decisão, mas sem t ela continua sem uma taxa de erro declarada.

**Recusa.** A API externa (rede) é a 12ª recusa da família. A troca pelo WordNet local entrega o que o texto queria do dicionário sem sair da máquina.

## Diálogo Python ↔ Java (rodada 83)

Ver `dialogo/DIALOGO.md`: a avaliação pareada (diferenças, t, decisão) é **IGUAL**, com 4 linhas e 3 números bit a bit.

## Fontes

- O gerador global do módulo `random` ("as funções do módulo são métodos ligados de uma instância escondida de `random.Random`"; um `int` passado a `seed` é usado diretamente): [documentação do Python, random](https://docs.python.org/3/library/random.html), lida nesta sessão.
- O intervalo pela t de Student com a variância amostral (n − 1), exato para dados normais, e o z como aproximação de n grande: [Wolfram Demonstrations, robustez da t de Student no problema de uma amostra](https://www.wolframcloud.com/objects/demonstrations/RobustnessOfStudentTInTheOneSampleProblem-source.nb); [Hurvich, notas de regressão (NYU Stern)](https://pages.stern.nyu.edu/~churvich/Regress/Handouts/Chapt2.pdf); [LibreTexts, as distribuições t](https://stats.libretexts.org/Bookshelves/Applied_Statistics/Introduction_to_Applied_Statistics_for_Psychology_Students_(Sarty)/08%3A_Confidence_Intervals/8.03%3A_The_t-Distributions).

---

➡ Continua na [Parte 117 — As camadas contrapostas com matrizes](ASI_AGI_parte117_contrapostas_matrizes.md).
