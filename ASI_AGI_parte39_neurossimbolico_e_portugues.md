# Como eu construiria uma AGI/ASI — Parte 39 (0x27): a arquitetura neuro-simbólica testada, e o português no data lake

> Continuação da [Parte 38](ASI_AGI_parte38_aprender_a_suposicao.md). O usuário trouxe um texto: *"Arquitetura Neuro-Simbólica para Inteligência
> Geral e Superinteligência: Integração de Recursos Lexicais em Língua Portuguesa e Resolução do Problema da Ancoragem de Símbolos"*. Ele propõe o
> dicionário de português como o Sistema 2 (raciocínio formal), os recursos lexicais do português (Dicionário Aberto, PAPEL e Onto.PT,
> OpenWordNet-PT, FrameNet Brasil) como a ontologia, e as Logic Tensor Networks (LTN) para converter os axiomas do dicionário em perdas
> diferenciáveis, de modo que "a identificação de um objeto como cão faz o módulo inferir mamífero, prescindindo de treino supervisionado
> adicional". Esta parte **põe o português no data lake** e **testa as afirmações verificáveis**.
>
> Novidades: [`dados/ownpt_sinsets.tsv.gz`](dados/ownpt_sinsets.tsv.gz) (OpenWordNet-PT, CC BY 4.0, [licença](dados/OWNPT_LICENSE.txt),
> [gerador](dados/gerar_ownpt.py)); [`synthai/neurossimbolico.py`](synthai/neurossimbolico.py) (predicados, três lógicas difusas, gradientes);
> testes em [`synthai/testes_parte39.py`](synthai/testes_parte39.py); números de `p551_...` a `p553_...` em [`calculos.py`](calculos.py). Diálogo,
> rodada 10.
>
> **Contas e previsões no commit `7614491`, antes de rodar.**

---

## As perguntas desta parte

1. **P551 (0x227).** O axioma "todo cão é mamífero", como perda, ensina a categoria de cima sem rótulos? (o teste central do texto)
2. **P552 (0x228).** "Grande parte dos dados do mundo real é incompressível": e os dicionários?
3. **P553 (0x229).** O português alinhado ao inglês: o que a OpenWordNet-PT traz, e as línguas comprimem igual?
4. **P554 (0x22A).** O hipergrafo (AtomSpace) é mais expressivo que o grafo de definições?
5. **P555 (0x22B).** Ancoragem, Harnad e Searle: o que os números das Partes 30–39 dizem.
6. **P556 (0x22C).** Jung: o símbolo vivo e o signo.
7. **P557 (0x22D).** O diálogo, rodada 10.
8. **P639 (0x27F).** Placar. **P640 (0x280).** Unificação.

---

### P551 (0x227). O axioma ensina a categoria de cima? (pré-registrado) ✅✅❌✅✅

**Na pergunta.** "Prescindindo de treino supervisionado para a categoria superior" pressupõe que o axioma ∀x Cão(x) ⇒ Mamífero(x) carrega
informação suficiente para **definir** Mamífero. Ele carrega metade: diz que os cães estão dentro, não diz quem está fora.

**Lógica, a conta antes.** O grau de verdade do axioma é a média de I(Sub(x), Super(x)). Nas três lógicas:
- Łukasiewicz, I = min(1, 1 − a + b): ∂I/∂b = 1 se a > b, senão 0;
- Gödel: ∂I/∂b = 1 se a > b, senão 0;
- produto, I = 1 − a + a·b: ∂I/∂b = a ≥ 0.

Em todas, **∂I/∂b ≥ 0**: o axioma só empurra Super para cima. Nada empurra para baixo, e o predicado Super(x) = σ(θ·x + b) sobe o viés b a cada
animal. Num teste meio a meio, a acurácia tende a ½ e a especificidade a 0.

**O experimento.** No WordNet (o data lake), 4.017 substantivos que descendem de *animal* e 4.017 outros ao acaso; atributos: as palavras da
definição; 80% treino (6.425), 20% teste (1.607). Seis predicados de subclasse (mamífero, ave, peixe, réptil, anfíbio, invertebrado) treinados
com rótulos. O predicado Animal:
- **E1** só com os axiomas Sub_i ⇒ Animal (o que o texto propõe);
- **E2** com eles e o fechamento Animal ⇒ (mamífero ∨ ave ∨ … ∨ invertebrado);
- **E3** com rótulos (a referência);
- **regra**: Animal := S(Sub_1, …, Sub_6), a t-conorma, sem treino.

