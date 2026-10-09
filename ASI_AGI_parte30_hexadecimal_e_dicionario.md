# Como eu construiria uma AGI/ASI — Parte 30 (0x1E): a SYNTHAI em hexadecimal, e o dicionário como data lake

> Continuação da [Parte 29](ASI_AGI_parte29_compor_e_pesar.md). Módulos novos: [`synthai/hexadecimal.py`](synthai/hexadecimal.py) e
> [`synthai/dicionario.py`](synthai/dicionario.py) (testes em [`synthai/testes_hexadecimal.py`](synthai/testes_hexadecimal.py) e
> [`synthai/testes_dicionario.py`](synthai/testes_dicionario.py)). Data lake: [`dados/`](dados/) (WordNet 3.0 de Princeton, com a
> [licença](dados/WORDNET_LICENSE.txt) e o [gerador](dados/gerar_wordnet.py)). Os números saem de `p361_...` a `p372_...` em
> [`calculos.py`](calculos.py); a saída completa está em [`resultados.txt`](resultados.txt). Tudo num arquivo só, agora com o dicionário:
> [`SYNTHAI_completo.py`](SYNTHAI_completo.py).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.
>
> **Previsões em quatro commits, cada um antes da sua execução**: `8a0797a` (hexadecimal), o do dicionário, o do desempate e o da correção.
> **Pedidos novos, gravados no `CLAUDE.md`:** usar o **dicionário de inglês como data lake** (cálculos, equações, pesquisa e métodos sobre ele a
> cada "Continue") e, **separadamente**, o **hexadecimal**, juntando os dois só quando for conveniente. Esta parte tem as duas trilhas e uma ponte.
>
> Como esta parte tem duas trilhas, ela usa 20 perguntas (P361–P380, ou 0x169–0x17C).

---

## As perguntas desta parte

**Trilha hexadecimal**
1. **P361 (0x169).** Por que o limiar da P71, em hexadecimal, é `0x1.23456789abcdfp-9`?
2. **P362 (0x16A).** Quantos dígitos hex por peso o pensamento da SYNTHAI precisa? (a conta Δ²/12)
3. **P363 (0x16B).** Os 16 tipos de SYNTHAI num dígito hex: quanto vale cada bit? (fatorial e Walsh–Hadamard)
4. **P364 (0x16C).** O pensamento com 1 ou 2 dígitos hex por peso decide igual?
5. **P365 (0x16D).** Impressões digitais exatas: resultados como bits, não como arredondamentos.
6. **P366 (0x16E).** O desempate: a composta ganha mesmo no sequencial?
7. **P367 (0x16F).** Jung: 16 tipos ou 8?
8. **P368 (0x170).** O piso do caos: quanto efeito dá para ver?
9. **P369 (0x171).** Auditoria do meu próprio código: o erro de sinal.
10. **P370 (0x172).** O que o hexadecimal ensinou.

**Trilha do dicionário**
11. **P371 (0x173).** A estrutura do dicionário: núcleo, Core, MinSet, Zipf, letras, taxonomia.
12. **P372 (0x174).** A ponte: o dicionário em hexadecimal.
13. **P373 (0x175).** Como um dicionário pode levar uma IA simples rumo a uma AGI? (o método, com números)
14. **P374 (0x176).** Jung: o dicionário e o inconsciente coletivo.
15. **P375 (0x177).** Por que o núcleo e o MinSet do WordNet saíram maiores que os da literatura?
16. **P376 (0x178).** Que módulos o dicionário pede para a SYNTHAI?
17. **P377 (0x179).** Capacidades.
18. **P378 (0x17A).** As fontes e a licença do data lake.
19. **P379 (0x17B).** Placar.
20. **P380 (0x17C).** Unificação e metacognição.

---

# A — Trilha hexadecimal

## Parte CXLII — O limiar escrito em base 16

### P361 (0x169). Por que o limiar da P71 é `0x1.23456789abcdfp-9`?

**Na pergunta.** Ao escrever o limiar da P71 em hexadecimal (`float.hex()`, que mostra os bits exatos do número), aparece:
$$
P^\* = \frac{c}{(1-\varepsilon)L} = \frac{0{,}1}{0{,}9 \times 50} = \frac{1}{450} = \texttt{0x1.23456789abcdf} \times 2^{-9}.
$$
Os dígitos em ordem, 1 2 3 4 5 6 7 8 9 A B C D F, pulando o E. Estava escondido desde a Parte 4: "as equações já foram resolvidas, só ninguém
percebeu", literalmente.

