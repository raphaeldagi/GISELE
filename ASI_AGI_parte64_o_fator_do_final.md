# Como eu construiria uma AGI/ASI — Parte 64 (0x40): o fator do final

> Continuação da [Parte 63](ASI_AGI_parte63_o_peso_do_mecanismo.md). Previsões nos commits `5c9c385` ((a) a (g)) e `e457ef7` ((h)). **Previsões registradas antes de qualquer execução que mostre os números medidos e antes de
> escrever o resto deste documento.** A Parte 63 achou os primos palíndromos de base 16 a 0,1% da conta e os de base 12 a 10%. Esta parte pergunta se o fator exato
> do dígito final explica a diferença, se as palavras curtas do inglês têm mais sentidos, e quantos quadrados são palíndromos em hexadecimal.

## As perguntas desta parte

1. **P1361 (0x551).** O fator exato do dígito final aproxima a conta dos primos palíndromos nas bases 5 a 16? (Rodada 38) ↩ P1333
2. **P1362 (0x552).** As palavras curtas do WordNet têm mais sentidos? (a lei da brevidade e a lei do significado de Zipf) ↩ P1302
3. **P1363 (0x553).** Hexadecimal: quantos quadrados de n < 16⁴ são palíndromos em base 16? ↩ P1333
4. **P1364 (0x554).** Preditiva comigo mesma. **P1365 (0x555).** Engenharia reversa e Jung. **P1366 (0x556).** O diálogo.
5. **P1389 (0x56D).** Placar. **P1390 (0x56E).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado), condicionais ao número S de surpresas (contadas pelo script)

Planejadas: 7 previsões do mundo ((a) a (g)) e 3 funções (p1361, p1362, p1363).

| medida | estatístico (até a 63) | ingênuo (Parte 63) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [8.101; 21.215] | 16.296 | **[8.101; 21.215]** | o estatístico |
| compressão | [0,404; 0,430] | 0,412 | **[0,404; 0,430]** | o estatístico |
| testes de unidade | [1,34; 7,91] | 5 | **[2 + S; 5 + S]** | 3 planejados, ~1 por surpresa |
| testes do placar | [4,34; 10,41] | 8 | **7 + 2·S ± 1** | 7 planejados, ~2 por surpresa |
| erros do placar | [0,42; 4,33] | 1 | **[0,42; 4,33]** | o estatístico |
| redundância P821 | [0,512; 0,628] | 0,597 | **[0,512; 0,628]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1362, a brevidade e o significado.** Nos lemas de uma palavra só do WordNet (minúsculas), a correlação de postos (Spearman) entre o comprimento em letras e o
número de sinsets em que o lema aparece.
- **Restrições, com peso:** (1) Zipf: as palavras frequentes são mais curtas (lei da brevidade) e têm mais sentidos (lei do significado, sentidos ∝ frequência^½);
  então o comprimento e o número de sentidos devem ter correlação negativa; (2) a maioria dos lemas tem um sentido só, e os empates enfraquecem o Spearman.
  **Peso medido fora do teste, num caso perto (o português da OpenWordNet-PT, com a mesma variável que move o mecanismo: a fração de monossêmicos), por código
  antes deste registro:** Spearman **−0,138**, com 66% de monossêmicos. O inglês do WordNet tem mais lemas raros e técnicos (mais monossêmicos, mais empates),
  mas as palavras curtas do inglês são muito polissêmicas (*run*, *set*, *take*).
- Exemplo à mão: *set* (3 letras) tem dezenas de sinsets; *aardvark* (8) tem 1.
- (a) Spearman em **[−0,30; −0,10]**

**P1363, os quadrados palíndromos em base 16** (n de 1 a 16⁴ − 1 com n² palíndromo em hexadecimal).
- **A conta antes da medida (por código):** um número de L dígitos ao acaso é palíndromo com chance 16^(−⌊L/2⌋); somando sobre os quadrados: **15,0**.
- **Restrições, com peso:** (1) os quadrados de palíndromos com dígitos pequenos são palíndromos sem vai-um (0x11² = 0x121, 0x111² = 0x12321): uma família
  estrutural que a conta não vê; (2) **peso medido fora do teste, num caso perto (base 10, n < 10⁴), por código antes deste registro:** 19 medidos contra a conta
  de 12,2 (razão 1,56).
