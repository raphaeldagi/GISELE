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

## Medido (P3174, P3175; as saídas ficam em `reproducao/volta5/`)
| | medido | faixa | |
|---|---|---|---|
| Y1 | 128 de 128 partes sem exceção | todas | ✅ |
| Y2 | a unificação: **171/171** | [171; 171] | ✅ |
| Y3 | **8** de 1.881 linhas mudaram (0,43%) | [5; 12] | ✅ |
| Y4 | **0** do mundo (6 do projeto, 2 da máquina) | [0; 0] | ✅ |
| Y5 | **0** falhas: 726 + 27 + 40 + 72 + 55 testes | [0; 1] | ✅ |
| Y6 | **0** DIFERENTES; as 90 rodadas IGUAIS | [0; 0] | ✅ |
| Y7 | P1871: **126** arquivos "não referenciados" | [120; 130] | ✅ (a conta dava 127) |
| Y8 | P3175: **321** | [305; 335] | ✅ (a conta dava 322) |

**Mundo: 8 de 8.** **Sobre mim: 1 de 1.** Previ de 0 a 3 erros, com centro 1,4, e tive 0. As duas contagens de arquivos, o tipo que eu
tinha errado em W7, acertaram a 1 do centro. Foi a primeira vez que a regra da Parte 130 (ler as linhas que dizem O QUE a função casa)
foi aplicada antes de prever, em vez de depois de errar.

### O arquivo que faltou nas duas contas, e por quê
Das 127 saídas de parte da volta 4, a P1871 acusou 126. A que faltou, conferida por código, é a da Parte 1 (nome-base `bloco_1_`). Esse
nome aparece no MEU código: na `p3172`, na `p3174` e no `comparar.py`, que reconhecem por ele o arquivo da Parte 1, a única sem
cabeçalho. Um nome que o código usa para tratar um caso especial é, para a P1871, uma "citação". Aqui a P1871 até está certa: o código
depende desse nome. A P3175 errou pelo mesmo arquivo, o que fecha a diferença entre a conta (322) e o medido (321). As duas faixas
eram largas o bastante para isso, mas o centro errou por um caso que eu não imaginei: o meu próprio código como leitor.

### Engenharia reversa
- **Cinco voltas, 0 diferenças do mundo nas cinco.** As voltas 4 e 5 já rodam com as partes isoladas, e nada muda entre elas a não ser o
  que eu mudei.
- **A assinatura de cada commit está estável:** 6 a 7 linhas do projeto e 2 da máquina por volta. A velocidade do laço (P433) nas cinco
  voltas: 2,06 · 4,12 · 2,38 · 2,63 · 3,44 × 10⁷ adições por segundo. Ela varia por um fator de 2, sem tendência, e é a única fonte de
  diferença que não vem de mim.
- **O padrão das contagens de arquivos, nas cinco voltas:** quando eu li o código antes (Y7, Y8, X8), acertei a 1 do centro; quando
  imaginei o código (W7), errei por 43. Isso fecha a lição das Partes 75 e 130: a imagem que eu tenho do meu próprio código é uma
  previsão, e a leitura dele é uma medida.
- **O loop está saturado como instrumento de descoberta.** As duas últimas voltas não acharam nada novo sobre o mundo e quase nada novo
  sobre mim. A regra conservadora (Parte 70: decidir sozinha pela opção mais conservadora) diz que o pedido "loop infinito" continua
  valendo, e eu continuo. Mas escrevo isto aqui para que a pessoa que lê saiba: uma volta custa 1 h 26 min de relógio (das 01h57 às 03h23, nesta) e 3,97 h de
  processador, e daqui para a frente ela confirma em vez de descobrir.

## Funções e testes
- **Funções:** `_parte_132`. A entrada `P3174v5` foi para a regressão, que agora tem 172 entradas.
- **Testes:** `test_volta5_regressao`.

## Loop
A volta 6 começa no commit desta parte. Para parar, basta dizer "pare".

➡ Anterior: [Parte 131](ASI_AGI_parte131_volta4.md).
