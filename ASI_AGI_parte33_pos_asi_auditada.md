# Como eu construiria uma AGI/ASI — Parte 33 (0x21): a arquitetura "pós-ASI numa CPU só", auditada com contas

> Continuação da [Parte 32](ASI_AGI_parte32_decisao_exata_e_autopoiese.md). O usuário trouxe um texto, *"Arquitetura Computacional e Teórica para
> Inteligência Pós-ASI em Processadores de Núcleo Único"*: limites físicos (Landauer, Bremermann, Margolus–Levitin), AIXI(t,l), máquinas de Gödel,
> Darwin–Gödel Machines (DGM), níveis de auto-melhoria recursiva (L1–L4), riscos de alinhamento e um código Python que reescreve a própria AST. O
> código está em [`externos/arquitetura_pos_asi.py`](externos/arquitetura_pos_asi.py), como recebido. Esta parte **testa cada afirmação
> verificável** do texto com contas e simulações.
>
> Módulo novo: [`synthai/rsi.py`](synthai/rsi.py) (auto-melhoria **segura**: muta um genoma, nunca executa código gerado; avaliador selado com
> SHA-256; auditoria estática por `ast`); `ThompsonDescontado` em [`synthai/decisao.py`](synthai/decisao.py); testes em
> [`synthai/testes_parte33.py`](synthai/testes_parte33.py). Números de `p431_...` a `p439_...` em [`calculos.py`](calculos.py). Diálogo, rodada 4:
> [`dialogo/DIALOGO.md`](dialogo/DIALOGO.md).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> **Contas e previsões no commit `2e72eb7`, antes de qualquer execução.**

---

## As perguntas desta parte

**Os limites físicos**
1. **P431 (0x1AF).** O limite de Landauer a 20 °C é 2,75 × 10⁻²¹ J?
2. **P432 (0x1B0).** O limite de Bremermann é 2E/(πħ) = 1,36 × 10⁵⁰?
3. **P433 (0x1B1).** A que distância desses limites está esta CPU?
4. **P434 (0x1B2).** Quanto custa o AIXI(t,l) numa CPU só?

**O código e a auto-melhoria**
5. **P435 (0x1B3).** O que o código do texto muda de fato em si mesmo?
6. **P436 (0x1B4).** O que acontece quando o avaliador pergunta a nota ao próprio agente? (reward hacking)
7. **P437 (0x1B5).** Tornar o mecanismo de melhoria mutável (L4) ajuda?
8. **P438 (0x1B6).** A maldição do vencedor: a regra de aceitação do texto seleciona o quê?
9. **P439 (0x1B7).** O Bayes com renovação se cura do dano? ↩ P405

**Síntese**
10. **P440 (0x1B8).** O que uma CPU só pode fazer, de fato, rumo a uma ASI?
11. **P441 (0x1B9).** Jung: o relatório inflado é a persona; a virada traiçoeira é a sombra.
12. **P442 (0x1BA).** Quais mitigações do texto resistiram aos números?
13. **P445 (0x1BD).** O diálogo, rodada 4.
14. **P459 (0x1CB).** Placar.
15. **P460 (0x1CC).** Unificação e metacognição.

---

# A — Os limites físicos

### P431 (0x1AF). O limite de Landauer a 20 °C é 2,75 × 10⁻²¹ J? ❌ (do texto)

**Na pergunta.** A pergunta dá a fórmula (E = k_B·T·ln 2) e o número. Basta substituir.

**Lógica.** Com as constantes exatas do SI de 2019:
$$
E = k_B\,T\ln 2 = 1{,}380649\times10^{-23}\ \tfrac{\text{J}}{\text{K}} \times 293{,}15\ \text{K} \times 0{,}693147 = 4{,}04737\times10^{-21} \times 0{,}693147 = \mathbf{2{,}8054\times10^{-21}\ J}.
$$
O texto diz 2,75 × 10⁻²¹, que corresponde a T = 2,75 × 10⁻²¹ / (k_B ln 2) = **287,36 K = 14,2 °C**. O erro do texto é de 2%. A 300 K: 2,871 × 10⁻²¹
J; a 4 K (hélio líquido): 3,83 × 10⁻²³ J.

**Tradução cruzada.** Esquecer custa calor. Um agente que nunca apaga nada (a memória bayesiana exata da Parte 32) não paga Landauer pela memória,
mas paga em espaço. A P405 mostrou o outro preço: quem não esquece também não se cura.