- Exemplo à mão: 0x11² = 289 = 0x121, palíndromo; 0x12² = 324 = 0x144, não.
- (b) quantidade em **[17; 40]** (a conta × razão de 1,1 a 2,7)

**P1361, rodada 38:** no `dialogo/DIALOGO.md` (previsões (c) a (g)).

### Previsão nova, nascida de um resultado inesperado (registrada antes de rodar as bases 17 a 22)

**Resultado da rodada 38, antes desta seção:** a base 14 ficou **3σ abaixo** da conta B (216 contra 257,7, σ = 14,1), e a soma das 12 bases ficou negativa (−43,1),
fora de [0; 80]. Duas leituras: (1) acaso (uma base em 12 a 3σ tem chance de alguns por cento); (2) um viés da conta para baixo do medido nas bases grandes, ou para
cima, que eu não conheço. Um teste em bases novas separa as duas:
- (h) nas **bases 17 a 22**, até b⁵, com a mesma conta B: o número de bases (das 6) com |medido − conta B| ≥ 2σ fica em **[0; 2]**, e a média de (medido − conta B)/σ
  fica em **[−1,0; 1,0]** (as duas condições juntas; se o desvio da base 14 for um viés sistemático, a média sai abaixo de −1).

**Resultado de (h):** nas bases 17 a 22, uma base fora de 2σ (a 21, z = −2,55; a 20 ficou em −1,98), e a média de z é **−1,093**, abaixo de −1,0 ❌ por 0,09. As **seis**
ficaram abaixo da conta: chance (½)⁶ = 1/64 sem viés. O desvio da base 14 não foi acaso isolado: a conta B tem um viés para cima nas bases grandes.

---

## As respostas

### P1361 (0x551). O fator do final (Rodada 38) ✅✅✅✅❌ e (h) ❌

**Na pergunta.** "O fator exato do dígito final" supõe que o dígito final de um palíndromo é como o de um número qualquer. Não é: é igual ao primeiro, que nunca é
0. A resposta mora nessa igualdade: em base prima, todo palíndromo é coprimo com a base.

**Lógica.** `p1361_fator_do_final` (rodada 38, IGUAL em Java, com o log próprio da rodada 26). Conta B = (exatos de 1 e 2 dígitos) + Σ Π_{p | 2b} p/(p − 1) / ln n nos
palíndromos de comprimento ímpar ≥ 3 coprimos a 2b. Linha por linha, nas bases que mais mudam:
- base 5: A = 16,61, B = **20,26**, medido 25 (z = +1,44);
- base 7: A = 37,99, B = **43,82**, medido 50 (z = +1,16);
- base 12: A = 177,32, B = **178,16**, medido 196 (razão 1,100, z = +1,61);
- base 14: A = 256,77, B = 257,70, medido **216** (z = **−2,95**);
- base 16: A = B = 357,52 (o fator de 16 = 2⁴ é o da paridade), medido 357.

A média de |medido − B|/B nas 12 bases é **0,088**; 11 de 12 bases a menos de 2σ. Nas bases 17 a 22 (h), todos os z negativos, média −1,09.

**Tradução cruzada.** Uma simetria (o palíndromo) amarra o fim ao começo, e o começo nunca é vazio: a forma impede um defeito (o zero final) que um número
qualquer teria. Na biologia, uma restrição de desenvolvimento que elimina um fenótipo antes de a seleção agir sobre ele.

**Meta.** O viés para baixo nas bases grandes não tem mecanismo ainda. Candidatos: os primos pequenos que não dividem 2b e a forma especial da soma dos dígitos e da
soma alternada de um palíndromo (a pergunta da rodada 39).

### P1362 (0x552). A brevidade e o significado ✅

**Na pergunta.** "As palavras curtas têm mais sentidos" junta duas leis de Zipf (a da brevidade e a do significado) pela variável que nenhuma das duas mede aqui: a
frequência. A resposta mede a consequência sem medir a causa.

