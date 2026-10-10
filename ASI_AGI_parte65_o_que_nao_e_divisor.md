# Como eu construiria uma AGI/ASI — Parte 65 (0x41): o que não é divisor

> Continuação da [Parte 64](ASI_AGI_parte64_o_fator_do_final.md). Previsões nos commits `21d71b2` ((a) a (g)) e `329cc7f` ((h) e (i)). **Previsões registradas antes de qualquer execução que mostre os números medidos e antes de
> escrever o resto deste documento.** A Parte 64 achou as seis bases de 17 a 22 abaixo da conta dos primos palíndromos. Esta parte pergunta se os primos pequenos que
> não dividem 2b explicam o viés, se a definição de um substantivo fica mais longa quanto mais fundo ele está na taxonomia, e quanto vale o período de 1/p em hexadecimal.

## As perguntas desta parte

1. **P1391 (0x56F).** Os primos pequenos q ∤ 2b dividem os palíndromos com a frequência 1/q? A correção explica o viés das bases grandes? (Rodada 39) ↩ P1361
2. **P1392 (0x570).** A definição de um substantivo é mais longa quanto mais fundo ele está na taxonomia? ↩ P1362
3. **P1393 (0x571).** Hexadecimal: o período de 1/p em base 16, relativo ao maior possível (p − 1). ↩ P1363
4. **P1394 (0x572).** Preditiva comigo mesma. **P1395 (0x573).** Engenharia reversa e Jung. **P1396 (0x574).** O diálogo.
5. **P1419 (0x58B).** Placar. **P1420 (0x58C).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado), condicionais ao número S de surpresas (contadas pelo script)

Planejadas: 7 previsões do mundo ((a) a (g)) e 3 funções (p1391, p1392, p1393).

| medida | estatístico (até a 64) | ingênuo (Parte 64) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [8.500; 21.356] | 14.704 | **[8.500; 21.356]** | o estatístico |
| compressão | [0,404; 0,429] | 0,417 | **[0,404; 0,429]** | o estatístico |
| testes de unidade | [1,61; 7,89] | 4 | **[2 + S; 5 + S]** | 3 planejados, ~1 por surpresa |
| testes do placar | [4,72; 10,53] | 8 | **7 + 2·S ± 1** | 7 planejados, ~2 por surpresa |
| erros do placar | [0,33; 4,17] | 2 | **[0,33; 4,17]** | o estatístico |
| redundância P821 | [0,537; 0,638] | 0,643 | **[0,537; 0,638]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1392, a profundidade e o tamanho da definição.** Nos substantivos com profundidade na taxonomia (P793), o Spearman entre a profundidade e o número de palavras da
definição (sem os exemplos).
- **Restrições, com peso:** (1) um conceito mais específico precisa de mais diferenças para ser separado dos irmãos (gênero + mais diferenças): puxa para cima; (2) os
  sinsets fundos são sobretudo espécies e gêneros, definidos por uma fórmula curta ("a genus of…", "any of various…"): puxa para baixo. **Peso medido num caso
  escolhido por regra escrita antes (a outra classe com hierarquia, os verbos), por código antes deste registro:** Spearman **0,020** (13.708 verbos).
- Exemplo à mão: *entity* (profundidade 0), 18 palavras; *dog* (profundidade ~13), "a member of the genus Canis…", ~20 palavras: quase igual.
- (a) Spearman nos substantivos em **[−0,10; 0,15]**

**P1393, o período de 1/p em base 16.** Para os primos p de 10⁴ a 10⁵, a média de ord_p(16)/(p − 1) (ord_p(16) é o período de 1/p em hexadecimal).
- **Restrições, com peso:** (1) 16 = 2⁴ é um quadrado, então nunca é raiz primitiva: ord_p(16) = ord_p(2)/mdc(ord_p(2), 4) ≤ (p − 1)/2; (2) a média de ord_p(2)/(p − 1)
  é uma constante conhecida (~0,58, da conjectura de Artin e dos trabalhos de Stephens). **Peso medido num caso escolhido por regra escrita antes (todos os primos
  abaixo de 10⁴), por código antes deste registro:** média de ord_p(16)/(p − 1) = **0,279**; de ord_p(2)/(p − 1) = 0,585; razão 0,477 = E[1/mdc(ord₂, 4)].
- Exemplo à mão: p = 17: ord₁₇(2) = 8, ord₁₇(16) = 8/4 = 2; 1/17 = 0x0,0F0F…, período 2.
- (b) média de ord_p(16)/(p − 1) nos primos de 10⁴ a 10⁵ em **[0,26; 0,30]**

**P1391, rodada 39:** no `dialogo/DIALOGO.md` (previsões (c) a (g)).

