# Como eu construiria uma AGI/ASI — Parte 64 (0x40): o fator do final

> Continuação da [Parte 63](ASI_AGI_parte63_o_peso_do_mecanismo.md). **Previsões registradas antes de qualquer execução que mostre os números medidos e antes de
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