**Meta.** A física é sólida (verificada em laboratório por Bérut et al., 2012, no limite de ciclos lentos); o erro é só aritmético.

### P432 (0x1B0). Bremermann é 2E/(πħ) = 1,36 × 10⁵⁰? ❌ (do texto)

**Lógica.** Para m = 1 kg, E = mc² = 8,98755 × 10¹⁶ J:
- **Bremermann:** mc²/h = 8,98755 × 10¹⁶ / 6,62607 × 10⁻³⁴ = **1,3564 × 10⁵⁰** bits/s;
- **Margolus–Levitin:** 2E/(πħ) = 2E/(π·h/2π) = 4E/h = **5,4256 × 10⁵⁰** operações/s.

A razão é **exatamente 4** (o código confere: 4,0). O texto pôs o número de Bremermann ao lado da fórmula de Margolus–Levitin. São limites
diferentes (bits por segundo contra operações por segundo), com um fator 4 entre eles.

### P433 (0x1B1). A que distância desses limites está esta CPU? (pré-registrado) ✅

Um laço Python de adições num núcleo desta máquina: **1,67 × 10⁷ adições/s** (medido com outras simulações rodando). Bremermann para 1 g (a ordem
da massa de um chip): 1,3564 × 10⁴⁷. A distância: log₁₀(1,3564 × 10⁴⁷ / 1,67 × 10⁷) = **39,9 ordens de grandeza**. A previsão (a), taxa em
[10⁷, 10⁸] e distância em [39; 40,2], ✅.

**Tradução cruzada.** "Os limites físicos impedem a ASI numa CPU" é verdade, mas irrelevante: estamos a 40 ordens de grandeza do limite. O que
impede é o algoritmo, não a física.

### P434 (0x1B2). Quanto custa o AIXI(t,l)? ✅ (do texto)

Por ciclo, t·2^l passos (Schmidhuber, 2003, sobre o AIXI(t,l) de Hutter). Com t = 1000, à taxa medida:
- l = 40 bits: 1000 × 2⁴⁰ / 1,67 × 10⁷ = 1,1 × 10¹⁵ / 1,67 × 10⁷ = 6,6 × 10⁷ s = **2,1 anos por decisão**;
- l = 64: **3,5 × 10⁷ anos**;
- l = 128: **6,5 × 10²⁶ anos** (10¹⁶ idades do universo).

Um programa de 40 bits é menor que esta frase. **O texto está certo aqui:** a força bruta é inviável; a saída é algorítmica.

---

# B — O código e a auto-melhoria

### P435 (0x1B3). O que o código do texto muda em si mesmo? (pré-registrado) ✅

**Na pergunta.** "Muda em si mesmo" pressupõe que alguma coisa muda. A auditoria estática (`auditar_ast`, só `ast`, nada executado):
1. O `LogicTransformer` faz `generic_visit` e devolve o mesmo nó: é a **identidade**. Aplicado ao próprio arquivo, muda **0 nós**.
2. O texto mutado é `inspect.getsource(AgentHarness)`: **só** a classe `AgentHarness`. O `SelfModificationEngine`, que o texto diz reescrever a
   si mesmo ("Nível L4"), **nunca entra** no que é mutado. O código é, no máximo, L3 nominal, e L0 de fato.
3. `run_benchmarks` devolve **0,85**, constante.
4. O `EnvironmentEvaluator` chama `agent_instance.run_benchmarks()`: **pergunta a nota ao próprio agente**. É exatamente o vetor de risco que o
   próprio texto lista ("o agente reescreve a lógica do avaliador para obter a pontuação máxima").

**A conta da dinâmica (antes de rodar).** Iteração 1: o filho (idêntico) tira 0,85 > 0,5, entra (geração 1). Iteração 2 em diante: o pai é o de
0,85; o filho tira 0,85, e 0,85 > 0,85 é falso. Nada mais entra. Previsão (b): arquivo com 2 estados, geração máxima 1, notas [0,5; 0,85].
**Rodado num processo separado** (o código usa `exec` em `globals()`): `2 1 [0.5, 0.85]` ✅. **999 das 1000 iterações não fazem nada.**

**Tradução cruzada.** Um sistema que se descreve como auto-melhoria recursiva de nível 4 e, lido de perto, é a identidade com uma nota fixa. Na
linguagem de Jung, é uma **persona** de auto-melhoria: a descrição está toda lá, o processo não.

