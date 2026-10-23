# Parte 141 — O resultado da volta 8, e o reservatório e o posto efetivo bit a bit (rodada 93)

↩ Nasce da Parte 135 (o registro da volta 8) e da Parte 137 (`synthai/reservatorio.py`, de `aprendizagem_continua.py`).

## A rodada 93, prevista antes de rodar
Um fluxo de 64 vetores de 4 dimensões vem de um LCG. O reservatório de 16 é o `synthai.reservatorio.Reservatorio` REAL, com o gerador
trocado por um que tira randrange(n) = ⌊u·n⌋ do mesmo LCG; o Java faz o mesmo. Depois vem o posto efetivo da matriz 16 × 4 guardada:
centrar, ZᵀZ, autovalores por Jacobi cíclico (a mesma ordem de rotações) e exp(−Σp ln p) com o exp e o log próprios da rodada 26.

| | quantidade | faixa | procedência |
|---|---|---|---|
| H1 | os 16 índices guardados | iguais | o reservatório só compara inteiros |
| H2 | o posto efetivo | IGUAL bit a bit | o Jacobi usa só + − × ÷ e √, na mesma ordem de varredura; o posto usa o exp e o log próprios |
| H3 | o posto da tradução contra o `posto_efetivo` do módulo (math.log, sum compensado) | \|dif\| < 1e-12 | os dois diferem só no último bit |

Registrado antes da primeira execução da rodada.

## Medido (rodada 93)
| | medido | faixa | |
|---|---|---|---|
| H1 | os 16 índices, linha idêntica | iguais | ✅ |
| H2 | posto 3,8429827… IGUAL bit a bit | IGUAL | ✅ |
| H3 | a asserção passou | < 1e-12 | ✅ |

**Mundo: 3 de 3.**

## A suíte e a regressão
A suíte inteira (711 testes, com os das Partes 136 a 138) deu OK, e as 92 rodadas do diálogo deram IGUAIS. A regressão deu **181 de 183**: as
entradas P3181 e P3183 falharam por um erro MEU ao escrevê-las. Comparei com tolerância de 1e-9 números que copiei da saída IMPRESSA, já
arredondada (0,5578 era 0,55785; 32,036 era 32,0365). A medida estava certa; a régua da regressão, não. Corrigi as duas entradas para
comparar no arredondamento impresso.

**Regra nova (Parte 141):** uma entrada de regressão nunca compara com tolerância menor que a precisão com que o número foi impresso. Ou ela
compara pelo mesmo arredondamento, ou chama a função e guarda o número inteiro. É a regra da Parte 69 (números do texto passam por código)
aplicada à própria regressão: copiar da tela é escrever de cabeça.

**A rodada seguinte da regressão** (as Partes 136 a 140 de novo) deu 185 de 186, e a falha nova foi a P3191, a calibração das Partes 80 a 140.
Conferi a régua: ela está certa, e o número mudou porque a Parte 139 (G1, G2) e a 140 (a sua linha de placar, 9 previsões) ganharam
vereditos DEPOIS que eu fixei a entrada. A v4 foi de 360 para 369 previsões, e a v5 de 472 para 483. É a lição da Parte 109 (uma função
"das Partes A–B" passa A–B explícito), num caso que ela não cobria: A–B explícito ainda se move se B é uma parte aberta. A entrada agora usa
as Partes 80 a 138, que estão fechadas, e dá os mesmos (360, 325) e (472, 425).

**Regra (Parte 141, complemento):** uma entrada de regressão só fixa medidas sobre partes FECHADAS, isto é, com todos os vereditos escritos.

## O resultado da volta 8
A volta 8, registrada na Parte 135 (commit 4363101), deu **8 de 8**, com a tabela de vereditos na própria Parte 135, onde a P3187 a lê:
- 131 partes sem exceção, a regressão 174/174, 730 + 27 + 40 + 72 + 55 testes OK e as 90 rodadas IGUAIS;
- 8 de 1.888 linhas mudaram, exatamente as 8 nomeadas no registro, e 0 do mundo;
- a P1871 deu 1 e a P3175 deu 720, os dois no centro exato da conta.

Oito voltas, e nenhuma diferença do mundo em nenhuma. O contêiner reiniciou duas vezes durante a volta, e a retomada por parte recuperou as duas.

➡ Anterior: [Parte 140](ASI_AGI_parte140_leitor_dicionario_hex.md). ➡ Próxima: [Parte 142](ASI_AGI_parte142_enantiodromia.md).
