# Como eu construiria uma AGI/ASI — Parte 58 (0x3A): a primeira diferença

> Continuação da [Parte 57](ASI_AGI_parte57_as_restricoes.md). **Em andamento: previsões registradas antes de qualquer execução e antes de escrever o resto deste
> documento.** O refazer da Parte 46 está fechado (57 partes num `resultados.txt`, regressão 104/104, 31 rodadas IGUAIS). A Rodada 31 achou que a ordem alfabética
> se decide na primeira letra diferente; esta parte mede onde fica essa primeira diferença no dicionário português, quanto o português é mais longo que o inglês,
> e o primeiro dígito hexadecimal das potências.

## As perguntas desta parte

1. **P1181 (0x49D).** No dicionário português, onde fica a primeira diferença entre vizinhos alfabéticos, e quantos vizinhos trocam de ordem entre a ordem dos
   códigos e a do português? (Rodada 32) ↩ P1151
2. **P1182 (0x49E).** Uma palavra portuguesa é mais longa que a inglesa do mesmo sinset? ↩ P972
3. **P1183 (0x49F).** Hexadecimal: o primeiro dígito de 2ⁿ e de 3ⁿ em base 16.
4. **P1184 (0x4A0).** Preditiva comigo mesma. **P1185 (0x4A1).** Engenharia reversa e Jung. **P1186 (0x4A2).** O diálogo.
5. **P1209 (0x4B9).** Placar. **P1210 (0x4BA).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado)

| medida | estatístico (até a 57) | ingênuo (Parte 57) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [8.138; 13.665] | 10.336 | **[9.500; 13.665]** | mecanismo conferido (a seção sobre mim acrescenta) |
| compressão | [0,406; 0,463] | 0,427 | **[0,405; 0,445]** | mecanismo conferido (a tabela baixa) |
| testes de unidade | [2,40; 4,85] | 3 | **[3; 4]** | 3 a 4 funções novas (p1181, p1182, p1183 e talvez um auxiliar), um teste cada |
| testes do placar | [3,26; 11,49] | 5 | **[3,26; 11,49]** | o estatístico |
| erros do placar | [0,42; 4,33] | 1 | **[0,42; 4,33]** | o estatístico |
| redundância P821 | [0,500; 0,596] | 0,554 | **[0,500; 0,596]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | passo verificável |
| pNN novas sem teste | — | 0 | **0** | passo verificável |

### Sobre o mundo

As entradas, medidas antes: **37.725** lemas portugueses de uma palavra só; **24,5%** com acento; **9.176** começam com maiúscula; entropia de 2,937 nats por letra
(alfabeto efetivo 18,9); tamanho médio 8,52.

**As restrições, antes das contas.** (1) Na ordem dos códigos, maiúsculas (65–90) < minúsculas (97–122) < letras acentuadas (≥ 192): as palavras com maiúscula formam
um bloco no começo, e uma palavra com letra acentuada é empurrada para depois de todas as irmãs sem acento que dividem o prefixo; a ordem portuguesa as
devolve ao lugar. (2) Os prefixos e sufixos de derivação (*des-*, *in-*, *-mente*) fazem vizinhos dividirem prefixos maiores que cadeias ao acaso. (3) Em base 16,
2ⁿ = 2^(n mod 4) · 16^k: o primeiro dígito de 2ⁿ **só pode** ser 1, 2, 4 ou 8.

**P1181, rodada 32:** no `dialogo/DIALOGO.md`.

**P1182, português contra inglês.** Para cada sinset com lema português e lema inglês de uma palavra só (o primeiro de cada), a razão média tamanho(pt)/tamanho(en).
- Exemplo à mão: *dog*/*cão* = 3/3 = 1; *nation*/*nação* = 5/6 = 0,83; *happiness*/*felicidade* = 10/9 = 1,11.
- Restrições: o português flexiona e tem sufixos longos (*-mento*, *-idade*), o que alonga; o inglês tem palavras longas de origem latina, que encurtam ao
  traduzir (*-ation* → *-ação*).
- (a) razão média em **[1,00; 1,30]**

**P1183, o primeiro dígito hexadecimal das potências** (n de 1 a 10.000).
- (b) para 2ⁿ: os dígitos 1, 2, 4 e 8 aparecem **exatamente 2.500** vezes cada, e os outros 12 nunca (pela restrição 3)
- (c) para 3ⁿ: o dígito 1 aparece numa fração em **[0,240; 0,260]** (Benford em base 16 dá log₁₆ 2 = 0,25, porque n log₁₆ 3 é equidistribuído: log₁₆ 3 é irracional)