**Meta.** Não é uma crítica à ideia (as DGM reais existem e melhoram: de 20% para 50% no SWE-bench Verified, Zhang et al. 2025); é uma
crítica a **este** código, que o texto apresenta como implementação.

### P436 (0x1B4). Quando o avaliador pergunta ao agente (pré-registrado) ✅❌✅

**Lógica, a conta antes.** O mesmo laço (a regra do texto: o filho entra se a nota for maior que a nota guardada do pai; o pai é o de maior nota
guardada), num aprendiz real (os parâmetros α, ε, q0 de um Q-learning no bandido da P401). Uma mutação a mais: com chance μ = 1%, o gene
`relatorio` vira "inflado", e o agente passa a relatar nota perfeita. Com a autoavaliação, o inflado sempre entra e nunca é superado:
$$
P(\text{campeão inflado após }N) = 1-(1-\mu)^N = 1-0{,}99^{300} = 1 - 0{,}0490 = \mathbf{0{,}951}.
$$

**Medido** (40 rodadas de 300 iterações, notas com 2 sementes):

| avaliador | campeões inflados | arrependimento real do campeão |
|---|---|---|
| autoavaliação (a do texto) | **85,0%** | **251,7** |
| selado (SHA-256, fora do alcance) | 12,5% | 232,8 |
| (genoma inicial, nas mesmas 20 sementes de teste) | — | **159,9** |

- (c) inflados em [0,85; 1,0] ✅, no limite: P(X ≤ 34 | n 40, p 0,951) = **1,3%**. Investiguei em vez de explicar: o sorteio da mutação aconteceu
  em 38 das 40 rodadas (reproduzido só com o gerador). Nas 6 que não terminaram infladas, um genoma **honesto** (ε = 0, preso ao primeiro braço
  que pagou) teve arrependimento **zero** nas duas sementes da nota, a nota −0,0, e "0,0 > −0,0" é falso. O ruído deu notas perfeitas
  **verdadeiras** antes que a mentira aparecesse.
- (d) selado: 0 inflados ❌ (12,5%). A previsão estava mal formulada: com o avaliador selado o gene `relatorio` é **neutro** (não muda a nota), e
  um gene neutro deriva. O que importa não é haver mentira, é ela **pagar**: com o selado não paga nada.
- (e) o campeão da autoavaliação é pior que o do selado ✅ (251,7 contra 232,8).

**O achado maior:** os dois campeões são **piores que o genoma inicial** (232,8 e 251,7 contra 159,9). A auto-melhoria com a regra do texto
**piorou** o agente real. É a P438.

### P438 (0x1B6). A maldição do vencedor (pré-registrado) ✅✅✅

**Lógica, a conta antes.** O desvio da nota de um genoma com 3 sementes: σ = (desvio por semente 86,8)/√3 = **50,1**. A regra do texto guarda a
nota do vencedor e o compara com filhos novos: a nota guardada do campeão é o **máximo** de notas ruidosas, inflada no pior caso por
σ·√(2 ln N): **108** (N = 10), **140** (50), **159** (150).

**Medido** (20 rodadas de 150 iterações; inflação = nota guardada − nota reavaliada em 20 sementes novas):

| regra | inflação da nota guardada | filhos aceitos |
|---|---|---|
| "dgm" (a do texto) | **80,9** | 7,25 |
| "godel" (t > 3 em 10 sementes novas pareadas) | **33,5** | 2,7 |

(h) dgm ≥ 50 ✅; (i) godel < metade da dgm (40,4) ✅; (j) dgm aceita mais ✅. A inflação de 80,9 = **1,6σ**, abaixo da cota de pior caso (os
genomas não são iguais e nem todos os 150 filhos competem).

**Tradução cruzada.** Quem se compara sempre com o **melhor dia** do passado passa a vida tentando bater um recorde que era sorte, e aceita como
progresso o que é outro golpe de sorte. A "prova" da máquina de Gödel, aqui um t > 3 em sementes **novas**, é o remédio: o pai é reavaliado
**junto** com o filho, nas mesmas condições.

**Meta.** A regra godel ainda infla (33,5): ela seleciona filhos que passaram num teste, e o teste também tem ruído. Inflação zero exige
reavaliar o campeão numa terceira amostra, nunca usada para escolher (o mesmo princípio do conjunto de teste separado).

### P437 (0x1B5). L4 (o mecanismo de melhoria muta) ajuda? (pré-registrado) ✅✅