### Previsões novas, nascidas do viés que persistiu (registradas antes de rodar a correção nas bases 17 a 22)

**Resultado da rodada 39, antes desta seção:** a correção dos primos pequenos não muda nada (média |correção − 1| = 0,0149; (c) ❌ por pouco), e o viés persiste
(média de z nas bases 17 a 22 = −1,07, (d) ✅), 86,5% dele nos palíndromos de comprimento 5.

**Um mecanismo novo, deduzido:** para um primo r que divide b² + 1, um palíndromo de 5 dígitos d₀d₁d₂d₁d₀ é n = d₀(b⁴ + 1) + d₁(b³ + b) + d₂b²; como b² ≡ −1 (mod r),
b³ + b ≡ 0 e b⁴ + 1 ≡ 2, então **n ≡ 2d₀ − d₂ (mod r)**: a divisibilidade depende só de dois dígitos, e o par (d₀, d₂ = 2d₀) a produz com chance ~1/(2b), muito maior
que 1/r quando r ≈ b². **O peso, medido antes nas bases escolhidas por regra (23 a 26), só as frações:** nas pares, f·r = 12,5 e 13,5 e a correção é **0,978**; nas
ímpares, a correção é **1,019 e 1,002**, porque numa base ímpar o palíndromo coprimo a 2b é ímpar, a paridade de n é a do dígito do meio, e d₂ = 2d₀ (par) fica proibido.
O mecanismo existe, pesa ~2% e troca de sinal com a paridade da base.
- (h) com a correção dos primos r > 13 que dividem (b² + 1)(b⁴ + 1) e não dividem 2b, a média de z nas bases 17 a 22 fica em **[−1,4; −0,7]** (o efeito se cancela entre
  pares e ímpares; o viés continua sem explicação).
- (i) o sinal de (correção_r − 1) nas seis bases: **negativo nas três pares (18, 20, 22) e não negativo nas três ímpares (17, 19, 21)**, as seis (ao acaso, (½)⁶ = 1/64).

**Resultado de (h) e (i):** com a correção dos primos de b² + 1 e b⁴ + 1, a média de z nas bases 17 a 22 vai de −1,072 a **−1,011** (h) ✅. Os sinais de (correção_r − 1):
20 e 22 negativos, 17, 19 e 21 positivos, e **18 positivo** (1,0012), contra a previsão (i) ❌: 18² + 1 = 325 = 5²·13 só tem primos ≤ 13, já tratados na rodada 39, e
o mecanismo forte precisa de um primo grande em b² + 1. A base 21 fica a **−3,03σ**.

---

## As respostas

### P1391 (0x56F). O que não é divisor (Rodada 39) ❌✅✅✅✅ e (h) ✅ (i) ❌

**Na pergunta.** "Os primos pequenos que não dividem 2b" é a lista dos suspeitos que a conta já tratava como independentes. A resposta inocenta todos eles: os palíndromos
são divisíveis por 3, 5, 7, 11 e 13 com a frequência 1/q, a menos de 1,5% nas bases pequenas e de 0,3% nas grandes. O suspeito estava fora da lista: os primos de b² + 1.

**Lógica.** `p1391_o_que_nao_e_divisor` (rodada 39, IGUAL em Java). A correção Π (1 − f_q)/(1 − 1/q) fica entre **0,945** (base 8) e **1,089** (base 5), média de
|correção − 1| = **0,0149**; nas bases 17 a 22, entre 0,986 e 1,010. Com a conta C, a média de z nas bases 17 a 22 é **−1,072** e o déficit está 86,5% nos de 5 dígitos.

**A conta do mecanismo novo, linha por linha.** Para r | b² + 1: b² ≡ −1, então b³ + b = b(b² + 1) ≡ 0 e b⁴ + 1 = (b²)² + 1 ≡ 2 (mod r). O palíndromo
n = d₀(b⁴ + 1) + d₁(b³ + b) + d₂b² ≡ 2d₀ + 0 − d₂ = 2d₀ − d₂ (mod r). Com r > 2b, só d₂ = 2d₀ (para d₀ < b/2) zera o resto: ~b/2 pares (d₀, d₂) entre ~b², chance
~1/(2b), contra 1/r ≈ 1/b². Na base 20 (r = 401): f·r = **10,5** (`p1397`), e a correção é 0,974. Numa base ímpar, o palíndromo coprimo a 2b é ímpar, a sua paridade é a do
dígito do meio, e d₂ = 2d₀ é par: a família some, e a correção passa de 1 (17: 1,021).

