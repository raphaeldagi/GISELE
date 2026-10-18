# Parte 109 — O NEXUS anexado: o que entra, o que fica no arquivo (0x6D)

↩ Parte 108 (o minimax) · ↩ Parte 102 (o pacote v0.15.0, Global Workspace) · ↩ Partes 84/93/103 (a fronteira da rede e da auto-replicação) · ↩ Parte 88 (auditar o texto contra o PRÓPRIO código)

> Pedido do usuário, no meio do ciclo: "Anexe ao nosso código humilde" / "Anexe tudo ao nosso código", com dois objetos. **(1)** Um arquivo enviado duas vezes (as duas cópias têm o mesmo SHA-256 `9b9dbe9e…`): `asi_metacognitivo_1.py`, 51.967 linhas, 1.908 funções, 81 classes. Não é o NEXUS: é o "ASI METACOGNITIVO — SIMULADOR EXPERIMENTAL, RODADA 37", que usa numpy. **(2)** O código NEXUS-RAPHAEL v0.1.0 colado na mensagem: só biblioteca padrão, ~700 linhas.
>
> **A leitura escolhida (regra da Parte 83, escrita antes de medir).** "Anexar tudo" é feito em DOIS níveis, conforme o mecanismo (regra da Parte 103: classificar cada componente pelo que ele faz, não pela moldura).
> - **Arquivo, não importado.** O simulador de 52 mil linhas fica guardado intacto em `externos/nexus_raphael/` e NUNCA é importado nem executado. A auditoria AST (feita antes desta parte, sem executar nada, como passo de segurança) achou nele:
>   - rede ligada por PADRÃO: `--offline` é opcional, e sem ele o código chama dictionaryapi.dev, DuckDuckGo (`ddgs`) e yfinance;
>   - o programa se reexecuta por `subprocess.run([sys.executable, __file__, …])` (`verifica_jobs`) e executa um arquivo vizinho (`_autoteste_r15`);
>   - carrega módulos vizinhos por `exec_module` (R31, R35–R37);
>   - roda `multiprocessing` com `fork`;
>   - tem 17 blobs `pickle` embutidos (base64 + zlib), carregados por `pickle.loads`. O SHA-256 de cada blob está ao lado dele, no mesmo arquivo: ele só mostra que o blob não se corrompeu, não que é seguro.
>
>   É a família recusada pela 11ª vez (Partes 84/93/102/103).
> - **Anexado de verdade, reescrito offline.** O NEXUS-RAPHAEL vira `synthai/nexus.py`, escrito do zero na mesma API. O cliente de rede sai (fica só a consulta ao léxico offline, que era o padrão dele: `network_enabled=False`), o estado não é gravado em disco e cada defeito achado ganha um teste (regra da Parte 72).

## As perguntas desta parte

1. **P2711 (0xA97).** Os 17 blobs pickle do simulador escondem código? Inspecionar os opcodes (pickletools, que NÃO desserializa) e contar as referências GLOBAL a módulos perigosos (os, subprocess, posix, builtins.eval/exec, sys). ↩ P2236, P2501
2. **P2712 (0xA98).** A auditoria de segurança do NEXUS aprova o próprio NEXUS? (O texto contra o próprio código, Parte 88.) ↩ P2711
3. **P2713 (0xA99).** Qual o valor EXATO do "Kuhn simplificado" do NEXUS para o jogador 0? (Enumerar as 6 distribuições, sem simular.) ↩ P2683
4. **P2714 (0xA9A).** O "Desvio da Curva Preditiva" do jogo Raphael é verdadeiro? Medir separando "os dois jogadores desviam" (o código recebido) de "só o jogador 0 desvia" (o que a hipótese diz). ↩ P2652
5. **P2715 (0xA9B).** O estimador Beta do NEXUS calibra como a conta diz? E o grafo síncrono/assíncrono conta as operações que o texto promete? ↩ P2714
6. **P2716 (0xA9C).** O valor exato do Kuhn acrescenta fronteira entre Python e Java? (rodada 76) ↩ P2681

## Previsões pré-registradas (ANTES de medir — este commit)