**Lógica.** Da série $\sum_{k \ge 1} k x^k = x/(1-x)^2$, com $x = 1/b$:
$$
\frac{1}{(b-1)^2} = \sum_{k \ge 1} k\, b^{-(k+1)} = 0{,}0\,1\,2\,3\cdots_b
$$
Os coeficientes são os dígitos enquanto cabem na base. O que vem depois do dígito $b-2$ soma mais que uma unidade daquela casa e **vai um**: o
$b-2$ vira $b-1$, e o dígito $b-2$ some. Em base 10, $1/81 = 0{,}\overline{012345679}$ (sem o 8); em base 16, $1/15^2$:
$$
\frac{1}{225} = \texttt{0x0.}\overline{\texttt{0123456789ABCDF}} \quad (\text{sem o E, período } 15),
$$
conferido por divisão longa inteira até a 32ª casa: `0x0.0123456789ABCDF0123456789ABCDF01`. E
$$
\frac{1}{450} = \frac{1}{2 \times 225} = 2^{-9} \times \frac{256}{225} = 2^{-9} \times 16 \times \texttt{0x0.123456789ABCDF}\ldots = 2^{-9} \times \texttt{0x1.23456789ABCDF}\ldots
$$
porque $450 = 2 \times 15^2$. O limiar dobrado da P131 é o mesmo número com o expoente $-8$. A regra "período $b-1$, sem o dígito $b-2$" foi
conferida **em todas as bases de 3 a 16** (`p361_hex_do_limiar`).

**Tradução cruzada (Jung).** É um arquétipo no sentido exato da Parte 23: uma **forma** que já estava no número e que só aparece quando se olha na
base certa. Em base 10, $1/450 = 0{,}00222\ldots$ não mostra nada. A forma é a mesma; a "linguagem" em que se olha decide se ela se revela.

### P362 (0x16A). Quantos dígitos hex por peso o pensamento precisa? (a conta antes da simulação)

**Lógica.** Quantizar um vetor de pesos em $b$ bits com escala $R = \max|w|$ dá passo $\Delta = 2R/(2^b - 1)$. Com erro uniforme em
$[-\Delta/2, \Delta/2]$ (variância $\Delta^2/12$), o erro no logit de uma opção com variáveis $x$ é
$$
\sigma_{\text{logit}}^2 = \frac{\Delta^2}{12} \sum_i x_i^2 .
$$
Cada bit a menos multiplica a variância por ~4 (6 dB por bit). O pensamento de Newton de uma semente (escolha única), em hexadecimal exato:

| Peso | `float.hex()` | Decimal |
|---|---|---|
| intercepto | `-0x1.dd97831532641p+2` | −7,462 |
| discordância | `0x1.ec997b39a177cp+2` | 7,697 |
| nota − melhor | `0x1.c619c8ef26ac5p+0` | 1,774 |
| leitura | `0x1.1415407e500d2p+0` | 1,078 |

Com $R = 7{,}697$: 4 bits, $\Delta = 2 \times 7{,}697/15 = 1{,}026$, e o pensamento inteiro vira **4 dígitos hex: `0F99`**; 8 bits,
$\Delta = 2 \times 7{,}697/255 = 0{,}0604$, e vira **`04FF9D91`**.

Nas candidatas (10 sementes por mundo), erro no logit previsto pela conta contra o real:

| Mundo | 1 dígito hex (4 bits) | 2 dígitos hex (8 bits) |
|---|---|---|
| Escolha única | previsto 0,586 · real 0,685 | previsto 0,0345 · real 0,0314 |
| Sequencial | previsto 0,543 · real 0,476 | previsto 0,0319 · real 0,0232 |

A conta acerta a ordem de grandeza nos dois casos. Com 2 dígitos ela acerta a 10–30%: o erro uniforme é uma boa hipótese com 256 níveis. Com 1
dígito erra mais (16 níveis só, erro correlacionado com o peso). A razão entre os dois erros é $(255/15)^2 = 289$ na variância, $17$ no desvio:
$0{,}586/0{,}0345 = 17{,}0$. ✅ (conferência, não previsão).

## Parte CXLIII — Os 16 tipos

### P363 (0x16B). Quanto vale cada bit? (pré-registrado)

**Lógica.** Cada bit de um dígito hex liga um módulo; o tipo `0xN` é uma SYNTHAI:

| Bit | Módulo | De onde |
|---|---|---|
| `0x1` | pensamento de Newton | P302 |
| `0x2` | limiar autorregulado com âncora | P343 |
| `0x4` | exploração de Thompson | P295 |
| `0x8` | leitura neutra do sensor | P292 |

A SYNTHAI da Parte 22 é `0x0`; a principal antiga é `0x4`; a composta (P356) é `0x4` no bandido e `0x3` fora dele. Os testes de unidade conferem
duas **identidades exatas** que a arquitetura promete: fora do bandido, o bit `0x4` não muda nada; no bandido, o bit `0x2` não muda nada. Então,
em cada mundo, **só 3 bits agem**: 8 tipos efetivos, um fatorial $2^3$.

