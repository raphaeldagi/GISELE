# Como eu construiria uma AGI/ASI — Parte 81 (0x51): o que não serve

> Continuação da [Parte 80](ASI_AGI_parte80_o_valor_de_um_conjunto.md). **Próxima:** [Parte 82 — o pacote revisado](ASI_AGI_parte82_o_pacote_revisado.md). Pedido do usuário: **"Tire dos nossos trabalhos tudo que não serve pra nada."** Ele contraria a regra antiga "o `calculos.py`
> só cresce; nunca apagar funções antigas", e, por ser o pedido mais recente, vale. O critério, escolhido pela regra mais conservadora (a regra de autonomia) e escrito antes de medir: **sai só o que
> nada usa**, isto é, uma função, classe ou arquivo que nenhum código, teste, rodada ou documento do repositório referencia. **Ficam:** as funções `pNN` (cada número citado nos documentos sai de uma
> delas), os documentos das partes (o registro histórico) e o que for referenciado. Tudo num commit só, reversível pelo git. A mesma mensagem trouxe de novo o relatório do Módulo 007 e o texto do
> Módulo 008 (memória episódica e escore de Brier).

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[3; 7]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[1; 4]** (contagens de código morto podem ser zero)
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,10; 0,90]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,40; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 4]**
- **(m6)** o número de surpresas em **[0; 3]**

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,397; 0,422]** | o estatístico |
| testes de unidade | **[1 + S; 4 + S]** | 1 ou 2 funções novas de auditoria |
| testes do placar | **4 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir; sem calibração possível, por isso largas, e com o fator 1,36 já aplicado)

"Referenciado" = o nome aparece, como palavra inteira, em algum outro lugar do repositório (código, testes, rodadas, documentos, `CLAUDE.md`), fora da própria definição.
- **(a)** funções e classes de primeiro nível do `calculos.py` que não são `pNN` e não são referenciadas em lugar nenhum: **[0; 40]**
- **(b)** funções e classes de primeiro nível dos módulos de `synthai/` (fora os testes) não referenciadas fora do próprio arquivo nem dentro dele: **[0; 30]**
- **(c)** arquivos versionados cujo nome não aparece em nenhum outro arquivo versionado: **[0; 8]**
- **(d)** depois de tirar o que (a), (b) e (c) acharem, a suíte inteira de testes e a regressão completa passam como antes (categórica)

**Medido:** (a) **0** ✅; (b) **0** ✅; (c) **83** ❌ pela letra (o nome literal), mas **0** depois de olhar cada um (`p1872`): 34 rodadas que o `verificar.py` acha por `glob`, 24 saídas que a `rodada29.py` abre por
um nome montado, 24 originais em `dialogo/registro/` citadas pela pasta e este documento (ainda não ligado). (d) **não se aplica**: não havia nada a tirar. **Pelo critério escrito antes, nada no
repositório deixa de servir.** O erro da previsão (c) é o terceiro verificador meu, seguido, que acusa defeitos que não existem (o auditor da Parte 72, a `p1638`, e agora a `p1871`): procurar o
nome escrito não acha o uso por padrão.

## As perguntas desta parte

1. **P1871–P1872 (0x74F–0x750).** O que, no repositório, não serve para nada (nada o usa)? ↩ P1601
2. **P1873 (0x751).** O que, nos textos recebidos (os Módulos 001 a 010 da outra conversa), serve e o que não serve, pelo que as Partes 72 a 80 mediram? ↩ P1608
3. **P1874 (0x752).** O texto do Módulo 008: o que ele acrescenta. ↩ P1812
4. **P1875 (0x753).** Preditiva comigo mesma. **P1876 (0x754).** Engenharia reversa e Jung. **P1899 (0x76B).** Placar. **P1900 (0x76C).** Unificação.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [3; 7] | **3.0000** | ✅ |
| (m2) | [1; 4] | **3.0000** | ✅ |
| (m3) | [0.1; 0.9] | **indefinida (nenhuma faixa numérica: a p1481 não conta as categóricas como faixas)** | ❌ |
| (m4) | [0.4; 1.0] | **0.6667** | ✅ |
| (m5) | [0; 4] | **0.0000** | ✅ |
| (m6) | [0; 3] | **1.0000** | ✅ |

Registradas antes de eu pensar faixa nenhuma do mundo (a ordem que a Parte 70 pediu). **5 de 6** previsões sobre as minhas previsões dentro da faixa.

## As respostas

### P1871–P1872 (0x74F–0x750). O repositório: nada sem uso ✅✅❌

**Na pergunta.** "Não serve pra nada" precisa de uma medida, senão vira gosto. A medida escolhida antes de olhar foi a mais conservadora: **nada o usa**. Ficaram de fora, por regra, as funções `pNN`
(cada número citado nos documentos sai de uma delas, e tirá-las tornaria o número irreproduzível) e os documentos das partes (o registro histórico).