- **(a) P2711.** Os 17 blobs são caches de RESULTADO (dicionários, listas, arrays numpy): as referências GLOBAL nos opcodes são só numpy (`_reconstruct`, `ndarray`, `dtype`, `scalar`) e `builtins` inofensivos. Nº de referências a módulos perigosos (os, posix, nt, subprocess, sys, builtins.eval/exec/compile/getattr/__import__) **[0; 0]**. Risco: um único `os.system` ou `builtins.eval` refuta.
- **(b) P2712.** A `security_audit` do NEXUS procura `\bexec\s*\(` e `\beval\s*\(` no PRÓPRIO texto, e esse texto contém as strings `"exec("` e `"eval("` (dentro da checagem `Auditors`). Então ela se acusa: achados = {exec, eval}, `passed = False`, e `assert_harness` devolve **2 erros** (segurança + auditores). O NEXUS recebido, rodado, sairia com código 1. Faixa do nº de erros do harness **[2; 2]**. É um falso positivo que a auditoria por AST (chamadas reais) não tem: na versão reescrita, 0 achados.
- **(c) P2713.** Kuhn simplificado (P0 aposta com K, aposta com Q metade das vezes e com J nunca; P1 paga com Q ou K), pela conta: K → (½)(+1) + (½)(+2) = 1,5; Q → ½·[(½)(+1) + (½)(−2)] + ½·(−1) = −0,75; J → −1. Valor = (1,5 − 0,75 − 1)/3 = **−1/12 = −0,08333**. Faixa **[−0,08334; −0,08333]**. (O comentário do código, "chama Q com 50%", descreve o P1 errado: quem sorteia é o P0, e na hora de APOSTAR.)
- **(d) P2714.** Desviar = jogar a 2ª melhor casa, de valor ≤ ao da melhor naquele lance. Só o jogador 0 desviando, nas 60 partidas, a diferença (vitórias do desviante − vitórias do guloso) fica em **[−30; 0]**: a hipótese "o desvio aumenta as vitórias" é REJEITADA. No código recebido os DOIS jogadores desviam (`t % 2` não é testado); as perdas se compensam, então a diferença fica em **[−15; 15]**, um efeito confundido.
- **(e) P2715 (grafo).** Construção: 910 nós × 2 arestas = 1.820 operações; uma passada síncrona soma mais 1.820; total **[3.640; 3.640]**. Soma assíncrona com trava = 4 × 25 = **100**.
- **(f) P2715 (Beta).** O Brier do estimador Beta (p verdadeiro 0,72, 200 ensaios, semente 7) é p(1−p) = 0,2016 mais o custo de estimar, ≈ p(1−p)·ln n/n ≈ 0,005: centro 0,207. O desvio amostral da média dos erros quadráticos é √(0,72·0,28)·|0,518 − 0,078|/√200 ≈ 0,014, e a meia-largura fica em 1,645 × 0,014 × 1,36 (fator da Parte 79) ≈ 0,031. Faixa **[0,176; 0,238]**. A referência p = 0,5 dá 0,25 exato.
- **(g) P2716.** O valor exato do Kuhn (6 distribuições × árvore curta, só + − × ÷) é **IGUAL** bit a bit entre Python e Java. Divergências **[0; 0]**.

### Previsões sobre as previsões (m), pré-registradas

- **(m1)** nº de previsões do mundo em **[5; 8]**
- **(m2)** nº de faixas que cruzam/tocam o zero em **[2; 5]**
- **(m3)** mediana de w das faixas que não cruzam o zero em **[0; 0,60]**
- **(m4)** fração de acertos do mundo em **[0,55; 1,00]**
- **(m5)** nº de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** nº de surpresas (erro > largura) em **[0; 2]**

### Sobre mim, pré-registrado

(c) e (e) são contas fechadas, (b) é a leitura de duas linhas de regex contra o texto e (g) é mecânica. Os riscos são (a), porque nunca abri esses blobs e a previsão sai do nome "congelado = cache de resultado", que é procedência por NOME, a mesma da Parte 85; e (d), porque não rodei o caso mínimo do jogo Raphael (regra das Partes 84/87), embora a direção venha da conta: a 2ª melhor casa vale menos naquele lance. Espero **0 a 2 erros**, nesses dois.

