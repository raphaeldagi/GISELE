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

---

<!-- medição preenchida DEPOIS; pré-registro só até aqui -->