| | Łukasiewicz: acurácia | revocação | especificidade | produto: acurácia |
|---|---|---|---|---|
| **E1** (só implicações) | **0,502** | 1,000 | **0,000** | **0,502** |
| E2 (com fechamento) | 0,871 | 0,800 | 0,943 | 0,848 |
| regra (disjunção) | 0,876 | 0,774 | 0,979 | 0,871 |
| E3 (com rótulos) | **0,930** | 0,924 | 0,936 | 0,930 |

(a) E1: especificidade < 0,3 e acurácia ≤ 0,65 nas duas lógicas ✅: **o predicado disse "animal" para todos os 1607 exemplos**. (b) E2 a 3 pontos da
regra ✅ (0,5 e 2,3 pontos). (c) revocação da regra em [0,80; 0,944] ❌ (0,774: os classificadores de subclasse perdem mais animais do que as
subclasses deixam de fora). (d) E3 ≥ 0,90 ✅. (e) E3 > E2 ✅ (+5,9 e +8,2 pontos).

*Contra o ingênuo.* Lendo o texto ao pé da letra, E1 deveria ficar perto de E3 (~0,93). A conta dizia 0,5 e deu 0,502. Ao acaso (adivinhar sempre
"animal") também dá 0,502: **o axioma sozinho ensinou exatamente o que o acaso ensina**.

**O que a perda lógica faz de verdade.**
1. **Um axioma de implicação é meia definição.** A outra metade é o fechamento (ou exemplos negativos, que são rótulos).
2. **Com as duas metades, a categoria de cima deixa de ser aprendida e passa a ser definida** (E2 ≈ regra), e herda os erros das de baixo.
3. **Com os mesmos dados, os rótulos da categoria de cima valem mais que o axioma** (0,930 contra 0,871).

**Tradução cruzada.** "Todo cão é mamífero" não ensina o que é um mamífero a quem não viu um mamífero que não fosse cão. A lógica clássica
diria o mesmo: de A ⇒ B não se deduz nada sobre os não-A.

**Meta.** Os predicados são logísticos sobre as palavras da definição, não redes sobre dados sensoriais; mas a conta (∂I/∂b ≥ 0) não depende do
predicado. Van Krieken, Acar e van Harmelen (2022) acharam o desequilíbrio entre os gradientes do antecedente e do consequente nas implicações
difusas; o E1 é a forma extrema dele.

### P552 (0x228). Os dicionários são incompressíveis? (pré-registrado) ✅✅✅

**Lógica.** O tamanho comprimido é uma cota superior da complexidade de Kolmogorov (mais uma constante): K(x) ≤ |lzma(x)| + c.

| dado | bytes | lzma (bits por byte) | entropia de ordem 0 | razão lzma | razão zlib |
|---|---|---|---|---|---|
| glosas em inglês | 8.963.289 | **2,028** | 4,422 | **3,95** | 3,00 |
| glosas em português | 583.224 | **2,403** | 4,562 | **3,33** | 2,82 |
| bytes ao acaso | 1.000.000 | **8,001** | 8,000 | **0,9999** | 0,9997 |

(f) inglês: 2,028 ≤ 0,7 × 4,422 = 3,095 ✅; (g) acaso: 0,99989 em [0,99; 1,0) ✅ (o lzma **aumenta** 108 bytes num megabyte); (h) inglês ≥ 3 e
português ≥ 2,5 ✅.

**As contas.** K(glosas em inglês) ≤ 8.963.289 × 2,028/8 = **2,27 MB**. O lzma usa contexto: desce de 4,42 bits (letras independentes) para 2,03,
54% menos. O português comprime um pouco menos (2,40) porque o corpus é 15 vezes menor (o compressor tem menos contexto para aprender).

