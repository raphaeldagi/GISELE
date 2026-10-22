# Parte 131 — Volta 4 do loop, e a auditoria de arquivos sem uso corrigida

↩ Nasce das Partes 129 e 130: a P1871 lê menção como uso, e a sua própria saída absolve os acusados na volta seguinte.

## O que é novo nesta volta
1. **A P3175** (`p3175_arquivos_sem_uso_v2`): a parte (c) da P1871 sem contar como CITAÇÃO o que aparece em saídas de execução
   (`reproducao/`, `resultados.txt`). As saídas continuam sendo auditadas; só deixam de ser fonte. Ela tem um teste com controle dos
   dois lados (regra da Parte 75):
   - um arquivo citado só numa saída TEM de ser acusado;
   - um importado por um .py NÃO pode ser acusado.
   A P1871 antiga fica intacta: o código dela é medido, regra das Partes 14 e 16.
2. **A volta 4** propriamente: um clone limpo, as 127 partes (contadas pelo lançador), os testes e as rodadas, e a comparação volta 3
   contra volta 4.

## Previsões, registradas antes de lançar a volta e antes de rodar a P3175 no repositório
**Procedência:**
- identidades: X1, X4, X6;
- de mecanismo: X2, X3, X5, X7, X8.
O centro de "quantos erros" é 5 × 0,25 ≈ 1,25. X7 e X8 são previsões sobre contagens de arquivos, e eu errei a última (W7). Por isso as
duas saem da leitura do código, como a regra da Parte 130 manda: a P1871 casa o nome-base, e casa em .py, .java, .md, .txt e .tsv (os
.sh não são lidos).

| | quantidade | faixa | procedência |
|---|---|---|---|
| X1 | blocos sem exceção | todos | identidade |
| X2 | blocos com a regressão 170/170 | [15; 16] de 16 | P(16/16) ≈ 0,85 |
| X3 | linhas da volta 3 que mudam na volta 4 | [5; 12] | P143, P213, P913, P1692 (+2 funções), P2446 (+1 pNN), P1872 (troca o arquivo único), P433/P434 |
| X4 | dessas, do mundo | [0; 0] | identidade |
| X5 | testes que falham | [0; 1] | três voltas com 0 |
| X6 | rodadas DIFERENTES | [0; 0] de 90 | identidade |
| X7 | P1871 (a antiga), arquivos "não referenciados" na volta 4 | [0; 2] | mecanismo da Parte 130: só o arquivo de nome único da volta 3 (`bloco_122_123_126_127_128_129.txt`) fica sem irmão; o documento mais novo é citado pelo link da parte anterior |
| X8 | P3175 no repositório, no commit deste registro | [175; 215] | conta: os 130 da volta 1 + os 66 arquivos das três voltas (não citados fora das saídas: os nomes `bloco_*.txt` e `testes_*.txt` só aparecem em saídas e no `nova_volta.sh`, que não é lido) + o documento mais novo ≈ 197; ±10% de incerteza pelos arquivos que eu não li um a um, ×1,36 |

**Sobre mim:** erros no mundo em [0; 3], com centro 1,25.

## Mudança de procedimento, registrada antes de medir (23h10 UTC)
O contêiner reiniciou duas vezes durante a volta 4: às 22h36 e entre 22h40 e 23h08. Nas duas vezes nenhum bloco tinha terminado, porque um
bloco de 8 partes leva de 10 minutos a 2 horas (o das Partes 25 a 32). Com reinícios a cada ~30 min, a volta em blocos não termina nunca.

**A mudança: uma parte por processo** (`reproducao/nova_volta_por_parte.sh`). Cada parte roda isolada (`import calculos;
calculos.PARTES[k]()`), num arquivo `bloco_K_.txt` com marca de concluído, e a unificação roda uma vez, em `unificacao.txt`. O que já
terminou sobrevive a um reinício.

Isso muda duas previsões, e a mudança fica escrita aqui antes de qualquer número:
- **X2** passa a ser "a unificação única dá 170/170". Não há mais regressão por bloco: P(uma regressão) ≈ 0,99, faixa [170; 170].
- **X4 vira um teste mais forte.** Nas voltas 1 a 3, cada parte rodava DEPOIS das outras do seu bloco, no mesmo processo. Agora roda
  sozinha. Uma parte que dependesse do estado deixado pela anterior (o gerador global `random`, um cache, uma variável de módulo)
  mostraria uma diferença do MUNDO. A previsão continua [0; 0]: as simulações usam geradores locais com semente fixa (regra da série).
  Mas é a primeira vez que essa independência entre as partes é testada, e uma diferença seria um achado.

As outras faixas ficam como estavam.
