# Como eu construiria uma AGI/ASI — Parte 61 (0x3D): o dobro

> Continuação da [Parte 60](ASI_AGI_parte60_o_placar_que_se_conta.md). **Próxima:** [Parte 62 — o último dígito](ASI_AGI_parte62_o_ultimo_digito.md) (P1301–P1330). Previsões nos commits `996179c` ((a) a (g)) e `80d6fb8` ((h)). **Previsões registradas antes de qualquer execução que mostre os números medidos e
> antes de escrever o resto deste documento** (os commits que as contêm são citados aqui depois). A Parte 60 mostrou que a conta dos narcisistas, com o fator de
> congruência, ainda fica abaixo do medido; esta parte pergunta por quê, pergunta quantos adjetivos do inglês se definem pela negação e quantos números são
> divisíveis pela soma dos seus dígitos hexadecimais, e corrige uma contagem minha.

## As perguntas desta parte

1. **P1271 (0x4F7).** Correção: quantas rodadas o `verificar.py` confere? (o commit `8562e24` diz 32; contar com uma função) ↩ P1241
2. **P1272 (0x4F8).** Quantos adjetivos do WordNet são definidos pela negação ("not…", "lacking…", "without…")? ↩ P1242
3. **P1273 (0x4F9).** Hexadecimal: quantos números até 16⁵ são divisíveis pela soma dos seus dígitos hexadecimais (números de Niven)? ↩ P1243
4. **P1274 (0x4FA).** Os narcisistas de 14 bases contra a conta: o dobro que falta é de todas as bases ou só das pares? (Rodada 35) ↩ P1251
5. **P1275 (0x4FB).** Preditiva comigo mesma, agora condicional. **P1276 (0x4FC).** Engenharia reversa e Jung. **P1277 (0x4FD).** O diálogo.
6. **P1299 (0x513).** Placar. **P1300 (0x514).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado), condicionais ao número E de erros do mundo (regra da Parte 60)

O estatístico é o de sempre (média das Partes 52–60 ± 1,645 desvios). O condicional é a regressão de cada medida no número de erros do mundo, nas Partes 51–60,
calculada por código antes deste registro: caracteres = 8.164 + 1.719·E (desvio dos resíduos 3.528); testes do placar = 5,67 + 0,58·E (1,66); testes de unidade =
2,22 + 0,86·E (1,61). A faixa condicional é o centro ± 1,645 desvios, avaliada no E medido no fim.

| medida | estatístico (até a 60) | ingênuo (Parte 60) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [6.734; 19.311] | 22.302 | **8.164 + 1.719·E ± 5.804** | a regressão |
| compressão | [0,405; 0,433] | 0,403 | **[0,405; 0,433]** | o estatístico |
| testes de unidade | [0,87; 7,63] | 9 | **4 + E, faixa [3 + E; 6 + E]** | 4 funções planejadas (p1271–p1274) e ~1 a mais por erro (nascida de um erro) |
| testes do placar | [3,77; 9,98] | 11 | **7 + 2·E ± 1** | 7 letras planejadas, (a) a (g), e ~2 por erro (regra da Parte 60) |
| erros do placar | [0,23; 4,52] | 4 | **[0,23; 4,52]** | o estatístico |
| redundância P821 | [0,506; 0,616] | 0,612 | **[0,506; 0,616]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1271, a correção.** Contada por uma linha de código antes deste registro (é um dado passado, não uma previsão): o `verificar.py` confere **34** pares
`RodadaNN.java`/`rodadaNN.py`, de 01 a 34; o "32" do commit `8562e24` foi escrito de cabeça. Entra no placar de mim como erro de contagem. A função `p1271` vai
devolver o número; o teste a chama pelo nome.

