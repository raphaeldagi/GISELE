# Como eu construiria uma AGI/ASI — Parte 76 (0x4C): a forma do byte

> Continuação da [Parte 75](ASI_AGI_parte75_o_que_se_prova.md). **Próxima:** [Parte 77 — as duas abertas](ASI_AGI_parte77_as_duas_abertas.md) (P1751–P1780). A Parte 75 deixou uma pergunta medível, tirada do texto recebido: o embedding de um caractere como o produto de Kronecker de
> dois fatores, um para cada nibble do byte (W₁[b ≫ 4] ⊗ W₂[b & 0x0F]), serve para a forma de GPT deste projeto? Pedido do usuário, gravado no `CLAUDE.md`: **"Continue sem parar."**

## Previsões sobre as minhas previsões desta parte (num commit só delas, antes de pensar qualquer faixa)

- **(m1)** o número de previsões do mundo em **[3; 8]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]** (uma diferença de bits entre dois modelos pode ter qualquer sinal)
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,02; 0,40]**
- **(m4)** a fração de acertos do mundo em **[0,40; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**
- **(m6)** o número de surpresas em **[0; 2]**

## Previsões sobre mim (placar separado), antes de escrever

Planejadas: ~4 previsões do mundo, ~3 funções novas e um módulo novo no pacote (`synthai/gpt_kronecker.py`).

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,397; 0,422]** | o estatístico |
| testes de unidade | **[4 + S; 7 + S]** | 3 funções e o módulo |
| testes do placar | **4 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de treinar no inglês)

**O teste.** Dois GPTs iguais em tudo (d = 16, T = 16, h = 32, 2.000 passos, taxa 0,005), um com a tabela de embeddings cheia (34 × 16 = 544 pesos) e outro com o embedding de Kronecker por nibble
(d₁ = d₂ = 4; os 4 nibbles altos e os 16 baixos do vocabulário usam 4·4 + 16·4 = **80** pesos), nas mesmas sementes. A medida: bits por caractere no teste (300 janelas); a diferença Kronecker − cheio.
**O mecanismo:** caracteres com o mesmo nibble alto (as letras de *a* a *o* são todas 0x6_) compartilham o fator A, e cada embedding, visto como matriz 4 × 4, tem posto 1. Isso tira liberdade.
**Está presente na calibração?** Sim: o português sem acentos usa o mesmo alfabeto `VOCAB_GPT`.
**Calibração, pela regra escrita antes (o português, sementes 76 a 79, pareadas):** diferenças +0,0712, +0,0287, +0,0619, +0,0812; média **+0,0608**, desvio 0,0228. A faixa para a média de 4 sementes
novas pareadas é a média ± t₃ · desvio · √(1/4 + 1/4), com t₃ = 2,353.
- **(a)** a diferença média (Kronecker − cheio) no inglês, sementes 76 a 79, em **[+0,0229; +0,0986]** bit
- **(b)** o número de sementes (de 4) em que o Kronecker perde em **[3; 4]** (perdeu em 4 de 4 na calibração; dois casos não fixam um sinal, quatro fixam pouco, por isso 3 entra)

**Medido (a) e (b), logo depois do registro:** diferenças no inglês +0,1029, +0,0689, +0,0685, +0,0751; média **+0,0788** ✅; o Kronecker perde em **4 de 4** ✅.

**Previsão nova (o controle do mecanismo), registrada antes de treinar.** A perda pode vir de ter menos pesos (80 contra 544) ou da estrutura dos nibbles ASCII (as letras de *a* a *o* compartilham
um fator, as de *p* a *z* outro). O controle separa as duas: o mesmo Kronecker com os caracteres **embaralhados entre os mesmos 34 bytes** (uma permutação com a semente 1.000 + semente). Os nibbles
usados e o número de pesos ficam iguais, e só muda quem compartilha fator com quem. **A conta:** a ordem ASCII foi escolhida para máquinas de escrever e telégrafos, não pela estatística do inglês, e
por isso não deve carregar informação sobre quais letras se parecem. O desvio de uma diferença pareada entre dois Kronecker vem do mesmo ruído de semente da calibração (0,0228).
- **(c)** a diferença média (embaralhado − ASCII), no inglês, sementes 76 a 79, em **[−0,038; +0,038]** bit (0 ± 2,353 · 0,0228 · √(1/4 + 1/4))