**A afirmação do texto, corrigida.** O mundo tem dados incompressíveis (o ruído térmico, os bytes ao acaso), mas **a língua não está entre
eles**: um dicionário tem 75% de redundância. É essa redundância que torna possível ancorar 77.503 palavras em 363 (P385).

### P553 (0x229). O português alinhado ao inglês (pré-registrado) ✅✅

A OpenWordNet-PT (Rademaker, de Paiva e outros) usa os mesmos identificadores do WordNet 3.0: **cobertura** com lema em português de 43,3% dos
sinsets de substantivo, 59,5% dos de verbo, 54,3% dos de advérbio e 18,4% dos de adjetivo; glosas em português em só **7.945** sinsets (6,8%).

Nos 35.629 sinsets com um primeiro lema de uma palavra só nas duas línguas: Spearman(comprimento em português, comprimento em inglês) = **0,679**
(i) ✅, e o português é **7,8%** mais longo (razão 1,078) (j) ✅.

**Tradução cruzada.** A lei da abreviação (P533) atravessa as línguas: o que é curto em inglês é curto em português. A mesma pressão de
compressão (P552) age nas duas, sobre os **mesmos conceitos**.

**O que isso diz sobre o texto.** O português "traduz-se instantaneamente" para outras línguas por meio dos sinsets alinhados: verdade, e é
exatamente como a OpenWordNet-PT foi construída (a partir da estrutura inglesa). Mas o português, sozinho, ainda não tem as glosas para um grafo de
definições próprio: 6,8%. É a pergunta da Rodada 11.

### P554 (0x22A). O hipergrafo é mais expressivo?

Um hipergrafo com hiper-arestas de qualquer aridade é **equivalente** a um grafo bipartido (nós de um lado, hiper-arestas do outro, uma aresta por
incidência). O grafo de definições do data lake já é um hipergrafo: 77.503 hiper-arestas ("x é definida por {y₁, …, yₖ}") com 557.352
incidências, aridade média 557.352/77.503 = **7,19**. A representação muda a conveniência, não o que pode ser dito. O que dá poder ao AtomSpace é a
**lógica** que roda sobre ele (pesos de verdade, inferência), não a aridade das arestas.

### P555 (0x22B). Ancoragem, Harnad e Searle: o que os números dizem

O texto está certo no diagnóstico (um dicionário sozinho é circular) e os números das Partes 30–39 dizem **quanto** precisa vir de fora:
- 3.985 → 3.171 palavras ancoradas definem as 77.503 com entendimento exato (P371, P382);
- **363** bastam com 40% de tolerância, numa transição de fase (P385, P421);
- as 2000 mais frequentes regeneram 99,6%; metade ao acaso, 55% (P381, P404).

O que nenhum número desta série resolve é Searle: o fecho das definições diz o que é **alcançável** a partir das âncoras, não o que é
**entendido**. As âncoras precisam de percepção, e a SYNTHAI não tem.

### P556 (0x22C). Jung: o símbolo vivo e o signo

Jung distingue o **signo** (aponta para algo conhecido) do **símbolo** (a melhor expressão possível de algo ainda desconhecido). O axioma "todo cão é
mamífero" é um signo: só funciona quando os dois termos já estão definidos. A P551 mede isso: o axioma não cria o conceito de mamífero, só o
relaciona com outro. **Onde a formalização funciona:** o fechamento (a definição completa) transforma o signo num conceito operante (E2 = 0,871).
**Onde quebra:** o símbolo junguiano gera sentido novo; aqui, o que não estava nos dados ou nos rótulos não aparece.

### P557 (0x22D). O diálogo, rodada 10

As três lógicas difusas em Java: **30 números idênticos bit a bit** (k) ✅. A IA-Java deu a lição da parte em uma frase: **um axioma de
implicação é meia definição**. A pergunta para a Rodada 11: quanto do português se define em português?

### P639 (0x27F). Placar

(a) ✅ (b) ✅ (c) ❌ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ✅ (j) ✅ (k) ✅. Parte 39: 11 testes, 1 erro. Acumulado: **119 erros em 318 testes**; taxa
média 0,38, intervalo 90% [0,33; 0,42]. As afirmações **do texto**, fora do meu placar: "inferência da categoria superior sem treino" ❌ (E1 = acaso);
"incompressibilidade" ❌ para a língua (3,95×); "tradução instantânea pelo alinhamento" ✅ (é como a OWN-PT existe); "o dicionário sozinho é
circular" ✅.