**Tradução cruzada.** Dois efeitos opostos (as bases pares perdem primos, as ímpares ganham) se cancelam na média e escondem um mecanismo forte: em física, duas forças
iguais e opostas dão equilíbrio sem dar ausência de força. A média de z quase não mudou (−1,07 → −1,01), e o mecanismo existe com ±2%.

**Meta.** A base 21 (−3,03σ) segue sem explicação; o σ corrigido supõe que a correção multiplica a variância, o que é aproximado.

### P1392 (0x570). A profundidade e o tamanho da definição ✅

**Na pergunta.** "Mais fundo, mais longa" supõe que especificar custa palavras. Custa até um ponto: depois os sinsets fundos são espécies com fórmula curta.

**Lógica.** `p1392_profundidade_e_definicao`: nos **82.115** substantivos com profundidade, Spearman **0,081** (a faixa (a) era [−0,10; 0,15], calibrada nos verbos:
0,020) ✅. A média de palavras por profundidade sobe de 9,3 (profundidade 7) a **11,1** (profundidade 11) e cai para 8,4 (profundidade 16–17): uma curva em ∩. O meio
da taxonomia é onde as distinções são mais finas e mais verbais; o fundo é a nomenclatura biológica, curta e padronizada.

Ao acaso: sem associação, o erro-padrão de ρ com 82.115 sinsets é 1/√82.114 ≈ 0,0035, e 0,081 fica a ~23 erros-padrão: há associação, fraca. O ingênuo "como nos
verbos, 0,020" erraria por 0,061.

**Tradução cruzada.** O meio da hierarquia é onde mora a maior parte do esforço de distinguir: na biologia, a classificação no nível de família e gênero exige mais
caracteres que no nível de reino (poucos e grandes) ou de espécie (um ou dois). Na psicologia, o nível básico de Rosch (cachorro, não animal nem poodle) é o mais
informativo, e aqui as definições mais longas ficam no meio.

**Meta.** A profundidade é a do menor caminho até uma raiz; sinsets com dois pais podem estar em profundidades diferentes nos dois caminhos.

### P1393 (0x571). O período de 1/p em base 16 ✅

**Na pergunta.** "O período de 1/p em hexadecimal" é a ordem de 16 módulo p, e 16 = 2⁴: a pergunta já diz que a resposta é a ordem de 2 dividida por mdc(ord₂, 4).

**Lógica.** `p1393_periodo_hex`: nos **8.363** primos de 10⁴ a 10⁵, a média de ord_p(16)/(p − 1) é **0,2747** (a faixa (b) era [0,26; 0,30]) ✅; a de ord_p(2)/(p − 1), **0,5749**,
perto da constante de Stephens (0,5760, a média sobre as bases a, OEIS A065478; para a = 2 sozinho, não achei a fonte); a razão é **0,4778**, quase igual à da calibração
(0,4778 contra 0,477). O período máximo possível para um quarto poder, (p − 1)/mdc(p − 1, 4), aparece em **56,3%** dos primos.

Ao acaso: a faixa (b) tinha 0,04 de largura numa média que pode ir de 0 a 0,5; o ingênuo "a média de 2, 0,575, dividida por 4" daria 0,144, longe.

**Tradução cruzada.** Um quarto poder de um gerador gera no máximo um quarto do grupo, e em média um pouco menos que a metade do que o gerador gera (0,48): uma lente que
olha de 4 em 4 passos vê menos padrões, mas não 4 vezes menos, porque muitos ciclos já têm comprimento ímpar ou com pouco fator 2.

**Meta.** A conta do 0,48 é empírica (a razão medida na calibração); a fórmula fechada exigiria a distribuição da valorização 2-ádica de ord_p(2).

### P1394 (0x572). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 1 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 2)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **15849** | [8500; 21356] | ✅ | [8500; 21356] | ✅ | 14704 | 921 | 1145 |
| compressão | **0.4099 ↔ 0.4100** (oscila) | [0.4041; 0.4291] | ✅ | [0.4040; 0.4290] | ✅ | 0.4174 | 0.0066 | 0.0075 |
| testes de unidade | **4** | [1.61; 7.89] | ✅ | [3.00; 6.00] | ✅ | 4 | 0.50 | 0.00 |
| testes do placar | **9** | [4.72; 10.53] | ✅ | [8.00; 10.00] | ✅ | 8 | 0.00 | 1.00 |
| erros do placar | **2** | [0.33; 4.17] | ✅ | [0.33; 4.17] | ✅ | 2 | 0.25 | 0.00 |
| redundância P821 | **0.6125** | [0.5373; 0.6383] | ✅ | [0.5370; 0.6380] | ✅ | 0.6425 | 0.0250 | 0.0300 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 6 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 7 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 64"):** mais perto do medido em **4 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **14269**, compressão **0.4176**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 1 de 2 erros (a (i), uma previsão de largura zero: qualquer erro nela conta como surpresa pela regra).
- **Erros de processo nesta parte:** 0.