**Medido (c):** embaralhado − ASCII = −0,0105, +0,0103, +0,0236, −0,0312; média **−0,0020** ✅. A ordem ASCII não carrega informação sobre o inglês: o que custa os 0,08 bit é a restrição em si (80
pesos, posto 1 por caractere), e não quais letras compartilham fator.

**A fronteira da Parte 52, auditada de novo (`p1722`, as duas linguagens).** A auditoria nova acha, além das já corrigidas: as rodadas 06 e 20 (o log da biblioteca nos dois lados), 09 e 14 (o log
da biblioteca no Java, e no Python dentro de `synthai/decisao.py` e da `p732`, peças que as regras do projeto não deixam editar) e a 48 (só na preparação: sem risco). Registrada antes de corrigir
a 06 e a 20 (o `log_` de `dialogo/exatas.py` nos dois lados, as originais em `dialogo/registro/`):
- **(d)** a 06 e a 20 dão IGUAIS, e a `p1722` passa a listar só a 09, a 14 (com o Python vazio, porque o log está fora do arquivo da rodada) e a 48 (só na preparação) (categórica)

## As perguntas desta parte

1. **P1721 (0x6B9).** O embedding de Kronecker por nibble (a ideia do texto recebido na Parte 75) serve para a forma de GPT deste projeto? Quanto custa, e de onde vem o custo? ↩ P1695
2. **P1722 (0x6BA).** A fronteira da Parte 52, auditada de novo nas duas linguagens: que rodadas ainda passam por sorte? ↩ P1638
3. **P1723 (0x6BB).** Preditiva comigo mesma. **P1724 (0x6BC).** Engenharia reversa e Jung. **P1749 (0x6CD).** Placar. **P1750 (0x6CE).** Unificação.

## Sobre as minhas previsões desta parte (prever o previsto)

| previsão | faixa | medido | veredito |
|---|---|---|---|
| (m1) | [3; 8] | **4.0000** | ✅ |
| (m2) | [0; 3] | **1.0000** | ✅ |
| (m3) | [0.02; 0.4] | **0.3830** | ✅ |
| (m4) | [0.4; 1.0] | **1.0000** | ✅ |
| (m5) | [0; 2] | **1.0000** | ✅ |
| (m6) | [0; 2] | **0.0000** | ✅ |

Registradas antes de eu pensar faixa nenhuma do mundo (a ordem que a Parte 70 pediu). **6 de 6** previsões sobre as minhas previsões dentro da faixa.

## As respostas

### P1721 (0x6B9). A forma do byte ✅✅✅

**Na pergunta.** "Serve?" tem duas metades. A primeira é o preço: quantos bits por caractere o modelo perde com a restrição. A segunda é a causa: a perda vem de ter menos pesos, ou da estrutura
ASCII que a restrição impõe (letras com o mesmo nibble alto compartilham um fator)? O controle separa as duas.

**Lógica (álgebra).** O embedding do caractere de byte b é E[b] = A[b ≫ 4] ⊗ B[b & 0x0F], com A ∈ ℝ^{16×4} e B ∈ ℝ^{16×4}, e d = 4 · 4 = 16.
- **Os pesos, com a substituição:** os nibbles altos do vocabulário são 4 (0x2_, 0x3_, 0x6_, 0x7_) e os baixos são os 16; os embeddings usam 4 · 4 + 16 · 4 = **80** pesos, contra 34 · 16 = **544** da
  tabela cheia (6,8 vezes menos).
- **O gradiente, à mão:** ∂L/∂A[h][i] = Σ_c [alto(c) = h] Σ_j ∂L/∂E[c][4i + j] · B[baixo(c)][j], e o simétrico para B. Conferido por diferenças finitas em três coordenadas, até a 9ª casa
  (`synthai/testes_parte76.py`).
- **A geometria:** cada embedding, visto como uma matriz 4 × 4, tem posto 1. Os 34 pontos de ℝ¹⁶ vivem na variedade de Segre (dimensão 4 + 4 − 1 = 7), e não no espaço inteiro.

**A medida, com a calibração antes.**
- **Calibração no português (sementes 76 a 79):** diferença Kronecker − cheio de +0,0711, +0,0288, +0,0619 e +0,0812 bit.
- **Teste no inglês, nas mesmas sementes:** +0,1029, +0,0689, +0,0685, +0,0751; média **+0,0788** (a) ✅ [+0,0229; +0,0986]. O Kronecker perde em **4 de 4** sementes (b) ✅.
- **O controle:** o Kronecker com os 34 caracteres embaralhados entre os mesmos 34 bytes. A diferença média (embaralhado − ASCII) é **−0,0020** (c) ✅ [−0,038; +0,038].