### Adendo pré-registrado: dois testes novos nascidos de surpresas (escrito DEPOIS da 1ª medição, ANTES destes dois)

A 1ª medição trouxe duas surpresas (relatadas nas respostas). Pela regra da Parte 25, cada uma vira um teste novo, registrado antes de rodar:

- **(h) P2717.** No jogo Raphael recebido o jogador 0 NUNCA vence (0 de 60, nos dois braços). A minha hipótese: a agenda de palavras decide sozinha (P0 recebe as palavras dos lances pares, soma léxica 26; P1, 48). Teste: uma agenda JUSTA (no lance t, a palavra `words[t // 2]`, a mesma para os dois em cada rodada) e 60 partidas. **(h1)** O guloso P0 vence **[45; 60]**: ele escolhe primeiro em cada rodada e fica com o nexo (+5) no lance 0, contra uma casa a distância 1 (−1) do P1, uma vantagem de ~6 contra um ruído de cartas de desvio ≈ √(6·2·0,9²) ≈ 3,1. **(h2)** Só o P0 desviando, a diferença de vitórias fica em **[−30; 0]**: desviar no lance 0, com prob. 0,35, entrega o nexo.
- **(i) P2718.** No sorteio IID 6 de 60, o "número quente" acerta 0,237, contra a referência declarada 6/60 = 0,10. A minha hipótese: é um ARTEFATO e não uma previsão. O alvo é o MÍNIMO do sorteio ordenado (`draw[0]`), e o `most_common` desempata por ordem de primeira aparição, o que favorece números pequenos. A chance exata de um conjunto H fixo conter o mínimo é Σ_{h∈H} C(60−h, 5)/C(60, 6). Teste: a taxa observada contra a média dessa chance exata nos H realmente usados. **|z| ≤ 1,96** (binomial, forma fechada: sem o fator 1,36, regra da Parte 74), faixa de z **[−1,96; 1,96]**. Se |z| > 1,96, o histórico prevê alguma coisa e a hipótese do artefato cai.

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->

## As respostas (quatro camadas)

### P2711 — Os blobs pickle do R37 escondem código?

**Na pergunta.** "Escondem" supõe que olhar seja perigoso. Não é: o perigo do pickle está em **desserializar** (`pickle.loads` chama o que o `__reduce__` mandar). Ler os opcodes (`pickletools.genops`) não executa nada, e é isso que a pergunta pede.

**Lógica.** A AST do simulador tem **18** constantes de pickle (o pré-registro dizia 17, contadas de cabeça a partir de uma listagem de chamadas, e a AST conta 18). Mais o `R18_MEGA_B64`, que não é pickle: é um `struct` de sorteios (2 + 6 bytes por concurso). Os 18 SHA-256 embutidos conferem (**18 de 18**). As referências GLOBAL/STACK_GLOBAL são só **4**, todas do numpy: `dtype`, `ndarray`, `_reconstruct`, `scalar`. Referências perigosas: **0** ✅ (faixa [0; 0]). **Controle dos dois lados** (regra da Parte 75): um pickle PLANTADO com `os.system`, montado por `pickle.dumps` (que não executa), é acusado; um dict limpo passa (`p2711b`).

**Tradução cruzada.** O selo SHA-256 ao lado do blob é a assinatura que o próprio autor escreve sobre a própria carta: prova que ninguém a trocou no caminho, não que o conteúdo é bom. A confiança é verificada por quem lê, não declarada por quem escreve (a regra da Parte 33: o avaliador fica FORA do alcance de quem é avaliado).

**Meta.** Os blobs estão limpos, mas o arquivo continua no arquivo morto. O que ele faz ao RODAR (rede por padrão, se reexecutar, `exec_module` de vizinhos, `fork`) não muda porque os dados são inofensivos.

### P2712 — A auditoria de segurança do NEXUS aprova o próprio NEXUS?

**Na pergunta.** "Aprova a si mesmo" é a autorreferência que o NEXUS declara no topo ("Autorreferência não é prova"). A pergunta testa se ele segue a própria frase.