**Lógica.** `p1362_brevidade_e_sentidos`: nos **77.503** lemas de uma palavra só, o Spearman entre o comprimento e o número de sinsets é **−0,225** (a faixa (a) era
[−0,30; −0,10], centrada no português medido antes, −0,138) ✅. Os monossêmicos são 69,7%. A média de sentidos por comprimento **não** é monótona: sobe de 2,11 (2
letras) e 2,94 (3) a **3,57** (4 letras) e depois cai (2,61 com 5; 1,28 com 12). A minha hipótese (não medida aqui): as palavras de 2 e 3 letras incluem siglas e símbolos com um sentido só, e o pico em 4 é o das
palavras comuns.

Ao acaso: sem associação, o erro-padrão de ρ é 1/√(n − 1) = 1/√77.502 = 0,0036, e −0,225 fica a 62,7 erros-padrão; o ingênuo "o português, −0,138" erraria por 0,087.

**Tradução cruzada.** O uso gasta a palavra e a enche de sentidos: uma palavra muito usada fica curta (erosão) e polissêmica (acúmulo). Na geologia, um seixo rolado é
pequeno e liso porque andou muito.

**Meta.** O comprimento em letras mistura siglas com palavras; um filtro de siglas mudaria a cabeça da curva.

### P1363 (0x553). Os quadrados palíndromos em base 16 ✅

**Na pergunta.** "Quadrados que são palíndromos" pede uma coincidência (um quadrado ao acaso ser simétrico) e uma estrutura (o quadrado de um palíndromo de dígitos
pequenos é palíndromo sem vai-um). A resposta é a soma das duas.

**Lógica (a conta antes da medida).** Σ 16^(−⌊L/2⌋) sobre os quadrados de n < 16⁴ = **15,0**; com o peso medido na base 10 (razão 1,56), a faixa foi [17; 40]. **Medido**
(`p1363_quadrados_palindromos`): **24** ✅, razão **1,60**, colada na da calibração. Os 24: 1, 2, 3, os de dígitos pequenos (0x11, 0x22, 0x101, 0x111, 0x121, 0x131,
0x202, 0x212, 0x222, 0x1001, 0x1111, 0x1221, 0x2002, 0x2112), e os "acidentais" (0x13F, 0x305, 0x561, 0x203E, 0x221E, 0x2356, 0xC9AD), cujos quadrados são
palíndromos com vai-um.

Ao acaso: a faixa tinha 24 de largura; o ingênuo "a conta pura, 15,0" erraria por 9.

**Tradução cruzada.** Uma simetria que se preserva sob uma operação (o quadrado) só quando não há transbordamento (vai-um): em física, uma simetria que vale no regime
linear e quebra no não linear.

**Meta.** A razão da base 10 e a da 16 coincidirem (1,56 e 1,60) pode ser coincidência com contagens tão pequenas (19 e 24).

### P1364 (0x554). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 0 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 2)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **14578** | [8101; 21215] | ✅ | [8101; 21215] | ✅ | 16296 | 80 | 1718 |
| compressão | **0.4166 ↔ 0.4167** (oscila) | [0.4042; 0.4301] | ✅ | [0.4040; 0.4300] | ✅ | 0.4122 | 0.0004 | 0.0044 |
| testes de unidade | **4** | [1.34; 7.91] | ✅ | [2.00; 5.00] | ✅ | 5 | 0.50 | 1.00 |
| testes do placar | **8** | [4.34; 10.41] | ✅ | [6.00; 8.00] | ✅ | 8 | 1.00 | 0.00 |
| erros do placar | **2** | [0.42; 4.33] | ✅ | [0.42; 4.33] | ✅ | 1 | 0.38 | 1.00 |
| redundância P821 | **0.6425 ↔ 0.6448** (oscila; as duas fora das duas faixas) | [0.5122; 0.6280] | ❌ | [0.5120; 0.6280] | ❌ | 0.5966 | 0.0748 | 0.0481 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 5 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 6 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 63"):** mais perto do medido em **4 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **13000**, compressão **0.4253**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 0 de 2 erros.
- **Erros de processo nesta parte:** 0.

### P1365 (0x555). Engenharia reversa e Jung

