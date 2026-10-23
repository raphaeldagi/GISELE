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

## Medido (P3174, P3175; as saídas ficam em `reproducao/volta4/`)
| | medido | faixa | |
|---|---|---|---|
| X1 | 127 de 127 partes sem exceção | todos | ✅ |
| X2 | a unificação única: **170/170** | [170; 170] | ✅ |
| X3 | **9** de 1.878 linhas mudaram (0,48%) | [5; 12] | ✅ |
| X4 | **0** do mundo (7 do projeto, 2 da máquina), com cada parte ISOLADA | [0; 0] | ✅ |
| X5 | **0** falhas: 725 + 27 + 40 + 72 + 55 testes | [0; 1] | ✅ |
| X6 | **0** DIFERENTES; as 90 rodadas IGUAIS | [0; 0] | ✅ |
| X7 | P1871: **0** arquivos "não referenciados" | [0; 2] | ✅ (abaixo) |
| X8 | P3175: **191** arquivos sem uso | [175; 215] | ✅ (medido logo depois do registro, antes da volta) |

**Mundo: 8 de 8.** **Sobre mim: 1 de 1.** Previ de 0 a 3 erros, com centro 1,25, e tive 0.

### O que esta volta mostrou
- **As partes são independentes entre si.** Esta é a primeira vez que cada parte rodou sozinha, num processo novo, e nenhuma linha do
  mundo mudou. Nenhuma parte depende do estado deixado pelas anteriores (o gerador global, um cache, uma variável de módulo). É a
  propriedade que a regra "semente fixa, gerador local" deveria garantir, agora medida em 127 partes.
- **O tempo do processador explica-se por código:** 3,77 h somando as 127 partes, contra 6,33 h da volta 3 em blocos. Cada bloco fazia
  a sua própria unificação (555 s), e 6,33 − 16 × 555/3.600 = 3,87 h, a 0,1 h do medido. A diferença entre os dois procedimentos é quase
  toda a regressão repetida 16 vezes.
- **X7: a previsão mudou o objeto previsto.** Pela leitura do código, a P1871 acusaria um arquivo, o de nome único da volta 3
  (`bloco_122_123_126_127_128_129.txt`). Deu 0, porque eu escrevi esse nome no registro de X7, neste documento, e a P1871 casa o
  nome-base em qualquer arquivo versionado. Conferido por `grep`: o nome aparece 1 vez neste arquivo. A faixa [0; 2] acertou, mas o
  mecanismo que eu escrevi para o centro estava incompleto: faltava o próprio registro. É a Parte 53 ao pé da letra (uma previsão que
  mora dentro do objeto previsto muda o objeto), pela segunda vez no loop, depois da Parte 129.
- **A P3175 achou um defeito real.** O documento da Parte 124 não era citado por ninguém, porque a Parte 123 dizia "Parte 124" sem link
  (a regra "ligar a nova parte a partir da anterior" quebrada). O link foi posto no commit 275e349. Das 191 acusações, 187 (120 + 58 + 6 + 3, somadas por código) estão em
  `dialogo/`, `reproducao/`, `externos/` e `entregas/`. São rodadas, saídas e arquivos recebidos que ninguém cita pelo nome, e a
  maioria é usada por glob (o verificador) ou é registro. Olhar cada uma fica como pendência (regra da Parte 72: cada acusação é olhada
  antes de ser contada).

### O procedimento, contado
O contêiner reiniciou três vezes no começo desta volta (às 22h36, por volta das 23h08 e às 23h55), e uma quarta morte veio às 00h27.
A causa mais provável, deduzida pelo que mudou: nas voltas 1 a 3 sempre havia uma espera ou uma vigilância rodando entre os meus
turnos; na volta 4, até as 00h28, não havia, e o ambiente recolhe o contêiner por inatividade. Desde que voltei a deixar uma espera em
segundo plano, nenhum processo morreu (1 h 16 min seguidas, das 00h28 às 01h44; a primeira versão deste texto dizia "3 h 45 min", confundindo com as horas de processador). Isso é uma hipótese de um lote (Parte 66), não uma causa medida. Mesmo
assim, o procedimento por parte fica: ele sobrevive a um reinício de qualquer causa.

## Engenharia reversa
- **Quatro voltas, 0 diferenças do mundo nas quatro, e agora também com as partes isoladas.** O núcleo da SYNTHAI é reproduzível no
  sentido mais forte que o loop consegue medir: em processos diferentes, em ordens diferentes e em dias diferentes.
- **O padrão que se repetiu no loop (Partes 129, 130, 131) são as medidas sobre o projeto lendo os próprios registros:**
  - a P1871 caiu de 130 para 22 porque as saídas citavam os arquivos;
  - caiu de 22 para 1 porque a sua saída absolvia os acusados;
  - caiu de 1 para 0 porque a MINHA PREVISÃO citou o último.
  Toda medida de "o que é usado" num repositório que guarda as próprias medições converge para zero. O auditor acaba medindo o
  arquivamento, não o uso. A P3175 resolve metade disso: exclui as saídas como fonte. A outra metade, os documentos das partes que
  falam dos arquivos, fica, porque um documento que explica um arquivo é, de fato, um uso dele.
- **Regra nova (Parte 131):** um nome de arquivo escrito numa previsão sobre arquivos entra na conta da própria previsão. Ou eu o descrevo
  sem escrever o nome-base, ou somo o seu efeito no centro.

## Funções e testes
- **Funções:** `p3175_arquivos_sem_uso_v2` (com o teste dos dois controles) e `_parte_131`. A entrada `P3174v4` foi para a regressão,
  que agora tem 171 entradas.
- **Testes:** `test_p3175_arquivos_sem_uso_v2` e `test_volta4_regressao`, em `synthai/testes_parte128.py`.

## Loop
A volta 5 começa num clone novo, no commit desta parte, também uma parte por processo. A continuação está agendada; para parar, basta
dizer "pare".

➡ Anterior: [Parte 130](ASI_AGI_parte130_volta3.md).

Depois do link da Parte 124, a P3175 deu **190** (191 − 1: o documento da 124 passou a ser citado). A suíte deu 667/667, e a regressão
171/171.

➡ Próxima: [Parte 132 — volta 5](ASI_AGI_parte132_volta5.md).
