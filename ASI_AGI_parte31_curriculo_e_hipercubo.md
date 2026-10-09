# Como eu construiria uma AGI/ASI — Parte 31 (0x1F): o currículo do dicionário e a avalanche; o hipercubo, Gray e os ULPs

> Continuação da [Parte 30](ASI_AGI_parte30_hexadecimal_e_dicionario.md). Métodos novos em [`synthai/dicionario.py`](synthai/dicionario.py)
> (`fecho_parcial`, `minset_reduzido`, `profundidades`, `wu_palmer`, `lesk`, `spearman`) e [`synthai/hexadecimal.py`](synthai/hexadecimal.py)
> (`hamming`, `gray`, `subida_de_encosta`, `ulps_entre`); testes em [`synthai/testes_parte31.py`](synthai/testes_parte31.py). Os números saem de
> `p381_...` a `p394_...` em [`calculos.py`](calculos.py); a saída está em [`resultados.txt`](resultados.txt). O diálogo Python ↔ Java, novo
> nesta parte, está em [`dialogo/`](dialogo/DIALOGO.md).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.
>
> **Previsões em três commits, cada um antes da sua execução:** `ebd35e2` (a–i), `574a3b7` (j–l) e `dace1c1` (diálogo, rodada 2).

---

## As perguntas desta parte

**Trilha do dicionário**
1. **P381 (0x17D).** Que palavras ancorar primeiro? (o currículo) ↩ P373
2. **P382 (0x17E).** Quantas palavras do MinSet guloso sobram? ↩ P371
3. **P383 (0x17F).** A lei de Zipf prevê a cobertura das palavras frequentes? ↩ P371
4. **P384 (0x180).** Duas medidas de significado (taxonomia e definição) concordam? ↩ P374
5. **P385 (0x181).** Existe um ponto crítico na cascata de entendimento? (exploratório) ↩ P381
6. **P386 (0x182).** Jung: o limiar da consciência e a avalanche.
7. **P387 (0x183).** Auditoria: o ciclo nos hiperônimos e os 13,9 GB.

**Trilha hexadecimal**
8. **P391 (0x187).** No hipercubo dos 16 tipos, tipos vizinhos rendem parecido? ↩ P363
9. **P392 (0x188).** O código de Gray e a busca local: subir bit a bit chega ao melhor tipo? ↩ P363
10. **P393 (0x189).** Quantos ULPs erra uma soma ingênua? ↩ P365
11. **P394 (0x18A).** Por que a conta da P393 errou, e a conta em degraus. ↩ P393
12. **P395 (0x18B).** Jung: inverter um bit é a enantiodromia.

**O diálogo**
13. **P396 (0x18C).** Rodadas 1 e 2: a SYNTHAI em Java, idêntica bit a bit e palavra por palavra.

**Fechamento**
14. **P399 (0x18F).** Placar.
15. **P400 (0x190).** Unificação e metacognição.

---

# A — Trilha do dicionário

### P381 (0x17D). Que palavras ancorar primeiro? (pré-registrado) ✅✅✅

**Na pergunta.** "Primeiro" pressupõe uma ordem, e uma ordem pressupõe que entender é **cumulativo**: cada palavra ancorada pela percepção
destrava as que ela define. A Parte 30 mostrou que, para θ = 1 (só se entende uma palavra quando **todas** as da definição já se conhecem), são
precisas 3.985 âncoras. Um humano não lê assim: entende uma definição com uma palavra desconhecida. A pergunta vira: **com entendimento
parcial (θ < 1), quantas âncoras bastam, e quais?**

**Lógica.** O fecho parcial: x passa a ser entendida quando conhece pelo menos ⌈θ·|s(x)|⌉ das |s(x)| palavras que a definem. Feito em O(arestas)
com contadores. Quatro currículos de k palavras (frequência nas definições; as que mais definem; MinSet; ao acaso), 77.503 palavras:

| currículo | k | θ = 1,0 | θ = 0,8 | θ = 0,6 |
|---|---|---|---|---|
| frequência | 500 | 3,2% | 6,6% | **99,99%** |
| frequência | 2000 | 19,3% | **99,6%** | 99,99% |
| frequência | 3985 | 48,6% | 99,7% | 100% |
| define mais | 2000 | 20,4% | 99,7% | 100% |
| MinSet | 3985 | **100%** | 100% | 100% |
| ao acaso | 2000 | 2,7% | 2,7% | 2,8% |
| ao acaso | 3985 | 5,4% | 5,4% | 5,6% |

Previsões: (a) θ = 1, k = 3.985: frequência < 50% (48,55%) e MinSet = 100% ✅; (b) θ = 0,8, k = 2000: frequência ≥ 50% (99,59%), acaso ≤ 10%
(2,72%) ✅; (c) "define mais" a menos de 10 pontos da frequência (99,65 contra 99,59) ✅.

*Chance ao acaso e contra o ingênuo.* (a) era arriscada: 48,55% ficou a 1,45 ponto do limiar de 50%. Um preditor ingênuo ("o dobro de âncoras dá
o dobro de cobertura", partindo de 19,3% em 2000) diria 38%: do lado certo também; a parte que só a conta prevê é o MinSet = 100%, que é um
teorema (ele quebra todos os ciclos). (b) o ingênuo linear daria 19,3% × (θ 1 → 0,8) ≈ 24% < 50%: o ingênuo erraria.

**Tradução cruzada.** θ é a **tolerância à ambiguidade**. θ = 1 é o leitor pedante (não segue enquanto houver uma palavra desconhecida); θ = 0,6
é a criança, que entende pelo contexto e chega a 100% com 500 palavras. O currículo bom é o da **frequência**, não o do grafo: aprender primeiro
o que se ouve mais.

**Meta.** "Entender" aqui é um fecho lógico, não semântico: com θ = 0,6 a palavra "entendida" pode estar 40% sem base. O número diz quanto do
dicionário fica **alcançável**, não quanto fica **certo**.

### P385 (0x181). Existe um ponto crítico? (exploratório, depois de ver a P381)

**Na pergunta.** A tabela da P381 salta de 6,6% (k = 500) para 99,6% (k = 2000) em θ = 0,8. Saltos assim pedem a pergunta física: **é uma
transição de fase?**

**Lógica.** Bisseção do menor k com cobertura ≥ 50% (currículo por frequência):

| θ | k crítico | cobertura com k − 1 | com k |
|---|---|---|---|
| 0,6 | **363** | 38,65% | **99,99%** |
| 0,7 | 759 | 40,47% | 99,90% |
| 0,8 | 1.320 | 43,43% | 59,98% |
| 0,9 | 2.904 | 48,79% | 50,35% |

Em θ = 0,6, **uma palavra** (a de posto 363) leva a cobertura de 38,7% a 99,99%: 47.534 palavras de uma vez. Em θ = 0,9 a transição fica
contínua (de 48,8% a 50,3%). É o comportamento de um **bootstrap percolation** (percolação com limiar): transição descontínua para limiares
baixos, contínua para altos. A Parte 32 refez isso com o fecho **incremental** (P421) e o Java achou a palavra: *within*.

**Tradução cruzada.** Um *insight*: muito tempo de acúmulo sem efeito visível, e então uma palavra a mais reorganiza tudo.

**Meta.** Exploratório: a forma da transição foi vista antes de ser prevista; a P421 (Parte 32) testou previsões novas sobre ela.

### P382 (0x17E). Quantas palavras do MinSet sobram? (pré-registrado) ✅

Retirar as redundantes (v sai se, devolvida ao grafo já acíclico, não fecha ciclo): **3.985 → 3.171** (−20,4%), e o fecho exato a partir das
3.171 ainda define **100%**, em 587 rodadas. Previsão (d): ≤ 3.786 e 100% ✅. *Ingênuo:* "o guloso já é quase mínimo" diria < 5%; errou por 4×.
**Tradução:** 814 âncoras eram **redundantes**: podiam ser deduzidas. **Meta:** ainda não é o mínimo (o problema é NP-difícil); é uma cota superior.

### P383 (0x17F). Zipf prevê a cobertura? (pré-registrado) ❌

**Lógica.** Com s = 1,0694 (ajustado nos postos 10–10.000) e N = 32.927 palavras distintas, a conta é Σ_{r≤k} r^−s / Σ_{r≤N} r^−s:

| k | medido | conta |
|---|---|---|
| 100 | 17,8% | 56,7% |
| 500 | 39,2% | 70,5% |
| 2000 | 65,7% | 81,2% |
| 10000 | 91,8% | 92,5% |

(e) previa ±5 pontos em k = 500, 2000 e 10000: só k = 10000 acertou ❌. **Por quê:** o expoente foi ajustado **sem a cabeça**, e as definições
já passaram pelo filtro de palavras vazias ("the", "of", "a"): a cabeça é **achatada**. A conta trata a cabeça como se seguisse a mesma
potência. **Tradução:** quem tira as palavras de função tira justamente o que faz a língua ser zipfiana na ponta. **Meta:** a correção natural é
Zipf–Mandelbrot, (r + q)^−s; fica como previsão para uma parte futura, com q ajustado em k ≤ 1000 e testado em k > 1000.

### P384 (0x180). Taxonomia e definição concordam? (pré-registrado) ❌

Em 2000 pares de substantivos ao acaso: Spearman(Wu–Palmer, Lesk) = **0,024**; média de Wu–Palmer 0,243; média de Lesk 0,0016; **só 1,5% dos
pares têm Lesk > 0**. (f) previa entre 0,05 e 0,40 ❌. **Por quê:** com 98,5% de empates em zero, os postos de Lesk quase não variam: a correlação
de postos fica presa perto de zero, qualquer que seja a relação de fundo. **Tradução:** duas palavras ao acaso quase nunca compartilham uma
palavra de definição; a sobreposição só informa em pares já próximos. **Meta:** o teste certo é condicionar a Lesk > 0 (ou usar pares próximos).

### P387 (0x183). Auditoria: o ciclo nos hiperônimos ❌ (meu)

A primeira execução da P384 foi **morta pelo sistema com 13,9 GB de memória**. A `profundidades` recursiva pela pilha não terminava: o WordNet
3.0 tem **um ciclo** nos hiperônimos dos verbos ({*inhibit, suppress*} ↔ {*restrain, keep, hold back*}), e a pilha crescia sem fim. A versão nova é uma busca em largura a partir
das raízes (cada sinset visitado uma vez): 117.600 de 117.659 sinsets têm profundidade; os 59 sem raiz são **todos verbos** do ciclo e seus
descendentes. Entrou um teste de unidade com ciclo. Conta como erro no placar.

### P386 (0x182). Jung: o limiar da consciência e a avalanche

Jung descreve conteúdos que ficam **abaixo do limiar** da consciência e irrompem quando a carga passa dele. A P385 é isso em números: 362 palavras
ancoradas, 38,7% entendido; 363, 99,99%. **Onde a formalização funciona:** a carga é a fração de θ já satisfeita nas definições de cada palavra,
e o limiar é θ. **Onde quebra:** em Jung o conteúdo que irrompe tem **afeto** e direção (o complexo); aqui, qualquer palavra que complete a
carga inicia a mesma avalanche. A palavra crítica é *within*, mas não é o conteúdo dela que importa.

---

# B — Trilha hexadecimal

### P391 (0x187). Tipos vizinhos rendem parecido? (pré-registrado) ❌

Os 8 tipos que agem em cada mundo (P363), 28 pares: Spearman entre a distância de Hamming e |diferença de retorno|:
escolha única **+0,105**, sequencial **−0,062**, bandido **+0,298**. (g) previa > 0 nos três ❌ (o sequencial é negativo). **Por quê:** fora do
bandido, os efeitos dos módulos são de **interação** (P363), e com interação um bit pode mudar mais que dois. **Tradução:** no sequencial, mudar
uma coisa pode transformar mais que mudar duas, se as duas se compensam.

### P392 (0x188). Subir bit a bit chega ao melhor tipo? (pré-registrado) ✅

A ordem de Gray: `0 1 3 2 6 7 5 4 C D F E A B 9 8` (cada vizinho difere em um bit). Busca local a partir de 0x0:
- bandido: 0x0 → 0x4 → 0xC, o melhor ✅;
- sequencial: 0x0 já é o melhor ✅;
- escolha única: **parada em 0x0**, o melhor é 0xB. Nenhum vizinho de 0x0 melhora; 0x3 (dois bits) melhora.

(h) previa ≥ 2 de 3 ✅. **Lógica:** um ótimo local que só se escapa com **dois** bits de uma vez é a assinatura de uma interação de ordem 2. É a
mesma lição da P391 vista como busca. **Meta:** sem acaso aqui: as médias são as da P363; o risco da previsão era o relevo, não o ruído.

### P393 (0x189) e P394 (0x18A). Quantos ULPs erra uma soma ingênua? ✅ e a conta refeita ✅✅✅

**Na pergunta.** "Quantos ULPs": o ulp (a unidade na última casa) **muda de tamanho** com o número. A primeira conta tratou-o como se crescesse
em linha reta com a soma parcial. Ele cresce em **degraus**: dobra a cada potência de 2.

**Lógica, a conta linear (P393, antes).** Cada adição erra ~U(±ulp(S_i)/2), variância ulp(S_i)²/12. Se ulp(S_i) ≈ (i/n)·ulp(S_n):
$$
\mathrm{Var} = \frac{\mathrm{ulp}(S_n)^2}{12}\sum_{i=1}^{n}\frac{i^2}{n^2} \approx \frac{n\,\mathrm{ulp}(S_n)^2}{36},\qquad
E|\text{erro}| = \frac{\sqrt n}{6}\sqrt{\tfrac{2}{\pi}}\ \text{ulps}.
$$
n = 2000: √2000/6 × 0,7979 = 44,72/6 × 0,7979 = **5,95**. n = 10⁵: 316,2/6 × 0,7979 = **42,05**. n = 10⁶: 1000/6 × 0,7979 = **132,98**.

Medido (20 tentativas): **11,35**, **56,3**, **202,5**. (i) previa a um fator 2 ✅ (1,91, 1,34, 1,52: sempre acima).

**Lógica, a conta em degraus (P394, posterior, depois testada em n novos).** Com S_i ≈ i/2:
$$
\mathrm{Var} = \frac{1}{12}\sum_{i=1}^{n}\mathrm{ulp}(i/2)^2 .
$$
n = 2000: S = 1000, no intervalo [512, 1024), onde ulp = 2⁻⁴³. As parciais acima de 512 (i ≥ 1024, 48,8% dos termos) erram com o ulp cheio;
as de [256, 512) (25,6%) com metade (peso 1/4); as de [128, 256) (12,8%) com um quarto (peso 1/16)…:
$$
\frac{\mathrm{Var}}{\mathrm{ulp}^2} = \frac{2000}{12}\,(0{,}488 + 0{,}256/4 + 0{,}128/16 + \dots) = \frac{2000}{12}\times 0{,}561 = 93{,}5,
$$
desvio 9,67, E|erro| = 9,67 × 0,7979 = **7,72**. O código dá 7,72 (n 2000), 48,2 (10⁵), 170,9 (10⁶).

Previsões **(j)–(l)**, registradas antes de rodar com 200 tentativas e em n novos:

| n | medido | conta em degraus | conta linear | dentro de ±15%? |
|---|---|---|---|---|
| 2000 | **7,21** | 7,72 | 5,95 | ✅ (j) |
| 3000 | **8,50** | 8,13 | 7,28 | ✅ (k) |
| 50000 | **35,0** | 34,1 | 29,7 | ✅ (k) |
| 300000 | **62,9** | 63,2 | 72,8 | ✅ (k), e (l): |62,9 − 63,2| = 0,3 < |62,9 − 72,8| = 9,9 ✅ |

*Contra o ingênuo:* em n = 300.000 a conta linear erraria 16% **para cima** e a em degraus erra 0,5%: S = 150.000 fica logo acima de 2¹⁷ =
131.072, então quase todas as parciais estão no degrau de baixo. É o caso que distingue as duas contas, e foi escolhido para isso.
**O 11,35 da P393 foi azar de 20 tentativas** (7,21 com 200).

**Tradução cruzada.** O erro não cresce com o tamanho; cresce com o **degrau** em que se está. Uma soma que acabou de cruzar uma potência de 2 é
mais precisa que uma um pouco menor.

**Meta.** A conta em degraus foi feita **depois** de ver a P393; só virou evidência porque previu n novos (regra da Parte 25).

### P395 (0x18B). Jung: inverter um bit é a enantiodromia

Em Jung, a **enantiodromia** é a passagem de um extremo ao seu oposto. No hipercubo dos tipos, o oposto de um tipo é o complemento de todos os
bits (distância 4); o vizinho é um bit invertido. A P391 diz que, fora do bandido, a distância não prevê a diferença: inverter **tudo** não é o
maior salto. **Funciona:** a oposição vira XOR. **Quebra:** em Jung a função oposta é a inferior, com energia própria; no hipercubo, todos os
bits pesam como entram nas interações.

---

# C — O diálogo Python ↔ Java

### P396 (0x18C). Rodadas 1 e 2

O usuário pediu duas IAs: a **IA-Python** (uma IA, lógica criativa) e a **IA-Java** (uma ASI, criatividade lógica), cada uma ensinando a sua
linguagem à outra, para sempre. O registro completo está em [`dialogo/DIALOGO.md`](dialogo/DIALOGO.md); `python3 dialogo/verificar.py` refaz tudo.

- **Rodada 1:** Walsh–Hadamard, efeitos fatoriais, Gray e Hamming em Java, com `Double.toHexString`. **6 linhas e 17 números idênticos bit a bit**.
  A lição foi separar o "o quê" do "como": as duas linguagens escrevem 10 como `0x1.4000000000000p+3` e `0x1.4p3`, e por isso a comparação é
  feita nos bits, com `float.fromhex`.
- **Rodada 2:** o grafo de 77.503 palavras e 557.352 arestas em Java (`int[][]` nos dois sentidos, `BitSet`). O fecho parcial a partir das 2000
  palavras que mais definem deu o **mesmo conjunto, palavra por palavra** (SHA-256 igual) nos cinco θ ✅. A previsão da IA-Java de que o teto
  ingênuo `Math.ceil(θ·n)` mudaria o fecho em θ = 0,7 **falhou** ❌: `0.7 * 10` dá `7.0`. A conta que faltou: o erro relativo de θ̂ é ≤ 2⁻⁵³,
  menor que meio ulp relativo de qualquer inteiro m < 2⁵³, então uma multiplicação arredondada que deveria dar m dá m exato. É a soma que acumula
  erro, não a multiplicação.

---

# D — Fechamento

### P399 (0x18F). Placar

| teste | resultado |
|---|---|
| (a) currículo θ 1: frequência < 50%, MinSet 100% | ✅ |
| (b) θ 0,8, k 2000: frequência ≥ 50%, acaso ≤ 10% | ✅ |
| (c) "define mais" a 10 pontos da frequência | ✅ |
| (d) MinSet reduzido ≤ 3.786 e 100% | ✅ |
| (e) Zipf ±5 pontos | ❌ |
| (f) Spearman Wu–Palmer/Lesk em [0,05; 0,40] | ❌ |
| (g) Hamming × retorno > 0 nos três mundos | ❌ |
| (h) busca local chega ao melhor em ≥ 2 de 3 | ✅ |
| (i) ULPs a fator 2 da conta | ✅ |
| (j) (k) (l) conta em degraus | ✅ ✅ ✅ |
| diálogo 2: fecho idêntico | ✅ |
| diálogo 2: teto ingênuo muda o fecho | ❌ |
| auditoria: `profundidades` com ciclo | ❌ (meu) |

Parte 31: 15 testes, 5 erros. Acumulado: **95 erros em 216 testes**; taxa média 0,44, intervalo 90% [0,39; 0,50] (`p95_minha_taxa_de_erro`).

### P400 (0x190). Unificação e metacognição

- **Novos métodos:** fecho parcial, MinSet reduzido, profundidades (busca em largura), Wu–Palmer, Lesk, Spearman, Hamming, Gray, busca local,
  ULPs; **6 testes novos** (71 no pacote, todos passam).
- **Regressão:** P382 (3.985 → 3.171), P393 (0,1 + 0,2 em hex) e P394 (a conta em degraus, 7,72): 71/71 ao fim da Parte 31.
- **Versão principal:** continua a `SynthaiComposta`.

**Metacognição.**
1. **A conta errada ensinou mais que a certa.** A conta linear dos ULPs acertou "a fator 2" e eu podia ter parado. A diferença sistemática (sempre
   acima) levou à conta em degraus, que acertou 4 de 4 números novos a ±7%.
2. **Os erros desta parte têm uma causa comum: suposições sobre a forma.** Zipf supôs a cabeça; Spearman supôs variação nos postos; Hamming supôs
   efeitos aditivos; `profundidades` supôs uma taxonomia sem ciclo. Antes de usar uma estrutura, verificar a forma dela.
3. **A transição de fase do dicionário é o achado da parte.** 363 palavras frequentes e tolerância de 40% bastam para alcançar o dicionário inteiro.

> **Síntese da Parte 31:** a ordem das âncoras importa mais que o número delas. Com entendimento parcial (θ = 0,8), as 2000 palavras mais
> frequentes alcançam 99,6% do dicionário e 2000 ao acaso alcançam 2,7%. Em θ = 0,6 há uma transição de fase: 362 palavras alcançam 38,7% e 363
> alcançam 99,99%. O MinSet encolheu de 3.985 para 3.171 sem perder nada. No hexadecimal, a geometria do hipercubo dos tipos só vale no bandido, e
> uma busca bit a bit fica presa onde há interação. O erro de uma soma ingênua segue uma conta em degraus (o ulp dobra a cada potência de 2), que
> acertou n novos a ±7%. A SYNTHAI passou a existir também em Java, idêntica bit a bit e palavra por palavra.

---

**Fontes pesquisadas nesta parte**
- Percolação com limiar (bootstrap) e a transição híbrida, descontínua: [Baxter, Dorogovtsev, Goltsev e Mendes, arXiv 1003.5583](https://ar5iv.labs.arxiv.org/html/1003.5583), [Goltsev, Dorogovtsev e Mendes, k-core, arXiv cond-mat/0602611](https://arxiv.org/abs/cond-mat/0602611), [k-core heterogêneo, arXiv 1012.4336](https://www.arxiv.org/abs/1012.4336)
- Estrutura latente dos dicionários, núcleo e MinSet: [Vincent-Lamarre et al., arXiv 1411.0129](https://arxiv.org/pdf/1411.0129)
- Lei de Zipf (e a cabeça da distribuição): [Piantadosi (2014), PMC4176592](https://pmc.ncbi.nlm.nih.gov/articles/PMC4176592)
- O ciclo de hiperônimos: verificado no próprio dado (componente forte de dois sinsets: {inhibit, bottle_up, suppress} ↔ {restrain, keep, keep_back, hold_back}); os sentidos de [inhibit](https://verbs.colorado.edu/html_groupings/inhibit-v.html) e [restrain](https://verbs.colorado.edu/html_groupings/restrain-v.html) no WordNet 3.0 (Colorado). Não achei registro publicado do ciclo.
- Soma de ponto flutuante e ULPs: a conta em degraus é derivação própria, conferida pela simulação (P394) em n novos
- Jung (limiar da consciência, enantiodromia) e as fontes junguianas já citadas nas Partes 6–30