**Lógica.** A `p1871` lê pela árvore sintática cada função e classe de primeiro nível do `calculos.py` e do pacote, e procura o nome como palavra inteira em todos os arquivos versionados (fora a cópia
gerada `SYNTHAI_completo.py`, que contém tudo):
- **(a)** no `calculos.py` (fora as `pNN`, as `_parte_N` e as da unificação): **0** sem uso ✅;
- **(b)** nos módulos de `synthai/`: **0** sem uso ✅;
- **(c)** arquivos cujo nome não aparece em nenhum outro: **83** pela letra ❌, mas **0** depois de olhar um a um (`p1872`). São 34 rodadas que o `verificar.py` acha por `glob`, 24 saídas que a `rodada29.py`
  abre por um nome montado, 24 originais em `dialogo/registro/` citadas pela pasta, e este documento.

**Conclusão: no repositório, não há nada que nada use.** Nada foi tirado, porque tirar o que é usado quebraria o projeto. A única zona cinzenta é `dialogo/registro/` (24 cópias das versões antigas de
rodadas corrigidas). Elas duplicam o que o git já guarda, mas os documentos as citam pelo caminho, e uma delas é aberta por código (`p1751`). Ficam.

**Tradução cruzada.** Um projeto em que tudo é referenciado é como um texto em que toda frase é citada por outra: ele pode ser longo demais, mas não tem frase solta. O que se poderia cortar não é
o que nada usa, e sim o que se usa sem precisar (redundância). Essa é outra medida, que não foi a pedida.

### P1873 (0x751). Os textos recebidos: o que serve e o que não serve

O que as Partes 72 a 80 mediram sobre os Módulos 001 a 010 da outra conversa, peça por peça. "Serve" = a afirmação resistiu a um teste; "não serve" = o teste a desmentiu ou ela não tinha como ser
testada como estava.

| peça do texto | parte | veredito medido | serve? |
|---|---|---|---|
| "redundância de 48,63%" | 72 | medida contra 8 bits; contra o alfabeto, 15% | não |
| "ciclos autorreferentes reais" no dicionário | 72 | 0 de 2 no WordNet | não |
| "hash SHA-256 = pesos" | 72 | o hash não vê sinônimos (z = −0,26) | não |
| "100% de generalização" num grafo de 10 nós | 72 | sem dados não vistos, é memorização | não |
| `SemanticLake` (módulo 001) | 72 | 5 defeitos reais (esquemas misturados, relações não validadas, normalização só em parte) | **corrigido em `synthai/lago.py`** |
| `InferenceEngine` (módulo 002) | 72 | "8 testes" fixos no código (são 7); string lida letra por letra; `deque` sem uso | **a ideia serve; corrigido em `synthai/lago.py`** |
| a otimização "fila com índices" (Horn linear) | 72 | 80 vezes menos trabalho no WordNet inteiro; rodada 46 IGUAL | **serve** |
| prioridade S(q) = U + I + T | 73 | escolhe perguntas que valem 39% das melhores | não; o VOI serve |
| "ganho esperado de informação" para escolher experimentos | 74 | 25% do valor das melhores | não; o VOI serve |
| U(a) = ganho/custo com orçamento | 74 | 0,99 do ótimo quando o ganho é o VOI | **serve, com o VOI** |
| "corrigi a expectativa e confirmei" (7/8 virou 8/8) | 74 | um teste ajustado ao resultado tem informação zero | não |
| o laço de auto-modificação com "prova de Gödel" | 75 | nunca aprova nada (o espaço do JSON); corrigido, para na geração 1; a "prova" aprova 849 de 849 | não |
| embeddings de Kronecker por nibble | 76 | 80 pesos em vez de 544, a +0,079 bit; o ASCII não carrega informação | serve só para economizar pesos |
| a ordem B → A do planejador (módulo 007) | 75 | confere e é ótima (valor 1,22) | **serve** |
| "duas implementações que concordam podem errar juntas" | 72–77 | é o que a reverificação achou (5 rodadas passavam por sorte) | **serve** |
| o diagrama causal Z → X, Z → Y, X → Y (módulo 009) | 79 | a correlação mede o dobro; o ajuste e a intervenção recuperam o efeito | **serve** |
| "confiança declarada contra precisão observada" (módulo 010) | 79 | aplicado a mim: 77,3% contra 90% | **serve** |
| "preservar a previsão original" (módulo 008) | 81 | é a regra de pré-registro deste projeto desde a Parte 17 | **serve** (já existia) |
| escore de Brier (0,065) | 81 | a conta confere: ((0,8 − 1)² + 0,3²)/2 = 0,065 | **serve** |
| as declarações de limites ("não é uma AGI") | 72–81 | corretas em todas as partes | **serve** |

**A destilação.** Do que veio, serve o **método**: pré-registrar, separar correlação de causa, medir a calibração, desconfiar de duas implementações que concordam. Também serve o pouco código que,
corrigido, faz o que diz (o motor de Horn, o lago semântico). Não serve o que **declara resultado sem medida**: as porcentagens, os "✅", os "8/8", a "prova" que aprova tudo, a "segurança máxima".

### P1874 (0x752). O Módulo 008