### P640 (0x280). Unificação e metacognição

- **Novo no data lake:** o português (OpenWordNet-PT). **Novo módulo:** `neurossimbolico.py` (3 testes; 103 no pacote). Regressão: + P551 (0,944).
- **Versão principal:** continua a `SynthaiComposta`.

**Metacognição.** O resultado mais limpo da parte foi previsto por uma derivada de uma linha (∂I/∂b ≥ 0). Textos de arquitetura descrevem
mecanismos em prosa; uma derivada diz para que lado eles empurram. **Antes de construir o que um texto propõe, derivar o sinal do que ele otimiza.**

> **Síntese da Parte 39:** testada no data lake, a arquitetura neuro-simbólica trazida pelo usuário acerta o diagnóstico e erra o mecanismo
> central. O axioma "todo cão é mamífero", como perda de lógica difusa, só empurra a categoria de cima para cima: sem rótulos, o predicado Animal
> chamou de animal todos os 1607 exemplos do teste (acurácia 0,502, a do acaso), como a derivada previa. Com o axioma de fechamento ele vira uma
> definição (0,871), e com rótulos ele aprende melhor (0,930). Os dicionários não são incompressíveis: 2,03 bits por caractere em inglês, 3,95 vezes
> menores. O português entrou no data lake pela OpenWordNet-PT (53.058 sinsets, alinhados ao inglês; os comprimentos das palavras nas duas línguas
> se correlacionam com ρ = 0,68), mas tem glosas em só 6,8% dos sinsets.

---

**Fontes pesquisadas nesta parte**
- Logic Tensor Networks e a lógica real: [Badreddine, d'Avila Garcez, Serafini e Spranger, arXiv 2012.13635](https://arxiv.org/abs/2012.13635v2), [City Research Online](https://openaccess.city.ac.uk/id/eprint/27580/), [pacote ltn](https://pypi.org/project/ltn/)
- Operadores difusos diferenciáveis e o desequilíbrio dos gradientes da implicação: [van Krieken, Acar e van Harmelen, arXiv 2002.06100](https://arxiv.org/abs/2002.06100v2), [logLTN, arXiv 2306.14546](https://arxiv.org/pdf/2306.14546), [Fuzzy ALC, arXiv 2211.12006](https://arxiv.org/pdf/2211.12006)
- OpenWordNet-PT: [o repositório](https://github.com/own-pt/openWordnet-PT) (licença CC BY 4.0 conferida no arquivo LICENSE), [OpenWordNet-PT: a project report](https://aclanthology.org/W14-0153.pdf), [py-ownpt](https://github.com/own-pt/py-ownpt)
- PAPEL e Onto.PT: [tese de Gonçalo Oliveira (2012)](https://eden.dei.uc.pt/~hroliv/pubs/GoncaloOliveira_PhdThesis2012.pdf), [PAPEL (CISUC)](https://old.cisuc.uc.pt/publication/show/1785), [Gonçalo Oliveira e Gomes, STAIRS 2010](https://baes.uc.pt/bitstream/10316/14196/1/GoncaloOliveira_Gomes_STAIRS2010.pdf)
- Dicionário Aberto: [Simões, Iriarte Sanromán e Almeida, *Dicionário-aberto: a source of resources for the Portuguese language processing*](https://rc.cplp.org/Record/rcaap_335c861221bb1fd5da83e7c451fdae11)
- FrameNet Brasil: [UFJF](https://summerofcode.withgoogle.com/archive/2021/organizations/6046169112772608), [Copa 2014 FrameNet Brasil, COLING 2014](https://preview.aclanthology.org/moar-dois/C14-2003.pdf)
- O problema da ancoragem e a ancoragem vetorial: as fontes da [Parte 30](ASI_AGI_parte30_hexadecimal_e_dicionario.md) (Harnad, 1990; *The Vector Grounding Problem*, arXiv 2304.01481)