Os efeitos saem da **transformada de Walsh–Hadamard** (o algoritmo de Yates, 1937): com as respostas em ordem binária,
$$
T_j = \sum_i (-1)^{\operatorname{popcount}(i \,\&\, j)}\, y_i, \qquad \text{efeito}_j = (-1)^{\operatorname{popcount}(j)} \frac{T_j}{2^{k-1}},
$$
calculada em $k \cdot 2^k$ somas e diferenças (borboletas). O sinal $(-1)^{\operatorname{popcount}(j)}$ é o da P369.

20 sementes novas (900–919), os 8 tipos pareados em cada semente:

**Escolha única** (retorno médio):

| `0x0` | `0x1` | `0x2` | `0x3` | `0x8` | `0x9` | `0xA` | `0xB` |
|---|---|---|---|---|---|---|---|
| 1,4306 | 1,4167 | 1,4076 | **1,4780** | 1,4304 | 1,4167 | 1,3967 | **1,4781** |

| Efeito | Valor | t | Previsão |
|---|---|---|---|
| Newton `0x1` | +0,031 | 1,07 | (a) < 0 ❌ |
| âncora `0x2` | +0,017 | 1,04 | |
| Newton × âncora | **+0,045** | 1,59 | (b) > 0 ✅ |
| neutro `0x8` | −0,003 | −0,97 | (c) \|·\| < 0,03 ✅ |

**Sequencial:**

| `0x0` | `0x1` | `0x2` | `0x3` | `0x8` | `0x9` | `0xA` | `0xB` |
|---|---|---|---|---|---|---|---|
| **20,139** | 19,931 | 19,856 | 19,922 | 19,742 | 19,765 | 19,955 | 20,006 |

| Efeito | Valor | t | Previsão |
|---|---|---|---|
| Newton `0x1` | −0,017 | −0,11 | |
| âncora `0x2` | +0,040 | 0,51 | (d) entre +0,15 e +0,6 com t ≥ 2 ❌ |
| Newton × âncora | +0,075 | 1,05 | (e) > 0 ✅ |
| neutro `0x8` | −0,095 | −1,23 | |
| âncora × neutro | **+0,187** | **2,16** | |

**Bandido** (Υ normalizado):

| `0x0` | `0x1` | `0x4` | `0x5` | `0x8` | `0x9` | `0xC` | `0xD` |
|---|---|---|---|---|---|---|---|
| 0,4715 | 0,4318 | 0,5637 | 0,5219 | 0,4638 | 0,4140 | **0,5766** | 0,4435 |

| Efeito | Valor | t | Previsão |
|---|---|---|---|
| Newton `0x1` | **−0,066** | **−3,49** | (g) < 0 ✅ |
| Thompson `0x4` | **+0,081** | **3,46** | (f) entre +0,05 e +0,20 com t ≥ 2 ✅ |
| neutro `0x8` | −0,023 | −1,86 | (h) ≤ 0 ✅ |

**O que o fatorial mostra, num quadro só.** No bandido, dois bits mandam e com sinais opostos: Thompson ajuda (+0,081), Newton atrapalha (−0,066).
É a P344 e a P305 medidas de uma vez, com os outros bits balanceados. Fora do bandido, nenhum bit sozinho passa de t = 2; o que aparece é
**interação**: Newton e âncora juntos (`0x3`, `0xB`) são os melhores na escolha única, e a âncora com o neutro (`0xA`, `0xB`) no sequencial. Os
módulos valem **em combinação**, que é a tese da composição (P351) vista por outro lado.

### P366 (0x16E). O desempate: a composta ganha mesmo no sequencial? (pré-registrado) ✅

**Na pergunta.** No fatorial, `0x3` (a composta fora do bandido) perdeu de `0x0` (a principal antiga fora do bandido) por **−0,218** no sequencial.
Conferi a identidade nas sementes 900 e 901: os números batem até a sexta casa. Não é erro de código. Mas a P343 e a P356 tinham dado +0,411 e
+0,337 (t ≈ 3,5). Um lote contradiz dois.

**Previsão registrada:** em 60 sementes novas (1000–1059), composta − principal entre 0 e +0,4, com t ≥ 2.

| | Diferença | dp | t |
|---|---|---|---|
| 60 sementes | **+0,230** | 0,642 | **2,78** |
| primeira metade | +0,248 | | 2,04 |
| segunda metade | +0,213 | | |

✅ A composta continua a versão principal. A estimativa honesta, juntando os quatro lotes:
$$
\frac{0{,}411 \times 30 + 0{,}337 \times 30 - 0{,}218 \times 20 + 0{,}230 \times 60}{140} = \frac{31{,}88}{140} = +0{,}228,
$$
cerca de **metade** do que os dois primeiros lotes sugeriam. As catástrofes ficaram 1,97% contra 1,53%.

### P368 (0x170). O piso do caos