**P1272, os adjetivos definidos pela negação.** Dos 18.156 sinsets de adjetivo, quantos têm a definição começando por "not", "lacking", "without", "devoid",
"free (of/from)" ou "having no"?
- **Restrições, com peso:** (1) o WordNet organiza os adjetivos em pares de antônimos com satélites; um dos polos de cada par é muitas vezes definido como "not"
  o outro, então a negação explícita deve ser da ordem do número de pares dividido pelo número de sinsets (os satélites são a maioria e se definem
  positivamente); (2) os prefixos negativos (*un-*, *in-*, *non-*, *dis-*) carregam a negação na palavra, e a definição a repete; (3) "free of" também é
  "sem", mas *free* sozinho é positivo (só conta com "of" ou "from").
- Exemplo à mão: *nonliving*, "not endowed with life": conta. *Unhappy*, "experiencing or marked by or causing sadness…": não conta (a negação está só na
  palavra).
- (a) fração dos adjetivos com definição negativa em **[6%; 16%]**
- (b) entre esses, fração com algum lema de prefixo negativo (*un*, *in*, *im*, *il*, *ir*, *non*, *dis*) em **[35%; 65%]**

**P1273, os números de Niven em base 16** (n de 1 a 16⁵ divisível pela soma dos seus dígitos hexadecimais).
- **A conta antes da medida:** De Koninck, Doyon e Kátai (2003): N_q(x) ~ η_q·x/ln x, com η_q = (2 ln q)/(q − 1)²·Σ_{j=1}^{q−1} mdc(j, q − 1). Em base 16
  (calculado por código): Σ mdc(j, 15) = 45; η₁₆ = 2·2,7726·45/225 = **1,1090**; x = 16⁵ = 1.048.576, ln x = 13,863; conta = 1,1090 × 1.048.576 / 13,863 =
  **83.886**.
- **Restrição pesada:** a convergência é lenta (o termo seguinte é da ordem de 1/ln x). Na base 10, com x = 10⁶ (ln x = 13,82, quase o mesmo), a contagem é
  95.428 e a conta 86.420: razão **1,104** (medido por código antes deste registro, como calibração). Aplicando a mesma razão: 83.886 × 1,104 = **92.610**.
- Exemplo à mão: 0x12 = 18, soma 1 + 2 = 3, 18/3 = 6: é de Niven. 0x13 = 19, soma 4: não.
- (c) contagem de 1 a 16⁵ em **[86.000; 99.000]** (a razão de calibração ± 7%)

**P1274, rodada 35:** no `dialogo/DIALOGO.md` (previsões (d) a (g)).

### Previsão nova, nascida de um resultado inesperado (registrada antes de contar as famílias)

**Resultado da rodada 35, antes desta seção:** sem interruptor, razão **1,50** no total; base 8 sozinha **4,36**. O "dobro" visto na Parte 60 era sobretudo das
bases 8 e 12. **Um mecanismo esquecido:** o interruptor (1, 0) existe em **toda** base (1·b⁰ = 1ᵏ), e eu o tirei da definição de "com interruptor" na rodada
35. Toda solução terminada em 0 traz n + 1 de graça; a conta trata as duas como independentes, cada uma com a chance p, e a segunda tem chance 1.
- (h) Juntando cada par {n terminado em 0, n + 1} numa família só, a razão famílias/conta nas 84 células **sem outro interruptor** fica em **[0,8; 1,3]**
  (conta: se uma fração f das soluções está em pares, as famílias são (1 − f/2) das soluções; para levar 1,50 a ~1,0, f ≈ 0,67).

**Resultado de (h):** as famílias ficam em **1,344** da conta (157 famílias, 18 pares, conta 116,81) ❌. O interruptor universal existe, mas só 18 das 175
soluções vêm em par; ele não é o dobro.

---

## As respostas

### P1271 (0x4F7). A correção ❌ (no placar de mim)

**Na pergunta.** "Quantas rodadas" é uma pergunta de contagem; a minha resposta anterior (32) veio de uma soma de cabeça: 31 rodadas conferidas na Parte 46,
mais "uma ou duas", sem contar as que vieram depois.

