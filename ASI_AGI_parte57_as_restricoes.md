# Como eu construiria uma AGI/ASI — Parte 57 (0x39): as restrições

> Continuação da [Parte 56](ASI_AGI_parte56_empates.md). **Em andamento: previsões registradas antes de qualquer execução e antes de escrever o resto deste
> documento.** A Parte 56 achou que a conta fecha quando acho a restrição escondida (a rede dos múltiplos de 3). Esta parte aplica a regra antes de cada conta:
> listar as restrições, depois prever. Palíndromos no dicionário, números palíndromos em base 10 e 16 ao mesmo tempo, e a ordem alfabética do português.

## As perguntas desta parte

1. **P1151 (0x47F).** A ordem dos 4-gramas empatados muda se o alfabeto for o do português? (Rodada 31) ↩ P1121
2. **P1152 (0x480).** Quantas palavras do WordNet são palíndromos, contra um modelo de letras independentes?
3. **P1153 (0x481).** Hexadecimal: quantos números abaixo de 10⁶ são palíndromos em base 10 e em base 16?
4. **P1154 (0x482).** Preditiva comigo mesma. **P1155 (0x483).** Engenharia reversa e Jung. **P1156 (0x484).** O diálogo.
5. **P1179 (0x49B).** Placar. **P1180 (0x49C).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado)

O estatístico (até a Parte 56), os mecanismos conferidos e o efeito da regra com faixa na quantidade que entra nela: 3 a 4 funções novas (p1151, p1152, p1153 e
talvez um auxiliar), logo **3 a 4** testes de unidade.

| medida | estatístico | ingênuo (Parte 56) | **eu** |
|---|---|---|---|
| caracteres | [7.599; 13.614] | 12.464 | **[9.500; 13.614]** |
| compressão | [0,407; 0,468] | 0,421 | **[0,405; 0,445]** |
| testes de unidade | [2,40; 4,85] | 3 | **[3; 4]** |
| testes do placar | [4,00; 11,75] | 6 | **[4,00; 11,75]** |
| erros do placar | [0,74; 4,26] | 3 | **[0,74; 4,26]** |
| redundância P821 | [0,490; 0,597] | 0,501 | **[0,490; 0,597]** |
| previsões unilaterais | — | 0 | **0** |
| pNN novas sem teste | — | 0 | **0** |

### Sobre o mundo

**P1152, palíndromos no dicionário** (lemas alfabéticos de 3 letras ou mais, minúsculos). As entradas da conta, medidas antes: 77.197 palavras; Σp² das letras = 0,0629.
Modelo de letras independentes: P(palíndromo de tamanho L) = (Σp²)^⌊L/2⌋; somando sobre a distribuição dos tamanhos: **116** palíndromos esperados.
- **As restrições, antes da previsão:** (1) a primeira e a última letra de uma palavra têm distribuições diferentes (terminações *-s*, *-e*, *-y*; inícios *s*, *c*, *p*):
  a chance de coincidirem é menor que Σp²; (2) palavras curtas de 3 letras (*eve*, *pop*, *dad*) puxam para cima. Peso maior para (1): centro 0,7 × 116 = 81.
- Exemplo à mão: *civic*, *level*, *radar*, *kayak* são palíndromos do inglês; não conferi se estão no WordNet como lemas.
- (a) palíndromos em **[47; 140]** (centro 81, ×1,72)

**P1153, palíndromos em base 10 e 16** (1 a 999.999). Entradas medidas antes: 1.998 palíndromos decimais; para cada um, a chance de ser palíndromo em hexadecimal
16^(−⌊k/2⌋) (k dígitos hexadecimais): soma **25,3** esperados.
- **As restrições:** os dois sistemas dividem o fator 2 (a paridade do último dígito é a de n nos dois), o que amarra a paridade dos primeiros dígitos; em média
  isso não muda a probabilidade. Centro 25,3.
- Exemplo à mão: 353 = 0x161, palíndromo nos dois (3·256 = 768 > 353? não: 0x161 = 256 + 96 + 1 = 353 ✓).
- (b) duplos palíndromos em **[14,7; 43,5]** (centro 25,3, ×1,72)