**Lógica.** Não aprova. Por regex no texto, a `security_audit` acha **3** coisas: `exec`, `eval` e `backdoor_marker`. As duas primeiras vêm das strings `"exec("`/`"eval("` dentro da checagem `Auditors`; a terceira vem da palavra `BACKDOOR` dentro do PRÓPRIO padrão de busca. O `assert_harness` original devolve **2 erros** ("auditoria de segurança do código falhou", "auditores falharam"): o NEXUS, rodado, sairia com código 1. ✅ na faixa [2; 2]. O mecanismo, porém, eu previ incompleto: escrevi {exec, eval} e esqueci que o `BACKDOOR` do padrão casa consigo mesmo. A **auditoria por AST** (chamadas e imports reais) acha no colado só a rede: `chamada:urlopen` e `import:urllib`. No reescrito, **nada**. E no R37 acha 9 classes: `__import__`, `exec_module`, `run` (do subprocess), `urlopen` e os imports `importlib`, `multiprocessing`, `pickle`, `subprocess`, `urllib`.

**Tradução cruzada.** Um detector que procura a palavra "mentira" acusa todo dicionário, porque o dicionário contém a palavra. Confundir menção com uso é o erro clássico (Quine: usar uma expressão não é o mesmo que mencioná-la), aqui em código: o regex lê **menção**, a AST lê **uso**.

**Meta.** A ironia não é só do NEXUS. A **minha** 1ª versão do auditor AST acusou `re.compile` como o `compile` dos builtins (falso positivo por nome) e foi corrigida para olhar a FORMA da chamada (`Name` × `Attribute`). E o meu 1º teste de "sem rede" procurava a string `"urllib"` e falhou no próprio conjunto de imports perigosos do auditor. Três falsos positivos do mesmo tipo numa parte, dois deles meus.

### P2713 — O valor exato do Kuhn simplificado

**Lógica.** São 6 distribuições equiprováveis. Com K: aposta; P1 com J desiste (+1), com Q paga (+2): média **1,5**. Com Q: aposta com pa = ½; P1 com J desiste (+1), com K paga (−2): ½·(−0,5) + ½·(−1) = **−0,75**. Com J: **−1**. Valor = (1,5 − 0,75 − 1)/3 = **−1/12** ✅ (`Fraction(-1, 12)` exato; simulado em 200 mãos, **−0,085**). O valor é **afim em pa**: −1/6 + pa/6. Apostar SEMPRE com Q dá **0**: a estratégia do NEXUS deixa 1/12 por mão na mesa contra esse P1. O comentário do código ("chama Q com 50%") descreve o jogador errado: quem sorteia é o P0, ao APOSTAR.

**Tradução cruzada.** O minimax da Parte 108 de novo: contra um adversário FIXO (que paga com Q ou K), a melhor resposta é pura (pa = 1), porque o valor é linear na mistura. Misturar só vale contra quem também se adapta. É o equilíbrio de indiferença da Parte 105 visto pelo avesso.

**Meta.** Não é o Kuhn completo (o próprio NEXUS diz `is_full_poker: False`): o P1 não tem a opção de passar e apostar, e o valor −1/18 do Kuhn completo não se aplica. Fica como pendência (rodada 77).

### P2714 / P2717 — O "Desvio da Curva Preditiva"

**Na pergunta.** "Desvio da curva preditiva" promete que fugir do previsível ganha. A pergunta certa (regra da Parte 102) é: em que regime, e de que tamanho?

**Lógica.** Na agenda ORIGINAL, o P0 **nunca vence**: 0 de 60, guloso ou desviando, um ou os dois (dif **0** e **0**: ✅ nas faixas [−30; 0] e [−15; 15]). Mas pelo motivo que eu NÃO previ: a agenda de palavras decide sozinha. O P0 joga nos lances pares e recebe nexus, word, mind, proof, game, logic: soma léxica (a1z26 mod 13) **5+8+1+5+0+7 = 26**. O P1 recebe raphael, number, doubt, error, rule, chance: **9+8+10+9+4+8 = 48**. Uma diferença de 22 que nenhuma carta (−1 a +2) compensa. O experimento recebido compara 0 com 0: não mede nada. Com a agenda **JUSTA** (`words[t // 2]`, a mesma palavra para os dois em cada rodada), o P0 guloso vence **59 de 60** (h1 ✅, [45; 60]), e desviar SÓ o P0 custa **−23 vitórias** (h2 ✅, [−30; 0]); os dois desviando, −16. A hipótese "o desvio aumenta as vitórias" é **REJEITADA** quando o confundidor sai.