### P1395 (0x573). Engenharia reversa e Jung

**O padrão que se repetiu: duas regras certas que se atropelam.** A previsão (c) errou pelo motivo exato da Parte 63 (o caso de calibração longe do teste na variável que
move o mecanismo), e errou **porque** eu segui a regra da Parte 64 (escolher a calibração por uma regra escrita antes, não pela memória). A regra que escrevi ("as bases 23
a 26, logo depois do teste") era uma regra, mas escolhia só bases grandes, com muitos palíndromos, e a oscilação da correção mora nas bases pequenas. **O significado:**
cada regra nova corrige um erro e, sozinha, reabre outro; as regras da série são restrições que precisam valer juntas, e eu as aplico uma de cada vez. **Regra nova:** a
regra de escolha da calibração cobre a faixa inteira da variável que move o mecanismo no teste (aqui: bases pequenas e grandes, ou um sorteio estratificado por ela).

**A previsão categórica sem a condição.** A (i) previu o sinal nas seis bases pela paridade, e o mecanismo só existe quando b² + 1 tem um primo grande. Na base 18 ele não
tem, e o sinal saiu ao acaso. É a regra da Parte 61 (testar unidade por unidade) do lado da previsão: antes de prever para cada unidade, conferir em cada uma se a condição
do mecanismo vale.

**Jung: a coniunctio que só cancela.** Jung via na união dos opostos (coniunctio oppositorum) o nascimento de um terceiro, a função transcendente. Aqui os opostos (bases
pares perdem primos, ímpares ganham) se unem na média e somem: o total quase não mudou (−1,07 → −1,01) e esconde um mecanismo de ±2%. **Onde a formalização funciona:** a
média de opostos não informa sobre eles; só a separação (base por base, paridade por paridade) mostra o mecanismo, como na análise junguiana só a diferenciação mostra os
opostos que a persona equilibra. **Onde quebra:** não nasce terceiro nenhum; a soma é só um cancelamento aritmético.

### P1396 (0x574). O diálogo, rodada 39

Ver P1391. Placar por voz da função `p1241_placar_por_voz(39)`: IA-Python 19 em 33; IA-Java 16 em 33 (regra estrita, rodadas 13 a 39).

### P1419 (0x58B). Placar

Do mundo: (a) ✅ (b) ✅ (c) ❌ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ❌. Parte 65: **9 testes, 2 erros**. Acumulado (mundo): **186 erros em 544 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 4 pNN novas sem teste ✅. Sobre mim (placar separado): **7 de 7** dentro da faixa condicional; o estatístico, 6 de 6; e 0 erros de processo (P1335).

### P1420 (0x58C). Unificação

- **Novo:** `p1391` (o que não é divisor, rodada 39, IGUAIS), `p1392` (profundidade e tamanho da definição), `p1393` (o período de 1/p em base 16), `p1397` (a correção dos
  primos de b² + 1 e b⁴ + 1). Regressão: + P1393 (8.363 primos; base 5 com 48 palíndromos coprimos).
- **Regra nova (no `CLAUDE.md`):** ver a P1395.

> **Síntese da Parte 65:** os primos pequenos que não dividem 2b dividem os palíndromos com a frequência de sempre (1/q) e não explicam o viés das bases grandes. O mecanismo que existe é outro: um
primo r de b² + 1 divide o palíndromo de 5 dígitos quando 2d₀ = d₂, cerca de b/2 vezes mais do que 1/r, e só nas bases pares (nas ímpares a paridade proíbe a família).
Os efeitos se cancelam e a base 21 continua a −3σ. A definição dos substantivos é mais longa no meio da taxonomia (11,1 palavras na profundidade 11) do que no topo e no
fundo. O período de 1/p em hexadecimal vale em média 0,275 de p − 1, 0,478 do período em binário, porque 16 = 2⁴.

---

**Fontes desta parte**
- Constante de Stephens e ordens multiplicativas: [OEIS A065478](https://oeis.org/A065478); [S. Kim, "Explicit constants in averages involving the multiplicative order",
  arXiv:1510.04348](https://arxiv.org/abs/1510.04348); [P. Moree, "Artin's primitive root conjecture — a survey", arXiv:math/0412262](https://arxiv.org/pdf/math/0412262)
- Nível básico das categorias: E. Rosch et al., "Basic objects in natural categories", *Cognitive Psychology* 8 (1976)
- Primos palíndromos: [Palindromic prime, Wikipedia](https://en.wikipedia.org/wiki/Palindromic_prime)
- WordNet 3.0 em `dados/` (Princeton)