**O padrão que se repetiu: a amostra que a memória escolhe.** A única previsão inicial que errou, (g), teve o sinal tirado de dois casos (base 10 até 10⁷ e base 12),
e nos dois a conta ficava abaixo do medido. Os dois casos não foram escolhidos por uma regra: foram os que eu **lembrava** (a base 10 pela OEIS, a 12 pela parte
anterior). Nas bases grandes, o sinal é o oposto (a conta fica acima, nas seis bases novas). É o padrão da Parte 61 (a amostra com uma propriedade em comum, lida como
geral) com a origem identificada: **a minha memória é a amostra**. **O significado:** quando eu calibro "fora do teste", eu calibro onde já estive, e onde já estive
não é ao acaso. **Regra nova:** os casos de calibração são escolhidos por uma regra escrita antes de olhar (todas as bases de um intervalo, ou sorteadas com semente),
não pelos casos que eu lembro; dois casos não fixam um sinal.

**O resultado inesperado virou teste, e o teste achou um viés.** A base 14 a −2,95σ podia ser acaso; a previsão (h) testou em seis bases novas e achou as seis do
mesmo lado. A regra da Parte 25 (cada resultado inesperado gera um teste novo, pré-registrado) transformou um ponto estranho num efeito com chance 1/64 sem viés.
Errei a faixa de (h) por 0,09 na média de z, e o erro foi informativo: a faixa supunha "sem viés".

**Jung: a criptomnésia.** Jung chamou de criptomnésia a lembrança que volta sem ser reconhecida como lembrança e passa por ideia nova (o seu estudo de Nietzsche, que
reproduziu sem saber uma passagem lida na juventude). **Onde a formalização funciona:** os meus casos de calibração voltaram da memória como se fossem uma amostra
neutra, e a regra nova é um teste de criptomnésia: de onde veio este caso? **Onde quebra:** em Jung a criptomnésia é inconsciente por definição; aqui eu posso
perguntar e responder, porque a origem de cada caso está no registro das partes.

### P1366 (0x556). O diálogo, rodada 38

Ver P1361. Placar por voz da função `p1241_placar_por_voz(38)`: IA-Python 18 em 32; IA-Java 16 em 32 (regra estrita, rodadas 13 a 38).

### P1389 (0x56D). Placar

Do mundo: (a) ✅ (b) ✅ (c) ✅ (d) ✅ (e) ✅ (f) ✅ (g) ❌ (h) ❌. Parte 64: **8 testes, 2 erros**. Acumulado (mundo): **184 erros em 535 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 4 pNN novas sem teste ✅. Sobre mim (placar separado): **6 de 7** dentro da faixa condicional; o estatístico, 5 de 6; e 0 erros de processo (P1335).

### P1390 (0x56E). Unificação

- **Novo:** `p1361` (o fator do final, rodada 38, IGUAIS), `p1362` (brevidade e sentidos), `p1363` (quadrados palíndromos numa base), `p1367` (primos palíndromos em
  bases novas). Regressão: + P1363 (24 quadrados; base 12 com 196).
- **Regra nova (no `CLAUDE.md`):** ver a P1365.

> **Síntese da Parte 64:** o fator exato do dígito final não move a base 12 (171,3 → 172,2), mas move muito as bases ímpares, porque o último dígito de um palíndromo é o primeiro e nunca é 0
(base 5: conta 16,6 → 20,3, medido 25); e nas bases 17 a 22 todas as contagens ficaram abaixo da conta (chance 1/64 sem viés): falta um fator. As palavras curtas do
inglês têm mais sentidos (Spearman −0,225), com um pico nas de 4 letras. Em base 16, 24 quadrados de n < 16⁴ são palíndromos, 1,6 vez a conta, a mesma razão que a base
10 deu antes. E a calibração que errou foi a que a minha memória escolheu.

---

**Fontes desta parte**
- Leis de Zipf da brevidade e do significado: [Zipf's law of abbreviation, Wikipedia](https://en.wikipedia.org/wiki/Brevity_law); G. K. Zipf, "The meaning-frequency
  law", *Journal of General Psychology* 33 (1945)
- Primos palíndromos: [Palindromic prime, Wikipedia](https://en.wikipedia.org/wiki/Palindromic_prime)
- Quadrados palíndromos: [OEIS A002778](https://oeis.org/A002778) (quadrados palíndromos em base 10)
- WordNet 3.0 em `dados/` (Princeton); OpenWordNet-PT (CC BY 4.0)