**Tradução cruzada.** Duas camadas de confusão. (1) A variável que importava (a agenda) ficava fora do experimento: o resultado era da regra do jogo, não da estratégia. (2) O tratamento era aplicado aos dois braços (os dois desviavam), então a comparação não isolava o jogador 0. É o erro de desenho experimental que a Parte 9 (sementes pareadas) e a Parte 20 (medir o comportamento, não só a métrica) existem para evitar.

**Meta.** Acertei as faixas de (d) pelo motivo errado: previ que a diferença ficaria perto de 0 porque o desvio custa pouco, e ela ficou em 0 porque o P0 nunca podia ganhar. Isso conta como **erro de mecanismo** (regra da Parte 71): gerou o teste (h), que confirmou a direção que eu previa só quando o jogo deixou de estar decidido.

### P2715 — O grafo e o Beta

**Lógica.** Grafo: 910 × 2 = 1.820 operações na construção, mais 1.820 na passada síncrona, mais **100** nos incrementos assíncronos (cada um faz `ops += 1`): **3.740**. Previ 3.640 e esqueci os 100. **(e) ❌**: é a direção do meu viés medido na Parte 45 (esqueço custos). A soma travada é **100** exato (4 × 25): a trava funciona. Beta: Brier **0,1914** contra **0,25** da referência ✅ (faixa [0,176; 0,238]). Ficou abaixo do centro 0,207 porque a amostra deu p̂ = 0,7475 > 0,72.

**Achados sem previsão (posteriores; só viram evidência num mundo novo, regra da Parte 25).** O EWC do NEXUS "é apoiado" com um EMPATE: retenção 0,55 contra 0,55, e o critério é `>=`. Antes do deslocamento o EWC já estava PIOR (0,85 contra 0,975), porque a âncora é **zero** durante a tarefa A, e a penalidade puxa os pesos para 0 enquanto ele aprende a primeira tarefa. A Parte 95 já mediu que o EWC certo troca precisão por retenção nos pesos de Fisher alto; este EWC nem tem âncora até o fim da tarefa A.

### P2716 — rodada 76

**Lógica.** A enumeração do Kuhn numa grade de pa, Python × Java: **IGUAIS, 13 linhas e 12 números bit a bit** ✅. O resíduo −2⁻⁵⁴ de pa = 1 também coincide. 20 rodadas, e a fronteira continua a aritmética (exp, log, pow, sin… na faixa medida), nunca o jogo.

### P2718 — O número quente do sorteio

**Lógica.** O NEXUS declara que o histórico IID não prevê, e mede **0,237** de acerto contra **0,10** de "acaso". O próprio número dele parece desmentir a frase. Não desmente: a referência está errada. O alvo é o **mínimo** do sorteio ordenado (`draw[0]`), e a chance de um H fixo conter o mínimo é Σ_{h∈H} C(60 − h, 5)/C(60, 6), que é grande para números pequenos (para h = 1, C(59, 5)/C(60, 6) = 0,1). O `most_common(6)` desempata por ordem de primeira aparição, e como cada sorteio entra ORDENADO, os pequenos aparecem primeiro. Chance exata média nos H usados: **0,2299**; observado 0,2370; **z = 0,28** ✅ (faixa [−1,96; 1,96]). O histórico não prevê nada; a frase do NEXUS está certa e a régua dele, errada.

**Tradução cruzada.** É o paradoxo do mínimo: perguntar "o menor número sorteado é um dos 'quentes'?" já carrega a resposta, se os quentes são pequenos. Uma pergunta mal posta produz uma previsão aparente; o acaso tem de ser calculado para a pergunta FEITA, não para a pergunta pensada.

## Placar do mundo desta parte

### Sobre o mundo

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ❌ (f) ✅ (g) ✅ (h) ✅ (i) ✅. Parte 109: **9 testes, 1 erro** ((e): esqueci os 100 incrementos assíncronos). Erros de mecanismo dentro de faixas certas, registrados à parte: (b) previ 2 achados e houve 3; (d) previ ≈ 0 pelo motivo errado; a contagem de blobs, 17 contra 18. Acumulado (mundo): **220 erros em 814 testes**. Calibração (P1961, Partes 80–109): **138/155 = 0,890**.

