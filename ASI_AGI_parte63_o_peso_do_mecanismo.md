# Como eu construiria uma AGI/ASI — Parte 63 (0x3F): o peso do mecanismo

> Continuação da [Parte 62](ASI_AGI_parte62_o_ultimo_digito.md). **Previsões registradas antes de qualquer execução que mostre os números medidos e antes de
> escrever o resto deste documento.** A Parte 62 pediu uma regra: todo mecanismo deduzido ganha uma conta do seu peso num caso fora do teste, antes do registro.
> Esta parte é a primeira com essa regra. Pergunta se o fator de congruência efetivo explica a base 8, quanto a glosa portuguesa é mais longa que a inglesa,
> e quantos primos palíndromos há em hexadecimal.

## As perguntas desta parte

1. **P1331 (0x533).** O fator de congruência efetivo explica a base 8? (Rodada 37) ↩ P1301
2. **P1332 (0x534).** A glosa portuguesa da OpenWordNet-PT é mais longa que a inglesa do mesmo sinset? ↩ P1302
3. **P1333 (0x535).** Hexadecimal: quantos primos palíndromos há até 16⁵? ↩ P1303
4. **P1334 (0x536).** Preditiva comigo mesma. **P1335 (0x537).** Engenharia reversa e Jung. **P1336 (0x538).** O diálogo.
5. **P1359 (0x54F).** Placar. **P1360 (0x550).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado), condicionais ao número S de surpresas (contadas pelo script)

Planejadas: 7 previsões do mundo ((a) a (g)) e 3 funções (p1331, p1332, p1333).

| medida | estatístico (até a 62) | ingênuo (Parte 62) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [7.432; 20.719] | 15.473 | **[7.432; 20.719]** | o estatístico |
| compressão | [0,405; 0,434] | 0,411 | **[0,405; 0,434]** | o estatístico |
| testes de unidade | [1,34; 7,91] | 5 | **[2 + S; 5 + S]** | 3 planejados, ~1 por surpresa |
| testes do placar | [4,02; 10,23] | 8 | **7 + 2·S ± 1** | 7 planejados, ~2 por surpresa |
| erros do placar | [0,83; 4,67] | 3 | **[0,83; 4,67]** | o estatístico |
| redundância P821 | [0,505; 0,620] | 0,582 | **[0,505; 0,620]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1332, a glosa portuguesa e a inglesa.** Nos sinsets que têm glosa na OpenWordNet-PT (7.945), a razão (palavras da glosa portuguesa)/(palavras da definição
inglesa, sem os exemplos), e a sua mediana.
- **Restrições, com peso:** (1) o português usa mais palavras funcionais (contrações *do*, *na*, artigos antes de possessivos), o que alonga; (2) mas as glosas
  portuguesas não são traduções literais: algumas são notas curtas ("(geralmente seguido de 'de')"); (3) o português começa a definição sem artigo
  ("entidade que…" contra "an entity that…"), o que encurta em uma palavra. Peso: sem medida externa; a literatura de tradução fala em ~10–20% a mais de
  palavras do inglês para as línguas românicas (não conferido por mim).
- Exemplo à mão: "an entity that has physical existence" (6) contra "entidade que tem existência física" (5): razão 0,83.
- (a) mediana da razão em **[0,85; 1,30]**
- (b) fração dos sinsets em que a glosa portuguesa é mais longa que a inglesa em **[0,35; 0,70]**

**P1333, os primos palíndromos em base 16** (n de 1 a 16⁵ cujos dígitos hexadecimais formam um palíndromo, e primo).
- **Restrições, com peso (calculadas por código antes do registro):** (1) todo palíndromo de comprimento par é divisível por 17 = 0x11 (como os de base 10 por
  11): conferido para os de 2 e 4 dígitos; só o 0x11 sobra; (2) um primo > 2 é ímpar, então o primeiro dígito também é ímpar; (3) entre os ímpares, a densidade
  dos primos é 2/ln n.
- **A conta:** 1 dígito: os primos 2, 3, 5, 7, 0xB, 0xD (6, exatos); 2 dígitos: só 0x11 (1); 3 e 5 dígitos: Σ 2/ln n sobre os palíndromos ímpares = **350,5**.
  Total: 6 + 1 + 350,5 = **357,5**.
- Exemplo à mão: 0x101 = 257, primo (é um primo de Fermat); 0x111 = 273 = 3 × 7 × 13: não.
- (c) quantidade em **[320; 400]** (a conta ± ~11%: a densidade 2/ln n é a do teorema dos números primos, e os palíndromos de 3 dígitos são pequenos)

**P1331, rodada 37:** no `dialogo/DIALOGO.md` (previsões (d) a (g)).