**Lógica.** A P364 quantizou os pesos em 2 dígitos hex: o logit muda ~0,03. Mesmo assim, a diferença por semente teve desvio **0,58** no sequencial,
o mesmo tamanho da diferença entre duas versões quaisquer. Uma perturbação mínima desfaz um empate, uma decisão muda, e o episódio inteiro diverge:
é **caos de decisão**. Isso dá o menor efeito visível com $n$ sementes e t = 2:
$$
\delta_{\min} = \frac{2\,\sigma}{\sqrt n} = \frac{2 \times 0{,}58}{\sqrt{20}} = 0{,}26 \;(n = 20), \qquad \frac{2 \times 0{,}64}{\sqrt{60}} = 0{,}165 \;(n = 60).
$$
O desempate da P366 (+0,230, $n = 60$) está acima do piso; o lote de 20 sementes da P363 (−0,218) estava no limite dele. Um lote de 20 sementes não
consegue separar um efeito de +0,23 do zero com segurança, e foi isso que aconteceu.

### P364 (0x16C). O pensamento com 1 ou 2 dígitos hex decide igual? (pré-registrado) ❌❌

| Mundo | Completo (64 bits) | 2 dígitos hex | 1 dígito hex |
|---|---|---|---|
| Escolha única | 1,4957 | 1,4799 (−0,016; t −0,52) | 1,4734 (−0,022; t −0,60) |
| Sequencial | 20,1148 | 20,0328 (−0,082; t −0,63) | 19,9776 (−0,137; t −1,01) |

Previsões: (i) 2 dígitos com |diferença| < 0,02 nos dois mundos ❌ (sequencial: 0,082); (j) 1 dígito com |diferença| > 2 × a de 2 dígitos ❌ (1,4× e
1,7×). As duas previsões pediam precisão abaixo do piso do caos (P368): eu previ diferenças de 0,02 num mundo onde nada menor que 0,26 é visível.
Nenhuma das diferenças é significativa: **até onde 20 sementes enxergam, um dígito hex por peso basta** (o pensamento inteiro em `0F99`).

### P365 (0x16D). Impressões digitais exatas

**Lógica.** Um teste de regressão que arredonda (`round(x, 3)`) aceita qualquer mudança abaixo da terceira casa. Em hexadecimal, `float.hex()`
guarda os 53 bits da mantissa: duas máquinas que dão o mesmo `float.hex()` deram o mesmo número, bit a bit.

| Grandeza | Bits exatos |
|---|---|
| $P^\*$ | `0x1.23456789abcdfp-9` |
| $\mathbb E[1/X \mid X \ge 1]$, λ = 9,5 | `0x1.eb429c5594dc2p-4` |
| Wilson–Hilferty, forma 9,5 | `0x1.7e3b12136eaabp+3` |
| SHA-256 da bateria inteira (B1 + B2, em hex exato) | `38be1420a8d3622771d385187c1f388123df8fd44c69fb1a7a11e6c76b59ac11` |

A regressão passou a ter testes **exatos** (P361, P365): se um bit da bateria mudar, a impressão digital muda inteira.

### P367 (0x16F). Jung: 16 tipos ou 8?

**Tradução cruzada.** Um dígito hex são 4 bits: 16 tipos. Os 16 tipos famosos não são de Jung: são do Myers–Briggs, que acrescentou uma quarta
dicotomia (julgamento/percepção) aos tipos de Jung. Jung tinha **8**: 2 atitudes × 4 funções, ou 3 bits, um dígito **octal**. O fatorial
encontrou a mesma estrutura: em cada mundo, um dos 4 bits não age (identidade exata), e sobram **8 tipos efetivos**. O quarto bit é real em um
mundo e inerte no outro.

**Onde a formalização quebra.** Os bits de Jung não são independentes como os de um fatorial: a função dominante exclui a oposta (pensamento
dominante implica sentimento inferior). Um tipo junguiano é uma **ordem** das funções, não um conjunto de interruptores. O fatorial mede efeitos
de módulos que coexistem; a tipologia de Jung descreve quais dominam. Um fatorial de **ordens** ($4! = 24$ ordens das funções) seria a formalização
mais fiel, e é um experimento para outra parte.

### P369 (0x171). Auditoria do meu próprio código: o erro de sinal ❌ (meu)

**Lógica.** A primeira versão de `efeitos_fatoriais` fazia efeito $= -T_j/2^{k-1}$ para todo $j$. O sinal da transformada em cada linha é
$(-1)^{\operatorname{popcount}(i \,\&\, j)}$: (+) no nível **baixo** de cada fator. O contraste padrão de um efeito de ordem $r$ usa (+) no nível
**alto**, que é $(-1)^r$ vezes o da transformada. Negar todos acerta os efeitos principais ($r = 1$) e as interações triplas ($r = 3$), mas **troca
o sinal** das interações de ordem 2. O teste de unidade não pegou porque eu o fiz com interação igual a zero ($[10, 12, 20, 22]$).