### Previsões sobre previsões (m)

| | faixa | medido | |
|---|---|---|---|
| (m1) | [5; 8] | 9 | ❌ |
| (m2) | [2; 5] | 3 | ✅ |
| (m3) | [0; 0,60] | 0,00 | ✅ |
| (m4) | [0,55; 1,00] | 0,89 | ✅ |
| (m5) | [0; 2] | 0 | ✅ |
| (m6) | [0; 2] | 1 | ✅ |

Previsões sobre previsões (p1499): **5 de 6**. A (m1) errou pela regra que eu mesmo gravei na Parte 60 e não apliquei: cada surpresa gera previsões novas num mundo novo. As duas surpresas da 1ª medição viraram (h) e (i), e a contagem passou de 7 para 9.

### Sobre o meu código (auditoria desta parte)

- **P1092:** 0 de 8 pNN novas sem teste ✅. **P974:** 0 previsões unilaterais.
- **A suíte inteira** (488 testes, regra da Parte 41) achou **1 falha que não era desta parte**. O teste da Parte 100 (`test_p2446_retrospecto`) estava **vermelho desde a Parte 106**: a P2446 promete na docstring a calibração das Partes 80–100, mas chama a `p1961` com a faixa PADRÃO, que cresce a cada parte, e em 106 passou de 0,88 (120/136 = 0,882). Três partes (106, 107, 108) foram commitadas sem a suíte inteira, só com o teste da parte. A falha original fica registrada aqui. A P2446 não é editada (regra das Partes 14/16): a **P2719** fixa a faixa prometida e dá **0,868** (a Parte 100 escreveu 0,861, que era o valor até a Parte 99, antes do 5/5 dela entrar). A P2446, com a faixa crescente, dá 0,890.
- **Regra (reforço da Parte 41):** a suíte INTEIRA roda antes de CADA commit de código, não só o teste da parte. E toda função que diz "das Partes A–B" passa A–B explícito; uma faixa padrão que cresce é uma quantidade que muda sozinha.

## Engenharia reversa (metacognição)

**O padrão:** a confusão entre **menção e uso**, três vezes na mesma parte e duas delas minhas. O auditor do NEXUS acusa a palavra `exec(` que ele mesmo escreve para procurá-la. O meu 1º auditor AST acusou `re.compile` pelo NOME `compile`. O meu 1º teste de "sem rede" procurou a string `urllib` e achou a lista onde eu guardo os imports proibidos. **Significado:** quando eu escrevo um verificador, a minha 1ª versão olha a SUPERFÍCIE (o texto, o nome) e não a FORMA (a chamada, o import). É o mesmo atalho que eu aponto nos textos recebidos, e eu só o vi porque a regra da Parte 75 (um caso limpo que TEM de passar) estava no teste. **Regra nova:** todo verificador que eu escrevo roda, antes de qualquer veredito, sobre o PRÓPRIO código-fonte e sobre o próprio teste. Se ele acusa a si mesmo, ele lê menção.

**O segundo padrão:** as duas surpresas boas da parte ((d) e o sorteio) foram **réguas erradas, não efeitos**: o jogo estava decidido pela agenda, e o acaso estava calculado para a pergunta errada. Nos dois casos o número do NEXUS (0 vitórias; 0,237) parecia dizer algo sobre a estratégia ou sobre a previsão, e dizia algo sobre o desenho. **Significado:** antes de explicar um número surpreendente, conferir se a régua mede o que o nome diz (a régua da Parte 68: uma medida com defeito conhecido não sustenta conclusão).

**O erro (e):** esqueci um custo, os 100 incrementos que também contam operações. É a direção medida do meu viés (Parte 45: os meus centros ficam abaixo do medido porque eu esqueço custos). A lista de restrições da Parte 57 teria pegado: eu listei "construção + passada" e não perguntei "o que mais toca `self.ops`?". Um `grep "ops +="` antes de prever teria dado as três linhas.

## Síntese / unificação