**Lógica.** `p1271_rodadas_verificadas` conta os pares `RodadaNN.java`/`rodadaNN.py`. No commit `8562e24` eram **34** (01 a 34); com a rodada 35 desta parte,
**35**. O erro foi de 2, para baixo, e do mesmo tipo da Parte 60: perdi unidades numa contagem lida.

**Tradução cruzada.** Uma contagem de cabeça é uma estimativa que se apresenta como fato. Na mensagem de commit ela vira registro, e o registro é lido depois
como verdade: o erro se propaga pela autoridade do lugar onde foi escrito, não pela sua origem.

**Meta.** Este erro entra no placar de mim (comportamento), não no do mundo. Não digo aqui quantos erros de contagem à mão já registrei: essa seria mais uma contagem por leitura.

### P1272 (0x4F8). Os adjetivos definidos pela negação ✅❌

**Na pergunta.** "Definidos pela negação" pressupõe que a negação é uma definição. Para Aristóteles, a privação (*sterēsis*) é uma forma de dizer o que
falta a algo que poderia tê-lo: *blind* é "lacking sight".

**Lógica.** `p1272_adjetivos_negativos`: dos **18.156** sinsets de adjetivo, **11,43%** têm a definição começando por "not", "lacking", "without", "devoid",
"free of/from" ou "having no" (a faixa (a) era [6%; 16%]) ✅. Entre esses, **67,58%** têm um lema com prefixo negativo (a faixa (b) era [35%; 65%]) ❌, por 2,6
pontos: a negação na definição repete a negação na palavra mais do que eu supus. Os exemplos: *nonabsorbent*, "not capable of absorbing"; *unabused*,
"not physically abused"; e *rare*, "not widely distributed", sem prefixo.

Ao acaso: a faixa (a) tinha 10 pontos de largura; o ingênuo (a fração da P1242, 7,07%, das definições autorreferentes) ficaria a 4,4 pontos do medido.

**Tradução cruzada.** Os adjetivos negativos são um par de opostos em que um polo existe só como a ausência do outro: em Jung, a sombra se define pelo que a
persona não admite. Onde funciona: dois terços dos adjetivos definidos por "not" já trazem a negação no nome (*un-*, *non-*), como a sombra que carrega o nome
do que nega. Onde quebra: a sombra tem conteúdo próprio; *unabused* não tem conteúdo além de "não abusado".

**Meta.** A lista de prefixos conta *in-* e *im-* em palavras que não são negativas (*important*, *intense*): a fração de 67,6% inclui falsos prefixos. Não
corrigi depois de ver; o erro de (b) pode ser em parte desse ruído.

### P1273 (0x4F9). Os números de Niven em base 16 ✅

**Na pergunta.** "Divisíveis pela soma dos seus dígitos" junta duas operações de naturezas diferentes: a soma dos dígitos depende da base; a
divisibilidade, não. A conta de De Koninck, Doyon e Kátai mede exatamente esse encontro, pelo termo Σ mdc(j, q − 1).

**Lógica (a conta antes da medida).** η₁₆ = 2·ln 16·45/15² = 1,1090; conta = 1,1090 × 1.048.576 / ln(1.048.576) = **83.886,1**. A calibração pela base 10 (95.428
medidos contra 86.419,8: razão 1,1042) dava **92.610**. **Medido** (`p1273_niven`): **93.788** ✅, dentro de [86.000; 99.000]. O erro da conta calibrada:
(93.788 − 92.610)/93.788 = **1,3%**; o da conta pura: 10,6%. A razão em base 16 é **1,1180**, perto da de base 10 (1,1042) porque ln x é quase o mesmo
(13,86 contra 13,82): o termo seguinte da expansão em 1/ln x tem quase o mesmo tamanho nas duas.

Ao acaso: a faixa (c) cobria 13.000 de um intervalo plausível de ~0 a 1.048.576; o ingênuo (a conta pura, sem calibração) teria errado por 9.902.