O texto acrescenta o escore de Brier e a regra "preservar a previsão original e guardar a modificação separadamente". A conta confere, por código: ((0,8 − 1)² + (0,3 − 0)²)/2 = (0,04 + 0,09)/2 =
**0,065**. A regra é a deste projeto desde a Parte 17: cada previsão fica num commit antes da medida, e a "modificação" é uma previsão nova, num mundo novo (como (f) depois do erro de (e) na Parte 74).
O que este projeto ainda não tem e o texto sugere é a cadeia de hashes entre episódios. Aqui o papel dela é feito pelo próprio git: cada commit tem o hash do anterior, e a ordem "previsão antes da
medida" é verificável pelos hashes e pelas datas.

### P1875 (0x753). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 1 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 1)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **14824** | [13039; 22082] | ✅ | [13039; 22082] | ✅ | 22290 | 2736 | 7466 |
| compressão | **0.4072** | [0.3973; 0.4221] | ✅ | [0.3970; 0.4220] | ✅ | 0.4177 | 0.0023 | 0.0105 |
| testes de unidade | **2** | [2.87; 8.63] | ❌ | [2.00; 5.00] | ✅ | 6 | 1.50 | 4.00 |
| testes do placar | **3** | [5.67; 10.33] | ❌ | [4.00; 6.00] | ❌ | 8 | 2.00 | 5.00 |
| erros do placar | **1** | [-0.58; 3.33] | ✅ | [0.00; 3.33] | ✅ | 2 | 0.67 | 1.00 |
| redundância P821 | **0.6311** | [0.5631; 0.6510] | ✅ | [0.5630; 0.6510] | ✅ | 0.5877 | 0.0241 | 0.0433 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 4 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 6 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 71"):** mais perto do medido em **6 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **13093**, compressão **0.4138**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 1 de 1 erros.
- **Erros de processo nesta parte:** 1 (os testes da p1871 e da p1872 liam o estado vivo do projeto (a regra da Parte 48) e quebraram quando ele mudou; trocados por casos de controle fixos).

### P1876 (0x754). Engenharia reversa e Jung

**O padrão que se repetiu: o verificador que acusa sem olhar.** A `p1871` acusou 83 arquivos e todos eram usados (por `glob`, por nome montado, pela pasta). É a terceira vez seguida (o auditor da Parte 72,
a `p1638`, e agora esta). **O significado:** eu escrevo verificadores a partir da forma mais simples do uso (o nome escrito), e o uso real tem mais formas. **Regra (aplicada aqui):** um verificador sai
com um teste de controle dos dois lados no mesmo commit, e os acusados passam por uma segunda função que explica cada um antes de qualquer remoção (`p1872`).

**O pedido e o critério.** "Tire tudo que não serve" pedia uma medida; a mais conservadora achou zero. A engenharia reversa disso: o que parece inútil num projeto grande raramente é o que nada usa; é o
que se usa sem precisar (redundância), e essa é uma medida diferente, que não foi a pedida e não foi feita.

**Jung: a sombra do arquivo.** O que "não serve" num projeto é a sombra dele: o que está lá e ninguém olha. **Onde a formalização funciona:** "ninguém olha" virou "nenhum nome o cita", e a busca achou
que tudo é citado. **Onde quebra:** em Jung, a sombra também é o que se usa sem saber; aqui, os 83 arquivos eram usados sem que o nome deles aparecesse, e só olhar um por um mostrou o uso.

### O diálogo

Sem rodada nova nesta parte. Placar por voz da função `p1241_placar_por_voz(49)`: IA-Python 25 em 39; IA-Java 21 em 38 (regra estrita, rodadas 13 a 49).

### P1899 (0x76B). Placar

Do mundo: (a) ✅ (b) ✅ (c) ❌. Parte 81: **3 testes, 1 erros**. Acumulado (mundo): **202 erros em 660 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 2 pNN novas sem teste ✅. Sobre mim (placar separado): **6 de 7** dentro da faixa condicional; sobre as minhas previsões, 5 de 6; o estatístico, 4 de 6; e 1 erros de processo (P1335).

### P1900 (0x76C). Unificação

- **Novo:** `p1871` (o que nada usa), `p1872` (os acusados, olhados um a um, com um caso de controle de cada lado no teste). **Nada foi tirado.**

> **Síntese da Parte 81:** pelo critério escrito antes (sai só o que nada usa), nada no repositório deixa de servir: 0 funções, 0 classes, 0 arquivos sem uso, depois de olhar um a um os 83 arquivos que a busca pelo nome acusou (todos usados por padrão, por nome montado ou pela pasta). Nada foi tirado. Dos textos recebidos (Módulos 001 a 010), serve o método (pré-registrar, separar correlação de causa, medir a calibração, desconfiar de duas implementações que concordam) e o código que, corrigido, faz o que diz; não serve o que declara resultado sem medida.

---

**Fontes desta parte**
- G. W. Brier, "Verification of forecasts expressed in terms of probability", *Monthly Weather Review* 78 (1950)
- Git como cadeia de hashes: [Git Internals — Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)