A Parte 109 anexa o NEXUS-RAPHAEL à SYNTHAI em dois níveis, decididos pelo mecanismo e não pela moldura (regra da Parte 103):

- **Arquivado, nunca importado.** O simulador "ASI METACOGNITIVO R37", 51.967 linhas, fica intacto em `externos/nexus_raphael/`. Ele tem rede ligada por padrão, se reexecuta por `subprocess`, carrega vizinhos por `exec_module`, usa `fork` e traz 18 blobs pickle. Os blobs foram inspecionados por opcode sem desserializar: limpos, só numpy, 18 de 18 selos conferem. Os dados são inofensivos; o que o arquivo faz ao rodar não é.
- **Anexado de verdade.** O NEXUS v0.1.0 colado vira `synthai/nexus.py`, offline e sem disco, com quatro defeitos corrigidos, cada um com teste:
  - a auditoria que se acusa;
  - o experimento do desvio confundido (a agenda decide; os dois desviam);
  - o acaso errado do sorteio (0,23 e não 0,10);
  - a rede.

  Junta-se o Kuhn por enumeração (−1/12, e 0 com a melhor resposta pura, a mesma lição de indiferença das Partes 105/108). Rodada 76 IGUAL (20 rodadas).

Resultado do mundo: 8/9, calibração 0,890 mantida. O que o NEXUS tem de melhor (a higiene das afirmações: `agi: False`, "autorreferência não é prova", "consenso não é verdade") é o que a SYNTHAI pratica desde a Parte 33. O que ele tem de pior é o mesmo que eu tive nesta parte: verificadores que leem a superfície.

## Meta

Confiança alta em (a), (c), (g), (i) (contas fechadas e mecânica) e em (h) (60 partidas, efeito de −23, longe de zero). O que fica aberto:
- o Kuhn COMPLETO (−1/18 para o primeiro a jogar, Kuhn 1950), que este jogo não é;
- o EWC do NEXUS, com a âncora zero na 1ª tarefa (achado posterior, sem previsão; só vira evidência num mundo novo);
- o simplex n×m (a pendência da rodada 75, adiada).

O que não mudou: nenhuma rede, nenhuma auto-replicação, nenhum código recebido executado (11ª recusa da família). O `pickletools.genops` decodifica opcodes e argumentos sem importar módulos nem chamar `__reduce__`; o caso plantado com `os.system` foi lido sem efeito.

## Diálogo Python ↔ Java (rodada 76)

Ver `dialogo/DIALOGO.md`: a enumeração do Kuhn simplificado, numa grade da probabilidade de apostar com Q, é **IGUAL** bit a bit (13 linhas, 12 números), inclusive o resíduo −2⁻⁵⁴ de pa = 1. Pendência (rodada 77): o simplex n×m e o Kuhn completo.

## Fontes

- Kuhn poker, valor −1/18 para o primeiro jogador e a família de equilíbrios: [Wikipedia, Kuhn poker](https://en.wikipedia.org/wiki/Kuhn_poker); [Miao, tese (Dartmouth, 2014)](https://math.dartmouth.edu/theses/undergrad/2014/Miao-thesis.pdf); [Freiburg, notas de teoria dos jogos](https://gki.informatik.uni-freiburg.de/teaching/ss19/gametheory/gametheory14.pdf); [Hoehn et al., AAAI 2005](https://cdn.aaai.org/AAAI/2005/AAAI05-123.pdf).
- Pickle, `__reduce__` e execução arbitrária; `pickletools.genops` como leitor de opcodes: [arp242, Security of pickle and marshal](https://www.arp242.net/pickle-marshal-security); [Slaviero, Sour Pickles (Black Hat 2011)](https://sensepost.com/cms/resources/conferences/2011/sour_pickles/BH_US_11_Slaviero_Sour_Pickles.pdf); [CPython, Lib/pickletools.py](https://svn.python.org/projects/python/trunk/Lib/pickletools.py); [PyCharm Security, PIC100](https://pycharm-security.readthedocs.io/en/stable/_sources/checks/PIC100.md.txt).

---

➡ Continua na [Parte 110 — A dúvida calculada](ASI_AGI_parte110_a_duvida_calculada.md).
