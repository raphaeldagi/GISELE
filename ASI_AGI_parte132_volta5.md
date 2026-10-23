# Parte 132 — Volta 5 do loop

↩ Nasce da Parte 131 (a volta 4, a primeira com uma parte por processo) e do pedido "Repita sempre tudo que fizemos. Loop infinito."

## O que esta volta testa
É a volta 4 repetida pelo mesmo procedimento (uma parte por processo), no commit desta parte, comparada com a volta 4. Pela primeira
vez as duas voltas comparadas têm o mesmo procedimento E as partes isoladas.

Entre os commits 1980631 e este mudaram:
- o `calculos.py`: a `_parte_131` e a entrada P3174v4;
- o CLAUDE.md, o `resultados.txt` (as saídas das 130 e 131) e os testes;
- o link da Parte 123 para a 124;
- `reproducao/volta4/`, com 127 arquivos de parte com nomes NOVOS (um por parte), a unificação e os 6 dos testes.

O mecanismo, pela leitura do código da P1871 (regra da Parte 130):
- os arquivos de parte da volta 4 têm nomes-base que não existem em nenhum outro arquivo versionado. Os nomes das voltas 1 a 3 eram
  nomes de BLOCO. Os scripts que geram os novos nomes são .sh, que a P1871 não lê. Nenhum documento escreve um desses nomes: escrevo
  "bloco_K_" com a letra K, de propósito, pela regra da Parte 131;
- logo, a P1871 da volta 5 deve acusar os 127 arquivos de parte da volta 4. A unificação não: o nome dela aparece no documento da 131.

## Previsões, registradas antes de lançar a volta e antes de rodar a P3175 neste commit
**Procedência:**
- identidades: Y1, Y4, Y6;
- de mecanismo, com a leitura do código: Y2, Y3, Y5, Y7, Y8.

O centro de "quantos erros" é 5 × 0,25 ≈ 1,25. Mas Y7 e Y8 são contagens de arquivos, o tipo que eu errei duas vezes em três voltas
(W7 errou; X7 acertou com o mecanismo incompleto). Para elas, a taxa de erro histórica é 1/3, e o centro sobe para 3 × 0,25 + 2 × 0,33
≈ 1,4.

| | quantidade | faixa | procedência |
|---|---|---|---|
| Y1 | partes sem exceção | todas (128) | identidade |
| Y2 | a unificação: 171/171 | [171; 171] | P(uma) ≈ 0,99 |
| Y3 | linhas da volta 4 que mudam na volta 5 | [5; 12] | P143, P213, P913, P1692 (+1 função), P1871 e P1872 (0 → ~127), P433/P434 |
| Y4 | dessas, do mundo | [0; 0] | identidade |
| Y5 | testes que falham | [0; 1] | quatro voltas com 0 |
| Y6 | rodadas DIFERENTES | [0; 0] de 90 | identidade |
| Y7 | P1871 na volta 5: arquivos "não referenciados" | [120; 130] | conta: os 127 arquivos de parte da volta 4, ±3 pelos que eu não li |
| Y8 | P3175 neste commit | [305; 335] | conta: 190 + 127 arquivos de parte + 5 dos testes da volta 4 (os nomes `testes_*` só aparecem em saídas e em .sh) ≈ 322 |

**Sobre mim:** erros no mundo em [0; 3], com centro 1,4.