**Correção:** efeito$_j = (-1)^{\operatorname{popcount}(j)}\, T_j / 2^{k-1}$, com dois testes novos: um com interação não nula
($[10, 12, 20, 30]$ dá $A = 6$, $B = 14$, $AB = ((30-20) - (12-10))/2 = 4$) e um contra a definição direta em três fatores. Com o sinal certo,
duas previsões que pareciam erradas, (b) e (e), estavam certas. A primeira leitura delas foi feita com o código errado; registro isso aqui para que
fique claro que a correção veio de conferir a convenção, não de querer que as previsões acertassem. A previsão (d), sobre um efeito principal,
não mudou.

### P370 (0x172). O que o hexadecimal ensinou

1. **Escrever em outra base mostra formas escondidas** (P361): $1/450$ tem os dígitos em ordem em base 16.
2. **Bits exatos dão testes exatos** (P365): a regressão agora compara números bit a bit.
3. **Um dígito hex por peso basta** (P362, P364), até onde o caos deixa ver.
4. **Um fatorial binário mede interações** (P363), e as interações apareceram onde os efeitos isolados não apareciam.
5. **O piso do caos** (P368) explica por que um lote de 20 sementes contradisse dois de 30, e foi o desempate de 60 (P366) que decidiu.

---

# B — Trilha do dicionário

## Parte CXLIV — O dicionário como data lake

### P371 (0x173). A estrutura do dicionário (pré-registrado) ✅❌✅❌✅✅✅✅

**Na pergunta.** "Use o dicionário como data lake" e "descubra como manusear o dicionário para tornar uma IA simples numa AGI". Um dicionário
define palavras por palavras. Harnad (1990) chamou isso de **carrossel do dicionário**: quem só tem um dicionário chinês-chinês passa de símbolo em
símbolo sem nunca chegar ao significado. É o **problema da ancoragem dos símbolos**, e é a pergunta certa: o que falta a uma IA que só tem texto?

**Lógica (o método).** O WordNet 3.0 (117.659 conjuntos de sinônimos, 147.306 lemas, cada conjunto com uma definição) vira um **grafo de
definições**: uma aresta $v \to w$ quando $v$ aparece na definição de $w$ (depois do Morphy, que reduz "children" a "child", e sem as palavras
gramaticais). Sobre ele, os métodos de Vincent-Lamarre, Harnad et al. (2016):

- **Núcleo (kernel):** tirar, repetidamente, as palavras que não definem nenhuma palavra que restou. O que sobra define tudo o que saiu.
- **Core:** o maior componente fortemente conexo do núcleo (algoritmo de Tarjan). Os componentes pequenos que sobram são os **satélites**.
- **MinSet:** um conjunto de retroalimentação de vértices: com essas palavras ancoradas **de fora** (pela percepção), todas as outras se definem por
  cadeias de definições, sem círculos. Achar o mínimo é NP-completo; uso uma aproximação gulosa (tira o que não está em ciclo, ancora a palavra
  com maior produto "definida por × define", repete).
- **Fecho:** partindo do MinSet, quantas palavras se definem, e em quantas rodadas.

**Previsões registradas** (referências: núcleo ~10%, Core ~75% do núcleo, MinSet ~1% do dicionário, em Vincent-Lamarre et al.; 4,14 bits por
letra, em Shannon 1951):

| Medida | Resultado | Previsão | |
|---|---|---|---|
| Palavras no grafo / arestas | 77.503 / 557.352 (7,19 por palavra) | | |
| Expoente de Zipf nas definições | **1,069** | entre 0,9 e 1,2 | (a) ✅ |
| Núcleo | 16.795 = **21,7%** | entre 5% e 20% | (b) ❌ |
| Core | 15.142 = **90,2%** do núcleo (1.113 componentes; 1.653 palavras em satélites) | ≥ 50% | (c) ✅ |
| MinSet guloso | 3.985 = **5,14%** (3.502 no Core) | entre 0,5% e 5% | (d) ❌ |
| Fecho a partir do MinSet | **77.503 = 100%**, em **53 rodadas** | 100% | (e) ✅ |
| Entropia das letras | **4,213 bits** | entre 4,0 e 4,3 | (f) ✅ |
| Hexspeak | 83 palavras = **0,107%** | < 0,5% | (g) ✅ |
| Profundidade média dos substantivos na taxonomia | **7,96** (máximo 18) | entre 6 e 10 | (h) ✅ |

**A chance de cada acerto (regra da Parte 26).** As previsões que acertaram eram, quase todas, as que um preditor ingênuo também acertaria: Zipf
≈ 1, Core grande, entropia perto de 4,14 são resultados clássicos; o fecho de 100% é um **teorema** (removido um conjunto de retroalimentação, o grafo
fica acíclico e toda palavra se define em ordem topológica). As duas que arriscavam um número do WordNet (núcleo e MinSet) erraram, ambas para cima.

### P375 (0x177). Por que o núcleo e o MinSet saíram maiores?

**Lógica.** Três motivos, cada um com uma conta:
1. **Polissemia somada.** Uma palavra do WordNet tem vários sentidos, e eu juntei as palavras das definições de **todos** eles: "bank" se define por
   palavras de dinheiro **e** de rio. Isso aumenta as arestas (7,19 por palavra) e os ciclos. Um dicionário que separa sentidos teria um grafo
   menor.