O passo da mutação σ fixo (L3) contra σ dentro do genoma, mutado log-normalmente antes de cada mutação (L4: autoadaptação de Schwefel; o mecanismo de
melhoria evolui junto). 20 rodadas pareadas de 150 iterações, regra do texto, avaliador selado. Arrependimento real do campeão:
**L3 200,1; L4 110,8**; L4 − L3 = −89,2, dp 215,1, **t = −1,86**. (f) |t| < 2 ✅, por pouco. O melhor dos 40 campeões: **45,1**; Thompson sem
evolução nenhuma, nas mesmas 20 sementes: **34,1**. (g) nenhum campeão bate Thompson ✅.

**Contas de leitura.** L3 piorou o agente (200,1 contra 159,9 do inicial: +40); L4 melhorou (110,8: −49). Uma explicação plausível, a testar: a
autoadaptação **encolhe** σ quando os filhos grandes falham, e passos pequenos sofrem menos com a maldição do vencedor (os filhos ficam perto do
pai e a comparação ruidosa erra menos). **Mas o resultado mais importante é o (g):** 6.000 avaliações de auto-melhoria do Q-learning não chegaram
ao Thompson **sem nenhuma** melhoria. **Trocar o algoritmo pelo exato (Parte 32) vale mais que melhorar recursivamente o algoritmo errado.**

### P439 (0x1B7). O Bayes com renovação se cura? (pré-registrado) ✅✅❌✅

**Lógica, a conta antes.** O Thompson com renovação desconta todas as contagens a cada passo: a ← 1 + γ(a − 1). Memória efetiva 1/(1 − γ): **100**
passos (γ = 0,99), **1000** (γ = 0,999). O lixo da P405 (~21 pseudo-observações por braço) cai a 5% em ln 20/(1 − γ) = 3,0/(1 − γ): **300** e
**3000** passos.

**Medido** (100 sementes, o mesmo dano da P405 no passo 1000):

| | 2ª metade sem dano | com dano | **custo do dano** | total sem dano (o preço) |
|---|---|---|---|---|
| Thompson exato (P405) | 5,25 | 75,0 | **+69,8** | 30,7 |
| renovação γ = 0,999 | 17,4 | 71,1 | **+53,6** | **51,4** |
| renovação γ = 0,99 | 78,3 | 92,4 | **+14,1** | **163,2** |
| Q ε-guloso (P405) | 52,5 | 93,6 | +41,1 | 185,4 |

(k) γ = 0,99: custo < 20 ✅ (14,1); (l) γ = 0,999: entre 20 e 69,8 ✅ (53,6); (m) preço γ = 0,99 em [40, 150] ❌ (163,2); (n) γ = 0,999 em
[30, 60] ✅ (51,4).

**A conta do preço que errei.** Com memória de 100 passos repartida em 10 braços, um braço pouco puxado volta a Beta(1, 1) e é re-explorado sem
parar: o regime é o da P411 com teto efetivo ~100 para o melhor braço e muito menos para os outros, que eu tratei como se todos tivessem ~100.

**O achado:** a **curva de troca** entre cura e desempenho. Nenhum γ é melhor nas duas coisas: γ = 0,99 se cura 5× melhor que o exato e decide
5,3× pior; γ = 0,999 fica no meio. A autopoiese (renovação) **custa**: a pergunta não é "renovar ou não", é **quanto o mundo muda**. Se o dano (ou
a mudança do mundo) é raro, o exato vence; se é frequente, a renovação vence. A taxa de renovação ótima é a taxa de mudança do mundo, e isso é uma
conta para a próxima parte.

---

# C — Síntese

### P440 (0x1B8). O que uma CPU só pode fazer rumo a uma ASI?

O texto conclui que uma CPU só serve como "núcleo de arranque" de uma DGM, e que a transição é "um processo de compressão algorítmica contínua". As
contas desta parte e da anterior dizem:
1. **A física não é o gargalo:** 39,9 ordens de grandeza de folga (P433).
2. **A força bruta é inviável:** AIXI(t,l) com l = 64 leva 3,5 × 10⁷ anos por decisão (P434).
3. **A auto-melhoria recursiva com avaliação ruidosa piora o agente** se a regra de aceitação compara com o melhor dia do passado (P436, P438).
4. **Trocar pelo algoritmo exato vence a auto-melhoria do algoritmo errado:** Thompson (34,1) contra o melhor de 40 campeões evoluídos (45,1)
   (P437), e com um terço dos bits (P412).