**Conclusão: a ordem ASCII não carrega informação sobre o inglês.** O custo de 0,08 bit vem da restrição em si (menos pesos, posto 1), não de quais letras ficam juntas. Isso tem uma
consequência prática para a ideia do texto: os embeddings de Kronecker economizam pesos (464 aqui), mas não "ligam o significado à representação numérica", como ele dizia. A
estrutura do byte é arbitrária para a língua, e o modelo paga para desfazê-la.

**Tradução cruzada.** O código ASCII é como um sobrenome: diz de que família tipográfica um caractere vem (maiúscula, minúscula, pontuação), e não como ele se comporta numa frase. Forçar os
parentes a compartilhar traços (o fator comum) custa caro quando o parentesco não tem nada a ver com o comportamento.

**Meta.** Com d = 16 e 2.000 passos, os modelos são pequenos. Num modelo com muito mais pesos do que dados, a economia de 464 pesos poderia virar regularização e ganhar; isto não foi testado
aqui. Quatro sementes por língua são um lote só por condição: a conclusão "o custo é a restrição, não o ASCII" vale para este tamanho de modelo.

### P1722 (0x6BA). As rodadas que ainda passavam por sorte ✅

**Na pergunta.** A Parte 73 corrigiu as rodadas que a `p1638` acusou, e a reverificação mostrou que a `p1638` era cega: só olhava o Python, e só a forma `math.log`. A pergunta é o que um
verificador melhor acha.

**Lógica.** A `p1722` lê, pela árvore sintática, as chamadas no Python (`math.X` e os nomes importados de `math`) e, por expressão regular, as do Java (`Math.X`, `StrictMath.X`), e marca o caso
em que o Python só usa a biblioteca dentro de `preparar` (os valores vão para um arquivo que o Java lê: sem risco entre as linguagens). Ela achou:
- **06 e 20:** o log da biblioteca nos dois lados. Corrigidas com o `log_` de `dialogo/exatas.py`; IGUAIS (51 e 73 linhas) (d) ✅.
- **09 e 14:** o log da biblioteca no Java, e no Python dentro de peças que as regras do projeto não deixam editar (`synthai/decisao.py`, medido pela P285; a `p732`, medida). Ficam abertas: a
  correção é reescrever o lado Python da rodada com funções exatas próprias.
- **48:** só na preparação, sem risco.

**O balanço da fronteira** (contado na lista acima e na da Parte 73): de 48 rodadas, 14 usavam a biblioteca em algum lado. Em 12 havia risco entre as linguagens: 10 corrigidas (06, 18, 19, 20,
21, 22, 23, 24, 25 e a cópia Java da 26) e 2 abertas (09, 14). Nas outras 2, o Java não usa a biblioteca (a 30, trocada também, e a 48, só na preparação).

**Tradução cruzada.** Um exame que só olha um lado de uma conversa acha só metade dos mal-entendidos.

### P1723 (0x6BB). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 0)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **16195** | [13039; 22082] | ✅ | [13039; 22082] | ✅ | 22290 | 1366 | 6095 |
| compressão | **0.4045** | [0.3973; 0.4221] | ✅ | [0.3970; 0.4220] | ✅ | 0.4177 | 0.0050 | 0.0132 |
| testes de unidade | **6** | [2.87; 8.63] | ✅ | [4.00; 7.00] | ✅ | 6 | 0.50 | 0.00 |
| testes do placar | **4** | [5.67; 10.33] | ❌ | [3.00; 5.00] | ✅ | 8 | 0.00 | 4.00 |
| erros do placar | **0** | [-0.58; 3.33] | ✅ | [0.00; 3.33] | ✅ | 2 | 1.67 | 2.00 |
| redundância P821 | **0.6139** | [0.5631; 0.6510] | ✅ | [0.5630; 0.6510] | ✅ | 0.5877 | 0.0069 | 0.0262 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 5 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 7 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 71"):** mais perto do medido em **5 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **14534**, compressão **0.4105**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 0 erros.
- **Erros de processo nesta parte:** 1 (escrevi "12 rodadas" para uma lista de 14; contado e corrigido antes do commit).

### P1724 (0x6BC). Engenharia reversa e Jung