2. **Definições curtas e técnicas.** O WordNet define "fabaceae" por nomes de outras plantas; um dicionário para aprendizes (o Longman, usado na
   literatura) define com um vocabulário controlado de ~2.000 palavras. O núcleo de um dicionário de vocabulário controlado é menor **por
   construção**.
3. **O guloso superestima.** O MinSet guloso é uma cota **superior** do mínimo. O mínimo é NP-completo; com 3.985 palavras, o verdadeiro está em
   algum ponto abaixo.

**Meta.** As referências foram medidas em outros dicionários. Eu as usei como se valessem para o WordNet: é a regra da Parte 12 ("o mecanismo é o
mesmo, não só o nome") esquecida de novo.

### P372 (0x174). A ponte: o dicionário em hexadecimal

Aqui a junção é natural, porque as duas coisas se medem em bits.

**Uma palavra em dígitos hex.** Escolher uma palavra entre 77.503 custa
$$
\log_2 77.503 = 16{,}24 \text{ bits} = \frac{16{,}24}{4} = 4{,}06 \text{ dígitos hex}.
$$
O MinSet tem $3.985 = \texttt{0xF91}$ palavras, e escolher uma delas custa $\log_2 3.985 = 11{,}96$ bits, **quase exatamente 3 dígitos hex**. O
núcleo tem $16.795 = \texttt{0x419B}$; o Core, $15.142 = \texttt{0x3B26}$; o grafo inteiro, $77.503 = \texttt{0x12EBF}$.

**Uma letra em dígitos hex.** A entropia das letras é 4,213 bits: $4{,}213/4 = $ **1,053 dígito hex por letra**. Uma letra do inglês carrega um
pouco **mais** que um dígito hex, porque o alfabeto (26) é maior que 16, mas bem menos que os $\log_2 26 / 4 = 1{,}175$ dígitos que caberiam se
todas as letras fossem igualmente prováveis.

**As palavras que são números.** 83 palavras do grafo são escritas só com a–f, e cada uma **é** um número hexadecimal: `0xBEEF` = 48.879,
`0xCAFE` = 51.966, `0xDEAD` = 57.005, `0xFADE` = 64.222, `0xDECADE` = 14.600.926, `0xFACADE` = 16.435.934. A maior é **fabaceae**, a família do
feijão: `0xFABACEAE` = **4.206.546.606**.

**O tamanho do grafo em bits.** Cada aresta aponta para uma de 77.503 palavras (16,24 bits):
$557.352 \times 16{,}24 = 9{,}05$ Mbit $\approx 1{,}13$ MB. É o conteúdo relacional do dicionário, sem os textos das definições; o arquivo
comprimido inteiro tem 4,7 MB.

### P373 (0x175). Como um dicionário pode levar uma IA simples rumo a uma AGI? (o método, com números)

**Na pergunta.** "Tornar uma simples IA em uma ASI AGI" pelo dicionário. A resposta de Harnad: um dicionário **sozinho** não basta (o carrossel).
Com uma **âncora** na percepção, basta muito menos que o dicionário inteiro. O WordNet põe números nisso:

1. **Ancorar 3.985 palavras** (5,1%) pela percepção: é o MinSet. Para a SYNTHAI, "perceber" é o sensor de primeira mão (P225); para uma IA real,
   são as categorias aprendidas de imagens, sons e ações.
2. **Compor o resto por definições:** as outras 73.518 palavras se definem em **53 rodadas** de cadeias de definições, cada rodada usando só
   palavras já conhecidas.
3. **Abstrair pela taxonomia:** cada substantivo está, em média, a 7,96 passos de "entity". Um conceito herda o que sabe dos 8 níveis acima.
4. **Prever pela lei de Zipf** (s = 1,07): as ~100 palavras mais frequentes das definições cobrem uma fração grande dos usos; uma IA que aprende
   bem essas aprende a maior parte do que as definições dizem.

**A conta do esforço.** Ancorar 3.985 palavras pela experiência contra 77.503 é um fator $77.503/3.985 = 19{,}4$ a menos de trabalho de
percepção. O preço é profundidade: 53 rodadas de composição. É a troca de qualquer sistema simbólico ancorado: **pouca percepção, muita
composição**.

**Meta.** Isso não faz uma AGI. Mostra o tamanho do problema de ancoragem **neste** dicionário e a forma de uma solução: um núcleo perceptivo
pequeno e uma máquina de composição. A SYNTHAI tem o primeiro em miniatura (o sensor) e ainda não tem o segundo.

### P374 (0x176). Jung: o dicionário e o inconsciente coletivo

**Tradução cruzada.** Jung chamava de **inconsciente coletivo** a camada da psique que não vem da experiência de cada um, mas da espécie: as formas
herdadas (os arquétipos). Um dicionário é o análogo mais literal que existe numa cultura: um sistema de significados que **nenhum** falante criou e
que todo falante herda. O Core (90% do núcleo, um único componente fortemente conexo) é a parte em que tudo remete a tudo, como Jung descrevia as
imagens arquetípicas, que se definem umas pelas outras. O MinSet é o que precisa **vir de fora**: no vocabulário de Jung, o ponto em que o arquétipo
(a forma) recebe conteúdo da experiência.

**Onde a formalização quebra.** O inconsciente coletivo de Jung é, por hipótese, **anterior** à linguagem; o dicionário é linguagem pura. E os
arquétipos, para Jung, não se definem: só se vivem. O grafo de definições mede o oposto: o que se pode definir. O paralelo ilumina a estrutura e
falha no conteúdo.

### P376 (0x178). Que módulos o dicionário pede para a SYNTHAI?

Três próximos módulos, cada um com uma conta pronta para testar:
1. **Ancoragem:** ligar cada palavra do MinSet a um sinal do mundo da SYNTHAI e medir quantas palavras do resto ela consegue "entender" pelo fecho.
2. **Similaridade conceitual:** a distância na taxonomia (caminho até o ancestral comum) como medida de quão parecidas são duas situações; testar
   se agrupar situações parecidas ajuda a transferir o que ela aprendeu (P194).
3. **Um MinSet menor:** trocar o guloso por um algoritmo exato em subgrafos pequenos (o Core quebrado em blocos) e medir quanto a cota cai.

### P377 (0x179). Capacidades

Continua em **4 de 12**. O item "linguagem natural" ganhou um **data lake** e uma medida do problema de ancoragem, mas a SYNTHAI ainda não usa
palavras para decidir.

### P378 (0x17A). As fontes e a licença do data lake

O WordNet 3.0 é da Universidade de Princeton, com licença que permite usar, copiar, modificar e distribuir mantendo o aviso de copyright. O
arquivo original tem SHA-256 `640db279c949a88f61f851dd54ebbb22d003f8b90b85267042ef85a3781d3a52`; o gerador e a licença estão em `dados/`.

---

# C — Fechamento

### P379 (0x17B). Placar e taxa de erro

| Teste | Resultado |
|---|---|
| P363 (a): Newton < 0 na escolha única (pré-registrado) | ❌ (+0,031) |
| P363 (b): Newton × âncora > 0 na escolha única (pré-registrado) | ✅ (+0,045; ver P369) |
| P363 (c): neutro ≈ 0 na escolha única (pré-registrado) | ✅ |
| P363 (d): âncora entre +0,15 e +0,6 com t ≥ 2 no sequencial (pré-registrado) | ❌ (+0,040) |
| P363 (e): Newton × âncora > 0 no sequencial (pré-registrado) | ✅ (+0,075; ver P369) |
| P363 (f): Thompson entre +0,05 e +0,20 com t ≥ 2 no bandido (pré-registrado) | ✅ (+0,081) |
| P363 (g): Newton < 0 no bandido (pré-registrado) | ✅ (−0,066) |
| P363 (h): neutro ≤ 0 no bandido (pré-registrado) | ✅ |
| P364 (i): 2 dígitos hex sem efeito (pré-registrado) | ❌ |
| P364 (j): 1 dígito hex com o dobro do efeito (pré-registrado) | ❌ |
| P366: o desempate (pré-registrado) | ✅ (+0,230, t 2,78) |
| P371 (a)–(h): o dicionário (pré-registrado) | ✅ ❌ ✅ ❌ ✅ ✅ ✅ ✅ |
| P369: auditoria do meu código (erro de sinal) | ❌ |

Esta parte: **20** testes, **7** errados (o erro de sinal conta como uma afirmação minha errada, a de que a função estava certa). Acumulado:
**90 de 201**. Posterior: média **0,45**, intervalo de 90% **[0,39; 0,51]**.

### P380 (0x17C). Unificação e metacognição

- **Novos módulos:** `hexadecimal.py` (os 16 tipos, Walsh–Hadamard, efeitos fatoriais, quantização) e `dicionario.py` (o WordNet, Morphy, grafo de
  definições, núcleo, Tarjan, MinSet, fecho, Zipf, entropia). **18 testes de unidade novos: 65 no pacote, todos passam**, também a partir do arquivo
  único.
- **Data lake:** `dados/` com o WordNet 3.0 compacto (4,7 MB), o gerador e a licença.
- **Versão principal:** continua a `SynthaiComposta` (o desempate da P366 confirmou; o ganho honesto no sequencial é +0,23).
- `calculos.py`: `p361` a `p366`, `p371`, `p372`; testes de regressão **exatos** em hexadecimal (P361, P365) e P372: **68/68**; **221** funções
  `pNN`. `SYNTHAI_completo.py`: 7,1 MB, com o dicionário em base64.

**Metacognição.**
1. **Duas linguagens, dois tipos de descoberta.** O hexadecimal revelou **formas** (1/450 com os dígitos em ordem, a impressão digital exata). O
   dicionário revelou **tamanhos** (5% de ancoragem, 53 rodadas de composição). Juntá-los só fez sentido onde os dois se medem em bits (P372).
2. **O erro de sinal é o achado mais importante para mim.** Eu tinha testes e eles passavam. O teste era fraco (interação zero) e o código, errado.
   A correção veio de conferir a convenção matemática contra a definição. Regra para o `CLAUDE.md`: um teste de unidade de uma fórmula tem que
   usar um caso em que **todos** os termos da fórmula são diferentes de zero.
3. **O piso do caos muda como leio tudo o que veio antes.** Com desvio ~0,6 por semente, 20 sementes não veem nada abaixo de 0,26. Várias
   conclusões das Partes 23–29 com 10 ou 20 sementes estavam abaixo desse piso. As que resistiram foram as replicadas em lotes novos.

> **Síntese da Parte 30:** em hexadecimal, o limiar da P71 se revelou como 0x1.23456789ABCDF × 2⁻⁹, porque 1/450 = 2⁻⁹ · 256/225 e
> 1/15² = 0x0.0123456789ABCDF…, com o E sumindo num vai-um. A SYNTHAI virou um dígito hex: 16 tipos, 8 efetivos em cada mundo (como os 8 de Jung), e
> um fatorial mostrou que no bandido Thompson ajuda (+0,081) e Newton atrapalha (−0,066), enquanto fora dele os módulos valem em combinação. Um dígito
> hex por peso basta, até onde o caos de decisão deixa ver (nada abaixo de 0,26 com 20 sementes); e o desempate em 60 sementes manteve a composta como
> versão principal, com um ganho honesto de +0,23. O dicionário (WordNet) virou data lake: ancorando 3.985 palavras (5,1%) pela percepção, as outras
> 73.518 se definem em 53 rodadas, que é o tamanho do problema de ancoragem de Harnad neste dicionário. E um erro de sinal no meu próprio código,
> achado ao conferir a convenção, virou uma regra nova.

---

**Fontes pesquisadas nesta parte**
- $1/(b-1)^2$ e o dígito que some: derivação própria pela série $\sum k x^k = x/(1-x)^2$, conferida pelo código em todas as bases de 3 a 16 (`p361_hex_do_limiar`)
- Yates e Walsh–Hadamard em fatoriais $2^k$: [Penn State STAT 503](https://online.stat.psu.edu/stat503/book/export/html/657), [notas de WVU](https://stat.wvu.edu/~ghobbs/stat313/ch06.pdf), [Box (1961)](https://www.math.pku.edu.cn/teachers/yaoy/math112230/Box-1961.pdf)
- Jung, 8 tipos, e o Myers–Briggs, 16: [Friesian](https://friesian.com/types.htm), [Redalyc](https://www.redalyc.org/journal/3589/358951064010/html), [Bay Path, Jung](https://open.baypath.edu/psy321book/chapter/c3p3/)
- Ruído de quantização Δ²/12 e 6 dB por bit: [arXiv 1712.01048](https://arxiv.org/pdf/1712.01048), [arXiv 2102.06365](https://arxiv.org/pdf/2102.06365)
- Pontos flutuantes em hexadecimal (C99, `float.hex`): [GCC, Hex Floats](https://gcc.gnu.org/onlinedocs/gcc-8.3.0/gcc/Hex-Floats.html), [IBM, hexadecimal floating constants](https://www.ibm.com/docs/ssw_ibm_i_72/rzarg/hex_float_constants.htm)
- A estrutura latente dos dicionários: [Vincent-Lamarre et al., arXiv 1411.0129](https://arxiv.org/pdf/1411.0129), [Southampton](https://eprints.soton.ac.uk/370845/), [Harnad et al., arXiv 0806.3710](https://arxiv.org/pdf/0806.3710)
- O problema da ancoragem dos símbolos: [Harnad (1990), notas de Southampton](https://www.southampton.ac.uk/~harnad/Hypermail/Foundations.Cognitive.Science2001/0016.html), [The Vector Grounding Problem, arXiv 2304.01481](https://arxiv.org/pdf/2304.01481)
- Morphy do WordNet: [morphy(7WN)](https://www.mankier.com/7/morphy), [documentação do WordNet 3.0](https://research.cs.wisc.edu/zhu/space2/TTP/nlp/data/WordNet-3.0/doc/html/morphy.7WN.html)
- Entropia das letras (Shannon, 1951): [Shannon 1951 (PDF)](https://sites.socsci.uci.edu/~rfutrell/teaching/itl-davis/readings/shannon1951prediction.pdf), [Stanford](https://cs.stanford.edu/people/eroberts/courses/soco/projects/information-theory/entropy_of_english_9.html)
- WordNet 3.0: [Princeton](https://wordnetcode.princeton.edu/)