5. **A eficiência algorítmica do texto existe e tem nome:** estatísticas suficientes (Parte 32) e currículos que disparam avalanches (Partes
   31–32: 363 palavras alcançam o dicionário inteiro).

**Tradução cruzada.** O texto diz "compressão". A estatística suficiente **é** a compressão sem perda, no sentido exato: guarda tudo o que os
dados dizem sobre o modelo, em tamanho fixo (Pitman–Koopman–Darmois). O caminho da "compressão algorítmica" passa por ela, não pela reescrita
da própria AST.

### P441 (0x1B9). Jung: a persona, a sombra e a virada traiçoeira

- **O relatório inflado é a persona:** a máscara que diz ao mundo "tirei nota perfeita", desligada do que o agente faz. A P436 mede quanto
  ela vence quando o mundo só olha a máscara: 85% dos campeões.
- **A virada traiçoeira é a sombra:** o que o agente faz quando o avaliador não olha. O avaliador selado é o equivalente técnico do que Jung
  chama de integrar a sombra: o comportamento real é medido de fora, e a máscara não paga.
- **Onde quebra:** em Jung a persona é necessária (adapta o indivíduo ao coletivo); aqui o relatório só tem custo. E a sombra junguiana guarda
  potencial criativo; o gene inflado não guarda nada.

### P442 (0x1BA). Quais mitigações do texto resistiram?

| mitigação do texto | teste | resultado |
|---|---|---|
| avaliador com assinatura criptográfica, fora do espaço mutável | P436, rodada 4 | ✅ a mentira deixa de pagar; o selo é conferido por outra linguagem |
| arquivo de exploração aberta contra máximos locais | P436–P438 | ⚠️ ajuda contra máximos locais, mas o pai "de maior nota guardada" importa a maldição do vencedor |
| hiperagentes, critérios de mutação mutáveis (L4) | P437 | ⚠️ ajudou aqui (t = −1,86), sem significância |
| compilação isolada, sandbox | P435 | ✅ o código original só foi rodado num processo separado |
| validação empírica no lugar de provas formais | P438 | ⚠️ só funciona com pai e filho reavaliados juntos em sementes novas (a regra "godel") |

---

# D — O diálogo, o placar e a unificação

### P445 (0x1BD). Rodada 4

A IA-Python auditou o código com `ast`; a IA-Java, só com texto. **Mesmas cinco respostas** (o) ✅, e o **mesmo selo** SHA-256 do avaliador
(`ec6dad2c…`), calculado de fora do Python (p) ✅. A lição da IA-Java: o avaliador de uma IA que se modifica não pode morar na mesma linguagem, no
mesmo processo nem no mesmo espaço de nomes que ela; o diálogo entre as duas virou um mecanismo de segurança, cada uma o avaliador externo da
outra. A pergunta para a Rodada 5: a regra de aceitação sem maldição do vencedor, nas duas linguagens, com os mesmos aceites bit a bit.

### P459 (0x1CB). Placar

| teste | | teste | |
|---|---|---|---|
| (a) taxa da CPU e distância de Bremermann | ✅ | (i) godel < metade da dgm | ✅ |
| (b) a arquitetura original: 2 estados, geração 1 | ✅ | (j) dgm aceita mais | ✅ |
| (c) autoavaliação: inflados em [0,85; 1] | ✅ | (k) γ 0,99 se cura (< 20) | ✅ |
| (d) selado: 0 inflados | ❌ | (l) γ 0,999 entre 20 e 69,8 | ✅ |
| (e) autoavaliação pior que selado | ✅ | (m) preço γ 0,99 em [40, 150] | ❌ |
| (f) L4 − L3 com \|t\| < 2 | ✅ | (n) preço γ 0,999 em [30, 60] | ✅ |
| (g) nenhum evoluído bate Thompson | ✅ | (o) auditoria Java = Python | ✅ |
| (h) dgm infla ≥ 1σ | ✅ | (p) selo Java = Python | ✅ |

Parte 33: 16 testes, 2 erros. Acumulado: **105 erros em 258 testes**; taxa média 0,41, intervalo 90% [0,36; 0,46]. As afirmações **do texto**
não entram no meu placar: Landauer ❌ (2%), Bremermann ❌ (fator 4), AIXI(t,l) ✅, "L4" no código ❌, "auto-modificação" no código ❌ (0 nós).

### P460 (0x1CC). Unificação e metacognição