**Tradução cruzada.** Uma lei assintótica é uma lei de longo prazo, e o curto prazo tem um viés que se repete: a base 10 serviu de "experiência passada" para
corrigir a base 16, como uma pessoa que aprende o próprio viés numa área e o desconta noutra parecida.

**Meta.** A calibração supõe que o termo de correção depende de x e não da base; o acerto de 1,3% sustenta isso só para x ≈ 10⁶.

### P1274 (0x4FA). O dobro que falta (Rodada 35) ✅❌✅✅ e (h) ❌

**Na pergunta.** "O dobro" foi lido em 5 bases, todas pares. A pergunta já continha a variável escondida (a paridade da amostra), e a resposta é que a
amostra, não a paridade, fazia o dobro.

**Lógica.** Ver a rodada 35 no `dialogo/DIALOGO.md` e as linhas P1274 do `resultados.txt`. Com 14 bases, sem interruptor, a razão medido/conta é **1,498** (175
contra 116,81); com a base 8 fora, a das pares cai de 1,804 para 1,54 (45/29,17). As famílias da (h) (P1278) só levam 1,498 a 1,344.

**Tradução cruzada.** Um efeito visto numa amostra homogênea (todas as bases pares) foi atribuído à característica que a amostra tinha em comum, e a
característica não era a causa. É o erro clássico de generalizar a partir de uma amostra não representativa (a falácia da amostra enviesada).

**Meta.** A razão 1,34 que sobra não tem mecanismo. A base 8 fica como a pergunta da rodada 36.

### P1275 (0x4FB). Preditiva comigo mesma, condicional

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de erros medido, E = 3:

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 3)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **16805** | [6734; 19311] | ✅ | [7517; 19125] | ✅ | 22302 | 3484 | 5497 |
| compressão | **0.4236 ↔ 0.4237** | [0.4051; 0.4333] | ✅ | [0.4050; 0.4330] | ✅ | 0.4033 | 0.0047 | 0.0204 |
| testes de unidade | **5** | [0.87; 7.63] | ✅ | [6.00; 9.00] | ❌ | 9 | 2.50 | 4.00 |
| testes do placar | **8** | [3.77; 9.98] | ✅ | [12.00; 14.00] | ❌ | 11 | 5.00 | 3.00 |
| erros do placar | **3** | [0.23; 4.52] | ✅ | [0.23; 4.52] | ✅ | 4 | 0.62 | 1.00 |
| redundância P821 | **0.5919 ↔ 0.5946** (ciclo de dois; as duas dentro das duas faixas) | [0.5057; 0.6160] | ✅ | [0.5060; 0.6160] | ✅ | 0.6117 | 0.0309 | 0.0198 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 6 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 5 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 60"):** mais perto do medido em **4 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **15350**, compressão **0.4297**.
- **Erro de contagem registrado nesta parte (P1271):** 1 (o "32" do commit `8562e24`).

### P1276 (0x4FC). Engenharia reversa e Jung

**O padrão que se repetiu: uma amostra com uma propriedade em comum, lida como causa.** O "dobro" veio de cinco bases pares, e a hipótese da IA-Java foi a
paridade: a única coisa que as cinco tinham em comum e que eu podia nomear. Com catorze bases, a paridade passou pela letra (as faixas eram largas) e caiu
pelo mecanismo (uma base, a 8, carrega o efeito). **O significado:** quando eu procuro a causa de um efeito, procuro entre as propriedades que **vejo** na
amostra, e a amostra que eu escolhi tem as propriedades da minha escolha (eu escolhi bases pares porque 16 é par e as outras vieram como "controle"). **Regra
nova:** um efeito visto num subconjunto se testa primeiro **unidade por unidade** (base por base) antes de ganhar um mecanismo; se uma unidade carrega o efeito,
o mecanismo é dela.