**O padrão que se repetiu: o que em Python se herda por import, em Java se copia.** Corrigi o idf da rodada 21 nas duas linguagens, e o Python da 26 recebeu a correção de graça (ele importa a 21);
o Java da 26 tinha uma cópia própria do mesmo cálculo e ficou como estava. A mesma assimetria explica por que a `p1638` só via um lado: eu penso nas rodadas pelo Python, onde está a lógica que
importa, e o Java aparece como "a tradução". **O significado:** a minha imagem do diálogo é assimétrica (Python é a fonte, Java é a cópia), e as cópias são exatamente onde as correções não chegam.
**Regra:** uma correção numa rodada vem com uma busca pelo mesmo cálculo em todos os arquivos das duas linguagens (o `grep` pelo nome da função da biblioteca nos `.java`), no mesmo commit.

**O segundo: o verificador sem controle, terceira vez seguida.** O meu auditor da Parte 72 (a Parte 1), a `p1638` (só um lado) e, apontado por mim no texto recebido, o "provador de Gödel"
(aprova tudo). A regra da Parte 75 (um defeito plantado que o verificador tem de achar) foi escrita depois da `p1638`. **Aplicada agora:** o teste da `p1722` confere que ela acha a 48 e só a
preparação dela; e a própria `p1722` foi conferida contra a lista que o `grep` deu antes (06, 09, 14, 20).

**O que funcionou: a calibração perto do teste.** As três previsões do Kronecker acertaram, porque a calibração (o português) tinha o mesmo alfabeto, o mesmo tamanho de modelo e as mesmas
sementes do teste (o inglês): as regras das Partes 63 a 65 juntas.

**Jung: o duplo.** A cópia Java da rodada 26 é um duplo (o *Doppelgänger*): igual ao original em tudo, menos na correção que o original recebeu. **Onde a formalização funciona:** um duplo se acha
comparando, e a comparação bit a bit achou o desvio em 4 ulps. **Onde quebra:** em Jung, o duplo é uma figura do inconsciente que pede integração; aqui, a "integração" é apagar a duplicação
(as duas linguagens chamando o mesmo cálculo descrito uma vez), o que o diálogo não pode fazer, porque a tradução bit a bit é justamente o que ele testa.

### O diálogo

Sem rodada nova: as correções das rodadas 06 e 20 foram a tradução desta parte (o mesmo `log_` nas duas línguas). Placar por voz da função `p1241_placar_por_voz(48)`: IA-Python 25 em 39; IA-Java 21 em 38 (regra estrita, rodadas 13 a 48).

### P1749 (0x6CD). Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅. Parte 76: **4 testes, 0 erros**. Acumulado (mundo): **201 erros em 636 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 2 pNN novas sem teste ✅. Sobre mim (placar separado): **7 de 7** dentro da faixa condicional; sobre as minhas previsões, 6 de 6; o estatístico, 5 de 6; e 1 erros de processo (P1335).

### P1750 (0x6CE). Unificação

- **Novo:** `synthai/gpt_kronecker.py` (a forma de GPT com embeddings de Kronecker por nibble, com o gradiente à mão), `p1721` (Kronecker contra cheio, e o controle embaralhado), `p1722` (a
  auditoria da biblioteca nas duas linguagens). Regressão: + P1722.
- **Corrigido:** as rodadas 06 e 20 (o `log_` próprio nos dois lados).

> **Síntese da Parte 76:** o embedding de Kronecker por nibble (a ideia do texto recebido na Parte 75) usa 80 pesos em vez de 544 e custa +0,079 bit por caractere no inglês (4 de 4 sementes, como a calibração no português previa). O controle com os caracteres embaralhados entre os mesmos bytes custa o mesmo (−0,002): a ordem ASCII não carrega informação sobre a língua, e o preço é a restrição em si (posto 1 por caractere), não a escolha de quais letras ficam juntas. A auditoria da biblioteca nas duas linguagens achou o que a de um lado só deixava passar: das 14 rodadas que usavam exp e log da biblioteca, 12 tinham risco entre as linguagens, 10 estão corrigidas e 2 abertas. O erro que a abriu foi uma cópia Java que a correção não alcançou. Em um lote por condição.

---

**Fontes desta parte**
- Embeddings por produto de Kronecker: A. Novikov et al., "Tensorizing Neural Networks", NeurIPS 2015 (fatorações de pesos em produtos tensoriais)
- Variedade de Segre: J. Harris, *Algebraic Geometry: A First Course* (1992), aula 2
- Byte Latent Transformer: A. Pagnoni et al., [arXiv:2412.09871](https://arxiv.org/abs/2412.09871)
- A tabela ASCII e a sua origem: [ASCII, Wikipedia](https://en.wikipedia.org/wiki/ASCII)