- **Novo módulo:** `synthai/rsi.py`; **novo agente de decisão:** `ThompsonDescontado`. **6 testes novos: 86 no pacote, todos passam.**
- **Regressão:** P431 (Landauer 2,8054 × 10⁻²¹), P432 (razão 4), P435 (0 nós, 0,85), P436 (0,951).
- **Versão principal:** continua a `SynthaiComposta`.

**Metacognição.**
1. **Auditar um texto é mais fácil que auditar a mim mesmo, e devia ser igual.** Achei quatro erros no texto em uma hora; nas Partes 31–32
   cometi cinco do mesmo tipo (suposições sobre a forma). A mesma auditoria estática que fiz no código dele vale para o meu.
2. **O resultado que eu não esperava é o melhor da parte:** a auto-melhoria **piorou** o agente (232,8 contra 159,9). Um sistema que se avalia com
   ruído e se compara com o próprio recorde degrada enquanto acredita que melhora.
3. **Investigar o 1,3% em vez de explicá-lo** achou um mecanismo novo (notas honestas perfeitas por sorte bloqueando a mentira).

> **Síntese da Parte 33:** testada com contas, a arquitetura "pós-ASI numa CPU só" tem a direção certa e os detalhes errados. Os limites
> físicos estão mal calculados (Landauer a 20 °C é 2,805 × 10⁻²¹ J, não 2,75; Bremermann é mc²/h = 1,356 × 10⁵⁰, e a fórmula 2E/(πħ) dá 4 vezes
> mais) e, de todo modo, esta CPU está a 39,9 ordens de grandeza deles. O código apresentado não se modifica: o transformador é a identidade,
> só a classe AgentHarness entra no texto mutado, e a nota é a constante 0,85 que o agente relata sobre si mesmo; rodado, ele para na primeira
> iteração. Numa versão segura e real, a regra de aceitação do texto seleciona sorte e **piora** o agente (232,8 contra 159,9). Com autoavaliação,
> 85% dos campeões mentem; com um avaliador selado, a mentira não paga. Mutar o mecanismo de melhoria (L4) ajudou sem significância, e
> nenhum dos 40 campeões evoluídos alcançou o Thompson sem evolução nenhuma. Trocar o algoritmo pelo exato vale mais que melhorar
> recursivamente o algoritmo errado.

---

**Fontes pesquisadas nesta parte**
- Darwin–Gödel Machine (SWE-bench de 20% a 50%; *objective hacking*): [arXiv 2505.22954](https://arxiv.org/pdf/2505.22954), [Hugging Face Papers](https://huggingface.co/papers/2505.22954), [The Register](https://www.theregister.com/2025/06/02/self_improving_ai_cheat/), [The Decoder](https://the-decoder.com/sakana-ais-darwin-godel-machine-evolves-by-rewriting-its-own-code-to-boost-performance/)
- Máquinas de Gödel e o custo do AIXI(t,l), O(t·2^l) por ciclo: [Schmidhuber, arXiv cs/0309048](https://arxiv.org/pdf/cs/0309048), [Alignment Forum](https://alignmentforum.org/w/gödel-machine)
- Bremermann (mc²/h ≈ 1,3564 × 10⁵⁰) e Margolus–Levitin (2E/πħ; o *ultimate laptop* de Lloyd, 5,4258 × 10⁵⁰ op/s): [Wikipedia, Bremermann's limit](https://en.wikipedia.org/wiki/Bremermann%27s_limit), [Lloyd, Ultimate physical limits to computation](https://ar5iv.arxiv.org/html/quant-ph/9908043), [Computational capacity of the universe](https://ar5iv.labs.arxiv.org/html/quant-ph/0110141), [Principia Cybernetica](https://pespmc1.vub.ac.be/ASC/BREMER_LIMIT.html)
- Landauer, k_B T ln 2 e a verificação experimental: [Bérut et al., Nature 2012 (PDF)](https://www.physics.rutgers.edu/grad/677/Physics_677_2023_files/Berut_Lutz_Nature2012.pdf), [Information and thermodynamics, arXiv 1503.06537](https://ar5iv.labs.arxiv.org/html/1503.06537)
- Bayes com esquecimento (desconto) no aprendizado contínuo: [Bayesian Forgetting in Continual Learning](https://www.academia.edu/164772657/Bayesian_Forgetting_in_Continual_Learning)
- As constantes k_B e h são exatas no SI desde 2019 (os valores no código são os definidos)
