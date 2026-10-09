# Como eu construiria uma AGI/ASI — Parte 52 (0x34): o método ou a série

> Continuação da [Parte 51](ASI_AGI_parte51_curta_e_longa.md). **Em andamento: previsões registradas antes de qualquer execução.** A Parte 51 deu a vitória
> à potência sobre duas exponenciais, com uma ressalva: as duas foram ajustadas fora da escala do erro. Esta parte refaz o ajuste na escala certa, procura os
> funis das definições em **português**, e testa o "inverte e soma" (palíndromos) em hexadecimal.

## As perguntas desta parte

1. **P1001 (0x3E9).** Ajustadas em log, duas exponenciais vencem a potência? (Rodada 26) ↩ P971
2. **P1002 (0x3EA).** Para onde escorrem as definições em português? ↩ P912
3. **P1003 (0x3EB).** Hexadecimal: quantos números chegam a um palíndromo invertendo e somando?
4. **P1004 (0x3EC).** Engenharia reversa. **P1005 (0x3ED).** Jung. **P1006 (0x3EE).** O diálogo.
5. **P1029 (0x405).** Placar. **P1030 (0x406).** Unificação.

## Previsões pré-registradas

**P1002, os funis do português.** Para cada lema de uma palavra só de um sinset de substantivo da OpenWordNet-PT que tem glosa: a primeira palavra da glosa
(forma singular pela `DicionarioPT.lema`) que é lema de algum sinset de substantivo e não é ela mesma. O grau de entrada de cada palavra.
- Exemplo à mão: a glosa de *abaxial* (adjetivo, fora do teste) começa por "A superfície abaxial de uma folha": o primeiro substantivo é *superfície*.
- (a) a mais escolhida está em {*pessoa*, *ato*, *parte*, *forma*, *grupo*} (cinco candidatas; sem faixa porque é uma identidade)
- (b) as 10 mais escolhidas recebem entre **10% e 30%** das palavras com destino (no inglês, P912: 16,8%)

**P1003, inverte e soma em base 16.** n → n + (n com os dígitos hexadecimais invertidos), até ser um palíndromo hexadecimal (no máximo 50 passos), para n
de 1 a 4095 (0xFFF).
- Exemplo à mão: 0x1A + 0xA1 = 0xBB, palíndromo em 1 passo.
- A referência: em base 10, abaixo de 10.000 há 249 candidatos a número de Lychrel (97,5% chegam).
- (c) fração que chega a um palíndromo em até 50 passos em **[85%; 99,5%]**
- (d) média de passos dos que chegam em **[1,5; 4,0]**