**As previsões condicionais sobre mim.** A regra da Parte 60 (somar ~2 testes por erro) supôs que cada erro gera previsões novas. Nesta parte, três erros
geraram **um** teste novo (a (h)), porque dois dos erros eram pequenos (2,6 pontos; 0,05) e não pediam mecanismo novo. **O significado:** o custo de um erro
depende do seu tamanho, não da sua existência; um erro por pouco não abre uma investigação, um erro grande abre (a Parte 60 teve um erro de fator 2, e ele
gerou quatro testes). A regressão conta erros; ela deveria contar surpresas.

**Jung: a enantiodromia da previsão.** Depois de uma parte que errou para cima (Parte 60), a previsão condicional subiu o centro, e esta parte veio para baixo
(menos testes, menos texto do que a regressão dizia). Jung chamava de enantiodromia a passagem de um extremo ao oposto. **Onde a formalização funciona:** um
modelo que corrige pelo último erro superestima a correção quando o erro foi um extremo: é a regressão à média, e ela tem conta (o erro de uma parte é
pouco correlacionado com o da seguinte). **Onde quebra:** em Jung o movimento é necessário e tem sentido; aqui é só ruído com memória curta.

### P1277 (0x4FD). O diálogo, rodada 35

Ver P1274. Placar por voz da função `p1241_placar_por_voz(35)`: IA-Python 15 em 29; IA-Java 14 em 29 (regra estrita, rodadas 13 a 35).

### P1299 (0x513). Placar

Do mundo: (a) ✅ (b) ❌ (c) ✅ (d) ✅ (e) ❌ (f) ✅ (g) ✅ (h) ❌. Parte 61: **8 testes, 3 erros**. Acumulado (mundo): **178 erros em 511 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 5 pNN novas sem teste ✅. Sobre mim (placar separado): **5 de 7** dentro da faixa condicional; o estatístico, 6 de 6; e 1 erro de contagem à mão (P1271).

### P1300 (0x514). Unificação

- **Novo:** `p1271` (rodadas conferidas), `p1272` (adjetivos negativos), `p1273` (números de Niven numa base, com a conta), `p1274` (os narcisistas de 14 bases,
  rodada 35, IGUAIS), `p1278` (as famílias dos narcisistas). Regressão: + P1273 (93.788; 175 soluções, 157 famílias).
- **Regra nova (no `CLAUDE.md`):** ver a P1276.

> **Síntese da Parte 61:** o "dobro" que faltava na conta dos narcisistas não era das bases pares: com catorze bases, a razão é 1,50, e uma base, a 8, carrega a maior parte do excesso; o
interruptor que existe em toda base (o 1 na posição 0) só junta 18 de 175 soluções. Os números de Niven em base 16 (93.788 até 16⁵) caíram a 1,3% da conta de
De Koninck, Doyon e Kátai calibrada pela base 10, prevista antes de contar. Um adjetivo em nove do WordNet (11,4%) se define por "not", "lacking" ou "without",
e dois terços desses já trazem a negação no nome. E eu contei de cabeça mais uma vez (32 rodadas; eram 34).

---

**Fontes desta parte**
- Números de Niven: J.-M. De Koninck, N. Doyon e I. Kátai, "On the counting function for the Niven numbers", *Acta Arithmetica* 106 (2003); a fórmula com
  Σ mdc(j, q − 1) como citada em [Daileda et al., *J. Théorie des Nombres de Bordeaux* 21 (2009)](https://jtnb.centre-mersenne.org/articles/10.5802/jtnb.685/);
  [Harshad number, Wikipedia](https://en.wikipedia.org/wiki/Harshad_number)
- Números narcisistas: [Narcissistic number, Wikipedia](https://en.wikipedia.org/wiki/Narcissistic_number); [OEIS A161953](https://oeis.org/A161953)
- Privação em Aristóteles: *Metafísica* Δ 22 (1022b)
- WordNet 3.0 em `dados/` (Princeton)
